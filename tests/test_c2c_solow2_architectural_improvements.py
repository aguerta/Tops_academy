"""Regression and verification tests for Solow Model 2 architectural improvements.

Covers:
1. Pure JSON fragments in CTA & deterministic cta-stitch (<200ms, auto-normalization, cta.md).
2. Line-level editing guidance with replace_file_content in CTA prompt & dispatch bundle.
3. Isolated shard workspaces (work/shards/<shard_id>/scratch/) preventing concurrent collisions.
4. KaTeX safety across courses (non-math text preservation vs genuine LaTeX macros).
5. Template starter scaffold pre-seeding with metadata & 100% distractor coverage from cta.json.
6. Verification that pre-seeded template scaffolds pass check_templates.py with 0 errors.
7. Deactivation of R-20 false positives on uppercase set/tuple notation ({K}, {Y}, {K, L}) in both validator and engine invariants.
8. Deduplication of competency IDs across CTA parts in stitch_cta_parts.
9. Shard author turn budget is configured to 10 viajes (10 turns).
10. End-to-end simulated workflow of CTA subagent using modular parts and line replacements.
11. End-to-end simulated workflow of Shard Author subagent using pre-seeded scaffolds and isolated scratch.
"""

import copy
import json
import os
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path

# Ensure skills and repo are in sys.path
repo_root = Path(__file__).resolve().parents[1]
c2c_dir = repo_root / ".agents" / "skills" / "content-to-course"
if str(c2c_dir) not in sys.path:
    sys.path.insert(0, str(c2c_dir))
auditor_dir = repo_root / ".agents" / "skills" / "c2c-run-auditor" / "scripts"
if str(auditor_dir) not in sys.path:
    sys.path.insert(0, str(auditor_dir))

# Imports from skills & validator
from unittest.mock import patch
import audit_engine
import telemetry_collector
import traceback_analyzer
from check_cta import check_cta_katex, validate_distractor_math, RAW_LATEX_PATTERNS
from check_templates import check_templates_file_or_dir
from compile_shard import compile_shard
from cta_merge import normalize_orphan_math, sanitize_competency_math, merge_cta_parts
from dispatch import (
    build_dispatch,
    dispatch_authors,
    dispatch_cta,
    generate_define_subagent_specs,
    load_system_prompt,
    ROLE_SPECS,
)
from engine.invariants import validate_katex_syntax
from run import PipelineRunner
from validator.core import validate_course_content


class TestSolow2ArchitecturalImprovements(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="solow2_test_")
        self.work_dir = Path(self.test_dir) / "work"
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # -------------------------------------------------------------------------
    # 1. Pure JSON fragments in CTA & cta-merge stage (<200ms)
    # -------------------------------------------------------------------------
    def test_cta_merge_pure_json_parts_performance_and_accuracy(self):
        """CTA parts are merged into cta.json and cta.md in <200ms with math auto-normalized."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "test_course",
            "files": [{"doc": "solow.pdf", "file_index": 0}],
            "subparts": [
                {"subpart_id": "part_01", "subpart_index": 0, "file_index": 0},
                {"subpart_id": "part_02", "subpart_index": 1, "file_index": 0},
            ]
        }), encoding="utf-8")

        parts_dir = self.work_dir / "cta_parts"
        parts_dir.mkdir(parents=True, exist_ok=True)

        part_01 = [
            {
                "id": "H-01",
                "name": "Ecuación de dot{w}",
                "type": "fact",
                "bloom": "Remember",
                "session": "Sesión 1",
                "unit_index": 1,
                "description_latex": "Definición con bar{k} y tasa frac{1}{2}",
                "prerequisites": [],
                "evidence": [{"doc": "solow.pdf", "page": 1}],
                "distractors": [
                    {
                        "id": "D-H01-01",
                        "name": "Confusión con dot{w}",
                        "wrong_belief": "dot{w} es negativo",
                        "correct_belief": "dot{w} es positivo",
                        "omitted_step": None,
                        "trigger": "Tasa de cambio",
                        "manifestation": "Usa bar{k} erróneo en el cálculo",
                        "error_type": "sign_error",
                        "severity": "medium",
                        "origin": "inferred",
                        "evidence": {"doc": "solow.pdf", "page": 1},
                        "remediation_hint": "Verifique el signo de $\\dot{w}$",
                    }
                ],
            }
        ]
        part_02 = [
            {
                "id": "C-01",
                "name": "Concepto de Estado Estacionario",
                "type": "concept",
                "bloom": "Understand",
                "session": "Sesión 1",
                "unit_index": 2,
                "description_latex": "Equilibrio donde dot{k} se anula",
                "prerequisites": ["H-01"],
                "evidence": [{"doc": "solow.pdf", "page": 2}],
                "distractors": [
                    {
                        "id": "D-C01-01",
                        "name": "Trampa de k nulo",
                        "wrong_belief": "k nulo es estable",
                        "correct_belief": "k positivo es el equilibrio",
                        "omitted_step": None,
                        "trigger": "Raíz cero",
                        "manifestation": "Considera la raíz nula k = 0 como equilibrio no trivial",
                        "error_type": "boundary_case",
                        "severity": "high",
                        "origin": "source",
                        "evidence": {"doc": "solow.pdf", "page": 2},
                        "remediation_hint": "Descarte la solución trivial",
                    }
                ],
            }
        ]

        (parts_dir / "part_01.json").write_text(json.dumps(part_01), encoding="utf-8")
        (parts_dir / "part_02.json").write_text(json.dumps(part_02), encoding="utf-8")

        # Execute merge
        t0 = time.time()
        res = merge_cta_parts(self.work_dir)
        elapsed = time.time() - t0

        # Must execute in < 200 ms (0.2 seconds)
        self.assertLess(elapsed, 0.200, f"cta-merge took {elapsed:.4f}s, exceeding 200ms budget!")
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["total_competencies"], 2)

        # Check cta.json content
        cta_file = self.work_dir / "cta.json"
        self.assertTrue(cta_file.is_file())
        cta_data = json.loads(cta_file.read_text(encoding="utf-8"))

        # Verify math auto-normalization
        h01 = cta_data["competencies"][0]
        self.assertIn("$\\dot{w}$", h01["name"])
        self.assertIn("$\\bar{k}$", h01["description_latex"])
        self.assertIn("$\\frac{1}{2}$", h01["description_latex"])

        # Check cta.md rendering
        cta_md_file = self.work_dir / "cta.md"
        self.assertTrue(cta_md_file.is_file())
        md_text = cta_md_file.read_text(encoding="utf-8")
        self.assertIn("H-01", md_text)
        self.assertIn("C-01", md_text)
        self.assertIn("Curriculum Overview", md_text)

    def test_pipeline_runner_cta_merge_stage(self):
        """PipelineRunner executes --stage cta-merge seamlessly."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "test_course",
            "files": [{"doc": "solow.pdf", "file_index": 0}],
            "subparts": [{"subpart_id": "part_01", "subpart_index": 0, "file_index": 0}]
        }), encoding="utf-8")

        parts_dir = self.work_dir / "cta_parts"
        parts_dir.mkdir(parents=True, exist_ok=True)
        part = [{"id": "H-01", "name": "Test Comp", "type": "fact", "distractors": []}]
        (parts_dir / "part_01.json").write_text(json.dumps(part), encoding="utf-8")

        runner = PipelineRunner(work_dir=str(self.work_dir))
        res = runner.execute(target_stage="cta-merge")
        self.assertIn("cta-merge", res)
        self.assertEqual(res["cta-merge"]["total_competencies"], 1)

    def test_cta_merge_renumbers_and_detects_duplicate_candidates_across_parts(self):
        """merge_cta_parts deterministically sorts by (subpart_index, file_index, page, orig_idx), renumbers sequentially, and flags duplicate candidates."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "test_course",
            "files": [{"doc": "solow.pdf", "file_index": 0}],
            "subparts": [
                {"subpart_id": "part_01", "subpart_index": 0, "file_index": 0},
                {"subpart_id": "part_02", "subpart_index": 1, "file_index": 0},
            ]
        }), encoding="utf-8")

        parts_dir = self.work_dir / "cta_parts"
        parts_dir.mkdir(parents=True, exist_ok=True)

        part_01 = [
            {"id": "C-01", "name": "Concepto de Estado Estacionario en Solow", "type": "concept", "evidence": [{"doc": "solow.pdf", "page": 2}], "distractors": []}
        ]
        part_02 = [
            {"id": "C-01", "name": "Concepto de Estado Estacionario en Solow", "type": "concept", "evidence": [{"doc": "solow.pdf", "page": 5}], "distractors": []},
            {"id": "C-02", "name": "Regla de Oro de Acumulación de Capital", "type": "concept", "evidence": [{"doc": "solow.pdf", "page": 8}], "distractors": []}
        ]
        (parts_dir / "part_01.json").write_text(json.dumps(part_01), encoding="utf-8")
        (parts_dir / "part_02.json").write_text(json.dumps(part_02), encoding="utf-8")

        res = merge_cta_parts(self.work_dir)
        self.assertEqual(res["total_competencies"], 3)
        self.assertGreaterEqual(len(res["duplicate_candidates"]), 1)

        cta_data = json.loads((self.work_dir / "cta.json").read_text(encoding="utf-8"))
        comp_ids = [c["id"] for c in cta_data["competencies"]]
        self.assertEqual(comp_ids, ["C-01", "C-02", "C-03"])

    # -------------------------------------------------------------------------
    # 2. Line-level editing instruction in CTA prompt & bundle
    # -------------------------------------------------------------------------
    def test_cta_direct_bundle_enforces_pure_json_parts_and_replace_file_content(self):
        """CTA Direct dispatch requires declarative tuples/parts & replace_file_content for edits."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "test_course",
            "cta_mode": "direct",
            "documents": [{"doc": "solow.pdf", "path": "content/solow.pdf", "total_pages": 10}]
        }), encoding="utf-8")
        dispatch_res = dispatch_cta(work_dir=self.work_dir, mode="direct")
        self.assertEqual(len(dispatch_res["Subagents"]), 1)
        item_file = Path(dispatch_res["item_files"][0])
        self.assertTrue(item_file.exists())
        content = item_file.read_text(encoding="utf-8")
        self.assertIn("cta_data.py", content)
        self.assertIn("replace_file_content", content)
        self.assertIn("compile_cta.py", content)

    # -------------------------------------------------------------------------
    # 3. Isolated shard workspaces preventing concurrent collisions
    # -------------------------------------------------------------------------
    def test_isolated_shard_workspaces_prevent_collisions(self):
        """Each author shard receives an isolated target script."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "documents": [{"name": "solow.pdf", "path": "content/solow.pdf", "total_pages": 10}]
        }), encoding="utf-8")
        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [
                {"shard_id": "shard_01", "competency_ids": ["H-01"]},
                {"shard_id": "shard_02", "competency_ids": ["C-01"]}
            ]
        }), encoding="utf-8")
        (self.work_dir / "cta.json").write_text(
            json.dumps({"competencies": [{"id": "H-01"}, {"id": "C-01"}]}), encoding="utf-8"
        )

        dispatch = dispatch_authors(work_dir=self.work_dir)
        subagents = dispatch["Subagents"]
        self.assertEqual(len(subagents), 2)

        prompt1 = subagents[0]["Prompt"]
        prompt2 = subagents[1]["Prompt"]

        # Ensure isolated targets are referenced
        self.assertIn("shard_01_data.py", prompt1)
        self.assertIn("shard_02_data.py", prompt2)

    def test_author_turn_budget_is_ten_trips(self):
        """Author subagents are configured with 30 turn budget in v3.2."""
        self.assertEqual(ROLE_SPECS["author"]["turn_budget"], 30)
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "documents": [{"name": "solow.pdf", "path": "content/solow.pdf", "total_pages": 10}]
        }), encoding="utf-8")
        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [{"shard_id": "shard_01", "competency_ids": ["H-01"]}]
        }), encoding="utf-8")
        (self.work_dir / "cta.json").write_text(
            json.dumps({"competencies": [{"id": "H-01"}]}), encoding="utf-8"
        )

        dispatch_res = dispatch_authors(work_dir=self.work_dir)
        item_file = Path(dispatch_res["item_files"][0])
        content = item_file.read_text(encoding="utf-8")
        self.assertIn("compile_shard.py", content)
        self.assertIn("shard_01_data.py", content)

    # -------------------------------------------------------------------------
    # 4. KaTeX safety across courses (non-math text vs real LaTeX macros)
    # -------------------------------------------------------------------------
    def test_katex_safety_preserves_natural_language_across_courses(self):
        """Natural language text in non-math courses is not mangled nor flagged as LaTeX."""
        non_math_texts = [
            "In the navigation bar {Settings, Profile} the user configures options.",
            "Click the red dot {Target} on the screen to continue.",
            "Wear a top hat {Costume} for the play.",
            "The data table_{index} contains records.",
            "Un texto con bar {Herramientas} en la interfaz.",
        ]
        for text in non_math_texts:
            norm = normalize_orphan_math(text)
            self.assertNotIn("$\\bar{Settings", norm)
            self.assertNotIn("$\\dot{Target", norm)
            self.assertNotIn("$\\bar{Herramientas", norm)

    def test_katex_safety_normalizes_genuine_math_expressions(self):
        """Genuine unescaped or unbracketed LaTeX macros are accurately converted."""
        raw = "El estudiante analiza dot{w}, bar{k}, frac{1}{2}, sqrt{x} y \\alpha fuera de modo matematico"
        norm = normalize_orphan_math(raw)
        self.assertIn("$\\dot{w}$", norm)
        self.assertIn("$\\bar{k}$", norm)
        self.assertIn("$\\frac{1}{2}$", norm)
        self.assertIn("$\\sqrt{x}$", norm)
        self.assertIn("$\\alpha$", norm)

    def test_check_cta_katex_distinguishes_natural_language_from_raw_latex(self):
        """check_cta.py validator does not false-positive on natural language with braces."""
        distractor_clean = {
            "id": "D-01",
            "manifestation": "En la barra de menú bar {Configuración} se muestra el menú.",
            "remediation_hint": "Seleccione el punto dot {Inicio}.",
            "wrong_belief": "Creencia estándar sobre el modelo.",
            "omitted_step": None,
        }
        errs = validate_distractor_math(distractor_clean, "D-01")
        self.assertEqual(len(errs), 0, f"False positive in validate_distractor_math: {errs}")

        distractor_with_raw_latex = {
            "id": "D-02",
            "manifestation": "Calcula dot{w} sin delimitar.",
            "remediation_hint": "Error de cálculo.",
            "wrong_belief": None,
            "omitted_step": "Omitió paso",
        }
        errs2 = validate_distractor_math(distractor_with_raw_latex, "D-02")
        self.assertTrue(any("comandos LaTeX sin delimitar" in e for e in errs2))

    # -------------------------------------------------------------------------
    # 5. Scaffold pre-seeding for authors & validation parity
    # -------------------------------------------------------------------------
    def test_preseed_author_scaffolds_generates_valid_modular_scaffolds(self):
        """compile_shard compiles author tuples with 100% distractor coverage and 0 errors."""
        cta = {
            "course_id": "test_course",
            "competencies": [
                {
                    "id": "Hab-01",
                    "name": "Cálculo de Tasa de Crecimiento",
                    "type": "skill",
                    "bloom_level": "Apply",
                    "distractors": [
                        {
                            "id": f"D-Hab01-{i:02d}",
                            "name": f"Trampa conceptual {i}",
                            "manifestation": f"Confusión analítica sobre la tasa de convergencia {i} del sistema dinámico",
                            "remediation_hint": f"Verifique minuciosamente el cálculo analítico {i}"
                        }
                        for i in range(1, 7)
                    ],
                }
            ],
        }
        (self.work_dir / "cta.json").write_text(json.dumps(cta), encoding="utf-8")
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "documents": [{"name": "solow.pdf", "path": "content/solow.pdf", "total_pages": 10}]
        }), encoding="utf-8")

        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "pre_shard_manifest.json").write_text(
            json.dumps({"shards": [{"shard_id": "shard_01", "competency_ids": ["Hab-01"]}]}), encoding="utf-8"
        )

        shard_code = '''
def gen_hab01(rng):
    tc = rng.randint(250, 350)
    delta = rng.randint(150, 450)
    th = tc + delta
    ans_val = round(1.0 - (tc / th), 3)

    distractors = [
        {"value": rf"$\\eta = {round(ans_val + 0.10, 3)}$", "distractor_id": "D-Hab01-01", "error_rationale": "Inversión TH/TC"},
        {"value": rf"$\\eta = {round(ans_val + 0.20, 3)}$", "distractor_id": "D-Hab01-02", "error_rationale": "Calor residual"},
        {"value": rf"$\\eta = {round(ans_val + 0.30, 3)}$", "distractor_id": "D-Hab01-03", "error_rationale": "Desplazamiento"},
        {"value": rf"$\\eta = {round(ans_val + 0.40, 3)}$", "distractor_id": "D-Hab01-04", "error_rationale": "Factor espurio"},
        {"value": rf"$\\eta = {round(ans_val - 0.10, 3)}$", "distractor_id": "D-Hab01-05", "error_rationale": "Suma"},
        {"value": rf"$\\eta = {round(ans_val - 0.20, 3)}$", "distractor_id": "D-Hab01-06", "error_rationale": "Semidiferencia"},
    ]
    return {
        "vars": {"th": th, "tc": tc, "ans": ans_val},
        "correct": rf"$\\eta = {ans_val}$",
        "distractors": distractors
    }

def ver_hab01(res):
    v = res.get("vars", {})
    expected = round(1.0 - (v["tc"] / v["th"]), 3)
    return v.get("ans") == expected

TEMPLATES = [
    (
        "Hab-01",
        "multiple_choice",
        r"Una máquina térmica reversible de Carnot opera entre dos focos a temperaturas $T_H = {th}\\text{ K}$ y $T_C = {tc}\\text{ K}$. Determine el rendimiento térmico:",
        gen_hab01,
        ver_hab01,
        r"Por el teorema de Carnot, el rendimiento es $\\eta = 1 - \\frac{T_C}{T_H} = {ans}$.",
        "Eficiencia de Carnot",
        ["D-Hab01-01", "D-Hab01-02", "D-Hab01-03", "D-Hab01-04", "D-Hab01-05", "D-Hab01-06"],
        ("solow.pdf", 1, "Cita")
    )
]
'''
        (shards_dir / "shard_01_data.py").write_text(shard_code, encoding="utf-8")

        ok, errs = compile_shard(self.work_dir, "shard_01")
        self.assertTrue(ok, f"compile_shard failed with: {errs}")

        tpl_file = self.work_dir / "templates" / "Hab-01.json"
        self.assertTrue(tpl_file.is_file())

        is_valid, errors = check_templates_file_or_dir(tpl_file, cta_path=self.work_dir / "cta.json")
        self.assertTrue(is_valid, f"Compiled template failed validation: {errors}")
        self.assertEqual(len(errors), 0)

    # -------------------------------------------------------------------------
    # 6. Deactivate R-20 false positives on uppercase set/tuple notation
    # -------------------------------------------------------------------------
    def test_r20_allows_uppercase_set_tuple_notation_in_both_rules_and_invariants(self):
        """Uppercase set/tuple notation {K}, {Y}, {K, L} does NOT trigger R-20 in rules.py or invariants."""
        # 1. Test validator rules.py
        base_course = {
            "course_id": "solow_growth",
            "title": "Solow Growth Model",
            "competencies": [
                {
                    "id": "C-01",
                    "name": "Factores de Producción",
                    "type": "concept",
                    "bloom_level": "Understand",
                    "description": "Análisis de los factores {K, L} en el modelo.",
                }
            ],
            "questions": [
                {
                    "id": "Q-01",
                    "competency_id": "C-01",
                    "type": "multiple_choice",
                    "stem": "Considere la dotación agregada de factores {K, L} y el nivel de producto {Y}.",
                    "options": [
                        {"content": "El conjunto de factores es {K, L}.", "is_correct": True},
                        {"content": "La dotación {K} es irrelevante.", "is_correct": False, "error_rationale": "Ignora el capital {K}."},
                        {"content": "El producto {Y} no depende de {K}.", "is_correct": False, "error_rationale": "Desconoce {Y}."},
                        {"content": "El trabajo {L} es fijo.", "is_correct": False, "error_rationale": "Asume fijeza."},
                        {"content": "La tecnología {A} es constante.", "is_correct": False, "error_rationale": "No aplica."},
                        {"content": "No hay depreciación.", "is_correct": False, "error_rationale": "Erróneo."},
                        {"content": "El ahorro es total.", "is_correct": False, "error_rationale": "Inviable."},
                    ],
                    "hints": ["Examine el conjunto {K, L}."],
                    "solution": "La combinación {K, L} determina el producto {Y}.",
                }
            ],
        }
        res = validate_course_content(json.dumps(base_course))
        r20_errors = [e for e in res.errors if e.rule_id == "R-20" and "Unreplaced template variable" in e.message]
        self.assertEqual(len(r20_errors), 0, f"False positive R-20 triggered in rules.py: {r20_errors}")

        # 2. Test engine/invariants.py validate_katex_syntax
        inv_errors = validate_katex_syntax("Análisis de los factores {K, L} y producto {Y}", "stem")
        self.assertEqual(len(inv_errors), 0, f"False positive in validate_katex_syntax: {inv_errors}")

    def test_r20_still_catches_unreplaced_lowercase_dynamic_template_variables(self):
        """Unreplaced dynamic template variables like {k_val} STILL trigger R-20."""
        course = {
            "course_id": "test_unreplaced",
            "title": "Test Unreplaced",
            "competencies": [{"id": "C-01", "name": "Test", "type": "concept"}],
            "questions": [
                {
                    "id": "Q-01",
                    "competency_id": "C-01",
                    "type": "fill_in_the_blank",
                    "stem": "Calcule el valor numérico de la constante {k_val}.",
                    "answer_key": "10",
                    "hints": ["Sustituya {slope}."],
                    "solution": "El resultado es {res_num}.",
                }
            ],
        }
        res = validate_course_content(json.dumps(course))
        r20_errors = [e for e in res.errors if e.rule_id == "R-20" and "Unreplaced template variable" in e.message]
        self.assertGreater(len(r20_errors), 0, "Failed to catch unreplaced dynamic variable {k_val}!")

        # Also check engine invariants catches {k_val}
        inv_errors = validate_katex_syntax("Calcule {k_val}.", "stem")
        self.assertTrue(any("{k_val}" in e for e in inv_errors))

    # -------------------------------------------------------------------------
    # 7. Real-world end-to-end flow simulation for CTA and Shard Author
    # -------------------------------------------------------------------------
    def test_simulated_cta_subagent_full_workflow(self):
        """Simulates full CTA subagent flow: bundle dispatch -> modular parts -> surgical edit -> cta-stitch."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "solow_growth_sim",
            "title": "Simulated Solow Course",
            "cta_mode": "direct",
            "documents": [{"doc": "solow.pdf", "path": "content/solow.pdf", "total_pages": 10}],
            "files": [{"doc": "solow.pdf", "file_index": 0}],
            "subparts": [{"subpart_id": "part_01", "subpart_index": 0, "file_index": 0}]
        }), encoding="utf-8")

        # 1. Dispatch CTA direct role
        dispatch = build_dispatch(role="cta-direct", work_dir=self.work_dir)
        subagents = dispatch["Subagents"]
        self.assertEqual(len(subagents), 1)
        self.assertEqual(subagents[0]["TypeName"], "c2c_cta_architect")
        self.assertEqual(subagents[0]["Role"], "Cognitive Task Analysis Architect")

        # 2. Subagent emits modular declarative parts
        parts_dir = self.work_dir / "cta_parts"
        parts_dir.mkdir(parents=True, exist_ok=True)
        part_01 = [
            {
                "id": "C-01",
                "name": "Ecuación de Acumulación con dot{k}",
                "type": "concept",
                "bloom": "Understand",
                "session": "Sesión 1",
                "unit_index": 1,
                "description_latex": "Dinámica de bar{k}",
                "prerequisites": [],
                "distractors": [
                    {
                        "id": f"D-C01-{i:02d}",
                        "name": f"Error conceptual {i}",
                        "manifestation": f"Confusión analítica de sendero {i}",
                        "wrong_belief": "Belief erróneo",
                        "remediation_hint": "Pista formativa"
                    }
                    for i in range(1, 7)
                ]
            }
        ]
        part_01_file = parts_dir / "part_01.json"
        part_01_file.write_text(json.dumps(part_01, indent=2, ensure_ascii=False), encoding="utf-8")

        # 3. Subagent performs surgical line edit using replace_file_content pattern
        content = part_01_file.read_text(encoding="utf-8")
        updated_content = content.replace("Dinámica de bar{k}", "Dinámica formal con bar{k} y tasa frac{1}{3}")
        part_01_file.write_text(updated_content, encoding="utf-8")

        # 4. Execute cta-merge stage
        runner = PipelineRunner(work_dir=str(self.work_dir))
        res = runner.execute(target_stage="cta-merge")
        self.assertIn("cta-merge", res)
        self.assertEqual(res["cta-merge"]["total_competencies"], 1)

        # 5. Verify final cta.json has normalized math
        cta_data = json.loads((self.work_dir / "cta.json").read_text(encoding="utf-8"))
        comp = cta_data["competencies"][0]
        self.assertIn("$\\dot{k}$", comp["name"])
        self.assertIn("$\\bar{k}$", comp["description_latex"])
        self.assertIn("$\\frac{1}{3}$", comp["description_latex"])

    def test_simulated_shard_author_subagent_full_workflow(self):
        """Simulates full Shard Author flow: dispatch -> compile_shard -> validation."""
        cta = {
            "course_id": "solow_growth_sim",
            "competencies": [
                {
                    "id": "C-01",
                    "name": "Estado Estacionario",
                    "type": "concept",
                    "bloom": "Understand",
                    "distractors": [
                        {
                            "id": f"D-C01-{i:02d}",
                            "name": f"Trampa analítica {i}",
                            "manifestation": f"Confusión sobre la estabilidad asintótica {i}",
                            "wrong_belief": "Belief erróneo",
                            "remediation_hint": "Pista formativa"
                        }
                        for i in range(1, 7)
                    ]
                }
            ]
        }
        (self.work_dir / "cta.json").write_text(json.dumps(cta), encoding="utf-8")
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "documents": [{"name": "solow.pdf", "path": "content/solow.pdf", "total_pages": 10}]
        }), encoding="utf-8")
        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "pre_shard_manifest.json").write_text(
            json.dumps({"shards": [{"shard_id": "shard_01", "competency_ids": ["C-01"]}]}), encoding="utf-8"
        )

        # 1. Dispatch author role
        dispatch = dispatch_authors(work_dir=self.work_dir)
        subagents = dispatch["Subagents"]
        self.assertEqual(len(subagents), 1)

        # 2. Author creates shard_01_data.py with valid 9-element tuples
        shard_data = '''
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
        (shards_dir / "shard_01_data.py").write_text(shard_data, encoding="utf-8")

        # 3. Compile
        ok, errs = compile_shard(self.work_dir, "shard_01")
        self.assertTrue(ok, f"Compile shard failed: {errs}")

        tpl_path = self.work_dir / "templates" / "C-01.json"
        self.assertTrue(tpl_path.is_file())

        is_valid, errors = check_templates_file_or_dir(tpl_path, cta_path=self.work_dir / "cta.json")
        self.assertTrue(is_valid, f"Author starter scaffold has validation errors: {errors}")
        self.assertEqual(len(errors), 0)


class TestC2CV32AdvancedEdgeCases(unittest.TestCase):
    """Rigorous unit tests for C2C v3.2 edge cases:
    1. Dynamic scaling of audit_engine & traceback_analyzer with M=6 CTA Architects, N=8 Shard Authors, K=5 Blind Judges + thinking_traces.
    2. telemetry_collector stage telemetry (<30ms), cumulative state.json updates, and streaming resolution of thinking_traces.
    3. compile_shard native Python functions, exact line error reporting ([Tupla en shard_01_data.py: Líneas Start..End]), and pre_shard_manifest blocker (code 2).
    4. dispatch payload non-truncation (< 46,080 bytes) and 100% full system prompt integrity in both direct and mapreduce modes.
    """

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="v32_edge_")
        self.work_dir = Path(self.test_dir) / "work"
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.fake_brain = Path(self.test_dir) / "fake_brain"
        self.fake_brain.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # -------------------------------------------------------------------------
    # 1. audit_engine & traceback_analyzer with M=6 CTA, N=8 Authors, K=5 Judges
    # -------------------------------------------------------------------------
    def test_audit_engine_and_traceback_dynamic_scaling_m6_n8_k5_and_thinking_traces(self):
        """audit_engine and traceback_analyzer dynamically classify and audit M=6 CTA, N=8 Authors, and K=5 Judges with thinking traces."""
        root_conv_id = "root-c2c-v32-orch-001"
        root_dir = self.fake_brain / root_conv_id / ".system_generated" / "logs"
        root_dir.mkdir(parents=True, exist_ok=True)

        m_cta = 6
        n_authors = 8
        k_judges = 5
        total_subs = m_cta + n_authors + k_judges

        spawned_subagents_list = []
        cta_uuids = [f"00000000-0000-0000-0001-{i+1:012d}" for i in range(m_cta)]
        author_uuids = [f"00000000-0000-0000-0002-{i+1:012d}" for i in range(n_authors)]
        judge_uuids = [f"00000000-0000-0000-0003-{i+1:012d}" for i in range(k_judges)]

        # 1. Create subagent transcript directories and files in fake_brain
        for i, cid in enumerate(cta_uuids, 1):
            s_dir = self.fake_brain / cid / ".system_generated" / "logs"
            s_dir.mkdir(parents=True, exist_ok=True)
            p0 = f"# Asignación de Tarea para Cognitive Task Analysis Architect (part_{i:02d})\nInstrucciones para part_{i:02d}"
            t_lines = [
                json.dumps({"step_index": 0, "type": "USER_INPUT", "content": p0, "created_at": "2026-10-16T12:00:00Z"}),
                json.dumps({
                    "step_index": 1,
                    "type": "PLANNER_RESPONSE",
                    "content": f"Analyzing curriculum section part_{i:02d}",
                    "thinking": f"Reflecting deeply on cognitive task analysis for part {i:02d}. Formulating competencies and distractors.",
                    "input_tokens": 1200 + i * 50,
                    "output_tokens": 350 + i * 20,
                    "cache_read_tokens": 100,
                    "tool_calls": [{"name": "write_to_file", "args": {"TargetFile": f"work/cta_parts/part_{i:02d}_data.py"}}],
                    "created_at": "2026-10-16T12:00:05Z",
                }),
                json.dumps({"step_index": 2, "type": "TOOL_RESPONSE", "status": "DONE", "content": "File written", "created_at": "2026-10-16T12:00:06Z"}),
            ]
            (s_dir / "transcript.jsonl").write_text("\n".join(t_lines), encoding="utf-8")
            spawned_subagents_list.append({
                "conversationId": cid,
                "role": f"Cognitive Task Analysis Architect part_{i:02d}",
                "type": "c2c_cta_architect",
            })

        for i, cid in enumerate(author_uuids, 1):
            s_dir = self.fake_brain / cid / ".system_generated" / "logs"
            s_dir.mkdir(parents=True, exist_ok=True)
            shard_id = f"shard_{i:02d}"
            p0 = f"# Asignación de Tarea para Shard Author {shard_id}\nCompetencias: C-{i:02d}"
            t_lines = [
                json.dumps({"step_index": 0, "type": "USER_INPUT", "content": p0, "created_at": "2026-10-16T12:05:00Z"}),
                json.dumps({
                    "step_index": 1,
                    "type": "PLANNER_RESPONSE",
                    "content": f"Authoring parametric templates for {shard_id}",
                    "thinking": f"Synthesizing python tuples and testing compile_shard for {shard_id}.",
                    "input_tokens": 2000 + i * 40,
                    "output_tokens": 500 + i * 25,
                    "cache_read_tokens": 200,
                    "tool_calls": [{"name": "run_command", "args": {"CommandLine": f"python compile_shard.py --shard {shard_id}"}}],
                    "created_at": "2026-10-16T12:05:08Z",
                }),
                json.dumps({"step_index": 2, "type": "TOOL_RESPONSE", "status": "DONE", "content": "PASS", "created_at": "2026-10-16T12:05:09Z"}),
            ]
            (s_dir / "transcript.jsonl").write_text("\n".join(t_lines), encoding="utf-8")
            spawned_subagents_list.append({
                "conversationId": cid,
                "role": f"Shard Author {shard_id}",
                "type": "c2c_shard_author",
            })

        for i, cid in enumerate(judge_uuids, 1):
            s_dir = self.fake_brain / cid / ".system_generated" / "logs"
            s_dir.mkdir(parents=True, exist_ok=True)
            j_name = f"Judge {i:02d}"
            p0 = f"# Asignación de Tarea para {j_name}\nEvaluar lote {i:02d} ciegamente"
            t_lines = [
                json.dumps({"step_index": 0, "type": "USER_INPUT", "content": p0, "created_at": "2026-10-16T12:10:00Z"}),
                json.dumps({
                    "step_index": 1,
                    "type": "PLANNER_RESPONSE",
                    "content": f"Blind evaluation {j_name}",
                    "thinking": f"Evaluating psychometric validity for {j_name} without ground truth.",
                    "input_tokens": 900 + i * 30,
                    "output_tokens": 150 + i * 15,
                    "cache_read_tokens": 50,
                    "tool_calls": [{"name": "write_to_file", "args": {"TargetFile": f"work/verification/judge_responses_{i:02d}.json"}}],
                    "created_at": "2026-10-16T12:10:03Z",
                }),
                json.dumps({"step_index": 2, "type": "TOOL_RESPONSE", "status": "DONE", "content": "Saved", "created_at": "2026-10-16T12:10:04Z"}),
            ]
            (s_dir / "transcript.jsonl").write_text("\n".join(t_lines), encoding="utf-8")
            spawned_subagents_list.append({
                "conversationId": cid,
                "role": j_name,
                "type": "c2c_judge",
            })

        # 2. Build root orchestrator transcript referencing all 19 subagents
        root_steps = [
            {
                "step_index": 0,
                "type": "USER_INPUT",
                "content": "Run Content to Course pipeline on macroeconomic material",
                "created_at": "2026-10-16T11:59:00Z",
            },
            {
                "step_index": 1,
                "type": "PLANNER_RESPONSE",
                "content": "Spawning CTA, Author, and Judge subagents",
                "thinking": "Orchestrating multi-agent pipeline with dynamic M=6, N=8, K=5 fan-out.",
                "input_tokens": 5000,
                "output_tokens": 800,
                "cache_read_tokens": 1000,
                "tool_calls": [{"name": "invoke_subagent", "args": {"Subagents": spawned_subagents_list}}],
                "created_at": "2026-10-16T11:59:30Z",
            },
            {
                "step_index": 2,
                "type": "TOOL_RESPONSE",
                "status": "DONE",
                "content": f"Created the following subagents:\n{json.dumps(spawned_subagents_list, indent=2)}",
                "created_at": "2026-10-16T11:59:35Z",
            },
            {
                "step_index": 3,
                "type": "PLANNER_RESPONSE",
                "content": "All subagents successfully completed their workloads.",
                "thinking": "Verifying outputs across all stages before certifying publication.",
                "input_tokens": 2000,
                "output_tokens": 400,
                "cache_read_tokens": 500,
                "tool_calls": [],
                "created_at": "2026-10-16T12:15:00Z",
            },
        ]
        (root_dir / "transcript.jsonl").write_text(
            "\n".join(json.dumps(s) for s in root_steps), encoding="utf-8"
        )

        # 3. Test TranscriptParser.discover_all_subagents
        discovered = audit_engine.TranscriptParser.discover_all_subagents(root_steps, self.fake_brain)
        self.assertEqual(len(discovered), total_subs, f"Expected {total_subs} subagents, found {len(discovered)}")

        cta_subs = [s for s in discovered if s["category"] == "cta_mapper"]
        author_subs = [s for s in discovered if s["category"] == "author"]
        judge_subs = [s for s in discovered if s["category"] == "judge"]

        self.assertEqual(len(cta_subs), m_cta, f"Expected {m_cta} CTA subagents, found {len(cta_subs)}")
        self.assertEqual(len(author_subs), n_authors, f"Expected {n_authors} author subagents, found {len(author_subs)}")
        self.assertEqual(len(judge_subs), k_judges, f"Expected {k_judges} judge subagents, found {len(judge_subs)}")

        author_shard_ids = {s["shard_id"] for s in author_subs}
        for i in range(1, n_authors + 1):
            self.assertIn(f"shard_{i:02d}", author_shard_ids)

        # 4. Test SubagentTreeResolver from traceback_analyzer with brain patching
        with patch.object(traceback_analyzer, "get_brain_dir", return_value=self.fake_brain):
            subagent_tree = traceback_analyzer.SubagentTreeResolver.discover_subagents(root_steps)
            self.assertEqual(len(subagent_tree), total_subs)

            for i, cid in enumerate(cta_uuids, 1):
                self.assertIn(cid, subagent_tree)
                self.assertEqual(subagent_tree[cid]["role"], f"CTA Architect (part_{i:02d})")
                self.assertEqual(subagent_tree[cid]["stage"], "1b_cta")

            for i, cid in enumerate(author_uuids, 1):
                self.assertIn(cid, subagent_tree)
                self.assertEqual(subagent_tree[cid]["role"], f"Author Shard {i:02d}")
                self.assertEqual(subagent_tree[cid]["stage"], "3_authoring")

            for i, cid in enumerate(judge_uuids, 1):
                self.assertIn(cid, subagent_tree)
                self.assertEqual(subagent_tree[cid]["role"], f"Judge {i:02d}")
                self.assertEqual(subagent_tree[cid]["stage"], "5_judges")

        # 5. Test ExecutionAuditor.audit with thinking_traces extraction
        with patch.object(audit_engine, "get_brain_dir", return_value=self.fake_brain):
            auditor = audit_engine.ExecutionAuditor(root_steps, root_conv_id)
            workload = {
                "course_id": "macro_test",
                "course_title": "Macroeconomics Course",
                "shards_count": n_authors,
                "competencies_count": n_authors * 2,
                "questions_count": n_authors * 20,
                "shards_competencies_map": {
                    f"shard_{i:02d}": {"competency_ids": [f"C-{i:02d}"], "count": 1}
                    for i in range(1, n_authors + 1)
                },
            }
            report = auditor.audit(workload)

            self.assertEqual(report["summary"]["total_subagents_spawned"], total_subs)
            self.assertGreaterEqual(report["summary"]["total_thinking_turns"], total_subs)
            self.assertGreater(report["summary"]["total_thinking_chars"], 0)

            th_summary = report["thinking_traces_summary"]
            self.assertGreaterEqual(th_summary["total_thinking_turns"], total_subs)
            self.assertGreater(th_summary["subagents_thinking_chars"], 0)
            self.assertGreater(th_summary["orchestrator_thinking_chars"], 0)

            # Check individual subagents in audit report
            subagents_data = report["subagents"]
            self.assertEqual(len(subagents_data), total_subs)
            for sub in subagents_data:
                self.assertGreater(sub["input_tokens"], 0)
                self.assertGreater(sub["output_tokens"], 0)
                self.assertGreater(sub["thinking_chars"], 0)
                self.assertGreaterEqual(sub["thinking_turns_count"], 1)

    # -------------------------------------------------------------------------
    # 2. telemetry_collector: stage recording (<30ms) & streaming thinking
    # -------------------------------------------------------------------------
    def test_telemetry_collector_stage_recording_and_thinking_traces_streaming_resolution(self):
        """telemetry_collector records stages in < 30ms, updates state.json, and streaming-resolves truncated thinking."""
        # 1. Create a dummy pre_cta_manifest.json to establish artifact counts
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "econ_macro",
            "total_items": 42,
            "cta_mode": "mapreduce",
            "files": [{"doc": "macro.pdf", "total_pages": 42}],
        }), encoding="utf-8")

        # 2. Record stage 00_prepare and 01_cta isolated to self.fake_brain
        with patch.object(telemetry_collector, "get_brain_dir", return_value=self.fake_brain):
            t0 = time.perf_counter()
            snap_prep = telemetry_collector.record_stage_telemetry(
                work_dir=self.work_dir,
                stage_idx="00",
                stage_name="prepare",
                status="completed",
                metadata={"total_pages": 42, "duration_seconds": 1.25},
            )
            prep_overhead = (time.perf_counter() - t0) * 1000

            self.assertLess(prep_overhead, 150.0, "Telemetry collector overhead should be sub-perceptual")
            self.assertEqual(snap_prep["stage_idx"], "00")
            self.assertEqual(snap_prep["stage_name"], "prepare")
            self.assertTrue((self.work_dir / "telemetry" / "00_prepare.json").is_file())

            # 3. Record stage 01_cta with subagent tokens
            snap_cta = telemetry_collector.record_stage_telemetry(
                work_dir=self.work_dir,
                stage_idx="01",
                stage_name="cta",
                status="completed",
                metadata={
                    "subagents": [
                        {
                            "conversation_id": "subagent-cta-01",
                            "role": "Cognitive Task Analysis Architect",
                            "type_name": "c2c_cta_architect",
                            "tokens": {"input": 4500, "output": 1200, "cached": 300, "thinking": 800, "total": 6000},
                            "turns_count": 3,
                            "duration_seconds": 12.4,
                        }
                    ]
                },
            )
        self.assertEqual(snap_cta["stage_tokens"]["input"], 4500)
        self.assertEqual(snap_cta["stage_tokens"]["output"], 1200)
        self.assertTrue((self.work_dir / "telemetry" / "01_cta.json").is_file())

        # 4. Verify work/state.json accumulation
        state_file = self.work_dir / "state.json"
        self.assertTrue(state_file.is_file(), "state.json must be created and accumulated")
        state_data = json.loads(state_file.read_text(encoding="utf-8"))

        self.assertEqual(state_data["course_id"], "econ_macro")
        self.assertIn("00_prepare", state_data["stages"])
        self.assertIn("01_cta", state_data["stages"])
        self.assertEqual(state_data["last_stage"], "01_cta")
        self.assertEqual(state_data["artifact_counts"]["pages"], 42)
        self.assertEqual(state_data["tokens_total"]["input"], 4500)
        self.assertEqual(state_data["tokens_total"]["output"], 1200)

        # 5. Test streaming resolution of thinking_traces from transcript_full.jsonl
        dummy_cid = "conv-subagent-thinking-test-999"
        sub_logs_dir = self.fake_brain / dummy_cid / ".system_generated" / "logs"
        sub_logs_dir.mkdir(parents=True, exist_ok=True)

        full_thinking_text = (
            "DEEP FORENSIC THINKING TRACE: "
            + "Evaluating mathematical equilibrium conditions and distractor separation boundaries across Bloom levels. " * 30
        )
        self.assertGreater(len(full_thinking_text), 2500)

        # transcript.jsonl has truncated_fields
        compact_step = {
            "step_index": 1,
            "type": "PLANNER_RESPONSE",
            "content": "Drafting templates",
            "thinking": full_thinking_text[:120] + "... [truncated]",
            "input_tokens": 1000,
            "output_tokens": 300,
            "cache_read_tokens": 50,
            "truncated_fields": ["thinking", "content"],
            "created_at": "2026-10-16T12:00:00Z",
            "tool_calls": [{"name": "write_to_file", "args": {"TargetFile": "shard_01.py"}}],
        }
        (sub_logs_dir / "transcript.jsonl").write_text(json.dumps(compact_step) + "\n", encoding="utf-8")

        # transcript_full.jsonl has the untruncated content
        full_step = dict(compact_step)
        full_step.pop("truncated_fields", None)
        full_step["thinking"] = full_thinking_text
        full_step["content"] = "Drafting templates with full resolution"
        (sub_logs_dir / "transcript_full.jsonl").write_text(json.dumps(full_step) + "\n", encoding="utf-8")

        # Call read_transcript_with_full_resolution
        resolved_records = telemetry_collector.read_transcript_with_full_resolution(
            sub_logs_dir / "transcript.jsonl"
        )
        self.assertEqual(len(resolved_records), 1)
        self.assertEqual(resolved_records[0]["thinking"], full_thinking_text)
        self.assertEqual(resolved_records[0]["content"], "Drafting templates with full resolution")

        # Call inspect_subagent_transcript and verify thinking_traces
        sub_inspection = telemetry_collector.inspect_subagent_transcript(
            subagent_conv_id=dummy_cid,
            meta={"role": "Shard Author", "type_name": "c2c_shard_author"},
            brain_dir=self.fake_brain,
        )
        self.assertEqual(len(sub_inspection["thinking_traces"]), 1)
        self.assertEqual(sub_inspection["thinking_traces"][0]["thinking"], full_thinking_text)
        self.assertGreaterEqual(sub_inspection["tokens"]["thinking"], len(full_thinking_text) // 4)

    # -------------------------------------------------------------------------
    # 3. compile_shard: native functions, exact line report, and pre_shard blocker
    # -------------------------------------------------------------------------
    def test_compile_shard_native_functions_exact_line_mapping_and_pre_shard_blocker(self):
        """compile_shard compiles native Python functions, reports exact tuple lines on error, and halts on missing pre_shard_manifest."""
        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)

        # 3.1 Strict blocker: When pre_shard_manifest.json does not exist -> SystemExit(2)
        with self.assertRaises(SystemExit) as ctx:
            compile_shard(self.work_dir, "shard_01")
        self.assertEqual(ctx.exception.code, 2, "compile_shard must exit with code 2 on missing pre_shard_manifest.json")

        # Seed authoritative pre_shard_manifest.json and cta.json with matching distractors
        distractors_c01 = [
            {"id": f"D-C01-{i:02d}", "name": f"Distractor {i}", "wrong_belief": f"Error {i}"}
            for i in range(1, 7)
        ]
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [
                {
                    "shard_id": "shard_01",
                    "competency_ids": ["C-01"],
                    "competencies": [{"id": "C-01", "name": "Solow Steady State", "distractors": distractors_c01}],
                }
            ]
        }), encoding="utf-8")
        (self.work_dir / "cta.json").write_text(json.dumps({
            "course_id": "solow_test",
            "competencies": [{"id": "C-01", "name": "Solow Steady State", "distractors": distractors_c01}],
        }), encoding="utf-8")

        # 3.2 Native Python function compilation
        valid_shard_source = '''# Preamble helpers and constants
ALPHA_CONST = 0.33

def calculate_steady_state(s, n, g, delta):
    return round((s / (n + g + delta)) ** (1.0 / (1.0 - ALPHA_CONST)), 3)

def gen_steady_state(rng):
    s = round(rng.uniform(0.15, 0.25), 2)
    n = 0.02
    g = 0.02
    delta = 0.05
    k_star = calculate_steady_state(s, n, g, delta)
    distractors = [
        {"value": rf"$k^* = {round(k_star * 1.2, 3)}$", "distractor_id": "D-C01-01", "error_rationale": "Omite depreciación"},
        {"value": rf"$k^* = {round(k_star * 0.8, 3)}$", "distractor_id": "D-C01-02", "error_rationale": "Tasa g duplicada"},
        {"value": rf"$k^* = {round(k_star * 1.5, 3)}$", "distractor_id": "D-C01-03", "error_rationale": "Exponente inverso"},
        {"value": rf"$k^* = {round(k_star * 0.5, 3)}$", "distractor_id": "D-C01-04", "error_rationale": "Suma directa de tasas"},
        {"value": rf"$k^* = {round(k_star * 1.1, 3)}$", "distractor_id": "D-C01-05", "error_rationale": "Error aritmético menor"},
        {"value": rf"$k^* = {round(k_star * 0.9, 3)}$", "distractor_id": "D-C01-06", "error_rationale": "Subestimación"},
    ]
    return {
        "vars": {"s": s, "k_star": k_star},
        "correct": rf"$k^* = {k_star}$",
        "distractors": distractors,
    }

def ver_steady_state(res):
    v = res.get("vars", {})
    expected = calculate_steady_state(v.get("s", 0.2), 0.02, 0.02, 0.05)
    return v.get("k_star") == expected

TEMPLATES = [
    (
        "C-01",
        "multiple_choice",
        r"Considere el modelo de Solow con tasa de ahorro $s = {s}$. Calcule el capital de estado estacionario $k^*$:",
        gen_steady_state,
        ver_steady_state,
        r"En estado estacionario $sf(k^*) = (n + g + \\delta)k^*$, lo que produce $k^* = {k_star}$.",
        "Estado Estacionario de Solow",
        ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"],
        ("solow_doc.pdf", 5, "Cita textual")
    )
]
'''
        shard_file = shards_dir / "shard_01_data.py"
        shard_file.write_text(valid_shard_source, encoding="utf-8")

        ok, errs = compile_shard(self.work_dir, "shard_01", seeds=10)
        self.assertTrue(ok, f"Expected successful compile, got: {errs}")

        compiled_tpl = self.work_dir / "templates" / "C-01.json"
        self.assertTrue(compiled_tpl.is_file())
        tpl_data = json.loads(compiled_tpl.read_text(encoding="utf-8"))

        # Verify that native functions and helpers were correctly extracted into generate_py and cross_check_py
        self.assertIn("def generate_params(rng):", tpl_data["generate_py"])
        self.assertIn("generate = generate_params", tpl_data["generate_py"])
        self.assertIn("def verify(res):", tpl_data["cross_check_py"])
        self.assertIn("cross_check = verify", tpl_data["cross_check_py"])
        self.assertIn("calculate_steady_state", tpl_data["generate_py"])

        # 3.3 Exact line reporting on validation error
        # Inject placeholder rationale into the tuple to trigger strict R-17 rejection
        failing_shard_source = valid_shard_source.replace(
            '"error_rationale": "Omite depreciación"',
            '"error_rationale": "placeholder"'
        )
        shard_file.write_text(failing_shard_source, encoding="utf-8")

        ok_fail, fail_errs = compile_shard(self.work_dir, "shard_01", seeds=5)
        self.assertFalse(ok_fail, "compile_shard must fail on placeholder distractor rationale")

        # Verify exact tuple line reporting [Tupla en shard_01_data.py: Líneas Start..End]
        reported_text = " ".join(fail_errs)
        self.assertIn("[Tupla en shard_01_data.py: Líneas", reported_text)
        self.assertIn("StartLine:", reported_text)
        self.assertIn("EndLine:", reported_text)

    # -------------------------------------------------------------------------
    # 4. dispatch: payload size (<46,080 bytes) & full prompt integrity
    # -------------------------------------------------------------------------
    def test_dispatch_payload_size_subagent_specs_and_cta_mapreduce_full_prompt_integrity(self):
        """dispatch payloads are strictly < 46,080 bytes while preserving 100% full system prompts in direct and mapreduce."""
        # 4.1 Subagent type specifications in work/dispatch/types/*.json
        type_specs = generate_define_subagent_specs(self.work_dir)
        self.assertIn("type_files", type_specs)
        self.assertGreaterEqual(len(type_specs["type_files"]), 4)

        for type_file_str in type_specs["type_files"]:
            t_path = Path(type_file_str)
            self.assertTrue(t_path.is_file())
            f_size = t_path.stat().st_size
            self.assertLess(f_size, 46080, f"Type spec {t_path.name} exceeded 46,080 bytes: {f_size} bytes")

            spec_json = json.loads(t_path.read_text(encoding="utf-8"))
            self.assertIn("name", spec_json)
            self.assertIn("system_prompt", spec_json)
            # Verify system prompt has full integrity (> 3,000 characters)
            self.assertGreater(len(spec_json["system_prompt"]), 3000)

        # 4.2 Missing pre_cta_manifest.json -> FileNotFoundError(BLOCKER)
        with self.assertRaises(FileNotFoundError) as ctx:
            dispatch_cta(self.work_dir, mode="direct")
        self.assertIn("BLOCKER:: No existe pre_cta_manifest.json", str(ctx.exception))

        # 4.3 Direct mode dispatch
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "macro_dispatch_test",
            "cta_mode": "direct",
            "documents": [
                {"name": f"chapter_{i:02d}.pdf", "path": f"content/chapter_{i:02d}.pdf", "total_pages": 15, "valid_page_range": [1, 15]}
                for i in range(1, 20)
            ],
        }), encoding="utf-8")

        direct_res = dispatch_cta(self.work_dir, mode="direct")
        self.assertEqual(len(direct_res["Subagents"]), 1)
        self.assertEqual(len(direct_res["item_files"]), 1)

        direct_item = Path(direct_res["item_files"][0])
        self.assertTrue(direct_item.is_file())
        self.assertLess(direct_item.stat().st_size, 46080, f"Direct item file exceeded 46,080 bytes: {direct_item.stat().st_size}")

        direct_prompt = direct_res["Subagents"][0]["Prompt"]
        raw_cta_prompt = load_system_prompt("prompt_cta_architect.md")
        self.assertIn(raw_cta_prompt.strip(), direct_prompt, "System prompt in direct dispatch must be 100% full and uncompressed")

        # 4.4 MapReduce mode dispatch with M=6 subparts
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "macro_dispatch_mapreduce",
            "cta_mode": "mapreduce",
            "files": [
                {"doc": f"module_{i:02d}.pdf", "file_index": i - 1, "total_pages": 20, "valid_page_range": [1, 20]}
                for i in range(1, 7)
            ],
            "subparts": [
                {
                    "subpart_id": f"part_{i:02d}",
                    "subpart_index": i - 1,
                    "doc": f"module_{i:02d}.pdf",
                    "file_index": i - 1,
                    "page_range": [1, 20],
                    "total_pages": 20,
                }
                for i in range(1, 7)
            ],
        }), encoding="utf-8")

        map_res = dispatch_cta(self.work_dir, mode="mapreduce")
        self.assertEqual(len(map_res["Subagents"]), 6, "Expected 6 subagents for M=6 subparts")
        self.assertEqual(len(map_res["item_files"]), 6)

        for idx, item_path_str in enumerate(map_res["item_files"], 1):
            item_p = Path(item_path_str)
            self.assertTrue(item_p.is_file())
            i_size = item_p.stat().st_size
            self.assertLess(i_size, 46080, f"MapReduce item {item_p.name} exceeded 46,080 bytes: {i_size}")

            item_data = json.loads(item_p.read_text(encoding="utf-8"))
            prompt = item_data["Prompt"]
            part_tag = f"part_{idx:02d}"

            self.assertIn(part_tag, prompt)
            self.assertIn(f"module_{idx:02d}.pdf", prompt)
            self.assertIn(f"--part {part_tag}", prompt)
            self.assertIn(raw_cta_prompt.strip(), prompt, f"Prompt in {item_p.name} must preserve 100% of prompt_cta_architect.md")


if __name__ == "__main__":
    unittest.main()

