"""Tests for C2C Stage 3 First-Pass Rate & Stage 6B Zero-Repair improvements."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SKILL_DIR = ROOT_DIR / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

import check_templates
import dispatch
from engine.assemble import format_template_string
from engine.invariants import check_instance_invariants, validate_katex_syntax
from engine.stage_contract import check_template_bloom_coherence
from engine.template_healing import heal_katex_display_str


def test_heal_katex_cmd_placeholder_spacing():
    raw = r"Calcula $@sa@=@s@\cdot@a@$ y $@a0@\sqrt{k}\to@a1@\sqrt{k}$."
    healed = heal_katex_display_str(raw)
    assert r"\cdot @a@" in healed
    assert r"\to @a1@" in healed
    assert heal_katex_display_str(r"Resultado $4*x + 4*g$.") == r"Resultado $4 \cdot x + 4 \cdot g$."


def test_format_template_string_two_pass_at_interpolation():
    tpl = r"La respuesta es $@ans@$."
    variables = {"ans": r"(s/@n@)^{@pm1@}", "n": "0.05", "pm1": "2"}
    rendered = format_template_string(tpl, variables)
    assert rendered == r"La respuesta es $(s/0.05)^{2}$."
    assert "@n@" not in rendered and "@pm1@" not in rendered


def test_validate_katex_syntax_masks_multi_underscore_at_var():
    txt = r"Sea $Y = K^{@a@}L^{@one_m_a@}$ en equilibrio."
    errs = validate_katex_syntax(txt, "stem_variants[0]", allow_template_vars=False)
    assert not any("Double subscript" in e for e in errs), errs


def test_r15_ms_calibrated_bounds():
    def _make_ms(true_opts, false_opts):
        opts = [{"content": t, "is_correct": True} for t in true_opts] + [
            {"content": f, "is_correct": False, "distractor_id": f"D-0{i+1}", "error_rationale": "Error conceptual con x=2."}
            for i, f in enumerate(false_opts)
        ]
        return {
            "stem": "Seleccione las opciones correctas:",
            "options": opts,
            "hints": ["Pista uno suficientemente larga.", "Pista dos suficientemente larga.", "Pista tres suficientemente larga."],
            "detailed_solution": "Solución detallada paso a paso que supera ochenta caracteres de longitud mínima.",
        }

    # 0.84x and 1.19x should pass under [0.80, 1.20] (7 options: 3 true, 4 false)
    ok_low, errs_low = check_instance_invariants(
        _make_ms(["A" * 84, "B" * 84, "E" * 84], ["C" * 100, "D" * 100, "F" * 100, "G" * 100]),
        "multiple_select",
    )
    assert ok_low, errs_low

    ok_high, errs_high = check_instance_invariants(
        _make_ms(["A" * 119, "B" * 119, "E" * 119], ["C" * 100, "D" * 100, "F" * 100, "G" * 100]),
        "multiple_select",
    )
    assert ok_high, errs_high

    # 1.29x and 0.75x must still fail
    ok_too_long, errs_tl = check_instance_invariants(
        _make_ms(["A" * 129, "B" * 129, "E" * 129], ["C" * 100, "D" * 100, "F" * 100, "G" * 100]),
        "multiple_select",
    )
    assert not ok_too_long and any("MS length anti-giveaway violation" in e for e in errs_tl)

    ok_too_short, errs_ts = check_instance_invariants(
        _make_ms(["A" * 75, "B" * 75, "E" * 75], ["C" * 100, "D" * 100, "F" * 100, "G" * 100]),
        "multiple_select",
    )
    assert not ok_too_short and any("MS length anti-giveaway violation" in e for e in errs_ts)


def test_tpl_placeholder_answer_leak_open_symbolic():
    from engine.assemble import assemble_question
    from engine.invariants import placeholder_leaks_answer

    assert placeholder_leaks_answer("Ej: 1/(1-4*sqrt(s/0.09))**2", "1/(1-4*sqrt(s/0.09))**2", [], ["s"])
    assert not placeholder_leaks_answer("Ej: 1/(1-2*sqrt(s/0.25))**2", "1/(1-4*sqrt(s/0.09))**2", [], ["s"])

    # assemble_question must deterministically sanitize a 1-seed coincidental placeholder leak
    tpl = {
        "id": "T-Hab06-04",
        "interaction_type": "open_symbolic",
        "stem_variants": [r"Con $Y=(4\sqrt{K}+\sqrt{L})^2$ y $n=0.09$, halle $y^*(s)$:"],
        "hints": ["Pista uno suficientemente larga.", "Pista dos suficientemente larga.", "Pista tres suficientemente larga."],
        "solution": "Solución detallada paso a paso que supera ochenta caracteres de longitud mínima.",
    }
    gen_res = {
        "vars": {"a": 4, "n": 0.09},
        "correct": "1/(1-4*sqrt(s/0.09))**2",
        "variables": ["s"],
        "symbolic_config": {"variables": ["s"], "palette": ["sqrt()", "/"], "placeholder": "Ej: 1/(1-4*sqrt(s/0.09))**2"},
    }
    assembled = assemble_question(tpl, gen_res, "Hab-06", 1, seed=42)
    assert assembled["symbolic_config"]["placeholder"] == "Ej: expr(s)"
    assert assembled["interface_config"]["input_placeholder"] == "Ej: expr(s)"

    # Multi-seed check_templates: >= 2 leaking seeds must fail, 1 coincidental seed must pass
    tpl_dyn = {
        "id": "T-Hab06-05",
        "interaction_type": "open_symbolic",
        "archetype": "direct",
        "difficulty": "medium",
        "bloom": "Analyze",
        "generate_py": (
            "def generate(rng):\n"
            "    a = rng.randint(2, 6)\n"
            "    return {'vars': {'a': a}, 'correct': f'{a}*s', 'variables': ['s'], "
            "'symbolic_config': {'variables': ['s'], 'palette': ['*'], 'placeholder': f'Ej: {a}*s'}, "
            "'ds': [('D-Hab06-01', f'{a+1}*s', r'Error con $@a@$ en coeficiente.')]}\n"
        ),
        "cross_check_py": "def verify(c, v): return c2c_ver.equiv(c, f\"{v['a']}*s\", variables=['s'])\n",
        "stem_variants": [
            r"Con $f(s)=@a@s$, exprese $f(s)$:",
            r"Dada $f(s)=@a@s$, halle $f(s)$:",
            r"Si $f(s)=@a@s$, formule $f(s)$:",
        ],
        "hints": [
            "Identifique el coeficiente $@a@$ que multiplica a $s$.",
            "Conserve la variable simbólica $s$ en su respuesta.",
            "Verifique la linealidad directa respecto a $@a@$.",
        ],
        "solution": r"La expresión simbólica equivalente para $f(s)=@a@s$ es $@a@ \cdot s$ directamente.",
    }
    errs_dyn = check_templates.check_single_template(tpl_dyn, "Hab-06", {"D-Hab06-01"}, num_dry_run_seeds=10, strict=False)
    assert any("TPL-PLACEHOLDER-ANSWER-LEAK" in e for e in errs_dyn), errs_dyn

    tpl_static_low_collision = dict(tpl_dyn)
    tpl_static_low_collision["generate_py"] = (
        "def generate(rng):\n"
        "    a = rng.choice([2, 3, 4, 5, 6, 7])\n"
        "    return {'vars': {'a': a}, 'correct': f'{a}*s', 'variables': ['s'], "
        "'symbolic_config': {'variables': ['s'], 'palette': ['*'], 'placeholder': 'Ej: 3*s'}, "
        "'ds': [('D-Hab06-01', f'{a+1}*s', r'Error con $@a@$ en coeficiente.')]}\n"
    )
    errs_stat = check_templates.check_single_template(tpl_static_low_collision, "Hab-06", {"D-Hab06-01"}, num_dry_run_seeds=20, strict=False)
    assert not any("TPL-PLACEHOLDER-ANSWER-LEAK" in e for e in errs_stat), errs_stat

    tpl_static_systematic = dict(tpl_dyn)
    tpl_static_systematic["generate_py"] = (
        "def generate(rng):\n"
        "    a = rng.choice([3, 3, 3, 4])\n"
        "    return {'vars': {'a': a}, 'correct': f'{a}*s', 'variables': ['s'], "
        "'symbolic_config': {'variables': ['s'], 'palette': ['*'], 'placeholder': 'Ej: 3*s'}, "
        "'ds': [('D-Hab06-01', f'{a+1}*s', r'Error con $@a@$ en coeficiente.')]}\n"
    )
    errs_sys = check_templates.check_single_template(tpl_static_systematic, "Hab-06", {"D-Hab06-01"}, num_dry_run_seeds=10, strict=False)
    assert any("TPL-PLACEHOLDER-ANSWER-LEAK" in e for e in errs_sys), errs_sys


def test_tpl_stem_equation_parity():
    tpl = {
        "id": "T-Hab06-04",
        "interaction_type": "open_symbolic",
        "stem_variants": [
            r"Dada $Y=(@a@\sqrt{K}+\sqrt{L})^2$ y $n=@n@$, halle $y^*(s)$:",
            r"Con función de producción $Y=(@a@\sqrt{K}+\sqrt{L})^2$ y $n=@n@$, obtenga $y^*(s)$:",
            r"Si $a=@a@$ y $n=@n@$, calcule el producto estacionario $y^*(s)$:",
        ],
    }
    violations = check_templates._check_stem_equation_parity(tpl)
    assert violations == ["stem_variants[2]"]

    # Variants mixing \dot{K}=... and \phi(k)=... must pass without false positives
    tpl_phi = {
        "id": "T-Hab01-01",
        "interaction_type": "open_symbolic",
        "stem_variants": [
            r"Con $\dot{K}=@s@ Q$, $\dot{L}/L=@lam@$, $K=kL$ y $\phi(k)=@A@\sqrt{k}$, exprese $\dot{k}$:",
            r"Dada $\phi(k)=@A@\sqrt{k}$, tasa de ahorro $@s@$ y crecimiento laboral $@lam@$, halle $\dot{k}$:",
            r"Derive $\dot{k}$ en términos de $k$ si $\phi(k)=@A@\sqrt{k}$ ($s=@s@, \lambda=@lam@$):",
        ],
    }
    assert check_templates._check_stem_equation_parity(tpl_phi) == []


def test_dispatch_skeleton_preassigns_coherent_non_colliding_bands():
    comp_entries = [
        {
            "cid": "Hab-01",
            "is_skill": True,
            "comp_k": 2,
            "min_tpls": 6,
            "distractor_ids": ["D-Hab01-01", "D-Hab01-02"],
            "assumption_ids": ["A-Hab01-01"],
            "target_bloom": "Evaluate",
            "norm_rec_mods": ["FIB", "open_symbolic", "MS"],
        },
        {
            "cid": "C-07",
            "is_skill": False,
            "comp_k": 2,
            "min_tpls": 6,
            "distractor_ids": ["D-C07-01"],
            "assumption_ids": ["A-C07-01"],
            "target_bloom": "Evaluate",
            "norm_rec_mods": ["MC7", "MS", "proof_dag"],
        },
    ]
    skel = dispatch._build_author_skeleton(comp_entries, eff_tpl_per_mod=2)
    assert "def _ok_ds(" in skel
    assert "def _no_fib_leak(" in skel
    assert "_ok_ds(ans, ds, tol=0.005) and _no_fib_leak(ans, vars_d)" in skel

    # Evaluate the skeleton's TEMPLATES metadata (replacing dummy gen/ver)
    import re
    ns = {"RATS": {}, "c2c_ver": object()}
    cleaned = re.sub(r"```python|```", "", skel)
    # Stub gen_/ver_ so exec succeeds
    cleaned = re.sub(r"raise NotImplementedError\('TODO'\)", "pass", cleaned)
    exec(cleaned, ns)
    tpls = ns["TEMPLATES"]
    assert len(tpls) >= 11

    seen_per_cid_mod = {}
    for t in tpls:
        coh_err = check_template_bloom_coherence(t["qtype"], t["archetype"], t["band"][1])
        assert coh_err is None, f"{t['id']}: {coh_err}"
        if t["cid"].startswith("Hab-"):
            assert t["band"][1] in ("Apply", "Analyze", "Evaluate", "Create")
        key = (t["cid"], t["qtype"])
        band_tuple = (t["archetype"], t["band"][0], t["band"][1])
        assert band_tuple not in seen_per_cid_mod.get(key, set()), f"Duplicate band tuple {band_tuple} in {key}"
        seen_per_cid_mod.setdefault(key, set()).add(band_tuple)


def test_lean_prompts_and_subagent_types_sync():
    cta_p = (SKILL_DIR / "system_prompts" / "lean" / "prompt_cta_architect.md").read_text(encoding="utf-8")
    auth_p = (SKILL_DIR / "system_prompts" / "lean" / "prompt_shard_author.md").read_text(encoding="utf-8")
    rep_p = (SKILL_DIR / "system_prompts" / "lean" / "prompt_repair.md").read_text(encoding="utf-8")

    assert "Primeros Principios" in cta_p
    assert "MS>=Understand" in auth_p
    assert "0.80..1.20" in auth_p
    assert "TPL-PLACEHOLDER-ANSWER-LEAK" in auth_p
    assert "MS>=Understand" in rep_p
    assert "0.80 <= avg(len(true))/avg(len(false)) <= 1.20" in rep_p
    assert "TPL-PLACEHOLDER-ANSWER-LEAK" in rep_p

    sub_data = json.loads((SKILL_DIR / "subagent_types.json").read_text(encoding="utf-8"))
    by_name = {x["name"]: x["system_prompt"] for x in sub_data}
    assert "Primeros Principios" in by_name["c2c_cta_architect"]
    assert "TPL-PLACEHOLDER-ANSWER-LEAK" in by_name["c2c_shard_author"]
    assert "TPL-PLACEHOLDER-ANSWER-LEAK" in by_name["c2c_repair"]


def test_adversarial_break_relabels_reasons_post_shuffle():
    import random
    from engine.adversarial_generator import compile_and_verify_adversarial

    raw_adv = {
        "mode": "find_fallacy",
        "steps": [
            {"id": "S1", "content": "Sea $f(x)=2x^2$."},
            {"id": "S2", "content": "Deriva $f'(x)=2$.", "is_fallacy": True, "distractor_id": "D-01", "error_rationale": "Olvida exponente $2$."},
            {"id": "S3", "content": "Evalúa en $x=1$."},
        ],
        "reason_options": [
            {"id": "R1", "content": "Falta multiplicar por $2x$.", "is_correct": True},
            {"id": "R2", "content": "Falta signo negativo.", "is_correct": False, "distractor_id": "D-02", "error_rationale": "Signo positivo se mantiene."},
            {"id": "R3", "content": "Debe sumar constante.", "is_correct": False, "distractor_id": "D-03", "error_rationale": "La constante desaparece."},
        ],
    }
    seen_corr_ids = set()
    for s in range(20):
        compiled, ca = compile_and_verify_adversarial(raw_adv, variables={}, rng=random.Random(s))
        ids = [r["id"] for r in compiled["reason_options"]]
        assert ids == ["R1", "R2", "R3"]
        corr_r = next(r for r in compiled["reason_options"] if r["is_correct"])
        assert ca["correct_reason_id"] == corr_r["id"]
        seen_corr_ids.add(ca["correct_reason_id"])
    assert len(seen_corr_ids) >= 2


def test_concept_matching_relabels_targets_post_shuffle():
    import random
    from engine.assemble import _assemble_concept_matching

    raw_cm = {
        "premises": [
            {"id": "P1", "content": "A"},
            {"id": "P2", "content": "B"},
            {"id": "P3", "content": "C"},
            {"id": "P4", "content": "D"},
        ],
        "targets": [
            {"id": "T1", "content": "1"},
            {"id": "T2", "content": "2"},
            {"id": "T3", "content": "3"},
            {"id": "T4", "content": "4"},
            {"id": "T5", "content": "5", "is_distractor": True, "distractor_id": "D-01", "error_rationale": "Distractor cinco."},
            {"id": "T6", "content": "6", "is_distractor": True, "distractor_id": "D-02", "error_rationale": "Distractor seis."},
        ],
        "correct_pairs": {"P1": "T1", "P2": "T2", "P3": "T3", "P4": "T4"},
    }
    non_identity = False
    for s in range(15):
        compiled, ca = _assemble_concept_matching(raw_cm, {}, None, random.Random(s), {})
        assert [t["id"] for t in compiled["targets"]] == ["T1", "T2", "T3", "T4", "T5", "T6"]
        assert ca["pairs"] == compiled["correct_pairs"]
        if any(k[1:] != v[1:] for k, v in ca["pairs"].items()):
            non_identity = True
    assert non_identity


def test_degenerate_literal_cond():
    ms_degen = {
        "stem": "Sobre $[0, 6]$ ($3>0$), seleccione:",
        "options": [
            {"content": "Si $2=0$, el funcional se reduce a Lagrange.", "is_correct": True},
            {"content": "La frontera es fija en $t=0$.", "is_correct": True},
            {"content": "El integrando es nulo.", "is_correct": False, "distractor_id": "D-01", "error_rationale": "Error en integrando."},
            {"content": "El horizonte es infinito.", "is_correct": False, "distractor_id": "D-02", "error_rationale": "Error en horizonte."},
            {"content": "No hay término terminal.", "is_correct": False, "distractor_id": "D-03", "error_rationale": "Error en término."},
            {"content": "La trayectoria diverge en $t=0$.", "is_correct": False, "distractor_id": "D-04", "error_rationale": "Error en trayectoria."},
            {"content": "El multiplicador es negativo.", "is_correct": False, "distractor_id": "D-05", "error_rationale": "Error en multiplicador."},
        ],
        "hints": ["Pista uno suficientemente larga.", "Pista dos suficientemente larga.", "Pista tres suficientemente larga."],
        "detailed_solution": "Solución detallada paso a paso que supera ochenta caracteres de longitud mínima.",
    }
    ok_deg, errs_deg = check_instance_invariants(ms_degen, "multiple_select")
    assert not ok_deg
    assert sum(1 for e in errs_deg if "[TPL-DEGENERATE-LITERAL-COND]" in e) == 2


def test_m20_rigor_gates_in_check_templates():
    errs_ms: list[str] = []
    check_templates._check_m20_rigor_for_instance(
        {"options": [{"content": "A", "is_correct": True}] * 2 + [{"content": "B", "is_correct": False}] * 2},
        "multiple_select",
        strict=True,
        competency_id="C-01",
        tpl_id="T-C01-01",
        errors=errs_ms,
    )
    assert any("MS-MIN-OPTIONS" in e for e in errs_ms)

    errs_cm: list[str] = []
    check_templates._check_m20_rigor_for_instance(
        {"concept_matching": {"premises": [{"id": "P1"}, {"id": "P2"}], "targets": [{"id": "T1"}, {"id": "T2"}, {"id": "T3", "is_distractor": True}], "correct_pairs": {"P1": "T1", "P2": "T2"}}},
        "concept_matching",
        strict=True,
        competency_id="C-01",
        tpl_id="T-C01-03",
        errors=errs_cm,
    )
    assert any("MATCHING-MIN-RIGOR" in e for e in errs_cm)

    errs_div = check_templates._check_competency_rigor_diversity(
        "C-01",
        [
            {"interaction_type": "multiple_select", "template_id": "T-C01-01", "options": [{"is_correct": True}] * 2 + [{"is_correct": False}] * 5},
            {"interaction_type": "multiple_select", "template_id": "T-C01-02", "options": [{"is_correct": True}] * 2 + [{"is_correct": False}] * 5},
        ],
        strict=True,
    )
    assert any("MS-CORRECT-COUNT-DIVERSITY" in e for e in errs_div)


def test_dispatch_skeleton_rotates_ms_expected_correct_count():
    skel = dispatch._build_author_skeleton(
        [
            {
                "cid": "C-01",
                "is_skill": False,
                "comp_k": 2,
                "min_tpls": 4,
                "distractor_ids": ["D-C01-01"],
                "assumption_ids": [],
                "target_bloom": "Analyze",
                "norm_rec_mods": ["MS", "adversarial_break"],
            }
        ],
        eff_tpl_per_mod=2,
    )
    assert "expected_correct_count=3" in skel
    assert "expected_correct_count=2" in skel
    assert "7 opciones, 2..5 correctas" in skel
    assert "variar falacia (ej. S2)" in skel
    assert "variar falacia (ej. S4)" in skel


def test_mateco_sanitized_no_degenerate_literal_conditions():
    import re
    mateco_p = ROOT_DIR / "courses" / "mateco_4_optimizacion_v20_k_3.json"
    if not mateco_p.is_file():
        return
    txt = mateco_p.read_text(encoding="utf-8")
    assert not re.search(r"Si\s+\$[1-9]\d*=0\$", txt)
    assert not re.search(r"\(\$[1-9]\d*>0\$\)", txt)


def test_post_render_sanitize_katex_heals_sympy_in_math_only():
    from engine.assemble import sanitize_katex_syntax

    # Inside $...$, SymPy multiplication/power/sqrt injected via @var@ are healed
    rendered = sanitize_katex_syntax("La derivada es $6*L + x**2 + sqrt(k)$ en equilibrio.")
    assert r"6 \cdot L" in rendered
    assert "x^{2}" in rendered
    assert r"\sqrt{k}" in rendered

    # Bare open_symbolic expressions without $ or with heal_sympy_in_math=False stay raw SymPy
    assert sanitize_katex_syntax("6*L + x**2") == "6*L + x**2"
    assert sanitize_katex_syntax("$6*L + x**2$", heal_sympy_in_math=False) == "$6*L + x**2$"


def test_dispatch_skeleton_attaches_assumption_to_every_boundary_and_symbolic_ok_ds():
    skel = dispatch._build_author_skeleton(
        [
            {
                "cid": "Hab-01",
                "is_skill": True,
                "comp_k": 2,
                "min_tpls": 8,
                "distractor_ids": ["D-Hab01-01"],
                "assumption_ids": ["A-Hab01-01", "A-Hab01-02"],
                "target_bloom": "Evaluate",
                "norm_rec_mods": ["FIB", "open_symbolic", "MS", "proof_dag"],
            }
        ],
        eff_tpl_per_mod=2,
    )
    # Both boundary_or_edge_case slots must receive an assumption_id
    boundary_count = skel.count("'archetype': \"boundary_or_edge_case\"")
    aid_count = skel.count("'assumption_id':")
    assert boundary_count >= 2
    assert aid_count == boundary_count
    assert "A-Hab01-01" in skel and "A-Hab01-02" in skel
    # Key inline reminders present
    assert "MISMOS @var@ en las 4 variantes" in skel
    assert "Balance MS: len(true)~=len(false)" in skel
    assert ">=10 claves unicas en 50 seeds" in skel
    # Execute injected _ok_ds helper for both symbolic and numeric cases
    code_body = skel.split("```python\n", 1)[1].rsplit("\n```", 1)[0]
    ns: dict = {}
    helper_only = "\n".join(
        ln for ln in code_body.splitlines()
        if ln.startswith(("def _ok_ds", "    ")) and not ln.startswith("    {") and not ln.startswith("        ")
    )
    # Extract exact _ok_ds block cleanly
    start = code_body.index("def _ok_ds(")
    end = code_body.index("def _no_fib_leak(")
    exec(code_body[start:end], ns)
    ok_ds = ns["_ok_ds"]
    assert ok_ds("8-10*z", [("D1", "8 + 10*z"), ("D2", "10*z - 8")]) is True
    assert ok_ds("8-10*z", [("D1", "8 - 10*z"), ("D2", "10*z - 8")]) is False
    assert ok_ds(10.0, [("D1", 12.0), ("D2", 8.0)]) is True
    assert ok_ds(10.0, [("D1", 10.01), ("D2", 8.0)]) is False


def test_r15_ms_diagnostic_mentions_080_120_bounds():
    from engine.template_diagnostics import format_invariant_error_diagnostic

    msg = format_invariant_error_diagnostic(
        "C-01",
        "T-C01-01",
        "Q-C01-001",
        "MS length anti-giveaway violation: correct options too short on average (avg_true=51.0 vs avg_false=64.0, ratio=0.79x < 0.80x).",
    )
    assert "0.80x - 1.20x" in msg
    assert "0.85x - 1.15x" not in msg


def test_sandbox_allows_local_nt_variable_but_blocks_import_nt():
    import pytest
    from engine.sandbox import SandboxSecurityError, validate_code_ast

    assert validate_code_ast("def gen(rng):\n    n, t = 0.02, 5\n    nt = n * t\n    return {'nt': nt}\n") is True

    with pytest.raises(SandboxSecurityError):
        validate_code_ast("import nt\n")


def test_katex_healing_handles_digit_star_paren_and_adjacent_placeholders_in_math():
    from engine.assemble import sanitize_katex_syntax
    from engine.template_healing import heal_katex_display_str

    assert heal_katex_display_str("Evalúa $2*(x + 1)$.") == r"Evalúa $2 \cdot (x + 1)$."
    assert sanitize_katex_syntax("Evalúa $2*(x + 1)$.") == r"Evalúa $2 \cdot (x + 1)$."
    assert sanitize_katex_syntax("2*(x + 1)") == "2*(x + 1)"

    # Inside $...$, adjacent placeholders are healed to \cdot; outside $...$, they stay unhealed so validator rejects them
    assert heal_katex_display_str("Con $@s@@L0@$") == r"Con $@s@ \cdot @L0@$"
    assert heal_katex_display_str("Con @s@@L0@") == "Con @s@@L0@"


def test_fast_symbolic_equivalence_preserves_exact_semantics():
    from engine.c2c_ver import _ver_equiv
    from engine.invariants import _expressions_collide

    # Algebraic identities must still be detected as equal / colliding
    assert _expressions_collide("(1/1)*r", "r") is True
    assert _expressions_collide("(x + 1)**2", "x**2 + 2*x + 1") is True
    assert _expressions_collide("sin(x)**2 + cos(x)**2", "1") is False  # free_symbols mismatch (x vs empty)
    assert _expressions_collide("2*x + 3", "2*x + 4") is False
    assert _expressions_collide("a/6", "a/3") is False

    # _ver_equiv: exact identities, transcendental equivalence, and strict non-equivalence
    assert _ver_equiv("(x + 1)**2", "x**2 + 2*x + 1", variables=["x"]) is True
    assert _ver_equiv("exp(2*n*t)", "(exp(n*t))**2", variables=["n", "t"]) is True
    assert _ver_equiv("log(a*b)", "log(a) + log(b)", variables=["a", "b"]) is True
    assert _ver_equiv("2*x", "x**2", variables=["x"]) is False
    assert _ver_equiv("2*x + y", "2*x", variables=["x"]) is False  # undeclared variable y rejected
    assert _ver_equiv("1/2", "0.5") is True
    assert _ver_equiv("1/3", "0.5") is False


def test_find_pending_shards_idempotent_on_resume(tmp_path: Path):
    import ast
    import json
    from typing import List, Optional

    wf_path = ROOT_DIR / ".agents" / "skills" / "content-to-course" / "workflows" / "c2c_wave_workflow.py"
    tree = ast.parse(wf_path.read_text(encoding="utf-8"), filename=str(wf_path))
    fn_node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_find_pending_shards")
    mod = ast.Module(body=[fn_node], type_ignores=[])
    ns: dict = {"Path": Path, "Optional": Optional, "List": List, "json": json}
    exec(compile(mod, str(wf_path), "exec"), ns)
    find_pending = ns["_find_pending_shards"]

    # 1. No manifest -> None (must run Stage 2 sharding)
    assert find_pending(tmp_path) is None

    # 2. Manifest with 2 shards, only shard_01.json compiled -> ["shard_02"]
    shards_dir = tmp_path / "shards"
    shards_dir.mkdir(parents=True)
    (shards_dir / "pre_shard_manifest.json").write_text(
        json.dumps({"shards": [{"shard_id": "shard_01"}, {"shard_id": "shard_02"}]}),
        encoding="utf-8",
    )
    (shards_dir / "shard_01.cert.json").write_text('{"ok": true}', encoding="utf-8")
    assert find_pending(tmp_path) == ["shard_02"]

    # 3. Both compiled and non-empty -> [] (skip Stage 2 & 3)
    (shards_dir / "shard_02.cert.json").write_text('{"ok": true}', encoding="utf-8")
    assert find_pending(tmp_path) == []


def test_katex_collapses_variable_plus_minus_without_breaking_pm():
    from engine.assemble import sanitize_katex_syntax
    from engine.katex_ast import canonicalize_algebraic_katex

    collapsed = canonicalize_algebraic_katex(r"q=23-8p+-5\dot{p}", whole_is_math=True)
    assert "+-" not in collapsed
    assert r"8p- 5\dot{p}" in collapsed

    sanitized = sanitize_katex_syntax(r"Demanda $q=23-8p+-5\dot{p}$ y rango $x \pm 5$.")
    assert "+-" not in sanitized
    assert r"\pm 5" in sanitized


def test_qa_dag_overlap_excludes_concept_to_skill_prerequisite_pair():
    import importlib.util

    qa_path = ROOT_DIR / ".agents" / "skills" / "course-qa-evaluator" / "scripts" / "standardized_audit_engine.py"
    spec = importlib.util.spec_from_file_location("standardized_audit_engine", qa_path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules["standardized_audit_engine"] = mod
    spec.loader.exec_module(mod)
    linter = mod.ArchitectureDAGLinter

    c08 = {"id": "C-08", "type": "Concept", "name": "Transversalidad con Estado Final Libre", "prerequisites": ["C-05"]}
    hab04 = {"id": "Hab-04", "type": "Skill", "name": "Transversalidad en Horizonte Finito e Instante Final Libre", "prerequisites": ["C-08"]}
    assert linter._are_competencies_duplicate(c08, hab04) is False

    c12 = {"id": "C-12", "type": "Concept", "name": "Principio del Máximo y Soluciones de Esquina", "description": "Condiciones necesarias del principio del máximo en control óptimo."}
    c13 = {"id": "C-13", "type": "Concept", "name": "Hamiltoniano y Principio del Máximo", "description": "Condiciones necesarias del principio del máximo en control óptimo."}
    assert linter._are_competencies_duplicate(c12, c13) is True


def test_lean_cta_prompts_preserve_lf_and_new_rules():
    lean_dir = ROOT_DIR / ".agents" / "skills" / "content-to-course" / "system_prompts" / "lean"
    arch_bytes = (lean_dir / "prompt_cta_architect.md").read_bytes()
    harm_bytes = (lean_dir / "prompt_cta_harmonizer.md").read_bytes()
    assert b"\r\n" not in arch_bytes
    assert b"\r\n" not in harm_bytes
    assert "100% simbólico/conceptual" in arch_bytes.decode("utf-8")
    assert "Desambiguación obligatoria en misma categoría" in harm_bytes.decode("utf-8")


def test_unstructured_model_duplicate_options_caught_by_invariants():
    from engine.invariants import check_instance_invariants

    inst = {
        "interaction_type": "unstructured_model",
        "stem": "Formule el modelo de crecimiento óptimo con daño ambiental.",
        "hints": [
            "Identifique la variable de control y su derivada.",
            "Escriba el funcional integrando utilidad y daño.",
            "Derive la condición de Euler respecto al control.",
        ],
        "detailed_solution": "Se obtiene la condición $F_{\\dot{K}} = -e^{-5 t}\\frac{1}{C}$.",
        "unstructured_model": {
            "phase1_variables": {
                "roles": ["estado", "control"],
                "items": [
                    {"id": "V1", "label": "$K(t)$", "correct_role": "estado"},
                    {"id": "V2", "label": "$C(t)$", "correct_role": "control"},
                ],
            },
            "phase2_assumptions": {
                "options": [
                    {"id": "A1", "content": "Utilidad logarítmica $U(C)=\\ln C$.", "is_correct": True},
                    {"id": "A2", "content": "Tasa de descuento negativa.", "is_correct": False, "error_rationale": "La tasa $\\rho$ es positiva en este horizonte."},
                ]
            },
            "phase3_formulation": {
                "mode": "select",
                "options": [
                    {"id": "F1", "content": r"$F_{\dot{K}} = -e^{-5 t}\frac{1}{C}$", "is_correct": True},
                    {"id": "F4", "content": r"$F_{\dot{K}} = -e^{-5 t}\frac{1}{C}$", "is_correct": False, "error_rationale": r"Confunde el signo o factor del consumo $C$ en $F_{\dot{K}}$."},
                    {"id": "F2", "content": r"$F_{\dot{K}} = e^{-5 t}\frac{1}{C}$", "is_correct": False, "error_rationale": r"Omite el signo negativo de $\partial C / \partial \dot{K}$."},
                ],
            },
        },
    }
    ok, errs = check_instance_invariants(inst, "unstructured_model")
    assert ok is False
    assert any("Duplicate option content detected in unstructured_model.phase3_formulation" in e for e in errs), errs


def test_degenerate_literal_cond_extended_to_solution_and_proof_dag():
    from engine.invariants import check_instance_invariants

    inst = {
        "interaction_type": "proof_dag",
        "stem": "Clasifique el funcional $V[y]=\\int_0^3 (7y'+5t)\\,dt + 3y(3)^2$.",
        "hints": [
            "Observe el integrando y el término terminal.",
            "Compare las definiciones de Bolza, Lagrange y Mayer.",
            "Verifique qué término permanece activo.",
        ],
        "detailed_solution": "Si $5=0$, desaparece el término terminal.",
        "proof_dag": {
            "steps": [
                {"id": "S1", "content": "Contiene término integral y terminal.", "is_fallacy": False},
                {"id": "S2", "content": "En el caso en que se anula el coeficiente $5$, se reduce a Lagrange.", "is_fallacy": False},
                {"id": "S3", "content": "Por tanto es un problema de Bolza.", "is_fallacy": False},
            ],
            "edges": [["S1", "S2"], ["S2", "S3"]],
        },
    }
    ok, errs = check_instance_invariants(inst, "proof_dag")
    assert ok is False
    degen_errs = [e for e in errs if "TPL-DEGENERATE-LITERAL-COND" in e]
    assert any("detailed_solution" in e for e in degen_errs), degen_errs
    assert any("proof_dag.step[2]" in e for e in degen_errs), degen_errs


def test_check_cta_flags_static_example_in_remediation_hint():
    import check_cta

    bad_cta = {
        "contract_version": 2,
        "competencies": [
            {
                "id": "Hab-01",
                "type": "skill",
                "name": "Ecuación de Euler",
                "description_latex": "Resuelve la ecuación de Euler para funcionales cuadráticos con fronteras fijas en intervalos dados.",
                "target_bloom": "Evaluate",
                "doc": "doc.pdf",
                "page": 1,
                "prerequisites": [],
                "assumptions": [{"id": "A-Hab01-01", "statement_latex": "$F \\in C^2$ en todo el intervalo.", "violation_consequence": "Pueden existir esquinas."}],
                "recommended_modalities": ["fill_in_the_blank", "open_symbolic"],
                "distractors": [
                    {
                        "id": "D-Hab01-01",
                        "name": "Frontera fija errónea",
                        "wrong_belief": "Evalúa en el extremo erróneo",
                        "correct_belief": "Evalúa en t=T",
                        "manifestation": "Usa t=1 en vez de t=T",
                        "remediation_hint": "Sustituya $t=4$ en $x(4)=4$ y despeje $c_1$ con cuidado en la frontera.",
                        "omitted_step": "Evaluar x(T)",
                    }
                ],
            }
        ],
    }
    warns: list[str] = []
    check_cta._validate_competencies_rules(bad_cta["competencies"], warnings=warns)
    assert any("CTA-HINT-STATIC-EXAMPLE" in w for w in warns), warns


def test_c2c_wave_workflow_batches_stage3_authors_to_9():
    wf_txt = (ROOT_DIR / ".agents" / "skills" / "content-to-course" / "workflows" / "c2c_wave_workflow.py").read_text(encoding="utf-8")
    assert "max_concurrent_batch: int = 0" in wf_txt
    assert 'int(_WF_ARGS.get("author_concurrency") or _WF_ARGS.get("author_wave_size") or 9)' in wf_txt
    assert "max_concurrency=author_conc" in wf_txt
    assert "max_concurrent_batch=0" in wf_txt
