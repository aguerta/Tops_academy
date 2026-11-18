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
            "mode": "post_cta_pipeline",  # or "cta" | "authors" | "judges" | "repair"
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
from typing import Any, Dict, List

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


async def run_cli(cmd: str, summary: str) -> str:
    """Execute a deterministic C2C CLI stage as a local subprocess (no `call_tool` dependency) and enforce exit_code == 0."""
    log(f"[CLI] {summary}: {cmd}")
    if os.name == "nt":
        argv = ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd]
    else:
        argv = ["bash", "-lc", cmd]
    proc = await asyncio.create_subprocess_exec(
        *argv,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
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


async def run_c2c_workflow() -> Dict[str, Any]:
    """Entry point for C2C wave or post-CTA pipeline execution."""
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

    # Single-wave execution modes: "cta", "authors", "judges", "repair" (or default "wave" -> manifest_name arg)
    if mode in MANIFEST_BY_MODE or mode == "wave":
        manifest_file = str(_WF_ARGS.get("manifest") or MANIFEST_BY_MODE.get(mode, "authors.json")).strip()
        manifest_path = dispatch_dir / manifest_file
        phase_label = f"C2C Wave: {mode.upper()}"
        results = await run_wave_from_manifest(str(manifest_path), phase_label)
        summary = {"mode": mode, "work_dir": str(work_path), "workers_completed": len(results)}
        print(json.dumps(summary, ensure_ascii=False))
        return summary

    if mode != "post_cta_pipeline":
        raise ValueError(
            f"Unsupported mode '{mode}'. Expected one of: 'cta', 'authors', 'judges', 'repair', 'post_cta_pipeline'."
        )

    # Automated post-CTA pipeline:
    # shard -> dispatch-authors -> parallel(authors) -> templates -> build -> dispatch-judges -> parallel(judges) -> judge-compare -> gates
    phase("Stage 2: Sharding")
    await run_cli(
        _build_python_cmd(python_exe, run_py, "--stage", "shard", "--work-dir", work_dir_arg),
        "C2C stage shard",
    )

    phase("Stage 3: Dispatch & Run Authors")
    await run_cli(
        _build_python_cmd(python_exe, dispatch_py, "dispatch-authors", "--work-dir", work_dir_arg),
        "C2C dispatch authors",
    )
    author_results = await run_wave_from_manifest(
        str(dispatch_dir / "authors.json"),
        "Stage 3: Shard Authors Wave",
    )

    phase("Stage 4: Templates & Build")
    await run_cli(
        _build_python_cmd(python_exe, run_py, "--stage", "templates", "--work-dir", work_dir_arg),
        "C2C stage templates",
    )
    await run_cli(
        _build_python_cmd(python_exe, run_py, "--stage", "build", "--work-dir", work_dir_arg),
        "C2C stage build",
    )

    phase("Stage 5: Blind Epistemic Judges")
    judges_manifest = dispatch_dir / "judges.json"
    _unlink_if_exists(judges_manifest)
    stage5_start = time.time()
    await run_cli(
        _build_python_cmd(python_exe, dispatch_py, "dispatch-judges", "--work-dir", work_dir_arg),
        "C2C dispatch judges",
    )
    if not _is_fresh_file(judges_manifest, stage5_start):
        raise FileNotFoundError(f"Fresh judges manifest not generated by dispatch-judges: {judges_manifest}")
    judge_results = await run_wave_from_manifest(
        str(judges_manifest),
        "Stage 5: Blind Judges Wave",
    )
    await run_cli(
        _build_python_cmd(python_exe, run_py, "--stage", "judge-compare", "--work-dir", work_dir_arg),
        "C2C stage judge-compare",
    )

    phase("Stage 6: Quality Gates")
    _unlink_if_exists(work_path / "repair_matrix.json")
    _unlink_if_exists(dispatch_dir / "repair_matrix.json")
    gates_start = time.time()
    gates_out = await run_cli(
        _build_python_cmd(python_exe, run_py, "--stage", "gates", "--work-dir", work_dir_arg),
        "C2C stage gates",
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
            _build_python_cmd(python_exe, run_py, "--stage", "repair-matrix", "--work-dir", work_dir_arg),
            "C2C stage repair-matrix",
        )
        failing_cids = _collect_failing_competencies(
            work_path,
            matrix_min_mtime=repair_matrix_start,
            judge_min_mtime=stage5_start,
        )
        repair_manifest = dispatch_dir / "repair.json"
        _unlink_if_exists(repair_manifest)
        repair_args = ["dispatch-repair", "--work-dir", work_dir_arg]
        if failing_cids:
            repair_args.extend(["--ids", *failing_cids])
        repair_dispatch_start = time.time()
        await run_cli(
            _build_python_cmd(python_exe, dispatch_py, *repair_args),
            "C2C dispatch repair",
        )

        if _is_fresh_file(repair_manifest, repair_dispatch_start):
            repair_results = await run_wave_from_manifest(
                str(repair_manifest),
                "Stage 6B: Consolidated Repair Wave",
            )
            await run_cli(
                _build_python_cmd(python_exe, run_py, "--stage", "templates", "--work-dir", work_dir_arg),
                "C2C post-repair stage templates",
            )
            await run_cli(
                _build_python_cmd(python_exe, run_py, "--stage", "build", "--work-dir", work_dir_arg),
                "C2C post-repair stage build",
            )
            if failing_cids:
                rejudge_manifest = dispatch_dir / "judges.json"
                _unlink_if_exists(rejudge_manifest)
                rejudge_start = time.time()
                await run_cli(
                    _build_python_cmd(python_exe, run_py, "--stage", "rejudge", "--ids", *failing_cids, "--work-dir", work_dir_arg),
                    "C2C stage surgical rejudge",
                )
                if _is_fresh_file(rejudge_manifest, rejudge_start):
                    await run_wave_from_manifest(
                        str(rejudge_manifest),
                        "Stage 6B: Surgical Rejudge Wave",
                    )
                await run_cli(
                    _build_python_cmd(python_exe, run_py, "--stage", "rejudge-compare", "--work-dir", work_dir_arg),
                    "C2C stage rejudge-compare",
                )
            await run_cli(
                _build_python_cmd(python_exe, run_py, "--stage", "gates", "--work-dir", work_dir_arg),
                "C2C post-repair stage gates",
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
