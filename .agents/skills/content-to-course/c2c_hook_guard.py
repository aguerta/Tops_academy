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
    re.compile(r"(?:^|/)(?:shards/)?shard_fixes/[^/\\<>:\"|?*]+\.py$", re.IGNORECASE),
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
    )\s+(?!-c\b)""",
    re.IGNORECASE | re.VERBOSE,
)


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

    for p in candidates:
        try:
            if not p.is_file():
                continue
            mtime = p.stat().st_mtime
            if (now - mtime) > LOCK_MAX_AGE_SECONDS:
                continue
            cache_entry = _LOCK_CACHE.get(str(p))
            if cache_entry and cache_entry[0] == mtime:
                data = cache_entry[1]
            else:
                data = json.loads(p.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    _LOCK_CACHE[str(p)] = (mtime, data)
            if isinstance(data, dict) and data.get("active") is True:
                return data
        except Exception:
            continue

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
            if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
                s = s[1:-1].strip()
            return s
    return ""


def _check_fast_start_command_guard(cmd: str) -> Optional[Dict[str, str]]:
    """Blocks pre-bootstrap exploration commands (run.py --help, python -c inspecting C2C scripts or counting PDF pages)."""
    if not cmd:
        return None
    cmd_norm = cmd.lower().replace("\\", "/")

    # 1. Block --help / -h on C2C runner/dispatcher scripts
    if re.search(r"content-to-course/(?:run|dispatch|prepare|ingest)\.py\s+(?:--help|-h)\b", cmd_norm):
        return {
            "decision": "deny",
            "reason": (
                "C2C Fast-Start Guard: Do NOT run --help on C2C scripts! Execute Fast Bootstrap immediately in Turn 1: "
                '& ".venv\\Scripts\\python.exe" .agents/skills/content-to-course/run.py --stage bootstrap '
                "--course-id <id> --sources <path> --cta-mode <direct|mapreduce> "
                "--granularity <standard|fine|coarse> --director-id <CONVERSATION_ID>"
            ),
        }

    # 2. Block python -c inspecting content-to-course/*.py or counting PDF pages manually
    if re.search(r"(?:python(?:\.exe)?|py(?:\.exe)?)[/\"'\\]*\s+-c\b", cmd_norm):
        if "content-to-course/" in cmd_norm and any(
            tok in cmd_norm
            for tok in ("open(", "read_text", "run.py", "prepare.py", "ingest.py", "dispatch.py")
        ):
            return {
                "decision": "deny",
                "reason": (
                    "C2C Fast-Start Guard: Do NOT inspect content-to-course/*.py with python -c! "
                    "Execute Fast Bootstrap immediately: "
                    '& ".venv\\Scripts\\python.exe" .agents/skills/content-to-course/run.py --stage bootstrap '
                    "--course-id <id> --sources <path> --cta-mode <direct|mapreduce> "
                    "--granularity <standard|fine|coarse> --director-id <CONVERSATION_ID>"
                ),
            }
        if ("import pypdf" in cmd_norm or "import fitz" in cmd_norm) and "content/" in cmd_norm:
            return {
                "decision": "deny",
                "reason": (
                    "C2C Fast-Start Guard: Do NOT count PDF pages manually with pypdf/fitz! "
                    "run.py --stage bootstrap automatically discovers all PDFs and counts pages in <0.2s."
                ),
            }

    return None


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

    # Pre-Bootstrap Fast-Start Guard: applies even before .c2c_subagent_lock.json exists
    if tool_name in cmd_tools:
        fast_start_denial = _check_fast_start_command_guard(cmd)
        if fast_start_denial is not None:
            return fast_start_denial

    active_lock = find_active_c2c_lock(custom_lock_file)
    if not active_lock:
        return {"decision": "allow"}

    caller_id = str(payload.get("conversationId") or payload.get("conversation_id") or "").strip()

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
                f_norm = forbidden.replace("\\", "/").lower().strip("/")
                if f_norm in p_lower:
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
                    if tool_name in full_write_tools:
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
                                    if has_syntax_error:
                                        return {"decision": "allow"}

                                    try:
                                        existing_lines = len(
                                            target_file_on_disk.read_text(encoding="utf-8", errors="ignore").splitlines()
                                        )
                                    except Exception:
                                        existing_lines = 0

                                    new_content = args.get("Content") or args.get("content") or ""
                                    if isinstance(new_content, list):
                                        new_lines = len(new_content)
                                    else:
                                        new_lines = len(str(new_content).splitlines())

                                    error_count = c_data.get("error_count")

                                    # Case 2: error_count is positive int (v3.5 contract)
                                    if isinstance(error_count, int) and error_count >= 1:
                                        if error_count < 6 and (existing_lines >= 40 or new_lines >= 40):
                                            extra_250 = " y supera las 250 líneas" if (existing_lines > 250 or new_lines > 250) else ""
                                            if target_type == "shard":
                                                return {
                                                    "decision": "deny",
                                                    "reason": (
                                                        f"BLOCKER:: El archivo {target_id}_data.py ya fue compilado ({existing_lines} líneas){extra_250} "
                                                        f"y registra {error_count} errores (< 6, umbral oficial). "
                                                        "Para menos de 6 errores está prohibido reescribir todo el archivo desde cero con write_file: "
                                                        "usa edit_file quirúrgico (replace_file_content) sobre las líneas reportadas "
                                                        "(ej. para insertar tuplas faltantes en TEMPLATES como en [M3-ARCHETYPES]), "
                                                        "o escribe un parche modular aislado en work/shards/shard_fixes/<CID>.py."
                                                    ),
                                                }
                                            else:
                                                return {
                                                    "decision": "deny",
                                                    "reason": (
                                                        f"BLOCKER:: El archivo {target_file_on_disk.name} ya fue compilado ({existing_lines} líneas){extra_250} "
                                                        f"y registra {error_count} errores (< 6, umbral oficial). "
                                                        "Para menos de 6 errores está prohibido reescribir todo el archivo desde cero con write_file: "
                                                        "usa edit_file quirúrgico (replace_file_content) sobre las líneas reportadas, "
                                                        "o escribe un parche modular aislado en work/cta_fixes/<CID>.py."
                                                    ),
                                                }
                                        elif error_count >= 6:
                                            return {"decision": "allow"}

                                    # Case 3: error_count is None or <= 0 (legacy fallback: > 250 lines deny, <= 250 lines allow)
                                    else:
                                        if existing_lines > 250 or new_lines > 250:
                                            if target_type == "shard":
                                                return {
                                                    "decision": "deny",
                                                    "reason": (
                                                        f"BLOCKER:: El archivo {target_id}_data.py ya fue compilado y supera las 250 líneas. "
                                                        "Para corregir errores de validación usa edit_file quirúrgico sobre las líneas indicadas "
                                                        "por el compilador o escribe un override modular en work/shards/shard_fixes/<CID>.py "
                                                        "en lugar de reescribir todo el archivo con write_file."
                                                    ),
                                                }
                                            else:
                                                return {
                                                    "decision": "deny",
                                                    "reason": (
                                                        f"BLOCKER:: El archivo {target_file_on_disk.name} ya fue compilado y supera las 250 líneas. "
                                                        "Para corregir errores de validación usa edit_file quirúrgico sobre las líneas indicadas "
                                                        "por el compilador o escribe un override modular en work/cta_fixes/<CID>.py "
                                                        "en lugar de reescribir todo el archivo con write_file."
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
                f_norm = forbidden.replace("\\", "/").lower().strip("/")
                if f_norm == "tests":
                    if re.search(r"(?:^|[\s/\\\"'])tests(?:/|\\|[\s\"']|$)", cmd_lower.replace("\\", "/")):
                        return {
                            "decision": "deny",
                            "reason": "C2C Worker Boundary: Inspection of tests source or test files via shell commands is strictly forbidden.",
                        }
                elif f_norm in cmd_lower:
                    return {
                        "decision": "deny",
                        "reason": f"C2C Worker Boundary: Inspection of protected source code or check attempts via shell commands is strictly forbidden: {forbidden}.",
                    }

        # Deny .NET file read in PowerShell
        if "[system.io.file]" in cmd_lower:
            for forbidden in WORKER_DENIED_READ_SUBSTRINGS:
                f_norm = forbidden.replace("\\", "/").lower().strip("/")
                if f_norm in cmd_lower:
                    return {
                        "decision": "deny",
                        "reason": f"C2C Worker Boundary: Inspection of protected files via PowerShell .NET APIs is strictly forbidden: {forbidden}.",
                    }

        # Deny python -c bypasses
        if re.search(r"(?:python(?:\.exe)?|py(?:\.exe)?)[/\"'\\]*\s+-c\b", cmd, re.IGNORECASE):
            # Check if python -c targets forbidden files
            for forbidden in WORKER_DENIED_READ_SUBSTRINGS:
                f_norm = forbidden.replace("\\", "/").lower().strip("/")
                if f_norm == "tests":
                    if re.search(r"(?:^|[\s/\\\"'])tests(?:/|\\|[\s\"']|$)", cmd.lower().replace("\\", "/")):
                        return {
                            "decision": "deny",
                            "reason": "C2C Worker Boundary: Subagents are forbidden from inspecting internal files via python -c: tests.",
                        }
                elif f_norm in cmd_lower:
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
