"""Dynamic Competency Sharding Engine for content-to-course v3.

Partitions CTA competencies into K balanced shards (max 2 competencies per shard, K = ceil(N/2)):
- Weights competencies by cognitive demand (Skill=3.0, Concept=2.0, Fact=1.0 + 0.1 * distractors)
- Keeps consecutive competencies co-located in pairs (exact 2 per shard; odd total leaves 1 in last shard)
- Emits work/shards/shard_01.json ... shard_0K.json and work/shards/manifest.json
- Injects self-contained dsl_reference into every shard for 100% author isolation
"""

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

# Self-contained reference for shard authors so they never read engine code
DSL_REFERENCE: Dict[str, Any] = {
    "helpers": {
        "fmt": "fmt(x, nd=4): Formats scalars (integers as '3', floats as '3.1416', Fraction as '\\frac{a}{b}').",
        "bmatrix": "bmatrix(matrix, nd=4): Formats a 2D matrix or list of lists as KaTeX '\\begin{bmatrix} ... \\end{bmatrix}'.",
        "table_array": "table_array(rows, headers=None, align=None, nd=4): Formats rows as KaTeX '\\begin{array}{...} ... \\end{array}'.",
        "latex_frac": "latex_frac(num, den): Formats fraction as LaTeX '\\frac{num}{den}' with clean sign handling.",
    },
    "allowed_modules": [
        "math",
        "fractions",
        "statistics",
        "sympy",
        "numpy",
        "scipy",
        "random",
        "decimal",
    ],
    "rules": {
        "strict_isolation": (
            "PROHIBIDO leer código fuente del motor (sandbox.py, assemble.py, invariants.py, SKILL.md). "
            "Toda la información necesaria está embebida en tu archivo de shard asignado."
        ),
        "validation_command": (
            "python .agents/skills/content-to-course/check_templates.py work/templates/<comp_id1>.json work/templates/<comp_id2>.json ... --cta work/cta.json --strict"
        ),
        "quotas": (
            "Para CADA competencia asignada: autorar al menos 6 plantillas paramétricas "
            "(>=2 MC7, >=2 FIB, >=2 MS) en work/templates/<comp_id>.json."
        ),
        "distractor_coverage": (
            "Regla TPL-D3: 100% de los distractor_ids declarados en la competencia deben usarse en al menos una plantilla. "
            "Regla TPL-D2: Plantillas MC7 requieren exactamente 6 distractor_ids distintos."
        ),
        "tpl_var_mandatory": (
            "Regla TPL-VAR-MANDATORY: Declarar obligatoriamente entre 3 y 5 'stem_variants' "
            "(directa/conceptual, contextualizada, analítica/simbólica) con {placeholders} en cada plantilla "
            "para garantizar diversidad estructural de enunciados (ratio >= 0.50)."
        ),
    },
    "canonical_examples": {
        "multiple_choice_7_options": {
            "id": "T-SAMPLE-01",
            "competency_id": "<comp_id>",
            "interaction_type": "multiple_choice_7_options",
            "difficulty": "medium",
            "bloom": "Understand",
            "stem": "Considere la ecuación $${A} u_{{xx}} + {B} u_{{xy}} + {C} u_{{yy}} = 0$$. Calcule su discriminante $\\Delta = B^2 - 4AC$ y determine su clasificación:",
            "stem_variants": [
                "Considere la ecuación $${A} u_{{xx}} + {B} u_{{xy}} + {C} u_{{yy}} = 0$$. Calcule su discriminante $\\Delta = B^2 - 4AC$ y determine su clasificación:",
                "Dada la ecuación de segundo orden $${A} u_{{xx}} + {B} u_{{xy}} + {C} u_{{yy}} = 0$$, evalúe el discriminante $\\Delta = B^2 - 4AC$ para establecer el tipo de ecuación:",
                "Para el modelo formal plano $${A} u_{{xx}} + {B} u_{{xy}} + {C} u_{{yy}} = 0$$, clasifique su naturaleza analítica a partir del signo de $\\Delta = B^2 - 4AC$:",
            ],
            "generate_py": (
                "def generate(rng):\n"
                "    A = rng.randint(2, 4)\n"
                "    C = rng.randint(2, 4)\n"
                "    B = rng.choice([0, 1, 2])\n"
                "    delta = B**2 - 4 * A * C\n"
                "    correct_str = f'Discriminante $\\\\Delta = {delta} < 0$, de modo que la ecuación es elíptica en el plano.'\n"
                "    d1 = f'Discriminante $\\\\Delta = {delta} < 0$, de modo que la ecuación es hiperbólica en el plano.'\n"
                "    d2 = f'Discriminante $\\\\Delta = {B**2 - A*C}$, por lo que la ecuación es parabólica en el plano.'\n"
                "    d3 = f'Discriminante $\\\\Delta = {abs(delta)} > 0$, de modo que la ecuación es hiperbólica en el plano.'\n"
                "    d4 = f'Discriminante $\\\\Delta = {-delta}$, por lo que la ecuación es parabólica degenerada plana.'\n"
                "    d5 = f'Discriminante $\\\\Delta = {(2*B)**2 - 4*A*C}$, indicando indeterminación analítica global.'\n"
                "    d6 = f'Discriminante $\\\\Delta = 0$, concluyendo que la ecuación pertenece al tipo parabólico.'\n"
                "    return {\n"
                "        'vars': {'A': A, 'B': B, 'C': C, 'delta': delta},\n"
                "        'correct': correct_str,\n"
                "        'distractors': [\n"
                "            {'value': d1, 'distractor_id': 'D-01'},\n"
                "            {'value': d2, 'distractor_id': 'D-02'},\n"
                "            {'value': d3, 'distractor_id': 'D-03'},\n"
                "            {'value': d4, 'distractor_id': 'D-04'},\n"
                "            {'value': d5, 'distractor_id': 'D-05'},\n"
                "            {'value': d6, 'distractor_id': 'D-06'},\n"
                "        ]\n"
                "    }"
            ),
            "cross_check_py": (
                "def verify(result):\n"
                "    delta = result['vars']['delta']\n"
                "    return delta < 0 and 'elíptica' in result['correct']"
            ),
            "hints": [
                "Identifique los coeficientes de segundo orden: A acompaña a u_xx, B a u_xy y C a u_yy.",
                "Calcule el discriminante formal utilizando la expresión Delta = B^2 - 4AC.",
                "Recuerde el criterio: Delta < 0 es elíptica, Delta = 0 es parabólica y Delta > 0 es hiperbólica.",
            ],
            "solution": "Se tienen los coeficientes A = {A}, B = {B} y C = {C}. Al calcular el discriminante obtenemos Delta = {B}^2 - 4({A})({C}) = {delta}. Dado que Delta < 0, la ecuación es estrictamente elíptica.",
            "distractor_ids": ["D-01", "D-02", "D-03", "D-04", "D-05", "D-06"],
        },
        "fill_in_the_blank": {
            "id": "T-SAMPLE-02",
            "competency_id": "<comp_id>",
            "interaction_type": "fill_in_the_blank",
            "difficulty": "easy",
            "bloom": "Apply",
            "stem": "Determine el valor numérico del discriminante $\\Delta = B^2 - 4AC$ para la ecuación $${A} u_{{xx}} + {B} u_{{xy}} + {C} u_{{yy}} = 0$$.",
            "stem_variants": [
                "Determine el valor numérico del discriminante $\\Delta = B^2 - 4AC$ para la ecuación $${A} u_{{xx}} + {B} u_{{xy}} + {C} u_{{yy}} = 0$$.",
                "Calcule el valor escalar de $\\Delta = B^2 - 4AC$ correspondiente a la ecuación $${A} u_{{xx}} + {B} u_{{xy}} + {C} u_{{yy}} = 0$$.",
                "Para la formulación de segundo orden $${A} u_{{xx}} + {B} u_{{xy}} + {C} u_{{yy}} = 0$$, halle el discriminante numérico $\\Delta = B^2 - 4AC$.",
            ],
            "generate_py": (
                "def generate(rng):\n"
                "    A = rng.randint(1, 5)\n"
                "    B = rng.randint(1, 6)\n"
                "    C = rng.randint(1, 5)\n"
                "    delta = B**2 - 4 * A * C\n"
                "    return {\n"
                "        'vars': {'A': A, 'B': B, 'C': C},\n"
                "        'correct': delta,\n"
                "        'value': str(delta),\n"
                "        'canonical_algebraic': str(delta),\n"
                "        'accepted_equivalents': [str(delta), f'{delta}.0'],\n"
                "        'tolerance': 0.0001,\n"
                "        'distractors': []\n"
                "    }"
            ),
            "cross_check_py": (
                "def verify(result):\n"
                "    A = result['vars']['A']\n"
                "    B = result['vars']['B']\n"
                "    C = result['vars']['C']\n"
                "    return int(result['correct']) == (B**2 - 4 * A * C)"
            ),
            "hints": [
                "Identifique los valores de A, B y C dados en la ecuación.",
                "Calcule B^2 elevando al cuadrado el coeficiente de la derivada cruzada.",
                "Reste 4 * A * C para obtener el valor escalar final de Delta.",
            ],
            "solution": "Aplicando la fórmula del discriminante: Delta = ({B})^2 - 4({A})({C}) = {delta}.",
            "distractor_ids": [],
        },
        "multiple_select": {
            "id": "T-SAMPLE-03",
            "competency_id": "<comp_id>",
            "interaction_type": "multiple_select",
            "difficulty": "hard",
            "bloom": "Analyze",
            "stem": "Para la ecuación diferencial $${A} u_{{xx}} + {B} u_{{xy}} + {C} u_{{yy}} = 0$$, seleccione todas las afirmaciones teóricas que son matemáticamente verdaderas:",
            "stem_variants": [
                "Para la ecuación diferencial $${A} u_{{xx}} + {B} u_{{xy}} + {C} u_{{yy}} = 0$$, seleccione todas las afirmaciones teóricas que son matemáticamente verdaderas:",
                "Considere el modelo de segundo orden $${A} u_{{xx}} + {B} u_{{xy}} + {C} u_{{yy}} = 0$$. ¿Cuáles de las siguientes propiedades sobre su clasificación y discriminante son válidas?",
                "Respecto a la formulación $${A} u_{{xx}} + {B} u_{{xy}} + {C} u_{{yy}} = 0$$, identifique todas las proposiciones ciertas sobre sus curvas características y discriminante:",
            ],
            "generate_py": (
                "def generate(rng):\n"
                "    A = 1\n"
                "    C = 1\n"
                "    B = rng.randint(4, 12)\n"
                "    delta = B**2 - 4 * A * C\n"
                "    opts = [\n"
                "        {'content': 'El discriminante Delta es estrictamente positivo en todo el dominio.', 'is_correct': True, 'distractor_id': None},\n"
                "        {'content': 'La ecuación admite dos familias reales y distintas de curvas características.', 'is_correct': True, 'distractor_id': None},\n"
                "        {'content': 'La ecuación es de tipo elíptico en todo el plano euclídeo.', 'is_correct': False, 'distractor_id': 'D-01'},\n"
                "        {'content': 'El discriminante se calcula como Delta = B^2 - AC sin el factor cuatro.', 'is_correct': False, 'distractor_id': 'D-02'},\n"
                "    ]\n"
                "    return {\n"
                "        'vars': {'A': A, 'B': B, 'C': C, 'delta': delta},\n"
                "        'options': opts,\n"
                "        'distractors': []\n"
                "    }"
            ),
            "cross_check_py": (
                "def verify(result):\n"
                "    return result['vars']['delta'] > 0"
            ),
            "hints": [
                "Calcule el signo de Delta = B^2 - 4AC.",
                "Analice las implicaciones geométricas del signo sobre las curvas características.",
                "Marque sólo las propiedades que se desprenden del carácter hiperbólico de la ecuación.",
            ],
            "solution": "Dado que B^2 - 4AC = {delta} > 0, la ecuación es hiperbólica y admite dos familias de curvas características reales y distintas.",
            "distractor_ids": ["D-01", "D-02"],
        },
    },
}


def calculate_competency_weight(comp: Dict[str, Any]) -> float:
    """Compute cognitive authoring weight for a single competency."""
    ctype = comp.get("type", "concept").lower().strip()
    if ctype in ("skill", "hab", "habilidad"):
        base = 3.0
    elif ctype in ("concept", "c", "concepto"):
        base = 2.0
    else:  # fact / h
        base = 1.0

    distractors_count = len(comp.get("distractors", []))
    return base + (0.1 * distractors_count)


def determine_shard_count(
    competencies: List[Dict[str, Any]],
    requested_k: Optional[int] = None,
    max_comps_per_shard: Optional[int] = None,
) -> int:
    """Determine shard count K with sweet-spot amortized sharding (default max 8, auto-adapting)."""
    total_comps = len(competencies)
    if total_comps <= 1:
        return max(1, total_comps)

    if requested_k is not None:
        target_k = max(1, min(requested_k, total_comps))
        return target_k

    if max_comps_per_shard is not None and max_comps_per_shard > 0:
        target_max = max_comps_per_shard
    else:
        # Heuristic auto-selection based on architectural audit:
        # Check if distractor graph is dense (average distractors > 6) -> use 4 (Caso A.3)
        avg_distractors = sum(len(c.get("distractors", [])) for c in competencies) / max(1, total_comps)
        if avg_distractors > 6.0:
            target_max = 4
        else:
            target_max = 8

    # Balanced number of shards so that no shard exceeds target_max
    k = math.ceil(total_comps / float(target_max))
    return max(1, min(k, total_comps))


def partition_competencies_into_shards(
    competencies: List[Dict[str, Any]],
    k: int,
) -> List[Dict[str, Any]]:
    """Partition competencies into K balanced shards preserving pedagogical contiguity."""
    if not competencies:
        return []

    total_comps = len(competencies)
    k = max(1, min(k, total_comps))

    shards: List[Dict[str, Any]] = []

    # Distribute competencies evenly across K shards (sizes differ by at most 1)
    base_size = total_comps // k
    remainder = total_comps % k
    cur_idx = 0
    for idx in range(k):
        size = base_size + (1 if idx < remainder else 0)
        shard_comps = competencies[cur_idx:cur_idx + size]
        cur_idx += size
        shards.append({
            "shard_id": f"shard_{idx + 1:02d}",
            "shard_index": idx + 1,
            "total_shards": k,
            "weight": round(sum(calculate_competency_weight(c) for c in shard_comps), 2),
            "competency_ids": [c["id"] for c in shard_comps],
            "competencies": shard_comps,
        })

    return shards


def plan_shards(
    cta_path: Union[str, Path],
    output_dir: Union[str, Path],
    k: Optional[int] = None,
    max_comps: Optional[int] = None,
) -> Dict[str, Any]:
    """Execute sharding on cta.json and write shard JSON files."""
    cta_file = Path(cta_path).resolve()
    if not cta_file.is_file():
        raise FileNotFoundError(f"CTA file does not exist: {cta_file}")

    out_dir = Path(output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    cta_data = json.loads(cta_file.read_text(encoding="utf-8"))
    competencies = cta_data.get("competencies", [])
    if not competencies:
        raise ValueError("cta.json contains zero competencies.")

    shard_count = determine_shard_count(competencies, requested_k=k, max_comps_per_shard=max_comps)
    shards = partition_competencies_into_shards(competencies, shard_count)

    manifest_shards = []
    for shard in shards:
        s_id = shard["shard_id"]
        shard_file = out_dir / f"{s_id}.json"

        shard_payload = {
            "shard_id": s_id,
            "shard_index": shard["shard_index"],
            "total_shards": shard["total_shards"],
            "weight": shard["weight"],
            "competency_ids": shard["competency_ids"],
            "course_id": cta_data.get("course_id", "course"),
            "course_title": cta_data.get("title", ""),
            "competencies": shard["competencies"],
            "expected_templates": [f"templates/{cid}.json" for cid in shard["competency_ids"]],
            "dsl_reference": DSL_REFERENCE,
        }

        shard_file.write_text(json.dumps(shard_payload, indent=2, ensure_ascii=False), encoding="utf-8")

        manifest_shards.append({
            "shard_id": s_id,
            "shard_file": str(shard_file.as_posix()),
            "competency_count": len(shard["competency_ids"]),
            "competency_ids": shard["competency_ids"],
            "weight": shard["weight"],
        })

    manifest_payload = {
        "cta_source": str(cta_file.as_posix()),
        "total_competencies": len(competencies),
        "total_shards": len(shards),
        "shards": manifest_shards,
    }

    manifest_file = out_dir / "manifest.json"
    manifest_file.write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    return manifest_payload


def main():
    parser = argparse.ArgumentParser(description="Partition CTA competencies into balanced amortized shards")
    parser.add_argument("--cta", required=True, help="Path to cta.json")
    parser.add_argument("--output-dir", required=True, help="Output directory for shards (e.g. work/shards)")
    parser.add_argument("--k", type=int, default=None, help="Force specific shard count K")
    parser.add_argument("--comps-per-shard", type=int, default=None, help="Target max competencies per shard (default: 8, or 4 for dense distractors)")
    args = parser.parse_args()

    res = plan_shards(args.cta, args.output_dir, k=args.k, max_comps=args.comps_per_shard)
    print(f"[+] Successfully partitioned {res['total_competencies']} competencies into {res['total_shards']} shards:")
    for s in res["shards"]:
        print(f"    - [{s['shard_id']}] {s['competency_count']} competencies (weight={s['weight']}): {', '.join(s['competency_ids'])}")


if __name__ == "__main__":
    main()
