# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Mateco 4 Optimizacion K3 V2 M20 (`mateco_4_optimizacion_k3_v2_m20`)

**Fecha de Auditoría:** `2026-11-24 18:19:10 UTC`  
**Conversación Orquestadora:** [`36fdd76d-140a-4397-93a4-7472dd8bdf8f`](conversation://36fdd76d-140a-4397-93a4-7472dd8bdf8f)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_k3_v2_m20\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias, Costos USD (Gemini 4 Hydrogen) y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `6 archivos` (71 págs / 3.61 MB) | 01_optimizacion_dinamica.pdf, 02_Set_Problem_Calculo_de_variaciones.pdf, 03_Teoria_de_control_optimo___teoria (1).pdf, 04_opt_din_3.pdf, 05_Control Optimo Apuntes.pdf, 06_Problemas_teoria_de_control.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`27 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`27 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`53 subagentes`** | Visión (0), CTA (8), Autores (27), Repairs (4), Jueces (14) |
| **Reactivos Finales Validados** | **`903 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`2,765,148` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`943,678` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`7,167,735` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`3,819,855` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`10,987,590` tokens** | Consumo total de cuota facturable |
| **Costo Estimado Total (Gemini 4 Hydrogen)** | **`$11.97 USD`** | In: `$4.31` (`$1.50/1M`), Out+Think: `$7.12` (`$7.50/1M`), Cache: `$0.54` (`$0.08/1M`) |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`12,167.9 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`4,230.2 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`406,947.8 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`89,408.7 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`154,754.8 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Costo Estimado por Pregunta (Hydrogen)** | **`$0.01 USD/preg`** | Costo monetario valorizado por reactivo |
| **Costo Estimado por Competencia (Hydrogen)** | **`$0.44 USD/comp`** | Costo monetario valorizado por competencia |
| **Segundos de Pared por Pregunta** | **`1.32 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`45.38 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`5.22x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0a. Valorización Monetaria por Etapa (Tarifas Gemini 4 Hydrogen)
> Tarifas oficiales aplicables: Entrada `$1.50/1M`, Caché leído `$0.08/1M`, Salida (incl. thinking) `$7.50/1M`.

| Etapa / Rol | Agentes | Tokens Entrada | Tokens Salida | Caché Leído | Costo Estimado (USD) | % del Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 1A: Visión** | 0 | 0 | 0 | 0 | **`$0.00`** | 0.0% |
| **Stage 1B: CTA Architects** | 8 | 326,097 | 84,421 | 910,678 | **`$1.19`** | 9.9% |
| **Stage 3: Shard Authors** | 27 | 1,759,645 | 654,389 | 4,614,764 | **`$7.89`** | 65.9% |
| **Stage 3B: Repair Engineers** | 4 | 204,792 | 36,519 | 662,148 | **`$0.63`** | 5.3% |
| **Stage 5: Blind Judges** | 14 | 474,614 | 168,349 | 470,514 | **`$2.01`** | 16.8% |
| **Orquestador Principal (Director)** | 1 | 105,001 | 6,028 | 509,631 | **`$0.24`** | 2.0% |
| **TOTAL CORRIDA (Gemini 4 Hydrogen)** | **54** | **2,870,149** | **949,706** | **7,167,735** | **`$11.97 USD`** | **100.0%** |

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `36fdd76d`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-11-24 17:59:26` | `0.1s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-11-24 17:59:27` | `0.17s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_k3_v2_m20\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-11-24 18:03:10` | `1.93s` | `0` (`0` act) | 0 | `competencies=27` |
| **`02_shard`** | `2026-11-24 18:03:11` | `0.05s` | `0` (`0` act) | 0 | `shards=27` |
| **`03_templates`** | `2026-11-24 18:18:56` | `0.5s` | `0` (`0` act) | 0 | `count=27` |
| **`04_build`** | `2026-11-24 18:19:04` | `8.1s` | `0` (`0` act) | 0 | `total_questions=903` |
| **`05_verify`** | `2026-11-24 18:19:06` | `1.92s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_k3_v2_m20\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-11-24 18:13:07` | `0.2s` | `0` (`0` act) | 0 | `passed=False` |
| **`06_publish`** | `2026-11-24 18:19:10` | `3.6s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_k3_v2_m20.json` |

---

### 3.1. Stage 1A: Preprocesamiento de Visión
- **Subagentes de Visión Desplegados:** `0 agentes en paralelo`
- **Tiempo de Pared de la Etapa (Máximo / Critical Path):** **`0.0s`** (`0.0 min`)
- **Costo Estimado Etapa 1A (Gemini 4 Hydrogen):** **`$0.00 USD`**
- **Agente Determinante del Camino Crítico:** `N/A`

| Subagente de Visión | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- |

---

### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)
- **Arquitectura:** `MAPREDUCE (7 Mappers + 1 Harmonizer)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`114.0s`** (determinado por `Cognitive Task Analysis Architect part_05`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`96.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`210.0s`** (`3.5 min`)
- **Costo Estimado Etapa 1B (Gemini 4 Hydrogen):** **`$1.19 USD`**

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Costo (USD) | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **Cognitive Task Analysis Architect part_01** | Mapper | 4 | 38,182 | 10,486 | 70,930 | `$0.14` | 0 | **76.0s** |
| **Cognitive Task Analysis Architect part_05** | Mapper | 6 | 46,014 | 13,090 | 148,230 | `$0.18` | 1 | **114.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 4 | 40,032 | 12,339 | 72,711 | `$0.16` | 0 | **67.0s** |
| **Cognitive Task Analysis Architect part_04** | Mapper | 4 | 29,575 | 7,546 | 56,659 | `$0.11` | 0 | **50.0s** |
| **Cognitive Task Analysis Architect part_06** | Mapper | 4 | 31,736 | 9,015 | 59,803 | `$0.12` | 0 | **52.0s** |
| **Cognitive Task Analysis Architect part_03** | Mapper | 4 | 28,454 | 8,805 | 53,151 | `$0.11` | 0 | **47.0s** |
| **Cognitive Task Analysis Architect part_07** | Mapper | 4 | 24,376 | 8,326 | 45,597 | `$0.10` | 0 | **45.0s** |
| **CTA Harmonizer** | Harmonizer | 8 | 87,728 | 14,814 | 403,597 | `$0.27` | 1 | **96.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `27 shards concurrentes`
- **Tasa de Aprobación en 1ra Compilación:** **`12/27 (44.44%)`** (Reglas en 1er fallo: `[INVARIANT]` (4), `[TPL-STEM-EQUATION-PARITY]` (3), `[TPL-DYNAMIC-RATIONALE]` (3), `[TPL-STEM-VARIANT-PARITY]` (3), `[R-15-MS]` (2), `[TPL-DEGENERATE-LITERAL-COND]` (2))
- **Duración Mínima de Shard:** `87.0s` | **Mediana:** `130.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`196.0s`** (`3.3 min`) por `Shard Author shard_11`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+66.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`89,408.7 tokens/competencia`**
- **Costo Estimado Etapa 3 (Gemini 4 Hydrogen):** **`$7.89 USD`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **Shard Author shard_01** | `Hab-08` | 1 | 66,862 | 31,603 | 234,549 | 98,465 | `$0.35` | **98,465.0** | 6 | 1 | **169.0s** |
| **Shard Author shard_13** | `C-08` | 1 | 59,619 | 21,825 | 206,675 | 81,444 | `$0.27` | **81,444.0** | 6 | 1 | **130.0s** |
| **Shard Author shard_25** | `C-14` | 1 | 52,153 | 16,863 | 180,345 | 69,016 | `$0.22` | **69,016.0** | 6 | 1 | **98.0s** |
| **Shard Author shard_02** | `Hab-16` | 1 | 63,282 | 26,306 | 218,981 | 89,588 | `$0.31` | **89,588.0** | 6 | 1 | **143.0s** |
| **Shard Author shard_15** | `C-11` | 1 | 50,743 | 18,645 | 99,423 | 69,388 | `$0.22` | **69,388.0** | 4 | 0 | **95.0s** |
| **Shard Author shard_26** | `C-23` | 1 | 114,847 | 25,011 | 251,017 | 139,858 | `$0.38` | **139,858.0** | 8 | 2 | **152.0s** |
| **Shard Author shard_03** | `Hab-07` | 1 | 69,029 | 33,801 | 240,968 | 102,830 | `$0.38` | **102,830.0** | 6 | 1 | **181.0s** |
| **Shard Author shard_27** | `H-01` | 1 | 56,906 | 22,744 | 197,431 | 79,650 | `$0.27` | **79,650.0** | 6 | 1 | **120.0s** |
| **Shard Author shard_14** | `C-01` | 1 | 52,002 | 20,331 | 99,446 | 72,333 | `$0.24` | **72,333.0** | 4 | 0 | **95.0s** |
| **Shard Author shard_04** | `Hab-09` | 1 | 60,338 | 27,569 | 110,408 | 87,907 | `$0.31` | **87,907.0** | 4 | 0 | **132.0s** |
| **Shard Author shard_16** | `C-06` | 1 | 49,418 | 17,064 | 97,821 | 66,482 | `$0.21` | **66,482.0** | 4 | 0 | **96.0s** |
| **Shard Author shard_17** | `PRE-01` | 1 | 58,164 | 23,716 | 203,138 | 81,880 | `$0.28` | **81,880.0** | 6 | 1 | **135.0s** |
| **Shard Author shard_05** | `Hab-01` | 1 | 57,592 | 25,181 | 106,877 | 82,773 | `$0.28` | **82,773.0** | 4 | 0 | **118.0s** |
| **Shard Author shard_06** | `Hab-13` | 1 | 94,982 | 28,233 | 196,321 | 123,215 | `$0.37` | **123,215.0** | 6 | 1 | **157.0s** |
| **Shard Author shard_18** | `C-07` | 1 | 101,112 | 38,955 | 200,970 | 140,067 | `$0.46` | **140,067.0** | 6 | 1 | **187.0s** |
| **Shard Author shard_07** | `Hab-02` | 1 | 51,248 | 19,709 | 99,649 | 70,957 | `$0.23` | **70,957.0** | 4 | 0 | **106.0s** |
| **Shard Author shard_19** | `C-18` | 1 | 53,693 | 22,348 | 101,896 | 76,041 | `$0.26` | **76,041.0** | 4 | 0 | **109.0s** |
| **Shard Author shard_20** | `C-02` | 1 | 76,182 | 21,277 | 75,843 | 97,459 | `$0.28` | **97,459.0** | 4 | 0 | **111.0s** |
| **Shard Author shard_08** | `Hab-05` | 1 | 67,643 | 26,808 | 333,560 | 94,451 | `$0.33` | **94,451.0** | 8 | 1 | **154.0s** |
| **Shard Author shard_09** | `Hab-06` | 1 | 56,052 | 24,642 | 104,568 | 80,694 | `$0.28` | **80,694.0** | 4 | 0 | **118.0s** |
| **Shard Author shard_21** | `C-03` | 1 | 47,843 | 16,779 | 95,905 | 64,622 | `$0.20` | **64,622.0** | 4 | 0 | **87.0s** |
| **Shard Author shard_22** | `C-04` | 1 | 59,478 | 24,180 | 201,581 | 83,658 | `$0.29` | **83,658.0** | 6 | 1 | **131.0s** |
| **Shard Author shard_10** | `Hab-04` | 1 | 54,737 | 23,622 | 103,283 | 78,359 | `$0.27` | **78,359.0** | 4 | 0 | **119.0s** |
| **Shard Author shard_23** | `C-05` | 1 | 107,057 | 23,397 | 148,850 | 130,454 | `$0.35` | **130,454.0** | 6 | 1 | **137.0s** |
| **Shard Author shard_11 🛑** | `Hab-11` | 1 | 72,132 | 32,370 | 403,321 | 104,502 | `$0.38` | **104,502.0** | 9 | 3 | **196.0s** |
| **Shard Author shard_12** | `Hab-12` | 1 | 59,435 | 24,924 | 207,156 | 84,359 | `$0.29` | **84,359.0** | 6 | 1 | **148.0s** |
| **Shard Author shard_24** | `C-12` | 1 | 47,096 | 16,486 | 94,782 | 63,582 | `$0.20` | **63,582.0** | 4 | 0 | **91.0s** |

---

### 3.3b. Stage 3B: Remediación y Repair Engineers (Ingenieros de Reparación)
- **Total de Repair Engineers Desplegados:** `4 subagentes` en **`3 ronda(s)`** (`DONE`: `4`, `BLOCKED`: **`0`**)
- **Duración Mínima:** `53.0s` | **Mediana:** `72.0s` | **Máxima:** `97.0s` (`1.6 min`)
- **Tokens Activos Totales en Reparación:** `241,311 tokens`
- **Costo Estimado Etapa 3B (Gemini 4 Hydrogen):** **`$0.63 USD`**
- **Agente Determinante del Retraso:** `Repair Engineer Hab-12`

| Repair Engineer | Estado | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Errores | Duración |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Repair Engineer Hab-11** | `DONE` | 5 | 47,361 | 7,384 | 117,678 | 54,745 | `$0.14` | 0 | **54.0s** |
| **Repair Engineer Hab-07** | `DONE` | 5 | 48,837 | 6,355 | 119,924 | 55,192 | `$0.13` | 0 | **53.0s** |
| **Repair Engineer Hab-07** | `DONE` | 7 | 51,859 | 7,585 | 206,705 | 59,444 | `$0.15` | 1 | **72.0s** |
| **Repair Engineer Hab-12** | `DONE` | 7 | 56,735 | 15,195 | 217,841 | 71,930 | `$0.22` | 1 | **97.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ⚠️ NO PASÓ AL PRIMER INTENTO — APROBADO POST-REJUDGE (143/143 REACTIVOS)  
> La Ronda 1 de Blind Judges registró 3 discrepancia(s), por lo que no hubo acuerdo limpio al primer intento. Tras correcciones y Rejudge, el resultado final alcanzó 100.0% de acuerdo (0 discrepancias).

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `143 reactivos` (27 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `14 jueces` | Aislamiento epistémico en Stage 5 |
| **Costo Etapa 5 (Gemini 4 Hydrogen)** | **`$2.01 USD`** | Evaluado sobre los 14 Blind Judges (In: `474,614`, Out: `168,349`, Cache: `470,514`) |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | Ronda 1: 3 discrepancia(s) (`flaw_detected`: 4, `kernel_override`: 0); 0 violaciones iniciales |
| **Resultado Final Post-Rejudge** | **`✅ Aprobado`** | `100.0%` acuerdo, `0` discrepancia(s) |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Ronda 1 (`judge_report_round_1.json` / `rounds_history`)**: 3 discrepancia(s) detectada(s).
- 2. **Bucle de Auto-Reparación / Rejudge**: 3 ola(s) de jueces ejecutada(s) (0 intervenciones de supervisor).
- 3. **Resultado Final Post-Rejudge (`judge_report.json`)**: ✅ Aprobado (`100.0% agreement rate`, `0 discrepancias` sobre 143 reactivos).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo y Costo del Orquestador
- 💵 **Costo Estimado del Orquestador Principal (Gemini 4 Hydrogen):** **`$0.24 USD`** (In: `105,001`, Out: `6,028`, Cache: `509,631`)
- ⏱️ **Tiempo Total de Pared del Orquestador:** `19.9 min` (`1194.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `0.38 min` (`23.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `18.8 min` (`1128.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `0.65 min` (`39.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### ⚠️ [MEDIUM] Fricción de Herramientas en 1 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_11 acumularon fallos en consola (3 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `108 turnos`
- **Volumen Total de Razonamiento:** `529,641 caracteres`
- **Razonamiento del Orquestador:** `6 turnos` (2,787 chars)
- **Razonamiento de Subagentes:** `102 turnos` (526,854 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Repair Engineer Hab-11** | 5 | 5,948 | 0 |
| **Repair Engineer Hab-07** | 1 | 3,917 | 0 |
| **Blind Judge 01** | 1 | 4,665 | 0 |
| **Blind Judge 02** | 1 | 5,453 | 0 |
| **Cognitive Task Analysis Architect part_01** | 2 | 3,820 | 0 |
| **Cognitive Task Analysis Architect part_05** | 2 | 6,022 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_02** | 3 | 6,587 | 0 |
| **Cognitive Task Analysis Architect part_04** | 2 | 2,965 | 0 |
| **Cognitive Task Analysis Architect part_06** | 2 | 4,417 | 0 |
| **Cognitive Task Analysis Architect part_03** | 2 | 5,008 | 0 |
| **Cognitive Task Analysis Architect part_07** | 3 | 4,315 | 0 |
| **CTA Harmonizer** | 2 | 9,762 | ⚠️ 1 |
| **Shard Author shard_01** | 3 | 19,086 | ⚠️ 1 |
| **Shard Author shard_13** | 2 | 8,321 | ⚠️ 1 |
| **Shard Author shard_25** | 2 | 8,093 | ⚠️ 1 |
| **Shard Author shard_02** | 2 | 13,896 | ⚠️ 1 |
| **Shard Author shard_15** | 1 | 5,089 | 0 |
| **Shard Author shard_26** | 4 | 14,753 | ⚠️ 2 |
| **Shard Author shard_03** | 3 | 18,385 | ⚠️ 1 |
| **Shard Author shard_27** | 2 | 11,707 | ⚠️ 1 |
| **Shard Author shard_14** | 1 | 9,268 | 0 |
| **Shard Author shard_04** | 1 | 13,252 | 0 |
| **Shard Author shard_16** | 1 | 6,748 | 0 |
| **Shard Author shard_17** | 3 | 16,305 | ⚠️ 1 |
| **Shard Author shard_05** | 3 | 14,112 | 0 |
| **Shard Author shard_06** | 2 | 14,506 | ⚠️ 1 |
| **Shard Author shard_18** | 2 | 17,218 | ⚠️ 1 |
| **Shard Author shard_07** | 1 | 8,343 | 0 |
| **Shard Author shard_19** | 1 | 11,959 | 0 |
| **Shard Author shard_20** | 1 | 11,270 | 0 |
| **Shard Author shard_08** | 3 | 11,013 | ⚠️ 1 |
| **Shard Author shard_09** | 1 | 14,022 | 0 |
| **Shard Author shard_21** | 1 | 6,527 | 0 |
| **Shard Author shard_22** | 2 | 12,306 | ⚠️ 1 |
| **Shard Author shard_10** | 2 | 12,383 | 0 |
| **Shard Author shard_23** | 2 | 10,967 | ⚠️ 1 |
| **Shard Author shard_11** | 5 | 19,475 | ⚠️ 3 |
| **Shard Author shard_12** | 2 | 9,855 | ⚠️ 1 |
| **Shard Author shard_24** | 1 | 8,077 | 0 |
| **Blind Judge 01** | 1 | 11,160 | 0 |
| **Blind Judge 02** | 1 | 9,643 | 0 |
| **Blind Judge 03** | 1 | 11,545 | 0 |
| **Blind Judge 04** | 2 | 9,264 | 0 |
| **Blind Judge 05** | 1 | 9,794 | 0 |
| **Blind Judge 06** | 1 | 9,197 | 0 |
| **Blind Judge 07** | 1 | 11,827 | 0 |
| **Blind Judge 08** | 1 | 9,001 | 0 |
| **Blind Judge 09** | 1 | 9,389 | 0 |
| **Repair Engineer Hab-07** | 3 | 5,117 | ⚠️ 1 |
| **Repair Engineer Hab-12** | 4 | 6,246 | ⚠️ 1 |
| **Blind Judge 01** | 2 | 10,163 | 0 |
| **Blind Judge 03** | 1 | 7,284 | 0 |
| **Blind Judge 02** | 2 | 17,409 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*