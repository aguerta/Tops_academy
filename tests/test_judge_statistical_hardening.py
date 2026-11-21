"""Statistical & deterministic certification hardening tests for Stage 3 & Stage 5."""

import json
import sys
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from check_templates import _check_stem_variant_parity  # noqa: E402
from engine.assemble import assemble_question  # noqa: E402
from judge import (  # noqa: E402
    DEFAULT_MAX_SEED_RETRIES,
    DEFAULT_OVERLAP_RATIO,
    DEFAULT_TARGET_TOTAL_EVALUATIONS,
    _compute_cohens_kappa,
    _compute_template_risk_score,
    compare_judge_responses,
    generate_judge_batch,
    split_judge_batch,
)


def _make_fib_template(
    tid: str,
    cid: str = "C-01",
    with_verifier: bool = True,
    fail_on_even_seed: bool = False,
    num_variants: int = 3,
    interaction_type: str = "fill_in_the_blank",
):
    gen_py = (
        "def generate(rng):\n"
        "    x = rng.randint(2, 9)\n"
        "    ans = x * 2\n"
        "    return {\n"
        "        'vars': {'x': x},\n"
        "        'correct': str(ans),\n"
        "        'tolerance': 0.01,\n"
        "    }\n"
    )
    if fail_on_even_seed:
        ver_py = (
            "def verify(res):\n"
            "    return False\n"
        )
    elif with_verifier:
        ver_py = (
            "def verify(res):\n"
            "    return int(res['correct']) == res['vars']['x'] * 2\n"
        )
    else:
        ver_py = ""

    variants = [f"Variante {i}: calcule el doble de @x@." for i in range(num_variants)]
    return {
        "id": tid,
        "competency_id": cid,
        "interaction_type": interaction_type,
        "stem": "Calcule el doble de @x@.",
        "stem_variants": variants,
        "generate_py": gen_py,
        "verifier_code": ver_py,
        "hints": [
            "Identifica el valor numerico asignado a la variable dada en el enunciado.",
            "Multiplica la cantidad observada por el factor escalar correspondiente.",
            "Comprueba que el resultado sea exactamente dos veces el valor inicial.",
        ],
        "solution": "Para hallar el doble de @x@ se multiplica directamente por 2 obteniendo el valor exacto.",
    }


class TestStemVariantParity:
    def test_detects_missing_placeholder_in_one_variant(self):
        tpl = {
            "id": "T-C03-02",
            "interaction_type": "fill_in_the_blank",
            "stem": "Considere una economía con horizonte @T@ y tasa @s@.",
            "stem_variants": [
                "Dado un periodo @T@ y tasa de ahorro @s@, calcule el estado estacionario.",
                "Con tasa @s@ durante @T@ periodos, determine el producto.",
                "Con tasa de ahorro @s@, determine el producto final.",  # missing @T@
            ],
        }
        violations = _check_stem_variant_parity(tpl)
        assert len(violations) == 1
        assert violations[0][0] == "stem_variants[2]"
        assert violations[0][1] == ["T"]

    def test_passes_when_all_variants_have_consistent_placeholders(self):
        tpl = {
            "id": "T-C03-03",
            "stem": "Calcule @a@ + @b@.",
            "stem_variants": [
                "Sume @a@ y @b@.",
                "Obtenga el total de @b@ junto con @a@.",
                "Determine el resultado de añadir @a@ a @b@.",
            ],
        }
        assert _check_stem_variant_parity(tpl) == []


class TestDeterministicVariantRotation:
    def test_assemble_question_explicit_stem_variant_index(self):
        tpl = _make_fib_template("T-ROT-01", num_variants=4)
        gen_res = {"vars": {"x": 5}, "correct": "10", "tolerance": 0.01}
        stems = [
            assemble_question(tpl, gen_res, "C-01", idx + 1, seed=42, stem_variant_index=idx)["stem"]
            for idx in range(4)
        ]
        assert len(set(stems)) == 4
        for idx, s in enumerate(stems):
            assert f"Variante {idx}:" in s

    def test_generate_judge_batch_rotates_variants_without_replacement(self, tmp_path: Path):
        tpl = _make_fib_template("T-ROT-02", num_variants=3)
        tpl_path = tmp_path / "templates.json"
        tpl_path.write_text(json.dumps([tpl]), encoding="utf-8")
        batch_p, gt_p = generate_judge_batch(
            templates_path=tpl_path,
            work_dir=tmp_path / "work",
            samples_per_template=3,
            random_seed=7,
        )
        gt = json.loads(gt_p.read_text(encoding="utf-8"))
        var_indices = [rec["stem_variant_index"] for rec in gt.values()]
        assert sorted(var_indices) == [0, 1, 2]


class TestZeroToleranceSeedRetries:
    def test_default_max_seed_retries_is_one(self):
        assert DEFAULT_MAX_SEED_RETRIES == 1

    def test_single_failing_seed_is_immediately_refuted_without_silent_retry(self, tmp_path: Path):
        # Even seed 100 fails verifier; with max_seed_retries=1 it must NOT silently retry to odd seed
        tpl = _make_fib_template("T-FLAKY-01", fail_on_even_seed=True)
        tpl_path = tmp_path / "templates.json"
        tpl_path.write_text(json.dumps([tpl]), encoding="utf-8")
        _, gt_p = generate_judge_batch(
            templates_path=tpl_path,
            work_dir=tmp_path / "work",
            seeds=(100,),
            samples_per_template=1,
            random_seed=1,
        )
        gt = json.loads(gt_p.read_text(encoding="utf-8"))
        assert len(gt) == 1
        rec = next(iter(gt.values()))
        assert rec["kernel_refuted"] is True


class TestNeymanAllocationAndDoubleReadOverlap:
    def test_risk_score_orders_high_risk_templates_above_low_risk(self):
        low_risk = _make_fib_template("T-LOW", with_verifier=True, num_variants=2, interaction_type="multiple_choice_7_options")
        high_risk = _make_fib_template("T-HIGH", with_verifier=False, num_variants=4, interaction_type="open_symbolic")
        assert _compute_template_risk_score(high_risk) > _compute_template_risk_score(low_risk)

    def test_neyman_allocation_assigns_extra_samples_to_high_risk_templates(self, tmp_path: Path):
        # Create 4 low-risk templates and 2 high-risk templates, cap at 8 unique items
        tpls = [
            _make_fib_template(f"T-LOW-{i}", cid=f"C-0{i}", with_verifier=True, num_variants=2, interaction_type="multiple_choice_7_options")
            for i in range(1, 5)
        ] + [
            _make_fib_template("T-HIGH-1", cid="C-05", with_verifier=False, num_variants=4, interaction_type="fill_in_the_blank"),
            _make_fib_template("T-HIGH-2", cid="C-06", with_verifier=False, num_variants=4, interaction_type="fill_in_the_blank"),
        ]
        # Give low-risk templates valid MC7 generator so they pass invariants
        for t in tpls[:4]:
            t["generate_py"] = (
                "def generate(seed):\n"
                "    return {\n"
                "        'vars': {'x': 3},\n"
                "        'correct': '6',\n"
                "        'distractors': [\n"
                "            {'value': '3', 'distractor_id': 'D1', 'error_rationale': 'Omite multiplicar por dos el valor dado.'},\n"
                "            {'value': '9', 'distractor_id': 'D2', 'error_rationale': 'Multiplica por tres en lugar de dos.'},\n"
                "            {'value': '12', 'distractor_id': 'D3', 'error_rationale': 'Multiplica por cuatro en lugar de dos.'},\n"
                "            {'value': '15', 'distractor_id': 'D4', 'error_rationale': 'Multiplica por cinco en lugar de dos.'},\n"
                "            {'value': '18', 'distractor_id': 'D5', 'error_rationale': 'Multiplica por seis en lugar de dos.'},\n"
                "            {'value': '21', 'distractor_id': 'D6', 'error_rationale': 'Multiplica por siete en lugar de dos.'},\n"
                "        ],\n"
                "    }\n"
            )
            t["verifier_code"] = "def verify(res, seed):\n    return True\n"
        tpl_path = tmp_path / "templates.json"
        tpl_path.write_text(json.dumps(tpls), encoding="utf-8")

        _, gt_p = generate_judge_batch(
            templates_path=tpl_path,
            work_dir=tmp_path / "work",
            target_unique_items=8,
            random_seed=42,
        )
        gt = json.loads(gt_p.read_text(encoding="utf-8"))
        counts = {}
        for rec in gt.values():
            tid = rec["template_id"]
            counts[tid] = counts.get(tid, 0) + 1
        assert counts["T-HIGH-1"] >= 2
        assert counts["T-HIGH-2"] >= 2
        assert all(counts[f"T-LOW-{i}"] == 1 for i in range(1, 5))

    def test_split_judge_batch_injects_15pct_overlap_on_distinct_judges(self, tmp_path: Path):
        assert DEFAULT_TARGET_TOTAL_EVALUATIONS == 165
        assert DEFAULT_OVERLAP_RATIO == 0.15

        work = tmp_path / "work"
        (work / "verification").mkdir(parents=True, exist_ok=True)
        items = [
            {
                "item_id": f"T-{i:03d}_judge_1",
                "template_id": f"T-{i:03d}",
                "competency_id": f"C-{(i % 10) + 1:02d}",
                "interaction_type": "multiple_choice_7_options" if i % 2 == 0 else "fill_in_the_blank",
                "stem": f"Pregunta {i}",
            }
            for i in range(1, 141)  # 140 unique items
        ]
        (work / "verification" / "judge_batch.json").write_text(json.dumps(items), encoding="utf-8")

        paths = split_judge_batch(work, max_judges=10, items_per_judge=20, random_seed=123, overlap_ratio=0.15)
        assert 2 <= len(paths) <= 10

        seen_in_judges = {}
        total_evals = 0
        for j_idx, p in enumerate(paths):
            b = json.loads(p.read_text(encoding="utf-8"))
            assert len(b) <= 20
            total_evals += len(b)
            # No duplicate item_id inside the same judge
            ids_in_bucket = [x["item_id"] for x in b]
            assert len(ids_in_bucket) == len(set(ids_in_bucket))
            for iid in ids_in_bucket:
                seen_in_judges.setdefault(iid, []).append(j_idx)

        overlapped = [iid for iid, js in seen_in_judges.items() if len(js) == 2]
        assert len(overlapped) == 21  # round(140 * 0.15) == 21
        assert total_evals == 161 <= 165


class TestInterJudgeKappaAndAdaptiveLQAS:
    def test_cohens_kappa_calculation(self):
        perfect = _compute_cohens_kappa([(True, True)] * 10)
        assert perfect["raw_agreement"] == 1.0
        assert perfect["cohens_kappa"] == 1.0

        mixed = _compute_cohens_kappa([(True, True)] * 7 + [(False, False)] * 2 + [(True, False)])
        assert mixed["overlap_count"] == 10
        assert mixed["raw_agreement"] == 0.9
        assert 0.7 < mixed["cohens_kappa"] < 0.85

    def test_compare_reports_kappa_sensitivity_bound_and_lqas_flag(self):
        gt = {
            "T1_judge_1": {
                "item_id": "T1_judge_1",
                "template_id": "T1",
                "competency_id": "C1",
                "interaction_type": "fill_in_the_blank",
                "correct_value": "10",
                "tolerance": 0.01,
                "kernel_verified": True,
                "kernel_refuted": False,
            },
            "T2_judge_1": {
                "item_id": "T2_judge_1",
                "template_id": "T2",
                "competency_id": "C2",
                "interaction_type": "fill_in_the_blank",
                "correct_value": "20",
                "tolerance": 0.01,
                "kernel_verified": True,
                "kernel_refuted": False,
            },
        }
        # T1 has 1 judge failing by calc error -> kernel_override=True on k=1 -> triggers LQAS!
        # T2 has 2 independent judges both answering 20 -> double-read overlap!
        responses = [
            {"item_id": "T1_judge_1", "answer": "15"},
            {"item_id": "T2_judge_1", "answer": "20"},
            {"item_id": "T2_judge_1", "answer": "20"},
        ]
        rep = compare_judge_responses(responses=responses, ground_truth=gt)
        assert rep["passed"] is True
        assert rep["kernel_override_count"] == 1
        assert rep["single_seed_override_templates"] == ["T1"]
        assert rep["lqas_followup_required"] is True
        assert rep["inter_judge_reliability"]["overlap_count"] == 1
        assert rep["inter_judge_reliability"]["cohens_kappa"] == 1.0
        assert rep["statistical_certification"]["upper_defect_bound_95_adjusted"] <= 1.0

    def test_lqas_followup_with_prior_failure_triggers_guard_c(self):
        # During LQAS confirmation, T1 had 1 prior failure; failing 1 of the 2 new seeds => 2 total => Guard (c) blocks override!
        gt = {
            "T1_judge_1": {
                "item_id": "T1_judge_1",
                "template_id": "T1",
                "competency_id": "C1",
                "interaction_type": "fill_in_the_blank",
                "correct_value": "10",
                "tolerance": 0.01,
                "kernel_verified": True,
                "kernel_refuted": False,
            },
            "T1_judge_2": {
                "item_id": "T1_judge_2",
                "template_id": "T1",
                "competency_id": "C1",
                "interaction_type": "fill_in_the_blank",
                "correct_value": "20",
                "tolerance": 0.01,
                "kernel_verified": True,
                "kernel_refuted": False,
            },
        }
        responses = [
            {"item_id": "T1_judge_1", "answer": "10"},
            {"item_id": "T1_judge_2", "answer": "35"},  # 2nd failure across cycles!
        ]
        rep = compare_judge_responses(
            responses=responses,
            ground_truth=gt,
            prior_template_failures={"T1": 1},
        )
        assert rep["passed"] is False
        assert "T1" in rep["failed_templates"]
        assert rep["kernel_override_count"] == 0
