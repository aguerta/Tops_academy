import time
import subprocess
import sys
import os

skill_path = os.path.abspath(".agents/skills/content-to-course")
sys.path.insert(0, skill_path)

from engine.sandbox import execute_sandbox_instance

code = """
def generate(rng):
    a = rng.randint(10, 100)
    b = rng.randint(1, 5)
    return {"vars": {"a": a, "b": b}, "correct": a + b, "distractors": []}
"""

print("=== Running with current sandbox (eager imports) ===")
times = []
for i in range(3):
    t0 = time.perf_counter()
    res = execute_sandbox_instance(code, seed=42 + i, timeout=5.0)
    dt = time.perf_counter() - t0
    times.append(dt)
    print(f"Instance {i+1} took: {dt*1000:.1f}ms")
print(f"Total time for 3 single instances: {sum(times)*1000:.1f}ms")
