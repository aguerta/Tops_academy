# BRIEFING — Stream 2C (Fase 1: Implementador)

- **Agent:** `c2c38_implementer`
- **Stream:** 2C (Suites Forensic Replays)
- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Date:** 2026-10-31

---

## 1. Archivos en Frontera Exclusiva de Escritura
1. `tests/test_forensic_replay_ab30cf91.py`
2. `tests/test_forensic_shard06_and_variance_v34.py`
3. `tests/test_sweetspot_v35_cta_and_shards.py`
4. `.agents/teamwork/c2c_v38_mastery_triband_reengineering/stream_2c_impl/BRIEFING.md`
5. `.agents/teamwork/c2c_v38_mastery_triband_reengineering/stream_2c_impl/handoff.md`

**Archivos de producción modificables:** 0 (Frontera estricta).

---

## 2. Diagnóstico Inicial de Ejecución Pytest
Línea base ejecutada antes de modificaciones:
- **Total tests:** 43
- **Pasados:** 34
- **Fallados:** 9 (3 en ab30cf91, 2 en v34, 4 en v35)
- **Tiempo de ejecución:** 2.54s

---

## 3. Fallos Específicos Detectados y Mapeo a Contratos C2C v3.8

### A. `tests/test_forensic_replay_ab30cf91.py`
1. **Línea 133 (`test_v1_bootstrap_zero_raster_multi_pdf_and_stdout_cap`):**
   - *Causa:* En v3.8 la ingesta multi-PDF de Greene se promueve determinísticamente a `mapreduce`, generando múltiples subagentes (`cta_01.json`, `cta_02.json`). La aserción `assert "cta_01.json" in prompt` se ejecutaba dentro de un bucle sobre todos los subagentes, fallando en el subagente 2.
   - *Adaptación v3.8:* Verificar que cada subagente apunte a su respectivo `cta_{idx:02d}.json`.
2. **Líneas 480-534 (`test_v5_shard_06_katex_sandwich_and_delta_placeholder_block`):**
   - *Causa:* `check_single_template` en `template_sandwich` falla con `[TPL-CROSS: VERIFICADOR TRIVIAL]` debido a `def verify(r): return True`, y con `[TPL-DYNAMIC-RATIONALE]` porque los distractores generados varían numéricamente pero su `error_rationale` no varía dinámicamente.
   - *Adaptación v3.8:* Asignar verificador con validación analítica no trivial sobre `vars` y dotar a cada distractor generado de `error_rationale` dinámico contextualizado con el valor numérico/placeholder `@var@`.
3. **Líneas 654-656 y 721-723 (`test_v6_shard_08_zero_disk_mutation_and_shard_fixes_and_circuit_breaker`):**
   - *Causa:* Las tuplas de `shard_08_data.py` y `shard_fixes/C-08.py` usaban formato legacy de 10 elementos Form-A en vez del contrato Form-B de 9 elementos `(tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution)`.
   - *Adaptación v3.8:* Convertir tuplas a Form-B 9-elementos respetando `(difficulty, bloom)`, stems >= 3, hints >= 3 (>= 25 chars) y ver_fn no trivial.

### B. `tests/test_forensic_shard06_and_variance_v34.py`
1. **Líneas 331-365 (`test_legacy_shard06_exact_code_compiles_cleanly`):**
   - *Causa:* Código legacy con 1 sola tupla Form-A (10 elementos). Falla de inmediato en `compile_shard(strict=True)` por formato y por contrato Tri-Banda (min_archetypes >= 3).
   - *Adaptación v3.8:* Actualizar el fixture a 3 arquetipos Form-B 9-elementos cubriendo `easy`, `medium`, `hard`, >= 2 niveles Bloom, >= 2 modalidades activas (FIB/MS para `Hab-06`), distractores 3-tupla con `@var@`, stems >= 3, hints >= 3, preservando la invariante evaluada (evitar falsa clausura `b_}{LS}` y preservar `error_rationale` explícito de `D-Hab06-04`).
2. **Líneas 522-588 (`test_compile_four_disjoint_milestone3_archetypes_dry_distractors`):**
   - *Causa:* Tuplas de 10 elementos Form-A con 2-tuplas distractoras que fallan en strict mode.
   - *Adaptación v3.8:* Adaptar a Form-B 9-elementos con `(difficulty, bloom)`, distractores 3-tupla `(did, val, rationale)`, stems >= 3 y hints >= 3.

### C. `tests/test_sweetspot_v35_cta_and_shards.py`
1. **Líneas 702-714 (`test_dispatch_authors_stamps_min_archetypes_and_injected_in_compile_cmd`):**
   - *Causa:* La prueba esperaba `min_archetypes == 4`. En C2C v3.8 el estándar predeterminado es `min_archetypes == 3` (`--min-archetypes 3`).
   - *Adaptación v3.8:* Ajustar aserciones para verificar `min_archetypes == 3` y `--min-archetypes 3`.
2. **Líneas 749-766 (`test_shard_single_tuple_fails_m3_archetypes_and_hook_guard_rule_c_enforces_edit_file`):**
   - *Causa:* El código de 1 sola tupla estaba en formato Form-A, por lo que fallaba antes de llegar a la validación `[M3-ARCHETYPES]`.
   - *Adaptación v3.8:* Usar 1 tupla Form-B válida (9 elementos). Así la tupla pasa la validación sintáctica individual y es rechazada correctamente por `[M3-ARCHETYPES]` al no alcanzar el umbral mínimo (1 < 3 o 1 < 4).
3. **Líneas 891-945 (`test_shard_compact_pattern_passes_m3_archetypes_and_hook_guard_rule_b_blocks_further_edits`):**
   - *Causa:* Las tuplas en `compact_code` usan formato Form-A de 9 elementos con `[]` en posición 7 y omiten `hints`, siendo rechazadas por el compilador v3.8.
   - *Adaptación v3.8:* Actualizar las tuplas a Form-B 9-elementos con tri-banda (`easy`, `medium`, `hard`), Bloom múltiple, modalidad activa (al menos 1 FIB/MS para `C-06`), distractores 3-tupla y hints sustanciales.
4. **Líneas 1078-1083 (`test_shard_syntax_error_recovery_lifecycle_with_hook_guard`):**
   - *Causa:* El código compact de recuperación utilizaba tuplas Form-A de 9 elementos, fallando en la recompilación estricta.
   - *Adaptación v3.8:* Actualizar el código reparado a Form-B 9-elementos válido para que la recompilación culmine en `PASS` y active la regla B del Hook Guard.

---

## 4. Riesgos Identificados y Mitigaciones
1. **Riesgo de violación Zero-Domain (`tests/test_skill.py`):**
   - *Mitigación:* Ninguna modificación a archivos dentro de `.agents/skills/content-to-course/`. Todos los comentarios en los archivos de test se escribirán en inglés limpio sin contener subcadenas prohibidas (`edo`, `pde`, `derivadas`, etc.).
2. **Riesgo de colisión de hooks (`c2c_hook_guard.py`):**
   - *Mitigación:* Nunca invocar scripts con `-h`/`--help` ni `python -c` con rutas de skill. Ejecutar exclusivamente `pytest` con `.venv\Scripts\python.exe`.
3. **Riesgo de romper aserciones forenses originales (ab30cf91, v34, v35):**
   - *Mitigación:* Preservar el 100% de la lógica de assertions subyacentes: aislamiento de shards, ciclo de vida de `pass_<shard>.json`, rechazo de monolitos en Hook Guard (Reglas A, B, C), detección de fallas sintácticas y sanitización de KaTeX.
