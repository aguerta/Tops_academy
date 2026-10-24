# DISPATCH: Stream 1C — Forensic Auditor (`audit_1c`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory (ONLY allowed write target):** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1c_audit`
- **Artifacts to Audit:**
  - Original Stream Spec: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1c_impl/DISPATCH.md`
  - Implementer Handoff: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1c_impl/handoff.md`
  - Improver Spec & Handoff: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1c_impr/{DISPATCH.md,handoff.md}`
  - Audited Code & Tests (READ-ONLY):
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/plan_shards.py`
    - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_weighted_sharding_m7.py`

## Audit Checklist
1. **Boundary Integrity:** Run `git diff -- .agents/skills/content-to-course/plan_shards.py` and confirm Stream 1C modified ONLY `plan_shards.py` and `tests/test_weighted_sharding_m7.py` (note: other streams `1A`, `1B`, `1D`, `1E` are actively editing their own disjoint files in parallel—do NOT flag files belonging to `1A/1B/1D/1E` or baseline dirty files listed in `ORIGINAL_REQUEST.md`).
2. **Requirement Verification (Milestone 7.4 + Bottleneck #12):**
   - Every `Skill` (`Hab-*` / `"skill"` / `"habilidad"`) is strictly isolated in its own 1-competency shard under default Case 2B sharding.
   - `Concept`/`Fact` shards respect `<= 2` (or `<= 3` pure `Fact` when `N >= 30`) without mixing a `Skill`.
   - `Heaviest-First` ordering places all `Skill` shards at the front of Wave 1 (`wave_index == 1`), with `max_wave_size = 10` default, accurate `waves` summary in `pre_shard_manifest.json`, and downstream compatibility with `run.py` and `dispatch.py`.
   - `DSL_REFERENCE` teaches `@var@` / `@var:fmt@` in raw strings `r"..."`, 3–5 `stem_variants`, and `shard_fixes/<CID>.py`, with zero `rf"..."` or `{{{`.
   - Zero fake mocks, zero weakened assertions, zero `pytest.skip` workarounds in `tests/test_weighted_sharding_m7.py`.
3. **Independent Test Execution:**
   - Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_weighted_sharding_m7.py -q` and `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_compile_shard.py -k TestAdaptiveShardSizing -q`.
4. Write `BRIEFING.md`, `progress.md`, and `handoff.md` inside `stream_1c_audit/`, then `send_message` starting with `PASS:: stream_1c_audit | ...` or `REJECT:: stream_1c_audit | ...`.
