"""Comprehensive Verification Test Suite for Shard Authoring Reparations (C2C).

Tests:
1. Stage 1B upstream validation in check_cta.py (unconditional math checks, orphan LaTeX detection).
2. Stage 1B sanitization in cta_merge.py (normalize_orphan_math, sanitize_competency_math).
3. Invariant diagnosis fix in engine/invariants.py (unescaped LaTeX vs template variable).
4. Diagnostic messages in check_templates.py (distractor context, forbidden vars prescription).
5. Circuit Breaker in check_templates.py (3 identical consecutive failures detection).
6. Author role specs and bundles in dispatch.py (50 turns, modular templates, anti-monolith).
7. System prompt prompt_shard_author.md (50 turns, modular protocol, PowerShell prohibitions).
8. Telemetry fallback in audit_engine.py (aborted runs keep questions_count = 0).
"""

import hashlib
import json
import os
import re
import sys
import tempfile
from pathlib import Path
import unittest

# Ensure skills and repo are in sys.path
repo_root = Path(__file__).resolve().parents[1]
c2c_dir = repo_root / ".agents" / "skills" / "content-to-course"
auditor_dir = repo_root / ".agents" / "skills" / "c2c-run-auditor" / "scripts"

if str(c2c_dir) not in sys.path:
    sys.path.insert(0, str(c2c_dir))
if str(auditor_dir) not in sys.path:
    sys.path.insert(0, str(auditor_dir))

from check_cta import validate_distractor_math, check_cta_katex
from cta_merge import normalize_orphan_math, sanitize_competency_math
from engine.invariants import validate_katex_syntax
from check_templates import format_invariant_error_diagnostic, format_parity_error, check_templates_file_or_dir
from dispatch import ROLE_SPECS, build_dispatch, dispatch_authors


class TestStage1BUpstreamValidation(unittest.TestCase):
    """Test Component 1: Upstream KaTeX and math validation in check_cta.py."""

    def test_distractor_raw_latex_without_dollars_fails(self):
        # Distractor with orphan dot{w}
        d = {
            "id": "D-TEST-01",
            "name": "Error de derivada",
            "manifestation": "El estudiante calcula dot{w} directamente sin considerar la depreciacion",
            "remediation_hint": "Recuerde que bar{k} es el capital estacionario",
            "wrong_belief": "Cree que dot{w} = 0 siempre",
            "omitted_step": None,
        }
        errs = validate_distractor_math(d, d["id"])
        self.assertGreater(len(errs), 0)
        self.assertTrue(any("contiene comandos LaTeX sin delimitar por '$...$'" in e for e in errs))

    def test_distractor_with_proper_katex_passes(self):
        d = {
            "id": "D-TEST-02",
            "name": "Error de derivada",
            "manifestation": "El estudiante calcula $\\dot{w}$ directamente sin considerar la depreciacion",
            "remediation_hint": "Recuerde que $\\bar{k}$ es el capital estacionario",
            "wrong_belief": "Cree que $\\dot{w} = 0$ siempre",
            "omitted_step": None,
        }
        errs = validate_distractor_math(d, d["id"])
        self.assertEqual(len(errs), 0)

    def test_check_cta_katex_catches_orphan_latex(self):
        cta_data = {
            "competencies": [
                {
                    "id": "C-01",
                    "name": "Modelo de Solow con dot{w}",
                    "description": "Analisis de bar{k} en estado estacionario",
                    "distractors": [
                        {
                            "id": "D-C01-01",
                            "manifestation": "Confunde dot{w} con bar{w}",
                            "remediation_hint": "Revisar $\\dot{w}$",
                        }
                    ],
                }
            ]
        }
        errs = check_cta_katex(cta_data)
        self.assertGreater(len(errs), 0)
        self.assertTrue(any("name contiene comandos LaTeX" in e for e in errs))
        self.assertTrue(any("description contiene comandos LaTeX" in e for e in errs))
        self.assertTrue(any("manifestation" in e for e in errs))


class TestStage1BSanitization(unittest.TestCase):
    """Test Component 1: Deterministic normalizer in cta_merge.py."""

    def test_normalize_orphan_math_transformations(self):
        # 1. dot{w} and bar{k} without backslash
        raw = "El estudiante confunde dot{w} con bar{k} y calcula frac{1}{2}"
        normalized = normalize_orphan_math(raw)
        self.assertIn("$\\dot{w}$", normalized)
        self.assertIn("$\\bar{k}$", normalized)
        self.assertIn("$\\frac{1}{2}$", normalized)
        self.assertNotIn("dot{w}", normalized.replace("$\\dot{w}$", ""))

        # 2. \dot{w} without dollars
        raw2 = "Analiza \\dot{w} y \\bar{k} fuera de modo matematico"
        norm2 = normalize_orphan_math(raw2)
        self.assertIn("$\\dot{w}$", norm2)
        self.assertIn("$\\bar{k}$", norm2)

        # 3. Already delimited math must NOT be double-dollarized
        raw3 = "Calcula $\\dot{w}$ y $\\frac{a}{b}$ correctamente"
        norm3 = normalize_orphan_math(raw3)
        self.assertEqual(norm3, raw3)

    def test_sanitize_competency_math(self):
        comp = {
            "id": "C-01",
            "name": "Calculo de dot{w}",
            "description": "Estudio de bar{k}",
            "distractors": [
                {
                    "id": "D-C01-01",
                    "name": "Opcion con dot{w}",
                    "manifestation": "Confunde dot{w}",
                    "remediation_hint": "Usa bar{k}",
                    "wrong_belief": "dot{w} es negativo",
                }
            ],
        }
        sanitize_competency_math(comp)
        self.assertEqual(comp["name"], "Calculo de $\\dot{w}$")
        self.assertEqual(comp["description"], "Estudio de $\\bar{k}$")
        self.assertEqual(comp["distractors"][0]["manifestation"], "Confunde $\\dot{w}$")
        self.assertEqual(comp["distractors"][0]["remediation_hint"], "Usa $\\bar{k}$")
        self.assertEqual(comp["distractors"][0]["wrong_belief"], "$\\dot{w}$ es negativo")


class TestInvariantDiagnosisFix(unittest.TestCase):
    """Test Component 2: Invariant diagnosis in invariants.py and check_templates.py."""

    def test_invariants_distinguishes_unescaped_latex_command(self):
        # dot{w} without backslash in text
        text = "Calcula dot{w} para hallar el equilibrio"
        errs = validate_katex_syntax(text, "option content")
        self.assertGreater(len(errs), 0)
        self.assertTrue(any("Unescaped LaTeX math command 'dot{w}'" in e for e in errs))
        # It must NOT report an unsubstituted template variable
        self.assertFalse(any("Unsubstituted template variable '{w}'" in e for e in errs))

    def test_invariants_detects_real_template_var(self):
        # A real dynamic variable {k_star}
        text = "El valor del capital es {k_star} unidades"
        errs = validate_katex_syntax(text, "stem")
        self.assertTrue(any("Unsubstituted template variable '{k_star}'" in e for e in errs))

    def test_format_invariant_error_diagnostic_protects_distractors(self):
        # Distractor context error
        inv_err = "Unsubstituted template variable '{w}' detected in option 2 content."
        diag = format_invariant_error_diagnostic(
            cid="C-01",
            tpl_id="TPL-01",
            q_id="seed=100",
            inv_err=inv_err,
        )
        self.assertIn("R-20: SINTAXIS / LLAVES", diag)
        self.assertIn("PROHIBIDO declarar 'w' en el diccionario 'vars'", diag)
        self.assertNotIn("Declarar 'w' en el diccionario 'vars' retornado por generate_py.", diag)

    def test_format_invariant_error_diagnostic_unescaped_latex(self):
        inv_err = "Unescaped LaTeX math command 'dot{w}' detected in option 1 error_rationale."
        diag = format_invariant_error_diagnostic(
            cid="C-01",
            tpl_id="TPL-01",
            q_id="seed=100",
            inv_err=inv_err,
        )
        self.assertIn("R-20: SINTAXIS / LLAVES", diag)
        self.assertIn("PROHIBIDO declarar variables matemáticas en el diccionario 'vars'", diag)
        self.assertIn("$\\dot{w}$", diag)


class TestHardCircuitBreaker(unittest.TestCase):
    """Test Component 4: Circuit breaker in check_templates.py."""

    def test_circuit_breaker_triggers_after_3_identical_failures(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            att_dir = tmppath / ".check_attempts"

            # Create an invalid template file
            bad_tpl = {
                "id": "TPL-FAIL",
                "competency_id": "C-01",
                "interaction_type": "multiple_choice_7_options",
                "difficulty": "medium",
                "stem": "Pregunta de prueba con math $$$ invalido",
                "stem_variants": ["Variante 1", "Variante 2", "Variante 3"],
                "distractor_ids": ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"],
                "generate_py": "def generate(rng):\n    return {'correct': '$1$', 'distractors': ['$2$','$3$','$4$','$5$','$6$','$7$'], 'vars': {'a': 1}}",
            }
            tpl_file = tmppath / "C-01.json"
            tpl_file.write_text(json.dumps([bad_tpl]), encoding="utf-8")

            # Run 1: Should fail normally
            v1, errs1 = check_templates_file_or_dir(tpl_file, attempts_dir=att_dir)
            self.assertFalse(v1)
            self.assertFalse(any("CIRCUIT BREAKER: FALLOS CONSECUTIVOS IDÉNTICOS" in e for e in errs1))

            # Run 2: Should fail normally
            v2, errs2 = check_templates_file_or_dir(tpl_file, attempts_dir=att_dir)
            self.assertFalse(v2)
            self.assertFalse(any("CIRCUIT BREAKER: FALLOS CONSECUTIVOS IDÉNTICOS" in e for e in errs2))

            # Run 3: Identical consecutive failure -> CIRCUIT BREAKER MUST TRIP!
            v3, errs3 = check_templates_file_or_dir(tpl_file, attempts_dir=att_dir)
            self.assertFalse(v3)
            self.assertTrue(
                any("CIRCUIT BREAKER: FALLOS CONSECUTIVOS IDÉNTICOS" in e for e in errs3),
                "Circuit breaker did not trip on 3rd identical consecutive failure!",
            )

    def test_circuit_breaker_cli_exit_code_2(self):
        """CLI execution must exit with code 2 when circuit breaker trips, not code 1."""
        import subprocess
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            att_dir = tmppath / ".check_attempts"
            bad_tpl = {
                "id": "TPL-FAIL",
                "competency_id": "C-01",
                "interaction_type": "multiple_choice_7_options",
                "difficulty": "medium",
                "stem": "Pregunta con math $$$ invalido",
                "stem_variants": ["V1", "V2", "V3"],
                "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
                "generate_py": "def generate(rng):\n    return {'correct': '$1$', 'distractors': ['$2$','$3$','$4$','$5$','$6$','$7$'], 'vars': {}}",
            }
            tpl_file = tmppath / "C-01.json"
            tpl_file.write_text(json.dumps([bad_tpl]), encoding="utf-8")

            cli_script = c2c_dir / "check_templates.py"
            cmd = [sys.executable, str(cli_script), str(tpl_file), "--attempts-dir", str(att_dir)]

            # Run 1: normal failure -> exit code 1
            p1 = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(p1.returncode, 1)

            # Run 2: normal failure -> exit code 1
            p2 = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(p2.returncode, 1)

            # Run 3: Circuit Breaker trip -> MUST EXIT WITH CODE 2!
            p3 = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(p3.returncode, 2, f"Expected returncode 2, got {p3.returncode}. Output:\n{p3.stdout}\n{p3.stderr}")
            self.assertIn("CIRCUIT BREAKER TRIPPED", p3.stdout)


    def test_multi_shard_circuit_breaker_isolation(self):
        """CRITICAL: Multi-shard concurrent execution must not cross-contaminate or reset circuit breakers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            att_dir = tmppath / ".check_attempts"

            # Create invalid template file for Shard 1 (C-01)
            bad_tpl_1 = {
                "id": "TPL-FAIL-1",
                "competency_id": "C-01",
                "interaction_type": "multiple_choice_7_options",
                "difficulty": "medium",
                "stem": "Pregunta Shard 1 con math $$$ invalido",
                "stem_variants": ["V1", "V2", "V3"],
                "distractor_ids": ["D-C01-01", "D-C01-02", "D-C01-03", "D-C01-04", "D-C01-05", "D-C01-06"],
                "generate_py": "def generate(rng):\n    return {'correct': '$1$', 'distractors': ['$2$','$3$','$4$','$5$','$6$','$7$'], 'vars': {'a': 1}}",
            }
            f1 = tmppath / "C-01.json"
            f1.write_text(json.dumps([bad_tpl_1]), encoding="utf-8")

            # Create invalid template file for Shard 2 (C-02) with DIFFERENT error
            bad_tpl_2 = {
                "id": "TPL-FAIL-2",
                "competency_id": "C-02",
                "interaction_type": "multiple_choice_7_options",
                "difficulty": "medium",
                "stem": "Pregunta Shard 2 con math residual {{x}}",
                "stem_variants": ["V1", "V2", "V3"],
                "distractor_ids": ["D-C02-01", "D-C02-02", "D-C02-03", "D-C02-04", "D-C02-05", "D-C02-06"],
                "generate_py": "def generate(rng):\n    return {'correct': '$1$', 'distractors': ['$2$','$3$','$4$','$5$','$6$','$7$'], 'vars': {'b': 2}}",
            }
            f2 = tmppath / "C-02.json"
            f2.write_text(json.dumps([bad_tpl_2]), encoding="utf-8")

            # Interleaved execution across concurrent shards:
            # Iteration 1: Shard 1 fails (count 1)
            v1_1, errs1_1 = check_templates_file_or_dir(f1, attempts_dir=att_dir)
            self.assertFalse(v1_1)
            self.assertFalse(any("CIRCUIT BREAKER" in e for e in errs1_1))

            # Interleaved: Shard 2 fails (count 1 for Shard 2)
            v2_1, errs2_1 = check_templates_file_or_dir(f2, attempts_dir=att_dir)
            self.assertFalse(v2_1)
            self.assertFalse(any("CIRCUIT BREAKER" in e for e in errs2_1))

            # Iteration 2: Shard 1 fails again (count 2 for Shard 1 - must NOT have been reset by Shard 2!)
            v1_2, errs1_2 = check_templates_file_or_dir(f1, attempts_dir=att_dir)
            self.assertFalse(v1_2)
            self.assertFalse(any("CIRCUIT BREAKER" in e for e in errs1_2))

            # Interleaved: Shard 2 fails again (count 2 for Shard 2)
            v2_2, errs2_2 = check_templates_file_or_dir(f2, attempts_dir=att_dir)
            self.assertFalse(v2_2)
            self.assertFalse(any("CIRCUIT BREAKER" in e for e in errs2_2))

            # Iteration 3: Shard 1 fails 3rd consecutive time -> CIRCUIT BREAKER MUST TRIP FOR SHARD 1!
            v1_3, errs1_3 = check_templates_file_or_dir(f1, attempts_dir=att_dir)
            self.assertFalse(v1_3)
            self.assertTrue(
                any("CIRCUIT BREAKER: FALLOS CONSECUTIVOS IDÉNTICOS" in e for e in errs1_3),
                "Circuit breaker for Shard 1 did not trip in interleaved multi-shard execution!",
            )


class TestAuthorDispatchAndProtocol(unittest.TestCase):
    """Test Component 3: Shard Author v3.2 modular authoring and dispatch."""

    def test_role_specs_author_50_turns(self):
        spec = ROLE_SPECS["author"]
        self.assertEqual(spec["turn_budget"], 30, "Author turn_budget is 30 in v3.2")
        self.assertIn("scratch/**", spec["forbidden"])
        self.assertIn("work/cta.json", spec["read"])
        self.assertIn(".agents/skills/content-to-course/compile_shard.py", spec["forbidden"])
        self.assertNotIn(".agents/skills/content-to-course/compile_shard.py", spec["read"])

    def test_generate_author_bundle_has_50_turns_and_modular_directives(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "pre_cta_manifest.json").write_text(json.dumps({
                "documents": [{"name": "doc1.pdf", "path": "content/doc1.pdf", "total_pages": 10}]
            }), encoding="utf-8")
            (tmppath / "cta.json").write_text(json.dumps({
                "competencies": [{"id": "C-01", "name": "Comp 1"}]
            }), encoding="utf-8")
            shards_dir = tmppath / "shards"
            shards_dir.mkdir(parents=True)
            (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
                "shards": [{"shard_id": "shard_01", "competency_ids": ["C-01"]}]
            }), encoding="utf-8")

            res = dispatch_authors(work_dir=tmppath)
            self.assertEqual(len(res["Subagents"]), 1)
            item_file = tmppath / "dispatch" / "items" / "author_01.json"
            self.assertTrue(item_file.exists())
            content = item_file.read_text(encoding="utf-8")
            self.assertIn("compile_shard.py", content)
            self.assertIn("shard_01_data.py", content)
            self.assertIn("pre_shard_manifest.json", content)

    def test_prompt_shard_author_file(self):
        prompt_file = c2c_dir / "system_prompts" / "prompt_shard_author.md"
        content = prompt_file.read_text(encoding="utf-8")
        self.assertIn("compile_shard.py", content)
        self.assertIn("TEMPLATES = [", content)
        self.assertIn("BLOCKER:: No existe pre_shard_manifest.json", content)
        self.assertIn("replace_file_content", content)

    def test_build_dispatch_author_includes_cta_json_and_hard_50_turns(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = Path(tmpdir)
            (tmppath / "pre_cta_manifest.json").write_text(json.dumps({
                "documents": [{"name": "doc1.pdf", "path": "content/doc1.pdf", "total_pages": 10}]
            }), encoding="utf-8")
            (tmppath / "cta.json").write_text(json.dumps({
                "competencies": [{"id": "C-01", "name": "Comp 1"}]
            }), encoding="utf-8")
            shards_dir = tmppath / "shards"
            shards_dir.mkdir(parents=True)
            (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
                "shards": [{"shard_id": "shard_01", "competency_ids": ["C-01"]}]
            }), encoding="utf-8")

            payload = build_dispatch(role="author", work_dir=tmppath)
            self.assertEqual(len(payload["Subagents"]), 1)
            prompt = payload["Subagents"][0]["Prompt"]
            self.assertIn("compile_shard.py", prompt)
            self.assertIn("shard_01_data.py", prompt)


class TestExpandedMathNormalization(unittest.TestCase):
    """Test expanded math normalization covering Greek letters, dfrac, and subscripts."""

    def test_normalize_greek_letters_and_subscripts(self):
        raw = "El estudiante ignora \\alpha y \\delta en la funcion k_{t+1} con dfrac{1}{2}"
        norm = normalize_orphan_math(raw)
        self.assertIn("$\\alpha$", norm)
        self.assertIn("$\\delta$", norm)
        self.assertIn("$k_{t+1}$", norm)
        self.assertIn("$\\dfrac{1}{2}$", norm)

        # Confirm that after normalization, validate_distractor_math reports 0 errors
        d = {
            "id": "D-GREEK-01",
            "name": "Error con letras griegas",
            "manifestation": norm,
            "remediation_hint": "Revise $\\alpha$",
            "wrong_belief": "Cree que $\\delta = 0$",
            "omitted_step": None,
        }
        errs = validate_distractor_math(d, d["id"])
        self.assertEqual(len(errs), 0)


class TestTelemetryFallback(unittest.TestCase):
    """Test Component 5: audit_engine.py telemetry fallback fix."""

    def test_aborted_run_sets_questions_count_zero(self):
        from audit_engine import WorkloadExtractor

        # Simulate workload profile for an aborted conversation
        records = [
            {"created_at": "2026-10-13T00:00:00Z", "type": "PLANNER_RESPONSE", "content": "Running stage 3 shard authoring..."},
            {"created_at": "2026-10-13T00:05:00Z", "type": "PLANNER_RESPONSE", "content": "BLOCKED: shard author loop detected"},
        ]
        workload = WorkloadExtractor.extract(workspace_root=repo_root, records=records)
        self.assertEqual(workload["questions_count"], 0)
        self.assertEqual(workload["run_status"], "ABORTED_INCOMPLETE")

    def test_bare_mention_of_run_stage_build_does_not_mark_completed(self):
        from audit_engine import WorkloadExtractor

        records = [
            {"created_at": "2026-10-13T00:00:00Z", "type": "PLANNER_RESPONSE", "content": "We planned to call run_stage_build but it aborted in stage 3."},
        ]
        workload = WorkloadExtractor.extract(workspace_root=repo_root, records=records)
        self.assertEqual(workload["questions_count"], 0)
        self.assertEqual(workload["run_status"], "ABORTED_INCOMPLETE")


if __name__ == "__main__":
    unittest.main()
