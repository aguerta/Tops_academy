"""Tests for --fail-total accumulation mode vs default Fail-Fast mode in compile_shard.py."""

import json
import sys
from pathlib import Path

import pytest

_skill_root = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

from compile_shard import compile_shard


def _setup_mini_work(tmp_path: Path) -> Path:
    work = tmp_path / "work"
    (work / "shards").mkdir(parents=True, exist_ok=True)
    (work / "templates").mkdir(parents=True, exist_ok=True)

    cta = {
        "competencies": [
            {
                "id": "C-01",
                "title": "Test Concept",
                "type": "concept",
                "distractors": [
                    {"id": f"D-C01-0{i}", "wrong_belief": f"Wrong belief {i} for testing."}
                    for i in range(1, 7)
                ],
            }
        ]
    }
    (work / "cta.json").write_text(json.dumps(cta), encoding="utf-8")

    manifest = {
        "shards": [
            {
                "shard_id": "shard_01",
                "competencies": [cta["competencies"][0]],
            }
        ]
    }
    (work / "shards" / "pre_shard_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    # Shard with multiple distinct errors across multiple tuples:
    # 1) T-C01-01: short hint (< 25 chars)
    # 2) T-C01-02: unsound verifier (returns False)
    # 3) T-C01-03: unbalanced KaTeX brace in stem_variants
    shard_py = '''
RATS = {f"D-C01-0{i}": f"Error algebraico en calculo de @a@ y @b@ paso {i}." for i in range(1, 7)}

def gen_1(rng):
    a = rng.randint(10, 40)
    b = rng.randint(10, 40)
    ans = a + b
    ds = [(f"D-C01-0{i}", str(ans + i * 2)) for i in range(1, 7)]
    return {"vars": {"a": a, "b": b, "ans": ans}, "correct": str(ans), "ds": ds}

def ver_ok(c, v):
    return int(c) == v["a"] + v["b"]

def ver_bad(c, v):
    return int(c) == v["a"] + v["b"] + 999

TEMPLATES = [
    (
        "T-C01-01",
        "C-01",
        "mc7",
        gen_1,
        ver_ok,
        ("easy", "Remember"),
        [
            "Calcule la suma exacta de @a@ y @b@ en el modelo:",
            "Determine el resultado total al sumar @a@ con @b@:",
            "Halle el valor numerico de @a@ + @b@ directamente:",
        ],
        [
            "Pista corta",
            "Considere los valores iniciales dados en el problema.",
            "Verifique la operacion aritmetica entre los terminos.",
        ],
        "La suma de @a@ y @b@ es exactamente @ans@.",
    ),
    (
        "T-C01-02",
        "C-01",
        "fib",
        gen_1,
        ver_bad,
        ("medium", "Understand"),
        [
            "Escriba el resultado de sumar @a@ y @b@ paso a paso:",
            "Indique el valor obtenido al combinar @a@ con @b@:",
            "Calcule cuanto vale la expresion @a@ + @b@ ahora:",
        ],
        [
            "Observe cuidadosamente los dos operandos principales.",
            "Aplique la adicion basica sobre ambos parametros.",
            "Verifique que el resultado supere ambos sumandos.",
        ],
        "El resultado es @ans@ al sumar ambos parametros.",
    ),
    (
        "T-C01-03",
        "C-01",
        "fib",
        gen_1,
        ver_ok,
        ("hard", "Apply"),
        [
            "Halle $\\\\frac{@a@ + @b@$ con precision algebraica:",
            "Determine el total de @a@ mas @b@ en el sistema:",
            "Obtenga la suma directa de @a@ y @b@ evaluada:",
        ],
        [
            "Identifique primero cada parametro entero dado.",
            "Sume ambos valores manteniendo el signo positivo.",
            "Confirme que el entero final sea consistente.",
        ],
        "La suma solicitada produce exactamente @ans@.",
    ),
]
'''
    (work / "shards" / "shard_01_data.py").write_text(shard_py, encoding="utf-8")
    return work


def test_fail_fast_vs_fail_total_accumulates_all_tuple_errors(tmp_path: Path):
    work_ff = _setup_mini_work(tmp_path / "ff")
    ok_ff, errs_ff = compile_shard(work_ff, "shard_01", strict=True, seeds=10, fail_total=False)
    assert not ok_ff
    assert len(errs_ff) == 1
    assert "menos de 25 caracteres" in errs_ff[0]
    assert "TPL-VERIFIER-UNSOUND" not in errs_ff[0]
    assert "TPL-KATEX" not in errs_ff[0]

    work_ft = _setup_mini_work(tmp_path / "ft")
    ok_ft, errs_ft = compile_shard(work_ft, "shard_01", strict=True, seeds=10, fail_total=True)
    assert not ok_ft
    combined = "\n".join(errs_ft)
    assert "TPL-VERIFIER-UNSOUND" in combined
    assert "TPL-KATEX" in combined
    log_file = work_ft / "shards" / "shard_01_compile_error.log"
    assert log_file.is_file()
    log_text = log_file.read_text(encoding="utf-8")
    assert "menos de 25 caracteres" in log_text
    assert "TPL-VERIFIER-UNSOUND" in log_text
    assert "TPL-KATEX" in log_text
