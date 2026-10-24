"""Unit Tests for Shard 06, DRY Archetypes, CLI Outputs & Path Diagnostics (Stream 1B).

Covers:
1. DRY Distractor Inheritance with 4 Milestone 3 Archetypes:
   - Directo: 2-tuple compact format ("D-Hab06-01", r"$@d1@$")
   - Inverso: Compact dict format {"distractor_id": "D-Hab06-02", "value": r"$@d2@$"} without error_rationale
   - Perturbación: Inverted 2-tuple format (r"$@d1@$", "D-Hab06-01") via tuple return
   - Frontera: Bare string format r"$@d1@$"
   - Verifies auto-population from cta.json, KaTeX wrapping of bare expressions,
     giveaway prefix stripping, and strict mode validation (R-17, R-20, R-22, TPL-VAR, diversity >= 0.50).
2. Receipt JSON (--output) and Post-PASS Marker (.check_attempts/pass_shard_06.json):
   - Updates --output with compiled_status = "PASS" / "FAIL".
   - Creates and unlinks .check_attempts/pass_shard_06.json correctly.
3. Path Parity in render_compact_aggregated_errors:
   - Prioritizes real targets (courses/<id>/work/templates/<cid>.json) over default fallback.
4. Work Dir Auto-Inference:
   - Infers courses/<id>/work from active lockfile when default work is missing from CWD.
5. Surgical R-20 LaTeX Diagnostics:
   - Reports exact option field with distractor ID, brace counts open=N vs close=M, and inverted patterns.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

import pytest

# Ensure skill root and project src are in sys.path
_skill_root = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

_src_root = Path(__file__).resolve().parents[1] / "src"
if str(_src_root) not in sys.path:
    sys.path.insert(0, str(_src_root))

from check_templates import (
    _strip_giveaway_prefix,
    _wrap_bare_latex_in_rationale,
    format_invariant_error_diagnostic,
    render_compact_aggregated_errors,
)
from compile_shard import compile_shard, infer_work_dir


def _setup_workspace_shard06(tmp_path: Path):
    """Sets up a complete isolated workspace for shard_06 with competency Hab-06."""
    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    templates_dir = work_dir / "templates"
    shards_dir.mkdir(parents=True, exist_ok=True)
    templates_dir.mkdir(parents=True, exist_ok=True)

    cta_payload = {
        "competencies": [
            {
                "id": "Hab-06",
                "name": "Estimación y Propiedades del Modelo Lineal",
                "type": "skill",
                "distractors": [
                    {
                        "id": "D-Hab06-01",
                        "remediation_hint": "Verifique la covarianza entre las variables explicativas y el término de perturbación.",
                    },
                    {
                        "id": "D-Hab06-02",
                        "wrong_belief": "Confunde la varianza con el desvío estándar",
                        "omitted_step": "Elevar al cuadrado la dispersión muestral",
                    },
                    {
                        "id": "D-Hab06-03",
                        "wrong_belief": "Error de signo en la pendiente de la regresión",
                        "omitted_step": "Invertir el signo del numerador",
                    },
                    {
                        "id": "D-Hab06-04",
                        "remediation_hint": "Considere la condición de frontera con \\beta_1 = 0 en el estimador.",
                    },
                    {
                        "id": "D-Hab06-05",
                        "wrong_belief": "Asumiendo erróneamente: omitir el término cuadrático de la especificación",
                        "omitted_step": "Incluir el efecto no lineal",
                    },
                    {
                        "id": "D-Hab06-06",
                        "remediation_hint": "Calcule la varianza residual dividiendo por \\frac{n-k}{2} según los grados de libertad.",
                    },
                ],
            }
        ]
    }
    cta_file = work_dir / "cta.json"
    cta_file.write_text(json.dumps(cta_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    manifest_payload = {
        "shards": [
            {
                "shard_id": "shard_06",
                "competency_ids": ["Hab-06"],
                "shard_data_path": str((shards_dir / "shard_06_data.py").resolve().as_posix()),
                "templates_dir": str(templates_dir.resolve().as_posix()),
                "competencies": [
                    {
                        "id": "Hab-06",
                        "name": "Estimación y Propiedades del Modelo Lineal",
                        "type": "skill",
                        "distractors": cta_payload["competencies"][0]["distractors"],
                    }
                ],
            }
        ]
    }
    manifest_file = shards_dir / "pre_shard_manifest.json"
    manifest_file.write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    return work_dir, shards_dir, templates_file_dir(work_dir), cta_file, manifest_file


def templates_file_dir(work_dir: Path) -> Path:
    return work_dir / "templates"


class TestDryArchetypesAndDistractorInheritance:
    """Verifies Requirement 3.A: DRY Distractor Inheritance across 4 Milestone 3 Archetypes."""

    def test_dry_distractor_inheritance_four_archetypes_strict_pass(self, tmp_path: Path):
        """Compiles shard_06 with 4 archetypes using compact DRY formats without manual 24x rationales."""
        work_dir, shards_dir, templates_dir, cta_file, _ = _setup_workspace_shard06(tmp_path)
        shard_py = shards_dir / "shard_06_data.py"

        shard_code = '''"""Shard 06 Data with 4 Disjoint Archetypes for Hab-06."""
import random

# Archetype 1: Directo (compact 2-tuple distractors)
def gen_directo(rng):
    base = rng.randint(20, 80)
    step = rng.randint(2, 6)
    v_corr = base + 3 * step
    return {
        "vars": {
            "base": base, "step": step, "ans": v_corr,
            "d1": base + step, "d2": base + 2 * step, "d3": base + 4 * step,
            "d4": base + 5 * step, "d5": base + 6 * step, "d6": base + 7 * step,
        },
        "correct": r"$@ans@$",
        "distractors": [
            ("D-Hab06-01", r"$@d1@$"),
            ("D-Hab06-02", r"$@d2@$"),
            ("D-Hab06-03", r"$@d3@$"),
            ("D-Hab06-04", r"$@d4@$"),
            ("D-Hab06-05", r"$@d5@$"),
            ("D-Hab06-06", r"$@d6@$"),
        ],
    }

def ver_directo(res):
    return True

# Archetype 2: Inverso (compact dict format without error_rationale)
def gen_inverso(rng):
    target = rng.randint(50, 120)
    factor = rng.randint(2, 5)
    ans = target // factor
    return {
        "vars": {
            "target": target, "factor": factor, "ans": ans,
            "d1": ans - 1, "d2": ans + 1, "d3": ans + 2,
            "d4": ans + 3, "d5": ans + 4, "d6": ans + 5,
        },
        "correct": r"$@ans@$",
        "distractors": [
            {"distractor_id": "D-Hab06-01", "value": r"$@d1@$"},
            {"distractor_id": "D-Hab06-02", "value": r"$@d2@$"},
            {"distractor_id": "D-Hab06-03", "value": r"$@d3@$"},
            {"distractor_id": "D-Hab06-04", "value": r"$@d4@$"},
            {"distractor_id": "D-Hab06-05", "value": r"$@d5@$"},
            {"distractor_id": "D-Hab06-06", "value": r"$@d6@$"},
        ],
    }

def ver_inverso(res):
    return True

# Archetype 3: Perturbación (inverted 2-tuple format via tuple return)
def gen_perturbacion(rng):
    x = rng.randint(10, 40)
    dx = rng.randint(1, 4)
    ans = x + dx
    v_dict = {
        "x": x, "dx": dx, "ans": ans,
        "d1": x - dx, "d2": x + 2 * dx, "d3": x + 3 * dx,
        "d4": x - 2 * dx, "d5": x + 4 * dx, "d6": x + 5 * dx,
    }
    dists = [
        (r"$@d1@$", "D-Hab06-01"),
        (r"$@d2@$", "D-Hab06-02"),
        (r"$@d3@$", "D-Hab06-03"),
        (r"$@d4@$", "D-Hab06-04"),
        (r"$@d5@$", "D-Hab06-05"),
        (r"$@d6@$", "D-Hab06-06"),
    ]
    return (v_dict, r"$@ans@$", dists)

def ver_perturbacion(res):
    return True

# Archetype 4: Frontera (bare scalar string distractors)
def gen_frontera(rng):
    k = rng.randint(5, 25)
    return {
        "vars": {
            "k": k, "ans": k * 2,
            "d1": k, "d2": k + 1, "d3": k - 1,
            "d4": k * 3, "d5": k * 4, "d6": k * 5,
        },
        "correct": r"$@ans@$",
        "distractors": [
            r"$@d1@$", r"$@d2@$", r"$@d3@$",
            r"$@d4@$", r"$@d5@$", r"$@d6@$",
        ],
    }

def ver_frontera(res):
    return True

TEMPLATES = [
    (
        "T-Hab06-01", "Hab-06", "multiple_choice_7_options",
        gen_directo, ver_directo, "medium",
        [
            "Calcule el valor del estimador lineal directo bajo base {base} y paso {step}.",
            "A partir de las condiciones observadas con base {base}, determine el estimador lineal.",
            "Para los datos estructurados con parámetro base {base}, evalúe el valor directo.",
            "Determine analíticamente la estimación directa correspondiente dado el paso {step}.",
        ],
        ["Identifique el modelo lineal directo.", "Aplique la suma iterada.", "Verifique los supuestos."],
        "Resolución directa formal: el estimador es ans = base + 3*step = {ans}."
    ),
    (
        "T-Hab06-02", "Hab-06", "multiple_choice_7_options",
        gen_inverso, ver_inverso, "hard",
        [
            "Deduzca el parámetro invertido sabiendo que el producto objetivo es {target} con factor {factor}.",
            "A partir del valor objetivo {target}, determine el parámetro estructural inverso con factor {factor}.",
            "En el contexto inverso formal, evalúe la cantidad estimada correspondiente para factor {factor}.",
            "Despeje rigurosamente el parámetro del modelo sabiendo el objetivo {target}.",
        ],
        ["Plantee la ecuación inversa.", "Divida el objetivo por el factor.", "Compruebe la consistencia dimensional."],
        "Resolución inversa formal: el parámetro despejado es ans = target / factor = {ans}."
    ),
    (
        "T-Hab06-03", "Hab-06", "multiple_choice_7_options",
        gen_perturbacion, ver_perturbacion, "medium",
        [
            "Evalúe la respuesta ante una perturbación de magnitud {dx} sobre el valor inicial {x}.",
            "Considere el desplazamiento marginal {dx} aplicado al sistema con nivel {x} y determine la respuesta.",
            "Bajo el supuesto de una perturbación {dx}, calcule el estado final del estimador.",
            "Analice la sensibilidad analítica y halle el valor desplazado con variación {dx}.",
        ],
        ["Identifique el punto de perturbación.", "Sume el diferencial al nivel base.", "Compruebe el orden de magnitud."],
        "Resolución de perturbación: el valor perturbado es x + dx = {ans}."
    ),
    (
        "T-Hab06-04", "Hab-06", "multiple_choice_7_options",
        gen_frontera, ver_frontera, "hard",
        [
            "Establezca el comportamiento en el punto de frontera sabiendo que el parámetro de control es {k}.",
            "En el régimen límite donde el parámetro es {k}, evalúe la solución asintótica.",
            "Tomando en cuenta las condiciones de frontera para {k}, halle el valor estacionario.",
            "Verifique la cota analítica extrema cuando la variable de control alcanza {k}.",
        ],
        ["Analice la condición de frontera.", "Multiplique el parámetro de control por la ganancia.", "Verifique el límite."],
        "Resolución en la frontera: la solución extrema es ans = 2*k = {ans}."
    ),
]
'''
        shard_py.write_text(shard_code, encoding="utf-8")

        # Compile shard_06 with strict=True
        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_06",
            strict=True,
            seeds=50,
            cta_path=cta_file,
        )
        assert success, f"Expected successful compile, got errors: {errors}"
        assert len(errors) == 0

        # Verify compiled templates JSON
        tpl_json_path = templates_dir / "Hab-06.json"
        assert tpl_json_path.is_file(), f"Compiled template JSON not found at {tpl_json_path}"

        tpl_data = json.loads(tpl_json_path.read_text(encoding="utf-8"))
        assert "templates" in tpl_data
        templates_list = tpl_data["templates"]
        assert len(templates_list) == 4, f"Expected 4 archetypes, found {len(templates_list)}"

        # Check that post-PASS marker exists
        pass_marker = work_dir / ".check_attempts" / "pass_shard_06.json"
        assert pass_marker.is_file(), "pass_shard_06.json marker must exist after clean PASS"
        p_data = json.loads(pass_marker.read_text(encoding="utf-8"))
        assert p_data["status"] == "PASS"
        assert p_data["shard_id"] == "shard_06"
        assert p_data["template_counts"]["Hab-06"] == 4

    def test_dry_distractor_inheritance_heterogeneous_3tuple_return(self, tmp_path: Path):
        """Verifies 3-tuple return format (vars, correct, distractors) with heterogeneous distractor types
        including underscore IDs (D_Hab06_01), bare strings, and compact dicts without rationales.
        """
        work_dir, shards_dir, templates_dir, cta_file, _ = _setup_workspace_shard06(tmp_path)
        shard_py = shards_dir / "shard_06_data.py"

        shard_code = '''
import random
def gen_hetero(rng):
    v = rng.randint(10, 40)
    v_dict = {"v": v, "d1": v+1, "d2": v+2, "d3": v+3, "d4": v+4, "d5": v+5, "d6": v+6}
    # Mixed distractors: 2-tuple with underscore ID, compact dict, bare string
    dists = [
        ("D_Hab06_01", "$@d1@$"),
        {"distractor_id": "D-Hab06-02", "content": "$@d2@$"},
        ("$@d3@$", "D-Hab06-03"),
        "$@d4@$",
        "$@d5@$",
        "$@d6@$",
    ]
    return (v_dict, "$@v@$", dists)

def ver_hetero(res): return True

TEMPLATES = [
    (
        "T-Hab06-01", "Hab-06", "multiple_choice_7_options",
        gen_hetero, ver_hetero, "medium",
        [
            "Evalúe la función heterogénea con parámetro {v}.",
            "Para el valor observado {v}, determine el resultado correspondiente.",
            "En el análisis paramétrico con entrada {v}, halle el valor.",
            "Determine la magnitud estimada para el parámetro {v}.",
        ],
        ["Revise el modelo.", "Calcule la respuesta.", "Verifique los supuestos."],
        "Solución heterogénea con {v}."
    )
]
'''
        shard_py.write_text(shard_code, encoding="utf-8")

        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_06",
            strict=True,
            seeds=50,
            cta_path=cta_file,
        )
        assert success, f"Expected successful compile for heterogeneous 3-tuple, got: {errors}"
        out_json = templates_dir / "Hab-06.json"
        assert out_json.is_file()


class TestCliReceiptAndPassMarker:
    """Verifies Requirement 3.B: --output receipt JSON and post-PASS marker lifecycle."""

    def test_output_receipt_json_created_and_updated_on_pass(self, tmp_path: Path):
        work_dir, shards_dir, templates_dir, cta_file, _ = _setup_workspace_shard06(tmp_path)
        shard_py = shards_dir / "shard_06_data.py"

        # Minimal single template
        shard_code = '''
import random
def gen(rng):
    v = rng.randint(10, 50)
    return {
        "vars": {"v": v, "d1": v+1, "d2": v+2, "d3": v+3, "d4": v+4, "d5": v+5, "d6": v+6},
        "correct": str(v),
        "distractors": [
            ("D-Hab06-01", str(v+1)), ("D-Hab06-02", str(v+2)), ("D-Hab06-03", str(v+3)),
            ("D-Hab06-04", str(v+4)), ("D-Hab06-05", str(v+5)), ("D-Hab06-06", str(v+6)),
        ],
    }
def ver(r): return True
TEMPLATES = [
    ("T-Hab06", "Hab-06", "multiple_choice_7_options", gen, ver, "medium",
     ["Variante stem A con {v}", "Variante stem B con {v}", "Variante stem C con {v}", "Variante stem D con {v}"],
     ["Pista 1", "Pista 2", "Pista 3"], "Solucion formal con {v}")
]
'''
        shard_py.write_text(shard_code, encoding="utf-8")

        receipt_file = shards_dir / "shard_06.json"
        # Pre-seed receipt with author metadata to verify non-destructive update
        receipt_file.write_text(json.dumps({"author": "test_agent", "initial_status": "PENDING"}), encoding="utf-8")

        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_06",
            strict=True,
            seeds=20,
            output_path=receipt_file,
            cta_path=cta_file,
        )
        assert success, f"Expected pass, got: {errors}"

        # Receipt file must be updated preserving previous keys
        receipt_data = json.loads(receipt_file.read_text(encoding="utf-8"))
        assert receipt_data.get("author") == "test_agent"
        assert receipt_data.get("compiled_status") == "PASS"
        assert "compiled_templates" in receipt_data
        assert "compiled_at" in receipt_data

        # Pass marker must exist
        pass_marker = work_dir / ".check_attempts" / "pass_shard_06.json"
        assert pass_marker.is_file()

    def test_output_receipt_and_marker_cleanup_on_failure(self, tmp_path: Path):
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard06(tmp_path)
        shard_py = shards_dir / "shard_06_data.py"

        # Broken template (zero division)
        broken_code = '''
def gen(rng):
    return 10 / 0
def ver(r): return True
TEMPLATES = [
    ("T-Hab06", "Hab-06", "multiple_choice_7_options", gen, ver, "medium",
     ["Stem {v}"], ["H1", "H2", "H3"], "Sol")
]
'''
        shard_py.write_text(broken_code, encoding="utf-8")

        # Fake pre-existing pass marker from older run
        pass_marker = work_dir / ".check_attempts" / "pass_shard_06.json"
        pass_marker.parent.mkdir(parents=True, exist_ok=True)
        pass_marker.write_text(json.dumps({"status": "OLD_PASS"}), encoding="utf-8")

        receipt_file = shards_dir / "shard_06.json"
        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_06",
            strict=False,
            output_path=receipt_file,
            cta_path=cta_file,
        )
        assert not success

        # Old pass marker must be deleted
        assert not pass_marker.is_file(), "pass_shard_06.json must be unlinked on compilation failure"

        # Receipt file must record FAIL
        receipt_data = json.loads(receipt_file.read_text(encoding="utf-8"))
        assert receipt_data.get("compiled_status") == "FAIL"
        assert "compilation_errors" in receipt_data

    def test_pass_marker_unlinked_on_early_manifest_miss(self, tmp_path: Path):
        """Verifies pass marker is unlinked even if failure occurs early due to missing shard in manifest."""
        work_dir, shards_dir, _, cta_file, manifest_file = _setup_workspace_shard06(tmp_path)
        # Pre-seed stale pass marker
        pass_marker = work_dir / ".check_attempts" / "pass_shard_06.json"
        pass_marker.parent.mkdir(parents=True, exist_ok=True)
        pass_marker.write_text(json.dumps({"status": "STALE_PASS"}), encoding="utf-8")

        # Empty manifest so shard_06 is missing
        manifest_file.write_text(json.dumps({"shards": []}), encoding="utf-8")

        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_06",
            strict=True,
        )
        assert not success
        assert not pass_marker.is_file(), "pass marker must be unlinked even on early manifest missing shard error"


class TestWorkDirInference:
    """Verifies Requirement 3.B.1: In-memory inference of work directory via active lockfile."""

    def test_infer_work_dir_from_active_course_lockfile(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        course_dir = tmp_path / "courses" / "curso_econometria"
        work_dir = course_dir / "work"
        shards_dir = work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)

        manifest = shards_dir / "pre_shard_manifest.json"
        manifest.write_text("{}", encoding="utf-8")

        # Create active lockfile
        lock_file = course_dir / ".c2c_subagent_lock.json"
        lock_file.write_text(json.dumps({"active": True, "shard_id": "shard_06"}), encoding="utf-8")

        inferred = infer_work_dir("work", shard_id="shard_06")
        assert inferred.resolve() == work_dir.resolve()


class TestPathDiagnosticsAndR20Clarity:
    """Verifies Requirement 3.C: Path accuracy in render_compact_aggregated_errors & R-20 diagnostics."""

    def test_render_compact_aggregated_errors_reports_real_target_path(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        real_target = tmp_path / "courses" / "curso_macro" / "work" / "templates" / "Hab-06.json"
        real_target.parent.mkdir(parents=True, exist_ok=True)
        real_target.write_text("{}", encoding="utf-8")

        from check_templates import format_diagnostic_error
        dummy_err = format_diagnostic_error(
            rule_tag="R-20: SINTAXIS / LLAVES",
            competency="Hab-06",
            template="T-Hab-06",
            item_id="N/A",
            field_name="stem",
            snippet="x = 1",
            cause="Error sintáctico de prueba",
            actions=["Corregir sintaxis"],
        )

        report = render_compact_aggregated_errors([dummy_err], targets=[real_target])
        assert "courses/curso_macro/work/templates/Hab-06.json" in report
        assert " - work/templates/Hab-06.json" not in report

    def test_r20_diagnostic_exact_field_distractor_and_brace_analysis(self):
        """Verifies R-20 extracts options[idx].error_rationale, distractor ID, and counts open vs close."""
        inv_err = "LaTeX math expression in option 2 error_rationale has unbalanced braces: $H = \\hat{\\beta}_}{1}$"
        q_obj = {
            "options": [
                {"content": "$A$", "is_correct": True},
                {"content": "$B$", "is_correct": False, "distractor_id": "D-Hab06-02", "error_rationale": "$H = \\hat{\\beta}_}{1}$"},
            ]
        }

        diag = format_invariant_error_diagnostic(
            cid="Hab-06",
            tpl_id="T-Hab06-01",
            q_id="Q-001",
            inv_err=inv_err,
            q_obj=q_obj,
        )

        # Field must pinpoint options[1].error_rationale with distractor D-Hab06-02
        assert "options[1].error_rationale (distractor D-Hab06-02)" in diag.cause or "options[1].error_rationale" in diag.field_name
        # Must detect inverted pattern or brace discrepancy
        assert "patrón invertido" in diag.cause or "open=" in diag.cause
        # Action must instruct how to balance
        assert any("Balancear" in a for a in diag.actions)


class TestLatexWrappingAndGiveawayStripping:
    """Verifies KaTeX wrapping and giveaway prefix elimination."""

    def test_wrap_bare_latex_in_rationale_encloses_unwrapped_math(self):
        raw = "El estudiante confunde \\hat{\\beta}_1 con el valor poblacional \\beta_1 sin considerar el sesgo."
        wrapped = _wrap_bare_latex_in_rationale(raw)
        assert "$\\hat{\\beta}_1$" in wrapped
        assert "$\\beta_1$" in wrapped

    def test_wrap_bare_latex_leaves_existing_math_intact(self):
        raw = "Usa $\\sigma^2$ en lugar de $\\frac{s^2}{n}$."
        wrapped = _wrap_bare_latex_in_rationale(raw)
        assert wrapped == raw

    def test_strip_giveaway_prefix_removes_unwanted_labels(self):
        raw = "Asumiendo erróneamente: omitir la raíz cuadrada."
        cleaned = _strip_giveaway_prefix(raw)
        assert cleaned == "Omitir la raíz cuadrada."
        assert not cleaned.startswith("Asumiendo erróneamente")

    def test_wrap_bare_latex_nested_subscripts_and_superscripts(self):
        """Verifies robust KaTeX wrapping with nested braces like \\hat{\\beta}_{\\text{ML}}, \\sigma^2_{x_i}, \\hat{\\beta}_1^{(k)}, \\frac{n-k}{2}."""
        raw = "El estimador \\hat{\\beta}_{\\text{ML}} tiene varianza asintótica \\sigma^2_{x_i} y ratio \\frac{n-k}{2}."
        wrapped = _wrap_bare_latex_in_rationale(raw)
        assert "$\\hat{\\beta}_{\\text{ML}}$" in wrapped
        assert "$\\sigma^2_{x_i}$" in wrapped
        assert "$\\frac{n-k}{2}$" in wrapped
        assert "}" not in wrapped.replace("$\\hat{\\beta}_{\\text{ML}}$", "").replace("$\\sigma^2_{x_i}$", "").replace("$\\frac{n-k}{2}$", "")

    def test_wrap_bare_latex_relational_expressions(self):
        """Verifies wrapping relational math expressions like \\beta_1 = 0 without breaking punctuation."""
        raw = "Bajo la hipótesis nula donde \\beta_1 = 0, el estadístico diverge."
        wrapped = _wrap_bare_latex_in_rationale(raw)
        assert "$\\beta_1 = 0$" in wrapped
        assert wrapped.endswith(", el estadístico diverge.")


class TestRealShard06Compilation:
    """Verifies that the actual courses/asyntotic_estatistics_v4/work/shards/shard_06_data.py
    compiles with ZERO errors under strict=True and 50 seeds dry-run.
    """

    def test_compile_real_shard_06_strict_pass(self, tmp_path: Path):
        repo_root = Path(__file__).resolve().parents[1]
        real_course_dir = repo_root / "courses" / "asyntotic_estatistics_v4" / "work"
        real_shard_py = real_course_dir / "shards" / "shard_06_data.py"
        real_cta = real_course_dir / "cta.json"
        real_manifest = real_course_dir / "shards" / "pre_shard_manifest.json"

        assert real_shard_py.is_file(), f"Real shard 06 not found at {real_shard_py}"
        assert real_cta.is_file(), f"Real cta.json not found at {real_cta}"
        assert real_manifest.is_file(), f"Real manifest not found at {real_manifest}"

        # Setup isolated tmp workspace copying real files
        work_dir = tmp_path / "work"
        shards_dir = work_dir / "shards"
        templates_dir = work_dir / "templates"
        shards_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)

        import shutil
        shutil.copy(real_cta, work_dir / "cta.json")
        target_shard_py = shards_dir / "shard_06_data.py"
        shutil.copy(real_shard_py, target_shard_py)

        # Build isolated manifest for shard_06 pointing to tmp paths
        man_data = json.loads(real_manifest.read_text(encoding="utf-8"))
        s06_entries = [s for s in man_data.get("shards", []) if s.get("shard_id") == "shard_06"]
        assert len(s06_entries) == 1, "shard_06 entry must exist in real manifest"
        isolated_entry = dict(s06_entries[0])
        isolated_entry["shard_data_path"] = str(target_shard_py.resolve().as_posix())
        isolated_entry["templates_dir"] = str(templates_dir.resolve().as_posix())
        tmp_manifest = shards_dir / "pre_shard_manifest.json"
        tmp_manifest.write_text(json.dumps({"shards": [isolated_entry]}, indent=2), encoding="utf-8")

        # Compile in strict mode with 50 dry-run seeds
        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_06",
            strict=True,
            seeds=50,
            cta_path=work_dir / "cta.json",
        )
        assert success, f"Real shard_06 failed strict compilation: {errors}"
        assert len(errors) == 0

        # Verify compiled Hab-06.json
        out_json = templates_dir / "Hab-06.json"
        assert out_json.is_file(), f"Expected compiled template at {out_json}"
        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload.get("competency_id") == "Hab-06"
        if "templates" in payload:
            assert len(payload["templates"]) == 4
            assert all(t.get("interaction_type") == "multiple_choice_7_options" for t in payload["templates"])
        else:
            assert payload.get("interaction_type") == "multiple_choice_7_options"

        # Verify pass marker exists and is clean
        pass_marker = work_dir / ".check_attempts" / "pass_shard_06.json"
        assert pass_marker.is_file()
        p_data = json.loads(pass_marker.read_text(encoding="utf-8"))
        assert p_data.get("status") == "PASS"
        assert p_data.get("shard_id") == "shard_06"
