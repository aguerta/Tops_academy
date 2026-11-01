"""Unit tests for the 4 new deterministic audit linters added via /learn:
1. ClonedDistractorValueLinter
2. ParentheticalTelltaleLinter
3. ArchetypeEntropyLinter
4. UninterpolatedMathVariableLinter
"""
import sys
from pathlib import Path
import pytest

_c2c_dir = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
if str(_c2c_dir) not in sys.path:
    sys.path.insert(0, str(_c2c_dir))

_engine_dir = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "course-qa-evaluator" / "scripts"
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
    # 20 questions with identical structural skeleton
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
    assert len(issues) == 1
    assert issues[0].severity == "warning"


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


