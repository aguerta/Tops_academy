# Handoff — Stream 1D (Fase 2: Mejorador)

**Fecha:** 2026-10-25  
**Stream:** `stream_1d_impr`  
**Estado:** ✅ COMPLETADO

---

## 1. Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)

Se respetó estrictamente la frontera autorizada de escritura. Únicos archivos modificados / creados:
1. `run_platform.py` (Endurecimiento de validación y auto-reparación runtime).
2. `FUTURE_MILESTONES.md` (Verificación de paridad).
3. `docs/future_milestones/FUTURE_MILESTONES.md` (Verificación de paridad byte a byte).
4. `tests/test_platform_katex_admission_guard.py` (Ampliación con tests adversarios).
5. `.agents/teamwork/c2c_v37_katex_overescape_safeguards/stream_1d_impr/handoff.md` `[NEW]`

Cero archivos de otros streams o scripts sueltos fueron tocados ni creados.

---

## 2. Endurecimiento de Casos Borde Realizado

### 2.1. Endurecimiento en `run_platform.py`:
- **`validate_platform_course` (Pass 4 en memoria):**
  - Implementada la función modular `_check_katex_invariants(text: str, context_label: str) -> tuple[bool, str | None]`, que valida en memoria:
    1. Sobre-escape de comandos LaTeX (`r"\\\\([a-zA-Z]+)"`).
    2. Saltos de línea `\\` dentro de bloques inline `$ ... $` fuera de entornos matriciales (`matrix`, `cases`, `aligned`, `array`, `split`, `gathered`), despojando recursivamente entornos anidados y protegiendo bloques display `$$ ... $$`.
  - Cobertura exhaustiva de todos los campos del curso:
    - Metadatos de curso: `title`, `course_title`, `description`.
    - Competencias: `name`, `description`, `statement` por cada competencia (detectando anomalías históricas como las observadas en `gavilano_pre_parcial.json` y `saul_control_optimo.json`).
    - Preguntas: `stem`, `detailed_solution`, `solution`, `explanation`, `common_misconception_warning`, `misconception_warning`.
    - Pistas y Opciones: `hints[*]`, `options[*].content`, `options[*].error_rationale`, `options[*].feedback`, `options[*].rationale`.
    - `fill_in_the_blank`: `correct_answer` (tanto formato string como diccionario estructurado con `value`, `expression`, `canonical_algebraic`, `formula`, `explanation`, y `accepted_equivalents` como lista o string).
- **`repair_platform_course_katex`:**
  - **Colapso de sobreescapes:** Soporte para colapsar secuencias de 6 barras invertidas crudas adyacentes a comandos (`\\\\\cmd` sin espacio $\to$ `\\\\ \\cmd`), preservando intactos los saltos de fila de matrices.
  - **Mapeo completo de macros `\centernot`:** Cubiertas todas las flechas especificadas (`\Rightarrow`, `\implies`, `\Leftarrow`, `\impliedby`, `\Leftrightarrow`, `\iff`, `\rightarrow`, `\to`, `\leftarrow`, `\gets`, `\leftrightarrow`, y fallback a `\not`).
  - **Reparación de saltos inline ilegales:** Sustitución segura de `\\` fuera de entornos matriciales en bloques inline `$ ... $` por espacios en blanco, preservando matrices inline (`\begin{pmatrix}`, `\begin{bmatrix}`, etc.) y fórmulas multilínea en display `$$ ... $$`.
  - **Idempotencia 100%:** Verificado que múltiples ejecuciones sucesivas devuelven `fixes == 0` y `repaired == content`.

---

## 3. Cobertura de Tests Adversarios en `tests/test_platform_katex_admission_guard.py`

Se agregaron casos de prueba rigurosos:
1. **Rechazo léxico y semántico con `R-23`:**
   - `test_validate_rejects_overescaped_competency_description`
   - `test_validate_rejects_inline_linebreak_in_competency_description`
   - `test_validate_rejects_overescaped_competency_name`
   - `test_validate_rejects_inline_linebreak_in_competency_name`
   - `test_validate_rejects_overescaped_fill_in_the_blank_canonical_algebraic`
   - `test_validate_rejects_inline_linebreak_in_canonical_algebraic`
   - `test_validate_rejects_overescaped_fill_in_the_blank_accepted_equivalents`
   - `test_validate_rejects_inline_linebreak_in_accepted_equivalents`
   - `test_validate_rejects_overescaped_misconception_warning`
   - `test_validate_rejects_inline_linebreak_in_misconception_warning`
   - `test_validate_rejects_overescaped_course_metadata`
   - `test_validate_rejects_inline_linebreak_in_course_description`
2. **Reparación determinista KaTeX:**
   - `test_repair_all_centernot_arrow_variants`: Matriz parametrizada con las 12 variantes de flechas y fallback.
   - `test_repair_inline_line_break_outside_matrix`: Limpieza de `$a \\ b$` a `$a  b$` preservando matrices inline y display math.
   - `test_repair_matrix_row_break_adjacent_to_command_without_space`: Normalización de 6 barras crudas a salto de matriz con espacio.
3. **Auto-reparación en `scan_courses()`:**
   - `test_scan_courses_autorepairs_competency_description_and_fill_in_the_blank`: Curso temporal con sobreescape en competencias y `fill_in_the_blank` auto-reparado y servido como `valid`.
4. **Idempotencia y validación sobre cursos reales:**
   - `test_real_courses_pass_validation_100_percent`: Validación 100% de los 4 cursos reales en `courses/*.json`.
   - `test_real_courses_repair_idempotence`: `fixes == 0` y paridad idéntica garantizada sobre los 4 cursos reales.
5. **Paridad exacta de documentación:**
   - `test_future_milestones_byte_parity`: Validación byte a byte entre `FUTURE_MILESTONES.md` y `docs/future_milestones/FUTURE_MILESTONES.md`.

---

## 4. Resultados de Verificación

Comando ejecutado:
```powershell
pytest tests/test_platform_katex_admission_guard.py tests/test_platform.py -v
```

Resultado:
```
============================= 67 passed in 8.27s ==============================
```
- **Total Tests:** 67 pasados, 0 fallados, 0 advertencias.
- **Tasa de Éxito:** 100%.
- **Cursos Reales (`courses/*.json`):** 4/4 válidos, 0 fixes necesarios (100% limpios e idempotentes).
- **Paridad `FUTURE_MILESTONES.md`:** 100% idénticos byte a byte (`FC: no se han encontrado diferencias`).
