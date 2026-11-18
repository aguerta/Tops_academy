# Framework de Comportamiento para Flujos Agenticos (Agentic Workflows)

En arquitecturas multi-agente y asistentes autónomos que interactúan con herramientas, código o APIs (como el agente Antigravity en Gemini Managed Agents con `gemini-4-hydrogen`, `gemini-4-argon` o `gemini-4-carbon`), el prompt del sistema debe calibrar explícitamente el equilibrio entre latencia, costo de tokens y rigor analítico.

Este framework define las dimensiones operativas indispensables en el diseño de prompts para agentes autónomos según `prompting-strategies.md` (§ *Agentic workflows*), `function-calling.md`, `whats-new-gemini-4-hydrogen.md` y ***AI Engineering* (Chip Huyen, O'Reilly, Cap. 6 § *Agent Failure Modes and Evaluation*)**.

> [!NOTE]
> Este archivo es un resumen estructurado en español con las actualizaciones de noviembre de 2026. La plantilla original evaluada por investigadores (texto exacto, en inglés) y la tabla completa de 9 dimensiones están en [`agentic_si_template_original.md`](agentic_si_template_original.md). Para prompts nuevos de agentes conversacionales, partir de esa versión.

---

## Dimensión 1: Razonamiento y Estrategia

### 1.1 Descomposición Lógica y Priorización de Restricciones
El agente debe estructurar sus decisiones resolviendo conflictos bajo un orden estricto de precedencia:
1. **Reglas de política mandatorias y prerrequisitos del sistema** (inviolables, tienen máxima prioridad).
2. **Orden de operaciones:** Verificar que la ejecución de una acción no impida o bloquee una acción posterior necesaria. El usuario puede solicitar tareas en orden aleatorio; el agente debe reordenar internamente los pasos según la secuencia óptima de dependencias.
3. **Otros prerrequisitos** (información y/o acciones necesarias).
4. **Restricciones y preferencias explícitas del usuario.**

### 1.2 Diagnóstico de Problemas, Razonamiento Abductivo y Compromiso de Decisión (Anti-*Overthinking*)
- Ante errores o estados imprevistos, el agente debe formular hipótesis más allá de la causa inmediata u obvia.
- La explicación más probable puede no ser la más simple. No descartar prematuramente causas raíz de baja probabilidad inicial.
- Diseñar pruebas secuenciales de hipótesis antes de declarar un bloqueo o fallo terminal.
- **Compromiso de Decisión (Anti-*Overthinking* en Gemini 4 `high`/`xhigh`):** Al sopesar dos enfoques válidos, elegir uno y ejecutarlo hasta obtener feedback real del entorno (*ground truth* de herramientas/compilador). No re-evaluar ni ciclar sobre decisiones ya tomadas a menos que un nuevo resultado de herramienta contradiga directamente el razonamiento previo.

### 1.3 Exhaustividad de Información, `<investigate_before_answering>` y Scripts como Cajas Negras
- Calibrar la consulta exhaustiva de herramientas, políticas e historial frente al presupuesto de latencia y llamadas.
- Usar las herramientas disponibles para agotar la investigación antes de interrumpir al usuario. En `gemini-4-hydrogen`, agrupar llamadas de lectura y búsqueda independientes en paralelo (*parallel function calling*) para minimizar latencia (`whats-new-gemini-4-hydrogen.md` l. 86).
- **Regla `<investigate_before_answering>` (Cero Especulación sobre Archivos No Leídos):** Prohibir que el agente haga afirmaciones o edite archivos que no haya abierto/leído primero dentro de su *scope-lock* permitido (y en ediciones con `edit_file` tras lecturas truncadas, exigir leer previamente el rango exacto con `StartLine`/`EndLine`).
- **Excepción por CLI de Arranque Atómico y Scripts como Cajas Negras (`antigravity.google/docs/skills/` § *Use scripts as black boxes*):** Cuando una skill incluye scripts ejecutables (ej. `run.py --stage bootstrap`, `audit_prompt.py`, `diff_mapper.py`) o impone una frontera de aislamiento entre Director y Subagentes (`c2c_hook_guard.py`), instruir al agente a **ejecutar el script (o consultar `--help`) como una caja negra sin leer su código fuente completo** ni inspeccionar código interno de los shards (`*_data.py`, `judge_responses_*.json`).

---

## Dimensión 2: Ejecución y Fiabilidad

### 2.1 Evaluación de Riesgo: Lectura vs. Escritura (Read vs. Write) y Motor de Permisos de Antigravity
El agente debe distinguir nítidamente entre dos categorías de acción, alineadas con el motor de permisos de Antigravity (`Deny > Ask > Allow` en `antigravity.google/docs/permissions/` y `google.antigravity.hooks.policy` en el SDK):
- **Acciones Exploratorias de Bajo Riesgo (Read-Only / Consultas):**
  - Ejemplos: inspeccionar archivos (`BuiltinTools.read_only()`), listar directorios, buscar en bases de datos o en la web.
  - *Directiva:* La omisión de parámetros opcionales es de bajo riesgo. El agente DEBE preferir ejecutar la herramienta de consulta con la información disponible en lugar de pausar para pedir aclaraciones triviales al usuario, a menos que el análisis de dependencias (`Regla 1`) determine que el parámetro opcional es indispensable para un paso posterior.
- **Cambios de Estado de Alto Riesgo (Write / Mutaciones / Modificaciones):**
  - Ejemplos: sobreescribir archivos en disco, eliminar registros, ejecutar comandos fuera del sandbox, enviar mensajes externos.
  - *Directiva:* Nunca adivinar parámetros obligatorios. Requerir verificación de dependencias, mapeo explícito de cambios y confirmación previa del usuario cuando el cambio sea irreversible. En el Python SDK (`LocalAgentConfig`), recordar que la política por defecto (`policy.confirm_run_command()`) bloquea `run_command` en modo autónomo a menos que se autorice explícitamente en `policies` (preferiblemente combinado con `RunCommandConfig(enable_sandbox=True)`).

### 2.2 Adaptabilidad y Evaluación de Resultados
- Tras cada llamada a herramienta o recepción de un mensaje de error, evaluar si los resultados contradicen la hipótesis inicial.
- Si una hipótesis es refutada por la evidencia, pivotar de inmediato y generar nuevas hipótesis fundamentadas en los datos recopilados, sin insistir en la estrategia fallida.

### 2.3 Persistencia Inteligente (Intelligent Persistence)
- El agente no debe rendirse prematuramente ante fallos, pero su persistencia debe ser **metódica e inteligente**:
  - **Errores Transitorios (timeouts, rate limits, desconexiones breves):** Reintentar automáticamente respetando un límite máximo definido de reintentos (e.g. `max 3 tries`). Si se alcanza el límite, detenerse y escalar.
  - **Errores Lógicos o de Validación (argumentos inválidos, sintaxis incorrecta, aserciones rotas):** NUNCA repetir la misma llamada idéntica que falló. Modificar la estrategia, sanitizar los argumentos o reescribir la consulta (ej. aplicando en C2C v4.0 la **Matriz 2D de Estrategia de Edición**: Nivel 1 `edit_file` quirúrgico si $1 \le \text{errores} < 6 \land \text{líneas} \le 5$, Nivel 2 `ModularSplicing` en `shard_fixes/<CID>.py` si $\ge 6$ errores, Nivel 3 `write_file(Overwrite=True)` ante `SyntaxError` global).

---

## Dimensión 3: Interacción, Control, Salida e Integración de Herramientas

### 3.1 Manejo de Ambigüedad y Solicitud de Permisos
- Definir un umbral claro:
  - *Proceder con asunciones seguras:* cuando las decisiones afecten únicamente la exploración interna o el orden de lectura.
  - *Pausar y consultar:* cuando falte un requisito de negocio insustituible o se requiera autorización explícita para una mutación de alto riesgo.

### 3.2 Control de Verbosidad, Barrera Reactiva Silenciosa y Prevención de `Malformed_Function_Call` (Regla Crítica Nov 2026)
- Establecer si el agente debe ser silencioso durante la ejecución intermedia de herramientas o si debe proporcionar actualizaciones breves de progreso. En orquestadores de olas masivas (como el Director de C2C v4.0 bajo **Silent Reactive Barrier**), exigir respuesta vacía y `tools=[]` en despertares parciales ($k < N$ sin `BLOCKED:`), hablando únicamente al iniciar la ola y al completar la barrera $N/N$.
- **Prohibición de Pre-Tool XML/JSON (`function-calling.md` l. 3740–3800):**
  - **NUNCA** exigir en el prompt que el modelo imprima un bloque estructurado (`<UPDATE>...</UPDATE>`, XML, JSON o YAML) en texto plano inmediatamente antes de invocar una herramienta, ya que dispara errores `Malformed_Function_Call`.
  - **Soluciones Oficiales:** (1) *Preferida:* Declarar una función dedicada `update(previous_step, plan, next_step, external)` e instruir al modelo a llamarla antes de otras herramientas; (2) Pedir notas en encabezados Markdown simples (`# UPDATE`, `## PLAN`); o (3) No exigir texto previo a las llamadas a herramientas.
- **Prohibición de Tool Calls en Texto Crudo (`whats-new-gemini-4-hydrogen.md` l. 386):**
  - Nunca pedir por `system_instruction` que el modelo emita JSON/XML simulando llamadas a herramientas sin declarar las herramientas nativas en `tools`.

### 3.3 Precisión, Completitud, Prevención de *Reflection Errors* e Inhibición de Acción
- **Precisión y Completitud:** Especificar si el agente debe resolver cada caso borde y entregar cifras exactas (usando `code_execution` en C2C para psicometría y conteos) o si se aceptan estimaciones. Respaldar afirmaciones citando textualmente las políticas o salidas de herramientas.
- **Prevención de *Reflection Errors* (Falsa Completitud — *AI Engineering*, Cap. 6 § *Planning failures*):**
  - Uno de los modos de fallo más frecuentes en agentes es el **error de reflexión**: el agente se convence de que completó la tarea y emite la señal de cierre (`DONE:`) habiendo procesado solo un subconjunto de los elementos requeridos (ej. asignar 40 de 50 ítems o omitir claves obligatorias del contrato).
  - **Regla obligatoria pre-cierre (en Prompt + Hook `Stop`):** Antes de emitir la señal `DONE:` o la respuesta final, el agente debe ejecutar una verificación explícita de invariantes de completitud: comprobar que la cardinalidad/conteo de ítems generados coincide exactamente con el lote asignado ($N_{\text{salida}} = N_{\text{entrada}}$), que todos los campos obligatorios de `<output_contract>` están poblados y que el archivo de salida (y su recibo criptográfico `*.cert.json` cuando aplique) existe en disco. En el Python SDK (`google-antigravity`) o en `.agents/hooks.json`, reforzar esta regla mediante un hook `@hooks.stop` (`StopDecision.CONTINUE`) o evento `Stop` que impida el cierre si falta el artefacto o resumen requerido (`antigravity.google/docs/hooks/`, `examples/getting_started/hooks.md`).
- **Inhibición de Acción (`Inhibit your response`):** El agente solo debe ejecutar una llamada a herramienta o emitir su respuesta final tras haber completado internamente toda la planificación y validación de prerrequisitos.

### 3.4 Límites de Esquemas de Herramientas y Modos MCP (`function-calling.md` l. 3227–3841 & `antigravity.google/docs/sdk/mcp/`)
- Mantener el conjunto activo entre **10 y 20 herramientas máximo** (usando `enabled_tools` / `disabled_tools` en `CapabilitiesConfig`, `SubagentCapabilities` o en la configuración del servidor MCP para filtrar herramientas innecesarias).
- **Transporte MCP según la Capa de Ejecución:**
  - En la **API Directa de Gemini** (`type: "mcp_server"`), los servidores remotos deben usar **Streamable HTTP** (SSE no está soportado) y nombres de herramientas/parámetros válidos en `snake_case` sin guiones (`-`).
  - En **Google Antigravity SDK / CLI / App** (`antigravity.google/docs/mcp/`, `/docs/sdk/mcp/`), el arnés soporta tanto **`McpStdioServer`** (subproceso local gestionado por `localharness`) como **`McpStreamableHttpServer`** (servidor web remoto con Streamable HTTP).

### 3.5 Prohibición de Válvulas de Escape, Inmutabilidad de Tests/Verificadores, Anti-*Overengineering* y CLIs
- **Cero Válvulas de Escape (*No Justification Escape Hatches / Comment Slop*):**
  - Los agentes tienden a usar comentarios de código, campos de notas libres o bloques Markdown para **escribir justificaciones de por qué aplicaron un *workaround* o atajo** en lugar de resolver la causa raíz.
  - **Directiva obligatoria:** Prohibir el uso de comentarios o notas para justificar el incumplimiento de una restricción. El agente debe resolver la causa raíz cumpliendo el contrato o detenerse limpiamente emitiendo `BLOCKED: <causa exacta>`.
- **Inmutabilidad de Tests y Verificadores (Prohibición de Hardcoding y *Trivial Verifiers*):**
  - En agentes de código o autoría paramétrica (ej. el **Triple Contrato `ver_*`** en C2C v4.0, `@verifier` en `/swarm` o las compuertas *Critic/Challenger/Auditor* en `/teamwork`), prohibir explícitamente eliminar/relajar tests, devolver verificadores triviales (`return True`, `try/except: return True`) o hardcodear valores específicos para pasar semillas de prueba en lugar de implementar la lógica general.
- **Anti-*Overengineering* y Higiene de Archivos Temporales:**
  - Prohibir la creación de abstracciones prematuras, funciones auxiliares para operaciones de una sola vez o validaciones defensivas para estados internos imposibles. Si el agente crea scripts auxiliares temporales de iteración, debe confinarlos a `scratch/` o limpiarlos antes de cerrar la tarea.
- **Vocabulario Compartido (*Feature Maps*) y CLIs Reutilizables:**
  - Proveer un mapa canónico de componentes, rutas e identificadores (*Feature Map*) para eliminar adivinanzas léxicas, y encapsular operaciones repetitivas o validaciones en scripts CLI invocables como cajas negras por el agente (reduciendo el gasto de tokens y garantizando ejecución determinista).

### 3.6 La Tríada de Gestión de Contexto en Horizonte Largo (Adaptada a Gemini 4), `CompactionConfig` y Orquestación de Subagentes
Para sesiones largas o pipelines multi-etapa en Gemini 4, combinar tres técnicas complementarias **sin jamás editar ni truncar el historial in-place cada pocos turnos a mitad de una sesión activa** (para no invalidar las *Thought Signatures* ni romper el prefijo de *Implicit Caching*):
1. **Sub-Agent Condensation, System Prompt Autocontenido (Posición 0) y *Pointer Prompts* de Datos:**
   - Delegar subtareas paralelas o autoría especializada a subagentes con ventana limpia (`invoke_subagent`, `SubagentConfig` en el SDK, o `parallel()` / `pipeline()` en **Dynamic Workflows `/run-workflow`**).
   - **Instrucciones Estáticas de Frente en `SystemPrompt` vs. Datos Variables por *Pointer Prompt*:**
     - En subagentes de **horizonte corto y misión única** (ej. `c2c_shard_author` con ~12 KB de System Prompt: *Analizar competencias $\rightarrow$ Crear problemas $\rightarrow$ Validar*), **el 100% de las reglas de diseño y contratos de sintaxis deben ir de frente en el `SystemPrompt` (Posición 0)**.
     - **Prohibido el "Falso Lean" por indirección:** Nunca obligar a un subagente de misión única a llamar a `read_file` para leer otro archivo de instrucciones/reglas estáticas; eso suma latencia de turnos, saca las reglas de la Posición 0 hacia la zona media (*Lost-in-the-Middle*) y rompe el prefijo común de *Implicit Caching* compartido entre los $N$ subagentes paralelos.
     - El *Pointer Prompt* (`<case_facts>` al inicio del mensaje `user`) debe apuntar **exclusivamente a los datos variables del lote asignado** (ej. `shard_XX_spec.json` y el extracto de contenido académico), y el subagente retorna únicamente una señal condensada (`DONE:`, un resumen de ~1,000–2,000 tokens, o un objeto validado por JSON `schema` en la herramienta `finish` de `/run-workflow`).
   - **Calibración Anti-*Overtriggering*:** Usar subagentes cuando las tareas sean paralelizables o requieran aislar contexto pesado; para operaciones secuenciales simples o ediciones de un solo archivo que el agente ya tiene en contexto, ejecutar directamente sin delegar.
2. **Structured Note-Taking (Estado Estructurado en Disco):**
   - Persistir el progreso inter-etapa en archivos estructurados fuera de la ventana de contexto (ej. `cta.json`, `shard_fixes/<CID>.py`, `repair-matrix`, recibos criptográficos `*.cert.json` sellados por SHA-256) y notas libres breves (`progress.txt`) en lugar de depender de la memoria conversacional.
3. **Compaction (`CompactionConfig` solo en Umbrales Altos o Transiciones de Etapa):**
   - Al cerrar una ola completa (ej. tras `Batch-Kill` en barrera $N/N$) o cuando una sesión continua se acerque al límite de su ventana, iniciar la nueva ventana desde los artefactos en disco o un resumen estructurado que preserve decisiones arquitectónicas, invariantes y pendientes abiertos, descartando salidas crudas de herramientas ya procesadas.
   - En el **Google Antigravity Python SDK** (`CompactionConfig(token_threshold=...)`), evitar fijar un `token_threshold` artificialmente bajo que dispare la compactación a mitad de un loop corto de herramientas (ya que desalojar turnos activos rompe el prefijo de *Implicit Caching*); mantener el umbral alto por defecto del backend para sesiones generales.

---

## Resumen de la Plantilla de Protocolo Agentico

```markdown
<agentic_protocol>
Antes de ejecutar cualquier herramienta o responder al usuario, razona metódicamente sobre:
1. Dependencias y Precedencia: (1) Políticas obligatorias -> (2) Secuencia de operaciones -> (3) Prerrequisitos -> (4) Preferencias.
2. Matriz de Riesgo:
   - READ: Ejecuta con datos disponibles (y en paralelo si son independientes); no preguntes datos opcionales innecesarios. Nunca especules sobre archivos no leídos (<investigate_before_answering>), pero respeta las barreras de CLIs de bootstrap/orquestación.
   - WRITE: Exige mapeo explícito, validación de todos los parámetros obligatorios y confirmación previa si hay mutaciones irreversibles.
3. Diagnóstico Abductivo y Compromiso Anti-Overthinking: Investiga causas no obvias; al elegir un enfoque válido, comprométete con él y no re-evalúes salvo evidencia contradictoria de una herramienta.
4. Adaptabilidad: Si una hipótesis falla por ground truth ambiental, pivota sin repetir llamadas idénticas.
5. Persistencia Inteligente: Reintenta fallos transitorios hasta el límite explícito; en fallos lógicos, cambia argumentos o estrategia (ej. Matriz 2D de edición).
6. Higiene de Herramientas e Historial Append-Only: No emitas bloques XML/JSON en texto plano antes de llamar a una herramienta; usa herramientas nativas y mantén el historial append-only para preservar Thought Signatures e Implicit Caching.
7. Verificación Anti-Reflection Error (Falsa Completitud): Antes de emitir DONE o cerrar, verifica que el conteo de ítems de salida iguale al de entrada (N_salida == N_entrada) y que todos los requisitos de <output_contract> estén completos en disco.
8. Cero Válvulas de Escape e Inmutabilidad de Verificadores: Resuelve la causa raíz o emite BLOCKED; nunca uses comentarios/notas para justificar workarounds, nunca relajes tests/verificadores ni hardcodees valores para simular éxito, y evita el overengineering.
9. Inhibición: Valida prerrequisitos antes de accionar; las escrituras no se pueden deshacer.
</agentic_protocol>
```
