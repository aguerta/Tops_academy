# BRIEFING — Pre-Flight Stream 1E (Fase 1: Implementador)

- **Stream:** 1E (`c2c_v38_mastery_triband_reengineering`)
- **Implementer Conversation ID:** `b5487fb7-d045-44aa-9740-1ad693f75575`
- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Timestamp:** 2026-10-31

---

## 1. Archivos Asignados y Líneas Exactas Inspeccionadas

### 1.1 `repair_loop.py` (`.agents/skills/content-to-course/repair_loop.py`)
- **Líneas 58-201:** `RepairLoop.repair_course()`. Contiene la orquestación de Pass A (lexical LaTeX) y Pass B (mutadores sintéticos B1 a B8).
- **Líneas 255-357:** `_repair_giveaway_lengths` (Module B) con lista `shared_pads` (`", bajo las hipótesis del modelo."`, etc.) y mutación de `c_opt["content"]` / `distractors[idx]["content"]`. **ACCION:** Eliminar completamente.
- **Líneas 362-428:** `_repair_quota_shortfalls` (Module C) con inyecciones de `"Distractor homogéneo A"`. **ACCION:** Eliminar completamente.
- **Líneas 433-448:** `_repair_hint_counts` (Module D). **ACCION:** Eliminar completamente.
- **Líneas 453-497:** `_repair_mc_cardinality` (Module E1) con inyección de `"Alternativa complementaria..."`. **ACCION:** Eliminar completamente.
- **Líneas 498-532:** `_repair_ms_cardinality` (Module E2) con inyección de `"Propiedad complementaria..."`. **ACCION:** Eliminar completamente.
- **Líneas 533-547:** `_repair_fib_answers` (Module E3). **ACCION:** Eliminar completamente.
- **Líneas 552-575:** `_repair_strict_fields` (Module F). **ACCION:** Eliminar completamente.
- **Líneas 576-583:** `_repair_competency_descriptions`. **ACCION:** Eliminar completamente.
- **Líneas 207-249:** `sanitize_latex_escapes` (Module A). **ACCION:** Conservar íntegramente como único motor determinista de corrección léxica.
- **Contrato:** Conservar clases `RepairLoop`, `RepairResult`, `RepairIterationReport` con firmas compatibles para `run.py` y `course_publisher.py` (`repair_course()` y alias `run()`).

### 1.2 `src/validator/psychometric_checker.py`
- **Líneas 55-62:** 
  ```python
  is_longest = (len_c >= max_d)
  is_shortest = (len_c <= min_d)
  ```
  **Problema detectado:** Cuando `len_c == max_d == min_d` (empate exacto, ej. 7 opciones de longitud uniforme `$O(n^{-1/2})$`), ambas banderas se activaban simultáneamente en el 100% de las preguntas, disparando falsos positivos de `ERR_GIVEAWAY_COURSE` (R-16).
  **ACCION:** Cambiar a desigualdad estricta:
  ```python
  is_longest = (len_c > max_d)
  is_shortest = (len_c < min_d)
  ```

### 1.3 `src/validator/rules.py`
- **Líneas 404-828 (`check_latex_and_templates`):**
  - **Paridad `[KATEX-PROSE-OVERFLOW]`:** Implementar análisis de llaves balanceadas sobre `\text{...}`, `\textrm{...}`, `\mathrm{...}`. Si la longitud interna supera 45 caracteres, emitir `ValidationError(rule_id="R-20", code="ERR_KATEX_PROSE_OVERFLOW", message="Question '{q_id}' in {field_desc}: [KATEX-PROSE-OVERFLOW] ...", item_id=q_id)`.
  - **Importante:** Registrar con `rule_id="R-20"` (NUNCA `R-23`), garantizando que la suite `test_katex_overescape_validator_r23.py` (que audita cursos legados en `courses/*.json` filtrando `e.rule_id == "R-23"`) mantenga 0 errores de regresión.
- **Líneas 349-401 (`check_boilerplate_distractors_local`):**
  - **Desenvoltura `\text{...}`:** Desenvolver bloques `\text{...}`, `\textrm{...}`, `\mathrm{...}` dentro de delimitadores matemáticos (`$...$`, `$$...$$`) antes de calcular esqueletos y evaluar umbrales alfanuméricos, exponiendo prosa repetitiva camuflada en modo matemático.
- **Líneas 938-946 (`check_extended_quality_rules` en opciones):**
  - **Anti-Pad (`ERR_SYNTHETIC_PAD`, `rule_id="R-18"`):** Detección determinista de muletillas de relleno sintético en `opt_content` (y su versión desenvuelta):
    - `"bajo las premisas y condiciones del modelo"`
    - `"en el marco de las condiciones establecidas"`
    - `\bopci[oó]n\s+alterna\b`
    - `\bdistractor\s+homog[eé]neo\b`

### 1.4 `tests/test_validator.py` y `tests/test_katex_overescape_validator_r23.py`
- **Línea base previa:** 181 passed en 15.69s.
- **ACCION:** Añadir pruebas unitarias y adversarias verificando:
  1. `RepairLoop` ejecuta exclusivamente el Módulo A (sanea escapes LaTeX) y nunca altera longitudes ni inyecta padding textual.
  2. Empates simbólicos `len_c == max_d == min_d` generan 0 errores en R-16.
  3. `\text{...}` > 45 caracteres dispara `ERR_KATEX_PROSE_OVERFLOW` con `rule_id="R-20"`, mientras <= 45 caracteres pasa limpio.
  4. Muletillas de padding burocrático disparan `ERR_SYNTHETIC_PAD` (`rule_id="R-18"`).
  5. Boilerplate camuflado en `$\text{...}$` es detectado por `ERR_SYNTHETIC_BOILERPLATE`.
  6. Preservación del 100% de aprobación en las suites existentes y regresión de cursos publicados.

---

## 2. Contratos y Restricciones Específicas

1. **Frontera Exclusiva de Escritura:**
   Únicamente se editarán los 5 archivos del workspace especificados + `BRIEFING.md` y `handoff.md`.
2. **Regla Zero-Domain en `repair_loop.py`:**
   Prohibido incluir las subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. Todo comentario o docstring nuevo será redactado en inglés limpio sin esas raíces.
3. **Guardias de Hooks:**
   Toda ejecución de pruebas utilizará estrictamente:
   `& ".venv\Scripts\python.exe" -m pytest tests/test_validator.py tests/test_katex_overescape_validator_r23.py -q`.

---

## 3. Plan de Modificación Secuencial

1. Modificar `src/validator/psychometric_checker.py` con desigualdad estricta.
2. Modificar `src/validator/rules.py` incorporando desenvolvimiento de `\text{...}` en distractores, `[KATEX-PROSE-OVERFLOW]` (`rule_id="R-20"`, `code="ERR_KATEX_PROSE_OVERFLOW"`) y `ERR_SYNTHETIC_PAD` (`rule_id="R-18"`).
3. Modificar `repair_loop.py` purgando mutadores sintéticos B–F y conservando exclusivamente el Módulo A con soporte para `run()` y `repair_course()`.
4. Extender `tests/test_validator.py` y `tests/test_katex_overescape_validator_r23.py` con las pruebas unitarias y adversarias requeridas.
5. Ejecutar la suite completa y validar 100% PASS sin regresiones ni violaciones Zero-Domain.
6. Generar `handoff.md` y notificar al agente padre.
