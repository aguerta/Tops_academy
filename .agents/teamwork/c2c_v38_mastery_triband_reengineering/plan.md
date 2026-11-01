# Plan de Ejecución Aprobado (`c2c_v38_mastery_triband_reengineering`)

Referencia canónica aprobada: `C:\Users\augus\.gemini\antigravity\brain\eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589\implementation_plan.md`.

## Topología de Gates y Fronteras Exclusivas (`56/56` suites `tests/test_*.py`, `∩ = ∅`)

### Gate 1 — Módulos Nucleares (6 Tríadas Paralelas en `Model="flash"`)
- **Stream `1A` (`P0.1` + `Matiz 2, 3, 4a`):**
  - Prod: `partition_corpus.py`, `ingest.py`, `prepare.py`, `compile_cta.py`, `cta_merge.py`, `check_cta.py`
  - Tests (7): `test_cta_mapreduce.py`, `test_cta_merge_prereq_scoping.py`, `test_c2c_v321_comp1_cta.py`, `test_cta_healing.py`, `test_cta_sweetspot_and_autoheal.py`, `test_fast_ingest_and_cta_append.py`, `test_handouts.py`
- **Stream `1B` (`P0.2` + `Brecha 1`):**
  - Prod: `compile_shard.py`, `c2c_hook_guard.py`
  - Tests (8): `test_m3_archetypes_semantic_gate.py`, `test_compile_shard.py`, `test_shard_compiler_hardening.py`, `test_shard06_and_dry_archetypes.py`, `test_invariants_and_shard_overescape_r23.py`, `test_latex_engine.py`, `test_hook_post_pass_and_write_isolation.py`, `test_watchdog_and_hooks.py`
- **Stream `1C` (`P0.1/P0.3` + `Brecha 1` + `Matiz 3`):**
  - Prod: `plan_shards.py`, `dispatch.py`, `subagent_types.json`, `system_prompts/*.md`, `system_prompts/lean/*.md`
  - Tests (6): `test_dispatch_turn0_and_milestone3_prompts.py`, `test_c2c_v321_comp4_prompts.py`, `test_c2c_v321_comp3_dispatch.py`, `test_weighted_sharding_m7.py`, `test_skill_v3.py`, `test_orchestration_resilience.py`
- **Stream `1D` (`P0.4` + `Brecha 1` + `Matiz 4b`):**
  - Prod: `check_templates.py`, `engine/invariants.py`, `engine/assemble.py`, `examples/edo/templates/*.json`, `examples/edp/templates/*.json`
  - Tests (8): `test_engine_invariants_adversarial.py`, `test_assemble_katex_and_rationale.py`, `test_assemble_sanitize_katex_r23.py`, `test_katex_prairielearn_tokens.py`, `test_c2c_error_aggregation.py`, `test_sandbox_adversarial.py`, `test_sandbox_gil_and_circuit_breaker.py`, `test_template_variability.py`
- **Stream `1E` (`P0.5` Anti-Padding & Validator):**
  - Prod: `repair_loop.py`, `src/validator/psychometric_checker.py`, `src/validator/rules.py`
  - Tests (2): `test_validator.py`, `test_katex_overescape_validator_r23.py`
- **Stream `1F` (`P0.6` + `Brecha 1` + `Matiz 3`):**
  - Prod: `judge.py`, `course_publisher.py`
  - Tests (4): `test_new_audit_linters.py`, `test_c2c_validator_prescriptive.py`, `test_dispatch_scope.py`, `test_pipeline_optimizations.py`

### Gate 2 — Integración de Runner, Suites Multi-Módulo y Replays Forenses (3 Tríadas Paralelas tras `6/6 PASS::` en Gate 1)
- **Stream `2A`:** Prod: `run.py`, `SKILL.md` | Tests (7): `test_prompts_contract_alignment.py`, `test_bootstrap_and_wave_streaming.py`, `test_run_templates_and_dispatch_repair.py`, `test_append_workflow.py`, `test_c2c_v321_multi_instance_and_append.py`, `test_skill.py`, `test_delete_course.py`
- **Stream `2B`:** Prod: Ninguno | Tests (6): `test_c2c_solow2_architectural_improvements.py`, `test_c2c_remediation_optimization.py`, `test_c2c_v31_adversarial_plan.py`, `test_c2c_case_2b_mastery.py`, `test_c2c_v321_comp2_shard.py`, `test_pipeline_reparations.py`
- **Stream `2C`:** Prod: Ninguno | Tests (3): `test_forensic_replay_ab30cf91.py`, `test_forensic_shard06_and_variance_v34.py`, `test_sweetspot_v35_cta_and_shards.py`

### Gate 3 — Certificación Forense Global Read-Only
- Ejecución completa de las **56/56** suites `tests/test_*.py` (incluyendo las 5 suites `ORTHO`: `test_blind_guess_empirical.py`, `test_course_api_manifest.py`, `test_m1_zoomfix_contract.py`, `test_platform.py`, `test_platform_katex_admission_guard.py`), verificación LF de `subagent_types.json`, byte-budget `<= 4,750 B` de `lean/prompt_shard_author.md`, cero subcadenas Zero-Domain prohibidas, corrida empírica de `standardized_audit_engine.py` y `git status` limpio.
