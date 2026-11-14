import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

import compile_cta  # noqa: E402


def test_cta_d1_omitted_step_not_truncated_and_explicit():
    """Reproduces the exact Hab-01 screenshot case and ensures full specificity."""
    raw = (
        "CTA-D1 violation: Competencias tipo Skill con distractores insuficientes "
        "con omitted_step (<2): Hab-01 (línea 61) [0 con omitted_step], "
        "Hab-02 (línea 120) [1 con omitted_step] (mínimo 2 requerido)."
    )
    rendered = compile_cta.render_compact_cta_errors(
        [raw],
        data_filename="part_05_data.py",
        consolidated=True,
        write_pack=False,
    )
    assert "con omi " not in rendered
    assert not rendered.endswith("con omi")
    assert "[CTA-D1]" in rendered
    assert "omitted_step (<2)" in rendered
    assert "Hab-01" in rendered and "Hab-02" in rendered
    assert "Acción:" in rendered


def test_all_cta_error_categories_preserve_specific_context():
    """Every error family emitted by check_cta/compile_cta keeps IDs, fields, and actionable cause."""
    cases = [
        (
            "CTA-D1 violation: Competency 'C-01' (línea 12) has 2 distractors (minimum 3 required).",
            "CTA-D1",
            ["C-01", "2 distractors", "minimum 3 required"],
        ),
        (
            "CTA-D1 violation: Skill 'Hab-03' (línea 90) has 4 distractors (minimum 6 required).",
            "CTA-D1",
            ["Hab-03", "4 distractors", "minimum 6 required"],
        ),
        (
            "CTA-D2 violation: Duplicate distractor ids found within competency part: 'D-H01-01' (líneas 14, 22), 'D-H01-02' (líneas 30, 41) (2 ocurrencias).",
            "CTA-D2",
            ["D-H01-01", "D-H01-02", "líneas 14, 22"],
        ),
        (
            "CTA-D2 violation in distractor 'D-C02-03' (línea 44): both wrong_belief and omitted_step are null/empty.",
            "CTA-D2",
            ["D-C02-03", "wrong_belief", "omitted_step"],
        ),
        (
            "CTA-DISTRACTOR violation: Distractor 'D-H02-01' (línea 80) manifestation '$x=2$' is identical to correct_belief.",
            "CTA-DISTRACTOR",
            ["D-H02-01", "$x=2$", "correct_belief"],
        ),
        (
            "[CTA-ASSUMPTIONS-MISSING] [Línea 50] Competency 'Hab-01' (skill) requires at least 1 valid assumption.",
            "CTA-ASSUMPTIONS-MISSING",
            ["Hab-01", "skill", "assumption"],
        ),
        (
            "[CTA-DOCS] [Línea 15] Competencia 'C-01': doc='no_existe.pdf' no existe en pre_cta_manifest.json. Documentos disponibles: sesion_01.pdf, sesion_02.pdf.",
            "CTA-DOCS",
            ["C-01", "no_existe.pdf", "sesion_01.pdf"],
        ),
        (
            "[CTA-EV] [Línea 18] Distractor 'D-C01-01': doc='sesion_01.pdf' cita page=99 fuera del rango de páginas PDF válidas 1..12 en pre_cta_manifest.json.",
            "CTA-EV",
            ["D-C01-01", "sesion_01.pdf", "page=99", "1..12"],
        ),
        (
            "Too many root competencies (5/12 = 41.7%). Maximum allowed root ratio is 20% (max 2 roots for 12 competencies). Root competencies found: C-01, C-02, H-01, H-02, Hab-01.",
            "CTA-DAG",
            ["5/12", "20%", "C-01", "Hab-01"],
        ),
        (
            "Cycle detected in prerequisites: H-01 -> H-02 -> H-01",
            "CTA-DAG",
            ["H-01 -> H-02 -> H-01"],
        ),
        (
            "[KATEX-PROSE-OVERFLOW] In competency 'H-01' description_latex: \\text{Este texto descriptivo supera ampliamente el limite...} block exceeds 45 chars (67).",
            "KATEX-PROSE-OVERFLOW",
            ["H-01", "description_latex", "67"],
        ),
        (
            "Competency 'Hab-01' schema violation at [distractors -> 0 -> remediation_hint] (línea 64): '' is too short",
            "CTA-SCHEMA",
            ["Hab-01", "distractors -> 0 -> remediation_hint", "too short"],
        ),
        (
            "[CTA-TUPLE-STRUCTURE] [compile_cta] Tupla de competencia en índice 2 tiene 4 elementos (se requieren al menos 6).",
            "CTA-STRUCTURE",
            ["índice 2", "4 elementos"],
        ),
    ]

    for raw, expected_rule, required_tokens in cases:
        _, short_rule, cause, action = compile_cta.categorize_cta_error(raw)
        assert short_rule == expected_rule, f"Expected {expected_rule} for {raw}, got {short_rule}"
        assert action.strip(), f"Empty action for {raw}"
        for tok in required_tokens:
            assert tok in cause, f"Lost token {tok!r} in cause: {cause!r}"


def test_long_aggregated_error_preserved_up_to_700_chars():
    """Aggregated error details up to 700 chars are preserved without truncation."""
    items = ", ".join(f"Hab-{i:02d} (línea {i * 10}) [0 con omitted_step]" for i in range(1, 14))
    raw = f"CTA-D1 violation: Competencias tipo Skill con distractores insuficientes con omitted_step (<2): {items} (mínimo 2 requerido)."
    assert 400 < len(raw) < 700
    _, short_rule, cause, _ = compile_cta.categorize_cta_error(raw)
    assert short_rule == "CTA-D1"
    assert not cause.endswith("...")
    assert "Hab-13" in cause
