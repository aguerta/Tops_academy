"""Unit tests for Stream 1A: Tier-0 Auto-Heal, Exact AST Line Locator, Modular Splicing, and Attempt State.

Validates:
1. Tier-0 auto-heal for unescaped / orphaned KaTeX commands in distractor & competency fields.
2. CtaDataLineLocator exact line ranges for competencies, distractors, and subfields.
3. Isolated repair packs (<part_id>_repair_pack.json) with error_count.
4. Stateful .check_attempts/compile_cta_<target_id>.json and pass_cta_<target_id>.json.
5. Dynamic official threshold directives (< 6 surgical edit_file vs >= 6 modular cta_fixes/rewrite).
6. Modular cta_fixes/<CID>.py splicing and resolution.
"""

from pathlib import Path
import json
import re
import sys
import tempfile
import pytest

# Ensure skill directory is in sys.path
_skill_dir = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "content-to-course"
if str(_skill_dir) not in sys.path:
    sys.path.insert(0, str(_skill_dir))

from compile_cta import (
    CtaDataLineLocator,
    compile_cta,
    render_compact_cta_errors,
    discover_cta_fix_files,
)
from cta_merge import (
    auto_wrap_bare_latex_in_cta_field,
    normalize_orphan_math,
    sanitize_competency_math,
)
from check_cta import check_cta_katex, validate_cta_rules, check_cta_part, RAW_LATEX_PATTERNS


# ==============================================================================
# 1. Tier-0 Auto-Heal Unit Tests
# ==============================================================================

def test_auto_wrap_bare_latex_pure_math():
    """Validates that strings containing purely math expressions without $ are wrapped in $...$."""
    raw1 = r"\lim_{n\to\infty} \frac{\sigma^2}{n} = 0"
    wrapped1 = auto_wrap_bare_latex_in_cta_field(raw1)
    assert wrapped1 == r"$\lim_{n\to\infty} \frac{\sigma^2}{n} = 0$"

    raw2 = r"\frac{\sigma^2}{n}"
    wrapped2 = auto_wrap_bare_latex_in_cta_field(raw2)
    assert wrapped2 == r"$\frac{\sigma^2}{n}$"

    # Trailing sentence punctuation
    raw3 = r"\lim_{n\to\infty} \frac{\sigma^2}{n} = 0."
    wrapped3 = auto_wrap_bare_latex_in_cta_field(raw3)
    assert wrapped3 == r"$\lim_{n\to\infty} \frac{\sigma^2}{n} = 0$."

    raw4 = r"\sqrt{n}(\bar{X}_n - \mu) \xrightarrow{d} \mathcal{N}(0, \sigma^2)"
    wrapped4 = auto_wrap_bare_latex_in_cta_field(raw4)
    assert wrapped4 == r"$\sqrt{n}(\bar{X}_n - \mu) \xrightarrow{d} \mathcal{N}(0, \sigma^2)$"


def test_auto_wrap_bare_latex_mixed_prose():
    """Validates that mixed prose with bare LaTeX commands has only the math expressions wrapped."""
    prose1 = r"El estimador converge porque \lim_{n\to\infty} \frac{\sigma^2}{n} = 0 en probabilidad."
    wrapped1 = auto_wrap_bare_latex_in_cta_field(prose1)
    assert r"$\lim_{n\to\infty} \frac{\sigma^2}{n} = 0$" in wrapped1
    assert "El estimador converge porque " in wrapped1
    assert " en probabilidad." in wrapped1

    prose2 = r"Confunde \sigma con la varianza \sigma^2 al calcular."
    wrapped2 = auto_wrap_bare_latex_in_cta_field(prose2)
    assert r"$\sigma$" in wrapped2
    assert r"$\sigma^2$" in wrapped2
    assert "Confunde " in wrapped2
    assert " con la varianza " in wrapped2

    # Already wrapped text should not be doubly wrapped
    already_valid = r"Dado $X \sim \mathcal{N}(0, 1)$, se tiene que $\mu = 0$."
    assert auto_wrap_bare_latex_in_cta_field(already_valid) == already_valid


def test_normalize_orphan_math_integration():
    """Validates that normalize_orphan_math applies auto_wrap_bare_latex_in_cta_field transparently."""
    text = r"Asume erróneamente que \lim_{n\to\infty} \frac{\sigma^2}{n} = 0 para todo caso."
    norm = normalize_orphan_math(text)
    assert "$" in norm
    # Check that check_cta_katex validates this field with 0 errors
    sample_comp = {
        "competencies": [{
            "id": "H-01",
            "name": "Propiedad asintótica",
            "description_latex": "Definición formal",
            "distractors": [{
                "id": "D-H01-01",
                "wrong_belief": norm,
                "correct_belief": "La varianza debe ser finita",
                "manifestation": "$0$",
                "remediation_hint": "Verificar condiciones",
            }]
        }]
    }
    errs = check_cta_katex(sample_comp)
    assert len(errs) == 0, f"Expected 0 KaTeX errors, got: {errs}"


# ==============================================================================
# 2. CtaDataLineLocator AST Line Resolution Tests
# ==============================================================================

SAMPLE_CTA_SOURCE = '''# cta_data.py
COURSE_ID = "asymptotic_test"
COURSE_TITLE = "Estadística Asintótica"

COMPETENCIES = [
    (
        "fact",
        "H-01",
        "Consistencia del estimador",
        r"Definición formal de consistencia con $\\text{plim}_{n \\to \\infty} \\hat{\\theta}_n = \\theta$.",
        "Remember",
        "asymptotic_notes.pdf",
        1,
        [],
        [
            (
                "Error en definición de consistencia",
                r"Confunde consistencia con insesgadez finita.",
                r"Consistencia requiere convergencia en probabilidad.",
                r"Afirma que todo estimador insesgado es consistente.",
                r"Revisar la definición de convergencia en probabilidad.",
                None,
            ),
            (
                "Error de varianza en límite",
                r"\\lim_{n\\to\\infty} \\frac{\\sigma^2}{n} = 0",
                r"La varianza asintótica se evalúa bajo $\\sqrt{n}$.",
                r"Usa varianza muestral sin escalar por $n$.",
                r"Aplicar el Teorema del Límite Central.",
                None,
            ),
            (
                "Tercer distractor H-01",
                r"Error conceptual 3",
                r"Verdad conceptual 3",
                r"Manifestación 3",
                r"Pista 3",
                None,
            ),
        ],
    ),
    (
        "skill",
        "Hab-01",
        "Cálculo de distribución asintótica",
        r"Cálculo analítico de varianza asintótica.",
        "Apply",
        "asymptotic_notes.pdf",
        2,
        ["H-01"],
        [
            ("D1", "wb1", "cb1", "man1", "rh1", "os1"),
            ("D2", "wb2", "cb2", "man2", "rh2", "os2"),
            ("D3", "wb3", "cb3", "man3", "rh3", None),
            ("D4", "wb4", "cb4", "man4", "rh4", None),
            ("D5", "wb5", "cb5", "man5", "rh5", None),
            ("D6", "wb6", "cb6", "man6", "rh6", None),
        ],
    ),
]
'''

def test_cta_data_line_locator_distractor_ranges():
    """Validates that CtaDataLineLocator indexes distractor tuples independently from competency lines."""
    locator = CtaDataLineLocator(SAMPLE_CTA_SOURCE)

    # Competency range
    c_rng = locator.get_range("H-01")
    assert c_rng is not None
    assert c_rng[0] >= 6  # Tuple opening starts at line 6 or 7

    # Distractor 1 and 2 ranges must NOT equal competency opening line
    d1_rng = locator.get_range("D-H01-01")
    d2_rng = locator.get_range("D-H01-02")
    assert d1_rng is not None
    assert d2_rng is not None
    assert d1_rng[0] > c_rng[0]
    assert d2_rng[0] > d1_rng[0]

    # Subfield line for wrong_belief of D-H01-02
    wb_rng = locator.get_range("D-H01-02", "wrong_belief")
    assert wb_rng is not None
    assert wb_rng[0] >= d2_rng[0]

    # Test resolve_error_location
    err = "Distractor 'D-H01-02' en 'wrong_belief' contiene comandos LaTeX sin delimitar por '$...$'"
    sl, el, snip = locator.resolve_error_location(err)
    assert sl == wb_rng[0]
    assert "lim" in snip or "sigma" in snip


# ==============================================================================
# 3. End-to-End Compilation with Tier-0 Auto-Heal & .check_attempts State
# ==============================================================================

def test_compile_cta_tier0_autoheal_and_pass_file(tmp_path):
    """Verifies that unescaped LaTeX in distractors is healed in Tier 0 and generates pass_cta_<target_id>.json."""
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True)

    manifest_file = work_dir / "pre_cta_manifest.json"
    manifest_file.write_text(json.dumps({
        "course_id": "asymptotic_test",
        "title": "Estadística Asintótica",
        "files": [{
            "doc": "asymptotic_notes.pdf",
            "name": "asymptotic_notes.pdf",
            "valid_page_range": [1, 10],
            "total_pages": 10,
        }],
    }), encoding="utf-8")

    cta_py_file = work_dir / "cta_data.py"
    cta_py_file.write_text(SAMPLE_CTA_SOURCE, encoding="utf-8")

    valid, cta_dict, errors, elapsed = compile_cta(
        cta_data_path=cta_py_file,
        output_dir=work_dir,
        manifest_path=manifest_file,
    )

    assert valid is True, f"Compilation failed with errors: {errors}"
    assert len(errors) == 0

    # Verify that in cta.json, the distractor with bare latex was healed to $...$
    d2 = cta_dict["competencies"][0]["distractors"][1]
    assert "$" in d2["wrong_belief"], f"Distractor wrong_belief not auto-wrapped: {d2['wrong_belief']}"

    # Verify pass_cta_cta_data.json was created
    pass_file = work_dir / ".check_attempts" / "pass_cta_cta_data.json"
    assert pass_file.is_file()
    pass_obj = json.loads(pass_file.read_text(encoding="utf-8"))
    assert pass_obj["status"] == "PASS"
    assert pass_obj["target_id"] == "cta_data"
    assert pass_obj["competency_count"] == 2

    # Verify compile_cta_cta_data.json does not exist
    att_file = work_dir / ".check_attempts" / "compile_cta_cta_data.json"
    assert not att_file.is_file()


# ==============================================================================
# 4. Error Persistence, Isolation and Threshold Directives
# ==============================================================================

BROKEN_CTA_SOURCE_3_ERRORS = '''# part_01_data.py
COURSE_ID = "asymptotic_test"
COURSE_TITLE = "Estadística Asintótica"

COMPETENCIES = [
    (
        "fact",
        "H-01",
        "Competencia con pocos distractores",
        r"Definición matemática.",
        "Remember",
        "asymptotic_notes.pdf",
        1,
        [],
        [
            ("D1", "wb1", "cb1", "man1", "rh1", None),
        ],  # Only 1 distractor (CTA-D1 violation: minimum 3)
    ),
    (
        "concept",
        "C-01",
        "Segunda competencia",
        r"Concepto formal.",
        "Understand",
        "asymptotic_notes.pdf",
        20,  # Page 20 is out of valid range 1..10 (CTA-EV violation)
        [],
        [
            ("D1", None, "cb1", "man1", "rh1", None),  # Empty wrong_belief & omitted_step (CTA-D2 violation)
            ("D2", "wb2", "cb2", "man2", "rh2", None),
            ("D3", "wb3", "cb3", "man3", "rh3", None),
        ],
    ),
]
'''

def test_compile_cta_failure_state_and_isolation(tmp_path):
    """Verifies isolated repair pack, error_count in .check_attempts, and dynamic < 6 threshold directive."""
    work_dir = tmp_path / "work"
    parts_dir = work_dir / "cta_parts"
    parts_dir.mkdir(parents=True)

    manifest_file = work_dir / "pre_cta_manifest.json"
    manifest_file.write_text(json.dumps({
        "course_id": "asymptotic_test",
        "files": [{
            "doc": "asymptotic_notes.pdf",
            "name": "asymptotic_notes.pdf",
            "valid_page_range": [1, 10],
            "total_pages": 10,
        }],
    }), encoding="utf-8")

    part_file = parts_dir / "part_01_data.py"
    part_file.write_text(BROKEN_CTA_SOURCE_3_ERRORS, encoding="utf-8")

    valid, cta_dict, errors, elapsed = compile_cta(
        cta_data_path=part_file,
        output_dir=parts_dir,
        manifest_path=manifest_file,
        output_json_name="part_01.json",
        is_part=True,
        allow_degrade=False,
    )

    assert valid is False
    assert len(errors) > 0

    # 1. Verify .check_attempts/compile_cta_part_01.json
    att_file = parts_dir / ".check_attempts" / "compile_cta_part_01.json"
    assert att_file.is_file()
    state = json.loads(att_file.read_text(encoding="utf-8"))
    assert state["distinct_compiles"] == 1
    assert state["error_count"] >= 1
    assert "last_source_sha256" in state
    assert state["has_syntax_error"] is False

    # 2. Verify pass_cta_part_01.json does NOT exist
    pass_file = parts_dir / ".check_attempts" / "pass_cta_part_01.json"
    assert not pass_file.is_file()

    # 3. Verify isolated repair pack: part_01_repair_pack.json
    pack_msg = render_compact_cta_errors(
        errors,
        data_filename=str(part_file),
        consolidated=True,
        write_pack=True,
        work_dir=work_dir,
    )

    repair_pack_path = parts_dir / "part_01_repair_pack.json"
    assert repair_pack_path.is_file()
    pack_data = json.loads(repair_pack_path.read_text(encoding="utf-8"))
    assert "error_count" in pack_data
    assert pack_data["error_count"] == len(set(errors))

    # 4. Verify threshold directive: 1..5 errors -> [UMBRAL OFICIAL < 6 ERRORES]
    assert "[UMBRAL OFICIAL < 6 ERRORES" in pack_msg
    assert "replace_file_content" in pack_msg
    assert "PROHIBIDO reescribir todo el archivo with write_file" in pack_msg or "PROHIBIDO reescribir todo el archivo con write_file" in pack_msg


def test_render_compact_errors_threshold_ge_6():
    """Verifies that >= 6 errors emit the modular cta_fixes / full rewrite directive."""
    errors = [f"Error fake {i}" for i in range(1, 8)]  # 7 errors
    msg = render_compact_cta_errors(errors, data_filename="cta_data.py", consolidated=True, write_pack=False)
    assert "[UMBRAL OFICIAL >= 6 ERRORES (7)]" in msg
    assert "cta_fixes/<CID>.py" in msg


# ==============================================================================
# 5. Modular cta_fixes/<CID>.py Splicing Tests
# ==============================================================================

FIXED_H01_OVERRIDE = '''# cta_fixes/H-01.py
COMPETENCY = (
    "fact",
    "H-01",
    "Competencia corregida modularmente",
    r"Definición matemática formal corregida con KaTeX $\\theta = 0$.",
    "Remember",
    "asymptotic_notes.pdf",
    1,
    [],
    [
        ("D1", "wb1 corregido", "cb1", "man1", "rh1", None),
        ("D2", "wb2 corregido", "cb2", "man2", "rh2", None),
        ("D3", "wb3 corregido", "cb3", "man3", "rh3", None),
    ],
)
'''

def test_cta_fixes_modular_splice(tmp_path):
    """Verifies that cta_fixes/<CID>.py replaces the corresponding broken competency in memory."""
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True)

    manifest_file = work_dir / "pre_cta_manifest.json"
    manifest_file.write_text(json.dumps({
        "course_id": "asymptotic_test",
        "files": [{
            "doc": "asymptotic_notes.pdf",
            "name": "asymptotic_notes.pdf",
            "valid_page_range": [1, 10],
            "total_pages": 10,
        }],
    }), encoding="utf-8")

    # Initial cta_data.py has H-01 with only 1 distractor (failing CTA-D1)
    broken_source = '''# cta_data.py
COURSE_ID = "asymptotic_test"
COMPETENCIES = [
    (
        "fact",
        "H-01",
        "H-01 rota con 1 distractor",
        "desc",
        "Remember",
        "asymptotic_notes.pdf",
        1,
        [],
        [("D1", "wb1", "cb1", "man1", "rh1", None)],
    )
]
'''
    cta_file = work_dir / "cta_data.py"
    cta_file.write_text(broken_source, encoding="utf-8")

    # 1. Verify it fails without fix
    valid, _, errors, _ = compile_cta(cta_data_path=cta_file, output_dir=work_dir, manifest_path=manifest_file, allow_degrade=False)
    assert valid is False
    assert any("CTA-D1" in e for e in errors)

    # 2. Write fix into cta_fixes/H-01.py
    fixes_dir = work_dir / "cta_fixes"
    fixes_dir.mkdir(parents=True)
    fix_file = fixes_dir / "H-01.py"
    fix_file.write_text(FIXED_H01_OVERRIDE, encoding="utf-8")

    # Verify discover_cta_fix_files detects it
    discovered = discover_cta_fix_files(work_dir, cta_file)
    assert len(discovered) == 1
    assert discovered[0].name == "H-01.py"

    # 3. Recompile: should splice fix in memory and PASS
    valid2, cta_dict2, errors2, _ = compile_cta(cta_data_path=cta_file, output_dir=work_dir, manifest_path=manifest_file)
    assert valid2 is True, f"Expected PASS with spliced fix, got: {errors2}"
    assert len(cta_dict2["competencies"]) == 1
    assert len(cta_dict2["competencies"][0]["distractors"]) == 3
    assert cta_dict2["competencies"][0]["name"] == "Competencia corregida modularmente"

    # 4. Verify pass_cta_cta_data.json is written
    pass_file = work_dir / ".check_attempts" / "pass_cta_cta_data.json"
    assert pass_file.is_file()


# ==============================================================================
# 6. Hardening Tests: Asymptotic Statistics v5 Real Patterns & SyntaxError Flag
# ==============================================================================

ASYMPTOTIC_V5_CTA_SOURCE = r'''# cta_data.py
COURSE_ID = "asyntotic_estatistics_v5"
COURSE_TITLE = "Estadística Asintótica Avanzada"

COMPETENCIES = [
    (
        "fact",
        "H-03",
        "Límites y consistencia de varianzas",
        r"Propiedades asintóticas de varianza muestral.",
        "Remember",
        "asymptotic_notes.pdf",
        1,
        [],
        [
            ("D-H03-01", "wb1", "cb1", "man1", "rh1", None),
            ("D-H03-02", "wb2", "cb2", "man2", "rh2", None),
            (
                "Error de convergencia en límite D-H03-03",
                r"El estimador converge porque \lim_{n\to\infty} \frac{\sigma^2}{n} = 0 en probabilidad.",
                r"La convergencia requiere acotar la varianza asintótica.",
                r"\lim_{n\to\infty} \frac{\sigma^2}{n} = 0",
                r"Revisar el cálculo del límite de la varianza.",
                None,
            ),
        ],
    ),
    (
        "concept",
        "C-03",
        "Promedios y sumas muestrales",
        r"Ley débil de los grandes números.",
        "Understand",
        "asymptotic_notes.pdf",
        2,
        ["H-03"],
        [
            ("D-C03-01", "wb1", "cb1", "man1", "rh1", None),
            ("D-C03-02", "wb2", "cb2", "man2", "rh2", None),
            ("D-C03-03", "wb3", "cb3", "man3", "rh3", None),
            (
                "Confusión de promedio muestral D-C03-04",
                r"Confunde el promedio muestral \frac{1}{n}\sum_{i=1}^n X_i con la esperanza poblacional.",
                r"El promedio muestral es una variable aleatoria, la esperanza es constante.",
                r"\frac{1}{n}\sum_{i=1}^n X_i",
                r"Recordar la definición formal del promedio muestral.",
                None,
            ),
        ],
    ),
    (
        "skill",
        "Hab-01",
        "Normalidad asintótica del estimador",
        r"Aplicación del Teorema del Límite Central.",
        "Apply",
        "asymptotic_notes.pdf",
        3,
        ["H-03", "C-03"],
        [
            ("D-Hab01-01", "wb1", "cb1", "man1", "rh1", "os1"),
            ("D-Hab01-02", "wb2", "cb2", "man2", "rh2", "os2"),
            ("D-Hab01-03", "wb3", "cb3", "man3", "rh3", None),
            ("D-Hab01-04", "wb4", "cb4", "man4", "rh4", None),
            (
                "Fórmula TLC asintótica D-Hab01-05",
                r"El resultado establece que \sqrt{n}(\hat{\theta}_n - \theta_0) \xrightarrow{d} \mathcal{N}(0, V) para la muestra.",
                r"La distribución límite normal requiere escalar por la raíz del tamaño muestral.",
                r"\sqrt{n}(\hat{\theta}_n - \theta_0) \xrightarrow{d} \mathcal{N}(0, V)",
                r"Aplicar la estandarización adecuada bajo el TLC.",
                None,
            ),
            ("D-Hab01-06", "wb6", "cb6", "man6", "rh6", None),
        ],
    ),
    (
        "skill",
        "Hab-03",
        "Inferencia sobre parámetros de dispersión",
        r"Cálculo de errores estándar asintóticos.",
        "Apply",
        "asymptotic_notes.pdf",
        4,
        ["Hab-01"],
        [
            ("D-Hab03-01", "wb1", "cb1", "man1", "rh1", "os1"),
            (
                "Sigma suelto en prosa D-Hab03-02",
                r"Confunde \sigma con la varianza poblacional al estimar.",
                r"El parámetro \sigma es la desviación estándar, mientras que la varianza es \sigma^2.",
                r"\sigma",
                r"Distinguir la desviación estándar de la varianza.",
                None,
            ),
            ("D-Hab03-03", "wb3", "cb3", "man3", "rh3", None),
            ("D-Hab03-04", "wb4", "cb4", "man4", "rh4", None),
            ("D-Hab03-05", "wb5", "cb5", "man5", "rh5", None),
            ("D-Hab03-06", "wb6", "cb6", "man6", "rh6", None),
        ],
    ),
    (
        "skill",
        "Hab-04",
        "Ecuaciones de regresión asintótica",
        r"Estimación de coeficientes bajo ortogonalidad.",
        "Apply",
        "asymptotic_notes.pdf",
        5,
        ["Hab-03"],
        [
            ("D-Hab04-01", "wb1", "cb1", "man1", "rh1", "os1"),
            ("D-Hab04-02", "wb2", "cb2", "man2", "rh2", "os2"),
            ("D-Hab04-03", "wb3", "cb3", "man3", "rh3", None),
            ("D-Hab04-04", "wb4", "cb4", "man4", "rh4", None),
            (
                "Ecuación con signo igual D-Hab04-05",
                r"Afirma erróneamente que \beta = \alpha + 1 al estimar el modelo lineal.",
                r"El parámetro estimado depende de la covarianza muestral entre regresores.",
                r"\beta = \alpha + 1",
                r"Despejar los coeficientes a partir de las ecuaciones normales.",
                None,
            ),
            ("D-Hab04-06", "wb6", "cb6", "man6", "rh6", None),
        ],
    ),
]
'''


def test_asymptotic_statistics_v5_patterns_tier0_autoheal(tmp_path):
    """Verifies that all 5 real patterns of asyntotic_estatistics_v5 (D-H03-03, D-C03-04, D-Hab01-05,

    D-Hab03-02, D-Hab04-05) are healed in Tier 0 with 0 errors and pass check_cta_katex.
    """
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True)

    manifest_file = work_dir / "pre_cta_manifest.json"
    manifest_file.write_text(json.dumps({
        "course_id": "asyntotic_estatistics_v5",
        "title": "Estadística Asintótica Avanzada",
        "files": [{
            "doc": "asymptotic_notes.pdf",
            "name": "asymptotic_notes.pdf",
            "valid_page_range": [1, 10],
            "total_pages": 10,
        }],
    }), encoding="utf-8")

    cta_py_file = work_dir / "cta_data.py"
    cta_py_file.write_text(ASYMPTOTIC_V5_CTA_SOURCE, encoding="utf-8")

    # 1. Compile through compile_cta
    valid, cta_dict, errors, elapsed = compile_cta(
        cta_data_path=cta_py_file,
        output_dir=work_dir,
        manifest_path=manifest_file,
    )

    assert valid is True, f"Compilation failed with errors: {errors}"
    assert len(errors) == 0

    # 2. Verify check_cta_katex reports exactly 0 violations
    katex_violations = check_cta_katex(cta_dict)
    assert len(katex_violations) == 0, f"check_cta_katex reported violations: {katex_violations}"

    # 3. Locate and verify each of the 5 exact distractor fields
    comps_by_id = {c["id"]: c for c in cta_dict["competencies"]}

    # Pattern 1: D-H03-03 (\lim_{n\to\infty} \frac{\sigma^2}{n} = 0)
    d_h03_03 = comps_by_id["H-03"]["distractors"][2]
    assert r"$\lim_{n\to\infty} \frac{\sigma^2}{n} = 0$" in d_h03_03["wrong_belief"]
    assert d_h03_03["manifestation"] == r"$\lim_{n\to\infty} \frac{\sigma^2}{n} = 0$"

    # Pattern 2: D-C03-04 (\frac{1}{n}\sum_{i=1}^n X_i)
    d_c03_04 = comps_by_id["C-03"]["distractors"][3]
    assert r"$\frac{1}{n}\sum_{i=1}^n X_i$" in d_c03_04["wrong_belief"]
    assert d_c03_04["manifestation"] == r"$\frac{1}{n}\sum_{i=1}^n X_i$"

    # Pattern 3: D-Hab01-05 (\sqrt{n}(\hat{\theta}_n - \theta_0) \xrightarrow{d} \mathcal{N}(0, V))
    d_hab01_05 = comps_by_id["Hab-01"]["distractors"][4]
    assert r"$\sqrt{n}(\hat{\theta}_n - \theta_0) \xrightarrow{d} \mathcal{N}(0, V)$" in d_hab01_05["wrong_belief"]
    assert d_hab01_05["manifestation"] == r"$\sqrt{n}(\hat{\theta}_n - \theta_0) \xrightarrow{d} \mathcal{N}(0, V)$"

    # Pattern 4: D-Hab03-02 (\sigma suelto en prosa)
    d_hab03_02 = comps_by_id["Hab-03"]["distractors"][1]
    assert r"$\sigma$" in d_hab03_02["wrong_belief"]
    assert d_hab03_02["manifestation"] == r"$\sigma$"

    # Pattern 5: D-Hab04-05 (ecuación con =)
    d_hab04_05 = comps_by_id["Hab-04"]["distractors"][4]
    assert r"$\beta = \alpha + 1$" in d_hab04_05["wrong_belief"]
    assert d_hab04_05["manifestation"] == r"$\beta = \alpha + 1$"

    # 4. Verify pass_cta_cta_data.json and pass_cta_data.json both exist
    assert (work_dir / ".check_attempts" / "pass_cta_cta_data.json").is_file()
    assert (work_dir / ".check_attempts" / "pass_cta_data.json").is_file()


def test_compile_cta_syntax_error_state_flag(tmp_path):
    """Verifies that has_syntax_error: True is recorded in .check_attempts when part_01_data.py has a Python SyntaxError."""
    work_dir = tmp_path / "work"
    parts_dir = work_dir / "cta_parts"
    parts_dir.mkdir(parents=True)

    manifest_file = work_dir / "pre_cta_manifest.json"
    manifest_file.write_text(json.dumps({
        "course_id": "syntax_err_test",
        "files": [{"doc": "doc.pdf", "valid_page_range": [1, 10], "total_pages": 10}],
    }), encoding="utf-8")

    # Broken Python file with a deliberate syntax error (unclosed tuple/bracket)
    broken_syntax_content = '''# part_01_data.py
COURSE_ID = "syntax_err_test"
COMPETENCIES = [
    ("fact", "H-01", "Nombre incompleto", "desc", "Remember", "doc.pdf", 1, [], [
'''
    part_file = parts_dir / "part_01_data.py"
    part_file.write_text(broken_syntax_content, encoding="utf-8")

    valid, cta_dict, errors, elapsed = compile_cta(
        cta_data_path=part_file,
        output_dir=parts_dir,
        manifest_path=manifest_file,
        output_json_name="part_01.json",
        is_part=True,
        allow_degrade=False,
    )

    assert valid is False
    assert len(errors) >= 1
    assert any("Syntax" in e or "SyntaxError" in e for e in errors)

    # Verify .check_attempts/compile_cta_part_01.json
    att_file = parts_dir / ".check_attempts" / "compile_cta_part_01.json"
    assert att_file.is_file(), f"Expected {att_file} to exist"
    state = json.loads(att_file.read_text(encoding="utf-8"))
    assert state["has_syntax_error"] is True
    assert state["error_count"] >= 1
    assert state["distinct_compiles"] == 1

    # Verify .check_attempts/compile_part_01.json also exists with the same flags
    alt_att_file = parts_dir / ".check_attempts" / "compile_part_01.json"
    assert alt_att_file.is_file(), f"Expected {alt_att_file} to exist"
    alt_state = json.loads(alt_att_file.read_text(encoding="utf-8"))
    assert alt_state["has_syntax_error"] is True
    assert alt_state["error_count"] >= 1

    # Verify pass files do NOT exist
    assert not (parts_dir / ".check_attempts" / "pass_cta_part_01.json").is_file()
    assert not (parts_dir / ".check_attempts" / "pass_part_01.json").is_file()

