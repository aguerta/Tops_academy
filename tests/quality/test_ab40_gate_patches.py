"""Comprehensive regression tests for A/B Testing 4.0 compiler and sanitizer gate patches."""

from __future__ import annotations

import json
import random
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

SKILL_DIR = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))


def _make_stems(var_token: str = "@k@", count: int = 12) -> List[str]:
    base_patterns = [
        f"Calcule el resultado analítico correspondiente al parámetro {var_token}:",
        f"Determine la magnitud exacta asociada a la entrada {var_token}:",
        f"Halle el valor estructural que satisface el modelo con {var_token}:",
        f"Obtenga la expresión evaluada cuando el dato inicial es {var_token}:",
        f"Evalúe rigurosamente la condición de equilibrio para {var_token}:",
        f"Deduzca la cantidad resultante partiendo del parámetro {var_token}:",
        f"Verifique cuál es el resultado válido al fijar la variable {var_token}:",
        f"Encuentre la solución numérica consistente con el nivel {var_token}:",
        f"Establezca el comportamiento del sistema cuando aparece {var_token}:",
        f"Compute la respuesta formal requerida bajo el supuesto de {var_token}:",
        f"Analice la relación lineal propuesta tomando como base {var_token}:",
        f"Identifique la cuantía final obtenida a partir del dato {var_token}:",
        f"Califique el efecto estructural inducido al imponer {var_token}:",
        f"Formule el cálculo operativo requerido para el caso con {var_token}:",
        f"Estime la salida numérica que corresponde al escenario de {var_token}:",
        f"Contraste el resultado teórico derivado de fijar {var_token}:",
        f"Resuelva la expresión cuantitativa dependiente de {var_token}:",
        f"Precise el valor resultante tras sustituir el término {var_token}:",
    ]
    return base_patterns[:count]


def _setup_shard_workspace(
    tmp_path: Path,
    cid: str = "C-01",
    ctype: str = "skill",
    assumptions: Optional[List[Dict[str, str]]] = None,
    with_cta: bool = True,
) -> tuple[Path, Path, Path, Optional[Path]]:
    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    templates_dir = work_dir / "templates"
    shards_dir.mkdir(parents=True, exist_ok=True)
    templates_dir.mkdir(parents=True, exist_ok=True)

    comp_obj: Dict[str, Any] = {
        "id": cid,
        "name": f"Competencia {cid} Analítica",
        "type": ctype,
        "description_latex": (
            f"Descripción analítica rigurosa de la competencia {cid} con ecuaciones formales y condiciones de equilibrio."
        ),
        "distractors": [
            {
                "id": f"D-{cid}-0{i}",
                "wrong_belief": f"Error conceptual {i} en cálculo analítico",
                "correct_belief": f"Procedimiento correcto {i} en cálculo analítico",
                "manifestation": f"Resultado desplazado en factor {i}",
                "remediation_hint": (
                    f"Revise cuidadosamente la relación algebraica correspondiente al paso {i} del procedimiento formal."
                ),
            }
            for i in range(1, 7)
        ],
    }
    if assumptions is not None:
        comp_obj["assumptions"] = assumptions

    cta_file: Optional[Path] = None
    if with_cta:
        cta_payload = {
            "course_id": "test_ab40_course",
            "title": "Test AB40 Course",
            "competencies": [comp_obj],
        }
        cta_file = work_dir / "cta.json"
        cta_file.write_text(json.dumps(cta_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    manifest_payload = {
        "shards": [
            {
                "shard_id": "shard_01",
                "competency_ids": [cid],
                "shard_data_path": str((shards_dir / "shard_01_data.py").resolve().as_posix()),
                "templates_dir": str(templates_dir.resolve().as_posix()),
                "competencies": [comp_obj] if with_cta else [],
            }
        ]
    }
    (shards_dir / "pre_shard_manifest.json").write_text(
        json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return work_dir, shards_dir, templates_dir, cta_file


def _make_schema_valid_cta_dict(
    description_latex: str,
    hint_override_first: Optional[str] = None,
    math_in_distractors: bool = False,
) -> Dict[str, Any]:
    default_hint = (
        "Considere cuidadosamente el factor de descuento desde $\\$1$ manteniendo las unidades correctas en cada término."
        if math_in_distractors
        else "Revise detalladamente la ecuación de equilibrio y contraste las magnitudes del modelo analítico formal."
    )
    distractors = []
    for i in range(1, 4):
        hint = hint_override_first if (i == 1 and hint_override_first is not None) else default_hint
        if math_in_distractors:
            wb = f"Confusión intertemporal {i} al evaluar flujo de \\$100 frente a $\\alpha + {i}$."
            cb = f"Valoración exacta {i} desde $\\$1$ descontando con tasa $i(t)h$."
            manif = f"Resultado erróneo de \\${100 + i} bajo tasa $r_{i}$."
        else:
            wb = f"Creencia errónea {i} sobre parámetro"
            cb = f"Creencia correcta {i} sobre parámetro"
            manif = f"Manifestación desplazada {i}"
        distractors.append(
            {
                "id": f"D-C01-0{i}",
                "name": f"Distractor {i}",
                "wrong_belief": wb,
                "correct_belief": cb,
                "trigger": f"Trigger {i}",
                "manifestation": manif,
                "error_type": "sign_error",
                "severity": "medium",
                "origin": "inferred",
                "evidence": {"doc": "doc.pdf", "page": 1},
                "remediation_hint": hint,
            }
        )
    return {
        "course_id": "ab40_cta_schema_test",
        "title": "AB40 CTA Schema Test",
        "competencies": [
            {
                "id": "C-01",
                "type": "concept",
                "name": "Competencia AB40",
                "description_latex": description_latex,
                "bloom": "Understand",
                "session": "Sesion 1",
                "unit_index": 1,
                "prerequisites": [],
                "evidence": [{"doc": "doc.pdf", "page": 1}],
                "distractors": distractors,
            }
        ],
    }


# ==============================================================================
# A. COMPILE_SHARD & CHECK_TEMPLATES GATE PATCHES
# ==============================================================================


class TestAB40ShardCompilerPatches:
    """Tests for P0/P1/P2 fixes in compile_shard.py and check_templates.py."""

    @pytest.mark.parametrize(
        "mode,should_pass",
        [
            ("strong", True),
            ("weak_c1_ignores_rationale", False),
            ("weak_c2_ignores_mutated_sentinel", False),
            ("weak_c3_accepts_false_latex_0eq1", False),
        ],
    )
    def test_ms_decoupled_mut_c1_c2_c3_compile_shard(self, tmp_path: Path, mode: str, should_pass: bool):
        """P0: Weak MS verifiers failing only one of mut_c1, mut_c2, or mut_c3 must be rejected."""
        from compile_shard import compile_shard

        work_dir, shards_dir, _, cta_file = _setup_shard_workspace(tmp_path / mode, cid="C-01", ctype="skill")
        shard_py = shards_dir / "shard_01_data.py"

        if mode == "strong":
            ver_body = '''
    v = res.get("vars", {})
    k = v.get("k")
    opts = res.get("options", [])
    if not isinstance(k, int) or len(opts) != 4:
        return False
    exp_t = {f"$x > {k}$", f"$x + 1 > {k}$"}
    if {o.get("value") for o in opts if o.get("is_correct") is True} != exp_t:
        return False
    exp_f = {f"$x < {k}$": "D-C-01-01", f"$x = {k - 1}$": "D-C-01-02"}
    return all(
        o.get("value") in exp_f
        and o.get("distractor_id") == exp_f[o.get("value")]
        and len(str(o.get("error_rationale") or "")) >= 20
        for o in opts if o.get("is_correct") is False
    )
'''
        elif mode == "weak_c1_ignores_rationale":
            ver_body = '''
    v = res.get("vars", {})
    k = v.get("k")
    opts = res.get("options", [])
    exp_t = {f"$x > {k}$", f"$x + 1 > {k}$"}
    if {o.get("value") for o in opts if o.get("is_correct") is True} != exp_t:
        return False
    exp_f = {f"$x < {k}$": "D-C-01-01", f"$x = {k - 1}$": "D-C-01-02"}
    return all(
        o.get("value") in exp_f and o.get("distractor_id") == exp_f[o.get("value")]
        for o in opts if o.get("is_correct") is False
    )
'''
        elif mode == "weak_c2_ignores_mutated_sentinel":
            ver_body = '''
    opts = res.get("options", [])
    t_vals = [str(o.get("value") or "") for o in opts if o.get("is_correct") is True]
    f_opts = [o for o in opts if o.get("is_correct") is False]
    if len(t_vals) != 2 or len(f_opts) != 2:
        return False
    if any(tv.strip() in ("$0 = 1$", "$1 = 2$") for tv in t_vals):
        return False
    return all(
        o.get("distractor_id") in {"D-C-01-01", "D-C-01-02"}
        and len(str(o.get("error_rationale") or "")) >= 20
        for o in f_opts
    )
'''
        else:  # weak_c3_accepts_false_latex_0eq1
            ver_body = '''
    opts = res.get("options", [])
    t_vals = [str(o.get("value") or "") for o in opts if o.get("is_correct") is True]
    f_opts = [o for o in opts if o.get("is_correct") is False]
    if len(t_vals) != 2 or len(f_opts) != 2:
        return False
    if any("__MUTATED__" in tv or not (tv.startswith("$") and tv.endswith("$")) for tv in t_vals):
        return False
    return all(
        o.get("distractor_id") in {"D-C-01-01", "D-C-01-02"}
        and len(str(o.get("error_rationale") or "")) >= 20
        for o in f_opts
    )
'''

        stems = _make_stems("@k@", count=16)
        shard_code = f'''
def gen_ms(rng):
    k = rng.randint(10, 600)
    return {{
        "vars": {{"k": k}},
        "options": [
            {{"value": f"$x > {{k}}$", "is_correct": True}},
            {{"value": f"$x + 1 > {{k}}$", "is_correct": True}},
            {{
                "value": f"$x < {{k}}$",
                "is_correct": False,
                "distractor_id": "D-C-01-01",
                "error_rationale": "Inversión del signo de desigualdad respecto al umbral numérico @k@.",
            }},
            {{
                "value": f"$x = {{k - 1}}$",
                "is_correct": False,
                "distractor_id": "D-C-01-02",
                "error_rationale": "Sustitución por igualdad estricta debajo de la cota mínima @k@.",
            }},
        ],
    }}

def ver_ms(res):
    if not isinstance(res, dict):
        return False
{ver_body}

stems = {stems!r}
hints = [
    "Compare el sentido de cada desigualdad frente a la cota dada.",
    "Verifique si sumar una unidad mantiene la desigualdad estricta.",
    "Contraste las opciones verdaderas frente a igualdades o sentidos opuestos.",
]
TEMPLATES = [
    (
        "T-C01-MS", "C-01", "multiple_select", gen_ms, ver_ms,
        ("medium", "Apply"), stems, hints,
        "Si el número supera al parámetro umbral @k@, al sumar uno también permanece estrictamente por encima.",
    ),
]
'''
        shard_py.write_text(shard_code, encoding="utf-8")
        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            seeds=20,
            cta_path=cta_file,
            min_archetypes=1,
        )
        if should_pass:
            assert success, f"Expected strong verifier to pass, got: {errors}"
        else:
            assert not success, f"Expected weak verifier mode={mode} to fail!"
            assert any("VERIFIER-TAUTOLOGY-DETECTED" in e for e in errors), errors

    def test_ms_decoupled_check_templates_c1_warn_c2_c3_fail(self, tmp_path: Path, capsys):
        """P0: check_templates hard-fails on cand_c2 / cand_c3 and warns on cand_c1."""
        from check_templates import check_templates_file_or_dir

        cta_payload = {
            "course_id": "test_ms_ct",
            "title": "Test MS CT",
            "competencies": [
                {
                    "id": "C-MS",
                    "name": "MS Comp",
                    "type": "skill",
                    "distractors": [{"id": f"D{i}", "name": f"Distractor {i}"} for i in range(1, 7)],
                }
            ],
        }
        cta_file = tmp_path / "cta.json"
        cta_file.write_text(json.dumps(cta_payload, indent=2), encoding="utf-8")

        stems_ct = _make_stems("{k}", count=12)

        def _make_tpl_file(name: str, verify_py: str) -> Path:
            payload = {
                "competency_id": "C-MS",
                "templates": [
                    {
                        "id": f"T-{name}",
                        "competency_id": "C-MS",
                        "interaction_type": "multiple_select",
                        "difficulty": "medium",
                        "bloom": "Apply",
                        "stem": stems_ct[0],
                        "stem_variants": stems_ct,
                        "generate_py": (
                            "def generate(rng):\n"
                            "    k = rng.randint(10, 800)\n"
                            "    return {\n"
                            "        'vars': {'k': k},\n"
                            "        'options': [\n"
                            "            {'value': f'$x > {k}$', 'is_correct': True, 'distractor_id': None},\n"
                            "            {'value': f'$x + 1 > {k}$', 'is_correct': True, 'distractor_id': None},\n"
                            "            {'value': f'$x < {k}$', 'is_correct': False, 'distractor_id': 'D1', 'error_rationale': f'Inversión del sentido de desigualdad para el umbral numérico {k}.'},\n"
                            "            {'value': f'$x = {k-1}$', 'is_correct': False, 'distractor_id': 'D2', 'error_rationale': f'Sustitución por igualdad estricta debajo de la cota mínima {k}.'},\n"
                            "        ],\n"
                            "        'distractors': [],\n"
                            "    }\n"
                        ),
                        "cross_check_py": verify_py,
                        "hints": [
                            "Observe la relación estricta establecida respecto al parámetro k.",
                            "Verifique si incrementar en una unidad conserva la desigualdad.",
                            "Contraste las opciones positivas frente a los signos invertidos.",
                        ],
                        "solution": "Al cumplirse la desigualdad estricta respecto a {k}, sumar uno mantiene el orden estricto.",
                        "distractor_ids": ["D1", "D2"],
                    }
                ],
            }
            out = tmp_path / f"{name}.json"
            out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            return out

        # cand_c1: passes with WARNING [TPL-CROSS-RATIONALE]
        ver_c1 = (
            "def verify(res):\n"
            "    k = res['vars']['k']\n"
            "    opts = res['options']\n"
            "    exp_t = {f'$x > {k}$', f'$x + 1 > {k}$'}\n"
            "    if {o.get('value') for o in opts if o.get('is_correct')} != exp_t: return False\n"
            "    exp_f = {f'$x < {k}$': 'D1', f'$x = {k-1}$': 'D2'}\n"
            "    return all(o.get('value') in exp_f and o.get('distractor_id') == exp_f[o.get('value')] for o in opts if not o.get('is_correct'))\n"
        )
        ok_c1, errs_c1 = check_templates_file_or_dir(_make_tpl_file("c1", ver_c1), cta_path=cta_file, num_dry_run_seeds=10, strict=True)
        captured = capsys.readouterr()
        assert ok_c1, f"Expected cand_c1-only verifier to warn and pass in check_templates: {errs_c1}"
        assert "[TPL-CROSS-RATIONALE]" in captured.err

        # cand_c2: fails hard when true option value='__MUTATED__' passes
        ver_c2 = (
            "def verify(res):\n"
            "    opts = res['options']\n"
            "    t_vals = [str(o.get('value') or '') for o in opts if o.get('is_correct') is True]\n"
            "    if len(t_vals) != 2 or any(tv.strip() in ('$0 = 1$', '$1 = 2$') for tv in t_vals): return False\n"
            "    return all(o.get('distractor_id') in {'D1', 'D2'} and len(str(o.get('error_rationale') or '')) >= 20 for o in opts if not o.get('is_correct'))\n"
        )
        ok_c2, errs_c2 = check_templates_file_or_dir(_make_tpl_file("c2", ver_c2), cta_path=cta_file, num_dry_run_seeds=10, strict=True)
        assert not ok_c2
        assert any("TPL-CROSS" in e for e in errs_c2), errs_c2

        # cand_c3: fails hard when true option value='$0 = 1$' passes
        ver_c3 = (
            "def verify(res):\n"
            "    opts = res['options']\n"
            "    t_vals = [str(o.get('value') or '') for o in opts if o.get('is_correct') is True]\n"
            "    if len(t_vals) != 2 or any('__MUTATED__' in tv or not (tv.startswith('$') and tv.endswith('$')) for tv in t_vals): return False\n"
            "    return all(o.get('distractor_id') in {'D1', 'D2'} and len(str(o.get('error_rationale') or '')) >= 20 for o in opts if not o.get('is_correct'))\n"
        )
        ok_c3, errs_c3 = check_templates_file_or_dir(_make_tpl_file("c3", ver_c3), cta_path=cta_file, num_dry_run_seeds=10, strict=True)
        assert not ok_c3
        assert any("TPL-CROSS" in e for e in errs_c3), errs_c3

    def test_prompt_shard_author_example_compiles_clean_and_passes_strict(self, tmp_path: Path):
        """Smoke-test the canonical <example> in system_prompts/lean/prompt_shard_author.md against patched compile_shard."""
        from compile_shard import compile_shard

        prompt_path = SKILL_DIR / "system_prompts" / "lean" / "prompt_shard_author.md"
        text = prompt_path.read_text(encoding="utf-8")
        m = re.search(r"<example>.*?```python\s*(.*?)\s*```.*?</example>", text, re.DOTALL)
        assert m, "Could not locate <example> python block in prompt_shard_author.md"
        example_code = m.group(1)

        work_dir = tmp_path / "work"
        shards_dir = work_dir / "shards"
        templates_dir = work_dir / "templates"
        shards_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)

        comp = {
            "id": "Hab-01",
            "name": "Operaciones Aditivas con Cotas",
            "type": "skill",
            "description_latex": "Evaluación de sumas lineales, diferencias e invariantes de positividad en cotas.",
            "assumptions": [{"id": "A-Hab01-01", "statement": "Variables enteras positivas con y > x > 0."}],
            "distractors": [
                {
                    "id": f"D-Hab01-0{i}",
                    "wrong_belief": f"Error {i}",
                    "correct_belief": f"Correcto {i}",
                    "manifestation": f"Dist {i}",
                    "remediation_hint": (
                        f"Verifique cuidadosamente el signo y los coeficientes de la expresión aditiva paso {i}."
                    ),
                }
                for i in range(1, 7)
            ],
        }
        cta_file = work_dir / "cta.json"
        cta_file.write_text(json.dumps({"course_id": "ex", "title": "Ex", "competencies": [comp]}, indent=2), encoding="utf-8")
        (shards_dir / "pre_shard_manifest.json").write_text(
            json.dumps(
                {
                    "shards": [
                        {
                            "shard_id": "shard_01",
                            "competency_ids": ["Hab-01"],
                            "shard_data_path": str((shards_dir / "shard_01_data.py").as_posix()),
                            "templates_dir": str(templates_dir.as_posix()),
                            "competencies": [comp],
                        }
                    ]
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        (shards_dir / "shard_01_data.py").write_text(example_code, encoding="utf-8")

        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            min_archetypes=4,
            seeds=50,
            cta_path=cta_file,
        )
        assert success, f"Canonical prompt_shard_author.md <example> failed compile_shard: {errors}"
        assert errors == []

    @pytest.mark.parametrize("example_name", ["edo", "edp"])
    def test_examples_edo_and_edp_pass_strict_check_templates(self, example_name: str):
        """Regression guard: bundled examples/edo and examples/edp still pass strict check_templates."""
        from check_templates import check_templates_file_or_dir

        ex_dir = SKILL_DIR / "examples" / example_name
        tpl_dir = ex_dir / "templates"
        cta_file = ex_dir / "cta.json"
        if not tpl_dir.is_dir() or not cta_file.is_file():
            pytest.skip(f"Example directory not present: {ex_dir}")

        valid, errors = check_templates_file_or_dir(tpl_dir, cta_path=cta_file, num_dry_run_seeds=10, strict=True)
        assert valid, f"examples/{example_name} failed strict check_templates: {errors}"

    def test_assumption_id_validation_against_cta(self, tmp_path: Path):
        """P1: Hallucinated assumption_id fails [TPL-ASSUMPTION-LINK] even when cta.json has assumptions=[]."""
        from compile_shard import compile_shard

        stems_x = _make_stems("@x@", count=16)

        def _build_shard(base: Path, assumptions_cta: Optional[List[Dict[str, str]]], with_cta: bool, aid: str) -> tuple[bool, List[str]]:
            work_dir, shards_dir, _, cta_file = _setup_shard_workspace(
                base, cid="C-01", ctype="skill", assumptions=assumptions_cta, with_cta=with_cta
            )
            aid_entry = f'"assumption_id": "{aid}",' if aid else ""
            code = f'''
def gen_1(rng):
    x = rng.randint(10, 600)
    return {{"vars": {{"x": x, "ans": x * 2}}, "correct": str(x * 2), "distractors": []}}

def ver_1(res):
    return isinstance(res, dict) and str(res.get("correct")) == str(res.get("vars", {{}}).get("x", 0) * 2)

stems = {stems_x!r}
hints = [
    "Identifique primero la magnitud entera proporcionada en la consigna.",
    "Aplique el factor multiplicativo igual a dos sobre dicho valor base.",
    "Verifique la consistencia numérica sin agregar símbolos de moneda.",
]
TEMPLATES = [
    {{
        "id": "T-C01-01",
        "cid": "C-01",
        "qtype": "fill_in_the_blank",
        "archetype": "direct",
        {aid_entry}
        "gen": gen_1,
        "ver": ver_1,
        "band": ("easy", "Apply"),
        "stem_variants": stems,
        "hints": hints,
        "sol": "Paso 1: Identifique @x@. Paso 2: Multiplique @x@ por dos para obtener @ans@.",
    }}
]
'''
            (shards_dir / "shard_01_data.py").write_text(code, encoding="utf-8")
            return compile_shard(
                work_dir_or_path=work_dir,
                shard_id="shard_01",
                strict=True,
                seeds=20,
                cta_path=cta_file,
                min_archetypes=1,
            )

        # 1) cta.json has empty assumptions=[] -> hallucinated assumption_id must fail
        ok_empty, errs_empty = _build_shard(tmp_path / "empty_assump", [], True, "A-C01-99")
        assert not ok_empty
        assert any("[TPL-ASSUMPTION-LINK]" in e for e in errs_empty), errs_empty

        # 2) cta.json has A-C01-01 -> non-matching A-C01-HALLUCINATED must fail
        ok_bad, errs_bad = _build_shard(tmp_path / "bad_assump", [{"id": "A-C01-01", "statement": "x > 0"}], True, "A-C01-HALLUCINATED")
        assert not ok_bad
        assert any("[TPL-ASSUMPTION-LINK]" in e for e in errs_bad), errs_bad

        # 3) Matching A-C01-01 passes
        ok_good, errs_good = _build_shard(tmp_path / "good_assump", [{"id": "A-C01-01", "statement": "x > 0"}], True, "A-C01-01")
        assert ok_good, f"Expected matching assumption_id to pass: {errs_good}"

        # 4) No cta.json truth available -> degrades gracefully without false block
        ok_no_cta, errs_no_cta = _build_shard(tmp_path / "no_cta", None, False, "A-C01-UNCHECKED")
        assert ok_no_cta, f"Expected graceful pass when no CTA map exists: {errs_no_cta}"

    @pytest.mark.parametrize("case", ["hint2_leak", "fib_at_ans", "mc7_at_ans"])
    def test_tpl_hint_leak_catches_hint2_and_at_ans_in_fib_and_mc7(self, tmp_path: Path, case: str):
        """P1: [TPL-HINT-LEAK] inspects all hints (including hint[2]) and blocks @ans@ in FIB & MC7."""
        from compile_shard import compile_shard

        work_dir, shards_dir, _, cta_file = _setup_shard_workspace(tmp_path / case, cid="C-01", ctype="skill")
        stems_k = _make_stems("@k@", count=12)

        if case == "hint2_leak":
            # Fixed >= 15c answer substring repeated verbatim inside hint[2], with 6 distinct non-boilerplate distractors
            code = f'''
def gen_1(rng):
    k = rng.randint(10, 600)
    return {{
        "vars": {{"k": k}},
        "correct": "Equilibrio estable positivo global",
        "distractors": [
            ("D-C-01-01", f"Trayectoria oscilatoria en {{k}}", "Confunde amortiguamiento lineal con ciclo periódico alrededor de @k@."),
            ("D-C-01-02", f"Divergencia exponencial para {{k}}", "Asume erróneamente autovalor positivo bajo parámetro @k@ dado."),
            ("D-C-01-03", f"Colapso trivial nulo en {{k}}", "Iguala incorrectamente la solución estacionaria a cero con @k@."),
            ("D-C-01-04", f"Inestabilidad en silla bajo {{k}}", "Invierte el signo del determinante jacobiano evaluado en @k@."),
            ("D-C-01-05", f"Bifurcación degenerada con {{k}}", "Supone autovalores repetidos nulos sin sustento en @k@."),
            ("D-C-01-06", f"Cota asintótica infinita en {{k}}", "Omite el término disipativo estacionario en la variable @k@."),
        ],
    }}

def ver_1(res):
    return isinstance(res, dict) and str(res.get("correct")) == "Equilibrio estable positivo global"

stems = {stems_k!r}
hints = [
    "Identifique el parámetro inicial proporcionado en el enunciado.",
    "Compare el signo del término lineal alrededor del estado estacionario.",
    "La respuesta correcta afirma Equilibrio estable positivo global.",
]
'''
            tpl_type = "multiple_choice_7_options"
            sol_str = "Paso 1: Analice el parámetro @k@. Paso 2: Se concluye Equilibrio estable positivo global."
        elif case == "fib_at_ans":
            code = f'''
def gen_1(rng):
    k = rng.randint(10, 600)
    return {{"vars": {{"k": k, "ans": k * 3}}, "correct": str(k * 3), "distractors": []}}

def ver_1(res):
    return isinstance(res, dict) and str(res.get("correct")) == str(res.get("vars", {{}}).get("k", 0) * 3)

stems = {stems_k!r}
hints = [
    "Identifique el parámetro entero inicial en la consigna.",
    "Multiplique por tres dicho parámetro base paso a paso.",
    "Verifique que el resultado final coincida con @ans@ sin signos.",
]
'''
            tpl_type = "fill_in_the_blank"
            sol_str = "Paso 1: Tome @k@. Paso 2: Multiplique por tres para obtener el valor @ans@."
        else:  # mc7_at_ans
            code = f'''
def gen_1(rng):
    k = rng.randint(10, 600)
    ans = k * 3
    return {{
        "vars": {{"k": k, "ans": ans, **{{f"d{{i}}": ans + i for i in range(1, 7)}}}},
        "correct": r"$@ans@$",
        "distractors": [
            (f"D-C-01-0{{i}}", rf"$@d{{i}}@$", f"Desplazamiento numérico indebido en {{i}} unidades respecto al parámetro @k@.")
            for i in range(1, 7)
        ],
    }}

def ver_1(res):
    return isinstance(res, dict) and res.get("correct") == r"$@ans@$"

stems = {stems_k!r}
hints = [
    "Identifique el parámetro entero inicial en la consigna.",
    "Verifique que la opción elegida sea igual a @ans@ en formato KaTeX.",
    "Compruebe la consistencia numérica de la alternativa seleccionada.",
]
'''
            tpl_type = "multiple_choice_7_options"
            sol_str = "Paso 1: Tome @k@. Paso 2: Multiplique por tres para obtener el valor @ans@."

        full_code = code + f'''
TEMPLATES = [
    ("T-C01-01", "C-01", "{tpl_type}", gen_1, ver_1, ("easy", "Apply"), stems, hints, {sol_str!r}),
]
'''
        (shards_dir / "shard_01_data.py").write_text(full_code, encoding="utf-8")
        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            seeds=20,
            cta_path=cta_file,
            min_archetypes=1,
        )
        assert not success, f"Expected [TPL-HINT-LEAK] for case={case}"
        assert any("[TPL-HINT-LEAK]" in e for e in errors), errors

    def test_hints_duplicate_and_exp_short_promoted_under_strict(self, tmp_path: Path, capsys):
        """P1: [TPL-HINTS-DUPLICATE] and [TPL-EXP-SHORT] warn when strict=False and fail when strict=True."""
        from check_templates import check_templates_file_or_dir
        from compile_shard import compile_shard

        work_dir, shards_dir, _, cta_file = _setup_shard_workspace(tmp_path / "cs_dup", cid="C-01", ctype="skill")
        stems_1 = _make_stems("@x@", count=8)
        stems_2 = [s.replace("resultado", "sucesor doble").replace("magnitud", "cifra doble") for s in _make_stems("@x@", count=8)]
        shard_code = f'''
def gen_1(rng):
    x = rng.randint(10, 500)
    return {{"vars": {{"x": x, "ans": x + 1}}, "correct": str(x + 1), "distractors": []}}

def gen_2(rng):
    x = rng.randint(10, 500)
    return {{"vars": {{"x": x, "ans": x + 2}}, "correct": str(x + 2), "distractors": []}}

def ver_1(res):
    return isinstance(res, dict) and str(res.get("correct")) == str(res.get("vars", {{}}).get("x", 0) + 1)

def ver_2(res):
    return isinstance(res, dict) and str(res.get("correct")) == str(res.get("vars", {{}}).get("x", 0) + 2)

stems_1 = {stems_1!r}
stems_2 = {stems_2!r}
shared_hints = [
    "Identifique el número entero inicial en el enunciado del problema.",
    "Aplique el desplazamiento aditivo indicado sobre la magnitud base.",
    "Confirme el entero resultante sin delimitadores matemáticos.",
]
TEMPLATES = [
    ("T-C01-01", "C-01", "fill_in_the_blank", gen_1, ver_1, ("easy", "Apply"), stems_1, shared_hints, "Solución corta @ans@."),
    ("T-C01-02", "C-01", "fill_in_the_blank", gen_2, ver_2, ("medium", "Apply"), stems_2, shared_hints, "Solución paso a paso suficientemente extensa detallando el desplazamiento de dos unidades sobre @x@."),
]
'''
        (shards_dir / "shard_01_data.py").write_text(shard_code, encoding="utf-8")

        ok_nonstrict, errs_nonstrict = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=False,
            seeds=15,
            cta_path=cta_file,
            min_archetypes=2,
        )
        captured = capsys.readouterr()
        assert ok_nonstrict, f"Expected non-strict pass with warnings: {errs_nonstrict}"
        assert "[TPL-HINTS-DUPLICATE]" in captured.err
        assert "[TPL-EXP-SHORT]" in captured.err

        ok_strict, errs_strict = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            seeds=15,
            cta_path=cta_file,
            min_archetypes=2,
        )
        assert not ok_strict
        joined = "\n".join(errs_strict)
        assert "[TPL-HINTS-DUPLICATE]" in joined
        assert "[TPL-EXP-SHORT]" in joined

        # check_templates_file_or_dir: duplicate hints + short explanation_es (strict=False vs strict=True)
        cta_payload = {
            "course_id": "ct_dup",
            "title": "CT Dup",
            "competencies": [{"id": "C-01", "name": "C01", "type": "skill", "distractors": []}],
        }
        ct_cta = tmp_path / "ct_cta.json"
        ct_cta.write_text(json.dumps(cta_payload, indent=2), encoding="utf-8")
        tpl_json = tmp_path / "C-01.json"
        shared_h = [
            "Identifique la magnitud numérica entera en la consigna.",
            "Realice la suma directa siguiendo la definición dada.",
            "Verifique el resultado entero obtenido sin signos extra.",
        ]
        sv1 = _make_stems("{x}", count=8)
        sv2 = [s.replace("resultado", "valor desplazado") for s in sv1]
        tpl_json.write_text(
            json.dumps(
                {
                    "competency_id": "C-01",
                    "templates": [
                        {
                            "id": "T-C01-01",
                            "competency_id": "C-01",
                            "interaction_type": "fill_in_the_blank",
                            "difficulty": "easy",
                            "bloom": "Apply",
                            "stem": sv1[0],
                            "stem_variants": sv1,
                            "generate_py": "def generate(rng):\n    x = rng.randint(10, 500)\n    return {'vars': {'x': x}, 'correct': str(x + 1), 'value': str(x + 1), 'distractors': []}\n",
                            "cross_check_py": "def verify(res):\n    return str(res.get('correct')) == str(res['vars']['x'] + 1)\n",
                            "hints": shared_h,
                            "solution": "Solución breve.",
                            "distractor_ids": [],
                        },
                        {
                            "id": "T-C01-02",
                            "competency_id": "C-01",
                            "interaction_type": "fill_in_the_blank",
                            "difficulty": "medium",
                            "bloom": "Apply",
                            "stem": sv2[0],
                            "stem_variants": sv2,
                            "generate_py": "def generate(rng):\n    x = rng.randint(10, 500)\n    return {'vars': {'x': x}, 'correct': str(x + 2), 'value': str(x + 2), 'distractors': []}\n",
                            "cross_check_py": "def verify(res):\n    return str(res.get('correct')) == str(res['vars']['x'] + 2)\n",
                            "hints": shared_h,
                            "solution": "Solución detallada paso a paso sumando dos unidades al parámetro inicial {x} de forma rigurosa.",
                            "distractor_ids": [],
                        },
                    ],
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        ok_ct_ns, errs_ct_ns = check_templates_file_or_dir(tpl_json, cta_path=ct_cta, num_dry_run_seeds=10, strict=False)
        cap_ct = capsys.readouterr()
        assert ok_ct_ns, f"Expected check_templates strict=False to warn and pass: {errs_ct_ns}"
        assert "[TPL-HINTS-DUPLICATE]" in cap_ct.err
        assert "[TPL-EXP-SHORT]" in cap_ct.err

        ok_ct_s, errs_ct_s = check_templates_file_or_dir(tpl_json, cta_path=ct_cta, num_dry_run_seeds=10, strict=True)
        assert not ok_ct_s
        ct_joined = "\n".join(errs_ct_s)
        assert "[TPL-HINTS-DUPLICATE]" in ct_joined
        assert "[TPL-EXP-SHORT]" in ct_joined

    def test_error_rationale_var_shrinkage_gate(self, tmp_path: Path):
        """P1: Raw >= 50c that shrinks below 50c when normalizing @var@ -> 'X' fails under strict=True."""
        from compile_shard import compile_shard

        stems_vars = _make_stems("@parametro_largo_uno@ y @parametro_largo_dos@", count=16)

        def _run_rat(base: Path, rat_str: str) -> tuple[bool, List[str]]:
            work_dir, shards_dir, _, cta_file = _setup_shard_workspace(base, cid="C-01", ctype="skill")
            shard_code = f'''
def gen_1(rng):
    parametro_largo_uno = rng.randint(10, 200)
    parametro_largo_dos = rng.randint(1, 9)
    ans = parametro_largo_uno + parametro_largo_dos
    return {{
        "vars": {{
            "parametro_largo_uno": parametro_largo_uno,
            "parametro_largo_dos": parametro_largo_dos,
            "ans": ans,
            **{{f"d{{i}}": ans + i for i in range(1, 7)}},
        }},
        "correct": r"$@ans@$",
        "distractors": [
            ("D-C-01-01", r"$@d1@$", {rat_str!r}),
            ("D-C-01-02", r"$@d2@$", "Error sistemático al restar @parametro_largo_uno@ en vez de efectuar la suma directa."),
            ("D-C-01-03", r"$@d3@$", "Error sistemático al duplicar @parametro_largo_uno@ antes de calcular el total final."),
            ("D-C-01-04", r"$@d4@$", "Error sistemático al multiplicar @parametro_largo_uno@ en vez de sumar ambos aquí."),
            ("D-C-01-05", r"$@d5@$", "Error sistemático al dividir @parametro_largo_uno@ en vez de sumar las cantidades."),
            ("D-C-01-06", r"$@d6@$", "Error sistemático al agregar desplazamiento sobre @parametro_largo_uno@ al final."),
        ],
    }}

def ver_1(res):
    return isinstance(res, dict) and res.get("correct") == r"$@ans@$"

stems = {stems_vars!r}
hints = [
    "Identifique los dos sumandos enteros indicados en el enunciado.",
    "Sume directamente ambas magnitudes numéricas sin factores extra.",
    "Verifique que el total supere a cada sumando positivo individual.",
]
TEMPLATES = [
    (
        "T-C01-01", "C-01", "multiple_choice_7_options", gen_1, ver_1,
        ("easy", "Apply"), stems, hints,
        "Paso 1: Identifique ambos parámetros. Paso 2: Sume directamente para obtener el resultado @ans@.",
    ),
]
'''
            (shards_dir / "shard_01_data.py").write_text(shard_code, encoding="utf-8")
            return compile_shard(
                work_dir_or_path=work_dir,
                shard_id="shard_01",
                strict=True,
                seeds=20,
                cta_path=cta_file,
                min_archetypes=1,
            )

        # Raw = 69c, normalized @var@ -> 'X' = 31c (< 50c) -> MUST fail
        shrunk_rat = "Error al operar @parametro_largo_uno@ con @parametro_largo_dos@."
        ok_shrunk, errs_shrunk = _run_rat(tmp_path / "shrunk", shrunk_rat)
        assert not ok_shrunk
        assert any("TPL-MC7-RATIONALE" in e for e in errs_shrunk), errs_shrunk

        # Normalized >= 50c -> MUST pass
        robust_rat = "Error al restar @parametro_largo_uno@ menos @parametro_largo_dos@ en vez de sumarlos aquí."
        ok_robust, errs_robust = _run_rat(tmp_path / "robust", robust_rat)
        assert ok_robust, f"Expected >=50c normalized rationale to pass: {errs_robust}"

    def test_p2_fixes_receipt_cleanup_r18_boilerplate_and_mc7_correct(self, tmp_path: Path):
        """P2: shard_XX.json receipt clears error_count=0 on PASS; R-18 formats boilerplate accurately; MC7 sets r['correct']=c."""
        from check_templates import format_parity_error
        from compile_shard import build_adapted_mc7_generator, compile_shard

        work_dir, shards_dir, _, cta_file = _setup_shard_workspace(tmp_path / "rcpt", cid="C-01", ctype="skill")
        stems_x = _make_stems("@x@", count=12)
        shard_code = f'''
def gen_1(rng):
    x = rng.randint(10, 500)
    return {{"vars": {{"x": x, "ans": x + 1}}, "correct": str(x + 1), "distractors": []}}
def ver_1(res):
    return isinstance(res, dict) and str(res.get("correct")) == str(res.get("vars", {{}}).get("x", 0) + 1)
stems = {stems_x!r}
hints = [
    "Identifique el valor entero inicial en el enunciado.",
    "Sume exactamente una unidad al parámetro dado.",
    "Confirme que el número final sea mayor por una unidad.",
]
TEMPLATES = [
    ("T-C01-01", "C-01", "fill_in_the_blank", gen_1, ver_1, ("easy", "Apply"), stems, hints,
     "Paso 1: Identifique @x@. Paso 2: Sume una unidad para obtener el entero consecutivo @ans@."),
]
'''
        (shards_dir / "shard_01_data.py").write_text(shard_code, encoding="utf-8")
        receipt_path = shards_dir / "shard_01.json"
        receipt_path.write_text(
            json.dumps(
                {
                    "shard_id": "shard_01",
                    "compiled_status": "FAIL",
                    "has_syntax_error": True,
                    "error_count": 4,
                    "compilation_errors": ["stale error"],
                }
            ),
            encoding="utf-8",
        )
        ok, errs = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            seeds=15,
            cta_path=cta_file,
            output_path=receipt_path,
            min_archetypes=1,
        )
        assert ok, errs
        rcpt = json.loads(receipt_path.read_text(encoding="utf-8"))
        assert rcpt["compiled_status"] == "PASS"
        assert rcpt["has_syntax_error"] is False
        assert rcpt["error_count"] == 0
        assert rcpt["compilation_errors"] == []

        from types import SimpleNamespace

        r18_err = SimpleNamespace(
            rule_id="R-18",
            message="Question 'Q1' options show synthetic boilerplate pattern (antonym pair)",
            item_id="Q1",
        )
        r18_msg = format_parity_error("C-01", r18_err, {"Q1": {"template_id": "T-01"}})
        assert "BOILERPLATE / PATRÓN SINTÉTICO" in r18_msg
        assert "META-INFORMACIÓN / GIVEAWAY" not in r18_msg

        base_gen = """
def generate_params(rng):
    v = rng.randint(10, 99)
    return {
        "vars": {"v": v},
        "correct": f"{v}",
        "distractors": [(f"D-C-01-0{i}", f"{v + i}", f"Error sistemático número {i} en cálculo directo del parámetro.") for i in range(1, 7)],
    }
"""
        wrapped = build_adapted_mc7_generator(
            base_gen_code=base_gen,
            cid="C-01",
            cta_distractors=[{"id": f"D-C-01-0{i}"} for i in range(1, 7)],
            strict=True,
            rats_map=None,
            fmt="$@X@$",
        )
        ns: Dict[str, Any] = {}
        exec(wrapped, ns)
        out = ns["generate"](random.Random(42))
        assert out["correct"].startswith("$") and out["correct"] == out["options"][0]["value"]


# ==============================================================================
# B. CTA_MERGE, COMPILE_CTA, CHECK_CTA PATCHES
# ==============================================================================


class TestAB40CTASanitizerAndCompilerPatches:
    """Tests for cta_merge.py, compile_cta.py, and check_cta.py fixes."""

    def test_cta_merge_wrap_bare_equations_false_preserves_omitted_step_and_heals_controls(self):
        """P1: normalize_orphan_math(..., wrap_bare_equations=False) skips bare-token wrapping while wrapping backslash macros, healing controls & balancing $."""
        from cta_merge import normalize_orphan_math

        samples = [
            "|X_n - Z| >= c converge en probabilidad",
            "El promedio Y_barra = a + b permanece constante",
            "La derivada temporal X_p_dot controla la senda",
            "Factor de crecimiento e^{gt}K^a en equilibrio",
            "Consideramos X_n = Y_n como paso intermedio",
        ]
        for s in samples:
            assert normalize_orphan_math(s, wrap_bare_equations=False) == s

        # Explicit backslash LaTeX commands (such as \sqrt{n} in omitted_step) still wrap cleanly so check_cta passes
        omitted_with_sqrt = r"Dividir por n en lugar de la raíz cuadrada \sqrt{n}"
        assert normalize_orphan_math(omitted_with_sqrt, wrap_bare_equations=False) == r"Dividir por n en lugar de la raíz cuadrada $\sqrt{n}$"

        corrupted = "Tasa de crecimiento \x08eta en $x + y"
        healed = normalize_orphan_math(corrupted, wrap_bare_equations=False)
        assert "\\beta" in healed
        assert healed.count("$") % 2 == 0

    def test_cta_monetary_escaped_dollar_survives_normalize_and_check_cta(self):
        """P1: Monetary '\\$' inside or outside '$...$' never splits delimiters or triggers false KaTeX errors."""
        from check_cta import validate_cta_rules
        from cta_merge import auto_wrap_bare_latex_in_cta_field, normalize_orphan_math

        s_inside = r"Valor presente de $\$1$ hoy frente a $\$1(1+i(t)h)$ con $1=p(t)/p(t)$."
        s_outside = r"El costo unitario es \$100 cuando el parámetro cumple $\alpha + \beta = 1$."

        for wrap_flag in (False, True):
            res_in = normalize_orphan_math(s_inside, wrap_bare_equations=wrap_flag)
            res_out = normalize_orphan_math(s_outside, wrap_bare_equations=wrap_flag)
            assert res_in == s_inside
            assert res_out == s_outside

        assert auto_wrap_bare_latex_in_cta_field(s_inside) == s_inside
        assert auto_wrap_bare_latex_in_cta_field(s_outside) == s_outside

        cta_data = _make_schema_valid_cta_dict(
            description_latex=(
                r"Análisis de valoración intertemporal desde $\$1$ hoy hasta $\$1(1+i(t)h)$ con identidad $1=p(t)/p(t)$."
            ),
            math_in_distractors=True,
        )
        res = validate_cta_rules(cta_data)
        assert res.valid, f"Expected escaped monetary '\\$' in CTA to validate cleanly, got: {res.errors}"

    def test_compile_cta_l5_degrade_math_span_scoped_and_flags_truncation(self, tmp_path: Path):
        """P1: L5 DEGRADE_MATH preserves prose intact on short broken spans and hard-fails on >40c truncation."""
        from compile_cta import compile_cta

        def _setup_cta_dir(subdir: Path, desc_latex: str) -> tuple[Path, Path]:
            subdir.mkdir(parents=True, exist_ok=True)
            manifest_file = subdir / "pre_cta_manifest.json"
            manifest_file.write_text(
                json.dumps({"files": [{"doc": "doc.pdf", "valid_page_range": [1, 10], "total_pages": 10}]}),
                encoding="utf-8",
            )
            cta_py = subdir / "cta_data.py"
            cta_py.write_text(
                f'''
COURSE_ID = "l5_test"
TITLE = "L5 Degrade Test"
COMPETENCIES = [
    (
        "concept",
        "C-01",
        "Competencia L5",
        {desc_latex!r},
        "Understand",
        "doc.pdf",
        1,
        [],
        [
            ("D1", "$x=1$", "$x=2$", "wb1", "Revise minuciosamente la definición formal y los pasos de derivación algebraica en equilibrio.", None),
            ("D2", "$y=1$", "$y=2$", "wb2", "Revise minuciosamente la definición formal y los pasos de derivación algebraica en equilibrio.", None),
            ("D3", "$z=1$", "$z=2$", "wb3", "Revise minuciosamente la definición formal y los pasos de derivación algebraica en equilibrio.", None),
        ],
    ),
]
''',
                encoding="utf-8",
            )
            return cta_py, manifest_file

        # 1) Short broken span (<= 40c inner): degrades span-only, preserves surrounding prose intact!
        short_broken = (
            r"Análisis económico del crecimiento estacionario cuando ocurre un error $\frac{1}{{{{unclosed$ dentro del equilibrio dinámico."
        )
        cta_ok, man_ok = _setup_cta_dir(tmp_path / "l5_ok", short_broken)
        ok_s, compiled_s, errs_s, _ = compile_cta(
            cta_data_path=cta_ok,
            output_dir=tmp_path / "l5_ok",
            manifest_path=man_ok,
            allow_degrade=True,
        )
        assert ok_s, f"Expected span-scoped L5 degrade without truncation to succeed, got: {errs_s}"
        new_desc = compiled_s["competencies"][0]["description_latex"]
        assert "Análisis económico del crecimiento estacionario cuando ocurre un error" in new_desc
        assert "dentro del equilibrio dinámico." in new_desc
        assert r"\text{" in new_desc
        assert len(new_desc) >= 80

        # 2) Long broken span (> 40c inner): must NOT truncate silently — emits [CTA-L5-DEGRADE-TRUNCATED] hard fail!
        long_broken = (
            r"Análisis macroeconómico con expresión truncable $\\invalidmacro{{{{\alpha + \beta + \gamma + \delta + \epsilon + \zeta + \eta$ y texto."
        )
        cta_trunc, man_trunc = _setup_cta_dir(tmp_path / "l5_trunc", long_broken)
        ok_t, _, errs_t, _ = compile_cta(
            cta_data_path=cta_trunc,
            output_dir=tmp_path / "l5_trunc",
            manifest_path=man_trunc,
            allow_degrade=True,
        )
        assert not ok_t
        assert any("[CTA-L5-DEGRADE-TRUNCATED]" in e for e in errs_t), errs_t

    def test_cta_hint_short_calibrated_band_70_to_79_vs_under_70_hard_fail(self):
        """P2: remediation_hint 70-79c emits [CTA-HINT-SHORT] warning (valid=True), while <70c hard-fails schema."""
        from check_cta import check_cta_file

        desc = "Descripción suficientemente extensa del modelo analítico con al menos ochenta caracteres totales."

        hint_74 = "X" * 74
        assert 70 <= len(hint_74) < 80
        warns_74: List[str] = []
        res_warn = check_cta_file(_make_schema_valid_cta_dict(desc, hint_override_first=hint_74), warnings_out=warns_74)
        assert res_warn.valid, f"74-char hint must pass schema and warn only: {res_warn.errors}"
        assert any("[CTA-HINT-SHORT]" in w for w in warns_74), warns_74

        hint_65 = "X" * 65
        assert len(hint_65) < 70
        res_fail = check_cta_file(_make_schema_valid_cta_dict(desc, hint_override_first=hint_65))
        assert not res_fail.valid
        assert any("remediation_hint" in e or "70" in e for e in res_fail.errors), res_fail.errors
