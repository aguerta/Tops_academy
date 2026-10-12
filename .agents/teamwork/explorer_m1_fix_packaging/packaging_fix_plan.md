# Packaging & CLI Remediation Plan (Milestone 1)

**Author**: Explorer 3 (`explorer_m1_fix_packaging`)  
**Date**: 2026-10-11T01:40:00Z  
**Target Milestone**: Milestone 1 (Remediation Phase)  
**Parent Orchestrator**: `84948f37-b77a-4675-a1cb-6a3b8a288462`  

---

## 1. Executive Summary

Milestone 1 implements 16 course validation rules, but suffers from packaging defects and CLI omissions identified during review:
1. **Broken Console Script Entrypoint**: `validate-course` terminates with `ModuleNotFoundError: No module named 'src'` because setuptools packages the directory under `src/` as `validator`, whereas `pyproject.toml` registered `src.validator.cli:main`.
2. **Broken External Importability**: All 7 Python modules within `src/validator/` use hardcoded absolute imports (`from src.validator.X import Y`). When imported outside the repo root or from an installed site-packages environment, importing `validator` crashes with `ModuleNotFoundError: No module named 'src'`.
3. **Facade `--strict` CLI Flag**: The CLI accepts `--strict`, but ignores it; neither `core.py` nor `rules.py` implements strict semantics.
4. **Missing Packaging Tests**: No automated test in the repository executes the installed `validate-course` entry point or tests module importability from external working directories.

This document provides the complete, file-by-file specification to resolve all packaging and CLI defects.

---

## 2. Root Cause Analysis

### 2.1 Package Discovery and Entrypoint Mismatch
- **Observation**:
  `pyproject.toml` specifies:
  ```toml
  [project.scripts]
  validate-course = "src.validator.cli:main"
  ```
  without declaring `[tool.setuptools.packages.find]`.
- **Mechanism**:
  In a standard `src/` layout, `setuptools` discovers packages nested in `src/`. Here, `setuptools.find_packages("src")` finds `['validator']`. When setuptools builds and installs the package, the installed top-level package is `validator`, **not** `src`.
  When a user runs `validate-course`, the setuptools launcher executes:
  ```python
  from src.validator.cli import main
  ```
  Because `src` does not exist in site-packages, Python raises `ModuleNotFoundError: No module named 'src'`.
- **Remedy**:
  Configure `[tool.setuptools.packages.find] where = ["src"]` and point the script entry point to `validator.cli:main`.

### 2.2 Internal Absolute Import Pollution
- **Observation**:
  `src/validator/__init__.py`, `cli.py`, `core.py`, `lexical_scanner.py`, `schema_validator.py`, `rules.py`, and `psychometric_checker.py` all use `from src.validator.X import Y`.
- **Mechanism**:
  When `validator` is installed in `site-packages`, `sys.modules['validator']` is loaded. Any internal import attempting `from src.validator...` looks for a top-level package named `src`, which does not exist in site-packages.
- **Remedy**:
  Convert all internal imports across `src/validator/*.py` to relative imports (`from .X import Y`).
  Relative imports are completely agnostic to whether the package is loaded as `validator` or `src.validator`.

### 2.3 Unused `--strict` Flag
- **Observation**:
  `cli.py` passes `strict=args.strict` to `run_validation(target_path, strict=args.strict)`. Inside `run_validation`, `validate_course(target_path)` is called without the `strict` argument. Furthermore, `validate_course` and `validate_course_content` in `core.py` do not accept `strict`.
- **Mechanism**:
  The flag was implemented as a CLI parameter stub without underlying semantic rules.
- **Remedy**:
  Thread `strict: bool = False` through `run_validation`, `validate_course`, and `validate_course_content`. Define and implement strict pedagogical and metadata rules (Rules S-01, S-02, S-03).

---

## 3. Detailed Remediation Specification

### 3.1 `pyproject.toml`
**File**: `g:\Mi unidad\Competence_analyser\pyproject.toml`

#### Target Changes:
1. Register `[tool.setuptools.packages.find]` with `where = ["src"]`.
2. Update console script to `validate-course = "validator.cli:main"`.
3. Update `pythonpath` in `[tool.pytest.ini_options]` to `[".", "src"]`.

#### Proposed Replacement Content:
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "competence-analyser"
version = "1.0.0"
description = "Top's Academy Course and Validator System"
authors = [{ name = "Top's Academy Team" }]
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "jsonschema>=4.20.0",
    "pydantic>=2.0.0",
    "sympy>=1.12",
]

[project.scripts]
validate-course = "validator.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = [".", "src"]
```

---

### 3.2 Internal Relative Imports Across `src/validator/`

#### A. `src/validator/__init__.py`
**File**: `g:\Mi unidad\Competence_analyser\src\validator\__init__.py`  
**Lines 2-7**:
```python
# BEFORE
from src.validator.models import ValidationError, ValidationResult
from src.validator.core import validate_course, validate_course_content
from src.validator.lexical_scanner import scan_lexical
from src.validator.schema_validator import validate_schema, COURSE_SCHEMA
from src.validator.rules import check_semantic_rules
from src.validator.psychometric_checker import check_psychometrics

# AFTER
from .models import ValidationError, ValidationResult
from .core import validate_course, validate_course_content
from .lexical_scanner import scan_lexical
from .schema_validator import validate_schema, COURSE_SCHEMA
from .rules import check_semantic_rules
from .psychometric_checker import check_psychometrics
```

#### B. `src/validator/cli.py`
**File**: `g:\Mi unidad\Competence_analyser\src\validator\cli.py`  
**Lines 20-21**:
```python
# BEFORE
from src.validator.core import validate_course
from src.validator.models import ValidationResult

# AFTER
from .core import validate_course
from .models import ValidationResult
```

#### C. `src/validator/core.py`
**File**: `g:\Mi unidad\Competence_analyser\src\validator\core.py`  
**Lines 8-12**:
```python
# BEFORE
from src.validator.models import ValidationError, ValidationResult
from src.validator.lexical_scanner import scan_lexical
from src.validator.schema_validator import validate_schema
from src.validator.rules import check_semantic_rules
from src.validator.psychometric_checker import check_psychometrics

# AFTER
from .models import ValidationError, ValidationResult
from .lexical_scanner import scan_lexical
from .schema_validator import validate_schema
from .rules import check_semantic_rules
from .psychometric_checker import check_psychometrics
```

#### D. `src/validator/lexical_scanner.py`
**File**: `g:\Mi unidad\Competence_analyser\src\validator\lexical_scanner.py`  
**Line 13**:
```python
# BEFORE
from src.validator.models import ValidationError

# AFTER
from .models import ValidationError
```

#### E. `src/validator/schema_validator.py`
**File**: `g:\Mi unidad\Competence_analyser\src\validator\schema_validator.py`  
**Line 9**:
```python
# BEFORE
from src.validator.models import ValidationError

# AFTER
from .models import ValidationError
```

#### F. `src/validator/rules.py`
**File**: `g:\Mi unidad\Competence_analyser\src\validator\rules.py`  
**Line 19**:
```python
# BEFORE
from src.validator.models import ValidationError

# AFTER
from .models import ValidationError
```

#### G. `src/validator/psychometric_checker.py`
**File**: `g:\Mi unidad\Competence_analyser\src\validator\psychometric_checker.py`  
**Line 12**:
```python
# BEFORE
from src.validator.models import ValidationError

# AFTER
from .models import ValidationError
```

---

### 3.3 `--strict` Flag Semantics & Implementation

#### Strict Mode Specification:
In standard mode (`strict=False`), questions must satisfy rules R-01 through R-16.
In strict mode (`strict=True`), questions must additionally satisfy strict pedagogical completeness criteria:
- **Rule S-01 (`ERR_STRICT_MISSING_SOLUTION`)**: Every question must provide a non-empty step-by-step `solution` or `detailed_solution`.
- **Rule S-02 (`ERR_STRICT_MISSING_MISCONCEPTION`)**: Every question must provide a non-empty `misconception_warning` or `common_misconception_warning`.
- **Rule S-03 (`ERR_STRICT_MISSING_DIFFICULTY`)**: Every question must declare an explicit, valid `difficulty` level (`"easy" | "medium" | "hard"`).

#### Code Changes in `src/validator/rules.py`:
Add function `check_strict_rules`:
```python
def check_strict_rules(data: dict[str, Any]) -> list[ValidationError]:
    """Evaluates strict-mode criteria (Pass 3): verifies mandatory solutions,

    misconception warnings, and valid difficulty levels for every question.
    """
    errors: list[ValidationError] = []
    questions = data.get("questions", [])
    if not isinstance(questions, list):
        return errors

    for q in questions:
        if not isinstance(q, dict):
            continue
        q_id = q.get("id", "UNKNOWN")

        # S-01: Step-by-step solution required
        sol = q.get("solution") or q.get("detailed_solution")
        if not sol or not isinstance(sol, str) or not sol.strip():
            errors.append(ValidationError(
                rule_id="S-01",
                code="ERR_STRICT_MISSING_SOLUTION",
                message=f"Question '{q_id}' must provide a non-empty step-by-step 'solution' or 'detailed_solution' in strict mode",
                item_id=q_id
            ))

        # S-02: Misconception warning required
        misc = q.get("misconception_warning") or q.get("common_misconception_warning")
        if not misc or not isinstance(misc, str) or not misc.strip():
            errors.append(ValidationError(
                rule_id="S-02",
                code="ERR_STRICT_MISSING_MISCONCEPTION",
                message=f"Question '{q_id}' must provide a non-empty 'misconception_warning' in strict mode",
                item_id=q_id
            ))

        # S-03: Explicit difficulty required
        diff = q.get("difficulty")
        if diff not in ("easy", "medium", "hard"):
            errors.append(ValidationError(
                rule_id="S-03",
                code="ERR_STRICT_MISSING_DIFFICULTY",
                message=f"Question '{q_id}' must specify a valid difficulty level ('easy', 'medium', 'hard') in strict mode",
                item_id=q_id
            ))

    return errors
```

#### Code Changes in `src/validator/core.py`:
Update signatures and pass `strict`:
```python
def validate_course_content(
    raw_text: str,
    file_path: str | None = None,
    strict: bool = False
) -> ValidationResult:
    ...
    all_errors = schema_errors + semantic_errors + psychometric_errors

    if strict and parsed_data is not None and isinstance(parsed_data, dict):
        from .rules import check_strict_rules
        strict_errors = check_strict_rules(parsed_data)
        all_errors.extend(strict_errors)

    course_id = parsed_data.get("course_id")
    ...
    return ValidationResult(
        file_path=file_path,
        is_valid=(len(all_errors) == 0),
        errors=all_errors,
        ...
    )


def validate_course(
    path_or_text: Union[str, Path],
    is_raw_text: bool = False,
    strict: bool = False
) -> ValidationResult:
    """Validates a course by file path or directly from raw text string."""
    if is_raw_text:
        return validate_course_content(str(path_or_text), file_path=None, strict=strict)

    file_path = Path(path_or_text)
    if not file_path.exists():
        raise FileNotFoundError(f"Course file not found: {file_path}")
    if not file_path.is_file():
        raise IsADirectoryError(f"Specified path is not a file: {file_path}")

    raw_text = file_path.read_text(encoding="utf-8")
    return validate_course_content(raw_text, file_path=str(file_path), strict=strict)
```

#### Code Changes in `src/validator/cli.py`:
```python
def format_cli_output(result: ValidationResult, strict: bool = False) -> str:
    """Formats human-readable diagnostic messages for CLI output."""
    lines: list[str] = []
    file_name = result.file_path or "course.json"

    if result.is_valid:
        course_name = result.course_id or "course"
        mode_suffix = " (strict mode)" if strict else ""
        lines.append(f"VALID: Course '{course_name}' passed all validation rules{mode_suffix}.")
    else:
        lines.append(f"[VALIDATION FAILURE] {file_name}")
        for err in result.errors:
            lines.append(f"  {err.formatted()}")
        err_count = len(result.errors)
        lines.append(f"FAILED: {err_count} {'error' if err_count == 1 else 'errors'} detected.")

    return "\n".join(lines)


def run_validation(target_path: Path, strict: bool = False) -> list[ValidationResult]:
    """Runs validation on a single file or recursively on a directory."""
    results: list[ValidationResult] = []

    if target_path.is_file():
        results.append(validate_course(target_path, strict=strict))
    elif target_path.is_dir():
        json_files = sorted(list(target_path.glob("*.json")))
        if not json_files:
            raise FileNotFoundError(f"No JSON course files found in directory: {target_path}")
        for jf in json_files:
            results.append(validate_course(jf, strict=strict))
    else:
        raise FileNotFoundError(f"Path does not exist: {target_path}")

    return results


def main(argv: Sequence[str] | None = None) -> int:
    ...
    # Line 86:
    results = run_validation(target_path, strict=args.strict)
    ...
    # Line 105:
    for r in results:
        print(format_cli_output(r, strict=args.strict))
    ...
```

---

## 4. Automated Test Specification

Create `tests/validator/test_packaging_and_cli.py` covering:
1. **Console Script Entry Point (`validate-course`)**:
   Runs the installed `validate-course` executable and/or `python -m validator.cli` on fixture 28, verifying exit code 0 and proper success messaging.
2. **External Module Import Isolation**:
   Spawns a subprocess from an external temporary directory with `sys.path` containing `src/`, executing `import validator; from validator import validate_course` to verify zero `src` dependencies.
3. **Strict Flag Semantics**:
   - Asserts fixture 28 passes with `--strict` (exit code 0).
   - Asserts a fixture with missing `solution` or `misconception_warning` passes in standard mode (exit code 0) but fails with `--strict` (exit code 1, emitting `ERR_STRICT_MISSING_SOLUTION` / `ERR_STRICT_MISSING_MISCONCEPTION`).
4. **Dual Module Invocation Compatibility**:
   Asserts both `python -m validator.cli` and `python -m src.validator.cli` execute cleanly from repository root.

```python
"""Automated tests for Packaging, Entry Points, Import Isolation, and Strict Mode."""
import copy
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import pytest

from validator.core import validate_course, validate_course_content

FIXTURES_DIR = Path(__file__).resolve().parent.parent.parent / "courses" / "fixtures"


def test_import_validator_outside_repo(tmp_path: Path) -> None:
    """Verifies that validator can be imported from an external working directory."""
    repo_src = str(Path(__file__).resolve().parent.parent.parent / "src")
    test_script = f"""
import sys
sys.path.insert(0, {repo_src!r})
import validator
from validator.core import validate_course
from validator.cli import main
print("IMPORT_OK")
"""
    proc = subprocess.run(
        [sys.executable, "-c", test_script],
        cwd=str(tmp_path),
        capture_output=True,
        text=True
    )
    assert proc.returncode == 0, f"External import failed: {proc.stderr}"
    assert "IMPORT_OK" in proc.stdout


def test_cli_entrypoint_execution() -> None:
    """Verifies that validate-course console script or module executes fixture 28."""
    fixture_path = FIXTURES_DIR / "28_valid_complete_course.json"

    # Test via module entrypoint
    proc_module = subprocess.run(
        [sys.executable, "-m", "validator.cli", str(fixture_path)],
        capture_output=True,
        text=True
    )
    assert proc_module.returncode == 0
    assert "VALID" in proc_module.stdout

    # Test via console script binary if present in environment
    bin_path = shutil.which("validate-course")
    if bin_path:
        proc_bin = subprocess.run([bin_path, str(fixture_path)], capture_output=True, text=True)
        assert proc_bin.returncode == 0
        assert "VALID" in proc_bin.stdout


def test_strict_flag_semantics() -> None:
    """Verifies that --strict enforces solutions and misconception warnings."""
    fixture_path = FIXTURES_DIR / "28_valid_complete_course.json"
    data = json.loads(fixture_path.read_text(encoding="utf-8"))

    # Base valid fixture passes both modes
    assert validate_course_content(json.dumps(data), strict=False).is_valid is True
    assert validate_course_content(json.dumps(data), strict=True).is_valid is True

    # Mutate Q-001 by removing solution
    data_no_sol = copy.deepcopy(data)
    data_no_sol["questions"][0].pop("detailed_solution", None)
    data_no_sol["questions"][0].pop("solution", None)

    # Standard mode: valid
    res_std = validate_course_content(json.dumps(data_no_sol), strict=False)
    assert res_std.is_valid is True

    # Strict mode: invalid with ERR_STRICT_MISSING_SOLUTION
    res_strict = validate_course_content(json.dumps(data_no_sol), strict=True)
    assert res_strict.is_valid is False
    assert any(e.code == "ERR_STRICT_MISSING_SOLUTION" for e in res_strict.errors)

    # Test via CLI subprocess
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
        tf.write(json.dumps(data_no_sol))
        tmp_file = tf.name
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "validator.cli", "--strict", tmp_file],
            capture_output=True,
            text=True
        )
        assert proc.returncode == 1
        assert "ERR_STRICT_MISSING_SOLUTION" in proc.stdout
    finally:
        Path(tmp_file).unlink(missing_ok=True)
```

---

## 5. Verification Runbook for Implementer

To apply and verify these fixes:
1. Apply the edits specified in Section 3 to `pyproject.toml`, `src/validator/__init__.py`, `cli.py`, `core.py`, `rules.py`, `lexical_scanner.py`, `schema_validator.py`, and `psychometric_checker.py`.
2. Reinstall the package in editable mode:
   ```bash
   pip install -e . --no-deps
   ```
3. Run the automated validator test suite:
   ```bash
   python -m pytest tests/validator -v
   ```
4. Test the console script entry point directly:
   ```powershell
   validate-course courses/fixtures/28_valid_complete_course.json
   ```
5. Test from an external directory:
   ```powershell
   cd C:\Users\augus; validate-course "G:\Mi unidad\Competence_analyser\courses\fixtures\28_valid_complete_course.json"
   ```
6. Verify `--strict` flag behavior:
   ```powershell
   validate-course --strict courses/fixtures/28_valid_complete_course.json
   ```
