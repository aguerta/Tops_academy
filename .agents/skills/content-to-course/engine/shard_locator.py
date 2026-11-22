"""AST-based source line locator and diagnostic line finder for shard_*_data.py files."""

import ast
import re
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union


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
        self.function_segments: Dict[str, str] = {}
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
                seg = ast.get_source_segment(self.source_text, node)
                if seg:
                    self.function_segments[node.name] = seg
            elif isinstance(node, ast.Assign):
                if (
                    len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Name)
                    and isinstance(node.value, ast.Lambda)
                ):
                    fn_name = node.targets[0].id
                    end_lineno = getattr(node, "end_lineno", node.lineno)
                    self.functions[fn_name] = (node.lineno, end_lineno)
                    seg = ast.get_source_segment(self.source_text, node)
                    if seg:
                        self.function_segments[fn_name] = seg
                else:
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id != "TEMPLATES":
                            end_lineno = getattr(node, "end_lineno", node.lineno)
                            self.constants[target.id] = (node.lineno, end_lineno)
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name) and node.target.id != "TEMPLATES":
                    if isinstance(node.value, ast.Lambda):
                        fn_name = node.target.id
                        end_lineno = getattr(node, "end_lineno", node.lineno)
                        self.functions[fn_name] = (node.lineno, end_lineno)
                        seg = ast.get_source_segment(self.source_text, node)
                        if seg:
                            self.function_segments[fn_name] = seg
                    else:
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
        elif isinstance(node, ast.Dict):
            info["is_form_c"] = True
            for k_node, v_node in zip(node.keys, node.values):
                if not (isinstance(k_node, ast.Constant) and isinstance(k_node.value, str)):
                    continue
                k = k_node.value
                k_start = getattr(v_node, "lineno", start_line)
                k_end = getattr(v_node, "end_lineno", k_start)
                info["elements"][k] = {
                    "start_line": k_start,
                    "end_line": k_end,
                    "node_type": type(v_node).__name__,
                }
                if k in ("id", "tpl_id", "template_id") and isinstance(v_node, ast.Constant) and isinstance(v_node.value, str):
                    info["template_id"] = v_node.value
                elif k in ("cid", "competency_id") and isinstance(v_node, ast.Constant) and isinstance(v_node.value, str):
                    info["competency_id"] = v_node.value
                elif k in ("qtype", "question_type") and isinstance(v_node, ast.Constant) and isinstance(v_node.value, str):
                    info["question_type"] = v_node.value.strip().lower()
                elif k in ("band", "difficulty_bloom") and isinstance(v_node, (ast.Tuple, ast.List)) and len(v_node.elts) >= 2:
                    d_elt, b_elt = v_node.elts[0], v_node.elts[1]
                    if isinstance(d_elt, ast.Constant) and isinstance(d_elt.value, str):
                        info["difficulty"] = d_elt.value.strip().lower()
                    if isinstance(b_elt, ast.Constant) and isinstance(b_elt.value, str):
                        info["bloom"] = b_elt.value.strip()
                elif k == "difficulty" and isinstance(v_node, ast.Constant) and isinstance(v_node.value, str):
                    info["difficulty"] = v_node.value.strip().lower()
                elif k == "bloom" and isinstance(v_node, ast.Constant) and isinstance(v_node.value, str):
                    info["bloom"] = v_node.value.strip()
                elif k in ("gen", "generator_code") and isinstance(v_node, ast.Name):
                    info["gen_fn_name"] = v_node.id
                elif k in ("ver", "verifier_code") and isinstance(v_node, ast.Name):
                    info["ver_fn_name"] = v_node.id
                elif k in ("stems", "stem_variants") and isinstance(v_node, ast.Name):
                    info["stems_var"] = v_node.id
                elif k == "hints" and isinstance(v_node, ast.Name):
                    info["hints_var"] = v_node.id
                elif k in ("sol", "solution") and isinstance(v_node, ast.Name):
                    info["sol_var"] = v_node.id

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
            if hname in getattr(self, "function_segments", {}):
                helper_src = self.function_segments[hname]
            else:
                s, e = self.functions[hname]
                helper_src = "\n".join(self.lines[s - 1 : e])
            preamble_lines.append(textwrap.dedent(helper_src).strip())

        return "\n".join(preamble_lines).strip()
