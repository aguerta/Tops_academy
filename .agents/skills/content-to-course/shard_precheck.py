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


def precheck_source(source: str) -> List[str]:
    out: List[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return out  # the compiler reports syntax errors with exact lines
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if node.name.startswith("gen_") or node.name.startswith("_gen"):
                joined_str_constants = {p for js in ast.walk(node) if isinstance(js, ast.JoinedStr) for p in js.values if isinstance(p, ast.Constant)}
                for n in ast.walk(node):
                    if isinstance(n, ast.While):
                        out.append(f"L{n.lineno} [TPL-AD-HOC-PERTURBATION] while en '{node.name}': deriva cada distractor con una formula cerrada (offsets algebraicos), sin bucles de reintento.")
                    elif isinstance(n, ast.JoinedStr):
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
                    out.append(f"L{node.lineno} [VER-SIGNATURE] '{node.name}(res, v=None)': usa ver(c, v) (MC/FIB) o ver(res) (MS), sin parametros opcionales.")
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
