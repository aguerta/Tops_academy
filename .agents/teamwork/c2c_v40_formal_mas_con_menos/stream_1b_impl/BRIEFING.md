# BRIEFING — Stream 1B (Fase A: Implementador Ortogonal)

## 1. Executive Summary & Objective
Implement and verify Stream 1B enhancements across the compiler, hook guard, and budget guard modules of Content-to-Course (v4.0):
- **Stage Contract Update**: Upgrade to `CONTRACT_VERSION = 2`, `MIN_ARCHETYPES = 4`, and export `ARCHETYPE_KINDS`.
- **Form-C DSL & Compiler Hardening (`compile_shard.py`)**:
  - Support native `dict` Form-C definitions in `TEMPLATES` with backwards compatibility for 9-tuple Form-B.
  - Cartesian product expansion for 2-tuple stems `(contexts, questions)`.
  - Automatic wrapping via `"fmt"` (`@X@`), distractor auto-expansion via `"rats"`/`RATS`, and 2-arg `ver(cand, v)` support.
  - Semantic archetype mapping (`ARCHETYPE_KINDS`) and CTA assumption link validation (`[TPL-ASSUMPTION-LINK]`).
  - Triple anti-cheat verifier contract (soundness, distractor refutation `[VERIFIER-TAUTOLOGY-DETECTED]`, AST hygiene: `[VERIFIER-SWALLOWED-EXCEPTION]`, `[TPL-DEBUG-ARTIFACT]`, `[TPL-AD-HOC-PERTURBATION]`).
  - Algebraic non-cloning verification across all templates (`len(set(valid_100)) == len(valid_100)` for skills), tri-band coverage, cognitive bloom diversity, and active practice requirements.
  - Division detection (`ast.Div`) in `[DIAG-MAGIC-MULT]` and symbolic verification (`SymPy`/`z3`).
  - AST-pruned export of `<CID>.json` (~10 KB vs ~177 KB) and certification artifact `work/shards/<shard_id>.cert.json`.
- **Hook Guard & Budget Governance (`c2c_hook_guard.py`, `budget_guard.py`)**:
  - Rule B Post-PASS Exemption normalization for `status in ("REJECTED", "FAIL", "FAILED")` and shard union.
  - 2D Certified Matrix `decidir_estrategia_edicion` (`error_count`, `affected_line_count`, `has_syntax_error`) enforcing `ModularSplicing` when `error_count >= 6` or `affected_line_count > 5`.
  - Synchronous budget governance (`turn_count <= 40`, `est_tokens <= 5M`, `error_streak < 3`) and `[REPAIR-NO-FULL-CTA]` blocking full CTA reads for repair workers.
  - Pure stdlib implementation with global `try ... except BaseException:` returning exit code 0.
- **Zero-Domain Invariant Enforcement**:
  - All comments and docstrings in `.py` files strictly in English.
  - No occurrence of forbidden lowercase substrings: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`.

---

## 2. Target File Line Ranges & Architectural Anchors

| File Path | Key Line Ranges | Primary Responsibilities |
| :--- | :--- | :--- |
| `engine/stage_contract.py` | L11-L16, L32-L50, L73-L84 | Bump `CONTRACT_VERSION = 2`, `MIN_ARCHETYPES = 4`, export `ARCHETYPE_KINDS`. |
| `compile_shard.py` | L36-L45 (imports)<br>L400-L490 (locator tuple/dict analysis)<br>L730-L800 (code extraction/wrapping)<br>L1450-L1570 (TEMPLATES unpacking)<br>L1570-L1750 (Form-C & Form-B processing)<br>L1800-L1920 (verifier execution & distractor refutation)<br>L2000-L2080 (output JSON writing & AST pruning)<br>L2080-L2600 (M3-ARCHETYPES, non-cloning, Div detection, certification) | Complete Form-C parsing, Cartesian stems, fmt/rats, 2-arg verifiers, AST pruning, tautology detection, and certificate generation. |
| `c2c_hook_guard.py` | L660-L720 (Rule B exemption)<br>L820-L905 (Rule C 2D matrix)<br>L420-L470, L500-L560 (budget & repair CTA checks) | Rule B exemption for REJECTED shards, 2D matrix enforcement, repair CTA blocking, zero-domain english comments. |
| `budget_guard.py` | L28-L35 (SLA constants)<br>L390-L440 (rule evaluation) | Synchronize budget constants and lockfile evaluation logic. |
| `tests/test_m3_archetypes_semantic_gate.py` | L67, L145, L228, L330 | Align fixtures with `min_archetypes = 4` default and add Form-C / tautology / Div tests. |
| `tests/test_compile_shard.py` | L155, L397 | Support 4 archetypes where applicable and add AST pruning tests. |
| `tests/test_shard_compiler_hardening.py` | L80-L125 | Verify zero disk mutation and compiler hardening with 4 archetypes. |
| `tests/test_shard06_and_dry_archetypes.py` | L100-L120 | Test DRY archetypes and Form-C compatibility. |
| `tests/test_invariants_and_shard_overescape_r23.py` | L50-L100 | KaTeX overescape preservation. |
| `tests/test_latex_engine.py` | L30-L100 | LaTeX engine formatting. |
| `tests/test_hook_post_pass_and_write_isolation.py` | L150-L200 | Rule B rejection exemption and 2D matrix. |
| `tests/test_watchdog_and_hooks.py` | L90-L180 | Budget limits and hook checks. |
| `tests/test_specific_error_report_and_stem_gate.py` | L52, L133 | Stem diversity gate and specific error reporting. |

---

## 3. Strict Invariants & Edge Cases

1. **Pure Standard Library in `c2c_hook_guard.py`**:
   - MUST NOT import `sympy`, `z3`, `pydantic`, or any third-party package.
   - All operations must be wrapped in `try ... except BaseException:` with exit code 0 and valid JSON stdout.
2. **Zero-Domain Code & Comments**:
   - In every `.py` file inside `.agents/skills/content-to-course/`:
   - FORBIDDEN substrings: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`.
   - All comments and docstrings in English.
3. **Form-C Backward Compatibility**:
   - Existing 9-tuples `Form-B` must compile identically without any regression.
   - A 2-tuple distractor `(did, val)` without a corresponding entry in `rats` or `RATS` MUST still be rejected in `--strict`.
4. **AST Code Pruning**:
   - Pruned `<CID>.json` code must be self-contained: include only necessary imports, referenced constants, and reachable functions for `generator_code` and `verifier_code`.
   - Size reduction target: < 15 KB (typically ~5-10 KB).
5. **Windows CP1252 Safety**:
   - Never print raw `\u0332` (from pykatex). Clean with `.replace("\u0332", "^")`.
