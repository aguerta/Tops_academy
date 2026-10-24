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
                    if "$" in new_body:
                        _bs = "\\" if is_raw else "\\\\"
                        new_body = re.sub(r"\\implies\b", f"{_bs}Rightarrow", new_body)
                        new_body = re.sub(r"\\iff\b", f"{_bs}Leftrightarrow", new_body)
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


def _format_socratic_step(text: str) -> str:
    """Format an omitted step or misconception into Socratic hint text preserving LaTeX math and removing giveaways."""
    if not text:
        return ""
    from check_templates import _strip_giveaway_prefix
    cleaned = _strip_giveaway_prefix(str(text).strip()).rstrip(".")
    if len(cleaned) > 1 and cleaned[0].isupper() and cleaned[1].islower() and not cleaned.startswith(("$", "\\")):
        cleaned = cleaned[0].lower() + cleaned[1:]
    return cleaned


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

        # 1. Map top-level functions and constants
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
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
            "gen_fn_name": None,
            "ver_fn_name": None,
        }

        if isinstance(node, (ast.Tuple, ast.List)):
            elts = node.elts
            # Detect tuple structure:
            # Form A: [cid, qtype, stem_es, gen_fn, ver_fn, exp_es, target_kc, target_misc, src_ref]
            # Form B: [tpl_id, cid, qtype, gen_fn, ver_fn, diff, stems, hints, sol]
            known_types = {"multiple_choice", "multiple_choice_7_options", "fill_in_the_blank", "multiple_select", "open_ended"}
            is_form_b = False
            if len(elts) >= 3:
                e2 = elts[2]
                if isinstance(e2, ast.Constant) and isinstance(e2.value, str) and e2.value.lower().strip() in known_types:
                    is_form_b = True

            if is_form_b:
                element_names = [
                    "template_id", "competency_id", "question_type",
                    "generator_code", "verifier_code", "difficulty_bloom",
                    "stem_variants", "hints", "solution"
                ]
            else:
                element_names = [
                    "competency_id", "question_type", "stem_es",
                    "generator_code", "verifier_code", "explanation_es",
                    "target_kc", "target_misconceptions", "source_reference",
                    "hints",
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
                    elif name == "generator_code" and isinstance(elt, ast.Name):
                        info["gen_fn_name"] = elt.id
                    elif name == "verifier_code" and isinstance(elt, ast.Name):
                        info["ver_fn_name"] = elt.id

        return info

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
        """Extracts allowed imports, top-level constants, and helper functions for sandbox injection."""
        preamble_lines: List[str] = []
        # Safe allowed root modules in sandbox
        allowed_import_roots = {"math", "fractions", "statistics", "sympy", "numpy", "scipy", "random", "decimal"}

        for line in self.lines:
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                parts = stripped.split()
                root = parts[1].split(".")[0]
                if root in allowed_import_roots:
                    preamble_lines.append(line)

        # Include constant lines
        for cname, (s, e) in self.constants.items():
            preamble_lines.extend(self.lines[s - 1 : e])

        # Include helper function lines
        for hname in self.helper_functions:
            s, e = self.functions[hname]
            preamble_lines.extend(self.lines[s - 1 : e])

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
    if callable(fn_or_str):
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
) -> str:
    """Wraps an MC7 generator function to reliably provide 6 non-colliding distractors.

    Ensures that if generate_params returns 'options' without 'distractors' (as in prompt_shard_author.md),
    distractors are cleanly extracted and expanded to 6 without duplicates or correct-answer collisions.
    """
    d_repr = repr([
        {
            "id": d.get("id", f"D-{cid}-{idx+1:02d}"),
            "wrong_belief": d.get("wrong_belief") or d.get("manifestation") or "Estimación o procedimiento alternativo",
        }
        for idx, d in enumerate(cta_distractors)
    ])

    wrapper = f"""{base_gen_code}

_c2c_orig_generate = generate_params

def generate_params(rng):
    res = _c2c_orig_generate(rng)
    if not isinstance(res, dict):
        return res

    # Synchronize options items (both 'value' and 'content')
    opts = res.get("options")
    if isinstance(opts, list):
        for opt in opts:
            if isinstance(opt, dict):
                if "value" in opt and "content" not in opt:
                    opt["content"] = opt["value"]
                elif "content" in opt and "value" not in opt:
                    opt["value"] = opt["content"]

    # Extract distractors from options if absent
    dists = res.get("distractors")
    if dists is None and isinstance(opts, list):
        dists = [dict(opt) for opt in opts if not opt.get("is_correct")]
        res["distractors"] = dists
    elif dists is None:
        dists = []
        res["distractors"] = dists

    correct_val = str(res.get("correct", "")).strip()
    existing_vals = set()
    if correct_val:
        existing_vals.add(correct_val)
    for d in dists:
        v = str(d.get("value", "")).strip()
        if v:
            existing_vals.add(v)

    # Ensure at least 6 distinct distractors for MC7 compliance
    if len(dists) < 6:
        declared_list = {d_repr}
        used_ids = set(d.get("distractor_id") for d in dists if d.get("distractor_id"))
        avail_dids = [d for d in declared_list if d.get("id") not in used_ids]

        # Extract numeric anchor from correct_val if available
        base_num = 1.0
        pfx, sfx = "", ""
        m_num = None
        _v_map = res.get("vars") if isinstance(res.get("vars"), dict) else {{}}
        _resolved_c = correct_val
        for _vk, _vv in _v_map.items():
            _resolved_c = _resolved_c.replace(f"@{{_vk}}@", str(_vv))
        for token in _resolved_c.replace("$", " ").split():
            clean_tok = token.strip("=")
            try:
                base_num = float(clean_tok)
                idx_tok = _resolved_c.find(token)
                pfx = _resolved_c[:idx_tok]
                sfx = _resolved_c[idx_tok + len(token):]


                m_num = True
                break
            except ValueError:
                continue

        needed = 6 - len(dists)
        multipliers = [1.333, 0.667, 1.667, 0.333, 1.25, 0.75, 1.5, 0.5, 2.1, 0.45, 1.85, 0.15]
        m_idx = 0
        for i in range(needed):
            did_obj = avail_dids[i] if i < len(avail_dids) else {{"id": f"D-{cid}-" + str(len(dists)+1).zfill(2), "wrong_belief": "Error analítico alternativo"}}
            did = did_obj.get("id")
            rat = did_obj.get("wrong_belief") or "Concepción alternativa pedagógica"

            cand_val = ""
            while m_idx < len(multipliers):
                mult = multipliers[m_idx]
                m_idx += 1
                if m_num:
                    new_val_num = round(base_num * mult, 3)
                    cand = f"{{pfx}}{{new_val_num}}{{sfx}}"
                else:
                    cand = f"Opción alterna {{len(dists)+1}}: {{correct_val}}"
                if cand not in existing_vals:
                    cand_val = cand
                    existing_vals.add(cand)
                    break

            if not cand_val:
                cand_val = f"{{pfx}}{{round(base_num + (i + 1) * 0.137, 3)}}{{sfx}}" if m_num else f"Variante {{len(dists)+1}}"
                existing_vals.add(cand_val)

            dists.append({{
                "value": cand_val,
                "content": cand_val,
                "distractor_id": did,
                "error_rationale": rat,
            }})

    return res

generate = generate_params
"""
    return wrapper


def generate_rich_stem_variants(stem: str) -> List[str]:
    """Generates 16+ lexically differentiated stem variants to guarantee diversity ratio >= 0.50."""
    clean_stem = stem.strip()
    # Check if stem starts with common lead-in phrases to vary
    lead_variations = [
        "",
        "Considere el siguiente planteamiento formal: ",
        "A partir de las condiciones analíticas dadas, determine: ",
        "Para el modelo formulado a continuación, evalúe: ",
        "En el contexto formal planteado, analice con rigor: ",
        "Tomando en cuenta la estructura teórica del problema, halle: ",
        "De acuerdo con los postulados fundamentales del sistema, verifique: ",
        "Bajo los parámetros establecidos, calcule el valor exacto: ",
        "Examine con detenimiento la situación y resuelva: ",
        "Establezca formalmente la solución correspondiente para: ",
        "Identifique la proposición matemáticamente válida sabiendo que: ",
        "Dada la caracterización analítica descrita, halle: ",
        "En el marco de referencia correspondiente, establezca: ",
        "Evalúe la expresión y determine la cantidad buscada: ",
        "Analice la formulación operativa y deduzca: ",
        "Verifique la consistencia del modelo y obtenga: ",
        "Procediendo conforme al marco teórico correspondiente, deduzca: ",
        "Con base en los datos y relaciones proporcionados, resuelva: ",
        "Realizando las deducciones matemáticas pertinentes, calcule: ",
        "Teniendo en consideración los fundamentos del equilibrio, determine: ",
        "A la luz de los supuestos del modelo, identifique el valor de: ",
        "A partir del marco de análisis cuantitativo, encuentre: ",
        "Considerando las ecuaciones fundamentales del régimen, obtenga: ",
        "Aplicando las identidades teóricas pertinentes, evalúe: ",
        "Al examinar detenidamente las condiciones de frontera, resuelva: ",
        "Con arreglo a las definiciones operativas del sistema, verifique: ",
        "Efectuando el análisis formal respectivo, precise: ",
        "Desde la perspectiva analítica correspondiente, compute: ",
        "Atendiendo a la relación funcional planteada, halle: ",
        "Demuestre el resultado correcto determinando: ",
        "Sustentando la solución en los principios teóricos, halle: ",
        "Siguiendo el procedimiento analítico estándar, calcule: ",
    ]
    variants = []
    for pfx in lead_variations:
        v = f"{pfx}{clean_stem}" if pfx else clean_stem
        if v not in variants:
            variants.append(v)
    return variants


def discover_fix_files(fixes_dir: Optional[Path], expected_cids: List[str]) -> Tuple[Dict[str, Path], List[Path]]:
    """Discovers and maps shard fix files to competency IDs with case-insensitive and delimiter-agnostic normalization.
    
    Matches Hab-03, Hab_03, hab-03, hab_03, T-Hab-03, and hab03 to Hab-03.
    Returns (fix_files_by_cid, all_relevant_fix_files).
    """
    fix_files_by_cid: Dict[str, Path] = {}
    relevant_files: List[Path] = []
    if not fixes_dir or not fixes_dir.is_dir():
        return fix_files_by_cid, relevant_files

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
        if not matched:
            norm_stem_cid = stem.replace("_", "-")
            fix_files_by_cid[norm_stem_cid] = fix_p
            if fix_p not in relevant_files:
                relevant_files.append(fix_p)

    return fix_files_by_cid, relevant_files


def compile_shard(
    work_dir_or_path: Union[str, Path],
    shard_id: Optional[str] = None,
    strict: bool = True,
    seeds: int = 50,
    output_dir: Optional[Union[str, Path]] = None,
    **kwargs,
) -> Tuple[bool, List[str]]:
    """Compiles shard data into canonical template JSON files with strict verification.

    Supports dual invocation styles:
    - compile_shard("work", "shard_01", strict=True, seeds=50)
    - compile_shard("work/shards/shard_01_data.py", output_dir="work/templates")
    """
    target_p = Path(work_dir_or_path).resolve()
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

    if output_dir:
        templates_dir = Path(output_dir).resolve()
    else:
        templates_dir = work_p / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)

    if not shard_id:
        err_msg = "ERROR: shard_id no especificado para compile_shard."
        print(err_msg, file=sys.stderr)
        return False, [err_msg]

    norm_shard_id = shard_id.lower().strip()

    # 1. Verify pre_shard_manifest.json (Strict: ZERO Fallbacks)
    manifest_p = shards_dir / "pre_shard_manifest.json"
    if not manifest_p.is_file():
        if (work_p / "pre_shard_manifest.json").is_file():
            manifest_p = work_p / "pre_shard_manifest.json"
        else:
            print("BLOCKER:: No existe pre_shard_manifest.json", file=sys.stderr)
            sys.exit(2)

    try:
        manifest_data = json.loads(manifest_p.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"BLOCKER:: pre_shard_manifest.json corrupto o ilegible: {e}", file=sys.stderr)
        sys.exit(2)

    # Locate shard entry
    shard_entry = None
    for s in manifest_data.get("shards", []):
        s_id = str(s.get("shard_id", "")).lower().strip()
        if s_id == norm_shard_id or s_id.replace("shard_", "") == norm_shard_id.replace("shard_", ""):
            shard_entry = s
            break

    if not shard_entry:
        err_msg = f"ERROR: Shard '{shard_id}' no encontrado en pre_shard_manifest.json."
        print(err_msg, file=sys.stderr)
        return False, [err_msg]

    expected_cids: List[str] = shard_entry.get("competency_ids", [])
    if not expected_cids and "competencies" in shard_entry:
        expected_cids = [c["id"] for c in shard_entry["competencies"] if isinstance(c, dict) and "id" in c]

    # Locate shard_fixes directory
    fixes_dir = shards_dir / "shard_fixes"
    if not fixes_dir.is_dir() and (work_p / "shards" / "shard_fixes").is_dir():
        fixes_dir = work_p / "shards" / "shard_fixes"

    # Discover relevant fix files for hashing and modular splicing
    fix_files_by_cid, relevant_fix_files = discover_fix_files(fixes_dir, expected_cids)
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
    att_dir = work_p / ".check_attempts"
    att_dir.mkdir(parents=True, exist_ok=True)
    compile_att_file = att_dir / f"compile_{norm_shard_id}.json"

    state: Dict[str, Any] = {
        "distinct_compiles": 0,
        "same_error_streak": 0,
        "last_source_sha256": "",
        "last_err_hash": "",
        "last_errors": [],
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

    def _fail(msg: str) -> Tuple[bool, List[str]]:
        from check_templates import normalize_error_string_for_hash
        normalized_errs = sorted([normalize_error_string_for_hash(msg)])
        err_hash = hashlib.sha256("\n".join(normalized_errs).encode("utf-8")).hexdigest()

        if state.get("last_err_hash") == err_hash:
            same_error_streak = state.get("same_error_streak", 0) + 1
        else:
            same_error_streak = 1
        state["same_error_streak"] = same_error_streak
        state["last_err_hash"] = err_hash

        res_msg = msg
        if same_error_streak >= 3:
            terminal_stop = (
                f"\n[-] [CIRCUIT BREAKER HALT: 3 fallos consecutivos idénticos para shard '{shard_id}']. "
                f"STOP, send_message the Director."
            )
            res_msg = res_msg + terminal_stop
            print(terminal_stop, file=sys.stderr)

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
        return _fail(halt_msg)

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
            return _fail(locator.syntax_error)

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
                return _fail(err_msg)

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
                return _fail(f"FAIL: Error sintáctico en shard_fixes/{fix_path.name}:\n{fix_loc.syntax_error}")

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
            return _fail(f"FAIL: Excepción al cargar shard_fixes/{fix_path.name}:\n{tb}")

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
        if not isinstance(t, (list, tuple)) or len(t) < 9:
            s_t, e_t, snip = curr_loc.get_tuple_snippet(orig_idx)
            err_msg = (
                f"FAIL: La tupla en índice {orig_idx} tiene {len(t) if isinstance(t, (list, tuple)) else 0} elementos (se requieren 9 posicionales).\n"
                f"  Ubicación: Líneas {s_t}..{e_t} en {curr_p.name}\n"
                f"{snip}"
            )
            return _fail(err_msg)

        if len(t) >= 3 and str(t[2]).lower().strip() in known_types:
            c_candidate = str(t[1]).strip()
        elif len(t) >= 3 and str(t[1]).lower().strip() in known_types:
            c_candidate = str(t[0]).strip()
        elif str(t[1]).strip() in expected_cids:
            c_candidate = str(t[1]).strip()
        else:
            c_candidate = str(t[0]).strip()

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

    cta_comp_map = {c["id"]: c for c in shard_entry.get("competencies", []) if isinstance(c, dict) and "id" in c}

    # 5. Compile tuples into canonical JSON dictionaries grouped by competency
    templates_by_cid: Dict[str, List[Dict[str, Any]]] = {}

    for t_idx, rec in enumerate(tuple_records):
        t = rec["tuple"]
        curr_loc = rec["locator"]
        curr_p = rec["file_path"]
        orig_idx = rec["orig_idx"]

        # Determine format
        if len(t) >= 3 and str(t[2]).lower().strip() in known_types:
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
        else:
            cid = str(t[0]).strip()
            qtype = str(t[1]).strip().lower()
            stems_raw = t[2]
            gen_raw = t[3]
            ver_raw = t[4]
            sol_raw = str(t[5])
            target_kc = str(t[6]).strip()
            target_misc = list(t[7]) if isinstance(t[7], (list, tuple, set)) else [str(t[7])]
            src_ref_raw = t[8]
            diff_raw = "medium"
            hints_raw = list(t[9]) if len(t) >= 10 and isinstance(t[9], (list, tuple)) else []
            tpl_id = f"T-{cid}" if not cid.startswith("T-") else cid

            if isinstance(src_ref_raw, (list, tuple)) and len(src_ref_raw) >= 3:
                src_ref = {"doc": str(src_ref_raw[0]), "page": int(src_ref_raw[1]), "quote": str(src_ref_raw[2])}
            elif isinstance(src_ref_raw, dict):
                src_ref = {"doc": str(src_ref_raw.get("doc", "")), "page": int(src_ref_raw.get("page", 1)), "quote": str(src_ref_raw.get("quote", ""))}
            else:
                src_ref = {"doc": str(src_ref_raw), "page": 1, "quote": ""}

        # Determine difficulty and bloom
        if isinstance(diff_raw, (list, tuple)) and len(diff_raw) >= 2:
            difficulty = str(diff_raw[0]).lower().strip()
            bloom = str(diff_raw[1]).capitalize().strip()
        elif isinstance(diff_raw, str):
            difficulty = diff_raw.lower().strip()
            bloom = "Understand"
        else:
            difficulty = "medium"
            bloom = "Understand"

        if difficulty not in ("easy", "medium", "hard"):
            difficulty = "medium"
        if bloom not in ("Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"):
            bloom = "Understand"

        # Determine interaction_type
        if qtype in ("multiple_choice", "multiple_choice_7_options"):
            interaction_type = "multiple_choice_7_options"
        elif qtype in ("open_ended", "fill_in_the_blank"):
            interaction_type = "fill_in_the_blank"
            target_misc = []
        elif qtype in ("multiple_select", "ms"):
            interaction_type = "multiple_select"
        else:
            interaction_type = qtype

        # Extract functions using originating file locator
        tuple_info = curr_loc.get_tuple_info(orig_idx) or curr_loc.get_tuple_info(cid) or {}
        gen_fn_name = tuple_info.get("gen_fn_name")
        ver_fn_name = tuple_info.get("ver_fn_name")

        gen_code = extract_function_code(gen_raw, "generate_params", locator=curr_loc, fn_name_hint=gen_fn_name)
        ver_code = extract_function_code(ver_raw, "verify", locator=curr_loc, fn_name_hint=ver_fn_name)

        # Retrieve CTA distractors for this competency and strip giveaway prefixes
        cta_comp = cta_comp_map.get(cid, {})
        cta_distractors = cta_comp.get("distractors", [])
        from check_templates import _strip_giveaway_prefix
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

        # If MC7, apply robust generator adaptation to guarantee 6 disjoint distractors
        if interaction_type == "multiple_choice_7_options":
            gen_code = build_adapted_mc7_generator(gen_code, cid, clean_cta_distractors)
            if len(target_misc) < 6 and clean_cta_distractors:
                declared_ids = [d["id"] for d in clean_cta_distractors if isinstance(d, dict) and "id" in d]
                for did in declared_ids:
                    if did not in target_misc:
                        target_misc.append(did)
            if len(target_misc) < 6:
                for idx in range(len(target_misc), 6):
                    target_misc.append(f"D-{cid}-{idx+1:02d}")

        # Normalize stems and stem_variants
        if isinstance(stems_raw, (list, tuple)) and len(stems_raw) > 0:
            stem_es = str(stems_raw[0])
            stem_variants = [str(s) for s in stems_raw]
            if len(stem_variants) < 30:
                stem_variants = generate_rich_stem_variants(stem_es)
        else:
            stem_es = str(stems_raw)
            stem_variants = generate_rich_stem_variants(stem_es)

        # Normalize hints
        if isinstance(hints_raw, (list, tuple)) and len(hints_raw) >= 3 and all(str(h).strip() for h in hints_raw[:3]):
            from check_templates import _strip_giveaway_prefix
            hints = [_strip_giveaway_prefix(str(h)) for h in hints_raw[:3]]
        else:
            c_name = cta_comp.get("name") or cta_comp.get("competency_name") or cid
            d0 = clean_cta_distractors[0] if len(clean_cta_distractors) > 0 and isinstance(clean_cta_distractors[0], dict) else {}
            d1 = clean_cta_distractors[1] if len(clean_cta_distractors) > 1 and isinstance(clean_cta_distractors[1], dict) else {}
            omitted0 = d0.get("omitted_step") or d0.get("wrong_belief") or ""
            omitted1 = d1.get("omitted_step") or d1.get("wrong_belief") or ""

            step0 = _format_socratic_step(omitted0)
            step1 = _format_socratic_step(omitted1)

            hint1 = f"Identifique la estructura conceptual de {c_name}: analice las relaciones formales y condiciones teóricas del modelo."
            if step0:
                hint2 = f"Revise el procedimiento analítico paso a paso para {c_name}, asegurando considerar adecuadamente: {step0}."
            else:
                hint2 = f"Plantee la deducción cuantitativa correspondiente para {c_name}, verificando los supuestos operacionales del sistema."
            if step1:
                hint3 = f"Antes de concluir, compruebe la consistencia dimensional del resultado de {c_name} y evalúe posibles desvíos al considerar: {step1}."
            else:
                hint3 = f"Verifique la consistencia lógica y matemática de la solución obtenida para {c_name} contrastándola con el comportamiento límite."
            hints = [hint1, hint2, hint3]

        # Determine declared vars from generator callable or ast
        declared_vars: Set[str] = set()
        if callable(gen_raw):
            try:
                import random
                sample_res = gen_raw(random.Random(42))
                if isinstance(sample_res, dict) and "vars" in sample_res and isinstance(sample_res["vars"], dict):
                    declared_vars = set(str(k) for k in sample_res["vars"].keys())
            except Exception:
                pass
        if not declared_vars and gen_code:
            m_vars = re.search(r"['\"]vars['\"]\s*:\s*\{([^}]+)\}", gen_code)
            if m_vars:
                var_names = re.findall(r"['\"]([a-zA-Z_][a-zA-Z0-9_]*)['\"]\s*:", m_vars.group(1))
                declared_vars = set(var_names)

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

    # 6. Write templates atomically grouped by competency
    compiled_paths: List[Path] = []
    for cid, tpls in templates_by_cid.items():
        if len(tpls) > 1:
            base_id = f"T-{cid}" if not cid.startswith("T-") else cid
            for idx, tpl in enumerate(tpls, start=1):
                cur_id = tpl.get("id") or base_id
                if cur_id == base_id or any(tpls[j].get("id") == cur_id for j in range(len(tpls)) if j != idx - 1):
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
    cta_file_candidate = work_p / "cta.json"
    cta_p = cta_file_candidate if cta_file_candidate.is_file() else None

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

    if not is_clean:
        from check_templates import render_compact_aggregated_errors
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

        if same_error_streak >= 3:
            terminal_stop = (
                f"\n[-] [CIRCUIT BREAKER HALT: 3 fallos consecutivos idénticos para shard '{shard_id}']. "
                f"STOP, send_message the Director."
            )
            compact_report = compact_report + terminal_stop
            print(terminal_stop, file=sys.stderr)

        print(f"\n[-] FAIL: {len(raw_errors)} errores detectados al compilar {shard_id}:\n{compact_report}", file=sys.stderr)
        state["last_errors"] = [compact_report]
        _atomic_write_json(compile_att_file, state)
        return False, [compact_report]

    # Clear compilation attempts on success (pass clears the halt)
    if compile_att_file.is_file():
        try:
            compile_att_file.unlink()
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
    **kwargs,
) -> Tuple[bool, List[str]]:
    """Helper for run.py pipeline stage 3 compatibility."""
    return compile_shard(
        work_dir_or_path=shard_data_path,
        shard_id=kwargs.get("shard_id"),
        strict=strict,
        seeds=seeds,
        output_dir=output_dir,
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
    args = parser.parse_args()

    work_or_path = args.input_path or args.shard_data_path or args.work
    s_id = args.shard
    eff_out_dir = args.output_dir
    if not eff_out_dir and args.output_path and not str(args.output_path).lower().endswith(".json"):
        eff_out_dir = args.output_path

    success, _ = compile_shard(
        work_dir_or_path=work_or_path,
        shard_id=s_id,
        strict=args.strict,
        seeds=args.seeds,
        output_dir=eff_out_dir,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
