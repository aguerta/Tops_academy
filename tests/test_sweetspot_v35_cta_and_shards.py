"""Cross-Contract Integration Suite for C2C v3.5: Sweet-Spot CTA, Shards, Hook Guard & Milestone 3.

Validates the full cross-boundary integration between:
1. Stream 1A: compile_cta.py Tier-0 Auto-Heal, dynamic threshold directives, .check_attempts persistence, and modular cta_fixes/.
2. Stream 1B: compile_shard.py [M3-ARCHETYPES] gate, error_count aggregation, threshold directives, and compact helper pattern.
3. Stream 1C: c2c_hook_guard.py Rule B (Post-PASS Cut) and Rule C (Official Threshold < 6 write isolation).
4. Stream 1D: dispatch.py min_archetypes: 4 stamping, --min-archetypes 4 in compile_cmd, and Turn-0 specifications.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure content-to-course skill directory is in sys.path
REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from compile_cta import compile_cta, render_compact_cta_errors
from compile_shard import compile_shard
from c2c_hook_guard import process_hook
from dispatch import dispatch_authors, get_type_definitions


# ==============================================================================
# Sample CTA Source with Bare LaTeX (v5 Asymptotic Statistics scenario)
# ==============================================================================

SAMPLE_CTA_SOURCE_BARE_LATEX = '''# part_01_data.py
COURSE_ID = "asymptotic_stats"
COURSE_TITLE = "Estadística Asintótica v5"

COMPETENCIES = [
    (
        "concept",
        "C-01",
        "Consistencia y Convergencia Asintótica",
        # Bare LaTeX expressions as seen in v5:
        r"La propiedad fundamental establece que \\lim_{n\\to\\infty} \\frac{\\sigma^2}{n} = 0 para la varianza muestral.",
        "Understand",
        "asymptotic_notes.pdf",
        1,
        [],
        [
            (
                "Confundir límite con valor finito no nulo",
                r"Asume erróneamente que \\lim_{n\\to\\infty} \\frac{\\sigma^2}{n} = \\sigma^2 constante.",
                r"El límite converge a cero: $\\lim_{n\\to\\infty} \\frac{\\sigma^2}{n} = 0$.",
                "Varianza residual constante",
                "Revisar el comportamiento asintótico cuando $n \\to \\infty$.",
                None,
            ),
            (
                "Error en escala de dispersión estándar",
                r"Confunde \\sigma con la varianza \\sigma^2 al calcular.",
                r"La desviación estándar es $\\sigma$ y la varianza es $\\sigma^2$.",
                "Escala incorrecta",
                "Distinguir dispersión lineal de dispersión cuadrática.",
                None,
            ),
            (
                "Omisión del factor de escala muestral",
                r"Usa \\frac{\\sigma^2}{n} sin dividir por el tamaño muestral.",
                r"La varianza muestral promedio es $\\frac{\\sigma^2}{n}$.",
                "Magnitud de varianza",
                "Verificar la normalización por $n$.",
                None,
            ),
            (
                "Falsa equivalencia de estimadores asintóticos",
                r"Asume equivalencia asintótica universal sin regularidad.",
                r"La equivalencia asintótica requiere condiciones de regularidad de Cramér-Rao.",
                "Equivalencia no uniforme",
                "Revisar hipótesis de regularidad estadística.",
                None,
            ),
            (
                "Inversión de condiciones de frontera estocástica",
                r"Invierte el orden de los límites en la sucesión de estimadores.",
                r"El límite estocástico debe evaluarse en el soporte paramétrico.",
                "Soporte estocástico invertido",
                "Comprobar convergencia estocástica en probabilidad.",
                None,
            ),
            (
                "Confusión entre probabilidad y distribución",
                r"Confunde convergencia en probabilidad con normalidad asintótica.",
                r"La normalidad asintótica requiere escalamiento por $\\sqrt{n}$.",
                "Distribución límite no estandarizada",
                "Diferenciar convergencia en probabilidad de convergencia en ley.",
                None,
            ),
        ],
    ),
    (
        "skill",
        "Hab-01",
        "Cálculo de la Varianza Asintótica del Estimador",
        r"Calcular la varianza asintótica del estimador bajo el Teorema Central del Límite: $\\text{Avar}(\\hat{\\theta}_n)$.",
        "Apply",
        "asymptotic_notes.pdf",
        2,
        ["C-01"],
        [
            (
                "Uso de factor de escala muestral sin raíz cuadrada",
                r"Escalar por $n$ en lugar de $\\sqrt{n}$ en la normalización.",
                r"El factor correcto de escalamiento asintótico es $\\sqrt{n}(\\hat{\\theta}_n - \\theta)$.",
                "Factor de escala lineal",
                "El TLC exige multiplicar por la raíz del tamaño muestral.",
                "Omitir aplicar la raíz cuadrada al factor de normalización $n$",
            ),
            (
                "Inversión de la matriz de información de Fisher",
                r"Invertir la información de Fisher en el numerador en lugar del denominador.",
                r"La cota inferior de varianza asintótica es $I(\\theta)^{-1}$.",
                "Matriz no invertida",
                "La varianza asintótica óptima es el inverso de la información.",
                "Omitir invertir la matriz de información de Fisher esperada",
            ),
            (
                "Omisión del jacobiano en el método Delta multivariado",
                r"Aplicar transformación no lineal sin gradiente jacobiano.",
                r"El método Delta requiere la forma cuadrática $\\nabla g(\\theta)' \\Sigma \\nabla g(\\theta)$.",
                "Varianza sin jacobiano",
                "Multiplicar por el vector gradiente de la transformación.",
                None,
            ),
            (
                "Error en la derivada de la función de enlace",
                r"Derivar incorrectamente la función de enlace en el modelo no lineal.",
                r"La derivada de la función de enlace debe evaluarse en el verdadero valor del parámetro.",
                "Derivada incorrecta",
                "Verificar la regla de la cadena en la transformación.",
                None,
            ),
            (
                "Confusión entre matriz hessiana y producto exterior",
                r"Usar el producto exterior de gradientes sin matriz hessiana observada.",
                r"Bajo correcta especificación ambas matrices convergen asintóticamente.",
                "Discrepancia en covarianza robusta",
                "Comprobar la igualdad de la información de Fisher.",
                None,
            ),
            (
                "Evaluación fuera del soporte paramétrico admisible",
                r"Evaluar la varianza asintótica en la frontera del espacio paramétrico.",
                r"El Teorema Central del Límite estándar exige parámetros en el interior del espacio.",
                "Varianza degenerada",
                "Verificar que el parámetro pertenezca al interior del soporte.",
                None,
            ),
        ],
    ),
]
'''

BROKEN_CTA_SOURCE_3_ERRORS = '''# part_01_data.py
COURSE_ID = "asymptotic_stats"
COURSE_TITLE = "Estadística Asintótica"

COMPETENCIES = [
    (
        "concept",
        "C-01",
        "Consistencia del Estimador",
        r"Definición matemática formal con $\\sigma$.",
        "Understand",
        "asymptotic_notes.pdf",
        1,
        [],
        [
            ("D1", r"$\\frac{1}$", r"$\\sigma$", "Cero", "rh1", None),  # Error 1: KaTeX macro \\frac requires 2 args
            ("D2", r"$\\frac{2}$", r"$\\sigma$", "Cero", "rh2", None),  # Error 2: KaTeX macro \\frac requires 2 args
            ("D3", r"$\\frac{3}$", r"$\\sigma$", "Cero", "rh3", None),  # Error 3: KaTeX macro \\frac requires 2 args
            ("D4", r"$\\sigma$", r"$\\sigma$", "Cero", "rh4", None),
            ("D5", r"$\\sigma$", r"$\\sigma$", "Cero", "rh5", None),
            ("D6", r"$\\sigma$", r"$\\sigma$", "Cero", "rh6", None),
        ],
    ),
    (
        "skill",
        "Hab-01",
        "Cálculo de Varianza Asintótica",
        r"Cálculo analítico con $\\text{Avar}$.",
        "Apply",
        "asymptotic_notes.pdf",
        2,
        ["C-01"],
        [
            ("D1", r"$\\sigma$", r"$\\sigma$", "Cero", "rh1", "Omitir raíz cuadrada de n"),
            ("D2", r"$\\sigma$", r"$\\sigma$", "Cero", "rh2", "Omitir invertir información"),
            ("D3", r"$\\sigma$", r"$\\sigma$", "Cero", "rh3", None),
            ("D4", r"$\\sigma$", r"$\\sigma$", "Cero", "rh4", None),
            ("D5", r"$\\sigma$", r"$\\sigma$", "Cero", "rh5", None),
            ("D6", r"$\\sigma$", r"$\\sigma$", "Cero", "rh6", None),
        ],
    ),
]

# Padding lines to ensure file exceeds 40 lines:
# Line 43
# Line 44
# Line 45
# Line 46
# Line 47
# Line 48
# Line 49
# Line 50
'''

BROKEN_CTA_SOURCE_6_ERRORS = '''# part_01_data.py
COURSE_ID = "asymptotic_stats"
COURSE_TITLE = "Estadística Asintótica"

COMPETENCIES = [
    (
        "concept",
        "C-01",
        "Consistencia del Estimador",
        r"Definición matemática formal con $\\sigma$.",
        "Understand",
        "asymptotic_notes.pdf",
        1,
        [],
        [
            ("D1", r"$\\frac{1}$", r"$\\sigma$", "Cero", "rh1", None),  # Error 1
            ("D2", r"$\\frac{2}$", r"$\\sigma$", "Cero", "rh2", None),  # Error 2
            ("D3", r"$\\frac{3}$", r"$\\sigma$", "Cero", "rh3", None),  # Error 3
            ("D4", r"$\\frac{4}$", r"$\\sigma$", "Cero", "rh4", None),  # Error 4
            ("D5", r"$\\frac{5}$", r"$\\sigma$", "Cero", "rh5", None),  # Error 5
            ("D6", r"$\\frac{6}$", r"$\\sigma$", "Cero", "rh6", None),  # Error 6
        ],
    ),
]

# Padding lines to ensure file exceeds 40 lines:
# Line 32
# Line 33
# Line 34
# Line 35
# Line 36
# Line 37
# Line 38
# Line 39
# Line 40
# Line 41
# Line 42
'''

BROKEN_CTA_SOURCE_SYNTAX_ERROR = '''# part_01_data.py
COURSE_ID = "asymptotic_stats"
COURSE_TITLE = "Estadística Asintótica"

COMPETENCIES = [
    (
        "concept",
        "C-01",
        "Consistencia del Estimador",
        # Incomplete tuple with unclosed parenthesis/brackets causing genuine SyntaxError:
        r"Definición formal",
        "Understand",
        "asymptotic_notes.pdf",
        1,
        [],
        [
            ("D1", r"$\\sigma$", r"$\\sigma$", "Cero", "rh1", None),
''' + ("# Padding line to ensure file exceeds 40 lines\n" * 45)



class TestSweetSpotCrossContractCTA(unittest.TestCase):
    """End-to-end integration tests between compile_cta.py and c2c_hook_guard.py."""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="c2c_v35_sweetspot_cta_")
        self.course_id = "asymptotic_stats"
        self.work_dir = Path(self.test_dir) / "courses" / self.course_id / "work"
        self.cta_parts_dir = self.work_dir / "cta_parts"
        self.cta_fixes_dir = self.work_dir / "cta_fixes"
        self.check_attempts_dir = self.work_dir / ".check_attempts"

        self.cta_parts_dir.mkdir(parents=True, exist_ok=True)
        self.cta_fixes_dir.mkdir(parents=True, exist_ok=True)
        self.check_attempts_dir.mkdir(parents=True, exist_ok=True)

        self.lock_file = Path(self.test_dir) / ".c2c_subagent_lock.json"
        self.director_id = "director-conv-uuid"
        self.worker_id = "worker-cta-uuid"

        self.lock_data = {
            "active": True,
            "director_conversation_id": self.director_id,
            "course_id": self.course_id,
            "work_dir": str(self.work_dir),
            "exempt_conversation_ids": [],
        }
        self.lock_file.write_text(json.dumps(self.lock_data, indent=2), encoding="utf-8")

        # Manifest
        self.manifest_file = self.work_dir / "pre_cta_manifest.json"
        self.manifest_data = {
            "course_id": self.course_id,
            "title": "Estadística Asintótica",
            "files": [
                {
                    "doc": "asymptotic_notes.pdf",
                    "name": "asymptotic_notes.pdf",
                    "valid_page_range": [1, 10],
                    "total_pages": 10,
                }
            ],
        }
        self.manifest_file.write_text(json.dumps(self.manifest_data, indent=2), encoding="utf-8")

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def _find_check_file(self, filename: str) -> Optional[Path]:
        """Locates check file across work/.check_attempts and cta_parts/.check_attempts."""
        for d in (self.cta_parts_dir / ".check_attempts", self.work_dir / ".check_attempts"):
            p = d / filename
            if p.is_file():
                return p
        return None

    def test_cta_tier0_autoheal_generates_pass_and_hook_guard_rule_b_blocks_writes_and_edits(self) -> None:
        """1. CTA Integration: Tier-0 Auto-Heal of bare LaTeX passes with 0 errors and generates pass_cta_<id>.json.
        Then c2c_hook_guard.py (Rule B) blocks subsequent write_file and edit_file on part_01_data.py.
        """
        part_01_py = self.cta_parts_dir / "part_01_data.py"
        part_01_py.write_text(SAMPLE_CTA_SOURCE_BARE_LATEX, encoding="utf-8")

        # Compile CTA part_01
        ok, cta_dict, errors, elapsed = compile_cta(
            cta_data_path=part_01_py,
            output_dir=self.cta_parts_dir,
            manifest_path=self.manifest_file,
            output_json_name="part_01.json",
            is_part=True,
        )

        self.assertTrue(ok, f"Expected clean pass with Tier-0 Auto-Heal, got errors: {errors}")
        self.assertEqual(len(errors), 0)

        # Verify healed LaTeX in competency 0 distractor 1
        d1 = cta_dict["competencies"][0]["distractors"][1]
        self.assertIn("$", d1["wrong_belief"], "Expected bare LaTeX to be healed and wrapped in $...$")

        # Verify pass_cta_part_01.json created
        pass_file = self._find_check_file("pass_cta_part_01.json")
        self.assertIsNotNone(pass_file, "Expected pass_cta_part_01.json to exist on disk")
        pass_data = json.loads(pass_file.read_text(encoding="utf-8"))
        self.assertEqual(pass_data.get("status"), "PASS")
        self.assertEqual(pass_data.get("target_id"), "part_01")

        # Hook Guard Rule B: Verify write_file on part_01_data.py is blocked
        write_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(part_01_py),
                    "Content": "# Overwrite attempt post-pass",
                },
            },
        }
        res_write = process_hook(write_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_write.get("decision"), "deny")
        self.assertIn("BLOCKER:: El módulo CTA part_01 ya aprobó todas las validaciones estrictas ([+] PASS)", res_write.get("reason", ""))
        self.assertIn("emite DONE inmediatamente", res_write.get("reason", ""))

        # Hook Guard Rule B: Verify edit_file on part_01_data.py is ALSO blocked
        edit_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "edit_file",
                "args": {
                    "Path": str(part_01_py),
                    "Target": "Estadística Asintótica v5",
                    "Replacement": "Estadística Asintótica v5 Modificado",
                },
            },
        }
        res_edit = process_hook(edit_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_edit.get("decision"), "deny")
        self.assertIn("BLOCKER:: El módulo CTA part_01 ya aprobó todas las validaciones estrictas ([+] PASS)", res_edit.get("reason", ""))

    def test_cta_failure_under_threshold_records_error_count_and_hook_guard_rule_c_enforces_edit_file(self) -> None:
        """2. CTA Integration: When compile_cta.py fails with 1 <= error_count < 6 (e.g. 3 structural errors):
        - Records error_count: 3 in .check_attempts/compile_cta_part_01.json
        - Emits [UMBRAL OFICIAL < 6 ERRORES (3/5)]
        - c2c_hook_guard.py (Rule C) blocks write_file on part_01_data.py while allowing edit_file and cta_fixes/<CID>.py.
        """
        part_01_py = self.cta_parts_dir / "part_01_data.py"
        part_01_py.write_text(BROKEN_CTA_SOURCE_3_ERRORS, encoding="utf-8")
        self.assertGreaterEqual(len(BROKEN_CTA_SOURCE_3_ERRORS.splitlines()), 40)

        ok, cta_dict, errors, elapsed = compile_cta(
            cta_data_path=part_01_py,
            output_dir=self.cta_parts_dir,
            manifest_path=self.manifest_file,
            output_json_name="part_01.json",
            is_part=True,
            allow_degrade=False,
        )

        self.assertFalse(ok)
        self.assertEqual(len(errors), 3, f"Expected exactly 3 errors, got {len(errors)}: {errors}")

        # Check attempts state
        att_file = self._find_check_file("compile_cta_part_01.json")
        self.assertIsNotNone(att_file, "Expected compile_cta_part_01.json to exist on disk")
        att_data = json.loads(att_file.read_text(encoding="utf-8"))
        self.assertEqual(att_data.get("error_count"), 3)
        self.assertFalse(att_data.get("has_syntax_error"))

        # Diagnostic rendered output
        rendered = render_compact_cta_errors(
            errors,
            data_filename=str(part_01_py),
            consolidated=True,
            work_dir=self.work_dir,
        )
        self.assertIn("[UMBRAL OFICIAL < 6 ERRORES (3/5)]", rendered)
        self.assertIn("edit_file", rendered)
        self.assertIn("PROHIBIDO reescribir todo el archivo", rendered)

        # Hook Guard Rule C: write_file on part_01_data.py is DENIED
        write_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(part_01_py),
                    "Content": "# Complete rewrite attempt under threshold",
                },
            },
        }
        res_write = process_hook(write_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_write.get("decision"), "deny")
        self.assertIn("BLOCKER:: El archivo part_01_data.py ya fue compilado", res_write.get("reason", ""))
        self.assertIn("registra 3 errores (< 6, umbral oficial)", res_write.get("reason", ""))
        self.assertIn("usa edit_file quirúrgico (replace_file_content) sobre las líneas reportadas", res_write.get("reason", ""))
        self.assertIn("o escribe un parche modular aislado en work/cta_fixes/<CID>.py", res_write.get("reason", ""))

        # Hook Guard Rule C: edit_file on part_01_data.py is ALLOWED
        edit_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "edit_file",
                "args": {
                    "Path": str(part_01_py),
                    "Target": r"$\frac{1}$",
                    "Replacement": r"$\frac{1}{2}$",
                },
            },
        }
        res_edit = process_hook(edit_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_edit.get("decision"), "allow")

        # Hook Guard Rule C: modular fix in cta_fixes/C-01.py is ALLOWED
        fix_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(self.cta_fixes_dir / "C-01.py"),
                    "Content": "# Modular fix for C-01",
                },
            },
        }
        res_fix = process_hook(fix_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_fix.get("decision"), "allow")

    def test_cta_failure_over_threshold_allows_full_rewrite(self) -> None:
        """3. CTA Integration: When compile_cta.py fails with error_count >= 6:
        - Emits [UMBRAL OFICIAL >= 6 ERRORES]
        - c2c_hook_guard.py allows write_file on part_01_data.py.
        """
        part_01_py = self.cta_parts_dir / "part_01_data.py"
        part_01_py.write_text(BROKEN_CTA_SOURCE_6_ERRORS, encoding="utf-8")

        ok, cta_dict, errors, elapsed = compile_cta(
            cta_data_path=part_01_py,
            output_dir=self.cta_parts_dir,
            manifest_path=self.manifest_file,
            output_json_name="part_01.json",
            is_part=True,
            allow_degrade=False,
        )

        self.assertFalse(ok)
        self.assertGreaterEqual(len(errors), 6)

        att_file = self._find_check_file("compile_cta_part_01.json")
        self.assertIsNotNone(att_file)
        att_data = json.loads(att_file.read_text(encoding="utf-8"))
        self.assertGreaterEqual(att_data.get("error_count", 0), 6)

        rendered = render_compact_cta_errors(
            errors,
            data_filename=str(part_01_py),
            consolidated=True,
            work_dir=self.work_dir,
        )
        self.assertIn(f"[UMBRAL OFICIAL >= 6 ERRORES ({len(errors)})]", rendered)

        # Hook Guard Rule C: write_file on part_01_data.py is ALLOWED for rescue rewrite
        write_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(part_01_py),
                    "Content": "# Fresh rewrite after >= 6 errors",
                },
            },
        }
        res_write = process_hook(write_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_write.get("decision"), "allow")

    def test_cta_syntax_error_recovery_lifecycle_with_hook_guard(self) -> None:
        """4. CTA Cross-Contract Edge Case: Syntax error recovery lifecycle.
        - Unparseable source in part_01_data.py causes compile_cta.py to record has_syntax_error=True and error_count=1.
        - c2c_hook_guard.py allows write_file full overwrite to unbreak the file (bypassing Rule C rewrite restriction).
        - After writing valid code, compile_cta.py produces [+] PASS and writes pass_cta_part_01.json.
        - c2c_hook_guard.py immediately locks down part_01_data.py under Rule B (Post-PASS Cut).
        """
        part_01_py = self.cta_parts_dir / "part_01_data.py"
        part_01_py.write_text(BROKEN_CTA_SOURCE_SYNTAX_ERROR, encoding="utf-8")
        self.assertGreaterEqual(len(BROKEN_CTA_SOURCE_SYNTAX_ERROR.splitlines()), 40)

        ok, cta_dict, errors, elapsed = compile_cta(
            cta_data_path=part_01_py,
            output_dir=self.cta_parts_dir,
            manifest_path=self.manifest_file,
            output_json_name="part_01.json",
            is_part=True,
            allow_degrade=False,
        )

        self.assertFalse(ok)
        self.assertTrue(any("Syntax" in str(e) or "error" in str(e) for e in errors), f"Expected syntax error, got: {errors}")

        att_file = self._find_check_file("compile_cta_part_01.json")
        self.assertIsNotNone(att_file)
        att_data = json.loads(att_file.read_text(encoding="utf-8"))
        self.assertTrue(att_data.get("has_syntax_error"), "Expected has_syntax_error=True in check_attempts")
        self.assertEqual(att_data.get("error_count"), 1)

        # Hook Guard: write_file MUST be allowed because has_syntax_error=True even though lines >= 40 and error_count < 6
        write_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(part_01_py),
                    "Content": SAMPLE_CTA_SOURCE_BARE_LATEX,
                },
            },
        }
        res_write = process_hook(write_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_write.get("decision"), "allow", f"Expected allow on syntax error recovery, got: {res_write}")

        # Worker writes valid healed code
        part_01_py.write_text(SAMPLE_CTA_SOURCE_BARE_LATEX, encoding="utf-8")

        # Re-compilation succeeds to PASS
        ok_re, cta_dict_re, errors_re, elapsed_re = compile_cta(
            cta_data_path=part_01_py,
            output_dir=self.cta_parts_dir,
            manifest_path=self.manifest_file,
            output_json_name="part_01.json",
            is_part=True,
            allow_degrade=False,
        )
        self.assertTrue(ok_re, f"Expected successful pass after syntax fix, got errors: {errors_re}")
        self.assertEqual(len(errors_re), 0)

        # pass_cta_part_01.json exists
        pass_file = self._find_check_file("pass_cta_part_01.json")
        self.assertIsNotNone(pass_file)
        pass_data = json.loads(pass_file.read_text(encoding="utf-8"))
        self.assertEqual(pass_data.get("status"), "PASS")

        # Post-PASS lockdown: Hook Guard Rule B blocks further write_file and edit_file
        res_blocked_write = process_hook(write_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_blocked_write.get("decision"), "deny")
        self.assertIn("BLOCKER:: El módulo CTA part_01 ya aprobó", res_blocked_write.get("reason", ""))

        edit_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "edit_file",
                "args": {
                    "Path": str(part_01_py),
                    "Target": "Estadística Asintótica",
                    "Replacement": "Estadística Asintótica Modificada",
                },
            },
        }
        res_blocked_edit = process_hook(edit_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_blocked_edit.get("decision"), "deny")
        self.assertIn("BLOCKER:: El módulo CTA part_01 ya aprobó", res_blocked_edit.get("reason", ""))



class TestSweetSpotCrossContractShards(unittest.TestCase):
    """End-to-end integration tests between compile_shard.py, dispatch_authors, and c2c_hook_guard.py."""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="c2c_v35_sweetspot_shards_")
        self.course_id = "asymptotic_stats"
        self.work_dir = Path(self.test_dir) / "courses" / self.course_id / "work"
        self.shards_dir = self.work_dir / "shards"
        self.templates_dir = self.work_dir / "templates"
        self.shard_fixes_dir = self.shards_dir / "shard_fixes"
        self.check_attempts_dir = self.work_dir / ".check_attempts"

        self.shards_dir.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.shard_fixes_dir.mkdir(parents=True, exist_ok=True)
        self.check_attempts_dir.mkdir(parents=True, exist_ok=True)

        self.lock_file = Path(self.test_dir) / ".c2c_subagent_lock.json"
        self.director_id = "director-conv-uuid"
        self.worker_id = "worker-author-uuid"

        self.lock_data = {
            "active": True,
            "director_conversation_id": self.director_id,
            "course_id": self.course_id,
            "work_dir": str(self.work_dir),
            "exempt_conversation_ids": [],
        }
        self.lock_file.write_text(json.dumps(self.lock_data, indent=2), encoding="utf-8")

        # cta.json
        self.cta_payload = {
            "competencies": [
                {
                    "id": "C-06",
                    "name": "Estimación Asintótica de Máxima Verosimilitud",
                    "type": "skill",
                    "distractors": [
                        {"id": "D-C06-01", "remediation_hint": "Considere la varianza asintótica en la cota de Cramér-Rao."},
                        {"id": "D-C06-02", "remediation_hint": "Verifique el inverso de la información de Fisher observada."},
                        {"id": "D-C06-03", "remediation_hint": "Compruebe la normalización adecuada bajo la raíz cuadrada de n."},
                        {"id": "D-C06-04", "remediation_hint": "Evalúe las condiciones de regularidad de las derivadas del log-verosimilitud."},
                        {"id": "D-C06-05", "remediation_hint": "Revise el sesgo de segundo orden del estimador extremo."},
                        {"id": "D-C06-06", "remediation_hint": "Verifique la convergencia uniforme en probabilidad del gradiente."},
                    ],
                }
            ]
        }
        (self.work_dir / "cta.json").write_text(json.dumps(self.cta_payload, indent=2), encoding="utf-8")

        # pre_cta_manifest.json
        self.pre_cta_manifest = {
            "course_id": self.course_id,
            "title": "Estadística Asintótica",
            "documents": [{"doc_name": "asymptotic_notes.pdf", "path": "content/asymptotic_notes.pdf"}],
        }
        (self.work_dir / "pre_cta_manifest.json").write_text(json.dumps(self.pre_cta_manifest, indent=2), encoding="utf-8")

        # pre_shard_manifest.json without min_archetypes initially
        self.initial_shard_manifest = {
            "shards": [
                {
                    "shard_id": "shard_09",
                    "competency_ids": ["C-06"],
                    "shard_data_path": str((self.shards_dir / "shard_09_data.py").resolve().as_posix()),
                    "templates_dir": str(self.templates_dir.resolve().as_posix()),
                    "competencies": self.cta_payload["competencies"],
                }
            ]
        }
        (self.shards_dir / "pre_shard_manifest.json").write_text(
            json.dumps(self.initial_shard_manifest, indent=2), encoding="utf-8"
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_dispatch_authors_stamps_min_archetypes_and_injected_in_compile_cmd(self) -> None:
        """1. Shard Integration: dispatch_authors stamps min_archetypes: 4 in pre_shard_manifest.json
        and includes --min-archetypes 4 in compile_cmd.
        """
        dispatch_authors(self.work_dir, pointer=True)

        # Verify stamping in pre_shard_manifest.json
        manifest_on_disk = json.loads((self.shards_dir / "pre_shard_manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest_on_disk.get("min_archetypes"), 4, "Root min_archetypes must be 4")
        self.assertEqual(manifest_on_disk["shards"][0].get("min_archetypes"), 4, "Shard item min_archetypes must be 4")

        # Verify compile_cmd in item file
        item_file = self.work_dir / "dispatch" / "items" / "author_09.json"
        self.assertTrue(item_file.is_file(), f"Missing item file: {item_file}")
        item_data = json.loads(item_file.read_text(encoding="utf-8"))
        compile_cmd = item_data.get("compile_command", "")
        self.assertIn("--min-archetypes 4", compile_cmd, f"compile_cmd missing --min-archetypes 4: {compile_cmd}")
        self.assertIn("--strict", compile_cmd)
        self.assertIn("--shard shard_09", compile_cmd)

    def test_shard_single_tuple_fails_m3_archetypes_and_hook_guard_rule_c_enforces_edit_file(self) -> None:
        """2. Shard Integration: When a shard emits only 1 tuple per competency (like shard_09_data.py in v5):
        - compile_shard.py fails with [M3-ARCHETYPES]
        - Records error_count (< 6) in .check_attempts/compile_shard_09.json
        - c2c_hook_guard.py blocks full write_file and instructs to use edit_file or shard_fixes/<CID>.py.
        """
        shard_09_py = self.shards_dir / "shard_09_data.py"
        # 1-tuple legacy implementation with >= 40 lines
        single_tuple_code = '''# shard_09_data.py
"""Exercise templates for shard_09 (v5 legacy 1-tuple implementation)."""
import random
import math

# Preamble functions
def gen_c06(rng):
    n = rng.randint(20, 200)
    ans = n * 2
    deltas = [-5, 5, 10, -10, 15, -15]
    d_ids = ["D-C06-01", "D-C06-02", "D-C06-03", "D-C06-04", "D-C06-05", "D-C06-06"]
    v_dict = {"n": n, "ans": ans}
    distractors = []
    for i, (d, did) in enumerate(zip(deltas, d_ids), 1):
        v_dict[f"d{i}"] = ans + d
        distractors.append({"value": r"$\\text{Avar} = @d" + str(i) + r"@$", "distractor_id": did})
    return {
        "vars": v_dict,
        "correct": r"$\\text{Avar} = @ans@$",
        "distractors": distractors,
    }

def ver_c06(res):
    return res["vars"]["ans"] == res["vars"]["n"] * 2

# Legacy 1 tuple per competency covering 4 stem_variants (v5 pattern)
TEMPLATES = [
    (
        "C-06",
        "multiple_choice",
        [
            r"Para una muestra de tamaño $n = @n@$, determine la varianza asintótica del estimador MLE:",
            r"Considere el estimador de máxima verosimilitud con $n = @n@$. Calcule $\\text{Avar}(\\hat{\\theta})$:",
            r"En un modelo regular con $n = @n@$ observaciones, halle la cota de varianza asintótica:",
            r"Dado el tamaño muestral $n = @n@$, compute la varianza límite del estimador:",
        ],
        gen_c06,
        ver_c06,
        r"La varianza asintótica resulta $\\text{Avar} = 2n = @ans@$.",
        "Varianza Asintótica MLE",
        ["D-C06-01", "D-C06-02", "D-C06-03", "D-C06-04", "D-C06-05", "D-C06-06"],
        ("asymptotic_notes.pdf", 2, "Cálculo de varianza asintótica"),
    )
]
'''
        shard_09_py.write_text(single_tuple_code, encoding="utf-8")
        self.assertGreaterEqual(len(single_tuple_code.splitlines()), 40)

        # Compile with min_archetypes=4
        ok, errors = compile_shard(
            work_dir_or_path=self.work_dir,
            shard_id="shard_09",
            strict=True,
            min_archetypes=4,
        )

        self.assertFalse(ok, "Expected compilation to fail under min_archetypes=4")
        self.assertTrue(any("[M3-ARCHETYPES]" in str(e) for e in errors), f"Expected [M3-ARCHETYPES] in errors: {errors}")

        # Check attempts state
        att_file = self.check_attempts_dir / "compile_shard_09.json"
        self.assertTrue(att_file.is_file(), f"Expected compile_shard_09.json in {self.check_attempts_dir}")
        att_data = json.loads(att_file.read_text(encoding="utf-8"))
        error_count = att_data.get("error_count", 0)
        self.assertGreaterEqual(error_count, 1)
        self.assertLess(error_count, 6)
        self.assertFalse(att_data.get("has_syntax_error"))

        # Hook Guard Rule C: write_file on shard_09_data.py is DENIED
        write_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(shard_09_py),
                    "Content": "# Overwrite attempt instead of surgical edit",
                },
            },
        }
        res_write = process_hook(write_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_write.get("decision"), "deny")
        self.assertIn("BLOCKER:: El archivo shard_09_data.py ya fue compilado", res_write.get("reason", ""))
        self.assertIn("umbral oficial", res_write.get("reason", ""))
        self.assertIn("[M3-ARCHETYPES]", res_write.get("reason", ""))
        self.assertIn("usa edit_file quirúrgico", res_write.get("reason", ""))
        self.assertIn("shard_fixes/<CID>.py", res_write.get("reason", ""))

        # Hook Guard Rule C: edit_file on shard_09_data.py is ALLOWED
        edit_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "edit_file",
                "args": {
                    "Path": str(shard_09_py),
                    "Target": "TEMPLATES = [",
                    "Replacement": "TEMPLATES = [",
                },
            },
        }
        res_edit = process_hook(edit_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_edit.get("decision"), "allow")

        # Hook Guard Rule C: modular fix in shard_fixes/C-06.py is ALLOWED
        fix_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(self.shard_fixes_dir / "C-06.py"),
                    "Content": "# Modular fix for C-06",
                },
            },
        }
        res_fix = process_hook(fix_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_fix.get("decision"), "allow")

    def test_shard_compact_pattern_passes_m3_archetypes_and_hook_guard_rule_b_blocks_further_edits(self) -> None:
        """3. Shard Integration: When the shard uses the compact pattern:
        - def _gen_c06(rng, arch): + gen_c06_1..4 + 4 tuples of 9 elements with [] in position 7
        - compile_shard.py approves with [+] PASS and writes pass_shard_09.json
        - c2c_hook_guard.py (Rule B) blocks further writes and edits.
        """
        shard_09_py = self.shards_dir / "shard_09_data.py"
        compact_code = '''# shard_09_data.py
"""Compact 4-archetype implementation using shared helper _gen_c06(rng, arch)."""
import random

# Preamble helper function
def _gen_c06(rng, arch):
    n = rng.randint(20, 200)
    if arch == 1:
        ans = n + 10
        distractors = [ans - 2, ans + 2, ans + 4, ans + 6, ans + 8, ans + 10]
    elif arch == 2:
        ans = n * 2
        distractors = [ans - 5, ans + 5, ans + 10, ans + 15, ans + 20, ans + 25]
    elif arch == 3:
        ans = n + 5
        distractors = [ans - 1, ans + 1, ans + 3, ans + 7, ans + 9, ans + 11]
    else:  # arch == 4 (frontera)
        ans = n * 3
        distractors = [ans - 3, ans + 3, ans + 6, ans + 9, ans + 12, ans + 15]

    return {
        "vars": {
            "n": n, "ans": ans,
            "d1": distractors[0], "d2": distractors[1], "d3": distractors[2],
            "d4": distractors[3], "d5": distractors[4], "d6": distractors[5],
        },
        "correct": r"$@ans@$",
        "distractors": [
            r"$@d1@$", r"$@d2@$", r"$@d3@$",
            r"$@d4@$", r"$@d5@$", r"$@d6@$",
        ],
    }

# 4 Thin Wrappers
def gen_c06_1(rng): return _gen_c06(rng, 1)
def gen_c06_2(rng): return _gen_c06(rng, 2)
def gen_c06_3(rng): return _gen_c06(rng, 3)
def gen_c06_4(rng): return _gen_c06(rng, 4)

def ver_c06_1(res): return res["vars"]["ans"] == res["vars"]["n"] + 10
def ver_c06_2(res): return res["vars"]["ans"] == res["vars"]["n"] * 2
def ver_c06_3(res): return res["vars"]["ans"] == res["vars"]["n"] + 5
def ver_c06_4(res): return res["vars"]["ans"] == res["vars"]["n"] * 3

# 4 Form-A 9-element tuples: position 7 is [] and 10th element (hints) is omitted
TEMPLATES = [
    (
        "C-06", "multiple_choice_7_options",
        [
            r"Arquetipo 1: Calcule la varianza asintótica directa para $n = @n@$:",
            r"Arquetipo 1 Variante B: Determine el valor asintótico frontal con $n = @n@$:",
            r"Arquetipo 1 Variante C: Para tamaño $n = @n@$, halle la dispersión directa:",
        ],
        gen_c06_1, ver_c06_1,
        r"La varianza asintótica frontal es $@ans@$.",
        "Varianza Asintótica Directa",
        [],
        ("asymptotic_notes.pdf", 2, "Fórmula directa de varianza"),
    ),
    (
        "C-06", "multiple_choice_7_options",
        [
            r"Arquetipo 2: Inverso: A partir de la dispersión dada con $n = @n@$, determine el parámetro:",
            r"Arquetipo 2 Variante B: Diagnóstico inverso de varianza asintótica con $n = @n@$:",
            r"Arquetipo 2 Variante C: Deduzca el parámetro subyacente para $n = @n@$:",
        ],
        gen_c06_2, ver_c06_2,
        r"Por inversión analítica del estimador, el resultado es $@ans@$.",
        "Diagnóstico Inverso Asintótico",
        [],
        ("asymptotic_notes.pdf", 2, "Inversión analítica"),
    ),
    (
        "C-06", "multiple_choice_7_options",
        [
            r"Arquetipo 3: Perturbación: Analice el cambio incremental en la varianza con $n = @n@$:",
            r"Arquetipo 3 Variante B: Estática comparativa de la varianza límite bajo $n = @n@$:",
            r"Arquetipo 3 Variante C: Evalúe la perturbación de primer orden para $n = @n@$:",
        ],
        gen_c06_3, ver_c06_3,
        r"La perturbación de primer orden incrementa la varianza a $@ans@$.",
        "Perturbación Asintótica",
        [],
        ("asymptotic_notes.pdf", 2, "Estática comparativa"),
    ),
    (
        "C-06", "multiple_choice_7_options",
        [
            r"Arquetipo 4: Frontera: Evalúe el comportamiento en el régimen límite con $n = @n@$:",
            r"Arquetipo 4 Variante B: Caso extremo de cota asintótica para $n = @n@$:",
            r"Arquetipo 4 Variante C: En la condición de frontera con $n = @n@$, halle la dispersión:",
        ],
        gen_c06_4, ver_c06_4,
        r"En la frontera del soporte paramétrico el valor límite es $@ans@$.",
        "Frontera Asintótica",
        [],
        ("asymptotic_notes.pdf", 2, "Condiciones de frontera"),
    ),
]
'''
        shard_09_py.write_text(compact_code, encoding="utf-8")

        # Compile with min_archetypes=4
        ok, errors = compile_shard(
            work_dir_or_path=self.work_dir,
            shard_id="shard_09",
            strict=True,
            min_archetypes=4,
        )

        self.assertTrue(ok, f"Expected clean pass for compact 4-archetype pattern, got errors: {errors}")
        self.assertEqual(len(errors), 0)

        # Verify pass_shard_09.json was created
        pass_file = self.check_attempts_dir / "pass_shard_09.json"
        self.assertTrue(pass_file.is_file(), "Expected pass_shard_09.json to exist on disk")
        pass_data = json.loads(pass_file.read_text(encoding="utf-8"))
        self.assertEqual(pass_data.get("status"), "PASS")
        self.assertEqual(pass_data.get("shard_id"), "shard_09")

        # Verify templates/C-06.json was produced and auto-populated from cta.json
        t_file = self.templates_dir / "C-06.json"
        self.assertTrue(t_file.is_file(), f"Expected compiled template {t_file}")
        t_data = json.loads(t_file.read_text(encoding="utf-8"))
        templates_list = t_data.get("templates", [])
        self.assertEqual(len(templates_list), 4)
        for tpl in templates_list:
            self.assertEqual(len(tpl.get("distractor_ids", [])), 6)
            self.assertGreaterEqual(len(tpl.get("hints", [])), 3)

        # Hook Guard Rule B: Verify write_file on shard_09_data.py is blocked post-PASS
        write_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(shard_09_py),
                    "Content": "# Overwrite attempt post-pass",
                },
            },
        }
        res_write = process_hook(write_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_write.get("decision"), "deny")
        self.assertIn("BLOCKER:: El shard shard_09 ya aprobó todas las validaciones estrictas ([+] PASS)", res_write.get("reason", ""))
        self.assertIn("emite DONE inmediatamente", res_write.get("reason", ""))

        # Hook Guard Rule B: Verify edit_file on shard_09_data.py is ALSO blocked post-PASS
        edit_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "edit_file",
                "args": {
                    "Path": str(shard_09_py),
                    "Target": "Arquetipo 1",
                    "Replacement": "Arquetipo 1 Modificado",
                },
            },
        }
        res_edit = process_hook(edit_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_edit.get("decision"), "deny")
        self.assertIn("BLOCKER:: El shard shard_09 ya aprobó todas las validaciones estrictas ([+] PASS)", res_edit.get("reason", ""))

    def test_shard_syntax_error_recovery_lifecycle_with_hook_guard(self) -> None:
        """4. Shard Cross-Contract Edge Case: Syntax error recovery lifecycle.
        - Unparseable source in shard_09_data.py causes compile_shard.py to record has_syntax_error=True and error_count=1.
        - c2c_hook_guard.py allows write_file full overwrite to unbreak the file (bypassing Rule C rewrite restriction).
        - After writing valid 4-archetypes code, compile_shard.py produces [+] PASS and writes pass_shard_09.json.
        - c2c_hook_guard.py immediately locks down shard_09_data.py under Rule B (Post-PASS Cut).
        """
        shard_09_py = self.shards_dir / "shard_09_data.py"
        broken_shard_syntax_code = '''# shard_09_data.py
"""Exercise templates for shard_09 with deliberate Python syntax error."""
import random

def gen_c06(rng):
    # Syntax error: unclosed parenthesis
    ans = ( 1 +
    return {"vars": {"ans": ans}, "correct": "$1$", "distractors": []}

TEMPLATES = [
    ("C-06", "multiple_choice", ["Stem"], gen_c06, lambda r: True, "Sol", "KC", [], ("doc.pdf", 1, "Q"))
]
''' + ("# Padding line to ensure file exceeds 40 lines\n" * 45)

        shard_09_py.write_text(broken_shard_syntax_code, encoding="utf-8")
        self.assertGreaterEqual(len(broken_shard_syntax_code.splitlines()), 40)

        ok, errors = compile_shard(
            work_dir_or_path=self.work_dir,
            shard_id="shard_09",
            strict=True,
            min_archetypes=4,
        )

        self.assertFalse(ok)
        self.assertTrue(any("Syntax" in str(e) or "error" in str(e).lower() for e in errors), f"Expected syntax error, got: {errors}")

        att_file = self.check_attempts_dir / "compile_shard_09.json"
        self.assertTrue(att_file.is_file(), f"Expected compile_shard_09.json in {self.check_attempts_dir}")
        att_data = json.loads(att_file.read_text(encoding="utf-8"))
        self.assertTrue(att_data.get("has_syntax_error"), "Expected has_syntax_error=True in check_attempts")
        self.assertEqual(att_data.get("error_count"), 1)

        # Hook Guard: write_file MUST be allowed because has_syntax_error=True even though lines >= 40 and error_count < 6
        compact_code = '''# shard_09_data.py
"""Compact 4-archetype implementation using shared helper _gen_c06(rng, arch)."""
import random

def _gen_c06(rng, arch):
    n = rng.randint(20, 200)
    ans = n * (arch + 1)
    distractors = [ans - 2, ans + 2, ans + 4, ans + 6, ans + 8, ans + 10]
    return {
        "vars": {
            "n": n, "ans": ans,
            "d1": distractors[0], "d2": distractors[1], "d3": distractors[2],
            "d4": distractors[3], "d5": distractors[4], "d6": distractors[5],
        },
        "correct": r"$@ans@$",
        "distractors": [r"$@d1@$", r"$@d2@$", r"$@d3@$", r"$@d4@$", r"$@d5@$", r"$@d6@$"],
    }

def gen_c06_1(rng): return _gen_c06(rng, 1)
def gen_c06_2(rng): return _gen_c06(rng, 2)
def gen_c06_3(rng): return _gen_c06(rng, 3)
def gen_c06_4(rng): return _gen_c06(rng, 4)

def ver_c06_1(res): return res["vars"]["ans"] == res["vars"]["n"] * 2
def ver_c06_2(res): return res["vars"]["ans"] == res["vars"]["n"] * 3
def ver_c06_3(res): return res["vars"]["ans"] == res["vars"]["n"] * 4
def ver_c06_4(res): return res["vars"]["ans"] == res["vars"]["n"] * 5

TEMPLATES = [
    ("C-06", "multiple_choice_7_options", [r"Arquetipo 1: $n = @n@$:"], gen_c06_1, ver_c06_1, r"Solución: $@ans@$.", "KC Directo", [], ("asymptotic_notes.pdf", 2, "Ref 1")),
    ("C-06", "multiple_choice_7_options", [r"Arquetipo 2: $n = @n@$:"], gen_c06_2, ver_c06_2, r"Solución: $@ans@$.", "KC Inverso", [], ("asymptotic_notes.pdf", 2, "Ref 2")),
    ("C-06", "multiple_choice_7_options", [r"Arquetipo 3: $n = @n@$:"], gen_c06_3, ver_c06_3, r"Solución: $@ans@$.", "KC Perturbación", [], ("asymptotic_notes.pdf", 2, "Ref 3")),
    ("C-06", "multiple_choice_7_options", [r"Arquetipo 4: $n = @n@$:"], gen_c06_4, ver_c06_4, r"Solución: $@ans@$.", "KC Frontera", [], ("asymptotic_notes.pdf", 2, "Ref 4")),
]
'''
        write_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(shard_09_py),
                    "Content": compact_code,
                },
            },
        }
        res_write = process_hook(write_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_write.get("decision"), "allow", f"Expected allow on syntax error recovery, got: {res_write}")

        # Worker writes valid healed code
        shard_09_py.write_text(compact_code, encoding="utf-8")

        # Re-compilation succeeds to PASS
        ok_re, errors_re = compile_shard(
            work_dir_or_path=self.work_dir,
            shard_id="shard_09",
            strict=True,
            min_archetypes=4,
        )
        self.assertTrue(ok_re, f"Expected successful pass after syntax fix, got errors: {errors_re}")
        self.assertEqual(len(errors_re), 0)

        # pass_shard_09.json exists
        pass_file = self.check_attempts_dir / "pass_shard_09.json"
        self.assertTrue(pass_file.is_file())
        pass_data = json.loads(pass_file.read_text(encoding="utf-8"))
        self.assertEqual(pass_data.get("status"), "PASS")

        # Post-PASS lockdown: Hook Guard Rule B blocks further write_file and edit_file
        res_blocked_write = process_hook(write_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_blocked_write.get("decision"), "deny")
        self.assertIn("BLOCKER:: El shard shard_09 ya aprobó", res_blocked_write.get("reason", ""))

        edit_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "edit_file",
                "args": {
                    "Path": str(shard_09_py),
                    "Target": "Arquetipo 1",
                    "Replacement": "Arquetipo 1 Modificado",
                },
            },
        }
        res_blocked_edit = process_hook(edit_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_blocked_edit.get("decision"), "deny")
        self.assertIn("BLOCKER:: El shard shard_09 ya aprobó", res_blocked_edit.get("reason", ""))

    def test_shard_failure_over_threshold_allows_full_rewrite(self) -> None:
        """5. Shard Cross-Contract Edge Case: When compile_shard.py records error_count >= 6:
        - c2c_hook_guard.py allows write_file on shard_09_data.py for rescue rewrite.
        """
        shard_09_py = self.shards_dir / "shard_09_data.py"
        shard_09_py.write_text("# Shard data file\n" * 50, encoding="utf-8")

        # Simulate check attempts state recording 6 errors
        att_state = {
            "distinct_compiles": 1,
            "error_count": 6,
            "has_syntax_error": False,
            "last_err_hash": "hash-6-errors",
            "last_errors": ["Error 1", "Error 2", "Error 3", "Error 4", "Error 5", "Error 6"],
        }
        (self.check_attempts_dir / "compile_shard_09.json").write_text(
            json.dumps(att_state, indent=2), encoding="utf-8"
        )

        # Hook Guard Rule C: write_file on shard_09_data.py is ALLOWED for rescue rewrite
        write_payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(shard_09_py),
                    "Content": "# Fresh rescue rewrite after >= 6 errors",
                },
            },
        }
        res_write = process_hook(write_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_write.get("decision"), "allow")


class TestCatalogAndPromptsAlignment(unittest.TestCase):
    """Verifies subagent_types.json catalog and system_prompts/lean synchronization and encoding."""

    def test_subagent_types_json_exact_sync_and_lf_encoding(self) -> None:
        """subagent_types.json is strictly LF encoded and matches dispatch.get_type_definitions(lean=False) byte-by-byte."""
        types_file = SKILL_DIR / "subagent_types.json"
        self.assertTrue(types_file.is_file(), f"subagent_types.json missing from {SKILL_DIR}")

        raw_bytes = types_file.read_bytes()
        self.assertNotIn(b"\r", raw_bytes, "subagent_types.json must use strict LF line endings without CRLF")

        disk_content = json.loads(raw_bytes.decode("utf-8"))
        mem_types = get_type_definitions(lean=False)

        self.assertEqual(
            disk_content,
            mem_types,
            "subagent_types.json on disk is out of sync with dispatch.get_type_definitions(lean=False)",
        )
        self.assertEqual(len(disk_content), 4)
        names = {t["name"] for t in disk_content}
        self.assertEqual(names, {"c2c_cta_architect", "c2c_shard_author", "c2c_judge", "c2c_repair"})

    def test_lean_system_prompts_sync_and_lf_encoding(self) -> None:
        """Active lean prompts for the 4 catalog subagents are under 5KB and match get_type_definitions(lean=True) byte-by-byte."""
        lean_dir = SKILL_DIR / "system_prompts" / "lean"
        self.assertTrue(lean_dir.is_dir(), f"Missing lean directory: {lean_dir}")

        file_map = {
            "c2c_cta_architect": "prompt_cta_architect.md",
            "c2c_shard_author": "prompt_shard_author.md",
            "c2c_judge": "prompt_blind_judge.md",
            "c2c_repair": "prompt_repair.md",
        }

        for subagent_name, prompt_name in file_map.items():
            lf = lean_dir / prompt_name
            self.assertTrue(lf.is_file(), f"Missing lean prompt file: {lf}")
            lf_bytes = lf.read_bytes()
            max_size = 4750 if prompt_name == "prompt_shard_author.md" else 5120
            self.assertLessEqual(
                len(lf_bytes),
                max_size,
                f"Lean prompt {prompt_name} exceeded size budget of {max_size} bytes (actual: {len(lf_bytes)})",
            )

        mem_lean = get_type_definitions(lean=True)
        self.assertEqual(len(mem_lean), 4)

        for subagent in mem_lean:
            name = subagent["name"]
            self.assertIn(name, file_map)
            expected_prompt = (lean_dir / file_map[name]).read_text(encoding="utf-8")
            self.assertEqual(
                subagent["system_prompt"],
                expected_prompt,
                f"get_type_definitions(lean=True) for {name} does not match {file_map[name]} byte-by-byte",
            )

    def test_sweetspot_v35_contract_directives_in_all_subagents(self) -> None:
        """Both full and lean definitions consistently enforce official threshold < 6, M3-ARCHETYPES, and ArtifactMetadata bans."""
        full_types = get_type_definitions(lean=False)
        lean_types = get_type_definitions(lean=True)

        for types_list, mode in [(full_types, "full"), (lean_types, "lean")]:
            type_map = {t["name"]: t["system_prompt"] for t in types_list}

            # 1. c2c_cta_architect
            cta_sp = type_map["c2c_cta_architect"]
            self.assertIn("6", cta_sp, f"[{mode}] cta_architect missing < 6 error threshold directive")
            self.assertTrue("edit_file" in cta_sp or "replace_file_content" in cta_sp, f"[{mode}] cta_architect missing edit_file")
            self.assertIn("ArtifactMetadata", cta_sp, f"[{mode}] cta_architect missing ArtifactMetadata prohibition")
            self.assertIn('r"', cta_sp, f"[{mode}] cta_architect missing raw string requirement")

            # 2. c2c_shard_author
            author_sp = type_map["c2c_shard_author"]
            self.assertIn("M3-ARCHETYPES", author_sp, f"[{mode}] shard_author missing [M3-ARCHETYPES]")
            self.assertIn("6", author_sp, f"[{mode}] shard_author missing < 6 error threshold directive")
            self.assertIn("ArtifactMetadata", author_sp, f"[{mode}] shard_author missing ArtifactMetadata prohibition")

            # 3. c2c_repair
            repair_sp = type_map["c2c_repair"]
            self.assertIn("6", repair_sp, f"[{mode}] repair missing < 6 error threshold directive")
            self.assertIn("shard_fixes", repair_sp, f"[{mode}] repair missing shard_fixes directive")

            # 4. c2c_judge
            judge_sp = type_map["c2c_judge"]
            self.assertIn("DONE:", judge_sp, f"[{mode}] judge missing DONE signal contract")
            self.assertIn("ArtifactMetadata", judge_sp, f"[{mode}] judge missing ArtifactMetadata prohibition")



if __name__ == "__main__":
    unittest.main()
