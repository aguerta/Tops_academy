import sys

class LazySandboxGlobals(dict):
    """Dictionary subclass that lazily imports heavy modules on first access."""
    
    _LOADERS = {
        "numpy": lambda: __import__("numpy"),
        "np": lambda: __import__("numpy"),
        "sympy": lambda: __import__("sympy"),
        "scipy": lambda: __import__("scipy"),
    }

    def __missing__(self, key):
        if key in self._LOADERS:
            mod = self._LOADERS[key]()
            self[key] = mod
            return mod
        raise KeyError(key)

    def __contains__(self, key):
        return key in self._LOADERS or super().__contains__(key)

# Test with exec
env = LazySandboxGlobals({
    "math": __import__("math"),
})

code = """
def generate(rng):
    return {'np_type': type(np).__name__, 'val': int(np.sin(0))}
"""

exec(code, env)
func = env["generate"]
res = func(None)
print("Function result:", res)
print("Keys after function execution:", sorted(env.keys()))
