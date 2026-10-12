import sys
import os

sys.path.insert(0, os.path.abspath(".agents/skills/content-to-course"))

from engine.sandbox import (
    validate_code_ast,
    execute_sandbox_instance,
    execute_sandbox_batch,
    SecurityViolationError,
    SandboxTimeoutError,
)

# Test 1: Banned imports
for banned in ["import os", "import sys", "import subprocess", "import socket"]:
    try:
        validate_code_ast(f"{banned}\ndef generate(rng): return {{}}")
        assert False, f"Failed to block {banned}"
    except SecurityViolationError:
        print(f"PASS: Blocked {banned}")

# Test 2: Banned builtins
for banned in ["open('foo')", "eval('1+1')", "exec('x=1')", "__import__('os')"]:
    try:
        validate_code_ast(f"def generate(rng):\n    {banned}\n    return {{}}")
        assert False, f"Failed to block {banned}"
    except SecurityViolationError:
        print(f"PASS: Blocked {banned}")

# Test 3: Dunder attribute access
for banned in ["().__class__", "x.__dict__", "x.__subclasses__()"]:
    try:
        validate_code_ast(f"def generate(rng):\n    x = {banned}\n    return {{}}")
        assert False, f"Failed to block {banned}"
    except SecurityViolationError:
        print(f"PASS: Blocked {banned}")

# Test 4: Valid mathematical generation
valid_code = """
def generate(rng):
    import numpy as np
    import math
    a = rng.randint(2, 9)
    b = rng.randint(1, 5)
    ans = a * b
    distractors = [{"value": a * b + i, "distractor_id": f"D-0{i}"} for i in range(1, 7)]
    return {
        "vars": {"a": a, "b": b},
        "correct": ans,
        "distractors": distractors
    }
"""

import time
t0 = time.time()
res = execute_sandbox_instance(valid_code, seed=123, timeout=5.0)
print(f"PASS: Valid generation executed in {time.time()-t0:.2f}s:", res["vars"], res["correct"])

# Test 5: Batch execution
batch_res = execute_sandbox_batch(valid_code, seeds=[1, 2, 3, 4, 5])
assert len(batch_res) == 5
assert all(r["success"] for r in batch_res)
print("PASS: Batch execution passed 5 seeds!")

# Test 6: Timeout test
timeout_code = """
def generate(rng):
    while True:
        pass
"""
try:
    execute_sandbox_instance(timeout_code, seed=1, timeout=1.0)
    assert False, "Failed to timeout infinite loop"
except SandboxTimeoutError:
    print("PASS: Timeout successfully terminated infinite loop!")

print("\nALL SMOKE TESTS PASSED!")
