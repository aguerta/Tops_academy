# BRIEFING: Stream 1C — Weighted Cognitive Sharding M7.4 & Wave Dispatch

## 1. Pre-Flight Verification & Codebase State
- **Target File to Refactor:** `.agents/skills/content-to-course/plan_shards.py`
- **Callers and Dependents Analyzed:**
  - `run.py`: Line 510 calls `plan_shards(cta_file, shards_dir, k=self.shards_k, max_comps=self.comps_per_shard)`. Iterates over `res["shards"]` printing `shard_id`, `competency_count`, `weight`, `competency_ids`.
  - `dispatch.py`: Lines 756-857 read `pre_shard_manifest.json` from `work/shards/` or `work/`. Sorts shards heaviest-first using `_shard_weight`. Formats items per shard.
  - `compile_shard.py`: Lines 696-720 load `pre_shard_manifest.json`, match `shard_id` against `s["shard_id"]`, and read `shard_data_path`.
  - `tests/test_c2c_case_2b_mastery.py`: Direct calls to `determine_shard_count` and `partition_competencies_into_shards(comps, k)`. Requires backward compatibility when explicit `k` or `max_comps_per_shard` are passed.
  - `tests/test_compile_shard.py`: Test suite for `determine_shard_count` with integer sizes `N = 1, 8, 16, 24, 32, 43, 60` and explicit `requested_k` / `max_comps_per_shard`.
  - `tests/test_pipeline_optimizations.py`: Calls `plan_shards(..., k=8)` and checks `total_shards <= 8`, `pre_shard_manifest.json`, and `dsl_reference`.
  - `tests/test_skill_v3.py`: Tests `plan_shards` blocker when `pre_cta_manifest.json` is missing, and tests standard deterministic partitioning.
  - `tests/test_template_variability.py`: Direct calls to `determine_shard_count` and `partition_competencies_into_shards`.

## 2. Invariant & Non-Regression Analysis
- **Explicit `k` Override Rule:** When a caller passes an explicit integer `k` (or `requested_k > 0`), the engine maintains legacy uniform partitioning via `partition_competencies_into_shards(competencies, k)` ensuring 100% pass rate on all legacy unit tests.
- **Default Cognitive Sharding (`k is None`):** Activated by default in pipeline runs.
  - Hard Skill Isolation: Every competency with `type == "skill"` (or prefix `Hab-`/`HAB-`) receives an exclusive 1-competency shard.
  - Contiguous Concept/Fact Grouping: Consecutive non-skill competencies (`concept` and `fact`) in curriculum order are packed max 2 competencies per shard (allowing 3 only when all 3 are `fact` and total competencies $N \ge 30$).
- **Cognitive Weights & Heaviest-First Ordering:**
  - Competency weights: `Skill = 6.0`, `Concept = 2.5`, `Fact = 1.5` + `0.1 * len(distractors)`.
  - Dispatched shards sorted descending by `weight` (breaking ties deterministically by curriculum index), ensuring all `Skill` shards sit in Wave 1.
  - Sequential `shard_id` (`shard_01` to `shard_NN`) and `wave_index` (`1, 2, ...`) computed using `max_wave_size: int = 10` (configurable via CLI `--max-wave-size`).
  - Top-level manifest payload contains `total_waves`, `max_wave_size`, and `waves` summary list.
- **`DSL_REFERENCE` Updates:**
  - Injects orthogonal tokens `@var@` and `@var:fmt@` in raw strings `r"..."`, forbidding `rf"..."`.
  - Re-states mandatory 3–5 `stem_variants`.
  - Documents modular per-competency override via `work/shards/shard_fixes/<CID>.py`.

## 3. Implementation Steps & Write Boundaries
- Strictly adhere to write boundaries:
  - Edit `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/plan_shards.py`
  - Create `d:/Augusto/personal_portfolio/Tops_academy/tests/test_weighted_sharding_m7.py`
  - Maintain `<teamwork_dir>/{BRIEFING.md,progress.md,handoff.md}`
- Run targeted pytest test suite using project `.venv`.
- Escalate via `BLOCKER::` if any conflict emerges (no blockers found).
