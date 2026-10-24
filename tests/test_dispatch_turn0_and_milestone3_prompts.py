"""Tests for Turn-0 Complete Context, Anti-PDF-Reading Directives, and Milestone 3 Prompts.

Validates Stream 1C implementation:
1. dispatch_authors Turn-0 complete context:
   - Injects correct_belief into competency header
   - Injects manifestation and remediation_hint into each distractor
   - Injects Turn-0 Autosufficiency directive ("AUTOSUFICIENCIA TURN-0 (CERO LECTURA INNECESARIA DE PDFs)")
   - Injects Milestone 3 4 disjoint archetypes and DRY distractor format ("D-XX-01", f"...")
   - Injects Post-PASS immediate cut directive
2. dispatch_repair attempts and pass-marker cleanup:
   - Deletes .check_attempts/pass_<shard_id>.json and sticky attempt files so Post-PASS does not block c2c_repair
3. prompt_shard_author.md (Full and Lean):
   - Specifies Milestone 3 4 disjoint archetypes (Directo, Inverso, Perturbación, Frontera)
   - Documents ultra-compact DRY distractor format
   - Documents Turn-0 Autosufficiency and Post-PASS immediate cut
   - All lean prompts in system_prompts/lean/*.md have file size <= 5,000 bytes (with author lean <= 4,750 bytes)
4. prompt_repair.md (Full and Lean):
   - Documents repairing [R-20] and explicit error_rationale or DRY inheritance
   - Documents surgical edit_file and shard_fixes/<CID>.py modular patches
   - Documents Post-PASS immediate cut
"""

from __future__ import annotations

import ast
import json
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from dispatch import dispatch_authors, dispatch_repair


class TestDispatchTurn0AndMilestone3Prompts(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="c2c_v34_stream1c_test_")
        self.work_dir = Path(self.test_dir) / "courses" / "macro_m3_test" / "work"
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.prompts_dir = SKILL_DIR / "system_prompts"
        self.lean_dir = self.prompts_dir / "lean"

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # =========================================================================
    # 1. dispatch_authors Turn-0 Context & Directives
    # =========================================================================
    def test_dispatch_authors_injects_turn0_rich_context_and_directives(self) -> None:
        """dispatch_authors injects correct_belief, manifestation, remediation_hint, and anti-reading Turn-0 directive."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "macro_m3_test",
            "documents": [
                {"name": "capitulo_01.pdf", "path": "content/capitulo_01.pdf", "total_pages": 25, "valid_page_range": [1, 25]}
            ],
        }), encoding="utf-8")

        distractors_c01 = [
            {
                "id": f"D-01-{i:02d}",
                "name": f"Error Conceptual {i}",
                "wrong_belief": f"El estudiante asume erróneamente el valor {i * 0.1}",
                "omitted_step": f"Paso {i} omitido en la derivación",
                "manifestation": f"El estudiante escribe $k = {i}$ en lugar de la fórmula canónica",
                "remediation_hint": f"Recuerde que el multiplicador depende de $c$ y $t$: revise paso {i}",
                "common_misconception_warning": f"Advertencia pedagógica {i}",
            }
            for i in range(1, 7)
        ]

        cta_data = {
            "course_id": "macro_m3_test",
            "competencies": [
                {
                    "id": "C-01",
                    "type": "knowledge",
                    "name": "Multiplicador Keynesiano",
                    "description_latex": r"Calcular multiplicador $k = \frac{1}{1 - c(1 - t)}$",
                    "correct_belief": r"El multiplicador canónico es $k = \frac{1}{1 - c(1 - t)}$ con propensión marginal $c \in (0, 1)$",
                    "evidence": [{"doc": "capitulo_01.pdf", "page": 10, "section": "2.1"}],
                    "distractors": distractors_c01,
                }
            ],
        }
        (self.work_dir / "cta.json").write_text(json.dumps(cta_data), encoding="utf-8")

        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [{"shard_id": "shard_01", "competency_ids": ["C-01"]}],
        }), encoding="utf-8")

        res = dispatch_authors(self.work_dir, pointer=False)
        self.assertEqual(len(res["Subagents"]), 1)
        prompt = res["Subagents"][0]["Prompt"]

        # 1. Correct belief in competency header
        self.assertIn("Modelo/Fórmula Correcta Canónica (correct_belief):", prompt)
        self.assertIn(r"El multiplicador canónico es $k = \frac{1}{1 - c(1 - t)}$", prompt)

        # 2. Rich distractor fields: wrong_belief, omitted_step, manifestation, remediation_hint
        for i in range(1, 7):
            self.assertIn(f"D-01-{i:02d}", prompt)
            self.assertIn(f"El estudiante asume erróneamente el valor {i * 0.1}", prompt)
            self.assertIn(f"Paso {i} omitido en la derivación", prompt)
            self.assertIn(f"Manifestación: *\"El estudiante escribe $k = {i}$ en lugar de la fórmula canónica\"*", prompt)
            self.assertIn(f"Remediation Hint: *\"Recuerde que el multiplicador depende de $c$ y $t$: revise paso {i}\"*", prompt)
            self.assertIn(f"Advertencia: *\"Advertencia pedagógica {i}\"*", prompt)

        # 3. Turn-0 Autosufficiency directive
        self.assertIn("AUTOSUFICIENCIA TURN-0 (CERO LECTURA INNECESARIA DE PDFs)", prompt)
        self.assertIn("NO abras ni leas los documentos fuente de content/ en Turno 1", prompt)
        self.assertIn("empieza directamente escribiendo shard_01_data.py", prompt)

        # 4. Milestone 3 4 disjoint archetypes & DRY format
        self.assertIn("4 arquetipos disjuntos", prompt)
        self.assertIn("1. Directo / Frontal", prompt)
        self.assertIn("2. Inverso / Diagnóstico", prompt)
        self.assertIn("3. Perturbación / Estática Comparativa", prompt)
        self.assertIn("4. Frontera / Casos Límite", prompt)
        self.assertIn("formato DRY compacto de distractores", prompt)
        self.assertIn("hereda automáticamente desde `cta.json`", prompt)

        # 5. Surgical edit_file requirement and Post-PASS cut
        self.assertIn("NO reescribas todo el archivo desde cero con `write_file`", prompt)
        self.assertIn("Corte Inmediato Post-PASS", prompt)
        self.assertIn("DONE: work/shards/shard_01.json", prompt)

    # =========================================================================
    # 2. dispatch_repair attempts and pass-marker cleanup
    # =========================================================================
    def test_dispatch_repair_clears_pass_file_and_sticky_attempts(self) -> None:
        """dispatch_repair removes .check_attempts/pass_<shard_id>.json and sticky attempt files."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "macro_m3_test",
            "documents": [{"name": "book.pdf", "path": "content/book.pdf"}],
        }), encoding="utf-8")
        (self.work_dir / "cta.json").write_text(json.dumps({"course_id": "macro_m3_test"}), encoding="utf-8")

        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [{"shard_id": "shard_02", "competency_ids": ["Hab-02"]}],
        }), encoding="utf-8")

        # Mock existing .check_attempts directory with pass marker and attempt records
        attempts_dir = self.work_dir / ".check_attempts"
        attempts_dir.mkdir(parents=True, exist_ok=True)
        pass_file = attempts_dir / "pass_shard_02.json"
        pass_file.write_text(json.dumps({"status": "PASS", "shard_id": "shard_02"}), encoding="utf-8")
        cb_file = attempts_dir / "compile_shard_02.json"
        cb_file.write_text(json.dumps({"same_error_streak": 3, "last_errors": ["R-20 error"]}), encoding="utf-8")

        self.assertTrue(pass_file.is_file())
        self.assertTrue(cb_file.is_file())

        (self.work_dir / "reports").mkdir(parents=True, exist_ok=True)
        (self.work_dir / "reports" / "templates_report.json").write_text(json.dumps({
            "results": [{"cid": "Hab-02", "status": "fail", "errors": ["LaTeX math expression has unbalanced braces"]}],
        }), encoding="utf-8")

        repair_payload = dispatch_repair(self.work_dir)
        subagents = repair_payload.get("Subagents", [])
        self.assertEqual(len(subagents), 1)

        # Confirm pass marker and attempt records were deleted
        self.assertFalse(pass_file.exists(), f"pass_shard_02.json must be unlinked by dispatch_repair!")
        self.assertFalse(cb_file.exists(), f"compile_shard_02.json must be unlinked by dispatch_repair!")

        # Verify repair prompt contents
        prompt = subagents[0]["Prompt"]
        self.assertIn("Hab-02", prompt)
        self.assertIn("shard_02", prompt)
        self.assertIn("shard_fixes/Hab-02.py", prompt)
        self.assertIn("DONE: work/shards/shard_02.json", prompt)

    # =========================================================================
    # 3. System Prompts (Full + Lean): Milestone 3 & DRY Distractors
    # =========================================================================
    def test_prompt_shard_author_specifies_milestone3_dry_archetypes_and_headroom(self) -> None:
        """prompt_shard_author.md (Full and Lean) establishes 4 archetypes, DRY format, Turn-0 autosufficiency, and <= 4,750 bytes lean."""
        full_author = (self.prompts_dir / "prompt_shard_author.md").read_text(encoding="utf-8")
        lean_author = (self.lean_dir / "prompt_shard_author.md").read_text(encoding="utf-8")

        # Full prompt checks
        self.assertIn("4 arquetipos disjuntos", full_author)
        self.assertIn("1. Directo / Frontal", full_author)
        self.assertIn("2. Inverso / Diagnóstico", full_author)
        self.assertIn("3. Perturbación / Estática Comparativa", full_author)
        self.assertIn("4. Frontera / Casos Límite", full_author)
        self.assertIn("Formato DRY Compacto de Distractores", full_author)
        self.assertIn("Autosuficiencia Turn-0 (Cero Lectura Innecesaria de PDFs)", full_author)
        self.assertIn("Corte Inmediato Post-PASS", full_author)

        # Lean prompt checks
        self.assertIn("Milestone 3 (4 Disjoint Archetypes)", lean_author)
        self.assertIn("1. Directo, 2. Inverso, 3. Perturbación, 4. Frontera", lean_author)
        self.assertIn("DRY Compact Distractors", lean_author)
        self.assertIn("Turn-0 Autosufficiency", lean_author)
        self.assertIn("Post-PASS Cut", lean_author)

        # Lean file size headroom checks
        lean_author_file = self.lean_dir / "prompt_shard_author.md"
        size_author = lean_author_file.stat().st_size
        self.assertLessEqual(size_author, 4750, f"lean/prompt_shard_author.md must be <= 4,750 bytes (got {size_author})")

        # All lean prompts strictly <= 5,000 bytes
        for lfile in self.lean_dir.glob("*.md"):
            lsize = lfile.stat().st_size
            self.assertLessEqual(lsize, 5000, f"Lean prompt {lfile.name} exceeded 5,000 bytes! (got {lsize})")

    # =========================================================================
    # 4. System Prompts (Full + Lean): Repair Prompts
    # =========================================================================
    def test_prompt_repair_specifies_r20_rationale_and_size_limits(self) -> None:
        """prompt_repair.md (Full and Lean) documents R-20 fix, error_rationale, modular patches, and size <= 5,000 bytes."""
        full_repair_file = self.prompts_dir / "prompt_repair.md"
        lean_repair_file = self.lean_dir / "prompt_repair.md"

        self.assertTrue(full_repair_file.is_file())
        self.assertTrue(lean_repair_file.is_file())

        full_repair = full_repair_file.read_text(encoding="utf-8")
        lean_repair = lean_repair_file.read_text(encoding="utf-8")

        # Full prompt repair checks
        self.assertIn("c2c_repair", full_repair)
        self.assertIn("[R-20]", full_repair)
        self.assertIn("error_rationale", full_repair)
        self.assertIn("shard_fixes/<CID>.py", full_repair)
        self.assertIn("ArtifactMetadata", full_repair)
        self.assertIn("CORTE INMEDIATO POST-PASS", full_repair)

        # Lean prompt repair checks
        self.assertIn("c2c_repair", lean_repair)
        self.assertIn("R-20", lean_repair)
        self.assertIn("error_rationale", lean_repair)
        self.assertIn("shard_fixes/<CID>.py", lean_repair)
        self.assertIn("ArtifactMetadata", lean_repair)
        self.assertIn("Post-PASS Cut", lean_repair)

        # Lean repair size limit
        self.assertLessEqual(lean_repair_file.stat().st_size, 5000)

    # =========================================================================
    # 5. Adversarial: Sanitization of None/Null/Empty and Nested KaTeX Preserved
    # =========================================================================
    def test_dispatch_authors_sanitizes_none_null_empty_and_preserves_nested_katex(self) -> None:
        """dispatch_authors sanitizes None, null, empty fields and preserves nested KaTeX formulas."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "macro_m3_test",
            "documents": [
                {"name": "doc_win.pdf", "path": "content\\subfolder\\doc_win.pdf", "total_pages": 10}
            ],
        }), encoding="utf-8")

        # C-01 has "None" strings and null fields everywhere
        distractors_c01 = [
            {
                "id": f"D-01-{i:02d}",
                "name": "None",
                "wrong_belief": None,
                "omitted_step": "None",
                "manifestation": "null",
                "remediation_hint": None,
                "common_misconception_warning": "",
            }
            for i in range(1, 7)
        ]

        nested_latex = r"Maximizar $\sum_{i=1}^n x_{i_j}^{k^2}$ sujeto a $\hat{\theta}_{ML}^{(t)} \le \alpha$"
        canonical_cb = r"$\hat{\beta}_{GLS} = (X^T \Omega^{-1} X)^{-1} X^T \Omega^{-1} y$ con $\Omega_{i_j} \ne 0$"

        cta_data = {
            "course_id": "macro_m3_test",
            "competencies": [
                {
                    "id": "C-01",
                    "type": "knowledge",
                    "name": "None",
                    "description_latex": "None",
                    "correct_belief": "None",
                    "evidence": [{"doc": "doc_win.pdf", "page": 2, "section": "None"}],
                    "distractors": distractors_c01,
                },
                {
                    "id": "C-02",
                    "type": "skill",
                    "name": "Estimación Robusta",
                    "description_latex": nested_latex,
                    "correct_belief": canonical_cb,
                    "evidence": [{"doc": "doc_win.pdf", "page": 5, "section": "3.2"}],
                    "distractors": [
                        {
                            "id": f"D-02-{i:02d}",
                            "name": f"Distractor {i}",
                            "wrong_belief": f"Error {i}",
                            "omitted_step": f"Paso {i}",
                            "manifestation": r"$\Omega_{i_j} = \delta_{ij}$ asumiendo homocedasticidad",
                            "remediation_hint": r"Revise la matriz de covarianza $\Omega$",
                        }
                        for i in range(1, 7)
                    ],
                },
            ],
        }
        (self.work_dir / "cta.json").write_text(json.dumps(cta_data), encoding="utf-8")

        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [{"shard_id": "shard_01", "competency_ids": ["C-01", "C-02"]}],
        }), encoding="utf-8")

        res = dispatch_authors(self.work_dir, pointer=False)
        self.assertEqual(len(res["Subagents"]), 1)
        prompt = res["Subagents"][0]["Prompt"]

        # In C-01:
        # 1. correct_belief line must NOT be output because it was "None"
        c01_section = prompt.split("### Competencia: `C-02`")[0]
        self.assertNotIn("Modelo/Fórmula Correcta Canónica (correct_belief):", c01_section)
        # 2. Never print literal "None" or "null" in distractor entries
        for i in range(1, 7):
            did = f"D-01-{i:02d}"
            # Name fell back to did, not literal "None"
            self.assertIn(f"- **`{did}`** (`{did}`):", c01_section)
            # wrong_belief fell back to default string, not "None"
            self.assertIn('Creencia errónea: *"Creencia errónea no especificada"*', c01_section)
            # omitted_step fell back to "N/A", not "None"
            self.assertIn("Paso omitido: `N/A`", c01_section)
            # Manifestation: *"null"* or *"None"* must NOT appear
            self.assertNotIn('Manifestación: *"null"*', c01_section)
            self.assertNotIn('Manifestación: *"None"*', c01_section)
            self.assertNotIn("Remediation Hint:", c01_section)
            self.assertNotIn("Advertencia:", c01_section)

        # In C-02:
        c02_section = prompt.split("### Competencia: `C-02`")[1]
        self.assertIn(nested_latex, c02_section)
        self.assertIn(canonical_cb, c02_section)
        self.assertIn(r"$\Omega_{i_j} = \delta_{ij}$ asumiendo homocedasticidad", c02_section)

        # Windows path normalization to POSIX forward slash
        self.assertIn("content/subfolder/doc_win.pdf", prompt)
        self.assertNotIn(r"content\subfolder\doc_win.pdf", prompt)

    # =========================================================================
    # 6. Adversarial: dispatch_repair cleans pass markers & handles missing/locked dir
    # =========================================================================
    def test_dispatch_repair_clears_competency_pass_files_and_tolerates_missing_dir(self) -> None:
        """dispatch_repair cleans pass_{shard_id}.json and pass_{cid}.json, and tolerates missing or locked .check_attempts."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "macro_m3_test",
            "documents": [{"name": "book.pdf", "path": "content/book.pdf"}],
        }), encoding="utf-8")
        (self.work_dir / "cta.json").write_text(json.dumps({"course_id": "macro_m3_test"}), encoding="utf-8")

        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [{"shard_id": "shard_03", "competency_ids": ["C-03"]}],
        }), encoding="utf-8")

        (self.work_dir / "reports").mkdir(parents=True, exist_ok=True)
        (self.work_dir / "reports" / "templates_report.json").write_text(json.dumps({
            "results": [{"cid": "C-03", "status": "fail", "errors": ["R-20 delimiter unbalance"]}],
        }), encoding="utf-8")

        # Case A: .check_attempts does NOT exist -> must execute cleanly without exception
        attempts_dir = self.work_dir / ".check_attempts"
        if attempts_dir.exists():
            shutil.rmtree(attempts_dir)
        res_a = dispatch_repair(self.work_dir)
        self.assertEqual(len(res_a["Subagents"]), 1)

        # Case B: .check_attempts exists with pass files for shard_03, C-03, and unrelated targets
        attempts_dir.mkdir(parents=True, exist_ok=True)
        pass_shard = attempts_dir / "pass_shard_03.json"
        pass_cid_dash = attempts_dir / "pass_C-03.json"
        pass_cid_under = attempts_dir / "pass_C_03.json"
        pass_comp = attempts_dir / "pass_comp_C_03.json"
        pass_unrelated = attempts_dir / "pass_shard_99.json"
        pass_unrelated_cid = attempts_dir / "pass_C-99.json"

        for pf in [pass_shard, pass_cid_dash, pass_cid_under, pass_comp, pass_unrelated, pass_unrelated_cid]:
            pf.write_text(json.dumps({"status": "PASS"}), encoding="utf-8")

        res_b = dispatch_repair(self.work_dir)
        self.assertEqual(len(res_b["Subagents"]), 1)

        # Confirm target pass files are deleted
        self.assertFalse(pass_shard.exists())
        self.assertFalse(pass_cid_dash.exists())
        self.assertFalse(pass_cid_under.exists())
        self.assertFalse(pass_comp.exists())
        # Confirm unrelated pass files remain untouched
        self.assertTrue(pass_unrelated.exists())
        self.assertTrue(pass_unrelated_cid.exists())

    # =========================================================================
    # 7. AST Validation: All Python Code Blocks in Prompts are Valid Syntax
    # =========================================================================
    def test_all_python_snippets_in_prompts_are_valid_ast(self) -> None:
        """Every python code block in prompt_shard_author.md and prompt_repair.md (Full + Lean) parses as valid Python AST."""
        files_to_check = [
            self.prompts_dir / "prompt_shard_author.md",
            self.lean_dir / "prompt_shard_author.md",
            self.prompts_dir / "prompt_repair.md",
            self.lean_dir / "prompt_repair.md",
        ]

        total_blocks_checked = 0
        for fpath in files_to_check:
            if not fpath.is_file():
                continue
            text = fpath.read_text(encoding="utf-8")
            blocks = re.findall(r"```python\s*(.*?)```", text, re.DOTALL)
            for i, b in enumerate(blocks):
                code_snippet = b.strip()
                if not code_snippet:
                    continue
                try:
                    ast.parse(code_snippet)
                    total_blocks_checked += 1
                except SyntaxError:
                    # Try parsing as eval mode for standalone dictionary or tuple expressions
                    try:
                        ast.parse(code_snippet, mode="eval")
                        total_blocks_checked += 1
                    except SyntaxError as e:
                        self.fail(f"Syntax error in code block {i} of {fpath.name}: {e}\nSnippet:\n{code_snippet}")

        self.assertGreaterEqual(total_blocks_checked, 5, f"Expected at least 5 python code blocks across prompts, checked {total_blocks_checked}")

    # =========================================================================
    # 8. Domain-Agnostic and CLI Backward Compatibility Checks
    # =========================================================================
    def test_dispatch_and_prompts_are_100pct_domain_agnostic(self) -> None:
        """dispatch.py and repair prompts must not contain hardcoded course identifiers."""
        dispatch_code = (SKILL_DIR / "dispatch.py").read_text(encoding="utf-8")
        # Ensure no specific academic courses are hardcoded
        forbidden_course_terms = ["macroeconomia", "econometria", "microeconomia", "termodinamica_clausius"]
        for term in forbidden_course_terms:
            self.assertNotIn(term, dispatch_code.lower())

    def test_dispatch_authors_cli_and_pointer_backward_compatibility(self) -> None:
        """dispatch_authors works seamlessly with pointer=True and pointer=False, preserving backwards-compatibility."""
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "course_id": "agnostic_test",
            "documents": [{"name": "spec.pdf", "path": "content/spec.pdf"}],
        }), encoding="utf-8")
        (self.work_dir / "cta.json").write_text(json.dumps({
            "competencies": [{"id": "Hab-01", "name": "Atomic Operation", "type": "skill"}],
        }), encoding="utf-8")
        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [{"shard_id": "shard_01", "competency_ids": ["Hab-01"]}],
        }), encoding="utf-8")

        # 1. Pointer mode True (default in orchestrations)
        res_ptr = dispatch_authors(self.work_dir, pointer=True)
        self.assertEqual(len(res_ptr["Subagents"]), 1)
        ptr_prompt = res_ptr["Subagents"][0]["Prompt"]
        self.assertIn("view_file", ptr_prompt)
        self.assertIn("author_01.json", ptr_prompt)

        # 2. Pointer mode False (inline full prompt)
        res_full = dispatch_authors(self.work_dir, pointer=False)
        self.assertEqual(len(res_full["Subagents"]), 1)
        full_prompt = res_full["Subagents"][0]["Prompt"]
        self.assertIn("Asignación de Tarea: Shard Exercise Author", full_prompt)
        self.assertIn("Hab-01", full_prompt)


if __name__ == "__main__":
    unittest.main()
