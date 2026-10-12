# Forensic Audit Report: Phase 1 Codebase Integrity

**Work Product**: Phase 1 Codebase (`.agents/skills/content-to-course/`, `platform/`, `courses/`, `tests/`)  
**Profile**: General Project (Integrity Mode: Demo)  
**Auditor**: `auditor_phase1_integrity`  
**Verdict**: **INTEGRITY VIOLATION**

---

## 1. Observation

### Check 1: Anti-cheating & Facade Check
- **Tests inspection**:
  - `tests/test_validator.py` (521 lines) contains 0 instances of `mock`, `patch`, `skip`, or `xfail`. 0 empty `pass` or dummy assertions.
  - `tests/test_platform.py` (281 lines) contains 0 instances of `mock`, `patch`, `skip`, or `xfail`. 0 empty `pass` or dummy assertions.
- **Platform Implementation**:
  - `platform/src/utils/mathEquivalence.ts` implements genuine parsing, normalization, mathjs evaluation, tolerance checking, and Monte Carlo sampling without bypasses or hardcoded constant returns.
- **Result**: PASS.

---

### Check 2: Anti-overfitting & Domain Logic Check
- **Tool execution**: Scanned all `.py` files under `.agents/skills/content-to-course/` excluding `examples/` for domain keywords: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`.
- **Findings**:
  1. File: `.agents/skills/content-to-course\pdf_extractor.py`:
     - Lines 368-379:
       ```python
       # Also detect typical partial differential equation patterns in plain text
       pde_patterns = [
           r"([Uu]_[xytz]{1,3}\s*[+\-=].*?=\s*[\w\d\-+()*/]+)",
           r"(F\([\w\s,.]+\)\s*=\s*0)",
           r"(\w+\s*U_x\s*[+\-]\s*\w+\s*U_y\s*=\s*[\w\d\-+()*/]+)",
           r"(f\(t[\w, ]+\)\s*=\s*t\^?\w*\s*f\([\w, ]+\))",
       ]
       for pat in pde_patterns:
           for match in re.finditer(pat, text):
               candidate = match.group(1).strip()
               if len(candidate) > 4 and candidate not in equations:
                   equations.append(candidate)
       ```
     - Lines 389-394:
       ```python
       section_keywords = [
           "Contenido", "Agenda", "Definición", "Homogeneidad",
           "Euler", "Separación de Variables", "Características",
           "Lagrange", "Cauchy", "Segundo Orden", "Operadores",
           "Bibliografía", "Referencias"
       ]
       ```
  2. File: `.agents/skills/content-to-course\ingest.py`:
     - Line 49: Docstring comment in `normalize_corrupt_diacritics`:
       `Examples: Regresi´on -> Regresión, Te´orico -> Teórico, ˆβ -> β̂` (Non-functional docstring explanation of broken accents).
  3. File: `tests/test_skill.py`:
     - Line 706: `test_engine_zero_domain_logic` restricts its check to:
       `engine_dir = SKILL_DIR / "engine"`
       thereby failing to inspect `.agents/skills/content-to-course/*.py` and masking the presence of `pdf_extractor.py`.
- **Result**: **FAIL** (Domain-specific EDP regexes and keywords exist in `.agents/skills/content-to-course/pdf_extractor.py`).

---

### Check 3: Legacy Course Immutability Check
- **SHA-256 Hashes**:
  - `courses/pde_course.json`:
    - Computed: `3A8D4C0D23CA9FCFA8A2B7E05765725E1C3B71391DDB74011667850256694192`
    - Baseline: `3A8D4C0D23CA9FCFA8A2B7E05765725E1C3B71391DDB74011667850256694192`
    - Status: Exact Match (0 modifications).
  - `courses/sistemas_edos.json`:
    - Computed: `6AFAFB088AEABF0729A4223DE8F28BEC80D958395C5157C56D592F4B9D3FCB06`
    - Baseline: `6AFAFB088AEABF0729A4223DE8F28BEC80D958395C5157C56D592F4B9D3FCB06`
    - Status: Exact Match (0 modifications).
- **Strict Validation Execution**:
  - Command: `python -m validator.cli courses/pde_course.json --strict`
    Output: `VALID: Course 'pde_course' passed all 16 validation rules (strict mode).` Exit code: 0.
  - Command: `python -m validator.cli courses/sistemas_edos.json --strict`
    Output: `VALID: Course 'sistemas_edos' passed all 16 validation rules (strict mode).` Exit code: 0.
- **Result**: PASS.

---

### Check 4: Independent Test Execution
- **Run A**: `python -m pytest tests/test_skill.py -v`
  - First execution: Exit code 1 (31 passed, 1 failed in 69.96s):
    `FAILED tests/test_skill.py::TestSandboxSecurity::test_sandbox_deterministic_seed`
    `engine.sandbox.SandboxTimeoutError: Template execution timed out after 2.0s (seed=43)`
  - Root cause: `engine/sandbox.py:execute_sandbox_instance` launches Python subprocesses with a default `timeout: float = 2.0`. On Windows under full suite execution load, process startup exceeded 2.0s.
  - Second execution (clean rerun): Exit code 0 (32 passed in 49.40s).
- **Run B**: `python -m pytest tests/test_validator.py tests/test_platform.py -v`
  - Output: `114 passed in 16.28s`. Exit code: 0. (100% pass rate).
- **Run C**: `node tests/test_math_adversarial_suite.mjs`
  - Output: `81/81 Passed, 0 Failed`. Exit code: 0. (100% pass rate).
- **Result**: PARTIAL PASS / CONCERN (Pass rate across validator, platform, and math suite is 100%; `test_skill.py` exhibits timeout flakiness on Windows due to tight 2.0s subprocess timeout).

---

## 2. Logic Chain

1. **Premise 1 (R6 & Dispatch Requirement)**:
   ORIGINAL_REQUEST.md Requirement R6 explicitly demands: *"Eliminar el código específico de EDP/EDO y los tests que dependían de él (reescribirlos contra el motor genérico)."* Furthermore, the dispatch prompt specifies: *"Confirm that 0 domain logic exists in the skill and engine code"*, and Acceptance Criteria specifies: *"grep -ri de términos de dominio (edo, pde, derivadas, jacobiana, eigen, regresi) en .py de la skill y del motor no encuentra lógica de dominio (solo ejemplos en examples/)."*
2. **Observation 1**:
   The file `.agents/skills/content-to-course/pdf_extractor.py` is present in the skill directory and contains `pde_patterns` targeting PDE notation (`[Uu]_[xytz]`, `U_x`, `U_y`), and section keywords including `"Euler"`, `"Lagrange"`, `"Cauchy"`, `"Separación de Variables"`.
3. **Inference 1**:
   Although `pdf_extractor.py` is unused by the new v2 pipeline runner (`run.py`), it was not purged from the skill codebase during migration. Because it resides directly in `.agents/skills/content-to-course/`, it constitutes unpurged domain-specific code in violation of Requirement R6 and Check 2.
4. **Premise 2 (Mandatory Forensic Policy)**:
   *"If ANY check fails, your verdict is INTEGRITY VIOLATION and you MUST reject the work product."*
5. **Conclusion**:
   Check 2 fails. Therefore, the mandatory forensic verdict is **INTEGRITY VIOLATION**.

---

## 3. Caveats

- `pdf_extractor.py` appears to be orphaned legacy code from v1 and is not imported by `run.py`, `ingest.py`, or `run_platform.py`. Deleting or archiving this unreferenced file will immediately bring the codebase into full compliance.
- In `ingest.py:49`, `Regresi´on` is merely an illustrative comment in a docstring explaining broken diacritic normalization, not executable domain logic.
- In `engine/sandbox.py`, the default timeout of 2.0s in `execute_sandbox_instance` is marginally tight on Windows environments where subprocess creation overhead can occasionally exceed 2.0s under I/O load. Increasing the default timeout to 5.0s would eliminate test flakiness.

---

## 4. Conclusion

**Verdict: INTEGRITY VIOLATION**

**Blocking Reason**:
Check 2 failed. Hardcoded PDE patterns and mathematical topic terms (`Euler`, `Lagrange`, `Cauchy`) remain inside `.agents/skills/content-to-course/pdf_extractor.py`.

**Required Remediations**:
1. Remove `.agents/skills/content-to-course/pdf_extractor.py` (or relocate it outside the skill directory) as required by R6.
2. In `tests/test_skill.py:test_engine_zero_domain_logic`, expand the search scope to inspect all `.py` files in `SKILL_DIR` (excluding `examples/`), ensuring any future orphaned domain files are caught.
3. In `engine/sandbox.py:execute_sandbox_instance`, consider increasing the default subprocess timeout from 2.0s to 5.0s to ensure reliable execution on Windows.

---

## 5. Verification Method

To independently verify the finding and the remediation:

1. **Verify the domain logic violation in `pdf_extractor.py`**:
   ```powershell
   python -c "
   import re
   with open(r'.agents/skills/content-to-course/pdf_extractor.py', 'r', encoding='utf-8') as f:
       for idx, line in enumerate(f, 1):
           if re.search(r'\b(pde|euler|lagrange|cauchy)\b', line, re.I):
               print(f'L{idx}: {line.strip()}')
   "
   ```
   *Expected result*: Prints lines 368, 374, 391, 392.

2. **Verify legacy courses immutability and strict validation**:
   ```powershell
   powershell -Command "Get-FileHash courses\pde_course.json, courses\sistemas_edos.json -Algorithm SHA256 | Format-List"
   python -m validator.cli courses/pde_course.json --strict
   python -m validator.cli courses/sistemas_edos.json --strict
   ```

3. **Verify independent test suites**:
   ```powershell
   python -m pytest tests/test_validator.py tests/test_platform.py -v
   node tests/test_math_adversarial_suite.mjs
   python -m pytest tests/test_skill.py -v
   ```

4. **Invalidation condition**:
   The violation is resolved if `.agents/skills/content-to-course/pdf_extractor.py` is removed, and running a recursive scan for domain terms across all non-example `.py` files in `.agents/skills/content-to-course/` returns exactly 0 matches.
