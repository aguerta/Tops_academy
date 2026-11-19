"""Fast static pre-check (AST only, <50 ms) for shard_NN_data.py (C2C v4.0).

Reports in ONE pass the known high-frequency compile failures, so the author can fix them
together instead of discovering them one compile at a time. Findings are WARNINGS ONLY
(never change the compile verdict).
"""
import ast
import re
from typing import List


def _names(node) -> set:
    return {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}


_MATRIX_RE = re.compile(r"\\begin\{(?:b|p|v)?matrix\}")
_DOT_DIGIT_RE = re.compile(r"\\dot\{\s*\d+\s*\}")


def is_bounded_while(node: ast.While) -> bool:
    """Return True if while loop has an explicit verifiable iteration bound."""
    incremented_vars = set()
    for child in ast.walk(node):
        if isinstance(child, ast.AugAssign) and isinstance(child.op, (ast.Add, ast.Sub)):
            if isinstance(child.target, ast.Name):
                incremented_vars.add(child.target.id)
        elif isinstance(child, ast.Assign):
            for t in child.targets:
                if isinstance(t, ast.Name):
                    for sub in ast.walk(child.value):
                        if isinstance(sub, ast.Name) and sub.id == t.id:
                            incremented_vars.add(t.id)

    if not incremented_vars:
        return False

    def _check_compare(comp: ast.Compare) -> bool:
        left = comp.left
        rights = comp.comparators
        if isinstance(left, ast.Name) and left.id in incremented_vars:
            if any(isinstance(r, (ast.Constant, ast.Name)) for r in rights):
                return True
        for r in rights:
            if isinstance(r, ast.Name) and r.id in incremented_vars:
                if isinstance(left, (ast.Constant, ast.Name)):
                    return True
        return False

    if isinstance(node.test, ast.Compare):
        if _check_compare(node.test):
            return True
    elif isinstance(node.test, ast.BoolOp):
        for val in node.test.values:
            if isinstance(val, ast.Compare) and _check_compare(val):
                return True

    for child in ast.walk(node):
        if isinstance(child, ast.If):
            has_break = any(isinstance(b, ast.Break) for b in ast.walk(child))
            if has_break:
                if isinstance(child.test, ast.Compare) and _check_compare(child.test):
                    return True
                elif isinstance(child.test, ast.BoolOp):
                    for val in child.test.values:
                        if isinstance(val, ast.Compare) and _check_compare(val):
                            return True

    return False


def precheck_source(source: str) -> List[str]:
    out: List[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return out  # the compiler reports syntax errors with exact lines

    func_defs = {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    gen_reachable = set()
    for fn_name, fn_node in func_defs.items():
        if fn_name.startswith("gen_") or fn_name.startswith("_gen"):
            queue = [fn_name]
            while queue:
                curr = queue.pop(0)
                if curr in gen_reachable:
                    continue
                gen_reachable.add(curr)
                callee_node = func_defs.get(curr)
                if callee_node:
                    for child in ast.walk(callee_node):
                        if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                            c_id = child.func.id
                            if c_id in func_defs and c_id not in gen_reachable:
                                queue.append(c_id)

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name in gen_reachable:
                for n in ast.walk(node):
                    if isinstance(n, ast.While) and not is_bounded_while(n):
                        out.append(f"L{n.lineno} [TPL-AD-HOC-PERTURBATION] [TPL-UNBOUNDED-LOOP] while en '{node.name}': deriva cada distractor con una formula cerrada (offsets algebraicos), sin bucles de reintento.")

            if node.name.startswith("gen_") or node.name.startswith("_gen"):
                joined_str_constants = {p for js in ast.walk(node) if isinstance(js, ast.JoinedStr) for p in js.values if isinstance(p, ast.Constant)}
                for n in ast.walk(node):
                    if isinstance(n, ast.JoinedStr):
                        if any(isinstance(p, ast.Constant) and isinstance(p.value, str) and _MATRIX_RE.search(p.value) for p in n.values):
                            out.append(f"L{n.lineno} [SYMPY-LATEX-MATRIX] f-string con matriz en '{node.name}': usa sympy.latex() en lugar de ensamblar matrices manualmente en Python.")
                    elif isinstance(n, ast.Constant) and isinstance(n.value, str) and n not in joined_str_constants and _MATRIX_RE.search(n.value):
                        if re.search(r"%[sdf]|@[a-zA-Z0-9_]+@|\{[a-zA-Z0-9_]+\}", n.value):
                            out.append(f"L{n.lineno} [SYMPY-LATEX-MATRIX] plantilla de matriz en '{node.name}': usa sympy.latex() en lugar de ensamblar matrices manualmente en Python.")
                    elif isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mod):
                        if isinstance(n.left, ast.Constant) and isinstance(n.left.value, str) and _MATRIX_RE.search(n.left.value):
                            out.append(f"L{n.lineno} [SYMPY-LATEX-MATRIX] interpolación de matriz con '%' en '{node.name}': usa sympy.latex() en lugar de ensamblar matrices manualmente en Python.")
                    elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "format":
                        if isinstance(n.func.value, ast.Constant) and isinstance(n.func.value.value, str) and _MATRIX_RE.search(n.func.value.value):
                            out.append(f"L{n.lineno} [SYMPY-LATEX-MATRIX] interpolación de matriz con .format() en '{node.name}': usa sympy.latex() en lugar de ensamblar matrices manualmente en Python.")
            if node.name.startswith("ver_"):
                for n in ast.walk(node):
                    if isinstance(n, ast.Raise):
                        out.append(f"L{n.lineno} [TPL-DEBUG-ARTIFACT] raise en '{node.name}': los verificadores deben retornar bool.")
                args = node.args
                n_req = len(args.args) - len(args.defaults)
                if len(args.args) == 2 and n_req == 1:
                    out.append(f"L{node.lineno} [VER-SIGNATURE] '{node.name}(res, v=None)': usa ver(c, v) (MC/FIB/open_symbolic) o ver(res) (MS/M20 estructurado), sin parametros opcionales.")
                if isinstance(node.body[-1], ast.Return) and isinstance(node.body[-1].value, ast.Constant) and node.body[-1].value.value is True and len(node.body) == 1:
                    out.append(f"L{node.lineno} [TPL-VERIFIER] '{node.name}' trivial (return True).")
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Name) and node.value.id.startswith("ver_"):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id.startswith("ver_"):
                    out.append(f"L{node.lineno} [NO-GLOBAL-ALIAS] '{t.id} = {node.value.id}': declara def {t.id}(res): return {node.value.id}(res).")
        # RATS-like dicts / tuples of rationale strings
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id.upper().startswith("RATS") for t in node.targets):
            for n in ast.walk(node.value):
                if isinstance(n, ast.Constant) and isinstance(n.value, str) and not re.fullmatch(r"D-[\w-]+", n.value):
                    if "@" not in n.value or len(n.value) < 20:
                        out.append(f"L{n.lineno} [TPL-DYNAMIC-RATIONALE] rationale '{n.value[:30]}': requiere @var@ y len >= 20.")
    # Module-level constant checks (KaTeX AST invariants & raw string control chars)
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            val = n.value
            if re.search(r"[\x07\x08\x0c\r\t\x0b]", val):
                out.append(f"L{n.lineno} [LATEX-RAW-STRING] control char en cadena (falta prefijo r\"...\" en LaTeX).")
            if _DOT_DIGIT_RE.search(val):
                out.append(f"L{n.lineno} [KATEX-AST-CHECK] \\dot{{}} aplicado a un dígito: la notación newtoniana \\dot solo es válida para variables/símbolos, no escalares.")
            for m in re.finditer(r"\\text\{", val):
                start = m.end()
                depth = 1
                i = start
                while i < len(val) and depth > 0:
                    if val[i] == "{" and (i == 0 or val[i-1] != "\\"):
                        depth += 1
                    elif val[i] == "}" and (i == 0 or val[i-1] != "\\"):
                        depth -= 1
                    i += 1
                if depth == 0:
                    inner = val[start : i - 1]
                    if len(inner) > 45:
                        out.append(f"L{n.lineno} [KATEX-AST-CHECK] \\text{{...}} con más de 45 caracteres ({len(inner)} chars): divide en prosa fuera de math o usa tokens breves.")
                        break
    return out
