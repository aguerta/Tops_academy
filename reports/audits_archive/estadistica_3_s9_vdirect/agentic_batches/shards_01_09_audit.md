# Auditoría Forense Granular de Shards de Autoría (Shards 01 al 09)
## Pipeline Content-to-Course (C2C v3.21) — Conversación [`592de77b-afd9-4fae-8744-4ef0be7212f4`](conversation://592de77b-afd9-4fae-8744-4ef0be7212f4)

**Fecha de Auditoría:** `2026-10-31 18:35:00 UTC`  
**Auditor Forense:** Worker 2 — Especialista en Autoría de Shards 01 a 09  
**Entorno de Ejecución:** Top's Academy C2C Engine / Google Antigravity SDK  
**Curso Auditado:** `estadistica_3_s9_vdirect` (`Semana 9: Propiedades Asintóticas de Estimadores`)  
**Directorio de Trabajo Auditado:** [`d:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_s9_vdirect\work\shards`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/shards)  
**Archivo de Curso Publicado:** [`d:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_s9_vdirect.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect.json)  

---

## 1. Resumen Ejecutivo y Metrología Forense Comparativa (Shards 01–09)

El presente informe constituye la auditoría forense y psicométrica de la primera mitad del clúster paralelo de autoría (Shards `shard_01` a `shard_09`), ejecutados concurrentemente durante la fase `03_templates` del pipeline C2C v3.21. Este lote de 9 subagentes cubrió un total de **10 competencias académicas** (8 habilidades analíticas de demostración `Hab-01` a `Hab-08` y 2 competencias conceptuales avanzadas `C-01` y `C-02`), generando **40 plantillas generativas paramétricas** que dieron lugar a **280 reactivos evaluativos interactivos** (30 reactivos por cada habilidad y 20 por cada competencia conceptual) en el curso final publicado.

### 1.1. Matriz Metrológica Consolidada de Ejecución

| Shard ID | Subagent UUID | Competencias Asignadas | Duración Pared (s) | Turnos | Tokens In | Tokens Out | Cache Tokens | Errores Exploratorios | 1st-Pass Compile | Remediaciones Post-Compile |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`shard_01`** | [`201b96e8-48d9-4fa8-bee8-ac42eeecddc0`](file:///C:/Users/augus/.gemini/antigravity/brain/201b96e8-48d9-4fa8-bee8-ac42eeecddc0/.system_generated/logs/transcript.jsonl) | `Hab-01` | `214.0s` | 11 | 67,668 | 28,541 | 227,212 | 2 | ✅ PASS | 0 (Pase Limpio) |
| **`shard_02`** | [`f029517c-a58a-499a-81f6-33c4a7b253a1`](file:///C:/Users/augus/.gemini/antigravity/brain/f029517c-a58a-499a-81f6-33c4a7b253a1/.system_generated/logs/transcript.jsonl) | `Hab-02` | `212.0s` | 7 | 77,046 | 30,970 | 124,252 | 1 | ✅ PASS | 0 (Pase Limpio) |
| **`shard_03`** | [`c99727cf-4b7a-4b01-a117-ac37dfc3d1ca`](file:///C:/Users/augus/.gemini/antigravity/brain/c99727cf-4b7a-4b01-a117-ac37dfc3d1ca/.system_generated/logs/transcript.jsonl) | `Hab-03` | `256.0s` | 10 | 96,668 | 35,230 | 274,694 | 4 | ✅ PASS | 0 (Pase Limpio) |
| **`shard_04`** | [`37cfcefd-beb5-4408-b3d6-bcc593052280`](file:///C:/Users/augus/.gemini/antigravity/brain/37cfcefd-beb5-4408-b3d6-bcc593052280/.system_generated/logs/transcript.jsonl) | `Hab-04` | **`210.0s`** | 8 | 80,081 | 30,403 | 136,276 | 2 | ✅ PASS | 0 (Gold Standard) |
| **`shard_05`** | [`d1465f5d-bf1f-4091-b76b-e32cdf4fcd47`](file:///C:/Users/augus/.gemini/antigravity/brain/d1465f5d-bf1f-4091-b76b-e32cdf4fcd47/.system_generated/logs/transcript.jsonl) | `Hab-05` | `273.0s` | 11 | 72,115 | 32,325 | 239,506 | 3 | ✅ PASS | 0 (Pase Limpio) |
| **`shard_06`** | [`f3704081-15dc-4beb-96ff-745c27742aa3`](file:///C:/Users/augus/.gemini/antigravity/brain/f3704081-15dc-4beb-96ff-745c27742aa3/.system_generated/logs/transcript.jsonl) | `Hab-06` | `235.0s` | 9 | 81,456 | 33,735 | 184,440 | 2 | ✅ PASS | 0 (Pase Limpio) |
| **`shard_07`** | [`a307d4d9-a83d-4fe7-b9c2-404dc731ec4f`](file:///C:/Users/augus/.gemini/antigravity/brain/a307d4d9-a83d-4fe7-b9c2-404dc731ec4f/.system_generated/logs/transcript.jsonl) | `Hab-07` | **`210.0s`** | 8 | 79,011 | 29,744 | 231,277 | 2 | ✅ PASS | 0 (Co-Fastest Clean) |
| **`shard_08`** | [`2da986f3-14db-44b4-ad27-47f501625966`](file:///C:/Users/augus/.gemini/antigravity/brain/2da986f3-14db-44b4-ad27-47f501625966/.system_generated/logs/transcript.jsonl) | `Hab-08` | `289.0s` | 18 | 101,063 | 35,142 | 577,341 | 4 | ✅ PASS | 0 (Pase Limpio) |
| **`shard_09`** | [`9240ae0d-b45d-4112-bffc-79395bd35199`](file:///C:/Users/augus/.gemini/antigravity/brain/9240ae0d-b45d-4112-bffc-79395bd35199/.system_generated/logs/transcript.jsonl) | `C-01, C-02` | `231.0s` | 8 | 72,720 | 34,641 | 173,310 | 2 | ✅ PASS | 0 (Pase Limpio) |
| **TOTALES** | **9 Subagentes** | **10 Comps** | **Mediana: 231s** | **90 turnos** | **727,828** | **290,731** | **2,168,308** | **22 errs** | **100% (9/9)** | **0 ediciones** |

### 1.2. Hallazgos Forenses Centrales

1. **Eficiencia de Compilación Impecable (100% First-Pass Pass Rate):** A diferencia de ejecuciones previas de C2C donde los autores requerían múltiples ciclos de remediación (`shard_fixes`), **los 9 shards lograron compilar exitosamente en su primer intento formal de compilación**, con 0 fallos de validación matemática y 0 ediciones de código post-escritura.
2. **El Patrón de Falsa Compilación Temprana (`compile_shard.py --help`):** En `shard_01`, `shard_05` y `shard_06`, la métrica previa de telemetría reportaba "compilaciones tempranas" a los ~57-84s. La auditoría microscópica del transcript revela que estos subagentes **no compilaron código prematuramente**, sino que ejecutaron `python compile_shard.py --help` para inspeccionar la interfaz CLI del compilador antes de redactar el código.
3. **El Síndrome de la Prospección Ciega (22 Errores de Turnos Tempranos):** Los 22 errores registrados en el lote corresponden al 100% a fallos de herramientas `view_file` intentando leer archivos inexistentes (`work/templates/Hab-XX.json`, `shard_01_data.py` de subagentes hermanos, o rutas relativas). Ningún error provino del código Python generado ni de violaciones psicométricas denegadas por hooks.
4. **Colapso Psicométrico Universal por Aplanamiento de Tuplas (Form A):** Todos los shards emplearon tuplas de 9 elementos (Form A), las cuales carecen de ranuras para `difficulty` y `hints`. Como consecuencia directa del descompilador de [`compile_shard.py`](file:///D:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py#L1421-L1527), **el 100% de los 280 reactivos generados quedó forzado a `difficulty = "medium"` y `bloom_taxonomy_level = "Understand"`**, sustituyendo las pistas socráticas reales por un generador de cadenas tipo Mad-Libs que además filtró variables crudas (`$theta_hat$`, `$Y_bar$`, `$sigma^2$`) a la vista del estudiante.

---

## 2. Inquiry 1: Benchmarking del Shard de Referencia Clean-Room (`shard_04` y `shard_07` a 210.0s)

### 2.1. Anatomía Operativa de los Clean-Room Reference Shards

Los subagentes `shard_04` ([`37cfcefd-beb5-4408-b3d6-bcc593052280`](file:///C:/Users/augus/.gemini/antigravity/brain/37cfcefd-beb5-4408-b3d6-bcc593052280/.system_generated/logs/transcript.jsonl)) y `shard_07` ([`a307d4d9-a83d-4fe7-b9c2-404dc731ec4f`](file:///C:/Users/augus/.gemini/antigravity/brain/a307d4d9-a83d-4fe7-b9c2-404dc731ec4f/.system_generated/logs/transcript.jsonl)) lograron la marca de pared más veloz de todo el clúster de autoría: **exactamente 210.0 segundos**, completando la totalidad de su ciclo de vida en 8 turnos estrictos con 0 fallos de compilación y 0 ediciones posteriores.

```mermaid
sequenceDiagram
    autonumber
    participant Orch as Orchestrator (592de77b)
    participant S4 as Shard Author 04 (37cfcefd)
    participant FS as Local Filesystem
    participant Comp as compile_shard.py

    Orch->>S4: Dispatch Work Order (Hab-04)
    Note over S4: Turn 1 (0-6s): Ingesta de author_04.json
    S4->>FS: view_file(author_04.json)
    Note over S4: Turn 2 (6-9s): Verificación de Manifest
    S4->>FS: view_file(pre_shard_manifest.json)
    Note over S4: Turn 3-4 (9-23s): Exploración tentativa (2 errores)
    S4->>FS: view_file(work/templates/Hab-04.json) -> ERROR 404
    S4->>FS: view_file(work/shards/shard_01_data.py) -> ERROR 404
    Note over S4: Turn 5 (23-198s): Inferencia y Generación Python
    S4->>FS: write_file(shard_04_data.py) [2,069 bytes, 4 arquetipos]
    Note over S4: Turn 6 (198-208s): Compilación Determinista
    S4->>Comp: run_command(compile_shard.py --strict --min-archetypes 4)
    Comp-->>S4: PASS (30 items, 0 errors)
    Note over S4: Turn 7 (208-210s): Señal de Cierre
    S4->>Orch: send_message(DONE: courses/.../shard_04.json)
    Note over S4: Turn 8: Idle Exit
```

#### Factores Críticos del Rendimiento Clean-Room:
1. **Pivote Rápido ante Archivos Faltantes (Desconexión de Bucle en Turno 4):** Tanto `shard_04` como `shard_07` intentaron inicialmente leer `work/templates/Hab-XX.json` y `shard_01_data.py`. Al recibir el segundo error en Turno 4, sus cadenas de razonamiento (thinking traces) reconocieron inmediatamente que los archivos no existían debido a la autosuficiencia de Turno 0 prescrita en la orden de trabajo:
   > *Thinking snippet `shard_04` (Turno 4):* `"Initial examination confirms the template file is absent, as anticipated. Analyzing the author_04.json reveals the competency Hab-04, a skill requiring 30 items related to demonstrating Markov's inequality... Autosufficiency holds. Proceeding directly to generate the mathematical data structures."*
2. **Generación Monolítica y Correcta en Turno 5:** La escritura del archivo de código se realizó en una sola llamada a `write_file` ([`shard_04_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/shards/shard_04_data.py) con 2,069 bytes / 80 líneas; [`shard_07_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/shards/shard_07_data.py) con 2,068 bytes / 75 líneas). La inferencia consumió 175 segundos continuos de pensamiento y generación matemática densa, cubriendo los 4 arquetipos con espacios paramétricos superiores a 500 combinaciones sin errores de sintaxis LaTeX ni llamadas a librerías prohibidas.
3. **Cero Prospección CLI Redundante:** Ni `shard_04` ni `shard_07` perdieron tiempo ejecutando comandos como `python compile_shard.py --help` o `dir`. Tomaron la cadena de compilación provista de forma literal en la clave `compile_command` del archivo JSON de despacho y la ejecutaron directamente.

---

### 2.2. Trayectorias Comparativas: `shard_04` / `shard_07` frente a `shard_03` y `shard_08`

| Parámetro Comparativo | Clean-Room Reference (`shard_04` / `shard_07`) | Path-Penalty Stalled (`shard_03`) | Overthinking Paginator (`shard_08`) |
| :--- | :---: | :---: | :---: |
| **Duración Total de Pared** | **`210.0s`** | **`256.0s` (+46.0s)** | **`289.0s` (+79.0s)** |
| **Total de Turnos** | `8 turnos` | `10 turnos` | `18 turnos` |
| **Tiempo Pre-1st-Compile** | `198.0s` | `246.0s` | `273.0s` |
| **Tiempo Post-1st-Compile** | `12.0s` | `10.0s` | `16.0s` |
| **Errores de Exploración I/O** | `2` | `4` | `4` |
| **Turnos de Lectura de Manifest** | `1 turno` (Slice 1-20) | `1 turno` (Slice completo) | **`9 turnos consecutivos`** |
| **Causa Raíz del Desvío Temporal** | Ruta crítica ideal de inferencia continua | Fallo de sintaxis de path relativo + triple exploración | Bucle de paginación forzada sobre archivo de 230 KB |

#### Caso `shard_03` (256.0s, 10 turnos, 4 errores):
En el Turno 1 (Paso 1), el agente invocó `view_file` utilizando una ruta relativa:
```json
{"AbsolutePath": "courses/estadistica_3_s9_vdirect/work/dispatch/items/author_03.json"}
```
La herramienta Cortex de Antigravity SDK rechazó la llamada inmediatamente con error de validación de esquema: `AbsolutePath: Must be an absolute path`. Aunque el agente corrigió la ruta a `d:/Augusto/...` en el Turno 2, incurrió en tres exploraciones fallidas consecutivas en los pasos 7, 9 y 11:
1. `view_file("d:/.../work/templates/Hab-03.json")` -> `FileNotFoundError` (Paso 8).
2. `view_file("d:/.../work/shards/shard_03_data.py")` -> `FileNotFoundError` (Paso 10, intentando leer su propio archivo antes de escribirlo).
3. `view_file("d:/.../work/shards/shard_01_data.py")` -> `FileNotFoundError` (Paso 12, intentando copiar la estructura de un shard hermano aún en ejecución).
Estas 4 iteraciones innecesarias sumaron 46 segundos netos de latencia de inferencia y round-trips de contexto.

#### Caso `shard_08` (289.0s, 18 turnos, 4 errores) — El Bucle del Manifiesto:
El agente `shard_08` ([`2da986f3-14db-44b4-ad27-47f501625966`](file:///C:/Users/augus/.gemini/antigravity/brain/2da986f3-14db-44b4-ad27-47f501625966/.system_generated/logs/transcript.jsonl)) exhibió el comportamiento más patológico de lectura de archivos de todo el pipeline. Tras fracasar en la lectura de `Hab-08.json` y `shard_01_data.py` (Pasos 6 y 8), el agente entró en una obsesión reflexiva por encontrar los datos de su competencia en el archivo global [`pre_shard_manifest.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/shards/pre_shard_manifest.json) (229,318 bytes).
Debido a que `view_file` limita las respuestas a un máximo de 800 líneas o 46,080 bytes, el agente **ejecutó 8 llamadas consecutivas a `view_file`** en los pasos 9, 11, 13, 15, 17, 19, 21 y 23, paginando a través de fragmentos de líneas (`StartLine: 1, EndLine: 10`, `StartLine: 11, EndLine: 50`, etc.). En el Paso 12 incurrió en un error por intentar desplazar el offset más allá del rango:
```text
ContentOffset 80000 exceeds line range size 49646
```
Posteriormente, en el Paso 27, el agente intentó leer `shard_07_data.py` con la esperanza de que el subagente 07 ya hubiera terminado, generando un nuevo `FileNotFoundError`. Recién en el Turno 15 (Paso 29, +96s de pared) comenzó la escritura de `shard_08_data.py`. A pesar de este colapso exploratorio, una vez que escribió el archivo, **compiló limpiamente en el primer intento sin un solo fallo**.

---

### 2.3. Desmitificación de las "Compilaciones Tempranas" en `shard_01`, `shard_05` y `shard_06`

El reporte inicial de descomposición temporal (`shard_timing_decomposition.md`) indicaba anomalías en tres shards con tiempos `Pre-1st-Compile` sospechosamente bajos:
- `shard_01`: Pre-1st-Compile `57.0s` | Post-1st-Compile `172.0s`
- `shard_05`: Pre-1st-Compile `84.0s` | Post-1st-Compile `201.0s`
- `shard_06`: Pre-1st-Compile `74.0s` | Post-1st-Compile `172.0s`

La auditoría forense determinó que **estos registros fueron clasificados erróneamente por el analizador estático original**. 

#### Evidencia del Transcript:
En `shard_01` ([`201b96e8-48d9-4fa8-bee8-ac42eeecddc0`](file:///C:/Users/augus/.gemini/antigravity/brain/201b96e8-48d9-4fa8-bee8-ac42eeecddc0/.system_generated/logs/transcript.jsonl)), en el Turno 7 (Paso 13, timestamp `2026-10-31T17:45:51Z`, t = +42.0s desde el inicio), el subagente ejecutó la siguiente llamada:
```json
{
  "name": "run_command",
  "args": {
    "CommandLine": "& \"D:/Augusto/personal_portfolio/Tops_academy/.venv/Scripts/python.exe\" .agents/skills/content-to-course/compile_shard.py --help",
    "toolSummary": "Check compile_shard CLI options"
  }
}
```
El analizador estático detectó la subcadena `compile_shard.py` dentro de una invocación de `run_command` y la etiquetó como la "primera compilación del shard", cuando en realidad fue una consulta de flags `--help` en la terminal.
La secuencia cronológica real demostrada en los logs forenses fue:
1. `t = 00:00` (17:45:09Z): Arranque del agente e ingesta de `author_01.json`.
2. `t = 00:42` (17:45:51Z): Paso 13 -> Ejecuta `compile_shard.py --help` (42s).
3. `t = 01:06` (17:46:15Z): Paso 15 -> Escribe [`shard_01_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/shards/shard_01_data.py) (7,465 bytes).
4. `t = 03:08` (17:48:17Z): Paso 17 -> **Verdadera primera compilación del código** con `--strict --min-archetypes 4`. Resultado: `PASS (30 items, 0 errors)`.
5. `t = 03:26` (17:48:35Z): Paso 19 -> Envía mensaje `DONE` al orquestador.
6. `t = 03:34` (17:48:43Z): Paso 21 -> Finalización en reposo.

Idéntico patrón ocurrió en `shard_05` (Paso 13, t = +72.0s ejecutando `--help`) y `shard_06` (Paso 9, t = +63.0s ejecutando `--help`). **Ningún subagente sufrió errores de compilación prematura ni ciclos de remediación fallida.**

---

## 3. Inquiry 2: Transcripciones y Taxonomía Forense de Errores (49 Globales vs 22 en Shards 01–09)

En el run global `592de77b`, el sistema catalogó **49 errores de herramientas**. Dentro del subconjunto de Shards 01 al 09, se identificaron **exactamente 22 errores**.

### 3.1. Clasificación Taxonómica de Errores en Shards 01–09

```mermaid
pie title Distribución de Errores en Shards 01-09 (Total: 22)
    "Sondeo a templates inexistentes (Hab-XX.json)" : 9
    "Sondeo a shards hermanos en paralelo (shard_01/07)" : 7
    "Sondeo al propio archivo destino no creado" : 4
    "Error de ruta relativa en view_file" : 1
    "Desbordamiento de ContentOffset" : 1
```

| Categoría Técnica | Ocurrencias | Subagentes Involucrados | Causa Raíz Sistémica |
| :--- | :---: | :--- | :--- |
| **Sondeo de plantillas inexistentes (`work/templates/Hab-XX.json`)** | **9** | Shards 01, 02, 03, 04, 05, 06, 07, 08, 09 | Desfase temporal en el pipeline: los subagentes asumen que las plantillas JSON ya fueron creadas por un paso previo, cuando en realidad las crea `compile_shard.py` durante esta misma etapa. |
| **Sondeo de shards hermanos concurrentes (`shard_01_data.py` / `shard_07`)** | **7** | Shards 03, 04, 05, 06, 08, 09 | Asunción errónea de ejecución secuencial: los agentes buscan un archivo canónico de referencia en `work/shards/` sin considerar que todos los shards fueron despachados en paralelo. |
| **Sondeo del propio archivo no creado (`shard_XX_data.py`)** | **4** | Shards 01, 03, 05, 07 | Comprobación de existencia o lectura defensiva previa a la escritura (`view_file` antes de `write_file`). |
| **Violación de contrato de ruta absoluta en `view_file`** | **1** | Shard 03 (Paso 2) | El agente emitió `courses/estadistica_...` omitiendo el drive letter y prefijo absoluto exigido por la herramienta de Cortex. |
| **Desbordamiento de buffer en `ContentOffset`** | **1** | Shard 08 (Paso 12) | Especificación de offset arbitrario (80,000) superior a la longitud del bloque activo (49,646) durante la paginación ciega. |

### 3.2. Catálogo Forense Detallado de Errores por Incidencia

A continuación se documentan las 22 incidencias con sus marcas de tiempo exactas, subagente emisor y mensaje de error literal de la plataforma:

1. **`shard_01` — Paso 6 (17:45:25Z):**
   - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/templates/Hab-01.json", StartLine: 1, EndLine: 50)`
   - *Error:* `declaring permissions: cortex tool view_file: convert tool call for permissions: model output error: invalid tool call error (invalid_args) failed to read file: GetFileAttributesEx d:/Augusto/.../work/templates/Hab-01.json: The system cannot find the path specified.`
2. **`shard_01` — Paso 8 (17:45:30Z):**
   - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/shards/shard_01_data.py", StartLine: 1, EndLine: 20)`
   - *Error:* `failed to read file: GetFileAttributesEx .../work/shards/shard_01_data.py: The system cannot find the file specified.`
3. **`shard_02` — Paso 6 (17:45:31Z):**
   - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/templates/Hab-02.json")`
   - *Error:* `GetFileAttributesEx .../work/templates/Hab-02.json: The system cannot find the path specified.`
4. **`shard_03` — Paso 2 (17:45:15Z):**
   - *Tool Call:* `view_file(AbsolutePath: "courses/estadistica_3_s9_vdirect/work/dispatch/items/author_03.json")`
   - *Error:* `model output error: invalid tool call error (invalid_args) courses/estadistica_3_s9_vdirect/work/dispatch/items/author_03.json. Must be an absolute path.`
5. **`shard_03` — Paso 8 (17:45:26Z):**
   - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/templates/Hab-03.json")`
   - *Error:* `GetFileAttributesEx .../work/templates/Hab-03.json: The system cannot find the path specified.`
6. **`shard_03` — Paso 10 (17:45:31Z):**
   - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/shards/shard_03_data.py")`
   - *Error:* `GetFileAttributesEx .../work/shards/shard_03_data.py: The system cannot find the file specified.`
7. **`shard_03` — Paso 12 (17:45:38Z):**
   - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/shards/shard_01_data.py")`
   - *Error:* `GetFileAttributesEx .../work/shards/shard_01_data.py: The system cannot find the file specified.`
8. **`shard_04` — Paso 6 (17:45:23Z):**
   - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/templates/Hab-04.json", StartLine: 1, EndLine: 100)`
   - *Error:* `GetFileAttributesEx .../work/templates/Hab-04.json: The system cannot find the path specified.`
9. **`shard_04` — Paso 8 (17:45:28Z):**
   - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/shards/shard_01_data.py", StartLine: 1, EndLine: 60)`
   - *Error:* `GetFileAttributesEx .../work/shards/shard_01_data.py: The system cannot find the file specified.`
10. **`shard_05` — Paso 6 (17:45:22Z):**
    - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/templates/Hab-05.json")`
    - *Error:* `GetFileAttributesEx .../work/templates/Hab-05.json: The system cannot find the path specified.`
11. **`shard_05` — Paso 8 (17:45:28Z):**
    - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/shards/shard_05_data.py")`
    - *Error:* `GetFileAttributesEx .../work/shards/shard_05_data.py: The system cannot find the file specified.`
12. **`shard_05` — Paso 10 (17:45:34Z):**
    - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/shards/shard_01_data.py", StartLine: 1, EndLine: 60)`
    - *Error:* `GetFileAttributesEx .../work/shards/shard_01_data.py: The system cannot find the file specified.`
13. **`shard_06` — Paso 6 (17:45:23Z):**
    - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/templates/Hab-06.json", StartLine: 1, EndLine: 20)`
    - *Error:* `GetFileAttributesEx .../work/templates/Hab-06.json: The system cannot find the path specified.`
14. **`shard_06` — Paso 8 (17:45:29Z):**
    - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/shards/shard_01_data.py", StartLine: 1, EndLine: 40)`
    - *Error:* `GetFileAttributesEx .../work/shards/shard_01_data.py: The system cannot find the file specified.`
15. **`shard_07` — Paso 6 (17:45:22Z):**
    - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/templates/Hab-07.json")`
    - *Error:* `GetFileAttributesEx .../work/templates/Hab-07.json: The system cannot find the path specified.`
16. **`shard_07` — Paso 8 (17:45:29Z):**
    - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/shards/shard_07_data.py")`
    - *Error:* `GetFileAttributesEx .../work/shards/shard_07_data.py: The system cannot find the file specified.`
17. **`shard_08` — Paso 6 (17:45:24Z):**
    - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/templates/Hab-08.json")`
    - *Error:* `GetFileAttributesEx .../work/templates/Hab-08.json: The system cannot find the path specified.`
18. **`shard_08` — Paso 8 (17:45:29Z):**
    - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/shards/shard_01_data.py", StartLine: 1, EndLine: 60)`
    - *Error:* `GetFileAttributesEx .../work/shards/shard_01_data.py: The system cannot find the file specified.`
19. **`shard_08` — Paso 12 (17:45:49Z):**
    - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/shards/pre_shard_manifest.json", ContentOffset: 80000)`
    - *Error:* `Encountered error in step execution: ContentOffset 80000 exceeds line range size 49646`
20. **`shard_08` — Paso 28 (17:46:45Z):**
    - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/shards/shard_07_data.py", StartLine: 1, EndLine: 60)`
    - *Error:* `GetFileAttributesEx .../work/shards/shard_07_data.py: The system cannot find the file specified.`
21. **`shard_09` — Paso 6 (17:45:23Z):**
    - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/shards/shard_01_data.py", StartLine: 1, EndLine: 60)`
    - *Error:* `GetFileAttributesEx .../work/shards/shard_01_data.py: The system cannot find the file specified.`
22. **`shard_09` — Paso 8 (17:45:28Z):**
    - *Tool Call:* `view_file(AbsolutePath: "d:/Augusto/.../work/templates/C-01.json")`
    - *Error:* `GetFileAttributesEx .../work/templates/C-01.json: The system cannot find the path specified.`

---

## 4. Inquiry 3: Inspección Forense de Código y Artefactos (`shard_01_data.py` a `shard_09_data.py`)

### 4.1. Análisis Estructural de Tuplas: Dominancia de Form A (9 Elementos)

La inspección mediante árbol sintáctico abstracto (AST) de los 9 archivos en [`courses/estadistica_3_s9_vdirect/work/shards/`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/shards) reveló una adopción casi uniforme del formato histórico denominado **Form A (tuplas de 9 elementos)**:

```python
# Estructura Form A observada en Shards 01-09:
(
    cid,        # [0] str: Identificador de competencia ("Hab-01", "C-01", etc.)
    qtype,      # [1] str: Tipo de reactivo ("multiple_choice")
    stems,      # [2] list: Variantes de enunciado con placeholders @var@
    gen_fn,     # [3] callable: Función generadora (rng -> dict con 'vars', 'correct', 'distractors')
    ver_fn,     # [4] callable: Función validadora formal (res -> bool)
    sol,        # [5] str: Explicación y resolución canónica paso a paso
    target_kc,  # [6] str: Concepto clave evaluado ("Derivación de la Descomposición del ECM")
    dids,       # [7] list: Lista de IDs de distractores canónicos (['D-Hab01-01', ...])
    t_meta      # [8] tuple: Metadatos de fuente (doc, página, tipo)
)
```

En algunos shards (`shard_02`, `shard_04`, `shard_06`, `shard_08`), los autores insertaron un décimo elemento (`[9]`), pero este fue instanciado exclusivamente como una lista vacía `[]`:
```python
# Ejemplo en shard_02_data.py (Línea 61):
("Hab-02", "multiple_choice", stems_1, gen_hab02_1, ver_ok, sol, 'Deducción de Momentos de la Media Muestral', dids, t_meta, [])
```

#### La Ausencia Total de Parámetros Pedagógicos:
**En ninguna de las 40 tuplas definidas a lo largo de los 9 shards existe un elemento asignado a `difficulty` ni a `hints` pedagógicas personalizadas.**
El contrato de tupla de 11 elementos (Form B: `(cid, qtype, stems, gen_fn, ver_fn, sol, target_kc, dids, t_meta, difficulty, hints)`) fue completamente ignorado por las órdenes de trabajo de despacho (`author_01.json` a `author_09.json`), las cuales instruían expresamente:
> *"Usa tuplas de 9 elementos con `[]` en `target_misconceptions` (donde compile_shard.py los hereda automáticamente desde cta.json)."*

---

### 4.2. El Mecanismo Coercitivo de `compile_shard.py` (Líneas 1421 y 1509–1527)

Al ejecutarse el compilador [`compile_shard.py`](file:///D:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py), las tuplas de Form A ingresan en la rutina de extracción de plantillas (líneas 1415–1446):

```python
# compile_shard.py (Líneas 1420-1446):
src_ref_raw = t[8]
diff_raw = "medium"                      # <--- HARDCODED A "medium"
hints_raw = list(t[9]) if len(t) >= 10 and isinstance(t[9], (list, tuple)) else []
tpl_id = f"T-{cid}" if not cid.startswith("T-") else cid

# Determine difficulty and bloom
if isinstance(diff_raw, (list, tuple)) and len(diff_raw) >= 2:
    difficulty = str(diff_raw[0]).lower().strip()
    bloom = str(diff_raw[1]).capitalize().strip()
elif isinstance(diff_raw, str):
    difficulty = diff_raw.lower().strip()
    bloom = "Understand"                 # <--- HARDCODED A "Understand"
else:
    difficulty = "medium"
    bloom = "Understand"
```

Dado que `diff_raw` se asigna a `"medium"`, la bifurcación condicional entra indefectiblemente en la línea 1438, asignando:
- `difficulty = "medium"`
- `bloom = "Understand"`

#### El Fallback de Pistas Mad-Libs (Líneas 1504–1527):
Dado que `hints_raw` es `[]` (o tiene longitud 0), no cumple la condición `len(hints_raw) >= 3`. En consecuencia, el compilador ejecuta la síntesis por defecto:

```python
# compile_shard.py (Líneas 1508-1527):
c_name = cta_comp.get("name") or cta_comp.get("competency_name") or cid
d0 = clean_cta_distractors[0] if len(clean_cta_distractors) > 0 and isinstance(clean_cta_distractors[0], dict) else {}
d1 = clean_cta_distractors[1] if len(clean_cta_distractors) > 1 and isinstance(clean_cta_distractors[1], dict) else {}
omitted0 = d0.get("omitted_step") or d0.get("wrong_belief") or ""
omitted1 = d1.get("omitted_step") or d1.get("wrong_belief") or ""

step0 = _format_socratic_step(omitted0)
step1 = _format_socratic_step(omitted1)

hint1 = f"Identifique la estructura conceptual de {c_name}: analice las relaciones formales y condiciones teóricas del modelo."
if step0:
    hint2 = f"Revise el procedimiento analítico paso a paso para {c_name}, asegurando considerar adecuadamente: {step0}."
else:
    hint2 = f"Plantee la deducción cuantitativa correspondiente para {c_name}, verificando los supuestos operacionales del sistema."
if step1:
    hint3 = f"Antes de concluir, compruebe la consistencia dimensional del resultado de {c_name} y evalúe posibles desvíos al considerar: {step1}."
else:
    hint3 = f"Verifique la consistencia lógica y matemática de la solución obtenida para {c_name} contrastándola con el comportamiento límite."
hints = [hint1, hint2, hint3]
```

---

### 4.3. Impacto Psicométrico y Degradación del Path-to-Mastery

La combinación de Form A en los shards y la coerción estática de `compile_shard.py` genera severas distorsiones en los reactivos publicados en [`estadistica_3_s9_vdirect.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect.json):

```mermaid
graph TD
    A["Autor Shard (Form A 9-element)"] -->|Omite difficulty y hints| B["compile_shard.py (L1421, L1509)"]
    B --> C["Coerción: diff='medium' & bloom='Understand'"]
    B --> D["Síntesis Mad-Libs de Pistas"]
    C --> E["280 Reactivos Aplanados Psicométricamente"]
    D --> F["Pistas Genéricas Descontextualizadas"]
    D --> G["Fuga de LaTeX Crudo ($theta_hat$, $Y_bar$)"]
    E --> H["Colapso de Evaluación Adaptativa (CAT Imposible)"]
    F --> I["Pérdida de Andamiaje Socrático Real"]
```

1. **Aplanamiento Cognitivo Total (280/280 Reactivos):**
   - El 100% de los reactivos de estas 10 competencias quedaron clasificados en la taxonomía de Bloom como `"Understand"`. No existe un solo reactivo clasificado en `"Apply"`, `"Analyze"` o `"Evaluate"`, a pesar de que competencias como `Hab-01`, `Hab-03`, `Hab-07` y `Hab-08` exigen deducciones algebraicas multietapa altamente complejas.
   - La dificultad fue congelada en `"medium"` para los 280 reactivos. Esto anula por completo la capacidad de la plataforma Top's Academy para desplegar **Mastery Learning Adaptativo** o algoritmos de Teoría de Respuesta al Ítem (TRI/CAT), ya que el motor no puede diferenciar entre ejercicios de andamiaje introductorio y problemas de discriminación avanzada.
2. **Devaluación Pedagógica de las Pistas:**
   - Las tres pistas que recibe el estudiante no ofrecen guía heurística ni pasos intermedios. La pista 1 es siempre un cliché idéntico: *"Identifique la estructura conceptual de [Nombre de Competencia]..."*.
   - Las pistas 2 y 3 se limitan a citar el paso omitido del distractor canónico precedido por la frase *"asegurando considerar adecuadamente:"*, lo cual en ocasiones revela involuntariamente el distractor de la pregunta o confunde al estudiante con terminología abstracta.

---

### 4.4. Fuga de Variables Crudas y Sintaxis LaTeX Corrupta

La inspección de los reactivos publicados reveló la presencia de texto corrupto y tokens sin escapar insertados por el motor de síntesis de pistas:

#### Caso 1: Fuga de `$theta_hat$` en Competencia `Hab-01` (30 de 30 reactivos afectados):
En el archivo original de CTA, el distractor `D-Hab01-01` definía:
`omitted_step = "Omitir la evaluación de la esperanza del desvío E[$theta_hat$ - E[$theta_hat$]] = 0"`.
Al concatenarse en la línea 1520 de `compile_shard.py`, la Pista 2 de los 30 reactivos de `Hab-01` en el curso final publicado reza textualmente:
> *"Revise el procedimiento analítico paso a paso para Derivación de la Descomposición del Error Cuadrático Medio, asegurando considerar adecuadamente: omitir la evaluación de la esperanza del desvío E[$theta_hat$ - E[$theta_hat$]] = 0."*

El estudiante visualiza la cadena `$theta_hat$` en lugar de la macro LaTeX interpretada $\hat{\theta}$.

#### Caso 2: Fuga de `$Y_bar$` y `$sigma^2$` en Competencia `Hab-03` (30 de 30 reactivos afectados):
En `Hab-03` ([`courses/.../templates/Hab-03.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/templates/Hab-03.json)), la Pista 3 sintetizada presenta:
> *"Antes de concluir, compruebe la consistencia dimensional del resultado de Demostración de Insesgadez de la Cuasivarianza y Sesgo de m2 y evalúe posibles desvíos al considerar: omitir la aplicación del resultado de la varianza de la media muestral Var($Y_bar$) = $sigma^2$/n en la ecuación."*

El uso de `$Y_bar$` sin barra invertida (`\bar{Y}`) constituye un error tipográfico directo transferido desde la arquitectura de CTA hacia la interfaz estudiantil.

---

### 4.5. Contaminación Semántica Inter-Dominio (Prompt Bleed)

Se constató una evidente **contaminación por copia literal de directivas de prompt** en los enunciados generados por los autores:

```python
# shard_01_data.py (Línea 103, Arquetipo 3):
r"Al perturbar el estimador reduciendo su sesgo a @b2:.4f@ con varianza invariable \operatorname{Var}(\hat{\theta}_n) = @v:.4f@, ¿cuál es el nuevo \operatorname{ECM}'(\hat{\theta}_n) tras la estática comparativa?"

# shard_01_data.py (Líneas 106 y 108, Arquetipo 4):
r"En la condición de frontera donde el estimador es insesgado (\operatorname{Sesgo}(\hat{\theta}_n) = 0)..."
r"Bajo la condición de frontera de insesgadez estricta (\mathbb{E}[\hat{\theta}_n] = \theta)..."
```

#### Trazabilidad Forense:
En la instrucción de la orden de trabajo (`author_01.json` a `author_09.json`), la sección `[M3-ARCHETYPES]` exigía textualmente:
> *"DEBES cubrir los 4 arquetipos disjuntos definiendo 4 tuplas en TEMPLATES por cada competencia asignada (1. Directo / Frontal, 2. Inverso / Diagnóstico, 3. Perturbación / Estática Comparativa, 4. Frontera / Casos Límite)."*

Los modelos LLM (Flash) interpretaron erróneamente los nombres pedagógicos de las categorías (*"Estática Comparativa"*, concepto exclusivo de la Microeconomía; y *"Condición de Frontera"*, concepto de Ecuaciones Diferenciales y Física Matemática) como parte del lenguaje técnico de las preguntas estadísticas, incorporándolos directamente en la redacción de los problemas sobre el Error Cuadrático Medio.

---

### 4.6. Validación Matemática de Generadores y Espacio Paramétrico (`[TPL-VAR]`)

A pesar de los vicios psicométricos causados por Form A, **la implementación de los generadores estocásticos (`gen_*(rng)`) en los 9 shards fue de alta calidad matemática**:
1. **Espacio Paramétrico Robusto:** Las pruebas de estrés con 50 semillas pseudo-aleatorias determinaron que las 40 plantillas producen entre **48 y 50 instancias numéricas únicas sobre 50 ejecuciones**, superando holgadamente el mínimo de 30 requerido para competencias de tipo habilidad (`Hab-*`) y 20 para conocimiento (`C-*`).
2. **Generación Completa de 6 Distractores:** Ningún generador colapsó a listas de distractores vacías ni activó mecanismos de fallback. Cada generador produce exactamente 6 distractores matemáticos con valores plausibles basados en las desviaciones canónicas del CTA.
3. **Resolución Anticolisión Activa:** Todos los shards implementaron bucles deterministas de resolución de colisiones numéricas:
   ```python
   # shard_01_data.py (Líneas 69-73):
   vals = {ans}
   for i in range(len(ds)):
       while ds[i] in vals or ds[i] <= 0:
           ds[i] = round(ds[i] + 0.0103, 4)
       vals.add(ds[i])
   ```
   Esto garantizó que en los 280 reactivos generados jamás se presentaran dos opciones de respuesta idénticas.

---

## 5. Cuadro Comparativo por Shard (Shards 01 al 09)

| Shard | Archivo Python | Líneas | Tamaño | Compilación CLI | Arquetipos | Unicidad (50 Seeds) | Errores de Exploración | Fugas Detectadas |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`01`** | [`shard_01_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/shards/shard_01_data.py) | 121 | 7,465 B | `--strict --min-archetypes 4` | 4 (Form A) | 48–50 / 50 | 2 (Hab-01.json, shard_01.py) | `$theta_hat$` en Pista 2; "estática comparativa" en stem |
| **`02`** | [`shard_02_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/shards/shard_02_data.py) | 67 | 5,483 B | `--strict --min-archetypes 4` | 4 (Form A) | 50 / 50 | 1 (Hab-02.json) | Ninguna en stems; Pistas Mad-Libs aplanadas |
| **`03`** | [`shard_03_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/shards/shard_03_data.py) | 80 | 4,745 B | `--strict --min-archetypes 4` | 4 (Form A) | 48–50 / 50 | 4 (Path relativo, Hab-03, shard 03/01) | `$Y_bar$` y `$sigma^2$` en Pista 3 |
| **`04`** | [`shard_04_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/shards/shard_04_data.py) | 80 | 5,582 B | `--strict --min-archetypes 4` | 4 (Form A) | 48–50 / 50 | 2 (Hab-04.json, shard_01.py) | Gold Standard Clean-Room; Pistas aplanadas |
| **`05`** | [`shard_05_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/shards/shard_05_data.py) | 86 | 6,079 B | `--strict --min-archetypes 4` | 4 (Form A) | 49–50 / 50 | 3 (Hab-05.json, shard 05/01) | Pistas Mad-Libs aplanadas; CLI `--help` probe |
| **`06`** | [`shard_06_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/shards/shard_06_data.py) | 73 | 6,309 B | `--strict --min-archetypes 4` | 4 (Form A) | 49 / 50 | 2 (Hab-06.json, shard_01.py) | CLI `--help` probe; Pistas Mad-Libs |
| **`07`** | [`shard_07_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/shards/shard_07_data.py) | 75 | 5,613 B | `--strict --min-archetypes 4` | 4 (Form A) | 48–50 / 50 | 2 (Hab-07.json, shard_07.py) | Co-Fastest Clean-Room; Pistas aplanadas |
| **`08`** | [`shard_08_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/shards/shard_08_data.py) | 85 | 5,229 B | `--strict --min-archetypes 4` | 4 (Form A) | 49–50 / 50 | 4 (Hab-08, manifest offset, shard 01/07) | 8 turnos de paginación en manifest; Pistas aplanadas |
| **`09`** | [`shard_09_data.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/estadistica_3_s9_vdirect/work/shards/shard_09_data.py) | 115 | 12,001 B | `--strict --min-archetypes 4` | 8 (Form A) | 49–50 / 50 | 2 (shard_01.py, C-01.json) | 2 competencias (`C-01`, `C-02`); Pistas aplanadas |

---

## 6. Recomendaciones Arquitecturales y Mejoras Sistémicas para el Engine C2C

Para prevenir los problemas identificados en futuros despliegues de la plataforma Top's Academy, se proponen cuatro intervenciones técnicas concretas:

### 6.1. Adopción Estricta de Form B (Tuplas de 11 Elementos) en el Contrato de Despacho
Las plantillas generadas en `author_XX.json` deben especificar obligatoriamente los elementos `[9]` (`difficulty`) y `[10]` (`hints`):
```python
# Contrato canónico propuesto (Form B 11-element):
TEMPLATES = [
    (
        "Hab-01",
        "multiple_choice",
        stems_1,
        gen_hab01_1,
        ver_ok,
        sol_1,
        "Derivación de la Descomposición del ECM",
        dids,
        t_meta,
        ("medium", "Apply"),  # [9] Dificultad y Taxonomía de Bloom contextual
        [                     # [10] Pistas Socráticas Específicas
            r"Recuerde que el ECM se define como la esperanza cuadrática del error: $\mathbb{E}[(\hat{\theta}_n - \theta)^2]$.",
            r"Introduzca el artificio algebraico sumando y restando $\mathbb{E}[\hat{\theta}_n]$ dentro del binomio antes de expandir.",
            r"Aplique la linealidad del operador esperanza y justifique por qué el término cruzado se anula."
        ]
    )
]
```

### 6.2. Eliminación del Fallback Coercitivo en `compile_shard.py`
En [`compile_shard.py`](file:///D:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_shard.py#L1421), debe eliminarse la asignación por defecto `diff_raw = "medium"`. Si una tupla no provee dificultad y nivel cognitivo, el compilador debe emitir una advertencia o inferir el nivel en función de la naturaleza de la competencia (`Hab-*` -> `Apply`/`Analyze`; `C-*` -> `Understand`/`Analyze`).

### 6.3. Sanitización de Macros LaTeX en la Fase CTA (`check_cta.py`)
Incorporar una regla de validación estricta en el validador de CTA que rechace la generación de pasos omitidos o creencias erróneas con sintaxis LaTeX rota (`$theta_hat$`, `$Y_bar$`, `$sigma^2$`), exigiendo macros válidas (`\hat{\theta}`, `\bar{Y}`, `\sigma^2`).

### 6.4. Blindaje del Entorno de Aislamiento para Eliminar Sondeos Ciegos
Para suprimir los 22 errores de exploración que demoran el arranque de los shards:
- Incluir en el prompt del autor una directiva explícita de pre-condición:
  > *"PROHIBIDO ejecutar view_file sobre `work/templates/` o shards hermanos (`shard_01_data.py`). El entorno se ejecuta en paralelo y dichos archivos no existen al inicio de su ejecución."*
- Proporcionar un mini-ejemplo canónico en memoria dentro de la orden de trabajo (`author_XX.json`) para que los modelos no sientan el reflejo de buscar archivos de referencia en el disco.
