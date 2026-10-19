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

# Content-to-Course Antigravity Skill (v3.22 High-Throughput Hardened Architecture)

A universal, subject-agnostic educational engineering pipeline that converts raw academic materials (Beamer presentations, handwritten OneNote notes, statistical software exports, and high-resolution chalkboard images) into fully playable, interactive Top's Academy courses in **≤ 20 minutes** for a standard 20-competency curriculum.

---

> [!IMPORTANT]
> ## ROL FUNDAMENTAL: LA CONVERSACIÓN PRINCIPAL ES EL DIRECTOR DE EQUIPO (ORQUESTADOR)
> 
> La conversación principal actúa **exclusivamente como Directora de Proyecto / Orquestadora General**. Su responsabilidad es coordinar el flujo de trabajo, invocar las etapas del runner CLI (`run.py`), inspeccionar los presupuestos y artefactos de control, y **delegar todas las tareas intensivas a subagentes especializados en paralelo mediante `invoke_subagent`**.
>
> ### 🏛️ ARQUITECTURA HARDENED v3.22 (SWIFT-DISPATCH & POINTER PROMPTS):
> - **Pointer Prompts (~300 B)**: El Director NUNCA transcribe grandes fragmentos de especificación en el chat. Los system prompts se definen una sola vez (≤ 5 KB cada uno) y las llamadas a `invoke_subagent` utilizan encabezados ultra-compactos que apuntan a órdenes de trabajo en disco (`work/dispatch/items/<role>_XX.json`). El tiempo de mecanografiado del Director se reduce de 96–186s a ≤ 1s.
> - **Swift-Dispatch SLA (≤ 20s)**: Entre la finalización del comando `dispatch` y el envío de `invoke_subagent`, el Director no debe inspeccionar los contenidos ni razonar sobre ellos: toma el bloque estructurado de subagentes y lo despacha de inmediato en **un único llamado concurrente** ordenado por peso descendente.
> - **Lossless MapReduce Slicing**: Partición física de PDFs mediante `pymupdf` `select()` + `save()` en `work/parts/part_NN/`, preservando trazos vectoriales y tipografías originales. Las citas de evidencia se mantienen locales (1..n) y se remapean deterministamente en la fase reduce.
> - **Automated Watchdog (`budget_guard.py`)**: Temporizador reactivo (`schedule`) que despierta al Director tras 5–8 minutos de fan-out para auditar `transcript.jsonl`. Subagentes con > 40 turnos, > 5M tokens o bucles de lectura son abortados y reemplazados quirúrgicamente por `c2c_repair`.
> - **Layered Automated Healing (L1–L5)**: Ciclo cerrado que repara sintaxis KaTeX, snapping de encabezados y delimitadores de matemáticas antes de requerir intervención del subagente, registrando cada ajuste en `patch_ledger.json`.
> - **Append Workflow & Environment Resilience**: Inyección delta en `prepare.py --append` leyendo `courses/<id>.json` para generar secuencias numéricas continuas sin solapamiento (ej. Solow 21 → 45). Resiliencia a UTF-8 en PowerShell (fallback ante `\ufffd`) y saneamiento de comillas en rutas de Windows.

---

## 🏗️ Diagrama de Arquitectura del Pipeline v3.22

```
[ Fuentes Originales: PDFs Beamer, Trazos Vectoriales, Apuntes ]
                           │
                           ▼
┌───────────────────────────────────────────────────────────────────────┐
│ Stage 0: Prepare & Delta Manifest (prepare.py / run.py --stage prepare)│
│ - Particionado físico sin pérdidas (pymupdf select() + save())        │
│ - Ponderación estructural por streams vectoriales e imágenes          │
│ - Modo --append: Lee courses/<id>.json e inyecta next_ids continuos    │
│ - Genera: work/pre_cta_manifest.json (y delta_manifest.json)          │
│ - BLOCKER estricto si falta manifiesto central                        │
└──────────────────────────────────┬────────────────────────────────────┘
                                   │
                                   ▼
┌───────────────────────────────────────────────────────────────────────┐
│ Stage 1: Síntesis CTA MapReduce / Directa (dispatch-cta)              │
│ - Swift-Dispatch: Director emite invoke_subagent con Pointer Prompts  │
│ - Arquitectos leen su slice (work/parts/part_NN/) citando páginas 1..n│
│ - Layered Healing L1–L5: KaTeX tokenization, snapped headings         │
│ - patch_ledger.json audita reparaciones; cta_merge.py remapea global  │
│ - Cero micro-ediciones: emisión atómica en work/cta_data.py           │
└──────────────────────────────────┬────────────────────────────────────┘
                                   │
                                   ▼
┌───────────────────────────────────────────────────────────────────────┐
│ Stage 2: Sizing Adaptativo y Sharding (run.py --stage shard)          │
│ - Shards dinámicos: clamp(ceil(N / 8), 2, 6) comp/shard, hasta 8 aut. │
│ - Balanceo contiguo de dependencias pedagógicas sin cortes arbitrarios│
│ - Genera manifiesto: work/shards/pre_shard_manifest.json              │
└──────────────────────────────────┬────────────────────────────────────┘
                                   │
                                   ▼
┌───────────────────────────────────────────────────────────────────────┐
│ Stage 3: Fan-Out de Autores Atómicos & Watchdog (dispatch-authors)    │
│ - Pointer Prompts (<300 B) apuntando a work/dispatch/items/author_XX  │
│ - Contexto Turn-0 completo inyectado en disco; prohibido compile_shard│
│ - SHA-256 Circuit Breaker: auto-reset inmediato ante cambios de código│
│ - Interpolación de variables por regex; espacio paramétrico >= 500    │
│ - Watchdog (budget_guard.py a 8 min): aborta y reemplaza stragglers   │
│ - Gate de compilación: run.py --stage templates                       │
└──────────────────────────────────┬────────────────────────────────────┘
                                   │
                                   ▼
┌───────────────────────────────────────────────────────────────────────┐
│ Stage 4: Instanciación Masiva en Sandbox (run.py --stage build)       │
│ - Sweeps deterministas CRC32 (30 habilidad / 20 concepto y hecho)     │
│ - Diversidad de stems >= 0.5 y verificación de invariantes algebraicos│
│ - Genera curso unificado instanciado: work/course.json                │
└──────────────────────────────────┬────────────────────────────────────┘
                                   │
                                   ▼
┌───────────────────────────────────────────────────────────────────────┐
│ Stage 5: Verificación Ciega en Lotes Nativos (dispatch-judges)        │
│ - Limpieza previa: manage_subagents(kill_all) para purgar errored     │
│ - Lotes ciegos particionados nativamente: <= 12 ítems por juez        │
│ - Zero context checkpoint: Director nunca lee los 90 KB de preguntas  │
│ - Jueces resuelven por primeros principios en 1 solo turno            │
│ - Autovalidación de completitud y re-despacho de reactivos faltantes  │
│ - run.py --stage judge-compare evalúa acuerdo contra claves           │
└──────────────────────────────────┬────────────────────────────────────┘
                                   │
                                   ▼
┌───────────────────────────────────────────────────────────────────────┐
│ Stage 6: Publicación y Registro en Plataforma (run.py --stage publish)│
│ - Valida arbitraje ciego aprobado (acuerdo >= 95% o 0 discordancias)  │
│ - Saneamiento UTF-8: fallback a cta.json ante \ufffd en --title       │
│ - Modo --append: fusión directa continua; remap como fallback avisado │
│ - Publica a courses/<course_id>.json y registra en base de datos      │
│ - Acceso inmediato en: http://localhost:3000/#/course/<course_id>     │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Taxonomía Forense de Fallas y Matriz de Mitigación (12 Defectos Críticos)

A partir de la síntesis forense sobre las 7 corridas de producción, se consolidaron los 12 modos de falla que degradaban el rendimiento del pipeline y sus correspondientes soluciones arquitectónicas en v3.22:

| # | Modo de Falla | Causa Raíz Exacta | Impacto en Producción | Mitigación Arquitectónica v3.22 |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Purga de Espacios Activos en `delete_course.py`** | `clean_orphan_course_dirs` borraba carpetas sin JSON final aunque tuvieran trabajo en curso. | Eliminación accidental de `work/` activo en Runs 1–3 y pérdida de artefactos. | Guardia estricta: prohibido borrar si existe `state.json`, `pre_cta_manifest.json` o archivos con `< 24h` de modificación. |
| **2** | **Residuos de `corpus.md` en Stdout / Logs** | Referencias heredadas a archivos de texto intermedios en scripts y prompts. | Confusión en subagentes, intentos de lectura de archivos inexistentes. | Purga completa de código y stdout para `corpus.md` y `section_*.md`; lectura directa de PDF/imágenes. |
| **3** | **Micro-Ediciones Iterativas en CTA** | Arquitecto emitía el archivo con múltiples llamadas a `replace_file_content` corrigiendo sintaxis. | Hasta 33 turnos y 24 minutos en Stage 1 (Run 2). | Emisión atómica en 1 solo `write_to_file`; capas de auto-healing L1–L5; límite de ≤ 3 edits y ≤ 2 compilaciones. |
| **4** | **Sobre-Lectura de Herramientas por Autores** | Subagentes ejecutaban `view_file` de `compile_shard.py` o `check_templates.py`. | Quema masiva de tokens de lectura (hasta 18M en Shard 03). | Prohibición en Scope-Lock de leer herramientas internas; inyección de plantilla canónica de 15 líneas en prompt. |
| **5** | **Colisión LaTeX `{...}` vs Regla `R-20`** | `str.format(**vars)` en `assemble.py` fallaba con llaves de KaTeX (`K^{0.5}`, `\frac{a}{b}`). | 132 turnos en Shard 03 (Run 6) al intentar escapar con llaves dobles residuales. | Reemplazo de `.format()` por regex selectivo de variables; normalización automática `{{token}}` → `{token}` en compilador. |
| **6** | **Corrupción de Subíndices en `\frac`** | Regex simple de fracciones rompía subíndices compuestos tipo `\frac{S_{xy}}{S_{xx}}`. | 136 turnos y 16.4M tokens en Shard 01 (Run 2) hasta intervención manual. | Parche estructural de fracciones balanceadas (`frac_simple_fix`) protegido por suite unitaria de regresión. |
| **7** | **Bloqueo Permanente de Circuit Breaker** | `BUDGET HALT` en `.check_attempts` no se reseteaba tras corregir el código del shard. | Autores en bucle infinito reintentando contra un bloqueo permanente (Runs 2, 5, 6). | Circuit Breaker con hash SHA-256: auto-reset inmediato en cuanto el código del archivo cambia. |
| **8** | **Creación de Carpeta en vez de Archivo** | `compile_shard.py` ejecutaba `mkdir(parents=True)` sobre la ruta destino cuando el archivo no existía. | Creación de directorios `shard_XX_data.py/` que impedían escrituras futuras (Runs 1 y 5). | Comprobación estricta de extensión `.py` y salida con error limpio sin invocar `mkdir`. |
| **9** | **Discrepancia de Flags CLI en Shards** | Omisión de `--shard` o `--work` en ejemplos de ejecución del prompt de autores. | `ERROR: shard_id no especificado` y lecturas cruzadas entre autores concurrentes. | Auto-inferencia de `shard_id` y `work_dir` a partir de la ruta de `--input`; aislamiento de espacio paramétrico (≥500 comb). |
| **10** | **Lotes Monolíticos en Jueces y Context Checkpoint** | Despacho de 42–48 reactivos en un solo lote a jueces; Director hacía `view_file` de 260 KB. | Salida truncada del juez (22/48 en Run 7) y `CHECKPOINT` de compactación en Director (Run 2). | Particionado nativo en sub-lotes de ≤ 12 ítems (`judge_batch_NN.json`); Pointer Prompts (<300 B) sin saturar contexto. |
| **11** | **Ceguera Delta en Modo `--append`** | Etapas 0–5 no leían el curso existente, re-extrayendo competencias desde `C-01` y remapeando al final. | Gasto innecesario de 7.68M tokens y remapeo heurístico tardío en Stage 6 (Run 6). | `prepare.py --append` lee `courses/<id>.json`, inyecta competencias existentes y secuencias numéricas continuas desde Stage 0. |
| **12** | **Fricción de Consola Windows y Caracteres `\ufffd`** | Codificación PowerShell corrompía tildes en `--title` (`Estad\ufffdstica`); comillas escapadas `\"`. | 12 turnos reparando títulos y fallos de sintaxis en one-liners de `python -c` (Runs 2, 3, 7). | Saneamiento de argumentos CLI; fallback automático al título de `cta.json`; prohibición de `python -c` con comillas anidadas. |

---

## 🛡️ Procedimientos de Watchdog y Protocolo de Presupuesto

Para garantizar que ningún subagente descontrolado queme tokens en bucle, el Director implementa una vigilancia automatizada en dos capas:

### 1. Despacho Rápido y SLAs de Tiempo (Swift-Dispatch SLA)
- **SLA de Despacho (≤ 20 segundos)**: El Director debe despachar los subagentes en **un único llamado paralelo a `invoke_subagent`** en un plazo no mayor a 20s desde que el comando `dispatch` finaliza.
- **Orden de Fan-Out**: Las tareas se ordenan de mayor a menor peso computacional (ej. el shard con mayor densidad de cálculos primero), permitiendo que el straggler potencial inicie primero.
- **Finalización de Turno Inmediata**: Tras emitir `invoke_subagent`, el Director NO invoca más herramientas y finaliza su turno para esperar el despertar reactivo.

### 2. Guardián de Presupuesto (`budget_guard.py`)
- Al fannear autores o jueces, el Director agenda un temporizador de control mediante `schedule`:
  - **Autores de Shards**: Timer a **8 minutos** (`DurationSeconds=480`).
  - **Particiones CTA MapReduce**: Timer a **5 minutos** (`DurationSeconds=300`).
- Al sonar el temporizador, si el fan-out no ha concluido, el Director ejecuta:
  ```bash
  python .agents/skills/content-to-course/budget_guard.py --work-dir <work_dir>
  ```
- **Criterios de Aborto**:
  - Subagente con más de **40 turnos**.
  - Subagente con más de **5,000,000 tokens** acumulados.
  - Subagente en bucle repetitivo de lecturas de herramientas (`compile_shard.py`, `check_templates.py`).
- **Protocolo de Recuperación**:
  1. Abortar el subagente conflictivo mediante `manage_task(Action='kill', TaskId=...)` o `manage_subagents(Action='kill')`.
  2. Despachar un subagente de rescate `c2c_repair` asignado **exclusivamente a las competencias incompletas**, heredando el código parcial compilado.

---

## 🔄 Playbook de Resunción ante Límites de Tasa (429 / 404)

Cuando la API emite errores de cuota o indisponibilidad (`429 RESOURCE_EXHAUSTED` o `404 NOT_FOUND`):

1. **Estado Incremental Persistente (`work/state.json`)**:
   - Cada etapa registra checkpoints atómicos con el estado de cada shard o partición (`completed`, `in_progress`, `pending`).
   - Los archivos completados en disco (`shard_01.json`, `cta_parts/part_01.json`) son inmutables e idempotentes: no se vuelven a procesar.
2. **Limpieza de Subagentes Residuales Pre-Stage 5**:
   - Antes de iniciar la verificación de jueces ciegos, el Director ejecuta:
     ```bash
     manage_subagents(Action="kill_all")
     ```
   - Esto evita que entradas residuales en estado `errored` por 429 previos confundan la toma de decisiones del Director.
3. **Resunción Focalizada**:
   - Al recuperarse de un corte, el Director reanuda la ejecución únicamente para las unidades no marcadas como completadas en `work/state.json`.
   - PROHIBIDO reiniciar el pipeline desde la etapa 0 si las etapas previas ya están certificadas.

---

## 💻 Guía de Entorno y Manejo de Rutas en Windows PowerShell

Para evitar anomalías de quoting y fallos de codificación observados en sistemas Windows:

1. **Saneamiento de Títulos Unicode**:
   - Si la terminal pasa un título con caracteres de reemplazo (`\ufffd`), los componentes `run.py`, `prepare.py` y `course_publisher.py` descartan automáticamente la cadena dañada y leen el título íntegro UTF-8 desde `cta.json`, `pre_cta_manifest.json` o el curso base.
2. **Rutas Absolutas Limpias (Cero `\"` Incrustadas)**:
   - Pasar siempre rutas absolutas limpias sin comillas dobles escapadas internas:
     - ✅ Correcto: `--work-dir D:/Augusto/courses/solow/work`
     - ❌ Incorrecto: `--work-dir "\"D:\\Augusto\\courses\\solow\\work\""`
3. **Prohibición de One-Liners Complejos con `python -c`**:
   - No ejecutar comandos complejos con comillas anidadas en PowerShell mediante `python -c`.
   - Si se requiere una manipulación de datos o particionado auxiliar, escribir un script temporal en `scratch/script.py` y ejecutarlo directamente:
     ```bash
     python scratch/helper.py
     ```

---

## 🚀 Guía de Ejecución Paso a Paso del Director

### Paso 0: Preparación y Manifiesto (prepare.py)
```bash
python .agents/skills/content-to-course/run.py --stage prepare --pdf <pdf_path> --course-id <course_id> --work-dir <work_dir> [--append] [--cta-mode auto]
```
- Si se activa `--append`, lee `courses/<id>.json` y calcula la secuencia continua de IDs (`delta_manifest.json`).

### Paso 1: Registro de Tipos con Load Inversion (<20s)
```bash
python .agents/skills/content-to-course/run.py --stage define-types --work-dir <work_dir>
```
- El Director lee los 4 tipos en 1 solo turno de `view_file` y registra `define_subagent` en paralelo.

### Paso 2: Despacho CTA y Validación
```bash
python .agents/skills/content-to-course/dispatch.py dispatch-cta --work-dir <work_dir>
```
- Despacha los arquitectos con Pointer Prompts en 1 solo turno concurrente. Al finalizar:
```bash
python .agents/skills/content-to-course/run.py --stage cta --work-dir <work_dir>
```

### Paso 3: Sharding y Fan-Out de Autores
```bash
python .agents/skills/content-to-course/run.py --stage shard --work-dir <work_dir>
python .agents/skills/content-to-course/dispatch.py dispatch-authors --work-dir <work_dir>
```
- El Director lanza todos los autores en **una sola llamada concurrente a `invoke_subagent`**.
- Activa el watchdog a 8 minutos. Al concluir:
```bash
python .agents/skills/content-to-course/run.py --stage templates --work-dir <work_dir>
```

### Paso 4: Instanciación Masiva en Sandbox
```bash
python .agents/skills/content-to-course/run.py --stage build --work-dir <work_dir>
```

### Paso 5: Verificación Ciega y Arbitraje
```bash
manage_subagents(Action="kill_all")
python .agents/skills/content-to-course/run.py --stage verify --work-dir <work_dir>
python .agents/skills/content-to-course/dispatch.py dispatch-judges --work-dir <work_dir>
```
- Lotes nativos de ≤ 12 ítems por juez. Lanzamiento simultáneo en 1 solo turno de `invoke_subagent`. Al concluir:
```bash
python .agents/skills/content-to-course/run.py --stage judge-compare --work-dir <work_dir>
```

### Paso 6: Publicación en Plataforma
```bash
python .agents/skills/content-to-course/run.py --stage publish --work-dir <work_dir> --output-dir courses [--append]
```
- Publica a `courses/<course_id>.json` e imprime URL interactiva: `http://localhost:3000/#/course/<course_id>`.
