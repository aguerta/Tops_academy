# BRIEFING — Stream 1E: Inter-Stage Schemas, Neuro-Symbolic Judge Dominance, and Course Publisher Hardening

**Stream:** Stream 1E (Fase A: Implementador Ortogonal)  
**Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`  
**Engineer:** `c2c40_implementer` (Senior Formal Verification & Systems Engineer)  
**Date:** 2026-11-08  

---

## 1. Scope & Exclusive Write Boundary

We have exclusive write permissions ONLY for:
1. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\engine\interstage_schemas.py` `[NEW]`
2. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\judge.py`
3. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\content-to-course\course_publisher.py`
4. `d:\Augusto\personal_portfolio\Tops_academy\.agents\skills\course-qa-evaluator\scripts\standardized_audit_engine.py`
5. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_new_audit_linters.py`
6. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_validator_prescriptive.py`
7. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_dispatch_scope.py`
8. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_pipeline_optimizations.py`
9. `d:\Augusto\personal_portfolio\Tops_academy\tests\test_c2c_straggler_and_postproduction_prevention.py`
10. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1e_impl\BRIEFING.md` `[NEW]`
11. `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1e_impl\handoff.md` `[NEW]`

All other files are strictly read-only (`∩ = ∅`).

---

## 2. Invariants & Guardrails

1. **Zero-Domain Invariant (`test_skill.py:test_engine_zero_domain_logic`):**
   - For all `.py` files inside `.agents/skills/content-to-course/` (`interstage_schemas.py`, `judge.py`, `course_publisher.py`):
     Strictly forbidden lowercase substrings:
     `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`.
   - All comments, docstrings, variable names, and string literals MUST be in English to prevent Spanish words containing forbidden substrings (e.g. `metodo` contains `edo`, `quedo` contains `edo`, `regresion` contains `regresi`).
2. **Windows cp1252 Safe Console Output:**
   - No raw Unicode math characters or combining accents (`\u0332`) output without safe replacement.
3. **Backward Compatibility:**
   - Legacy courses (`solow_growth_model`, `gavilano_pre_parcial`, `asymptotic_statistics_v7`, `saul_control_optimo`) in `courses/*.json` must remain evaluated with `req_arch = 3`, maintaining their scores without regression.
4. **Focused Single-Process Pytest:**
   - Execute tests using `& ".venv\Scripts\python.exe" -m pytest -o addopts="" ... -q`.

---

## 3. Component Analysis & Line Ranges

### Component 1: `engine/interstage_schemas.py` `[NEW]`
- Pydantic v2 schemas for all inter-stage contracts:
  - `ArtifactCertificate`:
    - `schema_version: int = 1`
    - `stage: str`
    - `artifact_id: str`
    - `source_sha256: str`
    - `cta_sha256: str = ""`
    - `compiler_sha256: str = ""`
    - `contract_version: int = 2`
    - `template_shas: Dict[str, str] = Field(default_factory=dict)`
    - `passed_50_seeds: bool = True`
    - `created_at: str = Field(default_factory=...)`
    - Helper functions: `write_certificate(cert_path, ...) -> Path`, `verify_certificate(cert_path, expected_source_bytes=None, ...) -> bool` with SHA-256 tamper detection.
  - `CompileAttemptRecord`:
    - `attempt: int`
    - `passed: bool`
    - `error_count: int`
    - `affected_line_count: int`
    - `has_syntax_error: bool`
    - `error_sha256: str`
    - `errors: List[str]`
  - `RejectionSpec`:
    - Normalizes `status` to `"REJECTED"` (tolerating `"rejected"`, `"fail"`, `"failed"`, etc. on input).
    - Synchronizes dual keys:
      - `failing_shards` <-> `affected_shards` (both present, sorted, deduplicated).
      - `grouped_by_rule` <-> `groups` (both present).
      - `diagnostics_by_competency` (present).
    - Serialization helper `to_dict()` and `write_json(path)` ensuring keys never drift for `run.py`, `c2c_hook_guard.py`, and `dispatch.py`.

### Component 2: `judge.py`
- Line ranges: `~L280-L360` (seed sampling logic), `~L380-L420` (item assembly & pre-verification), `~L1200-L1350` (verdict resolution & comparison).
- **Pre-Judge Strict Verification:**
  - When selecting seeds for each template in `generate_judge_batch`:
    Evaluate candidate seeds against:
    1. Template verifier / cross-check code (`execute_sandbox_instance` with `verifier_code` / `cross_check_py`).
    2. Invariant verification via `check_instance_invariants` (no KaTeX errors, no `TPL-D4` collisions, no missing rationales).
  - Deterministically iterate candidates if a seed collides or fails invariants.
  - If no seed passes among retry limit (e.g. 10 seeds), mark template as `kernel_refuted = True` immediately, logging deterministic refutation without spending LLM tokens.
- **Canonical 1-Seed Default:**
  - Add `samples_per_template: Optional[int] = None` and `num_samples: Optional[int] = None` to `generate_judge_batch`.
  - When template has non-empty verifier code and no explicit seed count is requested, default to `samples_per_template = 1`.
  - If template has no verifier code or caller explicitly passes `samples_per_template=3` or `seeds=(...)`, honor that value (preserving 100% compatibility with existing test `test_judge_sampling_three_seeds_full_template_coverage`).
- **Neuro-Symbolic Kernel Dominance ($\alpha_{\text{Kernel}} = 0$):**
  - Implement `resolve_neuro_symbolic_verdict(...)`:
    - If `kernel_refuted == True`: final verdict is unconditionally `FAIL` even if LLM judges vote `PASS`.
    - If `kernel_verified == True` and LLM judge emits `FAIL` citing only calculation/math error (`math_error`, `calculation_error` without alleging `epistemic_insufficiency`, `missing_definition`, `ambiguous_stem`, or `giveaway`): set `kernel_override = True`, logging algebraic proof superiority.
    - If LLM judge notes epistemic insufficiency, ambiguity, or giveaway: mark `FAIL` (human or prompt correction required).
  - When judge stage passes, emit `work/judge.cert.json` using `ArtifactCertificate`.

### Component 3: `course_publisher.py`
- Line ranges: `~L510-L760` (`build_specific_error_report`), `~L1130-L1170` (quality gate handling), `~L1200-L1285` (`publish` success serialization).
- **Rejection Spec Persistence:**
  - In `build_specific_error_report` and gate rejection:
    Construct and write `publish_rejection_spec.json` (as well as `specific_error_report.json`) using `RejectionSpec`.
    Ensure `status = "REJECTED"`, with bidirectional synchronization of `failing_shards` + `affected_shards`, `grouped_by_rule` + `groups`, and `diagnostics_by_competency`.
- **Course Metadata Stamping & Publish Certificate:**
  - Stamp `"contract_version": 2` and `"min_archetypes": 4` in published course data (at root and within `metadata` dict if present). Read `MIN_ARCHETYPES` from `engine.stage_contract` (or default to 4 if >= 4).
  - On successful publish, emit `work/publish.cert.json` using `ArtifactCertificate`.

### Component 4: `standardized_audit_engine.py`
- Line ranges: `~L674-L760` (`ArchetypeEntropyLinter`).
- Dynamically determine `req_arch`:
  - Check `course_data.get("contract_version")` or `metadata.get("contract_version")`.
  - If `contract_version >= 2` or `min_archetypes` is explicitly provided, use `int(min_archetypes)` (defaulting to 4 for `contract_version >= 2`).
  - For legacy courses without `contract_version >= 2`, keep `req_arch = 3`.
  - Ensures historical courses in `courses/*.json` retain `>= 19.0/20` while new v4.0 courses require 4 archetypes.

---

## 4. Edge Cases & Risk Mitigations

1. **Pydantic v2 Compatibility:**
   - Use standard Pydantic v2 `BaseModel`, `Field`, `model_dump()`, and `model_validate()`. Provide fallback `dict()` / tolerant parsing if running across environments.
2. **Zero-Domain Check in English:**
   - In all code and comments in `interstage_schemas.py`, `judge.py`, and `course_publisher.py`, strictly avoid forbidden strings: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`.
   - Never write words like `metodo`, `quedo`, `puedo`, `regresion`.
3. **Preservation of Existing Test Behaviors:**
   - In `test_pipeline_optimizations.py`, `test_judge_sampling_three_seeds_full_template_coverage` tests unverified templates expecting 12 items (4 * 3 seeds). That must continue to pass because those templates do not have `verifier_code`!
4. **Certificate Tampering Detection:**
   - `verify_certificate` verifies source SHA-256 against actual file bytes, detecting tampering.

---

## 5. Execution Plan

1. Create `engine/interstage_schemas.py` with `ArtifactCertificate`, `CompileAttemptRecord`, and `RejectionSpec`.
2. Enhance `judge.py` with seed pre-verification, canonical 1-seed default for verified templates, `resolve_neuro_symbolic_verdict`, and certificate emission.
3. Update `course_publisher.py` to use `RejectionSpec`, stamp `contract_version: 2` and `min_archetypes: 4`, and emit `publish.cert.json`.
4. Update `standardized_audit_engine.py` (`ArchetypeEntropyLinter`) with dynamic `req_arch`.
5. Add unit and adversarial tests across the 5 test suites.
6. Run single-process pytest on all 5 suites and run `test_engine_zero_domain_logic` from `test_skill.py`.
7. Write `handoff.md` and send completion message.
