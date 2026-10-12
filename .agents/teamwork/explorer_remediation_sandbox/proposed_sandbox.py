"""AST Sandbox and isolated execution environment for parametric exercise templates.

Features:
- Strict AST whitelist validation (bans os, sys, subprocess, open, eval, exec, dunder, etc.)
- Allowed modules: math, fractions, statistics, sympy, numpy, scipy, scipy.stats, random, decimal, engine.render
- Subprocess execution with hard timeout
- Deterministic RNG injection and global RNG seeding
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
    "modules",
    "attrgetter",
    "itemgetter",
    "methodcaller",
    "ctypeslib",
    "operator",
    "system",
    "popen",
}


def is_module_allowed(mod_name: Optional[str]) -> bool:
    """Check if a module path is permitted under sandbox whitelist policy.
    
    Permits allowed root modules (e.g. math, numpy, scipy.stats) and engine.render only.
    Bare 'engine' or 'engine.sandbox' are strictly prohibited.
    """
    if not mod_name:
        return False
    if mod_name == "engine.render" or mod_name.startswith("engine.render."):
        return True
    root = mod_name.split(".")[0]
    return root in ALLOWED_ROOT_MODULES


class SandboxASTValidator(ast.NodeVisitor):
    """Validates that Python code complies with AST whitelist constraints."""

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            if not is_module_allowed(alias.name):
                raise SecurityViolationError(
                    f"Import of module '{alias.name}' is prohibited. "
                    f"Only {sorted(ALLOWED_ROOT_MODULES)} and 'engine.render' are allowed."
                )
            if alias.asname:
                if alias.asname in BANNED_NAMES or alias.asname.startswith("__") or alias.asname.endswith("__"):
                    raise SecurityViolationError(
                        f"Import alias '{alias.asname}' uses a banned or dunder identifier."
                    )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.level > 0 or node.module is None:
            raise SecurityViolationError("Relative imports are prohibited in sandbox templates.")
        if not is_module_allowed(node.module):
            raise SecurityViolationError(
                f"Import from module '{node.module}' is prohibited. "
                f"Only {sorted(ALLOWED_ROOT_MODULES)} and 'engine.render' are allowed."
            )
        for alias in node.names:
            if alias.name in BANNED_NAMES or alias.name.startswith("__") or alias.name.endswith("__"):
                raise SecurityViolationError(
                    f"Importing banned symbol '{alias.name}' is prohibited."
                )
            if alias.asname:
                if alias.asname in BANNED_NAMES or alias.asname.startswith("__") or alias.asname.endswith("__"):
                    raise SecurityViolationError(
                        f"Import alias '{alias.asname}' uses a banned or dunder identifier."
                    )
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if node.id in BANNED_NAMES:
            raise SecurityViolationError(f"Use of banned identifier '{node.id}' is prohibited.")
        if node.id.startswith("__") or node.id.endswith("__"):
            raise SecurityViolationError(f"Use of dunder identifier '{node.id}' is prohibited.")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr.startswith("__") or node.attr.endswith("__"):
            raise SecurityViolationError(f"Access to dunder attribute '{node.attr}' is prohibited.")
        if node.attr in BANNED_NAMES:
            raise SecurityViolationError(f"Access to banned attribute '{node.attr}' is prohibited.")
        self.generic_visit(node)


def validate_code_ast(code_str: str) -> bool:
    """Validate a Python code string against security whitelist rules.
    
    Raises:
        SecurityViolationError: If a security rule is violated.
        SyntaxError: If the code contains syntax errors.
    """
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
        if level > 0:
            raise SecurityViolationError("Relative imports are prohibited in sandbox templates.")
        if not is_module_allowed(name):
            raise SecurityViolationError(
                f"Import of module '{name}' is prohibited. Only {sorted(ALLOWED_ROOT_MODULES)} and 'engine.render' are allowed."
            )
        if fromlist:
            for item in fromlist:
                if isinstance(item, str) and (item in BANNED_NAMES or item.startswith("__") or item.endswith("__")):
                    raise SecurityViolationError(f"Importing banned symbol '{item}' is prohibited.")
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


def build_sandbox_globals() -> Dict[str, Any]:
    """Construct safe globals dictionary pre-populated with mathematical libraries."""
    import math
    import fractions
    import statistics
    import sympy
    import numpy as np
    import scipy
    import scipy.stats
    import random
    from engine.render import bmatrix, table_array, fmt, latex_frac

    # Purge re-exported internal leaks from whitelisted modules
    for mod in (fractions, statistics):
        if hasattr(mod, "sys"):
            try:
                delattr(mod, "sys")
            except Exception:
                setattr(mod, "sys", None)
    if hasattr(fractions, "operator"):
        try:
            delattr(fractions, "operator")
        except Exception:
            setattr(fractions, "operator", None)
    try:
        np.ctypeslib = None
    except Exception:
        pass

    env = {
        "__builtins__": get_safe_builtins(),
        "math": math,
        "fractions": fractions,
        "Fraction": fractions.Fraction,
        "statistics": statistics,
        "sympy": sympy,
        "numpy": np,
        "np": np,
        "scipy": scipy,
        "random": random,
        "bmatrix": bmatrix,
        "table_array": table_array,
        "fmt": fmt,
        "latex_frac": latex_frac,
    }
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
    import numpy as np

    if seed is not None:
        random.seed(seed)
        try:
            np.random.seed(int(seed) % (2**32 - 1))
        except Exception:
            pass
        rng = random.Random(seed)
        rng.np = np.random.default_rng(seed)
    else:
        rng = random.Random()
        rng.np = np.random.default_rng()

    compiled = compile(code_str, "<sandbox>", "exec")
    exec(compiled, env)

    if func_name not in env:
        raise SandboxExecutionError(f"Function '{func_name}' was not defined in template code.")

    func = env[func_name]
    kwargs = kwargs or {}

    # If func expects rng as first arg, supply it if not present
    if "rng" not in kwargs and len(args) == 0:
        return func(rng, **kwargs)
    return func(*args, **kwargs)


def execute_sandbox_instance(
    generate_py: str,
    seed: int,
    cross_check_py: Optional[str] = None,
    timeout: float = 5.0,
) -> Dict[str, Any]:
    """Execute a single template generation (and optional cross check) via isolated worker.
    
    Returns the serialized result dictionary.
    Raises:
        SecurityViolationError: If code contains prohibited AST constructs.
        SandboxTimeoutError: If execution exceeds the timeout limit.
        SandboxExecutionError: If execution raises an exception.
    """
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

    # Run via isolated subprocess
    cmd = [sys.executable, os.path.abspath(__file__)]
    skill_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "skills", "content-to-course"))
    if not os.path.isdir(skill_root):
        skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        proc = subprocess.run(
            cmd,
            input=input_bytes,
            capture_output=True,
            timeout=timeout,
            cwd=skill_root,
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
    """Execute a batch of seeds in a single isolated process run.
    
    Returns a list of dicts: {"seed": int, "success": bool, "result": dict, "error": str}
    """
    validate_code_ast(generate_py)
    if cross_check_py:
        validate_code_ast(cross_check_py)

    total_timeout = max(5.0, len(seeds) * timeout_per_item)
    payload = {
        "action": "batch",
        "generate_py": generate_py,
        "cross_check_py": cross_check_py,
        "seeds": seeds,
    }
    input_bytes = json.dumps(payload).encode("utf-8")

    cmd = [sys.executable, os.path.abspath(__file__)]
    skill_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "skills", "content-to-course"))
    if not os.path.isdir(skill_root):
        skill_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        proc = subprocess.run(
            cmd,
            input=input_bytes,
            capture_output=True,
            timeout=total_timeout,
            cwd=skill_root,
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


# =========================================================================
# Subprocess Entrypoint (when invoked as `python path/to/sandbox.py`)
# =========================================================================

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
    _this_dir = os.path.dirname(os.path.abspath(__file__))
    _skill_candidate = os.path.abspath(os.path.join(_this_dir, "..", "..", "skills", "content-to-course"))
    _parent = os.path.dirname(_this_dir)
    for p in [_skill_candidate, _parent, _this_dir]:
        if os.path.isdir(p) and p not in sys.path:
            sys.path.insert(0, p)
    _worker_entrypoint()
