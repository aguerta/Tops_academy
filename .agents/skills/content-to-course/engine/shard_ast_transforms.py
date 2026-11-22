"""AST dependency pruning, auto-vars injection, generator specialization, and anti-clone checks."""

import ast
import copy
import inspect
import logging
import re
import textwrap
import threading
import time
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from engine.shard_locator import ShardDataLineLocator

_logger = logging.getLogger(__name__)

_QTYPE_TO_INTERACTION: Dict[str, str] = {
    "mc7": "multiple_choice_7_options",
    "mc": "multiple_choice_7_options",
    "multiple_choice": "multiple_choice_7_options",
    "multiple_choice_7_options": "multiple_choice_7_options",
    "fib": "fill_in_the_blank",
    "open_ended": "fill_in_the_blank",
    "fill_in_the_blank": "fill_in_the_blank",
    "ms": "multiple_select",
    "multiple_select": "multiple_select",
    "open_symbolic": "open_symbolic",
    "sym": "open_symbolic",
    "symbolic": "open_symbolic",
    "proof_dag": "proof_dag",
    "proof": "proof_dag",
    "parsons": "proof_dag",
    "adversarial_break": "adversarial_break",
    "adversarial": "adversarial_break",
    "fallacy": "adversarial_break",
    "unstructured_model": "unstructured_model",
    "stage0": "unstructured_model",
    "stage_0": "unstructured_model",
    "modeling": "unstructured_model",
    "invariant_canvas": "invariant_canvas",
    "graph_manipulator": "invariant_canvas",
    "canvas": "invariant_canvas",
    "concept_matching": "concept_matching",
    "matching": "concept_matching",
}



class EvaluationContext:
    """Thread-safe context tracking active template, generator callable and seed during compilation."""

    _lock = threading.Lock()
    _current: Dict[str, Any] = {
        "shard_id": "unknown",
        "cid": "unknown",
        "template_id": "unknown",
        "gen_fn": "_gen_unknown",
        "archetype": "?",
        "seed": None,
        "start_time": 0.0,
    }

    @classmethod
    def set(
        cls,
        shard_id: Optional[str] = None,
        cid: Optional[str] = None,
        template_id: Optional[str] = None,
        gen_fn: Optional[str] = None,
        archetype: Optional[Any] = None,
        seed: Optional[int] = None,
    ) -> None:
        with cls._lock:
            if shard_id is not None:
                cls._current["shard_id"] = str(shard_id)
            if cid is not None:
                cls._current["cid"] = str(cid)
            if template_id is not None:
                cls._current["template_id"] = str(template_id)
            if gen_fn is not None:
                cls._current["gen_fn"] = str(gen_fn)
            if archetype is not None:
                cls._current["archetype"] = archetype
            if seed is not None:
                cls._current["seed"] = seed
            cls._current["start_time"] = time.time()

    @classmethod
    def get(cls) -> Dict[str, Any]:
        with cls._lock:
            return dict(cls._current)

    @classmethod
    def reset(cls, shard_id: str = "unknown") -> None:
        with cls._lock:
            cls._current = {
                "shard_id": shard_id,
                "cid": "unknown",
                "template_id": "unknown",
                "gen_fn": "_gen_unknown",
                "archetype": "?",
                "seed": None,
                "start_time": time.time(),
            }




def prune_ast_dependencies(source_text: str, target_fn_name: str) -> str:
    """Extracts minimal self-contained AST code containing reachable imports, constants,
    and helper functions needed by target_fn_name, followed by target_fn_name itself.
    """
    if not source_text or not target_fn_name:
        return source_text
    try:
        tree = ast.parse(source_text)
    except Exception:
        return source_text

    imports: List[Tuple[ast.AST, str]] = []
    constants: Dict[str, Tuple[ast.AST, str]] = {}
    functions: Dict[str, Tuple[ast.AST, str]] = {}

    lines = source_text.splitlines()

    def _get_node_text(node: ast.AST) -> str:
        seg = ast.get_source_segment(source_text, node)
        if seg is not None:
            return seg
        s = getattr(node, "lineno", 1) - 1
        e = getattr(node, "end_lineno", s + 1)
        return "\n".join(lines[s:e])

    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append((node, _get_node_text(node)))
        elif isinstance(node, ast.Assign):
            if (
                len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and isinstance(node.value, ast.Lambda)
            ):
                functions[node.targets[0].id] = (node, _get_node_text(node))
            else:
                for t in node.targets:
                    if isinstance(t, ast.Name) and t.id != "TEMPLATES":
                        constants[t.id] = (node, _get_node_text(node))
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id != "TEMPLATES":
                if isinstance(node.value, ast.Lambda):
                    functions[node.target.id] = (node, _get_node_text(node))
                else:
                    constants[node.target.id] = (node, _get_node_text(node))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions[node.name] = (node, _get_node_text(node))

    if target_fn_name not in functions:
        return source_text

    needed_funcs: Set[str] = set()
    needed_consts: Set[str] = set()
    needed_names: Set[str] = set()

    queue: List[Tuple[str, str]] = [("fn", target_fn_name)]
    visited_fns: Set[str] = set()
    visited_consts: Set[str] = set()

    while queue:
        kind, curr = queue.pop(0)
        if kind == "fn":
            if curr in visited_fns:
                continue
            visited_fns.add(curr)
            if curr != target_fn_name:
                needed_funcs.add(curr)
            node_entry = functions.get(curr)
        else:
            if curr in visited_consts:
                continue
            visited_consts.add(curr)
            needed_consts.add(curr)
            node_entry = constants.get(curr)
        if not node_entry:
            continue
        for sub in ast.walk(node_entry[0]):
            if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load):
                nid = sub.id
                needed_names.add(nid)
                if nid in functions and nid not in visited_fns:
                    queue.append(("fn", nid))
                elif nid in constants and nid not in visited_consts:
                    queue.append(("const", nid))
            elif isinstance(sub, ast.Attribute) and isinstance(sub.value, ast.Name):
                needed_names.add(sub.value.id)

    needed_imports: List[str] = []
    allowed_import_roots = {"math", "fractions", "statistics", "sympy", "numpy", "scipy", "random", "decimal"}
    for imp_node, imp_text in imports:
        keep = False
        if isinstance(imp_node, ast.Import):
            for alias in imp_node.names:
                root = alias.name.split(".")[0]
                asname = alias.asname or root
                if asname in needed_names or (root in allowed_import_roots and (root in needed_names or not needed_names)):
                    keep = True
                    break
        elif isinstance(imp_node, ast.ImportFrom):
            root = (imp_node.module or "").split(".")[0]
            if root in needed_names:
                keep = True
            else:
                for alias in imp_node.names:
                    asname = alias.asname or alias.name
                    if asname == "*" or asname in needed_names:
                        keep = True
                        break
        if keep:
            needed_imports.append(imp_text.strip())

    sorted_consts = sorted([c for name, c in constants.items() if name in needed_consts], key=lambda x: getattr(x[0], "lineno", 0))
    sorted_funcs = sorted([f for name, f in functions.items() if name in needed_funcs], key=lambda x: getattr(x[0], "lineno", 0))

    parts = []
    if needed_imports:
        parts.append("\n".join(needed_imports))
    if sorted_consts:
        parts.append("\n\n".join(c[1].strip() for c in sorted_consts))
    if sorted_funcs:
        parts.append("\n\n".join(f[1].strip() for f in sorted_funcs))

    target_code = functions[target_fn_name][1].strip()
    parts.append(target_code)
    return "\n\n".join(parts).strip()


def prune_ast_preamble(source_text: str, target_fn_name: str) -> str:
    """Returns pruned preamble code (reachable imports, constants, and helper functions)
    for target_fn_name, excluding target_fn_name itself.
    """
    if not source_text or not target_fn_name:
        return ""
    full_pruned = prune_ast_dependencies(source_text, target_fn_name)
    if not full_pruned:
        return ""
    try:
        ptree = ast.parse(full_pruned)
        if ptree.body:
            last = ptree.body[-1]
            is_target = (
                (isinstance(last, (ast.FunctionDef, ast.AsyncFunctionDef)) and last.name == target_fn_name)
                or (isinstance(last, ast.Assign) and len(last.targets) == 1 and isinstance(last.targets[0], ast.Name) and last.targets[0].id == target_fn_name)
                or (isinstance(last, ast.AnnAssign) and isinstance(last.target, ast.Name) and last.target.id == target_fn_name)
            )
            if is_target:
                lines = full_pruned.splitlines()
                return "\n".join(lines[: max(0, last.lineno - 1)]).strip()
    except Exception:
        pass
    m = re.search(rf"^(?:def\s+{re.escape(target_fn_name)}\s*\(|{re.escape(target_fn_name)}\s*=)", full_pruned, flags=re.MULTILINE)
    if m:
        return full_pruned[:m.start()].strip()
    return ""




_RESERVED_VAR_NAMES = {
    "rng", "r", "arch", "ans", "correct", "ds", "distractors", "options", "v1", "vl", "_"
}


def inject_ast_auto_vars(code_or_fn: Any) -> Any:
    """AST helper that auto-injects 'vars': {name: name, ...} into return dicts of generator functions.

    M4.5: Eliminates the repetitive boilerplate of 'vars': {...} in Form-C generator functions.
    If a generator function returns a dict with at least one output key ('ans', 'correct', 'ds', 'distractors', 'options')
    and lacks 'vars', local variables assigned in the function body are automatically collected and injected.

    Accepts either:
    - code_or_fn as callable: extracts source, injects AST auto-vars, recompiles and returns the transformed callable.
    - code_or_fn as str: parses, injects AST auto-vars, and returns the transformed code string.
    """
    if callable(code_or_fn):
        try:
            fn_src = textwrap.dedent(inspect.getsource(code_or_fn))
            transformed_src = inject_ast_auto_vars(fn_src)
            fn_globals = getattr(code_or_fn, "__globals__", {})
            ns = dict(fn_globals)
            exec(compile(transformed_src, "<auto_vars>", "exec"), ns)
            fn_name = getattr(code_or_fn, "__name__", "")
            candidate = ns.get(fn_name)
            if callable(candidate):
                return candidate
            return _wrap_gen_raw_with_auto_vars(code_or_fn, transformed_src)
        except Exception:
            return _wrap_gen_raw_with_auto_vars(code_or_fn, "")

    if not isinstance(code_or_fn, str) or not code_or_fn.strip():
        return code_or_fn

    code_str = code_or_fn
    try:
        tree = ast.parse(code_str)
    except Exception:
        return code_str

    class _AutoVarsTransformer(ast.NodeTransformer):
        def __init__(self):
            self.modified = False

        def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
            return self._transform_fn(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AsyncFunctionDef:
            return self._transform_fn(node)

        def _transform_fn(self, fn_node):
            parent = self

            def _inject_return(ret_node: ast.Return, vars_list: List[str]) -> ast.Return:
                if not isinstance(ret_node.value, ast.Dict):
                    return ret_node
                dict_node = ret_node.value
                str_keys = [
                    k.value if (isinstance(k, ast.Constant) and isinstance(k.value, str)) else None
                    for k in dict_node.keys
                ]
                output_keys = {"ans", "correct", "ds", "distractors", "options"}
                has_output = any(k in output_keys for k in str_keys if k)
                has_vars = "vars" in str_keys
                if has_output and not has_vars:
                    v_keys = [ast.Constant(value=v) for v in vars_list]
                    v_vals = [ast.Name(id=v, ctx=ast.Load()) for v in vars_list]
                    if "ans" not in vars_list:
                        if "ans" in str_keys:
                            idx_ans = str_keys.index("ans")
                            v_keys.append(ast.Constant(value="ans"))
                            v_vals.append(dict_node.values[idx_ans])
                        elif "correct" in str_keys:
                            idx_corr = str_keys.index("correct")
                            v_keys.append(ast.Constant(value="ans"))
                            v_vals.append(dict_node.values[idx_corr])
                    if v_keys:
                        vars_dict_node = ast.Dict(keys=v_keys, values=v_vals)
                        dict_node.keys.insert(0, ast.Constant(value="vars"))
                        dict_node.values.insert(0, vars_dict_node)
                        parent.modified = True
                return ret_node

            def _walk_stmts(stmts: List[ast.stmt], inherited_vars: List[str], inherited_seen: Set[str]) -> None:
                local_vars = list(inherited_vars)
                seen = set(inherited_seen)
                for idx, stmt in enumerate(stmts):
                    if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        continue
                    if isinstance(stmt, ast.Return):
                        stmts[idx] = _inject_return(stmt, local_vars)
                        continue
                    if isinstance(stmt, ast.Assign):
                        for tgt in stmt.targets:
                            self._extract_names(tgt, local_vars, seen)
                    elif isinstance(stmt, ast.AnnAssign):
                        self._extract_names(stmt.target, local_vars, seen)
                    elif isinstance(stmt, ast.If):
                        _walk_stmts(stmt.body, local_vars, seen)
                        _walk_stmts(stmt.orelse, local_vars, seen)
                    elif isinstance(stmt, (ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith)):
                        _walk_stmts(stmt.body, local_vars, seen)
                        if hasattr(stmt, "orelse") and stmt.orelse:
                            _walk_stmts(stmt.orelse, local_vars, seen)
                    elif isinstance(stmt, ast.Try):
                        _walk_stmts(stmt.body, local_vars, seen)
                        for h in stmt.handlers:
                            _walk_stmts(h.body, local_vars, seen)
                        _walk_stmts(stmt.orelse, local_vars, seen)
                        _walk_stmts(stmt.finalbody, local_vars, seen)

            _walk_stmts(fn_node.body, [], set())
            self.generic_visit(fn_node)
            return fn_node

        def _extract_names(self, tgt, out_list, seen):
            if isinstance(tgt, ast.Name):
                name = tgt.id
                if name not in seen and name not in _RESERVED_VAR_NAMES and not name.startswith("_"):
                    seen.add(name)
                    out_list.append(name)
            elif isinstance(tgt, (ast.Tuple, ast.List)):
                for elt in tgt.elts:
                    self._extract_names(elt, out_list, seen)

    try:
        transformer = _AutoVarsTransformer()
        new_tree = transformer.visit(tree)
        if not transformer.modified:
            return code_str
        ast.fix_missing_locations(new_tree)
        return ast.unparse(new_tree)
    except Exception:
        return code_str


def _wrap_gen_raw_with_auto_vars(raw_fn: Any, transformed_code: str) -> Any:
    """Wraps gen_raw callable so calls in compile_shard dry-runs return auto-exported 'vars'."""
    if not callable(raw_fn):
        return raw_fn
    compiled_fn = None
    if transformed_code and ("def generate_params(" in transformed_code or "def generate(" in transformed_code):
        try:
            fn_globals = getattr(raw_fn, "__globals__", None)
            ns = dict(fn_globals) if fn_globals is not None else {}
            exec(compile(transformed_code, "<gen_auto_vars>", "exec"), ns)
            candidate = ns.get("generate_params") or ns.get("generate")
            if callable(candidate):
                compiled_fn = candidate
        except Exception:
            compiled_fn = None

    def _auto_vars_wrapper(*args, **kwargs):
        res = None
        if compiled_fn is not None:
            try:
                res = compiled_fn(*args, **kwargs)
            except Exception as exc:
                if type(exc).__name__ in ("SandboxTimeoutError", "SecurityViolationError", "SandboxSecurityError"):
                    raise
                res = None
        if res is None:
            res = raw_fn(*args, **kwargs)

        if isinstance(res, dict) and "vars" not in res:
            c_val = res.get("correct") or res.get("ans") or ""
            res["vars"] = {"ans": c_val} if c_val else {}
        return res

    for attr in ("__name__", "__doc__", "__module__", "__qualname__"):
        if hasattr(raw_fn, attr):
            try:
                setattr(_auto_vars_wrapper, attr, getattr(raw_fn, attr))
            except Exception:
                pass
    target_for_trace = compiled_fn if compiled_fn is not None else raw_fn
    setattr(_auto_vars_wrapper, "__wrapped__", target_for_trace)
    return _auto_vars_wrapper


def extract_function_code(
    fn_or_str: Any,
    target_name: str,
    locator: Optional[ShardDataLineLocator] = None,
    fn_name_hint: Optional[str] = None,
    include_preamble: bool = True,
) -> str:
    """Extract and normalize Python code string for sandbox execution.

    Renames def <orig_name>( to def <target_name>( and ensures aliases:
    - generate_params -> generate = generate_params
    - verify -> cross_check = verify
    """
    raw_src = ""
    orig_name = getattr(fn_or_str, "__name__", fn_name_hint or "")
    if orig_name == "<lambda>" and fn_name_hint:
        orig_name = fn_name_hint
    if callable(fn_or_str):
        if locator and orig_name and hasattr(locator, "function_segments") and orig_name in locator.function_segments:
            raw_src = locator.function_segments[orig_name]
        elif locator and orig_name and orig_name in locator.functions:
            s, e = locator.functions[orig_name]
            raw_src = textwrap.dedent("\n".join(locator.lines[s - 1 : e]))
        else:
            try:
                raw_src = textwrap.dedent(inspect.getsource(fn_or_str))
            except Exception:
                if locator and orig_name and orig_name in locator.functions:
                    s, e = locator.functions[orig_name]
                    raw_src = textwrap.dedent("\n".join(locator.lines[s - 1 : e]))
                else:
                    raw_src = ""
    elif locator and orig_name and hasattr(locator, "function_segments") and orig_name in locator.function_segments:
        raw_src = locator.function_segments[orig_name]
    elif locator and orig_name and orig_name in locator.functions:
        s, e = locator.functions[orig_name]
        raw_src = textwrap.dedent("\n".join(locator.lines[s - 1 : e]))
    elif fn_or_str is None or (isinstance(fn_or_str, str) and not fn_or_str.strip()):
        if target_name == "verify":
            raw_src = "def verify(instance):\n    return True"
        else:
            raw_src = f"def {target_name}(rng):\n    return {{}}"
    elif isinstance(fn_or_str, str):
        raw_src = textwrap.dedent(fn_or_str)
    else:
        raw_src = str(fn_or_str)

    # Transform lambda assignment or lambda expression into standard def function
    converted_lambda = False
    if raw_src.strip():
        try:
            parsed_src = ast.parse(raw_src.strip())
            lambda_node = None
            if len(parsed_src.body) == 1:
                stmt = parsed_src.body[0]
                if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Lambda):
                    lambda_node = stmt.value
                elif isinstance(stmt, ast.AnnAssign) and isinstance(stmt.value, ast.Lambda):
                    lambda_node = stmt.value
                elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Lambda):
                    lambda_node = stmt.value
            if lambda_node is not None:
                new_fn = ast.FunctionDef(
                    name=target_name,
                    args=lambda_node.args,
                    body=[ast.Return(value=lambda_node.body)],
                    decorator_list=[],
                    returns=None,
                    lineno=1,
                )
                code_str = ast.unparse(new_fn)
                converted_lambda = True
        except Exception:
            pass

    if not converted_lambda:
        # Rename first function definition to target_name
        code_str = re.sub(r"^def\s+[A-Za-z0-9_]+\s*\(", f"def {target_name}(", raw_src, count=1, flags=re.MULTILINE)

    if target_name == "generate_params":
        code_str = inject_ast_auto_vars(code_str)

    # Alias bindings for sandbox execution
    if target_name == "generate_params":
        if "\ngenerate = " not in code_str and "def generate(" not in code_str:
            code_str = code_str.rstrip() + "\n\ngenerate = generate_params\n"
    elif target_name == "verify":
        if "\ncross_check = " not in code_str and "def cross_check(" not in code_str:
            code_str = code_str.rstrip() + "\n\ncross_check = verify\n"

    # Prepend pruned preamble (helpers, constants, allowed imports) if available
    if include_preamble and locator:
        preamble = ""
        has_pruned = False
        if orig_name and locator.source_text:
            try:
                preamble = prune_ast_preamble(locator.source_text, orig_name)
                has_pruned = True
            except Exception:
                has_pruned = False
                preamble = ""
        if not has_pruned:
            preamble = locator.get_preamble_code()
        if preamble:
            code_str = f"{preamble}\n\n{code_str}"

    return code_str




_CLONE_STEM_STOPWORDS: Set[str] = {
    "con", "del", "las", "los", "una", "uno", "por", "para", "que", "como",
    "sea", "dado", "dada", "the", "and", "for", "with",
}
_SYMPY_CLONE_CHECK_MODS: Set[str] = {
    "open_symbolic",
    "fill_in_the_blank",
    "multiple_choice_7_options",
}


def _extract_const_literal(node: Optional[ast.AST]) -> Tuple[bool, Any]:
    """Return (True, value) if AST node is a pure literal constant or simple negation/tuple."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, str, bool, type(None))):
        return True, node.value
    if (
        isinstance(node, ast.UnaryOp)
        and isinstance(node.op, ast.USub)
        and isinstance(node.operand, ast.Constant)
        and isinstance(node.operand.value, (int, float))
        and not isinstance(node.operand.value, bool)
    ):
        return True, -node.operand.value
    if isinstance(node, (ast.Tuple, ast.List, ast.Set)):
        items: List[Any] = []
        for elt in node.elts:
            ok, val = _extract_const_literal(elt)
            if not ok:
                return False, None
            items.append(val)
        return True, tuple(items) if isinstance(node, (ast.Tuple, ast.Set)) else items
    return False, None


def _const_value_to_ast(val: Any) -> Optional[ast.AST]:
    if isinstance(val, (int, float)) and not isinstance(val, bool) and val < 0:
        return ast.UnaryOp(op=ast.USub(), operand=ast.Constant(value=-val))
    if isinstance(val, (int, float, str, bool, type(None))):
        return ast.Constant(value=val)
    if isinstance(val, tuple):
        elts = [_const_value_to_ast(v) for v in val]
        if all(e is not None for e in elts):
            return ast.Tuple(elts=[e for e in elts if e is not None], ctx=ast.Load())
    if isinstance(val, list):
        elts = [_const_value_to_ast(v) for v in val]
        if all(e is not None for e in elts):
            return ast.List(elts=[e for e in elts if e is not None], ctx=ast.Load())
    return None


def _eval_const_if_test(test: ast.AST) -> Optional[bool]:
    ok, val = _extract_const_literal(test)
    if ok:
        return bool(val)
    if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not):
        inner = _eval_const_if_test(test.operand)
        return (not inner) if inner is not None else None
    if isinstance(test, ast.BoolOp):
        vals = [_eval_const_if_test(v) for v in test.values]
        if isinstance(test.op, ast.And):
            if any(v is False for v in vals):
                return False
            if all(v is True for v in vals):
                return True
        elif isinstance(test.op, ast.Or):
            if any(v is True for v in vals):
                return True
            if all(v is False for v in vals):
                return False
        return None
    if isinstance(test, ast.Compare) and len(test.ops) == 1 and len(test.comparators) == 1:
        ok_l, l_val = _extract_const_literal(test.left)
        ok_r, r_val = _extract_const_literal(test.comparators[0])
        if not (ok_l and ok_r):
            return None
        op = test.ops[0]
        try:
            if isinstance(op, ast.Eq):
                return l_val == r_val
            if isinstance(op, ast.NotEq):
                return l_val != r_val
            if isinstance(op, ast.Lt):
                return l_val < r_val
            if isinstance(op, ast.LtE):
                return l_val <= r_val
            if isinstance(op, ast.Gt):
                return l_val > r_val
            if isinstance(op, ast.GtE):
                return l_val >= r_val
            if isinstance(op, ast.In):
                return l_val in r_val
            if isinstance(op, ast.NotIn):
                return l_val not in r_val
        except Exception:
            return None
    return None


class _ConstBindingSubstitutor(ast.NodeTransformer):
    def __init__(self, bindings: Dict[str, ast.AST]):
        self.bindings = bindings

    def visit_Name(self, node: ast.Name) -> ast.AST:
        if isinstance(node.ctx, ast.Load) and node.id in self.bindings:
            return copy.deepcopy(self.bindings[node.id])
        return node

    def visit_IfExp(self, node: ast.IfExp) -> ast.AST:
        self.generic_visit(node)
        branch_val = _eval_const_if_test(node.test)
        if branch_val is True:
            return node.body
        if branch_val is False:
            return node.orelse
        return node


def _prune_const_if_stmts(stmts: List[ast.stmt]) -> List[ast.stmt]:
    out: List[ast.stmt] = []
    for stmt in stmts:
        if isinstance(stmt, ast.If):
            branch_val = _eval_const_if_test(stmt.test)
            if branch_val is True:
                pruned = _prune_const_if_stmts(stmt.body)
                out.extend(pruned)
                if pruned and isinstance(pruned[-1], ast.Return):
                    break
                continue
            if branch_val is False:
                pruned = _prune_const_if_stmts(stmt.orelse)
                out.extend(pruned)
                if pruned and isinstance(pruned[-1], ast.Return):
                    break
                continue
            stmt_c = copy.copy(stmt)
            stmt_c.body = _prune_const_if_stmts(stmt.body)
            stmt_c.orelse = _prune_const_if_stmts(stmt.orelse)
            out.append(stmt_c)
        elif isinstance(stmt, (ast.For, ast.AsyncFor, ast.While)):
            stmt_c = copy.copy(stmt)
            stmt_c.body = _prune_const_if_stmts(stmt.body)
            stmt_c.orelse = _prune_const_if_stmts(stmt.orelse)
            out.append(stmt_c)
        elif isinstance(stmt, (ast.With, ast.AsyncWith)):
            stmt_c = copy.copy(stmt)
            stmt_c.body = _prune_const_if_stmts(stmt.body)
            out.append(stmt_c)
        else:
            out.append(stmt)
            if isinstance(stmt, ast.Return):
                break
    return out


def _specialize_gen_ast(
    fn_node: Union[ast.FunctionDef, ast.AsyncFunctionDef],
    ast_funcs: Dict[str, Union[ast.FunctionDef, ast.AsyncFunctionDef]],
    max_depth: int = 3,
) -> Union[ast.FunctionDef, ast.AsyncFunctionDef]:
    """Inline single-return helper wrappers (e.g. `def gen_2(r): return _g(r, 2)`) and prune constant branches."""
    cur = copy.deepcopy(fn_node)
    seen_helpers: Set[str] = set()
    for _ in range(max_depth):
        body = list(cur.body)
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
            body = body[1:]
        if (
            len(body) != 1
            or not isinstance(body[0], ast.Return)
            or not isinstance(body[0].value, ast.Call)
            or not isinstance(body[0].value.func, ast.Name)
        ):
            break
        call = body[0].value
        helper_name = call.func.id
        if helper_name == cur.name or helper_name not in ast_funcs:
            break
        if any(isinstance(a, ast.Starred) for a in call.args) or any(kw.arg is None for kw in call.keywords):
            break

        helper = copy.deepcopy(ast_funcs[helper_name])
        pos_params = [a.arg for a in getattr(helper.args, "posonlyargs", []) + helper.args.args]
        kwonly_params = [a.arg for a in getattr(helper.args, "kwonlyargs", [])]
        bound_exprs: Dict[str, ast.AST] = {}
        for idx_p, arg_node in enumerate(call.args):
            if idx_p < len(pos_params):
                bound_exprs[pos_params[idx_p]] = arg_node
        for kw in call.keywords:
            if kw.arg in pos_params or kw.arg in kwonly_params:
                bound_exprs[kw.arg] = kw.value

        defaults = list(helper.args.defaults or [])
        if defaults:
            for p_name, d_node in zip(pos_params[len(pos_params) - len(defaults):], defaults):
                if p_name not in bound_exprs:
                    bound_exprs[p_name] = d_node
        kw_defaults = list(getattr(helper.args, "kw_defaults", []) or [])
        for p_name, d_node in zip(kwonly_params, kw_defaults):
            if p_name not in bound_exprs and d_node is not None:
                bound_exprs[p_name] = d_node

        assigned_names = {
            sub.id
            for sub in ast.walk(helper)
            if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Store)
        }
        const_ast_bindings: Dict[str, ast.AST] = {}
        bound_const_params: Set[str] = set()
        for p_name, val_node in bound_exprs.items():
            if p_name in assigned_names:
                continue
            ok_c, c_val = _extract_const_literal(val_node)
            if ok_c:
                c_ast = _const_value_to_ast(c_val)
                if c_ast is not None:
                    const_ast_bindings[p_name] = c_ast
                    bound_const_params.add(p_name)

        param_renames: Dict[str, ast.AST] = {}
        can_passthrough = True
        for p_name, val_node in bound_exprs.items():
            if p_name in bound_const_params:
                continue
            if isinstance(val_node, ast.Name) and p_name not in assigned_names:
                continue
            else:
                can_passthrough = False
                break
        if not const_ast_bindings and not (can_passthrough and bound_exprs):
            break
        if not const_ast_bindings and helper_name in seen_helpers:
            break
        seen_helpers.add(helper_name)

        helper = _ConstBindingSubstitutor({**const_ast_bindings, **param_renames}).visit(helper)
        helper.body = _prune_const_if_stmts(helper.body)
        drop_params = bound_const_params | set(param_renames)
        helper.args.posonlyargs = [a for a in helper.args.posonlyargs if a.arg not in drop_params]
        helper.args.args = [a for a in helper.args.args if a.arg not in drop_params]
        helper.args.kwonlyargs = [a for a in helper.args.kwonlyargs if a.arg not in drop_params]
        helper.args.defaults = []
        helper.args.kw_defaults = []
        ast.fix_missing_locations(helper)
        cur = helper

    if cur.body and isinstance(cur.body[0], ast.Expr) and isinstance(cur.body[0].value, ast.Constant) and isinstance(cur.body[0].value.value, str):
        cur.body = cur.body[1:]
    return cur


class _CanonicalGenASTNormalizer(ast.NodeTransformer):
    """Normalizes generator ASTs: renames args/locals and masks numeric literals."""

    def __init__(self, fn_node: Union[ast.FunctionDef, ast.AsyncFunctionDef]):
        self.param_map: Dict[str, str] = {}
        self.local_map: Dict[str, str] = {}

        all_params = (
            list(getattr(fn_node.args, "posonlyargs", []))
            + list(fn_node.args.args)
            + list(getattr(fn_node.args, "kwonlyargs", []))
        )
        for p in all_params:
            if p.arg not in self.param_map:
                self.param_map[p.arg] = f"arg{len(self.param_map)}"
        if fn_node.args.vararg and fn_node.args.vararg.arg not in self.param_map:
            self.param_map[fn_node.args.vararg.arg] = f"arg{len(self.param_map)}"
        if fn_node.args.kwarg and fn_node.args.kwarg.arg not in self.param_map:
            self.param_map[fn_node.args.kwarg.arg] = f"arg{len(self.param_map)}"

        self._collect_locals(fn_node.body)

    def _register_local(self, name: Optional[str]) -> None:
        if name and name not in self.param_map and name not in self.local_map:
            self.local_map[name] = f"v{len(self.local_map)}"

    def _collect_target(self, node: Optional[ast.AST]) -> None:
        if node is None:
            return
        if isinstance(node, ast.Name):
            self._register_local(node.id)
        elif isinstance(node, (ast.Tuple, ast.List)):
            for elt in node.elts:
                self._collect_target(elt)
        elif isinstance(node, ast.Starred):
            self._collect_target(node.value)

    def _collect_locals(self, node: Any) -> None:
        if node is None:
            return
        if isinstance(node, list):
            for item in node:
                self._collect_locals(item)
            return
        if not isinstance(node, ast.AST):
            return
        if isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp)):
            for gen in node.generators:
                self._collect_target(gen.target)
                self._collect_locals(gen.iter)
                self._collect_locals(gen.ifs)
            self._collect_locals(node.elt)
            return
        if isinstance(node, ast.DictComp):
            for gen in node.generators:
                self._collect_target(gen.target)
                self._collect_locals(gen.iter)
                self._collect_locals(gen.ifs)
            self._collect_locals(node.key)
            self._collect_locals(node.value)
            return
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                self._collect_target(tgt)
            self._collect_locals(node.value)
            return
        if isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            self._collect_target(node.target)
            self._collect_locals(node.value)
            return
        if isinstance(node, (ast.For, ast.AsyncFor)):
            self._collect_target(node.target)
            self._collect_locals(node.iter)
            self._collect_locals(node.body)
            self._collect_locals(node.orelse)
            return
        if isinstance(node, ast.NamedExpr):
            self._collect_target(node.target)
            self._collect_locals(node.value)
            return
        if isinstance(node, ast.ExceptHandler):
            self._register_local(node.name)
            self._collect_locals(node.body)
            return
        if isinstance(node, ast.withitem):
            self._collect_target(node.optional_vars)
            self._collect_locals(node.context_expr)
            return
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            self._register_local(node.id)
        for child in ast.iter_child_nodes(node):
            self._collect_locals(child)

    def normalize(self, fn_node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> ast.AST:
        cloned = copy.deepcopy(fn_node)
        return ast.fix_missing_locations(self.visit(cloned))

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.AST:
        node.name = "_gen_fn"
        node.decorator_list = []
        node.returns = None
        node.type_comment = None
        self.generic_visit(node)
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AST:
        node.name = "_gen_fn"
        node.decorator_list = []
        node.returns = None
        node.type_comment = None
        self.generic_visit(node)
        return node

    def visit_arg(self, node: ast.arg) -> ast.AST:
        node.arg = self.param_map.get(node.arg, node.arg)
        node.annotation = None
        node.type_comment = None
        return node

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> ast.AST:
        if node.name and node.name in self.local_map:
            node.name = self.local_map[node.name]
        self.generic_visit(node)
        return node

    def visit_Name(self, node: ast.Name) -> ast.AST:
        if node.id in self.param_map:
            node.id = self.param_map[node.id]
        elif node.id in self.local_map:
            node.id = self.local_map[node.id]
        return node

    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return ast.Constant(value="__NUM__")
        if isinstance(node.value, str) and re.fullmatch(r"D[-_][A-Za-z0-9_-]*\d+", node.value.strip()):
            return ast.Constant(value="__DID__")
        return node

    def visit_Dict(self, node: ast.Dict) -> ast.AST:
        new_keys: List[Optional[ast.expr]] = []
        new_vals: List[ast.expr] = []
        for k_node, v_node in zip(node.keys, node.values):
            norm_k = self.visit(k_node) if k_node is not None else None
            if (
                isinstance(k_node, ast.Constant)
                and k_node.value == "vars"
                and isinstance(v_node, ast.Dict)
            ):
                vars_keys: List[Optional[ast.expr]] = []
                vars_vals: List[ast.expr] = []
                for vk, vv in zip(v_node.keys, v_node.values):
                    if (
                        isinstance(vk, ast.Constant)
                        and isinstance(vk.value, str)
                        and vk.value != "ans"
                        and vk.value in self.local_map
                    ):
                        vars_keys.append(ast.Constant(value=self.local_map[vk.value]))
                    else:
                        vars_keys.append(self.visit(vk) if vk is not None else None)
                    vars_vals.append(self.visit(vv))
                norm_v: ast.expr = ast.Dict(keys=vars_keys, values=vars_vals)
            elif (
                isinstance(k_node, ast.Constant)
                and k_node.value in ("ds", "distractors")
                and isinstance(v_node, (ast.List, ast.Tuple))
            ):
                norm_elts: List[ast.expr] = []
                for elt in v_node.elts:
                    if isinstance(elt, (ast.Tuple, ast.List)) and len(elt.elts) == 3:
                        elt.elts = [
                            self.visit(elt.elts[0]),
                            self.visit(elt.elts[1]),
                            ast.Constant(value="__RAT__"),
                        ]
                        norm_elts.append(elt)
                    else:
                        norm_elts.append(self.visit(elt))
                v_node.elts = norm_elts
                norm_v = v_node
            else:
                norm_v = self.visit(v_node)
            new_keys.append(norm_k)
            new_vals.append(norm_v)
        node.keys = new_keys
        node.values = new_vals
        return node


def _extract_pure_sympy_expr(fn_node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> Any:
    """Safely extract a pure SymPy algebraic expression for 'correct'/'ans' from a branchless generator AST."""
    try:
        import sympy
    except Exception:
        return None

    env: Dict[str, Any] = {}
    sampled_syms: List[Any] = []

    def _new_sym() -> Any:
        sym = sympy.Symbol(f"_p{len(sampled_syms)}", real=True)
        sampled_syms.append(sym)
        return sym

    def _eval_expr(node: Optional[ast.AST]) -> Any:
        if node is None:
            return None
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                return sympy.Rational(str(node.value)) if isinstance(node.value, float) else sympy.Integer(node.value)
            if isinstance(node.value, str):
                toks = re.findall(r"@([A-Za-z_][A-Za-z0-9_]*)(?::[^@]+)?@", node.value)
                if len(toks) == 1 and toks[0] in env:
                    return env[toks[0]]
            return None
        if isinstance(node, ast.JoinedStr):
            fvs = [v.value for v in node.values if isinstance(v, ast.FormattedValue)]
            return _eval_expr(fvs[0]) if len(fvs) == 1 else None
        if isinstance(node, ast.Name):
            return env.get(node.id)
        if isinstance(node, ast.UnaryOp):
            operand = _eval_expr(node.operand)
            if operand is None:
                return None
            if isinstance(node.op, ast.USub):
                return -operand
            if isinstance(node.op, ast.UAdd):
                return operand
            return None
        if isinstance(node, ast.BinOp):
            left = _eval_expr(node.left)
            right = _eval_expr(node.right)
            if left is None or right is None:
                return None
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, (ast.Div, ast.FloorDiv)):
                if right == 0:
                    return None
                return left / right
            if isinstance(node.op, ast.Pow):
                if getattr(right, "is_Number", False) and abs(float(right)) > 64:
                    return None
                return left ** right
            return None
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and node.func.attr in (
                "randint", "randrange", "uniform", "choice", "randbelow"
            ):
                return _new_sym()
            if isinstance(node.func, ast.Name) and node.func.id in ("str", "fmt", "round", "int", "float"):
                if node.args:
                    return _eval_expr(node.args[0])
                return None
            if (
                (isinstance(node.func, ast.Attribute) and node.func.attr == "sqrt")
                or (isinstance(node.func, ast.Name) and node.func.id == "sqrt")
            ) and len(node.args) == 1:
                inner = _eval_expr(node.args[0])
                return sympy.sqrt(inner) if inner is not None else None
            return None
        return None

    def _assign_target(tgt: ast.AST, val_node: ast.AST) -> bool:
        if isinstance(tgt, ast.Name):
            expr_val = _eval_expr(val_node)
            if expr_val is not None:
                env[tgt.id] = expr_val
            return True
        if isinstance(tgt, (ast.Tuple, ast.List)) and isinstance(val_node, (ast.Tuple, ast.List)):
            if len(tgt.elts) != len(val_node.elts):
                return False
            for sub_t, sub_v in zip(tgt.elts, val_node.elts):
                if not _assign_target(sub_t, sub_v):
                    return False
            return True
        return False

    for stmt in fn_node.body:
        if isinstance(stmt, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try)):
            return None
        if isinstance(stmt, ast.Assign):
            if len(stmt.targets) != 1:
                return None
            if not _assign_target(stmt.targets[0], stmt.value):
                return None
        elif isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Dict):
            dict_map: Dict[str, ast.expr] = {}
            for k_n, v_n in zip(stmt.value.keys, stmt.value.values):
                if isinstance(k_n, ast.Constant) and isinstance(k_n.value, str):
                    dict_map[k_n.value] = v_n
            for ck in ("correct", "ans"):
                if ck in dict_map:
                    c_expr = _eval_expr(dict_map[ck])
                    if c_expr is not None:
                        return c_expr
            vars_node = dict_map.get("vars")
            if isinstance(vars_node, ast.Dict):
                for vk_n, vv_n in zip(vars_node.keys, vars_node.values):
                    if isinstance(vk_n, ast.Constant) and vk_n.value == "ans":
                        return _eval_expr(vv_n)
                last_dep = None
                for vk_n, vv_n in zip(vars_node.keys, vars_node.values):
                    val_e = _eval_expr(vv_n)
                    if val_e is not None and getattr(val_e, "free_symbols", None):
                        last_dep = val_e
                return last_dep
            return None
    return None


def _clone_correct_str(res: Dict[str, Any]) -> str:
    raw = res.get("correct", res.get("ans", ""))
    if isinstance(raw, dict):
        raw = raw.get("expression") or raw.get("value") or raw.get("canonical_algebraic") or ""
    return str(raw)


def _canon_syms(expr: Any) -> Any:
    syms = sorted(getattr(expr, "free_symbols", set()), key=lambda x: x.name)
    if not syms:
        return expr
    import sympy
    tmp = {sy: sympy.Symbol(f"__t{k}") for k, sy in enumerate(syms)}
    out = expr.subs(tmp)
    return out.subs({sympy.Symbol(f"__t{k}"): sympy.Symbol(f"x{k}") for k in range(len(syms))})


def _sympy_to_z3_expr(
    expr: Any,
    var_map: Dict[str, Any],
    extra_constraints: List[Any],
    aux_counter: List[int],
) -> Optional[Any]:
    """Translate a bounded algebraic/piecewise SymPy expression into a Z3 Real expression."""
    import sympy
    import z3

    _TRANSCENDENTALS = (
        sympy.exp,
        sympy.log,
        sympy.sin,
        sympy.cos,
        sympy.tan,
        sympy.cot,
        sympy.sec,
        sympy.csc,
        sympy.asin,
        sympy.acos,
        sympy.atan,
        sympy.sinh,
        sympy.cosh,
        sympy.tanh,
    )
    if isinstance(expr, _TRANSCENDENTALS):
        return None
    if isinstance(expr, sympy.Symbol):
        name = expr.name
        if name not in var_map:
            var_map[name] = z3.Real(name)
        return var_map[name]
    if isinstance(expr, sympy.Integer):
        return z3.RealVal(int(expr))
    if isinstance(expr, sympy.Rational):
        return z3.Q(int(expr.p), int(expr.q))
    if isinstance(expr, sympy.Float):
        frac = sympy.Rational(str(expr))
        return z3.Q(int(frac.p), int(frac.q))
    if expr is sympy.S.Zero:
        return z3.RealVal(0)
    if expr is sympy.S.One:
        return z3.RealVal(1)
    if expr is sympy.S.NegativeOne:
        return z3.RealVal(-1)
    if expr is sympy.S.Half:
        return z3.Q(1, 2)

    if isinstance(expr, sympy.Add):
        acc = None
        for arg in expr.args:
            sub = _sympy_to_z3_expr(arg, var_map, extra_constraints, aux_counter)
            if sub is None:
                return None
            acc = sub if acc is None else (acc + sub)
        return acc

    if isinstance(expr, sympy.Mul):
        acc = None
        for arg in expr.args:
            sub = _sympy_to_z3_expr(arg, var_map, extra_constraints, aux_counter)
            if sub is None:
                return None
            acc = sub if acc is None else (acc * sub)
        return acc

    if isinstance(expr, sympy.Pow):
        base_s, exp_s = expr.args
        base_z = _sympy_to_z3_expr(base_s, var_map, extra_constraints, aux_counter)
        if base_z is None:
            return None
        if isinstance(exp_s, sympy.Integer):
            n = int(exp_s)
            if abs(n) > 8:
                return None
            if n == 0:
                return z3.RealVal(1)
            if n > 0:
                return base_z ** n
            denom = base_z ** (-n)
            extra_constraints.append(denom != 0)
            return z3.RealVal(1) / denom
        if exp_s == sympy.Rational(1, 2):
            aux_idx = aux_counter[0]
            aux_counter[0] += 1
            root_var = z3.Real(f"__z3_sqrt_{aux_idx}")
            extra_constraints.append(base_z >= 0)
            extra_constraints.append(root_var >= 0)
            extra_constraints.append(root_var * root_var == base_z)
            return root_var
        if exp_s == sympy.Rational(-1, 2):
            aux_idx = aux_counter[0]
            aux_counter[0] += 1
            root_var = z3.Real(f"__z3_sqrt_{aux_idx}")
            extra_constraints.append(base_z > 0)
            extra_constraints.append(root_var > 0)
            extra_constraints.append(root_var * root_var == base_z)
            return z3.RealVal(1) / root_var
        return None

    if isinstance(expr, sympy.Abs):
        arg_z = _sympy_to_z3_expr(expr.args[0], var_map, extra_constraints, aux_counter)
        if arg_z is None:
            return None
        return z3.If(arg_z >= 0, arg_z, -arg_z)

    if isinstance(expr, sympy.Min) and len(expr.args) >= 2:
        args_z = [_sympy_to_z3_expr(a, var_map, extra_constraints, aux_counter) for a in expr.args]
        if any(a is None for a in args_z):
            return None
        cur = args_z[0]
        for nxt in args_z[1:]:
            cur = z3.If(cur <= nxt, cur, nxt)
        return cur

    if isinstance(expr, sympy.Max) and len(expr.args) >= 2:
        args_z = [_sympy_to_z3_expr(a, var_map, extra_constraints, aux_counter) for a in expr.args]
        if any(a is None for a in args_z):
            return None
        cur = args_z[0]
        for nxt in args_z[1:]:
            cur = z3.If(cur >= nxt, cur, nxt)
        return cur

    if isinstance(expr, sympy.Piecewise):
        return _sympy_piecewise_to_z3(expr.args, var_map, extra_constraints, aux_counter)

    return None


def _sympy_rel_to_z3(
    cond: Any,
    var_map: Dict[str, Any],
    extra_constraints: List[Any],
    aux_counter: List[int],
) -> Optional[Any]:
    """Translate SymPy boolean/relational condition into a Z3 boolean formula."""
    import sympy
    from sympy.core.relational import Relational
    import z3

    if cond is True or cond is sympy.S.true:
        return z3.BoolVal(True)
    if cond is False or cond is sympy.S.false:
        return z3.BoolVal(False)
    if isinstance(cond, sympy.And):
        parts = [_sympy_rel_to_z3(a, var_map, extra_constraints, aux_counter) for a in cond.args]
        return None if any(p is None for p in parts) else z3.And(*parts)
    if isinstance(cond, sympy.Or):
        parts = [_sympy_rel_to_z3(a, var_map, extra_constraints, aux_counter) for a in cond.args]
        return None if any(p is None for p in parts) else z3.Or(*parts)
    if isinstance(cond, sympy.Not):
        sub = _sympy_rel_to_z3(cond.args[0], var_map, extra_constraints, aux_counter)
        return None if sub is None else z3.Not(sub)
    if isinstance(cond, Relational):
        lhs = _sympy_to_z3_expr(cond.lhs, var_map, extra_constraints, aux_counter)
        rhs = _sympy_to_z3_expr(cond.rhs, var_map, extra_constraints, aux_counter)
        if lhs is None or rhs is None:
            return None
        rel_op = cond.rel_op
        if rel_op == "==":
            return lhs == rhs
        if rel_op == "!=":
            return lhs != rhs
        if rel_op == "<":
            return lhs < rhs
        if rel_op == "<=":
            return lhs <= rhs
        if rel_op == ">":
            return lhs > rhs
        if rel_op == ">=":
            return lhs >= rhs
    return None


def _sympy_piecewise_to_z3(
    pairs: Tuple[Any, ...],
    var_map: Dict[str, Any],
    extra_constraints: List[Any],
    aux_counter: List[int],
) -> Optional[Any]:
    """Translate SymPy Piecewise (val, cond) branches recursively into nested z3.If."""
    if not pairs:
        return None
    import sympy
    import z3

    val_s, cond_s = pairs[0]
    cond_z = _sympy_rel_to_z3(cond_s, var_map, extra_constraints, aux_counter)
    if cond_z is None:
        return None
    val_constraints: List[Any] = []
    val_z = _sympy_to_z3_expr(val_s, var_map, val_constraints, aux_counter)
    if val_z is None:
        return None
    if len(pairs) == 1:
        is_always_true = cond_s is True or cond_s is sympy.S.true
        if val_constraints:
            if is_always_true:
                extra_constraints.extend(val_constraints)
            else:
                extra_constraints.append(z3.Implies(cond_z, z3.And(*val_constraints)))
        if not is_always_true:
            extra_constraints.append(cond_z)
        return val_z
    rest_constraints: List[Any] = []
    rest_z = _sympy_piecewise_to_z3(pairs[1:], var_map, rest_constraints, aux_counter)
    if rest_z is None:
        return None
    if val_constraints:
        extra_constraints.append(z3.Implies(cond_z, z3.And(*val_constraints)))
    if rest_constraints:
        extra_constraints.append(z3.Implies(z3.Not(cond_z), z3.And(*rest_constraints)))
    return z3.If(cond_z, val_z, rest_z)


def _z3_check_sympy_equiv(expr_i: Any, expr_j: Any, timeout_ms: int = 150) -> Optional[bool]:
    """Check positive-domain algebraic equivalence via Z3 with silent fallback on unsupported ASTs."""
    try:
        import z3
    except ImportError:
        return None

    try:
        var_map: Dict[str, Any] = {}
        extra_constraints: List[Any] = []
        aux_counter = [0]
        z_i = _sympy_to_z3_expr(expr_i, var_map, extra_constraints, aux_counter)
        z_j = _sympy_to_z3_expr(expr_j, var_map, extra_constraints, aux_counter)
        if z_i is None or z_j is None or not var_map:
            return None

        solver = z3.Solver()
        solver.set("timeout", timeout_ms)
        for v in var_map.values():
            solver.add(v > 0)
        for c in extra_constraints:
            solver.add(c)
        if solver.check() != z3.sat:
            return None
        solver.add(z_i != z_j)
        res = solver.check()
        if res == z3.unsat:
            return True
        if res == z3.sat:
            return False
        return None
    except Exception:
        return None


def _check_intra_competency_anti_clone(
    cid: str,
    source_name: str,
    tpls: List[Dict[str, Any]],
    gen_callables: List[Any],
    cid_ast_funcs: Dict[str, Union[ast.FunctionDef, ast.AsyncFunctionDef]],
    eff_k: int,
    norm_shard_id: str,
    warnings_out: Optional[List[str]] = None,
) -> List[str]:
    """Enforce the 4 deterministic anti-clone gates within a competency."""
    if len(tpls) < 2:
        return []

    errors: List[str] = []

    def _norm_mod(t: Dict[str, Any]) -> str:
        raw_m = str(t.get("interaction_type") or t.get("question_type") or "").strip().lower()
        return _QTYPE_TO_INTERACTION.get(raw_m, raw_m)

    def _tpl_id(t: Dict[str, Any], idx: int) -> str:
        return str(t.get("id") or t.get("template_id") or f"T-{cid}-{idx + 1:02d}")

    def _resolve_gen_ast(t: Dict[str, Any]) -> Optional[Union[ast.FunctionDef, ast.AsyncFunctionDef]]:
        g_name = t.get("gen_fn_name")
        if g_name and g_name in cid_ast_funcs:
            return cid_ast_funcs[g_name]
        gen_src = t.get("generator_code") or t.get("generate_py") or ""
        if not gen_src:
            return None
        try:
            tree = ast.parse(textwrap.dedent(str(gen_src).strip()))
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.name == "generate_params":
                        return node
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    return node
        except Exception:
            return None
        return None

    def _stem_tokens(t: Dict[str, Any]) -> Set[str]:
        svs = t.get("stem_variants") or ([t.get("stem_es")] if t.get("stem_es") else [])
        combined = " ".join(str(s) for s in svs if s)
        cleaned = re.sub(r"@[A-Za-z0-9_]+(?::[^@]+)?@", " ", combined)
        cleaned = re.sub(r"\{[A-Za-z0-9_]+\}", " ", cleaned)
        cleaned = re.sub(r"\\[A-Za-z]+", " ", cleaned)
        cleaned = re.sub(r"\d+(?:\.\d+)?", " ", cleaned)
        words = re.findall(r"[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]{3,}", cleaned.lower())
        return {w for w in words if w not in _CLONE_STEM_STOPWORDS}

    # Gate 2: [TPL-CLONE-BAND] unique (archetype, difficulty, bloom) per modality when eff_k <= 4
    if eff_k <= 4:
        by_mod: Dict[str, List[Tuple[int, Dict[str, Any]]]] = defaultdict(list)
        for idx_t, t_item in enumerate(tpls):
            mod_name = _norm_mod(t_item)
            if mod_name:
                by_mod[mod_name].append((idx_t, t_item))
        for mod_name, group in by_mod.items():
            if len(group) > 4:
                continue
            seen_bands: Dict[Tuple[str, str, str], str] = {}
            for idx_t, t_item in group:
                tid = _tpl_id(t_item, idx_t)
                arch = str(t_item.get("archetype") or "").strip().lower()
                diff = str(t_item.get("difficulty") or "").strip().lower()
                blm = str(t_item.get("bloom") or "").strip().lower()
                if not (arch and diff and blm):
                    continue
                band_key = (arch, diff, blm)
                if band_key in seen_bands:
                    prev_tid = seen_bands[band_key]
                    errors.append(
                        f"{cid}.json ({source_name}): [TPL-CLONE-BAND] Plantillas '{prev_tid}' y '{tid}' "
                        f"en '{cid}' ({mod_name}) repiten exactamente la tupla (archetype={arch!r}, "
                        f"difficulty={diff!r}, bloom={blm!r}). Diferencia al menos arquetipo, dificultad o Bloom."
                    )
                else:
                    seen_bands[band_key] = tid

    # Precompute normalized ASTs, stem token sets, and pure SymPy expressions
    norm_ast_dumps: List[Optional[str]] = []
    sympy_ast_exprs: List[Any] = []
    stem_token_sets: List[Set[str]] = []
    mods: List[str] = []
    archs: List[str] = []
    tids: List[str] = []

    for idx_t, t_item in enumerate(tpls):
        mods.append(_norm_mod(t_item))
        archs.append(str(t_item.get("archetype") or "").strip().lower())
        tids.append(_tpl_id(t_item, idx_t))
        stem_token_sets.append(_stem_tokens(t_item))

        raw_fn = _resolve_gen_ast(t_item)
        if raw_fn is not None:
            try:
                spec_fn = _specialize_gen_ast(raw_fn, cid_ast_funcs)
                norm_fn = _CanonicalGenASTNormalizer(spec_fn).normalize(spec_fn)
                norm_ast_dumps.append(ast.dump(norm_fn))
                sympy_ast_exprs.append(_extract_pure_sympy_expr(spec_fn))
            except Exception:
                norm_ast_dumps.append(None)
                sympy_ast_exprs.append(None)
        else:
            norm_ast_dumps.append(None)
            sympy_ast_exprs.append(None)

    eval_cache: Dict[Tuple[int, int], Optional[Dict[str, Any]]] = {}

    def _eval_tpl_seed(t_idx: int, seed_val: int) -> Optional[Dict[str, Any]]:
        key = (t_idx, seed_val)
        if key in eval_cache:
            return eval_cache[key]
        res_out: Optional[Dict[str, Any]] = None
        c_call = gen_callables[t_idx] if t_idx < len(gen_callables) else None
        if callable(c_call):
            try:
                import random
                from engine.sandbox import call_with_timeout, _LazyNPRNG
                EvaluationContext.set(
                    template_id=tids[t_idx],
                    gen_fn=tpls[t_idx].get("gen_fn_name") or "gen_fn",
                    archetype=t_idx + 1,
                    seed=seed_val,
                )
                rng = random.Random(seed_val)
                try:
                    rng.np = _LazyNPRNG(seed_val)
                except Exception:
                    pass
                r_val = call_with_timeout(c_call, args=(rng,), timeout=0.4, seed=seed_val)
                if isinstance(r_val, dict):
                    res_out = r_val
            except Exception:
                res_out = None
            finally:
                EvaluationContext.reset(norm_shard_id)
        if res_out is None:
            gen_c = tpls[t_idx].get("generator_code") or tpls[t_idx].get("generate_py") or ""
            if gen_c:
                try:
                    from engine.sandbox import run_code_in_env
                    r_val = run_code_in_env(gen_c, "generate", seed=seed_val, timeout=0.5)
                    if isinstance(r_val, dict):
                        res_out = r_val
                except Exception:
                    res_out = None
        eval_cache[key] = res_out
        return res_out

    def _sympy_expr_equiv_from_strings(s1: str, s2: str) -> Optional[bool]:
        c1 = s1.strip().strip("$").strip()
        c2 = s2.strip().strip("$").strip()
        if not c1 or not c2 or len(c1) > 120 or len(c2) > 120:
            return None
        try:
            import sympy
            from sympy.parsing.sympy_parser import (
                convert_xor,
                implicit_multiplication_application,
                parse_expr,
                standard_transformations,
            )
            trans = standard_transformations + (implicit_multiplication_application, convert_xor)
            e1 = parse_expr(c1, transformations=trans)
            e2 = parse_expr(c2, transformations=trans)
            if not (getattr(e1, "free_symbols", None) or getattr(e2, "free_symbols", None)):
                return None
            syms1 = sorted(e1.free_symbols, key=lambda s: s.name)
            syms2 = sorted(e2.free_symbols, key=lambda s: s.name)
            if len(syms1) != len(syms2):
                return False
            canon_syms = [sympy.Symbol(f"x{k}") for k in range(len(syms1))]
            e1_c = e1.subs(list(zip(syms1, canon_syms)))
            e2_c = e2.subs(list(zip(syms2, canon_syms)))
            return sympy.simplify(e1_c - e2_c) == 0
        except Exception:
            return None

    for i in range(len(tpls)):
        for j in range(i + 1, len(tpls)):
            same_mod = bool(mods[i] and mods[i] == mods[j])
            same_arch = bool(archs[i] and archs[i] == archs[j])
            if not (same_mod or same_arch):
                continue

            # Gate 1: [TPL-CLONE-AST]
            if norm_ast_dumps[i] is not None and norm_ast_dumps[i] == norm_ast_dumps[j]:
                errors.append(
                    f"{cid}.json ({source_name}): [TPL-CLONE-AST] Plantillas '{tids[i]}' y '{tids[j]}' "
                    f"en '{cid}' tienen AST normalizado idéntico en 'gen' (posible clon por renombre de variables o constantes). "
                    f"Implementa lógica o formulación matemática distinta."
                )

            # Gate 3: [TPL-CLONE-STEM]
            ti, tj = stem_token_sets[i], stem_token_sets[j]
            if ti and tj:
                jacc = len(ti & tj) / float(len(ti | tj))
                if jacc >= 0.70:
                    errors.append(
                        f"{cid}.json ({source_name}): [TPL-CLONE-STEM] Plantillas '{tids[i]}' y '{tids[j]}' "
                        f"en '{cid}' presentan stem_variants casi idénticos (Jaccard={jacc:.3f} >= 0.70). "
                        f"Reescribe la redacción y estructura sintáctica de los enunciados."
                    )

            # Gate 4: [TPL-CLONE-SYMPY] intra-archetype symbolic/algebraic equivalence
            if same_arch and mods[i] in _SYMPY_CLONE_CHECK_MODS and mods[j] in _SYMPY_CLONE_CHECK_MODS:
                sympy_clone_detected = False
                if "open_symbolic" in (mods[i], mods[j]):
                    eq_42 = None
                    eq_43 = None
                    r42_i = _eval_tpl_seed(i, 42)
                    r42_j = _eval_tpl_seed(j, 42)
                    if r42_i and r42_j:
                        eq_42 = _sympy_expr_equiv_from_strings(_clone_correct_str(r42_i), _clone_correct_str(r42_j))
                    if eq_42 is True:
                        r43_i = _eval_tpl_seed(i, 43)
                        r43_j = _eval_tpl_seed(j, 43)
                        if r43_i and r43_j:
                            eq_43 = _sympy_expr_equiv_from_strings(_clone_correct_str(r43_i), _clone_correct_str(r43_j))
                    if eq_42 is True and eq_43 is True:
                        sympy_clone_detected = True
                        errors.append(
                            f"{cid}.json ({source_name}): [TPL-CLONE-SYMPY] Plantillas '{tids[i]}' y '{tids[j]}' "
                            f"en '{cid}' (arquetipo '{archs[i]}') producen expresiones simbólicas equivalentes "
                            f"en SymPy (seeds 42 y 43). Usa expresiones genuinamente distintas."
                        )

                if (
                    not sympy_clone_detected
                    and mods[i] in ("fill_in_the_blank", "multiple_choice_7_options")
                    and mods[j] in ("fill_in_the_blank", "multiple_choice_7_options")
                ):
                    s_expr_i = sympy_ast_exprs[i]
                    s_expr_j = sympy_ast_exprs[j]
                    if (
                        s_expr_i is not None
                        and s_expr_j is not None
                        and getattr(s_expr_i, "free_symbols", None)
                        and getattr(s_expr_j, "free_symbols", None)
                        and len(s_expr_i.free_symbols) == len(s_expr_j.free_symbols)
                    ):
                        s_expr_i = _canon_syms(s_expr_i)
                        s_expr_j = _canon_syms(s_expr_j)
                        is_equiv = False
                        try:
                            import sympy
                            is_equiv = (sympy.simplify(s_expr_i - s_expr_j) == 0)
                            if not is_equiv and s_expr_j != 0:
                                ratio = sympy.simplify(s_expr_i / s_expr_j)
                                if getattr(ratio, "is_number", False) and not getattr(ratio, "free_symbols", set()):
                                    is_equiv = True
                        except Exception:
                            is_equiv = False

                        if is_equiv:
                            errors.append(
                                f"{cid}.json ({source_name}): [TPL-CLONE-SYMPY] Plantillas '{tids[i]}' y '{tids[j]}' "
                                f"en '{cid}' (arquetipo '{archs[i]}') reducen a fórmulas algebraicas equivalentes "
                                f"o reescaladas trivialmente en SymPy ({s_expr_i} vs {s_expr_j})."
                            )
                        elif _z3_check_sympy_equiv(s_expr_i, s_expr_j, timeout_ms=150) is True:
                            z3_warn_msg = (
                                f"{cid}.json ({source_name}): [Z3-RULE-WARNING] Plantillas '{tids[i]}' y '{tids[j]}' "
                                f"en '{cid}' (arquetipo '{archs[i]}') son algebraicamente equivalentes en Z3 bajo "
                                f"dominio positivo ({s_expr_i} vs {s_expr_j}), aunque SymPy no las redujo."
                            )
                            _logger.warning(z3_warn_msg)
                            if warnings_out is not None:
                                warnings_out.append(z3_warn_msg)

    return errors


