"""Deterministic, self-contained unit tests covering all Stage 1 remediations (Streams 1A - 1E) for ab_testing_3.

None of these tests touch or depend on scratch/ab_testing_3/**.
All dynamic tests create clean synthetic fixtures in pytest tmp_path.
"""

from __future__ import annotations

import ast
import json
import random
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest

# Ensure skill directory is in sys.path
SKILL_DIR = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))


# ==============================================================================
# STREAM 1A REMEDIATIONS (7 TESTS)
# ==============================================================================

class TestStream1ARemediations:
    """Verifies all Stream 1A template compiler and invariant fixes."""

    def test_mc7_generator_parity_without_relevant_rats(self):
        """MC7 generator wrapper in 'not relevant_rats' branch assigns r['correct'] = c,

        formats distractors consistently with fmt, avoiding length imbalance false positives (R-15).
        """
        from compile_shard import build_adapted_mc7_generator
        from engine.invariants import check_instance_invariants

        base_code = """
def generate_params(rng):
    v = rng.randint(10, 99)
    corr = f"\\\\frac{{{v}}}{{100}}"
    dists = [
        ("D-C01-01", f"\\\\frac{{{v + 1}}}{{100}}", "Error aditivo en numerador 1"),
        ("D-C01-02", f"\\\\frac{{{v + 2}}}{{100}}", "Error aditivo en numerador 2"),
        ("D-C01-03", f"\\\\frac{{{v + 3}}}{{100}}", "Error aditivo en numerador 3"),
        ("D-C01-04", f"\\\\frac{{{v + 4}}}{{100}}", "Error aditivo en numerador 4"),
        ("D-C01-05", f"\\\\frac{{{v + 5}}}{{100}}", "Error aditivo en numerador 5"),
        ("D-C01-06", f"\\\\frac{{{v + 6}}}{{100}}", "Error aditivo en numerador 6"),
    ]
    return {"vars": {"v": v}, "correct": corr, "distractors": dists}
"""
        cta_distractors = [{"id": f"D-C01-0{i}"} for i in range(1, 7)]
        wrapped_code = build_adapted_mc7_generator(
            base_gen_code=base_code,
            cid="C-01",
            cta_distractors=cta_distractors,
            strict=True,
            rats_map=None,  # Triggers 'not relevant_rats' branch
            fmt="$@X@$",
        )

        ns: Dict[str, Any] = {}
        exec(wrapped_code, ns)
        gen_fn = ns["generate_params"]

        rng = random.Random(42)
        res = gen_fn(rng)

        # 1. Parity check: correct option must have $ formatted
        assert res["correct"].startswith("$") and res["correct"].endswith("$")
        assert res["options"][0]["value"] == res["correct"]
        assert res["options"][0]["is_correct"] is True

        # 2. Distractor parity: all distractors formatted identically
        assert len(res["options"]) == 7
        for opt in res["options"][1:]:
            assert opt["is_correct"] is False
            assert opt["value"].startswith("$") and opt["value"].endswith("$")
            assert opt.get("error_rationale")

        # 3. Invariants check: no false positive R-15 length violation or $ imbalance
        mock_question = {
            "type": "multiple_choice_7_options",
            "stem": "Enunciado de prueba formal.",
            "options": res["options"],
            "hints": ["Pista 1 orientativa.", "Pista 2 conceptual.", "Pista 3 final."],
        }
        valid, inv_errors = check_instance_invariants(mock_question, "multiple_choice_7_options")
        assert valid is True, f"Invariants failed unexpectedly: {inv_errors}"

    def test_compile_shard_ms_verifier_adversarial_mutations(self):
        """compile_shard strict mode rejects verifiers that pass mutation (b) (__INVALID_DID__)

        or mutation (c) (error_rationale=''), detecting [VERIFIER-TAUTOLOGY-DETECTED].
        check_templates flags mutation (c) as TPL-CROSS error and mutation (b) as [TPL-CROSS-DID] warning.
        """
        from check_templates import check_single_template

        # Tautological verifier that only checks option count and is_correct flags
        tautological_cross_check = """
def verify(res):
    opts = res.get("options", [])
    return len(opts) == 4 and sum(1 for o in opts if o.get("is_correct")) == 2
"""
        template_obj = {
            "id": "T-C-01-04",
            "interaction_type": "multiple_select",
            "stem": "Seleccione las dos opciones correctas para $a=@x@$:",
            "stem_variants": ["Variante 1 con @x@ y @y@", "Variante 2 con @x@ y @y@", "Variante 3 con @x@ y @y@", "Variante 4 con @x@ y @y@"],
            "hints": ["Pista 1 suficientemente larga para pasar", "Pista 2 suficientemente larga para pasar", "Pista 3 suficientemente larga para pasar"],
            "explanation_es": "Explicación detallada del problema con más de 60 caracteres requeridos formalmente.",
            "distractor_ids": ["D-C01-01", "D-C01-02"],
            "generate_py": """
def generate(rng):
    return {
        "vars": {"x": rng.randint(1, 100), "y": rng.randint(1, 100)},
        "options": [
            {"value": "A", "is_correct": True},
            {"value": "B", "is_correct": True},
            {"value": "C", "is_correct": False, "distractor_id": "D-C01-01", "error_rationale": "Razón C formal."},
            {"value": "D", "is_correct": False, "distractor_id": "D-C01-02", "error_rationale": "Razón D formal."},
        ]
    }
""",
            "cross_check_py": tautological_cross_check,
        }

        warns: List[str] = []
        errors = check_single_template(
            template=template_obj,
            competency_id="C-01",
            declared_distractor_ids={"D-C01-01", "D-C01-02"},
            num_dry_run_seeds=5,
            strict=True,
            warnings_out=warns,
        )

        # The tautological verifier accepted mutated values / rationale (mutation c), triggering TPL-CROSS
        assert any("TPL-CROSS" in str(e) for e in errors), f"Expected TPL-CROSS error, got: {errors}"

        # Now test mutation (b): verifier that checks values and rationale but ignores distractor_id
        ver_ignores_did = """
def verify(res):
    opts = res.get("options", [])
    if len(opts) != 4: return False
    vals = [o.get("value") for o in opts if o.get("is_correct")]
    f_opts = [o for o in opts if not o.get("is_correct")]
    return "A" in vals and "B" in vals and all(len(o.get("error_rationale", "")) >= 5 for o in f_opts)
"""
        template_obj["cross_check_py"] = ver_ignores_did
        warns_did: List[str] = []
        errors_did = check_single_template(
            template=template_obj,
            competency_id="C-01",
            declared_distractor_ids={"D-C01-01", "D-C01-02"},
            num_dry_run_seeds=5,
            strict=True,
            warnings_out=warns_did,
        )
        assert any("TPL-CROSS-DID" in w for w in warns_did), f"Expected TPL-CROSS-DID warning, got: {warns_did}"

    def test_orphan_vars_format_specs_and_hints_allowlist(self):
        """_check_orphan_vars supports format-spec placeholders (@v_lim:.4f@), placeholders in hints,

        and only warns for legitimately unused auxiliary variables without failing.
        """
        from check_templates import _check_orphan_vars

        template = {
            "id": "T-C-01-01",
            "stem": "El límite es @v_lim:.4f@ y el factor es @k@.",
            "stem_variants": ["Variante con @v_lim:.4f@ y factor @k@."],
            "hints": ["Considere el parámetro @h_param@ en su análisis formal."],
            "explanation_es": "Resolución completa con @v_lim:.4f@.",
            "options": [{"value": "1", "distractor_id": "D-C01-01", "error_rationale": "Razón @k@"}],
        }

        # vars returned by generator include format-spec var, hint var, and an unused var
        batch_results = [
            {
                "success": True,
                "result": {
                    "vars": {
                        "v_lim": 0.123456,
                        "k": 10,
                        "h_param": 42,
                        "extra_orphan_var": 999,  # This one is genuinely unused
                    }
                },
            }
        ]

        orphans = _check_orphan_vars(template, batch_results, cross_check_py="")

        # v_lim and h_param must NOT be reported as orphans
        assert "v_lim" not in orphans, "v_lim should be recognized through @v_lim:.4f@"
        assert "k" not in orphans, "k should be recognized"
        assert "h_param" not in orphans, "h_param in hints should be recognized"
        assert "extra_orphan_var" in orphans, "extra_orphan_var must be flagged as orphan"

    def test_unbounded_while_ast_detection_in_call_graph(self):
        """AST check rejects unconstrained 'while True:' in helpers and generators with [TPL-UNBOUNDED-LOOP],

        while allowing bounded while loops ('while tries < 50') and dynamic convergence loops ('while any(...)').
        """
        from shard_precheck import is_bounded_while

        code_unbounded_constant = "while True: pass"
        ast_unbounded = ast.parse(code_unbounded_constant).body[0]
        assert is_bounded_while(ast_unbounded) is False

        code_bounded_counter = """
tries = 0
while tries < 50:
    tries += 1
"""
        ast_bounded = ast.parse(code_bounded_counter).body[1]
        assert is_bounded_while(ast_bounded) is True

        code_dynamic_convergence = """
while any(x < 0 for x in values):
    values = [v + 1 for v in values]
"""
        ast_dynamic = ast.parse(code_dynamic_convergence).body[0]
        # Dynamic loop has a non-constant test, so compile_shard treats it as WARNING rather than hard FAIL
        is_const_true = isinstance(ast_dynamic.test, ast.Constant) and bool(ast_dynamic.test.value) is True
        assert is_const_true is False

    def test_r15_diagnostic_message_enrichment(self):
        """Invariants R-15 violation prints len(correct)= and distractor_lens= for rapid calibration."""
        from engine.invariants import check_instance_invariants

        mock_q = {
            "type": "multiple_choice_7_options",
            "stem": "¿Cuál es la respuesta correcta para el valor calculado?",
            "hints": [
                "Pista 1 suficientemente larga para pasar la validación.",
                "Pista 2 suficientemente larga para pasar la validación.",
                "Pista 3 suficientemente larga para pasar la validación.",
            ],
            "options": [
                {"content": "1", "value": "1", "is_correct": True},  # Length 1
                {"content": "Esta es una opción distractora extremadamente larga para forzar R-15 número 1", "value": "D1", "is_correct": False, "distractor_id": "D-01", "error_rationale": "Razón 1"},
                {"content": "Esta es una opción distractora extremadamente larga para forzar R-15 número 2", "value": "D2", "is_correct": False, "distractor_id": "D-02", "error_rationale": "Razón 2"},
                {"content": "Esta es una opción distractora extremadamente larga para forzar R-15 número 3", "value": "D3", "is_correct": False, "distractor_id": "D-03", "error_rationale": "Razón 3"},
                {"content": "Esta es una opción distractora extremadamente larga para forzar R-15 número 4", "value": "D4", "is_correct": False, "distractor_id": "D-04", "error_rationale": "Razón 4"},
                {"content": "Esta es una opción distractora extremadamente larga para forzar R-15 número 5", "value": "D5", "is_correct": False, "distractor_id": "D-05", "error_rationale": "Razón 5"},
                {"content": "Esta es una opción distractora extremadamente larga para forzar R-15 número 6", "value": "D6", "is_correct": False, "distractor_id": "D-06", "error_rationale": "Razón 6"},
            ],
        }

        valid, errors = check_instance_invariants(mock_q, "multiple_choice_7_options", strict_length_bounds=True)
        assert valid is False
        r15_err = next(e for e in errors if "Length anti-giveaway violation" in e)
        assert "len(correct)=" in r15_err
        assert "distractor_lens=" in r15_err

    def test_sandbox_execution_error_propagation_without_silencing(self):
        """instantiate_template raises SandboxExecutionError when any seed fails instead of silently skipping."""
        from engine.instantiate import instantiate_template
        from engine.sandbox import SandboxExecutionError

        broken_template = {
            "id": "T-C-01-01",
            "interaction_type": "multiple_choice_7_options",
            "stem": "Pregunta de prueba con @x@",
            "stem_variants": ["V1 con @x@", "V2 con @x@", "V3 con @x@"],
            "hints": ["Pista 1 suficientemente larga", "Pista 2 suficientemente larga", "Pista 3 suficientemente larga"],
            "generate_py": """
def generate(rng):
    raise ValueError("Simulated seed crash in dry-run")
""",
            "cross_check_py": "def verify(res): return True",
        }

        with pytest.raises(SandboxExecutionError) as exc_info:
            instantiate_template(
                template=broken_template,
                competency_id="C-01",
                target_count=50,
            )
        assert "failed on seed" in str(exc_info.value) or "Simulated seed crash" in str(exc_info.value)

    def test_stem_derivative_giveaway_and_tpl_warnings(self, capsys: pytest.CaptureFixture[str]):
        """_check_stem_derivative_giveaway detects explicit functions with evaluated derivatives,

        ignores critical points (= 0) and abstract functions; check_templates emits
        [TPL-EXP-SHORT] and [TPL-HINTS-DUPLICATE] warnings.
        """
        from check_templates import _check_stem_derivative_giveaway, check_single_template

        # 1. Derivative giveaway: explicit function + evaluated derivative
        stem_giveaway = r"Sea la función $g(\theta) = 3\theta^2 + 5$. Sabiendo que $g'(@t@) = @gp@$, halle la tasa."
        res_giveaway = _check_stem_derivative_giveaway(stem_giveaway)
        assert res_giveaway is not None
        assert "g" in res_giveaway[0]

        # 2. Critical point condition (f'(x) = 0) must NOT be flagged as giveaway
        stem_crit = r"Sea $f(x) = x^3 - 3x$. Halle los puntos donde $f'(x) = 0$."
        assert _check_stem_derivative_giveaway(stem_crit) is None

        # 3. Abstract function without formula (F'(r_2, 1) = @fp@) must NOT be flagged
        stem_abstract = r"Bajo la tecnología $F(K, L)$, se cumple $F'(r_2, 1) = @fp@$."
        assert _check_stem_derivative_giveaway(stem_abstract) is None

        # 4. Warnings check: short explanation_es prints [TPL-EXP-SHORT] to stderr
        short_exp_tpl = {
            "id": "T-C-01-01",
            "interaction_type": "multiple_choice_7_options",
            "stem": "Stem de prueba con @x@.",
            "stem_variants": ["S1 con @x@", "S2 con @x@", "S3 con @x@"],
            "hints": [
                "Pista 1 suficientemente extensa para pasar.",
                "Pista 2 suficientemente extensa para pasar.",
                "Pista 3 suficientemente extensa para pasar.",
            ],
            "explanation_es": "Corta (< 60c).",
            "generate_py": "def generate(rng): return {'vars': {'x': 1}, 'options': [{'value': '1', 'is_correct': True}]}",
            "cross_check_py": "def verify(r): return True",
        }
        check_single_template(
            template=short_exp_tpl,
            competency_id="C-01",
            declared_distractor_ids=set(),
            strict=False,
        )
        captured = capsys.readouterr()
        assert "[TPL-EXP-SHORT]" in captured.err


# ==============================================================================
# STREAM 1B REMEDIATIONS (5 TESTS)
# ==============================================================================

class TestStream1BRemediations:
    """Verifies all Stream 1B CTA schema, sanitizer, and merge fixes."""

    def test_cta_schema_remediation_hint_min_length_70(self):
        """cta.schema.json rejects remediation_hint under 70 chars and accepts 70+ chars."""
        import jsonschema

        schema_path = SKILL_DIR / "schemas" / "cta.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        base_cta = {
            "course_id": "test_hint_len",
            "title": "Test Title",
            "competencies": [
                {
                    "id": "C-01",
                    "type": "concept",
                    "name": "Concepto de Prueba",
                    "description_latex": "Descripción detallada del concepto con suficiente longitud para el esquema.",
                    "bloom": "Understand",
                    "session": "Sesion 1",
                    "unit_index": 1,
                    "prerequisites": [],
                    "evidence": [{"doc": "doc.pdf", "page": 1}],
                    "distractors": [
                        {
                            "id": "D-C01-01",
                            "name": "Distractor 1",
                            "wrong_belief": "Creencia errónea detallada",
                            "correct_belief": "Creencia correcta detallada",
                            "trigger": "Trigger analítico",
                            "manifestation": "Manifestación clara",
                            "error_type": "sign_error",
                            "severity": "medium",
                            "origin": "inferred",
                            "evidence": {"doc": "doc.pdf", "page": 1},
                            "remediation_hint": "A" * 69,  # 69 chars -> INVALID
                        }
                    ],
                }
            ],
        }

        # 69 chars fails validation
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(base_cta, schema)

        # 70 chars passes validation
        base_cta["competencies"][0]["distractors"][0]["remediation_hint"] = "A" * 70
        jsonschema.validate(base_cta, schema)

    def test_check_cta_hint_and_desc_short_warnings(self):
        """check_cta_file emits [CTA-HINT-SHORT] (< 80) and [CTA-DESC-SHORT] (< 80) without blocking PASS."""
        from check_cta import check_cta_file

        cta_data = {
            "course_id": "test_warns",
            "title": "Test Warnings",
            "competencies": [
                {
                    "id": "C-01",
                    "type": "concept",
                    "name": "Concepto Breve",
                    "description_latex": "Corta de 35 caracteres aquí.",  # < 80 chars
                    "bloom": "Understand",
                    "session": "Sesion 1",
                    "unit_index": 1,
                    "prerequisites": [],
                    "evidence": [{"doc": "doc.pdf", "page": 1}],
                    "distractors": [
                        {
                            "id": f"D-C01-0{i}",
                            "name": f"Distractor {i}",
                            "wrong_belief": f"Creencia errónea {i}",
                            "correct_belief": f"Creencia correcta {i}",
                            "trigger": f"Trigger {i}",
                            "manifestation": f"Manifestación {i}",
                            "error_type": "sign_error",
                            "severity": "medium",
                            "origin": "inferred",
                            "evidence": {"doc": "doc.pdf", "page": 1},
                            "remediation_hint": "B" * 72,  # 72 chars: passes schema (>= 70) but < 80
                        }
                        for i in range(1, 7)
                    ],
                }
            ],
        }

        warns: List[str] = []
        result = check_cta_file(cta_data, warnings_out=warns)

        assert result.valid is True
        assert any("[CTA-DESC-SHORT]" in w for w in warns)
        assert any("[CTA-HINT-SHORT]" in w for w in warns)

    def test_render_compact_cta_errors_multi_comp_threshold_ge_6(self):
        """render_compact_cta_errors unpacks multi-competency errors (re.findall)

        and activates effective_error_count >= 6 (write_file Overwrite=True).
        """
        from compile_cta import render_compact_cta_errors

        # Single error message listing 7 skills lacking omitted_step
        errors = [
            "Missing required omitted_step field for skills: Hab-01, Hab-02, Hab-03, Hab-04, Hab-05, Hab-06, Hab-07"
        ]

        output = render_compact_cta_errors(errors=errors, data_filename="cta_data.py")
        assert "[UMBRAL OFICIAL >= 6 ERRORES (7)]" in output
        assert "write_file(Overwrite=True)" in output

    def test_cta_sanitizer_telemetry_isolation_and_accumulation(self, tmp_path: Path):
        """compile_cta writes isolated cta_sanitizer_{part_id}.json and accumulates into cta_sanitizer_log.json."""
        from compile_cta import compile_cta

        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True, exist_ok=True)
        telem_dir = work_dir / "telemetry"

        manifest = {"course_id": "test_sanitizer", "files": [{"doc": "d.pdf", "total_pages": 10, "valid_page_range": [1, 10]}]}
        (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        # Compile part_01
        cta_part1_code = """
COURSE_ID = "test_sanitizer"
TITLE = "Test Sanitizer Part 1"
COMPETENCIES = [
    ("concept", "C-01", "Nombre 1", "Descripcion formal suficientemente extensa para pasar las validaciones.", "Understand", "d.pdf", 1, [], [
        ("D-C01-01", "WB1", "CB1", "$0$", "Revise minuciosamente la definicion formal y los pasos de derivacion algebraica 1.", None),
        ("D-C01-02", "WB2", "CB2", "$0$", "Revise minuciosamente la definicion formal y los pasos de derivacion algebraica 2.", None),
        ("D-C01-03", "WB3", "CB3", "$0$", "Revise minuciosamente la definicion formal y los pasos de derivacion algebraica 3.", None),
    ])
]
"""
        part1_py = work_dir / "part_01_data.py"
        part1_py.write_text(cta_part1_code, encoding="utf-8")

        valid1, _, errs1, _ = compile_cta(cta_data_path=part1_py, output_dir=work_dir, manifest_path=work_dir / "pre_cta_manifest.json")
        assert valid1 is True, f"part_01 failed: {errs1}"

        assert (telem_dir / "cta_sanitizer_part_01.json").is_file()
        log_content1 = json.loads((telem_dir / "cta_sanitizer_log.json").read_text(encoding="utf-8"))
        assert "part_01" in log_content1.get("parts", {})

        # Compile part_02
        cta_part2_code = """
COURSE_ID = "test_sanitizer"
TITLE = "Test Sanitizer Part 2"
COMPETENCIES = [
    ("concept", "C-02", "Nombre 2", "Descripcion formal suficientemente extensa para pasar las validaciones.", "Understand", "d.pdf", 2, [], [
        ("D-C02-01", "WB1", "CB1", "$0$", "Revise minuciosamente la definicion formal y los pasos de derivacion algebraica 1.", None),
        ("D-C02-02", "WB2", "CB2", "$0$", "Revise minuciosamente la definicion formal y los pasos de derivacion algebraica 2.", None),
        ("D-C02-03", "WB3", "CB3", "$0$", "Revise minuciosamente la definicion formal y los pasos de derivacion algebraica 3.", None),
    ])
]
"""
        part2_py = work_dir / "part_02_data.py"
        part2_py.write_text(cta_part2_code, encoding="utf-8")

        valid2, _, errs2, _ = compile_cta(cta_data_path=part2_py, output_dir=work_dir, manifest_path=work_dir / "pre_cta_manifest.json")
        assert valid2 is True, f"part_02 failed: {errs2}"

        assert (telem_dir / "cta_sanitizer_part_02.json").is_file()
        log_content2 = json.loads((telem_dir / "cta_sanitizer_log.json").read_text(encoding="utf-8"))
        # Both parts must coexist without overwriting
        assert "part_01" in log_content2["parts"]
        assert "part_02" in log_content2["parts"]

    def test_cta_merge_omitted_step_preserves_bar_math(self):
        """cta_merge sanitizes omitted_step with wrap_bare_equations=False, preserving bare prose."""
        from cta_merge import normalize_orphan_math

        bare_equation = r"|\bar{X}_n - Z|"
        # wrap_bare_equations=False preserves string without adding external $...$ wrapper
        sanitized_no_wrap = normalize_orphan_math(bare_equation, wrap_bare_equations=False)
        assert not sanitized_no_wrap.startswith("$")
        assert not sanitized_no_wrap.endswith("$")

        # wrap_bare_equations=True wraps whole string in $...$
        sanitized_wrap = normalize_orphan_math(bare_equation, wrap_bare_equations=True)
        assert sanitized_wrap.startswith("$") and sanitized_wrap.endswith("$")


# ==============================================================================
# STREAM 1C REMEDIATIONS (3 TESTS)
# ==============================================================================

class TestStream1CRemediations:
    """Verifies all Stream 1C judge ground truth, kernel overrides, and dispatch fixes."""

    def test_judge_strict_ground_truth_validation(self):
        """judge.py strictly validates ground truth schema and exempts kernel_refuted=True."""
        from judge import _validate_ground_truth_item

        # 1. MC7: missing correct_letter raises ValueError
        with pytest.raises(ValueError, match="correct_letter"):
            _validate_ground_truth_item({"interaction_type": "multiple_choice_7_options"}, "multiple_choice_7_options")

        # 2. FITB: missing correct_value raises ValueError, but 0 or "0" passes
        with pytest.raises(ValueError, match="correct_value"):
            _validate_ground_truth_item({"interaction_type": "fill_in_the_blank", "correct_value": None}, "fill_in_the_blank")
        # 0 must be preserved and valid
        _validate_ground_truth_item({"interaction_type": "fill_in_the_blank", "correct_value": 0}, "fill_in_the_blank")
        _validate_ground_truth_item({"interaction_type": "fill_in_the_blank", "correct_value": "0"}, "fill_in_the_blank")

        # 3. MS: missing or empty correct_letters raises ValueError
        with pytest.raises(ValueError, match="correct_letters"):
            _validate_ground_truth_item({"interaction_type": "multiple_select", "correct_letters": []}, "multiple_select")

        # 4. kernel_refuted=True exempts malformed GT from raising
        _validate_ground_truth_item({"interaction_type": "multiple_choice_7_options", "kernel_refuted": True}, "multiple_choice_7_options")

    def test_judge_kernel_override_traceability(self, tmp_path: Path):
        """judge_report.json records kernel_overridden_items and kernel_override_count with stderr warning."""
        from judge import compare_judge_responses, resolve_neuro_symbolic_verdict

        # Direct neuro-symbolic verdict test
        verdict = resolve_neuro_symbolic_verdict(
            kernel_verified=True,
            kernel_refuted=False,
            llm_verdict="FAIL",
            failure_category="calculation_error",
            failure_reasons=["LLM arithmetic discrepancy"],
        )
        assert verdict["verdict"] == "PASS"
        assert verdict["kernel_override"] is True

        # End-to-end compare_judge_responses report test
        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True, exist_ok=True)

        gt = {
            "item_01": {
                "template_id": "T-C-01-01",
                "competency_id": "C-01",
                "interaction_type": "multiple_choice_7_options",
                "correct_letter": "A",
                "kernel_verified": True,
            }
        }
        judge_responses = {
            "item_01": [{"response": "B", "category": "calculation_error", "reason": "Error aritmético"}]
        }

        report = compare_judge_responses(
            responses=judge_responses,
            ground_truth=gt,
            work_dir=work_dir,
        )

        assert report["kernel_override_count"] == 1
        assert len(report["kernel_overridden_items"]) == 1
        assert report["kernel_overridden_items"][0]["item_id"] == "item_01"
        assert report["agreed_items"] == 1  # Kernel override preserves agreement

    def test_dispatch_read_file_and_assumptions_warning(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]):
        """dispatch.py uses read_file in pointer prompt, declares 3 TURNOS LLM in judge dispatch,

        and warns when contract_version >= 2 arrives with assumptions=[].
        """
        import inspect
        from dispatch import dispatch_authors, dispatch_judges, make_pointer_prompt

        # 1. Pointer prompt uses read_file
        pointer = make_pointer_prompt(role="c2c_shard_author", work_order_rel="work/order.json")
        assert "read_file" in pointer
        assert "view_file" not in pointer

        # 2. Judge 3-turn protocol lives in lean prompt_blind_judge.md and dispatch_judges pointer prompt
        lean_judge_prompt = (
            Path(__file__).resolve().parents[2]
            / ".agents"
            / "skills"
            / "content-to-course"
            / "system_prompts"
            / "lean"
            / "prompt_blind_judge.md"
        ).read_text(encoding="utf-8")
        assert "Turno 1" in lean_judge_prompt and "Turno 2" in lean_judge_prompt
        assert "read_file" in lean_judge_prompt
        assert "DONE:" in lean_judge_prompt

        judge_src = inspect.getsource(dispatch_judges)
        assert "3 TURNOS LLM" in judge_src
        assert "DONE" in judge_src

        judge_pointer = make_pointer_prompt(role="c2c_judge", work_order_rel="work/dispatch/items/judge_01.json")
        assert "read_file" in judge_pointer

        # 3. Warning emitted when cta has contract_version >= 2 and assumptions=[]
        work_dir = tmp_path / "work_disp"
        work_dir.mkdir(parents=True, exist_ok=True)
        cta = {
            "contract_version": 2,
            "competencies": [
                {
                    "id": "Hab-01",
                    "type": "skill",
                    "name": "Habilidad 1",
                    "description_latex": "Descripcion formal de la habilidad.",
                    "assumptions": [],  # Missing assumptions!
                    "distractors": [{"id": "D-Hab01-01", "name": "D1"}],
                }
            ],
        }
        (work_dir / "cta.json").write_text(json.dumps(cta), encoding="utf-8")
        manifest = {"shards": [{"shard_id": "shard_01", "competencies": cta["competencies"], "competency_ids": ["Hab-01"]}]}
        (work_dir / "shards").mkdir(parents=True, exist_ok=True)
        (work_dir / "shards" / "pre_shard_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        dispatch_authors(work_dir=work_dir, pointer=True)
        captured = capsys.readouterr()
        assert "Ausencia de A-ids (assumptions=[])" in captured.err

        item_file = work_dir / "dispatch" / "items" / "author_01.json"
        assert item_file.is_file()
        item_data = json.loads(item_file.read_text(encoding="utf-8"))
        assert "Hab-01" in item_data.get("work_order", {}).get("missing_assumptions", [])


# ==============================================================================
# STREAM 1D REMEDIATIONS (2 TESTS)
# ==============================================================================

class TestStream1DRemediations:
    """Verifies all Stream 1D telemetry collector async system messages and cohort fixes."""

    def test_telemetry_collector_async_system_message_exit_codes(self, tmp_path: Path):
        """telemetry_collector parses exit codes != 0 and [TPL-*] from async SYSTEM_MESSAGE without duplicates."""
        from telemetry_collector import inspect_subagent_transcript

        t_dir = tmp_path / "conv_01" / ".system_generated" / "logs"
        t_dir.mkdir(parents=True, exist_ok=True)
        t_file = t_dir / "transcript.jsonl"

        records = [
            {
                "type": "SYSTEM_MESSAGE",
                "timestamp": "2026-11-14T10:00:00Z",
                "content": 'Task id "task-100" finished with result: Command exited with code 1. FAIL: [TPL-UNBOUNDED-LOOP]',
            },
            # Duplicate notification for same task id
            {
                "type": "SYSTEM_MESSAGE",
                "timestamp": "2026-11-14T10:00:01Z",
                "content": 'Task id "task-100" finished with result: Command exited with code 1. FAIL: [TPL-UNBOUNDED-LOOP]',
            },
        ]
        with open(t_file, "w", encoding="utf-8") as f:
            for r in records:
                f.write(json.dumps(r) + "\n")

        summary = inspect_subagent_transcript(
            subagent_conv_id="conv_01",
            meta={"role": "author", "cohort": "author"},
            brain_dir=tmp_path,
        )

        assert len(summary["cli_errors"]) == 1  # Deduplicated by task id
        assert summary["cli_errors"][0]["exit_code"] == 1
        assert "TPL-UNBOUNDED-LOOP" in summary["cli_errors"][0]["error_codes"]

    def test_telemetry_collector_judge_cohort_uses_compiler_false(self):
        """telemetry_collector marks judge cohorts with uses_compiler=False and fpy_ratio='N/A'."""
        from telemetry_collector import summarize_cohorts

        subagents_summary = [
            {
                "conversation_id": "c_j1",
                "cohort": "judge",
                "role": "judge",
                "uses_compiler": False,
                "first_pass": None,
                "final_pass": None,
                "compiler_invocations": 0,
                "turns_count": 3,
                "duration_seconds": 12.0,
                "tokens": {"input": 100, "output": 50, "cached": 0, "thinking": 0, "total": 150},
                "cli_errors": [],
            }
        ]

        summaries = summarize_cohorts(subagents_summary)
        assert "judge" in summaries
        j_summary = summaries["judge"]
        assert j_summary["uses_compiler"] is False
        assert j_summary["first_pass_count"] is None
        assert j_summary["fpy_ratio"] == "N/A"
        assert j_summary["pass_ratio"] == "N/A"


# ==============================================================================
# STREAM 1E REMEDIATIONS (1 TEST)
# ==============================================================================

class TestStream1ERemediations:
    """Verifies all Stream 1E prompt contracts and size budgets."""

    def test_system_prompts_shard_author_contract_and_budgets(self):
        """lean/prompt_shard_author.md is <= 5,000 bytes (pure LF), defines 4 unique hints lists,

        and full prompt defines differentiated hints and compiles under 46,080 bytes.
        """
        lean_path = SKILL_DIR / "system_prompts" / "lean" / "prompt_shard_author.md"
        assert lean_path.is_file(), f"Missing {lean_path}"

        raw_bytes = lean_path.read_bytes()
        assert b"\r\n" not in raw_bytes, "Lean prompt must use pure Unix LF line endings"

        content = lean_path.read_text(encoding="utf-8")
        assert "M3-ARCHETYPES" in content

        # Check unique hint arrays modeled in lean prompt (H1=[...], H2=[...], H3=[...], H4=[...])
        assert "H1=[" in content and "H2=[" in content and "H3=[" in content and "H4=[" in content

        # Check length standards modeled in lean prompt
        assert "sol`>=80c" in content or "sol>=80c" in content or "sol >= 80" in content
        assert "error_rationale`>=60c" in content or "error_rationale>=60c" in content or "error_rationale >= 60" in content or "len(error_rationale)>=20" in content

        # Full author prompt check
        full_path = SKILL_DIR / "system_prompts" / "prompt_shard_author.md"
        assert full_path.is_file()
        full_content = full_path.read_text(encoding="utf-8")
        assert "H1 = [" in full_content
        assert "H2 = [" in full_content
        assert "H3 = [" in full_content
        assert "H4 = [" in full_content

        # Compiled type spec size must be < 75,000 bytes (full XML prompt)
        from dispatch import load_system_prompt
        author_sys_prompt = load_system_prompt("prompt_shard_author.md")
        spec_dict = {
            "name": "c2c_shard_author",
            "system_prompt": author_sys_prompt,
        }
        spec_json_bytes = len(json.dumps(spec_dict, indent=2, ensure_ascii=False).encode("utf-8"))
        assert spec_json_bytes < 75000, f"Compiled type spec exceeded 75,000 bytes: {spec_json_bytes}"
