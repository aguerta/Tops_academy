# DISPATCH — Stream 2A (Fase A: Implementador Ortogonal — Gate 2)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2a_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\run.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\SKILL.md`
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\rules\c2c-quality-invariants.md` `[NEW]`
4. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_prompts_contract_alignment.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_bootstrap_and_wave_streaming.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_run_templates_and_dispatch_repair.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_append_workflow.py`
8. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v321_multi_instance_and_append.py`
9. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_skill.py`
10. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_delete_course.py`
11. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2a_impl\BRIEFING.md` `[NEW]`
12. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2a_impl\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier otro archivo.

## Guardias Obligatorias
- **Zero-Domain (`test_skill.py`):** En `run.py` (y en TODOS los `.py` de `content-to-course/`) NO pueden aparecer las subcadenas en minúsculas: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. Escribe comentarios/docstrings en inglés.
- **Hooks:** Prohibido ejecutar `run.py --help` o `python -c` mencionando `"content-to-course/"` junto con `open(`, `read_text`, `run.py`, `prepare.py`, `ingest.py`, `dispatch.py`.
- **Pytest sin contención de CPU:** Usa `-o addopts=""` al correr tus 7 suites.

## Especificación Técnica (Gate 2 — Integración `run.py` con Recibos `*.cert.json` `< 5 ms`, Fix `gates` & `repair-matrix`, `SKILL.md` y Regla Universal)

*(Todos los módulos nucleares de Gate 1 — `stage_contract.py`, `interstage_schemas.py`, `compile_cta.py`, `compile_shard.py`, `check_templates.py`, `dispatch.py`, `judge.py`, `course_publisher.py` — ya fueron implementados y auditados con `PASS::`).*

1. **`run.py` — Fast-Path Criptográfico `< 5 ms` por Recibos `shard_XX.cert.json` en `--stage templates` (`~L755-L890`) y `--stage certify` (`~L1896`):**
   - En `--stage templates` (cuando no se pase `--force-recheck` / `force_recheck=True`):
     * Para cada shard en `work/shards/<shard_id>.cert.json`, verifica mediante `verify_certificate` de `engine.interstage_schemas` (o comparación SHA-256 directa):
       1) `cert.get("passed_50_seeds") is True`,
       2) `cert.get("source_sha256") == sha256(shard_XX_data.py)`,
       3) `cert.get("cta_sha256") == sha256(cta.json)`,
       4) para cada `<cid>: <tpl_sha>` en `cert.get("template_shas", {})`, el archivo `work/templates/<cid>.json` existe y su SHA-256 coincide exactamente!
     * Si todos los hashes coinciden, **marca esas competencias como pre-certificadas en `< 5 ms` y salta re-ejecutar el sandbox de 50 semillas sobre ellas**! Solo ejecuta `check_templates` sobre plantillas que carezcan de certificado válido o cuyo hash haya cambiado.
   - En `--stage certify` (`~L1896`): reutiliza esa misma verificación criptográfica sin repetir re-cómputos redundantes.
   - Al escribir `template_failures.json` (`~L1189-L1195`), usa `RejectionSpec` de `engine.interstage_schemas` (escribiendo `"status": "REJECTED"` y poblando simultáneamente `"failing_shards"` y `"affected_shards"`).

2. **`run.py` — Corrección Crítica de `--stage gates` (`~L1755-L1771`) y `--stage repair-matrix` (`~L1693`):**
   - **`--stage repair-matrix` (`~L1693`):** Hoy busca únicamente `spec.get("groups")`, devolviendo 0 grupos cuando `course_publisher.py` escribe `"grouped_by_rule"` y `"diagnostics_by_competency"`. Actualízalo para normalizar vía `RejectionSpec` o leer `spec.get("grouped_by_rule") or spec.get("groups")` junto con `spec.get("diagnostics_by_competency")` y `spec.get("failing_shards") or spec.get("affected_shards")`!
   - **`--stage gates` (`~L1755-L1771`):** Hoy solo ejecuta `build` + `repair-matrix`, omitiendo `verify` y `standardized_audit_engine.run_full_audit` (dando `PASS` en cursos que `publish` rechaza). Actualízalo para que ejecute en secuencia determinista:
     1) `build`,
     2) `verify` (validador léxico/psicométrico `validate_course_content`),
     3) auditoría QA determinista de publicación (dry-run de las compuertas de `CoursePublisher` / `standardized_audit_engine.run_full_audit`, escribiendo `publish_rejection_spec.json` si hay bloqueantes), y
     4) `repair-matrix` consolidando todos los hallazgos en una sola matriz! Si cualquiera de los pasos 1–3 detecta fallos bloqueantes, `gates` DEBE reportar estado fallido (`False` / código no-cero en CLI) y poblar la matriz de reparación.

3. **`run.py` — Campos de Gobernanza en `.c2c_subagent_lock.json` (`~L1958-L1965`):**
   - Al crear `.c2c_subagent_lock.json`, inicializa `{ "active": True, "course_id": ..., "created_at": ..., "fsm_state": stage_name, "turn_count": 0, "max_turns": 40, "est_tokens": 0, "max_tokens": 5000000, "last_error_sha256": "", "error_sha256_streak": 0, "max_error_streak": 3 }` (retrocompatible con cualquier lector existente).

4. **Actualización de `SKILL.md` y Creación de `.agents/rules/c2c-quality-invariants.md`:**
   - Actualiza `SKILL.md` al contrato C2C v4.0 (`MIN_ARCHETYPES = 4`, DSL `Form-C`, `assumptions` explícitos, Triple Contrato `ver_*`, Matriz 2D de edición, `*.cert.json` `< 5 ms`, `--lean` por defecto y Juez Epistémico 1-Seed con $\alpha_{\text{Kernel}} = 0$).
   - Crea `.agents/rules/c2c-quality-invariants.md` según la especificación de `FUTURE_MILESTONES.md` §8.1.

5. **Actualización y Ampliación de tus 7 Suites Exclusivas:**
   - Alinea las aserciones de `test_prompts_contract_alignment.py`, `test_run_templates_and_dispatch_repair.py`, `test_skill.py`, etc., con `MIN_ARCHETYPES = 4`, `Form-C`/`Form-B` y los nuevos ejemplos de 4 arquetipos en `examples/{edo,edp}`.
   - Añade pruebas unitarias para: fast-path `< 5 ms` de `shard_XX.cert.json` (y re-ejecución inmediata si cambia 1 byte del `.py` o `.json`), `--stage gates` bloqueando cursos con fallos de `verify` o QA, y `--stage repair-matrix` leyendo `grouped_by_rule` + `diagnostics_by_competency`.

## Verificación y Entrega
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_prompts_contract_alignment.py tests/test_bootstrap_and_wave_streaming.py tests/test_run_templates_and_dispatch_repair.py tests/test_append_workflow.py tests/test_c2c_v321_multi_instance_and_append.py tests/test_skill.py tests/test_delete_course.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar, y envía `DONE:: Stream 2A (<N> passed)` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
