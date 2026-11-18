"""Regression and Hypothesis property-based tests for compile_shard.py hardening."""

import ast
import json
import sys
from pathlib import Path

from hypothesis import given, settings, strategies as st

_skill_root = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

from compile_shard import (
    _format_with_fmt,
    build_adapted_mc7_generator,
    compile_shard,
    extract_function_code,
    heal_shard_source_text,
    inject_ast_auto_vars,
    normalize_double_braces,
    prune_ast_dependencies,
    prune_ast_preamble,
)


def _setup_work(tmp_path: Path, extra_distractor: bool = True, inline_manifest_dists: bool = True):
    work = tmp_path / "work"
    (work / "shards").mkdir(parents=True, exist_ok=True)
    (work / "templates").mkdir(parents=True, exist_ok=True)

    dists = [
        {"id": f"D-C01-0{i}", "wrong_belief": f"Concepcion erronea numero {i} en el calculo."}
        for i in range(1, 7)
    ]
    if not extra_distractor:
        dists = dists[:5]

    cta = {
        "competencies": [
            {
                "id": "C-01",
                "title": "Test Concept",
                "type": "concept",
                "distractors": dists,
            }
        ]
    }
    (work / "cta.json").write_text(json.dumps(cta), encoding="utf-8")
    manifest_comp = dict(cta["competencies"][0]) if inline_manifest_dists else {"id": "C-01", "title": "Test Concept", "type": "concept"}
    manifest = {
        "shards": [
            {
                "shard_id": "shard_01",
                "competencies": [manifest_comp],
            }
        ]
    }
    (work / "shards" / "pre_shard_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return work


def _valid_shard_code() -> str:
    return '''
def gen_1(rng):
    a = int(rng.np.integers(10, 40))
    b = rng.randint(10, 40)
    ans = a + b
    return {"vars": {"a": a, "b": b, "ans": ans}, "correct": str(ans), "ds": []}

def ver_1(c, v):
    return int(c) == v["a"] + v["b"]

TEMPLATES = [
    (
        "T-C01-01",
        "C-01",
        "fib",
        gen_1,
        ver_1,
        ("easy", "Remember"),
        [
            "Calcule la suma exacta de @a@ y @b@ en el modelo:",
            "Determine el resultado total al sumar @a@ con @b@:",
            "Halle el valor numerico de @a@ + @b@ directamente:",
            "Obtenga la cantidad resultante al combinar @a@ mas @b@:",
            "Evalue la adicion algebraica entre @a@ y @b@ ahora:",
            "Indique cuanto vale la suma de los terminos @a@ y @b@:",
        ],
        [
            "Observe cuidadosamente ambos operandos positivos del enunciado.",
            "Aplique la adicion aritmetica directa sobre los parametros dados.",
            "Verifique que el entero resultante sea mayor que cada sumando.",
        ],
        "La suma detallada de @a@ y @b@ produce exactamente @ans@ tras operar ambos terminos.",
    ),
]
'''


def test_cert_invalidated_and_templates_not_corrupted_on_subsequent_fail(tmp_path: Path):
    work = _setup_work(tmp_path)
    shard_py = work / "shards" / "shard_01_data.py"
    shard_py.write_text(_valid_shard_code(), encoding="utf-8")

    ok, errs = compile_shard(work, "shard_01", strict=False, seeds=10)
    assert ok, f"Expected initial compile to pass: {errs}"

    cert_path = work / "shards" / "shard_01.cert.json"
    tpl_path = work / "templates" / "C-01.json"
    assert cert_path.is_file()
    assert tpl_path.is_file()
    cert_data = json.loads(cert_path.read_text(encoding="utf-8"))
    assert cert_data["passed_50_seeds"] is False  # seeds=10 and strict=False
    original_tpl_text = tpl_path.read_text(encoding="utf-8")

    # Now break the shard so Step 7 / M3 fails
    broken = _valid_shard_code().replace('("easy", "Remember")', '("invalid_diff", "Remember")')
    shard_py.write_text(broken, encoding="utf-8")
    ok2, errs2 = compile_shard(work, "shard_01", strict=False, seeds=10)
    assert not ok2
    assert not cert_path.exists(), "Stale .cert.json must be removed on failed compile!"
    assert tpl_path.read_text(encoding="utf-8") == original_tpl_text, "Failed compile must not overwrite good template JSON!"


def test_cta_change_invalidates_no_change_cache(tmp_path: Path):
    work = _setup_work(tmp_path, extra_distractor=False, inline_manifest_dists=False)
    shard_py = work / "shards" / "shard_01_data.py"
    _rats_list = [
        "Error de signo al restar @b@ de @a@ en lugar de sumar ambos terminos positivos.",
        "Omision completa de la unidad decenas de @a@ durante la agregacion con @b@.",
        "Duplicacion incorrecta del coeficiente @a@ antes de combinarlo con el termino @b@.",
        "Intercambio de orden posicional entre @b@ y @a@ generando un desfase decimal.",
        "Sustitucion de la adicion entre @a@ y @b@ por un producto parcial truncado.",
        "Calculo del promedio simple de @a@ y @b@ en vez de acumular la suma total.",
    ]
    mc7_code = f'''
def gen_mc(rng):
    a = rng.randint(10, 30)
    b = rng.randint(10, 30)
    ans = a + b
    _r = {_rats_list!r}
    ds = [(f"D-C01-0{{i}}", str(ans + i * 3 + 1), _r[i - 1]) for i in range(1, 7)]
    return {{"vars": {{"a": a, "b": b, "ans": ans}}, "correct": str(ans), "ds": ds}}

def ver_mc(c, v):
    return int(c) == v["a"] + v["b"]

TEMPLATES = [
    (
        "T-C01-01",
        "C-01",
        "mc7",
        gen_mc,
        ver_mc,
        ("easy", "Remember"),
        [
            "Calcule la suma exacta de @a@ y @b@ en el modelo:",
            "Determine el resultado total al sumar @a@ con @b@:",
            "Halle el valor numerico de @a@ + @b@ directamente:",
            "Obtenga la cantidad resultante al combinar @a@ mas @b@:",
            "Evalue la adicion algebraica entre @a@ y @b@ ahora:",
            "Indique cuanto vale la suma de los terminos @a@ y @b@:",
        ],
        [
            "Observe cuidadosamente ambos operandos positivos del enunciado.",
            "Aplique la adicion aritmetica directa sobre los parametros dados.",
            "Verifique que el entero resultante sea mayor que cada sumando.",
        ],
        "La suma detallada de @a@ y @b@ produce exactamente @ans@ tras operar ambos terminos.",
    ),
]
'''
    shard_py.write_text(mc7_code, encoding="utf-8")
    ok1, errs1 = compile_shard(work, "shard_01", strict=True, seeds=10, min_archetypes=1)
    assert not ok1
    assert any("D-C01-06" in e for e in errs1)

    # Fix cta.json without modifying shard_01_data.py
    work_fixed = _setup_work(tmp_path / "fixed_cta_tmp", extra_distractor=True)
    (work / "cta.json").write_text((work_fixed / "cta.json").read_text(encoding="utf-8"), encoding="utf-8")

    ok2, errs2 = compile_shard(work, "shard_01", strict=True, seeds=10, min_archetypes=1)
    assert ok2, f"Expected recompile after cta.json fix, got: {errs2}"
    assert not any("NO-CHANGE" in e for e in errs2)


def test_sample_dict_no_unbound_local_when_gen_fails_seed_42(tmp_path: Path):
    work = _setup_work(tmp_path)
    shard_py = work / "shards" / "shard_01_data.py"
    code = '''
def gen_boom(rng):
    x = rng.randint(1, 5)
    raise ValueError("intentional seed 42 failure")

def ver_ok(c, v):
    return int(c) > 0

TEMPLATES = [
    (
        "T-C01-01",
        "C-01",
        "fib",
        gen_boom,
        ver_ok,
        ("easy", "Remember"),
        [
            "Calcule el valor exacto de @x@ en el sistema:",
            "Determine cuanto vale @x@ en el modelo actual:",
            "Halle el numero @x@ correspondiente al ejercicio:",
        ],
        [
            "Observe el valor del parametro inicial en el problema.",
            "Identifique la regla de calculo aplicada al parametro.",
            "Confirme que el resultado entero sea estrictamente positivo.",
        ],
        "El resultado obtenido al evaluar el parametro @x@ es exactamente @ans@.",
    ),
]
'''
    shard_py.write_text(code, encoding="utf-8")
    # Must return (False, errors) cleanly, NEVER crash with UnboundLocalError
    ok, errs = compile_shard(work, "shard_01", strict=True, seeds=5, min_archetypes=1)
    assert not ok
    assert len(errs) >= 1


def test_rng_np_available_across_all_compile_shard_sweeps(tmp_path: Path):
    work = _setup_work(tmp_path)
    shard_py = work / "shards" / "shard_01_data.py"
    shard_py.write_text(_valid_shard_code(), encoding="utf-8")
    ok, errs = compile_shard(work, "shard_01", strict=True, seeds=10, min_archetypes=1)
    assert ok, f"Expected rng.np generator to pass all sweeps, got: {errs}"


def test_inject_ast_auto_vars_conditional_returns_no_unbound_local():
    src = """
def generate_params(rng):
    a = rng.randint(1, 5)
    if a == 1:
        return {"correct": str(a)}
    b = a * 2
    return {"correct": str(b)}
"""
    transformed = inject_ast_auto_vars(src)
    ns = {}
    exec(compile(transformed, "<test>", "exec"), ns)
    fn = ns["generate_params"]

    class _FakeRng:
        def __init__(self, v):
            self._v = v
        def randint(self, lo, hi):
            return self._v

    r1 = fn(_FakeRng(1))
    assert r1["vars"] == {"a": 1, "ans": "1"}
    r2 = fn(_FakeRng(3))
    assert r2["vars"] == {"a": 3, "b": 6, "ans": "6"}


def test_prune_ast_transitive_constants_and_decorated_extract():
    src = """
B = 10
A = B + 5

@staticmethod
def gen_c01(rng):
    # def gen_c01( trick comment
    return {"vars": {"v": A}, "correct": str(A)}
"""
    pruned = prune_ast_dependencies(src, "gen_c01")
    assert "B = 10" in pruned
    assert "A = B + 5" in pruned
    preamble = prune_ast_preamble(src, "gen_c01")
    assert "B = 10" in preamble
    assert "def gen_c01" not in preamble

    extracted = extract_function_code(
        """@staticmethod
def gen_c01(rng):
    return {"vars": {"v": 1}, "correct": "1"}""",
        "generate_params",
    )
    assert "def generate_params(" in extracted
    assert "generate = generate_params" in extracted


def test_mc7_suffix_fmt_and_non_strict_two_tuple():
    base = "def generate_params(rng):\n    return {'vars': {'x': 5}, 'correct': '5', 'ds': [('D-C01-01', '10')]}\n"
    wrapped = build_adapted_mc7_generator(base, "C-01", [{"id": "D-C01-01"}], strict=False, fmt="@X@%")
    ns = {}
    exec(compile(wrapped, "<mc7>", "exec"), ns)
    res = ns["generate_params"](None)
    assert res["correct"] == "5%"
    assert len(res["distractors"]) == 1
    assert res["distractors"][0]["value"] == "10%"


@given(
    var_name=st.sampled_from(["i", "u", "eq", "abla", "atural", "x"]),
    val=st.integers(min_value=-100, max_value=100),
    s=st.text(alphabet=st.characters(blacklist_categories=("Cs", "Cc"), blacklist_characters="\"'\\"), max_size=30),
)
@settings(max_examples=40)
def test_hypothesis_heal_shard_source_preserves_valid_python(var_name: str, val: int, s: str):
    src = f"{var_name} = {val}\nMSG = '{s}'\n"
    _, healed = heal_shard_source_text(src)
    ast.parse(healed)


@given(
    text=st.text(max_size=40),
    vars_set=st.sets(st.sampled_from(["a", "b", "ans", "x"]), max_size=3),
)
@settings(max_examples=60)
def test_hypothesis_normalize_double_braces_idempotent(text: str, vars_set):
    once = normalize_double_braces(text, vars_set)
    twice = normalize_double_braces(once, vars_set)
    assert once == twice


@given(
    val=st.text(min_size=1, max_size=12, alphabet=st.characters(whitelist_categories=("Nd", "Ll", "Lu"))),
    fmt=st.sampled_from(["$@X@$", "@X@%", "R = @X@", "@X@ kg", "$@X@ u$"]),
)
@settings(max_examples=50)
def test_hypothesis_format_with_fmt_idempotent(val: str, fmt: str):
    once = _format_with_fmt(val, fmt)
    twice = _format_with_fmt(once, fmt)
    assert once == twice
