# Informe de Auditoría Arquitectónica Forense: Rendimiento, Shards y Telemetría Multi-Agente
## Curso: Ecuaciones en Derivadas Parciales - Saúl Elguera (`pde_saul_1`)

**Fecha de Auditoría:** `2026-10-17 11:35:49 UTC`  
**Conversación Orquestadora:** [`876ad3df-153b-4de2-8d3a-43a580b2dbc6`](conversation://876ad3df-153b-4de2-8d3a-43a580b2dbc6)  
**Directorio de Trabajo Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\pde_saul_1\work` (`match=True`)  
**Enfoque:** Telemetría Determinista de API, Subagentes, Shards, Latencias y Operaciones del Orquestador.

---

## 1. Consolidación de Métricas y Caracterización de Carga

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada** | `1 archivos` (25 págs / 0.56 MB) | I__Ecuaciones_en_derivadas_parciales_2026.pdf |
| **Requerimiento de Visión** | `0 páginas` (0 handouts) | Cuadrículas generadas para diagramas/fórmulas |
| **Corpus Sintetizado** | `0 caracteres` (0 palabras) | Texto consolidado tras ingesta y visión |
| **Competencias Extraídas** | **`16 competencias`** | Desglose pedagógico (Hechos, Conceptos, Habilidades) |
| **Shards Particionados** | **`3 shards`** | Unidades de trabajo concurrentes |
| **Subagentes Desplegados** | **`5 subagentes`** | Visión (0), CTA (1), Autores (3), Jueces (0) |
| **Reactivos Finales Validados** | **`380 preguntas`** | Evaluadas en sandbox |
| **Tokens Entrada (Subagentes)** | **`1,442,204` tokens** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`359,271` tokens** | Código de plantillas y JSON generado |
| **Tokens Caché (Leídos)** | **`46,445,404` tokens** | Caché de contexto reutilizado por la API |
| **Gran Total Tokens Activos** | **`2,918,171` tokens** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`49,363,575` tokens** | Consumo total de cuota facturable |

---

## 2. Ratios Unitarios Normalizados (Unit Economics)

Métricas normalizadas para comparación *apples-to-apples* frente a cursos de diferente volumen de contenido:

| Métrica Unitaria | Valor Obtenido | Interpretación de Eficiencia |
| :--- | :--- | :--- |
| **Tokens Totales por Pregunta** | **`129,904.1 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`7,679.4 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`3,085,223.4 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`77,266.8 tokens/comp`** | Costo puro de la etapa de autoría por competencia |
| **Tokens Totales por Página / Slide** | **`1,974,543.0 tokens/pág`** | Esfuerzo cognitivo por diapositiva original |
| **Segundos de Pared por Pregunta** | **`8.82 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`6.8 preg/min`** | Velocidad de producción del pipeline |
| **Factor de Aceleración Paralela** | **`1.93x`** | Relación tiempo cómputo vs tiempo de pared |

---

## 3. Desglose Forense por Etapas Críticas

### 3.0. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json` & `state.json`)
- **Snapshots de Etapa Verificados (`conversation_id` = `876ad3df`):** `7 etapas`
- **Estado Maestro (`work/state.json`):** `completed` (Etapa actual/final: `publish`)

| Etapa (Snapshot) | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes Capturados | Artefactos / Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-10-17 05:58:34` | `0.34s` | `0` (`0` act) | 0 | `—` |
| **`02_shard`** | `2026-10-17 05:58:48` | `0.01s` | `19,479,783` (`1,236,269` act) | 3 | `shards=3` |
| **`03_templates`** | `2026-10-17 06:13:46` | `23.35s` | `19,479,783` (`1,236,269` act) | 3 | `count=16` |
| **`04_build`** | `2026-10-17 06:13:57` | `3.73s` | `0` (`0` act) | 0 | `total_questions=380` |
| **`05_verify`** | `2026-10-17 06:14:04` | `1.07s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\pde_saul_1\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-10-17 06:20:52` | `0.01s` | `551,034` (`155,795` act) | 1 | `passed=True` |
| **`06_publish`** | `2026-10-17 06:21:06` | `1.67s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\pde_saul_1.json` |

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
- **Tiempo Fase Harmonizer (Barrera Síncrona):** **`629.0s`**
- **Tiempo de Pared Total de Etapa 1B:** **`629.0s`** (`10.5 min`)

| Subagente CTA | Rol / Sección | Turnos | Tokens In | Tokens Out | Cache Leído | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cognitive Task Analysis Architect** | Direct Architect | 33 | 338,331 | 71,080 | 2,920,013 | 1 | **629.0s** |

---

### 3.3. Stage 3: Autoría de Reactivos por Shard y Análisis por Competencia
- **Total de Shards Auditados:** `3 shards concurrentes`
- **Duración Mínima de Shard:** `468.0s` | **Mediana:** `761.0s`
- **Tiempo de Pared Máximo (Straggler Crítico):** **`1000.0s`** (`16.7 min`) por `Shard Author shard_02`
- **Retraso de Sincronización Impuesto por el Straggler:** **`+239.0s`** frente a la mediana
- **Tokens Promedio por Competencia en Autores:** **`77,266.8 tokens/competencia`**

| Shard ID | Competencias Asignadas | Comps | Tokens In | Tokens Out | Cache Leído | Total Activo | Tokens / Comp | Turnos | Errores | Duración |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Shard Author shard_01** | `H-01, C-01, H-02, C-02 (+2)` | 6 | 128,080 | 65,949 | 1,187,480 | 194,029 | **32,338.2** | 22 | 6 | **468.0s** |
| **Shard Author shard_02 🛑** | `Hab-02, C-04, H-03, Hab-03 (+1)` | 5 | 363,312 | 88,735 | 11,969,335 | 452,047 | **90,409.4** | 89 | 7 | **1000.0s** |
| **Shard Author shard_03** | `Hab-04, Hab-05, H-04, C-06 (+1)` | 5 | 501,960 | 88,233 | 5,086,699 | 590,193 | **118,038.6** | 57 | 5 | **761.0s** |

---

### 3.4. Evaluación y Arbitraje de Blind Judges (Verificación Psicométrica Ciega)

> [!NOTE]
> **Dictamen Real de Blind Judges:** ✅ **100% ACUERDO AL PRIMER INTENTO (32/32 REACTIVOS)** *(Aclaración Forense de Telemetría)*  
> La validación psicométrica oficial registrada en `work/telemetry/05b_judge_compare.json` y `work/judge_report.json` certificó un **acuerdo perfecto del 100.0% (32/32 reactivos)**, con **0 discrepancias**, **0 discordancias** y veredicto definitivo `passed: True` en el primer y único ciclo de arbitraje.  
> *Nota de calibración del auditor:* La alerta inicial generada por el motor determinista de `audit_engine.py` se debió a un falso positivo heurístico: el motor computó 7 intervenciones manuales del supervisor sin discriminar que estas ocurrieron tempranamente durante la **Etapa 3 (Autoría de Shards)** para estabilizar plantillas paramétricas antes de la compilación del curso, y **ninguna ocurrió durante la Etapa 5 de arbitraje ciego**.

| Dimensión de Arbitraje Ciego | Valor Registrado | Observación Técnica Forense |
| :--- | :--- | :--- |
| **Lote Estratificado Ciego** | `32 reactivos` (16 comps × 2) | Lote de evaluación sin soluciones (`judge_batch.json`) |
| **Subagentes Jueces Ciegos** | `1 juez` (`Judge 01`: `53d65c2c`) | Aislamiento epistémico estricto (0 búsquedas web, 0 HTTP) |
| **Resultado al Primer Intento** | **`✅ 100.0% (32/32 acuerdos)`** | 0 discordancias frente a ground truth (`passed: True`) |
| **Iteraciones de Auto-Reparación** | `0 iteraciones` en sandbox | No requirió RepairLoop en Stage 5 |
| **Intervenciones en Stage 5** | `0 operaciones directas` | Arbitraje ciego 100% autónomo y limpio |
| **Intervenciones Previas (Stage 3)**| 🛠️ `7 operaciones directas` | Correcciones en `shard_01_data.py` y `shard_03_data.py` |

#### Secuencia Verificada de Arbitraje Ciego:
- 1. **Generación del Lote Ciego (`judge_batch.json`)**: 32 reactivos estratificados (2 por cada una de las 16 competencias).
- 2. **Despacho Epistémicamente Aislado (`judge_01`)**: El subagente `53d65c2c` resolvió los 32 ejercicios en 4.22 min mediante inferencia deductiva pura, generando `verification/judge_responses_01.json`.
- 3. **Comparación Determinista (`05b_judge_compare.json`)**: Se validó coincidencia unánime (32/32, `agreement_rate = 1.0`).

---

## 4. Auditoría Forense del Orquestador y Catálogo de Intervenciones Manuales

### 4.1. Descomposición del Tiempo Total del Orquestador
- ⏱️ **Tiempo Total de Pared del Orquestador:** `55.87 min` (`3352.0s`)
- 💻 **Tiempo Activo Ejecutando Comandos CLI (`run.py`):** `11.6 min` (`697.0s`)
- 🛠️ **Tiempo Gastado en Intervenciones Manuales (Supervisor Repair):** **`1.4 min`** (`83.0s`)
- ⏳ **Tiempo Ocioso en Barreras de Sincronización (Esperando Subagentes):** `1.6 min` (`94.0s`)
- 🧠 **Tiempo de Inferencia y Razonamiento del Modelo:** `3.6 min` (`216.0s`)
- 🚨 **Tiempo Perdido en Diagnóstico y Recuperación de Wipeout:** **`9.8 min`** (Pasos 58–164)

### 4.2. Catálogo Cronológico de Reparaciones Manuales del Orquestador
El orquestador ejecutó **7 operaciones quirúrgicas** de edición directa de código con `replace_file_content` sobre los archivos de datos de shards en Stage 3:

| Paso | Archivo Afectado | Categoría Técnica | Causa Raíz / Justificación Técnica Forense | Herramienta | Tokens Paso |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **181** | `shard_03_data.py` | Sintaxis / Escape LaTeX | En `gen_hab05`, en un `rf"..."` string, Author 03 escribió `\operatorname{arccot}(y/x)`. En Python, `{arccot}` fue interpretado como variable en el f-string, provocando `NameError: name 'arccot' is not defined`. Se escapó a `\operatorname{{arccot}}(y/x)`. | `replace_file_content` | 3,431 |
| **266** | `shard_03_data.py` | Expansión Paramétrica (TPL-VAR) | En `gen_hab05`, el dominio inicial tenía solo 50 combinaciones ($k \in [1, 25]$, $p \in [2, 4]$). Bajo 50 semillas de dry-run (`--seeds 50`), la colisión de opciones generó violaciones TPL-COLLAPSE. Se amplió a $k \in [1, 40]$ y $p \in [2, 4, 6]$ (120 combinaciones). | `replace_file_content` | 4,743 |
| **270** | `shard_03_data.py` | Invariante Pedagógico (R-19) | En `Hab-05`, Hint 3 utilizaba la frase *"Elimine los parámetros auxiliares combinando las relaciones trigonométricas y espaciales para despejar u(x, y)"*, disparando la heurística anti-giveaway R-19 (scaffolding leak). Se refraseó pedagógicamente a *"Despeje las variables auxiliares..."*. | `replace_file_content` | 3,436 |
| **328** | `shard_01_data.py` | Expansión Paramétrica (TPL-VAR) | En `gen_h02`, el rango de orden y grado de EDPs era insuficiente para soportar 50 semillas sin repetir enunciados. Se amplió el espacio a `order in [2..7]`, `deg in [2..6]`, `p_low in [8..13]` y se actualizó `ver_h02`. | `replace_file_content` | 7,110 |
| **332** | `shard_01_data.py` | Sintaxis / Llaves Residuales | En la lista `TEMPLATES` de `shard_01_data.py`, Author 01 colocó llaves dobles en cadenas crudas LaTeX: `$F(K, L) = {A} K^{{{alpha}}} L^{{{beta}}}$`. `check_templates` detectó `Residual double curly braces`. Se simplificó a `${A} K^{alpha} L^{beta}$`. | `replace_file_content` | 9,285 |
| **345** | `shard_01_data.py` | Vinculación de Variables | En `gen_hab01`, el stem requería las expresiones LaTeX formateadas `cand_tex` ($e^{c(x-y)}$) y `sol_ux_tex` ($c e^{c(x-y)}$), pero la función no las exportaba en el diccionario `vars`, causando que `assemble.py` fallara al rellenar la plantilla. | `replace_file_content` | 4,042 |
| **349** | `shard_01_data.py` | Placeholders en Stem/Sol | En `Hab-01`, el stem tenía la expresión fija $U(x,y)=e^{{c}(x-y)}$ que colisionaba con el motor de sustitución. Se reemplazó por los placeholders dinámicos `{cand_tex}` y `{sol_ux_tex}` vinculados a `vars`. | `replace_file_content` | 3,764 |

---

### 4.3. Incidente Forense Crítico: Borrado Masivo Concurrente por `clean_orphan_course_dirs` y Resurrección
Uno de los hallazgos más extraordinarios de esta auditoría es la causa raíz del retraso y los errores masivos de "archivos no encontrados" entre los pasos 58 y 164:

1. **La Interferencia Externa Concurrente:** A las `05:47:02 UTC`, mientras los 3 autores de `pde_saul_1` estaban trabajando, otra sesión/agente en el workspace (`1db5ddea`) ejecutó una suite global de pruebas: `pytest -q`.
2. **El Mecanismo Destructor:** La prueba unitaria `tests/test_delete_course.py::test_clean_orphan_dirs` invocó la función de producción `clean_orphan_course_dirs(dry_run=False)` sin aislarla en un entorno temporal (`tmp_path`). 
3. **La Condición de Carrera:** `clean_orphan_course_dirs` inspecciona la carpeta `courses/` y borra con `shutil.rmtree` **cualquier subdirectorio que no posea un archivo `<id>.json` correspondiente publicado**. Dado que `pde_saul_1` estaba en plena generación (su JSON final solo se publica en Stage 6), `clean_orphan_course_dirs` identificó erróneamente a `courses/pde_saul_1` como un "directorio huérfano" y **borró de golpe todo el directorio `work/`** (`cta.json`, `cta_data.py`, `pre_cta_manifest.json`, `pre_shard_manifest.json`, `pages/`).
4. **La Reacción en Cadena de los Autores:** A las `05:47:44–05:49:05 UTC`, los 3 autores (`shard_01`, `shard_02`, `shard_03`) detectaron la desaparición de los manifiestos y emitieron bloqueos críticos (`BLOCKER:: No existe pre_shard_manifest.json`). Author 02 entró en un bucle forense de 181 pasos buscando el archivo en la Papelera de Reciclaje (`C:\$Recycle.Bin`), en el historial de Git y en los logs de otros subagentes.
5. **La Resurrección Manual por el Orquestador:** Tras notar el borrado en el paso 59 y sospechar inicialmente de `delete_course.py` (paso 100), el orquestador resolvió la crisis con maestría forense (pasos 151–160):
   - Localizó la transcripción profunda de CTA Architect (`d30cf777...transcript_full.jsonl`).
   - Extrajo quirúrgicamente el código fuente de `cta_data.py` (77,538 bytes) y lo reescribió en disco.
   - Re-ejecutó `run.py --stage prepare`, recompiló `compile_cta.py` y ejecutó `run.py --stage shard`, reconstruyendo intacto el entorno de trabajo.

---

### 4.4. Defecto en `compile_shard.py`: Creación Errónea de Directorios Fantasma
Se identificó un defecto sutil pero crítico en `compile_shard.py` (líneas 570–586):
- Cuando un subagente invoca `compile_shard.py` antes de que el archivo `shard_XX_data.py` exista físicamente en disco, `Path(work_or_path).is_file()` retorna `False`.
- El script asume entonces que la ruta proporcionada es un directorio de trabajo (`work_p`) y ejecuta:
  ```python
  templates_dir = work_p / "templates"
  templates_dir.mkdir(parents=True, exist_ok=True)
  ```
- Dado que `work_p` era `courses/pde_saul_1/work/shards/shard_03_data.py`, `mkdir(parents=True)` **creó `shard_03_data.py` como una CARPETA** en disco con una subcarpeta `templates/` adentro.
- Esto bloqueó a Author 03 de guardar su código fuente en `shard_03_data.py` hasta que en el paso 100 ejecutó `Remove-Item -Recurse -Force` para eliminar el directorio espurio y escribir el archivo real.

---

### 4.5. Discrepancia de Contrato CLI en el Prompt del Autor
En el paso 55, el orquestador inyectó a los 3 autores una plantilla de comando CLI desactualizada:
```bash
python .agents/skills/content-to-course/compile_shard.py --input ... --output ... --cta ... --manifest ...
```
Al omitir el parámetro `--shard shard_XX`, el compilador abortó inmediatamente con `ERROR: shard_id no especificado para compile_shard`, forzando a los subagentes a inspeccionar el código fuente del compilador (turnos redundantes y consumo de tokens de lectura de código).

---

## 5. Diagnóstico de Cuellos de Botella y Antipatrones Detectados

### 🛑 [CRITICAL] Destrucción Masiva de Directorio de Trabajo por Test Concurrente (`clean_orphan_course_dirs`)
- **Ámbito:** `Infraestructura / Concurrencia de Workspace`
- **Diagnóstico:** A las 05:47:02 UTC, una corrida global de `pytest -q` ejecutada en otra sesión (`1db5ddea`) invocó `clean_orphan_course_dirs(dry_run=False)` en `tests/test_delete_course.py`. Al no estar mockeada ni usar `tmp_path`, la función borró todo `courses/pde_saul_1/work/` porque aún no existía `courses/pde_saul_1.json`. Esto provocó un apagón total en los autores y demandó 10 minutos de reconstrucción forense por el orquestador.
- **Impacto:** ~10 minutos de retraso en pared, 3 subagentes bloqueados y consumo masivo de tokens redundantes en bucles de búsqueda en disco.

### 🛑 [HIGH] Defecto de Creación de Directorio en `compile_shard.py` (`shard_03_data.py/`)
- **Ámbito:** `Compilador Determinista (compile_shard.py)`
- **Diagnóstico:** Si `compile_shard.py` es invocado antes de que el archivo `.py` exista físicamente, `is_file()` retorna `False` y el script interpreta la ruta como directorio, ejecutando `templates_dir.mkdir(parents=True)`. Esto creó `shard_03_data.py` como carpeta, bloqueando las operaciones de escritura de Author 03 hasta su purga forzada en el paso 100.

### 🛑 [HIGH] Antipatrón de Micro-Bucle Interactivo e Investigación Forzada (181 turnos en Shard Author shard_02)
- **Ámbito:** `Shard Author shard_02`
- **Diagnóstico:** Tras la desaparición repentina de `pre_shard_manifest.json` y la ausencia de `shard_02.json` (que no se compila en esa ruta), Author 02 intentó diagnosticar la desaparición de archivos ejecutando 48 comandos de PowerShell, revisando la papelera de reciclaje y transcripciones ajenas durante 16.67 minutos.

### 🛑 [HIGH] Síndrome del Orquestador Reparador (7 intervenciones manuales en Stage 3)
- **Ámbito:** `Director (Orchestrator)`
- **Diagnóstico:** El orquestador principal asumió la corrección directa de código con `replace_file_content` (escapes LaTeX, dominios paramétricos TPL-VAR para 50 semillas, invariante R-19 y placeholders de stem). Consumió más de 35,811 tokens en turnos de mantenimiento que debieron haber sido resueltos por auto-reparación o validadores más permisivos en tiempo de autoría.

### ⚠️ [MEDIUM] Deriva de Contrato en la Plantilla de Prompt de Autores
- **Ámbito:** `Orquestación / Dispatcher (dispatch.py)`
- **Diagnóstico:** El prompt inyectado a los autores en el paso 55 omitió `--shard shard_XX` en el comando sugerido de `compile_shard.py`, arrojando errores inmediatos de sintaxis CLI en el turno inicial de los 3 autores.

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)

- **Total de Turnos con Razonamiento:** `166 turnos`
- **Volumen Total de Razonamiento:** `229,305 caracteres`
- **Razonamiento del Orquestador:** `66 turnos` (31,573 chars)
- **Razonamiento de Subagentes:** `100 turnos` (197,732 chars)

| Agente / Subagente | Turnos de Thinking | Caracteres de Thinking | Trazas de Error Capturadas |
| :--- | :---: | :---: | :---: |
| **Cognitive Task Analysis Architect** | 13 | 39,709 | ⚠️ 1 |
| **Shard Author shard_01** | 15 | 40,268 | ⚠️ 6 |
| **Shard Author shard_02** | 37 | 46,401 | ⚠️ 7 |
| **Shard Author shard_03** | 31 | 47,331 | ⚠️ 5 |
| **Blind Judge (Judge 01: `53d65c2c`)** | 4 | 24,023 | 0 |

---
*Reporte forense enriquecido emitido por `c2c-run-auditor` (Modo Agéntico).*