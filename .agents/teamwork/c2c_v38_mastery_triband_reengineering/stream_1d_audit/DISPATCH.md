# DISPATCH — Stream 1D (Fase 3: Auditor Forense Read-Only)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1d_audit`
- **Impl Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1d_impl\handoff.md`
- **Impr Handoff:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1d_impr\handoff.md`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\stream_1d_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Auditoría Forense (Stream 1D)
*(Nota de concurrencia Gate 1: `Stream 1B` y `Stream 1C` siguen activos sobre sus fronteras disjuntas; `git status` mostrará cambios legítimos en sus archivos).*

1. **Higiene y Frontera de Stream 1D:**
   - Ejecuta `git status --short` y verifica cero scripts temporales sueltos ni `.c2c_subagent_lock.json` activos en el workspace, y que los archivos de `Stream 1D` se limiten a `check_templates.py`, `engine/invariants.py`, `engine/assemble.py`, `examples/{edo,edp}/templates/*.json` y sus 8 suites asignadas.
2. **Inspección de Código en Producción (`read_file` en bloques amplios `400-800` líneas):**
   - `check_templates.py`:
     - Confirma `[TPL-STATIC-OPT]` (`strict=True`): bloqueo incondicional de `len(unique_correct) == 1` para `N >= 2` **incluso cuando `vars == {}` / `domain == {}` está vacío** (`Matiz 4b`), `>= 10` claves únicas / 20 semillas en cuantitativas (`>= 4` en conceptuales), concentración `<= 20%` por clave en la competencia, y rotación en `multiple_select`.
     - Confirma `[TPL-DYNAMIC-RATIONALE]` (`strict=True`, `seeds >= 15`): bloqueo por slot individual cuando `content` varía entre semillas pero `error_rationale` es estático, y bloqueo por competencia cuando `rationale_uniqueness_pct < 35.0%` (`>= 30` distractores).
     - Confirma AST `cross_check_py` no trivial, `hints >= 25` chars, soporte multimodal en `TPL-D3` (`FIB + MS`) y preservación de `evaluate_competency_diversity(stems, min_diversity_ratio=0.5)` junto con la calibración `0.25` + `>= 0.85` en `check_competency_diversity`.
   - `engine/invariants.py`: confirma `[KATEX-PROSE-OVERFLOW]` (llaves balanceadas, `<= 45` pasa, `>= 46` falla con `[KATEX-PROSE-OVERFLOW]`, nunca `R-23`) y desenvoltura `\text{...}` en `[R-18]`.
   - `engine/assemble.py`: confirma interpolación universal `@var@` (`len >= 1`, ej. `@n@`, `@k@`, `@c@`) con `is_cta=True`, preservando `len(k) > 2` únicamente para llaves legacy `{var}` (`${k}^*$`).
   - Confirma **0 subcadenas Zero-Domain prohibidas** en `check_templates.py`, `engine/invariants.py` y `engine/assemble.py` (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`).
3. **Ejecución Independiente de Tests:**
   ```powershell
   & ".venv\Scripts\python.exe" -m pytest tests/test_engine_invariants_adversarial.py tests/test_assemble_katex_and_rationale.py tests/test_assemble_sanitize_katex_r23.py tests/test_katex_prairielearn_tokens.py tests/test_c2c_error_aggregation.py tests/test_sandbox_adversarial.py tests/test_sandbox_gil_and_circuit_breaker.py tests/test_template_variability.py -q
   ```
4. Escribe `audit_report.md` en `stream_1d_audit/` y envía `PASS:: Stream 1D (<N> passed)` o `REJECT:: Stream 1D | <archivo:línea> | <causa>` a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`.
