"""Lightweight, process-isolated Stage 4 worker for fast Windows spawn execution."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_SKILL_DIR = str(Path(__file__).resolve().parents[1])
if _SKILL_DIR not in sys.path:
    sys.path.insert(0, _SKILL_DIR)

from engine.diversity import evaluate_competency_diversity
from engine.instantiate import instantiate_competency

_STAGE4_DISTRACTOR_MAP: Optional[Dict[str, Dict[str, Any]]] = None


def init_stage4_worker(distractor_map: Dict[str, Dict[str, Any]]) -> None:
    """Initializes per-process distractor lookup once per ProcessPoolExecutor worker."""
    global _STAGE4_DISTRACTOR_MAP
    _STAGE4_DISTRACTOR_MAP = distractor_map


def build_course_comp_dict(comp: Dict[str, Any]) -> Dict[str, Any]:
    """Constructs the published competency metadata dict from a CTA entry."""
    cid = comp["id"]
    cat = comp.get("type", "concept").title()
    name = comp.get("name", cid)
    desc = comp.get("description_latex") or comp.get("description", "")
    course_comp_dict: Dict[str, Any] = {
        "id": cid,
        "code": cid.upper(),
        "name": name,
        "category": cat,
        "description": desc,
        "mastery_target": 100,
        "prerequisites": comp.get("prerequisites", []),
    }
    if cid.upper().startswith("PRE-") or comp.get("is_prerequisite"):
        course_comp_dict["is_prerequisite"] = True
    for opt_key in ("session", "unit_index", "evidence", "assumptions", "source_examples"):
        opt_val = comp.get(opt_key)
        if opt_val is not None and opt_val != "" and opt_val != []:
            course_comp_dict[opt_key] = opt_val
    return course_comp_dict


def instantiate_single_comp_worker(
    payload: Tuple[Dict[str, Any], List[Dict[str, Any]], Optional[Dict[str, Dict[str, Any]]], int]
) -> Tuple[str, Dict[str, Any], List[Dict[str, Any]], Dict[str, Any]]:
    """Process-isolated Stage 4 worker so QuickJS runs safely across bounded CPU cores."""
    comp, comp_templates, inline_distractor_map, seed_offset = payload
    cid = comp["id"]
    effective_dmap = (
        _STAGE4_DISTRACTOR_MAP
        if _STAGE4_DISTRACTOR_MAP is not None
        else (inline_distractor_map or {})
    )
    course_comp_dict = build_course_comp_dict(comp)
    comp_res = instantiate_competency(
        competency=comp,
        templates=comp_templates,
        cta_distractors_map=effective_dmap,
        seed_offset_base=seed_offset,
    )
    comp_questions = (
        comp_res["questions"]
        if isinstance(comp_res, dict) and "questions" in comp_res
        else comp_res
    )
    stems = [q["stem"] for q in comp_questions]
    div_res = evaluate_competency_diversity(stems)
    return cid, course_comp_dict, comp_questions, div_res
