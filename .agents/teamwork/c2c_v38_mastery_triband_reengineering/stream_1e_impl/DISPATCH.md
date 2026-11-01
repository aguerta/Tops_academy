# DISPATCH — Stream 1E (Fase 1: Implementador)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1e_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\repair_loop.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\src\validator\psychometric_checker.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\src\validator\rules.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_validator.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_katex_overescape_validator_r23.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1e_impl\BRIEFING.md` `[NEW]`
7. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1e_impl\handoff.md` `[NEW]`

PROHIBIDO modificar cualquier otro archivo.

## Reglas Pre-Flight y Guardias de Entorno
- **Hooks:** Prohibido ejecutar `run.py --help` / `dispatch.py --help` o `python -c` mencionando `"content-to-course/"` junto con `open(`, `read_text`, `run.py`, `prepare.py`, `ingest.py`, `dispatch.py`. Usa `read_file` y `& ".venv\Scripts\python.exe" -m pytest <archivos_test> -q`.
- **Zero-Domain (`test_skill.py`):** En `repair_loop.py`, PROHIBIDO incluir (ni en comentarios ni en strings) las subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. ¡Cuidado en español con `puedo`, `quedo`, `heredo` (`edo`) o `regresión` (`regresi`)!
- **Tag KaTeX y Regresión Cursos Publicados:**
  - En `src/validator/rules.py`, registra `[KATEX-PROSE-OVERFLOW]` con `rule_id="R-20"` y `code="ERR_KATEX_PROSE_OVERFLOW"` (NUNCA `rule_id="R-23"`), e inspecciona en Pre-Flight cómo `test_katex_overescape_validator_r23.py` y `test_validator.py` auditan `courses/*.json` legacy para no romper la regresión de cursos históricos publicados mientras se audita estrictamente cualquier banco nuevo.

## Especificación Técnica

### 1. `repair_loop.py` (`P0.5` — Purga Integral de Padding y Mutadores Sintéticos)
- Eliminar por completo `_repair_giveaway_lengths` (`shared_pads` como `" bajo las premisas y condiciones del modelo dado"`, etc.) y todos los mutadores sintéticos C–F (`_repair_numeric_outliers`, `_repair_duplicate_options`, `_repair_homogeneous_distractors` y cualquier inyección textual/numérica sobre `options` o `error_rationale`).
- Conservar la clase `RepairLoop` y sus firmas públicas compatibles con `run.py` y suites de integración, ejecutando en `run()` **exclusivamente el Módulo A (`sanitize_latex_escapes`)**: limpieza determinista de escapes LaTeX sin mutar jamás la redacción, longitud ni valores matemáticos de las opciones.

### 2. `src/validator/psychometric_checker.py` (Empates Simbólicos `[R-16]`)
- En la regla `[R-16]` de longitud delatora (`~L58-59`): utilizar desigualdad estricta (`len_c > max_d ...` y `len_c < min_d ...`) de modo que opciones simbólicas cortas de igual longitud (ej. 7 opciones de 12 caracteres como `$O(n^{-1/2})$`, `$O_p(n^{-1})$`) **jamás** disparen falso positivo por empate `len_c == max_d == min_d`.

### 3. `src/validator/rules.py` (`[KATEX-PROSE-OVERFLOW]`, `[R-18]` y Anti-Pad)
- **Paridad `[KATEX-PROSE-OVERFLOW]`:** detectar cualquier bloque `\text{...}`, `\textrm{...}`, `\mathrm{...}` (con conteo balanceado de llaves) cuyo contenido interno supere `45` caracteres y emitir `ValidationError(rule_id="R-20", code="ERR_KATEX_PROSE_OVERFLOW", message=f"[KATEX-PROSE-OVERFLOW] ...", item_id=q_id)` (en modo `strict=True` o según el gate de reglas extendidas; verifica en Pre-Flight si `test_katex_overescape_validator_r23.py` llama `validate_course_content(..., strict=True)` sobre `courses/*.json` filtrando solo `e.rule_id == "R-23"` — si filtra solo `R-23`, emitir `R-20` en `check_extended_quality_rules` funciona directo sin fricción).
- **Desenvoltura `\text{...}` en `[R-18]`:** antes de calcular esqueletos repetitivos de distractores en `[R-18]`, desenvolver `\text{...}` / `\textrm{...}` dentro de `$...$` para capturar prosa repetitiva camuflada en modo matemático.
- **Bloqueo determinista de muletillas de padding (`[R-18]` / `ERR_SYNTHETIC_PAD`):** rechazar en opciones de pregunta frases burocráticas inyectadas como `"bajo las premisas y condiciones del modelo"`, `"en el marco de las condiciones establecidas"`, `"Opción alterna "`, `"Distractor homogéneo "`.

### 4. Actualización y Ampliación de las 2 Suites Exclusivas
En `test_validator.py` y `test_katex_overescape_validator_r23.py`, añade pruebas unitarias y adversarias verificando:
- `RepairLoop` ya NO modifica longitudes de opciones ni inyecta `shared_pads`, pero sigue saneando escapes LaTeX (Módulo A).
- Empates simbólicos `len_c == max_d == min_d` pasan `[R-16]` con 0 errores.
- `\text{...}` `> 45` chars dispara `ERR_KATEX_PROSE_OVERFLOW` (`[KATEX-PROSE-OVERFLOW]`, `rule_id="R-20"`), mientras `\text{corto}` `<= 45` chars pasa limpio.
- Muletillas de padding y boilerplate camuflado en `$\text{...}$` son rechazados por `rules.py`.

## Verificación
Ejecuta:
```powershell
& ".venv\Scripts\python.exe" -m pytest tests/test_validator.py tests/test_katex_overescape_validator_r23.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar y notifica a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589` con `DONE:: Stream 1E Impl completado (<N> passed)`.
