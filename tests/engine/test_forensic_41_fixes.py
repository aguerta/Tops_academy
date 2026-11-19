"""Regression test suite verifying the 41 forensic bug fixes across Lots 1-4 (Milestone 20)."""
from __future__ import annotations

import ast
import json
import random
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def test_l1_01_02_04_05_06_compile_shard_helpers():
    import compile_shard as cs

    # L1-02 & L1-04 & L1-05: passthrough helper inlining, ast.Set literal, ternary IfExp folding, D_C01_1 regex
    code = """
def _h_base(rng, mode):
    s = {1, 2}
    val = rng.randint(10, 20) if mode == 1 else rng.randint(30, 40)
    return {"vars": {"x": val}, "ans": f"{val}", "ds": [("D_C01_1", f"{val+1}")]}

def _h_wrap(rng):
    return _h_base(rng, 1)

def gen_1(rng):
    return _h_wrap(rng)

def gen_2(rng):
    s = {1, 2}
    val = rng.randint(10, 20)
    return {"vars": {"x": val}, "ans": f"{val}", "ds": [("D-C01-02", f"{val+1}")]}
"""
    tree = ast.parse(code)
    fn_map = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    spec1 = cs._specialize_gen_ast(fn_map["gen_1"], fn_map)
    spec2 = cs._specialize_gen_ast(fn_map["gen_2"], fn_map)
    dump1 = ast.dump(cs._CanonicalGenASTNormalizer(spec1).normalize(spec1))
    dump2 = ast.dump(cs._CanonicalGenASTNormalizer(spec2).normalize(spec2))
    assert dump1 == dump2

    # L1-06: _extract_pure_sympy_expr supports single-var f-string and @var@
    code_sym = """
def gen_a(rng):
    a = rng.randint(2, 9)
    b = rng.randint(2, 9)
    P = a + b
    return {"vars": {"a": a, "b": b, "P": P}, "ans": f"{P}"}

def gen_b(rng):
    x = rng.randint(2, 9)
    y = rng.randint(2, 9)
    Q = y + x
    return {"vars": {"x": x, "y": y, "Q": Q}, "correct": "@Q@"}
"""
    tree_sym = ast.parse(code_sym)
    fn_sym = {n.name: n for n in tree_sym.body if isinstance(n, ast.FunctionDef)}
    e1 = cs._extract_pure_sympy_expr(fn_sym["gen_a"])
    e2 = cs._extract_pure_sympy_expr(fn_sym["gen_b"])
    assert e1 is not None and e2 is not None
    import sympy
    assert sympy.simplify(cs._canon_syms(e1) - cs._canon_syms(e2)) == 0


def test_l1_03_09_instantiate_quota_and_tpl_id_fallback():
    from engine.instantiate import allocate_template_quotas

    # L1-09: template_id fallback when "id" is absent
    tpls = [
        {"template_id": "T-01", "difficulty": "easy"},
        {"template_id": "T-02", "difficulty": "medium"},
        {"template_id": "T-03", "difficulty": "hard"},
    ]
    q_map = allocate_template_quotas(tpls, 15)
    assert set(q_map.keys()) == {"T-01", "T-02", "T-03"}
    assert sum(q_map.values()) == 15


def test_l2_c01_c02_cta_merge_skill_mc7_and_contract_version(tmp_path: Path):
    import compile_cta
    import cta_merge

    parts_dir = tmp_path / "cta_parts"
    parts_dir.mkdir()
    manifest = {
        "course_id": "test_c",
        "title": "Curso de Prueba Cálculo",
        "files": [{"doc": "doc.pdf", "doc_slug": "doc", "file_index": 0, "pages": 10}],
        "subparts": [{"subpart_id": "part_01", "subpart_index": 0, "file_index": 0, "doc": "doc.pdf"}],
    }
    manifest_p = tmp_path / "pre_cta_manifest.json"
    manifest_p.write_text(json.dumps(manifest), encoding="utf-8")

    part_py = parts_dir / "part_01_data.py"
    part_py.write_text(
        """
CTA_CONTRACT_VERSION = 2
COURSE_ID = "test_c"
TITLE = "Curso de Prueba Cálculo"
COMPETENCIES = [
    {
        "id": "C-01",
        "name": "Derivadas parciales en funciones multivariables",
        "type": "concept",
        "description_latex": "Cálculo e interpretación geométrica de derivadas parciales de primer orden en campos escalares diferenciables.",
        "evidence": [("doc.pdf", 1, "Derivadas parciales")],
        "recommended_modalities": ["mc7", "open_symbolic", "proof_dag"],
        "assumptions": [("A-C01-01", "La función f(x,y) es diferenciable en un entorno abierto.", "Las derivadas direccionales no se obtienen con el gradiente.")],
        "distractors": [
            (
                f"Error conceptual {i} en derivación parcial de orden uno",
                f"El estudiante cree erróneamente el modelo {i} sobre variables independientes libres",
                f"La derivada parcial respecto a x mantiene constante la variable y en el modelo {i}",
                f"Expresión algebraica resultante {i}x + y^2 sin mantener constante y",
                f"Identifica qué variable permanece fija durante la derivación parcial en el caso {i} antes de derivar.",
                f"Omite fijar la variable secundaria como constante en el paso {i}",
            )
            for i in range(1, 7)
        ],
    },
    {
        "id": "Hab-01",
        "name": "Derivadas parciales en funciones multivariables",
        "type": "skill",
        "description_latex": "Aplicación operativa de derivadas parciales de primer orden en problemas de optimización y aproximación lineal.",
        "evidence": [("doc.pdf", 2, "Aplicaciones de derivadas")],
        "recommended_modalities": ["open_symbolic", "proof_dag"],
        "assumptions": [("A-Hab01-01", "La función f(x,y) posee derivadas parciales continuas.", "El teorema de Clairaut no aplica si las cruzadas no son continuas.")],
        "distractors": [
            (
                f"Error operativo {i} al aplicar regla de la cadena multivariable",
                f"El estudiante aplica mal la regla {i} en funciones compuestas de dos variables",
                f"La derivada compuesta requiere sumar los productos de cada parcial por su derivada interna {i}",
                f"Resultado truncado sin multiplicar por el factor interno {i}z",
                f"Aplica la regla de la cadena multiplicando cada término por la derivada interna correspondiente {i}.",
                f"Omite multiplicar por la derivada interna del argumento en el paso {i}",
            )
            for i in range(1, 7)
        ],
    },
]
""",
        encoding="utf-8",
    )
    ok, _, errs, _ = compile_cta.compile_cta(part_py, parts_dir, manifest_p, output_json_name="part_01.json", is_part=True)
    assert ok, errs
    cta_merge.merge_cta_parts(tmp_path)
    draft_json = json.loads((tmp_path / "cta_draft.json").read_text(encoding="utf-8"))
    assert draft_json.get("contract_version") == 2
    harmonize_payload = {
        "merge": [
            {
                "survivor_id": "C-01",
                "absorbed_ids": ["Hab-01"],
                "type": "skill",
            }
        ]
    }
    (tmp_path / "cta_harmonize.json").write_text(json.dumps(harmonize_payload), encoding="utf-8")
    cta_merge.apply_harmonize(tmp_path)
    cta_json = json.loads((tmp_path / "cta.json").read_text(encoding="utf-8"))
    assert cta_json.get("contract_version") == 2
    comp = cta_json["competencies"][0]
    assert comp["type"] == "skill"
    assert "multiple_choice_7_options" not in comp["recommended_modalities"]


def test_l2_c03_compile_cta_fail_total_modality_invalid(tmp_path: Path):
    import compile_cta

    manifest = {
        "course_id": "c",
        "title": "Course",
        "files": [{"doc": "doc.pdf", "doc_slug": "doc", "file_index": 0, "pages": 10}],
    }
    manifest_p = tmp_path / "pre_cta_manifest.json"
    manifest_p.write_text(json.dumps(manifest), encoding="utf-8")

    cta_py = tmp_path / "cta_data.py"
    cta_py.write_text(
        """
CTA_CONTRACT_VERSION = 2
COURSE_ID = "c"
TITLE = "Course"
COMPETENCIES = [
    {
        "id": "C-01",
        "name": "Concept 1",
        "type": "concept",
        "description_latex": "Desc",
        "evidence": [("doc.pdf", 1, "Sec")],
        "recommended_modalities": ["open_symbolic", "invented_modality_xyz"],
        "assumptions": [("A-C01-01", "Stmt", "Viol")],
        "distractors": [
            (f"D-C01-0{i}", f"Name {i}", f"Wrong belief {i} distinct", f"Omit {i}", f"Manif {i}", f"Hint {i}", f"Warn {i}")
            for i in range(1, 7)
        ],
    }
]
""",
        encoding="utf-8",
    )
    ok, _, errs, _ = compile_cta.compile_cta(cta_py, tmp_path, manifest_p)
    assert not ok
    assert any("CTA-MODALITY-INVALID" in e for e in errs), errs


def test_l2_c04_check_templates_canonical_signature_order_invariant():
    import check_templates as ct

    q1 = {
        "interaction_type": "proof_dag",
        "correct_answer": {"canonical_order": ["S1", "S2"]},
        "proof_dag": {"steps": [{"id": "S1", "content": "A"}, {"id": "S2", "content": "B"}]},
    }
    q2 = {
        "interaction_type": "proof_dag",
        "correct_answer": {"canonical_order": ["S1", "S2"]},
        "proof_dag": {"steps": [{"id": "S2", "content": "B"}, {"id": "S1", "content": "A"}]},
    }
    assert ct._canonical_answer_signature(q1, "proof_dag") == ct._canonical_answer_signature(q2, "proof_dag")


def test_l2_c05_m01_m05_adversarial_and_proof_negative_numbers():
    from engine.adversarial_generator import compile_and_verify_adversarial
    from engine.proof_compiler import compile_and_verify_proof_dag

    # Negative number in adversarial_break counterexample predicate + @var@ in sample_witness
    raw_adv = {
        "mode": "counterexample",
        "prompt": "Refuta para a=@a@",
        "claim": "x^2 > @a@",
        "inputs": [{"name": "x", "min": "@min_x@", "max": 5, "step": 1}],
        "predicates": [{"id": "P1", "expr": "x**2 <= @a@**2", "label": "Cond"}],
        "sample_witness": {"x": "@w_x@"},
    }
    compiled_adv, ans_adv = compile_and_verify_adversarial(
        raw_adv,
        {"a": -3, "min_x": -5, "w_x": -2},
        {},
        random.Random(42),
    )
    assert compiled_adv["prompt"] == "Refuta para a=-3"
    assert ans_adv["sample_witness"]["x"] == -2.0

    # Negative number in proof_dag sympy_expr / expected_sympy_expr (3+ valid steps, >=1 edge)
    raw_dag = {
        "steps": [
            {"id": "S1", "content": "Paso 1: $@a@$", "sympy_expr": "@a@**2", "expected_sympy_expr": "9"},
            {"id": "S2", "content": "Paso 2: $@b@$"},
            {"id": "S3", "content": "Paso 3: cierre $@b@$"},
        ],
        "edges": [["S1", "S2"], ["S2", "S3"]],
    }
    compiled_dag, _ = compile_and_verify_proof_dag(raw_dag, {"a": -3, "b": 9}, {}, random.Random(42))
    assert len(compiled_dag["steps"]) == 3

    # Non-equivalent sympy_expr must raise [PROOF-DAG-SYMPY]
    bad_sympy_dag = {
        "steps": [
            {"id": "S1", "content": "Paso 1: $@a@$", "sympy_expr": "@a@**2", "expected_sympy_expr": "-9"},
            {"id": "S2", "content": "Paso 2: $@b@$"},
            {"id": "S3", "content": "Paso 3: cierre $@b@$"},
        ],
        "edges": [["S1", "S2"], ["S2", "S3"]],
    }
    with pytest.raises(ValueError, match="PROOF-DAG-SYMPY"):
        compile_and_verify_proof_dag(bad_sympy_dag, {"a": -3, "b": 9}, {}, random.Random(42))

    # Empty edges or < 3 valid steps in proof_dag must be rejected
    with pytest.raises(ValueError, match="PROOF-DAG-EDGES"):
        compile_and_verify_proof_dag({**raw_dag, "edges": []}, {"a": -3, "b": 9}, {}, random.Random(42))
    with pytest.raises(ValueError, match="PROOF-DAG-SIZE"):
        compile_and_verify_proof_dag(
            {"steps": raw_dag["steps"][:2], "edges": [["S1", "S2"]]},
            {"a": -3, "b": 9},
            {},
            random.Random(42),
        )

    # find_fallacy with < 3 steps must be rejected
    with pytest.raises(ValueError, match="ADV-STEPS"):
        compile_and_verify_adversarial(
            {
                "mode": "find_fallacy",
                "steps": [
                    {"id": "A1", "content": "Paso 1"},
                    {"id": "A2", "content": "Paso 2", "is_fallacy": True, "error_rationale": "Fallo algebraico claro."},
                ],
            },
            {},
            {},
            random.Random(42),
        )

    # counterexample witness_scope must NOT leak uninterpolated vars_dict scalars (browser parity)
    with pytest.raises(ValueError, match="ADV-WITNESS-EVAL"):
        compile_and_verify_adversarial(
            {
                "mode": "counterexample",
                "inputs": [{"id": "x", "label": "x", "min": -5, "max": 5}],
                "predicates": [{"id": "P1", "expr": "x <= a", "failure_rationale": "Falta interpolar."}],
                "sample_witness": {"x": -2},
            },
            {"a": 3},
            {},
            random.Random(42),
        )


def test_l3_01_02_06_assemble_and_invariants():
    from engine.assemble import _assemble_invariant_canvas, _assemble_unstructured_model
    from engine.invariants import validate_katex_syntax

    # L3-01: invariant_canvas target_value & point_coords x/y normalization
    ic, ic_ans = _assemble_invariant_canvas(
        {
            "mode": "cartesian",
            "interactive_points": [{"id": "P1", "initial_x": 0, "initial_y": 0}],
            "sliders": [{"id": "s1", "min": 0, "max": 10, "initial": 1}],
            "invariants": [
                {"kind": "point_coords", "target": "P1", "x": "@px@", "y": "@py@", "error_rationale": "Ajusta P1."},
                {"kind": "slider_eq", "slider_id": "s1", "target_value": "@sv@", "error_rationale": "Ajusta s1."},
            ],
        },
        {"px": 3, "py": 4, "sv": 5},
        {},
        {},
    )
    assert ic["invariants"][0]["target_x"] == 3
    assert ic["invariants"][0]["target_y"] == 4
    assert ic["invariants"][1]["target"] == 5

    # L3-02: validate_katex_syntax exempts correct_answer from Rule 15 exposed command check
    assert validate_katex_syntax(r"\frac{a}{b}", "correct_answer") == []

    # L3-06: unstructured_model rejects undeclared correct_role
    with pytest.raises(ValueError, match="correct_role"):
        _assemble_unstructured_model(
            {
                "phase1_variables": {
                    "roles": ["Endógena", "Exógena"],
                    "items": [
                        {"id": "V1", "label": "Precio", "correct_role": "Endógena"},
                        {"id": "V2", "label": "Clima", "correct_role": "RolInexistente"},
                    ],
                },
                "phase2_assumptions": {
                    "options": [
                        {"id": "A1", "content": "Linealidad", "is_required": True},
                        {"id": "A2", "content": "Falso", "is_required": False},
                    ]
                },
                "phase3_formulation": {"input_mode": "symbolic", "correct_expression": "x + y"},
            },
            {},
            {},
            random.Random(1),
            {},
        )


def test_l4_01_03_judge_m20_arbitration():
    import judge

    # 1. proof_dag alternative valid topological order
    gt_dag = {
        "correct_answer": {
            "canonical_order": ["S1", "S2", "S3"],
            "required_step_ids": ["S1", "S2", "S3"],
            "edges": [["S1", "S3"], ["S2", "S3"]],
        }
    }
    ok_dag, msg_dag = judge._check_m20_answer_match(
        {"canonical_order": ["S2", "S1", "S3"], "required_step_ids": ["S1", "S2", "S3"]},
        gt_dag,
        "proof_dag",
    )
    assert ok_dag, msg_dag

    # 2. adversarial_break counterexample via REAL compile_and_verify_adversarial + judge sanitization
    from engine.adversarial_generator import compile_and_verify_adversarial

    compiled_adv, ca_adv = compile_and_verify_adversarial(
        {
            "mode": "counterexample",
            "prompt": "Refuta con entero negativo:",
            "inputs": [{"id": "x", "label": "x", "type": "integer", "min": -10, "max": 10}],
            "predicates": [
                {
                    "id": "P1",
                    "expr": "x < 0",
                    "distractor_id": "D-ADV-01",
                    "failure_rationale": "Debe ser estrictamente negativo.",
                }
            ],
            "trap_predicates": [
                {
                    "expr": "x <= -6",
                    "distractor_id": "D-ADV-02",
                    "error_rationale": "Cayó en el extremo prohibido <= -6.",
                }
            ],
            "sample_witness": {"x": -2},
        },
        {},
        {},
        random.Random(42),
    )
    ji_adv: Dict[str, Any] = {}
    gt_adv: Dict[str, Any] = {}
    judge._sanitize_m20_judge_item(
        "adversarial_break",
        {"adversarial_break": compiled_adv, "correct_answer": ca_adv},
        ji_adv,
        gt_adv,
    )
    # Blind judge payload must NOT leak failure_rationale or distractor_id
    for b_pred in ji_adv["adversarial_break"]["predicates"]:
        assert set(b_pred.keys()) <= {"id", "expr", "description"}
        assert "failure_rationale" not in b_pred
        assert "distractor_id" not in b_pred

    ok_adv, msg_adv = judge._check_m20_answer_match({"sample_witness": {"x": -4}}, gt_adv, "adversarial_break")
    assert ok_adv, msg_adv
    assert not judge._check_m20_answer_match({"sample_witness": {"x": 2}}, gt_adv, "adversarial_break")[0]
    assert not judge._check_m20_answer_match({"sample_witness": {"x": -7}}, gt_adv, "adversarial_break")[0]
    assert not judge._check_m20_answer_match({"sample_witness": {"x": -3.5}}, gt_adv, "adversarial_break")[0]

    # 3. invariant_canvas cartesian flat vs nested target_state + invariants fallthrough + kink_at without target_y
    gt_ic_flat = {
        "correct_answer": {"mode": "cartesian", "target_state": {"pt_kink": {"x": 5, "y": 10}}},
        "invariants": [
            {"id": "INV_POS", "kind": "point_coords", "point_id": "pt_kink", "target_x": 5, "target_y": 10},
            {"id": "INV_KINK", "kind": "kink_at", "curve_id": "budget", "x": 5, "target": 0.5},
        ],
    }
    ok_ic_norm, msg_ic_norm = judge._check_m20_answer_match(
        {"points": {"pt_kink": {"x": 5, "y": 10}}},
        gt_ic_flat,
        "invariant_canvas",
    )
    assert ok_ic_norm, msg_ic_norm

    gt_ic_fallthrough = {
        "correct_answer": {
            "mode": "cartesian",
            "target_state": {"points": {"pt_kink": {"x": 5, "y": 10}}, "extra_field": "ignore_if_invs_hold"},
        },
        "invariants": [
            {"id": "INV_POS", "kind": "point_coords", "point_id": "pt_kink", "target_x": 5, "target_y": 10},
            {"id": "INV_KINK", "kind": "kink_at", "point_id": "pt_kink", "x": 5},
        ],
    }
    ok_ic_ft, msg_ic_ft = judge._check_m20_answer_match(
        {"points": {"pt_kink": {"x": 5.01, "y": 10.0}}},
        gt_ic_fallthrough,
        "invariant_canvas",
    )
    assert ok_ic_ft, msg_ic_ft
    assert not judge._check_m20_answer_match(
        {"points": {"pt_kink": {"x": 2, "y": 10}}},
        gt_ic_fallthrough,
        "invariant_canvas",
    )[0]

    # 4. invariant_canvas tree edge ID vs [from, to] pair
    gt_tree = {
        "correct_answer": {"mode": "tree", "required_edges": [["N1", "N2"]], "required_info_sets": [["N2", "N3"]]},
        "edges": [{"id": "E1", "from": "N1", "to": "N2"}],
    }
    ok_tree, msg_tree = judge._check_m20_answer_match(
        {"mode": "tree", "required_edges": ["E1"], "required_info_sets": [["N3", "N2"]]},
        gt_tree,
        "invariant_canvas",
    )
    assert ok_tree, msg_tree


def test_fib_single_digit_homogeneous_stem_no_false_leak():
    from engine.invariants import check_instance_invariants

    q_fib_zero = {
        "stem": "Calcule el discriminante de $u_{xx} + 2u_{xy} + u_{yy} = 0$.",
        "correct_answer": {
            "value": "0",
            "canonical_algebraic": "0",
            "accepted_equivalents": ["0", "0.0"],
            "tolerance": 0.0001,
        },
        "hints": ["A=1, B=2, C=1.", "Evalúa B^2 - 4AC.", "Simplifica."],
        "solution": "Delta = 2^2 - 4(1)(1) = 0.",
    }
    ok_zero, errs_zero = check_instance_invariants(q_fib_zero, "fill_in_the_blank")
    assert ok_zero, f"Unexpected leak error for homogeneous stem '= 0': {errs_zero}"

    q_open_leak = {
        "stem": "Determine la función sabiendo que $f(x) = 2*x + 1$.",
        "correct_answer": {
            "expression": "2*x + 1",
            "canonical_algebraic": "2*x + 1",
            "variables": ["x"],
        },
        "hints": ["Observa f(x).", "Simplifica.", "Escribe."],
        "solution": "f(x) = 2*x + 1.",
    }
    ok_leak, errs_leak = check_instance_invariants(q_open_leak, "open_symbolic")
    assert not ok_leak
    assert any("leaked as direct assignment" in e for e in errs_leak), errs_leak
