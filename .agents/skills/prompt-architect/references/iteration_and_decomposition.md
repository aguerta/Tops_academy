# Iteración, descomposición, verificación y gobernanza de prompts

Contenido de `prompting-strategies.md`, `whats-new-gemini-3.6.md`, `whats-new-gemini-3.8.md`, `whats-new-gemini-4-hydrogen.md`, `thinking.md` y ***AI Engineering* (Chip Huyen, O'Reilly, Cap. 4, 5 y 10)** que complementa la guía principal.

## 1. Estrategias de iteración (cuando el prompt no da el resultado esperado)

1. **Reformular.** Palabras distintas con el mismo significado producen respuestas distintas.
   `Version 1: How do I bake a pie?` · `Version 2: Suggest a recipe for a pie.` · `Version 3: What's a good pie recipe?`
2. **Cambiar a una tarea análoga.** Si el modelo no respeta las opciones ("¿A qué categoría pertenece La Odisea: thriller, sci-fi, mitología, biografía?" → responde con un párrafo), reencuadrar como **problema de opción múltiple** ("Multiple choice problem: ... Options: ...") o migrar a una pregunta `choice` en la **Decisions API (`gemini-decision-1`)** para obtener la opción exacta con probabilidad calibrada y 0 tokens de salida.
3. **Reordenar el contenido.** Probar variantes: `[examples][context][input]`, `[input][examples][context]`, `[examples][input][context]`. Para contexto largo (1M unificado), el punto de partida obligatorio es **contexto estático primero y tarea al final**, lo que además maximiza los aciertos de **Implicit Caching** (95% de descuento desde 4,096 tokens).
4. **Suprimir preámbulos sin pre-llenar turnos del modelo.** En modelos antiguos se usaba *partial input completion* o un turno `model` pre-llenado (`{"role": "model", "parts": [{"text": "JSON:"}]}`). **En Gemini 3.6+, 3.8 y Gemini 4, pre-llenar el turno `model` devuelve HTTP 400** (`whats-new-gemini-3.6.md` §2). Para fijar el inicio de la respuesta sin preámbulos, usar `system_instruction` (`"Output only the JSON object without introductory text"`) o `response_format` con JSON Schema nativo.
5. **Quitar instrucciones si los ejemplos bastan.** La fuente indica que, con ejemplos claros, parte de las instrucciones puede eliminarse (`prompting-strategies.md` l. 297–299).

## 2. Selección de Nivel de Autonomía (Augmented LLM vs. Workflow vs. Agent) y Orquestación Multi-Modelo

Antes de escribir o auditar un prompt, el arquitecto debe elegir el **nivel más simple, predecible y económico** que satisfaga el requisito (*"Start with the simplest solution possible; an agent is a tradeoff, not an upgrade"*):

### 2.1 Los Tres Niveles de Autonomía
1. **Nivel 1 — Decisions API (`gemini-decision-1`) o *Augmented LLM* (1 Llamada):**
   - **Cuándo usarlo:** Cero orquestación. Una sola llamada con contexto recuperado (`<context>`) o herramientas de consulta puntual, o evaluación paralela de decisiones cerradas (`noul`, `choice`, `score` en `gemini-decision-1` con 0 tokens de salida).
2. **Nivel 2 — *Workflow* (Caminos de Código Predefinidos):**
   - **Cuándo usarlo:** La secuencia de pasos y sus ramas **se conocen de antemano**. El flujo de control lo gobierna el código del runner (ej. `run.py` en C2C v4.0), **no** el LLM. Es más rápido, barato, determinista y auditable que un agente libre.
3. **Nivel 3 — *Agent* (Loop Dinámico de Herramientas dirigido por el LLM):**
   - **Cuándo usarlo:** Únicamente cuando el número y orden de llamadas a herramientas **no puede predeterminarse** porque depende del *ground truth* ambiental descubierto en cada paso (ej. el loop interno de `c2c_shard_author` o `c2c_repair` compilando con `compile_shard.py --fail-total` y ajustando código según el error).

### 2.2 Los 5 Patrones de Workflow y la Matriz de 6 Primitivas de Orquestación en Antigravity (v2.32.0, Nov 2026)

| Patrón / Técnica | Quién decide el flujo | Cuándo usarla | Aplicación en C2C v4.0 (`content-to-course`), Antigravity (`v2.32.0`) y SDK |
|:---|:---|:---|:---|
| **1. Prompt Chaining** | Código fijo + compuertas programáticas | Pasos secuenciales fijos donde cada etapa valida un invariante antes de pasar a la siguiente. | C2C: `bootstrap` → `cta` (`cta.cert.json`) → `shard` → `authors` → `build` → `judges` → `gates` → `certify` → `publish`. En Antigravity (`/run-workflow`): fases `phase()` + `pipeline(items, fn)`. |
| **2. Routing** | Código determinista o `gemini-decision-1` | Clasificar la entrada y despachar a un camino especializado predefinido (**no** es *Orchestrator-Workers* si la regla de partición es fija). | Selección `direct` vs `mapreduce` ($k = \lceil P/20 \rceil$ si $>25$ págs.), aislamiento `1 Hab/shard` y **Matriz 2D de Edición** (Nivel 0 AST, Nivel 1 `edit_file`, Nivel 2 `ModularSplicing`, Nivel 3 `write_file`). |
| **3. Parallelization (*Sectioning* & *Voting*)** | Código fan-out / fan-in | *Sectioning*: dividir lotes independientes a $t=0$. *Voting*: múltiples evaluadores ciegos sobre el mismo ítem. | C2C: 1 sola ola paralela de `c2c_shard_author` a $t=0$ con `--lean`, o `parallel(items, fn)` en **Dynamic Workflows (`/run-workflow`)** validando cada retorno con JSON `schema` en `finish`. *Voting*: `c2c_judge` ciegos + `judge-compare`. |
| **4. Orchestrator-Workers** | LLM Coordinador en runtime | Cuando la descomposición de subtareas **no** puede fijarse por código y el coordinador debe decidir dinámicamente cómo dividir/re-dividir según hallazgos. | `invoke_subagent` / `SubagentConfig` en el SDK (con `max_subagent_depth` y `allowed_subagents`), o **`/swarm`** cuando los workers deben coordinar interfaces en un pizarrón compartido (*message board*). |
| **5. Evaluator-Optimizer** | Loop Generador ↔ Crítico | Un generador produce un borrador y un evaluador (determinista o juez LLM) emite diagnósticos accionables para refinarlo acotadamente. | Compilador `compile_shard.py` + `gates` + `repair-matrix` → `c2c_repair`; o `/swarm` con `@verifier` en un modelo distinto (*cross-model verification*), `/boost` y compuertas *Critic/Challenger/Auditor* en `/teamwork`. |
| **Enrutamiento Multi-Modelo (`Orchestrator` / `Carbon`/`Argon` + `Hydrogen`)** | Selector `Orchestrator` o Configuración por rol | Planificación arquitectónica o destrabe complejo seguido de ejecución paralela masiva (`whats-new-gemini-4-hydrogen.md` l. 102, 398; `antigravity.google/docs/models/`). | En 1 conversación: selector nativo **`Orchestrator (Carbon)`** u **`Orchestrator (Argon)`** (handoff automático a `Hydrogen`, regresando al planner tras 2 fallos de verificación). En multi-agente: Director en `Argon`/`Carbon` y olas de workers en `Hydrogen` (`flash` / `inherit`). |

#### Matriz Oficial de Selección Multi-Agente en Antigravity (`antigravity.google/docs/dynamic-workflows/` & `/docs/swarm/`)
Cuando se diseña u orquesta dentro del ecosistema Google Antigravity, elegir la primitiva exacta según la topología de coordinación:
1. **`Orchestrator (Carbon / Argon)`:** 1 sola conversación; Carbon/Argon planifica y revisa mientras `gemini-4-hydrogen` ejecuta herramientas con menor gasto de tokens. (*Nota:* tiene configuración fija; no admite ajustar `thinking_level` / `--effort`).
2. **`Subagents` (`invoke_subagent` / `SubagentConfig` en SDK):** Delegación puntual en background (investigación, validación en navegador o ejecución de un shard) con ventana limpia (`workspace: "inherit" | "branch" | "share"`, `model: "inherit" | "flash_lite" | "flash" | "pro"`).
3. **`Dynamic Workflows` (`/run-workflow`):** Flujo de control predecible gobernado por un script Python (`phase()`, `parallel()`, `pipeline()`, `agent(prompt, schema, role, type_name, workspace, model)`). Los agentes no se ven entre sí ni ven el script: cada uno recibe un prompt autocontenido y entrega un resultado estructurado validado contra `schema` mediante la herramienta `finish`.
4. **`/swarm`:** Tareas amplias que se dividen limpiamente entre archivos/paquetes donde workers nombrados, un `@verifier` (que puede fijarse a otro modelo para *cross-model verification*) y un `@monitor` se coordinan en un pizarrón compartido (*shared message board*). Los miembros en estado `waiting` consumen 0 tokens.
5. **`/boost`:** Razonamiento profundo iterativo para bugs complejos, condiciones de carrera o algoritmos donde workers desafían, rompen y verifican intentos previos.
6. **`/teamwork`:** Proyectos multi-hito de horizonte largo (horas a días) en un directorio dedicado con entrevista previa de alcance y compuertas adversariales independientes (*Sentinel*, *Project Orchestrator*, *Explorers*, *Workers*, *Critic*, *Challenger*, *Auditor*, *Success Auditor*).

Señal de que hay que descomponer o bajar de *Agent* a *Workflow*: el prompt intenta que el LLM recuerde y decida manualmente una secuencia de pasos que siempre es fija, mezcla objetivos con criterios de éxito distintos, supera el umbral de `500–1,500 tokens` en el system prompt (caso GoDaddy en *AI Engineering*, Cap. 5), o ignora restricciones ubicadas en la zona media (*Lost-in-the-Middle*).

## 3. Entradas multimodales y Resolución de Medios

- Tratar texto, imágenes, audio, video, PDF y documentos Office (DOCX, PPTX, XLSX, CSV) como **entradas de igual categoría** (`prompting-strategies.md` l. 699–701, `function-calling.md` l. 2820–2826).
- Las instrucciones deben **referenciar explícitamente cada modalidad** ("En la imagen de la página 3...", "Según el PDF adjunto...").
- En respuestas de funciones multimodales (`function_result`), colocar los archivos dentro del bloque `result` (usando URI de `Files API` para archivos >15 MB) y separar instrucciones inline con `\n\n` (`whats-new-gemini-3.8.md` l. 447–448).
- En Gemini 4, el entendimiento de video soporta `processing: "agentic"` (además de `"static"`) para inspeccionar fotogramas específicos y detalles visuales (`whats-new-gemini-4-hydrogen.md` l. 89–90).
- Para C2C (PDF, tinta manuscrita, imágenes grandes): indicar qué hacer con contenido ilegible (ej. marcar `[ILEGIBLE]` o `BLOCKED`) en lugar de dejar que el modelo adivine (`gemini-4-hydrogen` reduce afirmaciones fabricadas >5x cuando se le instruye reportar contexto faltante).

## 4. Planificación y autocrítica explícitas (opcional)

Con modelos que tienen razonamiento nativo (Gemini 2.5+, 3.6+, 3.8 y Gemini 4), **no hace falta** pedir el plan en la salida visible. Para tareas muy complejas, la fuente propone:

```text
Before providing the final answer, please:
1. Parse the stated goal into distinct sub-tasks.
2. Check if the input information is complete.
3. Create a structured outline to achieve the goal.
```

```text
Before returning your final response, review your generated output against the user's original constraints.
1. Did I answer the user's *intent*, not just their literal words?
2. Is the tone authentic to the requested persona?
```

Alternativa de menor costo en tokens de salida: configurar `thinking_level: "high"` (o `"xhigh"` en `gemini-4-hydrogen`) o añadir en `<final_instruction>`: `"Think very hard before answering"`.

## 5. Herramientas para evitar alucinaciones

- **Grounding con Google Search / Google Maps / URL Context:** habilitar cuando el modelo puede necesitar hechos recientes, geoespaciales o contenido de URLs específicas.
- **Code execution:** habilitar para cualquier aritmética, conteo o cálculo.
- **Decisions API (`gemini-decision-1`):** habilitar cuando el código necesita evaluar condiciones booleanas (`noul`), enrutamiento (`choice`) o puntajes de rúbrica (`score`) con probabilidades calibradas y 0 tokens generados.

## 6. Parámetros: resolución de conflictos entre fuentes (Actualizado Nov 2026)

Las fuentes históricas y las guías de migración recientes presentan diferencias; regla de precedencia: **la guía más reciente y específica del modelo destino manda.**

| Recomendación / Parámetro | Fuente | Estado en Modelos Actuales (Nov 2026) |
|:---|:---|:---|
| "Si hay respuesta de fallback, sube la temperatura." | Guía general (antigua, `prompting-strategies.md` l. 660) | **Obsoleta** para Gemini 3.6+/3.8/4: `temperature` se ignora o da error 400. Reformular el prompt o revisar `safety_settings`. |
| Enviar `temperature`, `top_p`, `top_k`, `candidate_count`. | Guía general antigua | **Prohibido en Gemini 3.6+, 3.8 y Gemini 4:** se ignoran en rango y devuelven **HTTP 400** fuera de rango o en futuras versiones (`whats-new-gemini-4-hydrogen.md` l. 385). |
| Pre-llenar turno `model` (`{"role": "model", ...}`). | Guía general antigua | **Prohibido (Error HTTP 400)** desde Gemini 3.6 (`whats-new-gemini-3.6.md` l. 171, 193). Usar `system_instruction` o `response_format`. |
| Usar `thinking_budget` numérico. | Gemini 2.5 | **Deprecado en Gemini 3.6+ y 4:** reemplazar por el enum `thinking_level` (`whats-new-gemini-3.8.md` l. 444). |
| Usar `thinking_level: "minimal"`. | Gemini 3.5 Flash-Lite / 3.6 Flash | **Error 400 en Gemini 4 y Gemini 3.8 Flash** (`thinking.md` l. 704). En Gemini 4 usar `low`, `medium`, `high` (y `xhigh` solo en `gemini-4-hydrogen`). |
| Ajustar `thinking_level` (`--effort` / `/effort`) cuando está seleccionado `Orchestrator`. | Selector de modelos en Antigravity App / CLI | **No aplicable en `Orchestrator (Carbon)` ni `Orchestrator (Argon)` (`antigravity.google/docs/models/`):** `Orchestrator` tiene configuración fija de razonamiento. Para elegir manualmente `thinking_level` (`low`/`medium`/`high`/`xhigh`), seleccionar el modelo directo (`gemini-4-hydrogen`, `gemini-4-argon` o `gemini-4-carbon`). |
| Usar `cachedContents` / `caches.create` (Explicit Caching) o marcadores `cache_control: {type: "ephemeral"}`. | Guía Long Context antigua / APIs de terceros | **No soportado en Gemini 4 ni en Interactions API** (`caching.md` l. 13–16). Eliminar `cached_content` / `cache_control` y aprovechar **Implicit Caching** (automático desde 4,096 tokens, 95% descuento y 0% recargo de escritura) manteniendo el prefijo inicial libre de timestamps/UUIDs volátiles. |
| Truncar o reescribir el historial `messages` in-place cada pocos turnos (*in-place windowing*). | Patrones pre-reasoning (ej. windowing en turno 5) | **Prohibido en Gemini 4 y Claude 5+ (`thinking.md`, `caching.md` l. 44–50):** editar turnos previos invalida las firmas criptográficas de los bloques `thought` (*Thought Signatures*) y destruye el caché incremental multi-turno. Mantener el historial *append-only*, usar *Structured Note-Taking* en disco y aplicar *Compaction* (`CompactionConfig(token_threshold=...)` en Antigravity SDK) solo con umbrales altos ante agotamiento de ventana o al iniciar una sesión/etapa nueva. |
| Bajar `max_output_tokens` (ej. a 8,192) para ahorrar tokens. | Práctica común antigua | **Contraproducente en Gemini 4 (`long-decode.md` l. 140, 383):** corta el pensamiento y deja la respuesta `incomplete`. Mantener 65,536 (o mín. 32,768) y regular el gasto con `thinking_level`. Para >64K usar `background: true`. |
| Pedir `<UPDATE>` XML/JSON en texto plano antes de una tool call. | Prompts de agentes antiguos | **Causa `Malformed_Function_Call` (`function-calling.md` l. 3742):** reemplazar por una función dedicada `update()` o encabezados Markdown `# UPDATE`. |

Las cláusulas específicas de modelo (ej. `"Your knowledge cutoff date is January 2025"`, recomendada para Gemini 3 Flash) **solo se incluyen si coinciden con el modelo destino**; verificar el valor real del modelo antes de usarlas.

---

## 7. Verificación de Instrucciones al Estilo *IFEval* vs. *INFOBench* (*AI Engineering*, Cap. 4)

Chip Huyen (*AI Engineering*, Cap. 4 § *Instruction-Following Capability*) distingue dos capas complementarias para verificar si un modelo obedece un prompt:

1. **Verificación Determinista tipo *IFEval* (Zhou et al. / Google):**
   - Evalúa restricciones mecánicamente comprobables mediante código sin necesidad de otro LLM: formato JSON válido, presencia de claves obligatorias, inclusión/exclusión de palabras clave (`forbidden words`), marcadores de finalización (`DONE:`, `BLOCKED:`), número de secciones o viñetas e idioma de respuesta.
   - **Regla de diseño:** Siempre que una restricción de salida pueda expresarse como una propiedad verificable al estilo *IFEval*, debe especificarse de forma determinista en `<output_format>` y validarse por script (como `audit_prompt.py` o un validador de esquema).
2. **Verificación Semántica Descompuesta tipo *INFOBench* (Qin et al. — DRFR):**
   - Evalúa restricciones de contenido, estilo, tono o dominio descomponiendo la instrucción compleja en una **lista de criterios atómicos `Sí/No`** (*Decomposed Requirements Following Ratio*).
   - **Sinergia con `prompt-architect` y `Decisions API`:**
     - En auditoría de prompts, `semantic_audit_checklist.md` implementa este patrón descomponiendo la calidad del prompt en preguntas atómicas `Sí/No/N/A`.
     - En producción, cuando una aplicación necesite verificar automáticamente múltiples criterios tipo *INFOBench* sobre una salida generada, enviar el mapa de preguntas `noul` (Sí/No) en una sola llamada a `gemini-decision-1` (**Decisions API**), evaluando hasta 1,000 criterios en paralelo con 0 tokens de salida.

---

## 8. Gobernanza de Prompts como Artefactos de Ingeniería: Metadatos, Catálogo y Prevención de *Drift* (*AI Engineering*, Cap. 5 y Cap. 10)

Tratar los prompts como cadenas de texto incrustadas dentro del código fuente dificulta las pruebas, la colaboración con expertos de dominio y la trazabilidad (*AI Engineering*, Cap. 5 § *Organize and Version Prompts* y Cap. 10 § *Drift detection*):

1. **Desacoplamiento y Metadatos Tipo `Dotprompt`:**
   - Separar los prompts de la lógica de ejecución en archivos dedicados y documentar sus metadatos de contrato (modelo destino, `thinking_level`, variables/placeholders de entrada `{var}`, esquema de salida y script consumidor).
2. **Prevención de *System Prompt Drift* y Ruptura de Contratos:**
   - En arquitecturas donde múltiples flujos o subagentes dependen de un prompt (o donde existen variantes `standard` y `lean/`), un cambio aparentemente menor en un prompt puede alterar silenciosamente las métricas del sistema (*System prompt drift*, Cap. 10) o romper el parseo aguas abajo.
   - Por ello, toda edición en `prompt-architect` exige ejecutar **`diff_mapper.py`** antes de aplicar cambios en disco, verificando determinísticamente que no se pierdan placeholders (`{x}`, `<x>`, `@x@`), rutas, señales (`DONE`/`BLOCKED`), claves JSON ni IDs de regla, y registrando el diff unificado para aprobación explícita del usuario.

---

## 9. La Pirámide Invertida de Confianza y su Materialización en Antigravity App/CLI/IDE y Python SDK (*Lauren Tan, SpaceX / xAI — "All Code Is Slop"*)

Cuando un agente falla o produce salidas de baja calidad (*slop*), el error más común es inflar `AGENTS.md`, `SKILL.md` o el system prompt añadiendo una nueva línea de prosa por cada fallo observado. Lauren Tan demuestra que el entorno del agente debe estructurarse como una **pirámide invertida de confianza**:

1. **Capa 1 y 2 — Checks Deterministas en Código, Schemas, Hooks y Políticas (Base de Mayor Confianza):**
   - **Regla *Deterministic Checks > Prose Rules*:** Antes de añadir una restricción en prosa al prompt, evaluar si puede imponerse de forma 100% determinista mediante:
     - **En Antigravity App / CLI / IDE (`antigravity.google/docs/hooks/`, `/docs/permissions/`, `/docs/skills/`):**
       - **Hooks declarativos (`.agents/hooks.json`):** Interceptar el ciclo de vida en `SessionStart`, `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation` y `Stop` (ej. `c2c_hook_guard.py` o linters síncronos).
       - **Motor de Permisos y Sandbox OS:** Regla de precedencia estricta `Deny > Ask > Allow` sobre presets (`Request Review`, `Default` con sandbox OS activo, `Auto`, `Turbo`).
       - **Scripts como Cajas Negras (*"Use scripts as black boxes"*, `/docs/skills/`):** Si una herramienta o API requiere demasiada sutileza para que el agente la use bien, encapsularla en un script CLI de la skill e instruir al agente a ejecutarlo (o consultar `--help`) sin leer el código fuente completo del script.
     - **En Google Antigravity Python SDK (`antigravity.google/docs/sdk/*`):**
       - **Esquemas Tipados:** `LocalAgentConfig(response_schema=PydanticModel)` + `await response.structured_output()`.
       - **Políticas Declarativas y Sandbox:** `policy.deny(...)` / `policy.allow(...)` / `policy.ask_user(...)` con predicados de argumentos (`when=lambda args: ...`) y `RunCommandConfig(enable_sandbox=True)` (recordando que `policy.confirm_run_command()` por defecto bloquea `run_command` en modo autónomo salvo autorización explícita en `policies`).
       - **Hooks Programáticos y Presupuestos:** Decoradores `@hooks.pre_tool_call_decide`, `@hooks.on_tool_error`, `@hooks.stop` (con `StopDecision.CONTINUE` para forzar completitud antes de cerrar) y `BudgetConfig(max_model_calls=..., max_tool_calls=..., max_total_tokens=...)`.
2. **Capa 3 — Verificación en Runtime e Invariantes (70% del esfuerzo de tokens):**
   - Dar al agente herramientas o CLIs para verificar su propia salida contra invariantes del sistema antes de dar por terminada la tarea (`antigravity.google/docs/cli/best-practices/` § *Establish verification loops*).
3. **Capa 4 — Prosa Mínima de Alto Juicio (`AGENTS.md` vs. `SKILL.md` vs. System Prompts):**
   - Reservar el texto del prompt exclusivamente para decisiones que requieren **juicio semántico**, arquitectura, tono y manejo de ambigüedad.
   - Aplicar la distinción oficial de `/docs/rules/`: escribir una **Rule** (`AGENTS.md`, `.agents/rules/*.md`) para invariantes y restricciones persistentes del repositorio, y escribir una **Skill** (`.agents/skills/<name>/SKILL.md`) para flujos de trabajo multi-paso cargados bajo demanda (*progressive disclosure*).
4. **Prevención de *Over-Rotation* (Prohibición de Parches Sintomáticos Ad-Hoc):**
   - Los modelos frontier tienden a **sobre-rotar** (*over-rotate*) cuando se añade al prompt una corrección puntual nacida de un único caso borde, tratándola como un dogma rígido que degrada el rendimiento general.
   - En el modo `editar` de `prompt-architect`, queda prohibido inyectar parches ad-hoc para un input aislado (*one-off symptom patching*); toda regla añadida debe formularse como un **principio generalizable de dominio o contrato**.
5. **El Contexto y los Ejemplos como "Jardín" (*Context Hygiene*):**
   - Dado que el código y los bloques `<context>` / `<examples>` son el mayor input del modelo, cualquier *workaround*, comentario obsoleto o inconsistencia menor dentro de los ejemplos few-shot será copiado y multiplicado por el agente como si fuera el patrón canónico establecido. Los ejemplos deben ser 100% prístinos.
