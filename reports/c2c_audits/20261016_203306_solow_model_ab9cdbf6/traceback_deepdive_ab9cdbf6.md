# Deep-Dive Forense de Trazas, Thinking Traces y Taxonomía de los 91 Errores (`ab9cdbf6`)

> **ID de Conversación Raíz (Orquestador)**: `ab9cdbf6-d44c-4ab2-b3bd-4575b6ae7b8f`
> **Curso Auditado**: `solow_model` ("Solow Model")
> **Directorio de Trabajo**: [`courses/solow_model/work/`](file:///d:/Augusto/personal_portfolio/Tops_academy/courses/solow_model/work)
> **Total de Conversaciones Inspeccionadas**: **13** (`1` Orquestador + `1` Direct CTA Architect + `6` Shard Authors + `5` Blind Judges)

---

## 1. Desglose de Tiempo de Pared: Inferencia LLM vs. Ejecución de Herramientas

| Agente / Subagente | ID Conversación | Tiempo Pared | Inferencia LLM | % Inf. | Ejecución Tools | % Tool | Turnos | Turnos c/ Thinking | Chars Thinking | Tokens Activos | Errores Tool |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Director (Orchestrator)** | `ab9cdbf6-d44c-4ab2-b3bd-4575b6ae7b8f` | **4824.0s** (`80.40m`) | `4542.0s` *(incl. waits)* | `94.2%` | `282.0s` | `5.8%` | **253** | 81 | `33,469` | `1,287,747` | **26** |
| **Direct CTA Architect** | `d8f1dd6f-6984-4640-864c-e92a06695946` | **1197.0s** (`19.95m`) | `1176.0s` | `98.2%` | `21.0s` | `1.8%` | **33** | 20 | `65,892` | `417,316` | **6** |
| **Author `shard_01`** | `99522bb8-953a-4b02-a65a-953f0f42d092` | **1034.0s** (`17.23m`) | `924.0s` | `89.4%` | `100.0s` | `9.7%` | **70** | 18 | `40,724` | `594,053` | **8** *(+1 async)* |
| **Author `shard_02`** | `55d7764b-1170-4251-a28d-ac7f72911e91` | **1364.0s** (`22.73m`) | `1199.0s` | `87.9%` | `142.0s` | `10.4%` | **130** | 55 | `60,341` | `651,857` | **12** *(+1 async)* |
| **Author `shard_03`** | `79de8018-bb8b-4b4b-8502-79fd5682f132` | **707.0s** (`11.78m`) | `622.0s` | `88.0%` | `85.0s` | `12.0%` | **80** | 26 | `40,192` | `350,708` | **10** |
| **Author `shard_04` 🛑** | `cb54ea87-4604-44b4-a921-b26cc954ab7c` | **1468.0s** (`24.47m`) | `1319.0s` | `89.9%` | `148.0s` | `10.1%` | **135** | 46 | `53,332` | `581,396` | **16** *(+1 async)* |
| **Author `shard_05`** | `e29b37b4-e2ab-4aa6-8e86-2960389d8f29` | **766.0s** (`12.77m`) | `689.0s` | `89.9%` | `77.0s` | `10.1%` | **77** | 25 | `40,704` | `401,970` | **7** |
| **Author `shard_06`** | `10c19faf-04c4-4d2c-ae75-c810fd4edd25` | **741.0s** (`12.35m`) | `657.0s` | `88.7%` | `84.0s` | `11.3%` | **80** | 33 | `44,311` | `520,615` | **7** |
| **Blind Judge 01** | `28044e4a-df52-415d-a5fb-a92989e89da1` | **55.0s** (`0.92m`) | `55.0s` | `100.0%` | `0.0s` | `0.0%` | **3** | 1 | `7,800` | `43,037` | **0** |
| **Blind Judge 02** | `78c93382-1c23-4b68-a1a1-8931d51a65cc` | **63.0s** (`1.05m`) | `63.0s` | `100.0%` | `0.0s` | `0.0%` | **3** | 1 | `7,364` | `43,849` | **0** |
| **Blind Judge 03** | `baa3ebb2-ca49-43fd-9d37-147f6d4aabb6` | **65.0s** (`1.08m`) | `65.0s` | `100.0%` | `0.0s` | `0.0%` | **3** | 1 | `12,127` | `47,125` | **0** |
| **Blind Judge 04** | `bc062d44-f245-49b1-9b1f-696e281b3ae3` | **69.0s** (`1.15m`) | `69.0s` | `100.0%` | `0.0s` | `0.0%` | **2** | 1 | `9,360` | `49,214` | **0** |
| **Blind Judge 05** | `f60af888-b862-473d-9459-0b62d3a1fe3c` | **61.0s** (`1.02m`) | `61.0s` | `100.0%` | `0.0s` | `0.0%` | **2** | 1 | `9,878` | `42,545` | **0** |
| **TOTAL / AGREGADO** | **13 Agentes** | **4824.0s Pared** (`12414s` Cómputo) | **95.8% Prom.** | — | **4.2% Prom.** | — | **871** | **309** | **`425,494`** | **`5,031,432`** | **91** *(+4 async)* |

---

## 2. Radiografía Turno por Turno de los Agentes Críticos (`thinking_traces` + Herramientas)

### 2.1. `Direct CTA Architect` (`d8f1dd6f-6984-4640-864c-e92a06695946`)
- **Cronología de sus 33 turnos (`1197.0s`)**:
  - **Steps 1–5 (`00:11:38` – `00:11:53`)**: Lee el prompt `cta_01.json` y el manifiesto `pre_cta_manifest.json` (`3` llamadas a `view_file`).
  - **Steps 7–13 (`00:12:04` – `00:16:57`)**: En lugar de escribir un único archivo `cta_data.py` con raw strings `r"..."`, escribe el archivo en **4 lotes secuenciales** (`write_to_file`):
    * **Step 7** (`21,616` output tokens, `130s`): Escribe la cabecera y el Lote 1 (`05_15_07_El_modelo_de_crecimiento_de_Solow.pdf`, Chiang cap. 15.7, 7 competencias), usando correctamente `$ ... $` pero mezclando strings normales `"..."` con expresiones LaTeX.
    * **Step 9** (`11,128` output tokens, `85s`): Hace `Append=True` con el Lote 2 (`solow1956.pdf` págs. 2–12), **omitiendo los delimitadores `$ ... $`** en decenas de fórmulas dentro de `wrong_belief` y `correct_belief`.
    * **Step 11** (`12,256` output tokens, `78s`): Hace `Append=True` con el Lote 3 (`solow1956.pdf` págs. 13–21), nuevamente sin `$ ... $` y con `"Cálculo de razón capital-trabajo estacionaria con función CES ($\rho = 1/2$)"` sin prefijo `r` en la línea 1104 (`Hab-07`).
    * **Step 13** (`13,355` output tokens, `88s`): Hace `Append=True` con el Lote 4 (`solow1956.pdf` págs. 22–31) y el bloque `if __name__ == "__main__": compile_cta(...)`.
  - **Steps 15–31 (`00:18:25` – `00:21:14`, 6 errores de consola)**:
    * **Step 15–16**: Ejecuta `python courses/solow_model/work/cta_data.py`. Falla con >216 líneas de errores `[CTA-SCHEMA]` por comandos LaTeX fuera de `$ ... $` y por variables `{k}`, `{dz}`, `{dt}` detectadas dentro de `remediation_hint`.
    * **Step 21–22**: Ejecuta un script inline para listar los errores de `compile_cta.py`. En su `thinking_trace` de Step 22 concluye: *"The initial hypothesis is that missing LaTeX delimiters are causing most of the errors in distractors and mathematical expressions."*
    * **Step 23–24**: Ejecuta un validador en Python que imprime `SyntaxWarning: invalid escape sequence '\i'`, `'\p'`, `'\l'`, `'\d'`.
    * **Step 25–26**: Vuelve a correr `cta_data.py` filtrando los primeros 35 errores y descubre que `compile_cta.py` rechaza cualquier `{identificador}` en `remediation_hint` (`Unsubstituted template variable '{k}' in remediation_hint`).
    * **Step 27–28**: Intenta leer `compile_cta.py` usando una ruta mal formada `D:/.agents/skills/content-to-course/compile_cta.py` (Error: `invalid path`), corregida en Step 29.
  - **Steps 33–59 (`00:21:18` – `00:31:35`, ~10.3 min de reemplazos masivos)**:
    * Ejecuta **6 llamadas a `replace_file_content`**: 3 ediciones puntuales (Steps 37, 39, 41) para limpiar `{k}`, `{s}`, `{ah}` en los hints del Lote 1, seguidas de **3 reescrituras masivas de ~500 líneas cada una** (Step 47: `14,768` output tokens en `153s`; Step 51: `15,436` output tokens en `146s`; Step 55: `15,826` output tokens en `155s`) para agregar `$ ... $` a los Lotes 2, 3 y 4.
    * En **Step 59** (`00:31:22`), `cta_data.py` compila `[OK] CTA compiled successfully: 33 competencies, 198 distractors`, pero deja **33 cadenas sin prefijo `r"..."`** (incluyendo `\rho` $\to$ `\x0d` en `Hab-07` y `\frac` $\to$ `\x0c` en `D-Hab03-01`).

---

### 2.2. Tabla Comparativa Real de los 6 Shard Authors (Corrigiendo el Analizador Headless)

> [!NOTE]
> El script headless original reportó `Check Runs: 0` para `shard_02`, `25` para `shard_06`, y `Micro-Bucle: NO` para `shard_02` (130 turnos) y `shard_04` (135 turnos) porque buscaba ingenuamente la subcadena `"check_templates.py"` en los comandos ejecutados (contando las 20 lecturas de código de `shard_06` como ejecuciones de validación e ignorando las ejecuciones reales de `compile_shard.py` / `shard_0X_data.py`). La tabla siguiente refleja la contabilidad forense real:

| Shard Author | Competencias (`solow_model`) | Turnos | Lecturas de Ing. Inversa (Steps Iniciales) | Escrituras / Ediciones en `shard_0X_data.py` | Ejecuciones Reales de `compile_shard` (Pass / Fail) | Micro-Bucle Real (>30 turnos) | Causa Raíz Principal de Fricción |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **`shard_01`** | `H-01, C-01, H-02, Hab-01, C-02, C-03` (6) | **70** | **21 lecturas** (Steps 1–55, `4.5m`) | 1 write + 9 edits | **4 runs** (1 Pass / 3 Fail) | **SÍ** (70 turnos) | Ing. inversa inicial + `TPL-VAR` (`C-01, C-02`) + `R-18` (`"asumiendo erróneamente"` en `C-01`) + `R-16` longitud en `C-03`. |
| **`shard_02`** | `Hab-02, Hab-03, C-04, H-03, Hab-04, C-05` (6) | **130** | **25 lecturas** (Steps 1–51 + 143–248) | 3 writes + 2 edits | **3 runs** (1 Pass / 2 Fail) + 18 pruebas Python inline | **SÍ (Severo: 130 turnos)** | **57 turnos (Steps 142–256)** diagnosticando `R-03 LaTeX corruption` en `Hab-03` causada por `\frac` (`\x0c`) y `\alpha` (`\x07`) en `D-Hab03-01` dentro de `cta.json`. Resuelto permutando `D-Hab03-02` al índice 0. |
| **`shard_03`** | `C-06, C-07, C-08, Hab-05, Hab-06, H-04` (6) | **80** | **29 lecturas** (Steps 1–91, `5.5m`) | 1 write + 4 edits | **6 runs** (2 Pass / 4 Fail) | **SÍ** (80 turnos) | Ing. inversa inicial (leyó `work/templates/C-07.json` obsoleto) + llaves dobles `{{a}}` en raw string (`H-04`) + `R-16` longitud + `TPL-VAR` (`C-06` 48/50). |
| **`shard_04` 🛑** | `Hab-07, C-09, H-05, C-10, Hab-08` (5) | **135** | **32 lecturas** (Steps 1–98 + 126–227) | 3 writes + 6 edits | **12 runs** (2 Pass / 10 Fail) | **SÍ (Crítico: 135 turnos)** | **58 turnos (Steps 125–240)** diagnosticando `R-03 LaTeX corruption` en `Hab-07` causada por `\rho` (`\x0d`) en el título de `Hab-07` en `cta.json`, más `R-18` en `H-05` y `TPL-VAR` en `C-09` y `Hab-07`. |
| **`shard_05`** | `Hab-09, Hab-10, C-11, Hab-11, C-12` (5) | **77** | **19 lecturas** (Steps 1–58, `4.8m`) | 1 write + 6 edits | **7 runs** (2 Pass / 5 Fail) | **SÍ** (77 turnos) | Ing. inversa inicial + `TPL-VAR` en `Hab-10` y `C-12` (36/50) + `R-18` en `C-11` (`"asumiendo erróneamente"`) + `R-16` longitud en `Hab-09, Hab-11`. |
| **`shard_06`** | `Hab-12, C-13, C-14, Hab-13, C-15` (5) | **80** | **35 lecturas** (Steps 1–104, `6.2m`) | 2 writes + 0 edits | **5 runs** (1 Pass / 4 Fail) | **SÍ** (80 turnos) | **52 turnos iniciales** leyendo `check_templates.py` en rodajas con `python -c` antes de escribir código + `TPL-VAR` en `Hab-13` + `R-16` longitud en `C-13, C-14, C-15`. |

---

## 3. Taxonomía Completa de los 91 Errores de Consola / Herramientas (0% Cajas Negras)

A continuación se desglosan **todos y cada uno de los 91 errores** registrados en `traceback_deepdive_ab9cdbf6.json`, eliminando por completo la categoría genérica `"Other Console / Tool Failures"` (que agrupaba 66 errores en el reporte headless).

### Categoría 1: Errores de API, Import, Type o Key en One-Liners Python Ad-hoc durante Ingeniería Inversa (**28 errores — 30.77%**)
Ocurrieron cuando el Orquestador o los Shard Authors ejecutaron scripts exploratorios `python -c "..."` llamando funciones internas del motor con argumentos incorrectos, módulos sin `PYTHONPATH` o claves JSON inexistentes:
1. **`Orchestrator` Step 205**: `ModuleNotFoundError: No module named 'judge'` al intentar importar `judge` sin añadir `.agents/skills/content-to-course` a `sys.path`.
2. **`Orchestrator` Step 230**: `KeyError: 'role'` inspeccionando la estructura de `transcript.jsonl` de `shard_01` para entender cómo se registraban las llamadas de herramientas.
3. **`Orchestrator` Step 240**: `TypeError: string indices must be integers, not 'str'` iterando sobre `step.get('tool_calls')` en `transcript.jsonl`.
4. **`Orchestrator` Step 242**: `KeyError: slice(None, 2, None)` aplicando un slice `[:2]` sobre un `dict` en `transcript.jsonl`.
5. **`Orchestrator` Step 258**: `AttributeError: 'list' object has no attribute 'get'` al inspeccionar `subagent_step` en `transcript.jsonl`.
6. **`Orchestrator` Step 266**: `AttributeError: 'str' object has no attribute 'get'` al parsear bloques `output` en `transcript.jsonl`.
7. **`Orchestrator` Step 270**: `UnicodeEncodeError: 'charmap' codec can't encode character '\u2713'` al imprimir en consola Windows (`cp1252`) el resumen de un subagente sin `PYTHONIOENCODING=utf-8`.
8. **`Author Shard 02` Step 88**: `TypeError: assemble_question() missing 3 required positional arguments: 'comp_info', 'distractor_map', and 'rng'` al probar `assemble_question(t)` manualmente.
9. **`Author Shard 02` Step 118**: `ModuleNotFoundError: No module named 'validator'` al ejecutar `from validator.rules import check_r18` sin configurar `sys.path`.
10. **`Author Shard 02` Step 126**: `AttributeError: module 'src.validator.rules' has no attribute 'meta_giveaway_regex'` al adivinar el nombre de la expresión regular de `R-18`.
11. **`Author Shard 02` Step 168**: `ImportError: cannot import name 'LexicalScanner' from 'src.validator.lexical_scanner'` durante el diagnóstico del fallo `R-03` en `Hab-03`.
12. **`Author Shard 02` Step 182**: `ImportError: cannot import name '_evaluate_comp_diversity_and_parity' from 'check_templates'` mientras buscaba dónde se originaba el fallo `R-03` de `Hab-03`.
13. **`Author Shard 03` Step 56**: `ModuleNotFoundError: No module named 'check_templates'` al importar sin añadir `.agents/skills/content-to-course` a `sys.path`.
14. **`Author Shard 03` Step 62**: `json.decoder.JSONDecodeError: Invalid \escape` al leer por error el archivo obsoleto `work/templates/C-07.json` de una corrida previa.
15. **`Author Shard 03` Step 90**: `AttributeError: name 'inspect' is not defined` (olvidó `import inspect` en su one-liner).
16. **`Author Shard 03` Step 102**: `TypeError: assemble_question() missing 3 required positional arguments` al invocar `assemble_question(t, p)` directamente.
17. **`Author Shard 03` Step 114**: `ValueError: Length anti-giveaway violation (len(C)=162 not in [50.4, 158.4])` + `NameError: name 'millones' is not defined` al ejecutar un barrido manual sobre `TEMPLATES` en `shard_03_data.py`.
18. **`Author Shard 04` Step 50**: `NameError: name 'os' is not defined` en un one-liner que usaba `os.listdir` sin `import os`.
19. **`Author Shard 04` Step 60**: `ModuleNotFoundError: No module named 'pypdf'` antes de cambiar a `fitz` (`pymupdf`) para leer `solow1956.pdf`.
20. **`Author Shard 04` Step 149**: `TypeError: instantiate_competency() takes from 2 to 4 positional arguments but 5 were given` durante el diagnóstico de `Hab-07`.
21. **`Author Shard 04` Step 153**: `AttributeError: 'str' object has no attribute 'get'` pasando argumentos en orden invertido a `instantiate_competency`.
22. **`Author Shard 04` Step 157**: `ModuleNotFoundError: No module named 'validator'` intentando importar `validator.lexical_scanner` sin el prefijo `src.`.
23. **`Author Shard 04` Step 159**: `ImportError: cannot import name 'scan_lexical_tokens' from 'src.validator.lexical_scanner'` adivinando el nombre de la función en `lexical_scanner.py`.
24. **`Author Shard 04` Step 175**: `ValueError: Template T-C-09 produced 0 valid instances after 400 attempts: Cross-check verification returned False` al probar `instantiate_template` sobre `C-09`.
25. **`Author Shard 05` Step 70**: `TypeError: execute_sandbox_batch() got multiple values for keyword argument 'seeds'` al llamar `execute_sandbox_batch` manualmente.
26. **`Author Shard 05` Step 72**: `SyntaxError: invalid syntax (<unknown>, line 1)` dentro de `validate_code_ast` al pasar el ID de la plantilla (`'T-Hab-09'`) en vez del código fuente Python.
27. **`Author Shard 05` Step 84**: `TypeError: validate_katex_syntax() missing 1 required positional argument: 'context'` al llamar `validate_katex_syntax` con 1 solo argumento.
28. **`Author Shard 06` Step 106**: `ModuleNotFoundError: No module named 'pypdf'` antes de usar `fitz` (`pymupdf`).

---

### Categoría 2: Fricción de Quoting en PowerShell, Expansión de `$var` y Sintaxis en `python -c` (**21 errores — 23.08%**)
Ocurrieron porque los agentes ejecutaron `python -c "..."` en PowerShell incluyendo comillas dobles sin escapar, operadores `|` o variables con `$` (`$schema`, `$F(r,1)`) que PowerShell interpoló antes de invocar a Python:
1. **`Orchestrator` Steps 141, 149, 151, 157** (4 errores): Errores de sintaxis PowerShell/Python al intentar escribir una expresión regular `r'(?<!r)\"([^\"\\n]*\\\\[^\"\\n]*)\"'` inline en `python -c` para buscar strings no-raw en `cta_data.py` (lo que llevó al Orquestador a crear `check_escapes.py`).
2. **`Orchestrator` Steps 298, 300** (2 errores): Errores de quoting en PowerShell (`$_` expandido a vacío) al consultar `Get-WinEvent` / procesos tras el borrado externo de `courses/solow_model`.
3. **`Orchestrator` Step 392** (1 error): `SyntaxError: unexpected character after line continuation character` en `python -c` al intentar parchar escapes de `cta_data.py` inline antes de escribir `fix_cta.py`.
4. **`Author Shard 01` Steps 48, 112** (2 errores): `SyntaxError` por comillas dobles anidadas en `python -c` al buscar `"check_production_parity"` y al medir longitudes de opciones en `shard_01_data.py`.
5. **`Author Shard 02` Steps 80, 116, 176, 206** (4 errores): En Step 80, PowerShell expandió `$schema` dentro de `python -c "... '$schema' ..."`, dejando `''` y causando `SyntaxError: Octal literal (\'...)`; en Steps 116, 176 y 206, comillas dobles sin escapar dentro de `python -c`.
6. **`Author Shard 03` Steps 64, 124** (2 errores): En Step 64, el pipe `|` dentro de `r'\$(?!\d)[^$]+?\$|\$\$[\s\S]+?\$\$'` fue interpretado por PowerShell como un pipeline de comandos; en Step 124, PowerShell expandió `$F(r, 1)` como variable `$F` dentro de un `python -c`.
7. **`Author Shard 04` Steps 4, 28, 38** (3 errores): En Step 4 encadenó dos comandos con `&&` (no soportado en Windows PowerShell 5.1); en Steps 28 y 38 usó comillas dobles sin escapar dentro de `python -c`.
8. **`Author Shard 06` Steps 58, 60, 142** (3 errores): Comillas dobles sin escapar en `python -c` al buscar `"def compile_shard"` (S58, S60) y al medir longitudes de `C-15` (S142).

---

### Categoría 3: Errores de Sistema de Archivos, Borrado Externo del Workspace y Rutas Relativas/Inexistentes (**20 errores — 21.98%**)
1. **`Orchestrator` Steps 276, 282, 335, 341, 398** (5 errores del incidente de borrado externo):
   - **S276 y S282**: `FileNotFoundError: [WinError 3] El sistema no puede encontrar la ruta especificada: 'courses/solow_model'` cuando el directorio fue eliminado externamente.
   - **S335**: `Get-Process` retornó exit code 1 al no haber procesos activos con ventana coincidente.
   - **S341**: `manage_task kill` sobre la tarea background de `run.py --stage verify` que ya había terminado (`already in DONE state`).
   - **S398**: `BLOCKER:: No existe pre_cta_manifest.json` al intentar compilar `cta_data.py` recuperado antes de re-ejecutar `run.py --stage prepare`.
2. **`Orchestrator` Steps 165, 425, 529** (3 errores de herramientas/rutas):
   - **S165**: `replace_file_content` no encontró el bloque exacto en `cta_data.py` por secuencias de escape.
   - **S425**: `replace_file_content` rechazó la ruta relativa `courses/solow_model/work/shards/shard_02_data.py` (`TargetFile must be an absolute path`).
   - **S529**: `python .agents/skills/content-to-course/validate_course.py` falló con `No such file or directory` (el validador se invoca vía `run.py --stage verify` o `src/validator/`).
3. **Subagentes (`12` errores por consultar archivos o carpetas antes de crearlos o con rutas erróneas)**:
   - **`Direct CTA Architect` S28**: `view_file` con ruta inválida `D:/.agents/...`.
   - **`Author Shard 01` S18, S70, S110**: `Get-ChildItem courses/solow_model/work/templates` antes de que existiera la carpeta `templates/` (S18); `view_file` en `src/engine/assemble.py` en vez de `.agents/skills/content-to-course/engine/assemble.py` (S70); `Select-String` con exit code 1 al no hallar coincidencias para `"C-03"` en los errores (S110).
   - **`Author Shard 02` S14**: `view_file` sobre `shard_01_data.py` cuando `shard_01` aún no lo había creado.
   - **`Author Shard 03` S120**: `run_command` con `Cwd: courses/solow_model/work/shards` relativo duplicado.
   - **`Author Shard 04` S64, S94, S147**: Rutas inexistentes `courses/solow_model/solow1956.pdf` (estaba en `content/Solow_model/solow1956.pdf`, S64), `src/engine/assemble.py` (S94) y `courses/solow_model/work/shards/Hab-07.json` (estaba en `work/templates/Hab-07.json`, S147).
   - **`Author Shard 05` S22**: `Get-ChildItem courses/solow_model/work/templates` antes de compilar plantillas.
   - **`Author Shard 06` S4, S90**: `view_file` con ruta relativa `.agents/...` (S4) y `view_file` sobre `tests/test_compile_shard.py` inexistente (S90).

---

### Categoría 4: Violaciones de Cuota de Diversidad Paramétrica (`TPL-VAR`: 20 / 50 Semillas) (**9 errores — 9.89%**)
Fallos legítimos de `compile_shard.py` cuando el generador `gen_*` produjo menos instancias únicas que las requeridas:
1. **`Author Shard 01` Step 106 & Step 108**: `C-01` y `C-02` generaron solo `14/20` instancias únicas por falta de parámetros variados en las tuplas de escenarios.
2. **`Author Shard 03` Step 100**: `H-04` falló al instanciar (0 instancias válidas) porque el autor escribió dobles llaves `{{a}}` y `{{L0}}` dentro de un raw string `r"""..."""` que no era f-string, dejando `{{a}}` sin sustituir (`R-20`).
3. **`Author Shard 03` Step 146**: `C-06` generó `48/50` instancias únicas bajo `--strict` (2 colisiones en 50 semillas).
4. **`Author Shard 04` Step 125**: `C-09` generó `0/20` instancias válidas en su primera corrida por discrepancia en la verificación cruzada `ver_c09`.
5. **`Author Shard 04` Step 249**: `Hab-07` generó menos de 50 semillas únicas bajo `--strict`.
6. **`Author Shard 05` Step 62**: `Hab-10` falló `TPL-VAR` en la primera compilación del shard.
7. **`Author Shard 05` Step 140**: `C-12` generó `36/50` semillas únicas bajo `--strict`.
8. **`Author Shard 06` Step 114**: `Hab-13` generó `0/20` instancias válidas porque `ver_hab13` comparaba una identidad distinta a la calculada en `gen_hab13`.

---

### Categoría 5: Fallos de Validación Psicométrica y Contrato Léxico (`R-18` Giveaway y `R-03` Corrupción LaTeX) (**6 errores — 6.59%**)
1. **Regla `R-18 (Meta-Información / Giveaway)` — 4 errores**:
   - **`Author Shard 01` Step 114 (`C-01`)**, **`Author Shard 02` Step 114 (`Hab-04`)**, **`Author Shard 04` Step 108 (`H-05`)** y **`Author Shard 05` Step 110 (`C-11`)**: `compile_shard.py` rechazó distractores que contenían las frases auto-incriminatorias `"asumiendo erróneamente"` o `"sumando erróneamente"`.
2. **Regla `R-03 (Corrupción Léxica LaTeX por Caracteres de Control de `cta.json`)` — 2 errores de compilación/verificación**:
   - **`Author Shard 02` Step 142 (`Hab-03`)**: `compile_shard.py` rechazó `Hab-03` porque `assemble.py` inyectó el `remediation_hint` de `D-Hab03-01` (que tenía `\x0c` de `\frac` y `\x07` de `\alpha` en `cta.json`) dentro de `misconception_warning`.
   - **`Orchestrator` Step 125 (`run.py --stage verify`)**: El verificador global rechazó `course.json` (`1 error`) porque el título de `Hab-07` copiado de `cta.json` contenía `\x0dho = 1/2` (`\r` de `\rho`).

---

### Categoría 6: Errores del Compilador CTA (`CTA-SCHEMA`, Delimitadores `$`, Escapes y `CTA-EV`) (**6 errores — 6.59%**)
1. **`Direct CTA Architect` Steps 16, 22, 26, 30** (4 errores): Fallos de `compile_cta.py` por expresiones LaTeX sin delimitadores `$ ... $` en los Lotes 2–4 y variables entre llaves `{k}`, `{dz}`, `{dt}`, `{s}`, `{ah}`, `{r}` en `remediation_hint`.
2. **`Direct CTA Architect` Step 24** (1 error): Fallo de ejecución al evaluar `cta_data.py` con `SyntaxWarning: invalid escape sequence '\i'`, `'\p'`, `'\l'`, `'\d'`.
3. **`Orchestrator` Step 402** (1 error): Durante la recuperación del borrado externo, `compile_cta.py` falló con `[CTA-EV] evidence_pages fora de rango` porque en el paso previo el Orquestador había corrido `prepare` apuntando solo a `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (5 págs) en lugar del directorio `content/Solow_model` (36 págs). En Step 404 re-ejecutó `prepare` sobre `content/Solow_model` y `compile_cta.py` pasó de inmediato.

---

### Categoría 7: Discrepancia de Cargador `dict` vs `list` en `run.py --stage build` (**1 error — 1.10%**)
1. **`Orchestrator` Step 95**: `run.py --stage build` terminó con `"No templates found for competency 'H-01'"` porque `compile_shard.py` serializó cada plantilla individual como un objeto JSON (`dict`), mientras que `run_stage_build` en `run.py` solo cargaba archivos JSON que contuvieran una clave `"templates"` de tipo `list`. Reparado definitivamente en **Step 118**.
