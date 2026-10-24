# BRIEFING: Stream 1A Forensic Audit (`audit_1a`)

- **Auditor Subagent:** `stream_1a_audit`
- **Orchestrator Conversation ID:** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Audit Target:** Stream 1A (Implementer `stream_1a_impl` + Improver `stream_1a_impr`)
- **Scope:**
  - `engine/assemble.py`
  - `engine/instantiate.py`
  - `engine/invariants.py`
  - `tests/test_katex_prairielearn_tokens.py`

## 1. Audit Mandate & Verification Criteria
1. **Boundary Integrity:** Verify whether changes are strictly confined to the 4 assigned production/test files, without modifying files assigned to other streams or leaving untracked residue in repository root.
2. **Requirement Completeness:**
   - PrairieLearn `@var@` / `@var:fmt@` interpolation (Phase 0 priority pass, raw string support, nested KaTeX, single-letter tokens `@k@`, `@n@`).
   - Backward compatibility for `{var}` / `{var:fmt}` without corrupting LaTeX braces (`\frac{a}{b}`, matrix row breaks `\\`, `\mathbb{R}^k`).
   - Question-type coverage: `fill_in_the_blank` (`correct_answer`, `accepted_equivalents`), `multiple_select` (`content`, `value`, `error_rationale`), `hints` (strings & dicts), `stem_variants`.
   - `compute_option_length_metrics` / `calibrate_option_lengths`: Zero fake text padding, pure deterministic psychometric diagnostics.
   - Anti-unrendered-placeholder invariants (`invariants.py` + `instantiate.py`): Hard rejection of `@ident@`, `{key}` when in variables or bare in prose, zero false positives on legitimate KaTeX (`\xrightarrow{d}`, `x_n`, `\mathbb{R}^k`, `\frac{a}{b}`, `\mathcal{N}(0, \sigma^2)`, `S_{zz}`).
   - Zero stubs, zero fake mocks, zero weakened assertions, zero `pytest.skip` workarounds.
3. **Regression & Test Verification:**
   - Execute all targeted test suites independently in `.venv` and verify 100% pass rate.
