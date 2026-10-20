# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Practica Parcial Saul Standard (`practica_parcial_saul_standard`)

**Fecha de Auditoría:** `2026-10-20 03:37:15 UTC`  
**Conversación Orquestadora:** [`f9b9d459-d84a-4e3d-bf32-48e74d8b5c5a`](conversation://f9b9d459-d84a-4e3d-bf32-48e74d8b5c5a)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\practica_parcial_saul_standard\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `7 archivos` (103 págs / 10.39 MB) | MATH_IV_Problem_Set_I.pdf, MATH_IV_Problem_Set_II_2026_II.pdf, MATH_IV_Problem_Set_III_2026_II.pdf, TEMA 1 (EDP SAÚL) 2.pdf, TEMA 2 (APLICACIONES ECONOMICAS).pdf, TEMA 2 (S'EDOS I ).pdf, TEMA 2 (S'EDOS II).pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`65 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`11 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`30 subagentes`** | Visión (0), CTA (7), Autores (11), Jueces (11) |
| **Reactivos Finales Validados** | **`1590 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`4,144,071` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`1,436,374` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`64,952,056` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`6,491,590` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`71,443,646` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`44,933.1 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`4,082.8 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`1,099,133.0 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`52,438.2 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`693,627.6 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`2.42 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`24.76 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`3.92x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `f9b9d459`):** `8 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-10-19 07:45:47` | `4.21s` | `0` (`0` act) | 0 | `—` |
| **`01_cta`** | `2026-10-19 07:57:54` | `0.53s` | `4,093,145` (`1,055,592` act) | 8 | `competencies=65` |
| **`02_shard`** | `2026-10-19 07:58:00` | `0.03s` | `0` (`0` act) | 0 | `shards=11` |
| **`03_templates`** | `2026-10-19 08:31:48` | `92.77s` | `36,420,851` (`3,408,481` act) | 11 | `count=65` |
| **`04_build`** | `2026-10-19 08:32:23` | `15.85s` | `0` (`0` act) | 0 | `total_questions=1590` |
| **`05_verify`** | `2026-10-19 08:33:06` | `10.86s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\practica_parcial_saul_standard\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-10-19 08:40:28` | `0.2s` | `2,390,558` (`1,113,567` act) | 11 | `passed=True` |
| **`06_publish`** | `2026-10-19 08:40:44` | `6.77s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\practica_parcial_saul_standard.json` |

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
- **Tiempo de Pared Fase Mappers (Máximo):** **`558.0s`** (determinado por `Cognitive Task Analysis Architect part_07`)
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`0.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`558.0s`** (`9.3 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cognitive Task Analysis Architect part_04** | Mapper | 7 | 134,873 | 46,869 | 226,260 | 0 | **445.0s** |
| **Cognitive Task Analysis Architect part_07** | Mapper | 12 | 122,094 | 68,274 | 657,013 | 1 | **558.0s** |
| **Cognitive Task Analysis Architect part_05** | Mapper | 9 | 116,398 | 36,886 | 260,886 | 0 | **291.0s** |
| **Cognitive Task Analysis Architect part_06** | Mapper | 20 | 111,994 | 43,951 | 1,244,068 | 1 | **496.0s** |
| **Cognitive Task Analysis Architect part_03** | Mapper | 8 | 96,752 | 37,283 | 208,662 | 0 | **250.0s** |
| **Cognitive Task Analysis Architect part_02** | Mapper | 8 | 60,049 | 26,733 | 233,995 | 0 | **207.0s** |
| **Cognitive Task Analysis Architect part_01** | Mapper | 7 | 64,841 | 35,750 | 199,541 | 0 | **259.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `11 shards concurrentes`
- **Duración Mínima de Shard:** `355.0s` | **Mediana:** `570.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`1426.0s`** (`23.8 min`) por `Shard Author shard_05`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+856.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`52,438.2 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_03** | `Hab-06, C-05, Hab-07, Hab-08 (+2)` | 6 | 178,161 | 96,577 | 2,927,278 | 274,738 | **45,789.7** | 28 | 2 | **713.0s** |
| **Shard Author shard_10** | `H-10, C-23, Hab-24, Hab-25 (+2)` | 6 | 96,339 | 49,083 | 485,044 | 145,422 | **24,237.0** | 10 | 1 | **355.0s** |
| **Shard Author shard_01** | `C-01, Hab-01, Hab-02, H-01 (+2)` | 6 | 155,485 | 63,363 | 2,271,072 | 218,848 | **36,474.7** | 27 | 4 | **570.0s** |
| **Shard Author shard_06** | `C-13, Hab-13, C-14, Hab-14 (+2)` | 6 | 328,588 | 82,149 | 3,233,550 | 410,737 | **68,456.2** | 31 | 4 | **564.0s** |
| **Shard Author shard_07** | `Hab-16, C-15, Hab-17, C-16 (+2)` | 6 | 148,194 | 78,002 | 1,308,691 | 226,196 | **37,699.3** | 15 | 1 | **488.0s** |
| **Shard Author shard_08** | `H-08, Hab-19, C-18, H-09 (+2)` | 6 | 267,978 | 100,631 | 6,916,378 | 368,609 | **61,434.8** | 45 | 2 | **841.0s** |
| **Shard Author shard_02** | `H-02, C-03, Hab-04, C-04 (+2)` | 6 | 313,496 | 80,915 | 4,760,437 | 394,411 | **65,735.2** | 45 | 6 | **682.0s** |
| **Shard Author shard_05 🛑** | `H-06, C-10, C-11, Hab-11 (+2)` | 6 | 561,272 | 177,698 | 6,233,114 | 738,970 | **123,161.7** | 62 | 8 | **1426.0s** |
| **Shard Author shard_09** | `C-19, Hab-22, C-20, Hab-23 (+2)` | 6 | 169,038 | 78,969 | 2,096,088 | 248,007 | **41,334.5** | 23 | 2 | **631.0s** |
| **Shard Author shard_04** | `C-06, C-07, C-08, H-05 (+2)` | 6 | 141,252 | 57,397 | 1,624,320 | 198,649 | **33,108.2** | 22 | 4 | **443.0s** |
| **Shard Author shard_11** | `C-24, Hab-28, C-25, H-11 (+1)` | 5 | 129,194 | 54,700 | 1,156,398 | 183,894 | **36,778.8** | 20 | 2 | **388.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ❌ NO PASARON AL PRIMER INTENTO (REQUIRIÓ INTERVENCIONES)  
> Los blind judges y la verificación psicométrica registraron discrepancias que requirieron correcciones. La validación previa operó con 1 errores iniciales, requiriendo rondas de auto-reparación o intervención técnica.

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `130 reactivos` (65 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `11 jueces` | Aislamiento epistémico en Stage 5 |
| **Resultado al Primer Intento** | **`❌ Falló al primer intento`** | 1 violaciones iniciales registradas |
| **Iteraciones de Auto-Reparación** | `1 iteraciones` en sandbox | 1 iteraciones ejecutadas |
| **Intervenciones del Supervisor** | 🛠️ `3 operaciones directas` | 3 ediciones registradas |

#### Detalle de Acciones Registradas:
- 1. **Bucle de Auto-Reparación**: Se ejecutó RepairLoop sobre el lote de evaluación.
- 2. **Intervenciones de Supervisor (3 operaciones)**: Operaciones sobre `assemble.py`, `circuit_breaker_Hab-12.json`, `compile_shard_05.json`.
- 3. **Certificación y Verificación Final**: Se concluyó la validación tras 1 iteraciones sobre el lote de 130 reactivos.

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared del Orquestador:** `64.22 min` (`3853.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `12.9 min` (`775.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.5 min`** (`28.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `1.1 min` (`64.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `3.2 min` (`191.0s`)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
Operaciones directas de edición de código ejecutadas por el orquestador: **`3`**

| Paso | Archivo Afectado | Tipo de Acción | Causa Raíz / Justificación Técnica | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **239** | `compile_shard_05.json` | Modificación / Script Auxiliar | "Reset circuit breaker attempt count for shard_05" | `write_to_file` | 3,025 |
| **241** | `circuit_breaker_Hab-12.json` | Modificación / Script Auxiliar | "Reset circuit breaker for Hab-12" | `write_to_file` | 2,617 |
| **307** | `assemble.py` | Parche de Infraestructura Core | "Guard frac_den_fix and script_outer_fix so they only run when curly braces are actually u | `replace_file_content` | 3,692 |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [HIGH] Síndrome del Orquestador Reparador (3 intervenciones manuales)
- **Ámbito:** `Director (Orchestrator)`
- **Diagnóstico:** El orquestador principal ejecutó 3 operaciones directas de edición de código y plantillas. Consumió más de 9,334 tokens en turnos de mantenimiento/recuperación manual.

### 🛑 [HIGH] Straggler Crítico en Shards: Shard Author shard_05
- **Ámbito:** `Stage 3: Question Authoring`
- **Diagnóstico:** Shard Author shard_05 tardó 1426.0s frente a la mediana de 570.0s (+856.0s de retraso en la barrera). Determinó el tiempo total de pared de la etapa de autoría.

### 🛑 [HIGH] Antipatrón de Micro-Bucle Interactivo (62 turnos en Shard Author shard_05)
- **Ámbito:** `Shard Author shard_05`
- **Diagnóstico:** 4 subagentes realizaron > 30 turnos individuales (ej. Shard Author shard_05 con 62 turnos). Ocurre por bucles de depuración o escritura incremental en lugar de redactar por lotes atómicos.

### ⚠️ [MEDIUM] Fricción de Herramientas en 5 subagentes
- **Ámbito:** `Multiple Subagents`
- **Diagnóstico:** Subagentes como Shard Author shard_01 acumularon fallos en consola (4 errores), provocando reintentos e invalidación de caché.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `326 turnos`
- **Volumen Total de Razonamiento:** `955,026 caracteres`
- **Razonamiento del Orquestador:** `59 turnos` (19,721 chars)
- **Razonamiento de Subagentes:** `267 turnos` (935,305 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Subagent** | 5 | 2,342 | 0 |
| **Cognitive Task Analysis Architect part_04** | 6 | 28,483 | 0 |
| **Cognitive Task Analysis Architect part_07** | 8 | 33,562 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_05** | 6 | 32,152 | 0 |
| **Cognitive Task Analysis Architect part_06** | 14 | 30,391 | ⚠️ 1 |
| **Cognitive Task Analysis Architect part_03** | 5 | 28,685 | 0 |
| **Cognitive Task Analysis Architect part_02** | 6 | 19,606 | 0 |
| **Cognitive Task Analysis Architect part_01** | 5 | 27,889 | 0 |
| **Shard Author shard_03** | 14 | 56,816 | ⚠️ 2 |
| **Shard Author shard_10** | 6 | 31,813 | ⚠️ 1 |
| **Shard Author shard_01** | 18 | 42,832 | ⚠️ 4 |
| **Shard Author shard_06** | 18 | 52,118 | ⚠️ 4 |
| **Shard Author shard_07** | 10 | 45,784 | ⚠️ 1 |
| **Shard Author shard_08** | 24 | 61,818 | ⚠️ 2 |
| **Shard Author shard_02** | 14 | 44,575 | ⚠️ 6 |
| **Shard Author shard_05** | 36 | 107,043 | ⚠️ 8 |
| **Shard Author shard_09** | 15 | 69,136 | ⚠️ 2 |
| **Shard Author shard_04** | 14 | 36,303 | ⚠️ 4 |
| **Shard Author shard_11** | 9 | 31,498 | ⚠️ 2 |
| **Blind Judge 01** | 3 | 8,427 | 0 |
| **Blind Judge 02** | 3 | 8,978 | 0 |
| **Blind Judge 03** | 3 | 22,066 | 0 |
| **Blind Judge 04** | 3 | 32,356 | ⚠️ 1 |
| **Blind Judge 05** | 3 | 12,973 | 0 |
| **Blind Judge 06** | 3 | 10,829 | 0 |
| **Blind Judge 07** | 3 | 10,062 | 0 |
| **Blind Judge 08** | 3 | 8,443 | ⚠️ 1 |
| **Blind Judge 09** | 3 | 13,589 | ⚠️ 1 |
| **Blind Judge 10** | 4 | 12,578 | 0 |
| **Blind Judge 11** | 3 | 12,158 | ⚠️ 1 |

---

---

## 7. Diagnóstico Forense de Causa Raíz y Optimización Agéntica

### 7.1. Verificación de Aislamiento Estricto Zero-Collision (Garantía C2C v3.2)
- **Validación de Identidad de Corrida:** Confirmada de extremo a extremo contra la conversación [`f9b9d459-d84a-4e3d-bf32-48e74d8b5c5a`](conversation://f9b9d459-d84a-4e3d-bf32-48e74d8b5c5a).
- **Directorio de Trabajo (`work/state.json`):** `conversation_id = "f9b9d459-d84a-4e3d-bf32-48e74d8b5c5a"`, `course_id = "practica_parcial_saul_standard"`, etapa final `publish` (`completed`).
- **Snapshots de Telemetría (`work/telemetry/*.json`):** Las 8 etapas emitidas (`00_prepare`, `01_cta`, `02_shard`, `03_templates`, `04_build`, `05_verify`, `05b_judge_compare`, `06_publish`) poseen estampado idéntico e inviolable de `conversation_id`.
- **Espejo Persistente:** Verificado en `work/telemetry/by_conversation/f9b9d459-d84a-4e3d-bf32-48e74d8b5c5a/`. Se certifica 0% de interferencia o colisión con corridas previas o posteriores en el mismo espacio de trabajo (p. ej. `acdc402d`, `afb5aa18`, `a53e6af1`).

---

### 7.2. Causa Raíz del Straggler Crítico: Shard Author 05 (1426.0s / 23.8 min, 62 turnos, 8 errores)
El subagente `Shard Author shard_05` representó el cuello de botella más severo de toda la ejecución, excediendo la mediana de los shards (570.0s) en **+856.0s** (+150.2%) e imponiendo una latencia ociosa en la barrera síncrona de Stage 3:
1. **Contenido Pedagógico Problemático:** Asignado a 6 competencias: `H-06`, `C-10`, `C-11`, `Hab-11`, `Hab-12` y `C-12`. La competencia desencadenante fue **`Hab-12`** (Resolución de Ecuaciones Diferenciales Parciales de primer orden lineales y homogéneas mediante el método de separación de variables).
2. **Defectos de Balance KaTeX en Cadenas Dinámicas:** Al parametrizar la solución general $u(x, y) = X(x)Y(y) = C e^{k(x + y/a)}$, el autor generó expresiones con fracciones anidadas dentro de exponentes (`rf"$u(x, y) = C e^{{k \left( x + \frac{{y}}{{{a}}} \right)}}..."$`), incurriendo en desbalances de llaves (`R-20: SINTAXIS / LLAVES`).
3. **Micro-Bucle de Validación y Agotamiento de Cuota:** El autor ejecutó **8 intentos de compilación** (`compile_shard.py`), registrando fallos masivos en cascada (`FAIL: 17 errores`, luego `FAIL: 9 errores` y `FAIL: 14 errores`).
4. **Fricción de Consola CLI:** En el turno 104, el subagente intentó modificar la configuración del buffer de PowerShell invocando `$Host.UI.RawUI.BufferSize = New-Object System.Management.Automation.Host.Size(500, 100)`, lo que provocó un fallo no recuperable de sintaxis en el entorno host de Windows.
5. **Disparo del Circuit Breaker:** Al alcanzar el intento 7 de 6 (`[COMPILE 7/6] Límite de compilaciones alcanzado para shard 'shard_05'`), el compilador abortó la ejecución y disparó el disyuntor en `.check_attempts/circuit_breaker_Hab-12.json`. El subagente quedó bloqueado y se vio forzado a enviar un mensaje de auxilio (`send_message`) al orquestador en el turno 122.

---

### 7.3. Auditoría Forense de las 3 Intervenciones Manuales del Orquestador
El orquestador ejecutó 3 intervenciones directas sobre archivos del sistema para desbloquear el pipeline:

| Operación | Paso / Registro | Archivo Intervenido | Herramienta | Causa Raíz Subyacente | Razonamiento Previo (`thinking`) del Modelo |
| :---: | :---: | :--- | :---: | :--- | :--- |
| **1** | Paso 239 (Reg 276) | `work/.check_attempts/compile_shard_05.json` | `write_to_file` | Shard 05 agotó los 6 intentos permitidos de compilación tras continuos fallos sintácticos en `Hab-12`. | `"Initial hypothesis: 'compile_shard.py's behavior needs to be re-evaluated due to a code change in 'shard_05_data.py'. To ensure a clean slate, resetting the state of related JSON files is necessary. This will ensure no lingering states interfere with the test. Applying the reset requires writing to a file, overwriting its existing content."` |
| **2** | Paso 241 (Reg 278) | `work/.check_attempts/circuit_breaker_Hab-12.json` | `write_to_file` | El disyuntor persistente de `Hab-12` bloqueaba cualquier invocación subsiguiente de `compile_shard.py`. Se reescribió con `{"consecutive_count": 0, "last_hash": "", "history": []}`. | Complementario a la intervención 1: Garantizar un reset atómico de los hashes de intento previos para permitir que el compilador reevaluara la corrección aplicada por el autor. |
| **3** | Paso 307 (Reg 344) | `.agents/skills/content-to-course/engine/assemble.py` (L250-264) | `replace_file_content` | **Defecto en el Core del Engine C2C:** Las expresiones regulares `frac_den_fix` y `script_outer_fix` en `sanitize_katex_syntax` operaban incondicionalmente. En fórmulas balanceadas con delimitadores `\left(` y `\right)` dentro de exponentes o fracciones (ej. `$u(x,y)=Ce^{k\left(x+\frac{y}{a}\right)}$`), `script_outer_fix` cerraba prematuramente la llave antes de `\right)`, corrompiendo fórmulas válidas. | `"Examining the code, a pattern emerges: the system attempts to auto-repair missing closing braces in LaTeX fractions... The script_outer_fix regex mistakenly closes the superscript when encountering \right), because the superscript's closing brace is further along in the equation... The auto-repair function should only insert a closing brace if there are more opening than closing braces... The code's logic is flawed as it unconditionally inserts the closing brace. The correct behavior demands that the auto-repair should only run when the number of opening braces exceeds the number of closing braces."` |

---

### 7.4. Comportamiento y Evaluación Forense de Blind Judges (Stage 5 / 5b)
- **Aislamiento Epistémico Ciego:** 11 subagentes evaluaron en paralelo 130 reactivos estratificados (2 por competencia) sin acceso a claves ni retroalimentación.
- **Métricas Registradas:** 128 acuerdos y 2 desacuerdos (**`agreement_rate = 98.46%`**). El pipeline dictaminó **`PASSED`** (superando el umbral mínimo operativo de 95.0%).
- **Causa Raíz de los 2 Desacuerdos:**
  * Ítems afectados: `T-H-10_judge_1` (competencia `H-10`, polinomio característico) y `T-Hab-21_judge_1` (competencia `Hab-21`, sistemas lineales con raíces complejas).
  * Veredicto emitido por el Juez: `BLOCKED: Reactivo carece de contexto matemático autosuficiente`.
  * Razón técnica: El exportador de lotes para jueces (`judge_batch.json`) omitió incluir la matriz $A$ o el sistema diferencial de origen en el campo `stem` del ítem ciego. Al recibir solo las opciones de autovalores o combinaciones lineales sin el enunciado completo del problema, el juez se negó a adivinar y aplicó la política de bloqueo prudencial.
- **Aclaración del Dictamen en Auditoría Automática:** El reporte determinista reportó inicialmente que no pasaron en primera instancia porque `audit_engine.py` utiliza una condición booleana estricta `agreement_rate == 1.0` (acuerdo perfecto al 100%). En la ejecución real, **no se requirió ningún bucle de reparación (`c2c_repair`) ni intervención humana en Stage 5**, aprobándose el lote para publicación inmediata.

---

### 7.5. Erradicación Total de Errores de Caja Negra (0% en Categorías Genéricas)
Los **61 errores** detectados en el transcript se encuentran desglosados en 10 categorías técnicas precisas:
1. **Missing File / Relative Path / Directory Error (18 errores):** 14 llamadas de subagentes (particularmente jueces y autores) pasaron `ContentOffset` mayor al tamaño del archivo en archivos de trabajo pequeños de < 8 KB; 4 exploraciones de rutas relativas por el orquestador.
2. **Parameter Diversity & Option Collapse (11 errores):** Fallos detectados durante compilación preliminar (`compile_shard.py`) por colapso de opciones distractoras en fórmulas algebraicas (4 de ellos en Shard 05).
3. **Exploratory Python One-Liner / Script Exceptions (9 errores):** Pruebas de consola del orquestador (`python -c`) con sintaxis no compatible antes de afinar los filtros regex de KaTeX.
4. **Shard Compilation & Template Validator Failure (9 errores):** Fallos sintácticos en archivos `shard_XX_data.py` (ej. comas faltantes o llaves no cerradas) y disparo de circuit breakers.
5. **Python Environment / Virtualenv / Encoding Discrepancy (4 errores):** Intentos fallidos de importar módulos locales sin ajustar `sys.path`.
6. **File Edit / Write Tool Target Mismatch (4 errores):** Fallos de coincidencia de cadenas de texto en `replace_file_content` ejecutados por Shard 02 y Shard 04.
7. **Non-Zero CLI Exit / Subprocess Probe (2 errores):** Intentos del orquestador de invocar `define_subagent` para tipos de agentes que ya habían sido instanciados previamente.
8. **LaTeX Control Character / Raw-String Corruption (2 errores):** Ocurrencias de secuencias de escape no declaradas con prefijo `r"..."` en Shard 04 y Shard 07.
9. **CTA Compilation & Schema Errors (1 error):** Validación inicial fallida de esquema DAG en Stage 1B.
10. **PowerShell Command / Quoting / $Variable Expansion Friction (1 error):** Invocación de comando de configuración de buffer no soportado en el host.

---

### 7.6. Síntesis Forense Comparativa Longitudinal (Matriz de las 5 Corridas Recientes)

| Corrida / Run ID | Curso Auditado | Págs | Comps | Preguntas | Pared (min) | Tokens/Preg | Seg/Preg | Throughput (QPM) | Eficiencia Arquitectónica |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `20261019_223707_..._afb5aa18` | `practica_parcial_coarse_v2` | 103 | 14 | 370 | 60.03 | 160,187 | 9.74 | 6.16 | 🛑 Muy baja: Granularidad gruesa con severo desperdicio de tokens |
| **`20261019_223715_..._f9b9d459` (TARGET)** | **`practica_parcial_standard`** | **103** | **65** | **1,590** | **64.22** | **44,933** | **2.42** | **24.76** | **✅ Óptima: Excelente equilibrio de unit economics y granularidad** |
| `20261019_223720_..._a53e6af1` | `practica_parcial_coarse` | 103 | 13 | 320 | 32.83 | 66,027 | 6.16 | 9.74 | ⚠️ Moderada: Rápida pero baja densidad psicométrica |
| `20261019_223729_..._acdc402d` | `practica_parcial_saul` | 103 | 118 | 2,850 | 85.65 | 36,040 | 1.80 | 33.27 | ⚡ Ultra-alta producción unitaria, pero saturación de tokens totales (>102M) |
| `20261019_223736_..._4ceacf92` | `solow_model_v15` | 36 | 15 | 360 | 27.10 | 61,291 | 4.52 | 13.28 | ✅ Consistente: Corrida estándar de referencia teórica |

**Hallazgos Clave de la Comparativa:**
- **La granularidad estándar (65 competencias) demostró ser el *sweet spot* del pipeline:** Logra un rendimiento industrial de **24.76 preguntas/minuto** y un tiempo unitario de **2.42 s/pregunta**, frente a los ineficientes **9.74 s/pregunta** del enfoque de grano grueso (`afb5aa18`).
- **Impacto del Straggler:** Si Shard 05 hubiera operado en la mediana de los shards (9.5 min en lugar de 23.8 min), el tiempo total de pared de la corrida habría descendido de 64.2 min a ~50.0 min, reduciendo los segundos por pregunta a **1.88 s/preg**.

---

### 7.7. Recomendaciones Accionables de Optimización para el Pipeline C2C
1. **Pre-validación AST de KaTeX en Subagentes Autores (Eliminación de Micro-bucles):** Incorporar en el template base de `c2c_shard_author` un script de linting estático previo que valide balance de llaves KaTeX antes de invocar `compile_shard.py`, evitando agotar el límite de intentos (6) y previniendo el disparo del circuit breaker.
2. **Guarda Definitiva en `engine/assemble.py`:** Integrar de forma permanente en el código fuente del skill la guarda `if text.count("{") > text.count("}"):` antes de aplicar cualquier regex de auto-cierre de llaves en exponentes o fracciones (`frac_den_fix`, `script_outer_fix`), asegurando que jamás se modifiquen fórmulas que ya se encuentran balanceadas.
3. **Autosuficiencia Contextual en Lotes de Blind Judges (`judge_batch.json`):** Modificar la rutina de serialización en Stage 5 para que copie obligatoriamente los objetos matemáticos base (matrices de coeficientes, ecuaciones diferenciales completas) dentro del campo de texto de la pregunta ciega, evitando que los jueces clasifiquen ítems como `BLOCKED`.
4. **Instrucción de Lectura Paginada en Prompts de Jueces:** Actualizar el system prompt de `c2c_judge` instruyendo explícitamente no enviar `ContentOffset` a menos que se reciba un error de truncamiento previo, eliminando 14 errores innecesarios de ejecución de herramientas.
5. **Idempotencia en Registro de Agentes (`define_subagent`):** Envolver la llamada `define_subagent` en el orquestador con verificación de existencia previa para evitar excepciones de `agent already exists`.

---
*Reporte forense enriquecido emitido por `c2c-run-auditor` (Paso B Agéntico).*
