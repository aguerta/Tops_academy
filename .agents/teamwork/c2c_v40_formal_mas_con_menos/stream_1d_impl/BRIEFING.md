# Pre-Flight Sanity Check & Briefing — Stream 1D (Fase A: Implementador Ortogonal)

- **Agent:** `c2c40_implementer`
- **Stream:** 1D (Dispatch, Sharding, Load Inversion, Form-C Prompts & Clean-Room Architecture)
- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`

---

## 1. Exclusive Write Boundary (`∩ = ∅`)

Files strictly within scope:
1. `.agents/skills/content-to-course/plan_shards.py`
2. `.agents/skills/content-to-course/dispatch.py`
3. `.agents/skills/content-to-course/subagent_types.json`
4. `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
5. `.agents/skills/content-to-course/system_prompts/prompt_cta_architect.md`
6. `.agents/skills/content-to-course/system_prompts/prompt_repair.md`
7. `.agents/skills/content-to-course/system_prompts/prompt_blind_judge.md`
8. `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
9. `.agents/skills/content-to-course/system_prompts/lean/prompt_cta_architect.md`
10. `.agents/skills/content-to-course/system_prompts/lean/prompt_repair.md`
11. `.agents/skills/content-to-course/system_prompts/lean/prompt_blind_judge.md`
12. `tests/test_dispatch_turn0_and_milestone3_prompts.py`
13. `tests/test_c2c_v321_comp4_prompts.py`
14. `tests/test_c2c_v321_comp3_dispatch.py`
15. `tests/test_weighted_sharding_m7.py`
16. `tests/test_skill_v3.py`
17. `tests/test_orchestration_resilience.py`
18. `.agents/teamwork/c2c_v40_formal_mas_con_menos/stream_1d_impl/BRIEFING.md`
19. `.agents/teamwork/c2c_v40_formal_mas_con_menos/stream_1d_impl/handoff.md`

All other files are strictly read-only or out of bounds.

---

## 2. Invariants, Targets & Exact Line Ranges

### A. `plan_shards.py`
- **Line 65 (`DSL_REFERENCE`):**
  - Update `min_archetypes: 4` (referencing `MIN_ARCHETYPES` from `engine.stage_contract` with fallback 4).
  - Update descriptions and rule notes from 3 archetypes to **4 orthogonal archetypes** (`direct`, `inverse`, `perturbation`, `boundary_or_edge_case`).
- **Lines 491-582 (`partition_competencies_weighted`):**
  - Ensure weighted cognitive sharding enforces at most 1 Skill (`Hab-*`) per shard, at most 2 for Concept/Misconception (with 3-Fact exception only if all 3 are fact and total $N \ge 30$).
- **Lines 747-789 (`plan_shards` manifest & shard slices):**
  - Include `"assumptions"` in each competency dictionary in `pre_shard_manifest.json` and shard JSON files, ensuring Turn-0 authors know assumptions to break in Archetype 4.

### B. `dispatch.py`
- **Deduplication of payload (`L689, 831, 984, 1359, 1643, 2373`):**
  - Replace huge redundant `prompt_full` string inside `"work_order"` with compact structured metadata + `"prompt_sha256"`.
  - For judges (`L1643`), avoid triplicating the full `items` array inside `"work_order"` (retain scalar keys required by tests like `role`, `shard_id`, `compile_cmd`, `min_archetypes`, `batch_id`, `items_count`, `item_ids`).
- **Fix `author_snapshot.json` and `_is_allowed_path` (`L1384-1400, 1707, 2409, 2496`):**
  - In `dispatch_authors`, persist `work/dispatch/author_snapshot.json` using `snapshot_work_dir(work)` prior to returning.
  - In `_is_allowed_path`, allow nested `/__pycache__/` paths in any subpath of `work/`, `*.cert.json` files, and `cta_fixes/*.py`.
- **Competence Slicing `< 2 KB` in `dispatch_repair` (`L318, 2267`):**
  - Remove `work/cta.json` and `pre_shard_manifest.json` from `ROLE_SPECS["repair"]["read"]` and from `read_paths` in `dispatch_repair`.
  - Extract compact Competence Slice (`< 2 KB`: `id`, `title`, `description`, `assumptions`, 6 `distractors` + exact diagnostics + line range of `shard_XX_data.py`), persist in `work/dispatch/repair_slices/<shard_id>_<cid>.json`, add to `read_paths`, and inject 2D matrix repair instructions into the repair prompt.
- **Stamping `min_archetypes = 4` and `--lean` Default (`L1120, 1306, 1331, 2263, 2604`):**
  - Stamp `min_archetypes = 4` across all compiler commands and manifests.
  - In `define-types` CLI and type generation, make `lean=True` the default, with `--full-prompts` / `lean=False` flag to opt out.
  - Generate `subagent_types.json` with `lean=True` and strict Unix LF (`\n`).

### C. System Prompts & Lean Prompts
- **`system_prompts/lean/prompt_shard_author.md` (`<= 4,750` bytes strict, LF only):**
  - Replace broken `H-01` example with canonical Form-C clean Carnot cycle (`Hab-01` with explicit assumption `A-Hab01-01` $\sigma_{\text{irr}} = 0$):
    1. `direct` (`MC7`, `("easy", "Apply")`, $\eta = 1 - T_C/T_H$),
    2. `inverse` (`FIB`, `("medium", "Apply")`, $T_H = T_C / (1 - \eta)$ naked FIB),
    3. `perturbation` (`FIB`, `("hard", "Analyze")`, $T_C' = T_C/2$),
    4. `boundary_or_edge_case` (`MS`, `("hard", "Evaluate")`, assumption break $\sigma_{\text{irr}} > 0$).
  - Include unified `RATS` dictionary, 16 stems via $(2 \times 2)$, 3 Socratic hints, genuine analytical verifiers `ver_*` refuting distractors.
  - Ensure mandatory keywords for external tests: `## 0. SCOPE-LOCK`, `DONE:`, `compile_shard.py`, `Física`, `Sistemas Distribuidos`, `línea`, `stem_variants`, `ArtifactMetadata`.
  - Total size must satisfy `len(path.read_bytes()) <= 4750`.
- **`system_prompts/prompt_shard_author.md`:**
  - Remove obsolete Form-A (L72-196), document Form-C and Form-B with `min_archetypes = 4`, `assumptions`, real verifiers.
- **`prompt_cta_architect.md` & `lean/prompt_cta_architect.md`:**
  - Document 7-tuple with `assumptions: [(id, statement_latex, violation_consequence)]` and `CTA_CONTRACT_VERSION = 2`.
- **`prompt_repair.md` & `lean/prompt_repair.md`:**
  - Align with 2D Matrix (`edit_file` vs `ModularSplicing`) + Competence Slice (forbidden to read `cta.json`).
- **`prompt_blind_judge.md` & `lean/prompt_blind_judge.md`:**
  - Align with epistemic sufficiency and semantic no-giveaway validation.

### D. 6 Assigned Test Suites
- Update tests verifying `min_archetypes == 3` to `min_archetypes == 4`.
- Validate deduplication of `work_order`, persistence of `author_snapshot.json`, absence of `cta.json` in repair `read_paths`, `--lean` default, LF line endings, and `<= 4,750 B` byte budget.

---

## 3. Zero-Domain Guardrails
- In all `.py` files inside `.agents/skills/content-to-course/`, forbidden lowercase substrings:
  `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`.
- Write all Python comments and docstrings in English to prevent accidental Spanish substrings.
