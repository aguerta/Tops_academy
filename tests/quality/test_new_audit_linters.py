"""Unit tests for the 4 new deterministic audit linters added via /learn:
1. ClonedDistractorValueLinter
2. ParentheticalTelltaleLinter
3. ArchetypeEntropyLinter
4. UninterpolatedMathVariableLinter
"""
import sys
from pathlib import Path
import pytest

_c2c_dir = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "content-to-course"
if str(_c2c_dir) not in sys.path:
    sys.path.insert(0, str(_c2c_dir))

_engine_dir = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "course-qa-evaluator" / "scripts"
if str(_engine_dir) not in sys.path:
    sys.path.insert(0, str(_engine_dir))

from course_publisher import CoursePublisher, PublishQualityGateError
from validator.models import ValidationResult

from standardized_audit_engine import (
    run_full_audit,
    ClonedDistractorValueLinter,
    ParentheticalTelltaleLinter,
    ArchetypeEntropyLinter,
    UninterpolatedMathVariableLinter,
    ZPDProgressionCalibrationLinter,
    RetrievalModalityDiversityLinter,
    SocraticScaffoldingIntegrityLinter,
    DiagnosticRationaleAlignmentLinter,
    AntiGamingPsychometricLinter,
    DAGMasteryTopologyLinter,
    KaTeXFrontendErgonomicsLinter,
)


def test_cloned_distractor_value_linter():
    course_data = {
        "course_id": "test_course",
        "competencies": [{"id": "C-01"}],
        "questions": [
            {
                "id": "Q-01",
                "competency_id": "C-01",
                "options": [
                    {"text": "Opción correcta: $x = 5$", "is_correct": True},
                    {"text": "Opción alterna 4: $x = 5$", "is_correct": False},
                ]
            },
            {
                "id": "Q-02",
                "competency_id": "C-01",
                "options": [
                    {"text": "$10$", "is_correct": True},
                    {"text": "$10$", "is_correct": False},
                ]
            }
        ]
    }
    issues = []
    summary = ClonedDistractorValueLinter().run(course_data, issues)
    assert summary["cloned_distractor_items_count"] == 2
    assert len(issues) == 2
    assert issues[0].severity == "critical"


def test_parenthetical_telltale_linter():
    course_data = {
        "course_id": "test_course",
        "competencies": [{"id": "C-01"}],
        "questions": [
            {
                "id": "Q-01",
                "competency_id": "C-01",
                "options": [
                    {"text": "$0.75$ (confusión con la proporción ruido a señal)", "is_correct": False},
                    {"text": "$0.50$ (definición errónea de varianza)", "is_correct": False},
                    {"text": "$0.25$", "is_correct": True},
                ]
            }
        ]
    }
    issues = []
    summary = ParentheticalTelltaleLinter().run(course_data, issues)
    assert summary["parenthetical_telltale_count"] == 1
    assert len(issues) == 2
    assert issues[0].severity == "critical"


def test_archetype_entropy_linter():
    # Case 1: 20 questions with 1 identical structural skeleton (ratio = 1.0 > 0.85 & distinct = 1 < 3)
    questions = []
    for i in range(20):
        questions.append({
            "id": f"Q-{i:02d}",
            "competency_id": "C-01",
            "stem": f"Considere el modelo de Solow con tasa de ahorro $s = 0.{i}$ y depreciación $\\delta = 0.05$. Calcule el capital estacionario.",
        })
    course_data = {
        "course_id": "test_course",
        "competencies": [{"id": "C-01"}],
        "questions": questions
    }
    issues = []
    summary = ArchetypeEntropyLinter().run(course_data, issues)
    assert summary["monotonous_competencies_count"] == 1
    assert "C-01" in summary["monotonous_competencies"]
    assert summary["low_archetype_variety_competencies_count"] == 1
    assert "C-01" in summary["low_archetype_variety_competencies"]
    assert len(issues) == 1
    assert issues[0].severity == "warning"

    # Case 2: 20 questions split 50%/50% across ONLY 2 skeletons (ratio = 0.50 <= 0.85, but distinct = 2 < 3)
    two_arch_qs = []
    for i in range(10):
        two_arch_qs.append({
            "id": f"Q-A-{i:02d}",
            "competency_id": "C-02",
            "stem": f"Dado el estimador muestral con tamaño $n = {i + 20}$, determine la varianza asintótica exacta.",
        })
        two_arch_qs.append({
            "id": f"Q-B-{i:02d}",
            "competency_id": "C-02",
            "stem": f"Si la varianza límite observada equivale a $\\sigma^2 = {i + 5}$, despeje el parámetro estructural subyacente.",
        })
    issues_two = []
    summary_two = ArchetypeEntropyLinter().run(
        {"course_id": "test_two_arch", "competencies": [{"id": "C-02"}], "questions": two_arch_qs},
        issues_two,
    )
    assert summary_two["monotonous_competencies_count"] == 1
    assert summary_two["low_archetype_variety_competencies_count"] == 1
    assert "C-02" in summary_two["low_archetype_variety_competencies"]
    assert summary_two["min_distinct_skeletons_observed"] == 2
    assert len(issues_two) == 1
    assert "Variedad insuficiente de arquetipos" in issues_two[0].message

    # Case 3: 18 questions balanced across 3 distinct skeletons (6/6/6 -> ratio = 0.33 <= 0.85 & distinct = 3 >= 3) -> CLEAN
    three_arch_qs = []
    for i in range(6):
        three_arch_qs.append({
            "id": f"Q-T1-{i:02d}",
            "competency_id": "Hab-01",
            "template_id": "T-Hab-01-01",
            "stem": f"Calcule directamente el equilibrio estacionario cuando la productividad toma valor $A = {i + 2}$.",
        })
        three_arch_qs.append({
            "id": f"Q-T2-{i:02d}",
            "competency_id": "Hab-01",
            "template_id": "T-Hab-01-02",
            "stem": f"Sabiendo que el capital de regla de oro converge a $k^* = {i + 10}$, infiera la tasa de ahorro requerida.",
        })
        three_arch_qs.append({
            "id": f"Q-T3-{i:02d}",
            "competency_id": "Hab-01",
            "template_id": "T-Hab-01-03",
            "stem": f"Ante un choque permanente sobre la depreciación $\\delta' = 0.0{i + 3}$, evalúe la dirección de transición dinámica.",
        })
    issues_three = []
    summary_three = ArchetypeEntropyLinter().run(
        {"course_id": "test_three_arch", "competencies": [{"id": "Hab-01"}], "questions": three_arch_qs},
        issues_three,
    )
    assert summary_three["monotonous_competencies_count"] == 0
    assert summary_three["low_archetype_variety_competencies_count"] == 0
    assert summary_three["min_distinct_skeletons_observed"] == 3
    assert len(issues_three) == 0


def test_uninterpolated_math_variable_linter():
    course_data = {
        "course_id": "test_course",
        "competencies": [{"id": "C-01"}],
        "questions": [
            {
                "id": "Q-01",
                "competency_id": "C-01",
                "stem": "El valor del estimador es $\\hat{\\beta} = {sigma2} / n$.",
                "detailed_solution": "Calculamos $x - -4$ directamente.",
                "options": [{"text": "Valor", "is_correct": True}]
            }
        ]
    }
    issues = []
    summary = UninterpolatedMathVariableLinter().run(course_data, issues)
    assert summary["uninterpolated_math_items_count"] == 1
    assert len(issues) >= 1


def test_full_audit_integration():
    course_data = {
        "course_id": "test_integration",
        "competencies": [{"id": "C-01", "name": "Concepto 1", "type": "Concept", "prerequisites": []}],
        "questions": [
            {
                "id": "Q-01",
                "competency_id": "C-01",
                "stem": "Enunciado limpio $x = 1$.",
                "hints": ["Pista 1", "Pista 2", "Pista 3"],
                "detailed_solution": "Solución detallada paso a paso.",
                "options": [
                    {"text": "Opción A", "is_correct": True, "error_rationale": "Correcto"},
                    {"text": "Opción B", "is_correct": False, "error_rationale": "Falso"},
                ]
            }
        ]
    }
    report = run_full_audit(course_data)
    assert "cloned_distractor_value_linter" in report["dimension_summaries"]
    assert "parenthetical_telltale_linter" in report["dimension_summaries"]
    assert "archetype_entropy_linter" in report["dimension_summaries"]
    assert "uninterpolated_math_variable_linter" in report["dimension_summaries"]
    assert "mastery_path_readiness" in report
    assert report["mastery_path_readiness"]["mpri_score"] >= 85.0


def test_path_to_mastery_v2_linters():
    # 1. ZPD collapse + Skill lower-order Bloom
    zpd_qs = [
        {"id": f"Q-{i}", "competency_id": "Hab-01", "difficulty": "medium", "bloom_taxonomy_level": "Understand", "stem": f"Item {i}"}
        for i in range(10)
    ]
    zpd_issues = []
    zpd_sum = ZPDProgressionCalibrationLinter().run(
        {"competencies": [{"id": "Hab-01", "category": "Skill"}], "questions": zpd_qs},
        zpd_issues,
    )
    assert zpd_sum["zpd_dead_competencies_count"] == 1
    assert zpd_sum["skill_higher_bloom_pct"] == 0.0

    # 2. Socratic hint poisoning & boilerplate + v3 'content' option key
    soc_issues = []
    soc_sum = SocraticScaffoldingIntegrityLinter().run(
        {
            "questions": [
                {
                    "id": "Q-SOC-1",
                    "competency_id": "Hab-01",
                    "options": [
                        {"content": "$256$", "is_correct": True},
                        {"content": "$135$", "is_correct": False},
                    ],
                    "hints": [
                        "Identifique la estructura conceptual de ECM: analice las relaciones formales y condiciones teóricas del modelo.",
                        "Revise el procedimiento analítico paso a paso para ECM, asegurando considerar adecuadamente: omitir el cuadrado del sesgo.",
                        "Antes de concluir, compruebe la consistencia dimensional del resultado de ECM.",
                    ],
                }
            ]
        },
        soc_issues,
    )
    assert soc_sum["poisoned_hints_items_count"] == 1
    assert any(iss.severity == "critical" for iss in soc_issues)

    # 3. Magic-multiplier fake numerical distractors
    diag_issues = []
    diag_sum = DiagnosticRationaleAlignmentLinter().run(
        {
            "questions": [
                {
                    "id": "Q-MAG-1",
                    "competency_id": "Hab-01",
                    "options": [
                        {"content": "$10.0$", "is_correct": True},
                        {"content": "$13.33$", "is_correct": False, "error_rationale": "R1"},
                        {"content": "$6.67$", "is_correct": False, "error_rationale": "R2"},
                        {"content": "$16.67$", "is_correct": False, "error_rationale": "R3"},
                        {"content": "$3.33$", "is_correct": False, "error_rationale": "R4"},
                    ],
                }
            ]
        },
        diag_issues,
    )
    assert diag_sum["magic_multiplier_distractor_items_count"] == 1

    # 4. Anti-gaming: vacuous quantifier, [R-15] length padding, cross-domain prefix, memorizable answers
    ag_qs = []
    for i in range(16):
        ag_qs.append({
            "id": f"Q-AG-{i}",
            "competency_id": "C-02",
            "stem": "Al examinar detenidamente las condiciones de frontera, resuelva: defina plim.",
            "options": [
                {
                    "content": "$\\lim_{n \\to \\infty} P(|X_n - 7| \\le 0.13) = 1$ válido para todo margen $\\varepsilon > 0$",
                    "is_correct": True,
                },
                {
                    "content": "$X_n = 7$, para los parámetros bajo análisis",
                    "is_correct": False,
                },
            ],
        })
    ag_issues = []
    ag_sum = AntiGamingPsychometricLinter().run(
        {"title": "Estadística Asintótica", "competencies": [{"id": "C-02"}], "questions": ag_qs},
        ag_issues,
    )
    assert ag_sum["memorizable_competencies_count"] == 1
    assert ag_sum["vacuous_quantifier_items_count"] == 16
    assert ag_sum["length_padded_items_count"] == 16
    assert ag_sum["cross_domain_prefix_items_count"] == 16

    # 5. DAG topology inversion & isolated island
    dag_issues = []
    dag_sum = DAGMasteryTopologyLinter().run(
        {
            "competencies": [
                {"id": "Hab-01", "category": "Skill", "prerequisites": ["C-01"]},
                {"id": "C-01", "category": "Concept", "prerequisites": []},
                {"id": "H-99", "category": "Fact", "prerequisites": []},
            ]
        },
        dag_issues,
    )
    assert dag_sum["inverted_prerequisite_edges_count"] == 1
    assert dag_sum["isolated_competencies_count"] == 1

    # 6. KaTeX frontend ergonomics: full-sentence \text{...} & raw $theta_hat$
    erg_issues = []
    erg_sum = KaTeXFrontendErgonomicsLinter().run(
        {
            "questions": [
                {
                    "id": "Q-ERG-1",
                    "competency_id": "C-01",
                    "stem": "Evalúe el estimador $theta_hat$ bajo muestreo aleatorio.",
                    "options": [
                        {
                            "content": "$\\text{La teoría asintótica exige que el proceso generador poblacional converja uniformemente}$",
                            "is_correct": False,
                        }
                    ],
                }
            ]
        },
        erg_issues,
    )
    assert erg_sum["prose_in_katex_text_items_count"] == 1
    assert erg_sum["raw_identifier_math_items_count"] == 1


def test_discovered_v2_self_improvement_rules():
    """Verify newly learned rules from Argon/Flash v2 audit loop:
    symbolic LaTeX hint poisoning, bound constant in forall, stuttered [R-15] padding, and disjoint subgraphs.
    """
    from standardized_audit_engine import (
        SocraticScaffoldingIntegrityLinter,
        AntiGamingPsychometricLinter,
        DAGMasteryTopologyLinter,
    )

    soc_issues = []
    soc_sum = SocraticScaffoldingIntegrityLinter().run(
        {
            "questions": [
                {
                    "id": "Q-SYM-1",
                    "competency_id": "H-03",
                    "hints": [
                        "Identifique la estructura conceptual de ECM: analice las relaciones formales.",
                        "Revise el procedimiento analítico paso a paso para ECM, asegurando considerar adecuadamente: $\\operatorname{ECM}(\\hat{\\theta}) = \\operatorname{Var}(\\hat{\\theta})$.",
                        "Antes de concluir, compruebe la consistencia dimensional del resultado de ECM.",
                    ],
                    "options": [{"content": "$\\operatorname{Var} + \\operatorname{Sesgo}^2$", "is_correct": True}],
                }
            ]
        },
        soc_issues,
    )
    assert soc_sum["poisoned_hints_items_count"] == 1

    ag_issues = []
    ag_sum = AntiGamingPsychometricLinter().run(
        {
            "title": "Estadística 3",
            "competencies": [{"id": "C-10"}],
            "questions": [
                {
                    "id": "Q-BND-1",
                    "competency_id": "C-10",
                    "stem": "Determine la propiedad asintótica.",
                    "options": [
                        {
                            "content": "Válido para todo $\\epsilon = 0.02 > 0$, bajo las hipótesis del modelo, bajo las hipótesis del modelo.",
                            "is_correct": True,
                        }
                    ],
                }
            ],
        },
        ag_issues,
    )
    assert ag_sum["vacuous_quantifier_items_count"] == 1
    assert ag_sum["length_padded_items_count"] == 1

    dag_issues = []
    dag_sum = DAGMasteryTopologyLinter().run(
        {
            "competencies": [
                {"id": "A-1", "prerequisites": []},
                {"id": "A-2", "prerequisites": ["A-1"]},
                {"id": "B-1", "prerequisites": []},
                {"id": "B-2", "prerequisites": ["B-1"]},
                {"id": "ISLAND-1", "prerequisites": []},
            ]
        },
        dag_issues,
    )
    assert dag_sum["multi_node_subgraphs_count"] == 2
    assert dag_sum["connected_components_count"] == 3
    assert any("sub-grafos" in iss.message for iss in dag_issues)


def _make_dummy_course_payload(num_q: int = 25) -> dict:
    comps = [
        {"id": f"C-{i:02d}", "name": f"Competency {i}", "category": "Concept", "type": "Concept", "level": "Analyze", "mastery_target": 100}
        for i in range(1, 4)
    ]
    questions = []
    for i in range(num_q):
        cid = f"C-{(i % 3) + 1:02d}"
        qid = f"Q-{i+1:03d}"
        questions.append({
            "id": qid,
            "competency_id": cid,
            "stem": f"Question stem text for item {qid} with sufficient descriptive wording.",
            "correct_answer": "Option A is correct",
            "options": [
                {"id": "opt_a", "option_id": "A", "content": "Option A is correct", "is_correct": True, "error_rationale": None},
                {"id": "opt_b", "option_id": "B", "content": "Option B distractor content with sufficient text length", "is_correct": False, "error_rationale": f"Misconception explanation for item {qid} B"},
                {"id": "opt_c", "option_id": "C", "content": "Option C distractor content with sufficient text length", "is_correct": False, "error_rationale": f"Misconception explanation for item {qid} C"},
                {"id": "opt_d", "option_id": "D", "content": "Option D distractor content with sufficient text length", "is_correct": False, "error_rationale": f"Misconception explanation for item {qid} D"},
            ],
            "bloom_taxonomy_level": "Analyze",
            "interaction_type": "multiple_choice_7_options",
            "hints": ["Hint 1 step scaffolding", "Hint 2 check calculations", "Hint 3 dimensional analysis"],
            "detailed_solution": f"Step by step solution for question {qid}.",
        })
    return {
        "course_id": "gate_test_course",
        "course_title": "Quality Gate Verification Unit Test Course",
        "competencies": comps,
        "questions": questions,
    }


def test_publish_quality_gate_mpri_low(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """PublishQualityGateError is raised when MPRI < 75.0 on banks with >= 20 questions."""
    monkeypatch.setattr(
        "course_publisher._load_run_full_audit",
        lambda project_root=None: lambda data: {
            "mpri_score": 72.5,
            "pillars": {
                "zpd_adaptive_progression": {"score": 20.0},
                "diagnostic_remediation_alignment": {"score": 15.0},
            },
            "diagnostics": {"rationale_uniqueness_pct": 85.0},
            "hard_penalties": [],
            "all_issues": [],
            "risk_clusters": {},
        },
    )
    publisher = CoursePublisher(courses_dir=tmp_path)
    with pytest.raises(PublishQualityGateError, match="MPRI score below threshold: 72.5 < 75.0"):
        publisher.publish(_make_dummy_course_payload(25), strict=True)


def test_publish_quality_gate_zpd_collapsed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """PublishQualityGateError is raised when ZPD score collapses to 0.0 with >= 6 questions."""
    monkeypatch.setattr(
        "course_publisher._load_run_full_audit",
        lambda project_root=None: lambda data: {
            "mpri_score": 85.0,
            "pillars": {
                "zpd_adaptive_progression": {"score": 0.0},
                "diagnostic_remediation_alignment": {"score": 15.0},
            },
            "diagnostics": {"rationale_uniqueness_pct": 85.0},
            "hard_penalties": [],
            "all_issues": [],
            "risk_clusters": {},
        },
    )
    publisher = CoursePublisher(courses_dir=tmp_path)
    with pytest.raises(PublishQualityGateError, match="ZPD progression score collapsed: 0.0 <= 0.0"):
        publisher.publish(_make_dummy_course_payload(10), strict=True)


def test_publish_quality_gate_p4_diagnostic_remediation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """PublishQualityGateError is raised on low P4 diagnostic score or static recycling (< 30% uniqueness)."""
    monkeypatch.setattr(
        "course_publisher._load_run_full_audit",
        lambda project_root=None: lambda data: {
            "mpri_score": 82.0,
            "pillars": {
                "zpd_adaptive_progression": {"score": 20.0},
                "diagnostic_remediation_alignment": {"score": 11.5},
            },
            "diagnostics": {"rationale_uniqueness_pct": 24.0},
            "hard_penalties": [],
            "all_issues": [],
            "risk_clusters": {},
        },
    )
    publisher = CoursePublisher(courses_dir=tmp_path)
    with pytest.raises(PublishQualityGateError, match="Diagnostic remediation deficiency"):
        publisher.publish(_make_dummy_course_payload(30), strict=True)


def test_publish_quality_gate_length_padded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """PublishQualityGateError is raised when options contain length padding artifacts."""
    monkeypatch.setattr(
        "course_publisher._load_run_full_audit",
        lambda project_root=None: lambda data: {
            "mpri_score": 88.0,
            "pillars": {
                "zpd_adaptive_progression": {"score": 20.0},
                "diagnostic_remediation_alignment": {"score": 15.0},
            },
            "diagnostics": {"rationale_uniqueness_pct": 85.0},
            "hard_penalties": [],
            "all_issues": [],
            "risk_clusters": {"length_padded_options": ["Q-001", "Q-002"]},
        },
    )
    publisher = CoursePublisher(courses_dir=tmp_path)
    with pytest.raises(PublishQualityGateError, match="Length-padded options detected"):
        publisher.publish(_make_dummy_course_payload(25), strict=True)


def test_publish_quality_gate_hard_penalties(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """PublishQualityGateError is raised when hard penalties or critical issues are flagged."""
    monkeypatch.setattr(
        "course_publisher._load_run_full_audit",
        lambda project_root=None: lambda data: {
            "mpri_score": 88.0,
            "pillars": {
                "zpd_adaptive_progression": {"score": 20.0},
                "diagnostic_remediation_alignment": {"score": 15.0},
            },
            "diagnostics": {"rationale_uniqueness_pct": 85.0},
            "hard_penalties": [{"rule": "P_CRIT", "reason": "Severe pedagogical breach"}],
            "all_issues": [{"severity": "critical", "message": "Critical formatting defect"}],
            "risk_clusters": {},
        },
    )
    publisher = CoursePublisher(courses_dir=tmp_path)
    with pytest.raises(PublishQualityGateError, match="Hard penalties detected"):
        publisher.publish(_make_dummy_course_payload(25), strict=True)


def test_publish_quality_gate_healthy_course_passes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Healthy tri-band course with strong MPRI, ZPD, and dynamic rationales passes the gate."""
    monkeypatch.setattr(
        "course_publisher._load_run_full_audit",
        lambda project_root=None: lambda data: {
            "mpri_score": 92.5,
            "pillars": {
                "zpd_adaptive_progression": {"score": 20.0},
                "diagnostic_remediation_alignment": {"score": 18.0},
            },
            "diagnostics": {"rationale_uniqueness_pct": 94.0},
            "hard_penalties": [],
            "all_issues": [],
            "risk_clusters": {},
        },
    )
    publisher = CoursePublisher(courses_dir=tmp_path)
    publisher._run_cli_validator = lambda p, strict=True: True
    monkeypatch.setattr(
        "course_publisher.validate_course_content",
        lambda raw, file_path=None, strict=False: ValidationResult(is_valid=True, file_path=file_path, errors=[]),
    )
    result = publisher.publish(_make_dummy_course_payload(25), strict=True)
    assert result.success is True


def test_archetype_entropy_linter_dynamic_contract_v2():
    """Verify ArchetypeEntropyLinter enforces 4 archetypes for contract_version >= 2,
    while retaining req_arch = 3 for legacy courses without contract_version >= 2."""
    linter = ArchetypeEntropyLinter()

    # 1. Course with 3 distinct skeletons under contract_version = 2 -> FAILS (requires 4)
    three_arch_qs = []
    for i in range(6):
        three_arch_qs.append({"id": f"Q-A-{i}", "competency_id": "C-01", "template_id": "T1", "stem": f"First skeleton with ${i}$."})
        three_arch_qs.append({"id": f"Q-B-{i}", "competency_id": "C-01", "template_id": "T2", "stem": f"Second pattern involving ${i + 5}$."})
        three_arch_qs.append({"id": f"Q-C-{i}", "competency_id": "C-01", "template_id": "T3", "stem": f"Third formulation calculating ${i + 10}$."})

    issues_v2_failing = []
    course_v2_failing = {
        "course_id": "v40_course",
        "contract_version": 2,
        "competencies": [{"id": "C-01"}],
        "questions": three_arch_qs,
    }
    summary_v2 = linter.run(course_v2_failing, issues_v2_failing)
    assert summary_v2["min_required_archetypes"] == 4
    assert summary_v2["low_archetype_variety_competencies_count"] == 1
    assert any("mínimo requerido: 4" in iss.message for iss in issues_v2_failing)

    # 2. Same 3 skeletons under legacy course (no contract_version or contract_version = 1) -> PASSES (requires 3)
    issues_legacy = []
    course_legacy = {
        "course_id": "legacy_v38_course",
        "competencies": [{"id": "C-01"}],
        "questions": three_arch_qs,
    }
    summary_legacy = linter.run(course_legacy, issues_legacy)
    assert summary_legacy["min_required_archetypes"] == 3
    assert summary_legacy["low_archetype_variety_competencies_count"] == 0
    assert len(issues_legacy) == 0

    # 3. Modern course with 4 distinct skeletons under contract_version = 2 -> PASSES (requires 4)
    four_arch_qs = list(three_arch_qs)
    for i in range(5):
        four_arch_qs.append({"id": f"Q-D-{i}", "competency_id": "C-01", "template_id": "T4", "stem": f"Fourth orthogonal structure analyzing ${i * 3}$."})

    issues_v2_passing = []
    course_v2_passing = {
        "course_id": "v40_course_ok",
        "contract_version": 2,
        "competencies": [{"id": "C-01"}],
        "questions": four_arch_qs,
    }
    summary_v2_pass = linter.run(course_v2_passing, issues_v2_passing)
    assert summary_v2_pass["min_required_archetypes"] == 4
    assert summary_v2_pass["low_archetype_variety_competencies_count"] == 0
    assert len(issues_v2_passing) == 0


def test_archetype_entropy_linter_historical_courses_backward_compatibility():
    """Historical v3.8 courses in courses/*.json must evaluate with req_arch = 3 without variety warnings."""
    import json
    linter = ArchetypeEntropyLinter()
    historical_courses = [
        "courses/solow_growth_model.json",
        "courses/gavilano_pre_parcial.json",
        "courses/asymptotic_statistics_v7.json",
        "courses/saul_control_optimo.json",
    ]
    for c_rel in historical_courses:
        p = Path(c_rel)
        if p.is_file():
            data = json.loads(p.read_text(encoding="utf-8"))
            issues = []
            summary = linter.run(data, issues)
            assert summary["min_required_archetypes"] == 3
            assert summary["low_archetype_variety_competencies_count"] == 0


def test_forensic_v3_linter_upgrades():
    """Verify all forensic linter upgrades discovered during Estadística 3 Pre PC2 vs S9 V6 audit:
    1. Zero false positives on LaTeX commands/subscripts in UninterpolatedMathVariableLinter + string-concat collision detection.
    2. Rotating taxonomic prefix stripping + disconnected numeric rationales in DiagnosticRationaleAlignmentLinter.
    3. Bare-formula & cross-competency cloned misconception_warning + static example numbers in ScaffoldingHintsLinter.
    4. Corrupted probability key (>1.0), % probability bounds, degenerate 1.0000 collapse, and P(X=x) variance false-positive fix in DomainImpossibleDistractorLinter.
    5. Duplicate competencies & ID-category mismatch in ArchitectureDAGLinter.
    6. Raw scientific floats, raw asterisk multiplication, partial dummy-var substitution, and decorative parameter stuffing.
    """
    from standardized_audit_engine import (
        ArchitectureDAGLinter,
        BlindStringReplacementLinter,
        DomainImpossibleDistractorLinter,
        ScaffoldingHintsLinter,
    )

    # 1. UninterpolatedMathVariableLinter: LaTeX macros/subscripts clean vs string-concat collisions caught
    math_issues = []
    math_sum = UninterpolatedMathVariableLinter().run(
        {
            "questions": [
                {
                    "id": "Q-CLEAN-LATEX",
                    "competency_id": "C-01",
                    "stem": "Sea $\\bar{Y}_{n_1} \\xrightarrow{p} \\mu$ con $\\text{Var}(Y) = \\sigma^2$ en $\\mathcal{F}$.",
                    "options": [{"content": "$\\hat{p} \\xrightarrow{d} N(0,1)$", "is_correct": True}],
                },
                {
                    "id": "Q-CONCAT-DERIV",
                    "competency_id": "C-29",
                    "stem": "Aplique método delta para $g(x)=7x^2+10x$.",
                    "hints": ["Derive primero $g(x)=7x^2+10x$ respecto a $x$ para obtener $g'(x)=27x+10$."],
                    "options": [{"content": "$1.25$", "is_correct": True}],
                },
                {
                    "id": "Q-CONCAT-EXP",
                    "competency_id": "C-39",
                    "stem": "Con $g(X)=4X^2+10X+3$ y media $12$, evalúe:",
                    "options": [
                        {"content": "$100$", "is_correct": True},
                        {"content": "$0.5$", "is_correct": False, "error_rationale": "Calcula $(412+10)^2$ o $146^{20.5}$ o $(12+63)/(263)$."},
                    ],
                },
            ]
        },
        math_issues,
    )
    assert "Q-CLEAN-LATEX" not in math_sum["uninterpolated_math_sample_items"]
    assert math_sum["string_concat_collision_items_count"] == 2
    assert set(math_sum["string_concat_collision_sample_items"]) == {"Q-CONCAT-DERIV", "Q-CONCAT-EXP"}

    # 2. DiagnosticRationaleAlignmentLinter: rotating prefixes stripped + disconnected numeric rationales
    prefixes = [
        "Error conceptual", "Confusión teórica", "Fallo de cálculo", "Desvío algebraico",
        "Aplicación incorrecta", "Sustitución inválida", "Desvío de operador", "Desliz analítico",
    ]
    diag_qs = []
    for i in range(16):
        p = prefixes[i % len(prefixes)]
        diag_qs.append({
            "id": f"Q-DIAG-{i}",
            "competency_id": "C-12",
            "options": [
                {"content": f"${100 + i}$", "is_correct": True},
                {"content": f"${200 + i}$", "is_correct": False, "error_rationale": f"{p}: Exige normalidad poblacional previa para la validez asintótica del estimador."},
                {"content": f"${300 + i}$", "is_correct": False, "error_rationale": f"{p}: Afirma que la convergencia en distribución implica convergencia casi segura."},
                {"content": f"${400 + i}$", "is_correct": False, "error_rationale": f"{p}: Sostiene que el parámetro poblacional es una variable aleatoria muestral."},
                {"content": f"${500 + i}$", "is_correct": False, "error_rationale": f"{p}: Confunde la cota de Chebyshev con la desigualdad de Markov en espacios métricos."},
            ],
        })
    diag_issues = []
    diag_sum = DiagnosticRationaleAlignmentLinter().run({"questions": diag_qs}, diag_issues)
    assert diag_sum["synthetic_prefix_rationales_pct"] == 100.0
    assert diag_sum["raw_normalized_uniqueness_pct"] > diag_sum["rationale_uniqueness_pct"] + 20.0
    assert diag_sum["rationale_uniqueness_pct"] < 15.0
    assert diag_sum["disconnected_numeric_rationale_items_count"] == 16

    # 3. ScaffoldingHintsLinter: bare-formula & cross-competency cloned misconception_warning + static example numbers
    scaf_qs = []
    for i in range(6):
        scaf_qs.append({
            "id": f"Q-SCAF-{i}",
            "competency_id": f"C-0{(i % 3) + 1}",
            "stem": f"Calcule la varianza combinada con varianzas muestrales ${14 + i}$ y ${62 + i}$.",
            "hints": ["P1", "P2", "P3"],
            "detailed_solution": "Paso 1.",
            "common_misconception_warning": "$\\mathrm{Sesgo}(\\hat{\\theta}_n)=\\theta-\\mathbb{E}[\\hat{\\theta}_n]$",
        })
    for i in range(3):
        scaf_qs.append({
            "id": f"Q-STATIC-EX-{i}",
            "competency_id": "Hab-12",
            "stem": f"Con varianzas ${20 + i}$ y ${40 + i}$, halle la varianza ponderada.",
            "hints": ["P1", "P2", "P3"],
            "detailed_solution": "Paso 1.",
            "misconception_warning": "promediar varianzas sin ponderar (1^2+3^2)/2=5 en lugar de usar pesos",
        })
    scaf_issues = []
    scaf_sum = ScaffoldingHintsLinter().run({"questions": scaf_qs}, scaf_issues)
    assert scaf_sum["bare_formula_misconception_count"] == 6
    assert scaf_sum["cloned_misconception_warning_count"] == 6
    assert scaf_sum["disconnected_warning_numbers_count"] == 3

    # 4. DomainImpossibleDistractorLinter: P(X=x) variance clean, Chebyshev key > 1.0 caught, % bounds caught, 1.0000 degenerate caught
    dom_issues = []
    dom_sum = DomainImpossibleDistractorLinter().run(
        {
            "questions": [
                {
                    "id": "Q-VAR-CLEAN",
                    "competency_id": "C-11",
                    "stem": "Con cuantías $P(X=x)$ dadas en la tabla, calcule la varianza $\\text{Var}(X)$.",
                    "options": [
                        {"content": "$38.00$", "is_correct": True},
                        {"content": "$12.50$", "is_correct": False},
                    ],
                },
                {
                    "id": "Q-CHEB-CORRUPT",
                    "competency_id": "C-02",
                    "stem": "Determine la cota de Chebyshev en probabilidad para $\\mathbb{P}(|X-\\mu|\\ge k)$.",
                    "options": [
                        {"content": "$1.6056$", "is_correct": True},
                        {"content": "$-0.6056$", "is_correct": False},
                    ],
                },
                {
                    "id": "Q-PCT-BOUNDS",
                    "competency_id": "H-01",
                    "stem": "Calcule la probabilidad del evento en porcentaje.",
                    "options": [
                        {"content": "$75\\%$", "is_correct": True},
                        {"content": "$-5\\%$", "is_correct": False},
                        {"content": "$131\\%$", "is_correct": False},
                    ],
                },
                {
                    "id": "Q-DEGEN-CDF",
                    "competency_id": "Hab-03",
                    "stem": "Evalúe la función de distribución $F_{X_{(1)}}(t)$ para los parámetros dados.",
                    "options": [
                        {"content": "$1.0000$", "is_correct": True},
                        {"content": "$0.2500$", "is_correct": False},
                    ],
                },
            ]
        },
        dom_issues,
    )
    assert "Q-VAR-CLEAN" not in dom_sum["domain_impossible_sample_items"]
    assert dom_sum["corrupted_prob_key_items_count"] == 1
    assert dom_sum["degenerate_prob_key_items_count"] == 1
    assert "Q-CHEB-CORRUPT" in dom_sum["domain_impossible_sample_items"]
    assert "Q-PCT-BOUNDS" in dom_sum["domain_impossible_sample_items"]

    # 5. ArchitectureDAGLinter: duplicate competencies & ID-category mismatch
    arch_issues = []
    arch_sum = ArchitectureDAGLinter().run(
        {
            "competencies": [
                {
                    "id": "C-01",
                    "name": "Definición de sesgo y estimador insesgado",
                    "description": "Cálculo del sesgo puntual $\\mathrm{Sesgo}(\\hat{\\theta})=\\mathbb{E}[\\hat{\\theta}]-\\theta$.",
                    "category": "Concept",
                    "prerequisites": [],
                },
                {
                    "id": "Hab-08",
                    "name": "Sesgo de un estimador puntual e insesgadez",
                    "description": "Determinación del sesgo $\\mathrm{Sesgo}(\\hat{\\theta})=\\mathbb{E}[\\hat{\\theta}]-\\theta$ de estimadores.",
                    "category": "Skill",
                    "prerequisites": ["C-01"],
                },
                {
                    "id": "Hab-04",
                    "name": "Convergencia en distribución",
                    "description": "Teorema central del límite.",
                    "category": "Concept",
                    "prerequisites": ["C-01"],
                },
            ],
            "questions": [
                {"id": f"Q-1-{i}", "competency_id": "C-01"} for i in range(4)
            ] + [
                {"id": f"Q-2-{i}", "competency_id": "Hab-08"} for i in range(4)
            ] + [
                {"id": f"Q-3-{i}", "competency_id": "Hab-04"} for i in range(4)
            ],
        },
        arch_issues,
    )
    assert arch_sum["duplicate_competency_pairs_count"] == 1
    assert arch_sum["id_category_mismatch_count"] == 1

    # 6. KaTeXFrontendErgonomicsLinter, BlindStringReplacementLinter & AntiGamingPsychometricLinter
    erg_issues = []
    erg_sum = KaTeXFrontendErgonomicsLinter().run(
        {
            "questions": [
                {
                    "id": "Q-SCI-AST",
                    "competency_id": "Hab-25",
                    "stem": "Con sesgo $-7.2e-05$ y varianza $500*0.73*0.27\\approx 98.55$.",
                    "options": [{"content": "$1.1e-04$", "is_correct": True}],
                }
            ]
        },
        erg_issues,
    )
    assert erg_sum["raw_scientific_float_items_count"] == 1
    assert erg_sum["raw_asterisk_math_items_count"] == 1

    blind_issues = []
    blind_sum = BlindStringReplacementLinter().run(
        {
            "questions": [
                {
                    "id": "Q-DUMMY-N",
                    "competency_id": "Hab-04",
                    "stem": "Sabemos que $a^{11} \\to 0$ cuando $n \\to \\infty$ y $\\frac{n-1}{3}\\sigma^2$.",
                    "options": [{"content": "$0$", "is_correct": True}],
                }
            ]
        },
        blind_issues,
    )
    assert blind_sum["partial_dummy_var_substitution_count"] == 1

    ag_issues = []
    ag_sum = AntiGamingPsychometricLinter().run(
        {
            "title": "Estadística 3",
            "competencies": [{"id": "C-08"}],
            "questions": [
                {
                    "id": "Q-STUFF-1",
                    "competency_id": "C-08",
                    "stem": "Sea una muestra (prueba 30, $n=28$) (no r=1/9) de variables i.i.d. con media 5, varianza 12 y covarianza 3.",
                    "options": [{"content": "$12$", "is_correct": True}],
                }
            ],
        },
        ag_issues,
    )
    assert ag_sum["decorative_param_stuffing_items_count"] == 1




