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

    def test_pilar1_auto_balance_math_complex_delimiters_and_punctuation(self) -> None:
        """Verifies auto_balance_math_delimiters handles compound punctuation, display blocks, and orphan delimiters."""
        from cta_merge import auto_balance_math_delimiters

        # 1. Multiple inline math blocks followed by an orphan delimiter and period
        self.assertEqual(auto_balance_math_delimiters("Si $a = 1$, halle $b = 2."), "Si $a = 1$, halle $b = 2$.")

        # 2. Orphan delimiter with question mark (not in stripped punctuation tuple -> appended at end)
        self.assertEqual(
            auto_balance_math_delimiters("¿Dada la tasa $s = 0.2$, se cumple que $n = 0.05?"),
            "¿Dada la tasa $s = 0.2$, se cumple que $n = 0.05?$",
        )

        # 3. Comma, colon, and semicolon punctuation
        self.assertEqual(auto_balance_math_delimiters("Dado $x = 1$ y $y = 2,"), "Dado $x = 1$ y $y = 2$,")
        self.assertEqual(auto_balance_math_delimiters("Considere $a = 1$ y la relación $b = 2:"), "Considere $a = 1$ y la relación $b = 2$:")
        self.assertEqual(auto_balance_math_delimiters("Propiedad $\\lim_{k \\to 0} f'(k) = \\infty;"), "Propiedad $\\lim_{k \\to 0} f'(k) = \\infty$;")

        # 4. Display math blocks '$$' mixed with orphan inline '$' (with and without punctuation)
        display_mixed = "Sea $$y = f(k)$$ la función de producción y $\\delta la depreciación."
        self.assertEqual(
            auto_balance_math_delimiters(display_mixed),
            "Sea $$y = f(k)$$ la función de producción y $\\delta la depreciación$.",
        )
        display_no_punct = "Sea $$y = f(k)$$ con parámetro $\\alpha"
        self.assertEqual(
            auto_balance_math_delimiters(display_no_punct),
            "Sea $$y = f(k)$$ con parámetro $\\alpha$",
        )

        # 5. Already balanced expressions must remain strictly untouched
        balanced_text = "El valor óptimo es $k^* = 5$ y el producto es $y^* = 2$."
        self.assertEqual(auto_balance_math_delimiters(balanced_text), balanced_text)

        # 6. Escaped dollars \\$ must NOT be counted as math delimiters
        escaped_dollar = r"El costo unitario es \$100 y la elasticidad es $\alpha"
        self.assertEqual(
            auto_balance_math_delimiters(escaped_dollar),
            r"El costo unitario es \$100 y la elasticidad es $\alpha$",
        )

        # 7. Broken macros with unbalanced braces must NOT be auto-closed even with trailing punctuation
        broken_with_dot = r"\frac{a}{b$."
        self.assertEqual(auto_balance_math_delimiters(broken_with_dot), broken_with_dot)

    def test_pilar1_compile_cta_anti_overwrite_backup(self) -> None:
        """Verifies compile_cta creates .cta_data.py.bak when >= 10 competencies and detects destructive shrink."""
        import compile_cta

        cta_data_file = self.work_dir / "cta_data.py"

        # Case 1: Initial compilation with < 10 competencies should NOT create .bak
        small_tuples = [
            ("concept", f"C-{i:02d}", f"Concepto {i}", f"Desc $k_{i}$", "Understand", "doc.pdf", 1, [], [
                (f"D{j}", f"W{j}", f"C{j}", f"${j}$", f"H{j}") for j in range(1, 7)
            ])
            for i in range(1, 6)
        ]
        cta_data_file.write_text(
            f"COURSE_ID = 'macro_small'\nTITLE = 'Macro Small'\nCOMPETENCIES = {repr(small_tuples)}\n",
            encoding="utf-8",
        )
        ok1, _, _, _ = compile_cta.compile_cta(cta_data_file, output_dir=self.work_dir)
        bak_file = self.work_dir / ".cta_data.py.bak"
        self.assertFalse(bak_file.is_file(), ".cta_data.py.bak should not be created for < 10 competencies")

        # Case 2: Compilation with >= 10 competencies MUST create .cta_data.py.bak
        ten_tuples = [
            ("concept", f"C-{i:02d}", f"Concepto {i}", f"Desc $k_{i}$", "Understand", "doc.pdf", 1, [], [
                (f"D{j}", f"W{j}", f"C{j}", f"${j}$", f"H{j}") for j in range(1, 7)
            ])
            for i in range(1, 11)
        ]
        ten_source = f"COURSE_ID = 'macro_ten'\nTITLE = 'Macro 10'\nCOMPETENCIES = {repr(ten_tuples)}\n"
        cta_data_file.write_text(ten_source, encoding="utf-8")

        ok2, cta_dict2, errs2, _ = compile_cta.compile_cta(cta_data_file, output_dir=self.work_dir)
        self.assertTrue(bak_file.is_file(), ".cta_data.py.bak MUST be created when len(COMPETENCIES) >= 10")
        bak_content = bak_file.read_text(encoding="utf-8")
        self.assertEqual(bak_content, ten_source, "Backup content must exactly match cta_data.py source")
        self.assertIn("C-10", bak_content)

        # Case 3: Destructive overwrite (accidental shrink to 2 competencies)
        # compile_cta detects shrink, and backup file remains safely preserved with all 10 competencies
        two_tuples = ten_tuples[:2]
        cta_data_file.write_text(
            f"COURSE_ID = 'macro_ten'\nTITLE = 'Macro 10'\nCOMPETENCIES = {repr(two_tuples)}\n",
            encoding="utf-8",
        )
        ok3, _, _, _ = compile_cta.compile_cta(cta_data_file, output_dir=self.work_dir)
        self.assertTrue(bak_file.is_file(), "Backup file must NOT be destroyed upon destructive shrink")
        preserved_bak = bak_file.read_text(encoding="utf-8")
        self.assertIn("C-10", preserved_bak, "Backup must retain all 10 original competencies")

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
        """Simulates 5 shards with 33 competencies using real preseeded scaffolds and certifies author.json < 45,000 bytes.

        - Uses preseed_author_scaffolds() to generate real starter templates for all 33 competencies.
        - Ensures author.json does not exceed the Antigravity view_file limit of 46,080 bytes.
        - Ensures ### MAPA DE LÍNEAS PRE-INDEXADO is present in each shard prompt with real template lines.
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

            (shards_dir / f"{s_id}.json").write_text(
                json.dumps({"shard_id": s_id, "competency_ids": s_cids}, indent=2),
                encoding="utf-8",
            )
            shards_info.append({"shard_id": s_id, "competency_ids": s_cids})

        # Write realistic cta.json with 6 distractors per competency
        cta_comps = []
        for cid in all_comp_ids:
            clean_id = cid.replace("-", "")
            cta_comps.append({
                "id": cid,
                "name": f"Dinámica y Acumulación {cid}",
                "type": "skill",
                "bloom": "Apply",
                "description_latex": f"Análisis dinámico de {cid} en Solow $\\dot{{k}} = s f(k) - (n+g+\\delta)k$.",
                "distractors": [
                    {
                        "id": f"D-{clean_id}-0{d_idx}",
                        "name": f"Error Conceptual {d_idx} en {cid}",
                        "manifestation": f"Omitir parámetro estructural {d_idx}",
                        "wrong_belief": f"El parámetro {d_idx} no influye en la convergencia",
                        "remediation_hint": f"Verificar la ley de acumulación para {cid}",
                    }
                    for d_idx in range(1, 7)
                ]
            })

        (self.work_dir / "cta.json").write_text(
            json.dumps({"course_id": "solow_33", "competencies": cta_comps}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        (self.work_dir / "shards_plan.json").write_text(
            json.dumps({"shards": shards_info}, indent=2),
            encoding="utf-8",
        )

        # Generate dispatch for role='author' (automatically invokes preseed_author_scaffolds)
        dispatch_payload = dispatch.build_dispatch(role="author", work_dir=self.work_dir)

        author_json_path = self.work_dir / "dispatch" / "author.json"
        self.assertTrue(author_json_path.is_file(), f"Expected author.json at {author_json_path}")

        author_bytes = author_json_path.stat().st_size
        self.assertLess(
            author_bytes,
            45000,
            f"author.json ({author_bytes} bytes) exceeds strict 45,000 bytes limit (view_file buffer limit: 46,080 bytes)!",
        )

        # Verify all 33 template files were automatically generated by preseed_author_scaffolds
        for cid in all_comp_ids:
            tpl_path = templates_dir / f"{cid}.json"
            self.assertTrue(tpl_path.is_file(), f"Preseeded template for {cid} was not created!")
            self.assertGreater(tpl_path.stat().st_size, 100)

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

    def test_pilar2_preseed_author_scaffolds_end_to_end_zero_errors(self) -> None:
        """Certifies end-to-end that preseed_author_scaffolds generates a template satisfying 100% of rules.

        Enforces: TPL-D1..D4, TPL-VAR >= 0.50, R-15, R-18, R-19, R-20, R-22 with strict=True and 50 seeds dry run.
        """
        import check_templates
        import dispatch

        comp: Dict[str, Any] = {
            "id": "C-01",
            "name": "Dinámica de Transición hacia el Estado Estacionario",
            "type": "skill",
            "bloom": "Apply",
            "description_latex": r"Ecuación fundamental de Solow $\dot{k} = s f(k) - (n + g + \delta) k$.",
            "distractors": [
                {
                    "id": "D-C01-01",
                    "name": "Omisión de Depreciación",
                    "manifestation": "Omitir la tasa de depreciación delta",
                    "wrong_belief": "La tasa efectiva de reemplazo es solo n + g",
                    "remediation_hint": "Incluir depreciación de capital delta en la tasa efectiva",
                },
                {
                    "id": "D-C01-02",
                    "name": "Confusión entre Flujo y Stock",
                    "manifestation": "Inversión bruta como stock",
                    "wrong_belief": "El stock de capital equivale a la inversión de flujo",
                    "remediation_hint": "Diferenciar claramente magnitudes de flujo y de acervo",
                },
                {
                    "id": "D-C01-03",
                    "name": "Exponente Invertido en Steady State",
                    "manifestation": "Exponente 1 - alpha en lugar de 1 / (1 - alpha)",
                    "wrong_belief": "El despeje produce k* con exponente invertido",
                    "remediation_hint": "Invertir correctamente el exponente al despejar",
                },
                {
                    "id": "D-C01-04",
                    "name": "Error de Signo en Amortiguamiento",
                    "manifestation": "Signo positivo en la tasa de ensanchamiento",
                    "wrong_belief": "El ensanchamiento del capital incrementa la acumulación neta",
                    "remediation_hint": "El ensanchamiento detrae capital per cápita, su signo es negativo",
                },
                {
                    "id": "D-C01-05",
                    "name": "Error de Escala Intensiva",
                    "manifestation": "Producto total Y en lugar de producto per cápita y",
                    "wrong_belief": "El producto agregado coincide numéricamente con el per cápita",
                    "remediation_hint": "Normalizar las variables por el trabajo efectivo",
                },
                {
                    "id": "D-C01-06",
                    "name": "Caso Frontera Extremo",
                    "manifestation": "Tasa de ahorro extrema s = 1",
                    "wrong_belief": "Una economía puede ahorrar el 100% de la producción de forma permanente",
                    "remediation_hint": "La tasa de ahorro satisface estrictamente 0 < s < 1",
                },
            ]
        }

        cta_file = self.work_dir / "cta.json"
        cta_file.write_text(
            json.dumps({"course_id": "macro_transition", "competencies": [comp]}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        preseeded = dispatch.preseed_author_scaffolds(work_dir=self.work_dir)
        self.assertIn("C-01", preseeded)

        tpl_file = self.work_dir / "templates" / "C-01.json"
        self.assertTrue(tpl_file.is_file(), "Starter template C-01.json must exist")

        tpl_data = json.loads(tpl_file.read_text(encoding="utf-8"))
        templates = tpl_data.get("templates", [])
        self.assertEqual(len(templates), 6, "Starter template must provide exactly 6 templates (2 MC7, 2 FIB, 2 MS)")

        # Verify interaction types: 2 MC7, 2 FIB, 2 MS
        itypes = [t["interaction_type"] for t in templates]
        self.assertEqual(itypes.count("multiple_choice_7_options"), 2)
        self.assertEqual(itypes.count("fill_in_the_blank"), 2)
        self.assertEqual(itypes.count("multiple_select"), 2)

        # Validate with strict production isomorphic parity and 50 seeds dry run
        is_clean, errors = check_templates.check_templates_file_or_dir(
            target_path=[tpl_file],
            cta_path=cta_file,
            num_dry_run_seeds=50,
            strict=True,
        )

        self.assertTrue(
            is_clean,
            f"Preseeded scaffold failed check_templates validation with {len(errors)} errors:\n" + "\n".join(errors[:5]),
        )
        self.assertEqual(len(errors), 0)

    def test_pilar2_starter_template_special_characters_and_single_quotes(self) -> None:
        """Verifies build_starter_template_for_competency handles single quotes in distractors without breaking AST."""
        import ast
        import check_templates
        import dispatch

        comp: Dict[str, Any] = {
            "id": "C-02",
            "name": "Regla de Hopital y Teorema de Euler",
            "type": "skill",
            "bloom": "Apply",
            "description_latex": r"Cálculo de límites indeterminados $\lim_{x \to 0} \frac{f(x)}{g(x)}$.",
            "distractors": [
                {
                    "id": "D-C02-01",
                    "name": "Hopital mal aplicado",
                    "manifestation": "Aplicar cuando no es 0/0 (L'Hopital)",
                    "wrong_belief": "L'Hopital sirve siempre para cualquier cociente",
                    "remediation_hint": "Verificar 0/0 o inf/inf antes de aplicar L'Hopital",
                },
                {
                    "id": "D-C02-02",
                    "name": "Euler constant swap",
                    "manifestation": "Confundir base e con Euler's gamma",
                    "wrong_belief": "Son la misma constante de Euler's",
                    "remediation_hint": "Diferenciar la base del logaritmo de la constante de Euler's",
                },
                {
                    "id": "D-C02-03",
                    "name": "Alembert swap",
                    "manifestation": "Invertir fuerzas en D'Alembert",
                    "wrong_belief": "Las fuerzas inerciales de D'Alembert tienen signo contrario",
                    "remediation_hint": "Revisar la ley dinámica de D'Alembert",
                },
                {
                    "id": "D-C02-04",
                    "name": "Fisher hypothesis",
                    "manifestation": "Tasa nominal sin inflacion esperada",
                    "wrong_belief": "La hipotesis de Fisher's establece igualdad estricta",
                    "remediation_hint": "Anadir inflacion esperada segun Fisher's equation",
                },
                {
                    "id": "D-C02-05",
                    "name": "Cauchy mean value",
                    "manifestation": "Omitir diferenciabilidad en Cauchy's theorem",
                    "wrong_belief": "El teorema de Cauchy's no requiere continuidad en el intervalo",
                    "remediation_hint": "Comprobar hipótesis de Cauchy's mean value",
                },
                {
                    "id": "D-C02-06",
                    "name": "Taylor remainder",
                    "manifestation": "Truncar sin residuo de Lagrange's",
                    "wrong_belief": "El residuo de Lagrange's es despreciable en todo el dominio",
                    "remediation_hint": "Acotar residuo de Lagrange's",
                },
            ]
        }

        scaffold = dispatch.build_starter_template_for_competency(comp)
        self.assertEqual(scaffold["competency_id"], "C-02")
        self.assertEqual(len(scaffold["templates"]), 6)

        # 1. Certify AST parsing of generate_py and cross_check_py for all 6 templates
        for idx, t in enumerate(scaffold["templates"], start=1):
            gen_py = t["generate_py"]
            try:
                ast.parse(gen_py)
            except SyntaxError as e:
                self.fail(f"Template {t['id']} generate_py failed AST parse due to unescaped single quote: {e}\n{gen_py}")

            cc_py = t["cross_check_py"]
            try:
                ast.parse(cc_py)
            except SyntaxError as e:
                self.fail(f"Template {t['id']} cross_check_py failed AST parse: {e}")

        # Verify that single quotes in distractors were escaped with \' in generate_py
        all_gen_py = " ".join(t["generate_py"] for t in scaffold["templates"])
        self.assertIn(r"\'", all_gen_py, "Single quotes in distractors must be escaped with \\' in generate_py")

        # 2. Write to disk and certify with check_templates
        cta_file = self.work_dir / "cta.json"
        cta_file.write_text(
            json.dumps({"course_id": "special_chars", "competencies": [comp]}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        tpl_dir = self.work_dir / "templates"
        tpl_dir.mkdir(parents=True, exist_ok=True)
        tpl_file = tpl_dir / "C-02.json"
        tpl_file.write_text(json.dumps(scaffold, indent=2, ensure_ascii=False), encoding="utf-8")

        is_clean, errors = check_templates.check_templates_file_or_dir(
            target_path=[tpl_file],
            cta_path=cta_file,
            strict=True,
        )
        self.assertTrue(is_clean, f"Special characters template failed validation: {errors}")
        self.assertEqual(len(errors), 0)

        # 3. Verify that even if comp['name'] contains single quotes (e.g. "Regla de L'Hôpital"),
        # build_starter_template_for_competency escapes cname_fstr cleanly so AST parse succeeds.
        quoted_name_comp = dict(comp, name="Regla de L'Hôpital")
        quoted_name_scaffold = dispatch.build_starter_template_for_competency(quoted_name_comp)
        for t in quoted_name_scaffold["templates"]:
            ast.parse(t["generate_py"])

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

    def test_pilar3_check_templates_auto_heal_persistence_and_no_auto_fix(self) -> None:
        """Verifies check_templates_file_or_dir persists healed templates to disk with auto_fix=True, and preserves disk with auto_fix=False."""
        import check_templates

        templates_dir = self.work_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        tpl_path = templates_dir / "C-01.json"
        cta_path = self.work_dir / "cta.json"

        cta_comp = {
            "id": "C-01",
            "name": "Acumulación y Convergencia",
            "type": "concept",
            "bloom": "Understand",
            "description_latex": "Dinámica de Solow.",
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
        cta_path.write_text(json.dumps({"course_id": "auto_heal_test", "competencies": [cta_comp]}, indent=2), encoding="utf-8")

        corrupted_raw = {
            "competency_id": "C-01",
            "templates": [
                {
                    "id": "T-C01-01",
                    "interaction_type": "multiple_choice_7_options",
                    "difficulty": "medium",
                    "bloom": "Understand",
                    "stem": "Calcular la tasa \x0crac{s}{n} con parámetro \x08eta y valor {y_star}.",
                    "stem_variants": ["Variante con \x0crac{Y}{L} y \x08ar{k}."],
                    "generate_py": (
                        "def generate(rng):\n"
                        "    alpha = round(rng.uniform(0.2, 0.4), 2)\n"
                        "    s = round(rng.uniform(0.1, 0.3), 2)\n"
                        "    y_star = round(alpha * s, 2)\n"
                        "    return {\n"
                        "        'vars': {'alpha': alpha, 's': s},\n"
                        "        'correct': 'A',\n"
                        "        'distractors': [{'value': f'D{i}', 'distractor_id': f'D-C01-0{i}'} for i in range(1, 7)],\n"
                        "    }\n"
                    ),
                    "cross_check_py": "def verify(res):\n    return True\n",
                    "hints": ["Pista con \x0crac{1}{2}."],
                    "solution": "Solución con \x08eta.",
                    "distractor_ids": ["D-C01-01", "D-C01-02"],
                },
                {
                    "id": "T-C01-02",
                    "interaction_type": "multiple_select",
                    "difficulty": "medium",
                    "bloom": "Understand",
                    "stem": "Seleccione las afirmaciones correctas para C-01:",
                    "stem_variants": ["Variante de selección múltiple para C-01:"],
                    "generate_py": (
                        "def generate(rng):\n"
                        "    return {\n"
                        "        'vars': {},\n"
                        "        'options': [\n"
                        "            {'content': 'Opt A', 'is_correct': True, 'distractor_id': None, 'error_rationale': None},\n"
                        "            {'content': 'Opt B', 'is_correct': False, 'distractor_id': 'D-C01-01', 'error_rationale': None},\n"
                        "        ],\n"
                        "    }\n"
                    ),
                    "cross_check_py": "def verify(res):\n    return True\n",
                    "hints": ["Pista MS"],
                    "solution": "Solución MS",
                    "distractor_ids": ["D-C01-01"],
                }
            ]
        }

        # Step 1: Write corrupted template to disk
        corrupted_text = json.dumps(corrupted_raw, indent=2, ensure_ascii=False)
        tpl_path.write_text(corrupted_text, encoding="utf-8")
        data_step1 = json.loads(tpl_path.read_text(encoding="utf-8"))
        self.assertIn("\x0c", data_step1["templates"][0]["stem"])
        self.assertIn("\x08", data_step1["templates"][0]["stem"])

        # Step 2: Validate with auto_fix=False -> Disk MUST NOT be mutated
        check_templates.check_templates_file_or_dir(
            target_path=[tpl_path],
            cta_path=cta_path,
            auto_fix=False,
            num_dry_run_seeds=5,
        )
        data_after_no_fix = json.loads(tpl_path.read_text(encoding="utf-8"))
        self.assertIn("\x0c", data_after_no_fix["templates"][0]["stem"], "Disk content MUST NOT be mutated when auto_fix=False!")
        self.assertIn("\x08", data_after_no_fix["templates"][0]["stem"], "Disk content MUST NOT be mutated when auto_fix=False!")
        self.assertNotIn("'y_star': y_star", data_after_no_fix["templates"][0]["generate_py"])

        # Step 3: Validate with auto_fix=True -> Disk MUST be mechanically healed
        check_templates.check_templates_file_or_dir(
            target_path=[tpl_path],
            cta_path=cta_path,
            auto_fix=True,
            num_dry_run_seeds=5,
        )
        data_after_fix = json.loads(tpl_path.read_text(encoding="utf-8"))
        self.assertNotIn("\x0c", data_after_fix["templates"][0]["stem"], "Control char \\x0c must be eliminated from disk!")
        self.assertNotIn("\x08", data_after_fix["templates"][0]["stem"], "Control char \\x08 must be eliminated from disk!")
        self.assertIn(r"\frac", data_after_fix["templates"][0]["stem"], "\\frac must be restored on disk!")
        self.assertIn(r"\beta", data_after_fix["templates"][0]["stem"], "\\beta must be restored on disk!")
        self.assertIn("'y_star': y_star", data_after_fix["templates"][0]["generate_py"], "Unexported variable y_star must be persisted to 'vars' on disk!")
        self.assertIn("Confundir la inversión de flujo con el stock de capital acumulado", data_after_fix["templates"][1]["generate_py"],
                      "Multiple_select error_rationale must be auto-populated and saved to disk!")

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
