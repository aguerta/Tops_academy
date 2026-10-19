"""Tests for C2C Prescriptive Diagnostics, Cumulative Error Sweeps, and Hermetic Publisher.

Verifies:
1. Full-sweep cumulative error accumulation in check_templates and engine/invariants (no early break/return).
2. Prescriptive surgical diagnostic formatting with location, snippet, root cause, remediation, and agent warning note.
3. Hermetic Python environment resolution and in-memory fallback in course_publisher.py.
4. Epistemic closure and atomic contracts in dispatch.py.
"""

import json
import os
import sys
from pathlib import Path

import pytest

# Ensure skill scripts are importable
_skills_root = Path(__file__).parent.parent / ".agents" / "skills" / "content-to-course"
if str(_skills_root) not in sys.path:
    sys.path.insert(0, str(_skills_root))

from check_templates import check_single_template, format_diagnostic_error
from engine.invariants import check_instance_invariants, validate_katex_syntax
from course_publisher import CoursePublisher
from dispatch import ROLE_SPECS, get_type_definitions, dispatch_authors, dispatch_judges, dispatch_cta


class TestPrescriptiveDiagnosticsAndAccumulation:
    """Tests for prescriptive error formatting and non-fail-fast accumulation."""

    def test_format_diagnostic_error_structure(self):
        """asserts diagnostic error string contains all required fields for LLM comprehension."""
        err_str = format_diagnostic_error(
            rule_tag="R-20: SINTAXIS / LLAVES",
            competency="Hab-03",
            template="T-Hab03-01",
            item_id="Q-Hab03-001",
            field_name="misconception_warning",
            snippet="...cuando {K} aumenta respecto a {L}...",
            cause="Se detectaron llaves aisladas '{K}' y '{L}' en un campo de texto que NO corresponden a variables del diccionario 'vars'.",
            actions=[
                "Si son símbolos matemáticos: enciérralos en delimitadores KaTeX simples: '$K$' y '$L$'.",
                "Si son texto explicativo: retira las llaves: 'K' y 'L'.",
                "Si son parámetros dinámicos: agrégalos explícitamente en el retorno de 'vars' en generate_py.",
            ],
        )

        assert "[-] [R-20: SINTAXIS / LLAVES]" in err_str
        assert "UBICACIÓN: Competencia: 'Hab-03', Plantilla: 'T-Hab03-01', Reactivo: 'Q-Hab03-001', Campo: 'misconception_warning'" in err_str
        assert "FRAGMENTO INFRACTOR: ...cuando {K} aumenta respecto a {L}..." in err_str
        assert "CAUSA:" in err_str
        assert "ACTION REQUIRED:" in err_str
        assert "ACCIONES CORRECTIVAS:" in err_str
        assert "1. Si son símbolos matemáticos:" in err_str
        assert "2. Si son texto explicativo:" in err_str
        assert "NOTA PARA EL AGENTE: NO abras ni inspecciones el código de check_templates.py ni rules.py." in err_str

    def test_validate_katex_syntax_accumulates_multiple_errors_without_break(self):
        """validate_katex_syntax must return all KaTeX defects without breaking early."""
        # Text containing: triple dollar, unreplaced variable, and double curly braces
        problematic_text = "Fórmula con $$$x + y$$$ y llaves dobles {{val}} y variable no sustituida {Z_star}."
        errors = validate_katex_syntax(problematic_text, "test_field")

        assert len(errors) >= 3
        assert any("$$$" in e for e in errors)
        assert any("{{val}}" in e or "{{" in e for e in errors)
        assert any("{Z_star}" in e for e in errors)

    def test_check_instance_invariants_accumulates_all_errors_across_fields(self):
        """check_instance_invariants must evaluate stem, hints, options without early break."""
        bad_mc7 = {
            "stem": "$$$x + y$$$ con {leaked_var}",  # 2 errors: $$$ and {var}
            "hints": ["Hint 1 with $$$", "Hint 2", "Hint 3 with {{bad}}"],
            "detailed_solution": "Solución con $$$ error",
            "options": [
                {"content": "Opcion 1", "is_correct": True},
                {"content": "Opcion 2", "is_correct": False},  # Missing error_rationale
                {"content": "Opcion 3", "is_correct": False, "error_rationale": "Confundiendo erróneamente el signo"},  # Giveaway
                {"content": "Opcion 4", "is_correct": False, "error_rationale": "Ok"},
                {"content": "Opcion 5", "is_correct": False, "error_rationale": "Ok"},
                {"content": "Opcion 6", "is_correct": False, "error_rationale": "Ok"},
                {"content": "Opcion 7", "is_correct": False, "error_rationale": "Ok"},
            ],
        }

        is_valid, errors = check_instance_invariants(bad_mc7, "multiple_choice_7_options")
        assert not is_valid
        # Multiple independent errors accumulated:
        assert any("$$$" in e for e in errors)
        assert any("{leaked_var}" in e for e in errors)
        assert any("error_rationale" in e for e in errors)

    def test_check_single_template_dry_run_continues_on_partial_seed_failures(self):
        """When some seeds fail but others succeed, check_single_template must not abort early with return."""
        partial_fail_template = {
            "id": "T-PARTIAL-FAIL",
            "interaction_type": "multiple_choice_7_options",
            "stem": "Determine el valor de {x}.",
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "detailed_solution": "Solución {x}",
            "distractor_ids": ["D1", "D2", "D3", "D4", "D5", "D6"],
            "generate_py": (
                "def generate(rng):\n"
                "    # Seed 100 fails with ZeroDivisionError, but seeds 101-105 succeed\n"
                "    s = rng.randint(0, 10)\n"
                "    if s == 0:\n"
                "        raise ZeroDivisionError('Division by zero in generator')\n"
                "    return {\n"
                "        'vars': {'x': s},\n"
                "        'correct': f'Valor {s}',\n"
                "        'distractors': [\n"
                "            {'value': f'Dist {i}_{s}', 'distractor_id': f'D{i+1}'}\n"
                "            for i in range(6)\n"
                "        ]\n"
                "    }\n"
            ),
        }

        declared_dids = {"D1", "D2", "D3", "D4", "D5", "D6"}
        errors = check_single_template(
            template=partial_fail_template,
            competency_id="C-TEST",
            declared_distractor_ids=declared_dids,
            num_dry_run_seeds=20,
        )

        assert len(errors) > 0
        # The dry-run error is recorded
        assert any("TPL-DRY" in e for e in errors)
        # All errors are formatted prescriptively
        assert all("NOTA PARA EL AGENTE:" in e for e in errors)

    def test_check_single_template_validates_all_stem_variants_syntax(self):
        """Static check_single_template must catch broken KaTeX syntax across all stem_variants."""
        template = {
            "id": "TPL-VARIANTS-KATEX-ERR",
            "interaction_type": "fill_in_the_blank",
            "stem": "Determine el valor de {x}.",
            "stem_variants": [
                "Variante 0 válida con valor ${x}$.",
                "Variante 1 válida con parámetro ${x}$.",
                "Variante 2 rota con $\\frac{a}$ y ${x}$.",
                "Variante 3 rota con $\\hat{\\boldsymbol{\\beta}$ y ${x}$.",
            ],
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "detailed_solution": "Solución {x}",
            "distractor_ids": [],
            "generate_py": (
                "def generate(rng):\n"
                "    x = rng.randint(10, 50)\n"
                "    return {'vars': {'x': x}, 'correct': str(x), 'distractors': []}\n"
            ),
        }
        errors = check_single_template(
            template=template,
            competency_id="Hab-01",
            declared_distractor_ids=set(),
            num_dry_run_seeds=5,
        )
        assert len(errors) >= 2
        error_blob = "\n".join(errors)
        assert "stem_variants[2]" in error_blob
        assert "stem_variants[3]" in error_blob
        assert any("R-20" in e for e in errors)

    def test_validate_katex_syntax_detects_nested_unclosed_macro(self):
        """validate_katex_syntax must detect unclosed nested accent/style macros."""
        bad_text = r"El estimador puntual es $\hat{\boldsymbol{\beta}$ en el modelo."
        errors = validate_katex_syntax(bad_text, "test_field")
        assert len(errors) > 0
        assert any("nested" in e.lower() or "unclosed" in e.lower() for e in errors)

        good_text = r"El estimador puntual es $\hat{\boldsymbol{\beta}}$ en el modelo."
        good_errors = validate_katex_syntax(good_text, "test_field")
        assert not any("nested" in e.lower() for e in good_errors)


class TestHermeticPublisherAndRuntime:
    """Tests for virtualenv resolution and fallback in CoursePublisher."""

    def test_publisher_resolves_python_executable_to_venv(self):
        """CoursePublisher must find and prefer project .venv Python interpreter."""
        publisher = CoursePublisher(courses_dir="courses")
        py_exe = publisher._resolve_python_executable()

        assert py_exe is not None
        # On Windows or Linux, if .venv exists, it must point inside .venv
        if (Path(__file__).resolve().parents[1] / ".venv").exists():
            assert ".venv" in py_exe.lower()

    def test_publisher_in_memory_fallback_on_cli_failure(self, tmp_path, monkeypatch):
        """When CLI validator subprocess fails due to ModuleNotFoundError, CoursePublisher falls back to in-memory validator."""
        import subprocess
        from unittest.mock import MagicMock

        publisher = CoursePublisher(courses_dir=str(tmp_path))

        # Use an existing course JSON file or create a minimally valid one
        valid_course_file = Path("courses/solow_model.json")
        if not valid_course_file.exists():
            valid_course_file = Path("courses/solow_growth_model.json")
        if not valid_course_file.exists():
            pytest.skip("courses/solow_model.json not found for fallback test")

        # Mock subprocess.run to simulate ModuleNotFoundError: No module named 'validator'
        def mock_subprocess_run(*args, **kwargs):
            mock_res = MagicMock()
            mock_res.returncode = 1
            mock_res.stdout = "Error while finding module specification for 'validator.cli' (ModuleNotFoundError: No module named 'validator')\n"
            mock_res.stderr = ""
            return mock_res

        monkeypatch.setattr(subprocess, "run", mock_subprocess_run)

        # Running CLI validator should catch ModuleNotFoundError and fall back in-memory
        is_valid = publisher._run_cli_validator(valid_course_file, strict=False)
        assert is_valid is True


class TestDispatchContractsAndEpistemicClosure:
    """Tests that dispatch role specs enforce contracts and forbidden lists."""

    def test_author_forbidden_list_includes_validator(self):
        """c2c_shard_author must have scratch and engine in forbidden list."""
        author_spec = ROLE_SPECS["author"]
        forbidden = [f.lower() for f in author_spec["forbidden"]]

        assert any("engine" in f for f in forbidden)
        assert any("scratch" in f for f in forbidden)

    def test_judge_forbidden_list_includes_web_tools(self):
        """c2c_judge must have search_web and read_url_content in forbidden list."""
        judge_spec = ROLE_SPECS["judge"]
        forbidden = [f.lower() for f in judge_spec["forbidden"]]

        assert any("search_web" in f for f in forbidden)
        assert any("read_url_content" in f for f in forbidden)

    def test_cta_spec_declares_architect_contract(self):
        """c2c_cta_architect type description must declare positional tuples."""
        cta_type = next(t for t in get_type_definitions() if t["name"] == "c2c_cta_architect")
        desc = cta_type["description"]

        assert "c2c v3.2" in desc.lower() or "tuples" in desc.lower() or "cta_data.py" in desc.lower()

    def test_dispatch_generators_inject_repaired_contracts(self, tmp_path):
        """Zero-bundle dispatch generators must write item files with strict atomic contracts."""
        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True)
        (work_dir / "pre_cta_manifest.json").write_text(json.dumps({
            "files": [{"doc": "doc1.pdf", "path": "content/doc1.pdf", "total_pages": 10, "valid_page_range": [1, 10]}]
        }), encoding="utf-8")
        (work_dir / "cta.json").write_text(json.dumps({
            "competencies": [{"id": "C-01", "name": "Comp 1"}]
        }), encoding="utf-8")
        shards_dir = work_dir / "shards"
        shards_dir.mkdir(parents=True)
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
            "shards": [{"shard_id": "shard_01", "competency_ids": ["C-01"]}]
        }), encoding="utf-8")

        res_author = dispatch_authors(work_dir=work_dir)
        assert len(res_author["Subagents"]) >= 1
        item_author = Path(res_author["item_files"][0])
        assert item_author.exists()
        prompt_author = json.loads(item_author.read_text(encoding="utf-8"))["Prompt"]
        assert "compile_shard.py" in prompt_author
        assert "shard_01_data.py" in prompt_author

        # Seed items for judge
        verif_dir = work_dir / "verification"
        verif_dir.mkdir(parents=True)
        (verif_dir / "judge_batch_01.json").write_text(json.dumps({
            "items": [
                {
                    "item_id": "item_1",
                    "competency_id": "C-01",
                    "stem": "¿Cuánto es 2+2?",
                    "options": [
                        {"content": "4", "is_correct": True},
                        {"content": "3", "is_correct": False, "distractor_id": "D-01"}
                    ]
                }
            ]
        }), encoding="utf-8")
        res_judge = dispatch_judges(work_dir=work_dir)
        assert len(res_judge["Subagents"]) >= 1
        item_judge = Path(res_judge["item_files"][0])
        assert item_judge.exists()
        prompt_judge = json.loads(item_judge.read_text(encoding="utf-8"))["Prompt"]
        assert "search_web" in prompt_judge or "read_url_content" in prompt_judge

        res_cta = dispatch_cta(work_dir=work_dir)
        assert len(res_cta["Subagents"]) >= 1
        item_cta = Path(res_cta["item_files"][0])
        assert item_cta.exists()
        prompt_cta = json.loads(item_cta.read_text(encoding="utf-8"))["Prompt"]
        assert "compile_cta.py" in prompt_cta or "cta_data.py" in prompt_cta
