"""C2C Dual-Role Lifecycle Hook Guard (C2C v3.3 Hardened).

Enforces:
1. Fast-path zero interference (< 15 ms) when outside active C2C runs.
2. Director Context Diet: Prevents Director from loading worker *_data.py,
   shard_fixes/*.py, or judge_responses files, while allowing manifests, dispatch items/types, and logs.
3. Worker Subagent Boundaries: Prevents workers from inspecting compiler/validator
   source, tampering with .check_attempts, or executing nested-quote / inspection shell commands.
4. Auditor Exemption: Respects exempt_conversation_ids in lockfile.
5. Exit Code 0 Invariant: Always exits with 0 and emits compliant JSON to stdout.
"""

from __future__ import annotations

from datetime import datetime
import json
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

LOCK_MAX_AGE_SECONDS = 7200  # 2 hours

REPO_ROOT = Path(__file__).resolve().parents[3]
USER_HOME = Path.home()

_LOCK_CACHE: Dict[str, Tuple[float, Dict[str, Any]]] = {}
_DIRECTOR_TRANSCRIPT_CACHE: Dict[str, Tuple[float, bool, str]] = {}

# Director denied targets (read or edit)
DIRECTOR_DENIED_PATTERNS = [
    re.compile(r".*_data\.py$", re.IGNORECASE),
    re.compile(r".*shard_fixes[\\/].*\.py$", re.IGNORECASE),
    re.compile(r".*judge_responses.*\.json$", re.IGNORECASE),
    re.compile(r".*skills[\\/]content-to-course[\\/].*\.py$", re.IGNORECASE),
]

# Worker denied read targets (file tools)
WORKER_DENIED_READ_SUBSTRINGS = [
    "compile_shard.py",
    "check_templates.py",
    "compile_cta.py",
    "check_cta.py",
    "cta_merge.py",
    "/engine/",
    "engine/",
    "/validator/",
    "validator/",
    "src/validator/",
    ".check_attempts",
    "judge_ground_truth.json",
    "skill.md",
    "tests/",
    "tests\\",
]

# Worker denied write/edit targets
WORKER_DENIED_WRITE_SUBSTRINGS = [
    ".check_attempts",
    ".agents/skills/",
    ".agents\\skills\\",
    "skills/content-to-course",
    "skills\\content-to-course",
    "compile_shard.py",
    "check_templates.py",
    "compile_cta.py",
    "check_cta.py",
    "cta_merge.py",
    "/engine/",
    "engine/",
    "/validator/",
    "validator/",
    "src/validator/",
    "judge_ground_truth.json",
]

_WRITE_TOOLS = (
    "write_file",
    "write_to_file",
    "edit_file",
    "replace_file_content",
    "multi_replace_file_content",
    "notebook_edit",
)

WORKER_AUTHORIZED_PYTHON_PATTERNS = [
    re.compile(r"(?:^|/)shards/[a-zA-Z0-9_-]+_data\.py$", re.IGNORECASE),
    re.compile(r"(?:^|/)shard_[a-zA-Z0-9_-]+_data\.py$", re.IGNORECASE),
    re.compile(r"(?:^|/)(?:shards/)?shard_fixes/(?:[a-zA-Z0-9_-]+/)?(?:[^/\\<>:\"|?*]+\.py)$", re.IGNORECASE),
    re.compile(r"(?:^|/)(?:shards/)?build_[a-zA-Z0-9_-]+\.py$", re.IGNORECASE),
    re.compile(r"(?:^|/)(?:cta_parts/)?cta_fixes/[^/\\<>:\"|?*]+\.py$", re.IGNORECASE),
    re.compile(r"(?:^|/)cta_fixes/[^/\\<>:\"|?*]+\.py$", re.IGNORECASE),
    re.compile(r"(?:^|/)(?:cta_parts/|cta/)?part_[a-zA-Z0-9_-]+(?:_data)?\.py$", re.IGNORECASE),
    re.compile(r"(?:^|/)cta_parts/[a-zA-Z0-9_-]+_data\.py$", re.IGNORECASE),
    re.compile(r"(?:^|/)cta_parts/[a-zA-Z0-9_-]+\.py$", re.IGNORECASE),
    re.compile(r"(?:^|/)cta/[a-zA-Z0-9_-]+_data\.py$", re.IGNORECASE),
    re.compile(r"(?:^|/)(?:cta/|cta_parts/)?build_[a-zA-Z0-9_-]+\.py$", re.IGNORECASE),
    re.compile(r"(?:^|/)cta_data\.py$", re.IGNORECASE),
]

SHARD_DATA_PATTERN = re.compile(
    r"(?:^|/)(?:.*/shards/|shards/)?(shard_[a-zA-Z0-9_-]+|[a-zA-Z0-9_-]+)_data\.py$",
    re.IGNORECASE,
)

CTA_DATA_PATTERN = re.compile(
    r"(?:^|/)(?:(?:.*/)?(?:cta_parts|cta)/([a-zA-Z0-9_-]+?)(?:_data)?\.py|(cta_data)\.py)$",
    re.IGNORECASE,
)


def _shard_id_aliases(target_id: str) -> List[str]:
    """Generates candidate shard identifiers (e.g. shard_01, 01) across casing and normalization."""
    raw = str(target_id or "").strip()
    if not raw:
        return []
    variants = [raw, re.sub(r"[^\w-]", "_", raw)]
    raw_lower = raw.lower()
    if raw_lower.startswith("shard_"):
        suffix = raw[6:]
        if suffix:
            variants.extend([suffix, re.sub(r"[^\w-]", "_", suffix)])
    else:
        variants.extend([f"shard_{raw}", f"shard_{re.sub(r'[^\w-]', '_', raw)}"])

    res: List[str] = []
    seen: Set[str] = set()
    for v in variants:
        for item in (v, v.lower()):
            if item and item not in seen:
                seen.add(item)
                res.append(item)
    return res


def _cta_id_aliases(target_id: str) -> List[str]:
    """Generates candidate CTA part identifiers (e.g. part_01, 01) across casing and normalization."""
    raw = str(target_id or "").strip()
    if not raw:
        return []
    variants = [raw, re.sub(r"[^\w-]", "_", raw)]
    raw_lower = raw.lower()
    if raw_lower.startswith("part_"):
        suffix = raw[5:]
        if suffix:
            variants.extend([suffix, re.sub(r"[^\w-]", "_", suffix)])
    else:
        variants.extend([f"part_{raw}", f"part_{re.sub(r'[^\w-]', '_', raw)}"])

    res: List[str] = []
    seen: Set[str] = set()
    for v in variants:
        for item in (v, v.lower()):
            if item and item not in seen:
                seen.add(item)
                res.append(item)
    return res


def _extract_target_file_path(args: Dict[str, Any]) -> Optional[str]:
    """Extracts the primary target file path from write/edit tool arguments."""
    for k in (
        "Path",
        "path",
        "AbsolutePath",
        "absolute_path",
        "TargetFile",
        "target_file",
        "file_path",
        "filePath",
        "file",
    ):
        if k in args and args[k]:
            return _normalize_path(args[k])
    return None


def _is_authorized_worker_python_write(p: str) -> bool:
    """Checks whether a .py file write is within authorized C2C worker boundaries."""
    norm = _normalize_path(p)
    norm_lower = norm.lower()
    if "/scratch/" in f"/{norm_lower}" or norm_lower.startswith("scratch/"):
        return True
    if "/work_append/" in f"/{norm_lower}" or norm_lower.startswith("work_append/"):
        return True
    if "/shard_fixes/" in f"/{norm_lower}" or norm_lower.startswith("shard_fixes/"):
        return True
    if "/cta_fixes/" in f"/{norm_lower}" or norm_lower.startswith("cta_fixes/"):
        return True
    for pat in WORKER_AUTHORIZED_PYTHON_PATTERNS:
        if pat.search(norm):
            return True
    return False

# Shell reader / inspection command tokens (PowerShell, CMD, bash)
SHELL_READ_CMDS_PATTERN = re.compile(
    r"(?<![-/a-zA-Z0-9_])(?:get-content|gc|cat|type|more|head|tail|select-string|sls|grep|findstr|copy-item|copy|cp|move-item|move|mv)(?!\w)",
    re.IGNORECASE,
)

DEL_INDICATORS_PATTERN = re.compile(
    r"\b(?:rm|del|remove-item|rmdir|unlink|erase|truncate)\b",
    re.IGNORECASE,
)

PYTHON_EXEC_PATTERN = re.compile(
    r"""^\s*(?:&|call)?\s*(?:
        ["'](?:.*[/\\])?(?:python(?:\.exe)?|py(?:\.exe)?)["']
        |
        (?:[^\s"']*[/\\])?(?:python(?:\.exe)?|py(?:\.exe)?)
    )(?:\s+-(?!c\b)[A-Za-z]+)*(?!\s+-c\b)\s+""",
    re.IGNORECASE | re.VERBOSE,
)


def _matches_forbidden_target(text_lower: str, forbidden: str) -> bool:
    """Matches forbidden path/command targets using segment boundaries for directory entries."""
    f_norm = forbidden.replace("\\", "/").lower()
    norm_text = text_lower.replace("\\", "/")
    if f_norm.endswith("/"):
        f_clean = f_norm.strip("/")
        return bool(re.search(rf"(?:^|[\s/\"'=]){re.escape(f_clean)}(?:/|[\s\"']|$)", norm_text))
    return f_norm.strip("/") in norm_text


def decidir_estrategia_edicion(
    error_count: Optional[int],
    affected_line_count: Optional[int] = None,
    has_syntax_error: bool = False,
    existing_lines: int = 0,
    target_type: str = "shard",
    affected_competencies_count: int = 0,
    distinct_compiles: int = 0,
) -> str:
    """Certified 2D Matrix for determining file edition strategy.

    Returns:
        'write_file': Allow monolithic write_file rewrite.
        'edit_file': Require surgical edit_file (block monolithic write_file).
        'modular_splicing': Block monolithic write_file and redirect to modular fix.
        'legacy_over_250': Legacy fallback for > line_limit (450 on 1st shard failure, 250 otherwise) when error_count is absent.
    """
    if has_syntax_error or existing_lines < 40:
        return "write_file"

    # Excepción aprobada: subagentes CTA (Stage 1B) cuando los fallos afecten simultáneamente a >= 3 competencias
    if target_type == "cta" and error_count is not None and error_count >= 3 and affected_competencies_count >= 3:
        return "write_file"

    if error_count is not None:
        if error_count <= 0:
            return "write_file"
        eff_affected = affected_line_count if affected_line_count is not None else error_count
        if 1 <= error_count < 6 and eff_affected <= 5:
            return "edit_file"
        if error_count >= 6 or eff_affected > 5:
            return "modular_splicing"

    line_limit = 450 if (target_type == "shard" and distinct_compiles == 1) else 250
    if existing_lines > line_limit:
        return "legacy_over_250"

    return "write_file"


def _is_target_rejected(wd: Path, target_type: str, target_id: str) -> bool:
    """Checks if a shard or CTA is actively marked as REJECTED in failure reports."""
    report_candidates = [
        wd / "specific_error_report.json",
        wd / "publish_rejection_spec.json",
        wd / "template_failures.json",
        wd.parent / "specific_error_report.json",
        wd.parent / "publish_rejection_spec.json",
        wd.parent / "template_failures.json",
    ]
    aliases = _shard_id_aliases(target_id) if target_type == "shard" else _cta_id_aliases(target_id)
    alias_set = {a.lower().strip() for a in aliases}

    for rep_file in report_candidates:
        if not rep_file.is_file():
            continue
        try:
            raw = rep_file.read_text(encoding="utf-8", errors="ignore")
            if not raw.strip():
                continue
            spec = json.loads(raw)
            if not isinstance(spec, dict):
                continue
            st = str(spec.get("status", "")).strip().upper()
            if st in ("REJECTED", "FAIL", "FAILED"):
                if target_type == "shard":
                    failing = {str(x).lower().strip() for x in (spec.get("failing_shards") or [])}
                    affected = {str(x).lower().strip() for x in (spec.get("affected_shards") or [])}
                    combined = failing | affected
                    for a in alias_set:
                        clean_a = a.replace("shard_", "")
                        if a in combined or f"shard_{clean_a}" in combined or clean_a in combined:
                            return True
                else:
                    if spec.get("affected_cta") or spec.get("failing_cta"):
                        return True
                    failing = {str(x).lower().strip() for x in (spec.get("failing_cta_parts") or spec.get("failing_shards") or [])}
                    affected = {str(x).lower().strip() for x in (spec.get("affected_cta_parts") or spec.get("affected_shards") or [])}
                    combined = failing | affected
                    for a in alias_set:
                        clean_a = a.replace("part_", "")
                        if a in combined or f"part_{clean_a}" in combined or clean_a in combined:
                            return True
        except Exception:
            continue
    return False


def find_active_c2c_lock(custom_lock_file: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Finds an active, non-stale .c2c_subagent_lock.json file."""
    now = time.time()
    candidates: List[Path] = []

    if custom_lock_file:
        p = Path(custom_lock_file)
        if p.is_file():
            candidates.append(p)
        elif (REPO_ROOT / custom_lock_file).is_file():
            candidates.append(REPO_ROOT / custom_lock_file)
        else:
            candidates.append(p)
    elif "C2C_LOCK_FILE" in os.environ:
        p = Path(os.environ["C2C_LOCK_FILE"])
        if p.is_file():
            candidates.append(p)
        elif (REPO_ROOT / os.environ["C2C_LOCK_FILE"]).is_file():
            candidates.append(REPO_ROOT / os.environ["C2C_LOCK_FILE"])
        else:
            candidates.append(p)
    else:
        try:
            cwd = Path.cwd()
            candidates.extend(cwd.glob("work*/.c2c_subagent_lock.json"))
            candidates.extend(cwd.glob(".c2c_subagent_lock.json"))
        except Exception:
            pass
        candidates.extend(REPO_ROOT.glob("courses/*/work*/.c2c_subagent_lock.json"))
        candidates.extend(REPO_ROOT.glob("courses/*/.c2c_subagent_lock.json"))
        candidates.extend(REPO_ROOT.glob("work*/.c2c_subagent_lock.json"))
        candidates.extend(REPO_ROOT.glob(".c2c_subagent_lock.json"))

    valid_candidates: List[Tuple[float, Path, Dict[str, Any]]] = []
    for p in candidates:
        try:
            if not p.is_file():
                continue
            st = p.stat()
            mtime = st.st_mtime
            if (now - mtime) > LOCK_MAX_AGE_SECONDS:
                continue
            cache_entry = _LOCK_CACHE.get(str(p))
            if cache_entry and cache_entry[0] == mtime and cache_entry[1].get("_cached_size") == st.st_size:
                data = cache_entry[1]
            else:
                data = json.loads(p.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    data["_cached_size"] = st.st_size
                    _LOCK_CACHE[str(p)] = (mtime, data)
            if isinstance(data, dict) and data.get("active") is True:
                valid_candidates.append((mtime, p, data))
        except Exception:
            continue

    if valid_candidates:
        valid_candidates.sort(key=lambda item: item[0], reverse=True)
        return valid_candidates[0][2]

    return None


def _normalize_path(p: Any) -> str:
    """Normalizes file paths across Windows slashes, URL-encoding, and file URIs."""
    if not p:
        return ""
    s = str(p).strip().strip('"\'')
    if s.lower().startswith("file://localhost/"):
        s = s[17:]
    elif s.lower().startswith("file:///"):
        s = s[8:]
    elif s.lower().startswith("file://"):
        s = s[7:]
    try:
        s = urllib.parse.unquote(s)
    except Exception:
        pass
    s = s.replace("\\", "/")
    while "//" in s:
        s = s.replace("//", "/")
    if re.match(r"^/[a-zA-Z]:", s):
        s = s[1:]
    if s.startswith("./"):
        s = s[2:]
    return s


def _extract_paths_from_args(args: Dict[str, Any]) -> List[str]:
    """Extracts target paths from diverse tool argument representations."""
    paths: List[str] = []
    keys = [
        "AbsolutePath",
        "absolute_path",
        "Path",
        "path",
        "TargetFile",
        "target_file",
        "file_path",
        "filePath",
        "Target",
        "target",
        "file",
        "Uri",
        "uri",
        "Url",
        "url",
        "dir_path",
        "dirPath",
        "directory",
        "folder",
        "Directory",
    ]
    for k in keys:
        if k in args and args[k]:
            val = str(args[k])
            if "\n" in val or "\r" in val or len(val) > 400:
                continue
            paths.append(_normalize_path(val))
    return paths


def _extract_command_from_args(args: Dict[str, Any]) -> str:
    """Extracts raw shell command line from diverse tool argument representations."""
    for k in ("CommandLine", "command_line", "command", "cmd", "CommandLine"):
        if k in args and args[k]:
            s = str(args[k]).strip()
            if len(s) >= 2 and s[0] in ('"', "'") and s[-1] == s[0] and s[0] not in s[1:-1]:
                s = s[1:-1].strip()
            return s
    return ""


def _resolve_work_dir(active_lock: Dict[str, Any]) -> Optional[Path]:
    """Resolves the active C2C work_dir from active_lock or by scanning active lockfiles."""
    wd_raw = active_lock.get("work_dir")
    if wd_raw:
        wd = Path(str(wd_raw))
        return wd if wd.is_absolute() else (REPO_ROOT / wd)

    now = time.time()
    candidates: List[Path] = []
    if "C2C_LOCK_FILE" in os.environ:
        p = Path(os.environ["C2C_LOCK_FILE"])
        candidates.append(p if p.is_absolute() else (REPO_ROOT / p))
    try:
        cwd = Path.cwd()
        candidates.extend(cwd.glob("work*/.c2c_subagent_lock.json"))
        candidates.extend(cwd.glob(".c2c_subagent_lock.json"))
    except Exception:
        pass
    candidates.extend(REPO_ROOT.glob("courses/*/work*/.c2c_subagent_lock.json"))
    candidates.extend(REPO_ROOT.glob("courses/*/.c2c_subagent_lock.json"))
    candidates.extend(REPO_ROOT.glob("work*/.c2c_subagent_lock.json"))
    candidates.extend(REPO_ROOT.glob(".c2c_subagent_lock.json"))

    for p in candidates:
        try:
            if not p.is_file() or (now - p.stat().st_mtime) > LOCK_MAX_AGE_SECONDS:
                continue
            data = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data.get("active") is True:
                return p.parent
        except Exception:
            continue
    return None


def _resolve_output_candidates(path_str: str, work_dir: Path) -> List[Path]:
    """Returns candidate filesystem Paths for a manifest-referenced file."""
    p = Path(path_str)
    if p.is_absolute():
        return [p]
    cands = [REPO_ROOT / p, work_dir / p, work_dir.parent / p]
    norm = path_str.replace("\\", "/")
    if norm.startswith("work/"):
        cands.append(work_dir / norm[5:])
    return cands


def _check_file_exists(
    path_str: str,
    work_dir: Path,
    min_bytes: int = 0,
    min_ts: Optional[float] = None,
) -> bool:
    """Checks whether any candidate path exists on disk, meets min_bytes, and optional freshness min_ts."""
    for cand in _resolve_output_candidates(path_str, work_dir):
        try:
            if cand.is_file():
                st = cand.stat()
                if min_bytes > 0 and st.st_size < min_bytes:
                    continue
                if min_ts is not None and min_ts > 0 and (st.st_mtime + 1.0) < min_ts:
                    continue
                return True
        except OSError:
            continue
    return False


def _read_json_safe(path: Path) -> Optional[Dict[str, Any]]:
    """Reads a JSON object safely, returning None on error."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def _load_item_dicts(manifest: Dict[str, Any], work_dir: Path) -> List[Dict[str, Any]]:
    """Loads JSON dicts for all item_files listed in a dispatch manifest."""
    items: List[Dict[str, Any]] = []
    for raw_item in manifest.get("item_files") or []:
        if not raw_item:
            continue
        for cand in _resolve_output_candidates(str(raw_item), work_dir):
            if cand.is_file():
                data = _read_json_safe(cand)
                if data is not None:
                    items.append(data)
                break
    return items


def _all_cids_have_blocked_transcript(conv_ids: Any) -> bool:
    """Returns True iff every requested ConversationId has 'BLOCKED:' in its transcript."""
    if not isinstance(conv_ids, (list, tuple)) or not conv_ids:
        return False
    for cid in conv_ids:
        cid_str = str(cid).strip()
        if not cid_str:
            return False
        t_path = (
            USER_HOME
            / ".gemini"
            / "antigravity"
            / "brain"
            / cid_str
            / ".system_generated"
            / "logs"
            / "transcript.jsonl"
        )
        try:
            if not t_path.is_file():
                return False
            if "BLOCKED:" not in t_path.read_text(encoding="utf-8", errors="ignore"):
                return False
        except OSError:
            return False
    return True


def _parse_iso_timestamp(ts_str: Any) -> Optional[float]:
    """Parses an ISO-8601 timestamp string into a UTC epoch float, or None."""
    if not ts_str or not isinstance(ts_str, str):
        return None
    raw = ts_str.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(raw).timestamp()
    except Exception:
        return None


def _resolve_existing_candidate(path_str: str, work_dir: Path) -> Optional[Path]:
    """Returns the first existing file Path among manifest-referenced candidates."""
    for cand in _resolve_output_candidates(path_str, work_dir):
        try:
            if cand.is_file():
                return cand
        except OSError:
            continue
    return None


def _file_is_fresh(path: Path, json_data: Optional[Dict[str, Any]], ts_keys: Tuple[str, ...], min_ts: Optional[float]) -> bool:
    """Checks whether a certified artifact was written at or after min_ts (with 1s skew tolerance)."""
    if min_ts is None:
        return True
    threshold = min_ts - 1.0
    if isinstance(json_data, dict):
        for k in ts_keys:
            val = json_data.get(k)
            if isinstance(val, (int, float)) and float(val) >= threshold:
                return True
    try:
        return path.stat().st_mtime >= threshold
    except OSError:
        return False


def _shard_has_circuit_breaker_halt(work_dir: Path, shard_id: str, min_ts: Optional[float] = None) -> bool:
    """Returns True only if a shard explicitly halted at Circuit Breaker (>=3 consecutive identical fails)."""
    att_dirs = (work_dir / ".check_attempts", work_dir / "shards" / ".check_attempts")
    for att_dir in att_dirs:
        for alias in _shard_id_aliases(shard_id):
            for fname in (f"compile_{alias}.json", f"{alias}.json"):
                cand = att_dir / fname
                if not cand.is_file():
                    continue
                data = _read_json_safe(cand)
                if not isinstance(data, dict):
                    continue
                streak = data.get("same_error_streak") or data.get("consecutive_same_error") or 0
                if isinstance(streak, int) and streak >= 3 and _file_is_fresh(cand, data, ("updated_at", "timestamp"), min_ts):
                    return True
    return False


def _verify_shard_certified(
    work_dir: Path,
    shard_id: str,
    receipt_hint: Optional[str] = None,
    min_ts: Optional[float] = None,
    allow_circuit_breaker: bool = False,
) -> List[str]:
    """Verifies a shard has compiled_status PASS, valid .cert.json, and optional freshness."""
    if allow_circuit_breaker and _shard_has_circuit_breaker_halt(work_dir, shard_id, min_ts=min_ts):
        return []

    problems: List[str] = []
    aliases = _shard_id_aliases(shard_id) if shard_id else []

    receipt_path: Optional[Path] = None
    if receipt_hint:
        receipt_path = _resolve_existing_candidate(receipt_hint, work_dir)
    if receipt_path is None:
        for a in aliases:
            cand = work_dir / "shards" / f"{a}.json"
            if cand.is_file():
                receipt_path = cand
                break

    receipt_label = receipt_hint or f"work/shards/{shard_id}.json"
    if receipt_path is None:
        problems.append(receipt_label)
    else:
        r_data = _read_json_safe(receipt_path)
        if not isinstance(r_data, dict) or str(r_data.get("compiled_status", "")).upper() != "PASS":
            problems.append(f"{receipt_label} (compiled_status!=PASS)")
        elif not _file_is_fresh(receipt_path, r_data, ("compiled_at",), min_ts):
            problems.append(f"{receipt_label} (stale pre-repair)")

    cert_path: Optional[Path] = None
    for a in aliases:
        cand = work_dir / "shards" / f"{a}.cert.json"
        if cand.is_file():
            cert_path = cand
            break
    cert_label = f"work/shards/{shard_id}.cert.json"
    if cert_path is None:
        problems.append(cert_label)
    else:
        c_data = _read_json_safe(cert_path)
        if not isinstance(c_data, dict) or c_data.get("passed_50_seeds") is not True:
            problems.append(f"{cert_label} (unverified)")
        elif not _file_is_fresh(cert_path, c_data, ("created_at",), min_ts):
            problems.append(f"{cert_label} (stale pre-repair)")

    return problems


def _verify_cta_output_certified(
    out_str: str,
    work_dir: Path,
    min_ts: Optional[float] = None,
) -> Optional[str]:
    """Verifies CTA output file exists, optional freshness min_ts, and for cta_parts subparts, has a PASS attempt marker."""
    if not _check_file_exists(out_str, work_dir, min_bytes=1):
        return out_str
    if not _check_file_exists(out_str, work_dir, min_bytes=1, min_ts=min_ts):
        return f"{out_str} (stale pre-dispatch)"
    norm = _normalize_path(out_str)
    m = re.search(r"cta_parts/([a-zA-Z0-9_-]+)\.json$", norm, re.IGNORECASE)
    if m:
        part_id = m.group(1)
        attempts_dir = work_dir / "cta_parts" / ".check_attempts"
        for a in _cta_id_aliases(part_id):
            for fname in (f"pass_cta_{a}.json", f"pass_{a}.json"):
                cand = attempts_dir / fname
                if cand.is_file():
                    pdata = _read_json_safe(cand)
                    if (
                        isinstance(pdata, dict)
                        and str(pdata.get("status", "")).upper() == "PASS"
                        and _file_is_fresh(cand, pdata, ("updated_at", "created_at", "timestamp"), min_ts)
                    ):
                        return None
        return f"work/cta_parts/.check_attempts/pass_cta_{part_id}.json"
    return None


def _has_anchored_signal(text: str, signals: Tuple[str, ...]) -> bool:
    """Returns True if any completion/blocked signal appears at the start of a line/message."""
    if not text:
        return False
    pat = r"(?m)^\s*(?:" + "|".join(re.escape(s) for s in signals) + r")"
    return bool(re.search(pat, text))


def _worker_transcript_has_signal(cid: str, signals: Tuple[str, ...]) -> bool:
    """Checks a worker subagent's transcript.jsonl for completion/blocked MODEL signals."""
    t_path = (
        USER_HOME
        / ".gemini"
        / "antigravity"
        / "brain"
        / cid
        / ".system_generated"
        / "logs"
        / "transcript.jsonl"
    )
    if not t_path.is_file():
        return False
    try:
        for line in t_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            step_type = obj.get("type")
            if step_type in ("GENERIC", "USER_INPUT", "SYSTEM_MESSAGE", "TOOL_RESPONSE", "TOOL_RESULT"):
                continue
            if step_type != "PLANNER_RESPONSE" and obj.get("source") != "MODEL":
                continue
            tool_calls = obj.get("tool_calls")
            if isinstance(tool_calls, list) and len(tool_calls) > 0:
                for tc in tool_calls:
                    if not isinstance(tc, dict):
                        continue
                    tname = tc.get("name") or tc.get("tool_name")
                    if tname == "send_message":
                        targs = tc.get("args") if isinstance(tc.get("args"), dict) else tc.get("arguments")
                        if isinstance(targs, dict):
                            msg = str(targs.get("Message") or targs.get("message") or "")
                            if _has_anchored_signal(msg, signals):
                                return True
                continue
            text = str(obj.get("content") or "")
            if _has_anchored_signal(text, signals):
                return True
    except OSError:
        return False
    return False


def _extract_short_worker_label(role: str = "", prompt: str = "", fallback: str = "") -> str:
    """Extracts concise wave unit label (e.g. part_01, shard_02, C-01, batch_01) instead of raw UUID."""
    for text in (role, prompt):
        if not text:
            continue
        m_part = re.search(r"\b(part_\d+|shard_\d+|batch_\d+|judge_\d+)\b", text, re.IGNORECASE)
        if m_part:
            val = m_part.group(1)
            return val.lower() if val.lower().startswith("judge_") else val
        m_judge_space = re.search(r"\bjudge\s+(\d+)\b", text, re.IGNORECASE)
        if m_judge_space:
            return f"judge_{m_judge_space.group(1)}"
        m_comp = re.search(r"\b(Hab-\d+|PRE-\d+|[CH]-\d+)\b", text)
        if m_comp:
            return m_comp.group(1)
    clean_role = str(role or "").strip()
    return clean_role or fallback


def _find_pending_wave_subagents(active_lock: Dict[str, Any]) -> List[str]:
    """Identifies active wave workers lacking DONE:/BLOCKED:, returning concise labels when known."""
    director_id = str(active_lock.get("director_conversation_id") or "").strip()
    if not director_id:
        return []
    t_path = (
        USER_HOME
        / ".gemini"
        / "antigravity"
        / "brain"
        / director_id
        / ".system_generated"
        / "logs"
        / "transcript.jsonl"
    )
    if not t_path.is_file():
        return []

    active_cids: List[str] = []
    cid_labels: Dict[str, str] = {}
    queued_invoke_labels: List[str] = []
    completed_cids: Set[str] = set()
    pending_kill_actions: List[Tuple[str, List[str]]] = []
    signals = ("DONE:", "BLOCKED:", "CIRCUIT BREAKER")

    lock_start_ts = _parse_iso_timestamp(active_lock.get("started_at") or active_lock.get("created_at"))

    try:
        lines = t_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return []

    for line in lines:
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue

        if lock_start_ts is not None:
            step_ts = _parse_iso_timestamp(obj.get("created_at"))
            if step_ts is not None and step_ts < (lock_start_ts - 5.0):
                continue

        src = obj.get("source")
        step_type = obj.get("type")
        content = str(obj.get("content") or "")

        if step_type == "PLANNER_RESPONSE":
            for tc in obj.get("tool_calls") or []:
                if not isinstance(tc, dict):
                    continue
                tname = tc.get("name") or tc.get("tool_name")
                targs = tc.get("args") if isinstance(tc.get("args"), dict) else tc.get("arguments")
                if tname == "invoke_subagent" and isinstance(targs, dict):
                    lbl = _extract_short_worker_label(
                        role=str(targs.get("Role") or targs.get("role") or ""),
                        prompt=str(targs.get("Prompt") or targs.get("prompt") or ""),
                    )
                    queued_invoke_labels.append(lbl)
                elif tname == "manage_subagents" and isinstance(targs, dict):
                    act = str(targs.get("Action") or targs.get("action") or "").strip().lower()
                    if act in ("kill", "kill_all"):
                        raw_cids = (
                            targs.get("ConversationIds")
                            or targs.get("conversationIds")
                            or targs.get("conversation_ids")
                            or []
                        )
                        cids = [str(x).strip() for x in raw_cids if str(x).strip()]
                        pending_kill_actions.append((act, cids))
        elif step_type in ("GENERIC", "TOOL_RESULT", "TOOL_RESPONSE") and str(obj.get("status") or "").upper() == "ERROR":
            lower_c = content.lower()
            if ("invoke_subagent" in lower_c or "subagent" in lower_c) and queued_invoke_labels:
                queued_invoke_labels.pop(0)
            if ("manage_subagents" in lower_c or "kill" in lower_c or "barrera n/n" in lower_c) and pending_kill_actions:
                pending_kill_actions.pop(0)
        elif src == "MODEL" and "Created the following subagent:" in content:
            m = re.search(r'"conversationId"\s*:\s*"([^"]+)"', content)
            if m:
                cid = m.group(1).strip()
                if cid and cid not in active_cids:
                    active_cids.append(cid)
                if cid:
                    lbl = queued_invoke_labels.pop(0) if queued_invoke_labels else ""
                    if lbl:
                        cid_labels[cid] = lbl
        elif src == "MODEL" and "Successfully killed " in content:
            act, k_cids = pending_kill_actions.pop(0) if pending_kill_actions else ("", [])
            if act == "kill_all" or (not act and "Killed roles:" in content):
                active_cids.clear()
                completed_cids.clear()
                cid_labels.clear()
                queued_invoke_labels.clear()
            elif act == "kill" and k_cids:
                k_set = set(k_cids)
                active_cids = [c for c in active_cids if c not in k_set]
                for k in k_set:
                    completed_cids.discard(k)
                    cid_labels.pop(k, None)
        elif src == "SYSTEM" and step_type == "SYSTEM_MESSAGE":
            m = re.search(r"sender=([^\s\]]+)", content)
            if m:
                m_body = re.search(r"\bcontent=(.+)$", content, re.DOTALL)
                msg_body = m_body.group(1) if m_body else content
                if _has_anchored_signal(msg_body, signals):
                    completed_cids.add(m.group(1).strip())

    pending: List[str] = []
    for cid in active_cids:
        if cid in completed_cids:
            continue
        if _worker_transcript_has_signal(cid, signals):
            continue
        pending.append(cid_labels.get(cid) or cid)
    return pending


def _find_pending_director_stage_tasks(active_lock: Dict[str, Any]) -> List[str]:
    """Identifies in-flight background tasks (task-XX) running run.py stages in the Director transcript."""
    director_id = str(active_lock.get("director_conversation_id") or "").strip()
    if not director_id:
        return []
    t_path = (
        USER_HOME
        / ".gemini"
        / "antigravity"
        / "brain"
        / director_id
        / ".system_generated"
        / "logs"
        / "transcript.jsonl"
    )
    if not t_path.is_file():
        return []

    lock_start_ts = _parse_iso_timestamp(active_lock.get("started_at") or active_lock.get("created_at"))
    active_stage_tasks: Dict[str, str] = {}
    try:
        lines = t_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return []

    for line in lines:
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if lock_start_ts is not None:
            step_ts = _parse_iso_timestamp(obj.get("created_at"))
            if step_ts is not None and step_ts < (lock_start_ts - 5.0):
                continue
        content = str(obj.get("content") or "")
        m_start = re.search(
            r"Tool is running as a background task with task id:\s*([^\s\r\n]+/task-\d+).*?Task Description:\s*([^\r\n]+)",
            content,
            re.DOTALL,
        )
        if m_start:
            tid, tdesc = m_start.group(1).strip(), m_start.group(2).strip()
            if re.search(
                r"run\.py\b[^;|&\n]*--stage(?:\s+|=)[\"']?(gates|judge-compare|rejudge-compare|verify|build|templates|repair-matrix)[\"']?",
                tdesc,
                re.IGNORECASE,
            ):
                active_stage_tasks[tid] = tdesc
        for m_done in re.finditer(
            r'Task(?: id)?\s+"([^"]+/task-\d+)"\s+(?:finished|cancelled)',
            content,
        ):
            active_stage_tasks.pop(m_done.group(1).strip(), None)

    return list(active_stage_tasks.keys())


def _verify_wave_outputs_before_kill(active_lock: Dict[str, Any], args: Dict[str, Any]) -> Tuple[bool, str]:
    """Verifies active wave JSON outputs, certificates, and worker DONE signals before kill/kill_all."""
    action_val = str(args.get("Action") or args.get("action") or "").strip().lower()
    conv_ids = args.get("ConversationIds") or args.get("conversationIds") or args.get("conversation_ids")
    if action_val == "kill" and _all_cids_have_blocked_transcript(conv_ids):
        return (True, "")

    pending_cids = _find_pending_wave_subagents(active_lock)
    work_dir = _resolve_work_dir(active_lock)
    if not work_dir:
        if pending_cids:
            return (
                False,
                f"Barrera N/N: aún hay {len(pending_cids)} subagente(s) activos sin DONE:/BLOCKED:: {', '.join(pending_cids[:6])}",
            )
        return (True, "")

    dispatch_dir = work_dir / "dispatch"
    if not dispatch_dir.is_dir():
        if pending_cids:
            return (
                False,
                f"Barrera N/N: aún hay {len(pending_cids)} subagente(s) activos sin DONE:/BLOCKED:: {', '.join(pending_cids[:6])}",
            )
        return (True, "")

    manifest_candidates: List[Path] = []
    for name in ("repair.json", "judges.json", "authors.json", "author.json", "shards.json", "cta_reduce.json", "cta.json"):
        if name == "author.json" and (dispatch_dir / "authors.json").is_file():
            continue
        p = dispatch_dir / name
        if p.is_file():
            manifest_candidates.append(p)
    manifest_candidates.extend(p for p in dispatch_dir.glob("shards_wave_*.json") if p.is_file())

    if not manifest_candidates:
        if pending_cids:
            return (
                False,
                f"Barrera N/N: aún hay {len(pending_cids)} subagente(s) activos sin DONE:/BLOCKED:: {', '.join(pending_cids[:6])}",
            )
        return (True, "")

    latest_manifest = max(manifest_candidates, key=lambda p: p.stat().st_mtime)
    manifest = _read_json_safe(latest_manifest)
    if manifest is None:
        if pending_cids:
            return (
                False,
                f"Barrera N/N: aún hay {len(pending_cids)} subagente(s) activos sin DONE:/BLOCKED:: {', '.join(pending_cids[:6])}",
            )
        return (True, "")

    m_name = latest_manifest.name
    missing: List[str] = []

    if m_name == "cta.json":
        dispatched_ts = _parse_iso_timestamp(manifest.get("dispatched_at"))
        items = _load_item_dicts(manifest, work_dir)
        checked_any = False
        for it in items:
            out = it.get("output_json") or (it.get("work_order") or {}).get("output_json")
            if out:
                checked_any = True
                err = _verify_cta_output_certified(str(out), work_dir, min_ts=dispatched_ts)
                if err:
                    missing.append(err)
        if not checked_any:
            cta_parts = list((work_dir / "cta_parts").glob("*.json")) if (work_dir / "cta_parts").is_dir() else []
            if not (work_dir / "cta.json").is_file() and not cta_parts:
                missing.append("work/cta.json")

    elif m_name == "cta_reduce.json":
        for req_name in ("cta_harmonize.json", "cta.json"):
            if not (work_dir / req_name).is_file():
                missing.append(f"work/{req_name}")

    elif m_name in ("authors.json", "author.json", "shards.json") or m_name.startswith("shards_wave_"):
        dispatched_ts = _parse_iso_timestamp(manifest.get("dispatched_at"))
        items = _load_item_dicts(manifest, work_dir)
        pre_manifest = _read_json_safe(work_dir / "shards" / "pre_shard_manifest.json") or {}
        shard_cids_map: Dict[str, List[str]] = {}
        raw_shards = pre_manifest.get("shards")
        if isinstance(raw_shards, list):
            for entry in raw_shards:
                if isinstance(entry, dict) and entry.get("shard_id"):
                    raw_cids = (
                        entry.get("competency_ids")
                        or entry.get("assigned_competencies")
                        or entry.get("cids")
                        or entry.get("competencies")
                        or []
                    )
                    parsed_cids = [
                        str(c["id"]) if isinstance(c, dict) and c.get("id") else str(c)
                        for c in raw_cids
                        if not isinstance(c, dict) or c.get("id")
                    ]
                    shard_cids_map[str(entry["shard_id"])] = parsed_cids
        elif isinstance(raw_shards, dict):
            for sid, cids in raw_shards.items():
                if isinstance(cids, list):
                    shard_cids_map[str(sid)] = [str(c) for c in cids]

        cb_ok = not pending_cids
        for it in items:
            wo = it.get("work_order") if isinstance(it.get("work_order"), dict) else {}
            sid = str(it.get("shard_id") or wo.get("shard_id") or "").strip()
            out = it.get("output_json") or wo.get("output_json")
            if not sid and out:
                sid = Path(str(out)).stem
            if sid:
                missing.extend(
                    _verify_shard_certified(
                        work_dir,
                        sid,
                        receipt_hint=str(out) if out else None,
                        min_ts=dispatched_ts,
                        allow_circuit_breaker=cb_ok,
                    )
                )
            elif out and not _check_file_exists(str(out), work_dir, min_ts=dispatched_ts):
                missing.append(str(out))

            if sid and cb_ok and _shard_has_circuit_breaker_halt(work_dir, sid, min_ts=dispatched_ts):
                continue

            exp_tpls = it.get("expected_templates") or wo.get("expected_templates")
            if isinstance(exp_tpls, list) and exp_tpls:
                for tpl in exp_tpls:
                    tpl_str = str(tpl)
                    if not tpl_str.endswith(".json") and "/" not in tpl_str and "\\" not in tpl_str:
                        tpl_str = f"work/templates/{tpl_str}.json"
                    if not _check_file_exists(tpl_str, work_dir, min_bytes=1, min_ts=dispatched_ts):
                        missing.append(tpl_str)
            else:
                cids = it.get("assigned_competencies") or wo.get("assigned_competencies") or shard_cids_map.get(sid, [])
                for cid in cids:
                    if not _check_file_exists(f"work/templates/{cid}.json", work_dir, min_bytes=1, min_ts=dispatched_ts):
                        missing.append(f"work/templates/{cid}.json")

        if not items:
            for sid, cids in shard_cids_map.items():
                missing.extend(
                    _verify_shard_certified(
                        work_dir,
                        sid,
                        min_ts=dispatched_ts,
                        allow_circuit_breaker=cb_ok,
                    )
                )
                if cb_ok and _shard_has_circuit_breaker_halt(work_dir, sid, min_ts=dispatched_ts):
                    continue
                for cid in cids:
                    if not _check_file_exists(f"work/templates/{cid}.json", work_dir, min_bytes=1, min_ts=dispatched_ts):
                        missing.append(f"work/templates/{cid}.json")

    elif m_name == "judges.json":
        dispatched_ts = _parse_iso_timestamp(manifest.get("dispatched_at"))
        for it in _load_item_dicts(manifest, work_dir):
            wo = it.get("work_order") if isinstance(it.get("work_order"), dict) else {}
            out = it.get("output_json") or it.get("output_target") or wo.get("output_json") or wo.get("output_target")
            if out:
                out_str = str(out)
                if not _check_file_exists(out_str, work_dir, min_bytes=20):
                    missing.append(out_str)
                elif not _check_file_exists(out_str, work_dir, min_bytes=20, min_ts=dispatched_ts):
                    missing.append(f"{out_str} (stale pre-dispatch)")

    elif m_name == "repair.json":
        dispatched_ts = _parse_iso_timestamp(manifest.get("dispatched_at"))
        checked_shards: Set[str] = set()
        for it in _load_item_dicts(manifest, work_dir):
            wo = it.get("work_order") if isinstance(it.get("work_order"), dict) else {}
            out = it.get("output_json") or wo.get("output_json")
            sid = str(it.get("shard_id") or wo.get("shard_id") or "").strip()
            if not sid and out:
                sid = Path(str(out)).stem
            if sid and sid not in checked_shards:
                checked_shards.add(sid)
                missing.extend(
                    _verify_shard_certified(
                        work_dir,
                        sid,
                        receipt_hint=str(out) if out else None,
                        min_ts=dispatched_ts,
                    )
                )
            elif out and not _check_file_exists(str(out), work_dir, min_ts=dispatched_ts):
                missing.append(str(out))
            exp_tpls = it.get("expected_templates") or wo.get("expected_templates")
            if isinstance(exp_tpls, list):
                for tpl in exp_tpls:
                    tpl_str = str(tpl)
                    if not tpl_str.endswith(".json") and "/" not in tpl_str and "\\" not in tpl_str:
                        tpl_str = f"work/templates/{tpl_str}.json"
                    if not _check_file_exists(tpl_str, work_dir, min_bytes=1, min_ts=dispatched_ts):
                        missing.append(tpl_str)

    if not missing and not pending_cids:
        return (True, "")

    reasons: List[str] = []
    if pending_cids:
        reasons.append(f"{len(pending_cids)} subagente(s) sin DONE:/BLOCKED: [{', '.join(pending_cids[:6])}]")
    if missing:
        dedup_missing = list(dict.fromkeys(missing))
        preview = ", ".join(dedup_missing[:8])
        if len(dedup_missing) > 8:
            preview += f" (+{len(dedup_missing) - 8} más)"
        reasons.append(f"artefactos incompletos/sin certificar: {preview}")

    return (
        False,
        f"Barrera N/N ({m_name}): {'; '.join(reasons)}",
    )


def process_hook(payload: Dict[str, Any], custom_lock_file: Optional[str] = None) -> Dict[str, Any]:
    """Processes a PreToolUse hook payload and returns decision dict conforming to docs/hooks.md."""
    tool_call = payload.get("toolCall") or payload.get("tool_call") or {}
    tool_name = str(
        tool_call.get("name")
        or tool_call.get("tool_name")
        or payload.get("toolName")
        or payload.get("tool_name")
        or ""
    ).strip().lower()

    args = (
        tool_call.get("args")
        or tool_call.get("arguments")
        or tool_call.get("tool_input")
        or tool_call.get("toolInput")
        or payload.get("toolInput")
        or payload.get("args")
        or {}
    )
    if not isinstance(args, dict):
        args = {}

    paths = _extract_paths_from_args(args)
    cmd = _extract_command_from_args(args)
    cmd_tools = ("run_command", "execute_command", "bash", "powershell", "shell", "terminal")

    active_lock = find_active_c2c_lock(custom_lock_file)
    if not active_lock:
        return {"decision": "allow"}

    caller_id = str(payload.get("conversationId") or payload.get("conversation_id") or "").strip()
    if not caller_id:
        return {"decision": "allow"}

    # AUDITOR EXEMPTION: Support exempt_conversation_ids list in lockfile
    exempt_ids = active_lock.get("exempt_conversation_ids") or []
    if isinstance(exempt_ids, (list, tuple, set)):
        exempt_set = {str(x).strip() for x in exempt_ids if str(x).strip()}
        if caller_id and caller_id in exempt_set:
            return {"decision": "allow"}

    director_id = str(active_lock.get("director_conversation_id") or "").strip()

    # INDEPENDENT CONVERSATION EXEMPTION: If caller_id != director_id, check whether
    # the active director's real AGY transcript exists on disk. In a real AGY session,
    # every child subagent spawned by director_id is recorded in director_id's transcript.jsonl.
    # If director_id's transcript.jsonl exists on disk and does NOT contain caller_id,
    # then caller_id is an independent top-level user/auditor session (e.g. /c2c-run-auditor,
    # /learn) and must NOT be blocked by a concurrent C2C run.
    if caller_id and director_id and caller_id != director_id:
        now_ts = time.time()
        cached_trans = _DIRECTOR_TRANSCRIPT_CACHE.get(director_id)
        if cached_trans and (now_ts - cached_trans[0]) < 2.0:
            exists, trans_text = cached_trans[1], cached_trans[2]
        else:
            director_transcript = (
                USER_HOME
                / ".gemini"
                / "antigravity"
                / "brain"
                / director_id
                / ".system_generated"
                / "logs"
                / "transcript.jsonl"
            )
            exists = director_transcript.is_file()
            trans_text = ""
            if exists:
                try:
                    trans_text = director_transcript.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    trans_text = ""
            _DIRECTOR_TRANSCRIPT_CACHE[director_id] = (now_ts, exists, trans_text)

        if exists and caller_id not in trans_text:
            return {"decision": "allow"}

    # CASE A: Caller IS Director
    if director_id and caller_id == director_id:
        if tool_name == "manage_subagents":
            action_val = str(args.get("Action") or args.get("action") or "").strip().lower()
            if action_val in ("kill", "kill_all"):
                ok, reason = _verify_wave_outputs_before_kill(active_lock, args)
                if not ok:
                    return {"decision": "deny", "reason": reason}
        if tool_name in cmd_tools and cmd:
            stage_m = re.search(
                r"run\.py\b[^;|&\n]*--stage(?:\s+|=)[\"']?(cta|cta-reduce|cta-apply|cta-merge|shard|templates|build|verify|publish|repair-matrix|judge-compare|rejudge-compare|gates|certify|unlock)[\"']?",
                cmd,
                re.IGNORECASE,
            )
            dispatch_m = re.search(
                r"dispatch\.py\b[^;|&\n]*\b(dispatch-cta-reduce|dispatch-authors|dispatch-judges)\b",
                cmd,
                re.IGNORECASE,
            )
            if stage_m or dispatch_m:
                pending_cids = _find_pending_wave_subagents(active_lock)
                if pending_cids:
                    op_name = f"run.py --stage {stage_m.group(1)}" if stage_m else f"dispatch.py {dispatch_m.group(1)}"
                    return {
                        "decision": "deny",
                        "reason": (
                            f"Barrera N/N: Prohibido ejecutar {op_name} mientras sigan activos "
                            f"{len(pending_cids)} subagente(s) sin DONE:/BLOCKED:: {', '.join(pending_cids[:6])}"
                        ),
                    }
            repair_dispatch_m = re.search(
                r"dispatch\.py\b[^;|&\n]*\bdispatch-repair\b",
                cmd,
                re.IGNORECASE,
            )
            if repair_dispatch_m or stage_m or dispatch_m:
                pending_tasks = _find_pending_director_stage_tasks(active_lock)
                if pending_tasks:
                    return {
                        "decision": "deny",
                        "reason": (
                            f"Barrera de Consolidación: Prohibido ejecutar '{cmd[:80]}' mientras sigan en ejecución "
                            f"tareas de validación/gates en segundo plano ({', '.join(pending_tasks)}). "
                            "Espera a que gates y repair-matrix terminen para consolidar todos los hallazgos en 1 sola ola."
                        ),
                    }
        file_tools = (
            "read_file",
            "view_file",
            "write_file",
            "write_to_file",
            "edit_file",
            "replace_file_content",
            "multi_replace_file_content",
        )
        if tool_name in file_tools:
            for p in paths:
                for pattern in DIRECTOR_DENIED_PATTERNS:
                    if pattern.search(p):
                        return {
                            "decision": "deny",
                            "reason": (
                                "C2C v3.3 Director Diet: Do not read or edit worker *_data.py, "
                                "judge_responses, or internal C2C .py scripts directly. "
                                "Delegate repairs via: python .agents/skills/content-to-course/dispatch.py dispatch-repair --work-dir <work_dir> --ids <CID>"
                            ),
                        }
        return {"decision": "allow"}

    # CASE B: Caller IS C2C Worker Subagent
    read_tools = ("read_file", "view_file", "read_resource", "grep_search", "find_by_name", "file_search")
    write_tools = _WRITE_TOOLS

    # Synchronous Budget Governance SLA Limits
    max_turns = active_lock.get("max_turns", 40)
    max_tokens = active_lock.get("max_tokens", 5_000_000)
    max_streak = active_lock.get("max_error_streak", 3)

    turn_count = active_lock.get("turn_count", 0)
    est_tokens = active_lock.get("est_tokens", 0)
    error_streak = active_lock.get("error_sha256_streak", 0)

    if isinstance(turn_count, int) and turn_count > max_turns:
        return {
            "decision": "deny",
            "reason": f"HARD_ABORT: Turn count limit exceeded ({turn_count} > {max_turns}). STOP, report to orchestrator.",
        }
    if isinstance(est_tokens, int) and est_tokens > max_tokens:
        return {
            "decision": "deny",
            "reason": f"HARD_ABORT: Token burn limit exceeded ({est_tokens:,} > {max_tokens:,}). STOP, report to orchestrator.",
        }
    if isinstance(error_streak, int) and error_streak >= max_streak:
        return {
            "decision": "deny",
            "reason": f"HARD_ABORT: Consecutive identical error streak limit reached ({error_streak} >= {max_streak}). STOP, report to orchestrator.",
        }

    # REPAIR Worker Barrier: Block full cta.json and manifest inspection [REPAIR-NO-FULL-CTA]
    lock_role = str(active_lock.get("role") or active_lock.get("subagent_role") or "").strip().lower()
    if lock_role == "repair" and tool_name in ("read_file", "view_file", "read_resource"):
        for p in paths:
            norm_p = p.lower()
            if norm_p.endswith("pre_shard_manifest.json") or norm_p.endswith("pre_cta_manifest.json"):
                return {
                    "decision": "deny",
                    "reason": (
                        "BLOCKER:: [REPAIR-NO-FULL-CTA] Repair subagents are forbidden from reading full manifests. "
                        "Use the provided competence slice or modular fix specification."
                    ),
                }
            if norm_p.endswith("cta.json"):
                cand_p = Path(norm_p)
                sz = 0
                check_list = [cand_p]
                if not cand_p.is_absolute():
                    check_list.extend([REPO_ROOT / cand_p, Path.cwd() / cand_p])
                for cp in check_list:
                    if cp.is_file():
                        try:
                            sz = cp.stat().st_size
                            break
                        except Exception:
                            pass
                if sz > 20_000:
                    return {
                        "decision": "deny",
                        "reason": (
                            "BLOCKER:: [REPAIR-NO-FULL-CTA] Repair subagents are forbidden from reading full cta.json (> 20 KB). "
                            "Use the provided competence slice."
                        ),
                    }

    # 0. Cross-Course Isolation Guard: prevent workers from reading/copying from sibling courses/<other_id>/
    active_course_id = str(active_lock.get("course_id") or "").strip().lower()
    if active_course_id:
        course_ref_pattern = re.compile(
            r"(?:^|[/\\'\"\s])courses[/\\]+([a-zA-Z0-9_-]+)",
            re.IGNORECASE,
        )
        if tool_name in read_tools or tool_name in write_tools:
            for p in paths:
                for m in course_ref_pattern.finditer(p):
                    ref_cid = m.group(1).strip().lower()
                    if ref_cid and ref_cid.endswith(".json"):
                        ref_cid = ref_cid[:-5]
                    if ref_cid and ref_cid != active_course_id:
                        return {
                            "decision": "deny",
                            "reason": (
                                f"C2C Cross-Course Isolation: Workers may only access files within the active course "
                                f"directory (courses/{active_course_id}/). Access to courses/{m.group(1)}/ is strictly forbidden."
                            ),
                        }
        if tool_name in cmd_tools and cmd:
            cmd_norm_slashes = cmd.replace("\\", "/")
            for m in course_ref_pattern.finditer(cmd_norm_slashes):
                ref_cid = m.group(1).strip().lower()
                if ref_cid and ref_cid.endswith(".json"):
                    ref_cid = ref_cid[:-5]
                if ref_cid and ref_cid != active_course_id:
                    return {
                        "decision": "deny",
                        "reason": (
                            f"C2C Cross-Course Isolation: Workers may only access or copy files within the active course "
                            f"directory (courses/{active_course_id}/). Referencing courses/{m.group(1)} is strictly forbidden."
                        ),
                    }
            list_match = re.search(
                r"\b(?:get-childitem|gci|dir|ls|find|tree)\b([^;|&\n]*\bcourses(?:[/\\]|\b)[^;|&\n]*)",
                cmd_norm_slashes,
                re.IGNORECASE,
            )
            if list_match:
                listing_args = list_match.group(1).lower()
                courses_refs = list(re.finditer(r"\bcourses([/\\'\"\s]|$)", listing_args))
                is_general_or_sibling = False
                for cr in courses_refs:
                    tail = listing_args[cr.start():]
                    if not re.match(rf"\bcourses[/\\]+{re.escape(active_course_id)}(?:[/\\]|\b|$)", tail):
                        is_general_or_sibling = True
                        break
                if is_general_or_sibling or not courses_refs:
                    return {
                        "decision": "deny",
                        "reason": (
                            f"C2C Cross-Course Isolation: Listing sibling courses in 'courses/' is forbidden. "
                            f"Operate strictly within courses/{active_course_id}/."
                        ),
                    }

    # 1. Deny reading forbidden internal compiler / validator / ground truth targets
    if tool_name in read_tools:
        for p in paths:
            p_lower = p.lower().replace("\\", "/")
            for forbidden in WORKER_DENIED_READ_SUBSTRINGS:
                f_norm = forbidden.replace("\\", "/").lower()
                if f_norm.endswith("/"):
                    f_clean = f_norm.strip("/")
                    matched = bool(re.search(rf"(?:^|/){re.escape(f_clean)}(?:/|$)", p_lower))
                else:
                    matched = f_norm.strip("/") in p_lower
                if matched:
                    return {
                        "decision": "deny",
                        "reason": f"C2C Worker Boundary: Access denied to internal compiler/validator source or ground truth: {p}.",
                    }

    # 2. Deny writing / modifying skills, compiler source, or check attempts
    if tool_name in write_tools:
        for p in paths:
            p_lower = p.lower()
            for forbidden in WORKER_DENIED_WRITE_SUBSTRINGS:
                if _matches_forbidden_target(p_lower, forbidden):
                    return {
                        "decision": "deny",
                        "reason": f"C2C Worker Boundary: Modification denied to protected internal skills/scripts or check attempts: {p}.",
                    }

        # Stream 1D: Worker Write Isolation, Early Post-PASS Cut, & Anti-Monolithic Rewrite Guards
        target_file = _extract_target_file_path(args) or (paths[0] if paths else "")
        if target_file:
            norm_target = _normalize_path(target_file)

            # Rule A: Worker Python write path isolation (blocking ad-hoc debug scripts)
            if norm_target.lower().endswith(".py"):
                if not _is_authorized_worker_python_write(norm_target):
                    return {
                        "decision": "deny",
                        "reason": (
                            "BLOCKER:: Prohibido crear o editar scripts Python arbitrarios fuera de tu shard asignado "
                            "(ej. scripts de debug sueltos). Escribe únicamente en work/shards/<shard_id>_data.py, "
                            "work/shards/shard_fixes/<CID>.py o work/cta_fixes/<CID>.py."
                        ),
                    }

            # Shard and CTA data files guards
            # Ensure shard_fixes and cta_fixes are NEVER considered data files
            is_fix_file = (
                "/shard_fixes/" in f"/{norm_target.lower()}"
                or norm_target.lower().startswith("shard_fixes/")
                or "/cta_fixes/" in f"/{norm_target.lower()}"
                or norm_target.lower().startswith("cta_fixes/")
            )
            if not is_fix_file:
                cta_match = CTA_DATA_PATTERN.search(norm_target)
                shard_match = SHARD_DATA_PATTERN.search(norm_target) if not cta_match else None
                if cta_match or shard_match:
                    target_type = "cta" if cta_match else "shard"
                    target_id = (
                        (cta_match.group(1) or cta_match.group(2))
                        if cta_match
                        else shard_match.group(1)
                    )
                    norm_target_id = re.sub(r"[^\w-]", "_", target_id)

                    candidate_dirs: List[Path] = []
                    if active_lock.get("work_dir"):
                        try:
                            lock_wd = Path(str(active_lock["work_dir"]))
                            candidate_dirs.append(lock_wd)
                            if not lock_wd.is_absolute():
                                candidate_dirs.append(REPO_ROOT / lock_wd)
                                candidate_dirs.append(Path.cwd() / lock_wd)
                        except Exception:
                            pass

                    try:
                        p_target = Path(norm_target)
                        p_parent_2 = p_target.parent.parent
                        candidate_dirs.append(p_parent_2)
                        candidate_dirs.append(p_target.parent)
                        if not p_parent_2.is_absolute():
                            candidate_dirs.append(REPO_ROOT / p_parent_2)
                            candidate_dirs.append(Path.cwd() / p_parent_2)
                        if not p_target.parent.is_absolute():
                            candidate_dirs.append(REPO_ROOT / p_target.parent)
                            candidate_dirs.append(Path.cwd() / p_target.parent)
                    except Exception:
                        pass

                    seen_keys: Set[str] = set()
                    deduped_candidate_dirs: List[Path] = []
                    for cd in candidate_dirs:
                        k = str(cd).replace("\\", "/").lower()
                        if k not in seen_keys:
                            seen_keys.add(k)
                            deduped_candidate_dirs.append(cd)

                    # Rule B: Early cut guard post-PASS (.check_attempts/pass_<target_id>.json)
                    if target_type == "shard":
                        for wd in deduped_candidate_dirs:
                            for s_id in _shard_id_aliases(target_id):
                                try:
                                    pass_file = wd / ".check_attempts" / f"pass_{s_id}.json"
                                    if pass_file.is_file():
                                        p_raw = pass_file.read_text(encoding="utf-8", errors="ignore")
                                        if p_raw.strip():
                                            p_data = json.loads(p_raw)
                                            if isinstance(p_data, dict):
                                                st = str(p_data.get("status", "")).strip().upper()
                                                if st == "PASS":
                                                    # Exemption: Do not deny edits when the shard is actively marked REJECTED/under repair
                                                    if _is_target_rejected(wd, "shard", target_id):
                                                        continue

                                                    return {
                                                        "decision": "deny",
                                                        "reason": (
                                                            f"BLOCKER:: El shard {target_id} ya aprobó todas las validaciones estrictas ([+] PASS). "
                                                            "Detén llamadas a herramientas de edición y emite DONE inmediatamente."
                                                        ),
                                                    }
                                except Exception:
                                    continue
                    elif target_type == "cta":
                        for wd in deduped_candidate_dirs:
                            for c_id in _cta_id_aliases(target_id):
                                for fname in (f"pass_cta_{c_id}.json", f"pass_{c_id}.json", "pass_cta.json"):
                                    try:
                                        pass_file = wd / ".check_attempts" / fname
                                        if pass_file.is_file():
                                            p_raw = pass_file.read_text(encoding="utf-8", errors="ignore")
                                            if p_raw.strip():
                                                p_data = json.loads(p_raw)
                                                if isinstance(p_data, dict):
                                                    st = str(p_data.get("status", "")).strip().upper()
                                                    if st == "PASS":
                                                        # Exemption: Do not deny edits when CTA is actively marked REJECTED/under repair
                                                        if _is_target_rejected(wd, "cta", target_id):
                                                            continue

                                                        return {
                                                            "decision": "deny",
                                                            "reason": (
                                                                f"BLOCKER:: El módulo CTA {target_id} ya aprobó todas las validaciones estrictas ([+] PASS). "
                                                                "Detén cualquier edición o reescritura adicional y emite DONE inmediatamente."
                                                            ),
                                                        }
                                    except Exception:
                                        continue

                    # Rule C: Anti-monolithic rewrite guard after compile failure (write_file vs edit_file)
                    full_write_tools = ("write_file", "write_to_file")
                    edit_tools = ("edit_file", "replace_file_content", "multi_replace_file_content")
                    if tool_name in full_write_tools or tool_name in edit_tools:
                        target_file_on_disk: Optional[Path] = None
                        p_norm = Path(norm_target)
                        check_paths = [p_norm]
                        if not p_norm.is_absolute():
                            check_paths.extend([REPO_ROOT / p_norm, Path.cwd() / p_norm])

                        for cand_f in check_paths:
                            try:
                                if cand_f.is_file():
                                    target_file_on_disk = cand_f
                                    break
                            except Exception:
                                continue

                        if not target_file_on_disk:
                            for wd in deduped_candidate_dirs:
                                if target_type == "shard":
                                    for s_id in _shard_id_aliases(target_id):
                                        try:
                                            cand_f = wd / "shards" / f"{s_id}_data.py"
                                            if cand_f.is_file():
                                                target_file_on_disk = cand_f
                                                break
                                        except Exception:
                                            continue
                                    if target_file_on_disk:
                                        break
                                elif target_type == "cta":
                                    cand_candidates = [
                                        wd / "cta_data.py",
                                    ]
                                    for c_id in _cta_id_aliases(target_id):
                                        cand_candidates.extend([
                                            wd / "cta" / f"{c_id}.py",
                                            wd / "cta" / f"{c_id}_data.py",
                                            wd / "cta_parts" / f"{c_id}.py",
                                            wd / "cta_parts" / f"{c_id}_data.py",
                                        ])
                                    for cand_f in cand_candidates:
                                        try:
                                            if cand_f.is_file():
                                                target_file_on_disk = cand_f
                                                break
                                        except Exception:
                                            continue
                                    if target_file_on_disk:
                                        break

                        if target_file_on_disk:
                            compile_file_on_disk: Optional[Path] = None
                            for wd in deduped_candidate_dirs:
                                if target_type == "shard":
                                    for s_id in _shard_id_aliases(target_id):
                                        try:
                                            cf = wd / ".check_attempts" / f"compile_{s_id}.json"
                                            if cf.is_file():
                                                compile_file_on_disk = cf
                                                break
                                        except Exception:
                                            continue
                                    if compile_file_on_disk:
                                        break
                                elif target_type == "cta":
                                    for c_id in _cta_id_aliases(target_id):
                                        for fname in (f"compile_cta_{c_id}.json", f"compile_{c_id}.json", "compile_cta.json"):
                                            try:
                                                cf = wd / ".check_attempts" / fname
                                                if cf.is_file():
                                                    compile_file_on_disk = cf
                                                    break
                                            except Exception:
                                                continue
                                        if compile_file_on_disk:
                                            break
                                    if compile_file_on_disk:
                                        break

                            if compile_file_on_disk:
                                try:
                                    c_raw = compile_file_on_disk.read_text(encoding="utf-8", errors="ignore")
                                    c_data = json.loads(c_raw) if c_raw.strip() else {}
                                except Exception:
                                    c_data = {}

                                has_compile_attempt = (
                                    isinstance(c_data, dict)
                                    and (
                                        c_data.get("distinct_compiles", 0) >= 1
                                        or bool(c_data.get("last_err_hash"))
                                        or c_data.get("total_compiles", 0) >= 1
                                        or c_data.get("attempts", 0) >= 1
                                        or bool(c_data.get("last_errors"))
                                        or c_data.get("error_count") is not None
                                    )
                                )

                                if has_compile_attempt:
                                    has_syntax_error = bool(c_data.get("has_syntax_error", False))
                                    if has_syntax_error and tool_name in full_write_tools:
                                        return {"decision": "allow"}

                                    try:
                                        existing_lines = len(
                                            target_file_on_disk.read_text(encoding="utf-8", errors="ignore").splitlines()
                                        )
                                    except Exception:
                                        existing_lines = 0

                                    new_content = args.get("CodeContent") or args.get("Content") or args.get("content") or ""
                                    if isinstance(new_content, list):
                                        new_lines = len(new_content)
                                    else:
                                        new_lines = len(str(new_content).splitlines())

                                    error_count = c_data.get("error_count")
                                    affected_lines = c_data.get("affected_line_count")
                                    streak = c_data.get("same_error_streak", 0)

                                    affected_cids = set()
                                    for err_msg in c_data.get("last_errors", []):
                                        for m in re.finditer(r"\b(?:H|C|Hab|Fact|Concept|Skill)-?\d+\b", str(err_msg), re.IGNORECASE):
                                            affected_cids.add(m.group(0).upper())
                                    aff_comp_cnt = max(len(affected_cids), int(c_data.get("affected_competencies_count", 0) or 0))

                                    distinct_compiles = int(c_data.get("distinct_compiles", 0) or 0)
                                    line_limit = 450 if (target_type == "shard" and distinct_compiles == 1) else 250

                                    strategy = decidir_estrategia_edicion(
                                        error_count=error_count,
                                        affected_line_count=affected_lines,
                                        has_syntax_error=has_syntax_error,
                                        existing_lines=existing_lines,
                                        target_type=target_type,
                                        affected_competencies_count=aff_comp_cnt,
                                        distinct_compiles=distinct_compiles,
                                    )

                                    extra_250 = f" y supera las {line_limit} líneas" if (existing_lines > line_limit or new_lines > line_limit) else ""
                                    target_desc = f"{target_id}_data.py" if target_type == "shard" else target_file_on_disk.name
                                    fix_target = "work/shards/shard_fixes/<CID>.py" if target_type == "shard" else "work/cta_fixes/<CID>.py"

                                    if tool_name in full_write_tools:
                                        # Excepción aprobada: subagentes CTA (Stage 1B) cuando los fallos afecten simultáneamente a >= 3 competencias
                                        if target_type == "cta" and error_count is not None and error_count >= 3 and aff_comp_cnt >= 3:
                                            return {"decision": "allow"}

                                        if strategy == "write_file":
                                            return {"decision": "allow"}

                                        if strategy == "legacy_over_250":
                                            return {
                                                "decision": "deny",
                                                "reason": (
                                                    f"BLOCKER:: El archivo {target_file_on_disk.name} ya fue compilado y supera las {line_limit} líneas. "
                                                    "Para corregir errores de validación usa edit_file quirúrgico sobre las líneas indicadas "
                                                    f"por el compilador o escribe un override modular en {fix_target} "
                                                    "en lugar de reescribir todo el archivo con write_file."
                                                ),
                                            }
                                        elif strategy == "edit_file":
                                            return {
                                                "decision": "deny",
                                                "reason": (
                                                    f"BLOCKER:: El archivo {target_file_on_disk.name} ya fue compilado ({existing_lines} líneas){extra_250} "
                                                    f"y registra {error_count or 1} errores (< 6, umbral oficial). "
                                                    "Para menos de 6 errores está prohibido reescribir todo el archivo desde cero con write_file: "
                                                    "usa edit_file quirúrgico (replace_file_content) sobre las líneas reportadas "
                                                    "(ej. para actualizar tuplas en TEMPLATES al nuevo contrato Form-C / Form-B Tri-Banda: --min-archetypes 4, bandas easy/medium/hard, "
                                                    ">= 2 Bloom, FIB/MS obligatorio y 3-tuplas (did, val, error_rationale_@var@) como en [M3-ARCHETYPES]), "
                                                    f"o escribe un parche modular aislado en {fix_target}."
                                                ),
                                            }
                                        elif strategy == "modular_splicing":
                                            # Shard Authors (Stage 3) pueden reescribir en los primeros 2 fallos;
                                            # ModularSplicing se impone solo a Repair Engineers o desde el 3er fallo.
                                            _role = str(active_lock.get("role") or active_lock.get("subagent_role") or "").strip().lower()
                                            _compiles = int(c_data.get("total_compiles") or c_data.get("distinct_compiles") or 0)
                                            if target_type == "shard" and _role != "repair" and _compiles < 3 and streak < 3:
                                                return {"decision": "allow"}
                                            if target_type == "cta" and aff_comp_cnt >= 3:
                                                return {"decision": "allow"}
                                            return {
                                                "decision": "deny",
                                                "reason": (
                                                    f"BLOCKER:: El archivo {target_file_on_disk.name} registra {error_count or 6} errores (o líneas afectadas > 5) sin SyntaxError. "
                                                    f"Está prohibido reescribir todo el archivo con write_file monolítico. "
                                                    f"Aplica ModularSplicing creando o editando un parche modular aislado en {fix_target}."
                                                ),
                                            }
                                    elif tool_name in edit_tools:
                                        if strategy == "modular_splicing" and streak >= 2:
                                            return {
                                                "decision": "deny",
                                                "reason": (
                                                    f"BLOCKER:: Se detectó un bucle repetitivo de edit_file in-place ({streak} intentos fallidos) sobre {target_file_on_disk.name}. "
                                                    f"Redirige inmediatamente a ModularSplicing en {fix_target}."
                                                ),
                                            }

    # 3. Deny circumventing via shell commands
    if tool_name in cmd_tools:
        cmd_lower = cmd.lower()

        # Deny git exploration commands
        if re.search(r"\bgit\s+(?:log|diff|show|status|branch|grep)\b", cmd, re.IGNORECASE):
            return {
                "decision": "deny",
                "reason": (
                    "C2C Worker Boundary: Git exploration commands (git log/diff/show/status/branch/grep) "
                    "are strictly forbidden for workers. Focus on your assigned shard/task."
                ),
            }

        # Deny ANY command accessing ground truth verification files
        if "judge_ground_truth.json" in cmd_lower:
            return {
                "decision": "deny",
                "reason": "C2C Worker Boundary: Access to ground truth verification files is strictly forbidden.",
            }

        # Deny deleting or truncating .check_attempts
        if ".check_attempts" in cmd_lower:
            if DEL_INDICATORS_PATTERN.search(cmd_lower) or ">" in cmd_lower:
                return {
                    "decision": "deny",
                    "reason": "C2C Worker Boundary: Modification or deletion of .check_attempts is strictly forbidden.",
                }

        # Check if command is attempting to run python on a script vs python -c
        is_python_script_exec = bool(PYTHON_EXEC_PATTERN.match(cmd.strip()))

        # Deny shell read/inspection commands on protected targets (Get-Content, type, cat, gc, etc.)
        if not is_python_script_exec and SHELL_READ_CMDS_PATTERN.search(cmd_lower):
            for forbidden in WORKER_DENIED_READ_SUBSTRINGS:
                if _matches_forbidden_target(cmd_lower, forbidden):
                    if forbidden.replace("\\", "/").lower().strip("/") == "tests":
                        return {
                            "decision": "deny",
                            "reason": "C2C Worker Boundary: Inspection of tests source or test files via shell commands is strictly forbidden.",
                        }
                    return {
                        "decision": "deny",
                        "reason": f"C2C Worker Boundary: Inspection of protected source code or check attempts via shell commands is strictly forbidden: {forbidden}.",
                    }

        # Deny .NET file read in PowerShell
        if "[system.io.file]" in cmd_lower:
            for forbidden in WORKER_DENIED_READ_SUBSTRINGS:
                if _matches_forbidden_target(cmd_lower, forbidden):
                    return {
                        "decision": "deny",
                        "reason": f"C2C Worker Boundary: Inspection of protected files via PowerShell .NET APIs is strictly forbidden: {forbidden}.",
                    }

        # Deny python -c bypasses (including flags like python -u -c / python -B -c)
        if re.search(r"(?:python(?:\.exe)?|py(?:\.exe)?)[/\"'\\]*(?:\s+-[A-Za-z]+)*\s+-c\b", cmd, re.IGNORECASE):
            # Check if python -c targets forbidden files
            for forbidden in WORKER_DENIED_READ_SUBSTRINGS:
                if _matches_forbidden_target(cmd_lower, forbidden):
                    if forbidden.replace("\\", "/").lower().strip("/") == "tests":
                        return {
                            "decision": "deny",
                            "reason": "C2C Worker Boundary: Subagents are forbidden from inspecting internal files via python -c: tests.",
                        }
                    return {
                        "decision": "deny",
                        "reason": f"C2C Worker Boundary: Subagents are forbidden from inspecting internal files via python -c: {forbidden}.",
                    }

            has_escaped_quotes = r'\"' in cmd or r"\'" in cmd
            if has_escaped_quotes or len(cmd) > 120:
                return {
                    "decision": "deny",
                    "reason": (
                        "C2C Worker Boundary: Complex nested-quote or overly long python -c commands "
                        "(> 120 characters or escaped quotes) are forbidden. "
                        "Write a standalone script or use official compiler CLI instead."
                    ),
                }

    return {"decision": "allow"}


# Public alias for evaluation conforming to benchmark specifications
evaluate_hook_payload = process_hook


def main() -> None:
    # Fail-open safety default with exit code 0 invariant & pure 7-bit ASCII JSON stdout
    # (prevents Windows CP1252 pipe byte corruption in Antigravity protojson unmarshaler).
    try:
        try:
            sys.stdin.reconfigure(encoding="utf-8", errors="replace")
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"decision": "allow"}, ensure_ascii=True))
            sys.exit(0)
        payload = json.loads(raw_input)
        if not isinstance(payload, dict):
            print(json.dumps({"decision": "allow"}, ensure_ascii=True))
            sys.exit(0)

        result = process_hook(payload)
        print(json.dumps(result, ensure_ascii=True))
    except SystemExit:
        raise
    except BaseException:
        try:
            print(json.dumps({"decision": "allow"}, ensure_ascii=True))
        except BaseException:
            pass
    sys.exit(0)


if __name__ == "__main__":
    main()
