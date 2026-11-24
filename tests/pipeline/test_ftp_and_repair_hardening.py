"""Tests for FTP / repair-loop hardening: MS const-distractor, STATIC-OPT classification,
canvas bounds, witness leak, Phase-B skip, auditor cleanup."""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKILL = REPO / ".agents" / "skills" / "content-to-course"
AUD = REPO / ".agents" / "skills" / "c2c-run-auditor" / "scripts"
for p in (str(SKILL), str(AUD), str(REPO / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from engine.invariants import check_instance_invariants  # noqa: E402
from engine.shard_compiler_steps import _is_conceptual_statement  # noqa: E402
from check_templates import check_single_template  # noqa: E402
import audit_engine  # noqa: E402


def test_conceptual_statement_with_latex_is_exempt():
    assert _is_conceptual_statement(r"Si $\frac{df}{dx}>0$ la función crece siempre en el dominio.")
    assert not _is_conceptual_statement("0")
    assert not _is_conceptual_statement("$5$")


def _adv(stem):
    return {
        "stem": stem,
        "hints": ["a" * 30, "b" * 30, "c" * 30],
        "adversarial_break": {
            "mode": "counterexample",
            "inputs": [{"id": "L", "label": "L"}, {"id": "K", "label": "K"}],
            "predicates": [{"expr": "L>=1", "failure_rationale": "Falla."}],
            "sample_witness": {"L": 9, "K": 54},
        },
    }


def test_adv_witness_leak():
    _, errs = check_instance_invariants(_adv("Refute con L = 9 y K = 54 el enunciado."), "adversarial_break")
    assert any("ADV-WITNESS-LEAK" in e for e in errs)
    _, errs = check_instance_invariants(_adv("Refute el enunciado con L >= 1."), "adversarial_break")
    assert not any("ADV-WITNESS-LEAK" in e for e in errs)


def _static_tpl(cid, n_vals):
    return {
        "id": "T-X-01",
        "competency_id": cid,
        "interaction_type": "fill_in_the_blank",
        "difficulty": "easy",
        "bloom": "Apply",
        "stem": "Calcule el valor para {k}:",
        "generate_py": (
            "def generate(rng):\n"
            f"    k = rng.randint(1, {n_vals})\n"
            "    return {'vars': {'k': k}, 'correct': str(k*7), 'value': str(k*7), 'distractors': []}\n"
        ),
        "cross_check_py": "def verify(res):\n    return True",
        "hints": ["Identifique el parámetro k en el enunciado.", "Aplique la definición formal al valor.", "Verifique la magnitud del resultado."],
        "solution": "La solución se obtiene multiplicando k por siete, entonces resulta k*7 exacto.",
        "distractor_ids": [],
    }


def test_static_opt_fact_vs_skill_threshold():
    fact = check_single_template(_static_tpl("H-01", 6), "H-01", set(), num_dry_run_seeds=20, strict=True)
    assert not any("TPL-STATIC-OPT" in e for e in fact)
    skill = check_single_template(_static_tpl("Hab-01", 6), "Hab-01", set(), num_dry_run_seeds=20, strict=True)
    assert any("TPL-STATIC-OPT" in e for e in skill)


def test_first_compile_rules_unpack_general_and_skip_precheck():
    content = (
        "Command exited with code 1.\n"
        "   - L2 [TPL-DYNAMIC-RATIONALE] rationale corta\n"
        "   • [GENERAL] a.json -> Causa: [TPL-CONST-DISTRACTOR] En 'T-1'\n"
        "   • [GENERAL] b.json -> Causa: FAIL: texto sin tag\n"
        "   [-] [R-19: X]\n"
    )
    rules = audit_engine._extract_first_compile_blocking_rules(content)
    assert "TPL-CONST-DISTRACTOR" in rules
    assert "TPL-DYNAMIC-RATIONALE" not in rules
    assert rules.count("GENERAL") == 1


def test_zero_valid_out_tracks_broken_template_without_truncating_phase_a():
    broken = _static_tpl("H-01", 6)
    broken["stem"] = "Calcule {k} y @missing_token@:"
    z_out: list[str] = []
    errs = check_single_template(
        broken, "H-01", set(), num_dry_run_seeds=15, strict=True, zero_valid_out=z_out
    )
    assert "T-X-01" in z_out
    assert any("missing_token" in e for e in errs)


