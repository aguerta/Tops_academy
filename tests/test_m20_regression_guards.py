"""Regression tests for M2.0 quality guards (open_symbolic, MS length symmetry,
run_platform M2.0 validation, and QA audit engine nested LaTeX & phantom numeric detection).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
C2C_DIR = ROOT_DIR / ".agents" / "skills" / "content-to-course"
QA_SCRIPTS_DIR = ROOT_DIR / ".agents" / "skills" / "course-qa-evaluator" / "scripts"

for p in (str(ROOT_DIR), str(C2C_DIR), str(QA_SCRIPTS_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

from check_templates import _check_digit_placeholder_concat  # noqa: E402
from engine.invariants import check_instance_invariants, validate_katex_syntax  # noqa: E402
from engine.template_diagnostics import get_canonical_invariant_key  # noqa: E402
import run_platform  # noqa: E402
from standardized_audit_engine import run_full_audit  # noqa: E402


def _base_open_symbolic_instance(rationale: str) -> dict:
    return {
        "stem": r"Resuelva $s r^{4/5} = n r$ para el estado estacionario $r^*$ usando `s` y `n`:",
        "correct_answer": {
            "expression": "(s/n)**5",
            "accepted_equivalents": ["s**5/n**5", "(s/n)^5"],
        },
        "symbolic_config": {
            "variables": ["s", "n"],
            "palette": ["/", "^", "(", ")"],
            "placeholder": "Ej: (s/n)^2",
        },
        "diagnostic_distractors": [
            {
                "expression": "(s/n)**(1/5)",
                "distractor_id": "D-Hab05-01",
                "error_rationale": rationale,
            }
        ],
        "hints": [
            "Iguala la tasa de ahorro efectiva con la línea de dilución $nr$.",
            "Divide ambos lados por $r^{4/5}$ para aislar $r^{1/5}$.",
            "Eleva ambos lados a la quinta potencia para despejar $r^*$ en función de $s$ y $n$.",
        ],
        "detailed_solution": (
            r"De $s r^{4/5} = n r$ se obtiene $r^{1/5} = s/n$, por lo que $r^* = (s/n)^5$."
        ),
    }


def test_open_symbolic_rejects_numeric_var_collision():
    inst = _base_open_symbolic_instance(
        r"Olvida invertir el exponente $1-4/5$ al despejar $r^*$ desde $r^{1-4/5}=s/n$."
    )
    ok, errs = check_instance_invariants(
        inst,
        "open_symbolic",
        variables={"k": 5, "a": "4/5", "s": 0.15, "n": 0.03},
    )
    assert not ok
    assert any("open_symbolic variable collision" in e for e in errs)
    assert get_canonical_invariant_key(errs[0]) == "open_symbolic variable collision: symbolic variable numerically bound in vars"


def test_open_symbolic_rejects_phantom_numeric_rationale_and_accepts_clean():
    bad = _base_open_symbolic_instance(
        r"Olvida invertir el exponente $1-4/5$ al despejar $r^*$ desde $r^{1-4/5}=0.15/0.03$."
    )
    ok_bad, errs_bad = check_instance_invariants(bad, "open_symbolic")
    assert not ok_bad
    assert any("Phantom numeric leak in open_symbolic" in e for e in errs_bad)
    assert (
        get_canonical_invariant_key(errs_bad[0])
        == "Phantom numeric leak in open_symbolic diagnostic_distractors.error_rationale"
    )

    good = _base_open_symbolic_instance(
        r"Olvida invertir el exponente $1-4/5$ al despejar $r^*$ desde $r^{1-4/5}=s/n$."
    )
    ok_good, errs_good = check_instance_invariants(
        good,
        "open_symbolic",
        variables={"k": 5, "a": "4/5"},
    )
    assert ok_good, f"Expected clean open_symbolic to pass, got: {errs_good}"


def test_ms_length_symmetry_guard():
    def _make_ms(true_texts: list[str], false_texts: list[str]) -> dict:
        opts = [
            {"content": t, "is_correct": True}
            for t in true_texts
        ] + [
            {
                "content": f,
                "is_correct": False,
                "distractor_id": f"D-TEST-0{i+1}",
                "error_rationale": "Confunde el supuesto de ahorro exógeno con una identidad contable fija.",
            }
            for i, f in enumerate(false_texts)
        ]
        return {
            "stem": r"Con $s=23\%$ exógena y $Y=105$, determine qué propiedades sostiene $\dot{K}=sY$:",
            "options": opts,
            "hints": [
                "Revisa si $s$ depende de la tasa de interés o si es un parámetro constante.",
                "Compara el flujo neto de inversión con la fracción ahorrada del producto.",
                "Verifica si la ecuación $\\dot{K}=sY$ impone depreciación nula o ahorro endógeno.",
            ],
            "detailed_solution": (
                r"En el modelo básico de Solow con $s$ constante, la inversión neta equivale a $sY$."
            ),
        }

    # Asymmetric: avg_true ~ 72, avg_false ~ 56 -> ratio ~ 1.29x > 1.15x (7 options: 3 true, 4 false)
    biased = _make_ms(
        [
            "La inversión neta agregada iguala exactamente la fracción constante del ingreso",
            "El capital se acumula de forma continua a tasa proporcional al producto total",
            "El producto per cápita crece mientras la inversión supere a la dilución total",
        ],
        [
            "El ahorro depende siempre de la tasa de interés real",
            "La depreciación debe ser cero para que exista equilibrio",
            "El consumo agregado equivale al producto total siempre",
            "La población decrece cuando el capital alcanza el nivel",
        ],
    )
    ok_biased, errs_biased = check_instance_invariants(biased, "multiple_select")
    assert not ok_biased
    assert any("MS length anti-giveaway violation" in e for e in errs_biased)

    # Balanced: avg_true ~ 64, avg_false ~ 62 -> ratio ~ 1.03x <= 1.15x (7 options: 3 true, 4 false)
    balanced = _make_ms(
        [
            "La inversión neta iguala una fracción constante del producto Y.",
            "El capital crece de manera continua en proporción directa a sY.",
            "La tasa de ahorro exógena s permanece fija a lo largo del tiempo.",
        ],
        [
            "La tasa de ahorro responde endógenamente a la tasa de interés.",
            "El equilibrio estacionario exige que la depreciación sea nula.",
            "La producción agregada ignora por completo el acervo de capital.",
            "El flujo de inversión neta excede siempre al producto total Y.",
        ],
    )
    ok_bal, errs_bal = check_instance_invariants(balanced, "multiple_select")
    assert ok_bal, f"Expected balanced MS to pass, got: {errs_bal}"


def test_run_platform_accepts_all_m20_types():
    all_types = [
        "multiple_choice_7_options",
        "multiple_select",
        "fill_in_the_blank",
        "open_symbolic",
        "proof_dag",
        "adversarial_break",
        "unstructured_model",
        "invariant_canvas",
        "concept_matching",
    ]
    m20_payloads = {
        "proof_dag": {"steps": [{"id": "S1", "content": "Paso 1"}], "edges": []},
        "adversarial_break": {"mode": "find_fallacy", "steps": [{"id": "S1", "content": "Paso 1"}]},
        "unstructured_model": {"phase1_variables": {}, "phase2_assumptions": {}, "phase3_formulation": {}},
        "invariant_canvas": {"mode": "cartesian", "x_range": [0, 10], "y_range": [0, 10], "invariants": []},
        "concept_matching": {"premises": [], "targets": [], "correct_pairs": {}},
    }
    sample_course = {
        "course_id": "test_m20_all",
        "title": "Test M2.0 All Types",
        "competencies": [{"id": "C-01", "name": "Test Comp"}],
        "questions": [
            {
                "id": f"Q-{i}",
                "competency_id": "C-01",
                "type": qtype,
                "stem": f"Stem {i}",
                **({qtype: m20_payloads[qtype]} if qtype in m20_payloads else {}),
            }
            for i, qtype in enumerate(all_types, start=1)
        ],
    }
    ok, res = run_platform.validate_platform_course(json.dumps(sample_course))
    assert ok, f"Expected all M2.0 types to be valid, got: {res}"

    for m20_type in m20_payloads:
        missing_payload_course = {
            "course_id": "test_m20_missing",
            "title": "Missing M20 Payload",
            "competencies": [{"id": "C-01", "name": "Test Comp"}],
            "questions": [{"id": "Q-1", "competency_id": "C-01", "type": m20_type, "stem": "Stem 1"}],
        }
        ok_m, err_m = run_platform.validate_platform_course(json.dumps(missing_payload_course))
        assert not ok_m and m20_type in str(err_m), (
            f"Expected missing '{m20_type}' payload to be rejected, got: {(ok_m, err_m)}"
        )

    for slug in ("solow_m20_v1", "solow_m20_v2"):
        course_path = ROOT_DIR / "courses" / f"{slug}.json"
        if course_path.is_file():
            ok_c, res_c = run_platform.validate_platform_course(course_path.read_text(encoding="utf-8"))
            assert ok_c, f"Expected {slug}.json to pass run_platform validation, got: {res_c}"


def test_qa_engine_nested_latex_no_false_positive_and_phantom_detection():
    synthetic = {
        "course_id": "test_nested_katex",
        "title": "Nested KaTeX & Phantom Numeric Check",
        "competencies": [{"id": "C-01", "name": "Estabilidad", "category": "Concept", "prerequisites": []}],
        "questions": [
            {
                "id": "Q-1",
                "competency_id": "C-01",
                "type": "open_symbolic",
                "difficulty": "medium",
                "bloom": "Analyze",
                "stem": r"Evalúe la estabilidad con $\frac{d\dot{k}}{dk} < 0$ y $\frac{\dot{L}}{L} = n$ en función de `s` y `n`:",
                "correct_answer": {"expression": "(s/n)**2"},
                "symbolic_config": {"variables": ["s", "n"]},
                "diagnostic_distractors": [
                    {
                        "expression": "(n/s)**2",
                        "error_rationale": r"Invierte la razón colocando $0.03$ en el numerador y $0.15$ en el denominador.",
                    }
                ],
                "hints": ["Pista 1 conceptual.", "Pista 2 procedimental.", "Pista 3 algebraica."],
                "detailed_solution": r"Como $\frac{d\dot{k}}{dk} < 0$, el equilibrio $r^* = (s/n)^2$ es estable.",
            }
        ],
    }
    res = run_full_audit(synthetic)
    uninterp = res["dimension_summaries"]["uninterpolated_math_variable_linter"]
    assert uninterp["uninterpolated_math_items_count"] == 0, f"Unexpected false positive on nested LaTeX: {uninterp}"

    phantom = res["dimension_summaries"]["phantom_numeric_rationale_linter"]
    assert phantom["phantom_numeric_items_count"] == 1
    assert "Q-1" in res["risk_clusters"]["phantom_numeric_rationale"]

    v2_path = ROOT_DIR / "courses" / "solow_m20_v2.json"
    if v2_path.is_file():
        v2_res = run_full_audit(json.loads(v2_path.read_text(encoding="utf-8")))
        assert v2_res["dimension_summaries"]["uninterpolated_math_variable_linter"]["uninterpolated_math_items_count"] == 0
        assert v2_res["dimension_summaries"]["phantom_numeric_rationale_linter"]["phantom_numeric_items_count"] >= 4
        assert "Q-Hab05-241" in v2_res["risk_clusters"]["phantom_numeric_rationale"]
        assert "Q-Hab06-271" in v2_res["risk_clusters"]["phantom_numeric_rationale"]


def test_katex_rejects_python_pow_in_math_allows_markdown_bold():
    errs_bad = validate_katex_syntax(r"Resulta $r^*=(s/n)**5$ exacto.", "detailed_solution")
    assert any("[TPL-KATEX-SYMPY-LEAK]" in e for e in errs_bad)
    assert get_canonical_invariant_key(errs_bad[0]) == "[TPL-KATEX-SYMPY-LEAK] Raw SymPy syntax leaked inside KaTeX math"

    errs_good = validate_katex_syntax(r"**Paso 1:** Resulta $r^*=(s/n)^{5}$ exacto.", "detailed_solution")
    assert errs_good == [], f"Expected valid LaTeX + Markdown bold to pass, got: {errs_good}"


def test_tautological_self_identity_rejected_in_solution():
    errs_bad = validate_katex_syntax(r"Evaluando: $0.11 r^{-0.65}=0.11 r^{-0.65}$ en equilibrio.", "detailed_solution")
    assert any("[TPL-TAUTOLOGICAL-IDENTITY]" in e for e in errs_bad)
    assert get_canonical_invariant_key(errs_bad[0]) == "[TPL-TAUTOLOGICAL-IDENTITY] Redundant self-identity in solution/hints"

    errs_neq = validate_katex_syntax(r"Verifique que $0.11 r^{-0.65} \neq 0$ cuando $1=1$.", "detailed_solution")
    assert not any("[TPL-TAUTOLOGICAL-IDENTITY]" in e for e in errs_neq)


def test_digit_placeholder_concat_rejected_in_template():
    bad_tpl = {
        "id": "T-C01-01",
        "stem": r"La productividad es $2@c@k^{-1/2}$.",
        "stem_variants": [r"La productividad marginal vale $2@c@k^{-1/2}$."],
        "hints": ["Calcule $f'(k)$.", "Evalúe en @x@.", "Multiplique por 2."],
        "solution": r"El resultado es $2@c@k^{-1/2}$.",
        "generate_py": "def g(r):\n return {'vars': {'c': 1, 'x': 2}, 'correct': '2'}",
    }
    hits = _check_digit_placeholder_concat(bad_tpl)
    assert hits, "Expected 2@c@ concatenation to be flagged"
    assert any("@c@" in tok for _, tok in hits)

    bad_pair = {"stem": r"Producto $@a@@b@$.", "generate_py": "def g(r):\n return {}"}
    assert _check_digit_placeholder_concat(bad_pair)

    good_tpl = {
        "stem": r"La productividad es $2 \cdot @c@ k^{-1/2}$.",
        "hints": ["Derive.", "Sustituya.", "Simplifique."],
        "solution": r"El coeficiente es $@coef@$.",
        "generate_py": "def g(r):\n return {'vars': {'c': 1, 'coef': 2}, 'correct': '2'}",
    }
    assert _check_digit_placeholder_concat(good_tpl) == []


def test_qa_engine_detects_v3_pow_tautology_and_no_cross_category_dup():
    v3_path = ROOT_DIR / "courses" / "solow_m20_v3.json"
    if not v3_path.is_file():
        return
    v3_res = run_full_audit(json.loads(v3_path.read_text(encoding="utf-8")))
    assert "Q-Hab05-241" in v3_res["risk_clusters"]["sympy_in_katex"]
    assert "Q-Hab10-475" in v3_res["risk_clusters"]["katex_ergonomics"]
    assert not any(
        "Hab-04" in iss["message"] and "C-08" in iss["message"]
        for iss in v3_res["all_issues"]
        if iss["linter"] == "architecture_dag_linter"
    )
    assert v3_res["dimension_summaries"]["zpd_progression_linter"]["bloom_weighted_index"] > 3.5


def test_sympy_in_katex_segments_bold_display_and_bidual_superscripts():
    """SYMPY_IN_KATEX parses math segments: ignores Markdown **bold** between $...$,
    allows bidual superscripts like $f^{**}(x)$, and catches $$2 * x + 1$$."""
    # 1) Markdown bold between two inline math spans must NOT trigger in invariants or QA engine
    bold_between = r"Sea $x > 0$ el valor **óptimo** cuando $y = 1$."
    assert validate_katex_syntax(bold_between, "stem") == []

    # 2) Valid bidual superscript $f^{**}(x)$ / $V^{**}$ must NOT trigger
    bidual = r"El bidual $V^{**}$ y la biconjugada $f^{**}(x)$ coinciden con $f(x)$."
    assert validate_katex_syntax(bidual, "detailed_solution") == []

    # 3) Display math $$2 * x + 1$$ MUST trigger both engine invariants and QA linter
    disp_bad = r"Calcula $$2 * x + 1$$ en el punto óptimo."
    assert any("[TPL-KATEX-SYMPY-LEAK]" in e for e in validate_katex_syntax(disp_bad, "stem"))

    synthetic = {
        "course_id": "test_katex_segments",
        "title": "KaTeX Segment Boundary Regression",
        "competencies": [{"id": "C-01", "name": "Dualidad", "category": "Concept", "prerequisites": []}],
        "questions": [
            {
                "id": "Q-OK-1",
                "competency_id": "C-01",
                "type": "multiple_choice_7_options",
                "difficulty": "medium",
                "bloom": "Analyze",
                "stem": bold_between,
                "options": ["$1$", "$2$", "$3$", "$4$", "$5$", "$6$", "$7$"],
                "correct_answer": "$1$",
                "hints": ["P1.", "P2.", "P3."],
                "detailed_solution": bidual,
            },
            {
                "id": "Q-BAD-DISP",
                "competency_id": "C-01",
                "type": "multiple_choice_7_options",
                "difficulty": "medium",
                "bloom": "Apply",
                "stem": disp_bad,
                "options": ["$1$", "$2$", "$3$", "$4$", "$5$", "$6$", "$7$"],
                "correct_answer": "$1$",
                "hints": ["P1.", "P2.", "P3."],
                "detailed_solution": "Sustitución directa.",
            },
        ],
    }
    res = run_full_audit(synthetic)
    sympy_cluster = res["risk_clusters"].get("sympy_in_katex", [])
    assert "Q-OK-1" not in sympy_cluster
    assert "Q-BAD-DISP" in sympy_cluster

