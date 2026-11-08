# DISPATCH — Stream 1E (Fase A: Implementador Ortogonal)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1e_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\engine\interstage_schemas.py` `[NEW]`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\judge.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\course_publisher.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\course-qa-evaluator\scripts\standardized_audit_engine.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_new_audit_linters.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_validator_prescriptive.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_dispatch_scope.py`
8. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_pipeline_optimizations.py`
9. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_straggler_and_postproduction_prevention.py`
10. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1e_impl\BRIEFING.md` `[NEW]`
11. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1e_impl\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Guardias Obligatorias
- **Zero-Domain (`test_skill.py`):** En NINGÚN `.py` de `content-to-course/` (`interstage_schemas.py`, `judge.py`, `course_publisher.py`) pueden aparecer (ni siquiera en comentarios) las subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. Escribe comentarios en inglés.
- **Retrocompatibilidad con Cursos Ya Publicados en `courses/*.json`:** Los cursos históricos (`solow_growth_model`, `gavilano_pre_parcial`, `asymptotic_statistics_v7`, `saul_control_optimo`) fueron compilados bajo v3.8 (`3` arquetipos) y DEBEN conservar sus puntajes `>= 19.0/20` al correr `standardized_audit_engine.py`.
- **Pytest sin contención de CPU:** Usa `-o addopts=""` al correr tus 5 suites.

## Especificación Técnica (Fase 1 + Fase 2: `interstage_schemas.py`, `judge.py` 1-Seed Bayesiano $\alpha_{\text{Kernel}}=0$, `course_publisher.py` y `standardized_audit_engine.py`)

1. **`engine/interstage_schemas.py` `[NEW]` (Milestone 18.1 — Fuente Única Anti-Drift de Esquemas Inter-Etapa):**
   - Implementa modelos Pydantic v2 + funciones helper de serialización/normalización tolerante para todos los artefactos de intercambio entre etapas:
     * `ArtifactCertificate` (`schema_version=1`, `stage`, `artifact_id`, `source_sha256`, `cta_sha256`, `compiler_sha256`, `contract_version=2`, `template_shas`, `passed_50_seeds`, `created_at`) + `write_certificate` / `verify_certificate`.
     * `CompileAttemptRecord` (`attempt`, `passed`, `error_count`, `affected_line_count`, `has_syntax_error`, `error_sha256`, `errors`).
     * `RejectionSpec` (usado tanto para `template_failures.json` como `publish_rejection_spec.json`): normaliza `status` siempre a mayúsculas `"REJECTED"` (aceptando `"rejected"`, `"fail"`, `"failed"` al leer), sincroniza bidireccionalmente **`failing_shards` y `affected_shards`** (ambos presentes con la misma lista ordenada al serializar!) y sincroniza bidireccionalmente **`grouped_by_rule` y `groups`** junto con `diagnostics_by_competency`! Así ningún consumidor (`run.py`, `c2c_hook_guard.py`, `dispatch.py`) volverá jamás a quedar ciego por drift de nombres de claves.

2. **`judge.py` (Arbitraje Epistémico 1-Seed Pre-Verificada + Dominancia Bayesiana $\alpha_{\text{Kernel}} = 0$):**
   - **a) Verificación Estricta de Semillas Pre-Juez (`~L300, L396-L409`):**
     * Corrige el muestreo de semillas en `range(100, 100000)`: toda instancia candidata para `blind_judge_items.json` DEBE ejecutarse validando `cross_check` / `verifier_code` (exigiendo `True` booleano estricto) y `check_instance_invariants` (sin colisiones `TPL-D4` ni errores KaTeX). Si una semilla aleatoria colisiona o falla invariantes, reintenta deterministamente la siguiente semilla antes de empaquetar el ítem; si ninguna semilla de una plantilla pasa (plantilla rota), regístrala inmediatamente como fallo determinista del kernel (`kernel_refuted = True`) sin gastar tokens LLM!
   - **b) Muestreo Canónico 1-Seed por Defecto (`-65%` Tokens Stage 5):**
     * Cuando una plantilla incluye `verifier_code` / `cross_check_py` no vacío y no se forzó explícitamente otro valor por parámetro/CLI, usa **`samples_per_template = 1`** (1 semilla canónica verificada por plantilla para evaluar Suficiencia Epistémica y no-giveaway semántico; si un test pasa explícitamente `samples_per_template=3` o `num_samples=3`, respeta el argumento explícito!).
   - **c) Dominancia de Arbitraje del Kernel (`resolve_neuro_symbolic_verdict`, $\alpha_{\text{Kernel}} = 0$):**
     * Si el kernel determinista refutó una instancia (`kernel_refuted == True`), el veredicto final es incondicionalmente `FAIL` aunque un juez LLM vote `PASS`.
     * Si el kernel verificó constructivamente la instancia (`kernel_verified == True`: `verifier_code` pasó y refutó distractores) y un juez LLM emite `FAIL` alegando únicamente error de cálculo numérico (`failure_category == "math_error"` / `"calculation_error"` sin señalar `"epistemic_insufficiency"`, `"missing_definition"`, `"ambiguous_stem"` ni `"giveaway"`), marca `kernel_override = True` y preserva la validez algebraica demostrada (mientras que cualquier rechazo por insuficiencia epistémica, ambigüedad o giveaway sí bloquea y exige remediación!).
     * Al aprobar la evaluación de Stage 5, emite `work/judge.cert.json` mediante `ArtifactCertificate`.

3. **`course_publisher.py` y `standardized_audit_engine.py`:**
   - En `course_publisher.py` (`~L730-L755`):
     * Usa `RejectionSpec` de `engine.interstage_schemas` al escribir `publish_rejection_spec.json` (`"status": "REJECTED"`, poblando simultáneamente `"failing_shards"` + `"affected_shards"` y `"grouped_by_rule"` + `"groups"` + `"diagnostics_by_competency"`).
     * Estampa en el curso publicado (`metadata` / nivel raíz compatible con schema) `"contract_version": 2` y `"min_archetypes": 4` (leyendo `MIN_ARCHETYPES` desde `engine.stage_contract`), y emite `work/publish.cert.json` al publicar con éxito.
   - En `standardized_audit_engine.py` (`ArchetypeEntropyLinter`, `~L674-L755`):
     * Calcula dinámicamente `req_arch`: si el curso declara `contract_version >= 2` o `min_archetypes` explícito en `course_data` / `course_data.get("metadata", {})`, usa `int(min_archetypes)` (default `4` para `contract_version >= 2`); para cursos legacy sin `contract_version >= 2` (los JSON históricos ya publicados en `courses/`), mantiene `3`. Así los cursos nuevos v4.0 exigen estrictamente **4 esqueletos `$MATH$` y 4 `template_id` por competencia**, sin degradar los cursos v3.8 ya publicados!

4. **Pruebas Exhaustivas en tus 5 Suites Exclusivas:**
   - Añade tests unitarios y adversarios para `interstage_schemas.py` (`RejectionSpec` dual keys + case-insensitive status, `ArtifactCertificate` SHA-256 tamper detection), `judge.py` (pre-verificación de semillas descartando colisiones, default 1-seed en plantillas verificadas, y `resolve_neuro_symbolic_verdict` con $\alpha_{\text{Kernel}} = 0$), `course_publisher.py` (`publish_rejection_spec.json` con `REJECTED` + `failing_shards` + `grouped_by_rule` + `groups`), y `ArchetypeEntropyLinter` (`4` arquetipos en cursos `contract_version=2` vs `3` en legacy).

## Verificación y Entrega
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_new_audit_linters.py tests/test_c2c_validator_prescriptive.py tests/test_dispatch_scope.py tests/test_pipeline_optimizations.py tests/test_c2c_straggler_and_postproduction_prevention.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar, y envía `DONE:: Stream 1E (<N> passed)` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
