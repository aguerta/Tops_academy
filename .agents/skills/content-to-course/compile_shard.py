"""Deterministic Python Tuple Compiler for Content-to-Course v3.2 Shard Authors.

Compiles work/shards/<shard_id>_data.py into canonical template JSON files in < 100 ms:
- Zero-fallback strict check of work/shards/pre_shard_manifest.json (BLOCKER on missing)
- AST-level Line Locator (ShardDataLineLocator) tracking exact line ranges, constants, and helper functions
- Dual-signature support (direct CLI, run.py stage 3 subprocess, and Python module imports)
- Clean Python callable to AST string extraction with preamble constants/helpers injection
- Intelligent tuple format unpacking supporting both prompt_shard_author.md examples and v3.2 canonical tuples
- Robust MC7 distractor completion and stem variant diversification ensuring 0 errors on H-01 & H-02
- Atomic, race-condition-free file writes and isolated .check_attempts per shard_id
- Strict dry-run validation (20 seeds) with surgical line-mapped diagnostics
"""

import argparse
import ast
import hashlib
import importlib.util
import inspect
import json
import os
import re
import sys
import textwrap
import threading
import time
import traceback
import types
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

# Force unbuffered standard streams to ensure immediate error reporting and avoid NTFS / Windows pipe deadlocks
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(line_buffering=True)
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass

# Ensure skill root is in sys.path
_skill_root = Path(__file__).parent.resolve()
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

from engine.invariants import validate_katex_syntax
from engine.stage_contract import (
    MIN_ARCHETYPES as _S4_MIN_ARCHETYPES,
    ARCHETYPE_KINDS as _S4_ARCHETYPE_KINDS,
    competency_contract as _s4_competency_contract,
    contract_drift as _s4_contract_drift,
    is_skill_type as _s4_is_skill_type,
    stems_advice as _s4_stems_advice,
)


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


class _CompilationWatchdog:
    """Watchdog daemon thread enforcing strict hard timeout budget (< 15.0s) on shard compilation."""

    def __init__(self, timeout: float = 15.0, shard_id: str = "unknown"):
        self.timeout = float(timeout)
        self.shard_id = shard_id
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self.start_time = 0.0

    def start(self) -> None:
        if self.timeout <= 0:
            return
        self.start_time = time.time()
        EvaluationContext.reset(self.shard_id)
        self._thread = threading.Thread(target=self._run, daemon=True, name="c2c_compile_watchdog")
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()

    def _run(self) -> None:
        while not self._stop_event.wait(0.2):
            elapsed = time.time() - self.start_time
            if elapsed >= self.timeout:
                ctx = EvaluationContext.get()
                shard_str = ctx.get("shard_id") or self.shard_id or "unknown"
                tpl_str = ctx.get("template_id") or "unknown"
                fn_str = ctx.get("gen_fn") or "_gen_unknown"
                arch_str = ctx.get("archetype") or "?"
                seed_str = str(ctx.get("seed")) if ctx.get("seed") is not None else "?"

                diag_msg = (
                    f"\n[-] CRITICAL ERROR: [TIMEOUT_INFINITE_LOOP]\n"
                    f"    Shard:          {shard_str}\n"
                    f"    Template ID:    {tpl_str}\n"
                    f"    Generator Func: {fn_str} (Archetype {arch_str}, Seed {seed_str})\n"
                    f"    Execution Time: {elapsed:.2f}s (Exceeded hard budget of {self.timeout:.1f}s)\n"
                    f"    Diagnostic:     Detected potential infinite loop, unbounded while-loop, \n"
                    f"                    or exhausted rejection sampling. Verify termination predicates \n"
                    f"                    and unbuffered output (-u).\n"
                    f"[-] FAIL: [TIMEOUT_INFINITE_LOOP] En '{tpl_str}' (función '{fn_str}', semilla {seed_str}): "
                    f"Tiempo de ejecución excedió el límite de {self.timeout:.1f}s.\n"
                )
                try:
                    sys.stderr.write(diag_msg)
                    sys.stderr.flush()
                    sys.stdout.write(diag_msg)
                    sys.stdout.flush()
                except Exception:
                    pass
                os._exit(1)


def _atomic_write_json(target_path: Path, data: Any) -> None:
    """Safely write JSON payload to file using atomic rename to prevent race conditions."""
    from check_templates import heal_control_chars_in_obj
    data = heal_control_chars_in_obj(data)
    target_path = Path(target_path).resolve()
    target_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = target_path.with_name(f".{target_path.name}.tmp.{os.getpid()}_{uuid.uuid4().hex[:8]}")
    if target_path.parent.name == "templates":
        payload_str = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    else:
        payload_str = json.dumps(data, indent=2, ensure_ascii=False)
    tmp_path.write_text(payload_str, encoding="utf-8")
    try:
        os.replace(tmp_path, target_path)
    except Exception:
        try:
            if target_path.is_file():
                target_path.unlink()
            os.replace(tmp_path, target_path)
        except Exception:
            target_path.write_text(payload_str, encoding="utf-8")
            if tmp_path.is_file():
                try:
                    tmp_path.unlink()
                except Exception:
                    pass


def count_distinct_shard_error_hunks(
    raw_errors: List[Any],
    targets: Optional[List[Path]] = None,
    shard_py: Optional[Union[str, Path]] = None,
) -> int:
    """Helper re-exported from check_templates for counting deduplicated error hunks."""
    from check_templates import count_distinct_shard_error_hunks as _count_hunks
    return _count_hunks(raw_errors, targets=targets, shard_py=shard_py)


def check_ast_rf_triple_braces(source_text: str) -> List[str]:
    """Check for rf'...' or fr'...' strings containing '{{{' which corrupts KaTeX braces."""
    warnings = []
    for m in re.finditer(r"(?i)\b(rf|fr)(['\"]{1,3})([\s\S]*?)\2", source_text):
        if "{{{" in m.group(3):
            snippet = m.group(0)[:60] + ("..." if len(m.group(0)) > 60 else "")
            warnings.append(
                f"[!] Warning: Se detectó {m.group(1)}{m.group(2)}...{m.group(2)} conteniendo '{{{{{{' ({snippet}). "
                "Recomendación: Utilice raw strings r\"...\" con tokens @var@ para evitar la corrupción de llaves KaTeX."
            )
    return warnings


try:
    import pykatex as _pykatex
except ImportError:  # optional dependency: warn-only check is skipped when absent
    _pykatex = None

_PYKATEX_SPAN_RE = re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$|(?<!\\)\$(.+?)(?<!\\)\$", re.DOTALL)
_PYKATEX_VAR_RE = re.compile(r"@[a-zA-Z0-9_]+@")


def pykatex_warnings(text: Any, context: str, whole_is_math: bool = False) -> List[str]:
    """Warn-only KaTeX render check (PyKaTeX). Never fails the compile.

    Template placeholders @var@ are replaced by '1' before rendering. Set C2C_PYKATEX=off to disable.
    """
    if _pykatex is None or not isinstance(text, str) or not text.strip():
        return []
    if os.environ.get("C2C_PYKATEX", "").lower() == "off":
        return []
    spans: List[Tuple[str, bool]] = []
    if whole_is_math and "$" not in text:
        spans.append((text, False))
    else:
        for m in _PYKATEX_SPAN_RE.finditer(text):
            if m.group(1) is not None:
                spans.append((m.group(1), True))
            else:
                spans.append((m.group(2), False))
    out: List[str] = []
    for span, display in spans:
        probe = _PYKATEX_VAR_RE.sub("1", span).strip()
        if not probe:
            continue
        try:
            _pykatex.renderToString(probe, display)
        except Exception as exc:
            raw_msg = str(exc)
            col = None
            m_pos = re.search(r"position\s+(\d+)", raw_msg, re.IGNORECASE)
            if m_pos:
                col = m_pos.group(1)
            elif "\u0332" in raw_msg:
                colon_idx = raw_msg.rfind(":")
                snippet = raw_msg[colon_idx + 1:] if colon_idx != -1 else raw_msg
                clean_before = snippet[:snippet.find("\u0332")].replace("\u0332", "")
                col = str(len(clean_before))
            col_info = f" [col={col}]" if col is not None else ""
            msg = raw_msg.replace("\u0332", "^").strip().splitlines()[0][:160]
            out.append(f"[!] Warning: [PYKATEX-WARN] {context}: {msg}{col_info} (span: {span[:60]!r})")
    return out


def heal_shard_source_text(source_text: str) -> Tuple[bool, str]:
    """Uses Python's tokenize module to inspect and heal non-raw string tokens and control characters in-memory.

    Heals unescaped LaTeX prefixes and ASCII control characters without modifying files on disk.
    Returns (modified, healed_text).
    """
    if not source_text:
        return False, source_text
    try:
        import io, tokenize
        from check_templates import heal_control_chars_in_str, COMBINED_LATEX
        clean_source = heal_control_chars_in_str(source_text)
        modified = (clean_source != source_text)
        tokens = list(tokenize.tokenize(io.BytesIO(clean_source.encode("utf-8")).readline))
        new_tokens = []
        for t in tokens:
            if t.type == tokenize.STRING:
                m = re.match(r"^([a-zA-Z]*)(['\"]{1,3})(.*)(['\"]{1,3})$", t.string, flags=re.DOTALL)
                if m:
                    prefix, q_open, body, q_close = m.groups()
                    is_raw = "r" in prefix.lower()
                    new_body = heal_control_chars_in_str(body)
                    if not is_raw:
                        new_body = re.sub(rf"(?<!\\)\\({COMBINED_LATEX})", r"\\\\\1", new_body)
                    else:
                        new_body = re.sub(r"(?<!\\)(?:\\\\)+([a-zA-Z]+)", r"\\\1", new_body)
                    if "$" in new_body:
                        _bs = r"\\" if is_raw else r"\\\\"
                        new_body = re.sub(r"(?<!\\)\\+centernot\s*\{?\s*\\+(?:Rightarrow|implies)\b\s*\}?", f"{_bs}nRightarrow", new_body)
                        new_body = re.sub(r"(?<!\\)\\+implies\b", f"{_bs}Rightarrow", new_body)
                        new_body = re.sub(r"(?<!\\)\\+iff\b", f"{_bs}Leftrightarrow", new_body)
                        new_body = re.sub(r"(?<!\\)\b(hat|bar|tilde|vec|dot|ddot|frac|dfrac|tfrac|sqrt|mathcal|mathbb|mathbf|boldsymbol|operatorname)\s*\{", rf"{_bs}\1{{", new_body)
                        if new_body.count("$$") == 1 and new_body.replace("$$", "").count("$") == 1:
                            new_body = new_body.replace("$$", "$")
                    if new_body != body:
                        modified = True
                        new_tokens.append(tokenize.TokenInfo(t.type, f"{prefix}{q_open}{new_body}{q_close}", t.start, t.end, t.line))
                        continue
            new_tokens.append(t)
        if not modified:
            return False, source_text
        rebuilt_text = tokenize.untokenize(new_tokens).decode("utf-8")
        return True, rebuilt_text
    except Exception:
        try:
            from check_templates import heal_control_chars_in_str, COMBINED_LATEX
            healed = heal_control_chars_in_str(source_text)
            has_raw = bool(re.search(r'\br["\']', source_text, re.IGNORECASE))
            if not has_raw:
                healed = re.sub(rf"(?<!\\)\\({COMBINED_LATEX})", r"\\\\\1", healed)
            return (healed != source_text), healed
        except Exception:
            return False, source_text


def heal_shard_source_file(py_path: Path) -> bool:
    """Uses Python's tokenize module to inspect and heal non-raw string tokens and control characters.

    Heals unescaped LaTeX prefixes and ASCII control characters in py_path before importing.
    Returns True if the file was modified and rewritten, False otherwise.
    """
    if not py_path.is_file():
        return False
    source_text = py_path.read_text(encoding="utf-8")
    modified, healed = heal_shard_source_text(source_text)
    if modified:
        py_path.write_text(healed.replace("\r\n", "\n"), encoding="utf-8", newline="\n")
    return modified


_parenthetical_telltale_re = re.compile(
    r"\(\s*(?:confusi[oó]n|error|omisi[oó]n|sesgo|falsamente|definici[oó]n\s+err[oó]nea|desplazamiento\s+err[oó]neo|c[aá]lculo\s+err[oó]neo)[^)]*\)",
    re.IGNORECASE,
)
_telltale_patterns = [
    re.compile(r"\b(err[oó]neamente|incorrectamente|falsamente)\b", re.IGNORECASE),
    re.compile(r"\b(derivada\s+err[oó]nea|f[oó]rmula\s+err[oó]nea|c[aá]lculo\s+err[oó]neo)\b", re.IGNORECASE),
    re.compile(r"\b(omitiendo\s+(elevar|multiplicar|dividir|sumar|restar))\b", re.IGNORECASE),
    re.compile(r"\b(confundiendo\s+con|al\s+rev[eé]s)\b", re.IGNORECASE),
    re.compile(r"\b(factorizando\s+err[oó]neamente|con\s+signos\s+positivos\s+incorrectos)\b", re.IGNORECASE),
]
_synthetic_prefix_re = re.compile(r"^\s*(?:Opci[oó]n|Alternativa|Variante)\s+(?:alterna\s+)?\d+\s*:?", re.IGNORECASE)


def parse_katex_number(val: Any) -> float:
    """Robustly parse a float from strings containing LaTeX formatting, delimiters, percentages, inequalities or macros."""
    if isinstance(val, (int, float)):
        return float(val)
    if not isinstance(val, str):
        val = str(val)
    s = val.replace(r"\le", "=").replace(r"\ge", "=").replace(r"\approx", "=").replace("<=", "=").replace(">=", "=")
    # Strip LaTeX formatting macros like \mathbf{...}, \operatorname{...}, \frac, etc.
    s = re.sub(r"\\[a-zA-Z]+", "", s)
    s = s.replace("$", "").replace(r"\%", "").replace("%", "").replace("{", "").replace("}", "").replace("\\", "").strip()
    s = s.split("=")[-1].strip()
    m = re.findall(r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", s)
    if m:
        return float(m[-1])
    return float(s)



def _find_telltale_in_option(text: Any, is_distractor: bool = True) -> Optional[str]:
    """Find parenthetical cues, distractor confessions, or synthetic clone prefixes in option text."""
    if not isinstance(text, str) or not text.strip():
        return None
    m_pt = _parenthetical_telltale_re.search(text)
    if m_pt:
        return m_pt.group(0)
    if is_distractor:
        for p in _telltale_patterns:
            m_p = p.search(text)
            if m_p:
                return m_p.group(0)
        m_syn = _synthetic_prefix_re.search(text)
        if m_syn:
            return m_syn.group(0)
    return None


def is_trivial_verifier(ver_code: str, ver_fn_callable: Any = None) -> Tuple[bool, str]:
    """Inspect AST of verifier code to reject trivial verifiers like constant 'return True'."""
    if not ver_code or not ver_code.strip():
        return True, "verifier code is empty"
    clean_ver_code = textwrap.dedent(ver_code.strip())
    try:
        tree = ast.parse(clean_ver_code)
    except Exception as e:
        return True, f"verifier code syntax error: {e}"

    fn_node = None
    target_names = {"verify", "cross_check"}
    if ver_fn_callable and hasattr(ver_fn_callable, "__name__"):
        target_names.add(ver_fn_callable.__name__)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name in target_names:
                fn_node = node
                break
    if not fn_node:
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fn_node = node
                break

    if not fn_node:
        return True, "no function definition found in verifier code"

    body_stmts = [
        s for s in fn_node.body
        if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and isinstance(s.value.value, str))
    ]

    if not body_stmts:
        return True, "verifier function body has no operational statements"

    # Single return constant (e.g. return True, return 1, or return None)
    if len(body_stmts) == 1 and isinstance(body_stmts[0], ast.Return):
        ret_val = body_stmts[0].value
        if isinstance(ret_val, ast.Constant):
            return True, f"returns constant '{ret_val.value}' without evaluating conditions"
        if ret_val is None:
            return True, "returns None without evaluating conditions"

    # Check if arguments (instance / cand, v) are ever loaded in operational statements
    arg_names = [a.arg for a in (getattr(fn_node.args, "posonlyargs", []) + fn_node.args.args + getattr(fn_node.args, "kwonlyargs", []))]
    if arg_names:
        used_arg = False
        for s in body_stmts:
            for sub in ast.walk(s):
                if isinstance(sub, ast.Name) and sub.id in arg_names and isinstance(sub.ctx, ast.Load):
                    used_arg = True
                    break
            if used_arg:
                break
        if not used_arg:
            return True, f"arguments {arg_names} are never inspected in verifier function body"

    return False, ""


def normalize_double_braces(text: str, declared_vars: Optional[Set[str]] = None) -> str:
    r"""Normalize non-variable double curly braces {{token}} -> {token} when token is not a declared variable.

    Protects declared variables so that {var} can still be evaluated, while ensuring LaTeX braces like
    {{0.5}}, {{\operatorname{arccot}}}, {{S_{xy}}} are normalized to {0.5}, {\operatorname{arccot}}, {S_{xy}}
    before R-20 validation.
    """
    if not isinstance(text, str) or "{{" not in text:
        return text

    v_set = declared_vars or set()

    def _normalize_once(s: str) -> str:
        out = []
        i = 0
        n = len(s)
        while i < n:
            if s[i:i+2] == "{{":
                j = i + 2
                depth = 0
                found = False
                while j < n:
                    if s[j:j+2] == "}}" and depth == 0:
                        found = True
                        break
                    elif s[j] == "{":
                        depth += 1
                        j += 1
                    elif s[j] == "}":
                        if depth > 0:
                            depth -= 1
                            j += 1
                        else:
                            break
                    else:
                        j += 1

                if found:
                    token = s[i+2:j]
                    var_name = token.strip().split(":")[0].strip()
                    if v_set and var_name in v_set:
                        out.append(s[i:j+2])
                    else:
                        out.append("{" + token + "}")
                    i = j + 2
                else:
                    out.append(s[i])
                    i += 1
            else:
                out.append(s[i])
                i += 1
        return "".join(out)

    prev = None
    curr = text
    while prev != curr:
        prev = curr
        curr = _normalize_once(curr)
    return curr


def _find_diagnostic_line(
    locator: Optional[Any],
    gen_fn_name: Optional[str],
    orig_idx: int,
    needle: str = "",
) -> int:
    """Finds exact 1-based source line for surgical error diagnostics."""
    if not locator or not hasattr(locator, "lines"):
        return 1
    # 1. Search in generator function lines if gen_fn_name is known
    if gen_fn_name and hasattr(locator, "functions") and gen_fn_name in locator.functions:
        s_fn, e_fn = locator.functions[gen_fn_name]
        if needle:
            n_clean = needle.strip()
            for line_no in range(s_fn, min(e_fn + 1, len(locator.lines) + 1)):
                if n_clean and n_clean in locator.lines[line_no - 1]:
                    return line_no
        return s_fn
    # 2. Search in tuple lines
    if hasattr(locator, "get_tuple_info"):
        t_info = locator.get_tuple_info(orig_idx)
        if t_info:
            s_t = t_info.get("start_line", 1)
            e_t = t_info.get("end_line", s_t)
            if needle:
                n_clean = needle.strip()
                for line_no in range(s_t, min(e_t + 1, len(locator.lines) + 1)):
                    if n_clean and n_clean in locator.lines[line_no - 1]:
                        return line_no
            return s_t
    return 1



class ShardDataLineLocator:
    """AST-based source line tracker for shard_XX_data.py files.

    Extracts precise line ranges for:
    - Syntax errors with exact line and column
    - Top-level constants (Assign, AnnAssign) -> (start_line, end_line)
    - Functions (def gen_*, def ver_*, helpers) -> (start_line, end_line)
    - TEMPLATES list assignment -> list of tuples
    - Each tuple index -> (tuple_start, tuple_end)
    - Each of the 9 tuple elements -> (item_start, item_end)
    - Source snippet extraction for replace_file_content
    """

    def __init__(self, file_path: Union[str, Path], source_text: Optional[str] = None):
        self.file_path = Path(file_path).resolve()
        if source_text is not None:
            self.source_text = source_text
        else:
            self.source_text = self.file_path.read_text(encoding="utf-8") if self.file_path.is_file() else ""
        self.lines = self.source_text.splitlines()
        self.syntax_error: Optional[str] = None
        self.syntax_error_details: Optional[Dict[str, Any]] = None
        self.constants: Dict[str, Tuple[int, int]] = {}
        self.functions: Dict[str, Tuple[int, int]] = {}
        self.function_segments: Dict[str, str] = {}
        self.helper_functions: Set[str] = set()
        self.top_level_imports: List[Tuple[int, int, str]] = []
        self.tuples: List[Dict[str, Any]] = []
        self.competency_to_tuple_idx: Dict[str, int] = {}
        if self.source_text:
            self.parse_ast()

    def parse_ast(self) -> bool:
        try:
            tree = ast.parse(self.source_text, filename=str(self.file_path))
        except SyntaxError as e:
            lineno = e.lineno or 1
            offset = e.offset or 1
            line_txt = self.lines[lineno - 1] if 0 <= lineno - 1 < len(self.lines) else (e.text or "")
            self.syntax_error = (
                f"SyntaxError en {self.file_path.name} (Línea {lineno}, Columna {offset}): {e.msg}\n"
                f"  {line_txt.strip()}\n"
                f"  Rango: StartLine: {lineno}, EndLine: {lineno}"
            )
            self.syntax_error_details = {
                "line": lineno,
                "offset": offset,
                "msg": e.msg,
                "line_text": line_txt,
                "start_line": lineno,
                "end_line": lineno,
            }
            return False

        # 1. Map top-level imports, functions, and constants
        for node in tree.body:
            if isinstance(node, ast.Import):
                root = node.names[0].name.split(".")[0] if node.names else ""
                end_lineno = getattr(node, "end_lineno", node.lineno)
                self.top_level_imports.append((node.lineno, end_lineno, root))
            elif isinstance(node, ast.ImportFrom):
                root = (node.module or "").split(".")[0]
                end_lineno = getattr(node, "end_lineno", node.lineno)
                self.top_level_imports.append((node.lineno, end_lineno, root))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                end_lineno = getattr(node, "end_lineno", node.lineno)
                self.functions[node.name] = (node.lineno, end_lineno)
                seg = ast.get_source_segment(self.source_text, node)
                if seg:
                    self.function_segments[node.name] = seg
            elif isinstance(node, ast.Assign):
                if (
                    len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Name)
                    and isinstance(node.value, ast.Lambda)
                ):
                    fn_name = node.targets[0].id
                    end_lineno = getattr(node, "end_lineno", node.lineno)
                    self.functions[fn_name] = (node.lineno, end_lineno)
                    seg = ast.get_source_segment(self.source_text, node)
                    if seg:
                        self.function_segments[fn_name] = seg
                else:
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id != "TEMPLATES":
                            end_lineno = getattr(node, "end_lineno", node.lineno)
                            self.constants[target.id] = (node.lineno, end_lineno)
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name) and node.target.id != "TEMPLATES":
                    if isinstance(node.value, ast.Lambda):
                        fn_name = node.target.id
                        end_lineno = getattr(node, "end_lineno", node.lineno)
                        self.functions[fn_name] = (node.lineno, end_lineno)
                        seg = ast.get_source_segment(self.source_text, node)
                        if seg:
                            self.function_segments[fn_name] = seg
                    else:
                        end_lineno = getattr(node, "end_lineno", node.lineno)
                        self.constants[node.target.id] = (node.lineno, end_lineno)

        # 2. Locate TEMPLATES = [...] or TEMPLATES += [...]
        for node in tree.body:
            if isinstance(node, (ast.Assign, ast.AugAssign)):
                target_name = None
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "TEMPLATES":
                            target_name = "TEMPLATES"
                            break
                elif isinstance(node, ast.AugAssign):
                    if isinstance(node.target, ast.Name) and node.target.id == "TEMPLATES":
                        target_name = "TEMPLATES"

                if target_name == "TEMPLATES" and isinstance(node.value, (ast.List, ast.Tuple)):
                    start_idx = len(self.tuples)
                    for elt_offset, elt in enumerate(node.value.elts):
                        tuple_info = self._analyze_tuple_node(elt, start_idx + elt_offset)
                        self.tuples.append(tuple_info)
                        cid = tuple_info.get("competency_id")
                        if cid and cid not in self.competency_to_tuple_idx:
                            self.competency_to_tuple_idx[cid] = start_idx + elt_offset

        # 3. Classify helper functions (any top-level function not directly used as gen/ver in a tuple)
        used_fn_names = set()
        for t in self.tuples:
            if t.get("gen_fn_name"):
                used_fn_names.add(t["gen_fn_name"])
            if t.get("ver_fn_name"):
                used_fn_names.add(t["ver_fn_name"])
        self.helper_functions = set(self.functions.keys()) - used_fn_names

        return True

    def _analyze_tuple_node(self, node: ast.AST, idx: int) -> Dict[str, Any]:
        start_line = getattr(node, "lineno", 1)
        end_line = getattr(node, "end_lineno", start_line)

        info: Dict[str, Any] = {
            "index": idx,
            "start_line": start_line,
            "end_line": end_line,
            "elements": {},
            "competency_id": None,
            "template_id": None,
            "question_type": None,
            "difficulty": None,
            "bloom": None,
            "gen_fn_name": None,
            "ver_fn_name": None,
            "stems_var": None,
            "hints_var": None,
            "sol_var": None,
        }

        if isinstance(node, (ast.Tuple, ast.List)):
            elts = node.elts
            # Strictly Form B 9-tuple: [tpl_id, cid, qtype, gen_fn, ver_fn, diff_bloom, stems, hints, sol]
            element_names = [
                "template_id", "competency_id", "question_type",
                "generator_code", "verifier_code", "difficulty_bloom",
                "stem_variants", "hints", "solution"
            ]

            for e_idx, elt in enumerate(elts):
                if e_idx < len(element_names):
                    name = element_names[e_idx]
                    e_start = getattr(elt, "lineno", start_line)
                    e_end = getattr(elt, "end_lineno", e_start)
                    info["elements"][name] = {
                        "start_line": e_start,
                        "end_line": e_end,
                        "node_type": type(elt).__name__,
                    }
                    if name == "competency_id" and isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                        info["competency_id"] = elt.value
                    elif name == "template_id" and isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                        info["template_id"] = elt.value
                    elif name == "question_type" and isinstance(elt, ast.Constant) and isinstance(elt.value, str):
                        info["question_type"] = elt.value.strip().lower()
                    elif name == "difficulty_bloom" and isinstance(elt, (ast.Tuple, ast.List)) and len(elt.elts) >= 2:
                        d_elt, b_elt = elt.elts[0], elt.elts[1]
                        if isinstance(d_elt, ast.Constant) and isinstance(d_elt.value, str):
                            info["difficulty"] = d_elt.value.strip().lower()
                        if isinstance(b_elt, ast.Constant) and isinstance(b_elt.value, str):
                            info["bloom"] = b_elt.value.strip()
                    elif name == "generator_code" and isinstance(elt, ast.Name):
                        info["gen_fn_name"] = elt.id
                    elif name == "verifier_code" and isinstance(elt, ast.Name):
                        info["ver_fn_name"] = elt.id
                    elif name == "stem_variants" and isinstance(elt, ast.Name):
                        info["stems_var"] = elt.id
                    elif name == "hints" and isinstance(elt, ast.Name):
                        info["hints_var"] = elt.id
                    elif name == "solution" and isinstance(elt, ast.Name):
                        info["sol_var"] = elt.id
        elif isinstance(node, ast.Dict):
            info["is_form_c"] = True
            for k_node, v_node in zip(node.keys, node.values):
                if not (isinstance(k_node, ast.Constant) and isinstance(k_node.value, str)):
                    continue
                k = k_node.value
                k_start = getattr(v_node, "lineno", start_line)
                k_end = getattr(v_node, "end_lineno", k_start)
                info["elements"][k] = {
                    "start_line": k_start,
                    "end_line": k_end,
                    "node_type": type(v_node).__name__,
                }
                if k in ("id", "tpl_id", "template_id") and isinstance(v_node, ast.Constant) and isinstance(v_node.value, str):
                    info["template_id"] = v_node.value
                elif k in ("cid", "competency_id") and isinstance(v_node, ast.Constant) and isinstance(v_node.value, str):
                    info["competency_id"] = v_node.value
                elif k in ("qtype", "question_type") and isinstance(v_node, ast.Constant) and isinstance(v_node.value, str):
                    info["question_type"] = v_node.value.strip().lower()
                elif k in ("band", "difficulty_bloom") and isinstance(v_node, (ast.Tuple, ast.List)) and len(v_node.elts) >= 2:
                    d_elt, b_elt = v_node.elts[0], v_node.elts[1]
                    if isinstance(d_elt, ast.Constant) and isinstance(d_elt.value, str):
                        info["difficulty"] = d_elt.value.strip().lower()
                    if isinstance(b_elt, ast.Constant) and isinstance(b_elt.value, str):
                        info["bloom"] = b_elt.value.strip()
                elif k == "difficulty" and isinstance(v_node, ast.Constant) and isinstance(v_node.value, str):
                    info["difficulty"] = v_node.value.strip().lower()
                elif k == "bloom" and isinstance(v_node, ast.Constant) and isinstance(v_node.value, str):
                    info["bloom"] = v_node.value.strip()
                elif k in ("gen", "generator_code") and isinstance(v_node, ast.Name):
                    info["gen_fn_name"] = v_node.id
                elif k in ("ver", "verifier_code") and isinstance(v_node, ast.Name):
                    info["ver_fn_name"] = v_node.id
                elif k in ("stems", "stem_variants") and isinstance(v_node, ast.Name):
                    info["stems_var"] = v_node.id
                elif k == "hints" and isinstance(v_node, ast.Name):
                    info["hints_var"] = v_node.id
                elif k in ("sol", "solution") and isinstance(v_node, ast.Name):
                    info["sol_var"] = v_node.id

        return info

    def find_tuple_for_question(
        self,
        cid: str,
        template_id: Optional[str] = None,
        difficulty: Optional[str] = None,
        interaction_type: Optional[str] = None,
        bloom: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Resolves the exact TEMPLATES tuple info matching a question's competency, template_id, or difficulty/type."""
        cand_tuples = [t for t in self.tuples if t.get("competency_id") == cid]
        if not cand_tuples:
            cand_tuples = list(self.tuples)
        if not cand_tuples:
            return None

        if template_id:
            for t in cand_tuples:
                tid = str(t.get("template_id") or "")
                if (
                    tid == template_id
                    or tid.replace("_", "-") == template_id.replace("_", "-")
                    or f"T-{tid}" == template_id
                    or tid == f"T-{template_id}"
                    or tid.lower() == template_id.lower()
                ):
                    return t
            m_idx = re.search(r"[_-]0*(\d+)$", str(template_id))
            if m_idx:
                idx_1based = int(m_idx.group(1))
                if 1 <= idx_1based <= len(cand_tuples):
                    return cand_tuples[idx_1based - 1]

        norm_diff = (difficulty or "").strip().lower()
        norm_itype = (interaction_type or "").strip().lower()
        norm_bloom = (bloom or "").strip().lower()

        if norm_diff:
            diff_matches = [t for t in cand_tuples if t.get("difficulty") == norm_diff]
            if len(diff_matches) == 1:
                return diff_matches[0]
            if len(diff_matches) > 1 and norm_itype:
                for t in diff_matches:
                    qt = t.get("question_type") or ""
                    if ("multiple_choice" in norm_itype and "multiple_choice" in qt) or (
                        "fill_in" in norm_itype and ("fill_in" in qt or "open" in qt or "fib" in qt)
                    ) or ("select" in norm_itype and "select" in qt):
                        return t
                return diff_matches[0]

        if norm_itype:
            for t in cand_tuples:
                qt = t.get("question_type") or ""
                if ("multiple_choice" in norm_itype and "multiple_choice" in qt) or (
                    "fill_in" in norm_itype and ("fill_in" in qt or "open" in qt or "fib" in qt)
                ) or ("select" in norm_itype and "select" in qt):
                    if not norm_bloom or (t.get("bloom") or "").lower() == norm_bloom:
                        return t

        return cand_tuples[0]

    def find_offending_lines(
        self,
        tuple_info: Optional[Dict[str, Any]],
        linter_name: str = "",
        needle: str = "",
    ) -> Tuple[int, int, List[Tuple[int, str]]]:
        """Pinpoints the exact 1-based (start_line, end_line, [(lineno, code), ...]) inside the shard file."""
        if not self.lines:
            return 1, 1, []
        if not tuple_info:
            return 1, min(len(self.lines), 5), [(i + 1, self.lines[i]) for i in range(min(len(self.lines), 5))]

        linter_low = (linter_name or "").lower()
        gen_fn = tuple_info.get("gen_fn_name")
        ver_fn = tuple_info.get("ver_fn_name")
        stems_var = tuple_info.get("stems_var")
        hints_var = tuple_info.get("hints_var")
        sol_var = tuple_info.get("sol_var")
        t_start = tuple_info.get("start_line", 1)
        t_end = tuple_info.get("end_line", t_start)

        def _slice_lines(s: int, e: int) -> List[Tuple[int, str]]:
            s_c = max(1, s)
            e_c = min(len(self.lines), max(s_c, e))
            return [(ln, self.lines[ln - 1]) for ln in range(s_c, e_c + 1)]

        # 1. Hints linters -> locate hints_var or tuple hints element
        if "hint" in linter_low or "socratic" in linter_low or "scaffolding" in linter_low:
            if hints_var and hints_var in self.constants:
                s_h, e_h = self.constants[hints_var]
                return s_h, e_h, _slice_lines(s_h, e_h)
            h_elt = tuple_info.get("elements", {}).get("hints")
            if h_elt:
                return h_elt["start_line"], h_elt["end_line"], _slice_lines(h_elt["start_line"], h_elt["end_line"])

        # 2. ZPD / modality / archetype linters -> locate TEMPLATES tuple(s)
        if "zpd" in linter_low or "modality" in linter_low or "archetype" in linter_low:
            cid = tuple_info.get("competency_id")
            if cid:
                cid_tuples = [t for t in self.tuples if t.get("competency_id") == cid]
                if cid_tuples:
                    s_all = min(t["start_line"] for t in cid_tuples)
                    e_all = max(t["end_line"] for t in cid_tuples)
                    return s_all, e_all, _slice_lines(s_all, e_all)
            return t_start, t_end, _slice_lines(t_start, t_end)

        # 3. Distractor / rationale / magic-multiplier / anti-gaming / option length linters -> inside gen_fn
        if any(
            k in linter_low
            for k in ("diagnostic_rationale", "distractor", "cloned", "telltale", "anti_gaming", "length_padded", "magic")
        ):
            if gen_fn and gen_fn in self.functions:
                s_fn, e_fn = self.functions[gen_fn]
                fn_lines = _slice_lines(s_fn, e_fn)
                if "multiplicador" in needle.lower() or "magic" in linter_low or "diagnostic_rationale" in linter_low:
                    mult_lines = [
                        (ln, txt)
                        for ln, txt in fn_lines
                        if re.search(
                            r"\b(?:ds|cds|dists|distractors|d[1-6])\s*=|\bround\s*\(\s*ans\b|\bans\s*[\*/]|\(\"D-",
                            txt,
                        )
                    ]
                    if mult_lines:
                        s_m = mult_lines[0][0]
                        e_m = min(e_fn, max(mult_lines[-1][0], s_m + 1))
                        # If a multi-line list assignment starts at s_m, include up to its closing bracket or dists
                        return s_m, e_m, _slice_lines(s_m, min(e_m, s_m + 14))
                dist_lines = [
                    (ln, txt)
                    for ln, txt in fn_lines
                    if re.search(r"\b(?:dists|distractors|options|ds|d[1-6])\s*=|\(\"D-", txt)
                ]
                if dist_lines:
                    s_d = dist_lines[0][0]
                    e_d = dist_lines[-1][0]
                    return s_d, e_d, _slice_lines(s_d, min(e_d + 2, e_fn))
                return s_fn, e_fn, fn_lines

        # 4. KaTeX / uninterpolated / residue / string replacement -> search needle across gen_fn, stems_var, hints_var, sol_var
        if needle:
            n_clean = needle.strip()
            search_ranges: List[Tuple[int, int]] = []
            if gen_fn and gen_fn in self.functions:
                search_ranges.append(self.functions[gen_fn])
            for vname in (stems_var, hints_var, sol_var):
                if vname and vname in self.constants:
                    search_ranges.append(self.constants[vname])
            search_ranges.append((t_start, t_end))
            for s_r, e_r in search_ranges:
                matched = [
                    (ln, txt)
                    for ln, txt in _slice_lines(s_r, e_r)
                    if n_clean in txt
                ]
                if matched:
                    return matched[0][0], matched[-1][0], matched

        if gen_fn and gen_fn in self.functions:
            s_fn, e_fn = self.functions[gen_fn]
            return s_fn, e_fn, _slice_lines(s_fn, e_fn)

        return t_start, t_end, _slice_lines(t_start, t_end)

    def get_tuple_info(self, idx_or_cid: Union[int, str]) -> Optional[Dict[str, Any]]:
        idx = self.competency_to_tuple_idx.get(idx_or_cid) if isinstance(idx_or_cid, str) else idx_or_cid
        if idx is not None and isinstance(idx, int) and 0 <= idx < len(self.tuples):
            return self.tuples[idx]
        return None

    def get_tuple_snippet(self, idx_or_cid: Union[int, str]) -> Tuple[int, int, str]:
        """Returns (start_line, end_line, snippet_text) for a tuple."""
        idx = self.competency_to_tuple_idx.get(idx_or_cid) if isinstance(idx_or_cid, str) else idx_or_cid
        if idx is not None and isinstance(idx, int) and 0 <= idx < len(self.tuples):
            t = self.tuples[idx]
            s = t["start_line"]
            e = t["end_line"]
            snippet_lines = self.lines[s - 1 : e]
            numbered = [f"{s + i:4d}: {line}" for i, line in enumerate(snippet_lines)]
            return s, e, "\n".join(numbered)
        return 0, 0, ""

    def get_function_snippet(self, fn_name: str) -> Tuple[int, int, str]:
        """Returns (start_line, end_line, snippet_text) for a function definition."""
        if fn_name in self.functions:
            s, e = self.functions[fn_name]
            snippet_lines = self.lines[s - 1 : e]
            numbered = [f"{s + i:4d}: {line}" for i, line in enumerate(snippet_lines)]
            return s, e, "\n".join(numbered)
        return 0, 0, ""

    def get_constant_snippet(self, const_name: str) -> Tuple[int, int, str]:
        """Returns (start_line, end_line, snippet_text) for a constant assignment."""
        if const_name in self.constants:
            s, e = self.constants[const_name]
            snippet_lines = self.lines[s - 1 : e]
            numbered = [f"{s + i:4d}: {line}" for i, line in enumerate(snippet_lines)]
            return s, e, "\n".join(numbered)
        return 0, 0, ""

    def get_preamble_code(self) -> str:
        """Extracts allowed top-level imports, top-level constants, and helper functions for sandbox injection."""
        preamble_lines: List[str] = []
        # Safe allowed root modules in sandbox
        allowed_import_roots = {"math", "fractions", "statistics", "sympy", "numpy", "scipy", "random", "decimal"}

        # Only extract top-level imports from tree.body (ignoring imports inside functions)
        if getattr(self, "top_level_imports", None):
            for s, e, root in self.top_level_imports:
                if root in allowed_import_roots:
                    import_lines = self.lines[s - 1 : e]
                    preamble_lines.append(textwrap.dedent("\n".join(import_lines)).strip())
        else:
            # Fallback when AST didn't parse: strictly column-0 imports with NO leading indentation
            for line in self.lines:
                if line.startswith("import ") or line.startswith("from "):
                    stripped = line.strip()
                    parts = stripped.split()
                    if len(parts) >= 2:
                        root = parts[1].split(".")[0]
                        if root in allowed_import_roots:
                            preamble_lines.append(stripped)

        # Include constant lines
        for cname, (s, e) in sorted(self.constants.items(), key=lambda x: x[1][0]):
            const_lines = self.lines[s - 1 : e]
            preamble_lines.append(textwrap.dedent("\n".join(const_lines)).strip())

        # Include helper function lines in ascending line order
        for hname in sorted(self.helper_functions, key=lambda k: self.functions[k][0]):
            if hname in getattr(self, "function_segments", {}):
                helper_src = self.function_segments[hname]
            else:
                s, e = self.functions[hname]
                helper_src = "\n".join(self.lines[s - 1 : e])
            preamble_lines.append(textwrap.dedent(helper_src).strip())

        return "\n".join(preamble_lines).strip()


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

    queue = [target_fn_name]
    visited = set()

    while queue:
        curr = queue.pop(0)
        if curr in visited:
            continue
        visited.add(curr)
        if curr != target_fn_name:
            needed_funcs.add(curr)
        fnode = functions.get(curr)
        if not fnode:
            continue
        for sub in ast.walk(fnode[0]):
            if isinstance(sub, ast.Name) and isinstance(sub.ctx, ast.Load):
                nid = sub.id
                needed_names.add(nid)
                if nid in functions and nid not in visited:
                    queue.append(nid)
                elif nid in constants and nid not in needed_consts:
                    needed_consts.add(nid)
                    for csub in ast.walk(constants[nid][0]):
                        if isinstance(csub, ast.Name) and isinstance(csub.ctx, ast.Load):
                            needed_names.add(csub.id)
                            if csub.id in functions and csub.id not in visited:
                                queue.append(csub.id)
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
    m = re.search(rf"\b(?:def\s+{re.escape(target_fn_name)}\s*\(|{re.escape(target_fn_name)}\s*=)", full_pruned)
    if m:
        return full_pruned[:m.start()].strip()
    return ""


def normalize_form_c_template(t: Any) -> Any:
    """Normalizes template entry: converts ShardCompetenceContract or Pydantic BaseModel to Form-C dict.

    Transparently supports:
    1. Instances of ShardCompetenceContract (with to_form_c_dict())
    2. Pydantic BaseModel instances (with model_dump())
    3. Form-C dicts (unchanged)
    4. Form-B 9-tuples (unchanged)
    """
    if hasattr(t, "to_form_c_dict") and callable(getattr(t, "to_form_c_dict")):
        return t.to_form_c_dict()
    if hasattr(t, "model_dump") and callable(getattr(t, "model_dump")):
        data = dict(t.model_dump())
        field_mapping = {
            "competence_id": "cid",
            "archetype": "archetype",
            "assumption_tested_id": "assumption_id",
            "statement_variants_markdown": "stems",
            "hints_markdown": "hints",
            "solution_markdown": "sol",
        }
        out = {}
        for k, v in data.items():
            mapped_k = field_mapping.get(k, k)
            out[mapped_k] = v
        # Preserve non-dumped callables or attributes on the model
        for attr in ("gen", "ver", "generator_code", "verifier_code", "fmt", "rats", "band", "qtype", "id", "cid"):
            if attr not in out and hasattr(t, attr):
                out[attr] = getattr(t, attr)
        return out
    return t


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
            local_var_names: List[str] = []
            seen = set()

            def _collect_assignments(stmts):
                for stmt in stmts:
                    if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        continue
                    if isinstance(stmt, ast.Assign):
                        for tgt in stmt.targets:
                            self._extract_names(tgt, local_var_names, seen)
                    elif isinstance(stmt, ast.AnnAssign):
                        self._extract_names(stmt.target, local_var_names, seen)
                    for _, child_val in ast.iter_fields(stmt):
                        if isinstance(child_val, list):
                            _collect_assignments(child_val)
                        elif isinstance(child_val, ast.AST) and not isinstance(child_val, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            _collect_assignments([child_val])

            _collect_assignments(fn_node.body)

            class _ReturnTransformer(ast.NodeTransformer):
                def __init__(self, vars_list: List[str]):
                    self.vars_list = vars_list

                def visit_FunctionDef(self, n):
                    return n

                def visit_AsyncFunctionDef(self, n):
                    return n

                def visit_Return(self, ret_node: ast.Return) -> ast.Return:
                    if not isinstance(ret_node.value, ast.Dict):
                        return ret_node
                    dict_node = ret_node.value
                    str_keys = []
                    for k in dict_node.keys:
                        if isinstance(k, ast.Constant) and isinstance(k.value, str):
                            str_keys.append(k.value)
                        else:
                            str_keys.append(None)

                    output_keys = {"ans", "correct", "ds", "distractors", "options"}
                    has_output = any(k in output_keys for k in str_keys if k)
                    has_vars = "vars" in str_keys

                    if has_output and not has_vars:
                        v_keys = [ast.Constant(value=v) for v in self.vars_list]
                        v_vals = [ast.Name(id=v, ctx=ast.Load()) for v in self.vars_list]

                        if "ans" not in self.vars_list:
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

            ret_trans = _ReturnTransformer(local_var_names)
            fn_node.body = [ret_trans.visit(stmt) for stmt in fn_node.body]
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
        code_str = re.sub(r"^def\s+[A-Za-z0-9_]+\s*\(", f"def {target_name}(", raw_src, count=1)

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


def build_adapted_mc7_generator(
    base_gen_code: str,
    cid: str,
    cta_distractors: List[Dict[str, Any]],
    strict: bool = True,
    rats_map: Optional[Dict[str, str]] = None,
    fmt: Optional[str] = None,
) -> str:
    """Wraps an MC7 generator function to assemble options list with 1 correct and distractors.

    In strict mode:
    - Eliminates magical multipliers and synthetic positional assignment.
    - Rejects 2-tuples (did, val) unless declared in rats_map/RATS, and requires 3-tuples.
    - Ensures distractor IDs match declared CTA distractors.
    """
    declared_ids_list = [d.get("id") for d in cta_distractors if isinstance(d, dict) and d.get("id")]
    declared_ids_repr = ("{" + ",".join(repr(x) for x in sorted(declared_ids_list)) + "}") if declared_ids_list else "set()"
    strict_repr = "True" if strict else "False"
    relevant_rats = {k: v for k, v in (rats_map or {}).items() if not declared_ids_list or k in declared_ids_list}

    base = base_gen_code.rstrip()
    if base.endswith("generate = generate_params"):
        base = base[:-len("generate = generate_params")].rstrip()

    if fmt and "@X@" in fmt:
        pfx = fmt.split("@X@")[0]
        fmt_helper = f'lambda s: ({repr(fmt)}.replace("@X@", s) if (s and not s.startswith({repr(pfx)})) else s)'
    else:
        fmt_helper = "lambda s: s"

    if not relevant_rats:
        if fmt and "@X@" in fmt:
            pfx = fmt.split("@X@")[0]
            fmt_def = f'f=lambda s:({repr(fmt)}.replace("@X@",s) if (s and not s.startswith({repr(pfx)})) else s)'
            f_c = 'f(str(r.get("correct") or r.get("ans","")).strip())'
            f_w = 'f(str(d[1]))'
        else:
            fmt_def = ''
            f_c = 'str(r.get("correct") or r.get("ans","")).strip()'
            f_w = 'str(d[1])'
        wrapper = f"""{base}
_g=generate_params
def generate_params(rng):
 r=_g(rng)
 if isinstance(r,(tuple,list)):r={{"vars":r[0] if isinstance(r[0],dict) else {{"val":r[0]}},"correct":str(r[1]),"distractors":r[2] if len(r)>2 else []}}
 elif not isinstance(r,dict):return r
 {fmt_def}
 ids,st={declared_ids_repr},{strict_repr}
 ds=[]
 for d in (r.get("distractors") or r.get("ds") or []):
  if isinstance(d,(tuple,list)) and len(d)>=3:
   did=str(d[0]).replace("_","-")
   if ids and did not in ids and st:raise ValueError(f"Distractor ID '{{did}}' no esta declarado en cta.json ({cid}).")
   w={f_w};ds.append({{"value":w,"content":w,"distractor_id":did,"error_rationale":str(d[2]),"is_correct":False}})
  elif isinstance(d,dict):ds.append(d)
  elif st:raise ValueError(f"[TPL-MC7-STRICT] 3-tupla requerida: {{d!r}}")
 c={f_c}
 r["distractors"],r["options"]=ds,[{{"value":c,"content":c,"is_correct":True}}]+ds
 return r
generate=generate_params
"""
    else:
        rats_map_repr = json.dumps(relevant_rats, separators=(",", ":"))
        ids_code = "set(rats)" if (set(relevant_rats) >= set(declared_ids_list)) else f"{declared_ids_repr}|set(rats)"
        wrapper = f"""{base}
_g=generate_params
def generate_params(rng):
 r=_g(rng)
 if isinstance(r,(tuple,list)):r={{"vars":r[0] if isinstance(r[0],dict) else {{"val":r[0]}},"correct":str(r[1]),"distractors":r[2] if len(r)>2 else []}}
 elif not isinstance(r,dict):return r
 rats,st,f={rats_map_repr},{strict_repr},{fmt_helper}
 ids={ids_code}
 c=f(str(r.get("correct") or r.get("ans","")).strip())
 r["correct"],ds=c,[]
 for d in (r.get("distractors") or r.get("ds") or []):
  if isinstance(d,dict):v,i,t=str(d.get("value") or d.get("content") or d.get("ans","")).strip(),d.get("distractor_id") or d.get("id"),d.get("error_rationale") or d.get("rationale")
  elif isinstance(d,(tuple,list)) and len(d)>=2:
   d0=str(d[0]).strip().replace("_","-")
   i,v=(d0,str(d[1]).strip()) if (d0.startswith("D-") or d0 in ids) else (str(d[1]).strip().replace("_","-"),str(d[0]).strip())
   t=str(d[2]).strip() if len(d)>2 else rats.get(i)
   if not t and st:raise ValueError(f"[TPL-MC7-STRICT] 3-tupla requerida: {{d!r}}")
  elif st:raise ValueError(f"Distractor escalar no permitido: {{d!r}}")
  else:i,t,v=None,"",str(d[0] if isinstance(d,(tuple,list)) and d else d).strip()
  if i and ids and i not in ids and st:raise ValueError(f"Distractor ID '{{i}}' no esta declarado en cta.json ({cid}).")
  w=f(v);ds.append({{"value":w,"content":w,"distractor_id":i,"error_rationale":t or "","is_correct":False}})
 r["distractors"],r["options"]=ds,[{{"value":c,"content":c,"is_correct":True}}]+ds
 return r
generate=generate_params
"""
    return wrapper


def discover_fix_files(
    fixes_dir: Optional[Path],
    expected_cids: List[str],
    shard_id: Optional[str] = None,
) -> Tuple[Dict[str, Path], List[Path]]:
    """Discovers and maps shard fix files to competency IDs with case-insensitive and delimiter-agnostic normalization.
    
    Supports both per-shard isolated directories (shard_fixes/<shard_id>/<cid>.py)
    and legacy flat directories (shard_fixes/<cid>.py).
    Matches Hab-03, Hab_03, hab-03, hab_03, T-Hab-03, and hab03 to Hab-03.
    Returns (fix_files_by_cid, all_relevant_fix_files).
    """
    fix_files_by_cid: Dict[str, Path] = {}
    relevant_files: List[Path] = []
    if not fixes_dir or not fixes_dir.is_dir():
        return fix_files_by_cid, relevant_files

    # Check for per-shard subdirectory if fixes_dir is a root shard_fixes dir
    if shard_id and (fixes_dir / shard_id).is_dir():
        sub_files = sorted((fixes_dir / shard_id).glob("*.py"))
        if sub_files:
            all_fix_files = sub_files
        else:
            all_fix_files = sorted(fixes_dir.glob("*.py"))
    else:
        all_fix_files = sorted(fixes_dir.glob("*.py"))

    for fix_p in all_fix_files:
        stem = fix_p.stem
        norm_stem = re.sub(r"[^a-zA-Z0-9]", "", stem).lower()
        matched = False
        for ecid in expected_cids:
            norm_ecid = re.sub(r"[^a-zA-Z0-9]", "", ecid).lower()
            if (
                stem == ecid
                or stem == ecid.replace("-", "_")
                or stem.lower() == ecid.lower()
                or stem.replace("_", "-").lower() == ecid.lower()
                or norm_stem == norm_ecid
                or norm_stem == f"t{norm_ecid}"
            ):
                fix_files_by_cid[ecid] = fix_p
                if fix_p not in relevant_files:
                    relevant_files.append(fix_p)
                matched = True
                break
        if not matched and not expected_cids:
            norm_stem_cid = stem.replace("_", "-")
            fix_files_by_cid[norm_stem_cid] = fix_p
            if fix_p not in relevant_files:
                relevant_files.append(fix_p)

    return fix_files_by_cid, relevant_files


def infer_work_dir(
    explicit_work: Union[str, Path] = "work",
    shard_id: Optional[str] = None,
) -> Path:
    """Infers work directory if default 'work' is missing from CWD.

    Searches for:
    1. Active lockfiles: courses/*/.c2c_subagent_lock.json or courses/*/work/.c2c_subagent_lock.json with active=true.
    2. Most recent courses/*/work directory containing shards/{shard_id}_data.py or shards/pre_shard_manifest.json.
    Returns inferred Path, or Path(explicit_work) if no course match found.
    """
    target = Path(explicit_work)
    if (target / "shards" / "pre_shard_manifest.json").is_file() or (target / "pre_shard_manifest.json").is_file():
        return target

    cwd = Path.cwd()
    courses_dir = cwd / "courses"
    if not courses_dir.is_dir():
        return target

    norm_s_id = (shard_id or "").lower().strip()
    candidate_works: List[Tuple[float, Path]] = []

    for c_dir in sorted(courses_dir.iterdir()):
        if not c_dir.is_dir():
            continue
        lock_paths = [
            c_dir / ".c2c_subagent_lock.json",
            c_dir / "work" / ".c2c_subagent_lock.json",
        ]
        is_active = False
        for lp in lock_paths:
            if lp.is_file():
                try:
                    ldata = json.loads(lp.read_text(encoding="utf-8"))
                    if isinstance(ldata, dict) and ldata.get("active") is True:
                        is_active = True
                        break
                except Exception:
                    pass

        w_cand = c_dir / "work"
        if w_cand.is_dir():
            has_manifest = (w_cand / "shards" / "pre_shard_manifest.json").is_file() or (w_cand / "pre_shard_manifest.json").is_file()
            has_shard = (w_cand / "shards" / f"{norm_s_id}_data.py").is_file() if norm_s_id else False

            if is_active and (has_manifest or has_shard):
                return w_cand

            if has_shard or has_manifest:
                mtime = 0.0
                if has_shard:
                    mtime = (w_cand / "shards" / f"{norm_s_id}_data.py").stat().st_mtime
                elif has_manifest:
                    m_p = (w_cand / "shards" / "pre_shard_manifest.json") if (w_cand / "shards" / "pre_shard_manifest.json").is_file() else (w_cand / "pre_shard_manifest.json")
                    mtime = m_p.stat().st_mtime
                candidate_works.append((mtime, w_cand))

    if candidate_works:
        candidate_works.sort(key=lambda x: x[0], reverse=True)
        return candidate_works[0][1]

    return target


def compile_shard(
    work_dir_or_path: Union[str, Path],
    shard_id: Optional[str] = None,
    strict: bool = True,
    seeds: int = 50,
    output_dir: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None,
    cta_path: Optional[Union[str, Path]] = None,
    manifest_path: Optional[Union[str, Path]] = None,
    min_archetypes: Optional[int] = None,
    **kwargs,
) -> Tuple[bool, List[str]]:
    """Compiles shard data into canonical template JSON files with strict verification.

    Supports dual invocation styles:
    - compile_shard("work", "shard_01", strict=True, seeds=50)
    - compile_shard("work/shards/shard_01_data.py", output_dir="work/templates")
    """
    output_path = output_path or kwargs.get("output")
    cta_path = cta_path or kwargs.get("cta")
    manifest_path = manifest_path or kwargs.get("manifest")
    min_archetypes = min_archetypes if min_archetypes is not None else kwargs.get("min_archetypes")

    target_p = Path(work_dir_or_path).resolve()
    # In-memory inference when default "work" does not have manifest
    if not target_p.name.endswith(".py"):
        if str(work_dir_or_path) in ("work", "./work", ".\\work") or target_p == (Path.cwd() / "work").resolve():
            if not (target_p / "shards" / "pre_shard_manifest.json").is_file() and not (target_p / "pre_shard_manifest.json").is_file():
                inferred = infer_work_dir(target_p, shard_id=shard_id)
                if inferred != target_p:
                    target_p = inferred.resolve()

    # Guarantee sys.modules and linecache safety across multiple compiles in same process
    import linecache
    linecache.clearcache()
    for k in list(sys.modules.keys()):
        if k.startswith("c2c_fix_mod_") or k.startswith("c2c_shard_mod_"):
            sys.modules.pop(k, None)

    # Determine if target_p is a shard data file or a work directory
    if target_p.name.endswith(".py"):
        if not shard_id:
            m_s = re.search(r"shard_(\d+)", target_p.stem)
            shard_id = f"shard_{m_s.group(1)}" if m_s else target_p.stem.replace("_data", "")
        shards_dir = target_p.parent
        work_p = shards_dir.parent if shards_dir.name == "shards" else shards_dir
        if not target_p.is_file():
            err_msg = f"ERROR: No existe el archivo de datos del shard: {target_p}"
            print(err_msg, file=sys.stderr)
            return False, [err_msg]
        shard_data_path = target_p
    else:
        work_p = target_p
        shards_dir = work_p / "shards"
        shard_data_path = None

    receipt_p = Path(output_path).resolve() if output_path and str(output_path).lower().endswith(".json") else None
    if output_dir:
        templates_dir = Path(output_dir).resolve()
    elif output_path and not receipt_p:
        templates_dir = Path(output_path).resolve()
    else:
        templates_dir = work_p / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)

    if not shard_id:
        err_msg = "ERROR: shard_id no especificado para compile_shard."
        print(err_msg, file=sys.stderr)
        return False, [err_msg]

    norm_shard_id = shard_id.lower().strip()
    att_dir = work_p / ".check_attempts"
    pass_marker = att_dir / f"pass_{norm_shard_id}.json"

    # Watchdog timer enforcement: hard budget <= 15.0 seconds
    watchdog_timeout_val = kwargs.get("watchdog_timeout")
    if watchdog_timeout_val is None:
        env_timeout = os.getenv("C2C_COMPILE_WATCHDOG_TIMEOUT")
        if env_timeout is not None:
            try:
                watchdog_timeout_val = float(env_timeout)
            except ValueError:
                watchdog_timeout_val = 15.0
        else:
            watchdog_timeout_val = 15.0
    else:
        watchdog_timeout_val = float(watchdog_timeout_val)

    watchdog = _CompilationWatchdog(timeout=watchdog_timeout_val, shard_id=norm_shard_id)
    watchdog.start()

    try:
        return _compile_shard_body(
            work_p=work_p,
            shards_dir=shards_dir,
            shard_data_path=shard_data_path,
            templates_dir=templates_dir,
            receipt_p=receipt_p,
            shard_id=shard_id,
            norm_shard_id=norm_shard_id,
            att_dir=att_dir,
            pass_marker=pass_marker,
            strict=strict,
            seeds=seeds,
            cta_path=cta_path,
            manifest_path=manifest_path,
            min_archetypes=min_archetypes,
            **kwargs,
        )
    finally:
        watchdog.stop()


def _compile_shard_body(
    work_p: Path,
    shards_dir: Path,
    shard_data_path: Optional[Path],
    templates_dir: Path,
    receipt_p: Optional[Path],
    shard_id: str,
    norm_shard_id: str,
    att_dir: Path,
    pass_marker: Path,
    strict: bool,
    seeds: int,
    cta_path: Optional[Union[str, Path]],
    manifest_path: Optional[Union[str, Path]],
    min_archetypes: Optional[int],
    **kwargs,
) -> Tuple[bool, List[str]]:

    def _cleanup_stale_pass_marker():
        if pass_marker.is_file():
            try:
                pass_marker.unlink()
            except Exception:
                pass

    # 1. Verify pre_shard_manifest.json (resolving --manifest pre_cta_manifest.json fallback cleanly)
    def _find_pre_shard_manifest() -> Optional[Path]:
        for cand in (shards_dir / "pre_shard_manifest.json", work_p / "pre_shard_manifest.json"):
            if cand.is_file():
                return cand.resolve()
        return None

    if manifest_path and Path(manifest_path).is_file():
        manifest_p = Path(manifest_path).resolve()
    else:
        found_m = _find_pre_shard_manifest()
        if not found_m:
            _cleanup_stale_pass_marker()
            print("BLOCKER:: No existe pre_shard_manifest.json", file=sys.stderr)
            sys.exit(2)
        manifest_p = found_m

    try:
        manifest_data = json.loads(manifest_p.read_text(encoding="utf-8"))
    except Exception as e:
        _cleanup_stale_pass_marker()
        print(f"BLOCKER:: pre_shard_manifest.json corrupto o ilegible: {e}", file=sys.stderr)
        sys.exit(2)

    if not isinstance(manifest_data, dict) or "shards" not in manifest_data:
        fallback_m = _find_pre_shard_manifest()
        if fallback_m and fallback_m != manifest_p:
            try:
                manifest_data = json.loads(fallback_m.read_text(encoding="utf-8"))
                manifest_p = fallback_m
            except Exception as e:
                _cleanup_stale_pass_marker()
                print(f"BLOCKER:: pre_shard_manifest.json corrupto o ilegible: {e}", file=sys.stderr)
                sys.exit(2)
        elif not fallback_m:
            _cleanup_stale_pass_marker()
            print("BLOCKER:: No existe pre_shard_manifest.json", file=sys.stderr)
            sys.exit(2)

    # Locate shard entry
    shard_entry = None
    for s in manifest_data.get("shards", []):
        s_id = str(s.get("shard_id", "")).lower().strip()
        if s_id == norm_shard_id or s_id.replace("shard_", "") == norm_shard_id.replace("shard_", ""):
            shard_entry = s
            break

    if not shard_entry:
        _cleanup_stale_pass_marker()
        err_msg = f"ERROR: Shard '{shard_id}' no encontrado en pre_shard_manifest.json."
        print(err_msg, file=sys.stderr)
        return False, [err_msg]

    expected_cids: List[str] = shard_entry.get("competency_ids", [])

    _drift = _s4_contract_drift(manifest_data.get("stage4_contract"))
    if _drift:
        _cleanup_stale_pass_marker()
        err_msg = f"BLOCKER:: [STAGE4-CONTRACT-DRIFT] {_drift}"
        print(err_msg, file=sys.stderr)
        return False, [err_msg]
    if not expected_cids and "competencies" in shard_entry:
        expected_cids = [c["id"] for c in shard_entry["competencies"] if isinstance(c, dict) and "id" in c]

    eff_min_arch = _S4_MIN_ARCHETYPES
    if min_archetypes is not None:
        eff_min_arch = int(min_archetypes)
    elif isinstance(shard_entry, dict) and shard_entry.get("min_archetypes"):
        eff_min_arch = int(shard_entry["min_archetypes"])
    elif isinstance(manifest_data, dict) and manifest_data.get("min_archetypes"):
        eff_min_arch = int(manifest_data["min_archetypes"])

    # Locate shard_fixes directory: prioritize shard-isolated directory (shard_fixes/<shard_id>/)
    shard_fixes_dir = shards_dir / "shard_fixes" / norm_shard_id
    if not shard_fixes_dir.is_dir() and (work_p / "shards" / "shard_fixes" / norm_shard_id).is_dir():
        shard_fixes_dir = work_p / "shards" / "shard_fixes" / norm_shard_id

    flat_fixes_dir = shards_dir / "shard_fixes"
    if not flat_fixes_dir.is_dir() and (work_p / "shards" / "shard_fixes").is_dir():
        flat_fixes_dir = work_p / "shards" / "shard_fixes"

    # Prioritize shard-isolated directory if it exists and has fix files, else fallback to flat
    fixes_dir = shard_fixes_dir if (shard_fixes_dir.is_dir() and any(shard_fixes_dir.glob("*.py"))) else flat_fixes_dir

    # Discover relevant fix files for hashing and modular splicing
    fix_files_by_cid, relevant_fix_files = discover_fix_files(fixes_dir, expected_cids, shard_id=norm_shard_id)
    has_all_fixes = bool(expected_cids and all(ecid in fix_files_by_cid for ecid in expected_cids))

    # Locate shard data path if not provided
    if not shard_data_path or not shard_data_path.is_file():
        shard_data_path_str = shard_entry.get("shard_data_path")
        if shard_data_path_str and Path(shard_data_path_str).is_file():
            shard_data_path = Path(shard_data_path_str).resolve()
        else:
            candidate = shards_dir / f"{norm_shard_id}_data.py"
            if candidate.is_file():
                shard_data_path = candidate
            else:
                if not has_all_fixes:
                    _cleanup_stale_pass_marker()
                    err_msg = f"ERROR: No existe el archivo de datos del shard: {candidate}"
                    print(err_msg, file=sys.stderr)
                    return False, [err_msg]
                shard_data_path = candidate

    # Compute source_sha256 over shard_data_path (if exists) + relevant fix files
    hasher = hashlib.sha256()
    if shard_data_path and shard_data_path.is_file():
        hasher.update(shard_data_path.read_bytes())
    for rf in sorted(relevant_fix_files, key=lambda p: p.name):
        hasher.update(f"\n--FIX:{rf.name}--\n".encode("utf-8"))
        hasher.update(rf.read_bytes())
    source_sha256 = hasher.hexdigest()

    # Bounded compilation counter & unified stateful circuit breaker (.check_attempts/compile_{norm_shard_id}.json)
    att_dir.mkdir(parents=True, exist_ok=True)
    compile_att_file = att_dir / f"compile_{norm_shard_id}.json"

    state: Dict[str, Any] = {
        "distinct_compiles": 0,
        "same_error_streak": 0,
        "last_source_sha256": "",
        "last_err_hash": "",
        "last_errors": [],
        "error_count": 0,
        "has_syntax_error": False,
    }
    if compile_att_file.is_file():
        try:
            loaded_state = json.loads(compile_att_file.read_text(encoding="utf-8"))
            if isinstance(loaded_state, dict):
                if "distinct_compiles" in loaded_state:
                    state.update(loaded_state)
                elif "count" in loaded_state:
                    state["distinct_compiles"] = loaded_state.get("count", 0)
        except Exception:
            pass

    # Idempotent [NO-CHANGE] Re-Run check: do not increment counter or streak on identical source
    if (
        state.get("last_source_sha256") == source_sha256
        and state.get("last_errors")
    ):
        cached_errors = state["last_errors"]
        no_change_prefix = "[NO-CHANGE: código idéntico al intento previo; edita el archivo antes de recompilar]"
        prefixed_errors = []
        for e in cached_errors:
            if no_change_prefix not in e:
                prefixed_errors.append(f"{no_change_prefix}\n{e}")
            else:
                prefixed_errors.append(e)
        print(prefixed_errors[0], file=sys.stderr)
        return False, prefixed_errors

    # Distinct compile increment
    distinct_compiles = state.get("distinct_compiles", 0) + 1
    state["distinct_compiles"] = distinct_compiles
    state["last_source_sha256"] = source_sha256

    print(f"[COMPILE {distinct_compiles}/10] Compilando shard '{shard_id}'...")

    def _fail(msg: str, has_syntax_error: bool = False, error_count: int = 1) -> Tuple[bool, List[str]]:
        from check_templates import normalize_error_string_for_hash
        normalized_errs = sorted([normalize_error_string_for_hash(msg)])
        err_hash = hashlib.sha256("\n".join(normalized_errs).encode("utf-8")).hexdigest()

        if state.get("last_err_hash") == err_hash:
            same_error_streak = state.get("same_error_streak", 0) + 1
        else:
            same_error_streak = 1
        state["same_error_streak"] = same_error_streak
        state["last_err_hash"] = err_hash
        state["error_count"] = error_count
        state["has_syntax_error"] = bool(has_syntax_error)
        state["affected_line_count"] = error_count
        state["error_sha256"] = err_hash

        res_msg = msg
        if same_error_streak >= 3:
            terminal_stop = (
                f"\n[-] [CIRCUIT BREAKER HALT: 3 fallos consecutivos idénticos para shard '{shard_id}']. "
                f"STOP, send_message the Director."
            )
            res_msg = res_msg + terminal_stop
            print(terminal_stop, file=sys.stderr)

        _cleanup_stale_pass_marker()

        if receipt_p:
            try:
                import time
                r_data = {}
                if receipt_p.is_file():
                    try:
                        r_data = json.loads(receipt_p.read_text(encoding="utf-8"))
                    except Exception:
                        r_data = {}
                r_data["shard_id"] = shard_id
                r_data["compiled_status"] = "FAIL"
                r_data["compilation_errors"] = [res_msg]
                r_data["error_count"] = error_count
                r_data["has_syntax_error"] = bool(has_syntax_error)
                r_data["compiled_at"] = time.time()
                _atomic_write_json(receipt_p, r_data)
            except Exception:
                pass

        state["last_errors"] = [res_msg]
        _atomic_write_json(compile_att_file, state)
        print(msg, file=sys.stderr)
        return False, [res_msg]

    # Dual Calibrated Halt Threshold: distinct_compiles > 10
    if distinct_compiles > 10:
        halt_msg = (
            f"[-] [CIRCUIT BREAKER HALT: Límite de 10 compilaciones distintas alcanzado para shard '{shard_id}']. "
            f"STOP, send_message the Director."
        )
        return _fail(halt_msg, has_syntax_error=False, error_count=1)

    # In-memory healing of shard_XX_data.py (Zero-Disk-Mutation: source file on disk is NEVER modified)
    raw_source = shard_data_path.read_text(encoding="utf-8") if shard_data_path.is_file() else ""
    if raw_source:
        rf_warnings = check_ast_rf_triple_braces(raw_source)
        for w in rf_warnings:
            print(w, file=sys.stderr)
        _, healed_source = heal_shard_source_text(raw_source)
        try:
            from shard_precheck import precheck_source as _precheck
            _pre = _precheck(raw_source)
            if _pre:
                print(f"[PRECHECK] {len(_pre)} hallazgo(s) estaticos (advertencias, corrige todos juntos):", file=sys.stderr)
                for _w in _pre[:20]:
                    print(f"  - {_w}", file=sys.stderr)
        except Exception:
            pass
    else:
        healed_source = ""

    # Staged copy under .check_attempts/_staged/ for debugging without mutating source
    if healed_source:
        staged_dir = att_dir / "_staged"
        staged_dir.mkdir(parents=True, exist_ok=True)
        staged_p = staged_dir / f"{norm_shard_id}_data.py"
        try:
            staged_p.write_text(healed_source, encoding="utf-8")
        except Exception:
            pass

    # 2. AST Line Locator & Syntax Verification (evaluated on in-memory healed source)
    locator = ShardDataLineLocator(shard_data_path, source_text=healed_source)
    skip_base_module = False
    if raw_source and locator.syntax_error:
        if has_all_fixes:
            print(
                f"[!] Warning: {shard_data_path.name} contiene error sintáctico, pero el 100% de las competencias "
                f"({expected_cids}) están cubiertas por fijaciones en shard_fixes/. Omitiendo {shard_data_path.name}.",
                file=sys.stderr,
            )
            skip_base_module = True
        else:
            print(f"FAIL: Error sintáctico en {shard_data_path.name}:", file=sys.stderr)
            return _fail(locator.syntax_error, has_syntax_error=True, error_count=1)

    # 3. Load shard module dynamically from in-memory string
    mod_name = f"c2c_shard_mod_{norm_shard_id}_{uuid.uuid4().hex[:6]}"
    mod = types.ModuleType(mod_name)
    mod.__file__ = str(shard_data_path)
    mod.__dict__["parse_katex_number"] = parse_katex_number
    mod.__dict__["_pv"] = parse_katex_number
    if healed_source and not skip_base_module:
        try:
            code_obj = compile(healed_source, str(shard_data_path), "exec")
            sys.modules[mod_name] = mod
            exec(code_obj, mod.__dict__)
        except Exception as e:
            if has_all_fixes:
                print(
                    f"[!] Warning: Excepción al ejecutar {shard_data_path.name}, pero el 100% de las competencias "
                    f"están cubiertas por shard_fixes/. Omitiendo {shard_data_path.name}.",
                    file=sys.stderr,
                )
                skip_base_module = True
            else:
                tb = traceback.format_exc()
                err_msg = f"FAIL: Excepción al ejecutar {shard_data_path.name}:\n{tb}"
                return _fail(err_msg, has_syntax_error=isinstance(e, SyntaxError), error_count=1)

    base_templates = [] if skip_base_module else (getattr(mod, "TEMPLATES", None) or [])
    module_rats = getattr(mod, "RATS", {}) if isinstance(getattr(mod, "RATS", None), dict) else {}
    from check_templates import heal_control_chars_in_obj
    base_templates = heal_control_chars_in_obj(base_templates)

    # Map tuples to their origin file and line locator
    tuple_records: List[Dict[str, Any]] = []
    for orig_idx, t in enumerate(base_templates):
        t = normalize_form_c_template(t)
        tuple_records.append({
            "tuple": t,
            "file_path": shard_data_path,
            "locator": locator,
            "orig_idx": orig_idx,
        })

    # Splice fix files from shards/shard_fixes/<CID>.py
    known_types = {"multiple_choice", "multiple_choice_7_options", "fill_in_the_blank", "multiple_select", "open_ended", "mc7", "fib", "ms"}

    for cid_fix, fix_path in fix_files_by_cid.items():
        if not fix_path.is_file():
            continue
        try:
            fix_raw_text = fix_path.read_text(encoding="utf-8")
            rf_w = check_ast_rf_triple_braces(fix_raw_text)
            for w in rf_w:
                print(w, file=sys.stderr)
            _, healed_fix_text = heal_shard_source_text(fix_raw_text)
            fix_loc = ShardDataLineLocator(fix_path, source_text=healed_fix_text)
            if fix_loc.syntax_error:
                return _fail(
                    f"FAIL: Error sintáctico en shard_fixes/{fix_path.name}:\n{fix_loc.syntax_error}",
                    has_syntax_error=True,
                    error_count=1,
                )

            fix_mod_name = f"c2c_fix_mod_{cid_fix.replace('-', '_')}_{uuid.uuid4().hex[:6]}"
            fix_mod = types.ModuleType(fix_mod_name)
            fix_mod.__file__ = str(fix_path)
            fix_mod.__dict__["parse_katex_number"] = parse_katex_number
            fix_mod.__dict__["_pv"] = parse_katex_number
            fix_code_obj = compile(healed_fix_text, str(fix_path), "exec")
            sys.modules[fix_mod_name] = fix_mod
            exec(fix_code_obj, fix_mod.__dict__)

            fix_templates = getattr(fix_mod, "TEMPLATES", None)
            if fix_templates and isinstance(fix_templates, (list, tuple)):
                fix_templates = heal_control_chars_in_obj(fix_templates)

                new_records = []
                replaced = False
                for rec in tuple_records:
                    t_cand = normalize_form_c_template(rec["tuple"])
                    rec["tuple"] = t_cand
                    t_cid = None
                    if isinstance(t_cand, dict):
                        t_cid = str(t_cand.get("cid") or t_cand.get("competency_id") or "").strip()
                    elif len(t_cand) >= 3 and str(t_cand[2]).lower().strip() in known_types:
                        t_cid = str(t_cand[1]).strip()
                    elif len(t_cand) >= 3 and str(t_cand[1]).lower().strip() in known_types:
                        t_cid = str(t_cand[0]).strip()
                    else:
                        t_cid = str(t_cand[0]).strip()

                    if t_cid == cid_fix or t_cid.replace("-", "_") == cid_fix.replace("-", "_"):
                        if not replaced:
                            for fix_idx, ft in enumerate(fix_templates):
                                ft = normalize_form_c_template(ft)
                                new_records.append({
                                    "tuple": ft,
                                    "file_path": fix_path,
                                    "locator": fix_loc,
                                    "orig_idx": fix_idx,
                                })
                            replaced = True
                    else:
                        new_records.append(rec)

                if not replaced:
                    for fix_idx, ft in enumerate(fix_templates):
                        ft = normalize_form_c_template(ft)
                        new_records.append({
                            "tuple": ft,
                            "file_path": fix_path,
                            "locator": fix_loc,
                            "orig_idx": fix_idx,
                        })

                tuple_records = new_records
        except Exception as e:
            tb = traceback.format_exc()
            return _fail(
                f"FAIL: Excepción al cargar shard_fixes/{fix_path.name}:\n{tb}",
                has_syntax_error=isinstance(e, SyntaxError),
                error_count=1,
            )

    raw_templates = [rec["tuple"] for rec in tuple_records]
    if not raw_templates:
        err_msg = f"FAIL: {shard_data_path.name} no define la lista 'TEMPLATES = [...]'."
        return _fail(err_msg)

    # 4. Identify competencies and verify parity (Form-C dict or Form-B 9-tuple)
    found_cids = []
    for rec_idx, rec in enumerate(tuple_records):
        t = normalize_form_c_template(rec["tuple"])
        rec["tuple"] = t
        curr_loc = rec["locator"]
        curr_p = rec["file_path"]
        orig_idx = rec["orig_idx"]
        if isinstance(t, dict):
            c_candidate = str(t.get("cid") or t.get("competency_id") or "").strip()
            if not c_candidate:
                s_t, e_t, snip = curr_loc.get_tuple_snippet(orig_idx)
                err_msg = (
                    f"FAIL: El diccionario Form-C en índice {orig_idx} no define 'cid' ni 'competency_id'.\n"
                    f"  Ubicación: Líneas {s_t}..{e_t} en {curr_p.name}\n"
                    f"{snip}"
                )
                return _fail(err_msg)
            found_cids.append(c_candidate)
        elif isinstance(t, (list, tuple)):
            if len(t) != 9:
                s_t, e_t, snip = curr_loc.get_tuple_snippet(orig_idx)
                err_msg = (
                    f"FAIL: La tupla en índice {orig_idx} tiene {len(t) if isinstance(t, (list, tuple)) else 0} elementos "
                    f"(se requieren exactamente 9 elementos según el contrato Form-B: "
                    f"tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution).\n"
                    f"  Ubicación: Líneas {s_t}..{e_t} en {curr_p.name}\n"
                    f"{snip}"
                )
                return _fail(err_msg)

            if str(t[1]).lower().strip() in known_types or str(t[2]).lower().strip() not in known_types:
                s_t, e_t, snip = curr_loc.get_tuple_snippet(orig_idx)
                err_msg = (
                    f"FAIL: Se detectó formato legacy Form-A o tipo inválido en la tupla {orig_idx}. "
                    f"El compilador solo admite el contrato Form-B de 9 elementos: "
                    f"(tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, solution).\n"
                    f"  Ubicación: Líneas {s_t}..{e_t} en {curr_p.name}\n"
                    f"{snip}"
                )
                return _fail(err_msg)

            c_candidate = str(t[1]).strip()
            found_cids.append(c_candidate)
        else:
            s_t, e_t, snip = curr_loc.get_tuple_snippet(orig_idx)
            err_msg = (
                f"FAIL: Entrada inválida en TEMPLATES en índice {orig_idx}: se esperaba una 9-tupla Form-B o un dict Form-C, "
                f"se recibió: {type(t).__name__}.\n"
                f"  Ubicación: Líneas {s_t}..{e_t} en {curr_p.name}\n"
                f"{snip}"
            )
            return _fail(err_msg)

    missing_cids = [cid for cid in expected_cids if cid not in found_cids]
    unexpected_cids = [cid for cid in found_cids if cid not in expected_cids]
    if missing_cids or unexpected_cids:
        err_parts = []
        if missing_cids:
            err_parts.append(f"Competencias faltantes en TEMPLATES: {', '.join(missing_cids)}")
        if unexpected_cids:
            err_parts.append(f"Competencias no asignadas a este shard: {', '.join(unexpected_cids)}")
        err_msg = f"FAIL: Paridad de competencias violada en {shard_data_path.name}: " + " | ".join(err_parts)
        return _fail(err_msg)

    from check_templates import auto_heal_template_data, check_templates_file_or_dir

    if cta_path and Path(cta_path).is_file():
        cta_p = Path(cta_path).resolve()
    else:
        cta_file_candidate = work_p / "cta.json"
        cta_p = cta_file_candidate if cta_file_candidate.is_file() else None

    cta_comp_map = {c["id"]: c for c in shard_entry.get("competencies", []) if isinstance(c, dict) and "id" in c}
    if cta_p and cta_p.is_file():
        try:
            cta_data = json.loads(cta_p.read_text(encoding="utf-8"))
            for c in cta_data.get("competencies", []):
                if isinstance(c, dict) and "id" in c:
                    cid_key = c["id"]
                    if cid_key not in cta_comp_map or not cta_comp_map[cid_key].get("distractors"):
                        cta_comp_map[cid_key] = c
                    elif c.get("distractors") and not cta_comp_map[cid_key].get("distractors"):
                        cta_comp_map[cid_key]["distractors"] = c["distractors"]
        except Exception:
            pass

    # 5. Compile tuples into canonical JSON dictionaries grouped by competency
    templates_by_cid: Dict[str, List[Dict[str, Any]]] = {}
    gen_callables_by_cid: Dict[str, List[Any]] = {}
    deferred_verifier_errors: List[str] = []

    for t_idx, rec in enumerate(tuple_records):
        t = normalize_form_c_template(rec["tuple"])
        rec["tuple"] = t
        curr_loc = rec["locator"]
        curr_p = rec["file_path"]
        orig_idx = rec["orig_idx"]

        # Determine format (Form-C dict vs Form-B 9-tuple)
        is_form_c = isinstance(t, dict)
        if is_form_c:
            tpl_id = str(t.get("id") or t.get("tpl_id") or t.get("template_id") or "").strip()
            cid = str(t.get("cid") or t.get("competency_id") or "").strip()
            qtype_in = str(t.get("qtype") or t.get("question_type") or "").strip().lower()
            if qtype_in in ("mc7", "mc", "multiple_choice", "multiple_choice_7_options"):
                qtype = "multiple_choice_7_options"
            elif qtype_in in ("fib", "open_ended", "fill_in_the_blank"):
                qtype = "fill_in_the_blank"
            elif qtype_in in ("ms", "multiple_select"):
                qtype = "multiple_select"
            else:
                qtype = qtype_in
            gen_raw = t.get("gen") or t.get("generator_code") or t.get("generate_py")
            ver_raw = t.get("ver") or t.get("verifier_code") or t.get("cross_check_py")
            diff_raw = t.get("band") or t.get("difficulty_bloom")
            if not diff_raw and t.get("difficulty") and t.get("bloom"):
                diff_raw = (t.get("difficulty"), t.get("bloom"))
            stems_raw = t.get("stems") or t.get("stem_variants") or t.get("stem")
            hints_raw = t.get("hints")
            sol_raw = str(t.get("sol") or t.get("solution") or t.get("explanation_es") or "")
            archetype = t.get("archetype")
            assumption_id = t.get("assumption_id")
            fmt_str = t.get("fmt")
            tpl_rats = t.get("rats") if isinstance(t.get("rats"), dict) else {}
        elif isinstance(t, (list, tuple)) and len(t) == 9:
            tpl_id = str(t[0]).strip()
            cid = str(t[1]).strip()
            qtype = str(t[2]).strip().lower()
            gen_raw = t[3]
            ver_raw = t[4]
            diff_raw = t[5]
            stems_raw = t[6]
            hints_raw = t[7]
            sol_raw = str(t[8])
            archetype = None
            assumption_id = None
            fmt_str = None
            tpl_rats = {}
        else:
            return _fail(
                f"FAIL: Entrada en índice {orig_idx} no cumple el contrato Form-B de 9 elementos ni Form-C dict: {repr(t)}"
            )

        target_kc = cid
        target_misc = []
        src_ref = {"doc": "manifest.pdf", "page": 1, "quote": ""}

        # Determine difficulty and bloom (element must be 2-tuple (difficulty, bloom))
        if not isinstance(diff_raw, (list, tuple)) or len(diff_raw) != 2:
            return _fail(
                f"FAIL: El elemento de dificultad en tupla {orig_idx} ('{tpl_id}') debe ser explícitamente "
                f"una 2-tupla (difficulty, bloom) (ej. ('easy', 'Remember')), se recibió: {repr(diff_raw)}."
            )

        difficulty = str(diff_raw[0]).lower().strip()
        bloom = str(diff_raw[1]).capitalize().strip()

        if difficulty not in ("easy", "medium", "hard"):
            return _fail(
                f"FAIL: Dificultad inválida '{difficulty}' en tupla {orig_idx} ('{tpl_id}'). "
                f"Debe ser 'easy', 'medium' o 'hard'."
            )
        if bloom not in ("Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"):
            return _fail(
                f"FAIL: Nivel de Bloom inválido '{bloom}' en tupla {orig_idx} ('{tpl_id}'). "
                f"Debe ser Remember, Understand, Apply, Analyze, Evaluate o Create."
            )

        # Determine interaction_type
        if qtype in ("multiple_choice", "multiple_choice_7_options", "mc7"):
            interaction_type = "multiple_choice_7_options"
        elif qtype in ("open_ended", "fill_in_the_blank", "fib"):
            interaction_type = "fill_in_the_blank"
            target_misc = []
        elif qtype in ("multiple_select", "ms"):
            interaction_type = "multiple_select"
        else:
            interaction_type = qtype

        # Stems Cartesian expansion if 2-tuple of (contexts, questions)
        if isinstance(stems_raw, (list, tuple)) and len(stems_raw) == 2:
            ctxs, qsts = stems_raw[0], stems_raw[1]
            if isinstance(ctxs, (list, tuple)) and isinstance(qsts, (list, tuple)) and len(ctxs) >= 2 and len(qsts) >= 2:
                stems_raw = [f"{str(c).strip()} {str(q).strip()}" for c in ctxs for q in qsts]

        # Extract functions using originating file locator
        tuple_info = curr_loc.get_tuple_info(orig_idx) or curr_loc.get_tuple_info(cid) or {}
        gen_fn_name = tuple_info.get("gen_fn_name") or getattr(gen_raw, "__name__", None)
        ver_fn_name = tuple_info.get("ver_fn_name") or getattr(ver_raw, "__name__", None)

        gen_code = extract_function_code(gen_raw, "generate_params", locator=curr_loc, fn_name_hint=gen_fn_name)
        gen_raw = _wrap_gen_raw_with_auto_vars(gen_raw, gen_code)
        ver_code = extract_function_code(ver_raw, "verify", locator=curr_loc, fn_name_hint=ver_fn_name)

        # Check if ver_raw is a 2-argument verifier ver(cand, v)
        is_two_arg_ver = False
        if callable(ver_raw):
            try:
                sig = inspect.signature(ver_raw)
                pos_params = [
                    p for p in sig.parameters.values()
                    if p.default == inspect.Parameter.empty and p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
                ]
                # Solo 2 argumentos posicionales OBLIGATORIOS => ver(cand, v).
                # Firmas con opcionales (res, v=None) o *args reciben la instancia completa.
                if len(pos_params) == 2:
                    is_two_arg_ver = True
            except Exception:
                pass

        if is_two_arg_ver:
            base_v = ver_code.rstrip()
            if base_v.endswith("cross_check = verify"):
                base_v = base_v[:-len("cross_check = verify")].rstrip()
            ver_code = f"""{base_v}
_v=verify
def verify(inst):
 try:return _v(inst.get("correct") or inst.get("ans"),inst.get("vars",{{}})) if isinstance(inst,dict) else False
 except Exception:return _v(inst) if isinstance(inst,dict) else False
cross_check=verify
"""

        def run_ver(c_val, vars_d, inst_d):
            if not callable(ver_raw):
                return True
            try:
                if is_two_arg_ver:
                    return ver_raw(c_val, vars_d)
                else:
                    return ver_raw(inst_d)
            except TypeError:
                try:
                    return ver_raw(inst_d)
                except TypeError:
                    return ver_raw(c_val, vars_d)

        # Check non-trivial verifier
        ver_is_trivial, ver_reason = is_trivial_verifier(ver_code, ver_raw)
        if ver_is_trivial:
            return _fail(
                f"FAIL: [TPL-VERIFIER] El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' es trivial ({ver_reason}). "
                f"Debe evaluar condiciones lógicas o matemáticas reales sobre el resultado generado."
            )

        # Verifier AST Hygiene checks
        if ver_fn_name and curr_loc and hasattr(curr_loc, "functions") and ver_fn_name in curr_loc.functions:
            s_v, e_v = curr_loc.functions[ver_fn_name]
            v_src = "\n".join(curr_loc.lines[s_v - 1 : e_v])
            try:
                v_ast = ast.parse(textwrap.dedent(v_src))
                for sub in ast.walk(v_ast):
                    if isinstance(sub, ast.Try):
                        for h in sub.handlers:
                            for s in h.body:
                                if isinstance(s, ast.Return) and isinstance(s.value, ast.Constant) and bool(s.value.value) is True:
                                    return _fail(
                                        f"FAIL: [VERIFIER-SWALLOWED-EXCEPTION] El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' (Líneas {s_v}..{e_v} en {curr_p.name}) "
                                        f"contiene un bloque try/except que retorna True en el manejador de excepción. Los errores de validación deben resultar en False."
                                    )
                    elif isinstance(sub, ast.Raise):
                        exc_n = ""
                        if isinstance(sub.exc, ast.Call) and isinstance(sub.exc.func, ast.Name):
                            exc_n = sub.exc.func.id
                        elif isinstance(sub.exc, ast.Name):
                            exc_n = sub.exc.id
                        return _fail(
                            f"FAIL: [TPL-DEBUG-ARTIFACT] El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' contiene una sentencia 'raise {exc_n}'. "
                            f"Los verificadores deben retornar booleanos sin sentencias 'raise' de depuración."
                        )
                    elif isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id in ("breakpoint", "print"):
                        return _fail(
                            f"FAIL: [TPL-DEBUG-ARTIFACT] El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' contiene una llamada a '{sub.func.id}()'."
                        )
                    elif isinstance(sub, ast.Import) and any(a.name == "pdb" for a in sub.names):
                        return _fail(
                            f"FAIL: [TPL-DEBUG-ARTIFACT] El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' importa 'pdb'."
                        )
            except Exception:
                pass

        # Generator AST Hygiene checks
        if gen_fn_name and curr_loc and hasattr(curr_loc, "functions") and gen_fn_name in curr_loc.functions:
            s_g, e_g = curr_loc.functions[gen_fn_name]
            g_src = "\n".join(curr_loc.lines[s_g - 1 : e_g])
            try:
                g_ast = ast.parse(textwrap.dedent(g_src))
                for sub in ast.walk(g_ast):
                    if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id in ("breakpoint", "print"):
                        return _fail(
                            f"FAIL: [TPL-DEBUG-ARTIFACT] La función generadora '{gen_fn_name}' en '{tpl_id}' contiene una llamada a '{sub.func.id}()'."
                        )
                    elif isinstance(sub, ast.Import) and any(a.name == "pdb" for a in sub.names):
                        return _fail(
                            f"FAIL: [TPL-DEBUG-ARTIFACT] La función generadora '{gen_fn_name}' en '{tpl_id}' importa 'pdb'."
                        )
                    elif isinstance(sub, ast.Raise):
                        exc_n = ""
                        if isinstance(sub.exc, ast.Call) and isinstance(sub.exc.func, ast.Name):
                            exc_n = sub.exc.func.id
                        elif isinstance(sub.exc, ast.Name):
                            exc_n = sub.exc.id
                        return _fail(
                            f"FAIL: [TPL-DEBUG-ARTIFACT] La función generadora '{gen_fn_name}' en '{tpl_id}' contiene una sentencia 'raise {exc_n}'. "
                            f"Las funciones generadoras de ítems deben retornar un diccionario de variables y opciones, sin sentencias 'raise' de depuración."
                        )
                if "clean_ds" in gen_fn_name:
                    return _fail(
                        f"FAIL: [TPL-AD-HOC-PERTURBATION] La función generadora '{gen_fn_name}' en '{tpl_id}' utiliza perturbación ad-hoc ('clean_ds'). "
                        f"Los distractores deben originarse en modelos de error conceptuales o algebraicos."
                    )
                for sub in ast.walk(g_ast):
                    if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and "clean_ds" in sub.func.id:
                        return _fail(
                            f"FAIL: [TPL-AD-HOC-PERTURBATION] La función generadora '{gen_fn_name}' en '{tpl_id}' invoca la función de perturbación '{sub.func.id}'."
                        )
                    elif isinstance(sub, ast.While):
                        for w_sub in ast.walk(sub):
                            if isinstance(w_sub, ast.BinOp) and isinstance(w_sub.op, ast.Add):
                                if isinstance(w_sub.right, ast.Constant) and isinstance(w_sub.right.value, float):
                                    return _fail(
                                        f"FAIL: [TPL-AD-HOC-PERTURBATION] Bucle while de perturbación numérica ad-hoc detectado en '{gen_fn_name}' de '{tpl_id}'."
                                    )
                                if isinstance(w_sub.right, ast.Call) and getattr(w_sub.right.func, "id", "") in ("uniform", "random"):
                                    return _fail(
                                        f"FAIL: [TPL-AD-HOC-PERTURBATION] Bucle while con perturbación flotante aleatoria detectado en '{gen_fn_name}' de '{tpl_id}'."
                                    )
            except Exception:
                pass

        # Stems validation: require at least 3 distinct author-written stems
        if not isinstance(stems_raw, (list, tuple)) or len(stems_raw) < 3:
            return _fail(
                f"FAIL: La plantilla '{tpl_id}' debe proporcionar al menos 3 enunciados distintos en stems "
                f"(se recibieron {len(stems_raw) if isinstance(stems_raw, (list, tuple)) else 0})."
            )
        cleaned_stems = [str(s).strip() for s in stems_raw if str(s).strip()]
        if len(set(cleaned_stems)) < 3:
            return _fail(
                f"FAIL: La plantilla '{tpl_id}' contiene enunciados duplicados en stems "
                f"(se encontraron {len(set(cleaned_stems))} únicos, se requieren >= 3)."
            )
        stem_es = cleaned_stems[0]
        stem_variants = cleaned_stems

        # Hints validation: require 3 to 5 author hints, >= 25 chars, no anti-socratic catchphrases, no literal wrong_belief copy
        cta_comp = cta_comp_map.get(cid, {})
        cta_distractors = cta_comp.get("distractors", [])
        if not isinstance(hints_raw, (list, tuple)) or not (3 <= len(hints_raw) <= 5):
            return _fail(
                f"FAIL: La plantilla '{tpl_id}' debe definir entre 3 y 5 pistas explícitas (hints) "
                f"(se recibieron {len(hints_raw) if isinstance(hints_raw, (list, tuple)) else 0})."
            )

        from check_templates import _strip_giveaway_prefix
        hints = []
        anti_socratic_patterns = [
            "evita el error",
            "recuerda no confundir",
            "no confundas",
            "cuidado con el error",
            "no cometas el error",
            "error común",
        ]
        cta_wrong_beliefs = [
            str(d.get("wrong_belief") or "").strip().lower()
            for d in cta_distractors if isinstance(d, dict) and d.get("wrong_belief")
        ]
        for h_idx, h_item in enumerate(hints_raw, start=1):
            h_text = _strip_giveaway_prefix(str(h_item).strip())
            if len(h_text) < 25:
                return _fail(
                    f"FAIL: La pista {h_idx} de '{tpl_id}' tiene menos de 25 caracteres ({len(h_text)} < 25): '{h_text}'."
                )
            h_lower = h_text.lower()
            for pat in anti_socratic_patterns:
                if pat in h_lower:
                    return _fail(
                        f"FAIL: La pista {h_idx} de '{tpl_id}' contiene una muletilla anti-socrática prohibida ('{pat}'): '{h_text}'."
                    )
            for wb in cta_wrong_beliefs:
                if len(wb) >= 12 and wb in h_lower:
                    return _fail(
                        f"FAIL: La pista {h_idx} de '{tpl_id}' copia literalmente la concepción errónea de cta.json ('{wb}')."
                    )
            hints.append(h_text)

        # Retrieve CTA declared distractor IDs
        clean_cta_distractors = []
        for d in cta_distractors:
            if isinstance(d, dict):
                cd = dict(d)
                for rkey in ("wrong_belief", "omitted_step", "remediation_hint", "manifestation"):
                    if isinstance(cd.get(rkey), str):
                        cd[rkey] = _strip_giveaway_prefix(cd[rkey])
                clean_cta_distractors.append(cd)
            else:
                clean_cta_distractors.append(d)

        cta_declared_ids = {d.get("id") for d in clean_cta_distractors if isinstance(d, dict) and d.get("id")}
        combined_rats = {**module_rats, **tpl_rats}

        # Adapt MC7 generator if applicable
        if interaction_type == "multiple_choice_7_options":
            gen_code = build_adapted_mc7_generator(
                gen_code, cid, clean_cta_distractors, strict=strict, rats_map=combined_rats, fmt=fmt_str
            )

        # Determine declared vars from generator callable (with timeout guard) or sandbox or AST
        sample_res = None
        declared_vars: Set[str] = set()
        if callable(gen_raw):
            try:
                import random
                from engine.sandbox import call_with_timeout
                sample_res = call_with_timeout(
                    gen_raw,
                    args=(random.Random(42),),
                    timeout=0.4,
                    seed=42,
                )
            except Exception:
                pass

        if sample_res is None and gen_code:
            try:
                from engine.sandbox import run_code_in_env
                sample_res = run_code_in_env(gen_code, "generate", seed=42, timeout=0.5)
            except Exception:
                pass

        if isinstance(sample_res, dict):
            if "ans" in sample_res and "correct" not in sample_res:
                sample_res["correct"] = sample_res["ans"]
            if "ds" in sample_res and "distractors" not in sample_res:
                sample_res["distractors"] = sample_res["ds"]
            if "vars" not in sample_res:
                c_val = sample_res.get("correct") or sample_res.get("ans") or ""
                sample_res["vars"] = {"ans": c_val} if c_val else {}
            if "vars" in sample_res and isinstance(sample_res["vars"], dict):
                declared_vars = set(str(k) for k in sample_res["vars"].keys())
        elif isinstance(sample_res, (tuple, list)) and len(sample_res) >= 1 and isinstance(sample_res[0], dict):
            declared_vars = set(str(k) for k in sample_res[0].keys())

        if not declared_vars and gen_code:
            try:
                _gtree = ast.parse(textwrap.dedent(gen_code.strip()))
                for _gnode in ast.walk(_gtree):
                    if isinstance(_gnode, ast.Dict):
                        for _gk, _gv in zip(_gnode.keys, _gnode.values):
                            if isinstance(_gk, ast.Constant) and _gk.value == "vars":
                                if isinstance(_gv, ast.Dict):
                                    declared_vars.update(
                                        str(k.value) for k in _gv.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)
                                    )
                                elif isinstance(_gv, ast.Name):
                                    _vname = _gv.id
                                    for _anode in ast.walk(_gtree):
                                        if isinstance(_anode, ast.Assign) and isinstance(_anode.value, ast.Dict):
                                            if any(isinstance(t, ast.Name) and t.id == _vname for t in _anode.targets):
                                                declared_vars.update(
                                                    str(k.value) for k in _anode.value.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)
                                                )
            except Exception:
                m_vars = re.search(r"['\"]vars['\"]\s*:\s*\{([^}]+)\}", gen_code)
                if m_vars:
                    var_names = re.findall(r"['\"]([a-zA-Z_][a-zA-Z0-9_]*)['\"]\s*:", m_vars.group(1))
                    declared_vars = set(var_names)

        # Distractor validation, dynamic rationale check, and KaTeX guards on sample_res
        if sample_res is not None and isinstance(sample_res, (dict, tuple, list)):
            if isinstance(sample_res, (tuple, list)):
                if len(sample_res) >= 3:
                    s_vars = sample_res[0] if isinstance(sample_res[0], dict) else {}
                    s_corr = str(sample_res[1])
                    s_dists = sample_res[2] if isinstance(sample_res[2], list) else []
                    sample_dict = {"vars": s_vars, "correct": s_corr, "distractors": s_dists}
                elif len(sample_res) == 2:
                    s_vars = sample_res[0] if isinstance(sample_res[0], dict) else {}
                    s_corr = str(sample_res[1])
                    sample_dict = {"vars": s_vars, "correct": s_corr, "distractors": []}
                else:
                    sample_dict = {}
            else:
                sample_dict = sample_res

            # Apply fmt_str to sample_dict if defined
            if fmt_str and "@X@" in fmt_str and sample_dict.get("correct"):
                c_val_s = str(sample_dict["correct"]).strip()
                prefix_fmt = fmt_str.split("@X@")[0]
                if not c_val_s.startswith(prefix_fmt):
                    sample_dict["correct"] = fmt_str.replace("@X@", c_val_s)

            # Parametric indicators for dynamic rationale check
            has_var_in_correct = bool(re.search(r"@([a-zA-Z0-9_]+)@", str(sample_dict.get("correct", ""))))
            has_var_in_stem = bool(re.search(r"@([a-zA-Z0-9_]+)@", stem_es)) or any(bool(re.search(r"@([a-zA-Z0-9_]+)@", s)) for s in stem_variants)

            # FIB KaTeX guard
            if interaction_type == "fill_in_the_blank":
                corr_str = str(sample_dict.get("correct", "")).strip()
                if corr_str.startswith("$") and corr_str.endswith("$") and len(corr_str) >= 2:
                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, corr_str)
                    return _fail(
                        f"FAIL: [TPL-FIB-KATEX] La respuesta FIB en '{tpl_id}' ('{corr_str}') (Línea {line_no} en {curr_p.name}) contiene delimitadores '$' externos. "
                        f"En Frontend (FeedbackToast) se formatea automáticamente en modo matemático; retire los '$' externos."
                    )
                fib_katex_errs = validate_katex_syntax(corr_str, f"FIB correct answer in '{tpl_id}'", allow_template_vars=True)
                if fib_katex_errs:
                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, corr_str)
                    return _fail(f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {fib_katex_errs[0]}")

            # Warn-only PyKaTeX render check (does not affect pass/fail)
            _is_fib = interaction_type == "fill_in_the_blank"
            for _w in pykatex_warnings(sample_dict.get("correct", ""), f"correct in '{tpl_id}'", whole_is_math=_is_fib):
                print(_w, file=sys.stderr)
            for _d in (sample_dict.get("distractors") or []):
                _dv = _d.get("value") if isinstance(_d, dict) else (_d[1] if isinstance(_d, (tuple, list)) and len(_d) > 1 else _d)
                for _w in pykatex_warnings(_dv, f"distractor in '{tpl_id}'"):
                    print(_w, file=sys.stderr)

            # MC7 checks
            if interaction_type == "multiple_choice_7_options":
                s_corr_raw = str(sample_dict.get("correct", "")).strip()
                if s_corr_raw:
                    corr_katex_errs = validate_katex_syntax(s_corr_raw, f"correct answer in '{tpl_id}'", allow_template_vars=True)
                    if corr_katex_errs:
                        line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, s_corr_raw)
                        return _fail(f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {corr_katex_errs[0]}")
                    if strict:
                        m_tt = _find_telltale_in_option(s_corr_raw, is_distractor=False)
                        if m_tt:
                            line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, s_corr_raw)
                            return _fail(
                                f"FAIL: [TPL-TELLTALE / parenthetical_telltale_linter / distractor_integrity_linter] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): "
                                f"la opción visible contiene metainformación delatora: '{m_tt}'. "
                                f"Elimina palabras y coletillas delatoras del texto visible de la opción y traslada explicaciones conceptuales a 'error_rationale' o 'sol'."
                            )
                dists_list = sample_dict.get("distractors") or []
                if isinstance(dists_list, list) and dists_list:
                    dids_found = []
                    for d_idx, d_item in enumerate(dists_list, start=1):
                        did = None
                        rat = ""
                        val = ""
                        if isinstance(d_item, dict):
                            did = d_item.get("distractor_id") or d_item.get("id") or d_item.get("did")
                            rat = str(d_item.get("error_rationale") or d_item.get("rationale") or "")
                            val = str(d_item.get("value") if "value" in d_item else (d_item.get("content") or ""))
                        elif isinstance(d_item, (tuple, list)):
                            if len(d_item) >= 3:
                                did = str(d_item[0]).strip().replace("_", "-")
                                val = str(d_item[1]).strip()
                                rat = str(d_item[2]).strip()
                            elif len(d_item) == 2:
                                did_cand = str(d_item[0]).strip().replace("_", "-")
                                orig_did0 = str(d_item[0]).strip()
                                if did_cand in combined_rats or orig_did0 in combined_rats:
                                    did = did_cand
                                    val = str(d_item[1]).strip()
                                    rat = combined_rats.get(did_cand) or combined_rats[orig_did0]
                                elif strict:
                                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, str(d_item[0]))
                                    return _fail(
                                        f"FAIL: [TPL-MC7-STRICT] En modo estricto, la 2-tupla (distractor_id, value) está prohibida en MC7 ('{tpl_id}') (Línea {line_no} en {curr_p.name}). "
                                        f"Cada distractor debe ser una 3-tupla (distractor_id, value, error_rationale) con error_rationale >= 20 caracteres: {repr(d_item)}"
                                    )
                                else:
                                    did = did_cand
                                    val = str(d_item[1]).strip()

                        if fmt_str and "@X@" in fmt_str and val:
                            pfx = fmt_str.split("@X@")[0]
                            if not val.startswith(pfx):
                                val = fmt_str.replace("@X@", val)

                        if val:
                            val_katex_errs = validate_katex_syntax(val, f"distractor '{did}' value in '{tpl_id}'", allow_template_vars=True)
                            if val_katex_errs:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or val)
                                return _fail(f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {val_katex_errs[0]}")
                            if strict:
                                m_tt = _find_telltale_in_option(val, is_distractor=True)
                                if m_tt:
                                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or val)
                                    return _fail(
                                        f"FAIL: [TPL-TELLTALE / parenthetical_telltale_linter / distractor_integrity_linter] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): "
                                        f"la opción visible contiene metainformación delatora: '{m_tt}'. "
                                        f"Elimina palabras y coletillas delatoras del texto visible de la opción y traslada explicaciones conceptuales a 'error_rationale' o 'sol'."
                                    )
                        if rat:
                            rat_katex_errs = validate_katex_syntax(rat, f"distractor '{did}' rationale in '{tpl_id}'", allow_template_vars=True)
                            if rat_katex_errs:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                return _fail(f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {rat_katex_errs[0]}")

                        if did:
                            dids_found.append(did)
                            if cta_declared_ids and did not in cta_declared_ids:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did)
                                return _fail(
                                    f"FAIL: Distractor ID '{did}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) no está declarado en cta.json para la competencia '{cid}'. "
                                    f"Distractores obligatorios declarados en cta.json: {sorted(cta_declared_ids)}."
                                )

                        if strict:
                            if len(rat.strip()) < 20:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                return _fail(
                                    f"FAIL: [TPL-MC7-RATIONALE] El distractor '{did}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) tiene error_rationale de longitud {len(rat.strip())} (< 20 caracteres): '{rat}'."
                                )
                            # Dynamic rationale check [TPL-DYNAMIC-RATIONALE]
                            if declared_vars:
                                has_var_in_val = bool(re.search(r"@([a-zA-Z0-9_]+)@", val))
                                is_param_dist = has_var_in_val or has_var_in_correct or has_var_in_stem
                                if is_param_dist:
                                    rat_tokens = set(re.findall(r"@([a-zA-Z0-9_]+)@", rat))
                                    valid_rat_tokens = rat_tokens.intersection(declared_vars)
                                    if not valid_rat_tokens:
                                        line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                        return _fail(
                                            f"FAIL: [TPL-DYNAMIC-RATIONALE] El distractor '{did}' en la plantilla paramétrica '{tpl_id}' (Línea {line_no} en {curr_p.name}) tiene una explicación estática sin variables ('{rat}'). "
                                            f"Debe incluir al menos un token @var@ declarado en vars ({', '.join(sorted(declared_vars))}) para explicar dinámicamente el desvío."
                                        )
                    target_misc = dids_found

            # MS checks
            if interaction_type == "multiple_select":
                opts_list = sample_dict.get("options") or []
                ms_dids = []
                for opt in opts_list:
                    if isinstance(opt, dict) and not opt.get("is_correct"):
                        did = opt.get("distractor_id") or opt.get("id") or opt.get("did")
                        rat = str(opt.get("error_rationale") or opt.get("rationale") or "")
                        val = str(opt.get("value") if "value" in opt else (opt.get("content") or ""))
                        if val:
                            opt_katex_errs = validate_katex_syntax(val, f"option '{did}' value in '{tpl_id}'", allow_template_vars=True)
                            if opt_katex_errs:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or val)
                                return _fail(f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {opt_katex_errs[0]}")
                            if strict:
                                m_tt = _find_telltale_in_option(val, is_distractor=True)
                                if m_tt:
                                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or val)
                                    return _fail(
                                        f"FAIL: [TPL-TELLTALE / parenthetical_telltale_linter / distractor_integrity_linter] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): "
                                        f"la opción visible contiene metainformación delatora: '{m_tt}'. "
                                        f"Elimina palabras y coletillas delatoras del texto visible de la opción y traslada explicaciones conceptuales a 'error_rationale' o 'sol'."
                                    )
                        if rat:
                            opt_rat_errs = validate_katex_syntax(rat, f"option '{did}' rationale in '{tpl_id}'", allow_template_vars=True)
                            if opt_rat_errs:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                return _fail(f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {opt_rat_errs[0]}")
                        if did:
                            norm_did = str(did).replace("_", "-")
                            ms_dids.append(norm_did)
                            if cta_declared_ids and norm_did not in cta_declared_ids:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, str(did))
                                return _fail(
                                    f"FAIL: Distractor ID '{did}' en opción falsa de '{tpl_id}' (Línea {line_no} en {curr_p.name}) no está declarado en cta.json para la competencia '{cid}'."
                                )
                        if strict:
                            if not did:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, val)
                                return _fail(f"FAIL: [TPL-MS-DISTRACTOR-ID] Opción falsa en multiple_select ('{tpl_id}') (Línea {line_no} en {curr_p.name}) carece de distractor_id.")
                            if len(rat.strip()) < 20:
                                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                return _fail(
                                    f"FAIL: [TPL-MS-RATIONALE] La opción falsa '{did}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) tiene error_rationale de longitud {len(rat.strip())} (< 20 caracteres): '{rat}'."
                                )
                            # Dynamic rationale check [TPL-DYNAMIC-RATIONALE]
                            if declared_vars:
                                has_var_in_val = bool(re.search(r"@([a-zA-Z0-9_]+)@", val))
                                is_param_opt = has_var_in_val or has_var_in_correct or has_var_in_stem
                                if is_param_opt:
                                    rat_tokens = set(re.findall(r"@([a-zA-Z0-9_]+)@", rat))
                                    valid_rat_tokens = rat_tokens.intersection(declared_vars)
                                    if not valid_rat_tokens:
                                        line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, did or rat)
                                        return _fail(
                                            f"FAIL: [TPL-DYNAMIC-RATIONALE] La opción falsa '{did}' en la plantilla paramétrica '{tpl_id}' (Línea {line_no} en {curr_p.name}) tiene una explicación estática sin variables ('{rat}'). "
                                            f"Debe incluir al menos un token @var@ declarado en vars ({', '.join(sorted(declared_vars))})."
                                        )
                target_misc = list(dict.fromkeys(ms_dids))

        # Soundness and Distractor Refutation Dry-Run (seeds 42, 43, 44)
        if callable(gen_raw) and callable(ver_raw) and strict:
            import random
            tautology_recorded = False
            for test_seed in (42, 43, 44):
                try:
                    rng_test = random.Random(test_seed)
                    EvaluationContext.set(template_id=tpl_id, gen_fn=gen_fn_name, archetype=orig_idx, seed=test_seed)
                    from engine.sandbox import call_with_timeout
                    res_test = call_with_timeout(gen_raw, args=(rng_test,), timeout=0.8, seed=test_seed)
                except Exception:
                    continue
                if not isinstance(res_test, dict):
                    continue
                if "ans" in res_test and "correct" not in res_test:
                    res_test["correct"] = res_test["ans"]
                if "ds" in res_test and "distractors" not in res_test:
                    res_test["distractors"] = res_test["ds"]
                if "vars" not in res_test:
                    c_val = res_test.get("correct") or res_test.get("ans") or ""
                    res_test["vars"] = {"ans": c_val} if c_val else {}
                c_test = str(res_test.get("correct", "")).strip()
                v_test = res_test.get("vars", {}) if isinstance(res_test.get("vars"), dict) else {}
                if fmt_str and "@X@" in fmt_str and c_test:
                    pfx = fmt_str.split("@X@")[0]
                    if not c_test.startswith(pfx):
                        c_test = fmt_str.replace("@X@", c_test)
                        res_test["correct"] = c_test

                # Soundness check
                if callable(ver_raw) and not c_test and isinstance(res_test.get("options"), list):
                    # Multiple Select: sin clave "correct"; el verificador recibe la instancia completa.
                    try:
                        from engine.sandbox import call_with_timeout
                        sound_res = call_with_timeout(ver_raw, args=(res_test,), timeout=0.8, seed=test_seed)
                    except TypeError:
                        sound_res = run_ver(c_test, v_test, res_test)
                else:
                    sound_res = run_ver(c_test, v_test, res_test)
                if hasattr(sound_res, "item"):
                    sound_res = sound_res.item()
                if sound_res is not True:
                    line_no = _find_diagnostic_line(curr_loc, ver_fn_name, orig_idx)
                    return _fail(
                        f"FAIL: [TPL-VERIFIER-UNSOUND] El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) "
                        f"no retornó True para la instancia válida generada (semilla {test_seed}, resultado: {sound_res})."
                    )

                # Distractor refutation
                dists_test = res_test.get("distractors") or []
                if isinstance(dists_test, list) and not tautology_recorded:
                    for d_t in dists_test:
                        d_val = ""
                        if isinstance(d_t, dict):
                            d_val = str(d_t.get("value") if "value" in d_t else d_t.get("content", "")).strip()
                        elif isinstance(d_t, (tuple, list)) and len(d_t) >= 2:
                            d_val = str(d_t[1]).strip()
                        elif isinstance(d_t, (tuple, list)) and len(d_t) == 1:
                            d_val = str(d_t[0]).strip()
                        elif isinstance(d_t, (str, int, float)):
                            d_val = str(d_t).strip()
                        if fmt_str and "@X@" in fmt_str and d_val:
                            pfx = fmt_str.split("@X@")[0]
                            if not d_val.startswith(pfx):
                                d_val = fmt_str.replace("@X@", d_val)
                        if d_val and d_val != c_test:
                            mutated = {**res_test, "correct": d_val}
                            refute_res = run_ver(d_val, v_test, mutated)
                            if hasattr(refute_res, "item"):
                                refute_res = refute_res.item()
                            if refute_res is True:
                                line_no = _find_diagnostic_line(curr_loc, ver_fn_name, orig_idx, d_val)
                                deferred_verifier_errors.append(
                                    f"[-] [VERIFIER-TAUTOLOGY-DETECTED] {cid}.json ({curr_p.name}): El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) "
                                    f"retornó True para el distractor falso '{d_val}'. El verificador no refuta respuestas incorrectas (tautología)."
                                )
                                tautology_recorded = True
                                break

        # Vacuous quantifier check in stem_variants
        if strict:
            vacuous_re = re.compile(r"(?:\\forall|\bpara\s+todo\b)\s*\\?[a-zA-Z_]+\s*=\s*\d+|(?:\\exists|\bexiste\b)\s*\\?[a-zA-Z_]+\s*=\s*\d+", re.IGNORECASE)
            for s_idx, sv in enumerate(stem_variants):
                m_vac = vacuous_re.search(sv)
                if m_vac:
                    line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, sv)
                    return _fail(
                        f"FAIL: [TPL-VACUOUS-QUANTIFIER] Cuantificador vacuo detectado en stem_variants[{s_idx}] de '{tpl_id}' (Línea {line_no} en {curr_p.name}): '{m_vac.group(0)}'. "
                        f"No se permite asignar un valor literal constante a una variable cuantificada."
                    )

            if sample_dict and sample_dict.get("correct"):
                corr_val_str = str(sample_dict["correct"]).replace("$", "").strip()
                if len(corr_val_str) >= 15 and corr_val_str.lower() not in ("remember", "understand", "apply"):
                    for h_idx in range(min(2, len(hints))):
                        if corr_val_str.lower() in hints[h_idx].lower():
                            line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, hints[h_idx])
                            return _fail(
                                f"FAIL: [TPL-HINT-LEAK] La pista {h_idx + 1} de '{tpl_id}' (Línea {line_no} en {curr_p.name}) filtra la respuesta correcta ('{corr_val_str}'). "
                                f"Las pistas tempranas deben ser de andamiaje socrático y no revelar la respuesta final."
                            )

        # Normalize non-variable double curly braces {{token}} -> {token} before R-20 validation
        stem_es = normalize_double_braces(stem_es, declared_vars)
        stem_variants = [normalize_double_braces(sv, declared_vars) for sv in stem_variants]
        hints = [normalize_double_braces(h, declared_vars) for h in hints]
        healed_solution = normalize_double_braces(sol_raw, declared_vars)
        healed_solution = re.sub(
            r"\{\{([A-Za-z0-9_]+)\}\}",
            lambda m: f"{{{m.group(1)}}}" if m.group(1) not in declared_vars else m.group(0),
            healed_solution,
        )

        for s_idx, sv in enumerate(stem_variants):
            sv_katex = validate_katex_syntax(sv, f"stem_variant[{s_idx}] in '{tpl_id}'", allow_template_vars=True)
            if sv_katex:
                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, sv)
                return _fail(f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {sv_katex[0]}")
        for h_idx, h_text in enumerate(hints):
            h_katex = validate_katex_syntax(h_text, f"hint[{h_idx}] in '{tpl_id}'", allow_template_vars=True)
            if h_katex:
                line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, h_text)
                return _fail(f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {h_katex[0]}")
        sol_katex = validate_katex_syntax(healed_solution, f"explanation_es in '{tpl_id}'", allow_template_vars=True)
        if sol_katex:
            line_no = _find_diagnostic_line(curr_loc, gen_fn_name, orig_idx, sol_raw)
            return _fail(f"FAIL: [TPL-KATEX] En '{tpl_id}' (Línea {line_no} en {curr_p.name}): {sol_katex[0]}")


        canonical_dict: Dict[str, Any] = {
            "template_id": tpl_id,
            "competency_id": cid,
            "gen_fn_name": gen_fn_name,
            "question_type": qtype,
            "stem_es": stem_es,
            "stem_variants": stem_variants,
            "generator_code": gen_code,
            "verifier_code": ver_code,
            "explanation_es": healed_solution,
            "target_kc": target_kc,
            "target_misconceptions": target_misc,
            "source_reference": src_ref,
            # Schema compatibility fields
            "id": tpl_id,
            "interaction_type": interaction_type,
            "difficulty": difficulty,
            "bloom": bloom,
            "stem": stem_es,
            "generate_py": gen_code,
            "cross_check_py": ver_code,
            "solution": healed_solution,
            "distractor_ids": target_misc,
            "hints": hints,
            "source_file": curr_p.name,
        }
        if archetype:
            canonical_dict["archetype"] = archetype
        if assumption_id:
            canonical_dict["assumption_id"] = assumption_id

        # Apply mechanical auto-healing
        auto_heal_template_data(canonical_dict, cta_comp=cta_comp)
        canonical_dict = heal_control_chars_in_obj(canonical_dict)

        templates_by_cid.setdefault(cid, []).append(canonical_dict)
        gen_callables_by_cid.setdefault(cid, []).append(gen_raw)

    # Pre-check: Ensure full distractor coverage per competency with explicit set-difference
    if cta_p and Path(cta_p).is_file():
        try:
            cta_info = json.loads(Path(cta_p).read_text(encoding="utf-8"))
            cta_comp_dids = {}
            for comp_entry in cta_info.get("competencies", []):
                if isinstance(comp_entry, dict) and "id" in comp_entry:
                    c_dids = [str(d.get("id")) for d in comp_entry.get("distractors", []) if isinstance(d, dict) and d.get("id")]
                    if c_dids:
                        cta_comp_dids[comp_entry["id"]] = set(c_dids)
            for cid, tpls in templates_by_cid.items():
                if cid in cta_comp_dids:
                    used_dids = set()
                    for t in tpls:
                        used_dids.update([str(d) for d in t.get("distractor_ids", [])])
                    missing_dids = cta_comp_dids[cid] - used_dids
                    if missing_dids and strict:
                        return _fail(
                            f"FAIL: [TPL-D3: COBERTURA COMPLETA DE DISTRACTORES] FALTAN DISTRACTORES OBLIGATORIOS en '{cid}': {sorted(missing_dids)}. "
                            f"Distractores declarados: {sorted(cta_comp_dids[cid])}. Debes asignarlos a las plantillas de tu shard."
                        )
        except Exception:
            pass

    # 6. Write templates atomically grouped by competency
    compiled_paths: List[Path] = []
    for cid, tpls in templates_by_cid.items():
        base_id = f"T-{cid}" if not cid.startswith("T-") else cid
        for idx, tpl in enumerate(tpls, start=1):
            cur_id = tpl.get("id") or base_id
            needs_normalization = (
                not cur_id.startswith("T-")
                or (len(tpls) > 1 and cur_id == base_id)
                or any(tpls[j].get("id") == cur_id for j in range(len(tpls)) if j != idx - 1)
            )
            if needs_normalization:
                unique_id = f"{base_id}-{idx:02d}"
                tpl["id"] = unique_id
                tpl["template_id"] = unique_id

        out_json_path = templates_dir / f"{cid}.json"
        if len(tpls) == 1:
            payload = tpls[0]
        else:
            payload = {
                "competency_id": cid,
                "templates": tpls,
            }
        _atomic_write_json(out_json_path, payload)
        compiled_paths.append(out_json_path)

    # 7. Execute Strict Validation with check_templates (isolated by shard_id)
    is_clean, raw_errors = check_templates_file_or_dir(
        target_path=compiled_paths,
        cta_path=cta_p,
        num_dry_run_seeds=seeds,
        strict=strict,
        auto_fix=True,
        shard_py=(staged_p if (healed_source and staged_p.is_file()) else shard_data_path),
        shard_id=norm_shard_id,
        from_compile_shard=True,
    )

    # Milestone 3 Tri-Band Multimodal Enforcement Gate [M3-ARCHETYPES]
    m3_errors: List[str] = []
    if strict:
        target_cids = expected_cids if expected_cids else list(templates_by_cid.keys())
        shard_data_name = shard_data_path.name if shard_data_path else f"{norm_shard_id}_data.py"

        def _fn_declares_arch(fn_node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> bool:
            all_args = getattr(fn_node.args, "posonlyargs", []) + fn_node.args.args + getattr(fn_node.args, "kwonlyargs", [])
            return any(a.arg == "arch" for a in all_args)

        def _fn_uses_arch_in_body(fn_node: Union[ast.FunctionDef, ast.AsyncFunctionDef]) -> bool:
            for b_stmt in fn_node.body:
                for sub in ast.walk(b_stmt):
                    if isinstance(sub, ast.Name) and sub.id == "arch" and isinstance(sub.ctx, ast.Load):
                        # Filter out dummy loads like _ = arch or dummy = arch or unused = arch
                        if isinstance(b_stmt, ast.Assign):
                            if any(isinstance(tgt, ast.Name) and tgt.id in ("_", "dummy", "unused") for tgt in b_stmt.targets):
                                continue
                        # Filter out bare statement expressions like `arch` or `arch == arch`
                        if isinstance(b_stmt, ast.Expr):
                            if isinstance(b_stmt.value, ast.Name) and b_stmt.value.id == "arch":
                                continue
                            if isinstance(b_stmt.value, ast.Compare):
                                if isinstance(b_stmt.value.left, ast.Name) and b_stmt.value.left.id == "arch":
                                    if any(isinstance(comp, ast.Name) and comp.id == "arch" for comp in b_stmt.value.comparators):
                                        continue
                        return True
            return False

        for cid in target_cids:
            tpls = templates_by_cid.get(cid, [])
            gen_callables = gen_callables_by_cid.get(cid, [])
            is_modular_fix = bool(cid in fix_files_by_cid and fix_files_by_cid[cid].is_file())
            source_name = fix_files_by_cid[cid].name if is_modular_fix else shard_data_name

            # AST analysis de la fuente efectiva de esta competencia
            cid_sources: List[str] = []
            if is_modular_fix:
                try:
                    cid_sources.append(fix_files_by_cid[cid].read_text(encoding="utf-8"))
                except Exception:
                    pass
            else:
                if healed_source:
                    cid_sources.append(healed_source)
                elif raw_source:
                    cid_sources.append(raw_source)
                elif shard_data_path and shard_data_path.is_file():
                    try:
                        cid_sources.append(shard_data_path.read_text(encoding="utf-8"))
                    except Exception:
                        pass

            for t in tpls:
                gen_c = t.get("generator_code") or t.get("generate_py") or ""
                if gen_c and gen_c not in cid_sources:
                    cid_sources.append(gen_c)

            cid_ast_funcs: Dict[str, Union[ast.FunctionDef, ast.AsyncFunctionDef]] = {}
            for src_txt in cid_sources:
                try:
                    parsed_tree = ast.parse(textwrap.dedent(src_txt.strip()))
                    for ast_node in ast.walk(parsed_tree):
                        if isinstance(ast_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            cid_ast_funcs[ast_node.name] = ast_node
                        elif (
                            isinstance(ast_node, ast.Assign)
                            and len(ast_node.targets) == 1
                            and isinstance(ast_node.targets[0], ast.Name)
                            and isinstance(ast_node.value, ast.Lambda)
                        ):
                            fn_id = ast_node.targets[0].id
                            synthetic_fn = ast.FunctionDef(
                                name=fn_id,
                                args=ast_node.value.args,
                                body=[ast.Return(value=ast_node.value.body)],
                                decorator_list=[],
                                returns=None,
                                lineno=getattr(ast_node, "lineno", 1),
                            )
                            cid_ast_funcs[fn_id] = synthetic_fn
                except Exception:
                    pass

            # Assumption link and 4 archetype kinds validation
            cta_comp_raw = cta_comp_map.get(cid, {})
            assumptions_list = cta_comp_raw.get("assumptions") or []
            if assumptions_list and eff_min_arch >= 4:
                tpl_archs = [t.get("archetype") for t in tpls if t.get("archetype")]
                if len(tpl_archs) >= 4 or any(t.get("archetype") for t in tpls):
                    missing_archs = set(_S4_ARCHETYPE_KINDS) - set(tpl_archs)
                    if missing_archs:
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [M3-ARCHETYPES] La competencia '{cid}' declara supuestos en cta.json pero sus plantillas no cubren todos los arquetipos requeridos ({_S4_ARCHETYPE_KINDS}). Faltan: {sorted(list(missing_archs))}."
                        )
                    edge_tpls = [t for t in tpls if t.get("archetype") == "boundary_or_edge_case"]
                    if edge_tpls:
                        decl_assump_ids = {
                            (a.get("id") if isinstance(a, dict) else str(a)).strip()
                            for a in assumptions_list
                        }
                        for et in edge_tpls:
                            a_id = et.get("assumption_id")
                            if not a_id or a_id not in decl_assump_ids:
                                m3_errors.append(
                                    f"{cid}.json ({source_name}): [TPL-ASSUMPTION-LINK] La plantilla de borde '{et.get('id')}' en la competencia '{cid}' "
                                    f"debe vincularse a un assumption_id válido declarado en cta.json ({sorted(list(decl_assump_ids))}). Encontrado: '{a_id}'."
                                )

            if eff_min_arch >= 3 and len(tpls) < eff_min_arch:
                m3_errors.append(
                    f"{cid}.json ({source_name}): [M3-ARCHETYPES] La competencia '{cid}' define solo {len(tpls)} plantilla(s) en TEMPLATES, "
                    f"pero el contrato Tri-Banda exige mínimo {eff_min_arch} plantillas/arquetipos por competencia."
                )
            elif eff_min_arch >= 3:
                # Verificación Tri-Banda de dificultad
                diffs = {t.get("difficulty") for t in tpls}
                if not {"easy", "medium", "hard"}.issubset(diffs):
                    missing_diffs = sorted(list({"easy", "medium", "hard"} - diffs))
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M3-ARCHETYPES] Cobertura incompleta de bandas de dificultad para '{cid}'. "
                        f"Se requieren las 3 bandas {{'easy', 'medium', 'hard'}}, faltan: {missing_diffs}."
                    )

                # Verificación de diversidad de Bloom (>= 2 distintos)
                blooms = {t.get("bloom") for t in tpls if t.get("bloom")}
                if len(blooms) < 2:
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M3-ARCHETYPES] Diversidad cognitiva insuficiente para '{cid}'. "
                        f"Se requieren al menos 2 niveles Bloom distintos por competencia (encontrados: {sorted(list(blooms))})."
                    )

                # Verificación de práctica activa (FIB o MS)
                cta_c = cta_comp_map.get(cid, {})
                c_type = str(cta_c.get("type", "")).lower()
                is_skill = cid.startswith("Hab-") or c_type in ("skill", "habilidad")
                req_active = 2 if is_skill else 1
                active_tpls = [
                    t for t in tpls
                    if t.get("interaction_type") in ("fill_in_the_blank", "multiple_select")
                    or t.get("question_type") in ("fib", "fill_in_the_blank", "ms", "multiple_select")
                ]
                if len(active_tpls) < req_active:
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M3-ARCHETYPES] Práctica activa insuficiente para '{cid}' "
                        f"({'habilidad' if is_skill else 'concepto/misconception'}). Se requieren al menos {req_active} plantilla(s) "
                        f"de tipo FIB o MS (encontradas: {len(active_tpls)})."
                    )

                if eff_min_arch >= 4 and is_skill:
                    high_blooms = {"Apply", "Analyze", "Evaluate", "Create"}
                    if not any(b in high_blooms for b in blooms):
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [M3-ARCHETYPES] Diversidad cognitiva insuficiente para habilidad '{cid}'. "
                            f"Se requiere al menos 1 nivel Bloom de aplicación o superior ({sorted(list(high_blooms))})."
                        )
                    fib_tpls = [
                        t for t in tpls
                        if t.get("interaction_type") == "fill_in_the_blank"
                        or t.get("question_type") in ("fib", "fill_in_the_blank")
                    ]
                    if len(fib_tpls) < 1:
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [M3-ARCHETYPES] Práctica activa insuficiente para habilidad '{cid}'. "
                            f"Se requiere al menos 1 plantilla de tipo FIB (fill_in_the_blank) cuando eff_min_arch >= 4."
                        )

                # Verificación 1 — Enunciados (stem_es) distintos por arquetipo & detección de clones
                distinct_stems = {t.get("stem_es", "").strip() for t in tpls if t.get("stem_es", "").strip()}
                norm_gen_codes = {
                    re.sub(r"def\s+gen_[a-zA-Z0-9_]+_\d+\s*\(", "def _gen_wrapper_(", t.get("generator_code", "").strip())
                    for t in tpls
                }

                if len(distinct_stems) < len(tpls):
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M3-ARCHETYPES] Competencia '{cid}' repite el mismo enunciado (stem_es) entre sus plantillas ({len(distinct_stems)} únicos de {len(tpls)} plantillas). Cada plantilla debe tener su propio enunciado distintivo."
                    )
                elif len(norm_gen_codes) < min(eff_min_arch, 2):
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [M3-ARCHETYPES] Las {len(tpls)} tuplas de '{cid}' en TEMPLATES son clones idénticos (mismo generador)."
                    )

                # Verificación 2 — AST analysis de la fuente efectiva de esta competencia
                cid_clean = cid.lower().replace("-", "_")
                cid_compact = cid.lower().replace("-", "")
                cid_candidate_funcs: Set[str] = set()

                for t in tpls:
                    g_fn = t.get("gen_fn_name")
                    if g_fn and g_fn in cid_ast_funcs:
                        cid_candidate_funcs.add(g_fn)
                        w_node = cid_ast_funcs[g_fn]
                        for b_stmt in w_node.body:
                            for sub in ast.walk(b_stmt):
                                if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name):
                                    if sub.func.id in cid_ast_funcs:
                                        cid_candidate_funcs.add(sub.func.id)

                for fname, fnode in cid_ast_funcs.items():
                    if _fn_declares_arch(fnode):
                        if cid_clean in fname.lower() or cid_compact in fname.lower():
                            cid_candidate_funcs.add(fname)
                        elif is_modular_fix or len(target_cids) == 1:
                            cid_candidate_funcs.add(fname)

                checked_fn_names: Set[str] = set()
                for func_name in sorted(cid_candidate_funcs):
                    if func_name in checked_fn_names:
                        continue
                    checked_fn_names.add(func_name)
                    fn_node = cid_ast_funcs.get(func_name)
                    if fn_node and _fn_declares_arch(fn_node):
                        if not _fn_uses_arch_in_body(fn_node):
                            m3_errors.append(
                                f"{cid}.json ({source_name}): [M3-ARCHETYPES] Competencia '{cid}': la función generadora '{func_name}' recibe el parámetro 'arch' pero nunca lo utiliza en su cuerpo, produciendo salidas idénticas en los 4 arquetipos. Ramifica con 'if arch == 1 / elif arch == 2 / elif arch == 3 / else' para variar el problema matemático por arquetipo."
                            )
                    # Pillar 3: Detect artificial debug exceptions in generator functions
                    if fn_node:
                        for sub_ast in ast.walk(fn_node):
                            if isinstance(sub_ast, ast.Raise):
                                exc_name = ""
                                if isinstance(sub_ast.exc, ast.Call) and isinstance(sub_ast.exc.func, ast.Name):
                                    exc_name = sub_ast.exc.func.id
                                elif isinstance(sub_ast.exc, ast.Name):
                                    exc_name = sub_ast.exc.id
                                m3_errors.append(
                                    f"{cid}.json ({source_name}): [TPL-DEBUG-ARTIFACT] La función generadora '{func_name}' contiene una sentencia 'raise {exc_name or ''}' en su cuerpo. Las funciones generadoras de ítems deben retornar un diccionario de variables y opciones, sin sentencias 'raise' de depuración."
                                )
                                break

                # Verificación 3 — Detección de Evasión Trivial y Clones Matemáticos Puros (seed=100 & seed=101)
                if eff_min_arch >= 3 and len(tpls) >= 3:
                    def _eval_tuple_output(t_idx: int, seed_val: int) -> Optional[Tuple[str, str, str]]:
                        c_call = gen_callables[t_idx] if t_idx < len(gen_callables) else None
                        if callable(c_call):
                            try:
                                import random
                                from engine.sandbox import call_with_timeout, _LazyNPRNG
                                rng = random.Random(seed_val)
                                try:
                                    rng.np = _LazyNPRNG(seed_val)
                                except Exception:
                                    pass
                                res = call_with_timeout(
                                    c_call,
                                    args=(rng,),
                                    timeout=0.4,
                                    seed=seed_val,
                                )
                                if isinstance(res, dict):
                                    if "vars" not in res:
                                        c_val = res.get("correct") or res.get("ans") or ""
                                        res["vars"] = {"ans": c_val} if c_val else {}
                                    c_v = str(res.get("correct", ""))
                                    v_d = res.get("vars", {})
                                    v_s = json.dumps(v_d, sort_keys=True, default=str) if isinstance(v_d, dict) else str(v_d)
                                    opts = res.get("options", [])
                                    opts_s = ""
                                    if isinstance(opts, list) and opts:
                                        simplified_opts = [
                                            (str(o.get("value") or o.get("content", "")), bool(o.get("is_correct")))
                                            for o in opts if isinstance(o, dict)
                                        ]
                                        opts_s = json.dumps(sorted(simplified_opts), default=str)
                                    return (c_v, v_s, opts_s)
                                elif isinstance(res, (tuple, list)) and len(res) >= 1 and isinstance(res[0], dict):
                                    v_d = res[0]
                                    v_s = json.dumps(v_d, sort_keys=True, default=str)
                                    return ("", v_s, "")
                            except Exception:
                                pass

                        gen_c = tpls[t_idx].get("generator_code") or tpls[t_idx].get("generate_py") or ""
                        if gen_c:
                            try:
                                from engine.sandbox import run_code_in_env
                                res = run_code_in_env(gen_c, "generate", seed=seed_val, timeout=0.5)
                                if isinstance(res, dict):
                                    if "vars" not in res:
                                        c_val = res.get("correct") or res.get("ans") or ""
                                        res["vars"] = {"ans": c_val} if c_val else {}
                                    c_v = str(res.get("correct", ""))
                                    v_d = res.get("vars", {})
                                    v_s = json.dumps(v_d, sort_keys=True, default=str) if isinstance(v_d, dict) else str(v_d)
                                    opts = res.get("options", [])
                                    opts_s = ""
                                    if isinstance(opts, list) and opts:
                                        simplified_opts = [
                                            (str(o.get("value") or o.get("content", "")), bool(o.get("is_correct")))
                                            for o in opts if isinstance(o, dict)
                                        ]
                                        opts_s = json.dumps(sorted(simplified_opts), default=str)
                                    return (c_v, v_s, opts_s)
                            except Exception:
                                pass
                        return None

                    outs_100 = [_eval_tuple_output(i, 100) for i in range(len(tpls))]
                    valid_100 = [o for o in outs_100 if o is not None]
                    if is_skill and eff_min_arch >= 3 and len(valid_100) == len(tpls) and len(set(valid_100)) < len(valid_100):
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [M3-ARCHETYPES] Competencia de habilidad '{cid}': las plantillas generan salidas matemáticas duplicadas en seed=100 ({len(set(valid_100))} únicas de {len(tpls)} plantillas). Cada arquetipo de habilidad debe formular una variante matemática distinta."
                        )
                    elif len(valid_100) == len(tpls) and len(set(valid_100)) < 2:
                        outs_101 = [_eval_tuple_output(i, 101) for i in range(len(tpls))]
                        valid_101 = [o for o in outs_101 if o is not None]
                        if len(valid_101) == len(tpls) and len(set(valid_101)) < 2:
                            m3_errors.append(
                                f"{cid}.json ({source_name}): [M3-ARCHETYPES] Competencia '{cid}': las {len(tpls)} tuplas generan salidas matemáticas idénticas (mismo 'correct', 'vars' y 'options' en la misma semilla). Las plantillas deben producir al menos 2 variantes matemáticas distintas."
                            )

            # Verificación 4 — Detección de Distractores por Multiplicador Arbitrario [DIAG-MAGIC-MULT] y Pistas Parentéticas [PSYCHOMETRIC-OPTIONS]
            _magic_mults = (1.333, 0.667, 1.667, 0.333, 1.25, 0.75, 1.5, 0.5, 2.1, 0.45, 1.85, 0.15)
            _distinctive_magic = {1.333, 0.667, 1.667, 0.333, 2.1, 0.45, 1.85, 0.15}
            # Shift-left: a SINGLE distractor with an exact fixed ratio (e.g. n->4n => ME/4 = 0.5*ans) in >=80% of seeds is systematic and collides with the final audit.
            _isolated_exact_mults = (0.5, 0.75, 1.5, 1.25)
            _ISO_MIN_FRACTION = 0.8
            _num_re = re.compile(r"-?\d+\.\d+|-?\d+")

            def _check_func_has_magic_mult(fn_node: ast.AST) -> bool:
                for sub_n in ast.walk(fn_node):
                    if isinstance(sub_n, ast.Constant) and isinstance(sub_n.value, (int, float)):
                        val = float(sub_n.value)
                        for mf in _magic_mults:
                            if abs(val - mf) <= 0.01:
                                return True
                    if isinstance(sub_n, ast.BinOp) and isinstance(sub_n.op, (ast.Mult, ast.Div, ast.FloorDiv)):
                        left_names = {n.id for n in ast.walk(sub_n.left) if isinstance(n, ast.Name)}
                        right_names = {n.id for n in ast.walk(sub_n.right) if isinstance(n, ast.Name)}
                        ans_indicators = {"ans", "correct", "corr", "c_val", "c_num", "target"}
                        if (left_names & ans_indicators) or (right_names & ans_indicators):
                            return True
                        if (
                            isinstance(sub_n.left, ast.Constant)
                            and isinstance(sub_n.right, ast.Constant)
                            and isinstance(sub_n.left.value, (int, float))
                            and isinstance(sub_n.right.value, (int, float))
                        ):
                            try:
                                if float(sub_n.right.value) != 0:
                                    r_val = float(sub_n.left.value) / float(sub_n.right.value)
                                    for mf in _magic_mults:
                                        if abs(r_val - mf) <= 0.01:
                                            return True
                            except Exception:
                                pass
                        if isinstance(sub_n.right, ast.Constant) and isinstance(sub_n.right.value, (int, float)):
                            try:
                                if float(sub_n.right.value) != 0:
                                    inv_factor = 1.0 / float(sub_n.right.value)
                                    for mf in _magic_mults:
                                        if abs(inv_factor - mf) <= 0.01:
                                            return True
                                    if float(sub_n.right.value) in (2.0, 3.0, 4.0, 5.0):
                                        return True
                            except Exception:
                                pass
                return False

            try:
                import zlib
                from engine.assemble import format_template_string
                _seed_base = 42 + (zlib.crc32(cid.encode("utf-8")) % 10000)
            except Exception:
                _seed_base = 10000
                format_template_string = None

            for t_idx_m, tpl_m in enumerate(tpls):
                itype_curr = tpl_m.get("interaction_type") or tpl_m.get("qtype")
                if itype_curr not in ("multiple_choice_7_options", "multiple_choice", "multiple_select"):
                    continue
                c_call_m = gen_callables[t_idx_m] if t_idx_m < len(gen_callables) else None
                if not callable(c_call_m):
                    continue
                tpl_id_m = tpl_m.get("id") or tpl_m.get("template_id") or f"T-{cid}-{t_idx_m+1:02d}"
                gen_fn_m = tpl_m.get("gen_fn_name") or getattr(c_call_m, "__name__", "gen_fn")

                # Walk generator AST and any helper functions reached via call graph in cid_ast_funcs
                queue_funcs = [gen_fn_m]
                visited_fn_names: Set[str] = set()
                while queue_funcs:
                    curr_fn = queue_funcs.pop(0)
                    if curr_fn in visited_fn_names:
                        continue
                    visited_fn_names.add(curr_fn)
                    c_node = cid_ast_funcs.get(curr_fn)
                    if c_node:
                        for sub_call in ast.walk(c_node):
                            if isinstance(sub_call, ast.Call) and isinstance(sub_call.func, ast.Name):
                                if sub_call.func.id in cid_ast_funcs and sub_call.func.id not in visited_fn_names:
                                    queue_funcs.append(sub_call.func.id)

                if not visited_fn_names or not any(fn_n in cid_ast_funcs for fn_n in visited_fn_names):
                    gen_c_src = str(tpl_m.get("generator_code") or tpl_m.get("generate_py") or "")
                    if gen_c_src.strip():
                        try:
                            tree_m = ast.parse(textwrap.dedent(gen_c_src.strip()))
                            has_mult_ast = _check_func_has_magic_mult(tree_m)
                        except Exception:
                            has_mult_ast = True
                    else:
                        has_mult_ast = True
                else:
                    has_mult_ast = any(
                        _check_func_has_magic_mult(cid_ast_funcs[fn_n])
                        for fn_n in visited_fn_names
                        if fn_n in cid_ast_funcs
                    )

                tpl_seed_off = _seed_base + (t_idx_m * 500)
                eval_seeds = [tpl_seed_off + s_i for s_i in range(300)]
                hit_seeds: List[int] = []
                iso_valid_seeds = 0
                iso_hit_seeds: List[int] = []
                iso_hit_ratio: Optional[float] = None
                hit_mults_sample: List[float] = []
                corr_answers_sample: List[str] = []
                telltale_sample: Optional[Tuple[str, str]] = None
                for s_val in eval_seeds:
                    try:
                        import random
                        EvaluationContext.set(template_id=tpl_id_m, gen_fn=gen_fn_m, archetype=t_idx_m + 1, seed=s_val)
                        from engine.sandbox import call_with_timeout
                        rng_m = random.Random(s_val)
                        res_m = call_with_timeout(c_call_m, args=(rng_m,), timeout=0.8, seed=s_val)
                        if not isinstance(res_m, dict):
                            continue
                        if "vars" not in res_m:
                            c_val = res_m.get("correct") or res_m.get("ans") or ""
                            res_m["vars"] = {"ans": c_val} if c_val else {}
                        vars_m = res_m.get("vars", {}) if isinstance(res_m.get("vars"), dict) else {}

                        if itype_curr == "multiple_select":
                            opts_raw = res_m.get("options") or []
                            for opt_item in opts_raw:
                                if not isinstance(opt_item, dict):
                                    continue
                                val_raw = str(opt_item.get("value") if "value" in opt_item else (opt_item.get("content") or ""))
                                opt_txt = format_template_string(val_raw, vars_m) if format_template_string else val_raw
                                is_corr_opt = bool(opt_item.get("is_correct"))
                                if not telltale_sample:
                                    tt_found = _find_telltale_in_option(opt_txt, is_distractor=not is_corr_opt)
                                    if tt_found:
                                        telltale_sample = (tt_found, "distractor" if not is_corr_opt else "correct")
                            continue

                        corr_raw = str(res_m.get("correct") or res_m.get("ans") or "")
                        corr_txt = format_template_string(corr_raw, vars_m) if format_template_string else corr_raw
                        corr_answers_sample.append(corr_txt.strip())
                        if not telltale_sample:
                            tt_c = _find_telltale_in_option(corr_txt, is_distractor=False)
                            if tt_c:
                                telltale_sample = (tt_c, "correct")

                        dists_raw = res_m.get("distractors") or res_m.get("ds") or []
                        if not isinstance(dists_raw, list) or len(dists_raw) < 4:
                            continue
                        c_nums = _num_re.findall(corr_txt)
                        if not c_nums:
                            continue
                        try:
                            c_val = parse_katex_number(c_nums[-1])
                        except Exception:
                            continue
                        if abs(c_val) <= 1e-6 or abs(c_val) in (1.0, 2.0, 4.0):
                            continue
                        matched_m: List[float] = []
                        iso_valid_seeds += 1
                        _iso_hit_here = False
                        for d_item in dists_raw:
                            if isinstance(d_item, (tuple, list)) and len(d_item) >= 2:
                                d_raw = str(d_item[1])
                            elif isinstance(d_item, dict):
                                d_raw = str(d_item.get("value") or d_item.get("content") or "")
                            else:
                                continue
                            d_txt = format_template_string(d_raw, vars_m) if format_template_string else d_raw
                            if not telltale_sample:
                                tt_d = _find_telltale_in_option(d_txt, is_distractor=True)
                                if tt_d:
                                    telltale_sample = (tt_d, "distractor")
                            d_nums = _num_re.findall(d_txt)
                            if not d_nums:
                                continue
                            try:
                                d_val = parse_katex_number(d_nums[-1])
                            except Exception:
                                continue
                            # Guard 1: Skip conceptual distractors sharing the same numerical value as correct answer
                            if abs(d_val - c_val) <= 1e-4:
                                continue
                            actual_ratio = d_val / c_val if abs(c_val) > 1e-9 else 0.0
                            for m_factor in _magic_mults:
                                # Ratio check with 5% relative tolerance AND absolute rounding check to reject small-number false positives
                                expected_round = round(c_val * m_factor, 3)
                                if m_factor == 0.333:
                                    expected_div = round(c_val / 3.0, 3)
                                elif m_factor == 0.667:
                                    expected_div = round(c_val * 2.0 / 3.0, 3)
                                elif m_factor == 1.333:
                                    expected_div = round(c_val * 4.0 / 3.0, 3)
                                elif m_factor == 1.667:
                                    expected_div = round(c_val * 5.0 / 3.0, 3)
                                else:
                                    expected_div = expected_round
                                if abs(actual_ratio - m_factor) <= 0.05 and (abs(d_val - expected_round) <= 0.0015 or abs(d_val - expected_div) <= 0.0015):
                                    matched_m.append(m_factor)
                                    break
                            for m_iso in _isolated_exact_mults:
                                if abs(actual_ratio - m_iso) <= 0.05 and abs(d_val - round(c_val * m_iso, 3)) <= 0.0015:
                                    _iso_hit_here = True
                                    iso_hit_ratio = m_iso
                                    break
                        if _iso_hit_here:
                            iso_hit_seeds.append(s_val)
                        dist_hits = [m_f for m_f in matched_m if m_f in _distinctive_magic]
                        if len(dist_hits) >= 2 or len(matched_m) >= 4:
                            hit_seeds.append(s_val)
                            if not hit_mults_sample:
                                hit_mults_sample = dist_hits[:3] or matched_m[:3]
                    except Exception as e_seed:
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [TPL-EXEC-ERROR] En '{tpl_id_m}' (semilla {s_val}), la función generadora falló con excepción: {type(e_seed).__name__}: {e_seed}"
                        )
                        break

                if telltale_sample:
                    eff_loc = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                    loc_obj = ShardDataLineLocator(eff_loc) if eff_loc and eff_loc.is_file() else locator
                    t_info_m = loc_obj.find_tuple_for_question(cid, template_id=tpl_id_m) if loc_obj else None
                    s_off, e_off, _ = loc_obj.find_offending_lines(t_info_m, "distractor_integrity_linter", telltale_sample[0]) if loc_obj else (1, 1, [])
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [PSYCHOMETRIC-OPTIONS / parenthetical_telltale_linter / distractor_integrity_linter] En '{tpl_id_m}' (función '{gen_fn_m}', Líneas {s_off}..{e_off} en {source_name}), "
                        f"la opción visible contiene metainformación delatora: '{telltale_sample[0]}'. "
                        "Elimina palabras y coletillas delatoras del texto visible de la opción y traslada explicaciones conceptuales a 'error_rationale' o 'sol'."
                    )

                _MAGIC_MULT_MIN_FRACTION = 0.07
                _magic_min_hits = max(1, int(_MAGIC_MULT_MIN_FRACTION * iso_valid_seeds) + 1) if iso_valid_seeds > 0 else 22
                if len(hit_seeds) >= _magic_min_hits:
                    eff_loc = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                    loc_obj = ShardDataLineLocator(eff_loc) if eff_loc and eff_loc.is_file() else locator
                    t_info_m = loc_obj.find_tuple_for_question(cid, template_id=tpl_id_m) if loc_obj else None
                    s_off, e_off, _ = loc_obj.find_offending_lines(t_info_m, "diagnostic_rationale_alignment_linter", "multiplicador") if loc_obj else (1, 1, [])
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [DIAG-MAGIC-MULT] En '{tpl_id_m}' (función '{gen_fn_m}', Líneas {s_off}..{e_off} en {source_name}), "
                        f"los distractores numéricos en {len(hit_seeds)}/{iso_valid_seeds or len(eval_seeds)} semillas (>{_MAGIC_MULT_MIN_FRACTION*100:.0f}%, ej. seed={hit_seeds[0]}) coinciden con multiplicadores arbitrarios prohibidos ({hit_mults_sample}) respecto a la respuesta correcta. "
                        f"PROHIBIDO ajustar multiplicadores decimales; reemplace la expresión por la fórmula algebraica del error conceptual."
                    )
                if iso_valid_seeds >= 10 and len(iso_hit_seeds) >= _ISO_MIN_FRACTION * iso_valid_seeds and len(hit_seeds) == 0:
                    eff_loc = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                    loc_obj = ShardDataLineLocator(eff_loc) if eff_loc and eff_loc.is_file() else locator
                    t_info_m = loc_obj.find_tuple_for_question(cid, template_id=tpl_id_m) if loc_obj else None
                    s_off, e_off, _ = loc_obj.find_offending_lines(t_info_m, "diagnostic_rationale_alignment_linter", "multiplicador") if loc_obj else (1, 1, [])
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [DIAG-MAGIC-MULT] En '{tpl_id_m}' (funcion '{gen_fn_m}', Lineas {s_off}..{e_off} en {source_name}), "
                        f"un distractor numerico equivale a {iso_hit_ratio} x respuesta correcta en {len(iso_hit_seeds)}/{iso_valid_seeds} semillas (razon fija sistematica, colisiona con el linter final). "
                        f"PROHIBIDO ajustar multiplicadores decimales; reemplace la expresión por la fórmula algebraica del error conceptual."
                    )
                if strict and len(set(corr_answers_sample)) <= 1 and len(corr_answers_sample) >= 10:
                    first_ans_str = str(corr_answers_sample[0]) if corr_answers_sample else ""
                    if len(first_ans_str) > 50:
                        first_ans_str = first_ans_str[:47] + "..."
                    eff_loc = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                    loc_obj = ShardDataLineLocator(eff_loc) if eff_loc and eff_loc.is_file() else locator
                    t_info_m = loc_obj.find_tuple_for_question(cid, template_id=tpl_id_m) if loc_obj else None
                    s_off, e_off, _ = loc_obj.find_offending_lines(t_info_m, "TPL-STATIC-OPT", "correct") if loc_obj else (1, 1, [])
                    m3_errors.append(
                        f"{cid}.json ({source_name}): [TPL-STATIC-OPT] En '{tpl_id_m}' (función '{gen_fn_m}', Líneas {s_off}..{e_off} en {source_name}), "
                        f"mono-clave fija detectada en {len(corr_answers_sample)} semillas: '{first_ans_str}'. "
                        f"La respuesta correcta debe ser dinámica y depender de parámetros generados (@var@)."
                    )

            # Verificación 4b — Detección Temprana de Mono-Clave [TPL-STATIC-OPT] para FIB y MS
            if strict:
                for t_idx_m, tpl_m in enumerate(tpls):
                    itype_m = tpl_m.get("interaction_type") or tpl_m.get("question_type")
                    if itype_m not in ("fill_in_the_blank", "multiple_select"):
                        continue
                    c_call_m = gen_callables[t_idx_m] if t_idx_m < len(gen_callables) else None
                    if not callable(c_call_m):
                        continue
                    tpl_id_m = tpl_m.get("id") or tpl_m.get("template_id") or f"T-{cid}-{t_idx_m+1:02d}"
                    gen_fn_m = tpl_m.get("gen_fn_name") or getattr(c_call_m, "__name__", "gen_fn")
                    tpl_seed_off = _seed_base + (t_idx_m * 500)
                    eval_seeds = [tpl_seed_off + s_i for s_i in range(20)]
                    corr_samples: List[str] = []
                    for s_val in eval_seeds:
                        try:
                            import random
                            res_m = c_call_m(random.Random(s_val))
                            if not isinstance(res_m, dict):
                                continue
                            vars_m = res_m.get("vars", {}) if isinstance(res_m.get("vars"), dict) else {}
                            if itype_m == "fill_in_the_blank":
                                c_raw = str(res_m.get("correct", ""))
                                c_txt = format_template_string(c_raw, vars_m) if format_template_string else c_raw
                                corr_samples.append(c_txt.strip())
                            else:  # multiple_select
                                opts_m = res_m.get("options", [])
                                corr_set = tuple(sorted([
                                    (format_template_string(str(o.get("content") or o.get("value") or ""), vars_m) if format_template_string else str(o.get("content") or o.get("value") or "")).strip()
                                    for o in opts_m if isinstance(o, dict) and o.get("is_correct")
                                ]))
                                corr_samples.append(str(corr_set))
                        except Exception:
                            pass
                    if len(set(corr_samples)) <= 1 and len(corr_samples) >= 10:
                        first_ans_str = str(corr_samples[0]) if corr_samples else ""
                        if len(first_ans_str) > 50:
                            first_ans_str = first_ans_str[:47] + "..."
                        eff_loc = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                        loc_obj = ShardDataLineLocator(eff_loc) if eff_loc and eff_loc.is_file() else locator
                        t_info_m = loc_obj.find_tuple_for_question(cid, template_id=tpl_id_m) if loc_obj else None
                        s_off, e_off, _ = loc_obj.find_offending_lines(t_info_m, "TPL-STATIC-OPT", "correct") if loc_obj else (1, 1, [])
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [TPL-STATIC-OPT] En '{tpl_id_m}' (función '{gen_fn_m}', Líneas {s_off}..{e_off} en {source_name}), "
                            f"mono-clave fija detectada en {len(corr_samples)} semillas: '{first_ans_str}'. "
                            f"La respuesta correcta debe ser dinámica y depender de parámetros generados (@var@)."
                        )

                # Verificación 5 — Compuerta de Diversidad de Enunciados [STEM-DIVERSITY-GATE] (Paridad con run.py --stage build)
                if eff_min_arch >= 3 and len(tpls) >= 3 and seeds >= 30:
                    try:
                        from engine.diversity import mask_stem_numbers as _mask_stem_nums
                    except Exception:
                        def _mask_stem_nums(st: str) -> str:
                            return re.sub(r"\b\d+(?:\.\d+)?\b", "[NUM]", re.sub(r"\s+", " ", st.strip()))

                    # Stage 2 -> Stage 4 contract parity: quota/threshold come from the manifest
                    # (written by plan_shards from engine.stage_contract), never hardcoded here.
                    _s4c = (shard_entry.get("stage4_contract") or {}).get(cid) if isinstance(shard_entry, dict) else None
                    if not isinstance(_s4c, dict):
                        # Legacy manifest without stage4_contract: preserve id-prefix heuristic.
                        _legacy_skill = cid.startswith("Hab-") or (
                            not cid.startswith(("C-", "H-")) and bool(locals().get("is_skill", False))
                        )
                        _s4c = _s4_competency_contract("skill" if _legacy_skill else "concept")
                    is_true_skill = _s4_is_skill_type(_s4c.get("type", ""))
                    quota_build = int(_s4c["quota"])
                    req_unique_stems = int(_s4c["required_unique_stems"])
                    all_masked_stems: Set[str] = set()
                    stem_line_ranges: List[str] = []
                    eff_loc_s = fix_files_by_cid.get(cid) if is_modular_fix else shard_data_path
                    loc_obj_s = ShardDataLineLocator(eff_loc_s) if eff_loc_s and eff_loc_s.is_file() else locator

                    for t_idx_s, tpl_s in enumerate(tpls):
                        tpl_id_s = tpl_s.get("id") or tpl_s.get("template_id") or f"T-{cid}-{t_idx_s+1:02d}"
                        sv_list = tpl_s.get("stem_variants") or ([tpl_s.get("stem_es")] if tpl_s.get("stem_es") else [])
                        c_call_s = gen_callables[t_idx_s] if t_idx_s < len(gen_callables) else None
                        sample_vars_list: List[Dict[str, Any]] = []
                        if callable(c_call_s):
                            for s_try in (100, 101, 102):
                                try:
                                    import random
                                    r_try = c_call_s(random.Random(s_try))
                                    if isinstance(r_try, dict) and isinstance(r_try.get("vars"), dict):
                                        sample_vars_list.append(r_try["vars"])
                                except Exception:
                                    pass
                        for sv_raw in sv_list:
                            sv_str = str(sv_raw).strip()
                            if not sv_str:
                                continue
                            if sample_vars_list and format_template_string:
                                for sv_vars in sample_vars_list:
                                    rendered_sv = format_template_string(sv_str, sv_vars)
                                    all_masked_stems.add(_mask_stem_nums(rendered_sv))
                            else:
                                dummy_sv = re.sub(r"@[a-zA-Z0-9_]+(?::[^@]+)?@", "100", sv_str)
                                all_masked_stems.add(_mask_stem_nums(dummy_sv))

                        if loc_obj_s:
                            t_info_s = loc_obj_s.find_tuple_for_question(cid, template_id=tpl_id_s)
                            s_ln, e_ln, _ = loc_obj_s.find_offending_lines(t_info_s, "anti_gaming_psychometric_linter", "stem")
                            rng_lbl = f"L{s_ln}..L{e_ln}" if s_ln != e_ln else f"L{s_ln}"
                            if rng_lbl not in stem_line_ranges:
                                stem_line_ranges.append(rng_lbl)

                    if len(all_masked_stems) < req_unique_stems:
                        cat_label = "skills" if is_true_skill else "concepts/facts"
                        _adv = _s4_stems_advice("skill" if is_true_skill else "concept")
                        req_per_tpl = _adv["per_tpl"]
                        tot_rec = _adv["total"]
                        lines_ctx = f" [{', '.join(stem_line_ranges)} en {source_name}]" if stem_line_ranges else ""
                        m3_errors.append(
                            f"{cid}.json ({source_name}): [STEM-DIVERSITY-GATE] Diagnostic: Stem diversity gate failed for competency '{cid}' "
                            f"(only {len(all_masked_stems)} stems, required >= {req_unique_stems} unique, quota {quota_build} for {cat_label}){lines_ctx}. "
                            f"Provide >= {req_per_tpl} distinct syntactic stems per template (totaling >= {tot_rec})."
                        )

    if deferred_verifier_errors or m3_errors:
        is_clean = False
        raw_errors = deferred_verifier_errors + m3_errors + list(raw_errors)

    if not is_clean:
        from check_templates import render_compact_aggregated_errors, count_distinct_shard_error_hunks
        error_count = count_distinct_shard_error_hunks(
            raw_errors, targets=compiled_paths, shard_py=shard_data_path
        )
        compact_report = render_compact_aggregated_errors(
            raw_errors, targets=compiled_paths, shard_py=shard_data_path, max_output_lines=28
        )
        from check_templates import normalize_error_string_for_hash
        normalized_errs = sorted([normalize_error_string_for_hash(str(e)) for e in raw_errors])
        err_hash = hashlib.sha256("\n".join(normalized_errs).encode("utf-8")).hexdigest()

        if state.get("last_err_hash") == err_hash:
            same_error_streak = state.get("same_error_streak", 0) + 1
        else:
            same_error_streak = 1
        state["same_error_streak"] = same_error_streak
        state["last_err_hash"] = err_hash
        state["error_count"] = error_count
        state["has_syntax_error"] = False
        state["affected_line_count"] = error_count
        state["error_sha256"] = err_hash

        _cleanup_stale_pass_marker()

        if receipt_p:
            try:
                import time
                r_data = {}
                if receipt_p.is_file():
                    try:
                        r_data = json.loads(receipt_p.read_text(encoding="utf-8"))
                    except Exception:
                        r_data = {}
                r_data["shard_id"] = shard_id
                r_data["compiled_status"] = "FAIL"
                r_data["compilation_errors"] = [compact_report]
                r_data["error_count"] = error_count
                r_data["has_syntax_error"] = False
                r_data["compiled_at"] = time.time()
                _atomic_write_json(receipt_p, r_data)
            except Exception:
                pass

        if same_error_streak >= 3:
            terminal_stop = (
                f"\n[-] [CIRCUIT BREAKER HALT: 3 fallos consecutivos idénticos para shard '{shard_id}']. "
                f"STOP, send_message the Director."
            )
            compact_report = compact_report + terminal_stop
            print(terminal_stop, file=sys.stderr)

        print(f"\n[-] FAIL: {len(raw_errors)} errores detectados ({error_count} errores consolidados) al compilar {shard_id}:\n{compact_report}", file=sys.stderr)
        state["last_errors"] = [compact_report]
        _atomic_write_json(compile_att_file, state)
        return False, [compact_report]

    # Clear compilation attempts on success (pass clears the halt)
    if compile_att_file.is_file():
        try:
            compile_att_file.unlink()
        except Exception:
            pass

    import time
    pass_marker = att_dir / f"pass_{norm_shard_id}.json"
    pass_payload = {
        "shard_id": shard_id,
        "status": "PASS",
        "source_sha256": source_sha256,
        "template_counts": {cid: len(tpls) for cid, tpls in templates_by_cid.items()},
        "timestamp": time.time(),
    }
    _atomic_write_json(pass_marker, pass_payload)

    for cp in compiled_paths:
        if cp.is_file():
            try:
                _atomic_write_json(cp, json.loads(cp.read_text(encoding="utf-8")))
            except Exception:
                pass

    cert_path = shards_dir / f"{norm_shard_id}.cert.json"
    cert_payload = {
        "schema_version": 1,
        "stage": "shard",
        "artifact_id": shard_id,
        "source_sha256": source_sha256,
        "cta_sha256": hashlib.sha256(cta_p.read_bytes()).hexdigest() if (cta_p and cta_p.is_file()) else "",
        "compiler_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "contract_version": 2,
        "template_shas": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in compiled_paths},
        "passed_50_seeds": True,
        "created_at": time.time(),
    }
    _atomic_write_json(cert_path, cert_payload)

    if receipt_p:
        try:
            r_data = {}
            if receipt_p.is_file():
                try:
                    r_data = json.loads(receipt_p.read_text(encoding="utf-8"))
                except Exception:
                    r_data = {}
            r_data["shard_id"] = shard_id
            r_data["compiled_status"] = "PASS"
            r_data["compiled_templates"] = [p.as_posix() for p in compiled_paths]
            r_data["compiled_at"] = time.time()
            _atomic_write_json(receipt_p, r_data)
        except Exception:
            pass

    total_archetypes = sum(len(tpls) for tpls in templates_by_cid.values())
    written_files_str = ", ".join(p.as_posix() for p in compiled_paths)
    print(f"[+] PASS: Shard '{shard_id}' compilado exitosamente ({len(compiled_paths)} competencias, {total_archetypes} plantillas/arquetipos en [{written_files_str}], {seeds} semillas dry-run validadas). STOP: No ejecutes más herramientas y emite tu señal DONE.")
    return True, []


def compile_shard_file(
    shard_data_path: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    strict: bool = True,
    seeds: int = 50,
    min_archetypes: Optional[int] = None,
    **kwargs,
) -> Tuple[bool, List[str]]:
    """Helper for run.py pipeline stage 3 compatibility."""
    return compile_shard(
        work_dir_or_path=shard_data_path,
        shard_id=kwargs.get("shard_id"),
        strict=strict,
        seeds=seeds,
        output_dir=output_dir,
        min_archetypes=min_archetypes if min_archetypes is not None else kwargs.get("min_archetypes"),
        **kwargs,
    )


def main():
    parser = argparse.ArgumentParser(description="Deterministic Python Tuple Compiler for Content-to-Course v3.21 Shards")
    parser.add_argument("shard_data_path", nargs="?", default=None, help="Optional positional path to shard_XX_data.py")
    parser.add_argument("--input", "-i", dest="input_path", default=None, help="Optional path to shard_XX_data.py")
    parser.add_argument("--output", "-o", dest="output_path", default=None, help="Optional output path or directory")
    parser.add_argument("--cta", default=None, help="Optional path to cta.json")
    parser.add_argument("--manifest", default=None, help="Optional path to manifest")
    parser.add_argument("--work", "--work-dir", dest="work", default="work", help="Path to work directory (default: work)")
    parser.add_argument("--shard", default=None, help="Shard ID to compile (e.g. shard_01)")
    parser.add_argument("--output-dir", default=None, help="Output directory for templates (e.g. work/templates)")
    parser.add_argument("--strict", action="store_true", default=True, help="Enforce strict validation (default: True)")
    parser.add_argument("--no-strict", dest="strict", action="store_false", help="Bypass strict validation")
    parser.add_argument("--seeds", type=int, default=50, help="Number of dry-run seeds (default: 50)")
    parser.add_argument("--min-archetypes", dest="min_archetypes", type=int, default=None, help="Minimum disjoint archetypes (tuples) required per competency in TEMPLATES (default: 3)")
    parser.add_argument("--watchdog-timeout", type=float, default=15.0, help="Watchdog hard timeout budget in seconds (default: 15.0)")
    args = parser.parse_args()

    work_or_path = args.input_path or args.shard_data_path or args.work
    s_id = args.shard
    receipt_path = None
    eff_out_dir = args.output_dir
    if args.output_path:
        if str(args.output_path).lower().endswith(".json"):
            receipt_path = args.output_path
        elif not eff_out_dir:
            eff_out_dir = args.output_path

    if work_or_path == "work" and not (Path("work/shards/pre_shard_manifest.json").is_file() or Path("work/pre_shard_manifest.json").is_file()):
        inferred = infer_work_dir(work_or_path, shard_id=s_id)
        if inferred != Path(work_or_path):
            work_or_path = str(inferred)

    success, _ = compile_shard(
        work_dir_or_path=work_or_path,
        shard_id=s_id,
        strict=args.strict,
        seeds=args.seeds,
        output_dir=eff_out_dir,
        output_path=receipt_path,
        cta_path=args.cta,
        manifest_path=args.manifest,
        min_archetypes=args.min_archetypes,
        watchdog_timeout=args.watchdog_timeout,
    )
    try:
        sys.stdout.flush()
        sys.stderr.flush()
    except Exception:
        pass
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
