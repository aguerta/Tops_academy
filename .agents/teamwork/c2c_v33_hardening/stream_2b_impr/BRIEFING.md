# BRIEFING: Stream 2B Improver Pre-Flight & Hardening Plan (`impr_2b`)

**Author:** Stream 2B Improver (`impr_2b`)  
**Date:** 2026-10-24  
**Orchestrator Conversation ID:** `d0ce22db-904e-4856-b353-59975bfb5874`  
**Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2b_impr`  
**Implementer Handoff:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2b_impl/handoff.md`

---

## 1. Architectural Scrutiny & Pre-Flight Review

We conducted a forensic inspection of the 8 assigned files and all pre-existing / newly introduced test suites:
1. **Implementer Delivery Audit:**
   - The Implementer (`impl_2b`) successfully migrated the code examples in `prompt_shard_author.md` (Full + Lean) to raw strings `r"..."` using PrairieLearn `@var@` / `@var:fmt@` tokens, eliminating all occurrences of `rf"..."` / `fr"..."` and triple curly braces `{{{...}}}`.
   - 3–5 disjunct `stem_variants` are declared in both Full and Lean author examples.
   - `prompt_blind_judge.md` (Full + Lean) introduced Harmonized Pointer Mode.
   - `prompt_cta_architect.md` (Full + Lean) documents relative page density for `standard` granularity, Delta Mode compliance, and `$ ... $` math wrapping.
   - `SKILL.md` documents Fast Bootstrap CLI, Silent Reactive Barrier Protocol, weighted waves, director diet, and lockfile release.
   - `ArtifactMetadata` is prohibited across all worker prompts.
   - Existing baseline: 50 tests in target suite passing (100%).

2. **Gaps and Hardening Opportunities Identified:**
   - **`compile_shard.py` Read Prohibition Parity:** In `prompt_shard_author.md` (Full + Lean), line 22 listed `compile_shard.py` generically without the full skill path `.agents/skills/content-to-course/compile_shard.py`, while `c2c_hook_guard.py` explicitly denies `read_file` / `view_file` on `compile_shard.py`. We must align the exact prohibition string so workers understand they ONLY execute `compile_shard.py` via `run_command` using `compile_cmd`, and reading it is strictly forbidden.
   - **Blind Judge Turn-Count Clarity:** In `prompt_blind_judge.md` (Full + Lean), the distinction between Inline Mode (`--no-pointer`, Zero-Warmup In-Prompt Payload, strictly 1 turn) and Harmonized Pointer Mode (`pointer=True`, 2 turns: Turn 1 `view_file`/`read_file` on assigned `judge_XX.json`, Turn 2 `write_file` without `ArtifactMetadata` + `send_message` / text `DONE: <output_path>`) must be made unequivocally distinct to prevent subagents from attempting to write in Turn 1 in pointer mode or asking for permissions.
   - **Lean Prompt Byte Headroom:** `lean/prompt_shard_author.md` is currently at `4,916` bytes (only 204 bytes under the 5,120-byte limit). We will tighten redundant phrasing to achieve `<= 4,750` bytes (> 370 bytes headroom) while keeping all mandatory tokens, runnable `@var@` code block, `stem_variants`, `shard_fixes/`, and prohibitions intact.
   - **End-to-End Dry-Run Validation (`test_prompts_contract_alignment.py`):** The test suite previously evaluated examples through `instantiate_template` and `check_instance_invariants`, but did not run `check_single_template` from `check_templates.py`. Running `check_single_template` on all 3 extracted prompt examples (Full H-01, Full H-02, Lean H-01) exercises the full production pipeline: 50 dry-run sandbox seeds, invariant verification, `TPL-VAR` parameter diversity, `R-16` parity, KaTeX syntax, and distractor coverage with strict `assert errors == []`.
   - **Hook Guard Contradiction Test:** Add an explicit test asserting that `prompt_shard_author.md` (Full + Lean) forbids reading `compile_shard.py` while permitting execution via `run_command`.

3. **Blocker Evaluation:**
   - **Status:** **NO ARCHITECTURAL BLOCKER.**
   - All improvements can be performed strictly within the 8 files of our `Write Boundaries` and `stream_2b_impr/`.
   - No modifications to `subagent_types.json` or `.py` files under `.agents/skills/content-to-course/` are needed.

---

## 2. Hardening & Refinement Plan

1. **`prompt_shard_author.md` (Full):**
   - Refine Section 0 to place `.agents/skills/content-to-course/compile_shard.py` explicitly in `PROHIBIDO leer` (execute ONLY via `run_command`).
   - Retain all legacy anchors required by `test_c2c_v321_comp4_prompts.py` (`replace_file_content`, `Append=True`, `r"`, `\rho`, `\frac`, `\alpha`, `\beta`, `$r$`, `$k$`, `\bar`, `\dot`, `python -c`, `PROHIBIDO`, `R-16`, `0.80`, `1.20`, `R-18`, `R-20`).

2. **`lean/prompt_shard_author.md` (Lean):**
   - Tighten prose to achieve `<= 4,750` bytes.
   - Retain complete runnable `@var@` Python example, `stem_variants`, `shard_fixes/`, `ArtifactMetadata` prohibition, and explicit `compile_shard.py` read prohibition.

3. **`prompt_blind_judge.md` (Full) & `lean/prompt_blind_judge.md` (Lean):**
   - Delineate Inline Mode (strictly 1 turn) vs Harmonized Pointer Mode (2 turns: Turn 1 `view_file` on assigned `judge_XX.json`, Turn 2 `write_file` without `ArtifactMetadata` + `send_message` / text `DONE: <output_path>`).
   - Retain `"Zero-Warmup In-Prompt Payload"`, `"RESOLUCIÓN EN 1 SOLO TURNO"`, `"<work_dir>/judges/judge_XX.json"`, `"<work_dir>/verification/judge_responses_XX.json"`, `"DONE: <output_path>"`.

4. **`tests/test_prompts_contract_alignment.py`:**
   - Expand tests 3, 4, 5 to execute `check_single_template` on all 3 extracted examples with 50 dry-run seeds, verifying `assert errors == []`.
   - Add `test_compile_shard_read_prohibition_parity` asserting `prompt_shard_author.md` (Full + Lean) forbids reading `compile_shard.py`.
   - Add tests for Harmonized Pointer Mode 2-turn contract and lean prompt byte budgets (`<= 4,750` bytes for author lean).

5. **Run & Verify Verification Suites:**
   - Execute pytest on `tests/test_prompts_contract_alignment.py`, `tests/test_c2c_v321_comp4_prompts.py`, `tests/test_skill.py`.
