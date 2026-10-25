# DISPATCH: Stream 1C — Improver (`impr_1c`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1c_impr`
- **Implementer Handoff to Audit & Improve:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1c_impl/handoff.md`
- **Role:** `Phase 2 Mejorador — Stream 1C (Sharding Ponderado M7.4 y Oleadas en plan_shards.py)`

## 1. Strict Write Boundaries (ONLY touch these files + your Teamwork Directory)
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/plan_shards.py`
- `d:/Augusto/personal_portfolio/Tops_academy/tests/test_weighted_sharding_m7.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1c_impr/{BRIEFING.md,progress.md,handoff.md}`

## 2. Hardening & Scrutiny Objectives
1. Read `stream_1c_impl/handoff.md`, `stream_1c_impl/BRIEFING.md`, `plan_shards.py`, and `tests/test_weighted_sharding_m7.py`.
2. Verify genuinely & harden:
   - Does `plan_shards` strictly isolate **max 1 `Skill` (`Hab-*` or `type == "skill"`, case-insensitive, including Spanish `"habilidad"` if normalized)** per shard even when skills appear consecutively (`Hab-03, Hab-04` as in `ab30cf91` `shard_06`, and `Hab-08, Hab-09` as in `shard_14`)?
   - Are `Concept`/`Fact` shards packed contiguously (`<= 2`, or up to `3` pure `Fact` when `N >= 30`) without ever mixing a `Skill` into a `Concept`/`Fact` shard under default Case 2B sharding?
   - Does `Heaviest-First` sorting place all `Hab-*` shards at the front of Wave 1 (`wave_index == 1`), with deterministic tie-breaking, clean `shard_01..shard_NN` IDs, accurate `shard_data_path` matching `shard_id`, and clean `waves` metadata in `pre_shard_manifest.json`?
   - Check downstream consumers (`run.py` `run_stage_shard` and `dispatch.py` `dispatch_authors`—READ-ONLY check!) to confirm every dict key expected in `plan_shards()` return payload and `pre_shard_manifest.json` (`total_competencies`, `total_shards`, `shards[*].shard_id`, `shards[*].competency_count`, `shards[*].weight`, `shards[*].competency_ids`, `shards[*].wave_index`, etc.) matches 100%!
   - Verify `DSL_REFERENCE` has zero leftover `rf"..."` or `{{{...}}}` suggestions and clearly teaches `@var@` / `@var:fmt@`, `stem_variants` (3–5), and `shard_fixes/<CID>.py`.
   - Expand `tests/test_weighted_sharding_m7.py` with adversarial cases (e.g., 0 competencies / empty list graceful handling, case-insensitive `"SKILL"` / `"Hab-10"`, `N=30` pure-fact packing of 3 vs mixed fact+concept packing of 2, CLI `main()` invocation with `--max-wave-size`).
3. Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_weighted_sharding_m7.py -q` plus existing shard tests (`tests/test_compile_shard.py -k TestAdaptiveShardSizing`).
4. Write `BRIEFING.md`, `progress.md`, and `handoff.md`, then `send_message` starting with `DONE:: stream_1c_impr`.
