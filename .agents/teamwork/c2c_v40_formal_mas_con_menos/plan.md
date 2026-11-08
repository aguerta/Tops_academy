# Plan Maestro de Ejecución Paralela — Fase 1 + Fase 2 (`c2c_v40_formal_mas_con_menos`)

- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Modelo de Subagentes:** `Model="flash"`
- **Topología por Stream:** Díada `c2c40_implementer` $\longrightarrow$ `c2c40_auditor` (**sin Improvers**).
- **Cobertura Total de Tests:** `61` suites existentes + `2` suites nuevas de certificación = **`63/63` suites (`∩ = ∅`)**.

---

## Contratos Transversales Inmutables entre Streams (`Stage 1 <-> Stage 6`)

1. **`engine/stage_contract.py`:** `CONTRACT_VERSION = 2`, `MIN_ARCHETYPES = 4`, `ARCHETYPE_KINDS = ("direct", "inverse", "perturbation", "boundary_or_edge_case")`.
2. **Recibos *Proof-Carrying Artifacts* (`*.cert.json`):**
   - Ubicaciones: `work/cta.cert.json`, `work/shards/<shard_id>.cert.json`, `work/judge.cert.json`, `work/publish.cert.json`.
   - Campos: `{"schema_version": 1, "stage": str, "artifact_id": str, "source_sha256": str, "cta_sha256": str, "compiler_sha256": str, "contract_version": 2, "template_shas": dict, "passed_50_seeds": bool, "created_at": str}`.
3. **Intento de Compilación (`.check_attempts/compile_<id>.json`):**
   - Preserva campos existentes y añade siempre: `"affected_line_count": int`, `"has_syntax_error": bool`, `"error_sha256": str`.
4. **Rechazo Downstream (`publish_rejection_spec.json` y `template_failures.json`):**
   - Escribe `"status": "REJECTED"` (consumidores normalizan `.upper()`), poblando **ambas** claves `"failing_shards"` y `"affected_shards"`, y en publicación **ambas** `"grouped_by_rule"` y `"groups"`, más `"diagnostics_by_competency"`.
5. **DSL Composicional `Form-C` en `compile_shard.py`:**
   - Retrocompatible 100% con 9-tuplas `Form-B`.
   - Soporta entradas `dict` `Form-C` en `TEMPLATES` (`id`, `cid`, `qtype`, `archetype`, `assumption_id`, `gen`, `ver`, `band`, `fmt`, `stems`, `hints`, `sol`, `rats`) y diccionario compartido `RATS`:
     * `fmt` con `@X@` envuelve automáticamente `ans` y valores desnudos de `ds` en `MC7`.
     * `stems` como 2-tupla `(lista_contextos, lista_preguntas)` se expande por producto cartesiano.
     * `ver` admite firma de 2 argumentos `ver(cand, v)` además de 1 argumento `ver(res)`.
     * Compila a `generator_code` / `verifier_code` podados por AST compatibles 100% con `template.schema.json`.

---

## Topología de Gates y Fronteras Exclusivas (`∩ = ∅`)

### Gate 1 — Módulos Nucleares Fase 1 + Fase 2 (6 Díadas Paralelas)
- **Stream `1A` (Stage 1 CTA, `assumptions`, `cta_fixes/`, `affected_line_count`, KaTeX No-Destructivo & DAG Monótono):**
  - Prod: `schemas/cta.schema.json`, `compile_cta.py`, `cta_merge.py`, `check_cta.py`
  - Tests (7): `test_cta_mapreduce.py`, `test_cta_merge_prereq_scoping.py`, `test_c2c_v321_comp1_cta.py`, `test_cta_healing.py`, `test_cta_sweetspot_and_autoheal.py`, `test_fast_ingest_and_cta_append.py`, `test_handouts.py`
- **Stream `1B` (Stage 3 `Form-C` + 4 Arquetipos + Triple `ver_*` + `SymPy`/`Z3` + Poda AST + Hook Síncrono 2D):**
  - Prod: `engine/stage_contract.py`, `compile_shard.py`, `c2c_hook_guard.py`, `budget_guard.py`
  - Tests (9): `test_m3_archetypes_semantic_gate.py`, `test_compile_shard.py`, `test_shard_compiler_hardening.py`, `test_shard06_and_dry_archetypes.py`, `test_invariants_and_shard_overescape_r23.py`, `test_latex_engine.py`, `test_hook_post_pass_and_write_isolation.py`, `test_watchdog_and_hooks.py`, `test_specific_error_report_and_stem_gate.py`
- **Stream `1C` (`sandbox.py` `np.bool_` Fix + *Rejection Sampling*, `check_templates.py` Cache/Parity, `invariants.py` `pykatex`/`KaTeXAST` & `examples/edo,edp`):**
  - Prod: `engine/sandbox.py`, `engine/instantiate.py`, `engine/invariants.py`, `engine/assemble.py`, `check_templates.py`, `schemas/template.schema.json`, `examples/edo/**`, `examples/edp/**`
  - Tests (9): `test_sandbox_adversarial.py`, `test_sandbox_gil_and_circuit_breaker.py`, `test_engine_invariants_adversarial.py`, `test_assemble_katex_and_rationale.py`, `test_assemble_sanitize_katex_r23.py`, `test_katex_prairielearn_tokens.py`, `test_c2c_error_aggregation.py`, `test_template_variability.py`, `test_blind_guess_empirical.py`
- **Stream `1D` (`dispatch.py` Deduplicación `-2M` Tokens + Slicing `< 2 KB` + `author_snapshot.json`, `plan_shards.py` `MIN_ARCHETYPES=4` & Reescritura `Form-C` de `system_prompts/`):**
  - Prod: `plan_shards.py`, `dispatch.py`, `subagent_types.json`, `system_prompts/*.md`, `system_prompts/lean/*.md`
  - Tests (6): `test_dispatch_turn0_and_milestone3_prompts.py`, `test_c2c_v321_comp4_prompts.py`, `test_c2c_v321_comp3_dispatch.py`, `test_weighted_sharding_m7.py`, `test_skill_v3.py`, `test_orchestration_resilience.py`
- **Stream `1E` (`interstage_schemas.py`, `judge.py` 1-Seed Pre-Verificada + Dominancia Bayesiana $\alpha_{\text{Kernel}}=0$, `course_publisher.py` & `standardized_audit_engine.py`):**
  - Prod: `engine/interstage_schemas.py` `[NEW]`, `judge.py`, `course_publisher.py`, `course-qa-evaluator/scripts/standardized_audit_engine.py`
  - Tests (5): `test_new_audit_linters.py`, `test_c2c_validator_prescriptive.py`, `test_dispatch_scope.py`, `test_pipeline_optimizations.py`, `test_c2c_straggler_and_postproduction_prevention.py`
- **Stream `1F` (Linters Psicométricos `src/validator/` & `repair_loop.py`):**
  - Prod: `repair_loop.py`, `src/validator/psychometric_checker.py`, `src/validator/rules.py`, `src/validator/lexical_scanner.py`
  - Tests (2): `test_validator.py`, `test_katex_overescape_validator_r23.py`

### Gate 2 — Integración de `run.py`, Suites Multi-Módulo y Compuertas CI Milestone 18 (3 Díadas Paralelas tras `6/6 PASS::` en Gate 1)
- **Stream `2A`:** Prod: `run.py`, `SKILL.md`, `.agents/rules/c2c-quality-invariants.md` `[NEW]` | Tests (7): `test_prompts_contract_alignment.py`, `test_bootstrap_and_wave_streaming.py`, `test_run_templates_and_dispatch_repair.py`, `test_append_workflow.py`, `test_c2c_v321_multi_instance_and_append.py`, `test_skill.py`, `test_delete_course.py`
- **Stream `2B`:** Prod: Ninguno | Tests (7): `test_c2c_solow2_architectural_improvements.py`, `test_c2c_remediation_optimization.py`, `test_c2c_v31_adversarial_plan.py`, `test_c2c_case_2b_mastery.py`, `test_c2c_v321_comp2_shard.py`, `test_pipeline_reparations.py`, `test_system_prompts_compile_clean.py` `[NEW]`
- **Stream `2C`:** Prod: Ninguno | Tests (4): `test_forensic_replay_ab30cf91.py`, `test_forensic_shard06_and_variance_v34.py`, `test_sweetspot_v35_cta_and_shards.py`, `test_c2c_v40_formal_certification.py` `[NEW]`

### Gate 3 — Certificación Forense Global Read-Only
- Ejecución paralela completa (`-n auto --dist worksteal`) de las **`63/63` suites** (`< 30 s`), verificación LF de `subagent_types.json`, byte-budget `<= 4,750 B` de `lean/prompt_shard_author.md`, `0` subcadenas Zero-Domain prohibidas, corrida empírica de `standardized_audit_engine.py`, verificación viva de `lean 4.35.0` / `z3` / `pykatex` / `hypothesis` y `git status` limpio.
