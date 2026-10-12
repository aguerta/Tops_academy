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
> 1. **PASO 0B OBLIGATORIO (Registro de Tipos Especializados):** Al inicio de la sesión, el Director ejecuta `python .agents/skills/content-to-course/run.py --stage define-types` y registra mediante `define_subagent` los 7 tipos especializados (`c2c-vision`, `c2c-cta-mapper`, `c2c-cta-harmonizer`, `c2c-author`, `c2c-judge`, `c2c-cta-direct`, `c2c-repair`).
> 2. **PROHIBIDO redactar prompts a mano.** El Director **NUNCA** redacta a mano el `Prompt` de un subagente. Debe generar el payload ejecutando `python run.py --stage dispatch --role <vision|cta-map|cta-reduce|author|judge|repair>` y copiar fielmente los subagentes generados en `invoke_subagent`.
> 3. **MODELO ESTÁNDAR PARA SUBAGENTES:** Todos los subagentes especializados y jueces ciegos operan con el modelo rápido `flash` (`"Model": "flash"`).
> 4. **PROHIBIDO redactar plantillas de ejercicios (`work/templates/*.json`) en el hilo principal.** La autoría de plantillas **DEBE** ser delegada a subagentes autores en paralelo (`invoke_subagent`).
> 5. **PROHIBIDO transcribir páginas a mano en el hilo principal.** La visión se procesa mediante cuadrículas Handout (2x2 / 1x2) y subagentes Vision Analyzers en paralelo.
> 6. **PROHIBIDO resolver manualmente lotes de evaluación a ciegas.** La resolución ciega se delega a subagentes jueces en paralelo.
> 7. **FAN-OUT EN UN SOLO LLAMADO:** Al delegar trabajo en paralelo, el Director **DEBE** invocar a todos los subagentes simultáneamente dentro del array `Subagents` de un **único llamado a `invoke_subagent`**, y luego finalizar su turno (no invocar más herramientas) para esperar el despertar reactivo del sistema.

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

### Paso 0b: Registro de Tipos Especializados de Subagentes
1. El Director ejecuta:
   ```bash
   python .agents/skills/content-to-course/run.py --stage define-types
   ```
2. El Director invoca `define_subagent` para los 7 roles antes de despachar subagentes (`c2c-vision`, `c2c-cta-mapper`, `c2c-cta-harmonizer`, `c2c-author`, `c2c-judge`, `c2c-cta-direct`, `c2c-repair`).

---

### Paso 1: Visión y Análisis Cognitivo (CTA)

> [!IMPORTANT]
> **Ortogonalidad de Etapas:** El preprocesamiento de visión (`total_handouts > 0`) es completamente independiente del modo de síntesis de CTA.
> - Si existen imágenes, fórmulas complejas o diagramas que generaron Handouts, **la Fase 1A (Visión) es OBLIGATORIA y debe ejecutarse siempre**.
> - La **Fase 1B (Síntesis CTA)** se ejecuta luego de que las transcripciones de visión han sido cosidas con `run.py --stage stitch`, siguiendo estrictamente el modo indicado por el usuario (`direct` o `multiple/mapreduce`).

#### Fase 1A: Preprocesamiento Obligatorio de Visión (si `total_handouts > 0`)
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
   *(Si el usuario solicitó modo map-reduce, se puede usar `--partial` para habilitar secciones progresivas).*

*(Si no hay contenido visual y `total_handouts == 0`, se avanza directamente a la Fase 1B).*

---

#### Fase 1B: Síntesis de Competencias (CTA) según la instrucción del usuario

##### Vía 1: Direct CTA (si el usuario pidió Direct CTA o `--cta-mode direct`)
Aplica cuando el usuario desea síntesis directa en un solo subagente arquitecto sobre el corpus enriquecido con visión:
1. **Despachar Direct CTA Architect:**
   ```bash
   python .agents/skills/content-to-course/run.py --stage dispatch --role cta-direct --work-dir <work_dir>
   ```
   El Director copia el JSON resultante, llama a `invoke_subagent` con el Direct CTA Architect y finaliza el turno.
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
   Cada autor sigue el **Protocolo Atómico en 4 Fases**:
   - Fase 1: Lee su task bundle asignado en `work/dispatch/bundles/author_shard_XX.md`.
   - Fase 2: Redacta masivamente todas las plantillas en `work/templates/<cid>.json` utilizando raw strings `r"..."` para LaTeX.
   - Fase 3: Ejecuta la validación isomórfica completa en un solo comando:
     `python .agents/skills/content-to-course/check_templates.py work/shards/shard_XX.json --strict`
   - Fase 4: Termina respondiendo estrictamente `DONE: <archivos>`.
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
3. Evaluar respuestas contra ground truth:
   ```bash
   python .agents/skills/content-to-course/run.py --stage judge-compare --work-dir <work_dir>
   ```
4. **Circuito de Reparación Focalizada (si hay desacuerdos):**
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
