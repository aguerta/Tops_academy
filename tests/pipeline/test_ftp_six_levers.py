"""Tests for the 6 domain-agnostic FTP (First-Time Pass) levers in content-to-course."""

from __future__ import annotations

import ast
import copy
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

import check_templates  # noqa: E402
from compile_shard import compile_shard  # noqa: E402
import dispatch  # noqa: E402
from engine.assemble import assemble_question  # noqa: E402
from engine.c2c_ver import c2c_ver  # noqa: E402
from engine.instantiate import instantiate_competency  # noqa: E402
from engine.sandbox import (  # noqa: E402
    SecurityViolationError,
    execute_template_code,
    execute_verifier_code,
    validate_code_ast,
)
from engine.template_healing import normalize_prose_outside_math  # noqa: E402
import plan_shards  # noqa: E402


def _seed_workspace(
    tmp_path: Path,
    competencies: list[Dict[str, Any]],
    course_id: str = "ftp_test_course",
    min_archetypes: int = 4,
) -> tuple[Path, Path, Path, Path]:
    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    templates_dir = work_dir / "templates"
    shards_dir.mkdir(parents=True, exist_ok=True)
    templates_dir.mkdir(parents=True, exist_ok=True)

    cta_payload = {
        "contract_version": 2,
        "course_id": course_id,
        "title": f"Course {course_id}",
        "competencies": competencies,
    }
    cta_file = work_dir / "cta.json"
    cta_file.write_text(json.dumps(cta_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    pre_cta = {
        "course_id": course_id,
        "cta_mode": "direct",
        "files": [{"doc": "source.pdf", "file_index": 0, "total_pages": 10}],
        "documents": [{"doc_name": "source.pdf", "path": "content/source.pdf"}],
    }
    (work_dir / "pre_cta_manifest.json").write_text(json.dumps(pre_cta, indent=2), encoding="utf-8")

    manifest = {
        "min_archetypes": min_archetypes,
        "templates_per_modality": 1,
        "shards": [
            {
                "shard_id": "shard_01",
                "min_archetypes": min_archetypes,
                "competency_ids": [c["id"] for c in competencies],
                "shard_data_path": str((shards_dir / "shard_01_data.py").resolve().as_posix()),
                "templates_dir": str(templates_dir.resolve().as_posix()),
                "competencies": competencies,
            }
        ],
    }
    (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return work_dir, shards_dir, templates_dir, cta_file


def _base_skill_comp(cid: str = "Hab-01", rec_mods: list[str] | None = None) -> Dict[str, Any]:
    clean = cid.replace("-", "")
    return {
        "id": cid,
        "name": f"Competency {cid}",
        "type": "skill",
        "bloom": "Analyze",
        "recommended_modalities": rec_mods or ["FIB", "open_symbolic", "MS"],
        "assumptions": [
            {
                "id": f"A-{clean}-01",
                "statement_latex": r"Parámetros positivos $a, b > 0$",
                "violation_consequence": "Cambia el signo de la respuesta.",
            }
        ],
        "distractors": [
            {
                "id": f"D-{clean}-{i:02d}",
                "name": f"Distractor {i}",
                "wrong_belief": f"Confusión algebraica tipo {i} distinta del modelo correcto.",
                "remediation_hint": f"Revise la relación operacional {i} usando los coeficientes dados.",
            }
            for i in range(1, 7)
        ],
    }


# =============================================================================
# LEVER 1: Canonical Verifier Helpers (c2c_ver)
# =============================================================================

class TestLever1CanonicalVerifiers:
    def test_numeric_helper(self):
        assert c2c_ver.numeric("3.1416", 3.1416) is True
        assert c2c_ver.numeric(r"$x = 12.500\text{ u}$", 12.5, tol=0.005) is True
        assert c2c_ver.numeric(10, 10.003, tol=0.005) is True
        assert c2c_ver.numeric("10.05", 10.0, tol=0.005) is False
        assert c2c_ver.numeric(None, 10.0) is False
        assert c2c_ver.numeric("", 10.0) is False
        assert c2c_ver.numeric(True, 1) is False
        assert c2c_ver.numeric("nan", 0.0) is False
        assert c2c_ver.numeric("inf", 0.0) is False

    def test_equiv_helper_algebraic_and_transcendental(self):
        assert c2c_ver.equiv("2*(x + 1)", "2*x + 2", variables=["x"]) is True
        assert c2c_ver.equiv("x^2 + 1", "1 + x**2", variables=["x"]) is True
        assert c2c_ver.equiv("exp(x + 1)", "exp(1)*exp(x)", variables=["x"]) is True
        assert c2c_ver.equiv("sqrt(4*x)", "2*sqrt(x)", variables=["x"]) is True
        assert c2c_ver.equiv("log(2*x)", "log(x) + log(2)", variables=["x"]) is True

        assert c2c_ver.equiv("2*x + 3", "2*x + 2", variables=["x"]) is False
        assert c2c_ver.equiv("z + 2*x", "2*x", variables=["x"]) is False
        assert c2c_ver.equiv("__MUTATED__", "2*x", variables=["x"]) is False
        assert c2c_ver.equiv("0 = 1", "2*x", variables=["x"]) is False
        assert c2c_ver.equiv("", "2*x", variables=["x"]) is False

    def test_m20_guard_rejects_all_five_ms_mutations_and_is_readonly(self):
        rats = {
            "D-C01-01": r"Omite el factor $@a@$ al expandir la relación lineal dada.",
            "D-C01-02": r"Invierte el signo de $@b@$ respecto a la ordenada al origen.",
        }
        valid_ms = {
            "vars": {"a": 3, "b": 5},
            "options": [
                {"value": r"$y = @a@x + @b@$", "is_correct": True},
                {"value": r"$y = @b@x + @a@$", "is_correct": True},
                {
                    "value": r"$y = @a@x - @b@$",
                    "is_correct": False,
                    "distractor_id": "D-C01-01",
                    "error_rationale": rats["D-C01-01"],
                },
                {
                    "value": r"$y = x + @b@$",
                    "is_correct": False,
                    "distractor_id": "D-C01-02",
                    "error_rationale": rats["D-C01-02"],
                },
            ],
        }
        assert c2c_ver.m20_guard(valid_ms, rats, "MS") is True

        # mut_a: swap is_correct between true and false
        mut_a = copy.deepcopy(valid_ms)
        mut_a["options"][0]["is_correct"] = False
        mut_a["options"][2]["is_correct"] = True
        assert c2c_ver.m20_guard(mut_a, rats, "MS") is False

        # mut_b: invalid distractor_id
        mut_b = copy.deepcopy(valid_ms)
        mut_b["options"][2]["distractor_id"] = "__INVALID_DID__"
        assert c2c_ver.m20_guard(mut_b, rats, "MS") is False

        # mut_c1: blank error_rationale
        mut_c1 = copy.deepcopy(valid_ms)
        mut_c1["options"][2]["error_rationale"] = ""
        assert c2c_ver.m20_guard(mut_c1, rats, "MS") is False

        # mut_c2: __MUTATED__ content
        mut_c2 = copy.deepcopy(valid_ms)
        mut_c2["options"][0]["value"] = "__MUTATED__"
        assert c2c_ver.m20_guard(mut_c2, rats, "MS") is False

        # mut_c3: false LaTeX equation sentinel
        mut_c3 = copy.deepcopy(valid_ms)
        mut_c3["options"][0]["value"] = "$0 = 1$"
        assert c2c_ver.m20_guard(mut_c3, rats, "MS") is False

        # Read-only proxy checks
        with pytest.raises(AttributeError):
            c2c_ver.numeric = lambda *a: True  # type: ignore[misc]
        with pytest.raises(AttributeError):
            del c2c_ver.numeric  # type: ignore[misc]
        with pytest.raises(AttributeError):
            _ = c2c_ver.__dict__

    def test_m20_guard_supports_all_m20_modalities(self):
        rats = {f"D-C01-0{i}": f"Diagnóstico completo D-C01-0{i} con parámetro @a@ aplicado." for i in range(1, 5)}
        pd_res = {
            "vars": {"a": 2},
            "proof_dag": {
                "steps": [
                    {"id": "S1", "content": "Paso 1 válido"},
                    {"id": "S2", "content": "Paso 2 válido"},
                    {"id": "S3", "content": "Paso 3 válido"},
                    {"id": "F1", "content": "Falacia", "is_fallacy": True, "distractor_id": "D-C01-01", "error_rationale": rats["D-C01-01"]},
                ],
                "edges": [["S1", "S2"], ["S2", "S3"]],
            },
        }
        assert c2c_ver.m20_guard(pd_res, rats, "proof_dag") is True

        adv_res = {
            "vars": {"a": 2},
            "adversarial_break": {
                "mode": "find_fallacy",
                "steps": [
                    {"id": "S1", "content": "Paso 1"},
                    {"id": "S2", "content": "Paso 2"},
                    {"id": "S3", "content": "Fallo", "is_fallacy": True, "distractor_id": "D-C01-01", "error_rationale": rats["D-C01-01"]},
                ],
                "reason_options": [
                    {"id": "R1", "content": "Razón correcta", "is_correct": True},
                    {"id": "R2", "content": "Razón falsa", "is_correct": False, "distractor_id": "D-C01-02", "error_rationale": rats["D-C01-02"]},
                ],
            },
        }
        assert c2c_ver.m20_guard(adv_res, rats, "adversarial_break") is True

        um_res = {
            "vars": {"a": 2},
            "unstructured_model": {
                "phase1_variables": {"prompt": "P1", "roles": ["e"], "items": [{"id": "V1", "label": "X", "correct_role": "e"}]},
                "phase2_assumptions": {"prompt": "P2", "options": [{"id": "A1", "content": "Supuesto", "is_required": True}, {"id": "A2", "content": "Falso", "is_required": False, "distractor_id": "D-C01-03", "error_rationale": rats["D-C01-03"]}]},
                "phase3_formulation": {"prompt": "P3", "input_mode": "symbolic", "correct_expression": {"expression": "2*x"}},
            },
        }
        assert c2c_ver.m20_guard(um_res, rats, "unstructured_model") is True

        cm_res = {
            "vars": {"a": 2},
            "concept_matching": {
                "premises": [{"id": "P1", "content": "Derivada"}],
                "targets": [
                    {"id": "T1", "content": "2"},
                    {"id": "T2", "content": "2x", "is_distractor": True, "distractor_id": "D-C01-04", "error_rationale": rats["D-C01-04"]},
                ],
                "correct_pairs": {"P1": "T1"},
            },
        }
        assert c2c_ver.m20_guard(cm_res, rats, "concept_matching") is True

        ic_res = {
            "vars": {"a": 2},
            "invariant_canvas": {
                "mode": "cartesian",
                "invariants": [{"kind": "point_coords", "point_id": "P1", "target_x": "@a@", "target_y": "4", "distractor_id": "D-C01-01", "error_rationale": rats["D-C01-01"]}],
            },
        }
        assert c2c_ver.m20_guard(ic_res, rats, "invariant_canvas") is True

    def test_sandbox_injection_and_end_to_end_compile_shard(self, tmp_path: Path):
        # Sandbox security: engine.sandbox still banned; c2c_ver available without import
        with pytest.raises(SecurityViolationError):
            validate_code_ast("import engine.sandbox\ndef generate(rng): return {}")
        with pytest.raises(SecurityViolationError):
            validate_code_ast("def verify(r): return c2c_ver.__class__ is not None")

        gen_py = "def generate(rng): return {'vars': {'x': 3}, 'correct': '6'}"
        ver_py = "def verify(c, v): return c2c_ver.numeric(c, v['x'] * 2)"
        res = execute_template_code(gen_py, seed=42, cross_check_py=ver_py)
        assert res["correct"] == "6"
        assert execute_verifier_code(ver_py, res, seed=42) is True

        # End-to-end compile_shard using c2c_ver.numeric, c2c_ver.equiv, and c2c_ver.m20_guard
        comp = _base_skill_comp("Hab-01", ["FIB", "open_symbolic", "MS"])
        work_dir, shards_dir, _, cta_file = _seed_workspace(tmp_path, [comp], min_archetypes=4)
        shard_code = r'''
RATS = {
    "D-Hab01-01": r"Resta $@b@$ al calcular $@a@ \cdot @x@$ en lugar de sumarlo.",
    "D-Hab01-02": r"Omite el intercepto $@b@$ dejando solamente $@a@ \cdot @x@$ sin desplazamiento.",
    "D-Hab01-03": r"Suma $@a@$ y $@b@$ omitiendo multiplicar $@d@$ por $@a@$ en la expansión.",
    "D-Hab01-04": r"Invierte el desplazamiento $@d@$ restando $@a@ \cdot @d@$ de $@b@$.",
    "D-Hab01-05": r"Mantiene $@b@$ constante sin escalar el término $@a@$ por $@d@$.",
    "D-Hab01-06": r"Confunde el signo negativo de $@a@$ cambiando el signo del término $@b@$.",
}

def gen_1(rng):
    a, x, b = rng.randint(3, 12), rng.randint(4, 18), rng.randint(5, 25)
    ans = round(a * x + b / 7.0, 4)
    return {
        "vars": {"a": a, "x": x, "b": b, "ans": ans},
        "correct": str(ans),
        "ds": [
            ("D-Hab01-01", str(round(a * x - b / 7.0, 4)), RATS["D-Hab01-01"]),
            ("D-Hab01-02", str(round(a * x, 4)), RATS["D-Hab01-02"]),
        ],
    }

def ver_1(c, v):
    return c2c_ver.numeric(c, v["a"] * v["x"] + v["b"] / 7.0, tol=0.005)

def gen_2(rng):
    a, b, d = rng.randint(3, 12), rng.randint(12, 28), rng.randint(2, 9)
    c0 = a * d + b
    return {
        "vars": {"a": a, "b": b, "d": d, "c0": c0, "ans": f"{a}x+{c0}"},
        "correct": f"{a}*x+{c0}",
        "accepted_equivalents": [f"{a}*(x+{d})+{b}"],
        "variables": ["x"],
        "symbolic_config": {"variables": ["x"], "palette": ["+", "*", "(", ")"], "placeholder": "3*x+11"},
        "ds": [("D-Hab01-03", f"{a}*x+{b}", RATS["D-Hab01-03"])],
    }

def ver_2(c, v):
    return c2c_ver.equiv(c, f"{v['a']}*(x+{v['d']})+{v['b']}", variables=["x"])

def gen_3(rng):
    a, d, b = rng.randint(3, 12), rng.randint(2, 9), rng.randint(12, 28)
    ad = a * d
    return {
        "vars": {"a": a, "d": d, "b": b, "ad": ad},
        "options": [
            {"value": r"$f(@d@)-f(0)=@ad@$", "is_correct": True},
            {"value": r"$f(@d@)>f(0)$ con pendiente $@a@$", "is_correct": True},
            {"value": r"$f(@d@)-f(0)>0$", "is_correct": True},
            {"value": r"$f(@d@)-f(0)=@b@$", "is_correct": False, "distractor_id": "D-Hab01-04", "error_rationale": RATS["D-Hab01-04"]},
            {"value": r"$f(@d@)-f(0)=@d@$", "is_correct": False, "distractor_id": "D-Hab01-05", "error_rationale": RATS["D-Hab01-05"]},
        ],
    }

def ver_3(r):
    return c2c_ver.m20_guard(r, RATS, "MS") and r["vars"]["a"] > 0

def gen_4(rng):
    a, x, b = -rng.randint(3, 12), rng.randint(4, 16), rng.randint(10, 28)
    return {
        "vars": {"a": a, "x": x, "b": b},
        "options": [
            {"value": r"$f(@x@)=@a@(@x@)+@b@$", "is_correct": True},
            {"value": r"$f(@x@)<@b@$ con pendiente $@a@$", "is_correct": True},
            {"value": r"$f(@x@)=@a@(@x@)-@b@$", "is_correct": False, "distractor_id": "D-Hab01-06", "error_rationale": RATS["D-Hab01-06"]},
            {"value": r"$f(@x@)=@a@+@b@$", "is_correct": False, "distractor_id": "D-Hab01-02", "error_rationale": RATS["D-Hab01-02"]},
            {"value": r"$f(@x@)=@b@$", "is_correct": False, "distractor_id": "D-Hab01-01", "error_rationale": RATS["D-Hab01-01"]},
        ],
    }

def ver_4(r):
    return c2c_ver.m20_guard(r, RATS, "MS") and r["vars"]["a"] < 0

S1 = [
    r"Evalúe $f(@x@) = @a@x + @b@/7$ para $x=@x@$ (redondee a 4 decimales):",
    r"Determine la imagen $f(@x@)$ en la función afín $f(x) = @a@x + @b@/7$ (redondee a 4 decimales):",
    r"Calcule el valor de $f(x) = @a@x + @b@/7$ en $x = @x@$ (redondee a 4 decimales):",
    r"Obtenga numéricamente $f(@x@)$ para la recta $f(t)=@a@t+@b@/7$ (redondee a 4 decimales):",
    r"¿Cuál es el resultado aproximado a 4 decimales de $f(@x@)$ si $f(x)=@a@x+@b@/7$?",
    r"Encuentre la ordenada correspondiente a la abscisa $@x@$ bajo $f(u)=@a@u+@b@/7$ (4 decimales):",
]
S2 = [
    r"Desplace $f(x) = @a@x + @b@$ evaluando la regla algebraica $f(x+@d@)$:",
    r"Exprese en términos de $x$ el polinomio $f(x+@d@)$ cuando $f(t)=@a@t+@b@$:",
    r"Halle la forma simbólica de $f(x+@d@)$ dado $f(x)=@a@x+@b@$:",
    r"Expanda la composición desplazada $f(x+@d@)$ de la recta $f(u)=@a@u+@b@$:",
    r"Simplifique la traslación horizontal $f(x+@d@)$ partiendo de $f(x)=@a@x+@b@$:",
    r"¿Qué expresión lineal en $x$ resulta al sustituir $x+@d@$ en $f(t)=@a@t+@b@$?",
]
S3 = [
    r"Para $f(x)=@a@x+@b@$ con incremento $@d@$ y pendiente positiva $@a@$, seleccione las afirmaciones válidas:",
    r"Dada la recta $f(t)=@a@t+@b@$ (pendiente $@a@$) y paso $@d@$, marque las correctas:",
    r"Analice el cambio $f(@d@)-f(0)$ cuando $f(x)=@a@x+@b@$ con pendiente positiva $@a@$:",
    r"Evalúe propiedades de variación en $@d@$ para la función afín $f(x)=@a@x+@b@$ ($a=@a@$):",
    r"Al comparar $f(@d@)$ contra $f(0)$ en $f(t)=@a@t+@b@$ ($a=@a@$), elija las ciertas:",
    r"Identifique relaciones verdaderas sobre el incremento $f(@d@)-f(0)$ para $f(x)=@a@x+@b@$ ($a=@a@$):",
]
S4 = [
    r"Con pendiente negativa $@a@$ en $f(x)=@a@x+@b@$ evaluada en $x=@x@$, marque las válidas:",
    r"Dado $f(t)=@a@t+@b@$ (pendiente $@a@$) en el punto $t=@x@$, seleccione las proposiciones ciertas:",
    r"Para el caso límite $a=@a@$ en $f(x)=@a@x+@b@$ ($x=@x@$), elija las válidas:",
    r"Verifique cotas de $f(@x@)$ bajo decrecimiento con $a=@a@$ en la recta $@a@x+@b@$:",
    r"¿Qué afirmaciones se cumplen para $f(@x@)$ en la recta decreciente $f(x)=@a@x+@b@$ ($a=@a@$)?",
    r"Contraste los valores de $f(@x@)$ frente a $@b@$ cuando la pendiente es $a=@a@$:",
]
H1 = [
    r"Identifique la pendiente $@a@$ y el término racional $@b@/7$ de la función afín.",
    r"Multiplique $@a@$ por $@x@$ antes de sumar la fracción $@b@/7$.",
    r"Redondee el resultado decimal final a cuatro cifras tras el punto.",
]
H2 = [
    r"Sustituya la variable $t$ por $(x+@d@)$ en toda la regla afín.",
    r"Distribuya el coeficiente $@a@$ sobre ambos sumandos de $(x+@d@)$.",
    r"Agrupe la constante $@a@ \cdot @d@ + @b@$ como término independiente.",
]
H3 = [
    r"Reste $f(0)=@b@$ al evaluar $f(@d@)=@a@(@d@)+@b@$ directamente.",
    r"Observe que el intercepto $@b@$ se cancela por completo en la diferencia.",
    r"Use el signo positivo de $@a@$ para confirmar el crecimiento estricto.",
]
H4 = [
    r"Conserve el signo negativo de $@a@$ al multiplicar por $@x@>0$.",
    r"Compare el producto negativo $@a@ \cdot @x@$ frente al intercepto $@b@$.",
    r"Verifique la desigualdad respecto a la ordenada al origen $@b@$.",
]
SOL1 = r"Paso 1: Sustituya $x=@x@$ en $f(x)=@a@x+@b@/7$. Paso 2: El resultado redondeado a 4 decimales es @ans@."
SOL2 = r"Paso 1: Sustituya $x+@d@$ en $f(x)=@a@x+@b@$. Paso 2: Expanda $@a@(x+@d@)+@b@ = @ans@ = @c0@+@a@x$."
SOL3 = r"Paso 1: Calcule $f(@d@)-f(0)=@a@ \cdot @d@=@ad@>0$. Paso 2: El intercepto $@b@$ se cancela."
SOL4 = r"Paso 1: Como $@a@<0$ y $@x@>0$, $@a@ \cdot @x@ < 0$. Paso 2: Por ello $f(@x@)=@a@(@x@)+@b@ < @b@$."

TEMPLATES = [
    {"id": "T-Hab01-01", "cid": "Hab-01", "qtype": "FIB", "archetype": "direct", "band": ("easy", "Apply"), "gen": gen_1, "ver": ver_1, "stem_variants": S1, "hints": H1, "sol": SOL1, "rats": RATS},
    {"id": "T-Hab01-02", "cid": "Hab-01", "qtype": "open_symbolic", "archetype": "inverse", "band": ("medium", "Analyze"), "gen": gen_2, "ver": ver_2, "stem_variants": S2, "hints": H2, "sol": SOL2, "rats": RATS},
    {"id": "T-Hab01-03", "cid": "Hab-01", "qtype": "MS", "archetype": "perturbation", "band": ("hard", "Analyze"), "gen": gen_3, "ver": ver_3, "stem_variants": S3, "hints": H3, "sol": SOL3},
    {"id": "T-Hab01-04", "cid": "Hab-01", "qtype": "MS", "archetype": "boundary_or_edge_case", "band": ("hard", "Evaluate"), "assumption_id": "A-Hab01-01", "gen": gen_4, "ver": ver_4, "stem_variants": S4, "hints": H4, "sol": SOL4},
]
'''
        (shards_dir / "shard_01_data.py").write_text(shard_code, encoding="utf-8")
        ok, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            seeds=50,
            min_archetypes=4,
            templates_per_modality=1,
        )
        assert ok, f"compile_shard with c2c_ver failed: {errors}"
        assert errors == []


# =============================================================================
# LEVER 2: Read-Only Typed Skeleton in author_XX_data.md + CLI flag
# =============================================================================

class TestLever2TypedSkeleton:
    def test_dispatch_authors_embeds_valid_readonly_skeleton_and_cli_accepts_k(self, tmp_path: Path):
        comp = _base_skill_comp("Hab-01", ["FIB", "open_symbolic", "MS"])
        work_dir, shards_dir, _, cta_file = _seed_workspace(tmp_path, [comp], min_archetypes=4)

        res = dispatch.dispatch_authors(work_dir=work_dir, pointer=True, templates_per_modality=2)
        assert len(res["Subagents"]) == 1

        data_md = (work_dir / "dispatch" / "items" / "author_01_data.md").read_text(encoding="utf-8")
        assert "## 3. ESQUELETO CONTRACTUAL DE REFERENCIA (SOLO LECTURA)" in data_md
        for i in range(1, 7):
            assert f"D-Hab01-0{i}" in data_md

        # Skeleton must be valid Python AST containing NotImplementedError stubs
        import re
        blocks = re.findall(r"```python\s*([\s\S]*?)```", data_md)
        assert blocks, "Expected fenced Python skeleton in author_01_data.md"
        skel_code = blocks[-1]
        ast.parse(skel_code)
        assert "NotImplementedError" in skel_code
        assert "c2c_ver." in skel_code

        # author_01.json must stay compact (does not duplicate Section 3)
        item_json = (work_dir / "dispatch" / "items" / "author_01.json").read_text(encoding="utf-8")
        assert "ESQUELETO CONTRACTUAL DE REFERENCIA" not in item_json

        # Stubbed skeleton must fail compilation if left unimplemented
        (shards_dir / "shard_01_data.py").write_text(skel_code, encoding="utf-8")
        ok, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            seeds=10,
            min_archetypes=4,
            templates_per_modality=2,
        )
        assert ok is False
        assert errors

        # CLI dispatch-authors --templates-per-modality 3 works cleanly
        proc = subprocess.run(
            [
                sys.executable,
                str(SKILL_DIR / "dispatch.py"),
                "dispatch-authors",
                "--work-dir",
                str(work_dir),
                "--templates-per-modality",
                "3",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert proc.returncode == 0, f"CLI failed: {proc.stderr}"


# =============================================================================
# LEVER 3: Stage 4 Stratified Rejection Sampling
# =============================================================================

class TestLever3RejectionSampling:
    def test_rejection_sampling_prevents_key_clumping_while_catching_constant_gen(self):
        skewed_gen = (
            "def generate(rng):\n"
            "    a = rng.randint(1, 5000)\n"
            "    ans = '10' if (a % 3 != 0) else str(100 + a)\n"
            "    return {'vars': {'a': a, 'ans': ans}, 'correct': ans, 'distractors': []}\n"
        )
        ver_ok = "def verify(c, v): return c2c_ver.numeric(c, float(v['ans']), tol=1e-4)"
        tpl_skewed = {
            "id": "T-C01-01",
            "competency_id": "C-01",
            "interaction_type": "fill_in_the_blank",
            "difficulty": "easy",
            "bloom": "Apply",
            "stem": "Calcule el valor asociado al parámetro @a@:",
            "stem_variants": [
                "Calcule el valor asociado al parámetro @a@:",
                "Determine el resultado numérico para @a@:",
                "Halle la salida del sistema con entrada @a@:",
            ],
            "hints": [
                "Evalúe el parámetro entero @a@ paso a paso.",
                "Verifique el módulo de la operación sobre @a@.",
                "Exprese el resultado numérico exacto obtenido.",
            ],
            "solution": "Paso 1: Evaluamos @a@. Paso 2: Resultado final @ans@.",
            "distractor_ids": [],
            "generate_py": skewed_gen,
            "cross_check_py": ver_ok,
        }
        comp = {"id": "C-01", "type": "concept"}
        res = instantiate_competency(comp, [tpl_skewed], quota=20, base_seed=1000)
        assert res["total_generated"] == 20
        q_ids = [q["id"] for q in res["questions"]]
        assert len(set(q_ids)) == 20, "Backfill/rejection must preserve unique question IDs"

        key_10_count = sum(1 for q in res["questions"] if q["correct_answer"]["value"] == "10")
        assert key_10_count <= 4, f"Expected <= 4 (20%) occurrences of '10', got {key_10_count}"

        # Truly constant answer generator still triggers [TPL-STATIC-OPT]
        const_gen = (
            "def generate(rng):\n"
            "    a = rng.randint(1, 5000)\n"
            "    return {'vars': {'a': a, 'ans': '42'}, 'correct': '42', 'distractors': []}\n"
        )
        tpl_const = {**tpl_skewed, "generate_py": const_gen}
        errs = check_templates.check_competency_diversity([tpl_const], comp, num_seeds=50, strict=True)
        assert any("TPL-STATIC-OPT" in e for e in errs), f"Expected TPL-STATIC-OPT, got: {errs}"


# =============================================================================
# LEVER 4 & LEVER 5: Normalizer, Abbreviations, Orphan Vars & Subscript Warning
# =============================================================================

class TestLever4And5ValidationPolish:
    def test_normalize_prose_outside_math_preserves_math_and_ellipses(self):
        raw = "Sea $a..b$  en  $$x +  y$$.  Texto con doble punto..   Sigue ... fin.."
        norm, changes = normalize_prose_outside_math(raw)
        assert "$a..b$" in norm
        assert "$$x +  y$$" in norm
        assert "Sigue ... fin." in norm
        assert ".." not in norm.replace("$a..b$", "").replace("...", "")
        assert "  " not in norm.replace("$$x +  y$$", "")
        assert len(changes) == 2

    def test_abbreviations_double_periods_orphan_vars_and_cosmetic_subscript_pass_clean(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ):
        comp = _base_skill_comp("Hab-01", ["FIB", "MS", "open_symbolic"])
        work_dir, shards_dir, _, _ = _seed_workspace(tmp_path, [comp], min_archetypes=4)
        shard_code = r'''
RATS = {
    "D-Hab01-01": r"Resta $@b@$ al operar con $@a@$ en vez de sumar $@b@$ en $@x@$..",
    "D-Hab01-02": r"Omite $@b@$ conservando únicamente $@a@$ y $@d@$ en la expansión.",
    "D-Hab01-03": r"Suma $@a@$ y $@b@$ directamente antes de operar el incremento positivo $@d@$.",
    "D-Hab01-04": r"Invierte el desplazamiento $@d@$ sobre el factor $@a@$..",
    "D-Hab01-05": r"Mantiene $@b@$ constante sin escalar el término $@a@$ por el valor $@x@$.",
    "D-Hab01-06": r"Invierte signo de $@a@$ respecto a $@b@$ evaluando en $@x@$.",
}

def gen_1(rng):
    a, x, b = rng.randint(3, 12), rng.randint(4, 18), rng.randint(5, 25)
    ans = a * x + b
    return {
        "vars": {"a": a, "x": x, "b": b, "ans": ans, "aux_unused": 99},
        "correct": str(ans),
        "ds": [("D-Hab01-01", str(a * x - b), RATS["D-Hab01-01"])],
    }

def ver_1(c, v):
    return c2c_ver.numeric(c, v["a"] * v["x"] + v["b"], tol=1e-4)

def gen_2(rng):
    a, b, d = rng.randint(3, 12), rng.randint(12, 28), rng.randint(2, 9)
    c0 = a * d + b
    return {
        "vars": {"a": a, "b": b, "d": d, "c0": c0, "ans": f"{a}x+{c0}"},
        "correct": f"{a}*x+{c0}",
        "accepted_equivalents": [f"{a}*(x+{d})+{b}"],
        "variables": ["x"],
        "symbolic_config": {"variables": ["x"], "palette": ["+", "*", "(", ")"], "placeholder": "3*x+11"},
        "ds": [("D-Hab01-02", f"{a}*x+{b}", RATS["D-Hab01-02"])],
    }

def ver_2(c, v):
    return c2c_ver.equiv(c, f"{v['a']}*(x+{v['d']})+{v['b']}", variables=["x"])

def gen_3(rng):
    a, d, b = rng.randint(3, 12), rng.randint(2, 9), rng.randint(12, 28)
    ad = a * d
    return {
        "vars": {"a": a, "d": d, "b": b, "ad": ad},
        "options": [
            {"value": r"$f(@d@)-f(0)=@ad@$", "is_correct": True},
            {"value": r"$f(@d@)>f(0)$ con pendiente $@a@$", "is_correct": True},
            {"value": r"$f(@d@)-f(0)>0$", "is_correct": True},
            {"value": r"$f(@d@)-f(0)=@b@$", "is_correct": False, "distractor_id": "D-Hab01-03", "error_rationale": RATS["D-Hab01-03"]},
            {"value": r"$f(@d@)-f(0)=@d@$", "is_correct": False, "distractor_id": "D-Hab01-04", "error_rationale": RATS["D-Hab01-04"]},
        ],
    }

def ver_3(r):
    return c2c_ver.m20_guard(r, RATS, "MS")

def gen_4(rng):
    a, x, b = -rng.randint(3, 12), rng.randint(4, 16), rng.randint(10, 28)
    return {
        "vars": {"a": a, "x": x, "b": b},
        "options": [
            {"value": r"$f(@x@)=@a@(@x@)+@b@$", "is_correct": True},
            {"value": r"$f(@x@)<@b@$ con pendiente $@a@$", "is_correct": True},
            {"value": r"$f(@x@)=@a@(@x@)-@b@$", "is_correct": False, "distractor_id": "D-Hab01-05", "error_rationale": RATS["D-Hab01-05"]},
            {"value": r"$f(@x@)=@a@+@b@$", "is_correct": False, "distractor_id": "D-Hab01-06", "error_rationale": RATS["D-Hab01-06"]},
            {"value": r"$f(@x@)=@b@$", "is_correct": False, "distractor_id": "D-Hab01-01", "error_rationale": RATS["D-Hab01-01"]},
        ],
    }

def ver_4(r):
    return c2c_ver.m20_guard(r, RATS, "MS")

S1 = [
    r"Evalúe $f(x)=@a@x+@b@$, i.e. calcule $f(@x@)$ en la fig. 1 (aprox. entera) para $X_n$..",
    r"Determine según la ec. afín $f(x)=@a@x+@b@$ (e.g. $x=@x@$) el valor exacto:",
    r"Calcule el valor de $f(x)=@a@x+@b@$ en $x=@x@$ usando la eq. dada:",
    r"Obtenga el valor de la función $f(t)=@a@t+@b@$ evaluada en $t=@x@$:",
    r"¿Cuál es la imagen exacta de $f(@x@)$ para la recta $f(x)=@a@x+@b@$?",
    r"Halle el resultado numérico al sustituir $u=@x@$ en $f(u)=@a@u+@b@$:",
]
S2 = [
    r"Desplace $f(x)=@a@x+@b@$ evaluando $f(x+@d@)$:",
    r"Exprese en $x$ el polinomio $f(x+@d@)$ para $f(t)=@a@t+@b@$:",
    r"Halle simbólicamente $f(x+@d@)$ si $f(x)=@a@x+@b@$:",
    r"Expanda algebraicamente la traslación $f(x+@d@)$ dada la regla $f(x)=@a@x+@b@$:",
    r"Obtenga la forma desarrollada de $f(x+@d@)$ a partir de $f(u)=@a@u+@b@$:",
    r"¿Cómo queda escrita la composición afín $f(x+@d@)$ cuando $f(x)=@a@x+@b@$?",
]
S3 = [
    r"Para $f(x)=@a@x+@b@$ con incremento $@d@$ y pendiente $@a@$, seleccione las afirmaciones válidas:",
    r"Dada la recta $f(t)=@a@t+@b@$ (pendiente $@a@$) y paso $@d@$, marque las correctas:",
    r"Analice el cambio $f(@d@)-f(0)$ cuando $f(x)=@a@x+@b@$ ($a=@a@$):",
    r"Identifique propiedades exactas de la variación en $@d@$ para $f(x)=@a@x+@b@$ ($a=@a@$):",
    r"Al evaluar la diferencia $f(@d@)-f(0)$ con $f(t)=@a@t+@b@$ ($a=@a@$), elija las ciertas:",
    r"Determine cuáles proposiciones describen el incremento $f(@d@)-f(0)$ para $f(x)=@a@x+@b@$ ($a=@a@$):",
]
S4 = [
    r"Con pendiente $a=@a@$ en $f(x)=@a@x+@b@$ evaluada en $x=@x@$, marque las válidas:",
    r"Dado $f(t)=@a@t+@b@$ ($a=@a@$) en $t=@x@$, seleccione las ciertas:",
    r"Para el caso límite $a=@a@$ en $f(x)=@a@x+@b@$ ($x=@x@$), elija las válidas:",
    r"Verifique propiedades de $f(@x@)$ cuando la pendiente es $a=@a@$ en $@a@x+@b@$:",
    r"¿Qué relaciones valen para $f(@x@)$ en la función decreciente $f(x)=@a@x+@b@$ ($a=@a@$)?",
    r"Compare $f(@x@)$ con el intercepto $@b@$ cuando la recta tiene pendiente $a=@a@$:",
]
H1 = [
    r"Identifique la pendiente $@a@$ y el término independiente $@b@$ de la función..",
    r"Multiplique la pendiente $@a@$ por el punto de evaluación $@x@$.",
    r"Sume finalmente el intercepto $@b@$ al producto calculado.",
]
H2 = [
    r"Sustituya la variable independiente por $(x+@d@)$ en $f(x)=@a@x+@b@$.",
    r"Distribuya el coeficiente $@a@$ sobre ambos sumandos del paréntesis.",
    r"Simplifique el término constante resultante $@a@ \cdot @d@ + @b@$.",
]
H3 = [
    r"Plantee la resta $f(@d@)-f(0)$ cancelando el intercepto $@b@$.",
    r"Multiplique la pendiente $@a@$ por el incremento positivo $@d@$.",
    r"Confirme el signo estricto del incremento cuando $@a@>0$.",
]
H4 = [
    r"Evalúe primero el producto $@a@ \cdot @x@$ conservando el signo negativo.",
    r"Compare el valor resultante $f(@x@)$ respecto al intercepto $@b@$.",
    r"Verifique cuál opción altera indebidamente el signo de $@b@$.",
]
SOL1 = r"Paso 1: Sustituya $@a@$, $@x@$ y $@b@$. Paso 2: Obtenga la respuesta final $@ans@$ exacto.."
SOL2 = r"Paso 1: Sustituya $x+@d@$ en $@a@x+@b@$. Paso 2: Expanda a $@ans@ = @c0@+@a@x$.."
SOL3 = r"Paso 1: Reste $f(0)=@b@$ de $f(@d@)=@a@(@d@)+@b@$. Paso 2: Queda $@ad@>0$.."
SOL4 = r"Paso 1: Con $@a@<0$ y $@x@>0$, $@a@ \cdot @x@<0$. Paso 2: Luego $f(@x@)<@b@$.."

TEMPLATES = [
    {"id": "T-Hab01-01", "cid": "Hab-01", "qtype": "FIB", "archetype": "direct", "band": ("easy", "Apply"), "gen": gen_1, "ver": ver_1, "stem_variants": S1, "hints": H1, "sol": SOL1, "rats": RATS},
    {"id": "T-Hab01-02", "cid": "Hab-01", "qtype": "open_symbolic", "archetype": "inverse", "band": ("medium", "Analyze"), "gen": gen_2, "ver": ver_2, "stem_variants": S2, "hints": H2, "sol": SOL2, "rats": RATS},
    {"id": "T-Hab01-03", "cid": "Hab-01", "qtype": "MS", "archetype": "perturbation", "band": ("hard", "Analyze"), "gen": gen_3, "ver": ver_3, "stem_variants": S3, "hints": H3, "sol": SOL3},
    {"id": "T-Hab01-04", "cid": "Hab-01", "qtype": "MS", "archetype": "boundary_or_edge_case", "band": ("hard", "Evaluate"), "assumption_id": "A-Hab01-01", "gen": gen_4, "ver": ver_4, "stem_variants": S4, "hints": H4, "sol": SOL4},
]
'''
        (shards_dir / "shard_01_data.py").write_text(shard_code, encoding="utf-8")
        ok, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            seeds=50,
            min_archetypes=4,
            templates_per_modality=1,
        )
        captured = capsys.readouterr()
        assert ok, f"Expected clean compile after polish/whitelist/warning downgrade, got: {errors}"
        assert errors == []
        assert "WARNING: [TPL-STEM-SYMBOL-PARITY]" in captured.err
        assert "INFO: [AUTO-FIXED] [PROSE-NORM]" in captured.err
        assert "INFO: [AUTO-FIXED] [TPL-ORPHAN-VARS]" in captured.err

        # Assembled question also polishes dynamic rationales with '..'
        tpl_missing_var = {
            "id": "T-BAD-01",
            "interaction_type": "fill_in_the_blank",
            "stem": "Calcule @a@ + @b@",
            "stem_variants": ["Calcule @a@ + @b@", "Determine la suma sin variables"],
        }
        parity_errs = check_templates._check_stem_variant_parity(tpl_missing_var)
        assert parity_errs, "Missing @var@ placeholder in non-MS stem_variant must still hard-fail"

        q = assemble_question(
            template={
                "id": "T-Hab01-03",
                "interaction_type": "multiple_select",
                "stem": "Marque opciones..",
                "hints": ["Pista uno con doble punto..", "Pista dos de verificación.", "Pista tres de cierre."],
                "solution": "Solución detallada con doble punto..",
                "distractor_ids": ["D-Hab01-03"],
            },
            gen_result={
                "vars": {"a": 2},
                "options": [
                    {"value": "$x=2$", "is_correct": True},
                    {"value": "$x=3$", "is_correct": False, "distractor_id": "D-Hab01-03", "error_rationale": "Error con doble punto en parámetro @a@.."},
                    {"value": "$x=4$", "is_correct": False, "distractor_id": "D-Hab01-04", "error_rationale": "Error segundo válido con parámetro @a@."},
                    {"value": "$x=5$", "is_correct": False, "distractor_id": "D-Hab01-05", "error_rationale": "Error tercero válido con parámetro @a@."},
                ],
            },
            competency_id="Hab-01",
            question_index=1,
            seed=42,
        )
        assert not q["stem"].endswith("..")
        assert not q["detailed_solution"].endswith("..")
        assert not q["hints"][0].endswith("..")
        assert all(not (o.get("error_rationale") or "").endswith("..") for o in q["options"])


# =============================================================================
# LEVER 6: Complexity-Weighted Sharding
# =============================================================================

class TestLever6ComplexityWeightedSharding:
    def test_is_heavy_competency_and_partitioning(self, tmp_path: Path):
        assert plan_shards.DEFAULT_COMPS_PER_SHARD == 2
        assert plan_shards.MAX_SKILLS_PER_SHARD == 1

        c_skill = {"id": "Hab-01", "type": "skill", "recommended_modalities": ["FIB", "MS"]}
        c_heavy_m20 = {"id": "C-01", "type": "concept", "recommended_modalities": ["invariant_canvas", "open_symbolic"]}
        c_light_concept = {"id": "C-02", "type": "concept", "recommended_modalities": ["MC7", "open_symbolic", "MS"]}
        c_light_fact = {"id": "H-01", "type": "fact", "recommended_modalities": ["MC7", "FIB"]}

        assert plan_shards.is_heavy_competency(c_skill) is True
        assert plan_shards.is_heavy_competency(c_heavy_m20) is True
        assert plan_shards.is_heavy_competency(c_light_concept) is False
        assert plan_shards.is_heavy_competency(c_light_fact) is False

        comps = [c_light_fact, c_heavy_m20, c_light_concept, c_skill]
        for c in comps:
            c["distractors"] = []
            c["evidence"] = [{"doc": "source.pdf", "page": 1}]

        work_dir, shards_dir, _, cta_file = _seed_workspace(tmp_path, comps)
        manifest = plan_shards.plan_shards(cta_file, shards_dir)
        shards = manifest["shards"]

        # Hab-01 (1 comp) + C-01 (1 comp) isolated; C-02 + H-01 packed into 1 light shard (2 comps)
        assert len(shards) == 3
        assert shards[0]["competency_ids"] == ["Hab-01"]
        assert shards[1]["competency_ids"] == ["C-01"]
        assert set(shards[2]["competency_ids"]) == {"H-01", "C-02"}
