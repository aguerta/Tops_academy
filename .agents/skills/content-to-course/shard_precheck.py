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


def precheck_source(source: str) -> List[str]:
    out: List[str] = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return out  # the compiler reports syntax errors with exact lines
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            if node.name.startswith("gen_") or node.name.startswith("_gen"):
                for n in ast.walk(node):
                    if isinstance(n, ast.While):
                        out.append(f"L{n.lineno} [TPL-AD-HOC-PERTURBATION] while en '{node.name}': deriva cada distractor con una formula cerrada (offsets algebraicos), sin bucles de reintento.")
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
    # non-raw strings with LaTeX backslashes
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and re.search(r"[\x07\x08\x0c\r\t\x0b]", n.value):
            out.append(f"L{n.lineno} [LATEX-RAW-STRING] control char en cadena (falta prefijo r\"...\" en LaTeX).")
    return out
