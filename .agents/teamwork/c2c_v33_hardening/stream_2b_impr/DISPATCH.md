# DISPATCH: Stream 2B — Improver (`impr_2b`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory (Governance Docs):** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2b_impr`
- **Implementer Handoff to Review:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2b_impl/handoff.md`
- **Exclusive Production/Test Write Boundaries:**
  1. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
  2. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
  3. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/prompt_blind_judge.md`
  4. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/lean/prompt_blind_judge.md`
  5. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/prompt_cta_architect.md`
  6. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/lean/prompt_cta_architect.md`
  7. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/SKILL.md`
  8. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_prompts_contract_alignment.py`

> **CRITICAL RULES:**
> - **DO NOT** modify `subagent_types.json` or any `.py` file under `.agents/skills/content-to-course/`!
> - **NEVER** pass `ArtifactMetadata` when calling `write_file` or `edit_file`.
> - Preserve all backward-compatibility keyword anchors required by `tests/test_c2c_v321_comp4_prompts.py` (see `stream_2b_impl/handoff.md` Section 4).

## Hardening & Adversarial Polish Checklist
1. **`compile_shard.py` Read Prohibition Parity (`prompt_shard_author.md` Full + Lean):**
   - Inspect every occurrence of `compile_shard.py` in `prompt_shard_author.md` (Full + Lean). Remember: `c2c_hook_guard.py` and `ROLE_SPECS` v3.3 **DENY** workers from reading `.agents/skills/content-to-course/compile_shard.py` via `read_file`/`view_file` (workers ONLY execute `compile_shard.py` via `run_command` using their `compile_cmd`!). Verify `prompt_shard_author.md` does NOT claim `compile_shard.py` is allowed in `READ`—move `.agents/skills/content-to-course/compile_shard.py` into `FORBIDDEN` to read (keeping the exact string `.agents/skills/content-to-course/compile_shard.py` present in the document so `test_anti_cheat_and_introspection_policy` in `test_c2c_v321_comp4_prompts.py` passes!).
2. **Blind Judge Turn-Count Clarity (`prompt_blind_judge.md` Full + Lean):**
   - Keep `"Zero-Warmup In-Prompt Payload"` and `"RESOLUCIÓN EN 1 SOLO TURNO"` present for inline mode (`--no-pointer`) backward compatibility with `test_c2c_v321_comp4_prompts.py`, while clarifying cleanly that in **Harmonized Pointer Mode** (`pointer=True`), Turn 1 calls `read_file`/`view_file` ONLY on `work/dispatch/items/judge_XX.json` and Turn 2 immediately writes the response JSON (`write_file` without `ArtifactMetadata`) + sends `DONE: <output_path>` (via `send_message` when Orchestrator ID is given + final text).
3. **Lean Prompt Byte Headroom (`<= 5,120` bytes with comfortable margin):**
   - `lean/prompt_shard_author.md` is at `4,916` bytes (`204` bytes margin). Tighten redundant prose slightly (targeting `<= 4,750` bytes) while keeping its complete runnable `@var@` Python example, `stem_variants`, `shard_fixes/<CID>.py`, `ArtifactMetadata` ban, and `compile_shard.py` read ban crystal clear!
4. **Full End-to-End Dry-Run Validation of Prompt Examples (`test_prompts_contract_alignment.py`):**
   - Verify `tests/test_prompts_contract_alignment.py` runs `check_single_template` from `check_templates.py` (not just `instantiate_template`, so `TPL-VAR`, `R-16`, `R-18`, `R-20`, hints count, and `@var@` placeholder rules are all verified!) on every extracted example in `prompt_shard_author.md` (Full + Lean) with **strict `assert errors == []`**!
   - Add an explicit test asserting `prompt_shard_author.md` (Full + Lean) forbids reading `compile_shard.py` (no contradiction with `c2c_hook_guard.py`).

Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_prompts_contract_alignment.py tests/test_c2c_v321_comp4_prompts.py tests/test_skill.py -q`, write `BRIEFING.md`, `progress.md`, and `handoff.md` inside `stream_2b_impr/`, and `send_message` `DONE:: stream_2b_impr | ...` to `d0ce22db-904e-4856-b353-59975bfb5874`.
