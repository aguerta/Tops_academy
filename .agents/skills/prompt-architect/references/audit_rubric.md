# Rúbrica de Auditoría Factual y Citada (v3)

Esta rúbrica establece la evaluación de calidad de prompts para modelos frontier (Gemini 3+, 3.8 Flash, Gemini 4) y agentes autónomos.

> [!IMPORTANT]
> **Principio de Trazabilidad e Integridad de Fuentes:**
> Cada dimensión, regla y hallazgo está respaldado por una **cita directa e inmutable** de las fuentes canónicas:
> 1. `prompting-strategies.md` / `prompting-strategies (1).md` (Google DeepMind)
> 2. `prompt_masterprompter.md` (Ultimate Prompt Architect)
>
> Queda terminantemente prohibido incorporar reglas sintomáticas o convenciones de infraestructura de código que no provengan de estas fuentes.

---

## 1. Catálogo Canónico de Reglas Citadas

| Regla ID | Categoría | Cita Directa de la Fuente | Severidad de Incumplimiento |
|:---|:---|:---|:---:|
| `R_ANTI_PATTERN` | Ejemplos Few-Shot | `prompting-strategies.md` § "Patterns vs anti patterns" (l. 96-109) & `masterprompter` Principle 6 | **Alta** |
| `R_DEPRECATED_SAMPLING` | Parámetros | `prompting-strategies (1).md` § "Model parameters note" (l. 511-524) & `masterprompter` Principle 4 | **Alta** |
| `R_CONTEXT_ORDER` | Contexto Largo | `prompting-strategies.md` § "Structure for long contexts" (l. 231-233) & `masterprompter` Principle 3 | **Alta** |
| `R_INPUT_ISOLATION` | Seguridad | `prompt_masterprompter.md` Stage 3 & Principle 2 (l. 45, 68-70, 133) | **Alta** |
| `R_AGENTIC_RISK` | Control Agentico | `prompting-strategies (1).md` § "Agentic workflows - Risk assessment" (l. 882-883, 915-917) & `masterprompter` l. 106-107 | **Alta** |
| `R_STRUCTURE_DELIMITERS` | Estructura | `prompting-strategies.md` § "Use consistent structure" (l. 226) & `masterprompter` Principle 2 | **Alta** |
| `R_SHOUTING` | Claridad y Tono | `prompting-strategies.md` § "Core prompting principles" (l. 225) & `masterprompter` Principle 1 | **Media** |
| `R_SEMANTIC_VERBOSITY` | Claridad y Tono | `prompting-strategies.md` § "Control output verbosity" (l. 228) & `masterprompter` Principle 4 | **Media** |
| `R_FEW_SHOT_MISSING` | Ejemplos Few-Shot | `prompting-strategies.md` § "Zero-shot vs few-shot prompts" (l. 78-79) & `masterprompter` Principle 6 | **Media** |
| `R_TEMPORAL_ANCHOR` | Grounding | `prompting-strategies (1).md` § "Gemini 3 Flash strategies" (l. 721-729) & `masterprompter` Principle 7 | **Media** |
| `R_STRICT_GROUNDING` | Grounding | `prompting-strategies (1).md` § "Grounding performance" (l. 738-754) & `masterprompter` Principle 7 | **Media** |
| `R_FEW_SHOT_COUNT` | Ejemplos Few-Shot | `prompt_masterprompter.md` Principle 6 (l. 84) & `prompting-strategies.md` § "Optimal number of examples" | **Baja** |
| `R_NATIVE_THINKING` | Razonamiento | `prompting-strategies (1).md` § "Enhancing reasoning and planning" (l. 757-767) & `masterprompter` Principle 5 | **Baja** |

---

## 2. Veredictos Cualitativos (Sin Puntuaciones Falsas)

En lugar de un número agregado que invite a la optimización engañosa, la evaluación clasifica el prompt en un veredicto técnico basado en la severidad de los hallazgos:

1. **Conforme con Estándares Frontier:** 0 hallazgos de severidad Alta o Media. El prompt sigue de forma rigurosa la totalidad de los principios citados.
2. **Aceptable con Observaciones:** 0 hallazgos de severidad Alta, 1-2 hallazgos de severidad Media. Funciona en producción pero presenta oportunidades de optimización.
3. **Requiere Refactorización:** 1 hallazgo de severidad Alta o $\ge 3$ hallazgos de severidad Media. Presenta riesgos concretos de mala interpretación, fallos de API (400) o reproducción de errores.
4. **Crítico:** $\ge 2$ hallazgos de severidad Alta. Vulnerable a inyección de prompt, fallos catastróficos de mutación o alucinaciones severas por falta de aislamiento y orden.

---

## 3. Desacoplamiento de Convenciones de Infraestructura

Las convenciones de infraestructura de proyectos específicos (tales como señales `DONE:`, salidas `BLOCKED:`, presupuestos de turnos o modos de puntero de disco de Top's Academy) **NO forman parte de la calidad del prompt engineering**.
- Se evalúan exclusivamente de manera informativa y separada mediante el flag `--pipeline-check`.
- Nunca suman ni restan al veredicto de calidad de ingeniería de prompts.
