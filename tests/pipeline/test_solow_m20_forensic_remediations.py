"""Regression tests for the 6 forensic pipeline root causes from solow_m20_v1."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[2]
C2C_DIR = ROOT_DIR / ".agents" / "skills" / "content-to-course"
RUN_AUDITOR_DIR = ROOT_DIR / ".agents" / "skills" / "c2c-run-auditor" / "scripts"
QA_EVAL_DIR = ROOT_DIR / ".agents" / "skills" / "course-qa-evaluator" / "scripts"

for p in (C2C_DIR, RUN_AUDITOR_DIR, QA_EVAL_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))


# ---------------------------------------------------------------------------
# 1. check_cta.py & plan_shards.py: [CTA-MC7-DISTRACTORS]
# ---------------------------------------------------------------------------

def test_check_cta_rejects_mc7_with_fewer_than_6_distractors():
    import check_cta

    def _dist(i: int) -> dict:
        return {
            "id": f"D-C01-0{i}",
            "wrong_belief": f"Creencia errónea {i} suficientemente descriptiva",
            "omitted_step": f"Paso omitido {i}",
        }

    comp_bad = {
        "id": "C-01",
        "type": "concept",
        "distractors": [_dist(1), _dist(2), _dist(3)],
        "assumptions": [{"statement_latex": "$s \\in (0,1)$ constante.", "violation_consequence": "Cambia la trayectoria de equilibrio."}],
        "recommended_modalities": ["concept_matching", "adversarial_break", "multiple_choice_7_options"],
    }
    errs_bad = check_cta._validate_competencies_rules([comp_bad], require_assumptions=True, require_modalities=True)
    assert any("[CTA-MC7-DISTRACTORS]" in e for e in errs_bad), errs_bad

    comp_ok_6 = dict(comp_bad, distractors=[_dist(i) for i in range(1, 7)])
    errs_ok_6 = check_cta._validate_competencies_rules([comp_ok_6], require_assumptions=True, require_modalities=True)
    assert not any("[CTA-MC7-DISTRACTORS]" in e for e in errs_ok_6), errs_ok_6

    comp_ok_no_mc7 = dict(comp_bad, recommended_modalities=["concept_matching", "adversarial_break", "multiple_select"])
    errs_ok_no_mc7 = check_cta._validate_competencies_rules([comp_ok_no_mc7], require_assumptions=True, require_modalities=True)
    assert not any("[CTA-MC7-DISTRACTORS]" in e for e in errs_ok_no_mc7), errs_ok_no_mc7


def test_plan_shards_rejects_mc7_with_fewer_than_6_distractors(tmp_path: Path):
    import plan_shards

    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    shards_dir.mkdir(parents=True)

    (work_dir / "pre_cta_manifest.json").write_text(
        json.dumps({"course_id": "test_mc7", "files": [{"doc": "doc.pdf"}]}),
        encoding="utf-8",
    )
    cta_path = work_dir / "cta.json"
    cta_path.write_text(
        json.dumps({
            "course_id": "test_mc7",
            "competencies": [{
                "id": "C-01",
                "type": "concept",
                "name": "Concepto prueba",
                "distractors": [{"id": "D-C01-01"}, {"id": "D-C01-02"}, {"id": "D-C01-03"}],
                "recommended_modalities": ["concept_matching", "multiple_choice_7_options"],
            }],
        }),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match=r"CTA-MC7-DISTRACTORS"):
        plan_shards.plan_shards(cta_path, shards_dir)


# ---------------------------------------------------------------------------
# 2. compile_shard.py: cta.json overrides stale pre_shard_manifest.json
# ---------------------------------------------------------------------------

def test_compile_shard_cta_overrides_stale_manifest_modalities(tmp_path: Path):
    import compile_shard

    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    templates_dir = work_dir / "templates"
    shards_dir.mkdir(parents=True)
    templates_dir.mkdir(parents=True)

    stale_comp = {
        "id": "C-01",
        "type": "concept",
        "name": "Modelo básico",
        "recommended_modalities": ["fill_in_the_blank", "multiple_choice_7_options"],
        "distractors": [{"id": f"D-C01-0{i}", "wrong_belief": f"Error {i} descrito"} for i in range(1, 4)],
        "assumptions": [{"statement_latex": "$s \\in (0,1)$", "violation_consequence": "No converge"}],
    }
    fresh_comp = dict(stale_comp, recommended_modalities=["fill_in_the_blank"])

    (work_dir / "cta.json").write_text(
        json.dumps({"course_id": "test_sync", "contract_version": 2, "competencies": [fresh_comp]}),
        encoding="utf-8",
    )
    (shards_dir / "pre_shard_manifest.json").write_text(
        json.dumps({
            "course_id": "test_sync",
            "shards": [{
                "shard_id": "shard_01",
                "competency_ids": ["C-01"],
                "competencies": [stale_comp],
            }],
        }),
        encoding="utf-8",
    )

    shard_py = shards_dir / "shard_01_data.py"
    shard_py.write_text(
        r'''
def gen_c01_1(rng):
    s = rng.choice([3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
    k = rng.choice([3, 4, 5, 6])
    ans = str(s * k)
    return {
        "vars": {"s": s, "k": k, "ans": ans},
        "correct": ans,
        "distractors": [
            ("D-C01-01", str(s + k), "Se sumó s=@s@ con k=@k@ en lugar de multiplicar."),
            ("D-C01-02", str(s * k + 1), "Se añadió una unidad espuria al producto de @s@ y @k@."),
            ("D-C01-03", str(s * k + 2), "Se desplazó en dos unidades el equilibrio para @s@ y @k@."),
        ],
    }

def ver_c01_1(c, v):
    return int(str(c).strip()) == int(v["s"]) * int(v["k"])

TEMPLATES = [
    {
        "id": "T-C01-01",
        "cid": "C-01",
        "qtype": "fill_in_the_blank",
        "gen": gen_c01_1,
        "ver": ver_c01_1,
        "band": ("easy", "Apply"),
        "stems": [
            "Calcule $y = @s@ \\cdot @k@$ para estos valores.",
            "Determine el producto $y$ cuando $s=@s@$ y $k=@k@$.",
            "Obtenga la producción total con $s=@s@$ y $k=@k@$.",
        ],
        "hints": [
            "Identifica los dos factores dados en el enunciado inicial.",
            "Multiplica la tasa de ahorro por el acervo de capital dado.",
            "Verifica que la operación sea multiplicativa y no aditiva.",
        ],
        "sol": "El producto se obtiene multiplicando los factores dados: $@s@ \\cdot @k@ = @ans@$.",
    }
]
''',
        encoding="utf-8",
    )

    ok, errs = compile_shard.compile_shard(
        work_dir,
        "shard_01",
        strict=False,
        seeds=5,
        min_archetypes=1,
        templates_per_modality=1,
    )
    assert ok, f"Expected stale manifest MC7 to be overridden by cta.json, got errors: {errs}"


# ---------------------------------------------------------------------------
# 3. shard_precheck.py: [VER-SYMPY-ASSUMPTIONS]
# ---------------------------------------------------------------------------

def test_shard_precheck_flags_sympy_symbol_assumptions_with_sympify():
    import shard_precheck

    bad_src = '''
import sympy
def ver_h3_3(c, v):
    r_sym = sympy.Symbol("r", positive=True)
    expr = sympy.sympify(str(c))
    return sympy.simplify(expr - r_sym) == 0
'''
    bad_warnings = shard_precheck.precheck_source(bad_src)
    assert any("[VER-SYMPY-ASSUMPTIONS]" in w for w in bad_warnings), bad_warnings

    ok_with_locals = '''
import sympy
def ver_h3_3(c, v):
    r_sym = sympy.Symbol("r", positive=True)
    expr = sympy.sympify(str(c), locals={"r": r_sym})
    return sympy.simplify(expr - r_sym) == 0
'''
    assert not any("[VER-SYMPY-ASSUMPTIONS]" in w for w in shard_precheck.precheck_source(ok_with_locals))

    ok_no_assump = '''
import sympy
def ver_h3_3(c, v):
    r_sym = sympy.Symbol("r")
    expr = sympy.sympify(str(c))
    return sympy.simplify(expr - r_sym) == 0
'''
    assert not any("[VER-SYMPY-ASSUMPTIONS]" in w for w in shard_precheck.precheck_source(ok_no_assump))


# ---------------------------------------------------------------------------
# 4. engine/shard_compiler_steps.py: [TPL-ADJACENT-PLACEHOLDERS]
# ---------------------------------------------------------------------------

def test_shard_compiler_steps_rejects_adjacent_placeholders(tmp_path: Path):
    from engine.shard_compiler_steps import compile_tuple_records_to_templates
    from engine.shard_locator import ShardDataLineLocator

    src = 'TEMPLATES = []\n'
    f_path = tmp_path / "shard_01_data.py"
    f_path.write_text(src, encoding="utf-8")
    locator = ShardDataLineLocator(src)

    def _make_record(stem_text: str) -> dict:
        return {
            "tuple": {
                "id": "T-Hab-04-02",
                "cid": "Hab-04",
                "qtype": "fill_in_the_blank",
                "gen": "def gen(rng):\n    return {'vars': {'n': 0.064, 'b': 5}, 'correct': '0.6', 'distractors': []}",
                "ver": "def ver(c, v):\n    return True",
                "band": ("easy", "Apply"),
                "stems": [
                    stem_text,
                    "Variante alternativa con $n=@n@$ y $b=@b@$ para calcular $r$.",
                    "Tercera variante con $n=@n@$ y $b=@b@$ en equilibrio.",
                ],
                "hints": [
                    "Identifica los valores de la razón capital-trabajo en el enunciado.",
                    "Evalúa la razón de ahorro respecto a la tasa de crecimiento.",
                    "Expresa el porcentaje final en forma decimal redondeada.",
                ],
                "sol": "Calculamos el cociente usando los parámetros del enunciado.",
            },
            "locator": locator,
            "file_path": f_path,
            "orig_idx": 0,
        }

    errs_bad: list[str] = []
    res_bad = compile_tuple_records_to_templates(
        tuple_records=[_make_record("Existe exceso de capacidad en $r=0.4/(@n@@b@)$. Halle el valor.")],
        cta_comp_map={"Hab-04": {"id": "Hab-04", "type": "skill", "distractors": []}},
        strict=True,
        module_rats={},
        norm_shard_id="shard_01",
        templates_by_cid={},
        gen_callables_by_cid={},
        deferred_hints_dup_errors=[],
        deferred_verifier_errors=[],
        step5_err_fn=lambda msg: (errs_bad.append(msg), False)[1],
        fail_fn=lambda msg: (False, [msg]),
    )
    assert res_bad is None or res_bad[0] is False
    assert any("[TPL-ADJACENT-PLACEHOLDERS]" in e for e in errs_bad), errs_bad


# ---------------------------------------------------------------------------
# 5. engine/invariants.py: [TPL-KATEX-SYMPY-LEAK]
# ---------------------------------------------------------------------------

def test_invariants_validate_katex_flags_sympy_leak_without_false_positives():
    from engine.invariants import validate_katex_syntax

    bad_errs = validate_katex_syntax(
        "La derivada de equilibrio es $2.8*sqrt(k)-0.08*k$ en estado estacionario.",
        "detailed_solution",
    )
    assert any("[TPL-KATEX-SYMPY-LEAK]" in e for e in bad_errs), bad_errs

    good_errs = validate_katex_syntax(
        r"La derivada en $k^*$ es $2.8\sqrt{k}-0.08k$ y la tasa $r^*$ satisface $f^*(k)$.",
        "detailed_solution",
    )
    assert not any("[TPL-KATEX-SYMPY-LEAK]" in e for e in good_errs), good_errs


# ---------------------------------------------------------------------------
# 6. audit_engine.py: inline python -c work/ mutation detection
# ---------------------------------------------------------------------------

def test_audit_engine_detects_inline_shell_mutation_and_ignores_readonly():
    from audit_engine import ExecutionAuditor

    auditor = ExecutionAuditor([], "test-conv")
    records = [
        {
            "step_index": 69,
            "type": "PLANNER_RESPONSE",
            "created_at": "2026-11-19T20:16:29Z",
            "input_tokens": 100,
            "output_tokens": 50,
            "tool_calls": [{
                "name": "run_command",
                "args": {
                    "CommandLine": "& \".venv\\Scripts\\python.exe\" -c \"import json; d=json.load(open('courses/solow_m20_v1/work/cta.json')); print(len(d))\""
                },
            }],
        },
        {
            "step_index": 71,
            "type": "PLANNER_RESPONSE",
            "created_at": "2026-11-19T20:16:35Z",
            "input_tokens": 120,
            "output_tokens": 60,
            "tool_calls": [{
                "name": "run_command",
                "args": {
                    "CommandLine": "& \".venv\\Scripts\\python.exe\" -c \"import json; p='courses/solow_m20_v1/work/cta.json'; d=json.load(open(p)); json.dump(d, open(p,'w'))\""
                },
            }],
        },
        {
            "step_index": 72,
            "type": "GENERIC",
            "created_at": "2026-11-19T20:16:38Z",
        },
    ]

    interventions = auditor._extract_orchestrator_interventions(records)
    assert len(interventions) == 1
    assert interventions[0]["step"] == 71
    assert interventions[0]["file"] == "cta.json"
    assert interventions[0]["tool"] == "run_command"
    assert "Mutación Inline" in interventions[0]["action_type"]

    decomp = auditor._decompose_orchestrator_time(records, interventions)
    assert decomp["supervisor_repair_seconds"] == 3.0


# ---------------------------------------------------------------------------
# 7. standardized_audit_engine.py & prepare_course_payload.py
# ---------------------------------------------------------------------------

def test_qa_linter_detects_sympy_in_katex_and_payload_falls_back_to_raw_json(tmp_path: Path, monkeypatch):
    from standardized_audit_engine import KaTeXSyntaxLinter, LintIssue, run_full_audit
    import prepare_course_payload

    course = {
        "course_id": "sympy_katex_test",
        "title": "SymPy KaTeX Test",
        "competencies": [{"id": "Hab-01", "category": "Skill", "prerequisites": []}],
        "questions": [{
            "id": "Q-Hab01-031",
            "competency_id": "Hab-01",
            "interaction_type": "open_symbolic",
            "stem": "Encuentre la expresión de inversión neta.",
            "hints": ["Pista 1 suficiente", "Pista 2 suficiente", "Pista 3 suficiente"],
            "detailed_solution": "Sustituyendo los valores obtenemos $2.8*sqrt(k)-0.08*k$.",
        }],
    }
    issues: list[LintIssue] = []
    summary = KaTeXSyntaxLinter().run(course, issues)
    assert summary["sympy_in_katex_count"] == 1
    assert any("SymPy" in iss.message for iss in issues)

    tel = run_full_audit(course)
    assert "Q-Hab01-031" in tel["risk_clusters"]["sympy_in_katex"]

    # Raw JSON fallback when run_platform marks course as status="error" without "data"
    fake_courses_dir = tmp_path / "courses"
    fake_courses_dir.mkdir()
    (fake_courses_dir / "broken_schema.json").write_text(json.dumps(course), encoding="utf-8")
    monkeypatch.setattr(prepare_course_payload, "COURSES_DIR", fake_courses_dir)

    pkg = prepare_course_payload.summarize_course({
        "id": "broken_schema",
        "filename": "broken_schema.json",
        "title": "broken_schema",
        "status": "error",
        "error_message": "Invalid question type 'concept_matching'",
    })
    assert pkg["total_questions"] == 1
    assert pkg["total_competencies"] == 1
    assert pkg["platform_validation_error"] == "Invalid question type 'concept_matching'"
