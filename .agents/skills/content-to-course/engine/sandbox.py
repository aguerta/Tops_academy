"""AST Sandbox and in-process execution environment for parametric exercise templates.

Features:
- Strict AST whitelist validation (bans os, sys, subprocess, open, eval, exec, dunder, etc.)
- Allowed modules: math, fractions, statistics, sympy, numpy, scipy, scipy.stats, random, decimal, engine.render
- 100% In-process execution with deterministic RNG injection and trace-based hard timeout
- Batch execution support for fast multi-seed sweeps
"""

import ast
import json
import os
import sys
import time
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


import warnings

# Suspicious substrings resulting from unescaped LaTeX backslashes in standard Python strings
_CORRUPTED_LATEX_PATTERNS = [
    ("\x0c", "rac", r"\frac"),
    ("\x08", "eta", r"\beta"),
    ("\x08", "matrix", r"\bmatrix"),
    ("\x08", "egin", r"\begin"),
    ("\x07", "lpha", r"\alpha"),
    ("\x07", "pprox", r"\approx"),
    ("\x0b", "ec", r"\vec"),
    ("\t", "au", r"\tau"),
    ("\t", "imes", r"\times"),
    ("\t", "ext", r"\text"),
    ("\t", "heta", r"\theta"),
    ("\n", "abla", r"\nabla"),
    ("\n", "u", r"\nu"),
    ("\n", "eq", r"\neq"),
    ("\n", "ot", r"\not"),
    ("\r", "ho", r"\rho"),
    ("\r", "ight", r"\right"),
]


def check_latex_escape_corruption_structured(code_str: str) -> List[Dict[str, Any]]:
    """Detects strings where LaTeX escape sequences were corrupted into control characters.

    Returns structured dicts:
    [
        {
            "line": int or None,
            "cmd": str (e.g. r"\frac"),
            "tail": str (e.g. "rac"),
            "ctrl_char": str,
            "message": str
        }, ...
    ]
    """
    results: List[Dict[str, Any]] = []
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(code_str, filename="<template>")
    except Exception:
        return results

    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            val = node.value
            lineno = getattr(node, "lineno", None)
            for ctrl_char, tail, latex_cmd in _CORRUPTED_LATEX_PATTERNS:
                if ctrl_char + tail in val:
                    line_info = f"line {lineno}: " if lineno is not None else ""
                    msg = (
                        f"Corrupted LaTeX escape sequence at {line_info}"
                        f"'{latex_cmd}' was parsed as control character + '{tail}'. "
                        f"Use raw string r\"...\" or escape backslash '\\\\{latex_cmd[1:]}'."
                    )
                    results.append({
                        "line": lineno,
                        "cmd": latex_cmd,
                        "tail": tail,
                        "ctrl_char": ctrl_char,
                        "message": msg,
                    })
    return results


def check_latex_escape_corruption(code_str: str) -> List[str]:
    """Detects strings where LaTeX escape sequences were corrupted into control characters.

    For example, '\\frac' in a regular string becomes '\\x0c rac' (formfeed),
    '\\beta' becomes '\\x08 eta' (backspace), etc.
    """
    return [item["message"] for item in check_latex_escape_corruption_structured(code_str)]


def validate_code_ast(code_str: str) -> bool:
    """Validate a Python code string against security whitelist rules.
    
    Raises:
        SecurityViolationError: If a security rule is violated.
        SyntaxError: If the code contains syntax errors.
    """
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", SyntaxWarning)
            tree = ast.parse(code_str, filename="<template>")
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


class _LazyModule:
    """Lazy module proxy that only imports the underlying package upon first attribute access."""

    def __init__(self, name: str, clean_fn=None):
        self._name = name
        self._clean_fn = clean_fn
        self._loaded_mod = None

    def _get_mod(self):
        if self._loaded_mod is None:
            mod = __import__(self._name, fromlist=["*"])
            if self._clean_fn:
                self._clean_fn(mod)
            self._loaded_mod = mod
        return self._loaded_mod

    def __getattr__(self, name: str) -> Any:
        return getattr(self._get_mod(), name)

    def __call__(self, *args, **kwargs) -> Any:
        return self._get_mod()(*args, **kwargs)

    def __repr__(self) -> str:
        return f"<module '{self._name}' (lazy)>"


class _LazyNPRNG:
    """Lazy proxy for numpy random generator attached to rng.np."""

    def __init__(self, seed: Optional[int]):
        self._seed = seed
        self._rng = None

    def _get_rng(self):
        if self._rng is None:
            import numpy as np
            if self._seed is not None:
                self._rng = np.random.default_rng(int(self._seed) % (2**32 - 1))
            else:
                self._rng = np.random.default_rng()
        return self._rng

    def __getattr__(self, attr: str) -> Any:
        return getattr(self._get_rng(), attr)


def _clean_numpy(np_mod: Any) -> None:
    try:
        np_mod.ctypeslib = None
    except Exception:
        pass


def build_sandbox_globals() -> Dict[str, Any]:
    """Construct safe globals dictionary pre-populated with mathematical libraries."""
    import math
    import fractions
    import statistics
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

    lazy_np = _LazyModule("numpy", clean_fn=_clean_numpy)
    lazy_sympy = _LazyModule("sympy")
    lazy_scipy = _LazyModule("scipy")

    env = {
        "__builtins__": get_safe_builtins(),
        "math": math,
        "fractions": fractions,
        "Fraction": fractions.Fraction,
        "statistics": statistics,
        "sympy": lazy_sympy,
        "numpy": lazy_np,
        "np": lazy_np,
        "scipy": lazy_scipy,
        "random": random,
        "bmatrix": bmatrix,
        "table_array": table_array,
        "fmt": fmt,
        "latex_frac": latex_frac,
    }
    return env


def call_with_timeout(
    func: Any,
    args: tuple = (),
    kwargs: Optional[dict] = None,
    timeout: Optional[float] = 0.5,
    seed: Optional[int] = None,
    max_user_steps: int = 250_000,
) -> Any:
    """Invoke a callable with a per-thread sys.settrace wall-clock and user-step guard."""
    if kwargs is None:
        kwargs = {}
    prev_trace = sys.gettrace()
    use_tracer = (timeout is not None and timeout > 0) or (max_user_steps and max_user_steps > 0)
    if use_tracer:
        deadline = time.perf_counter() + float(timeout) if (timeout is not None and timeout > 0) else None
        total_steps = [0]
        user_steps = [0]
        target_code = getattr(func, "__code__", None)
        target_filename = getattr(target_code, "co_filename", None)

        def _timeout_tracer(frame, event, arg):
            total_steps[0] += 1
            f_code = frame.f_code
            fn = f_code.co_filename
            if (
                f_code is target_code
                or (target_filename and fn == target_filename)
                or fn in ("<sandbox>", "<generate_py>", "<cross_check_py>")
            ):
                user_steps[0] += 1
                if max_user_steps and user_steps[0] > max_user_steps:
                    raise SandboxTimeoutError(
                        f"Infinite loop guard triggered after {max_user_steps} steps (seed={seed})"
                    )
            if deadline is not None and (total_steps[0] & 63) == 0 and time.perf_counter() > deadline:
                raise SandboxTimeoutError(
                    f"Template execution timed out after {timeout}s (seed={seed})"
                )
            if prev_trace is not None:
                prev_trace(frame, event, arg)
            return _timeout_tracer

        sys.settrace(_timeout_tracer)

    try:
        return func(*args, **kwargs)
    finally:
        if use_tracer:
            sys.settrace(prev_trace)


def run_code_in_env(
    code_str: str,
    func_name: str,
    args: tuple = (),
    kwargs: Optional[dict] = None,
    seed: Optional[int] = None,
    timeout: Optional[float] = None,
) -> Any:
    """Execute code in a local restricted in-process environment with optional deadline timeout."""
    validate_code_ast(code_str)
    env = build_sandbox_globals()

    import random

    if seed is not None:
        random.seed(seed)
        rng = random.Random(seed)
        rng.np = _LazyNPRNG(seed)
    else:
        rng = random.Random()
        rng.np = _LazyNPRNG(None)

    compiled = compile(code_str, "<sandbox>", "exec")
    exec(compiled, env)

    if func_name not in env:
        raise SandboxExecutionError(f"Function '{func_name}' was not defined in template code.")

    func = env[func_name]
    if kwargs is None:
        kwargs = {}

    call_args = (rng,) if ("rng" not in kwargs and len(args) == 0) else args
    try:
        return call_with_timeout(
            func,
            args=call_args,
            kwargs=kwargs,
            timeout=timeout,
            seed=seed,
            max_user_steps=250_000 if (timeout is not None and timeout > 0) else 0,
        )
    except (SecurityViolationError, SandboxTimeoutError, SandboxExecutionError):
        raise
    except Exception as e:
        raise SandboxExecutionError(f"{type(e).__name__}: {e}") from e


def execute_template_code(
    generate_py: str,
    seed: int = 42,
    cross_check_py: Optional[str] = None,
    timeout: float = 5.0,
    use_subprocess: bool = False,
) -> Dict[str, Any]:
    """Execute template code strictly in-process (use_subprocess parameter is deprecated and ignored)."""
    validate_code_ast(generate_py)
    if cross_check_py:
        validate_code_ast(cross_check_py)

    gen_res = run_code_in_env(generate_py, "generate", seed=seed, timeout=timeout)
    if cross_check_py:
        cc_res = run_code_in_env(cross_check_py, "verify", args=(gen_res,), seed=seed, timeout=timeout)
        if cc_res is False:
            raise SandboxExecutionError("cross_check verification returned False")
    return serialize_for_json(gen_res)


def execute_verifier_code(
    verifier_py: str,
    generated_result: Dict[str, Any],
    seed: int = 42,
    timeout: float = 5.0,
    use_subprocess: bool = False,
) -> bool:
    """Execute verifier/cross-check code strictly in-process."""
    validate_code_ast(verifier_py)
    res = run_code_in_env(verifier_py, "verify", args=(generated_result,), seed=seed, timeout=timeout)
    return bool(res)


# Backward compatibility aliases (100% in-process)
execute_template_in_sandbox = execute_template_code
execute_verifier_in_sandbox = execute_verifier_code
execute_sandbox_instance = execute_template_code


def execute_sandbox_batch(
    generate_py: str,
    seeds: List[int],
    cross_check_py: Optional[str] = None,
    timeout_per_item: float = 2.0,
    isolated: bool = False,
    use_subprocess: bool = False,
) -> List[Dict[str, Any]]:
    """Execute a batch of seeds strictly in-process via the fast-path."""
    validate_code_ast(generate_py)
    if cross_check_py:
        validate_code_ast(cross_check_py)

    results = []
    timeout_count = 0
    last_timeout_err = ""
    for s in seeds:
        if timeout_count >= 2:
            results.append({
                "seed": s,
                "success": False,
                "error": last_timeout_err or f"SandboxTimeoutError: Batch aborted after repeated timeouts (seed={s})",
            })
            continue
        try:
            gen_res = run_code_in_env(generate_py, "generate", seed=s, timeout=timeout_per_item)
            if cross_check_py:
                cc_res = run_code_in_env(cross_check_py, "verify", args=(gen_res,), seed=s, timeout=timeout_per_item)
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
        except SandboxTimeoutError as te:
            timeout_count += 1
            last_timeout_err = f"SandboxTimeoutError: {str(te)}"
            results.append({
                "seed": s,
                "success": False,
                "error": last_timeout_err,
            })
        except Exception as e:
            results.append({
                "seed": s,
                "success": False,
                "error": f"{type(e).__name__}: {str(e)}",
            })
    return results


_SANDBOX_WARMED_UP = False


def warm_up_sandbox(timeout: float = 60.0) -> bool:
    """Pre-warm in-process sandbox caches for sympy, numpy, scipy.stats."""
    global _SANDBOX_WARMED_UP
    if _SANDBOX_WARMED_UP:
        return True

    code = (
        "def generate(rng):\n"
        "    import sympy\n"
        "    import numpy as np\n"
        "    import scipy.stats as stats\n"
        "    return {'vars': {'warmed': True}, 'correct': '1', 'distractors': []}\n"
    )
    batch_res = execute_sandbox_batch(code, [42], timeout_per_item=timeout)
    warmed = bool(
        batch_res
        and batch_res[0].get("success")
        and batch_res[0].get("result", {}).get("vars", {}).get("warmed")
    )
    _SANDBOX_WARMED_UP = True
    return warmed
