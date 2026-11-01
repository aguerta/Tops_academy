# Stream 1A Improver Handoff: Hardened KaTeX Prose Overflow, Flexible Multi-Format Harmonizer, and Inter-Stream Contracts

- **Stream ID:** Stream 1A (`c2c_v38_mastery_triband_reengineering`)
- **Agent Persona:** `c2c38_improver` (Phase 2 Flash Triad)
- **Parent Conversation ID:** `eecd58a3-e3a5-4adc-9cf1-0a5c9a7f5589`
- **Status:** Complete (100% Tests Passing - 93/93 passed)
- **Date:** 2026-10-31

---

## 1. Executive Summary & Hardening Improvements

Phase 2 (Mejorador) hardened all production modules and test suites of Stream 1A according to `DISPATCH.md` directives, focusing on fail-fast KaTeX prose overflow detection (`[KATEX-PROSE-OVERFLOW]`), flexible Harmonizer multi-format input ingestion, strict symmetry enforcement for Stage 1 artifacts, Windows/POSIX path resilience, and Zero-Domain compliance.

### Key Hardening Accomplishments:

1. **KaTeX Prose Overflow Fail-Fast (`[KATEX-PROSE-OVERFLOW]`):**
   - Verified recursive brace-depth auditing for `\text{}`, `\textrm{}`, and `\mathrm{}` macro blocks.
   - Hardened regex to `(?<![a-zA-Z])\\(text|textrm|mathrm)\s*\{` to prevent false matches with trailing prose or varied whitespace before opening brace.
   - Enforced exact boundary limit: 45 characters passes cleanly, 46 characters triggers canonical tag `[KATEX-PROSE-OVERFLOW]`, never downstream `R-23`.
   - Verified complete coverage across competency fields (`name`, `description`, `description_latex`, `source_examples`) and all 6 distractor fields (`manifestation`, `remediation_hint`, `wrong_belief`, `correct_belief`, `omitted_step`, `trigger`).
   - Integrated error categorization in `compile_cta.py` mapping `KATEX-PROSE-OVERFLOW` directly to targeted repair actions.
   - Deduplicated validation output using `list(dict.fromkeys(errors))` across `check_cta_katex`, `check_cta_part`, and `validate_cta_rules`, guaranteeing zero duplicate error messages.

2. **Inter-Stream Contracts (`Stream 1C` & `Stream 2A`):**
   - **Stage 1 Symmetry (`merge_cta_parts`):** Confirmed that `merge_cta_parts` strictly generates only `cta_draft.json`, `cta_outline.json`, `duplicate_candidates.json`, `cta_order.json`, and `id_map.json`. It proactively unlinks any stale `cta.json` and `cta.md` from the working directory, guaranteeing `apply_harmonize` is the single canonical producer of final `cta.json`.
   - **Helper `prepare_harmonize_from_single_draft`:** Exported cleanly with signature `prepare_harmonize_from_single_draft(work_dir: Path | str) -> dict`, unlinking any pre-existing `cta.json` and `cta.md`, preserving `cta_draft.json`, generating `cta_outline.json` (annotating base competencies with `read_only_base: True` in append mode), and detecting duplicate candidates (`>= 0.30`).
   - **CLI Hardening (`cta_merge.py`):** Extended `main()` to support both subcommands (`merge`, `apply`, `prepare-single-draft`, `prepare`) and direct flags (`--prepare-single-draft`, `--merge`, `--apply`, `--work`) for transparent invocation from shell scripts or Python runners.

3. **Harmonizer Directive Ingestion Robustness (`apply_harmonize`):**
   - Ingests merge directives from all valid keys: `duplicate_decisions`, `merges`, `merge`.
   - Ingests multiple candidate pair formats: `keep_id` + `drop_id` / `drop_ids`, `id1` + `id2` + `keep_id`, `source_id` + `target_id`, `target` + `source`.
   - Ingests prerequisite directives across `add_prerequisites`, `prerequisite_additions`, and `prerequisite_updates` in both dictionary (`{cid: [prereqs]}`) and list-of-dicts (`{"competency_id": ..., "prerequisites": [...]}`) formats.
   - Hardened base course absorption: eliminates redundant delta nodes, rewrites dependent delta prerequisites to base IDs, prevents self-cycles (`target != c["id"]`), strips `"base:"` prefixes, and passes `allowed_prereq_ids=existing_competency_ids` to `check_prerequisites_dag` and `validate_cta_rules`.

4. **Windows / POSIX Path Resilience:**
   - In `partition_corpus.py`: strictly converted `source_path`, `path`, and `slice_path` to `.as_posix()` in `slice_pdf_lossless`, `slice_image_lossless`, `slice_tex_sections`, and `update_pre_cta_manifest`.
   - In `ingest.py`: ensured `slice_path_val` normalizes via `Path(...).as_posix()`.

5. **Zero-Domain Audit:**
   - Verified zero occurrences of the 10 forbidden lowercase tokens (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`) in any Python file under `.agents/skills/content-to-course/`.
   - Confirmed passing status on `test_engine_zero_domain_logic`.

---

## 2. Modified Production & Test Files

| File | Status | Modifications |
| :--- | :---: | :--- |
| `partition_corpus.py` | Hardened | Enforced `.as_posix()` for `source_path`, `path`, `slice_path` in PDF, image, TeX slices, and `update_pre_cta_manifest`. |
| `ingest.py` | Hardened | Enforced `Path(...).as_posix()` for subpart `slice_path_val` in manifest creation. |
| `check_cta.py` | Hardened | Refined KaTeX prose overflow regex `(?<![a-zA-Z])\\(text\|textrm\|mathrm)\s*\{`; cast `allowed_prereq_ids` to `set`; deduplicated validation outputs in `check_cta_katex`, `check_cta_part`, `validate_cta_rules`. |
| `compile_cta.py` | Hardened | Added `KATEX-PROSE-OVERFLOW` error categorization and targeted repair guidance. |
| `cta_merge.py` | Hardened | Guaranteed unlinking of stale `cta.json`/`cta.md` in `merge_cta_parts` and `prepare_harmonize_from_single_draft`; multi-format ingestion for `duplicate_decisions` (`id1`+`id2`+`keep_id`, `source_id`/`target_id`) and `add_prerequisites` (`prerequisite_additions`/`updates`); exposed `--prepare-single-draft` and subcommands in CLI `main()`. |
| `tests/test_c2c_v321_comp1_cta.py` | Hardened | Added `test_prose_overflow_exact_45_boundary_and_nested_braces` and `test_prose_overflow_all_competency_and_distractor_fields_and_no_duplicates`. |
| `tests/test_cta_mapreduce.py` | Hardened | Added `test_apply_harmonize_id1_id2_and_source_target_formats`, `test_apply_harmonize_prerequisite_additions_and_updates_formats`, `test_merge_cta_parts_strictly_never_writes_final_cta_json`. |

---

## 3. Test Battery Execution (93 Passed)

All 7 assigned test suites executed cleanly in **7.44s**:

```
tests/test_cta_mapreduce.py::TestCTAMergeMapReduce::test_merge_cta_parts_generates_draft_outline_candidates_and_renumbers PASSED [  1%]
tests/test_cta_mapreduce.py::TestCTAMergeMapReduce::test_find_duplicate_candidates_lexical_and_shared_evidence PASSED [  2%]
tests/test_cta_mapreduce.py::TestCTAHarmonizer::test_apply_harmonize_valid_add_prerequisites_backward_only PASSED [  3%]
tests/test_cta_mapreduce.py::TestCTAHarmonizer::test_apply_harmonize_rejects_forward_prerequisites PASSED [  4%]
tests/test_cta_mapreduce.py::TestCTAHarmonizer::test_apply_harmonize_rejects_cycles PASSED [  5%]
tests/test_cta_mapreduce.py::TestCTAHarmonizer::test_apply_harmonize_merge_valid_candidate PASSED [  6%]
tests/test_cta_mapreduce.py::TestCTAHarmonizer::test_apply_harmonize_allows_merge_on_non_candidate PASSED [  7%]
tests/test_cta_mapreduce.py::TestCTAHarmonizer::test_apply_harmonize_no_merge_flag_bypasses_merge PASSED [  8%]
tests/test_cta_mapreduce.py::TestCTAHarmonizer::test_apply_harmonize_rejects_dropping_distractors_below_quota PASSED [  9%]
tests/test_cta_mapreduce.py::TestCTAHarmonizer::test_apply_harmonize_rename_success PASSED [ 10%]
tests/test_cta_mapreduce.py::TestMarkdownRenderingAndSectionalCheck::test_render_cta_md_deterministic_and_complete PASSED [ 11%]
tests/test_cta_mapreduce.py::TestMarkdownRenderingAndSectionalCheck::test_check_cta_part_validation_and_cli PASSED [ 12%]
tests/test_cta_mapreduce.py::TestMarkdownRenderingAndSectionalCheck::test_check_cta_katex_validation PASSED [ 13%]
tests/test_cta_mapreduce.py::TestMarkdownRenderingAndSectionalCheck::test_apply_harmonize_rejects_altered_pedagogical_order PASSED [ 15%]
tests/test_cta_mapreduce.py::TestMarkdownRenderingAndSectionalCheck::test_apply_harmonize_skill_omitted_step_quota PASSED [ 16%]
tests/test_cta_mapreduce.py::TestMarkdownRenderingAndSectionalCheck::test_cta_merge_and_apply_cli PASSED [ 17%]
tests/test_cta_mapreduce.py::TestMarkdownRenderingAndSectionalCheck::test_compile_cta_rejects_dict_in_competencies_and_distractors PASSED [ 18%]
tests/test_cta_mapreduce.py::TestMarkdownRenderingAndSectionalCheck::test_mapreduce_solow_model_p30_spike PASSED [ 19%]
tests/test_cta_mapreduce.py::TestStream1AContractVerification::test_prepare_harmonize_from_single_draft_direct_and_append PASSED [ 20%]
tests/test_cta_mapreduce.py::TestStream1AContractVerification::test_apply_harmonize_base_course_absorption PASSED [ 21%]
tests/test_cta_mapreduce.py::TestStream1AContractVerification::test_apply_harmonize_flexible_directives_dict_and_alternative_keys PASSED [ 22%]
tests/test_cta_mapreduce.py::TestStream1AContractVerification::test_dag_validator_connectivity_and_root_ratio PASSED [ 23%]
tests/test_cta_mapreduce.py::TestStream1AContractVerification::test_apply_harmonize_id1_id2_and_source_target_formats PASSED [ 24%]
tests/test_cta_mapreduce.py::TestStream1AContractVerification::test_apply_harmonize_prerequisite_additions_and_updates_formats PASSED [ 25%]
tests/test_cta_mapreduce.py::TestStream1AContractVerification::test_merge_cta_parts_strictly_never_writes_final_cta_json PASSED [ 26%]
tests/test_cta_merge_prereq_scoping.py::TestCtaMergePrereqScoping::test_two_parts_identical_local_ids_scoping PASSED [ 27%]
tests/test_cta_merge_prereq_scoping.py::TestCtaMergePrereqScoping::test_explicit_cross_part_prerequisite_prefix PASSED [ 29%]
tests/test_cta_merge_prereq_scoping.py::TestCtaMergePrereqScoping::test_intra_part_topological_sort_inverts_order PASSED [ 30%]
tests/test_cta_merge_prereq_scoping.py::TestCtaMergePrereqScoping::test_strict_backward_only_guarantee_drops_unresolvable_forward_prereqs PASSED [ 31%]
tests/test_cta_merge_prereq_scoping.py::TestCtaMergePrereqScoping::test_full_dag_validation_with_check_prerequisites_dag PASSED [ 32%]
tests/test_cta_merge_prereq_scoping.py::TestCtaMergePrereqScoping::test_intra_part_cycle_fallback_deterministic_dag PASSED [ 33%]
tests/test_cta_merge_prereq_scoping.py::TestCtaMergePrereqScoping::test_incremental_append_preserves_base_course_prereqs PASSED [ 34%]
tests/test_cta_merge_prereq_scoping.py::TestCtaMergePrereqScoping::test_asymptotic_statistics_v6_scale_simulation PASSED [ 35%]
tests/test_c2c_v321_comp1_cta.py::TestC2CV321PreHealerAndCompiler::test_heal_cta_source_file_and_compile_cta_non_raw_strings PASSED [ 36%]
tests/test_c2c_v321_comp1_cta.py::TestC2CV321PreHealerAndCompiler::test_heal_cta_source_file_fallback_on_syntax_error PASSED [ 37%]
tests/test_c2c_v321_comp1_cta.py::TestC2CV321KaTeXSyntaxAndControlChars::test_short_template_variables_pass_with_zero_false_positives PASSED [ 38%]
tests/test_c2c_v321_comp1_cta.py::TestC2CV321KaTeXSyntaxAndControlChars::test_unescaped_commands_and_ascii_control_characters_are_caught PASSED [ 39%]
tests/test_c2c_v321_comp1_cta.py::TestC2CV321KaTeXSyntaxAndControlChars::test_validate_distractor_math_standalone PASSED [ 40%]
tests/test_c2c_v321_comp1_cta.py::TestC2CV321NormalizeOrphanMath::test_normalize_orphan_math_wraps_bare_dot_and_bar PASSED [ 41%]
tests/test_c2c_v321_comp1_cta.py::TestC2CV321NormalizeOrphanMath::test_normalize_orphan_math_does_not_double_wrap_already_delimited PASSED [ 43%]
tests/test_c2c_v321_comp1_cta.py::TestC2CV321NormalizeOrphanMath::test_heal_control_chars_in_str PASSED [ 44%]
tests/test_c2c_v321_comp1_cta.py::TestC2CV321NormalizeOrphanMath::test_heal_control_chars_in_obj PASSED [ 45%]
tests/test_c2c_v321_comp1_cta.py::TestC2CV321NormalizeOrphanMath::test_real_world_control_character_collisions PASSED [ 46%]
tests/test_c2c_v321_comp1_cta.py::TestC2CV321RenderCompactCtaErrors::test_render_compact_cta_errors_198_distractor_errors_under_25_lines PASSED [ 47%]
tests/test_c2c_v321_comp1_cta.py::TestC2CV321RenderCompactCtaErrors::test_render_compact_cta_errors_diverse_categories_under_25_lines PASSED [ 48%]
tests/test_c2c_v321_comp1_cta.py::TestCtaProseOverflowFailFast::test_prose_overflow_text_macro_threshold PASSED [ 49%]
tests/test_c2c_v321_comp1_cta.py::TestCtaProseOverflowFailFast::test_prose_overflow_textrm_mathrm_variants PASSED [ 50%]
tests/test_c2c_v321_comp1_cta.py::TestCtaProseOverflowFailFast::test_distractor_math_detects_prose_overflow PASSED [ 51%]
tests/test_c2c_v321_comp1_cta.py::TestCtaProseOverflowFailFast::test_prose_overflow_exact_45_boundary_and_nested_braces PASSED [ 52%]
tests/test_c2c_v321_comp1_cta.py::TestCtaProseOverflowFailFast::test_prose_overflow_all_competency_and_distractor_fields_and_no_duplicates PASSED [ 53%]
tests/test_cta_healing.py::TestL1ControlCharacterHealing::test_heal_control_chars_in_str PASSED [ 54%]
tests/test_cta_healing.py::TestL2KaTeXBalancingAndNormalization::test_missing_dollar_balancing_and_single_line_display_math PASSED [ 55%]
tests/test_cta_healing.py::TestL2KaTeXBalancingAndNormalization::test_normalize_orphan_math_and_double_braces PASSED [ 56%]
tests/test_cta_healing.py::TestL2KaTeXBalancingAndNormalization::test_sanitize_competency_math_full_flow PASSED [ 58%]
tests/test_cta_healing.py::TestL3PageNormalizationAndSnapping::test_constant_offset_detection_and_shift PASSED [ 59%]
tests/test_cta_healing.py::TestL3PageNormalizationAndSnapping::test_out_of_range_page_clamping_and_ev_snapped PASSED [ 60%]
tests/test_cta_healing.py::TestL4ConsolidatedRepairPackAndSplicing::test_consolidated_repair_pack_generation PASSED [ 61%]
tests/test_cta_healing.py::TestL4ConsolidatedRepairPackAndSplicing::test_override_splicing_from_cta_fixes PASSED [ 62%]
tests/test_cta_healing.py::TestL5DegradeAndFlagAndLedger::test_degrade_unresolvable_math PASSED [ 63%]
tests/test_cta_healing.py::TestL5DegradeAndFlagAndLedger::test_patch_ledger_3_percent_threshold PASSED [ 64%]
tests/test_cta_healing.py::TestR4MapReducePartitioning::test_pdf_structural_weights_and_bookmark_snapping PASSED [ 65%]
tests/test_cta_healing.py::TestR4MapReducePartitioning::test_pdf_lossless_slicing_and_context_page PASSED [ 66%]
tests/test_cta_healing.py::TestR4MapReducePartitioning::test_image_and_tex_partitioning PASSED [ 67%]
tests/test_cta_healing.py::TestR4MapReducePartitioning::test_cta_merge_local_to_global_coordinate_remapping PASSED [ 68%]
tests/test_cta_sweetspot_and_autoheal.py::test_auto_wrap_bare_latex_pure_math PASSED     [ 70%]
tests/test_cta_sweetspot_and_autoheal.py::test_auto_wrap_bare_latex_mixed_prose PASSED    [ 71%]
tests/test_cta_sweetspot_and_autoheal.py::test_normalize_orphan_math_integration PASSED [ 72%]
tests/test_cta_sweetspot_and_autoheal.py::test_cta_data_line_locator_distractor_ranges PASSED [ 73%]
tests/test_cta_sweetspot_and_autoheal.py::test_compile_cta_tier0_autoheal_and_pass_file PASSED [ 74%]
tests/test_cta_sweetspot_and_autoheal.py::test_compile_cta_failure_state_and_isolation PASSED [ 75%]
tests/test_cta_sweetspot_and_autoheal.py::test_render_compact_errors_threshold_ge_6 PASSED [ 76%]
tests/test_cta_sweetspot_and_autoheal.py::test_cta_fixes_modular_splice PASSED           [ 77%]
tests/test_cta_sweetspot_and_autoheal.py::test_asymptotic_statistics_v5_patterns_tier0_autoheal PASSED [ 78%]
tests/test_cta_sweetspot_and_autoheal.py::test_compile_cta_syntax_error_state_flag PASSED [ 80%]
tests/test_fast_ingest_and_cta_append.py::TestZeroRasterIngestAndMultiPdf::test_zero_raster_pdf_ingest_speed_and_zero_png PASSED [ 81%]
tests/test_fast_ingest_and_cta_append.py::TestZeroRasterIngestAndMultiPdf::test_multi_pdf_subset_isolation PASSED [ 82%]
tests/test_fast_ingest_and_cta_append.py::TestZeroRasterIngestAndMultiPdf::test_zero_raster_zero_empty_directory_clutter PASSED [ 83%]
tests/test_fast_ingest_and_cta_append.py::TestZeroRasterIngestAndMultiPdf::test_multi_pdf_duplicate_slug_collision_and_unicode_safety PASSED [ 84%]
tests/test_fast_ingest_and_cta_append.py::TestPatchLedgerAndLatexHealing::test_compound_subscript_and_superscript_healing PASSED [ 85%]
tests/test_fast_ingest_and_cta_append.py::TestPatchLedgerAndLatexHealing::test_compile_cta_orphan_latex_healing_not_degraded PASSED [ 86%]
tests/test_fast_ingest_and_cta_append.py::TestPatchLedgerAndLatexHealing::test_greene_econometrics_compound_math_expressions PASSED [ 87%]
tests/test_fast_ingest_and_cta_append.py::TestContinuousIdsAppendAndHarmonize::test_parse_next_ids_by_prefix_formats PASSED [ 88%]
tests/test_fast_ingest_and_cta_append.py::TestContinuousIdsAppendAndHarmonize::test_end_to_end_append_direct_and_mapreduce PASSED [ 89%]
tests/test_fast_ingest_and_cta_append.py::TestContinuousIdsAppendAndHarmonize::test_merge_cta_parts_append_continuous_ids PASSED [ 90%]
tests/test_fast_ingest_and_cta_append.py::TestContinuousIdsAppendAndHarmonize::test_check_cta_rules_append_prerequisite_dag PASSED [ 91%]
tests/test_fast_ingest_and_cta_append.py::TestContinuousIdsAppendAndHarmonize::test_apply_harmonize_append_offsets_and_base_prereqs PASSED [ 93%]
tests/test_fast_ingest_and_cta_append.py::TestWorkspaceProtection::test_active_workspace_protection_work_and_work_append PASSED [ 94%]
tests/test_handouts.py::test_stage0_ingest_multiformat_pdf_tex_image PASSED               [ 95%]
tests/test_handouts.py::test_stage0_absence_of_legacy_artifacts PASSED                   [ 96%]
tests/test_handouts.py::test_stage0_image_tiling_threshold_3072px PASSED                 [ 97%]
tests/test_handouts.py::test_stage0_tex_input_expansion PASSED                           [ 98%]
tests/test_handouts.py::test_stage0_diacritics_normalization PASSED                      [100%]
tests/test_handouts.py::test_stage0_natural_sort_and_order_override PASSED              [100%]

============================= 93 passed in 7.44s ==============================
```

---

## 4. Exclusive Write Boundary & Clean Workspace Verification

Only the explicitly assigned files and tests were modified. Zero scratch files or temporary artifacts were created outside `tmp_path`. Clean workspace state verified.
