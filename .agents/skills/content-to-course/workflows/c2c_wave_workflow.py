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
import random
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_WF_ARGS: Dict[str, Any] = globals().get("args", {}) or {}

DEFAULT_MAX_CONCURRENCY: int = 12
DEFAULT_WORKER_RETRIES: int = 2
DEFAULT_RETRY_BACKOFF_S: Tuple[float, ...] = (3.0, 8.0)
DEFAULT_QUOTA_RETRIES: int = 4
DEFAULT_QUOTA_BACKOFF_S: Tuple[float, ...] = (12.0, 25.0, 45.0, 60.0)
DEFAULT_QUOTA_ABORT_RESET_S: float = 300.0


class QuotaPausedError(RuntimeError):
    """Raised when a wave aborts early due to a long HTTP 429 quota reset."""


def _is_quota_error(reason: str) -> bool:
    """Return True when a worker collapse reason indicates an HTTP 429 / API quota error."""
    low = str(reason or "").lower()
    return any(tok in low for tok in ("429", "resource_exhausted", "ratelimiterror", "exhausted your capacity"))


def _parse_quota_reset_seconds(reason: str) -> float:
    """Parse 'Resets in XhYmZs' from a quota error string; returns 0.0 when absent."""
    m = re.search(r"resets\s+in\s+((?:\d+\s*[hms]\s*)+)", str(reason or ""), re.IGNORECASE)
    if not m:
        return 0.0
    span = m.group(1)
    total_s = 0.0
    for val_s, unit in re.findall(r"(\d+)\s*([hms])", span, re.IGNORECASE):
        val = int(val_s)
        u = unit.lower()
        if u == "h":
            total_s += val * 3600.0
        elif u == "m":
            total_s += val * 60.0
        elif u == "s":
            total_s += val
    return total_s

MANIFEST_BY_MODE: Dict[str, str] = {
    "cta": "cta.json",
    "cta_harmonize": "cta_reduce.json",
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


async def run_cli_status(
    cmd: str,
    summary: str,
    env_extra: Optional[Dict[str, str]] = None,
) -> Tuple[int, str]:
    """Execute a C2C CLI stage via `run_cli`, returning `(returncode, output)` without raising on non-zero exit."""
    try:
        out = await run_cli(cmd, summary, env_extra=env_extra)
        return 0, out
    except RuntimeError as exc:
        msg = str(exc)
        m = re.search(r"with exit code (\d+)", msg)
        rc = int(m.group(1)) if m else 1
        return rc, msg

_PLATFORM_FAILURE_MARKERS: Tuple[str, ...] = (
    "UNKNOWN",
    "WorkflowError",
    "MODEL_PLACEHOLDER_",
    "model not found",
    "RESOURCE_EXHAUSTED",
    "failed to run agent",
    "RateLimitError",
)


def _is_worker_collapse(
    prompt: str,
    result: Any,
    err: Optional[BaseException],
    elapsed_s: float,
) -> Tuple[bool, str]:
    """Detect silent 0s/UNKNOWN worker collapses, empty replies, or platform model errors."""
    if err is not None:
        return True, f"exception: {err}"
    res_str = str(result or "").strip()
    if not res_str:
        return True, "empty worker response"
    has_terminal = ("DONE:" in res_str) or ("BLOCKED:" in res_str)
    if not has_terminal:
        for marker in _PLATFORM_FAILURE_MARKERS:
            if marker in res_str:
                return True, f"platform error marker '{marker}'"
        requires_done = ("DONE:" in prompt) or ("[SCOPE-LOCK]" in prompt)
        if requires_done and elapsed_s < 5.0:
            return True, f"silent early exit in {elapsed_s:.2f}s without DONE:/BLOCKED:"
    return False, ""


async def run_wave_from_manifest(
    manifest_path: str,
    phase_name: str,
    max_concurrency: Optional[int] = None,
    max_retries: Optional[int] = None,
    max_concurrent_batch: int = 0,
) -> List[str]:
    """Read a C2C dispatch manifest and run workers with bounded concurrency, startup jitter, and auto-retry."""
    path = Path(manifest_path)
    if not path.exists():
        raise FileNotFoundError(f"Dispatch manifest not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    subagents: List[Dict[str, Any]] = data.get("Subagents") or []
    total = len(subagents)

    phase(phase_name)
    if total == 0:
        log(f"Launching 0 workers for {phase_name}")
        log(f"Completed 0/0 workers for {phase_name} (empty wave)")
        return []

    for idx, s in enumerate(subagents):
        if not isinstance(s, dict) or not str(s.get("Prompt") or "").strip():
            raise ValueError(f"Subagent entry #{idx} in {path} is missing a non-empty 'Prompt'")

    eff_conc = max(
        1,
        int(max_concurrency if max_concurrency is not None else (_WF_ARGS.get("max_concurrency") or DEFAULT_MAX_CONCURRENCY)),
    )
    eff_retries = max(
        0,
        int(max_retries if max_retries is not None else (_WF_ARGS.get("worker_max_retries") if _WF_ARGS.get("worker_max_retries") is not None else DEFAULT_WORKER_RETRIES)),
    )
    eff_quota_retries = max(
        eff_retries,
        int(
            _WF_ARGS.get("quota_max_retries")
            if _WF_ARGS.get("quota_max_retries") is not None
            else (max_retries if max_retries is not None else DEFAULT_QUOTA_RETRIES)
        ),
    )
    stagger_step = float(
        _WF_ARGS.get("startup_stagger_s")
        if _WF_ARGS.get("startup_stagger_s") is not None
        else 0.12
    )
    raw_backoff = _WF_ARGS.get("retry_backoff_s")
    if isinstance(raw_backoff, (list, tuple)) and raw_backoff:
        backoffs = tuple(float(x) for x in raw_backoff)
    elif raw_backoff is not None:
        backoffs = (float(raw_backoff),)
    else:
        backoffs = DEFAULT_RETRY_BACKOFF_S

    raw_quota_backoff = _WF_ARGS.get("quota_retry_backoff_s")
    if isinstance(raw_quota_backoff, (list, tuple)) and raw_quota_backoff:
        quota_backoffs = tuple(float(x) for x in raw_quota_backoff)
    elif raw_quota_backoff is not None:
        quota_backoffs = (float(raw_quota_backoff),)
    else:
        quota_backoffs = DEFAULT_QUOTA_BACKOFF_S

    quota_abort_reset_s = float(
        _WF_ARGS.get("quota_abort_reset_s")
        if _WF_ARGS.get("quota_abort_reset_s") is not None
        else DEFAULT_QUOTA_ABORT_RESET_S
    )
    quota_abort_event = asyncio.Event()
    quota_abort_info: Dict[str, Any] = {"reason": "", "reset_s": 0.0, "completed": 0}

    log(f"Launching {total} workers for {phase_name} (max_concurrency={eff_conc}, max_retries={eff_retries}, quota_max_retries={eff_quota_retries})")
    sem = asyncio.Semaphore(eff_conc)
    slot_counter = {"next": 0}

    async def _run_worker(s: Dict[str, Any]) -> str:
        slot = slot_counter["next"]
        slot_counter["next"] += 1
        role_label = str(s.get("Role", "C2C Worker"))
        prompt_text = str(s["Prompt"])

        if quota_abort_event.is_set():
            return ""

        if total > 1 and slot > 0 and stagger_step > 0.0:
            delay = (slot % eff_conc) * stagger_step + random.uniform(0.0, stagger_step * 0.5)
            if delay > 0.0:
                await asyncio.sleep(delay)

        if quota_abort_event.is_set():
            return ""

        async with sem:
            last_err: Optional[Exception] = None
            last_res: Any = ""
            attempt = 0
            while True:
                if quota_abort_event.is_set():
                    return ""
                t0 = time.monotonic()
                err_caught: Optional[Exception] = None
                res: Any = ""
                try:
                    res = await agent(
                        prompt=prompt_text,
                        type_name=s.get("TypeName", "self"),
                        role=role_label,
                        model=s.get("Model", "inherit"),
                        workspace="inherit",
                        schema={"type": "string"},
                    )
                except Exception as exc:
                    err_caught = exc
                elapsed = time.monotonic() - t0
                collapsed, reason = _is_worker_collapse(prompt_text, res, err_caught, elapsed)
                if not collapsed:
                    quota_abort_info["completed"] += 1
                    return str(res)
                last_err = err_caught
                last_res = res
                is_quota = _is_quota_error(reason)
                if is_quota:
                    reset_s = _parse_quota_reset_seconds(reason)
                    if reset_s > quota_abort_reset_s:
                        if not quota_abort_event.is_set():
                            quota_abort_info["reason"] = reason
                            quota_abort_info["reset_s"] = reset_s
                            quota_abort_event.set()
                            log(
                                f"[QUOTA-CIRCUIT-BREAKER] Long quota reset detected ({reset_s:.0f}s > {quota_abort_reset_s:.0f}s) "
                                f"on {role_label}; aborting remaining wave spawns."
                            )
                        break
                allowed_retries = eff_quota_retries if is_quota else eff_retries
                if attempt < allowed_retries:
                    if is_quota:
                        base_wait = quota_backoffs[min(attempt, len(quota_backoffs) - 1)] if quota_backoffs else 0.0
                        wait_s = base_wait * random.uniform(0.85, 1.15) if base_wait > 0.0 else 0.0
                    else:
                        wait_s = backoffs[min(attempt, len(backoffs) - 1)] if backoffs else 0.0
                    log(
                        f"[AUTO-RETRY] {role_label} collapsed on attempt {attempt + 1}/{allowed_retries + 1} "
                        f"({reason}); retrying in {wait_s:.1f}s"
                    )
                    if wait_s > 0.0:
                        await asyncio.sleep(wait_s)
                    attempt += 1
                else:
                    log(
                        f"[WORKER-EXHAUSTED] {role_label} failed after {attempt + 1} attempts ({reason})"
                    )
                    break
            if quota_abort_event.is_set():
                return ""
            if last_err is not None:
                raise last_err
            return str(last_res or "")

    if max_concurrent_batch > 0 and len(subagents) > max_concurrent_batch:
        results: List[str] = []
        total_batches = (len(subagents) + max_concurrent_batch - 1) // max_concurrent_batch
        for batch_idx in range(0, len(subagents), max_concurrent_batch):
            if quota_abort_event.is_set():
                break
            batch = subagents[batch_idx : batch_idx + max_concurrent_batch]
            log(f"[WAVE-BATCH] {phase_name}: batch {batch_idx // max_concurrent_batch + 1}/{total_batches} ({len(batch)} workers)")
            results.extend(await parallel(batch, _run_worker))
    else:
        results = await parallel(subagents, _run_worker)
    if quota_abort_event.is_set():
        raise QuotaPausedError(
            f"PAUSED_QUOTA: {quota_abort_info['reason']} "
            f"(completed {quota_abort_info['completed']}/{total} workers before abort)"
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
    """Check whether `path` exists and its mtime is >= `min_mtime` (with 50ms NTFS clock tolerance)."""
    if not path.is_file():
        return False
    if min_mtime <= 0.0:
        return True
    try:
        return path.stat().st_mtime >= (min_mtime - 0.05)
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


def _has_fresh_repair_compile(
    work_path: Path,
    shard_id: str,
    min_ts: float,
) -> bool:
    """Verify check_runs >= 1 after `min_ts` via `.check_attempts/compile_<shard>.json` or fresh `<shard>.json`."""
    shard_json = work_path / "shards" / f"{shard_id}.json"
    if _is_fresh_file(shard_json, min_ts - 0.5):
        return True
    norm_sid = shard_id.lower().strip()
    att_file = work_path / ".check_attempts" / f"compile_{norm_sid}.json"
    if _is_fresh_file(att_file, min_ts - 0.5):
        try:
            att_data = json.loads(att_file.read_text(encoding="utf-8"))
            if int(att_data.get("distinct_compiles", att_data.get("count", 0)) or 0) >= 1:
                return True
        except Exception:
            return True
    return False


def _collect_unfinished_repair_ids(
    work_path: Path,
    repair_manifest: Path,
    repair_results: List[str],
    min_ts: float,
) -> List[str]:
    """Identify targeted competencies whose Repair Engineer closed silently without `check_runs >= 1` or `DONE:`."""
    try:
        manifest_data = json.loads(repair_manifest.read_text(encoding="utf-8"))
    except Exception:
        return []
    subagents = manifest_data.get("Subagents") or []
    if not subagents:
        return []

    unfinished: List[str] = []
    seen = set()
    for idx, entry in enumerate(subagents):
        if not isinstance(entry, dict):
            continue
        shard_id = str(entry.get("shard_id") or "").strip()
        if not shard_id:
            # Skip synthetic test manifests that omit real shard metadata
            continue
        prompt_text = str(entry.get("Prompt") or "")
        res_text = str(repair_results[idx] if idx < len(repair_results) else "").strip()
        has_done = ("DONE:" in res_text) or ("DONE:" not in prompt_text)
        has_blocked = "BLOCKED:" in res_text
        has_compile = _has_fresh_repair_compile(work_path, shard_id, min_ts)
        if (not has_compile or (not has_done and not has_blocked)):
            cids = entry.get("assigned_competencies") or []
            if isinstance(cids, str):
                cids = _parse_ids(cids)
            if not cids and entry.get("assigned_competency"):
                cids = _parse_ids(entry.get("assigned_competency"))
            log(
                f"[REPAIR-CLOSE-GUARD] Shard '{shard_id}' did not verify close "
                f"(has_compile={has_compile}, has_done={has_done}) for {cids}"
            )
            for cid in cids:
                cid_s = str(cid).strip()
                if cid_s and cid_s not in seen:
                    seen.add(cid_s)
                    unfinished.append(cid_s)
    return unfinished


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
    raise_on_gates_fail: bool = True,
) -> Tuple[List[str], List[str]]:
    """Execute one atomic repair -> templates -> build -> surgical rejudge -> rejudge-compare -> gates cycle."""
    dispatch_dir = work_path / "dispatch"
    rejudge_ckpt = work_path / ".rejudge_pending.json"
    force_repair = bool(_WF_ARGS.get("force_repair"))

    resume_rejudge = False
    if target_ids and not force_repair and rejudge_ckpt.is_file():
        try:
            ckpt_data = json.loads(rejudge_ckpt.read_text(encoding="utf-8"))
            ckpt_ids = ckpt_data.get("ids") or []
            built_at = float(ckpt_data.get("built_at") or 0.0)
            shards_dir = work_path / "shards"
            shards_modified_after = False
            if shards_dir.is_dir() and built_at > 0.0:
                shards_modified_after = any(
                    sf.stat().st_mtime > built_at
                    for sf in shards_dir.glob("*.py")
                )
            if (
                isinstance(ckpt_ids, list)
                and sorted(str(x) for x in ckpt_ids) == sorted(str(x) for x in target_ids)
                and not shards_modified_after
            ):
                resume_rejudge = True
                log(f"[REJUDGE-RESUME] Skipping already-built Repair Wave and resuming Surgical Rejudge for {target_ids}")
        except Exception:
            resume_rejudge = False

    repair_results: List[str] = []
    rejudge_results: List[str] = []
    ran_build = resume_rejudge

    if not resume_rejudge:
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

        if _is_fresh_file(repair_manifest, repair_dispatch_start):
            repair_results = await run_wave_from_manifest(
                str(repair_manifest),
                repair_wave_label,
            )
            unfinished_cids = _collect_unfinished_repair_ids(
                work_path,
                repair_manifest,
                repair_results,
                repair_dispatch_start,
            )
            if unfinished_cids:
                log(f"[REPAIR-CLOSE-GUARD] Re-dispatching unfinished repairs once for: {unfinished_cids}")
                _unlink_if_exists(repair_manifest)
                retry_start = time.time()
                await run_cli(
                    _build_python_cmd(
                        python_exe,
                        dispatch_py,
                        "dispatch-repair",
                        "--work-dir",
                        work_dir_arg,
                        "--ids",
                        *unfinished_cids,
                    ),
                    "C2C dispatch repair (close-guard retry)",
                    env_extra=cli_env,
                )
                if _is_fresh_file(repair_manifest, retry_start):
                    retry_results = await run_wave_from_manifest(
                        str(repair_manifest),
                        f"{repair_wave_label} (Close-Guard Retry)",
                    )
                    repair_results.extend(retry_results)
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
            ran_build = True
            if target_ids:
                try:
                    rejudge_ckpt.write_text(
                        json.dumps({"ids": list(target_ids), "built_at": time.time()}, ensure_ascii=False),
                        encoding="utf-8",
                    )
                except OSError:
                    pass

    if ran_build:
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
            # Stage 5B LQAS inside rejudge cycle if rejudge triggered kernel_override
            for jr_cand in (work_path / "judge_report_rejudge.json", work_path / "judge_report.json"):
                if _is_fresh_file(jr_cand, rejudge_start):
                    try:
                        jr_data = json.loads(jr_cand.read_text(encoding="utf-8"))
                    except Exception:
                        jr_data = {}
                    if bool(jr_data.get("lqas_followup_required")) and (jr_data.get("single_seed_override_templates") or []):
                        phase("Stage 5B (Rejudge): Adaptive Two-Stage LQAS Confirmation")
                        _unlink_if_exists(rejudge_manifest)
                        lqas_start = time.time()
                        await run_cli(
                            _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "lqas-rejudge", "--work-dir", work_dir_arg),
                            "C2C stage lqas-rejudge",
                            env_extra=cli_env,
                        )
                        if _is_fresh_file(rejudge_manifest, lqas_start):
                            await run_wave_from_manifest(
                                str(rejudge_manifest),
                                "Stage 5B (Rejudge): Adaptive LQAS Confirmation Wave",
                            )
                            await run_cli(
                                _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "lqas-compare", "--work-dir", work_dir_arg),
                                "C2C stage lqas-compare",
                                env_extra=cli_env,
                            )
                    break
            _unlink_if_exists(rejudge_ckpt)
        if raise_on_gates_fail:
            await run_cli(
                _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "gates", "--work-dir", work_dir_arg),
                "C2C post-repair stage gates",
                env_extra=cli_env,
            )
        else:
            await run_cli_status(
                _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "gates", "--work-dir", work_dir_arg),
                "C2C post-repair stage gates",
                env_extra=cli_env,
            )

    return repair_results, rejudge_results


async def _run_cta_pipeline(
    work_path: Path,
    work_dir_arg: str,
    python_exe: str,
    run_py: str,
    director_id: str,
    cli_env: Optional[Dict[str, str]],
) -> Dict[str, Any]:
    """Execute Stage 1B CTA Mappers -> validate/merge -> CTA Harmonizer (if needed) -> apply & certify."""
    dispatch_dir = work_path / "dispatch"
    phase("Stage 1B: CTA Architects & Harmonization")
    cta_manifest = dispatch_dir / "cta.json"
    cta_results = await run_wave_from_manifest(str(cta_manifest), "Stage 1B: CTA Architects Wave")

    reduce_manifest = dispatch_dir / "cta_reduce.json"
    _unlink_if_exists(reduce_manifest)
    cta_stage_start = time.time()
    await run_cli(
        _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "cta", "--work-dir", work_dir_arg),
        "C2C stage cta (validate or emit cta-reduce)",
        env_extra=cli_env,
    )
    harmonizer_results: List[str] = []
    if _is_fresh_file(reduce_manifest, cta_stage_start):
        harmonizer_results = await run_wave_from_manifest(
            str(reduce_manifest),
            "Stage 1B: CTA Harmonizer",
        )
        await run_cli(
            _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "cta", "--work-dir", work_dir_arg),
            "C2C stage cta (apply harmonize & certify)",
            env_extra=cli_env,
        )
    return {
        "cta_workers_completed": len(cta_results),
        "harmonizer_completed": len(harmonizer_results),
        "cta_json": str((work_path / "cta.json").as_posix()),
    }


def _find_pending_shards(work_path: Path) -> Optional[List[str]]:
    """Return list of shard IDs missing their compiled shard_XX.json, or None if not yet sharded."""
    manifest_path = work_path / "shards" / "pre_shard_manifest.json"
    if not manifest_path.is_file():
        return None
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    raw_shards = manifest.get("shards") or []
    if not isinstance(raw_shards, list) or not raw_shards:
        return None
    pending: List[str] = []
    for entry in raw_shards:
        sid = entry.get("shard_id") if isinstance(entry, dict) else str(entry)
        if not sid:
            continue
        cert_json = work_path / "shards" / f"{sid}.cert.json"
        if cert_json.is_file() and cert_json.stat().st_size > 0:
            continue
        compiled_json = work_path / "shards" / f"{sid}.json"
        is_mock_compiled = False
        if compiled_json.is_file() and compiled_json.stat().st_size > 0:
            try:
                is_mock_compiled = "templates" in json.loads(compiled_json.read_text(encoding="utf-8"))
            except Exception:
                is_mock_compiled = False
        if not is_mock_compiled:
            pending.append(str(sid))
    return pending


async def _run_post_cta_pipeline(
    work_path: Path,
    work_dir_arg: str,
    python_exe: str,
    run_py: str,
    dispatch_py: str,
    director_id: str,
    cli_env: Optional[Dict[str, str]],
    max_repair_rounds: int,
) -> Dict[str, Any]:
    """Execute Stage 2..6B: shard -> authors -> templates -> build -> judges -> gates -> repair loop.

    Idempotent on resume: if pre_shard_manifest.json already exists and all shards have compiled
    shard_XX.json artifacts (unless force_reshard=True), skips Stage 2 & Stage 3 instead of
    re-spawning a duplicate wave of Shard Authors over already-compiled shards.
    """
    dispatch_dir = work_path / "dispatch"
    force_reshard = bool(_WF_ARGS.get("force_reshard"))
    pending_shards = None if force_reshard else _find_pending_shards(work_path)

    if pending_shards is None:
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

    author_results: Dict[str, Any] = {"skipped_all_compiled": True, "count": 0}
    if pending_shards is None or len(pending_shards) > 0:
        phase("Stage 3: Dispatch & Run Authors")
        author_dispatch_args = ["dispatch-authors", "--work-dir", work_dir_arg]
        if _WF_ARGS.get("templates_per_modality") is not None:
            author_dispatch_args.extend(["--templates-per-modality", str(_WF_ARGS["templates_per_modality"])])
        await run_cli(
            _build_python_cmd(python_exe, dispatch_py, *author_dispatch_args),
            "C2C dispatch authors",
            env_extra=cli_env,
        )
        authors_manifest_path = dispatch_dir / "authors.json"
        if pending_shards is not None and authors_manifest_path.is_file():
            try:
                m_data = json.loads(authors_manifest_path.read_text(encoding="utf-8"))
                pending_set = set(pending_shards)
                if isinstance(m_data.get("Subagents"), list):
                    m_data["Subagents"] = [
                        s for s in m_data["Subagents"]
                        if any(pid in str(s.get("Role", "")) or pid in str(s.get("Prompt", "")) for pid in pending_set)
                    ]
                    m_data["subagents_count"] = len(m_data["Subagents"])
                    authors_manifest_path.write_text(json.dumps(m_data, indent=2, ensure_ascii=False), encoding="utf-8")
            except Exception:
                pass
        author_conc = int(_WF_ARGS.get("author_concurrency") or _WF_ARGS.get("author_wave_size") or 9)
        author_results = await run_wave_from_manifest(
            str(authors_manifest_path),
            "Stage 3: Shard Authors Wave",
            max_concurrency=author_conc,
            max_concurrent_batch=0,
        )
    else:
        phase("Stage 2-3: Skipped (all shards already compiled)")

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

    # Stage 5B: Adaptive Two-Stage LQAS micro-wave if any k=1 template triggered kernel_override=True
    jr_path = work_path / "judge_report.json"
    if _is_fresh_file(jr_path, stage5_start):
        try:
            jr_data = json.loads(jr_path.read_text(encoding="utf-8"))
        except Exception:
            jr_data = {}
        if bool(jr_data.get("lqas_followup_required")) and (jr_data.get("single_seed_override_templates") or []):
            phase("Stage 5B: Adaptive Two-Stage LQAS Confirmation")
            _unlink_if_exists(judges_manifest)
            lqas_start = time.time()
            await run_cli(
                _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "lqas-rejudge", "--work-dir", work_dir_arg),
                "C2C stage lqas-rejudge",
                env_extra=cli_env,
            )
            if _is_fresh_file(judges_manifest, lqas_start):
                await run_wave_from_manifest(
                    str(judges_manifest),
                    "Stage 5B: Adaptive LQAS Confirmation Wave",
                )
                await run_cli(
                    _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "lqas-compare", "--work-dir", work_dir_arg),
                    "C2C stage lqas-compare",
                    env_extra=cli_env,
                )

    phase("Stage 6: Quality Gates")
    _unlink_if_exists(work_path / "repair_matrix.json")
    _unlink_if_exists(dispatch_dir / "repair_matrix.json")
    gates_start = time.time()
    gates_rc, gates_out = await run_cli_status(
        _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "gates", "--work-dir", work_dir_arg),
        "C2C stage gates",
        env_extra=cli_env,
    )

    failing_cids = _collect_failing_competencies(
        work_path,
        matrix_min_mtime=gates_start,
        judge_min_mtime=stage5_start,
    )
    repair_results: List[str] = []
    repair_rounds_executed = 0
    needs_repair = (gates_rc != 0) or bool(failing_cids) or ("dispatch-repair" in (gates_out or ""))

    for round_idx in range(max(0, max_repair_rounds)):
        if not needs_repair:
            break
        phase(f"Stage 6B: Consolidated Shard Repair & Surgical Rejudge (Round {round_idx + 1}/{max_repair_rounds})")
        _unlink_if_exists(work_path / "repair_matrix.json")
        _unlink_if_exists(dispatch_dir / "repair_matrix.json")
        repair_matrix_start = time.time()
        await run_cli(
            _build_run_py_cmd(python_exe, run_py, director_id, "--stage", "repair-matrix", "--work-dir", work_dir_arg),
            "C2C stage repair-matrix",
            env_extra=cli_env,
        )
        round_targets = _collect_failing_competencies(
            work_path,
            matrix_min_mtime=repair_matrix_start,
            judge_min_mtime=stage5_start,
        )
        if not round_targets:
            failing_cids = []
            needs_repair = False
            break
        _unlink_if_exists(work_path / "repair_matrix.json")
        _unlink_if_exists(dispatch_dir / "repair_matrix.json")
        cycle_start = time.time()
        round_repairs, _ = await _execute_repair_and_rejudge_cycle(
            work_path=work_path,
            work_dir_arg=work_dir_arg,
            python_exe=python_exe,
            run_py=run_py,
            dispatch_py=dispatch_py,
            director_id=director_id,
            cli_env=cli_env,
            target_ids=round_targets,
            repair_wave_label=f"Stage 6B: Consolidated Repair Wave (R{round_idx + 1})",
            rejudge_wave_label=f"Stage 6B: Surgical Rejudge Wave (R{round_idx + 1})",
            raise_on_gates_fail=False,
        )
        repair_results.extend(round_repairs)
        repair_rounds_executed += 1
        failing_cids = _collect_failing_competencies(
            work_path,
            matrix_min_mtime=cycle_start,
            judge_min_mtime=cycle_start,
        )
        needs_repair = bool(failing_cids)

    if needs_repair and failing_cids:
        raise RuntimeError(
            f"C2C stage gates still failing after {repair_rounds_executed} repair round(s): {failing_cids}"
        )

    return {
        "authors_completed": len(author_results),
        "judges_completed": len(judge_results),
        "repairs_completed": len(repair_results),
        "repair_rounds_executed": repair_rounds_executed,
        "remaining_failing_ids": failing_cids,
    }


async def run_c2c_workflow() -> Dict[str, Any]:
    """Entry point for C2C wave, cta_pipeline, repair_and_rejudge, post_cta_pipeline, or full_pipeline."""
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

    # Single-wave execution modes: "cta", "cta_harmonize", "authors", "judges", "repair" (or default "wave")
    if mode in MANIFEST_BY_MODE or mode == "wave":
        manifest_file = str(_WF_ARGS.get("manifest") or MANIFEST_BY_MODE.get(mode, "authors.json")).strip()
        manifest_path = dispatch_dir / manifest_file
        phase_label = f"C2C Wave: {mode.upper()}"
        wave_start = time.time()
        wave_conc = (
            int(_WF_ARGS.get("author_concurrency") or _WF_ARGS.get("author_wave_size") or 9)
            if mode == "authors"
            else None
        )
        results = await run_wave_from_manifest(
            str(manifest_path),
            phase_label,
            max_concurrency=wave_conc,
            max_concurrent_batch=0,
        )
        unfinished_cids: List[str] = []
        if mode == "repair":
            unfinished_cids = _collect_unfinished_repair_ids(
                work_path,
                manifest_path,
                results,
                min_ts=wave_start,
            )
            if unfinished_cids:
                log(f"[REPAIR-CLOSE-GUARD] Re-dispatching unfinished repairs in single-wave mode: {unfinished_cids}")
                _unlink_if_exists(manifest_path)
                retry_start = time.time()
                await run_cli(
                    _build_python_cmd(
                        python_exe,
                        dispatch_py,
                        "dispatch-repair",
                        "--work-dir",
                        work_dir_arg,
                        "--ids",
                        *unfinished_cids,
                    ),
                    "C2C dispatch repair (close-guard retry)",
                    env_extra=cli_env,
                )
                if _is_fresh_file(manifest_path, retry_start):
                    results.extend(
                        await run_wave_from_manifest(str(manifest_path), f"{phase_label} (Close-Guard Retry)")
                    )
        summary: Dict[str, Any] = {
            "mode": mode,
            "work_dir": str(work_path),
            "workers_completed": len(results),
        }
        if unfinished_cids:
            summary["retried_repair_ids"] = unfinished_cids
        print(json.dumps(summary, ensure_ascii=False))
        return summary

    if mode == "cta_pipeline":
        cta_info = await _run_cta_pipeline(
            work_path=work_path,
            work_dir_arg=work_dir_arg,
            python_exe=python_exe,
            run_py=run_py,
            director_id=director_id,
            cli_env=cli_env,
        )
        summary = {"mode": mode, "work_dir": str(work_path), **cta_info}
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

    if mode == "post_cta_pipeline":
        eff_rounds = max(1, int(_WF_ARGS.get("max_repair_rounds") or 1))
        post_info = await _run_post_cta_pipeline(
            work_path=work_path,
            work_dir_arg=work_dir_arg,
            python_exe=python_exe,
            run_py=run_py,
            dispatch_py=dispatch_py,
            director_id=director_id,
            cli_env=cli_env,
            max_repair_rounds=eff_rounds,
        )
        summary = {"mode": mode, "work_dir": str(work_path), **post_info}
        print(json.dumps(summary, ensure_ascii=False))
        return summary

    if mode == "full_pipeline":
        eff_rounds = max(1, int(_WF_ARGS.get("max_repair_rounds") or 2))
        cta_info = await _run_cta_pipeline(
            work_path=work_path,
            work_dir_arg=work_dir_arg,
            python_exe=python_exe,
            run_py=run_py,
            director_id=director_id,
            cli_env=cli_env,
        )
        post_info = await _run_post_cta_pipeline(
            work_path=work_path,
            work_dir_arg=work_dir_arg,
            python_exe=python_exe,
            run_py=run_py,
            dispatch_py=dispatch_py,
            director_id=director_id,
            cli_env=cli_env,
            max_repair_rounds=eff_rounds,
        )
        summary = {"mode": mode, "work_dir": str(work_path), **cta_info, **post_info}
        print(json.dumps(summary, ensure_ascii=False))
        return summary

    raise ValueError(
        f"Unsupported mode '{mode}'. Expected one of: 'cta', 'cta_harmonize', 'cta_pipeline', 'authors', 'judges', 'repair', 'repair_and_rejudge', 'post_cta_pipeline', 'full_pipeline'."
    )


if "parallel" in globals():
    await run_c2c_workflow()
