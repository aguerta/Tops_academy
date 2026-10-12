import sys
import os
import time
import pytest

# Put current teamwork directory first in sys.path so we import proposed_sandbox
teamwork_dir = os.path.abspath(".agents/teamwork/explorer_remediation_timing")
skill_dir = os.path.abspath(".agents/skills/content-to-course")
sys.path.insert(0, teamwork_dir)
sys.path.insert(0, skill_dir)

import proposed_sandbox as ps

print("=== Running Validation Suite on proposed_sandbox.py ===")

# Test 1: Determinism
code_simple = """
def generate(rng):
    a = rng.randint(10, 100)
    b = rng.randint(1, 5)
    return {"vars": {"a": a, "b": b}, "correct": a + b, "distractors": []}
"""

t0 = time.perf_counter()
r1 = ps.execute_sandbox_instance(code_simple, seed=42)
r2 = ps.execute_sandbox_instance(code_simple, seed=42)
r3 = ps.execute_sandbox_instance(code_simple, seed=43)
dt_3runs = time.perf_counter() - t0
assert r1 == r2, "Deterministic seed failed (r1 != r2)"
assert r1 != r3, "Distinct seeds produced same result (r1 == r3)"
print(f"[PASS] Determinism test passed: 3 instances in {dt_3runs*1000:.1f}ms (average {dt_3runs/3*1000:.1f}ms/instance)")

# Test 2: Timeout enforcement on infinite loop
infinite_loop = """
def generate(rng):
    while True:
        pass
"""
t0 = time.perf_counter()
try:
    ps.execute_sandbox_instance(infinite_loop, seed=1, timeout=1.0)
    assert False, "Infinite loop did not raise SandboxTimeoutError"
except ps.SandboxTimeoutError as e:
    dt_timeout = time.perf_counter() - t0
    print(f"[PASS] Infinite loop timed out in {dt_timeout*1000:.1f}ms as expected ({e})")

# Test 3: All math libraries (sympy, scipy, numpy, fractions, stats)
heavy_math = """
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
        'distractors': [v_np + 1, v_np - 1],
    }
"""
t0 = time.perf_counter()
res_math = ps.execute_sandbox_instance(heavy_math, seed=123)
dt_math = time.perf_counter() - t0
assert res_math["vars"]["math"] == 7.0
assert res_math["vars"]["frac"] == "1/2"
assert res_math["vars"]["stat"] == 4
assert res_math["vars"]["sym"] == "3*x**2"
assert res_math["vars"]["np"] == 23
assert res_math["vars"]["sci"] == 0.5
print(f"[PASS] All math libraries executed cleanly in {dt_math*1000:.1f}ms")

# Test 4: Batch execution 50 seeds
t0 = time.perf_counter()
batch_res = ps.execute_sandbox_batch(code_simple, seeds=list(range(50)))
dt_batch = time.perf_counter() - t0
assert len(batch_res) == 50
assert all(b["success"] for b in batch_res)
print(f"[PASS] Batch execution of 50 seeds finished in {dt_batch*1000:.1f}ms ({dt_batch/50*1000:.2f}ms/seed)")

print("\n=== ALL 4 VALIDATION SUITE TESTS PASSED 100% ===")
