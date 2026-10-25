# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Asyntotic Estatistics V3 (`asyntotic_estatistics_v5`)

**Fecha de Auditoría:** `2026-10-25 00:52:33 UTC`  
**Conversación Orquestadora:** [`89cf485b-52bf-4cdd-b5cb-ede7a4c7ea5e`](conversation://89cf485b-52bf-4cdd-b5cb-ede7a4c7ea5e)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\asyntotic_estatistics_v5\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `2 archivos` (52 págs / 3.44 MB) | ECONOMETRIC ANALTYSIS FIFTH EDITION  -  William H_ Greene  -  5th ed_, Upper Saddle River, N_J, New Jersey, 2003  -  Prentice Hall PTR  -  isbn13 9780130661890  -  d139b0dca2a0c7d0984d735f6be1944e  -  Anna’s Archive-93.pdf, Econometric Analysis (Greene) (z-library.sk, 1lib.sk, z-lib.sk)-923-946.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`30 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`25 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`29 subagentes`** | Visión (0), CTA (2), Autores (25), Jueces (0) |
| **Reactivos Finales Validados** | **`0 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`3,850,872` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`1,159,313` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`38,627,091` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`5,846,270` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`44,473,361` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`0.0 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`0.0 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`1,482,445.4 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`140,467.0 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`855,256.9 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`0.0 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`0.0 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`3.91x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `89cf485b`):** `4 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `shard`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-10-24 23:56:59` | `0.01s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-10-24 23:56:59` | `0.09s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\asyntotic_estatistics_v5\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-10-25 00:10:06` | `0.48s` | `1,960,067` (`517,154` act) | 2 | `competencies=30` |
| **`02_shard`** | `2026-10-25 00:10:11` | `0.04s` | `0` (`0` act) | 0 | `shards=19` |

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
- **Tiempo de Pared Fase Mappers (Máximo):** **`732.0s`** (determinado por `Cognitive Task Analysis Architect part_02`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`0.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`732.0s`** (`12.2 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cognitive Task Analysis Architect part_01** | Mapper | 14 | 175,494 | 98,688 | 694,929 | 1 | **686.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 16 | 155,497 | 90,091 | 870,206 | 2 | **732.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `25 shards concurrentes`
- **Duración Mínima de Shard:** `77.0s` | **Mediana:** `297.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`507.0s`** (`8.4 min`) por `Shard Author shard_17`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+210.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`113,892.1 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_01** | `Hab-01` | 1 | 86,448 | 41,997 | 554,910 | 128,445 | **128,445.0** | 14 | 6 | **297.0s** |
| **Shard Author shard_02** | `Hab-02` | 1 | 122,867 | 16,013 | 801,745 | 138,880 | **138,880.0** | 23 | 4 | **165.0s** |
| **Shard Author shard_03** | `Hab-03` | 1 | 290,302 | 50,414 | 1,506,496 | 340,716 | **340,716.0** | 24 | 4 | **385.0s** |
| **Shard Author shard_04** | `Hab-04` | 1 | 121,239 | 24,993 | 761,850 | 146,232 | **146,232.0** | 19 | 5 | **214.0s** |
| **Shard Author shard_05** | `Hab-05` | 1 | 136,471 | 14,335 | 538,695 | 150,806 | **150,806.0** | 15 | 4 | **150.0s** |
| **Shard Author shard_06** | `Hab-06` | 1 | 171,610 | 60,452 | 1,507,786 | 232,062 | **232,062.0** | 24 | 5 | **455.0s** |
| **Shard Author shard_07** | `Hab-07` | 1 | 128,906 | 38,834 | 989,331 | 167,740 | **167,740.0** | 24 | 5 | **329.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 138,063 | 71,215 | 1,014,071 | 209,278 | **209,278.0** | 27 | 6 | **485.0s** |
| **Shard Author shard_09** | `C-06, C-07` | 2 | 116,656 | 20,020 | 1,179,954 | 136,676 | **68,338.0** | 28 | 4 | **228.0s** |
| **Shard Author shard_10** | `C-10, C-11` | 2 | 183,181 | 50,486 | 1,930,905 | 233,667 | **116,833.5** | 26 | 3 | **443.0s** |
| **Shard Author shard_11** | `C-01, H-01` | 2 | 111,516 | 34,053 | 994,995 | 145,569 | **72,784.5** | 23 | 4 | **272.0s** |
| **Shard Author shard_12** | `C-02, H-02` | 2 | 159,044 | 53,944 | 1,668,459 | 212,988 | **106,494.0** | 29 | 6 | **424.0s** |
| **Shard Author shard_13** | `H-03, C-03` | 2 | 144,598 | 53,866 | 1,361,532 | 198,464 | **99,232.0** | 24 | 4 | **439.0s** |
| **Shard Author shard_14** | `C-04, H-04` | 2 | 137,276 | 37,601 | 1,549,759 | 174,877 | **87,438.5** | 32 | 7 | **330.0s** |
| **Shard Author shard_15** | `H-05, C-05` | 2 | 126,800 | 34,962 | 834,084 | 161,762 | **80,881.0** | 15 | 3 | **245.0s** |
| **Shard Author shard_16** | `C-08, H-08` | 2 | 152,407 | 38,063 | 1,677,312 | 190,470 | **95,235.0** | 32 | 5 | **323.0s** |
| **Shard Author shard_17 🛑** | `C-09, H-09` | 2 | 163,797 | 58,810 | 1,792,592 | 222,607 | **111,303.5** | 33 | 4 | **507.0s** |
| **Shard Author shard_18** | `C-12, H-10` | 2 | 104,900 | 30,107 | 830,539 | 135,007 | **67,503.5** | 22 | 6 | **247.0s** |
| **Shard Author shard_19** | `H-06, H-07` | 2 | 122,134 | 37,645 | 1,071,998 | 159,779 | **79,889.5** | 26 | 3 | **321.0s** |
| **Shard Author shard_05** | `Hab-05` | 1 | 96,678 | 13,886 | 652,775 | 110,564 | **110,564.0** | 19 | 3 | **137.0s** |
| **Shard Author shard_04** | `Hab-04` | 1 | 68,408 | 8,307 | 465,475 | 76,715 | **76,715.0** | 17 | 2 | **96.0s** |
| **Shard Author shard_18** | `C-12, H-10` | 2 | 62,146 | 5,215 | 269,197 | 67,361 | **33,680.5** | 12 | 1 | **77.0s** |
| **Shard Author shard_01** | `Hab-01` | 1 | 61,322 | 33,519 | 297,961 | 94,841 | **94,841.0** | 13 | 2 | **226.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 210,990 | 53,446 | 449,390 | 264,436 | **264,436.0** | 15 | 5 | **354.0s** |
| **Shard Author shard_01** | `Hab-01` | 1 | 80,547 | 33,520 | 141,138 | 114,067 | **114,067.0** | 5 | 1 | **203.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ❌ NO PASARON AL PRIMER INTENTO (REQUIRIÓ INTERVENCIONES)  
> Los blind judges y la verificación psicométrica registraron discrepancias que requirieron correcciones. La validación previa operó con discrepancias detectadas, requiriendo rondas de auto-reparación o intervención técnica.

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `60 reactivos` (30 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `0 jueces` | Aislamiento epistémico en Stage 5 |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | 0 violaciones iniciales registradas |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Bucle de Auto-Reparación**: Se ejecutó RepairLoop sobre el lote de evaluación.
- 2. **Intervenciones de Supervisor (0 operaciones)**: Operaciones sobre archivos de reactivos.
- 3. **Certificación y Verificación Final**: Se concluyó la validación tras 1 iteraciones sobre el lote de 60 reactivos.

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared del Orquestador:** `52.32 min` (`3139.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `3.4 min` (`205.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `1.6 min` (`98.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `2.1 min` (`126.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_17
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_17 tardó 507.0s frente a la mediana de 297.0s (+210.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

### 🛑 [HIGH] Antipatrón de Micro-Bucle Interactivo (33 turnos en Shard Author shard_17)
- **Ámbito:** `Shard Author shard_17`
- **Diagnóstico:** 3 subagentes realizaron > 30 turnos individuales (ej. Shard Author shard_17 con 33 turnos). Ocurre por bucles de depuración o escritura incremental en lugar de redactar por lotes atómicos.

### ⚠️ [MEDIUM] Fricción de Herramientas en 21 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_01 acumularon fallos en consola (6 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `397 turnos`
- **Volumen Total de Razonamiento:** `772,318 caracteres`
- **Razonamiento del Orquestador:** `51 turnos` (38,061 chars)
- **Razonamiento de Subagentes:** `346 turnos` (734,257 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect part_01** | 8 | 42,135 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_02** | 11 | 55,220 | ⚠️ 2 |
| **Shard Author shard_01** | 9 | 30,821 | ⚠️ 6 |
| **Shard Author shard_02** | 10 | 8,207 | ⚠️ 4 |
| **Shard Author shard_03** | 14 | 36,167 | ⚠️ 4 |
| **Shard Author shard_04** | 10 | 17,154 | ⚠️ 5 |
| **Shard Author shard_05** | 8 | 7,162 | ⚠️ 4 |
| **Shard Author shard_06** | 12 | 42,474 | ⚠️ 5 |
| **Shard Author shard_07** | 14 | 38,987 | ⚠️ 5 |
| **Shard Author shard_08** | 14 | 36,996 | ⚠️ 6 |
| **Shard Author shard_09** | 14 | 12,154 | ⚠️ 4 |
| **Shard Author shard_10** | 13 | 30,539 | ⚠️ 3 |
| **Shard Author shard_11** | 15 | 26,143 | ⚠️ 4 |
| **Shard Author shard_12** | 15 | 34,363 | ⚠️ 6 |
| **Shard Author shard_13** | 13 | 36,199 | ⚠️ 4 |
| **Shard Author shard_14** | 17 | 20,674 | ⚠️ 7 |
| **Shard Author shard_15** | 10 | 24,149 | ⚠️ 3 |
| **Shard Author shard_16** | 21 | 25,550 | ⚠️ 5 |
| **Shard Author shard_17** | 21 | 38,450 | ⚠️ 4 |
| **Shard Author shard_18** | 11 | 19,537 | ⚠️ 6 |
| **Shard Author shard_19** | 14 | 26,549 | ⚠️ 3 |
| **Shard Author shard_05** | 15 | 6,995 | ⚠️ 3 |
| **Shard Author shard_04** | 11 | 4,743 | ⚠️ 2 |
| **Shard Author shard_18** | 7 | 2,409 | ⚠️ 1 |
| **Shard Author shard_01** | 7 | 21,955 | ⚠️ 2 |
| **Shard Author shard_08** | 11 | 34,290 | ⚠️ 5 |
| **Shard Author shard_01** | 5 | 19,746 | ⚠️ 1 |
| **Subagent** | 8 | 25,405 | 0 |
| **Subagent** | 8 | 9,084 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*


---

## 7. Investigación Forense Profunda: Varianza Multi-Shard (2–3m vs 9–14m) y Regresión de Latencia en CTA Architects (`edit_file` vs `write_file`)

### 7.1. Hallazgo 1: ¿Por qué existen Shards de 2–3 min frente a Shards de 9–14+ min?

Al descomponer los **19 shards (+ 8 re-despachos = 27 ejecuciones)** en **`Pre-1st-Compile`** ($t_{\text{1st\_compile}} - t_{\text{spawn}}$) vs **`Post-1st-Compile`** ($t_{\text{end}} - t_{\text{1st\_compile}}$) y cruzarlos contra `asyntotic_estatistics_v4` (`0b8b5084`), se demuestra que la varianza de $4\times\text{–}6\times$ proviene de **5 multiplicadores ortogonales** (donde el benchmark *Gold-Standard Clean-Room* es **`shard_09` (`228s = 3.80m` para 2 competencias en 78 líneas)** y **`shard_02` (`165s = 2.75m` para 1 habilidad `Hab-02`)**):

| Perfil de Shard | Ejemplos Empíricos (`v5` / `v4`) | Pre-1st-Compile | Post-1st-Compile | Total (Indiv. / Acum.) | Tokens Out (`write_file`) | Causa Raíz Primaria |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Clean-Room Fast (Benchmark)** | `shard_05` R1 (`Hab-05`), `shard_02` (`Hab-02`), `shard_09` (`C-06, C-07`) | `101s – 169s` | `36s – 59s` | **`2.50m – 3.80m`** | `5.9k – 16.0k` (`78–135` lín.) | 1 generador compacto parametrizado, `0` lecturas cross-course, `PASS` al 1er intento válido. |
| **Code Bloat / Monolito Verboso** | `shard_10` (`C-10, C-11`), `shard_03` (`Hab-03`), `shard_17` (`C-09, H-09`) | `333s – 419s` | `52s – 88s` | **`6.42m – 8.45m`** | `30.9k – 40.9k` (`382–470` lín.) | Escriben 4 a 8 funciones `gen_*` separadas con boilerplate duplicado: **un solo turno `write_file` tarda `179s – 236s` (`3.0–3.9 min`)** streameando tokens a ~168 tok/s. |
| **Exploración Prohibida Pre-Compile** | `shard_17` (`b91ca386`), `shard_16` (`ec88b1d6`), `shard_03` (`9417c823`) | `292s – 419s` | `31s – 88s` | **`5.38m – 8.45m`** | `38.0k – 58.8k` | `shard_17` gastó **`225s` (24 turnos)** ejecutando `git log -n 5` y leyendo `tests/test_validator.py` y `tests/test_shard06_and_dry_archetypes.py` (no bloqueados por `c2c_hook_guard.py`). El 75% ejecutó `Get-ChildItem -Recurse -Path courses/`. |
| **Re-despachos por Crash / Hang** | `shard_01` (`4` runs), `shard_08` (`2` runs), `shard_12` (`2` runs) | `93s – 383s` | `102s – 204s` | **`9.58m – 15.85m` acum.** | `71.5k – 146.3k` acum. | **(a)** Crash `protojson` CP1252 en Windows al emitir acentos (`ó`, `é`) en `c2c_hook_guard.py` tras `PASS` (`shard_01` 3 veces, `shard_08` 2 veces); **(b)** Bucle infinito `while len(set(...)) < 7` en `gen_c02_frontera` (`shard_12`). |
| **Bucles Post-Compile con Full Rewrite** | `v5 shard_06` (`7.58m`), `v5 shard_13` (`7.32m`); `v4 shard_07` (`9.27m`), `v4 shard_09` (`11.25m`), `v4 shard_06` (`17.70m`) | `177s – 320s` | `154s – 885s` | **`7.32m – 17.70m`** | `53.9k – 115.1k` (`2–7` `write_file`s) | Reescriben todo el archivo con `write_file(Overwrite=True)` ante errores `[R-20]`, `[R-19]` o `[TPL-DRY]`. Contraste directo: `shard_14` (32 turnos, **3 `edit_file` quirúrgicos de 8–27s**) terminó en **`5.50m`**, **109s más rápido** que `shard_13` (`7.32m`, 2 `write_file`s = `218s`). |

---

### 7.2. Hallazgo 2: Regresión de Latencia en CTA Architects (`5.3–6.8m` en `v3`/`v4` $\rightarrow$ `11.4–12.2m` en `v5`)

Comparativa longitudinal exacta sobre el **mismo corpus de 52 páginas** (`estadistica_asintotica`, 2 Mappers MapReduce):

| Métrica | `v3` `part_01` (`8e09ad50`) | `v4` `part_01` (`7dd7fd94`) | `v4` `part_02` (`feee4956`) | `v5` `part_01` (`adce53ba`) | `v5` `part_02` (`0e7b305a`) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Duración Total** | **`5.25m` (315s)** | **`6.87m` (412s)** | **`6.68m` (401s)** | **`11.43m` (686s)** | **`12.20m` (732s)** |
| **Pre-1st-Compile** | `299s` (4.98m) | `397s` (6.62m) | `365s` (6.08m) | `450s` (7.50m) | `425s` (7.08m) |
| **Post-1st-Compile** | **`16s`** (0.27m) | **`15s`** (0.25m) | **`36s`** (0.60m) | **`236s` (3.93m)** | **`307s` (5.12m)** |
| **Llamadas `write_file`** | `1` | `1` | `1` | **`2`** | **`2`** |
| **Tokens Out Totales** | `41,281` | `49,812` | `52,014` | **`98,688`** | **`90,091`** |
| **Tokens / Tiempo de `write_file #2`** | `0` | `0` | `0` | **`31,682 tok` (`177s`)** | **`32,250 tok` (`187s`)** |
| **Líneas Idénticas Re-generadas** | — | — | — | **`885 / 981` (`90.21%`)** | **`657 / 849` (`77.39%`)** |

#### Las 5 Trampas Encadenadas que Forzaron el Full Rewrite en `v5`:
1. **Compresión Excesiva en `system_prompts/lean/prompt_cta_architect.md` (Línea 14):** El prompt completo original (`system_prompts/prompt_cta_architect.md`, L342–345) prohibía `Append=True` en la *creación*, pero **exigía explícitamente `edit_file` (máx. 3 ediciones) en la *reparación***. Al comprimirlo a Lean v3.3, quedó como `🚫 Incremental micro-edits; write entire module in ONE atomic write_file(Overwrite=True)`, prohibiendo `edit_file` incluso para reparar.
2. **Instrucción Contradictoria en `compile_cta.py` (Línea 1604, modo `consolidated=True`) + Bloqueo en `c2c_hook_guard.py` (L82–89):** El compilador imprimió: `1. Resolve all errors above in ONE turn using parallel write_to_file calls to 'cta_fixes/<ID>.py' (or rewrite whole part in ONE write_to_file)`. Pero `c2c_hook_guard.py` **no incluye `cta_fixes/`** en `WORKER_AUTHORIZED_PYTHON_PATTERNS`, dejando el full `write_file(Overwrite=True)` como única vía legal.
3. **Desfase de Números de Línea JSON vs Python (`compile_cta.py` L1204 / L1355):** `check_cta.py` reportó los 5 distractores (`D-H03-03`, `D-C03-04`, `D-Hab01-05`, `D-Hab03-02`, `D-Hab04-05`) usando líneas del `cta.json` en memoria (`305, 929, 1437, 1632, 1806`) en vez de líneas de `part_01_data.py`, y el snippet impreso (`L158–L160`) mostró solo el paréntesis de apertura `(` de la tupla en lugar de la línea `manifestation` (`L163`).
4. **Condición de Carrera Concurrente en `work/cta_repair_pack.json` (`compile_cta.py` L1615):** Ambos Mappers escribieron al mismo archivo sin namespace (`work/cta_repair_pack.json`). `part_01` sobrescribió el archivo a las `00:05:17Z`, y `part_02` lo leyó a las `00:05:37Z` — razón exacta por la cual el segundo arquitecto citó los 5 IDs de `part_01` (`D-H03-03`, `D-C03-04`, `D-Hab01-05`, `D-Hab03-02`, `D-Hab04-05`) cuando fue interrogado.
5. **Brecha en el Auto-Healer L1/L2 (`cta_merge.py` `normalize_orphan_math`):** No envolvía automáticamente campos `manifestation` completos con macros LaTeX (`\lim`, `\to`, `\implies`, `\text`, `\varepsilon`) cuando carecían de `$ ... $`.

---

### 7.3. Análisis de Criterio según la Arquitectura de Agentes Google Antigravity: El "Sweet Spot" Exacto entre `edit_file` y `write_file`

#### Física de Latencia y Confiabilidad de Herramientas en Antigravity SDK:
- **Velocidad empírica de decodificación (`Model="flash"` en `v5`):** $v_{\text{out}} \approx \mathbf{168\text{ tokens/s}}$ ($\approx 5.95\text{ s}$ por cada $1{,}000$ output tokens).
- **Costo de `write_file(Overwrite=True)` en CTA (`850–980` líneas, `32k–50k` tokens):**
  $$T_{\text{write\_full}} = t_{\text{turn}} + \frac{N_{\text{tokens}}}{168} \approx 6\text{s} + \frac{32{,}000\text{–}50{,}000}{168} \approx \mathbf{196\text{s}\text{–}304\text{s}\ (3.3\text{–}5.1\text{ min})}$$
- **Costo y mecánica de `edit_file` (`BuiltinTools.EDIT_FILE`) en Antigravity:**
  1. Regla 1 del schema nativo: cada llamada opera sobre **un bloque contiguo**; múltiples regiones no adyacentes se emiten como **llamadas `edit_file` paralelas en el mismo turno**.
  2. Regla 2: exige coincidencia **100% exacta de caracteres y espacios iniciales (`Target`)** — muy sensible en tuplas Python anidadas a 12–16 espacios con raw strings `r"..."`.
  3. Regla 3: si `Target` aparece más de una vez (ej. `None` o `r"$0$"`), reemplaza **todas** las ocurrencias accidentalmente si no se incluye contexto único (ID o nombre del distractor).
  4. Costo temporal de $K$ llamadas `edit_file` paralelas en 1 turno ($\sim 250$ tokens por hunk):
     $$T_{\text{edit}}(K) \approx 8\text{s} + \frac{250 \cdot K + N_{\text{think}}}{168}$$
     - Para **$K = 1..3$ hunks** (criterio propuesto por el usuario): **`12s – 18s`** ($\sim 1{,}000$ tokens) $\rightarrow$ **$11\times\text{–}16\times$ más rápido** que `write_file`, con probabilidad de éxito al primer turno $> 85\%$.
     - Para **$K = 4..6$ hunks** (con snippets exactos provistos por `compile_cta.py`): **`20s – 28s`** ($\sim 2{,}000$ tokens). Incluso si 1 hunk falla por indentación y requiere 1 turno extra (`+15s`), el total (`~40s`) sigue siendo **$4.5\times$ más rápido** que `write_file` (`185s`).
     - Para **$K > 6$ hunks dispersos**: la probabilidad acumulada de fallo de `Target` ($1 - (1 - p_{\text{miss}})^K$) supera el $45\text{–}70\%$, disparando cascadas de `view_file` + reintentos e invalidación de caché.

#### Arquitectura Óptima de 4 Niveles (Sweet-Spot Escalation Protocol para CTA Architects):
1. **Nivel 0 — Auto-Healing Determinista en `compile_cta.py` (`0` turnos LLM, `< 5 ms`):** Envolver automáticamente en `$ ... $` cualquier campo `manifestation` / `wrong_belief` / `correct_belief` que contenga comandos/operadores LaTeX sin delimitadores `$`. Resuelve el 100% del caso `v5` sin re-invocar al LLM.
2. **Nivel 1 — `edit_file` Quirúrgico Paralelo (Sweet Spot: `1 ≤ K ≤ 6` hunks localizados y `≤ 25` líneas modificadas):**
   - Tu criterio de `≤ 3` errores es el núcleo óptimo de máxima seguridad; extender el umbral hasta **`≤ 6` hunks localizados** (emitidos en paralelo en 1 solo turno usando el snippet Python exacto `L-2..L+2` impreso por `compile_cta.py`) captura el punto *Pareto-óptimo* (`12s–28s` vs `185s`).
3. **Nivel 2 — Override Modular por Competencia `cta_fixes/<CID>.py` (`> 6` hunks concentrados en `1–3` competencias, ej. `CTA-D1`):**
   - `compile_cta.py` (L1062–1097) **ya soporta splicing L4 desde `cta_fixes/<ID>.py`** (`~55` líneas = `~2,200` tokens = **`13s` por competencia**). Solo requiere autorizar `cta_fixes/` en `c2c_hook_guard.py` y en `lean/prompt_cta_architect.md`.
4. **Nivel 3 — Full Atomic `write_file(Overwrite=True)` (Último Recurso: errores sistémicos en `> 3` competencias y `> 6` hunks, o `SyntaxError` estructural masivo):**
   - Único escenario donde pagar el costo fijo de `180s–300s` es más eficiente y seguro que decenas de `edit_file`.

---

### 7.4. Matriz de Estado Dual (`Ya Parcheado en Phase A` vs `Pendiente de Parchear`)

#### ✅ Capa Ya Parcheada en Working Tree (`Phase A` de `89cf485b`):
- **`c2c_hook_guard.py`:** Salida JSON 7-bit ASCII (`ensure_ascii=True`) + UTF-8 stdin/stdout $\rightarrow$ erradica el crash `protojson` CP1252 que mató 7 subagentes en `v5`.
- **`dispatch.py`:** Corrección de `manifest_rel` a `pre_shard_manifest.json` en `dispatch_authors` y `build_dispatch` $\rightarrow$ elimina el fallo del 100% en el primer `compile_shard.py`.
- **`engine/sandbox.py` & `compile_shard.py`:** Guardián `call_with_timeout(..., max_user_steps=250_000)` $\rightarrow$ erradica cuelgues infinitos como `shard_12`.

#### 🛠️ Capa Pendiente de Parchear (Acciones de Alto Impacto Recomendadas):
1. **CTA Sweet-Spot & Prompt Alignment (`system_prompts/lean/prompt_cta_architect.md` + `compile_cta.py` + `c2c_hook_guard.py`):**
   - Reemplazar la prohibición absoluta de `edit_file` en `lean/prompt_cta_architect.md` por la regla híbrida: *Creación inicial en 1 `write_file(Overwrite=True)`; reparaciones con `edit_file` (`≤ 6` hunks), `cta_fixes/<CID>.py` (`1–3` competencias), o `write_file` solo si `> 6` hunks en `> 3` competencias*.
   - Autorizar `(?:^|/)(?:cta_parts/)?cta_fixes/[^/\\<>:"|?*]+\.py$` en `c2c_hook_guard.py` (`WORKER_AUTHORIZED_PYTHON_PATTERNS`).
   - Actualizar `compile_cta.py` L1604 para recomendar `edit_file` quirúrgico cuando `len(errors) <= 6`, mapear todos los IDs a líneas reales de `.py` (incluyendo la línea exacta del campo `manifestation`), y separar el repair pack por subpart (`cta_parts/<part_id>_repair_pack.json`).
   - Ampliar `normalize_orphan_math` / `compile_cta.py` para auto-envolver fórmulas LaTeX desnudas en `manifestation` con `$ ... $`.
2. **Reducción de Varianza en Shards (`system_prompts/lean/prompt_shard_author.md` + `c2c_hook_guard.py`):**
   - Bloquear lecturas a `tests/` y `git log` en `c2c_hook_guard.py` (`WORKER_DENIED_READ_SUBSTRINGS` + comando `git`), y bloquear `Get-ChildItem ... -Recurse` sobre `courses/` sin importar el orden de flags.
   - Estandarizar en `lean/prompt_shard_author.md` el **Patrón Clean-Room `shard_09`** (`1` sola función `gen_<cid>(rng)` con `rng.choice` para los 4 arquetipos, tope `≤ 110` líneas para 1 competencia y `≤ 170` líneas para 2 competencias), evitando monolitos de 380–470 líneas (`180–236s` de streaming).
   - Reducir el umbral anti-reescritura monolítica en `c2c_hook_guard.py` (Rule C, L633) de `250` a `140` líneas para forzar `edit_file` o `shard_fixes/<CID>.py`.
