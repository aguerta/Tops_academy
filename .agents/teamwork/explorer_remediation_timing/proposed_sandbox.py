"""AST Sandbox and isolated execution environment for parametric exercise templates.

Features:
- Strict AST whitelist validation (bans os, sys, subprocess, open, eval, exec, dunder, etc.)
- Allowed modules: math, fractions, statistics, sympy, numpy, scipy, scipy.stats, random, decimal
- Subprocess execution with default 5.0s timeout per instance
- Lazy globals loader for fast worker startup (<100ms for lightweight templates)
- Deterministic RNG injection
- Batch execution support for fast multi-seed sweeps
"""

import ast
import json
import os
import subprocess
import sys
import traceback
from typing import Any, Dict, List, Optional, Tuple, Union


class SecurityViolationError(Exception):
    """Raised when code violates sandbox security policies."""
    pass


class SandboxExecutionError(Exception):
    """Raised when sandbox code raises a runtime exception."""
    pass


class SandboxTimeoutError(Exception):
    """Raised when sandbox code exceeds the timeout limit."""
    pass


ALLOWED_ROOT_MODULES = {
    "math",
    "fractions",
    "statistics",
    "sympy",
    "numpy",
    "scipy",
    "random",
    "decimal",
    "engine",
}

BANNED_NAMES = {
    "open",
    "eval",
    "exec",
    "compile",
    "__import__",
    "globals",
    "locals",
    "vars",
    "breakpoint",
    "input",
    "exit",
    "quit",
    "builtins",
    "__builtins__",
    "os",
    "sys",
    "subprocess",
    "socket",
    "urllib",
    "requests",
    "http",
    "shutil",
    "pathlib",
    "io",
    "posix",
    "nt",
    "ctypes",
    "importlib",
    "pickle",
    "shelve",
    "tempfile",
}


class SandboxASTValidator(ast.NodeVisitor):
    """Validates that Python code complies with AST whitelist constraints."""

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            root = alias.name.split(".")[0]
            if root not in ALLOWED_ROOT_MODULES:
                raise SecurityViolationError(
                    f"Import of module '{alias.name}' is prohibited. "
                    f"Only {sorted(ALLOWED_ROOT_MODULES)} are allowed."
                )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module:
            root = node.module.split(".")[0]
            if root not in ALLOWED_ROOT_MODULES:
                raise SecurityViolationError(
                    f"Import from module '{node.module}' is prohibited. "
                    f"Only {sorted(ALLOWED_ROOT_MODULES)} are allowed."
                )
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if node.id in BANNED_NAMES:
            raise SecurityViolationError(f"Use of banned identifier '{node.id}' is prohibited.")
        if node.id.startswith("__") and node.id.endswith("__"):
            raise SecurityViolationError(f"Use of dunder identifier '{node.id}' is prohibited.")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr.startswith("__"):
            raise SecurityViolationError(f"Access to dunder attribute '{node.attr}' is prohibited.")
        self.generic_visit(node)


def validate_code_ast(code_str: str) -> bool:
    """Validate a Python code string against security whitelist rules."""
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        raise SyntaxError(f"Syntax error in template code: {e}") from e

    validator = SandboxASTValidator()
    validator.visit(tree)
    return True


def serialize_for_json(obj: Any) -> Any:
    """Recursively serialize objects to JSON-compatible data types."""
    if hasattr(obj, "tolist") and callable(getattr(obj, "tolist")):
        return serialize_for_json(obj.tolist())
    if hasattr(obj, "item") and callable(getattr(obj, "item")):
        return serialize_for_json(obj.item())
    if isinstance(obj, (int, float, str, bool)) or obj is None:
        return obj
    if isinstance(obj, dict):
        return {str(k): serialize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [serialize_for_json(v) for v in obj]
    return str(obj)


def get_safe_builtins() -> Dict[str, Any]:
    """Return a restricted builtins dictionary without I/O or meta-programming."""
    import builtins

    orig_import = builtins.__import__

    def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
        root = name.split(".")[0]
        if root not in ALLOWED_ROOT_MODULES:
            raise SecurityViolationError(
                f"Import of module '{name}' is prohibited. Only {sorted(ALLOWED_ROOT_MODULES)} are allowed."
            )
        return orig_import(name, globals, locals, fromlist, level)

    allowed_builtin_names = {
        "abs", "all", "any", "bin", "bool", "chr", "complex", "dict", "divmod",
        "enumerate", "filter", "float", "format", "frozenset", "hash", "hex",
        "int", "isinstance", "issubclass", "iter", "len", "list", "map", "max",
        "min", "next", "oct", "ord", "pow", "print", "range", "repr", "reversed",
        "round", "set", "slice", "sorted", "str", "sum", "tuple", "type", "zip",
        "AssertionError", "ValueError", "TypeError", "ZeroDivisionError",
        "Exception", "IndexError", "KeyError", "AttributeError", "StopIteration",
    }
    safe_builtins = {"__import__": safe_import}
    for name in allowed_builtin_names:
        if hasattr(builtins, name):
            safe_builtins[name] = getattr(builtins, name)
    return safe_builtins


class LazySandboxGlobals(dict):
    """Dictionary subclass that lazily imports heavy mathematical libraries on first access."""

    @staticmethod
    def _load_numpy():
        import numpy as np
        return np

    @staticmethod
    def _load_sympy():
        import sympy
        return sympy

    @staticmethod
    def _load_scipy():
        import scipy
        import scipy.stats
        return scipy

    @classmethod
    def get_loaders(cls):
        return {
            "numpy": cls._load_numpy,
            "np": cls._load_numpy,
            "sympy": cls._load_sympy,
            "scipy": cls._load_scipy,
        }

    def __missing__(self, key: str) -> Any:
        loaders = self.get_loaders()
        if key in loaders:
            mod = loaders[key]()
            self[key] = mod
            if key in ("numpy", "np"):
                self["numpy"] = mod
                self["np"] = mod
            return mod
        raise KeyError(key)

    def __contains__(self, key: object) -> bool:
        if super().__contains__(key):
            return True
        return key in self.get_loaders()

    def get(self, key: str, default: Any = None) -> Any:
        if super().__contains__(key):
            return super().__getitem__(key)
        loaders = self.get_loaders()
        if key in loaders:
            return self.__missing__(key)
        return default


def build_sandbox_globals() -> Dict[str, Any]:
    """Construct safe globals dictionary with lazy-loaded mathematical libraries."""
    import math
    import fractions
    import statistics
    import random
    from engine.render import bmatrix, table_array, fmt, latex_frac

    env = LazySandboxGlobals({
        "__builtins__": get_safe_builtins(),
        "math": math,
        "fractions": fractions,
        "Fraction": fractions.Fraction,
        "statistics": statistics,
        "random": random,
        "bmatrix": bmatrix,
        "table_array": table_array,
        "fmt": fmt,
        "latex_frac": latex_frac,
    })
    return env


def run_code_in_env(
    code_str: str,
    func_name: str,
    args: tuple = (),
    kwargs: Optional[dict] = None,
    seed: Optional[int] = None,
) -> Any:
    """Execute code in a local restricted environment."""
    validate_code_ast(code_str)
    env = build_sandbox_globals()

    import random
    if seed is not None:
        rng = random.Random(seed)
        random.seed(seed)
        # Attach numpy default_rng if numpy is already loaded or requested
        try:
            import numpy as np
            rng.np = np.random.default_rng(seed)
            np.random.seed(seed)
        except ImportError:
            pass
    else:
        rng = random.Random()
        try:
            import numpy as np
            rng.np = np.random.default_rng()
        except ImportError:
            pass

    compiled = compile(code_str, "<sandbox>", "exec")
    exec(compiled, env)

    if func_name not in env:
        raise SandboxExecutionError(f"Function '{func_name}' was not defined in template code.")

    func = env[func_name]
    kwargs = kwargs or {}

    if "rng" not in kwargs and len(args) == 0:
        return func(rng, **kwargs)
    return func(*args, **kwargs)


def execute_sandbox_instance(
    generate_py: str,
    seed: int,
    cross_check_py: Optional[str] = None,
    timeout: float = 5.0,
) -> Dict[str, Any]:
    """Execute a single template generation (and optional cross check) via isolated worker."""
    validate_code_ast(generate_py)
    if cross_check_py:
        validate_code_ast(cross_check_py)

    payload = {
        "action": "single",
        "generate_py": generate_py,
        "cross_check_py": cross_check_py,
        "seed": seed,
    }
    input_bytes = json.dumps(payload).encode("utf-8")

    cmd = [sys.executable, os.path.abspath(__file__)]
    try:
        proc = subprocess.run(
            cmd,
            input=input_bytes,
            capture_output=True,
            timeout=timeout,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        )
    except subprocess.TimeoutExpired as e:
        raise SandboxTimeoutError(f"Template execution timed out after {timeout}s (seed={seed})") from e

    if proc.returncode != 0:
        err_msg = proc.stderr.decode("utf-8", errors="replace")
        raise SandboxExecutionError(f"Sandbox worker process failed: {err_msg}")

    try:
        res = json.loads(proc.stdout.decode("utf-8"))
    except json.JSONDecodeError as e:
        out_msg = proc.stdout.decode("utf-8", errors="replace")
        raise SandboxExecutionError(f"Failed to decode sandbox output: {out_msg}") from e

    if not res.get("success"):
        error_type = res.get("error_type", "SandboxExecutionError")
        msg = res.get("error_message", "Unknown sandbox error")
        if error_type == "SecurityViolationError":
            raise SecurityViolationError(msg)
        raise SandboxExecutionError(msg)

    return res["result"]


def execute_sandbox_batch(
    generate_py: str,
    seeds: List[int],
    cross_check_py: Optional[str] = None,
    timeout_per_item: float = 2.0,
) -> List[Dict[str, Any]]:
    """Execute a batch of seeds in a single isolated process run."""
    validate_code_ast(generate_py)
    if cross_check_py:
        validate_code_ast(cross_check_py)

    total_timeout = max(10.0, len(seeds) * timeout_per_item)
    payload = {
        "action": "batch",
        "generate_py": generate_py,
        "cross_check_py": cross_check_py,
        "seeds": seeds,
    }
    input_bytes = json.dumps(payload).encode("utf-8")

    cmd = [sys.executable, os.path.abspath(__file__)]
    try:
        proc = subprocess.run(
            cmd,
            input=input_bytes,
            capture_output=True,
            timeout=total_timeout,
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        )
    except subprocess.TimeoutExpired as e:
        raise SandboxTimeoutError(
            f"Batch template execution timed out after {total_timeout}s for {len(seeds)} seeds"
        ) from e

    if proc.returncode != 0:
        err_msg = proc.stderr.decode("utf-8", errors="replace")
        raise SandboxExecutionError(f"Sandbox batch worker process failed: {err_msg}")

    try:
        res = json.loads(proc.stdout.decode("utf-8"))
    except json.JSONDecodeError as e:
        out_msg = proc.stdout.decode("utf-8", errors="replace")
        raise SandboxExecutionError(f"Failed to decode batch sandbox output: {out_msg}") from e

    if not res.get("success"):
        raise SandboxExecutionError(res.get("error_message", "Unknown batch error"))

    return res["results"]


def _worker_entrypoint():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            sys.exit(0)

        data = json.loads(raw_input)
        action = data.get("action", "single")
        generate_py = data["generate_py"]
        cross_check_py = data.get("cross_check_py")

        validate_code_ast(generate_py)
        if cross_check_py:
            validate_code_ast(cross_check_py)

        if action == "single":
            seed = data.get("seed", 42)
            gen_res = run_code_in_env(generate_py, "generate", seed=seed)
            if cross_check_py:
                cc_res = run_code_in_env(cross_check_py, "verify", args=(gen_res,), seed=seed)
                if cc_res is False:
                    raise SandboxExecutionError("cross_check verification returned False")
            
            output = {
                "success": True,
                "result": serialize_for_json(gen_res),
            }
            print(json.dumps(output))

        elif action == "batch":
            seeds = data.get("seeds", [])
            results = []
            for s in seeds:
                try:
                    gen_res = run_code_in_env(generate_py, "generate", seed=s)
                    if cross_check_py:
                        cc_res = run_code_in_env(cross_check_py, "verify", args=(gen_res,), seed=s)
                        if cc_res is False:
                            results.append({
                                "seed": s,
                                "success": False,
                                "error": "cross_check verification returned False",
                            })
                            continue
                    results.append({
                        "seed": s,
                        "success": True,
                        "result": serialize_for_json(gen_res),
                    })
                except Exception as e:
                    results.append({
                        "seed": s,
                        "success": False,
                        "error": f"{type(e).__name__}: {str(e)}",
                    })
            print(json.dumps({"success": True, "results": results}))

    except SecurityViolationError as e:
        print(json.dumps({
            "success": False,
            "error_type": "SecurityViolationError",
            "error_message": str(e),
        }))
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error_type": type(e).__name__,
            "error_message": f"{str(e)}\n{traceback.format_exc()}",
        }))


if __name__ == "__main__":
    _parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _parent not in sys.path:
        sys.path.insert(0, _parent)
    _worker_entrypoint()
