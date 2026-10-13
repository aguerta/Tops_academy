"""Scope Isolation, Subagent Dispatch Payload Generator, and Scope Check.

Provides strict scope isolation contracts for all pipeline subagents:
- vision: Handout Vision Analyzers
- cta-map: Sectional CTA Mappers
- cta-reduce: CTA Harmonizer
- author: Shard Exercise Authors
- judge: Blind Evaluation Judges
- cta-direct / vision-legacy: Fallback legacy flows
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import logging
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

logger = logging.getLogger("dispatch")

# Directory of the skill
SKILL_DIR = Path(__file__).parent.resolve()

TYPE_DEFINITIONS: List[Dict[str, Any]] = [
    {
        "name": "c2c-vision",
        "description": "Handout Vision Analyzer for mathematical transcriptions",
        "system_prompt": "You are a specialized Handout Vision Analyzer for Content-to-Course. Read your assigned task bundle in work/dispatch/bundles/ and produce transcription patches. Terminate strictly with DONE: <files>.",
        "enable_write_tools": True,
        "enable_subagent_tools": False,
        "enable_mcp_tools": False,
    },
    {
        "name": "c2c-cta-mapper",
        "description": "Sectional Cognitive Task Analysis Mapper",
        "system_prompt": "You are a Sectional Curriculum Analyst for Content-to-Course. Read your assigned task bundle in work/dispatch/bundles/ and produce cta_part JSON. Terminate strictly with DONE: <files>.",
        "enable_write_tools": True,
        "enable_subagent_tools": False,
        "enable_mcp_tools": False,
    },
    {
        "name": "c2c-cta-harmonizer",
        "description": "Curriculum Harmonization subagent",
        "system_prompt": "You are a Curriculum Harmonization specialist for Content-to-Course. Read your assigned task bundle in work/dispatch/bundles/ and resolve duplicate competencies. Terminate strictly with DONE: <files>.",
        "enable_write_tools": True,
        "enable_subagent_tools": False,
        "enable_mcp_tools": False,
    },
    {
        "name": "c2c-author",
        "description": "Psychometric Exercise Author for parametric templates (refinamiento quirúrgico con replace_file_content sobre scaffolds pre-sembrados; prohibido leer bundles en turno 1; prohibido chat emissions)",
        "system_prompt": "You are a Lead Psychometric Assessment Author for Content-to-Course. Directly refine parametric templates in work/templates/<comp_id>.json on pre-seeded scaffolds using replace_file_content. Strictly forbidden to waste turns reading task bundles or system prompts in Turn 1, forbidden to inspect engine or validator code, forbidden to create monolithic scripts, and forbidden to output template JSON in chat text. Terminate strictly with DONE: <files>.",
        "enable_write_tools": True,
        "enable_subagent_tools": False,
        "enable_mcp_tools": False,
    },
    {
        "name": "c2c-judge",
        "description": "Blind Psychometric Evaluation Judge",
        "system_prompt": "You are an Independent Blind Evaluation Judge for Content-to-Course. Read your assigned task bundle in work/dispatch/bundles/ and analytically solve questions with zero access to answer keys. Terminate strictly with DONE: <files>.",
        "enable_write_tools": True,
        "enable_subagent_tools": False,
        "enable_mcp_tools": False,
    },
    {
        "name": "c2c-cta-direct",
        "description": "Direct CTA Architect for concise courses (arquitectura de 2 archivos: cta_data.py tabular y compile_cta.py; lotes de máximo 10 competencias; prohibido chat emissions)",
        "system_prompt": "You are a Direct CTA Architect for Content-to-Course. Directly synthesize competencies into pure tabular tuples in work/cta_data.py using the 2-file architecture, then compile and certify with 'python work/compile_cta.py'. Batches of max 10 competencias per chunk. Strictly forbidden to modify compile_cta.py, create auxiliary scripts, or output competencies in chat text. Terminate strictly with DONE: work/cta.json.",
        "enable_write_tools": True,
        "enable_subagent_tools": False,
        "enable_mcp_tools": False,
    },
    {
        "name": "c2c-repair",
        "description": "Targeted Repair subagent for fixing failing templates or discordances",
        "system_prompt": "You are a Targeted Quality Repair Engineer for Content-to-Course. Read your assigned task bundle in work/dispatch/bundles/ and resolve only diagnosed errors on failing templates. Terminate strictly with DONE: <files>.",
        "enable_write_tools": True,
        "enable_subagent_tools": False,
        "enable_mcp_tools": False,
    },
]

ROLE_SPECS: Dict[str, Dict[str, Any]] = {
    "vision": {
        "type_name": "c2c-vision",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_handout_transcriber.md",
        "read": [
            "work/handouts/handout_<id>.png",
            "work/handouts/handout_<id>_text.md",
        ],
        "write": [
            "work/handout_patches/patch_<id>.md",
            "work/handout_patches/patch_handout_<id>.md",
        ],
        "forbidden": [
            "código fuente",
            "corpus*.md",
            "otros handouts no asignados",
            "SKILL.md",
        ],
        "turn_budget": 10,
    },
    "cta-map": {
        "type_name": "c2c-cta-mapper",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_cta_sectional.md",
        "read": [
            "work/sections/section_XX.md",
            "work/sections/section_*.md",
        ],
        "write": [
            "work/cta_parts/cta_part_XX.json",
            "work/cta_parts/cta_part_*.json",
        ],
        "forbidden": [
            "otras secciones",
            "handouts",
            "código fuente",
        ],
        "turn_budget": 15,
    },
    "cta-reduce": {
        "type_name": "c2c-cta-harmonizer",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_cta_harmonizer.md",
        "read": [
            "work/cta_outline.json",
            "work/duplicate_candidates.json",
        ],
        "write": [
            "work/cta_harmonize.json",
        ],
        "forbidden": [
            "corpus*.md",
            "secciones",
            "código fuente",
        ],
        "turn_budget": 10,
    },
    "author": {
        "type_name": "c2c-author",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_shard_author.md",
        "description": "Shard Exercise Author: refinar quirúrgicamente plantillas paramétricas modulares (work/templates/<comp_id>.json) sobre scaffolds pre-sembrados utilizando prioritariamente replace_file_content.",
        "directives": [
            "Refinar quirúrgicamente los scaffolds pre-sembrados en work/templates/<comp_id>.json usando prioritariamente replace_file_content.",
            "Prohibido gastar Turno 1 leyendo bundles o system prompts: toda la asignación y comando de validación ya están incluidos en tu prompt.",
            "Prohibido escribir scripts monolíticos gigantes de 2,000 líneas (como build_<shard_id>.py) o scripts en el directorio scratch raíz compartido.",
            "Prohibido ejecutar comandos exploratorios o inspeccionar código del validador (check_templates.py, src/validator/*, engine/*).",
            "Do not output template JSON in chat text. Terminate strictly with DONE: <files>.",
            "Validar todas las plantillas del shard en un único comando oficial provisto en el prompt.",
        ],
        "read": [
            "work/templates/<comp_id>.json",
            "work/templates/*.json",
            "work/shards/shard_XX.json",
            "work/shards/shard_*.json",
            "work/cta.json",
            "content/**/*.pdf",
        ],
        "write": [
            "work/templates/<comp_id>.json",
            "work/templates/*.json",
            "work/shards/<shard_id>/scratch/**",
            "work/scratch/<shard_id>/**",
        ],
        "forbidden": [
            "engine/*",
            "SKILL.md",
            "otras plantillas fuera de su shard",
            "work/cta.json (READ-ONLY; strictly forbidden to edit, modify, or overwrite)",
            "check_templates.py",
            "src/validator/*",
            "rules.py",
            "system_prompts/* (todas las directivas están incluidas directamente en este prompt)",
            "work/dispatch/bundles/* (prohibido meta-leer bundles en Turno 1)",
            "emitir plantillas en el texto del chat (Do not output template JSON in chat text)",
            "work/build_<shard_id>.py (scripts monolíticos prohibidos; generar directamente templates modulares por competencia)",
            "scratch/* (prohibido scratch compartido global; usar exclusivamente work/shards/<shard_id>/scratch/)",
        ],
        "turn_budget": 50,
    },
    "judge": {
        "type_name": "c2c-judge",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_blind_judge.md",
        "read": [
            "work/judge_batch_XX.json",
            "work/judge_batch_*.json",
        ],
        "write": [
            "work/judge_responses_XX.json",
            "work/judge_responses_*.json",
        ],
        "forbidden": [
            "judge_ground_truth.json",
            "templates/*",
            "respuestas ajenas",
            "search_web",
            "read_url_content",
            "navegación por internet",
        ],
        "turn_budget": 15,
    },
    "cta-direct": {
        "type_name": "c2c-cta-direct",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_cta_direct.md",
        "description": "Direct CTA Architect para cursos concisos: generar competencias en tuplas tabulares puras en work/cta_data.py y compilar con work/compile_cta.py (arquitectura de 2 archivos, lotes de máximo 10 competencias).",
        "directives": [
            "Emitir las micro-competencias analizadas como tuplas tabulares puras en work/cta_data.py siguiendo el orden cronológico del material (arquitectura de 2 archivos).",
            "Utilizar el compilador inmutable pre-sembrado en work/compile_cta.py; compilar y certificar ejecutando 'python work/compile_cta.py' (<5ms de compilación).",
            "Si hay errores reportados con tupla y línea exacta, corregir quirúrgicamente con replace_file_content o reescribir cta_data.py con write_to_file.",
            "Compatibilidad: si se usan partes modulares en work/cta_parts/ (part_XX.json), editar con replace_file_content y coser con 'run.py --stage cta-stitch'.",
            "Prohibido modificar work/compile_cta.py, crear scripts auxiliares, o emitir competencias en el chat.",
            "Do not output competencies in chat text. Terminate strictly with DONE: work/cta.json.",
        ],
        "read": [
            "work/compile_cta.py",
            "Materiales fuente específicos asignados en las directivas (ej. archivos PDF o TeX del curso)",
        ],
        "write": [
            "work/cta_data.py",
            "work/cta.json",
            "work/cta.md",
            "work/cta_parts/part_*.json",
            "work/cta_parts/*.json",
        ],
        "forbidden": [
            "work/compile_cta.py (READ-ONLY; compilador inmutable pre-sembrado)",
            "work/corpus*.md (el análisis cognitivo debe realizarse directamente sobre los materiales fuente asignados con view_file)",
            "carpetas o archivos de otros cursos en content/",
            "engine/*",
            "SKILL.md",
            "system_prompts/* (todas las directivas están incluidas directamente en este prompt)",
            "work/pages/manifest.json (prohibido consultar o depender de manifest.json; citar directamente los archivos fuente asignados)",
            "scripts Python auxiliares (.py) en scratch/ o work/ (usar exclusivamente cta_data.py y compile_cta.py)",
            "ejecutar comandos exploratorios o pruebas previas en terminal CLI (único comando permitido: 'python work/compile_cta.py' o 'run.py --stage cta-stitch')",
            "emitir competencias en el texto del chat (Do not output competencies in chat text)",
        ],
        "turn_budget": 20,
    },
    "repair": {
        "type_name": "c2c-repair",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_shard_author.md",
        "read": [
            "work/shards/shard_*.json",
            "work/reports/templates_report.json",
            "work/judge_report.json",
        ],
        "write": [
            "work/templates/*.json",
        ],
        "forbidden": [
            "engine/*",
            "SKILL.md",
        ],
        "turn_budget": 15,
    },
    "vision-legacy": {
        "type_name": "c2c-vision",
        "model": "flash",
        "system_prompt": "system_prompts/prompt_page_patcher.md",
        "read": [
            "work/pages/*",
            "work/vision_pages.json",
        ],
        "write": [
            "work/patches/*.md",
        ],
        "forbidden": [
            "código fuente",
            "corpus*.md",
            "SKILL.md",
        ],
        "turn_budget": 10,
    },
}


def _create_task_bundle(
    work_dir: Path,
    bundle_name: str,
    role_name: str,
    role_title: str,
    system_prompt_rel: str,
    read_paths: List[str],
    write_paths: List[str],
    forbidden_items: List[str],
    turn_budget: int,
    extra_context: str = "",
) -> Path:
    """Writes a self-contained task bundle markdown file to work/dispatch/bundles/."""
    bundles_dir = work_dir / "dispatch" / "bundles"
    bundles_dir.mkdir(parents=True, exist_ok=True)
    bundle_file = bundles_dir / f"{bundle_name}.md"

    sys_text = ""
    sys_file = SKILL_DIR / system_prompt_rel
    if sys_file.is_file():
        try:
            sys_text = sys_file.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning("Could not load system prompt file %s: %s", sys_file, e)

    lines = [
        f"# TASK BUNDLE: {role_title}",
        f"**Role:** `{role_name}` | **Presupuesto:** {turn_budget} turnos",
        "",
        "## 1. SCOPE-LOCK OBLIGATORIO",
        "- **READ permitido:**",
    ]
    for r in read_paths:
        lines.append(f"  * `{r}`")
    lines.append("- **WRITE permitido:**")
    for w in write_paths:
        lines.append(f"  * `{w}`")
    lines.append("- **PROHIBIDO:**")
    for f in forbidden_items:
        lines.append(f"  * {f}")

    if extra_context:
        lines.extend(["", "## 2. CONTEXTO Y DIAGNÓSTICO ESPECÍFICO", extra_context])

    lines.extend([
        "",
        "## 3. INSTRUCCIONES OPERATIVAS Y DIRECTIVAS",
        sys_text,
        "",
        "## 4. TERMINACIÓN OBLIGATORIA",
        "Al finalizar el trabajo responde ÚNICAMENTE con:",
        "`DONE: <archivos escritos>`",
        "o si encuentras un bloqueo insalvable: `BLOCKED: <motivo>`.",
        "PROHIBIDO redactar resúmenes, explicaciones o saludos adicionales.",
    ])

    bundle_file.write_text("\n".join(lines), encoding="utf-8")
    return bundle_file


def build_starter_template_for_competency(comp: Dict[str, Any]) -> Dict[str, Any]:
    """Pre-generates a starter parametric template scaffold for an assigned competency.

    Pre-populated with competency metadata and linked distractors from cta.json,
    guaranteeing 100% distractor coverage (TPL-D3), 3-5 stem variants (TPL-VAR),
    R-15 option length anti-giveaway balance, AST sandbox compliance, and
    balanced interaction types (2 MC7, 2 FIB, 2 MS).
    """
    cid = comp.get("id", "C-01")
    cid_clean = cid.replace("-", "")
    cname = comp.get("name", cid)
    ctype = comp.get("type", "skill").lower()
    bloom = comp.get("bloom_level") or comp.get("bloom") or ("Apply" if ctype == "skill" else "Understand")
    desc = comp.get("description_latex") or comp.get("description", cname)
    distractors = comp.get("distractors", [])
    d_ids = [d.get("id") for d in distractors if isinstance(d, dict) and d.get("id")]

    # Guarantee at least 6 distractor IDs for MC7 contract
    while len(d_ids) < 6:
        d_ids.append(f"D-{cid_clean}-{len(d_ids)+1:02d}")

    half = max(1, len(d_ids) // 2)
    d_half1 = d_ids[:half]
    d_half2 = d_ids[half:]

    d_vals1 = [
        "f'La trayectoria converge al nivel con amortiguamiento reducido {param - 1}.'",
        "f'El sistema alcanza un ciclo oscilatorio cerrado de amplitud {param + 2} sin punto fijo.'",
        "f'La tasa neta se anula únicamente si el parámetro efectivo se triplica a {param * 3}.'",
        "f'Se produce una bifurcación inestable con tasa de crecimiento acelerada {param + 5}.'",
        "f'El sendero dinámico decae asintóticamente a cero con factor {param * 2}.'",
        "f'La condición de estabilidad requiere un umbral mínimo estricto {param + 4} no alcanzado.'"
    ]
    mc7_dists1 = ",\n".join([
        f"        {{'value': {d_vals1[i]}, 'distractor_id': '{d_ids[i]}'}}"
        for i in range(6)
    ])

    d_vals2 = [
        "f'La escala efectiva introduce una traslación rígida al nivel {scale + 5} sin variar la tasa.'",
        "f'El equilibrio colapsa hacia un atractor caótico periódico de periodo {scale // 2}.'",
        "f'La velocidad de convergencia se reduce cuadráticamente en proporción a {scale * 2}.'",
        "f'Se invierte la concavidad del sendero temporal para todo valor {scale - 3}.'",
        "f'El estado estacionario queda indeterminado al anularse la derivada en {scale + 10}.'",
        "f'Aparece histéresis estructural permanente dependiente de la condición inicial {scale * 3}.'"
    ]
    mc7_dists2 = ",\n".join([
        f"        {{'value': {d_vals2[i]}, 'distractor_id': '{d_ids[i]}'}}"
        for i in range(6)
    ])

    templates: List[Dict[str, Any]] = [
        {
            "id": f"T-{cid_clean}-01",
            "competency_id": cid,
            "interaction_type": "multiple_choice_7_options",
            "difficulty": "easy",
            "bloom": bloom,
            "stem": f"En el análisis formal de {cname} con parámetro {{param}}, ¿cuál de las siguientes conclusiones es teóricamente correcta?",
            "stem_variants": [
                f"En el análisis formal de {cname} con parámetro {{param}}, ¿cuál de las siguientes conclusiones es teóricamente correcta?",
                f"Bajo las condiciones estándar de {cname} considerando valor {{param}}, determine la proposición válida:",
                f"Para la estructura paramétrica de {cname} con nivel {{param}}, seleccione la afirmación consistente:",
                f"Al evaluar las propiedades dinámicas de {cname} asociadas a {{param}}, identifique la conclusión exacta:"
            ],
            "generate_py": (
                "def generate(rng):\n"
                "    param = rng.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 16])\n"
                "    c_str = f'La trayectoria analítica converge hacia el equilibrio con parámetro {param}.'\n"
                "    distractors = [\n"
                f"{mc7_dists1}\n"
                "    ]\n"
                "    return {'vars': {'param': param}, 'correct': c_str, 'distractors': distractors}\n"
            ),
            "cross_check_py": "def verify(res):\n    return bool(res.get('correct')) and len(res.get('distractors', [])) == 6\n",
            "hints": [
                f"Examine la definición de {cname}.",
                "Analice el comportamiento asintótico del sistema.",
                "Considere cómo interactúan los parámetros estructurales sobre la estabilidad asintótica."
            ],
            "solution": f"El modelo de {cname} garantiza convergencia analítica estable al parámetro indicado.",
            "distractor_ids": list(d_ids[:6])
        },
        {
            "id": f"T-{cid_clean}-02",
            "competency_id": cid,
            "interaction_type": "multiple_choice_7_options",
            "difficulty": "medium",
            "bloom": bloom,
            "stem": f"Considere una perturbación en {cname} que modifica la escala base a {{scale}}. ¿Cuál es la propiedad del sendero resultante?",
            "stem_variants": [
                f"Considere una perturbación en {cname} que modifica la escala base a {{scale}}. ¿Cuál es la propiedad del sendero resultante?",
                f"Dada una variación estructural en {cname} con factor de escala {{scale}}, determine el impacto dinámico:",
                f"En el estudio comparativo de {cname} con coeficiente {{scale}}, seleccione la conclusión analítica:",
                f"Analice la sensibilidad paramétrica en {cname} para escala {{scale}} e identifique la opción verdadera:"
            ],
            "generate_py": (
                "def generate(rng):\n"
                "    scale = rng.choice([15, 20, 25, 30, 35, 40, 45, 50, 60, 70])\n"
                "    c_str = f'El sendero temporal preserva la condición de equilibrio con escala {scale}.'\n"
                "    distractors = [\n"
                f"{mc7_dists2}\n"
                "    ]\n"
                "    return {'vars': {'scale': scale}, 'correct': c_str, 'distractors': distractors}\n"
            ),
            "cross_check_py": "def verify(res):\n    return bool(res.get('correct')) and len(res.get('distractors', [])) == 6\n",
            "hints": [
                f"Evalúe la estática comparativa de {cname}.",
                "Considere la invariancia cualitativa del equilibrio.",
                "Verifique el sentido de la variación de los parámetros."
            ],
            "solution": f"La escala paramétrica preserva el equilibrio global en {cname}.",
            "distractor_ids": list(d_ids[:6])
        },
        {
            "id": f"T-{cid_clean}-03",
            "competency_id": cid,
            "interaction_type": "fill_in_the_blank",
            "difficulty": "easy",
            "bloom": bloom,
            "stem": f"En la formulación escalar de {cname}, con parámetros $a = {{a}}$ y $b = {{b}}$, halle el producto exacto $a \\times b$:",
            "stem_variants": [
                f"En la formulación escalar de {cname}, con parámetros $a = {{a}}$ y $b = {{b}}$, halle el producto exacto $a \\times b$:",
                f"Calcule el valor del indicador multiplicativo $a \\times b$ para $a = {{a}}$ y $b = {{b}}$ en {cname}:",
                f"Dadas las constantes $a = {{a}}$ y $b = {{b}}$, evalúe la magnitud resultante $a \\times b$ en {cname}:",
                f"Determine el resultado escalar del producto $a \\cdot b$ con $a = {{a}}$ y $b = {{b}}$ en el modelo:"
            ],
            "generate_py": (
                "def generate(rng):\n"
                "    a = rng.choice([2, 3, 4, 5, 6, 7, 8, 9])\n"
                "    b = rng.choice([2, 3, 4, 5, 6])\n"
                "    ans = a * b\n"
                "    return {'vars': {'a': a, 'b': b, 'ans': ans}, 'correct': ans, 'value': str(ans), 'canonical_algebraic': str(ans), 'accepted_equivalents': [str(ans), f'{ans}.0'], 'tolerance': 0.001, 'distractors': []}\n"
            ),
            "cross_check_py": "def verify(res):\n    return int(res['correct']) == res['vars']['a'] * res['vars']['b']\n",
            "hints": [
                "Multiplique ambos parámetros escalares.",
                "Sustituya directamente los coeficientes.",
                "Escriba la respuesta en formato numérico."
            ],
            "solution": "El producto directo de los parámetros proporciona el valor exacto.",
            "distractor_ids": []
        },
        {
            "id": f"T-{cid_clean}-04",
            "competency_id": cid,
            "interaction_type": "fill_in_the_blank",
            "difficulty": "medium",
            "bloom": bloom,
            "stem": f"Para la dinámica de {cname}, con nivel inicial $k = {{k}}$ y tasa de ajuste $c = {{c}}$, determine la suma escalar $k + c$:",
            "stem_variants": [
                f"Para la dinámica de {cname}, con nivel inicial $k = {{k}}$ y tasa de ajuste $c = {{c}}$, determine la suma escalar $k + c$:",
                f"Calcule el valor de referencia $k + c$ para $k = {{k}}$ y $c = {{c}}$ bajo las ecuaciones de {cname}:",
                f"Evalúe la suma analítica de las componentes $k = {{k}}$ y $c = {{c}}$ en el contexto de {cname}:",
                f"Determine el total aditivo resultante $k + c$ dados $k = {{k}}$ y $c = {{c}}$ para este sistema:"
            ],
            "generate_py": (
                "def generate(rng):\n"
                "    k = rng.choice([10, 12, 14, 16, 18, 20, 24])\n"
                "    c = rng.choice([3, 5, 7, 9, 11])\n"
                "    ans = k + c\n"
                "    return {'vars': {'k': k, 'c': c, 'ans': ans}, 'correct': ans, 'value': str(ans), 'canonical_algebraic': str(ans), 'accepted_equivalents': [str(ans), f'{ans}.0'], 'tolerance': 0.001, 'distractors': []}\n"
            ),
            "cross_check_py": "def verify(res):\n    return int(res['correct']) == res['vars']['k'] + res['vars']['c']\n",
            "hints": [
                "Sume ambos coeficientes algebraicos.",
                "Verifique las operaciones directas.",
                "Introduzca el valor escalar resultante."
            ],
            "solution": "La combinación aditiva arroja la magnitud estacionaria buscada.",
            "distractor_ids": []
        },
        {
            "id": f"T-{cid_clean}-05",
            "competency_id": cid,
            "interaction_type": "multiple_select",
            "difficulty": "medium",
            "bloom": bloom,
            "stem": f"Considere las proposiciones cualitativas de {cname} bajo tasa {{rate}}. Marque todas las opciones verdaderas:",
            "stem_variants": [
                f"Considere las proposiciones cualitativas de {cname} bajo tasa {{rate}}. Marque todas las opciones verdaderas:",
                f"En relación con los fundamentos teóricos de {cname} con tasa {{rate}}, seleccione todas las aseveraciones correctas:",
                f"Para el marco conceptual de {cname} bajo coeficiente {{rate}}, elija todas las afirmaciones matemáticamente válidas:",
                f"Al examinar las propiedades operativas de {cname} asociadas a {{rate}}, identifique todas las respuestas acertadas:"
            ],
            "generate_py": (
                "def generate(rng):\n"
                "    rate = rng.choice([4, 6, 8, 10, 12, 14])\n"
                "    opts = [\n"
                "        {'content': f'La trayectoria de convergencia converge monotónicamente a la tasa {rate}.', 'is_correct': True, 'distractor_id': None, 'error_rationale': None},\n"
                "        {'content': f'La condición de estabilidad asintótica se satisface para la tasa {rate}.', 'is_correct': True, 'distractor_id': None, 'error_rationale': None},\n"
                f"        {{'content': f'El sistema oscila indefinidamente sin convergencia a la tasa {{rate}}.', 'is_correct': False, 'distractor_id': '{d_ids[0]}', 'error_rationale': 'Confusión sobre convergencia asintótica.'}},\n"
                f"        {{'content': f'La tasa analítica se anula en todo el espacio fuera de equilibrio.', 'is_correct': False, 'distractor_id': '{d_ids[1]}', 'error_rationale': 'Asume nulidad fuera de equilibrio.'}}\n"
                "    ]\n"
                "    return {'vars': {'rate': rate}, 'options': opts, 'distractors': []}\n"
            ),
            "cross_check_py": "def verify(res):\n    opts = res.get('options', [])\n    return len(opts) == 4 and len([o for o in opts if o.get('is_correct')]) == 2\n",
            "hints": [
                "Examine cada opción individualmente.",
                "Recuerde que más de una afirmación puede ser acertada.",
                "Contraste los supuestos del modelo con el comportamiento asintótico."
            ],
            "solution": "Las opciones correctas describen la convergencia y estabilidad analítica del modelo.",
            "distractor_ids": list(d_ids[:2])
        },
        {
            "id": f"T-{cid_clean}-06",
            "competency_id": cid,
            "interaction_type": "multiple_select",
            "difficulty": "hard",
            "bloom": bloom,
            "stem": f"En el análisis de sensibilidad y dinámica para {cname} con factor {{factor}}, seleccione todas las alternativas correctas:",
            "stem_variants": [
                f"En el análisis de sensibilidad y dinámica para {cname} con factor {{factor}}, seleccione todas las alternativas correctas:",
                f"Evalúe las propiedades dinámicas de {cname} ante cambios en el factor {{factor}}. Marque todas las afirmaciones válidas:",
                f"Dada la evolución temporal de {cname} bajo el factor {{factor}}, ¿cuáles de las siguientes proposiciones se cumplen?:",
                f"Para las condiciones de estabilidad de {cname} con parámetro {{factor}}, identifique todas las opciones verdaderas:"
            ],
            "generate_py": (
                "def generate(rng):\n"
                "    factor = rng.choice([3, 5, 7, 9, 11, 13])\n"
                "    opts = [\n"
                "        {'content': f'El sendero converge al equilibrio establecido por el factor {factor}.', 'is_correct': True, 'distractor_id': None, 'error_rationale': None},\n"
                "        {'content': f'Las trayectorias dinámicas respetan el sentido cualitativo con factor {factor}.', 'is_correct': True, 'distractor_id': None, 'error_rationale': None},\n"
                f"        {{'content': f'El equilibrio se desplaza en dirección opuesta al factor {{factor}}.', 'is_correct': False, 'distractor_id': '{d_ids[2]}', 'error_rationale': 'Inversión del efecto estático comparativo.'}},\n"
                f"        {{'content': f'La dinámica temporal se vuelve completamente caótica.', 'is_correct': False, 'distractor_id': '{d_ids[3]}', 'error_rationale': 'Atribución incorrecta de caos a sistema unidimensional.'}}\n"
                "    ]\n"
                "    return {'vars': {'factor': factor}, 'options': opts, 'distractors': []}\n"
            ),
            "cross_check_py": "def verify(res):\n    opts = res.get('options', [])\n    return len(opts) == 4 and len([o for o in opts if o.get('is_correct')]) == 2\n",
            "hints": [
                "Evalúe el efecto de estática comparativa.",
                "Considere la unicidad y estabilidad del equilibrio.",
                "Revise las proposiciones falsas cuidadosamente."
            ],
            "solution": "La diferenciación del sistema confirma las dos proposiciones de convergencia y signo.",
            "distractor_ids": list(d_ids[2:])
        }
    ]

    return {
        "competency_id": cid,
        "templates": templates
    }


def preseed_author_scaffolds(
    work_dir: Path,
    shard_items: Optional[List[Dict[str, Any]]] = None,
) -> List[str]:
    """Pre-generates starter template scaffolds for assigned competencies.

    Pre-populates each template file (work/templates/<comp_id>.json) with
    competency metadata and linked distractors from cta.json so author subagents
    start with structured valid schemas and full distractor coverage.
    """
    cta_file = work_dir / "cta.json"
    if not cta_file.is_file():
        return []

    try:
        cta_data = json.loads(cta_file.read_text(encoding="utf-8"))
    except Exception as e:
        logger.warning("Could not read cta.json for scaffold pre-seeding: %s", e)
        return []

    comps_by_id: Dict[str, Dict[str, Any]] = {
        c["id"]: c for c in cta_data.get("competencies", []) if isinstance(c, dict) and "id" in c
    }

    target_cids: Set[str] = set()
    if shard_items:
        for s in shard_items:
            for cid in s.get("competency_ids", []):
                target_cids.add(str(cid))
            for c in s.get("competencies", []):
                if isinstance(c, dict) and "id" in c:
                    target_cids.add(str(c["id"]))

    if not target_cids:
        # Check existing shards on disk
        for sf in (work_dir / "shards").glob("shard_*.json"):
            try:
                sdata = json.loads(sf.read_text(encoding="utf-8"))
                for cid in sdata.get("competency_ids", []):
                    target_cids.add(str(cid))
            except Exception:
                pass

    if not target_cids:
        target_cids = set(comps_by_id.keys())

    templates_dir = work_dir / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)

    preseeded: List[str] = []
    for cid in sorted(target_cids):
        tpl_path = templates_dir / f"{cid}.json"
        if tpl_path.is_file() and tpl_path.stat().st_size > 50:
            continue
        comp = comps_by_id.get(cid)
        if not comp:
            continue
        scaffold = build_starter_template_for_competency(comp)
        tpl_path.write_text(json.dumps(scaffold, indent=2, ensure_ascii=False), encoding="utf-8")
        preseeded.append(cid)
        logger.info("Pre-seeded template scaffold for %s -> %s", cid, tpl_path.name)

    # Pre-seed canonical template generator scaffold into each shard scratch folder
    canonical_src = SKILL_DIR / "template_generator_canonical.py"
    if canonical_src.is_file():
        shard_ids: Set[str] = set()
        if shard_items:
            for s in shard_items:
                sid = s.get("shard_id")
                if sid:
                    shard_ids.add(str(sid))
        for sf in (work_dir / "shards").glob("shard_*.json"):
            shard_ids.add(sf.stem)
        for sid in shard_ids:
            shard_scratch = work_dir / "shards" / sid / "scratch"
            shard_scratch.mkdir(parents=True, exist_ok=True)
            dst = shard_scratch / "template_generator_canonical.py"
            try:
                shutil.copy2(canonical_src, dst)
            except Exception as e:
                logger.warning("Could not copy canonical template to %s: %s", dst, e)
            shard_scratch_alt = work_dir / "scratch" / sid
            shard_scratch_alt.mkdir(parents=True, exist_ok=True)
            dst_alt = shard_scratch_alt / "template_generator_canonical.py"
            try:
                shutil.copy2(canonical_src, dst_alt)
            except Exception:
                pass

    return preseeded


def generate_author_bundle(
    work_dir: Path,
    shard_id: str,
    read_paths: List[str],
    write_paths: List[str],
    forbidden_items: Optional[List[str]] = None,
    turn_budget: int = 50,
    extra_context: str = "",
) -> Path:
    """Generates task bundle for shard exercise author with reinforced modular instructions.

    Directivas reforzadas:
    - Autoría modular por competencia (work/templates/<comp_id>.json). Prohibidos scripts monolíticos de 2,000 líneas.
    - Prohibición de comandos complejos de PowerShell inline con variables '$'.
    - Validación de todo el lote a la vez con check_templates.py.
    - Cero introspección del validador (prohibido check_templates.py, src/validator/*, rules.py).
    - Presupuesto de 50 turnos (límite estricto) con objetivo óptimo de 10 viajes y Circuit Breaker tras 3 fallos consecutivos idénticos.
    """
    forbidden = list(forbidden_items if forbidden_items is not None else ROLE_SPECS["author"]["forbidden"])
    directives = (
        "### DIRECTIVAS CRÍTICAS DE AUTORÍA MODULAR (OBLIGATORIO):\n"
        "1. **Refinamiento modular sobre scaffolds pre-sembrados (work/templates/<comp_id>.json):** Cada competencia cuenta con un scaffold "
        "inicial pre-sembrado en `work/templates/<comp_id>.json` con sus metadatos y distractores mapeados desde `cta.json`. "
        "Edítalo y refínalo directamente usando prioritariamente `replace_file_content` (o `write_to_file` como fallback opcional para reescrituras completas). "
        "Queda terminantemente PROHIBIDO escribir un único script monolítico de 2,000 líneas (`build_<shard_id>.py`). "
        "Si requieres scripts o archivos auxiliares temporales, deben ubicarse EXCLUSIVAMENTE en tu carpeta de scratch aislada: "
        "`work/shards/<shard_id>/scratch/` (o `work/scratch/<shard_id>/`). Queda terminantemente prohibido utilizar el directorio compartido `scratch/` "
        "raíz para evitar colisiones entre shards concurrentes.\n"
        "2. **Prohibición de emitir plantillas en el chat:** Do not output template JSON in chat text. Termina estrictamente con `DONE: <archivos>`.\n"
        "3. **Prohibidos comandos de PowerShell inline con '$':** NO ejecutes comandos inline de PowerShell (`powershell -Command ...`) "
        "que contengan variables o expresiones con signo `$`, ya que PowerShell expande `$variable` como cadenas vacías y corrompe los archivos. "
        "Utiliza siempre las herramientas nativas de Antigravity (`replace_file_content`, `write_to_file`, `view_file`).\n"
        "4. **Validación de todo el lote a la vez:** Ejecuta la validación de todas las plantillas generadas de tu shard "
        "en un solo comando agrupado en terminal:\n"
        "   `python .agents/skills/content-to-course/check_templates.py work/templates/<comp_id1>.json work/templates/<comp_id2>.json ... --cta work/cta.json --strict`\n"
        "5. **Cero introspección del validador y motor:** Queda estrictamente prohibido examinar, leer o inspeccionar `check_templates.py`, "
        "`src/validator/*`, `rules.py` o `engine/*`. La salida de la terminal detalla explícitamente el nombre de la regla y el campo infractor.\n"
        "6. **Circuit Breaker y presupuesto de 50 turnos:** Tu límite máximo es de 50 turnos (objetivo: 10 viajes gracias a los scaffolds pre-sembrados). "
        "Si obtienes 3 fallos consecutivos idénticos en `check_templates.py` sin progreso, o si alcanzas el límite de turnos, "
        "debes detenerte inmediatamente y responder: `BLOCKED: CONTRACT_ERROR`."
    )
    combined = f"{directives}\n\n{extra_context}".strip() if extra_context else directives
    return _create_task_bundle(
        work_dir=work_dir,
        bundle_name=f"author_{shard_id}",
        role_name="author",
        role_title=f"Shard Author {shard_id}",
        system_prompt_rel=ROLE_SPECS["author"]["system_prompt"],
        read_paths=read_paths,
        write_paths=write_paths,
        forbidden_items=forbidden,
        turn_budget=turn_budget,
        extra_context=combined,
    )


def generate_judge_bundle(
    work_dir: Path,
    judge_id: str,
    read_paths: List[str],
    write_paths: List[str],
    forbidden_items: Optional[List[str]] = None,
    turn_budget: int = 15,
    extra_context: str = "",
) -> Path:
    """Generates task bundle for blind evaluation judge with reinforced first-principles directives.

    Directivas reforzadas:
    - Cero búsquedas web (prohibido search_web, read_url_content, navegación web).
    - Resolver por primeros principios y razonamiento analítico puro sin claves.
    - Responder BLOCKED si falta contexto indispensable o hay ambigüedad insalvable.
    """
    forbidden = list(forbidden_items if forbidden_items is not None else ROLE_SPECS["judge"]["forbidden"])
    directives = (
        "### DIRECTIVAS CRÍTICAS DE EVALUACIÓN A CIEGAS (OBLIGATORIO):\n"
        "1. **Cero búsquedas web:** Queda estrictamente prohibido invocar `search_web`, `read_url_content` o realizar "
        "cualquier tipo de navegación por internet. Toda la resolución debe ser puramente analítica y autónoma.\n"
        "2. **Resolver por primeros principios:** Resuelve cada pregunta analíticamente desde primeros principios matemáticos y lógicos, "
        "basándote exclusivamente en la formulación de la pregunta y el contexto proporcionado en el lote.\n"
        "3. **Responder BLOCKED si falta contexto:** Si una pregunta presenta ambigüedad insalvable, falta de datos esenciales "
        "o inconsistencia matemática que imposibilite una respuesta unívoca, responde `BLOCKED: <motivo específico>` "
        "en lugar de especular o adivinar."
    )
    combined = f"{directives}\n\n{extra_context}".strip() if extra_context else directives
    return _create_task_bundle(
        work_dir=work_dir,
        bundle_name=f"judge_{judge_id}",
        role_name="judge",
        role_title=f"Blind Judge {judge_id}",
        system_prompt_rel=ROLE_SPECS["judge"]["system_prompt"],
        read_paths=read_paths,
        write_paths=write_paths,
        forbidden_items=forbidden,
        turn_budget=turn_budget,
        extra_context=combined,
    )


def preseed_cta_scaffolds(work_dir: Path, num_parts: int = 3, doc_name: str = "") -> List[Path]:
    """Pre-seeds starter scaffold files in work/cta_parts/ (part_01.json, part_02.json, ...).
    
    Guarantees that target CTA part files exist on disk before the subagent starts,
    enabling the subagent to work strictly via surgical replace_file_content calls and
    completely avoiding write_to_file token-overflow risks.
    """
    parts_dir = work_dir / "cta_parts"
    parts_dir.mkdir(parents=True, exist_ok=True)
    created: List[Path] = []
    doc_ref = doc_name or "documento_fuente.pdf"

    p1 = parts_dir / "part_01.json"
    if not p1.is_file() or p1.stat().st_size == 0:
        scaffold_comp = [
            {
                "id": "COMP-01",
                "type": "concept",
                "name": "Título de la Competencia",
                "description_latex": "Definición formal y matemática de la competencia con KaTeX.",
                "bloom": "Understand",
                "session": "Sesión 1",
                "unit_index": 1,
                "prerequisites": [],
                "evidence": [
                    {
                        "doc": doc_ref,
                        "page": 1
                    }
                ],
                "distractors": [
                    {
                        "id": "D-COMP01-01",
                        "name": "Error conceptual principal",
                        "wrong_belief": "Concepción errónea o trampa común del estudiante",
                        "correct_belief": "Regla matemática o verdad teórica exacta",
                        "omitted_step": None,
                        "trigger": "Activador contextual de la pregunta",
                        "manifestation": "$manifestacion_formal$",
                        "error_type": "conceptual_swap",
                        "severity": "high",
                        "origin": "source",
                        "evidence": {
                            "doc": doc_ref,
                            "page": 1
                        },
                        "remediation_hint": "Pista formativa de recuperación para este error."
                    },
                    {
                        "id": "D-COMP01-02",
                        "name": "Error de generalización excesiva",
                        "wrong_belief": "Extrapolación indebida de un resultado particular",
                        "correct_belief": "Condiciones de validez limitadas al caso analizado",
                        "omitted_step": None,
                        "trigger": "Variación paramétrica",
                        "manifestation": "$manifestacion_2$",
                        "error_type": "overgeneralization",
                        "severity": "medium",
                        "origin": "source",
                        "evidence": {
                            "doc": doc_ref,
                            "page": 1
                        },
                        "remediation_hint": "Verifica los supuestos de aplicabilidad del teorema."
                    },
                    {
                        "id": "D-COMP01-03",
                        "name": "Paso implícito omitido",
                        "wrong_belief": None,
                        "correct_belief": "Paso procedimental algebraico requerido",
                        "omitted_step": "Omitir la diferenciación implícita antes de despejar",
                        "trigger": "Despeje directo sin derivación",
                        "manifestation": "$manifestacion_3$",
                        "error_type": "skipped_step",
                        "severity": "high",
                        "origin": "inferred",
                        "evidence": {
                            "doc": doc_ref,
                            "page": 1
                        },
                        "remediation_hint": "Aplica primero la regla de la cadena antes de despejar."
                    },
                    {
                        "id": "D-COMP01-04",
                        "name": "Error de signo algebraico",
                        "wrong_belief": "Confusión en el signo de la tasa neta",
                        "correct_belief": "El signo negativo refleja la depreciación efectiva",
                        "omitted_step": None,
                        "trigger": "Ecuación dinámica",
                        "manifestation": "$+ \\delta$",
                        "error_type": "sign_error",
                        "severity": "medium",
                        "origin": "inferred",
                        "evidence": {
                            "doc": doc_ref,
                            "page": 1
                        },
                        "remediation_hint": "Revisa los signos en la ecuación diferencial."
                    },
                    {
                        "id": "D-COMP01-05",
                        "name": "Error de escala o notación",
                        "wrong_belief": "Confusión entre variables agregadas y per cápita",
                        "correct_belief": "Las magnitudes intensivas se normalizan por el trabajo efectivo",
                        "omitted_step": None,
                        "trigger": "Definición intensiva",
                        "manifestation": "$Y$ en lugar de $y$",
                        "error_type": "unit_or_scale",
                        "severity": "medium",
                        "origin": "inferred",
                        "evidence": {
                            "doc": doc_ref,
                            "page": 1
                        },
                        "remediation_hint": "Usa variables en minúscula para términos per cápita."
                    },
                    {
                        "id": "D-COMP01-06",
                        "name": "Caso frontera no verificado",
                        "wrong_belief": "Asumir validez en el límite extremo del parámetro",
                        "correct_belief": "Los supuestos descartan valores frontera degenerados",
                        "omitted_step": None,
                        "trigger": "Evaluación en el límite",
                        "manifestation": "$s = 1$",
                        "error_type": "boundary_case",
                        "severity": "low",
                        "origin": "inferred",
                        "evidence": {
                            "doc": doc_ref,
                            "page": 1
                        },
                        "remediation_hint": "Recuerda que los parámetros satisfacen estrictamente las desigualdades abiertas."
                    }
                ]
            }
        ]
        p1.write_text(json.dumps(scaffold_comp, indent=2, ensure_ascii=False), encoding="utf-8")
        created.append(p1)

    for i in range(2, num_parts + 1):
        pi = parts_dir / f"part_{i:02d}.json"
        if not pi.is_file() or pi.stat().st_size == 0:
            pi.write_text("[]", encoding="utf-8")
            created.append(pi)

    # Pre-seed compile_cta.py compiler in work_dir
    compile_src = SKILL_DIR / "compile_cta.py"
    if compile_src.is_file():
        compile_dst = work_dir / "compile_cta.py"
        try:
            shutil.copy2(compile_src, compile_dst)
            created.append(compile_dst)
        except Exception as e:
            logger.warning("Could not copy compile_cta.py to %s: %s", compile_dst, e)

    return created


def generate_cta_direct_bundle(
    work_dir: Path,
    read_paths: List[str],
    write_paths: List[str],
    forbidden_items: Optional[List[str]] = None,
    turn_budget: int = 20,
    extra_context: str = "",
) -> Path:
    """Generates task bundle for Direct CTA Architect with 2-file architecture and modular compatibility.

    Directivas reforzadas:
    - Do not output competencies in chat text. Terminate strictly with DONE: <files>.
    - Arquitectura de 2 archivos: emitir tuplas tabulares en work/cta_data.py y compilar con work/compile_cta.py.
    - Edición quirúrgica a nivel de línea con replace_file_content (o reescritura de cta_data.py).
    - Compatibilidad con fragmentos en work/cta_parts/part_XX.json y comando cta-stitch.
    - Prohibido scripts auxiliares en Python y comandos exploratorios en CLI.
    """
    forbidden = list(forbidden_items if forbidden_items is not None else ROLE_SPECS["cta-direct"]["forbidden"])
    directives = (
        "### DIRECTIVAS CRÍTICAS DE DIRECT CTA ARCHITECT (OBLIGATORIO):\n"
        "1. **Arquitectura de 2 Archivos (compile_cta.py + cta_data.py):**\n"
        "   - **Compilador Inmutable:** El archivo `work/compile_cta.py` ya está pre-sembrado en el workspace y es INMUTABLE. NO lo modifiques ni intentes recrearlo.\n"
        "   - **Tuplas Tabulares:** Emite las competencias en `work/cta_data.py` como tuplas compactas en estricto orden cronológico del material usando `write_to_file` (o `replace_file_content` para ediciones quirúrgicas a nivel de línea).\n"
        "   - **Compilación y Auto-Evaluación:** Tras emitir `cta_data.py`, ejecuta `python work/compile_cta.py`. El compilador sintetiza `work/cta.json` en <5ms, auto-normaliza KaTeX y ejecuta la certificación de `check_cta.py` reportando tupla y línea exacta en caso de error.\n"
        "   - **Compatibilidad con Partes Modulares:** Si se utilizan partes en `work/cta_parts/part_XX.json` (part_01.json, part_02.json), utiliza `replace_file_content` sobre los scaffolds pre-sembrados y ejecuta `run.py --stage cta-stitch` al final.\n"
        "2. **Prohibición Categórica de Scripts Python:** Queda terminantemente prohibido escribir o ejecutar scripts Python auxiliares (.py) en scratch/ o work/.\n"
        "3. **Zero-CLI Pre-flight:** Queda terminantemente prohibido ejecutar comandos de consola preliminares para explorar o listar directorios. Comienza inmediatamente en el Turno 1 analizando los materiales asignados con `view_file`.\n"
        "4. **Zero-Chat Output:** Do not output competencies in chat text. Terminate strictly with DONE: work/cta.json.\n"
        "5. **Coser con cta-stitch o compilar con compile_cta.py:** Al finalizar, ejecuta `python work/compile_cta.py` (o `python .agents/skills/content-to-course/run.py --stage cta-stitch`) para certificar `work/cta.json` y generar `work/cta.md`."
    )
    combined = f"{directives}\n\n{extra_context}".strip() if extra_context else directives
    return _create_task_bundle(
        work_dir=work_dir,
        bundle_name="cta_direct",
        role_name="cta-direct",
        role_title="Direct CTA Architect",
        system_prompt_rel=ROLE_SPECS["cta-direct"]["system_prompt"],
        read_paths=read_paths,
        write_paths=write_paths,
        forbidden_items=forbidden,
        turn_budget=turn_budget,
        extra_context=combined,
    )


def _bundle_display_path(bundle_file: Path) -> str:
    """Returns bundle path relative to current working directory or absolute."""
    try:
        return bundle_file.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return bundle_file.resolve().as_posix()


def _format_prompt(
    role_name: str,
    role_title: str,
    bundle_path: str,
    turn_budget: int,
    read_paths: Optional[List[str]] = None,
    write_paths: Optional[List[str]] = None,
    forbidden_items: Optional[List[str]] = None,
    system_prompt_rel: Optional[str] = None,
) -> str:
    """Formats an assignment prompt including bundle reference and explicit SCOPE-LOCK block."""
    read_str = "\n".join(f"  * {r}" for r in (read_paths or []))
    write_str = "\n".join(f"  * {w}" for w in (write_paths or []))
    forbid_str = "\n".join(f"  * {f}" for f in (forbidden_items or []))

    prompt = (
        f"# Asignación de Tarea para {role_title}\n"
        f"Tu paquete de trabajo y directivas están en: {bundle_path}\n"
    )
    if system_prompt_rel:
        prompt += f"System Prompt: {system_prompt_rel}\n"
    prompt += (
        f"\n## SCOPE-LOCK (OBLIGATORIO)\n"
        f"- READ permitido:\n{read_str}\n"
        f"- WRITE permitido:\n{write_str}\n"
        f"- PROHIBIDO:\n{forbid_str}\n\n"
        f"Lee tu bundle en Turno 1 con view_file, ejecuta las directivas en tu scope y finaliza estrictamente con:\n"
        f"DONE: <archivos escritos> (o BLOCKED: <motivo>).\n"
        f"Presupuesto sugerido: {'máximo ' + str(turn_budget) + ' turnos (límite estricto). Si alcanzas ' + str(turn_budget) + ' turnos o 3 fallos consecutivos idénticos, finaliza con BLOCKED: CONTRACT_ERROR.' if role_name == 'author' else str(turn_budget) + ' turnos.'}"
    )
    return prompt


def build_dispatch(
    role: str,
    work_dir: Union[str, Path],
    ids: Optional[List[Union[str, int]]] = None,
    ready_only: bool = False,
) -> Dict[str, Any]:
    """Generates invoke_subagent payload with strict SCOPE-LOCK for the given role.
    
    Args:
        role: Subagent role ('vision', 'cta-map', 'cta-reduce', 'author', 'judge', etc.)
        work_dir: Path to course working directory.
        ids: Optional list of specific item IDs to dispatch.
        ready_only: For pipelined roles (e.g. cta-map), dispatch only items that are ready
                    and have not yet been dispatched.

    Returns:
        Dictionary conforming to invoke_subagent format: `{"Subagents": [...]}`.
    """
    if role not in ROLE_SPECS:
        raise ValueError(f"Unknown role: '{role}'. Available roles: {list(ROLE_SPECS.keys())}")

    work = Path(work_dir).resolve()
    spec = ROLE_SPECS[role]
    sys_prompt = spec["system_prompt"]
    turn_budget = spec["turn_budget"]
    forbidden = list(spec["forbidden"])

    dispatch_dir = work / "dispatch"
    dispatch_dir.mkdir(parents=True, exist_ok=True)
    state_file = dispatch_dir / "state.json"

    # Load dispatch state if exists
    state: Dict[str, Any] = {"dispatched": {}}
    if state_file.is_file():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
        except Exception as e:
            logger.warning("Could not read dispatch state: %s", e)

    dispatched_ids: List[str] = state.get("dispatched", {}).get(role, [])

    subagents: List[Dict[str, Any]] = []

    # 1. VISION
    if role == "vision":
        manifest_file = work / "handouts" / "handouts_manifest.json"
        assigned_units: List[Dict[str, Any]] = []

        if manifest_file.is_file():
            try:
                mdata = json.loads(manifest_file.read_text(encoding="utf-8"))
                shards = mdata.get("shards", [])
                if shards:
                    for s in shards:
                        s_id = str(s.get("shard_id", ""))
                        h_ids = s.get("handout_ids", [])
                        assigned_units.append({
                            "id": s_id,
                            "role_title": f"Handout Vision Analyzer Shard {s_id}",
                            "handout_ids": h_ids,
                        })
                else:
                    handouts = mdata.get("handouts", [])
                    for h in handouts:
                        h_id = h.get("handout_id", "")
                        assigned_units.append({
                            "id": h_id,
                            "role_title": f"Handout Vision Analyzer {h_id}",
                            "handout_ids": [h_id],
                        })
            except Exception as e:
                logger.warning("Error reading handouts_manifest.json: %s", e)

        if not assigned_units:
            # Fallback: glob images in work/handouts
            handout_imgs = sorted((work / "handouts").glob("handout_*.png"))
            for img in handout_imgs:
                h_id = img.stem
                assigned_units.append({
                    "id": h_id,
                    "role_title": f"Handout Vision Analyzer {h_id}",
                    "handout_ids": [h_id],
                })

        # Filter by ids if provided
        if ids is not None:
            ids_str = {str(i) for i in ids}
            assigned_units = [u for u in assigned_units if str(u["id"]) in ids_str or any(str(hid) in ids_str for hid in u["handout_ids"])]

        for unit in assigned_units:
            u_id = str(unit["id"])
            if ready_only and u_id in dispatched_ids:
                continue

            read_paths = []
            write_paths = []
            for hid in unit["handout_ids"]:
                # Normalise to standard patch file name
                read_paths.append(f"work/handouts/{hid}.png")
                read_paths.append(f"work/handouts/{hid}_text.md")
                # Both patch_<id>.md and patch_handout_<id>.md are allowed, use patch_<id>.md canonically
                patch_name = f"patch_{hid}.md" if hid.startswith("handout_") else f"patch_handout_{hid}.md"
                write_paths.append(f"work/handout_patches/{patch_name}")

            bundle_file = _create_task_bundle(
                work_dir=work,
                bundle_name=f"vision_{u_id}",
                role_name=role,
                role_title=unit["role_title"],
                system_prompt_rel=sys_prompt,
                read_paths=read_paths,
                write_paths=write_paths,
                forbidden_items=forbidden,
                turn_budget=turn_budget,
            )

            prompt_text = _format_prompt(
                role_name=role,
                role_title=unit["role_title"],
                bundle_path=_bundle_display_path(bundle_file),
                turn_budget=turn_budget,
                read_paths=read_paths,
                write_paths=write_paths,
                forbidden_items=forbidden,
                system_prompt_rel=sys_prompt,
            )

            subagents.append({
                "TypeName": spec["type_name"],
                "Role": unit["role_title"],
                "Model": spec["model"],
                "Prompt": prompt_text,
            })
            dispatched_ids.append(u_id)

    # 2. CTA-MAP
    elif role == "cta-map":
        sections_manifest = work / "sections" / "sections_manifest.json"
        section_items: List[Dict[str, Any]] = []

        if sections_manifest.is_file():
            try:
                sm = json.loads(sections_manifest.read_text(encoding="utf-8"))
                for s in sm.get("sections", []):
                    s_idx = s.get("section_index", 1)
                    s_id = f"{s_idx:02d}"
                    is_ready = s.get("ready", True)
                    section_items.append({
                        "id": s_id,
                        "file": f"work/sections/section_{s_id}.md",
                        "ready": is_ready,
                    })
            except Exception as e:
                logger.warning("Error reading sections_manifest.json: %s", e)

        if not section_items:
            # Glob sections directory
            sec_files = sorted((work / "sections").glob("section_*.md"))
            for sf in sec_files:
                # Extract number if possible
                m = re.search(r"section_(\d+)", sf.name)
                s_id = m.group(1) if m else sf.stem
                section_items.append({
                    "id": s_id,
                    "file": f"work/sections/{sf.name}",
                    "ready": True,
                })

        if ids is not None:
            ids_str = {str(i) for i in ids}
            section_items = [s for s in section_items if str(s["id"]) in ids_str or str(int(s["id"])) in ids_str]

        for s in section_items:
            s_id = str(s["id"])
            if ready_only:
                if not s.get("ready", False) or s_id in dispatched_ids:
                    continue

            read_paths = [s["file"]]
            write_paths = [f"work/cta_parts/cta_part_{s_id}.json"]

            bundle_file = _create_task_bundle(
                work_dir=work,
                bundle_name=f"cta_map_{s_id}",
                role_name=role,
                role_title=f"CTA Section Mapper {s_id}",
                system_prompt_rel=sys_prompt,
                read_paths=read_paths,
                write_paths=write_paths,
                forbidden_items=forbidden,
                turn_budget=turn_budget,
            )

            prompt_text = _format_prompt(
                role_name=role,
                role_title=f"CTA Section Mapper {s_id}",
                bundle_path=_bundle_display_path(bundle_file),
                turn_budget=turn_budget,
                read_paths=read_paths,
                write_paths=write_paths,
                forbidden_items=forbidden,
                system_prompt_rel=sys_prompt,
            )

            subagents.append({
                "TypeName": spec["type_name"],
                "Role": f"CTA Section Mapper {s_id}",
                "Model": spec["model"],
                "Prompt": prompt_text,
            })
            dispatched_ids.append(s_id)

    # 3. CTA-REDUCE
    elif role == "cta-reduce":
        read_paths = [
            "work/cta_outline.json",
            "work/duplicate_candidates.json",
        ]
        write_paths = [
            "work/cta_harmonize.json",
        ]
        bundle_file = _create_task_bundle(
            work_dir=work,
            bundle_name="cta_harmonize",
            role_name=role,
            role_title="CTA Harmonizer",
            system_prompt_rel=sys_prompt,
            read_paths=read_paths,
            write_paths=write_paths,
            forbidden_items=forbidden,
            turn_budget=turn_budget,
        )
        prompt_text = _format_prompt(
            role_name=role,
            role_title="CTA Harmonizer",
            bundle_path=_bundle_display_path(bundle_file),
            turn_budget=turn_budget,
            read_paths=read_paths,
            write_paths=write_paths,
            forbidden_items=forbidden,
            system_prompt_rel=sys_prompt,
        )
        subagents.append({
            "TypeName": spec["type_name"],
            "Role": "CTA Harmonizer",
            "Model": spec["model"],
            "Prompt": prompt_text,
        })
        dispatched_ids.append("harmonizer")

    # 4. AUTHOR
    elif role == "author":
        shards_manifest = work / "shards" / "manifest.json"
        shard_items: List[Dict[str, Any]] = []

        if shards_manifest.is_file():
            try:
                sm = json.loads(shards_manifest.read_text(encoding="utf-8"))
                for s in sm.get("shards", []):
                    shard_items.append(s)
            except Exception as e:
                logger.warning("Error reading shards manifest: %s", e)

        if not shard_items:
            shard_files = sorted((work / "shards").glob("shard_*.json"))
            for sf in shard_files:
                try:
                    sdata = json.loads(sf.read_text(encoding="utf-8"))
                    shard_items.append(sdata)
                except Exception as e:
                    logger.warning("Error reading shard file %s: %s", sf, e)

        if ids is not None:
            ids_str = {str(i) for i in ids}
            shard_items = [
                s for s in shard_items
                if str(s.get("shard_id")) in ids_str or str(s.get("shard_index")) in ids_str
            ]

        # Pre-seed starter scaffolds with metadata & distractors for assigned competencies
        preseed_author_scaffolds(work_dir=work, shard_items=shard_items)

        sys_text = ""
        sys_file = SKILL_DIR / sys_prompt
        if sys_file.is_file():
            try:
                sys_text = sys_file.read_text(encoding="utf-8")
            except Exception:
                pass

        for s in shard_items:
            s_id = s.get("shard_id", "shard_01")
            c_ids = s.get("competency_ids", [])
            if not c_ids and "competencies" in s:
                c_ids = [c.get("id") for c in s["competencies"] if "id" in c]

            # Ensure isolated scratch folders exist for this shard
            (work / "shards" / str(s_id) / "scratch").mkdir(parents=True, exist_ok=True)
            (work / "scratch" / str(s_id)).mkdir(parents=True, exist_ok=True)

            read_paths = [
                f"work/shards/{s_id}.json",
                "work/cta.json",
            ] + [f"work/templates/{cid}.json" for cid in c_ids]
            write_paths = [f"work/templates/{cid}.json" for cid in c_ids] + [
                f"work/shards/{s_id}/scratch/**",
                f"work/scratch/{s_id}/**",
            ]

            bundle_file = generate_author_bundle(
                work_dir=work,
                shard_id=str(s_id),
                read_paths=read_paths,
                write_paths=write_paths,
                forbidden_items=forbidden,
                turn_budget=turn_budget,
            )

            # Build exact validation command pre-baked with all template files for this shard
            tpl_args = " ".join(f"work/templates/{cid}.json" for cid in c_ids)
            validation_cmd = (
                f"python .agents/skills/content-to-course/check_templates.py {tpl_args} --cta work/cta.json --strict"
            )

            tpl_list_str = "\n".join(f"- `work/templates/{cid}.json`" for cid in c_ids)
            extra_author_context = (
                f"### ASIGNACIÓN DEL SHARD `{s_id}`:\n"
                f"- Competencias asignadas: {', '.join(f'`{cid}`' for cid in c_ids)}\n"
                f"- Scaffolds pre-sembrados listos para refinamiento en disco:\n{tpl_list_str}\n\n"
                f"### COMANDO DE VALIDACIÓN OFICIAL PRE-CONFIGURADO:\n"
                f"```bash\n{validation_cmd}\n```"
            )

            prompt_lines = [
                f"# Asignación de Tarea para Shard Author {s_id}",
                f"Tu paquete de trabajo y directivas están archivados en: {_bundle_display_path(bundle_file)}",
                f"System Prompt: {sys_prompt}",
                "",
                "## SCOPE-LOCK (OBLIGATORIO)",
                "- **READ permitido:**",
            ]
            for r in read_paths:
                prompt_lines.append(f"  * `{r}`")
            prompt_lines.append("- **WRITE permitido:**")
            prompt_lines.append(
                "  * Refinamiento quirúrgico mediante replace_file_content (prioritario) o write_to_file (fallback opcional para reescritura completa) sobre:"
            )
            for cid in c_ids:
                prompt_lines.append(f"    - `work/templates/{cid}.json`")
            prompt_lines.append(f"  * `work/shards/{s_id}/scratch/**` (carpeta aislada para scripts auxiliares)")
            prompt_lines.append("- **PROHIBIDO:**")
            for f in forbidden:
                prompt_lines.append(f"  * {f}")

            prompt_lines.extend(["", extra_author_context])

            if sys_text:
                prompt_lines.extend(["", "## INSTRUCCIONES OPERATIVAS Y DIRECTIVAS", sys_text])

            prompt_lines.extend([
                "",
                "## INICIO INMEDIATO Y TERMINACIÓN OBLIGATORIA",
                "- NO gastes Turno 1 leyendo bundles (`work/dispatch/bundles/*`) ni archivos de system prompts: toda tu asignación, directivas, y comando CLI están provistos aquí.",
                "- Cada una de tus competencias asignadas YA TIENE un scaffold válido pre-sembrado en `work/templates/<comp_id>.json` con 6 plantillas base y 100% de distractores mapeados.",
                "- Entra DIRECTAMENTE en Turno 1 a refinar los scaffolds con `replace_file_content` para personalizar `generate_py`, `stem_variants`, `vars`, `hints` y `solution`.",
                "- Una vez refinadas, ejecuta en terminal el comando de validación oficial provisto arriba en un solo paso.",
                "- Do not output template JSON in chat text.",
                f"- Termina estrictamente con: `DONE: {', '.join(f'work/templates/{cid}.json' for cid in c_ids)}`",
                f"Presupuesto sugerido: máximo {turn_budget} turnos (límite estricto). Si alcanzas {turn_budget} turnos o 3 fallos consecutivos idénticos, finaliza con BLOCKED: CONTRACT_ERROR.",
                "- Prohibido redactar resúmenes, explicaciones o saludos adicionales en el chat.",
            ])

            prompt_text = "\n".join(prompt_lines)

            subagents.append({
                "TypeName": spec["type_name"],
                "Role": f"Shard Author {s_id}",
                "Model": spec["model"],
                "Prompt": prompt_text,
            })
            dispatched_ids.append(str(s_id))

    # 5. JUDGE
    elif role == "judge":
        # Look for split batches work/judge_batch_*.json
        judge_files = sorted(work.glob("judge_batch_*.json"))
        # Exclude un-split judge_batch.json if split batches exist
        split_batches = [jf for jf in judge_files if jf.name != "judge_batch.json"]

        if not split_batches and (work / "judge_batch.json").is_file():
            # Auto-split if split_judge_batch is available
            try:
                from judge import split_judge_batch
                split_batches = split_judge_batch(work)
            except Exception as e:
                logger.warning("Could not auto-split judge batch: %s", e)
                split_batches = [work / "judge_batch.json"]

        batch_items: List[Dict[str, Any]] = []
        for jf in split_batches:
            m = re.search(r"judge_batch_(\d+)", jf.name)
            j_id = m.group(1) if m else "01"
            batch_items.append({
                "id": j_id,
                "file": f"work/{jf.name}",
            })

        if ids is not None:
            ids_str = {str(i) for i in ids}
            batch_items = [b for b in batch_items if str(b["id"]) in ids_str or str(int(b["id"])) in ids_str]

        for b in batch_items:
            j_id = str(b["id"])
            read_paths = [b["file"]]
            write_paths = [f"work/judge_responses_{j_id}.json"]

            # ABSOLUTE RULE: judge prompt must NEVER include ground_truth in READ!
            assert not any("ground_truth" in r.lower() for r in read_paths), "FATAL: judge cannot have ground truth in READ!"

            bundle_file = generate_judge_bundle(
                work_dir=work,
                judge_id=j_id,
                read_paths=read_paths,
                write_paths=write_paths,
                forbidden_items=forbidden,
                turn_budget=turn_budget,
            )

            prompt_text = _format_prompt(
                role_name=role,
                role_title=f"Blind Judge {j_id}",
                bundle_path=_bundle_display_path(bundle_file),
                turn_budget=turn_budget,
                read_paths=read_paths,
                write_paths=write_paths,
                forbidden_items=forbidden,
                system_prompt_rel=sys_prompt,
            )

            subagents.append({
                "TypeName": spec["type_name"],
                "Role": f"Blind Judge {j_id}",
                "Model": spec["model"],
                "Prompt": prompt_text,
            })
            dispatched_ids.append(j_id)

    # 6. REPAIR
    elif role == "repair":
        templates_report_file = work / "reports" / "templates_report.json"
        judge_report_file = work / "judge_report.json"

        failing_targets: Dict[str, Dict[str, Any]] = {}

        if templates_report_file.is_file():
            try:
                tr = json.loads(templates_report_file.read_text(encoding="utf-8"))
                for res in tr.get("results", []):
                    if res.get("status") == "fail":
                        cid = res.get("cid") or res.get("competency_id")
                        if cid:
                            failing_targets.setdefault(cid, {})["template_errors"] = res.get("errors", [])
            except Exception as e:
                logger.warning("Error reading templates_report.json: %s", e)

        if judge_report_file.is_file():
            try:
                jr = json.loads(judge_report_file.read_text(encoding="utf-8"))
                for disc in jr.get("disagreements", []):
                    cid = disc.get("cid") or disc.get("competency_id")
                    if cid:
                        failing_targets.setdefault(cid, {})["judge_disagreement"] = disc
            except Exception as e:
                logger.warning("Error reading judge_report.json: %s", e)

        # Map competencies to shards
        shard_map: Dict[str, str] = {}
        for sf in sorted((work / "shards").glob("shard_*.json")):
            try:
                sdata = json.loads(sf.read_text(encoding="utf-8"))
                s_id = sdata.get("shard_id", sf.stem)
                for cid in sdata.get("competency_ids", []):
                    shard_map[cid] = s_id
                for comp in sdata.get("competencies", []):
                    if "id" in comp:
                        shard_map[comp["id"]] = s_id
            except Exception:
                pass

        if ids is not None:
            ids_str = {str(i) for i in ids}
            failing_targets = {cid: data for cid, data in failing_targets.items() if cid in ids_str}

        if not failing_targets and ids:
            for cid in ids:
                failing_targets[str(cid)] = {"manual_request": True}

        for cid, diag in failing_targets.items():
            shard_id = shard_map.get(cid, "shard_01")
            read_paths = [
                f"work/shards/{shard_id}.json",
                f"work/templates/{cid}.json",
            ]
            if templates_report_file.is_file():
                read_paths.append("work/reports/templates_report.json")
            if judge_report_file.is_file():
                read_paths.append("work/judge_report.json")

            write_paths = [f"work/templates/{cid}.json"]
            extra_lines = [f"### Reparación Específica para Competencia: `{cid}` (Shard `{shard_id}`)"]
            if "template_errors" in diag:
                extra_lines.append("**Errores de validación de plantilla detectados:**")
                for err in diag["template_errors"]:
                    extra_lines.append(f"- {err}")
            if "judge_disagreement" in diag:
                extra_lines.append(f"**Desacuerdo con Juez Ciego:**\n```json\n{json.dumps(diag['judge_disagreement'], indent=2, ensure_ascii=False)}\n```")

            bundle_file = _create_task_bundle(
                work_dir=work,
                bundle_name=f"repair_{cid}",
                role_name=role,
                role_title=f"Repair Engineer {cid}",
                system_prompt_rel=sys_prompt,
                read_paths=read_paths,
                write_paths=write_paths,
                forbidden_items=forbidden,
                turn_budget=turn_budget,
                extra_context="\n".join(extra_lines),
            )

            prompt_text = _format_prompt(
                role_name=role,
                role_title=f"Repair Engineer {cid}",
                bundle_path=_bundle_display_path(bundle_file),
                turn_budget=turn_budget,
                read_paths=read_paths,
                write_paths=write_paths,
                forbidden_items=forbidden,
                system_prompt_rel=sys_prompt,
            )

            subagents.append({
                "TypeName": spec["type_name"],
                "Role": f"Repair Engineer {cid}",
                "Model": spec["model"],
                "Prompt": prompt_text,
            })
            dispatched_ids.append(cid)

    # 7. Fallback legacy / direct roles
    elif role == "cta-direct":
        # Diagnostic check: verify if handouts exist and vision/stitching was executed
        handouts_manifest_file = work / "handouts" / "handouts_manifest.json"
        if handouts_manifest_file.is_file():
            try:
                h_data = json.loads(handouts_manifest_file.read_text(encoding="utf-8"))
                total_h = h_data.get("total_handouts", len(h_data.get("handouts", [])))
                if total_h > 0 and not (work / "patches").is_dir() and not (work / "handout_patches").is_dir():
                    logger.warning(
                        "Advertencia: Existen %d handouts en work/handouts pero no se detectaron parches cosidos. "
                        "Asegúrate de ejecutar los subagentes de visión y 'run.py --stage stitch' antes de sintetizar cta-direct.",
                        total_h,
                    )
            except Exception:
                pass

        source_rel_str = None
        manifest_file = work / "pages" / "manifest.json"
        if not manifest_file.is_file():
            manifest_file = work / "manifest.json"
        if manifest_file.is_file():
            try:
                m_data = json.loads(manifest_file.read_text(encoding="utf-8"))
                sp = m_data.get("source_path")
                if sp:
                    p = Path(sp)
                    try:
                        source_rel_str = p.resolve().relative_to(Path.cwd().resolve()).as_posix()
                    except ValueError:
                        source_rel_str = p.as_posix()
            except Exception:
                pass

        source_files: List[str] = []
        if source_rel_str:
            s_dir = Path(source_rel_str)
            if s_dir.is_dir():
                source_files = sorted(f.name for f in s_dir.iterdir() if f.is_file())
            read_paths = [f"{source_rel_str}/{f}" for f in source_files] if source_files else [f"{source_rel_str}/*"]
            forbidden_cta = list(forbidden) + [
                "modificar o editar work/compile_cta.py (el compilador es inmutable; solo consulta su contrato con view_file si lo requieres)",
                "work/corpus*.md (el análisis cognitivo debe realizarse directamente sobre los materiales fuente asignados con view_file)",
                f"carpetas o archivos de otros cursos en content/ (distintas de {source_rel_str})",
                "content/* (excepto los materiales fuente asignados)",
                "work/pages/manifest.json (prohibido consultar o depender de manifest.json; citar directamente los archivos fuente asignados)",
                "scripts Python auxiliares (.py) en scratch/ o work/ (prohibido crear generadores en Python; usar exclusivamente cta_data.py y compile_cta.py)",
                "ejecutar comandos exploratorios o pruebas previas en terminal CLI (único comando permitido: 'python work/compile_cta.py')",
                "emitir competencias en el texto del chat (Do not output competencies in chat text)",
            ]
        else:
            read_paths = ["content/*"]
            forbidden_cta = list(forbidden) + [
                "modificar o editar work/compile_cta.py (el compilador es inmutable; solo consulta su contrato con view_file si lo requieres)",
                "work/corpus*.md (inspección directa de contenidos requerida)",
                "work/pages/manifest.json (prohibido consultar o depender de manifest.json)",
                "scripts Python auxiliares (.py) en scratch/ o work/ (usar exclusivamente cta_data.py y compile_cta.py)",
                "emitir competencias en el texto del chat (Do not output competencies in chat text)",
            ]

        # Ensure immutable compile_cta.py is copied to work directory
        compile_src = SKILL_DIR / "compile_cta.py"
        if compile_src.is_file():
            shutil.copy2(compile_src, work / "compile_cta.py")

        # Ensure cta_parts directory exists for backward compatibility without bait files
        (work / "cta_parts").mkdir(parents=True, exist_ok=True)

        if (work / "patches").is_dir():
            read_paths.append("work/patches/*.md")
        if (work / "handout_patches").is_dir():
            read_paths.append("work/handout_patches/*.md")

        write_paths = ["work/cta_data.py", "work/cta.json", "work/cta.md"]

        extra_cta_context = ""
        first_source_doc = source_files[0] if source_files else "material_fuente.pdf"
        if source_files:
            file_list_str = "\n".join(f"- `{f}`" for f in source_files)
            extra_cta_context = (
                f"### MATERIALES FUENTE ASIGNADOS ({source_rel_str}):\n"
                f"{file_list_str}\n\n"
                "Usa estos nombres exactos de archivo en el campo de evidencia (`evidence: doc, pag`). "
                f"Comienza INMEDIATAMENTE en el Turno 1 abriendo `{source_rel_str}/{first_source_doc}` con `view_file`."
            )

        bundle_file = generate_cta_direct_bundle(
            work_dir=work,
            read_paths=read_paths,
            write_paths=write_paths,
            forbidden_items=forbidden_cta,
            turn_budget=turn_budget,
            extra_context=extra_cta_context,
        )

        sys_text = ""
        sys_file = SKILL_DIR / sys_prompt
        if sys_file.is_file():
            try:
                sys_text = sys_file.read_text(encoding="utf-8")
            except Exception:
                pass

        prompt_lines = [
            "# Asignación de Tarea para Direct CTA Architect",
            "",
            "## SCOPE-LOCK (OBLIGATORIO)",
            "- **READ permitido:**",
        ]
        for r in read_paths:
            prompt_lines.append(f"  * `{r}`")
        prompt_lines.append("- **WRITE permitido:**")
        prompt_lines.append("  * `work/cta_data.py` (emisión de datos tabulares puros con write_to_file)")
        prompt_lines.append("  * `work/cta.json` y `work/cta.md` (generados automáticamente por `python work/compile_cta.py`)")
        prompt_lines.append("- **EJECUTABLE CLI permitido:**")
        prompt_lines.append("  * `python work/compile_cta.py` (compilador determinista pre-sembrado en work/)")
        prompt_lines.append("- **PROHIBIDO:**")
        for f in forbidden_cta:
            prompt_lines.append(f"  * {f}")

        if extra_cta_context:
            prompt_lines.extend(["", extra_cta_context])

        if sys_text:
            prompt_lines.extend(["", "## INSTRUCCIONES OPERATIVAS Y DIRECTIVAS", sys_text])

        prompt_lines.extend([
            "",
            "## INICIO INMEDIATO Y TERMINACIÓN OBLIGATORIA (ARQUITECTURA DE 2 ARCHIVOS)",
            f"- **TURNO 1 MANDATORIO:** Abre INMEDIATAMENTE `{source_rel_str}/{first_source_doc}` con `view_file`.",
            "- Queda TERMINANTEMENTE PROHIBIDO gastar Turno 1 leyendo `compile_cta.py`, explorando directorios o buscando archivos auxiliares.",
            "- El contrato completo de tuplas para `COMPETENCIES` está especificado al 100% en las directivas superiores.",
            "- El compilador `work/compile_cta.py` ya está pre-sembrado en disco y es INMUTABLE. No lo edites ni lo modifiques.",
            "- Emite las competencias en formato de tuplas tabulares compactas en `work/cta_data.py` usando `write_to_file`.",
            "- Para cursos extensos, emite en 2 o más bloques continuos usando `write_to_file` con `Append: true` para bloques subsecuentes.",
            "- Tras emitir los datos, ejecuta: `python work/compile_cta.py` para compilar y validar automáticamente.",
            "- Si el compilador o `check_cta.py` reportan errores (con tupla y número de línea exacto en `cta_data.py`), corrígelos quirúrgicamente con `replace_file_content` o reescribe con `write_to_file(Overwrite=True)`.",
            "- Re-ejecuta `python work/compile_cta.py` hasta obtener certificación limpia (`PASS`).",
            f"- Presupuesto de turnos sugerido: {turn_budget} turnos.",
            "- Do not output competencies in chat text. Terminate strictly with:",
            "`DONE: work/cta.json` (o BLOCKED: <motivo>).",
            "PROHIBIDO emitir resúmenes, explicaciones o saludos adicionales en el chat.",
        ])
        prompt_text = "\n".join(prompt_lines)
        subagents.append({
            "TypeName": spec["type_name"],
            "Role": "Direct CTA Architect",
            "Model": spec["model"],
            "Prompt": prompt_text,
        })
        dispatched_ids.append("direct")

    elif role == "vision-legacy":
        read_paths = ["work/pages/*", "work/vision_pages.json"]
        write_paths = ["work/patches/*.md"]
        bundle_file = _create_task_bundle(
            work_dir=work,
            bundle_name="vision_legacy",
            role_name=role,
            role_title="Legacy Page Patcher",
            system_prompt_rel=sys_prompt,
            read_paths=read_paths,
            write_paths=write_paths,
            forbidden_items=forbidden,
            turn_budget=turn_budget,
        )
        prompt_text = _format_prompt(
            role_name=role,
            role_title="Legacy Page Patcher",
            bundle_path=_bundle_display_path(bundle_file),
            turn_budget=turn_budget,
            read_paths=read_paths,
            write_paths=write_paths,
            forbidden_items=forbidden,
            system_prompt_rel=sys_prompt,
        )
        subagents.append({
            "TypeName": spec["type_name"],
            "Role": "Legacy Page Patcher",
            "Model": spec["model"],
            "Prompt": prompt_text,
        })
        dispatched_ids.append("legacy")

    payload = {"Subagents": subagents}

    # Snapshot pre-dispatch for automated scope verification
    snap = snapshot_work_dir(work)
    snap_file = dispatch_dir / f"{role}_snapshot.json"
    snap_payload = {k: list(v) for k, v in snap.items()}
    snap_file.write_text(json.dumps(snap_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Write audit log to work/dispatch/{role}.json
    audit_file = dispatch_dir / f"{role}.json"
    audit_payload = {
        "role": role,
        "dispatched_at": datetime.now(timezone.utc).isoformat(),
        "subagents_count": len(subagents),
        "Subagents": subagents,
    }
    audit_file.write_text(json.dumps(audit_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Update state.json
    state.setdefault("dispatched", {})[role] = list(sorted(set(dispatched_ids)))
    state_file.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    return payload


def snapshot_work_dir(work_dir: Union[str, Path]) -> Dict[str, Tuple[int, float]]:
    """Takes a snapshot of all files and their sizes/mtimes in work_dir.
    
    Returns:
        Dict mapping POSIX relative paths to (size_bytes, mtime_timestamp).
    """
    work = Path(work_dir).resolve()
    snapshot: Dict[str, Tuple[int, float]] = {}
    if not work.is_dir():
        return snapshot

    for root, _, files in os.walk(work):
        root_path = Path(root)
        for fname in files:
            fpath = root_path / fname
            try:
                st = fpath.stat()
                rel = fpath.relative_to(work).as_posix()
                snapshot[rel] = (st.st_size, st.st_mtime)
            except OSError:
                pass
    return snapshot


def _is_allowed_path(rel_path: str, role: str) -> bool:
    """Checks whether rel_path is an allowed write destination for the specified role."""
    norm = rel_path.replace("\\", "/").lstrip("/")

    # Internal pipeline / audit files that are always permitted
    if (
        norm.startswith("dispatch/")
        or norm.startswith("work/dispatch/")
        or norm in ("timings.json", "work/timings.json", "order.json", "work/order.json")
        or norm.startswith("__pycache__/")
        or norm.startswith(".pytest_cache/")
        or norm.startswith(".git/")
    ):
        return True

    spec = ROLE_SPECS.get(role)
    if not spec:
        return False

    write_patterns = spec.get("write", [])
    candidates = [norm]
    if norm.startswith("work/"):
        candidates.append(norm[5:])
    else:
        candidates.append(f"work/{norm}")

    for pattern in write_patterns:
        pat_clean = pattern.replace("\\", "/").lstrip("/")
        pat_candidates = [pat_clean]
        if pat_clean.startswith("work/"):
            pat_candidates.append(pat_clean[5:])
        else:
            pat_candidates.append(f"work/{pat_clean}")

        for cand in candidates:
            for pat in pat_candidates:
                # Direct glob match
                if fnmatch.fnmatch(cand, pat):
                    return True
                # Match parameterized templates like <comp_id> or <id> or _XX
                wildcard_pat = re.sub(r"<[^>]+>", "*", pat)
                wildcard_pat = re.sub(r"_XX\b", "_*", wildcard_pat)
                wildcard_pat = re.sub(r"XX\b", "*", wildcard_pat)
                if fnmatch.fnmatch(cand, wildcard_pat):
                    return True

    return False


def get_type_definitions() -> List[Dict[str, Any]]:
    """Returns concise type definitions for define_subagent registration."""
    return [dict(t) for t in TYPE_DEFINITIONS]


def scope_check(
    work_dir: Union[str, Path],
    role: str,
    snapshot: Optional[Dict[str, Tuple[int, float]]] = None,
) -> Tuple[bool, List[str]]:
    """Detects files created or modified outside the permitted write paths for role.
    
    Args:
        work_dir: Course working directory.
        role: Subagent role that just executed.
        snapshot: Snapshot dictionary from snapshot_work_dir prior to execution.
                 If None or empty, attempts to load work/dispatch/{role}_snapshot.json.

    Returns:
        Tuple of (is_clean, violations_list).
    """
    work = Path(work_dir).resolve()
    if not snapshot:
        snap_file = work / "dispatch" / f"{role}_snapshot.json"
        if snap_file.is_file():
            try:
                raw_snap = json.loads(snap_file.read_text(encoding="utf-8"))
                snapshot = {k: (v[0], v[1]) for k, v in raw_snap.items()}
            except Exception as e:
                logger.warning("Could not load snapshot file %s: %s", snap_file, e)
    if snapshot is None:
        snapshot = {}

    current_snapshot = snapshot_work_dir(work)
    violations: List[str] = []

    for rel_path, (size, mtime) in current_snapshot.items():
        if rel_path not in snapshot:
            # File newly created
            if not _is_allowed_path(rel_path, role):
                violations.append(rel_path)
        else:
            # File modified
            old_size, old_mtime = snapshot[rel_path]
            if (size, mtime) != (old_size, old_mtime):
                if not _is_allowed_path(rel_path, role):
                    violations.append(rel_path)

    violations.sort()
    is_clean = len(violations) == 0
    return is_clean, violations


def main() -> None:
    """CLI utility for subagent dispatch and scope checking."""
    parser = argparse.ArgumentParser(description="Subagent Scope-Lock & Dispatch Generator")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # dispatch subcommand
    disp = subparsers.add_parser("build", help="Generate invoke_subagent payload for role")
    disp.add_argument("--role", required=True, choices=list(ROLE_SPECS.keys()), help="Subagent role")
    disp.add_argument("--work-dir", required=True, help="Course working directory")
    disp.add_argument("--ready-only", action="store_true", help="Dispatch only ready sections")
    disp.add_argument("--ids", nargs="*", help="Optional specific IDs to dispatch")

    # check subcommand
    chk = subparsers.add_parser("check", help="Run scope violation check")
    chk.add_argument("--role", required=True, choices=list(ROLE_SPECS.keys()), help="Subagent role")
    chk.add_argument("--work-dir", required=True, help="Course working directory")

    # define-types subcommand
    subparsers.add_parser("define-types", help="Print define_subagent payloads for all c2c types")

    args = parser.parse_args()

    if args.action == "define-types":
        print(json.dumps(get_type_definitions(), indent=2, ensure_ascii=False))

    elif args.action == "build":
        payload = build_dispatch(
            role=args.role,
            work_dir=args.work_dir,
            ids=args.ids,
            ready_only=args.ready_only,
        )
        print(json.dumps(payload, indent=2, ensure_ascii=False))

    elif args.action == "check":
        # Check against persisted pre-dispatch snapshot or empty if not present
        is_clean, violations = scope_check(args.work_dir, args.role, None)
        if is_clean:
            print(f"[+] Scope-check PASSED for role '{args.role}'.")
            sys.exit(0)
        else:
            print(f"[-] Scope-check FAILED for role '{args.role}'. {len(violations)} violations detected:")
            for v in violations:
                print(f"    * {v}")
            sys.exit(1)


if __name__ == "__main__":
    main()
