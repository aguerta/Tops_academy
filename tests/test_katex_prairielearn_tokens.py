"""Tests for orthogonal PrairieLearn @var@ tokens, KaTeX sanitization, full question-type coverage, and anti-placeholder invariants."""

import sys
from pathlib import Path
from typing import Any, Dict

import pytest

# Ensure skills root is in sys.path
_skill_root = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

from engine.assemble import (
    assemble_question,
    compute_option_length_metrics,
    format_template_string,
    render_template,
    sanitize_katex_syntax,
)
from engine.invariants import (
    check_instance_invariants,
    check_unrendered_placeholders,
    validate_katex_syntax,
)


def test_prairielearn_tokens_in_nested_katex():
    """Verify @var@ and @var:fmt@ inside complex nested KaTeX preserve LaTeX braces completely."""
    template_str = r"$\operatorname{Est.Asy.Var}[b_{IV}] = \frac{@s2:.2f@ \cdot @szz@}{@szx@^2} \mathbf{I}_{@k_dim@}$"
    variables = {
        "s2": 1.254,
        "szz": 4.5,
        "szx": 2.0,
        "k_dim": 3,
    }

    rendered = render_template(template_str, variables)
    expected = r"$\operatorname{Est.Asy.Var}[b_{IV}] = \frac{1.25 \cdot 4.5}{2.0^2} \mathbf{I}_{3}$"
    assert rendered == expected

    # Verify KaTeX validation passes with zero errors
    errors = validate_katex_syntax(rendered, "test_context", variables=variables)
    assert errors == []


def test_single_letter_variables_alongside_latex_exponents_and_sums():
    """Verify single-letter variables @n@ and @k@ interpolate cleanly without corrupting LaTeX sums or superscripts."""
    template_str = r"Considerando $\sum_{i=1}^{n} X_i \in \mathbb{R}^{k}$ con tamaño muestral @n@ y dimensión @k@."
    variables = {"n": 100, "k": 5}

    rendered = render_template(template_str, variables)
    expected = r"Considerando $\sum_{i=1}^{n} X_i \in \mathbb{R}^{k}$ con tamaño muestral 100 y dimensión 5."
    assert rendered == expected

    # Invariants must recognize \sum_{i=1}^{n} and \mathbb{R}^{k} as valid LaTeX, not unrendered placeholders
    errors = validate_katex_syntax(rendered, "stem", variables=variables)
    assert errors == []


def test_fill_in_the_blank_variable_interpolation_and_invariants():
    """Verify fill_in_the_blank variable interpolation on value, canonical_algebraic, and equivalents."""
    template = {
        "id": "tpl_fib_01",
        "stem": "Calcule el valor crítico @param_name@ para @n@ observaciones.",
        "interaction_type": "fill_in_the_blank",
        "hints": [
            "Identifique los grados de libertad con @n@.",
            "Consulte la distribución correspondiente para @param_name@.",
            "Aproxime el resultado a dos decimales.",
        ],
        "detailed_solution": "Sustituyendo @n@ se obtiene el valor crítico @crit_val:.2f@.",
    }
    gen_result = {
        "correct": "@crit_val:.2f@",
        "canonical_algebraic": "@crit_val:.2f@ \\cdot \\sigma",
        "equivalents": ["@crit_val:.2f@", "@crit_val@"],
        "tolerance": 0.01,
        "vars": {
            "param_name": "t_{crit}",
            "n": 50,
            "crit_val": 2.0086,
        },
    }

    assembled = assemble_question(
        template=template,
        gen_result=gen_result,
        competency_id="Comp-FIB",
        question_index=1,
    )

    assert assembled["stem"] == "Calcule el valor crítico t_{crit} para 50 observaciones."
    ans = assembled["correct_answer"]
    assert ans["value"] == "2.01"
    assert ans["canonical_algebraic"] == "2.01 \\cdot \\sigma"
    assert "2.01" in ans["accepted_equivalents"]
    assert "2.0086" in ans["accepted_equivalents"]

    is_valid, errors = check_instance_invariants(assembled, "fill_in_the_blank", variables=gen_result["vars"])
    assert is_valid, f"Expected valid instance, got errors: {errors}"
    assert errors == []


def test_multiple_select_variable_interpolation_and_invariants():
    """Verify multiple_select option content and error rationale variable interpolation."""
    template = {
        "id": "tpl_ms_01",
        "stem": "Seleccione todas las propiedades válidas de @estimator@:",
        "interaction_type": "multiple_select",
        "hints": [
            "Considere las propiedades asintóticas de @estimator@.",
            "Recuerde el supuesto de varianza @var_type@.",
            "Evalúe la consistencia y normalidad asintótica.",
        ],
        "detailed_solution": "El estimador @estimator@ es consistente bajo @var_type@.",
    }
    gen_result = {
        "options": [
            {
                "content": "Es consistente bajo varianza @var_type@.",
                "is_correct": True,
                "error_rationale": None,
            },
            {
                "content": "Tiene sesgo de orden $O(@rate@)$.",
                "is_correct": False,
                "error_rationale": "El sesgo real de @estimator@ decae más rápido.",
            },
            {
                "content": "La varianza asintótica alcanza la cota inferior.",
                "is_correct": True,
                "error_rationale": None,
            },
            {
                "content": "No converge en probabilidad.",
                "is_correct": False,
                "error_rationale": "Sí converge bajo @var_type@.",
            },
        ],
        "vars": {
            "estimator": "\\hat{\\theta}_{IV}",
            "var_type": "heterocedástica",
            "rate": "1/n",
        },
    }

    assembled = assemble_question(
        template=template,
        gen_result=gen_result,
        competency_id="Comp-MS",
        question_index=1,
    )

    assert "\\hat{\\theta}_{IV}" in assembled["stem"]
    contents = [opt["content"] for opt in assembled["options"]]
    assert any("heterocedástica" in c for c in contents)
    assert any("1/n" in c for c in contents)

    rationales = [opt["error_rationale"] for opt in assembled["options"] if not opt["is_correct"]]
    assert any("\\hat{\\theta}_{IV}" in str(r) for r in rationales)
    assert any("heterocedástica" in str(r) for r in rationales)

    is_valid, errors = check_instance_invariants(assembled, "multiple_select", variables=gen_result["vars"])
    assert is_valid, f"Expected valid MS instance, got errors: {errors}"
    assert errors == []


def test_rejection_of_unresolved_prairielearn_tokens():
    """Verify rejection of unresolved @token@ or @token:fmt@ across all question fields."""
    unresolved_text = "El umbral crítico es @delta@ con tolerancia @tol:.4f@."
    errors = check_unrendered_placeholders(unresolved_text, "stem")
    assert len(errors) == 2
    assert any("@delta@" in err for err in errors)
    assert any("@tol:.4f@" in err for err in errors)

    # In FIB correct answer
    fib_instance = {
        "stem": "Determine el valor.",
        "hints": ["Pista 1", "Pista 2", "Pista 3"],
        "detailed_solution": "Solución.",
        "correct_answer": {
            "value": "@unresolved_val@",
            "canonical_algebraic": "@unresolved_val@",
            "accepted_equivalents": ["@unresolved_val@"],
            "tolerance": 0.01,
        },
    }
    is_valid, errors = check_instance_invariants(fib_instance, "fill_in_the_blank")
    assert not is_valid
    assert any("Unresolved PrairieLearn template token '@unresolved_val@'" in e for e in errors)


def test_rejection_of_uninterpolated_curly_placeholders():
    """Verify rejection of uninterpolated {delta} in prose or known variables while allowing valid LaTeX."""
    # 1. Bare {delta} in prose
    prose_with_var = "donde {delta} es el umbral de convergencia"
    errors = check_unrendered_placeholders(prose_with_var, "stem")
    assert len(errors) == 1
    assert "Unsubstituted template variable '{delta}'" in errors[0]

    # 2. Known variable {delta} in math span with variables dict
    math_with_var = "$f({delta}) = 0$"
    errors = check_unrendered_placeholders(math_with_var, "stem", variables={"delta": 0.05})
    assert len(errors) == 1
    assert "Unsubstituted template variable '{delta}'" in errors[0]

    # 3. Valid LaTeX constructs with 'delta', 'n', 'k' MUST NOT be rejected
    valid_latex_cases = [
        r"$\frac{delta}{n}$",
        r"$x_{delta}$",
        r"$\text{delta}$",
        r"$\mathbf{I}_{k}$",
        r"$\sum_{i=1}^{n} X_i$",
        r"$\begin{matrix} 1 & 0 \\ 0 & 1 \end{matrix}$",
        r"$\operatorname{plim}_{n \to \infty} \hat{\theta} = \theta$",
    ]
    for expr in valid_latex_cases:
        errs = check_unrendered_placeholders(expr, "test_context", variables={"delta": 0.05, "n": 100, "k": 3})
        assert errs == [], f"Legitimate LaTeX falsely rejected: '{expr}' -> {errs}"


def test_backward_compatibility_with_legacy_curly_templates():
    """Verify 100% backward compatibility for legacy templates authored with {var} and {var:fmt}."""
    legacy_template = "El parámetro estimado es {param_val:.3f} y el estado es {status_str}."
    variables = {"param_val": 3.14159, "status_str": "convergente"}

    formatted = format_template_string(legacy_template, variables)
    assert formatted == "El parámetro estimado es 3.142 y el estado es convergente."

    # Verify render_template alias
    assert render_template(legacy_template, variables) == formatted


def test_compute_option_length_metrics():
    """Verify compute_option_length_metrics returns correct diagnostic metrics and respects bounds."""
    correct = "Esta es la respuesta correcta detallada y justificada."
    distractors_balanced = [
        "Esta es la primera opción alternativa incorrecta.",
        "Esta es la segunda opción alternativa incorrecta.",
        "Esta es la tercera opción alternativa incorrecta.",
        "Esta es la cuarta opción alternativa incorrecta.",
        "Esta es la quinta opción alternativa incorrecta.",
        "Esta es la sexta opción alternativa incorrecta.",
    ]

    metrics = compute_option_length_metrics(correct, distractors_balanced, min_ratio=0.65, max_ratio=1.35)
    assert metrics["correct_len"] == len(correct)
    assert len(metrics["distractor_lens"]) == 6
    assert metrics["is_within_bounds"] is True
    assert "PASS" in metrics["summary_str"]
    assert 0.65 <= metrics["ratio"] <= 1.35

    # Test out-of-bounds (giveaway length)
    tiny_distractors = ["a", "b", "c"]
    fail_metrics = compute_option_length_metrics(correct, tiny_distractors, min_ratio=0.65, max_ratio=1.35)
    assert fail_metrics["is_within_bounds"] is False
    assert "FAIL" in fail_metrics["summary_str"]
    assert fail_metrics["ratio"] > 1.35


def test_instantiate_template_wires_variables_to_invariants(monkeypatch):
    """Verify instantiate_template passes variables to check_instance_invariants to reject leaked placeholders."""
    from engine.instantiate import instantiate_template

    # Template with unrendered placeholder @leaked_token@ in stem
    leaked_template = {
        "id": "tpl_leak_01",
        "stem": "Determine el valor de $\\beta$ cuando el umbral es @leaked_token@.",
        "interaction_type": "fill_in_the_blank",
        "hints": ["Pista 1", "Pista 2", "Pista 3"],
        "detailed_solution": "Solución paso a paso.",
        "generate_py": "def generate(seed):\n    return {'correct': '42', 'vars': {'dummy': 1}}\n",
    }

    # Should fail to generate required count because invariant rejects every attempt
    with pytest.raises(ValueError, match="could only generate 0/1 unique invariant instances"):
        instantiate_template(
            template=leaked_template,
            competency_id="Comp-Leak",
            target_count=1,
            max_attempts=3,
        )


def test_safe_numeric_formatting_coercion():
    """Verify numeric coercion in @var:fmt@ and {var:fmt} prevents runtime crashes on numeric strings or floats."""
    # 1. Float format on string, int, and float
    template_pl = "Valores: @val_str:.2f@, @val_int:.2f@, @val_flt:.2f@, @val_txt:.2f@"
    vars_pl = {
        "val_str": "2.50",
        "val_int": 5,
        "val_flt": 2.50,
        "val_txt": "no_num",
    }
    rendered_pl = render_template(template_pl, vars_pl)
    assert rendered_pl == "Valores: 2.50, 5.00, 2.50, no_num"

    # 2. Integer format on numeric string, float with zero fractional part, and int
    template_int = "Conteos: @cnt_str:03d@, @cnt_flt:03d@, @cnt_int:03d@"
    vars_int = {
        "cnt_str": "42",
        "cnt_flt": 42.0,
        "cnt_int": 42,
    }
    rendered_int = render_template(template_int, vars_int)
    assert rendered_int == "Conteos: 042, 042, 042"

    # 3. Legacy curly templates also benefit from safe formatting
    template_legacy = "Legacy: {val_str:.2f@} {val_str:.2f} {cnt_flt:03d}"
    vars_legacy = {"val_str": "3.14159", "cnt_flt": 7.0}
    rendered_legacy = render_template(template_legacy, vars_legacy)
    assert "3.14" in rendered_legacy
    assert "007" in rendered_legacy


def test_email_and_multiple_at_signs_not_false_flagged():
    """Verify email addresses or non-placeholder @ symbols on the same line are never corrupted or false-flagged."""
    # 1. Plain emails in prose
    email_text = "Para soporte contacte a soporte@tops.academy o admin@domain.com para más detalles."
    rendered = render_template(email_text, {"dummy": 1})
    assert rendered == email_text

    # No unrendered placeholder errors
    errors = check_unrendered_placeholders(email_text, "stem")
    assert errors == []

    # 2. Mixed: genuine leaked token alongside legitimate emails
    mixed_text = "Contacte a user@domain.com si el parámetro @unresolved_token@ no converge."
    mixed_errors = check_unrendered_placeholders(mixed_text, "stem")
    assert len(mixed_errors) == 1
    assert "@unresolved_token@" in mixed_errors[0]
    assert "user@domain.com" not in mixed_errors[0]


def test_econometrics_katex_with_single_letter_variables_adversarial():
    """Adversarial test: Greene econometrics LaTeX expressions with single-letter vars (d, n, k, a, b).
    
    Verifies ZERO false positives on legitimate LaTeX like \\xrightarrow{d}, \\operatorname{plim}_{n \\to \\infty},
    \\stackrel{a}{\\sim}, \\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}, \\mathbb{R}^{k}, \\mathcal{N}(0, \\sigma^2),
    S_{zz}, X'Z(Z'Z)^{-1}Z'X, {k}^*, x_{n}, \\frac{a}{b}, while reliably catching leaked prose '{d}', '{n}', '{delta}'.
    """
    econometrics_vars = {
        "d": 4,
        "n": 100,
        "k": 3,
        "a": 2,
        "b": 5,
        "p": 0.05,
    }

    # Legitimate complex econometrics formulas from Greene
    legitimate_latex_cases = [
        r"$\operatorname{plim}_{n \to \infty} \hat{\beta} = \beta$",
        r"$\operatorname*{plim}_{n \to \infty} b_{IV} = \beta$",
        r"$b_{IV} \xrightarrow{d} \mathcal{N}(0, \sigma^2)$",
        r"$b_{IV} \xrightarrow[n \to \infty]{d} \beta$",
        r"$\hat{\theta} \stackrel{a}{\sim} \mathcal{N}(\theta, \mathbf{V})$",
        r"$\mathbf{A} = \begin{pmatrix} a & b \\ c & d \end{pmatrix}$",
        r"$\mathbf{X} \in \mathbb{R}^{k}$",
        r"$\mathcal{N}(0, \sigma^2)$",
        r"$S_{zz} = \frac{1}{n} \sum_{i=1}^{n} z_i^2$",
        r"$P_Z = Z(Z'Z)^{-1}Z'$",
        r"${k}^* = \arg\max f(k)$",
        r"$x_{n} + x_ {n} + x^{n} + x^ {k}$",
        r"$\frac{a}{b} + \frac{a} {b} + \frac{d}{n} + \frac{d} {n}$",
        r"$\binom{n}{k} + \binom{n} {k}$",
        r"$\mathbf{I}_{k} + \mathbf{I}_{d}$",
    ]

    for expr in legitimate_latex_cases:
        errs = check_unrendered_placeholders(expr, "econometrics_stem", variables=econometrics_vars)
        assert errs == [], f"Legitimate econometrics LaTeX falsely rejected: '{expr}' -> {errs}"
        katex_errs = validate_katex_syntax(expr, "econometrics_stem", variables=econometrics_vars)
        assert katex_errs == [], f"validate_katex_syntax falsely rejected: '{expr}' -> {katex_errs}"

    # In contrast, genuine leaked placeholders in prose MUST be caught!
    leaked_prose_cases = [
        ("El modelo tiene dimensión {d} y muestra {n}.", ["{d}", "{n}"]),
        ("Verifique que la tolerancia cumpla <= {delta} en la iteración.", ["{delta}"]),
        ("Compare el parámetro {a} frente a {b} en el test.", ["{a}", "{b}"]),
    ]

    for prose, expected_tokens in leaked_prose_cases:
        errs = check_unrendered_placeholders(prose, "prose_stem", variables=econometrics_vars)
        assert len(errs) == len(expected_tokens), f"Failed to catch leaked tokens in '{prose}': got {errs}"
        for exp in expected_tokens:
            assert any(f"'{exp}'" in e for e in errs), f"Expected token {exp} not flagged in {errs}"


def test_fill_in_the_blank_accepted_equivalents_mixed_types():
    """Verify FIB accepted_equivalents with mixed scalar types ([2.5, '5/2', '@frac_str@']) are normalized and validated."""
    template = {
        "id": "tpl_fib_mixed",
        "stem": "Determine el valor estimado del parámetro $\\theta$:",
        "interaction_type": "fill_in_the_blank",
        "hints": [
            {"text": "Calcule el estimador puntual con @n@ observaciones."},
            "Aproxime el cociente con precisión.",
            "Exprese el resultado en forma decimal o fraccionaria.",
        ],
        "detailed_solution": "El estimador converge a @frac_str@ = 2.5.",
    }
    gen_result = {
        "correct": "2.5",
        "canonical_algebraic": "5/2",
        "accepted_equivalents": [2.5, "5/2", "@frac_str@"],
        "tolerance": 0.001,
        "vars": {
            "n": 50,
            "frac_str": "10/4",
        },
    }

    assembled = assemble_question(
        template=template,
        gen_result=gen_result,
        competency_id="Comp-FIB-Mixed",
        question_index=1,
    )

    ans = assembled["correct_answer"]
    assert ans["value"] == "2.5"
    assert "2.5" in ans["accepted_equivalents"]
    assert "5/2" in ans["accepted_equivalents"]
    assert "10/4" in ans["accepted_equivalents"]
    # All elements must be strings, without duplicates
    assert all(isinstance(eq, str) for eq in ans["accepted_equivalents"])
    assert len(ans["accepted_equivalents"]) == len(set(ans["accepted_equivalents"]))

    # Invariant validation passes
    is_valid, errors = check_instance_invariants(assembled, "fill_in_the_blank", variables=gen_result["vars"])
    assert is_valid, f"Unexpected invariant errors: {errors}"
    assert errors == []


def test_multiple_select_content_and_value_fallback():
    """Verify MS handles content/value/text fallback and dict hints seamlessly."""
    template = {
        "id": "tpl_ms_fallback",
        "stem": "Seleccione las propiedades verdaderas:",
        "interaction_type": "multiple_select",
        "hints": [
            {"text": "Considere la tasa de convergencia @rate@."},
            {"content": "Verifique la condición de rango con @k@ variables."},
            "Examine la matriz de varianzas asintóticas.",
        ],
        "detailed_solution": "Propiedades válidas bajo regularidad.",
    }
    gen_result = {
        "options": [
            {
                "content": "",
                "value": "El estimador es consistente a tasa @rate@.",
                "is_correct": True,
                "error_rationale": None,
            },
            {
                "content": None,
                "text": "La matriz tiene rango defectuoso de dimensión @k@.",
                "is_correct": False,
                "error_rationale": "El rango no es defectuoso bajo los supuestos.",
            },
            {
                "content": "La varianza asintótica es mínima.",
                "is_correct": True,
                "error_rationale": None,
            },
            {
                "content": "El sesgo asintótico no converge a cero.",
                "is_correct": False,
                "error_rationale": "El sesgo converge a cero a tasa @rate@.",
            },
        ],
        "vars": {
            "rate": "1/\\sqrt{n}",
            "k": 4,
        },
    }

    assembled = assemble_question(
        template=template,
        gen_result=gen_result,
        competency_id="Comp-MS-Fallback",
        question_index=1,
    )

    # Options correctly resolved from value and text fallback
    opt_contents = [opt["content"] for opt in assembled["options"]]
    assert any("tasa 1/\\sqrt{n}" in c for c in opt_contents)
    assert any("dimensión 4" in c for c in opt_contents)

    # Hints correctly resolved from dict text and content
    assert any("tasa de convergencia 1/\\sqrt{n}" in h for h in assembled["hints"])
    assert any("4 variables" in h for h in assembled["hints"])

    # Invariants pass
    is_valid, errors = check_instance_invariants(assembled, "multiple_select", variables=gen_result["vars"])
    assert is_valid, f"Unexpected invariant errors: {errors}"
    assert errors == []


def test_stem_variants_with_prairielearn_tokens():
    """Verify stem_variants (3-5 variants) work seamlessly with @var@ tokens in assemble_question and instantiate_template."""
    from engine.instantiate import instantiate_template

    template = {
        "id": "tpl_variants_01",
        "stem": "Stem por defecto con @n@ datos.",
        "stem_variants": [
            "Variante 1: Para una muestra de @n@ observaciones y dimensión @d@, calcule el estadístico.",
            "Variante 2: Considerando @n@ datos con dimensión @d@, determine el estimador.",
            "Variante 3: Con @n@ observaciones en dimensión @d@, halle el resultado.",
        ],
        "interaction_type": "multiple_choice_7_options",
        "hints": ["Pista 1", "Pista 2", "Pista 3"],
        "detailed_solution": "Solución detallada paso a paso.",
        "generate_py": (
            "def generate(rng):\n"
            "    n = rng.choice([100, 200, 300, 400, 500])\n"
            "    d = rng.choice([2, 3, 4, 5, 6])\n"
            "    val = n * d\n"
            "    distractors = [\n"
            "        {'value': f'Distractor {i} con {val + i * 10}', 'error_rationale': f'Error {i} por cálculo incorrecto'}\n"
            "        for i in range(1, 7)\n"
            "    ]\n"
            "    return {\n"
            "        'correct': f'Correcto con {val}',\n"
            "        'distractors': distractors,\n"
            "        'vars': {'n': n, 'd': d},\n"
            "    }\n"
        ),
    }

    # Generate 3 questions, verifying variant indexing and token interpolation
    questions = instantiate_template(
        template=template,
        competency_id="Comp-Variants",
        target_count=3,
        seed_offset=100,
    )

    assert len(questions) == 3
    for q in questions:
        stem = q["stem"]
        assert "@n@" not in stem
        assert "@d@" not in stem
        assert any(v in stem for v in ["Variante 1", "Variante 2", "Variante 3"])
        is_valid, errors = check_instance_invariants(q, "multiple_choice_7_options")
        assert is_valid, f"Variant instance invariant error: {errors}"

