import sys
import os
import time

skill_path = os.path.abspath(".agents/skills/content-to-course")
if skill_path not in sys.path:
    sys.path.insert(0, skill_path)

from engine.sandbox import (
    validate_code_ast,
    get_safe_builtins,
    serialize_for_json,
    SandboxTimeoutError,
    SecurityViolationError,
    SandboxExecutionError,
)

class LazySandboxGlobals(dict):
    """Dictionary subclass that lazily imports heavy mathematical libraries on first access."""

    @staticmethod
    def _load_numpy():
        import numpy as np
        return np

    @staticmethod
    def _load_sympy():
        import sympy
        return sympy

    @staticmethod
    def _load_scipy():
        import scipy
        import scipy.stats
        return scipy

    @classmethod
    def get_loaders(cls):
        return {
            "numpy": cls._load_numpy,
            "np": cls._load_numpy,
            "sympy": cls._load_sympy,
            "scipy": cls._load_scipy,
        }

    def __missing__(self, key: str):
        loaders = self.get_loaders()
        if key in loaders:
            mod = loaders[key]()
            self[key] = mod
            if key in ("numpy", "np"):
                self["numpy"] = mod
                self["np"] = mod
            return mod
        raise KeyError(key)

    def __contains__(self, key: object) -> bool:
        if super().__contains__(key):
            return True
        return key in self.get_loaders()

    def get(self, key: str, default=None):
        if super().__contains__(key):
            return super().__getitem__(key)
        loaders = self.get_loaders()
        if key in loaders:
            return self.__missing__(key)
        return default


def build_lazy_sandbox_globals():
    import math
    import fractions
    import statistics
    import random
    from engine.render import bmatrix, table_array, fmt, latex_frac

    # Sanitize module leaks if present
    if hasattr(fractions, "sys"):
        try:
            del fractions.sys
        except Exception:
            pass
    if hasattr(statistics, "sys"):
        try:
            del statistics.sys
        except Exception:
            pass

    env = LazySandboxGlobals({
        "__builtins__": get_safe_builtins(),
        "math": math,
        "fractions": fractions,
        "Fraction": fractions.Fraction,
        "statistics": statistics,
        "random": random,
        "bmatrix": bmatrix,
        "table_array": table_array,
        "fmt": fmt,
        "latex_frac": latex_frac,
    })
    return env


def run_test(name, code, expected_check):
    import random
    env = build_lazy_sandbox_globals()
    rng = random.Random(42)
    t0 = time.perf_counter()
    compiled = compile(code, "<sandbox>", "exec")
    exec(compiled, env)
    res = env["generate"](rng)
    dt = time.perf_counter() - t0
    check_ok = expected_check(res)
    print(f"[{'PASS' if check_ok else 'FAIL'}] {name:40s} | took: {dt*1000:6.1f}ms | result: {res}")
    return check_ok

print("=== Running Comprehensive Lazy Sandbox Tests ===")

# Test 1: rng only
run_test("1. Pure RNG", 
    "def generate(rng): return {'v': rng.randint(1, 100)}", 
    lambda r: 1 <= r['v'] <= 100)

# Test 2: Global np without import
run_test("2. Global np without import", 
    "def generate(rng): return {'v': int(np.sum([1, 2, 3]))}", 
    lambda r: r['v'] == 6)

# Test 3: Global numpy without import
run_test("3. Global numpy without import", 
    "def generate(rng): return {'v': int(numpy.sum([4, 5, 6]))}", 
    lambda r: r['v'] == 15)

# Test 4: Global sympy without import
run_test("4. Global sympy without import", 
    "def generate(rng): x = sympy.Symbol('x'); return {'v': str(sympy.diff(x**2, x))}", 
    lambda r: r['v'] == "2*x")

# Test 5: Global scipy without import
run_test("5. Global scipy without import", 
    "def generate(rng): return {'v': round(float(scipy.stats.norm.cdf(0)), 4)}", 
    lambda r: r['v'] == 0.5)

# Test 6: Explicit import numpy
run_test("6. Explicit import numpy", 
    "def generate(rng): import numpy as np2; return {'v': int(np2.prod([2, 3, 4]))}", 
    lambda r: r['v'] == 24)

# Test 7: Explicit import sympy
run_test("7. Explicit import sympy", 
    "def generate(rng): import sympy as sp; y = sp.Symbol('y'); return {'v': str(sp.diff(y**3, y))}", 
    lambda r: r['v'] == "3*y**2")

# Test 8: Explicit import scipy.stats
run_test("8. Explicit import scipy.stats", 
    "def generate(rng): import scipy.stats as st; return {'v': float(st.norm.cdf(0))}", 
    lambda r: r['v'] == 0.5)

# Test 9: render helper
run_test("9. Render helper bmatrix", 
    "def generate(rng): return {'v': bmatrix([[1, 2], [3, 4]])}", 
    lambda r: "\\begin{bmatrix}" in r['v'])
