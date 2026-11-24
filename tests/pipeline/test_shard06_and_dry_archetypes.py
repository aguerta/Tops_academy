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
_skill_root = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

_src_root = Path(__file__).resolve().parents[2] / "src"
if str(_src_root) not in sys.path:
    sys.path.insert(0, str(_src_root))

from check_templates import (
    DiagnosticError,
    _strip_giveaway_prefix,
    _wrap_bare_latex_in_rationale,
    count_distinct_shard_error_hunks,
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

# Archetype 1: Directo (MS, easy, Apply)
def gen_directo(rng):
    base = rng.randint(20, 80)
    step = rng.randint(2, 6)
    v_corr = base + 3 * step
    d1, d2, d3 = base + step, base + 2 * step, base + 4 * step
    d4, d5, d6 = base + 5 * step, base + 6 * step, base + 7 * step
    opts = [
        {"value": r"$@ans@$ es el estimador lineal directo", "is_correct": True},
        {"value": r"El incremento acumulado es $3(@step@)$ sobre @base@", "is_correct": True},
        {"value": r"$@d1@$", "is_correct": False, "distractor_id": "D-Hab06-01", "error_rationale": "Error al estimar por omitir el término base @base@ en el cálculo inicial."},
        {"value": r"$@d2@$", "is_correct": False, "distractor_id": "D-Hab06-02", "error_rationale": "Confusión en la escala del incremento de paso @step@ dentro del modelo lineal."},
        {"value": r"$@d3@$", "is_correct": False, "distractor_id": "D-Hab06-03", "error_rationale": "Desplazamiento erróneo del parámetro base @base@ en la estimación directa."},
        {"value": r"$@d4@$", "is_correct": False, "distractor_id": "D-Hab06-04", "error_rationale": "Multiplicación incorrecta del incremento @step@ durante la estimación lineal."},
        {"value": r"$@d5@$", "is_correct": False, "distractor_id": "D-Hab06-05", "error_rationale": "Exceso de incremento en el parámetro base @base@ al calcular @d5@."},
    ]
    return {
        "vars": {
            "base": base, "step": step, "ans": v_corr,
            "d1": d1, "d2": d2, "d3": d3, "d4": d4, "d5": d5,
        },
        "options": opts,
    }

def ver_directo(res):
    if not isinstance(res, dict):
        return False
    v = res.get("vars", {})
    if v.get("ans") != v.get("base", 0) + 3 * v.get("step", 0):
        return False
    opts = res.get("options", [])
    exp_t = {r"$@ans@$ es el estimador lineal directo", r"El incremento acumulado es $3(@step@)$ sobre @base@"}
    exp_f = {f"$@d{i}@$": f"D-Hab06-0{i}" for i in range(1, 6)}
    t_opts = [o for o in opts if o.get("is_correct") is True]
    f_opts = [o for o in opts if o.get("is_correct") is False]
    return (
        len(t_opts) == 2
        and {o.get("value") for o in t_opts} == exp_t
        and len(f_opts) == 5
        and all(
            o.get("value") in exp_f
            and o.get("distractor_id") == exp_f[o.get("value")]
            and len(str(o.get("error_rationale") or "")) >= 20
            for o in f_opts
        )
    )

# Archetype 2: Inverso (FIB, medium, Apply)
def gen_inverso(rng):
    target = rng.randint(50, 120)
    factor = rng.randint(2, 5)
    ans = target // factor
    d5 = target * factor
    return {
        "vars": {
            "target": target, "factor": factor, "ans": ans, "d5": d5,
        },
        "correct": str(ans),
        "ds": [("D-Hab06-05", str(d5), "Multiplica @target@ por @factor@ en vez de dividir obteniendo el error @d5@.")],
    }

def ver_inverso(res):
    return bool(res and isinstance(res.get("vars"), dict) and str(res.get("vars", {}).get("ans")) == str(res.get("correct")))

# Archetype 3: Perturbacion (FIB, medium, Analyze)
def gen_perturbacion(rng):
    x = rng.randint(10, 40)
    dx = rng.randint(1, 4)
    ans = x + dx
    d6 = x - dx
    return {
        "vars": {
            "x": x, "dx": dx, "ans": ans, "d6": d6,
        },
        "correct": str(ans),
        "ds": [("D-Hab06-06", str(d6), "Resta el incremento @dx@ del nivel base @x@ provocando el error @d6@.")],
    }

def ver_perturbacion(res):
    return bool(res and isinstance(res.get("vars"), dict) and str(res.get("vars", {}).get("ans")) == str(res.get("correct")))

# Archetype 4: Frontera (FIB, hard, Evaluate)
def gen_frontera(rng):
    k = rng.randint(5, 25)
    ans = k * 2
    return {
        "vars": {
            "k": k, "ans": ans,
        },
        "correct": str(ans),
        "distractors": [],
    }

def ver_frontera(res):
    return bool(res and isinstance(res.get("vars"), dict) and str(res.get("vars", {}).get("ans")) == str(res.get("correct")))

hints_directo = [
    "Identifique con precision los parametros iniciales del modelo estimado.",
    "Aplique la expresion algebraica formal correspondiente al regimen directo.",
    "Compruebe la consistencia dimensional y el orden de magnitud del resultado.",
]
hints_inverso = [
    "Reconozca el valor objetivo proporcionado y el factor multiplicativo inverso.",
    "Divida el producto objetivo entre el factor estructural correspondiente.",
    "Verifique multiplicando el cociente obtenido por el factor para validar el objetivo.",
]
hints_perturbacion = [
    "Determine el nivel inicial antes de aplicar el desplazamiento marginal.",
    "Sume la perturbacion marginal al estado base del sistema lineal.",
    "Confirme que la variacion neta coincida con el incremento especificado.",
]
hints_frontera = [
    "Examine el valor de la variable de control en el limite del dominio.",
    "Evalue el doble de la magnitud de control en la condicion extrema.",
    "Valide que el resultado asintotico respete la cota analitica superior.",
]

TEMPLATES = [
    (
        "T-Hab06-01", "Hab-06", "multiple_select",
        gen_directo, ver_directo, ("easy", "Apply"),
        [
            "Calcule el valor del estimador lineal directo bajo base {base} y paso {step}.",
            "A partir de las condiciones observadas con base {base}, determine el estimador lineal.",
            "Para los datos estructurados con parametro base {base}, evalue el valor directo.",
            "Determine analiticamente la estimacion directa correspondiente dado el paso {step}.",
        ],
        hints_directo,
        "Resolucion directa formal: el estimador es ans = base + 3*step = {ans}."
    ),
    (
        "T-Hab06-02", "Hab-06", "fill_in_the_blank",
        gen_inverso, ver_inverso, ("medium", "Apply"),
        [
            "Deduzca el parametro invertido sabiendo que el producto objetivo es {target} con factor {factor}.",
            "A partir del valor objetivo {target}, determine el parametro estructural inverso con factor {factor}.",
            "En el contexto inverso formal, evalue la cantidad estimada correspondiente para objetivo {target} y factor {factor}.",
            "Despeje rigurosamente el parametro del modelo sabiendo el objetivo {target} y factor {factor}.",
        ],
        hints_inverso,
        "Resolucion inversa formal: el parametro despejado es ans = target / factor = {ans}."
    ),
    (
        "T-Hab06-03", "Hab-06", "fill_in_the_blank",
        gen_perturbacion, ver_perturbacion, ("medium", "Analyze"),
        [
            "Evalue la respuesta ante una perturbacion de magnitud {dx} sobre el valor inicial {x}.",
            "Considere el desplazamiento marginal {dx} aplicado al sistema con nivel {x} y determine la respuesta.",
            "Bajo el supuesto de una perturbacion {dx} desde el nivel {x}, calcule el estado final del estimador.",
            "Analice la sensibilidad analitica desde {x} y halle el valor desplazado con variacion {dx}.",
        ],
        hints_perturbacion,
        "Resolucion de perturbacion: el valor perturbado es x + dx = {ans}."
    ),
    (
        "T-Hab06-04", "Hab-06", "fill_in_the_blank",
        gen_frontera, ver_frontera, ("hard", "Evaluate"),
        [
            "Establezca el comportamiento en el punto de frontera sabiendo que el parametro de control es {k}.",
            "En el regimen limite donde el parametro es {k}, evalue la solucion asintotica.",
            "Tomando en cuenta las condiciones de frontera para {k}, halle el valor estacionario.",
            "Verifique la cota analitica extrema cuando la variable de control alcanza {k}.",
        ],
        hints_frontera,
        "Resolucion en la frontera: la solucion extrema es ans = 2*k = {ans}."
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
    v = rng.randint(10, 200)
    v_dict = {"v": v, "d1": v+1, "d2": v+2, "d3": v+3, "d4": v+4, "d5": v+5, "d6": v+6}
    dists = [
        ("D-Hab06-01", "$@d1@$", "Error al estimar sumando uno al parametro observado @v@ en opcion uno."),
        ("D-Hab06-02", "$@d2@$", "Error al estimar sumando dos al parametro observado @v@ en opcion dos."),
        ("D-Hab06-03", "$@d3@$", "Error al estimar sumando tres al parametro observado @v@ en opcion tres."),
        ("D-Hab06-04", "$@d4@$", "Error al estimar sumando cuatro al parametro observado @v@ en opcion cuatro."),
        ("D-Hab06-05", "$@d5@$", "Error al estimar sumando cinco al parametro observado @v@ en opcion cinco."),
        ("D-Hab06-06", "$@d6@$", "Error al estimar sumando seis al parametro observado @v@ en opcion seis."),
    ]
    return (v_dict, "$@v@$", dists)

def ver_hetero(res): return bool(res and isinstance(res.get("vars"), dict) and res.get("correct") == "$@v@$")

hints_h = [
    "Identifique con precision los parametros iniciales del modelo estimado.",
    "Aplique la expresion algebraica formal correspondiente al regimen analizado.",
    "Compruebe la consistencia dimensional y el orden de magnitud del resultado.",
]

TEMPLATES = [
    (
        "T-Hab06-01", "Hab-06", "multiple_choice_7_options",
        gen_hetero, ver_hetero, ("medium", "Apply"),
        [
            "Evalue la funcion heterogenea con parametro {v}.",
            "Para el valor observado {v}, determine el resultado correspondiente.",
            "En el analisis parametrico con entrada {v}, halle el valor.",
            "Determine la magnitud estimada para el parametro {v}.",
            "Calcule la cota analitica del sistema dado el parametro {v}.",
            "Deduzca el comportamiento evaluado para la variable {v}.",
            "Obtenga la estimacion puntual considerando la medicion {v}.",
            "Halle el resultado asintotico para el estado {v}.",
            "Identifique la respuesta calculada a partir de la entrada {v}.",
            "Estime la magnitud resultante empleando el factor {v}.",
            "Establezca el valor cuantitativo asociado a la medicion {v}.",
            "Compute el parametro del modelo bajo la condicion {v}.",
            "Verifique la cota superior del modelo para el dato {v}.",
            "Determine el valor esperado con parametro observado {v}.",
            "Halle la prediccion puntual resultante de {v}.",
        ],
        hints_h,
        "Solucion heterogenea detallada paso a paso evaluando el parametro observado {v}."
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
            min_archetypes=1,
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
    v = rng.randint(10, 200)
    return {
        "vars": {"v": v, "d1": v+1, "d2": v+2, "d3": v+3, "d4": v+4, "d5": v+5, "d6": v+6},
        "correct": str(v),
        "distractors": [
            ("D-Hab06-01", str(v+1), "Error al estimar sumando uno al valor observado @v@ en paso uno."),
            ("D-Hab06-02", str(v+2), "Error al estimar sumando dos al valor observado @v@ en paso dos."),
            ("D-Hab06-03", str(v+3), "Error al estimar sumando tres al valor observado @v@ en paso tres."),
            ("D-Hab06-04", str(v+4), "Error al estimar sumando cuatro al valor observado @v@ en paso cuatro."),
            ("D-Hab06-05", str(v+5), "Error al estimar sumando cinco al valor observado @v@ en paso cinco."),
            ("D-Hab06-06", str(v+6), "Error al estimar sumando seis al valor observado @v@ en paso seis."),
        ],
    }
def ver(r): return bool(r and isinstance(r.get("vars"), dict) and str(r.get("vars", {}).get("v")) == str(r.get("correct")))
hints = [
    "Identifique con precision los parametros iniciales del modelo estimado.",
    "Aplique la expresion algebraica formal correspondiente al regimen analizado.",
    "Compruebe la consistencia dimensional y el orden de magnitud del resultado.",
]
TEMPLATES = [
    ("T-Hab06-01", "Hab-06", "multiple_choice_7_options", gen, ver, ("medium", "Apply"),
     [
         "Calcule la estimación directa del parámetro observado {v}",
         "Determine el valor analítico correspondiente al parámetro {v}",
         "Halle la magnitud estructural derivada de evaluar {v}",
         "Obtenga el resultado numérico fijando la entrada en {v}",
         "Evalúe rigurosamente la expresión base para el valor {v}",
         "Deduzca la cantidad resultante tomando como referencia {v}",
         "Verifique el monto esperado cuando el parámetro vale {v}",
         "Encuentre la solución numérica asociada al dato {v}",
         "Establezca el equilibrio lineal fijando el parámetro {v}",
         "Compute la respuesta formal requerida bajo el nivel {v}",
         "Analice la relación paramétrica usando la variable {v}",
         "Identifique la cuantía final obtenida a partir de {v}",
         "Califique el efecto numérico observado al imponer {v}",
         "Formule el cálculo operativo requerido para el caso {v}",
         "Estime la salida analítica correspondiente al valor {v}",
         "Contraste el resultado derivado tras fijar el parámetro {v}",
     ],
     hints, "Solucion formal detallada paso a paso evaluando el parametro observado {v}.")
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
            min_archetypes=1,
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
        repo_root = Path(__file__).resolve().parents[2]
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

        # Adapt shard_06 source code to Form-B Tri-Band contract
        real_code = real_shard_py.read_text(encoding="utf-8")
        # Replace 2-tuple distractors in generator functions with 3-tuples containing dynamic rationales
        adapted_code = real_code.replace(
            '("D-Hab06-01", r"H = @d1@"),',
            '("D-Hab06-01", r"H = @d1@", "Error al estimar el contraste con varianza muestral @v_ls@ en paso uno."),'
        ).replace(
            '("D-Hab06-02", r"H = @d2@"),',
            '("D-Hab06-02", r"H = @d2@", "Error al estimar el contraste con varianza muestral @v_ls@ en paso dos."),'
        ).replace(
            '("D-Hab06-03", r"H = @d3@"),',
            '("D-Hab06-03", r"H = @d3@", "Error al estimar el contraste con varianza muestral @v_ls@ en paso tres."),'
        ).replace(
            '("D-Hab06-04", r"H = @d4@"),',
            '("D-Hab06-04", r"H = @d4@", "Error al estimar el contraste con varianza muestral @v_ls@ en paso cuatro."),'
        ).replace(
            '("D-Hab06-05", r"H = @d5@"),',
            '("D-Hab06-05", r"H = @d5@", "Error al estimar el contraste con varianza muestral @v_ls@ en paso cinco."),'
        ).replace(
            '("D-Hab06-06", r"H = @d6@"),',
            '("D-Hab06-06", r"H = @d6@", "Error al estimar el contraste con varianza muestral @v_ls@ en paso seis."),'
        ).replace(
            "return abs(ans - expected) < 1e-3",
            'return abs(ans - expected) < 1e-3 and res.get("correct") == r"H = @ans@"'
        )

        # Replace TEMPLATES with Form-B 9-tuples
        fb_templates_str = '''
hints_h06_1 = [
    "Identifique con precision los parametros del modelo salarial estimado.",
    "Aplique la expresion formal del estadistico univariado bajo exogeneidad.",
    "Compruebe la consistencia dimensional del contraste y el orden de magnitud.",
]
hints_h06_2 = [
    "Considere el sesgo de atenuacion provocado por la fiabilidad observada q.",
    "Relacione la estimacion atenuada MCO con las varianzas de ambos estimadores.",
    "Compute la razon analitica del contraste de Hausman univariado resultante.",
]
hints_h06_3 = [
    "Analice como se modifica el contraste ante una perturbacion en la medicion.",
    "Sustituya las varianzas V_LS y V_IV perturbadas en el denominador del estadistico.",
    "Valide el signo positivo de la diferencia de varianzas bajo el nuevo regimen.",
]
hints_h06_4 = [
    "Examine el limite teorico cuando la fiabilidad tiende hacia su cota maxima.",
    "Compare las estimaciones b_LS y b_IV y sus varianzas respectivas en frontera.",
    "Determine el valor asintotico final del estadistico de contraste de Hausman.",
]

TEMPLATES = [
    ("T-Hab06-01", "Hab-06", "multiple_choice_7_options", gen_directo_hab06, ver_directo_hab06, ("easy", "Apply"), [
        r"Enfoque Directo: En un modelo salarial con datos de gemelos donde b_LS = @b_ls@, b_IV = @b_iv@, V_LS = @v_ls@, V_IV = @v_iv@, y ratio de fiabilidad q = @q@, calcule el estadistico de Hausman H:",
        r"A partir de estimaciones directas con datos de gemelos con b_LS = @b_ls@, b_IV = @b_iv@, varianzas V_LS = @v_ls@, V_IV = @v_iv@, y q = @q@, halle el valor de H:",
        r"Para contrastar frontalmente la presencia de endogeneidad en gemelos con b_LS = @b_ls@, b_IV = @b_iv@, V_LS = @v_ls@, V_IV = @v_iv@ y q = @q@, determine el estadistico H:",
        r"Bajo la hipotesis nula de exogeneidad en el modelo de gemelos con estimadores b_LS = @b_ls@, b_IV = @b_iv@, V_LS = @v_ls@, V_IV = @v_iv@ y q = @q@, compute el estadistico H:",
    ], hints_h06_1, r"El estadistico de Hausman univariado directo calculado paso a paso es H = @ans@."),
    ("T-Hab06-02", "Hab-06", "multiple_choice_7_options", gen_directo_hab06, ver_directo_hab06, ("medium", "Apply"), [
        r"A partir de una estimacion MCO atenuada b_LS = @b_ls@, b_IV = @b_iv@, V_LS = @v_ls@, V_IV = @v_iv@ y fiabilidad observada q = @q@ en datos de gemelos, calcule el estadistico H:",
        r"Diagnostico inverso: Sabiendo que el sesgo de atenuacion reduce el coeficiente con b_LS = @b_ls@, b_IV = @b_iv@, V_LS = @v_ls@, V_IV = @v_iv@ y fiabilidad q = @q@, halle el estadistico H:",
        r"Despeje analiticamente el efecto causal con b_LS = @b_ls@, b_IV = @b_iv@, varianzas V_LS = @v_ls@, V_IV = @v_iv@ y fiabilidad q = @q@, compute H:",
        r"En el modelo de gemelos con fiabilidad q = @q@, b_LS = @b_ls@, b_IV = @b_iv@, V_LS = @v_ls@ y V_IV = @v_iv@, obtenga el estadistico H:",
    ], hints_h06_2, r"El estadistico de Hausman univariado inverso despejado paso a paso es H = @ans@."),
    ("T-Hab06-03", "Hab-06", "multiple_choice_7_options", gen_directo_hab06, ver_directo_hab06, ("medium", "Analyze"), [
        r"Sensibilidad: Si el ratio de fiabilidad es q = @q@ con b_LS = @b_ls@, b_IV = @b_iv@ y varianzas V_LS = @v_ls@, V_IV = @v_iv@, determine H:",
        r"Analisis perturbado: Evaluando una perturbacion marginal en q = @q@ con b_LS = @b_ls@, b_IV = @b_iv@, V_LS = @v_ls@ y V_IV = @v_iv@, calcule H:",
        r"Estudio de perturbacion: Ante un cambio en la medicion q = @q@ partiendo de b_LS = @b_ls@, b_IV = @b_iv@, V_LS = @v_ls@ y V_IV = @v_iv@, halle H:",
        r"Impacto de perturbacion: Con variacion en q = @q@ bajo b_LS = @b_ls@, b_IV = @b_iv@, V_LS = @v_ls@ y V_IV = @v_iv@, determine H:",
    ], hints_h06_3, r"El estadistico de Hausman univariado bajo perturbacion marginal es H = @ans@."),
    ("T-Hab06-04", "Hab-06", "multiple_choice_7_options", gen_directo_hab06, ver_directo_hab06, ("hard", "Evaluate"), [
        r"Frontera: En el limite teorico de medicion con q = @q@ donde b_LS = @b_ls@, V_LS = @v_ls@ y b_IV = @b_iv@, V_IV = @v_iv@, halle H:",
        r"Regimen de frontera: Si q = @q@, b_LS = @b_ls@, b_IV = @b_iv@ y las varianzas son V_LS = @v_ls@ y V_IV = @v_iv@, determine el estadistico de Hausman H:",
        r"Caso frontera extrema: Cuando la fiabilidad alcanza q = @q@ con b_LS = @b_ls@, b_IV = @b_iv@, V_LS = @v_ls@ y V_IV = @v_iv@, calcule el contraste H:",
        r"Condicion asintotica de frontera: Con q = @q@, b_LS = @b_ls@, b_IV = @b_iv@, V_LS = @v_ls@ y V_IV = @v_iv@, deduzca H:",
    ], hints_h06_4, r"El estadistico de Hausman univariado en la frontera teorica resulta H = @ans@."),
]
'''
        # Splice TEMPLATES into adapted code
        tpl_idx = adapted_code.find("TEMPLATES = [")
        if tpl_idx != -1:
            adapted_code = adapted_code[:tpl_idx] + fb_templates_str
        target_shard_py.write_text(adapted_code, encoding="utf-8")

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
            min_archetypes=1,
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


class TestStructuredErrorCountAndThresholdDirectives:
    """Verifies Stream 1B requirements:
    1. error_count (1..5) and has_syntax_error: False persisted in compile_<shard>.json & receipt JSON,
       including [UMBRAL < 6 (N/5 errores)] directive.
    2. error_count (>= 6) persisted in state and receipt, including [UMBRAL >= 6 (N errores)] directive.
    3. Python SyntaxError in shard_data.py sets has_syntax_error: True and error_count: 1.
    4. render_compact_aggregated_errors strictly <= max_output_lines (<= 28 default).
    """

    def test_state_and_receipt_persist_error_count_and_syntax_flag_under_threshold(self, tmp_path: Path):
        """Under 1 to 5 consolidated errors across 50 seeds, compile_shard records error_count in [1, 5],
        has_syntax_error=False, and includes [UMBRAL < 6 ...] directive.
        """
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard06(tmp_path)
        shard_py = shards_dir / "shard_06_data.py"

        # Template that references undeclared variable {missing_var} in stem across all seeds
        shard_code = '''
import random
def gen(rng):
    v = rng.randint(10, 50)
    return {
        "vars": {"v": v, "d1": v+1, "d2": v+2, "d3": v+3, "d4": v+4, "d5": v+5, "d6": v+6},
        "correct": str(v),
        "distractors": [
            ("D-Hab06-01", str(v+1), "Error al computar sumando uno al valor observado @v@ en paso uno."),
            ("D-Hab06-02", str(v+2), "Error al computar sumando dos al valor observado @v@ en paso dos."),
            ("D-Hab06-03", str(v+3), "Error al computar sumando tres al valor observado @v@ en paso tres."),
            ("D-Hab06-04", str(v+4), "Error al computar sumando cuatro al valor observado @v@ en paso cuatro."),
            ("D-Hab06-05", str(v+5), "Error al computar sumando cinco al valor observado @v@ en paso cinco."),
            ("D-Hab06-06", str(v+6), "Error al computar sumando seis al valor observado @v@ en paso seis."),
        ],
    }
def ver(r): return bool(r and str(r.get("vars", {}).get("v")) == str(r.get("correct")))
hints = [
    "Identifique con precision los parametros iniciales del modelo estimado.",
    "Aplique la expresion algebraica formal correspondiente al regimen analizado.",
    "Compruebe la consistencia dimensional y el orden de magnitud del resultado.",
]
TEMPLATES = [
    ("T-Hab06-01", "Hab-06", "multiple_choice_7_options", gen, ver, ("medium", "Apply"),
     ["Stem referencing {missing_var} and {v}", "Stem B referencing {missing_var} and {v}", "Stem C referencing {missing_var} and {v}", "Stem D referencing {missing_var} and {v}"],
     hints, "Solucion formal detallada paso a paso evaluando el parametro observado {v}.")
]
'''
        shard_py.write_text(shard_code, encoding="utf-8")
        receipt_file = shards_dir / "shard_06.json"

        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_06",
            strict=True,
            seeds=50,
            output_path=receipt_file,
            cta_path=cta_file,
            min_archetypes=1,
        )
        assert not success
        assert len(errors) > 0

        # Verify .check_attempts/compile_shard_06.json
        state_file = work_dir / ".check_attempts" / "compile_shard_06.json"
        assert state_file.is_file()
        state_data = json.loads(state_file.read_text(encoding="utf-8"))
        assert state_data["has_syntax_error"] is False
        assert 1 <= state_data["error_count"] < 6

        # Verify receipt JSON
        assert receipt_file.is_file()
        receipt_data = json.loads(receipt_file.read_text(encoding="utf-8"))
        assert receipt_data["compiled_status"] == "FAIL"
        assert receipt_data["has_syntax_error"] is False
        assert 1 <= receipt_data["error_count"] < 6
        assert state_data["error_count"] == receipt_data["error_count"]

        # Verify report directive
        err_report = errors[0]
        assert f"[UMBRAL < 6 ({receipt_data['error_count']}/5 errores)]" in err_report
        assert "Usa edit_file" in err_report and ("write_file(Overwrite=True)" in err_report or "PROHIBIDO write_file completo" in err_report)

        # Also verify that 50 duplicate seed errors consolidate to hunk_count == 1
        multi_seed_errors = [
            DiagnosticError(
                f"Error on seed {s}",
                rule_tag="R-20: SINTAXIS / LLAVES",
                competency="Hab-06",
                template="T-Hab06-01",
                cause="Llaves '{missing_var}' no declaradas",
                actions=["Declarar missing_var"],
            )
            for s in range(50)
        ]
        assert count_distinct_shard_error_hunks(multi_seed_errors) == 1
        rep_single = render_compact_aggregated_errors(multi_seed_errors)
        assert "[UMBRAL < 6 (1/5 errores)]" in rep_single

    def test_state_and_receipt_persist_error_count_over_threshold(self, tmp_path: Path):
        """With >= 6 distinct consolidated errors, error_count is >= 6 and directive is [UMBRAL >= 6 ...]."""
        # Test directly via render_compact_aggregated_errors and count_distinct_shard_error_hunks
        diag_errors = []
        for i in range(7):
            diag_errors.append(
                DiagnosticError(
                    f"Error {i}",
                    rule_tag=f"R-{i+1:02d}: RULE_{i+1}",
                    competency="Hab-06",
                    template=f"T-Hab06-{i+1:02d}",
                    item_id=f"item_{i}",
                    field_name=f"field_{i}",
                    snippet=f"broken_{i}",
                    cause=f"Causa específica del error {i}",
                    actions=[f"Acción para resolver {i}"],
                    lines=[i + 10],
                    file_path=str(tmp_path / "work" / "templates" / "Hab-06.json"),
                )
            )

        hunk_count = count_distinct_shard_error_hunks(diag_errors)
        assert hunk_count == 7

        report = render_compact_aggregated_errors(diag_errors, max_output_lines=28)
        assert "[UMBRAL >= 6 (7 errores)]" in report
        assert "Usa write_file modular en shard_fixes/<CID>.py (1-2 comps) o write_file(Overwrite=True) completo." in report

        # Test end-to-end via compile_shard with 6 distinct templates failing
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard06(tmp_path / "e2e_over")
        shard_py = shards_dir / "shard_06_data.py"

        # Shard with 6 separate templates each failing with a unique missing variable
        templates_defs = []
        for idx in range(6):
            templates_defs.append(f"""
def gen_{idx}(rng):
    v = rng.randint(10, 50)
    return {{
        "vars": {{"v": v, "d1": v+1, "d2": v+2, "d3": v+3, "d4": v+4, "d5": v+5, "d6": v+6}},
        "correct": str(v),
        "distractors": [
            ("D-Hab06-01", str(v+1), "Error al computar con valor @v@ en paso uno."),
            ("D-Hab06-02", str(v+2), "Error al computar con valor @v@ en paso dos."),
            ("D-Hab06-03", str(v+3), "Error al computar con valor @v@ en paso tres."),
            ("D-Hab06-04", str(v+4), "Error al computar con valor @v@ en paso cuatro."),
            ("D-Hab06-05", str(v+5), "Error al computar con valor @v@ en paso cinco."),
            ("D-Hab06-06", str(v+6), "Error al computar con valor @v@ en paso seis."),
        ],
    }}
def ver_{idx}(r): return bool(r and str(r.get("vars", {{}}).get("v")) == str(r.get("correct")))
""")
        shard_code = "import random\n" + "\n".join(templates_defs) + "\nhints = ['Pista uno con suficiente longitud formal.', 'Pista dos con suficiente longitud formal.', 'Pista tres con suficiente longitud formal.']\nTEMPLATES = [\n"
        for idx in range(6):
            shard_code += f"""    ("T-Hab06-{idx+1:02d}", "Hab-06", "multiple_choice_7_options", gen_{idx}, ver_{idx}, ("medium", "Apply"),
     ["Stem {idx} with {{unbound_var_{idx}}} and {{v}}", "Stem B {idx} with {{unbound_var_{idx}}}", "Stem C {idx} with {{unbound_var_{idx}}}", "Stem D {idx} with {{unbound_var_{idx}}}"],
     hints, "Sol"),\n"""
        shard_code += "]\n"

        shard_py.write_text(shard_code, encoding="utf-8")
        receipt_file = shards_dir / "shard_06.json"

        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_06",
            strict=True,
            seeds=10,
            output_path=receipt_file,
            cta_path=cta_file,
            min_archetypes=1,
        )
        assert not success

        state_file = work_dir / ".check_attempts" / "compile_shard_06.json"
        assert state_file.is_file()
        state_data = json.loads(state_file.read_text(encoding="utf-8"))
        assert state_data["has_syntax_error"] is False
        assert state_data["error_count"] >= 6

        receipt_data = json.loads(receipt_file.read_text(encoding="utf-8"))
        assert receipt_data["has_syntax_error"] is False
        assert receipt_data["error_count"] >= 6
        assert f"[UMBRAL >= 6 ({receipt_data['error_count']} errores)]" in errors[0]

    def test_state_records_syntax_error_flag_on_python_syntax_error(self, tmp_path: Path):
        """A Python SyntaxError in shard_XX_data.py sets has_syntax_error=True and error_count=1."""
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard06(tmp_path)
        shard_py = shards_dir / "shard_06_data.py"

        # Deliberate syntax error: def without closing paren
        broken_syntax_code = "def broken_syntax(rng:\n    return {}\n"
        shard_py.write_text(broken_syntax_code, encoding="utf-8")
        receipt_file = shards_dir / "shard_06.json"

        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_06",
            strict=True,
            output_path=receipt_file,
            cta_path=cta_file,
        )
        assert not success
        assert len(errors) > 0

        # State must record has_syntax_error = True and error_count = 1
        state_file = work_dir / ".check_attempts" / "compile_shard_06.json"
        assert state_file.is_file()
        state_data = json.loads(state_file.read_text(encoding="utf-8"))
        assert state_data["has_syntax_error"] is True
        assert state_data["error_count"] == 1

        # Receipt must also record has_syntax_error = True and error_count = 1
        assert receipt_file.is_file()
        receipt_data = json.loads(receipt_file.read_text(encoding="utf-8"))
        assert receipt_data["compiled_status"] == "FAIL"
        assert receipt_data["has_syntax_error"] is True
        assert receipt_data["error_count"] == 1

    def test_render_compact_aggregated_errors_never_exceeds_max_output_lines(self, tmp_path: Path):
        """render_compact_aggregated_errors strictly preserves <= max_output_lines (<= 28 default)
        across 1, 5, 20, 50, and 100 errors, always ending with the threshold directive.
        """
        for err_count in [1, 5, 10, 25, 50, 100]:
            errors = []
            for i in range(err_count):
                errors.append(
                    DiagnosticError(
                        f"Error msg {i}",
                        rule_tag=f"R-{(i % 8) + 1:02d}: RULE_{(i % 8) + 1}",
                        competency=f"Hab-{(i % 3) + 1:02d}",
                        template=f"T-Hab-{(i % 3) + 1:02d}",
                        item_id=f"item_{i}",
                        field_name="stem",
                        snippet=f"code_{i}",
                        cause=f"Cause description for error {i} with details",
                        actions=["Action to take"],
                        lines=[i + 1],
                        file_path=str(tmp_path / f"template_{(i % 3) + 1}.json"),
                    )
                )

            report = render_compact_aggregated_errors(errors, max_output_lines=28)
            report_lines = report.splitlines()
            assert len(report_lines) <= 28, f"Failed for {err_count} errors: got {len(report_lines)} lines > 28"

            # Must contain the directive line
            assert any("[UMBRAL " in line for line in report_lines), f"Missing UMBRAL directive for {err_count} errors"
            if err_count < 6:
                assert any(f"[UMBRAL < 6 ({err_count}/5 errores)]" in line for line in report_lines)
            else:
                assert any("[UMBRAL >= 6" in line for line in report_lines)


class TestMilestone3FourArchetypeEnforcement:
    """Enforces Milestone 3 requirements: minimum 4 disjoint archetypes (tuples) per competency in TEMPLATES."""

    def test_milestone3_min_archetypes_rejects_single_tuple_even_with_4_stem_variants(self, tmp_path: Path):
        """Simulates shard_09_data.py and shard_19_data.py: 1 single tuple with 4 stem_variants inside.
        When min_archetypes=4 (or manifest has min_archetypes: 4), compile_shard must fail with [M3-ARCHETYPES],
        persisting error_count >= 1 and has_syntax_error: False in .check_attempts/compile_<shard>.json.
        """
        work_dir, shards_dir, _, cta_file, manifest_file = _setup_workspace_shard06(tmp_path)
        shard_py = shards_dir / "shard_06_data.py"

        single_tuple_code = '''"""Single tuple with 4 stem variants inside."""
import random

def gen_single(rng):
    base = rng.randint(20, 80)
    ans = base * 2
    return {
        "vars": {
            "base": base, "ans": ans,
            "d1": ans - 1, "d2": ans + 1, "d3": ans + 2,
            "d4": ans + 3, "d5": ans + 4, "d6": ans + 5,
        },
        "correct": r"$@ans@$",
        "distractors": [
            ("D-Hab06-01", r"$@d1@$", "Error al computar con base @base@ en paso uno."),
            ("D-Hab06-02", r"$@d2@$", "Error al computar con base @base@ en paso dos."),
            ("D-Hab06-03", r"$@d3@$", "Error al computar con base @base@ en paso tres."),
            ("D-Hab06-04", r"$@d4@$", "Error al computar con base @base@ en paso cuatro."),
            ("D-Hab06-05", r"$@d5@$", "Error al computar con base @base@ en paso cinco."),
            ("D-Hab06-06", r"$@d6@$", "Error al computar con base @base@ en paso seis."),
        ],
    }

def ver_single(res):
    return bool(res and isinstance(res.get("vars"), dict) and res.get("correct") == r"$@ans@$")

hints_s = [
    "Identifique con precision los parametros iniciales del modelo estimado.",
    "Aplique la expresion algebraica formal correspondiente al regimen analizado.",
    "Compruebe la consistencia dimensional y el orden de magnitud del resultado.",
]

TEMPLATES = [
    (
        "T-Hab06-01", "Hab-06", "multiple_choice_7_options",
        gen_single, ver_single, ("medium", "Apply"),
        [
            "Calcule el valor directo con base {base}.",
            "A partir de base {base}, determine el estimador lineal.",
            "Para el parametro base {base}, evalue el valor directo.",
            "Determine la estimacion directa correspondiente dado {base}.",
        ],
        hints_s,
        "Resolucion directa formal: el estimador es ans = 2 * base = {ans}."
    ),
]
'''
        shard_py.write_text(single_tuple_code, encoding="utf-8")
        receipt_file = shards_dir / "shard_06.json"

        # Case A: Passed via min_archetypes=4 parameter
        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_06",
            strict=True,
            seeds=10,
            output_path=receipt_file,
            cta_path=cta_file,
            min_archetypes=4,
        )
        assert not success
        assert len(errors) > 0
        assert "[M3-ARCHETYPES]" in errors[0]
        assert "define solo 1" in errors[0]

        state_file = work_dir / ".check_attempts" / "compile_shard_06.json"
        assert state_file.is_file()
        state_data = json.loads(state_file.read_text(encoding="utf-8"))
        assert state_data["has_syntax_error"] is False
        assert state_data["error_count"] >= 1

        assert receipt_file.is_file()
        receipt_data = json.loads(receipt_file.read_text(encoding="utf-8"))
        assert receipt_data["compiled_status"] == "FAIL"
        assert receipt_data["has_syntax_error"] is False
        assert receipt_data["error_count"] >= 1

    def test_milestone3_min_archetypes_rejects_4_cloned_identical_tuples(self, tmp_path: Path):
        """Repeating 4 cloned identical tuples (same stem and same generator) fails with [M3-ARCHETYPES]."""
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard06(tmp_path)
        shard_py = shards_dir / "shard_06_data.py"

        cloned_code = '''"""4 Cloned identical tuples for Hab-06."""
import random

def gen_cloned(rng):
    base = rng.randint(20, 80)
    ans = base * 2
    return {
        "vars": {
            "base": base, "ans": ans,
            "d1": ans - 1, "d2": ans + 1, "d3": ans + 2,
            "d4": ans + 3, "d5": ans + 4, "d6": ans + 5,
        },
        "correct": r"$@ans@$",
        "distractors": [
            ("D-Hab06-01", r"$@d1@$", "Error al computar con base @base@ en paso uno."),
            ("D-Hab06-02", r"$@d2@$", "Error al computar con base @base@ en paso dos."),
            ("D-Hab06-03", r"$@d3@$", "Error al computar con base @base@ en paso tres."),
            ("D-Hab06-04", r"$@d4@$", "Error al computar con base @base@ en paso cuatro."),
            ("D-Hab06-05", r"$@d5@$", "Error al computar con base @base@ en paso cinco."),
            ("D-Hab06-06", r"$@d6@$", "Error al computar con base @base@ en paso seis."),
        ],
    }

def ver_cloned(res):
    return bool(res and isinstance(res.get("vars"), dict) and res.get("correct") == r"$@ans@$")

hints_cloned = [
    "Identifique con precision los parametros iniciales del modelo estimado.",
    "Aplique la expresion algebraica formal correspondiente al regimen analizado.",
    "Compruebe la consistencia dimensional y el orden de magnitud del resultado.",
]

stems_cloned = [
    "Calcule el valor clonado con base {base}.",
    "Determine la respuesta clonada para base {base}.",
    "Evalue la cantidad estimada correspondiente a base {base}.",
]

TEMPLATES = [
    ("T-Hab06-01", "Hab-06", "multiple_choice_7_options", gen_cloned, ver_cloned, ("easy", "Apply"), stems_cloned, hints_cloned, "Resolucion formal: {ans}."),
    ("T-Hab06-02", "Hab-06", "multiple_choice_7_options", gen_cloned, ver_cloned, ("medium", "Apply"), stems_cloned, hints_cloned, "Resolucion formal: {ans}."),
    ("T-Hab06-03", "Hab-06", "multiple_choice_7_options", gen_cloned, ver_cloned, ("medium", "Analyze"), stems_cloned, hints_cloned, "Resolucion formal: {ans}."),
    ("T-Hab06-04", "Hab-06", "multiple_choice_7_options", gen_cloned, ver_cloned, ("hard", "Evaluate"), stems_cloned, hints_cloned, "Resolucion formal: {ans}."),
]
'''
        shard_py.write_text(cloned_code, encoding="utf-8")

        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_06",
            strict=True,
            seeds=10,
            cta_path=cta_file,
            min_archetypes=4,
        )
        assert not success
        assert len(errors) > 0
        assert "[M3-ARCHETYPES]" in errors[0]
        assert "repite el mismo enunciado" in errors[0] or "clones" in errors[0]

    def test_milestone3_min_archetypes_passes_with_compact_shared_helper_pattern(self, tmp_path: Path):
        """Compact shared helper pattern:
        def _gen_c01(rng, arch):
        + gen_c01_1..4
        + 4 tuples of 9 elements with [] in position 7 and without 10th hints element.
        Verifies [+] PASS with min_archetypes=4, compiling into C-01.json with target_misconceptions
        and hints auto-populated from cta.json.
        """
        work_dir = tmp_path / "work_c01"
        shards_dir = work_dir / "shards"
        templates_dir = work_dir / "templates"
        shards_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)

        cta_payload = {
            "competencies": [
                {
                    "id": "C-01",
                    "name": "Modelos Lineales Paramétricos",
                    "type": "skill",
                    "distractors": [
                        {"id": "D-C01-01", "remediation_hint": "Considere el error cuadrático medio residual."},
                        {"id": "D-C01-02", "remediation_hint": "Verifique la independencia de los residuos estimados."},
                        {"id": "D-C01-03", "remediation_hint": "Revise el orden de la matriz de covarianza."},
                        {"id": "D-C01-04", "remediation_hint": "Compruebe la normalización de la varianza condicional."},
                        {"id": "D-C01-05", "remediation_hint": "Calcule la suma de cuadrados explicada por el modelo."},
                        {"id": "D-C01-06", "remediation_hint": "Verifique la significancia estadística del estadístico F."},
                    ],
                }
            ]
        }
        cta_file = work_dir / "cta.json"
        cta_file.write_text(json.dumps(cta_payload, indent=2, ensure_ascii=False), encoding="utf-8")

        manifest_payload = {
            "min_archetypes": 4,  # Configured globally in manifest
            "shards": [
                {
                    "shard_id": "shard_01",
                    "competency_ids": ["C-01"],
                    "shard_data_path": str((shards_dir / "shard_01_data.py").resolve().as_posix()),
                    "templates_dir": str(templates_dir.resolve().as_posix()),
                    "competencies": [
                        {
                            "id": "C-01",
                            "name": "Modelos Lineales Paramétricos",
                            "type": "skill",
                            "distractors": cta_payload["competencies"][0]["distractors"],
                        }
                    ],
                }
            ]
        }
        manifest_file = shards_dir / "pre_shard_manifest.json"
        manifest_file.write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8")

        shard_py = shards_dir / "shard_01_data.py"
        compact_code = '''"""Compact 4-archetype implementation using shared helper _gen_c01(rng, arch)."""
import random

def _gen_c01(rng, arch):
    n = rng.randint(20, 200)
    if arch == 1:
        ans = n + 10
        rats = [
            "Calculo aditivo incorrecto al operar con parametro @n@ en paso inicial.",
            "Desplazamiento positivo erroneo al evaluar valor base @n@ del modelo.",
            "Error de escala acumulado sobre el parametro @n@ del modelo lineal.",
            "Ajuste residual equivocado aplicado sobre parametro @n@ evaluado.",
            "Inversion de signo en el desplazamiento lineal de @n@ evaluado.",
        ]
        d_vals = [ans - 2, ans + 2, ans + 4, ans + 6, ans + 8]
        opts = [
            {"value": "El estimador directo lineal suma diez unidades al parametro @n@ dando @ans@.", "is_correct": True},
            {"value": "La estimacion aditiva para base @n@ es exactamente @ans@.", "is_correct": True},
        ]
        opts += [
            {"value": f"$@d{i}@$", "is_correct": False, "distractor_id": f"D-C01-0{i}", "error_rationale": rat}
            for i, rat in enumerate(rats, 1)
        ]
        return {
            "vars": {"n": n, "ans": ans, **{f"d{i}": d for i, d in enumerate(d_vals, 1)}},
            "options": opts,
        }
    elif arch == 2:
        ans = n * 2
        d5 = n * 4
        return {
            "vars": {"n": n, "ans": ans, "d5": d5},
            "correct": str(ans),
            "ds": [("D-C01-05", str(d5), "Sesgo sistematico en combinacion lineal multiplicando @n@ por cuatro hacia @d5@.")],
        }
    elif arch == 3:
        ans = n + 5
        d6 = n - 5
        return {
            "vars": {"n": n, "ans": ans, "d6": d6},
            "correct": str(ans),
            "ds": [("D-C01-06", str(d6), "Inversion indebida de signo al restar cinco unidades sobre parametro base @n@ dando @d6@.")],
        }
    else:  # arch == 4
        ans = n * n + 1
        return {
            "vars": {"n": n, "ans": ans},
            "correct": str(ans),
        }

def gen_c01_1(rng): return _gen_c01(rng, 1)
def gen_c01_2(rng): return _gen_c01(rng, 2)
def gen_c01_3(rng): return _gen_c01(rng, 3)
def gen_c01_4(rng): return _gen_c01(rng, 4)

def ver_c01_1(res):
    if not isinstance(res, dict):
        return False
    v = res.get("vars", {})
    if v.get("ans") != v.get("n", 0) + 10:
        return False
    opts = res.get("options", [])
    exp_t = {
        "El estimador directo lineal suma diez unidades al parametro @n@ dando @ans@.",
        "La estimacion aditiva para base @n@ es exactamente @ans@.",
    }
    exp_f = {f"$@d{i}@$": f"D-C01-0{i}" for i in range(1, 6)}
    t_opts = [o for o in opts if o.get("is_correct") is True]
    f_opts = [o for o in opts if o.get("is_correct") is False]
    return (
        len(t_opts) == 2
        and {o.get("value") for o in t_opts} == exp_t
        and len(f_opts) == 5
        and all(
            o.get("value") in exp_f
            and o.get("distractor_id") == exp_f[o.get("value")]
            and len(str(o.get("error_rationale") or "")) >= 20
            for o in f_opts
        )
    )
def ver_c01_2(res): return bool(res and isinstance(res.get("vars"), dict) and str(res.get("correct")) == str(res["vars"]["ans"]) and res["vars"]["ans"] == res["vars"]["n"] * 2)
def ver_c01_3(res): return bool(res and isinstance(res.get("vars"), dict) and str(res.get("correct")) == str(res["vars"]["ans"]) and res["vars"]["ans"] == res["vars"]["n"] + 5)
def ver_c01_4(res): return bool(res and isinstance(res.get("vars"), dict) and str(res.get("correct")) == str(res["vars"]["ans"]) and res["vars"]["ans"] == res["vars"]["n"] * res["vars"]["n"] + 1)

stem_c01_1 = [
    "Calcule la estimacion directa del modelo lineal para parametro base @n@.",
    "Determine la estimacion directa del modelo lineal con parametro @n@.",
    "Obtenga la estimacion directa del modelo lineal en funcion de @n@.",
    "Halle la estimacion directa del modelo lineal segun el parametro @n@.",
    "Calcule el valor directo del modelo lineal considerando la base @n@.",
]
stem_c01_2 = [
    "Deduzca el factor inverso del modelo lineal con base @n@.",
    "Calcule el factor inverso del modelo lineal para muestra de tamano @n@.",
    "Determine el factor inverso en el modelo lineal con parametro @n@.",
    "Halle el factor inverso del modelo lineal en base a @n@.",
    "Obtenga la razon inversa correspondiente al parametro @n@.",
]
stem_c01_3 = [
    "Determine la respuesta bajo perturbacion aditiva con base @n@.",
    "Calcule el resultado bajo perturbacion aditiva para base @n@.",
    "Obtenga la respuesta del modelo ante perturbacion aditiva con parametro @n@.",
    "Halle el valor desplazado por perturbacion aditiva en @n@.",
    "Evalue el impacto de la perturbacion aditiva sobre base @n@.",
]
stem_c01_4 = [
    "Evalue el comportamiento cuadratico en el regimen frontera con parametro de escala @n@.",
    "Determine el valor cuadratico en el regimen frontera para parametro de escala @n@.",
    "Calcule el resultado cuadratico en la frontera del regimen con parametro @n@.",
    "Halle la cota cuadratica extrema del regimen considerando parametro @n@.",
    "Obtenga el valor cuadratico limite en la frontera del regimen con parametro @n@.",
]

hints_1 = [
    "Considere primero la definicion operacional directa del modelo lineal.",
    "Aplique la transformacion aditiva correspondiente sumando diez unidades.",
    "Verifique el valor final sustituyendo el parametro base evaluado.",
]
hints_2 = [
    "Identifique el parametro base antes de aplicar el factor inverso.",
    "Multiplique por dos el parametro observado del modelo lineal.",
    "Compruebe la consistencia duplicada del resultado en el caso inverso.",
]
hints_3 = [
    "Determine el nivel inicial previo a la perturbacion aditiva.",
    "Agregue cinco unidades al parametro de base especificado en el modelo.",
    "Confirme que la variacion neta corresponda a la respuesta abierta.",
]
hints_4 = [
    "Evalúe la variable de escala elevada al cuadrado en el limite del dominio analizado.",
    "Sume la unidad al cuadrado del parametro de escala en el regimen frontera.",
    "Valide que el resultado entero coincida con la cota cuadratica extrema calculada.",
]

TEMPLATES = [
    (
        "T-C01-01", "C-01", "multiple_select",
        gen_c01_1, ver_c01_1, ("easy", "Apply"),
        stem_c01_1, hints_1,
        "Resolucion directa formal: el estimador es ans = n + 10 = @ans@."
    ),
    (
        "T-C01-02", "C-01", "fill_in_the_blank",
        gen_c01_2, ver_c01_2, ("medium", "Apply"),
        stem_c01_2, hints_2,
        "Resolucion inversa formal: el parametro es ans = n * 2 = @ans@."
    ),
    (
        "T-C01-03", "C-01", "fill_in_the_blank",
        gen_c01_3, ver_c01_3, ("medium", "Analyze"),
        stem_c01_3, hints_3,
        "Resolucion de perturbacion: el valor perturbado es ans = n + 5 = @ans@."
    ),
    (
        "T-C01-04", "C-01", "fill_in_the_blank",
        gen_c01_4, ver_c01_4, ("hard", "Evaluate"),
        stem_c01_4, hints_4,
        "Resolucion en la frontera: la cota cuadratica extrema es ans = n*n + 1 = @ans@."
    ),
]
'''
        shard_py.write_text(compact_code, encoding="utf-8")
        receipt_file = shards_dir / "shard_01.json"

        # Manifest has "min_archetypes": 4 -> eff_min_arch must be 4
        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            seeds=50,
            output_path=receipt_file,
            cta_path=cta_file,
            manifest_path=manifest_file,
        )
        assert success, f"Expected compile_shard to PASS, got errors: {errors}"
        assert len(errors) == 0

        # Verify C-01.json generated and containing 4 templates
        out_json = templates_dir / "C-01.json"
        assert out_json.is_file(), f"Expected template file {out_json} to exist"
        data = json.loads(out_json.read_text(encoding="utf-8"))
        assert "templates" in data
        assert len(data["templates"]) == 4

        # Verify auto-population of target_misconceptions and hints from cta.json
        expected_dids = ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"]
        for idx, tpl in enumerate(data["templates"]):
            if tpl.get("question_type") == "multiple_choice_7_options":
                assert tpl.get("target_misconceptions") == expected_dids, f"Template {idx} missing auto-populated target_misconceptions"
                assert tpl.get("distractor_ids") == expected_dids
            hints = tpl.get("hints", [])
            assert len(hints) >= 3, f"Template {idx} has < 3 hints: {hints}"
            assert all(isinstance(h, str) and len(h.strip()) > 10 for h in hints)
            assert len(tpl.get("stem_variants", [])) >= 3

        # Verify receipt JSON records PASS
        assert receipt_file.is_file()
        receipt_data = json.loads(receipt_file.read_text(encoding="utf-8"))
        assert receipt_data["compiled_status"] == "PASS"
