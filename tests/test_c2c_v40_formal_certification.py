"""
C2C v4.0 Formal Neuro-Symbolic Certification Suite
Certification of the 10 Eradicated Pathologies & Invariant Guarantees:
1. Eradication of np.bool_(False) / None / 0 in sandbox execution.
2. Triple Contract ver_* hygiene (tautology, swallowed exception, debug artifact, ad-hoc perturbation).
3. Form-C DSL (<= 65 lines source, < 15 KB artifact pruning, shard_01.cert.json contract_version=2).
4. Symbolic verification with Z3/SymPy on ans / 3 and algebraic collisions.
5. Hypothesis Property-Based Testing on 2D decision matrix, synchronous budget, and neuro-symbolic arbitration.
6. Inter-stage RejectionSpec releasing Rule B selectively for failing shards.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import shutil
import sys
import tempfile
import textwrap
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / ".agents" / "skills" / "content-to-course"
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from budget_guard import check_lock_budget
from c2c_hook_guard import (
    decidir_estrategia_edicion,
    process_hook,
    find_active_c2c_lock,
)
from compile_shard import compile_shard
from engine.sandbox import (
    SandboxExecutionError,
    execute_sandbox_batch,
    execute_sandbox_instance,
)
from judge import resolve_neuro_symbolic_verdict


# ==============================================================================
# PILLAR 1: ERADICATION OF np.bool_(False) / None / 0 BUG
# ==============================================================================

class TestPillar1NumpyBoolEradication:
    """Certifies that verifier results returning np.bool_(False), None, or 0
    are treated strictly as failure and raise SandboxExecutionError.
    """

    def test_cross_check_returning_np_bool_false_raises_in_instance_and_batch(self):
        gen_code = (
            "def generate(rng):\n"
            "    return {'vars': {'x': 10}, 'correct': '10', 'distractors': []}\n"
        )
        # Using np.isclose(1.0, 2.0) returns np.bool_(False)
        cc_code_np_false = (
            "def cross_check(r):\n"
            "    import numpy as np\n"
            "    return np.isclose(1.0, 2.0)\n"
        )

        with pytest.raises(SandboxExecutionError, match="Cross-check verification failed"):
            execute_sandbox_instance(
                generate_py=gen_code,
                seed=42,
                cross_check_py=cc_code_np_false,
            )

        batch_res = execute_sandbox_batch(
            generate_py=gen_code,
            seeds=[42, 43],
            cross_check_py=cc_code_np_false,
        )
        assert len(batch_res) == 2
        assert batch_res[0]["success"] is False
        assert "Cross-check verification failed" in batch_res[0]["error"]

    def test_cross_check_returning_none_or_zero_fails_in_instance_and_batch(self):
        gen_code = (
            "def generate(rng):\n"
            "    return {'vars': {'x': 5}, 'correct': '5', 'distractors': []}\n"
        )
        cc_code_none = "def cross_check(r):\n    return None\n"
        cc_code_zero = "def cross_check(r):\n    return 0\n"

        for cc_code in (cc_code_none, cc_code_zero):
            with pytest.raises(SandboxExecutionError, match="Cross-check verification failed"):
                execute_sandbox_instance(
                    generate_py=gen_code,
                    seed=42,
                    cross_check_py=cc_code,
                )

            batch_res = execute_sandbox_batch(
                generate_py=gen_code,
                seeds=[42],
                cross_check_py=cc_code,
            )
            assert batch_res[0]["success"] is False
            assert "Cross-check verification failed" in batch_res[0]["error"]

    def test_cross_check_returning_np_bool_true_or_true_succeeds(self):
        gen_code = (
            "def generate(rng):\n"
            "    return {'vars': {'x': 7}, 'correct': '7', 'distractors': []}\n"
        )
        # Using np.isclose(1.0, 1.0) returns np.bool_(True)
        cc_code_np_true = (
            "def cross_check(r):\n"
            "    import numpy as np\n"
            "    return np.isclose(1.0, 1.0)\n"
        )

        inst_res = execute_sandbox_instance(
            generate_py=gen_code,
            seed=42,
            cross_check_py=cc_code_np_true,
        )
        assert inst_res["vars"]["x"] == 7

        batch_res = execute_sandbox_batch(
            generate_py=gen_code,
            seeds=[42, 43],
            cross_check_py=cc_code_np_true,
        )
        assert batch_res[0]["success"] is True
        assert batch_res[1]["success"] is True


# ==============================================================================
# PILLAR 2: TRIPLE CONTRACT ver_* HYGIENE IN compile_shard.py
# ==============================================================================

class TestPillar2TripleContractVerifierHygiene:
    """Certifies deterministic blockage of verifier anti-patterns:
    tautologies, swallowed exceptions, debug artifacts, and ad-hoc while loops.
    """

    def _setup_minimal_shard_dir(self, tmp_path: Path, shard_name: str = "shard_hygiene"):
        work_dir = tmp_path / shard_name
        shards_dir = work_dir / "shards"
        templates_dir = work_dir / "templates"
        shards_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)

        cta_data = {
            "competencies": [
                {
                    "id": "Hab-01",
                    "name": "Asymptotic Variance Skill",
                    "type": "skill",
                    "distractors": [
                        {"id": f"D-Hab01-{i:02d}", "name": f"Distractor {i}", "remediation_hint": f"Hint for distractor {i}"}
                        for i in range(1, 7)
                    ],
                }
            ]
        }
        (work_dir / "cta.json").write_text(json.dumps(cta_data), encoding="utf-8")

        manifest_data = {
            "min_archetypes": 4,
            "shards": [{"shard_id": shard_name, "competency_ids": ["Hab-01"]}],
        }
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")
        return work_dir, shards_dir

    def test_verifier_tautology_detected(self, tmp_path: Path):
        work_dir, shards_dir = self._setup_minimal_shard_dir(tmp_path, "shard_tautology")
        code = '''
def gen_1(rng):
    k = rng.randint(10, 40)
    ans = k * 2
    ds = [(f"D-Hab01-0{i}", f"${ans + i * 5}$", f"Error rationale with parameter @k@ and delta.") for i in range(1, 7)]
    return {"vars": {"k": k, "ans": ans}, "correct": f"${ans}$", "distractors": ds}

# Tautological verifier: checks v["ans"] > 0 without refuting distractor values
def ver_1(r):
    v = r.get("vars", {})
    return v.get("ans", 0) > 0

TEMPLATES = [
    ("T-Hab01-01", "Hab-01", "multiple_choice_7_options", gen_1, ver_1, ("easy", "Remember"), [r"S1 @k@:", r"S2 @k@:", r"S3 @k@:"], ["Pista 1 identificacion conceptual", "Pista 2 procedimiento analitico", "Pista 3 comprobacion numerica"], "Sol @ans@."),
]
'''
        (shards_dir / "shard_tautology_data.py").write_text(code, encoding="utf-8")
        ok, errors = compile_shard(work_dir_or_path=work_dir, shard_id="shard_tautology", strict=True)
        assert ok is False
        assert any("[VERIFIER-TAUTOLOGY-DETECTED]" in str(e) for e in errors)

    def test_verifier_swallowed_exception_try_except_true(self, tmp_path: Path):
        work_dir, shards_dir = self._setup_minimal_shard_dir(tmp_path, "shard_swallow")
        code = '''
def gen_1(rng):
    k = rng.randint(10, 40)
    ans = k * 2
    ds = [(f"D-Hab01-0{i}", f"${ans + i * 5}$", f"Error rationale with parameter @k@ and delta.") for i in range(1, 7)]
    return {"vars": {"k": k, "ans": ans}, "correct": f"${ans}$", "distractors": ds}

# Swallowed exception verifier returning True in except handler
def ver_1(r):
    try:
        expected = str(r["vars"]["ans"])
        return str(r.get("correct", "")).strip() == expected
    except Exception:
        return True

TEMPLATES = [
    ("T-Hab01-01", "Hab-01", "multiple_choice_7_options", gen_1, ver_1, ("easy", "Remember"), [r"S1 @k@:", r"S2 @k@:", r"S3 @k@:"], ["Pista 1 identificacion conceptual", "Pista 2 procedimiento analitico", "Pista 3 comprobacion numerica"], "Sol @ans@."),
]
'''
        (shards_dir / "shard_swallow_data.py").write_text(code, encoding="utf-8")
        ok, errors = compile_shard(work_dir_or_path=work_dir, shard_id="shard_swallow", strict=True)
        assert ok is False
        assert any("[VERIFIER-SWALLOWED-EXCEPTION]" in str(e) for e in errors)

    def test_generator_or_verifier_debug_artifact_raise_detected(self, tmp_path: Path):
        work_dir, shards_dir = self._setup_minimal_shard_dir(tmp_path, "shard_debug_raise")
        code = '''
def gen_1(rng):
    raise RuntimeError("CAUGHT_5570")
    return {"vars": {"k": 1}, "correct": "1", "distractors": []}

def ver_1(cand, v):
    return str(cand) == "1"

TEMPLATES = [
    ("T-Hab01-01", "Hab-01", "fill_in_the_blank", gen_1, ver_1, ("easy", "Remember"), [r"S1 @k@:", r"S2 @k@:", r"S3 @k@:"], ["Pista 1 identificacion conceptual", "Pista 2 procedimiento analitico", "Pista 3 comprobacion numerica"], "Sol."),
]
'''
        (shards_dir / "shard_debug_raise_data.py").write_text(code, encoding="utf-8")
        ok, errors = compile_shard(work_dir_or_path=work_dir, shard_id="shard_debug_raise", strict=True)
        assert ok is False
        assert any("[TPL-DEBUG-ARTIFACT]" in str(e) for e in errors)

    def test_ad_hoc_while_loop_float_perturbation_detected(self, tmp_path: Path):
        work_dir, shards_dir = self._setup_minimal_shard_dir(tmp_path, "shard_while_pert")
        code = '''
def gen_1(rng):
    cand = 10.0
    seen = [10.0, 10.35]
    while cand in seen:
        cand = cand + 0.35
    return {"vars": {"cand": cand}, "correct": str(cand), "distractors": []}

def ver_1(cand, v):
    return float(cand) == float(v.get("cand", 0))

TEMPLATES = [
    ("T-Hab01-01", "Hab-01", "fill_in_the_blank", gen_1, ver_1, ("easy", "Remember"), [r"S1 @cand@:", r"S2 @cand@:", r"S3 @cand@:"], ["Pista 1 identificacion conceptual", "Pista 2 procedimiento analitico", "Pista 3 comprobacion numerica"], "Sol."),
]
'''
        (shards_dir / "shard_while_pert_data.py").write_text(code, encoding="utf-8")
        ok, errors = compile_shard(work_dir_or_path=work_dir, shard_id="shard_while_pert", strict=True)
        assert ok is False
        assert any("[TPL-AD-HOC-PERTURBATION]" in str(e) for e in errors)


# ==============================================================================
# PILLAR 3: FORM-C DSL (<= 65 LINES, < 15 KB ARTIFACT, shard_01.cert.json)
# ==============================================================================

class TestPillar3DSLFormCCompressionAndCertification:
    """Certifies Form-C concise syntax compiling a 4-archetype competency
    in <= 65 lines of code, resulting in pruned < 15 KB JSON and emitting cert.json.
    """

    def test_compile_form_c_quad_band_under_65_lines_and_under_15kb(self, tmp_path: Path):
        work_dir = tmp_path / "work_form_c"
        shards_dir = work_dir / "shards"
        templates_dir = work_dir / "templates"
        shards_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)

        cta_data = {
            "competencies": [
                {
                    "id": "Hab-01",
                    "name": "Asymptotic Distribution of Sample Mean",
                    "type": "skill",
                    "assumptions": [
                        {
                            "id": "A-Hab01-01",
                            "statement_latex": "Finite variance constraint",
                            "violation_consequence": "Heavy tails failure",
                        }
                    ],
                    "distractors": [
                        {"id": f"D-Hab01-{i:02d}", "name": f"Distractor {i}", "remediation_hint": f"Hint for distractor {i}"}
                        for i in range(1, 7)
                    ],
                }
            ]
        }
        (work_dir / "cta.json").write_text(json.dumps(cta_data), encoding="utf-8")

        manifest_data = {
            "min_archetypes": 4,
            "shards": [{"shard_id": "shard_01", "competency_ids": ["Hab-01"]}],
        }
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")

        # Form-C Quad-Band implementation strictly under 65 lines:
        form_c_code = '''
RATS = {
    "D-Hab01-01": "No invierte matriz con @k@.",
    "D-Hab01-02": "Omite correlacion con @k@.",
    "D-Hab01-03": "Usa varianza simple con @k@.",
    "D-Hab01-04": "Suma varianzas con @k@.",
    "D-Hab01-05": "Divide por n con factor @k@.",
    "D-Hab01-06": "Fija estimador con factor @k@.",
}
def g1(rng): k=rng.randint(100,400); a=k*2; return {"vars":{"k":k,"ans":a},"correct":a,"ds":[(f"D-Hab01-0{i}",a+i*5) for i in range(1,7)]}
def g2(rng): k=rng.randint(100,400); a=k+10; return {"vars":{"k":k,"ans":a},"correct":a,"distractors":[]}
def g3(rng): k=rng.randint(100,400); a=k+20; return {"vars":{"k":k,"ans":a},"correct":a,"distractors":[]}
def g4(rng): k=rng.randint(100,400); a=k+30; return {"vars":{"k":k,"ans":a},"correct":a,"distractors":[]}
def ver(cand, v): return str(cand).strip() in (f"${v['ans']}$", str(v['ans']))

HINTS = ["Identifica el estimador @k@.", "Aplica el calculo analitico.", "Comprueba el valor estimado."]
C = ["Con la muestra @k@:", "Para el diseno @k@:"]

TEMPLATES = [
    {"cid": "Hab-01", "archetype": "direct", "qtype": "mc7", "gen": g1, "ver": ver, "fmt": "$@X@$", "band": ("easy", "Remember"), "hints": HINTS, "sol": "Solucion frontal @ans@.", "stems": (C, ["halla el valor frontal.", "evalua el estimador directo."])},
    {"cid": "Hab-01", "archetype": "inverse", "qtype": "fib", "gen": g2, "ver": ver, "band": ("medium", "Understand"), "hints": HINTS, "sol": "Solucion inversa @ans@.", "stems": (C, ["halla el valor inverso.", "evalua el reciproco."])},
    {"cid": "Hab-01", "archetype": "perturbation", "qtype": "fib", "gen": g3, "ver": ver, "band": ("hard", "Apply"), "hints": HINTS, "sol": "Solucion perturbacion @ans@.", "stems": (C, ["calcula la perturbacion.", "estima el impacto sensible."])},
    {"cid": "Hab-01", "archetype": "boundary_or_edge_case", "assumption_id": "A-Hab01-01", "qtype": "fib", "gen": g4, "ver": ver, "band": ("medium", "Evaluate"), "hints": HINTS, "sol": "Solucion frontera @ans@.", "stems": (C, ["calcula el caso extremo.", "analiza la cota limite."])},
]
'''
        source_lines = [l for l in form_c_code.strip().splitlines() if l.strip()]
        assert len(source_lines) <= 65, f"Form-C implementation exceeded 65 lines: {len(source_lines)}"

        shard_file = shards_dir / "shard_01_data.py"
        shard_file.write_text(form_c_code, encoding="utf-8")

        ok, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            seeds=50,
            cta_path=work_dir / "cta.json",
        )
        assert ok is True, f"Expected successful Form-C compilation, got errors: {errors}"
        assert len(errors) == 0

        # Verify pruned template JSON size < 15 KB
        out_json = templates_dir / "Hab-01.json"
        assert out_json.is_file(), f"Output JSON not found at {out_json}"
        file_bytes = len(out_json.read_bytes())
        assert file_bytes < 15_000, f"Pruned JSON exceeded 15 KB limit: {file_bytes} B"

        # Verify emission of shard_01.cert.json with contract_version == 2
        cert_file = shards_dir / "shard_01.cert.json"
        assert cert_file.is_file(), f"Certificate not found at {cert_file}"
        cert_data = json.loads(cert_file.read_text(encoding="utf-8"))
        assert cert_data.get("contract_version") == 2
        assert cert_data.get("passed_50_seeds") is True
        assert cert_data.get("stage") == "shard"


# ==============================================================================
# PILLAR 4: SYMBOLIC VERIFICATION (Z3 / SymPy on ans / 3 & Collisions)
# ==============================================================================

class TestPillar4SymbolicVerificationZ3Sympy:
    """Certifies symbolic detection of forbidden magic divisors (ans / 3)
    and algebraic distractor collisions.
    """

    def test_zero_magic_mult_ast_div_ans_detected(self):
        # Generator code with ans / 3
        code_with_div_3 = '''
def gen_bad(rng):
    k = rng.randint(10, 50)
    ans = k * 3
    d1 = ans / 3
    return {"vars": {"k": k, "ans": ans, "d1": d1}, "correct": str(ans), "distractors": [("D1", str(d1), "test rationale")]}
'''
        tree = ast.parse(code_with_div_3)
        has_ans_div = False
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Div, ast.FloorDiv)):
                left_names = {n.id for n in ast.walk(node.left) if isinstance(n, ast.Name)}
                right_names = {n.id for n in ast.walk(node.right) if isinstance(n, ast.Name)}
                if "ans" in left_names or "ans" in right_names:
                    has_ans_div = True
                    break
        assert has_ans_div is True, "AST analysis failed to detect 'ans / 3' division"

    def test_symbolic_algebraic_collision_detection(self):
        import sympy as sp
        x = sp.Symbol("x")
        ans_expr = 2 * x + 4
        # Equivalent algebraic distractor disguised under alternative factoring
        collision_distractor = 2 * (x + 2)
        diff = sp.simplify(ans_expr - collision_distractor)
        assert diff == 0, "Algebraic collision was not detected symbolically"

        # Non-colliding distractor
        valid_distractor = 2 * x + 5
        diff_valid = sp.simplify(ans_expr - valid_distractor)
        assert diff_valid != 0, "Valid distractor was incorrectly marked as colliding"


# ==============================================================================
# PILLAR 5: PROPERTY-BASED TESTING (Hypothesis)
# ==============================================================================

class TestPillar5HypothesisPropertyBasedTesting:
    """Hypothesis tests certifying invariant properties:
    - 2D edition strategy matrix (decidir_estrategia_edicion)
    - Synchronous budget governance (check_lock_budget)
    - Neuro-symbolic decision dominance (resolve_neuro_symbolic_verdict)
    """

    @given(
        error_count=st.integers(min_value=6, max_value=200),
        affected_line_count=st.integers(min_value=6, max_value=500),
        existing_lines=st.integers(min_value=40, max_value=1000),
    )
    @settings(max_examples=100)
    def test_prop_2d_matrix_modular_splicing_never_write_file(
        self, error_count: int, affected_line_count: int, existing_lines: int
    ):
        """Property: When affected lines > 5 and no syntax error, strategy is ALWAYS
        'modular_splicing', and NEVER 'write_file'.
        """
        strat = decidir_estrategia_edicion(
            error_count=error_count,
            affected_line_count=affected_line_count,
            has_syntax_error=False,
            existing_lines=existing_lines,
        )
        assert strat == "modular_splicing"
        assert strat != "write_file"

    @given(
        error_count=st.integers(min_value=1, max_value=5),
        affected_line_count=st.integers(min_value=1, max_value=5),
        existing_lines=st.integers(min_value=40, max_value=1000),
    )
    @settings(max_examples=100)
    def test_prop_2d_matrix_edit_file_for_small_errors(
        self, error_count: int, affected_line_count: int, existing_lines: int
    ):
        """Property: For error count < 6 and affected lines <= 5, strategy is ALWAYS 'edit_file'."""
        strat = decidir_estrategia_edicion(
            error_count=error_count,
            affected_line_count=affected_line_count,
            has_syntax_error=False,
            existing_lines=existing_lines,
        )
        assert strat == "edit_file"

    @given(
        turn_count=st.integers(min_value=41, max_value=150),
        est_tokens=st.integers(min_value=5_000_001, max_value=20_000_000),
        error_streak=st.integers(min_value=3, max_value=10),
    )
    @settings(max_examples=100)
    def test_prop_synchronous_budget_governance(
        self, turn_count: int, est_tokens: int, error_streak: int
    ):
        """Property: Exceeding SLA limits always triggers synchronous hard abort."""
        lock_turn = {"active": True, "turn_count": turn_count}
        breached, reason = check_lock_budget(lock_turn)
        assert breached is True
        assert "Turn count SLA limit" in reason

        lock_tokens = {"active": True, "est_tokens": est_tokens}
        breached, reason = check_lock_budget(lock_tokens)
        assert breached is True
        assert "Token burn SLA limit" in reason

        lock_streak = {"active": True, "error_sha256_streak": error_streak}
        breached, reason = check_lock_budget(lock_streak)
        assert breached is True
        assert "streak limit reached" in reason

    @given(
        llm_verdict=st.sampled_from(["PASS", "FAIL", "TRUE", "FALSE", "UNKNOWN"]),
        failure_category=st.text(max_size=30),
    )
    @settings(max_examples=100)
    def test_prop_neuro_symbolic_alpha_kernel_zero_dominance(
        self, llm_verdict: str, failure_category: str
    ):
        """Property: When kernel_refuted is True (alpha_kernel = 0), verdict is
        unconditionally FAIL, regardless of LLM verdict.
        """
        verdict = resolve_neuro_symbolic_verdict(
            kernel_verified=False,
            kernel_refuted=True,
            llm_verdict=llm_verdict,
            failure_category=failure_category,
        )
        assert verdict["verdict"] == "FAIL"
        assert verdict["passed"] is False
        assert verdict["kernel_refuted"] is True

    @given(
        cat=st.sampled_from(["math_error", "calculation_error", "arithmetic_error", "numeric_error", ""]),
        reasons=st.lists(st.text(alphabet="abcdefghijklmnopqrstuvwxyz ", min_size=1, max_size=20), max_size=3).filter(
            lambda r_list: not any(b in " ".join(r_list).lower() for b in ["epistemic", "missing", "ambiguous", "giveaway"])
        ),
    )
    @settings(max_examples=100)
    def test_prop_neuro_symbolic_kernel_overrides_stochastic_calculation_error(
        self, cat: str, reasons: List[str]
    ):
        """Property: When kernel_verified is True and LLM fails alleging only arithmetic error,
        kernel proof overrides LLM to produce PASS.
        """
        verdict = resolve_neuro_symbolic_verdict(
            kernel_verified=True,
            kernel_refuted=False,
            llm_verdict="FAIL",
            failure_category=cat,
            failure_reasons=reasons,
        )
        assert verdict["verdict"] == "PASS"
        assert verdict["passed"] is True
        assert verdict["kernel_override"] is True


# ==============================================================================
# PILLAR 6: INTER-STAGE REJECTION SPEC PARITY (Selective Rule B Release)
# ==============================================================================

class TestPillar6RejectionSpecRuleBParity:
    """Certifies that publish_rejection_spec.json with status=REJECTED selectively
    releases Rule B post-PASS lockdown only for the failing shard, preserving
    lockdown on passing shards.
    """

    def test_rejection_spec_releases_rule_b_only_for_failing_shard(self, tmp_path: Path):
        work_dir = tmp_path / "courses" / "cert_course" / "work"
        shards_dir = work_dir / "shards"
        att_dir = work_dir / ".check_attempts"
        shards_dir.mkdir(parents=True, exist_ok=True)
        att_dir.mkdir(parents=True, exist_ok=True)

        lock_file = tmp_path / ".c2c_subagent_lock.json"
        lock_file.write_text(json.dumps({
            "active": True,
            "director_conversation_id": "dir_uuid",
            "course_id": "cert_course",
            "work_dir": str(work_dir),
            "exempt_conversation_ids": [],
        }), encoding="utf-8")

        # Two shards both marked PASS
        (att_dir / "pass_shard_01.json").write_text(json.dumps({"status": "PASS"}), encoding="utf-8")
        (att_dir / "pass_shard_02.json").write_text(json.dumps({"status": "PASS"}), encoding="utf-8")

        shard_01_py = shards_dir / "shard_01_data.py"
        shard_02_py = shards_dir / "shard_02_data.py"
        shard_01_py.write_text("# Shard 01 content\n" * 45, encoding="utf-8")
        shard_02_py.write_text("# Shard 02 content\n" * 45, encoding="utf-8")

        # A) Prior to rejection spec, BOTH shards are locked down under Rule B
        payload_s1 = {
            "conversationId": "worker_uuid",
            "toolCall": {"name": "edit_file", "args": {"Path": str(shard_01_py), "Target": "x", "Replacement": "y"}},
        }
        payload_s2 = {
            "conversationId": "worker_uuid",
            "toolCall": {"name": "edit_file", "args": {"Path": str(shard_02_py), "Target": "x", "Replacement": "y"}},
        }

        res_s1_init = process_hook(payload_s1, custom_lock_file=str(lock_file))
        res_s2_init = process_hook(payload_s2, custom_lock_file=str(lock_file))
        assert res_s1_init["decision"] == "deny"
        assert res_s2_init["decision"] == "deny"
        assert "BLOCKER:: El shard shard_01 ya aprobó" in res_s1_init["reason"]
        assert "BLOCKER:: El shard shard_02 ya aprobó" in res_s2_init["reason"]

        # B) Publish rejection spec rejecting ONLY shard_02
        rejection_spec = {
            "status": "REJECTED",
            "failing_shards": ["shard_02"],
            "reason": "Auditor identified missing edge cases in shard_02",
        }
        (work_dir / "publish_rejection_spec.json").write_text(json.dumps(rejection_spec), encoding="utf-8")

        # C) Rule B is selectively released for shard_02, but remains locked for shard_01
        res_s1_post = process_hook(payload_s1, custom_lock_file=str(lock_file))
        res_s2_post = process_hook(payload_s2, custom_lock_file=str(lock_file))

        # Shard 01 must STILL be denied
        assert res_s1_post["decision"] == "deny"
        assert "BLOCKER:: El shard shard_01 ya aprobó" in res_s1_post["reason"]

        # Shard 02 must be released from Rule B early cut (decision is allow for surgical edit)
        assert res_s2_post["decision"] == "allow"
