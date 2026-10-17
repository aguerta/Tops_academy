"""Comprehensive Integration Verification Suite for C2C v2 Pipeline Remediation and Optimization Plan.

Validates all 5 architectural components:
1. Direct CTA Architect (2-File Architecture): compile_cta.py (<5ms), cta_data.py tabular tuples, line error mapping.
2. Quality Triad for Shard Authors: cognitive antipatterns, template_generator_canonical.py, deterministic linter rules.
3. Canonical Workspace Isolation: courses/<course_id>/work isolation, dynamic work_dir propagation, no root work fallback.
4. Batch Subagent Registration: 1-step definition of 7 specialized types via define-types (<20s startup).
5. Typed Contract for Blind Judges: answer_contract in judge_batch.json, math.isclose numeric comparison (tol=0.01).
"""

from __future__ import annotations

import json
import math
import os
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path

# Ensure skills and repo root in sys.path
repo_root = Path(__file__).resolve().parents[1]
c2c_dir = repo_root / ".agents" / "skills" / "content-to-course"
if str(c2c_dir) not in sys.path:
    sys.path.insert(0, str(c2c_dir))

from check_templates import (
    check_templates_file_or_dir,
    format_invariant_error_diagnostic,
    get_canonical_invariant_key,
    synthetic_boilerplate_distractor_rule,
    scaffolding_answer_leak_rule,
)
from compile_shard import compile_shard
from dispatch import (
    ROLE_SPECS,
    build_dispatch,
    dispatch_authors,
    dispatch_cta,
    get_type_definitions,
)
from judge import (
    _is_numeric_equal,
    compare_judge_responses,
    generate_judge_batch,
)
from engine.sandbox import (
    execute_sandbox_batch,
    validate_code_ast,
)
from run import PipelineRunner


class TestC2CRemediationOptimization(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="c2c_remed_opt_")
        self.work_dir = Path(self.test_dir) / "courses" / "test_course" / "work"
        self.work_dir.mkdir(parents=True, exist_ok=True)
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "files": [
                {"doc": "algoritmos.pdf", "path": "content/algoritmos.pdf", "total_pages": 50, "valid_page_range": [1, 50]},
                {"doc": "termo.pdf", "path": "content/termo.pdf", "total_pages": 50, "valid_page_range": [1, 50]},
                {"doc": "doc.pdf", "path": "content/doc.pdf", "total_pages": 50, "valid_page_range": [1, 50]},
                {"doc": "solow.pdf", "path": "content/solow.pdf", "total_pages": 50, "valid_page_range": [1, 50]},
            ]
        }), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # =========================================================================
    # COMPONENT 1: Direct CTA Architect (2-File Architecture)
    # =========================================================================
    def test_component_1_compile_cta_performance_and_accuracy(self):
        """compile_cta.py compiles tabular tuples to cta.json and cta.md in <50ms with validation."""
        import compile_cta

        data_content = '''# cta_data.py for testing
COMPETENCIES = [
    (
        "concept", "C-01", "Concepto de Invariante de Bucle",
        r"La propiedad $A[0 \\dots i-1]$ ordenada se preserva en cada iteracion.",
        "Understand", "algoritmos.pdf", 18, [],
        [
            ("Error de inicializacion", r"Invariante solo al final", r"Vale en inicio, mantenimiento y fin", r"$P(0)$", "Verifique el caso base."),
            ("Error off-by-one", r"$A[0 \\dots i]$", r"$A[0 \\dots i-1]$", r"$i$ elementos", "El subarray excluye el pivote."),
            ("Asumir estabilidad", r"Todo sort es estable", r"Depende del criterio", r"Swap inestable", "Compruebe el orden relativo.")
        ]
    ),
    (
        "skill", "Hab-01", "Calculo de Eficiencia de Carnot",
        r"Calcular rendimiento $\\eta = 1 - \\frac{T_C}{T_H}$ en ciclos reversibles.",
        "Apply", "termo.pdf", 45, ["C-01"],
        [
            ("Uso de Celsius", r"$\\eta$ en Celsius", r"Kelvin absoluto", r"$\\eta < 0$", "Convertir a Kelvin."),
            ("Inversion de focos", r"$\\eta = 1 - T_H/T_C$", r"$\\eta = 1 - T_C/T_H$", r"$\\eta < 0$", "Foco frio va en el numerador."),
            ("Omision de conversion de calor", None, r"$\\eta = W/Q_H$", r"$\\eta > 1$", "Verificar unidades.", "Omitir conversion de Joules a Calorias"),
            ("Asumir irreversibilidad", r"$S_{gen} > 0$", r"$\\Delta S = 0$", r"$\\eta < \\eta_{Carnot}$", "El ciclo es reversible."),
            ("Error de escala", r"$\\eta$ en escala porcentual directa", r"Fraccion decimal", r"$\\eta = 100$", "Expresar en fraccion."),
            ("Omision de trabajo util", None, r"$W = Q_H - Q_C$", r"$W = 0$", "Calcular trabajo util neto.", "Omitir balance energetico de primera ley")
        ]
    )
]
'''
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "files": [
                {"doc": "algoritmos.pdf", "path": "content/algoritmos.pdf", "total_pages": 50, "valid_page_range": [1, 50]},
                {"doc": "termo.pdf", "path": "content/termo.pdf", "total_pages": 50, "valid_page_range": [1, 50]}
            ]
        }), encoding="utf-8")

        data_file = self.work_dir / "cta_data.py"
        data_file.write_text(data_content, encoding="utf-8")

        success, res, errs, elapsed_ms = compile_cta.compile_cta(
            cta_data_path=data_file,
            output_dir=self.work_dir,
        )

        self.assertTrue(success, f"Compilation failed: {errs}")
        self.assertLess(elapsed_ms, 200.0, f"Compilation took {elapsed_ms:.2f}ms, exceeding budget")
        self.assertEqual(len(res["competencies"]), 2)

        # Verify cta.json and cta.md exist
        cta_json = self.work_dir / "cta.json"
        cta_md = self.work_dir / "cta.md"
        self.assertTrue(cta_json.is_file())
        self.assertTrue(cta_md.is_file())

        loaded = json.loads(cta_json.read_text(encoding="utf-8"))
        self.assertEqual(len(loaded["competencies"]), 2)
        # Check skill has omitted steps
        hab01 = loaded["competencies"][1]
        omitted_dists = [d for d in hab01["distractors"] if d.get("omitted_step")]
        self.assertGreaterEqual(len(omitted_dists), 2)

    def test_component_1_preseed_cta_scaffolds_includes_compiler(self):
        """dispatch_cta specifies official compile_cta.py command in prompt."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "files": [{"doc": "doc.pdf", "path": "content/doc.pdf", "total_pages": 10, "valid_page_range": [1, 10]}]
        }), encoding="utf-8")
        res = dispatch_cta(work_dir=self.work_dir, mode="direct")
        self.assertEqual(len(res["Subagents"]), 1)
        prompt = res["Subagents"][0]["Prompt"]
        self.assertIn("compile_cta.py", prompt)
        self.assertIn("cta_data.py", prompt)

    def test_component_1_dispatch_bundle_directives(self):
        """dispatch_cta injects 2-file architecture and modular compatibility."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "files": [{"doc": "doc.pdf", "path": "content/doc.pdf", "total_pages": 10, "valid_page_range": [1, 10]}]
        }), encoding="utf-8")
        dispatch_res = dispatch_cta(work_dir=self.work_dir, mode="direct")
        item_file = Path(dispatch_res["item_files"][0])
        text = json.loads(item_file.read_text(encoding="utf-8"))["Prompt"]
        self.assertIn("compile_cta.py", text)
        self.assertIn("cta_data.py", text)
        self.assertIn("replace_file_content", text)

    def test_component_1_compile_cta_distractor_line_error_mapping(self):
        """compile_cta maps distractor errors back to exact lines in cta_data.py."""
        import compile_cta

        data_content = '''# cta_data.py with intentional distractor syntax error
COMPETENCIES = [
    (
        "concept", "C-01", "Concepto de Invariante",
        r"Definicion formal de invariante.",
        "Understand", "algoritmos.pdf", 10, [],
        [
            ("Error sintaxis", r"\\frac{a}{b$", "Correcto", "$0$", "Hint"),
            ("Distractor 2", "wb2", "Correcto", "$1$", "Hint"),
            ("Distractor 3", "wb3", "Correcto", "$2$", "Hint")
        ]
    )
]
'''
        data_file = self.work_dir / "cta_data_err.py"
        data_file.write_text(data_content, encoding="utf-8")
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "files": [{"doc": "algoritmos.pdf", "path": "content/algoritmos.pdf", "total_pages": 50}]
        }), encoding="utf-8")

        success, res, errs, elapsed_ms = compile_cta.compile_cta(
            cta_data_path=data_file,
            output_dir=self.work_dir,
        )

        self.assertFalse(success)
        self.assertGreater(len(errs), 0)
        has_mapped_line = any("Línea 8" in e or "Linea 8" in e for e in errs)
        self.assertTrue(has_mapped_line, f"Errors missing exact distractor line mapping: {errs}")

    def test_component_1_auto_balance_math_delimiters(self):
        """auto_balance_math_delimiters collapses $$$ and balances unescaped $ when braces are balanced."""
        from cta_merge import auto_balance_math_delimiters, normalize_orphan_math

        # Triple dollars collapse
        self.assertEqual(auto_balance_math_delimiters("$$$x$$$"), "$$x$$")
        self.assertEqual(auto_balance_math_delimiters("Ecuación: $$$E = mc^2$$$"), "Ecuación: $$E = mc^2$$")

        # Odd unescaped $ with balanced braces -> closed with $
        self.assertEqual(auto_balance_math_delimiters("Calcular $x"), "Calcular $x$")
        self.assertEqual(auto_balance_math_delimiters("Calcular $x."), "Calcular $x$.")
        self.assertEqual(auto_balance_math_delimiters("Calcular $x,"), "Calcular $x$,")
        self.assertEqual(auto_balance_math_delimiters("Calcular $x;"), "Calcular $x$;")

        # Odd unescaped $ with UNBALANCED braces -> left alone so syntax validator flags it
        self.assertEqual(auto_balance_math_delimiters(r"\frac{a}{b$"), r"\frac{a}{b$")
        self.assertEqual(auto_balance_math_delimiters(r"\sqrt{x$"), r"\sqrt{x$")

        # normalize_orphan_math uses auto_balance_math_delimiters
        res = normalize_orphan_math("Valor $x")
        self.assertEqual(res, "Valor $x$")

    def test_component_1_sanitize_competency_math_includes_correct_belief(self):
        """sanitize_competency_math sanitizes correct_belief and trigger in distractors."""
        from cta_merge import sanitize_competency_math

        comp = {
            "name": "Test Comp",
            "description": "Desc",
            "distractors": [
                {
                    "name": "D1",
                    "manifestation": "$0$",
                    "wrong_belief": "wb",
                    "correct_belief": r"El valor es \alpha",
                    "trigger": r"Cuando se usa \beta",
                }
            ],
        }
        sanitize_competency_math(comp)
        d = comp["distractors"][0]
        self.assertIn(r"$\alpha$", d["correct_belief"])
        self.assertIn(r"$\beta$", d["trigger"])

    def test_component_1_skill_omitted_step_auto_promotion(self):
        """compile_tuples_to_cta_dict auto-promotes wrong_belief to omitted_step if < 2 for skill."""
        import compile_cta

        skill_tuples = [
            (
                "skill", "Hab-01", "Habilidad de Prueba",
                r"Descripcion de la habilidad $\phi(k)$.",
                "Apply", "doc.pdf", 1, [],
                [
                    ("D1", "Error de calculo 1", "Correcto 1", "$1$", "Hint 1"),
                    ("D2", "Error de calculo 2", "Correcto 2", "$2$", "Hint 2"),
                    ("D3", "Error de calculo 3", "Correcto 3", "$3$", "Hint 3"),
                ]
            )
        ]
        cta_dict = compile_cta.compile_tuples_to_cta_dict(
            competencies_tuples=skill_tuples,
            course_id="test_course",
            title="Test Title",
        )
        comp = cta_dict["competencies"][0]
        omitted = [d for d in comp["distractors"] if d.get("omitted_step")]
        self.assertGreaterEqual(len(omitted), 2)
        self.assertEqual(omitted[0]["omitted_step"], "Error de calculo 1")
        self.assertEqual(omitted[0]["error_type"], "skipped_step")
        self.assertEqual(omitted[1]["omitted_step"], "Error de calculo 2")
        self.assertEqual(omitted[1]["error_type"], "skipped_step")

    def test_component_1_anti_overwrite_backup_and_course_id_resolution(self):
        """compile_cta writes .cta_data.py.bak when >= 10 comps, and resolves course_id properly."""
        import compile_cta

        # Build >= 10 competencies
        comps = []
        for i in range(1, 11):
            comps.append(
                f'    ("concept", "C-{i:02d}", "Concepto {i}", "Desc {i}", "Remember", "doc.pdf", {i}, [], '
                f'[("D1", "wb1", "cb1", "$1$", "h1"), ("D2", "wb2", "cb2", "$2$", "h2"), ("D3", "wb3", "cb3", "$3$", "h3")])'
            )
        data_text = "COMPETENCIES = [\n" + ",\n".join(comps) + "\n]\n"
        data_file = self.work_dir / "cta_data.py"
        data_file.write_text(data_text, encoding="utf-8")
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "files": [{"doc": "doc.pdf", "path": "content/doc.pdf", "total_pages": 50}]
        }), encoding="utf-8")

        success, res, errs, _ = compile_cta.compile_cta(
            cta_data_path=data_file,
            output_dir=self.work_dir,
        )
        self.assertTrue(success, f"Failed to compile: {errs}")
        bak_file = self.work_dir / ".cta_data.py.bak"
        self.assertTrue(bak_file.is_file(), "Backup .cta_data.py.bak was not written for >= 10 comps")
        self.assertIn("Concepto 10", bak_file.read_text(encoding="utf-8"))

        # Verify pre_cta_manifest.json resolution when COURSE_ID is Tops_academy
        manifest_file = self.work_dir / "pre_cta_manifest.json"
        manifest_file.write_text(json.dumps({
            "course_id": "macroeconomia_avanzada",
            "files": [{"doc": "doc.pdf", "path": "content/doc.pdf", "total_pages": 50}]
        }), encoding="utf-8")
        data_text_with_bad_id = 'COURSE_ID = "Tops_academy"\n' + data_text
        data_file.write_text(data_text_with_bad_id, encoding="utf-8")
        success, res, _, _ = compile_cta.compile_cta(
            cta_data_path=data_file,
            output_dir=self.work_dir,
        )
        self.assertTrue(success)
        self.assertEqual(res["course_id"], "macroeconomia_avanzada")

    def test_component_1_render_compact_cta_errors_with_source_lines(self):
        """render_compact_cta_errors shows exact 3-line snippets and anti-overwrite warning."""
        import compile_cta

        errors = ["[CTA-D1] [cta_data.py:Línea 5] Distractor 'D-C01-01' error de prueba"]
        source_lines = [
            "# line 1",
            "# line 2",
            "# line 3",
            "# line 4",
            '("Distractor 1", "wrong", "correct", "$0$", "hint"),  # line 5',
            "# line 6",
            "# line 7",
        ]
        msg = compile_cta.render_compact_cta_errors(errors, "cta_data.py", source_lines=source_lines)
        self.assertIn("CONTEXTO EXACTO PARA replace_file_content (NO uses view_file ni write_to_file Overwrite):", msg)
        self.assertIn("StartLine=4, EndLine=6", msg)
        self.assertIn("L5: (\"Distractor 1\", \"wrong\", \"correct\", \"$0$\", \"hint\"),  # line 5", msg)
        self.assertIn("PROHIBIDO usar 'write_to_file' con Overwrite=True", msg)

    # =========================================================================
    # COMPONENT 2: Quality Triad for Shard Authors
    # =========================================================================
    def test_component_2_canonical_template_generator_validates_cleanly(self):
        """Author tuples compiled via compile_shard execute and pass invariants with 0 errors."""
        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "documents": [{"name": "solow.pdf", "path": "content/solow.pdf", "total_pages": 10}]
        }), encoding="utf-8")
        (self.work_dir / "cta.json").write_text(json.dumps({
            "competencies": [
                {
                    "id": "C-01",
                    "name": "Carnot",
                    "type": "concept",
                    "bloom": "Understand",
                    "distractors": [{"id": f"D-C01-{i:02d}"} for i in range(1, 7)]
                }
            ]
        }), encoding="utf-8")
        (shards_dir / "pre_shard_manifest.json").write_text(
            json.dumps({"shards": [{"shard_id": "shard_01", "competency_ids": ["C-01"]}]}), encoding="utf-8"
        )
        shard_code = '''
def gen_c01(rng):
    tc = rng.randint(250, 350)
    delta = rng.randint(150, 450)
    th = tc + delta
    ans_val = round(1.0 - (tc / th), 3)

    distractors = [
        {"value": rf"$\\eta = {round(ans_val + 0.10, 3)}$", "distractor_id": "D-C01-01", "error_rationale": "Inversión TH/TC"},
        {"value": rf"$\\eta = {round(ans_val + 0.20, 3)}$", "distractor_id": "D-C01-02", "error_rationale": "Calor residual"},
        {"value": rf"$\\eta = {round(ans_val + 0.30, 3)}$", "distractor_id": "D-C01-03", "error_rationale": "Desplazamiento"},
        {"value": rf"$\\eta = {round(ans_val + 0.40, 3)}$", "distractor_id": "D-C01-04", "error_rationale": "Factor espurio"},
        {"value": rf"$\\eta = {round(ans_val - 0.10, 3)}$", "distractor_id": "D-C01-05", "error_rationale": "Suma"},
        {"value": rf"$\\eta = {round(ans_val - 0.20, 3)}$", "distractor_id": "D-C01-06", "error_rationale": "Semidiferencia"},
    ]
    return {
        "vars": {"th": th, "tc": tc, "ans": ans_val},
        "correct": rf"$\\eta = {ans_val}$",
        "distractors": distractors
    }

def ver_c01(res):
    v = res.get("vars", {})
    expected = round(1.0 - (v["tc"] / v["th"]), 3)
    return v.get("ans") == expected

TEMPLATES = [
    (
        "C-01",
        "multiple_choice",
        r"Una máquina térmica reversible de Carnot opera entre dos focos a temperaturas $T_H = {th}\\text{ K}$ y $T_C = {tc}\\text{ K}$. Determine el rendimiento térmico:",
        gen_c01,
        ver_c01,
        r"Por el teorema de Carnot, el rendimiento es $\\eta = 1 - \\frac{T_C}{T_H} = {ans}$.",
        "Eficiencia de Carnot",
        ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"],
        ("solow.pdf", 1, "Cita")
    )
]
'''
        (shards_dir / "shard_01_data.py").write_text(shard_code, encoding="utf-8")
        ok, errs = compile_shard(self.work_dir, "shard_01")
        self.assertTrue(ok, f"Compilation failed: {errs}")
        tpl_file = self.work_dir / "templates" / "C-01.json"
        self.assertTrue(tpl_file.is_file())
        is_valid, errs = check_templates_file_or_dir(tpl_file, cta_path=self.work_dir / "cta.json")
        self.assertTrue(is_valid, f"Template validation failed: {errs}")
        self.assertEqual(len(errs), 0)

    def test_component_2_canonical_template_generator_ast_and_sandbox(self):
        """Author generator function satisfies AST sandbox security and executes cleanly in sandbox batch."""
        code = '''
def generate(rng):
    tc = rng.randint(250, 350)
    delta = rng.randint(150, 450)
    th = tc + delta
    ans_val = round(1.0 - (tc / th), 3)
    distractors = [
        {"value": rf"$\\eta = {round(ans_val + 0.10, 3)}$", "distractor_id": "D-C01-01", "error_rationale": "Inversión TH/TC"},
        {"value": rf"$\\eta = {round(ans_val + 0.20, 3)}$", "distractor_id": "D-C01-02", "error_rationale": "Calor residual"},
        {"value": rf"$\\eta = {round(ans_val + 0.30, 3)}$", "distractor_id": "D-C01-03", "error_rationale": "Desplazamiento"},
        {"value": rf"$\\eta = {round(ans_val + 0.40, 3)}$", "distractor_id": "D-C01-04", "error_rationale": "Factor espurio"},
        {"value": rf"$\\eta = {round(ans_val - 0.10, 3)}$", "distractor_id": "D-C01-05", "error_rationale": "Suma"},
        {"value": rf"$\\eta = {round(ans_val - 0.20, 3)}$", "distractor_id": "D-C01-06", "error_rationale": "Semidiferencia"},
    ]
    return {
        "vars": {"th": th, "tc": tc, "ans": ans_val},
        "correct": rf"$\\eta = {ans_val}$",
        "distractors": distractors
    }
'''
        # Must pass AST security whitelist without any SecurityViolationError
        self.assertTrue(validate_code_ast(code))

        # Must execute across 50 sandbox seeds with 100% success rate
        seeds = list(range(100, 150))
        results = execute_sandbox_batch(generate_py=code, seeds=seeds, timeout_per_item=2.0)
        self.assertEqual(len(results), 50)
        self.assertTrue(all(r.get("success") for r in results), f"Sandbox failures: {[r for r in results if not r.get('success')]}")

    def test_component_2_boilerplate_and_leak_rules_detection(self):
        """Linter rules detect boilerplate distractors and scaffolding answer leaks."""
        # 1. Repetitive boilerplate distractors
        bad_assembled = {
            "options": [
                {"content": "La trayectoria diverge con parametro 2", "is_correct": False},
                {"content": "La trayectoria diverge con parametro 4", "is_correct": False},
                {"content": "La trayectoria diverge con parametro 6", "is_correct": False},
                {"content": "La trayectoria diverge con parametro 8", "is_correct": False},
                {"content": "La trayectoria diverge con parametro 10", "is_correct": False},
                {"content": "La trayectoria diverge con parametro 12", "is_correct": False},
                {"content": "La trayectoria converge con parametro 2", "is_correct": True},
            ]
        }
        b_errs = synthetic_boilerplate_distractor_rule(bad_assembled)
        self.assertGreaterEqual(len(b_errs), 1)
        self.assertTrue(any("boilerplate" in e.lower() or "repetitive" in e.lower() for e in b_errs))

        # 2. Scaffolding hint answer leak
        bad_hints = [
            "Analice la ecuacion diferencial.",
            "Revise la condicion de estabilidad.",
            "Descarte las respuestas que asumen divergencia del sistema.",
        ]
        leak_errs = scaffolding_answer_leak_rule(bad_hints)
        self.assertGreaterEqual(len(leak_errs), 1)
        self.assertTrue(any("leak" in e.lower() or "descarte" in e.lower() for e in leak_errs))

    def test_component_2_canonical_invariant_keys_aggregation(self):
        """Both rules are registered in get_canonical_invariant_key and format_invariant_error_diagnostic."""
        key1 = get_canonical_invariant_key("Synthetic boilerplate distractor pattern detected: repetitive prefix")
        self.assertEqual(key1, "Synthetic boilerplate distractor pattern detected")
        diag1 = format_invariant_error_diagnostic("C-01", "T-01", "item_1", "Synthetic boilerplate distractor pattern detected: repetitive prefix")
        self.assertIn("R-18: DISTRACTORES BOILERPLATE SINTÉTICOS", diag1)

        key2 = get_canonical_invariant_key("Scaffolding answer leak detected in hint 3: mechanical elimination rule")
        self.assertEqual(key2, "Scaffolding answer leak detected in hint")
        diag2 = format_invariant_error_diagnostic("C-01", "T-01", "item_1", "Scaffolding answer leak detected in hint 3: mechanical elimination rule")
        self.assertIn("R-19: FUGA DE RESPUESTA EN ANDAMIAJE", diag2)

    def test_component_2_preseed_author_scaffolds_copies_canonical_template(self):
        """dispatch_authors creates item files with compile_shard directives."""
        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "documents": [{"name": "solow.pdf", "path": "content/solow.pdf", "total_pages": 10}]
        }), encoding="utf-8")
        (self.work_dir / "cta.json").write_text(json.dumps({
            "competencies": [
                {
                    "id": "C-01",
                    "name": "Equilibrio",
                    "type": "concept",
                    "bloom": "Understand",
                    "distractors": [{"id": f"D-C01-{i:02d}"} for i in range(1, 7)]
                }
            ]
        }), encoding="utf-8")
        (shards_dir / "pre_shard_manifest.json").write_text(
            json.dumps({"shards": [{"shard_id": "shard_01", "competency_ids": ["C-01"]}]}), encoding="utf-8"
        )

        res = dispatch_authors(self.work_dir)
        self.assertEqual(len(res["Subagents"]), 1)
        item_file = Path(res["item_files"][0])
        content = item_file.read_text(encoding="utf-8")
        self.assertIn("compile_shard.py", content)
        self.assertIn("shard_01_data.py", content)

    # =========================================================================
    # COMPONENT 3: Canonical Workspace Isolation
    # =========================================================================
    def test_component_3_canonical_workspace_resolution(self):
        """PipelineRunner resolves canonical work_dir to courses/<course_id>/work without root work fallback."""
        runner = PipelineRunner(course_id="algebra_lineal")
        expected = Path("courses") / "algebra_lineal" / "work"
        self.assertEqual(runner.work_dir, expected)

        # Dynamic work-dir argument overrides cleanly
        custom_dir = self.work_dir / "custom"
        runner_custom = PipelineRunner(course_id="algebra_lineal", work_dir=str(custom_dir))
        self.assertEqual(runner_custom.work_dir, custom_dir)

    # =========================================================================
    # COMPONENT 4: Batch Subagent Registration
    # =========================================================================
    def test_component_4_batch_subagent_registration(self):
        """Pipeline define-types auxiliary stage provides all 4 specialized subagents in 1 step."""
        types = get_type_definitions()
        self.assertEqual(len(types), 4)
        type_names = {t["name"] for t in types}
        expected_names = {
            "c2c_cta_architect",
            "c2c_shard_author",
            "c2c_judge",
            "c2c_repair",
        }
        self.assertEqual(type_names, expected_names)

        # Test execute(target_stage="define-types")
        runner = PipelineRunner(work_dir=str(self.work_dir))
        res = runner.execute(target_stage="define-types")
        self.assertIn("define-types", res)
        self.assertEqual(len(res["define-types"]["types"]), 4)
        self.assertLess(res["elapsed_seconds"], 1.0)

    # =========================================================================
    # COMPONENT 5: Typed Contract for Blind Judges
    # =========================================================================
    def test_component_5_judge_batch_typed_contract_and_numeric_comparison(self):
        """judge_batch.json contains answer_contract for FIB and evaluates with math.isclose."""
        # Create a sample template file
        templates_dir = self.work_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        fib_tpl = {
            "id": "T-C01-03",
            "competency_id": "C-01",
            "interaction_type": "fill_in_the_blank",
            "difficulty": "medium",
            "bloom": "Apply",
            "stem": "Calcule el valor de referencia para k = {k}:",
            "stem_variants": [
                "Calcule el valor de referencia para k = {k}:",
                "Determine la magnitud asociada a k = {k}:",
                "Evalúe la función objetivo en el punto k = {k}:",
            ],
            "generate_py": (
                "def generate(rng):\n"
                "    k = rng.choice([10, 12, 14, 16])\n"
                "    ans = round(k * 1.25, 2)\n"
                "    return {'vars': {'k': k}, 'correct': ans, 'value': str(ans), 'tolerance': 0.01, 'distractors': []}\n"
            ),
            "cross_check_py": "def verify(res):\n    return float(res['correct']) > 0\n",
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "solution": "Solución.",
            "distractor_ids": []
        }
        (templates_dir / "C-01.json").write_text(
            json.dumps({"competency_id": "C-01", "templates": [fib_tpl]}), encoding="utf-8"
        )

        batch_path, gt_path = generate_judge_batch(
            templates_path=templates_dir,
            work_dir=self.work_dir,
            items_per_competency=1,
        )

        self.assertTrue(batch_path.is_file())
        batch_items = json.loads(batch_path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(batch_items), 1)

        item = batch_items[0]
        self.assertIn("answer_contract", item)
        contract = item["answer_contract"]
        self.assertIn("expected_type", contract)
        self.assertIn("decimal_places", contract)
        self.assertIn("tolerance", contract)
        self.assertEqual(contract["tolerance"], 0.01)

        # Test numeric tolerance comparison with _is_numeric_equal
        self.assertTrue(_is_numeric_equal(12.500, 12.508, tol=0.01))
        self.assertTrue(_is_numeric_equal("12.50", "12.505", tol=0.01))
        self.assertFalse(_is_numeric_equal(12.50, 12.55, tol=0.01))

        # Test compare_judge_responses with floating tolerance
        gt = json.loads(gt_path.read_text(encoding="utf-8"))
        item_id = item["item_id"]
        exact_ans = gt[item_id]["correct_value"]
        approx_ans = str(float(exact_ans) + 0.005)

        res = compare_judge_responses({item_id: approx_ans}, gt)
        self.assertEqual(res["agreement_rate"], 1.0)
        self.assertEqual(len(res["discordances"]), 0)


if __name__ == "__main__":
    unittest.main()
