"""Focused hardening tests for engine/assemble.py and c2c_hook_guard.py."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Dict

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SKILL_ROOT = _REPO_ROOT / ".agents" / "skills" / "content-to-course"
if str(_SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(_SKILL_ROOT))

from engine.assemble import assemble_question  # noqa: E402


def _load_hook_guard():
    guard_path = _SKILL_ROOT / "c2c_hook_guard.py"
    spec = importlib.util.spec_from_file_location("c2c_hook_guard", guard_path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["c2c_hook_guard"] = mod
    spec.loader.exec_module(mod)
    return mod


guard = _load_hook_guard()


# ==============================================================================
# 1. assemble.py: FIB common_misconception_warning & decimal rounding prompt
# ==============================================================================


def test_fib_misconception_warning_uses_cta_wrong_belief_and_omitted_step():
    template = {
        "id": "TPL-FIB-01",
        "competency_id": "Hab-03",
        "interaction_type": "fill_in_the_blank",
        "stem": "Calcule el valor esperado de $X$.",
        "hints": ["Identifique la distribución.", "Sume los productos.", "Verifique el resultado."],
        "detailed_solution": "E[X] = 18.33.",
    }
    gen_result = {"vars": {}, "correct": "18.33"}
    cta_map = {
        "D-OTHER": {
            "competency_id": "Hab-01",
            "wrong_belief": "Otro error de otra competencia",
            "omitted_step": "Otro paso",
        },
        "D-H03-01": {
            "competency_id": "Hab-03",
            "wrong_belief": "El estudiante promedia sin ponderar por las probabilidades",
            "omitted_step": "multiplicar cada valor por su probabilidad $p_i$",
        },
    }

    assembled = assemble_question(
        template=template,
        gen_result=gen_result,
        competency_id="Hab-03",
        question_index=1,
        cta_distractors_map=cta_map,
        seed=7,
    )

    warning = assembled["common_misconception_warning"]
    assert "Verifique cuidadosamente los supuestos y cálculos" not in warning
    assert "promedia sin ponderar por las probabilidades" in warning
    assert "multiplicar cada valor por su probabilidad" in warning
    assert assembled["misconception_warning"] == warning


def test_fib_misconception_warning_falls_back_to_template_error_rationale_or_competency():
    template_with_rationale = {
        "id": "TPL-FIB-02",
        "competency_id": "Hab-05",
        "interaction_type": "fill_in_the_blank",
        "stem": "Calcule la pendiente.",
        "hints": ["Use dos puntos."],
        "detailed_solution": "m = 2.",
        "error_rationale": "Invertir el cociente dx/dy en lugar de dy/dx.",
    }
    assembled_rat = assemble_question(
        template=template_with_rationale,
        gen_result={"vars": {}, "correct": "2"},
        competency_id="Hab-05",
        question_index=1,
        cta_distractors_map=None,
        seed=1,
    )
    assert assembled_rat["common_misconception_warning"] == "Invertir el cociente dx/dy en lugar de dy/dx."

    template_minimal = {
        "id": "TPL-FIB-03",
        "competency_id": "Hab-09",
        "interaction_type": "fill_in_the_blank",
        "stem": "Calcule el determinante.",
        "hints": ["Regla de Sarrus."],
        "detailed_solution": "det = 5.",
    }
    assembled_min = assemble_question(
        template=template_minimal,
        gen_result={"vars": {}, "correct": "5"},
        competency_id="Hab-09",
        question_index=1,
        cta_distractors_map=None,
        seed=1,
    )
    assert "Verifique cuidadosamente los supuestos y cálculos" not in assembled_min["common_misconception_warning"]
    assert "Hab-09" in assembled_min["common_misconception_warning"]


def test_fib_appends_rounding_instruction_for_three_or_more_decimals():
    base_tpl = {
        "id": "TPL-FIB-DEC",
        "competency_id": "Hab-04",
        "interaction_type": "fill_in_the_blank",
        "hints": ["Paso 1"],
        "detailed_solution": "Resultado numérico.",
    }

    # Case 1: 4 decimals and no mention of decimals/rounding -> appends suffix
    q1 = assemble_question(
        template={**base_tpl, "stem": "Calcule la media muestral."},
        gen_result={"vars": {}, "correct": "18.3333"},
        competency_id="Hab-04",
        question_index=1,
        seed=1,
    )
    assert q1["stem"] == "Calcule la media muestral. (Exprese su respuesta redondeada a 4 decimales)."

    # Case 2: 3 decimals negative number -> appends suffix
    q2 = assemble_question(
        template={**base_tpl, "stem": "Determine el coeficiente."},
        gen_result={"vars": {}, "correct": "-0.125"},
        competency_id="Hab-04",
        question_index=2,
        seed=1,
    )
    assert q2["stem"].endswith(" (Exprese su respuesta redondeada a 4 decimales).")

    # Case 3: Already mentions "decimales" or "Redondee" (case-insensitive) -> unchanged
    q3 = assemble_question(
        template={**base_tpl, "stem": "Calcule la media con 2 Decimales."},
        gen_result={"vars": {}, "correct": "18.3333"},
        competency_id="Hab-04",
        question_index=3,
        seed=1,
    )
    assert q3["stem"] == "Calcule la media con 2 Decimales."

    q4 = assemble_question(
        template={**base_tpl, "stem": "Redondee su respuesta al entero o milésima."},
        gen_result={"vars": {}, "correct": "18.3333"},
        competency_id="Hab-04",
        question_index=4,
        seed=1,
    )
    assert q4["stem"] == "Redondee su respuesta al entero o milésima."

    # Case 4: Fewer than 3 decimals or algebraic expression -> unchanged
    q5 = assemble_question(
        template={**base_tpl, "stem": "Calcule el valor exacto."},
        gen_result={"vars": {}, "correct": "18.33"},
        competency_id="Hab-04",
        question_index=5,
        seed=1,
    )
    assert q5["stem"] == "Calcule el valor exacto."


# ==============================================================================
# 2. c2c_hook_guard.py: 450-line threshold on 1st failure & --dry-run allow
# ==============================================================================


def _setup_worker_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(guard, "USER_HOME", tmp_path / "home")
    guard._LOCK_CACHE.clear()

    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    att_dir = work_dir / ".check_attempts"
    shards_dir.mkdir(parents=True)
    att_dir.mkdir(parents=True)

    lock_path = work_dir / ".c2c_subagent_lock.json"
    lock_path.write_text(
        json.dumps(
            {
                "active": True,
                "director_conversation_id": "dir-001",
                "worker_conversation_id": "worker-001",
                "work_dir": str(work_dir),
            }
        ),
        encoding="utf-8",
    )
    return work_dir, shards_dir, att_dir, lock_path


def test_shard_write_file_threshold_450_on_first_failure_and_250_on_second(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    _, shards_dir, att_dir, lock_path = _setup_worker_env(tmp_path, monkeypatch)
    shard_py = shards_dir / "shard_01_data.py"
    compile_file = att_dir / "compile_shard_01.json"

    content_350 = "".join([f"# line {i}\n" for i in range(350)])
    content_460 = "".join([f"# line {i}\n" for i in range(460)])

    # 1st failure (distinct_compiles == 1): 350 lines <= 450 -> ALLOW
    shard_py.write_text(content_350, encoding="utf-8")
    compile_file.write_text(json.dumps({"distinct_compiles": 1, "last_errors": []}), encoding="utf-8")
    res_1_allow = guard.process_hook(
        {
            "conversationId": "worker-001",
            "toolCall": {"name": "write_file", "args": {"Path": str(shard_py), "Content": content_350}},
        },
        custom_lock_file=str(lock_path),
    )
    assert res_1_allow == {"decision": "allow"}

    # 1st failure (distinct_compiles == 1): 460 lines > 450 -> DENY
    shard_py.write_text(content_460, encoding="utf-8")
    res_1_deny = guard.process_hook(
        {
            "conversationId": "worker-001",
            "toolCall": {"name": "write_file", "args": {"Path": str(shard_py), "Content": content_460}},
        },
        custom_lock_file=str(lock_path),
    )
    assert res_1_deny["decision"] == "deny"
    assert "supera las 450 líneas" in res_1_deny["reason"]

    # 2nd+ failure (distinct_compiles == 2): 350 lines > 250 -> DENY
    shard_py.write_text(content_350, encoding="utf-8")
    compile_file.write_text(json.dumps({"distinct_compiles": 2, "last_errors": []}), encoding="utf-8")
    res_2_deny = guard.process_hook(
        {
            "conversationId": "worker-001",
            "toolCall": {"name": "write_file", "args": {"Path": str(shard_py), "Content": content_350}},
        },
        custom_lock_file=str(lock_path),
    )
    assert res_2_deny["decision"] == "deny"
    assert "supera las 250 líneas" in res_2_deny["reason"]


def test_compile_shard_dry_run_allowed_while_source_inspection_denied(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    _, _, _, lock_path = _setup_worker_env(tmp_path, monkeypatch)

    allow_res = guard.process_hook(
        {
            "conversationId": "worker-001",
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": "python .agents/skills/content-to-course/compile_shard.py --shard shard_01 --dry-run"},
            },
        },
        custom_lock_file=str(lock_path),
    )
    assert allow_res == {"decision": "allow"}

    deny_res = guard.process_hook(
        {
            "conversationId": "worker-001",
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": "Get-Content .agents/skills/content-to-course/compile_shard.py"},
            },
        },
        custom_lock_file=str(lock_path),
    )
    assert deny_res["decision"] == "deny"
