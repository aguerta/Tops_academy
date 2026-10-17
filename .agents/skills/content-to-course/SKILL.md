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
    required: true
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
    description: Run a single stage (prepare, cta, shard, templates, build, verify, publish, define-types, judge-compare)
    required: false
  from_stage:
    type: string
    description: Resume pipeline execution from a given stage to completion
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

# Content-to-Course Antigravity Skill (v3.21 High-Throughput Load Inversion Architecture)

A universal, subject-agnostic educational engineering pipeline that converts raw academic materials (Beamer presentations, handwritten OneNote notes, statistical software exports, and high-resolution chalkboard images) into fully playable, interactive Top's Academy courses.

---

> [!IMPORTANT]
> ## ROL FUNDAMENTAL: LA CONVERSACIÓN PRINCIPAL ES EL DIRECTOR DE EQUIPO (ORQUESTADOR)
> 
> La conversación principal actúa **exclusivamente como Directora de Proyecto / Orquestadora General**. Su responsabilidad es coordinar el flujo de trabajo, invocar las etapas del runner CLI (`run.py`), inspeccionar los presupuestos y artefactos de control, y **delegar todas las tareas intensivas a subagentes especializados en paralelo mediante `invoke_subagent`**.
>
> ### 🏛️ ARQUITECTURA DE INVERSIÓN DE CARGA (LOAD INVERSION ARCHITECTURE - v3.21):
> - **`work/dispatch/types/*.json`**: Almacena el **100% íntegro del `system_prompt` universal** (sin truncar ni comprimir), registrado una sola vez al inicio de la sesión mediante `define_subagent`.
> - **`work/dispatch/items/*.json`**: Contiene exclusivamente **órdenes de trabajo atómicas, concisas y con cero duplicación de system prompt** (`< 2,500 caracteres`), equipadas con encabezado Scope-Lock, directivas de tarea, comandos exactos de compilación determinista y señal de finalización `DONE:`.
>
> ### 🚫 REGLAS ESTRICTAS DE CONDUCTA DEL DIRECTOR:
> 1. **PASO 0 (Registro de Tipos Especializados con Load Inversion vía `define_subagent`):** Al inicio de la sesión, el Director ejecuta `python .agents/skills/content-to-course/run.py --stage define-types` (o `dispatch.py define-types --work-dir <work_dir>`). Este comando genera archivos individuales por tipo en `work/dispatch/types/<type_name>.json` (`c2c_cta_architect.json`, `c2c_shard_author.json`, `c2c_judge.json`, `c2c_repair.json`), cada uno conteniendo el 100% del system prompt sin truncamiento (`< 20 KB`). El Director lee en **1 solo turno paralelo de llamadas a `view_file`** todos los archivos de tipos y emite simultáneamente en un **ÚNICO turno paralelo las llamadas a `define_subagent`** (Parallel Tool Calling).
> 2. **DESPACHO LOAD INVERSION Y TRASPASO DIRECTO (`work/dispatch/items/`):** Al despachar subagentes (`cta`, `authors`, `judges`, `repair`), `dispatch.py` genera un archivo individual por subagente en `work/dispatch/items/<stage>_<idx:02d>.json` (cada uno `< 5 KB`, conciso y libre de system prompts duplicados). El Director ejecuta llamadas paralelas a `view_file` en **1 solo turno** sobre todos los archivos de ítems asignados para obtener las órdenes de trabajo íntegras, y las pasa directamente a `invoke_subagent`.
> 3. **MODELO ESTÁNDAR PARA SUBAGENTES:** Todos los subagentes especializados y jueces ciegos operan con el modelo rápido `flash` (`"Model": "flash"`).
> 4. **PROHIBIDO redactar plantillas de ejercicios (`work/templates/*.json`) en el hilo principal:** La autoría de plantillas **DEBE** ser delegada a subagentes autores en paralelo (`invoke_subagent`).
> 5. **INGESTA DIRECTA DE PDF POR DEFECTO:** En Antigravity, la herramienta `view_file` lee archivos PDF (`.pdf`) directamente. Se debe utilizar **Ingesta Directa de PDF** (`--no-handouts --vision none`), aprovechando la extracción de texto en `work/corpus.md` y la lectura directa del PDF.
> 6. **PROHIBIDO resolver manualmente lotes de evaluación a ciegas:** La resolución ciega se delega a subagentes jueces en paralelo con Zero-Warmup in-prompt payload.
> 7. **FAN-OUT EN UN SOLO LLAMADO CONCURRENTE (`invoke_subagent`):** Al delegar trabajo en paralelo en cualquier etapa (CTA, Shards/Autores, Jueces Ciegos), el Director **DEBE** leer todos los ítems en **1 solo turno paralelo de `view_file`** e invocar a **TODOS** los subagentes concurrentes dentro del array `Subagents` en un **ÚNICO llamado a `invoke_subagent`** con `"Model": "flash"` (incluyendo **todos los `judge_01..judge_N` simultáneamente en una sola llamada**, ¡NUNCA de forma secuencial ni en tandas separadas!). Inmediatamente después, el Director finaliza su turno (sin invocar más herramientas) para esperar el despertar reactivo del sistema.
> 8. **BLINDAJE OPERATIVO DE DIRECT CTA (TUPLAS POSICIONALES EN `cta_data.py`):** El subagente `c2c_cta_architect` emite tuplas pedagógicas compactas en `work/cta_data.py` (o `work/cta_parts/part_XX_data.py`) en estricto orden cronológico. Cero diccionarios y cero chat emissions.
> 9. **BLINDAJE OPERATIVO DE AUTORES DE SHARDS (CONTEXTO TURN-0 COMPLETO & `compile_shard.py`):** Los autores `c2c_shard_author` reciben la especificación completa Turn-0 de sus competencias y los 6 distractores (D-XX-01..06) inyectados en su orden de trabajo, escriben funciones Python nativas y tuplas de 9 elementos en `work/shards/shard_XX_data.py` y compilan deterministamente con `compile_shard.py`. Cero scaffolds pre-sembrados en `work/templates/` y cero carpetas `scratch/`.
> 10. **BLINDAJE OPERATIVO DE JUECES CIEGOS (ZERO-WARMUP EN 1 SOLO TURNO):** Los jueces `c2c_judge` reciben el lote completo de preguntas inyectado directamente en su prompt, resuelven por primeros principios sin llamar a `view_file` ni `run_command`, y escriben `work/verification/judge_responses_XX.json` (o `work/judges/judge_XX.json`) en **1 solo turno**.
> 11. **RECOLECCIÓN INCREMENTAL DE TELEMETRÍA ETAPA POR ETAPA:** El estado y la telemetría de cada etapa se recolectan y persisten de forma incremental en `work/state.json` y `work/telemetry/` (`telemetry_<stage>.json`), registrando tokens (input, output, thinking, cache), latencias por turno y estado de cumplimiento.

---

## Arquitectura del Pipeline y Contratos de Etapa (v3.2 High-Throughput)

```
[ Documentos del Curso: PDFs Beamer, Papers, Libros ]
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 0: Prepare & Manifiesto Pre-CTA (run.py --stage prepare)  │
│ - Extrae capa de texto/matemáticas (work/corpus.md)             │
│ - Genera manifiesto de fuentes: work/pre_cta_manifest.json      │
│   (documentos, rutas y rangos de páginas válidas 1..N)          │
│ - Si falta pre_cta_manifest.json: BLOCKER inmediato             │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 1: Síntesis de Competencias CTA (dispatch-cta)             │
│ - Exige work/pre_cta_manifest.json (cero fallbacks)             │
│ - Director lee work/dispatch/items/cta_01.json (<28KB)          │
│ - Subagente c2c_cta_architect escribe tuplas en cta_data.py     │
│ - Compilación y certificación determinista a work/cta.json      │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 2: Sharding de Competencias (run.py --stage shard)        │
│ - Particiona en shards balanceados contiguos (4 a 8 comp.)      │
│ - Genera manifiesto de shards: work/shards/pre_shard_manifest.json
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 3: Fan-Out de Autores Atómicos (dispatch-authors)         │
│ - Exige pre_shard_manifest.json y pre_cta_manifest.json         │
│ - Director lee work/dispatch/items/author_XX.json (<28KB) c/u   │
│ - K subagentes c2c_shard_author escriben shard_XX_data.py       │
│ - Compilación estricta con compile_shard.py                     │
│ - Gate de plantillas: run.py --stage templates                  │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 4: Instanciación Masiva en Sandbox (run.py --stage build) │
│ - Sweeps deterministas CRC32 cumpliendo cuotas (30/20)          │
│ - Verificación de invariantes y diversidad de stems >= 0.5      │
│ - Outputs: work/course.json                                     │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 5: Verificación y Jueces Ciegos (dispatch-judges)         │
│ - Genera lotes ciegos en work/verification/judge_batch_XX.json   │
│ - Director lee work/dispatch/items/judge_XX.json (<28KB) c/u    │
│ - Zero-Warmup: Ítems inyectados directamente en prompt de juez  │
│ - Jueces resuelven y escriben en 1 solo turno                   │
│ - run.py --stage judge-compare evalúa acuerdo contra claves     │
│ - Circuito de reparación focalizado ante discordancias          │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 6: Publicación en Plataforma (run.py --stage publish)     │
│ - Valida arbitraje ciego aprobado                               │
│ - Publica a courses/<course_id>.json y registra en plataforma   │
│ - Plataforma interactiva lista en http://localhost:3000         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Protocolo de Orquestación del Director (Paso a Paso)

### Paso 0a: Preparación y Manifiesto Pre-CTA
1. Ejecutar en terminal:
   ```bash
   python .agents/skills/content-to-course/run.py --stage prepare --pdf <pdf_path> --course-id <course_id> --work-dir <work_dir> [--granularity standard] [--cta-mode auto]
   ```
2. La salida del comando genera:
   - Capa de texto enriquecida: `work/corpus.md`.
   - **Manifiesto de documentos pre-CTA (`work/pre_cta_manifest.json`)**: lista exhaustiva de documentos fuente, rutas de acceso y rango de páginas PDF válidas `1..N`.
   - Si no existe `work/pre_cta_manifest.json`, el pipeline se detiene inmediatamente con:
     `BLOCKER:: No existe pre_cta_manifest.json`

---

### Paso 0 (0b): Registro de Tipos Especializados de Subagentes con Load Inversion (<20s)
1. El Director ejecuta:
   ```bash
   python .agents/skills/content-to-course/run.py --stage define-types --work-dir <work_dir>
   ```
   *(Este comando genera los archivos individuales en `work/dispatch/types/<type_name>.json`, cada uno con el 100% íntegro del system prompt universal, y el índice en `work/dispatch/subagent_types.json`).*

2. **Lectura Paralela de Tipos y Registro Simultáneo con `define_subagent`:**
   El Director lee en **1 solo turno paralelo de llamadas a `view_file`** todos los archivos individuales (`< 20 KB` cada uno):
   - `work/dispatch/types/c2c_cta_architect.json`
   - `work/dispatch/types/c2c_shard_author.json`
   - `work/dispatch/types/c2c_judge.json`
   - `work/dispatch/types/c2c_repair.json`

   Y emite simultáneamente en ese **mismo único turno** las 4 llamadas a `define_subagent` (Parallel Tool Calling), registrando:
   - `c2c_cta_architect`: Cognitive Task Analysis Architect (`enable_write_tools: true`)
   - `c2c_shard_author`: Shard Exercise Author (`enable_write_tools: true`)
   - `c2c_judge`: Blind Evaluation Judge (`enable_write_tools: true`)
   - `c2c_repair`: Targeted Repair Engineer (`enable_write_tools: true`)

---

### Paso 1 / Paso 2 (CTA): Síntesis Cognitiva de Competencias

1. **Generar Despacho CTA:**
   ```bash
   python .agents/skills/content-to-course/dispatch.py dispatch-cta --work-dir <work_dir> [--mode direct]
   ```
   - El script verifica estrictamente que exista `work/pre_cta_manifest.json` (o `work/ingestion_manifest.json`). Si no existe, detiene con:
     `BLOCKER:: No existe pre_cta_manifest.json`.
   - Genera los archivos de subagente individuales en `work/dispatch/items/cta_*.json` (`< 2,500 caracteres`, sin duplicación de system prompt gracias a Load Inversion) y el log en `work/dispatch/cta.json`.

2. **Lectura en 1 Solo Turno Paralelo e Invocación Única:**
   El Director lee todos los archivos `work/dispatch/items/cta_*.json` generados en **1 solo turno paralelo de llamadas a `view_file`**, e invoca inmediatamente a todos los subagentes CTA en **1 sola llamada a `invoke_subagent`** con `"Model": "flash"`.

3. **Contrato de Operación del Arquitecto:**
   - **Paginación 1-indexed:** Cita exclusivamente páginas `1..N` del archivo PDF según la tabla de `pre_cta_manifest.json` / `ingestion_manifest.json`. NUNCA usa la numeración impresa del libro o capítulo.
   - **Tuplas Puras:** Emite tuplas de 9 elementos en `work/cta_data.py` (o `work/cta_parts/part_XX_data.py`). Cero diccionarios y cero chat output.
   - **Compilación Determinista:** Compila con `python .agents/skills/content-to-course/compile_cta.py --input <py_path> --output <json_path> --manifest <manifest_path>` y corrige errores línea a línea con `replace_file_content`.

> [!NOTE]
> **Modos CTA (`direct` vs `mapreduce`):**
> - **Modo `direct` (por defecto):** Despacha un único arquitecto con `work/dispatch/items/cta_01.json` (`< 2,500 caracteres`) para emitir el currículo completo en `work/cta_data.py`.
> - **Modo `mapreduce`:** Despacha un subagente arquitecto por cada subparte declarada (`work/dispatch/items/cta_01.json`, `cta_02.json`, ..., `cta_MM.json`), pasando a cada uno exclusivamente el documento/rango de páginas de su subparte y el comando `compile_cta.py`.

4. **Validar Gate de CTA:**
   Al despertar tras `DONE`:
   ```bash
   python .agents/skills/content-to-course/run.py --stage cta --work-dir <work_dir>
   ```

---

### Paso 2: Partición en Shards Amortizados

1. El Director ejecuta el particionador:
   ```bash
   python .agents/skills/content-to-course/run.py --stage shard --work-dir <work_dir>
   ```
   - Genera `work/shards/pre_shard_manifest.json` con la distribución de competencias por shard.

---

### Paso 3 / Paso 4 (Shards): Fan-Out Paralelo de Autores con Contexto Turn-0

1. **Generar Despacho de Autores:**
   ```bash
   python .agents/skills/content-to-course/dispatch.py dispatch-authors --work-dir <work_dir>
   ```
   - Exige `work/shards/pre_shard_manifest.json` y `work/pre_cta_manifest.json`. Si falta alguno, emite:
     `BLOCKER:: No existe pre_shard_manifest.json` o `BLOCKER:: No existe pre_cta_manifest.json`.
   - Escribe archivos individuales por autor en `work/dispatch/items/author_01.json`, `author_02.json`, ... con especificación Turn-0 completa (competencias + 6 distractores D-XX-01..06) y cero duplicación de system prompt.

2. **Lectura en 1 Solo Turno Paralelo e Invocación Masiva Única:**
   El Director lee **todos** los archivos `work/dispatch/items/author_*.json` generados en **1 solo turno paralelo de llamadas a `view_file`**, y lanza simultáneamente a **todos los subagentes autores (`author_01..author_N`) en 1 sola llamada a `invoke_subagent`** con `"Model": "flash"`.

3. **Contrato de Autoría Nativa de Shards:**
   - Cada autor escribe funciones Python y tuplas de 9 elementos en `work/shards/shard_XX_data.py` (`TEMPLATES = [...]`).
   - Cero pre-siembra de JSONs en `work/templates/` ni bundles en `work/shards/bundles/`.
   - Ejecuta la compilación estricta con:
     `python .agents/skills/content-to-course/compile_shard.py --input work/shards/<shard_id>_data.py --output work/shards/<shard_id>.json --cta work/cta.json --manifest work/ingestion_manifest.json`
   - Si se reportan errores mapeados a línea, los corrige con `replace_file_content` sobre `shard_XX_data.py` y finaliza con `DONE: work/shards/<shard_id>.json`.

4. **Validar Gate de Plantillas:**
   ```bash
   python .agents/skills/content-to-course/run.py --stage templates --work-dir <work_dir>
   ```

---

### Paso 4: Instanciación Masiva en Sandbox

1. El Director ejecuta:
   ```bash
   python .agents/skills/content-to-course/run.py --stage build --work-dir <work_dir>
   ```
   - Valida sweeps deterministas CRC32, cuotas (≥30 por habilidad, ≥20 por hecho/concepto), invariantes y diversidad de stems (≥0.5).

---

### Paso 5: Verificación Independiente y Circuito Cerrado de Jueces Ciegos

1. Generar lote de evaluación ciego:
   ```bash
   python .agents/skills/content-to-course/run.py --stage verify --work-dir <work_dir>
   ```

2. **Despachar Jueces con Zero-Warmup:**
   ```bash
   python .agents/skills/content-to-course/dispatch.py dispatch-judges --work-dir <work_dir>
   ```
   - Escribe archivos de ítems en `work/dispatch/items/judge_01.json`, `judge_02.json`, ...
   - Inyecta los reactivos del batch (`question_id`, `question_type`, `stem_es`, `options`) directamente dentro del `Prompt` sin duplicar el system prompt.

3. **Lectura en 1 Solo Turno Paralelo y Lanzamiento Concurrente Total:**
   El Director lee **todos** los archivos `work/dispatch/items/judge_*.json` en **1 solo turno paralelo de llamadas a `view_file`** y lanza a **TODOS los jueces (`judge_01..judge_N`) concurrentemente en 1 único llamado a `invoke_subagent`** con `"Model": "flash"` (¡estrictamente PROHIBIDO lanzarlos secuencialmente o en tandas separadas!).
   - Los jueces ciegos **NO leen archivos con `view_file` ni ejecutan `run_command`**: resuelven analíticamente desde primeros principios y escriben `work/verification/judge_responses_XX.json` (o `work/judges/judge_XX.json`) en **1 solo turno**.

4. **Evaluar Respuestas contra Claves:**
   ```bash
   python .agents/skills/content-to-course/run.py --stage judge-compare --work-dir <work_dir>
   ```

5. **Circuito de Reparación Focalizada:**
   Si se reportan discordancias en `work/judge_report.json`:
   ```bash
   python .agents/skills/content-to-course/dispatch.py dispatch-repair --work-dir <work_dir>
   ```
   El subagente `c2c_repair` corrige quirúrgicamente las tuplas en `work/shards/shard_XX_data.py` y re-compila con `compile_shard.py`.

---

### Paso 6: Publicación y Registro del Curso

1. El Director publica el curso:
   ```bash
   python .agents/skills/content-to-course/run.py --stage publish --work-dir <work_dir> --output-dir courses
   ```
2. Presenta el resumen ejecutivo al usuario:
   - Título y Course ID.
   - Ruta del archivo publicado (`courses/<course_id>.json`).
   - Conteo de preguntas y competencias validadas (100% de reglas psicométricas).
   - Enlace interactivo en la plataforma: `http://localhost:3000/#/course/<course_id>`.
