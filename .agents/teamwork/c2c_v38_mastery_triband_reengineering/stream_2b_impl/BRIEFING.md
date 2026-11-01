# BRIEFING — Stream 2B (Fase 1: Implementador — Suites de Integración Multi-Módulo)

- **Date:** 2026-10-31
- **Agent:** `c2c38_implementer`
- **Stream:** Stream 2B
- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Exclusive Write Boundary:**
  1. `tests/test_c2c_solow2_architectural_improvements.py`
  2. `tests/test_c2c_remediation_optimization.py`
  3. `tests/test_c2c_v31_adversarial_plan.py`
  4. `tests/test_c2c_case_2b_mastery.py`
  5. `tests/test_c2c_v321_comp2_shard.py`
  6. `tests/test_pipeline_reparations.py`
  7. `.agents/teamwork/c2c_v38_mastery_triband_reengineering/stream_2b_impl/BRIEFING.md`
  8. `.agents/teamwork/c2c_v38_mastery_triband_reengineering/stream_2b_impl/handoff.md`

---

## 1. Initial State & Diagnostics

Initial execution of assigned test suites revealed:
- `tests/test_c2c_v321_comp2_shard.py`: Collection error due to `ImportError: cannot import name '_format_socratic_step' from 'compile_shard'`.
- Running the remaining 5 suites: `11 failed, 63 passed, 0 skipped` in 9.22s.
- `tests/test_pipeline_reparations.py`: 19 passed, 0 failed.

---

## 2. Granular Root Causes & Exact Line Mappings

### 2.1 `tests/test_c2c_v321_comp2_shard.py`
- **Line 60:** Deprecated import `_format_socratic_step`. In C2C v3.8, Socratic hint auto-synthesis from `wrong_belief` was removed; hints must be 3..5 explicit hints in Form-B tuples.
- **Lines 442–460 (`test_9_element_tuple_socratic_hints_synthesis_math_integrity`):** Tests deprecated `_format_socratic_step`. Update to test explicit Form-B hints validation preserving LaTeX math integrity (`$K$`, `\Delta K`) without improper alterations and verifying strict hint rules (3..5 hints, >= 25 chars, no anti-socratic catchphrases, no literal `wrong_belief` copying).
- **Lines 529–542 (`test_compile_shard_end_to_end_seeds_50`):** Shard tuple uses legacy 10-element Form-A format with trivial verifier `return True` and short distractor rationales (`"Err {i}"` < 20 chars, no `@var@`).
  - *Fix:* Migrate to Form-B 9-tuple `("T-C-01", "C-01", "multiple_choice", gen_c01, ver_c01, ("medium", "Understand"), stems, hints, solution)`. Interpolate `@k@` in distractors (len >= 20), implement non-trivial verifier, provide >= 3 stems preserving LaTeX math immunity `${k}^*$, $f({k}) = {r}$, ${r}_t$`, and 3 explicit hints.
- **Lines 601–604 (`test_compile_shard_failing_outputs_compact_error_under_30_lines`):** Tuple in failing shard is legacy Form-A.
  - *Fix:* Migrate to Form-B 9-tuple so it reaches distractor ID validation against `cta.json` (`TPL-D1`), producing the expected line-mapped compact error `< 30` lines.

### 2.2 `tests/test_c2c_solow2_architectural_improvements.py`
- **Lines 148–175 (`test_cta_merge_pure_json_parts_performance_and_accuracy`):** Assumes `merge_cta_parts()` produces `cta.json` and `cta.md`. Under v3.8 contracts, `merge_cta_parts()` produces `cta_draft.json` and `cta_outline.json` (while `apply_harmonize()` produces `cta.json` and `cta.md`).
  - *Fix:* Verify `cta_draft.json` and `cta_outline.json` after `merge_cta_parts()`.
- **Lines 217–224 (`test_cta_merge_renumbers_and_detects_duplicate_candidates_across_parts`):** Checks `cta.json` after `merge_cta_parts()`.
  - *Fix:* Check `cta_draft.json`.
- **Lines 408–420 (`test_preseed_author_scaffolds_generates_valid_modular_scaffolds`):** Legacy Form-A 9-tuple and static rationales < 20 chars without `@var@`.
  - *Fix:* Convert to Form-B 9-tuple with explicit `(difficulty, bloom)`, >= 3 stems, 3..5 hints >= 25 chars, and dynamic distractor rationales interpolating `@tc@` / `@th@`.
- **Lines 560–572 (`test_simulated_cta_subagent_full_workflow`):** `runner.execute(target_stage="cta-merge")` produces `cta_draft.json`.
  - *Fix:* Assert on `cta_draft.json` for `cta-merge` stage.
- **Lines 643–688 (`test_simulated_shard_author_subagent_full_workflow`):** 4 archetypes written as Form-A legacy tuples with static rationales.
  - *Fix:* Convert all 4 templates to Form-B 9-tuples with tri-band difficulty coverage, bloom diversity, >= 3 stems, 3..5 hints >= 25 chars, and dynamic distractor rationales interpolating `@tc@` / `@th@`.
- **Lines 1097–1127 (`test_compile_shard_native_functions_exact_line_mapping_and_pre_shard_blocker`):** Form-A legacy tuple with static rationales.
  - *Fix:* Convert to Form-B 9-tuple with dynamic rationales interpolating `@s@` / `@k_star@`, >= 3 stems, and 3..5 hints >= 25 chars.

### 2.3 `tests/test_c2c_remediation_optimization.py`
- **Lines 275–295 (`test_component_1_anti_overwrite_backup_and_course_id_resolution`):** 10 competencies created with empty prerequisites `[]`. Triggered v3.8 DAG invariant: 10 disconnected components and root_ratio = 100% (> 20%).
  - *Fix:* Chain prerequisites `C-01 -> C-02 -> ... -> C-10` so connected_components = 1 and root_ratio = 1/10 = 10% <= 20%.
- **Lines 382–395 (`test_component_2_canonical_template_generator_validates_cleanly`):** Shard code has legacy Form-A tuple and static rationales < 20 chars.
  - *Fix:* Convert to Form-B 9-tuple with dynamic rationales interpolating `@tc@` / `@th@`, >= 3 stems, and 3..5 hints >= 25 chars.

### 2.4 `tests/test_c2c_v31_adversarial_plan.py`
- **Lines 474–486 (`test_pilar2_preseed_author_scaffolds_end_to_end_zero_errors`):** Form-A legacy tuple with static rationales.
  - *Fix:* Convert to Form-B 9-tuple with dynamic rationales interpolating `@tc@` / `@th@`, >= 3 stems, and 3..5 hints >= 25 chars.
- **Lines 565–577 (`test_pilar2_starter_template_special_characters_and_single_quotes`):** Form-A legacy tuple, static rationales without `@k@`, trivial verifier.
  - *Fix:* Convert to Form-B 9-tuple with dynamic rationales interpolating `@k@`, non-trivial verifier, >= 3 stems, and 3..5 hints >= 25 chars.

### 2.5 `tests/test_c2c_case_2b_mastery.py`
- **Lines 377–389 (`test_compile_shard_c2_t4_archetypes`):** 10-element tuples with static rationales and old positional arguments.
  - *Fix:* Convert all 8 templates (4 for C-01, 4 for C-02) to Form-B 9-tuples `(tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution)` with tri-band coverage `{"easy", "medium", "hard"}`, non-trivial verifiers, dynamic distractor rationales interpolating `@var@` tokens (len >= 20), >= 3 stems, and 3..5 hints >= 25 chars.

---

## 3. Strict Safety & Contract Constraints

- **Zero-Domain Rule:** Zero lowercase substrings `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi` in any modified code or comments.
- **Zero-Production Touch:** All edits strictly confined to the 6 test files in `Exclusive Write Boundary`.
- **Pre-Flight Complete:** Ready to proceed with surgical edits.
