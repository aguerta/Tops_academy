# Handoff Report: Packaging & CLI Remediation Plan

**Agent**: Explorer 3 (`explorer_m1_fix_packaging`)  
**Task**: Milestone 1 Packaging & CLI Remediation Exploration  
**Recipient**: Parent Orchestrator (`84948f37-b77a-4675-a1cb-6a3b8a288462`)  
**Date**: 2026-10-11T01:41:00Z  

---

## 1. Observation

1. **`pyproject.toml` Package Discovery and Script Entrypoint**:
   - In `pyproject.toml` lines 18-19:
     ```toml
     [project.scripts]
     validate-course = "src.validator.cli:main"
     ```
   - Notice that `pyproject.toml` completely omits `[tool.setuptools.packages.find]`.
   - Executing `python -c "import setuptools; print(setuptools.find_packages('src'))"` returns `['validator']`. The package discovered inside `src` is `validator`, not `src`.
   - Running the installed console script executable `validate-course` produced:
     ```
     Traceback (most recent call last):
       File "<frozen runpy>", line 198, in _run_module_as_main
       File "<frozen runpy>", line 88, in _run_code
       File ".../Scripts/validate-course.exe/__main__.py", line 2, in <module>
     ModuleNotFoundError: No module named 'src'
     ```
   - Cause: The script attempts `from src.validator.cli import main`. When installed, site-packages contains `validator`, not `src`.

2. **Absolute Imports Across `src/validator/` Modules**:
   - In `src/validator/__init__.py:2-7`:
     ```python
     from src.validator.models import ValidationError, ValidationResult
     from src.validator.core import validate_course, validate_course_content
     from src.validator.lexical_scanner import scan_lexical
     from src.validator.schema_validator import validate_schema, COURSE_SCHEMA
     from src.validator.rules import check_semantic_rules
     from src.validator.psychometric_checker import check_psychometrics
     ```
   - In `src/validator/cli.py:20-21`:
     ```python
     from src.validator.core import validate_course
     from src.validator.models import ValidationResult
     ```
   - In `src/validator/core.py:8-12`:
     ```python
     from src.validator.models import ValidationError, ValidationResult
     from src.validator.lexical_scanner import scan_lexical
     from src.validator.schema_validator import validate_schema
     from src.validator.rules import check_semantic_rules
     from src.validator.psychometric_checker import check_psychometrics
     ```
   - In `src/validator/lexical_scanner.py:13`: `from src.validator.models import ValidationError`
   - In `src/validator/schema_validator.py:9`: `from src.validator.models import ValidationError`
   - In `src/validator/rules.py:19`: `from src.validator.models import ValidationError`
   - In `src/validator/psychometric_checker.py:12`: `from src.validator.models import ValidationError`
   - Testing external import from an isolated directory:
     Command: `python -c "import sys; sys.path.insert(0, r'g:\Mi unidad\Competence_analyser\src'); import validator"` (executed from `C:\Users\augus`)
     Result:
     ```
     Traceback (most recent call last):
       File "<string>", line 1, in <module>
       File "g:\Mi unidad\Competence_analyser\src\validator\__init__.py", line 2, in <module>
         from src.validator.models import ValidationError, ValidationResult
     ModuleNotFoundError: No module named 'src'
     ```

3. **`--strict` Flag Semantics**:
   - In `src/validator/cli.py:42-57`:
     `def run_validation(target_path: Path, strict: bool = False) -> list[ValidationResult]:` receives `strict`, but calls `validate_course(target_path)` without passing `strict`.
   - In `src/validator/core.py:15, 78`:
     `validate_course_content` and `validate_course` do not accept `strict`, nor do they implement any strict validation pass.

4. **Missing Packaging Tests in Test Suite**:
   - In `tests/validator/test_validator.py:84-85`:
     Tests invoke `subprocess.run([sys.executable, "-m", "src.validator.cli", ...])`.
   - No test in `tests/validator/test_validator.py` or elsewhere tests the console script `validate-course` or verifies importing `validator` from an external directory.

---

## 2. Logic Chain

1. **Premise 1 (Packaging Architecture)**:
   - Observation 1 proves that setuptools discovers `validator` when searching under `src/`.
   - Therefore, the installable package name is `validator`.
   - Because `[project.scripts]` mapped `validate-course` to `"src.validator.cli:main"`, setuptools generates an entrypoint script that imports `src.validator.cli`. This fails because `src` is not installed into site-packages.
   - *Inference*: Updating `pyproject.toml` with `[tool.setuptools.packages.find] where = ["src"]` and changing the script entrypoint to `validate-course = "validator.cli:main"` fixes the launcher.

2. **Premise 2 (Module Portability & Relative Imports)**:
   - Observation 2 proves that every internal module in `src/validator/` imports with `from src.validator...`.
   - Even if the package is discovered as `validator`, importing `validator` fails immediately because `src/validator/__init__.py` attempts `import src`.
   - When all internal imports are converted to relative imports (`from .X import Y`), the modules become independent of the parent package name: they work identically whether imported as `validator` (when installed) or as `src.validator` (when run from repository root).

3. **Premise 3 (Strict Mode Semantics)**:
   - Observation 3 proves that `--strict` is currently an inert facade flag.
   - To fulfill R2 and PROJECT.md requirements, strict mode should enforce higher pedagogical completeness:
     * Rule S-01: Mandatory step-by-step solution (`solution` or `detailed_solution`).
     * Rule S-02: Mandatory misconception warning (`misconception_warning` or `common_misconception_warning`).
     * Rule S-03: Mandatory explicit difficulty rating (`easy` | `medium` | `hard`).
   - Propagating `strict: bool` through `cli.py`, `core.py`, and `rules.py` provides concrete, measurable behavior where `exit_code == 1` if pedagogical scaffolding is missing.

4. **Premise 4 (Regression Prevention)**:
   - Observation 4 proves that existing tests only tested `python -m src.validator.cli`.
   - Adding `test_packaging_and_cli.py` with tests for console script execution, external importability, and strict mode semantics guarantees that these packaging defects cannot silently regress.

---

## 3. Caveats

1. **Read-Only Scope**:
   In accordance with Explorer constraints, no source code or configuration files were modified during this investigation. Implementation must be performed by the designated fixer agent.
2. **Reviewer 2 Lexical Scanner Findings**:
   Reviewer 2 also identified missing keywords in `LATEX_CONTROL_PREFIXES` (e.g. `\ne`, `\not`, `\bm`, `\tr`, `\ref`) and ungradable `fill_in_the_blank` items. Those are within the scope of Explorer 1 and Explorer 2, and are accounted for in our test strategy.

---

## 4. Conclusion

The packaging and CLI failures in Milestone 1 have a clear, localized root cause and a low-risk, backward-compatible solution:
1. Update `pyproject.toml`:
   - Add `[tool.setuptools.packages.find] where = ["src"]`
   - Point `validate-course` to `"validator.cli:main"`
   - Add `pythonpath = [".", "src"]` to `[tool.pytest.ini_options]`
2. Replace all `from src.validator.X import Y` statements across the 7 modules in `src/validator/` with relative imports `from .X import Y`.
3. Implement `--strict` semantics in `rules.py` (`check_strict_rules`), threading `strict` through `core.py` and `cli.py`.
4. Add automated tests in `tests/validator/test_packaging_and_cli.py` to verify console script execution, import isolation, and `--strict` enforcement.

The complete implementation specification and exact before/after code snippets are documented in:
`g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_m1_fix_packaging\packaging_fix_plan.md`

---

## 5. Verification Method

Once implemented, the reviewer or implementer can independently verify all fixes using the following commands:

1. **Reinstall Package in Editable Mode**:
   ```bash
   pip install -e . --no-deps
   ```
2. **Verify Entry Point Directly**:
   ```powershell
   validate-course courses/fixtures/28_valid_complete_course.json
   ```
   *Expected: Exit code 0, prints `VALID: Course 'demo' passed all validation rules.`*
3. **Verify Entry Point from External Directory**:
   ```powershell
   cd C:\Users\augus; validate-course "G:\Mi unidad\Competence_analyser\courses\fixtures\28_valid_complete_course.json"
   ```
   *Expected: Exit code 0 without `ModuleNotFoundError`.*
4. **Verify Strict Mode**:
   ```powershell
   validate-course --strict courses/fixtures/28_valid_complete_course.json
   ```
   *Expected: Exit code 0.*
5. **Run Full Validator Test Suite**:
   ```bash
   python -m pytest tests/validator -v
   ```
   *Expected: 100% tests pass.*
