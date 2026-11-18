# Checklist de auditoría semántica (Actualizado Nov 2026 + AI Engineering)

Se aplica **después** de `audit_prompt.py`. El pre-scan es heurístico (expresiones regulares); este checklist es la fuente de verdad del veredicto. Responder cada ítem con **Sí / No / N/A** y citar la línea o sección del prompt como evidencia. Todo "No" se convierte en hallazgo con severidad.

Severidad: **Alta** = puede producir salida incorrecta, inválida, fallo HTTP 400 / `Malformed_Function_Call` o insegura. **Media** = degrada calidad, introduce sesgo de evaluación o reduce consistencia. **Baja** = estilo o eficiencia.

## A. Objetivo, alcance, nivel de autonomía y paradigma de API
- A1. ¿El objetivo se puede expresar en una oración, cada sección del system prompt es *load-bearing* (sin prosa redundante; en workers de horizonte corto como `c2c_shard_author` ~12 KB, **incluyendo el 100% de las instrucciones estáticas de frente en Posición 0 sin obligar al agente a leer otro archivo de reglas por herramienta**) y coincide con lo que pide la salida?
- A2. ¿Todos los términos de dominio, umbrales, rutas y vocabulario compartido (*Feature Map*) están definidos sin ambigüedad?
- A3. **Nivel de Autonomía (*Augmented LLM vs. Workflow vs. Agent*) y Primitivas de Orquestación en Antigravity:** ¿El diseño elige el nivel más simple y predecible (evitando usar un loop de *Agent* libre cuando los pasos son fijos y corresponden a un *Workflow* de código como `run.py` o **`Dynamic Workflows (/run-workflow)`** con `parallel()`/`pipeline()` y validación por JSON `schema`), o selecciona la topología adecuada (`Orchestrator (Carbon/Argon)` en 1 conversación, `Subagents`, `/swarm`, `/boost`, `/teamwork`) distinguiendo Model IDs explícitos de API/SDK (`gemini-4-hydrogen`, etc.) frente a tiers de subagentes de Antigravity (`inherit | flash_lite | flash | pro`)? (ver `iteration_and_decomposition.md` §2)
- A4. Si la tarea es exclusivamente una decisión cerrada (sí/no `noul`, opción única `choice` o rúbrica `score`) o una lista de verificaciones atómicas tipo *INFOBench* sin requerir texto generativo: ¿se evaluó usar la **Decisions API (`gemini-decision-1`)** con 0 tokens de salida?

## B. Instrucciones, Justificación Causal, Verificabilidad (*IFEval* vs. *INFOBench*) y Pirámide Invertida
- B1. ¿Las instrucciones están en positivo (qué hacer) y las restricciones críticas no obvias incluyen **1 oración de justificación causal técnica** (*por qué* importa en el pipeline) para facilitar su generalización en Gemini 4?
- B2. ¿Existen instrucciones contradictorias? (Alta si sí.) ¿Está definida la precedencia cuando chocan?
- B3. ¿El orden de los pasos coincide con el orden real de ejecución?
- B4. ¿Hay énfasis por volumen (mayúsculas, "CRÍTICO", emojis de alarma) donde bastaría una directiva precisa (y que además provoque *overtriggering* de herramientas/subagentes en Gemini 4)?
- B5. ¿Las restricciones de formato/estructura están expresadas como propiedades verificables por código (estilo *IFEval*) y las restricciones de contenido/estilo como criterios atómicos verificables Sí/No (estilo *INFOBench*)?
- B6. **Pirámide Invertida y Anti-*Over-Rotation* (*Lauren Tan*):** ¿El prompt delega las invariantes deterministas a schemas (`response_schema`), linters, hooks (`.agents/hooks.json` o `@hooks` en Python SDK), políticas (`policy.deny/allow/ask_user`) y scripts ejecutados como cajas negras (`--help` sin leer su código fuente) en lugar de inflar la prosa, y está libre de parches sintomáticos hiper-específicos (*one-off symptom patches*) que provoquen sobre-rotación?

## C. Contexto, *Attention Engineering*, *Implicit Caching* y Grounding (*Textual Entailment* & *Negative Knowledge*)
- C1. **Ingeniería de Atención (Curva en U / *Lost-in-the-Middle*) e Higiene de Prefijo de *Implicit Caching*:** Con contexto largo o multi-turno: ¿está el contexto estático primero (**libre de variables volátiles como `timestamp` o `request_id` al inicio que invaliden el prefijo de *Implicit Caching***), los datos transaccionales de la instancia en un bloque `<case_facts>` / *Pointer Prompt* compacto al tope, los múltiples documentos estructurados en `<documents><document index="n"><source>...`, la `<task>` al final absoluto y una frase de anclaje entre ambos (y sin depender de negritas/mayúsculas para destacar hechos a mitad del contexto)?
- C2. ¿Está explícito si se permite conocimiento general o solo el material provisto bajo relación de *Textual Entailment* (tratando el estado `Neutral` —hechos no mencionados en el contexto— como falso/no respaldado, y pidiendo extraer citas `<quotes>` o supuestos explícitos `assumptions` antes de sintetizar cuando el documento supera 20k tokens)?
- C3. ¿Qué hace el modelo cuando la información falta? (respuesta fija, `BLOCKED`, campo `null`; `gemini-4-hydrogen` reduce invenciones >5x cuando se le instruye señalar contexto faltante).
- C4. ¿Las cláusulas específicas de modelo (fecha de corte, año 2026) corresponden al modelo destino?

## D. Formato de salida
- D1. ¿El formato es verificable mecánicamente (esquema JSON, secciones fijas, señal final)?
- D2. ¿Los ejemplos usan exactamente el mismo formato que la especificación?
- D3. Para JSON complejo: ¿se recomienda `response_format` (`mime_type: "application/json"`, `schema`) o `response_schema` nativo además del prompt, y **sin usar turnos `model` pre-llenados** (prohibidos con HTTP 400 desde Gemini 3.6)?

## E. Ejemplos Few-Shot y *Negative Knowledge*
- E1. ¿Hay 2–4 ejemplos con formato compacto en tokens? (0 = hallazgo Media; la fuente recomienda incluirlos siempre.)
- E2. ¿Son variados (casos normales, borde, de rechazo) y no copias con valores cambiados? En prompts RAG con `<grounding_contract>`: **¿incluye al menos 1 ejemplo de rechazo (*Negative Knowledge* / estado `Neutral`) donde el dato pedido no existe en el `<context>`?** (Media si falta.)
- E3. ¿Todos muestran el patrón correcto y son 100% prístinos (sin *workarounds*, comentarios obsoletos ni deuda técnica que el agente pueda copiar)? (Un ejemplo negativo / anti-patrón es Alta.)

## F. Seguridad
- F1. ¿Toda entrada externa (texto del usuario, archivos, salida de otros agentes) está delimitada y declarada como datos?
- F2. ¿Puede un contenido de entrada redefinir rutas, rol o formato? (Alta si sí.)

## G. Agentes, subagentes, gestión de horizonte largo y herramientas (N/A si no usa herramientas)
- G1. Scope-lock y `<investigate_before_answering>`: ¿define rutas de lectura/escritura exactas, prohíbe especular sobre archivos no leídos (respetando barreras de CLIs como `bootstrap` / `c2c_hook_guard.py`) y, si despacha subagentes, les pasa un *Pointer Prompt* autocontenido (`<case_facts>`) sin volcar el historial crudo del coordinador?
- G2. ¿Distingue lecturas (ejecutar sin preguntar, agrupando en paralelo si son independientes) de escrituras (verificar / confirmar), y aplica **Gobernanza en Dos Capas** (*System Prompt = Macro Policy* y *Tool Descriptions = Micro Policy* con la restricción principal en la primera línea de cada herramienta)?
- G3. Errores y Compromiso Anti-*Overthinking*: ¿reintento acotado en transitorios, cambio de estrategia en lógicos (ej. Matriz 2D de edición), salida `BLOCKED`, y directiva de comprometerse con un enfoque válido sin re-evaluar decisiones salvo evidencia contradictoria de una herramienta?
- G4. Contrato de turnos, presupuesto y **Tríada de Contexto en Gemini 4**: ¿mantiene el historial **estrictamente *append-only*** durante la sesión (prohibido truncar/windowing in-place que invalide *Thought Signatures* e *Implicit Caching*), combinando *Structured Note-Taking* en disco (`*.cert.json`, `cta.json`, `progress.txt`), *Sub-Agent Condensation* (~1,000–2,000 tokens de retorno) y *Compaction* solo al cambiar de sesión/etapa?
- G5. Señal de finalización única y parseable por el orquestador (y *Silent Reactive Barrier* `tools=[]` en despertares parciales $k < N$ cuando el prompt es de un Director de olas paralelas).
- G6. ¿La verbosidad durante la ejecución está fijada y **evita exigir bloques `<UPDATE>` XML/JSON en texto plano inmediatamente antes de llamar a una herramienta** (lo cual causa `Malformed_Function_Call`; usar función `update()` dedicada o Markdown `# UPDATE`)?
- G7. **Prevención de *Reflection Errors* (Falsa Completitud):** ¿Exige verificar explícitamente que el conteo de ítems de salida coincida con el lote de entrada ($N_{\text{salida}} = N_{\text{entrada}}$) y que todos los campos de `<output_contract>` estén poblados antes de emitir `DONE`, declarando las herramientas de forma nativa en `tools`?
- G8. **Cero Válvulas de Escape, Inmutabilidad de Tests/Verificadores, Anti-*Overengineering* y Uso de CLIs:** ¿Prohíbe usar comentarios/notas para justificar *workarounds*, prohíbe relajar tests/verificadores (`ver_*` triviales) o hardcodear casos de prueba, evita el *overengineering* / archivos temporales huérfanos e invoca CLIs deterministas de la skill cuando existen?

## H. Parámetros, ventana unificada y razonamiento
- H1. ¿Libre de `temperature`, `top_p`, `top_k`, `candidate_count`, `thinking_budget` legado, parámetros foráneos (`thinking: {type: "adaptive"}`, `effort`, `cache_control`) y turnos `model` pre-llenados para Gemini 3.6+/3.8/4?
- H2. ¿El `thinking_level` es válido para el modelo destino (`minimal` prohibido en Gemini 4 y 3.8 Flash; `xhigh` exclusivo de `gemini-4-hydrogen`; y recordando que en `Orchestrator (Carbon/Argon)` el nivel de pensamiento es fijo y no ajustable con `--effort`), `max_output_tokens` no está truncado artificialmente bajo (mín. `32,768` o default `65,536` ya que comparte presupuesto con `thought`), y no invoca `cachedContents` explícito en Gemini 4?
- H3. ¿Evita forzar razonamiento visible salvo que se necesite traza de auditoría, guía la reflexión post-herramienta (*interleaved thinking*) en bucles agénticos e indica usar `code_execution` para cálculo o conteo cuando esté disponible?

## I. Gobernanza, Jueces LLM (*AI as a Judge*) y Coherencia con el Pipeline
- I1. ¿Rutas, nombres de archivo, placeholders (`{x}`), IDs de regla (ej. `TPL-D3`) y esquemas coinciden con el código/skill que consume la salida (prevención de *Prompt Drift*)? Verificar leyendo el consumidor.
- I2. ¿Existe una versión `lean/` del mismo prompt? Si sí, ¿las reglas compartidas son consistentes entre ambas?
- I3. **Específico para Prompts de Jueces / Evaluadores (*AI as a Judge*, N/A si no es juez):** ¿Define una escala discreta corta (ej. `PASS/NEEDS_REPAIR/FAIL` o `1–5`) con descripciones claras por nivel, exige citar evidencia textual (mitigando *Self-Bias*) e incluye directivas explícitas contra el **Sesgo de Verbosidad** (*no premiar longitud sobre exactitud*) y el **Sesgo de Posición**?

## Veredicto
- **Listo para producción:** 0 hallazgos Alta y ≤ 2 Media.
- **Requiere refactorización:** 1 Alta o ≥ 3 Media.
- **Crítico:** ≥ 2 Alta.

Si el veredicto semántico difiere del puntaje del pre-scan, prevalece el semántico; explicar la diferencia en el reporte.
