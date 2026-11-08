# HANDOFF — Stream 1C (Fase A: Implementador Ortogonal)

## 1. Executive Summary & Status
- **Stream:** Stream 1C — Engine Sandbox & Invariant Hardening, Template Validation Parity, 4-Archetype Canonical Examples.
- **Status:** COMPLETE & REMEDIATED — 100% SUCCESS.
- **Pytest Suite Results:** **218 passed, 0 failed** across all 9 assigned suites in `18.39s`.
- **Zero-Domain Compliance:** Exactly 0 occurrences of forbidden domain substrings (`edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`) in all modified `.py` files inside `.agents/skills/content-to-course/`.
- **Windows `cp1252` Console Safety:** Cleaned `\u0332` -> `^` on `pykatex.ParseError`, 0 encoding crashes.

---

## 2. Remediations Applied (Auditor Review Feedback)

1. **`examples/edo/templates/C-02.json:117` (`T-C02-04`) & 50-Seed Validation:**
   - Expanded parameter range `w = rng.randint(2, 16)` (15 distinct values) in `T-C02-04`.
   - Verified that `check_templates.py --cta examples/edo/cta.json examples/edo/templates/` and `examples/edp/templates/` pass cleanly with canonical 50 seeds dry run (`num_dry_run_seeds=50, strict=True`).
   - Cleaned all stale `.ok.pkl` and `.validation_cache` files in `examples/edo/.validation_cache/` and `examples/edp/.validation_cache/`.

2. **`check_templates.py:L2776-L2795` (Competency Classification Parity):**
   - Corrected `is_skill_or_hab` determination so that `Concept` and `Misconception` competencies (`C-`, `M-`) are NEVER reclassified as `Skill` based merely on Bloom level (`"Apply"`, `"Analyze"`, `"Evaluate"`, `"Create"`). Archetype 4 (`boundary_or_edge_case`) of a Concept legitimately uses Bloom `Evaluate` while remaining a Concept.
   - Enforces `min_req = min(10, max(5, N_eval // 2))` (10 at 50 seeds) strictly for Skills (`Hab-`, `H-`, `is_skill_type`), and `min_req = min(5, N_eval)` (5 at 50 seeds) for parametric Concepts/Misconceptions (`has_dynamic_vars`).

3. **`tests/test_template_variability.py:L727-L744`:**
   - Updated `test_examples_templates_strict_validation` to run with the full canonical **`num_dry_run_seeds=50`** (unmasked) for both `edo` and `edp`. Both pass with 0 errors in strict mode.

---

## 3. Exact Changes by Exclusive Write Boundary Item

### Core Engine & Validation

1. **`engine/sandbox.py`**
   - **`np.bool_` & Strict Truthiness Hardening:** Unwraps scalar types via `item()` and strictly enforces `if cc_res is not True: raise SandboxExecutionError(...)` in both `execute_sandbox_instance` (L542) and `execute_sandbox_batch` (L671), preventing falsy bypasses (`False`, `np.bool_(False)`, `None`, `0`).
   - **Flexible Verifier Signature Inspection:** Dispatches verifiers according to parameter count and names: `(rng, result)` when first argument is `rng`, `(cand, v)` where `cand = result.get('correct')` and `v = result.get('vars', {})` for 2-arg non-rng functions, and `(result,)` for single-argument verifiers.
   - **Deterministic Sub-seed Derivation & Public Helper:** Added deterministic sub-seed generator `(seed * 1009 + k) & 0x7FFFFFFF` and public helper `instantiate_verified_seed`.

2. **`engine/instantiate.py`**
   - **Deterministic Sub-seed Rejection Sampling:** Integrated sub-seed retry loop with `MAX_SUBSEED_ATTEMPTS = 8` to resolve incidental numerical collisions in distractors or between correct answers and distractors.
   - **Anti-Cloning Guard:** Triggers strict `TPL-D4` collision error if all 8 sub-seed attempts fail on a seed, or if more than 20% of seeds in a batch require retries (detecting algebraically identical distractor definitions).

3. **`engine/invariants.py`**
   - **`pykatex` LRU-Cached Integration:** Render verification using `pykatex.renderToString` with `@functools.lru_cache(maxsize=8192)` (< 1 ms overhead) and sanitization of `\u0332` -> `^` on `ParseError`.
   - **`KaTeXAST` Inductive Invariants:**
     - Enforces prose limit `<= 45` characters in `\text{...}`, `\textrm{...}`, `\mathrm{...}` while allowing legitimate math subscripts like `$x_i$` inside text blocks.
     - Forbids double curly braces `{{...}}`.
     - Forbids vacuous quantifiers (`\forall x = 3`, `\exists y = -2`).
     - Forbids Newtonian dots on digits (`\dot{2}`).

4. **`engine/assemble.py`**
   - **Algebraic Double-Sign Canonicalization:** Safely collapses interpolation double signs (`+ -5` -> `- 5`, `- -5` -> `+ 5`, `+ +5` -> `+ 5`, `- +5` -> `- 5`) inside math spans (`$...$` and `$$...$$`) without modifying LaTeX macros or matrix structures.

5. **`check_templates.py`**
   - **Strict Distractor Refutation (`TPL-CROSS`):** Implemented `check_distractor_refutation` validating that substituting each distractor into `correct` fails `cross_check_py` / `verifier_code`.
   - **Shift-Left Parity:**
     - Removed `passes_calibrated` bypass; strictly enforces `div_ratio >= MIN_DIVERSITY_RATIO` (0.50).
     - Full skill detection via `is_skill_type(ctype) or cid.startswith("Hab-")`.
     - Retains `R-16` when `len(questions) >= 10`.
     - Enforces dynamic variability (`>= 10` for Skills, `>= 5` for Concept/MS with dynamic vars).
   - **Cold Cache Optimization:** Writes cache `.ok.pkl` even when `shard_py is not None`.
   - **Compact Diagnostic Reporting:** Aggregated error reporting grouping repeated seed failures into `(rule_id, template_id, norm_msg)` with `affected_seeds_count` and `sample_seed` (< 1.5 KB vs 82 KB).

6. **`schemas/template.schema.json`**
   - Extended schema with optional fields: `"archetype"` (`enum`: `["direct", "inverse", "perturbation", "boundary_or_edge_case"]`), `"assumption_tested_id"`, and `"contract_version"`.

---

### Canonical Examples (4 Orthogonal Archetypes)

7. **`examples/edo/cta.json` & `examples/edp/cta.json`**
   - Added explicit `"assumptions"` blocks for each competency (`A-C02-01`, `A-C02-02`, `A-Hab02-01`, `A-Hab02-02` for EDO; `A-C01-01`, `A-C01-02`, `A-Hab01-01`, `A-Hab01-02` for EDP).

8. **`examples/edo/templates/C-02.json`**
   - 4 archetypes: `T-C02-01` (`direct`), `T-C02-02` (`inverse`), `T-C02-03` (`perturbation`), `T-C02-04` (`boundary_or_edge_case`).
   - `w = rng.randint(2, 16)` generating $\ge 10$ unique correct answers across 50 seeds.
   - Calibrated distractor lengths for R-15 and R-16 compliance (longest ratio 0.0% <= 25.0%).

9. **`examples/edo/templates/Hab-02.json`**
   - 4 archetypes: `T-Hab02-01` (`direct`), `T-Hab02-02` (`inverse`), `T-Hab02-03` (`perturbation`), `T-Hab02-04` (`boundary_or_edge_case`).
   - Full distractor refutation and dynamic rationales.

10. **`examples/edp/templates/C-01.json`**
    - 4 archetypes: `T-C01-01` (`direct`), `T-C01-02` (`inverse`), `T-C01-03` (`perturbation`), `T-C01-04` (`boundary_or_edge_case`).
    - Dynamic parametrization in `T-C01-04` ensuring dynamic correct answers and distractor refutation.

11. **`examples/edp/templates/Hab-01.json`**
    - 4 archetypes: `T-Hab01-01` (`direct`), `T-Hab01-02` (`inverse`), `T-Hab01-03` (`perturbation`), `T-Hab01-04` (`boundary_or_edge_case`).
    - Explicit $x > 0, y > 0$, $a \ge 2$, balanced delimiters, PrairieLearn tokens `@a@` and `@b@`, refutation verifiers.

---

### Test Suites Verification

| Suite File | Tests | Result |
|---|---|---|
| `tests/test_sandbox_adversarial.py` | 14 | PASSED |
| `tests/test_sandbox_gil_and_circuit_breaker.py` | 6 | PASSED |
| `tests/test_engine_invariants_adversarial.py` | 60 | PASSED |
| `tests/test_assemble_katex_and_rationale.py` | 16 | PASSED |
| `tests/test_assemble_sanitize_katex_r23.py` | 28 | PASSED |
| `tests/test_katex_prairielearn_tokens.py` | 17 | PASSED |
| `tests/test_c2c_error_aggregation.py` | 63 | PASSED |
| `tests/test_template_variability.py` | 13 | PASSED |
| `tests/test_blind_guess_empirical.py` | 1 | PASSED |
| **Total** | **218** | **ALL PASSED (0 failures)** |

Execution command:
`& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_sandbox_adversarial.py tests/test_sandbox_gil_and_circuit_breaker.py tests/test_engine_invariants_adversarial.py tests/test_assemble_katex_and_rationale.py tests/test_assemble_sanitize_katex_r23.py tests/test_katex_prairielearn_tokens.py tests/test_c2c_error_aggregation.py tests/test_template_variability.py tests/test_blind_guess_empirical.py -q`
Result: `218 passed in 18.39s`

---

## 4. Verification & Compliance Sign-Off
- **Exclusive Write Boundary:** Enforced 100%. No outside files touched.
- **Zero-Domain Invariant:** Verified 0 occurrences of forbidden words across all 5 `.py` files.
- **Production-Grade Standard:** Remediated according to auditor specifications, ready for Auditor pass.
