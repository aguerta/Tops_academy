# DISPATCH: Stream 2B — Implementer (`impl_2b`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory (Governance Docs):** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2b_impl`
- **Exclusive Production/Test Write Boundaries:**
  1. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
  2. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
  3. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/prompt_blind_judge.md`
  4. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/lean/prompt_blind_judge.md`
  5. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/prompt_cta_architect.md`
  6. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/lean/prompt_cta_architect.md`
  7. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/SKILL.md`
  8. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_prompts_contract_alignment.py` *(new)*

> **CRITICAL RULES:**
> - **DO NOT** modify `subagent_types.json`, `run.py`, `dispatch.py`, `judge.py`, `plan_shards.py`, or any `.py` file under `.agents/skills/content-to-course/`! (`subagent_types.json` will be regenerated in Stage 3 after both 2A and 2B pass Gate 2).
> - **NEVER** pass `ArtifactMetadata` when calling `write_file` or `edit_file`.
> - **NEVER** leave temporary `.py` scripts in the workspace root.

## Step 0: Mandatory Pre-Flight Sanity Check
Read all 7 target markdown files (`Full` + `Lean` prompts + `SKILL.md`) plus READ-ONLY inspection of `engine/assemble.py`, `check_templates.py`, `compile_shard.py`, and `plan_shards.py` (`DSL_REFERENCE`) so every single instruction and code snippet in the v3.3 prompts matches the hardened Stage 1 engine 100%!
Also check if any existing test in `tests/` inspects `SKILL.md` or `system_prompts/*.md` (`grep` in `tests/` for `prompt_shard_author`, `prompt_blind_judge`, `prompt_cta_architect`, `SKILL.md`) so you maintain 100% compatibility with existing prompt tests.
Write `stream_2b_impl/BRIEFING.md` confirming Pre-Flight before editing.

## Scope of Implementation (Bottlenecks #1, #2, #3, #4, #5, #6, #7, #9, #12 + Milestones 3, 4 & 7)

### 1. `prompt_shard_author.md` (Full + Lean `<= 5,120` bytes)
- **Orthogonal PrairieLearn `@var@` / `@var:fmt@` Syntax:**
  - Migrate **100% of code examples** to raw strings `r"..."` using `@var@` / `@var:fmt@` (e.g., `r"Sea $\hat{\beta} = @beta_hat:.4f@$ en $\mathbb{R}^{@k@}$"` and matrix example `r"$$\begin{bmatrix} @a11@ & @a12@ \\ @a21@ & @a22@ \end{bmatrix}$$"`).
  - **STRICT PROHIBITION** of `rf"..."` / `fr"..."` and triple/double curly braces `{{{...}}}` or `{{tc}}` (you may mention in 1 concise rule that `rf"` and `{{{` are banned—never emit `rf"` or `{{{` inside any code block or recommended pattern!).
  - Explicitly warn that every `@var@` used in `stem`, `stem_variants`, `options`, `correct_answer`, `accepted_equivalents`, `hints`, or `solution` MUST exist in the `vars` dict returned by `generate(rng)` (uninterpolated `@var@` or `{var}` is hard-blocked by `[TPL-DRY]`).
- **`stem_variants` (3–5 Disjunct Variants):**
  - Require 3–5 structurally distinct `stem_variants` per template (different narrative framing/context, sharing the same `@var@` math contract) for anti-memorization Mastery Learning.
- **Anti-Collapse (`TPL-VAR`) & Anti-Giveaway (`R-16`) Rules:**
  - Teach authors to verify `[TPL-VAR]` (distinct numerical outputs across RNG seeds; avoid integer division or tautological cancellation that collapses instances) and `[R-16]` (keep correct option length balanced within `[0.65, 1.35]` of distractor average via genuine academic detail, never artificial filler).
- **Hybrid Edit & Modular Fix Protocol (Replaces Dogmatic `Overwrite=True` Ban):**
  - Turn 1 initial creation writes `work/shards/shard_XX_data.py` with `write_file(Overwrite=True)`.
  - For localized edits (`<= 15` lines): use `edit_file`.
  - When `[TPL-DRY]`, `[TPL-VAR]`, `[R-16]`, or `[R-20]` requires rewriting a competency block (`> 15` lines) or during `c2c_repair`: write ONLY that competency (`COMPETENCY_DATA = {...}`) to `work/shards/shard_fixes/<CID>.py` using `write_file(Overwrite=True)`! `compile_shard.py` automatically splices `shard_fixes/<CID>.py` in memory without risking `edit_file` target-mismatch failures on 400-line files.
- **Tool Hygiene & Circuit Breaker Awareness:**
  - **NEVER** pass `ArtifactMetadata` to `write_file` or `edit_file`.
  - **NEVER** read `compile_shard.py`, `check_templates.py`, `engine/`, or `.check_attempts/`, and NEVER run `python -c` shell one-liners. Run ONLY the exact `compile_cmd` from the work order. If `[CIRCUIT BREAKER]` triggers, stop immediately and `send_message("BLOCKED: ...")`.

### 2. `prompt_cta_architect.md` (Full + Lean `<= 5,120` bytes)
- Explicitly forbid passing `ArtifactMetadata` to `write_file` / `edit_file` when writing to `work/`.
- Document `--append` / Delta Mode compliance: when `existing_competencies_outline` and `next_ids_by_prefix` are present in the work order, NEVER duplicate competencies already covered in the base course, start new IDs strictly at `next_ids_by_prefix` (`H-XX`, `C-XX`, `Hab-XX`), and allow `prerequisites` to reference existing base IDs.
- Maintain `granularity: standard` as **relative page density** (`3–5` competencies per `5–10` pages of dense academic material, never a flat cap of `5` total across a 50-page book) and wrap all inline symbolic expressions (`Q_{zx}^{-1}`, `\sqrt{n}`, `X'X`) in `$...$`.

### 3. `prompt_blind_judge.md` (Full + Lean `<= 5,120` bytes)
- **Harmonized Pointer Mode (Zero Contradiction):**
  - Turn 0: Execute `view_file` / `read_file` **ONLY** on the single assigned batch file `work/dispatch/items/judge_XX.json` indicated in the prompt. Reading ANY other file (`cta.json`, `templates/`, `shards/`, `judge_ground_truth.json`, `courses/`) is strictly forbidden.
  - Solve every item analytically from first principles (`independent_reasoning` + `selected_index` / `computed_answer`), flag any unrendered `@var@` / `{var}` or broken math (`flaw_detected: true`), write `judge_responses_XX.json` via `write_file` (**WITHOUT** `ArtifactMetadata`), and `send_message("DONE: ...")`.

### 4. `SKILL.md` v3.3 (Director Anti-Oversaturation & `< 90s` Bootstrap Runbook)
Update `SKILL.md` to v3.3 while preserving Stage Contracts and core architecture:
- **Fast Initialization (`<= 60–90s` SLA):** Replace separate multi-turn `prepare` + `define-types` + `dispatch-cta` steps with the single atomic command:
  `& ".venv\Scripts\python.exe" .agents/skills/content-to-course/run.py --stage bootstrap --course-id <id> --sources <...> --director-id <CONVERSATION_ID>`
  followed by reading the 4 small `work/dispatch/types/*.json` files (`<= 5 KB` each) to call `define_subagent`, launching `c2c_cta_architect` with `pointer=True` payloads, and starting the 5-minute `schedule` watchdog (`budget_guard.py`).
- **Golden Rule — Silent Reactive Barrier Protocol (`~12–16` Director Turns Total):**
  - When partial `DONE:` messages arrive from workers (`k < N` of the active wave) and the watchdog timer has NOT fired: the Director **MUST CALL ZERO TOOLS** (do NOT run `Get-ChildItem`, `run.py`, `read_file`, or `manage_subagents` on every wakeup—simply note `Wave progress k/N` in 1 line and end the turn in `< 2s`).
  - Only when `N/N` workers of the wave report `DONE:` (or `BLOCKED:`, or when the `budget_guard.py` timer fires) may the Director invoke `run.py --stage wave-status` / `templates` / `judge-compare`.
- **Weighted Waves (`1 Hab/shard`, `<= 10` per wave) & Incremental Judge Streaming:**
  - Document `dispatch-authors --wave 1` (isolated `Hab-*` skills launched first at `t=0`), followed by subsequent waves and `--ready-only` judge streaming.
- **Strict Director Diet & Zero Manual Debugging:**
  - The Director is **PROHIBITED** (and blocked by `c2c_hook_guard.py`) from reading or editing `*_data.py`, `shard_fixes/*.py`, or `judge_responses_*.json`. Every compilation failure or Judge rejection is delegated via `dispatch.py --role repair` (writing modular overrides to `work/shards/shard_fixes/<CID>.py`).
  - Recommend `/compact` only when chaining multiple courses in a single user session, and verify `.c2c_subagent_lock.json` is released upon `publish` (or `--stage unlock`).

## Verification Suite (`tests/test_prompts_contract_alignment.py`)
Write thorough automated tests verifying:
1. All 3 `system_prompts/lean/*.md` files (and `prompt_repair.md` if present in `lean/`) are strictly `<= 5,120` bytes (`5 KB`).
2. Zero occurrences of `rf"` or `fr"` or `{{{` in code blocks across `prompt_shard_author.md` (Full + Lean), and presence of `@` PrairieLearn tokens, `stem_variants`, `shard_fixes/`, and `ArtifactMetadata` prohibition.
3. Programmatic extraction and execution of Python template examples in `prompt_shard_author.md` (Full + Lean) through `engine.instantiate.instantiate_template` / `engine.assemble.assemble_question` with **0 errors and 0 invariant violations**!
4. Zero contradiction in `prompt_blind_judge.md` (Full + Lean): allows reading assigned `judge_XX.json` while forbidding all other files, plus `ArtifactMetadata` prohibition in CTA/Author/Judge prompts.
5. `SKILL.md` v3.3 documents `--stage bootstrap`, `--director-id`, Silent Reactive Barrier (`0` tools on partial `k < N` wakeups), `--wave`, `shard_fixes`, and `c2c_repair` delegation.

Run `.venv\Scripts\python.exe -m pytest tests/test_prompts_contract_alignment.py` (plus any existing prompt/skill tests), write `progress.md` and `handoff.md` in `stream_2b_impl/`, and `send_message` `DONE:: stream_2b_impl | ...` to `d0ce22db-904e-4856-b353-59975bfb5874`.
