
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
