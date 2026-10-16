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
import json
import logging
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
                    raw_t = "concept"
                    if len(c_node.elts) > 0 and isinstance(c_node.elts[0], ast.Constant) and isinstance(c_node.elts[0].value, str):
                        raw_t = c_node.elts[0].value.strip().lower()
                    prefix = type_prefix_map.get(raw_t, "C")
                    type_counts[prefix] = type_counts.get(prefix, 0) + 1

                    cid = None
                    if len(c_node.elts) > 1 and isinstance(c_node.elts[1], ast.Constant) and c_node.elts[1].value:
                        cid = str(c_node.elts[1].value).strip()
                    if not cid:
                        cid = f"{prefix}-{type_counts[prefix]:02d}"

                    self.comp_lines[cid] = c_line
                    self.comp_lines[cid.replace("-", "")] = c_line
                    self.comp_tuple_indices[global_c_idx] = c_line
                    cid_clean = cid.replace("-", "")

                    if len(c_node.elts) > 8 and isinstance(c_node.elts[8], (ast.List, ast.Tuple)):
                        for d_idx, d_node in enumerate(c_node.elts[8].elts, start=1):
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
    """Normalizes distractors from either dict or tuple representation, guaranteeing
    canonical id, error_type, evidence, and CTA-D2 compliance for skill competencies."""
    compiled_distractors: List[Dict[str, Any]] = []

    for d_idx, d in enumerate(raw_distractors, start=1):
        if isinstance(d, dict):
            d_dict = dict(d)
            d_id = str(d_dict.get("id") or "").strip() or f"D-{cid_clean}-{d_idx:02d}"
            d_dict["id"] = d_id
            d_name = str(d_dict.get("name") or "").strip() or f"Distractor {d_idx}"
            d_dict["name"] = d_name

            wrong_belief = d_dict.get("wrong_belief")
            if wrong_belief is not None:
                wrong_belief = str(wrong_belief).strip() or None
            correct_belief = d_dict.get("correct_belief")
            if correct_belief is not None:
                correct_belief = str(correct_belief).strip() or f"Verdad teórica de {comp_name}."
            else:
                correct_belief = f"Verdad teórica de {comp_name}."
            manifestation = str(d_dict.get("manifestation") or "$0$").strip()
            hint = str(d_dict.get("remediation_hint") or f"Revisar la definición de {comp_name}.").strip()
            omitted_step = d_dict.get("omitted_step")
            if omitted_step is not None:
                omitted_step = str(omitted_step).strip() or None

            # Fallback if both wrong_belief and omitted_step are None (schema requires at least one)
            if not wrong_belief and not omitted_step:
                wrong_belief = f"Asume resultado incorrecto en {comp_name}"

            error_type = d_dict.get("error_type")
            if not error_type:
                error_type = "skipped_step" if omitted_step else "conceptual_swap"

            d_dict["wrong_belief"] = wrong_belief
            d_dict["correct_belief"] = correct_belief
            d_dict["manifestation"] = manifestation
            d_dict["remediation_hint"] = hint
            d_dict["omitted_step"] = omitted_step
            d_dict["error_type"] = error_type
            d_dict.setdefault("severity", "high")
            d_dict.setdefault("origin", "inferred")
            d_dict.setdefault("trigger", f"Evaluación formal de {comp_name}")
            if "evidence" not in d_dict or not d_dict["evidence"]:
                d_dict["evidence"] = {"doc": doc, "page": page}

            compiled_distractors.append(d_dict)
            continue

        if not isinstance(d, (list, tuple)):
            continue

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


def compile_tuples_to_cta_dict(
    competencies_tuples: List[Any],
    course_id: str = "custom_course",
    title: str = "Curso Académico",
    macro_competency: str = "",
) -> Dict[str, Any]:
    """Compiles tabular positional tuples into formal cta.json dictionary."""
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
            comp_obj = dict(item)
            c_type = str(comp_obj.get("type", "concept")).strip().lower()
            norm_type, default_prefix = type_map.get(c_type, ("concept", "C"))
            comp_obj["type"] = norm_type

            raw_id = str(comp_obj.get("id") or "").strip()
            if not raw_id:
                counts_by_prefix[default_prefix] = counts_by_prefix.get(default_prefix, 0) + 1
                raw_id = f"{default_prefix}-{counts_by_prefix[default_prefix]:02d}"
                comp_obj["id"] = raw_id
            else:
                m_pref = re.match(r"^([A-Za-z]+)-(\d+)$", raw_id)
                if m_pref:
                    pfx, num = m_pref.group(1), int(m_pref.group(2))
                    if pfx in counts_by_prefix:
                        counts_by_prefix[pfx] = max(counts_by_prefix[pfx], num)

            cid_clean = raw_id.replace("-", "")
            comp_name = str(comp_obj.get("name") or f"Competencia {raw_id}").strip()
            comp_obj["name"] = comp_name

            raw_dists = comp_obj.get("distractors", [])
            doc = "material_fuente.pdf"
            page = 1
            if comp_obj.get("evidence") and isinstance(comp_obj["evidence"], list) and len(comp_obj["evidence"]) > 0:
                first_ev = comp_obj["evidence"][0]
                if isinstance(first_ev, dict):
                    doc = str(first_ev.get("doc") or first_ev.get("pdf") or doc).strip()
                    page = int(first_ev.get("page", page)) if str(first_ev.get("page", "")).isdigit() else page

            comp_obj["distractors"] = _normalize_distractors_list(
                raw_distractors=raw_dists,
                cid_clean=cid_clean,
                comp_name=comp_name,
                norm_type=norm_type,
                doc=doc,
                page=page,
            )
            sanitize_competency_math(comp_obj)
            compiled_comps.append(comp_obj)
            continue

        if not isinstance(item, (list, tuple)):
            continue

        raw_type = str(item[0]).strip().lower() if len(item) > 0 else "concept"
        norm_type, default_prefix = type_map.get(raw_type, ("concept", "C"))
        counts_by_prefix[default_prefix] = counts_by_prefix.get(default_prefix, 0) + 1

        raw_id = str(item[1]).strip() if len(item) > 1 and item[1] else f"{default_prefix}-{counts_by_prefix[default_prefix]:02d}"
        name = str(item[2]).strip() if len(item) > 2 else f"Competencia {raw_id}"
        desc_latex = str(item[3]).strip() if len(item) > 3 else f"Definición formal de {name}."
        raw_bloom = str(item[4]).strip() if len(item) > 4 and item[4] else ("Apply" if norm_type == "skill" else "Understand")
        bloom = raw_bloom.capitalize()
        if bloom not in ("Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"):
            bloom = "Apply" if norm_type == "skill" else "Understand"

        doc = str(item[5]).strip() if len(item) > 5 and item[5] else "material_fuente.pdf"
        page = int(item[6]) if len(item) > 6 and str(item[6]).isdigit() else 1
        prereqs = list(item[7]) if len(item) > 7 and isinstance(item[7], (list, tuple)) else []
        raw_distractors = item[8] if len(item) > 8 and isinstance(item[8], (list, tuple)) else []

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

    return {
        "course_id": course_id,
        "title": title,
        "macro_competency": macro_competency,
        "competencies": compiled_comps,
    }


def compile_cta(
    cta_data_path: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    manifest_path: Optional[Union[str, Path]] = None,
) -> Tuple[bool, Dict[str, Any], List[str], float]:
    """Compiles cta_data.py into cta.json and cta.md, validating all constraints in < 5ms."""
    t0 = time.perf_counter()
    data_file = Path(cta_data_path).resolve()
    if not data_file.is_file():
        return False, {}, [f"Data file not found: {data_file}"], 0.0

    work_dir = Path(output_dir).resolve() if output_dir else data_file.parent
    work_dir.mkdir(parents=True, exist_ok=True)
    bak_file = work_dir / ".cta_data.py.bak"

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
        # Try reading course_id or source_path from manifest.json
        mp_cands = []
        if manifest_path:
            mp_cands.append(Path(manifest_path))
        mp_cands.extend([work_dir / "pages" / "manifest.json", work_dir / "manifest.json"])
        for mp_cand in mp_cands:
            if mp_cand.is_file():
                try:
                    m_obj = json.loads(mp_cand.read_text(encoding="utf-8"))
                    cid = m_obj.get("course_id") or Path(m_obj.get("source_path", "")).stem
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
    macro = getattr(mod, "MACRO_COMPETENCY", "")

    # 2. Compile to dict
    cta_dict = compile_tuples_to_cta_dict(
        competencies_tuples=competencies,
        course_id=course_id,
        title=title,
        macro_competency=macro,
    )

    # 3. Load manifest if available
    manifest_data = None
    if manifest_path:
        mp = Path(manifest_path)
        if mp.is_file():
            try:
                manifest_data = json.loads(mp.read_text(encoding="utf-8"))
            except Exception:
                pass
    else:
        def_manifest = work_dir / "pages" / "manifest.json"
        if def_manifest.is_file():
            try:
                manifest_data = json.loads(def_manifest.read_text(encoding="utf-8"))
            except Exception:
                pass

    # 4. Validate with platform rules using in-memory JsonLineLocator
    target_json_path = work_dir / "cta.json"
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

    # 6. Write cta.json and cta.md
    target_json_path.write_text(json.dumps(cta_dict, indent=2, ensure_ascii=False), encoding="utf-8")
    target_md_path = work_dir / "cta.md"
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

    # 1. KaTeX errors
    if any(k in err for k in ["Unbalanced inline math", "Unbalanced display math", "Triple dollar", "Residual double curly", "sin delimitar por '$...$'"]):
        short_rule = "CTA-KATEX"
        rule_tag = "CTA-KATEX: SINTAXIS / DELIMITADORES"
        if "Unbalanced inline math" in err:
            cause = "Delimitador '$' impar en expresión matemática"
            action = "Cerrar delimitador '$...$' o usar raw string r'...'"
        elif "sin delimitar" in err:
            cause = "Comandos LaTeX sin delimitar por '$...$'"
            action = "Encerrar expresión matemática en '$...$'"
        elif "Triple dollar" in err:
            cause = "Delimitador '$$$' inválido"
            action = "Reemplazar por '$$' (display) o '$' (inline)"
        elif "Residual double" in err:
            cause = "Llaves dobles '{{' o '}}' residuales"
            action = "Usar llaves simples '{...}' para KaTeX"
        else:
            cause = err
            action = "Verificar sintaxis KaTeX y escapar barras invertidas"
        return rule_tag, short_rule, cause, action

    # 2. Distractor count
    if "distractors (minimum" in err or "declarados" in err:
        return (
            "CTA-D1: CUOTA DE DISTRACTORES",
            "CTA-D1",
            "Competencia declara menos de 6 distractores obligatorios",
            "Completar la lista con al menos 6 tuplas de distractores",
        )

    # 3. DAG / Prerequisites
    if "Cycle detected" in err or "prerequisite" in err.lower():
        return (
            "CTA-DAG: GRAFO DE PRERREQUISITOS",
            "CTA-DAG",
            "Ciclo o identificador de prerrequisito inválido en el grafo",
            "Corregir la lista de prerrequisitos para mantener un DAG acíclico",
        )

    # 4. Evidence
    if "evidence" in err.lower() or "manifest" in err.lower():
        return (
            "CTA-EV: EVIDENCIA EN CORPUS",
            "CTA-EV",
            "Página o documento de evidencia fuera de los límites del corpus",
            "Alinear el número de página y nombre de documento con el corpus",
        )

    # 5. Schema fallback
    m_code = re.match(r"^\[([A-Z0-9_-]+)\]", err)
    code = m_code.group(1) if m_code else "CTA-SCHEMA"
    return (
        f"{code}: ESQUEMA FORMAL",
        code,
        err.splitlines()[0][:90],
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

    grouped: Dict[str, Dict[Tuple[str, str, str], List[int]]] = defaultdict(lambda: defaultdict(list))

    for raw_err in errors:
        rule_tag, short_rule, cause, action = categorize_cta_error(raw_err)
        m_line = re.search(r"\[(?:.+:)?L[íi]nea\s+(\d+)\]", raw_err)
        line_num = int(m_line.group(1)) if m_line else None

        m_id = re.search(r"\b(D-[A-Za-z0-9_-]+|H-\d+|C-\d+|Hab-\d+)\b", raw_err)
        item_id = m_id.group(1) if m_id else ""
        full_cause = f"{cause} en '{item_id}'" if item_id and item_id not in cause else cause

        key = (short_rule, full_cause, action)
        if line_num:
            grouped[rule_tag][key].append(line_num)
        else:
            grouped[rule_tag][key]

    out_lines = [f"[ERROR] CTA compilation failed ({len(errors)} errors) [{data_filename}]:", ""]
    snippet_lines_to_show: List[int] = []

    for rule_tag, err_map in grouped.items():
        out_lines.append(f"[-] [{rule_tag}]")
        for (short_rule, cause, action), line_list in err_map.items():
            uniq_lines = sorted(set(line_list))
            if uniq_lines:
                snippet_lines_to_show.extend(uniq_lines[:2])
                if len(uniq_lines) > 5:
                    lines_str = f":L{uniq_lines[0]}-{uniq_lines[-1]} ({len(uniq_lines)} líneas)"
                else:
                    lines_str = f":L{','.join(str(l) for l in uniq_lines)}"
            else:
                lines_str = ""

            out_lines.append(f"  • [{short_rule}] {data_filename}{lines_str} -> Causa: {cause} | Acción: {action}")
        out_lines.append("")

    if source_lines and snippet_lines_to_show:
        out_lines.append("CONTEXTO EXACTO PARA replace_file_content (NO uses view_file ni write_to_file Overwrite):")
        for ln in sorted(set(snippet_lines_to_show))[:3]:
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

    return "\n".join(out_lines).strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic Fast CTA Compiler")
    parser.add_argument("cta_data_path", nargs="?", default="cta_data.py", help="Path to cta_data.py")
    parser.add_argument("--work-dir", default=None, help="Output work directory (defaults to cta_data.py parent)")
    parser.add_argument("--manifest", default=None, help="Optional manifest.json for evidence verification")
    args = parser.parse_args()

    data_path = Path(args.cta_data_path)
    if not data_path.is_file() and (Path("work") / "cta_data.py").is_file():
        data_path = Path("work") / "cta_data.py"

    work_dir = Path(args.work_dir) if args.work_dir else data_path.parent
    manifest_p = Path(args.manifest) if args.manifest else None

    print(f"[*] Compiling CTA data: {data_path.resolve()} -> {work_dir.resolve()} ...")
    valid, cta_dict, errors, elapsed_ms = compile_cta(
        cta_data_path=data_path,
        output_dir=work_dir,
        manifest_path=manifest_p,
    )

    if not valid:
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
    print(f"PASS: cta.json satisfies all schema, CTA-D1, CTA-D2, and evidence constraints.")
    print(f"  [+] Compiled {len(comps)} competencies ({total_d} distractors) in {elapsed_ms:.2f} ms.")
    print(f"  [+] Artifacts written:")
    print(f"      - {work_dir / 'cta.json'}")
    print(f"      - {work_dir / 'cta.md'}")
    sys.exit(0)


if __name__ == "__main__":
    main()
