# DISPATCH: Stream 2B — Forensic Auditor (`audit_2b`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory (ONLY allowed write target):** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2b_audit`
- **Artifacts to Audit:**
  - Original Stream Spec: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2b_impl/DISPATCH.md`
  - Implementer Handoff: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2b_impl/handoff.md`
  - Improver Spec & Handoff: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2b_impr/{DISPATCH.md,handoff.md}`
  - Audited Code & Tests (READ-ONLY):
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/prompt_blind_judge.md`
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/lean/prompt_blind_judge.md`
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/prompt_cta_architect.md`
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/system_prompts/lean/prompt_cta_architect.md`
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/SKILL.md`
    - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_prompts_contract_alignment.py`

## Audit Checklist
1. **Boundary & Cleanliness Integrity:**
   - Confirm Stream 2B modified ONLY its 8 assigned files above (note: Stream 2A is actively editing `run.py`, `dispatch.py`, `judge.py`, `test_bootstrap_and_wave_streaming.py`, `test_c2c_v321_comp3_dispatch.py`, `test_pipeline_reparations.py` in parallel, and Stage 1 streams modified their own files—do NOT false-flag those). Confirm `subagent_types.json` was NOT touched by Stream 2B and zero temporary `.py` scripts exist in repo root.
2. **Requirement Verification (Prompts + `SKILL.md` v3.3):**
   - `lean/*.md`: Every file under `system_prompts/lean/` is strictly `<= 5,120` bytes on disk.
   - `prompt_shard_author.md` (Full + Lean): Zero `rf"`, `fr"`, or `{{{` inside code blocks; 100% raw strings `r"..."` + `@var@` / `@var:fmt@`; 3–5 disjunct `stem_variants`; `TPL-VAR` & `R-16` `[0.65, 1.35]` guidance; `work/shards/shard_fixes/<CID>.py` hybrid modular edit protocol; `ArtifactMetadata` ban; reading `compile_shard.py` explicitly forbidden (execute-only via `run_command`).
   - `prompt_cta_architect.md` (Full + Lean): `ArtifactMetadata` ban; `--append` (`existing_competencies_outline` & `next_ids_by_prefix`) rules; `granularity: standard` relative density (`3–5` comps per `5–10` pages); `$ ... $` inline math wrapping.
   - `prompt_blind_judge.md` (Full + Lean): Harmonized Pointer Mode (`view_file` ONLY on assigned `work/dispatch/items/judge_XX.json` in Turn 1 -> analytical solving + `write_file` without `ArtifactMetadata` + `DONE:` in Turn 2, while preserving 1-turn inline mode compatibility); zero contradiction.
   - `SKILL.md` v3.3: `run.py --stage bootstrap --director-id`, **Silent Reactive Barrier Protocol** (`0` tools called on partial `DONE:` `k < N` wakeups), `--wave` weighted isolation (`1 Hab/shard`), strict Director diet (`0` reads/edits of `*_data.py` / `shard_fixes/` / `judge_responses_*.json`, delegating to `c2c_repair`), lockfile release.
   - `tests/test_prompts_contract_alignment.py`: Zero fake mocks, zero masked assertions (`check_single_template` verified with strict `assert errors == []` on extracted prompt code examples).
3. **Independent Test Execution:**
   - Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_prompts_contract_alignment.py tests/test_c2c_v321_comp4_prompts.py tests/test_delete_course.py -q`.
   *(Note: avoid running `test_skill.py` if Stream 2A is mid-write on `run.py`/`dispatch.py`, or if `test_skill.py` passes cleanly record it).*
4. Write `BRIEFING.md`, `progress.md`, and `handoff.md` inside `stream_2b_audit/`, then `send_message` starting with `PASS:: stream_2b_audit | ...` or `REJECT:: stream_2b_audit | ...`.
