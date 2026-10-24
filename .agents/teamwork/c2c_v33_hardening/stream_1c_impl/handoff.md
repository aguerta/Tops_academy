# HANDOFF: Stream 1C — Weighted Cognitive Sharding M7.4 & Wave Dispatch

## 1. Summary of Changes
- **Refactored Module:** [`.agents/skills/content-to-course/plan_shards.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/plan_shards.py)
  - **`is_skill_competency`, `is_fact_competency`, `is_concept_competency`:** Helper functions identifying competency pedagogical types from `type` attribute or ID prefixes (`Hab-`/`HAB-`, `C-`, `H-`).
  - **`calculate_competency_weight`:** Updated cognitive weighting per Milestone 7.4 specifications:
    - Skill (`Hab-*`): base `6.0`
    - Concept (`C-*`): base `2.5`
    - Fact (`H-*`): base `1.5`
    - Dynamic distractor surcharge: `+ 0.1 * len(distractors)`
  - **`partition_competencies_weighted`:** New cognitive partitioning algorithm enforcing:
    - *Hard Skill Isolation Rule (Anti-Straggler SLA):* Every skill competency is assigned to an exclusive 1-competency shard (never paired with another skill, concept, or fact).
    - *Contiguous Concept/Fact Grouping:* Adjacent non-skill competencies in curriculum order are packed with max 2 competencies per shard (allowing up to 3 ONLY when all 3 are `fact` and total competencies $N \ge 30$).
  - **`plan_shards`:**
    - Dual partitioning dispatch: default weighted cognitive sharding when `k is None` and `isolate_skills=True`; preserves legacy uniform partitioning when explicit `k` or `isolate_skills=False` is passed.
    - *Heaviest-First Ordering:* Dispatched shards sorted descending by `weight` (breaking ties deterministically by curriculum index). All Skill shards sit at the very front of Wave 1 ($t = 0$).
    - *Wave Indexing & Manifest Summary:* Computes `wave_index` (`1, 2, ...`) for each shard using `max_wave_size` (default: 10), and adds top-level `"total_waves"`, `"max_wave_size"`, and `"waves"` list summary to `pre_shard_manifest.json` and shard JSON payloads.
  - **`DSL_REFERENCE`:**
    - Injects orthogonal tokens `@var@` / `@var:fmt@` in raw strings `r"..."`, forbidding `rf"..."` to eradicate KaTeX collisions.
    - Emphasizes mandatory 3–5 `stem_variants`.
    - Documents modular per-competency overrides via `work/shards/shard_fixes/<CID>.py`.
  - **CLI `main()`:** Added `--max-wave-size` (default 10) and `--no-isolate-skills` flags.

- **New Test Suite:** [`tests/test_weighted_sharding_m7.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/tests/test_weighted_sharding_m7.py)
  - `TestWeightedShardingAb30cf91`: Exact 32-competency curriculum replication from forensic run `ab30cf91` (6 Fact, 16 Concept, 10 Skill in mixed curriculum order).
    - Verifies all 10 `Hab-*` shards have `competency_count == 1`.
    - Verifies all 10 `Hab-*` shards sit in Wave 1 (`wave_index == 1`).
    - Verifies Concept/Fact shards have $\le 2$ competencies.
    - Verifies 100% of 32 competencies are accounted for with zero drops or duplicates.
    - Verifies file persistence of `pre_shard_manifest.json` and `shard_01.json..shard_21.json`.
  - `TestWeightedShardingEdgeCases`:
    - Single competency (concept and skill).
    - All-skill course (8 skills -> 8 exclusive shards).
    - Large 45-competency course (`total_waves >= 2` with `max_wave_size=10`).
    - Explicit `k` override parameter compatibility (`k=4` with 24 comps produces 4 shards of 6 comps).
    - `isolate_skills=False` flag fallback.
  - `TestThreeFactGroupingRule`:
    - 3 facts grouped into 1 shard when $N \ge 30$.
    - 3 facts strictly packed max 2 per shard when $N < 30$.
    - Mixed triplet (2 facts + 1 concept) strictly packed max 2 per shard even when $N \ge 30$.
  - `TestDslReferenceUpdates`:
    - Tests presence of `@var@` orthogonal tokens rule, `stem_variants` quotas, and modular overrides.

## 2. Pre-Flight Notes & Verification
- Strict Write Boundaries respected: Only `plan_shards.py`, `tests/test_weighted_sharding_m7.py`, and `stream_1c_impl/*` files were created or modified.
- Legacy tests calling `determine_shard_count` and `partition_competencies_into_shards` directly continue to work with 100% backward compatibility.

## 3. Test Command & Pass Counts
Target pytest command executed:
```powershell
& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_weighted_sharding_m7.py tests/test_c2c_case_2b_mastery.py tests/test_compile_shard.py tests/test_pipeline_optimizations.py tests/test_skill_v3.py tests/test_template_variability.py -q
```
**Results:** `46 passed, 2 skipped in 4.87s` (100% pass rate).
- `tests/test_weighted_sharding_m7.py`: 13 passed
- `tests/test_c2c_case_2b_mastery.py`: 7 passed
- `tests/test_compile_shard.py`: 12 passed
- `tests/test_pipeline_optimizations.py`: 5 passed, 2 skipped (external Solow CTA)
- `tests/test_skill_v3.py`: 4 passed
- `tests/test_template_variability.py`: 5 passed

## 4. Edge Cases for Improver (`impr_1c`) to Scrutinize
1. **Windows Path and CRLF Handling:** Ensure atomic write paths and POSIX path representations in `pre_shard_manifest.json` (`/` vs `\`) remain consistent across Windows environments.
2. **Tie-Breaking Determinism:** Verify that when two non-skill shards have identical weights, the tie-breaking key `min_curriculum_idx` guarantees 100% reproducible ordering across runs.
3. **Dispatch Integration with Wave Indexing:** Consider whether `dispatch.py` consumers benefit from filtering or grouping by `wave_index` when dispatching subagents in multi-turn execution.
