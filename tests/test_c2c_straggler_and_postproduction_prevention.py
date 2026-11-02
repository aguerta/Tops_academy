"""Tests for prevention of Straggler, Post-Production, and Quality Gate incidents:
1. Raw LaTeX commands exposed outside $...$ (vdirect5 incident).
2. KaTeX prose overflow in text macros > 45 chars (vmapreduce5 incident).
3. Early detection of static mono-keys [TPL-STATIC-OPT] in compile_shard.py (vmapreduce12 Shard 15 incident).
4. Detection of magic multipliers [DIAG-MAGIC-MULT] in compile_shard.py without has_mult_ast limitation (vmapreduce12 C-06 and Hab-12 incident).
"""

import json
import sys
import textwrap
from pathlib import Path

# Add content-to-course skill directory to sys.path
_c2c_root = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "content-to-course"
if str(_c2c_root) not in sys.path:
    sys.path.insert(0, str(_c2c_root))

import pytest
from engine.invariants import validate_katex_syntax
from compile_shard import compile_shard


def test_invariants_flags_raw_latex_outside_dollars():
    # vdirect5 shard_13 incident
    bad_item = r"\operatorname{Var}(Y_i) = \infty \Rightarrow Z_n \xrightarrow{d} N(0, 1)"
    errors = validate_katex_syntax(bad_item, "distractor_value")
    assert any("exposed outside '$...$' delimiters" in e for e in errors)
    assert any(r"\operatorname" in e for e in errors)

    # properly delimited passes
    good_item = r"$\operatorname{Var}(Y_i) = \infty \Rightarrow Z_n \xrightarrow{d} N(0, 1)$"
    assert validate_katex_syntax(good_item, "distractor_value") == []


def test_invariants_flags_katex_prose_overflow():
    # vmapreduce5 shard_23 incident
    bad_prose = r"$\text{Insesgadez en } n=@n_val@ \succ \text{Consistencia, siendo preferible en muestras grandes}$"
    errors = validate_katex_syntax(bad_prose, "distractor_value", allow_template_vars=True)
    assert any("[KATEX-PROSE-OVERFLOW]" in e for e in errors)

    # under 45 chars passes
    good_prose = r"Insesgadez en $n=@n_val@ \succ$ consistencia"
    assert validate_katex_syntax(good_prose, "distractor_value", allow_template_vars=True) == []


def test_validate_katex_syntax_tolerates_normal_text_without_latex():
    normal_text = "El rendimiento termodinámico de Carnot es adimensional."
    assert validate_katex_syntax(normal_text, "explanation") == []


def test_compile_shard_diagnoses_exposed_latex_in_distractor(tmp_path):
    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    shards_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "shards": [
            {
                "shard_id": "shard_01",
                "competencies": [
                    {
                        "id": "H-01",
                        "name": "Eficiencia de Carnot",
                        "knowledge_component": "Termodinámica",
                        "distractor_ids": ["D-H01-01", "D-H01-02", "D-H01-03", "D-H01-04", "D-H01-05", "D-H01-06"]
                    }
                ]
            }
        ]
    }
    (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (work_dir / "cta.json").write_text(json.dumps({"competencies": manifest["shards"][0]["competencies"]}), encoding="utf-8")

    shard_file = shards_dir / "shard_01_data.py"
    shard_file.write_text(
        textwrap.dedent(r"""
            def gen_h01(rng):
                ans = 0.5
                return {
                    "vars": {"ans": ans, "d1": 0.25},
                    "correct": r"$\eta = @ans@$",
                    "distractors": [
                        ("D-H01-01", r"\operatorname{Var}(Y) = 1", r"Error conceptual en varianza @ans@"),
                        ("D-H01-02", r"$\eta = 0.2$", r"Error 2 con @ans@"),
                        ("D-H01-03", r"$\eta = 0.3$", r"Error 3 con @ans@"),
                        ("D-H01-04", r"$\eta = 0.4$", r"Error 4 con @ans@"),
                        ("D-H01-05", r"$\eta = 0.6$", r"Error 5 con @ans@"),
                        ("D-H01-06", r"$\eta = 0.7$", r"Error 6 con @ans@"),
                    ]
                }
            def ver_h01(res):
                return res.get("vars", {}).get("ans") == 0.5

            TEMPLATES = [
                ("T-H01-01", "H-01", "multiple_choice", gen_h01, ver_h01, ("easy", "Remember"),
                 [r"Stem 1 @ans@", r"Stem 2 @ans@", r"Stem 3 @ans@"],
                 ["Hint 1 con texto largo...", "Hint 2 con texto largo...", "Hint 3 con texto largo..."],
                 r"Solución $\eta = @ans@$"),
            ]
        """).strip(),
        encoding="utf-8"
    )

    out_json = work_dir / "templates" / "H-01.json"
    success, errors = compile_shard(
        work_dir_or_path=work_dir,
        shard_id="shard_01",
        strict=False
    )
    assert not success
    assert any("[TPL-KATEX]" in e and r"\operatorname" in e for e in errors)


def test_compile_shard_diagnoses_static_mono_key(tmp_path):
    # vmapreduce12 Shard 15 incident: static Cauchy-Schwarz ans = 1 across all seeds
    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    shards_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "shards": [
            {
                "shard_id": "shard_02",
                "competencies": [
                    {
                        "id": "C-05",
                        "name": "Cauchy-Schwarz",
                        "knowledge_component": "Probabilidad",
                        "distractor_ids": ["D-C05-01", "D-C05-02", "D-C05-03", "D-C05-04", "D-C05-05", "D-C05-06"],
                        "distractors": [{"id": f"D-C05-0{i}", "wrong_belief": f"W{i}"} for i in range(1, 7)]
                    }
                ]
            }
        ]
    }
    (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (work_dir / "cta.json").write_text(json.dumps({"competencies": manifest["shards"][0]["competencies"]}), encoding="utf-8")

    shard_file = shards_dir / "shard_02_data.py"
    shard_file.write_text(
        textwrap.dedent(r"""
            def gen_c05(rng):
                # Mono-clave invariante: ans = 1 siempre estático
                ex = rng.randint(2, 20)
                return {
                    "vars": {"ex": ex, "ans": 1},
                    "correct": r"$|\rho_{XY}| \le 1$",
                    "distractors": [
                        ("D-C05-01", r"$|\rho_{XY}| \le 0.5$", r"Cota errónea estimada para el parámetro @ex@."),
                        ("D-C05-02", r"$|\rho_{XY}| \le 2.0$", r"Cota errónea estimada para el parámetro @ex@."),
                        ("D-C05-03", r"$|\rho_{XY}| \le 0.0$", r"Cota errónea estimada para el parámetro @ex@."),
                        ("D-C05-04", r"$|\rho_{XY}| \le 1.5$", r"Cota errónea estimada para el parámetro @ex@."),
                        ("D-C05-05", r"$|\rho_{XY}| \le 3.0$", r"Cota errónea estimada para el parámetro @ex@."),
                        ("D-C05-06", r"$|\rho_{XY}| \le 4.0$", r"Cota errónea estimada para el parámetro @ex@."),
                    ]
                }
            def ver_c05(res):
                return res.get("vars", {}).get("ans") == 1

            TEMPLATES = [
                ("T-C05-01", "C-05", "multiple_choice", gen_c05, ver_c05, ("easy", "Remember"),
                 [r"Stem 1 @ex@", r"Stem 2 @ex@", r"Stem 3 @ex@"],
                 ["Hint 1 con texto largo...", "Hint 2 con texto largo...", "Hint 3 con texto largo..."],
                 r"Solución con @ex@"),
            ]
        """).strip(),
        encoding="utf-8"
    )

    success, errors = compile_shard(
        work_dir_or_path=work_dir,
        shard_id="shard_02",
        strict=True,
        min_archetypes=1
    )
    assert not success
    assert any("[TPL-STATIC-OPT]" in e and "mono-clave" in e.lower() for e in errors)


def test_compile_shard_diagnoses_magic_multipliers_without_ans_variable(tmp_path):
    # vmapreduce12 Hab-12 incident: variable not named 'ans' but produces magic multiplier ratios
    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    shards_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "shards": [
            {
                "shard_id": "shard_03",
                "competencies": [
                    {
                        "id": "H-12",
                        "name": "Error Estándar Asintótico",
                        "knowledge_component": "Inferencia",
                        "distractor_ids": ["D-H12-01", "D-H12-02", "D-H12-03", "D-H12-04", "D-H12-05", "D-H12-06"],
                        "distractors": [{"id": f"D-H12-0{i}", "wrong_belief": f"W{i}"} for i in range(1, 7)]
                    }
                ]
            }
        ]
    }
    (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    (work_dir / "cta.json").write_text(json.dumps({"competencies": manifest["shards"][0]["competencies"]}), encoding="utf-8")

    shard_file = shards_dir / "shard_03_data.py"
    shard_file.write_text(
        textwrap.dedent(r"""
            def gen_h12(rng):
                # Generador que calcula SE pero usa multiplicadores sintéticos (1.333 y 0.667)
                n = rng.randint(50, 200)
                se_est = round(10.0 / (n ** 0.5), 3)
                v_dict = {"n": n, "se": se_est}
                # Multiplicadores prohibidos sin usar la palabra 'ans' en el código
                d1 = round(se_est * 1.333, 3)
                d2 = round(se_est * 0.667, 3)
                d3 = round(se_est * 1.667, 3)
                d4 = round(se_est * 0.333, 3)
                d5 = round(se_est + 5.0, 3)
                d6 = round(se_est + 10.0, 3)
                v_dict.update({"d1": d1, "d2": d2, "d3": d3, "d4": d4, "d5": d5, "d6": d6})
                return {
                    "vars": v_dict,
                    "correct": r"$\text{SE} = @se@$",
                    "distractors": [
                        ("D-H12-01", r"$\text{SE} = @d1@$", r"Error conceptual en el cálculo para @n@."),
                        ("D-H12-02", r"$\text{SE} = @d2@$", r"Error conceptual en el cálculo para @n@."),
                        ("D-H12-03", r"$\text{SE} = @d3@$", r"Error conceptual en el cálculo para @n@."),
                        ("D-H12-04", r"$\text{SE} = @d4@$", r"Error conceptual en el cálculo para @n@."),
                        ("D-H12-05", r"$\text{SE} = @d5@$", r"Error conceptual en el cálculo para @n@."),
                        ("D-H12-06", r"$\text{SE} = @d6@$", r"Error conceptual en el cálculo para @n@."),
                    ]
                }
            def ver_h12(res):
                return res.get("vars", {}).get("se") is not None

            TEMPLATES = [
                ("T-H12-01", "H-12", "multiple_choice", gen_h12, ver_h12, ("easy", "Remember"),
                 [r"Stem 1 @n@", r"Stem 2 @n@", r"Stem 3 @n@"],
                 ["Hint 1 con texto largo...", "Hint 2 con texto largo...", "Hint 3 con texto largo..."],
                 r"Solución con @n@"),
            ]
        """).strip(),
        encoding="utf-8"
    )

    success, errors = compile_shard(
        work_dir_or_path=work_dir,
        shard_id="shard_03",
        strict=True,
        min_archetypes=1
    )
    assert not success
    assert any("[DIAG-MAGIC-MULT]" in e for e in errors)


