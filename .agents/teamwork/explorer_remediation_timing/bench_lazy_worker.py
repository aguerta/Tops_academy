import time
import subprocess
import sys
import os
import json

# We simulate running with lazy imports
worker_code = """
import sys
import os
import json
import ast
import random

_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _parent not in sys.path:
    sys.path.insert(0, _parent)

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

def build_lazy_sandbox_globals():
    import math
    import fractions
    import statistics
    import random
    from engine.render import bmatrix, table_array, fmt, latex_frac

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
    return env

raw = sys.stdin.read()
data = json.loads(raw)
code = data['generate_py']
seed = data.get('seed', 42)

env = build_lazy_sandbox_globals()
rng = random.Random(seed)
compiled = compile(code, '<sandbox>', 'exec')
exec(compiled, env)
func = env['generate']
res = func(rng)
print(json.dumps({'success': True, 'result': serialize_for_json(res)}))
"""

# Save worker to temp file in our teamwork folder
worker_path = os.path.abspath(".agents/teamwork/explorer_remediation_timing/lazy_worker.py")
with open(worker_path, "w", encoding="utf-8") as f:
    f.write(worker_code)

template = """
def generate(rng):
    a = rng.randint(10, 100)
    b = rng.randint(1, 5)
    return {"vars": {"a": a, "b": b}, "correct": a + b, "distractors": []}
"""

print("=== Running with lazy sandbox worker ===")
times = []
for i in range(3):
    t0 = time.perf_counter()
    payload = json.dumps({"action": "single", "generate_py": template, "seed": 42 + i})
    proc = subprocess.run([sys.executable, worker_path], input=payload.encode("utf-8"), capture_output=True, timeout=5.0)
    dt = time.perf_counter() - t0
    times.append(dt)
    res = json.loads(proc.stdout.decode("utf-8"))
    print(f"Instance {i+1} took: {dt*1000:.1f}ms (result: {res['result']['correct']})")
print(f"Total time for 3 single instances: {sum(times)*1000:.1f}ms")
