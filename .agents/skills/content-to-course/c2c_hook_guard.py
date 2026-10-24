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
from typing import Any, Dict, List, Optional, Set

LOCK_MAX_AGE_SECONDS = 7200  # 2 hours

REPO_ROOT = Path(__file__).resolve().parents[3]

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
            data = json.loads(p.read_text(encoding="utf-8"))
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
    if s.startswith("file:///"):
        s = s[8:]
    elif s.startswith("file://"):
        s = s[7:]
    try:
        s = urllib.parse.unquote(s)
    except Exception:
        pass
    s = s.replace("\\", "/")
    while "//" in s:
        s = s.replace("//", "/")
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
    ]
    for k in keys:
        if k in args and args[k]:
            paths.append(_normalize_path(args[k]))
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
    read_tools = ("read_file", "view_file", "read_resource")
    write_tools = (
        "write_file",
        "write_to_file",
        "edit_file",
        "replace_file_content",
        "multi_replace_file_content",
        "notebook_edit",
    )

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
            if re.search(
                r"\b(?:get-childitem|gci|dir|ls)\s+['\"]?(?:\./)?courses['\"]?(?:\s|$|;|\|)",
                cmd_norm_slashes,
                re.IGNORECASE,
            ):
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
            p_lower = p.lower()
            for forbidden in WORKER_DENIED_READ_SUBSTRINGS:
                f_norm = forbidden.replace("\\", "/").lower().strip("/")
                if f_norm in p_lower:
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

    # 3. Deny circumventing via shell commands
    if tool_name in cmd_tools:
        cmd_lower = cmd.lower()

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
                if f_norm in cmd_lower:
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
                if f_norm in cmd_lower:
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


def main() -> None:
    # Fail-open safety default with exit code 0 invariant
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({"decision": "allow"}))
            return
        payload = json.loads(raw_input)
        if not isinstance(payload, dict):
            print(json.dumps({"decision": "allow"}))
            return
    except Exception:
        print(json.dumps({"decision": "allow"}))
        return

    try:
        result = process_hook(payload)
        print(json.dumps(result, ensure_ascii=False))
    except Exception:
        print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
