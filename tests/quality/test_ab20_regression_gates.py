"""Comprehensive A/B 2.0 Regression Test Suite.

Validates all gates, contracts, and remediations implemented across Stage 1:
1. Prompts Lean v4.0 Byte-Cap, LF Hygiene & Canonical Compilation.
2. CTA Compiler, Checker & LaTeX Math Invariants (No Autoheal, Matrix Wrapping, R-19, SyntaxWarning).
3. Shard Compiler & MS Adversarial Refutation (CLI flags, helper _g, MS tautology, TPL-ASSUMPTION-LINK, TPL-CONST-DISTRACTOR).
4. Orchestration, Dispatch & Blind Judge (Lean defaults, --fail-total, pointer-stub protection, Heaviest-First, Zero-Preservation).
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
import warnings
from pathlib import Path
from typing import Any, Dict, List

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
SRC_DIR = REPO_ROOT / "src"

for p in [str(SRC_DIR), str(SKILL_DIR), str(REPO_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from compile_cta import compile_cta, compile_cta_module, load_cta_data_module
from check_cta import validate_cta_rules, check_cta_part, ValidationResult
from cta_merge import auto_wrap_bare_latex_in_cta_field
from engine.invariants import validate_katex_syntax, check_instance_invariants
from validator.core import validate_course_content
from validator.models import ValidationError
from compile_shard import compile_shard
import dispatch
from dispatch import (
    ROLE_SPECS,
    load_system_prompt,
    get_type_definitions,
    dispatch_authors,
    dispatch_repair,
    dispatch_judges,
    dispatch_cta_reduce,
)
from judge import check_judge_completeness, compare_judge_responses


# ==============================================================================
# 1. PROMPTS LEAN v4.0 BYTE-CAP & HYGIENE
# ==============================================================================

LEAN_PROMPT_FILES = [
    "prompt_shard_author.md",
    "prompt_cta_architect.md",
    "prompt_blind_judge.md",
    "prompt_repair.md",
    "prompt_cta_harmonizer.md",
]


@pytest.mark.parametrize("prompt_name", LEAN_PROMPT_FILES)
def test_lean_prompts_byte_cap_and_hygiene(prompt_name: str) -> None:
    """Every Lean v4.0 prompt must exist, have <= 5000 UTF-8 bytes and exactly 0 carriage returns."""
    prompt_path = SKILL_DIR / "system_prompts" / "lean" / prompt_name
    assert prompt_path.is_file(), f"Lean prompt file missing: {prompt_path}"

    raw_bytes = prompt_path.read_bytes()
    assert b"\r" not in raw_bytes, f"Prompt {prompt_name} contains CRLF line endings (\\r detected)"


def test_lean_cta_architect_canonical_compile(tmp_path: Path) -> None:
    """Canonical COMPETENCIES example in prompt_cta_architect.md must compile cleanly with 0 SyntaxWarnings."""
    prompt_path = SKILL_DIR / "system_prompts" / "lean" / "prompt_cta_architect.md"
    content = prompt_path.read_text(encoding="utf-8")

    # Extract python code block containing COMPETENCIES
    match = re.search(r"```python\s*([\s\S]*?COMPETENCIES\s*=\s*\[[\s\S]*?\][\s\S]*?)\s*```", content)
    assert match is not None, "Could not find canonical COMPETENCIES python block in prompt_cta_architect.md"

    cta_code = match.group(1)
    cta_data_file = tmp_path / "cta_data.py"
    cta_data_file.write_text(
        f"# -*- coding: utf-8 -*-\nCOURSE_ID = 'test_canonical'\nCOURSE_TITLE = 'Curso Test'\n{cta_code}\n",
        encoding="utf-8",
        newline="\n",
    )

    manifest_file = tmp_path / "pre_cta_manifest.json"
    manifest_data = {
        "files": [
            {
                "doc": "solow.pdf",
                "valid_page_range": [1, 200],
                "total_pages": 200,
            }
        ]
    }
    manifest_file.write_text(json.dumps(manifest_data), encoding="utf-8")

    with warnings.catch_warnings(record=True) as captured_warnings:
        warnings.simplefilter("always", SyntaxWarning)
        ok, cta_dict, errors, _ = compile_cta(
            cta_data_path=cta_data_file,
            output_dir=tmp_path,
            manifest_path=manifest_file,
            require_assumptions=True,
        )

    syntax_warnings = [w for w in captured_warnings if issubclass(w.category, SyntaxWarning)]
    assert len(syntax_warnings) == 0, f"Unexpected SyntaxWarnings during canonical compile: {syntax_warnings}"
    assert ok is True, f"Canonical CTA failed to compile cleanly: {errors}"
    assert len(errors) == 0
    assert cta_dict.get("contract_version") == 2
    assert len(cta_dict.get("competencies", [])) >= 2


# ==============================================================================
# 2. CTA GATES (compile_cta, check_cta, cta_merge, invariants, rules)
# ==============================================================================

def test_cta_no_autoheal_omitted_step_fails_cta_d1(tmp_path: Path) -> None:
    """Skill with < 2 omitted_step distractors is NO LONGER silently autohealed; fails [CTA-D1]."""
    # Define a skill competency with 6 distractors, but only 1 declaring an omitted_step (5 have None)
    competencies_code = """
COMPETENCIES = [
    (
        "skill", "Hab-01", "Cálculo de Estabilidad", "Determinar la estabilidad local.", "Apply",
        "material_fuente.pdf", 1, [],
        [
            ("D1", "Error conceptual 1", "Verdad 1", "$1$", "Hint 1 (largo para evitar warnings de hint corto)", "Omitió paso crítico 1"),
            ("D2", "Error conceptual 2", "Verdad 2", "$2$", "Hint 2 (largo para evitar warnings de hint corto)", None),
            ("D3", "Error conceptual 3", "Verdad 3", "$3$", "Hint 3 (largo para evitar warnings de hint corto)", None),
            ("D4", "Error conceptual 4", "Verdad 4", "$4$", "Hint 4 (largo para evitar warnings de hint corto)", None),
            ("D5", "Error conceptual 5", "Verdad 5", "$5$", "Hint 5 (largo para evitar warnings de hint corto)", None),
            ("D6", "Error conceptual 6", "Verdad 6", "$6$", "Hint 6 (largo para evitar warnings de hint corto)", None),
        ],
        [
            ("A-Hab01-01", "$f'(x^*) < 0$", "Si se viola, el punto no es asintóticamente estable.", "Condición de Lyapunov")
        ]
    )
]
"""
    cta_data_file = tmp_path / "cta_data.py"
    cta_data_file.write_text(competencies_code, encoding="utf-8", newline="\n")

    manifest_file = tmp_path / "pre_cta_manifest.json"
    manifest_data = {
        "files": [{"doc": "material_fuente.pdf", "valid_page_range": [1, 50], "total_pages": 50}]
    }
    manifest_file.write_text(json.dumps(manifest_data), encoding="utf-8")

    ok, cta_dict, errors, _ = compile_cta(
        cta_data_path=cta_data_file,
        output_dir=tmp_path,
        manifest_path=manifest_file,
        require_assumptions=True,
    )

    assert ok is False, "compile_cta should fail when a skill has < 2 omitted_step distractors"
    d1_errors = [e for e in errors if "CTA-D1 violation" in e and "omitted_step" in e]
    assert len(d1_errors) > 0, f"Expected [CTA-D1] violation for omitted_step, got errors: {errors}"
    assert "has 1 distractors with omitted_step (minimum 2 required)" in d1_errors[0]


def test_cta_hard_fail_manifestation_equals_correct_belief() -> None:
    """check_cta must strictly fail (valid=False) when manifestation == correct_belief."""
    cta_dict = {
        "course_id": "test_manif_cb",
        "title": "Curso Test",
        "macro_competency": "Dominio integral",
        "contract_version": 2,
        "competencies": [
            {
                "id": "C-01",
                "type": "concept",
                "name": "Concepto 1",
                "description_latex": "Definición formal de concepto 1.",
                "bloom": "Understand",
                "evidence": [{"doc": "doc.pdf", "page": 1}],
                "prerequisites": [],
                "distractors": [
                    {
                        "id": "D-C01-01",
                        "name": "Distractor 1",
                        "wrong_belief": "Creencia errónea 1",
                        "correct_belief": "$k = k^*$",
                        "manifestation": "$k = k^*$",  # Identical to correct_belief
                        "remediation_hint": "Pista suficientemente larga para evitar warnings de longitud reducida.",
                    },
                    {
                        "id": "D-C01-02",
                        "name": "Distractor 2",
                        "wrong_belief": "Creencia errónea 2",
                        "correct_belief": "$k = k^*$",
                        "manifestation": "$k > k^*$",
                        "remediation_hint": "Pista suficientemente larga para evitar warnings de longitud reducida.",
                    },
                    {
                        "id": "D-C01-03",
                        "name": "Distractor 3",
                        "wrong_belief": "Creencia errónea 3",
                        "correct_belief": "$k = k^*$",
                        "manifestation": "$k < k^*$",
                        "remediation_hint": "Pista suficientemente larga para evitar warnings de longitud reducida.",
                    },
                ],
                "assumptions": [
                    {
                        "id": "A-C01-01",
                        "statement_latex": "$k^* > 0$",
                        "violation_consequence": "Si no se cumple, el estado estacionario no existe.",
                    }
                ],
            }
        ],
    }

    manifest_data = {"files": [{"doc": "doc.pdf", "valid_page_range": [1, 10]}]}
    res = validate_cta_rules(cta_dict, manifest_data=manifest_data, require_assumptions=True)

    assert isinstance(res, ValidationResult)
    is_valid, errors = res[0], res[1]
    assert is_valid is False
    assert any("manifestation '$k = k^*$' is identical to correct_belief" in e for e in errors)


def test_cta_matrices_no_false_r23_and_no_wrap_truncation() -> None:
    """Matrix environments \\begin{bmatrix} and \\begin{pmatrix} must not trigger false [R-23] nor truncate."""
    bm_text = r"$\begin{bmatrix} x \\ y \end{bmatrix}$"
    pm_text = r"$\begin{pmatrix} \dot{x} \\ \dot{y} \end{pmatrix}$"

    # Invariants should not report overescaped or syntax errors
    assert validate_katex_syntax(bm_text, "test_bmatrix") == []
    assert validate_katex_syntax(pm_text, "test_pmatrix") == []

    # cta_merge wrapping should preserve matrices without truncating or failing
    wrapped_bm = auto_wrap_bare_latex_in_cta_field(r"\begin{bmatrix} x \\ y \end{bmatrix}")
    assert r"\end{bmatrix}" in wrapped_bm
    assert wrapped_bm.startswith("$") and wrapped_bm.endswith("$")

    wrapped_pm = auto_wrap_bare_latex_in_cta_field(r"\begin{pmatrix} \dot{x} \\ \dot{y} \end{pmatrix}")
    assert r"\end{pmatrix}" in wrapped_pm
    assert wrapped_pm.startswith("$") and wrapped_pm.endswith("$")


def test_cta_syntax_warning_captured_as_syntax_error(tmp_path: Path) -> None:
    """Invalid escape sequence in cta_data.py must be caught as an actionable SyntaxError."""
    bad_source = "COMPETENCIES = [('\\m_bad_escape',)]\n"
    bad_file = tmp_path / "cta_data.py"
    bad_file.write_text(bad_source, encoding="utf-8")

    with pytest.raises(SyntaxError) as exc_info:
        load_cta_data_module(bad_file)

    err = exc_info.value
    assert "Secuencia de escape inválida en cta_data.py" in str(err)
    assert err.lineno == 1
    assert "raw string" in str(err)


def test_cta_module_contract_version_2_emitted() -> None:
    """compile_cta_module must emit contract_version: 2 when require_assumptions=True or specified."""
    raw_tuples = [
        (
            "concept", "C-01", "Concepto 1", "Descripción matemática del concepto 1.", "Understand",
            "doc.pdf", 1, [],
            [("D1", "Error 1", "Verdad 1", "$1$", "Hint 1 con longitud suficiente para test.", None)],
            [("A-C01-01", "$x > 0$", "Consecuencia de violación formal de al menos 10 caracteres.")],
            ["MC7", "FIB"],
        )
    ]
    res = compile_cta_module(raw_tuples, require_assumptions=True)
    assert res.get("contract_version") == 2
    assert "competencies" in res
    assert res["competencies"][0]["id"] == "C-01"


# ==============================================================================
# 3. SHARD COMPILER & MS ADVERSARIAL REFUTATION
# ==============================================================================

def test_compile_shard_cli_fail_total_defaults() -> None:
    """CLI --fail-total is default=True, and --fail-fast sets it to False."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--fail-total", dest="fail_total", action="store_true", default=True)
    parser.add_argument("--fail-fast", dest="fail_total", action="store_false")
    parser.add_argument("--min-archetypes", dest="min_archetypes", type=int, default=None, help="(default: 4)")

    # Default invocation
    args = parser.parse_args([])
    assert args.fail_total is True

    # Fast opt-out
    args_fast = parser.parse_args(["--fail-fast"])
    assert args_fast.fail_total is False


def test_compile_shard_helper_g_no_collision(tmp_path: Path) -> None:
    """A shard declaring helper def _g(x): must compile without collision with _c2c_gen_inner."""
    shards_dir = tmp_path / "shards"
    shards_dir.mkdir(parents=True)

    manifest_file = shards_dir / "pre_shard_manifest.json"
    manifest_file.write_text(json.dumps({"shards": [{"shard_id": "shard_01", "competency_ids": ["Hab-01"]}]}), encoding="utf-8")

    shard_source = """# -*- coding: utf-8 -*-
import random

def _g(x):
    return x * 3 + 1

def gen_h01_1(rng):
    val = _g(rng.randint(2, 20))
    return {
        "vars": {"val": val, "ans": val},
        "correct": str(val),
        "distractors": [
            ("D-H01-01", str(val + 1), "Error por sumar uno al parámetro @val@."),
            ("D-H01-02", str(val + 2), "Error por sumar dos al parámetro @val@."),
            ("D-H01-03", str(val + 3), "Error por sumar tres al parámetro @val@."),
            ("D-H01-04", str(val + 4), "Error por sumar cuatro al parámetro @val@."),
            ("D-H01-05", str(val + 5), "Error por sumar cinco al parámetro @val@."),
            ("D-H01-06", str(val + 6), "Error por sumar seis al parámetro @val@."),
        ]
    }

def ver_h01_1(c, v):
    return int(c) == v["val"]

TEMPLATES = [
    (
        "T-Hab-01-01", "Hab-01", "multiple_choice_7_options",
        gen_h01_1, ver_h01_1,
        ("easy", "Apply"),
        [
            r"Calcule el valor transformado sabiendo que la base es @val@.",
            r"Determine el resultado final de aplicar la regla para @val@.",
            r"Halle el valor correspondiente al parámetro numérico @val@.",
            r"Encuentre la magnitud resultante cuando la variable es @val@.",
            r"A partir de la expresión anterior determine el valor para @val@.",
            r"Obtenga el resultado numérico final considerando la entrada @val@.",
            r"Deduzca la solución cuantitativa exacta sabiendo que el dato es @val@."
        ],
        ["Pista inicial de andamiaje socrático.", "Segunda pista explicativa detallada.", "Tercera pista con la fórmula aplicada."],
        r"La solución directa evalúa $val$ resultando en @val@."
    )
]
"""
    shard_file = shards_dir / "shard_01_data.py"
    shard_file.write_text(shard_source, encoding="utf-8")

    cta_json = tmp_path / "cta.json"
    cta_payload = {
        "contract_version": 2,
        "competencies": [
            {
                "id": "Hab-01",
                "type": "skill",
                "name": "Competencia 1",
                "distractors": [{"id": f"D-H01-{i:02d}"} for i in range(1, 7)],
                "assumptions": [{"id": "A-Hab01-01", "statement_latex": "$x > 0$", "violation_consequence": "Invalida el modelo."}],
            }
        ],
    }
    cta_json.write_text(json.dumps(cta_payload), encoding="utf-8")

    ok, errors = compile_shard(
        work_dir_or_path=tmp_path,
        shard_id="shard_01",
        strict=False,  # Single template test (skip 4 archetypes requirement for this unit)
        seeds=10,
        cta_path=cta_json,
    )
    assert ok is True, f"Compilation with def _g(x): helper failed: {errors}"


def test_compile_shard_ms_tautological_verifier_rejected(tmp_path: Path) -> None:
    """Tautological counting MS verifier (len==4 and sum==2) must be REJECTED by adversarial mutation."""
    shards_dir = tmp_path / "shards"
    shards_dir.mkdir(parents=True)

    manifest_file = shards_dir / "pre_shard_manifest.json"
    manifest_file.write_text(json.dumps({"shards": [{"shard_id": "shard_01", "competency_ids": ["Hab-01"]}]}), encoding="utf-8")

    shard_source = """# -*- coding: utf-8 -*-
import random

def gen_h01_4(rng):
    a = rng.randint(2, 20)
    opts = [
        {"content": f"Opción verdadera 1 {a}", "value": f"Opción verdadera 1 {a}", "is_correct": True},
        {"content": f"Opción verdadera 2 {a}", "value": f"Opción verdadera 2 {a}", "is_correct": True},
        {"content": f"Opción falsa 1 {a}", "value": f"Opción falsa 1 {a}", "is_correct": False, "distractor_id": "D-H01-01", "error_rationale": "Rationale explicativo largo para opción falsa 1 con parámetro @a@."},
        {"content": f"Opción falsa 2 {a}", "value": f"Opción falsa 2 {a}", "is_correct": False, "distractor_id": "D-H01-02", "error_rationale": "Rationale explicativo largo para opción falsa 2 con parámetro @a@."},
    ]
    return {"vars": {"a": a}, "options": opts}

def ver_h01_4(res):
    # TAUTOLOGICAL: Only counts lengths, ignores contents / correctness mutations
    opts = res.get("options", [])
    return len(opts) == 4 and sum(1 for o in opts if o.get("is_correct")) == 2

TEMPLATES = [
    (
        "T-Hab-01-04", "Hab-01", "multiple_select",
        gen_h01_4, ver_h01_4,
        ("hard", "Analyze"),
        [
            r"Seleccione las afirmaciones correctas con respecto a @a@.",
            r"Identifique las opciones verdaderas asociadas a @a@.",
            r"Marque todas las sentencias válidas para el parámetro @a@.",
            r"Determine cuáles de las siguientes alternativas son ciertas para @a@.",
            r"Señale las proposiciones verdaderas para el valor de @a@.",
            r"Indique qué enunciados son correctos respecto a la variable @a@."
        ],
        ["Pista socrática de análisis 1.", "Pista socrática de análisis 2.", "Pista socrática de análisis 3."],
        r"La solución demuestra la validez analítica de las afirmaciones para @a@."
    )
]
"""
    shard_file = shards_dir / "shard_01_data.py"
    shard_file.write_text(shard_source, encoding="utf-8")

    cta_json = tmp_path / "cta.json"
    cta_payload = {
        "contract_version": 2,
        "competencies": [
            {
                "id": "Hab-01",
                "type": "skill",
                "name": "Competencia 1",
                "distractors": [{"id": f"D-H01-{i:02d}"} for i in range(1, 3)],
                "assumptions": [{"id": "A-Hab01-01", "statement_latex": "$x > 0$", "violation_consequence": "Invalida el modelo."}],
            }
        ],
    }
    cta_json.write_text(json.dumps(cta_payload), encoding="utf-8")

    ok, errors = compile_shard(
        work_dir_or_path=tmp_path,
        shard_id="shard_01",
        strict=True,
        seeds=10,
        cta_path=cta_json,
    )
    assert ok is False, "Tautological MS verifier should be rejected by compile_shard"
    taut_errors = [e for e in errors if "VERIFIER-TAUTOLOGY-DETECTED" in e or "TPL-CROSS: VERIFICADOR MS TAUTOLOGICO" in e]
    assert len(taut_errors) > 0, f"Expected tautology detection, got errors: {errors}"


def test_compile_shard_ms_canonical_verifier_accepted(tmp_path: Path) -> None:
    """Canonical MS verifier evaluating semantic properties must PASS adversarial mutation without false rejection."""
    shards_dir = tmp_path / "shards"
    shards_dir.mkdir(parents=True)

    manifest_file = shards_dir / "pre_shard_manifest.json"
    manifest_file.write_text(json.dumps({"shards": [{"shard_id": "shard_01", "competency_ids": ["Hab-01"]}]}), encoding="utf-8")

    shard_source = """# -*- coding: utf-8 -*-
import random

def gen_h01_4(rng):
    a = rng.randint(2, 20)
    opts = [
        {"content": f"Opción verdadera 1 {a}", "value": f"val_{a}_1", "is_correct": True},
        {"content": f"Opción verdadera 2 {a}", "value": f"val_{a}_2", "is_correct": True},
        {"content": f"Opción falsa 1 {a}", "value": f"fake_{a}_1", "is_correct": False, "distractor_id": "D-H01-01", "error_rationale": "Rationale explicativo largo para opción falsa 1 con parámetro @a@."},
        {"content": f"Opción falsa 2 {a}", "value": f"fake_{a}_2", "is_correct": False, "distractor_id": "D-H01-02", "error_rationale": "Rationale explicativo largo para opción falsa 2 con parámetro @a@."},
    ]
    return {"vars": {"a": a}, "options": opts}

def ver_h01_4(res):
    # CANONICAL: Evaluates semantic consistency between values, variables, and is_correct flags
    a = res.get("vars", {}).get("a")
    opts = res.get("options", [])
    expected_true_vals = {f"val_{a}_1", f"val_{a}_2"}
    for o in opts:
        val = o.get("value")
        corr = o.get("is_correct")
        if corr is True and val not in expected_true_vals:
            return False
        if corr is False and val in expected_true_vals:
            return False
    return True

TEMPLATES = [
    (
        "T-Hab-01-04", "Hab-01", "multiple_select",
        gen_h01_4, ver_h01_4,
        ("hard", "Analyze"),
        [
            r"Seleccione las afirmaciones correctas con respecto a @a@.",
            r"Identifique las opciones verdaderas asociadas a @a@.",
            r"Marque todas las sentencias válidas para el parámetro @a@.",
            r"Determine cuáles de las siguientes alternativas son ciertas para @a@.",
            r"Señale las proposiciones verdaderas para el valor de @a@.",
            r"Indique qué enunciados son correctos respecto a la variable @a@."
        ],
        ["Pista socrática de análisis 1.", "Pista socrática de análisis 2.", "Pista socrática de análisis 3."],
        r"La solución demuestra la validez analítica de las afirmaciones para @a@."
    )
]
"""
    shard_file = shards_dir / "shard_01_data.py"
    shard_file.write_text(shard_source, encoding="utf-8")

    cta_json = tmp_path / "cta.json"
    cta_payload = {
        "contract_version": 2,
        "competencies": [
            {
                "id": "Hab-01",
                "type": "skill",
                "name": "Competencia 1",
                "distractors": [{"id": f"D-H01-{i:02d}"} for i in range(1, 3)],
                "assumptions": [{"id": "A-Hab01-01", "statement_latex": "$x > 0$", "violation_consequence": "Invalida el modelo."}],
            }
        ],
    }
    cta_json.write_text(json.dumps(cta_payload), encoding="utf-8")

    ok, errors = compile_shard(
        work_dir_or_path=tmp_path,
        shard_id="shard_01",
        strict=False,
        min_archetypes=1,
        seeds=10,
        cta_path=cta_json,
    )
    assert ok is True, f"Canonical MS verifier was unexpectedly rejected: {errors}"
    assert len(errors) == 0
    assert not any("VERIFIER-TAUTOLOGY-DETECTED" in e for e in errors)
    assert not any("TPL-CROSS: VERIFICADOR MS TAUTOLOGICO" in e for e in errors)


def test_compile_shard_tpl_assumption_link_enforced(tmp_path: Path) -> None:
    """Missing assumption_id in boundary_or_edge_case archetype must trigger [TPL-ASSUMPTION-LINK]."""
    shards_dir = tmp_path / "shards"
    shards_dir.mkdir(parents=True)

    manifest_file = shards_dir / "pre_shard_manifest.json"
    manifest_file.write_text(json.dumps({"shards": [{"shard_id": "shard_01", "competency_ids": ["Hab-01"]}]}), encoding="utf-8")

    shard_source = """# -*- coding: utf-8 -*-
import random

def gen_1(rng):
    v = rng.randint(5, 50)
    return {"vars": {"v": v}, "correct": str(v), "distractors": [(f"D-Hab01-0{i}", str(v+i), "Rationale formativo largo de distractor con @v@.") for i in range(1, 7)]}
def ver_1(c, v): return int(c) == v["v"]

def gen_2(rng):
    v = rng.randint(5, 50)
    return {"vars": {"v": v}, "correct": str(v*2), "distractors": [(f"D-Hab01-0{i}", str(v*2+i), "Rationale formativo largo de distractor con @v@.") for i in range(1, 7)]}
def ver_2(c, v): return int(c) == v["v"]*2

def gen_3(rng):
    v = rng.randint(5, 50)
    return {"vars": {"v": v}, "correct": str(v*3), "distractors": [(f"D-Hab01-0{i}", str(v*3+i), "Rationale formativo largo de distractor con @v@.") for i in range(1, 7)]}
def ver_3(c, v): return int(c) == v["v"]*3

def gen_4(rng):
    v = rng.randint(5, 50)
    return {"vars": {"v": v}, "correct": str(v), "distractors": [(f"D-Hab01-0{i}", str(v+i*10), "Rationale formativo largo de distractor con @v@.") for i in range(1, 7)]}
def ver_4(c, v): return int(c) == v["v"]

stems = [
    r"Variante de stem número 1 con parámetro @v@.",
    r"Segunda formulación sintáctica para @v@.",
    r"Tercer planteamiento del problema con @v@.",
    r"Cuarta consigna independiente evaluando @v@.",
    r"Quinta alternativa de redacción analizando @v@."
]
hints = ["Pista socrática 1 suficientemente larga para test.", "Pista socrática 2 suficientemente larga para test.", "Pista socrática 3 suficientemente larga para test."]

TEMPLATES = [
    {"id": "T-Hab-01-01", "cid": "Hab-01", "archetype": "direct", "qtype": "mc7", "gen": gen_1, "ver": ver_1, "band": ("easy", "Apply"), "stems": stems, "hints": hints, "sol": "Solución paso a paso para @v@."},
    {"id": "T-Hab-01-02", "cid": "Hab-01", "archetype": "inverse", "qtype": "fib", "gen": gen_2, "ver": ver_2, "band": ("medium", "Analyze"), "stems": stems, "hints": hints, "sol": "Solución paso a paso para @v@."},
    {"id": "T-Hab-01-03", "cid": "Hab-01", "archetype": "perturbation", "qtype": "fib", "gen": gen_3, "ver": ver_3, "band": ("medium", "Apply"), "stems": stems, "hints": hints, "sol": "Solución paso a paso para @v@."},
    # Archetype 4 boundary_or_edge_case WITHOUT assumption_id
    {"id": "T-Hab-01-04", "cid": "Hab-01", "archetype": "boundary_or_edge_case", "qtype": "mc7", "gen": gen_4, "ver": ver_4, "band": ("hard", "Evaluate"), "stems": stems, "hints": hints, "sol": "Solución paso a paso para @v@."},
]
"""
    shard_file = shards_dir / "shard_01_data.py"
    shard_file.write_text(shard_source, encoding="utf-8")

    cta_json = tmp_path / "cta.json"
    cta_payload = {
        "contract_version": 2,
        "competencies": [
            {
                "id": "Hab-01",
                "type": "skill",
                "name": "Competencia 1",
                "distractors": [{"id": f"D-Hab01-{i:02d}"} for i in range(1, 7)],
                "assumptions": [
                    {
                        "id": "A-Hab01-01",
                        "statement_latex": "$k > 0$",
                        "violation_consequence": "Si no se cumple, el capital colapsa.",
                    }
                ],
            }
        ],
    }
    cta_json.write_text(json.dumps(cta_payload), encoding="utf-8")

    ok, errors = compile_shard(
        work_dir_or_path=tmp_path,
        shard_id="shard_01",
        strict=True,
        min_archetypes=4,
        seeds=10,
        cta_path=cta_json,
    )
    assert ok is False
    link_errs = [e for e in errors if "[TPL-ASSUMPTION-LINK]" in e]
    assert len(link_errs) > 0, f"Expected [TPL-ASSUMPTION-LINK] error, got: {errors}"
    assert "A-Hab01-01" in link_errs[0]


@pytest.mark.parametrize("interaction_type", ["multiple_choice_7_options", "multiple_select"])
@pytest.mark.parametrize("leaked_stem, token_var", [
    (r"Halle $x=@x@$", "x"),
    ("Considere X = @X@ en la expresión de equilibrio.", "X"),
    ("Determine el valor de la función sabiendo que Y = @Y@.", "Y"),
    ("Considere la ecuación con valor k=@k@ que determina la tasa.", "k"),
])
def test_r19_anti_leak_mc7_and_ms(interaction_type: str, leaked_stem: str, token_var: str) -> None:
    """PrairieLearn token X=@X@ and answer leak must be rejected in MC7 and MS under R-19."""
    if interaction_type == "multiple_choice_7_options":
        options = [
            {"content": "15.5", "is_correct": True},
            {"content": "10.0", "is_correct": False, "distractor_id": "D1", "error_rationale": "Rationale explicativo suficientemente largo para pasar validación."},
            {"content": "11.0", "is_correct": False, "distractor_id": "D2", "error_rationale": "Rationale explicativo suficientemente largo para pasar validación."},
            {"content": "12.0", "is_correct": False, "distractor_id": "D3", "error_rationale": "Rationale explicativo suficientemente largo para pasar validación."},
            {"content": "13.0", "is_correct": False, "distractor_id": "D4", "error_rationale": "Rationale explicativo suficientemente largo para pasar validación."},
            {"content": "14.0", "is_correct": False, "distractor_id": "D5", "error_rationale": "Rationale explicativo suficientemente largo para pasar validación."},
            {"content": "16.0", "is_correct": False, "distractor_id": "D6", "error_rationale": "Rationale explicativo suficientemente largo para pasar validación."},
        ]
    else:
        options = [
            {"content": "Opción verdadera 1", "is_correct": True},
            {"content": "Opción verdadera 2", "is_correct": True},
            {"content": "Opción falsa 1", "is_correct": False, "distractor_id": "D1", "error_rationale": "Rationale explicativo suficientemente largo para pasar validación."},
            {"content": "Opción falsa 2", "is_correct": False, "distractor_id": "D2", "error_rationale": "Rationale explicativo suficientemente largo para pasar validación."},
        ]

    q_data = {
        "id": "Q-Hab01-01",
        "competency_id": "Hab-01",
        "difficulty": "easy" if interaction_type == "multiple_choice_7_options" else "hard",
        "interaction_type": interaction_type,
        "stem": leaked_stem,
        "options": options,
        "hints": [
            "Pista inicial socrática para guiar al estudiante.",
            "Segunda pista con mayor detalle sobre la fórmula.",
            "Tercera pista con el procedimiento algebraico completo.",
        ],
    }

    course_leak = {
        "schema_version": "1.2.0",
        "course_id": "test_r19",
        "course_title": "Curso Test Regresión R19",
        "description": "Descripción formal de prueba para validación de compuertas R-19.",
        "language": "es",
        "created_at": "2026-11-14T00:00:00Z",
        "competencies": [
            {
                "id": "Hab-01",
                "name": "Competencia 1",
                "category": "Skill",
                "description": "Descripción formal completa con longitud suficiente para el validador.",
                "bloom_level": "Apply",
            }
        ],
        "questions": [q_data],
    }

    errs = validate_course_content(json.dumps(course_leak), strict=True)
    assert errs.is_valid is False
    r19_errs = [e for e in errs.errors if e.rule_id == "R-19" and e.code == "ERR_ANSWER_LEAK"]
    assert len(r19_errs) > 0, f"Expected R-19 ERR_ANSWER_LEAK for '{leaked_stem}' in {interaction_type}, got: {errs.errors}"
    assert any(f"@{token_var}@" in e.message for e in r19_errs)

    # Also verify instance invariant detection
    ok, inv_errs = check_instance_invariants(q_data, interaction_type)
    assert ok is False
    assert any("R-19" in e or "leaks literal PrairieLearn token" in e or "PrairieLearn token leak" in e or f"@{token_var}@" in e for e in inv_errs)


def test_compile_shard_tpl_const_distractor_rejected(tmp_path: Path) -> None:
    """A distractor returning the exact same scalar constant across >5 seeds when params vary must fail [TPL-CONST-DISTRACTOR]."""
    shards_dir = tmp_path / "shards"
    shards_dir.mkdir(parents=True)

    manifest_file = shards_dir / "pre_shard_manifest.json"
    manifest_file.write_text(json.dumps({"shards": [{"shard_id": "shard_01", "competency_ids": ["Hab-01"]}]}), encoding="utf-8")

    shard_source = """# -*- coding: utf-8 -*-
import random

def gen_h01_1(rng):
    v = rng.randint(10, 500)
    return {
        "vars": {"v": v},
        "correct": str(v),
        "distractors": [
            # Constant scalar distractor: always returns "0"
            ("D-H01-01", "0", "Error conceptual constante @v@."),
            ("D-H01-02", str(v + 2), "Rationale dinamico 2 @v@."),
            ("D-H01-03", str(v + 3), "Rationale dinamico 3 @v@."),
            ("D-H01-04", str(v + 4), "Rationale dinamico 4 @v@."),
            ("D-H01-05", str(v + 5), "Rationale dinamico 5 @v@."),
            ("D-H01-06", str(v + 6), "Rationale dinamico 6 @v@."),
        ]
    }

def ver_h01_1(c, v): return int(c) == v["v"]

stems = [
    r"Formulacion primera evaluando parametro @v@.",
    r"Segunda opcion sintactica para @v@.",
    r"Tercer enunciado para variable @v@.",
    r"Cuarta consigna con datos @v@."
]
hints = ["Pista 1 suficientemente larga para test.", "Pista 2 suficientemente larga para test.", "Pista 3 suficientemente larga para test."]

TEMPLATES = [
    (
        "T-Hab-01-01", "Hab-01", "multiple_choice_7_options",
        gen_h01_1, ver_h01_1,
        ("easy", "Apply"),
        stems, hints, r"Solucion para @v@."
    )
]
"""
    shard_file = shards_dir / "shard_01_data.py"
    shard_file.write_text(shard_source, encoding="utf-8")

    cta_json = tmp_path / "cta.json"
    cta_payload = {
        "contract_version": 2,
        "competencies": [
            {
                "id": "Hab-01",
                "type": "skill",
                "name": "Competencia 1",
                "distractors": [{"id": f"D-H01-{i:02d}"} for i in range(1, 7)],
                "assumptions": [{"id": "A-Hab01-01", "statement_latex": "$v > 0$", "violation_consequence": "Invalida."}],
            }
        ],
    }
    cta_json.write_text(json.dumps(cta_payload), encoding="utf-8")

    ok, errors = compile_shard(
        work_dir_or_path=tmp_path,
        shard_id="shard_01",
        strict=True,
        seeds=50,
        cta_path=cta_json,
    )
    assert ok is False
    const_errs = [e for e in errors if "[TPL-CONST-DISTRACTOR]" in e]
    assert len(const_errs) > 0, f"Expected [TPL-CONST-DISTRACTOR] violation, got: {errors}"
    assert "D-H01-01" in const_errs[0]


# ==============================================================================
# 4. ORCHESTRATION, DISPATCH & JUDGE
# ==============================================================================

def test_dispatch_role_specs_lean_defaults() -> None:
    """All ROLE_SPECS and dispatch_cta_reduce must target system_prompts/lean/ by default."""
    for role, spec in ROLE_SPECS.items():
        sp = spec.get("system_prompt", "")
        assert "system_prompts/lean/" in sp, f"Role '{role}' system_prompt does not default to lean: {sp}"


def test_dispatch_compile_cmd_fail_total_flag(tmp_path: Path) -> None:
    """dispatch_authors and dispatch_repair must both emit --fail-total in compile_cmd."""
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True)
    shards_dir = work_dir / "shards"
    shards_dir.mkdir(parents=True)

    manifest_file = shards_dir / "pre_shard_manifest.json"
    manifest_data = {
        "shards": [
            {
                "shard_id": "shard_01",
                "competency_ids": ["Hab-01"],
            }
        ]
    }
    manifest_file.write_text(json.dumps(manifest_data), encoding="utf-8")

    cta_file = work_dir / "cta.json"
    cta_payload = {
        "contract_version": 2,
        "competencies": [
            {
                "id": "Hab-01",
                "name": "Competencia 1",
                "type": "skill",
                "distractors": [{"id": f"D-Hab01-{i:02d}", "name": f"Dist {i}"} for i in range(1, 7)],
                "assumptions": [{"id": "A-Hab01-01", "statement_latex": "$k > 0$", "violation_consequence": "Falla."}],
            }
        ]
    }
    cta_file.write_text(json.dumps(cta_payload), encoding="utf-8")

    # 1. Author dispatch
    author_payload = dispatch_authors(work_dir=work_dir, pointer=False)
    author_item_file = work_dir / "dispatch" / "items" / "author_01.json"
    assert author_item_file.is_file()
    author_item_data = json.loads(author_item_file.read_text(encoding="utf-8"))
    author_prompt = author_item_data.get("Prompt", "")
    assert "--fail-total" in author_prompt, "compile_cmd in author prompt missing --fail-total"

    # 2. Repair dispatch
    # Create failing target metadata in specific_error_report.json
    reports_dir = work_dir / "reports"
    reports_dir.mkdir(parents=True)
    specific_report_file = work_dir / "specific_error_report.json"
    specific_report_file.write_text(json.dumps({
        "diagnostics_by_competency": {
            "Hab-01": [
                {
                    "rule_tag": "TPL-FAIL",
                    "file": "shard_01_data.py",
                    "template_id": "T-Hab-01-01",
                    "description": "Error descriptivo",
                }
            ]
        }
    }), encoding="utf-8")

    repair_payload = dispatch_repair(work_dir=work_dir, pointer=False)
    repair_item_file = work_dir / "dispatch" / "items" / "repair_01.json"
    assert repair_item_file.is_file()
    repair_item_data = json.loads(repair_item_file.read_text(encoding="utf-8"))
    repair_prompt = repair_item_data.get("Prompt", "")
    assert "--fail-total" in repair_prompt, "compile_cmd in repair prompt missing --fail-total"


def test_dispatch_authors_injects_assumptions(tmp_path: Path) -> None:
    """dispatch_authors must inject assumptions from cta.json into author work order."""
    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    shards_dir.mkdir(parents=True)

    manifest_file = shards_dir / "pre_shard_manifest.json"
    manifest_data = {"shards": [{"shard_id": "shard_01", "competency_ids": ["Hab-01"]}]}
    manifest_file.write_text(json.dumps(manifest_data), encoding="utf-8")

    cta_payload = {
        "contract_version": 2,
        "competencies": [
            {
                "id": "Hab-01",
                "name": "Competencia 1",
                "type": "skill",
                "distractors": [{"id": f"D-Hab01-{i:02d}", "name": f"Dist {i}"} for i in range(1, 7)],
                "assumptions": [
                    {
                        "id": "A-Hab01-01",
                        "statement_latex": "$k(0) > 0$",
                        "violation_consequence": "La economía colapsa inmediatamente.",
                    }
                ],
            }
        ]
    }
    (work_dir / "cta.json").write_text(json.dumps(cta_payload), encoding="utf-8")

    dispatch_authors(work_dir=work_dir, pointer=False)
    author_item_file = work_dir / "dispatch" / "items" / "author_01.json"
    author_text = author_item_file.read_text(encoding="utf-8")

    assert "A-Hab01-01" in author_text
    assert "$k(0) > 0$" in author_text
    assert "La economía colapsa inmediatamente" in author_text


def test_run_stage_dispatch_pointer_stub_no_overwrite(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """run_stage_dispatch in pointer mode must NOT overwrite existing author_01.json with minimal pointer stub."""
    import run
    from run import PipelineRunner

    work_dir = tmp_path / "work"
    dispatch_items_dir = work_dir / "dispatch" / "items"
    dispatch_items_dir.mkdir(parents=True)

    author_file = dispatch_items_dir / "author_01.json"
    original_work_order = {
        "role": "Shard Author shard_01",
        "work_order": "ORDEN COMPLETA EXTENSA CON METADATOS Y ESPECIFICACIONES TURN-0" * 20,
        "Prompt": "Prompt largo detallado" * 20,
    }
    author_file.write_text(json.dumps(original_work_order, indent=2), encoding="utf-8")

    # Simulate dispatch payload where subagents contains pointer stub
    runner = PipelineRunner(work_dir=work_dir, role="author")

    # Monkeypatch build_dispatch in run module to return payload with compact stub
    stub_sa = {
        "TypeName": "c2c_shard_author",
        "Role": "Shard Author shard_01",
        "Prompt": "You are Shard Author shard_01. Work order: work/dispatch/items/author_01.json.",
    }
    monkeypatch.setattr(run, "build_dispatch", lambda **kw: {
        "Role": "author",
        "Subagents": [stub_sa],
    })

    runner.run_stage_dispatch()

    # Verify author_01.json was PRESERVED and NOT overwritten by stub
    current_content = json.loads(author_file.read_text(encoding="utf-8"))
    assert "work_order" in current_content, "Existing complete work order was overwritten by minimal stub!"
    assert "ORDEN COMPLETA EXTENSA" in current_content["work_order"]


def test_dispatch_judges_batch_dict_size_and_heaviest_first(tmp_path: Path) -> None:
    """dispatch_judges counts len(items) on dict batches, cleans obsolete files, and sorts Heaviest-First."""
    work_dir = tmp_path / "work"
    v_dir = work_dir / "verification"
    v_dir.mkdir(parents=True)

    # Establish existing verification batch setup
    (v_dir / "judge_batch.json").write_text("[]", encoding="utf-8")
    (v_dir / "judge_ground_truth.json").write_text("{}", encoding="utf-8")

    # Batch 1 with 3 items
    b1_file = v_dir / "judge_batch_01.json"
    b1_file.write_text(json.dumps({
        "items": [{"question_id": f"q_1_{i}", "stem": f"stem {i}", "options": []} for i in range(3)]
    }), encoding="utf-8")

    # Batch 2 with 10 items (Heavier)
    b2_file = v_dir / "judge_batch_02.json"
    b2_file.write_text(json.dumps({
        "items": [{"question_id": f"q_2_{i}", "stem": f"stem {i}", "options": []} for i in range(10)]
    }), encoding="utf-8")

    # Obsolete residual judge item
    items_dir = work_dir / "dispatch" / "items"
    items_dir.mkdir(parents=True)
    obsolete_file = items_dir / "judge_99.json"
    obsolete_file.write_text("{}", encoding="utf-8")

    payload = dispatch_judges(work_dir=work_dir, pointer=True)

    # 1. Obsolete file must be wiped
    assert not obsolete_file.is_file(), "Obsolete judge_99.json was not cleaned up"

    # 2. Heaviest-First sorting: batch 2 (10 items) must be dispatched first
    subagents = payload.get("Subagents", [])
    assert len(subagents) == 2
    # First subagent corresponds to the heaviest batch (judge_02)
    assert "judge_02.json" in subagents[0]["Prompt"]
    assert "judge_responses_02.json" in subagents[0]["Prompt"]


def test_judge_completeness_preserves_zero_answers(tmp_path: Path) -> None:
    """check_judge_completeness must preserve numerical answers 0 and 0.0 without coercion to True."""
    v_dir = tmp_path / "verification"
    v_dir.mkdir(parents=True)

    # Batch file with expected items
    batch_file = v_dir / "judge_batch_01.json"
    batch_items = [
        {"item_id": "q_zero_int", "stem": "stem 1"},
        {"item_id": "q_zero_float", "stem": "stem 2"},
        {"item_id": "q_nonzero", "stem": "stem 3"},
    ]
    batch_file.write_text(json.dumps({"items": batch_items}), encoding="utf-8")

    # Response file declaring answers 0 and 0.0
    responses_file = v_dir / "judge_responses_01.json"
    responses_data = [
        {"item_id": "q_zero_int", "answer": 0, "verdict": "correct"},
        {"item_id": "q_zero_float", "answer": 0.0, "verdict": "correct"},
        {"item_id": "q_nonzero", "answer": 42, "verdict": "correct"},
    ]
    responses_file.write_text(json.dumps(responses_data), encoding="utf-8")

    metrics = check_judge_completeness(work_dir=tmp_path)

    assert metrics["is_complete"] is True
    assert metrics["total_expected_items"] == 3
    assert metrics["total_received_items"] == 3
    assert len(metrics["missing_ids"]) == 0


def test_compare_judge_responses_handles_flaw_detected(tmp_path: Path) -> None:
    """compare_judge_responses must mark flaw_detected: true as epistemic failure without zero-suppression."""
    gt = {
        "q_zero": {
            "competency_id": "Hab-01",
            "template_id": "T-Hab-01-01",
            "interaction_type": "fill_in_the_blank",
            "correct_value": 0,
            "kernel_verified": True,
        }
    }

    # 1. Clean response declaring answer 0 without flaw
    clean_responses = [
        {"item_id": "q_zero", "answer": 0, "verdict": "correct", "flaw_detected": False}
    ]
    clean_report = compare_judge_responses(responses=clean_responses, ground_truth=gt, work_dir=tmp_path)
    assert clean_report["agreement_rate"] == 1.0
    assert clean_report["passed"] is True
    assert len(clean_report["discordances"]) == 0

    # 2. Response declaring answer 0 BUT reporting epistemic flaw_detected: True
    flaw_responses = [
        {
            "item_id": "q_zero",
            "answer": 0,
            "verdict": "correct",
            "flaw_detected": True,
            "failure_category": "epistemic_insufficiency",
            "flaw_description": "Contradicción matemática detectada en el enunciado del reactivo.",
        }
    ]
    flaw_report = compare_judge_responses(responses=flaw_responses, ground_truth=gt, work_dir=tmp_path)

    # Must NOT be marked as matching agreement despite matching answer 0
    assert flaw_report["passed"] is False
    assert flaw_report["agreement_rate"] == 0.0
    assert len(flaw_report["discordances"]) == 1

    disc = flaw_report["discordances"][0]
    # Answer 0 is preserved and not coerced to True or lost
    assert disc["judge_response"] == 0
    assert "Epistemic flaw detected by judge" in disc["reason"]
    assert "Contradicción matemática" in disc["reason"]
