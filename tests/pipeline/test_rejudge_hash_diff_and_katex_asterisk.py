"""Unit tests for template-level SHA-256 rejudge hash-diff and raw '*' KaTeX leak detection."""

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

_skill_root = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

from engine.invariants import validate_katex_syntax  # noqa: E402
from judge import _compute_template_hash, generate_judge_batch  # noqa: E402
import run as run_mod  # noqa: E402


# ---------------------------------------------------------------------------
# 1. KaTeX raw digit-asterisk-digit multiplication detection
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "context,bad_text",
    [
        ("detailed_solution", "Sustituyendo obtenemos $K^*(A)=(A/(2*0.11))^{2}$ en el óptimo."),
        ("stem", "Calcule el valor de $500*0.73*0.27$ en el equilibrio."),
        ("detailed_solution", "Evaluando $$2 * 3 + x^*(t)$$ en la frontera."),
    ],
)
def test_katex_blocks_raw_digit_asterisk_multiplication(context: str, bad_text: str) -> None:
    errs = validate_katex_syntax(bad_text, context=context)
    assert any("[TPL-KATEX-SYMPY-LEAK]" in e for e in errs), f"Expected [TPL-KATEX-SYMPY-LEAK], got: {errs}"


@pytest.mark.parametrize(
    "context,good_text",
    [
        ("detailed_solution", r"Sustituyendo obtenemos $K^*(A)=(A/(2 \cdot 0.11))^{2}$ en el óptimo."),
        ("stem", r"La trayectoria óptima $x^*(t)$ y el precio sombra $\lambda^*(t) = 0$."),
        ("detailed_solution", r"El control óptimo es $u^*(t) = 1 - e^{t-2}$ para $t \in [0, 2]$."),
    ],
)
def test_katex_allows_valid_star_superscripts(context: str, good_text: str) -> None:
    errs = validate_katex_syntax(good_text, context=context)
    assert not any("[TPL-KATEX-SYMPY-LEAK]" in e for e in errs), f"Unexpected leak error: {errs}"


# ---------------------------------------------------------------------------
# 2. Per-template SHA-256 hash tracking & surgical rejudge detection
# ---------------------------------------------------------------------------


def _make_template(tid: str, cid: str, val: int) -> dict:
    return {
        "id": tid,
        "template_id": tid,
        "competency_id": cid,
        "interaction_type": "fill_in_the_blank",
        "difficulty": "medium",
        "bloom": "Apply",
        "stem": f"Calcule {val} + @x@ en {tid}.",
        "stem_variants": [
            f"Calcule {val} + @x@ en {tid}.",
            f"Determine el valor de {val} + @x@ para {tid}.",
            f"Halle la suma {val} + @x@ ({tid}).",
        ],
        "generate_py": f"def generate_params(rng):\n    x = rng.randint(2, 9)\n    return {{'x': x, 'ans': str({val} + x), 'answer': str({val} + x), '_seed': 1}}\n",
        "cross_check_py": "",
        "hints": ["Pista 1", "Pista 2", "Pista 3"],
        "solution": f"Sumando {val} + @x@ = @ans@.",
        "detailed_solution": f"Paso 1: Sumamos {val} + @x@ = @ans@.",
        "answer_key": "@ans@",
        "correct_answer": "@ans@",
        "distractor_ids": [],
    }


def _make_runner(work_dir: Path, ids=None) -> run_mod.PipelineRunner:
    runner = run_mod.PipelineRunner.__new__(run_mod.PipelineRunner)
    runner.work_dir = work_dir
    runner.ids = ids
    runner.no_pointer = True
    return runner


def test_generate_judge_batch_persists_template_hashes_and_detects_only_changed(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    tpl_dir = work_dir / "templates"
    tpl_dir.mkdir(parents=True)

    t1 = _make_template("T-C01-01", "C-01", 10)
    t2 = _make_template("T-C01-02", "C-01", 20)
    t3 = _make_template("T-C02-01", "C-02", 30)
    (tpl_dir / "C-01.json").write_text(json.dumps([t1, t2]), encoding="utf-8")
    (tpl_dir / "C-02.json").write_text(json.dumps([t3]), encoding="utf-8")

    generate_judge_batch(templates_path=tpl_dir, work_dir=work_dir, samples_per_template=1)

    ev_path = work_dir / "verification" / "evaluated_competencies.json"
    assert ev_path.is_file()
    ev_data = json.loads(ev_path.read_text(encoding="utf-8"))
    tpl_hashes = ev_data.get("template_hashes", {})
    assert set(tpl_hashes.keys()) == {"T-C01-01", "T-C01-02", "T-C02-01"}
    assert tpl_hashes["T-C01-01"] == _compute_template_hash(t1)

    # Modify ONLY T-C01-02 (collateral or repaired edit); T-C01-01 and T-C02-01 stay identical
    t2_edited = _make_template("T-C01-02", "C-01", 25)
    (tpl_dir / "C-01.json").write_text(json.dumps([t1, t2_edited]), encoding="utf-8")

    runner = _make_runner(work_dir)
    cids, tids = runner._detect_changed_templates()
    assert cids == ["C-01"]
    assert tids == ["T-C01-02"]

    # Explicit competency id should still narrow to changed/failed templates within C-01
    cids_exp, tids_exp = runner._detect_changed_templates(explicit_ids=["C-01"])
    assert cids_exp == ["C-01"]
    assert tids_exp == ["T-C01-02"]

    # Failed template from baseline report is also included even if hash wasn't edited yet
    (work_dir / "judge_report_baseline.json").write_text(
        json.dumps({"failed_templates": ["T-C01-01"]}), encoding="utf-8"
    )
    cids_fail, tids_fail = runner._detect_changed_templates(explicit_ids=["C-01"])
    assert cids_fail == ["C-01"]
    assert tids_fail == ["T-C01-01", "T-C01-02"]


def test_detect_changed_templates_legacy_fallback_without_template_hashes(tmp_path: Path) -> None:
    work_dir = tmp_path / "work"
    tpl_dir = work_dir / "templates"
    (work_dir / "verification").mkdir(parents=True)
    tpl_dir.mkdir(parents=True)

    t1 = _make_template("T-C01-01", "C-01", 10)
    (tpl_dir / "C-01.json").write_text(json.dumps([t1]), encoding="utf-8")

    # Legacy evaluated_competencies.json with competency_hashes only (no template_hashes)
    (work_dir / "verification" / "evaluated_competencies.json").write_text(
        json.dumps({"evaluated_competency_ids": ["C-01"], "competency_hashes": {"C-01": "old_hash"}}),
        encoding="utf-8",
    )

    runner = _make_runner(work_dir)
    cids, tids = runner._detect_changed_templates()
    assert cids == ["C-01"]
    assert tids == []


# ---------------------------------------------------------------------------
# 3. Template-granular rejudge-compare merge
# ---------------------------------------------------------------------------


def test_rejudge_compare_merges_at_template_granularity(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True)

    (work_dir / "rejudge_scope.json").write_text(
        json.dumps({"ids": ["C-01"], "template_ids": ["T-C01-01"], "baseline": "judge_report_baseline.json"}),
        encoding="utf-8",
    )
    # Baseline had 2 disagreements in C-01: T-C01-01 (rejudged) and T-C01-02 (untouched, must be preserved)
    (work_dir / "judge_report_baseline.json").write_text(
        json.dumps(
            {
                "total_items": 10,
                "agreed_items": 8,
                "disagreements": [
                    {"competency_id": "C-01", "template_id": "T-C01-01", "item_id": "T-C01-01_judge_1"},
                    {"competency_id": "C-01", "template_id": "T-C01-02", "item_id": "T-C01-02_judge_1"},
                ],
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        run_mod,
        "compare_judge_responses",
        lambda work_dir: {"all_complete": True, "total_items": 2, "disagreements": []},
    )

    runner = _make_runner(work_dir)
    merged = runner.run_stage_rejudge_compare()
    assert merged["passed"] is False
    assert merged["failed_templates"] == ["T-C01-02"]
    assert merged["rejudged_templates"] == ["T-C01-01"]
    assert len(merged["disagreements"]) == 1
    assert merged["disagreements"][0]["template_id"] == "T-C01-02"
