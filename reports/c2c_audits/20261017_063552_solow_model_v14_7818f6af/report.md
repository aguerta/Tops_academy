# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Solow Model V14 (`solow_model_v14`)

**Fecha de Auditoría:** `2026-10-17 11:35:52 UTC`  
**Conversación Orquestadora:** [`7818f6af-4344-4f6c-8f01-24ecdf14c583`](conversation://7818f6af-4344-4f6c-8f01-24ecdf14c583)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\solow_model_v14\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `2 archivos` (36 págs / 1.49 MB) | 05_15_07_El_modelo_de_crecimiento_de_Solow.pdf, solow1956.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`23 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`4 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`10 subagentes`** | Visión (0), CTA (2), Autores (4), Jueces (4) |
| **Reactivos Finales Validados** | **`540 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`2,847,511` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`670,644` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`39,999,846` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`4,765,328` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`44,765,174` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Bruto (Registrado) | Valor Activo Neto (Forense) | Interpretación de Eficiencia |
| :--- | :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`82,898.5 tokens/preg`** | **`82,898.5 tokens/preg`** | Esfuerzo de API por reactivo (inflado por 18.1M en Shard 04 y 9.7M en doble CTA) |
| **Tokens Activos por Pregunta** | **`8,824.7 tokens/preg`** | **`8,824.7 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`1,946,311.9 tokens/comp`** | **`1,946,311.9 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`112,932.8 tokens/comp`** | **`112,932.8 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`1,243,477.1 tokens/pág`** | **`1,243,477.1 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`36.65 s/preg`** | **`8.96 s/preg`** | Bruto incluye 4.09h de pausa/suspensión; neto refleja el ritmo activo real |
| **Rendimiento de Generación (QPM)** | **`1.64 preg/min`** | **`6.70 preg/min`** | Velocidad de producción activa del pipeline de autoría |
| **Factor de Aceleración Paralela** | **`1.3x`** | **`5.3x`** | Aceleración paralela real (25,659s cómputo / 4,838s pared activa) |

> [!NOTE]
> **Descomposición Forense de Pared (Gross vs. Net Active):**  
> El tiempo total bruto registrado de `329.87 min` (19,792 s) contiene una **ventana de inactividad/suspensión del sistema de 4 horas, 9 minutos y 14 segundos (14,954 s, 75.6% del tiempo total)** entre la finalización de `05_verify` (`07:03:41 UTC` / `02:03:41 local`) y la reanudación del orquestador en `11:12:55 UTC` (`06:12:55 local`). El **tiempo neto activo del pipeline fue de 80.64 min (4,838 s)**, alcanzando un factor de aceleración concurrente real de **`5.3x`** frente al cómputo total acumulado.

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `7818f6af`):** `8 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-10-17 05:52:22` | `2.92s` | `0` (`0` act) | 0 | `—` |
| **`01_cta`** | `2026-10-17 06:28:47` | `0.11s` | `9,692,174` (`718,010` act) | 2 | `competencies=23` |
| **`02_shard`** | `2026-10-17 06:28:52` | `0.01s` | `0` (`0` act) | 0 | `shards=4` |
| **`03_templates`** | `2026-10-17 07:03:14` | `43.24s` | `26,362,668` (`2,597,455` act) | 4 | `count=23` |
| **`04_build`** | `2026-10-17 07:03:29` | `8.48s` | `0` (`0` act) | 0 | `total_questions=540` |
| **`05_verify`** | `2026-10-17 07:03:41` | `4.23s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\solow_model_v14\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-10-17 11:20:47` | `0.01s` | `432,236` (`200,276` act) | 4 | `passed=True` |
| **`06_publish`** | `2026-10-17 11:21:12` | `2.88s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\solow_model_v14.json` |

---

### 3.1. Stage 1A: Preprocesamiento de Visión
- **Subagentes de Visión Desplegados:** `0 agentes en paralelo`
- **Tiempo de Pared de la Etapa (Máximo / Critical Path):** **`0.0s`** (`0.0 min`)
- **Agente Determinante del Camino Crítico:** `N/A`

| Subagente de Visión | Turnos | Tokens In | Tokens Out | Cache Leído | Total Activo | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |

---

### 3.2. Stage 1B: Análisis Cognitivo de Competencias (CTA)
- **Arquitectura:** `DIRECT (2 Direct CTA Architects secuenciales por fallo de ejecución)`
- **Tiempo de Pared Fase Mappers (Máximo):** **`0.0s`** (modalidad direct)
- **Tiempo Fase Harmonizer / Direct:** **`2004.0s`** (`33.4 min` acumulados: CTA 1 = 1016.0s + CTA 2 = 988.0s)
- **Tiempo de Pared Total de Etapa 1B:** **`2004.0s`** (`33.4 min`)

| Subagente CTA | ID Conversación | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración | Estado Final / Diagnóstico Forense |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Direct CTA Architect 1** | `517d984d` | Direct Architect | 47 | 380,775 | 86,338 | 4,904,213 | 2 | **1016.0s** | 💥 **Fallo/Abrupt Exit:** Agotó turnos (step 94); dejó `cta_data.py` con 20 errores KaTeX. |
| **Direct CTA Architect 2** | `c2a69d5f` | Direct Architect | 42 | 178,034 | 75,277 | 4,233,667 | 5 | **988.0s** | ✅ **Recuperación Exitosa:** Corrigió 20 errores de delimitadores KaTeX y compiló `cta.json`. |

> [!WARNING]
> **Causa Raíz de Doble Despliegue en CTA:**  
> CTA Architect 1 redactó 1400+ líneas en `cta_data.py`, pero incurrió en omisión sistemática de delimitadores `$...$` en expresiones KaTeX y warnings de escape `\p`. Al alcanzar el turno 47 (paso 94), el subagente abortó por agotamiento de turnos/contexto. El orquestador detectó la terminación anómala vía mensaje del sistema (`55107a8f`) y re-despachó a CTA Architect 2. Este último heredó el archivo `cta_data.py`, corrigió quirúrgicamente los 20 errores sintácticos mediante `replace_file_content` y certificó las 23 competencias a las 06:28:40 UTC.

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `4 shards concurrentes`
- **Duración Mínima de Shard:** `396.0s` | **Mediana:** `708.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`1902.0s`** (`31.7 min`) por `Shard Author shard_04`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+1194.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`112,932.8 tokens/competencia`**

| Shard ID | ID Conv | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_01** | `684e5d32` | `H-01, C-01, Hab-01, C-02 (+2)` | 6 | 295,096 | 73,931 | 2,049,905 | 369,027 | **61,504.5** | 33 | 2 | **522.0s** (8.7m) |
| **Shard Author shard_02** | `175b9cb1` | `Hab-03, H-02, C-04, Hab-04 (+2)` | 6 | 166,851 | 56,422 | 2,072,056 | 223,273 | **37,212.2** | 26 | 2 | **396.0s** (6.6m) |
| **Shard Author shard_03** | `d3978b24` | `C-07, Hab-05, Hab-06, C-08 (+2)` | 6 | 204,260 | 103,152 | 3,192,693 | 307,412 | **51,235.3** | 35 | 6 | **708.0s** (11.8m) |
| **Shard Author shard_04 🛑** | `7af766a2` | `C-09, Hab-08, C-10, C-11 (+1)` | 5 | 1,479,702 | 218,041 | 16,450,559 | 1,697,743 | **339,548.6** | 131 | 8 | **1902.0s** (31.7m) |

> [!CAUTION]
> **Autopsia Causal del Straggler Crítico (`shard_04` — 31.7 min, 131 turnos, 18.15M tokens):**  
> 1. **Fricción Inicial de Herramienta CLI:** En turnos 20-24, invocó `compile_shard.py` sin `--shard` y sin `--manifest`, recibiendo salidas de error no informativas.  
> 2. **Falla de I/O en Windows (`write_to_file`):** En turno 34, el SDK arrojó `read ... shard_04_data.py: Incorrect function`, requiriendo comandos PowerShell manuales de eliminación y re-escritura.  
> 3. **Cascada de 15 Errores Sintácticos (`task-44.log`):** Presencia de llaves dobles residuales `{{...}}` heredadas de f-strings en `C-09`, `Hab-08` y `C-12`, además de cuota de diversidad no alcanzada (TPL-VAR).  
> 4. **Trunca-Excepciones en `compile_shard.py` (Causa Raíz Principal):** En `task-78.log`, el compilador reportó `La ejecución en sandbox falló en 50/50 semillas evaluadas` pero **truncó la traza de excepción real (Traceback)**. El subagente quedó ciego ante el error exacto en `gen_c09` y `gen_hab08`.  
> 5. **Bucle de Ingeniería Inversa (91 `view_file` calls):** Al no ver la excepción, el subagente procedió a inspeccionar línea por línea el código fuente de `compile_shard.py` (líneas 1-120, 351-440, 440-505, 500-650, 650-750) y los JSONs de otros shards (`shard_01.json`).  
> 6. **Trampa de Circuit Breaker (`BUDGET HALT`):** El validador bloqueó la compilación tras 5 intentos fallidos (`Exceeded 5 validation cycles`), disparando búsquedas infructuosas de `.check_attempts/shard_04.json` (FileNotFoundError en pasos 169 y 171).  
> 7. **Certificación Final:** El subagente corrigió la lógica paramétrica de `PARAMS_HAB08`, eliminó las llaves conflictivas y superó la validación en `task-254.log` a las 07:02:25 UTC.

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen de Blind Judges:** ✅ 100% ACUERDO AL PRIMER INTENTO (46/46 REACTIVOS)  
> Los 4 Blind Judges evaluaron el lote estratificado de 46 reactivos en 1 turno de razonamiento puro cada uno (0 búsquedas web, 100% aislamiento epistémico), logrando un acuerdo psicométrico del 100.0% (46/46) con 0 discrepancias frente al ground truth.

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `46 reactivos` (23 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `4 jueces` | Aislamiento epistémico en Stage 5 |
| **Resultado al Primer Intento** | **`✅ 100% Limpio (Sin Discrepancias)`** | Sin discrepancias ni arbitraje necesario |
| **Iteraciones de Auto-Reparación** | `1 iteraciones` en sandbox | 0 requeridas |
| **Intervenciones del Supervisor** | 🛠️ `0 operaciones directas` | Ninguna (ejecución autónoma) |

#### Detalle de Acciones Registradas:
- 1. **Arbitraje Ciego (`05b_judge_compare.json`)**: 46/46 acuerdos (`100.0% agreement rate`, `0 discrepancias`).
- 2. **Verificación Determinista Previa (`--stage verify`)**: Detectó 1 error(es) léxico/estructural(es) corregido(s) antes del arbitraje ciego.

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared Bruto Registrado:** `329.87 min` (`19,792.0s`)
- 🛑 **Ventana de Suspensión / Inactividad del Sistema (Dead Time):** **`249.23 min`** (`14,954.0s`, **75.6% del tiempo bruto**)
  - *Inicio de Inactividad:* `07:03:41 UTC` (`02:03:41 local`) tras completarse `05_verify`.
  - *Reanudación:* `11:12:55 UTC` (`06:12:55 local`) al reactivarse la sesión de trabajo en el cliente.
  - *Causa Raíz:* Suspensión del equipo/sesión durante la madrugada. Durante este lapso no hubo consumo de tokens, cómputo LLM, procesos en segundo plano ni I/O.
- ⚡ **Tiempo de Pared Activo Real del Pipeline:** **`80.64 min`** (`4,838.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py` / `dispatch.py`):** `2.2 min` (`133.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`0.0 min`** (`0.0s`)
- ⏳ **Tiempo de Espera en Barreras de Subagentes (Esperando Finalización):** `76.6 min` (`4,594.0s` netos esperando a CTA 1, CTA 2, Shards 01-04 y Judges 01-04)
- 🧠 **Tiempo Real de Inferencia y Razonamiento del Orquestador:** **`1.85 min`** (`111.0s` netos en 81 turnos de API)

### 4.2. Catálogo de Errores e Incidencias en Turnos del Orquestador
Operaciones de edición manual de código por el orquestador: **`0`** (ejecución 100% no invasiva).  
Sin embargo, se registraron **2 errores de ejecución de comandos CLI** durante la fase de sondeo previo a los jueces:

| Paso / Turno | Herramienta | Comando Ejecutado | Causa Raíz / Justificación Técnica | Resultado / Impacto |
| :---: | :--- | :--- | :--- | :--- |
| **Paso 89** | `run_command` | `python -c "import inspect; from src.pipeline.verify import compare_judge_responses..."` | **Error de Asunción de Arquitectura:** Asumió erróneamente que C2C era un paquete Python instalable (`src.pipeline`) en lugar de scripts CLI planos en `.agents/skills/content-to-course/`. | `ModuleNotFoundError: No module named 'src.pipeline'` (Exit Code 1). Corregido en pasos posteriores leyendo `judge.py` y `run.py`. |
| **Paso 115** | `run_command` | `powershell -Command "Get-ChildItem -Path courses/solow_model_v14/work/verification ... \| Select-Object ..."` | **Fallo de Sintaxis / Escape de Comillas en PowerShell:** El pipe `\|` y el entrecomillado anidado provocaron un fallo de parseo en el subproceso. | Salida vacía con Exit Code 1. No afectó el flujo de trabajo; el orquestador alternó a `manage_subagents list`. |

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [CRITICAL] Trunca-Excepciones y Bucle de Ingeniería Inversa en Shard 04 (1902.0s, 131 turnos, 18.15M tokens)
- **Ámbito:** `Stage 3: Question Authoring (shard_04)`
- **Diagnóstico:** `compile_shard.py` silenció el traceback real de la excepción de sandbox (`La ejecución en sandbox falló en 50/50 semillas...` sin volcar el `traceback.format_exc()`). Al quedar a ciegas, el subagente ejecutó **91 operaciones `view_file`** leyendo el código interno de `compile_shard.py` (líneas 1-120, 351-750) y otros shards para adivinar el motivo de la falla.
- **Efecto Cascada:** Disparó la trampa de circuit breaker (`[!] BUDGET HALT on competency ... Exceeded 5 validation cycles`), consumiendo por sí solo el **40.5% de todos los tokens del curso**.

### 🛑 [HIGH] Caída Inesperada y Re-despacho Secuencial en CTA (2004.0s, 89 turnos, 9.69M tokens)
- **Ámbito:** `Stage 1B: Cognitive Task Analysis`
- **Diagnóstico:** CTA Architect 1 alcanzó 47 turnos (paso 94) y abortó abruptamente tras una cascada de 20 advertencias KaTeX y errores de escape `\p`. El orquestador tuvo que despachar un segundo CTA Architect (`c2a69d5f`), el cual tuvo que recomenzar la validación y edición granular de `cta_data.py` durante otros 42 turnos (988s), duplicando el tiempo y costo de la etapa.

### ⚠️ [HIGH] Contaminación del Wall-Clock por Suspensión del Host (249.23 min de Dead Time)
- **Ámbito:** `Infraestructura / Orquestación Longitudinal`
- **Diagnóstico:** El orquestador permaneció suspendido/ocioso entre las 07:03:41 UTC y las 11:12:55 UTC (madrugada local). El cálculo bruto de `c2c-run-auditor` reportó un tiempo de 5.5 horas y un speedup engañoso de `1.3x`, cuando el speedup concurrente neto real fue de **`5.3x`**.

### ⚠️ [MEDIUM] Fricción de I/O en Entornos Windows ("Incorrect function" en `write_to_file`)
- **Ámbito:** `SDK / File System I/O`
- **Diagnóstico:** En Shard 03 (paso 26) y Shard 04 (paso 34), llamadas a `write_to_file` arrojaron `read ... Incorrect function` al sobreescribir archivos recién creados, obligando a los subagentes a emitir comandos manuales `Remove-Item` vía PowerShell.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `162 turnos`
- **Volumen Total de Razonamiento:** `387,578 caracteres`
- **Razonamiento del Orquestador:** `20 turnos` (7,289 chars)
- **Razonamiento de Subagentes:** `142 turnos` (380,289 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect** | 13 | 19,758 | ⚠️ 2 |
| **Cognitive Task Analysis Architect** | 13 | 23,384 | ⚠️ 5 |
| **Shard Author shard_01** | 17 | 45,712 | ⚠️ 2 |
| **Shard Author shard_02** | 11 | 44,771 | ⚠️ 2 |
| **Shard Author shard_03** | 18 | 60,123 | ⚠️ 6 |
| **Shard Author shard_04** | 64 | 131,953 | ⚠️ 8 |
| **Blind Judge 01** | 1 | 13,380 | 0 |
| **Blind Judge 02** | 2 | 15,220 | 0 |
| **Blind Judge 03** | 2 | 13,868 | 0 |
| **Blind Judge 04** | 1 | 12,120 | 0 |

---

## 7. Matriz de Hallazgos Forenses y Plan de Acción de Ingeniería

### 7.1. Optimizaciones para el Pipeline `content-to-course` (C2C v3.22)

1. **Eliminar el Truncamiento de Excepciones en `compile_shard.py` (Prioridad Crítica):**
   - *Problema:* El reporte compacto `compact_report` silencia el mensaje de error de Python y el traceback cuando falla una semilla en el dry-run (`[TPL-DRY]`).
   - *Solución:* Modificar `compile_shard.py` para capturar e imprimir siempre los primeros 3 fallos con su excepción completa (`traceback.format_exc()`). Esto habría ahorrado 91 lecturas de archivo, ~15M tokens y 25 minutos de ejecución en Shard 04.
2. **Revisión del Circuit Breaker (`BUDGET HALT`):**
   - *Problema:* Al alcanzar 5 ciclos fallidos, el validador bloquea permanentemente la compilación del shard sin resetear el contador cuando el autor modifica el archivo fuente.
   - *Solución:* Resetear automáticamente el contador de intentos si el hash criptográfico (SHA-256) de `shard_XX_data.py` cambia respecto al intento anterior.
3. **Refuerzo de Prompts para LaTeX y Escapes (`prompt_shard_author.md` y `prompt_cta_architect.md`):**
   - *Problema:* Aparición sistemática de `SyntaxWarning: invalid escape sequence` (`\d`, `\p`) y llaves dobles `{{...}}` en cadenas de texto no f-string.
   - *Solución:* Incluir una regla canónica estricta: *"Todas las fórmulas LaTeX deben definirse en cadenas raw `r"..."` con delimitadores simples `$ ... $` y llaves simples `{...}`. Jamás duplicar llaves salvo dentro de f-strings activas."*
4. **Manejo de Errores de I/O en Windows (`write_to_file`):**
   - *Problema:* Fallos esporádicos `read ...: Incorrect function` al sobreescribir archivos bloqueados por el sistema operativo.
   - *Solución:* Exigir en las instrucciones de subagentes el uso explícito de `Overwrite: true` y una pausa de 500 ms antes de compilar.

### 7.2. Optimizaciones para el Motor Auditor `c2c-run-auditor`

1. **Detección Determinista de Ventanas de Inactividad / Suspensión (Dead-Time Gap Filter):**
   - *Problema:* El cálculo simple de tiempo de pared (`t_final - t_inicial`) distorsiona severamente los Unit Economics y el speedup cuando el equipo entra en suspensión (ej. 4.09 horas inactivas en este run).
   - *Solución:* Incorporar un filtro que identifique lapsos sin actividad (`gap > 10 min` entre turnos consecutivos sin comandos ni subagentes activos). Reportar formalmente:
     - `wall_clock_gross_seconds` (19,792s / 329.87 min)
     - `wall_clock_net_active_seconds` (4,838s / 80.64 min)
     - `speedup_gross` (1.3x) vs. `speedup_net_active` (5.3x)
2. **Normalización del Esquema en `traceback_deepdive_<id>.json`:**
   - *Problema:* Claves como `wall_clock_time_minutes`, `total_turns` y `total_errors` no estaban expuestas en el nivel raíz del JSON.
   - *Solución:* Estandarizar la cabecera del JSON de traceback con la misma estructura que `telemetry.json`.

---
*Reporte forense determinista y diagnóstico causal completado por `c2c-run-auditor`.*