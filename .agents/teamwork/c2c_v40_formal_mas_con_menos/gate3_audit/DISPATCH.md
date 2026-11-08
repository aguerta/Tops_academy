# DISPATCH — Gate 3 (Certificación Forense Global Read-Only)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Audit Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\gate3_audit`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\gate3_audit\audit_report.md` `[NEW]`

PROHIBIDO modificar cualquier archivo del repositorio fuera de `gate3_audit/audit_report.md`.

## Protocolo de Certificación Integral Gate 3
1. **Ejecución Completa Paralela (`pytest-xdist`) de las `63/63` Suites (`< 35 s`):**
   ```powershell
   & ".venv\Scripts\python.exe" -m pytest -q
   ```
   Confirma `0 failed`, cuenta exacta de tests pasados y tiempo total de reloj.
2. **Verificación de Invariantes Duros de Repositorio y Toolchain:**
   - **Zero-Domain:** Comprueba que NINGÚN `.py` dentro de `.agents/skills/content-to-course/` contenga en minúsculas `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`.
   - **LF y Presupuesto `lean`:** Comprueba que `.agents/skills/content-to-course/subagent_types.json` tenga `0` bytes `\r` y que `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md` pese `<= 4,750` bytes.
   - **Paridad `FUTURE_MILESTONES.md`:** Confirma paridad byte a byte entre `FUTURE_MILESTONES.md` y `docs/future_milestones/FUTURE_MILESTONES.md`.
   - **No Regresión QA en Cursos Publicados:** Ejecuta `standardized_audit_engine` sobre `courses/solow_growth_model.json` y `courses/saul_control_optimo.json` verificando puntajes `>= 19.0 / 20.0`.
   - **Toolchain Formal Vivo:** Comprueba `& "$env:USERPROFILE\.elan\bin\lean.exe" --version`, `z3`, `hypothesis` y `pykatex`.
   - **Higiene Git:** Ejecuta `git status --short` comprobando cero scripts basura, cero `.c2c_subagent_lock.json` y cero archivos fuera de alcance.
3. Escribe `audit_report.md` en `gate3_audit/` y envía `PASS:: Gate 3 Global Audit (<N> passed across <M> suites in <T>s)` o `REJECT:: Gate 3 | <detalle>` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
