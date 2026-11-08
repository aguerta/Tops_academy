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

# Content-to-Course Antigravity Skill (C2C v4.0 Formal Mas con Menos Architecture)

A universal, subject-agnostic educational engineering pipeline that converts raw academic materials (Beamer presentations, handwritten OneNote notes, statistical software exports, and high-resolution chalkboard images) into fully playable, interactive Top's Academy courses in **≤ 12 minutes** for a standard 20-competency curriculum under the "Más con Menos" (-65% tokens) formal paradigm.

---

> [!CAUTION]
> ## ⚡ REGLA CERO: ARRANQUE ATÓMICO EN 3 TURNOS (PROHIBIDO EXPLORAR SCRIPTS O CONTAR PÁGINAS)
>
> En cuanto leas este `SKILL.md`, tu **Turno 1** debe ser **EXCLUSIVAMENTE** ejecutar el comando `--stage bootstrap`.
> - 🚫 **PROHIBIDO** ejecutar `Get-ChildItem`, `dir`, `ls` sobre `.agents/skills/content-to-course/` o sobre `content/`.
> - 🚫 **PROHIBIDO** ejecutar `run.py --help`, `dispatch.py --help`, `prepare.py --help` o `ingest.py --help`.
> - 🚫 **PROHIBIDO** usar `read_file`, `view_file` o `python -c "with open(...)"` para inspeccionar `run.py`, `prepare.py`, `ingest.py`, `dispatch.py` o cualquier otro script `.py` del skill (bloqueado activamente por `c2c_hook_guard.py`).
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
> - **Turno 3 (arranque mínimo, solo el CTA Architect)**: En **un único turno paralelo**, realiza únicamente:
>   1. **UNA** llamada a `define_subagent` para `c2c_cta_architect` (usando exactamente `Name`, `Description`, `SystemPrompt`, `EnableWriteTools=true`, `EnableMCPTools=false`, `EnableSubagentTools=false` de su JSON). **NO registres aún los demás tipos**: copiar sus system prompts (~14 KB) cuesta ~20 s de generación.
>   2. Todas las llamadas a `invoke_subagent` (`Model="flash"`, `Workspace="inherit"`) para cada elemento del arreglo `Subagents` que ya te devolvió `bootstrap` en el Turno 1 (**NO ejecutes `dispatch.py dispatch-cta` de nuevo**).
>   3. Una llamada a `schedule` (`DurationSeconds=420` = 7 min, `Prompt="Auditar progreso CTA"`).
> - **Turno 4 (registro diferido mientras los CTA Architects trabajan, ~5-10 min)**: Inmediatamente después, en **un único turno paralelo**, registra con `define_subagent` los tipos restantes (`c2c_shard_author`, `c2c_judge`, `c2c_repair` y `c2c_cta_harmonizer` si su JSON existe) usando los JSON ya leídos en el Turno 2 (**sin volver a leerlos**). Luego detén tu turno y entra en **Barrera Reactiva Silenciosa** (cero herramientas hasta recibir `DONE:` de los architects). Los tipos ya estarán listos antes de `cta-reduce` / `dispatch-authors`.

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
> - **`--lean` por Defecto en Despacho**: System prompts ultra-compactos ($\le 5\text{ KB}$), ahorrando ~65% de tokens de salida y tiempo de generación.
> - **Juez Epistémico 1-Seed con Dominancia Bayesiana ($\alpha_{\text{Kernel}} = 0$)**: 1 única semilla pre-verificada por plantilla enfocada en suficiencia epistémica y no-giveaway semántico; ninguna objeción heurística revoca una prueba matemática formal.
> - **Silent Reactive Barrier Protocol (~12–16 Turnos del Director)**: En despertares reactivos parciales (`k < N`), el Director no ejecuta herramientas, reporta `Progreso de ola: k/N subagentes completados.` y finaliza en `< 2s`.
> - **Weighted Waves (`1 Hab/shard`, olas ≤ 10)**: Priorización *Heaviest-First*: cada habilidad compleja (`Hab-*`) se aísla en su propio shard individual y se despacha a $t=0$.
> - **Compuerta Bloqueante Pre-Publish (`PublishQualityGateError`)**: Publicación bloqueada ante objeciones de jueces no resueltas o incumplimiento psicométrico (MPRI $\ge 75$, ZPD $> 0$, P4 $\ge 13.0/15$, unicidad de racionalizaciones $\ge 30\%$, 0 hard penalties).
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
│ - Aislamiento estricto: máximo 1 Skill (Hab-*) por shard                    │
│ - Conceptos y Hechos contiguos en parejas de 2 (hasta 3 Facts si N >= 30)   │
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
│ - Silent Reactive Barrier: 0 herramientas en mensajes parciales (k < N)    │
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
│ - Libera cerrojo .c2c_subagent_lock.json y reporta URL de visualización     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Regla de Oro: Protocolo de Barrera Reactiva Silenciosa y Auto-Kill Inmediato

El Director de Proyecto debe mantener una interacción conversacional ultra-eficiente (~12–16 turnos en toda la corrida).

> [!IMPORTANT]
> **AUTO-KILL OBLIGATORIO DE CUALQUIER SUBAGENTE AL DECIR 'DONE':**
> En cuanto CUALQUIER subagente (sea `c2c_cta_architect`, `c2c_cta_harmonizer`, `c2c_shard_author`, `c2c_repair`, `c2c_judge`, etc.) reporte `DONE: ...`, el Director **DEBE TERMINARLO INMEDIATAMENTE** llamando a:
> ```python
> manage_subagents(Action='kill', ConversationIds=[subagent_conversation_id])
> ```
> Dejar subagentes terminados vivos en segundo plano genera procesos zombis, sobreconsumo de inferencia y asfixia por cuota de API (HTTP 429). El auto-kill al recibir `DONE:` es una regla universal e inviolable.

> [!CAUTION]
> **COMPORTAMIENTO EN DESPERTARES PARCIALES (`k < N`):**
> Cuando un subagente finaliza y envía `DONE: ...`, la plataforma despierta al Director:
> 1. Ejecuta **únicamente** `manage_subagents(Action='kill', ConversationIds=[subagent_conversation_id])` para apagar al trabajador que concluyó.
> 2. Si aún restan subagentes activos (`k < N`) y el temporizador no ha vencido:
>    - 🚫 **PROHIBIDO** ejecutar `Get-ChildItem`, `dir`, `run.py`, `view_file` o inspecciones exploratorias.
>    - Emite una línea de texto informativo: `Progreso de ola: k/N subagentes completados.` y **detén inmediatamente tu turno** (`< 2s` de ejecución).
>    - La plataforma volverá a despertarte reactivamente cuando el siguiente subagente reporte `DONE:` o cuando la ola completa `N/N` esté lista.

> [!NOTE]
> **GESTIÓN DE STRAGGLERS A LOS 10 MINUTOS (WATCHDOG ACTIVO):**
> Si un subagente de shard o reparación supera los 10 minutos de pared sin reportar `DONE:` y el watchdog despierta al Director:
> 1. El Director debe leer el transcript del subagente (`transcript.jsonl`) para auditar su estado real.
> 2. **Si el subagente está convergiendo y terminando sus últimas verificaciones:** déjalo continuar y reprograma el watchdog.
> 3. **Si el subagente está ciclado o atascado:** envíale un mensaje de ayuda directa analítica (`send_message(Recipient=cid, Message="...")`) indicándole la causa exacta del bloqueo y cómo destrabarlo.

Solo cuando se satisfaga la condición de barrera completa (`N/N` trabajadores de la ola reportaron `DONE:`, o `BLOCKED:`, o tras la resolución de rezagados), el Director procede a ejecutar la etapa siguiente del runner.

---

## 🛡️ Dieta Estricta del Director y Cero Depuración Manual

Para evitar saturar el contexto del chat y consumir tokens en inspecciones redundantes:
1. **Bloqueo Pre-Tool (`c2c_hook_guard.py`)**: Mientras exista `.c2c_subagent_lock.json` (e incluso antes de `bootstrap` para inspecciones `python -c`), el hook previene activamente que el Director lea o modifique archivos de código de shards (`*_data.py`, `shard_fixes/*.py`), respuestas masivas de jueces (`judge_responses_*.json`) o scripts internos del skill (`run.py`, `prepare.py`, `ingest.py`, `dispatch.py`).
2. **Delegación de Reparaciones (`c2c_repair`)**:
   - Si un shard no compila tras los intentos de su autor o activa el Circuit Breaker:
     ```bash
     python .agents/skills/content-to-course/dispatch.py dispatch-repair --work-dir <work_dir> --ids <CID>
     ```
   - `dispatch-repair` detecta automáticamente fallos de compilación, plantillas faltantes (`work/templates/<CID>.json`) o *circuit breakers* activos, **limpia automáticamente los archivos de bloqueo en `.check_attempts/`** del shard afectado y genera la orden para `c2c_repair` (`Model="flash"`).
   - El subagente `c2c_repair` analiza el diagnóstico inyectado y emite la corrección quirúrgica en `work/shards/<shard_id>_data.py` o `work/shards/shard_fixes/<CID>.py`, la cual es incorporada de inmediato por `compile_shard.py`. El Director NUNCA edita código a mano.
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
2. **Turno 3**: Registra **solo** `c2c_cta_architect` vía `define_subagent`, invoca `invoke_subagent` (`Model="flash"`) para cada elemento de `Subagents` devuelto por `bootstrap`, y agenda el watchdog a 7 minutos mediante `schedule` (`DurationSeconds=420` = 7 min, `Prompt="Auditar progreso CTA"`).
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

### Paso 3: Despacho de Autores en 1 Sola Ola (Contrato Form-C Quad-Band con `--lean`)
1. Despacha todos los shards en **1 sola ola paralela a $t=0$** (con prompts `--lean`, ordenados *Heaviest-First*, admitiendo segmentación por olas con `--wave`, requiriendo `MIN_ARCHETYPES = 4` y supuestos explícitos):
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/dispatch.py dispatch-authors --work-dir <work_dir> [--wave 1]
   ```
2. Invoca todos los subagentes en paralelo (`Model="flash"`) y agenda watchdog a 7 minutos (`DurationSeconds=420`).
3. Aplica Barrera Silenciosa: cero herramientas en mensajes parciales (`k < N`).
4. Al completar la ola (o si un shard activa Circuit Breaker, delegando con `dispatch.py dispatch-repair --work-dir <work_dir> --ids <CID>`), valida los templates aprovechando el fast-path `< 5 ms` de recibos criptográficos `shard_XX.cert.json`:
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage templates --work-dir <work_dir>
   ```

### Paso 4: Instanciación Masiva y Arbitraje Ciego
1. Instancia el banco completo en el sandbox de Top's Academy:
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage build --work-dir <work_dir>
   ```
2. Despacha los lotes ciegos a jueces con 1 semilla canónica pre-verificada por plantilla bajo Dominancia Bayesiana ($\alpha_{\text{Kernel}} = 0$):
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/dispatch.py dispatch-judges --work-dir <work_dir>
   ```
3. Espera en silencio la conclusión del arbitraje y evalúa concordancia:
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage judge-compare --work-dir <work_dir>
   ```
4. **Gates concurrentes y ola única de reparación**: usa `--stage gates` (secuencia determinista `build` + `verify` + QA dry-run + `repair-matrix` consolidada) y `dispatch-judges`. Al recibir veredictos, `--stage repair-matrix` fusiona linters + objeciones de jueces y emite UN solo comando `dispatch-repair --ids ...`:
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage gates --work-dir <work_dir>
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage repair-matrix --work-dir <work_dir>
   ```
   Si una reparación altera plantillas, usa re-arbitraje quirúrgico con `--stage rejudge` y `--stage rejudge-compare`:
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage rejudge --ids <CID1> <CID2> --work-dir <work_dir>
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage rejudge-compare --work-dir <work_dir>
   ```
5. **Certificación formal obligatoria**: ejecuta `--stage certify` (valida criptográficamente `*.cert.json` en `< 5 ms` para templates y re-ejecuta compuertas deterministas):
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage certify --work-dir <work_dir> --output-dir courses
   ```

### Paso 5: Publicación Final y Liberación (Compuerta Bloqueante PublishQualityGateError)
Publica el curso certificado (validando estricto `PublishQualityGateError` con MPRI $\ge 75$ y ZPD $> 0$):
```powershell
& ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage publish --work-dir <work_dir> --output-dir courses
```
El cerrojo `.c2c_subagent_lock.json` se libera automáticamente y la plataforma presenta la URL de interacción directa:
`http://localhost:3000/#/course/<course_id>`
