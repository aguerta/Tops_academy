"""Comprehensive Adversarial Integration Test Suite for Content-to-Course (C2C) v3.1.

Certifies the 4 Architectural Pillars:
- Pilar 1: Anti-Rewrite Shield in Direct CTA (auto_balance_math_delimiters, sanitize_competency_math,
           skill omitted_step auto-promotion, exact 3-5 line context for replace_file_content).
- Pilar 2: Zero-Friction Orchestration (dynamic get_work_rel, author.json < 45KB view_file limit,
           pre-indexed scaffold line map).
- Pilar 3: Mechanical Non-Semantic Auto-Healer (ASCII control chars restoration, generate(rng) local
           variables export to 'vars', multiple_select error_rationale auto-population from CTA).
- Pilar 4: Blind Judges Zero-Warmup & Scope-Lock Security (prompt batch injection, ground_truth strictly
           forbidden from READ).
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List

# Ensure skill package is in sys.path
SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))


class TestC2Cv31AdversarialPlan(unittest.TestCase):
    """Adversarial Integration Test Suite for C2C v3.1 optimizations."""

    def setUp(self) -> None:
        self.test_dir = Path(tempfile.mkdtemp(prefix="test_c2c_v31_adversarial_"))
        self.work_dir = self.test_dir / "work"
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir, ignore_errors=True)

    # =========================================================================
    # PILAR 1: Anti-Rewrite Shield in Stage 1B Direct CTA
    # =========================================================================

    def test_pilar1_auto_balance_math_and_correct_belief(self) -> None:
        """Verifies auto_balance_math_delimiters and sanitize_competency_math behavior.

        - Repairs odd unescaped '$' delimiters in description_latex and correct_belief when '{' and '}' are balanced.
        - Collapses accidental '$$$' into '$$'.
        - Preserves genuine broken macros with unbalanced braces (e.g. r"\\frac{a}{b$") without auto-closing.
        """
        from cta_merge import auto_balance_math_delimiters, sanitize_competency_math

        # 1. Triple dollar collapse
        self.assertEqual(auto_balance_math_delimiters("$$$k_{t+1}$$$"), "$$k_{t+1}$$")
        self.assertEqual(auto_balance_math_delimiters("Ecuación: $$$y = f(k)$$$"), "Ecuación: $$y = f(k)$$")

        # 2. Odd unescaped '$' with balanced braces -> closed cleanly
        self.assertEqual(auto_balance_math_delimiters("Valor $k"), "Valor $k$")
        self.assertEqual(auto_balance_math_delimiters("Dinámica del capital $\\dot{k} = s f(k) - (n + g + \\delta) k."),
                         "Dinámica del capital $\\dot{k} = s f(k) - (n + g + \\delta) k$.")
        self.assertEqual(auto_balance_math_delimiters("Tasa efectiva $n + g + \\delta,"),
                         "Tasa efectiva $n + g + \\delta$,")
        self.assertEqual(auto_balance_math_delimiters("Condición de Inada $\\lim_{k \\to 0} f'(k) = \\infty;"),
                         "Condición de Inada $\\lim_{k \\to 0} f'(k) = \\infty$;")

        # 3. Unbalanced braces MUST NOT be masked by auto-closing '$'
        broken_expr1 = r"\frac{a}{b$"
        self.assertEqual(auto_balance_math_delimiters(broken_expr1), broken_expr1)
        broken_expr2 = r"\sqrt{x$"
        self.assertEqual(auto_balance_math_delimiters(broken_expr2), broken_expr2)

        # 4. sanitize_competency_math on full competency dictionary
        comp: Dict[str, Any] = {
            "id": "C-09",
            "name": "Acumulación $k^*",
            "description_latex": "Dinámica de Solow $\\dot{k} = s f(k) - (n+g) k",
            "description": "Análisis formal",
            "distractors": [
                {
                    "id": "D-C09-01",
                    "name": "Error de Depreciación",
                    "manifestation": "Omitir $\\delta",
                    "wrong_belief": "La tasa efectiva es $n + g",
                    "correct_belief": "La tasa efectiva es $n + g + \\delta",
                    "remediation_hint": "Incluir depreciación $\\delta",
                    "trigger": "Al despejar $k^*",
                },
                {
                    "id": "D-C09-02",
                    "name": "Error de Sintaxis Rota",
                    "manifestation": r"\frac{a}{b$",
                    "wrong_belief": "wb",
                    "correct_belief": "cb",
                    "remediation_hint": "hint",
                }
            ],
        }

        sanitize_competency_math(comp)

        # Verify description_latex was auto-balanced with closing '$'
        self.assertTrue(comp["description_latex"].endswith("$"),
                        f"description_latex should end with '$': {comp['description_latex']}")
        self.assertEqual(comp["description_latex"].count("$"), 2)

        # Verify correct_belief in D-C09-01 was sanitized and auto-balanced
        d1 = comp["distractors"][0]
        self.assertTrue(d1["correct_belief"].endswith("$"),
                        f"correct_belief should end with '$': {d1['correct_belief']}")
        self.assertEqual(d1["correct_belief"].count("$"), 2)
        self.assertTrue(d1["wrong_belief"].endswith("$"))
        self.assertTrue(d1["manifestation"].endswith("$"))
        self.assertTrue(d1["trigger"].endswith("$"))

        # Verify broken distractor with unbalanced braces was NOT auto-closed
        d2 = comp["distractors"][1]
        self.assertEqual(d2["manifestation"], r"\frac{a}{b$")

    def test_pilar1_compile_cta_context_and_skill_omitted_step(self) -> None:
        """Verifies render_compact_cta_errors snippet block and skill omitted_step auto-promotion.

        - render_compact_cta_errors with source_lines returns 'CONTEXTO EXACTO PARA replace_file_content'.
        - compile_tuples_to_cta_dict for 'skill' competencies auto-promotes omitted_step from wrong_belief.
        """
        import compile_cta

        # 1. Test render_compact_cta_errors with source_lines
        errors = ["[CTA-D1] [cta_data.py:Línea 5] Distractor 'D-C01-01' error de prueba"]
        source_lines = [
            "# Header Line 1",
            "# Line 2: COMPETENCIES = [",
            "    ('skill', 'Hab-01', 'Name', 'Desc', 'Apply', 'doc.pdf', 1, [], [",
            "        ('D1', 'Wrong 1', 'Correct 1', '$0$', 'Hint 1'),",
            "        ('D2', 'Wrong 2', 'Correct 2', '$1$', 'Hint 2'),",  # Line 5
            "        ('D3', 'Wrong 3', 'Correct 3', '$2$', 'Hint 3'),",
            "    ])",
        ]
        compact_output = compile_cta.render_compact_cta_errors(
            errors,
            data_filename="cta_data.py",
            source_lines=source_lines,
        )

        self.assertIn("CONTEXTO EXACTO PARA replace_file_content", compact_output)
        self.assertIn("StartLine=4, EndLine=6", compact_output)
        self.assertIn("L5:         ('D2', 'Wrong 2', 'Correct 2', '$1$', 'Hint 2'),", compact_output)
        self.assertIn("PROHIBIDO usar 'write_to_file' con Overwrite=True", compact_output)

        # 2. Test compile_tuples_to_cta_dict auto-promotion for skill
        skill_tuples = [
            (
                "skill",
                "Hab-01",
                "Derivación de Tasa Dorada",
                r"Optimización intertemporal $\max c(k)$ en Solow.",
                "Apply",
                "solow_paper.pdf",
                12,
                [],
                [
                    ("D1", "Olvidar depreciación al derivar", "Derivar f'(k) = n + g + delta", "$1$", "Hint 1"),
                    ("D2", "Despejar k con exponente invertido", "k = (s / (n+g+delta))^(1/(1-alpha))", "$2$", "Hint 2"),
                    ("D3", "Confundir producto per cápita con total", "Usar Y en vez de y", "$3$", "Hint 3"),
                    ("D4", "Error aritmético en estado estacionario", "Verificar constantes", "$4$", "Hint 4"),
                    ("D5", "Signo incorrecto en la acumulación", "Añadir inversión", "$5$", "Hint 5"),
                    ("D6", "Inversión nula asumida", "s > 0", "$6$", "Hint 6"),
                ],
            )
        ]

        cta_dict = compile_cta.compile_tuples_to_cta_dict(
            competencies_tuples=skill_tuples,
            course_id="solow_macro",
            title="Macroeconomía Dinámica",
        )

        comp = cta_dict["competencies"][0]
        self.assertEqual(comp["type"], "skill")
        distractors = comp["distractors"]
        self.assertEqual(len(distractors), 6)

        omitted_steps = [d for d in distractors if d.get("omitted_step")]
        self.assertGreaterEqual(
            len(omitted_steps),
            2,
            f"Skill competency must have >= 2 omitted_step distractors to satisfy CTA-D2. Found {len(omitted_steps)}",
        )
        # Verify first two were promoted from wrong_belief
        self.assertEqual(omitted_steps[0]["omitted_step"], "Olvidar depreciación al derivar")
        self.assertEqual(omitted_steps[0]["error_type"], "skipped_step")
        self.assertEqual(omitted_steps[1]["omitted_step"], "Despejar k con exponente invertido")
        self.assertEqual(omitted_steps[1]["error_type"], "skipped_step")

    # =========================================================================
    # PILAR 2: Zero-Friction Orchestration & Author Dispatch < 45KB
    # =========================================================================

    def test_pilar2_dynamic_work_rel_and_pytest_tmp_path_compat(self) -> None:
        """Verifies get_work_rel dynamic workspace pathing and pytest tmp_path fallback."""
        import dispatch

        # 1. Relative path within workspace returns identical normalized posix relative path
        rel_course = "courses/solow_model/work"
        self.assertEqual(dispatch.get_work_rel(rel_course), "courses/solow_model/work")

        # 2. Path inside cwd returns relative posix path
        cwd_sub = Path.cwd() / "courses" / "macroeconomics" / "work"
        self.assertEqual(dispatch.get_work_rel(cwd_sub), "courses/macroeconomics/work")

        # 3. External temporary directory (e.g. pytest tmp_path) outside cwd falls back to "work"
        external_tmp = Path(tempfile.gettempdir()) / "pytest_external_run" / "test"
        self.assertEqual(dispatch.get_work_rel(external_tmp), "work")
        self.assertEqual(dispatch.get_work_rel(str(external_tmp)), "work")

        # 4. Standard "work" returns "work"
        self.assertEqual(dispatch.get_work_rel("work"), "work")

    def test_pilar2_author_dispatch_under_45kb_view_file_limit(self) -> None:
        """Simulates 5 shards with 33 competencies and certifies author.json < 45,000 bytes.

        - Ensures author.json does not exceed the Antigravity view_file limit of 46,080 bytes.
        - Ensures ### MAPA DE LÍNEAS PRE-INDEXADO is present in each shard prompt.
        """
        import dispatch

        # Setup course with 33 competencies across 5 shards (7 + 7 + 7 + 6 + 6)
        shard_sizes = [7, 7, 7, 6, 6]
        all_comp_ids: List[str] = []
        c_counter = 1
        shards_info: List[Dict[str, Any]] = []

        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        templates_dir = self.work_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)

        for s_idx, size in enumerate(shard_sizes, start=1):
            s_id = f"shard_{s_idx:02d}"
            s_cids = []
            for _ in range(size):
                cid = f"C-{c_counter:02d}"
                s_cids.append(cid)
                all_comp_ids.append(cid)
                c_counter += 1

                # Write a standard 6-template JSON file for each competency
                tpls = []
                for t_idx in range(1, 7):
                    itype = "multiple_choice_7_options" if t_idx <= 2 else ("fill_in_the_blank" if t_idx <= 4 else "multiple_select")
                    tpls.append({
                        "id": f"T-{cid}-0{t_idx}",
                        "competency_id": cid,
                        "interaction_type": itype,
                        "difficulty": "medium",
                        "bloom": "Apply",
                        "stem": f"Pregunta modelo para {cid} plantilla {t_idx} con math $y = k^\\alpha$.",
                        "stem_variants": [f"Variante alternativa para {cid}."],
                        "generate_py": (
                            "def generate(rng):\n"
                            "    k = round(rng.uniform(1.0, 5.0), 2)\n"
                            "    return {\n"
                            "        'vars': {'k': k},\n"
                            "        'options': [{'content': 'A', 'is_correct': True, 'distractor_id': None, 'error_rationale': None}],\n"
                            "    }\n"
                        ),
                        "cross_check_py": "def cross_check(inst):\n    return True, []\n",
                        "hints": ["Pista 1", "Pista 2", "Pista 3"],
                        "solution": "Solución formal detallada.",
                        "distractor_ids": [f"D-{cid}-01", f"D-{cid}-02"],
                    })

                tpl_content = json.dumps({"competency_id": cid, "templates": tpls}, indent=2, ensure_ascii=False)
                (templates_dir / f"{cid}.json").write_text(tpl_content, encoding="utf-8")

            (shards_dir / f"{s_id}.json").write_text(
                json.dumps({"shard_id": s_id, "competency_ids": s_cids}, indent=2),
                encoding="utf-8",
            )
            shards_info.append({"shard_id": s_id, "competency_ids": s_cids})

        # Write cta.json and shards_plan.json
        cta_comps = [{"id": cid, "name": f"Competencia {cid}", "distractors": []} for cid in all_comp_ids]
        (self.work_dir / "cta.json").write_text(
            json.dumps({"course_id": "solow_33", "competencies": cta_comps}, indent=2),
            encoding="utf-8",
        )
        (self.work_dir / "shards_plan.json").write_text(
            json.dumps({"shards": shards_info}, indent=2),
            encoding="utf-8",
        )

        # Generate dispatch for role='author'
        dispatch_payload = dispatch.build_dispatch(role="author", work_dir=self.work_dir)

        author_json_path = self.work_dir / "dispatch" / "author.json"
        self.assertTrue(author_json_path.is_file(), f"Expected author.json at {author_json_path}")

        author_bytes = author_json_path.stat().st_size
        self.assertLess(
            author_bytes,
            45000,
            f"author.json ({author_bytes} bytes) exceeds strict 45,000 bytes limit (view_file buffer limit: 46,080 bytes)!",
        )

        # Verify each subagent prompt contains pre-indexed line map
        subagents = dispatch_payload.get("Subagents", [])
        self.assertEqual(len(subagents), 5, f"Expected 5 author subagents, got {len(subagents)}")

        for sa in subagents:
            prompt = sa.get("Prompt", "")
            self.assertIn(
                "### MAPA DE LÍNEAS PRE-INDEXADO",
                prompt,
                f"Subagent {sa.get('TypeName')} prompt missing pre-indexed line map!",
            )
            self.assertIn("replace_file_content", prompt)

    # =========================================================================
    # PILAR 3: Mechanical Non-Semantic Auto-Healer
    # =========================================================================

    def test_pilar3_auto_heal_control_chars_and_vars_export(self) -> None:
        """Verifies auto_heal_template_data on control chars, vars export, and multiple_select rationales."""
        import check_templates

        # 1. Test ASCII control characters restoration: \x0c -> \\f, \x08 -> \\b
        corrupted_template_data = {
            "competency_id": "C-01",
            "templates": [
                {
                    "id": "T-C01-01",
                    "interaction_type": "multiple_choice_7_options",
                    "stem": "Calcular la tasa \x0crac{s}{n} del modelo con parámetro \x08eta.",
                    "stem_variants": ["Variante con \x0crac{Y}{L} y \x08ar{k}."],
                    "generate_py": (
                        "def generate(rng):\n"
                        "    alpha = round(rng.uniform(0.2, 0.4), 2)\n"
                        "    s = round(rng.uniform(0.1, 0.3), 2)\n"
                        "    k_star = round((s / 0.1) ** (1 / (1 - alpha)), 2)\n"
                        "    y_star = round(k_star ** alpha, 2)\n"
                        "    return {\n"
                        "        'vars': {'alpha': alpha, 's': s, 'k_star': k_star},\n"
                        "        'options': [{'content': 'A', 'is_correct': True, 'distractor_id': None, 'error_rationale': None}],\n"
                        "    }\n"
                    ),
                    "hints": ["Pista con \x0crac{1}{2}."],
                    "solution": "Solución con \x08eta y \x0crac{s}{n}.",
                },
                {
                    "id": "T-C01-02",
                    "interaction_type": "multiple_select",
                    "stem": "Seleccione las opciones correctas con respecto al valor calculado {y_star}.",
                    "generate_py": (
                        "def generate(rng):\n"
                        "    return {\n"
                        "        'vars': {},\n"
                        "        'options': [\n"
                        "            {'content': 'Opt A', 'is_correct': True, 'distractor_id': None, 'error_rationale': None},\n"
                        "            {'content': 'Opt B', 'is_correct': False, 'distractor_id': 'D-C01-01', 'error_rationale': None},\n"
                        "            {'content': 'Opt C', 'is_correct': False, 'distractor_id': 'D-C01-02', 'error_rationale': ''},\n"
                        "        ],\n"
                        "    }\n"
                    ),
                    "solution": "Solución para MS.",
                }
            ],
        }

        cta_comp = {
            "id": "C-01",
            "distractors": [
                {
                    "id": "D-C01-01",
                    "name": "Error de Flujo vs Stock",
                    "wrong_belief": "Confundir la inversión de flujo con el stock de capital acumulado",
                    "remediation_hint": "Revisar la ley fundamental de acumulación",
                },
                {
                    "id": "D-C01-02",
                    "name": "Omisión de Depreciación",
                    "wrong_belief": "Ignorar la tasa de depreciación delta en el equilibrio",
                    "remediation_hint": "Verificar la inversión de reposición",
                }
            ]
        }

        modified, fixes = check_templates.auto_heal_template_data(
            corrupted_template_data,
            cta_comp=cta_comp,
        )

        self.assertTrue(modified, "auto_heal_template_data should report modified=True for corrupted data")
        self.assertGreater(len(fixes), 0)

        t1 = corrupted_template_data["templates"][0]
        # Verify \x0c -> \\f and \x08 -> \\b
        self.assertNotIn("\x0c", t1["stem"])
        self.assertIn(r"\frac", t1["stem"])
        self.assertNotIn("\x08", t1["stem"])
        self.assertIn(r"\beta", t1["stem"])

        self.assertNotIn("\x0c", t1["stem_variants"][0])
        self.assertIn(r"\frac", t1["stem_variants"][0])
        self.assertIn(r"\bar", t1["stem_variants"][0])

        self.assertNotIn("\x0c", t1["hints"][0])
        self.assertIn(r"\frac", t1["hints"][0])

        self.assertNotIn("\x08", t1["solution"])
        self.assertIn(r"\beta", t1["solution"])

        # Verify auto-export of local variable y_star into 'vars'
        # Notice T-C01-02 stem references {y_star}, and T-C01-01 generate_py computes y_star!
        # If referenced in stem or solution, it gets auto-exported:
        t1["stem"] += " El valor es {y_star}."
        modified2, fixes2 = check_templates.auto_heal_template_data(corrupted_template_data, cta_comp=cta_comp)
        self.assertTrue(modified2)
        self.assertIn("'y_star': y_star", corrupted_template_data["templates"][0]["generate_py"])

        # Verify auto-fill of error_rationale in multiple_select
        t2_gen_py = corrupted_template_data["templates"][1]["generate_py"]
        self.assertIn("Confundir la inversión de flujo con el stock de capital acumulado", t2_gen_py)
        self.assertIn("Ignorar la tasa de depreciación delta en el equilibrio", t2_gen_py)

    # =========================================================================
    # PILAR 4: Blind Judges Zero-Warmup & Scope Security
    # =========================================================================

    def test_pilar4_judge_prompt_batch_injection_without_ground_truth(self) -> None:
        """Verifies build_dispatch(role='judge') injects items without leaking ground_truth in READ."""
        import dispatch

        # Create judge batch file
        batch_items = {
            "items": [
                {
                    "item_id": "I-C01-01",
                    "interaction_type": "multiple_choice_7_options",
                    "stem": "¿Cuál es la tasa de ahorro requerida en estado estacionario?",
                    "options": [
                        {"letter": "A", "content": "s = 0.20"},
                        {"letter": "B", "content": "s = 0.35"},
                    ],
                },
                {
                    "item_id": "I-C01-02",
                    "interaction_type": "fill_in_the_blank",
                    "stem": "Calcular k* cuando s = 0.3, delta = 0.05, n = 0.01.",
                }
            ]
        }

        # Write judge_batch_01.json in work_dir
        batch_file = self.work_dir / "judge_batch_01.json"
        batch_file.write_text(json.dumps(batch_items, indent=2), encoding="utf-8")

        # Also write judge_ground_truth.json to ensure it is isolated
        gt_file = self.work_dir / "judge_ground_truth.json"
        gt_file.write_text(json.dumps({"I-C01-01": {"correct": "A"}}, indent=2), encoding="utf-8")

        # Build judge dispatch
        dispatch_payload = dispatch.build_dispatch(role="judge", work_dir=self.work_dir)
        subagents = dispatch_payload.get("Subagents", [])
        self.assertGreaterEqual(len(subagents), 1, "Expected at least 1 judge subagent")

        judge_sa = subagents[0]
        prompt = judge_sa.get("Prompt", "")

        # 1. Verify prompt contains batch items directly (Zero-Warmup injection)
        self.assertIn("I-C01-01", prompt, "Judge prompt should inject batch item I-C01-01 directly for zero-warmup!")
        self.assertIn("I-C01-02", prompt, "Judge prompt should inject batch item I-C01-02 directly for zero-warmup!")

        # 2. Strict Scope-Lock Security: ground_truth MUST NOT be in READ permitido
        lines = prompt.splitlines()
        in_read = False
        in_prohibido = False
        read_lines: List[str] = []
        prohibido_lines: List[str] = []

        for line in lines:
            if "- READ permitido:" in line:
                in_read = True
                in_prohibido = False
                continue
            elif "- WRITE permitido:" in line:
                in_read = False
                in_prohibido = False
                continue
            elif "- PROHIBIDO:" in line:
                in_read = False
                in_prohibido = True
                continue
            elif line.startswith("## ") or line.startswith("# "):
                in_read = False
                in_prohibido = False

            if in_read:
                read_lines.append(line)
            if in_prohibido:
                prohibido_lines.append(line)

        read_block = "\n".join(read_lines)
        prohibido_block = "\n".join(prohibido_lines)

        self.assertNotIn("ground_truth", read_block.lower(),
                         "CRITICAL SECURITY LEAK: ground_truth found in READ permitido of blind judge!")
        self.assertNotIn("judge_ground_truth", read_block.lower(),
                         "CRITICAL SECURITY LEAK: judge_ground_truth found in READ permitido of blind judge!")

        self.assertIn("ground_truth", prohibido_block.lower(),
                      "ground_truth MUST be explicitly listed under - PROHIBIDO: in blind judge prompt!")

    def test_pilar4_audit_engine_published_course_telemetry(self) -> None:
        """Verifies audit_engine.py resolves published courses in courses/ when course_id is generic ('Tops_academy', 'unknown', 'work')."""
        auditor_scripts = SKILL_DIR.parent / "c2c-run-auditor" / "scripts"
        if str(auditor_scripts) not in sys.path:
            sys.path.insert(0, str(auditor_scripts))
        from audit_engine import WorkloadExtractor

        courses_dir = self.test_dir / "courses"
        courses_dir.mkdir(parents=True, exist_ok=True)
        course_file = courses_dir / "solow_growth_model.json"
        course_data = {
            "course_id": "solow_growth_model",
            "title": "Modelo de Crecimiento de Solow-Swan",
            "questions": [{"id": f"Q-{i}"} for i in range(198)],
        }
        course_file.write_text(json.dumps(course_data, indent=2), encoding="utf-8")

        # Mock transcript records indicating completed Stage 4/5
        records = [
            {"content": "Iniciando ejecución del pipeline para Tops_academy..."},
            {"content": "Stage 4 (build) completed successfully. Built 198 items for solow_growth_model."},
            {"content": "run_stage_publish completed."},
        ]

        workload = WorkloadExtractor.extract(
            work_dir=self.work_dir,
            workspace_root=self.test_dir,
            records=records,
        )

        self.assertEqual(workload["course_id"], "solow_growth_model")
        self.assertEqual(workload["course_title"], "Modelo de Crecimiento de Solow-Swan")
        self.assertEqual(workload["questions_count"], 198)


if __name__ == "__main__":
    unittest.main()
