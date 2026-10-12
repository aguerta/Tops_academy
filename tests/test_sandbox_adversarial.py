"""Empirical Adversarial Security & Stress Testing Suite for Sandbox.py.

Authored by Challenger Agent (challenger_phase1_sandbox_security).
Empirically stress-tests AST validation, subprocess isolation, timeouts,
memory bounds, whitelisted math modules, determinism, and potential escape exploits.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict

import pytest

# Ensure repository root and skill directories are on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
import sys
for p in [str(SKILL_DIR), str(REPO_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from engine.sandbox import (
    execute_sandbox_instance,
    execute_sandbox_batch,
    validate_code_ast,
    warm_up_sandbox,
    SandboxExecutionError,
    SandboxTimeoutError,
    SecurityViolationError,
)


# =============================================================================
# SECTION 1: Standard Security Verification (Expected to PASS / Block)
# =============================================================================

class TestStandardSandboxRestrictions:
    """Verifies that standard attacks specified in R3 are rejected by AST validator."""

    @pytest.mark.parametrize("mod", [
        "os", "sys", "subprocess", "socket", "urllib", "requests",
        "http", "shutil", "pathlib", "ctypes", "pickle"
    ])
    def test_direct_banned_imports_rejected(self, mod: str):
        code = f"import {mod}\ndef generate(rng): return {{}}"
        with pytest.raises(SecurityViolationError):
            validate_code_ast(code)

    @pytest.mark.parametrize("mod", [
        "os", "sys", "subprocess", "socket", "urllib", "pathlib", "ctypes"
    ])
    def test_banned_from_imports_rejected(self, mod: str):
        code = f"from {mod} import something\ndef generate(rng): return {{}}"
        with pytest.raises(SecurityViolationError):
            validate_code_ast(code)

    @pytest.mark.parametrize("banned_fn", [
        "open('test.txt')",
        "eval('1 + 1')",
        "exec('a = 1')",
        "compile('x = 1', '<test>', 'exec')",
        "__import__('os')",
        "globals()",
        "locals()",
        "vars()",
        "input()",
        "breakpoint()",
        "exit()",
        "quit()",
    ])
    def test_banned_builtins_rejected(self, banned_fn: str):
        code = f"def generate(rng):\n    {banned_fn}\n    return {{}}"
        with pytest.raises(SecurityViolationError):
            validate_code_ast(code)

    @pytest.mark.parametrize("dunder_expr", [
        "().__class__",
        "[].__class__",
        "(1).__class__.__bases__",
        "().__class__.__base__.__subclasses__()",
        "rng.__dict__",
        "generate.__globals__",
        "generate.__code__",
    ])
    def test_dunder_attribute_traversal_rejected(self, dunder_expr: str):
        code = f"def generate(rng):\n    val = {dunder_expr}\n    return {{'vars': {{'v': str(val)}}}}"
        with pytest.raises(SecurityViolationError):
            validate_code_ast(code)

    def test_infinite_loop_timeout_clean_termination(self):
        """Resource exhaustion via infinite loop must trigger 2.0s timeout and exit cleanly."""
        code = "def generate(rng):\n    while True:\n        pass\n"
        t0 = time.time()
        with pytest.raises(SandboxTimeoutError):
            execute_sandbox_instance(code, seed=42, timeout=2.0)
        elapsed = time.time() - t0
        assert 1.8 <= elapsed <= 3.5, f"Timeout took {elapsed:.2f}s, expected ~2.0s"

    def test_memory_bomb_handled_gracefully(self):
        """Excessive memory allocation must not corrupt host process or hang indefinitely."""
        code = "def generate(rng):\n    big = [0] * (10**12)\n    return {'vars': {}, 'correct': 1, 'distractors': []}"
        with pytest.raises((SandboxExecutionError, SandboxTimeoutError)):
            execute_sandbox_instance(code, seed=42, timeout=2.0)


# =============================================================================
# SECTION 2: Legitimate Whitelisted Math Libraries & Determinism
# =============================================================================

class TestLegitimateFunctionality:
    """Verifies legitimate whitelisted math libraries execute and RNG is deterministic."""

    def test_all_whitelisted_math_libraries(self):
        """math, fractions, statistics, sympy, numpy, scipy.stats, random with rng."""
        warm_up_sandbox(timeout=60.0)
        code = """
def generate(rng):
    import math
    import fractions
    import statistics
    import sympy
    import numpy as np
    import scipy.stats as stats
    import random

    v_math = math.sqrt(49.0)
    v_frac = fractions.Fraction(1, 3) + fractions.Fraction(1, 6)
    v_stat = statistics.mean([2, 4, 6])
    x = sympy.Symbol('x')
    v_sym = str(sympy.diff(x**3, x))
    v_np = int(np.dot([2, 3], [4, 5]))
    v_sci = round(float(stats.norm.cdf(0.0)), 4)
    v_rng = rng.randint(1000, 9999)

    return {
        'vars': {
            'math': v_math,
            'frac': str(v_frac),
            'stat': v_stat,
            'sym': v_sym,
            'np': v_np,
            'sci': v_sci,
            'rng': v_rng,
        },
        'correct': v_np,
        'distractors': [v_np + 1, v_np - 1, v_np + 2, v_np - 2, v_np + 3, v_np - 3],
    }
"""
        res = execute_sandbox_instance(code, seed=123, timeout=30.0)
        assert res["vars"]["math"] == 7.0
        assert res["vars"]["frac"] == "1/2"
        assert res["vars"]["stat"] == 4
        assert res["vars"]["sym"] == "3*x**2"
        assert res["vars"]["np"] == 23
        assert res["vars"]["sci"] == 0.5
        assert isinstance(res["vars"]["rng"], int)

    def test_rng_determinism(self):
        """Identical seed must produce identical output; distinct seeds must produce distinct outputs."""
        code = """
def generate(rng):
    val = rng.randint(1, 1000000)
    lst = [rng.random() for _ in range(5)]
    return {'vars': {'val': val, 'lst': lst}, 'correct': val, 'distractors': []}
"""
        r1 = execute_sandbox_instance(code, seed=999, timeout=3.0)
        r2 = execute_sandbox_instance(code, seed=999, timeout=3.0)
        assert r1 == r2, "Identical seeds must yield identical results"

        r3 = execute_sandbox_instance(code, seed=1000, timeout=3.0)
        assert r1 != r3, "Different seeds must yield different results"


# =============================================================================
# =============================================================================
# SECTION 3: Adversarial Vulnerabilities Remediated (0 Escapes)
# =============================================================================

class TestAdversarialVulnerabilitiesRemediated:
    """Verifies that all 6 adversarial vulnerabilities are now completely blocked (0 escapes)."""

    def test_vuln_1_fractions_sys_module_escape_blocked(self):
        """VULN 1: fractions.sys attribute traversal is blocked by AST validator and purged from runtime."""
        code = """
def generate(rng):
    import fractions
    sys_mod = fractions.sys
    os_mod = sys_mod.modules.get('os')
    return {'vars': {}, 'correct': 1, 'distractors': []}
"""
        with pytest.raises(SecurityViolationError, match="banned attribute 'sys'"):
            validate_code_ast(code)

        with pytest.raises(SecurityViolationError):
            execute_sandbox_instance(code, seed=42)

    def test_vuln_2_import_alias_sys_bypass_blocked(self):
        """VULN 2: 'from fractions import sys as safe_helper' is blocked because alias 'sys' is banned."""
        code = """
from fractions import sys as safe_helper

def generate(rng):
    os_mod = safe_helper.modules.get('os')
    return {'vars': {}, 'correct': 1, 'distractors': []}
"""
        with pytest.raises(SecurityViolationError, match="banned symbol 'sys'"):
            validate_code_ast(code)

        with pytest.raises(SecurityViolationError):
            execute_sandbox_instance(code, seed=42)

    def test_vuln_3_engine_sandbox_reexport_command_execution_blocked(self):
        """VULN 3: 'import engine.sandbox as es' is blocked because only engine.render is permitted."""
        code = """
import engine.sandbox as es

def generate(rng):
    proc = es.subprocess.run(['cmd.exe', '/c', 'echo PWNED'], capture_output=True, text=True)
    return {'vars': {'stdout': proc.stdout.strip()}, 'correct': 1, 'distractors': []}
"""
        with pytest.raises(SecurityViolationError, match="engine.sandbox.*prohibited"):
            validate_code_ast(code)

        with pytest.raises(SecurityViolationError):
            execute_sandbox_instance(code, seed=42)

    def test_vuln_3b_bare_engine_import_blocked(self):
        """VULN 3b: Bare 'import engine' is also prohibited."""
        code = """
import engine

def generate(rng):
    return {'vars': {}, 'correct': 1, 'distractors': []}
"""
        with pytest.raises(SecurityViolationError, match="engine.*prohibited"):
            validate_code_ast(code)

    def test_vuln_4_operator_attrgetter_dunder_traversal_blocked(self):
        """VULN 4: fractions.operator.attrgetter is blocked by BANNED_NAMES (operator, attrgetter)."""
        code = """
def generate(rng):
    import fractions
    get_attr = fractions.operator.attrgetter
    return {'vars': {}, 'correct': 1, 'distractors': []}
"""
        with pytest.raises(SecurityViolationError):
            validate_code_ast(code)

        with pytest.raises(SecurityViolationError):
            execute_sandbox_instance(code, seed=42)

    def test_vuln_5_numpy_ctypeslib_access_blocked(self):
        """VULN 5: numpy.ctypeslib.ctypes is blocked by BANNED_NAMES (ctypeslib, ctypes)."""
        code = """
def generate(rng):
    import numpy as np
    ctypes_mod = np.ctypeslib.ctypes
    return {'vars': {}, 'correct': 1, 'distractors': []}
"""
        with pytest.raises(SecurityViolationError, match=r"banned attribute '(ctypes|ctypeslib)'"):
            validate_code_ast(code)

        with pytest.raises(SecurityViolationError):
            execute_sandbox_instance(code, seed=42)

    def test_vuln_6_global_random_deterministic_with_seed(self):
        """VULN 6: Global random module is seeded, guaranteeing deterministic results."""
        code = """
def generate(rng):
    import random
    return {'vars': {'r': random.randint(1, 10**9)}, 'correct': 1, 'distractors': []}
"""
        r1 = execute_sandbox_instance(code, seed=777)
        r2 = execute_sandbox_instance(code, seed=777)
        assert r1 == r2, "Identical seeds must yield identical results even when using global random module"

        r3 = execute_sandbox_instance(code, seed=888)
        assert r1 != r3, "Different seeds must yield different results"

    def test_relative_import_blocked(self):
        """Relative imports like 'from . import foo' must be blocked."""
        code = """
from . import render

def generate(rng):
    return {'vars': {}, 'correct': 1, 'distractors': []}
"""
        with pytest.raises(SecurityViolationError, match="Relative imports are prohibited"):
            validate_code_ast(code)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
