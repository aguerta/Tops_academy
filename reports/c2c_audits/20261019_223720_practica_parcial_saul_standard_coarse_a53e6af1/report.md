# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Practica Parcial Saul Standard Coarse (`practica_parcial_saul_standard_coarse`)

**Fecha de Auditoría:** `2026-10-20 03:37:20 UTC`  
**Conversación Orquestadora:** [`a53e6af1-07b8-4246-8afd-4b4ac647d536`](conversation://a53e6af1-07b8-4246-8afd-4b4ac647d536)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\practica_parcial_saul_standard_coarse\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `7 archivos` (103 págs / 10.39 MB) | MATH_IV_Problem_Set_I.pdf, MATH_IV_Problem_Set_II_2026_II.pdf, MATH_IV_Problem_Set_III_2026_II.pdf, TEMA 1 (EDP SAÚL) 2.pdf, TEMA 2 (APLICACIONES ECONOMICAS).pdf, TEMA 2 (S'EDOS I ).pdf, TEMA 2 (S'EDOS II).pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`13 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`7 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`11 subagentes`** | Visión (0), CTA (1), Autores (7), Jueces (3) |
| **Reactivos Finales Validados** | **`320 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`1,682,013` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`492,786` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`18,202,590` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`2,926,179` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`21,128,769` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`66,027.4 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`9,144.3 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`1,625,289.9 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`138,133.5 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`205,133.7 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`6.16 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`9.75 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`3.33x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `a53e6af1`):** `8 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-10-19 07:39:02` | `4.15s` | `0` (`0` act) | 0 | `—` |
| **`01_cta`** | `2026-10-19 07:51:59` | `0.07s` | `655,468` (`165,764` act) | 1 | `competencies=13` |
| **`02_shard`** | `2026-10-19 07:52:06` | `0.01s` | `0` (`0` act) | 0 | `shards=7` |
| **`03_templates`** | `2026-10-19 08:06:48` | `20.54s` | `13,565,252` (`1,793,171` act) | 7 | `count=13` |
| **`04_build`** | `2026-10-19 08:06:58` | `3.67s` | `0` (`0` act) | 0 | `total_questions=320` |
| **`05_verify`** | `2026-10-19 08:07:23` | `2.43s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\practica_parcial_saul_standard_coarse\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-10-19 08:10:14` | `0.06s` | `507,575` (`210,958` act) | 3 | `passed=True` |
| **`06_publish`** | `2026-10-19 08:10:25` | `1.76s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\practica_parcial_saul_standard_coarse.json` |

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
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`601.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`601.0s`** (`10.0 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cognitive Task Analysis Architect** | Direct Architect | 12 | 125,533 | 42,572 | 608,295 | 0 | **601.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `7 shards concurrentes`
- **Duración Mínima de Shard:** `308.0s` | **Mediana:** `541.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`785.0s`** (`13.1 min`) por `Shard Author shard_02`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+244.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`138,133.5 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_01** | `C-01, Hab-01` | 2 | 92,803 | 41,160 | 569,741 | 133,963 | **66,981.5** | 15 | 1 | **308.0s** |
| **Shard Author shard_02 🛑** | `H-01, Hab-02` | 2 | 144,379 | 56,008 | 1,138,105 | 200,387 | **100,193.5** | 19 | 1 | **785.0s** |
| **Shard Author shard_03** | `C-02, Hab-03` | 2 | 430,349 | 60,806 | 3,732,462 | 491,155 | **245,577.5** | 42 | 3 | **579.0s** |
| **Shard Author shard_04** | `C-03, Hab-04` | 2 | 168,587 | 67,313 | 2,552,128 | 235,900 | **117,950.0** | 29 | 2 | **603.0s** |
| **Shard Author shard_06** | `Hab-05, C-06` | 2 | 197,431 | 64,860 | 1,220,291 | 262,291 | **131,145.5** | 18 | 2 | **479.0s** |
| **Shard Author shard_05** | `C-04, C-05` | 2 | 170,786 | 79,360 | 1,786,325 | 250,146 | **125,073.0** | 21 | 3 | **541.0s** |
| **Shard Author shard_07** | `Hab-06` | 1 | 185,558 | 36,336 | 899,831 | 221,894 | **221,894.0** | 21 | 2 | **375.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ✅ 100% ACUERDO AL PRIMER INTENTO (26/26 REACTIVOS)  
> Los **3 Blind Judges** (`Judge 01`, `Judge 02`, `Judge 03`) evaluaron concurrentemente el lote estratificado de 26 reactivos en aislamiento epistémico estricto (0 búsquedas web, 0 llamadas HTTP), logrando un acuerdo psicométrico del **100.0% (26/26)** con 0 discrepancias frente al ground truth al primer intento.

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `26 reactivos` (13 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `3 jueces` | Aislamiento epistémico estricto en Stage 5B (`Judge 01`, `Judge 02`, `Judge 03`) |
| **Resultado al Primer Intento** | **`✅ 100% Limpio (Sin Discrepancias)`** | Sin discrepancias ni arbitraje necesario |
| **Iteraciones de Auto-Reparación** | `1 iteraciones` en sandbox | 0 requeridas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Arbitraje Ciego (`05b_judge_compare.json`)**: 26/26 acuerdos (`100.0% agreement rate`, `0 discrepancias`).
- 2. **Verificación Determinista Previa (`--stage verify`)**: Detectó 1 error(es) léxico/estructural(es) corregido(s) antes del arbitraje ciego.

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared del Orquestador:** `32.83 min` (`1970.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `3.3 min` (`197.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `0.6 min` (`33.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `1.0 min` (`58.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`0`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| — | *Ninguna intervención registrada* | — | — | — | 0 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_02
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_02 tardó 785.0s frente a la mediana de 541.0s (+244.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

### 🛑 [HIGH] Antipatrón de Micro-Bucle Interactivo (42 turnos en Shard Author shard_03)
- **Ámbito:** `Shard Author shard_03`
- **Diagnóstico:** 1 subagentes realizaron > 30 turnos individuales (ej. Shard Author shard_03 con 42 turnos). Ocurre por bucles de depuración o escritura incremental en lugar de redactar por lotes atómicos.

### ⚠️ [MEDIUM] Fricción de Herramientas en 2 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_03 acumularon fallos en consola (3 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `132 turnos`
- **Volumen Total de Razonamiento:** `374,865 caracteres`
- **Razonamiento del Orquestador:** `24 turnos` (7,281 chars)
- **Razonamiento de Subagentes:** `108 turnos` (367,584 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect** | 6 | 31,975 | 0 |
| **Shard Author shard_01** | 7 | 31,790 | ⚠️ 1 |
| **Shard Author shard_02** | 10 | 39,632 | ⚠️ 1 |
| **Shard Author shard_03** | 24 | 41,986 | ⚠️ 3 |
| **Shard Author shard_04** | 15 | 52,865 | ⚠️ 2 |
| **Shard Author shard_06** | 12 | 54,341 | ⚠️ 2 |
| **Shard Author shard_05** | 17 | 57,403 | ⚠️ 3 |
| **Shard Author shard_07** | 7 | 25,098 | ⚠️ 2 |
| **Judge 01** (`0b12e5b0`) | 3 | 10,257 | 0 |
| **Judge 02** (`1cd527dc`) | 3 | 15,650 | 0 |
| **Judge 03** (`59e5b194`) | 4 | 6,587 | 0 |

---

## 7. Diagnóstico Forense de Causa Raíz y Optimización Agéntica

### 7.1. Verificación de Aislamiento Estricto Zero-Collision
- **Validación Criptográfica y de Estado:** La auditoría confirmó de manera fehaciente que `courses/practica_parcial_saul_standard_coarse/work/state.json` estampa exactamente `conversation_id: a53e6af1-07b8-4246-8afd-4b4ac647d536`.
- **Integridad de Snapshots de Etapa:** Los 8 archivos JSON incrementales en `work/telemetry/` (`00_prepare.json` a `06_publish.json`) corresponden al 100% a la conversación `a53e6af1`.
- **Espejo Persistente:** Se verificó la existencia del directorio `work/telemetry/by_conversation/a53e6af1-07b8-4246-8afd-4b4ac647d536/`, garantizando que esta corrida no colisionó ni reutilizó artefactos de ejecuciones previas de `practica_parcial_saul` ni de otros cursos en el workspace.

### 7.2. Despliegue y Orquestación de los 11 Subagentes
El transcript maestro de Antigravity (`transcript.jsonl`) evidencia el despacho ordenado y concurrente de **11 subagentes especializados**:
1. **1 Direct CTA Architect (`c2c_cta_architect` | UUID `a4091257-e2a0-445e-9b94-9b30eb0de8b5`):**
   - Despachado en el Turno 50.
   - Ejecutó 12 turnos durante 601.0s (10.02 min), sintetizando 7 archivos fuente (103 páginas) y abstrayendo **13 competencias pedagógicas** (`C-01` a `C-06`, `Hab-01` a `Hab-06`, `H-01`).
   - Generó el archivo de análisis pedagógico `courses/competence_analysis_practica_parcial_saul_standard_coarse.md` (42.5 KB) sin una sola advertencia de DAG cíclico o token cutoff.
2. **7 Shard Authors Concurrentes (`c2c_shard_author` | Despacho Turno 74):**
   - Invocados en paralelo con arquitectura *Pointer-Prompt* (`author_01.json` a `author_07.json`).
   - Cada autor asumió entre 1 y 2 competencias complejas de Ecuaciones Diferenciales Ordinarias (EDO), Ecuaciones en Derivadas Parciales (EDP) y Macroeconomía Dinámica.
   - Produjeron 13 plantillas paramétricas de código Python en `work/templates/` y sus respectivos datasets en `work/shards/`.
3. **3 Blind Judges Concurrentes (`c2c_judge` | Despacho Turno 120):**
   - Invocados en paralelo con orden de trabajo individual (`judge_01.json`, `judge_02.json`, `judge_03.json`).
   - Evaluaron un lote ciego estratificado de **26 reactivos** (2 por competencia) sin acceso a las soluciones (`judge_batch.json`).
   - **Resultado:** 100.0% de acuerdo psicométrico (26/26 reactivos concordantes, 0 discrepancias).

### 7.3. Causa Raíz de Cero Intervenciones Manuales del Supervisor
A diferencia de corridas tempranas donde el orquestador debió parchear manualmente archivos intermedios, esta corrida registró **`0` escrituras y `0` ediciones del supervisor (`writes=0`, `edits=0`)**.
- **Mecanismo de Éxito:** La combinación de la arquitectura de *Pointer Prompts* con el contrato determinista del script de compilación local (`compile_shard.py`) dotó a los Shard Authors de **capacidad de auto-reparación en sandbox (self-healing)**.
- Cuando los subagentes autores encontraron fallos sintácticos (`[R-20]` en Shard 02, 04, 05, 06) o errores de ejecución (`[TPL-DRY]` en Shard 03), el output del CLI les devolvió la tupla exacta con `StartLine`, `EndLine`, descripción del error y sugerencia de remediación.
- Los subagentes reescribieron o parcharon su propio código y relanzaron la compilación hasta obtener un estado limpio (`PASS`), permitiendo que el orquestador avanzara de etapa sin intervención humana ni asistencia correctiva manual.

### 7.4. Investigación Forense del Straggler Crítico: Shard Author shard_02 (785.0s)
- **Diagnóstico del Cuello de Botella:** `Shard Author shard_02` tardó **785.0s (13.08 min)**, superando en **+244.0s** la mediana de los autores (541.0s) y convirtiéndose en el determinante absoluto del camino crítico de Stage 3.
- **Descomposición del Tiempo:** El **98.5% del tiempo (773.0s)** correspondió a **inferencia LLM pura**, mientras que las herramientas locales consumieron únicamente 12.0s (1.5%). No existió bloqueo por comandos colgados ni lentitud de I/O en disco.
- **Causa Raíz Temática y Sintáctica:**
  1. *Complejidad Pedagógica:* Shard 02 tuvo a su cargo las competencias `H-01` y `Hab-02` (Ecuaciones en Derivadas Parciales de primer orden aplicadas a funciones de beneficios de empresas competitivas $\\Pi(p, w)$ con homogeneidad lineal y condiciones de frontera).
  2. *Fallo de Compilación:* En el Turno 24, la primera ejecución de `compile_shard.py` falló con `[-] [R-20: SINTAXIS / LLAVES]` debido a la presencia de llaves dobles residuales `{{...}}` en `Hab-02.json` (líneas 186..204), generadas al intentar escapar llaves de LaTeX dentro de cadenas de formato en Python.
  3. *Reescritura Monolítica:* En lugar de aplicar una edición focalizada, el subagente razonó durante casi 4 minutos y regeneró por completo el archivo `shard_02_data.py` (Turno 29), resolviendo el fallo y logrando la compilación limpia en el Turno 31 (`PASS: 2 plantillas, 50 semillas dry-run validadas`).

### 7.5. Patrón de Edición Granular y Micro-Bucle en Shard Author shard_03 (42 Turnos)
- **Comportamiento Atípico:** Shard 03 consumió **42 turnos**, ejecutando 5 operaciones consecutivas de edición granular (`replace_file_content`), 10 lecturas de inspección de código sobre el validador `compile_shard.py` y 3 corridas de compilación (2 fallidas, 1 exitosa).
- **Causa Raíz:**
  1. En el Turno 41, sufrió un `SyntaxError` en Python (`Línea 24: f-string: single '}' is not allowed`) por el uso de llaves triples `{{{lam1}} t}`.
  2. En el Turno 61, tras corregir las llaves, la compilación en sandbox falló con `[TPL-DRY: FALLO EN EJECUCIÓN DRY-RUN]` debido a un `NameError: name 'X' is not defined` en la expresión de dinámica no lineal $\\dot{X} = f(X)$.
  3. El subagente realizó múltiples lecturas de `compile_shard.py` para entender la lógica de validación de cuotas (`TPL-VAR`) antes de corregir la variable y finalizar con éxito en el Turno 75.
- **Paradoja de Rendimiento:** A pesar de haber realizado el doble de turnos que los demás agentes, Shard 03 completó su trabajo en **579.0s (9.65 min)**, resultando más rápido que Shard 02 (785s) y Shard 04 (603s). Esto demuestra que en arquitecturas agénticas, los turnos rápidos con modificaciones quirúrgicas son significativamente más eficientes en tiempo de pared que turnos lentos de reescritura monolítica.

### 7.6. Rendimiento Global y Pase Limpio de Validación
- **Construcción y Verificación Impecables:**
  - Stage 4 (`--stage build`): Compiló las 13 plantillas en **3.67s**, generando **320 preguntas interactivas** sin errores estructurales.
  - Stage 5 (`--stage verify`): Validó los 320 reactivos en **2.43s**, confirmando integridad léxica, balance de opciones y cobertura matemática.
  - Stage 5B (`--stage judge-compare`): Los 3 Blind Judges ratificaron el 100% de las 26 preguntas auditadas en **0.06s** de procesamiento CLI tras su evaluación epistémica.
  - Stage 6 (`--stage publish`): Emitió `courses/practica_parcial_saul_standard_coarse.json` (320 preguntas) y el informe pedagógico en **1.76s**.
- **Unit Economics Sobresalientes:**
  - Throughput de producción: **9.75 preguntas por minuto** (ritmo de pared: 6.16 s/pregunta).
  - Aceleración por concurrencia multi-agente: **3.33x** (tiempo de cómputo acumulado: 109.33 min vs tiempo de pared: 32.83 min).
  - Tasa de reuso de caché de contexto de API: **86.1%** (18,202,590 tokens leídos de caché vs 2,926,179 tokens activos).

### 7.7. Recomendaciones Accionables de Optimización para el Pipeline C2C
1. **Blindaje de Prompts de Autoría contra Escapes de LaTeX y Colisión de Llaves:**
   - Incorporar en el *system prompt* de `c2c_shard_author` la directiva explícita de declarar variables matemáticas usando notación simple `$c_1$` o interpolación formateada previa en Python, prohibiendo el uso de triples llaves `{{{var}}}` en f-strings y exigiendo cadenas crudas `r"..."` con placeholders limpios.
2. **Eliminación del Chequeo Especulativo de Pre-Existencia:**
   - Los autores ejecutaron 4 llamadas erróneas a `view_file` buscando archivos `shard_XX_data.py` antes de haberlos creado. Modificar el prompt del autor para indicar claramente que el archivo no existe al inicio y debe ser creado directamente mediante `write_to_file`.
3. **Partición Dinámica Asimétrica para Competencias de Alta Densidad Matemática:**
   - Shards con temas avanzados de Ecuaciones en Derivadas Parciales (EDP) o sistemas dinámicos matriciales 2D no lineales deben asignarse a razón de **1 competencia por shard** en lugar de 2. Esto distribuirá la carga de inferencia LLM y abatirá el straggler de 13 minutos a ~6 minutos.
4. **Normalización del Etiquetado de Blind Judges en el Recolector de Telemetría:**
   - Corregir el mapeador en `telemetry_collector.py` y `audit_engine.py` para asignar explícitamente `"category": "judge"` y `"label": "Blind Judge XX"` a los subagentes desplegados en Stage 5B, evitando que queden catalogados como `generic / Subagent` en las tablas de resumen.

---
*Reporte forense enriquecido con auditoría de causa raíz (c2c-run-auditor v3.2).*