#!/usr/bin/env python3
"""Top's Academy - Deterministic Test Runner.

Automatically resolves and invokes the project's virtual environment (.venv)
regardless of whether the calling shell or agent invokes it via the global Python
or the venv Python.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# Force UTF-8 encoding on standard streams
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = Path(__file__).resolve().parent
VENV_PYTHON = ROOT_DIR / ".venv" / "Scripts" / "python.exe"
VENV_PYTEST = ROOT_DIR / ".venv" / "Scripts" / "pytest.exe"


def main() -> int:
    args = sys.argv[1:]

    # Check if we are already running inside the project's .venv
    current_executable = Path(sys.executable).resolve()
    is_in_project_venv = False
    if VENV_PYTHON.exists() and current_executable == VENV_PYTHON.resolve():
        is_in_project_venv = True

    # If running inside the venv, run pytest in-process or via pytest module
    if is_in_project_venv:
        try:
            import pytest
            return pytest.main(args)
        except ImportError:
            pass

    # If not in project venv, delegate to the venv python / pytest
    target_cmd: list[str] = []
    if VENV_PYTHON.exists():
        target_cmd = [str(VENV_PYTHON), "-m", "pytest", *args]
    elif VENV_PYTEST.exists():
        target_cmd = [str(VENV_PYTEST), *args]
    else:
        # Fallback to current python
        target_cmd = [sys.executable, "-m", "pytest", *args]

    # Set PYTHONPATH to include root and src
    env = os.environ.copy()
    current_pythonpath = env.get("PYTHONPATH", "")
    additional_paths = [str(ROOT_DIR), str(ROOT_DIR / "src")]
    env["PYTHONPATH"] = (
        os.pathsep.join(additional_paths) + (os.pathsep + current_pythonpath if current_pythonpath else "")
    )
    env["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(target_cmd, env=env)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
