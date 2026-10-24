"""Dynamic Competency Sharding Engine for content-to-course v3.3.

Partitions CTA competencies into balanced shards with Milestone 7.4 Cognitive Sharding:
- Hard Skill Isolation Rule: Every skill ('Hab-*') is isolated into an exclusive 1-competency shard (Anti-Straggler SLA).
- Contiguous Concept/Fact Grouping: Consecutive non-skill competencies are packed max 2 competencies per shard
  (allowing up to 3 competencies ONLY when all 3 are 'fact' and total competencies N >= 30).
- Heaviest-First Ordering: Shards are sorted descending by weight (Skill=6.0, Concept=2.5, Fact=1.5 + 0.1*distractors)
  so all Skill shards sit at the front of Wave 1 (t = 0).
- Wave Indexing: Single-wave maximum parallelism by default (max_wave_size default: 50, Heaviest-First at t = 0).
- Backward compatibility: Preserves uniform partitioning when explicit K is passed.
- Emits work/shards/shard_01.json ... shard_0K.json and work/shards/pre_shard_manifest.json.
- Injects self-contained dsl_reference into every shard for 100% author isolation.
"""

import argparse
import json
import math
import os
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

# =============================================================================
# SHARD & TEMPLATE SCALING CONFIGURATION
# Caso 2B (Variedad Máxima / Deep Mastery) - ACTUAL:
#   C = 2 (máximo 2 competencias por shard)
#   T = 4 (4 plantillas disjuntas por competencia: Directa, Inversa, Perturbación, Frontera)
# [REVERT TO 2A]: Cambiar DEFAULT_COMPS_PER_SHARD = 3 para volver al Caso 2A (C=3, T=3)
# =============================================================================
DEFAULT_COMPS_PER_SHARD: int = 2
DEFAULT_MAX_WAVE_SIZE: int = 50


def _atomic_write_json(target_path: Path, data: Any) -> None:
    """Safely write JSON payload to file using atomic replace to prevent race conditions."""
    target_path = Path(target_path).resolve()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = target_path.with_name(f".{target_path.name}.tmp.{os.getpid()}_{uuid.uuid4().hex[:8]}")
    payload_str = json.dumps(data, indent=2, ensure_ascii=False)
    tmp_path.write_text(payload_str, encoding="utf-8")
    try:
        try:
            os.replace(tmp_path, target_path)
        except Exception:
            # Fallback in case os.replace encounters a transient lock on Windows
            try:
                if target_path.is_file():
                    target_path.unlink()
                os.replace(tmp_path, target_path)
            except Exception:
                target_path.write_text(payload_str, encoding="utf-8")
    finally:
        if tmp_path.is_file():
            try:
                tmp_path.unlink()
            except Exception:
                pass


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
            "Para CADA competencia asignada: autorar exactamente 4 plantillas paramétricas disjuntas "
            "(Caso 2B: 4 arquetipos: 1. Directo / Cálculo Frontal, 2. Inverso / Despeje de Parámetro, "
            "3. Perturbación / Estática Comparativa, 4. Frontera / Casos Límite y Contraejemplos) "
            "en work/shards/<shard_id>_data.py y compilar a work/templates/<comp_id>.json. "
            "[REVERT TO 2A]: Cambiar a 3 plantillas disjuntas para Caso 2A (Directo, Inverso, Perturbación)."
        ),
        "distractor_coverage": (
            "Regla TPL-D3: 100% de los distractor_ids declarados en la competencia deben usarse en al menos una plantilla. "
            "Regla TPL-D2: Plantillas MC7 requieren exactamente 6 distractor_ids distintos."
        ),
        "tpl_var_mandatory": (
            "Regla TPL-VAR-MANDATORY: Declarar obligatoriamente entre 3 y 5 'stem_variants' "
            "(directa/conceptual, contextualizada, analítica/simbólica) con placeholders @var@ o {var} en cada plantilla "
            "para garantizar diversidad estructural de enunciados (ratio >= 0.50)."
        ),
        "orthogonal_tokens_raw_strings": (
            "REGLA DE TOKENS ORTOGONALES (@var@ / @var:fmt@): Usar strings crudos r'...' con tokens @nombre@ o @nombre:fmt@ "
            "(ej. r'Sea f(x) = @a@ x^2 + @b:fmt@ x'). PROHIBIDO usar rf'...' o f-strings directos para erradicar al 100% las "
            "colisiones de llaves con KaTeX '{...}'. Se preserva compatibilidad con {var} clásico siempre que no colisione con KaTeX."
        ),
        "anti_double_braces": (
            "REGLA DE ORO DE LLAVES: PROHIBIDO usar dobles llaves '{{' o '}}' en stem, hints o solution en JSON. "
            "En KaTeX las llaves son simples: 'u_{xx}', 'x^{-1}', '\\bar{r}', '\\dot{r}'. "
            "Usar tokens @var@ en raw strings r'...' para evitar cualquier ambigüedad."
        ),
        "vars_contract": (
            "REGLA DE ORO DE VARIABLES: Toda variable usada como @nombre@ o {nombre} en stem, hints o solution DEBE declararse "
            "en el diccionario 'vars' retornado por generate_py. Especialmente, si usas '@correct@' o '{correct}' en solution, "
            "incluye obligatoriamente 'correct': ... dentro de 'vars'."
        ),
        "error_rationale_math": (
            "REGLA DE NOTACIÓN EN RATIONALE: Toda expresión matemática en 'error_rationale' DEBE ir entre signos de "
            "dólar '$...$' (ej. '$\\dot{r}$', nunca texto plano 'dot{r}')."
        ),
        "tpl_var_minimum_domain": (
            "REGLA DE DOMINIO Y DIVERSIDAD (TPL-VAR): Todo rng.choice DEBE tener un dominio de al menos 8 a 12 valores "
            "distintos, o usar rng.randint / rng.uniform, para satisfacer TPL-VAR (mínimo 4 variantes únicas generadas)."
        ),
        "native_graph_schema": (
            "SOPORTE NATIVO DE GRÁFICOS: Para diagramas de fase o curvas analíticas, Top's Academy soporta "
            "el esquema JSON nativo 'graph': {'title': str, 'x_axis': {'label': str, 'min': float, 'max': float}, "
            "'y_axis': {'label': str, 'min': float, 'max': float}, 'curves': [{'name': str, 'fn': str, 'style': 'solid'}], "
            "'points': [{'name': str, 'x': float, 'y': float, 'label': str}]}. NO simular gráficos en puro texto KaTeX."
        ),
        "shard_isolated_script": (
            "SCRIPT INDEPENDIENTE: Cada shard escribe exclusivamente su propio script work/build_<shard_id>.py. "
            "Valida únicamente tu shard asignado: python .agents/skills/content-to-course/check_templates.py "
            "work/shards/<shard_id>.json --cta work/cta.json --strict"
        ),
        "modular_per_comp_overrides": (
            "SOPORTE MODULAR DE CORRECCIONES POR COMPETENCIA: Si una competencia específica requiere corrección "
            "o parchado aislado sin recompilar todo el shard, escribir el módulo en work/shards/shard_fixes/<CID>.py "
            "con la plantilla corregida."
        ),
    },
    "canonical_examples": {
        "multiple_choice_7_options": {
            "id": "T-SAMPLE-01",
            "competency_id": "<comp_id>",
            "interaction_type": "multiple_choice_7_options",
            "difficulty": "medium",
            "bloom": "Understand",
            "stem": r"Considere la ecuación @A@ u_{xx} + @B@ u_{xy} + @C@ u_{yy} = 0. Calcule su discriminante $\Delta = B^2 - 4AC$ y determine su clasificación:",
            "stem_variants": [
                r"Considere la ecuación @A@ u_{xx} + @B@ u_{xy} + @C@ u_{yy} = 0. Calcule su discriminante $\Delta = B^2 - 4AC$ y determine su clasificación:",
                r"Dada la ecuación de segundo orden @A@ u_{xx} + @B@ u_{xy} + @C@ u_{yy} = 0, evalúe el discriminante $\Delta = B^2 - 4AC$ para establecer el tipo de ecuación:",
                r"Para el modelo formal plano @A@ u_{xx} + @B@ u_{xy} + @C@ u_{yy} = 0, clasifique su naturaleza analítica a partir del signo de $\Delta = B^2 - 4AC$:",
            ],
            "generate_py": (
                "def generate(rng):\n"
                "    A = rng.randint(2, 5)\n"
                "    C = rng.randint(2, 5)\n"
                "    B = rng.choice([0, 1, 2, 3, 4, 5, 6, 7])\n"
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
            "solution": r"Se tienen los coeficientes A = @A@, B = @B@ y C = @C@. Al calcular el discriminante obtenemos Delta = (@B@)^2 - 4(@A@)(@C@) = @delta@. Dado que Delta < 0, la ecuación es estrictamente elíptica.",
            "distractor_ids": ["D-01", "D-02", "D-03", "D-04", "D-05", "D-06"],
        },
        "fill_in_the_blank": {
            "id": "T-SAMPLE-02",
            "competency_id": "<comp_id>",
            "interaction_type": "fill_in_the_blank",
            "difficulty": "easy",
            "bloom": "Apply",
            "stem": r"Determine el valor numérico del discriminante $\Delta = B^2 - 4AC$ para la ecuación @A@ u_{xx} + @B@ u_{xy} + @C@ u_{yy} = 0.",
            "stem_variants": [
                r"Determine el valor numérico del discriminante $\Delta = B^2 - 4AC$ para la ecuación @A@ u_{xx} + @B@ u_{xy} + @C@ u_{yy} = 0.",
                r"Calcule el valor escalar de $\Delta = B^2 - 4AC$ correspondiente a la ecuación @A@ u_{xx} + @B@ u_{xy} + @C@ u_{yy} = 0.",
                r"Para la formulación de segundo orden @A@ u_{xx} + @B@ u_{xy} + @C@ u_{yy} = 0, halle el discriminante numérico $\Delta = B^2 - 4AC$.",
            ],
            "generate_py": (
                "def generate(rng):\n"
                "    A = rng.randint(1, 5)\n"
                "    B = rng.randint(1, 6)\n"
                "    C = rng.randint(1, 5)\n"
                "    delta = B**2 - 4 * A * C\n"
                "    return {\n"
                "        'vars': {'A': A, 'B': B, 'C': C, 'delta': delta},\n"
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
            "solution": r"Aplicando la fórmula del discriminante: Delta = (@B@)^2 - 4(@A@)(@C@) = @delta@.",
            "distractor_ids": [],
        },
        "multiple_select": {
            "id": "T-SAMPLE-03",
            "competency_id": "<comp_id>",
            "interaction_type": "multiple_select",
            "difficulty": "hard",
            "bloom": "Analyze",
            "stem": r"Para la ecuación diferencial @A@ u_{xx} + @B@ u_{xy} + @C@ u_{yy} = 0, seleccione todas las afirmaciones teóricas que son matemáticamente verdaderas:",
            "stem_variants": [
                r"Para la ecuación diferencial @A@ u_{xx} + @B@ u_{xy} + @C@ u_{yy} = 0, seleccione todas las afirmaciones teóricas que son matemáticamente verdaderas:",
                r"Considere el modelo de segundo orden @A@ u_{xx} + @B@ u_{xy} + @C@ u_{yy} = 0. ¿Cuáles de las siguientes propiedades sobre su clasificación y discriminante son válidas?",
                r"Respecto a la formulación @A@ u_{xx} + @B@ u_{xy} + @C@ u_{yy} = 0, identifique todas las proposiciones ciertas sobre sus curvas características y discriminante:",
            ],
            "generate_py": (
                "def generate(rng):\n"
                "    A = 1\n"
                "    C = 1\n"
                "    B = rng.choice([4, 5, 6, 7, 8, 9, 10, 11, 12])\n"
                "    delta = B**2 - 4 * A * C\n"
                "    opts = [\n"
                "        {'content': 'El discriminante Delta es estrictamente positivo en todo el dominio.', 'is_correct': True, 'distractor_id': None},\n"
                "        {'content': 'La ecuación admite dos familias reales y distintas de curvas características.', 'is_correct': True, 'distractor_id': None},\n"
                "        {'content': 'La ecuación es de tipo elíptico en todo el plano euclídeo.', 'is_correct': False, 'distractor_id': 'D-01', 'error_rationale': 'El discriminante es estrictamente positivo, por lo que la ecuación es hiperbólica.'},\n"
                "        {'content': 'El discriminante se calcula como Delta = B^2 - AC sin el factor cuatro.', 'is_correct': False, 'distractor_id': 'D-02', 'error_rationale': 'La fórmula del discriminante exige el factor cuatro: $4AC$.'},\n"
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
            "solution": r"Dado que B^2 - 4AC = @delta@ > 0, la ecuación es hiperbólica y admite dos familias de curvas características reales y distintas.",
            "distractor_ids": ["D-01", "D-02"],
        },
    },
}


def is_skill_competency(comp: Dict[str, Any]) -> bool:
    """Return True if competency is classified as a Skill (Hab)."""
    ctype = str(comp.get("type", "")).lower().strip()
    cid = str(comp.get("id", "")).strip().upper()
    if ctype in ("skill", "skills", "hab", "habilidad", "habilidades"):
        return True
    if (
        cid.startswith("HAB-")
        or cid.startswith("HAB_")
        or cid.startswith("SKILL-")
        or cid.startswith("SKILL_")
        or "-HAB-" in cid
        or "-HAB_" in cid
        or "_HAB_" in cid
        or "-SKILL-" in cid
        or "_SKILL_" in cid
    ):
        return True
    if cid.startswith("HAB") and len(cid) > 3 and cid[3:].isdigit():
        return True
    return False


def is_fact_competency(comp: Dict[str, Any]) -> bool:
    """Return True if competency is classified as a Fact (H)."""
    if is_skill_competency(comp):
        return False
    ctype = str(comp.get("type", "")).lower().strip()
    cid = str(comp.get("id", "")).strip().upper()
    if ctype in ("fact", "facts", "h", "hecho", "hechos"):
        return True
    if (
        cid.startswith("H-")
        or cid.startswith("H_")
        or cid.startswith("FACT-")
        or cid.startswith("FACT_")
        or cid.startswith("HECHO-")
        or cid.startswith("HECHO_")
        or "-H-" in cid
        or "-H_" in cid
        or "_H_" in cid
        or "-FACT-" in cid
        or "_FACT_" in cid
    ):
        return True
    if cid.startswith("H") and len(cid) > 1 and cid[1:].isdigit():
        return True
    return False


def is_concept_competency(comp: Dict[str, Any]) -> bool:
    """Return True if competency is classified as a Concept (C)."""
    if is_skill_competency(comp):
        return False
    ctype = str(comp.get("type", "")).lower().strip()
    cid = str(comp.get("id", "")).strip().upper()
    if ctype in ("concept", "concepts", "c", "concepto", "conceptos"):
        return True
    if (
        cid.startswith("C-")
        or cid.startswith("C_")
        or cid.startswith("CONCEPT-")
        or cid.startswith("CONCEPT_")
        or cid.startswith("CONCEPTO-")
        or cid.startswith("CONCEPTO_")
        or "-C-" in cid
        or "-C_" in cid
        or "_C_" in cid
        or "-CONCEPT-" in cid
        or "_CONCEPT_" in cid
    ):
        return True
    if cid.startswith("C") and len(cid) > 1 and cid[1:].isdigit():
        return True
    return False


def calculate_competency_weight(comp: Dict[str, Any]) -> float:
    """Compute cognitive authoring weight for a single competency.
    
    Milestone 7.4 calibrated weights:
    - Skill = 6.0
    - Concept = 2.5
    - Fact = 1.5
    + 0.1 * len(distractors)
    """
    if is_skill_competency(comp):
        base = 6.0
    elif is_concept_competency(comp):
        base = 2.5
    else:  # fact / other
        base = 1.5

    distractors_raw = comp.get("distractors")
    distractors_count = len(distractors_raw) if isinstance(distractors_raw, list) else 0
    return round(base + (0.1 * distractors_count), 2)


def determine_shard_count(
    competencies: Union[List[Dict[str, Any]], int],
    avg_distractors: Optional[Union[float, int]] = None,
    requested_k: Optional[int] = None,
    max_comps_per_shard: Optional[int] = DEFAULT_COMPS_PER_SHARD,
) -> int:
    """Determine shard count K with sweet-spot amortized sharding (Case 2B: max 2 per shard; Case 2A: max 3 per shard).

    Can be invoked with:
      determine_shard_count(num_competencies, avg_distractors)
    or:
      determine_shard_count(competencies, requested_k=k, max_comps_per_shard=max_comps)
    """
    if isinstance(competencies, int):
        total_comps = competencies
        avg_d = float(avg_distractors) if avg_distractors is not None else 0.0
    else:
        total_comps = len(competencies)
        if avg_distractors is not None:
            avg_d = float(avg_distractors)
        else:
            avg_d = sum(len(c.get("distractors", [])) for c in competencies) / max(1, total_comps)

    if total_comps <= 1:
        return max(1, total_comps)

    if requested_k is not None and requested_k > 0:
        target_k = max(1, min(requested_k, total_comps))
        return target_k

    if max_comps_per_shard is not None and max_comps_per_shard > 0:
        target_max = float(max_comps_per_shard)
    else:
        # Adaptive Shard Sizing: target max comps per shard clamped to DEFAULT_COMPS_PER_SHARD (Case 2B: 2, Case 2A: 3)
        # Sized for up to 8 concurrent author subagents, never exceeding DEFAULT_COMPS_PER_SHARD.
        target_max = float(max(2, min(DEFAULT_COMPS_PER_SHARD, math.ceil(total_comps / 8.0))))

    # Balanced number of shards so that no shard exceeds target_max
    k = math.ceil(total_comps / float(target_max))
    return max(1, min(k, total_comps))


def partition_competencies_into_shards(
    competencies: List[Dict[str, Any]],
    k: int,
) -> List[Dict[str, Any]]:
    """Partition competencies into K balanced shards preserving pedagogical contiguity (Legacy Uniform)."""
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
        w = round(sum(calculate_competency_weight(c) for c in shard_comps), 2)
        shards.append({
            "shard_id": f"shard_{idx + 1:02d}",
            "shard_index": idx,
            "total_shards": k,
            "weight": w,
            "estimated_weight": w,
            "competency_ids": [c["id"] for c in shard_comps],
            "competencies": shard_comps,
        })

    return shards


def partition_competencies_weighted(
    competencies: List[Dict[str, Any]],
    max_comps: Optional[int] = DEFAULT_COMPS_PER_SHARD,
) -> List[Dict[str, Any]]:
    """Partition competencies using Milestone 7.4 Weighted Cognitive Sharding & Anti-Straggler Rules:
    
    1. Hard Skill Isolation Rule:
       Every competency with type == 'skill' (or prefix 'Hab-') is assigned to its own exclusive
       1-competency shard (never grouped with another skill, concept, or fact).
    
    2. Contiguous Concept/Fact Grouping:
       Adjacent concept ('C-*') and fact ('H-*') competencies in curriculum order are packed
       with max 2 competencies per shard by default (Case 2B), allowing up to 3 competencies
       ONLY when all 3 are 'fact' and total competencies N >= 30.
       If max_comps >= 3 (e.g. Case 2A), groups up to max_comps per shard.
    """
    if not competencies:
        return []

    total_n = len(competencies)
    if total_n == 1:
        c = competencies[0]
        cid = c.get("id", "comp_01")
        w = calculate_competency_weight(c)
        return [{
            "weight": w,
            "estimated_weight": w,
            "competency_ids": [cid],
            "competencies": [c],
            "min_curriculum_idx": 0,
            "is_skill": is_skill_competency(c),
        }]

    curriculum_indices = {c.get("id", f"idx_{i}"): i for i, c in enumerate(competencies)}

    raw_shards: List[Dict[str, Any]] = []

    # 1. Hard Skill Isolation: Every skill gets its own exclusive 1-competency shard
    for c in competencies:
        if is_skill_competency(c):
            cid = c.get("id", "")
            w = calculate_competency_weight(c)
            raw_shards.append({
                "weight": w,
                "estimated_weight": w,
                "competency_ids": [cid],
                "competencies": [c],
                "min_curriculum_idx": curriculum_indices.get(cid, 0),
                "is_skill": True,
            })

    # 2. Contiguous Concept/Fact Grouping: Group non-skills in curriculum order
    target_max = max_comps if (max_comps is not None and max_comps > 0) else DEFAULT_COMPS_PER_SHARD
    non_skills = [c for c in competencies if not is_skill_competency(c)]
    idx = 0
    m = len(non_skills)
    while idx < m:
        remaining = m - idx
        # Exception rule for target_max == 2 (Case 2B):
        # up to 3 competencies allowed ONLY when all 3 are 'fact' and total competencies N >= 30
        if target_max == 2 and remaining >= 3 and total_n >= 30:
            if all(is_fact_competency(non_skills[idx + j]) for j in range(3)):
                if remaining == 3 or remaining >= 5:
                    chunk = non_skills[idx:idx + 3]
                    w = round(sum(calculate_competency_weight(x) for x in chunk), 2)
                    c_ids = [x.get("id", "") for x in chunk]
                    raw_shards.append({
                        "weight": w,
                        "estimated_weight": w,
                        "competency_ids": c_ids,
                        "competencies": chunk,
                        "min_curriculum_idx": min(curriculum_indices.get(x_id, 0) for x_id in c_ids),
                        "is_skill": False,
                    })
                    idx += 3
                    continue

        take = min(target_max, remaining)
        chunk = non_skills[idx:idx + take]
        w = round(sum(calculate_competency_weight(x) for x in chunk), 2)
        c_ids = [x.get("id", "") for x in chunk]
        raw_shards.append({
            "weight": w,
            "estimated_weight": w,
            "competency_ids": c_ids,
            "competencies": chunk,
            "min_curriculum_idx": min(curriculum_indices.get(x_id, 0) for x_id in c_ids),
            "is_skill": False,
        })
        idx += take

    return raw_shards


def plan_shards(
    cta_path: Union[str, Path],
    output_dir: Union[str, Path],
    k: Optional[int] = None,
    max_comps: Optional[int] = DEFAULT_COMPS_PER_SHARD,
    max_wave_size: int = DEFAULT_MAX_WAVE_SIZE,
    isolate_skills: bool = True,
) -> Dict[str, Any]:
    """Execute sharding on cta.json and write pre_shard_manifest.json (v3.3 canonical)."""
    cta_file = Path(cta_path).resolve()
    if not cta_file.is_file():
        raise FileNotFoundError(f"CTA file does not exist: {cta_file}")

    out_dir = Path(output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir = out_dir.parent

    # Locate pre_cta_manifest.json (No global fallback: strict workspace isolation)
    pre_cta_candidates = [
        work_dir / "pre_cta_manifest.json",
        cta_file.parent / "pre_cta_manifest.json",
    ]
    pre_cta_file = None
    for cand in pre_cta_candidates:
        if cand.is_file():
            pre_cta_file = cand
            break

    if not pre_cta_file:
        print("BLOCKER:: No existe pre_cta_manifest.json", file=sys.stderr)
        raise FileNotFoundError("BLOCKER:: No existe pre_cta_manifest.json")

    pre_cta_data = json.loads(pre_cta_file.read_text(encoding="utf-8"))
    candidate_sources: List[Any] = []
    if isinstance(pre_cta_data, list):
        candidate_sources = pre_cta_data
    elif isinstance(pre_cta_data, dict):
        if "source_files" in pre_cta_data and isinstance(pre_cta_data["source_files"], list):
            candidate_sources = pre_cta_data["source_files"]
        elif "files" in pre_cta_data and isinstance(pre_cta_data["files"], list):
            candidate_sources = pre_cta_data["files"]
        elif "documents" in pre_cta_data and isinstance(pre_cta_data["documents"], list):
            candidate_sources = pre_cta_data["documents"]
        elif "handouts" in pre_cta_data and isinstance(pre_cta_data["handouts"], list):
            candidate_sources = pre_cta_data["handouts"]
        else:
            candidate_sources = list(pre_cta_data.values()) + list(pre_cta_data.keys())

    if max_wave_size is None or max_wave_size <= 0:
        max_wave_size = DEFAULT_MAX_WAVE_SIZE

    cta_data = json.loads(cta_file.read_text(encoding="utf-8"))
    raw_comps = cta_data.get("competencies", []) if isinstance(cta_data, dict) else (cta_data if isinstance(cta_data, list) else [])
    if isinstance(raw_comps, dict):
        competencies = []
        for cid, c in raw_comps.items():
            if isinstance(c, dict):
                c_copy = dict(c)
                c_copy.setdefault("id", cid)
                competencies.append(c_copy)
    elif isinstance(raw_comps, list):
        competencies = raw_comps
    else:
        competencies = []

    if not competencies:
        raise ValueError("cta.json contains zero competencies.")

    # Partitioning Strategy Selection
    if k is not None or not isolate_skills:
        # Legacy explicit K partitioning
        shard_count = determine_shard_count(competencies, requested_k=k, max_comps_per_shard=max_comps)
        shards = partition_competencies_into_shards(competencies, shard_count)
        total_shards = len(shards)
        total_waves = math.ceil(total_shards / max_wave_size) if total_shards > 0 else 1
        for idx, s in enumerate(shards):
            s["wave_index"] = (idx // max_wave_size) + 1
            s["total_shards"] = total_shards
            s["total_waves"] = total_waves
            s["estimated_weight"] = s["weight"]
    else:
        # Milestone 7.4 Weighted Cognitive Sharding & Anti-Straggler SLA
        raw_shards = partition_competencies_weighted(competencies, max_comps=max_comps)
        # Heaviest-First Ordering:
        # Sort descending by weight (breaking ties deterministically by curriculum index).
        # Skills sit at the front of Wave 1 (t = 0).
        raw_shards.sort(
            key=lambda s: (0 if s.get("is_skill") else 1, -s["weight"], s.get("min_curriculum_idx", 0))
        )
        total_shards = len(raw_shards)
        total_waves = math.ceil(total_shards / max_wave_size) if total_shards > 0 else 1
        shards = []
        for idx, s in enumerate(raw_shards):
            s_id = f"shard_{idx + 1:02d}"
            shards.append({
                "shard_id": s_id,
                "shard_index": idx,
                "wave_index": (idx // max_wave_size) + 1,
                "total_shards": total_shards,
                "total_waves": total_waves,
                "weight": s["weight"],
                "estimated_weight": s["estimated_weight"],
                "competency_ids": s["competency_ids"],
                "competencies": s["competencies"],
            })

    manifest_shards = []
    templates_dir_abs = str((work_dir / "templates").resolve().as_posix())

    for idx, shard in enumerate(shards):
        s_id = shard["shard_id"]
        shard_data_path_abs = str((out_dir / f"{s_id}_data.py").resolve().as_posix())

        # Extract evidence docs from competencies and distractors
        shard_docs = set()
        for comp in shard["competencies"]:
            ev = comp.get("evidence", [])
            if isinstance(ev, list):
                for e in ev:
                    if isinstance(e, dict) and e.get("doc"):
                        shard_docs.add(e["doc"])
                    elif isinstance(e, str):
                        shard_docs.add(e)
            elif isinstance(ev, dict) and ev.get("doc"):
                shard_docs.add(ev["doc"])
            elif isinstance(ev, str):
                shard_docs.add(ev)
            for d in comp.get("distractors", []):
                dev = d.get("evidence")
                if isinstance(dev, dict) and dev.get("doc"):
                    shard_docs.add(dev["doc"])
                elif isinstance(dev, str):
                    shard_docs.add(dev)

        # Cross evidence.doc with pre_cta_manifest
        matched_sources: List[str] = []
        for doc in sorted(shard_docs):
            doc_name = Path(doc).name.lower()
            matched = False
            for item in candidate_sources:
                if isinstance(item, str):
                    if doc_name == Path(item).name.lower() or doc.lower() in item.lower():
                        if item not in matched_sources:
                            matched_sources.append(item)
                        matched = True
                elif isinstance(item, dict):
                    item_val = item.get("path") or item.get("doc") or item.get("file") or item.get("filename") or item.get("name")
                    if item_val and (doc_name == Path(str(item_val)).name.lower() or doc.lower() in str(item_val).lower()):
                        target_val = item.get("path") or str(item_val)
                        if target_val not in matched_sources:
                            matched_sources.append(target_val)
                        matched = True
            if not matched and doc not in matched_sources:
                matched_sources.append(doc)

        wave_idx = shard.get("wave_index", (idx // max_wave_size) + 1)
        shard_entry = {
            "shard_id": s_id,
            "shard_index": idx,
            "wave_index": wave_idx,
            "competencies": shard["competencies"],
            "competency_count": len(shard["competency_ids"]),
            "shard_data_path": shard_data_path_abs,
            "templates_dir": templates_dir_abs,
            "source_files": matched_sources,
            "competency_ids": shard["competency_ids"],
            "weight": shard["weight"],
            "estimated_weight": shard.get("estimated_weight", shard["weight"]),
        }
        manifest_shards.append(shard_entry)

        # Write self-contained shard json for backward compatibility & author isolation
        shard_file = out_dir / f"{s_id}.json"
        shard_payload = {
            "shard_id": s_id,
            "shard_index": idx,
            "wave_index": wave_idx,
            "total_shards": len(shards),
            "total_waves": shard.get("total_waves", math.ceil(len(shards) / max_wave_size)),
            "max_wave_size": max_wave_size,
            "weight": shard["weight"],
            "estimated_weight": shard.get("estimated_weight", shard["weight"]),
            "competency_ids": shard["competency_ids"],
            "course_id": cta_data.get("course_id", "course"),
            "course_title": cta_data.get("title", ""),
            "competencies": shard["competencies"],
            "expected_templates": [f"templates/{cid}.json" for cid in shard["competency_ids"]],
            "shard_data_path": shard_data_path_abs,
            "templates_dir": templates_dir_abs,
            "source_files": matched_sources,
            "dsl_reference": DSL_REFERENCE,
        }
        _atomic_write_json(shard_file, shard_payload)

    total_waves = math.ceil(len(shards) / max_wave_size) if shards else 1
    waves_summary = []
    for w in range(1, total_waves + 1):
        w_shards = [s["shard_id"] for s in manifest_shards if s.get("wave_index") == w]
        waves_summary.append({
            "wave_index": w,
            "shard_count": len(w_shards),
            "shard_ids": w_shards,
        })

    pre_shard_manifest_payload = {
        "cta_source": str(cta_file.as_posix()),
        "total_competencies": len(competencies),
        "total_shards": len(shards),
        "total_waves": total_waves,
        "max_wave_size": max_wave_size,
        "waves": waves_summary,
        "shards": manifest_shards,
    }

    # Write work/shards/pre_shard_manifest.json (Canonical v3.3 Manifest)
    pre_shard_manifest_file = out_dir / "pre_shard_manifest.json"
    _atomic_write_json(pre_shard_manifest_file, pre_shard_manifest_payload)

    # Clean up legacy manifest.json if present (strictly no manifest.json writing)
    legacy_manifest = out_dir / "manifest.json"
    if legacy_manifest.is_file():
        try:
            legacy_manifest.unlink()
        except Exception:
            pass

    return pre_shard_manifest_payload


def main():
    parser = argparse.ArgumentParser(description="Partition CTA competencies into balanced amortized shards")
    parser.add_argument("--cta", required=True, help="Path to cta.json")
    parser.add_argument("--output-dir", required=True, help="Output directory for shards (e.g. work/shards)")
    parser.add_argument("--k", type=int, default=None, help="Force specific shard count K")
    parser.add_argument("--comps-per-shard", type=int, default=DEFAULT_COMPS_PER_SHARD, help="Target max competencies per shard (default: 2 for Case 2B, change to 3 for Case 2A)")
    parser.add_argument("--max-wave-size", type=int, default=DEFAULT_MAX_WAVE_SIZE, help="Maximum number of author shards dispatched per wave (default: 10)")
    parser.add_argument("--no-isolate-skills", action="store_true", default=False, help="Disable 1-Skill-per-shard isolation rule")
    args = parser.parse_args()

    try:
        res = plan_shards(
            args.cta,
            args.output_dir,
            k=args.k,
            max_comps=args.comps_per_shard,
            max_wave_size=args.max_wave_size,
            isolate_skills=not args.no_isolate_skills,
        )
    except FileNotFoundError as ex:
        if "BLOCKER::" in str(ex):
            sys.exit(2)
        raise

    print(f"[+] Successfully partitioned {res['total_competencies']} competencies into {res['total_shards']} shards (total waves: {res['total_waves']}):")
    for s in res["shards"]:
        print(f"    - [{s['shard_id']}] (wave {s.get('wave_index')}) {s['competency_count']} competencies (weight={s['weight']}): {', '.join(s['competency_ids'])}")


if __name__ == "__main__":
    main()
