"""Unit and integration tests for:
1. Pre-Publish Quality Gate `specific_error_report` (line-mapped by rule/linter, template_id, item_id, offending lines, and proposed repair command).
2. `dispatch.py` (`dispatch-repair`) ingestion of `specific_error_report.json` into repair work orders.
3. `compile_shard.py` enforcement of `[STEM-DIVERSITY-GATE]` (rejecting 9-stem competencies before `run.py --stage build`).
4. `compile_shard.py` enforcement of `[DIAG-MAGIC-MULT]` (rejecting magic-multiplier distractors before `run.py --stage publish`).
"""

import json
import sys
from pathlib import Path
import pytest

_repo_root = Path(__file__).resolve().parents[1]
_skill_root = _repo_root / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

_src_root = _repo_root / "src"
if str(_src_root) not in sys.path:
    sys.path.insert(0, str(_src_root))

from compile_shard import compile_shard
from course_publisher import CoursePublisher, PublishQualityGateError, build_specific_error_report
from dispatch import dispatch_repair


def _create_isolated_workspace(tmp_path: Path, cid: str = "Hab-01", ctype: str = "skill"):
    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    templates_dir = work_dir / "templates"
    shards_dir.mkdir(parents=True, exist_ok=True)
    templates_dir.mkdir(parents=True, exist_ok=True)

    cta_payload = {
        "title": "Curso de Prueba",
        "competencies": [
            {
                "id": cid,
                "name": f"Competencia {cid}",
                "type": ctype,
                "distractors": [
                    {"id": f"D-{cid.replace('-', '')}-0{i}", "remediation_hint": f"Error conceptual {i} en el cálculo."}
                    for i in range(1, 7)
                ],
            }
        ],
    }
    cta_file = work_dir / "cta.json"
    cta_file.write_text(json.dumps(cta_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    manifest_payload = {
        "min_archetypes": 3,
        "shards": [
            {
                "shard_id": "shard_01",
                "competency_ids": [cid],
                "shard_data_path": str((shards_dir / "shard_01_data.py").resolve().as_posix()),
                "templates_dir": str(templates_dir.resolve().as_posix()),
                "competencies": cta_payload["competencies"],
            }
        ],
    }
    manifest_file = shards_dir / "pre_shard_manifest.json"
    manifest_file.write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return work_dir, shards_dir, templates_dir, cta_file, manifest_file


def test_compile_shard_rejects_9_stems_skill_with_stem_diversity_gate(tmp_path: Path):
    """Verifies that a 3-archetype Skill shard with only 3 stems per template (9 total < 15 required)
    fails at compile_shard with [STEM-DIVERSITY-GATE] and exact line numbers.
    """
    work_dir, shards_dir, _, cta_file, _ = _create_isolated_workspace(tmp_path, cid="Hab-01", ctype="skill")
    shard_py = shards_dir / "shard_01_data.py"

    code = r'''
import random

def gen_1(rng):
    a = rng.randint(20, 120)
    b = rng.randint(5, 30)
    ans = a + b * 2
    ds = [a + b + i * 3 for i in range(1, 7)]
    v = {"a": a, "b": b, "ans": ans, **{f"d{i}": d for i, d in enumerate(ds, 1)}}
    dists = [(f"D-Hab01-0{i}", rf"$y = @d{i}@$", rf"Desvío aditivo con base @a@ y factor @b@ en paso {i}.") for i in range(1, 7)]
    return {"vars": v, "correct": r"$y = @ans@$", "distractors": dists}

def ver_1(res): return res.get("correct") == r"$y = @ans@$" and res["vars"]["ans"] == res["vars"]["a"] + res["vars"]["b"] * 2

def gen_2(rng):
    a = rng.randint(30, 150)
    b = rng.randint(4, 25)
    ans = a * 2 - b
    return {"vars": {"a": a, "b": b, "ans": ans}, "correct": str(ans), "distractors": []}

def ver_2(res): return res.get("correct") == str(res["vars"]["ans"]) and res["vars"]["ans"] == res["vars"]["a"] * 2 - res["vars"]["b"]

def gen_3(rng):
    a = rng.randint(15, 95)
    b = rng.randint(3, 20)
    ans = a + b * 3
    return {"vars": {"a": a, "b": b, "ans": ans}, "correct": str(ans), "distractors": []}

def ver_3(res): return res.get("correct") == str(res["vars"]["ans"]) and res["vars"]["ans"] == res["vars"]["a"] + res["vars"]["b"] * 3

s1 = [
    r"Calcule el valor directo cuando $a = @a@$ y $b = @b@$:",
    r"Determine la combinación lineal frontal para $a = @a@$ y $b = @b@$:",
    r"Halle el resultado directo dados los parámetros $a = @a@$ y $b = @b@$:",
]
s2 = [
    r"En el planteamiento inverso con $a = @a@$ y $b = @b@$, calcule el término:",
    r"A partir de la cota inversa con $a = @a@$ y $b = @b@$, obtenga el valor:",
    r"Deduzca la magnitud inversa asociada a $a = @a@$ y $b = @b@$:",
]
s3 = [
    r"Bajo una perturbación con $a = @a@$ y $b = @b@$, evalúe el resultado:",
    r"Determine el efecto perturbativo total cuando $a = @a@$ y $b = @b@$:",
    r"Calcule el estado perturbado del sistema con $a = @a@$ y $b = @b@$:",
]
hints = [
    "Identifique los parámetros de entrada y la relación lineal correspondiente.",
    "Sustituya los valores numéricos respetando la jerarquía de operaciones.",
    "Verifique la consistencia algebraica del término resultante final.",
]

TEMPLATES = [
    ("T-Hab01-01", "Hab-01", "multiple_choice_7_options", gen_1, ver_1, ("easy", "Remember"), s1, hints, "Solución @ans@."),
    ("T-Hab01-02", "Hab-01", "fill_in_the_blank", gen_2, ver_2, ("medium", "Apply"), s2, hints, "Solución @ans@."),
    ("T-Hab01-03", "Hab-01", "fill_in_the_blank", gen_3, ver_3, ("hard", "Analyze"), s3, hints, "Solución @ans@."),
]
'''
    shard_py.write_text(code, encoding="utf-8")
    ok, errors = compile_shard(work_dir, shard_id="shard_01", strict=True, min_archetypes=3, cta_path=cta_file, seeds=50)
    assert not ok, "Expected compile_shard to reject 9-stem skill competency"
    err_str = "\n".join(errors)
    assert "[STEM-DIVERSITY-GATE]" in err_str
    assert "only 9 stems, required >=" in err_str
    assert "distinct syntactic stems per template" in err_str


def test_compile_shard_rejects_magic_multiplier_distractors_with_line_numbers(tmp_path: Path):
    """Verifies that a generator scaling `ans` by prohibited magic multipliers (`0.667`, `1.333`)
    is rejected during compile_shard with [DIAG-MAGIC-MULT] and exact line numbers.
    """
    work_dir, shards_dir, _, cta_file, _ = _create_isolated_workspace(tmp_path, cid="C-01", ctype="concept")
    shard_py = shards_dir / "shard_01_data.py"

    code = r'''
import random

def gen_c01_1(rng):
    mu = rng.randint(15, 65)
    delta = mu + rng.randint(20, 95)
    ans = round(mu / delta, 3)
    ds = [
        round(ans * 0.667, 3),
        round(ans * 1.333, 3),
        round(ans * 0.75, 3),
        round(ans * 1.25, 3),
        round(ans * 0.5, 3),
        round(ans * 1.5, 3),
    ]
    v = {"mu": mu, "delta": delta, "ans": ans, **{f"d{i}": d for i, d in enumerate(ds, 1)}}
    dists = [(f"D-C01-0{i}", rf"$p = @d{i}@$", rf"Desvío conceptual sobre mu=@mu@ y delta=@delta@ en caso {i}.") for i in range(1, 7)]
    return {"vars": v, "correct": r"$p = @ans@$", "distractors": dists}

def ver_c01_1(res): return res.get("correct") == r"$p = @ans@$" and abs(res["vars"]["ans"] - round(res["vars"]["mu"] / res["vars"]["delta"], 3)) < 1e-6

def gen_c01_2(rng):
    mu = rng.randint(20, 90)
    ans = mu * 2
    return {"vars": {"mu": mu, "ans": ans}, "correct": str(ans), "distractors": []}

def ver_c01_2(res): return res["vars"]["ans"] == res["vars"]["mu"] * 2

def gen_c01_3(rng):
    mu = rng.randint(25, 110)
    ans = mu * 3
    return {"vars": {"mu": mu, "ans": ans}, "correct": str(ans), "distractors": []}

def ver_c01_3(res): return res["vars"]["ans"] == res["vars"]["mu"] * 3

s1 = [
    r"Consigna 1 directa para $\mu = @mu@$ y $\delta = @delta@$:",
    r"Consigna 2 frontal con esperanza $\mu = @mu@$ y cota $\delta = @delta@$:",
    r"Consigna 3 analítica evaluando $\mu = @mu@$ frente a $\delta = @delta@$:",
    r"Consigna 4 teórica sobre el cociente con $\mu = @mu@$ y $\delta = @delta@$:",
]
s2 = [
    r"En el caso inverso 1 con parámetro $\mu = @mu@$, halle el doble:",
    r"En el caso inverso 2 dado $\mu = @mu@$, calcule la escala doble:",
    r"En el caso inverso 3 para $\mu = @mu@$, determine el resultado:",
    r"En el caso inverso 4 bajo $\mu = @mu@$, obtenga la magnitud:",
]
s3 = [
    r"Bajo perturbación 1 con $\mu = @mu@$, determine el triple:",
    r"Bajo perturbación 2 fijando $\mu = @mu@$, evalúe la cota:",
    r"Bajo perturbación 3 para $\mu = @mu@$, calcule el valor:",
    r"Bajo perturbación 4 considerando $\mu = @mu@$, halle el total:",
]
hints = [
    "Identifique los parámetros relevantes del modelo probabilístico.",
    "Aplique la relación funcional correspondiente al arquetipo.",
    "Verifique la consistencia numérica del resultado obtenido.",
]

TEMPLATES = [
    ("T-C01-01", "C-01", "multiple_choice_7_options", gen_c01_1, ver_c01_1, ("easy", "Remember"), s1, hints, "Sol @ans@."),
    ("T-C01-02", "C-01", "fill_in_the_blank", gen_c01_2, ver_c01_2, ("medium", "Understand"), s2, hints, "Sol @ans@."),
    ("T-C01-03", "C-01", "fill_in_the_blank", gen_c01_3, ver_c01_3, ("hard", "Apply"), s3, hints, "Sol @ans@."),
]
'''
    shard_py.write_text(code, encoding="utf-8")
    ok, errors = compile_shard(work_dir, shard_id="shard_01", strict=True, min_archetypes=3, cta_path=cta_file, seeds=50)
    assert not ok, "Expected compile_shard to reject magic-multiplier distractors"
    err_str = "\n".join(errors)
    assert "[DIAG-MAGIC-MULT]" in err_str
    assert "T-C01-01" in err_str
    assert "gen_c01_1" in err_str


def test_specific_error_report_and_dispatch_repair_integration(tmp_path: Path):
    """Verifies that `build_specific_error_report` produces a grouped, line-mapped report
    with template_id, item_id, offending lines, and proposed repair command, and that
    `dispatch_repair` ingests `specific_error_report.json` into the repair work order.
    """
    work_dir, shards_dir, templates_dir, cta_file, _ = _create_isolated_workspace(tmp_path, cid="H-04", ctype="fact")
    shard_py = shards_dir / "shard_01_data.py"

    shard_code = r'''"""Shard 01 data for H-04."""
import random

def gen_h04_1(rng):
    sigma = rng.randint(5, 30)
    eps = sigma + rng.randint(5, 45)
    var_x = sigma * sigma
    ans = round(var_x / (eps * eps), 4)
    ds = [round(ans * 0.667, 4), round(ans * 1.333, 4), round(ans * 0.75, 4),
          round(ans * 1.25, 4), round(ans * 0.5, 4), round(ans * 1.5, 4)]
    v = {"sigma": sigma, "eps": eps, "var_x": var_x, "ans": ans, **{f"d{i}": d for i, d in enumerate(ds, 1)}}
    dists = [
        ("D-H04-01", r"$P \le @d1@$", r"Omite elevar el margen @eps@ al cuadrado."),
        ("D-H04-02", r"$P \le @d2@$", r"Usa desviación típica @sigma@ en vez de varianza."),
        ("D-H04-03", r"$P \le @d3@$", r"Asume normalidad para @sigma@."),
        ("D-H04-04", r"$P \le @d4@$", r"Decaimiento lineal con @eps@."),
        ("D-H04-05", r"$P \le @d5@$", r"Invierte el evento con @eps@."),
        ("D-H04-06", r"$P \le @d6@$", r"Omite valor absoluto con @eps@.")
    ]
    return {"vars": v, "correct": r"$P \le @ans@$", "distractors": dists}

def ver_h04_1(res): return True

s1 = [r"Enunciado 1 @var_x@ @eps@", r"Enunciado 2 @var_x@ @eps@", r"Enunciado 3 @var_x@ @eps@", r"Enunciado 4 @var_x@ @eps@"]
h1 = ["Pista 1 suficientemente larga", "Pista 2 suficientemente larga", "Pista 3 suficientemente larga"]

TEMPLATES = [
    ("T-H04-01", "H-04", "multiple_choice_7_options", gen_h04_1, ver_h04_1, ("easy", "Remember"), s1, h1, "Sol @ans@."),
]
'''
    shard_py.write_text(shard_code, encoding="utf-8")
    (templates_dir / "H-04.json").write_text(
        json.dumps({"competency_id": "H-04", "templates": [{"id": "T-H04-01", "difficulty": "easy", "interaction_type": "multiple_choice_7_options"}]}),
        encoding="utf-8",
    )

    course_data = {
        "course_id": "test_course",
        "competencies": [{"id": "H-04", "name": "Chebyshev", "category": "Fact"}],
        "questions": [
            {
                "id": "Q-H04-207",
                "competency_id": "H-04",
                "template_id": "T-H04-01",
                "difficulty": "easy",
                "bloom": "Remember",
                "interaction_type": "multiple_choice_7_options",
                "stem": "Calcule la cota de Chebyshev",
            }
        ],
    }
    (work_dir / "course.json").write_text(json.dumps(course_data, indent=2), encoding="utf-8")

    audit_report = {
        "course_id": "test_course",
        "issues": [
            {
                "linter": "diagnostic_rationale_alignment_linter",
                "dimension": "D2_assessment",
                "severity": "critical",
                "item_id": "Q-H04-207",
                "competency_id": "H-04",
                "message": "Distractores numéricos sintéticos por multiplicador arbitrario ([0.667, 1.333]) con error_rationale desconectado del cálculo real.",
                "snippet": "$P \\le 0.15$",
            }
        ],
    }

    payload = build_specific_error_report(
        audit_report=audit_report,
        course_data=course_data,
        work_dir=work_dir,
        gate_failures=["Critical audit issues detected (1)"],
    )
    report_text = payload["report_text"]

    assert (work_dir / "specific_error_report.md").is_file()
    assert (work_dir / "specific_error_report.json").is_file()
    assert "[-] [DIAG-MAGIC-MULT / diagnostic_rationale_alignment_linter]" in report_text
    assert "template_id=T-H04-01" in report_text
    assert "item_ids=Q-H04-207" in report_text
    assert "Fn gen_h04_1: L4..L20" in report_text
    assert "CONTEXTO EXACTO (OFFENDING LINES)" in report_text
    assert "dispatch.py dispatch-repair" in report_text
    assert payload["failing_competencies"] == ["H-04"]

    # Now verify dispatch_repair ingests specific_error_report.json into the repair work order
    res = dispatch_repair(work_dir=work_dir, ids=["H-04"])
    assert len(res["Subagents"]) == 1
    repair_wo = json.loads((work_dir / "prompts" / "repair" / "repair_h04.json").read_text(encoding="utf-8"))
    prompt_str = repair_wo["Prompt"]
    assert "specific_error_report" in prompt_str
    assert "T-H04-01" in prompt_str
    assert "Q-H04-207" in prompt_str
    assert "gen_h04_1" in prompt_str
    assert "CONTEXTO EXACTO (OFFENDING LINES)" in prompt_str


def test_blind_judge_stratified_random_max_20_items_max_10_judges(tmp_path: Path):
    """Verifies that `generate_judge_batch`, `split_judge_batch`, and `dispatch_judges`:
    - Enforce max 20 questions per judge and max 10 judges in total (<= 200 items total).
    - Guarantee >= 1 random instance per template/competency via stratified random selection.
    - Randomize seeds and item ordering across runs.
    """
    from judge import generate_judge_batch, split_judge_batch
    from dispatch import dispatch_judges

    work_dir = tmp_path / "work"
    templates_dir = work_dir / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)

    # Create 25 competencies x 3 templates = 75 templates (75 * 3 = 225 candidate items > 200 cap)
    all_tpl_ids = set()
    all_comp_ids = set()
    for c_idx in range(1, 26):
        cid = f"C-{c_idx:02d}"
        all_comp_ids.add(cid)
        t_list = []
        for a_idx in range(1, 4):
            tid = f"T-C{c_idx:02d}-0{a_idx}"
            all_tpl_ids.add(tid)
            t_list.append({
                "id": tid,
                "competency_id": cid,
                "interaction_type": "fill_in_the_blank",
                "stem": f"Calcule el valor {{val}} para {tid}",
                "hints": ["Pista 1", "Pista 2", "Pista 3"],
                "detailed_solution": "Sol {val}",
                "generate_py": (
                    "def generate(rng):\n"
                    "    v = rng.randint(100, 999999)\n"
                    "    return {'vars': {'val': v}, 'correct': v, 'equivalents': [str(v)]}\n"
                ),
            })
        (templates_dir / f"{cid}.json").write_text(
            json.dumps({"competency_id": cid, "templates": t_list}),
            encoding="utf-8",
        )

    batch_p, gt_p = generate_judge_batch(templates_path=templates_dir, work_dir=work_dir, random_seed=12345)
    batch_1 = json.loads(batch_p.read_text(encoding="utf-8"))
    gt_1 = json.loads(gt_p.read_text(encoding="utf-8"))

    # Total items capped at 10 judges * 20 items = 200
    assert len(batch_1) == 200
    assert len(gt_1) == 200

    # Every single one of the 75 templates and 25 competencies has >= 1 random question
    covered_tpls = {itm["template_id"] for itm in batch_1}
    covered_comps = {itm["competency_id"] for itm in batch_1}
    assert covered_tpls == all_tpl_ids
    assert covered_comps == all_comp_ids

    # Dispatch judges: must dispatch at most 10 judges, each with at most 20 items
    disp = dispatch_judges(work_dir=work_dir, pointer=True)
    assert len(disp["Subagents"]) == 10
    for item_file_str in disp["item_files"]:
        item_data = json.loads(Path(item_file_str).read_text(encoding="utf-8"))
        assert len(item_data["items"]) <= 20
        assert len(item_data["items"]) == 20

    # Re-run with a different random_seed to verify random seed & ordering selection
    work_dir_2 = tmp_path / "work_2"
    batch_p2, _ = generate_judge_batch(templates_path=templates_dir, work_dir=work_dir_2, random_seed=67890)
    batch_2 = json.loads(batch_p2.read_text(encoding="utf-8"))
    stems_1 = [itm["stem"] for itm in batch_1]
    stems_2 = [itm["stem"] for itm in batch_2]
    assert stems_1 != stems_2


def test_compile_shard_rejects_debug_raise_and_accepts_legitimate_chebyshev(tmp_path: Path):
    """Verifies that:
    1. A generator with an artificial debug 'raise' statement is rejected with [TPL-DEBUG-ARTIFACT].
    2. A legitimate Chebyshev exercise with small bound and conceptual distractors is accepted.
    """
    work_dir, shards_dir, _, cta_file, _ = _create_isolated_workspace(tmp_path, cid="H-05", ctype="concept")
    shard_py = shards_dir / "shard_01_data.py"

    # Part 1: Artifact rejection
    code_with_raise = r'''
import random

def _gen_h05(rng, arch=1):
    mu = rng.randint(20, 60)
    sigma = rng.randint(5, 12)
    varx = sigma**2
    eps = rng.randint(sigma * 2 + 5, 80)
    ans = round(varx / (eps**2), 4)
    d1 = round(sigma / eps, 4)
    d3 = round(sigma / (eps**2), 4)
    v = {"mu": mu, "sigma": sigma, "varx": varx, "eps": eps, "ans": ans, "d1": d1, "d3": d3}
    if arch == 2:
        return {"vars": v, "correct": r"@ans@"}
    dists = [
        ("D-H05-01", r"$P(|X - @mu@| \ge @eps@) \le @d1@$", r"Error de exponente lineal 1/k en lugar de cuadrático para eps=@eps@ y sigma=@sigma@."),
        ("D-H05-02", r"$P(|X - @mu@| \ge @eps@) \ge @ans@$", r"Inversión de la cota de Chebyshev para dispersión eps=@eps@ y sigma=@sigma@."),
        ("D-H05-03", r"$P(|X - @mu@| \ge @eps@) \le @d3@$", r"Uso de desviación típica sigma=@sigma@ en vez de varianza para eps=@eps@."),
        ("D-H05-04", r"$P(|X - @mu@| < @eps@) \le @ans@$", r"Confunde evento de cola con evento central para eps=@eps@ y sigma=@sigma@."),
        ("D-H05-05", r"$X \sim \mathcal{N} \Rightarrow P(|X - @mu@| \ge @eps@) \le @ans@$", r"Asume incorrectamente distribución normal para mu=@mu@ y sigma=@sigma@."),
        ("D-H05-06", r"$P(|X| \ge @eps@) \le @ans@$", r"Omite centrado respecto a la media mu=@mu@ para eps=@eps@."),
    ]
    return {"vars": v, "correct": r"$P(|X - @mu@| \ge @eps@) \le @ans@$", "distractors": dists}

def gen_h05_1(rng): return _gen_h05(rng, 1)
def gen_h05_2(rng): return _gen_h05(rng, 2)
def gen_h05_3(rng):
    res = _gen_h05(rng, 3)
    if res["vars"]["mu"] > 0:
        raise RuntimeError("DEBUG_CRASH")
    return res

def ver_h05(res): return bool(res.get("correct") in (r"$P(|X - @mu@| \ge @eps@) \le @ans@$", r"@ans@") and abs(res["vars"]["ans"] - round(res["vars"]["varx"] / (res["vars"]["eps"]**2), 4)) < 1e-6)

s1 = [
    r"Para una variable aleatoria $X$ con $\mu = @mu@$ y varianza $\sigma^2 = @varx@$, halle la cota:",
    r"Considere una distribución con media $\mu = @mu@$ y varianza $\sigma^2 = @varx@$, determine la cota:",
    r"Aplicando Chebyshev a una variable con centro en $\mu = @mu@$ y $\text{Var}(X) = @varx@$, determine la relación:",
    r"A partir de los parámetros $\mu = @mu@$ y varianza $\sigma^2 = @varx@$, determine la cota de Chebyshev:",
]
s2 = [
    r"Dada una muestra teórica con media $\mu = @mu@$ y dispersión $\sigma^2 = @varx@$, calcule el valor crítico:",
    r"En un proceso con promedio $\mu = @mu@$ y varianza $\sigma^2 = @varx@$, obtenga el resultado de la cota:",
    r"Calcule la cota superior del evento según Chebyshev para $\mu = @mu@$ y $\sigma^2 = @varx@$:",
    r"Estime el límite probabilístico con parámetros $\mu = @mu@$ y $\sigma^2 = @varx@$:",
]
s3 = [
    r"Se tiene una distribución continua con valor esperado $\mu = @mu@$ y $\sigma^2 = @varx@$. Identifique la cota:",
    r"Evalúe la probabilidad de desviación respecto a $\mu = @mu@$ cuando la varianza es $\sigma^2 = @varx@$:",
    r"Utilizando la regla de Chebyshev para $\mu = @mu@$ y varianza poblacional $\sigma^2 = @varx@$, halle la expresión:",
    r"Determine la cota de Chebyshev con base en $\mu = @mu@$ y segundo momento central $\sigma^2 = @varx@$:",
]
hints = [
    "La desigualdad de Chebyshev acota colas bilaterales empleando el segundo momento central.",
    "La cota superior general se evalúa mediante el cociente de la varianza entre el cuadrado de la tolerancia.",
    "Compruebe que la cota decrezca de manera cuadrática con respecto a la amplitud permitida.",
]
TEMPLATES = [
    ("T-H05-01", "H-05", "multiple_choice_7_options", gen_h05_1, ver_h05, ("easy", "Remember"), s1, hints, "Sol @ans@."),
    ("T-H05-02", "H-05", "fill_in_the_blank", gen_h05_2, ver_h05, ("medium", "Understand"), s2, hints, "Sol @ans@."),
    ("T-H05-03", "H-05", "multiple_choice_7_options", gen_h05_3, ver_h05, ("hard", "Apply"), s3, hints, "Sol @ans@."),
]
'''
    shard_py.write_text(code_with_raise, encoding="utf-8")
    ok, errors = compile_shard(work_dir, shard_id="shard_01", strict=True, min_archetypes=3, cta_path=cta_file, seeds=50)
    assert not ok, "Expected compile_shard to reject generator with debug raise"
    err_str = "\n".join(errors)
    assert "[TPL-DEBUG-ARTIFACT]" in err_str

    # Part 2: Clean code without raise passes without false DIAG-MAGIC-MULT
    clean_code = code_with_raise.replace(
        'def gen_h05_3(rng):\n    res = _gen_h05(rng, 3)\n    if res["vars"]["mu"] > 0:\n        raise RuntimeError("DEBUG_CRASH")\n    return res',
        'def gen_h05_3(rng): return _gen_h05(rng, 3)'
    )
    shard_py.write_text(clean_code, encoding="utf-8")
    ok, errors = compile_shard(work_dir, shard_id="shard_01", strict=True, min_archetypes=3, cta_path=cta_file, seeds=50)
    assert ok, f"Expected clean Chebyshev exercise to compile with PASS, got: {errors}"


