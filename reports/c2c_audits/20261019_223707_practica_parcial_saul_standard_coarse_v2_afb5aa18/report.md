# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Practica Parcial Saul Standard Coarse V2 (`practica_parcial_saul_standard_coarse_v2`)

**Fecha de Auditoría:** `2026-10-20 03:37:07 UTC`  
**Conversación Orquestadora:** [`afb5aa18-d2f3-4bd2-b452-4b73c313316e`](conversation://afb5aa18-d2f3-4bd2-b452-4b73c313316e)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\practica_parcial_saul_standard_coarse_v2\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `7 archivos` (103 págs / 10.39 MB) | MATH_IV_Problem_Set_I.pdf, MATH_IV_Problem_Set_II_2026_II.pdf, MATH_IV_Problem_Set_III_2026_II.pdf, TEMA 1 (EDP SAÚL) 2.pdf, TEMA 2 (APLICACIONES ECONOMICAS).pdf, TEMA 2 (S'EDOS I ).pdf, TEMA 2 (S'EDOS II).pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`14 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`7 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`17 subagentes`** | Visión (0), CTA (7), Autores (7), Jueces (0) |
| **Reactivos Finales Validados** | **`370 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`2,983,655` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`698,105` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`54,140,018` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`5,129,203` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`59,269,221` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`160,187.1 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`13,862.7 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`4,233,515.8 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`173,132.1 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`575,429.3 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`9.74 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`6.16 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`3.03x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `afb5aa18`):** `8 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-10-19 08:16:01` | `4.08s` | `0` (`0` act) | 0 | `—` |
| **`01_cta`** | `2026-10-19 08:32:07` | `0.13s` | `4,411,197` (`1,035,459` act) | 7 | `competencies=14` |
| **`02_shard`** | `2026-10-19 08:32:14` | `0.01s` | `0` (`0` act) | 0 | `shards=7` |
| **`03_templates`** | `2026-10-19 09:09:49` | `24.77s` | `21,893,599` (`2,423,849` act) | 7 | `count=14` |
| **`04_build`** | `2026-10-19 09:10:12` | `4.53s` | `0` (`0` act) | 0 | `total_questions=370` |
| **`05_verify`** | `2026-10-19 09:10:24` | `3.26s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\practica_parcial_saul_standard_coarse_v2\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-10-19 09:14:16` | `0.06s` | `537,747` (`209,488` act) | 3 | `passed=True` |
| **`06_publish`** | `2026-10-19 09:14:26` | `2.28s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\practica_parcial_saul_standard_coarse_v2.json` |

---

### 3.1. Stage 1A: Preprocesamiento de Visión
- **Subagentes de Visión Desplegados:** `0 agentes en paralelo`
- **Tiempo de Pared de la Etapa (Máximo / Critical Path):** **`0.0s`** (`0.0 min`)
- **Agente Determinante del Camino Crítico:** `N/A`

| Subagente de Visión | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

---

### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)
- **Arquitectura:** `MAPREDUCE (7 Mappers)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`777.0s`** (determinado por `Cognitive Task Analysis Architect part_04`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`0.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`777.0s`** (`12.9 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cognitive Task Analysis Architect part_04** | Mapper | 17 | 222,557 | 20,305 | 480,774 | 0 | **777.0s** |
| **Cognitive Task Analysis Architect part_07** | Mapper | 25 | 185,203 | 20,420 | 1,061,962 | 1 | **441.0s** |
| **Cognitive Task Analysis Architect part_05** | Mapper | 24 | 164,980 | 20,834 | 874,958 | 2 | **253.0s** |
| **Cognitive Task Analysis Architect part_06** | Mapper | 10 | 80,240 | 16,103 | 225,320 | 1 | **148.0s** |
| **Cognitive Task Analysis Architect part_03** | Mapper | 10 | 73,810 | 16,147 | 191,238 | 1 | **166.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 17 | 119,839 | 23,591 | 622,101 | 2 | **219.0s** |
| **Cognitive Task Analysis Architect part_01** | Mapper | 9 | 68,747 | 15,647 | 161,817 | 1 | **171.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `7 shards concurrentes`
- **Duración Mínima de Shard:** `425.0s` | **Mediana:** `794.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`858.0s`** (`14.3 min`) por `Shard Author shard_07`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+64.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`173,132.1 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_01** | `Hab-01, Hab-02` | 2 | 151,684 | 44,974 | 1,669,258 | 196,658 | **98,329.0** | 33 | 0 | **425.0s** |
| **Shard Author shard_06** | `Hab-07, Hab-08` | 2 | 361,557 | 89,799 | 2,746,501 | 451,356 | **225,678.0** | 34 | 3 | **812.0s** |
| **Shard Author shard_02** | `C-01, Hab-03` | 2 | 356,688 | 64,879 | 2,212,348 | 421,567 | **210,783.5** | 36 | 2 | **573.0s** |
| **Shard Author shard_03** | `Hab-04, C-02` | 2 | 366,251 | 88,936 | 4,441,423 | 455,187 | **227,593.5** | 47 | 5 | **794.0s** |
| **Shard Author shard_04** | `C-03, Hab-05` | 2 | 221,279 | 55,129 | 3,358,943 | 276,408 | **138,204.0** | 45 | 3 | **559.0s** |
| **Shard Author shard_05** | `C-04, Hab-06` | 2 | 243,720 | 92,495 | 3,099,422 | 336,215 | **168,107.5** | 38 | 3 | **847.0s** |
| **Shard Author shard_07 🛑** | `Hab-09, C-05` | 2 | 199,013 | 87,445 | 1,941,855 | 286,458 | **143,229.0** | 33 | 3 | **858.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ❌ NO PASARON AL PRIMER INTENTO (REQUIRIÓ INTERVENCIONES)  
> Los blind judges y la verificación psicométrica registraron discrepancias que requirieron correcciones. La validación previa operó con 1 errores iniciales, requiriendo rondas de auto-reparación o intervención técnica.

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `28 reactivos` (14 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `0 jueces` | Aislamiento epistémico en Stage 5 |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | 1 violaciones iniciales registradas |
| **Iteraciones de Auto-Reparación** | `1 iteraciones` en sandbox | 1 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `5 operaciones directas` | 5 ediciones registradas |

#### Detalle de Acciones Registradas:
- 1. **Bucle de Auto-Reparación**: Se ejecutó RepairLoop sobre el lote de evaluación.
- 2. **Intervenciones de Supervisor (5 operaciones)**: Operaciones sobre `c2c_cta_architect.json`, `shard_06_data.py`.
- 3. **Certificación y Verificación Final**: Se concluyó la validación tras 1 iteraciones sobre el lote de 28 reactivos.

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared del Orquestador:** `60.03 min` (`3602.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `19.8 min` (`1189.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`4.3 min`** (`257.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `1.0 min` (`59.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `4.1 min` (`247.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`5`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **65** | `c2c_cta_architect.json` | Modificación / Script Auxiliar | Fixing CTA architect lean prompt to use canonical positional tuples instead of dicts | `replace_file_content` | 6,829 |
| **291** | `shard_06_data.py` | Expansión Paramétrica (TPL-VAR) | Ampliación de dominio para superar 50 semillas en shard_06_data.py (Fix pmatrix double braces, parameter ranges, and non-repetitive c) | `write_to_file` | 13,726 |
| **311** | `shard_06_data.py` | Modificación / Script Auxiliar | Clean vars dict without inner f-strings or braces in shard_06_data.py | `write_to_file` | 13,127 |
| **426** | `shard_06_data.py` | Modificación / Script Auxiliar | Update shard_06_data.py with clean LaTeX notation avoiding brace ambiguity after double ba | `write_to_file` | 12,290 |
| **452** | `shard_06_data.py` | Modificación / Script Auxiliar | Clean shard_06_data.py without top-level string constants and with clean inline strings | `write_to_file` | 11,530 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Síndrome del Orquestador Reparador (5 intervenciones manuales)
- **Ámbito:** `Director (Orchestrator)`
- **Diagnóstico:** El orquestador principal ejecutó 5 operaciones directas de edición de código y plantillas. Consumió más de 57,502 tokens en turnos de mantenimiento/recuperación manual.

### 🛑 [HIGH] Antipatrón de Micro-Bucle Interactivo (47 turnos en Shard Author shard_03)
- **Ámbito:** `Shard Author shard_03`
- **Diagnóstico:** 7 subagentes realizaron > 30 turnos individuales (ej. Shard Author shard_03 con 47 turnos). Ocurre por bucles de depuración o escritura incremental en lugar de redactar por lotes atómicos.

### ⚠️ [MEDIUM] Fricción de Herramientas en 5 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_06 acumularon fallos en consola (3 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `259 turnos`
- **Volumen Total de Razonamiento:** `564,724 caracteres`
- **Razonamiento del Orquestador:** `79 turnos` (40,566 chars)
- **Razonamiento de Subagentes:** `180 turnos` (524,158 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect part_04** | 7 | 14,440 | 0 |
| **Cognitive Task Analysis Architect part_07** | 8 | 13,406 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_05** | 8 | 14,919 | ⚠️ 2 |
| **Cognitive Task Analysis Architect part_06** | 7 | 18,910 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_03** | 7 | 17,522 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_02** | 7 | 18,009 | ⚠️ 2 |
| **Cognitive Task Analysis Architect part_01** | 6 | 12,640 | ⚠️ 1 |
| **Shard Author shard_01** | 15 | 31,886 | 0 |
| **Shard Author shard_06** | 21 | 67,364 | ⚠️ 3 |
| **Shard Author shard_02** | 13 | 47,451 | ⚠️ 2 |
| **Shard Author shard_03** | 22 | 66,742 | ⚠️ 5 |
| **Shard Author shard_04** | 18 | 31,543 | ⚠️ 3 |
| **Shard Author shard_05** | 18 | 69,679 | ⚠️ 3 |
| **Shard Author shard_07** | 14 | 68,587 | ⚠️ 3 |
| **Subagent** | 3 | 14,370 | 0 |
| **Subagent** | 3 | 9,081 | 0 |
| **Subagent** | 3 | 7,609 | 0 |

---

## 7. Diagnóstico Forense de Causa Raíz y Optimización Agéntica

### 7.1. Verificación de Aislamiento Estricto Zero-Collision (`conversation_id`)
- **Estado de Aislamiento:** ✅ **100% Verificado (Zero Telemetry Collision)**
- **Validación Causal:**
  - El archivo `courses/practica_parcial_saul_standard_coarse_v2/work/state.json` registra de forma unívoca `conversation_id: afb5aa18-d2f3-4bd2-b452-4b73c313316e` y `course_id: practica_parcial_saul_standard_coarse_v2`.
  - La totalidad de los 8 snapshots incrementales en `work/telemetry/` (`00_prepare.json`, `01_cta.json`, `02_shard.json`, `03_templates.json`, `04_build.json`, `05_verify.json`, `05b_judge_compare.json` y `06_publish.json`) poseen estampas concordantes `conversation_id: afb5aa18-d2f3-4bd2-b452-4b73c313316e`.
  - Se confirmó la existencia del subdirectorio de archivo y respaldo en caliente `work/telemetry/by_conversation/afb5aa18-d2f3-4bd2-b452-4b73c313316e/`, garantizando una barrera infranqueable frente a otras corridas del mismo corpus (`a53e6af1`, `f9b9d459`, `acdc402d`).
  - Cero contaminación cruzada en métricas unitarias, manifiestos de fragmentación o evaluaciones psicométricas ciegas.

---

### 7.2. Inspección Forense de Cuellos de Botella y Transcripts Agénticos

#### 7.2.1. Stage 1B: Análisis Cognitivo de Competencias (CTA Architects)
- **Straggler Determinante:** `Cognitive Task Analysis Architect part_04` (`79fcd0b8-288c-44a7-8a71-355627e28d18`).
- **Duración y Métricas:** **`777.0s`** (12.95 min), 17 turnos, 222,557 tokens in, 20,305 tokens out, 480,774 tokens cache.
- **Diagnóstico Forense de Causa Raíz:**
  1. **Desorientación de Esquema Inicial (Pasos 11 a 21):** El subagente no contó en su orden de trabajo con un bloque de sintaxis canónica inequívoca. Esto provocó que ejecutara consultas de ayuda en CLI (`python compile_cta.py --help`) y exploración no autorizada de sistemas de archivos de corridas previas (`Get-ChildItem courses/practica_parcial_saul_standard_coarse/work/cta_parts` y lectura de `courses/practica_parcial_saul/work/cta_parts/part_04_data.py`), desperdiciando más de 4 minutos en sondeos exploratorios.
  2. **Inferencia Monolítica Masiva (Paso 23):** El modelo entró en una cadena de pensamiento (`thinking`) de 4,120 caracteres analizando equilibrio de mercado vs ecuaciones diferenciales parciales (EDP cuasilineales de primer orden, método de Lagrange y curvas características). En un único turno generó **13,661 tokens de salida**, demorando 2 minutos 13 segundos de inferencia continua en streaming.
  3. **Verificación Redundante en Fragmentos (Pasos 27 y 29):** Tras compilar exitosamente, el subagente ejecutó dos llamadas consecutivas de `view_file` para leer `part_04.json` (líneas 1..100 y 101..249) antes de enviar la señal `send_message`, agregando 2 minutos adicionales de latencia ociosa.

#### 7.2.2. Stage 3: Autoría de Reactivos por Shard y Análisis de Micro-Bucles
- **Shard Author shard_03 (`6ef434b8`, 47 turnos, 794.0s / 13.23 min):**
  - *Patrón Detectado:* Micro-bucle interactivo severo con 5 ediciones parciales consecutivas (`replace_file_content`) sobre `shard_03_data.py`.
  - *Causa Raíz:* En el paso 45 falló con `NameError: name 'pmatrix' is not defined` (intento de invocar `pmatrix` como identificador de Python en lugar de entorno LaTeX). Posteriormente sufrió fallos recurrentes de la regla **`R-20: SINTAXIS / LLAVES`** por variables matemáticas no escapadas (`{r0}` y `{theta}`). Ejecutó 10 lecturas de inspección sobre `compile_shard.py` para realizar ingeniería inversa de las reglas de validación.
- **Shard Author shard_05 (`2c690087`, 38 turnos, 847.0s / 14.12 min):**
  - *Patrón Detectado:* 3 reescrituras completas de `shard_05_data.py` y 12 lecturas a archivos del validador.
  - *Causa Raíz:* Errores repetitivos de resolución de variables en los dominios continuos y colisiones de rutas en `.check_attempts`, forzando ciclos de regeneración completos.
- **Shard Author shard_06 (`a517b028`, 34 turnos, 812.0s / 13.53 min):**
  - *Patrón Detectado:* Bloqueo total del agente en paso 52 con `TypeError: unsupported format string passed to tuple.__format__` y distractor repetitivo `R-18`. El subagente no logró recuperarse autónomamente y abandonó el shard en estado fallido, transfiriendo la carga de reparación al orquestador principal.
- **Shard Author shard_07 (`23410f2b`, 33 turnos, 858.0s / 14.3 min — Straggler Crítico):**
  - *Patrón Detectado:* Agente más lento de la etapa (+64s sobre la mediana). 16 lecturas exhaustivas a `compile_shard.py` (líneas 580..1080).
  - *Causa Raíz:* En el paso 56 colapsó con 6 errores de `R-20` (`Llaves '{c21}' no declaradas en vars`). El modelo demoró más de 5 minutos formulando expresiones analíticas de trayectorias en sistemas dinámicos para `Hab-09` y `C-05` antes de lograr una segunda escritura limpia en paso 65.

---

### 7.3. Auditoría Forense Exhaustiva de las 5 Intervenciones Manuales del Orquestador

El orquestador principal ejecutó **5 operaciones directas de reparación de código**, consumiendo 4.3 minutos y 57,502 tokens en tareas de soporte:

```mermaid
flowchart TD
    O1["Paso 65: c2c_cta_architect.json
Fix de Esquema de Tuplas Lean"] --> CTA["Fase CTA Architects (7 Mappers)"]
    CTA --> Shards["Fase Shard Authors (7 Shards)"]
    Shards --> FailS6["Shard 06 Falla en Paso 52
(TypeError + R-18)"]
    FailS6 --> O2["Paso 291: shard_06_data.py
Fix {{pmatrix}} + R-18 + Expansión Dominios"]
    O2 --> RegexFail["check_templates.py falla en auto_heal
(Regex truncada por f-string)"]
    RegexFail --> O3["Paso 311: shard_06_data.py
Eliminación de f-strings en vars"]
    O3 --> R20Fail["Fallo R-20 en instantiate_competency
({y0}, {b2} sin sustituir)"]
    R20Fail --> O4["Paso 426: shard_06_data.py
Fix de llaves tras doble backslash"]
    O4 --> R03Fail["Fallo R-03: ERR_LATEX_CORRUPT
(Constantes multilínea con \n)"]
    R03Fail --> O5["Paso 452: shard_06_data.py
Incrustación Raw Strings Inline (Patrón Shard 01)"]
    O5 --> CompileOK["Compilación Shard 06 Exitosa (0 Errores)"]
```

1. **Paso 65 (`work/dispatch/types/c2c_cta_architect.json` — Modificación de Prompt Lean):**
   - *Error Subyacente:* El prompt lean pre-generado contenía un ejemplo obsoleto donde los distractores clínicos se estructuraban como diccionarios (`{"name": ..., "error": ...}`), mientras que el compilador `compile_cta.py` exigía estrictamente tuplas posicionales canónicas de 6 elementos.
   - *Razonamiento Previo (`thinking`):* El modelo analizó el esquema y razonó: *"The existing example's distractor format uses dictionaries, differing from the expected tuple structure. The c2c_cta_architect.json file needs correction to align with the tuple format: (error name, wrong belief, correct belief, manifestation, hint, omitted step)."*
   - *Herramienta y Resultado:* `replace_file_content`. Armonizó el contrato antes de lanzar los 7 subagentes CTA, evitando un fallo generalizado en toda la etapa 1B.
2. **Paso 291 (`work/shards/shard_06_data.py` — Reparación TPL-VAR y R-18):**
   - *Error Subyacente:* El subagente de Shard 06 dejó el código inutilizable: las matrices `\\begin{pmatrix}` tenían llaves simples `{pmatrix}` que Python `.format()` intentaba evaluar como variables inexistentes; el generador producía menos de 50 semillas válidas y los distractores de `Hab-08` violaban `R-18` (distractores boilerplate sintéticos con prefijos idénticos).
   - *Razonamiento Previo (`thinking`):* *"Python's .format() interprets single braces as format fields, seeking a key named pmatrix within the provided variables... escape the braces as {{pmatrix}}. Parameter space in gen_Hab07 required expanding variable ranges... distractors in Hab-08 use a repetitive, synthetic template... rewrite distractors to have more natural, clinically-varied phrasings."*
   - *Herramienta y Resultado:* `write_to_file`. Reescribió completamente el shard con dobles llaves y distractores enriquecidos.
3. **Paso 311 (`work/shards/shard_06_data.py` — Corrección de Truncamiento de Regex en Validador):**
   - *Error Subyacente:* `compile_shard.py` falló en dry-run con `TypeError: unsupported format string passed to tuple.__format__`.
   - *Razonamiento Previo (`thinking`):* El orquestador inspeccionó `check_templates.py` (líneas 520..610) y descubrió un bug arquitectónico en el motor de auto-reparación: la expresión regular `r"(['"]vars['"]\s*:\s*\{)([^}]*)(\})"` utilizada para capturar `vars` se detenía en el primer cierre de llave `}`. En `shard_06_data.py` (línea 127), existía un f-string `f"{lambda1}t"`, cuya llave interna cerraba prematuramente la captura y corrompía la inyección de variables. Razonó: *"The regex failure stems from the presence of f-strings within the vars dictionary, specifically the embedded curly brace... Removing f-strings from the vars dictionary and instead using string concatenation resolves the issue."*
   - *Herramienta y Resultado:* `write_to_file`. Sustituyó los f-strings internos por concatenación de cadenas, neutralizando el fallo de la regex.
4. **Paso 426 (`work/shards/shard_06_data.py` — Reparación de Sustitución de Variables R-20):**
   - *Error Subyacente:* Durante `instantiate_competency`, las preguntas de `Hab-07` fallaban por la regla `R-20`: las variables `{y0}` y `{b2}` no se sustituían en los enunciados/soluciones, y un comando de verificación en PowerShell falló por interpolación errónea de `$X(0)`.
   - *Razonamiento Previo (`thinking`):* *"The template failed to generate valid instances; check_instance_invariants consistently failed. The root cause appears to be rule R-20. The variables {y0} and {b2} weren't being substituted in the stem/solution... Update shard_06_data.py with clean LaTeX notation avoiding brace ambiguity after double backslash."*
   - *Herramienta y Resultado:* `write_to_file`. Sincronizó todas las variables de los strings matemáticos con las llaves exportadas por `vars`.
5. **Paso 452 (`work/shards/shard_06_data.py` — Eliminación de Corrupción de Escapes R-03):**
   - *Error Subyacente:* `compile_shard.py` arrojó `[R-03: ERR_LATEX_CORRUPT]` debido a secuencias `\n` interpretadas como caracteres de control por el escáner léxico dentro de constantes multilínea a nivel de módulo (`stem_hab07`, `sol_hab07`).
   - *Razonamiento Previo (`thinking`):* El orquestador inspeccionó `src/validator/lexical_scanner.py` y luego revisó `shard_01_data.py` para entender por qué Shard 01 había compilado sin errores: *"shard_01_data.py contains single-line raw strings for problem stems and solutions, lacking newline characters... directly embed raw strings for stem and sol within the data structure. Replicating this pattern will resolve the issue."*
   - *Herramienta y Resultado:* `write_to_file`. Reestructuró `shard_06_data.py` eliminando constantes globales e incrustando cadenas raw (`r"..."`) inline en la lista `TEMPLATES`. En el paso 456, `compile_shard.py` finalizó con **0 errores**.

---

### 7.4. Stage 5: Verificación, Arbitraje Ciego y Aclaración Psicométrica
- **Incidencia de Rutas en Paso 471 (17 Errores de FileNotFoundError):**
  - El orquestador intentó acceder al archivo inexistente `work/dispatch/manifest.json` mediante `view_file`. El sistema operativo arrojó errores de permisos/ruta que se registraron como 17 fallos de tipo `FileNotFoundError` en la telemetría antes de que el orquestador corrigiera el comando y listara `work/dispatch/items/judge_*.json`.
- **Desempeño de los Blind Judges (Stage 5b):**
  - Los 3 jueces ciegos (`judge_01`, `judge_02`, `judge_03`) evaluaron concurrentemente el lote estratificado de **28 reactivos** (14 competencias × 2 reactivos).
  - Operaron con **100% de aislamiento epistémico** (0 búsquedas web, 0 llamadas a APIs externas, resolución matemática pura desde primeros principios).
  - **Dictamen Psicométrico Real:** El arbitraje determinista en `run_stage_judge_compare` concluyó con **`passed=True`**, registrando un acuerdo del **100.0% (28/28 reactivos)** frente al ground truth (`0 discrepancias`).
  - *Nota Forense:* El distintivo de *"no pasaron al primer intento"* emitido en la sección 3.4 responde a la lógica estricta del motor de auditoría (`audit_engine.py`), que marca la etapa como "con intervenciones" si se requirieron reparaciones previas sobre los archivos de datos de los shards (`shard_06_data.py`). La fase psicométrica ciega en sí misma fue perfecta y no requirió reintentos.

---

### 7.5. Síntesis Forense Comparativa Longitudinal de las 5 Corridas

A continuación se presenta la comparativa técnica entre las 5 ejecuciones de la tanda evaluada en el histórico:

| Parámetro / Métrica | Solow Model v15 (`4ceacf92`) | Práctica Parcial Full (`acdc402d`) | Práctica Parcial Coarse v1 (`a53e6af1`) | Práctica Parcial Standard (`f9b9d459`) | **Práctica Parcial Coarse v2 (`afb5aa18`) [AUDITADA]** |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Páginas / Peso Entrada** | 36 pág (1.49 MB) | 103 pág (10.39 MB) | 103 pág (10.39 MB) | 103 pág (10.39 MB) | **103 pág (10.39 MB)** |
| **Competencias / Reactivos** | 15 comp / 360 preg | 118 comp / 2850 preg | 13 comp / 320 preg | 65 comp / 1590 preg | **14 comp / 370 preg** |
| **Tiempo de Pared Total** | 27.1 min (1626s) | 85.7 min (5139s) | **32.8 min (1970s)** | 64.2 min (3853s) | **60.0 min (3602s)** |
| **Factor de Aceleración (Speedup)** | 3.32x | **5.17x** | 3.33x | 3.92x | **3.03x** |
| **Tokens Totales (con Caché)** | 22.06 M | 102.72 M | **21.13 M** | 71.44 M | **59.27 M** |
| **Tokens Activos (Netos)** | 2.11 M | 9.85 M | **1.84 M** | 6.21 M | **5.13 M** |
| **Tokens / Pregunta Final** | 61,291.6 | **36,040.6** | 66,027.4 | 44,933.1 | **160,187.1** |
| **Segundos / Pregunta Final** | 4.52 s | **1.80 s** | 6.16 s | 2.42 s | **9.74 s** |
| **Intervenciones Manuales** | 🛠️ 1 | 🛠️ 17 | **🛠️ 0 (Limpio)** | 🛠️ 3 | **🛠️ 5** |
| **Veredicto Blind Judges** | ✅ Limpio | ❌ Requiere Interv. | **✅ Limpio** | ❌ Requiere Interv. | **❌ Requiere Interv. (Templates)** |

#### Hallazgos Clave de la Comparativa:
1. **El Coste de la Fricción (Coarse v1 vs Coarse v2):** Frente a la corrida gemela `a53e6af1` (Coarse v1), que generó 320 preguntas en solo 32.8 minutos y 21.1M tokens sin ninguna intervención manual, la corrida auditada (`afb5aa18`) requirió **el doble de tiempo (60.0 min)** y **casi el triple de tokens (59.27 M)**. Este sobrecosto masivo fue provocado por el straggler de CTA part_04 (777s vs 150s), el micro-bucle de Shard 03 (47 turnos) y las 4 intervenciones manuales consecutivas sobre Shard 06.
2. **Economía de Escala vs Sobrecarga de Coordinación:** La corrida full `acdc402d` obtuvo la mayor eficiencia unitaria (1.80 s/preg y 36k tok/preg) debido a la amortización sobre 2,850 reactivos, pero requirió 17 intervenciones manuales del director. La granularidad coarse bien ejecutada (`a53e6af1`) demostró ser el punto óptimo de estabilidad cero-intervención.

---

### 7.6. Recomendaciones Accionables de Optimización para el Pipeline C2C

1. **Blindaje de Esquema en Prompts de Stage 1B (Anti-Exploración):**
   - *Medida:* Incluir directamente en el cuerpo del work order de cada mapper CTA un bloque de ejemplo inmutable con la sintaxis exacta de tuplas posicionales de 6 elementos para los distractores.
   - *Impacto:* Eliminará las búsquedas de ayuda en CLI y exploraciones externas de archivos ajenos, reduciendo la duración de mappers como `part_04` de 777s a menos de 180s.
2. **Sustitución de Expresión Regular Frágil por Parser AST en `check_templates.py`:**
   - *Medida:* Reemplazar la regex `r"(['"]vars['"]\s*:\s*\{)([^}]*)(\})"` en `auto_heal_template_data` por una transformación basada en el módulo nativo `ast` de Python.
   - *Impacto:* Permitirá que el generador soporte f-strings anidados, diccionarios complejos y llaves matemáticas sin truncamientos prematuros ni fallos de auto-curación.
3. **Inyección Canónica del Patrón de Shards en `c2c_shard_author.json`:**
   - *Medida:* Incorporar en las instrucciones del autor de shards:
     a) Obligatoriedad de incrustar `stem` y `sol` como raw strings (`r"..."`) inline en la tupla `TEMPLATES` (prohibiendo constantes globales con `\n`).
     b) Obligatoriedad de dobles llaves `{{pmatrix}}` para matrices LaTeX.
   - *Impacto:* Reducirá a cero las 10 a 16 lecturas de ingeniería inversa que realiza cada autor sobre `compile_shard.py`, recortando el tiempo de autoría en un 40%.
4. **Barrera de Contención de Micro-Bucles (Circuit Breaker de Ediciones):**
   - *Medida:* Configurar el subagente de autoría para abortar ediciones parciales si acumula más de 2 fallos de compilación consecutivos, forzando una reescritura atómica integral del archivo en lugar de micro-parches de 47 turnos.
5. **Sanitización de Caracteres en Ejecución de Scripts CLI:**
   - *Medida:* Envolver las cadenas de comandos PowerShell del orquestador en bloques que escapen sistemáticamente el símbolo `$` en fórmulas matemáticas para evitar excepciones de variable no reconocida en Windows.

---
*Diagnóstico forense avanzado incorporado por el Auditor Forense Especializado C2C v3.2.*