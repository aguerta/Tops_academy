# BRIEFING — Stream 2B: Multi-Module Integration Suites & CI Prompt-Compiler Parity Gate (Milestone 18.3)

## 1. Context & Scope
- **Assigned Stream:** Stream 2B (Phase A: Orthogonal Implementer — Gate 2).
- **Exclusive Write Boundary:**
  1. `tests/test_c2c_solow2_architectural_improvements.py`
  2. `tests/test_c2c_remediation_optimization.py`
  3. `tests/test_c2c_v31_adversarial_plan.py`
  4. `tests/test_c2c_case_2b_mastery.py`
  5. `tests/test_c2c_v321_comp2_shard.py`
  6. `tests/test_pipeline_reparations.py`
  7. `tests/test_system_prompts_compile_clean.py` [NEW]
  8. `.agents/teamwork/c2c_v40_formal_mas_con_menos/stream_2b_impl/BRIEFING.md` [NEW]
  9. `.agents/teamwork/c2c_v40_formal_mas_con_menos/stream_2b_impl/handoff.md` [NEW]

- **Production Immutability:** Strict prohibition on modifying `.agents/skills/content-to-course/**` and `src/**`.
- **Zero-Domain Invariant:** All code, comments, docstrings in any test or script must NEVER contain forbidden substrings (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`). All text in English.

---

## 2. Pre-Flight Root Cause Analysis of Existing Suites Failures (12 Failures out of 109 tests)

### A. Verifier Tautologies & Distractor Refutation (`VERIFIER-TAUTOLOGY-DETECTED`)
- Under C2C v4.0 strict mode, `compile_shard.py` checks both soundness (`run_ver(c, v, inst) is True`) AND strict distractor refutation (`run_ver(d, v, mutated) is not True`).
- In several legacy synthetic fixtures, verifiers were implemented checking only `res.get("vars", {})` or returning `True` trivially without inspecting the candidate answer:
  1. `test_c2c_solow2_architectural_improvements.py`:
     - `test_preseed_author_scaffolds_generates_valid_modular_scaffolds`: lines 65-68 (`ver_hab01` checked `v.get("ans") == expected` instead of parsing candidate `c` or `res.get("correct")`).
     - `test_simulated_shard_author_subagent_full_workflow`: lines 181-184 (`ver_c01` checked `v.get("ans") == expected`).
     - `test_compile_shard_native_functions_exact_line_mapping_and_pre_shard_blocker`: lines 336-339 (`ver_steady_state` checked `v.get("k_star") == expected`).
  2. `test_c2c_remediation_optimization.py`:
     - `test_component_2_canonical_template_generator_validates_cleanly`: lines 461-464 (`ver_c01` checked `v.get("ans") == expected`).
  3. `test_c2c_v31_adversarial_plan.py`:
     - `test_pilar2_preseed_author_scaffolds_end_to_end_zero_errors`: lines 589-592 (`ver_h01` checked `v.get("ans") == expected`).
     - `test_pilar2_starter_template_special_characters_and_single_quotes`: lines 707-708 (`ver_h01` checked `res.get("vars", {}).get("k") is not None`).
  4. `test_c2c_case_2b_mastery.py`:
     - `test_compile_shard_c2_t4_archetypes`: lines 844-910, 934-994 (Direct, Inverse, Perturbation, Boundary verifiers checked only `res["vars"]` or generic substrings that also matched distractors).
     - `test_triband_multimodal_coverage_and_fib_non_dollar`: lines 1136-1137, 1164-1165 (`ver_mc` and `ver_ms` checked only `res.get("vars", {}).get("k") is not None`).

### B. Verifier Signature Mismatches (`AttributeError: 'str' object has no attribute 'get'`)
- In `test_c2c_v321_comp2_shard.py`:
  - `test_compile_shard_end_to_end_seeds_50`: line 1264 (`def ver_c01(result, *args):`). `inspect.signature` detected 2 positional parameters (`result`, `args`), classifying it as a 2-argument verifier `ver(cand, vars)`. `result` received string candidate `'$427 unidades$'`, causing `result.get(...)` to raise `AttributeError`.
  - `test_compile_shard_failing_outputs_compact_error_under_30_lines`: line 1366 (`def ver_fail(params, ans):`). Same 2-arg signature issue.
  - `test_dynamic_rationale_blocking_when_distractor_omits_var`: line 1466 (`def ver_static_rat(result, *args):`). Same issue.

### C. Subagent Type Specs Prompt Parity (`--lean` by default)
- `test_c2c_solow2_architectural_improvements.py`:
  - `test_dispatch_payload_size_subagent_specs_and_cta_mapreduce_full_prompt_integrity`: line 1360. `generate_define_subagent_specs` creates subagent type specs using `lean=True` (persisting lean static prompts <= 5 KB), while line 1360 asserted equality against `load_system_prompt("prompt_cta_architect.md")` with `lean=False`.

---

## 3. Plan of Execution

1. **Harden 6 Integration Test Files:**
   - Update synthetic template fixtures to use robust 2-arg analytical verifiers `ver(c, v)` (or robust 1-arg `ver(res)` where `c = res.get("correct")`) that parse numbers/values from candidates and strictly refute distractors without tautologies.
   - For `test_dispatch_payload_size_subagent_specs_and_cta_mapreduce_full_prompt_integrity`, align assertion with `lean=True` per default C2C v4.0 architecture.
   - Ensure all updated test code strictly complies with Zero-Domain Invariant (English docstrings/comments, no forbidden tokens).

2. **Implement `tests/test_system_prompts_compile_clean.py` [NEW]:**
   - Extract canonical Python code block from `system_prompts/lean/prompt_shard_author.md`.
   - Setup clean `tmp_path` environment with:
     * Valid `cta.json` for `Hab-01` including 6 distractors (`D-H01-01` to `D-H01-06`) and assumption `A-Hab01-01`, validated via `compile_cta.py` with `require_assumptions=True`.
     * `pre_shard_manifest.json` referencing `Hab-01` with `min_archetypes=4`.
   - Execute `compile_shard.py` in `--strict` mode with `min_archetypes=4` and `seeds=50`.
   - Assert:
     1. `ok is True` and `errors == []`, producing valid `shard_01.cert.json`.
     2. 4 archetypes generated (`1 MC7 + 2 FIB + 1 MS`), `>= 15` unique stems, `div_ratio >= 0.50`.
     3. Assembly via `instantiate_competency` passes `validate_course_content(..., strict=True)` and `standardized_audit_engine.run_full_audit` with 0 critical errors and 0 `ArchetypeEntropyLinter` warnings (`contract_version=2`).
     4. `len(prompt_shard_author.md.read_bytes()) <= 4750` and `subagent_types.json` contains 0 `\r` carriage return bytes.

3. **Validation & Handoff:**
   - Run full 7-suite test run with `pytest -o addopts="" <assigned_suites> -q`.
   - Verify Zero-Domain compliance across all touched files.
   - Document results in `handoff.md` and signal parent orchestrator.
