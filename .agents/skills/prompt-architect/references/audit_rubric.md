# Rúbrica de Auditoría Factual y Citada (v5 — Actualizada Nov 2026 + AI Engineering)

Esta rúbrica establece la evaluación de calidad de prompts para modelos frontier (`gemini-4-hydrogen`, `gemini-4-argon`, `gemini-4-carbon`, `gemini-3.8-flash`, `gemini-3.6+`) y agentes autónomos.

> [!IMPORTANT]
> **Principio de Trazabilidad e Integridad de Fuentes:**
> Cada dimensión, regla y hallazgo está respaldado por una **cita directa e inmutable** de las fuentes canónicas oficiales de Google DeepMind / Google AI Studio (actualizadas a noviembre de 2026), Ultimate Prompt Architect y *AI Engineering* (Chip Huyen, O'Reilly):
> 1. `prompting-strategies.md` (`https://aistudio.google.com/docs/prompting-strategies.md`)
> 2. `whats-new-gemini-4-hydrogen.md`, `whats-new-gemini-4-argon.md`, `whats-new-gemini-4-carbon.md`, `whats-new-gemini-3.8.md`, `whats-new-gemini-3.6.md`
> 3. `thinking.md`, `long-decode.md`, `caching.md`, `function-calling.md`, `decisions-api.md`
> 4. `prompt_masterprompter.md` (Ultimate Prompt Architect)
> 5. *AI Engineering: Building Applications with Foundation Models* (Chip Huyen, O'Reilly, Cap. 3, 4, 5, 6 y 10)
>
> Queda terminantemente prohibido incorporar reglas sintomáticas o convenciones de infraestructura de código que no provengan de estas fuentes.

---

## 1. Catálogo Canónico de Reglas Citadas

| Regla ID | Categoría | Cita Directa de la Fuente | Severidad de Incumplimiento |
|:---|:---|:---|:---:|
| `R_ANTI_PATTERN` | Ejemplos Few-Shot | `prompting-strategies.md` § "Patterns vs anti patterns" & `masterprompter` Principle 6 | **Alta** |
| `R_DEPRECATED_SAMPLING` | Parámetros | `prompting-strategies.md` § "Experiment with model parameters" (l. 513-520), `whats-new-gemini-4-hydrogen.md` l. 385 & `masterprompter` Principle 4 | **Alta** |
| `R_PREFILLED_TURN_OR_INVALID_API` | Parámetros / API | `whats-new-gemini-3.6.md` § "Prefilled model turn validation" (l. 171, 193), `thinking.md` l. 704 (`minimal` error en Gemini 4/3.8) & `caching.md` l. 13-16 (`cached_content` / `cache_control` explícito no soportado en Gemini 4) | **Alta** |
| `R_PRE_TOOL_STRUCTURED_TEXT` | Control Agentico / Tools | `function-calling.md` § "Workarounds for pre-tool text requirements" (l. 3740-3800) & `whats-new-gemini-4-hydrogen.md` l. 386 (`MALFORMED_FUNCTION_CALL`) | **Alta** |
| `R_CONTEXT_ORDER` | Contexto Largo | `prompting-strategies.md` § "Core prompting principles - Structure for long contexts" (l. 707-714) & `masterprompter` Principle 3 | **Alta** |
| `R_INPUT_ISOLATION` | Seguridad | `prompting-strategies.md` § "Structured prompting examples" (l. 783-785) & `prompt_masterprompter.md` Stage 3 / Principle 2 | **Alta** |
| `R_AGENTIC_RISK` | Control Agentico | `prompting-strategies.md` § "Agentic workflows - Risk Assessment" (l. 879, 912-913) & `masterprompter` l. 106-107 | **Alta** |
| `R_STRUCTURE_DELIMITERS` | Estructura | `prompting-strategies.md` § "Core prompting principles - Use consistent structure" (l. 688-691) & `masterprompter` Principle 2 | **Alta** |
| `R_SHOUTING` | Claridad y Tono | `prompting-strategies.md` § "Core prompting principles - Be precise and direct" (l. 685-686) & `masterprompter` Principle 1 | **Media** |
| `R_SEMANTIC_VERBOSITY` | Claridad y Tono | `prompting-strategies.md` § "Core prompting principles - Control output verbosity" (l. 695-697, 827) & `masterprompter` Principle 4 | **Media** |
| `R_FEW_SHOT_MISSING` | Ejemplos Few-Shot | `prompting-strategies.md` § "Zero-shot vs few-shot prompts" (l. 296-299) & `masterprompter` Principle 6 | **Media** |
| `R_TEMPORAL_ANCHOR` | Grounding | `prompting-strategies.md` § "Gemini 3 Flash strategies - Current day accuracy" (l. 718-726) & `masterprompter` Principle 7 | **Media** |
| `R_STRICT_GROUNDING` | Grounding (NLI) | `prompting-strategies.md` § "Gemini 3 Flash strategies - Grounding performance" (l. 735-751) & *AI Engineering* (Chip Huyen) Ch. 4 § "Factual consistency - Textual entailment" | **Media** |
| `R_RAG_NEGATIVE_EXAMPLE` | Grounding / Few-Shot | *AI Engineering* (Chip Huyen) Ch. 4 § "Factual consistency" (queries sobre hechos inexistentes) & Ch. 5 § "How to Restrict a Model's Knowledge to Only Its Context" | **Media** |
| `R_JUDGE_BIAS_AND_SCALE` | Evaluación / AI as a Judge | *AI Engineering* (Chip Huyen) Ch. 3 § "How to Use AI as a Judge" & "Biases of AI as a judge" (Verbosity bias, Position bias, discrete scoring) | **Media** |
| `R_FEW_SHOT_COUNT` | Ejemplos Few-Shot | `prompting-strategies.md` § "Optimal number of examples" (l. 371-377) & `prompt_masterprompter.md` Principle 6 | **Baja** |
| `R_NATIVE_THINKING` | Razonamiento | `prompting-strategies.md` § "Enhancing reasoning and planning" (l. 754-764) & `masterprompter` Principle 5 | **Baja** |

---

## 2. Veredictos Cualitativos (Sin Puntuaciones Falsas)

En lugar de un número agregado que invite a la optimización engañosa, la evaluación clasifica el prompt en un veredicto técnico basado en la severidad de los hallazgos:

1. **Conforme con Estándares Frontier:** 0 hallazgos de severidad Alta o Media. El prompt sigue de forma rigurosa la totalidad de los principios citados.
2. **Aceptable con Observaciones:** 0 hallazgos de severidad Alta, 1-2 hallazgos de severidad Media. Funciona en producción pero presenta oportunidades de optimización.
3. **Requiere Refactorización:** 1 hallazgo de severidad Alta o $\ge 3$ hallazgos de severidad Media. Presenta riesgos concretos de mala interpretación, fallos de API (`400` / `Malformed_Function_Call`), sesgos de evaluación o reproducción de errores.
4. **Crítico:** $\ge 2$ hallazgos de severidad Alta. Vulnerable a inyección de prompt, fallos catastróficos de mutación o alucinaciones severas por falta de aislamiento y orden.

---

## 3. Desacoplamiento de Convenciones de Infraestructura

Las convenciones de infraestructura de proyectos específicos (tales como señales `DONE:`, salidas `BLOCKED:`, presupuestos de turnos o modos de puntero de disco de Top's Academy) **NO forman parte de la calidad del prompt engineering**.
- Se evalúan exclusivamente de manera informativa y separada mediante el flag `--pipeline-check`.
- Nunca suman ni restan al veredicto de calidad de ingeniería de prompts.
