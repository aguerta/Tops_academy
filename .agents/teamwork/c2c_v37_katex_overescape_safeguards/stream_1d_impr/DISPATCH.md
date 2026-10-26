# DISPATCH — Stream 1D (Fase 2: Mejorador)

- **Parent Conversation ID:** `da4d9acf-34da-4bc8-930b-6fb3d28b5744`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1d_impl\handoff.md`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1d_impr`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\run_platform.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\FUTURE_MILESTONES.md`
3. `d:\Augusto\personal_portfolio\Tops_academy\docs\future_milestones\FUTURE_MILESTONES.md`
4. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_platform_katex_admission_guard.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v37_katex_overescape_safeguards\stream_1d_impr\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Instrucciones de Endurecimiento
1. Lee el `handoff.md` del Implementador 1D, `run_platform.py`, `FUTURE_MILESTONES.md`, `docs/future_milestones/FUTURE_MILESTONES.md` y `tests/test_platform_katex_admission_guard.py`.
2. Revisa y endurece casos borde en `run_platform.py`:
   - En `validate_platform_course`:
     - Verifica que la inspección en memoria (Pass 4) revise también los campos `name` y `description` de `competencies`, `description` y `title`/`course_title` del curso, `common_misconception_warning`/`misconception_warning` de cada pregunta, y `correct_answer` de preguntas `fill_in_the_blank` (tanto si es string como si es dict con `value`, `expression`, `canonical_algebraic`, `accepted_equivalents`).
     - Verifica que `repair_platform_course_katex` también repare saltos de línea `\\` ilegales en modo inline `$ ... $` fuera de entornos matriciales o al menos cubra todos los patrones de sobreescape, `\centernot` (todas las flechas: `\Rightarrow`, `\implies`, `\Leftarrow`, `\Leftrightarrow`, `\iff`, `\rightarrow`, `\to`, `\leftarrow`, `\leftrightarrow`) y `\text{textVar[barx_n] = O(n)}`, de modo que `scan_courses()` pueda auto-reparar cualquier curso afectado por R-23.
     - Verifica que `repair_platform_course_katex` sea 100% idempotente sobre los 4 cursos reales de `courses/*.json` (`fixes == 0` y `repaired == content`).
   - Verifica que `FUTURE_MILESTONES.md` y `docs/future_milestones/FUTURE_MILESTONES.md` sean idénticos byte a byte (`fc` / igualdad de contenido).
3. Amplía `tests/test_platform_katex_admission_guard.py` con tests adversarios para:
   - `competencies[*].description` con sobreescape (como ocurría en `gavilano_pre_parcial.json` y `saul_control_optimo.json`).
   - `fill_in_the_blank` con `correct_answer.canonical_algebraic` y `accepted_equivalents` sobreescapados.
   - Idempotencia exacta (`fixes == 0`) de `repair_platform_course_katex` sobre los 4 cursos reales de `courses/*.json`.
   - Paridad exacta entre `FUTURE_MILESTONES.md` y `docs/future_milestones/FUTURE_MILESTONES.md`.
4. Ejecuta:
   ```powershell
   pytest tests/test_platform_katex_admission_guard.py tests/test_platform.py -q
   ```
5. Escribe `handoff.md` en tu carpeta `stream_1d_impr/` y finaliza con `DONE:: Stream 1D Impr completado`.
