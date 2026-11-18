"""Regression tests for engine/invariants.py and c2c_hook_guard.py hardening."""

import json
import sys
from pathlib import Path

_skill_root = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

import c2c_hook_guard as hook
from engine.invariants import (
    _unwrap_text_in_math,
    check_instance_invariants,
    check_unrendered_placeholders,
    validate_katex_syntax,
)


def test_invariants_escaped_dollar_does_not_desync_math_blocks():
    txt = r"El costo es \$50 y la fraccion es $\frac{1}{2}$."
    errs = validate_katex_syntax(txt, "stem")
    assert errs == [], f"Unexpected errors on valid escaped dollar + math: {errs}"

    # Unbalanced brace inside real math after escaped dollar MUST still be caught
    bad_txt = r"El costo es \$50 y la fraccion es $\frac{1}{2$."
    bad_errs = validate_katex_syntax(bad_txt, "stem")
    assert bad_errs, "Unclosed brace after escaped dollar was missed!"

    # check_unrendered_placeholders keeps aligned math spans
    ok_ph = check_unrendered_placeholders(r"El precio es \$50 para todo $x \in {K}$", "stem")
    assert ok_ph == []

    # _unwrap_text_in_math preserves escaped dollar
    unwrapped = _unwrap_text_in_math(r"Costo \$50 cuando $\text{x} > 0$")
    assert r"\$50" in unwrapped


def test_invariants_fib_numeric_zero_and_stem_leak_without_dollars():
    # FIB with numeric value=0 must be accepted
    fib_inst = {
        "stem": "Calcule el valor de la derivada en el punto critico:",
        "hints": [
            "Identifique la primera derivada de la funcion dada.",
            "Iguale la expresion resultante a la constante nula.",
            "Verifique el signo de la pendiente en la vecindad.",
        ],
        "correct_answer": {"value": 0},
    }
    ok, errs = check_instance_invariants(fib_inst, "fill_in_the_blank")
    assert ok, f"Expected numeric 0 FIB answer to be valid, got: {errs}"

    # Answer leak without '$' in stem must still be caught
    mc7_leak = {
        "stem": "Considere la expresion x^2 + 3x + 1 en el dominio real:",
        "hints": [
            "Observe el termino cuadratico principal de la funcion.",
            "Factorice o evalue los coeficientes positivos dados.",
            "Confirme la consistencia algebraica del polinomio final.",
        ],
        "options": [
            {"content": "$x^2 + 3x + 1$", "is_correct": True},
            {"content": "$x^2 - 3x + 1$", "is_correct": False, "error_rationale": "Error de signo en el termino lineal del polinomio."},
            {"content": "$x^2 + 3x - 1$", "is_correct": False, "error_rationale": "Error de signo en el termino independiente final."},
            {"content": "$2x^2 + 3x + 1$", "is_correct": False, "error_rationale": "Duplicacion incorrecta del coeficiente cuadratico."},
            {"content": "$x^2 + 6x + 1$", "is_correct": False, "error_rationale": "Duplicacion incorrecta del coeficiente lineal."},
            {"content": "$x^2 + 3x + 2$", "is_correct": False, "error_rationale": "Incremento arbitrario del termino independiente."},
            {"content": "$x^2 + 2x + 1$", "is_correct": False, "error_rationale": "Reduccion erronea del coeficiente lineal dado."},
        ],
    }
    ok_leak, errs_leak = check_instance_invariants(mc7_leak, "multiple_choice_7_options", strict_length_bounds=False)
    assert not ok_leak
    assert any("leaked verbatim" in e for e in errs_leak)


def test_hook_guard_circuit_breaker_path_and_manifest_competency_ids(tmp_path: Path):
    work_dir = tmp_path / "work"
    (work_dir / ".check_attempts").mkdir(parents=True, exist_ok=True)
    (work_dir / "shards").mkdir(parents=True, exist_ok=True)

    # compile_shard.py writes compile_shard_01.json under work/.check_attempts/
    cb_file = work_dir / ".check_attempts" / "compile_shard_01.json"
    cb_file.write_text(json.dumps({"same_error_streak": 3, "distinct_compiles": 3}), encoding="utf-8")

    assert hook._shard_has_circuit_breaker_halt(work_dir, "shard_01") is True
    assert hook._verify_shard_certified(work_dir, "shard_01", allow_circuit_breaker=True) == []

    # pre_shard_manifest with competency_ids + competencies list of dicts must not stringify dicts
    manifest = {
        "shards": [
            {
                "shard_id": "shard_01",
                "competency_ids": ["C-01"],
                "competencies": [{"id": "C-01", "name": "Concepto 1"}],
            }
        ]
    }
    (work_dir / "shards" / "pre_shard_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (work_dir / "dispatch").mkdir(parents=True, exist_ok=True)
    (work_dir / "dispatch" / "shards.json").write_text(json.dumps({"item_files": []}), encoding="utf-8")

    ok, reason = hook._verify_wave_outputs_before_kill(
        {"work_dir": str(work_dir)},
        {"Action": "kill_all"},
    )
    assert ok, f"Expected Circuit Breaker shard to pass wave barrier, got: {reason}"


def test_hook_guard_course_name_containing_engine_and_python_u_c(tmp_path: Path):
    lock_file = tmp_path / ".c2c_subagent_lock.json"
    lock_file.write_text(
        json.dumps({
            "active": True,
            "director_conversation_id": "dir-1",
            "course_id": "software_engineering",
            "work_dir": str(tmp_path / "courses" / "software_engineering" / "work"),
        }),
        encoding="utf-8",
    )

    # Worker writing to courses/software_engineering/work/shards/shard_01_data.py must NOT be blocked by "engine" substring
    res_write = hook.process_hook(
        {
            "conversationId": "worker-1",
            "toolCall": {
                "name": "write_file",
                "args": {"Path": "courses/software_engineering/work/shards/shard_01_data.py", "Content": "x = 1\n"},
            },
        },
        custom_lock_file=str(lock_file),
    )
    assert res_write["decision"] == "allow", f"False positive block on course name 'software_engineering': {res_write}"

    # Worker running `python -u -c "open('compile_shard.py')"` must be denied
    res_cmd = hook.process_hook(
        {
            "conversationId": "worker-1",
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": "python -u -c \"print(open('compile_shard.py').read())\""},
            },
        },
        custom_lock_file=str(lock_file),
    )
    assert res_cmd["decision"] == "deny"
