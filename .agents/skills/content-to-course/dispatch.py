"""Scope Isolation, Subagent Dispatch Payload Generator, and Scope Check (C2C v3.2).

Provides zero-bundle dispatch and non-truncating payloads for C2C pipeline subagents:
- c2c_cta_architect: Cognitive Task Analysis Curriculum Architect
- c2c_shard_author: Shard Exercise Authors (pure Python tuples & compile_shard.py)
- c2c_judge: Independent Blind Evaluation Judges (Zero-Warmup In-Prompt resolution)
- c2c_repair: Targeted Repair subagents
"""

from __future__ import annotations

import argparse
import ast
import fnmatch
import hashlib
import json
import logging
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, Set

sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine.stage_contract import (  # noqa: E402
    DEFAULT_TEMPLATES_PER_MODALITY,
    competency_contract,
    contract_tokens as _s4_tokens,
    is_skill_type,
    quota_for_competency,
    quota_for_type,
    render_contract_tokens,
    required_templates_for_competency,
)

_S4 = _s4_tokens()
_S4_UNIQ_SKILL = _S4["<<S4_UNIQ_SKILL>>"]
_S4_UNIQ_OTHER = _S4["<<S4_UNIQ_OTHER>>"]
_S4_VARIANTS_OTHER = _S4["<<S4_VARIANTS_OTHER>>"]
_S4_VARIANTS_SKILL = _S4["<<S4_VARIANTS_SKILL>>"]
_S4_QUOTA_SKILL = _S4["<<S4_QUOTA_SKILL>>"]
_S4_QUOTA_OTHER = _S4["<<S4_QUOTA_OTHER>>"]

if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

logger = logging.getLogger("dispatch")

# Directory of the skill
SKILL_DIR = Path(__file__).parent.resolve()

GRANULARITY_SPECS: Dict[str, Tuple[str, float, float]] = {
    "standard": ("0.35-0.65 comp/pág (3-5 comps c/5-10 págs)", 0.35, 0.65),
    "fine": ("1.0-1.6 comp/pág (6-10 comps c/5-10 págs)", 1.0, 1.6),
    "coarse": ("0.15-0.30 comp/pág (1-2 comps/módulo)", 0.15, 0.30),
}


def _resolve_repo_python_and_env() -> Tuple[str, str, str]:
    """Resolves repo root, python executable, and compile command prefix.

    Returns:
        (repo_root_posix, python_exe_posix, cmd_prefix)
    """
    repo_root = SKILL_DIR.parents[2].resolve()
    if sys.platform == "win32":
        venv_py = repo_root / ".venv" / "Scripts" / "python.exe"
    else:
        venv_py = repo_root / ".venv" / "bin" / "python"

    if venv_py.is_file():
        py_exe = venv_py.resolve().as_posix()
    else:
        py_exe = Path(sys.executable).resolve().as_posix()

    repo_posix = repo_root.as_posix()
    if sys.platform == "win32":
        cmd_prefix = f'& "{py_exe}"'
    else:
        cmd_prefix = f'"{py_exe}"'
    return repo_posix, py_exe, cmd_prefix


def _clean_str(val: Any) -> str:
    """Sanitizes strings from CTA/manifest data, eliminating None, null, undefined, and empty values."""
    if val is None:
        return ""
    s = str(val).strip()
    if s.lower() in ("none", "null", "undefined"):
        return ""
    return s


def load_system_prompt(name_or_path: Union[str, Path], lean: bool = False) -> str:
    """Loads a system prompt markdown file and renders live Stage 4 contract tokens.

    When lean=True (or C2C_LEAN_PROMPTS=1 env var is set), loads the prompt from
    system_prompts/lean/ (synced with the M20 v4.3 full prompt, < 46,080 bytes).
    Otherwise loads directly from system_prompts/.
    """
    use_lean = lean or os.getenv("C2C_LEAN_PROMPTS", "").lower() in ("1", "true", "yes")
    p = Path(name_or_path)
    if not p.is_absolute():
        candidates = []
        if use_lean:
            candidates.extend([
                SKILL_DIR / "system_prompts" / "lean" / p.name,
                SKILL_DIR / "system_prompts" / f"{p.stem}_lean{p.suffix}",
            ])
        candidates.extend([
            SKILL_DIR / "system_prompts" / p.name,
            SKILL_DIR / p,
            Path.cwd() / p,
        ])
        for c in candidates:
            if c.is_file():
                return render_contract_tokens(c.read_text(encoding="utf-8"))
        raise FileNotFoundError(f"System prompt file not found: {name_or_path}")
    if not p.is_file():
        raise FileNotFoundError(f"System prompt file not found: {p}")
    return render_contract_tokens(p.read_text(encoding="utf-8"))


def get_type_definitions(lean: bool = True) -> List[Dict[str, Any]]:
    """Returns subagent type definitions for define_subagent registration.

    Loads M20 v4.3 system prompts (< 46,080 bytes) with rendered Stage 4 tokens.
    """
    repair_prompt = "prompt_repair.md"
    return [
        {
            "name": "c2c_cta_architect",
            "description": "Cognitive Task Analysis Curriculum Architect for C2C v3.2 (pure positional tuples in cta_data.py)",
            "system_prompt": load_system_prompt("prompt_cta_architect.md", lean=lean),
            "enable_write_tools": True,
            "enable_subagent_tools": False,
            "enable_mcp_tools": False,
        },
        {
            "name": "c2c_shard_author",
            "description": "Shard Exercise Author for native Python parametric templates and compile_shard.py",
            "system_prompt": load_system_prompt("prompt_shard_author.md", lean=lean),
            "enable_write_tools": True,
            "enable_subagent_tools": False,
            "enable_mcp_tools": False,
        },
        {
            "name": "c2c_judge",
            "description": "Independent Blind Psychometric Evaluation Judge with Zero-Warmup in-prompt resolution",
            "system_prompt": load_system_prompt("prompt_blind_judge.md", lean=lean),
            "enable_write_tools": True,
            "enable_subagent_tools": False,
            "enable_mcp_tools": False,
        },
        {
            "name": "c2c_repair",
            "description": "Targeted Quality Repair Engineer for fixing failing templates or discordances",
            "system_prompt": load_system_prompt(repair_prompt, lean=lean),
            "enable_write_tools": True,
            "enable_subagent_tools": False,
            "enable_mcp_tools": False,
        },
    ]


def make_pointer_prompt(
    role_name: str = "",
    work_order_rel: str = "",
    done_signal: Optional[str] = None,
    extra_instructions: Optional[str] = None,
    role: Optional[str] = None,
    item_file_rel: Optional[str] = None,
) -> str:
    """Generates an ultra-compact pointer prompt (~150-250 bytes, strictly <= 400 bytes) referencing disk JSON payload.
    
    Under the Pointer-Prompt Protocol (R5 / P4), the Director never types large work orders
    into invoke_subagent.Prompt. Instead, a compact pointer references the disk JSON payload.
    """
    r_name = role or role_name
    w_rel = item_file_rel or work_order_rel
    parts = [
        f"You are {r_name}.",
        f"Work order: `{w_rel}`. Read with `read_file`.",
    ]
    if extra_instructions:
        parts.append(extra_instructions)
    if done_signal:
        parts.append(f"{done_signal}." if not done_signal.endswith(".") else done_signal)
    prompt_str = " ".join(parts)
    return prompt_str


ROLE_SPECS: Dict[str, Dict[str, Any]] = {
    "cta": {
        "type_name": "c2c_cta_architect",
        "model": "inherit",
        "system_prompt": "system_prompts/lean/prompt_cta_architect.md",
        "read": [
            "work/ingestion_manifest.json",
            "work/pre_cta_manifest.json",
            "work/cta_data.py",
            "work/cta_parts/**",
            "work/cta/**",
            "work/cta.json",
            "content/**",
        ],
        "write": [
            "work/cta_data.py",
            "work/cta.json",
            "work/cta.md",
            "work/cta_parts/**",
            "work/cta/**",
            "work/cta_fixes/**",
            "work/cta_parts/cta_fixes/**",
        ],
        "forbidden": [
            ".agents/skills/content-to-course/compile_cta.py (leer)",
            ".agents/skills/content-to-course/check_cta.py",
            "engine/*",
            "SKILL.md",
            "tests/**",
            "scripts Python auxiliares en scratch/",
        ],
        "turn_budget": 20,
    },
    "cta-direct": {
        "type_name": "c2c_cta_architect",
        "model": "inherit",
        "system_prompt": "system_prompts/lean/prompt_cta_architect.md",
        "read": [
            "work/ingestion_manifest.json",
            "work/pre_cta_manifest.json",
            "work/cta_data.py",
            "work/cta_parts/**",
            "work/cta/**",
            "work/cta.json",
            "content/**",
        ],
        "write": [
            "work/cta_data.py",
            "work/cta.json",
            "work/cta.md",
            "work/cta_parts/**",
            "work/cta/**",
            "work/cta_fixes/**",
            "work/cta_parts/cta_fixes/**",
        ],
        "forbidden": [
            ".agents/skills/content-to-course/compile_cta.py (leer)",
            ".agents/skills/content-to-course/check_cta.py",
            "engine/*",
            "SKILL.md",
            "tests/**",
            "scripts Python auxiliares en scratch/",
        ],
        "turn_budget": 20,
    },
    "author": {
        "type_name": "c2c_shard_author",
        "model": "inherit",
        "system_prompt": "system_prompts/lean/prompt_shard_author.md",
        "read": [
            "content/**",
            "work/dispatch/items/author_*.json",
            "work/pre_cta_manifest.json",
            "work/shards/pre_shard_manifest.json",
            "work/shards/*_data.py",
            "work/templates/*.json",
            "work/cta.json",
        ],
        "write": [
            "work/shards/*_data.py",
            "work/shards/*.json",
            "work/templates/*.json",
            "work/shards/shard_fixes/<shard_id>/<CID>.py",
            "work/shards/shard_fixes/<CID>.py",
        ],
        "forbidden": [
            "tests/**",
            ".agents/skills/content-to-course/compile_shard.py",
            "scratch/**",
            "work/scratch/**",
            "engine/*",
            "SKILL.md",
            ".check_attempts/**",
            ".agents/skills/content-to-course/check_templates.py",
            ".agents/skills/content-to-course/check_cta.py",
            "src/validator/**",
        ],
        "turn_budget": 30,
    },
    "judge": {
        "type_name": "c2c_judge",
        "model": "inherit",
        "system_prompt": "system_prompts/lean/prompt_blind_judge.md",
        "read": [
            "work/verification/judge_batch_*.json",
            "work/judge_batch_*.json",
        ],
        "write": [
            "work/verification/judge_responses_*.json",
            "work/judge_responses_*.json",
            "work/judges/judge_*.json",
            "work/judges/*.json",
            "work/judges/**",
        ],
        "forbidden": [
            "judge_ground_truth.json",
            "work/templates/*",
            "templates/*",
            "engine/*",
            "search_web",
            "read_url_content",
            "navegación por internet",
        ],
        "turn_budget": 5,
    },
    "repair": {
        "type_name": "c2c_repair",
        "model": "inherit",
        "system_prompt": "system_prompts/lean/prompt_repair.md",
        "read": [
            "work/shards/*",
            "work/dispatch/repair_slices/*.json",
            "work/dispatch/items/repair_*.json",
            "work/prompts/repair/*.json",
            "work/reports/templates_report.json",
            "work/judge_report.json",
            "work/templates/*.json",
        ],
        "write": [
            "work/shards/*_data.py",
            "work/shards/*.json",
            "work/templates/*.json",
            "work/shards/shard_fixes/<shard_id>/<CID>.py",
            "work/shards/shard_fixes/<CID>.py",
        ],
        "forbidden": [
            "tests/**",
            ".agents/skills/content-to-course/compile_shard.py",
            "engine/*",
            "SKILL.md",
            ".agents/skills/content-to-course/check_templates.py",
            ".agents/skills/content-to-course/check_cta.py",
            "src/validator/**",
        ],
        "turn_budget": 15,
    },
    "cta-map": {
        "type_name": "c2c_cta_architect",
        "model": "inherit",
        "system_prompt": "system_prompts/lean/prompt_cta_architect.md",
        "read": [
            "work/parts/part_*/**",
            "work/parts/part_manifest_*.json",
            "work/pre_cta_manifest.json",
            "work/ingestion_manifest.json",
        ],
        "write": [
            "work/cta_parts/part_*.py",
            "work/cta_parts/cta_part_*.json",
            "work/cta/cta_shard_*_data.py",
            "work/cta/cta_shard_*.json",
            "work/cta_fixes/**",
            "work/cta_parts/cta_fixes/**",
        ],
        "forbidden": [
            ".agents/skills/content-to-course/compile_cta.py (leer)",
            ".agents/skills/content-to-course/check_cta.py",
            "código fuente",
            "SKILL.md",
            "tests/**",
        ],
        "turn_budget": 15,
    },
    "cta-reduce": {
        "type_name": "c2c_cta_harmonizer",
        "model": "inherit",
        "system_prompt": "system_prompts/lean/prompt_cta_harmonizer.md",
        "read": [
            "work/cta_outline.json",
            "work/duplicate_candidates.json",
            "work/cta_parts/*.json",
            "work/cta/cta_shard_*.json",
        ],
        "write": [
            "work/cta_harmonize.json",
            "work/cta.json",
            "work/cta.md",
        ],
        "forbidden": [
            "código fuente",
            "SKILL.md",
        ],
        "turn_budget": 10,
    },
}


def build_scope_header(
    role: str,
    read_paths: Optional[List[str]] = None,
    write_paths: Optional[List[str]] = None,
    forbidden_paths: Optional[List[str]] = None,
    done_signal: Optional[str] = None,
) -> str:
    """Builds a standardized Markdown Scope-Lock header with allowed/forbidden paths and DONE signal."""
    spec = ROLE_SPECS.get(role, {})
    r_paths = read_paths if read_paths is not None else spec.get("read", [])
    w_paths = write_paths if write_paths is not None else spec.get("write", [])
    f_paths = forbidden_paths if forbidden_paths is not None else spec.get("forbidden", [])

    lines = [
        "## 0. SCOPE-LOCK Y CONTRATO DE EJECUCIÓN",
        f"- **Rol:** `{role}`",
        "- READ permitido:",
    ]
    if r_paths:
        for p in r_paths:
            lines.append(f"  - `{p}`")
    else:
        lines.append("  - (Ninguno adicional fuera de este prompt)")

    lines.append("- WRITE permitido:")
    if w_paths:
        for p in w_paths:
            lines.append(f"  - `{p}`")
    else:
        lines.append("  - (Ninguno)")

    lines.append("- PROHIBIDO:")
    if f_paths:
        for p in f_paths:
            lines.append(f"  - `{p}`")
    else:
        lines.append("  - Modificar archivos fuera de las rutas de WRITE permitidas")

    if done_signal:
        lines.append(f"- **SEÑAL DE FINALIZACIÓN:** Responder estrictamente con `{done_signal}` al completar.")

    return "\n".join(lines)


def _atomic_write_text(path: Path, text: str, encoding: str = "utf-8") -> None:
    """Atomically writes text to path via a sibling temporary file and os.replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding=encoding) as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, str(path))
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def _matches_token(token: str, text: str) -> bool:
    """Returns True if token appears in text bounded by non-alphanumeric delimiters."""
    if not token or not text:
        return False
    return bool(re.search(rf"(?<![A-Za-z0-9]){re.escape(token)}(?![A-Za-z0-9])", text))


ROLE_ALIASES: Dict[str, str] = {
    "authors": "author",
    "c2c_shard_author": "author",
    "judges": "judge",
    "c2c_judge": "judge",
    "c2c_cta_architect": "cta",
    "c2c_cta_harmonizer": "cta-reduce",
    "c2c_repair": "repair",
}


def _normalize_role(role: str) -> str:
    """Normalizes role aliases to canonical ROLE_SPECS keys."""
    r = (role or "").strip().lower()
    return ROLE_ALIASES.get(r, r)


def get_work_rel(work_dir: Union[str, Path]) -> str:
    """Returns normalized relative POSIX path for work_dir within cwd or repo root, falling back to 'work'."""
    p = Path(work_dir)
    if not p.is_absolute():
        p_str = p.as_posix()
        if p_str == "work" or p_str.startswith("courses/"):
            return p_str
        resolved = (Path.cwd() / p).resolve()
    else:
        resolved = p.resolve()

    try:
        rel = resolved.relative_to(Path.cwd().resolve())
        return rel.as_posix()
    except ValueError:
        pass

    try:
        repo_root = SKILL_DIR.parents[2].resolve()
        rel = resolved.relative_to(repo_root)
        return rel.as_posix()
    except (ValueError, IndexError):
        pass

    return "work"


def _resolve_posix_path(work: Path, work_rel: str, raw_path: str) -> str:
    """Resolves a relative or absolute path to a canonical POSIX absolute path."""
    if not raw_path:
        return work.resolve().as_posix()
    clean = str(raw_path).replace("\\", "/")
    if "*" in clean:
        return clean
    p_obj = Path(clean)
    if p_obj.is_absolute():
        return p_obj.resolve().as_posix()
    if work_rel and clean.startswith(f"{work_rel}/"):
        return (work / clean[len(work_rel) + 1:]).resolve().as_posix()
    if clean.startswith("work/"):
        return (work / clean[5:]).resolve().as_posix()
    for base in (work, work.parent, SKILL_DIR.parents[2]):
        cand = base / clean
        if cand.exists():
            return cand.resolve().as_posix()
    return (work.parent / clean).resolve().as_posix()


def _locate_competency_line_range(shard_py: Path, cid: str) -> Tuple[Optional[int], Optional[int]]:
    """Deterministically locates line_range (start, end) for cid in shard_XX_data.py (< 2 ms)."""
    if not shard_py.is_file() or not cid:
        return None, None
    try:
        text = shard_py.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, None

    cid_str = str(cid)
    cid_norm = re.sub(r"[^\w]", "", cid_str).lower()
    t_prefix_dash = f"T-{cid_str}-"
    t_prefix_us = f"T-{cid_str}_"
    t_exact = f"T-{cid_str}"

    def _is_cid_str(val: Any) -> bool:
        if not isinstance(val, str):
            return False
        return val == cid_str or val == t_exact or val.startswith(t_prefix_dash) or val.startswith(t_prefix_us)

    def _fn_matches_cid(fn_name: str) -> bool:
        if not (fn_name.startswith("gen_") or fn_name.startswith("ver_")):
            return False
        norm_fn = re.sub(r"[^\w]", "", fn_name).lower()
        # Check bounded token match (e.g. gen_c01_01 matches c01, not c010)
        return bool(
            re.search(rf"^(?:gen|ver){re.escape(cid_norm)}(?:_|\D|$)", norm_fn)
            or re.search(rf"(?:^|_)(?:gen|ver)_{re.escape(cid_norm)}(?:_|\D|$)", fn_name.lower().replace("-", "_"))
        )

    starts: List[int] = []
    ends: List[int] = []

    try:
        tree = ast.parse(text)
        fn_ranges: Dict[str, Tuple[int, int]] = {}
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and (node.name.startswith("gen_") or node.name.startswith("ver_")):
                fn_s = getattr(node, "lineno", None)
                fn_e = getattr(node, "end_lineno", fn_s)
                if fn_s is not None:
                    fn_ranges[node.name] = (fn_s, fn_e or fn_s)
                    if _fn_matches_cid(node.name):
                        starts.append(fn_s)
                        ends.append(fn_e or fn_s)

        for node in tree.body:
            target_names: List[str] = []
            val_node: Optional[ast.AST] = None
            if isinstance(node, ast.Assign):
                target_names = [t.id for t in node.targets if isinstance(t, ast.Name)]
                val_node = node.value
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                target_names = [node.target.id]
                val_node = node.value

            if "TEMPLATES" in target_names and isinstance(val_node, (ast.List, ast.Tuple)):
                for elt in val_node.elts:
                    matched_elt = False
                    for sub in ast.walk(elt):
                        if isinstance(sub, ast.Constant) and _is_cid_str(sub.value):
                            matched_elt = True
                            break
                    if matched_elt:
                        e_s = getattr(elt, "lineno", None)
                        e_e = getattr(elt, "end_lineno", e_s)
                        if e_s is not None:
                            starts.append(e_s)
                            ends.append(e_e or e_s)
                        for sub in ast.walk(elt):
                            if isinstance(sub, ast.Name) and sub.id in fn_ranges:
                                fn_s, fn_e = fn_ranges[sub.id]
                                starts.append(fn_s)
                                ends.append(fn_e)

        if starts and ends:
            return min(starts), max(ends)
    except SyntaxError:
        pass

    # Fast line-scan fallback (handles SyntaxError or non-AST templates)
    lines = text.splitlines()
    cid_esc = re.escape(cid_str)
    tpl_pat = re.compile(
        rf"""['"](?:cid)['"]\s*:\s*['"]{cid_esc}['"]|['"]T-{cid_esc}(?:[-_][^'"]*)?['"]|['"]{cid_esc}['"]"""
    )
    fn_pat = re.compile(r"^\s*def\s+((?:gen|ver)_[A-Za-z0-9_]+)\s*\(")
    in_matching_fn = False
    for lineno, line in enumerate(lines, start=1):
        m_fn = fn_pat.match(line)
        if m_fn:
            in_matching_fn = _fn_matches_cid(m_fn.group(1))
            if in_matching_fn:
                starts.append(lineno)
                ends.append(lineno)
            continue
        if in_matching_fn:
            if line and not line[0].isspace() and not line.startswith("#"):
                in_matching_fn = False
            else:
                ends.append(lineno)
        if tpl_pat.search(line):
            starts.append(lineno)
            ends.append(lineno)

    if starts and ends:
        return min(starts), max(ends)
    return None, None


def generate_define_subagent_specs(work_dir: Union[str, Path], lean: bool = True) -> Dict[str, Any]:
    """Writes individual subagent type spec files in work/dispatch/types/<type_name>.json
    and the consolidated index in work/dispatch/subagent_types.json.
    
    When lean=True (default), persists lean static system prompts strictly <= 5 KB.
    """
    work = Path(work_dir).resolve()
    types_dir = work / "dispatch" / "types"
    types_dir.mkdir(parents=True, exist_ok=True)

    types_list = list(get_type_definitions(lean=lean))
    type_files: List[str] = []

    granularity = "standard"
    for m_name in ("pre_cta_manifest.json", "ingestion_manifest.json"):
        m_path = work / m_name
        if m_path.is_file():
            try:
                m_data = json.loads(m_path.read_text(encoding="utf-8"))
                g_val = m_data.get("granularity")
                if isinstance(g_val, str) and g_val in GRANULARITY_SPECS:
                    granularity = g_val
                break
            except Exception as e:
                logger.warning("Could not read granularity from %s: %s", m_path, e)

    gran_label = GRANULARITY_SPECS[granularity][0]

    for t_spec in types_list:
        t_name = t_spec["name"]
        if t_name == "c2c_cta_architect" and "system_prompt" in t_spec:
            t_spec["system_prompt"] = re.sub(
                r'granularity="[^"]*"',
                f'granularity="{gran_label}"',
                t_spec["system_prompt"],
                count=1,
            )
        clean_name = t_name.replace("-", "_")
        t_file = types_dir / f"{clean_name}.json"
        _atomic_write_text(t_file, json.dumps(t_spec, indent=2, ensure_ascii=False))
        type_files.append(t_file.resolve().as_posix())

    # Auxiliary type definition: c2c_cta_harmonizer for cta-reduce
    try:
        harmonizer_prompt = load_system_prompt("prompt_cta_harmonizer.md", lean=lean)
        harmonizer_spec = {
            "name": "c2c_cta_harmonizer",
            "description": "Cognitive Task Analysis Harmonizer for deduplicating and merging sectional CTA parts",
            "system_prompt": harmonizer_prompt,
            "enable_write_tools": True,
            "enable_subagent_tools": False,
            "enable_mcp_tools": False,
        }
        h_file = types_dir / "c2c_cta_harmonizer.json"
        _atomic_write_text(h_file, json.dumps(harmonizer_spec, indent=2, ensure_ascii=False))
        type_files.append(h_file.resolve().as_posix())
    except Exception as e:
        logger.warning("Could not write c2c_cta_harmonizer.json: %s", e)

    summary_payload = {
        "types": types_list,
        "type_files": type_files,
    }

    subagent_types_file = work / "dispatch" / "subagent_types.json"
    _atomic_write_text(subagent_types_file, json.dumps(summary_payload, indent=2, ensure_ascii=False))

    return summary_payload


def dispatch_cta(
    work_dir: Union[str, Path],
    mode: Optional[str] = None,
    pointer: bool = True,
) -> Dict[str, Any]:
    """Generates dispatch payload and individual item files for CTA Architect (Load Inversion v3.21).
    
    Exige pre_cta_manifest.json o ingestion_manifest.json (cero fallbacks; si no existe, lanza BLOCKER).
    En modo direct y mapreduce: genera ítems concisos (< 2,500 caracteres) en work/dispatch/items/cta_XX.json
    sin duplicar el system prompt, inyectando tabla de documentos, rangos físicos 1..N y contrato compile_cta.py.
    When pointer=True (default), generates ultra-compact (~350-500 B) pointer prompts in the ready-made Subagents array.
    """
    work = Path(work_dir).resolve()
    work_rel = get_work_rel(work)
    use_pointer = pointer if pointer is not None else (os.getenv("C2C_POINTER_PROMPTS", "1").lower() in ("1", "true", "yes"))
    manifest_path = work / "pre_cta_manifest.json"
    if not manifest_path.is_file():
        alt_m = work / "ingestion_manifest.json"
        if alt_m.is_file():
            manifest_path = alt_m
        else:
            err_msg = "BLOCKER:: No existe pre_cta_manifest.json"
            logger.error(err_msg)
            raise FileNotFoundError(err_msg)

    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    cta_mode = mode or manifest_data.get("cta_mode") or manifest_data.get("mode") or "direct"
    granularity = manifest_data.get("granularity", "standard")
    if granularity not in GRANULARITY_SPECS:
        granularity = "standard"
    gran_label, low_rate, high_rate = GRANULARITY_SPECS[granularity]
    manifest_rel = f"{work_rel}/ingestion_manifest.json" if (work / "ingestion_manifest.json").is_file() else f"{work_rel}/pre_cta_manifest.json"

    # Append Delta context detection
    delta_manifest_path = work / "delta_manifest.json"
    delta_info: Dict[str, Any] = {}
    if delta_manifest_path.is_file():
        try:
            delta_info = json.loads(delta_manifest_path.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning("Could not load delta_manifest.json: %s", e)
    elif isinstance(manifest_data.get("delta"), dict):
        delta_info = manifest_data["delta"]

    next_ids_by_prefix = delta_info.get("next_ids_by_prefix", {})
    existing_comps_outline = delta_info.get("existing_competencies_outline", [])
    delta_block = ""
    if delta_info:
        delta_lines = [
            "",
            "## APPEND DELTA MODE: COMPETENCIAS BASE EXISTENTES Y SECUENCIA DE IDs",
            "> [!IMPORTANT]",
            f"> - **Secuencia de inicio para IDs nuevos:** `{next_ids_by_prefix}`",
            "> - **PROHIBIDO reiniciar la numeración en 01 o duplicar competencias base.**",
            "> - **Competencias existentes en el curso base (NO DUPLICAR):**",
        ]
        for c in existing_comps_outline:
            cid = c.get("id", "")
            ctype = c.get("type", "")
            cname = c.get("name", "")
            delta_lines.append(f">   * `{cid}` ({ctype}): {cname}")
        delta_block = "\n".join(delta_lines)

    total_physical_pages = manifest_data.get("total_pages")
    if total_physical_pages is None:
        raw_files = manifest_data.get("documents") or manifest_data.get("files") or []
        total_physical_pages = sum(f.get("total_pages", 0) for f in raw_files if isinstance(f, dict)) or 1

    items_dir = work / "dispatch" / "items"
    items_dir.mkdir(parents=True, exist_ok=True)
    for old_cf in items_dir.glob("cta_*.json"):
        try:
            old_cf.unlink()
        except Exception:
            pass

    _, _, cmd_prefix = _resolve_repo_python_and_env()

    subagents: List[Dict[str, Any]] = []
    item_files: List[str] = []

    if cta_mode == "mapreduce":
        subparts = manifest_data.get("subparts") or manifest_data.get("parts") or []
        if not subparts:
            files_list = manifest_data.get("files") or manifest_data.get("documents") or []
            subparts = [
                {
                    "subpart_id": f"part_{i+1:02d}",
                    "subpart_index": i,
                    "doc": f.get("doc") or f.get("doc_name") or f.get("name") or "document.pdf",
                    "path": f.get("path") or f.get("file") or f.get("doc") or "document.pdf",
                    "page_range": f.get("valid_page_range") or f.get("page_range") or [1, f.get("total_pages", 1)],
                    "total_pages": f.get("total_pages", 1),
                }
                for i, f in enumerate(files_list)
            ]
        if not subparts:
            subparts = [
                {
                    "subpart_id": "part_01",
                    "subpart_index": 0,
                    "doc": "material_fuente.pdf",
                    "path": "material_fuente.pdf",
                    "page_range": [1, 1],
                    "total_pages": 1,
                }
            ]

        # Swift-Dispatch SLA: Order subparts heaviest partition first
        def _subpart_weight(sp: Dict[str, Any]) -> int:
            explicit = sp.get("total_pages") or sp.get("slide_count") or sp.get("pages")
            if explicit:
                return int(explicit)
            pr = sp.get("page_range") or sp.get("valid_page_range") or [1, 1]
            if isinstance(pr, (list, tuple)) and len(pr) >= 2:
                return int(pr[1]) - int(pr[0]) + 1
            return 1

        subparts = sorted(subparts, key=_subpart_weight, reverse=True)

        syllabus_map: List[Dict[str, Any]] = []
        for idx_sm, sp_sm in enumerate(subparts, start=1):
            p_idx_sm = sp_sm.get("part_index") or idx_sm
            sp_id_sm = sp_sm.get("subpart_id") or f"part_{p_idx_sm:02d}"
            sp_doc_sm = sp_sm.get("doc") or sp_sm.get("doc_name") or sp_sm.get("name") or "document.pdf"
            sp_range_sm = sp_sm.get("page_range") or sp_sm.get("valid_page_range") or [1, sp_sm.get("total_pages", 1)]
            sp_s_sm = sp_range_sm[0] if len(sp_range_sm) > 0 else 1
            sp_e_sm = sp_range_sm[1] if len(sp_range_sm) > 1 else sp_s_sm
            sp_total_sm = sp_sm.get("total_pages") or (sp_e_sm - sp_s_sm + 1)
            syllabus_map.append({
                "subpart_id": sp_id_sm,
                "doc": sp_doc_sm,
                "page_range": [sp_s_sm, sp_e_sm],
                "total_pages": sp_total_sm,
            })

        syllabus_lines = [
            "",
            "## 2.1 MAPA GLOBAL DE SUBPARTES (SYLLABUS MAP — EVITAR EXTRACCIÓN REDUNDANTE)",
            "> Extrae SOLO competencias del slice asignado arriba; las demás subpartes cubren sus propios rangos:",
            "| Subparte | Documento | Rango Físico | Páginas |",
            "|---|---|---|---|",
        ]
        for sm in syllabus_map:
            s_r = sm["page_range"]
            syllabus_lines.append(
                f"| `{sm['subpart_id']}` | `{sm['doc']}` | `{s_r[0]}..{s_r[1]}` | {sm['total_pages']} |"
            )
        syllabus_section = "\n".join(syllabus_lines)

        for idx, sp in enumerate(subparts, start=1):
            part_idx = sp.get("part_index") or idx
            subpart_id = sp.get("subpart_id") or f"part_{part_idx:02d}"
            doc_name = sp.get("doc") or sp.get("doc_name") or sp.get("name") or "document.pdf"
            doc_path = sp.get("path") or sp.get("file") or doc_name
            c_type = sp.get("content_type") or sp.get("type") or "pdf"
            v_range = sp.get("page_range") or sp.get("valid_page_range") or [1, sp.get("total_pages", 1)]
            s_p = v_range[0] if len(v_range) > 0 else 1
            e_p = v_range[1] if len(v_range) > 1 else s_p
            total_p = sp.get("total_pages") or (e_p - s_p + 1)
            t_ref = sp.get("slice_path") or sp.get("text_ref") or sp.get("page_index_path") or sp.get("pages_dir") or doc_path
            if not t_ref or not doc_path:
                raise RuntimeError(f"BLOCKER:: Missing source path or slice for subpart {subpart_id}")

            out_py = f"{work_rel}/cta/{subpart_id}_data.py" if "cta_shard" in subpart_id else f"{work_rel}/cta_parts/{subpart_id}_data.py"
            json_target = f"{work_rel}/cta/{subpart_id}.json" if "cta_shard" in subpart_id else f"{work_rel}/cta_parts/{subpart_id}.json"

            subpart_table = "\n".join([
                "| Documento Subpart | Ruta Fuente | Tipo | Rango Físico (1..N) | Páginas | Referencia Texto |",
                "|---|---|---|---|---|---|",
                f"| `{doc_name}` | `{doc_path}` | `{c_type}` | **`{s_p}..{e_p}`** | {total_p} | `{t_ref}` |",
            ])

            compile_cmd = f"{cmd_prefix} .agents/skills/content-to-course/compile_cta.py --input {out_py} --output {json_target} --manifest {manifest_rel} --part {subpart_id}"
            pdf_slice_candidate = str(sp.get("slice_path") or doc_path).replace("\\", "/")
            is_pdf_slice = bool(pdf_slice_candidate) and pdf_slice_candidate.lower().endswith(".pdf")
            if is_pdf_slice:
                read_paths = list(dict.fromkeys([doc_path, t_ref]))
            else:
                read_paths = list(dict.fromkeys([manifest_rel, doc_path, t_ref]))
            cta_fix_target = f"{work_rel}/cta_parts/cta_fixes/<CID>.py" if "cta_parts" in out_py else f"{work_rel}/cta_fixes/<CID>.py"
            disk_done_signal = f"Cierre al aprobar: {json_target} (señal terminal DONE)"
            scope_header = build_scope_header(
                role="cta-map",
                read_paths=read_paths,
                write_paths=[out_py, json_target, cta_fix_target],
                done_signal=disk_done_signal,
            )

            min_c = max(2, round(low_rate * total_p))
            max_c = max(min_c + 1, round(high_rate * total_p))

            prompt_lines = [
                f"# Asignación de Tarea: Cognitive Task Analysis Architect ({subpart_id} - MapReduce C2C v3.21)",
                "",
                scope_header,
                "",
                "## 1. PARÁMETROS DE LA SUBPARTE",
                f"- **Manifest:** `{manifest_rel}`",
                f"- **CTA Mode:** `mapreduce` (Subpart: `{subpart_id}`)",
                f"- **Granularity:** `{granularity}` ({gran_label}; presupuesto slice: **{min_c}–{max_c} competencias** para {total_p} págs)",
                f"- **Total Physical Pages:** {total_physical_pages}",
                f"- **Archivo Python de Salida:** `{out_py}`",
                f"- **Destino JSON Final:** `{json_target}`",
            ]
            if delta_block:
                prompt_lines.append(delta_block)

            prompt_lines.extend([
                "",
                "## 2. DOCUMENTO ASIGNADO A ESTA SUBPARTE Y RANGO DE PÁGINAS (1..N)",
                subpart_table,
                syllabus_section,
                "",
                "> [!CRITICAL]",
                "> **REGLA MANDATORIA DE PAGINACIÓN `evidence.page`:**",
                f"> SIEMPRE usa el índice de página 1-indexed del archivo PDF (`{s_p}..{e_p}` según la tabla anterior), NUNCA la numeración impresa del libro o capítulo.",
                "",
                "## 3. DIRECTIVAS DE OPERACIÓN",
                f"1. Lee `{doc_path}` con `read_file` y escribe `COMPETENCIES = [...]` (tuplas de 11 elementos —11.º obligatorio `recommended_modalities` con 2..4 modalidades canónicas—, `CTA_CONTRACT_VERSION = 2`) en `{out_py}`.",
                f"2. Compila deterministamente: `{compile_cmd}`",
                f"3. Con < 6 errores (1..5 errores), corrige con edit_file (replace_file_content) sobre `{out_py}` (PROHIBIDO write_file completo cuando hay < 6 errores); con >= 6 errores, usa cta_fixes/<CID>.py (1-2 comps) o write_file(Overwrite=True).",
                f"4. Cierre al aprobar: `{json_target}` (señal terminal DONE).",
            ])
            prompt_full = "\n".join(prompt_lines)

            prompt_sha256 = hashlib.sha256(prompt_full.encode("utf-8")).hexdigest()
            item_file = items_dir / f"cta_{idx:02d}.json"
            work_order_meta = {
                "role": f"Cognitive Task Analysis Architect {subpart_id}",
                "subpart_id": subpart_id,
                "output_python": out_py,
                "output_json": json_target,
                "compile_cmd": compile_cmd,
                "compile_command": compile_cmd,
                "prompt_sha256": prompt_sha256,
                "syllabus_map": syllabus_map,
                "target_competency_range": [min_c, max_c],
            }
            item_data = {
                "TypeName": "c2c_cta_architect",
                "Role": f"Cognitive Task Analysis Architect {subpart_id}",
                "Model": "inherit",
                "Workspace": "inherit",
                "Prompt": prompt_full,
                "work_order": work_order_meta,
                "subpart_id": subpart_id,
                "output_python": out_py,
                "output_json": json_target,
                "compile_command": compile_cmd,
            }
            if delta_info:
                item_data["delta_context"] = {
                    "next_ids_by_prefix": next_ids_by_prefix,
                    "existing_competencies_outline": existing_comps_outline,
                }
            item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")

            if use_pointer:
                abs_out_py = _resolve_posix_path(work, work_rel, out_py)
                if is_pdf_slice:
                    abs_slice = _resolve_posix_path(work, work_rel, pdf_slice_candidate)
                    delta_hint = f" Delta: {next_ids_by_prefix}." if delta_info else ""
                    pointer_prompt = (
                        f"You are CTA Architect {subpart_id}. [SCOPE-LOCK] "
                        f"READ: `{abs_slice}`. Doc: `{doc_name}`. Rango: `1..{total_p}` (orig `{s_p}..{e_p}`). "
                        f"WRITE: `{abs_out_py}`. COMPILE: `{compile_cmd}`.{delta_hint} "
                        f"DONE: `{json_target}`."
                    )
                    if len(pointer_prompt.encode("utf-8")) > 650:
                        short_compile_cmd = compile_cmd.replace(f"{cmd_prefix} ", "python ", 1)
                        pointer_prompt = (
                            f"You are CTA Architect {subpart_id}. [SCOPE-LOCK] "
                            f"READ: `{abs_slice}`. Doc: `{doc_name}`. Rango: `1..{total_p}`. "
                            f"WRITE: `{abs_out_py}`. COMPILE: `{short_compile_cmd}`. "
                            f"DONE: `{json_target}`."
                        )
                else:
                    w_abs = item_file.resolve().as_posix()
                    abs_doc = _resolve_posix_path(work, work_rel, doc_path)
                    extra = f"[SCOPE-LOCK] READ: `{w_abs}`, `{abs_doc}`; WRITE: `{abs_out_py}`; COMPILE: `.agents/skills/content-to-course/compile_cta.py`."
                    if delta_info:
                        cand_extra = extra + f" Delta: {next_ids_by_prefix}."
                        if len(make_pointer_prompt(role_name=f"CTA Architect {subpart_id}", work_order_rel=w_abs, done_signal=f"DONE: {json_target}", extra_instructions=cand_extra).encode("utf-8")) <= 650:
                            extra = cand_extra
                    pointer_prompt = make_pointer_prompt(
                        role_name=f"CTA Architect {subpart_id}",
                        work_order_rel=w_abs,
                        done_signal=f"DONE: {json_target}",
                        extra_instructions=extra,
                    )
                    if len(pointer_prompt.encode("utf-8")) > 650:
                        extra = f"[SCOPE-LOCK] READ: `{w_abs}`; WRITE: `{abs_out_py}`; COMPILE: `.agents/skills/content-to-course/compile_cta.py`."
                        pointer_prompt = make_pointer_prompt(
                            role_name=f"CTA Architect {subpart_id}",
                            work_order_rel=w_abs,
                            done_signal=f"DONE: {json_target}",
                            extra_instructions=extra,
                        )
                subagent_item = {
                    "TypeName": "c2c_cta_architect",
                    "Role": f"Cognitive Task Analysis Architect {subpart_id}",
                    "Model": "inherit",
                    "Prompt": pointer_prompt,
                }
            else:
                inline_data = dict(item_data)
                inline_data["Prompt"] = prompt_full.replace(disk_done_signal, f"DONE: {json_target}")
                subagent_item = inline_data

            subagents.append(subagent_item)
            item_files.append(item_file.resolve().as_posix())

    else:
        # direct mode
        out_target = f"{work_rel}/cta_data.py"
        json_target = f"{work_rel}/cta.json"

        docs = manifest_data.get("documents") or manifest_data.get("files") or []
        doc_rows: List[Tuple[str, str, str, str, Any, str]] = []
        if isinstance(docs, list):
            for d in docs:
                if isinstance(d, dict):
                    d_name = d.get("doc_name") or d.get("name") or d.get("doc") or "document.pdf"
                    d_path = d.get("path") or d.get("file") or d_name
                    c_type = d.get("content_type") or d.get("type") or "pdf"
                    v_range = d.get("valid_page_range") or d.get("page_range") or [1, d.get("total_pages", 1)]
                    s_p = v_range[0] if len(v_range) > 0 else 1
                    e_p = v_range[1] if len(v_range) > 1 else s_p
                    tot = d.get("total_pages") or (e_p - s_p + 1)
                    t_ref = d.get("slice_path") or d.get("text_ref") or d.get("page_index_path") or d.get("pages_dir") or d_path
                    if not t_ref or not d_path:
                        raise RuntimeError(f"BLOCKER:: Missing source path or slice for document {d_name}")
                    doc_rows.append((d_name, d_path, c_type, f"{s_p}..{e_p}", tot, t_ref))
                elif isinstance(d, str):
                    doc_rows.append((d, d, "pdf", "1..N", "desconocido", d))
        elif isinstance(docs, dict):
            for d_name, d_info in docs.items():
                if isinstance(d_info, dict):
                    c_type = d_info.get("content_type") or d_info.get("type") or "pdf"
                    v_range = d_info.get("valid_page_range") or d_info.get("page_range") or [1, d_info.get("total_pages", 1)]
                    s_p = v_range[0] if len(v_range) > 0 else 1
                    e_p = v_range[1] if len(v_range) > 1 else s_p
                    tot = d_info.get("total_pages") or (e_p - s_p + 1)
                    d_path = d_info.get("path") or d_name
                    t_ref = d_info.get("slice_path") or d_info.get("text_ref") or d_info.get("page_index_path") or d_info.get("pages_dir") or d_path
                    if not t_ref or not d_path:
                        raise RuntimeError(f"BLOCKER:: Missing source path or slice for document {d_name}")
                    doc_rows.append((d_name, d_path, c_type, f"{s_p}..{e_p}", tot, t_ref))

        if len(doc_rows) > 10:
            table_lines = [
                "| # | Documento | Rango Físico (1..N) | Páginas |",
                "|---|---|---|---|",
            ]
            for i, r in enumerate(doc_rows, 1):
                table_lines.append(f"| {i} | `{r[0]}` | **`{r[3]}`** | {r[4]} |")
            doc_table_str = f"- **Total de documentos asignados:** {len(doc_rows)} archivos (ver `{manifest_rel}`).\n\n" + "\n".join(table_lines)
        else:
            table_lines = [
                "| Documento | Rango Físico (1..N) | Páginas | Referencia Texto |",
                "|---|---|---|---|",
            ]
            for r in doc_rows:
                table_lines.append(f"| `{r[0]}` | **`{r[3]}`** | {r[4]} | `{r[5]}` |")
            doc_table_str = "\n".join(table_lines)

        compile_cmd = f"{cmd_prefix} .agents/skills/content-to-course/compile_cta.py --input {out_target} --output {json_target} --manifest {manifest_rel}"
        disk_done_signal = f"Cierre al aprobar: {json_target} (señal terminal DONE)"
        scope_header = build_scope_header(
            role="cta",
            read_paths=[manifest_rel, "content/**"],
            write_paths=[out_target, json_target, f"{work_rel}/cta.md", f"{work_rel}/cta_fixes/<CID>.py"],
            done_signal=disk_done_signal,
        )

        prompt_lines = [
            "# Asignación de Tarea: Cognitive Task Analysis Architect (C2C v3.21 Load Inversion)",
            "",
            scope_header,
            "",
            "## 1. PARÁMETROS DEL CURRÍCULO",
            f"- **Manifest:** `{manifest_rel}`",
            f"- **CTA Mode:** `{cta_mode}`",
            f"- **Granularity:** `{granularity}`",
            f"- **Total Physical Pages:** {total_physical_pages}",
            f"- **Archivo Python de Salida:** `{out_target}`",
            f"- **Destino JSON Final:** `{json_target}`",
        ]
        if delta_block:
            prompt_lines.append(delta_block)

        prompt_lines.extend([
            "",
            "## 2. DOCUMENTOS ASIGNADOS Y RANGOS DE PÁGINAS FÍSICAS (1..N)",
            doc_table_str,
            "",
            "> [!CRITICAL]",
            "> **REGLA MANDATORIA DE PAGINACIÓN `evidence.page`:**",
            "> SIEMPRE usa el índice de página 1-indexed del archivo PDF (`1..N` según la tabla anterior), NUNCA la numeración impresa del libro o capítulo.",
            "",
            "## 3. DIRECTIVAS DE OPERACIÓN",
            f"1. Lee el material fuente asignado con `read_file` y escribe `COMPETENCIES = [...]` (tuplas de 11 elementos —11.º obligatorio `recommended_modalities` con 2..4 modalidades canónicas—, `CTA_CONTRACT_VERSION = 2`) en `{out_target}`.",
            f"2. Compila deterministamente: `{compile_cmd}`",
            f"3. Con < 6 errores (1..5 errores), corrige con edit_file (replace_file_content) sobre `{out_target}` (PROHIBIDO write_file completo cuando hay < 6 errores); con >= 6 errores, usa cta_fixes/<CID>.py (1-2 comps) o write_file(Overwrite=True).",
            f"4. Cierre al aprobar: `{json_target}` (señal terminal DONE).",
        ])
        prompt_full = "\n".join(prompt_lines)

        prompt_sha256 = hashlib.sha256(prompt_full.encode("utf-8")).hexdigest()
        item_file = items_dir / "cta_01.json"
        work_order_meta = {
            "role": "Cognitive Task Analysis Architect",
            "output_python": out_target,
            "output_json": json_target,
            "compile_cmd": compile_cmd,
            "compile_command": compile_cmd,
            "prompt_sha256": prompt_sha256,
        }
        item_data = {
            "TypeName": "c2c_cta_architect",
            "Role": "Cognitive Task Analysis Architect",
            "Model": "inherit",
            "Workspace": "inherit",
            "Prompt": prompt_full,
            "work_order": work_order_meta,
            "output_python": out_target,
            "output_json": json_target,
            "compile_command": compile_cmd,
        }
        if delta_info:
            item_data["delta_context"] = {
                "next_ids_by_prefix": next_ids_by_prefix,
                "existing_competencies_outline": existing_comps_outline,
            }
        item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")

        if use_pointer:
            w_abs = item_file.resolve().as_posix()
            first_doc = doc_rows[0][1] if doc_rows else "content/**"
            abs_first_doc = _resolve_posix_path(work, work_rel, first_doc)
            abs_out_target = _resolve_posix_path(work, work_rel, out_target)
            extra = f"[SCOPE-LOCK] READ: `{w_abs}`, `{abs_first_doc}`; WRITE: `{abs_out_target}`; COMPILE: `.agents/skills/content-to-course/compile_cta.py`."
            if delta_info:
                cand_extra = extra + f" Delta: {next_ids_by_prefix}."
                if len(make_pointer_prompt(role_name="Cognitive Task Analysis Architect", work_order_rel=w_abs, done_signal=f"DONE: {json_target}", extra_instructions=cand_extra).encode("utf-8")) <= 650:
                    extra = cand_extra
            pointer_prompt = make_pointer_prompt(
                role_name="Cognitive Task Analysis Architect",
                work_order_rel=w_abs,
                done_signal=f"DONE: {json_target}",
                extra_instructions=extra,
            )
            if len(pointer_prompt.encode("utf-8")) > 650:
                extra = f"[SCOPE-LOCK] READ: `{w_abs}`; WRITE: `{abs_out_target}`; COMPILE: `.agents/skills/content-to-course/compile_cta.py`."
                pointer_prompt = make_pointer_prompt(
                    role_name="Cognitive Task Analysis Architect",
                    work_order_rel=w_abs,
                    done_signal=f"DONE: {json_target}",
                    extra_instructions=extra,
                )
            subagents = [{
                "TypeName": "c2c_cta_architect",
                "Role": "Cognitive Task Analysis Architect",
                "Model": "inherit",
                "Prompt": pointer_prompt,
            }]
        else:
            inline_data = dict(item_data)
            inline_data["Prompt"] = prompt_full.replace(disk_done_signal, f"DONE: {json_target}")
            subagents = [inline_data]
        item_files = [item_file.resolve().as_posix()]

    dispatch_dir = work / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    cta_audit_file = dispatch_dir / "cta.json"
    dispatched_at = datetime.now(timezone.utc).isoformat()
    cta_audit = {
        "stage": "cta",
        "cta_mode": cta_mode,
        "dispatched_at": dispatched_at,
        "subagents_count": len(subagents),
        "item_files": item_files,
        "Subagents": subagents,
    }
    cta_audit_file.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_text(cta_audit_file, json.dumps(cta_audit, indent=2, ensure_ascii=False))

    cta_orders_file = dispatch_dir / "cta_work_orders.json"
    _atomic_write_text(cta_orders_file, json.dumps(cta_audit, indent=2, ensure_ascii=False))

    snap = snapshot_work_dir(work)
    snap_json = json.dumps({k: list(v) for k, v in snap.items()}, indent=2, ensure_ascii=False)
    _atomic_write_text(dispatch_dir / "cta_snapshot.json", snap_json)
    if cta_mode == "mapreduce":
        _atomic_write_text(dispatch_dir / "cta-map_snapshot.json", snap_json)
    else:
        _atomic_write_text(dispatch_dir / "cta-direct_snapshot.json", snap_json)

    return {"dispatched_at": dispatched_at, "Subagents": subagents, "item_files": item_files}


def dispatch_cta_reduce(
    work_dir: Union[str, Path],
    pointer: bool = True,
) -> Dict[str, Any]:
    """Generates dispatch payload and individual item file for CTA Harmonizer (MapReduce Harmonization v3.21).

    Supports Pointer Mode by writing work/dispatch/items/cta_reduce_01.json and ensuring
    work/dispatch/types/c2c_cta_harmonizer.json, using TypeName: 'c2c_cta_harmonizer'.
    Instructs semantic deduplication over all work/cta_outline.json, base node absorption
    ([BASE], read_only_base: true) in delta mode (--append), and DAG closure using add_prerequisites
    to ensure connected_components == 1 and root_ratio <= 0.20, emitting duplicate_decisions
    and add_prerequisites in work/cta_harmonize.json.
    """
    work = Path(work_dir).resolve()
    work_rel = get_work_rel(work)
    use_pointer = pointer if pointer is not None else (os.getenv("C2C_POINTER_PROMPTS", "1").lower() in ("1", "true", "yes"))

    dispatch_dir = work / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    items_dir = dispatch_dir / "items"
    items_dir.mkdir(parents=True, exist_ok=True)
    types_dir = dispatch_dir / "types"
    types_dir.mkdir(parents=True, exist_ok=True)

    # Ensure c2c_cta_harmonizer type spec
    h_type_file = types_dir / "c2c_cta_harmonizer.json"
    if not h_type_file.is_file():
        try:
            harmonizer_prompt = load_system_prompt("prompt_cta_harmonizer.md", lean=True)
            harmonizer_spec = {
                "name": "c2c_cta_harmonizer",
                "description": "Cognitive Task Analysis Harmonizer for deduplicating and merging sectional CTA parts",
                "system_prompt": harmonizer_prompt,
                "enable_write_tools": True,
                "enable_subagent_tools": False,
                "enable_mcp_tools": False,
            }
            h_type_file.write_text(json.dumps(harmonizer_spec, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            logger.warning("Could not write c2c_cta_harmonizer.json: %s", e)

    shard_jsons = sorted(list((work / "cta_parts").glob("*.json")) + list((work / "cta").glob("cta_shard_*.json")))
    shard_json_rel_list = [f"{work_rel}/{p.relative_to(work).as_posix()}" for p in shard_jsons] if shard_jsons else [f"{work_rel}/cta_parts/*.json"]
    shard_json_lines = "\n".join(f"- `{p}`" for p in shard_json_rel_list)

    _, _, cmd_prefix = _resolve_repo_python_and_env()
    compile_cmd = f"{cmd_prefix} .agents/skills/content-to-course/cta_merge.py apply --work \"{work.resolve().as_posix()}\""

    delta_file = work / "delta_manifest.json"
    delta_note = ""
    if delta_file.is_file():
        delta_note = (
            "\n> [!NOTE]\n"
            "> **MODO DELTA (--append) ACTIVO:** Existen competencias base marcadas como `read_only_base: true` o prefijo `[BASE]`. "
            "Si una competencia nueva duplica una base, absórbela hacia el nodo base preexistente para evitar redundancia.\n"
        )

    disk_done_signal = f"Cierre al aprobar: {work_rel}/cta.json (señal terminal DONE)"
    scope_header = build_scope_header(
        role="cta-reduce",
        read_paths=[f"{work_rel}/cta_outline.json", f"{work_rel}/duplicate_candidates.json"],
        write_paths=[f"{work_rel}/cta_harmonize.json", f"{work_rel}/cta.json", f"{work_rel}/cta.md"],
        done_signal=disk_done_signal,
    )

    prompt_text = (
        f"# Asignación de Tarea: CTA Harmonizer (MapReduce Harmonization v4.1)\n\n"
        f"{scope_header}\n\n"
        f"- **Insumos:** `{work_rel}/cta_outline.json`, `{work_rel}/duplicate_candidates.json`\n"
        f"- **Salida JSON:** `{work_rel}/cta_harmonize.json` (`duplicate_decisions` [`keep_id`/`drop_id`], `add_prerequisites`, `rename`, `drop_duplicate_distractors`)\n"
        f"- **Invariantes DAG:** `connected_components == 1`, `root_ratio <= 0.20`\n"
        f"{delta_note}"
        f"- **Merge:** `{compile_cmd}`\n"
        f"- **Cierre al aprobar:** `{work_rel}/cta.json` (señal terminal DONE)\n"
    )

    prompt_sha256 = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()
    item_file = items_dir / "cta_reduce_01.json"
    work_order_meta = {
        "role": "CTA Harmonizer",
        "output_json": f"{work_rel}/cta.json",
        "compile_cmd": compile_cmd,
        "compile_command": compile_cmd,
        "prompt_sha256": prompt_sha256,
    }
    item_data = {
        "TypeName": "c2c_cta_harmonizer",
        "Role": "CTA Harmonizer",
        "Model": "inherit",
        "Prompt": prompt_text,
        "work_order": work_order_meta,
        "output_json": f"{work_rel}/cta.json",
        "compile_command": compile_cmd,
    }
    item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")

    # Also keep cta_harmonize_01.json for backward compatibility
    compat_item_file = items_dir / "cta_harmonize_01.json"
    compat_item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")

    if use_pointer:
        pointer_prompt = (
            f"You are CTA Harmonizer. [SCOPE-LOCK] "
            f"READ: `{work_rel}/cta_outline.json`, `{work_rel}/duplicate_candidates.json` (do NOT read `{item_file.name}`). "
            f"WRITE: `{work_rel}/cta_harmonize.json`, `{work_rel}/cta.json`. "
            f"RUN: `{compile_cmd}`. "
            f"DONE: `{work_rel}/cta.json`."
        )
        subagents = [{
            "TypeName": "c2c_cta_harmonizer",
            "Role": "CTA Harmonizer",
            "Model": "inherit",
            "Prompt": pointer_prompt,
        }]
    else:
        inline_data = dict(item_data)
        inline_data["Prompt"] = prompt_text.replace(disk_done_signal, f"DONE: {work_rel}/cta.json").replace(
            f"Cierre al aprobar: `{work_rel}/cta.json` (señal terminal DONE).",
            f"DONE: {work_rel}/cta.json",
        )
        subagents = [inline_data]

    item_files = [item_file.resolve().as_posix()]

    audit_file = dispatch_dir / "cta_reduce.json"
    dispatched_at = datetime.now(timezone.utc).isoformat()
    audit_data = {
        "stage": "cta-reduce",
        "dispatched_at": dispatched_at,
        "subagents_count": len(subagents),
        "item_files": item_files,
        "Subagents": subagents,
    }
    _atomic_write_text(audit_file, json.dumps(audit_data, indent=2, ensure_ascii=False))

    snap = snapshot_work_dir(work)
    snap_json = json.dumps({k: list(v) for k, v in snap.items()}, indent=2, ensure_ascii=False)
    _atomic_write_text(dispatch_dir / "cta-reduce_snapshot.json", snap_json)

    return {"dispatched_at": dispatched_at, "Subagents": subagents, "item_files": item_files}


def dispatch_authors(
    work_dir: Union[str, Path],
    pointer: bool = True,
    wave_index: Optional[int] = None,
    ids: Optional[Union[str, List[Union[str, int]]]] = None,
) -> Dict[str, Any]:
    """Generates dispatch payload and individual item files for Shard Authors (Load Inversion v3.21).
    
    Exige work/shards/pre_shard_manifest.json y work/pre_cta_manifest.json (cero fallbacks).
    NO pre-siembra JSON en work/templates/ ni bundles en work/shards/bundles/.
    Inyecta especificación Turn-0 completa de competencias y 6 distractores (D-XX-01..06)
    directamente en el prompt conciso del autor, permitiendo autoría autónoma sin lectura de cta.json.
    When pointer=True (default), generates ultra-compact (~350-500 B) pointer prompts in the ready-made Subagents array,
    ordered heaviest unit first (Swift-Dispatch SLA).
    """
    work = Path(work_dir).resolve()
    work_rel = get_work_rel(work)
    use_pointer = pointer if pointer is not None else (os.getenv("C2C_POINTER_PROMPTS", "1").lower() in ("1", "true", "yes"))

    shard_manifest_path = work / "shards" / "pre_shard_manifest.json"
    if not shard_manifest_path.is_file():
        if (work / "pre_shard_manifest.json").is_file():
            shard_manifest_path = work / "pre_shard_manifest.json"
        else:
            err_msg = "BLOCKER:: No existe pre_shard_manifest.json"
            logger.error(err_msg)
            raise FileNotFoundError(err_msg)

    cta_manifest_path = work / "pre_cta_manifest.json"
    if not cta_manifest_path.is_file():
        if (work / "ingestion_manifest.json").is_file():
            cta_manifest_path = work / "ingestion_manifest.json"
        elif not (work / "cta.json").is_file():
            err_msg = "BLOCKER:: No existe pre_cta_manifest.json"
            logger.error(err_msg)
            raise FileNotFoundError(err_msg)

    shard_manifest_rel = (
        f"{work_rel}/shards/pre_shard_manifest.json"
        if (work / "shards" / "pre_shard_manifest.json").is_file()
        else f"{work_rel}/pre_shard_manifest.json"
    )
    manifest_rel = shard_manifest_rel
    cta_rel = f"{work_rel}/cta.json"

    cta_file = work / "cta.json"
    cta_comps_by_id: Dict[str, Dict[str, Any]] = {}
    cta_contract_version = 1
    if cta_file.is_file():
        try:
            cta_data = json.loads(cta_file.read_text(encoding="utf-8"))
            if isinstance(cta_data, dict):
                cta_contract_version = int(cta_data.get("contract_version", cta_data.get("CTA_CONTRACT_VERSION", 1)))
            raw_comps = cta_data.get("competencies", []) if isinstance(cta_data, dict) else (cta_data if isinstance(cta_data, list) else [])
            if isinstance(raw_comps, list):
                for c in raw_comps:
                    if isinstance(c, dict) and "id" in c:
                        cta_comps_by_id[c["id"]] = c
            elif isinstance(raw_comps, dict):
                for cid, c in raw_comps.items():
                    if isinstance(c, dict):
                        c_copy = dict(c)
                        c_copy.setdefault("id", cid)
                        cta_comps_by_id[cid] = c_copy
        except Exception as e:
            logger.warning("Could not read cta.json: %s", e)

    # Document map from pre_cta_manifest
    cta_manifest_data: Dict[str, Any] = {}
    if cta_manifest_path.is_file():
        try:
            cta_manifest_data = json.loads(cta_manifest_path.read_text(encoding="utf-8"))
        except Exception:
            pass
    doc_paths_by_name: Dict[str, str] = {}
    docs = cta_manifest_data.get("documents", [])
    if isinstance(docs, list):
        for d in docs:
            if isinstance(d, dict):
                dn = _clean_str(d.get("doc_name") or d.get("name") or d.get("doc"))
                dp = _clean_str(d.get("path") or d.get("file") or dn)
                if dp:
                    dp = dp.replace("\\", "/")
                if dn:
                    doc_paths_by_name[dn] = dp
    elif isinstance(docs, dict):
        for dn, dinfo in docs.items():
            if isinstance(dinfo, dict):
                dp = _clean_str(dinfo.get("path") or dn)
                if dp:
                    dp = dp.replace("\\", "/")
                doc_paths_by_name[dn] = dp

    shard_manifest_data = json.loads(shard_manifest_path.read_text(encoding="utf-8"))
    eff_tpl_per_mod = max(
        1,
        int(
            (shard_manifest_data.get("stage4_contract") or {}).get("templates_per_modality")
            or shard_manifest_data.get("templates_per_modality")
            or DEFAULT_TEMPLATES_PER_MODALITY
        ),
    )
    manifest_dirty = False
    if isinstance(shard_manifest_data, dict):
        if "min_archetypes" not in shard_manifest_data or shard_manifest_data.get("min_archetypes") != 4:
            shard_manifest_data["min_archetypes"] = 4
            manifest_dirty = True
        raw_shards = shard_manifest_data.get("shards")
        if isinstance(raw_shards, list):
            for s_item in raw_shards:
                if isinstance(s_item, dict) and s_item.get("min_archetypes") != 4:
                    s_item["min_archetypes"] = 4
                    manifest_dirty = True
        elif isinstance(raw_shards, dict):
            for s_key, s_val in raw_shards.items():
                if isinstance(s_val, dict) and s_val.get("min_archetypes") != 4:
                    s_val["min_archetypes"] = 4
                    manifest_dirty = True
        if manifest_dirty:
            try:
                shard_manifest_path.write_text(
                    json.dumps(shard_manifest_data, indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
            except Exception as e:
                logger.warning("Could not persist min_archetypes to %s: %s", shard_manifest_path, e)

    manifest_comps_by_id: Dict[str, Dict[str, Any]] = {}
    shards_raw = shard_manifest_data.get("shards", [])
    if isinstance(shards_raw, dict):
        shard_list = []
        for k, v in shards_raw.items():
            if isinstance(v, dict):
                entry = dict(v)
                entry.setdefault("shard_id", k)
                shard_list.append(entry)
                for c in entry.get("competencies", []):
                    if isinstance(c, dict) and "id" in c:
                        manifest_comps_by_id[c["id"]] = c
            elif isinstance(v, list):
                shard_list.append({"shard_id": k, "competency_ids": v})
            else:
                shard_list.append({"shard_id": k, "competency_ids": [v] if v else []})
    elif isinstance(shards_raw, list):
        shard_list = shards_raw
        for s_item in shard_list:
            if isinstance(s_item, dict):
                for c in s_item.get("competencies", []):
                    if isinstance(c, dict) and "id" in c:
                        manifest_comps_by_id[c["id"]] = c
    else:
        shard_list = []

    # Filter by wave_index if specified
    if wave_index is not None:
        shard_list = [s for s in shard_list if s.get("wave_index") == wave_index]

    if ids is not None:
        ids_set = {str(i) for i in ([ids] if isinstance(ids, (str, int)) else ids)}
        shard_list = [
            s for s in shard_list
            if str(s.get("shard_id")) in ids_set or any(str(cid) in ids_set for cid in (s.get("competency_ids") or []))
        ]

    _MC7_MOD_ALIASES = {"mc7", "mc_7", "mc", "multiple_choice", "multiple-choice", "multiple_choice_7_options", "single_choice"}

    # Swift-Dispatch SLA: Sort shards heaviest unit first
    def _shard_weight(shard: Dict[str, Any]) -> int:
        if shard.get("estimated_questions"):
            return int(shard["estimated_questions"]) * 10
        c_ids = shard.get("competency_ids") or []
        if not c_ids and "competencies" in shard:
            raw_c = shard["competencies"]
            c_ids = [c["id"] if isinstance(c, dict) and "id" in c else str(c) for c in raw_c]
        w = 0
        for cid in c_ids:
            c_obj = cta_comps_by_id.get(cid) or manifest_comps_by_id.get(cid, {})
            t = str(c_obj.get("type", "knowledge")).lower()
            rec_m = c_obj.get("recommended_modalities") or []
            norm_m = list(dict.fromkeys(str(m).strip().lower() for m in rec_m if str(m).strip()))
            n_m = len(norm_m)
            has_mc7_m = any(m in _MC7_MOD_ALIASES for m in norm_m) and not (is_skill_type(t) or str(cid).startswith("Hab-"))
            n_t = required_templates_for_competency(n_m, eff_tpl_per_mod, has_mc7=has_mc7_m)
            w += quota_for_competency(t, n_t)
        return w if w > 0 else (len(c_ids) * 20)

    shard_list = sorted(shard_list, key=_shard_weight, reverse=True)

    items_dir = work / "dispatch" / "items"
    items_dir.mkdir(parents=True, exist_ok=True)
    if ids is None and wave_index is None:
        for old_af in items_dir.glob("author_*.json"):
            try:
                old_af.unlink()
            except Exception:
                pass

    _, _, cmd_prefix = _resolve_repo_python_and_env()

    subagents: List[Dict[str, Any]] = []
    item_files: List[str] = []
    used_author_filenames: Set[str] = set()

    for idx, s in enumerate(shard_list, start=1):
        s_idx = s.get("shard_index") or idx
        s_id = s.get("shard_id") or f"shard_{s_idx:02d}"
        c_ids = s.get("competency_ids") or []
        if not c_ids and "competencies" in s:
            raw_c = s["competencies"]
            c_ids = [c["id"] if isinstance(c, dict) and "id" in c else str(c) for c in raw_c]

        out_py = f"{work_rel}/shards/{s_id}_data.py"
        target_json = f"{work_rel}/shards/{s_id}.json"

        # Structured Turn-0 specification for each assigned competency
        comp_blocks = []
        source_doc_set: Set[str] = set()
        missing_assumptions_cids: List[str] = []

        for cid in c_ids:
            c_obj = cta_comps_by_id.get(cid) or manifest_comps_by_id.get(cid, {})
            c_name = _clean_str(c_obj.get("name")) or cid
            raw_type = str(c_obj.get("type", "knowledge")).lower()
            raw_rec_mods = c_obj.get("recommended_modalities") or []
            norm_rec_mods = list(dict.fromkeys(str(m).strip().lower() for m in raw_rec_mods if str(m).strip()))
            num_mods = len(norm_rec_mods)
            has_mc7_comp = any(m in _MC7_MOD_ALIASES for m in norm_rec_mods) and not (is_skill_type(raw_type) or str(cid).startswith("Hab-"))
            _s4c = (s.get("stage4_contract") or {}).get(cid) or competency_contract(
                raw_type,
                num_modalities=num_mods,
                templates_per_modality=eff_tpl_per_mod,
                has_mc7=has_mc7_comp,
            )
            comp_k = max(1, int(_s4c.get("templates_per_modality") or eff_tpl_per_mod))
            min_tpls = int(
                _s4c.get("min_templates_required")
                or required_templates_for_competency(num_mods, comp_k, _s4c.get("min_archetypes", 4), has_mc7=has_mc7_comp)
            )
            quota = int(_s4c["quota"])
            comp_type = "skill" if is_skill_type(raw_type) else "knowledge"
            req_uniq = int(_s4c["required_unique_stems"])
            per_tpl = -(-req_uniq // max(1, min_tpls))

            desc_latex = _clean_str(c_obj.get("description_latex") or c_obj.get("description")) or "(Definición pedagógica según fuentes del curso)"

            # Evidence
            ev_list = []
            raw_ev = c_obj.get("evidence", [])
            if isinstance(raw_ev, dict):
                raw_ev = [raw_ev]
            if isinstance(raw_ev, list):
                for ev in raw_ev:
                    if isinstance(ev, dict):
                        doc = _clean_str(ev.get("doc") or ev.get("document"))
                        sec = _clean_str(ev.get("section_heading") or ev.get("section"))
                        page = ev.get("page") or ev.get("page_or_slide") or ev.get("slide") or 1
                        raw_resolved = doc_paths_by_name.get(doc, doc) if doc else ""
                        resolved_doc = raw_resolved.replace("\\", "/") if raw_resolved else ""
                        if resolved_doc:
                            source_doc_set.add(resolved_doc)
                        ev_desc = f"`{resolved_doc or doc}` (pág. {page}" + (f", sección: '{sec}'" if sec else "") + ")"
                        ev_list.append(ev_desc)
            ev_str = "; ".join(ev_list) if ev_list else "Consultar material fuente en `content/`"

            # 6 Distractors D-XX-01..06
            raw_distractors = c_obj.get("distractors", [])
            d_lines = []
            correct_belief = _clean_str(c_obj.get("correct_belief") or c_obj.get("canonical_formula"))
            if not correct_belief and isinstance(raw_distractors, list) and raw_distractors:
                first_d = raw_distractors[0]
                if isinstance(first_d, dict):
                    correct_belief = _clean_str(first_d.get("correct_belief"))

            if isinstance(raw_distractors, list):
                for d in raw_distractors:
                    if isinstance(d, dict):
                        did = _clean_str(d.get("id")) or "D-XX"
                        dname = _clean_str(d.get("name")) or did
                        dw = _clean_str(d.get("wrong_belief") or d.get("rationale")) or "Creencia errónea no especificada"
                        d_omit = _clean_str(d.get("omitted_step")) or "N/A"
                        d_manif = _clean_str(d.get("manifestation"))
                        d_hint = _clean_str(d.get("remediation_hint"))
                        d_warn = _clean_str(d.get("common_misconception_warning"))
                        line_entry = f"    - **`{did}`** (`{dname}`): Creencia errónea: *\"{dw}\"* | Paso omitido: `{d_omit}`"
                        if d_manif:
                            line_entry += f" | Manifestación: *\"{d_manif}\"*"
                        if d_hint:
                            line_entry += f" | Remediation Hint: *\"{d_hint}\"*"
                        if d_warn:
                            line_entry += f" | Advertencia: *\"{d_warn}\"*"
                        d_lines.append(line_entry)
            if not d_lines:
                d_lines.append("    - *(Distractores no provistos en manifiesto; sintetizar 6 distractores canónicos D-XX-01..06)*")
            distractors_block = "\n".join(d_lines)

            # Assumptions A-XX-YY (mandatory binding for Archetype 4 boundary_or_edge_case)
            raw_assumptions = c_obj.get("assumptions", [])
            a_lines = []
            if isinstance(raw_assumptions, list):
                for a in raw_assumptions:
                    if isinstance(a, dict):
                        aid = _clean_str(a.get("id")) or "A-XX"
                        astmt = _clean_str(a.get("statement_latex") or a.get("statement") or a.get("description")) or "Supuesto no especificado"
                        aconseq = _clean_str(a.get("violation_consequence") or a.get("consequence")) or "Consecuencia no especificada"
                        a_lines.append(f"    - **`{aid}`**: Enunciado: *\"{astmt}\"* | Consecuencia de violación: *\"{aconseq}\"*")
            if not a_lines:
                a_lines.append("    - *(Supuestos no provistos en manifiesto; Arquetipo 4 boundary_or_edge_case debe explorar supuestos o condiciones límite del modelo)*")
            assumptions_block = "\n".join(a_lines)

            # Warning when assumptions are empty in cta.json for contract_version >= 2 or concept/skill
            has_assumptions = bool(isinstance(raw_assumptions, list) and len(raw_assumptions) > 0)
            is_concept_or_skill = raw_type in ("concept", "skill") or is_skill_type(raw_type) or comp_type in ("concept", "skill")
            if not has_assumptions and (cta_contract_version >= 2 or is_concept_or_skill):
                missing_assumptions_cids.append(cid)
                warn_msg = (
                    f"[WARNING] dispatch_authors: Ausencia de A-ids (assumptions=[]) en cta.json para competencia '{cid}' "
                    f"(tipo: '{raw_type}', contract_version: {cta_contract_version})."
                )
                print(warn_msg, file=sys.stderr)
                logger.warning(warn_msg)

            cb_line = f"- **Modelo/Fórmula Correcta Canónica (correct_belief):** {correct_belief}\n" if correct_belief else ""
            if raw_rec_mods:
                if has_mc7_comp and comp_k >= 2:
                    mod_floor_desc = (
                        f"M={num_mods}, exactamente 1 plantilla MC7 [tope M20-MC7-CAP <= 1] y >= {comp_k} plantillas distintas por cada modalidad activa [>= 80% activo M20-ACTIVE-QUOTA] => mínimo {min_tpls} plantillas"
                    )
                else:
                    mod_floor_desc = (
                        f"M={num_mods}, obligatorio >= {comp_k} plantillas distintas por modalidad => mínimo {min_tpls} plantillas"
                    )
                rec_mods_line = f"- **Modalidades decididas por CTA Architect ({mod_floor_desc}):** {', '.join(str(m) for m in raw_rec_mods)}\n"
            else:
                rec_mods_line = f"- **Modalidades decididas por CTA Architect (mínimo {min_tpls} plantillas):** Libre criterio epistémico dentro de modalidades válidas del contrato (sin cuotas rígidas por tipo).\n"
            tpl_distrib_note = (
                f"1 MC7 + >={comp_k}/modalidad activa" if (has_mc7_comp and comp_k >= 2) else f"{comp_k}/modalidad"
            )
            block = (
                f"### Competencia: `{cid}`\n"
                f"- **Tipo:** `{comp_type}` (Cuota requerida: **{quota}** reactivos)\n"
                f"{rec_mods_line}"
                f"- **Umbrales Stage 4 (contrato exacto, se auditan al construir):** cuota **{quota}**; "
                f"mínimo **{min_tpls} plantillas** ({tpl_distrib_note}, >= {_s4c['min_archetypes']} arquetipos); "
                f"**>= {req_uniq} stems únicos** tras enmascarar números (>= {per_tpl} `stems` distintos por plantilla); "
                f"ratio de diversidad >= {_s4c['min_diversity_ratio']:.2f}\n"
                f"- **Nombre:** {c_name}\n"
                f"- **Descripción (LaTeX):** {desc_latex}\n"
                f"{cb_line}"
                f"- **Evidencia Fuente:** {ev_str}\n"
                f"- **Supuestos Epistémicos (Assumptions A-XX-YY; obligatorio vincular en Arquetipo 4 con `assumption_id=\"<id>\"`):**\n"
                f"{assumptions_block}\n"
                f"- **6 Distractores Canónicos (D-XX-01..06):**\n"
                f"{distractors_block}"
            )
            comp_blocks.append(block)

        source_doc_list = sorted(source_doc_set) if source_doc_set else ["content/**"]
        disk_done_signal = f"Cierre al aprobar: {target_json} (señal terminal DONE)"
        scope_header = build_scope_header(
            role="author",
            read_paths=source_doc_list,
            write_paths=[out_py, target_json, f"{work_rel}/shards/shard_fixes/<CID>.py"],
            forbidden_paths=[
                "tests/**",
                ".agents/skills/content-to-course/compile_shard.py",
                "scratch/**",
                "work/scratch/**",
                "engine/*",
                "SKILL.md",
                ".check_attempts/**",
                ".agents/skills/content-to-course/check_templates.py",
                ".agents/skills/content-to-course/check_cta.py",
                "src/validator/**",
            ],
            done_signal=disk_done_signal,
        )

        compile_cmd = f"{cmd_prefix} -u .agents/skills/content-to-course/compile_shard.py --input {out_py} --output {target_json} --work {work_rel} --shard {s_id} --strict --min-archetypes 4 --templates-per-modality {eff_tpl_per_mod} --fail-total"

        prompt_lines = [
            f"# Asignación de Tarea: Shard Exercise Author `{s_id}` (C2C v3.21 Load Inversion)",
            "",
            scope_header,
            "",
            "## 1. ESPECIFICACIÓN DEL SHARD",
            f"- **Shard ID:** `{s_id}`",
            f"- **Manifest:** `{work_rel}/shards/pre_shard_manifest.json`",
            f"- **Archivo Python de Salida:** `{out_py}`",
            f"- **Destino JSON Final:** `{target_json}`",
            f"- **Documentos Fuente Asignados:**",
        ]
        for sdoc in source_doc_list:
            prompt_lines.append(f"  - `{sdoc}`")
        _n_head = len(prompt_lines)

        prompt_lines.extend([
            "",
            "## 2. ESPECIFICACIÓN TURN-0 COMPLETA DE COMPETENCIAS Y DISTRACTORES",
            "\n\n".join(comp_blocks),
            "",
            "## 3. INSTRUCCIONES DE EJECUCIÓN",
            f"1. **AUTOSUFICIENCIA TURN-0 (CERO LECTURA INNECESARIA DE PDFs):** La Sección 2 contiene el 100% de competencias y distractores; NO abras ni leas los documentos fuente de content/ en Turno 1 y empieza directamente escribiendo {s_id}_data.py (`{out_py}`, <= 80-110 líneas por competencia, <= 180-220 líneas totales por shard).",
            f"2. **Contrato Form-C (`min_archetypes = 4`, `[M3-ARCHETYPES]`, `K={eff_tpl_per_mod}`/modalidad activa, `[M20-MC7-CAP]`, `[M20-ACTIVE-QUOTA]`):** Define el mínimo requerido de tuplas distintas en `TEMPLATES` por competencia (al menos `{eff_tpl_per_mod}` plantillas no-clon por cada modalidad activa en `'Modalidades decididas por CTA Architect'`; `0 MC7` en `Skill`, y `<= 1 MC7` en `Concept`/`Fact` —candados `[TPL-CLONE-AST]`, `[TPL-CLONE-BAND]`, `[TPL-CLONE-STEM]`, `[TPL-CLONE-SYMPY]`—) en bandas `'easy'`, `'medium'`, `'hard'` según tu SystemPrompt (`[TPL-DYNAMIC-RATIONALE]`, `[KATEX-TEXT-PROSE]`/`[KATEX-PROSE-OVERFLOW]`, FIB sin `$`).",
            f"3. **Compilación determinista:** `{compile_cmd}`",
            f"4. **Reparación (Matriz 2D):** Con < 6 errores (1..5 errores) usa `edit_file` quirúrgico (en >= 300 líneas NO reescribas todo el archivo desde cero con `write_file`); con >= 6 errores usa `{work_rel}/shards/shard_fixes/<CID>.py`.",
            f"5. **[Corte Inmediato Post-PASS]:** Cierre al aprobar: `{target_json}` (señal terminal DONE).",
        ])
        prompt_full = "\n".join(prompt_lines)

        prompt_sha256 = hashlib.sha256(prompt_full.encode("utf-8")).hexdigest()
        m_exact_shard = re.fullmatch(r"shard_(\d+)", str(s_id))
        safe_s_id = re.sub(r"[^\w-]", "_", str(s_id)).strip("_") or f"{idx:02d}"
        if m_exact_shard:
            candidate_name = f"author_{int(m_exact_shard.group(1)):02d}.json"
        else:
            candidate_name = f"author_{safe_s_id}.json"
        if candidate_name in used_author_filenames:
            candidate_name = f"author_{safe_s_id}_{idx:02d}.json"
        used_author_filenames.add(candidate_name)
        item_file = items_dir / candidate_name
        work_order_meta = {
            "role": f"Shard Author {s_id}",
            "shard_id": s_id,
            "assigned_competencies": c_ids,
            "output_python": out_py,
            "output_json": target_json,
            "compile_cmd": compile_cmd,
            "compile_command": compile_cmd,
            "min_archetypes": 4,
            "templates_per_modality": eff_tpl_per_mod,
            "prompt_sha256": prompt_sha256,
        }
        if missing_assumptions_cids:
            work_order_meta["missing_assumptions"] = missing_assumptions_cids
        item_data = {
            "TypeName": "c2c_shard_author",
            "Role": f"Shard Author {s_id}",
            "Model": "inherit",
            "Workspace": "inherit",
            "shard_id": s_id,
            "assigned_competencies": c_ids,
            "output_python": out_py,
            "output_json": target_json,
            "compile_command": compile_cmd,
            "compile_cmd": compile_cmd,
            "min_archetypes": 4,
            "templates_per_modality": eff_tpl_per_mod,
            "Prompt": prompt_full,
            "work_order": work_order_meta,
        }
        item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")

        # Pure-data payload file for live Shard Author (zero wrapper bloat)
        data_filename = f"{item_file.stem}_data.md"
        data_file = items_dir / data_filename
        author_data_md = (
            f"# Shard `{s_id}`\n\n"
            f"## 1. METADATOS DEL SHARD\n"
            f"- **work_dir:** `{work_rel}`\n"
            f"- **shard_id:** `{s_id}`\n"
            f"- **output_python:** `{out_py}`\n"
            f"- **output_json:** `{target_json}`\n"
            f"- **templates_per_modality:** `{eff_tpl_per_mod}`\n"
            f"- **compile_command:** `{compile_cmd}`\n\n"
            f"## 2. ESPECIFICACIÓN TURN-0 COMPLETA DE COMPETENCIAS Y DISTRACTORES\n"
            + "\n\n".join(comp_blocks)
            + "\n"
        )
        data_file.write_text(author_data_md, encoding="utf-8")

        if use_pointer:
            data_abs = data_file.resolve().as_posix()
            out_py_abs = _resolve_posix_path(work, work_rel, out_py)
            extra = f"[SCOPE-LOCK] READ: `{data_abs}` (not `{item_file.name}`); WRITE: `{out_py_abs}`; COMPILE: `.agents/skills/content-to-course/compile_shard.py`."
            pointer_prompt = make_pointer_prompt(
                role_name=f"Shard Author {s_id}",
                work_order_rel=data_abs,
                done_signal=f"DONE: {target_json}",
                extra_instructions=extra,
            )
            if len(pointer_prompt.encode("utf-8")) > 650:
                extra = f"[SCOPE-LOCK] READ: `{data_abs}`; WRITE: `{out_py_abs}`; COMPILE: `.agents/skills/content-to-course/compile_shard.py`."
                pointer_prompt = make_pointer_prompt(
                    role_name=f"Shard Author {s_id}",
                    work_order_rel=data_abs,
                    done_signal=f"DONE: {target_json}",
                    extra_instructions=extra,
                )
            subagent_item = {
                "TypeName": "c2c_shard_author",
                "Role": f"Shard Author {s_id}",
                "Model": "inherit",
                "Prompt": pointer_prompt,
            }
            if os.getenv("C2C_INLINE_AUTHOR_ORDER", "0").lower() in ("1", "true", "yes") and len(shard_list) <= 8:
                # Inline Work Order (G): only when explicitly enabled via env and shard_list <= 8 so stdout/turn tokens never overflow.
                inline_lines = list(prompt_lines[:_n_head]) + [
                    "",
                    "## 2. ESPECIFICACIÓN TURN-0 COMPLETA DE COMPETENCIAS Y DISTRACTORES",
                    "\n\n".join(comp_blocks),
                    "",
                    "## 3. EJECUCIÓN",
                    f"- La orden de trabajo completa YA está en este mensaje: PROHIBIDO `read_file` en Turno 1; tu primera acción es `write_file` de `{out_py}` (`TEMPLATES = [...]`, {_S4_VARIANTS_OTHER}+ stems por plantilla, reglas de contrato en tu system prompt).",
                    f"- Compila (run_command con `WaitMsBeforeAsync: 15000`): `{compile_cmd}`",
                    "- Errores: corrige SOLO con la salida del compilador ([PRECHECK] primero, todos juntos). Tras `PASS` no edites más.",
                    f"- Cierre: `DONE: {target_json}`",
                ]
                subagent_item["Prompt"] = "\n".join(inline_lines)
        else:
            inline_data = dict(item_data)
            inline_data["Prompt"] = prompt_full.replace(disk_done_signal, f"DONE: {target_json}").replace(
                f"Cierre al aprobar: `{target_json}` (señal terminal DONE).",
                f"DONE: {target_json}",
            )
            subagent_item = inline_data

        subagents.append(subagent_item)
        item_files.append(item_file.resolve().as_posix())

    dispatch_dir = work / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    authors_audit_file = dispatch_dir / "authors.json"
    dispatched_at = datetime.now(timezone.utc).isoformat()
    authors_audit = {
        "stage": "authors",
        "dispatched_at": dispatched_at,
        "subagents_count": len(subagents),
        "item_files": item_files,
        "Subagents": subagents,
    }
    _atomic_write_text(authors_audit_file, json.dumps(authors_audit, indent=2, ensure_ascii=False))

    # Also write author.json for backward compatibility with run.py
    author_compat_file = dispatch_dir / "author.json"
    _atomic_write_text(author_compat_file, json.dumps(authors_audit, indent=2, ensure_ascii=False))

    # Persist author_snapshot.json prior to return for strict scope auditing
    snap = snapshot_work_dir(work)
    snap_payload = {k: list(v) for k, v in snap.items()}
    snap_json = json.dumps(snap_payload, indent=2, ensure_ascii=False)
    _atomic_write_text(dispatch_dir / "author_snapshot.json", snap_json)
    _atomic_write_text(dispatch_dir / "authors_snapshot.json", snap_json)
    _atomic_write_text(work / "author_snapshot.json", snap_json)
    _atomic_write_text(work / "authors_snapshot.json", snap_json)

    return {"dispatched_at": dispatched_at, "Subagents": subagents, "item_files": item_files}


def dispatch_judges(
    work_dir: Union[str, Path],
    pointer: bool = True,
    max_items_per_judge: int = 20,
    max_judges: int = 10,
    ready_only: bool = False,
    ids: Optional[Union[str, List[Union[str, int]]]] = None,
    samples_per_template: Optional[int] = None,
    overlap_ratio: Optional[float] = None,
    stem_variant_offset: int = 0,
) -> Dict[str, Any]:
    """Generates dispatch payload and individual item files for Blind Judges (Load Inversion v3.21).
    
    Zero-Warmup In-Prompt payload: inyecta los ítems del batch (question_id, question_type, stem_es, options)
    directamente dentro del Prompt sin duplicar el system prompt.
    When pointer=True (default), generates ultra-compact (~200 B) pointer prompts in the ready-made Subagents array,
    enforcing native batch slicing <= 20 items per judge and <= 10 judges total (Swift-Dispatch SLA).
    """
    work = Path(work_dir).resolve()
    work_rel = get_work_rel(work)
    use_pointer = pointer if pointer is not None else (os.getenv("C2C_POINTER_PROMPTS", "1").lower() in ("1", "true", "yes"))

    has_existing_batch = (
        ((work / "verification" / "judge_batch.json").is_file() or (work / "judge_batch.json").is_file())
        and ((work / "verification" / "judge_ground_truth.json").is_file() or (work / "judge_ground_truth.json").is_file())
    )

    def _purge_stale_judge_batches() -> None:
        for pat_dir in (work / "verification", work):
            if pat_dir.is_dir():
                for old_bf in pat_dir.glob("judge_batch_*.json"):
                    if old_bf.name not in ("judge_batch.json", "judge_redispatch_batch.json"):
                        try:
                            old_bf.unlink()
                        except Exception:
                            pass

    if ids or ready_only or not has_existing_batch:
        from judge import (
            DEFAULT_OVERLAP_RATIO,
            DEFAULT_TARGET_TOTAL_EVALUATIONS,
            generate_judge_batch,
            split_judge_batch,
        )
        templates_path = work / "templates"
        if templates_path.is_dir() and any(templates_path.glob("*.json")):
            _purge_stale_judge_batches()
            cta_file = work / "cta.json"
            eff_overlap = DEFAULT_OVERLAP_RATIO if overlap_ratio is None else overlap_ratio
            target_unique: Optional[int] = None
            if (
                samples_per_template is None
                and ids is None
                and max_judges == 10
                and max_items_per_judge == 20
            ):
                target_unique = int(round(DEFAULT_TARGET_TOTAL_EVALUATIONS / (1.0 + eff_overlap)))
            generate_judge_batch(
                templates_path=templates_path,
                work_dir=work,
                cta_path=cta_file if cta_file.is_file() else None,
                ready_only=ready_only,
                max_judges=max_judges,
                max_items_per_judge=max_items_per_judge,
                ids=ids,
                samples_per_template=samples_per_template,
                target_unique_items=target_unique,
                stem_variant_offset=stem_variant_offset,
            )
            split_kwargs: Dict[str, Any] = {
                "max_judges": max_judges,
                "items_per_judge": max_items_per_judge,
            }
            if overlap_ratio is not None:
                split_kwargs["overlap_ratio"] = overlap_ratio
            split_batches = split_judge_batch(work, **split_kwargs)

    # Native Batch Slicing: ensure batches are sliced at <= max_items_per_judge (default 20) and <= max_judges (default 10)
    unsplit = work / "verification" / "judge_batch.json"
    if not unsplit.is_file():
        unsplit = work / "judge_batch.json"

    batch_files = sorted(work.glob("verification/judge_batch_*.json"))
    if not batch_files:
        batch_files = sorted(work.glob("judge_batch_*.json"))
    split_batches = [bf for bf in batch_files if bf.name not in ("judge_batch.json", "judge_redispatch_batch.json")]

    if not split_batches and not unsplit.is_file():
        shards_dir = work / "shards"
        shard_files = list(shards_dir.glob("shard_*.json")) if shards_dir.is_dir() else []
        if shard_files:
            extracted_items = []
            for sf in sorted(shard_files):
                try:
                    s_data = json.loads(sf.read_text(encoding="utf-8"))
                    if isinstance(s_data, list):
                        qs = s_data
                    elif isinstance(s_data, dict):
                        qs = s_data.get("questions") or s_data.get("items") or []
                    else:
                        qs = []
                    for q in qs:
                        if isinstance(q, dict):
                            b_item = {
                                "id": q.get("id") or q.get("question_id"),
                                "question_id": q.get("id") or q.get("question_id"),
                                "competency_id": q.get("competency_id") or "default",
                                "stem": q.get("prompt") or q.get("stem") or q.get("stem_es") or "",
                                "stem_es": q.get("prompt") or q.get("stem_es") or q.get("stem") or "",
                                "options": q.get("options") or q.get("distractors") or [],
                            }
                            extracted_items.append(b_item)
                except Exception as e:
                    logger.warning("Could not extract items from %s: %s", sf, e)
            if extracted_items:
                v_dir = work / "verification"
                v_dir.mkdir(parents=True, exist_ok=True)
                unsplit = v_dir / "judge_batch.json"
                unsplit.write_text(json.dumps(extracted_items, indent=2, ensure_ascii=False), encoding="utf-8")

    needs_split = False
    if not split_batches and unsplit.is_file():
        needs_split = True
    elif split_batches and max_judges > 0 and len(split_batches) > max_judges:
        needs_split = True
    elif split_batches and max_items_per_judge > 0:
        for bf in split_batches:
            try:
                b_raw = json.loads(bf.read_text(encoding="utf-8"))
                b_cnt = len(b_raw.get("items", [])) if isinstance(b_raw, dict) else (len(b_raw) if isinstance(b_raw, list) else 0)
                if b_cnt > max_items_per_judge:
                    needs_split = True
                    break
            except Exception:
                pass

    if needs_split and unsplit.is_file():
        from judge import split_judge_batch
        _purge_stale_judge_batches()
        split_batches = split_judge_batch(work, max_judges=max_judges, items_per_judge=max_items_per_judge)

    if not split_batches and unsplit.is_file():
        split_batches = [unsplit]

    def _load_batch_items(bf: Path) -> List[Dict[str, Any]]:
        try:
            b_data = json.loads(bf.read_text(encoding="utf-8"))
            raw = b_data.get("items", []) if isinstance(b_data, dict) else (b_data if isinstance(b_data, list) else [])
            return [it for it in raw if isinstance(it, dict)]
        except Exception:
            return []

    batch_items_map: Dict[Path, List[Dict[str, Any]]] = {}

    if ids is not None:
        raw_ids = [ids] if isinstance(ids, (str, int)) else list(ids)
        target_ids = {str(x).strip().upper() for x in raw_ids if str(x).strip()}
        if target_ids and split_batches:
            filtered_batches = []
            for bf in split_batches:
                raw_items = _load_batch_items(bf)
                matching = [
                    it for it in raw_items
                    if (
                        str(it.get("competency_id", "")).strip().upper() in target_ids
                        or any(_matches_token(tid, str(it.get("question_id", "")).upper()) for tid in target_ids)
                        or any(_matches_token(tid, str(it.get("id", "")).upper()) for tid in target_ids)
                    )
                ]
                if matching:
                    batch_items_map[bf] = matching
                    filtered_batches.append(bf)
            split_batches = filtered_batches

    if max_judges > 0 and len(split_batches) > max_judges:
        logger.warning(
            "Rebalancing %d judge batches into max_judges=%d without dropping items",
            len(split_batches),
            max_judges,
        )
        target_batches = split_batches[:max_judges]
        for tb in target_batches:
            if tb not in batch_items_map:
                batch_items_map[tb] = _load_batch_items(tb)
        excess_items: List[Dict[str, Any]] = []
        for eb in split_batches[max_judges:]:
            excess_items.extend(batch_items_map.get(eb, _load_batch_items(eb)))
        for idx_ex, ex_item in enumerate(excess_items):
            batch_items_map[target_batches[idx_ex % len(target_batches)]].append(ex_item)
        split_batches = target_batches

    # Swift-Dispatch SLA: Sort batches heaviest unit first
    def _batch_count(bf: Path) -> int:
        if bf in batch_items_map:
            return len(batch_items_map[bf])
        return len(_load_batch_items(bf))

    split_batches = sorted(split_batches, key=_batch_count, reverse=True)

    items_dir = work / "dispatch" / "items"
    items_dir.mkdir(parents=True, exist_ok=True)

    for old_jf in items_dir.glob("judge_*.json"):
        try:
            old_jf.unlink()
        except Exception:
            pass

    subagents: List[Dict[str, Any]] = []
    item_files: List[str] = []

    for idx, bf in enumerate(split_batches, start=1):
        m = re.search(r"judge_batch_(\d+)", bf.name)
        j_id = m.group(1) if m else f"{idx:02d}"

        # Extract items for in-prompt payload (strictly blind: zero ground truth)
        items_payload: List[Dict[str, Any]] = []
        try:
            raw_items = batch_items_map[bf] if bf in batch_items_map else _load_batch_items(bf)
            for item in raw_items:
                if isinstance(item, dict):
                    q_id = item.get("question_id") or item.get("item_id") or item.get("id")
                    cleaned_item = {
                        "question_id": q_id,
                        "item_id": item.get("item_id") or q_id,
                        "question_type": item.get("question_type") or item.get("interaction_type") or "multiple_choice",
                        "stem_es": item.get("stem_es") or item.get("stem") or "",
                        "options": item.get("options") or item.get("choices") or [],
                    }
                    if "answer_contract" in item:
                        cleaned_item["answer_contract"] = item["answer_contract"]
                    if "graph" in item:
                        cleaned_item["graph"] = item["graph"]
                    for m20_key in (
                        "symbolic_config",
                        "proof_dag",
                        "adversarial_break",
                        "unstructured_model",
                        "invariant_canvas",
                        "concept_matching",
                        "judge_instructions",
                        "response_schema",
                    ):
                        if m20_key in item:
                            cleaned_item[m20_key] = item[m20_key]
                    items_payload.append(cleaned_item)
        except Exception as e:
            logger.warning("Could not read judge batch %s: %s", bf, e)

        items_json_str = json.dumps(items_payload, indent=2, ensure_ascii=False)

        j_tag = f"judge_{j_id}"
        out_target = f"{work_rel}/verification/judge_responses_{j_id}.json"
        alt_out_target = f"{work_rel}/judges/{j_tag}.json"
        item_filename = f"judge_{j_id}.json"
        item_file_rel = f"{work_rel}/dispatch/items/{item_filename}"

        disk_done_signal = f"Cierre al aprobar: {out_target} (señal terminal DONE)"
        if use_pointer:
            read_paths = [item_file_rel]
            protocol_directives = [
                f"- **PROHIBIDO leer cualquier archivo del curso, templates, shards o ground truth distinto de este lote asignado `{item_file_rel}`.**",
                f"- Resuelve analíticamente sin `run_command` (reglas en tu SystemPrompt `c2c_judge`) y escribe `{out_target}` con `write_file(Overwrite=True)`.",
                f"- Cierre al aprobar: `{out_target}` (señal terminal DONE).",
            ]
        else:
            read_paths = ["Items inyectados en este prompt"]
            protocol_directives = [
                "- **NO EJECUTES `read_file` para leer el lote:** Todos los reactivos ya están inyectados abajo.",
                "- **NO EJECUTES `run_command`:** Resuelve analíticamente desde primeros principios.",
                "- **Completa tu tarea en 1 SOLO TURNO** escribiendo directamente el archivo de respuestas con `write_file`.",
                f"- Cierre al aprobar: `{out_target}` (señal terminal DONE).",
            ]

        scope_header = build_scope_header(
            role="judge",
            read_paths=read_paths,
            write_paths=[out_target, alt_out_target, f"{work_rel}/judge_responses_{j_id}.json"],
            forbidden_paths=[
                "judge_ground_truth.json",
                "work/templates/*",
                "templates/*",
                "engine/*",
                "search_web",
                "read_url_content",
                "navegación por internet",
            ],
            done_signal=disk_done_signal,
        )

        turn_header = "## 1. PROTOCOLO EN 2 TURNOS LLM (cierre terminal DONE)" if use_pointer else "## 1. PROTOCOLO ZERO-WARMUP EN 1 SOLO TURNO"
        prompt_lines = [
            f"# Asignación de Evaluación a Ciegas: Blind Judge `{j_tag}` (C2C v3.21 Zero-Warmup Load Inversion)",
            "",
            scope_header,
            "",
            turn_header,
            f"- **Judge ID:** `{j_tag}`",
            f"- **Lote Asignado:** `{bf.name}`",
            f"- **Ruta de Salida Obligatoria:** `{out_target}` (o `{alt_out_target}`)",
        ]
        prompt_lines.extend(protocol_directives)
        prompt_lines.extend([
            "",
            "## 2. ÍTEMS A EVALUAR (ZERO-WARMUP IN-PROMPT PAYLOAD)",
            "```json",
            items_json_str,
            "```",
        ])
        prompt_full = "\n".join(prompt_lines)

        prompt_sha256 = hashlib.sha256(prompt_full.encode("utf-8")).hexdigest()
        item_ids = [it.get("question_id") or it.get("id") or f"item_{i}" for i, it in enumerate(items_payload)]
        work_order_meta = {
            "role": f"Blind Judge {j_id}",
            "batch_id": j_id,
            "batch_file": bf.name,
            "items_count": len(items_payload),
            "item_ids": item_ids,
            "output_target": out_target,
            "prompt_sha256": prompt_sha256,
        }
        item_file = items_dir / item_filename
        item_data = {
            "TypeName": "c2c_judge",
            "Role": f"Blind Judge {j_id}",
            "Model": "inherit",
            "Workspace": "inherit",
            "batch_file": bf.name,
            "batch_id": j_id,
            "items_count": len(items_payload),
            "item_ids": item_ids,
            "output_target": out_target,
            "Prompt": prompt_full,
            "work_order": work_order_meta,
            "items": items_payload,
        }
        item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")

        # Pure-data payload file for live Blind Judge (minimal {"items": [...]} wrapper, zero bloat)
        items_only_filename = f"judge_{j_id}_items.json"
        items_only_file = items_dir / items_only_filename
        items_only_rel = f"{work_rel}/dispatch/items/{items_only_filename}"
        items_only_file.write_text(json.dumps({"items": items_payload}, indent=2, ensure_ascii=False), encoding="utf-8")

        if use_pointer:
            extra = f"[SCOPE-LOCK] READ ONLY `{items_only_filename}` (not `{item_filename}`); WRITE `{out_target}`."
            pointer_prompt = make_pointer_prompt(
                role_name=f"Blind Judge {j_id}",
                work_order_rel=items_only_rel,
                done_signal=f"DONE: {out_target}",
                extra_instructions=extra,
            )
            if len(pointer_prompt.encode("utf-8")) > 400:
                extra = f"[SCOPE-LOCK] READ `{items_only_filename}` (`{item_filename}`); WRITE `{out_target}`."
                pointer_prompt = make_pointer_prompt(
                    role_name=f"Blind Judge {j_id}",
                    work_order_rel=items_only_rel,
                    done_signal=f"DONE: {out_target}",
                    extra_instructions=extra,
                )
            subagent_item = {
                "TypeName": "c2c_judge",
                "Role": f"Blind Judge {j_id}",
                "Model": "inherit",
                "Prompt": pointer_prompt,
            }
        else:
            inline_data = dict(item_data)
            inline_data["Prompt"] = prompt_full.replace(disk_done_signal, f"DONE: {out_target}").replace(
                f"Cierre al aprobar: `{out_target}` (señal terminal DONE).",
                f"DONE: {out_target}",
            )
            subagent_item = inline_data

        subagents.append(subagent_item)
        item_files.append(item_file.resolve().as_posix())

    dispatch_dir = work / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    judges_audit_file = dispatch_dir / "judges.json"
    dispatched_at = datetime.now(timezone.utc).isoformat()
    judges_audit = {
        "stage": "judges",
        "dispatched_at": dispatched_at,
        "subagents_count": len(subagents),
        "max_items_per_judge": max_items_per_judge,
        "item_files": item_files,
        "Subagents": subagents,
    }
    _atomic_write_text(judges_audit_file, json.dumps(judges_audit, indent=2, ensure_ascii=False))

    judge_compat_file = dispatch_dir / "judge.json"
    _atomic_write_text(judge_compat_file, json.dumps(judges_audit, indent=2, ensure_ascii=False))

    snap = snapshot_work_dir(work)
    snap_json = json.dumps({k: list(v) for k, v in snap.items()}, indent=2, ensure_ascii=False)
    _atomic_write_text(dispatch_dir / "judges_snapshot.json", snap_json)
    _atomic_write_text(dispatch_dir / "judge_snapshot.json", snap_json)

    return {"dispatched_at": dispatched_at, "Subagents": subagents, "item_files": item_files}


def build_dispatch(
    role: str,
    work_dir: Union[str, Path],
    ids: Optional[List[Union[str, int]]] = None,
    ready_only: bool = False,
    pointer: bool = True,
    wave_index: Optional[int] = None,
) -> Dict[str, Any]:
    """Generates invoke_subagent payload with strict SCOPE-LOCK for the given role."""
    use_pointer = pointer if pointer is not None else (os.getenv("C2C_POINTER_PROMPTS", "1").lower() in ("1", "true", "yes"))

    if role in ("vision", "vision-legacy"):
        raise ValueError(f"Stages 'vision' and 'vision-legacy' have been removed in C2C v3.2. Use Direct PDF Ingestion instead.")

    if role in ("cta", "cta-direct", "cta-map", "c2c_cta_architect"):
        mode = "mapreduce" if role == "cta-map" else None
        return dispatch_cta(work_dir, mode=mode, pointer=use_pointer)

    if role in ("author", "authors", "c2c_shard_author"):
        return dispatch_authors(work_dir, pointer=use_pointer, wave_index=wave_index, ids=ids)

    if role in ("judge", "judges", "c2c_judge"):
        return dispatch_judges(work_dir, pointer=use_pointer, ready_only=ready_only, ids=ids)

    if role in ("cta-reduce", "c2c_cta_harmonizer"):
        return dispatch_cta_reduce(work_dir, pointer=use_pointer)

    if role not in ROLE_SPECS:
        raise ValueError(f"Unknown role: '{role}'. Available roles: {list(ROLE_SPECS.keys())}")

    work = Path(work_dir).resolve()
    work_rel = get_work_rel(work_dir)
    spec = ROLE_SPECS[role]
    sys_prompt = spec["system_prompt"]
    turn_budget = spec["turn_budget"]
    forbidden = list(spec["forbidden"])

    dispatch_dir = work / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    state_file = dispatch_dir / "state.json"

    state: Dict[str, Any] = {"dispatched": {}}
    if state_file.is_file():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning("Could not read dispatch state: %s", e)

    dispatched_ids: List[str] = state.get("dispatched", {}).get(role, [])
    subagents: List[Dict[str, Any]] = []
    item_files: List[str] = []

    # CTA-REDUCE
    if role == "cta-reduce":
        shard_jsons = sorted(list((work / "cta_parts").glob("*.json")) + list((work / "cta").glob("cta_shard_*.json")))
        shard_json_rel_list = [f"{work_rel}/{p.relative_to(work).as_posix()}" for p in shard_jsons] if shard_jsons else [f"{work_rel}/cta_parts/*.json"]
        shard_json_lines = "\n".join(f"- `{p}`" for p in shard_json_rel_list)
        _, _, cmd_prefix = _resolve_repo_python_and_env()
        compile_cmd = f"{cmd_prefix} .agents/skills/content-to-course/cta_merge.py apply --work \"{work.resolve().as_posix()}\""

        scope_header = build_scope_header(
            role="cta-reduce",
            read_paths=[f"{work_rel}/cta_outline.json", f"{work_rel}/duplicate_candidates.json"] + shard_json_rel_list,
            write_paths=[f"{work_rel}/cta_harmonize.json", f"{work_rel}/cta.json", f"{work_rel}/cta.md"],
            done_signal=f"DONE: {work_rel}/cta.json",
        )

        prompt_text = (
            f"# Asignación de Tarea: CTA Harmonizer (MapReduce Harmonization v3.21)\n\n"
            f"{scope_header}\n\n"
            f"## 1. FRAGMENTOS CTA A FUSIONAR Y ARMONIZAR\n"
            f"{shard_json_lines}\n\n"
            f"## 2. INSTRUCCIONES DE EJECUCIÓN\n"
            f"0. FAST-PATH: lee en paralelo SOLO `cta_outline.json` + `duplicate_candidates.json`, escribe `cta_harmonize.json` de una vez y ejecuta el merge. PROHIBIDO listar/buscar directorios o leer los shards. Si el merge falla, corrige `cta_harmonize.json` con `edit_file` y re-ejecuta.\n"
            f"1. Analiza los fragmentos curriculares y deduplica competencias.\n"
            f"2. Emite la armonización en `{work_rel}/cta_harmonize.json` y luego EJECUTA TÚ el merge oficial (obligatorio, el orquestador NO lo ejecuta):\n"
            f"   ```bash\n"
            f"   {compile_cmd}\n"
            f"   ```\n"
            f"3. Sigue las directivas de tu System Prompt `c2c_cta_harmonizer` y finaliza estrictamente con: `DONE: {work_rel}/cta.json`.\n"
        )
        item_data = {
            "TypeName": spec["type_name"],
            "Role": "CTA Harmonizer",
            "Model": spec["model"],
            "Prompt": prompt_text,
        }
        subagents.append(item_data)
        dispatched_ids.append("harmonizer")
        items_dir = work / "dispatch" / "items"
        items_dir.mkdir(parents=True, exist_ok=True)
        item_file = items_dir / "cta_harmonize_01.json"
        item_file.write_text(json.dumps(item_data, indent=2, ensure_ascii=False), encoding="utf-8")
        item_files.append(item_file.resolve().as_posix())

    # REPAIR
    elif role == "repair":
        templates_report_file = work / "reports" / "templates_report.json"
        judge_report_file = work / "judge_report.json"
        attempts_dir = work / ".check_attempts"
        templates_dir = work / "templates"
        failing_targets: Dict[str, Dict[str, Any]] = {}

        # 1. Build comp_to_shard and shard_to_comps mapping FIRST
        shard_map: Dict[str, str] = {}
        shard_to_comps: Dict[str, List[str]] = {}
        eff_repair_k = DEFAULT_TEMPLATES_PER_MODALITY
        pre_shard_manifest = work / "shards" / "pre_shard_manifest.json"
        if not pre_shard_manifest.is_file():
            pre_shard_manifest = work / "pre_shard_manifest.json"
        if pre_shard_manifest.is_file():
            try:
                sm_data = json.loads(pre_shard_manifest.read_text(encoding="utf-8"))
                eff_repair_k = max(
                    1,
                    int(
                        (sm_data.get("stage4_contract") or {}).get("templates_per_modality")
                        or sm_data.get("templates_per_modality")
                        or DEFAULT_TEMPLATES_PER_MODALITY
                    ),
                )
                shards_info = sm_data.get("shards", [])
                if isinstance(shards_info, list):
                    for s in shards_info:
                        s_id = s.get("shard_id") or "shard_01"
                        c_ids = s.get("competency_ids") or []
                        if not c_ids and "competencies" in s:
                            c_ids = [c.get("id") for c in s["competencies"] if isinstance(c, dict) and "id" in c]
                        for cid in c_ids:
                            if cid:
                                shard_map[cid] = s_id
                                shard_to_comps.setdefault(s_id, []).append(cid)
                elif isinstance(shards_info, dict):
                    for s_id, comps in shards_info.items():
                        if isinstance(comps, list):
                            for c in comps:
                                cid = c.get("id") if isinstance(c, dict) else str(c)
                                if cid:
                                    shard_map[cid] = s_id
                                    shard_to_comps.setdefault(s_id, []).append(cid)
            except Exception as e:
                logger.warning("Error reading pre_shard_manifest.json in repair: %s", e)

        for sf in sorted((work / "shards").glob("shard_*.json")):
            try:
                sdata = json.loads(sf.read_text(encoding="utf-8"))
                s_id = sdata.get("shard_id", sf.stem)
                for cid in sdata.get("competency_ids", []):
                    if cid and cid not in shard_map:
                        shard_map[cid] = s_id
                        shard_to_comps.setdefault(s_id, []).append(cid)
                if "competencies" in sdata and isinstance(sdata["competencies"], list):
                    for c in sdata["competencies"]:
                        cid = c.get("id") if isinstance(c, dict) else str(c)
                        if cid and cid not in shard_map:
                            shard_map[cid] = s_id
                            shard_to_comps.setdefault(s_id, []).append(cid)
            except Exception:
                pass

        # 2. Collect failures from templates_report.json and judge_report.json
        if templates_report_file.is_file():
            try:
                tr = json.loads(templates_report_file.read_text(encoding="utf-8"))
                for res in tr.get("results", []):
                    if res.get("status") in ("fail", "FAIL"):
                        cid = res.get("cid") or res.get("competency_id")
                        if cid:
                            failing_targets.setdefault(cid, {}).setdefault("template_errors", []).extend(res.get("errors", []))
                            failing_targets.setdefault(cid, {}).setdefault("errors", []).extend(res.get("errors", []))
                for comp_item in tr.get("competencies", []):
                    if isinstance(comp_item, dict) and comp_item.get("status") in ("fail", "FAIL"):
                        cid = comp_item.get("cid") or comp_item.get("id") or comp_item.get("competency_id")
                        if cid:
                            failing_targets.setdefault(cid, {}).setdefault("template_errors", []).extend(comp_item.get("errors", []))
                            failing_targets.setdefault(cid, {}).setdefault("errors", []).extend(comp_item.get("errors", []))
                if isinstance(tr.get("errors_by_cid"), dict):
                    for cid, err_list in tr["errors_by_cid"].items():
                        if err_list:
                            failing_targets.setdefault(cid, {}).setdefault("template_errors", []).extend(err_list)
                            failing_targets.setdefault(cid, {}).setdefault("errors", []).extend(err_list)
                fc_data = tr.get("failed_competencies")
                if isinstance(fc_data, dict):
                    for cid, c_data in fc_data.items():
                        c_errs = []
                        if isinstance(c_data, dict):
                            c_errs = c_data.get("errors", [])
                        elif isinstance(c_data, list):
                            c_errs = c_data
                        if c_errs:
                            failing_targets.setdefault(cid, {}).setdefault("template_errors", []).extend(c_errs)
                            failing_targets.setdefault(cid, {}).setdefault("errors", []).extend(c_errs)
                        else:
                            failing_targets.setdefault(cid, {})
                elif isinstance(fc_data, list):
                    for cid in fc_data:
                        if isinstance(cid, str):
                            failing_targets.setdefault(cid, {})

                flat_errors = tr.get("errors", [])
                if isinstance(flat_errors, list):
                    for err in flat_errors:
                        err_str = str(err)
                        matched_cids = set()
                        for known_cid in shard_map.keys():
                            if re.search(rf"(?<![A-Za-z0-9_-]){re.escape(known_cid)}(?![A-Za-z0-9_-])", err_str):
                                matched_cids.add(known_cid)
                        for m in re.finditer(r"\b(?:PRE|Aut|C|H|Hab|COMP)-[A-Za-z0-9_-]+\b", err_str):
                            cand_cid = m.group(0)
                            if cand_cid in shard_map:
                                matched_cids.add(cand_cid)
                        for cid in matched_cids:
                            t_entry = failing_targets.setdefault(cid, {})
                            errs_list = t_entry.setdefault("template_errors", [])
                            if err_str not in errs_list:
                                errs_list.append(err_str)
                            all_errs = t_entry.setdefault("errors", [])
                            if err_str not in all_errs:
                                all_errs.append(err_str)

                # Clean and deduplicate errors per target
                for cid, t_entry in failing_targets.items():
                    for k in ("template_errors", "errors"):
                        if k in t_entry and isinstance(t_entry[k], list):
                            seen_e = set()
                            dedup_e = []
                            for e in t_entry[k]:
                                s_e = str(e)
                                if s_e not in seen_e:
                                    seen_e.add(s_e)
                                    dedup_e.append(s_e)
                            t_entry[k] = dedup_e
            except Exception as e:
                logger.warning("Error reading templates_report.json: %s", e)

        if judge_report_file.is_file():
            try:
                jr = json.loads(judge_report_file.read_text(encoding="utf-8"))
                # 1. Disagreements and discordances
                for disc in (jr.get("disagreements", []) or jr.get("discordances", [])):
                    if isinstance(disc, dict):
                        cid = disc.get("cid") or disc.get("competency_id")
                        if cid:
                            t_entry = failing_targets.setdefault(cid, {})
                            disc_list = t_entry.setdefault("judge_disagreements", [])
                            disc_list.append(disc)
                            t_entry["judge_disagreement"] = disc
                            reason = disc.get("reason") or disc.get("error") or disc.get("feedback") or "Discordancia evaluador ciego"
                            item_id = disc.get("item_id") or disc.get("question_id") or ""
                            r_str = f"Discordancia en {item_id}: {reason}" if item_id else f"Discordancia: {reason}"
                            t_entry.setdefault("errors", []).append(r_str)

                # 2. Failed templates reported by judge evaluation
                ft_data = jr.get("failed_templates", [])
                if isinstance(ft_data, dict):
                    for cid, f_info in ft_data.items():
                        t_entry = failing_targets.setdefault(cid, {})
                        err_items = f_info if isinstance(f_info, list) else [f_info]
                        for ei in err_items:
                            ei_str = str(ei)
                            t_entry.setdefault("errors", []).append(ei_str)
                            t_entry.setdefault("template_errors", []).append(ei_str)
                elif isinstance(ft_data, list):
                    for item in ft_data:
                        if isinstance(item, dict):
                            cid = item.get("cid") or item.get("competency_id")
                            if cid:
                                t_entry = failing_targets.setdefault(cid, {})
                                reason = item.get("reason") or item.get("error") or str(item)
                                t_entry.setdefault("errors", []).append(str(reason))
                                t_entry.setdefault("template_errors", []).append(str(reason))
                        elif isinstance(item, str):
                            failing_targets.setdefault(item, {})

                # 3. Failed competencies reported in judge report
                fc_data = jr.get("failed_competencies", [])
                if isinstance(fc_data, dict):
                    for cid, f_info in fc_data.items():
                        t_entry = failing_targets.setdefault(cid, {})
                        err_items = f_info if isinstance(f_info, list) else [f_info]
                        for ei in err_items:
                            t_entry.setdefault("errors", []).append(str(ei))
                elif isinstance(fc_data, list):
                    for cid in fc_data:
                        if isinstance(cid, str):
                            failing_targets.setdefault(cid, {})
                        elif isinstance(cid, dict):
                            c_id = cid.get("cid") or cid.get("id") or cid.get("competency_id")
                            if c_id:
                                t_entry = failing_targets.setdefault(c_id, {})
                                if cid.get("reason"):
                                    t_entry.setdefault("errors", []).append(str(cid["reason"]))
            except Exception as e:
                logger.warning("Error reading judge_report.json: %s", e)

        # 2b. Also ingest work/specific_error_report.json and work/audit_gate_report.json (Pre-Publish Quality Gate & Build Stem Diversity Gate)
        specific_report_file = work / "specific_error_report.json"
        audit_gate_file = work / "audit_gate_report.json"
        if not specific_report_file.is_file() and audit_gate_file.is_file():
            try:
                from course_publisher import build_specific_error_report
                ag_data = json.loads(audit_gate_file.read_text(encoding="utf-8"))
                course_json_p = work / "course.json"
                c_data = json.loads(course_json_p.read_text(encoding="utf-8")) if course_json_p.is_file() else {}
                build_specific_error_report(audit_report=ag_data, course_data=c_data, work_dir=work)
            except Exception as e:
                logger.warning("Could not synthesize specific_error_report.json from audit_gate_report.json: %s", e)

        if specific_report_file.is_file():
            try:
                sr = json.loads(specific_report_file.read_text(encoding="utf-8"))
                seen_loc_keys: Set[Tuple[Any, ...]] = set()
                diag_by_comp = sr.get("diagnostics_by_competency")
                if isinstance(diag_by_comp, dict):
                    for cid_loc, g_entries in diag_by_comp.items():
                        if not cid_loc or cid_loc in ("global", "COURSE-LEVEL") or not isinstance(g_entries, list):
                            continue
                        t_entry = failing_targets.setdefault(cid_loc, {})
                        for g_ent in g_entries:
                            if not isinstance(g_ent, dict):
                                continue
                            r_tag = g_ent.get("rule_tag", "QUALITY-GATE")
                            l_name = g_ent.get("linter", "quality_gate_linter")
                            s_file = g_ent.get("file") or g_ent.get("shard_file") or f"{shard_map.get(cid_loc, 'shard_01')}_data.py"
                            l_s = g_ent.get("offending_start_line", g_ent.get("offending_line_start", 1))
                            l_e = g_ent.get("offending_end_line", g_ent.get("offending_line_end", l_s))
                            tpl_id = g_ent.get("template_id") or "UNKNOWN"
                            loc_key = (cid_loc, str(r_tag), str(s_file), int(l_s or 1), int(l_e or 1), str(tpl_id))
                            if loc_key in seen_loc_keys:
                                continue
                            seen_loc_keys.add(loc_key)
                            i_ids = ", ".join((g_ent.get("item_ids") or [])[:5])
                            fn_name = g_ent.get("gen_fn_name") or "N/A"
                            fn_s = g_ent.get("fn_start_line", g_ent.get("gen_fn_line_start", 1))
                            fn_e = g_ent.get("fn_end_line", g_ent.get("gen_fn_line_end", 1))
                            tup_s = g_ent.get("tuple_start_line", g_ent.get("tuple_line_start", 1))
                            tup_e = g_ent.get("tuple_end_line", g_ent.get("tuple_line_end", 1))
                            msgs = g_ent.get("messages") or []
                            desc_txt = msgs[0] if msgs else g_ent.get("description", "")
                            cause_txt = g_ent.get("cause", "")
                            action_txt = g_ent.get("action", "")
                            code_lns = g_ent.get("offending_code") or g_ent.get("offending_code_lines") or []
                            summary_line = (
                                f"[{r_tag}] {s_file}:L{l_s}-L{l_e} | "
                                f"competency_id={cid_loc} | template_id={tpl_id} | item_id=[{i_ids}] | "
                                f"[Fn {fn_name}: L{fn_s}..L{fn_e} | Tupla: L{tup_s}..L{tup_e}] — "
                                f"Descripción: {desc_txt} | Causa: {cause_txt} | Acción: {action_txt}"
                            )
                            errs_list = t_entry.setdefault("errors", [])
                            if summary_line not in errs_list:
                                errs_list.append(summary_line)
                            tpl_errs = t_entry.setdefault("template_errors", [])
                            if summary_line not in tpl_errs:
                                tpl_errs.append(summary_line)
                            q_gate_list = t_entry.setdefault("specific_error_locations", [])
                            q_gate_list.append({
                                "rule_tag": r_tag,
                                "linter": l_name,
                                "description": desc_txt,
                                "cause": cause_txt,
                                "action": action_txt,
                                "competency_id": cid_loc,
                                "shard_file": s_file,
                                "template_id": tpl_id,
                                "item_ids": g_ent.get("item_ids") or [],
                                "gen_fn_name": fn_name,
                                "gen_fn_line_start": fn_s,
                                "gen_fn_line_end": fn_e,
                                "tuple_line_start": tup_s,
                                "tuple_line_end": tup_e,
                                "offending_line_start": l_s,
                                "offending_line_end": l_e,
                                "offending_code_lines": code_lns,
                            })
                for grp in (sr.get("groups") or []):
                    if not isinstance(grp, dict):
                        continue
                    linter_name = grp.get("linter", "quality_gate_linter")
                    rule_tag = grp.get("rule_tag", "QUALITY-GATE")
                    desc_txt = grp.get("description", "")
                    cause_txt = grp.get("cause", "")
                    action_txt = grp.get("action", "")
                    for loc in (grp.get("locations") or []):
                        if not isinstance(loc, dict):
                            continue
                        cid_loc = loc.get("competency_id")
                        if not cid_loc or cid_loc == "COURSE-LEVEL":
                            continue
                        t_entry = failing_targets.setdefault(cid_loc, {})
                        s_file = loc.get("shard_file") or f"{shard_map.get(cid_loc, 'shard_01')}_data.py"
                        l_s = loc.get("offending_line_start", 1)
                        l_e = loc.get("offending_line_end", l_s)
                        tpl_id = loc.get("template_id") or "UNKNOWN"
                        loc_key = (cid_loc, str(rule_tag), str(s_file), int(l_s or 1), int(l_e or 1), str(tpl_id))
                        if loc_key in seen_loc_keys:
                            continue
                        seen_loc_keys.add(loc_key)
                        i_ids = ", ".join((loc.get("item_ids") or [])[:5])
                        fn_name = loc.get("gen_fn_name") or "N/A"
                        fn_s = loc.get("gen_fn_line_start", 1)
                        fn_e = loc.get("gen_fn_line_end", 1)
                        tup_s = loc.get("tuple_line_start", 1)
                        tup_e = loc.get("tuple_line_end", 1)
                        summary_line = (
                            f"[{rule_tag} / {linter_name}] {s_file}:L{l_s}-L{l_e} | "
                            f"competency_id={cid_loc} | template_id={tpl_id} | item_id=[{i_ids}] | "
                            f"[Fn {fn_name}: L{fn_s}..L{fn_e} | Tupla: L{tup_s}..L{tup_e}] — "
                            f"Descripción: {desc_txt} | Causa: {cause_txt} | Acción: {action_txt}"
                        )
                        errs_list = t_entry.setdefault("errors", [])
                        if summary_line not in errs_list:
                            errs_list.append(summary_line)
                        tpl_errs = t_entry.setdefault("template_errors", [])
                        if summary_line not in tpl_errs:
                            tpl_errs.append(summary_line)
                        q_gate_list = t_entry.setdefault("specific_error_locations", [])
                        q_gate_list.append({
                            "rule_tag": rule_tag,
                            "linter": linter_name,
                            "description": desc_txt,
                            "cause": cause_txt,
                            "action": action_txt,
                            **loc,
                        })
            except Exception as e:
                logger.warning("Error reading specific_error_report.json: %s", e)

        # 3. Also detect circuit-broken or failing shards from .check_attempts/ and missing work/templates/<cid>.json
        shard_attempt_diagnostics: Dict[str, Dict[str, Any]] = {}
        if attempts_dir.is_dir():
            for att_f in sorted(attempts_dir.glob("*.json")):
                try:
                    adata = json.loads(att_f.read_text(encoding="utf-8"))
                    if not isinstance(adata, dict):
                        continue
                    fname = att_f.stem
                    matched_s_id: Optional[str] = None
                    for cand_s_id in shard_to_comps:
                        if _matches_token(cand_s_id, fname):
                            matched_s_id = cand_s_id
                            break
                    if matched_s_id:
                        streak = adata.get("same_error_streak", 0)
                        compiles = adata.get("distinct_compiles", adata.get("attempt_count", 0))
                        last_errs = adata.get("last_errors") or adata.get("errors") or []
                        is_cb = fname.startswith("circuit_breaker") or streak >= 3 or compiles > 10 or "CIRCUIT BREAKER" in str(last_errs)
                        diag_entry = shard_attempt_diagnostics.setdefault(matched_s_id, {})
                        if is_cb:
                            diag_entry["circuit_broken"] = True
                        if last_errs:
                            diag_entry["compiler_last_errors"] = last_errs
                        diag_entry["same_error_streak"] = max(diag_entry.get("same_error_streak", 0), streak)
                except Exception:
                    pass

        for cid, s_id in shard_map.items():
            tpl_ok = (templates_dir / f"{cid}.json").is_file()
            s_diag = shard_attempt_diagnostics.get(s_id, {})
            if not tpl_ok or s_diag.get("circuit_broken"):
                target_diag = failing_targets.setdefault(cid, {})
                if not tpl_ok:
                    target_diag["missing_compiled_template"] = f"work/templates/{cid}.json"
                if s_diag:
                    target_diag["attempt_diagnostics"] = s_diag

        # 4. Filter by requested ids (supporting both competency IDs like 'Hab-02' and shard IDs like 'shard_02')
        if ids is not None:
            raw_list = [ids] if isinstance(ids, (str, int)) else ids
            flattened_ids: List[str] = [
                part.strip()
                for raw in raw_list
                for part in str(raw).split(",")
                if part.strip()
            ]
            seen_rids: Set[str] = set()
            unique_flattened_ids: List[str] = []
            for rid in flattened_ids:
                if rid not in seen_rids:
                    seen_rids.add(rid)
                    unique_flattened_ids.append(rid)

            expanded_ids: List[str] = []
            for rid in unique_flattened_ids:
                if rid in shard_to_comps:
                    for c in shard_to_comps[rid]:
                        if c not in expanded_ids:
                            expanded_ids.append(c)
                else:
                    if rid not in expanded_ids:
                        expanded_ids.append(rid)

            ordered_failing: Dict[str, Any] = {}
            for cid in expanded_ids:
                if cid in failing_targets:
                    t_diag = failing_targets[cid]
                    if t_diag.get("template_errors") or t_diag.get("errors"):
                        t_diag.pop("manual_request", None)
                    ordered_failing[cid] = t_diag
                else:
                    s_id = shard_map.get(cid)
                    diag_info: Dict[str, Any] = {"manual_request": True}
                    if s_id and s_id in shard_attempt_diagnostics:
                        diag_info["attempt_diagnostics"] = shard_attempt_diagnostics[s_id]
                    ordered_failing[cid] = diag_info
            failing_targets = ordered_failing

        shard_manifest_rel = (
            f"{work_rel}/shards/pre_shard_manifest.json"
            if (work / "shards" / "pre_shard_manifest.json").is_file()
            else f"{work_rel}/pre_shard_manifest.json"
        )
        manifest_rel = shard_manifest_rel
        cta_rel = f"{work_rel}/cta.json"

        items_dir = work / "dispatch" / "items"
        items_dir.mkdir(parents=True, exist_ok=True)
        prompts_repair_dir = work / "prompts" / "repair"
        prompts_repair_dir.mkdir(parents=True, exist_ok=True)
        repair_slices_dir = work / "dispatch" / "repair_slices"
        repair_slices_dir.mkdir(parents=True, exist_ok=True)
        if ids is None:
            for old_rf in items_dir.glob("repair_*.json"):
                try:
                    old_rf.unlink()
                except Exception:
                    pass
            for old_pf in prompts_repair_dir.glob("repair_*.json"):
                try:
                    old_pf.unlink()
                except Exception:
                    pass
            for old_sf in repair_slices_dir.glob("*.json"):
                try:
                    old_sf.unlink()
                except Exception:
                    pass
        item_files: List[str] = []
        cleared_attempt_files: List[str] = []

        cta_comps_by_id: Dict[str, Dict[str, Any]] = {}
        cta_file = work / "cta.json"
        if cta_file.is_file():
            try:
                cta_raw = json.loads(cta_file.read_text(encoding="utf-8"))
                c_list = cta_raw.get("competencies", []) if isinstance(cta_raw, dict) else (cta_raw if isinstance(cta_raw, list) else [])
                if isinstance(c_list, dict):
                    for k_cid, c_val in c_list.items():
                        if isinstance(c_val, dict):
                            cta_comps_by_id[k_cid] = c_val
                elif isinstance(c_list, list):
                    for c_val in c_list:
                        if isinstance(c_val, dict) and c_val.get("id"):
                            cta_comps_by_id[c_val["id"]] = c_val
            except Exception as e:
                logger.warning("Could not index cta.json for repair slices: %s", e)

        _, _, cmd_prefix = _resolve_repo_python_and_env()
        shard_repair_groups: Dict[str, List[Dict[str, Any]]] = {}
        per_cid_entries: List[Dict[str, Any]] = []

        for idx, (cid, diag) in enumerate(failing_targets.items(), start=1):
            shard_id = shard_map.get(cid)
            if not shard_id:
                raise ValueError(
                    f"BLOCKER:: Competency '{cid}' is not mapped to any shard in pre_shard_manifest.json"
                )

            # Auto-reset sticky circuit breaker / attempt state in .check_attempts/ for this shard & cid
            try:
                if attempts_dir.is_dir():
                    norm_s_id = re.sub(r"[^\w]", "_", str(shard_id))
                    dash_s_id = str(shard_id).replace("_", "-")
                    norm_cid = re.sub(r"[^\w]", "_", str(cid))
                    dash_cid = str(cid).replace("_", "-")
                    targets_to_clear = [
                        attempts_dir / f"pass_{shard_id}.json",
                        attempts_dir / f"pass_{norm_s_id}.json",
                        attempts_dir / f"pass_{dash_s_id}.json",
                        attempts_dir / f"pass_{cid}.json",
                        attempts_dir / f"pass_{norm_cid}.json",
                        attempts_dir / f"pass_{dash_cid}.json",
                        attempts_dir / f"pass_comp_{cid}.json",
                        attempts_dir / f"pass_comp_{norm_cid}.json",
                        attempts_dir / f"pass_comp_{dash_cid}.json",
                        attempts_dir / f"pass_{shard_id}_{cid}.json",
                        attempts_dir / f"pass_{shard_id}_{norm_cid}.json",
                    ]
                    for p_file in targets_to_clear:
                        try:
                            if p_file.is_file():
                                p_file.unlink()
                                if p_file.name not in cleared_attempt_files:
                                    cleared_attempt_files.append(p_file.name)
                        except Exception as e:
                            logger.warning("Could not remove pass file %s: %s", p_file, e)

                    try:
                        f_list = list(attempts_dir.glob("*.json"))
                    except Exception as e:
                        logger.warning("Could not list attempt files in %s: %s", attempts_dir, e)
                        f_list = []

                    tokens_to_match = [
                        t for t in (norm_s_id, dash_s_id, norm_cid, dash_cid, str(shard_id), str(cid)) if t
                    ]
                    for att_f in f_list:
                        stem = att_f.stem
                        if any(_matches_token(tok, stem) for tok in tokens_to_match):
                            try:
                                if att_f.is_file():
                                    att_f.unlink()
                                    if att_f.name not in cleared_attempt_files:
                                        cleared_attempt_files.append(att_f.name)
                            except Exception as e:
                                logger.warning("Could not remove sticky attempt file %s: %s", att_f, e)
            except Exception as e:
                logger.warning("Error accessing .check_attempts dir: %s", e)

            out_py = f"{work_rel}/shards/{shard_id}_data.py"
            out_json = f"{work_rel}/shards/{shard_id}.json"
            shard_fix_dir = work / "shards" / "shard_fixes" / shard_id
            shard_fix_dir.mkdir(parents=True, exist_ok=True)
            shard_fix_path = f"{work_rel}/shards/shard_fixes/{shard_id}/{cid}.py"
            compile_cmd = (
                f"{cmd_prefix} -u .agents/skills/content-to-course/compile_shard.py "
                f"--input {out_py} --output {out_json} --work {work_rel} --shard {shard_id} --strict --min-archetypes 4 --templates-per-modality {eff_repair_k} --fail-total"
            )

            # Generate compact Competence Slice (< 2 KB) for isolated Turn-0 repair
            comp_info = cta_comps_by_id.get(cid, {})
            spec_locs = diag.get("specific_error_locations") or []
            shard_py_path = work / "shards" / f"{shard_id}_data.py"
            if spec_locs:
                lr_start = spec_locs[0].get("offending_line_start")
                lr_end = spec_locs[0].get("offending_line_end")
            else:
                lr_start, lr_end = _locate_competency_line_range(shard_py_path, cid)
            slice_data = {
                "id": cid,
                "title": str(comp_info.get("name") or comp_info.get("title") or cid)[:100],
                "description": str(comp_info.get("description_latex") or comp_info.get("description") or "")[:200],
                "recommended_modalities": comp_info.get("recommended_modalities") or [],
                "templates_per_modality": eff_repair_k,
                "assumptions": comp_info.get("assumptions", [])[:4],
                "distractors": [
                    {
                        "id": d.get("id"),
                        "name": str(d.get("name") or "")[:50],
                        "wrong_belief": str(d.get("wrong_belief") or "")[:100],
                        "omitted_step": str(d.get("omitted_step") or "")[:100] if d.get("omitted_step") else None,
                    }
                    for d in (comp_info.get("distractors") or [])[:6]
                ],
                "diagnostics": {
                    "errors": (diag.get("errors") or [])[:6],
                    "template_errors": (diag.get("template_errors") or [])[:6],
                    "disagreements": (diag.get("judge_disagreements") or [])[:4],
                },
                "line_range": {
                    "start": lr_start,
                    "end": lr_end,
                    "locations_count": len(spec_locs),
                },
            }
            slice_json_str = json.dumps(slice_data, indent=2, ensure_ascii=False)
            if len(slice_json_str.encode("utf-8")) > 2000:
                slice_data["description"] = slice_data["description"][:80]
                slice_json_str = json.dumps(slice_data, indent=2, ensure_ascii=False)

            safe_cid = re.sub(r"[^\w-]", "_", str(cid))
            cid_norm = re.sub(r"[^\w]", "", str(cid)).lower()
            slice_file = repair_slices_dir / f"{shard_id}_{cid}.json"
            slice_safe_file = repair_slices_dir / f"{shard_id}_{safe_cid}.json"
            slice_norm_file = repair_slices_dir / f"{shard_id}_{cid_norm}.json"
            slice_file.write_text(slice_json_str, encoding="utf-8")
            if slice_safe_file != slice_file:
                slice_safe_file.write_text(slice_json_str, encoding="utf-8")
            if slice_norm_file not in (slice_file, slice_safe_file):
                slice_norm_file.write_text(slice_json_str, encoding="utf-8")
            slice_rel = f"{work_rel}/dispatch/repair_slices/{slice_file.name}"
            slice_abs = slice_file.resolve().as_posix()
            disk_done_signal = f"Cierre al aprobar: {out_json} (señal terminal DONE)"
            scope_header = build_scope_header(
                role="repair",
                read_paths=[
                    out_py,
                    f"{work_rel}/templates/{cid}.json",
                    slice_rel,
                    f"{work_rel}/prompts/repair/repair_{cid_norm}.json",
                ],
                write_paths=[out_py, out_json, shard_fix_path, f"{work_rel}/shards/shard_fixes/{shard_id}/<CID>.py", f"{work_rel}/shards/shard_fixes/<CID>.py"],
                forbidden_paths=[
                    cta_rel,
                    f"{work_rel}/shards/pre_shard_manifest.json",
                    ".agents/skills/content-to-course/compile_shard.py",
                    "scratch/**",
                    "work/scratch/**",
                    "engine/*",
                    "SKILL.md",
                    ".check_attempts/**",
                    ".agents/skills/content-to-course/check_templates.py",
                    ".agents/skills/content-to-course/check_cta.py",
                    "src/validator/**",
                ],
                done_signal=disk_done_signal,
            )
            all_active: List[str] = []
            for e in (diag.get("template_errors") or []):
                s_e = str(e)
                if s_e not in all_active:
                    all_active.append(s_e)
            for e in (diag.get("errors") or []):
                s_e = str(e)
                if s_e not in all_active:
                    all_active.append(s_e)
            for d in (diag.get("judge_disagreements") or []):
                if isinstance(d, dict):
                    item_id = d.get("item_id") or ""
                    reason = d.get("reason") or str(d)
                    d_str = f"Discordancia evaluador ({item_id}): {reason}" if item_id else f"Discordancia evaluador: {reason}"
                    if d_str not in all_active:
                        all_active.append(d_str)
            error_bullets = ""
            if all_active:
                error_bullets = "### Diagnóstico Consolidado de Fallos y Discordancias:\n" + "\n".join(f"- `{e}`" for e in all_active[:25]) + "\n\n"
            if spec_locs:
                loc_blocks: List[str] = ["### Líneas Exactas y Contexto Infractor (`specific_error_report`):"]
                for s_loc in spec_locs[:10]:
                    s_file = s_loc.get("shard_file") or f"{shard_id}_data.py"
                    l_s = s_loc.get("offending_line_start", 1)
                    l_e = s_loc.get("offending_line_end", l_s)
                    t_id = s_loc.get("template_id") or "UNKNOWN"
                    i_ids = ", ".join((s_loc.get("item_ids") or [])[:5])
                    fn_name = s_loc.get("gen_fn_name") or "N/A"
                    fn_s = s_loc.get("gen_fn_line_start", 1)
                    fn_e = s_loc.get("gen_fn_line_end", 1)
                    tup_s = s_loc.get("tuple_line_start", 1)
                    tup_e = s_loc.get("tuple_line_end", 1)
                    loc_blocks.append(
                        f"- **`[-] [{s_loc.get('rule_tag')} / {s_loc.get('linter')}]`** `{s_file}:L{l_s}-L{l_e}` "
                        f"| `template_id`: `{t_id}` | `item_id`: `{i_ids}` "
                        f"| `[Fn {fn_name}: L{fn_s}..L{fn_e} | Tupla: L{tup_s}..L{tup_e}]`"
                    )
                    loc_blocks.append(f"  - **Descripción:** {s_loc.get('description')}")
                    loc_blocks.append(f"  - **Causa:** {s_loc.get('cause')}")
                    loc_blocks.append(f"  - **Acción:** {s_loc.get('action')}")
                    code_lns = [
                        (f"{cl[0]}: {cl[1]}" if isinstance(cl, (list, tuple)) and len(cl) >= 2 else str(cl))
                        for cl in (s_loc.get("offending_code_lines") or [])
                    ]
                    if code_lns:
                        loc_blocks.append("  - **CONTEXTO EXACTO (OFFENDING LINES):**\n    ```python\n    " + "\n    ".join(code_lns[:10]) + "\n    ```")
                error_bullets += "\n".join(loc_blocks) + "\n\n"

            prompt_text = (
                f"# Asignación de Tarea: Targeted Repair Engineer `{cid}` (C2C v3.21 Load Inversion)\n\n"
                f"{scope_header}\n\n"
                f"## 1. REPARACIÓN ASIGNADA\n"
                f"- **Competencia Afectada:** `{cid}`\n"
                f"- **Shard Asociado:** `{shard_id}`\n"
                f"- **Archivo Python Objetivo:** `{out_py}`\n"
                f"- **Destino JSON Final:** `{out_json}`\n"
                f"- **Módulo de Parche Quirúrgico:** `{shard_fix_path}`\n"
                f"- **Competence Slice (< 2 KB):** `{slice_rel}`\n"
                f"- **Circuit Breaker Reset:** Se han limpiado automáticamente los contadores previos en `.check_attempts/`.\n\n"
                f"## 2. DIAGNÓSTICO DEL FALLO & COMPETENCE SLICE\n"
                f"{error_bullets}"
                f"Consulta el slice de competencia en `{slice_rel}` con `read_file` para ver la especificación completa.\n\n"
                f"## 3. INSTRUCCIONES DE REPARACIÓN (MATRIZ 2D)\n"
                f"1. **Matriz 2D (edita antes de compilar):** Con < 6 errores (sin SyntaxError) usa `edit_file` quirúrgico sobre `{out_py}`; con >= 6 errores escribe módulo en `{shard_fix_path}` (reglas Form-C `min_archetypes=4` en tu SystemPrompt `c2c_repair`).\n"
                f"2. **Compila tras editar:** `{compile_cmd}`\n"
                f"3. **Post-PASS Cut:** Cierre al aprobar: `{out_json}` (señal terminal DONE).\n"
            )
            item_file = items_dir / f"repair_{idx:02d}.json"
            cid_item_file = items_dir / f"repair_{safe_cid}.json"
            items_cid_norm_file = items_dir / f"repair_{cid_norm}.json"
            prompts_cid_file = prompts_repair_dir / f"repair_{cid_norm}.json"
            prompts_safe_file = prompts_repair_dir / f"repair_{safe_cid}.json"
            prompts_idx_file = prompts_repair_dir / f"repair_{idx:02d}.json"

            prompt_sha256 = hashlib.sha256(prompt_text.encode("utf-8")).hexdigest()
            work_order_meta = {
                "role": f"Repair Engineer {cid}",
                "shard_id": shard_id,
                "competency_id": cid,
                "output_python": out_py,
                "output_json": out_json,
                "compile_cmd": compile_cmd,
                "compile_command": compile_cmd,
                "min_archetypes": 4,
                "repair_slice": slice_rel,
                "prompt_sha256": prompt_sha256,
            }
            item_data = {
                "TypeName": spec["type_name"],
                "Role": f"Repair Engineer {cid}",
                "Model": spec["model"],
                "competency_id": cid,
                "assigned_competency": cid,
                "shard_id": shard_id,
                "output_python": out_py,
                "output_json": out_json,
                "compile_cmd": compile_cmd,
                "compile_command": compile_cmd,
                "min_archetypes": 4,
                "diagnostics": diag,
                "Prompt": prompt_text,
                "work_order": work_order_meta,
            }
            item_json_str = json.dumps(item_data, indent=2, ensure_ascii=False)
            item_file.write_text(item_json_str, encoding="utf-8")
            cid_item_file.write_text(item_json_str, encoding="utf-8")
            items_cid_norm_file.write_text(item_json_str, encoding="utf-8")
            prompts_cid_file.write_text(item_json_str, encoding="utf-8")
            prompts_safe_file.write_text(item_json_str, encoding="utf-8")
            prompts_idx_file.write_text(item_json_str, encoding="utf-8")

            # Pure-data payload file for live Repair Engineer (zero wrapper bloat)
            rec_mods_str = ", ".join(str(m) for m in (comp_info.get("recommended_modalities") or []))
            mods_meta_line = (
                f"- **Modalidades recomendadas (CTA Architect, K={eff_repair_k}/modalidad activa, 0 MC7 en Skill, <=1 MC7 en Concept/Fact):** {rec_mods_str}\n"
                if rec_mods_str
                else f"- **Modalidades recomendadas (CTA Architect, K={eff_repair_k}):** libre según criterio epistémico sin cuotas rígidas\n"
            )
            prompts_cid_data_file = prompts_repair_dir / f"repair_{cid_norm}_data.md"
            repair_data_md = (
                f"# Repair `{cid}` (`{shard_id}`)\n\n"
                f"{mods_meta_line}"
                f"- **Comando compile:** `{compile_cmd}`\n\n"
                f"## 2. DIAGNÓSTICO DEL FALLO & COMPETENCE SLICE\n"
                f"{error_bullets}"
                f"Consulta el slice de competencia en `{slice_abs}` con `read_file` para ver la especificación completa.\n"
            )
            prompts_cid_data_file.write_text(repair_data_md, encoding="utf-8")

            inline_item_data = dict(item_data)
            inline_item_data["Prompt"] = prompt_text.replace(disk_done_signal, f"DONE: {out_json}").replace(
                f"Cierre al aprobar: `{out_json}` (señal terminal DONE).",
                f"DONE: {out_json}",
            )

            entry_record = {
                "cid": cid,
                "cid_norm": cid_norm,
                "safe_cid": safe_cid,
                "shard_id": shard_id,
                "out_py": out_py,
                "out_json": out_json,
                "shard_fix_path": shard_fix_path,
                "slice_rel": slice_rel,
                "slice_abs": slice_abs,
                "compile_cmd": compile_cmd,
                "prompts_cid_file": prompts_cid_file,
                "prompts_cid_data_file": prompts_cid_data_file,
                "repair_data_md": repair_data_md,
                "item_file": item_file,
                "item_data": item_data,
                "inline_item_data": inline_item_data,
                "error_bullets": error_bullets,
                "diag": diag,
            }
            shard_repair_groups.setdefault(shard_id, []).append(entry_record)
            per_cid_entries.append(entry_record)

            dispatched_ids.append(cid)
            item_files.append(prompts_cid_file.resolve().as_posix())
            if item_file.resolve().as_posix() not in item_files:
                item_files.append(item_file.resolve().as_posix())

        def _bounded_repair_pointer(role_label: str, w_rel_path: str, done_sig: str, extra_opts: List[str]) -> str:
            cand = ""
            for ext in extra_opts:
                cand = make_pointer_prompt(
                    role_name=role_label,
                    work_order_rel=w_rel_path,
                    done_signal=done_sig,
                    extra_instructions=ext if ext else None,
                )
                if len(cand.encode("utf-8")) <= 650:
                    return cand
            logger.warning(
                "Repair pointer prompt exceeds 650 bytes (%d B) due to long work_rel: %s",
                len(cand.encode("utf-8")),
                w_rel_path,
            )
            return cand

        for shard_id, group_entries in shard_repair_groups.items():
            if len(group_entries) == 1:
                ent = group_entries[0]
                if use_pointer:
                    w_abs = ent["prompts_cid_data_file"].resolve().as_posix()
                    slice_abs_ent = ent["slice_abs"]
                    out_py_abs = _resolve_posix_path(work, work_rel, ent["out_py"])
                    fix_abs = _resolve_posix_path(work, work_rel, ent["shard_fix_path"])
                    extra_full = (
                        f"[SCOPE-LOCK] READ: `{w_abs}`, `{slice_abs_ent}`, `{out_py_abs}`; "
                        f"WRITE: `{out_py_abs}`, `{fix_abs}`; COMPILE: `.agents/skills/content-to-course/compile_shard.py`."
                    )
                    extra_mid = (
                        f"[SCOPE-LOCK] READ: `{w_abs}`, `{slice_abs_ent}`; "
                        f"WRITE: `{out_py_abs}`; COMPILE: `.agents/skills/content-to-course/compile_shard.py`."
                    )
                    pointer_prompt = _bounded_repair_pointer(
                        role_label=f"Repair Engineer {ent['cid']}",
                        w_rel_path=w_abs,
                        done_sig=f"DONE: {ent['out_json']}",
                        extra_opts=[extra_full, extra_mid],
                    )
                    sub_item = {
                        "TypeName": spec["type_name"],
                        "Role": f"Repair Engineer {ent['cid']}",
                        "Model": spec["model"],
                        "shard_id": shard_id,
                        "assigned_competencies": [ent["cid"]],
                        "assigned_competency": ent["cid"],
                        "Prompt": pointer_prompt,
                    }
                else:
                    sub_item = dict(ent["inline_item_data"])
                subagents.append(sub_item)
            else:
                cids_in_shard = [e["cid"] for e in group_entries]
                cids_label = ", ".join(cids_in_shard)
                out_py = group_entries[0]["out_py"]
                out_json = group_entries[0]["out_json"]
                compile_cmd = group_entries[0]["compile_cmd"]
                w_rels = [f"{work_rel}/prompts/repair/{e['prompts_cid_file'].name}" for e in group_entries]
                slice_rels = [e["slice_rel"] for e in group_entries]
                fix_paths = [e["shard_fix_path"] for e in group_entries]
                combined_prompts = "\n\n---\n\n".join(e["inline_item_data"]["Prompt"] for e in group_entries)

                consolidated_data_file = prompts_repair_dir / f"repair_{shard_id}_data.md"
                combined_data_md = "\n\n---\n\n".join(e["repair_data_md"] for e in group_entries)
                _atomic_write_text(consolidated_data_file, combined_data_md)

                consolidated_prompt_file = prompts_repair_dir / f"repair_{shard_id}.json"
                consolidated_item_file = items_dir / f"repair_{shard_id}.json"
                consolidated_order = {
                    "TypeName": spec["type_name"],
                    "Role": f"Repair Engineer {shard_id} ({cids_label})",
                    "Model": spec["model"],
                    "shard_id": shard_id,
                    "assigned_competencies": cids_in_shard,
                    "assigned_competency": cids_label,
                    "output_python": out_py,
                    "output_json": out_json,
                    "compile_cmd": compile_cmd,
                    "compile_command": compile_cmd,
                    "min_archetypes": 4,
                    "competency_work_orders": w_rels,
                    "repair_slices": slice_rels,
                    "shard_fix_paths": fix_paths,
                    "diagnostics": {e["cid"]: e["diag"] for e in group_entries},
                    "Prompt": combined_prompts,
                }
                consolidated_json_str = json.dumps(consolidated_order, indent=2, ensure_ascii=False)
                _atomic_write_text(consolidated_prompt_file, consolidated_json_str)
                _atomic_write_text(consolidated_item_file, consolidated_json_str)
                cons_resolved = consolidated_prompt_file.resolve().as_posix()
                if cons_resolved not in item_files:
                    item_files.append(cons_resolved)

                if use_pointer:
                    w_abs = consolidated_data_file.resolve().as_posix()
                    out_py_abs = _resolve_posix_path(work, work_rel, out_py)
                    fix_dir_abs = (work / "shards" / "shard_fixes" / shard_id).resolve().as_posix()
                    cid_data_names = ", ".join(e["prompts_cid_data_file"].name for e in group_entries)
                    extra_full = (
                        f"[SCOPE-LOCK] READ: `{w_abs}` ({cid_data_names}), `{out_py_abs}`; "
                        f"WRITE: `{out_py_abs}`, `{fix_dir_abs}/*.py`; COMPILE: `.agents/skills/content-to-course/compile_shard.py`."
                    )
                    extra_mid = (
                        f"[SCOPE-LOCK] READ: `{w_abs}`; "
                        f"WRITE: `{out_py_abs}`; COMPILE: `.agents/skills/content-to-course/compile_shard.py`."
                    )
                    pointer_prompt = _bounded_repair_pointer(
                        role_label=f"Repair Engineer {shard_id}",
                        w_rel_path=w_abs,
                        done_sig=f"DONE: {out_json}",
                        extra_opts=[extra_full, extra_mid],
                    )
                    sub_item = {
                        "TypeName": spec["type_name"],
                        "Role": f"Repair Engineer {shard_id} ({cids_label})",
                        "Model": spec["model"],
                        "shard_id": shard_id,
                        "assigned_competencies": cids_in_shard,
                        "assigned_competency": cids_label,
                        "Prompt": pointer_prompt,
                    }
                else:
                    sub_item = dict(consolidated_order)
                subagents.append(sub_item)

    dispatched_at = datetime.now(timezone.utc).isoformat()
    payload = {"dispatched_at": dispatched_at, "Subagents": subagents, "item_files": item_files}

    snap = snapshot_work_dir(work)
    snap_file = dispatch_dir / f"{role}_snapshot.json"
    snap_payload = {k: list(v) for k, v in snap.items()}
    _atomic_write_text(snap_file, json.dumps(snap_payload, indent=2, ensure_ascii=False))

    audit_file = dispatch_dir / f"{role}.json"
    audit_payload = {
        "role": role,
        "dispatched_at": dispatched_at,
        "subagents_count": len(subagents),
        "item_files": item_files,
        "Subagents": subagents,
    }
    _atomic_write_text(audit_file, json.dumps(audit_payload, indent=2, ensure_ascii=False))

    state.setdefault("dispatched", {})[role] = list(sorted(set(dispatched_ids)))
    _atomic_write_text(state_file, json.dumps(state, indent=2, ensure_ascii=False))

    return payload


def dispatch_repair(
    work_dir: Union[str, Path],
    ids: Optional[List[Union[str, int]]] = None,
    pointer: bool = False,
) -> Dict[str, Any]:
    """Generates dispatch payload and individual item files for Targeted Repair Engineers (Load Inversion v3.21)."""
    return build_dispatch(role="repair", work_dir=work_dir, ids=ids, pointer=pointer)


def pre_stage5_cleanup(work_dir: Union[str, Path]) -> Dict[str, Any]:
    """Protocol for clearing stale/errored subagents prior to Stage 5 verification (P4 / R5 SLA).
    
    Instructs the Director to execute manage_subagents(kill_all) so that stale 429
    or aborted subagent entries do not mislead Stage 5 decisions. Also cleans up
    transient failure markers in state.json.
    """
    work = Path(work_dir).resolve()
    from budget_guard import update_state_checkpoint, load_state_checkpoint

    state = load_state_checkpoint(work)
    subagents = state.get("subagents", {})
    cleared = []
    for s_name, s_info in list(subagents.items()):
        if isinstance(s_info, dict) and s_info.get("status") in ("errored", "aborted"):
            s_info["status"] = "purged_pre_stage5"
            cleared.append(s_name)

    state["subagents"] = subagents
    _atomic_write_text(work / "state.json", json.dumps(state, indent=2, ensure_ascii=False))
    update_state_checkpoint(work, "pre_stage5_cleanup", "completed", metadata={"purged_subagents": cleared})
    msg = (
        "[+] Pre-Stage-5 Cleanup executed.\n"
        "    SLA Requirement: Run `manage_subagents(Action='kill_all')` before dispatching Stage 5 judges.\n"
        f"    Purged {len(cleared)} stale subagent error records."
    )
    return {"status": "ok", "purged": cleared, "message": msg}


def snapshot_work_dir(work_dir: Union[str, Path]) -> Dict[str, Tuple[int, float]]:
    """Takes a snapshot of all files and their sizes/mtimes in work_dir."""
    work = Path(work_dir).resolve()
    snapshot: Dict[str, Tuple[int, float]] = {}
    if not work.is_dir():
        return snapshot

    for root, _, files in os.walk(work):
        root_path = Path(root)
        for fname in files:
            fpath = root_path / fname
            try:
                st = fpath.stat()
                rel = fpath.relative_to(work).as_posix()
                snapshot[rel] = (st.st_size, st.st_mtime)
            except OSError:
                pass
    return snapshot


def _is_allowed_path(rel_path: str, role: str) -> bool:
    """Checks whether rel_path is an allowed write destination for the specified role."""
    norm = rel_path.replace("\\", "/").lstrip("/")
    norm_role = _normalize_role(role)

    if (
        norm.startswith("dispatch/")
        or norm.startswith("work/dispatch/")
        or norm in ("timings.json", "work/timings.json", "order.json", "work/order.json")
        or "/__pycache__/" in f"/{norm}/"
        or norm.endswith(".pyc")
        or norm.endswith(".cert.json")
        or norm.startswith(".pytest_cache/")
        or norm.startswith(".git/")
        # Pipeline-internal artifacts written by the orchestrator/check tooling, not by subagents
        or norm.startswith(".check_attempts/")
        or norm.startswith("logs/")
        or norm.startswith("telemetry/")
        or norm.startswith("prompts/")
        or norm.startswith(".c2c_")
        or (
            norm_role in ("cta", "cta-direct", "cta-map", "cta-reduce")
            and ("cta_fixes/" in norm or norm.startswith("cta_fixes/"))
            and norm.endswith(".py")
        )
    ):
        return True

    spec = ROLE_SPECS.get(norm_role)
    if not spec:
        return False

    write_patterns = spec.get("write", [])
    candidates = [norm]
    if norm.startswith("work/"):
        candidates.append(norm[5:])
    else:
        candidates.append(f"work/{norm}")

    for pattern in write_patterns:
        pat_clean = pattern.replace("\\", "/").lstrip("/")
        pat_candidates = [pat_clean]
        if pat_clean.startswith("work/"):
            pat_candidates.append(pat_clean[5:])
        else:
            pat_candidates.append(f"work/{pat_clean}")

        for cand in candidates:
            for pat in pat_candidates:
                if fnmatch.fnmatch(cand, pat):
                    return True
                wildcard_pat = re.sub(r"<[^>]+>", "*", pat)
                wildcard_pat = re.sub(r"_XX\b", "_*", wildcard_pat)
                wildcard_pat = re.sub(r"XX\b", "*", wildcard_pat)
                if fnmatch.fnmatch(cand, wildcard_pat):
                    return True

    return False


def scope_check(
    work_dir: Union[str, Path],
    role: str,
    snapshot: Optional[Dict[str, Tuple[int, float]]] = None,
) -> Tuple[bool, List[str]]:
    """Detects files created or modified outside the permitted write paths for role."""
    work = Path(work_dir).resolve()
    norm_role = _normalize_role(role)
    if not snapshot:
        cand_snaps = [work / "dispatch" / f"{norm_role}_snapshot.json"]
        if role and role != norm_role:
            cand_snaps.append(work / "dispatch" / f"{role}_snapshot.json")
        for snap_file in cand_snaps:
            if snap_file.is_file():
                try:
                    raw_snap = json.loads(snap_file.read_text(encoding="utf-8"))
                    snapshot = {k: (v[0], v[1]) for k, v in raw_snap.items()}
                    break
                except Exception as e:
                    logger.warning("Could not load snapshot file %s: %s", snap_file, e)
    if snapshot is None:
        snapshot = {}

    current_snapshot = snapshot_work_dir(work)
    violations: List[str] = []

    for rel_path, (size, mtime) in current_snapshot.items():
        if rel_path not in snapshot:
            if not _is_allowed_path(rel_path, norm_role):
                violations.append(rel_path)
        else:
            old_size, old_mtime = snapshot[rel_path]
            if (size, mtime) != (old_size, old_mtime):
                if not _is_allowed_path(rel_path, norm_role):
                    violations.append(rel_path)

    violations.sort()
    is_clean = len(violations) == 0
    return is_clean, violations


def main() -> None:
    """CLI utility for subagent dispatch and scope checking."""
    # Backward-compatible fallback: if invoked as `dispatch.py --role <role> ...` without subcommand, route to `build`
    if len(sys.argv) > 1 and sys.argv[1].startswith("--"):
        if any(arg == "--role" or arg.startswith("--role=") for arg in sys.argv[1:]):
            sys.argv = [sys.argv[0], "build"] + sys.argv[1:]

    parser = argparse.ArgumentParser(description="Subagent Scope-Lock & Dispatch Generator (C2C v3.2)")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # dispatch subcommand
    disp = subparsers.add_parser("build", help="Generate invoke_subagent payload for role")
    disp.add_argument("--role", required=True, choices=list(ROLE_SPECS.keys()), help="Subagent role")
    disp.add_argument("--work-dir", required=True, help="Course working directory")
    disp.add_argument("--ready-only", action="store_true", help="Dispatch only ready sections")
    disp.add_argument("--ids", "--failed-cid", nargs="*", dest="ids", help="Optional specific IDs to dispatch")
    disp.add_argument("--wave", "--wave-index", type=int, default=None, dest="wave", help="Wave index for author dispatch")
    disp.add_argument("--pointer", action="store_true", default=True, help="Generate pointer-prompt work orders referencing disk JSON (default: True)")
    disp.add_argument("--no-pointer", action="store_false", dest="pointer", help="Disable pointer-prompt work orders")

    # check subcommand
    chk = subparsers.add_parser("check", help="Run scope violation check")
    chk.add_argument("--role", required=True, choices=list(ROLE_SPECS.keys()), help="Subagent role")
    chk.add_argument("--work-dir", required=True, help="Course working directory")

    # define-types subcommand
    dt = subparsers.add_parser("define-types", help="Print and persist define_subagent payloads for all c2c types")
    dt.add_argument("--work-dir", default=None, help="Optional course working directory to persist type files")
    dt.add_argument("--lean", action="store_true", default=True, help="Use lean static system prompts (<= 5 KB, default: True)")
    dt.add_argument("--full-prompts", "--no-lean", action="store_false", dest="lean", help="Use full uncompressed system prompts (opt-out of lean)")

    # dispatch-cta subcommand
    dc = subparsers.add_parser("dispatch-cta", help="Dispatch CTA Architect using pre_cta_manifest.json")
    dc.add_argument("--work-dir", required=True, help="Course working directory")
    dc.add_argument("--mode", default=None, help="CTA mode: direct or mapreduce")
    dc.add_argument("--pointer", action="store_true", default=True, help="Generate pointer-prompt work orders (default: True)")
    dc.add_argument("--no-pointer", action="store_false", dest="pointer", help="Disable pointer-prompt work orders")

    # dispatch-cta-reduce subcommand
    dcr = subparsers.add_parser("dispatch-cta-reduce", help="Dispatch CTA Harmonizer for MapReduce reduction")
    dcr.add_argument("--work-dir", required=True, help="Course working directory")
    dcr.add_argument("--pointer", action="store_true", default=True, help="Generate pointer-prompt work orders (default: True)")
    dcr.add_argument("--no-pointer", action="store_false", dest="pointer", help="Disable pointer-prompt work orders")

    # dispatch-authors subcommand
    da = subparsers.add_parser("dispatch-authors", help="Dispatch Shard Authors using pre_shard_manifest.json")
    da.add_argument("--work-dir", required=True, help="Course working directory")
    da.add_argument("--wave", "--wave-index", type=int, default=None, dest="wave", help="Wave index to filter author dispatch")
    da.add_argument("--ids", nargs="*", default=None, help="Optional specific shard or competency IDs to filter author dispatch")
    da.add_argument("--pointer", action="store_true", default=True, help="Generate pointer-prompt work orders (default: True)")
    da.add_argument("--no-pointer", action="store_false", dest="pointer", help="Disable pointer-prompt work orders")

    # dispatch-judges subcommand
    dj = subparsers.add_parser("dispatch-judges", help="Dispatch Blind Judges with Zero-Warmup in-prompt payload")
    dj.add_argument("--work-dir", required=True, help="Course working directory")
    dj.add_argument("--pointer", action="store_true", default=True, help="Generate pointer-prompt work orders (default: True)")
    dj.add_argument("--no-pointer", action="store_false", dest="pointer", help="Disable pointer-prompt work orders")
    dj.add_argument("--ready-only", action="store_true", default=False, help="Dispatch only ready evaluated items")
    dj.add_argument("--ids", nargs="*", default=None, help="Target competency IDs to arbitrate (default: all)")
    dj.add_argument("--max-items-per-judge", type=int, default=12, help="Maximum items per judge batch (default: 12)")

    # dispatch-repair subcommand
    dr = subparsers.add_parser("dispatch-repair", help="Dispatch Targeted Repair Engineers")
    dr.add_argument("--work-dir", required=True, help="Course working directory")
    dr.add_argument("--ids", "--failed-cid", nargs="*", dest="ids", help="Optional specific IDs to repair")
    dr.add_argument("--pointer", action="store_true", default=True, help="Generate pointer-prompt work orders (default: True)")
    dr.add_argument("--no-pointer", action="store_false", dest="pointer", help="Disable pointer-prompt work orders")

    # checkpoint subcommand
    cp = subparsers.add_parser("checkpoint", help="Record stage checkpoint in state.json")
    cp.add_argument("--work-dir", required=True, help="Course working directory")
    cp.add_argument("--stage", required=True, help="Pipeline stage name")
    cp.add_argument("--status", default="completed", help="Status of stage (completed/in_progress/failed)")

    # cleanup-subagents subcommand
    cl = subparsers.add_parser("cleanup-subagents", help="Execute Pre-Stage-5 subagent cleanup protocol")
    cl.add_argument("--work-dir", required=True, help="Course working directory")

    # status subcommand
    st = subparsers.add_parser("status", help="Read state.json and show pipeline progress")
    st.add_argument("--work-dir", required=True, help="Course working directory")

    args = parser.parse_args()

    if args.action == "define-types":
        target_work = args.work_dir or Path.cwd() / "work"
        res = generate_define_subagent_specs(target_work, lean=args.lean)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "dispatch-cta":
        res = dispatch_cta(args.work_dir, mode=args.mode, pointer=args.pointer)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "dispatch-cta-reduce":
        res = dispatch_cta_reduce(args.work_dir, pointer=args.pointer)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "dispatch-authors":
        res = dispatch_authors(args.work_dir, pointer=args.pointer, wave_index=args.wave, ids=args.ids)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "dispatch-judges":
        res = dispatch_judges(args.work_dir, pointer=args.pointer, max_items_per_judge=args.max_items_per_judge, ready_only=args.ready_only, ids=args.ids)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "dispatch-repair":
        res = dispatch_repair(args.work_dir, ids=args.ids, pointer=args.pointer)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "checkpoint":
        from budget_guard import update_state_checkpoint
        state = update_state_checkpoint(args.work_dir, args.stage, args.status)
        print(json.dumps(state, indent=2, ensure_ascii=False))

    elif args.action == "cleanup-subagents":
        res = pre_stage5_cleanup(args.work_dir)
        print(json.dumps(res, indent=2, ensure_ascii=False))

    elif args.action == "status":
        from budget_guard import load_state_checkpoint
        state = load_state_checkpoint(args.work_dir)
        print(json.dumps(state, indent=2, ensure_ascii=False))

    elif args.action == "build":
        payload = build_dispatch(
            role=args.role,
            work_dir=args.work_dir,
            ids=args.ids,
            ready_only=args.ready_only,
            pointer=args.pointer,
            wave_index=args.wave,
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False))

    elif args.action == "check":
        is_clean, violations = scope_check(args.work_dir, args.role, None)
        if is_clean:
            print(f"[+] Scope-check PASSED for role '{args.role}'.")
            sys.exit(0)
        else:
            print(f"[-] Scope-check FAILED for role '{args.role}'. {len(violations)} violations detected:")
            for v in violations:
                print(f"    * {v}")
            sys.exit(1)


if __name__ == "__main__":
    main()


