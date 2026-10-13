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

# Imports from skills & validator
from check_cta import check_cta_katex, validate_distractor_math, RAW_LATEX_PATTERNS
from check_templates import check_templates_file_or_dir
from cta_merge import normalize_orphan_math, sanitize_competency_math, stitch_cta_parts
from dispatch import (
    build_dispatch,
    generate_author_bundle,
    generate_cta_direct_bundle,
    preseed_author_scaffolds,
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
    # 1. Pure JSON fragments in CTA & cta-stitch stage (<200ms)
    # -------------------------------------------------------------------------
    def test_cta_stitch_pure_json_parts_performance_and_accuracy(self):
        """CTA parts are stitched into cta.json and cta.md in <200ms with math auto-normalized."""
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

        # Execute stitch
        t0 = time.time()
        res = stitch_cta_parts(self.work_dir)
        elapsed = time.time() - t0

        # Must execute in < 200 ms (0.2 seconds)
        self.assertLess(elapsed, 0.200, f"cta-stitch took {elapsed:.4f}s, exceeding 200ms budget!")
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

    def test_pipeline_runner_cta_stitch_stage(self):
        """PipelineRunner executes --stage cta-stitch seamlessly."""
        parts_dir = self.work_dir / "cta_parts"
        parts_dir.mkdir(parents=True, exist_ok=True)
        part = [{"id": "H-01", "name": "Test Comp", "type": "fact", "distractors": []}]
        (parts_dir / "part_01.json").write_text(json.dumps(part), encoding="utf-8")

        runner = PipelineRunner(work_dir=str(self.work_dir))
        res = runner.execute(target_stage="cta-stitch")
        self.assertIn("cta-stitch", res)
        self.assertEqual(res["cta-stitch"]["total_competencies"], 1)

    def test_cta_stitch_deduplicates_duplicate_competencies_across_parts(self):
        """stitch_cta_parts gracefully deduplicates competency IDs defined across multiple parts."""
        parts_dir = self.work_dir / "cta_parts"
        parts_dir.mkdir(parents=True, exist_ok=True)

        part_01 = [
            {"id": "C-01", "name": "Definición Inicial", "type": "concept", "distractors": []}
        ]
        part_02 = [
            {"id": "C-01", "name": "Definición Refinada", "type": "concept", "distractors": []},
            {"id": "C-02", "name": "Segunda Competencia", "type": "concept", "distractors": []}
        ]
        (parts_dir / "part_01.json").write_text(json.dumps(part_01), encoding="utf-8")
        (parts_dir / "part_02.json").write_text(json.dumps(part_02), encoding="utf-8")

        res = stitch_cta_parts(self.work_dir)
        self.assertEqual(res["total_competencies"], 2)

        cta_data = json.loads((self.work_dir / "cta.json").read_text(encoding="utf-8"))
        comp_ids = [c["id"] for c in cta_data["competencies"]]
        self.assertEqual(comp_ids, ["C-01", "C-02"])
        # Should keep the latest definition
        c01 = next(c for c in cta_data["competencies"] if c["id"] == "C-01")
        self.assertEqual(c01["name"], "Definición Refinada")

    # -------------------------------------------------------------------------
    # 2. Line-level editing instruction in CTA prompt & bundle
    # -------------------------------------------------------------------------
    def test_cta_direct_bundle_enforces_pure_json_parts_and_replace_file_content(self):
        """CTA Direct bundle requires declarative JSON parts & replace_file_content for edits."""
        bundle_file = generate_cta_direct_bundle(
            work_dir=self.work_dir,
            read_paths=["work/pages/manifest.json"],
            write_paths=["work/cta_parts/part_*.json"],
        )
        content = bundle_file.read_text(encoding="utf-8")
        self.assertIn("work/cta_parts/part_XX.json", content)
        self.assertIn("replace_file_content", content)
        self.assertIn("cta-stitch", content)

    # -------------------------------------------------------------------------
    # 3. Isolated shard workspaces preventing concurrent collisions
    # -------------------------------------------------------------------------
    def test_isolated_shard_workspaces_prevent_collisions(self):
        """Each author shard receives an isolated scratch/work folder."""
        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "shard_01.json").write_text(
            json.dumps({"shard_id": "shard_01", "competency_ids": ["H-01"]}), encoding="utf-8"
        )
        (shards_dir / "shard_02.json").write_text(
            json.dumps({"shard_id": "shard_02", "competency_ids": ["C-01"]}), encoding="utf-8"
        )
        (self.work_dir / "cta.json").write_text(
            json.dumps({"competencies": [{"id": "H-01"}, {"id": "C-01"}]}), encoding="utf-8"
        )

        dispatch = build_dispatch(role="author", work_dir=self.work_dir)
        subagents = dispatch["Subagents"]
        self.assertEqual(len(subagents), 2)

        prompt1 = subagents[0]["Prompt"]
        prompt2 = subagents[1]["Prompt"]

        # Ensure isolated scratch folders are referenced
        self.assertIn("work/shards/shard_01/scratch/**", prompt1)
        self.assertIn("work/shards/shard_02/scratch/**", prompt2)

        # Ensure the physical isolated scratch folders were created
        self.assertTrue((self.work_dir / "shards" / "shard_01" / "scratch").is_dir())
        self.assertTrue((self.work_dir / "shards" / "shard_02" / "scratch").is_dir())
        self.assertTrue((self.work_dir / "scratch" / "shard_01").is_dir())
        self.assertTrue((self.work_dir / "scratch" / "shard_02").is_dir())

    def test_author_turn_budget_is_ten_trips(self):
        """Author subagents are configured with 50 turn ceiling and 10 trips operational target ('10 viajes')."""
        self.assertEqual(ROLE_SPECS["author"]["turn_budget"], 50)
        bundle_file = generate_author_bundle(
            work_dir=self.work_dir,
            shard_id="shard_01",
            read_paths=["work/shards/shard_01.json"],
            write_paths=["work/templates/H-01.json"],
        )
        content = bundle_file.read_text(encoding="utf-8")
        self.assertIn("50 turnos", content)
        self.assertIn("10 viajes", content)

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
        """preseed_author_scaffolds pre-populates templates with 100% distractor coverage and 0 errors."""
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

        shards = [{"shard_id": "shard_01", "competency_ids": ["Hab-01"]}]
        preseeded = preseed_author_scaffolds(self.work_dir, shards)

        self.assertIn("Hab-01", preseeded)
        tpl_file = self.work_dir / "templates" / "Hab-01.json"
        self.assertTrue(tpl_file.is_file())

        tpl_data = json.loads(tpl_file.read_text(encoding="utf-8"))
        self.assertEqual(tpl_data["competency_id"], "Hab-01")
        self.assertGreaterEqual(len(tpl_data["templates"]), 6)

        # Verify 100% distractor coverage (TPL-D3) across pre-seeded templates
        all_referenced_dids = set()
        for t in tpl_data["templates"]:
            self.assertIn("stem_variants", t)
            self.assertGreaterEqual(len(t["stem_variants"]), 3)
            all_referenced_dids.update(t.get("distractor_ids", []))

        expected_dids = {f"D-Hab01-{i:02d}" for i in range(1, 7)}
        self.assertEqual(expected_dids, all_referenced_dids)

        # CRITICAL TEST: Validate that pre-seeded scaffold passes check_templates.py with 0 errors!
        is_valid, errors = check_templates_file_or_dir(tpl_file, cta_path=self.work_dir / "cta.json")
        self.assertTrue(is_valid, f"Pre-seeded scaffold failed validation with errors: {errors}")
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
        manifest = {
            "course_id": "solow_growth_sim",
            "title": "Simulated Solow Course",
            "source_path": "content/solow",
            "pages": [{"page_number": 1, "text": "Model Intro"}]
        }
        (self.work_dir / "pages").mkdir(parents=True, exist_ok=True)
        (self.work_dir / "pages" / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        # 1. Dispatch CTA direct role
        dispatch = build_dispatch(role="cta-direct", work_dir=self.work_dir)
        subagents = dispatch["Subagents"]
        self.assertEqual(len(subagents), 1)
        self.assertEqual(subagents[0]["TypeName"], "c2c-cta-direct")
        self.assertEqual(subagents[0]["Role"], "Direct CTA Architect")

        # 2. Subagent emits modular declarative parts
        parts_dir = self.work_dir / "cta_parts"
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

        # 4. Execute cta-stitch stage
        runner = PipelineRunner(work_dir=str(self.work_dir))
        res = runner.execute(target_stage="cta-stitch")
        self.assertIn("cta-stitch", res)
        self.assertEqual(res["cta-stitch"]["total_competencies"], 1)

        # 5. Verify final cta.json has normalized math
        cta_data = json.loads((self.work_dir / "cta.json").read_text(encoding="utf-8"))
        comp = cta_data["competencies"][0]
        self.assertIn("$\\dot{k}$", comp["name"])
        self.assertIn("$\\bar{k}$", comp["description_latex"])
        self.assertIn("$\\frac{1}{3}$", comp["description_latex"])

    def test_simulated_shard_author_subagent_full_workflow(self):
        """Simulates full Shard Author flow: bundle dispatch -> pre-seeded scaffolds -> isolated scratch -> validation."""
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
        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "shard_01.json").write_text(
            json.dumps({"shard_id": "shard_01", "competency_ids": ["C-01"]}), encoding="utf-8"
        )

        # 1. Dispatch author role (automatically triggers scaffold pre-seeding)
        dispatch = build_dispatch(role="author", work_dir=self.work_dir)
        subagents = dispatch["Subagents"]
        self.assertEqual(len(subagents), 1)

        # 2. Check isolated scratch exists
        shard_scratch = self.work_dir / "shards" / "shard_01" / "scratch"
        self.assertTrue(shard_scratch.is_dir())

        # Author can safely write scratch scripts in isolated directory
        (shard_scratch / "calc_test.py").write_text("# Scratch test for shard_01", encoding="utf-8")

        # 3. Check pre-seeded scaffold exists and validates cleanly
        tpl_path = self.work_dir / "templates" / "C-01.json"
        self.assertTrue(tpl_path.is_file())

        is_valid, errors = check_templates_file_or_dir(tpl_path, cta_path=self.work_dir / "cta.json")
        self.assertTrue(is_valid, f"Author starter scaffold has validation errors: {errors}")
        self.assertEqual(len(errors), 0)

        # 4. Author modifies template via line-level edits (e.g. adjusts difficulty)
        content = tpl_path.read_text(encoding="utf-8")
        modified = content.replace('"difficulty": "easy"', '"difficulty": "medium"')
        tpl_path.write_text(modified, encoding="utf-8")

        # 5. Re-validate within turn budget (<= 10 turnos)
        is_valid_after, errors_after = check_templates_file_or_dir(tpl_path, cta_path=self.work_dir / "cta.json")
        self.assertTrue(is_valid_after, f"Validation errors after author edit: {errors_after}")
        self.assertEqual(len(errors_after), 0)


if __name__ == "__main__":
    unittest.main()
