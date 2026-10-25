# BRIEFING: Stream 2B Pre-Flight Verification & Execution Plan (`impl_2b`)

**Author:** Stream 2B Implementer (`impl_2b`)  
**Date:** 2026-10-24  
**Orchestrator Conversation ID:** `d0ce22db-904e-4856-b353-59975bfb5874`  
**Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2b_impl`

---

## 1. Pre-Flight Inspection Summary

We conducted a comprehensive read-only inspection of:
1. **Target Markdown Prompts and Skill (7 files):**
   - `system_prompts/prompt_shard_author.md` (Full)
   - `system_prompts/lean/prompt_shard_author.md` (Lean)
   - `system_prompts/prompt_blind_judge.md` (Full)
   - `system_prompts/lean/prompt_blind_judge.md` (Lean)
   - `system_prompts/prompt_cta_architect.md` (Full)
   - `system_prompts/lean/prompt_cta_architect.md` (Lean)
   - `SKILL.md` (v3.22 -> v3.3)
2. **Hardened Stage 1 Engine & References (Read-Only):**
   - `engine/assemble.py`: Verified `format_template_string` implementation prioritizing PrairieLearn orthogonal tokens `@var@` / `@var:fmt@` with zero KaTeX brace collisions, regex variable interpolation, and `_strip_giveaway_prefix`.
   - `compile_shard.py`: Verified AST-level tuple parsing (Form A 9/10 elements and Form B), `check_ast_rf_triple_braces`, in-memory healing, `stem_variants` synthesis, and dynamic splicing of modular overrides from `work/shards/shard_fixes/<CID>.py`.
   - `check_templates.py`: Verified rules `[TPL-DRY]` (dry-run execution failure, missing dynamic vars in stem or un-interpolated placeholders), `[TPL-VAR]` (minimum parametric diversity >= 4 unique instances across seeds, stem diversity ratio >= 0.50), and `[R-16]` / `[R-18]` / `[R-20]`.
   - `plan_shards.py`: Inspected `DSL_REFERENCE` for canonical schema, `@var@` PrairieLearn examples, `stem_variants` requirement (3-5 disjunct variants), and modular per-comp overrides.
3. **Existing Verification Suites in `tests/`:**
   - Ran baseline: 83 tests passing in 6.10s.
   - Checked all references to prompt files across test files (`test_c2c_v321_comp4_prompts.py`, `test_dispatch_scope.py`, `test_orchestration_resilience.py`, `test_pipeline_reparations.py`, etc.).
   - Discovered critical compatibility constraints:
     - `test_shift_left_rules_and_short_variable_tables`: Asserts presence of `"Append=True"`, `"replace_file_content"`, `"r\""` / `"r'"`, `"\rho"`, `"\frac"`, `"\alpha"`, `"\beta"`, `"$r$"`, `"$k$"`, `"\bar"`, `"\dot"`, `"python -c"`, `"PROHIBIDO"`, `"R-16"`, `"0.80"`, `"1.20"`, `"R-18"`, `"R-20"` in author prompt; and `"omitted_step"` in CTA prompt.
     - `test_example_1_carnot_cleanliness_and_length_parity`: Searches for `def gen_h01(rng):` up to `def ver_h01`, checking no forbidden prefixes/adverbs and psychometric length parity.
     - `test_example_2_raft_cleanliness_and_length_parity`: Searches for `def gen_h02(rng):` up to `def ver_h02`.
     - `test_prompt_blind_judge_contracts`: Asserts presence of `"Zero-Warmup In-Prompt Payload"`, `"RESOLUCIÓN EN 1 SOLO TURNO"`, `"view_file"`, `"search_web"`, `"<work_dir>/judges/judge_XX.json"`, `"<work_dir>/verification/judge_responses_XX.json"`, `"DONE: <output_path>"`.
     - `test_lean_system_prompts_size_and_contract`: Asserts every file in `system_prompts/lean/*.md` is strictly `<= 5,120` bytes (5 KB).

## 2. Technical Invariants & Conflict Evaluation

- **Status:** **NO BLOCKER DETECTED.**
- All requirements from `DISPATCH.md` can be integrated while harmoniously preserving 100% backward compatibility with all pre-existing tests. Specifically:
  - We preserve the required strings (`replace_file_content`, `Append=True`, `Zero-Warmup In-Prompt Payload`, etc.) while advancing the protocol to v3.3 (documenting `edit_file` / `replace_file_content` for localized edits `<= 15` lines, modular overrides via `shard_fixes/<CID>.py` for larger rewrites, Pointer Mode for Turn 0 reading of assigned `judge_XX.json` or in-prompt payload, and strict prohibition of `ArtifactMetadata`).
  - Lean prompts will be kept compact and strictly under `<= 5,120` bytes.
  - Examples 1 and 2 in `prompt_shard_author.md` (and lean version) will use 100% raw strings `r"..."` with `@var@` PrairieLearn tokens, zero `rf"`/`fr"` and zero `{{{`, while maintaining mathematical length parity and cleanliness.

---

## 3. Detailed Execution Plan

### A. `system_prompts/prompt_shard_author.md` (Full)
1. **PrairieLearn `@var@` / `@var:fmt@` Syntax:**
   - Ban `rf"..."` / `fr"..."` and `{{{...}}}`.
   - Update 100% of code examples and recommended patterns to use raw strings `r"..."` with `@var@` tokens.
   - In `gen_h01` and `gen_h02`, return `@ans@`, `@d1@`..`@d6@`, `@quorum@`, `@f_max@`, etc. inside `vars` and reference them via `@var@` in raw strings.
   - Add explicit notice that any `@var@` or `{var}` used in stem, variants, options, hints, or solution must exist in `vars` dictionary (enforced by `[TPL-DRY]`).
2. **`stem_variants` (3–5 Disjunct Variants):**
   - Document requirement of 3–5 structurally distinct variants per template.
3. **Anti-Collapse (`TPL-VAR`) & Anti-Giveaway (`R-16`) Rules:**
   - Document `[TPL-VAR]` (minimum 4 unique instances across seeds; avoid integer division collapse) and `[R-16]` (length within `[0.80, 1.20]` strict / `[0.65, 1.35]` hardened bounds, genuine academic detail without filler).
4. **Hybrid Edit & Modular Fix Protocol:**
   - Initial creation: `write_file(Overwrite=True)` on `work/shards/shard_XX_data.py`.
   - Small edits (`<= 15` lines): `edit_file` / `replace_file_content`.
   - Block rewrites (`> 15` lines) or `c2c_repair`: write ONLY the competency to `work/shards/shard_fixes/<CID>.py` via `write_file(Overwrite=True)`.
5. **Tool Hygiene:**
   - Explicitly ban passing `ArtifactMetadata` to `write_file` or `edit_file`.
   - Ban reading `compile_shard.py`, `check_templates.py`, `engine/`, `.check_attempts/`, and ban `python -c`.
   - Document Circuit Breaker awareness and `BLOCKER::` / `send_message("BLOCKED: ...")` escalation.

### B. `system_prompts/lean/prompt_shard_author.md` (Lean `<= 5,120` bytes)
- Incorporate PrairieLearn `@var@` raw strings, ban `rf"` / `{{{`, 3-5 `stem_variants`, `shard_fixes/<CID>.py`, `ArtifactMetadata` prohibition, and keep total file size strictly `<= 5,120` bytes.

### C. `system_prompts/prompt_cta_architect.md` (Full)
- Explicitly forbid `ArtifactMetadata` when writing to `work/`.
- Document `--append` / Delta Mode compliance (`existing_competencies_outline`, `next_ids_by_prefix`).
- Clarify `granularity: standard` as relative page density (3-5 competencies per 5-10 pages, not a flat cap of 5).
- Wrap inline symbolic math (`Q_{zx}^{-1}`, `\sqrt{n}`, `X'X`) in `$...$`.

### D. `system_prompts/lean/prompt_cta_architect.md` (Lean `<= 5,120` bytes)
- Mirror the above rules compactly within `<= 5,120` bytes.

### E. `system_prompts/prompt_blind_judge.md` (Full) & `lean/prompt_blind_judge.md` (Lean `<= 5,120` bytes)
- Harmonized Pointer Mode: Turn 0 executes `view_file` ONLY on the single assigned batch file `work/dispatch/items/judge_XX.json` (or reads In-Prompt Payload if pointer=False). Strict prohibition of reading any other files.
- Solve items analytically from first principles, flag unrendered `@var@` / `{var}`, write responses via `write_file` without `ArtifactMetadata`, signal completion with `DONE: <output_path>`.

### F. `SKILL.md` (v3.3)
- Fast bootstrap: single atomic CLI `run.py --stage bootstrap --course-id <id> --sources <...> --director-id <CONVERSATION_ID>`.
- Silent Reactive Barrier Protocol: 0 tools called on partial `k < N` worker wakeups.
- Weighted Waves (max 1 `Skill` / `Hab-*` isolated per shard, waves `<= 10`) and incremental `--ready-only` judge streaming.
- Director diet & Zero manual debugging: Director never reads/edits `*_data.py` or `shard_fixes/`; delegates repairs to `c2c_repair`.
- Release of `.c2c_subagent_lock.json` upon publish / `--stage unlock`.

### G. Verification Suite: `tests/test_prompts_contract_alignment.py`
- Test 1: All lean prompts `<= 5,120` bytes.
- Test 2: Zero occurrences of `rf"` / `fr"` / `{{{` in code blocks in `prompt_shard_author.md` (Full + Lean), and presence of `@` PrairieLearn tokens, `stem_variants`, `shard_fixes/`, `ArtifactMetadata` prohibition.
- Test 3: Programmatic extraction and execution of Python template examples in `prompt_shard_author.md` (Full + Lean) through `engine.instantiate.instantiate_template` / `engine.assemble.assemble_question` with 0 errors and 0 invariant violations.
- Test 4: Zero contradiction in `prompt_blind_judge.md` (Full + Lean) regarding assigned `judge_XX.json` and `ArtifactMetadata` prohibition.
- Test 5: `SKILL.md` v3.3 verification for `--stage bootstrap`, `--director-id`, Silent Reactive Barrier, `--wave`, `shard_fixes`, and `c2c_repair`.

---
Pre-flight check is complete and verified. Proceeding to implementation.
