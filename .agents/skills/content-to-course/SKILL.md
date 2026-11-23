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
  comps_per_shard:
    type: integer
    description: Optional override for max competencies per shard (e.g. 2 or 1) forwarded to --stage shard / run_workflow
    required: false
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
> ## ⚡ REGLA CERO: ARRANQUE ATÓMICO EN 2 TURNOS CON AGENTES PRE-CARGADOS (PROHIBIDO EXPLORAR SCRIPTS O CONTAR PÁGINAS)
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
> 4. **Sincroniza el plugin global `c2c-agents`** (`~/.gemini/config/plugins/c2c-agents/agents/*.md`) y genera los 5 archivos de tipos en `<work_dir>/dispatch/types/{c2c_cta_architect,c2c_cta_harmonizer,c2c_shard_author,c2c_judge,c2c_repair}.json`.
> 5. **Ejecuta internamente `dispatch_cta(pointer=True)`**, devolviendo en su JSON de salida (`stdout`) `subagents_preloaded: true`, `workflow_script_path`, `type_spec_files` y el arreglo `Subagents` listo para invocar.
>
> ### Secuencia Exacta de Arranque (Fast-Path en 2 Turnos `< 3s` con Plugin `c2c-agents` pre-cargado):
> - **Turno 1 (inmediatamente tras leer `SKILL.md`)**: Ejecuta **únicamente** este comando (ajustando `--course-id`, `--sources`, `--cta-mode` y `--granularity` según el pedido del usuario):
>   ```powershell
>   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage bootstrap --course-id <id> --sources <ruta_o_directorio_fuente> --cta-mode <direct|mapreduce> --granularity <standard|fine|coarse> --director-id <CONVERSATION_ID>
>   ```
>   *(Si el usuario no especifica modo o granularidad, usa `--cta-mode mapreduce --granularity standard` (default). Si el usuario pide explícitamente `cta_direct`/`direct`, pasa `--cta-mode direct`: la instrucción del usuario SIEMPRE prevalece y NUNCA se promueve a mapreduce por número de páginas o archivos. Si es extensión incremental de un curso existente, añade `--append --base-course courses/<id>.json`).*
> - **Turno 2 (Fast-Path Cero-Define — cuando `c2c_cta_architect`, `c2c_cta_harmonizer`, `c2c_shard_author`, `c2c_judge` y `c2c_repair` YA aparecen en tu bloque `<subagents>`)**:
>   - 🚫 **PROHIBIDO leer `type_spec_files` ni llamar a `define_subagent`** cuando los 5 subagentes C2C ya están pre-cargados en `<subagents>` por el plugin `c2c-agents`.
>   - Llama **DIRECTAMENTE** a `run_workflow` en el Turno 2 (`< 2s`):
>   - **Modo 1-paso completo (`mode="full_pipeline"`):** corre de frente CTA -> Harmonizer -> Sharding -> Autores -> Templates -> Build -> Jueces -> Gates -> hasta 2 rondas de Repair+Rejudge automáticas.
>   - **Modo en 2 fases (`mode="cta_pipeline"` y luego `mode="post_cta_pipeline"`):** útil cuando quieres inspeccionar `cta.json` antes de lanzar Stage 2–6B.
>   ```python
>   run_workflow(
>       ScriptPath="<workflow_script_path absoluto devuelto por --stage bootstrap>",
>       Description="Ejecutar pipeline C2C completo (CTA -> Autores -> Jueces -> Repairs)",
>       Args={"work_dir": "<work_dir>", "mode": "full_pipeline"},  # o "cta_pipeline"
>   )
>   ```
>   *(Gobernanza unificada: **100% `run_workflow`**, nunca mezcles `invoke_subagent` ni `manage_subagents` manuales en el flujo estándar).*
> - **Fallback (solo si los 5 agentes C2C NO aparecen en `<subagents>` en esta sesión)**: Lee en paralelo `type_spec_files` en Turno 2, regístralos vía `define_subagent` en Turno 3, y lanza `run_workflow` en Turno 4.

---

> [!IMPORTANT]
> ## ROL FUNDAMENTAL: LA CONVERSACIÓN PRINCIPAL ES EL DIRECTOR DE PROYECTO
>
> La conversación principal actúa **exclusivamente como Directora de Proyecto / Orquestadora General**. Su responsabilidad es coordinar el flujo de trabajo, invocar las etapas del runner CLI (`run.py`), inspeccionar los presupuestos y artefactos de control, y **delegar todas las tareas intensivas en olas mediante `run_workflow` (`workflows/c2c_wave_workflow.py`)** sin ediciones manuales ni gobernanza híbrida.
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
> - **Orquestación de Olas 100% en Código con `run_workflow` (`workflows/c2c_wave_workflow.py`)**: Todo el pipeline agéntico —desde ejecución completa en 1 llamada (`full_pipeline`: CTA + Harmonizer + Autores + Jueces + hasta 2 rondas de `repair_and_rejudge` integradas) hasta ejecución en fases (`cta_pipeline`, `cta` + `cta_harmonize`, `post_cta_pipeline`, `authors`/`judges`/`repair`, y `repair_and_rejudge`)— se ejecuta exclusivamente vía `run_workflow(ScriptPath="<workflow_script_path absoluto devuelto por --stage bootstrap>", Args={...})`. Incorpora semáforo anti-`429` (`max_concurrency=12` + jitter), auto-retry en colapsos silenciosos `< 5s`/`UNKNOWN`, y validación `check_runs >= 1` en `Repair Engineer`, eliminando la gobernanza híbrida con `invoke_subagent` y `manage_subagents(kill_all)`.
> - **Fail-Total en Compilador (`--fail-total`)**: `compile_shard.py` opera con `--fail-total` tanto en autoría como en reparación para abortar ante errores fatales sin tolerar compilaciones inconsistentes.
> - **Herramientas Nativas Estándar**: Subagentes y runner operan con herramientas nativas de plataforma (`read_file`, `write_file`, `edit_file`, `run_command`, `send_message`) con soporte retrocompatible.
> - **Juez Epistémico 1-Seed con Dominancia Bayesiana ($\alpha_{\text{Kernel}} = 0$)**: 1 única semilla pre-verificada por plantilla enfocada en suficiencia epistémica y no-giveaway semántico; ninguna objeción heurística revoca una prueba matemática formal.
> - **Protocolo de Cierre Limpio (`run_workflow`) y Barrera Reactiva Silenciosa (`k < N`)**: Al despachar una ola vía `run_workflow`, el Director espera pasivamente su notificación final sin emitir `manage_subagents` ni `manage_task`. El hook `c2c_hook_guard.py` mantiene además la Barrera Reactiva Silenciosa (`k < N`) como salvaguarda para impedir transiciones prematuras mientras haya tareas activas en segundo plano.
> - **Weighted Waves (`1-2 Hab/shard`, `<= 3 Concept/Fact` default o `--comps-per-shard N` opcional)**: Priorización *Heaviest-First*. Por defecto `plan_shards.py` agrupa hasta `2 Hab-*` por shard y hasta `3 C-*/H-*` por shard; si el usuario solicita explícitamente otro tamaño (p. ej. `2` competencias/shard globalmente), el Director pasa `comps_per_shard` en `Args` de `run_workflow` o `--comps-per-shard` en `run.py --stage bootstrap`/`shard`. Para filtrar una ola concreta usa `dispatch.py dispatch-authors --work-dir <work> --wave <N>`. **Regla de espera y remediación consolidada:** espera siempre la finalización de `run_workflow` o `gates` antes de consolidar reparaciones; tras finalizar `gates` + `repair-matrix`, usa `run_workflow` con `mode="repair_and_rejudge"`, nunca despaches reparación con resultados parciales y **nunca** ejecutes `rejudge-compare` mientras una tarea `run_workflow` siga activa en segundo plano.
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

## ⚡ Regla de Oro: Cero Gobernanza Híbrida y Protección de Barreras

El Director de Proyecto debe mantener una interacción conversacional ultra-eficiente (~10–14 turnos en toda la corrida) delegando el ciclo de vida de los subagentes exclusivamente a `run_workflow` (`c2c_wave_workflow.py`).

> [!CAUTION]
> **REGLAS DE ESPERA Y CERO ALUCINACIÓN DE CIERRE:**
> - **Prohibido mezclar `invoke_subagent` o `manage_subagents` manuales** en el flujo estándar: toda ejecución paralela de CTA, CTA Harmonizer, Autores, Jueces y Reparaciones corre encapsulada en `run_workflow`.
> - **🚫 PROHIBIDO SIMULAR O NARRAR ETAPAS FUTURAS:** JAMÁS escribas `"Listo, se completó..."`, `"Iniciando etapa: Jueces Ciegos"`, `"Iniciando etapa: Publicación"` ni `"# 🎓 Curso Creado y Publicado con Éxito"` antes de recibir **`Command exited with code 0`** real de `run.py --stage publish` con las métricas reales del QA Evaluator en `stdout`.
> - **Salvaguarda de `c2c_hook_guard.py` (Silent Reactive Barrier / `k < N`):** El hook `PreToolUse` bloquea cualquier transición `run.py --stage` o `dispatch.py` mientras exista una tarea `run_workflow` o de validación activa en segundo plano, o artefactos sin certificar/frescos en disco respecto a `dispatched_at`. Nota operativa: Antigravity carga cambios de `.agents/hooks.json` al iniciar nuevas invocaciones/subagentes, no a mitad de turno.

> [!TIP]
> **MANEJO DE I/O EN WINDOWS (NTFS) Y PREVENCIÓN DE SONDEOS ERRÓNEOS:**
> 1. **Búfer de Escritura NTFS:** Tras recibir `DONE:` de una etapa o subagente, espera un retardo preventivo de 500 ms antes de invocar la siguiente etapa CLI o leer archivos para asegurar el vaciado (*flush*) del búfer del sistema de archivos NTFS en Windows.
> 2. **Sondeo de Tareas Asíncronas:** NUNCA llames a `manage_task(Action='kill', ...)` o `manage_task(Action='status', ...)` sobre subagentes ni sobre tareas en estado `DONE`; la orquestación de olas vive dentro de `run_workflow`.
> 3. **Paginación Inteligente en `edit_file`:** Prohibido aplicar `edit_file` sobre bloques mayores a 30 líneas tras lecturas parciales truncadas; exige leer previamente con `read_file` el bloque específico indicando líneas exactas (`StartLine` y `EndLine`).
> 4. **Pre-Validación Psicométrica [R-15]:** La longitud en caracteres de las 4 opciones visibles no debe diferir en más de un 15% antes de llamar a `write_file` ([R-15]).

Solo cuando se satisfaga la condición de barrera completa (`N/N` trabajadores de la ola reportaron `DONE:`, o `BLOCKED:`, o tras la resolución de rezagados), el Director procede a ejecutar la etapa siguiente del runner.

---

## 🛡️ Dieta Estricta del Director y Cero Depuración Manual

Para evitar saturar el contexto del chat y consumir tokens en inspecciones redundantes:
1. **Bloqueo Pre-Tool (`c2c_hook_guard.py`)**: Mientras exista `.c2c_subagent_lock.json`, el hook previene activamente que el Director lea o modifique archivos de código de shards (`*_data.py`, `shard_fixes/*.py`), respuestas masivas de jueces (`judge_responses_*.json`) o scripts internos del skill (`run.py`, `prepare.py`, `ingest.py`, `dispatch.py`).
2. **Delegación de Reparaciones (`c2c_repair` vía `run_workflow`)**:
   - Si `gates`, `certify`, `publish` o un Circuit Breaker requieren reparaciones adicionales fuera del pase automático de `post_cta_pipeline`, **invoca directamente `run_workflow` con `mode="repair_and_rejudge"`** (sin ejecutar `dispatch.py dispatch-repair` manualmente antes, ya que `c2c_wave_workflow.py` lo invoca internamente de forma consolidada). Reserva el uso manual de `dispatch.py dispatch-repair` **únicamente** cuando ejecutes la ola aislada `mode="repair"`:
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
   - `dispatch-repair` detecta automáticamente fallos de compilación, plantillas faltantes (`work/templates/<CID>.json`) o *circuit breakers* activos, **limpia automáticamente los archivos de bloqueo en `.check_attempts/`** del shard afectado y **consolida las reparaciones por `shard_id`** (1 subagente `c2c_repair` por shard afectado leyendo `repair_*_data.md`). El Director NUNCA edita código a mano. Si usaste `mode="repair"` aislado y la reparación modifica plantillas, ejecuta `--stage rejudge --ids ...` seguido de `run_workflow(..., Args={"work_dir": "<work_dir>", "mode": "judges"})` y `--stage rejudge-compare`.
   - **Checkpoint de reanudación automática (`work/.rejudge_pending.json`):** En `repair_and_rejudge`, si la fase `Repair + build` concluye pero el *Surgical Rejudge* aborta por cuota (`HTTP 429`), al relanzar `mode="repair_and_rejudge"` el workflow reanuda directamente en `--stage rejudge` sin volver a ejecutar los Repair Engineers (usa `force_repair=True` en `Args` solo si necesitas forzar nueva edición).
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

### Paso 1: Lanzamiento Directo con `run_workflow` (Turno 2 — `< 2s` con Agentes Pre-Cargados)
1. **Turno 2 (Fast-Path con `c2c-agents` pre-cargados en `<subagents>`)**:
   Como `c2c_cta_architect`, `c2c_cta_harmonizer`, `c2c_shard_author`, `c2c_judge` y `c2c_repair` ya vienen pre-cargados en la sesión desde `~/.gemini/config/plugins/c2c-agents/agents/*.md`, **NO leas `type_spec_files` ni llames a `define_subagent`**. Lanza directamente `run_workflow` (`mode="full_pipeline"` o `mode="cta_pipeline"`):
   ```python
   run_workflow(
       ScriptPath="<workflow_script_path absoluto devuelto por --stage bootstrap>",
       Description="Ejecutar pipeline C2C completo (CTA -> Autores -> Jueces -> Repairs)",
       Args={"work_dir": "<work_dir>", "mode": "full_pipeline"},  # o "cta_pipeline"
   )
   ```
2. **Fallback (solo si los tipos `c2c_*` no aparecen en `<subagents>`)**:
   Lee en paralelo `<work_dir>/dispatch/types/*.json`, regístralos vía `define_subagent` y lanza `run_workflow`.

### Paso 2: Validación Curricular Simétrica (CTA) y Sharding Opcional
1. Si usaste `mode="cta"` en lugar de `cta_pipeline`, ejecuta `run.py --stage cta` y, si `dispatch/cta_reduce.json` se genera, corre `run_workflow(..., Args={"work_dir": "<work_dir>", "mode": "cta_harmonize"})` seguido de `run.py --stage cta`. (`mode="cta_pipeline"` ya automatiza todo este flujo).
2. *(Opcional si deseas inspeccionar shards antes de Stage 3):* puedes correr `run.py --stage shard --work-dir <work_dir>` (agregando `--comps-per-shard 2` si el usuario pidió tope de 2 competencias por shard). De lo contrario, `post_cta_pipeline` ejecuta Stage 2 directamente.

### Paso 3 y 4: Ejecución Determinista Post-CTA con `run_workflow` (VÍA ÚNICA)
1. **Orquestación Determinista en Código (`workflows/c2c_wave_workflow.py` — OBLIGATORIA):**
   Una vez certificado `cta.json`, ejecuta **toda la secuencia post-CTA** (`shard -> dispatch-authors -> parallel(authors) -> templates -> build -> dispatch-judges -> parallel(judges) -> judge-compare -> gates`, con semáforo anti-`429`, auto-retry en colapsos silenciosos y hasta 1 pase consolidado de reparación por shard con `check_runs >= 1` + re-arbitraje quirúrgico) en una sola llamada a `run_workflow`:
   ```python
   run_workflow(
       ScriptPath="<workflow_script_path absoluto devuelto por --stage bootstrap>",
       Description="Ejecutar pipeline post-CTA C2C (Autores -> Templates -> Build -> Jueces -> Gates)",
       Args={
           "work_dir": "<work_dir>",
           "mode": "post_cta_pipeline",
           # Opcional solo si el usuario solicita un tope distinto (ej. 2 comps/shard):
           # "comps_per_shard": 2,
           # "max_concurrency": 12,
       },
   )
   ```
   *(También admite olas individuales con `mode="cta"`, `"cta_harmonize"`, `"authors"`, `"judges"` o `"repair"`. Si `gates` posteriores o `certify` detectan fallos adicionales, ejecuta directamente `run_workflow` con `mode="repair_and_rejudge"` — sin ejecutar `dispatch.py dispatch-repair` manualmente antes, nunca mezcles `invoke_subagent` manual ni ejecutes `rejudge-compare` mientras `run_workflow` siga activo en segundo plano).*
2. Al concluir `run_workflow`, ejecuta la certificación y publicación final (Paso 5):
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
   > | **D4: Alineación Instruccional y ZPD (Piso Bloom Expected: `{bloom_floor}` \| Real Generado: `{bloom_idx}` / 5.0)** | **{d4}** | 4.0 | {d4_pct}% | ✅ Impecable |
   > | **D5: Ergonomía Técnica y KaTeX** | **{d5}** | 2.0 | {d5_pct}% | ✅ Impecable |
   > | **Penalizaciones Duras** | **0.0** | - | - | ✅ Sin penalizaciones |
   > | **TOTAL CERTIFICADO** | **{final_score}** | **20.0** | **{total_pct}%** | 🏆 **{quality_tier}** |
   >
   > #### 🎯 2. Pilares de Preparación para el Dominio (MPRI: 100.0 Puntos)
   >
   > | Pilar de Dominio del Estudiante | Puntaje MPRI | Máximo | Calificación |
   > | :--- | :---: | :---: | :---: |
   > | **1. Progresión Adaptativa ZPD y Bloom (Piso Expected: `{bloom_floor}` \| Real Generado: `{bloom_idx}` / 5.0 — {bloom_tier})** | **{p1}** | 20.0 | {p1_pct}% |
   > | **2. Modalidad de Evocación y Anti-Gaming** | **{p2}** | 20.0 | {p2_pct}% |
   > | **3. Integridad del Salvavidas Socrático (3-Strikes)** | **{p3}** | 25.0 | {p3_pct}% |
   > | **4. Alineación Diagnóstica en FeedbackToast** | **{p4}** | 15.0 | {p4_pct}% |
   > | **5. Topología DAG e Interleaving (Quiz/Test)** | **{p5}** | 10.0 | {p5_pct}% |
   > | **6. Ergonomía Cognitiva y Sintaxis KaTeX** | **{p6}** | 10.0 | {p6_pct}% |
   > | **TOTAL MPRI** | **{mpri_score}** | **100.0** | **{mpri_score}% ({mpri_tier})** |
   > | **📊 Piso Bloom Expected vs. Real Generado (1–5)** | **Real: `{bloom_idx}`** | **Piso Expected: `{bloom_floor}`** | **Tier: `{bloom_tier}` (`Analyze+Evaluate`: `{bloom_sup_pct}%`)** |
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
   > - **Costo Estimado Total (Gemini 4 Hydrogen):** **\${total_cost_usd} USD** (\${usd_per_q} USD/preg | \${usd_per_comp} USD/comp | In=\${in_usd} @ \$1.50/1M, Out+Think=\${out_usd} @ \$7.50/1M, Cache=\${cache_usd} @ \$0.08/1M)
   > - **Unit Economics:** {tok_per_q} tok/preg ({act_tok_per_q} activos/preg) | {sec_per_q} s/preg ({qpm} preg/min)
   >
   > | Etapa / Sección | Duración / Pared | Costo (USD) | Recursos y Resultado |
   > | :--- | :---: | :---: | :--- |
   > | **Stage 0 (Bootstrap/Prep)** | {prep_dur}s | \$0.00 | CLI |
   > | **Stage 1A (Visión)** | {s1a_wall}s | \${s1a_usd} | {s1a_agents} agentes / {s1a_tok} tok activos |
   > | **Stage 1B (CTA)** | {s1b_wall}s | \${s1b_usd} | {s1b_agents} agentes / {s1b_tok} tok activos ({total_comps} comps) |
   > | **Stage 2 (Sharding)** | {shard_dur}s | \$0.00 | {shards_count} shards |
   > | **Stage 3 (Autores)** | min={s3_min}s / med={s3_med}s / max={s3_max}s | \${s3_usd} | Straggler: {straggler} / {s3_tok} tok activos |
   > | **Stage 3B (Reparaciones)** | {s3b_max}s | \${s3b_usd} | {s3b_count} reparaciones / {s3b_tok} tok activos |
   > | **Stage 4 (Templates/Build)** | {s4_dur}s | \$0.00 | {total_questions} reactivos |
   > | **Stage 5 (Blind Judges)** | {s5_wall}s | \${s5_usd} | {s5_judges} jueces / {s5_items} ítems ({s5_agree}% acuerdo) |
   > | **Stage 6 (Publish)** | {pub_dur}s | \$0.00 | CLI + QA + Run Auditor |
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
