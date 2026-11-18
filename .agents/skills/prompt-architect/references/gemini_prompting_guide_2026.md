# Guía de Prompt Engineering para Modelos Frontier (Gemini 4 Hydrogen/Argon/Carbon, Gemini 3.8 Flash, Gemini 3.6+)

Este documento consolida las directrices oficiales de diseño de prompts de Google DeepMind y Google AI Studio para modelos de la familia **Gemini 4** (`gemini-4-hydrogen`, `gemini-4-argon`, `gemini-4-carbon`), **Gemini 3.8 Flash** (`gemini-3.8-flash`) y **Gemini 3.6+**, actualizadas según la documentación oficial de noviembre de 2026 (`prompting-strategies.md`, `whats-new-gemini-4-*.md`, `thinking.md`, `long-decode.md`, `caching.md`, `function-calling.md`, `decisions-api.md`), complementadas con los principios de evaluación e ingeniería de sistemas de ***AI Engineering* (Chip Huyen, O'Reilly, Cap. 3–6 y 10)**.

---

## 1. Catálogo de Modelos Frontier Vigentes (Noviembre 2026)

| Modelo | Model ID | `thinking_level` Soportados (Default) | Ventana y Salida | Caso de Uso Recomendado por Google |
|:---|:---|:---|:---|:---|
| **Gemini 4 Hydrogen** | `gemini-4-hydrogen` | `low`, `medium`, **`high`** (default), `xhigh` | 1M unificado / 64K síncrono (1M *long decode*) | **Modelo general por defecto** (y default del agente Antigravity). Reemplazo recomendado de `gemini-3.8-flash`. Reduce afirmaciones fabricadas >5x al señalar contexto faltante en vez de adivinar; agrupa llamadas de lectura/búsqueda en paralelo. |
| **Gemini 4 Argon** | `gemini-4-argon` | `low`, **`medium`** (default), `high` | 1M unificado / 64K síncrono (1M *long decode*) | **Razonamiento frontier eficiente.** Inteligencia Gemini 4 con menor gasto de tokens de pensamiento por turno y menor latencia que Carbon en ingeniería de software, matemáticas y agentes de horizonte largo. |
| **Gemini 4 Carbon** | `gemini-4-carbon` | `low`, **`medium`** (default), `high` | 1M unificado / 64K síncrono (1M *long decode*) | **Máxima profundidad de razonamiento.** Invierte más tokens de pensamiento para explorar hipótesis y verificar casos borde en arquitectura compleja, pruebas formales, síntesis multimodal densa y auditoría de seguridad. |
| **Gemini 3.8 Flash** | `gemini-3.8-flash` | `low`, **`medium`** (default), `high` | 1M entrada / 64K salida separada | Ingeniería de software de horizonte largo y agentes autónomos en la serie Gemini 3. |
| **Gemini 3.5 Flash-Lite** | `gemini-3.5-flash-lite` | **`minimal`** (default), `low`, `medium`, `high` | 1M entrada / 64K salida separada | Máximo throughput y menor costo para extracción masiva, clasificación, enrutamiento y subagentes ligeros (subir a `medium`/`high` si el subagente usa herramientas). |
| **Orchestrator (Carbon / Argon)** | `Orchestrator (Carbon)` / `Orchestrator (Argon)` | **Fijo / No ajustable** (`--effort` no aplica) | 1M unificado (Planner + Executor) | **Selector multi-modelo nativo en Antigravity (`antigravity.google/docs/models/`):** Empareja `gemini-4-carbon` o `gemini-4-argon` (planificación y revisión) con `gemini-4-hydrogen` (ejecución e invocación rápida de herramientas) en una sola conversación, devolviendo el control al planner si un paso de verificación falla dos veces. |
| **Gemini Decision 1** | `gemini-decision-1` | N/A (1 pase prefill) | 262,144 entrada / **0 tokens de salida** | **Decisions API (`/v1beta/decisions`):** Evaluación paralela de hasta 1,000 preguntas cerradas (`noul` sí/no, `choice` opción única, `score` rúbrica ordenada) con probabilidades calibradas y `confidence`. |
| **Gemma 4 26B A4B (Local)** | `gemma4-26b` (`.litertlm`) | N/A (On-device LiteRT) | Ventana local compacta (`.lightweight()`) | **Ejecución local sin nube en Antigravity SDK (`LiteRTAgentConfig`):** Corre on-device (GPU Metal/CUDA o NPU, mín. 24 GB VRAM/unified memory recomendados) aplicando automáticamente el preset `.lightweight()`. |

> [!TIP]
> **Orquestación Multi-Modelo (`Orchestrator` Nativo vs. Enrutamiento Explícito por Rol):**
> - **En una sola conversación interactiva (Antigravity App / CLI / IDE):** Seleccionar `Orchestrator (Carbon)` o `Orchestrator (Argon)` automatiza el handoff entre planificación (`Carbon`/`Argon`) e implementación (`Hydrogen`). Ten en cuenta que `Orchestrator` tiene configuración fija y **no permite ajustar `thinking_level` (`--effort` / `/effort`)**; si necesitas fijar manualmente `thinking_level` (ej. `xhigh` en Hydrogen), selecciona el modelo individual directamente.
> - **Identificadores de `model` según la Capa de Ejecución (API/SDK Directo vs. Subagentes Internos de Antigravity):**
>   - **API Directa de Gemini / CLI (`agy --model`) / Python SDK (`LocalAgentConfig(model=...)`):** Usar los **Model IDs explícitos** de la tabla superior (`gemini-4-hydrogen`, `gemini-4-argon`, `gemini-4-carbon`, `gemini-3.8-flash`, `gemini-3.5-flash-lite`, `gemini-decision-1`).
>   - **Subagentes y Dynamic Workflows internos de Antigravity (`invoke_subagent`, `.agents/agents/*.md`, `agent(..., model=...)` en `/run-workflow`):** El arnés interno recibe **tiers abstractos** en el campo `model`: `inherit` (default, hereda el modelo de la sesión), `flash_lite`, `flash` o `pro` (`antigravity.google/docs/subagents/`, `antigravity.google/docs/dynamic-workflows/`).

---

## 2. Principios Fundamentales de Prompting

### 2.1 Precisión, Franqueza (Directness) y Justificación Causal (*Why Behind Constraints*)
- Formular el objetivo de manera clara, concisa e inequívoca.
- **Evitar el lenguaje persuasivo, emocional o enfático en mayúsculas** (e.g. evitar `¡MUY IMPORTANTE!`, `POR FAVOR NO OLVIDES`, `CRITICAL RULE`). Los modelos modernos responden significativamente mejor a especificaciones deterministas y técnicas (`prompting-strategies.md` § *Core prompting principles*). Además, en Gemini 4 (`Hydrogen`, `Argon`, `Carbon`), el lenguaje imperativo agresivo heredado de modelos antiguos provoca **sobre-disparo (*overtriggering*)** de herramientas o verificaciones redundantes.
- **Justificación Causal Técnica (*Motivation Behind Instructions*):** Acompañar las restricciones no obvias con 1 oración concisa que explique la **causa técnica o consecuencia en el pipeline** (ej. *"No inspecciones archivos antes de `--stage bootstrap` porque `bootstrap` normaliza el ID, cuenta páginas en `<0.2s` y genera los manifiestos automáticamente"*, o *"Tu salida será ingerida por un parser JSON sin pre-procesador, por lo que cualquier preámbulo romperá la etapa downstream"*). En Gemini 4, conocer el *porqué* técnico permite que el modelo generalice la restricción en sus pasos `thought` ante casos borde no enumerados.
- Definir explícitamente cualquier término ambiguo, parámetro de entrada o umbral numérico.

### 2.2 Delimitadores Estructurales, Presupuesto `--lean` y Gobernanza en Dos Capas
- Separar semánticamente las distintas secciones del prompt utilizando etiquetas XML (`<role>`, `<instructions>`, `<constraints>`, `<context>`, `<case_facts>`, `<task>`, `<output_format>`, `<examples>`) o encabezados Markdown estructurados.
- Mantener la misma convención de delimitadores a lo largo de todo el prompt; no mezclar formatos arbitrariamente.
- Colocar las reglas de comportamiento críticas, la definición de persona (`<role>`) y las restricciones invariantes en la **Instrucción de Sistema (`system_instruction` / `.agents/AGENTS.md`)** o al inicio absoluto del prompt (Posición 0 de máxima atención).
- **Dimensionamiento del System Prompt según Horizonte (*Generalista* vs. *Worker de Horizonte Corto*), `TemplatedSystemInstructions` vs. `CustomSystemInstructions` y Prohibición del "Falso Lean" por Indirección:**
  - **En agentes generalistas de sesión abierta** (ej. Antigravity IDE / App 2.0 o un agente interactivo en `google-antigravity` SDK donde el 90% de las reglas son condicionales según qué pida el usuario):
    - Modularizar flujos multi-paso en **Skills** (`.agents/skills/<name>/SKILL.md` con *progressive disclosure*: solo `name` y `description` se cargan de inicio) y dejar en **Rules** (`AGENTS.md`, `GEMINI.md` o `.agents/rules/*.md` con frontmatter `trigger: always_on | model_decision | glob | manual`) únicamente las invariantes y restricciones arquitectónicas (`antigravity.google/docs/rules/`, `antigravity.google/docs/skills/`).
    - En el **Google Antigravity Python SDK** (`antigravity.google/docs/sdk/personas/`), usar **`TemplatedSystemInstructions(identity=..., sections=[...])`** (o pasar un `str`), lo cual conserva el scaffolding base del arnés y las directrices de seguridad del SDK mientras añade tus secciones personalizadas.
  - **En subagentes especializados de horizonte corto y misión única** (ej. `c2c_shard_author` en C2C, ~12 KB vs. ~60 KB del prompt antiguo, cuyo flujo es fijo de 2–4 turnos: *Analizar competencia asignada $\rightarrow$ Crear problemas $\rightarrow$ Validar con `compile_shard.py`*), **TODAS las reglas e instrucciones estáticas que necesita para producir el artefacto a la primera (*First-Pass Yield*) DEBEN ir de frente en el `SystemPrompt` (Posición 0)**. En el Python SDK, cuando se requiera control total de la Posición 0 sin el scaffolding generalista del SDK, utilizar **`CustomSystemInstructions(text="...")`** o declarar un `SubagentConfig(system_instructions=..., tools=[...])` acotado.
  - **Anti-patrón de Indirección (*False Lean*):** Recortar artificialmente un System Prompt obligando al subagente a usar `read_file` en el Turno 1 para leer otro archivo de instrucciones/reglas es **contraproducente en Gemini 4** por cuatro razones:
    1. **Mismo o mayor gasto de tokens:** Los tokens del manual entran igual a la ventana cuando el agente los lee.
    2. **Pérdida de Posición 0 (Curva en U):** Al entrar como `tool_result` intermedio en vez de `system_instruction`, las reglas caen en la zona media (*Lost-in-the-Middle*) cuando el agente pasa a escribir y compilar código.
    3. **Ruptura del *Implicit Caching* entre subagentes paralelos:** Lo que está en el `SystemPrompt` (más `tools`) forma un prefijo 100% idéntico al inicio de los $N$ shards paralelos (activando el 95% de descuento de *Implicit Caching* desde $\ge 4,096$ tokens); en cambio, si cada subagente lee primero su `shard_XX_spec.json` (variable) y luego lee un archivo de reglas, rompe el prefijo común.
    4. **Penalización de latencia y *First-Pass Yield*:** Añade tool calls de lectura o provoca errores en el compilador por falta de reglas en el Turno 1.
  - **Regla de Oro para Workers (`~10–15 KB` Autocontenidos):** La reducción de 60 KB a ~12 KB se logra **eliminando prosa redundante y moviendo invariantes al compilador determinista (`compile_shard.py`)**, **nunca** mandando al worker a leer instrucciones en otro archivo. El subagente solo debe usar `read_file` para leer los **datos variables de su unidad asignada** (las competencias y el material fuente de su shard).
- **Gobernanza en Dos Capas (*System Prompt = Macro Policy* vs. *Tool Descriptions = Micro Policy*):**
  - El **System Prompt** establece la política macro (identidad, invariantes globales, secuencia general).
  - Las **Descripciones de Herramientas (`tool descriptions` / docstrings de funciones Python en `LocalAgentConfig(tools=[...])`)** establecen la política micro (qué hace la herramienta, cuándo invocarla, límites de ordenamiento frente a herramientas con nombres similares y precondiciones). **Colocar siempre la restricción o precondición más crítica en la primera línea de la descripción/docstring de la herramienta** (ej. `"Ejecutar SOLO después de que compile_shard.py haya emitido estado PASS"`).
- **Aislamiento contra Prompt Injection:** Envolver toda entrada externa en etiquetas de datos (`<context>`, `<input_data>`) y declarar explícitamente que su contenido es dato inerte y nunca instrucciones ejecutables (`prompting-strategies.md` l. 783–785).

### 2.3 Control Semántico de Verbosidad y Prohibición de Sampling Parameters
- **Deprecación de Sampling Parameters:** En Gemini 4 y Gemini 3.6+ (`3.6-flash`, `3.8-flash`, `4-hydrogen`, `4-argon`, `4-carbon`), los parámetros `temperature`, `top_p`, `top_k` y `candidate_count` están **deprecados e ignorados** (y valores fuera de rango o futuras versiones devuelven **HTTP 400**). Deben eliminarse por completo de la configuración (`prompting-strategies.md` l. 513–520, `whats-new-gemini-4-hydrogen.md` l. 385).
- **Control Semántico:** El determinismo, la extensión y el tono deben regularse mediante instrucciones semánticas explícitas dentro del bloque `<constraints>`:
  - `Verbosity: Low` (respuestas directas, telegráficas, sin introducciones ni despedidas).
  - `Verbosity: Medium` (explicaciones balanceadas con soporte técnico conciso).
  - `Verbosity: High` (análisis exhaustivo paso a paso, derivaciones completas).
  - `Tone: Technical / Formal / Conversational / Socratic`.

---

## 3. Tipos de Entrada y Prohibición de *Prefilled Model Turns*

### 3.1 Tipos de Entrada
1. **Pregunta (`Question Input`):** Consulta que el modelo debe responder directamente.
2. **Tarea (`Task Input`):** Acción concreta o procedimiento a ejecutar sobre datos.
3. **Entidad (`Entity Input`):** Clasificación, transformación o extracción sobre un objeto específico.

### 3.2 Prohibición de *Prefilled Model Turns* (Error HTTP 400 en Gemini 3.6+ y Gemini 4)
> [!WARNING]
> **Cambio Crítico de API (`whats-new-gemini-3.6.md` §2 & `whats-new-gemini-3.8.md`):**
> A partir de Gemini 3.6 Flash, 3.8 Flash y toda la serie Gemini 4, **pre-llenar el turno del modelo (*prefilled model turn* o *assistant response prefilling*) está prohibido y devuelve un Error HTTP 400** si el último turno no vacío del payload tiene `role: "model"`.
> - **NO usar** turnos `model` pre-llenados (ej. `{"role": "model", "parts": [{"text": "{"}]}`) para suprimir preámbulos o forzar JSON.
> - **En su lugar:** Utilizar directivas explícitas en `system_instruction` / `<constraints>` (ej. `"Output only the JSON object without introductory text"`) y esquemas nativos en `response_format` (`mime_type: "application/json"`, `schema: ...`).

---

## 4. Ejemplos Few-Shot: Reglas de Oro

### 4.1 Cantidad Óptima y *Many-Shot In-Context Learning*
- En prompts estándar, incluir de **2 a 4 ejemplos variados y de alta calidad** (`prompting-strategies.md` § *Zero-shot vs few-shot prompts*).
- Más de 4 ejemplos en tareas simples puede provocar *overfitting* al patrón sintáctico de los ejemplos.
- **Excepción (*Many-Shot In-Context Learning*):** Para tareas de dominio altamente especializadas donde few-shot no alcance calidad de producción, la ventana de 1M de tokens permite escalar a cientos o miles de ejemplos (*many-shot learning*), logrando rendimiento comparable a fine-tuning con descuento del 95% por *Implicit Caching* (`long-context.md` l. 109–120).

### 4.2 Patrones Positivos vs. Anti-Patrones (Regla Crítica)
- **SIEMPRE mostrar el patrón POSITIVO a seguir.**
- **NUNCA incluir ejemplos negativos o "anti-patrones"** (e.g. "Ejemplo de lo que NO debes hacer: ..."). Exponer un ejemplo erróneo aumenta la probabilidad condicionada de que el modelo replique dicho error.
- Formular toda restricción de forma afirmativa:
  - *Incorrecto:* `Don't end haikus with a question: [Ejemplo con pregunta]`
  - *Correcto:* `Always end haikus with an assertion: [Ejemplo con afirmación]`

### 4.3 Consistencia de Formato y Economía de Tokens
- Garantizar que la estructura sintáctica, etiquetas XML, espacios en blanco y saltos de línea de todos los bloques `<example>` sean exactamente idénticos al esquema especificado en `<output_format>` (`prompting-strategies.md` l. 379–386).
- **Economía de Tokens en Ejemplos (*AI Engineering*, Cap. 5, Tabla 5-2):** Cuando el volumen de peticiones sea alto, preferir estructuras compactas sin verbosidad redundante dentro de `<example>`, reduciendo hasta un ~30% el consumo de tokens de entrada a igual eficacia.

---

## 5. Arquitectura de Contextos Largos (1M Unificado), *Attention Engineering*, *Implicit Caching* y NLI Grounding

### 5.1 Posicionamiento de Contexto Primero, *Attention Engineering* (Curva en U) e *Implicit Caching* (95% Descuento)
1. **Curva de Atención en U (*Lost-in-the-Middle*, Liu et al.) y Posición Estructural:**
   - Todos los transformers presentan máxima atención en la **Posición 0** (`system_instruction` y primer 10% del prompt) y al **final absoluto** (último 5%, *Recency Bias*), con una caída de 40–50% en la zona media (40%–80%).
   - **La posición manda sobre el formato tipográfico:** poner hechos enterrados a mitad del contexto en **negritas** o MAYÚSCULAS no altera el peso de atención QKV del transformer; la solución es mover las restricciones críticas a Posición 0 (`system_instruction`), los hechos invariantes de la instancia a un bloque `<case_facts>` al tope del mensaje, y la `<task>` al final absoluto.
2. **Bloque `<case_facts>` / *Pointer Prompt* Autocontenido (`50–500 tokens`, sin prosa):**
   - En tareas transaccionales, olas de subagentes (que **no** heredan el historial de la conversación del Director) o bucles multi-turno, encabezar el turno `user` con un bloque `<case_facts>` de pares clave-valor escaneables (ej. IDs de competencias `CID`, rutas exactas de lectura/escritura en disco, cuotas como `MIN_ARCHETYPES = 4`, conteo esperado $N_{\text{entrada}}$).
3. **Estructura Multi-Documento Jerárquica (`<documents>`) y Extracción Previa de Evidencia (`<quotes>` / `assumptions`):**
   - Cuando se inyecten múltiples fuentes o documentos largos ($>20\text{k}$ tokens), anidarlos explícitamente en `<documents><document index="1"><source>...</source><document_content>...</document_content></document></documents>`.
   - Para maximizar la precisión sobre documentos densos, instruir al modelo a extraer primero citas textuales relevantes (`<quotes>`) o supuestos formales explícitos (`assumptions`: `id`, `statement_latex`, `role_in_proof`, `violation_consequence`, como en C2C v4.0) antes de ejecutar la síntesis o generación downstream.
4. **Frase de Anclaje (Context Anchoring):** Interpolar una frase de transición entre el `<context>` y la `<task>` final (`"Con base exclusivamente en la información proporcionada en el <context> y <case_facts> anteriores..."`, `prompting-strategies.md` l. 707–714).
5. **Traducción Estricta de Caching a Gemini 4 (`caching.md`):**
   - **Prohibición de `cachedContents` / `cache_control` explícito:** `cachedContents` / `caches.create` y marcadores manuales tipo `cache_control: {type: "ephemeral"}` **no existen o devuelven HTTP 400** en Gemini 4 (`Carbon`, `Argon`, `Hydrogen`) y en la Interactions API.
   - **Implicit Caching Automático (95% Descuento, 0% Recargo de Escritura):** Activo por defecto en Gemini 4 para prompts $\ge 4,096$ tokens cuando el prefijo común se ubica al inicio (sin el recargo `1.25x`/`2.0x` de escritura que cobran otras plataformas). En olas paralelas de subagentes dentro del mismo workspace que comparten `system_instruction` y definiciones de herramientas, o en bucles multi-turno *append-only* donde el nuevo turno añade $\ge 2,050$ tokens (`caching.md` l. 44–50), el caché se reutiliza automáticamente.
   - **Higiene del Prefijo de Caché (Prohibido Mutar el Inicio):** **NUNCA** inyectar variables volátiles (`{timestamp}`, `{request_id}`, reloj con segundos, contadores dinámicos) al inicio del `system_instruction` ni antes del bloque `<context>` estático; cualquier cambio de 1 token al principio invalida el 100% del prefijo de *Implicit Caching* aguas abajo. Ubicar datos dinámicos siempre después del prefijo estático.

### 5.2 Ventana Unificada de 1M, `max_output_tokens` y *Long Decode* (`long-decode.md`)
- En Gemini 4, la ventana de **1,048,576 tokens es compartida** entre entrada, pensamiento (`thought`) y salida (`output`).
- `max_output_tokens` limita la **suma combinada de tokens de pensamiento + salida**.
- **Regla crítica de presupuesto:** Bajar `max_output_tokens` (ej. a `8,192`) **NO** hace que el modelo piense de forma más concisa; simplemente **corta la respuesta antes de que termine de pensar** (estado `incomplete` con texto vacío).
  - Mantener el default de `65,536` (o mínimo `32,768`). Para gastar menos tokens, reducir `thinking_level`, nunca `max_output_tokens`.
  - Para respuestas o razonamientos que superen 64K tokens (hasta 1M), activar **Long Decode** con `background: true` y `max_output_tokens` entre `131,072` y `262,144`+ (`long-decode.md` l. 139–141, 381–392).

### 5.3 Cláusula de Grounding Estricto como *Textual Entailment* (NLI) y *Negative Knowledge* (*AI Engineering*, Cap. 4)
- **Factual Consistency como Textual Entailment (NLI):** Según *AI Engineering* (Cap. 4 § *Factual consistency*), la verificación de consistencia factual local frente a un `<context>` opera sobre tres estados lógicos:
  1. **Entailment (Implicación):** La afirmación se deduce directamente de las premisas del `<context>` $\rightarrow$ **Permitido**.
  2. **Contradiction (Contradicción):** La afirmación contradice el `<context>` $\rightarrow$ **Prohibido**.
  3. **Neutral (Indeterminado):** El `<context>` ni implica ni contradice la afirmación (incluso si es verdad en el mundo real) $\rightarrow$ **En RAG estricto debe tratarse como FALSO / No soportado**.
- **Regla de *Negative Knowledge* (Ejemplo Few-Shot de Rechazo Obligatorio en RAG):**
  - Chip Huyen (Cap. 4 y Cap. 5) demuestra que los LLMs alucinan desproporcionadamente ante consultas con **presuposiciones falsas o entidades ausentes en el contexto** (*"¿Qué dijo X sobre Y?"* cuando X no menciona Y).
  - Por tanto, en todo prompt con `<context>` y `<grounding_contract>`, **al menos 1 de los ejemplos `<example>` debe demostrar explícitamente el caso `Neutral` / sin evidencia**, respondiendo con la declaración exacta de indisponibilidad (`"La información solicitada no se encuentra disponible en los documentos provistos."`).

```xml
<grounding_contract>
Eres un asistente estrictamente anclado y limitado a la información proporcionada en el <context>.
En tus respuestas, apóyate ÚNICAMENTE en los hechos directamente mencionados en dicho contexto (relación lógica de Entailment).
NO debes utilizar tu conocimiento previo, sentido común ni extrapolaciones.
No asumas ni infieras más allá de lo explícitamente redactado; reporta los hechos con fidelidad exacta.
Trata el contexto como el límite absoluto de la verdad; cualquier detalle no contenido en el contexto (estado Neutral o Contradiction) debe ser considerado completamente falso e infundado.
Si la respuesta exacta no está contenida explícitamente en el texto, debes declarar inequívocamente: "La información solicitada no se encuentra disponible en el material suministrado."
</grounding_contract>
```

### 5.4 Anclaje Temporal
Para modelos con herramientas de búsqueda web (`Grounding with Google Search`), cláusula recomendada por la fuente (`prompting-strategies.md` l. 718–726):
```text
For time-sensitive user queries that require up-to-date information, you MUST follow the provided current time (date and year) when formulating search queries in tool calls. Remember it is 2026 this year.
```
Cláusula de fecha de corte — **solo si coincide con el modelo destino** (la fuente la da para Gemini 3 Flash; verificar el valor real de otros modelos):
```text
Your knowledge cutoff date is January 2025.
```

---

## 6. Razonamiento Nativo (`thinking_level`), *Interleaved Thinking* y *Thought Signatures*

- Reemplazar siempre el parámetro legado `thinking_budget` (o configuraciones foráneas como `thinking: {type: "adaptive"}` / `effort`) por el enum nativo de Gemini 4 **`thinking_level`** (`whats-new-gemini-3.8.md` l. 444):
  - `low`: Menor latencia y costo para chat rápido, clasificación o alto throughput.
  - `medium`: Balance óptimo (default en `gemini-4-carbon`, `gemini-4-argon`, `gemini-3.8-flash`, `gemini-3.6-flash`).
  - `high`: Default en `gemini-4-hydrogen`; máxima profundidad en `Carbon`, `Argon` y `3.8 Flash`.
  - `xhigh`: Exclusivo de `gemini-4-hydrogen` para problemas multi-paso extremos donde `high` no baste (evitar en extracción simple JSON para no causar *overthinking*).
  - `minimal`: **PROHIBIDO en Gemini 4 y Gemini 3.8 Flash** (devuelve error 400). Solo soportado en `gemini-3.6-flash` y `gemini-3.5-flash-lite` (`thinking.md` l. 676–705).
- **Guía de *Interleaved Thinking* (Reflexión Post-Herramienta) y Prevención de *Overthinking*:**
  - En bucles con herramientas (ej. compilación de shards o reparación en C2C), guiar el pensamiento intercalado: *"Tras recibir el resultado de una herramienta o compilador, evalúa en tu pensamiento interno si la evidencia confirma o refuta tu hipótesis antes de invocar la siguiente acción"*.
  - Para evitar parálisis por análisis (*overthinking*) en `high`/`xhigh`, incluir la directiva de **compromiso de decisión**: *"Al elegir entre dos enfoques válidos, selecciona uno y ejecútalo hasta el final; no re-evalúes decisiones tomadas a menos que el resultado de una herramienta o test contradiga directamente tu hipótesis"*.
- **No forzar bloques visibles `<thinking>` en la salida del usuario** salvo que se requiera traza de auditoría explícita. Para solicitar resúmenes del pensamiento interno por API, configurar `thinking_summaries: "auto"`.
- **Preservación de *Thought Signatures* e Historial *Append-Only*:** En sesiones multi-turno y de llamadas a herramientas en Gemini 4, el historial de mensajes debe ser **estrictamente *append-only*** (usando `previous_interaction_id` en la Interactions API o devolviendo intactos todos los bloques `thought` previos con su `signature` criptográfica). **Prohibido truncar, resumir in-place o reescribir mensajes anteriores a mitad del loop** (ej. borrar los turnos 1–4 en el turno 5), ya que invalida las firmas `thought` y destruye el prefijo de *Implicit Caching*.

---

## 7. Herramientas Nativas, Salidas Estructuradas y *Decisions API*

1. **Prohibición de Tool Calls en Texto Crudo y Pre-Tool XML (`function-calling.md` & `whats-new-gemini-4-hydrogen.md`):**
   - **Nunca** instruir en el prompt que el modelo emita llamadas a herramientas en JSON/XML de texto crudo sin declarar herramientas nativas en `tools` (provoca `MALFORMED_FUNCTION_CALL`).
   - **Nunca** exigir que el modelo imprima un bloque estructurado (`<UPDATE>...</UPDATE>`, XML, JSON o YAML) en texto plano **inmediatamente antes** de invocar una herramienta, ya que causa `Malformed_Function_Call`. Si se requieren notas de progreso previas a la herramienta, encapsularlas en una herramienta dedicada `update(previous_step, plan, next_step, external)` o usar encabezados Markdown (`# UPDATE`).
2. **Simplificación de Esquemas Complejos (`function-calling.md` l. 3808–3841):**
   - Mantener el conjunto activo entre **10 y 20 herramientas máximo**.
   - Si la máquina de estados rechaza un esquema complejo con `400 INVALID_ARGUMENT`: aplanar objetos anidados, hacer recursiones opcionales/nullable, reducir ramas `anyOf`/`enum` masivos, acortar nombres de propiedades y mover restricciones de longitud de arrays (`minItems`/`maxItems`) a la descripción del prompt.
3. **Structured Outputs (`structured-output.md`):**
   - En la Interactions API, configurar `response_format={"type": "text", "mime_type": "application/json", "schema": ...}` (o `response_schema` en `generateContent`) en combinación con `<output_format>`.
4. **Cuándo usar `Decisions API` (`gemini-decision-1`) en vez de un Prompt Generativo (`decisions-api.md`):**
   - Si el caso de uso **no** necesita generar texto libre ni extraer objetos abiertos, sino tomar una **decisión cerrada con probabilidades calibradas** (enrutar solicitudes, verificar cumplimiento de hasta 1,000 reglas de política en paralelo, clasificar sí/no `noul`, elegir una opción `choice` o calificar con una rúbrica lineal `score`), recomendar la **Decisions API (`gemini-decision-1`)**: ejecuta en un solo pase prefill con **0 tokens de salida** y entrega `confidence` calibrada.
   - Al redactar `instructions` para `gemini-decision-1`: formular preguntas atómicas en positivo (`"Is the tier Gold?"` en vez de `"Is the tier NOT Gold?"`), definir descripciones lineales en `criteria` y usar claves no posicionales como `"other"` en lugar de `"none_of_the_above"` (ya que las claves `choice` se ordenan alfabéticamente en UTF-8).
5. **Code Execution (Python Sandbox):**
   - Habilitar la herramienta nativa `code_execution` para cualquier tarea que involucre aritmética, conteo de palabras/tokens, álgebra simbólica o manipulación tabular.

---

## 8. Ingeniería de Prompts para Jueces (*AI as a Judge* — *AI Engineering*, Cap. 3 y Cap. 4)

Cuando un prompt tiene como misión evaluar, auditar, arbitrar o puntuar la salida de otro modelo o candidato (ej. jueces ciegos en C2C, evaluadores de calidad pedagógica o guardrails de salida), debe cumplir tres reglas específicas documentadas por Chip Huyen (*AI Engineering*, Cap. 3 § *AI as a Judge* y Cap. 4 § *Create scoring rubrics with examples*):

### 8.1 Sistemas de Puntuación Discretos vs. Continuos
- Los modelos de lenguaje razonan con mucha mayor consistencia sobre **clasificaciones categóricas** (`PASS | NEEDS_REPAIR | FAIL`, `Entailment | Contradiction | Neutral`) o **escalas enteras discretas y cortas (`1 a 5`)** que sobre escalas continuas (`0.0 a 1.0`) o rangos amplios (`1 a 100`).
- **Regla de diseño:** Prohibir que un prompt generativo pida puntajes flotantes arbitrarios sin anclaje. Definir siempre una rúbrica discreta donde cada nivel tenga una descripción semántica inequívoca y ejemplos de qué constituye cada puntaje. Si el sistema requiere probabilidades continuas calibradas (`0.01 a 0.99`), delegar la evaluación a `gemini-decision-1` (**Decisions API**).

### 8.2 Mitigación Explícita de Sesgos del Juez (*Judge Biases*)
Todo prompt de Juez LLM está expuesto a tres sesgos empíricamente demostrados (*AI Engineering*, Cap. 3 § *Biases of AI as a judge*):
1. **Sesgo de Verbosidad (*Verbosity Bias* — Wu & Aji, Saito et al.):** Los jueces LLM tienden a preferir respuestas más largas aunque contengan errores factuales o relleno, sobre respuestas concisas y exactas.
   - *Directiva obligatoria en `<constraints>` del Juez:* `"Evalúa exclusivamente la exactitud factual y el cumplimiento de criterios; NO premies la longitud, extensión ni verbosidad superficial. Una respuesta concisa y exacta es superior a una extensa con relleno o imprecisiones."`
2. **Sesgo de Posición (*First-Position Bias*):** En comparaciones pareadas (A vs. B), los LLMs favorecen sistemáticamente la primera opción mostrada.
   - *Directiva obligatoria:* Evaluar cada candidato contra la rúbrica objetiva antes de comparar, e ignorar el orden de presentación (`Candidato A` vs. `Candidato B`). En el pipeline consumidor, alternar (*swap*) el orden cuando sea crítico.
3. **Sesgo de Auto-Preferencia (*Self-Bias*):** Un modelo tiende a puntuar más alto texto generado por su propia familia. Se mitiga exigiendo **evidencia textual citada** antes de emitir el veredicto y utilizando verificaciones deterministas previas.
