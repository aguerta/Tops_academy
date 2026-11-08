# BRIEFING — Stream 1A: Formal CTA Stage 1, Assumptions, 2D Telemetry & DAG Monotonicity

## 1. Executive Summary & Scope
Stream 1A establishes the formal verification core for Stage 1 Cognitive Task Analysis (CTA) under the Flash Dyad protocol. This briefing captures the precise technical baseline, line ranges, invariants, and edge cases across the four production files and seven test suites in our Exclusive Write Boundary.

---

## 2. Target Files & Exact Line Ranges

### A. `schemas/cta.schema.json`
- **Current Lines:** 1-152.
- **Modifications:**
  - In `definitions`: Add `assumption` object schema with required fields `["id", "statement_latex", "violation_consequence"]`, optional `"name"`, `"role_in_proof"`.
  - In `definitions.competency.properties`: Add optional `"assumptions"`: array of `$ref: "#/definitions/assumption"`.
  - Preserves full backward compatibility with legacy CTA objects.

### B. `compile_cta.py`
- **Current Lines:** 1-2285.
- **Key Regions:**
  - **Lines 82-356 (`CtaDataLineLocator`):**
    * AST indexing of `COMPETENCIES`: Support 6-tuples, 7-tuples `(comp_type, title, desc, bloom, prereqs, distractors, assumptions)` and dictionary representations with `"assumptions"`.
    * Index assumption line numbers and subfields (`statement_latex`, `violation_consequence`, `name`, `id`).
  - **Lines 664-736 (`_normalize_distractors_list`) & Lines 768-1000 (`compile_cta_module`):**
    * Add `_normalize_assumptions_list`: normalize 3-tuples `(id_or_name, statement_latex, violation_consequence)` or dicts, auto-prefixing `id` as `f"A-{cid_clean}-{idx:02d}"` if `id` does not begin with `A-`.
    * Add parameter `require_assumptions: bool = False`. Check if `require_assumptions=True` or `getattr(mod, "CTA_CONTRACT_VERSION", 1) >= 2`.
    * When required: competencies of type `Skill` or `Concept` must have `>= 1` assumption with `len(statement_latex.strip()) >= 10` and `len(violation_consequence.strip()) >= 10`. If missing/invalid, report `[CTA-ASSUMPTIONS-MISSING]` mapped to exact line in `cta_data.py`.
  - **Lines 1317-1350 & 1671-1706 (2D Attempt Persistence):**
    * When writing `.check_attempts/compile_cta*.json`, persist:
      - `"affected_line_count"`: distinct source lines reported in errors (`0` if passed).
      - `"has_syntax_error"`: boolean.
      - `"error_sha256"`: SHA-256 hex hash of normalized sorted `f"{rule_tag}:{line}"` signatures (`""` if passed).
  - **Lines 1360-1400 (`ModularSplicing`):**
    * Load and splice `cta_fixes/<CID>.py` (supporting tuple or dict format `COMPETENCY = ...` or `COMPETENCIES = [...]`).
  - **Lines 1710-1732 (Compiler Receipt `cta.cert.json`):**
    * On `passed=True`, write `cta.cert.json` alongside `cta.json` with hash receipts:
      `{"schema_version": 1, "stage": "cta", "artifact_id": "cta", "source_sha256": <hex>, "cta_sha256": <hex>, "compiler_sha256": <hex>, "contract_version": 2, "passed_50_seeds": True, "created_at": <ISO8601>}`.
  - **Lines 2177-2285 (`main()` CLI):**
    * Add CLI argument `--require-assumptions`.

### C. `cta_merge.py`
- **Current Lines:** 1-1992.
- **Key Regions:**
  - **Lines 126-390 (`auto_balance_math_delimiters` & `auto_wrap_bare_latex_in_cta_field`):**
    * Non-destructive KaTeX repair: Never corrupt partially delimited strings like `r"Sea P(Y \ge $\delta) = 0.95$"`.
    * If unclosed math delimiters or internal commands cannot be symmetrically and safely repaired, leave unmutated for `check_cta_katex` to flag.
  - **Lines 973-1060 & 1570-1678 (Part Merging & Harmonizer):**
    * Preserve `assumptions` across part merging and harmonizer merges.
  - **Lines 1810-1908 (`render_cta_md`):**
    * Render markdown tables/sections for `assumptions` when present.
  - **Epistemic Monotonicity ($K_t \subseteq K_{t+1}$):**
    * In append/merge mode, base competencies cannot be dropped, truncated, or stripped of distractors/assumptions.

### D. `check_cta.py`
- **Current Lines:** 1-912.
- **Key Regions:**
  - **Lines 184-281 (`check_prerequisites_dag`):**
    * Deterministic DFS cycle path reporting (e.g., `C-01 -> C-02 -> C-01`).
    * Full referential integrity verification (no orphan IDs).
  - **Lines 460-585 (`check_cta_katex`):**
    * Integrate `pykatex.renderToString` fast parser with fallback.
    * Windows cp1252 safety: Clean `"\u0332"` -> `"^"` in ParseError.
    * Validate `statement_latex` and `violation_consequence` inside `assumptions`.
  - **Lines 588-735 & 787-836 (`validate_cta_rules`):**
    * Validate assumption contracts when version requires it.

---

## 3. Invariants & Zero-Domain Guardrails
1. **Zero-Domain Substring Check:**
   - Forbidden lowercase tokens in all `.py` files under `.agents/skills/content-to-course/`:
     `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`.
   - All code, docstrings, and comments in `.py` files MUST be written in English.
2. **Windows cp1252 Console Safety:**
   - Clean `\u0332` from `pykatex` error strings before printing or re-raising.
3. **Execution Guard:**
   - Pytest execution uses `-o addopts=""`.
