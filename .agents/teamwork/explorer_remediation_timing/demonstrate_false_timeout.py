import time
import subprocess
import sys
import os

skill_path = os.path.abspath(".agents/skills/content-to-course")
sys.path.insert(0, skill_path)

from engine.sandbox import execute_sandbox_instance, SandboxTimeoutError

# Case A: Current sandbox with heavy imports and timeout=1.0 on legitimate template
legit_template = """
def generate(rng):
    import scipy.stats
    return {'vars': {}, 'correct': 1, 'distractors': []}
"""

try:
    t0 = time.perf_counter()
    execute_sandbox_instance(legit_template, seed=42, timeout=1.0)
    print("Legitimate template succeeded in < 1.0s")
except SandboxTimeoutError:
    dt = time.perf_counter() - t0
    print(f"FALSE TIMEOUT on legitimate template after {dt*1000:.1f}ms! (Worker couldn't even finish importing before timeout killed it!)")
