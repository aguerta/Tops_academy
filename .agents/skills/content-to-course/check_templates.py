"""Template validator for content-to-course v2.

Validates parametric exercise templates against template.schema.json and enforces:
- AST sandbox whitelist security
- 50-seed dry run execution without runtime or timeout errors
- Invariant evaluation on 100% of dry-run instances
- TPL-D1: all distractor_ids referenced exist in the competency's declared distractors in cta.json
- TPL-D2: MC7 items use 6 distinct distractor_ids
- TPL-D3: 100% distractor coverage across templates for each competency
- TPL-D4: distractors != correct answer on 100% of instances
"""

import argparse
import json
import os
import re
import sys
import zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import jsonschema

# Add skills root and project src to sys.path so engine and validator can be imported directly
_skills_root = Path(__file__).parent.resolve()
if str(_skills_root) not in sys.path:
    sys.path.insert(0, str(_skills_root))

_project_root = Path(__file__).resolve().parents[3]
_src_dir = _project_root / "src"
if str(_src_dir) not in sys.path and _src_dir.is_dir():
    sys.path.insert(0, str(_src_dir))
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from engine.assemble import assemble_question, format_template_string
from engine.diversity import evaluate_competency_diversity, mask_stem_numbers
from engine.invariants import check_instance_invariants, validate_katex_syntax
from engine.instantiate import instantiate_competency, competency_seed_base
from engine.sandbox import (
    execute_sandbox_batch,
    validate_code_ast,
    check_latex_escape_corruption,
    warm_up_sandbox,
    SandboxExecutionError,
    SandboxTimeoutError,
    SecurityViolationError,
)
from validator.core import validate_course_content


AGENT_WARNING_NOTE = (
    "NOTA PARA EL AGENTE: NO abras ni inspecciones el código de check_templates.py ni rules.py. "
    "Corrige directamente el texto en tu script generador."
)


def format_diagnostic_error(
    rule_tag: str,
    competency: str,
    template: str,
    item_id: str,
    field_name: str,
    snippet: str,
    cause: str,
    actions: List[str],
) -> str:
    """Format validation error with enriched surgical and prescriptive diagnostics."""
    actions_formatted = "\n".join(f"      {idx + 1}. {act}" for idx, act in enumerate(actions))
    primary_action = actions[0] if actions else "Corrige el archivo generador."
    return (
        f"[-] [{rule_tag}]\n"
        f"    UBICACIÓN: Competencia: '{competency}', Plantilla: '{template}', Reactivo: '{item_id}', Campo: '{field_name}'\n"
        f"    FRAGMENTO INFRACTOR: {snippet}\n"
        f"    CAUSA: {cause}\n"
        f"    ACTION REQUIRED: {primary_action}\n"
        f"    ACCIONES CORRECTIVAS:\n"
        f"{actions_formatted}\n"
        f"    {AGENT_WARNING_NOTE}"
    )


def format_invariant_error_diagnostic(
    cid: str,
    tpl_id: str,
    q_id: str,
    inv_err: str,
    q_obj: Optional[Dict[str, Any]] = None,
) -> str:
    """Formats an error from check_instance_invariants into the enriched diagnostic structure."""
    inv_clean = inv_err.strip()

    # Case A: Unsubstituted template variable '{var}'
    m_var = re.search(r"Unsubstituted template variable '\{([^}]+)\}' detected in (.+)", inv_clean)
    if m_var:
        var_name = m_var.group(1)
        field_name = m_var.group(2).rstrip(".")
        snippet = f"{{{var_name}}}"
        cause = f"Llaves '{{{var_name}}}' no declaradas en el diccionario 'vars' generado en generate_py o no sustituidas en el campo '{field_name}'."
        actions = [
            f"Usar '${var_name}$' si se trata de notación matemática en LaTeX.",
            "Quitar las llaves '{}' si es texto plano literal no paramétrico.",
            f"Declarar '{var_name}' en el diccionario 'vars' retornado por generate_py.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case B: Triple dollar delimiter '$$$'
    if "$$$" in inv_clean:
        m_ctx = re.search(r"detected in (.+)", inv_clean)
        field_name = m_ctx.group(1).rstrip(".") if m_ctx else "stem / hint / text"
        snippet = "$$$"
        cause = f"Delimitador matemático triple '$$$' inválido detectado en '{field_name}'."
        actions = [
            "Reemplazar '$$$' por '$$' si se trata de un bloque matemático en display mode.",
            "Reemplazar '$$$' por '$' si es matemática inline.",
            "Asegurar que los delimitadores de apertura y cierre coincidan sin signos de dólar redundantes.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case C: Unbalanced display math delimiter '$$'
    if "Unbalanced display math delimiter '$$'" in inv_clean:
        m_ctx = re.search(r"in (.+)", inv_clean)
        field_name = m_ctx.group(1).rstrip(".") if m_ctx else "stem / hint / text"
        snippet = "$$"
        cause = f"Delimitadores '$$' de display math no balanceados en '{field_name}' (número impar de '$$')."
        actions = [
            "Asegurarse de que cada '$$' de apertura tenga un '$$' de cierre.",
            "No mezclar '$$' con '$' en la misma expresión matemática.",
            "Escapar cualquier símbolo de dólar literal como '\\$'.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case D: Unbalanced inline math delimiter '$'
    if "Unbalanced inline math delimiter '$'" in inv_clean:
        m_ctx = re.search(r"in (.+)", inv_clean)
        field_name = m_ctx.group(1).rstrip(".") if m_ctx else "stem / hint / text"
        snippet = "$"
        cause = f"Delimitadores '$' de matemática inline no balanceados en '{field_name}' (número impar de '$')."
        actions = [
            "Verificar que cada '$' de apertura cuente con su correspondiente '$' de cierre.",
            "Escapar cualquier símbolo de dólar literal o de moneda como '\\$'.",
            "Evitar saltos de línea o texto no matemático dentro del bloque '$...$'.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case E: Residual double curly braces '{{' or '}}'
    if "Residual double curly braces" in inv_clean:
        m_ctx = re.search(r"detected in (.+)", inv_clean)
        field_name = m_ctx.group(1).rstrip(".") if m_ctx else "stem / hint / text"
        snippet = "{{ o }}"
        cause = f"Llaves dobles residuales '{{' o '}}' provenientes de formato o f-string de Python en '{field_name}'."
        actions = [
            "Usar llaves simples '{...}' para grupos en LaTeX en lugar de llaves dobles '{{...}}'.",
            "Revisar el escape de llaves en f-strings dentro de generate_py.",
            "Utilizar raw strings r'...' para expresiones KaTeX.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case F: Unbalanced curly braces in LaTeX math expression
    if "Unbalanced curly braces in LaTeX math expression" in inv_clean:
        m_ctx = re.search(r"in ([^:]+):\s*'(.*)'", inv_clean)
        field_name = m_ctx.group(1).strip() if m_ctx else "math expression"
        snippet = m_ctx.group(2) if m_ctx else "{ o }"
        cause = f"Llaves curvas '{{' y '}}' desbalanceadas dentro de la fórmula LaTeX en '{field_name}': '{snippet}'."
        actions = [
            "Contar y balancear las llaves '{' y '}' en la expresión LaTeX.",
            "Si se usaron llaves literales escapadas '\\{', asegurar que la barra invertida esté presente.",
            "Revisar macros de LaTeX con múltiples argumentos como \\frac{a}{b} donde falte una llave de cierre.",
        ]
        return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, snippet, cause, actions)

    # Case F2: Unclosed nested LaTeX macro or accent
    if "Unclosed nested macro brace detected" in inv_clean or "nested macro" in inv_clean:
        m_ctx = re.search(r"in ([^:]+):", inv_clean)
        field_name = m_ctx.group(1).strip() if m_ctx else "math expression"
        return format_diagnostic_error(
            "R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, inv_clean,
            f"Acento o macro anidado de LaTeX sin cerrar correctamente en '{field_name}'.",
            [
                "Asegurar que macros anidados como \\hat{\\boldsymbol{\\beta}} tengan ambas llaves de cierre '}}'.",
                "Revisar expresiones matemáticas con acentos combinados con estilos vectoriales o matriciales.",
                "Balancear todas las llaves en la fórmula.",
            ],
        )

    # Case F3: Macro arity / unclosed argument
    if "requires 2 arguments" in inv_clean or "unclosed first argument" in inv_clean or "unclosed second argument" in inv_clean or "missing argument brackets" in inv_clean:
        m_ctx = re.search(r"in ([^.]+)", inv_clean)
        field_name = m_ctx.group(1).strip() if m_ctx else "math expression"
        return format_diagnostic_error(
            "R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, inv_clean,
            f"Macro de LaTeX (como \\frac, \\binom, \\overset) con aridad incorrecta o argumento incompleto en '{field_name}'.",
            [
                "Comprobar que \\frac posea tanto numerador como denominador: \\frac{num}{den}.",
                "Cerrar adecuadamente cada bloque de llaves '{...}'.",
                "Evitar macros con argumentos incompletos antes del cierre del delimitador '$'.",
            ],
        )

    # Case F4: Unclosed or mismatched LaTeX environment
    if "LaTeX environment" in inv_clean:
        m_ctx = re.search(r"in ([^.]+)", inv_clean)
        field_name = m_ctx.group(1).strip() if m_ctx else "math expression"
        return format_diagnostic_error(
            "R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, inv_clean,
            f"Entorno LaTeX sin cerrar o con cierre discordante en '{field_name}'.",
            [
                "Asegurar que cada \\begin{env} tenga su correspondiente \\end{env}.",
                "Verificar entornos matriciales o de casos como pmatrix, bmatrix, cases, aligned.",
                "Comprobar que no haya errores tipográficos en el nombre del entorno.",
            ],
        )

    # Case F5: Unclosed or unmatched scalable delimiter
    if "scalable delimiter" in inv_clean:
        m_ctx = re.search(r"in ([^.]+)", inv_clean)
        field_name = m_ctx.group(1).strip() if m_ctx else "math expression"
        return format_diagnostic_error(
            "R-20: SINTAXIS / LLAVES", cid, tpl_id, q_id, field_name, inv_clean,
            f"Delimitador escalable \\left o \\right sin emparejar en '{field_name}'.",
            [
                "Emparejar cada \\left( con \\right), \\left[ con \\right], \\left\\{ con \\right\\}.",
                "Si se requiere un delimitador invisible, usar \\left. o \\right..",
                "Verificar la simetría de paréntesis y corchetes en las fórmulas matemáticas.",
            ],
        )

    # Case G: Distractor identical to correct answer (TPL-D4)
    if "Distractor identical to correct answer" in inv_clean:
        m_d = re.search(r"Distractor identical to correct answer:\s*'(.*)'", inv_clean)
        snippet = m_d.group(1) if m_d else inv_clean
        cause = f"Un distractor generado en generate_py es idéntico a la respuesta correcta ('{snippet}')."
        actions = [
            "Verificar en generate_py que los distractores nunca tomen el valor de la clave correcta.",
            "Añadir una guarda en generate_py que desplace o regenere el distractor si colisiona con 'correct'.",
            "Comprobar casos particulares donde parámetros aleatorios anulen la diferencia.",
        ]
        return format_diagnostic_error("TPL-D4: DISTRACTOR IDÉNTICO A RESPUESTA CORRECTA", cid, tpl_id, q_id, "options", snippet, cause, actions)

    # Case H: Length anti-giveaway violation (R-15)
    if "Length anti-giveaway violation" in inv_clean:
        cause = "La longitud de la respuesta correcta difiere significativamente del rango de los distractores (fuera de 0.80x - 1.20x)."
        actions = [
            "Calibrar la longitud de la respuesta correcta o de los distractores para que tengan una extensión homogénea.",
            "Homogeneizar el nivel de detalle y formato matemático entre todas las opciones.",
            "Asegurar que 0.80 * min(len(D)) <= len(correct) <= 1.20 * max(len(D)).",
        ]
        return format_diagnostic_error("R-15: EQUILIBRIO DE LONGITUD", cid, tpl_id, q_id, "options", inv_clean, cause, actions)

    # Case I: Answer leak (R-19)
    if "leaked verbatim in" in inv_clean:
        cause = "El valor o texto de la respuesta correcta aparece textualmente en el stem o en la primera pista, revelando la clave."
        actions = [
            "Remover la mención textual de la respuesta del enunciado de la pregunta o de la primera pista.",
            "Reformular la primera pista para que oriente sobre el método conceptual sin dar el resultado numérico/algebraico.",
            "Verificar que la consigna plantee el problema requiriendo el cálculo en lugar de enunciar la solución.",
        ]
        return format_diagnostic_error("R-19: FUGA DE RESPUESTA", cid, tpl_id, q_id, "stem / hints[0]", inv_clean, cause, actions)

    # Case J: Missing error_rationale
    if "must possess a non-empty 'error_rationale'" in inv_clean:
        is_ms = "MS option" in inv_clean
        rule_tag = "R-22: RATIONALE EN MULTIPLE_SELECT" if is_ms else "R-17: RATIONALE FALTANTE EN DISTRACTOR"
        m_opt = re.search(r"option\s+(\d+)", inv_clean, re.IGNORECASE)
        opt_idx = m_opt.group(1) if m_opt else "X"
        field_name = f"options[{opt_idx}].error_rationale"
        cause = f"La opción distractora {opt_idx} con is_correct=False carece de un 'error_rationale' explicativo."
        actions = [
            "Agregar una explicación diagnóstica en 'error_rationale' para cada opción con is_correct=False.",
            "Describir la falacia conceptual o error procedimental que lleva a seleccionar dicha opción.",
            "Asegurar que el texto de rationale no sea una cadena vacía ni un placeholder genérico.",
        ]
        return format_diagnostic_error(rule_tag, cid, tpl_id, q_id, field_name, "(vacío o ausente)", cause, actions)

    # Case K: Duplicate options
    if "Duplicate option content detected" in inv_clean:
        m_opt = re.search(r"detected(?:\s+in\s+MS)?:\s*'(.*)'", inv_clean)
        snippet = m_opt.group(1) if m_opt else inv_clean
        cause = f"Dos o más opciones tienen contenido idéntico ('{snippet}')."
        actions = [
            "Garantizar que todos los distractores generados en generate_py sean disjuntos y únicos.",
            "Agregar una comprobación en generate_py que descarte o regenere opciones repetidas.",
            "Variar las fórmulas de perturbación para producir valores distintos.",
        ]
        return format_diagnostic_error("TPL-D4: OPCIONES DUPLICADAS", cid, tpl_id, q_id, "options", snippet, cause, actions)

    # Fallback Invariant
    return format_diagnostic_error(
        rule_tag="INVARIANT: invariant violation",
        competency=cid,
        template=tpl_id,
        item_id=q_id,
        field_name="instance",
        snippet=inv_clean,
        cause=f"Template '{tpl_id}' invariant violation ({q_id}): {inv_clean}",
        actions=[
            "Revisar la salida de generate_py para cumplir con los requerimientos estructurales del reactivo.",
            "Asegurar que todos los campos requeridos estén presentes y sean del tipo esperado.",
            "Verificar que el reactivo cumpla con la especificación de interaction_type.",
        ],
    )


def format_parity_error(
    cid: str,
    err: Any,
    questions_by_id: Dict[str, Dict[str, Any]],
) -> str:
    """Formats a ValidationError from production parity check with prescriptive diagnosis."""
    rule_id = getattr(err, "rule_id", "PARITY")
    msg = getattr(err, "message", str(err))
    item_id = getattr(err, "item_id", None) or "UNKNOWN"
    q = questions_by_id.get(item_id, {})
    tpl_id = q.get("template_id") or "UNKNOWN"

    # Rule R-20
    if rule_id == "R-20":
        m_field = re.search(r"in\s+([a-zA-Z0-9_.\[\]]+):", msg)
        field_name = m_field.group(1) if m_field else "stem / options / text"

        if "Unreplaced template variable" in msg:
            m_s = re.search(r"Unreplaced template variable\(s\) found:\s*(.*)", msg)
            snippet = m_s.group(1) if m_s else "{var}"
            cause = f"Llaves '{snippet}' no declaradas en el diccionario 'vars' retornado por generate_py o no reemplazadas en '{field_name}'."
            actions = [
                f"Usar '${snippet.replace('{','').replace('}','')}$' si se trata de notación matemática en LaTeX.",
                "Quitar las llaves '{}' si es texto plano literal no paramétrico.",
                f"Agregar la clave sin llaves al diccionario 'vars' retornado por generate_py.",
            ]
            return format_diagnostic_error("R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, snippet, cause, actions)

        if "Unbalanced display math delimiters '$$'" in msg:
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, "$$",
                f"Delimitadores '$$' de display math no balanceados en '{field_name}' (número impar de '$$').",
                [
                    "Asegurarse de que cada '$$' de apertura tenga un '$$' de cierre.",
                    "No mezclar '$$' con '$' en la misma expresión.",
                    "Escapar cualquier símbolo de dólar literal como '\\$'.",
                ]
            )

        if "Unbalanced inline math delimiters '$'" in msg:
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, "$",
                f"Delimitadores '$' de matemática en línea no balanceados en '{field_name}' (número impar de '$').",
                [
                    "Verificar que cada '$' de apertura cuente con su correspondiente '$' de cierre.",
                    "Escapar cualquier símbolo de dólar literal como '\\$'.",
                    "Comprobar que no haya saltos de línea dentro del bloque '$...$'.",
                ]
            )

        if "Forbidden triple math delimiter '$$$'" in msg:
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, "$$$",
                f"Delimitador matemático triple '$$$' inválido detectado en '{field_name}'.",
                [
                    "Reemplazar '$$$' por '$$' si es bloque matemático en display mode.",
                    "Reemplazar '$$$' por '$' si es matemática inline.",
                    "Asegurar que los delimitadores de apertura y cierre coincidan.",
                ]
            )

        if "Residual double braces" in msg:
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, "{{ o }}",
                f"Llaves dobles residuales '{{' o '}}' provenientes de f-strings en Python dentro de '{field_name}'.",
                [
                    "Usar llaves simples '{...}' para grupos en LaTeX en lugar de llaves dobles '{{...}}'.",
                    "Revisar el escape de llaves en f-strings dentro de generate_py.",
                    "Utilizar raw strings r'...' para expresiones KaTeX.",
                ]
            )

        if "Unbalanced curly braces in LaTeX math block" in msg:
            m_s = re.search(r"LaTeX math block:\s*'(.*)'", msg)
            snippet = m_s.group(1) if m_s else "{ o }"
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, snippet,
                f"Llaves curvas '{{' y '}}' desbalanceadas dentro de la fórmula LaTeX en '{field_name}': '{snippet}'.",
                [
                    "Contar y balancear las llaves '{' y '}' en la expresión LaTeX.",
                    "Asegurar que llaves literales estén escapadas como '\\{'.",
                    "Revisar macros de LaTeX como \\frac{a}{b} donde falte una llave de cierre.",
                ]
            )

        if "Leaked raw code variable identifier" in msg:
            m_s = re.search(r"identifier\(s\) found:\s*(.*)", msg)
            snippet = m_s.group(1) if m_s else "identificador de código"
            return format_diagnostic_error(
                "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, snippet,
                f"Identificador interno de código filtrado al texto del reactivo ({snippet}).",
                [
                    "Eliminar o formatear las variables internas de código antes de insertarlas en el texto.",
                    "Reemplazar identificadores crudos (_val, _num, _str) por su valor formateado o símbolo matemático.",
                    "Verificar que el texto dirigido al estudiante sea completamente natural y pedagógico.",
                ]
            )

        return format_diagnostic_error(
            "R-20: SINTAXIS / LLAVES", cid, tpl_id, item_id, field_name, msg,
            f"Error de sintaxis KaTeX o delimitadores en '{field_name}'.",
            [
                "Revisar la sintaxis de KaTeX y los delimitadores '$' y '$$'.",
                "Asegurar que todas las llaves '{' y '}' estén balanceadas.",
                "Verificar que no queden placeholders sin sustituir.",
            ]
        )

    # Rule R-18
    if rule_id == "R-18":
        m_field = re.search(r"Option '([^']+)'", msg)
        opt_id = m_field.group(1) if m_field else "option"
        field_name = f"options[{opt_id}].content"
        m_s = re.search(r"visible content:\s*'(.*)'", msg)
        snippet = m_s.group(1) if m_s else msg
        cause = "Uso de términos metalingüísticos o autocríticos ('confundiendo', 'asumiendo erróneamente', etc.) en el texto visible de la opción que revelan al estudiante que es un distractor."
        actions = [
            "Reescribir el contenido de la opción como una afirmación objetiva o resultado alternativo plausible sin juzgar su veracidad en el texto visible.",
            "Mover la justificación del error ('confundiendo...', 'asumiendo erróneamente...') exclusivamente al campo 'error_rationale'.",
            "Asegurar que todas las opciones mantengan una apariencia neutra y verosímil sin dar pistas psicométricas.",
        ]
        return format_diagnostic_error("R-18: META-INFORMACIÓN / GIVEAWAY", cid, tpl_id, item_id, field_name, snippet, cause, actions)

    # Rule R-19
    if rule_id == "R-19":
        field_name = "stem"
        m_s = re.search(r"answer '([^']+)' leaked", msg)
        snippet = m_s.group(1) if m_s else msg
        cause = "El valor o clave de la respuesta correcta aparece textualmente dentro del stem del reactivo (fuga de respuesta), o hay sustitución que corrompió un operador (ej. \\dot<número>)."
        actions = [
            "Remover el valor o expresión de respuesta del enunciado (stem) reemplazándolo por una consigna neutra o línea de completación.",
            "Asegurar que las variables de LaTeX no sustituyan números directamente dentro de macros sin llaves.",
            "Verificar que la consigna plantee el problema requiriendo el cálculo en lugar de mostrar la solución.",
        ]
        return format_diagnostic_error("R-19: FUGA DE RESPUESTA / SINTAXIS", cid, tpl_id, item_id, field_name, snippet, cause, actions)

    # Rule R-22
    if rule_id == "R-22":
        m_field = re.search(r"Option '([^']+)'", msg)
        opt_id = m_field.group(1) if m_field else "option"
        field_name = f"options[{opt_id}].error_rationale"
        cause = "Opción incorrecta (is_correct=False) en ítem de selección múltiple (multiple_select) carece de 'error_rationale' diagnóstico formativo."
        actions = [
            "Agregar una explicación diagnóstica en 'error_rationale' para cada opción con is_correct=False.",
            "Explicar la falacia conceptual o el cálculo incorrecto que conduce a seleccionar dicha opción.",
            "Asegurarse de que el texto de rationale no esté vacío ni sea un placeholder genérico.",
        ]
        return format_diagnostic_error("R-22: RATIONALE EN MULTIPLE_SELECT", cid, tpl_id, item_id, field_name, "(vacío o ausente)", cause, actions)

    # Rule R-17
    if rule_id == "R-17":
        m_field = re.search(r"Option '([^']+)'", msg)
        opt_id = m_field.group(1) if m_field else "option"
        field_name = f"options[{opt_id}].error_rationale"
        m_s = re.search(r"error_rationale':\s*'(.*)'", msg)
        snippet = m_s.group(1) if m_s else "(vacío o placeholder)"
        cause = "El campo 'error_rationale' contiene un placeholder genérico prohibido (ej. 'placeholder', 'distractor', 'error') o está vacío."
        actions = [
            "Redactar una explicación pedagógica formativa sobre el error que comete el estudiante al elegir la opción.",
            "Eliminar palabras prohibidas como 'placeholder', 'distractor', 'error', 'n/a' o 'ninguno'.",
            "Describir la confusión conceptual o error algebraico/aritmético subyacente.",
        ]
        return format_diagnostic_error("R-17: RATIONALE GENÉRICO / PLACEHOLDER", cid, tpl_id, item_id, field_name, snippet, cause, actions)

    # Rule R-15
    if rule_id == "R-15":
        cause = "La longitud de la respuesta correcta difiere significativamente del rango de los distractores (fuera de 0.80x - 1.20x), constituyendo una pista visual."
        actions = [
            "Calibrar la longitud de la respuesta correcta o de los distractores para que tengan una extensión homogénea.",
            "Homogeneizar el nivel de detalle y formato matemático entre todas las opciones.",
            "Asegurar que 0.80 * min(len(D)) <= len(correct) <= 1.20 * max(len(D)).",
        ]
        return format_diagnostic_error("R-15: EQUILIBRIO DE LONGITUD", cid, tpl_id, item_id, "options", msg, cause, actions)

    # Rule S-01
    if rule_id == "S-01":
        return format_diagnostic_error(
            "S-01: SOLUCIÓN PASO A PASO OBLIGATORIA", cid, tpl_id, item_id, "solution / detailed_solution",
            "(vacío o ausente)",
            "El reactivo carece de una solución explicativa paso a paso requerida en modo strict.",
            [
                "Agregar el campo 'detailed_solution' o 'solution' en la plantilla con la resolución paso a paso.",
                "Describir el procedimiento matemático o conceptual completo para llegar a la respuesta correcta.",
                "Asegurar que la solución esté redactada con KaTeX válido.",
            ]
        )

    # Rule S-02
    if rule_id == "S-02":
        return format_diagnostic_error(
            "S-02: MISCONCEPTION WARNING OBLIGATORIO", cid, tpl_id, item_id, "misconception_warning",
            "(vacío o ausente)",
            "El reactivo carece de una advertencia de error común ('misconception_warning') requerida en modo strict.",
            [
                "Agregar el campo 'misconception_warning' o 'common_misconception_warning' en la plantilla.",
                "O asociar distractor_ids que tengan 'remediation_hint' definido en cta.json.",
                "Explicar brevemente el error más común que deben evitar los estudiantes.",
            ]
        )

    # Rule S-03
    if rule_id == "S-03":
        return format_diagnostic_error(
            "S-03: DIFICULTAD EXPLÍCITA", cid, tpl_id, item_id, "difficulty",
            "(inválido o ausente)",
            "El reactivo no especifica un nivel de dificultad válido ('easy', 'medium', 'hard') en modo strict.",
            [
                "Declarar 'difficulty': 'easy', 'medium' o 'hard' en la plantilla.",
                "Alinear la dificultad con el nivel de Bloom y la complejidad del problema.",
                "No dejar el campo vacío ni con valores no reconocidos.",
            ]
        )

    # Generic Fallback
    action_fallback = "Revisa la regla y ajusta el generador o las variantes."
    return format_diagnostic_error(
        f"{rule_id}: CONTRATO DE VALIDACIÓN", cid, tpl_id, item_id, "question",
        msg,
        f"Violación de la regla {rule_id}: {msg}",
        [
            action_fallback,
            "Verificar la estructura y tipos de datos de los reactivos producidos.",
            "Corregir directamente en el script generador o archivo de plantillas.",
        ]
    )


def check_production_parity_for_competency(
    cid: str,
    competency: Union[Dict[str, Any], Any],
    questions: List[Dict[str, Any]],
    strict: bool = True,
) -> List[str]:
    """Runs production validator core on instantiated competency questions.
    
    Guarantees Isomorphic Contract Parity: passing check_templates locally
    mathematically guarantees passing build and verify in production.
    """
    errors: List[str] = []
    if not questions:
        return errors

    if isinstance(competency, dict):
        comp_name = competency.get("name", cid)
        comp_type = competency.get("type", "concept")
        comp_desc = competency.get("description", f"Competencia {cid}")
    else:
        comp_name = getattr(competency, "name", cid)
        comp_type = getattr(competency, "type", "concept")
        comp_desc = getattr(competency, "description", f"Competencia {cid}")

    mini_course = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "schema_version": "1.0.0",
        "course_id": f"parity_{cid.lower().replace('-', '_')}",
        "course_title": f"Parity Check for {cid}",
        "title": f"Parity Check for {cid}",
        "description": f"Local contract parity validation mini-course for competency {cid}.",
        "language": "es",
        "created_at": "2026-10-12T00:00:00Z",
        "competencies": [{
            "id": cid,
            "code": cid.upper(),
            "name": comp_name,
            "category": str(comp_type).title(),
            "description": comp_desc,
            "mastery_target": 100,
        }],
        "questions": questions,
    }

    try:
        raw_json = json.dumps(mini_course, ensure_ascii=False)
        v_res = validate_course_content(raw_json, strict=strict)
    except Exception as ex:
        errors.append(f"[-] PARITY VALIDATOR EXCEPTION for '{cid}': {ex}")
        return errors

    if not v_res.is_valid:
        questions_by_id = {q.get("id", ""): q for q in questions if isinstance(q, dict)}
        for err in v_res.errors:
            # Skip course-level checks inapplicable to single competency mini-course
            if err.rule_id in ("R-05", "R-06", "R-07", "R-08", "R-09", "R-16"):
                continue
            errors.append(format_parity_error(cid, err, questions_by_id))

    return errors


import functools


@functools.lru_cache(maxsize=8)
def get_compiled_validator(schema_name: str = "template.schema.json") -> jsonschema.Draft7Validator:
    schema_path = Path(__file__).parent / "schemas" / schema_name
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    return jsonschema.Draft7Validator(schema)


def load_schema(schema_name: str = "template.schema.json") -> Dict[str, Any]:
    """Load JSON Schema from schemas directory."""
    return get_compiled_validator(schema_name).schema


def validate_template_schema(data: Dict[str, Any]) -> List[str]:
    """Validate data against template.schema.json."""
    validator = get_compiled_validator("template.schema.json")
    errors = []
    for err in validator.iter_errors(data):
        loc = " -> ".join(str(p) for p in err.path)
        errors.append(f"Template schema violation at [{loc}]: {err.message}")
    return errors


def check_single_template(
    template: Dict[str, Any],
    competency_id: str,
    declared_distractor_ids: Set[str],
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]] = None,
    num_dry_run_seeds: int = 50,
) -> List[str]:
    """Validate a single template including AST, dry-run, invariants, and TPL rules."""
    errors = []
    tpl_id = template.get("id", "UNKNOWN")
    interaction_type = template.get("interaction_type", "")
    generate_py = template.get("generate_py", "")
    cross_check_py = template.get("cross_check_py", "")
    distractor_ids = template.get("distractor_ids", [])

    # 1. AST Sandbox validation & LaTeX corruption check
    try:
        validate_code_ast(generate_py)
    except Exception as e:
        errors.append(format_diagnostic_error(
            "AST: SEGURIDAD DEL GENERADOR", competency_id, tpl_id, tpl_id, "generate_py",
            str(e), f"El código de generate_py violó las reglas de seguridad del AST: {e}",
            [
                "Eliminar llamadas a funciones prohibidas o imports inseguros en generate_py.",
                "Usar únicamente módulos permitidos (math, random, fractions, sympy, etc.).",
                "Revisar la sintaxis de Python en generate_py.",
            ]
        ))

    for ec in check_latex_escape_corruption(generate_py):
        errors.append(format_diagnostic_error(
            "AST: CORRUPCIÓN DE ESCAPE LATEX", competency_id, tpl_id, tpl_id, "generate_py",
            str(ec), f"Posible corrupción de escape de LaTeX en generate_py: {ec}",
            [
                "Usar raw strings r'...' para literales que contengan barras invertidas '\\'.",
                "Evitar cadenas con escapes inválidos como '\\d', '\\b', '\\c' sin 'r' prefix.",
                "Verificar la generación de fórmulas KaTeX.",
            ]
        ))

    if cross_check_py:
        try:
            validate_code_ast(cross_check_py)
        except Exception as e:
            errors.append(format_diagnostic_error(
                "AST: SEGURIDAD DEL CROSS-CHECK", competency_id, tpl_id, tpl_id, "cross_check_py",
                str(e), f"El código de cross_check_py violó las reglas de seguridad del AST: {e}",
                [
                    "Eliminar llamadas a funciones prohibidas o imports inseguros en cross_check_py.",
                    "Usar únicamente módulos permitidos del sandbox.",
                    "Revisar la sintaxis de Python en cross_check_py.",
                ]
            ))
        for ec in check_latex_escape_corruption(cross_check_py):
            errors.append(format_diagnostic_error(
                "AST: CORRUPCIÓN DE ESCAPE LATEX", competency_id, tpl_id, tpl_id, "cross_check_py",
                str(ec), f"Posible corrupción de escape de LaTeX en cross_check_py: {ec}",
                [
                    "Usar raw strings r'...' para literales que contengan barras invertidas '\\'.",
                    "Evitar cadenas con escapes inválidos.",
                    "Verificar la generación de fórmulas KaTeX.",
                ]
            ))

    # 2. Rule TPL-D1: All referenced distractor_ids exist in competency CTA
    for did in distractor_ids:
        if did not in declared_distractor_ids:
            errors.append(format_diagnostic_error(
                "TPL-D1: DISTRACTOR NO DECLARADO EN CTA", competency_id, tpl_id, tpl_id, "distractor_ids",
                f"'{did}'",
                f"El distractor_id '{did}' referenciado en la plantilla no existe en la lista de distractores de '{competency_id}' en cta.json.",
                [
                    f"Verificar los distractores declarados para '{competency_id}' en cta.json y usar los IDs exactos.",
                    f"O declarar el distractor '{did}' en la competencia '{competency_id}' dentro de cta.json.",
                    "Corregir cualquier error tipográfico en el ID del distractor dentro del JSON de la plantilla.",
                ]
            ))

    # 3. Rule TPL-D2: MC7 must reference/use at least 6 distinct distractor_ids
    if interaction_type == "multiple_choice_7_options":
        if len(set(distractor_ids)) < 6:
            errors.append(format_diagnostic_error(
                "TPL-D2: REQUISITO DE 6 DISTRACTORES EN MC7", competency_id, tpl_id, tpl_id, "distractor_ids",
                f"{len(set(distractor_ids))} distractor_ids declarados: {distractor_ids}",
                "Las plantillas MC7 requieren exactamente 6 distractor_ids distintos para cubrir los 6 distractores psicométricos.",
                [
                    "Declarar al menos 6 distractor_ids únicos en el arreglo 'distractor_ids' de la plantilla.",
                    "Vincular cada uno de los 6 distractores generados en generate_py a un distractor_id declarado.",
                    "Revisar cta.json para seleccionar 6 distractores relevantes de la competencia.",
                ]
            ))

    # 4. Static validation of ALL stem_variants syntax with validate_katex_syntax
    stem_variants_list = template.get("stem_variants", [])
    if isinstance(stem_variants_list, list):
        for idx, variant in enumerate(stem_variants_list):
            if isinstance(variant, str):
                for kv_err in validate_katex_syntax(variant, f"stem_variants[{idx}]"):
                    errors.append(format_invariant_error_diagnostic(
                        cid=competency_id,
                        tpl_id=tpl_id,
                        q_id=f"stem_variants[{idx}]",
                        inv_err=kv_err,
                    ))

    # 5. Dry-run 50 seeds and invariant evaluation
    seeds = list(range(100, 100 + num_dry_run_seeds))
    try:
        batch_results = execute_sandbox_batch(
            generate_py=generate_py,
            seeds=seeds,
            cross_check_py=cross_check_py,
            timeout_per_item=2.0,
        )
    except Exception as e:
        errors.append(format_diagnostic_error(
            "TPL-DRY: FALLO EN EJECUCIÓN DRY-RUN", competency_id, tpl_id, "batch_execution", "generate_py / cross_check_py",
            str(e), f"La ejecución por lotes en el sandbox falló completamente: {e}",
            [
                "Revisar la sintaxis y excepciones en generate_py o cross_check_py.",
                "Asegurar que el código sea determinista y termine dentro del tiempo límite de 2.0s.",
                "Verificar que no haya dependencias externas no disponibles.",
            ]
        ))
        return errors

    failed_seeds = [r for r in batch_results if not r.get("success")]
    if failed_seeds:
        first_err = failed_seeds[0].get("error", "Unknown error")
        example_seeds = [str(r.get("seed")) for r in failed_seeds[:5]]
        errors.append(format_diagnostic_error(
            "TPL-DRY: FALLO EN EJECUCIÓN DRY-RUN", competency_id, tpl_id, f"seeds={', '.join(example_seeds)}", "generate_py / cross_check_py",
            f"Error en seed {failed_seeds[0].get('seed')}: {first_err}",
            f"La ejecución en sandbox falló en {len(failed_seeds)}/{num_dry_run_seeds} semillas evaluadas.",
            [
                "Revisar la excepción en generate_py (división por cero, clave faltante, error de tipos, etc.).",
                "Probar localmente la función generate_py con la semilla que causó el fallo.",
                "Agregar validaciones o restricciones a los parámetros aleatorios para evitar estados matemáticos inválidos.",
            ]
        ))
        if len(failed_seeds) == len(batch_results):
            # Full failure of all seeds: no instances can be evaluated further
            return errors

    # Check invariants and TPL-D4 on all generated instances (Full Sweep: NO premature break)
    for idx, item in enumerate(batch_results):
        if not item.get("success"):
            continue
        gen_res = item.get("result", {})
        seed_val = item.get("seed", idx)

        try:
            assembled_q = assemble_question(
                template=template,
                gen_result=gen_res,
                competency_id=competency_id,
                question_index=idx + 1,
                cta_distractors_map=cta_distractors_map,
                seed=seed_val,
            )
        except Exception as e:
            errors.append(format_diagnostic_error(
                "TPL-ASM: FALLO EN ENSAMBLAJE DE REACTIVO", competency_id, tpl_id, f"seed={seed_val}", "assemble_question",
                str(e), f"No se pudo ensamblar el reactivo con la salida de generate_py para la semilla {seed_val}: {e}",
                [
                    "Verificar que generate_py retorne los campos obligatorios ('correct', 'distractors', 'vars').",
                    "Asegurar que 'distractors' contenga al menos 6 elementos para preguntas MC7.",
                    "Verificar que no haya discrepancia de formato entre template y generate_py.",
                ]
            ))
            continue

        # Invariant check (Accumulate all failures: NO break)
        is_valid, inv_errors = check_instance_invariants(assembled_q, interaction_type)
        if not is_valid:
            for inv_err in inv_errors:
                errors.append(format_invariant_error_diagnostic(
                    cid=competency_id,
                    tpl_id=tpl_id,
                    q_id=f"seed={seed_val}",
                    inv_err=inv_err,
                    q_obj=assembled_q,
                ))

        # Rule TPL-D4: Distractors != correct answer (Evaluate all distractors: NO break)
        if interaction_type == "multiple_choice_7_options":
            options = assembled_q.get("options", [])
            correct_opt = next((o for o in options if o.get("is_correct")), None)
            if correct_opt:
                c_content = str(correct_opt.get("content", "")).strip()
                for opt_idx, opt in enumerate(options):
                    if not opt.get("is_correct") and str(opt.get("content", "")).strip() == c_content:
                        errors.append(format_diagnostic_error(
                            "TPL-D4: TPL-D4 violation: DISTRACTOR IDÉNTICO A RESPUESTA CORRECTA", competency_id, tpl_id, f"seed={seed_val}", f"option {opt_idx + 1}",
                            f"'{c_content}'",
                            f"TPL-D4 violation in '{tpl_id}' (seed={seed_val}): distractor matches correct answer '{c_content}'",
                            [
                                "Asegurar en generate_py que la perturbación aplicada al distractor nunca dé el mismo valor que 'correct'.",
                                "Agregar una verificación en generate_py que modifique el distractor si colisiona con la clave.",
                                "Revisar los casos degenerados de los parámetros que puedan anular la diferencia.",
                            ]
                        ))

    # 5. Rule TPL-VAR: Early variability and parametric capacity validation
    # a) Verify vars dictionary is not empty across generated results
    has_empty_vars = any(
        len(r.get("result", {}).get("vars", {})) == 0 for r in batch_results if r.get("success")
    )
    if has_empty_vars:
        errors.append(format_diagnostic_error(
            "TPL-VAR: DIVERSIDAD DE REACTIVOS", competency_id, tpl_id, "generate_py", "vars",
            "vars: {}",
            f"TPL-VAR violation in '{tpl_id}': 'vars' dictionary is empty. Templates must generate dynamic variables.",
            [
                "Generar variables aleatorias en generate_py (ej. a = random.randint(1, 9)) y retornarlas en vars={'a': a}.",
                "Asegurar que generate_py defina y retorne variables para todos los placeholders del enunciado.",
                "No utilizar constantes estáticas sin parametrizar en generate_py.",
            ]
        ))

    # b) Verify stem contains at least one placeholder {var} or stem_variants is present
    stem = template.get("stem", "")
    stem_variants = template.get("stem_variants")
    has_placeholder = bool(re.search(r"\{[A-Za-z0-9_]+\}", stem))
    has_variants = bool(stem_variants and len(stem_variants) > 0)
    if not (has_placeholder or has_variants):
        errors.append(format_diagnostic_error(
            "TPL-VAR: DIVERSIDAD DE REACTIVOS", competency_id, tpl_id, "template", "stem / stem_variants",
            f"stem: '{stem[:60]}...'",
            f"TPL-VAR violation in '{tpl_id}': stem must contain at least one placeholder '{{var}}' or 'stem_variants' must be present.",
            [
                "Insertar al menos un placeholder dinámico como '{a}' o '{x}' en el campo 'stem'.",
                "O proveer una lista de 3 a 5 formulaciones alternativas en 'stem_variants'.",
                "Verificar que las variables coincidan con las claves generadas en generate_py.",
            ]
        ))

    # c) Unique capacity simulation across dry-run seeds
    seen_params = set()
    seen_stems = set()
    unique_instances = set()
    sim_unique = 0
    for item in batch_results:
        if not item.get("success"):
            continue
        gen_res = item.get("result", {})
        variables = gen_res.get("vars", {})
        param_tuple = tuple(sorted((str(k), str(v)) for k, v in variables.items()))

        stem_raw = stem
        if stem_variants and len(stem_variants) > 0:
            var_idx = (item.get("seed", 0) % len(stem_variants))
            stem_raw = stem_variants[var_idx]
        rendered_stem = format_template_string(stem_raw, variables)
        norm_stem = re.sub(r"\s+", " ", rendered_stem.strip())

        unique_instances.add((param_tuple, norm_stem))
        if param_tuple not in seen_params and norm_stem not in seen_stems:
            seen_params.add(param_tuple)
            seen_stems.add(norm_stem)
            sim_unique += 1

    unique_count = min(len(unique_instances), sim_unique)
    if unique_count < 4:
        errors.append(format_diagnostic_error(
            "TPL-VAR: DIVERSIDAD DE REACTIVOS", competency_id, tpl_id, "dry-run", "generate_py / vars",
            f"Únicamente {unique_count}/4 instancias únicas generadas a través de {num_dry_run_seeds} semillas.",
            f"TPL-VAR violation in '{tpl_id}': Only {unique_count}/4 unique instances generated across {num_dry_run_seeds} seeds. Parameter domain is too narrow or missing stem variations.",
            [
                "Ampliar los rangos numéricos aleatorios generados en generate_py (ej. random.choice o random.randint).",
                "Agregar 3 a 5 variantes sintácticas en 'stem_variants' para enriquecer la variabilidad textual.",
                "Evitar restringir los parámetros a un conjunto menor de 4 combinaciones posibles.",
            ]
        ))

    return errors


def check_competency_diversity(
    templates: List[Dict[str, Any]],
    competency: Union[Dict[str, Any], Any],
    distractor_map: Optional[Dict[str, Dict[str, Any]]] = None,
    num_seeds: Optional[int] = None,
    return_questions: bool = False,
) -> Union[List[str], Tuple[List[str], List[Dict[str, Any]]]]:
    """Verify stem structural diversity at the competency level (build simulation).
    
    Simulates build stage instantiation with quotas (30 for Skill, 20 for Fact/Concept)
    and evaluates masked stem diversity ratio >= 0.50.
    Returns errors_list (or (errors_list, instantiated_questions) if return_questions=True).
    """
    errors: List[str] = []
    if not templates:
        cid = competency.get("id", "UNKNOWN") if isinstance(competency, dict) else str(getattr(competency, "id", "UNKNOWN"))
        errors.append(format_diagnostic_error(
            "TPL-VAR: DIVERSIDAD DE REACTIVOS", cid, "N/A", "N/A", "templates",
            "No templates provided.",
            f"No se proporcionaron plantillas para la competencia '{cid}'.",
            [
                f"Crear y registrar archivos de plantillas para la competencia '{cid}'.",
                "Asegurar que cada competencia cuente con al menos una plantilla válida.",
                "Verificar la ruta de las plantillas en el sistema.",
            ]
        ))
        return (errors, []) if return_questions else errors

    if isinstance(competency, dict):
        cid = competency.get("id", "UNKNOWN")
        ctype = str(competency.get("type", "concept")).lower()
    else:
        cid = getattr(competency, "id", "UNKNOWN")
        ctype = str(getattr(competency, "type", getattr(competency, "category", "concept"))).lower()

    if num_seeds is not None:
        target_quota = num_seeds
    else:
        target_quota = 30 if ctype in ("skill", "hab", "habilidad") else 20

    seed_base = competency_seed_base(cid, 42)

    try:
        comp_res = instantiate_competency(
            competency=competency if isinstance(competency, dict) else None,
            competency_id=cid,
            category=ctype,
            templates=templates,
            cta_distractors_map=distractor_map,
            seed_offset_base=seed_base,
            quota=target_quota,
        )
    except Exception as e:
        errors.append(format_diagnostic_error(
            "TPL-VAR: DIVERSIDAD DE REACTIVOS", cid, "ALL", "instantiate_competency", "generate_py / vars",
            f"Fallo al instanciar cuota de diversidad ({target_quota} ítems): {e}",
            f"[-] TPL-VAR VIOLATION in competency '{cid}': Failed to instantiate diversity quota ({target_quota} items): {e}. No se pudieron generar los reactivos requeridos debido a colisiones o parámetros estrechos.",
            [
                "Ampliar los rangos de las variables aleatorias en generate_py.",
                "Agregar 3 a 5 'stem_variants' distintas con placeholders en las plantillas más estrechas.",
                "Comprobar que generate_py no lance excepciones con ciertas combinaciones de semillas.",
            ]
        ))
        return (errors, []) if return_questions else errors

    questions = comp_res.get("questions", [])

    # Annotate template_id on each question
    from engine.instantiate import allocate_template_quotas
    quotas = allocate_template_quotas(templates, target_quota)
    qid_to_tpl: Dict[str, str] = {}
    curr_idx = 1
    clean_comp = re.sub(r"[^A-Za-z0-9]", "", cid)
    for tpl in templates:
        tid = tpl.get("id", "UNKNOWN")
        cnt = quotas.get(tid, 0)
        for _ in range(cnt):
            qid = f"Q-{clean_comp}-{curr_idx:03d}"
            qid_to_tpl[qid] = tid
            curr_idx += 1

    for q in questions:
        if isinstance(q, dict) and "template_id" not in q:
            q["template_id"] = qid_to_tpl.get(q.get("id", ""), "UNKNOWN")

    # Validate invariants on all instantiated questions (Full Sweep: NO premature break)
    for q in questions:
        q_type = q.get("interaction_type") or q.get("type", "")
        q_id = q.get("id", "UNKNOWN")
        t_id = q.get("template_id", "UNKNOWN")
        is_valid, inv_errors = check_instance_invariants(q, q_type)
        if not is_valid:
            for inv_err in inv_errors:
                errors.append(format_invariant_error_diagnostic(
                    cid=cid,
                    tpl_id=t_id,
                    q_id=q_id,
                    inv_err=inv_err,
                    q_obj=q,
                ))

    div_stats = comp_res.get("diversity_stats", {})
    div_ratio = div_stats.get("diversity_ratio", 0.0)
    unique_c = div_stats.get("unique_masked", 0)
    total_c = div_stats.get("total", len(questions))

    if div_ratio < 0.5:
        pattern_counts = []
        for tpl in templates:
            t_id = tpl.get("id", "UNKNOWN")
            vars_list = tpl.get("stem_variants") or []
            if vars_list:
                p_cnt = len(set(mask_stem_numbers(v) for v in vars_list))
            else:
                p_cnt = 1
            pattern_counts.append((t_id, p_cnt))
        pattern_counts.sort(key=lambda x: x[1])

        narrowest_items = pattern_counts[:min(3, len(pattern_counts))]
        narrowest_str = ", ".join(f"{tid} ({cnt} pattern{'s' if cnt != 1 else ''})" for tid, cnt in narrowest_items)
        narrowest_tids = ", ".join(tid for tid, _ in narrowest_items)

        err_msg = format_diagnostic_error(
            rule_tag="TPL-VAR: DIVERSIDAD DE REACTIVOS",
            competency=cid,
            template=narrowest_tids,
            item_id="N/A (banco de preguntas de la competencia)",
            field_name="stem / stem_variants",
            snippet=f"stem diversity {div_ratio:.2f} < 0.50 ({unique_c}/{total_c} unique masked stems). Plantillas con menor variación: {narrowest_str}",
            cause=f"[-] TPL-VAR VIOLATION in competency '{cid}': stem diversity {div_ratio:.2f} < 0.50 ({unique_c}/{total_c} unique masked stems). Narrowest templates: {narrowest_str}. El ratio de diversidad léxico-estructural de los enunciados es menor al 50% requerido por el contrato psicométrico.",
            actions=[
                f"Agregar entre 3 y 5 'stem_variants' estructuralmente distintas en las plantillas críticas ({narrowest_tids}) usando {{placeholders}}.",
                "Ampliar los rangos numéricos y opciones aleatorias en 'vars' dentro de generate_py para evitar enunciados idénticos.",
                "Variar los verbos y formulaciones de la consigna (ej. 'Determine el valor...', 'Calcule la expresión...', 'Halle la solución...').",
            ],
        )
        errors.append(err_msg)

    return (errors, questions) if return_questions else errors


def _validate_single_template_file(
    tf: Path,
    cta_distractors_by_comp: Dict[str, Set[str]],
    cta_distractors_map: Dict[str, Dict[str, Any]],
    num_dry_run_seeds: int,
) -> Tuple[List[str], Optional[str], Set[str], List[Dict[str, Any]]]:
    """Validate a single template file and return (errors, comp_id, referenced_distractor_ids, templates_list)."""
    file_errors = []
    with open(tf, "r", encoding="utf-8") as f:
        try:
            t_content = json.load(f)
        except Exception as e:
            return [f"Failed to parse JSON in {tf}: {e}"], None, set(), []

    # Schema validation
    schema_errs = validate_template_schema(t_content)
    file_errors.extend(schema_errs)

    if isinstance(t_content, list):
        templates_list = t_content
        comp_id = t_content[0].get("competency_id") if t_content and isinstance(t_content[0], dict) else None
    elif isinstance(t_content, dict):
        comp_id = t_content.get("competency_id")
        templates_list = t_content.get("templates", [])
        if not templates_list and "interaction_type" in t_content:
            # Single template file
            templates_list = [t_content]
            comp_id = t_content.get("competency_id", comp_id)
    else:
        file_errors.append(f"File {tf.name} content must be a JSON object or list.")
        return file_errors, None, set(), []

    if cta_distractors_by_comp and (not comp_id or comp_id not in cta_distractors_by_comp):
        file_errors.append(f"File {tf.name} declares unknown or missing competency_id '{comp_id}'.")
        return file_errors, comp_id, set(), templates_list

    declared_dids = cta_distractors_by_comp.get(comp_id, set()) if cta_distractors_by_comp else set()
    referenced_dids: Set[str] = set()

    for tpl in templates_list:
        t_dids = tpl.get("distractor_ids", [])
        for did in t_dids:
            referenced_dids.add(did)

        single_errs = check_single_template(
            template=tpl,
            competency_id=comp_id or "UNKNOWN",
            declared_distractor_ids=declared_dids,
            cta_distractors_map=cta_distractors_map,
            num_dry_run_seeds=num_dry_run_seeds,
        )
        file_errors.extend(single_errs)

    return file_errors, comp_id, referenced_dids, templates_list


def check_templates_file_or_dir(
    target_path: Union[Path, List[Path], str, List[str]],
    cta_path: Optional[Path] = None,
    num_dry_run_seeds: int = 50,
    strict: bool = True,
    attempts_dir: Optional[Path] = None,
) -> Tuple[bool, List[str]]:
    """Validate all templates in file(s) or directory against CTA with production contract parity."""
    # warm_up_sandbox()  # Omit blind warmup: in-process execution is already instant
    errors = []

    cta_data: Dict[str, Any] = {}
    cta_distractors_by_comp: Dict[str, Set[str]] = {}
    cta_distractors_map: Dict[str, Dict[str, Any]] = {}

    if cta_path is not None:
        cta_p = Path(cta_path)
        if not cta_p.exists():
            return False, [f"CTA file does not exist: {cta_p}"]
        with open(cta_p, "r", encoding="utf-8") as f:
            cta_data = json.load(f)

        for comp in cta_data.get("competencies", []):
            cid = comp["id"]
            d_ids = set()
            for d in comp.get("distractors", []):
                did = d["id"]
                d_ids.add(did)
                cta_distractors_map[did] = d
            cta_distractors_by_comp[cid] = d_ids
    else:
        print("[!] Warning: cta_path omitted; competency diversity gate (TPL-VAR), parity checks, and distractor checks skipped.")

    # Collect template files
    template_files: List[Path] = []
    is_full_dir = False

    raw_targets = target_path if isinstance(target_path, (list, tuple)) else [target_path]
    for item in raw_targets:
        str_item = str(item)
        if "*" in str_item or "?" in str_item:
            p_obj = Path(str_item)
            parent = p_obj.parent if str(p_obj.parent) != "" else Path(".")
            pattern = p_obj.name
            matched = list(parent.glob(pattern))
            for m in matched:
                if m.is_file() and m.suffix.lower() == ".json" and m not in template_files:
                    template_files.append(m)
            continue

        p = Path(item)
        if p.is_file() and p.suffix.lower() == ".json":
            # Check if this file is a shard file (e.g. shard_XX.json)
            is_shard = False
            try:
                content = json.loads(p.read_text(encoding="utf-8"))
                if isinstance(content, dict) and ("shard_id" in content or "competency_ids" in content):
                    is_shard = True
                    c_ids = content.get("competency_ids", [])
                    for cid in c_ids:
                        candidate_paths = [
                            p.parent.parent / "templates" / f"{cid}.json",
                            p.parent / "templates" / f"{cid}.json",
                            Path("work/templates") / f"{cid}.json",
                            Path("templates") / f"{cid}.json",
                        ]
                        found_tpl = None
                        for cand in candidate_paths:
                            if cand.is_file():
                                found_tpl = cand
                                break
                        if found_tpl:
                            if found_tpl not in template_files:
                                template_files.append(found_tpl)
                        else:
                            errors.append(f"Shard '{p.name}' references competency '{cid}', but template file was not found at work/templates/{cid}.json")
            except Exception:
                is_shard = False

            if not is_shard and p not in template_files:
                template_files.append(p)
        elif p.is_dir():
            is_full_dir = True
            for f in sorted(p.glob("*.json")):
                if f not in template_files:
                    template_files.append(f)
        elif not p.exists():
            return False, [f"Target path does not exist: {p}"]

    if not template_files and not errors:
        return False, [f"No template JSON files found in: {target_path}"]

    referenced_distractors_by_comp: Dict[str, Set[str]] = {cid: set() for cid in cta_distractors_by_comp}
    templates_by_comp: Dict[str, List[Dict[str, Any]]] = {}
    processed_comp_ids: Set[str] = set()

    if len(template_files) > 1:
        max_workers = min(16, (os.cpu_count() or 4) * 2, len(template_files))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {
                executor.submit(
                    _validate_single_template_file,
                    tf,
                    cta_distractors_by_comp,
                    cta_distractors_map,
                    num_dry_run_seeds,
                ): tf
                for tf in template_files
            }
            for future in future_to_file:
                file_errs, comp_id, ref_dids, tpls = future.result()
                errors.extend(file_errs)
                if comp_id:
                    processed_comp_ids.add(comp_id)
                    templates_by_comp.setdefault(comp_id, []).extend(tpls)
                    if comp_id in referenced_distractors_by_comp:
                        referenced_distractors_by_comp[comp_id].update(ref_dids)
    else:
        for tf in template_files:
            file_errs, comp_id, ref_dids, tpls = _validate_single_template_file(
                tf,
                cta_distractors_by_comp,
                cta_distractors_map,
                num_dry_run_seeds,
            )
            errors.extend(file_errs)
            if comp_id:
                processed_comp_ids.add(comp_id)
                templates_by_comp.setdefault(comp_id, []).extend(tpls)
                if comp_id in referenced_distractors_by_comp:
                    referenced_distractors_by_comp[comp_id].update(ref_dids)

    # Rule TPL-D3: 100% distractor coverage across templates
    if cta_distractors_by_comp:
        comps_to_check = list(referenced_distractors_by_comp.keys()) if is_full_dir else list(processed_comp_ids)
        for cid in comps_to_check:
            declared_set = cta_distractors_by_comp.get(cid, set())
            referenced_set = referenced_distractors_by_comp.get(cid, set())
            uncovered = declared_set - referenced_set
            if uncovered:
                errors.append(format_diagnostic_error(
                    rule_tag="TPL-D3: COBERTURA COMPLETA DE DISTRACTORES",
                    competency=cid,
                    template="[Todas las plantillas de la competencia]",
                    item_id="N/A",
                    field_name="distractor_ids",
                    snippet=f"Distractores sin cubrir: {sorted(uncovered)} ({len(uncovered)}/{len(declared_set)})",
                    cause="Existen distractores definidos en cta.json que ninguna plantilla de la competencia está utilizando.",
                    actions=[
                        f"Asignar los distractores sin cubrir ({sorted(uncovered)}) en las plantillas existentes de '{cid}'.",
                        "O crear plantillas adicionales que ejerciten los conceptos erróneos representados por estos distractores.",
                        "Asegurar que el 100% de los distractores de cta.json tengan al menos una plantilla que los emplee.",
                    ],
                ))

    # Rule TPL-VAR (Competency Diversity Gate) & Isomorphic Contract Parity Check
    if cta_data and "competencies" in cta_data:
        comp_map = {c["id"]: c for c in cta_data.get("competencies", [])}
        comps_to_check = list(referenced_distractors_by_comp.keys()) if is_full_dir else list(processed_comp_ids)
        def _evaluate_comp_diversity_and_parity(cid: str) -> List[str]:
            c_errors: List[str] = []
            comp_obj = comp_map.get(cid)
            comp_tpls = templates_by_comp.get(cid, [])
            if not (comp_obj and comp_tpls):
                return c_errors
            sim_seeds = num_dry_run_seeds if num_dry_run_seeds < 20 else None
            div_errors, comp_questions = check_competency_diversity(
                templates=comp_tpls,
                competency=comp_obj,
                distractor_map=cta_distractors_map,
                num_seeds=sim_seeds,
                return_questions=True,
            )
            c_errors.extend(div_errors)

            if strict and comp_questions:
                parity_errors = check_production_parity_for_competency(
                    cid=cid,
                    competency=comp_obj,
                    questions=comp_questions,
                    strict=True,
                )
                c_errors.extend(parity_errors)
            return c_errors

        sorted_comps = sorted(comps_to_check)
        if len(sorted_comps) > 1:
            max_workers = min(16, (os.cpu_count() or 4) * 2, len(sorted_comps))
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                comp_futures = [executor.submit(_evaluate_comp_diversity_and_parity, cid) for cid in sorted_comps]
                for fut in comp_futures:
                    errors.extend(fut.result())
        else:
            for cid in sorted_comps:
                errors.extend(_evaluate_comp_diversity_and_parity(cid))

    is_clean = (len(errors) == 0)

    # Auto-repair attempt tracking if attempts_dir is supplied
    if attempts_dir is not None:
        try:
            att_path = Path(attempts_dir)
            att_path.mkdir(parents=True, exist_ok=True)
            for cid in processed_comp_ids:
                f_att = att_path / f"{cid}.json"
                cur_att = 0
                if f_att.is_file():
                    try:
                        cur_att = json.loads(f_att.read_text(encoding="utf-8")).get("attempts", 0)
                    except Exception:
                        pass
                if not is_clean:
                    cur_att += 1
                    f_att.write_text(json.dumps({"attempts": cur_att}), encoding="utf-8")
                    if cur_att >= 4:
                        errors.append(
                            f"[!] BUDGET HALT on competency '{cid}': Exceeded {cur_att} validation cycles. "
                            f"Action required: Cease iteration and report: BLOCKED: {cid} - validation failure limit reached."
                        )
                else:
                    # Clear on success
                    if f_att.is_file():
                        f_att.unlink()
        except Exception:
            pass

    return is_clean, errors


def main():
    parser = argparse.ArgumentParser(description="Validate parametric exercise templates with Isomorphic Contract Parity")
    parser.add_argument("target", nargs="+", help="Path(s) to template.json file(s) or templates/ directory")
    parser.add_argument("--cta", default=None, help="Path to cta.json file")
    parser.add_argument("--seeds", type=int, default=50, help="Number of dry-run seeds (default 50)")
    parser.add_argument("--strict", action="store_true", default=True, help="Enforce production contract parity (default: true)")
    parser.add_argument("--no-strict", dest="strict", action="store_false", help="Bypass production parity checks")
    parser.add_argument("--attempts-dir", default=None, help="Directory to track per-competency validation cycles")
    parser.add_argument("--json-report", default=None, help="Optional output path for structured JSON diagnostic report")
    args = parser.parse_args()

    cta_p = Path(args.cta) if args.cta else None
    targets = [Path(t) for t in args.target]
    valid, errors = check_templates_file_or_dir(
        targets,
        cta_p,
        num_dry_run_seeds=args.seeds,
        strict=args.strict,
        attempts_dir=Path(args.attempts_dir) if args.attempts_dir else None,
    )

    if args.json_report:
        report_data = {
            "valid": valid,
            "errors_count": len(errors),
            "errors": errors,
            "targets": [str(t) for t in targets],
        }
        try:
            r_path = Path(args.json_report)
            r_path.parent.mkdir(parents=True, exist_ok=True)
            r_path.write_text(json.dumps(report_data, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as ex:
            print(f"[!] Warning: Could not write json report: {ex}", file=sys.stderr)

    if not valid:
        print(f"FAIL: {len(errors)} validation errors in templates:")
        for e in errors[:15]:
            print(f"  - {e}")
        if len(errors) > 15:
            print(f"  ... and {len(errors) - 15} more errors.")
        sys.exit(1)

    print(f"PASS: All templates satisfy schema, AST security, {args.seeds} seeds dry run, invariants, TPL-D1..D4 rules, and Production Parity.")
    sys.exit(0)


if __name__ == "__main__":
    main()

