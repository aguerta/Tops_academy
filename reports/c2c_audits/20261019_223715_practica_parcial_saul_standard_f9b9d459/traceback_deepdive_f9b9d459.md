# Auditoría Forense Ultra-Detallada del Traceback de Ejecución
## Pipeline Content-to-Course (C2C) — Conversación [`f9b9d459-d84a-4e3d-bf32-48e74d8b5c5a`](conversation://f9b9d459-d84a-4e3d-bf32-48e74d8b5c5a)

**Fecha de Auditoría:** `2026-10-20 03:37:15 UTC`  
**Conversación Orquestadora:** [`f9b9d459-d84a-4e3d-bf32-48e74d8b5c5a`](conversation://f9b9d459-d84a-4e3d-bf32-48e74d8b5c5a)  
**Directorio de Telemetría Validado (Zero-Collision):** `D:\Augusto\personal_portfolio\Tops_academy\courses\practica_parcial_saul_standard\work` (`8` snapshots C2C v3.2)  
**Motor Forense:** C2C Traceback Deep-Dive Analyzer (Antigravity SDK)  

---

## 1. Resumen Ejecutivo y Metrología Forense Global

| Métrica Forense | Valor Registrado | Observación Técnica |
| :--- | :--- | :--- |
| **Tiempo de Pared Total** | **`64.22 min`** (3853.0 s) | Tiempo transcurrido de extremo a extremo |
| **Total de Turnos Analizados** | **`674 turnos`** | Suma de orquestador y subagentes |
| **Total de Errores Catalogados** | **`61 errores`** | Clasificados en 10 categorías técnicas (0% caja negra) |
| **Inferencia LLM Promedio** | **`95.8%`** | Porcentaje de tiempo dedicado a generación/thinking |
| **Ejecución Local de Tools** | **`4.2%`** | Porcentaje de tiempo consumido en I/O y terminal |

### 1.1. Distribución Empírica del Tiempo (Inferencia vs Tools)
```text
========================================================================================
DISTRIBUCIÓN DEL TIEMPO DE PARED POR SUBAGENTE (INFERENCIA LLM vs TOOLS)
========================================================================================
CTA Architect (part_01):    257s (99.2%) LLM |    2s Tools
CTA Architect (part_02):    205s (99.0%) LLM |    2s Tools
CTA Architect (part_03):    248s (99.2%) LLM |    2s Tools
CTA Architect (part_04):    444s (99.8%) LLM |    1s Tools
CTA Architect (part_05):    287s (98.6%) LLM |    4s Tools
CTA Architect (part_06):    490s (98.8%) LLM |    6s Tools
CTA Architect (part_07):    554s (99.3%) LLM |    4s Tools
Direct CTA Architect   :     88s (100.0%) LLM |    0s Tools
Author Shard 01        :    555s (97.4%) LLM |   15s Tools
Author Shard 02        :    667s (97.8%) LLM |   15s Tools
Author Shard 03        :    682s (95.7%) LLM |   27s Tools
Author Shard 04        :    425s (95.9%) LLM |   17s Tools
Author Shard 05        :   1359s (95.3%) LLM |   39s Tools
Author Shard 06        :    540s (95.7%) LLM |   24s Tools
Author Shard 07        :    474s (97.1%) LLM |   14s Tools
Author Shard 08        :    808s (96.1%) LLM |   28s Tools
Author Shard 09        :    610s (96.7%) LLM |   21s Tools
Author Shard 10        :    347s (97.7%) LLM |    8s Tools
Author Shard 11        :    377s (97.2%) LLM |   11s Tools
Judge 01               :     91s (98.9%) LLM |    1s Tools
Judge 02               :     95s (100.0%) LLM |    0s Tools
Judge 03               :    216s (99.5%) LLM |    1s Tools
Judge 04               :    391s (99.7%) LLM |    1s Tools
Judge 05               :    105s (100.0%) LLM |    0s Tools
Judge 06               :    104s (100.0%) LLM |    0s Tools
Judge 07               :     99s (100.0%) LLM |    0s Tools
Judge 08               :    101s (100.0%) LLM |    0s Tools
Judge 09               :    129s (99.2%) LLM |    1s Tools
Judge 10               :     99s (99.0%) LLM |    1s Tools
Judge 11               :    114s (100.0%) LLM |    0s Tools
========================================================================================
```

### 1.2. Telemetría Incremental por Etapa C2C v3.2 (`work/telemetry/*.json`)

| Etapa | Timestamp (UTC) | Duración Etapa | Tokens Etapa (Total / Activos) | Subagentes en Snapshot | Metadatos de Etapa |
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

## 2. Análisis Forense: CTA Architects (Stage 1)
### 2.1. CTA Architect (part_01)
- **Duración Total:** **`4.32 min`** (259.0 s) en **`7 turnos`**.
- **Tokens:** 64,841 In | 35,750 Out | 199,541 Cache.
### 2.2. CTA Architect (part_02)
- **Duración Total:** **`3.45 min`** (207.0 s) en **`8 turnos`**.
- **Tokens:** 60,049 In | 26,733 Out | 233,995 Cache.
### 2.3. CTA Architect (part_03)
- **Duración Total:** **`4.17 min`** (250.0 s) en **`8 turnos`**.
- **Tokens:** 96,752 In | 37,283 Out | 208,662 Cache.
### 2.4. CTA Architect (part_04)
- **Duración Total:** **`7.42 min`** (445.0 s) en **`7 turnos`**.
- **Tokens:** 134,873 In | 46,869 Out | 226,260 Cache.
### 2.5. CTA Architect (part_05)
- **Duración Total:** **`4.85 min`** (291.0 s) en **`9 turnos`**.
- **Tokens:** 116,398 In | 36,886 Out | 260,886 Cache.
### 2.6. CTA Architect (part_06)
- **Duración Total:** **`8.27 min`** (496.0 s) en **`20 turnos`**.
- **Tokens:** 111,994 In | 43,951 Out | 1,244,068 Cache.
### 2.7. CTA Architect (part_07)
- **Duración Total:** **`9.3 min`** (558.0 s) en **`12 turnos`**.
- **Tokens:** 122,094 In | 68,274 Out | 657,013 Cache.
### 2.8. Direct CTA Architect
- **Duración Total:** **`1.47 min`** (88.0 s) en **`6 turnos`**.
- **Tokens:** 51,941 In | 3,709 Out | 115,973 Cache.

---

## 3. Análisis Forense: Shards de Autoría (Stage 3)

| Shard ID | Duración (min) | Turnos | Writes | Edits | Check Runs (Fail/Pass) | Lecturas Validador (Ing. Inversa) | Micro-Bucle / Patrón |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Author Shard 01** | 9.5 | 27 | 1 | 5 | 4 (3/1) | NO (0) | NO |
| **Author Shard 02** | 11.37 | 45 | 1 | 11 | 3 (2/1) | NO (0) | ⚠️ SÍ (Edición Granular: 45t) |
| **Author Shard 03** | 11.88 | 28 | 1 | 5 | 3 (1/2) | NO (0) | NO |
| **Author Shard 04** | 7.38 | 22 | 1 | 5 | 3 (2/1) | NO (0) | NO |
| **Author Shard 05** | 23.77 | 62 | 1 | 11 | 8 (7/1) | NO (0) | ⚠️ SÍ (Check Loop: 7 fallos) |
| **Author Shard 06** | 9.4 | 31 | 1 | 7 | 4 (3/1) | NO (0) | NO |
| **Author Shard 07** | 8.13 | 15 | 1 | 2 | 2 (1/1) | NO (0) | NO |
| **Author Shard 08** | 14.02 | 45 | 1 | 6 | 3 (1/2) | 🛑 SÍ (10 lecturas) | ⚠️ SÍ (Edición Granular: 45t) |
| **Author Shard 09** | 10.52 | 23 | 1 | 2 | 4 (1/3) | NO (0) | NO |
| **Author Shard 10** | 5.92 | 10 | 1 | 0 | 1 (0/1) | NO (0) | NO |
| **Author Shard 11** | 6.47 | 20 | 1 | 1 | 3 (0/3) | NO (0) | NO |

---

## 4. Análisis Forense: Blind Judges (Stage 5)

| Blind Judge | Duración (min) | Turnos | Consultas `search_web` | Peticiones HTTP | Estado de Aislamiento |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Judge 01** | 1.53 | 5 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |
| **Judge 02** | 1.58 | 6 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |
| **Judge 03** | 3.62 | 5 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |
| **Judge 04** | 6.53 | 6 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |
| **Judge 05** | 1.75 | 5 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |
| **Judge 06** | 1.73 | 6 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |
| **Judge 07** | 1.65 | 5 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |
| **Judge 08** | 1.68 | 6 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |
| **Judge 09** | 2.17 | 7 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |
| **Judge 10** | 1.67 | 6 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |
| **Judge 11** | 1.9 | 6 | 0 | 0 | ✅ Aislamiento Estricto (Razonamiento Puro) |

---

## 5. Taxonomía Consolidada de Errores (61 Registrados)

| Categoría de Error | Ocurrencias | Ejemplo de Incidencia | Razonamiento Previo (Thinking) |
| :--- | :---: | :--- | :--- |
| **Missing File / Relative Path / Directory Error (FileNotFoundError)** | **18** | `Orchestrator` (Paso 105): The command exited with code 1. | Output: | C:\Users\augus\AppData\Loc... | *Sin thinking capturado* |
| **Parameter Diversity & Option Collapse (TPL-VAR / TPL-COLLAPSE)** | **11** | `Orchestrator` (Paso 202): The command exited with code 1. | Output: | Traceback (most recent cal... | *Sin thinking capturado* |
| **Exploratory Python One-Liner / Script Exceptions (Syntax/Key/Type/ValueError)** | **9** | `Orchestrator` (Paso 196): The command exited with code 1. | Output: | Traceback (most recent cal... | `Examining the LaTeX math expression in the distractor, a potential clue to the o...` |
| **Shard Compilation & Template Validator Failure (compile_shard / check_templates)** | **9** | `Author Shard 01` (Paso 10): The command exited with code 1. | Output: | FAIL: Error sint�ctico en ... | `Initiating the official compilation process. The objective is to transform input...` |
| **Python Environment / Virtualenv / Encoding Discrepancy** | **4** | `Orchestrator` (Paso 218): The command exited with code 1. | Output: | Traceback (most recent cal... | *Sin thinking capturado* |
| **File Edit / Write Tool Target Mismatch (replace_file_content / Overwrite)** | **4** | `Author Shard 02` (Paso 64): Encountered error in step execution: Could not successfully apply any ... | `The original text segment describes a competitive firm's profit function, which ...` |
| **Non-Zero CLI Exit / Subprocess Probe (Exit Code 1)** | **2** | `Orchestrator` (Paso 71): Encountered error in step execution: agent "c2c_cta_architect" already... | `The `prompt_cta_architect.md` file is verified as complete and accurate, contain...` |
| **LaTeX Control Character / Raw-String Corruption (R-03 / SyntaxWarning)** | **2** | `Author Shard 07` (Paso 8): The command exited with code 1. | Output: | <truncated 10 lines> | D:\... | `The data file for shard 07 is confirmed to exist, so the compilation step can be...` |
| **CTA Compilation & Schema Errors (CTA-SCHEMA / CTA-EV / DAG Cycle)** | **1** | `Orchestrator` (Paso 63): The command exited with code 1. | Output: | Traceback (most recent cal... | `Initial observation: the structure within the file seems to define concepts, pot...` |
| **PowerShell Command / Quoting / $Variable Expansion Friction** | **1** | `Author Shard 05` (Paso 105): The command exited with code 1. | Output: | System.Management.Automati... | `The decoupled equation includes X(x) and Y(y), which are functions, not variable...` |

---

## 6. Telemetría de Razonamiento Cognitivo (Thinking Traces)
- **Total de Turnos con Razonamiento:** `326 turnos`
- **Volumen Total de Razonamiento:** `955,026 caracteres`

| Agente | Turnos con Thinking | Volumen (Caracteres) | Muestra de Razonamiento Previo |
| :--- | :---: | :---: | :--- |
| **Author Shard 01** | 18 | 42,832 | `Initial task is to process a work order located at a specific file path. First a...` |
| **Author Shard 02** | 14 | 44,575 | `The assigned work order requires reading a specific JSON file to understand the ...` |
| **Author Shard 03** | 14 | 56,816 | `Understood. Reading the work order file to understand the task and its constrain...` |
| **Author Shard 04** | 14 | 36,303 | `Initiating the work order process, first retrieving the task definition file. Th...` |
| **Author Shard 05** | 36 | 107,043 | `Task is to process a work order specified in the caller message and to finalize ...` |
| **Author Shard 06** | 18 | 52,118 | `Initiating the assigned task as the designated author, `shard_06`, according to ...` |
| **Author Shard 07** | 10 | 45,784 | `Initial work order received, referencing an item file to be read and a specific ...` |
| **Author Shard 08** | 24 | 61,818 | `Initial task: review the provided work order file. Verify compliance with the sy...` |
| **Author Shard 09** | 15 | 69,136 | `Initial file inspection is required to understand the task. The system prompt sh...` |
| **Author Shard 10** | 6 | 31,813 | `Initial work order identified; now focusing on understanding the assigned conten...` |
| **Author Shard 11** | 9 | 31,498 | `Reviewing the instructions, the task is to shard author `shard_11` based on the ...` |
| **CTA Architect (part_01)** | 5 | 27,889 | `I'm thinking through how to approach this.
DONE: courses/practica_parcial_saul_s...` |
| **CTA Architect (part_02)** | 6 | 19,606 | `I'm thinking through how to approach this....` |
| **CTA Architect (part_03)** | 5 | 28,685 | `I'm thinking through how to approach this....` |
| **CTA Architect (part_04)** | 6 | 28,483 | `Examining the work order, expecting it to contain instructions for cognitive tas...` |
| **CTA Architect (part_05)** | 6 | 32,152 | `Initial task is to process the assigned work order file. Understanding its conte...` |
| **CTA Architect (part_06)** | 14 | 30,391 | `The instruction specifies the work order to be addressed. The task involves read...` |
| **CTA Architect (part_07)** | 8 | 33,562 | `Task involves finalizing a work order with a specific output path and rememberin...` |
| **Direct CTA Architect** | 5 | 2,342 | `Initial assignment parameters have been received. The task involves architectura...` |
| **Judge 01** | 3 | 8,427 | `Initial task: understand the provided work order and system prompt. Focus is on ...` |
| **Judge 02** | 3 | 8,978 | `Work order requires examining a specific file. The file content will inform the ...` |
| **Judge 03** | 3 | 22,066 | `Begin by accessing the specified work order file. The instruction explicitly dir...` |
| **Judge 04** | 3 | 32,356 | `Initial assignment is Blind Judge 04. The instructions specify a work order file...` |
| **Judge 05** | 3 | 12,973 | `Acknowledged the work order and system prompt. Initiating the defined workflow, ...` |
| **Judge 06** | 3 | 10,829 | `Initial work order acquired. The focus is to understand the task based on the pr...` |
| **Judge 07** | 3 | 10,062 | `Must begin by reading the assigned work order file. The instruction explicitly s...` |
| **Judge 08** | 3 | 8,443 | `The initial instruction specifies reading a file before proceeding, so that step...` |
| **Judge 09** | 3 | 13,589 | `Initiating the work order by reading the specified JSON file. Observing the syst...` |
| **Judge 10** | 4 | 12,578 | `Work order identified. Proceeding to retrieve and examine the specified file. Th...` |
| **Judge 11** | 3 | 12,158 | `Initial work order acquisition is necessary. Proceeding to view the specified fi...` |
| **Orchestrator** | 59 | 19,721 | `Checking available skills to fulfill the user's request to create a course from ...` |

---

---

## 7. Diagnóstico Forense de Causa Raíz y Optimización Agéntica

### 7.1. Verificación de Aislamiento Estricto Zero-Collision (Garantía C2C v3.2)
- **Conversación Evaluada:** [`f9b9d459-d84a-4e3d-bf32-48e74d8b5c5a`](conversation://f9b9d459-d84a-4e3d-bf32-48e74d8b5c5a).
- **Consistencia de WorkDir:** Validado en `courses/practica_parcial_saul_standard/work`.
- **Integridad de Snapshots:** Los 8 archivos `work/telemetry/00_prepare.json` a `06_publish.json` y `state.json` coinciden unívocamente con `conversation_id = f9b9d459-d84a-4e3d-bf32-48e74d8b5c5a`.
- **Aislamiento Multi-Run:** Sin colisión con corridas simultáneas o previas (`afb5aa18`, `a53e6af1`, `acdc402d`).

---

### 7.2. Análisis Forense Causal de Cuellos de Botella y Micro-Bucles

#### 7.2.1. Anatomía del Straggler Crítico en Shard Author 05 (1426.0s / 62 turnos / 8 errores)
- **Competencias Evaluadas:** `H-06`, `C-10`, `C-11`, `Hab-11`, `Hab-12`, `C-12`.
- **Patrón Causal:** En `Hab-12` (Ecuaciones Diferenciales Parciales - Método de Separación de Variables), el modelo generador intentó parametrizar la solución $u(x, y) = C e^{k(x + y/a)}$.
- **Inyección de Error Sintáctico:** Al renderizar cadenas f-strings con KaTeX (`rf"$u(x, y) = C e^{{k \left( x + \frac{{y}}{{{a}}} \right)}}..."$`), se generaron desbalances de llaves (`R-20: SINTAXIS / LLAVES`).
- **Cadena de Intentos Fallidos:**
  * Turno 18: Fallo con 17 errores de compilación.
  * Turno 52: Reintento con 9 errores.
  * Turno 66: Reintento con 9 errores.
  * Turno 95: Reintento con 14 errores.
  * Turno 104: Intento fallido de comando PowerShell `$Host.UI.RawUI.BufferSize`.
  * Turno 109: Intento 8 sobre 6 (`[COMPILE 8/6]`), disparando el disyuntor automático (`circuit_breaker_Hab-12.json`).
  * Turno 122: El subagente se rinde y emite `send_message` pidiendo rescate al orquestador.
- **Impacto Temporal:** Shard 05 requirió 23.8 min de pared frente a la mediana de 9.5 min, generando un retraso forzado de +856.0 segundos en la barrera de sincronización de Stage 3.

---

### 7.3. Auditoría Forense Exhaustiva de las 3 Intervenciones Manuales del Orquestador

#### Intervención 1 (Paso 239 / Registro 276): Reset de Intentos de Compilación de Shard 05
- **Archivo:** `work/.check_attempts/compile_shard_05.json`
- **Operación:** `write_to_file` con `{"count": 0}` (Overwrite: true).
- **Causa Raíz:** El contador de intentos de compilación de Shard 05 alcanzó el tope de seguridad (6), impidiendo cualquier nueva ejecución de `compile_shard.py`.
- **Thinking del Orquestador:** `"Initial hypothesis: 'compile_shard.py's behavior needs to be re-evaluated due to a code change in 'shard_05_data.py'. To ensure a clean slate, resetting the state of related JSON files is necessary. This will ensure no lingering states interfere with the test. Applying the reset requires writing to a file, overwriting its existing content."`

#### Intervención 2 (Paso 241 / Registro 278): Desbloqueo de Disyuntor para Hab-12
- **Archivo:** `work/.check_attempts/circuit_breaker_Hab-12.json`
- **Operación:** `write_to_file` con `{"consecutive_count": 0, "last_hash": "", "history": []}`.
- **Causa Raíz:** Bloqueo persistente por fallos consecutivos en la plantilla matemática de `Hab-12`.
- **Acción:** Reseteo completo de hash y contador para permitir la re-validación tras la corrección del código de la plantilla.

#### Intervención 3 (Paso 307 / Registro 344): Parche de Expresiones Regulares en KaTeX Sanitizer (`assemble.py`)
- **Archivo:** `.agents/skills/content-to-course/engine/assemble.py` (Líneas 250 a 264).
- **Herramienta:** `replace_file_content`.
- **Causa Raíz en el Motor Core:** La función `sanitize_katex_syntax` contenía dos expresiones regulares (`frac_den_fix` y `script_outer_fix`) que operaban incondicionalmente sin verificar si el texto ya estaba balanceado. Cuando una fórmula contenía delimitadores `\left(` y `\right)` dentro de exponentes o fracciones (como `$u(x, y) = C e^{k \left( x + \frac{y}{a} \right)}$`), el lookahead de `script_outer_fix` interpretaba erróneamente que el exponente terminaba antes de `\right)`, insertando un `}` espurio que desbalanceaba la fórmula.
- **Thinking del Orquestador:** `"Examining the code, a pattern emerges: the system attempts to auto-repair missing closing braces in LaTeX fractions... The script_outer_fix regex mistakenly closes the superscript when encountering \right), because the superscript's closing brace is further along in the equation... The auto-repair function should only insert a closing brace if there are more opening than closing braces... The code's logic is flawed as it unconditionally inserts the closing brace. The correct behavior demands that the auto-repair should only run when the number of opening braces exceeds the number of closing braces."`
- **Código Aplicado:**
```python
    # 3. Auto-repair \frac missing denominator closing brace when denominator ends with an inner braced group
    if text.count("{") > text.count("}"):
        frac_den_fix = re.compile(...)
        text = frac_den_fix.sub(r"\1}", text)

    # 4. Auto-repair superscript/subscript missing outer closing brace after inner macro
    if text.count("{") > text.count("}"):
        script_outer_fix = re.compile(...)
        text = script_outer_fix.sub(r"\1}", text)
```

---

### 7.4. Evaluación Psicométrica y Diagnóstico de Blind Judges (Stage 5 / 5b)
- **Desempeño Global:** 11 subagentes evaluaron en paralelo 130 reactivos estratificados (2 por competencia) con estricto aislamiento epistémico (0 accesos web, 0 HTTP, 100% razonamiento LLM).
- **Tasa de Acuerdo Registrada:** **`98.46%`** (128 de 130 ítems consensuados), superando holgadamente el criterio de aprobación `>= 95.0%`.
- **Causa Raíz de los 2 Desacuerdos:**
  * Ítems: `T-H-10_judge_1` (competencia `H-10`) y `T-Hab-21_judge_1` (competencia `Hab-21`).
  * Veredicto de los Jueces: `BLOCKED: Reactivo carece de contexto matemático autosuficiente`.
  * Explicación causal: El generador de lotes para jueces (`judge_batch.json`) omitió transferir la matriz $A$ de referencia o el sistema de EDOs al enunciado presentado al juez. Al no contar con los datos matemáticos indispensables en el cuerpo de la pregunta, los jueces activaron correctamente el protocolo de protección contra reactivos ambiguos.
- **Clarificación de Dictamen:** El reporte determinista señaló "falló al primer intento" exclusivamente porque la regla estricta de `audit_engine.py` exige 100% (`agreement_rate == 1.0`). Sin embargo, en la ejecución real el pipeline **no requirió ciclos de auto-reparación (`c2c_repair`) ni intervención humana en Stage 5**, aprobándose el lote para publicación inmediata.

---

### 7.5. Clasificación Técnica Rigurosa de los 61 Errores (0% Caja Negra)
Los 61 errores catalogados corresponden a 10 categorías técnicas concretas:
- **Missing File / Relative Path / Directory Error (18):** 14 llamadas erróneas de Cortex en `view_file` con `ContentOffset` fuera de rango en archivos menores a 8 KB; 4 exploraciones de rutas por el orquestador.
- **Parameter Diversity & Option Collapse (11):** Detección en dry-run y compilación preliminar de opciones duplicadas o colapsadas algebraicamente (4 en Shard 05).
- **Exploratory Python One-Liner / Script Exceptions (9):** Fallos de sintaxis en scripts de una línea (`python -c`) ejecutados por el orquestador durante depuración.
- **Shard Compilation & Template Validator Failure (9):** Fallos sintácticos en archivos de datos de shards y alcance del límite `[COMPILE 8/6]`.
- **Python Environment / Virtualenv / Encoding Discrepancy (4):** Discrepancias de `sys.path` al invocar módulos internos.
- **File Edit / Write Tool Target Mismatch (4):** Fallos de reemplazo en `replace_file_content` por discrepancias de espacios en blanco en Shard 02 y 04.
- **Non-Zero CLI Exit / Subprocess Probe (2):** Intentos redundantes de `define_subagent` para tipos ya existentes.
- **LaTeX Control Character / Raw-String Corruption (2):** Uso de escapes de barra invertida sin raw-string en Shard 04 y 07.
- **CTA Compilation & Schema Errors (1):** Validación preliminar de esquema en Stage 1B.
- **PowerShell Command / Quoting / $Variable Expansion Friction (1):** Comando de consola incompatible con el host en Shard 05.

---

### 7.6. Síntesis Forense Comparativa Longitudinal (5 Corridas de 2026-10-19)

| Métrica Forense | `afb5aa18` (Coarse v2) | `f9b9d459` (Standard - Target) | `a53e6af1` (Coarse) | `acdc402d` (Fine) | `4ceacf92` (Solow v15) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Páginas Fuente** | 103 págs | **103 págs** | 103 págs | 103 págs | 36 págs |
| **Competencias Extraídas** | 14 comps | **65 comps** | 13 comps | 118 comps | 15 comps |
| **Preguntas Generadas** | 370 preguntas | **1,590 preguntas** | 320 preguntas | 2,850 preguntas | 360 preguntas |
| **Tiempo de Pared (min)** | 60.03 min | **64.22 min** | 32.83 min | 85.65 min | 27.10 min |
| **Tokens Totales Facturables** | 59.27 M | **71.44 M** | 21.13 M | 102.72 M | 22.06 M |
| **Tokens / Pregunta** | 160,187 tok/q | **44,933 tok/q** | 66,027 tok/q | 36,040 tok/q | 61,291 tok/q |
| **Segundos / Pregunta** | 9.74 s/q | **2.42 s/q** | 6.16 s/q | 1.80 s/q | 4.52 s/q |
| **Throughput (QPM)** | 6.16 QPM | **24.76 QPM** | 9.74 QPM | 33.27 QPM | 13.28 QPM |
| **Veredicto Arquitectónico** | Desperdicio severo de tokens | **Equilibrio óptimo producción/costo** | Rápido pero superficial | Máxima producción / Costo extremo | Consistente / Teórico |

---

### 7.7. Recomendaciones Accionables de Optimización para el Pipeline C2C
1. **Pre-validación Sintáctica AST de KaTeX en Subagentes Autores:** Incorporar un linter previo que verifique balance de llaves KaTeX antes de invocar `compile_shard.py`, evitando agotar los 6 intentos permitidos.
2. **Guarda Permanente en `engine/assemble.py`:** Blindar formalmente el código base de C2C con la guarda condicional `if text.count("{") > text.count("}"):` para impedir corrupciones automáticas de fórmulas balanceadas.
3. **Autosuficiencia en Lotes de Blind Judges (`judge_batch.json`):** Asegurar que el exportador copie obligatoriamente los objetos matemáticos base en el enunciado del ítem ciego para evitar bloqueos por falta de contexto.
4. **Instrucción de Lectura Paginada en Prompts de Jueces:** Corregir el system prompt de `c2c_judge` prohibiendo el uso de `ContentOffset` en la primera lectura de archivos pequeños.
5. **Idempotencia en Registro de Agentes (`define_subagent`):** Verificar existencia previa del agente antes de emitir llamadas de definición en el orquestador.

---
*Informe forense de traceback enriquecido por `c2c-run-auditor` (Paso B Agéntico).*
