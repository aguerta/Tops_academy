---
name: content-to-course
description: End-to-end Antigravity skill that converts any academic course materials (PDFs, handwritten ink, large images) into interactive Top's Academy courses using strict JSON stage contracts, parametric templates in a sandboxed Python engine, blind LLM arbitration, and automated validation without domain-specific code.
triggers:
  - "create course from pdf"
  - "generate tops academy course"
  - "analyze competencies"
  - "convert pdf to course"
  - "publish course"
inputs:
  pdf:
    type: string
    description: Path to input course document, directory, or multiple files
    required: false
  sources:
    type: string
    description: Path or list of input course document(s), directory, or multiple files
    required: false
  output_dir:
    type: string
    description: Directory where the published course JSON is stored (defaults to courses/)
    default: courses
  course_id:
    type: string
    description: Alphanumeric slug identifier for the course
    required: false
  title:
    type: string
    description: Human-readable title for the course
    required: false
  work_dir:
    type: string
    description: Working directory for intermediate stage JSON artifacts
    required: false
  stage:
    type: string
    description: Run a single stage (bootstrap, prepare, cta, cta-reduce, cta-apply, shard, templates, build, verify, publish, define-types, judge-compare, wave-status, unlock, gates, repair-matrix, certify, rejudge, rejudge-compare)
    required: false
  from_stage:
    type: string
    description: Resume pipeline execution from a given stage to completion
    required: false
  director_id:
    type: string
    description: Antigravity Director conversation ID for reactive watchdog and hook lockfile
    required: false
  cta_mode:
    type: string
    description: CTA processing mode explicit by user (direct, mapreduce, multiple, auto)
    default: auto
  granularity:
    type: string
    description: Pedagogical competency granularity (fine, standard, coarse)
    default: standard
  skip_judges:
    type: boolean
    description: Bypass independent blind judge report verification on publish
    default: false
  review_cta:
    type: boolean
    description: Pause execution after stage 1 (CTA) for inspection before template generation
    default: false
  strict:
    type: boolean
    description: Whether to enforce strict mode validation (16 psychometric rules)
    default: true
  append:
    type: boolean
    description: Whether to append questions into an existing course bank instead of replacing it
    default: false
outputs:
  course_file:
    type: string
    description: Absolute path to the validated course JSON (courses/<course_id>.json)
  cta_file:
    type: string
    description: Absolute path to the Cognitive Task Analysis document
---

# Content-to-Course Antigravity Skill (C2C v4.1 Formal Mas con Menos Architecture)

A universal, subject-agnostic educational engineering pipeline that converts raw academic materials (Beamer presentations, handwritten OneNote notes, statistical software exports, and high-resolution chalkboard images) into fully playable, interactive Top's Academy courses in **≤ 12 minutes** for a standard 20-competency curriculum under the "Más con Menos" (-65% tokens) formal paradigm.

---

> [!CAUTION]
> ## ⚡ REGLA CERO: ARRANQUE ATÓMICO EN 3 TURNOS (PROHIBIDO EXPLORAR SCRIPTS O CONTAR PÁGINAS)
>
> En cuanto leas este `SKILL.md`, tu **Turno 1** debe ser **EXCLUSIVAMENTE** ejecutar el comando `--stage bootstrap`.
> - 🚫 **PROHIBIDO** ejecutar `Get-ChildItem`, `dir`, `ls` sobre `.agents/skills/content-to-course/` o sobre `content/`.
> - 🚫 **PROHIBIDO** ejecutar `run.py --help`, `dispatch.py --help`, `prepare.py --help` o `ingest.py --help`.
> - 🚫 **PROHIBIDO** usar `read_file`, `view_file` o `python -c "with open(...)"` para inspeccionar `run.py`, `prepare.py`, `ingest.py`, `dispatch.py` o cualquier otro script `.py` del skill.
> - 🚫 **PROHIBIDO** usar `python -c "import fitz..."` o `import pypdf` para contar páginas de PDFs manualmente.
>
> ### ¿Por qué NO debes inspeccionar nada antes de `bootstrap`?
> Porque `run.py --stage bootstrap` **ya resuelve todo automáticamente en `< 1s`**:
> 1. **Normaliza `--course-id`** automáticamente (convierte mayúsculas/espacios a `snake_case` seguro, ej. `"Asyntotic_Estatistics_v3"` -> `asyntotic_estatistics_v3`).
> 2. **Descubre todos los PDFs/archivos** dentro del directorio o rutas pasadas en `--sources` y **cuenta sus páginas instantáneamente (`< 0.2s`) sin rasterizar**.
> 3. **Acepta directamente `--cta-mode <direct|mapreduce>` y `--granularity <standard|fine|coarse>`**, persistiendo ambos en `pre_cta_manifest.json` e `ingestion_manifest.json`.
> 4. **Genera los 4 archivos de tipos** en `<work_dir>/dispatch/types/{c2c_cta_architect,c2c_shard_author,c2c_judge,c2c_repair}.json`.
> 5. **Ejecuta internamente `dispatch_cta(pointer=True)`**, devolviendo en su JSON de salida (`stdout`) la lista `type_spec_files` y el arreglo `Subagents` listo para invocar (`c2c_cta_architect`), **sin necesidad de llamar a `dispatch.py dispatch-cta` por separado**.
>
> ### Secuencia Exacta de Arranque (arranque en 3 turnos cortos + registro diferido de tipos):
> - **Turno 1 (inmediatamente tras leer `SKILL.md`)**: Ejecuta **únicamente** este comando (ajustando `--course-id`, `--sources`, `--cta-mode` y `--granularity` según el pedido del usuario):
>   ```powershell
>   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage bootstrap --course-id <id> --sources <ruta_o_directorio_fuente> --cta-mode <direct|mapreduce> --granularity <standard|fine|coarse> --director-id <CONVERSATION_ID>
>   ```
>   *(Si el usuario no especifica modo o granularidad, usa `--cta-mode mapreduce --granularity standard` (default). Si el usuario pide explícitamente `cta_direct`/`direct`, pasa `--cta-mode direct`: la instrucción del usuario SIEMPRE prevalece y NUNCA se promueve a mapreduce por número de páginas o archivos. Si es extensión incremental de un curso existente, añade `--append --base-course courses/<id>.json`).*
> - **Turno 2**: Lee en paralelo (en 1 solo turno, solo lecturas = costo de generación casi nulo) todos los archivos devueltos en `type_spec_files` (`c2c_cta_architect.json`, `c2c_shard_author.json`, `c2c_judge.json`, `c2c_repair.json` y, si existe, `c2c_cta_harmonizer.json`).
> - **Turno 3 (arranque mínimo, solo `c2c_cta_architect`)**: Registra **únicamente** `c2c_cta_architect` vía `define_subagent` (NO registres aún los demás tipos para no retrasar el arranque).
> - **Turno 4 (lanzamiento inmediato CTA vía `run_workflow`, `< 2s`)**: Llama **ÚNICAMENTE** a `run_workflow` (sin combinarlo con `define_subagent` en el mismo turno, porque el runtime espera a terminar de generar todos los argumentos del turno antes de ejecutar la primera herramienta):
>   ```python
>   run_workflow(
>       ScriptPath="<workflow_script_path absoluto devuelto por --stage bootstrap>",
>       Description="Ejecutar ola CTA MapReduce con barrera N/N determinista",
>       Args={"work_dir": "<work_dir>", "mode": "cta"},
>   )
>   ```
> - **Turno 5 (registro diferido mientras `run_workflow` ya corre en segundo plano)**: Con la ola CTA ya en ejecución en segundo plano, registra en un único turno paralelo los 4 tipos restantes (`c2c_shard_author`, `c2c_judge`, `c2c_repair` y `c2c_cta_harmonizer` si existe) usando los JSON ya leídos en el Turno 2. Luego detén tu turno hasta que `run_workflow` notifique el cierre `N/N`.
>   *(Solo usa `invoke_subagent` manual + `schedule` como fallback si `run_workflow` no está disponible en el entorno).*

---

> [!IMPORTANT]
> ## ROL FUNDAMENTAL: LA CONVERSACIÓN PRINCIPAL ES EL DIRECTOR DE PROYECTO
>
> La conversación principal actúa **exclusivamente como Directora de Proyecto / Orquestadora General**. Su responsabilidad es coordinar el flujo de trabajo, invocar las etapas del runner CLI (`run.py`), inspeccionar los presupuestos y artefactos de control, y **delegar todas las tareas intensivas a subagentes especializados en paralelo mediante `invoke_subagent`**.
>
> ### 🏛️ ARQUITECTURA C2C v4.0 FORMAL "MÁS CON MENOS":
> - **Fast Bootstrap & Promoción MapReduce (SLA ≤ 60–90s)**: Inicialización atómica CLI (`run.py --stage bootstrap`) sin rasterizado, selección determinista de modo CTA y particionado `slice_pdf_lossless` ($k = \lceil P/20 \rceil$) cuando supera 25 páginas.
> - **Contrato Form-C Quad-Band (`MIN_ARCHETYPES = 4`)**: Cada competencia define obligatoriamente 4 arquetipos disjuntos (Directo `'easy'`, Inverso `'medium'`, Perturbación `'hard'`, Frontera/Casos de Borde `'hard'`) con $\ge 2$ niveles Bloom y diversidad multimodal (`1 MC7 + 2 FIB + 1 MS` en `Hab-*`, `1 MC7 + 1 FIB + 1 MS` en `C-*`/`H-*`). En `Hab-*`, las 4 funciones generadoras producen **4 fórmulas algebraicas objetivo disjuntas en AST** (`SymPy`).
> - **Supuestos Explícitos (`assumptions` en `cta.json`)**: Toda competencia técnica declara supuestos formales (`id`, `statement_latex`, `role_in_proof`, `violation_consequence`). El 4.º arquetipo evalúa obligatoriamente la ruptura de un `assumption_id` explícito.
> - **Triple Contrato Anti-Trampas para Verificadores (`ver_*`)**: (1) Soundness positiva `ver_fn(correct) is True` en 50 semillas; (2) Refutación estricta de distractores `ver_fn(d_i) is False` para los 6 distractores; (3) Cero verificadores triviales (`return True` o `try/except: return True` bloqueados en AST).
> - **Matriz 2D de Estrategia de Edición (`decidirEstrategiaEdicion`)**:
>   * *Nivel 0 (< 5 ms)*: Auto-heal AST/Tokenize en compilador (delimitadores, wraps, R-23).
>   * *Nivel 1 (10–25 s)*: `1 <= errores < 6` Y `lineasInfractoras <= 5` $\implies$ `edit_file` quirúrgico obligatorio.
>   * *Nivel 2 (20–40 s)*: `errores >= 6` O `lineasInfractoras > 5` $\implies$ `ModularSplicing` obligatorio (`shards/shard_fixes/<CID>.py`). Bloquea edición in-place repetitiva.
>   * *Nivel 3 (60–120 s)*: `SyntaxError` global $\implies$ `write_file(Overwrite=True)` atómico.
> - **Recibos Criptográficos `*.cert.json` (< 5 ms)**: `compile_shard.py` emite certificados sellados por SHA-256. En `--stage templates` y `--stage certify`, la verificación criptográfica salta por completo re-ejecutar el sandbox sobre shards inalterados.
> - **Arquitectura de 1 Único `SystemPrompt` por Rol + `[SCOPE-LOCK]` en Mensaje Inicial**: Las reglas estáticas residen exclusivamente en `system_prompts/lean/prompt_*.md` ($\le 5\text{ KB}$ en `cta`, `judge`, `repair`; bloque canónico Form-C en `author`). El mensaje inicial (`Prompt`) de cada subagente define su contrato estricto `[SCOPE-LOCK]` con las rutas exactas permitidas (`READ`/`WRITE`/`COMPILE`/`DONE`), mientras que `dispatch/items/*.json` y `prompts/repair/*.json` contienen únicamente datos puros de la partición sin repetir el `SystemPrompt` ni incluir el literal `"DONE:"` en disco.
> - **Unicidad Diagnóstica por Slot de Distractor ($\ge 80.0\%$ por `(competency_id, distractor_id)`)**: Métrica unificada por slot de distractor entre Stage 3 (`check_templates.py`) y Stage 6 (`standardized_audit_engine.py`). Cada distractor dentro de una competencia debe tener un `error_rationale` causal específico y disjunto ($\ge 80.0\%$ de slots únicos); queda estrictamente prohibido el uso de prefijos taxonómicos rotativos (`"Error conceptual:"`, `"Trampa algebraica:"`, etc.) o tuplas de múltiples paráfrasis por semilla.
> - **Orquestación de Olas en Código con `run_workflow` (`workflows/c2c_wave_workflow.py`)**: Además de la barrera reactiva protegida por hooks (`invoke_subagent`), el Director puede ejecutar las olas de Stage 3–5 de forma determinista en código mediante `run_workflow(ScriptPath="<workflow_script_path absoluto devuelto por --stage bootstrap>", Args={"work_dir": "<work_dir>", "mode": "authors|judges|repair|repair_and_rejudge|post_cta_pipeline"})`, eliminando sondeos manuales de `manage_subagents` y errores por `kill_all` prematuro.
> - **Fail-Total en Compilador (`--fail-total`)**: `compile_shard.py` opera con `--fail-total` tanto en autoría como en reparación para abortar ante errores fatales sin tolerar compilaciones inconsistentes.
> - **Herramientas Nativas Estándar**: Subagentes y runner operan con herramientas nativas de plataforma (`read_file`, `write_file`, `edit_file`, `run_command`, `send_message`) con soporte retrocompatible.
> - **Juez Epistémico 1-Seed con Dominancia Bayesiana ($\alpha_{\text{Kernel}} = 0$)**: 1 única semilla pre-verificada por plantilla enfocada en suficiencia epistémica y no-giveaway semántico; ninguna objeción heurística revoca una prueba matemática formal.
> - **Silent Reactive Barrier Protocol (~12–16 Turnos del Director)**: Al iniciar una ola, el Director emite 1 línea mínima (`Iniciando etapa: <nombre> (<N> unidades).`). En despertares reactivos parciales (`k < N` sin `BLOCKED:` ni timer), no ejecuta herramientas ni emite texto visible (`tools=[]`, respuesta vacía) y finaliza en `< 2s`. Solo vuelve a hablar al completar `N/N` (`Listo, se completó la etapa de <nombre> (<N>/<N>).`), cuando vence el timer del watchdog, o si un subagente reporta `BLOCKED:`.
> - **Weighted Waves (`1 Hab/shard`, olas ≤ 100)**: Priorización *Heaviest-First*: cada habilidad compleja (`Hab-*`) se aísla en su propio shard individual y se despacha a $t=0$ (soporte continuo de hasta 100 shards concurrentes en una sola ola paralela). Para filtrar una ola concreta usa `dispatch.py dispatch-authors --work-dir <work> --wave <N>`. **Regla de espera y remediación consolidada:** si un comando encadena `judge-compare` y `gates` y `gates` pasa a segundo plano, espera su finalización (`manage_task`/barrera reactiva) y consolida TODAS las discrepancias de jueces y fallos de Quality Gates antes de lanzar reparación. Tras finalizar `gates` + `repair-matrix`, prefiere `run_workflow` con `mode="repair_and_rejudge"` (o un único `dispatch-repair --ids <todos>`), nunca despaches reparación con resultados parciales y **nunca** ejecutes `rejudge-compare` mientras una tarea `run_workflow` siga activa en segundo plano.
> - **Compuerta Bloqueante Pre-Publish (`PublishQualityGateError`)**: Publicación bloqueada ante objeciones de jueces no resueltas o incumplimiento psicométrico (MPRI $\ge 75$, ZPD $> 0$, P4 $\ge 13.0/15$, unicidad diagnóstica por slot de distractor `(competency_id, distractor_id)` $\ge 80.0\%$, 0 hard penalties).
> - **PrairieLearn KaTeX Orthogonal (@var@)**: Desacoplamiento total entre KaTeX y Python mediante tokens `@var@` / `@var:fmt@` en raw strings `r"..."`.

---

## 🏗️ Diagrama de Flujo v4.0

```
[ Fuentes Académicas: PDFs Beamer, Trazos Vectoriales, Apuntes ]
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Fast Bootstrap (run.py --stage bootstrap --course-id <id> --sources <...>)  │
│ - Ingesta Zero-Raster, manifiestos centralizados y delta continuo           │
│ - Genera work/dispatch/types/*.json (≤ 5 KB cada uno) y Subagents CTA       │
│ - Inicializa .c2c_subagent_lock.json con campos de gobernanza síncrona      │
│ - Activa watchdog (schedule a 7 min con budget_guard.py)                    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Stage 1: Síntesis Curricular CTA (run.py --stage cta)                       │
│ - Arquitectos leen sus partes con Pointer Prompts (<500 B) en Form-C        │
│ - Extrae competencias con assumptions [{id, statement, consequence}]        │
│ - Auto-healing L1–L5; en mapreduce fusiona cta_parts/part_*.json -> cta.json│
│ - Emite cta.cert.json sellado criptográficamente                            │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Stage 2: Sizing Ponderado y Sharding (run.py --stage shard)                 │
│ - Aislamiento estricto: máximo 2 Skills (Hab-*) por shard                   │
│ - Conceptos y Hechos contiguos en bloques de hasta 3 por shard              │
│ - Genera work/shards/pre_shard_manifest.json ordenado Heaviest-First        │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Stage 3: Fan-Out Paralelo en 1 Sola Ola (dispatch-authors)                  │
│ - Máxima paralelización: Todos los shards lanzados a t=0 con --lean         │
│ - Contrato Form-C Quad-Band: 4 arquetipos disjuntos (1 MC7 + 2 FIB + 1 MS)  │
│ - Triple contrato ver_* (Soundness + Refutación Estricta de Distractores)   │
│ - Emite shard_XX.cert.json al aprobar 50 semillas (< 5 ms en downstream)   │
│ - Silent Reactive Barrier: 0 texto y 0 herramientas en parciales (k < N) │
│ - Matriz 2D de edición en caso de error (edit_file vs shard_fixes/<CID>.py) │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Stage 4: Instanciación Masiva y Validación (run.py --stage templates/build) │
│ - Templates: Fast-path < 5 ms por shard_XX.cert.json sin re-cómputo         │
│ - Build: Sweeps deterministas CRC32 (cuotas: 30 Skill / 20 Concepto y Hecho)│
│ - Diversidad de stems >= 0.50 y evaluación de invariantes analíticos        │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Stage 5: Verificación Ciega Epistémica (dispatch-judges --ready-only)       │
│ - Lotes ciegos ≤ 12 ítems; 1 semilla canónica pre-verificada por plantilla  │
│ - Dominancia Bayesiana: α_Kernel = 0 (el juez LLM no anula verdad formal)   │
│ - Arbitraje ciego: run.py --stage judge-compare                             │
│ - Re-arbitraje quirúrgico sólo sobre modificadas: run.py --stage rejudge    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Stage 6: Compuertas y Publicación (run.py --stage gates / certify / publish)│
│ - run.py --stage gates: build + verify + QA dry-run + repair-matrix         │
│ - run.py --stage certify: verificación formal completa multi-etapa          │
│ - Publica a courses/<course_id>.json, emite publish.cert.json               │
│ - Evalúa Rúbrica Determinista QA y emite reports/qa_audits/<id>_qa_report.md│
│ - Libera cerrojo .c2c_subagent_lock.json y reporta URL y métricas de calidad│
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Regla de Oro: Protocolo de Barrera Reactiva Silenciosa y Batch-Kill en Barrera N/N

El Director de Proyecto debe mantener una interacción conversacional ultra-eficiente (~12–16 turnos en toda la corrida).

> [!CAUTION]
> **BARRERA REACTIVA EN DESPERTARES PARCIALES (`k < N`) — CERO ALUCINACIÓN DE CIERRE:**
> - **Al iniciar la ola:** Emite únicamente **1 línea mínima** (ej. `Iniciando etapa: Autores (17 shards).`) y **detén el turno**.
> - **Cuando un subagente finaliza (`DONE:`) y aún restan trabajadores activos (`k < N`):**
>   1. **`tools=[]` obligatorio:** 🚫 **PROHIBIDO** llamar a `manage_subagents(Action='kill', ...)`, `manage_subagents(Action='kill_all')`, `Get-ChildItem`, `dir`, `run.py`, `view_file` o cualquier herramienta en despertares parciales (salvo excepción explícita de un subagente que reporte `BLOCKED:`).
>   2. **Respuesta mínima de 1 sola línea (NO respuesta vacía):** Antigravity exige texto no vacío cuando `tools=[]`. Emite **exactamente 1 línea** (`Esperando: k/N.`) y **detén inmediatamente tu generación**.
>   3. **🚫 PROHIBIDO SIMULAR O NARRAR ETAPAS FUTURAS:** JAMÁS escribas `"Listo, se completó..."`, `"Iniciando etapa: Jueces Ciegos"`, `"Iniciando etapa: Publicación"` ni `"# 🎓 Curso Creado y Publicado con Éxito"` en un turno de espera. Solo puedes emitir el mensaje final de curso publicado en el turno inmediatamente posterior a recibir **`Command exited with code 0`** real de `run.py --stage publish` con las métricas reales del QA Evaluator en `stdout`.
> - **Al completar `N/N` (verificado por haber recibido `N` mensajes `SYSTEM_MESSAGE` con `DONE:` distintos):** Emite **1 línea** de cierre (ej. `Listo, se completó la etapa de Autores (17/17).`) y ejecuta el Batch-Kill para pasar a la siguiente etapa.
> - **Si un subagente reporta `BLOCKED:` / `CIRCUIT BREAKER`:** Avisa en **1 línea** qué unidad se bloqueó y gestiona su reparación.

> [!IMPORTANT]
> **BATCH-KILL EN BARRERA N/N (CERTIFICACIÓN + FRESCURA EN DISCO):**
> Solo cuando **todos** los `N/N` subagentes de la ola (`Pendientes: []`) hayan reportado `DONE:` en su turno terminal `PLANNER_RESPONSE` (o `BLOCKED:`/`CIRCUIT BREAKER`) **y** los artefactos de la ola estén certificados y frescos en disco respecto a `dispatched_at` (para `authors`/`shards`/`repair`: `<shard_id>.cert.json` con `passed_50_seeds: true` y `<shard_id>.json` con `compiled_status: "PASS"`, nunca `"FAIL"`; para `judges.json`: `judge_responses_XX.json` con `mtime >= dispatched_at`; para `cta_parts`/`cta.json`: `pass_cta_<part_id>.json` = `PASS` con `mtime >= dispatched_at`), el Director debe ejecutar un **único** apagado en lote:
> ```python
> manage_subagents(Action='kill_all')
> ```
> El hook `PreToolUse` (`c2c_hook_guard.py`, configurado con `manage_subagents` y `run_command` en `.agents/hooks.json` / `.agents/hooks.template.json`) ignora salidas `GENERIC` de `read_file` para evitar falsos positivos y bloqueará cualquier `kill`, `kill_all`, transición `run.py --stage` prematura (`cta`, `cta-reduce`, `cta-apply`, `cta-merge`, `shard`, `templates`, `build`, `verify`, `publish`, `repair-matrix`, `judge-compare`, `rejudge-compare`, `gates`, `certify`, `unlock`) o `dispatch.py` (`dispatch-cta-reduce`, `dispatch-authors`, `dispatch-judges`) mientras queden subagentes sin `DONE:`/`BLOCKED:` o artefactos sin certificar/frescos (salvo `kill` individual sobre UUIDs cuyo `transcript.jsonl` contenga `BLOCKED:` explícito). Nota operativa: Antigravity carga cambios de `.agents/hooks.json` al iniciar nuevas invocaciones/subagentes, no a mitad de turno.

> [!NOTE]
> **GESTIÓN DE STRAGGLERS A LOS 10 MINUTOS (WATCHDOG ACTIVO):**
> Si un subagente de shard o reparación supera el timer del watchdog sin reportar `DONE:` y el watchdog despierta al Director:
> 1. El Director debe leer el transcript del subagente (`transcript.jsonl`) para auditar su estado real.
> 2. **Si el subagente está convergiendo y terminando sus últimas verificaciones:** déjalo continuar y reprograma el watchdog.
> 3. **Si el subagente está ciclado o atascado:** envíale un mensaje de ayuda directa analítica (`send_message(Recipient=cid, Message="...")`) indicándole la causa exacta del bloqueo y cómo destrabarlo.
> 4. **Resumen al usuario:** Únicamente cuando venza este timer, emite **1 resumen breve** de la situación (`k/N` completados, cuáles siguen pendientes y la acción tomada).

> [!TIP]
> **MANEJO DE I/O EN WINDOWS (NTFS) Y PREVENCIÓN DE SONDEOS ERRÓNEOS:**
> 1. **Búfer de Escritura NTFS:** Tras recibir `DONE:` de una etapa o subagente, espera un retardo preventivo de 500 ms antes de invocar la siguiente etapa CLI o leer archivos para asegurar el vaciado (*flush*) del búfer del sistema de archivos NTFS en Windows.
> 2. **Sondeo de Tareas Asíncronas vs Subagentes:** NUNCA llames a `manage_task(Action='kill', ...)` o `manage_task(Action='status', ...)` sobre subagentes; los subagentes se gestionan EXCLUSIVAMENTE con `manage_subagents(Action='kill', ConversationIds=[...])`. NUNCA sondees o intentes matar tareas en estado `DONE`.
> 3. **Paginación Inteligente en `edit_file`:** Prohibido aplicar `edit_file` sobre bloques mayores a 30 líneas tras lecturas parciales truncadas; exige leer previamente con `read_file` el bloque específico indicando líneas exactas (`StartLine` y `EndLine`).
> 4. **Pre-Validación Psicométrica [R-15]:** La longitud en caracteres de las 4 opciones visibles no debe diferir en más de un 15% antes de llamar a `write_file` ([R-15]).

Solo cuando se satisfaga la condición de barrera completa (`N/N` trabajadores de la ola reportaron `DONE:`, o `BLOCKED:`, o tras la resolución de rezagados), el Director procede a ejecutar la etapa siguiente del runner.

---

## 🛡️ Dieta Estricta del Director y Cero Depuración Manual

Para evitar saturar el contexto del chat y consumir tokens en inspecciones redundantes:
1. **Bloqueo Pre-Tool (`c2c_hook_guard.py`)**: Mientras exista `.c2c_subagent_lock.json`, el hook previene activamente que el Director lea o modifique archivos de código de shards (`*_data.py`, `shard_fixes/*.py`), respuestas masivas de jueces (`judge_responses_*.json`) o scripts internos del skill (`run.py`, `prepare.py`, `ingest.py`, `dispatch.py`).
2. **Delegación de Reparaciones (`c2c_repair` vía `run_workflow`)**:
   - Si `gates`, `certify`, `publish` o un Circuit Breaker requieren reparaciones adicionales fuera del pase automático de `post_cta_pipeline`, genera el manifiesto consolidado por shard y ejecútalo en paralelo con `run_workflow` (`mode="repair"`):
     ```powershell
     & ".venv\Scripts\python.exe" .agents/skills/content-to-course/dispatch.py dispatch-repair --work-dir <work_dir> --ids <CID1> <CID2>
     ```
     ```python
     run_workflow(
         ScriptPath="<workflow_script_path absoluto devuelto por --stage bootstrap>",
         Description="Ejecutar ola de reparaciones C2C consolidada por shard",
         Args={"work_dir": "<work_dir>", "mode": "repair"},
     )
     ```
   - `dispatch-repair` detecta automáticamente fallos de compilación, plantillas faltantes (`work/templates/<CID>.json`) o *circuit breakers* activos, **limpia automáticamente los archivos de bloqueo en `.check_attempts/`** del shard afectado y **consolida las reparaciones por `shard_id`** (1 subagente `c2c_repair` por shard afectado leyendo `repair_*_data.md`). El Director NUNCA edita código a mano. Si la reparación modifica plantillas, ejecuta `--stage rejudge --ids ...` seguido de `run_workflow(..., Args={"work_dir": "<work_dir>", "mode": "judges"})` y `--stage rejudge-compare`.
3. **Liberación de Bloqueo**: Al concluir la publicación exitosa con `run.py --stage publish`, el archivo `.c2c_subagent_lock.json` se elimina automáticamente. En caso de aborto anticipado, ejecutar `python .agents/skills/content-to-course/run.py --stage unlock --work-dir <work_dir>`.

---

## 🚀 Runbook de Ejecución Rápida (<90s Bootstrap)

### Paso 0: Arranque Atómico (Fast Bootstrap — Turno 1)
Ejecuta la inicialización completa en un único comando consolidado (sin explorar archivos antes):
```powershell
& ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage bootstrap --course-id <id> --sources <ruta_o_directorio_fuente> --cta-mode <direct|mapreduce> --granularity <standard|fine|coarse> --director-id <CONVERSATION_ID>
```
Este comando ejecuta en `< 1s`:
- Normalización automática de `--course-id` y conteo instantáneo de páginas PDF sin rasterizado.
- Creación de estructura en `courses/<course_id>/work`, manifiestos iniciales (`pre_cta_manifest.json`, `ingestion_manifest.json`) y delta si aplica `--append`.
- Creación de especificaciones de tipos (`<work_dir>/dispatch/types/*.json`).
- Inicialización de `.c2c_subagent_lock.json` con metadatos de gobernanza formal.
- Generación inmediata de las órdenes de trabajo de CTA (`Subagents` en el JSON de salida de `bootstrap`).

### Paso 1: Lanzamiento de CTA y Registro Diferido de Subagentes (Turnos 2, 3 y 4)
1. **Turno 2**: Lee en paralelo los archivos de `<work_dir>/dispatch/types/*.json` listados en `type_spec_files` (solo lecturas).
2. **Turno 3**: Registra **solo** `c2c_cta_architect` vía `define_subagent`, invoca `invoke_subagent` (`Model="inherit"`) para cada elemento de `Subagents` devuelto por `bootstrap`, y agenda el watchdog a 7 minutos mediante `schedule` (`DurationSeconds=420` = 7 min, `Prompt="Auditar progreso CTA"`).
3. **Turno 4**: Mientras los architects trabajan, registra en un único turno paralelo los tipos restantes (`c2c_shard_author`, `c2c_judge`, `c2c_repair`, `c2c_cta_harmonizer` si existe) con `define_subagent`, y entra a la barrera.
4. Aplica el Protocolo de Barrera Silenciosa hasta recibir `DONE:` de todos los arquitectos CTA (`1/1` en modo `direct` o `N/N` `part_XX` en modo `mapreduce`).

### Paso 2: Validación Curricular Simétrica (CTA -> CTA-Reduce -> CTA-Apply) y Sharding
1. Certifica el currículo compilado. En modo `mapreduce` (o bajo `--append`), el runner procesa las partes, despacha `c2c_cta_harmonizer` (`run.py --stage cta-reduce`) y consolida las directivas mediante `run.py --stage cta-apply` produciendo `cta.json`:
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage cta --work-dir <work_dir>
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage cta-apply --work-dir <work_dir>
   ```
2. Realiza la partición ponderada en shards (aislando cada `Hab-*` en un shard exclusivo y asignando todos los shards en **1 sola ola** ordenada *Heaviest-First*):
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage shard --work-dir <work_dir>
   ```

### Paso 3 y 4: Ejecución Determinista Post-CTA con `run_workflow` (VÍA POR DEFECTO)
1. **Orquestación Determinista en Código (`workflows/c2c_wave_workflow.py` — OBLIGATORIA POR DEFECTO):**
   Una vez certificado `cta.json` (tras `cta-apply`), ejecuta **toda la secuencia post-CTA** (`shard -> dispatch-authors -> parallel(authors) -> templates -> build -> dispatch-judges -> parallel(judges) -> judge-compare -> gates`, con hasta 1 pase consolidado de reparación por shard y re-arbitraje quirúrgico) en una sola llamada a `run_workflow`, sin despertares parciales del Director:
   ```python
   run_workflow(
       ScriptPath="<workflow_script_path absoluto devuelto por --stage bootstrap>",
       Description="Ejecutar pipeline post-CTA C2C (Autores -> Templates -> Build -> Jueces -> Gates)",
       Args={"work_dir": "<work_dir>", "mode": "post_cta_pipeline"},
   )
   ```
   *(También admite olas individuales con `mode="authors"`, `"judges"` o `"repair"`. Las reglas estáticas viven solo en `system_prompts/lean/prompt_*.md`, cada `Prompt` inicial inyecta `[SCOPE-LOCK]` con rutas exactas, y los payloads en disco son datos puros: `author_XX_data.md`, `judge_XX_items.json`, `repair_*_data.md`.)*
2. Al concluir `run_workflow`, ejecuta la certificación y publicación final (Paso 5):
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage certify --work-dir <work_dir> --output-dir courses
   ```
3. *(Fallback únicamente si `run_workflow` no está disponible):* ejecuta `dispatch.py dispatch-authors`, invoca subagentes con `invoke_subagent` respetando la Barrera Reactiva (`Esperando: k/N.`), luego `--stage templates`, `--stage build`, `dispatch-judges`, `--stage judge-compare`, `--stage gates` y `--stage repair-matrix`.
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage rejudge --ids <CID1> <CID2> --work-dir <work_dir>
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage rejudge-compare --work-dir <work_dir>
   ```
5. **Certificación formal obligatoria**: ejecuta `--stage certify` (valida criptográficamente `*.cert.json` en `< 5 ms` para templates y re-ejecuta compuertas deterministas):
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage certify --work-dir <work_dir> --output-dir courses
   ```

### Paso 5: Publicación Final, Certificación de Calidad y Pantalla de Cierre

1. Publica el curso certificado (validando estricto `PublishQualityGateError` con MPRI $\ge 75$ y ZPD $> 0$):
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage publish --work-dir <work_dir> --output-dir courses
   ```
   El cerrojo `.c2c_subagent_lock.json` se libera automáticamente, el motor ejecuta la **Rúbrica Determinista del QA Evaluator** (< 300 ms) y el **Pipeline Auditor Determinista (`c2c-run-auditor`)**, genera los reportes `reports/qa_audits/<course_id>_qa_report.md` (autocontenido) y `reports/c2c_audits/<timestamp>_<course_id>_<conv_id[:8]>/`, y emite ambas telemetrías completas en stdout.

2. > [!IMPORTANT]
   > ### 🎓 Pantalla de Cierre Obligatoria (Presentación de Calidad y Ejecución al Usuario)
   >
   > Al concluir la publicación, el Director **NUNCA** debe limitarse a mostrar solo el tamaño del archivo o la URL genérica sin estadísticas de calidad ni de ejecución. **DEBE presentar obligatoriamente en su respuesta final al usuario las estadísticas completas de la Rúbrica Determinista del QA Evaluator y el Resumen Determinista de Ejecución del Run Auditor emitidos por `--stage publish`**:
   >
   > #### Formato Obligatorio del Mensaje Final:
   >
   > ```markdown
   > # 🎓 Curso Creado y Publicado con Éxito
   >
   > El curso **{Título}** (`{course_id}`) ha completado el pipeline de Content-to-Course y ha sido certificado formalmente bajo los estándares de **Quality Matters (QM)**, **OSCQR** y **Mastery Learning**.
   >
   > ---
   >
   > ### 🏆 Veredicto de Calidad Pedagógica y Psicométrica (Modo Determinista QA Evaluator)
   >
   > - **Calificación Final Certificada:** **{final_score} / 20.0 pts**
   > - **Quality Tier:** **{quality_tier}**
   > - **Mastery Path Readiness Index (`MPRI`):** **{mpri_score} / 100.0** ({mpri_tier})
   > - **Risk Score Global:** **{risk_score} / 100.0** (Bajo riesgo / Limpio)
   > - **Penalizaciones Duras:** **-{hard_penalties} pts** (0 deducciones activas)
   >
   > #### 📊 1. Rúbrica Normativa QM-OSCQR (Escala 20.0 Puntos)
   >
   > | Dimensión | Puntuación | Máximo | Calificación | Estado |
   > | :--- | :---: | :---: | :---: | :---: |
   > | **D1: Arquitectura Curricular y Topología DAG** | **{d1}** | 4.0 | {d1_pct}% | ✅ Impecable |
   > | **D2: Calidad Psicométrica y Reactivos** | **{d2}** | 5.0 | {d2_pct}% | ✅ Impecable |
   > | **D3: Andamiaje y Pistas Socráticas** | **{d3}** | 5.0 | {d3_pct}% | ✅ Impecable |
   > | **D4: Alineación Instruccional y ZPD** | **{d4}** | 4.0 | {d4_pct}% | ✅ Impecable |
   > | **D5: Ergonomía Técnica y KaTeX** | **{d5}** | 2.0 | {d5_pct}% | ✅ Impecable |
   > | **Penalizaciones Duras** | **0.0** | - | - | ✅ Sin penalizaciones |
   > | **TOTAL CERTIFICADO** | **{final_score}** | **20.0** | **{total_pct}%** | 🏆 **{quality_tier}** |
   >
   > #### 🎯 2. Pilares de Preparación para el Dominio (MPRI: 100.0 Puntos)
   >
   > | Pilar de Dominio del Estudiante | Puntaje MPRI | Máximo | Calificación |
   > | :--- | :---: | :---: | :---: |
   > | **1. Progresión Adaptativa ZPD y Bloom** | **{p1}** | 20.0 | {p1_pct}% |
   > | **2. Modalidad de Evocación y Anti-Gaming** | **{p2}** | 20.0 | {p2_pct}% |
   > | **3. Integridad del Salvavidas Socrático (3-Strikes)** | **{p3}** | 25.0 | {p3_pct}% |
   > | **4. Alineación Diagnóstica en FeedbackToast** | **{p4}** | 15.0 | {p4_pct}% |
   > | **5. Topología DAG e Interleaving (Quiz/Test)** | **{p5}** | 10.0 | {p5_pct}% |
   > | **6. Ergonomía Cognitiva y Sintaxis KaTeX** | **{p6}** | 10.0 | {p6_pct}% |
   > | **TOTAL MPRI** | **{mpri_score}** | **100.0** | **{mpri_score}% ({mpri_tier})** |
   >
   > #### 🔬 3. Telemetría Psicométrica y Resumen de Linters
   > - **Sintaxis KaTeX:** 0 errores críticos (delimitadores balanceados, llaves cerradas, renderizado 100% limpio).
   > - **Andamiaje Socrático:** 100% de reactivos con 3 a 5 pistas socráticas progresivas (0% boilerplate Mad-Libs, 0% envenenamiento).
   > - **Cobertura Diagnóstica:** 100% de distractores con `error_rationale` diagnóstico ({uniq}% unicidad, 0 multiplicadores sintéticos).
   > - **Modalidad Cognitiva:** {mc7}% MC7, {fib}% FIB, {ms}% MS ({active}% evocación activa y discriminación condicional).
   > - **Progresión ZPD:** 100% de competencias cubiertas en las 3 bandas de dificultad (`easy`, `medium`, `hard`).
   > - **Arbitraje Ciego Epistémico:** 100% de concordancia de jueces independientes ({judged}/{judged} ítems consensuados).
   >
   > ---
   >
   > ### ⏱️ 4. Resumen Determinista de Ejecución (Run Auditor)
   >
   > - **Tiempo Total de Pared:** **{wall_min} min** ({wall_sec}s) | **Cómputo Acumulado:** {comp_min} min | **Speedup Paralelo:** **{speedup}x**
   > - **Subagentes Desplegados:** **{sub_total}** | **Intervenciones Manuales:** {interventions}
   > - **Consumo de Tokens:** **{tot_tok} totales** (**{act_tok} activos**: In={in_tok}, Out={out_tok}, Think={think_tok} | Cache={cache_tok})
   > - **Costo Estimado Total (Gemini 4 Hydrogen):** **\${total_cost_usd} USD** (\${usd_per_q} USD/preg | \${usd_per_comp} USD/comp | In=\${in_usd} @ \$1.50/1M, Out+Think=\${out_usd} @ \$7.50/1M, Cache=\${cache_usd} @ \$0.075/1M)
   > - **Unit Economics:** {tok_per_q} tok/preg ({act_tok_per_q} activos/preg) | {sec_per_q} s/preg ({qpm} preg/min)
   >
   > | Etapa / Sección | Duración / Pared | Costo (USD) | Recursos y Resultado |
   > | :--- | :---: | :---: | :--- |
   > | **Stage 0 (Bootstrap/Prep)** | {prep_dur}s | \$0.0000 | CLI |
   > | **Stage 1A (Visión)** | {s1a_wall}s | \${s1a_usd} | {s1a_agents} agentes / {s1a_tok} tok activos |
   > | **Stage 1B (CTA)** | {s1b_wall}s | \${s1b_usd} | {s1b_agents} agentes / {s1b_tok} tok activos ({total_comps} comps) |
   > | **Stage 2 (Sharding)** | {shard_dur}s | \$0.0000 | {shards_count} shards |
   > | **Stage 3 (Autores)** | min={s3_min}s / med={s3_med}s / max={s3_max}s | \${s3_usd} | Straggler: {straggler} / {s3_tok} tok activos |
   > | **Stage 3B (Reparaciones)** | {s3b_max}s | \${s3b_usd} | {s3b_count} reparaciones / {s3b_tok} tok activos |
   > | **Stage 4 (Templates/Build)** | {s4_dur}s | \$0.0000 | {total_questions} reactivos |
   > | **Stage 5 (Blind Judges)** | {s5_wall}s | \${s5_usd} | {s5_judges} jueces / {s5_items} ítems ({s5_agree}% acuerdo) |
   > | **Stage 6 (Publish)** | {pub_dur}s | \$0.0000 | CLI + QA + Run Auditor |
   > | **Orquestador (Director)** | {wall_sec}s | \${orch_usd} | Subagente raíz + workflows |
   > | **TOTAL CORRIDA** | **{wall_sec}s** | **\${total_cost_usd} USD** | **Gemini 4 Hydrogen** |
   >
   > ---
   >
   > ### 📁 Artefactos Generados y Enlace Directo
   > - **Archivo del Curso (JSON):** `courses/{course_id}.json` ({size_mb} MB, {total_questions} reactivos en {total_comps} competencias)
   > - **Análisis Curricular CTA:** `courses/competence_analysis_{course_id}.md`
   > - **Informe de Calidad QA (Markdown autocontenido):** `reports/qa_audits/{course_id}_qa_report.md`
   > - **Informe Run Auditor (Markdown):** `reports/c2c_audits/{run_dir}/report.md`
   > - **Telemetría Run Auditor (JSON):** `reports/c2c_audits/{run_dir}/telemetry.json`
   > - **Benchmark Histórico:** `reports/c2c_audits/historical_benchmark.md`
   > - **URL de Interacción Directa:** http://localhost:3000/#/course/{course_id}
   > ```
