# Auditoría Forense Ultra-Detallada del Traceback de Ejecución
## Pipeline Content-to-Course (C2C) — Conversación [`876ad3df-153b-4de2-8d3a-43a580b2dbc6`](conversation://876ad3df-153b-4de2-8d3a-43a580b2dbc6)

**Fecha de Auditoría:** `2026-10-17 11:35:49 UTC`  
**Conversación Orquestadora:** [`876ad3df-153b-4de2-8d3a-43a580b2dbc6`](conversation://876ad3df-153b-4de2-8d3a-43a580b2dbc6)  
**Directorio de Telemetría Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\pde_saul_1\work` (`7` snapshots C2C v3.2)  
**Motor Forense:** C2C Traceback Deep-Dive Analyzer (Antigravity SDK)  

---

## 1. Resumen Ejecutivo y Metrología Forense Global

| Métrica Forense | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Tiempo de Pared Total** | **`55.87 min`** (3352.0 s) | Tiempo transcurrido de extremo a extremo |
| **Total de Turnos Analizados** | **`408 turnos`** | Suma de orquestador y subagentes |
| **Total de Errores Catalogados** | **`38 errores`** | Clasificados en 8 categorías técnicas (0% caja negra) |
| **Inferencia LLM Promedio** | **`95.8%`** | Porcentaje de tiempo dedicado a generación/thinking |
| **Ejecución Local de Tools** | **`4.2%`** | Porcentaje de tiempo consumido en I/O y terminal |

### 1.1. Distribución Empírica del Tiempo (Inferencia vs Tools)
```text
========================================================================================
DISTRIBUCIÓN DEL TIEMPO DE PARED POR SUBAGENTE (INFERENCIA LLM vs TOOLS)
========================================================================================
Direct CTA Architect   :    618s (98.3%) LLM |   11s Tools
Author Shard 01        :    458s (97.9%) LLM |   10s Tools
Author Shard 02        :    916s (91.6%) LLM |   83s Tools
Author Shard 03        :    709s (93.2%) LLM |   52s Tools
Judge 01               :    252s (99.6%) LLM |    1s Tools
========================================================================================
```

### 1.2. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json`)

| Etapa | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes en Snapshot | Metadatos de Etapa |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **`00_prepare`** | `2026-10-17 05:58:34` | `0.34s` | `0` (`0` act) | 0 | `—` |
| **`02_shard`** | `2026-10-17 05:58:48` | `0.01s` | `19,479,783` (`1,236,269` act) | 3 | `shards=3` |
| **`03_templates`** | `2026-10-17 06:13:46` | `23.35s` | `19,479,783` (`1,236,269` act) | 3 | `count=16` |
| **`04_build`** | `2026-10-17 06:13:57` | `3.73s` | `0` (`0` act) | 0 | `total_questions=380` |
| **`05_verify`** | `2026-10-17 06:14:04` | `1.07s` | `0` (`0` act) | 0 | `verified_course_path=D:\Augusto\personal_portfolio\Tops_academy\courses\pde_saul_1\work\course_verified.json` |
| **`05b_judge_compare`** | `2026-10-17 06:20:52` | `0.01s` | `551,034` (`155,795` act) | 1 | `passed=True` |
| **`06_publish`** | `2026-10-17 06:21:06` | `1.67s` | `0` (`0` act) | 0 | `published_json=D:\Augusto\personal_portfolio\Tops_academy\courses\pde_saul_1.json` |

---

## 2. Análisis Forense: CTA Architects (Stage 1)
### 2.1. Direct CTA Architect
- **Duración Total:** **`10.48 min`** (629.0 s) en **`33 turnos`**.
- **Tokens:** 338,331 In | 71,080 Out | 2,920,013 Cache.

---

## 3. Análisis Forense: Shards de Autoría (Stage 3)

| Shard ID | Duración (min) | Turnos | Writes | Edits | Check Runs (Fail/Pass) | Lecturas Validador (Ing. Inversa) | Micro-Bucle / Patrón |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Author Shard 01** | 7.8 | 22 | 2 | 0 | 5 (5/0) | 🛑 SÍ (11 lecturas) | ⚠️ SÍ (Check Loop: 5 fallos) |
| **Author Shard 02** | 16.67 | 89 | 2 | 1 | 2 (0/2) | 🛑 SÍ (6 lecturas) | ⚠️ SÍ (Edición Granular: 89t) |
| **Author Shard 03** | 12.68 | 57 | 2 | 0 | 3 (3/0) | 🛑 SÍ (12 lecturas) | ⚠️ SÍ (Edición Granular: 57t) |

---

### 4. Análisis Forense: Blind Judges (Stage 5)

| Blind Judge | Duración (min) | Turnos | Consultas `search_web` | Peticiones HTTP | Estado de Aislamiento | Veredicto y Acuerdo |
| :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| **Judge 01 (`53d65c2c`)** | 4.22 | 8 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) | **✅ 100.0% (32/32 acuerdos, 0 discrepancias)** |

> [!NOTE]
> **Certificación Forense de Stage 5:**  
> Judge 01 resolvió el lote ciego de 32 reactivos en 1 solo ciclo de arbitraje puro. No requirió iteraciones de auto-reparación (`RepairLoop`) ni intervenciones directas del orquestador en esta etapa. El informe `judge_report.json` certificó `passed: True` y `agreement_rate: 1.0`.

---

## 5. Taxonomía Consolidada de Errores (38 Registrados) y Causas Raíz

| Categoría de Error | Ocurrencias | Ejemplo de Incidencia | Causa Raíz Forense Verificada |
| :--- | :---: | :--- | :--- |
| **Shard Compilation & Template Validator Failure** | **11** | Orchestrator (Paso 165): `compile_shard.py` falló con código 1. | Desajuste inicial de argumentos CLI en el prompt (`--shard` omitido), seguido de violaciones R-19 y llaves dobles en plantillas. |
| **Missing File / Directory Error (FileNotFoundError)** | **10** | Autores y Orchestrator (Pasos 58–161): `No existe pre_shard_manifest.json` | **Wipeout catastrófico concurrente**: `clean_orphan_course_dirs` ejecutado por un `pytest` ajeno a las 05:47 UTC borró `courses/pde_saul_1/work`. |
| **Parameter Diversity & Option Collapse (TPL-VAR)** | **4** | Orchestrator (Paso 166, 328): Colisión de opciones bajo 50 semillas. | Dominios numéricos demasiado estrechos en `gen_hab05` y `gen_h02` (50 combinaciones teóricas colapsaron por el principio del palomar). |
| **Python Environment / Virtualenv / Encoding** | **4** | Orchestrator (Paso 186): Tracebacks de importación y codificación. | Exploración interactiva del orquestador inspeccionando módulos internos de `engine/invariants.py` sin sys.path adecuado. |
| **Non-Zero CLI Exit / Subprocess Probe** | **3** | Orchestrator (Paso 103): Sondeo de procesos Python activos. | Monitoreo del orquestador intentando determinar si algún subproceso externo borró el directorio `work`. |
| **Cross-check Verification False (TPL-CROSS)** | **2** | Shard 01 (Paso 105): Verificador `ver_h02` no conmutativo. | La función verificadora rechazaba semillas válidas con raíces repetidas en la ecuación característica. |
| **Exploratory One-Liner / Script Exceptions** | **2** | Orchestrator (Paso 178, 315): Error sintáctico en script en línea. | PowerShell quoting en scripts rápidos ejecutados con `python -c` para probar formateo de cadenas LaTeX. |
| **PowerShell Command / Quoting / $ Expansion** | **2** | Orchestrator (Paso 315): `En línea: 7 Carácter: 189` | Expansión de variables `$` de PowerShell interfiriendo con delimitadores de matemáticas LaTeX (`$F(K, L)$`). |

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)
- **Total de Turnos con Razonamiento:** `166 turnos`
- **Volumen Total de Razonamiento:** `229,305 caracteres`

| Agente | Turnos con Thinking | Volumen (Caracteres) | Muestra de Razonamiento Previo |
| :--- | :---: | :---: | :--- |
| **Author Shard 01** | 15 | 40,268 | `Confirming the role is author for shard_01 within the specified scope. The allow...` |
| **Author Shard 02** | 37 | 46,401 | `Initial check requires the existence of pre_shard_manifest.json before proceed...` |
| **Author Shard 03** | 31 | 47,331 | `Task involves authoring content for shard shard_03, specifically focusing on g...` |
| **Direct CTA Architect** | 13 | 39,709 | `The task is to act as a cta agent, with specific read and write access restricti...` |
| **Blind Judge (Judge 01: `53d65c2c`)** | 4 | 24,023 | `Carefully reviewing the instructions, focusing on the system prompt's architectu...` |
| **Orchestrator** | 66 | 31,573 | `Initiating course creation using the specified skill and applying the "Direct CT...` |

---

## 7. Acciones Correctivas y Recomendaciones Arquitectónicas

### 1. Inmunización de `clean_orphan_course_dirs` frente a Pipelines Activos
- **Problema:** `delete_course.py:clean_orphan_course_dirs` borra cualquier subcarpeta de `courses/` que no tenga un `.json` publicado. Esto provocó el borrado de `courses/pde_saul_1/work` al correr `pytest` en una sesión paralela.
- **Corrección Mandatoria:**
  1. En `tests/test_delete_course.py`, mockear o aislar las pruebas de borrado usando exclusivamente `tmp_path`.
  2. En `clean_orphan_course_dirs`, agregar un check de inmunidad: **NUNCA borrar un directorio si contiene `work/state.json` o si sus archivos fueron modificados en las últimas 24 horas**.

### 2. Corrección del Bug de Creación de Carpetas en `compile_shard.py`
- **Problema:** Si `target_p.name.endswith(".py")` no existe en disco al invocar `compile_shard`, el script salta a la rama `else`, asigna `work_p = target_p` y crea `target_p/templates` con `mkdir(parents=True)`, convirtiendo el archivo `.py` en una carpeta.
- **Corrección:**
  ```python
  if target_p.name.endswith(".py"):
      shard_data_path = target_p
      shards_dir = target_p.parent
      work_p = shards_dir.parent if shards_dir.name == "shards" else shards_dir
  ```
  La condición debe basarse en el nombre del archivo (`.endswith('.py')`), no en si `is_file()` es True en ese milisegundo.

### 3. Alineación del Contrato CLI en `dispatch.py` (Prompt de Autores)
- **Problema:** El prompt despachaba: `compile_shard.py --input ... --output ...`, causando `ERROR: shard_id no especificado`.
- **Corrección:** Estandarizar la instrucción a:
  ```bash
  python .agents/skills/content-to-course/compile_shard.py --work courses/<course_id>/work --shard <shard_id> --strict
  ```

### 4. Calibración de Detección de Arbitraje e Intervenciones en `audit_engine.py`
- **Problema:** `audit_engine.py` consideró que los Blind Judges fallaron al primer intento porque existían 7 intervenciones manuales en `interv_list`, ignorando que todas pertenecían a la Etapa 3 (autoría de plantillas) y ninguna a la Etapa 5.
- **Corrección:** Filtrar `judge_content_interventions` por timestamp o etapa (`stage == 'judge'` o turnos posteriores a `04_build.json`).
- **Problema de Clasificación:** El subagente `53d65c2c` se etiquetó como `"Subagent"` genérico porque su prompt iniciaba con `# Asignación de Evaluación a Ciegas: Blind Judge judge_01`. Incluir este patrón en `discover_all_subagents`.

---
*Informe generado y enriquecido forensemente por `c2c-run-auditor` (Modo Agéntico).*