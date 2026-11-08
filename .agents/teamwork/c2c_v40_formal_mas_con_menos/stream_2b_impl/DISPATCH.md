# DISPATCH — Stream 2B (Fase A: Implementador Ortogonal — Gate 2)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Stream Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2b_impl`

## Frontera Exclusiva de Escritura (`Exclusive Write Boundary`)
SOLO tienes permiso de escritura sobre:
1. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_solow2_architectural_improvements.py`
2. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_remediation_optimization.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v31_adversarial_plan.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_case_2b_mastery.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_v321_comp2_shard.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_pipeline_reparations.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_system_prompts_compile_clean.py` `[NEW]`
8. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2b_impl\BRIEFING.md` `[NEW]`
9. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_2b_impl\handoff.md` `[NEW]`

PROHIBIDO tocar cualquier archivo de producción (`.agents/skills/content-to-course/**`, `src/**`) u otros tests! Si encuentras un bug real en un archivo de producción fuera de tu frontera, usa el protocolo `BLOCKER:: Stream 2B | <archivo:línea> | <causa> | <fix propuesto>` vía `send_message`.

## Especificación Técnica (Gate 2 — Suites Multi-Módulo + Compuerta CI de Auto-Compilación de Prompts Milestone 18.3)

1. **Alineación y Endurecimiento de las 6 Suites de Integración Existentes:**
   - Ejecuta y revisa las 6 suites existentes frente al nuevo contrato C2C v4.0 (`MIN_ARCHETYPES = 4` por defecto, Refutación Estricta de Distractores en `ver_*`, `cc_res is True`, deduplicación de `work_order` en `dispatch.py`, `--lean` por defecto, etc.).
   - IMPORTANTE: Si algún fixture sintético antiguo en estas 6 suites tenía un verificador tautológico (`return True` o `return "x" in res["correct"]` que devuelve `True` también en distractores) o esperaba `min_archetypes == 3` cuando llamaba sin parámetro explícito, actualiza limpiamente el fixture para que tenga un verificador matemático genuino (que refute sus distractores!) o 4 arquetipos reales, **sin debilitar ninguna aserción de seguridad**.

2. **Creación de `tests/test_system_prompts_compile_clean.py` `[NEW]` (Milestone 18.3 — *Prompt-Compiler Parity Gate*):**
   - Implementa una suite automatizada de contrato CI que impida para siempre que los ejemplos de `system_prompts/` queden obsoletos frente al compilador:
     * Extrae el bloque de código Python canónico de `system_prompts/lean/prompt_shard_author.md` (y verifica también `lean/prompt_cta_architect.md` si incluye bloque ejecutable), construye un `tmp_path` limpio con su `cta.json` correspondiente (compilado con `compile_cta.py` y `require_assumptions=True`), y ejecuta `compile_shard.py` en modo `--strict` con `min_archetypes=4` y `seeds=50`!
     * Verifica que:
       1) La compilación apruebe a la primera (`ok is True, errors == []`) emitiendo `shard_01.cert.json` válido.
       2) Genere los 4 arquetipos (`1 MC7 + 2 FIB + 1 MS` o multimodalidad válida), `>= 15` stems únicos y `div_ratio >= 0.50`.
       3) Las preguntas ensambladas por `instantiate_competency` pasen `validate_course_content(..., strict=True)` y `standardized_audit_engine.run_full_audit` con `0` errores críticos y `0` warnings de `ArchetypeEntropyLinter` (`contract_version=2`).
       4) `len(Path(".../lean/prompt_shard_author.md").read_bytes()) <= 4750` y `subagent_types.json` tenga `0` bytes `\r`.

## Verificación y Entrega
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_c2c_solow2_architectural_improvements.py tests/test_c2c_remediation_optimization.py tests/test_c2c_v31_adversarial_plan.py tests/test_c2c_case_2b_mastery.py tests/test_c2c_v321_comp2_shard.py tests/test_pipeline_reparations.py tests/test_system_prompts_compile_clean.py -q
```
Escribe `BRIEFING.md` antes de editar, `handoff.md` al terminar, y envía `DONE:: Stream 2B (<N> passed)` a `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`.
