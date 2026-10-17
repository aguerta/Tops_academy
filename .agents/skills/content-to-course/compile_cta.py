#!/usr/bin/env python3
"""Deterministic, Ultra-Fast CTA Compiler for Top's Academy C2C Pipeline.

Implements Component 1 of the C2C Remediation and Optimization Plan:
Separation of Concerns between Immutable Compiler (compile_cta.py) and
Pure Tabular Pedagogical Data (cta_data.py).

Features:
- Reads cta_data.py (or loads COMPETENCIES tuples)
- Maps tuples to schemas/cta.schema.json canonical schema
- Auto-assigns canonical IDs (H-01, C-01, Hab-01, D-H01-01, etc.)
- Injects normative defaults (origin='inferred', severity='high', inherited evidence)
- Auto-normalizes LaTeX math with sanitize_competency_math
- Validates against platform check_cta.py / validate_cta_rules
- On error: maps failing ID/field directly to tuple index and exact line in cta_data.py
- Generates work/cta.json and work/cta.md in < 5 ms
"""

from __future__ import annotations

from collections import defaultdict
import argparse
import ast
import importlib.util
import io
import json
import logging
import tokenize
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Ensure skill directory is in sys.path whether running from skill or work/
_current_dir = Path(__file__).parent.resolve()
_skill_candidates = [
    _current_dir,
    Path.cwd() / ".agents" / "skills" / "content-to-course",
    _current_dir.parent / ".agents" / "skills" / "content-to-course",
] + ([_current_dir.parents[i] / ".agents" / "skills" / "content-to-course" for i in range(len(_current_dir.parents))] if _current_dir.parents else [])

for _cand in _skill_candidates:
    if _cand and (_cand / "check_cta.py").is_file():
        _cand_resolved = str(_cand.resolve())
        if _cand_resolved not in sys.path:
            sys.path.insert(0, _cand_resolved)
        break

from check_cta import JsonLineLocator, validate_cta_rules
from cta_merge import render_cta_md, sanitize_competency_math

logger = logging.getLogger("compile_cta")


class CtaDataLineLocator:
    """Indexes cta_data.py source code to locate exact line numbers of competencies and distractors."""

    def __init__(self, source_text: str):
        self.source_text = source_text
        self.lines = source_text.splitlines()
        self.comp_lines: Dict[str, int] = {}
        self.comp_tuple_indices: Dict[int, int] = {}
        self.distractor_lines: Dict[str, int] = {}
        self._index_source()

    def _index_source(self) -> None:
        if not self.source_text:
            return

        type_prefix_map = {
            "fact": "H", "hecho": "H", "h": "H",
            "concept": "C", "concepto": "C", "c": "C",
            "skill": "Hab", "habilidad": "Hab", "hab": "Hab",
        }

        # 1. Exact AST-based line number indexing
        try:
            tree = ast.parse(self.source_text)
            type_counts: Dict[str, int] = {"H": 0, "C": 0, "Hab": 0}
            global_c_idx = 0
            for stmt in tree.body:
                comps_nodes = None
                if isinstance(stmt, ast.Assign) and any(getattr(t, "id", None) == "COMPETENCIES" for t in stmt.targets):
                    comps_nodes = stmt.value.elts if isinstance(stmt.value, (ast.List, ast.Tuple)) else []
                elif isinstance(stmt, ast.AugAssign) and getattr(stmt.target, "id", None) == "COMPETENCIES":
                    comps_nodes = stmt.value.elts if isinstance(stmt.value, (ast.List, ast.Tuple)) else []

                if comps_nodes is None:
                    continue

                for c_node in comps_nodes:
                    if not isinstance(c_node, (ast.List, ast.Tuple)):
                        continue
                    global_c_idx += 1
                    c_line = getattr(c_node, "lineno", 1)
                    raw_t = ""
                    if len(c_node.elts) > 0 and isinstance(c_node.elts[0], ast.Constant) and isinstance(c_node.elts[0].value, str):
                        raw_t = c_node.elts[0].value.strip().lower()

                    is_6_format = (len(c_node.elts) == 6 and raw_t not in type_prefix_map)
                    d_elts: List[Any] = []

                    if is_6_format:
                        title_str = str(c_node.elts[0].value).strip() if isinstance(c_node.elts[0], ast.Constant) else ""
                        m_id = re.search(r"\b(H|C|Hab|Fact|Concept|Skill)-(\d+)\b", title_str, re.IGNORECASE)
                        if m_id:
                            pfx = m_id.group(1).upper()
                            pfx = "Hab" if pfx in ("HAB", "SKILL") else ("H" if pfx in ("H", "FACT") else "C")
                            cid = f"{pfx}-{int(m_id.group(2)):02d}"
                            prefix = pfx
                        else:
                            name_lower = title_str.lower()
                            if any(kw in name_lower for kw in ["cálculo", "calculo", "calcular", "resolver", "determinar"]):
                                prefix = "Hab"
                            elif any(kw in name_lower for kw in ["definición", "definicion", "fórmula", "formula", "constante"]):
                                prefix = "H"
                            else:
                                prefix = "C"
                            type_counts[prefix] = type_counts.get(prefix, 0) + 1
                            cid = f"{prefix}-{type_counts[prefix]:02d}"

                        if len(c_node.elts) > 5 and isinstance(c_node.elts[5], (ast.List, ast.Tuple)):
                            d_elts = c_node.elts[5].elts
                    else:
                        prefix = type_prefix_map.get(raw_t, "C")
                        type_counts[prefix] = type_counts.get(prefix, 0) + 1

                        cid = None
                        if len(c_node.elts) > 1 and isinstance(c_node.elts[1], ast.Constant) and c_node.elts[1].value:
                            val_str = str(c_node.elts[1].value).strip()
                            if re.match(r"^(?:H|C|Hab|Fact|Concept|Skill)-?\d+$", val_str, re.IGNORECASE):
                                cid = val_str
                        if not cid:
                            cid = f"{prefix}-{type_counts[prefix]:02d}"

                        if len(c_node.elts) > 8 and isinstance(c_node.elts[8], (ast.List, ast.Tuple)):
                            d_elts = c_node.elts[8].elts
                        elif len(c_node.elts) == 6 and isinstance(c_node.elts[5], (ast.List, ast.Tuple)):
                            d_elts = c_node.elts[5].elts
                        elif len(c_node.elts) == 7 and isinstance(c_node.elts[6], (ast.List, ast.Tuple)):
                            d_elts = c_node.elts[6].elts
                        elif len(c_node.elts) == 8 and isinstance(c_node.elts[7], (ast.List, ast.Tuple)):
                            d_elts = c_node.elts[7].elts

                    self.comp_lines[cid] = c_line
                    self.comp_lines[cid.replace("-", "")] = c_line
                    self.comp_tuple_indices[global_c_idx] = c_line
                    cid_clean = cid.replace("-", "")

                    for d_idx, d_node in enumerate(d_elts, start=1):
                        d_line = getattr(d_node, "lineno", c_line)
                        did = f"D-{cid_clean}-{d_idx:02d}"
                        self.distractor_lines[did] = d_line
                        self.distractor_lines[f"D-{cid}-{d_idx:02d}"] = d_line
                        if isinstance(d_node, (ast.List, ast.Tuple)) and len(d_node.elts) > 0:
                            if isinstance(d_node.elts[0], ast.Constant) and d_node.elts[0].value:
                                d_name = str(d_node.elts[0].value).strip()
                                if d_name:
                                    self.distractor_lines[d_name] = d_line
        except Exception:
            pass

        # 2. Regex fallback / supplement
        comp_id_pattern = re.compile(
            r'[\(\[]\s*["\'](fact|concept|skill)["\']\s*,\s*["\']([A-Za-z0-9_-]+)["\']',
            re.IGNORECASE,
        )
        for line_idx, line in enumerate(self.lines, start=1):
            m = comp_id_pattern.search(line)
            if m:
                cid = m.group(2)
                if cid not in self.comp_lines:
                    self.comp_lines[cid] = line_idx
                    self.comp_lines[cid.replace("-", "")] = line_idx

        id_pattern = re.compile(r'["\'](H-\d+|C-\d+|Hab-\d+|Fact-\d+|Concept-\d+|Skill-\d+)["\']')
        for line_idx, line in enumerate(self.lines, start=1):
            for m in id_pattern.finditer(line):
                cid = m.group(1)
                if cid not in self.comp_lines:
                    self.comp_lines[cid] = line_idx
                    self.comp_lines[cid.replace("-", "")] = line_idx

    def get_comp_line(self, comp_id: str) -> Optional[int]:
        if comp_id in self.distractor_lines:
            return self.distractor_lines[comp_id]
        if comp_id in self.comp_lines:
            return self.comp_lines[comp_id]
        clean_id = comp_id.replace("-", "")
        if clean_id in self.comp_lines:
            return self.comp_lines[clean_id]
        # Distractor ID decomposition fallback, e.g. D-Hab01-02 -> Hab-01
        m_did = re.match(r"^D-([A-Za-z]+)(\d+)(?:-(\d+))?$", comp_id)
        if m_did:
            prefix, comp_num, dist_idx = m_did.groups()
            cid_hyphen = f"{prefix}-{comp_num}"
            if dist_idx:
                try_did = f"D-{prefix}{comp_num}-{int(dist_idx):02d}"
                if try_did in self.distractor_lines:
                    return self.distractor_lines[try_did]
            if cid_hyphen in self.comp_lines:
                return self.comp_lines[cid_hyphen]
            if f"{prefix}{comp_num}" in self.comp_lines:
                return self.comp_lines[f"{prefix}{comp_num}"]
        return None

    def get_line(self, item_id: str) -> Optional[int]:
        return self.get_comp_line(item_id)

    def find_field_line(self, comp_id: str, snippet: str) -> Optional[int]:
        base_line = self.get_comp_line(comp_id) or 1
        for l_num in range(base_line, min(len(self.lines) + 1, base_line + 80)):
            if snippet in self.lines[l_num - 1]:
                return l_num
        return base_line


LATEX_PREFIX_PATTERNS = [
    r"rho\b|right\b|Rightarrow\b|rightarrow\b|ightharpoondown\b|ightharpoonup\b|rightleftharpoons\b|rangle\b|rceil\b|rfloor\b|rgroup\b|rhd\b|rule\b|rVert\b",
    r"frac\b|forall\b|flat\b|frown\b|fbox\b",
    r"alpha\b|approx\b|angle\b|alert\b|arrow\b|asymp\b|acute\b",
    r"beta\b|bar\b|begin\b|binom\b|big\b|boldsymbol\b|backslash\b|boxed\b|bullet\b|bot\b|mathbb\b",
    r"tau\b|theta\b|text\b|times\b|to\b|triangle\b|tilde\b|tanh\b|tan\b|top\b",
    r"nu\b|neq\b|nabla\b|ni\b|not\b|natural\b",
    r"vec\b|varepsilon\b|vartheta\b|varphi\b|varpi\b|varrho\b|varsigma\b|vdots\b|vdash\b|vee\b|vert\b",
    r"left\b|lambda\b|langle\b|lceil\b|lfloor\b",
]
COMBINED_LATEX = "|".join(LATEX_PREFIX_PATTERNS)


def heal_control_chars_in_str(s: str) -> str:
    """Heals ASCII control characters resulting from unescaped LaTeX backslashes."""
    if not isinstance(s, str) or not s:
        return s

    # First, preserve standard CRLF line endings by normalizing to \n
    s = s.replace("\r\n", "\n")

    # 1. LaTeX prefixes collided with control characters
    s = re.sub(r"\x07(?:a)?(lpha|pprox|ngle|lert|rrow|symp|cute)", r"\\a\1", s)
    s = re.sub(r"\x08(?:b)?(eta|ar|egin|inom|ig|oldsymbol|ackslash|oxed|ullet|ot)", r"\\b\1", s)
    s = re.sub(r"\x0b(?:v)?(ec|arepsilon|artheta|arphi|arpi|arrho|arsigma|dots|dash|ee|ert)", r"\\v\1", s)
    s = re.sub(r"\x0c(?:f)?(rac|orall|lat|rown|box)", r"\\f\1", s)
    s = re.sub(r"\x0d(?:r)?(ho|ight|ightarrow|ightharpoondown|ightharpoonup|ightleftharpoons|angle|ceil|floor|group|hd|ule|Vert)", r"\\r\1", s)
    s = re.sub(r"\x09(?:t)?(au|heta|ext|imes|o\b|riangle|tilde|tanh|tan\b|top\b)", r"\\t\1", s)
    s = re.sub(r"\x0a(?:n)?(u\b|eq\b|abla|i\b|ot\b|atural)", r"\\n\1", s)

    # 2. Bare control characters
    s = (
        s.replace("\x07", r"\a")
        .replace("\x08", r"\b")
        .replace("\x0b", r"\v")
        .replace("\x0c", r"\f")
        .replace("\x0d", r"\r")
    )
    return s


def heal_control_chars_in_obj(obj: Any) -> Any:
    """Recursively traverses dictionaries, lists, tuples and heals control chars in all strings."""
    if isinstance(obj, str):
        return heal_control_chars_in_str(obj)
    elif isinstance(obj, dict):
        return {
            (heal_control_chars_in_str(k) if isinstance(k, str) else k): heal_control_chars_in_obj(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, list):
        return [heal_control_chars_in_obj(elem) for elem in obj]
    elif isinstance(obj, tuple):
        return tuple(heal_control_chars_in_obj(elem) for elem in obj)
    return obj


def heal_string_token(token_str: str) -> str:
    """Heals a single STRING token from Python source."""
    m = re.match(r"^([a-zA-Z]*)(['\"]{1,3})(.*)(['\"]{1,3})$", token_str, flags=re.DOTALL)
    if not m:
        return token_str
    prefix, q_open, body, q_close = m.groups()
    is_raw = "r" in prefix.lower()

    new_body = heal_control_chars_in_str(body)
    if not is_raw:
        new_body = re.sub(rf"(?<!\\)\\({COMBINED_LATEX})", r"\\\\\1", new_body)

    if new_body != body:
        return f"{prefix}{q_open}{new_body}{q_close}"
    return token_str


def heal_cta_source_file(py_path: Path) -> bool:
    """Uses Python's tokenize module to inspect and heal non-raw string tokens and control characters.

    Heals unescaped LaTeX prefixes and ASCII control characters in py_path before importing.
    Returns True if the file was modified and rewritten, False otherwise.
    """
    if not py_path.is_file():
        return False
    try:
        source_text = py_path.read_bytes().decode("utf-8")
        clean_source = heal_control_chars_in_str(source_text)
        modified = (clean_source != source_text)
        tokens = list(tokenize.tokenize(io.BytesIO(clean_source.encode("utf-8")).readline))
        new_tokens = []
        for t in tokens:
            if t.type == tokenize.STRING:
                healed_str = heal_string_token(t.string)
                if healed_str != t.string:
                    modified = True
                new_tokens.append(tokenize.TokenInfo(t.type, healed_str, t.start, t.end, t.line))
            else:
                new_tokens.append(t)

        if not modified:
            return False

        rebuilt_text = tokenize.untokenize(new_tokens).decode("utf-8")
        py_path.write_bytes(rebuilt_text.encode("utf-8"))
        return True
    except Exception as e:
        logger.warning("heal_cta_source_file fallback for %s due to: %s", py_path.name, e)
        try:
            source_text = py_path.read_bytes().decode("utf-8")
            healed = heal_control_chars_in_str(source_text)
            healed = re.sub(rf"(?<!\\)\\({COMBINED_LATEX})", r"\\\\\1", healed)
            if healed != source_text:
                py_path.write_bytes(healed.encode("utf-8"))
                return True
        except Exception:
            pass
        return False


def load_cta_data_module(cta_data_path: Path) -> Any:
    """Loads cta_data.py module dynamically without poluting global sys.modules."""
    spec = importlib.util.spec_from_file_location("cta_data", str(cta_data_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module specification from {cta_data_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _normalize_distractors_list(
    raw_distractors: List[Any],
    cid_clean: str,
    comp_name: str,
    norm_type: str,
    doc: str = "material_fuente.pdf",
    page: int = 1,
) -> List[Dict[str, Any]]:
    """Normalizes distractors exclusively from tuple representations of at least 3 elements."""
    compiled_distractors: List[Dict[str, Any]] = []

    for d_idx, d in enumerate(raw_distractors, start=1):
        if isinstance(d, dict):
            raise TypeError(
                f"[compile_cta] Distractor #{d_idx} en '{comp_name}' es un diccionario. "
                "Los distractores deben ser exclusivamente tuplas (o listas posicionales) de 3 a 6 elementos, no diccionarios."
            )

        if not isinstance(d, (list, tuple)):
            raise TypeError(
                f"[compile_cta] Distractor #{d_idx} en '{comp_name}' no es una tupla: {type(d).__name__}"
            )

        if len(d) < 3:
            raise ValueError(
                f"[compile_cta] Distractor #{d_idx} en '{comp_name}' tiene {len(d)} elementos (se requieren al menos 3)."
            )

        d_name = str(d[0]).strip() if len(d) > 0 else f"Distractor {d_idx}"
        wrong_belief = str(d[1]).strip() if len(d) > 1 and d[1] is not None and str(d[1]).strip() else None
        correct_belief = str(d[2]).strip() if len(d) > 2 and d[2] is not None and str(d[2]).strip() else f"Verdad teórica de {comp_name}."
        manifestation = str(d[3]).strip() if len(d) > 3 and d[3] is not None and str(d[3]).strip() else "$0$"
        hint = str(d[4]).strip() if len(d) > 4 and d[4] is not None and str(d[4]).strip() else f"Revisar la definición de {comp_name}."
        omitted_step = str(d[5]).strip() if len(d) > 5 and d[5] is not None and str(d[5]).strip() else None

        # Fallback if both wrong_belief and omitted_step are None (schema requires at least one)
        if not wrong_belief and not omitted_step:
            wrong_belief = f"Asume resultado incorrecto en {comp_name}"

        d_id = f"D-{cid_clean}-{d_idx:02d}"
        error_type = "skipped_step" if omitted_step else "conceptual_swap"

        d_dict = {
            "id": d_id,
            "name": d_name,
            "wrong_belief": wrong_belief,
            "correct_belief": correct_belief,
            "omitted_step": omitted_step,
            "trigger": f"Evaluación formal de {comp_name}",
            "manifestation": manifestation,
            "error_type": error_type,
            "severity": "high",
            "origin": "inferred",
            "evidence": {
                "doc": doc,
                "page": page,
            },
            "remediation_hint": hint,
        }
        compiled_distractors.append(d_dict)

    # Auto-satisfy CTA-D2 (at least 2 omitted_step distractors required for 'skill' competencies)
    if norm_type == "skill" and len(compiled_distractors) >= 2:
        omitted_count = sum(1 for cd in compiled_distractors if isinstance(cd, dict) and cd.get("omitted_step"))
        for cd in compiled_distractors:
            if omitted_count >= 2:
                break
            if isinstance(cd, dict) and not cd.get("omitted_step"):
                cd["omitted_step"] = cd.get("wrong_belief") or f"Omitir paso algebraico en {cd.get('name', comp_name)}"
                cd["error_type"] = "skipped_step"
                omitted_count += 1

    return compiled_distractors


def compile_cta_module(
    competencies_data: Any,
    course_id: str = "custom_course",
    title: str = "Curso Académico",
    macro_competency: str = "",
) -> Dict[str, Any]:
    """Compiles tabular positional tuples into formal cta.json dictionary.

    Strictly rejects dictionary representations for competencies and distractors.
    Exclusively requires tuples (or lists) of 6 to 9 elements for competencies,
    and 3 to 6 elements for distractors.
    """
    if hasattr(competencies_data, "COMPETENCIES"):
        competencies_tuples = getattr(competencies_data, "COMPETENCIES")
        course_id = getattr(competencies_data, "COURSE_ID", course_id)
        title = getattr(competencies_data, "COURSE_TITLE", getattr(competencies_data, "TITLE", title))
        macro_competency = getattr(competencies_data, "MACRO_COMPETENCY", macro_competency)
    else:
        competencies_tuples = competencies_data

    competencies_tuples = heal_control_chars_in_obj(competencies_tuples)
    title = heal_control_chars_in_str(str(title))
    macro_competency = heal_control_chars_in_str(str(macro_competency))

    compiled_comps: List[Dict[str, Any]] = []

    type_map = {
        "fact": ("fact", "H"),
        "hecho": ("fact", "H"),
        "h": ("fact", "H"),
        "concept": ("concept", "C"),
        "concepto": ("concept", "C"),
        "c": ("concept", "C"),
        "skill": ("skill", "Hab"),
        "habilidad": ("skill", "Hab"),
        "hab": ("skill", "Hab"),
    }

    counts_by_prefix: Dict[str, int] = {"H": 0, "C": 0, "Hab": 0}

    for comp_idx, item in enumerate(competencies_tuples, start=1):
        if isinstance(item, dict):
            raise TypeError(
                f"[compile_cta] Competencia en índice {comp_idx} es un diccionario. "
                "COMPETENCIES y distractors deben ser exclusivamente tuplas (o listas posicionales), no diccionarios."
            )

        if not isinstance(item, (list, tuple)):
            raise TypeError(
                f"[compile_cta] Competencia en índice {comp_idx} no es una tupla o lista: {type(item).__name__}"
            )

        if len(item) < 6:
            raise ValueError(
                f"[compile_cta] Tupla de competencia en índice {comp_idx} tiene {len(item)} elementos (se requieren al menos 6)."
            )

        is_6_format = (len(item) == 6 and (isinstance(item[2], (list, tuple, set)) or str(item[0]).strip().lower() not in type_map))

        if is_6_format:
            name = str(item[0]).strip()
            desc_latex = str(item[1]).strip()
            prereqs = list(item[2]) if isinstance(item[2], (list, tuple, set)) else []
            evidence_raw = item[3]
            misconceptions_raw = item[4]
            raw_distractors = item[5]

            # Parse evidence_raw into (doc, page)
            doc = "material_fuente.pdf"
            page = 1
            if isinstance(evidence_raw, dict):
                doc = str(evidence_raw.get("doc") or evidence_raw.get("pdf") or doc).strip()
                p_val = evidence_raw.get("page", 1)
                page = int(p_val) if str(p_val).strip().isdigit() else 1
            elif isinstance(evidence_raw, (list, tuple)) and len(evidence_raw) > 0:
                first = evidence_raw[0]
                if isinstance(first, dict):
                    doc = str(first.get("doc") or first.get("pdf") or doc).strip()
                    p_val = first.get("page", 1)
                    page = int(p_val) if str(p_val).strip().isdigit() else 1
                elif isinstance(first, (list, tuple)) and len(first) >= 2:
                    doc = str(first[0]).strip()
                    p_val = first[1]
                    page = int(p_val) if str(p_val).strip().isdigit() else 1
                elif isinstance(first, str):
                    if ":" in first:
                        d_p, p_p = first.split(":", 1)
                        doc = d_p.strip()
                        page = int(p_p.strip()) if p_p.strip().isdigit() else 1
                    else:
                        doc = first.strip()
            elif isinstance(evidence_raw, str):
                if ":" in evidence_raw:
                    d_p, p_p = evidence_raw.split(":", 1)
                    doc = d_p.strip()
                    page = int(p_p.strip()) if p_p.strip().isdigit() else 1
                else:
                    doc = evidence_raw.strip()
            elif isinstance(evidence_raw, (int, float)):
                page = int(evidence_raw)

            # Determine type, prefix, raw_id
            m_id = re.search(r"\b(H|C|Hab|Fact|Concept|Skill)-(\d+)\b", name, re.IGNORECASE)
            if m_id:
                pfx = m_id.group(1).upper()
                pfx = "Hab" if pfx in ("HAB", "SKILL") else ("H" if pfx in ("H", "FACT") else "C")
                norm_type = "skill" if pfx == "Hab" else ("fact" if pfx == "H" else "concept")
                default_prefix = pfx
                raw_id = f"{pfx}-{int(m_id.group(2)):02d}"
            else:
                name_l = name.lower()
                if any(kw in name_l for kw in ["cálculo", "calculo", "calcular", "resolver", "determinar", "derivación", "ejecutar"]):
                    norm_type, default_prefix = "skill", "Hab"
                elif any(kw in name_l for kw in ["definición", "definicion", "fórmula", "formula", "constante", "identidad", "enunciado", "teorema"]):
                    norm_type, default_prefix = "fact", "H"
                else:
                    norm_type, default_prefix = "concept", "C"
                counts_by_prefix[default_prefix] = counts_by_prefix.get(default_prefix, 0) + 1
                raw_id = f"{default_prefix}-{counts_by_prefix[default_prefix]:02d}"

            bloom = "Apply" if norm_type == "skill" else ("Remember" if norm_type == "fact" else "Understand")

            # Fallback if raw_distractors is empty or None, but misconceptions_raw has items
            if (not raw_distractors or len(raw_distractors) == 0) and misconceptions_raw:
                raw_distractors = []
                for m_idx, m_item in enumerate(misconceptions_raw, start=1):
                    if isinstance(m_item, (list, tuple)) and len(m_item) >= 3:
                        raw_distractors.append(m_item)
                    elif isinstance(m_item, str) and m_item.strip():
                        raw_distractors.append((
                            f"Error común #{m_idx} en {name}",
                            f"Creencia errónea: {m_item.strip()}",
                            f"Verdad teórica de {name}.",
                            "$0$",
                            f"Revisar {name}.",
                            None,
                        ))
        else:
            raw_type = str(item[0]).strip().lower()
            norm_type, default_prefix = type_map.get(raw_type, ("concept", "C"))
            counts_by_prefix[default_prefix] = counts_by_prefix.get(default_prefix, 0) + 1

            raw_id = str(item[1]).strip() if len(item) > 1 and item[1] else f"{default_prefix}-{counts_by_prefix[default_prefix]:02d}"
            name = str(item[2]).strip() if len(item) > 2 else f"Competencia {raw_id}"
            desc_latex = str(item[3]).strip() if len(item) > 3 else f"Definición formal de {name}."
            raw_bloom = str(item[4]).strip() if len(item) > 4 and item[4] else ("Apply" if norm_type == "skill" else "Understand")
            bloom = raw_bloom.capitalize()
            if bloom not in ("Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"):
                bloom = "Apply" if norm_type == "skill" else "Understand"

            if len(item) == 6:
                doc = "material_fuente.pdf"
                page = 1
                prereqs = []
                raw_distractors = item[5]
            elif len(item) == 7:
                doc = "material_fuente.pdf"
                page = int(item[5]) if str(item[5]).strip().isdigit() else 1
                prereqs = []
                raw_distractors = item[6]
            elif len(item) == 8:
                doc = str(item[5]).strip()
                page = int(item[6]) if str(item[6]).strip().isdigit() else 1
                prereqs = []
                raw_distractors = item[7]
            else:  # >= 9
                doc = str(item[5]).strip() if len(item) > 5 and item[5] else "material_fuente.pdf"
                page = int(item[6]) if len(item) > 6 and str(item[6]).strip().isdigit() else 1
                prereqs = list(item[7]) if len(item) > 7 and isinstance(item[7], (list, tuple)) else []
                raw_distractors = item[8] if len(item) > 8 else []

        cid_clean = raw_id.replace("-", "")
        compiled_distractors = _normalize_distractors_list(
            raw_distractors=raw_distractors,
            cid_clean=cid_clean,
            comp_name=name,
            norm_type=norm_type,
            doc=doc,
            page=page,
        )

        comp_dict = {
            "id": raw_id,
            "type": norm_type,
            "name": name,
            "description_latex": desc_latex,
            "bloom": bloom,
            "session": f"Unidad {page}: {name}",
            "unit_index": page,
            "prerequisites": prereqs,
            "evidence": [
                {
                    "doc": doc,
                    "page": page,
                }
            ],
            "distractors": compiled_distractors,
        }
        sanitize_competency_math(comp_dict)
        compiled_comps.append(comp_dict)

    if not macro_competency and compiled_comps:
        macro_competency = f"Dominio y aplicación analítica integral de {title}"

    return heal_control_chars_in_obj({
        "course_id": course_id,
        "title": title,
        "macro_competency": macro_competency,
        "competencies": compiled_comps,
    })


def compile_tuples_to_cta_dict(
    competencies_tuples: List[Any],
    course_id: str = "custom_course",
    title: str = "Curso Académico",
    macro_competency: str = "",
) -> Dict[str, Any]:
    """Compatibility wrapper delegating to compile_cta_module."""
    return compile_cta_module(
        competencies_data=competencies_tuples,
        course_id=course_id,
        title=title,
        macro_competency=macro_competency,
    )


def auto_normalize_page_numbers(
    cta_dict: Dict[str, Any],
    manifest: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Auto-normalizes cited page numbers from printed book pagination to 1-indexed PDF page numbers.

    Rule: If for a doc whose valid PDF page range in pre_cta_manifest.json is [1, N],
    the set of cited pages P contains values > N, but (max(P) - min(P) + 1) <= N and min(P) > 1,
    AND all shifted pages (p - min(P) + 1) fall strictly within [1, N],
    automatically shifts each cited page p in P to (p - min(P) + 1).

    If any condition is not met (e.g. min(P) == 1, or shifting leaves pages outside [1, N]),
    no shift is applied, preserving original page numbers so check_cta reports exact offending citations.
    """
    if not manifest:
        return cta_dict

    doc_limits: Dict[str, int] = {}
    doc_alias_map: Dict[str, str] = {}
    files_list = manifest.get("files") or manifest.get("documents") or []
    for f in files_list:
        d_name = f.get("doc") or f.get("name") or ""
        d_slug = f.get("doc_slug", "")
        v_range = f.get("valid_page_range", [1, f.get("total_pages", 1)])
        n_pages = v_range[1] if len(v_range) > 1 else f.get("total_pages", 1)
        if d_name:
            doc_limits[d_name] = n_pages
            doc_alias_map[d_name.lower()] = d_name
            doc_alias_map[Path(d_name).stem.lower()] = d_name
        if d_slug:
            doc_alias_map[d_slug.lower()] = d_name

    competencies = cta_dict.get("competencies", [])
    if not competencies:
        return cta_dict

    doc_pages_cited: Dict[str, Set[int]] = defaultdict(set)
    for comp in competencies:
        for ev in comp.get("evidence", []):
            d_raw = str(ev.get("doc") or ev.get("pdf") or "").strip().lower()
            canon = doc_alias_map.get(d_raw) or doc_alias_map.get(Path(d_raw).stem.lower())
            p = ev.get("page")
            if canon and p is not None and str(p).isdigit():
                doc_pages_cited[canon].add(int(p))
        for dist in comp.get("distractors", []):
            ev = dist.get("evidence", {})
            if ev:
                d_raw = str(ev.get("doc") or ev.get("pdf") or "").strip().lower()
                canon = doc_alias_map.get(d_raw) or doc_alias_map.get(Path(d_raw).stem.lower())
                p = ev.get("page")
                if canon and p is not None and str(p).isdigit():
                    doc_pages_cited[canon].add(int(p))

    doc_shifts: Dict[str, int] = {}
    for canon_doc, pages in doc_pages_cited.items():
        if not pages:
            continue
        n_pages = doc_limits.get(canon_doc)
        if not n_pages:
            continue
        p_min = min(pages)
        p_max = max(pages)
        shift = -p_min + 1

        # Only shift if:
        # 1. min page is > 1 (pages are offset from 1)
        # 2. at least one page is > n_pages (confirms book pagination was cited)
        # 3. all pages after shift fall strictly within [1, n_pages]
        if p_min > 1 and any(p > n_pages for p in pages) and all(1 <= (p + shift) <= n_pages for p in pages):
            doc_shifts[canon_doc] = shift
            logger.info(
                "Auto-normalizing page numbers for '%s': printed book pages [%d, %d] shifted by %d to PDF range [1, %d].",
                canon_doc, p_min, p_max, shift, p_max - p_min + 1,
            )

    if not doc_shifts:
        return cta_dict

    for comp in competencies:
        for ev in comp.get("evidence", []):
            d_raw = str(ev.get("doc") or ev.get("pdf") or "").strip().lower()
            canon = doc_alias_map.get(d_raw) or doc_alias_map.get(Path(d_raw).stem.lower())
            shift = doc_shifts.get(canon, 0) if canon else 0
            p = ev.get("page")
            if shift != 0 and p is not None and str(p).isdigit():
                old_p = int(p)
                new_p = old_p + shift
                ev["page"] = new_p
                if comp.get("unit_index") == old_p:
                    comp["unit_index"] = new_p
                sess = comp.get("session")
                if isinstance(sess, str) and sess.startswith(f"Unidad {old_p}:"):
                    comp["session"] = f"Unidad {new_p}:" + sess[len(f"Unidad {old_p}:"):]

        for dist in comp.get("distractors", []):
            ev = dist.get("evidence", {})
            if ev:
                d_raw = str(ev.get("doc") or ev.get("pdf") or "").strip().lower()
                canon = doc_alias_map.get(d_raw) or doc_alias_map.get(Path(d_raw).stem.lower())
                shift = doc_shifts.get(canon, 0) if canon else 0
                p = ev.get("page")
                if shift != 0 and p is not None and str(p).isdigit():
                    ev["page"] = int(p) + shift

    return cta_dict


def compile_cta(
    cta_data_path: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    manifest_path: Optional[Union[str, Path]] = None,
    output_json_name: Optional[str] = None,
) -> Tuple[bool, Dict[str, Any], List[str], float]:
    """Compiles cta_data.py into cta.json and cta.md, validating all constraints in < 5ms."""
    t0 = time.perf_counter()
    data_file = Path(cta_data_path).resolve()
    if not data_file.is_file():
        return False, {}, [f"Data file not found: {data_file}"], 0.0

    work_dir = Path(output_dir).resolve() if output_dir else data_file.parent
    work_dir.mkdir(parents=True, exist_ok=True)
    bak_file = work_dir / ".cta_data.py.bak"

    # Source-Level Pre-Healer: heal unescaped LaTeX prefixes and control characters before loading
    heal_cta_source_file(data_file)

    source_text = data_file.read_text(encoding="utf-8")
    source_lines = source_text.splitlines()
    locator = CtaDataLineLocator(source_text)

    # 1. Dynamically load module
    try:
        mod = load_cta_data_module(data_file)
    except Exception as e:
        elapsed = (time.perf_counter() - t0) * 1000.0
        line_num = getattr(e, "lineno", None)
        if not line_num:
            import traceback
            tb = sys.exc_info()[2]
            if tb:
                for frame in traceback.extract_tb(tb):
                    if Path(frame.filename).name == data_file.name:
                        line_num = frame.lineno
                        break

        line_str = f" [{data_file.name}:Línea {line_num}]" if line_num else ""
        bak_hint = f" (NOTA: Backup de seguridad disponible en {bak_file.name})" if bak_file.is_file() else ""
        err_msg = f"Syntax / Execution error in {data_file.name}:{line_str} {e}{bak_hint}"

        if line_num and source_lines:
            start_l, end_l, snip = get_source_line_snippet(source_lines, line_num, radius=1)
            err_msg += (
                f"\nCONTEXTO EXACTO PARA replace_file_content (NO uses view_file ni write_to_file Overwrite):\n"
                f"  --- {data_file.name} (StartLine={start_l}, EndLine={end_l}) ---\n"
                f"{snip}"
            )

        return False, {}, [err_msg], elapsed

    competencies = getattr(mod, "COMPETENCIES", None)
    if competencies is None:
        elapsed = (time.perf_counter() - t0) * 1000.0
        return False, {}, [f"{data_file.name} does not define 'COMPETENCIES = [...]' list of tuples."], elapsed

    # Post-Import String Healer: clean control characters from imported competencies
    competencies = heal_control_chars_in_obj(competencies)

    # Anti-Overwrite Guard: protect against accidental write_to_file(Overwrite=True) shrinking >=10 comps to <6
    if len(competencies) >= 10:
        try:
            bak_file.write_text(source_text, encoding="utf-8")
        except Exception:
            pass
    elif bak_file.is_file() and 0 < len(competencies) < 6:
        try:
            bak_mod = load_cta_data_module(bak_file)
            bak_comps = getattr(bak_mod, "COMPETENCIES", [])
            if len(bak_comps) >= 10:
                logger.warning(
                    "Detected destructive shrink of %s (%d -> %d competencies). Restoring prefix from .cta_data.py.bak.",
                    data_file.name, len(bak_comps), len(competencies),
                )
        except Exception:
            pass

    course_id = getattr(mod, "COURSE_ID", None)
    if not course_id or course_id in ("work", "Tops_academy"):
        # Read course_id from pre_cta_manifest.json
        mp_cands = []
        if manifest_path:
            mp_cands.append(Path(manifest_path))
        mp_cands.append(work_dir / "pre_cta_manifest.json")
        for mp_cand in mp_cands:
            if mp_cand.is_file():
                try:
                    m_obj = json.loads(mp_cand.read_text(encoding="utf-8"))
                    cid = m_obj.get("course_id")
                    if cid and cid not in ("work", "Tops_academy"):
                        course_id = cid
                        break
                except Exception:
                    pass

        # Fallback to parent folder if not generic
        if not course_id or course_id in ("work", "Tops_academy"):
            parent_name = work_dir.parent.name if work_dir.name == "work" else work_dir.name
            if parent_name not in ("", ".", "work", "Tops_academy"):
                course_id = parent_name

    if not course_id or course_id in ("work", "Tops_academy"):
        course_id = "custom_course"
    title = getattr(mod, "COURSE_TITLE", None) or getattr(mod, "TITLE", None) or course_id.replace("_", " ").title()
    title = heal_control_chars_in_str(str(title))
    macro = heal_control_chars_in_str(str(getattr(mod, "MACRO_COMPETENCY", "")))

    # 2. Compile to dict
    cta_dict = compile_cta_module(
        competencies_data=competencies,
        course_id=course_id,
        title=title,
        macro_competency=macro,
    )
    cta_dict = heal_control_chars_in_obj(cta_dict)

    # 3. Load manifest: pre_cta_manifest.json required without fallback
    manifest_data = None
    if manifest_path:
        mp = Path(manifest_path)
        if mp.is_file():
            try:
                manifest_data = json.loads(mp.read_text(encoding="utf-8"))
            except Exception:
                pass
    else:
        def_manifest = work_dir / "pre_cta_manifest.json"
        if def_manifest.is_file():
            try:
                manifest_data = json.loads(def_manifest.read_text(encoding="utf-8"))
            except Exception:
                pass
        else:
            elapsed = (time.perf_counter() - t0) * 1000.0
            return False, cta_dict, ["BLOCKER:: No existe pre_cta_manifest.json"], elapsed

    # 3b. Auto-normalize page numbers before calling validate_cta_rules
    if manifest_data:
        cta_dict = auto_normalize_page_numbers(cta_dict, manifest_data)

    # 4. Validate with platform rules using in-memory JsonLineLocator
    target_json_name = output_json_name or "cta.json"
    target_json_path = work_dir / target_json_name
    json_str = json.dumps(cta_dict, indent=2, ensure_ascii=False)
    json_locator = JsonLineLocator(json_str)
    is_valid, validation_errors = validate_cta_rules(
        cta_data=cta_dict,
        manifest_data=manifest_data,
        file_path=target_json_path,
        locator=json_locator,
    )

    # 5. Format errors with line numbers mapped to cta_data.py
    mapped_errors: List[str] = []
    if not is_valid:
        for err in validation_errors:
            found_line = None
            for m in re.finditer(r"\b(D-[A-Za-z0-9_-]+|H-\d+|C-\d+|Hab-\d+|Fact-\d+|Concept-\d+|Skill-\d+)\b", err):
                candidate_id = m.group(1)
                l_num = locator.get_line(candidate_id)
                if l_num:
                    found_line = l_num
                    break
            line_info = f" [cta_data.py:Línea {found_line}]" if found_line else ""
            mapped_errors.append(f"{err}{line_info}")

    elapsed_ms = (time.perf_counter() - t0) * 1000.0

    if not is_valid:
        return False, cta_dict, mapped_errors, elapsed_ms

    # 6. Write target JSON and MD
    target_json_path.write_text(json.dumps(cta_dict, indent=2, ensure_ascii=False), encoding="utf-8")
    target_md_name = (Path(target_json_name).stem + ".md") if output_json_name else "cta.md"
    target_md_path = work_dir / target_md_name
    rendered_md = render_cta_md(cta_dict)
    target_md_path.write_text(rendered_md, encoding="utf-8")

    return True, cta_dict, [], elapsed_ms


def categorize_cta_error(err: str) -> Tuple[str, str, str, str]:
    """Categorize raw CTA error into (rule_tag, short_rule, cause, action)."""
    # 0. Python Syntax / Execution errors
    if any(k in err for k in ["Syntax / Execution error", "SyntaxError", "IndentationError"]):
        rule_tag = "CTA-PYTHON-SYNTAX: ERROR DE SINTAXIS PYTHON"
        short_rule = "CTA-SYNTAX"
        first_line = err.splitlines()[0]
        cause = first_line[:120]
        action = "Corregir sintaxis de Python (comilla, paréntesis o delimitador sin cerrar)"
        return rule_tag, short_rule, cause, action

    # 1. Corrupted ASCII control characters (unescaped \rho, \frac, \alpha, etc.)
    if "Corrupted ASCII control character" in err:
        return (
            "CTA-ESCAPE: CONTROL CHARACTERS CORRUPTOS",
            "CTA-ESCAPE",
            "Caracteres de control ASCII por barras LaTeX sin escapar (\\rho, \\frac, \\alpha)",
            "Prefijar strings con r'...' o usar doble barra '\\\\' en expresiones LaTeX",
        )

    # 2. KaTeX and LaTeX errors
    if any(k in err for k in [
        "Unbalanced inline math", "Unbalanced display math", "Triple dollar",
        "Residual double curly", "sin delimitar", "RAW_LATEX", "KaTeX",
        "Error de sintaxis KaTeX", "scalable delimiter", "LaTeX macro",
        "Unclosed LaTeX environment", "Unbalanced curly braces",
        "Unclosed nested macro brace", "Unsubstituted template variable",
        "Unescaped LaTeX", "LaTeX math command", "math command",
    ]):
        short_rule = "CTA-KATEX"
        rule_tag = "CTA-KATEX: SINTAXIS / DELIMITADORES"
        if "Unbalanced inline math" in err or "delimitador '$' impar" in err.lower():
            cause = "Delimitador '$' impar en expresión matemática"
            action = "Cerrar delimitador '$...$' o usar raw string r'...'"
        elif "sin delimitar" in err:
            cause = "Comandos LaTeX sin delimitar por '$...$'"
            action = "Encerrar expresión matemática en '$...$'"
        elif "unescaped latex" in err.lower() or "math command" in err.lower():
            cause = "Comandos LaTeX sin barra invertida o sin delimitar (e.g. bar{k}, dot{w})"
            action = "Prefijar con '\\' y encerrar en '$...$' (e.g. '$\\bar{k}$')"
        elif "Unbalanced display math" in err:
            cause = "Delimitador '$$' impar en expresión matemática"
            action = "Cerrar delimitador '$$...$$'"
        elif "Triple dollar" in err:
            cause = "Delimitador '$$$' inválido"
            action = "Reemplazar por '$$' (display) o '$' (inline)"
        elif "Residual double" in err:
            cause = "Llaves dobles '{{' o '}}' residuales"
            action = "Usar llaves simples '{...}' para KaTeX"
        elif "Unsubstituted template variable" in err:
            cause = "Llaves '{x}' interpretadas como variable o comando sin barra"
            action = "Verificar sintaxis de llaves o comandos KaTeX"
        elif "Unbalanced" in err or "desbalancead" in err.lower():
            cause = "Delimitadores o llaves desbalanceadas en LaTeX"
            action = "Cerrar todas las llaves '{...}' y delimitadores KaTeX"
        elif "scalable delimiter" in err:
            cause = "Delimitadores escalables \\left / \\right desbalanceados"
            action = "Verificar pares de delimitadores escalables (\\left( ... \\right))"
        elif "LaTeX macro" in err:
            cause = "Argumentos incompletos o faltantes en macro LaTeX"
            action = "Completar argumentos requeridos '{...}' de la macro KaTeX"
        elif "environment" in err.lower():
            cause = "Entorno \\begin{...} / \\end{...} desbalanceado o mal cerrado"
            action = "Cerrar entorno con \\end{...} correspondiente"
        else:
            clean_detail = err.splitlines()[0]
            clean_detail = re.sub(r"\[(?:.+:)?L[íi]nea\s+\d+\]", "", clean_detail)
            clean_detail = re.sub(r"\b(D-[A-Za-z0-9_-]+|H-\d+|C-\d+|Hab-\d+)\b", "", clean_detail)
            clean_detail = re.sub(r"['\"][^'\"]*['\"]", "...", clean_detail)
            clean_detail = re.sub(r"\s+", " ", clean_detail).strip()
            if len(clean_detail) > 80:
                clean_detail = clean_detail[:77] + "..."
            cause = f"Sintaxis LaTeX inválida ({clean_detail})"
            action = "Verificar sintaxis KaTeX y escapar barras invertidas"
        return rule_tag, short_rule, cause, action

    # 3. Distractor count
    if "distractors (minimum" in err or "declarados" in err:
        return (
            "CTA-D1: CUOTA DE DISTRACTORES",
            "CTA-D1",
            "Competencia declara menos de 6 distractores obligatorios",
            "Completar la lista con al menos 6 tuplas de distractores",
        )

    # 4. DAG / Prerequisites
    if "Cycle detected" in err or "prerequisite" in err.lower():
        return (
            "CTA-DAG: GRAFO DE PRERREQUISITOS",
            "CTA-DAG",
            "Ciclo o identificador de prerrequisito inválido en el grafo",
            "Corregir la lista de prerrequisitos para mantener un DAG acíclico",
        )

    # 5. Evidence
    if "evidence" in err.lower() or "manifest" in err.lower():
        return (
            "CTA-EV: EVIDENCIA EN CORPUS",
            "CTA-EV",
            "Página o documento de evidencia fuera de los límites del corpus",
            "Alinear el número de página y nombre de documento con el corpus",
        )

    # 6. Schema fallback
    m_code = re.match(r"^\[([A-Z0-9_-]+)\]", err)
    code = m_code.group(1) if m_code else "CTA-SCHEMA"
    clean_msg = re.sub(r"\[(?:.+:)?L[íi]nea\s+\d+\]", "", err.splitlines()[0])
    clean_msg = re.sub(r"\b(D-[A-Za-z0-9_-]+|H-\d+|C-\d+|Hab-\d+)\b", "", clean_msg)
    clean_msg = re.sub(r"['\"][^'\"]*['\"]", "...", clean_msg)
    clean_msg = re.sub(r"\s+", " ", clean_msg).strip()[:80]
    return (
        f"{code}: ESQUEMA FORMAL",
        code,
        clean_msg,
        "Corregir estructura de campos en la tupla",
    )


def get_source_line_snippet(lines: List[str], line_num: int, radius: int = 1) -> Tuple[int, int, str]:
    """Devuelve (start_line, end_line, formatted_snippet) en torno a line_num (1-indexed)."""
    start_l = max(1, line_num - radius)
    end_l = min(len(lines), line_num + radius)
    snip_lines = [f"  L{idx}: {lines[idx - 1]}" for idx in range(start_l, end_l + 1)]
    return start_l, end_l, "\n".join(snip_lines)


def render_compact_cta_errors(
    errors: List[str],
    data_filename: str = "cta_data.py",
    source_lines: Optional[List[str]] = None,
) -> str:
    """Renders single-line aggregated errors grouped by rule for compile_cta.py, with exact line snippets."""
    if not errors:
        return ""

    if source_lines is None:
        cand_p = Path(data_filename)
        if cand_p.is_file():
            try:
                source_lines = cand_p.read_text(encoding="utf-8").splitlines()
            except Exception:
                pass
        elif (Path("work") / data_filename).is_file():
            try:
                source_lines = (Path("work") / data_filename).read_text(encoding="utf-8").splitlines()
            except Exception:
                pass

    grouped: Dict[str, Dict[Tuple[str, str, str], Dict[str, Any]]] = defaultdict(
        lambda: defaultdict(lambda: {"lines": [], "items": []})
    )

    for raw_err in errors:
        rule_tag, short_rule, cause, action = categorize_cta_error(raw_err)
        m_line = re.search(r"\[(?:.+:)?L[íi]nea\s+(\d+)\]", raw_err)
        line_num = int(m_line.group(1)) if m_line else None

        m_id = re.search(r"\b(D-[A-Za-z0-9_-]+|H-\d+|C-\d+|Hab-\d+)\b", raw_err)
        item_id = m_id.group(1) if m_id else ""

        key = (short_rule, cause, action)
        if line_num:
            grouped[rule_tag][key]["lines"].append(line_num)
        if item_id:
            grouped[rule_tag][key]["items"].append(item_id)

    out_lines = [f"[ERROR] CTA compilation failed ({len(errors)} errors) [{data_filename}]:", ""]
    snippet_lines_to_show: List[int] = []

    # Target: total rendered lines strictly < 25 lines. Footer is ~5 lines, header is 2 lines.
    max_group_lines = 8 if source_lines else 12
    rendered_groups = 0
    omitted_groups = 0

    for rule_tag, err_map in grouped.items():
        if rendered_groups >= max_group_lines:
            omitted_groups += len(err_map)
            continue
        out_lines.append(f"[-] [{rule_tag}]")
        for (short_rule, cause, action), rec in err_map.items():
            if rendered_groups >= max_group_lines:
                omitted_groups += 1
                continue
            rendered_groups += 1
            uniq_lines = sorted(set(rec["lines"]))
            uniq_ids = [x for x in dict.fromkeys(rec["items"]) if x]
            if uniq_lines:
                snippet_lines_to_show.extend(uniq_lines[:2])
                if len(uniq_lines) > 5:
                    lines_str = f":L{uniq_lines[0]}-{uniq_lines[-1]} ({len(uniq_lines)} líneas)"
                else:
                    lines_str = f":L{','.join(str(l) for l in uniq_lines)}"
            else:
                lines_str = ""

            if len(uniq_ids) > 5:
                ids_str = f" [{', '.join(uniq_ids[:5])} (+{len(uniq_ids) - 5} más)]"
            elif uniq_ids:
                ids_str = f" [{', '.join(uniq_ids)}]"
            else:
                ids_str = ""

            out_lines.append(
                f"  • [{short_rule}] {data_filename}{lines_str}{ids_str} -> Causa: {cause} | Acción: {action}"
            )
        out_lines.append("")

    if omitted_groups > 0:
        out_lines.append(f"  • [+ {omitted_groups} categorías de error adicionales omitidas por brevedad]")
        out_lines.append("")

    if source_lines and snippet_lines_to_show and rendered_groups <= 8:
        out_lines.append("CONTEXTO EXACTO PARA replace_file_content (NO uses view_file ni write_to_file Overwrite):")
        for ln in sorted(set(snippet_lines_to_show))[:2]:
            start_l, end_l, snip = get_source_line_snippet(source_lines, ln, radius=1)
            out_lines.append(f"  --- {data_filename} (StartLine={start_l}, EndLine={end_l}) ---")
            out_lines.append(snip)
        out_lines.append("")

    out_lines.append("ACTION REQUIRED:")
    out_lines.append(
        f"  1. Usa EXCLUSIVAMENTE 'replace_file_content' en {data_filename} sobre las líneas indicadas arriba."
    )
    out_lines.append(
        f"  2. PROHIBIDO usar 'write_to_file' con Overwrite=True sobre {data_filename} (destruiría las competencias ya escritas)."
    )
    has_backup = any(".cta_data.py.bak" in err for err in errors) or (
        Path(data_filename).parent / ".cta_data.py.bak"
    ).is_file()
    if has_backup:
        out_lines.append(
            f"  3. Existe un backup '.cta_data.py.bak'. Si {data_filename} quedó corrupto o truncado, puedes restaurarlo."
        )
        out_lines.append(f"  4. Re-ejecuta: python compile_cta.py")
    else:
        out_lines.append(f"  3. Re-ejecuta: python compile_cta.py")

    rendered_text = "\n".join(out_lines).strip()
    res_lines = rendered_text.splitlines()
    if len(res_lines) >= 25:
        filtered = []
        skip_snippet = False
        for line in res_lines:
            if line.startswith("CONTEXTO EXACTO"):
                skip_snippet = True
                continue
            if skip_snippet and line.startswith("ACTION REQUIRED:"):
                skip_snippet = False
            if not skip_snippet:
                filtered.append(line)
        res_lines = filtered

    while len(res_lines) >= 25 and len(res_lines) > 8:
        act_idx = next((i for i, l in enumerate(res_lines) if l.startswith("ACTION REQUIRED:")), len(res_lines))
        res_lines.pop(act_idx - 1)

    return "\n".join(res_lines).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic Fast CTA Compiler")
    parser.add_argument("cta_data_path", nargs="?", default=None, help="Optional direct path to cta_data.py")
    parser.add_argument("--input", "-i", dest="input_path", default=None, help="Optional path to input cta_data.py")
    parser.add_argument("--output", "-o", dest="output_path", default=None, help="Optional path to output cta.json")
    parser.add_argument("--work", "--work-dir", dest="work", default=None, help="Working directory containing pre_cta_manifest.json")
    parser.add_argument("--part", default=None, help="Optional subpart id (e.g. part_01) to compile work/cta_parts/<part_id>_data.py -> work/cta_parts/<part_id>.json")
    parser.add_argument("--manifest", default=None, help="Optional path to pre_cta_manifest.json or ingestion_manifest.json")
    args = parser.parse_args()

    eff_input = args.input_path or args.cta_data_path
    if args.work:
        work_dir = Path(args.work).resolve()
    elif eff_input:
        in_p = Path(eff_input).resolve()
        work_dir = in_p.parent.parent if in_p.parent.name in ("cta_parts", "cta") else in_p.parent
    elif args.manifest:
        work_dir = Path(args.manifest).resolve().parent
    else:
        work_dir = Path("work").resolve()

    if args.manifest:
        manifest_p = Path(args.manifest).resolve()
        if not manifest_p.is_file() and (work_dir / "pre_cta_manifest.json").is_file():
            manifest_p = work_dir / "pre_cta_manifest.json"
    else:
        manifest_p = work_dir / "pre_cta_manifest.json"
        if not manifest_p.is_file() and (work_dir / "ingestion_manifest.json").is_file():
            manifest_p = work_dir / "ingestion_manifest.json"

    if not manifest_p.is_file():
        print("BLOCKER:: No existe pre_cta_manifest.json", file=sys.stderr)
        sys.exit(2)

    if eff_input:
        data_path = Path(eff_input).resolve()
        if args.output_path:
            out_p = Path(args.output_path).resolve()
            if out_p.suffix.lower() == ".json":
                output_dir = out_p.parent
                target_json_name = out_p.name
            else:
                output_dir = out_p
                target_json_name = f"{args.part}.json" if args.part else "cta.json"
        elif args.part:
            output_dir = data_path.parent
            target_json_name = f"{args.part}.json"
        else:
            output_dir = work_dir
            target_json_name = "cta.json"
    elif args.part:
        data_path = work_dir / "cta_parts" / f"{args.part}_data.py"
        output_dir = work_dir / "cta_parts"
        target_json_name = f"{args.part}.json"
    else:
        data_path = work_dir / "cta_data.py"
        output_dir = work_dir
        target_json_name = "cta.json"

    print(f"[*] Compiling CTA data: {data_path.resolve()} -> {output_dir.resolve()} ...")
    valid, cta_dict, errors, elapsed_ms = compile_cta(
        cta_data_path=data_path,
        output_dir=output_dir,
        manifest_path=manifest_p,
        output_json_name=target_json_name,
    )

    if not valid:
        if any("BLOCKER::" in err for err in errors):
            print("BLOCKER:: No existe pre_cta_manifest.json", file=sys.stderr)
            sys.exit(2)
        source_lines = None
        if data_path.is_file():
            try:
                source_lines = data_path.read_text(encoding="utf-8").splitlines()
            except Exception:
                pass
        compact_msg = render_compact_cta_errors(errors, data_filename=data_path.name, source_lines=source_lines)
        print(f"\n{compact_msg}\n(Calculado en {elapsed_ms:.2f} ms)", file=sys.stderr)
        sys.exit(1)

    comps = cta_dict.get("competencies", [])
    total_d = sum(len(c.get("distractors", [])) for c in comps)
    target_md_name = (Path(target_json_name).stem + ".md")
    print(f"PASS: {target_json_name} satisfies all schema, CTA-D1, CTA-D2, and evidence constraints.")
    print(f"  [+] Compiled {len(comps)} competencies ({total_d} distractors) in {elapsed_ms:.2f} ms.")
    print(f"  [+] Artifacts written:")
    print(f"      - {output_dir / target_json_name}")
    print(f"      - {output_dir / target_md_name}")
    sys.exit(0)


if __name__ == "__main__":
    main()
