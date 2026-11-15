# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Estadistica 3 Pre Pc2 (`estadistica_3_pre_pc2`)

**Fecha de Auditoría:** `2026-11-15 07:34:06 UTC`  
**Conversación Orquestadora:** [`e0291cf4-7aae-45dc-be49-f0f5ecad26b4`](conversation://e0291cf4-7aae-45dc-be49-f0f5ecad26b4)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_pc2\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `4 archivos` (129 págs / 1.88 MB) | 01_semana_9_apuntes.pdf, 02_EST3_LEC07_26.2_V2.pdf, 03_EST3_LEC08_26.2_v1.pdf, 04_semana_10_apuntes.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`57 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`24 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`103 subagentes`** | Visión (0), CTA (9), Autores (24), Repairs (39), Jueces (31) |
| **Reactivos Finales Validados** | **`1390 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`9,031,361` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`2,080,550` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`74,738,796` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`12,959,805` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`87,698,601` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`63,092.5 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`9,323.6 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`1,538,571.9 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`91,658.8 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`679,834.1 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`5.38 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`11.16 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`9.31x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `e0291cf4`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-11-15 05:29:36` | `0.24s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-11-15 05:29:36` | `0.29s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_pc2\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-11-15 05:35:49` | `0.42s` | `2,545,438` (`756,662` act) | 11 | `needs_harmonize=True` |
| **`02_shard`** | `2026-11-15 05:36:29` | `0.07s` | `0` (`0` act) | 0 | `shards=24` |
| **`03_templates`** | `2026-11-15 07:33:45` | `0.56s` | `50,945,520` (`9,287,626` act) | 61 | `count=57` |
| **`04_build`** | `2026-11-15 07:33:55` | `9.98s` | `19,718,842` (`4,112,518` act) | 39 | `total_questions=1390` |
| **`05_verify`** | `2026-11-15 07:33:59` | `3.84s` | `21,443,520` (`5,172,861` act) | 70 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_pc2\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-11-15 06:46:12` | `0.02s` | `1,681,898` (`1,038,820` act) | 30 | `passed=False` |
| **`06_publish`** | `2026-11-15 07:34:05` | `4.79s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_pc2.json` |

---

### 3.1. Stage 1A: Preprocesamiento de Visión
- **Subagentes de Visión Desplegados:** `0 agentes en paralelo`
- **Tiempo de Pared de la Etapa (Máximo / Critical Path):** **`0.0s`** (`0.0 min`)
- **Agente Determinante del Camino Crítico:** `N/A`

| Subagente de Visión | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

---

### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)
- **Arquitectura:** `MAPREDUCE (8 Mappers + 1 Harmonizer)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`98.0s`** (determinado por `CTA Harmonizer`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`228.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`326.0s`** (`5.4 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cognitive Task Analysis Architect part_06** | Mapper | 6 | 50,010 | 13,298 | 140,337 | 0 | **76.0s** |
| **Cognitive Task Analysis Architect part_03** | Mapper | 6 | 44,369 | 11,157 | 125,385 | 0 | **65.0s** |
| **Cognitive Task Analysis Architect part_04** | Mapper | 6 | 61,535 | 15,725 | 172,631 | 0 | **92.0s** |
| **Cognitive Task Analysis Architect part_01** | Mapper | 6 | 64,863 | 11,896 | 186,341 | 0 | **66.0s** |
| **Cognitive Task Analysis Architect part_05** | Mapper | 6 | 54,605 | 12,654 | 154,995 | 0 | **75.0s** |
| **Cognitive Task Analysis Architect part_08** | Mapper | 9 | 70,080 | 10,708 | 352,010 | 1 | **98.0s** |
| **Cognitive Task Analysis Architect part_07** | Mapper | 6 | 57,666 | 9,187 | 167,531 | 0 | **65.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 6 | 105,673 | 14,153 | 131,922 | 0 | **84.0s** |
| **CTA Harmonizer** | Harmonizer | 9 | 90,573 | 16,347 | 496,158 | 1 | **228.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `24 shards concurrentes`
- **Duración Mínima de Shard:** `84.0s` | **Mediana:** `2739.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`3034.0s`** (`50.6 min`) por `Shard Author shard_14`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+295.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`91,658.8 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_01** | `Hab-03, Hab-04` | 2 | 217,328 | 51,750 | 1,165,494 | 269,078 | **134,539.0** | 24 | 9 | **2825.0s** |
| **Shard Author shard_02** | `Hab-01, Hab-02` | 2 | 112,802 | 29,188 | 435,521 | 141,990 | **70,995.0** | 14 | 4 | **2108.0s** |
| **Shard Author shard_03** | `Hab-05, Hab-06` | 2 | 236,004 | 48,530 | 1,600,468 | 284,534 | **142,267.0** | 32 | 8 | **2805.0s** |
| **Shard Author shard_04** | `Hab-07, Hab-08` | 2 | 166,059 | 51,382 | 1,711,286 | 217,441 | **108,720.5** | 32 | 8 | **2297.0s** |
| **Shard Author shard_05** | `Hab-09, Hab-10` | 2 | 41,801 | 16,704 | 127,954 | 58,505 | **29,252.5** | 6 | 1 | **88.0s** |
| **Shard Author shard_06** | `Hab-12, Hab-13` | 2 | 44,715 | 19,432 | 136,325 | 64,147 | **32,073.5** | 6 | 1 | **98.0s** |
| **Shard Author shard_07** | `Hab-14, Hab-15` | 2 | 53,036 | 24,267 | 232,251 | 77,303 | **38,651.5** | 8 | 2 | **131.0s** |
| **Shard Author shard_08** | `Hab-16, Hab-17` | 2 | 142,719 | 53,773 | 965,002 | 196,492 | **98,246.0** | 20 | 7 | **2248.0s** |
| **Shard Author shard_09** | `Hab-18, Hab-19` | 2 | 197,358 | 42,190 | 811,819 | 239,548 | **119,774.0** | 21 | 6 | **2739.0s** |
| **Shard Author shard_10** | `Hab-20, Hab-21` | 2 | 98,882 | 25,136 | 304,122 | 124,018 | **62,009.0** | 11 | 2 | **2098.0s** |
| **Shard Author shard_11** | `Hab-22, Hab-23` | 2 | 187,145 | 46,978 | 775,607 | 234,123 | **117,061.5** | 19 | 6 | **2206.0s** |
| **Shard Author shard_12** | `Hab-24, Hab-25` | 2 | 223,190 | 56,136 | 1,084,753 | 279,326 | **139,663.0** | 22 | 8 | **2779.0s** |
| **Shard Author shard_14 🛑** | `C-04, C-05, C-06` | 3 | 282,118 | 57,581 | 3,142,199 | 339,699 | **113,233.0** | 47 | 7 | **3034.0s** |
| **Shard Author shard_15** | `C-28, C-29, C-30` | 3 | 209,833 | 42,627 | 1,014,073 | 252,460 | **84,153.3** | 23 | 7 | **2741.0s** |
| **Shard Author shard_16** | `C-01, C-02, C-03` | 3 | 213,250 | 48,891 | 1,076,418 | 262,141 | **87,380.3** | 22 | 7 | **2797.0s** |
| **Shard Author shard_17** | `C-25, C-26, C-27` | 3 | 249,332 | 64,683 | 1,761,931 | 314,015 | **104,671.7** | 30 | 8 | **2835.0s** |
| **Shard Author shard_18** | `C-31, C-32, C-33` | 3 | 149,378 | 49,916 | 1,024,675 | 199,294 | **66,431.3** | 20 | 5 | **2292.0s** |
| **Shard Author shard_19** | `C-07, C-08, C-09` | 3 | 187,232 | 77,278 | 1,845,691 | 264,510 | **88,170.0** | 28 | 10 | **2406.0s** |
| **Shard Author shard_20** | `C-10, C-11, C-12` | 3 | 225,614 | 54,532 | 1,464,359 | 280,146 | **93,382.0** | 28 | 7 | **2835.0s** |
| **Shard Author shard_21** | `C-13, C-14, C-15` | 3 | 262,363 | 77,807 | 1,448,199 | 340,170 | **113,390.0** | 24 | 9 | **2816.0s** |
| **Shard Author shard_22** | `C-17, C-22, C-23` | 3 | 197,755 | 44,791 | 1,066,866 | 242,546 | **80,848.7** | 23 | 5 | **2818.0s** |
| **Shard Author shard_23** | `C-34, C-39, C-40` | 3 | 247,145 | 58,450 | 1,775,334 | 305,595 | **101,865.0** | 31 | 9 | **2793.0s** |
| **Shard Author shard_24** | `C-41, C-42` | 2 | 141,478 | 42,440 | 1,030,576 | 183,918 | **91,959.0** | 22 | 7 | **2258.0s** |
| **Shard Author shard_13** | `Hab-26` | 1 | 39,131 | 14,421 | 145,368 | 53,552 | **53,552.0** | 7 | 1 | **84.0s** |

---

### 3.3b. Stage 3B: Remediación y Repair Engineers (Ingenieros de Reparación)
- **Total de Repair Engineers Desplegados:** `39 subagentes`
- **Duración Mínima:** `11.0s` | **Mediana:** `44.0s` | **Máxima:** `2312.0s` (`38.5 min`)
- **Tokens Activos Totales en Reparación:** `4,112,518 tokens`
- **Agente Determinante del Retraso:** `Repair Engineer Batch B`

| Repair Engineer | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Errores | Duración |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **CTA Architect part_02 repair** | 6 | 21,103 | 1,654 | 39,324 | 22,757 | 2 | **23.0s** |
| **CTA Architect part_02 repair** | 8 | 25,750 | 936 | 55,397 | 26,686 | 1 | **28.0s** |
| **Repair Engineer (C08)** | 24 | 162,336 | 58,279 | 2,120,999 | 220,615 | 6 | **529.0s** |
| **Repair Engineer shard_16** | 6 | 36,243 | 3,868 | 114,873 | 40,111 | 0 | **33.0s** |
| **Repair Engineer shard_20** | 6 | 55,387 | 8,832 | 185,699 | 64,219 | 0 | **60.0s** |
| **Repair Engineer shard_17** | 21 | 135,408 | 33,857 | 1,627,498 | 169,265 | 4 | **250.0s** |
| **Repair Engineer shard_24** | 6 | 32,133 | 3,007 | 97,628 | 35,140 | 0 | **37.0s** |
| **Repair Engineer shard_03** | 6 | 29,955 | 5,002 | 87,118 | 34,957 | 0 | **35.0s** |
| **Repair Engineer shard_04** | 6 | 37,946 | 4,565 | 116,743 | 42,511 | 0 | **41.0s** |
| **Repair Engineer shard_09** | 6 | 33,490 | 3,711 | 101,410 | 37,201 | 0 | **33.0s** |
| **Repair Engineer shard_10** | 6 | 31,645 | 3,132 | 95,330 | 34,777 | 0 | **30.0s** |
| **Repair Engineer shard_11** | 6 | 33,360 | 4,557 | 99,267 | 37,917 | 0 | **34.0s** |
| **Repair Engineer shard_12** | 6 | 35,013 | 3,644 | 115,877 | 38,657 | 0 | **34.0s** |
| **Repair Engineer (HAB07)** | 6 | 34,604 | 4,541 | 112,448 | 39,145 | 0 | **34.0s** |
| **Repair Engineer (C33)** | 6 | 39,292 | 3,718 | 127,468 | 43,010 | 0 | **33.0s** |
| **Repair Engineer shard_01** | 4 | 72,490 | 12,065 | 119,129 | 84,555 | 1 | **65.0s** |
| **Repair Engineer shard_02** | 4 | 37,111 | 11,396 | 57,613 | 48,507 | 1 | **71.0s** |
| **Repair Engineer shard_03** | 5 | 42,050 | 9,573 | 106,018 | 51,623 | 1 | **57.0s** |
| **Repair Engineer shard_05** | 6 | 42,594 | 10,416 | 144,014 | 53,010 | 0 | **58.0s** |
| **Repair Engineer shard_06** | 4 | 63,177 | 13,735 | 103,667 | 76,912 | 0 | **59.0s** |
| **Repair Engineer shard_07** | 4 | 35,247 | 8,812 | 63,427 | 44,059 | 0 | **55.0s** |
| **Repair Engineer shard_10** | 6 | 42,884 | 7,404 | 142,054 | 50,288 | 0 | **52.0s** |
| **Repair Engineer shard_12** | 3 | 52,742 | 11,081 | 49,938 | 63,823 | 0 | **52.0s** |
| **Repair Engineer shard_13** | 5 | 40,790 | 8,915 | 104,274 | 49,705 | 0 | **44.0s** |
| **Repair Engineer shard_14** | 2 | 28,943 | 11,764 | 8,533 | 40,707 | 0 | **44.0s** |
| **Repair Engineer shard_15** | 2 | 33,662 | 13,310 | 8,560 | 46,972 | 0 | **47.0s** |
| **Repair Engineer shard_16** | 3 | 38,408 | 12,451 | 42,231 | 50,859 | 0 | **51.0s** |
| **Repair Engineer shard_17** | 2 | 54,697 | 18,961 | 8,587 | 73,658 | 0 | **65.0s** |
| **Repair Engineer shard_18** | 2 | 46,203 | 11,230 | 8,579 | 57,433 | 0 | **41.0s** |
| **Repair Engineer shard_19** | 3 | 44,799 | 20,372 | 45,474 | 65,171 | 0 | **74.0s** |
| **Repair Engineer shard_20** | 2 | 40,424 | 10,499 | 8,570 | 50,923 | 0 | **39.0s** |
| **Repair Engineer shard_21** | 3 | 43,082 | 5,535 | 46,497 | 48,617 | 0 | **42.0s** |
| **Repair Engineer shard_22** | 2 | 40,066 | 7,755 | 8,557 | 47,821 | 0 | **28.0s** |
| **Repair Engineer shard_23** | 2 | 41,015 | 6,982 | 8,559 | 47,997 | 0 | **33.0s** |
| **Repair Engineer shard_24** | 4 | 28,799 | 4,040 | 56,089 | 32,839 | 0 | **31.0s** |
| **Repair Engineer (HAB04)** | 27 | 258,359 | 76,932 | 4,241,438 | 335,291 | 9 | **1765.0s** |
| **Repair Engineer Batch B** | 27 | 640,137 | 118,155 | 3,289,737 | 758,292 | 6 | **2312.0s** |
| **Repair Engineer Batch C** | 19 | 948,119 | 85,581 | 1,825,766 | 1,033,700 | 12 | **1973.0s** |
| **Repair Engineer shard_12** | 3 | 12,622 | 166 | 11,934 | 12,788 | 0 | **11.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ⚠️ NO PASÓ AL PRIMER INTENTO — APROBADO POST-REJUDGE (120/120 REACTIVOS)  
> La Ronda 1 de Blind Judges registró 0 discrepancia(s), por lo que no hubo acuerdo limpio al primer intento. Tras correcciones y Rejudge, el resultado final alcanzó 100.0% de acuerdo (0 discrepancias).

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `120 reactivos` (57 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `31 jueces` | Aislamiento epistémico en Stage 5 |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | Ronda 1: 0 discrepancia(s); 0 violaciones iniciales |
| **Resultado Final Post-Rejudge** | **`✅ Aprobado`** | `100.0%` acuerdo, `0` discrepancia(s) |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | 0 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Ronda 1 (`judge_report_round_1.json` / `rounds_history`)**: 0 discrepancia(s) detectada(s).
- 2. **Bucle de Auto-Reparación / Rejudge**: 1 iteración(es) ejecutada(s) (0 intervenciones de supervisor).
- 3. **Resultado Final Post-Rejudge (`judge_report.json`)**: ✅ Aprobado (`100.0% agreement rate`, `0 discrepancias` sobre 120 reactivos).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared del Orquestador:** `124.53 min` (`7472.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `8.7 min` (`522.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `1.9 min` (`113.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `10.1 min` (`608.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_14
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_14 tardó 3034.0s frente a la mediana de 2739.0s (+295.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

### 🛑 [HIGH] Antipatrón de Micro-Bucle Interactivo (47 turnos en Shard Author shard_14)
- **Ámbito:** `Shard Author shard_14`
- **Diagnóstico:** 4 subagentes realizaron > 30 turnos individuales (ej. Shard Author shard_14 con 47 turnos). Ocurre por bucles de depuración o escritura incremental en lugar de redactar por lotes atómicos.

### ⚠️ [MEDIUM] Fricción de Herramientas en 24 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_01 acumularon fallos en consola (9 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `412 turnos`
- **Volumen Total de Razonamiento:** `1,203,053 caracteres`
- **Razonamiento del Orquestador:** `75 turnos` (27,984 chars)
- **Razonamiento de Subagentes:** `337 turnos` (1,175,069 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect part_06** | 2 | 4,484 | 0 |
| **Cognitive Task Analysis Architect part_03** | 2 | 2,646 | 0 |
| **Cognitive Task Analysis Architect part_04** | 2 | 5,334 | 0 |
| **Cognitive Task Analysis Architect part_01** | 2 | 3,324 | 0 |
| **Cognitive Task Analysis Architect part_05** | 2 | 4,177 | 0 |
| **Cognitive Task Analysis Architect part_08** | 1 | 2,613 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_07** | 2 | 2,129 | 0 |
| **Cognitive Task Analysis Architect part_02** | 3 | 6,638 | 0 |
| **CTA Harmonizer** | 3 | 12,021 | ⚠️ 1 |
| **CTA Architect part_02 repair** | 2 | 552 | ⚠️ 1 |
| **CTA Architect part_02 repair** | 1 | 229 | 0 |
| **Shard Author shard_01** | 11 | 40,788 | ⚠️ 9 |
| **Shard Author shard_02** | 5 | 21,925 | ⚠️ 4 |
| **Shard Author shard_03** | 12 | 31,210 | ⚠️ 8 |
| **Shard Author shard_04** | 11 | 34,855 | ⚠️ 8 |
| **Shard Author shard_05** | 2 | 10,753 | ⚠️ 1 |
| **Shard Author shard_06** | 2 | 11,570 | ⚠️ 1 |
| **Shard Author shard_07** | 4 | 18,287 | ⚠️ 2 |
| **Shard Author shard_08** | 10 | 38,518 | ⚠️ 7 |
| **Shard Author shard_09** | 8 | 30,474 | ⚠️ 6 |
| **Shard Author shard_10** | 6 | 14,830 | ⚠️ 2 |
| **Shard Author shard_11** | 9 | 29,712 | ⚠️ 6 |
| **Shard Author shard_12** | 9 | 35,082 | ⚠️ 8 |
| **Shard Author shard_14** | 13 | 35,910 | ⚠️ 7 |
| **Shard Author shard_15** | 8 | 26,609 | ⚠️ 7 |
| **Shard Author shard_16** | 9 | 30,524 | ⚠️ 7 |
| **Shard Author shard_17** | 11 | 39,290 | ⚠️ 8 |
| **Shard Author shard_18** | 7 | 34,064 | ⚠️ 5 |
| **Shard Author shard_19** | 13 | 48,520 | ⚠️ 10 |
| **Shard Author shard_20** | 10 | 36,448 | ⚠️ 7 |
| **Shard Author shard_21** | 10 | 52,456 | ⚠️ 9 |
| **Shard Author shard_22** | 7 | 24,842 | ⚠️ 5 |
| **Shard Author shard_23** | 12 | 32,896 | ⚠️ 9 |
| **Shard Author shard_24** | 10 | 22,228 | ⚠️ 7 |
| **Shard Author shard_13** | 2 | 10,994 | ⚠️ 1 |
| **Repair Engineer (C08)** | 12 | 51,436 | ⚠️ 6 |
| **Blind Judge 01** | 1 | 5,984 | 0 |
| **Blind Judge 02** | 1 | 5,814 | 0 |
| **Blind Judge 03** | 1 | 4,788 | 0 |
| **Blind Judge 04** | 1 | 5,336 | 0 |
| **Blind Judge 05** | 1 | 8,454 | 0 |
| **Blind Judge 06** | 1 | 7,530 | 0 |
| **Blind Judge 07** | 1 | 14,061 | 0 |
| **Blind Judge 08** | 1 | 5,856 | 0 |
| **Blind Judge 09** | 1 | 7,820 | 0 |
| **Blind Judge 10** | 1 | 5,458 | 0 |
| **Repair Engineer shard_16** | 2 | 2,115 | 0 |
| **Repair Engineer shard_20** | 3 | 4,900 | 0 |
| **Repair Engineer shard_17** | 11 | 29,964 | ⚠️ 4 |
| **Repair Engineer shard_24** | 1 | 1,620 | 0 |
| **Repair Engineer shard_03** | 2 | 3,177 | 0 |
| **Repair Engineer shard_04** | 5 | 3,908 | 0 |
| **Repair Engineer shard_09** | 3 | 2,438 | 0 |
| **Repair Engineer shard_10** | 1 | 1,286 | 0 |
| **Repair Engineer shard_11** | 1 | 2,870 | 0 |
| **Repair Engineer shard_12** | 3 | 2,170 | 0 |
| **Repair Engineer (HAB07)** | 5 | 3,684 | 0 |
| **Blind Judge 01** | 1 | 6,649 | 0 |
| **Blind Judge 02** | 1 | 4,185 | 0 |
| **Blind Judge 03** | 1 | 6,292 | 0 |
| **Blind Judge 04** | 1 | 4,389 | 0 |
| **Blind Judge 05** | 1 | 6,461 | 0 |
| **Blind Judge 06** | 1 | 5,295 | 0 |
| **Blind Judge 07** | 1 | 6,451 | 0 |
| **Blind Judge 08** | 1 | 3,374 | 0 |
| **Blind Judge 09** | 1 | 5,475 | 0 |
| **Blind Judge 10** | 1 | 5,993 | 0 |
| **Blind Judge 01** | 1 | 7,586 | 0 |
| **Blind Judge 02** | 1 | 6,299 | 0 |
| **Blind Judge 03** | 1 | 4,396 | 0 |
| **Blind Judge 04** | 1 | 4,556 | 0 |
| **Blind Judge 05** | 1 | 5,959 | 0 |
| **Blind Judge 06** | 1 | 5,808 | 0 |
| **Blind Judge 07** | 1 | 3,984 | 0 |
| **Blind Judge 08** | 1 | 5,390 | 0 |
| **Blind Judge 09** | 1 | 7,947 | 0 |
| **Blind Judge 10** | 1 | 6,296 | 0 |
| **Repair Engineer (C33)** | 2 | 1,773 | 0 |
| **Blind Judge 01** | 1 | 2,908 | 0 |
| **Repair Engineer shard_01** | 1 | 7,387 | 0 |
| **Repair Engineer shard_02** | 1 | 3,959 | 0 |
| **Repair Engineer shard_03** | 2 | 4,466 | ⚠️ 1 |
| **Repair Engineer shard_05** | 2 | 6,818 | 0 |
| **Repair Engineer shard_06** | 3 | 5,276 | 0 |
| **Repair Engineer shard_07** | 2 | 5,916 | 0 |
| **Repair Engineer shard_10** | 3 | 4,033 | 0 |
| **Repair Engineer shard_12** | 1 | 3,140 | 0 |
| **Repair Engineer shard_13** | 2 | 3,043 | 0 |
| **Repair Engineer shard_14** | 1 | 6,379 | 0 |
| **Repair Engineer shard_15** | 1 | 9,197 | 0 |
| **Repair Engineer shard_16** | 1 | 10,407 | 0 |
| **Repair Engineer shard_17** | 1 | 7,321 | 0 |
| **Repair Engineer shard_18** | 1 | 4,712 | 0 |
| **Repair Engineer shard_19** | 2 | 8,789 | 0 |
| **Repair Engineer shard_20** | 2 | 8,081 | 0 |
| **Repair Engineer shard_21** | 1 | 4,729 | 0 |
| **Repair Engineer shard_22** | 1 | 5,472 | 0 |
| **Repair Engineer shard_23** | 2 | 8,358 | 0 |
| **Repair Engineer shard_24** | 2 | 2,519 | 0 |
| **Repair Engineer (HAB04)** | 0 | 0 | 0 |
| **Repair Engineer Batch B** | 0 | 0 | 0 |
| **Repair Engineer Batch C** | 0 | 0 | 0 |
| **Repair Engineer shard_12** | 0 | 0 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*