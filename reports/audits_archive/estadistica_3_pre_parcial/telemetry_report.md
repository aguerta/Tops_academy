# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Estadistica 3 Pre Parcial (`estadistica_3_pre_parcial`)

**Fecha de Auditoría:** `2026-10-26 05:26:37 UTC`  
**Conversación Orquestadora:** [`821334d0-216d-40c5-8920-dca90c0f0b26`](conversation://821334d0-216d-40c5-8920-dca90c0f0b26)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_parcial\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `8 archivos` (141 págs / 6.19 MB) | EST3_LEC01_26_2.pdf, EST3_LEC02_26_2.pdf, EST3_LEC03_26_2.pdf, EST3_LEC04_26_2.pdf, EST3_LEC05_26_2.pdf, Nota_academica_Econometria.pdf, Stats3 10-10.pdf, stats 3 3-10.png |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`93 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`63 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`87 subagentes`** | Visión (0), CTA (8), Autores (63), Jueces (16) |
| **Reactivos Finales Validados** | **`2190 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`8,587,302` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`3,141,412` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`38,536,687` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`12,061,356` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`50,598,043` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`23,104.1 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`5,507.5 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`544,065.0 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`100,067.3 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`358,851.4 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`0.74 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`81.36 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`16.37x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `821334d0`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-10-26 04:58:20` | `0.91s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-10-26 04:58:20` | `0.94s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_parcial\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-10-26 05:06:40` | `0.89s` | `3,067,245` (`1,284,900` act) | 8 | `competencies=93` |
| **`02_shard`** | `2026-10-26 05:06:45` | `0.1s` | `0` (`0` act) | 0 | `shards=63` |
| **`03_templates`** | `2026-10-26 05:20:08` | `128.83s` | `37,622,880` (`9,306,263` act) | 63 | `count=93` |
| **`04_build`** | `2026-10-26 05:20:38` | `22.34s` | `0` (`0` act) | 0 | `total_questions=2190` |
| **`05_verify`** | `2026-10-26 05:21:13` | `21.66s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_parcial\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-10-26 05:24:31` | `0.2s` | `2,228,972` (`1,134,916` act) | 16 | `passed=True` |
| **`06_publish`** | `2026-10-26 05:24:46` | `9.09s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_parcial.json` |

---

### 3.1. Stage 1A: Preprocesamiento de Visión
- **Subagentes de Visión Desplegados:** `0 agentes en paralelo`
- **Tiempo de Pared de la Etapa (Máximo / Critical Path):** **`0.0s`** (`0.0 min`)
- **Agente Determinante del Camino Crítico:** `N/A`

| Subagente de Visión | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

---

### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)
- **Arquitectura:** `MAPREDUCE (8 Mappers)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`445.0s`** (determinado por `Cognitive Task Analysis Architect part_05`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`0.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`445.0s`** (`7.4 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cognitive Task Analysis Architect part_03** | Mapper | 11 | 126,807 | 54,741 | 308,431 | 2 | **396.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 9 | 119,958 | 53,512 | 259,887 | 1 | **340.0s** |
| **Cognitive Task Analysis Architect part_06** | Mapper | 9 | 118,528 | 35,880 | 200,263 | 1 | **268.0s** |
| **Cognitive Task Analysis Architect part_05** | Mapper | 11 | 129,153 | 62,720 | 308,112 | 1 | **445.0s** |
| **Cognitive Task Analysis Architect part_04** | Mapper | 8 | 101,171 | 42,679 | 198,151 | 1 | **331.0s** |
| **Cognitive Task Analysis Architect part_01** | Mapper | 7 | 94,055 | 37,823 | 168,736 | 0 | **256.0s** |
| **Cognitive Task Analysis Architect part_07** | Mapper | 11 | 102,703 | 42,085 | 268,536 | 3 | **397.0s** |
| **Cognitive Task Analysis Architect part_08** | Mapper | 10 | 134,725 | 30,995 | 161,628 | 2 | **269.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `63 shards concurrentes`
- **Duración Mínima de Shard:** `221.0s` | **Mediana:** `310.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`599.0s`** (`10.0 min`) por `Shard Author shard_54`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+289.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`100,067.3 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_34** | `C-04, C-05` | 2 | 95,545 | 36,083 | 370,922 | 131,628 | **65,814.0** | 10 | 3 | **291.0s** |
| **Shard Author shard_35** | `C-08, C-09` | 2 | 98,706 | 44,697 | 348,353 | 143,403 | **71,701.5** | 12 | 1 | **351.0s** |
| **Shard Author shard_36** | `C-14, C-15` | 2 | 90,571 | 41,919 | 292,011 | 132,490 | **66,245.0** | 11 | 4 | **385.0s** |
| **Shard Author shard_37** | `C-20, C-21` | 2 | 92,811 | 34,619 | 279,500 | 127,430 | **63,715.0** | 8 | 2 | **254.0s** |
| **Shard Author shard_38** | `C-31, C-32` | 2 | 121,503 | 43,009 | 691,139 | 164,512 | **82,256.0** | 22 | 5 | **351.0s** |
| **Shard Author shard_39** | `C-35, C-36` | 2 | 140,073 | 36,445 | 146,668 | 176,518 | **88,259.0** | 8 | 2 | **274.0s** |
| **Shard Author shard_40** | `H-01, C-01` | 2 | 90,745 | 48,503 | 225,218 | 139,248 | **69,624.0** | 8 | 2 | **348.0s** |
| **Shard Author shard_41** | `H-02, C-02` | 2 | 85,696 | 39,262 | 238,625 | 124,958 | **62,479.0** | 9 | 2 | **269.0s** |
| **Shard Author shard_42** | `C-03, H-03` | 2 | 121,786 | 54,842 | 917,129 | 176,628 | **88,314.0** | 20 | 3 | **464.0s** |
| **Shard Author shard_43** | `C-06, H-04` | 2 | 97,255 | 42,742 | 200,805 | 139,997 | **69,998.5** | 8 | 2 | **284.0s** |
| **Shard Author shard_44** | `H-05, C-07` | 2 | 76,602 | 35,600 | 198,731 | 112,202 | **56,101.0** | 8 | 2 | **285.0s** |
| **Shard Author shard_45** | `C-10, H-06` | 2 | 89,498 | 43,285 | 309,121 | 132,783 | **66,391.5** | 11 | 2 | **326.0s** |
| **Shard Author shard_46** | `H-07, C-11` | 2 | 165,079 | 52,498 | 1,137,850 | 217,577 | **108,788.5** | 17 | 3 | **417.0s** |
| **Shard Author shard_47** | `H-08, C-12` | 2 | 97,222 | 34,980 | 373,132 | 132,202 | **66,101.0** | 12 | 4 | **260.0s** |
| **Shard Author shard_48** | `C-13, H-09` | 2 | 116,980 | 42,300 | 738,864 | 159,280 | **79,640.0** | 22 | 5 | **362.0s** |
| **Shard Author shard_49** | `H-10, C-16` | 2 | 86,801 | 39,814 | 272,081 | 126,615 | **63,307.5** | 10 | 3 | **310.0s** |
| **Shard Author shard_50** | `H-11, C-17` | 2 | 166,087 | 41,106 | 583,370 | 207,193 | **103,596.5** | 20 | 4 | **369.0s** |
| **Shard Author shard_51** | `C-18, H-12` | 2 | 107,200 | 39,828 | 533,852 | 147,028 | **73,514.0** | 16 | 4 | **319.0s** |
| **Shard Author shard_52** | `C-19, H-13` | 2 | 109,503 | 50,250 | 651,872 | 159,753 | **79,876.5** | 15 | 4 | **366.0s** |
| **Shard Author shard_53** | `H-14, C-22` | 2 | 119,294 | 50,191 | 834,898 | 169,485 | **84,742.5** | 21 | 5 | **391.0s** |
| **Shard Author shard_54 🛑** | `C-23, H-15` | 2 | 331,860 | 75,864 | 1,711,142 | 407,724 | **203,862.0** | 25 | 6 | **599.0s** |
| **Shard Author shard_55** | `C-24, H-16` | 2 | 118,130 | 42,017 | 510,238 | 160,147 | **80,073.5** | 14 | 4 | **373.0s** |
| **Shard Author shard_56** | `H-17, C-25` | 2 | 125,382 | 51,470 | 515,774 | 176,852 | **88,426.0** | 13 | 4 | **433.0s** |
| **Shard Author shard_57** | `C-26, H-18` | 2 | 171,679 | 49,869 | 424,752 | 221,548 | **110,774.0** | 13 | 4 | **364.0s** |
| **Shard Author shard_58** | `H-19, C-27` | 2 | 94,454 | 32,920 | 490,920 | 127,374 | **63,687.0** | 15 | 3 | **248.0s** |
| **Shard Author shard_59** | `H-20, C-28` | 2 | 84,565 | 40,342 | 256,974 | 124,907 | **62,453.5** | 10 | 3 | **321.0s** |
| **Shard Author shard_60** | `C-29, H-21` | 2 | 101,303 | 50,047 | 487,022 | 151,350 | **75,675.0** | 12 | 3 | **371.0s** |
| **Shard Author shard_61** | `H-22, C-30` | 2 | 123,770 | 61,016 | 725,641 | 184,786 | **92,393.0** | 17 | 3 | **477.0s** |
| **Shard Author shard_62** | `C-33, H-23` | 2 | 131,269 | 35,951 | 288,648 | 167,220 | **83,610.0** | 9 | 3 | **292.0s** |
| **Shard Author shard_63** | `C-34, H-24` | 2 | 96,239 | 31,440 | 607,449 | 127,679 | **63,839.5** | 18 | 3 | **286.0s** |
| **Shard Author shard_01** | `Hab-01` | 1 | 169,097 | 27,798 | 394,868 | 196,895 | **196,895.0** | 12 | 3 | **269.0s** |
| **Shard Author shard_02** | `Hab-02` | 1 | 84,845 | 42,482 | 195,032 | 127,327 | **127,327.0** | 8 | 2 | **310.0s** |
| **Shard Author shard_03** | `Hab-03` | 1 | 74,805 | 30,384 | 191,261 | 105,189 | **105,189.0** | 9 | 3 | **252.0s** |
| **Shard Author shard_04** | `Hab-04` | 1 | 91,192 | 32,662 | 294,243 | 123,854 | **123,854.0** | 9 | 3 | **252.0s** |
| **Shard Author shard_05** | `Hab-05` | 1 | 102,580 | 44,757 | 393,565 | 147,337 | **147,337.0** | 10 | 3 | **345.0s** |
| **Shard Author shard_06** | `Hab-06` | 1 | 101,575 | 42,108 | 520,163 | 143,683 | **143,683.0** | 15 | 4 | **348.0s** |
| **Shard Author shard_07** | `Hab-07` | 1 | 68,621 | 34,618 | 186,052 | 103,239 | **103,239.0** | 8 | 2 | **273.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 84,134 | 39,647 | 275,879 | 123,781 | **123,781.0** | 10 | 3 | **347.0s** |
| **Shard Author shard_09** | `Hab-09` | 1 | 92,752 | 33,895 | 450,950 | 126,647 | **126,647.0** | 15 | 3 | **288.0s** |
| **Shard Author shard_10** | `Hab-10` | 1 | 108,579 | 36,109 | 444,879 | 144,688 | **144,688.0** | 14 | 4 | **267.0s** |
| **Shard Author shard_11** | `Hab-11` | 1 | 86,129 | 29,170 | 288,893 | 115,299 | **115,299.0** | 9 | 3 | **263.0s** |
| **Shard Author shard_12** | `Hab-12` | 1 | 82,545 | 41,195 | 196,812 | 123,740 | **123,740.0** | 8 | 2 | **297.0s** |
| **Shard Author shard_13** | `Hab-13` | 1 | 91,610 | 32,044 | 399,150 | 123,654 | **123,654.0** | 14 | 4 | **246.0s** |
| **Shard Author shard_14** | `Hab-14` | 1 | 86,548 | 45,735 | 202,655 | 132,283 | **132,283.0** | 8 | 2 | **355.0s** |
| **Shard Author shard_15** | `Hab-15` | 1 | 75,033 | 33,186 | 173,528 | 108,219 | **108,219.0** | 8 | 2 | **256.0s** |
| **Shard Author shard_16** | `Hab-16` | 1 | 113,273 | 38,819 | 711,676 | 152,092 | **152,092.0** | 19 | 4 | **287.0s** |
| **Shard Author shard_17** | `Hab-17` | 1 | 90,700 | 42,203 | 363,890 | 132,903 | **132,903.0** | 12 | 3 | **344.0s** |
| **Shard Author shard_18** | `Hab-18` | 1 | 136,989 | 51,159 | 1,340,719 | 188,148 | **188,148.0** | 26 | 6 | **465.0s** |
| **Shard Author shard_19** | `Hab-19` | 1 | 96,812 | 38,677 | 492,209 | 135,489 | **135,489.0** | 16 | 4 | **356.0s** |
| **Shard Author shard_20** | `Hab-20` | 1 | 91,145 | 33,151 | 290,688 | 124,296 | **124,296.0** | 9 | 3 | **221.0s** |
| **Shard Author shard_21** | `Hab-21` | 1 | 77,372 | 36,502 | 184,133 | 113,874 | **113,874.0** | 8 | 2 | **292.0s** |
| **Shard Author shard_22** | `Hab-22` | 1 | 94,624 | 36,178 | 394,724 | 130,802 | **130,802.0** | 13 | 3 | **296.0s** |
| **Shard Author shard_23** | `Hab-23` | 1 | 77,558 | 34,653 | 258,204 | 112,211 | **112,211.0** | 10 | 3 | **287.0s** |
| **Shard Author shard_24** | `Hab-24` | 1 | 69,903 | 29,654 | 212,746 | 99,557 | **99,557.0** | 9 | 2 | **227.0s** |
| **Shard Author shard_25** | `Hab-25` | 1 | 75,830 | 31,360 | 201,152 | 107,190 | **107,190.0** | 9 | 2 | **265.0s** |
| **Shard Author shard_26** | `Hab-26` | 1 | 95,608 | 30,080 | 421,201 | 125,688 | **125,688.0** | 15 | 4 | **282.0s** |
| **Shard Author shard_27** | `Hab-27` | 1 | 85,001 | 32,899 | 335,774 | 117,900 | **117,900.0** | 14 | 4 | **254.0s** |
| **Shard Author shard_28** | `Hab-28` | 1 | 90,085 | 36,829 | 332,997 | 126,914 | **126,914.0** | 13 | 3 | **358.0s** |
| **Shard Author shard_29** | `Hab-29` | 1 | 81,763 | 29,454 | 313,358 | 111,217 | **111,217.0** | 12 | 2 | **259.0s** |
| **Shard Author shard_30** | `Hab-30` | 1 | 90,682 | 44,114 | 303,883 | 134,796 | **134,796.0** | 10 | 2 | **362.0s** |
| **Shard Author shard_31** | `Hab-31` | 1 | 189,079 | 71,202 | 1,234,505 | 260,281 | **260,281.0** | 23 | 3 | **574.0s** |
| **Shard Author shard_32** | `Hab-32` | 1 | 117,570 | 39,344 | 687,964 | 156,914 | **156,914.0** | 18 | 4 | **373.0s** |
| **Shard Author shard_33** | `Hab-33` | 1 | 131,356 | 28,283 | 266,163 | 159,639 | **159,639.0** | 13 | 3 | **242.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ✅ 100% ACUERDO AL PRIMER INTENTO (186/186 REACTIVOS)  
> Los 16 Blind Judges evaluaron el lote estratificado de 186 reactivos en 1 turno de razonamiento puro cada uno (0 búsquedas web, 100% aislamiento epistémico), logrando un acuerdo psicométrico del 100.0% (186/186) con 0 discrepancias frente al ground truth.

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `186 reactivos` (93 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `16 jueces` | Aislamiento epistémico en Stage 5 |
| **Resultado al Primer Intento** | **`✅ 100% Limpio (Sin Discrepancias)`** | Sin discrepancias ni arbitraje necesario |
| **Iteraciones de Auto-Reparación** | `2 iteraciones` en sandbox | 0 requeridas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Arbitraje Ciego (`05b_judge_compare.json`)**: 186/186 acuerdos (`100.0% agreement rate`, `0 discrepancias`).
- 2. **Verificación Determinista Previa (`--stage verify`)**: Detectó 2 error(es) léxico/estructural(es) corregido(s) antes del arbitraje ciego.

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared del Orquestador:** `26.92 min` (`1615.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `1.1 min` (`66.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `0.7 min` (`44.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `0.8 min` (`51.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_54
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_54 tardó 599.0s frente a la mediana de 310.0s (+289.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

### ⚠️ [MEDIUM] Fricción de Herramientas en 46 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Cognitive Task Analysis Architect part_07 acumularon fallos en consola (3 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `584 turnos`
- **Volumen Total de Razonamiento:** `2,322,607 caracteres`
- **Razonamiento del Orquestador:** `14 turnos` (5,327 chars)
- **Razonamiento de Subagentes:** `570 turnos` (2,317,280 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect part_03** | 9 | 38,786 | ⚠️ 2 |
| **Cognitive Task Analysis Architect part_02** | 6 | 32,966 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_06** | 5 | 23,896 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_05** | 7 | 40,069 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_04** | 5 | 33,307 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_01** | 5 | 23,510 | 0 |
| **Cognitive Task Analysis Architect part_07** | 8 | 38,282 | ⚠️ 3 |
| **Cognitive Task Analysis Architect part_08** | 7 | 39,939 | ⚠️ 2 |
| **Shard Author shard_34** | 6 | 25,872 | ⚠️ 3 |
| **Shard Author shard_35** | 7 | 35,011 | ⚠️ 1 |
| **Shard Author shard_36** | 7 | 30,610 | ⚠️ 4 |
| **Shard Author shard_37** | 5 | 31,743 | ⚠️ 2 |
| **Shard Author shard_38** | 9 | 28,840 | ⚠️ 5 |
| **Shard Author shard_39** | 5 | 24,715 | ⚠️ 2 |
| **Shard Author shard_40** | 6 | 40,631 | ⚠️ 2 |
| **Shard Author shard_41** | 6 | 31,112 | ⚠️ 2 |
| **Shard Author shard_42** | 12 | 40,632 | ⚠️ 3 |
| **Shard Author shard_43** | 5 | 29,616 | ⚠️ 2 |
| **Shard Author shard_44** | 7 | 24,015 | ⚠️ 2 |
| **Shard Author shard_45** | 9 | 32,393 | ⚠️ 2 |
| **Shard Author shard_46** | 12 | 38,836 | ⚠️ 3 |
| **Shard Author shard_47** | 8 | 28,362 | ⚠️ 4 |
| **Shard Author shard_48** | 9 | 33,518 | ⚠️ 5 |
| **Shard Author shard_49** | 5 | 29,332 | ⚠️ 3 |
| **Shard Author shard_50** | 12 | 26,128 | ⚠️ 4 |
| **Shard Author shard_51** | 6 | 27,085 | ⚠️ 4 |
| **Shard Author shard_52** | 9 | 37,785 | ⚠️ 4 |
| **Shard Author shard_53** | 10 | 33,205 | ⚠️ 5 |
| **Shard Author shard_54** | 13 | 47,943 | ⚠️ 6 |
| **Shard Author shard_55** | 7 | 29,321 | ⚠️ 4 |
| **Shard Author shard_56** | 8 | 41,436 | ⚠️ 4 |
| **Shard Author shard_57** | 9 | 33,979 | ⚠️ 4 |
| **Shard Author shard_58** | 10 | 22,387 | ⚠️ 3 |
| **Shard Author shard_59** | 7 | 32,401 | ⚠️ 3 |
| **Shard Author shard_60** | 10 | 32,431 | ⚠️ 3 |
| **Shard Author shard_61** | 10 | 38,543 | ⚠️ 3 |
| **Shard Author shard_62** | 7 | 24,239 | ⚠️ 3 |
| **Shard Author shard_63** | 8 | 19,922 | ⚠️ 3 |
| **Shard Author shard_01** | 8 | 17,710 | ⚠️ 3 |
| **Shard Author shard_02** | 4 | 30,655 | ⚠️ 2 |
| **Shard Author shard_03** | 5 | 24,882 | ⚠️ 3 |
| **Shard Author shard_04** | 6 | 21,719 | ⚠️ 3 |
| **Shard Author shard_05** | 9 | 37,858 | ⚠️ 3 |
| **Shard Author shard_06** | 8 | 29,315 | ⚠️ 4 |
| **Shard Author shard_07** | 5 | 26,018 | ⚠️ 2 |
| **Shard Author shard_08** | 7 | 35,147 | ⚠️ 3 |
| **Shard Author shard_09** | 9 | 24,677 | ⚠️ 3 |
| **Shard Author shard_10** | 10 | 24,473 | ⚠️ 4 |
| **Shard Author shard_11** | 6 | 19,856 | ⚠️ 3 |
| **Shard Author shard_12** | 5 | 35,337 | ⚠️ 2 |
| **Shard Author shard_13** | 6 | 20,193 | ⚠️ 4 |
| **Shard Author shard_14** | 5 | 39,220 | ⚠️ 2 |
| **Shard Author shard_15** | 4 | 22,895 | ⚠️ 2 |
| **Shard Author shard_16** | 11 | 29,763 | ⚠️ 4 |
| **Shard Author shard_17** | 6 | 33,141 | ⚠️ 3 |
| **Shard Author shard_18** | 14 | 33,039 | ⚠️ 6 |
| **Shard Author shard_19** | 10 | 27,679 | ⚠️ 4 |
| **Shard Author shard_20** | 5 | 24,793 | ⚠️ 3 |
| **Shard Author shard_21** | 5 | 29,044 | ⚠️ 2 |
| **Shard Author shard_22** | 5 | 26,784 | ⚠️ 3 |
| **Shard Author shard_23** | 8 | 25,257 | ⚠️ 3 |
| **Shard Author shard_24** | 7 | 20,280 | ⚠️ 2 |
| **Shard Author shard_25** | 5 | 20,722 | ⚠️ 2 |
| **Shard Author shard_26** | 6 | 22,276 | ⚠️ 4 |
| **Shard Author shard_27** | 7 | 21,923 | ⚠️ 4 |
| **Shard Author shard_28** | 9 | 26,601 | ⚠️ 3 |
| **Shard Author shard_29** | 9 | 19,586 | ⚠️ 2 |
| **Shard Author shard_30** | 6 | 35,697 | ⚠️ 2 |
| **Shard Author shard_31** | 14 | 48,882 | ⚠️ 3 |
| **Shard Author shard_32** | 8 | 35,423 | ⚠️ 4 |
| **Shard Author shard_33** | 9 | 20,862 | ⚠️ 3 |
| **Blind Judge 01** | 2 | 7,815 | 0 |
| **Blind Judge 02** | 2 | 8,877 | 0 |
| **Blind Judge 03** | 2 | 17,768 | 0 |
| **Blind Judge 04** | 2 | 12,086 | 0 |
| **Blind Judge 05** | 2 | 8,787 | 0 |
| **Blind Judge 06** | 2 | 9,268 | 0 |
| **Blind Judge 07** | 2 | 10,148 | 0 |
| **Blind Judge 08** | 2 | 10,881 | 0 |
| **Blind Judge 09** | 2 | 7,186 | 0 |
| **Blind Judge 10** | 2 | 12,943 | 0 |
| **Blind Judge 11** | 2 | 13,599 | 0 |
| **Blind Judge 12** | 2 | 13,536 | 0 |
| **Blind Judge 13** | 2 | 18,458 | 0 |
| **Blind Judge 14** | 2 | 14,799 | 0 |
| **Blind Judge 15** | 3 | 7,165 | 0 |
| **Blind Judge 16** | 2 | 9,459 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*