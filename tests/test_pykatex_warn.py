import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
sys.path.insert(0, str(SKILL))

import compile_shard as cs  # noqa: E402


def test_valid_math_has_no_warning():
    assert cs.pykatex_warnings(r"$\frac{@a@}{2}$", "ctx") == []


def test_invalid_math_warns():
    if cs._pykatex is None:
        return
    out = cs.pykatex_warnings(r"$\frac{1}$", "ctx")
    assert out and "PYKATEX-WARN" in out[0]


def test_fib_whole_math_and_plain_text_ignored():
    assert cs.pykatex_warnings("texto sin math", "ctx") == []
    assert cs.pykatex_warnings("@x@", "ctx", whole_is_math=True) == []


def test_env_off(monkeypatch):
    monkeypatch.setenv("C2C_PYKATEX", "off")
    assert cs.pykatex_warnings(r"$\frac{1}$", "ctx") == []
