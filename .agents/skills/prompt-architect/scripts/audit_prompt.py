#!/usr/bin/env python3
"""
audit_prompt.py - Pre-scan determinista basado estrictamente en fuentes oficiales (actualizado Nov 2026).

Cada regla implementada aquí DEBE contar con una cita directa y verificable de:
  - prompting-strategies.md (Google DeepMind / AI Studio)
  - whats-new-gemini-4-hydrogen.md / whats-new-gemini-3.6.md / thinking.md / caching.md / function-calling.md
  - prompt_masterprompter.md (Ultimate Prompt Architect)

Cualquier regla que no provenga de estas fuentes queda prohibida en el análisis de calidad.
Las convenciones de infraestructura de Top's Academy (DONE:, turnos, scope-lock)
se relegan a un chequeo auxiliar opcional (--pipeline-check) y NO alteran los hallazgos de prompt engineering.
"""

import sys
import os
import re
import json
import argparse
from typing import Dict, List, Any, Optional

# Catálogo canónico de reglas con citas directas de las fuentes originales
CITATIONS = {
    "R_ANTI_PATTERN": "prompting-strategies.md § 'Patterns vs anti patterns' & masterprompter Principle 6",
    "R_DEPRECATED_SAMPLING": "prompting-strategies.md § 'Experiment with model parameters' (l. 513-520), whats-new-gemini-4-hydrogen.md l. 385 & masterprompter Principle 4",
    "R_PREFILLED_TURN_OR_INVALID_API": "whats-new-gemini-3.6.md § 'Prefilled model turn validation' (l. 171, 193), thinking.md l. 704 & caching.md l. 13-16",
    "R_PRE_TOOL_STRUCTURED_TEXT": "function-calling.md § 'Workarounds for pre-tool text requirements' (l. 3740-3800) & whats-new-gemini-4-hydrogen.md l. 386",
    "R_CONTEXT_ORDER": "prompting-strategies.md § 'Core prompting principles - Structure for long contexts' (l. 707-714) & masterprompter Principle 3",
    "R_SHOUTING": "prompting-strategies.md § 'Core prompting principles - Be precise and direct' (l. 685-686) & masterprompter Principle 1",
    "R_INPUT_ISOLATION": "prompting-strategies.md § 'Structured prompting examples' (l. 783-785) & prompt_masterprompter.md Stage 3 / Principle 2",
    "R_AGENTIC_RISK": "prompting-strategies.md § 'Agentic workflows - Risk Assessment' (l. 879, 912-913) & masterprompter lines 106-107",
    "R_FEW_SHOT_MISSING": "prompting-strategies.md § 'Zero-shot vs few-shot prompts' (l. 296-299) & masterprompter Principle 6",
    "R_FEW_SHOT_COUNT": "prompting-strategies.md § 'Optimal number of examples' (l. 371-377) & prompt_masterprompter.md Principle 6",
    "R_STRUCTURE_DELIMITERS": "prompting-strategies.md § 'Core prompting principles - Use consistent structure' (l. 688-691) & masterprompter Principle 2",
    "R_SEMANTIC_VERBOSITY": "prompting-strategies.md § 'Core prompting principles - Control output verbosity' (l. 695-697, 827) & masterprompter Principle 4",
    "R_TEMPORAL_ANCHOR": "prompting-strategies.md § 'Gemini 3 Flash strategies - Current day accuracy' (l. 718-726) & masterprompter Principle 7",
    "R_STRICT_GROUNDING": "prompting-strategies.md § 'Gemini 3 Flash strategies - Grounding performance' (l. 735-751) & AI Engineering (Chip Huyen) Ch. 4 § 'Factual consistency - Textual entailment'",
    "R_RAG_NEGATIVE_EXAMPLE": "AI Engineering (Chip Huyen) Ch. 4 § 'Factual consistency' & Ch. 5 § 'How to Restrict a Model's Knowledge to Only Its Context'",
    "R_JUDGE_BIAS_AND_SCALE": "AI Engineering (Chip Huyen) Ch. 3 § 'How to Use AI as a Judge' & 'Biases of AI as a judge' (Verbosity bias, discrete scoring)",
    "R_NATIVE_THINKING": "prompting-strategies.md § 'Enhancing reasoning and planning' (l. 754-764) & masterprompter Principle 5"
}

# Líneas prohibitivas para evitar falsos positivos
NEGATION_LINE = re.compile(r"(🚫|\bnever\b|\bnunca\b|\bprohibid|\bprohibited\b|\bno\s+uses?\b|\bdo\s+not\b|\bdon't\b|\bevitar?\b|\bavoid\b)", re.I)


def _positive_lines(text: str) -> str:
    return "\n".join(l for l in text.splitlines() if not NEGATION_LINE.search(l))


class PromptAuditor:
    def __init__(self, content: str, filepath: str = ""):
        self.raw_content = content
        self.filepath = filepath
        self.flaws: List[Dict[str, Any]] = []
        self.strengths: List[Dict[str, Any]] = []
        self.recommendations: List[str] = []

    def flaw(self, rule_id: str, severity: str, category: str, message: str, evidence: str, recommendation: str):
        self.flaws.append({
            "rule_id": rule_id,
            "severity": severity,
            "category": category,
            "message": message,
            "evidence": evidence,
            "citation": CITATIONS.get(rule_id, "Fuente oficial")
        })
        self.recommendations.append(recommendation)

    def strength(self, rule_id: str, category: str, message: str, evidence: str):
        self.strengths.append({
            "rule_id": rule_id,
            "category": category,
            "message": message,
            "evidence": evidence,
            "citation": CITATIONS.get(rule_id, "Fuente oficial")
        })

    def audit(self) -> Dict[str, Any]:
        text = self.raw_content
        pos_lines = _positive_lines(text)

        # 1. Ejemplos negativos (Anti-patterns)
        anti_matches = re.findall(
            r"(\b(?:don't\s+do|anti-pattern|ejemplo\s+incorrecto|bad\s+example|incorrect\s+output|lo\s+que\s+no\s+debes|example of what not)\b[^\n]*)",
            text, re.I
        )
        if anti_matches:
            self.flaw(
                "R_ANTI_PATTERN", "Alta", "Ejemplos Few-Shot",
                "Se detectó la inclusión de ejemplos negativos o anti-patrones. Los LLMs tienden a reproducir los patrones mostrados en ejemplos negativos.",
                anti_matches[0][:100],
                "Eliminar ejemplos negativos. Mostrar exclusivamente patrones positivos a seguir y expresar prohibiciones como directivas afirmativas en restricciones."
            )

        # 2. Parámetros de sampling deprecados
        deprecated_matches = re.findall(r"(\b(?:temperature|top_p|top_k|topP|topK|candidate_count|thinking_budget)\s*[:=]\s*[0-9.]+\b)", text, re.I)
        # Excluir menciones en advertencias documentales
        if deprecated_matches and not re.search(r"(deprecated|deprecad|ignore|no\s+usar|do\s+not\s+set|remove)", text, re.I):
            self.flaw(
                "R_DEPRECATED_SAMPLING", "Alta", "Parámetros de Inferencia",
                f"Configuración explícita de parámetros deprecados ({', '.join(deprecated_matches)}). Gemini 3.6+, 3.8 Flash y Gemini 4 ignoran estos valores o emiten error 400.",
                deprecated_matches[0],
                "Eliminar temperature, top_p, top_k, candidate_count y thinking_budget. Controlar determinismo y extensión en <constraints> y usar thinking_level."
            )
        else:
            self.strength("R_DEPRECATED_SAMPLING", "Parámetros de Inferencia", "Libre de parámetros de sampling obsoletos.", "Sin asignaciones de temperature/top_p/top_k.")

        # 2b. Prefilled model turns, thinking_level: minimal en Gemini 4/3.8 o cached_content / cache_control en Gemini 4
        prefill_match = re.findall(r"(\"role\"\s*:\s*\"model\"[^\n}]*\}\s*\]|prefill(?:ed)?\s+model\s+turn|thinking_level\s*[:=]\s*[\"']?minimal[\"']?|cached_content\s*[:=]\s*[\"'][^\"']+[\"']|caches\.create|cache_control\s*[:=]\s*\{)", pos_lines, re.I)
        if prefill_match:
            self.flaw(
                "R_PREFILLED_TURN_OR_INVALID_API", "Alta", "Parámetros y API Frontier",
                "Uso de configuración inválida en Gemini 3.6+/3.8/4 (turno 'model' pre-llenado, thinking_level='minimal' en Gemini 4/3.8, o cached_content/cache_control explícito en Gemini 4). Provoca error HTTP 400.",
                prefill_match[0][:100],
                "Eliminar turnos 'model' pre-llenados (usar system_instruction o response_format), usar thinking_level válido (low/medium/high/xhigh) y emplear Implicit Caching (con prefijo libre de variables volátiles) en lugar de cached_content o cache_control."
            )

        # 2c. Pre-tool structured XML/JSON text (Malformed_Function_Call)
        pre_tool_match = re.findall(
            r"((?:before\s+calling\s+(?:a|any)\s+tool|antes\s+de\s+llamar\s+a\s+(?:una|cualquier)\s+herramienta)[^\n.]{0,120}(?:output|emitir|imprimir|escribe)[^\n.]{0,80}<(?:UPDATE|PLAN|STATUS)[> ])",
            pos_lines, re.I
        )
        if pre_tool_match:
            self.flaw(
                "R_PRE_TOOL_STRUCTURED_TEXT", "Alta", "Control Agentico / Tools",
                "Exige emitir un bloque XML/estructurado (<UPDATE>) en texto plano inmediatamente antes de llamar a una herramienta, lo que ocasiona errores Malformed_Function_Call.",
                pre_tool_match[0][:100],
                "Encapsular las notas previas en una función dedicada update(previous_step, plan, next_step, external) o usar encabezados Markdown (# UPDATE) en lugar de XML antes de tool calls."
            )

        # 3. Delimitadores estructurales consistentes
        xml_tags = set(re.findall(r"<([a-z_]{3,30})>", text))
        md_headers = re.findall(r"^#{1,4}\s+\S", text, re.M)
        if len(xml_tags) >= 3:
            self.strength("R_STRUCTURE_DELIMITERS", "Estructura", f"Uso de delimitadores XML consistentes ({len(xml_tags)} etiquetas clave).", f"<{list(xml_tags)[:4]}>")
        elif len(md_headers) >= 3:
            self.strength("R_STRUCTURE_DELIMITERS", "Estructura", f"Organización mediante encabezados jerárquicos Markdown ({len(md_headers)} encabezados).", "Encabezados ## detectados.")
        else:
            self.flaw(
                "R_STRUCTURE_DELIMITERS", "Alta", "Estructura",
                "Carece de delimitadores estructurales claros (XML o Markdown jerárquico). Las instrucciones y datos se mezclan en texto plano.",
                text[:120].replace("\n", " "),
                "Separar formalmente el prompt en secciones estructurales delimitadas (<role>, <instructions>, <constraints>, <output_format>)."
            )

        # 4. Énfasis persuasivo / gritos mayúsculos
        shouting = re.findall(r"(\b(?:CRITICAL|URGENT|SUPER IMPORTANT|EXTREMELY IMPORTANT|VERY IMPORTANT|MUY IMPORTANTE|IMPORTANT[EÍ]SIMO|DO NOT EVER|PLEASE BE CAREFUL|I BEG YOU|POR FAVOR TE LO PIDO)\b|!{2,})", text, re.I)
        caps_runs = re.findall(r"(\b[A-ZÁÉÍÓÚÑ]{2,}(?:\s+[A-ZÁÉÍÓÚÑ]{2,}){2,}\b)", _strip_markdown_and_code(text))
        if shouting or caps_runs:
            ev = (shouting[0] if shouting else caps_runs[0])[:80]
            self.flaw(
                "R_SHOUTING", "Media", "Claridad y Tono",
                "Uso de mayúsculas sostenidas o lenguaje persuasivo/emocional. Los modelos modernos responden a directivas técnicas directas, no a volumen.",
                ev,
                "Sustituir súplicas emocionales y mayúsculas sostenidas por especificaciones técnicas afirmativas."
            )
        else:
            self.strength("R_SHOUTING", "Claridad y Tono", "Tono técnico, directo y sin súplicas emocionales ni mayúsculas invasivas.", "Limpio de lenguaje persuasivo.")

        # 5. Control semántico de verbosidad
        if re.search(r"\bverbosity\s*[:=]\s*\[?\s*(?:low|medium|high)\b", text, re.I):
            self.strength("R_SEMANTIC_VERBOSITY", "Claridad y Tono", "Nivel de verbosidad semántica explícitamente parametrizado.", "Verbosity: Low/Medium/High")
        else:
            self.flaw(
                "R_SEMANTIC_VERBOSITY", "Media", "Claridad y Tono",
                "No se especifica el nivel de verbosidad semántica. Gemini 3+ y Gemini 4 asumen respuestas directas por defecto; si se requiere otra extensión, debe parametrizarse.",
                "Sin declaración de Verbosity en restricciones.",
                "Declarar explícitamente el nivel en <constraints> (ej. 'Verbosity: Low' para respuestas telegráficas o 'Medium' para balanceadas)."
            )

        # 6. Aislamiento de entradas (Prompt Injection Defense)
        has_input_tag = bool(re.search(r"<(context|input_data|user_input|payload)>", text, re.I))
        data_defense_rule = bool(re.search(r"(strictly as data|estrictamente como datos|como datos[,; ]|never as (new )?instructions|nunca como (nuevas )?instrucciones)", text, re.I))
        if has_input_tag and data_defense_rule:
            self.strength("R_INPUT_ISOLATION", "Seguridad e Inyección", "Entradas del usuario aisladas en etiquetas de datos y blindadas contra inyección.", "Etiquetas de datos + regla de datos inertes.")
        elif not has_input_tag and re.search(r"\{[a-z_]+\}|\[insert|\[insertar|input del usuario", text, re.I):
            self.flaw(
                "R_INPUT_ISOLATION", "Alta", "Seguridad e Inyección",
                "Entrada externa interpolada sin etiquetas de datos ni declaración de datos inertes. Vulnerable a sobrescritura de instrucciones (Prompt Injection).",
                "Entrada no delimitada detectada.",
                "Envolver toda entrada no confiable en etiquetas <context> o <input_data> e instruir que su contenido es dato inerte, nunca directiva ejecutable."
            )

        # 7. Arquitectura de Contexto Largo (Context First, Task Last)
        m_ctx = re.search(r"<context>|^#{1,3}\s*(context|contexto)\b", text, re.I | re.M)
        m_task = re.search(r"<task>|^#{1,3}\s*(task|tarea)\b", text, re.I | re.M)
        if m_ctx and m_task:
            if m_task.start() < m_ctx.start():
                self.flaw(
                    "R_CONTEXT_ORDER", "Alta", "Arquitectura de Contexto",
                    "Inversión de Contexto: la tarea (<task>) se colocó ANTES del bloque de contexto (<context>). Disminuye la atención del modelo y rompe el prefijo de Implicit Caching.",
                    "<task> precede a <context>",
                    "Colocar todo el contexto de referencia primero y la tarea al final absoluto, precedida por una frase de anclaje."
                )
            else:
                self.strength("R_CONTEXT_ORDER", "Arquitectura de Contexto", "Estructura Long-Context óptima: contexto suministrado primero, tarea al final.", "<context> precede a <task>")

        # 8. Cláusula de Grounding Estricto (para prompts con contexto) y Negative Knowledge en Few-Shot
        if m_ctx:
            has_strict_grounding = bool(re.search(r"(strict(ly)?\s+grounded|l[ií]mite absoluto de la verdad|untruthful|cero alucinaciones|informaci[oó]n (?:solicitada )?no se encuentra disponible)", text, re.I))
            if has_strict_grounding:
                self.strength("R_STRICT_GROUNDING", "Grounding y Veracidad", "Cláusula de Grounding Estricto (Zero-Hallucination / NLI) implementada.", "Contrato de veracidad estricta presente.")
                examples_section = "".join(re.findall(r"<examples>(.*?)</examples>", text, re.S | re.I))
                if examples_section:
                    if re.search(r"(no se encuentra disponible|not available|no disponible|insufficient|sin evidencia|ninguno)", examples_section, re.I):
                        self.strength("R_RAG_NEGATIVE_EXAMPLE", "Grounding y Veracidad", "Ejemplos few-shot incluyen caso de rechazo / Negative Knowledge (estado Neutral).", "Ejemplo de dato ausente en <examples>.")
                    else:
                        self.flaw(
                            "R_RAG_NEGATIVE_EXAMPLE", "Media", "Grounding y Veracidad",
                            "Prompt RAG con grounding estricto cuyos ejemplos few-shot no incluyen ningún caso de rechazo (Negative Knowledge / estado Neutral cuando el dato no figura en el contexto).",
                            "Ejemplos solo muestran casos con respuesta presente.",
                            "Añadir al menos 1 ejemplo few-shot donde la información consultada no exista en el <context> y la salida declare su indisponibilidad."
                        )
            else:
                self.flaw(
                    "R_STRICT_GROUNDING", "Media", "Grounding y Veracidad",
                    "Prompt con contexto de referencia sin cláusula de grounding estricto. Riesgo de extrapolaciones y alucinaciones fuera de las fuentes.",
                    "Bloque de contexto sin grounding_contract.",
                    "Añadir cláusula declarando que el contexto es el límite absoluto de la verdad y exigir declarar indisponibilidad si el dato no aparece."
                )

        # 8b. Jueces LLM (AI as a Judge): Escala discreta y mitigación de Verbosity Bias
        role_section = "".join(re.findall(r"<role>(.*?)</role>", text, re.S | re.I))
        is_judge = bool(re.search(r"<scoring_rubric>", text, re.I)) or bool(re.search(r"\b(juez|judge|[aá]rbitro|evaluador de respuestas)\b", role_section, re.I))
        if is_judge:
            has_anti_verbosity_bias = bool(re.search(r"(verbosity\s+bias|sesgo\s+de\s+verbosidad|no\s+premies?\s+la\s+longitud|do\s+not\s+reward\s+length|concisa\s+y\s+exacta)", text, re.I))
            has_discrete_rubric = bool(re.search(r"(<scoring_rubric>|escala\s+discreta|PASS\s*\|\s*NEEDS_REPAIR|1\s+to\s+5|1\s+a\s+5)", text, re.I))
            if has_anti_verbosity_bias and has_discrete_rubric:
                self.strength("R_JUDGE_BIAS_AND_SCALE", "Evaluación / AI as a Judge", "Prompt de Juez calibrado con rúbrica discreta y cláusula explícita contra sesgo de verbosidad.", "Rúbrica discreta + anti-verbosity bias.")
            else:
                self.flaw(
                    "R_JUDGE_BIAS_AND_SCALE", "Media", "Evaluación / AI as a Judge",
                    "Prompt de Juez LLM (AI as a Judge) sin mitigación explícita contra el sesgo de verbosidad (Verbosity Bias) o sin escala discreta definida.",
                    "Juez sin cláusula anti-verbosity bias o escala discreta.",
                    "Definir una rúbrica discreta corta (<scoring_rubric>) e instruir explícitamente no premiar longitud ni extensión superficial sobre exactitud factual."
                )

        # 9. Anclaje temporal para herramientas de búsqueda
        uses_search = bool(re.search(r"\b(search_web|google search|b[uú]squeda web|web search)\b", pos_lines, re.I))
        if uses_search:
            if re.search(r"2026", text):
                self.strength("R_TEMPORAL_ANCHOR", "Grounding y Veracidad", "Anclaje temporal 2026 explícito para consultas en herramientas de búsqueda.", "Año 2026 presente.")
            else:
                self.flaw(
                    "R_TEMPORAL_ANCHOR", "Media", "Grounding y Veracidad",
                    "El prompt utiliza herramientas de búsqueda web sin anclar el año en curso (2026). Provoca búsquedas temporales anacrónicas.",
                    "Uso de búsqueda sin ancla de año 2026.",
                    "Instruir explícitamente al modelo a formular búsquedas teniendo en cuenta que el año en curso es 2026."
                )

        # 10. Ejemplos Few-Shot (Presencia y Cantidad)
        example_blocks = len(re.findall(r"<example>", text))
        if example_blocks == 0:
            example_blocks = len(re.findall(r"^\s*(?:\*\*)?(?:ejemplo|example)\s*\d*\s*[:(]", text, re.I | re.M))

        if example_blocks == 0:
            self.flaw(
                "R_FEW_SHOT_MISSING", "Media", "Ejemplos Few-Shot",
                "Ausencia de ejemplos few-shot. La documentación oficial recomienda incluir siempre ejemplos; prompts zero-shot son significativamente menos consistentes.",
                "0 ejemplos detectados.",
                "Incorporar de 2 a 4 ejemplos de alta representatividad demostrando el patrón exacto deseado."
            )
        elif 2 <= example_blocks <= 4:
            self.strength("R_FEW_SHOT_COUNT", "Ejemplos Few-Shot", f"Cantidad óptima de ejemplos few-shot ({example_blocks} ejemplos balanceados).", f"{example_blocks} ejemplos.")
        elif example_blocks == 1:
            self.flaw(
                "R_FEW_SHOT_COUNT", "Baja", "Ejemplos Few-Shot",
                "Solo 1 ejemplo provisto. Riesgo de que el modelo sobreajuste al único caso mostrado.",
                "1 ejemplo detectado.",
                "Añadir al menos un segundo ejemplo que varíe en complejidad o casos de borde."
            )
        elif example_blocks > 4:
            self.flaw(
                "R_FEW_SHOT_COUNT", "Baja", "Ejemplos Few-Shot",
                f"Exceso de ejemplos ({example_blocks} detectados). Riesgo de overfitting sintáctico e incremento innecesario de tokens.",
                f"{example_blocks} ejemplos.",
                "Reducir a 2-4 ejemplos de alto valor sintáctico y representatividad."
            )

        # 11. Agentes: Matriz de Riesgo Read vs Write
        is_agent = bool(re.search(r"\b(agent|subagent|agente|subagente|tool|herramienta)\b", text, re.I))
        writes_tools = bool(re.search(r"\b(write_file|edit_file|delete|borrar|eliminar|modificar|mutaci[oó]n)\b", pos_lines, re.I))
        if is_agent and writes_tools:
            has_risk_matrix = bool(re.search(r"(read\s*(?:vs\.?|/|y)\s*write|bajo\s*riesgo|alto\s*riesgo|low[- ]risk|high[- ]risk|confirmaci[oó]n\s*previa|lecturas\s+dentro\s+del\s+scope)", text, re.I))
            if has_risk_matrix:
                self.strength("R_AGENTIC_RISK", "Control Agentico", "Matriz de evaluación de riesgo implementada (diferenciación explícita entre lectura y escritura).", "Distingue lectura de mutaciones.")
            else:
                self.flaw(
                    "R_AGENTIC_RISK", "Alta", "Control Agentico",
                    "Agente con herramientas de escritura/mutación sin matriz de riesgo Read vs Write. Permite mutaciones de estado sin validación ni confirmación.",
                    "Llamadas de mutación sin protocolo de riesgo.",
                    "Configurar la regla de riesgo: lecturas se ejecutan con datos disponibles; escrituras exigen confirmación o verificación exhaustiva de parámetros."
                )

        # 12. Razonamiento nativo vs CoT visible
        if re.search(r"(<thinking>|show your reasoning|muestra tu razonamiento paso a paso en la respuesta)", text, re.I) and not re.search(r"audit trail|traza de auditor", text, re.I):
            self.flaw(
                "R_NATIVE_THINKING", "Baja", "Eficiencia y Razonamiento",
                "Fuerza bloques de razonamiento visible innecesarios en la salida del usuario. Gemini 2.5/3+/4 generan tokens de pensamiento nativos internamente.",
                "CoT visible exigido.",
                "Eliminar exigencia de imprimir el razonamiento visible; utilizar <final_instruction> o thinking_level para elevar la profundidad de pensamiento nativo."
            )

        high_flaws = sum(1 for f in self.flaws if f["severity"] == "Alta")
        med_flaws = sum(1 for f in self.flaws if f["severity"] == "Media")

        if high_flaws >= 2:
            verdict = "Crítico (Múltiples riesgos de fallo o alucinación)"
        elif high_flaws == 1 or med_flaws >= 3:
            verdict = "Requiere Refactorización (Anti-patrones presentes)"
        elif med_flaws >= 1:
            verdict = "Aceptable con Observaciones"
        else:
            verdict = "Conforme con Estándares Frontier"

        return {
            "filepath": self.filepath,
            "verdict": verdict,
            "flaws_count": {
                "alta": high_flaws,
                "media": med_flaws,
                "baja": sum(1 for f in self.flaws if f["severity"] == "Baja")
            },
            "strengths": self.strengths,
            "flaws": self.flaws,
            "recommendations": list(dict.fromkeys(self.recommendations))
        }


def _strip_markdown_and_code(t: str) -> str:
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    t = re.sub(r"`[^`]*`", "", t)
    return "\n".join(l for l in t.splitlines() if not l.lstrip().startswith("#"))


def run_pipeline_check(text: str) -> Dict[str, Any]:
    """Chequeo auxiliar de convenciones internas del pipeline C2C de Top's Academy. NO altera la calidad del prompt."""
    checks = []
    has_scope = bool(re.search(r"scope[-_ ]lock|READ\s+permit|WRITE\s+permit", text, re.I))
    has_done = bool(re.search(r"DONE:\s*<", text))
    has_blocked = bool(re.search(r"BLOCKED:", text))
    has_turns = bool(re.search(r"turno|turn budget|presupuesto de turnos", text, re.I))

    checks.append({"item": "Scope-Lock con rutas acotadas", "passed": has_scope})
    checks.append({"item": "Señal de cierre estandarizada DONE:", "passed": has_done})
    checks.append({"item": "Vía de escape estandarizada BLOCKED:", "passed": has_blocked})
    checks.append({"item": "Contrato / Presupuesto de turnos", "passed": has_turns})

    return {
        "pipeline": "Top's Academy Content-to-Course",
        "checks": checks
    }


def format_markdown_report(res: Dict[str, Any], pipeline_info: Optional[Dict[str, Any]] = None) -> str:
    md = []
    title = os.path.basename(res["filepath"]) if res["filepath"] else "Prompt"
    md.append(f"# Auditoría Factual de Prompt: `{title}`\n")
    if res["filepath"]:
        md.append(f"**Archivo:** `{res['filepath']}`  ")
    md.append(f"**Veredicto de Calidad:** **{res['verdict']}**  ")
    fc = res["flaws_count"]
    md.append(f"**Hallazgos:** 🔴 Alta: `{fc['alta']}` | 🟡 Media: `{fc['media']}` | ⚪ Baja: `{fc['baja']}`\n")

    md.append("## 1. ¿Qué Hace Bien el Prompt? (Fortalezas con Evidencia Factual)\n")
    if res["strengths"]:
        for s in res["strengths"]:
            md.append(f"- ✅ **[{s['category']}]:** {s['message']}")
            md.append(f"  - *Evidencia:* `{s['evidence']}`")
            md.append(f"  - *Cita Fuente:* `{s['citation']}`")
    else:
        md.append("- *No se identificaron fortalezas arquitectónicas destacables.*")

    md.append("\n## 2. ¿Qué Hace Mal o Riesgos Detectados? (Vulnerabilidades y Deficiencias)\n")
    if res["flaws"]:
        for f in res["flaws"]:
            icon = "🔴" if f["severity"] == "Alta" else ("🟡" if f["severity"] == "Media" else "⚪")
            md.append(f"- {icon} **[{f['category']} · Severidad {f['severity']}]:** {f['message']}")
            md.append(f"  - *Evidencia detectada:* `{f['evidence']}`")
            md.append(f"  - *Cita Fuente:* `{f['citation']}`")
    else:
        md.append("- ✅ *Sin hallazgos de vulnerabilidad ni anti-patrones en el pre-scan.*")

    md.append("\n## 3. Recomendaciones de Optimización de Alto Impacto\n")
    if res["recommendations"]:
        for i, r in enumerate(dict.fromkeys(res["recommendations"]), 1):
            md.append(f"{i}. 🎯 {r}")
    else:
        md.append("- *El prompt cumple con las directrices de los documentos oficiales.*")

    if pipeline_info:
        md.append("\n---\n### Apéndice Auxiliar: Conformidad con Pipeline C2C (Informativo, no altera calidad)")
        for c in pipeline_info["checks"]:
            st = "✅" if c["passed"] else "⚠️"
            md.append(f"- {st} {c['item']}")

    return "\n".join(md)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    parser = argparse.ArgumentParser(description="Audita prompts basándose estrictamente en guías oficiales citadas.")
    parser.add_argument("--path", nargs="+", help="Ruta(s) al archivo de prompt.")
    parser.add_argument("--text", type=str, help="Texto del prompt.")
    parser.add_argument("--format", choices=["markdown", "json", "summary"], default="markdown")
    parser.add_argument("--pipeline-check", action="store_true", help="Incluye chequeo informativo de convenciones C2C.")
    args = parser.parse_args()

    items = []
    if args.path:
        for p in args.path:
            abs_p = os.path.abspath(p)
            if not os.path.isfile(abs_p):
                print(f"Error: No existe el archivo {abs_p}", file=sys.stderr)
                sys.exit(1)
            with open(abs_p, "r", encoding="utf-8-sig") as f:
                items.append((f.read(), abs_p))
    elif args.text:
        items.append((args.text, ""))
    elif not sys.stdin.isatty():
        items.append((sys.stdin.read(), ""))
    else:
        parser.print_help()
        sys.exit(1)

    reports = []
    for content, path in items:
        auditor = PromptAuditor(content, path)
        res = auditor.audit()
        p_info = run_pipeline_check(content) if args.pipeline_check else None
        if args.format == "json":
            res["pipeline_check"] = p_info
            reports.append(res)
        elif args.format == "summary":
            fc = res["flaws_count"]
            print(f"[{res['verdict'][:20]}] Alta:{fc['alta']} Med:{fc['media']} Baj:{fc['baja']} | {path or 'string'}")
        else:
            print(format_markdown_report(res, p_info))
            if len(items) > 1:
                print("\n---\n")

    if args.format == "json":
        print(json.dumps(reports if len(reports) > 1 else reports[0], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
