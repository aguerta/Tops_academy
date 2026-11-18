# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Estadistica 3 Pre Pc2 V7 (`estadistica_3_pre_pc2_v7`)

**Fecha de Auditoría:** `2026-11-18 23:28:59 UTC`  
**Conversación Orquestadora:** [`192cd54a-f06a-4a16-80ac-f1e7314629e4`](conversation://192cd54a-f06a-4a16-80ac-f1e7314629e4)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_pc2_v7\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `4 archivos` (129 págs / 1.88 MB) | 01_semana_9_apuntes.pdf, 02_EST3_LEC07_26.2_V2.pdf, 03_EST3_LEC08_26.2_v1.pdf, 04_semana_10_apuntes.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`53 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`22 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`49 subagentes`** | Visión (0), CTA (9), Autores (22), Repairs (6), Jueces (12) |
| **Reactivos Finales Validados** | **`1290 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`2,601,669` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`1,031,381` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`17,602,703` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`3,950,909` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`21,553,612` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`16,708.2 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`3,062.7 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`406,671.9 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`42,449.2 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`167,082.3 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`0.9 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`67.01 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`6.7x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `192cd54a`):** `9 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-11-18 22:39:18` | `0.23s` | `0` (`0` act) | 0 | `—` |
| **`00b_bootstrap`** | `2026-11-18 22:39:18` | `0.29s` | `0` (`0` act) | 0 | `lock_file=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_pc2_v7\work\.c2c_subagent_lock.json` |
| **`01_cta`** | `2026-11-18 22:42:22` | `0.5s` | `0` (`0` act) | 0 | `needs_harmonize=True` |
| **`02_shard`** | `2026-11-18 22:43:47` | `0.05s` | `0` (`0` act) | 0 | `shards=22` |
| **`03_templates`** | `2026-11-18 22:57:53` | `0.61s` | `0` (`0` act) | 0 | `count=53` |
| **`04_build`** | `2026-11-18 22:58:02` | `9.33s` | `0` (`0` act) | 0 | `total_questions=1290` |
| **`05_verify`** | `2026-11-18 22:58:04` | `2.4s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_pc2_v7\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-11-18 22:52:33` | `0.06s` | `0` (`0` act) | 0 | `passed=False` |
| **`06_publish`** | `2026-11-18 22:58:17` | `5.47s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\estadistica_3_pre_pc2_v7.json` |

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
- **Tiempo de Pared Fase Mappers (Máximo):** **`147.0s`** (determinado por `Cognitive Task Analysis Architect part_06`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`63.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`210.0s`** (`3.5 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cognitive Task Analysis Architect part_06** | Mapper | 5 | 60,766 | 29,883 | 138,438 | 1 | **147.0s** |
| **Cognitive Task Analysis Architect part_03** | Mapper | 7 | 55,397 | 21,955 | 213,750 | 2 | **131.0s** |
| **Cognitive Task Analysis Architect part_04** | Mapper | 7 | 54,842 | 21,225 | 211,266 | 2 | **120.0s** |
| **Cognitive Task Analysis Architect part_01** | Mapper | 6 | 50,882 | 10,121 | 170,683 | 1 | **75.0s** |
| **Cognitive Task Analysis Architect part_05** | Mapper | 7 | 51,898 | 22,013 | 195,577 | 2 | **126.0s** |
| **Cognitive Task Analysis Architect part_08** | Mapper | 9 | 62,938 | 19,970 | 331,263 | 3 | **138.0s** |
| **Cognitive Task Analysis Architect part_07** | Mapper | 7 | 57,877 | 21,596 | 226,675 | 2 | **125.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 6 | 45,326 | 9,606 | 148,300 | 1 | **75.0s** |
| **CTA Harmonizer** | Harmonizer | 6 | 77,621 | 9,583 | 254,335 | 0 | **63.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `22 shards concurrentes`
- **Duración Mínima de Shard:** `79.0s` | **Mediana:** `206.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`415.0s`** (`6.9 min`) por `Shard Author shard_17`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+209.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`42,449.2 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_01** | `Hab-01, Hab-02` | 2 | 52,941 | 25,569 | 244,840 | 78,510 | **39,255.0** | 9 | 1 | **173.0s** |
| **Shard Author shard_02** | `Hab-05, Hab-06` | 2 | 80,491 | 41,235 | 628,997 | 121,726 | **60,863.0** | 15 | 2 | **260.0s** |
| **Shard Author shard_03** | `Hab-20, Hab-21` | 2 | 83,957 | 30,732 | 659,649 | 114,689 | **57,344.5** | 16 | 3 | **231.0s** |
| **Shard Author shard_04** | `Hab-03, Hab-04` | 2 | 38,485 | 18,027 | 114,168 | 56,512 | **28,256.0** | 6 | 1 | **111.0s** |
| **Shard Author shard_05** | `Hab-07, Hab-08` | 2 | 64,676 | 25,179 | 485,525 | 89,855 | **44,927.5** | 16 | 3 | **191.0s** |
| **Shard Author shard_06** | `Hab-11, Hab-12` | 2 | 43,951 | 20,962 | 154,676 | 64,913 | **32,456.5** | 7 | 1 | **124.0s** |
| **Shard Author shard_07** | `Hab-14, Hab-15` | 2 | 48,259 | 24,495 | 199,693 | 72,754 | **36,377.0** | 8 | 2 | **165.0s** |
| **Shard Author shard_08** | `Hab-16, Hab-17` | 2 | 56,652 | 29,742 | 299,157 | 86,394 | **43,197.0** | 10 | 3 | **182.0s** |
| **Shard Author shard_09** | `Hab-18, Hab-19` | 2 | 49,640 | 24,913 | 197,017 | 74,553 | **37,276.5** | 8 | 2 | **169.0s** |
| **Shard Author shard_10** | `Hab-22, Hab-24` | 2 | 52,870 | 25,927 | 287,474 | 78,797 | **39,398.5** | 10 | 2 | **158.0s** |
| **Shard Author shard_11** | `Hab-25, Hab-26` | 2 | 55,894 | 22,081 | 330,967 | 77,975 | **38,987.5** | 12 | 1 | **160.0s** |
| **Shard Author shard_13** | `C-27, C-28, C-29` | 3 | 94,901 | 43,206 | 931,123 | 138,107 | **46,035.7** | 18 | 3 | **297.0s** |
| **Shard Author shard_14** | `C-04, C-05, C-06` | 3 | 63,586 | 32,815 | 342,233 | 96,401 | **32,133.7** | 10 | 1 | **206.0s** |
| **Shard Author shard_15** | `C-01, C-02, C-03` | 3 | 63,822 | 29,756 | 416,760 | 93,578 | **31,192.7** | 12 | 1 | **195.0s** |
| **Shard Author shard_16** | `C-24, C-25, C-26` | 3 | 94,412 | 55,520 | 753,104 | 149,932 | **49,977.3** | 15 | 2 | **333.0s** |
| **Shard Author shard_17 🛑** | `C-30, C-31, C-32` | 3 | 127,180 | 63,102 | 1,575,686 | 190,282 | **63,427.3** | 25 | 3 | **415.0s** |
| **Shard Author shard_18** | `C-07, C-08, C-09` | 3 | 69,067 | 33,020 | 484,689 | 102,087 | **34,029.0** | 13 | 1 | **218.0s** |
| **Shard Author shard_19** | `C-10, C-11, C-12` | 3 | 92,226 | 34,242 | 794,271 | 126,468 | **42,156.0** | 17 | 1 | **256.0s** |
| **Shard Author shard_20** | `C-13, C-19, C-20` | 3 | 64,034 | 34,637 | 343,035 | 98,671 | **32,890.3** | 10 | 1 | **208.0s** |
| **Shard Author shard_21** | `C-21, C-22, C-23` | 3 | 86,358 | 49,459 | 732,955 | 135,817 | **45,272.3** | 16 | 1 | **303.0s** |
| **Shard Author shard_22** | `C-38, C-40, C-41` | 3 | 111,247 | 44,297 | 1,372,842 | 155,544 | **51,848.0** | 24 | 4 | **311.0s** |
| **Shard Author shard_12** | `Hab-27` | 1 | 33,060 | 13,183 | 96,322 | 46,243 | **46,243.0** | 6 | 1 | **79.0s** |

---

### 3.3b. Stage 3B: Remediación y Repair Engineers (Ingenieros de Reparación)
- **Total de Repair Engineers Desplegados:** `6 subagentes`
- **Duración Mínima:** `20.0s` | **Mediana:** `58.0s` | **Máxima:** `78.0s` (`1.3 min`)
- **Tokens Activos Totales en Reparación:** `278,835 tokens`
- **Agente Determinante del Retraso:** `Repair Engineer C-20`

| Repair Engineer | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Errores | Duración |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Repair Engineer Hab-06** | 9 | 35,118 | 4,742 | 122,553 | 39,860 | 1 | **50.0s** |
| **Repair Engineer Hab-21** | 9 | 55,111 | 7,259 | 244,297 | 62,370 | 1 | **69.0s** |
| **Repair Engineer shard_14 (C-05, C-04)** | 5 | 41,194 | 6,730 | 84,590 | 47,924 | 0 | **58.0s** |
| **Repair Engineer C-20** | 7 | 41,842 | 8,952 | 158,010 | 50,794 | 1 | **78.0s** |
| **Repair Engineer C-06** | 6 | 38,498 | 2,100 | 80,786 | 40,598 | 1 | **20.0s** |
| **Repair Engineer shard_05 (Hab-07, Hab-08)** | 7 | 32,719 | 4,570 | 102,324 | 37,289 | 0 | **51.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ⚠️ NO PASÓ AL PRIMER INTENTO — APROBADO POST-REJUDGE (120/120 REACTIVOS)  
> La Ronda 1 de Blind Judges registró 0 discrepancia(s), por lo que no hubo acuerdo limpio al primer intento. Tras correcciones y Rejudge, el resultado final alcanzó 100.0% de acuerdo (0 discrepancias).

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `120 reactivos` (53 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `12 jueces` | Aislamiento epistémico en Stage 5 |
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
- ⏱️ **Tiempo Total de Pared del Orquestador:** `19.25 min` (`1155.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `1.2 min` (`73.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `0.1 min` (`4.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `2.0 min` (`119.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_17
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_17 tardó 415.0s frente a la mediana de 206.0s (+209.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

### ⚠️ [MEDIUM] Fricción de Herramientas en 7 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Cognitive Task Analysis Architect part_08 acumularon fallos en consola (3 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `171 turnos`
- **Volumen Total de Razonamiento:** `543,198 caracteres`
- **Razonamiento del Orquestador:** `18 turnos` (4,374 chars)
- **Razonamiento de Subagentes:** `153 turnos` (538,824 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect part_06** | 1 | 3,667 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_03** | 2 | 3,532 | ⚠️ 2 |
| **Cognitive Task Analysis Architect part_04** | 2 | 3,209 | ⚠️ 2 |
| **Cognitive Task Analysis Architect part_01** | 1 | 2,657 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_05** | 2 | 3,915 | ⚠️ 2 |
| **Cognitive Task Analysis Architect part_08** | 2 | 2,841 | ⚠️ 3 |
| **Cognitive Task Analysis Architect part_07** | 2 | 2,637 | ⚠️ 2 |
| **Cognitive Task Analysis Architect part_02** | 2 | 3,003 | ⚠️ 1 |
| **CTA Harmonizer** | 3 | 8,084 | 0 |
| **Shard Author shard_01** | 3 | 18,775 | ⚠️ 1 |
| **Shard Author shard_02** | 5 | 23,640 | ⚠️ 2 |
| **Shard Author shard_03** | 6 | 14,404 | ⚠️ 3 |
| **Shard Author shard_04** | 3 | 12,292 | ⚠️ 1 |
| **Shard Author shard_05** | 4 | 13,248 | ⚠️ 3 |
| **Shard Author shard_06** | 4 | 17,100 | ⚠️ 1 |
| **Shard Author shard_07** | 3 | 17,634 | ⚠️ 2 |
| **Shard Author shard_08** | 4 | 19,060 | ⚠️ 3 |
| **Shard Author shard_09** | 3 | 15,199 | ⚠️ 2 |
| **Shard Author shard_10** | 2 | 16,614 | ⚠️ 2 |
| **Shard Author shard_11** | 4 | 12,445 | ⚠️ 1 |
| **Shard Author shard_13** | 6 | 25,333 | ⚠️ 3 |
| **Shard Author shard_14** | 3 | 25,476 | ⚠️ 1 |
| **Shard Author shard_15** | 4 | 15,673 | ⚠️ 1 |
| **Shard Author shard_16** | 6 | 14,860 | ⚠️ 2 |
| **Shard Author shard_17** | 11 | 19,914 | ⚠️ 3 |
| **Shard Author shard_18** | 4 | 20,411 | ⚠️ 1 |
| **Shard Author shard_19** | 5 | 16,178 | ⚠️ 1 |
| **Shard Author shard_20** | 3 | 19,169 | ⚠️ 1 |
| **Shard Author shard_21** | 7 | 23,268 | ⚠️ 1 |
| **Shard Author shard_22** | 7 | 21,625 | ⚠️ 4 |
| **Shard Author shard_12** | 2 | 7,772 | ⚠️ 1 |
| **Blind Judge 01** | 1 | 6,956 | 0 |
| **Blind Judge 02** | 1 | 7,769 | 0 |
| **Blind Judge 03** | 1 | 8,919 | 0 |
| **Blind Judge 04** | 1 | 5,916 | 0 |
| **Blind Judge 05** | 1 | 6,511 | 0 |
| **Blind Judge 06** | 1 | 8,760 | 0 |
| **Blind Judge 07** | 1 | 8,031 | 0 |
| **Blind Judge 08** | 1 | 7,098 | 0 |
| **Blind Judge 09** | 1 | 7,283 | 0 |
| **Blind Judge 10** | 2 | 7,461 | 0 |
| **Repair Engineer Hab-06** | 4 | 2,682 | ⚠️ 1 |
| **Repair Engineer Hab-21** | 4 | 4,545 | ⚠️ 1 |
| **Repair Engineer shard_14 (C-05, C-04)** | 3 | 4,321 | 0 |
| **Repair Engineer C-20** | 4 | 8,217 | ⚠️ 1 |
| **Repair Engineer C-06** | 5 | 1,378 | ⚠️ 1 |
| **Repair Engineer shard_05 (Hab-07, Hab-08)** | 4 | 3,158 | 0 |
| **Blind Judge 01** | 1 | 7,958 | 0 |
| **Blind Judge 02** | 1 | 8,226 | 0 |

---
*Reporte forense determinista emitido por `c2c-run-auditor`.*