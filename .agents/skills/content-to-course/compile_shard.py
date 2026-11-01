"""Deterministic Python Tuple Compiler for Content-to-Course v3.2 Shard Authors.

Compiles work/shards/<shard_id>_data.py into canonical template JSON files in < 100 ms:
- Zero-fallback strict check of work/shards/pre_shard_manifest.json (BLOCKER on missing)
- AST-level Line Locator (ShardDataLineLocator) tracking exact line ranges, constants, and helper functions
- Dual-signature support (direct CLI, run.py stage 3 subprocess, and Python module imports)
- Clean Python callable to AST string extraction with preamble constants/helpers injection
- Intelligent tuple format unpacking supporting both prompt_shard_author.md examples and v3.2 canonical tuples
- Robust MC7 distractor completion and stem variant diversification ensuring 0 errors on H-01 & H-02
- Atomic, race-condition-free file writes and isolated .check_attempts per shard_id
- Strict dry-run validation (20 seeds) with surgical line-mapped diagnostics
"""

import argparse
import ast
import hashlib
import importlib.util
import inspect
import json
import os
import re
import sys
import textwrap
import traceback
import types
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

# Ensure skill root is in sys.path
_skill_root = Path(__file__).parent.resolve()
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))


def _atomic_write_json(target_path: Path, data: Any) -> None:
    """Safely write JSON payload to file using atomic rename to prevent race conditions."""
    from check_templates import heal_control_chars_in_obj
    data = heal_control_chars_in_obj(data)
    target_path = Path(target_path).resolve()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = target_path.with_name(f".{target_path.name}.tmp.{os.getpid()}_{uuid.uuid4().hex[:8]}")
    payload_str = json.dumps(data, indent=2, ensure_ascii=False)
    tmp_path.write_text(payload_str, encoding="utf-8")
    try:
        os.replace(tmp_path, target_path)
    except Exception:
        try:
            if target_path.is_file():
                target_path.unlink()
            os.replace(tmp_path, target_path)
        except Exception:
            target_path.write_text(payload_str, encoding="utf-8")
            if tmp_path.is_file():
                try:
                    tmp_path.unlink()
                except Exception:
                    pass


def count_distinct_shard_error_hunks(
    raw_errors: List[Any],
    targets: Optional[List[Path]] = None,
    shard_py: Optional[Union[str, Path]] = None,
) -> int:
    """Helper re-exported from check_templates for counting deduplicated error hunks."""
    from check_templates import count_distinct_shard_error_hunks as _count_hunks
    return _count_hunks(raw_errors, targets=targets, shard_py=shard_py)


def check_ast_rf_triple_braces(source_text: str) -> List[str]:
    """Check for rf'...' or fr'...' strings containing '{{{' which corrupts KaTeX braces."""
    warnings = []
    for m in re.finditer(r"(?i)\b(rf|fr)(['\"]{1,3})([\s\S]*?)\2", source_text):
        if "{{{" in m.group(3):
            snippet = m.group(0)[:60] + ("..." if len(m.group(0)) > 60 else "")
            warnings.append(
                f"[!] Warning: Se detectó {m.group(1)}{m.group(2)}...{m.group(2)} conteniendo '{{{{{{' ({snippet}). "
                "Recomendación: Utilice raw strings r\"...\" con tokens @var@ para evitar la corrupción de llaves KaTeX."
            )
    return warnings


def heal_shard_source_text(source_text: str) -> Tuple[bool, str]:
    """Uses Python's tokenize module to inspect and heal non-raw string tokens and control characters in-memory.

    Heals unescaped LaTeX prefixes and ASCII control characters without modifying files on disk.
    Returns (modified, healed_text).
    """
    if not source_text:
        return False, source_text
    try:
        import io, tokenize
        from check_templates import heal_control_chars_in_str, COMBINED_LATEX
        clean_source = heal_control_chars_in_str(source_text)
        modified = (clean_source != source_text)
        tokens = list(tokenize.tokenize(io.BytesIO(clean_source.encode("utf-8")).readline))
        new_tokens = []
        for t in tokens:
            if t.type == tokenize.STRING:
                m = re.match(r"^([a-zA-Z]*)(['\"]{1,3})(.*)(['\"]{1,3})$", t.string, flags=re.DOTALL)
                if m:
                    prefix, q_open, body, q_close = m.groups()
                    is_raw = "r" in prefix.lower()
                    new_body = heal_control_chars_in_str(body)
                    if not is_raw:
                        new_body = re.sub(rf"(?<!\\)\\({COMBINED_LATEX})", r"\\\\\1", new_body)
                    else:
                        new_body = re.sub(r"(?<!\\)(?:\\\\)+([a-zA-Z]+)", r"\\\1", new_body)
                    if "$" in new_body:
                        _bs = r"\\" if is_raw else r"\\\\"
                        new_body = re.sub(r"(?<!\\)\\+centernot\s*\{?\s*\\+(?:Rightarrow|implies)\b\s*\}?", f"{_bs}nRightarrow", new_body)
                        new_body = re.sub(r"(?<!\\)\\+implies\b", f"{_bs}Rightarrow", new_body)
                        new_body = re.sub(r"(?<!\\)\\+iff\b", f"{_bs}Leftrightarrow", new_body)
                        new_body = re.sub(r"(?<!\\)\b(hat|bar|tilde|vec|dot|ddot|frac|dfrac|tfrac|sqrt|mathcal|mathbb|mathbf|boldsymbol|operatorname)\s*\{", rf"{_bs}\1{{", new_body)
                        if new_body.count("$$") == 1 and new_body.replace("$$", "").count("$") == 1:
                            new_body = new_body.replace("$$", "$")
                    if new_body != body:
                        modified = True
                        new_tokens.append(tokenize.TokenInfo(t.type, f"{prefix}{q_open}{new_body}{q_close}", t.start, t.end, t.line))
                        continue
            new_tokens.append(t)
        if not modified:
            return False, source_text
        rebuilt_text = tokenize.untokenize(new_tokens).decode("utf-8")
        return True, rebuilt_text
    except Exception:
        try:
            from check_templates import heal_control_chars_in_str, COMBINED_LATEX
            healed = heal_control_chars_in_str(source_text)
            has_raw = bool(re.search(r'\br["\']', source_text, re.IGNORECASE))
            if not has_raw:
                healed = re.sub(rf"(?<!\\)\\({COMBINED_LATEX})", r"\\\\\1", healed)
            return (healed != source_text), healed
        except Exception:
            return False, source_text


def heal_shard_source_file(py_path: Path) -> bool:
    """Uses Python's tokenize module to inspect and heal non-raw string tokens and control characters.

    Heals unescaped LaTeX prefixes and ASCII control characters in py_path before importing.
    Returns True if the file was modified and rewritten, False otherwise.
    """
    if not py_path.is_file():
        return False
    source_text = py_path.read_text(encoding="utf-8")
    modified, healed = heal_shard_source_text(source_text)
    if modified:
        py_path.write_text(healed, encoding="utf-8")
    return modified


def is_trivial_verifier(ver_code: str, ver_fn_callable: Any = None) -> Tuple[bool, str]:
    """Inspect AST of verifier code to reject trivial verifiers like constant 'return True'."""
    if not ver_code or not ver_code.strip():
        return True, "verifier code is empty"
    clean_ver_code = textwrap.dedent(ver_code.strip())
    try:
        tree = ast.parse(clean_ver_code)
    except Exception as e:
        return True, f"verifier code syntax error: {e}"

    fn_node = None
    target_names = {"verify", "cross_check"}
    if ver_fn_callable and hasattr(ver_fn_callable, "__name__"):
        target_names.add(ver_fn_callable.__name__)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name in target_names:
                fn_node = node
                break
    if not fn_node:
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fn_node = node
                break

    if not fn_node:
        return True, "no function definition found in verifier code"

    body_stmts = [
        s for s in fn_node.body
        if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))
    ]

    if not body_stmts:
        return True, "verifier function body has no operational statements"

    # Single return constant (e.g. return True, return 1, or return None)
    if len(body_stmts) == 1 and isinstance(body_stmts[0], ast.Return):
        ret_val = body_stmts[0].value
        if isinstance(ret_val, ast.Constant):
            return True, f"returns constant '{ret_val.value}' without evaluating conditions"
        if ret_val is None:
            return True, "returns None without evaluating conditions"

    # Check if first argument (instance / res) is ever loaded in operational statements
    arg_names = [a.arg for a in (getattr(fn_node.args, "posonlyargs", []) + fn_node.args.args + getattr(fn_node.args, "kwonlyargs", []))]
    if arg_names:
        first_arg = arg_names[0]
        used_arg = False
        for s in body_stmts:
            for sub in ast.walk(s):
                if isinstance(sub, ast.Name) and sub.id == first_arg and isinstance(sub.ctx, ast.Load):
                    used_arg = True
                    break
            if used_arg:
                break
        if not used_arg:
            return True, f"argument '{first_arg}' is never inspected in verifier function body"

    return False, ""


def normalize_double_braces(text: str, declared_vars: Optional[Set[str]] = None) -> str:
    r"""Normalize non-variable double curly braces {{token}} -> {token} when token is not a declared variable.

    Protects declared variables so that {var} can still be evaluated, while ensuring LaTeX braces like
    {{0.5}}, {{\operatorname{arccot}}}, {{S_{xy}}} are normalized to {0.5}, {\operatorname{arccot}}, {S_{xy}}
    before R-20 validation.
    """
    if not isinstance(text, str) or "{{" not in text:
        return text

    v_set = declared_vars or set()

    def _normalize_once(s: str) -> str:
        out = []
        i = 0
        n = len(s)
        while i < n:
            if s[i:i+2] == "{{":
                j = i + 2
                depth = 0
                found = False
                while j < n:
                    if s[j:j+2] == "}}" and depth == 0:
                        found = True
                        break
                    elif s[j] == "{":
                        depth += 1
                        j += 1
                    elif s[j] == "}":
                        if depth > 0:
                            depth -= 1
                            j += 1
                        else:
                            break
                    else:
                        j += 1

                if found:
                    token = s[i+2:j]
                    var_name = token.strip().split(":")[0].strip()
                    if v_set and var_name in v_set:
                        out.append(s[i:j+2])
                    else:
                        out.append("{" + token + "}")
                    i = j + 2
                else:
                    out.append(s[i])
                    i += 1
            else:
                out.append(s[i])
                i += 1
        return "".join(out)

    prev = None
    curr = text
    while prev != curr:
        prev = curr
        curr = _normalize_once(curr)
    return curr


def _find_diagnostic_line(
    locator: Optional[Any],
    gen_fn_name: Optional[str],
    orig_idx: int,
    needle: str = "",
) -> int:
    """Finds exact 1-based source line for surgical error diagnostics."""
    if not locator or not hasattr(locator, "lines"):
        return 1
    # 1. Search in generator function lines if gen_fn_name is known
    if gen_fn_name and hasattr(locator, "functions") and gen_fn_name in locator.functions:
        s_fn, e_fn = locator.functions[gen_fn_name]
        if needle:
            n_clean = needle.strip()
            for line_no in range(s_fn, min(e_fn + 1, len(locator.lines) + 1)):
                if n_clean and n_clean in locator.lines[line_no - 1]:
                    return line_no
        return s_fn
    # 2. Search in tuple lines
    if hasattr(locator, "get_tuple_info"):
        t_info = locator.get_tuple_info(orig_idx)
        if t_info:
            s_t = t_info.get("start_line", 1)
            e_t = t_info.get("end_line", s_t)
            if needle:
                n_clean = needle.strip()
                for line_no in range(s_t, min(e_t + 1, len(locator.lines) + 1)):
                    if n_clean and n_clean in locator.lines[line_no - 1]:
                        return line_no
            return s_t
    return 1



class ShardDataLineLocator:
    """AST-based source line tracker for shard_XX_data.py files.

    Extracts precise line ranges for:
    - Syntax errors with exact line and column
    - Top-level constants (Assign, AnnAssign) -> (start_line, end_line)
    - Functions (def gen_*, def ver_*, helpers) -> (start_line, end_line)
    - TEMPLATES list assignment -> list of tuples
    - Each tuple index -> (tuple_start, tuple_end)
    - Each of the 9 tuple elements -> (item_start, item_end)
    - Source snippet extraction for replace_file_content
    """

    def __init__(self, file_path: Union[str, Path], source_text: Optional[str] = None):
        self.file_path = Path(file_path).resolve()
        if source_text is not None:
            self.source_text = source_text
        else:
            self.source_text = self.file_path.read_text(encoding="utf-8") if self.file_path.is_file() else ""
        self.lines = self.source_text.splitlines()
        self.syntax_error: Optional[str] = None
        self.syntax_error_details: Optional[Dict[str, Any]] = None
        self.constants: Dict[str, Tuple[int, int]] = {}
        self.functions: Dict[str, Tuple[int, int]] = {}
        self.helper_functions: Set[str] = set()
        self.top_level_imports: List[Tuple[int, int, str]] = []
        self.tuples: List[Dict[str, Any]] = []
        self.competency_to_tuple_idx: Dict[str, int] = {}
        if self.source_text:
            self.parse_ast()

    def parse_ast(self) -> bool:
        try:
            tree = ast.parse(self.source_text, filename=str(self.file_path))
        except SyntaxError as e:
            lineno = e.lineno or 1
            offset = e.offset or 1
            line_txt = self.lines[lineno - 1] if 0 <= lineno - 1 < len(self.lines) else (e.text or "")
            self.syntax_error = (
                f"SyntaxError en {self.file_path.name} (Línea {lineno}, Columna {offset}): {e.msg}\n"
                f"  {line_txt.strip()}\n"
                f"  Rango: StartLine: {lineno}, EndLine: {lineno}"
            )
            self.syntax_error_details = {
                "line": lineno,
                "offset": offset,
                "msg": e.msg,
                "line_text": line_txt,
                "start_line": lineno,
                "end_line": lineno,
            }
            return False

        # 1. Map top-level imports, functions, and constants
        for node in tree.body:
            if isinstance(node, ast.Import):
                root = node.names[0].name.split(".")[0] if node.names else ""
                end_lineno = getattr(node, "end_lineno", node.lineno)
                self.top_level_imports.append((node.lineno, end_lineno, root))
            elif isinstance(node, ast.ImportFrom):
                root = (node.module or "").split(".")[0]
                end_lineno = getattr(node, "end_lineno", node.lineno)
                self.top_level_imports.append((node.lineno, end_lineno, root))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                end_lineno = getattr(node, "end_lineno", node.lineno)
                self.functions[node.name] = (node.lineno, end_lineno)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id != "TEMPLATES":
                        end_lineno = getattr(node, "end_lineno", node.lineno)
                        self.constants[target.id] = (node.lineno, end_lineno)
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name) and node.target.id != "TEMPLATES":
                    end_lineno = getattr(node, "end_lineno", node.lineno)
                    self.constants[node.target.id] = (node.lineno, end_lineno)

        # 2. Locate TEMPLATES = [...] or TEMPLATES += [...]
        for node in tree.body:
            if isinstance(node, (ast.Assign, ast.AugAssign)):
                target_name = None
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "TEMPLATES":
                            target_name = "TEMPLATES"
                            break
                elif isinstance(node, ast.AugAssign):
                    if isinstance(node.target, ast.Name) and node.target.id == "TEMPLATES":
                        target_name = "TEMPLATES"

                if target_name == "TEMPLATES" and isinstance(node.value, (ast.List, ast.Tuple)):
                    start_idx = len(self.tuples)
                    for elt_offset, elt in enumerate(node.value.elts):
                        tuple_info = self._analyze_tuple_node(elt, start_idx + elt_offset)
                        self.tuples.append(tuple_info)
                        cid = tuple_info.get("competency_id")
                        if cid and cid not in self.competency_to_tuple_idx:
                            self.competency_to_tuple_idx[cid] = start_idx + elt_offset

        # 3. Classify helper functions (any top-level function not directly used as gen/ver in a tuple)
        used_fn_names = set()
        for t in self.tuples:
            if t.get("gen_fn_name"):
                used_fn_names.add(t["gen_fn_name"])
            if t.get("ver_fn_name"):
                used_fn_names.add(t["ver_fn_name"])
        self.helper_functions = set(self.functions.keys()) - used_fn_names

        return True

    def _analyze_tuple_node(self, node: ast.AST, idx: int) -> Dict[str, Any]:
        start_line = getattr(node, "lineno", 1)
        end_line = getattr(node, "end_lineno", start_line)

        info: Dict[str, Any] = {
            "index": idx,
            "start_line": start_line,
            "end_line": end_line,
            "elements": {},
            "competency_id": None,
            "template_id": None,
            "question_type": None,
            "difficulty": None,
            "bloom": None,
            "gen_fn_name": None,
            "ver_fn_name": None,
            "stems_var": None,
            "hints_var": None,
            "sol_var": None,
        }

        if isinstance(node, (ast.Tuple, ast.List)):
            elts = node.elts
            # Strictly Form B 9-tuple: [tpl_id, cid, qtype, gen_fn, ver_fn, diff_bloom, stems, hints, sol]
            element_names = [
                "template_id", "competency_id", "question_type",
                "generator_code", "verifier_code", "difficulty_bloom",
                "stem_variants", "hints", "solution"
            ]

            for e_idx, elt in enumerate(elts):
                if e_idx < len(element_names):
                    name = element_names[e_idx]
                    e_start = getattr(elt, "lineno", start_line)
                    e_end = getattr(elt, "end_lineno", e_start)
                    info["elements"][name] = {
                        "start_line": e_start,
                        "end_line": e_end,
                        "node_type": type(elt).__name__,
                    }
                    if name == "competency_id" and isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                        info["competency_id"] = elt.value
                    elif name == "template_id" and isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                        info["template_id"] = elt.value
                    elif name == "question_type" and isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                        info["question_type"] = elt.value.strip().lower()
                    elif name == "difficulty_bloom" and isinstance(elt, (ast.Tuple, ast.List)) and len(elt.elts) >= 2:
                        d_elt, b_elt = elt.elts[0], elt.elts[1]
                        if isinstance(d_elt, ast.Constant) and isinstance(d_elt.value, str):
                            info["difficulty"] = d_elt.value.strip().lower()
                        if isinstance(b_elt, ast.Constant) and isinstance(b_elt.value, str):
                            info["bloom"] = b_elt.value.strip()
                    elif name == "generator_code" and isinstance(elt, ast.Name):
                        info["gen_fn_name"] = elt.id
                    elif name == "verifier_code" and isinstance(elt, ast.Name):
                        info["ver_fn_name"] = elt.id
                    elif name == "stem_variants" and isinstance(elt, ast.Name):
                        info["stems_var"] = elt.id
                    elif name == "hints" and isinstance(elt, ast.Name):
                        info["hints_var"] = elt.id
                    elif name == "solution" and isinstance(elt, ast.Name):
                        info["sol_var"] = elt.id

        return info

    def find_tuple_for_question(
        self,
        cid: str,
        template_id: Optional[str] = None,
        difficulty: Optional[str] = None,
        interaction_type: Optional[str] = None,
        bloom: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Resolves the exact TEMPLATES tuple info matching a question's competency, template_id, or difficulty/type."""
        cand_tuples = [t for t in self.tuples if t.get("competency_id") == cid]
        if not cand_tuples:
            cand_tuples = list(self.tuples)
        if not cand_tuples:
            return None

        if template_id:
            for t in cand_tuples:
                tid = str(t.get("template_id") or "")
                if (
                    tid == template_id
                    or tid.replace("_", "-") == template_id.replace("_", "-")
                    or f"T-{tid}" == template_id
                    or tid == f"T-{template_id}"
                    or tid.lower() == template_id.lower()
                ):
                    return t
            m_idx = re.search(r"[_-]0*(\d+)$", str(template_id))
            if m_idx:
                idx_1based = int(m_idx.group(1))
                if 1 <= idx_1based <= len(cand_tuples):
                    return cand_tuples[idx_1based - 1]

        norm_diff = (difficulty or "").strip().lower()
        norm_itype = (interaction_type or "").strip().lower()
        norm_bloom = (bloom or "").strip().lower()

        if norm_diff:
            diff_matches = [t for t in cand_tuples if t.get("difficulty") == norm_diff]
            if len(diff_matches) == 1:
                return diff_matches[0]
            if len(diff_matches) > 1 and norm_itype:
                for t in diff_matches:
                    qt = t.get("question_type") or ""
                    if ("multiple_choice" in norm_itype and "multiple_choice" in qt) or (
                        "fill_in" in norm_itype and ("fill_in" in qt or "open" in qt or "fib" in qt)
                    ) or ("select" in norm_itype and "select" in qt):
                        return t
                return diff_matches[0]

        if norm_itype:
            for t in cand_tuples:
                qt = t.get("question_type") or ""
                if ("multiple_choice" in norm_itype and "multiple_choice" in qt) or (
                    "fill_in" in norm_itype and ("fill_in" in qt or "open" in qt or "fib" in qt)
                ) or ("select" in norm_itype and "select" in qt):
                    if not norm_bloom or (t.get("bloom") or "").lower() == norm_bloom:
                        return t

        return cand_tuples[0]

    def find_offending_lines(
        self,
        tuple_info: Optional[Dict[str, Any]],
        linter_name: str = "",
        needle: str = "",
    ) -> Tuple[int, int, List[Tuple[int, str]]]:
        """Pinpoints the exact 1-based (start_line, end_line, [(lineno, code), ...]) inside the shard file."""
        if not self.lines:
            return 1, 1, []
        if not tuple_info:
            return 1, min(len(self.lines), 5), [(i + 1, self.lines[i]) for i in range(min(len(self.lines), 5))]

        linter_low = (linter_name or "").lower()
        gen_fn = tuple_info.get("gen_fn_name")
        ver_fn = tuple_info.get("ver_fn_name")
        stems_var = tuple_info.get("stems_var")
        hints_var = tuple_info.get("hints_var")
        sol_var = tuple_info.get("sol_var")
        t_start = tuple_info.get("start_line", 1)
        t_end = tuple_info.get("end_line", t_start)

        def _slice_lines(s: int, e: int) -> List[Tuple[int, str]]:
            s_c = max(1, s)
            e_c = min(len(self.lines), max(s_c, e))
            return [(ln, self.lines[ln - 1]) for ln in range(s_c, e_c + 1)]

        # 1. Hints linters -> locate hints_var or tuple hints element
        if "hint" in linter_low or "socratic" in linter_low or "scaffolding" in linter_low:
            if hints_var and hints_var in self.constants:
                s_h, e_h = self.constants[hints_var]
                return s_h, e_h, _slice_lines(s_h, e_h)
            h_elt = tuple_info.get("elements", {}).get("hints")
            if h_elt:
                return h_elt["start_line"], h_elt["end_line"], _slice_lines(h_elt["start_line"], h_elt["end_line"])

        # 2. ZPD / modality / archetype linters -> locate TEMPLATES tuple(s)
        if "zpd" in linter_low or "modality" in linter_low or "archetype" in linter_low:
            cid = tuple_info.get("competency_id")
            if cid:
                cid_tuples = [t for t in self.tuples if t.get("competency_id") == cid]
                if cid_tuples:
                    s_all = min(t["start_line"] for t in cid_tuples)
                    e_all = max(t["end_line"] for t in cid_tuples)
                    return s_all, e_all, _slice_lines(s_all, e_all)
            return t_start, t_end, _slice_lines(t_start, t_end)

        # 3. Distractor / rationale / magic-multiplier / anti-gaming / option length linters -> inside gen_fn
        if any(
            k in linter_low
            for k in ("diagnostic_rationale", "distractor", "cloned", "telltale", "anti_gaming", "length_padded", "magic")
        ):
            if gen_fn and gen_fn in self.functions:
                s_fn, e_fn = self.functions[gen_fn]
                fn_lines = _slice_lines(s_fn, e_fn)
                if "multiplicador" in needle.lower() or "magic" in linter_low or "diagnostic_rationale" in linter_low:
                    mult_lines = [
                        (ln, txt)
                        for ln, txt in fn_lines
                        if re.search(
                            r"\b(?:ds|cds|dists|distractors|d[1-6])\s*=|\bround\s*\(\s*ans\b|\bans\s*[\*/]|\(\"D-",
                            txt,
                        )
                    ]
                    if mult_lines:
                        s_m = mult_lines[0][0]
                        e_m = min(e_fn, max(mult_lines[-1][0], s_m + 1))
                        # If a multi-line list assignment starts at s_m, include up to its closing bracket or dists
                        return s_m, e_m, _slice_lines(s_m, min(e_m, s_m + 14))
                dist_lines = [
                    (ln, txt)
                    for ln, txt in fn_lines
                    if re.search(r"\b(?:dists|distractors|options|ds|d[1-6])\s*=|\(\"D-", txt)
                ]
                if dist_lines:
                    s_d = dist_lines[0][0]
                    e_d = dist_lines[-1][0]
                    return s_d, e_d, _slice_lines(s_d, min(e_d + 2, e_fn))
                return s_fn, e_fn, fn_lines

        # 4. KaTeX / uninterpolated / residue / string replacement -> search needle across gen_fn, stems_var, hints_var, sol_var
        if needle:
            n_clean = needle.strip()
            search_ranges: List[Tuple[int, int]] = []
            if gen_fn and gen_fn in self.functions:
                search_ranges.append(self.functions[gen_fn])
            for vname in (stems_var, hints_var, sol_var):
                if vname and vname in self.constants:
                    search_ranges.append(self.constants[vname])
            search_ranges.append((t_start, t_end))
            for s_r, e_r in search_ranges:
                matched = [
                    (ln, txt)
                    for ln, txt in _slice_lines(s_r, e_r)
                    if n_clean in txt
                ]
                if matched:
                    return matched[0][0], matched[-1][0], matched

        if gen_fn and gen_fn in self.functions:
            s_fn, e_fn = self.functions[gen_fn]
            return s_fn, e_fn, _slice_lines(s_fn, e_fn)

        return t_start, t_end, _slice_lines(t_start, t_end)

    def get_tuple_info(self, idx_or_cid: Union[int, str]) -> Optional[Dict[str, Any]]:
        idx = self.competency_to_tuple_idx.get(idx_or_cid) if isinstance(idx_or_cid, str) else idx_or_cid
        if idx is not None and isinstance(idx, int) and 0 <= idx < len(self.tuples):
            return self.tuples[idx]
        return None

    def get_tuple_snippet(self, idx_or_cid: Union[int, str]) -> Tuple[int, int, str]:
        """Returns (start_line, end_line, snippet_text) for a tuple."""
        idx = self.competency_to_tuple_idx.get(idx_or_cid) if isinstance(idx_or_cid, str) else idx_or_cid
        if idx is not None and isinstance(idx, int) and 0 <= idx < len(self.tuples):
            t = self.tuples[idx]
            s = t["start_line"]
            e = t["end_line"]
            snippet_lines = self.lines[s - 1 : e]
            numbered = [f"{s + i:4d}: {line}" for i, line in enumerate(snippet_lines)]
            return s, e, "\n".join(numbered)
        return 0, 0, ""

    def get_function_snippet(self, fn_name: str) -> Tuple[int, int, str]:
        """Returns (start_line, end_line, snippet_text) for a function definition."""
        if fn_name in self.functions:
            s, e = self.functions[fn_name]
            snippet_lines = self.lines[s - 1 : e]
            numbered = [f"{s + i:4d}: {line}" for i, line in enumerate(snippet_lines)]
            return s, e, "\n".join(numbered)
        return 0, 0, ""

    def get_constant_snippet(self, const_name: str) -> Tuple[int, int, str]:
        """Returns (start_line, end_line, snippet_text) for a constant assignment."""
        if const_name in self.constants:
            s, e = self.constants[const_name]
            snippet_lines = self.lines[s - 1 : e]
            numbered = [f"{s + i:4d}: {line}" for i, line in enumerate(snippet_lines)]
            return s, e, "\n".join(numbered)
        return 0, 0, ""

    def get_preamble_code(self) -> str:
        """Extracts allowed top-level imports, top-level constants, and helper functions for sandbox injection."""
        preamble_lines: List[str] = []
        # Safe allowed root modules in sandbox
        allowed_import_roots = {"math", "fractions", "statistics", "sympy", "numpy", "scipy", "random", "decimal"}

        # Only extract top-level imports from tree.body (ignoring imports inside functions)
        if getattr(self, "top_level_imports", None):
            for s, e, root in self.top_level_imports:
                if root in allowed_import_roots:
                    import_lines = self.lines[s - 1 : e]
                    preamble_lines.append(textwrap.dedent("\n".join(import_lines)).strip())
        else:
            # Fallback when AST didn't parse: strictly column-0 imports with NO leading indentation
            for line in self.lines:
                if line.startswith("import ") or line.startswith("from "):
                    stripped = line.strip()
                    parts = stripped.split()
                    if len(parts) >= 2:
                        root = parts[1].split(".")[0]
                        if root in allowed_import_roots:
                            preamble_lines.append(stripped)

        # Include constant lines
        for cname, (s, e) in sorted(self.constants.items(), key=lambda x: x[1][0]):
            const_lines = self.lines[s - 1 : e]
            preamble_lines.append(textwrap.dedent("\n".join(const_lines)).strip())

        # Include helper function lines in ascending line order
        for hname in sorted(self.helper_functions, key=lambda k: self.functions[k][0]):
            s, e = self.functions[hname]
            helper_src = "\n".join(self.lines[s - 1 : e])
            preamble_lines.append(textwrap.dedent(helper_src).strip())

        return "\n".join(preamble_lines).strip()


def extract_function_code(
    fn_or_str: Any,
    target_name: str,
    locator: Optional[ShardDataLineLocator] = None,
    fn_name_hint: Optional[str] = None,
    include_preamble: bool = True,
) -> str:
    """Extract and normalize Python code string for sandbox execution.

    Renames def <orig_name>( to def <target_name>( and ensures aliases:
    - generate_params -> generate = generate_params
    - verify -> cross_check = verify
    """
    raw_src = ""
    orig_name = getattr(fn_or_str, "__name__", fn_name_hint or "")
    if fn_or_str is None or (isinstance(fn_or_str, str) and not fn_or_str.strip()):
        if target_name == "verify":
            raw_src = "def verify(instance):\n    return True"
        else:
            raw_src = f"def {target_name}(rng):\n    return {{}}"
    elif callable(fn_or_str):
        try:
            raw_src = textwrap.dedent("\n".join(locator.lines[locator.functions[orig_name][0] - 1 : locator.functions[orig_name][1]])) if (locator and orig_name in locator.functions) else textwrap.dedent(inspect.getsource(fn_or_str))
        except Exception:
            if locator and orig_name in locator.functions:
                s, e = locator.functions[orig_name]
                raw_src = textwrap.dedent("\n".join(locator.lines[s - 1 : e]))
            else:
                raw_src = ""
    elif isinstance(fn_or_str, str):
        raw_src = textwrap.dedent(fn_or_str)
    else:
        raw_src = str(fn_or_str)

    # Rename first function definition to target_name
    code_str = re.sub(r"^def\s+[A-Za-z0-9_]+\s*\(", f"def {target_name}(", raw_src, count=1)

    # Alias bindings for sandbox execution
    if target_name == "generate_params":
        if "\ngenerate = " not in code_str and "def generate(" not in code_str:
            code_str = code_str.rstrip() + "\n\ngenerate = generate_params\n"
    elif target_name == "verify":
        if "\ncross_check = " not in code_str and "def cross_check(" not in code_str:
            code_str = code_str.rstrip() + "\n\ncross_check = verify\n"

    # Prepend preamble (helpers, constants, allowed imports) if available
    if include_preamble and locator:
        preamble = locator.get_preamble_code()
        if preamble:
            code_str = f"{preamble}\n\n{code_str}"

    return code_str


def build_adapted_mc7_generator(
    base_gen_code: str,
    cid: str,
    cta_distractors: List[Dict[str, Any]],
    strict: bool = True,
) -> str:
    """Wraps an MC7 generator function to assemble options list with 1 correct and distractors.

    In strict mode:
    - Eliminates magical multipliers and synthetic positional assignment.
    - Rejects 2-tuples (did, val) and requires 3-tuples (did, val, error_rationale).
    - Ensures distractor IDs match declared CTA distractors.
    """
    declared_ids_list = [d.get("id") for d in cta_distractors if isinstance(d, dict) and d.get("id")]
    declared_ids_repr = repr(set(declared_ids_list))
    strict_repr = "True" if strict else "False"

    wrapper = f"""{base_gen_code}

_c2c_orig_generate = generate_params

def generate_params(rng):
    res = _c2c_orig_generate(rng)
    if isinstance(res, (tuple, list)):
        if len(res) >= 3:
            v_map = res[0] if isinstance(res[0], dict) else {{"val": res[0]}}
            res = {{"vars": v_map, "correct": str(res[1]), "distractors": res[2]}}
        elif len(res) == 2:
            v_map = res[0] if isinstance(res[0], dict) else {{"val": res[0]}}
            res = {{"vars": v_map, "correct": str(res[1]), "distractors": []}}
        else:
            return res
    elif not isinstance(res, dict):
        return res

    declared_ids = {declared_ids_repr}
    is_strict = {strict_repr}

    # Extract options and distractors
    opts = res.get("options")
    dists_raw = res.get("distractors")
    if dists_raw is None and isinstance(opts, list):
        dists_raw = [dict(opt) for opt in opts if isinstance(opt, dict) and not opt.get("is_correct")]
    elif dists_raw is None:
        dists_raw = []

    correct_val = str(res.get("correct", "")).strip()
    if not correct_val and isinstance(opts, list):
        for opt in opts:
            if isinstance(opt, dict) and opt.get("is_correct"):
                correct_val = str(opt.get("value") or opt.get("content", "")).strip()
                res["correct"] = correct_val
                break

    normalized_dists = []
    for idx, d in enumerate(dists_raw):
        val = ""
        did = None
        rat = None
        if isinstance(d, dict):
            val = str(d.get("value") if "value" in d else (d.get("content") if "content" in d else d.get("ans", ""))).strip()
            did = d.get("distractor_id") or d.get("id") or d.get("did")
            rat = d.get("error_rationale") or d.get("rationale")
        elif isinstance(d, (tuple, list)):
            if len(d) >= 3:
                e0, e1 = str(d[0]).strip(), str(d[1]).strip()
                norm_e0 = e0.replace("_", "-")
                norm_e1 = e1.replace("_", "-")
                if e0.startswith(("D-", "D_")) or norm_e0 in declared_ids:
                    did, val, rat = norm_e0, e1, str(d[2]).strip()
                elif e1.startswith(("D-", "D_")) or norm_e1 in declared_ids:
                    val, did, rat = e0, norm_e1, str(d[2]).strip()
                else:
                    did, val, rat = norm_e0, e1, str(d[2]).strip()
            elif len(d) == 2:
                if is_strict:
                    raise ValueError(
                        f"[TPL-MC7-STRICT] En modo estricto, la 2-tupla (distractor_id, value) esta prohibida en MC7. "
                        f"Cada distractor debe ser una 3-tupla (distractor_id, value, error_rationale) con error_rationale >= 20 caracteres: {{repr(d)}}"
                    )
                e0, e1 = str(d[0]).strip(), str(d[1]).strip()
                norm_e0 = e0.replace("_", "-")
                norm_e1 = e1.replace("_", "-")
                if e0.startswith(("D-", "D_")) or norm_e0 in declared_ids:
                    did, val = norm_e0, e1
                elif e1.startswith(("D-", "D_")) or norm_e1 in declared_ids:
                    val, did = e0, norm_e1
                else:
                    did, val = norm_e0, e1
            elif len(d) == 1:
                if is_strict:
                    raise ValueError(f"Distractor escalar no permitido en modo estricto: {{repr(d)}}")
                val = str(d[0]).strip()
        elif isinstance(d, (str, int, float)):
            if is_strict:
                raise ValueError(f"Distractor escalar no permitido en modo estricto: {{repr(d)}}")
            val = str(d).strip()

        if did and did not in declared_ids:
            norm_did = str(did).replace("_", "-")
            if norm_did in declared_ids:
                did = norm_did
            elif is_strict:
                raise ValueError(
                    f"Distractor ID '{{did}}' no esta declarado en cta.json para la competencia '{cid}'."
                )

        normalized_dists.append({{
            "value": val,
            "content": val,
            "distractor_id": did,
            "error_rationale": rat or "",
            "is_correct": False,
        }})

    res["distractors"] = normalized_dists
    correct_opt = {{
        "value": correct_val,
        "content": correct_val,
        "is_correct": True,
    }}
    res["options"] = [correct_opt] + normalized_dists
    return res

generate = generate_params
"""
    return wrapper


def discover_fix_files(
    fixes_dir: Optional[Path],
    expected_cids: List[str],
    shard_id: Optional[str] = None,
) -> Tuple[Dict[str, Path], List[Path]]:
    """Discovers and maps shard fix files to competency IDs with case-insensitive and delimiter-agnostic normalization.
    
    Supports both per-shard isolated directories (shard_fixes/<shard_id>/<cid>.py)
    and legacy flat directories (shard_fixes/<cid>.py).
    Matches Hab-03, Hab_03, hab-03, hab_03, T-Hab-03, and hab03 to Hab-03.
    Returns (fix_files_by_cid, all_relevant_fix_files).
    """
    fix_files_by_cid: Dict[str, Path] = {}
    relevant_files: List[Path] = []
    if not fixes_dir or not fixes_dir.is_dir():
        return fix_files_by_cid, relevant_files

    # Check for per-shard subdirectory if fixes_dir is a root shard_fixes dir
    if shard_id and (fixes_dir / shard_id).is_dir():
        sub_files = sorted((fixes_dir / shard_id).glob("*.py"))
        if sub_files:
            all_fix_files = sub_files
        else:
            all_fix_files = sorted(fixes_dir.glob("*.py"))
    else:
        all_fix_files = sorted(fixes_dir.glob("*.py"))

    for fix_p in all_fix_files:
        stem = fix_p.stem
        norm_stem = re.sub(r"[^a-zA-Z0-9]", "", stem).lower()
        matched = False
        for ecid in expected_cids:
            norm_ecid = re.sub(r"[^a-zA-Z0-9]", "", ecid).lower()
            if (
                stem == ecid
                or stem == ecid.replace("-", "_")
                or stem.lower() == ecid.lower()
                or stem.replace("_", "-").lower() == ecid.lower()
                or norm_stem == norm_ecid
                or norm_stem == f"t{norm_ecid}"
            ):
                fix_files_by_cid[ecid] = fix_p
                if fix_p not in relevant_files:
                    relevant_files.append(fix_p)
                matched = True
                break
        if not matched and not expected_cids:
            norm_stem_cid = stem.replace("_", "-")
            fix_files_by_cid[norm_stem_cid] = fix_p
            if fix_p not in relevant_files:
                relevant_files.append(fix_p)

    return fix_files_by_cid, relevant_files


def infer_work_dir(
    explicit_work: Union[str, Path] = "work",
    shard_id: Optional[str] = None,
) -> Path:
    """Infers work directory if default 'work' is missing from CWD.

    Searches for:
    1. Active lockfiles: courses/*/.c2c_subagent_lock.json or courses/*/work/.c2c_subagent_lock.json with active=true.
    2. Most recent courses/*/work directory containing shards/{shard_id}_data.py or shards/pre_shard_manifest.json.
    Returns inferred Path, or Path(explicit_work) if no course match found.
    """
    target = Path(explicit_work)
    if (target / "shards" / "pre_shard_manifest.json").is_file() or (target / "pre_shard_manifest.json").is_file():
        return target

    cwd = Path.cwd()
    courses_dir = cwd / "courses"
    if not courses_dir.is_dir():
        return target

    norm_s_id = (shard_id or "").lower().strip()
    candidate_works: List[Tuple[float, Path]] = []

    for c_dir in sorted(courses_dir.iterdir()):
        if not c_dir.is_dir():
            continue
        lock_paths = [
            c_dir / ".c2c_subagent_lock.json",
            c_dir / "work" / ".c2c_subagent_lock.json",
        ]
        is_active = False
        for lp in lock_paths:
            if lp.is_file():
                try:
                    ldata = json.loads(lp.read_text(encoding="utf-8"))
                    if isinstance(ldata, dict) and ldata.get("active") is True:
                        is_active = True
                        break
                except Exception:
                    pass

        w_cand = c_dir / "work"
        if w_cand.is_dir():
            has_manifest = (w_cand / "shards" / "pre_shard_manifest.json").is_file() or (w_cand / "pre_shard_manifest.json").is_file()
            has_shard = (w_cand / "shards" / f"{norm_s_id}_data.py").is_file() if norm_s_id else False

            if is_active and (has_manifest or has_shard):
                return w_cand

            if has_shard or has_manifest:
                mtime = 0.0
                if has_shard:
                    mtime = (w_cand / "shards" / f"{norm_s_id}_data.py").stat().st_mtime
                elif has_manifest:
                    m_p = (w_cand / "shards" / "pre_shard_manifest.json") if (w_cand / "shards" / "pre_shard_manifest.json").is_file() else (w_cand / "pre_shard_manifest.json")
                    mtime = m_p.stat().st_mtime
                candidate_works.append((mtime, w_cand))

    if candidate_works:
        candidate_works.sort(key=lambda x: x[0], reverse=True)
        return candidate_works[0][1]

    return target


def compile_shard(
    work_dir_or_path: Union[str, Path],
    shard_id: Optional[str] = None,
    strict: bool = True,
    seeds: int = 50,
    output_dir: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None,
    cta_path: Optional[Union[str, Path]] = None,
    manifest_path: Optional[Union[str, Path]] = None,
    min_archetypes: Optional[int] = None,
    **kwargs,
) -> Tuple[bool, List[str]]:
    """Compiles shard data into canonical template JSON files with strict verification.

    Supports dual invocation styles:
    - compile_shard("work", "shard_01", strict=True, seeds=50)
    - compile_shard("work/shards/shard_01_data.py", output_dir="work/templates")
    """
    output_path = output_path or kwargs.get("output")
    cta_path = cta_path or kwargs.get("cta")
    manifest_path = manifest_path or kwargs.get("manifest")
    min_archetypes = min_archetypes if min_archetypes is not None else kwargs.get("min_archetypes")

    target_p = Path(work_dir_or_path).resolve()
    # In-memory inference when default "work" does not have manifest
    if not target_p.name.endswith(".py"):
        if str(work_dir_or_path) in ("work", "./work", ".\\work") or target_p == (Path.cwd() / "work").resolve():
            if not (target_p / "shards" / "pre_shard_manifest.json").is_file() and not (target_p / "pre_shard_manifest.json").is_file():
                inferred = infer_work_dir(target_p, shard_id=shard_id)
                if inferred != target_p:
                    target_p = inferred.resolve()

    # Guarantee sys.modules and linecache safety across multiple compiles in same process
    import linecache
    linecache.clearcache()
    for k in list(sys.modules.keys()):
        if k.startswith("c2c_fix_mod_") or k.startswith("c2c_shard_mod_"):
            sys.modules.pop(k, None)

    # Determine if target_p is a shard data file or a work directory
    if target_p.name.endswith(".py"):
        if not shard_id:
            m_s = re.search(r"shard_(\d+)", target_p.stem)
            shard_id = f"shard_{m_s.group(1)}" if m_s else target_p.stem.replace("_data", "")
        shards_dir = target_p.parent
        work_p = shards_dir.parent if shards_dir.name == "shards" else shards_dir
        if not target_p.is_file():
            err_msg = f"ERROR: No existe el archivo de datos del shard: {target_p}"
            print(err_msg, file=sys.stderr)
            return False, [err_msg]
        shard_data_path = target_p
    else:
        work_p = target_p
        shards_dir = work_p / "shards"
        shard_data_path = None

    receipt_p = Path(output_path).resolve() if output_path and str(output_path).lower().endswith(".json") else None
    if output_dir:
        templates_dir = Path(output_dir).resolve()
    elif output_path and not receipt_p:
        templates_dir = Path(output_path).resolve()
    else:
        templates_dir = work_p / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)

    if not shard_id:
        err_msg = "ERROR: shard_id no especificado para compile_shard."
        print(err_msg, file=sys.stderr)
        return False, [err_msg]

    norm_shard_id = shard_id.lower().strip()
    att_dir = work_p / ".check_attempts"
    pass_marker = att_dir / f"pass_{norm_shard_id}.json"

    def _cleanup_stale_pass_marker():
        if pass_marker.is_file():
            try:
                pass_marker.unlink()
            except Exception:
                pass

    # 1. Verify pre_shard_manifest.json (resolving --manifest pre_cta_manifest.json fallback cleanly)
    def _find_pre_shard_manifest() -> Optional[Path]:
        for cand in (shards_dir / "pre_shard_manifest.json", work_p / "pre_shard_manifest.json"):
            if cand.is_file():
                return cand.resolve()
        return None

    if manifest_path and Path(manifest_path).is_file():
        manifest_p = Path(manifest_path).resolve()
    else:
        found_m = _find_pre_shard_manifest()
        if not found_m:
            _cleanup_stale_pass_marker()
            print("BLOCKER:: No existe pre_shard_manifest.json", file=sys.stderr)
            sys.exit(2)
        manifest_p = found_m

    try:
        manifest_data = json.loads(manifest_p.read_text(encoding="utf-8"))
    except Exception as e:
        _cleanup_stale_pass_marker()
        print(f"BLOCKER:: pre_shard_manifest.json corrupto o ilegible: {e}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(manifest_data, dict) or "shards" not in manifest_data:
        fallback_m = _find_pre_shard_manifest()
        if fallback_m and fallback_m != manifest_p:
            try:
                manifest_data = json.loads(fallback_m.read_text(encoding="utf-8"))
                manifest_p = fallback_m
            except Exception as e:
                _cleanup_stale_pass_marker()
                print(f"BLOCKER:: pre_shard_manifest.json corrupto o ilegible: {e}", file=sys.stderr)
                sys.exit(2)
        elif not fallback_m:
            _cleanup_stale_pass_marker()
            print("BLOCKER:: No existe pre_shard_manifest.json", file=sys.stderr)
            sys.exit(2)

    # Locate shard entry
    shard_entry = None
    for s in manifest_data.get("shards", []):
        s_id = str(s.get("shard_id", "")).lower().strip()
        if s_id == norm_shard_id or s_id.replace("shard_", "") == norm_shard_id.replace("shard_", ""):
            shard_entry = s
            break

    if not shard_entry:
        _cleanup_stale_pass_marker()
        err_msg = f"ERROR: Shard '{shard_id}' no encontrado en pre_shard_manifest.json."
        print(err_msg, file=sys.stderr)
        return False, [err_msg]

    expected_cids: List[str] = shard_entry.get("competency_ids", [])
    if not expected_cids and "competencies" in shard_entry:
        expected_cids = [c["id"] for c in shard_entry["competencies"] if isinstance(c, dict) and "id" in c]

    eff_min_arch = 3
    if min_archetypes is not None:
        eff_min_arch = int(min_archetypes)
    elif isinstance(shard_entry, dict) and shard_entry.get("min_archetypes"):
        eff_min_arch = int(shard_entry["min_archetypes"])
    elif isinstance(manifest_data, dict) and manifest_data.get("min_archetypes"):
        eff_min_arch = int(manifest_data["min_archetypes"])

    # Locate shard_fixes directory: prioritize shard-isolated directory (shard_fixes/<shard_id>/)
    shard_fixes_dir = shards_dir / "shard_fixes" / norm_shard_id
    if not shard_fixes_dir.is_dir() and (work_p / "shards" / "shard_fixes" / norm_shard_id).is_dir():
        shard_fixes_dir = work_p / "shards" / "shard_fixes" / norm_shard_id

    flat_fixes_dir = shards_dir / "shard_fixes"
    if not flat_fixes_dir.is_dir() and (work_p / "shards" / "shard_fixes").is_dir():
        flat_fixes_dir = work_p / "shards" / "shard_fixes"

    # Prioritize shard-isolated directory if it exists and has fix files, else fallback to flat
    fixes_dir = shard_fixes_dir if (shard_fixes_dir.is_dir() and any(shard_fixes_dir.glob("*.py"))) else flat_fixes_dir

    # Discover relevant fix files for hashing and modular splicing
    fix_files_by_cid, relevant_fix_files = discover_fix_files(fixes_dir, expected_cids, shard_id=norm_shard_id)
    has_all_fixes = bool(expected_cids and all(ecid in fix_files_by_cid for ecid in expected_cids))

    # Locate shard data path if not provided
    if not shard_data_path or not shard_data_path.is_file():
        shard_data_path_str = shard_entry.get("shard_data_path")
        if shard_data_path_str and Path(shard_data_path_str).is_file():
            shard_data_path = Path(shard_data_path_str).resolve()
        else:
            candidate = shards_dir / f"{norm_shard_id}_data.py"
            if candidate.is_file():
                shard_data_path = candidate
            else:
                if not has_all_fixes:
                    _cleanup_stale_pass_marker()
                    err_msg = f"ERROR: No existe el archivo de datos del shard: {candidate}"
                    print(err_msg, file=sys.stderr)
                    return False, [err_msg]
                shard_data_path = candidate

    # Compute source_sha256 over shard_data_path (if exists) + relevant fix files
    hasher = hashlib.sha256()
    if shard_data_path and shard_data_path.is_file():
        hasher.update(shard_data_path.read_bytes())
    for rf in sorted(relevant_fix_files, key=lambda p: p.name):
        hasher.update(f"\n--FIX:{rf.name}--\n".encode("utf-8"))
        hasher.update(rf.read_bytes())
    source_sha256 = hasher.hexdigest()

    # Bounded compilation counter & unified stateful circuit breaker (.check_attempts/compile_{norm_shard_id}.json)
    att_dir.mkdir(parents=True, exist_ok=True)
    compile_att_file = att_dir / f"compile_{norm_shard_id}.json"

    state: Dict[str, Any] = {
        "distinct_compiles": 0,
        "same_error_streak": 0,
        "last_source_sha256": "",
        "last_err_hash": "",
        "last_errors": [],
        "error_count": 0,
        "has_syntax_error": False,
    }
    if compile_att_file.is_file():
        try:
            loaded_state = json.loads(compile_att_file.read_text(encoding="utf-8"))
            if isinstance(loaded_state, dict):
                if "distinct_compiles" in loaded_state:
                    state.update(loaded_state)
                elif "count" in loaded_state:
                    state["distinct_compiles"] = loaded_state.get("count", 0)
        except Exception:
            pass

    # Idempotent [NO-CHANGE] Re-Run check: do not increment counter or streak on identical source
    if (
        state.get("last_source_sha256") == source_sha256
        and state.get("last_errors")
    ):
        cached_errors = state["last_errors"]
        no_change_prefix = "[NO-CHANGE: código idéntico al intento previo; edita el archivo antes de recompilar]"
        prefixed_errors = []
        for e in cached_errors:
            if no_change_prefix not in e:
                prefixed_errors.append(f"{no_change_prefix}\n{e}")
            else:
                prefixed_errors.append(e)
        print(prefixed_errors[0], file=sys.stderr)
        return False, prefixed_errors

    # Distinct compile increment
    distinct_compiles = state.get("distinct_compiles", 0) + 1
    state["distinct_compiles"] = distinct_compiles
    state["last_source_sha256"] = source_sha256

    print(f"[COMPILE {distinct_compiles}/10] Compilando shard '{shard_id}'...")

    def _fail(msg: str, has_syntax_error: bool = False, error_count: int = 1) -> Tuple[bool, List[str]]:
        from check_templates import normalize_error_string_for_hash
        normalized_errs = sorted([normalize_error_string_for_hash(msg)])
        err_hash = hashlib.sha256("\n".join(normalized_errs).encode("utf-8")).hexdigest()

        if state.get("last_err_hash") == err_hash:
            same_error_streak = state.get("same_error_streak", 0) + 1
        else:
            same_error_streak = 1
        state["same_error_streak"] = same_error_streak
        state["last_err_hash"] = err_hash
        state["error_count"] = error_count
        state["has_syntax_error"] = bool(has_syntax_error)

        res_msg = msg
        if same_error_streak >= 3:
            terminal_stop = (
                f"\n[-] [CIRCUIT BREAKER HALT: 3 fallos consecutivos idénticos para shard '{shard_id}']. "
                f"STOP, send_message the Director."
            )
            res_msg = res_msg + terminal_stop
            print(terminal_stop, file=sys.stderr)

        _cleanup_stale_pass_marker()

        if receipt_p:
            try:
                import time
                r_data = {}
                if receipt_p.is_file():
                    try:
                        r_data = json.loads(receipt_p.read_text(encoding="utf-8"))
                    except Exception:
                        r_data = {}
                r_data["shard_id"] = shard_id
                r_data["compiled_status"] = "FAIL"
                r_data["compilation_errors"] = [res_msg]
                r_data["error_count"] = error_count
                r_data["has_syntax_error"] = bool(has_syntax_error)
                r_data["compiled_at"] = time.time()
                _atomic_write_json(receipt_p, r_data)
            except Exception:
                pass

        state["last_errors"] = [res_msg]
        _atomic_write_json(compile_att_file, state)
        print(msg, file=sys.stderr)
        return False, [res_msg]

    # Dual Calibrated Halt Threshold: distinct_compiles > 10
    if distinct_compiles > 10:
        halt_msg = (
            f"[-] [CIRCUIT BREAKER HALT: Límite de 10 compilaciones distintas alcanzado para shard '{shard_id}']. "
            f"STOP, send_message the Director."
        )
        return _fail(halt_msg, has_syntax_error=False, error_count=1)

    # In-memory healing of shard_XX_data.py (Zero-Disk-Mutation: source file on disk is NEVER modified)
    raw_source = shard_data_path.read_text(encoding="utf-8") if shard_data_path.is_file() else ""
    if raw_source:
        rf_warnings = check_ast_rf_triple_braces(raw_source)
        for w in rf_warnings:
            print(w, file=sys.stderr)
        _, healed_source = heal_shard_source_text(raw_source)
    else:
        healed_source = ""

    # Staged copy under .check_attempts/_staged/ for debugging without mutating source
    if healed_source:
        staged_dir = att_dir / "_staged"
        staged_dir.mkdir(parents=True, exist_ok=True)
        staged_p = staged_dir / f"{norm_shard_id}_data.py"
        try:
            staged_p.write_text(healed_source, encoding="utf-8")
        except Exception:
            pass

    # 2. AST Line Locator & Syntax Verification (evaluated on in-memory healed source)
    locator = ShardDataLineLocator(shard_data_path, source_text=healed_source)
    skip_base_module = False
    if raw_source and locator.syntax_error:
        if has_all_fixes:
            print(
                f"[!] Warning: {shard_data_path.name} contiene error sintáctico, pero el 100% de las competencias "
                f"({expected_cids}) están cubiertas por fijaciones en shard_fixes/. Omitiendo {shard_data_path.name}.",
                file=sys.stderr,
            )
            skip_base_module = True
        else:
            print(f"FAIL: Error sintáctico en {shard_data_path.name}:", file=sys.stderr)
            return _fail(locator.syntax_error, has_syntax_error=True, error_count=1)

    # 3. Load shard module dynamically from in-memory string
    mod_name = f"c2c_shard_mod_{norm_shard_id}_{uuid.uuid4().hex[:6]}"
    mod = types.ModuleType(mod_name)
    mod.__file__ = str(shard_data_path)
    if healed_source and not skip_base_module:
        try:
            code_obj = compile(healed_source, str(shard_data_path), "exec")
            sys.modules[mod_name] = mod
            exec(code_obj, mod.__dict__)
        except Exception as e:
            if has_all_fixes:
                print(
                    f"[!] Warning: Excepción al ejecutar {shard_data_path.name}, pero el 100% de las competencias "
                    f"están cubiertas por shard_fixes/. Omitiendo {shard_data_path.name}.",
                    file=sys.stderr,
                )
                skip_base_module = True
            else:
                tb = traceback.format_exc()
                err_msg = f"FAIL: Excepción al ejecutar {shard_data_path.name}:\n{tb}"
                return _fail(err_msg, has_syntax_error=isinstance(e, SyntaxError), error_count=1)

    base_templates = [] if skip_base_module else (getattr(mod, "TEMPLATES", None) or [])
    from check_templates import heal_control_chars_in_obj
    base_templates = heal_control_chars_in_obj(base_templates)

    # Map tuples to their origin file and line locator
    tuple_records: List[Dict[str, Any]] = []
    for orig_idx, t in enumerate(base_templates):
        tuple_records.append({
            "tuple": t,
            "file_path": shard_data_path,
            "locator": locator,
            "orig_idx": orig_idx,
        })

    # Splice fix files from shards/shard_fixes/<CID>.py
    known_types = {"multiple_choice", "multiple_choice_7_options", "fill_in_the_blank", "multiple_select", "open_ended"}

    for cid_fix, fix_path in fix_files_by_cid.items():
        if not fix_path.is_file():
            continue
        try:
            fix_raw_text = fix_path.read_text(encoding="utf-8")
            rf_w = check_ast_rf_triple_braces(fix_raw_text)
            for w in rf_w:
                print(w, file=sys.stderr)
            _, healed_fix_text = heal_shard_source_text(fix_raw_text)
            fix_loc = ShardDataLineLocator(fix_path, source_text=healed_fix_text)
            if fix_loc.syntax_error:
                return _fail(
                    f"FAIL: Error sintáctico en shard_fixes/{fix_path.name}:\n{fix_loc.syntax_error}",
                    has_syntax_error=True,
                    error_count=1,
                )

            fix_mod_name = f"c2c_fix_mod_{cid_fix.replace('-', '_')}_{uuid.uuid4().hex[:6]}"
            fix_mod = types.ModuleType(fix_mod_name)
            fix_mod.__file__ = str(fix_path)
            fix_code_obj = compile(healed_fix_text, str(fix_path), "exec")
            sys.modules[fix_mod_name] = fix_mod
            exec(fix_code_obj, fix_mod.__dict__)

            fix_templates = getattr(fix_mod, "TEMPLATES", None)
            if fix_templates and isinstance(fix_templates, (list, tuple)):
                fix_templates = heal_control_chars_in_obj(fix_templates)

                new_records = []
                replaced = False
                for rec in tuple_records:
                    t_cand = rec["tuple"]
                    t_cid = None
                    if len(t_cand) >= 3 and str(t_cand[2]).lower().strip() in known_types:
                        t_cid = str(t_cand[1]).strip()
                    elif len(t_cand) >= 3 and str(t_cand[1]).lower().strip() in known_types:
                        t_cid = str(t_cand[0]).strip()
                    else:
                        t_cid = str(t_cand[0]).strip()

                    if t_cid == cid_fix or t_cid.replace("-", "_") == cid_fix.replace("-", "_"):
                        if not replaced:
                            for fix_idx, ft in enumerate(fix_templates):
                                new_records.append({
                                    "tuple": ft,
                                    "file_path": fix_path,
                                    "locator": fix_loc,
                                    "orig_idx": fix_idx,
                                })
                            replaced = True
                    else:
                        new_records.append(rec)

                if not replaced:
                    for fix_idx, ft in enumerate(fix_templates):
                        new_records.append({
                            "tuple": ft,
                            "file_path": fix_path,
                            "locator": fix_loc,
                            "orig_idx": fix_idx,
                        })

                tuple_records = new_records
        except Exception as e:
            tb = traceback.format_exc()
            return _fail(
                f"FAIL: Excepción al cargar shard_fixes/{fix_path.name}:\n{tb}",
                has_syntax_error=isinstance(e, SyntaxError),
                error_count=1,
            )

    raw_templates = [rec["tuple"] for rec in tuple_records]
    if not raw_templates:
        err_msg = f"FAIL: {shard_data_path.name} no define la lista 'TEMPLATES = [...]'."
        return _fail(err_msg)

    # 4. Identify competencies and verify parity
    found_cids = []
    for rec_idx, rec in enumerate(tuple_records):
        t = rec["tuple"]
        curr_loc = rec["locator"]
        curr_p = rec["file_path"]
        orig_idx = rec["orig_idx"]
        if not isinstance(t, (list, tuple)) or len(t) != 9:
            s_t, e_t, snip = curr_loc.get_tuple_snippet(orig_idx)
            err_msg = (
                f"FAIL: La tupla en índice {orig_idx} tiene {len(t) if isinstance(t, (list, tuple)) else 0} elementos "
                f"(se requieren exactamente 9 elementos según el contrato Form-B: "
                f"tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution).\n"
                f"  Ubicación: Líneas {s_t}..{e_t} en {curr_p.name}\n"
                f"{snip}"
            )
            return _fail(err_msg)

        if str(t[1]).lower().strip() in known_types or str(t[2]).lower().strip() not in known_types:
            s_t, e_t, snip = curr_loc.get_tuple_snippet(orig_idx)
            err_msg = (
                f"FAIL: Se detectó formato legacy Form-A o tipo inválido en la tupla {orig_idx}. "
                f"El compilador solo admite el contrato Form-B de 9 elementos: "
                f"(tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution).\n"
                f"  Ubicación: Líneas {s_t}..{e_t} en {curr_p.name}\n"
                f"{snip}"
            )
            return _fail(err_msg)

        c_candidate = str(t[1]).strip()
        found_cids.append(c_candidate)

    missing_cids = [cid for cid in expected_cids if cid not in found_cids]
    unexpected_cids = [cid for cid in found_cids if cid not in expected_cids]
    if missing_cids or unexpected_cids:
        err_parts = []
        if missing_cids:
            err_parts.append(f"Competencias faltantes en TEMPLATES: {', '.join(missing_cids)}")
        if unexpected_cids:
            err_parts.append(f"Competencias no asignadas a este shard: {', '.join(unexpected_cids)}")
        err_msg = f"FAIL: Paridad de competencias violada en {shard_data_path.name}: " + " | ".join(err_parts)
        return _fail(err_msg)

    from check_templates import auto_heal_template_data, check_templates_file_or_dir

    if cta_path and Path(cta_path).is_file():
        cta_p = Path(cta_path).resolve()
    else:
        cta_file_candidate = work_p / "cta.json"
        cta_p = cta_file_candidate if cta_file_candidate.is_file() else None

    cta_comp_map = {c["id"]: c for c in shard_entry.get("competencies", []) if isinstance(c, dict) and "id" in c}
    if cta_p and cta_p.is_file():
        try:
            cta_data = json.loads(cta_p.read_text(encoding="utf-8"))
            for c in cta_data.get("competencies", []):
                if isinstance(c, dict) and "id" in c:
                    cid_key = c["id"]
                    if cid_key not in cta_comp_map or not cta_comp_map[cid_key].get("distractors"):
                        cta_comp_map[cid_key] = c
                    elif c.get("distractors") and not cta_comp_map[cid_key].get("distractors"):
                        cta_comp_map[cid_key]["distractors"] = c["distractors"]
        except Exception:
            pass

    # 5. Compile tuples into canonical JSON dictionaries grouped by competency
    templates_by_cid: Dict[str, List[Dict[str, Any]]] = {}
    gen_callables_by_cid: Dict[str, List[Any]] = {}

    for t_idx, rec in enumerate(tuple_records):
        t = rec["tuple"]
        curr_loc = rec["locator"]
        curr_p = rec["file_path"]
        orig_idx = rec["orig_idx"]

        # Determine format (Form-B 9-tuple)
        if len(t) != 9 or str(t[2]).lower().strip() not in known_types:
            return _fail(
                f"FAIL: Tupla {orig_idx} no cumple el contrato Form-B de 9 elementos: "
                f"(tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution)."
            )

        tpl_id = str(t[0]).strip()
        cid = str(t[1]).strip()
        qtype = str(t[2]).strip().lower()
        gen_raw = t[3]
        ver_raw = t[4]
        diff_raw = t[5]
        stems_raw = t[6]
        hints_raw = t[7]
        sol_raw = str(t[8])
        target_kc = cid
        target_misc = []
        src_ref = {"doc": "manifest.pdf", "page": 1, "quote": ""}

        # Determine difficulty and bloom (element [5] must be 2-tuple (difficulty, bloom))
        if not isinstance(diff_raw, (list, tuple)) or len(diff_raw) != 2:
            return _fail(
                f"FAIL: El elemento de dificultad en tupla {orig_idx} ('{tpl_id}') debe ser explícitamente "
                f"una 2-tupla (difficulty, bloom) (ej. ('easy', 'Remember')), se recibió: {repr(diff_raw)}."
            )

        difficulty = str(diff_raw[0]).lower().strip()
        bloom = str(diff_raw[1]).capitalize().strip()

        if difficulty not in ("easy", "medium", "hard"):
            return _fail(
                f"FAIL: Dificultad inválida '{difficulty}' en tupla {orig_idx} ('{tpl_id}'). "
                f"Debe ser 'easy', 'medium' o 'hard'."
            )
        if bloom not in ("Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"):
            return _fail(
                f"FAIL: Nivel de Bloom inválido '{bloom}' en tupla {orig_idx} ('{tpl_id}'). "
                f"Debe ser Remember, Understand, Apply, Analyze, Evaluate o Create."
            )

        # Determine interaction_type
        if qtype in ("multiple_choice", "multiple_choice_7_options", "mc7"):
            interaction_type = "multiple_choice_7_options"
        elif qtype in ("open_ended", "fill_in_the_blank", "fib"):
            interaction_type = "fill_in_the_blank"
            target_misc = []
        elif qtype in ("multiple_select", "ms"):
            interaction_type = "multiple_select"
        else:
            interaction_type = qtype

        # Extract functions using originating file locator
        tuple_info = curr_loc.get_tuple_info(orig_idx) or curr_loc.get_tuple_info(cid) or {}
        gen_fn_name = tuple_info.get("gen_fn_name") or getattr(gen_raw, "__name__", None)
        ver_fn_name = tuple_info.get("ver_fn_name") or getattr(ver_raw, "__name__", None)

        gen_code = extract_function_code(gen_raw, "generate_params", locator=curr_loc, fn_name_hint=gen_fn_name)
        ver_code = extract_function_code(ver_raw, "verify", locator=curr_loc, fn_name_hint=ver_fn_name)

        # Check non-trivial verifier
        ver_is_trivial, ver_reason = is_trivial_verifier(ver_code, ver_raw)
        if ver_is_trivial:
            return _fail(
                f"FAIL: [TPL-VERIFIER] El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' es trivial ({ver_reason}). "
                f"Debe evaluar condiciones lógicas o matemáticas reales sobre el resultado generado."
            )

        # Stems validation: require at least 3 distinct author-written stems
        if not isinstance(stems_raw, (list, tuple)) or len(stems_raw) < 3:
            return _fail(
                f"FAIL: La plantilla '{tpl_id}' debe proporcionar al menos 3 enunciados distintos en stems "
                f"(se recibieron {len(stems_raw) if isinstance(stems_raw, (list, tuple)) else 0})."
            )
        cleaned_stems = [str(s).strip() for s in stems_raw if str(s).strip()]
        if len(set(cleaned_stems)) < 3:
            return _fail(
                f"FAIL: La plantilla '{tpl_id}' contiene enunciados duplicados en stems "
                f"(se encontraron {len(set(cleaned_stems))} únicos, se requieren >= 3)."
            )
        stem_es = cleaned_stems[0]
        stem_variants = cleaned_stems

        # Hints validation: require 3 to 5 author hints, >= 25 chars, no anti-socratic catchphrases, no literal wrong_belief copy
        cta_comp = cta_comp_map.get(cid, {})
        cta_distractors = cta_comp.get("distractors", [])
        if not isinstance(hints_raw, (list, tuple)) or not (3 <= len(hints_raw) <= 5):
            return _fail(
                f"FAIL: La plantilla '{tpl_id}' debe definir entre 3 y 5 pistas explícitas (hints) "
                f"(se recibieron {len(hints_raw) if isinstance(hints_raw, (list, tuple)) else 0})."
            )

        from check_templates import _strip_giveaway_prefix
        hints = []
        anti_socratic_patterns = [
            "evita el error",
            "recuerda no confundir",
            "no confundas",
            "cuidado con el error",
            "no cometas el error",
            "error común",
        ]
        cta_wrong_beliefs = [
            str(d.get("wrong_belief") or "").strip().lower()
            for d in cta_distractors if isinstance(d, dict) and d.get("wrong_belief")
        ]
        for h_idx, h_item in enumerate(hints_raw, start=1):
            h_text = _strip_giveaway_prefix(str(h_item).strip())
            if len(h_text) < 25:
                return _fail(
                    f"FAIL: La pista {h_idx} de '{tpl_id}' tiene menos de 25 caracteres ({len(h_text)} < 25): '{h_text}'."
                )
            h_lower = h_text.lower()
            for pat in anti_socratic_patterns:
                if pat in h_lower:
                    return _fail(
                        f"FAIL: La pista {h_idx} de '{tpl_id}' contiene una muletilla anti-socrática prohibida ('{pat}'): '{h_text}'."
                    )
            for wb in cta_wrong_beliefs:
                if len(wb) >= 12 and wb in h_lower:
                    return _fail(
                        f"FAIL: La pista {h_idx} de '{tpl_id}' copia literalmente la concepción errónea de cta.json ('{wb}')."
                    )
            hints.append(h_text)

        # Retrieve CTA declared distractor IDs
        clean_cta_distractors = []
        for d in cta_distractors:
            if isinstance(d, dict):
                cd = dict(d)
                for rkey in ("wrong_belief", "omitted_step", "remediation_hint", "manifestation"):
                    if isinstance(cd.get(rkey), str):
                        cd[rkey] = _strip_giveaway_prefix(cd[rkey])
                clean_cta_distractors.append(cd)
            else:
                clean_cta_distractors.append(d)

        cta_declared_ids = {d.get("id") for d in clean_cta_distractors if isinstance(d, dict) and d.get("id")}

        # Adapt MC7 generator if applicable
        if interaction_type == "multiple_choice_7_options":
            gen_code = build_adapted_mc7_generator(gen_code, cid, clean_cta_distractors, strict=strict)

        # Determine declared vars from generator callable (with timeout guard) or sandbox or AST
        sample_res = None
        declared_vars: Set[str] = set()
        if callable(gen_raw):
            try:
                import random
                from engine.sandbox import call_with_timeout
                sample_res = call_with_timeout(
                    gen_raw,
                    args=(random.Random(42),),
                    timeout=0.4,
                    seed=42,
                )
                if isinstance(sample_res, dict) and "vars" in sample_res and isinstance(sample_res["vars"], dict):
                    declared_vars = set(str(k) for k in sample_res["vars"].keys())
                elif isinstance(sample_res, (tuple, list)) and len(sample_res) >= 1 and isinstance(sample_res[0], dict):
                    declared_vars = set(str(k) for k in sample_res[0].keys())
            except Exception:
                pass

        if sample_res is None and gen_code:
            try:
                from engine.sandbox import run_code_in_env
                sample_res = run_code_in_env(gen_code, "generate", seed=42, timeout=0.5)
                if isinstance(sample_res, dict) and "vars" in sample_res and isinstance(sample_res["vars"], dict):
                    declared_vars = set(str(k) for k in sample_res["vars"].keys())
                elif isinstance(sample_res, (tuple, list)) and len(sample_res) >= 1 and isinstance(sample_res[0], dict):
                    declared_vars = set(str(k) for k in sample_res[0].keys())
            except Exception:
                pass

        if not declared_vars and gen_code:
            try:
                _gtree = ast.parse(textwrap.dedent(gen_code.strip()))
                for _gnode in ast.walk(_gtree):
                    if isinstance(_gnode, ast.Dict):
                        for _gk, _gv in zip(_gnode.keys, _gnode.values):
                            if isinstance(_gk, ast.Constant) and _gk.value == "vars":
                                if isinstance(_gv, ast.Dict):
                                    declared_vars.update(
                                        str(k.value) for k in _gv.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)
                                    )
                                elif isinstance(_gv, ast.Name):
                                    _vname = _gv.id
                                    for _anode in ast.walk(_gtree):
                                        if isinstance(_anode, ast.Assign) and isinstance(_anode.value, ast.Dict):
                                            if any(isinstance(t, ast.Name) and t.id == _vname for t in _anode.targets):
                                                declared_vars.update(
                                                    str(k.value) for k in _anode.value.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)
                                                )
            except Exception:
                m_vars = re.search(r"['\"]vars['\"]\s*:\s*\{([^}]+)\}", gen_code)
                if m_vars:
                    var_names = re.findall(r"['\"]([a-zA-Z_][a-zA-Z0-9_]*)['\"]\s*:", m_vars.group(1))
                    declared_vars = set(var_names)

        # Distractor validation, dynamic rationale check, and KaTeX guards on sample_res
        if sample_res is not None and isinstance(sample_res, (dict, tuple, list)):
            if isinstance(sample_res, (tuple, list)):
                if len(sample_res) >= 3:
                    s_vars = sample_res[0] if isinstance(sample_res[0], dict) else {}
                    s_corr = str(sample_res[1])
                    s_dists = sample_res[2] if isinstance(sample_res[2], list) else []
                    sample_dict = {"vars": s_vars, "correct": s_corr, "distractors": s_dists}
                elif len(sample_res) == 2:
                    s_vars = sample_res[0] if isinstance(sample_res[0], dict) else {}
                    s_corr = str(sample_res[1])
                    sample_dict = {"vars": s_vars, "correct": s_corr, "distractors": []}
                else:
                    sample_dict = {}
            else:
                sample_dict = sample_res

            # Parametric indicators for dynamic rationale check
            has_var_in_correct = bool(re.search(r"@([a-zA-Z0-9_]+)@", str(sample_dict.get("correct", ""))))
            has_var_in_stem = bool(re.search(r"@([a-zA-Z0-9_]+)@", stem_es)) or any(bool(re.search(r"@([a-zA-Z0-9_]+)@", s)) for s in stem_variants)

            # FIB KaTeX guard
            if interaction_type == "fill_in_the_blank":
                corr_str = str(sample_dict.get("correct", "")).strip()
                if corr_str.startswith("$") and corr_str.endswith("$") and len(corr_str) >= 2:
                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, corr_str)
                    return _fail(
                        f"FAIL: [TPL-FIB-KATEX] La respuesta FIB en '{tpl_id}' ('{corr_str}') (Línea {line_no} en {curr_p.name}) contiene delimitadores '$' externos. "
                        f"En Frontend (FeedbackToast) se formatea automáticamente en modo matemático; retire los '$' externos."
                    )

            # MC7 checks
            if interaction_type == "multiple_choice_7_options":
                dists_list = sample_dict.get("distractors") or []
                if isinstance(dists_list, list) and dists_list:
                    dids_found = []
                    for d_idx, d_item in enumerate(dists_list, start=1):
                        did = None
                        rat = ""
                        val = ""
                        if isinstance(d_item, dict):
                            did = d_item.get("distractor_id") or d_item.get("id") or d_item.get("did")
                            rat = str(d_item.get("error_rationale") or d_item.get("rationale") or "")
                            val = str(d_item.get("value") if "value" in d_item else (d_item.get("content") or ""))
                        elif isinstance(d_item, (tuple, list)):
                            if len(d_item) >= 3:
                                did = str(d_item[0]).strip().replace("_", "-")
                                val = str(d_item[1]).strip()
                                rat = str(d_item[2]).strip()
                            elif len(d_item) == 2 and strict:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, str(d_item[0]))
                                return _fail(
                                    f"FAIL: [TPL-MC7-STRICT] En modo estricto, la 2-tupla (distractor_id, value) está prohibida en MC7 ('{tpl_id}') (Línea {line_no} en {curr_p.name}). "
                                    f"Cada distractor debe ser una 3-tupla (distractor_id, value, error_rationale) con error_rationale >= 20 caracteres: {repr(d_item)}"
                                )
                            elif len(d_item) == 2:
                                did = str(d_item[0]).strip().replace("_", "-")
                                val = str(d_item[1]).strip()

                        if did:
                            dids_found.append(did)
                            if cta_declared_ids and did not in cta_declared_ids:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did)
                                return _fail(
                                    f"FAIL: Distractor ID '{did}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) no está declarado en cta.json para la competencia '{cid}'."
                                )

                        if strict:
                            if len(rat.strip()) < 20:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                return _fail(
                                    f"FAIL: [TPL-MC7-RATIONALE] El distractor '{did}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) tiene error_rationale de longitud {len(rat.strip())} (< 20 caracteres): '{rat}'."
                                )
                            # Dynamic rationale check [TPL-DYNAMIC-RATIONALE]
                            if declared_vars:
                                has_var_in_val = bool(re.search(r"@([a-zA-Z0-9_]+)@", val))
                                is_param_dist = has_var_in_val or has_var_in_correct or has_var_in_stem
                                if is_param_dist:
                                    rat_tokens = set(re.findall(r"@([a-zA-Z0-9_]+)@", rat))
                                    valid_rat_tokens = rat_tokens.intersection(declared_vars)
                                    if not valid_rat_tokens:
                                        line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                        return _fail(
                                            f"FAIL: [TPL-DYNAMIC-RATIONALE] El distractor '{did}' en la plantilla paramétrica '{tpl_id}' (Línea {line_no} en {curr_p.name}) tiene una explicación estática sin variables ('{rat}'). "
                                            f"Debe incluir al menos un token @var@ declarado en vars ({', '.join(sorted(declared_vars))}) para explicar dinámicamente el desvío."
                                        )
                    target_misc = dids_found

            # MS checks
            if interaction_type == "multiple_select":
                opts_list = sample_dict.get("options") or []
                ms_dids = []
                for opt in opts_list:
                    if isinstance(opt, dict) and not opt.get("is_correct"):
                        did = opt.get("distractor_id") or opt.get("id") or opt.get("did")
                        rat = str(opt.get("error_rationale") or opt.get("rationale") or "")
                        val = str(opt.get("value") if "value" in opt else (opt.get("content") or ""))
                        if did:
                            norm_did = str(did).replace("_", "-")
                            ms_dids.append(norm_did)
                            if cta_declared_ids and norm_did not in cta_declared_ids:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, str(did))
                                return _fail(
                                    f"FAIL: Distractor ID '{did}' en opción falsa de '{tpl_id}' (Línea {line_no} en {curr_p.name}) no está declarado en cta.json para la competencia '{cid}'."
                                )
                        if strict:
                            if not did:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, val)
                                return _fail(f"FAIL: [TPL-MS-DISTRACTOR-ID] Opción falsa en multiple_select ('{tpl_id}') (Línea {line_no} en {curr_p.name}) carece de distractor_id.")
                            if len(rat.strip()) < 20:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                return _fail(
                                    f"FAIL: [TPL-MS-RATIONALE] La opción falsa '{did}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) tiene error_rationale de longitud {len(rat.strip())} (< 20 caracteres): '{rat}'."
                                )
                            # Dynamic rationale check [TPL-DYNAMIC-RATIONALE]
                            if declared_vars:
                                has_var_in_val = bool(re.search(r"@([a-zA-Z0-9_]+)@", val))
                                is_param_opt = has_var_in_val or has_var_in_correct or has_var_in_stem
                                if is_param_opt:
                                    rat_tokens = set(re.findall(r"@([a-zA-Z0-9_]+)@", rat))
                                    valid_rat_tokens = rat_tokens.intersection(declared_vars)
                                    if not valid_rat_tokens:
                                        line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                        return _fail(
                                            f"FAIL: [TPL-DYNAMIC-RATIONALE] La opción falsa '{did}' en la plantilla paramétrica '{tpl_id}' (Línea {line_no} en {curr_p.name}) tiene una explicación estática sin variables ('{rat}'). "
                                            f"Debe incluir al menos un token @var@ declarado en vars ({', '.join(sorted(declared_vars))})."
                                        )
                target_misc = list(dict.fromkeys(ms_dids))

        # Normalize non-variable double curly braces {{token}} -> {token} before R-20 validation
        stem_es = normalize_double_braces(stem_es, declared_vars)
        stem_variants = [normalize_double_braces(sv, declared_vars) for sv in stem_variants]
        hints = [normalize_double_braces(h, declared_vars) for h in hints]
        healed_solution = normalize_double_braces(sol_raw, declared_vars)
        healed_solution = re.sub(
            r"\{\{([A-Za-z0-9_]+)\}\}",
            lambda m: f"{{{m.group(1)}}}" if m.group(1) not in declared_vars else m.group(0),
            healed_solution,
        )

        canonical_dict: Dict[str, Any] = {
            "template_id": tpl_id,
            "competency_id": cid,
            "gen_fn_name": gen_fn_name,
            "question_type": qtype,
            "stem_es": stem_es,
            "stem_variants": stem_variants,
            "generator_code": gen_code,
            "verifier_code": ver_code,
            "explanation_es": healed_solution,
            "target_kc": target_kc,
            "target_misconceptions": target_misc,
            "source_reference": src_ref,
            # Schema compatibility fields
            "id": tpl_id,
            "interaction_type": interaction_type,
            "difficulty": difficulty,
            "bloom": bloom,
            "stem": stem_es,
            "generate_py": gen_code,
            "cross_check_py": ver_code,
            "solution": healed_solution,
            "distractor_ids": target_misc,
            "hints": hints,
            "source_file": curr_p.name,
        }

        # Apply mechanical auto-healing
        auto_heal_template_data(canonical_dict, cta_comp=cta_comp)
        canonical_dict = heal_control_chars_in_obj(canonical_dict)

        templates_by_cid.setdefault(cid, []).append(canonical_dict)
        gen_callables_by_cid.setdefault(cid, []).append(gen_raw)

    # 6. Write templates atomically grouped by competency
    compiled_paths: List[Path] = []
    for cid, tpls in templates_by_cid.items():
        base_id = f"T-{cid}" if not cid.startswith("T-") else cid
        for idx, tpl in enumerate(tpls, start=1):
            cur_id = tpl.get("id") or base_id
            needs_normalization = (
                not cur_id.startswith("T-")
                or (len(tpls) > 1 and cur_id == base_id)
                or any(tpls[j].get("id") == cur_id for j in range(len(tpls)) if j != idx - 1)
            )
            if needs_normalization:
                unique_id = f"{base_id}-{idx:02d}"
                tpl["id"] = unique_id
                tpl["template_id"] = unique_id

        out_json_path = templates_dir / f"{cid}.json"
        if len(tpls) == 1:
            payload = tpls[0]
        else:
            payload = {
                "competency_id": cid,
                "templates": tpls,
            }
        _atomic_write_json(out_json_path, payload)
        compiled_paths.append(out_json_path)

    # 7. Execute Strict Validation with check_templates (isolated by shard_id)
    is_clean, raw_errors = check_templates_file_or_dir(
        target_path=compiled_paths,
        cta_path=cta_p,
        num_dry_run_seeds=seeds,
        strict=strict,
        auto_fix=True,
        shard_py=(staged_p if (healed_source and staged_p.is_file()) else shard_data_path),
        shard_id=norm_shard_id,
        from_compile_shard=True,
    )

    # Milestone 3 Tri-Band Multimodal Enforcement Gate [M3-ARCHETYPES]
    m3_errors: List[str] = []
    if strict and eff_min_arch >= 3:
        target_cids = expected_cids if expected_cids else list(templates_by_cid.keys())
        shard_data_name = shard_data_path.name if shard_data_path else f"{norm_shard_id}_data.py"

        def _fn_declares_arch(fn_node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> bool:
            all_args = getattr(fn_node.args, "posonlyargs", []) + fn_node.args.args + getattr(fn_node.args, "kwonlyargs", [])
            return any(a.arg == "arch" for a in all_args)

        def _fn_uses_arch_in_body(fn_node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> bool:
            for b_stmt in fn_node.body:
                for sub in ast.walk(b_stmt):
                    if isinstance(sub, ast.Name) and sub.id == "arch" and isinstance(sub.ctx, ast.Load):
                        # Filter out dummy loads like _ = arch or dummy = arch or unused = arch
                        if isinstance(b_stmt, ast.Assign):
                            if any(isinstance(tgt, ast.Name) and tgt.id in ("_", "dummy", "unused") for tgt in b_stmt.targets):
                                continue
                        # Filter out bare statement expressions like `arch` or `arch == arch`
                        if isinstance(b_stmt, ast.Expr):
                            if isinstance(b_stmt.value, ast.Name) and b_stmt.value.id == "arch":
                                continue
                            if isinstance(b_stmt.value, ast.Compare):
                                if isinstance(b_stmt.value.left, ast.Name) and b_stmt.value.left.id == "arch":
                                    if any(isinstance(comp, ast.Name) and comp.id == "arch" for comp in b_stmt.value.comparators):
                                        continue
                        return True
            return False

        for cid in target_cids:
            tpls = templates_by_cid.get(cid, [])
            gen_callables = gen_callables_by_cid.get(cid, [])
            is_modular_fix = bool(cid in fix_files_by_cid and fix_files_by_cid[cid].is_file())
            source_name = fix_files_by_cid[cid].name if is_modular_fix else shard_data_name

            if len(tpls) < eff_min_arch:
                m3_errors.append(
                    f"{cid}.json ({source_name}): [M3-ARCHETYPES] La competencia '{cid}' define solo {len(tpls)} plantilla(s) en TEMPLATES, "
                    f"pero el contrato Tri-Banda exige mínimo {eff_min_arch} plantillas/arquetipos por competencia."
                )
            else:
                # Verificación Tri-Banda de dificultad
                diffs = {t.get("difficulty") for t in tpls}
                if not {"easy", "medium", "hard"}.issubset(diffs):
                    missing_diffs = sorted(list({"easy", "medium", "hard"} - diffs))
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M3-ARCHETYPES] Cobertura incompleta de bandas de dificultad para '{cid}'. "
                        f"Se requieren las 3 bandas {{'easy', 'medium', 'hard'}}, faltan: {missing_diffs}."
                    )

                # Verificación de diversidad de Bloom (>= 2 distintos)
                blooms = {t.get("bloom") for t in tpls if t.get("bloom")}
                if len(blooms) < 2:
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M3-ARCHETYPES] Diversidad cognitiva insuficiente para '{cid}'. "
                        f"Se requieren al menos 2 niveles Bloom distintos por competencia (encontrados: {sorted(list(blooms))})."
                    )

                # Verificación de práctica activa (FIB o MS)
                cta_c = cta_comp_map.get(cid, {})
                c_type = str(cta_c.get("type", "")).lower()
                is_skill = cid.startswith("Hab-") or c_type in ("skill", "habilidad")
                req_active = 2 if is_skill else 1
                active_tpls = [
                    t for t in tpls
                    if t.get("interaction_type") in ("fill_in_the_blank", "multiple_select")
                    or t.get("question_type") in ("fib", "fill_in_the_blank", "ms", "multiple_select")
                ]
                if len(active_tpls) < req_active:
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M3-ARCHETYPES] Práctica activa insuficiente para '{cid}' "
                        f"({'habilidad' if is_skill else 'concepto/misconception'}). Se requieren al menos {req_active} plantilla(s) "
                        f"de tipo FIB o MS (encontradas: {len(active_tpls)})."
                    )

                # Verificación 1 — Enunciados (stem_es) distintos por arquetipo & detección de clones
                distinct_stems = {t.get("stem_es", "").strip() for t in tpls if t.get("stem_es", "").strip()}
                norm_gen_codes = {
                    re.sub(r"def\s+gen_[a-zA-Z0-9_]+_\d+\s*\(", "def _gen_wrapper_(", t.get("generator_code", "").strip())
                    for t in tpls
                }

                if len(distinct_stems) < len(tpls):
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M3-ARCHETYPES] Competencia '{cid}' repite el mismo enunciado (stem_es) entre sus plantillas ({len(distinct_stems)} únicos de {len(tpls)} plantillas). Cada plantilla debe tener su propio enunciado distintivo."
                    )
                elif len(norm_gen_codes) < min(eff_min_arch, 2):
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M3-ARCHETYPES] Las {len(tpls)} tuplas de '{cid}' en TEMPLATES son clones idénticos (mismo generador)."
                    )

                # Verificación 2 — AST analysis de la fuente efectiva de esta competencia
                cid_sources: List[str] = []
                if is_modular_fix:
                    try:
                        cid_sources.append(fix_files_by_cid[cid].read_text(encoding="utf-8"))
                    except Exception:
                        pass
                else:
                    if healed_source:
                        cid_sources.append(healed_source)
                    elif raw_source:
                        cid_sources.append(raw_source)
                    elif shard_data_path and shard_data_path.is_file():
                        try:
                            cid_sources.append(shard_data_path.read_text(encoding="utf-8"))
                        except Exception:
                            pass

                for t in tpls:
                    gen_c = t.get("generator_code") or t.get("generate_py") or ""
                    if gen_c and gen_c not in cid_sources:
                        cid_sources.append(gen_c)

                cid_ast_funcs: Dict[str, Union[ast.FunctionDef, ast.AsyncFunctionDef]] = {}
                for src_txt in cid_sources:
                    try:
                        parsed_tree = ast.parse(textwrap.dedent(src_txt.strip()))
                        for ast_node in ast.walk(parsed_tree):
                            if isinstance(ast_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                cid_ast_funcs[ast_node.name] = ast_node
                    except Exception:
                        pass

                cid_clean = cid.lower().replace("-", "_")
                cid_compact = cid.lower().replace("-", "")
                cid_candidate_funcs: Set[str] = set()

                for t in tpls:
                    g_fn = t.get("gen_fn_name")
                    if g_fn and g_fn in cid_ast_funcs:
                        cid_candidate_funcs.add(g_fn)
                        w_node = cid_ast_funcs[g_fn]
                        for b_stmt in w_node.body:
                            for sub in ast.walk(b_stmt):
                                if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name):
                                    if sub.func.id in cid_ast_funcs:
                                        cid_candidate_funcs.add(sub.func.id)

                for fname, fnode in cid_ast_funcs.items():
                    if _fn_declares_arch(fnode):
                        if cid_clean in fname.lower() or cid_compact in fname.lower():
                            cid_candidate_funcs.add(fname)
                        elif is_modular_fix or len(target_cids) == 1:
                            cid_candidate_funcs.add(fname)

                checked_fn_names: Set[str] = set()
                for func_name in sorted(cid_candidate_funcs):
                    if func_name in checked_fn_names:
                        continue
                    checked_fn_names.add(func_name)
                    fn_node = cid_ast_funcs.get(func_name)
                    if fn_node and _fn_declares_arch(fn_node):
                        if not _fn_uses_arch_in_body(fn_node):
                            m3_errors.append(
                                f"{cid}.json ({source_name}): [M3-ARCHETYPES] Competencia '{cid}': la función generadora '{func_name}' recibe el parámetro 'arch' pero nunca lo utiliza en su cuerpo, produciendo salidas idénticas en los 4 arquetipos. Ramifica con 'if arch == 1 / elif arch == 2 / elif arch == 3 / else' para variar el problema matemático por arquetipo."
                            )
                    # Pillar 3: Detect artificial debug exceptions in generator functions
                    if fn_node:
                        for sub_ast in ast.walk(fn_node):
                            if isinstance(sub_ast, ast.Raise):
                                exc_name = ""
                                if isinstance(sub_ast.exc, ast.Call) and isinstance(sub_ast.exc.func, ast.Name):
                                    exc_name = sub_ast.exc.func.id
                                elif isinstance(sub_ast.exc, ast.Name):
                                    exc_name = sub_ast.exc.id
                                m3_errors.append(
                                    f"{cid}.json ({source_name}): [TPL-DEBUG-ARTIFACT] La función generadora '{func_name}' contiene una sentencia 'raise {exc_name or ''}' en su cuerpo. Las funciones generadoras de ítems deben retornar un diccionario de variables y opciones, sin sentencias 'raise' de depuración."
                                )
                                break

                # Verificación 3 — Detección de Evasión Trivial y Clones Matemáticos Puros (seed=100 & seed=101)
                if eff_min_arch >= 3 and len(tpls) >= 3:
                    def _eval_tuple_output(t_idx: int, seed_val: int) -> Optional[Tuple[str, str, str]]:
                        c_call = gen_callables[t_idx] if t_idx < len(gen_callables) else None
                        if callable(c_call):
                            try:
                                import random
                                from engine.sandbox import call_with_timeout, _LazyNPRNG
                                rng = random.Random(seed_val)
                                try:
                                    rng.np = _LazyNPRNG(seed_val)
                                except Exception:
                                    pass
                                res = call_with_timeout(
                                    c_call,
                                    args=(rng,),
                                    timeout=0.4,
                                    seed=seed_val,
                                )
                                if isinstance(res, dict):
                                    c_v = str(res.get("correct", ""))
                                    v_d = res.get("vars", {})
                                    v_s = json.dumps(v_d, sort_keys=True, default=str) if isinstance(v_d, dict) else str(v_d)
                                    opts = res.get("options", [])
                                    opts_s = ""
                                    if isinstance(opts, list) and opts:
                                        simplified_opts = [
                                            (str(o.get("value") or o.get("content", "")), bool(o.get("is_correct")))
                                            for o in opts if isinstance(o, dict)
                                        ]
                                        opts_s = json.dumps(sorted(simplified_opts), default=str)
                                    return (c_v, v_s, opts_s)
                                elif isinstance(res, (tuple, list)) and len(res) >= 1 and isinstance(res[0], dict):
                                    v_d = res[0]
                                    v_s = json.dumps(v_d, sort_keys=True, default=str)
                                    return ("", v_s, "")
                            except Exception:
                                pass

                        gen_c = tpls[t_idx].get("generator_code") or tpls[t_idx].get("generate_py") or ""
                        if gen_c:
                            try:
                                from engine.sandbox import run_code_in_env
                                res = run_code_in_env(gen_c, "generate", seed=seed_val, timeout=0.5)
                                if isinstance(res, dict):
                                    c_v = str(res.get("correct", ""))
                                    v_d = res.get("vars", {})
                                    v_s = json.dumps(v_d, sort_keys=True, default=str) if isinstance(v_d, dict) else str(v_d)
                                    opts = res.get("options", [])
                                    opts_s = ""
                                    if isinstance(opts, list) and opts:
                                        simplified_opts = [
                                            (str(o.get("value") or o.get("content", "")), bool(o.get("is_correct")))
                                            for o in opts if isinstance(o, dict)
                                        ]
                                        opts_s = json.dumps(sorted(simplified_opts), default=str)
                                    return (c_v, v_s, opts_s)
                            except Exception:
                                pass
                        return None

                    outs_100 = [_eval_tuple_output(i, 100) for i in range(len(tpls))]
                    valid_100 = [o for o in outs_100 if o is not None]
                    if len(valid_100) == len(tpls) and len(set(valid_100)) < 2:
                        outs_101 = [_eval_tuple_output(i, 101) for i in range(len(tpls))]
                        valid_101 = [o for o in outs_101 if o is not None]
                        if len(valid_101) == len(tpls) and len(set(valid_101)) < 2:
                            m3_errors.append(
                                f"{cid}.json ({source_name}): [M3-ARCHETYPES] Competencia '{cid}': las {len(tpls)} tuplas generan salidas matemáticas idénticas (mismo 'correct', 'vars' y 'options' en la misma semilla). Las plantillas deben producir al menos 2 variantes matemáticas distintas."
                            )

                # Verificación 4 — Detección de Distractores por Multiplicador Arbitrario [DIAG-MAGIC-MULT]
                _magic_mults = (1.333, 0.667, 1.667, 0.333, 1.25, 0.75, 1.5, 0.5, 2.1, 0.45, 1.85, 0.15)
                _distinctive_magic = {1.333, 0.667, 1.667, 0.333, 2.1, 0.45, 1.85, 0.15}
                _num_re = re.compile(r"-?\d+\.\d+|-?\d+")
                try:
                    import zlib
                    from engine.assemble import format_template_string
                    _seed_base = 42 + (zlib.crc32(cid.encode("utf-8")) % 10000)
                except Exception:
                    _seed_base = 10000
                    format_template_string = None

                for t_idx_m, tpl_m in enumerate(tpls):
                    if tpl_m.get("interaction_type") != "multiple_choice_7_options":
                        continue
                    c_call_m = gen_callables[t_idx_m] if t_idx_m < len(gen_callables) else None
                    if not callable(c_call_m):
                        continue
                    gen_c_m = str(tpl_m.get("generator_code") or tpl_m.get("generate_py") or "")
                    has_mult_ast = bool(
                        re.search(r"\bans\s*[\*/]|[\*/]\s*ans\b", gen_c_m)
                        or re.search(r"\b(?:1\.333|0\.667|1\.667|0\.333|2\.1|0\.45|1\.85|0\.15)\b", gen_c_m)
                    )
                    if not has_mult_ast:
                        continue
                    tpl_id_m = tpl_m.get("id") or tpl_m.get("template_id") or f"T-{cid}-{t_idx_m+1:02d}"
                    gen_fn_m = tpl_m.get("gen_fn_name") or getattr(c_call_m, "__name__", "gen_fn")
                    tpl_seed_off = _seed_base + (t_idx_m * 500)
                    eval_seeds = [tpl_seed_off + s_i for s_i in range(20)]
                    hit_seeds: List[int] = []
                    hit_mults_sample: List[float] = []
                    for s_val in eval_seeds:
                        try:
                            import random
                            rng_m = random.Random(s_val)
                            res_m = c_call_m(rng_m)
                            if not isinstance(res_m, dict):
                                continue
                            vars_m = res_m.get("vars", {}) if isinstance(res_m.get("vars"), dict) else {}
                            corr_raw = str(res_m.get("correct", ""))
                            corr_txt = format_template_string(corr_raw, vars_m) if format_template_string else corr_raw
                            dists_raw = res_m.get("distractors", [])
                            if not isinstance(dists_raw, list) or len(dists_raw) < 4:
                                continue
                            c_nums = _num_re.findall(corr_txt)
                            if not c_nums:
                                continue
                            c_val = float(c_nums[-1])
                            if abs(c_val) <= 1e-6 or abs(c_val) in (1.0, 2.0, 4.0):
                                continue
                            matched_m: List[float] = []
                            for d_item in dists_raw:
                                if isinstance(d_item, (tuple, list)) and len(d_item) >= 2:
                                    d_raw = str(d_item[1])
                                elif isinstance(d_item, dict):
                                    d_raw = str(d_item.get("value") or d_item.get("content") or "")
                                else:
                                    continue
                                d_txt = format_template_string(d_raw, vars_m) if format_template_string else d_raw
                                d_nums = _num_re.findall(d_txt)
                                if not d_nums:
                                    continue
                                d_val = float(d_nums[-1])
                                # Guard 1: Skip conceptual distractors sharing the same numerical value as correct answer
                                if abs(d_val - c_val) <= 1e-4:
                                    continue
                                actual_ratio = d_val / c_val if abs(c_val) > 1e-9 else 0.0
                                for m_factor in _magic_mults:
                                    # Ratio check with 5% relative tolerance AND absolute rounding check to reject small-number false positives
                                    if abs(actual_ratio - m_factor) <= 0.05 and abs(d_val - round(c_val * m_factor, 3)) <= 0.0015:
                                        matched_m.append(m_factor)
                                        break
                            dist_hits = [m_f for m_f in matched_m if m_f in _distinctive_magic]
                            if len(dist_hits) >= 2 or len(matched_m) >= 4:
                                hit_seeds.append(s_val)
                                if not hit_mults_sample:
                                    hit_mults_sample = dist_hits[:3] or matched_m[:3]
                        except Exception as e_seed:
                            m3_errors.append(
                                f"{cid}.json ({source_name}): [TPL-EXEC-ERROR] En '{tpl_id_m}' (semilla {s_val}), la función generadora falló con excepción: {type(e_seed).__name__}: {e_seed}"
                            )
                            break
                    if len(hit_seeds) >= 3:
                        eff_loc = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                        loc_obj = ShardDataLineLocator(eff_loc) if eff_loc and eff_loc.is_file() else locator
                        t_info_m = loc_obj.find_tuple_for_question(cid, template_id=tpl_id_m) if loc_obj else None
                        s_off, e_off, _ = loc_obj.find_offending_lines(t_info_m, "diagnostic_rationale_alignment_linter", "multiplicador") if loc_obj else (1, 1, [])
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [DIAG-MAGIC-MULT] En '{tpl_id_m}' (función '{gen_fn_m}', Líneas {s_off}..{e_off} en {source_name}), "
                            f"los distractores numéricos en {len(hit_seeds)} semillas (ej. seed={hit_seeds[0]}) coinciden con multiplicadores arbitrarios prohibidos ({hit_mults_sample}) respecto a la respuesta correcta. "
                            f"Reemplaza los multiplicadores sintéticos sobre 'ans' por las fórmulas algebraicas reales de cada error_rationale."
                        )

                # Verificación 5 — Compuerta de Diversidad de Enunciados [STEM-DIVERSITY-GATE] (Paridad con run.py --stage build)
                if len(tpls) >= 3 and seeds >= 30:
                    try:
                        from engine.diversity import mask_stem_numbers as _mask_stem_nums
                    except Exception:
                        def _mask_stem_nums(st: str) -> str:
                            return re.sub(r"\b\d+(?:\.\d+)?\b", "[NUM]", re.sub(r"\s+", " ", st.strip()))

                    is_true_skill = cid.startswith("Hab-") or (not cid.startswith(("C-", "H-")) and is_skill)
                    quota_build = 30 if is_true_skill else 20
                    req_unique_stems = 15 if quota_build == 30 else 10
                    all_masked_stems: Set[str] = set()
                    stem_line_ranges: List[str] = []
                    eff_loc_s = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                    loc_obj_s = ShardDataLineLocator(eff_loc_s) if eff_loc_s and eff_loc_s.is_file() else locator

                    for t_idx_s, tpl_s in enumerate(tpls):
                        tpl_id_s = tpl_s.get("id") or tpl_s.get("template_id") or f"T-{cid}-{t_idx_s+1:02d}"
                        sv_list = tpl_s.get("stem_variants") or ([tpl_s.get("stem_es")] if tpl_s.get("stem_es") else [])
                        c_call_s = gen_callables[t_idx_s] if t_idx_s < len(gen_callables) else None
                        sample_vars_list: List[Dict[str, Any]] = []
                        if callable(c_call_s):
                            for s_try in (100, 101, 102):
                                try:
                                    import random
                                    r_try = c_call_s(random.Random(s_try))
                                    if isinstance(r_try, dict) and isinstance(r_try.get("vars"), dict):
                                        sample_vars_list.append(r_try["vars"])
                                except Exception:
                                    pass
                        for sv_raw in sv_list:
                            sv_str = str(sv_raw).strip()
                            if not sv_str:
                                continue
                            if sample_vars_list and format_template_string:
                                for sv_vars in sample_vars_list:
                                    rendered_sv = format_template_string(sv_str, sv_vars)
                                    all_masked_stems.add(_mask_stem_nums(rendered_sv))
                            else:
                                dummy_sv = re.sub(r"@[a-zA-Z0-9_]+(?::[^@]+)?@", "100", sv_str)
                                all_masked_stems.add(_mask_stem_nums(dummy_sv))

                        if loc_obj_s:
                            t_info_s = loc_obj_s.find_tuple_for_question(cid, template_id=tpl_id_s)
                            s_ln, e_ln, _ = loc_obj_s.find_offending_lines(t_info_s, "anti_gaming_psychometric_linter", "stem")
                            rng_lbl = f"L{s_ln}..L{e_ln}" if s_ln != e_ln else f"L{s_ln}"
                            if rng_lbl not in stem_line_ranges:
                                stem_line_ranges.append(rng_lbl)

                    if len(all_masked_stems) < req_unique_stems:
                        cat_label = "skills" if is_true_skill else "concepts/facts"
                        req_per_tpl = "6-7" if is_true_skill else "4-5"
                        tot_rec = "18-21" if is_true_skill else "12-15"
                        lines_ctx = f" [{', '.join(stem_line_ranges)} en {source_name}]" if stem_line_ranges else ""
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [STEM-DIVERSITY-GATE] Diagnostic: Stem diversity gate failed for competency '{cid}' "
                            f"(only {len(all_masked_stems)} stems, required >= {req_unique_stems} unique, quota {quota_build} for {cat_label}){lines_ctx}. "
                            f"Provide >= {req_per_tpl} distinct syntactic stems per template (totaling >= {tot_rec})."
                        )

    if m3_errors:
        is_clean = False
        raw_errors = m3_errors + list(raw_errors)

    if not is_clean:
        from check_templates import render_compact_aggregated_errors, count_distinct_shard_error_hunks
        error_count = count_distinct_shard_error_hunks(
            raw_errors, targets=compiled_paths, shard_py=shard_data_path
        )
        compact_report = render_compact_aggregated_errors(
            raw_errors, targets=compiled_paths, shard_py=shard_data_path, max_output_lines=28
        )
        from check_templates import normalize_error_string_for_hash
        normalized_errs = sorted([normalize_error_string_for_hash(str(e)) for e in raw_errors])
        err_hash = hashlib.sha256("\n".join(normalized_errs).encode("utf-8")).hexdigest()

        if state.get("last_err_hash") == err_hash:
            same_error_streak = state.get("same_error_streak", 0) + 1
        else:
            same_error_streak = 1
        state["same_error_streak"] = same_error_streak
        state["last_err_hash"] = err_hash
        state["error_count"] = error_count
        state["has_syntax_error"] = False

        _cleanup_stale_pass_marker()

        if receipt_p:
            try:
                import time
                r_data = {}
                if receipt_p.is_file():
                    try:
                        r_data = json.loads(receipt_p.read_text(encoding="utf-8"))
                    except Exception:
                        r_data = {}
                r_data["shard_id"] = shard_id
                r_data["compiled_status"] = "FAIL"
                r_data["compilation_errors"] = [compact_report]
                r_data["error_count"] = error_count
                r_data["has_syntax_error"] = False
                r_data["compiled_at"] = time.time()
                _atomic_write_json(receipt_p, r_data)
            except Exception:
                pass

        if same_error_streak >= 3:
            terminal_stop = (
                f"\n[-] [CIRCUIT BREAKER HALT: 3 fallos consecutivos idénticos para shard '{shard_id}']. "
                f"STOP, send_message the Director."
            )
            compact_report = compact_report + terminal_stop
            print(terminal_stop, file=sys.stderr)

        print(f"\n[-] FAIL: {len(raw_errors)} errores detectados ({error_count} errores consolidados) al compilar {shard_id}:\n{compact_report}", file=sys.stderr)
        state["last_errors"] = [compact_report]
        _atomic_write_json(compile_att_file, state)
        return False, [compact_report]

    # Clear compilation attempts on success (pass clears the halt)
    if compile_att_file.is_file():
        try:
            compile_att_file.unlink()
        except Exception:
            pass

    import time
    pass_marker = att_dir / f"pass_{norm_shard_id}.json"
    pass_payload = {
        "shard_id": shard_id,
        "status": "PASS",
        "source_sha256": source_sha256,
        "template_counts": {cid: len(tpls) for cid, tpls in templates_by_cid.items()},
        "timestamp": time.time(),
    }
    _atomic_write_json(pass_marker, pass_payload)

    if receipt_p:
        try:
            r_data = {}
            if receipt_p.is_file():
                try:
                    r_data = json.loads(receipt_p.read_text(encoding="utf-8"))
                except Exception:
                    r_data = {}
            r_data["shard_id"] = shard_id
            r_data["compiled_status"] = "PASS"
            r_data["compiled_templates"] = [p.as_posix() for p in compiled_paths]
            r_data["compiled_at"] = time.time()
            _atomic_write_json(receipt_p, r_data)
        except Exception:
            pass

    total_archetypes = sum(len(tpls) for tpls in templates_by_cid.values())
    written_files_str = ", ".join(p.as_posix() for p in compiled_paths)
    print(f"[+] PASS: Shard '{shard_id}' compilado exitosamente ({len(compiled_paths)} competencias, {total_archetypes} plantillas/arquetipos en [{written_files_str}], {seeds} semillas dry-run validadas). STOP: No ejecutes más herramientas y emite tu señal DONE.")
    return True, []


def compile_shard_file(
    shard_data_path: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    strict: bool = True,
    seeds: int = 50,
    min_archetypes: Optional[int] = None,
    **kwargs,
) -> Tuple[bool, List[str]]:
    """Helper for run.py pipeline stage 3 compatibility."""
    return compile_shard(
        work_dir_or_path=shard_data_path,
        shard_id=kwargs.get("shard_id"),
        strict=strict,
        seeds=seeds,
        output_dir=output_dir,
        min_archetypes=min_archetypes if min_archetypes is not None else kwargs.get("min_archetypes"),
        **kwargs,
    )


def main():
    parser = argparse.ArgumentParser(description="Deterministic Python Tuple Compiler for Content-to-Course v3.21 Shards")
    parser.add_argument("shard_data_path", nargs="?", default=None, help="Optional positional path to shard_XX_data.py")
    parser.add_argument("--input", "-i", dest="input_path", default=None, help="Optional path to shard_XX_data.py")
    parser.add_argument("--output", "-o", dest="output_path", default=None, help="Optional output path or directory")
    parser.add_argument("--cta", default=None, help="Optional path to cta.json")
    parser.add_argument("--manifest", default=None, help="Optional path to manifest")
    parser.add_argument("--work", "--work-dir", dest="work", default="work", help="Path to work directory (default: work)")
    parser.add_argument("--shard", default=None, help="Shard ID to compile (e.g. shard_01)")
    parser.add_argument("--output-dir", default=None, help="Output directory for templates (e.g. work/templates)")
    parser.add_argument("--strict", action="store_true", default=True, help="Enforce strict validation (default: True)")
    parser.add_argument("--no-strict", dest="strict", action="store_false", help="Bypass strict validation")
    parser.add_argument("--seeds", type=int, default=50, help="Number of dry-run seeds (default: 50)")
    parser.add_argument("--min-archetypes", dest="min_archetypes", type=int, default=None, help="Minimum disjoint archetypes (tuples) required per competency in TEMPLATES (default: 3)")
    args = parser.parse_args()

    work_or_path = args.input_path or args.shard_data_path or args.work
    s_id = args.shard
    receipt_path = None
    eff_out_dir = args.output_dir
    if args.output_path:
        if str(args.output_path).lower().endswith(".json"):
            receipt_path = args.output_path
        elif not eff_out_dir:
            eff_out_dir = args.output_path

    if work_or_path == "work" and not (Path("work/shards/pre_shard_manifest.json").is_file() or Path("work/pre_shard_manifest.json").is_file()):
        inferred = infer_work_dir(work_or_path, shard_id=s_id)
        if inferred != Path(work_or_path):
            work_or_path = str(inferred)

    success, _ = compile_shard(
        work_dir_or_path=work_or_path,
        shard_id=s_id,
        strict=args.strict,
        seeds=args.seeds,
        output_dir=eff_out_dir,
        output_path=receipt_path,
        cta_path=args.cta,
        manifest_path=args.manifest,
        min_archetypes=args.min_archetypes,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
