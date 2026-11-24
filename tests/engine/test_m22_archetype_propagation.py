"""Tests for M22 Phase 0 archetype and assumption_id propagation in assemble_question()."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = REPO_ROOT / ".agents" / "skills" / "content-to-course"
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from engine.assemble import assemble_question


def _base_template(**overrides):
    tpl = {
        "interaction_type": "fill_in_the_blank",
        "stem": "Evalúa $f(x) = {a}x$ en $x = 2$.",
        "hints": ["Sustituye $x = 2$ en la expresión."],
        "detailed_solution": "Sustituyendo $x = 2$, se obtiene $f(2) = {ans}$.",
        "bloom": "Apply",
        "difficulty": "medium",
    }
    tpl.update(overrides)
    return tpl


def _base_gen_result():
    return {
        "vars": {"a": 3, "ans": 6},
        "correct": "6",
    }


@pytest.mark.parametrize(
    "raw_archetype, expected_archetype",
    [
        ("direct", "direct"),
        ("inverse", "inverse"),
        ("perturbation", "perturbation"),
        ("boundary_or_edge_case", "boundary_or_edge_case"),
        ("  DIRECT  ", "direct"),
        ("Boundary_Or_Edge_Case", "boundary_or_edge_case"),
    ],
)
def test_assemble_question_propagates_and_normalizes_archetype(raw_archetype, expected_archetype):
    """assemble_question() preserves and normalizes valid archetype strings."""
    tpl = _base_template(archetype=raw_archetype)
    assembled = assemble_question(tpl, _base_gen_result(), "Hab-01", 1, seed=42)
    assert assembled["archetype"] == expected_archetype


def test_assemble_question_propagates_assumption_id():
    """assemble_question() preserves assumption_id with whitespace stripped (case preserved)."""
    tpl = _base_template(archetype="perturbation", assumption_id="  ASM-Hab01-02  ")
    assembled = assemble_question(tpl, _base_gen_result(), "Hab-01", 1, seed=42)
    assert assembled["archetype"] == "perturbation"
    assert assembled["assumption_id"] == "ASM-Hab01-02"


def test_assemble_question_backward_compatible_when_omitted():
    """assemble_question() omits archetype and assumption_id when not in template."""
    tpl = _base_template()
    assembled = assemble_question(tpl, _base_gen_result(), "Hab-01", 1, seed=42)
    assert "archetype" not in assembled
    assert "assumption_id" not in assembled


@pytest.mark.parametrize("invalid_val", ["", "   ", None, 123, []])
def test_assemble_question_ignores_empty_or_non_string_metadata(invalid_val):
    """Empty, whitespace-only, or non-string archetype/assumption_id are not emitted."""
    tpl = _base_template(archetype=invalid_val, assumption_id=invalid_val)
    assembled = assemble_question(tpl, _base_gen_result(), "Hab-01", 1, seed=42)
    assert "archetype" not in assembled
    assert "assumption_id" not in assembled
