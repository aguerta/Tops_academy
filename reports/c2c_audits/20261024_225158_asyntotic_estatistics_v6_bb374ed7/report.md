# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Asyntotic Estatistics V3 (`asyntotic_estatistics_v6`)

**Fecha de Auditoría:** `2026-10-25 04:13:43 UTC`  
**Conversación Orquestadora:** [`bb374ed7-5932-4d73-94c1-4b5064a1efb2`](conversation://bb374ed7-5932-4d73-94c1-4b5064a1efb2)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\asyntotic_estatistics_v6\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `2 archivos` (52 págs / 3.44 MB) | ECONOMETRIC ANALTYSIS FIFTH EDITION  -  William H_ Greene  -  5th ed_, Upper Saddle River, N_J, New Jersey, 2003  -  Prentice Hall PTR  -  isbn13 9780130661890  -  d139b0dca2a0c7d0984d735f6be1944e  -  Anna’s Archive-93.pdf, Econometric Analysis (Greene) (z-library.sk, 1lib.sk, z-lib.sk)-923-946.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`25 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`16 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`26 subagentes`** | Visión (0), CTA (2), Autores (16), Jueces (0) |
| **Reactivos Finales Validados** | **`0 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`2,850,825` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`826,798` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`15,101,484` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`4,404,898` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`19,506,382` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`0.0 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`0.0 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`780,255.3 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`108,589.1 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`375,122.7 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`0.0 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`0.0 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`3.55x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `bb374ed7`):** `4 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `shard`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-10-25 03:08:11` | `0.01s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-10-25 03:08:11` | `0.04s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\asyntotic_estatistics_v6\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-10-25 03:16:31` | `0.28s` | `885,598` (`387,572` act) | 2 | `competencies=25` |
| **`02_shard`** | `2026-10-25 03:16:35` | `0.03s` | `0` (`0` act) | 0 | `shards=16` |

---

### 3.1. Stage 1A: Preprocesamiento de Visión
- **Subagentes de Visión Desplegados:** `0 agentes en paralelo`
- **Tiempo de Pared de la Etapa (Máximo / Critical Path):** **`0.0s`** (`0.0 min`)
- **Agente Determinante del Camino Crítico:** `N/A`

| Subagente de Visión | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

---

### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)
- **Arquitectura:** `MAPREDUCE (2 Mappers)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`451.0s`** (determinado por `Cognitive Task Analysis Architect part_01`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`0.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`451.0s`** (`7.5 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cognitive Task Analysis Architect part_01** | Mapper | 11 | 175,254 | 58,741 | 359,135 | 0 | **451.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 9 | 109,252 | 47,017 | 231,225 | 2 | **330.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `16 shards concurrentes`
- **Duración Mínima de Shard:** `208.0s` | **Mediana:** `299.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`727.0s`** (`12.1 min`) por `Shard Author shard_09`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+428.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`108,589.1 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_07** | `C-04, C-05` | 2 | 92,600 | 41,873 | 306,680 | 134,473 | **67,236.5** | 10 | 3 | **287.0s** |
| **Shard Author shard_08** | `C-07, C-08` | 2 | 121,461 | 50,095 | 276,801 | 171,556 | **85,778.0** | 9 | 2 | **371.0s** |
| **Shard Author shard_09 🛑** | `C-11, C-12` | 2 | 241,514 | 55,424 | 1,068,477 | 296,938 | **148,469.0** | 24 | 5 | **727.0s** |
| **Shard Author shard_10** | `C-01, H-01` | 2 | 108,126 | 35,100 | 625,110 | 143,226 | **71,613.0** | 18 | 3 | **268.0s** |
| **Shard Author shard_11** | `H-02, C-02` | 2 | 143,480 | 45,693 | 729,937 | 189,173 | **94,586.5** | 17 | 2 | **322.0s** |
| **Shard Author shard_12** | `H-03, C-03` | 2 | 205,538 | 45,228 | 281,895 | 250,766 | **125,383.0** | 12 | 0 | **310.0s** |
| **Shard Author shard_13** | `C-06, H-04` | 2 | 109,754 | 44,437 | 712,440 | 154,191 | **77,095.5** | 21 | 5 | **367.0s** |
| **Shard Author shard_14** | `H-05, C-09` | 2 | 86,765 | 43,341 | 256,791 | 130,106 | **65,053.0** | 8 | 1 | **299.0s** |
| **Shard Author shard_15** | `H-06, C-10` | 2 | 124,957 | 47,217 | 954,684 | 172,174 | **86,087.0** | 17 | 1 | **357.0s** |
| **Shard Author shard_01** | `Hab-01` | 1 | 134,230 | 35,647 | 238,049 | 169,877 | **169,877.0** | 8 | 2 | **238.0s** |
| **Shard Author shard_02** | `Hab-02` | 1 | 115,906 | 37,865 | 264,297 | 153,771 | **153,771.0** | 10 | 2 | **249.0s** |
| **Shard Author shard_03** | `Hab-03` | 1 | 128,506 | 29,974 | 225,755 | 158,480 | **158,480.0** | 8 | 2 | **208.0s** |
| **Shard Author shard_04** | `Hab-04` | 1 | 84,845 | 41,046 | 236,669 | 125,891 | **125,891.0** | 9 | 3 | **266.0s** |
| **Shard Author shard_05** | `Hab-05` | 1 | 112,723 | 46,130 | 210,390 | 158,853 | **158,853.0** | 9 | 3 | **316.0s** |
| **Shard Author shard_06** | `Hab-06` | 1 | 98,806 | 35,107 | 429,748 | 133,913 | **133,913.0** | 14 | 3 | **246.0s** |
| **Shard Author shard_16** | `H-07` | 1 | 128,022 | 43,317 | 293,286 | 171,339 | **171,339.0** | 12 | 2 | **293.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ❌ NO PASARON AL PRIMER INTENTO (REQUIRIÓ INTERVENCIONES)  
> Los blind judges y la verificación psicométrica registraron discrepancias que requirieron correcciones. La validación previa operó con discrepancias detectadas, requiriendo rondas de auto-reparación o intervención técnica.

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `50 reactivos` (25 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `0 jueces` | Aislamiento epistémico en Stage 5 |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | 0 violaciones iniciales registradas |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Bucle de Auto-Reparación**: Se ejecutó RepairLoop sobre el lote de evaluación.
- 2. **Intervenciones de Supervisor (0 operaciones)**: Operaciones sobre archivos de reactivos.
- 3. **Certificación y Verificación Final**: Se concluyó la validación tras 1 iteraciones sobre el lote de 50 reactivos.

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared del Orquestador:** `41.25 min` (`2475.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `5.0 min` (`297.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `1.2 min` (`73.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `1.1 min` (`66.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_09
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_09 tardó 727.0s frente a la mediana de 299.0s (+428.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

### ⚠️ [MEDIUM] Fricción de Herramientas en 9 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_07 acumularon fallos en consola (3 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `171 turnos`
- **Volumen Total de Razonamiento:** `611,840 caracteres`
- **Razonamiento del Orquestador:** `27 turnos` (14,665 chars)
- **Razonamiento de Subagentes:** `144 turnos` (597,175 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect part_01** | 8 | 36,858 | 0 |
| **Cognitive Task Analysis Architect part_02** | 7 | 36,741 | ⚠️ 2 |
| **Shard Author shard_07** | 4 | 32,196 | ⚠️ 3 |
| **Shard Author shard_08** | 5 | 34,401 | ⚠️ 2 |
| **Shard Author shard_09** | 10 | 43,037 | ⚠️ 5 |
| **Shard Author shard_10** | 7 | 22,935 | ⚠️ 3 |
| **Shard Author shard_11** | 9 | 33,268 | ⚠️ 2 |
| **Shard Author shard_12** | 4 | 39,171 | 0 |
| **Shard Author shard_13** | 9 | 26,687 | ⚠️ 5 |
| **Shard Author shard_14** | 5 | 32,775 | ⚠️ 1 |
| **Shard Author shard_15** | 7 | 37,584 | ⚠️ 1 |
| **Shard Author shard_01** | 5 | 24,140 | ⚠️ 2 |
| **Shard Author shard_02** | 6 | 27,109 | ⚠️ 2 |
| **Shard Author shard_03** | 6 | 20,282 | ⚠️ 2 |
| **Shard Author shard_04** | 7 | 30,621 | ⚠️ 3 |
| **Shard Author shard_05** | 5 | 35,393 | ⚠️ 3 |
| **Shard Author shard_06** | 7 | 23,375 | ⚠️ 3 |
| **Shard Author shard_16** | 6 | 31,898 | ⚠️ 2 |
| **Subagent** | 9 | 17,008 | ⚠️ 3 |
| **Subagent** | 6 | 6,300 | ⚠️ 3 |
| **Subagent** | 4 | 2,663 | 0 |
| **Subagent** | 3 | 851 | 0 |
| **Subagent** | 1 | 354 | 0 |
| **Subagent** | 1 | 220 | 0 |
| **Subagent** | 1 | 819 | 0 |
| **Subagent** | 2 | 489 | ⚠️ 1 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*

---

## 9. Análisis Forense Especializado (Director, Sandbox Timeout, CTA y Estándar de 4 Arquetipos)

### 9.1. ¿Por qué los 16 Shards aprobaron individualmente (`compile_shard.py`), pero fallaron en la validación global (`run.py --stage templates`) disparando 8 Reparadores innecesarios?

#### A. Prueba Empírica de Determinismo y Velocidad Real de las Plantillas
Se ejecutó un benchmark aislado (`single-thread`) sobre las **25 competencias × 4 arquetipos × 50 semillas = 5,000 ejecuciones** de `generate(seed)` + `verify(vars, ans)` en `courses/asyntotic_estatistics_v6/work/templates/*.json`:
- **Fallos / Loops infinitos reales:** **`0 / 5,000` (`0.0%`)**.
- **Tiempo total por competencia (200 corridas de sandbox):** entre **`1.78 s` y `4.10 s`**.
- **Tiempo máximo de una semilla individual en todo el curso:** **`40.7 ms` (`0.0407 s`)** — es decir, **20 veces por debajo** del límite de `0.8 s` (`800 ms`). Specifically: `C-05` máx `29.7 ms`, `C-11` máx `13.9 ms`, `C-08` máx `20.4 ms`, `H-03` máx `29.1 ms`.

#### B. Causa Raíz #1: Inanición del GIL en `ThreadPoolExecutor(max_workers=16)` + `sys.settrace` contra Reloj de Pared (`time.perf_counter()`)
1. **Validación individual (`compile_shard.py`):** Valida únicamente 1 o 2 archivos JSON (`max_workers <= 2`). Sin contención de hilos, cada semilla tarda `~10–30 ms` y los **16 shards aprobaron al 100%**.
2. **Validación global (`run.py --stage templates` -> `check_templates.py:2941`):**
   - `check_templates_file_or_dir(templates_dir)` lanza un `ThreadPoolExecutor(max_workers=16)` dentro de **un único proceso de Python** compartiendo un solo **Global Interpreter Lock (GIL)**.
   - Dentro de `execute_sandbox_batch` (`engine/sandbox.py:535-589`) -> `run_code_in_env` (`engine/sandbox.py:448-493`), por **cada una de las 50 semillas × 2 funciones (`generate` y `verify`) × 100 plantillas = 10,000 invocaciones**, se ejecuta redundantemente:
     1. `validate_code_ast(code_str)` (`ast.parse` + recorrido completo del AST),
     2. `build_sandbox_globals()`,
     3. `compile(code_str, "<sandbox>", "exec")`,
     4. `exec(compiled, env)`, y finalmente
     5. `call_with_timeout(..., timeout=0.8)`.
   - En `call_with_timeout` (`engine/sandbox.py:411, 431`), el timeout se mide con **reloj de pared (`time.perf_counter() + 0.8`)** (no tiempo de CPU del hilo `time.thread_time()`), mientras los 16 hilos activan simultáneamente `sys.settrace(_timeout_tracer)` (que penaliza la ejecución del intérprete entre 10x y 30x).
   - Cuando un hilo entra a `call_with_timeout` y cede el GIL mientras los otros 15 hilos ejecutan `ast.parse`, `compile()`, `validate_katex_syntax` o recolección de basura, transcurren **`> 0.8 s` de tiempo de pared esperando el GIL** antes de que la semilla termine sus `15 ms` de trabajo real.
   - **Evidencia irrefutable en los 3 intentos del Director:**
     - **Intento 1 (Paso 106):** Timeout estocástico en `C-11` (seed 138), `C-05` (seed 133), `H-05` (seed 110) y `H-02` (seed 110).
     - **Intento 2 (Paso 122, sin ningún cambio de código):** ¡`C-11`, `H-05` y `H-02` pasan limpiamente! En su lugar, fallan aleatoriamente `C-08` (seed 141), `C-05` (seed 108 — distinta semilla), `C-10` y `C-02`.
     - **Intento 3 (Paso 167):** Fallan `C-05` (seed 133), `H-03` (seed 124), `C-08`, `C-09`, más 25 bloqueos por `BUDGET HALT`.
   - **Doble compilación innecesaria (`run.py:738-748`):** Además, `run_stage_templates` recompila secuencialmente los 16 `shard_*_data.py` antes de llamar a `check_templates_file_or_dir(templates_dir)`, añadiendo `~3.5 min` de sobrecarga por cada invocación de `run.py --stage templates`.

#### C. Causa Raíz #2: Bug del Booleano Global `is_clean` en el Circuit-Breaker `BUDGET HALT` (`check_templates.py:3153-3221`)
- En `check_templates.py:3153`, el bucle `for cid in processed_comp_ids:` actualiza `.check_attempts/<cid>.json` evaluando `if is_clean:`, donde `is_clean = (len(errors) == 0)` es el estado **global de todo el directorio** (las 25 competencias), y **no** si la competencia `cid` tuvo errores.
- Como resultado, cada vez que 1 competencia sufrió un timeout espurio por el GIL, `check_templates.py` incrementó el contador de fallos `attempts` de **las 25 competencias del curso simultáneamente**. En la 3ra corrida de `run.py --stage templates` (Paso 167), competencias 100% sanas (`C-01`, `C-03`, `H-03`, `H-04`, `H-07`, etc.) alcanzaron `attempts == 3` con el mismo `comp_hash` y dispararon falsos `[!] BUDGET HALT` en cascada.

#### D. Causa Raíz #3: Tres Bugs en `dispatch.py dispatch-repair` que dejaron a los Reparadores a Ciegas
1. **`run.py --stage templates` no escribe `work/reports/templates_report.json` (`run.py:756`):** `dispatch-repair` busca ese archivo (`dispatch.py:1557`); al no existir y ver que `work/templates/<cid>.json` sí existen, cae en el fallback `{"manual_request": True}` (`dispatch.py:1684`). Por eso los 4 reparadores de la Ola 1 (`C-05`, `C-08`, `C-10`, `C-02`) recibieron órdenes vacías de diagnóstico, corrieron `compile_shard.py` en su shard individual, vieron `PASS` inmediato en el 1er intento (`0` ediciones en `C-08`, `C-10`, `C-02`) y reportaron `DONE`.
2. **Falta de `.split(",")` en `--ids` (`dispatch.py:1674, 2071`):** Cuando el Director ejecutó `dispatch-repair --ids C-05,C-11,H-02,H-05` (Paso 107), `dispatch.py` trató la cadena completa `"C-05,C-11,H-02,H-05"` como un único ID inexistente y lo asignó por defecto a `shard_01`.
3. **Colisión del puntero `repair_01.json` (`dispatch.py:1813-1836`):** Al despachar de uno en uno (`--ids C-05`, `--ids C-08`), `dispatch.py` guarda `repair_<cid>.json` pero construye el `pointer_prompt` apuntando siempre a `repair_01.json` (`item_file.name`).

---

### 9.2. Evaluación de Inicio del Pipeline (Stage 0) y CTA Architects (Stage 1B)

1. **Rendimiento y Limpieza de Ejecución (100% First-Try Pass):**
   - **Stage 0 (`bootstrap`):** `8.0 s` (`03:08:03` -> `03:08:11`), particionando 52 páginas (`3.44 MB`) en 2 subpartes MapReduce (`part_01`: 28 págs, Cap. 5; `part_02`: 24 págs, Apéndice D).
   - **`CTA Architect part_01` (`4c058247`):** `451.0 s` (`7.52 min`), 11 turnos, 1 escritura (`part_01_data.py`), **`1/1` en `compile_cta.py` (`PASS` al primer intento, 12 competencias: `C-01..05`, `H-01..03`, `Hab-01..04`)**. Fricción menor: leyó `cta_02.json` y ejecutó `compile_cta.py --help` (`~45 s` ahorrables).
   - **`CTA Architect part_02` (`018771c0`):** `330.0 s` (`5.50 min`), 9 turnos, 1 escritura (`part_02_data.py`), **`1/1` en `compile_cta.py` (`PASS` al primer intento, 13 competencias: renombradas en el merge a `C-06..12`, `H-04..07`, `Hab-05..06`)**.
2. **Hallazgo Estructural en el Merge de CTA (`dispatch.py:581` + `cta_merge.py`):**
   - `dispatch_cta` ordenó las subpartes por cantidad de páginas descendente (`28` págs del Cap. 5 en `part_01` antes que `24` págs del Apéndice D en `part_02`).
   - Al fusionarse determinísticamente (`part_01` índices `0..11`, `part_02` índices `12..24`), las competencias fundamentales del Apéndice D (`C-06` Límite en Probabilidad, `H-04` Markov/Chebychev, `H-05` Slutsky, `C-10` TCL, `Hab-05` Método Delta Univariado) quedaron ubicadas **después** de las competencias aplicadas de MCO/VI del Capítulo 5 (`C-01..05`, `H-01..03`, `Hab-01..04`), generando **prerrequisitos hacia adelante (`forward prerequisites`)** en 10 competencias de `part_01` y un solapamiento temático parcial entre `Hab-02` (Método Delta en MCO) y `Hab-05`/`Hab-06` (Método Delta Univariado/Multivariado).

---

### 9.3. Auditoría del Estándar de Calidad de 4 Arquetipos por Competencia (`[M3-ARCHETYPES]`) en los 16 Shards

- **Regla de Negocio:** Cada competencia debe contar con **4 arquetipos disjuntos** (`1. Directo`, `2. Inverso`, `3. Perturbación / Sensibilidad`, `4. Frontera / Caso Límite`), dando **$25 \text{ competencias} \times 4 = 100 \text{ plantillas}$** distribuidas en los 16 shards.
- **Cumplimiento Estructural:** **`25/25` competencias (`100%`)** tienen 4 tuplas compiladas en `TEMPLATES` (`100` plantillas en total).
- **Cumplimiento Matemático y Pedagógico Real (Clasificación en 4 Niveles):**

| Nivel de Calidad de Arquetipos | Competencias (`N/25`) | Shards | Diagnóstico Técnico |
| :--- | :---: | :--- | :--- |
| **Nivel 1 — 4 Arquetipos Matemáticos y Pedagógicos Genuinos** | **`6 / 25` (`24%`)** | `shard_04` (`Hab-04`), `shard_05` (`Hab-05`), `shard_07` (`C-04`, `C-05`), `shard_15` (`H-06`, `C-10`) | Tanto los enunciados (`stems`) como la función `_gen_*(rng, arch)` ramifican explícitamente en `arch = 1, 2, 3, 4`, resolviendo incógnitas distintas (Directo, Inverso despejando tamaño muestral/parámetro, Perturbación/Razón de varianzas, Caso Frontera) con soluciones y respuestas distintas. |
| **Nivel 2 — 4 Enunciados de Arquetipo + Variación de Régimen/Parámetros (`arch`)** | **`4 / 25` (`16%`)** | `shard_03` (`Hab-03`), `shard_06` (`Hab-06`), `shard_11` (`H-02`, `C-02`) | Presentan 4 familias de enunciados distintos y varían el régimen de muestreo de parámetros según `arch` (`distinct_vars = 4/4`), aunque evalúan la misma expresión objetivo. |
| **Nivel 3 — 4 Enunciados Distintos, pero `_gen_*(rng, arch=1)` Ignora `arch`** | **`11 / 25` (`44%`)** | `shard_01` (`Hab-01`), `shard_02` (`Hab-02`), `shard_08` (`C-07`, `C-08`), `shard_09` (`C-11`, `C-12`), `shard_10` (`C-01`, `H-01`), `shard_13` (`C-06`, `H-04`), `shard_16` (`H-07`) | Tienen 4 enunciados distintos (`stems_1..4` redactados como Directo, Inverso, Perturbación y Frontera), pero la función `_gen_*(rng, arch=1)` **no utiliza el argumento `arch`**, devolviendo exactamente el mismo diccionario `vars`, la misma respuesta `correct` y la misma solución para los 4 arquetipos dada una misma semilla. |
| **Nivel 4 — Lista `stems` Clonada en las 4 Tuplas + `arch` Ignorado** | **`4 / 25` (`16%`)** | `shard_12` (`H-03`, `C-03`), `shard_14` (`H-05`, `C-09`) | El autor definió una única lista `stems_<cid>` y pasó **esa misma variable** a las 4 tuplas de `TEMPLATES` (`distinct_stems = 1/4`), además de ignorar `arch` en `_gen_*`. Los 4 arquetipos son clones idénticos. |

- **Causa Raíz de los Niveles 3 y 4 (Prompt + Validador):**
  1. En `prompt_shard_author.md` (líneas 245–301), el **Ejemplo Canónico 1 (`H-01` Carnot)** muestra `def _gen_h01(rng, arch=1):` donde `arch` **nunca se usa**, y pasa la **misma lista `stems_h01`** y la **misma cadena `sol`** a las 4 tuplas de `TEMPLATES`. Los subagentes imitaron literalmente ese patrón.
  2. En `compile_shard.py:1655`, la compuerta `[M3-ARCHETYPES]` evalúa `distinct_tuples = {(t.get("stem_es", "").strip(), t.get("generator_code", "").strip()) for t in tpls}`. Como `compile_shard.py` envuelve cada tupla con un nombre de función distinto (`def gen_h03_1`, `def gen_h03_2`, etc.), `generator_code` siempre difiere en el nombre del wrapper y `len(distinct_tuples)` siempre da `4`, permitiendo pasar tanto listas `stems` clonadas como funciones `_gen_*` que ignoran `arch`.
