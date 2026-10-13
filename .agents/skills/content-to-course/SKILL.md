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

# Content-to-Course Antigravity Skill (v3 High-Throughput Orchestration Architecture)

A universal, subject-agnostic educational engineering pipeline that converts raw academic materials (Beamer presentations, handwritten OneNote notes, statistical software exports, and high-resolution chalkboard images) into fully playable, interactive Top's Academy courses.

---

> [!IMPORTANT]
> ## ROL FUNDAMENTAL: LA CONVERSACIÓN PRINCIPAL ES EL DIRECTOR DE EQUIPO (ORQUESTADOR)
> 
> La conversación principal actúa **exclusivamente como Directora de Proyecto / Orquestadora General**. Su responsabilidad es coordinar el flujo de trabajo, invocar las etapas del runner CLI (`run.py`), inspeccionar los presupuestos y artefactos de control, y **delegar todas las tareas intensivas a subagentes especializados en paralelo mediante `invoke_subagent`**.
>
> ### 🚫 REGLAS ESTRICTAS DE CONDUCTA DEL DIRECTOR:
> 1. **PASO 0B OBLIGATORIO (Registro en Lote de Subagentes - <20s) EN PARALELO CON `define_subagent`:** Al inicio de la sesión, el Director ejecuta `python .agents/skills/content-to-course/run.py --stage define-types` (o consulta `subagent_types.json`) y registra **SIMULTÁNEAMENTE** los 7 tipos especializados (`c2c-vision`, `c2c-cta-mapper`, `c2c-cta-harmonizer`, `c2c-author`, `c2c-judge`, `c2c-cta-direct`, `c2c-repair`) utilizando la capacidad nativa de Google Antigravity de **Parallel Tool Calling** (múltiples llamadas a la tool `define_subagent` emitidas en un ÚNICO turno / mensaje de respuesta del modelo, según `/antigravity-guide`). Queda TERMINANTEMENTE PROHIBIDO registrar los tipos de forma secuencial consumiendo turnos separados (uno por uno). Asimismo, queda PROHIBIDO inspeccionar o leer código fuente interno (`run.py`, `dispatch.py`, etc.) durante la instanciación.
> 2. **PROHIBIDO redactar prompts a mano.** El Director **NUNCA** redacta a mano el `Prompt` de un subagente. Debe generar el payload ejecutando `python run.py --stage dispatch --role <vision|cta-map|cta-reduce|author|judge|repair>` y copiar fielmente los subagentes generados en `invoke_subagent`.
> 3. **MODELO ESTÁNDAR PARA SUBAGENTES:** Todos los subagentes especializados y jueces ciegos operan con el modelo rápido `flash` (`"Model": "flash"`).
> 4. **PROHIBIDO redactar plantillas de ejercicios (`work/templates/*.json`) en el hilo principal.** La autoría de plantillas **DEBE** ser delegada a subagentes autores en paralelo (`invoke_subagent`).
> 5. **PROHIBIDO el análisis imagen por imagen cuando existan documentos PDF.** En Antigravity, la herramienta `view_file` lee archivos PDF (`.pdf`) directamente. Se debe utilizar **Ingesta Directa de PDF** (`--no-handouts --vision none`), aprovechando la extracción de texto en `work/corpus.md` y la lectura directa del PDF. La visión con Handouts queda reservada únicamente para notas manuscritas escaneadas o colecciones de imágenes puras.
> 6. **PROHIBIDO resolver manualmente lotes de evaluación a ciegas.** La resolución ciega se delega a subagentes jueces en paralelo.
> 7. **FAN-OUT EN UN SOLO LLAMADO (`invoke_subagent`):** Para abrir y ejecutar subagentes en paralelo, Google Antigravity dispone de la tool específica `invoke_subagent` (referencia `/antigravity-guide`). Al delegar trabajo en paralelo, el Director **DEBE** invocar a todos los subagentes concurrentes dentro del array `Subagents` de un **único llamado a `invoke_subagent`**, y luego finalizar su turno (no invocar más herramientas) para esperar el despertar reactivo del sistema. Queda terminantemente PROHIBIDO abrir subagentes uno por uno en llamadas o turnos separados.
> 8. **BLINDAJE OPERATIVO DE DIRECT CTA (ARQUITECTURA DE 2 ARCHIVOS):** El subagente `c2c-cta-direct` opera bajo la arquitectura de 2 archivos: emite tuplas pedagógicas compactas en `work/cta_data.py` en estricto orden cronológico (reduciendo tokens en >70%), y compila/certifica en <5ms mediante el compilador inmutable pre-sembrado `python work/compile_cta.py`. PROHIBIDO terminantemente volcar competencias o estructuras JSON en el chat.
> 9. **BLINDAJE OPERATIVO DE AUTORES DE SHARDS (TRÍADA DE CALIDAD):** Los autores `c2c-author` operan bajo la Tríada de Calidad: (1) Catálogo de antipatrones cognitivos (raw strings `r"..."`, dobles llaves `rf"k^{{{alpha}}}"`, prohibición de adjetivos delatores R-18 y fugas de respuesta en hints R-19); (2) Scaffold canónico de referencia pre-sembrado en `work/shards/<shard_id>/scratch/template_generator_canonical.py`; (3) Linter determinista en `check_templates.py` (`synthetic_boilerplate_distractor_rule` y `scaffolding_answer_leak_rule`). Refinan scaffolds modulares con `replace_file_content` o `write_to_file`.
> 10. **BLINDAJE OPERATIVO DE JUECES CIEGOS (CONTRATO TIPADO):** Los jueces `c2c-judge` resuelven lotes ciegos `work/judge_batch.json` enriquecidos con `answer_contract` explícito para preguntas numéricas (`expected_type`, `decimal_places`, `tolerance`), evaluadas deterministamente con `math.isclose` (tolerancia 0.01) para eliminar discrepancias de punto flotante. Clausura epistémica absoluta (prohibida navegación web).
> 11. **AISLAMIENTO CANÓNICO DE ESPACIO DE TRABAJO:** Todo artefacto reside estrictamente en `courses/<course_id>/work` con propagación dinámica de `--work-dir`, eliminando rutas relativas a la raíz y enlaces simbólicos.

---

## Arquitectura del Pipeline y Contratos de Etapa (v3 High-Throughput)

```
[ Documentos del Curso: PDFs Beamer, Notas OneNote/Ink, Imágenes ]
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 0: Prepare, Orden y Handouts (run.py --stage prepare)     │
│ - Orden natural de documentos resuelto (work/order.json)        │
│ - PyMuPDF block extraction con cropping Beamer / densidad       │
│ - Generación de Handouts 2x2 (Beamer) y 1x2 (Ink/Imágenes)      │
│ - Outputs: work/corpus.md, work/handouts/handouts_manifest.json │
└────────────────────────────────┬────────────────────────────────┘
                                 │
             ┌───────────────────┴───────────────────┐
             ▼ (si total_handouts > 0)               ▼ (si total_handouts == 0)
┌──────────────────────────────────────────┐         │
│ Fase 1A: Preprocesamiento de Visión      │         │
│ 1. Fan-out Vision Handouts               │         │
│    dispatch --role vision                │         │
│ 2. Stitching progresivo a corpus.md      │         │
│    run.py --stage stitch [--partial]     │         │
└────────────────────┬─────────────────────┘         │
                     └───────────────────┬───────────┘
                                         │
             ┌───────────────────────────┴───────────────────────────┐
             ▼ (si el usuario pide direct CTA)                       ▼ (si el usuario pide multiple/mapreduce CTA)
┌───────────────────────────────────────────┐           ┌──────────────────────────────────────────┐
│ Fase 1B: Direct CTA                       │           │ Fase 1B: Multiple / Map-Reduce CTA       │
│ dispatch --role cta-direct                │           │ 1. Secciones: run.py --stage sections    │
│ 1 subagente sintetiza cta.json            │           │ 2. Fan-out CTA Map: dispatch --role cta-map
│ sobre corpus enriquecido con visión       │           │ 3. CTA Merge: run.py --stage cta-merge   │
│                                           │           │ 4. CTA Harmonize: dispatch --role cta-reduce
│                                           │           │ 5. CTA Apply: run.py --stage cta-apply   │
└─────────────────────┬─────────────────────┘           └────────────────────┬─────────────────────┘
                      └──────────────────────────┬───────────────────────────┘
                                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 1 Gate: Verificación CTA (run.py --stage cta)             │
│ - Valida cuotas de distractores fusionados (>=3 Fact/Concept, >=6 Skill)
│ - Valida evidencias y ontología [H], [C], [Hab]                 │
│ - Checkpoint opcional: --review-cta                             │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 2: Sharding de Competencias (run.py --stage shard)        │
│ - Particiona en shards balanceados contiguos (8 comp. default)  │
│ - Detección adaptativa de grafos densos de distractores (4 comp)│
│ - Outputs: work/shards/shard_01.json ... shard_0K.json          │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 3: Fan-Out de Autores Atómicos (dispatch --role author)    │
│ - Director genera payload de autores con SCOPE-LOCK y bundle    │
│ - K subagentes autores en paralelo en 1 solo invoke_subagent    │
│ - Protocolo Atómico en 4 Fases (Lectura -> Escritura masiva     │
│   -> Validación isomórfica en 1 comando -> DONE)                │
│ - Director verifica gate: run.py --stage templates              │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 4: Instanciación en Sandbox (run.py --stage build)        │
│ - Sweeps deterministas CRC32 cumpliendo cuotas (30/20)          │
│ - Verificación de invariantes y diversidad de stems >= 0.5      │
│ - Outputs: work/course.json                                     │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 5: Verificación y Jueces Ciegos (run.py --stage verify)   │
│ - Genera lote de evaluación estratificado sin soluciones        │
│ - dispatch --role judge divide en lotes para jueces flash       │
│ - run.py --stage judge-compare evalúa acuerdo contra claves     │
│ - Circuito de reparación: dispatch --role repair ante discordias│
│ - Outputs: work/judge_report.json, work/course_verified.json    │
└────────────────────────────────┬────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Stage 6: Publicación en Plataforma (run.py --stage publish)     │
│ - Verificación obligatoria de arbitraje ciego aprobado          │
│ - Publica a courses/<course_id>.json y registra en plataforma   │
│ - Plataforma interactiva lista en http://localhost:3000         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Protocolo de Orquestación del Director (Paso a Paso)

### Paso 0a: Preparación, Orden y Handouts
1. Ejecutar en terminal:
   ```bash
   python .agents/skills/content-to-course/run.py --stage prepare --pdf <pdf_path> --course-id <course_id> --work-dir <work_dir> [--granularity standard] [--cta-mode auto]
   ```
2. La salida del comando informa:
   - Orden resuelto de documentos (`work/order.json`). Si el usuario especificó un orden particular, se usó `--order`.
   - Modo CTA seleccionado (`mapreduce` o `direct`) y granularidad registrada en `budget.json`.
   - Total de Handouts generados (cuadrículas 2x2 para Beamer, 1x2 para notas/imágenes con banners indelebles).

### Paso 0b: Registro de Tipos Especializados de Subagentes en Paralelo (<20s)
1. El Director ejecuta:
   ```bash
   python .agents/skills/content-to-course/run.py --stage define-types
   ```
   *(Este comando emite el JSON limpio sin truncamiento y persiste `subagent_types.json`).*
2. **REGISTRO EN PARALELO EN UN ÚNICO TURNO CON `define_subagent` (PARALLEL TOOL CALLING):**
   De acuerdo con la arquitectura de Google Antigravity (referencia `/antigravity-guide`), el modelo dispone nativamente de la capacidad de **Parallel Tool Calling** para emitir múltiples llamadas a herramientas en una misma respuesta. El Director **DEBE** invocar la tool específica `define_subagent` para los 7 roles **SIMULTÁNEAMENTE en un ÚNICO turno** (emitiendo un único mensaje con las 7 llamadas a `define_subagent` en paralelo sin esperar turnos intermedios):
   - `c2c-vision`: Handout Vision Analyzer (`enable_write_tools: true`)
   - `c2c-cta-mapper`: Sectional CTA Mapper (`enable_write_tools: true`)
   - `c2c-cta-harmonizer`: Curriculum Harmonization (`enable_write_tools: true`)
   - `c2c-author`: Psychometric Exercise Author (`enable_write_tools: true`)
   - `c2c-judge`: Blind Psychometric Evaluation Judge (`enable_write_tools: true`)
   - `c2c-cta-direct`: Direct CTA Architect (`enable_write_tools: true`)
   - `c2c-repair`: Targeted Repair subagent (`enable_write_tools: true`)

   > [!CAUTION]
   > **PROHIBICIÓN ESTRICTA DE SERIALIZACIÓN:** Queda TERMINANTEMENTE PROHIBIDO invocar `define_subagent` de forma secuencial gastando 7 turnos separados (uno por subagente). Deben registrarse los 7 en el mismo turno. Posteriormente, para abrir y ejecutar subagentes en paralelo durante el pipeline, Google Antigravity cuenta con la tool específica `invoke_subagent`, la cual debe recibir todo el lote en su array `Subagents` en una única llamada. Queda estrictamente prohibido perder turnos explorando o leyendo archivos internos de la skill (`run.py`, `dispatch.py`, etc.).

---

### Paso 1: Ingesta Directa de PDF y Análisis Cognitivo (CTA)

> [!IMPORTANT]
> **Ingesta Directa de PDF vs Preprocesamiento de Visión:**
> En Antigravity SDK, la herramienta `view_file` soporta nativamente la lectura de documentos PDF completos (`.pdf`). Además, `run.py --stage prepare` extrae automáticamente la capa completa de texto y matemáticas en `work/corpus.md`.
> - **Cursos basados en PDFs (Beamer, Papers, Libros):** Se ejecutan con **Ingesta Directa de PDF** (`--no-handouts --vision none`). Se omite por completo la generación de imágenes y cuadrículas de handouts. **NO se hace análisis imagen por imagen.** Los subagentes arquitectos y autores leen directamente `work/corpus.md` y pueden consultar los PDFs fuente en `content/**/*.pdf` directamente con `view_file`. Se avanza **DIRECTAMENTE a la Fase 1B (Síntesis CTA)**.
> - **Materiales Manuscritos o Imágenes Puras:** Si el contenido proviene de notas manuscritas escaneadas o carpetas de imágenes sin texto (`total_handouts > 0`), se ejecuta la Fase 1A de visión.

#### Fase 1A: Preprocesamiento de Visión (RESERVADO EXCLUSIVAMENTE para imágenes puras o notas manuscritas con `total_handouts > 0`)
1. **Despachar Vision Analyzers en Paralelo:**
   Generar payload de subagentes de visión:
   ```bash
   python .agents/skills/content-to-course/run.py --stage dispatch --role vision --work-dir <work_dir>
   ```
   El Director copia el JSON resultante y llama a `invoke_subagent` con todos los Vision Analyzers en un solo llamado. Finaliza el turno para esperar.
2. **Coser Parches a `corpus.md` (Stitch):**
   A medida que los analizadores de visión notifican `DONE`:
   ```bash
   python .agents/skills/content-to-course/run.py --stage stitch --work-dir <work_dir>
   ```

*(En Ingesta Directa de PDF y cuando `total_handouts == 0`, se avanza DIRECTAMENTE a la Fase 1B).*

---

#### Fase 1B: Síntesis de Competencias (CTA)
En Ingesta Directa de PDF, esta etapa se ejecuta de inmediato tras el Paso 0 (Prepare).
Sigue estrictamente la modalidad pedida por el usuario (`direct` o `multiple/mapreduce`):

##### Vía 1: Direct CTA (si el usuario pidió Direct CTA o `--cta-mode direct`)
Aplica cuando el usuario desea síntesis directa en un solo subagente arquitecto que inspecciona directamente los archivos originales en `content/` (vía `view_file` sobre los PDFs) y complementa con `work/corpus.md`:
1. **Despachar Direct CTA Architect:**
   ```bash
   python .agents/skills/content-to-course/run.py --stage dispatch --role cta-direct --work-dir <work_dir>
   ```
   El Director copia el JSON resultante, llama a `invoke_subagent` con el Direct CTA Architect y finaliza el turno.
   - **Contrato Operativo de Emisión a Archivo:** El subagente `c2c-cta-direct` tiene **PROHIBICIÓN ESTRICTA** de volcar competencias o fragmentos JSON en el chat conversacional (evita agotar `max_output_tokens`). Su primera y única acción es emitir directamente a disco (`work/generate_cta.py` o `work/cta.json` / `work/cta.md`).
   - **Límite por Lotes:** Estructura las competencias de forma incremental en bloques de **COMO MÁXIMO 10 competencias a la vez** para prevenir colapsos de salida y garantizar la profundidad de los distractores.
2. **Validar gate de CTA:**
   Al despertar tras `DONE`:
   ```bash
   python .agents/skills/content-to-course/run.py --stage cta --work-dir <work_dir>
   ```

##### Vía 2: Multiple / Map-Reduce CTA (si el usuario pidió Multiple CTA o `--cta-mode mapreduce`)
Aplica cuando el usuario solicita partición seccional map-reduce:
1. **Generar Secciones:**
   ```bash
   python .agents/skills/content-to-course/run.py --stage sections --work-dir <work_dir>
   ```
2. **Despachar CTA Mappers:**
   ```bash
   python .agents/skills/content-to-course/run.py --stage dispatch --role cta-map --ready-only --work-dir <work_dir>
   ```
   Llama a `invoke_subagent` con las secciones listas y finaliza el turno.
3. **Consolidar Partes (Map -> Merge):**
   ```bash
   python .agents/skills/content-to-course/run.py --stage cta-merge --work-dir <work_dir>
   ```
4. **Despachar Harmonizer (Reduce):**
   ```bash
   python .agents/skills/content-to-course/run.py --stage dispatch --role cta-reduce --work-dir <work_dir>
   ```
   Llama a `invoke_subagent` con el CTA Harmonizer y finaliza el turno.
5. **Aplicar y Validar Gate de CTA:**
   ```bash
   python .agents/skills/content-to-course/run.py --stage cta-apply --work-dir <work_dir>
   ```
   ```bash
   python .agents/skills/content-to-course/run.py --stage cta --work-dir <work_dir>
   ```

---

### Paso 2: Partición en Shards Amortizados (8 competencias por Shard)
1. El Director ejecuta el particionador:
   ```bash
   python .agents/skills/content-to-course/run.py --stage shard --work-dir <work_dir>
   ```
   Garantiza shards contiguos equilibrados (diferencia de tamaño ≤ 1, 8 competencias por defecto).

---

### Paso 3: Fan-Out Paralelo de Autores con Protocolo Atómico
1. El Director genera el payload de autores:
   ```bash
   python .agents/skills/content-to-course/run.py --stage dispatch --role author --work-dir <work_dir>
   ```
2. El Director llama a `invoke_subagent` con todos los autores en un único llamado concurrente.
   Cada autor sigue el **Protocolo de Autoría Atómica Consolidada**:
   - **Erradicación de Micro-Bucles y Aislamiento:** Queda terminantemente PROHIBIDO crear scripts individuales por competencia (`generate_c01.py`, `generate_c02.py`, etc.) o usar nombres compartidos entre shards como `generate_all_templates.py`. Se utiliza un script modular consolidado exclusivo por shard (`work/build_<shard_id>.py` o en `scratch/`) o llamadas atómicas directas a `write_to_file`.
   - **Prevención de Colapso de Tokens:** Para no desbordar `max_output_tokens`, el script consolidado o los JSONs se construyen de forma incremental en bloques de **COMO MÁXIMO 1 o 2 competencias a la vez**. Queda prohibido volcar 8 competencias complejas en un solo llamado de escritura masiva.
   - **Cero Introspección del Validador:** Los autores tienen estrictamente prohibido abrir o hacer ingeniería inversa de `check_templates.py`, `src/validator/*` (incluyendo `rules.py`) o `engine/*`. Los diagnósticos del validador son auto-contenidos y prescriptivos.
   - **Validación Isomórfica en 1 Solo Comando:** Todo el shard se valida simultáneamente en una sola invocación de terminal (`check_templates.py work/templates/*.json --cta work/cta.json --strict`). Las correcciones se aplican en bloque (máx. 3 ciclos).
   - **Cierre Limpio:** Termina respondiendo estrictamente `DONE: <archivos>`.
   *El Director detiene sus llamadas a herramientas y espera el retorno reactivo.*
3. Al despertar, el Director verifica el gate de plantillas:
   ```bash
   python .agents/skills/content-to-course/run.py --stage templates --work-dir <work_dir>
   ```

---

### Paso 4: Instanciación Masiva en Sandbox
1. El Director ejecuta la instanciación de preguntas:
   ```bash
   python .agents/skills/content-to-course/run.py --stage build --work-dir <work_dir>
   ```
   *Verifica cuotas (≥30 por habilidad, ≥20 por hecho/concepto), invariantes y diversidad de stems (≥0.5).*

---

### Paso 5: Verificación Independiente y Circuito Cerrado de Jueces Ciegos
1. El Director genera el lote ciego:
   ```bash
   python .agents/skills/content-to-course/run.py --stage verify --work-dir <work_dir>
   ```
2. Despachar evaluadores ciegos (modelo `flash`):
   ```bash
   python .agents/skills/content-to-course/run.py --stage dispatch --role judge --work-dir <work_dir>
   ```
   Invoca `invoke_subagent` con los Blind Judges y espera retorno.
   - **Clausura Epistémica Absoluta:** Los evaluadores tienen terminantemente PROHIBIDO el uso de herramientas de búsqueda web (`search_web`, `read_url_content`) o acceso a internet. La deducción debe ser 100% analítica desde primeros principios a partir del lote recibido.
   - **Fallback de Bloqueo por Falta de Contexto:** Si un reactivo carece de variables o contexto matemático autosuficiente (ej. placeholders no sustituidos), el juez responde en el JSON:
     `"answer": "BLOCKED: Reactivo <id> carece de contexto matemático autosuficiente"`
     para que el pipeline lo derive al circuito de reparación (`c2c-repair`) en lugar de inventar o adivinar.
3. Evaluar respuestas contra ground truth:
   ```bash
   python .agents/skills/content-to-course/run.py --stage judge-compare --work-dir <work_dir>
   ```
4. **Circuito de Reparación Focalizada (si hay desacuerdos o reactivos bloqueados):**
   Si se reportan discordancias en `work/judge_report.json`:
   ```bash
   python .agents/skills/content-to-course/run.py --stage dispatch --role repair --work-dir <work_dir>
   ```
   El subagente `c2c-repair` recibe el diagnóstico exacto de la discordancia en su bundle, corrige la plantilla y valida localmente con `check_templates.py`. Re-ejecutar `judge-compare`.

---

### Paso 6: Publicación y Registro del Curso
1. El Director publica el curso:
   ```bash
   python .agents/skills/content-to-course/run.py --stage publish --work-dir <work_dir> --output-dir courses
   ```
   *(Valida automáticamente que `judge_report.json` esté en estado `passed`; puede omitirse con `--skip-judges`).*
2. El Director presenta el resumen ejecutivo al usuario:
   - Título y Course ID.
   - Ruta del archivo publicado (`courses/<course_id>.json`).
   - Conteo de preguntas y competencias validadas (100% de reglas psicométricas).
   - Enlace interactivo en la plataforma: `http://localhost:3000/#/course/<course_id>`.
