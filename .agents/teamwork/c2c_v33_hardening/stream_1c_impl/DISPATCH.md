# DISPATCH: Stream 1C — Implementer (`impl_1c`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1c_impl`
- **Role:** `Phase 1 Implementador — Stream 1C (Sharding Ponderado M7.4 y Oleadas en plan_shards.py)`

## 1. Strict Write Boundaries (ONLY touch these files + your Teamwork Directory)
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/plan_shards.py`
- `d:/Augusto/personal_portfolio/Tops_academy/tests/test_weighted_sharding_m7.py` *(new)*
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1c_impl/{BRIEFING.md,progress.md,handoff.md}`

*(Forbidden: Do NOT edit `run.py`, `dispatch.py`, `compile_shard.py`, or any other file outside the list above!)*

## 2. Technical Specifications
1. **Step 0 Pre-Flight Sanity Check:**
   - Read `plan_shards.py` and grep for all callers/tests importing `plan_shards` (`run.py`, `tests/*`) so you preserve backward compatibility when explicit `k` or `max_comps` arguments are passed by legacy tests! Record findings in `BRIEFING.md`. Escalate via `BLOCKER::` if any hard conflict blocks your order.
2. **Weighted Cognitive Sharding (`1 Hab/shard` Anti-Straggler Rule — Milestone 7.4):**
   - In `ab30cf91`, `plan_shards.py` paired `Hab-03 + Hab-04` into `shard_06` (8 algebraic templates = 34.1 min straggler) and `Hab-08 + Hab-09` into `shard_14` (17 min).
   - Refactor default sharding in `plan_shards.py` (when legacy explicit `k` is `None`):
     - **Hard Skill Isolation Rule:** Every competency with `type == "skill"` (or ID prefix `Hab-`) MUST be placed in **its own exclusive 1-competency shard** (`max 1 skill per shard`, never grouped with another `skill`, `concept`, or `fact`).
     - **Contiguous Concept/Fact Grouping:** Adjacent `concept` (`C-*`) and `fact` (`H-*`) competencies (in document/curriculum order, between skills or grouped cleanly while preserving pedagogical locality) are packed with max **2 competencies per shard** (allowing up to **3 competencies** in a shard ONLY when all 3 are `fact` and total competencies `N >= 30`).
   - Preserve explicit override behavior if a caller passes an explicit integer `k` (or add `isolate_skills: bool = True` defaulting to `True` when `k is None`, while keeping existing unit tests 100% green—check existing `tests/test_*shard*.py` in Pre-Flight!).
3. **`Heaviest-First` Ordering & Wave Indexing (`wave_index`):**
   - Compute deterministic `weight` / `estimated_weight` per shard: `Skill = 6.0`, `Concept = 2.5`, `Fact = 1.5`, plus `+ 0.1 * len(distractors)` per competency.
   - Sort dispatched shards **descending by `weight`** (breaking ties deterministically by original curriculum order) so all `Skill` (`Hab-*`) shards sit at the very front of Wave 1 (`t = 0`), OR assign `shard_id` sequentially after sorting (verify what `dispatch.py` and existing tests expect for `shard_01..shard_NN` ordering!).
   - Assign `wave_index` (`1, 2, ...`) to every shard entry in `shards` and `pre_shard_manifest.json` using `max_wave_size: int = 10` (configurable via CLI `--max-wave-size` and parameter `max_wave_size=10`), and include top-level `"total_waves"` and `"waves"` summary in `pre_shard_manifest.json`.
4. **Update Embedded `DSL_REFERENCE` in `plan_shards.py`:**
   - Update `DSL_REFERENCE` so shard bundles/manifests teach `@var@` / `@var:fmt@` tokens in raw strings `r"..."` (forbidding `rf"..."`), mandatory 3–5 `stem_variants` list, and modular per-competency override support via `work/shards/shard_fixes/<CID>.py`.

## 3. Required Tests & Verification
- Create `tests/test_weighted_sharding_m7.py` testing:
  - Exact 32-competency distribution of `ab30cf91` (`6 Fact`, `16 Concept`, `10 Skill` in mixed curriculum order) -> verifies all 10 `Hab-*` shards have `competency_count == 1`, all `Hab-*` are assigned to Wave 1 (`wave_index == 1`), `Concept`/`Fact` shards have `<= 2` competencies, and 100% of 32 competencies are accounted for without duplicates or drops.
  - Edge cases: 1 competency, all-Skill course, large 45-competency course (`total_waves >= 2` with `max_wave_size=10`), and legacy `k` parameter compatibility.
- Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_weighted_sharding_m7.py -q` plus all existing shard planning tests!
