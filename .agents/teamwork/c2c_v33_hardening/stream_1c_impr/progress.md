# PROGRESS: Stream 1C — Hardening & Quality Verification (Improver)

## Status: COMPLETED
All pre-flight checks, hardening items, edge cases, and adversarial unit tests have been implemented and validated against the entire relevant pytest suite.

### Detailed Actions Taken:
1. **Pre-Flight Scrutiny:**
   - Evaluated Implementer's delivery (`stream_1c_impl/handoff.md`).
   - Inspected downstream consumers (`run.py`, `dispatch.py`, `compile_shard.py`) in read-only mode to verify complete dictionary schema compatibility.
   - Recorded pre-flight audit in `BRIEFING.md`.

2. **Code Hardening in `plan_shards.py`:**
   - **Competency Type & ID Disambiguation:**
     - Expanded `is_skill_competency` to recognize uppercase/lowercase (`SKILL`, `habilidad`, `habilidades`, `skills`, `hab`), concatenated digits (`HAB04`), and underscore formats (`HAB_01`, `SKILL_01`).
     - Added strict guard in `is_fact_competency` and `is_concept_competency` (`if is_skill_competency(comp): return False`) to prevent any possibility of a skill being misclassified as a concept or fact.
     - Added support for Spanish and underscore identifiers (`hecho`, `hechos`, `H_01`, `concepto`, `conceptos`, `C_01`).
   - **Weight Calculation Defensive Handling:**
     - Guarded `comp.get("distractors")` in `calculate_competency_weight` to gracefully handle `None`, dicts, or missing keys without raising exceptions.
   - **Case 2A / Parametric Sizing Flexibility:**
     - Updated `partition_competencies_weighted` to support `max_comps=3` (Case 2A) dynamically while maintaining strict 1-skill isolation.
     - Preserved Case 2B 3-fact grouping exception when $N \ge 30$ and remaining facts avoid leaving awkward remainder of 1.
   - **CTA Data Parsing Robustness:**
     - Handled `cta.json` structures with competencies declared as a dictionary mapping (`{CID: {comp_data}}`) or a list.
   - **Wave Sizing Defensive Guard:**
     - Guarded against `max_wave_size <= 0` or `None` by falling back to `DEFAULT_MAX_WAVE_SIZE = 10`, eliminating any risk of `ZeroDivisionError`.
   - **Windows Atomic Write Safety:**
     - Enforced `try...finally` in `_atomic_write_json` to guarantee temporary files are unlinked even in lock failure scenarios on Windows.
   - **DSL_REFERENCE Clarity:**
     - Added `@b:fmt@` example into `orthogonal_tokens_raw_strings` rule.

3. **Test Suite Expansion in `tests/test_weighted_sharding_m7.py`:**
   - Expanded from 13 tests to 27 tests (+14 new adversarial test cases).
   - Added:
     - `TestAdversarialInputsAndGracefulFailures`: empty competencies error, missing competencies key, dict-based CTA formats, missing cta file, missing `pre_cta_manifest.json` blocker error.
     - `TestTypeAndIdDisambiguation`: multilingual skill isolation, Spanish/underscore detection, `None` distractor handling.
     - `TestWaveSizingAndLimits`: `max_wave_size=1`, `max_wave_size<=0` fallback, waves summary verification.
     - `TestConsecutiveSkillsAndTieBreaking`: consecutive skills isolation (`Hab-01`, `Hab-02`, `Hab-03`), deterministic tie-breaking.
     - `TestCase2AParametricOverride`: Case 2A (`max_comps=3`) grouping.
     - `TestCliMainInvocation`: `main()` CLI execution testing `--max-wave-size` and stdout formatting.

4. **Pytest Verification Results:**
   - Targeted: `tests/test_weighted_sharding_m7.py` -> 27 passed in 0.78s.
   - Full related suite: 60 passed, 2 skipped in 5.46s.
