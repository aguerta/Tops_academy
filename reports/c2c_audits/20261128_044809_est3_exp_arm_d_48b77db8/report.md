# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Estadistica 3 Test K4 (`est3_exp_arm_d`)

**Fecha de Auditoría:** `2026-11-28 09:48:09 UTC`  
**Conversación Orquestadora:** [`48b77db8-b730-4b12-bb92-7239637c959e`](conversation://48b77db8-b730-4b12-bb92-7239637c959e)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\est3_exp_arm_d\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias, Costos USD (Gemini 4 Hydrogen) y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `3 archivos` (43 págs / 1.56 MB) | 01_measure_theory_bridge.pdf, 02_stat110_lec27_conditional_expectation.pdf, 03_rincon_cl_caps1_2.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`23 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`31 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`59 subagentes`** | Visión (0), CTA (0), Autores (31), Repairs (6), Jueces (22) |
| **Reactivos Finales Validados** | **`0 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`3,058,992` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`1,159,894` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`11,240,676` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`4,482,861` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`15,723,537` tokens** | Consumo total de cuota facturable |
| **Costo Estimado Total (Gemini 4 Hydrogen)** | **`$14.64 USD`** | In: `$4.96` (`$1.50/1M`), Out+Think: `$8.84` (`$7.50/1M`), Cache: `$0.84` (`$0.08/1M`) |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`0.0 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`0.0 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`683,632.0 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`128,834.3 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`365,663.7 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Costo Estimado por Pregunta (Hydrogen)** | **`$0.00 USD/preg`** | Costo monetario valorizado por reactivo |
| **Costo Estimado por Competencia (Hydrogen)** | **`$0.64 USD/comp`** | Costo monetario valorizado por competencia |
| **Segundos de Pared por Pregunta** | **`0.0 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`0.0 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`2.69x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0a. Valorización Monetaria por Etapa (Tarifas Gemini 4 Hydrogen)
> Tarifas oficiales aplicables: Entrada `$1.50/1M`, Caché leído `$0.08/1M`, Salida (incl. thinking) `$7.50/1M`.

| Etapa / Rol | Agentes | Tokens Entrada | Tokens Salida | Caché Leído | Costo Estimado (USD) | % del Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 1A: Visión** | 0 | 0 | 0 | 0 | **`$0.00`** | 0.0% |
| **Stage 1B: CTA Architects** | 0 | 0 | 0 | 0 | **`$0.00`** | 0.0% |
| **Stage 3: Shard Authors** | 31 | 2,077,135 | 886,055 | 8,479,108 | **`$10.40`** | 71.0% |
| **Stage 3B: Repair Engineers** | 6 | 260,345 | 36,236 | 650,549 | **`$0.71`** | 4.8% |
| **Stage 5: Blind Judges** | 22 | 721,512 | 237,603 | 725,040 | **`$2.92`** | 19.9% |
| **Orquestador Principal (Director)** | 1 | 245,079 | 18,896 | 1,385,979 | **`$0.61`** | 4.2% |
| **TOTAL CORRIDA (Gemini 4 Hydrogen)** | **60** | **3,304,071** | **1,178,790** | **11,240,676** | **`$14.64 USD`** | **100.0%** |

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `48b77db8`):** `4 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`03_templates`** | `2026-11-28 09:47:38` | `0.58s` | `0` (`0` act) | 0 | `count=23` |
| **`04_build`** | `2026-11-28 09:47:52` | `14.03s` | `0` (`0` act) | 0 | `total_questions=831` |
| **`05_verify`** | `2026-11-28 09:47:54` | `2.19s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\est3_exp_arm_d\work\course_verified.json` |
| **`06_publish`** | `2026-11-28 09:48:08` | `4.8s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\est3_exp_arm_d.json` |

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
- **Arquitectura:** `DIRECT (0 Direct CTA Architect)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`0.0s`** (determinado por `N/A`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`0.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`0.0s`** (`0.0 min`)
- **Costo Estimado Etapa 1B (Gemini 4 Hydrogen):** **`$0.00 USD`**

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Costo (USD) | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `31 shards concurrentes`
- **Tasa de Aprobación en 1ra Compilación:** **`6/26 (23.08%)`** (Reglas en 1er fallo: `[INVARIANT]` (5), `[TPL-DYNAMIC-RATIONALE]` (4), `[TPL-STATIC-OPT]` (4), `[TPL-STEM-EQUATION-PARITY]` (4), `[TPL-D4]` (4), `[TPL-DEGENERATE-LITERAL-COND]` (3))
- **Duración Mínima de Shard:** `0.0s` | **Mediana:** `150.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`306.0s`** (`5.1 min`) por `Shard Author shard_16`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+156.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`70,552.1 tokens/competencia`**
- **Costo Estimado Etapa 3 (Gemini 4 Hydrogen):** **`$10.40 USD`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **Shard Author shard_13** | `C-01, C-02` | 2 | 67,937 | 30,997 | 177,915 | 98,934 | `$0.35` | **49,467.0** | 5 | 0 | **149.0s** |
| **Shard Author shard_10** | `Hab-10` | 1 | 125,211 | 27,469 | 219,745 | 152,680 | `$0.41` | **152,680.0** | 7 | 1 | **162.0s** |
| **Shard Author shard_17** | `C-13` | 1 | 66,213 | 33,403 | 211,789 | 99,616 | `$0.37` | **99,616.0** | 6 | 1 | **161.0s** |
| **Shard Author shard_14** | `C-07, C-08` | 2 | 73,814 | 24,977 | 411,729 | 98,791 | `$0.33` | **49,395.5** | 9 | 2 | **154.0s** |
| **Shard Author shard_16** | `C-11, C-12` | 2 | 91,873 | 30,900 | 805,404 | 122,773 | `$0.43` | **61,386.5** | 14 | 2 | **205.0s** |
| **Shard Author shard_01** | `Hab-01` | 1 | 60,130 | 27,130 | 109,667 | 87,260 | `$0.30` | **87,260.0** | 4 | 0 | **136.0s** |
| **Shard Author shard_02** | `Hab-02` | 1 | 65,060 | 27,297 | 281,212 | 92,357 | `$0.32` | **92,357.0** | 7 | 1 | **154.0s** |
| **Shard Author shard_03** | `Hab-03` | 1 | 66,405 | 26,975 | 275,443 | 93,380 | `$0.32` | **93,380.0** | 7 | 1 | **138.0s** |
| **Shard Author shard_07** | `Hab-07` | 1 | 83,144 | 28,553 | 598,221 | 111,697 | `$0.38` | **111,697.0** | 12 | 2 | **176.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 75,864 | 27,123 | 462,684 | 102,987 | `$0.35` | **102,987.0** | 10 | 1 | **176.0s** |
| **Shard Author shard_09** | `Hab-09` | 1 | 68,282 | 30,573 | 226,248 | 98,855 | `$0.35` | **98,855.0** | 6 | 1 | **177.0s** |
| **Shard Author shard_15** | `C-09, C-10` | 2 | 68,355 | 29,662 | 180,184 | 98,017 | `$0.34` | **49,008.5** | 5 | 0 | **150.0s** |
| **Shard Author shard_16 🛑** | `C-11, C-12` | 2 | 197,897 | 45,422 | 1,220,905 | 243,319 | `$0.73` | **121,659.5** | 18 | 3 | **306.0s** |
| **Shard Author shard_02a** | `Hab-02` | 1 | 53,925 | 17,571 | 186,698 | 71,496 | `$0.23` | **71,496.0** | 6 | 1 | **101.0s** |
| **Shard Author shard_06b** | `Hab-06` | 1 | 62,278 | 27,180 | 211,694 | 89,458 | `$0.31` | **89,458.0** | 6 | 1 | **149.0s** |
| **Shard Author shard_10b** | `Hab-10` | 1 | 54,664 | 19,717 | 192,717 | 74,381 | `$0.24` | **74,381.0** | 6 | 1 | **122.0s** |
| **Shard Author shard_17** | `C-13` | 1 | 59,017 | 24,013 | 207,381 | 83,030 | `$0.28` | **83,030.0** | 6 | 1 | **120.0s** |
| **Shard Author shard_11** | `C-05, C-06` | 2 | 81,991 | 32,183 | 505,525 | 114,174 | `$0.40` | **57,087.0** | 10 | 1 | **183.0s** |
| **Shard Author shard_04** | `Hab-04` | 1 | 59,127 | 24,246 | 159,573 | 83,373 | `$0.28` | **83,373.0** | 5 | 0 | **130.0s** |
| **Shard Author shard_05** | `Hab-05` | 1 | 61,450 | 26,512 | 164,247 | 87,962 | `$0.30` | **87,962.0** | 5 | 0 | **125.0s** |
| **Shard Author shard_12** | `C-03, C-04` | 2 | 76,365 | 28,305 | 417,141 | 104,670 | `$0.36` | **52,335.0** | 9 | 2 | **185.0s** |
| **Shard Author shard_06** | `Hab-06` | 1 | 76,044 | 31,459 | 425,152 | 107,503 | `$0.38` | **107,503.0** | 9 | 1 | **173.0s** |
| **Shard Author shard_13** | `C-01, C-02` | 2 | 66,915 | 52,346 | 179,206 | 119,261 | `$0.51` | **59,630.5** | 5 | 1 | **219.0s** |
| **Shard Author shard_07** | `Hab-07` | 1 | 68,773 | 39,185 | 218,211 | 107,958 | `$0.41` | **107,958.0** | 6 | 1 | **181.0s** |
| **Shard Author shard_14** | `C-07, C-08` | 2 | 62,796 | 47,910 | 168,780 | 110,706 | `$0.47` | **55,353.0** | 5 | 1 | **200.0s** |
| **Shard Author shard_15** | `C-09, C-10` | 2 | 60,227 | 23,303 | 162,684 | 83,530 | `$0.28` | **41,765.0** | 5 | 0 | **114.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 30,516 | 26,056 | 24,738 | 56,572 | `$0.24` | **56,572.0** | 2 | 0 | **107.0s** |
| **Shard Author shard_16** | `C-11, C-12` | 2 | 32,124 | 27,114 | 24,741 | 59,238 | `$0.25` | **29,619.0** | 2 | 0 | **113.0s** |
| **Shard Author shard_09** | `Hab-09` | 1 | 30,610 | 24,238 | 24,736 | 54,848 | `$0.23` | **54,848.0** | 2 | 0 | **103.0s** |
| **Shard Author shard_01** | `Hab-01` | 1 | 30,128 | 24,236 | 24,738 | 54,364 | `$0.23` | **54,364.0** | 2 | 0 | **112.0s** |
| **Shard Author shard_10** | `Hab-10` | 1 | 0 | 0 | 0 | 0 | `$0.00` | **0.0** | 0 | 0 | **0.0s** |

---

### 3.3b. Stage 3B: Remediación y Repair Engineers (Ingenieros de Reparación)
- **Total de Repair Engineers Desplegados:** `6 subagentes` en **`3 ronda(s)`** (`DONE`: `5`, `BLOCKED`: **`1`**)
- **Duración Mínima:** `19.0s` | **Mediana:** `41.0s` | **Máxima:** `66.0s` (`1.1 min`)
- **Tokens Activos Totales en Reparación:** `296,581 tokens`
- **Costo Estimado Etapa 3B (Gemini 4 Hydrogen):** **`$0.71 USD`**
- **Agente Determinante del Retraso:** `Repair Engineer C-13`

| Repair Engineer | Estado | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Errores | Duración |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Repair Engineer Hab-10** | `DONE` | 5 | 35,794 | 4,609 | 101,104 | 40,403 | `$0.10` | 0 | **41.0s** |
| **Repair Engineer Hab-09** | `DONE` | 6 | 48,638 | 7,897 | 143,974 | 56,535 | `$0.14` | 0 | **61.0s** |
| **Repair Engineer C-13** | `DONE` | 5 | 54,751 | 11,266 | 127,189 | 66,017 | `$0.18` | 0 | **66.0s** |
| **Repair Engineer Hab-08** | `DONE` | 5 | 39,748 | 5,747 | 107,763 | 45,495 | `$0.11` | 0 | **40.0s** |
| **Repair Engineer Hab-10** | `BLOCKED` | 4 | 45,951 | 3,000 | 69,809 | 48,951 | `$0.10` | 0 | **19.0s** |
| **Repair Engineer Hab-10** | `DONE` | 5 | 35,463 | 3,717 | 100,710 | 39,180 | `$0.09` | 0 | **33.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ⚠️ NO PASÓ AL PRIMER INTENTO — APROBADO POST-REJUDGE (143/143 REACTIVOS)  
> La Ronda 1 de Blind Judges registró 1 discrepancia(s), por lo que no hubo acuerdo limpio al primer intento. Tras correcciones y Rejudge, el resultado final alcanzó 100.0% de acuerdo (0 discrepancias).

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `143 reactivos` (23 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `22 jueces` | Aislamiento epistémico en Stage 5 |
| **Costo Etapa 5 (Gemini 4 Hydrogen)** | **`$2.92 USD`** | Evaluado sobre los 22 Blind Judges (In: `721,512`, Out: `237,603`, Cache: `725,040`) |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | Ronda 1: 1 discrepancia(s) (`flaw_detected`: 1, `kernel_override`: 0); 0 violaciones iniciales |
| **Resultado Final Post-Rejudge** | **`✅ Aprobado`** | `100.0%` acuerdo, `0` discrepancia(s) |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `2 operaciones directas` | 2 ediciones registradas |

#### Detalle de Acciones Registradas:
- 1. **Ronda 1 (`judge_report_round_1.json` / `rounds_history`)**: 1 discrepancia(s) detectada(s).
- 2. **Bucle de Auto-Reparación / Rejudge**: 3 ola(s) de jueces ejecutada(s) (4 intervenciones de supervisor).
- 3. **Resultado Final Post-Rejudge (`judge_report.json`)**: ✅ Aprobado (`100.0% agreement rate`, `0 discrepancias` sobre 143 reactivos).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo y Costo del Orquestador
- 💵 **Costo Estimado del Orquestador Principal (Gemini 4 Hydrogen):** **`$0.61 USD`** (In: `245,079`, Out: `18,896`, Cache: `1,385,979`)
- ⏱️ **Tiempo Total de Pared del Orquestador:** `58.55 min` (`3513.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `0.92 min` (`55.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.3 min`** (`18.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `28.05 min` (`1683.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `1.78 min` (`107.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`4`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **47** | `run.py` | Parche de Infraestructura Core | Ajuste en run.py | `edit_file` | 4,611 |
| **47** | `run.py` | Parche de Infraestructura Core | Ajuste en run.py | `edit_file` | 4,611 |
| **56** | `dispatch.py` | Modificación / Script Auxiliar | Created At: 2026-11-28T04:01:32-05:00
Completed At: 2026-11-28T04:01:33-05:00
Created At:  | `edit_file` | 4,480 |
| **56** | `dispatch.py` | Modificación / Script Auxiliar | Created At: 2026-11-28T04:01:32-05:00
Completed At: 2026-11-28T04:01:33-05:00
Created At:  | `edit_file` | 4,480 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Síndrome del Orquestador Reparador (4 intervenciones manuales)
- **Ámbito:** `Director (Orchestrator)`
- **Diagnóstico:** El orquestador principal ejecutó 4 operaciones directas de edición de código y plantillas. Consumió más de 18,182 tokens en turnos de mantenimiento/recuperación manual.

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_16
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_16 tardó 306.0s frente a la mediana de 150.0s (+156.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

### ⚠️ [MEDIUM] Fricción de Herramientas en 1 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_16 acumularon fallos en consola (3 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `108 turnos`
- **Volumen Total de Razonamiento:** `266,373 caracteres`
- **Razonamiento del Orquestador:** `19 turnos` (5,893 chars)
- **Razonamiento de Subagentes:** `89 turnos` (260,480 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Repair Engineer Hab-10** | 2 | 2,068 | 0 |
| **Blind Judge 01** | 1 | 1,251 | 0 |
| **Shard Author shard_13** | 1 | 4,568 | 0 |
| **Shard Author shard_10** | 2 | 5,419 | ⚠️ 1 |
| **Shard Author shard_17** | 2 | 3,555 | ⚠️ 1 |
| **Shard Author shard_14** | 3 | 2,377 | ⚠️ 2 |
| **Shard Author shard_16** | 3 | 2,550 | ⚠️ 2 |
| **Shard Author shard_01** | 1 | 6,698 | 0 |
| **Shard Author shard_02** | 2 | 6,313 | ⚠️ 1 |
| **Shard Author shard_03** | 2 | 4,970 | ⚠️ 1 |
| **Shard Author shard_07** | 3 | 6,029 | ⚠️ 2 |
| **Shard Author shard_08** | 3 | 5,875 | ⚠️ 1 |
| **Shard Author shard_09** | 2 | 6,203 | ⚠️ 1 |
| **Blind Judge 01** | 1 | 4,882 | 0 |
| **Blind Judge 02** | 1 | 5,918 | 0 |
| **Blind Judge 03** | 1 | 5,578 | 0 |
| **Blind Judge 04** | 2 | 7,947 | 0 |
| **Blind Judge 05** | 1 | 4,475 | 0 |
| **Blind Judge 06** | 1 | 4,928 | 0 |
| **Blind Judge 07** | 1 | 6,324 | 0 |
| **Blind Judge 08** | 1 | 4,052 | 0 |
| **Blind Judge 09** | 1 | 4,724 | 0 |
| **Repair Engineer Hab-09** | 1 | 1,643 | 0 |
| **Blind Judge 01** | 1 | 1,644 | 0 |
| **Shard Author shard_15** | 1 | 1,771 | 0 |
| **Shard Author shard_16** | 4 | 3,527 | ⚠️ 3 |
| **Shard Author shard_02a** | 2 | 5,372 | ⚠️ 1 |
| **Shard Author shard_06b** | 2 | 7,263 | ⚠️ 1 |
| **Shard Author shard_10b** | 2 | 4,967 | ⚠️ 1 |
| **Shard Author shard_17** | 2 | 2,800 | ⚠️ 1 |
| **Blind Judge 01** | 1 | 7,008 | 0 |
| **Blind Judge 02** | 1 | 4,328 | 0 |
| **Blind Judge 03** | 1 | 5,332 | 0 |
| **Blind Judge 04** | 1 | 5,280 | 0 |
| **Blind Judge 05** | 1 | 6,720 | 0 |
| **Blind Judge 06** | 1 | 5,288 | 0 |
| **Blind Judge 07** | 1 | 6,221 | 0 |
| **Blind Judge 08** | 1 | 4,453 | 0 |
| **Blind Judge 09** | 1 | 5,180 | 0 |
| **Repair Engineer C-13** | 2 | 2,646 | 0 |
| **Repair Engineer Hab-08** | 2 | 2,256 | 0 |
| **Repair Engineer Hab-10** | 2 | 1,355 | 0 |
| **Repair Engineer Hab-10** | 1 | 1,515 | 0 |
| **Blind Judge 01** | 1 | 4,011 | 0 |
| **Blind Judge 02** | 1 | 4,831 | 0 |
| **Shard Author shard_11** | 1 | 4,624 | ⚠️ 1 |
| **Shard Author shard_04** | 1 | 5,896 | 0 |
| **Shard Author shard_05** | 1 | 4,898 | 0 |
| **Shard Author shard_12** | 2 | 3,074 | ⚠️ 2 |
| **Shard Author shard_06** | 2 | 6,578 | ⚠️ 1 |
| **Shard Author shard_13** | 3 | 6,853 | ⚠️ 1 |
| **Shard Author shard_07** | 2 | 4,081 | ⚠️ 1 |
| **Shard Author shard_14** | 2 | 2,819 | ⚠️ 1 |
| **Shard Author shard_15** | 1 | 1,800 | 0 |
| **Shard Author shard_08** | 1 | 4,355 | 0 |
| **Shard Author shard_16** | 1 | 3,192 | 0 |
| **Shard Author shard_09** | 1 | 4,791 | 0 |
| **Shard Author shard_01** | 1 | 5,404 | 0 |
| **Shard Author shard_10** | 0 | 0 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*