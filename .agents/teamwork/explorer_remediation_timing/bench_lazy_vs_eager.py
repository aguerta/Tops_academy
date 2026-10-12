import time
import subprocess
import sys

# Test A: Eager imports (current sandbox.py)
eager_code = """
import time
t0 = time.perf_counter()
import math, fractions, statistics, sympy, numpy as np, scipy, scipy.stats, random
dt = time.perf_counter() - t0
print(f'Eager imports time: {dt*1000:.1f}ms')
"""

# Test B: Lazy imports (only stdlib + render eagerly, np/sympy/scipy lazy)
lazy_code = """
import time
t0 = time.perf_counter()
import math, fractions, statistics, random
class LazyGlobals(dict):
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

env = LazyGlobals({
    'math': math,
    'fractions': fractions,
    'Fraction': fractions.Fraction,
    'statistics': statistics,
    'random': random,
})
dt = time.perf_counter() - t0
print(f'Lazy initialization time: {dt*1000:.1f}ms')

# Now run a simple template
t1 = time.perf_counter()
code = '''
def generate(rng):
    return {'a': rng.randint(1, 10)}
'''
exec(code, env)
rng = random.Random(42)
res = env['generate'](rng)
dt1 = time.perf_counter() - t1
print(f'Template exec time: {dt1*1000:.1f}ms, result: {res}')
"""

r_eager = subprocess.run([sys.executable, "-c", eager_code], capture_output=True, text=True)
print(r_eager.stdout.strip())

r_lazy = subprocess.run([sys.executable, "-c", lazy_code], capture_output=True, text=True)
print(r_lazy.stdout.strip())
