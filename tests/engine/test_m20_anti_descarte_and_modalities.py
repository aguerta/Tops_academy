"""Milestone 20 Backend Certification Suite:
- Reforma Anti-Descarte (TPL-D3 decoupled from MC7, M20-MC7-CAP, M20-ACTIVE-QUOTA)
- Shift-Left proof_compiler (topological DAG + SymPy + fallacies)
- Shift-Left adversarial_generator (find_fallacy + counterexample witness AST check)
- Full assembly, invariants, src/validator, and QA evaluator across all 6 Bloom Superior modalities + FIB ds.
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
C2C_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
QA_DIR = REPO_ROOT / ".agents" / "skills" / "course-qa-evaluator" / "scripts"
SRC_DIR = REPO_ROOT / "src"

for p in (C2C_DIR, QA_DIR, SRC_DIR, REPO_ROOT):
    p_str = str(p)
    if p_str not in sys.path:
        sys.path.insert(0, p_str)

from check_templates import check_templates_file_or_dir
from compile_cta import compile_cta
from compile_shard import compile_shard
from engine.adversarial_generator import compile_and_verify_adversarial
from engine.assemble import assemble_question
from engine.invariants import check_instance_invariants
from engine.proof_compiler import compile_and_verify_proof_dag
from standardized_audit_engine import run_full_audit
from validator.core import validate_course_content


def _build_minimal_cta(
    work_dir: Path,
    cid: str = "Hab-20",
    is_skill: bool = True,
    recommended_modalities: list[str] | None = None,
) -> Path:
    shards_dir = work_dir / "shards"
    templates_dir = work_dir / "templates"
    shards_dir.mkdir(parents=True, exist_ok=True)
    templates_dir.mkdir(parents=True, exist_ok=True)

    pre_cta = {
        "course_id": "m20_unit_course",
        "title": "Curso M20 Unitario",
        "files": [{"doc": "manual.pdf", "file_index": 0, "total_pages": 20, "valid_page_range": [1, 20]}],
    }
    (work_dir / "pre_cta_manifest.json").write_text(json.dumps(pre_cta), encoding="utf-8")

    comp_type = "skill" if is_skill else "concept"
    d_entries = "\n".join(
        f'            ("Trampa {i}", r"$x_{i}$", r"$x^2$", r"$y_{i}$", "Revisar minuciosamente el error conceptual numero {i} y verificar la formula analitica antes de responder.", "Paso {i}."), '
        for i in range(1, 7)
    )
    assump_block = '        [("A-Hab20-01", r"Regularidad analitica del dominio sobre $x$", r"Ignorar las condiciones del dominio invalida el estimador.")],' if is_skill else "        [],"
    eff_rec_mods = ["MC7", "FIB"] if recommended_modalities is None else recommended_modalities
    rec_block = f"\n        {repr(eff_rec_mods)},"
    cta_code = f'''
CTA_CONTRACT_VERSION = 2
COURSE_ID = "m20_unit_course"
COURSE_TITLE = "Curso M20 Unitario"
COMPETENCIES = [
    (
        "{comp_type}",
        "{cid}",
        "Competencia M20 de Prueba",
        r"Relacion analitica $f(x)=x^2$ evaluada parametricamente en dominios reales con precision.",
        "Analyze",
        "manual.pdf",
        1,
        [],
        [
{d_entries}
        ],
{assump_block}{rec_block}
    ),
]
'''
    cta_py = work_dir / "cta_data.py"
    cta_py.write_text(cta_code, encoding="utf-8")
    ok_cta, _, cta_errs, _ = compile_cta(cta_py, work_dir, require_assumptions=False)
    assert ok_cta, f"compile_cta failed: {cta_errs}"

    cta_json_path = work_dir / "cta.json"
    cta_json = json.loads(cta_json_path.read_text(encoding="utf-8"))
    comp_entry = cta_json["competencies"][0]
    for idx, d in enumerate(comp_entry["distractors"], start=1):
        d["id"] = f"D-Hab20-{idx:02d}"
    for idx, a in enumerate(comp_entry.get("assumptions") or [], start=1):
        a["id"] = f"A-Hab20-{idx:02d}"
    cta_json_path.write_text(json.dumps(cta_json, indent=2, ensure_ascii=False), encoding="utf-8")
    manifest = {
        "total_competencies": 1,
        "total_shards": 1,
        "shards": [
            {
                "shard_id": "shard_01",
                "shard_index": 0,
                "min_archetypes": 4,
                "competency_ids": [cid],
                "competencies": [comp_entry],
                "shard_data_path": str((shards_dir / "shard_01_data.py").resolve().as_posix()),
                "templates_dir": str(templates_dir.resolve().as_posix()),
            }
        ],
    }
    (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return shards_dir


class TestM20ProofCompiler:
    def test_valid_dag_multiple_topological_orders_and_sympy(self):
        raw_dag = {
            "require_justification": True,
            "justification_bank": ["Suma", "Producto", "Sustitución", "Derivada"],
            "steps": [
                {
                    "id": "S1",
                    "content": r"Sea la aceleración $a = @g@ \cdot \sin(\theta)$.",
                    "justification": "Sustitución",
                },
                {
                    "id": "S2",
                    "content": r"Multiplicamos por masa $@m@$: $F_1 = @m@ \cdot @g@ \cdot \sin(\theta)$.",
                    "justification": "Producto",
                    "sympy_expr": "m * g * sin(theta)",
                    "expected_sympy_expr": "g * m * sin(theta)",
                },
                {
                    "id": "S3",
                    "content": r"Verificamos componente normal $N = @m@ \cdot @g@ \cdot \cos(\theta)$.",
                    "justification": "Sustitución",
                },
                {
                    "id": "S4",
                    "content": r"Concluimos $F_1 = @m@@g@\sin(\theta)$ con $N = @m@@g@\cos(\theta)$.",
                    "justification": "Suma",
                },
                {
                    "id": "F1",
                    "content": r"Asumimos $F = @m@ \cdot @g@ \cdot \cos(\theta)$ sobre la rampa.",
                    "is_fallacy": True,
                    "distractor_id": "D-Hab20-01",
                    "error_rationale": r"Usa coseno para el plano inclinado con masa $@m@$ en vez de seno.",
                },
            ],
            "edges": [["S1", "S2"], ["S1", "S3"], ["S2", "S4"], ["S3", "S4"]],
        }
        compiled, ans = compile_and_verify_proof_dag(
            raw_dag,
            variables={"m": 5, "g": 10},
            rng=random.Random(42),
        )
        assert ans["required_step_ids"] == ["S1", "S2", "S3", "S4"]
        assert sorted(ans["edges"]) == [["S1", "S2"], ["S1", "S3"], ["S2", "S4"], ["S3", "S4"]]
        assert compiled["require_justification"] is True
        assert any(st["is_fallacy"] and st["distractor_id"] == "D-Hab20-01" for st in compiled["steps"])

    def test_cycle_and_sympy_failure_rejected(self):
        cyclic = {
            "steps": [
                {"id": "S1", "content": "Paso 1"},
                {"id": "S2", "content": "Paso 2"},
            ],
            "edges": [["S1", "S2"], ["S2", "S1"]],
        }
        with pytest.raises(ValueError, match="PROOF-DAG-CYCLE"):
            compile_and_verify_proof_dag(cyclic)

        bad_sympy = {
            "steps": [
                {
                    "id": "S1",
                    "content": r"Fuerza incorrecta",
                    "sympy_expr": "m * g * cos(theta)",
                    "expected_sympy_expr": "m * g * sin(theta)",
                },
                {"id": "S2", "content": r"Cierre"},
            ],
            "edges": [["S1", "S2"]],
        }
        with pytest.raises(ValueError, match="PROOF-DAG-SYMPY"):
            compile_and_verify_proof_dag(bad_sympy)


class TestM20AdversarialGenerator:
    def test_find_fallacy_and_counterexample(self):
        raw_fallacy = {
            "mode": "find_fallacy",
            "prompt": r"Identifica el paso inválido en el criterio de segundo orden para $f(x)=x^@p@$:",
            "steps": [
                {"id": "A1", "label": "Paso 1", "content": r"Calculamos $f'(x) = @p@ x^3$ y hallamos $f'(0)=0$."},
                {
                    "id": "A2",
                    "label": "Paso 2",
                    "content": r"Como $f''(0)=0$, concluimos automáticamente un punto silla sin derivadas superiores.",
                    "is_fallacy": True,
                    "distractor_id": "D-Hab20-02",
                    "error_rationale": r"Con exponente par $@p@$, $f''(0)=0$ no basta para concluir silla; requiere derivadas de orden $@p@$.",
                },
            ],
            "reason_options": [
                {"id": "R1", "content": r"El criterio de segunda derivada es inconcluso si $f''(0)=0$.", "is_correct": True},
                {
                    "id": "R2",
                    "content": r"Se omitió dividir entre $@p@$ antes de evaluar $x=0$.",
                    "is_correct": False,
                    "distractor_id": "D-Hab20-03",
                    "error_rationale": r"El fallo con $@p@$ ocurre al aplicar $f''(0)=0$ de manera concluyente, no por un factor constante.",
                },
            ],
        }
        compiled_f, ans_f = compile_and_verify_adversarial(raw_fallacy, variables={"p": 4}, rng=random.Random(42))
        assert compiled_f["mode"] == "find_fallacy"
        assert ans_f == {"mode": "find_fallacy", "fallacy_step_id": "A2", "correct_reason_id": "R1"}

        raw_ce = {
            "mode": "counterexample",
            "prompt": r"Encuentra un entero positivo $n \ge @low@$ que viole la cota $n^2 < 3n$:",
            "inputs": [{"name": "n", "label": "n", "type": "integer", "min": 1, "max": 20}],
            "predicates": [
                {"expr": "n >= @low@", "failure_rationale": r"Debe cumplir $n \ge @low@$."},
                {"expr": "n**2 >= 3*n", "failure_rationale": r"El testigo elegido aún cumple $n^2 < 3n$."},
            ],
            "sample_witness": {"n": 5},
            "non_witness": {"n": 2},
        }
        compiled_ce, ans_ce = compile_and_verify_adversarial(raw_ce, variables={"low": 3}, rng=random.Random(42))
        assert compiled_ce["mode"] == "counterexample"
        assert ans_ce["sample_witness"] == {"n": 5}

        # Bad sample_witness must be rejected at compile time
        bad_ce = dict(raw_ce, sample_witness={"n": 2})
        with pytest.raises(ValueError, match="ADV-WITNESS-INVALID"):
            compile_and_verify_adversarial(bad_ce, variables={"low": 3})


class TestM20AntiDescarteCompilerGates:
    def test_zero_mc7_with_ds_and_bloom_superior_passes_tpl_d3(self, tmp_path: Path):
        """0 MC7 competency covers 6/6 distractors across FIB ds + open_symbolic ds + proof_dag + adversarial_break."""
        work_dir = tmp_path / "work_zero_mc7"
        shards_dir = _build_minimal_cta(
            work_dir,
            cid="Hab-20",
            is_skill=True,
            recommended_modalities=["fill_in_the_blank", "open_symbolic", "proof_dag", "adversarial_break"],
        )

        shard_code = r'''
RATS = {
    "D-Hab20-01": r"Confunde coeficiente positivo con $-@a@$ al operar el parámetro @x@.",
    "D-Hab20-02": r"Omite el exponente cuadrático sobre @a@ dentro de la regla dada.",
    "D-Hab20-03": r"Suma $@a@$ y $@b@$ en vez de aplicar producto con $@k@$ exacto.",
    "D-Hab20-04": r"Invierte el signo en el término de frontera con parámetro $@m@$ dado.",
    "D-Hab20-05": r"Aplica criterio de segunda derivada nula sobre grado par $@p@$ sin derivar más.",
    "D-Hab20-06": r"Desplaza la potencia cuadrática restando $@c@$ de forma impropia.",
}

def gen_1(rng):
    a = rng.randint(2, 15)
    x = rng.randint(3, 18)
    ans = a * x + 1
    return {
        "vars": {"a": a, "x": x, "ans": ans, "d1": -a * x + 1, "d2": a + x + 1},
        "correct": str(ans),
        "ds": [
            ("D-Hab20-01", "@d1@", RATS["D-Hab20-01"]),
            ("D-Hab20-02", "@d2@", RATS["D-Hab20-02"]),
        ],
    }

def ver_1(c, v):
    return str(c).strip() == str(v["a"] * v["x"] + 1)

def gen_2(rng):
    k = rng.randint(2, 25)
    b = rng.randint(1, 15)
    expr = f"{k}*x + {b}"
    return {
        "vars": {"k": k, "b": b, "a": k, "ans": expr},
        "correct": {"expression": expr, "accepted_equivalents": [expr, f"{b} + {k}*x"], "tolerance": 0.001},
        "symbolic_config": {"variables": ["x"]},
        "ds": [
            ("D-Hab20-03", f"({k}+{b})*x", RATS["D-Hab20-03"]),
        ],
    }

def ver_2(c, v):
    raw = c.get("expression", "") if isinstance(c, dict) else str(c)
    s = "".join(raw.split())
    k, b = v["k"], v["b"]
    return s in (f"{k}*x+{b}", f"{b}+{k}*x")

def gen_3(rng):
    m = rng.randint(3, 50)
    c = rng.randint(2, 25)
    return {
        "vars": {"m": m, "c": c, "ans": m * c},
        "proof_dag": {
            "steps": [
                {"id": "S1", "content": r"Partimos de masa $m = @m@$ y factor $c = @c@$."},
                {"id": "S2", "content": r"Calculamos el producto lineal $P = @m@ \cdot @c@ = @ans@$."},
                {"id": "F1", "content": r"Restamos $m - c$ dando $@m@ - @c@$.", "is_fallacy": True, "distractor_id": "D-Hab20-04", "error_rationale": RATS["D-Hab20-04"]},
                {"id": "F2", "content": r"Desplazamos por $-@c@$ fuera de rango.", "is_fallacy": True, "distractor_id": "D-Hab20-06", "error_rationale": RATS["D-Hab20-06"]},
            ],
            "edges": [["S1", "S2"]],
        },
    }

def ver_3(r):
    dag = r.get("proof_dag", {}) if isinstance(r, dict) else {}
    steps = dag.get("steps", [])
    return len([s for s in steps if not s.get("is_fallacy")]) == 2 and len([s for s in steps if s.get("is_fallacy")]) == 2

def gen_4(rng):
    p = rng.choice([4, 6, 8, 10, 12, 14, 16, 18, 20, 22])
    coef = rng.randint(2, 15)
    return {
        "vars": {"p": p, "coef": coef, "ans": coef * p},
        "adversarial_break": {
            "mode": "find_fallacy",
            "prompt": r"Detecta el error en la clasificación de $@coef@ x^{@p@}$ en $x=0$:",
            "steps": [
                {"id": "A1", "label": "Paso 1", "content": r"Evaluamos $f'(x) = @coef@ \cdot @p@ x^{@p@-1}$ en $x=0$, resultando $0$."},
                {"id": "A2", "label": "Paso 2", "content": r"Concluimos punto silla directo solo por obtener $f''(0)=0$ con $p=@p@$ y coeficiente $@coef@$.", "is_fallacy": True, "distractor_id": "D-Hab20-05", "error_rationale": RATS["D-Hab20-05"]},
            ],
        },
    }

def ver_4(r):
    adv = r.get("adversarial_break", {}) if isinstance(r, dict) else {}
    steps = adv.get("steps", [])
    return adv.get("mode") == "find_fallacy" and sum(1 for s in steps if s.get("is_fallacy")) == 1

S1 = [
    r"Dado $a=@a@$ y $x=@x@$, calcule el valor directo $ax + 1$:",
    r"Para $a=@a@$ y $x=@x@$, determine el resultado de $ax + 1$:",
    r"Con los factores $@a@$ y $@x@$, halle la cantidad escalar $ax + 1$:",
    r"Evalúe la expresión afín directa en $@a@$ y $@x@$:",
]
S2 = [
    r"Con pendiente $@k@$ y constante $@b@$, formule la función lineal en $x$:",
    r"Escriba la regla algebraica de pendiente $@k@$ e intercepto $@b@$ en $x$:",
    r"Exprese en términos de $x$ la función lineal con $@k@$ y $@b@$:",
    r"Determine la fórmula simbólica lineal usando $@k@$ y $@b@$ en $x$:",
]
S3 = [
    r"Ordene la derivación formal del producto para masa $m=@m@$ y factor $c=@c@$:",
    r"Construya la prueba deductiva del producto $m \cdot c$ con $m=@m@$ y $c=@c@$:",
    r"Organice los pasos válidos para calcular el producto escalar con $m=@m@$ y $c=@c@$:",
    r"Seleccione y ordene la derivación exacta de $m \cdot c$ usando $m=@m@$ y $c=@c@$:",
]
S4 = [
    r"Analice la prueba sobre $@coef@ x^{@p@}$ en $x=0$ y señale la falacia lógica:",
    r"Localice el paso inválido al clasificar $x=0$ para $@coef@ x^{@p@}$:",
    r"Identifique la inferencia falsa sobre derivadas superiores en $@coef@ x^{@p@}$:",
    r"Encuentre la deducción errónea al evaluar $f''(0)=0$ con $@coef@$ y exponente $@p@$:",
]

H1 = [r"Multiplique primero el coeficiente $@a@$ por $@x@$.", r"Agregue una unidad al producto $@a@@x@$.", r"Verifique la suma aritmética final obtenida."]
H2 = [r"Identifique la pendiente delante de la variable $x$.", r"Sume el término constante positivo al producto.", r"Combine el coeficiente lineal con la constante $@b@$."]
H3 = [r"Comience identificando los parámetros iniciales del sistema.", r"Descarte pasos que resten cantidades fuera de la regla.", r"Culmine el producto lógico tras declarar las variables."]
H4 = [r"Recuerde qué ocurre cuando la segunda derivada se anula.", r"Verifique si un exponente par $@p@$ puede tener mínimo.", r"Revise el paso que afirma conclusión sin orden superior."]

SOL = r"Paso 1: Aplicamos la regla canónica para los parámetros generados (@ans@). Paso 2: Verificamos consistencia sin falacias ni signos invertidos."

TEMPLATES = [
    {"id": "T-Hab-20-01", "cid": "Hab-20", "qtype": "fill_in_the_blank", "archetype": "direct", "band": ("easy", "Apply"), "gen": gen_1, "ver": ver_1, "stem_variants": S1, "hints": H1, "sol": SOL},
    {"id": "T-Hab-20-02", "cid": "Hab-20", "qtype": "open_symbolic", "archetype": "inverse", "band": ("medium", "Apply"), "gen": gen_2, "ver": ver_2, "stem_variants": S2, "hints": H2, "sol": SOL},
    {"id": "T-Hab-20-03", "cid": "Hab-20", "qtype": "proof_dag", "archetype": "perturbation", "band": ("hard", "Analyze"), "gen": gen_3, "ver": ver_3, "stem_variants": S3, "hints": H3, "sol": SOL},
    {"id": "T-Hab-20-04", "cid": "Hab-20", "qtype": "adversarial_break", "archetype": "boundary_or_edge_case", "assumption_id": "A-Hab20-01", "band": ("hard", "Evaluate"), "gen": gen_4, "ver": ver_4, "stem_variants": S4, "hints": H4, "sol": SOL},
]
'''
        shard_py = shards_dir / "shard_01_data.py"
        shard_py.write_text(shard_code, encoding="utf-8")

        ok, errs = compile_shard(work_dir, shard_id="shard_01", strict=True, min_archetypes=4, seeds=20, templates_per_modality=1)
        assert ok, f"0 MC7 shard failed compile_shard: {errs}"
        assert errs == []

        tpl_ok, tpl_errs = check_templates_file_or_dir(work_dir / "templates", work_dir / "cta.json", num_dry_run_seeds=20, strict=True)
        assert tpl_ok and tpl_errs == [], f"0 MC7 failed check_templates: {tpl_errs}"

    def test_flexible_modality_mix_without_rigid_quotas_passes(self, tmp_path: Path):
        """Flexible modality mixes (e.g., 2 MC7 + 2 FIB without rigid quotas) pass compile_shard cleanly with K=2."""
        work_dir = tmp_path / "work_2mc7_flex"
        shards_dir = _build_minimal_cta(work_dir, cid="Hab-20", is_skill=True, recommended_modalities=["MC7", "FIB"])

        shard_code = r'''
RATS = {
    "D-Hab20-01": r"Inviertes el signo del coeficiente lineal antes de multiplicar por @n@.",
    "D-Hab20-02": r"Sumas la constante sin escalar primero la entrada @n@ del modelo.",
    "D-Hab20-03": r"Duplicas el exponente en lugar de mantener dependencia lineal en @n@.",
    "D-Hab20-04": r"Divides entre el parámetro auxiliar en vez de multiplicar por @n@.",
    "D-Hab20-05": r"Omites el término independiente desplazando erróneamente el resultado desde @n@.",
    "D-Hab20-06": r"Evalúas la fórmula con el valor inicial sin incorporar el incremento sobre @n@.",
}

def gen_1(r):
    n, a = r.randint(12, 48), r.randint(3, 9)
    ans = a * n + 5
    ds = [(f"D-Hab20-0{i}", str(ans + i * 4), RATS[f"D-Hab20-0{i}"]) for i in range(1, 7)]
    return {"vars": {"n": n, "a": a, "ans": ans}, "correct": str(ans), "ds": ds}

def gen_2(r):
    n, b = r.randint(15, 65), r.randint(4, 14)
    ans = n * n - b
    ds = [(f"D-Hab20-0{i}", str(ans + i * 5), RATS[f"D-Hab20-0{i}"]) for i in range(1, 7)]
    return {"vars": {"n": n, "b": b, "ans": ans}, "correct": str(ans), "ds": ds}

def gen_3(r):
    n, d = r.randint(10, 50), r.randint(3, 12)
    ans = (n + d) * 3
    return {"vars": {"n": n, "d": d, "ans": ans}, "correct": str(ans)}

def gen_4(r):
    n, c = r.randint(8, 40), r.randint(2, 11)
    ans = (n - c) * 4 + c
    return {"vars": {"n": n, "c": c, "ans": ans}, "correct": str(ans)}

def ver_1(c, v): return str(c).strip() == str(v["a"] * v["n"] + 5)
def ver_2(c, v): return str(c).strip() == str(v["n"] * v["n"] - v["b"])
def ver_3(c, v): return str(c).strip() == str((v["n"] + v["d"]) * 3)
def ver_4(c, v): return str(c).strip() == str((v["n"] - v["c"]) * 4 + v["c"])

H1 = [r"Identifica primero la pendiente @a@ y el término @n@.", r"Multiplica @a@ por @n@ antes de sumar cinco.", r"Comprueba el entero positivo final obtenido."]
H2 = [r"Eleva al cuadrado el argumento @n@ inicial.", r"Reste el desplazamiento constante @b@ después.", r"Verifica que el valor supere el cuadrado previo."]
H3 = [r"Suma primero la perturbación @d@ al argumento @n@.", r"Multiplica la suma total por factor tres.", r"Confirma aritméticamente el entero final."]
H4 = [r"Calcula la diferencia frontera @n@ menos @c@.", r"Escala esa diferencia por cuatro y suma @c@.", r"Revisa el producto límite antes de enviarlo."]

S1 = [
    r"Calcula la respuesta directa $f(@n@) = @a@(@n@) + 5$:",
    r"Dado $@n@$ y pendiente $@a@$, evalúa $@a@ \cdot @n@ + 5$:",
    r"Obtén el valor lineal directo con coeficiente $@a@$ en $@n@$:",
    r"Determina $y = @a@x + 5$ evaluando en $x = @n@$:",
]
S2 = [
    r"Invierte la relación cuadrática hallando $@n@^2 - @b@$:",
    r"Con argumento $@n@$ y resta $@b@$, calcula la diferencia cuadrática:",
    r"Determina el valor inverso restando $@b@$ al cuadrado de $@n@$:",
    r"Resuelve $@n@^2 - @b@$ para los parámetros dados:",
]
S3 = [
    r"Bajo perturbación $+@d@$ sobre $@n@$, evalúa $3(@n@ + @d@)$:",
    r"Desplaza la entrada $@n@$ en $@d@$ unidades y triplica el total:",
    r"Si la entrada sube en $@d@$ desde $@n@$, halle el triple:",
    r"Calcula la respuesta perturbada multiplicando $(@n@ + @d@)$ por tres:",
]
S4 = [
    r"En frontera con desplazamiento $@c@$, evalúa $4(@n@ - @c@) + @c@$:",
    r"Para el caso borde dado por $@n@$ y $@c@$, calcula $4(@n@-@c@)+@c@$:",
    r"Aplica la regla límite con brecha $@n@ - @c@$ escalada por cuatro:",
    r"Halla el valor extremo de $4(@n@ - @c@) + @c@$:",
]
SOL = r"Paso 1: Identificamos el parámetro @n@ de la instancia y su regla algebraica específica. Paso 2: Calculamos el entero exacto @ans@ sin omitir términos."

TEMPLATES = [
    {"id": "T-Hab-20-01", "cid": "Hab-20", "qtype": "MC7", "archetype": "direct", "band": ("easy", "Apply"), "gen": gen_1, "ver": ver_1, "stem_variants": S1, "hints": H1, "sol": SOL, "rats": RATS},
    {"id": "T-Hab-20-02", "cid": "Hab-20", "qtype": "MC7", "archetype": "inverse", "band": ("medium", "Apply"), "gen": gen_2, "ver": ver_2, "stem_variants": S2, "hints": H2, "sol": SOL, "rats": RATS},
    {"id": "T-Hab-20-03", "cid": "Hab-20", "qtype": "FIB", "archetype": "perturbation", "band": ("hard", "Analyze"), "gen": gen_3, "ver": ver_3, "stem_variants": S3, "hints": H3, "sol": SOL},
    {"id": "T-Hab-20-04", "cid": "Hab-20", "qtype": "FIB", "archetype": "boundary_or_edge_case", "assumption_id": "A-Hab20-01", "band": ("hard", "Evaluate"), "gen": gen_4, "ver": ver_4, "stem_variants": S4, "hints": H4, "sol": SOL},
]
'''
        (shards_dir / "shard_01_data.py").write_text(shard_code, encoding="utf-8")
        ok, errs = compile_shard(work_dir, shard_id="shard_01", strict=True, min_archetypes=4, seeds=20, fail_total=True)
        assert ok, f"Flexible mix should pass without hardcoded MC7/active quotas: {errs}"

    def test_cta_architect_recommended_modalities_enforced(self, tmp_path: Path):
        """When CTA Architect sets recommended_modalities, unauthorized types fail [CTA-MODALITY-PLAN] while matching K=2 passes."""
        work_bad = tmp_path / "work_cta_plan_bad"
        shards_bad = _build_minimal_cta(
            work_bad,
            cid="Hab-20",
            is_skill=True,
            recommended_modalities=["invariant_canvas", "open_symbolic"],
        )
        shard_fib_code = r'''
RATS = {
    "D-Hab20-01": r"Inviertes el signo del coeficiente lineal antes de multiplicar por @n@.",
    "D-Hab20-02": r"Sumas la constante sin escalar primero la entrada @n@ del modelo.",
    "D-Hab20-03": r"Duplicas el exponente en lugar de mantener dependencia lineal en @n@.",
    "D-Hab20-04": r"Divides entre el parámetro auxiliar en vez de multiplicar por @n@.",
    "D-Hab20-05": r"Omites el término independiente desplazando erróneamente el resultado desde @n@.",
    "D-Hab20-06": r"Evalúas la fórmula con el valor inicial sin incorporar el incremento sobre @n@.",
}
def gen_1(r):
    n, a = r.randint(12, 48), r.randint(3, 9)
    ans = a * n + 5
    ds = [(f"D-Hab20-0{i}", str(ans + i * 4), RATS[f"D-Hab20-0{i}"]) for i in range(1, 7)]
    return {"vars": {"n": n, "a": a, "ans": ans}, "correct": str(ans), "ds": ds}
def gen_2(r):
    n, b = r.randint(15, 65), r.randint(4, 14)
    ans = n * n - b
    ds = [(f"D-Hab20-0{i}", str(ans + i * 5), RATS[f"D-Hab20-0{i}"]) for i in range(1, 7)]
    return {"vars": {"n": n, "b": b, "ans": ans}, "correct": str(ans), "ds": ds}
def gen_3(r):
    n, d = r.randint(10, 50), r.randint(3, 12)
    ans = (n + d) * 3
    return {"vars": {"n": n, "d": d, "ans": ans}, "correct": str(ans)}
def gen_4(r):
    n, c = r.randint(8, 40), r.randint(2, 11)
    ans = (n - c) * 4 + c
    return {"vars": {"n": n, "c": c, "ans": ans}, "correct": str(ans)}
def ver_1(c, v): return str(c).strip() == str(v["a"] * v["n"] + 5)
def ver_2(c, v): return str(c).strip() == str(v["n"] * v["n"] - v["b"])
def ver_3(c, v): return str(c).strip() == str((v["n"] + v["d"]) * 3)
def ver_4(c, v): return str(c).strip() == str((v["n"] - v["c"]) * 4 + v["c"])
H1 = [r"Identifica primero la pendiente @a@ y el término @n@.", r"Multiplica @a@ por @n@ antes de sumar cinco.", r"Comprueba el entero positivo final obtenido."]
H2 = [r"Eleva al cuadrado el argumento @n@ inicial.", r"Reste el desplazamiento constante @b@ después.", r"Verifica que el valor supere el cuadrado previo."]
H3 = [r"Suma primero la perturbación @d@ al argumento @n@.", r"Multiplica la suma total por factor tres.", r"Confirma aritméticamente el entero final."]
H4 = [r"Calcula la diferencia frontera @n@ menos @c@.", r"Escala esa diferencia por cuatro y suma @c@.", r"Revisa el producto límite antes de enviarlo."]
S1 = [r"Calcula la respuesta directa $f(@n@) = @a@(@n@) + 5$:", r"Dado $@n@$ y pendiente $@a@$, evalúa $@a@ \cdot @n@ + 5$:", r"Obtén el valor lineal directo con coeficiente $@a@$ en $@n@$:", r"Determina $y = @a@x + 5$ evaluando en $x = @n@$:"]
S2 = [r"Invierte la relación cuadrática hallando $@n@^2 - @b@$:", r"Con argumento $@n@$ y resta $@b@$, calcula la diferencia cuadrática:", r"Determina el valor inverso restando $@b@$ al cuadrado de $@n@$:", r"Resuelve $@n@^2 - @b@$ para los parámetros dados:"]
S3 = [r"Bajo perturbación $+@d@$ sobre $@n@$, evalúa $3(@n@ + @d@)$:", r"Desplaza la entrada $@n@$ en $@d@$ unidades y triplica el total:", r"Si la entrada sube en $@d@$ desde $@n@$, halle el triple:", r"Calcula la respuesta perturbada multiplicando $(@n@ + @d@)$ por tres:"]
S4 = [r"En frontera con desplazamiento $@c@$, evalúa $4(@n@ - @c@) + @c@$:", r"Para el caso borde dado por $@n@$ y $@c@$, calcula $4(@n@-@c@)+@c@$:", r"Aplica la regla límite con brecha $@n@ - @c@$ escalada por cuatro:", r"Halla el valor extremo de $4(@n@ - @c@) + @c@$:"]
SOL = r"Paso 1: Identificamos el parámetro @n@ de la instancia y su regla algebraica específica. Paso 2: Calculamos el entero exacto @ans@ sin omitir términos."
TEMPLATES = [
    {"id": "T-Hab-20-01", "cid": "Hab-20", "qtype": "MC7", "archetype": "direct", "band": ("easy", "Apply"), "gen": gen_1, "ver": ver_1, "stem_variants": S1, "hints": H1, "sol": SOL, "rats": RATS},
    {"id": "T-Hab-20-02", "cid": "Hab-20", "qtype": "MC7", "archetype": "inverse", "band": ("medium", "Apply"), "gen": gen_2, "ver": ver_2, "stem_variants": S2, "hints": H2, "sol": SOL, "rats": RATS},
    {"id": "T-Hab-20-03", "cid": "Hab-20", "qtype": "FIB", "archetype": "perturbation", "band": ("hard", "Analyze"), "gen": gen_3, "ver": ver_3, "stem_variants": S3, "hints": H3, "sol": SOL},
    {"id": "T-Hab-20-04", "cid": "Hab-20", "qtype": "FIB", "archetype": "boundary_or_edge_case", "assumption_id": "A-Hab20-01", "band": ("hard", "Evaluate"), "gen": gen_4, "ver": ver_4, "stem_variants": S4, "hints": H4, "sol": SOL},
]
'''
        (shards_bad / "shard_01_data.py").write_text(shard_fib_code, encoding="utf-8")
        ok_bad, errs_bad = compile_shard(work_bad, shard_id="shard_01", strict=True, min_archetypes=4, seeds=20, fail_total=True)
        assert not ok_bad and "[CTA-MODALITY-PLAN]" in "\n".join(errs_bad)

        work_ok = tmp_path / "work_cta_plan_ok"
        shards_ok = _build_minimal_cta(
            work_ok,
            cid="Hab-20",
            is_skill=True,
            recommended_modalities=["MC7", "FIB"],
        )
        (shards_ok / "shard_01_data.py").write_text(shard_fib_code, encoding="utf-8")
        ok_good, errs_good = compile_shard(work_ok, shard_id="shard_01", strict=True, min_archetypes=4, seeds=20, fail_total=True)
        assert ok_good, f"CTA Architect matching modality plan should pass: {errs_good}"

    def test_invariant_canvas_target_coordinate_leak_rejected(self):
        """Cartesian invariant_canvas questions must reject target coordinates leaked verbatim in stem."""
        base_ic = {
            "mode": "cartesian",
            "x_range": [0, 20],
            "y_range": [0, 30],
            "invariants": [
                {"id": "INV_POS", "kind": "point_coords", "point_id": "pt_kink", "target_x": 5, "target_y": 14, "tolerance": 0.5}
            ],
        }
        leaking_q = {
            "interaction_type": "invariant_canvas",
            "stem": r"Identifique sobre el plano el punto de quiebre $(\bar{x}_1, x_2) = (5, 14)$ con $m = 24$:",
            "hints": ["Calcula m - p1*x_bar.", "Verifica ambos tramos.", "Ubica el vertice resultante."],
            "invariant_canvas": base_ic,
        }
        ok_leak, errs_leak = check_instance_invariants(leaking_q, "invariant_canvas")
        assert not ok_leak and any("leaked verbatim in stem text" in e for e in errs_leak)

        clean_q = {
            **leaking_q,
            "stem": r"Con $m = 24$, $p_1 = 2$, $p_2 = 1$ y descuento desde $\bar{x}_1 = 5$, calcula $x_2^*$ y ubica el vértice:",
        }
        ok_clean, errs_clean = check_instance_invariants(clean_q, "invariant_canvas")
        assert ok_clean, f"Non-leaking canvas stem failed unexpectedly: {errs_clean}"


class TestM20EndToEndAssembleValidateAudit:
    def test_all_six_modalities_plus_fib_ds_assemble_validate_and_audit(self):
        rng = random.Random(42)
        base_tpl = {
            "competency_id": "Hab-20",
            "difficulty": "hard",
            "bloom": "Analyze",
            "stem_variants": ["Resuelve el reactivo paramétrico @x@ con rigor."],
            "hints": [
                "Analiza las condiciones del sistema físico o matemático dado.",
                "Comprueba invariantes fundamentales antes de concluir.",
                "Verifica dimensionalmente la estructura resultante.",
            ],
            "solution": "Paso 1: Identificar variables con @x@. Paso 2: Confirmar invariante de excelencia completo.",
        }

        payloads = [
            (
                "fill_in_the_blank",
                {
                    "vars": {"x": 5, "ans": 25},
                    "correct": "25",
                    "ds": [("D-Hab20-01", "10", r"Multiplica por 2 en vez de elevar $@x@$ al cuadrado.")],
                },
            ),
            (
                "open_symbolic",
                {
                    "vars": {"x": 2},
                    "correct": {"expression": "m*g*sin(theta)", "accepted_equivalents": ["g*m*sin(theta)", "m*g*sin(theta)"], "tolerance": 0.001},
                    "symbolic_config": {"variables": ["m", "g", "theta"], "palette": ["sin", "theta"]},
                    "ds": [("D-Hab20-02", "m*g*cos(theta)", r"Aplica coseno sobre el plano inclinado en vez de componente paralela seno para x=@x@.")],
                },
            ),
            (
                "proof_dag",
                {
                    "vars": {"x": 3},
                    "proof_dag": {
                        "steps": [
                            {"id": "S1", "content": r"Fijamos $k=@x@$."},
                            {"id": "S2", "content": r"Derivamos $f(t)=e^{-@x@t}$."},
                            {"id": "F1", "content": r"Asumimos crecimiento $e^{+@x@t}$.", "is_fallacy": True, "distractor_id": "D-Hab20-03", "error_rationale": r"Invierte el signo exponencial de enfriamiento $-@x@t$."},
                        ],
                        "edges": [["S1", "S2"]],
                    },
                },
            ),
            (
                "adversarial_break",
                {
                    "vars": {"x": 4},
                    "adversarial_break": {
                        "mode": "counterexample",
                        "prompt": r"Halla un entero $n \ge @x@$ con $n^2 > 15$:",
                        "inputs": [{"name": "n", "label": "n", "type": "integer", "min": 1, "max": 20}],
                        "predicates": [{"expr": "n >= @x@ and n**2 > 15", "failure_rationale": r"No satisface $n \ge @x@$ y $n^2 > 15$."}],
                        "sample_witness": {"n": 5},
                    },
                },
            ),
            (
                "unstructured_model",
                {
                    "vars": {"x": 7},
                    "unstructured_model": {
                        "phase1_variables": {
                            "roles": ["parametro_conocido", "incognita", "distractor_irrelevante"],
                            "items": [
                                {"id": "V1", "label": r"Temperatura inicial $T_0$", "correct_role": "parametro_conocido"},
                                {"id": "V2", "label": r"Constante térmica $k$", "correct_role": "incognita"},
                                {"id": "V3", "label": r"Color del recipiente", "correct_role": "distractor_irrelevante", "distractor_id": "D-Hab20-04", "error_rationale": r"Incluye atributo visual irrelevante como variable física para $x=@x@$."},
                            ],
                        },
                        "phase2_assumptions": {
                            "options": [
                                {"id": "A1", "content": r"Temperatura ambiente constante", "is_required": True},
                                {"id": "A2", "content": r"Gradiente infinito instantáneo", "is_required": False, "distractor_id": "D-Hab20-05", "error_rationale": r"Supone equilibrio instantáneo contradiciendo la ley exponencial con $x=@x@$."},
                            ]
                        },
                        "phase3_formulation": {
                            "input_mode": "symbolic",
                            "correct_expression": {"expression": "T_a + (T_0 - T_a)*e^(-k*t)", "accepted_equivalents": ["T_a + (T_0 - T_a)*exp(-k*t)"]},
                        },
                    },
                },
            ),
            (
                "invariant_canvas",
                {
                    "vars": {"x": 10},
                    "invariant_canvas": {
                        "mode": "tree",
                        "interaction_mode": "both",
                        "nodes": [
                            {"id": "N0", "label": "J1", "x": 100, "y": 40, "player": "1"},
                            {"id": "N1", "label": "J2", "x": 60, "y": 140, "player": "2"},
                            {"id": "N2", "label": "J2", "x": 140, "y": 140, "player": "2"},
                        ],
                        "edges": [
                            {"id": "E1", "from": "N0", "to": "N1", "label": "A"},
                            {"id": "E2", "from": "N0", "to": "N2", "label": "B"},
                        ],
                        "tree_invariants": {
                            "required_edges": ["E1"],
                            "required_info_sets": [["N1", "N2"]],
                            "distractor_id": "D-Hab20-06",
                            "edge_error_rationale": r"Selecciona trayectoria subóptima sin conservar conjunto de información con $@x@$ nodos.",
                        },
                    },
                },
            ),
            (
                "concept_matching",
                {
                    "vars": {"x": 2},
                    "concept_matching": {
                        "premises": [
                            {"id": "P1", "content": r"Derivada segunda nula $f''(0)=0$ con orden $@x@$"},
                            {"id": "P2", "content": r"Hessiana indefinida"},
                        ],
                        "targets": [
                            {"id": "T1", "content": r"Criterio inconcluso"},
                            {"id": "T2", "content": r"Punto silla"},
                            {"id": "T3", "content": r"Mínimo global garantizado", "is_distractor": True, "distractor_id": "D-Hab20-01", "error_rationale": r"Confunde indefinición con convexidad estricta bajo parámetro $@x@$."},
                        ],
                        "correct_pairs": {"P1": "T1", "P2": "T2"},
                    },
                },
            ),
        ]

        questions = []
        q_counter = 0
        for s_off in range(5):
            seed_val = 42 + s_off
            for q_idx, (itype, gen_res) in enumerate(payloads, start=1):
                q_counter += 1
                tpl = {**base_tpl, "id": f"T-Hab20-{q_idx:02d}", "interaction_type": itype}
                # Vary var x per seed so stems/ids remain unique across the 35 generated questions
                varied_res = json.loads(json.dumps(gen_res))
                if isinstance(varied_res.get("vars"), dict):
                    varied_res["vars"]["x"] = int(varied_res["vars"].get("x", 2)) + s_off
                if isinstance(varied_res.get("adversarial_break"), dict) and varied_res["adversarial_break"].get("mode") == "counterexample":
                    varied_res["adversarial_break"]["sample_witness"] = {"n": 10 + s_off}
                q = assemble_question(tpl, varied_res, competency_id="Hab-20", question_index=q_counter, seed=seed_val)
                ok_inv, inv_errs = check_instance_invariants(q, itype)
                assert ok_inv, f"Invariants failed for {itype}: {inv_errs}"
                questions.append(q)

        course = {
            "schema_version": "1.0.0",
            "course_id": "m20_test_course",
            "course_title": "Curso M20 Integrado",
            "description": "Curso unitario completo de validacion para todas las modalidades Bloom Superior de Milestone 20.",
            "language": "es",
            "created_at": "2026-11-19T00:00:00Z",
            "competencies": [
                {
                    "id": "Hab-20",
                    "name": "Comp M20",
                    "category": "Skill",
                    "description": "Competencia integral de evaluacion epistemica sin descarte pasivo.",
                }
            ],
            "questions": questions,
        }
        val_res = validate_course_content(json.dumps(course), strict=True)
        assert val_res.is_valid, f"Validator errors: {[e.message for e in val_res.errors]}"

        audit = run_full_audit(course)
        mod = audit["dimension_summaries"]["retrieval_modality_linter"]
        assert mod["fib_count"] == 5
        assert mod["bloom_superior_count"] == 30
        assert mod["active_generation_or_discrimination_pct"] == 100.0
        assert mod["mc7_count"] == 0
