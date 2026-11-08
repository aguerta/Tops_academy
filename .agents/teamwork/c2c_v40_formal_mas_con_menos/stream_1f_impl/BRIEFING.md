# BRIEFING — Stream 1F (Fase A: Implementador Ortogonal)

- **Date:** 2026-11-07
- **Agent:** `c2c40_implementer` (Stream 1F)
- **Parent Conversation ID:** `cbe0c4d9-d376-429c-92b2-ffaeec91ae7f`
- **Assigned Folder:** `d:\Augusto\personal_portfolio\Tops_academy\.agents\teamwork\c2c_v40_formal_mas_con_menos\stream_1f_impl`

---

## 1. Pre-Flight File Inspection Summary

All 6 production/test files within the scope have been read and inspected:

1. **`repair_loop.py` (236 lines, SKILL_DIR):**
   - Implements `RepairIterationReport`, `RepairResult`, `RepairLoop` with `sanitize_latex_escapes()`.
   - **Zero-Domain Guard:** Banned lowercase substrings: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`. All docstrings, comments and identifiers in English.
   - Slicing / Remediation Order generation and 2D matrix recommendations to be integrated here.

2. **`src/validator/rules.py` (1165 lines):**
   - Implements `check_semantic_rules`, `check_strict_rules`, `check_extended_quality_rules`.
   - Currently implements R-04 through R-14, R-17, R-18, R-19, R-20, R-22, R-23.
   - To be extended with pure functions and integrated checks for:
     - R-24: `check_vacuous_quantifiers(text)` (`ERR_VACUOUS_QUANTIFIER`)
     - R-25: `check_hint_answer_leak(hints, correct_text)` (`ERR_HINT_ANSWER_LEAK_S12`)
     - R-26: `check_option_parenthetical_telltale(option_text)` (`ERR_OPTION_PARENTHETICAL_TELLTALE`)
     - R-27: `check_numeric_newton_dot(text)` (`ERR_NUMERIC_NEWTON_DOT`)

3. **`src/validator/psychometric_checker.py` (125 lines):**
   - Implements `check_psychometrics` (R-15 per-item length symmetry, R-16 per-course distribution).
   - Can export or co-house anti-gaming / psychometric heuristics (such as telltales or hint leaks).

4. **`src/validator/lexical_scanner.py` (395 lines):**
   - Implements Pass 1 pre-parse token scanner (`scan_lexical`) with fast zero-copy regexes.
   - Verified that new rules do not impact lexical pass or regress zero-copy speed (< 10s).

5. **`tests/test_validator.py` (1026 lines):**
   - Validates all validator passes and fixtures.
   - New tests to be added for pure functions and extended validation rules R-24, R-25, R-26, R-27, plus `repair_loop.py` competence slicing, dual schema support, and 2D matrix recommendation.

6. **`tests/test_katex_overescape_validator_r23.py` (569 lines):**
   - Validates R-23 safeguards, memory parity, and tests all real published courses in `courses/*.json` with `strict=True`.
   - Invariant: Zero regressions and zero false positives across real published courses.

---

## 2. Technical Specification & Architecture

### A. New Deterministic Pure Functions & Rules

1. **`R-24` Vacuous Quantifiers (`check_vacuous_quantifiers`):**
   - Pattern: `r"\\(?:forall|exists)\s+(?:\\[a-zA-Z]+|[a-zA-Z])\s*=\s*[-+]?\d+(?:\.\d+)?"`
   - Detects quantifiers tied directly to numeric constants (e.g., `\forall \varepsilon = 0.05`, `\exists \delta = 0.1`, `\forall x = -2`).
   - Pure function: `check_vacuous_quantifiers(text: str) -> list[str]`
   - Integration: Flagged in `check_extended_quality_rules` on stem, hints, solution, and option content.

2. **`R-25` Socratic Hint Answer Leak (`check_hint_answer_leak`):**
   - Purpose: Ensure first two hints (`hints[0]`, `hints[1]`) do not verbatim leak the correct answer when `len(correct_text.strip().strip("$")) >= 15`.
   - Pure function: `check_hint_answer_leak(hints: list[Any], correct_text: str) -> list[tuple[int, str]]`
   - Normalization: strips spaces and `$` delimiters. If normalized correct answer appears in normalized `hints[0]` or `hints[1]`, report error.

3. **`R-26` Parenthetical Telltale in Options (`check_option_parenthetical_telltale`):**
   - Pattern: `r"\([^)]*?\b(?:sesgo\b|confusi[oó]n\s+con\b|error\s+al\b|omitiendo\b|despeje\s+err[oó]neo\b)[^)]*?\)"`
   - Detects internal distractor design commentary inadvertently leaked into visible option text.
   - Pure function: `check_option_parenthetical_telltale(text: str) -> list[str]`
   - Integration: Flagged on visible `options[].content`.

4. **`R-27` Numeric Newton Dot (`check_numeric_newton_dot`):**
   - Pattern: `r"\\d?dot\{\s*[-+]?\d+(?:\.\d+)?\s*\}"` and `r"\\d?dot\s*[-+]?\d+"`
   - Detects Newton differential dots erroneously placed over numeric literals (e.g., `\dot{5}`, `\ddot{12}`, `\dot{-3.5}`).
   - Pure function: `check_numeric_newton_dot(text: str) -> list[str]`
   - Integration: Flagged in `check_extended_quality_rules` on all mathematical fields.

### B. `repair_loop.py` Alignment: Competence Slicing, 2D Matrix & Dual Schemas

1. **Dual Schema Support:**
   - Reading `grouped_by_rule` OR `groups`.
   - Reading `failing_shards` OR `affected_shards`.
   - Case-insensitive status evaluation: `str(status).strip().upper() in ("REJECTED", "FAIL", "FAILED")`.

2. **Competence Slicing (< 2 KB):**
   - Function: `slice_competence_context(comp_data: dict[str, Any], max_bytes: int = 2048) -> dict[str, Any]`
   - Filters only the affected competency's core fields (`id`, `name`, `definition`/`description`, `assumptions`, `distractors`).
   - Prevents huge payloads by ensuring compact representation < 2048 bytes; never dumps full `cta.json`.

3. **2D Matrix Recommendation:**
   - Function: `evaluate_2d_matrix_recommendation(error_count: int, affected_line_count: int, shard_id: str, competency_id: str) -> dict[str, Any]`
   - If `1 <= error_count < 6` and `affected_line_count <= 5`:
     - Strategy: `"edit_file"`
     - Directive: `"edit_file"`
   - If `error_count >= 6` or `affected_line_count > 5`:
     - Strategy: `"ModularSplicing"`
     - Directive: `f"ModularSplicing shard_fixes/{shard_id}/{competency_id}.py"`

4. **Remediation Order Builder:**
   - Function: `build_remediation_order(audit_report: dict[str, Any], cta_data: Optional[dict[str, Any]] = None, ...) -> dict[str, Any]`
   - Orchestrates dual-schema parsing, competence slicing, and 2D matrix determination.

---

## 3. Pre-Flight Verification on Published Courses

- Tested patterns against all 6 active published courses in `courses/*.json` (`estadistica_3_s9_vmapreduce5.json`, `saul_cls_2_y_3_vmapreduce1.json`, `saul_control_optimo_vmapreduce2.json`, `saul_pc_sistemas_de_ecuaciones_vmapreduce1.json`, `saul_pre_parcial.json`, `solow_growth_model.json`).
- Result: **0 false positives across all published courses**.
- Full test suite baseline: **212 passed in 15.91s**.

---

## 4. Execution Plan

1. Update `src/validator/rules.py`:
   - Add and export pure functions `check_vacuous_quantifiers`, `check_hint_answer_leak`, `check_option_parenthetical_telltale`, `check_numeric_newton_dot`.
   - Integrate checks into `check_extended_quality_rules`.
2. Update `src/validator/psychometric_checker.py`:
   - Re-export or integrate rule helpers if needed for direct psychometric auditing.
3. Update `repair_loop.py`:
   - Implement `slice_competence_context`, `evaluate_2d_matrix_recommendation`, `build_remediation_order`.
   - Enforce 100% Zero-Domain compliance (English only, no forbidden domain substrings).
4. Update `tests/test_validator.py` and `tests/test_katex_overescape_validator_r23.py`:
   - Add unit tests for R-24, R-25, R-26, R-27 (positive and negative).
   - Add unit tests for `repair_loop.py` dual schema, slicing < 2 KB, 2D matrix recommendation.
   - Verify published courses pass with 0 errors.
5. Run full pytest suite, verify Zero-Domain compliance, write `handoff.md`, and notify parent.
