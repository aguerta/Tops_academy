# DISPATCH — Gate 3 (Auditoría Forense Global Read-Only)

- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Audit Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\gate3_audit`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v38_mastery_triband_reengineering\gate3_audit\audit_report.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción o `tests/`.

## Protocolo de Certificación Global (Gate 3)
1. **Ejecución de las 5 Suites `ORTHO`:**
   ```powershell
   & ".venv\Scripts\python.exe" -m pytest tests/test_blind_guess_empirical.py tests/test_course_api_manifest.py tests/test_m1_zoomfix_contract.py tests/test_platform.py tests/test_platform_katex_admission_guard.py -q
   ```
2. **Ejecución Completa de las 56 Suites Deterministas Top-Level (`tests/test_*.py`):**
   ```powershell
   & ".venv\Scripts\python.exe" -m pytest tests/ --ignore=tests/e2e -q
   ```
3. **Verificación de Invariantes Críticos (Zero-Domain, LF y Byte-Budgets Lean):**
   ```powershell
   & ".venv\Scripts\python.exe" -m pytest tests/test_skill.py tests/test_prompts_contract_alignment.py tests/test_sweetspot_v35_cta_and_shards.py -q
   ```
4. **Verificación Empírica de `standardized_audit_engine.py` sobre Cursos Publicados:**
   ```powershell
   & ".venv\Scripts\python.exe" .agents/skills/course-qa-evaluator/scripts/standardized_audit_engine.py courses/solow_growth_model.json
   & ".venv\Scripts\python.exe" .agents/skills/course-qa-evaluator/scripts/standardized_audit_engine.py courses/estadistica_3_s9_vdirect.json
   ```
5. **Auditoría de Higiene de Repositorio (`git status --short`):**
   - Verifica que todos los archivos modificados pertenezcan exclusivamente a la unión de las fronteras de `Streams 1A..1F, 2A..2C` y `.agents/teamwork/c2c_v38_mastery_triband_reengineering/`.
   - Verifica `0` modificaciones en `content/`, `0` scripts sueltos fuera de `tests/` y `0` `.c2c_subagent_lock.json` activos.

Escribe `gate3_audit/audit_report.md` con todos los resultados cuantitativos y envía `PASS:: Gate 3 Global Audit (<N> passed across 56 suites)` (o `REJECT:: ...`) a `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`.
