# Stream 1A: Formal CTA Schema, PyKaTeX Math Repair & Epistemic Monotonicity — Implementation Handoff

## 1. Executive Summary
Stream 1A has completed all assigned deliverables with production-grade formal verification, edge-case hardening, and 100% test pass rates (107/107 passed across 7 assigned suites, plus 33/33 in test_skill.py).

Zero regressions occurred, strict Zero-Domain guardrails were verified with 0 violations across all modified `.py` files, and Windows `cp1252` terminal safety was fully guaranteed by sanitizing `\u0332` to `^` on KaTeX parse errors.

---

## 2. Modified Production Files & Core Architectural Enhancements

### A. `schemas/cta.schema.json`
- **Formal Assumption Definition:** Added `definitions.assumption` enforcing:
  - `id`: pattern `^A-[A-Za-z0-9]+-\d{2}$` (e.g., `A-C01-01`).
  - `statement_latex`: KaTeX-safe string statement.
  - `violation_consequence`: string consequence explaining why the proof/derivation breaks down if violated.
  - Optional: `name` (label) and `role_in_proof`.
- **Competency Extension:** Added `"assumptions"` array property referencing `#/definitions/assumption`.

### B. `check_cta.py`
- **Safe PyKaTeX Integration:** Implemented `_validate_pykatex_math_span` with Windows `cp1252` terminal safety, substituting Unicode combining low line `\u0332` with `^` to prevent `UnicodeEncodeError`. Standalone `{...}` stripping fallback handled cleanly.
- **Deterministic DAG Cycle Detection:** Replaced non-deterministic traversal with sorted adjacency traversal in `check_prerequisites_dag`. Cycle paths now emit exact closed directed cycles (e.g., `C-01 -> C-02 -> C-01`).
- **Assumptions KaTeX Math Auditing:** Extended `check_cta_katex` to unconditionally audit `assumptions` for:
  - Mobile prose overflow (`\text{}` exceeding 45 chars via `[KATEX-PROSE-OVERFLOW]`).
  - Corrupted ASCII control characters (`\x07`, `\x08`, `\x0b`, `\x0c`, `\x0d`).
  - Raw unescaped LaTeX outside `$...$` or `$$...$$`.
  - KaTeX parse errors.
- **Rule `[CTA-ASSUMPTIONS-MISSING]`:** Enforced on `concept` and `skill` competencies when `require_assumptions=True` or `contract_version >= 2` (requires `>=1` valid assumption with `statement_latex` and `violation_consequence` of `>=10` characters).

### C. `cta_merge.py`
- **Symmetrical Math Repair Helper:** Implemented `try_symmetrical_math_repair(text)`:
  - Non-destructively repairs split math delimiters (e.g., `r"Sea P(Y \ge $\delta) = 0.95$"` -> `r"Sea $P(Y \ge \delta) = 0.95$"`).
  - Validates all candidate math spans under `pykatex.renderToString`.
  - Unresolvable or non-matching expressions remain untouched for `check_cta_katex`.
- **LaTeX Command Extensions:** Added `le` and `ge` to `LATEX_CMD_NAMES` and `MATH_NAMES`.
- **Assumption Preservation & Global Renumbering:** `merge_cta_parts` preserves local assumptions across all subparts and renumbers them to match the final global competency ID (e.g. `A-C01-01`, `A-C02-01`).
- **Epistemic Monotonicity ($K_t \subseteq K_{t+1}$):** In `apply_harmonize`, existing base course competencies (`existing_competency_ids`) can never be dropped or absorbed into newly generated incoming competencies. Rejections are logged with `"rejected_by_monotonicity"`. Unifies assumptions and distractors without loss.
- **Formal Assumptions Table Rendering:** `render_cta_md` renders a dedicated Markdown table for all formal mathematical assumptions per competency.

### D. `compile_cta.py`
- **Assumptions Input Flexibility:** Updated `compile_cta_module` and `_normalize_assumptions_list` to parse:
  - 7-tuples with assumptions: `(type, id, name, desc_latex, bloom, prereqs, distractors, assumptions)` or `(type, name, desc_latex, bloom, prereqs, distractors, assumptions)`.
  - 10-tuples: `(type, id, name, desc_latex, bloom, doc, page, prereqs, distractors, assumptions)`.
  - Dictionaries with `"assumptions"` key.
  - Dict or tuple assumptions with auto-assigned `A-<CID>-XX` IDs.
- **`CtaDataLineLocator` Line Indexing:**
  - Added AST indexation for `assumption_lines` and `assumption_field_lines`.
  - Fallback decomposition for `A-...` IDs.
  - Direct mapping of `[CTA-ASSUMPTIONS-MISSING]` to the exact competency declaration line in `cta_data.py`.
- **2D Attempt State Persistence (`.check_attempts/compile_cta*.json`):**
  - Failure: records `"affected_line_count"` (unique source lines with errors), `"has_syntax_error"`, and `"error_sha256"` (64-char hex SHA-256).
  - Pass: records `"affected_line_count": 0`, `"has_syntax_error": False`, `"error_sha256": ""`.
- **Modular Splicing (`cta_fixes/<CID>.py`):**
  - Supports both tuple and dict overrides (`COMPETENCY = (...)` or `COMPETENCY = {...}`).
- **Formal Certificate (`cta.cert.json`):**
  - Emitted alongside `cta.json` upon `is_valid=True`.
  - Schema: `schema_version: 1`, `stage: "cta"`, `artifact_id: "cta"`, `source_sha256`, `cta_sha256`, `compiler_sha256`, `contract_version: 2`, `passed_50_seeds: True`.
- **CLI Flag:** Added `--require-assumptions` flag in `main()`.

---

## 3. Test Suites Verification

Executed single-process focused pytest:
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_cta_mapreduce.py tests/test_cta_merge_prereq_scoping.py tests/test_c2c_v321_comp1_cta.py tests/test_cta_healing.py tests/test_cta_sweetspot_and_autoheal.py tests/test_fast_ingest_and_cta_append.py tests/test_handouts.py -q
```
**Results:** `107 passed in 7.54s` (0 failures, 0 warnings).

### Breakdown per Assigned Suite:
1. `tests/test_cta_mapreduce.py`: 8 passed
2. `tests/test_cta_merge_prereq_scoping.py`: 11 passed (includes exact cycle paths, assumption renumbering across parts, and epistemic monotonicity)
3. `tests/test_c2c_v321_comp1_cta.py`: 21 passed (includes 7-tuple/dict assumptions, require_assumptions rule, line mapping, 2D metrics, cert emission, modular splicing)
4. `tests/test_cta_healing.py`: 21 passed (includes symmetrical math repair, KaTeX cp1252 sanitization, and assumptions KaTeX validation)
5. `tests/test_cta_sweetspot_and_autoheal.py`: 18 passed
6. `tests/test_fast_ingest_and_cta_append.py`: 15 passed
7. `tests/test_handouts.py`: 13 passed

### Platform Regression Check:
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_skill.py -q
```
**Results:** `33 passed in 4.54s`.

---

## 4. Zero-Domain Guardrails & Safety Compliance

- **Zero-Domain Invariant:** Automated substring scan executed across all edited `.py` files inside `.agents/skills/content-to-course/` (`compile_cta.py`, `cta_merge.py`, `check_cta.py`) for forbidden lowercase tokens:
  `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`.
  **Outcome:** `0 violations found`.
- **Exclusive Write Boundary:** Strictly adhered to without leaving untracked files or modifying any file outside the assigned boundary.
- **Console Safety:** Zero unhandled combining characters (`\u0332`); all error messages render cleanly on Windows `cp1252`.
