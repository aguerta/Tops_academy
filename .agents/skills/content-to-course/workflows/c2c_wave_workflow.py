"""Antigravity run_workflow script for code-driven Content-to-Course (C2C) wave orchestration.

Eliminates manual Director `manage_subagents` polling and premature `kill_all` errors by
executing subagent waves (`parallel(subagents, ...)`) and deterministic CLI transitions
(`run.py` / `dispatch.py`) directly in code.

Usage via `run_workflow`:
    run_workflow(
        ScriptPath=".agents/skills/content-to-course/workflows/c2c_wave_workflow.py",
        Description="Execute C2C wave or post-CTA pipeline",
        Args={
            "work_dir": "courses/<course_id>/work",
            "mode": "post_cta_pipeline",  # or "cta" | "authors" | "judges" | "repair" | "repair_and_rejudge"
            "output_dir": "courses",
            "python_exe": ".venv/Scripts/python.exe",
        },
    )
"""

import asyncio
import json
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_WF_ARGS: Dict[str, Any] = globals().get("args", {}) or {}

MANIFEST_BY_MODE: Dict[str, str] = {
    "cta": "cta.json",
    "authors": "authors.json",
    "judges": "judges.json",
    "repair": "repair.json",
}


def _default_python_exe() -> str:
    """Return the OS-appropriate default virtualenv Python executable."""
    return ".venv/Scripts/python.exe" if os.name == "nt" else ".venv/bin/python"


def _normalize_python_exe(raw_exe: Any) -> str:
    """Normalize Windows/POSIX separators when a path is supplied; keep bare command names intact."""
    exe = str(raw_exe or "").strip() or _default_python_exe()
    if "/" in exe or "\\" in exe:
        return str(Path(exe))
    return exe


def _build_python_cmd(python_exe: str, script: str, *cli_args: str) -> str:
    """Build a Windows PowerShell or POSIX shell command invoking a Python script."""
    script_path = str(Path(script))
    parts = [f'"{python_exe}"', script_path, *cli_args]
    joined = " ".join(parts)
    return f"& {joined}" if os.name == "nt" else joined


def _read_json_field(path: Path, field: str) -> str:
    """Read a stripped string field from a JSON object file, returning '' if unavailable."""
    if not path.is_file():
        return ""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return ""
    if not isinstance(data, dict):
        return ""
    return str(data.get(field) or "").strip()


def _resolve_director_id(work_path: Path) -> str:
    """Resolve the Director conversation ID from workflow args, lockfile, or state.json."""
    arg_id = str(_WF_ARGS.get("director_id") or "").strip()
    if arg_id:
        return arg_id
    lock_id = _read_json_field(work_path / ".c2c_subagent_lock.json", "director_conversation_id")
    if lock_id:
        return lock_id
    return _read_json_field(work_path / "state.json", "conversation_id")


def _build_run_py_cmd(python_exe: str, run_py: str, director_id: str, *cli_args: str) -> str:
    """Build a `run.py` CLI command, appending `--director-id` when available."""
    extra_args = ["--director-id", director_id] if director_id else []
    return _build_python_cmd(python_exe, run_py, *cli_args, *extra_args)


def _parse_ids(raw_ids: Any) -> List[str]:
    """Normalize explicit competency IDs from a sequence or comma/whitespace-delimited string."""
    if not raw_ids:
        return []
    if isinstance(raw_ids, str):
        tokens = [tok.strip() for tok in re.split(r"[\s,]+", raw_ids) if tok.strip()]
    elif isinstance(raw_ids, (list, tuple, set)):
        tokens = [str(tok).strip() for tok in raw_ids if str(tok).strip()]
    else:
        return []
    deduped: List[str] = []
    seen = set()
    for tok in tokens:
        if tok not in seen:
            seen.add(tok)
            deduped.append(tok)
    return deduped


def _build_subprocess_env(env_extra: Optional[Dict[str, str]] = None) -> Optional[Dict[str, str]]:
    """Build subprocess environment propagating director_id and any explicit env_extra."""
    merged: Dict[str, str] = {}
    if env_extra:
        for key, val in env_extra.items():
            if val is not None:
                merged[str(key)] = str(val)

    director_id = (
        merged.get("C2C_DIRECTOR_ID")
        or merged.get("ANTIGRAVITY_CONVERSATION_ID")
        or ""
    ).strip()
    if not director_id:
        work_dir_raw = str(_WF_ARGS.get("work_dir") or "").strip()
        if work_dir_raw:
            director_id = _resolve_director_id(Path(work_dir_raw))
        else:
            director_id = str(_WF_ARGS.get("director_id") or "").strip()

    if director_id:
        merged.setdefault("ANTIGRAVITY_CONVERSATION_ID", director_id)
        merged.setdefault("C2C_DIRECTOR_ID", director_id)

    if not merged:
        return None
    proc_env = os.environ.copy()
    proc_env.update(merged)
    return proc_env


async def run_cli(
    cmd: str,
    summary: str,
    env_extra: Optional[Dict[str, str]] = None,
) -> str:
    """Execute a deterministic C2C CLI stage as a local subprocess (no `call_tool` dependency) and enforce exit_code == 0."""
    log(f"[CLI] {summary}: {cmd}")
    if os.name == "nt":
        argv = ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd]
    else:
        argv = ["bash", "-lc", cmd]
    proc_env = _build_subprocess_env(env_extra)
    exec_kwargs: Dict[str, Any] = {
        "stdout": asyncio.subprocess.PIPE,
        "stderr": asyncio.subprocess.STDOUT,
    }
    if proc_env is not None:
        exec_kwargs["env"] = proc_env
    proc = await asyncio.create_subprocess_exec(*argv, **exec_kwargs)
    try:
        raw, _ = await asyncio.wait_for(proc.communicate(), timeout=300)
    except asyncio.TimeoutError:
        proc.kill()
        raise RuntimeError(f"CLI command timed out ({summary}) after 300s")
    out_str = raw.decode("utf-8", errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(f"CLI command failed ({summary}) with exit code {proc.returncode}:\n{out_str}")
    return f"Command exited with code 0.\n{out_str}"

async def run_wave_from_manifest(manifest_path: str, phase_name: str) -> List[str]:
    """Read a C2C dispatch manifest and run all declared workers concurrently."""
    path = Path(manifest_path)
    if not path.exists():
        raise FileNotFoundError(f"Dispatch manifest not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    subagents: List[Dict[str, Any]] = data.get("Subagents") or []
    total = len(subagents)

    phase(phase_name)
    log(f"Launching {total} workers for {phase_name}")
    if total == 0:
        log(f"Completed 0/0 workers for {phase_name} (empty wave)")
        return []

    for idx, s in enumerate(subagents):
        if not isinstance(s, dict) or not str(s.get("Prompt") or "").strip():
            raise ValueError(f"Subagent entry #{idx} in {path} is missing a non-empty 'Prompt'")

    results = await parallel(
        subagents,
        lambda s: agent(
            prompt=s["Prompt"],
            type_name=s.get("TypeName", "self"),
            role=s.get("Role", "C2C Worker"),
            model=s.get("Model", "inherit"),
            workspace="inherit",
            schema={"type": "string"},
        ),
    )
    log(f"Completed {len(results)}/{total} workers for {phase_name}")
    return results


def _unlink_if_exists(path: Path) -> None:
    """Remove a stale manifest or artifact before regenerating it."""
    try:
        if path.is_file():
            path.unlink()
    except OSError:
        pass


def _is_fresh_file(path: Path, min_mtime: float) -> bool:
    """Check whether `path` exists and its mtime is >= `min_mtime`."""
    if not path.is_file():
        return False
    if min_mtime <= 0.0:
        return True
    try:
        return path.stat().st_mtime >= min_mtime
    except OSError:
        return False


def _collect_failing_competencies(
    work_path: Path,
    matrix_min_mtime: float = 0.0,
    judge_min_mtime: float = 0.0,
) -> List[str]:
    """Inspect gates/repair_matrix and judge_comparison artifacts for failing competency IDs."""
    failing: List[str] = []
    seen = set()

    def _add(cid: Any) -> None:
        if isinstance(cid, str) and cid.strip() and cid.strip() not in seen:
            seen.add(cid.strip())
            failing.append(cid.strip())

    # 1. Check consolidated repair_matrix.json if emitted by `--stage gates` or `--stage repair-matrix`
    for candidate in (
        work_path / "repair_matrix.json",
        work_path / "dispatch" / "repair_matrix.json",
    ):
        if _is_fresh_file(candidate, matrix_min_mtime):
            try:
                matrix = json.loads(candidate.read_text(encoding="utf-8"))
                for key in ("failing_competencies", "repair_ids", "competency_ids", "ids"):
                    for cid in matrix.get(key, []) or []:
                        _add(cid)
                for item in matrix.get("items", []) or []:
                    if isinstance(item, dict):
                        _add(item.get("competency_id") or item.get("id"))
            except Exception:
                pass

    # 2. Check judge_comparison.json for rejected/flagged competencies
    judge_cmp = work_path / "judge_comparison.json"
    if _is_fresh_file(judge_cmp, judge_min_mtime):
        try:
            cmp_data = json.loads(judge_cmp.read_text(encoding="utf-8"))
            for cid in cmp_data.get("failing_competencies", []) or []:
                _add(cid)
            for item in cmp_data.get("disagreements", []) or []:
                if isinstance(item, dict):
                    _add(item.get("competency_id"))
        except Exception:
            pass

    return failing


async def _execute_repair_and_rejudge_cycle(
    work_path: Path,
    work_dir_arg: str,
    python_exe: str,
    run_py: str,
    dispatch_py: str,
    director_id: str,
    cli_env: Optional[Dict[str, str]],
    target_ids: List[str],
    repair_wave_label: str,
    rejudge_wave_label: str,
) -> Tuple[List[str], List[str]]:
    """Execute one atomic repair -> templates -> build -> surgical rejudge -> rejudge-compare -> gates cycle."""
    dispatch_dir = work_path / "dispatch"
    repair_manifest = dispatch_dir / "repair.json"
    _unlink_if_exists(repair_manifest)
    repair_args = ["dispatch-repair", "--work-dir", work_dir_arg]
    if target_ids:
        repair_args.extend(["--ids", *target_ids])
    repair_dispatch_start = time.time()
    await run_cli(
        _build_python_cmd(python_exe, dispatch_py, *repair_args),
        "C2C dispatch repair",
        env_extra=cli_env,
    )

    repair_results: List[str] = []
    rejudge_results: List[str] = []
    if _is_fresh_file(repair_manifest, repair_dispatch_start):
        repair_results = await run_wave_from_manifest(
            str(repair_manifest),
            repair_wave_label,
        )
        await run_cli(
            _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "templates", "--work-dir", work_dir_arg),
            "C2C post-repair stage templates",
            env_extra=cli_env,
        )
        await run_cli(
            _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "build", "--work-dir", work_dir_arg),
            "C2C post-repair stage build",
            env_extra=cli_env,
        )
        if target_ids:
            rejudge_manifest = dispatch_dir / "judges.json"
            _unlink_if_exists(rejudge_manifest)
            rejudge_start = time.time()
            await run_cli(
                _build_run_py_cmd(
                    python_exe,
                    run_py,
                    director_id,
                    "--stage",
                    "rejudge",
                    "--ids",
                    *target_ids,
                    "--work-dir",
                    work_dir_arg,
                ),
                "C2C stage surgical rejudge",
                env_extra=cli_env,
            )
            if _is_fresh_file(rejudge_manifest, rejudge_start):
                rejudge_results = await run_wave_from_manifest(
                    str(rejudge_manifest),
                    rejudge_wave_label,
                )
            await run_cli(
                _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "rejudge-compare", "--work-dir", work_dir_arg),
                "C2C stage rejudge-compare",
                env_extra=cli_env,
            )
        await run_cli(
            _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "gates", "--work-dir", work_dir_arg),
            "C2C post-repair stage gates",
            env_extra=cli_env,
        )

    return repair_results, rejudge_results


async def run_c2c_workflow() -> Dict[str, Any]:
    """Entry point for C2C wave, repair_and_rejudge, or post-CTA pipeline execution."""
    work_dir_raw = str(_WF_ARGS.get("work_dir") or "").strip()
    if not work_dir_raw:
        raise ValueError("Missing required workflow arg: 'work_dir' (e.g. 'courses/<course_id>/work')")

    mode = str(_WF_ARGS.get("mode", "wave") or "wave").strip().lower()
    python_exe = _normalize_python_exe(_WF_ARGS.get("python_exe"))

    work_path = Path(work_dir_raw)
    work_dir_arg = f'"{work_path}"'
    dispatch_dir = work_path / "dispatch"
    run_py = ".agents/skills/content-to-course/run.py"
    dispatch_py = ".agents/skills/content-to-course/dispatch.py"

    director_id = _resolve_director_id(work_path)
    cli_env: Optional[Dict[str, str]] = (
        {"ANTIGRAVITY_CONVERSATION_ID": director_id, "C2C_DIRECTOR_ID": director_id}
        if director_id
        else None
    )

    # Single-wave execution modes: "cta", "authors", "judges", "repair" (or default "wave" -> manifest_name arg)
    if mode in MANIFEST_BY_MODE or mode == "wave":
        manifest_file = str(_WF_ARGS.get("manifest") or MANIFEST_BY_MODE.get(mode, "authors.json")).strip()
        manifest_path = dispatch_dir / manifest_file
        phase_label = f"C2C Wave: {mode.upper()}"
        results = await run_wave_from_manifest(str(manifest_path), phase_label)
        summary = {"mode": mode, "work_dir": str(work_path), "workers_completed": len(results)}
        print(json.dumps(summary, ensure_ascii=False))
        return summary

    if mode == "repair_and_rejudge":
        phase("Atomic Repair & Surgical Rejudge")
        explicit_ids = _parse_ids(_WF_ARGS.get("ids"))
        if explicit_ids:
            target_ids = explicit_ids
        else:
            _unlink_if_exists(work_path / "repair_matrix.json")
            _unlink_if_exists(dispatch_dir / "repair_matrix.json")
            repair_matrix_start = time.time()
            await run_cli(
                _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "repair-matrix", "--work-dir", work_dir_arg),
                "C2C stage repair-matrix",
                env_extra=cli_env,
            )
            target_ids = _collect_failing_competencies(
                work_path,
                matrix_min_mtime=repair_matrix_start,
            )
            if not target_ids:
                summary = {
                    "mode": mode,
                    "work_dir": str(work_path),
                    "ids": [],
                    "repairs_completed": 0,
                    "rejudges_completed": 0,
                }
                print(json.dumps(summary, ensure_ascii=False))
                return summary

        repair_results, rejudge_results = await _execute_repair_and_rejudge_cycle(
            work_path=work_path,
            work_dir_arg=work_dir_arg,
            python_exe=python_exe,
            run_py=run_py,
            dispatch_py=dispatch_py,
            director_id=director_id,
            cli_env=cli_env,
            target_ids=target_ids,
            repair_wave_label="Atomic Repair Wave",
            rejudge_wave_label="Atomic Surgical Rejudge Wave",
        )
        summary = {
            "mode": mode,
            "work_dir": str(work_path),
            "ids": target_ids,
            "repairs_completed": len(repair_results),
            "rejudges_completed": len(rejudge_results),
        }
        print(json.dumps(summary, ensure_ascii=False))
        return summary

    if mode != "post_cta_pipeline":
        raise ValueError(
            f"Unsupported mode '{mode}'. Expected one of: 'cta', 'authors', 'judges', 'repair', 'repair_and_rejudge', 'post_cta_pipeline'."
        )

    # Automated post-CTA pipeline:
    # shard -> dispatch-authors -> parallel(authors) -> templates -> build -> dispatch-judges -> parallel(judges) -> judge-compare -> gates
    phase("Stage 2: Sharding")
    shard_cmd_args = ["--stage", "shard", "--work-dir", work_dir_arg]
    if _WF_ARGS.get("shards") is not None:
        shard_cmd_args.extend(["--shards", str(_WF_ARGS["shards"])])
    if _WF_ARGS.get("comps_per_shard") is not None:
        shard_cmd_args.extend(["--comps-per-shard", str(_WF_ARGS["comps_per_shard"])])
    if _WF_ARGS.get("templates_per_modality") is not None:
        shard_cmd_args.extend(["--templates-per-modality", str(_WF_ARGS["templates_per_modality"])])
    await run_cli(
        _build_run_py_cmd(python_exe, run_py, director_id, *shard_cmd_args),
        "C2C stage shard",
        env_extra=cli_env,
    )

    phase("Stage 3: Dispatch & Run Authors")
    author_dispatch_args = ["dispatch-authors", "--work-dir", work_dir_arg]
    if _WF_ARGS.get("templates_per_modality") is not None:
        author_dispatch_args.extend(["--templates-per-modality", str(_WF_ARGS["templates_per_modality"])])
    await run_cli(
        _build_python_cmd(python_exe, dispatch_py, *author_dispatch_args),
        "C2C dispatch authors",
        env_extra=cli_env,
    )
    author_results = await run_wave_from_manifest(
        str(dispatch_dir / "authors.json"),
        "Stage 3: Shard Authors Wave",
    )

    phase("Stage 4: Templates & Build")
    await run_cli(
        _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "templates", "--work-dir", work_dir_arg),
        "C2C stage templates",
        env_extra=cli_env,
    )
    await run_cli(
        _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "build", "--work-dir", work_dir_arg),
        "C2C stage build",
        env_extra=cli_env,
    )

    phase("Stage 5: Blind Epistemic Judges")
    judges_manifest = dispatch_dir / "judges.json"
    _unlink_if_exists(judges_manifest)
    stage5_start = time.time()
    await run_cli(
        _build_python_cmd(python_exe, dispatch_py, "dispatch-judges", "--work-dir", work_dir_arg),
        "C2C dispatch judges",
        env_extra=cli_env,
    )
    if not _is_fresh_file(judges_manifest, stage5_start):
        raise FileNotFoundError(f"Fresh judges manifest not generated by dispatch-judges: {judges_manifest}")
    judge_results = await run_wave_from_manifest(
        str(judges_manifest),
        "Stage 5: Blind Judges Wave",
    )
    await run_cli(
        _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "judge-compare", "--work-dir", work_dir_arg),
        "C2C stage judge-compare",
        env_extra=cli_env,
    )

    phase("Stage 6: Quality Gates")
    _unlink_if_exists(work_path / "repair_matrix.json")
    _unlink_if_exists(dispatch_dir / "repair_matrix.json")
    gates_start = time.time()
    gates_out = await run_cli(
        _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "gates", "--work-dir", work_dir_arg),
        "C2C stage gates",
        env_extra=cli_env,
    )

    # Check if at most 1 consolidated shard-level repair + surgical rejudge pass is needed
    failing_cids = _collect_failing_competencies(
        work_path,
        matrix_min_mtime=gates_start,
        judge_min_mtime=stage5_start,
    )
    repair_results: List[str] = []
    if failing_cids or "dispatch-repair" in (gates_out or ""):
        phase("Stage 6B: Consolidated Shard Repair & Surgical Rejudge (Max 1 Pass)")
        _unlink_if_exists(work_path / "repair_matrix.json")
        _unlink_if_exists(dispatch_dir / "repair_matrix.json")
        repair_matrix_start = time.time()
        await run_cli(
            _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "repair-matrix", "--work-dir", work_dir_arg),
            "C2C stage repair-matrix",
            env_extra=cli_env,
        )
        failing_cids = _collect_failing_competencies(
            work_path,
            matrix_min_mtime=repair_matrix_start,
            judge_min_mtime=stage5_start,
        )
        repair_results, _ = await _execute_repair_and_rejudge_cycle(
            work_path=work_path,
            work_dir_arg=work_dir_arg,
            python_exe=python_exe,
            run_py=run_py,
            dispatch_py=dispatch_py,
            director_id=director_id,
            cli_env=cli_env,
            target_ids=failing_cids,
            repair_wave_label="Stage 6B: Consolidated Repair Wave",
            rejudge_wave_label="Stage 6B: Surgical Rejudge Wave",
        )

    summary = {
        "mode": mode,
        "work_dir": str(work_path),
        "authors_completed": len(author_results),
        "judges_completed": len(judge_results),
        "repairs_completed": len(repair_results),
    }
    print(json.dumps(summary, ensure_ascii=False))
    return summary


if "parallel" in globals():
    await run_c2c_workflow()
