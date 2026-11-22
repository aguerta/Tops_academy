"""Dynamic Competency Sharding Engine for content-to-course v3.3.

Partitions CTA competencies into balanced shards with Milestone 7.4 Cognitive Sharding:
- Skill Grouping Rule: Skill competencies ('Hab-*') are grouped in curriculum order in blocks of up to
  MAX_SKILLS_PER_SHARD = 2 per shard (default: 2), isolated from non-skill competencies.
- Contiguous Concept/Fact Grouping: Consecutive non-skill competencies are packed up to
  DEFAULT_COMPS_PER_SHARD = 3 competencies per shard (default: 3).
- Heaviest-First Ordering: Shards are sorted descending by weight (Skill=6.0, Concept=2.5, Fact=1.5 + 0.1*distractors)
  so all Skill shards sit at the front of Wave 1 (t = 0).
- Wave Indexing: Single-wave maximum parallelism by default (max_wave_size default: 100, Heaviest-First at t = 0).
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from engine.stage_contract import MIN_ARCHETYPES as _SC_MIN_ARCHETYPES
    MIN_ARCHETYPES = _SC_MIN_ARCHETYPES if _SC_MIN_ARCHETYPES >= 4 else 4
except Exception:
    MIN_ARCHETYPES = 4
from engine.stage_contract import (  # noqa: E402
    DEFAULT_TEMPLATES_PER_MODALITY,
    MAX_MODALITIES_PER_COMPETENCY,
    MIN_MODALITIES_PER_COMPETENCY,
    competency_contract,
    global_contract,
    render_contract_tokens,
    required_templates_for_competency,
)

# =============================================================================
# SHARD & TEMPLATE SCALING CONFIGURATION
# Capacidad por shard:
#   DEFAULT_COMPS_PER_SHARD = 3 (máximo 3 competencias no-skill por shard)
#   MAX_SKILLS_PER_SHARD = 2 (máximo 2 competencias skill por shard)
#   T >= 4 (mínimo 4 plantillas disjuntas por competencia: Directa, Inversa, Perturbación, Frontera; +MC7 adicionales si TPL-D3 excede capacidad base)
# =============================================================================
DEFAULT_COMPS_PER_SHARD: int = 3
MAX_SKILLS_PER_SHARD: int = 2
DEFAULT_MAX_WAVE_SIZE: int = 100


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
    "min_archetypes": MIN_ARCHETYPES,
    "templates_per_modality": DEFAULT_TEMPLATES_PER_MODALITY,
    "min_modalities": MIN_MODALITIES_PER_COMPETENCY,
    "max_modalities": MAX_MODALITIES_PER_COMPETENCY,
    "description": "Form-C Quad-Band dicts in TEMPLATES (or 9-tupla legacy) with min_archetypes = 4 (direct, inverse, perturbation, boundary_or_edge_case) and N_min = max(4, M * K) (Skill: 0 MC7; Concept/Fact: <= 1 MC7 y >= 80% activo => N_min = max(4, 5, 1 + (M-1)*K) si el plan incluye MC7)",
    "canonical_template_schema": "{'id': '^T-...', 'cid': '...', 'qtype': '...', 'archetype': '...', 'band': (diff, bloom), 'gen': gen_fn, 'ver': ver_fn, 'stem_variants': [...], 'hints': [...], 'sol': '...', 'rats': RATS}",
    "supported_question_types": [
        "multiple_choice_7_options",
        "fill_in_the_blank",
        "multiple_select",
        "open_symbolic",
        "proof_dag",
        "adversarial_break",
        "unstructured_model",
        "invariant_canvas",
        "concept_matching",
    ],
    "distractor_rules": {
        "mc7_tuple_format": "(did, val, rationale_con_@var@)",
        "min_rationale_length": 20,
        "requires_var_interpolation": True,
    },
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
            f"python .agents/skills/content-to-course/compile_shard.py --input work/shards/<shard_id>_data.py --output work/shards/<shard_id>.json --strict --min-archetypes 4 --templates-per-modality {DEFAULT_TEMPLATES_PER_MODALITY}"
        ),
        "quotas": (
            f"Para CADA competencia asignada: autorar un MÍNIMO OBLIGATORIO de N_min = max(4, M * K) plantillas paramétricas (si una competencia Concept/Fact incluye MC7: exactamente 1 MC7 y N_min = max(4, 5, 1 + (M-1)*K); en Skill MC7 está prohibido, [M20-MC7-CAP]/[M20-ACTIVE-QUOTA]) "
            f"disjuntas (con K = {DEFAULT_TEMPLATES_PER_MODALITY} por defecto vía --templates-per-modality K, M = len(recommended_modalities) "
            f"en [{MIN_MODALITIES_PER_COMPETENCY}..{MAX_MODALITIES_PER_COMPETENCY}], cubriendo >= K plantillas distintas por cada modalidad recomendada, "
            f"los 4 arquetipos Form-C 'direct', 'inverse', 'perturbation', 'boundary_or_edge_case', las 3 bandas easy/medium/hard y >= 2 niveles Bloom). "
            f"Las modalidades concretas se rigen por las 'recommended_modalities' decididas por el CTA Architect para cada competencia "
            f"(catálogo activo: FIB con 'ds', open_symbolic, MS, MC7, proof_dag, adversarial_break, unstructured_model, "
            f"invariant_canvas, concept_matching; sin cuotas fijas rígidas por tipo). "
            f"Si una competencia declara en cta.json más distractores de los que caben en una sola plantilla, "
            f"cubre 100% de distractor_ids mediante 'ds' diagnósticos en FIB/open_symbolic, MS, modalidades Bloom Superior "
            f"o MC7 si forma parte del plan del CTA Architect."
        ),
        "anti_clone": (
            "4 Candados Deterministas Anti-Clon intra-competencia en compile_shard.py: "
            "(1) [TPL-CLONE-AST]: AST normalizado de 'gen' estrictamente distinto dentro de la misma modalidad o arquetipo; "
            "(2) [TPL-CLONE-BAND]: tupla (archetype, difficulty, bloom) única dentro de cada modalidad cuando K <= 4; "
            "(3) [TPL-CLONE-STEM]: similitud léxica Jaccard < 0.70 en stem_variants entre plantillas de igual modalidad o arquetipo; "
            "(4) [TPL-CLONE-SYMPY]: expresiones algebraicas no equivalentes bajo SymPy dentro del mismo arquetipo."
        ),
        "bloom_coherence": (
            "[M3-BLOOM-COHERENCE] y [M3-TARGET-BLOOM]: Respeta los rangos coherentes modalidad x arquetipo x Bloom "
            "(MC7 <= Apply; concept_matching <= Analyze; FIB direct <= Apply y FIB <= Analyze; "
            "adversarial_break/unstructured_model >= Analyze; proof_dag >= Apply). En competencias Concept/Skill v2, "
            "al menos 1 plantilla (idealmente boundary_or_edge_case o perturbation) debe alcanzar el target_bloom factible."
        ),
        "form_b_triband": (
            "Contrato Form-C / Form-B (min_archetypes = 4): Cada plantilla se declara como una 9-tupla o dict Form-C "
            "por competencia cubriendo los 4 arquetipos ortogonales ('direct', 'inverse', 'perturbation', 'boundary_or_edge_case') "
            "con >= 2 niveles Bloom y las modalidades decididas en 'recommended_modalities' por el CTA Architect."
        ),
        "distractor_coverage": (
            "Regla TPL-D3: 100% de los distractor_ids declarados en cta.json deben cubrirse en la semilla representativa "
            "de las plantillas de la competencia (via 'ds' en FIB/open_symbolic, MS, pasos falaces/distractores en modalidades "
            "Bloom Superior o MC7 con exactamente 6 distractores en 3-tupla (did, val, rationale_con_@var@)). Sin cuotas rígidas fijas por tipo."
        ),
        "dynamic_rationale": (
            "[TPL-DYNAMIC-RATIONALE]: En MC7, cada distractor DEBE declararse como una 3-tupla (did, val, rationale_con_@var@) "
            "con len(rationale) >= 20 interpolando variables paramétricas. En MS, las opciones falsas deben incluir "
            "'error_rationale' interpolando @var@. Prohibido omitir rationale."
        ),
        "fib_naked_contract": (
            "[TPL-FIB-KATEX]: En fill_in_the_blank, el valor numérico o algebraico esperado en 'correct' y 'answer_contract' "
            "no debe incluir signos de dólar externos '$...$'."
        ),
        "katex_prose_overflow": (
            "[KATEX-PROSE-OVERFLOW]: Prohibido colocar fragmentos de prosa mayores a 45 caracteres dentro de \\text{...}. "
            "La prosa explicativa debe ubicarse fuera de $...$."
        ),
        "tpl_var_mandatory": render_contract_tokens(
            "Regla TPL-VAR-MANDATORY: Declarar obligatoriamente entre <<S4_VARIANTS_OTHER>> y 5 'stem_variants' "
            "(directa/conceptual, contextualizada, analítica/simbólica) con placeholders @var@ o {var} en cada plantilla. "
            "Stage 4 exige stems únicos enmascarados >= <<S4_UNIQ_SKILL>> (Skill, cuota <<S4_QUOTA_SKILL>>) o >= <<S4_UNIQ_OTHER>> "
            "(Concept/Fact, cuota <<S4_QUOTA_OTHER>>), ratio >= <<S4_RATIO>> (ver stage4_contract del shard)."
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
            "SOPORTE NATIVO DE GRÁFICOS: Para diagramas o curvas analíticas, Top's Academy soporta "
            "el esquema JSON nativo 'graph': {'title': str, 'x_axis': {'label': str, 'min': float, 'max': float}, "
            "'y_axis': {'label': str, 'min': float, 'max': float}, 'curves': [{'name': str, 'fn': str, 'style': 'solid'}], "
            "'points': [{'name': str, 'x': float, 'y': float, 'label': str}]}. NO simular gráficos en puro texto KaTeX."
        ),
        "shard_isolated_script": (
            "SCRIPT INDEPENDIENTE: Cada shard escribe exclusivamente su propio script work/shards/<shard_id>_data.py. "
            "Valida únicamente tu shard asignado: python .agents/skills/content-to-course/compile_shard.py "
            f"--input work/shards/<shard_id>_data.py --output work/shards/<shard_id>.json --strict --min-archetypes 4 --templates-per-modality {DEFAULT_TEMPLATES_PER_MODALITY}"
        ),
        "modular_per_comp_overrides": (
            "SOPORTE MODULAR DE CORRECCIONES POR COMPETENCIA: Si una competencia específica requiere corrección "
            "o parchado aislado sin recompilar todo el shard, escribir el módulo en work/shards/shard_fixes/<CID>.py "
            "con la plantilla corregida."
        ),
    },
    "canonical_examples": {
        "tuple_signature": "(tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution)",
        "multiple_choice_7_options": {
            "template_id": "T-SAMPLE-01",
            "competency_id": "<comp_id>",
            "question_type": "multiple_choice_7_options",
            "difficulty": "medium",
            "bloom": "Understand",
            "stems": [
                r"Considere un conductor óhmico con resistencia $R = @R@\text{ }\Omega$ por el que circula corriente $I = @I@\text{ A}$. Calcule la potencia disipada $P = I^2 R$:",
                r"Para un elemento resistivo lineal de $R = @R@\text{ }\Omega$ sometido a una corriente estacionaria $I = @I@\text{ A}$, determine la tasa de disipación de energía $P$:",
                r"Dado un circuito con resistencia nominal $R = @R@\text{ }\Omega$ e intensidad de corriente $I = @I@\text{ A}$, halle la potencia activa disipada por efecto Joule:",
            ],
            "generate_py": (
                "def gen_sample_mc7(rng):\n"
                "    R = rng.randint(3, 15)\n"
                "    I = rng.randint(2, 9)\n"
                "    P = (I**2) * R\n"
                "    d1 = I * R\n"
                "    d2 = (I**2) * (R + 2)\n"
                "    d3 = 2 * I * R\n"
                "    d4 = I * (R**2)\n"
                "    d5 = (I**2) + R\n"
                "    d6 = round((I**2) / R, 4)\n"
                "    return {\n"
                "        'vars': {'R': R, 'I': I, 'P': P, 'd1': d1, 'd2': d2, 'd3': d3, 'd4': d4, 'd5': d5, 'd6': d6},\n"
                "        'correct': f'$P = {P}\\\\text{{ W}}$',\n"
                "        'distractors': [\n"
                "            ('D-01', f'$P = {d1}\\\\text{{ W}}$', f'Omite elevar la corriente al cuadrado calculando $I \\\\cdot R = {d1}$ en lugar de $I^2 R$.'),\n"
                "            ('D-02', f'$P = {d2}\\\\text{{ W}}$', f'Suma resistencia parásita espuria calculando $I^2(R+2) = {d2}$ sin justificación física.'),\n"
                "            ('D-03', f'$P = {d3}\\\\text{{ W}}$', f'Multiplica por dos la potencia lineal $2 I R = {d3}$ confundiendo exponente cuadrático.'),\n"
                "            ('D-04', f'$P = {d4}\\\\text{{ W}}$', f'Aplica el cuadrado erróneamente a la resistencia $I R^2 = {d4}$ en lugar de la corriente.'),\n"
                "            ('D-05', f'$P = {d5}\\\\text{{ W}}$', f'Suma aditivamente los términos $I^2 + R = {d5}$ en vez de multiplicar factores.'),\n"
                "            ('D-06', f'$P = {d6}\\\\text{{ W}}$', f'Divide por la resistencia $I^2 / R = {d6}$ invirtiendo la formulación dimensional.'),\n"
                "        ]\n"
                "    }"
            ),
            "cross_check_py": (
                "def ver_sample_mc7(result):\n"
                "    R = result['vars']['R']\n"
                "    I = result['vars']['I']\n"
                "    return result['vars']['P'] == (I**2) * R"
            ),
            "hints": [
                "Identifique la relación fundamental de potencia disipada en función de corriente y resistencia.",
                "Recuerde elevar la corriente al cuadrado antes de multiplicarla por el valor de la resistencia.",
                "Verifique que las unidades resultantes correspondan a Watts en el Sistema Internacional.",
            ],
            "solution": r"Aplicando la relación de disipación Joule, $P = I^2 R = (@I@)^2 \cdot @R@ = @P@\text{ W}$.",
            "distractor_ids": ["D-01", "D-02", "D-03", "D-04", "D-05", "D-06"],
        },
        "fill_in_the_blank": {
            "template_id": "T-SAMPLE-02",
            "competency_id": "<comp_id>",
            "question_type": "fill_in_the_blank",
            "difficulty": "easy",
            "bloom": "Apply",
            "stems": [
                r"Calcule el valor escalar de la resistencia equivalente en serie de dos resistores $R_1 = @r1@\text{ }\Omega$ y $R_2 = @r2@\text{ }\Omega$:",
                r"Determine numéricamente la resistencia total de una rama con resistores en serie $R_1 = @r1@\text{ }\Omega$ y $R_2 = @r2@\text{ }\Omega$:",
                r"Halle la resistencia neta equivalente resultante de conectar en serie $R_1 = @r1@\text{ }\Omega$ junto a $R_2 = @r2@\text{ }\Omega$:",
            ],
            "generate_py": (
                "def gen_sample_fib(rng):\n"
                "    r1 = rng.randint(10, 45)\n"
                "    r2 = rng.randint(5, 30)\n"
                "    req = r1 + r2\n"
                "    return {\n"
                "        'vars': {'r1': r1, 'r2': r2, 'req': req},\n"
                "        'correct': str(req),\n"
                "        'value': str(req),\n"
                "        'canonical_algebraic': str(req),\n"
                "        'accepted_equivalents': [str(req), f'{req}.0'],\n"
                "        'tolerance': 0.01,\n"
                "        'distractors': []\n"
                "    }"
            ),
            "cross_check_py": (
                "def ver_sample_fib(result):\n"
                "    r1 = result['vars']['r1']\n"
                "    r2 = result['vars']['r2']\n"
                "    return int(result['correct']) == (r1 + r2)"
            ),
            "hints": [
                "Para resistores conectados en serie, las resistencias individuales se suman directamente.",
                "Sume los dos valores escalares r1 y r2 para obtener la resistencia total.",
                "Ingrese el resultado escalar sin signos de dólar ni unidades en la casilla de respuesta.",
            ],
            "solution": r"La resistencia equivalente en serie es la suma directa: $R_{eq} = R_1 + R_2 = @r1@ + @r2@ = @req@\text{ }\Omega$.",
            "distractor_ids": [],
        },
        "multiple_select": {
            "template_id": "T-SAMPLE-03",
            "competency_id": "<comp_id>",
            "question_type": "multiple_select",
            "difficulty": "hard",
            "bloom": "Analyze",
            "stems": [
                r"Para un sistema térmico cerrado que absorbe calor $Q = @Q@\text{ J}$ y realiza trabajo $W = @W@\text{ J}$, seleccione todas las afirmaciones analíticamente verdaderas:",
                r"Considere un gas ideal que recibe transferencia de calor $Q = @Q@\text{ J}$ realizando trabajo mecánico $W = @W@\text{ J}$. Identifique las proposiciones correctas:",
                r"En un proceso termodinámico con calor neto $Q = @Q@\text{ J}$ y trabajo de expansión $W = @W@\text{ J}$, marque todas las conclusiones cuantitativas válidas:",
            ],
            "generate_py": (
                "def gen_sample_ms(rng):\n"
                "    Q = rng.randint(50, 120)\n"
                "    W = rng.randint(15, 45)\n"
                "    delta_u = Q - W\n"
                "    opts = [\n"
                "        {'content': f'El cambio de energía interna satisface $\\\\Delta U = {delta_u}\\\\text{{ J}}$.', 'is_correct': True, 'distractor_id': None},\n"
                "        {'content': 'La energía interna aumenta porque el calor absorbido excede el trabajo realizado.', 'is_correct': True, 'distractor_id': None},\n"
                "        {'content': f'El cambio de energía interna es $\\\\Delta U = {Q + W}\\\\text{{ J}}$ sumando calor y trabajo.', 'is_correct': False, 'distractor_id': 'D-01', 'error_rationale': f'Suma erróneamente trabajo al calor obteniendo $\\\\Delta U = {Q + W}$ en lugar de $Q - W$.'},\n"
                "        {'content': f'El cambio de energía interna es $\\\\Delta U = {W - Q}\\\\text{{ J}}$ invirtiendo la resta.', 'is_correct': False, 'distractor_id': 'D-02', 'error_rationale': f'Invierte los signos del balance energético obteniendo ${W - Q}$ en vez de $Q - W$.'},\n"
                "    ]\n"
                "    return {\n"
                "        'vars': {'Q': Q, 'W': W, 'delta_u': delta_u},\n"
                "        'options': opts,\n"
                "        'distractors': []\n"
                "    }"
            ),
            "cross_check_py": (
                "def ver_sample_ms(result):\n"
                "    Q = result['vars']['Q']\n"
                "    W = result['vars']['W']\n"
                "    return result['vars']['delta_u'] == (Q - W)"
            ),
            "hints": [
                "Aplique la primera ley de la termodinámica para sistemas cerrados: Delta U = Q - W.",
                "Calcule la diferencia aritmética entre el calor suministrado y el trabajo realizado.",
                "Evalúe la coherencia física del signo resultante sobre la energía interna del sistema.",
            ],
            "solution": r"Por la primera ley, $\Delta U = Q - W = @Q@ - @W@ = @delta_u@\text{ J}$. Como $Q > W$, la energía interna aumenta.",
            "distractor_ids": ["D-01", "D-02"],
        },
    },
}


def _dsl_reference_for_k(k: int) -> Dict[str, Any]:
    """Return DSL_REFERENCE with templates_per_modality / K strings aligned to the effective K."""
    import copy as _copy
    ref = _copy.deepcopy(DSL_REFERENCE)
    try:
        k_int = max(1, int(k))
    except (TypeError, ValueError):
        return ref
    if k_int == DEFAULT_TEMPLATES_PER_MODALITY:
        return ref
    ref["templates_per_modality"] = k_int

    def _sub(node: Any) -> Any:
        if isinstance(node, str):
            return (
                node.replace(
                    f"--templates-per-modality {DEFAULT_TEMPLATES_PER_MODALITY}",
                    f"--templates-per-modality {k_int}",
                ).replace(
                    f"K = {DEFAULT_TEMPLATES_PER_MODALITY} por defecto",
                    f"K = {k_int} por defecto",
                )
            )
        if isinstance(node, dict):
            return {kk: _sub(vv) for kk, vv in node.items()}
        if isinstance(node, list):
            return [_sub(x) for x in node]
        return node

    return _sub(ref)


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
    if ctype in ("fact", "facts", "h", "hecho", "hechos"):
        return True
    if ctype in ("concept", "concepts", "c", "concepto", "conceptos"):
        return False
    cid = str(comp.get("id", "")).strip().upper()
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
    if ctype in ("concept", "concepts", "c", "concepto", "conceptos"):
        return True
    if ctype in ("fact", "facts", "h", "hecho", "hechos"):
        return False
    cid = str(comp.get("id", "")).strip().upper()
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
    extra_templates = 0.0
    rec_mods_w = comp.get("recommended_modalities")
    if isinstance(rec_mods_w, list) and rec_mods_w:
        n_mods_w = len({str(m).strip().lower() for m in rec_mods_w if str(m).strip()})
        n_req_w = required_templates_for_competency(n_mods_w, DEFAULT_TEMPLATES_PER_MODALITY)
        extra_templates = 0.5 * max(0, n_req_w - MIN_ARCHETYPES)
    return round(base + (0.1 * distractors_count) + extra_templates, 2)


def _compute_distractor_template_guidance(
    competencies: List[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    """Compute per-competency distractor coverage guidance aligned with CTA recommended_modalities."""
    guidance: Dict[str, Dict[str, Any]] = {}
    for comp in competencies:
        if not isinstance(comp, dict):
            continue
        cid = str(comp.get("id", "")).strip()
        if not cid:
            continue
        distractors_raw = comp.get("distractors")
        n_distractors = len(distractors_raw) if isinstance(distractors_raw, list) else 0
        rec_mods = comp.get("recommended_modalities") or []
        if n_distractors > 6:
            max_mc7_allowed = 0 if is_skill_competency(comp) else 1
            min_mc7_only = max_mc7_allowed
            min_mc7_with_ms4 = max_mc7_allowed
            exceeds_base_multimodal = n_distractors > 10
            entry: Dict[str, Any] = {
                "n_distractors": n_distractors,
                "recommended_modalities": list(rec_mods),
                "mc7_capacity_per_seed": 6,
                "ms_capacity_per_seed": "2-4",
                "max_mc7_allowed": max_mc7_allowed,
                "min_mc7_if_mc7_only": min_mc7_only,
                "min_mc7_with_ms4": min_mc7_with_ms4,
                "exceeds_base_multimodal": exceeds_base_multimodal,
            }
            if exceeds_base_multimodal:
                entry["warning"] = (
                    f"{cid} declara {n_distractors} distractores. Para cumplir TPL-D3 (100% cobertura por semilla) "
                    f"respetando las modalidades decididas por el CTA Architect ({rec_mods or 'libre elección'}), "
                    f"distribuye los distractor_ids mediante 'ds' en FIB/open_symbolic, MS o modalidades Bloom Superior."
                )
            guidance[cid] = entry
    return guidance


def determine_shard_count(
    competencies: Union[List[Dict[str, Any]], int],
    avg_distractors: Optional[Union[float, int]] = None,
    requested_k: Optional[int] = None,
    max_comps_per_shard: Optional[int] = DEFAULT_COMPS_PER_SHARD,
) -> int:
    """Determine shard count K with sweet-spot amortized sharding (non-skill: max 3 per shard; skill: max 2 per shard).

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
        # Adaptive Shard Sizing: target max comps per shard clamped to DEFAULT_COMPS_PER_SHARD (3 non-skill; skills capped separately at 2)
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


def _build_raw_shard(
    chunk: List[Dict[str, Any]],
    curriculum_indices: Dict[str, int],
    is_skill: bool,
) -> Dict[str, Any]:
    """Build a raw weighted shard dict from a chunk of competencies."""
    w = round(sum(calculate_competency_weight(x) for x in chunk), 2)
    c_ids = [x.get("id", "") for x in chunk]
    return {
        "weight": w,
        "estimated_weight": w,
        "competency_ids": c_ids,
        "competencies": chunk,
        "min_curriculum_idx": min(curriculum_indices.get(x_id, 0) for x_id in c_ids),
        "is_skill": is_skill,
    }


def partition_competencies_weighted(
    competencies: List[Dict[str, Any]],
    max_comps: Optional[int] = DEFAULT_COMPS_PER_SHARD,
    max_skills: Optional[int] = MAX_SKILLS_PER_SHARD,
) -> List[Dict[str, Any]]:
    """Partition competencies using Milestone 7.4 Weighted Cognitive Sharding:

    1. Skill Grouping Rule:
       Skill competencies ('Hab-*' or type == 'skill') are grouped in curriculum order
       in blocks of up to max_skills (default: MAX_SKILLS_PER_SHARD = 2) per shard.

    2. Contiguous Concept/Fact Grouping:
       Adjacent concept ('C-*') and fact ('H-*') competencies in curriculum order are packed
       in blocks of up to max_comps (default: DEFAULT_COMPS_PER_SHARD = 3) per shard.
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

    # 1. Skill Grouping: Pack skills in curriculum order in blocks of up to eff_max_skills
    eff_max_skills = max(1, int(max_skills) if max_skills is not None else MAX_SKILLS_PER_SHARD)
    skills = [c for c in competencies if is_skill_competency(c)]
    for s_idx in range(0, len(skills), eff_max_skills):
        chunk = skills[s_idx:s_idx + eff_max_skills]
        raw_shards.append(_build_raw_shard(chunk, curriculum_indices, is_skill=True))

    # 2. Contiguous Concept/Fact Grouping: Group non-skills in curriculum order
    target_max = max_comps if (max_comps is not None and max_comps > 0) else DEFAULT_COMPS_PER_SHARD
    non_skills = [c for c in competencies if not is_skill_competency(c)]
    idx = 0
    m = len(non_skills)
    while idx < m:
        remaining = m - idx
        take = min(target_max, remaining)
        chunk = non_skills[idx:idx + take]
        raw_shards.append(_build_raw_shard(chunk, curriculum_indices, is_skill=False))
        idx += take

    return raw_shards


def plan_shards(
    cta_path: Union[str, Path],
    output_dir: Union[str, Path],
    k: Optional[int] = None,
    max_comps: Optional[int] = None,
    max_wave_size: int = DEFAULT_MAX_WAVE_SIZE,
    isolate_skills: bool = True,
    max_skills: Optional[int] = None,
    templates_per_modality: Optional[int] = None,
) -> Dict[str, Any]:
    """Execute sharding on cta.json and write pre_shard_manifest.json (v3.3 canonical)."""
    eff_tpl_per_mod = (
        DEFAULT_TEMPLATES_PER_MODALITY
        if templates_per_modality is None
        else max(1, int(templates_per_modality))
    )
    eff_max_skills = (
        (1 if eff_tpl_per_mod >= 3 else MAX_SKILLS_PER_SHARD)
        if max_skills is None
        else max(1, int(max_skills))
    )
    eff_max_comps = (
        (2 if eff_tpl_per_mod >= 3 else DEFAULT_COMPS_PER_SHARD)
        if max_comps is None
        else max(1, int(max_comps))
    )
    if max_comps is not None and max_skills is None:
        eff_max_skills = min(eff_max_skills, eff_max_comps)

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

    for c in competencies:
        if isinstance(c, dict):
            c.setdefault("assumptions", [])
            rec_mods = c.get("recommended_modalities") or []
            dists = c.get("distractors") or []
            if isinstance(rec_mods, list) and "multiple_choice_7_options" in rec_mods and len(dists) < 6:
                cid_label = c.get("id", "<unknown>")
                raise ValueError(
                    f"[CTA-MC7-DISTRACTORS] Competency '{cid_label}' includes "
                    f"'multiple_choice_7_options' (MC7) in recommended_modalities but only declares "
                    f"{len(dists)} distractors (MC7 requires >= 6 distinct distractors)."
                )

    # Partitioning Strategy Selection
    if k is not None or not isolate_skills:
        # Legacy explicit K partitioning
        shard_count = determine_shard_count(competencies, requested_k=k, max_comps_per_shard=eff_max_comps)
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
        raw_shards = partition_competencies_weighted(
            competencies,
            max_comps=eff_max_comps,
            max_skills=eff_max_skills,
        )
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
    # Stage 4 authority: type is read exactly as run.py --stage build reads it (comp["type"]).
    cta_type_by_cid = {
        str(c.get("id")): ("skill" if is_skill_competency(c) else str(c.get("type", "concept")))
        for c in competencies
        if isinstance(c, dict) and c.get("id")
    }
    cta_rec_mods_by_cid = {
        str(c.get("id")): list(c.get("recommended_modalities") or [])
        for c in competencies
        if isinstance(c, dict) and c.get("id")
    }
    cta_bloom_by_cid = {
        str(c.get("id")): str(c.get("bloom") or "").strip()
        for c in competencies
        if isinstance(c, dict) and c.get("id")
    }
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
        s4_by_cid = {}
        for cid_s4 in shard["competency_ids"]:
            rec_mods_s4 = cta_rec_mods_by_cid.get(cid_s4) or []
            _mc7_aliases = {"mc7", "mc_7", "mc", "multiple_choice", "multiple-choice", "multiple_choice_7_options", "single_choice"}
            _canon_alias = {"fib": "fill_in_the_blank", "ms": "multiple_select", **{a: "multiple_choice_7_options" for a in _mc7_aliases}}
            norm_mods_s4 = list(dict.fromkeys(
                _canon_alias.get(str(m).strip().lower(), str(m).strip().lower()) for m in rec_mods_s4 if str(m).strip()
            ))
            num_mods_s4 = len(norm_mods_s4)
            has_mc7_s4 = "multiple_choice_7_options" in norm_mods_s4
            s4_by_cid[cid_s4] = competency_contract(
                cta_type_by_cid.get(cid_s4, "concept"),
                num_modalities=num_mods_s4,
                templates_per_modality=eff_tpl_per_mod,
                has_mc7=has_mc7_s4,
                target_bloom=cta_bloom_by_cid.get(cid_s4) or None,
            )
        shard_entry = {
            "shard_id": s_id,
            "templates_per_modality": eff_tpl_per_mod,
            "stage4_contract": s4_by_cid,
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
        distractor_guidance = _compute_distractor_template_guidance(shard["competencies"])
        shard_payload = {
            "shard_id": s_id,
            "shard_index": idx,
            "wave_index": wave_idx,
            "total_shards": len(shards),
            "total_waves": shard.get("total_waves", math.ceil(len(shards) / max_wave_size)),
            "max_wave_size": max_wave_size,
            "templates_per_modality": eff_tpl_per_mod,
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
            "dsl_reference": _dsl_reference_for_k(eff_tpl_per_mod),
            "stage4_contract": {"global": global_contract(templates_per_modality=eff_tpl_per_mod), "per_competency": s4_by_cid},
        }
        if distractor_guidance:
            shard_payload["distractor_guidance"] = distractor_guidance
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
        "min_archetypes": MIN_ARCHETYPES,
        "templates_per_modality": eff_tpl_per_mod,
        "max_skills_per_shard": eff_max_skills,
        "comps_per_shard": eff_max_comps,
        "stage4_contract": global_contract(templates_per_modality=eff_tpl_per_mod),
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
    parser.add_argument("--comps-per-shard", type=int, default=None, help="Target max non-skill competencies per shard (default: 3, or 2 when templates-per-modality >= 3)")
    parser.add_argument("--max-skills-per-shard", type=int, default=None, help="Max skill competencies per shard (default: 2, or 1 when templates-per-modality >= 3)")
    parser.add_argument("--templates-per-modality", type=int, default=DEFAULT_TEMPLATES_PER_MODALITY, help=f"Minimum distinct templates per recommended modality (default: {DEFAULT_TEMPLATES_PER_MODALITY})")
    parser.add_argument("--max-wave-size", type=int, default=DEFAULT_MAX_WAVE_SIZE, help="Maximum number of author shards dispatched per wave (default: 100)")
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
            max_skills=args.max_skills_per_shard,
            templates_per_modality=args.templates_per_modality,
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
