# BRIEFING: Stream 1C — Hardening & Architectural Scrutiny (Improver)

## 1. Implementer Review & Pre-Flight Assessment
The Implementer (`stream_1c_impl`) implemented the core Milestone 7.4 Weighted Cognitive Sharding, 1-Skill Anti-Straggler SLA, and Wave Dispatch mechanisms in `plan_shards.py` and provided unit tests in `tests/test_weighted_sharding_m7.py`.

### Strengths Identified:
- Strict 1-Skill isolation rule implemented in `partition_competencies_weighted`.
- Heaviest-first sorting prioritizes all Skill shards at the front of Wave 1 ($t = 0$).
- Wave indexing assigns sequential `wave_index` (`1, 2, ...`) with `total_waves` and `waves` summary in `pre_shard_manifest.json`.
- Backward compatibility preserved for explicit `k` or `--no-isolate-skills`.
- Existing test suites pass (`46 passed, 2 skipped`).

### Gaps & Edge Cases Identified for Hardening:
1. **Type & ID Normalization Robustness:**
   - `is_skill_competency`, `is_fact_competency`, `is_concept_competency` only partially handled Spanish terms and underscore delimiters (`HAB_01`, `SKILL_01`, `habilidades`, `hechos`).
   - Disambiguation: Fact/Concept check did not explicitly guard against potential skill overlaps.
2. **Defensive Weight Computation:**
   - `calculate_competency_weight` assumed `comp.get("distractors")` is always a list; if `None` or absent, could cause unhandled exceptions.
3. **Partitioning Parameter Respect (`max_comps`):**
   - `partition_competencies_weighted` hardcoded chunk size `min(2, remaining)`, ignoring `max_comps=3` when reverting or running Case 2A.
4. **CTA Format Flexibility:**
   - `plan_shards` assumed `cta_data.get("competencies")` is always a list, whereas CTA formats can sometimes supply competencies as a dict keyed by CID.
5. **ZeroDivision / Invalid Wave Size Guard:**
   - `max_wave_size <= 0` or `None` could lead to `ZeroDivisionError` in `math.ceil` or `idx // max_wave_size`.
6. **Windows Atomic Write Cleanup:**
   - `_atomic_write_json` should enforce `try...finally` cleanup of temporary files to eliminate lingering `.tmp` files under Windows process locking.
7. **Adversarial Test Suite Coverage:**
   - Need comprehensive tests for empty curriculum error diagnostics, consecutive skill isolation, case/language insensitivity, dict-based CTA formats, wave size boundary conditions, and CLI flags.

## 2. Hardening Strategy & Write Boundaries
- File Boundaries:
  - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/plan_shards.py`
  - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_weighted_sharding_m7.py`
  - `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1c_impr/*`
- All other files remain strictly READ-ONLY.
- Architectural Blocker Check: No blockers found. All adjustments fit cleanly within allowed boundaries.
