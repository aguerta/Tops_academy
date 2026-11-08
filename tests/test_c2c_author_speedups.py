"""Tests for author speed-ups: static precheck, MS verifier arity, pure-Python _pv, hook author rewrite."""
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
sys.path.insert(0, str(SKILL))

import shard_precheck  # noqa: E402
from engine.sandbox import validate_code_ast  # noqa: E402


def test_canonical_pv_in_prompts_is_sandbox_safe_and_handles_inequalities():
    lean_text = (SKILL / "system_prompts" / "lean" / "prompt_shard_author.md").read_text(encoding="utf-8")
    m = re.search(r"```python\s*([\s\S]*?)```", lean_text)
    assert m, "Missing python block in lean prompt"
    code = m.group(1)
    assert "import re" not in code
    # Validate AST passes Stage 4 sandbox security validator
    validate_code_ast(code)
    ns: dict = {}
    exec(compile(code, "lean_example", "exec"), ns)
    pv = ns["_pv"]
    assert pv(r"P \le 0.0118") == 0.0118
    assert pv("$x = -1.5$") == -1.5
    assert pv("1e-3") == 0.001


def test_precheck_reports_all_known_problems_at_once():
    src = (
        'RATS = {"D-1": r"corto"}\n'
        "def gen_a_1(rng):\n    while True:\n        break\n"
        "def ver_a_4(res, v=None):\n    raise ValueError('x')\n"
        "ver_a_2 = ver_a_1\n"
    )
    out = " ".join(shard_precheck.precheck_source(src))
    for code in ("TPL-AD-HOC-PERTURBATION", "VER-SIGNATURE", "TPL-DEBUG-ARTIFACT", "NO-GLOBAL-ALIAS", "TPL-DYNAMIC-RATIONALE"):
        assert code in out


def test_precheck_clean_source_is_silent():
    src = "def gen_a_1(rng):\n    return {}\ndef ver_a_1(c, v):\n    return abs(float(c) - v['a']) < 1e-3\n"
    assert shard_precheck.precheck_source(src) == []


def test_compile_shard_arity_detection_and_no_hidden_ast_injection():
    text = (SKILL / "compile_shard.py").read_text(encoding="utf-8")
    assert "len(pos_params) == 2 or len(sig.parameters) == 2" not in text
    assert 'isinstance(res_test.get("options"), list)' in text
    assert "shard_scaffold" not in text
