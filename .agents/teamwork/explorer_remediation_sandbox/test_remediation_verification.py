"""Verification Test Suite for Remediated Sandbox Implementation.

Directly tests proposed_sandbox.py against:
1. All standard security restrictions (banned modules, builtins, dunder attributes, timeout, memory bomb)
2. Legitimate whitelisted math functionality
3. The 6 adversarial vulnerabilities identified by Challenger 1, verifying that ALL of them
   are now completely blocked by AST validation and/or runtime isolation.
"""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
import pytest

# Put current directory and repo root on sys.path
THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parent.parent.parent
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"

for p in [str(THIS_DIR), str(SKILL_DIR), str(REPO_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import proposed_sandbox as sandbox
from proposed_sandbox import (
    execute_sandbox_instance,
    execute_sandbox_batch,
    validate_code_ast,
    SandboxExecutionError,
    SandboxTimeoutError,
    SecurityViolationError,
)


class TestStandardSandboxRestrictions:
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
        code = "def generate(rng):\n    while True:\n        pass\n"
        t0 = time.time()
        with pytest.raises(SandboxTimeoutError):
            execute_sandbox_instance(code, seed=42, timeout=2.0)
        elapsed = time.time() - t0
        assert 1.8 <= elapsed <= 3.5, f"Timeout took {elapsed:.2f}s, expected ~2.0s"

    def test_memory_bomb_handled_gracefully(self):
        code = "def generate(rng):\n    big = [0] * (10**12)\n    return {'vars': {}, 'correct': 1, 'distractors': []}"
        with pytest.raises((SandboxExecutionError, SandboxTimeoutError)):
            execute_sandbox_instance(code, seed=42, timeout=2.0)


class TestLegitimateFunctionality:
    def test_all_whitelisted_math_libraries(self):
        code = """
def generate(rng):
    import math
    import fractions
    import statistics
    import sympy
    import numpy as np
    import scipy.stats as stats
    import random
    from engine.render import fmt, latex_frac

    v_math = math.sqrt(49.0)
    v_frac = fractions.Fraction(1, 3) + fractions.Fraction(1, 6)
    v_stat = statistics.mean([2, 4, 6])
    x = sympy.Symbol('x')
    v_sym = str(sympy.diff(x**3, x))
    v_np = int(np.dot([2, 3], [4, 5]))
    v_sci = round(float(stats.norm.cdf(0.0)), 4)
    v_rng = rng.randint(1000, 9999)
    v_fmt = fmt(v_frac)

    return {
        'vars': {
            'math': v_math,
            'frac': str(v_frac),
            'stat': v_stat,
            'sym': v_sym,
            'np': v_np,
            'sci': v_sci,
            'rng': v_rng,
            'fmt': v_fmt,
        },
        'correct': v_np,
        'distractors': [v_np + 1, v_np - 1, v_np + 2, v_np - 2, v_np + 3, v_np - 3],
    }
"""
        res = execute_sandbox_instance(code, seed=123, timeout=5.0)
        assert res["vars"]["math"] == 7.0
        assert res["vars"]["frac"] == "1/2"
        assert res["vars"]["stat"] == 4
        assert res["vars"]["sym"] == "3*x**2"
        assert res["vars"]["np"] == 23
        assert res["vars"]["sci"] == 0.5
        assert isinstance(res["vars"]["rng"], int)

    def test_rng_determinism(self):
        code = """
def generate(rng):
    val = rng.randint(1, 1000000)
    lst = [rng.random() for _ in range(5)]
    return {'vars': {'val': val, 'lst': lst}, 'correct': val, 'distractors': []}
"""
        r1 = execute_sandbox_instance(code, seed=999, timeout=5.0)
        r2 = execute_sandbox_instance(code, seed=999, timeout=5.0)
        assert r1 == r2, "Identical seeds must yield identical results"

        r3 = execute_sandbox_instance(code, seed=1000, timeout=5.0)
        assert r1 != r3, "Different seeds must yield different results"


class TestAdversarialVulnerabilitiesRemediated:
    """Verifies that all 6 adversarial vulnerabilities are now completely blocked."""

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
