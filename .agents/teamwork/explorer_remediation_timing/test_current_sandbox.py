import time
import sys
import os

# Add skill path
skill_path = os.path.abspath(".agents/skills/content-to-course")
if skill_path not in sys.path:
    sys.path.insert(0, skill_path)

from engine.sandbox import execute_sandbox_instance, SandboxTimeoutError

# Test 1: Simple template (no math imports)
simple_code = """
def generate(rng):
    a = rng.randint(10, 100)
    b = rng.randint(1, 5)
    return {"vars": {"a": a, "b": b}, "correct": a + b, "distractors": []}
"""

t0 = time.perf_counter()
res1 = execute_sandbox_instance(simple_code, seed=42, timeout=5.0)
dt1 = time.perf_counter() - t0
print(f"Simple template took: {dt1*1000:.1f}ms")

# Test 2: Heavy template (sympy + scipy)
heavy_code = """
def generate(rng):
    import sympy as sp
    import scipy.stats as stats
    x = sp.Symbol('x')
    diff_val = str(sp.diff(x**3, x))
    p = float(stats.norm.cdf(0))
    return {"vars": {"diff": diff_val, "p": p}, "correct": 1, "distractors": []}
"""

t0 = time.perf_counter()
res2 = execute_sandbox_instance(heavy_code, seed=42, timeout=5.0)
dt2 = time.perf_counter() - t0
print(f"Heavy template (sympy + scipy) took: {dt2*1000:.1f}ms")

# Test 3: Infinite loop with timeout=1.0s
loop_code = """
def generate(rng):
    while True:
        pass
"""

t0 = time.perf_counter()
try:
    execute_sandbox_instance(loop_code, seed=1, timeout=1.0)
    print("ERROR: Infinite loop did not timeout!")
except SandboxTimeoutError:
    dt3 = time.perf_counter() - t0
    print(f"Infinite loop timed out correctly in: {dt3*1000:.1f}ms (expected ~1000-1100ms)")
