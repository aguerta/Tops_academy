# BRIEFING — Stream 2C (Implementador Ortogonal — Gate 2)

**Author:** `c2c40_implementer`  
**Date:** 2026-11-08  
**Scope:** Forensic Suites Alignment & Neuro-Symbolic Master Test Suite (`tests/test_c2c_v40_formal_certification.py`)

---

## 1. Executive Summary & Zero-Domain Verification

Stream 2C is tasked with formal certification and forensic test alignment under Gate 2:
1. Align legacy replay suites (`test_forensic_replay_ab30cf91.py`, `test_forensic_shard06_and_variance_v34.py`, `test_sweetspot_v35_cta_and_shards.py`) to the v4.0 contract (`CONTRACT_VERSION == 2`, `min_archetypes == 4`, strict non-tautological verifier distractor refutation).
2. Author `tests/test_c2c_v40_formal_certification.py` covering all 6 pillars in `< 4 s` total runtime:
   - Pillar 1: Eradication of `np.bool_(False)` falsifying `isinstance(..., bool)` / `== True` in `sandbox.py`.
   - Pillar 2: Triple Contract `ver_*` (`[VERIFIER-TAUTOLOGY-DETECTED]`, `[VERIFIER-SWALLOWED-EXCEPTION]`, `[TPL-DEBUG-ARTIFACT]`, `[TPL-AD-HOC-PERTURBATION]`).
   - Pillar 3: Form-C DSL (`<= 65` lines, `< 15 KB` output JSON, `shard_01.cert.json` emission, 4 archetypes).
   - Pillar 4: Symbolic verification `Z3` / `SymPy` catching `ans / 3` (`ast.Div` in `[DIAG-MAGIC-MULT]`) and collision detection.
   - Pillar 5: Property-Based Testing with `hypothesis` (`@given`): 2D Matrix in `c2c_hook_guard`, synchronous budget governance, `resolve_neuro_symbolic_verdict` in `judge.py`.
   - Pillar 6: Inter-stage parity with `RejectionSpec` releasing Rule B for failing shards only.

**Zero-Domain Guardrail Checklist:**
- All docstrings and comments are in English.
- Strictly forbidden tokens (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`) will NOT appear in any `.py` file.

---

## 2. Production Signatures & Exact Line Ranges Inspected

### 2.1 `engine/sandbox.py`
- Lines 605–608:
  ```python
  cc_res = call_with_timeout(ver_fn, args=ver_args, seed=seed, timeout=timeout)
  if hasattr(cc_res, "item") and callable(getattr(cc_res, "item", None)):
      cc_res = cc_res.item()
  if cc_res is not True:
      raise SandboxExecutionError(f"Cross-check verification failed (returned {cc_res!r}).")
  ```
- Lines 762–772:
  ```python
  if hasattr(cc_res, "item") and callable(getattr(cc_res, "item", None)):
      cc_res = cc_res.item()
  if cc_res is not True:
      results.append({"seed": s, "success": False, "ok": False, "error": f"Cross-check verification failed (returned {cc_res!r}).", "stage": "verify"})
  ```
- Invariant: When `cross_check` returns `np.bool_(False)`, `None`, or `0`, `cc_res is not True` evaluates to True:
  - In `execute_sandbox_instance`, it raises `SandboxExecutionError`.
  - In `execute_sandbox_batch`, it records `"success": False` with `"error": "...Cross-check verification failed..."`.
  - Conversely, `np.bool_(True)` and `True` convert to `True` via `.item()`, passing verification.

### 2.2 `compile_shard.py`
- Lines 1880–1909: AST inspection of verifier code:
  - `ast.Try` with handler returning `True`: emits `[VERIFIER-SWALLOWED-EXCEPTION]`.
  - `ast.Raise`: emits `[TPL-DEBUG-ARTIFACT]`.
  - `ast.Call` to `print()` / `breakpoint()` or import of `pdb`: emits `[TPL-DEBUG-ARTIFACT]`.
- Lines 1946–1956: AST inspection of generator code:
  - `ast.While` with ad-hoc float addition (`cand += 0.35`): emits `[TPL-AD-HOC-PERTURBATION]`.
- Lines 2353–2364: Distractor refutation dry-run:
  - Evaluates `run_ver(d_val, v_test, mutated)`. If `refute_res is True`, emits `[VERIFIER-TAUTOLOGY-DETECTED]`.
- Lines 2560–2585: Contract for 4 archetypes (`direct`, `inverse`, `perturbation`, `boundary_or_edge_case` linked to `assumption_id`).
- Lines 2950–3000: `[DIAG-MAGIC-MULT]` AST and ratio checks detecting multiplication/division over `ans`.
- Lines 3219–3233: `shard_XX.cert.json` emission with `schema_version: 1`, `stage: "shard"`, `contract_version: 2`.

### 2.3 `c2c_hook_guard.py`
- Lines 218–246: `decidir_estrategia_edicion`:
  - `has_syntax_error or existing_lines < 40` -> `"write_file"`
  - `error_count` between 1 and 5 and `affected_lines <= 5` -> `"edit_file"`
  - `error_count >= 6 or affected_lines > 5` -> `"modular_splicing"`
  - `existing_lines > 250` -> `"legacy_over_250"`
- Lines 579–601: Synchronous budget governance:
  - `turn_count > max_turns` (default 40) -> `deny`
  - `est_tokens > max_tokens` (default 5,000,000) -> `deny`
  - `error_streak >= max_streak` (default 3) -> `deny`
- Lines 795–820: Rule B post-PASS check:
  - Checks `.check_attempts/pass_<target_id>.json`.
  - If status is `PASS` and `_is_target_rejected(wd, "shard", target_id)` is False, denies edit tools.
  - If `publish_rejection_spec.json` marks the shard failing/rejected, `_is_target_rejected` returns True, unlocking editing ONLY for that failing shard.

### 2.4 `judge.py`
- Lines 1113–1208: `resolve_neuro_symbolic_verdict`:
  - If `kernel_refuted=True`: unconditionally `FAIL` (`passed=False`, `kernel_refuted=True`, `verdict="FAIL"`).
  - If `kernel_verified=True` and `llm_verdict` fails:
    - If `failure_category` is calculation error (`math_error`, `calculation_error`, etc.) without epistemic tokens: overrides to `PASS` (`kernel_override=True`).
    - If `failure_category` or reasons contain epistemic tokens (`epistemic_insufficiency`, `ambiguous_stem`, `giveaway`, etc.): returns `FAIL` (`kernel_override=False`).

### 2.5 `engine/interstage_schemas.py`
- Lines 127–226: `RejectionSpec`:
  - Validates and synchronizes `failing_shards` and `affected_shards`.
  - Normalizes `status` to uppercase `"REJECTED"`.
  - Synchronizes `grouped_by_rule` and `groups`.

---

## 3. Legacy Forensic Test Alignment Plan

1. **`tests/test_forensic_replay_ab30cf91.py`**:
   - `test_v9_tri_band_multimodal_contract_and_lean_prompt_budget`:
     - Update `min_archetypes: 3` to `min_archetypes: 4` in test manifest.
     - Add 4th archetype (`boundary_or_edge_case` or update archetypes) to the valid fixture so it compiles with 0 errors under `min_archetypes == 4`.
     - Update verifier to reject distractors (refutation contract).
2. **`tests/test_sweetspot_v35_cta_and_shards.py`**:
   - `test_dispatch_authors_stamps_min_archetypes_and_injected_in_compile_cmd`:
     - Update assertion from 3 to 4 (`self.assertEqual(manifest_on_disk.get("min_archetypes"), 4)` and `"--min-archetypes 4"`).
   - In single-tuple failure test and other fixtures, ensure valid fixtures have 4 archetypes and non-tautological verifiers.
3. **`tests/test_forensic_shard06_and_variance_v34.py`**:
   - Check all tests for any tautological verifiers (`def ver(inst): return True` or `return v["b"] > 0`) in test fixtures that fail under strict distractor refutation, and upgrade them to proper verification `cand == correct`.

---

## 4. `tests/test_c2c_v40_formal_certification.py` Architecture

- `TestPillar1NumpyBool`: Direct invocation of `execute_sandbox_instance` and `execute_sandbox_batch` with `np.bool_(False)`, `None`, `0`, `np.bool_(True)`, `True`.
- `TestPillar2TripleContract`: Calls `compile_shard` with tautology `v["a"] > 0`, swallowed exception `except: return True`, `raise RuntimeError("CAUGHT_5570")`, and while-loop perturbation `while cand in seen: cand += 0.35`.
- `TestPillar3FormCDSL`: In-memory compile of a complete Form-C shard with 4 archetypes (`direct`, `inverse`, `perturbation`, `boundary_or_edge_case` linked to `assumption_id="A-Hab-01-01"`), written in `<= 65` lines of Python, asserting compiled JSON `< 15 KB` and checking `shard_01.cert.json`.
- `TestPillar4SymbolicVerification`: Z3 and SymPy formal check catching `ans / 3` (`ast.Div`) and detecting algebraic collisions outside initial seeds.
- `TestPillar5PropertyBasedHypothesis`:
  - Property 1: `decidir_estrategia_edicion` with `@given`: when `affected_line_count > 5` and `has_syntax_error=False`, returns `"modular_splicing"` (never `"write_file"`).
  - Property 2: Synchronous budget governance with `@given`: `turn_count > 40`, `est_tokens > 5_000_000`, or `error_streak >= 3` always deny.
  - Property 3: `resolve_neuro_symbolic_verdict` with `@given`: $\alpha_{\text{Kernel}} = 0$, `kernel_refuted=True` never PASSes, `kernel_verified=True` overrides calculation error but respects epistemic insufficiency.
- `TestPillar6RejectionSpecParity`: Rejection spec with `failing_shards=["shard_01"]` releases Rule B only for `shard_01`, keeping `shard_02` (with `pass_shard_02.json`) blocked.

Runtime target: `< 4.0s` total.
