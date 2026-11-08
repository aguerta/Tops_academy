# PRE-FLIGHT BRIEFING — Stream 1C (Phase A: Orthogonal Implementer)

- **Agent:** `c2c40_implementer`
- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Dispatch Path:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1c_impl\DISPATCH.md`

---

## 1. Scope & Exclusive Write Boundary Verification

The write operations are strictly restricted to the 23 items assigned:
1. `engine/sandbox.py`
2. `engine/instantiate.py`
3. `engine/invariants.py`
4. `engine/assemble.py`
5. `check_templates.py`
6. `schemas/template.schema.json`
7. `examples/edo/cta.json`
8. `examples/edo/templates/C-02.json`
9. `examples/edo/templates/Hab-02.json`
10. `examples/edp/cta.json`
11. `examples/edp/templates/C-01.json`
12. `examples/edp/templates/Hab-01.json`
13. `tests/test_sandbox_adversarial.py`
14. `tests/test_sandbox_gil_and_circuit_breaker.py`
15. `tests/test_engine_invariants_adversarial.py`
16. `tests/test_assemble_katex_and_rationale.py`
17. `tests/test_assemble_sanitize_katex_r23.py`
18. `tests/test_katex_prairielearn_tokens.py`
19. `tests/test_c2c_error_aggregation.py`
20. `tests/test_template_variability.py`
21. `tests/test_blind_guess_empirical.py`
22. `stream_1c_impl/BRIEFING.md`
23. `stream_1c_impl/handoff.md`

All other files are strictly read-only (`∩ = ∅`).

---

## 2. Invariants & Zero-Domain Strict Guardrails

1. **Zero-Domain Invariant in `.py` Files (`test_skill.py`):**
   - For every `.py` file under `.agents/skills/content-to-course/`, the following lowercase substrings are strictly forbidden anywhere in code, strings, docstrings, or comments:
     `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`.
   - All code, comments, and docstrings in `.py` files will be written strictly in English to prevent substrings like `puedo`, `quedo`, `heredo`, `metodo`, or `regresion`.
2. **Windows cp1252 Console Safety:**
   - KaTeX errors originating from `pykatex.ParseError` contain combining low-line character `\u0332`. Whenever `pykatex.ParseError` is caught or converted to string, replace `\u0332` with `^` to prevent stdout encoding crashes.
3. **Execution Safety:**
   - Single-process test runner using `-o addopts=""` without CPU thrashing.

---

## 3. Detailed Technical Analysis & Target Line Ranges

### A. `engine/sandbox.py` (L535-L545, L660-L685)
- **Problem:**
  - `cc_res is False` check does not reject `np.bool_(False)` when checked with identity `is False`, nor does it reject non-booleans such as `None`, `0`, or truthy numbers.
  - Verifiers accepting flexible signatures `(rng, result)`, `(cand, v)`, or `(result,)` are not cleanly supported across in-process calls.
- **Resolution:**
  - Extract numpy/scalar item via `if hasattr(cc_res, "item") and callable(getattr(cc_res, "item", None)): cc_res = cc_res.item()`.
  - Enforce `if cc_res is not True:` raising `SandboxExecutionError(f"Cross-check verification failed (returned {cc_res!r}).")` in both `execute_template_code` (and `execute_verifier_code`) and `execute_sandbox_batch`.
  - Add flexible callable invocation helper: inspect function signature:
    - If 2 params and 1st param name is `'rng'`: pass `(rng, result)`.
    - If 2 params and 1st param is not `'rng'`: pass `(result.get("correct"), result.get("vars", {}))`.
    - If 1 param: pass `(result,)`.

### B. `engine/instantiate.py` (L60-L165)
- **Problem:**
  - Distractor or candidate collisions (`TPL-D4`) due to accidental seed collisions trigger immediate failure unless rejection sampling per seed is implemented.
- **Resolution:**
  - Implement deterministic sub-seed rejection sampling up to `MAX_SUBSEED_ATTEMPTS = 8`:
    - `k = 0`: use `seed`.
    - `k in 1..7`: use `(seed * 1009 + k) & 0x7FFFFFFF`.
  - Anti-cloning safeguard: If all 8 sub-seeds fail or if > 20% of seeds require sub-seed retries (indicating structural duplicate distractors), fail immediately with `TPL-D4`.
  - Export public helper `instantiate_verified_seed(template, seed, ...)`.

### C. `engine/invariants.py` & `engine/assemble.py`
- **Problem:**
  - KaTeX validation lacked real AST rendering verification with `pykatex` and specific AST sanity rules.
  - Algebraic sign collapse `+ -5` -> `- 5` was missing in math delimiters.
- **Resolution:**
  - In `engine/invariants.py`:
    - Integrate `pykatex.renderToString(math_content, is_display)` with an LRU cache (`@lru_cache(maxsize=8192)`). Clean `\u0332` -> `^` on any `pykatex.ParseError`.
    - Enforce KaTeX AST invariants:
      * Ban prose > 45 characters inside `\text{...}`.
      * Ban unescaped `_` inside `\text{...}`.
      * Ban orphan double braces `{{...}}`.
      * Ban vacuous quantifiers: `r"\\(?:forall|exists)\s+[a-zA-Z\\]+\s*=\s*[-+]?\d"`.
      * Ban Newtonian dot accents over numbers: `r"\\dot\{\s*\d+\s*\}"`.
  - In `engine/assemble.py`:
    - In `sanitize_katex_syntax`: collapse double interpolation signs inside `$..$` / `$$..$$` (e.g. `+ -` -> `- `, `- -` -> `+ `, `+ +` -> `+ `), maintaining R-23 zero-copy speed and preserving LaTeX command syntax.

### D. `check_templates.py` & `schemas/template.schema.json`
- **Problem:**
  - Validation cache not populated when `shard_py` is supplied at L3361.
  - Diversity ratio bypass `passes_calibrated` allowed lower threshold (0.25).
  - Shift-left parity gaps with Stage 4/6 (Skill detection, R-16 skip, dead trivial check code, lack of distractor refutation verification).
  - JSON diagnostic report dumping redundant errors across 50 seeds.
- **Resolution:**
  - `schemas/template.schema.json`: Add optional properties `"archetype"`, `"assumption_tested_id"`, and `"contract_version"` to `template_item`.
  - `check_templates.py`:
    * Line 3361: Allow cache generation whenever `cta_p is not None`.
    * Line ~3065: Remove `passes_calibrated` bypass and enforce `div_ratio >= 0.50` (or `MIN_DIVERSITY_RATIO`).
    * Use `is_skill_type(comp.get("type") or comp.get("category")) or cid.startswith("Hab-")` for skill detection.
    * Do not skip `R-16` when validating a sufficient set of questions (`len(questions) >= 10`).
    * Replace `_is_trivial_cross_check` dead code with genuine **Strict Distractor Refutation**: for MC7 with verifier code, verify on seed 0 that substituting each distractor into `correct` causes the verifier to return `False` or raise.
    * Enforce >= 5 distinct correct keys across seeds for parametric Concept or MS templates (`vars != {}`).
    * Line ~3883-3888: Compact diagnostic aggregation grouping repeated seed errors by `(rule_id, template_id, normalized_msg)` with `affected_seeds_count` and `sample_seed`.

### E. Canonical Examples `examples/edo/` & `examples/edp/`
- Update `cta.json` for both with explicit `"assumptions"`.
- In `examples/edp/templates/Hab-01.json`: Explicitly constrain domain $x > 0, y > 0$, require $a \ge 2$, and implement a robust symbolic verifier with `sympy` verifying the PDE invariant on the correct answer while refuting all 6 distractors.
- Expand `examples/edo/templates/{C-02, Hab-02}.json` and `examples/edp/templates/{C-01, Hab-01}.json` to 4 orthogonal templates (`direct`, `inverse`, `perturbation`, `boundary_or_edge_case`) passing `check_templates_file_or_dir` with 0 errors.

---

## 4. Verification Checkpoints
- Execute full 9 test suites via single-process pytest.
- Verify Zero-Domain compliance across all modified `.py` files.
- Produce `handoff.md` and report completion to parent agent.
