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
    description: Run a single stage (bootstrap, prepare, cta, cta-reduce, cta-apply, shard, templates, build, verify, publish, define-types, judge-compare, wave-status, unlock)
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

# Content-to-Course Antigravity Skill (v3.3 Pipeline Hardened Architecture)

A universal, subject-agnostic educational engineering pipeline that converts raw academic materials (Beamer presentations, handwritten OneNote notes, statistical software exports, and high-resolution chalkboard images) into fully playable, interactive Top's Academy courses in **≤ 20 minutes** for a standard 20-competency curriculum.

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
> ### 🏛️ ARQUITECTURA HARDENED v3.8 MASTERY TRI-BANDA:
> - **Fast Bootstrap & Promoción MapReduce (SLA ≤ 60–90s)**: Un único comando atómico CLI (`run.py --stage bootstrap`) inicializa el entorno, procesa PDFs sin rasterizado, y usa `mapreduce` por defecto (un `direct` expl&iacute;cito del usuario SIEMPRE prevalece y nunca se promueve por p&aacute;ginas/archivos), con particionado `slice_pdf_lossless` ($k = \lceil P/20 \rceil$) cuando el material supera 25 páginas o múltiples archivos.
> - **Flujo Simétrico de Armonización (`cta -> cta-reduce -> cta-apply`)**: En mapreduce o modo `--append`, la síntesis de partes converge simétricamente a través de `c2c_cta_harmonizer` (`cta_outline.json` y `duplicate_candidates.json`), absorbiendo nodos preexistentes `[BASE]` de solo lectura y ejecutando Fail-Fast ante desbordamiento de prosa en KaTeX (`[KATEX-PROSE-OVERFLOW]`, `\text{...} > 45` chars).
> - **Contrato Form-B Tri-Banda Multimodal (`--min-archetypes 3`)**: Cada competencia define 3 plantillas ortogonales (Directo `'easy'`, Inverso `'medium'`, Perturbación `'hard'`) con $\ge 2$ niveles Bloom y diversidad multimodal ($\ge 2$ FIB/MS en `Hab-*`, $\ge 1$ en `C-*`/`H-*`), con 3-tuplas dinámicas `(did, val, rationale_con_@var@)` (`[TPL-DYNAMIC-RATIONALE]`) y anti-patrón estático erradicado (`[TPL-STATIC-OPT]`).
> - **Silent Reactive Barrier Protocol (~12–16 Turnos del Director)**: En despertares reactivos parciales (`k < N` subagentes listos), el Director **NO EJECUTA NINGUNA HERRAMIENTA** (cero llamadas a CLI o sistema de archivos), registra el progreso en 1 línea (`Progreso de ola: k/N subagentes completados.`) y finaliza el turno en `< 2s`.
> - **Weighted Waves (`1 Hab/shard`, olas ≤ 10)**: Priorización *Heaviest-First*: cada habilidad práctica compleja (`Hab-*`) se aísla en su propio shard individual y se despacha en la Ola 1 (`--wave 1`) a $t=0$, amortiguando el camino crítico.
> - **Arbitraje Ciego 100% de Plantillas con 3 Semillas (101, 202, 303)**: Evaluación ciega tolerancia-cero (acuerdo 100% por `template_id`) en streaming concurrente (`--ready-only`).
> - **Compuerta Bloqueante Pre-Publish (`PublishQualityGateError`)**: Publicación bloqueada si el reporte de jueces falla o si el banco no cumple los umbrales psicométricos de producción (MPRI $\ge 75$, ZPD $> 0$, P4 $\ge 13.0/15$, unicidad de fundamentaciones $\ge 30\%$, 0 hard penalties, 0 opciones infladas con relleno de longitud).
> - **Dieta Estricta del Director & Cero Depuración Manual**: El Director tiene **PROHIBIDO** (y bloqueado por `c2c_hook_guard.py`) leer o editar código fuente de shards (`*_data.py`, `shard_fixes/*.py`), respuestas de jueces o scripts internos `.py` del skill. Todo error o discordancia se delega quirúrgicamente al subagente `c2c_repair`.
> - **PrairieLearn KaTeX Orthogonal (@var@)**: Desacoplamiento total entre KaTeX y Python mediante tokens `@var@` / `@var:fmt@` en raw strings `r"..."`, erradicando el uso de `rf"..."` y llaves triples `{{{...}}}`.

---

## 🏗️ Diagrama de Flujo v3.3

```
[ Fuentes Académicas: PDFs Beamer, Trazos Vectoriales, Apuntes ]
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Fast Bootstrap (run.py --stage bootstrap --course-id <id> --sources <...>)  │
│ - Ingesta Zero-Raster, manifiestos centralizados y delta continuo           │
│ - Genera work/dispatch/types/*.json (≤ 5 KB cada uno) y Subagents CTA       │
│ - Director define SOLO c2c_cta_architect, despacha CTA y luego define el resto│
│ - Activa watchdog (schedule a 7 min con budget_guard.py)                    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Stage 1: Síntesis Curricular CTA (run.py --stage cta)                       │
│ - Arquitectos leen sus partes asignadas con Pointer Prompts (<500 B)        │
│ - Granularidad standard: densidad relativa (3-5 comps por cada 5-10 págs)   │
│ - Auto-healing L1–L5; en mapreduce fusiona cta_parts/part_*.json -> cta.json│
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
│ - Máxima paralelización: Todos los shards lanzados en 1 ola a t=0           │
│ - Orden Heaviest-First: Habilidades (Hab-*) al frente del despacho          │
│ - Silent Reactive Barrier: 0 herramientas en mensajes parciales (k < N)    │
│ - SHA-256 Circuit Breaker; modular fixes en work/shards/shard_fixes/<CID>.py│
│ - Watchdog budget_guard.py audita transcript.jsonl y releva stragglers      │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Stage 4: Instanciación Masiva y Sweeps (run.py --stage build)               │
│ - Sweeps deterministas CRC32 (cuotas: 30 Skill / 20 Concepto y Hecho)       │
│ - Diversidad de stems >= 0.50 y evaluación de invariantes analíticos        │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Stage 5: Verificación Ciega Incremental (dispatch-judges --ready-only)      │
│ - Lotes ciegos ≤ 12 ítems; Turn 0 view_file ÚNICAMENTE sobre judge_XX.json  │
│ - Director ejecuta 0 herramientas hasta recibir N/N respuestas              │
│ - Arbitraje ciego: run.py --stage judge-compare                             │
│ - Si hay rechazos: delegación quirúrgica a c2c_repair                       │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Stage 6: Publicación y Cierre (run.py --stage publish)                      │
│ - Valida consenso de arbitraje ciego y publica a courses/<course_id>.json   │
│ - Libera cerrojo .c2c_subagent_lock.json y reporta URL de visualización     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Regla de Oro: Protocolo de Barrera Reactiva Silenciosa (Silent Reactive Barrier)

El Director de Proyecto debe mantener una interacción conversacional ultra-eficiente (~12–16 turnos en toda la corrida).

> [!CAUTION]
> **COMPORTAMIENTO OBLIGATORIO EN DESPERTARES PARCIALES (`k < N`):**
> Cuando un subagente finaliza y envía un mensaje `DONE: ...`, la plataforma despierta automáticamente al Director.
> - Si aún restan subagentes activos de la ola en curso (`k < N`) y el temporizador `schedule` de watchdog NO ha vencido:
> - **EL DIRECTOR TIENE ESTRICTAMENTE PROHIBIDO LLAMAR A CUALQUIER HERRAMIENTA.**
> - 🚫 NO ejecutes `Get-ChildItem`, `dir`, `run.py`, `view_file` ni `manage_subagents`.
> - Simplemente emite una línea de texto informativo: `Progreso de ola: k/N subagentes completados.` y **detén inmediatamente tu turno** (`< 2s` de ejecución).
> - La plataforma volverá a despertarte reactivamente cuando el siguiente subagente reporte o cuando la ola completa `N/N` esté lista.

Solo cuando se satisfaga la condición de barrera completa (`N/N` trabajadores de la ola reportaron `DONE:`, o `BLOCKED:`, o cuando el watchdog despierta al Director por tiempo), el Director procede a ejecutar la etapa siguiente del runner.

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
- Generación inmediata de las órdenes de trabajo de CTA (`Subagents` en el JSON de salida de `bootstrap`).

### Paso 1: Lanzamiento de CTA y Registro Diferido de Subagentes (Turnos 2, 3 y 4)
1. **Turno 2**: Lee en paralelo los archivos de `<work_dir>/dispatch/types/*.json` listados en `type_spec_files` (solo lecturas).
2. **Turno 3**: Registra **solo** `c2c_cta_architect` vía `define_subagent`, invoca `invoke_subagent` (`Model="flash"`) para cada elemento de `Subagents` devuelto por `bootstrap`, y agenda el watchdog a 7 minutos mediante `schedule` (`DurationSeconds=420` = 7 min, `Prompt="Auditar progreso CTA"`).
3. **Turno 4**: Mientras los architects trabajan, registra en un único turno paralelo los tipos restantes (`c2c_shard_author`, `c2c_judge`, `c2c_repair`, `c2c_cta_harmonizer` si existe) con `define_subagent`, y entra a la barrera.
   *(Nota: No necesitas ejecutar `dispatch.py dispatch-cta --work-dir <work_dir>` tras `bootstrap` porque `bootstrap` ya devuelve `Subagents` listos; usa `dispatch-cta` únicamente si necesitas re-despachar un trabajador caído).*
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

### Paso 3: Despacho de Autores en 1 Sola Ola (Contrato Form-B Tri-Banda)
1. Despacha todos los shards en **1 sola ola paralela a $t=0$** (sin partición artificial en olas secuenciales, ordenados *Heaviest-First* con `author_shard_XX.json` sin colisiones, requiriendo `--min-archetypes 3`):
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/dispatch.py dispatch-authors --work-dir <work_dir>
   ```
2. Invoca todos los subagentes en paralelo (`Model="flash"`) y agenda watchdog a 7 minutos (`DurationSeconds=420`).
3. Aplica Barrera Silenciosa: cero herramientas en mensajes parciales (`k < N`).
4. Al completar la ola (o si un shard activa Circuit Breaker, delegando con `dispatch.py dispatch-repair --work-dir <work_dir> --ids <CID>`), valida y compila los templates:
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage templates --work-dir <work_dir>
   ```

### Paso 4: Instanciación Masiva y Arbitraje Ciego
1. Instancia el banco completo en el sandbox de Top's Academy:
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage build --work-dir <work_dir>
   ```
2. Despacha los lotes ciegos a jueces (`≤ 12` ítems por juez con Pointer Mode, evaluando el 100% de plantillas con 3 semillas `(101, 202, 303)`):
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/dispatch.py dispatch-judges --work-dir <work_dir>
   ```
3. Espera en silencio la conclusión del arbitraje y evalúa concordancia:
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage judge-compare --work-dir <work_dir>
   ```

### Paso 5: Publicación Final y Liberación (Compuerta Bloqueante PublishQualityGateError)
Publica el curso certificado (validando estricto `PublishQualityGateError` con MPRI $\ge 75$ y ZPD $> 0$):
```powershell
& ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage publish --work-dir <work_dir> --output-dir courses
```
El cerrojo `.c2c_subagent_lock.json` se libera automáticamente y la plataforma presenta la URL de interacción directa:
`http://localhost:3000/#/course/<course_id>`
