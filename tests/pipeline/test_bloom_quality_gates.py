"""Tests for M20 Bloom quality gates across stage_contract, check_cta, cta_merge,
plan_shards, dispatch, shard_compiler_steps, standardized_audit_engine, and unified_audit_engine.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[2]
C2C_DIR = ROOT_DIR / ".agents" / "skills" / "content-to-course"
QA_DIR = ROOT_DIR / ".agents" / "skills" / "course-qa-evaluator" / "scripts"
UNIFIED_DIR = ROOT_DIR / ".agents" / "skills" / "c2c-unified-auditor" / "scripts"

for p in (str(ROOT_DIR), str(C2C_DIR), str(QA_DIR), str(UNIFIED_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from check_cta import check_cta_bloom_portfolio, check_cta_part, validate_cta_rules  # noqa: E402
from cta_merge import _build_outline_payload, apply_harmonize  # noqa: E402
from engine.shard_compiler_steps import evaluate_m3_and_m20_archetype_gates  # noqa: E402
from engine.stage_contract import (  # noqa: E402
    check_template_bloom_coherence,
    competency_contract,
    compute_cta_bloom_portfolio_metrics,
    max_achievable_bloom_rank,
)
from standardized_audit_engine import generate_deterministic_qa_report, run_full_audit  # noqa: E402
from unified_audit_engine import generate_merged_markdown_report  # noqa: E402


def _make_distractor(cid: str, idx: int, is_skill: bool) -> dict:
    code = cid.replace("-", "")
    return {
        "id": f"D-{code}-{idx:02d}",
        "name": f"Error {idx}",
        "wrong_belief": f"Asume fórmula errónea #{idx} sobre la pendiente del capital.",
        "correct_belief": "Usa la ecuación exacta del estado estacionario $sf(k)=dk$.",
        "omitted_step": f"Omitió verificar exponente #{idx}." if is_skill else None,
        "trigger": f"Al calcular paso #{idx}",
        "manifestation": f"Escribe término alterado #{idx}",
        "error_type": "procedural_slip",
        "severity": "medium",
        "origin": "source",
        "evidence": {"doc": "solow.pdf", "page": 1},
        "remediation_hint": (
            f"Verifique cuidadosamente la derivación del término #{idx} y sustituya correctamente en $sf(k)=dk$."
        ),
    }


def _make_comp(
    cid: str,
    ctype: str,
    bloom: str,
    modalities: list[str],
    prereqs: list[str],
    with_assumptions: bool = True,
    num_distractors: int | None = None,
) -> dict:
    is_skill = ctype == "skill"
    n_dist = num_distractors if num_distractors is not None else (6 if is_skill else 3)
    assumptions = (
        [{"id": f"A-{cid.replace('-', '')}-01", "statement_latex": r"$a \in (0,1)$", "violation_consequence": r"Equilibrio degenerado si $a \ge 1$."}]
        if (with_assumptions and ctype in ("concept", "skill"))
        else []
    )
    return {
        "id": cid,
        "type": ctype,
        "name": f"Competencia {cid}",
        "description_latex": f"Dominio formal y análisis cuantitativo de la competencia {cid} en equilibrio de crecimiento.",
        "bloom": bloom,
        "prerequisites": prereqs,
        "evidence": [{"doc": "solow.pdf", "page": 1}],
        "distractors": [_make_distractor(cid, i, is_skill) for i in range(1, n_dist + 1)],
        "assumptions": assumptions,
        "recommended_modalities": modalities,
    }


def _write_manifest(work_dir: Path, extra: dict | None = None) -> dict:
    manifest = {
        "course_id": "test_bloom_course",
        "files": [{"doc": "solow.pdf", "total_pages": 30, "valid_page_range": [1, 30]}],
    }
    if extra:
        manifest.update(extra)
    (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return manifest


def test_stage_contract_bloom_metrics_and_coherence():
    strong_comps = [
        _make_comp("H-01", "fact", "Remember", ["fill_in_the_blank", "multiple_select"], []),
        _make_comp("C-01", "concept", "Evaluate", ["adversarial_break", "proof_dag", "multiple_select"], ["H-01"]),
        _make_comp("Hab-01", "skill", "Evaluate", ["open_symbolic", "adversarial_break", "unstructured_model"], ["C-01"]),
        _make_comp("Hab-02", "skill", "Evaluate", ["open_symbolic", "proof_dag", "adversarial_break"], ["C-01"]),
        _make_comp("Hab-03", "skill", "Evaluate", ["open_symbolic", "proof_dag", "adversarial_break"], ["C-01"]),
    ]
    strong_m = compute_cta_bloom_portfolio_metrics(strong_comps)
    assert strong_m["active_gate"] is True
    assert strong_m["passes"] is True, f"Expected strong portfolio to pass: {strong_m}"
    assert strong_m["expected_bloom_index"] >= strong_m["adaptive_bloom_floor"]

    weak_comps = [
        _make_comp("H-01", "fact", "Remember", ["concept_matching", "fill_in_the_blank"], []),
        _make_comp("C-01", "concept", "Understand", ["concept_matching", "multiple_choice_7_options"], ["H-01"], num_distractors=6),
        _make_comp("Hab-01", "skill", "Apply", ["fill_in_the_blank", "open_symbolic"], ["C-01"]),
        _make_comp("Hab-02", "skill", "Apply", ["fill_in_the_blank", "invariant_canvas"], ["C-01"]),
        _make_comp("Hab-03", "skill", "Apply", ["fill_in_the_blank", "invariant_canvas"], ["C-01"]),
    ]
    weak_m = compute_cta_bloom_portfolio_metrics(weak_comps)
    assert weak_m["active_gate"] is True
    assert weak_m["passes"] is False
    assert len(weak_m["violations"]) >= 2
    assert weak_m["weak_competencies"][0]["id"] in {"H-01", "C-01", "Hab-01", "Hab-02", "Hab-03"}

    # Adaptive floor relaxes gracefully on Fact-heavy courses
    fact_heavy = [
        _make_comp(f"H-0{i}", "fact", "Remember", ["fill_in_the_blank", "multiple_select"], [])
        for i in range(1, 5)
    ] + [_make_comp("C-01", "concept", "Analyze", ["proof_dag", "multiple_select"], ["H-01"])]
    fh_m = compute_cta_bloom_portfolio_metrics(fact_heavy)
    assert fh_m["adaptive_bloom_floor"] < 3.50

    # --append excludes [BASE]
    excl_m = compute_cta_bloom_portfolio_metrics(weak_comps, exclude_ids={"H-01", "C-01"})
    assert excl_m["eligible_competencies"] == 3
    assert excl_m["active_gate"] is False

    # Coherence anti-Goodhart bounds
    assert check_template_bloom_coherence("multiple_choice_7_options", "direct", "Evaluate") is not None
    assert check_template_bloom_coherence("concept_matching", "perturbation", "Evaluate") is not None
    assert check_template_bloom_coherence("fill_in_the_blank", "direct", "Analyze") is not None
    assert check_template_bloom_coherence("fill_in_the_blank", "inverse", "Analyze") is None
    assert check_template_bloom_coherence("adversarial_break", "boundary_or_edge_case", "Apply") is not None
    assert check_template_bloom_coherence("unstructured_model", "direct", "Understand") is not None
    assert check_template_bloom_coherence("adversarial_break", "boundary_or_edge_case", "Evaluate") is None
    assert max_achievable_bloom_rank(["fill_in_the_blank", "concept_matching"]) == 4

    c_contract = competency_contract("skill", num_modalities=3, target_bloom="Evaluate")
    assert c_contract["target_bloom"] == "Evaluate"


def test_check_cta_bloom_floor_and_adjust_modalities_in_harmonize(tmp_path: Path):
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    manifest = _write_manifest(work_dir)

    weak_comps = [
        _make_comp("H-01", "fact", "Remember", ["concept_matching", "fill_in_the_blank"], []),
        _make_comp("C-01", "concept", "Understand", ["concept_matching", "fill_in_the_blank"], ["H-01"]),
        _make_comp("Hab-01", "skill", "Apply", ["fill_in_the_blank", "open_symbolic"], ["C-01"]),
        _make_comp("Hab-02", "skill", "Apply", ["fill_in_the_blank", "open_symbolic"], ["C-01"]),
        _make_comp("Hab-03", "skill", "Apply", ["fill_in_the_blank", "open_symbolic"], ["C-01"]),
    ]
    cta_draft = {
        "course_id": "test_bloom_course",
        "title": "Test Bloom",
        "contract_version": 2,
        "competencies": weak_comps,
    }

    # 1. check_cta_part does NOT trigger global bloom gate; validate_cta_rules DOES; --no-bloom-gate bypasses
    part_res = check_cta_part(cta_draft, manifest_data=manifest)
    assert part_res[0], f"check_cta_part should pass: {part_res[1]}"

    val_fail = validate_cta_rules(cta_draft, manifest_data=manifest)
    assert not val_fail[0]
    assert any("[CTA-BLOOM-FLOOR]" in e for e in val_fail[1])

    val_bypass = validate_cta_rules(cta_draft, manifest_data=manifest, enforce_bloom_gate=False)
    assert val_bypass[0], f"Expected bypass to pass: {val_bypass[1]}"

    # 2. _build_outline_payload includes bloom, distractor_count, bloom_portfolio_preview
    outline = _build_outline_payload("test_bloom_course", "Test Bloom", "Macro", weak_comps)
    assert outline["bloom_portfolio_preview"]["passes"] is False
    assert outline["competencies"][0]["bloom"] == "Remember"
    assert outline["competencies"][0]["distractor_count"] == 3

    # 3. apply_harmonize with 5th key adjust_modalities repairs in 1 turn
    (work_dir / "cta_draft.json").write_text(json.dumps(cta_draft), encoding="utf-8")
    (work_dir / "cta_order.json").write_text(json.dumps({"order": [c["id"] for c in weak_comps]}), encoding="utf-8")
    (work_dir / "duplicate_candidates.json").write_text("[]", encoding="utf-8")

    # 3a. Eligibility guard: reject unstructured_model on fact (assumptions=[])
    bad_harm = {
        "duplicate_decisions": [],
        "add_prerequisites": [],
        "rename": [],
        "drop_duplicate_distractors": [],
        "adjust_modalities": [
            {"competency": "H-01", "recommended_modalities": ["unstructured_model", "multiple_select"]}
        ],
    }
    (work_dir / "cta_harmonize.json").write_text(json.dumps(bad_harm), encoding="utf-8")
    with pytest.raises(ValueError, match=r"\[CTA-MODALITY-ELIGIBILITY\]"):
        apply_harmonize(work_dir)

    # 3b. Valid adjust_modalities passes and writes merge_report.json
    good_harm = {
        "duplicate_decisions": [],
        "add_prerequisites": [],
        "rename": [],
        "drop_duplicate_distractors": [],
        "adjust_modalities": [
            {"competency": "C-01", "recommended_modalities": ["adversarial_break", "proof_dag", "multiple_select"], "bloom": "Evaluate"},
            {"competency": "Hab-01", "recommended_modalities": ["open_symbolic", "adversarial_break", "unstructured_model"], "bloom": "Evaluate"},
            {"competency": "Hab-02", "recommended_modalities": ["open_symbolic", "proof_dag", "adversarial_break"], "bloom": "Evaluate"},
            {"competency": "Hab-03", "recommended_modalities": ["open_symbolic", "proof_dag", "adversarial_break"], "bloom": "Evaluate"},
        ],
    }
    (work_dir / "cta_harmonize.json").write_text(json.dumps(good_harm), encoding="utf-8")
    final_cta = apply_harmonize(work_dir)
    c01 = next(c for c in final_cta["competencies"] if c["id"] == "C-01")
    assert c01["bloom"] == "Evaluate"
    assert c01["recommended_modalities"] == ["adversarial_break", "proof_dag", "multiple_select"]
    m_report = json.loads((work_dir / "merge_report.json").read_text(encoding="utf-8"))
    assert any(d.get("operation") == "adjust_modalities" for d in m_report["decisions"])


def test_apply_harmonize_append_protects_base_and_excludes_from_bloom_gate(tmp_path: Path):
    work_dir = tmp_path / "work_append"
    work_dir.mkdir()
    base_comp = _make_comp("C-01", "concept", "Understand", ["concept_matching", "fill_in_the_blank"], [])
    delta_comp = _make_comp("Hab-01", "skill", "Apply", ["fill_in_the_blank", "open_symbolic"], ["C-01"])
    _write_manifest(work_dir, extra={"delta": {"existing_competency_ids": ["C-01"], "existing_competencies": [base_comp]}})
    draft = {"course_id": "test_append", "title": "Append", "contract_version": 2, "competencies": [delta_comp]}
    (work_dir / "cta_draft.json").write_text(json.dumps(draft), encoding="utf-8")
    (work_dir / "cta_order.json").write_text(json.dumps({"order": ["Hab-01"]}), encoding="utf-8")
    (work_dir / "duplicate_candidates.json").write_text("[]", encoding="utf-8")

    # Mutating [BASE] via adjust_modalities must fail
    bad = {
        "duplicate_decisions": [],
        "add_prerequisites": [],
        "rename": [],
        "drop_duplicate_distractors": [],
        "adjust_modalities": [{"competency": "C-01", "recommended_modalities": ["proof_dag", "adversarial_break"]}],
    }
    (work_dir / "cta_harmonize.json").write_text(json.dumps(bad), encoding="utf-8")
    with pytest.raises(ValueError, match="Epistemic monotonicity violation"):
        apply_harmonize(work_dir)

    # Clean append with 1 delta comp passes without blocking on legacy [BASE]
    clean = {
        "duplicate_decisions": [],
        "add_prerequisites": [],
        "rename": [],
        "drop_duplicate_distractors": [],
    }
    (work_dir / "cta_harmonize.json").write_text(json.dumps(clean), encoding="utf-8")
    res = apply_harmonize(work_dir)
    assert len(res["competencies"]) == 1


def test_shard_gate_bloom_coherence_and_feasible_target(tmp_path: Path):
    def _gen(r):
        x = r.randint(2, 9)
        return {"vars": {"x": x}, "correct": str(x)}

    def _make_tpl(idx: int, qtype: str, arch: str, diff: str, bloom: str) -> dict:
        return {
            "id": f"T-C01-{idx:02d}",
            "cid": "C-01",
            "interaction_type": qtype,
            "question_type": qtype,
            "archetype": arch,
            "difficulty": diff,
            "bloom": bloom,
            "stem_es": f"Variante única #{idx} para equilibrio con parámetro @x@:",
            "stem_variants": [
                f"Calcule propiedad #{idx} dado parámetro @x@ con ecuación $f(k)=k^a$:",
                f"Determine resultado #{idx} cuando @x@ cambia en modelo de Solow:",
                f"Evalúe condición #{idx} para valor @x@ en estado estacionario:",
                f"Resuelva caso #{idx} considerando parámetro @x@ positivo:",
            ],
            "generator_code": f"def gen_{idx}(r):\n x = r.randint(2, {10 + idx})\n return {{'vars': {{'x': x}}, 'correct': str(x + {idx})}}",
            "hints": ["Pista 1 conceptual.", "Pista 2 operativa.", "Pista 3 verificación."],
            "explanation_es": "Paso 1: sustituya el parámetro en la ecuación de equilibrio y resuelva el valor exacto.",
        }

    cta_comp = {
        "id": "C-01",
        "type": "concept",
        "bloom": "Evaluate",
        "recommended_modalities": ["fill_in_the_blank", "concept_matching"],
    }
    # Bad: FIB direct=Analyze (fails coherence) and concept_matching=Evaluate (fails coherence)
    bad_tpls = [
        _make_tpl(1, "fill_in_the_blank", "direct", "easy", "Analyze"),
        _make_tpl(2, "fill_in_the_blank", "inverse", "medium", "Apply"),
        _make_tpl(3, "concept_matching", "perturbation", "hard", "Evaluate"),
        _make_tpl(4, "concept_matching", "boundary_or_edge_case", "hard", "Understand"),
    ]
    errs_bad = evaluate_m3_and_m20_archetype_gates(
        expected_cids=["C-01"],
        templates_by_cid={"C-01": bad_tpls},
        gen_callables_by_cid={"C-01": [_gen] * 4},
        cta_comp_map={"C-01": cta_comp},
        cta_contract_version=2,
        shard_entry={},
        shard_data_path=tmp_path / "shard_01_data.py",
        fix_files_by_cid={},
        locator=None,
        healed_source="",
        raw_source="",
        strict=True,
        seeds=10,
        norm_shard_id="shard_01",
        fail_total=True,
        eff_k=2,
        eff_min_arch=4,
    )
    assert any("[M3-BLOOM-COHERENCE]" in e and "T-C01-01" in e for e in errs_bad)
    assert any("[M3-BLOOM-COHERENCE]" in e and "T-C01-03" in e for e in errs_bad)

    # Good: FIB/concept_matching max achievable is Analyze (rank 4); target_bloom='Evaluate' clamps to Analyze
    good_tpls = [
        _make_tpl(1, "fill_in_the_blank", "direct", "easy", "Apply"),
        _make_tpl(2, "fill_in_the_blank", "inverse", "medium", "Analyze"),
        _make_tpl(3, "concept_matching", "perturbation", "hard", "Understand"),
        _make_tpl(4, "concept_matching", "boundary_or_edge_case", "hard", "Analyze"),
    ]
    errs_good = evaluate_m3_and_m20_archetype_gates(
        expected_cids=["C-01"],
        templates_by_cid={"C-01": good_tpls},
        gen_callables_by_cid={"C-01": [_gen] * 4},
        cta_comp_map={"C-01": cta_comp},
        cta_contract_version=2,
        shard_entry={},
        shard_data_path=tmp_path / "shard_01_data.py",
        fix_files_by_cid={},
        locator=None,
        healed_source="",
        raw_source="",
        strict=True,
        seeds=10,
        norm_shard_id="shard_01",
        fail_total=True,
        eff_k=2,
        eff_min_arch=4,
    )
    assert not any("[M3-BLOOM-COHERENCE]" in e or "[M3-TARGET-BLOOM]" in e for e in errs_good)

    # Below feasible target: max is Apply (< Analyze) -> triggers [M3-TARGET-BLOOM]
    low_tpls = [
        _make_tpl(1, "fill_in_the_blank", "direct", "easy", "Apply"),
        _make_tpl(2, "fill_in_the_blank", "inverse", "medium", "Apply"),
        _make_tpl(3, "concept_matching", "perturbation", "hard", "Understand"),
        _make_tpl(4, "concept_matching", "boundary_or_edge_case", "hard", "Apply"),
    ]
    errs_low = evaluate_m3_and_m20_archetype_gates(
        expected_cids=["C-01"],
        templates_by_cid={"C-01": low_tpls},
        gen_callables_by_cid={"C-01": [_gen] * 4},
        cta_comp_map={"C-01": cta_comp},
        cta_contract_version=2,
        shard_entry={},
        shard_data_path=tmp_path / "shard_01_data.py",
        fix_files_by_cid={},
        locator=None,
        healed_source="",
        raw_source="",
        strict=True,
        seeds=10,
        norm_shard_id="shard_01",
        fail_total=True,
        eff_k=2,
        eff_min_arch=4,
    )
    assert any("[M3-TARGET-BLOOM]" in e for e in errs_low)


def test_qa_and_unified_engines_report_weighted_bloom_index():
    questions = []
    for i in range(1, 25):
        questions.append({
            "id": f"Q-Hab01-{i:03d}",
            "competency_id": "Hab-01",
            "interaction_type": "adversarial_break" if i <= 12 else "open_symbolic",
            "difficulty": ["easy", "medium", "hard"][i % 3],
            "bloom_taxonomy_level": "Evaluate" if i <= 12 else "Analyze",
            "stem": f"Pregunta {i} sobre equilibrio $sf(k)=dk$:",
            "hints": ["Pista 1.", "Pista 2.", "Pista 3."],
            "detailed_solution": "Paso 1: sustituya $sf(k)=dk$ para hallar el estado estacionario.",
        })
    course = {
        "course_id": "test_bloom_qa",
        "title": "Test Bloom QA",
        "competencies": [{"id": "Hab-01", "category": "Skill", "name": "Capital", "prerequisites": []}],
        "questions": questions,
    }
    telemetry = run_full_audit(course)
    zpd = telemetry["dimension_summaries"]["zpd_progression_linter"]
    assert zpd["bloom_weighted_index"] == 4.5
    assert zpd["adaptive_bloom_floor"] == 4.0
    assert zpd["bloom_tier"] == "ÉLITE"
    assert zpd["bloom_coherence_violations_count"] == 0

    qa_json, qa_md = generate_deterministic_qa_report(telemetry, course)
    assert qa_json["course_metadata"]["bloom_index"]["tier"] == "ÉLITE"
    assert "Índice Bloom Ponderado (1–5)" in qa_md

    merged_md = generate_merged_markdown_report(
        "test_bloom_qa",
        "00000000-0000-0000-0000-000000000000",
        qa_json,
        {"audit_telemetry": telemetry, "title": "Test Bloom QA", "total_competencies": 1, "total_questions": 24},
        {},
        {},
    )
    assert "Índice Bloom Ponderado (1–5)" in merged_md
    assert "4.50 / 5.0" in merged_md


def test_plan_shards_and_dispatch_propagate_target_bloom(tmp_path: Path):
    import dispatch
    import plan_shards

    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    shards_dir.mkdir(parents=True)
    manifest = _write_manifest(work_dir)
    (work_dir / "corpus.md").write_text("Modelo de crecimiento económico con función $f(k)=k^a$.", encoding="utf-8")

    comps = [
        _make_comp("H-01", "fact", "Remember", ["fill_in_the_blank", "multiple_select"], []),
        _make_comp("C-01", "concept", "Evaluate", ["adversarial_break", "proof_dag", "multiple_select"], ["H-01"]),
        _make_comp("Hab-01", "skill", "Evaluate", ["open_symbolic", "adversarial_break", "unstructured_model"], ["C-01"]),
    ]
    cta_path = work_dir / "cta.json"
    cta_path.write_text(
        json.dumps({"course_id": "test_bloom_course", "title": "Test", "contract_version": 2, "competencies": comps}),
        encoding="utf-8",
    )

    pre_manifest = plan_shards.plan_shards(cta_path, shards_dir)
    c01_contracts = [
        s["stage4_contract"]["C-01"]
        for s in pre_manifest["shards"]
        if "C-01" in (s.get("stage4_contract") or {})
    ]
    hab01_contracts = [
        s["stage4_contract"]["Hab-01"]
        for s in pre_manifest["shards"]
        if "Hab-01" in (s.get("stage4_contract") or {})
    ]
    assert c01_contracts and c01_contracts[0]["target_bloom"] == "Evaluate"
    assert hab01_contracts and hab01_contracts[0]["target_bloom"] == "Evaluate"

    dispatch_res = dispatch.dispatch_authors(work_dir, pointer=True)
    assert dispatch_res.get("Subagents")
    items_dir = work_dir / "dispatch" / "items"
    author_mds = sorted(items_dir.glob("author_*_data.md"))
    assert author_mds
    combined_md = "\n".join(p.read_text(encoding="utf-8") for p in author_mds)
    assert "target_bloom" in combined_md
    assert "Evaluate" in combined_md
    assert "[M3-BLOOM-COHERENCE]" in combined_md


def test_validate_cta_rules_excludes_manifest_base_from_bloom_floor(tmp_path: Path):
    """validate_cta_rules must exclude manifest delta.existing_competency_ids from [CTA-BLOOM-FLOOR]."""
    base_comps = [
        _make_comp(
            f"H-0{i}",
            "fact",
            "Remember",
            ["concept_matching", "fill_in_the_blank"],
            [] if i == 1 else [f"H-0{i - 1}"],
        )
        for i in range(1, 6)
    ]
    delta_comp = _make_comp(
        "Hab-01",
        "skill",
        "Evaluate",
        ["open_symbolic", "adversarial_break", "unstructured_model"],
        ["H-05"],
    )
    manifest = {
        "course_id": "test_append_cli",
        "files": [{"doc": "solow.pdf", "total_pages": 30, "valid_page_range": [1, 30]}],
        "delta": {"existing_competency_ids": [c["id"] for c in base_comps], "existing_competencies": base_comps},
    }
    cta = {
        "course_id": "test_append_cli",
        "title": "Append CLI Test",
        "contract_version": 2,
        "competencies": base_comps + [delta_comp],
    }
    valid, rule_errors = validate_cta_rules(cta, manifest)
    assert valid, f"Expected base comps in manifest.delta to be excluded from [CTA-BLOOM-FLOOR]: {rule_errors}"


def test_apply_harmonize_dict_adjust_modalities_and_forward_prereq_merge(tmp_path: Path):
    """adjust_modalities dict-of-dict unpacks cleanly and merge preserves forward prereqs for topological sort."""
    work_dir = tmp_path / "work_dict_merge"
    work_dir.mkdir()
    _write_manifest(work_dir)
    comps = [
        _make_comp("H-01", "fact", "Remember", ["fill_in_the_blank", "multiple_select"], []),
        _make_comp("C-01", "concept", "Understand", ["concept_matching", "multiple_choice_7_options"], ["H-01"], num_distractors=6),
        _make_comp("C-02", "concept", "Evaluate", ["adversarial_break", "proof_dag", "multiple_select"], ["H-01"]),
        _make_comp("C-03", "concept", "Understand", ["concept_matching", "multiple_choice_7_options"], ["C-02"], num_distractors=6),
        _make_comp("Hab-01", "skill", "Evaluate", ["open_symbolic", "adversarial_break", "unstructured_model"], ["C-01"]),
        _make_comp("Hab-02", "skill", "Evaluate", ["open_symbolic", "proof_dag", "adversarial_break"], ["C-01"]),
    ]
    draft = {"course_id": "test_bloom_course", "title": "Test", "contract_version": 2, "competencies": comps}
    (work_dir / "cta_draft.json").write_text(json.dumps(draft), encoding="utf-8")
    (work_dir / "cta_order.json").write_text(json.dumps({"order": [c["id"] for c in comps]}), encoding="utf-8")
    (work_dir / "duplicate_candidates.json").write_text("[]", encoding="utf-8")

    harmonize = {
        # C-01 absorbs C-03 (which depends on C-02 appearing after C-01 in original order)
        "duplicate_decisions": [
            {"decision": "merge", "keep_id": "C-01", "drop_id": "C-03", "reason": "Same concept"},
        ],
        "add_prerequisites": [],
        "rename": [],
        "drop_duplicate_distractors": [],
        "adjust_modalities": {
            "C-01": {
                "recommended_modalities": ["adversarial_break", "proof_dag", "multiple_select"],
                "bloom": "Evaluate",
            },
        },
    }
    (work_dir / "cta_harmonize.json").write_text(json.dumps(harmonize), encoding="utf-8")
    final_cta = apply_harmonize(work_dir)
    ids = [c["id"] for c in final_cta["competencies"]]
    c01 = next(c for c in final_cta["competencies"] if c["id"] == "C-01")
    assert c01["bloom"] == "Evaluate"
    assert c01["recommended_modalities"] == ["adversarial_break", "proof_dag", "multiple_select"]
    assert "C-02" in c01["prerequisites"]
    assert ids.index("C-02") < ids.index("C-01")
