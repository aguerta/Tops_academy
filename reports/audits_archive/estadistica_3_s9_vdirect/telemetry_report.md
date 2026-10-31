# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Estadistica 3 S9 Vdirect (`estadistica_3_s9_vdirect`)

**Fecha de Auditoría:** `2026-10-31 18:02:23 UTC`  
**Conversación Orquestadora:** [`592de77b-afd9-4fae-8744-4ef0be7212f4`](conversation://592de77b-afd9-4fae-8744-4ef0be7212f4)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_s9_vdirect\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `2 archivos` (80 págs / 0.93 MB) | Clases_sintetizadas_semana_9.pdf, EST3_LEC07_26.2_V2.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`27 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`18 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`24 subagentes`** | Visión (0), CTA (1), Autores (18), Jueces (5) |
| **Reactivos Finales Validados** | **`620 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`1,950,255` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`839,613` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`8,734,737` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`2,968,789` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`11,703,526` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`18,876.7 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`4,788.4 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`433,463.9 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`82,238.1 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`146,294.1 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`2.78 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`21.59 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`4.58x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `592de77b`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-10-31 17:25:54` | `0.05s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-10-31 17:25:54` | `0.12s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_s9_vdirect\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-10-31 17:44:33` | `0.13s` | `972,119` (`297,441` act) | 1 | `competencies=27` |
| **`02_shard`** | `2026-10-31 17:44:38` | `0.03s` | `0` (`0` act) | 0 | `shards=18` |
| **`03_templates`** | `2026-10-31 17:51:50` | `36.09s` | `7,673,592` (`2,220,429` act) | 18 | `count=27` |
| **`04_build`** | `2026-10-31 17:52:03` | `5.66s` | `0` (`0` act) | 0 | `total_questions=620` |
| **`05_verify`** | `2026-10-31 17:52:20` | `6.33s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_s9_vdirect\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-10-31 17:54:12` | `0.06s` | `588,938` (`269,733` act) | 5 | `passed=True` |
| **`06_publish`** | `2026-10-31 17:54:23` | `2.94s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_s9_vdirect.json` |

---

### 3.1. Stage 1A: Preprocesamiento de Visión
- **Subagentes de Visión Desplegados:** `0 agentes en paralelo`
- **Tiempo de Pared de la Etapa (Máximo / Critical Path):** **`0.0s`** (`0.0 min`)
- **Agente Determinante del Camino Crítico:** `N/A`

| Subagente de Visión | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

---

### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)
- **Arquitectura:** `DIRECT (1 Direct CTA Architect)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`0.0s`** (determinado por `Cognitive Task Analysis Architect`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`1068.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`1068.0s`** (`17.8 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cognitive Task Analysis Architect** | Direct Architect | 12 | 164,761 | 134,945 | 836,749 | 1 | **1068.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `18 shards concurrentes`
- **Duración Mínima de Shard:** `210.0s` | **Mediana:** `273.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`355.0s`** (`5.9 min`) por `Shard Author shard_11`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+82.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`82,238.1 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_01** | `Hab-01` | 1 | 67,668 | 28,541 | 227,212 | 96,209 | **96,209.0** | 11 | 2 | **214.0s** |
| **Shard Author shard_02** | `Hab-02` | 1 | 77,046 | 30,970 | 124,252 | 108,016 | **108,016.0** | 7 | 1 | **212.0s** |
| **Shard Author shard_03** | `Hab-03` | 1 | 96,668 | 35,230 | 274,694 | 131,898 | **131,898.0** | 10 | 4 | **256.0s** |
| **Shard Author shard_04** | `Hab-04` | 1 | 80,081 | 30,403 | 136,276 | 110,484 | **110,484.0** | 8 | 2 | **210.0s** |
| **Shard Author shard_05** | `Hab-05` | 1 | 72,115 | 32,325 | 239,506 | 104,440 | **104,440.0** | 11 | 3 | **273.0s** |
| **Shard Author shard_06** | `Hab-06` | 1 | 81,456 | 33,735 | 184,440 | 115,191 | **115,191.0** | 9 | 2 | **235.0s** |
| **Shard Author shard_07** | `Hab-07` | 1 | 79,011 | 29,744 | 231,277 | 108,755 | **108,755.0** | 8 | 2 | **210.0s** |
| **Shard Author shard_08** | `Hab-08` | 1 | 101,063 | 35,142 | 577,341 | 136,205 | **136,205.0** | 18 | 4 | **289.0s** |
| **Shard Author shard_09** | `C-01, C-02` | 2 | 72,720 | 34,641 | 173,310 | 107,361 | **53,680.5** | 8 | 2 | **231.0s** |
| **Shard Author shard_10** | `C-03, C-04` | 2 | 84,736 | 48,794 | 185,275 | 133,530 | **66,765.0** | 7 | 2 | **325.0s** |
| **Shard Author shard_11 🛑** | `C-05, C-06` | 2 | 121,999 | 43,132 | 859,960 | 165,131 | **82,565.5** | 21 | 5 | **355.0s** |
| **Shard Author shard_12** | `C-07, C-08` | 2 | 73,806 | 35,925 | 176,892 | 109,731 | **54,865.5** | 8 | 2 | **238.0s** |
| **Shard Author shard_13** | `H-01, H-02` | 2 | 96,707 | 45,246 | 420,813 | 141,953 | **70,976.5** | 13 | 2 | **329.0s** |
| **Shard Author shard_14** | `H-03, H-04` | 2 | 93,152 | 40,105 | 309,505 | 133,257 | **66,628.5** | 11 | 3 | **284.0s** |
| **Shard Author shard_15** | `H-05, H-06` | 2 | 77,965 | 42,438 | 170,066 | 120,403 | **60,201.5** | 7 | 1 | **290.0s** |
| **Shard Author shard_16** | `H-07, H-08` | 2 | 109,893 | 36,219 | 667,156 | 146,112 | **73,056.0** | 20 | 6 | **304.0s** |
| **Shard Author shard_17** | `H-09, H-10` | 2 | 93,799 | 42,266 | 354,902 | 136,065 | **68,032.5** | 13 | 2 | **312.0s** |
| **Shard Author shard_18** | `C-09` | 1 | 82,555 | 33,133 | 140,286 | 115,688 | **115,688.0** | 8 | 2 | **217.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ✅ 100% ACUERDO AL PRIMER INTENTO (54/54 REACTIVOS)  
> Los 5 Blind Judges evaluaron el lote estratificado de 54 reactivos en 1 turno de razonamiento puro cada uno (0 búsquedas web, 100% aislamiento epistémico), logrando un acuerdo psicométrico del 100.0% (54/54) con 0 discrepancias frente al ground truth.

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `54 reactivos` (27 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `5 jueces` | Aislamiento epistémico en Stage 5 |
| **Resultado al Primer Intento** | **`✅ 100% Limpio (Sin Discrepancias)`** | Sin discrepancias ni arbitraje necesario |
| **Iteraciones de Auto-Reparación** | `2 iteraciones` en sandbox | 0 requeridas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Arbitraje Ciego (`05b_judge_compare.json`)**: 54/54 acuerdos (`100.0% agreement rate`, `0 discrepancias`).
- 2. **Verificación Determinista Previa (`--stage verify`)**: Detectó 2 error(es) léxico/estructural(es) corregido(s) antes del arbitraje ciego.

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared del Orquestador:** `28.72 min` (`1723.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `1.1 min` (`64.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `0.7 min` (`39.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `0.6 min` (`38.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### ⚠️ [MEDIUM] Fricción de Herramientas en 6 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_03 acumularon fallos en consola (4 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `137 turnos`
- **Volumen Total de Razonamiento:** `615,081 caracteres`
- **Razonamiento del Orquestador:** `11 turnos` (3,088 chars)
- **Razonamiento de Subagentes:** `126 turnos` (611,993 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect** | 8 | 84,266 | ⚠️ 1 |
| **Shard Author shard_01** | 8 | 18,950 | ⚠️ 2 |
| **Shard Author shard_02** | 5 | 24,845 | ⚠️ 1 |
| **Shard Author shard_03** | 4 | 26,285 | ⚠️ 4 |
| **Shard Author shard_04** | 5 | 24,761 | ⚠️ 2 |
| **Shard Author shard_05** | 7 | 23,573 | ⚠️ 3 |
| **Shard Author shard_06** | 7 | 23,225 | ⚠️ 2 |
| **Shard Author shard_07** | 6 | 24,352 | ⚠️ 2 |
| **Shard Author shard_08** | 7 | 26,410 | ⚠️ 4 |
| **Shard Author shard_09** | 4 | 24,636 | ⚠️ 2 |
| **Shard Author shard_10** | 5 | 43,734 | ⚠️ 2 |
| **Shard Author shard_11** | 11 | 31,637 | ⚠️ 5 |
| **Shard Author shard_12** | 6 | 25,240 | ⚠️ 2 |
| **Shard Author shard_13** | 5 | 31,593 | ⚠️ 2 |
| **Shard Author shard_14** | 5 | 29,641 | ⚠️ 3 |
| **Shard Author shard_15** | 6 | 33,323 | ⚠️ 1 |
| **Shard Author shard_16** | 7 | 25,304 | ⚠️ 6 |
| **Shard Author shard_17** | 6 | 31,429 | ⚠️ 2 |
| **Shard Author shard_18** | 4 | 25,652 | ⚠️ 2 |
| **Blind Judge 01** | 2 | 6,106 | 0 |
| **Blind Judge 02** | 2 | 7,065 | 0 |
| **Blind Judge 03** | 2 | 10,215 | 0 |
| **Blind Judge 04** | 2 | 5,482 | 0 |
| **Blind Judge 05** | 2 | 4,269 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*