# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Mateco 4 Optimizacion K4 V2 (`mateco_4_optimizacion_k4_v2`)

**Fecha de Auditoría:** `2026-11-24 19:24:57 UTC`  
**Conversación Orquestadora:** [`753e4e81-d4e5-4916-9eac-076c1c9e92e8`](conversation://753e4e81-d4e5-4916-9eac-076c1c9e92e8)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_k4_v2\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias, Costos USD (Gemini 4 Hydrogen) y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `6 archivos` (71 págs / 3.61 MB) | 01_optimizacion_dinamica.pdf, 02_Set_Problem_Calculo_de_variaciones.pdf, 03_Teoria_de_control_optimo___teoria (1).pdf, 04_opt_din_3.pdf, 05_Control Optimo Apuntes.pdf, 06_Problemas_teoria_de_control.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`32 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`32 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`65 subagentes`** | Visión (0), CTA (8), Autores (32), Repairs (6), Jueces (19) |
| **Reactivos Finales Validados** | **`1472 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`3,768,686` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`1,412,441` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`11,252,760` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`5,263,849` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`16,516,609` tokens** | Consumo total de cuota facturable |
| **Costo Estimado Total (Gemini 4 Hydrogen)** | **`$17.23 USD`** | In: `$5.77` (`$1.50/1M`), Out+Think: `$10.61` (`$7.50/1M`), Cache: `$0.84` (`$0.08/1M`) |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`11,220.5 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`3,576.0 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`516,144.0 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`108,200.2 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`232,628.3 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Costo Estimado por Pregunta (Hydrogen)** | **`$0.01 USD/preg`** | Costo monetario valorizado por reactivo |
| **Costo Estimado por Competencia (Hydrogen)** | **`$0.54 USD/comp`** | Costo monetario valorizado por competencia |
| **Segundos de Pared por Pregunta** | **`1.07 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`55.93 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`5.88x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0a. Valorización Monetaria por Etapa (Tarifas Gemini 4 Hydrogen)
> Tarifas oficiales aplicables: Entrada `$1.50/1M`, Caché leído `$0.08/1M`, Salida (incl. thinking) `$7.50/1M`.

| Etapa / Rol | Agentes | Tokens Entrada | Tokens Salida | Caché Leído | Costo Estimado (USD) | % del Total |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Stage 1A: Visión** | 0 | 0 | 0 | 0 | **`$0.00`** | 0.0% |
| **Stage 1B: CTA Architects** | 8 | 333,744 | 86,666 | 932,442 | **`$1.22`** | 7.1% |
| **Stage 3: Shard Authors** | 32 | 2,436,163 | 1,026,244 | 8,299,537 | **`$11.97`** | 69.5% |
| **Stage 3B: Repair Engineers** | 6 | 335,266 | 58,554 | 1,176,273 | **`$1.03`** | 6.0% |
| **Stage 5: Blind Judges** | 19 | 663,513 | 240,977 | 665,170 | **`$2.85`** | 16.5% |
| **Orquestador Principal (Director)** | 1 | 80,007 | 2,715 | 179,338 | **`$0.15`** | 0.9% |
| **TOTAL CORRIDA (Gemini 4 Hydrogen)** | **66** | **3,848,693** | **1,415,156** | **11,252,760** | **`$17.23 USD`** | **100.0%** |

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `753e4e81`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-11-24 18:58:45` | `0.11s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-11-24 18:58:45` | `0.21s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_k4_v2\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-11-24 19:02:09` | `2.45s` | `0` (`0` act) | 0 | `competencies=32` |
| **`02_shard`** | `2026-11-24 19:02:10` | `0.07s` | `0` (`0` act) | 0 | `shards=32` |
| **`03_templates`** | `2026-11-24 19:24:38` | `0.81s` | `0` (`0` act) | 0 | `count=32` |
| **`04_build`** | `2026-11-24 19:24:48` | `10.03s` | `0` (`0` act) | 0 | `total_questions=1472` |
| **`05_verify`** | `2026-11-24 19:24:51` | `2.68s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_k4_v2\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-11-24 19:19:00` | `0.2s` | `0` (`0` act) | 0 | `passed=False` |
| **`06_publish`** | `2026-11-24 19:24:56` | `5.77s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\mateco_4_optimizacion_k4_v2.json` |

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
- **Tiempo de Pared Fase Mappers (Máximo):** **`87.0s`** (determinado por `CTA Harmonizer`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`103.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`190.0s`** (`3.2 min`)
- **Costo Estimado Etapa 1B (Gemini 4 Hydrogen):** **`$1.22 USD`**

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Costo (USD) | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- |
| **Cognitive Task Analysis Architect part_01** | Mapper | 4 | 37,107 | 9,391 | 69,891 | `$0.13` | 0 | **79.0s** |
| **Cognitive Task Analysis Architect part_05** | Mapper | 4 | 38,777 | 10,725 | 72,063 | `$0.14` | 0 | **87.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 4 | 38,322 | 10,576 | 71,556 | `$0.14` | 0 | **65.0s** |
| **Cognitive Task Analysis Architect part_04** | Mapper | 6 | 37,183 | 10,281 | 116,029 | `$0.14` | 1 | **83.0s** |
| **Cognitive Task Analysis Architect part_06** | Mapper | 4 | 32,483 | 9,804 | 60,554 | `$0.13` | 0 | **64.0s** |
| **Cognitive Task Analysis Architect part_03** | Mapper | 4 | 30,958 | 11,333 | 55,796 | `$0.14` | 0 | **64.0s** |
| **Cognitive Task Analysis Architect part_07** | Mapper | 4 | 26,650 | 10,551 | 47,781 | `$0.12` | 0 | **79.0s** |
| **CTA Harmonizer** | Harmonizer | 8 | 92,264 | 14,005 | 438,772 | `$0.28` | 1 | **103.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `32 shards concurrentes`
- **Tasa de Aprobación en 1ra Compilación:** **`6/32 (18.75%)`** (Reglas en 1er fallo: `[INVARIANT]` (10), `[TPL-STEM-EQUATION-PARITY]` (10), `[TPL-STEM-VARIANT-PARITY]` (7), `[TPL-DYNAMIC-RATIONALE]` (6), `[TPL-STATIC-OPT]` (5), `[TPL-DIGIT-PLACEHOLDER-CONCAT]` (5))
- **Duración Mínima de Shard:** `107.0s` | **Mediana:** `168.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`279.0s`** (`4.7 min`) por `Shard Author shard_18`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+111.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`108,200.2 tokens/competencia`**
- **Costo Estimado Etapa 3 (Gemini 4 Hydrogen):** **`$11.97 USD`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **Shard Author shard_01** | `Hab-10` | 1 | 150,108 | 37,859 | 331,115 | 187,967 | `$0.53` | **187,967.0** | 8 | 1 | **197.0s** |
| **Shard Author shard_02** | `Hab-15` | 1 | 91,490 | 52,034 | 328,963 | 143,524 | `$0.55` | **143,524.0** | 7 | 1 | **241.0s** |
| **Shard Author shard_03** | `Hab-18` | 1 | 77,606 | 35,617 | 372,789 | 113,223 | `$0.41` | **113,223.0** | 8 | 1 | **195.0s** |
| **Shard Author shard_04** | `Hab-19` | 1 | 87,927 | 35,697 | 587,903 | 123,624 | `$0.44` | **123,624.0** | 11 | 1 | **205.0s** |
| **Shard Author shard_05** | `Hab-20` | 1 | 89,540 | 36,728 | 613,893 | 126,268 | `$0.46` | **126,268.0** | 11 | 1 | **220.0s** |
| **Shard Author shard_06** | `Hab-01` | 1 | 76,715 | 42,367 | 238,901 | 119,082 | `$0.45` | **119,082.0** | 6 | 1 | **199.0s** |
| **Shard Author shard_07** | `Hab-02` | 1 | 93,731 | 28,113 | 191,686 | 121,844 | `$0.37` | **121,844.0** | 6 | 1 | **151.0s** |
| **Shard Author shard_08** | `Hab-03` | 1 | 66,907 | 29,840 | 224,733 | 96,747 | `$0.34` | **96,747.0** | 6 | 1 | **157.0s** |
| **Shard Author shard_09** | `Hab-04` | 1 | 89,754 | 49,403 | 394,732 | 139,157 | `$0.53` | **139,157.0** | 8 | 1 | **241.0s** |
| **Shard Author shard_13** | `Hab-08` | 1 | 67,432 | 27,405 | 288,474 | 94,837 | `$0.33` | **94,837.0** | 7 | 1 | **168.0s** |
| **Shard Author shard_14** | `Hab-09` | 1 | 82,088 | 34,033 | 392,615 | 116,121 | `$0.41` | **116,121.0** | 8 | 1 | **210.0s** |
| **Shard Author shard_15** | `Hab-11` | 1 | 53,931 | 21,919 | 103,227 | 75,850 | `$0.25` | **75,850.0** | 4 | 0 | **116.0s** |
| **Shard Author shard_16** | `Hab-13` | 1 | 79,868 | 36,165 | 492,854 | 116,033 | `$0.43` | **116,033.0** | 10 | 3 | **234.0s** |
| **Shard Author shard_17** | `Hab-14` | 1 | 71,469 | 29,631 | 344,739 | 101,100 | `$0.36` | **101,100.0** | 8 | 2 | **186.0s** |
| **Shard Author shard_18 🛑** | `Hab-16` | 1 | 92,342 | 57,600 | 274,199 | 149,942 | `$0.59` | **149,942.0** | 6 | 1 | **279.0s** |
| **Shard Author shard_10** | `Hab-05` | 1 | 81,603 | 45,876 | 243,852 | 127,479 | `$0.48` | **127,479.0** | 6 | 1 | **240.0s** |
| **Shard Author shard_11** | `Hab-06` | 1 | 62,251 | 26,548 | 214,164 | 88,799 | `$0.31` | **88,799.0** | 6 | 1 | **154.0s** |
| **Shard Author shard_12** | `Hab-07` | 1 | 62,267 | 26,571 | 216,237 | 88,838 | `$0.31` | **88,838.0** | 6 | 1 | **162.0s** |
| **Shard Author shard_25** | `C-05` | 1 | 80,651 | 45,023 | 246,110 | 125,674 | `$0.48` | **125,674.0** | 6 | 1 | **207.0s** |
| **Shard Author shard_26** | `C-06` | 1 | 60,456 | 22,293 | 248,996 | 82,749 | `$0.28` | **82,749.0** | 7 | 1 | **134.0s** |
| **Shard Author shard_27** | `C-08` | 1 | 52,343 | 20,959 | 100,700 | 73,302 | `$0.24` | **73,302.0** | 4 | 0 | **109.0s** |
| **Shard Author shard_19** | `C-03` | 1 | 68,985 | 32,475 | 235,076 | 101,460 | `$0.36` | **101,460.0** | 6 | 1 | **177.0s** |
| **Shard Author shard_20** | `C-10` | 1 | 67,696 | 31,664 | 240,026 | 99,360 | `$0.36` | **99,360.0** | 6 | 1 | **166.0s** |
| **Shard Author shard_21** | `C-12` | 1 | 74,684 | 38,746 | 230,561 | 113,430 | `$0.42` | **113,430.0** | 6 | 1 | **187.0s** |
| **Shard Author shard_22** | `C-01` | 1 | 56,963 | 22,215 | 196,378 | 79,178 | `$0.27` | **79,178.0** | 6 | 1 | **124.0s** |
| **Shard Author shard_23** | `C-02` | 1 | 55,547 | 24,337 | 104,206 | 79,884 | `$0.27` | **79,884.0** | 4 | 0 | **115.0s** |
| **Shard Author shard_24** | `C-04` | 1 | 51,566 | 20,061 | 99,820 | 71,627 | `$0.24` | **71,627.0** | 4 | 0 | **107.0s** |
| **Shard Author shard_28** | `C-09` | 1 | 105,532 | 23,838 | 53,212 | 129,370 | `$0.34` | **129,370.0** | 4 | 0 | **114.0s** |
| **Shard Author shard_29** | `C-11` | 1 | 113,754 | 25,312 | 156,554 | 139,066 | `$0.37` | **139,066.0** | 6 | 1 | **151.0s** |
| **Shard Author shard_30** | `C-13` | 1 | 57,229 | 19,615 | 233,196 | 76,844 | `$0.25` | **76,844.0** | 7 | 1 | **128.0s** |
| **Shard Author shard_31** | `C-14` | 1 | 58,198 | 26,656 | 106,314 | 84,854 | `$0.30` | **84,854.0** | 4 | 0 | **133.0s** |
| **Shard Author shard_32** | `H-01` | 1 | 55,530 | 19,644 | 193,312 | 75,174 | `$0.25` | **75,174.0** | 6 | 1 | **122.0s** |

---

### 3.3b. Stage 3B: Remediación y Repair Engineers (Ingenieros de Reparación)
- **Total de Repair Engineers Desplegados:** `6 subagentes` en **`1 ronda(s)`** (`DONE`: `6`, `BLOCKED`: **`0`**)
- **Duración Mínima:** `48.0s` | **Mediana:** `69.0s` | **Máxima:** `145.0s` (`2.4 min`)
- **Tokens Activos Totales en Reparación:** `393,820 tokens`
- **Costo Estimado Etapa 3B (Gemini 4 Hydrogen):** **`$1.03 USD`**
- **Agente Determinante del Retraso:** `Repair Engineer Hab-07`

| Repair Engineer | Estado | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Costo (USD) | Errores | Duración |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Repair Engineer C-01** | `DONE` | 5 | 44,785 | 4,107 | 107,251 | 48,892 | `$0.11` | 0 | **48.0s** |
| **Repair Engineer C-14** | `DONE` | 5 | 51,507 | 9,725 | 127,655 | 61,232 | `$0.16` | 0 | **67.0s** |
| **Repair Engineer Hab-07** | `DONE` | 10 | 68,274 | 18,066 | 393,682 | 86,340 | `$0.27` | 2 | **145.0s** |
| **Repair Engineer Hab-09** | `DONE` | 5 | 54,020 | 11,091 | 125,500 | 65,111 | `$0.17` | 0 | **69.0s** |
| **Repair Engineer Hab-13** | `DONE` | 5 | 51,153 | 9,223 | 120,245 | 60,376 | `$0.15` | 0 | **80.0s** |
| **Repair Engineer Hab-20** | `DONE` | 8 | 65,527 | 6,342 | 301,940 | 71,869 | `$0.17` | 1 | **63.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ⚠️ NO PASÓ AL PRIMER INTENTO — APROBADO POST-REJUDGE (147/147 REACTIVOS)  
> La Ronda 1 de Blind Judges registró 5 discrepancia(s), por lo que no hubo acuerdo limpio al primer intento. Tras correcciones y Rejudge, el resultado final alcanzó 100.0% de acuerdo (0 discrepancias).

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `147 reactivos` (32 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `19 jueces` | Aislamiento epistémico en Stage 5 |
| **Costo Etapa 5 (Gemini 4 Hydrogen)** | **`$2.85 USD`** | Evaluado sobre los 19 Blind Judges (In: `663,513`, Out: `240,977`, Cache: `665,170`) |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | Ronda 1: 5 discrepancia(s) (`flaw_detected`: 4, `kernel_override`: 2); 0 violaciones iniciales |
| **Resultado Final Post-Rejudge** | **`✅ Aprobado`** | `100.0%` acuerdo, `0` discrepancia(s) |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Ronda 1 (`judge_report_round_1.json` / `rounds_history`)**: 5 discrepancia(s) detectada(s).
- 2. **Bucle de Auto-Reparación / Rejudge**: 3 ola(s) de jueces ejecutada(s) (0 intervenciones de supervisor).
- 3. **Resultado Final Post-Rejudge (`judge_report.json`)**: ✅ Aprobado (`100.0% agreement rate`, `0 discrepancias` sobre 147 reactivos).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo y Costo del Orquestador
- 💵 **Costo Estimado del Orquestador Principal (Gemini 4 Hydrogen):** **`$0.15 USD`** (In: `80,007`, Out: `2,715`, Cache: `179,338`)
- ⏱️ **Tiempo Total de Pared del Orquestador:** `26.32 min` (`1579.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `0.33 min` (`20.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `25.6 min` (`1536.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `0.35 min` (`21.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### ⚠️ [MEDIUM] Fricción de Herramientas en 1 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_16 acumularon fallos en consola (3 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `136 turnos`
- **Volumen Total de Razonamiento:** `692,958 caracteres`
- **Razonamiento del Orquestador:** `4 turnos` (1,538 chars)
- **Razonamiento de Subagentes:** `132 turnos` (691,420 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Repair Engineer C-01** | 1 | 2,364 | 0 |
| **Repair Engineer C-14** | 3 | 5,438 | 0 |
| **Repair Engineer Hab-07** | 5 | 11,132 | ⚠️ 2 |
| **Repair Engineer Hab-09** | 1 | 4,512 | 0 |
| **Repair Engineer Hab-13** | 1 | 3,968 | 0 |
| **Repair Engineer Hab-20** | 2 | 3,767 | ⚠️ 1 |
| **Blind Judge 01** | 1 | 8,913 | 0 |
| **Blind Judge 02** | 1 | 10,679 | 0 |
| **Blind Judge 03** | 1 | 10,903 | 0 |
| **Blind Judge 04** | 1 | 7,711 | 0 |
| **Blind Judge 05** | 1 | 11,938 | 0 |
| **Blind Judge 06** | 1 | 13,066 | 0 |
| **Blind Judge 07** | 1 | 11,767 | 0 |
| **Blind Judge 08** | 1 | 13,488 | 0 |
| **Blind Judge 09** | 1 | 9,045 | 0 |
| **Cognitive Task Analysis Architect part_01** | 3 | 5,694 | 0 |
| **Cognitive Task Analysis Architect part_05** | 4 | 7,964 | 0 |
| **Cognitive Task Analysis Architect part_02** | 2 | 5,948 | 0 |
| **Cognitive Task Analysis Architect part_04** | 4 | 5,920 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_06** | 3 | 4,716 | 0 |
| **Cognitive Task Analysis Architect part_03** | 3 | 6,017 | 0 |
| **Cognitive Task Analysis Architect part_07** | 3 | 6,764 | 0 |
| **CTA Harmonizer** | 3 | 13,995 | ⚠️ 1 |
| **Shard Author shard_01** | 3 | 18,959 | ⚠️ 1 |
| **Shard Author shard_02** | 2 | 15,166 | ⚠️ 1 |
| **Shard Author shard_03** | 2 | 15,042 | ⚠️ 1 |
| **Shard Author shard_04** | 3 | 16,888 | ⚠️ 1 |
| **Shard Author shard_05** | 3 | 11,039 | ⚠️ 1 |
| **Shard Author shard_06** | 2 | 14,647 | ⚠️ 1 |
| **Shard Author shard_07** | 3 | 12,687 | ⚠️ 1 |
| **Shard Author shard_08** | 3 | 15,140 | ⚠️ 1 |
| **Shard Author shard_09** | 2 | 14,886 | ⚠️ 1 |
| **Shard Author shard_13** | 2 | 10,648 | ⚠️ 1 |
| **Shard Author shard_14** | 4 | 13,188 | ⚠️ 1 |
| **Shard Author shard_15** | 1 | 10,157 | 0 |
| **Shard Author shard_16** | 4 | 17,464 | ⚠️ 3 |
| **Shard Author shard_17** | 4 | 10,319 | ⚠️ 2 |
| **Shard Author shard_18** | 2 | 24,419 | ⚠️ 1 |
| **Shard Author shard_10** | 2 | 16,979 | ⚠️ 1 |
| **Shard Author shard_11** | 2 | 14,237 | ⚠️ 1 |
| **Shard Author shard_12** | 2 | 10,302 | ⚠️ 1 |
| **Shard Author shard_25** | 2 | 16,964 | ⚠️ 1 |
| **Shard Author shard_26** | 2 | 8,798 | ⚠️ 1 |
| **Shard Author shard_27** | 1 | 5,358 | 0 |
| **Shard Author shard_19** | 2 | 8,809 | ⚠️ 1 |
| **Shard Author shard_20** | 2 | 16,003 | ⚠️ 1 |
| **Shard Author shard_21** | 3 | 13,309 | ⚠️ 1 |
| **Shard Author shard_22** | 2 | 5,424 | ⚠️ 1 |
| **Shard Author shard_23** | 1 | 10,425 | 0 |
| **Shard Author shard_24** | 1 | 8,637 | 0 |
| **Shard Author shard_28** | 1 | 13,852 | 0 |
| **Shard Author shard_29** | 2 | 13,011 | ⚠️ 1 |
| **Shard Author shard_30** | 3 | 5,770 | ⚠️ 1 |
| **Shard Author shard_31** | 1 | 11,452 | 0 |
| **Shard Author shard_32** | 2 | 8,521 | ⚠️ 1 |
| **Blind Judge 01** | 1 | 7,243 | 0 |
| **Blind Judge 02** | 1 | 11,184 | 0 |
| **Blind Judge 03** | 1 | 9,673 | 0 |
| **Blind Judge 04** | 2 | 9,126 | 0 |
| **Blind Judge 05** | 2 | 10,219 | 0 |
| **Blind Judge 06** | 1 | 9,190 | 0 |
| **Blind Judge 07** | 2 | 14,417 | 0 |
| **Blind Judge 08** | 1 | 7,798 | 0 |
| **Blind Judge 09** | 2 | 10,125 | 0 |
| **Blind Judge 01** | 1 | 8,236 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*