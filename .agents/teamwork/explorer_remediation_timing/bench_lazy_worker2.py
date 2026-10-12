import subprocess
import sys
import json
import os
import time

skill_dir = os.path.abspath(".agents/skills/content-to-course")
env = os.environ.copy()
env["PYTHONPATH"] = skill_dir

worker_code = """
import sys, os, json, random
from engine.sandbox import validate_code_ast, serialize_for_json, get_safe_builtins

class LazySandboxGlobals(dict):
    _LOADERS = {
        'numpy': lambda: __import__('numpy'),
        'np': lambda: __import__('numpy'),
        'sympy': lambda: __import__('sympy'),
        'scipy': lambda: __import__('scipy'),
    }
    def __missing__(self, key):
        if key in self._LOADERS:
            mod = self._LOADERS[key]()
            self[key] = mod
            return mod
        raise KeyError(key)
    def __contains__(self, key):
        return key in self._LOADERS or super().__contains__(key)

import math, fractions, statistics
from engine.render import bmatrix, table_array, fmt, latex_frac

raw = sys.stdin.read()
data = json.loads(raw)
code = data['generate_py']
seed = data.get('seed', 42)

env = LazySandboxGlobals({
    '__builtins__': get_safe_builtins(),
    'math': math,
    'fractions': fractions,
    'Fraction': fractions.Fraction,
    'statistics': statistics,
    'random': random,
    'bmatrix': bmatrix,
    'table_array': table_array,
    'fmt': fmt,
    'latex_frac': latex_frac,
})
rng = random.Random(seed)
compiled = compile(code, '<sandbox>', 'exec')
exec(compiled, env)
func = env['generate']
res = func(rng)
print(json.dumps({'success': True, 'result': serialize_for_json(res)}))
"""

worker_file = os.path.abspath(".agents/teamwork/explorer_remediation_timing/lazy_worker.py")
with open(worker_file, "w", encoding="utf-8") as f:
    f.write(worker_code)

template = """
def generate(rng):
    a = rng.randint(10, 100)
    b = rng.randint(1, 5)
    return {"vars": {"a": a, "b": b}, "correct": a + b, "distractors": []}
"""

times = []
for i in range(3):
    t0 = time.perf_counter()
    payload = json.dumps({"action": "single", "generate_py": template, "seed": 42 + i})
    p = subprocess.run([sys.executable, worker_file], input=payload.encode("utf-8"), capture_output=True, env=env)
    dt = time.perf_counter() - t0
    times.append(dt)
    if p.returncode != 0:
        print("Worker failed:", p.stderr.decode())
        sys.exit(1)
    res = json.loads(p.stdout.decode("utf-8"))
    correct_val = res["result"]["correct"]
    print(f"Instance {i+1} took: {dt*1000:.1f}ms (correct: {correct_val})")
print(f"Total for 3 instances: {sum(times)*1000:.1f}ms")
