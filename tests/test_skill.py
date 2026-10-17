"""Comprehensive Test Suite for Content-to-Course v2 Generic Pipeline & Engine.

Consolidates 6 modular test classes (32 test cases):
1. TestSandboxSecurity (8 tests): AST whitelist, banned imports/builtins/dunders, determinism, timeout
2. TestIngestionAndVisionFallback (6 tests): multiformat discovery, image tiling >2500px, caching, diacritics
3. TestCTAContractAndValidation (5 tests): schema conformance, CTA-D1/D2, evidence mapping
4. TestGenericTemplateEngine (7 tests): template schema, duplicate rejection, MC7/FIB/MS, diversity >= 0.5
5. TestFewShotRegressionEDP_EDO (3 tests): EDP & EDO instantiation, strict validation, zero domain terms in engine
6. TestPipelineRunnerCLI (3 tests): fail-fast without cta.json, stage execution, publish & append
"""
from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List

import pytest
from PIL import Image

# Ensure repository root and skill directories are on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"
SRC_DIR = REPO_ROOT / "src"

for p in [str(SKILL_DIR), str(SRC_DIR), str(REPO_ROOT)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from check_cta import validate_cta_rules, validate_cta_schema
from check_templates import check_single_template, check_templates_file_or_dir, validate_template_schema
from course_publisher import CoursePublisher
from engine.assemble import assemble_question, check_course_giveaway_distribution
from engine.diversity import evaluate_competency_diversity, mask_stem_numbers
from engine.instantiate import allocate_template_quotas, instantiate_competency, instantiate_template
from engine.invariants import check_instance_invariants, InvariantViolationError
from engine.sandbox import (
    execute_sandbox_instance,
    validate_code_ast,
    SandboxExecutionError,
    SandboxTimeoutError,
    SecurityViolationError,
)
from ingest import ingest_course, ingest_image_file, normalize_corrupt_diacritics
from run import PipelineRunner
from validator.core import validate_course_content


# =============================================================================
# CLASS 1: TestSandboxSecurity (8 tests)
# =============================================================================
class TestSandboxSecurity:
    """Evaluates AST whitelist checks, banned modules, dunder protection, determinism and timeout."""

    def test_sandbox_ast_rejects_import_os(self):
        """Rejects banned modules: os, sys, subprocess, socket."""
        banned = [
            "import os\ndef generate(rng): return {}",
            "import sys\ndef generate(rng): return {}",
            "import subprocess\ndef generate(rng): return {}",
            "import socket\ndef generate(rng): return {}",
            "from os import path\ndef generate(rng): return {}",
        ]
        for snip in banned:
            with pytest.raises(SecurityViolationError):
                validate_code_ast(snip)

    def test_sandbox_ast_rejects_open_and_file_io(self):
        """Rejects file system access via open()."""
        code = "def generate(rng):\n    f = open('secret.txt')\n    return {}"
        with pytest.raises(SecurityViolationError):
            validate_code_ast(code)

    def test_sandbox_ast_rejects_dunder_import(self):
        """Rejects dynamic imports via __import__."""
        code = "def generate(rng):\n    m = __import__('os')\n    return {}"
        with pytest.raises(SecurityViolationError):
            validate_code_ast(code)

    def test_sandbox_ast_rejects_dunder_attributes(self):
        """Rejects object introspection and escaping via dunder attributes."""
        banned_dunders = [
            "def generate(rng):\n    c = ().__class__\n    return {}",
            "def generate(rng):\n    b = ().__class__.__bases__\n    return {}",
            "def generate(rng):\n    d = rng.__dict__\n    return {}",
            "def generate(rng):\n    g = generate.__globals__\n    return {}",
        ]
        for snip in banned_dunders:
            with pytest.raises(SecurityViolationError):
                validate_code_ast(snip)

    def test_sandbox_ast_rejects_transitive_banned_attribute(self):
        """Rejects transitive access to banned modules through allowed modules (e.g. fractions.sys)."""
        code = "import fractions\ndef generate(rng):\n    return {'v': fractions.sys.version}"
        with pytest.raises(SecurityViolationError):
            validate_code_ast(code)

    def test_sandbox_ast_rejects_eval_exec(self):
        """Rejects dynamic execution builtins: eval, exec, compile."""
        for builtin in ["eval('1+1')", "exec('a=1')", "compile('2+2', '', 'eval')"]:
            code = f"def generate(rng):\n    {builtin}\n    return {{}}"
            with pytest.raises(SecurityViolationError):
                validate_code_ast(code)

    def test_sandbox_ast_allows_whitelisted_math(self):
        """Allows whitelisted libraries: math, fractions, statistics, sympy, numpy, scipy."""
        valid_code = """
def generate(rng):
    import math
    import fractions
    import statistics
    import numpy as np
    import scipy.stats as stats
    import sympy as sp
    val = math.sqrt(16)
    f = fractions.Fraction(1, 2)
    s = statistics.mean([1, 2, 3])
    arr = np.array([1, 2, 3])
    p = stats.norm.cdf(0)
    x = sp.Symbol('x')
    return {"vars": {"v": val}, "correct": 4, "distractors": []}
"""
        # Should not raise
        validate_code_ast(valid_code)

    def test_sandbox_deterministic_seed(self):
        """Asserts generate(rng) with identical seeds produces identical outputs."""
        code = """
def generate(rng):
    a = rng.randint(10, 100)
    b = rng.randint(1, 5)
    return {"vars": {"a": a, "b": b}, "correct": a + b, "distractors": []}
"""
        r1 = execute_sandbox_instance(code, seed=42)
        r2 = execute_sandbox_instance(code, seed=42)
        assert r1 == r2, "Outputs must be identical for the same seed"

        r3 = execute_sandbox_instance(code, seed=43)
        assert r1 != r3, "Outputs should differ across differing seeds"

    def test_sandbox_timeout_enforced(self):
        """Asserts infinite loops trigger SandboxTimeoutError within timeout bounds."""
        infinite_loop = """
def generate(rng):
    while True:
        pass
"""
        with pytest.raises(SandboxTimeoutError):
            execute_sandbox_instance(infinite_loop, seed=1, timeout=1.0)


# =============================================================================
# CLASS 2: TestIngestionAndVisionFallback (6 tests)
# =============================================================================
class TestIngestionAndVisionFallback:
    """Evaluates multiformat document discovery, large image tiling, manifest caching, and diacritics."""

    def test_ingest_discovers_mixed_formats(self, tmp_path):
        """Discovers both PDF files and image formats in source folder."""
        in_dir = tmp_path / "in"
        in_dir.mkdir()
        pdf_file = in_dir / "sample.pdf"
        try:
            import pymupdf
        except ImportError:
            import fitz as pymupdf
        doc = pymupdf.open()
        doc.new_page()
        doc.save(str(pdf_file))
        doc.close()

        img_file = in_dir / "chart.png"
        img = Image.new("RGB", (300, 300), color="blue")
        img.save(str(img_file))

        out_pages = tmp_path / "work_pages"
        manifest = ingest_course(in_dir, out_pages)

        assert manifest["total_files"] >= 2
        types = [f["type"] for f in manifest["files"]]
        assert "pdf" in types
        assert "image" in types

    def test_ingest_image_tiling_large_dimensions(self, tmp_path):
        """Splits images exceeding 3072px into 3x2 grid with 10% overlap plus overview."""
        large_img_path = tmp_path / "board_large.png"
        img = Image.new("RGB", (3500, 3200), color="white")
        img.save(str(large_img_path))

        out_dir = tmp_path / "tiled_output"
        num_tiles = ingest_image_file(large_img_path, out_dir)

        # 3x2 grid = 6 tiles + 1 overview thumbnail
        assert num_tiles == 6
        assert (out_dir / "overview.png").is_file()
        assert len(list(out_dir.glob("tile_r*_c*.png"))) == 6

    def test_ingest_image_small_dimensions(self, tmp_path):
        """Keeps images <= 3072px as single whole page without tiling."""
        small_img_path = tmp_path / "small.jpg"
        img = Image.new("RGB", (800, 600), color="green")
        img.save(str(small_img_path))

        out_dir = tmp_path / "small_output"
        num_pages = ingest_image_file(small_img_path, out_dir)

        assert num_pages == 1
        assert (out_dir / "page_001.png").is_file()
        assert not (out_dir / "overview.png").exists()

    def test_ingest_sha256_manifest_caching(self, tmp_path):
        """Asserts re-running ingestion retains cached files and avoids duplication."""
        in_dir = tmp_path / "in_cache"
        in_dir.mkdir()
        img_file = in_dir / "diagram.png"
        img = Image.new("RGB", (400, 400), color="yellow")
        img.save(str(img_file))

        out_pages = tmp_path / "pages_cache"
        res1 = ingest_course(in_dir, out_pages)
        manifest1 = json.loads((out_pages / "pre_cta_manifest.json").read_text(encoding="utf-8"))

        res2 = ingest_course(in_dir, out_pages)
        manifest2 = json.loads((out_pages / "pre_cta_manifest.json").read_text(encoding="utf-8"))

        assert len(manifest1["files"]) == len(manifest2["files"])
        assert manifest1["files"][0]["doc"] == manifest2["files"][0]["doc"]

    def test_text_layer_normalization(self):
        """Normalizes corrupt diacritics from Beamer exports into valid accented characters."""
        corrupt = "Regresi´on Te´orico matem´atica funci´on ˆβ"
        normalized = normalize_corrupt_diacritics(corrupt)
        assert "Regresión" in normalized
        assert "Teórico" in normalized
        assert "matemática" in normalized
        assert "función" in normalized

    def test_stage0_pre_cta_manifest_structure(self, tmp_path):
        """Asserts pre_cta_manifest contains files, subparts, cta_mode, and no legacy artifacts."""
        in_dir = tmp_path / "in_stg0"
        in_dir.mkdir()
        img_file = in_dir / "pic.png"
        img = Image.new("RGB", (200, 200), color="red")
        img.save(str(img_file))

        out_dir = tmp_path / "work_stg0"
        res = ingest_course(in_dir, out_dir)

        manifest_file = out_dir / "pre_cta_manifest.json"
        assert manifest_file.is_file()
        m_data = json.loads(manifest_file.read_text(encoding="utf-8"))
        assert "files" in m_data
        assert "subparts" in m_data
        assert "cta_mode" in m_data
        assert "next_milestones_notes" not in m_data
        assert not (out_dir / "corpus.md").exists()
        assert not (out_dir / "density.json").exists()


# =============================================================================
# CLASS 3: TestCTAContractAndValidation (5 tests)
# =============================================================================
class TestCTAContractAndValidation:
    """Evaluates CTA schema conformance, CTA-D1/D2 distractor rules, and evidence verification."""

    def test_cta_schema_conformance(self):
        """Validates that well-formed CTA JSON passes cta.schema.json."""
        valid_cta = {
            "course_id": "test_c",
            "title": "Test Course",
            "macro_competency": "General Macro",
            "competencies": [
                {
                    "id": "C-01",
                    "type": "concept",
                    "name": "Concept One",
                    "description_latex": "Desc",
                    "bloom": "Understand",
                    "prerequisites": [],
                    "source_examples": ["Ex 1"],
                    "evidence": [{"doc": "doc1.pdf", "page": 1}],
                    "distractors": [
                        {
                            "id": f"D-C01-0{i}",
                            "name": f"Distractor {i}",
                            "wrong_belief": f"Belief {i}",
                            "omitted_step": None,
                            "trigger": "Trigger",
                            "manifestation": "Manifest",
                            "error_type": "conceptual_swap",
                            "severity": "medium",
                            "origin": "source",
                            "evidence": {"doc": "doc1.pdf", "page": 1},
                            "remediation_hint": "Hint",
                        }
                        for i in range(1, 4)
                    ],
                }
            ],
        }
        errs = validate_cta_schema(valid_cta)
        assert len(errs) == 0

    def test_check_cta_rule_cta_d1_skill_distractor_count(self):
        """Rejects Skill competency with fewer than 6 distractors or fewer than 2 with omitted_step."""
        invalid_skill_cta = {
            "course_id": "c1",
            "title": "T",
            "macro_competency": "M",
            "competencies": [
                {
                    "id": "Hab-01",
                    "type": "skill",
                    "name": "Skill 1",
                    "description_latex": "Desc",
                    "bloom": "Apply",
                    "prerequisites": [],
                    "source_examples": ["Ex"],
                    "evidence": [{"doc": "doc.pdf", "page": 1}],
                    # Only 5 distractors and 0 omitted_step
                    "distractors": [
                        {
                            "id": f"D-Hab01-0{i}",
                            "name": f"D {i}",
                            "wrong_belief": "Belief",
                            "omitted_step": None,
                            "trigger": "T",
                            "manifestation": "M",
                            "error_type": "procedural_slip",
                            "severity": "medium",
                            "origin": "source",
                            "evidence": {"doc": "doc.pdf", "page": 1},
                            "remediation_hint": "R",
                        }
                        for i in range(1, 6)
                    ],
                }
            ],
        }
        is_valid, errs = validate_cta_rules(invalid_skill_cta)
        assert not is_valid
        assert any("CTA-D1 violation: Skill 'Hab-01' has 5 distractors" in e for e in errs)
        assert any("omitted_step (minimum 2 required)" in e for e in errs)

    def test_check_cta_rule_cta_d1_concept_distractor_count(self):
        """Rejects Fact/Concept competency with fewer than 3 distractors."""
        invalid_concept_cta = {
            "course_id": "c1",
            "title": "T",
            "macro_competency": "M",
            "competencies": [
                {
                    "id": "C-01",
                    "type": "concept",
                    "name": "Concept",
                    "description_latex": "Desc",
                    "bloom": "Understand",
                    "prerequisites": [],
                    "source_examples": ["Ex"],
                    "evidence": [{"doc": "doc.pdf", "page": 1}],
                    # Only 2 distractors
                    "distractors": [
                        {
                            "id": f"D-C01-0{i}",
                            "name": f"D {i}",
                            "wrong_belief": "Belief",
                            "omitted_step": None,
                            "trigger": "T",
                            "manifestation": "M",
                            "error_type": "conceptual_swap",
                            "severity": "medium",
                            "origin": "source",
                            "evidence": {"doc": "doc.pdf", "page": 1},
                            "remediation_hint": "R",
                        }
                        for i in range(1, 3)
                    ],
                }
            ],
        }
        is_valid, errs = validate_cta_rules(invalid_concept_cta)
        assert not is_valid
        assert any("minimum 3 required" in e for e in errs)

    def test_check_cta_rule_cta_d2_distractor_fields(self):
        """Rejects distractor with duplicate ID or where both wrong_belief and omitted_step are null."""
        cta_data = {
            "course_id": "c1",
            "title": "T",
            "macro_competency": "M",
            "competencies": [
                {
                    "id": "C-01",
                    "type": "concept",
                    "name": "C",
                    "description_latex": "D",
                    "bloom": "Remember",
                    "prerequisites": [],
                    "source_examples": ["E"],
                    "evidence": [{"doc": "d.pdf", "page": 1}],
                    "distractors": [
                        {
                            "id": "D-C01-01",
                            "name": "D1",
                            "wrong_belief": None,
                            "omitted_step": None,  # Both null!
                            "trigger": "T",
                            "manifestation": "M",
                            "error_type": "other",
                            "severity": "low",
                            "origin": "source",
                            "evidence": {"doc": "d.pdf", "page": 1},
                            "remediation_hint": "H",
                        },
                        {
                            "id": "D-C01-01",  # Duplicate ID!
                            "name": "D2",
                            "wrong_belief": "WB",
                            "omitted_step": None,
                            "trigger": "T",
                            "manifestation": "M",
                            "error_type": "other",
                            "severity": "low",
                            "origin": "source",
                            "evidence": {"doc": "d.pdf", "page": 1},
                            "remediation_hint": "H",
                        },
                        {
                            "id": "D-C01-03",
                            "name": "D3",
                            "wrong_belief": "WB3",
                            "omitted_step": None,
                            "trigger": "T",
                            "manifestation": "M",
                            "error_type": "other",
                            "severity": "low",
                            "origin": "source",
                            "evidence": {"doc": "d.pdf", "page": 1},
                            "remediation_hint": "H",
                        },
                    ],
                }
            ],
        }
        is_valid, errs = validate_cta_rules(cta_data)
        assert not is_valid
        assert any("Duplicate distractor id 'D-C01-01'" in e for e in errs)
        assert any("both wrong_belief and omitted_step are null" in e for e in errs)

    def test_check_cta_evidence_mapping(self):
        """Rejects competency evidence referencing missing document pages in manifest."""
        cta_data = {
            "course_id": "c1",
            "title": "T",
            "macro_competency": "M",
            "competencies": [
                {
                    "id": "C-01",
                    "type": "concept",
                    "name": "C",
                    "description_latex": "D",
                    "bloom": "Remember",
                    "prerequisites": [],
                    "source_examples": ["E"],
                    "evidence": [{"doc": "lecture.pdf", "page": 99}],  # Page 99 doesn't exist
                    "distractors": [
                        {
                            "id": f"D-C01-0{i}",
                            "name": f"D{i}",
                            "wrong_belief": "W",
                            "omitted_step": None,
                            "trigger": "T",
                            "manifestation": "M",
                            "error_type": "other",
                            "severity": "low",
                            "origin": "source",
                            "evidence": {"doc": "lecture.pdf", "page": 99},
                            "remediation_hint": "H",
                        }
                        for i in range(1, 4)
                    ],
                }
            ],
        }
        manifest_data = {
            "files": [
                {"doc": "lecture.pdf", "valid_page_range": [1, 2], "total_pages": 2}
            ]
        }
        is_valid, errs = validate_cta_rules(cta_data, manifest_data=manifest_data)
        assert not is_valid
        assert any("CTA-EV" in e or "fuera del rango" in e for e in errs)


# =============================================================================
# CLASS 4: TestGenericTemplateEngine (7 tests)
# =============================================================================
class TestGenericTemplateEngine:
    """Evaluates template schema validation, parameter/stem deduplication, MC7/MS/FIB assembly, and diversity."""

    def test_template_schema_validation(self):
        """Validates that template object adheres to template.schema.json."""
        tpl_data = {
            "competency_id": "Hab-01",
            "templates": [
                {
                    "id": "T-Hab01-01",
                    "interaction_type": "multiple_choice_7_options",
                    "difficulty": "medium",
                    "bloom": "Apply",
                    "stem": "Determine the value of {x} + {y}.",
                    "generate_py": "def generate(rng):\n    return {'vars': {'x': 1, 'y': 2}, 'correct': 3, 'distractors': [{'value': i, 'distractor_id': f'D-0{i}'} for i in range(1, 7)]}",
                    "cross_check_py": "def verify(res):\n    return True",
                    "hints": ["Hint 1", "Hint 2", "Hint 3"],
                    "solution": "Solution text here",
                    "distractor_ids": [f"D-0{i}" for i in range(1, 7)],
                }
            ],
        }
        errs = validate_template_schema(tpl_data)
        assert len(errs) == 0

    def test_template_duplicate_rejection(self):
        """Engine rejects duplicate parameter tuples and duplicate rendered stems."""
        template = {
            "id": "T-01",
            "competency_id": "C-01",
            "interaction_type": "fill_in_the_blank",
            "stem": "Compute {a} squared.",
            "generate_py": "def generate(rng):\n    # Only 3 possible values\n    a = rng.choice([2, 3, 4])\n    return {'vars': {'a': a}, 'correct': a**2, 'distractors': []}",
            "hints": ["H1", "H2", "H3"],
            "solution": "Sol",
            "distractor_ids": [],
        }
        # Attempt to instantiate 10 items when only 3 unique parameter tuples exist
        # Engine must reject duplicates and raise ValueError when quota cannot be reached
        with pytest.raises(ValueError) as exc_info:
            instantiate_template(template, competency_id="C-01", target_count=10, seed_offset=100)
        assert "could only generate 3/10 unique invariant instances" in str(exc_info.value)

        # Instantiating exactly 3 items must succeed without any duplicates
        items = instantiate_template(template, competency_id="C-01", target_count=3, seed_offset=100)
        assert len(items) == 3
        stems = [item["stem"] for item in items]
        assert len(set(stems)) == 3

    def test_template_mc7_distractor_mapping(self):
        """MC7 question must have 7 shuffled options, 1 correct, and 6 distinct distractor IDs."""
        template = {
            "id": "T-01",
            "competency_id": "Hab-01",
            "interaction_type": "multiple_choice_7_options",
            "stem": "Evaluate {a} + {b}:",
            "hints": ["H1", "H2", "H3"],
            "solution": "Sol",
            "distractor_ids": [f"D-0{i}" for i in range(1, 7)],
        }
        gen_result = {
            "vars": {"a": 2, "b": 3},
            "correct": "5",
            "distractors": [
                {"value": str(5 + i), "distractor_id": f"D-0{i}"} for i in range(1, 7)
            ],
        }
        q = assemble_question(template, gen_result, "Hab-01", question_index=1, seed=42)

        assert len(q["options"]) == 7
        correct_opts = [o for o in q["options"] if o.get("is_correct")]
        assert len(correct_opts) == 1
        d_ids = [o.get("distractor_id") for o in q["options"] if not o.get("is_correct")]
        assert len(set(d_ids)) == 6

    def test_template_ms_cardinality(self):
        """Multiple-select questions must have 4-6 options with correct count between 1 and n-1."""
        template = {
            "id": "T-02",
            "competency_id": "Hab-01",
            "interaction_type": "multiple_select",
            "stem": "Select all valid propositions:",
            "hints": ["H1", "H2", "H3"],
            "solution": "Sol",
            "distractor_ids": ["D-01", "D-02"],
        }
        gen_result = {
            "vars": {},
            "options": [
                {"content": "Opt A", "is_correct": True},
                {"content": "Opt B", "is_correct": True},
                {"content": "Opt C", "is_correct": False, "distractor_id": "D-01"},
                {"content": "Opt D", "is_correct": False, "distractor_id": "D-02"},
            ],
        }
        q = assemble_question(template, gen_result, "Hab-01", question_index=1, seed=42)

        assert 4 <= len(q["options"]) <= 6
        correct_count = sum(1 for o in q["options"] if o.get("is_correct"))
        assert 1 <= correct_count < len(q["options"])

    def test_template_fib_tolerance_and_equivalents(self):
        """Fill-in-the-blank generates scalar value with tolerance and accepted equivalents."""
        template = {
            "id": "T-03",
            "competency_id": "Hab-01",
            "interaction_type": "fill_in_the_blank",
            "stem": "Compute the slope:",
            "hints": ["H1", "H2", "H3"],
            "solution": "Sol",
            "distractor_ids": [],
        }
        gen_result = {
            "vars": {},
            "value": "0.8333",
            "canonical_algebraic": "5/6",
            "accepted_equivalents": ["0.8333", "0,8333", "5/6"],
            "tolerance": 0.00005,
        }
        q = assemble_question(template, gen_result, "Hab-01", question_index=1, seed=42)

        assert q["correct_answer"]["value"] == "0.8333"
        assert "5/6" in q["correct_answer"]["accepted_equivalents"]
        assert q["correct_answer"]["tolerance"] == 0.00005

    def test_template_invariants_correct_differs_from_distractors(self):
        """Invariants engine rejects questions where a distractor matches the correct answer."""
        bad_q = {
            "id": "Q-01",
            "stem": "Question stem here with sufficient length.",
            "interaction_type": "multiple_choice_7_options",
            "options": [
                {"id": "opt_a", "option_id": "A", "content": "Correct Value", "is_correct": True},
                {"id": "opt_b", "option_id": "B", "content": "Correct Value", "is_correct": False}, # Collision!
                {"id": "opt_c", "option_id": "C", "content": "Distractor C", "is_correct": False},
                {"id": "opt_d", "option_id": "D", "content": "Distractor D", "is_correct": False},
                {"id": "opt_e", "option_id": "E", "content": "Distractor E", "is_correct": False},
                {"id": "opt_f", "option_id": "F", "content": "Distractor F", "is_correct": False},
                {"id": "opt_g", "option_id": "G", "content": "Distractor G", "is_correct": False},
            ],
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "solution": "Solution text",
        }
        is_valid, errs = check_instance_invariants(bad_q, "multiple_choice_7_options")
        assert not is_valid
        assert any("identical to correct answer" in e for e in errs)

    def test_template_diversity_threshold(self):
        """Masked stem diversity calculation satisfies ratio >= 0.5."""
        stems = [
            f"Given matrix A with value {i} and vector b with value {i * 2}, compute det."
            for i in range(10)
        ]
        res = evaluate_competency_diversity(stems)
        # All stems mask to the same template pattern -> diversity 0.1
        assert res["diversity_ratio"] < 0.5

        varied_stems = [
            "Given matrix A compute determinant.",
            "Determine the eigenvalues of A.",
            "Solve the system Ax = b.",
            "Is the matrix A invertible?",
            "Compute the trace of matrix A.",
        ]
        res_v = evaluate_competency_diversity(varied_stems)
        assert res_v["diversity_ratio"] >= 0.5


# =============================================================================
# CLASS 5: TestFewShotRegressionEDP_EDO (3 tests)
# =============================================================================
class TestFewShotRegressionEDP_EDO:
    """Evaluates instantiation of legacy EDP and EDO few-shot examples through generic engine."""

    def test_edp_regression_templates_generic_instantiation(self):
        """Instantiates questions for EDP few-shot competencies passing strict validator rules."""
        edp_dir = SKILL_DIR / "examples" / "edp"
        cta_p = edp_dir / "cta.json"
        assert cta_p.is_file(), f"EDP cta.json missing: {cta_p}"

        cta_data = json.loads(cta_p.read_text(encoding="utf-8"))
        assert len(cta_data["competencies"]) == 2

        # Check templates
        tpl_dir = edp_dir / "templates"
        is_valid, errs = check_templates_file_or_dir(tpl_dir, cta_path=cta_p, num_dry_run_seeds=5)
        assert is_valid, f"EDP templates failed check: {errs}"

    def test_edo_regression_templates_generic_instantiation(self):
        """Instantiates questions for EDO few-shot competencies passing strict validator rules."""
        edo_dir = SKILL_DIR / "examples" / "edo"
        cta_p = edo_dir / "cta.json"
        assert cta_p.is_file(), f"EDO cta.json missing: {cta_p}"

        cta_data = json.loads(cta_p.read_text(encoding="utf-8"))
        assert len(cta_data["competencies"]) == 2

        # Check templates
        tpl_dir = edo_dir / "templates"
        is_valid, errs = check_templates_file_or_dir(tpl_dir, cta_path=cta_p, num_dry_run_seeds=5)
        assert is_valid, f"EDO templates failed check: {errs}"

    def test_engine_zero_domain_logic(self):
        """Audits entire skill directory confirming zero domain keywords exist (excluding examples/)."""
        domain_terms = [
            "edo", "pde", "derivadas", "jacobiana", "eigen",
            "euler", "cobb_douglas", "lotka", "lagrange", "regresi",
        ]

        py_files = [
            p for p in SKILL_DIR.rglob("*.py")
            if not any(part in ("examples", "__pycache__", "courses", "work") for part in p.relative_to(SKILL_DIR).parts)
        ]
        assert len(py_files) >= 15, f"Expected >= 15 skill python files, found {len(py_files)}"

        for py_file in py_files:
            content = py_file.read_text(encoding="utf-8").lower()
            for term in domain_terms:
                assert term not in content, (
                    f"Domain term '{term}' found in skill module {py_file.relative_to(SKILL_DIR)}"
                )


# =============================================================================
# CLASS 6: TestPipelineRunnerCLI (3 tests)
# =============================================================================
class TestPipelineRunnerCLI:
    """Evaluates modular run.py CLI flags, fail-fast mechanics, and publish/append behavior."""

    def test_run_fails_without_cta_json(self, tmp_path):
        """Asserts PipelineRunner strictly terminates with non-zero error when cta.json is missing."""
        work_d = tmp_path / "empty_work"
        work_d.mkdir(parents=True, exist_ok=True)
        pre_cta = {
            "course_id": "test_fail",
            "cta_mode": "direct",
            "total_files": 1,
            "total_pages": 5,
            "files": [{"doc": "doc.pdf", "file_index": 0, "type": "pdf", "total_pages": 5}],
            "subparts": [],
        }
        (work_d / "pre_cta_manifest.json").write_text(json.dumps(pre_cta), encoding="utf-8")

        runner = PipelineRunner(
            work_dir=work_d,
            course_id="test_fail",
        )
        with pytest.raises(FileNotFoundError) as exc_info:
            runner.execute(target_stage="cta")
        assert "Missing required artifact" in str(exc_info.value)
        assert "cta.json" in str(exc_info.value)

    def test_run_stage_flags(self, tmp_path):
        """Asserts isolated execution of single stage without running subsequent stages."""
        # Create a valid cta.json in work dir
        work_d = tmp_path / "work"
        work_d.mkdir(parents=True, exist_ok=True)
        pre_cta = {
            "course_id": "test_stg",
            "cta_mode": "direct",
            "total_files": 1,
            "total_pages": 5,
            "files": [{"doc": "d.pdf", "file_index": 0, "type": "pdf", "total_pages": 5}],
            "subparts": [],
        }
        (work_d / "pre_cta_manifest.json").write_text(json.dumps(pre_cta), encoding="utf-8")
        cta_data = {
            "course_id": "test_stg",
            "title": "Stage Test",
            "macro_competency": "M",
            "competencies": [
                {
                    "id": "C-01",
                    "type": "concept",
                    "name": "C",
                    "description_latex": "Desc",
                    "bloom": "Remember",
                    "prerequisites": [],
                    "source_examples": ["Ex"],
                    "evidence": [{"doc": "d.pdf", "page": 1}],
                    "distractors": [
                        {
                            "id": f"D-C01-0{i}",
                            "name": f"D{i}",
                            "wrong_belief": "W",
                            "omitted_step": None,
                            "trigger": "T",
                            "manifestation": "M",
                            "error_type": "other",
                            "severity": "low",
                            "origin": "source",
                            "evidence": {"doc": "d.pdf", "page": 1},
                            "remediation_hint": "H",
                        }
                        for i in range(1, 4)
                    ],
                }
            ],
        }
        (work_d / "cta.json").write_text(json.dumps(cta_data), encoding="utf-8")

        runner = PipelineRunner(
            work_dir=work_d,
            course_id="test_stg",
        )
        res = runner.execute(target_stage="cta")
        # Only 'cta' ran; 'templates' and 'build' should not be in results
        assert "cta" in res
        assert "templates" not in res
        assert "build" not in res

    def test_run_publish_and_append(self, tmp_path):
        """Asserts CoursePublisher publishes course JSON and append mode merges questions without ID collisions."""
        courses_dir = tmp_path / "courses_out"
        courses_dir.mkdir(parents=True, exist_ok=True)

        base_q = {
            "id": "Q-C01-001",
            "competency_id": "C-01",
            "interaction_type": "multiple_choice_7_options",
            "stem": "First question stem with sufficient length?",
            "options": [
                {"id": "opt_a", "option_id": "A", "content": "Correct option text", "is_correct": True},
                {"id": "opt_b", "option_id": "B", "content": "Short text", "is_correct": False, "error_rationale": "Error rationale B"},
                {"id": "opt_c", "option_id": "C", "content": "Medium length text", "is_correct": False, "error_rationale": "Error rationale C"},
                {"id": "opt_d", "option_id": "D", "content": "Long distractor text", "is_correct": False, "error_rationale": "Error rationale D"},
                {"id": "opt_e", "option_id": "E", "content": "Very long distractor txt", "is_correct": False, "error_rationale": "Error rationale E"},
                {"id": "opt_f", "option_id": "F", "content": "Another distractor", "is_correct": False, "error_rationale": "Error rationale F"},
                {"id": "opt_g", "option_id": "G", "content": "Final distractor opt", "is_correct": False, "error_rationale": "Error rationale G"},
            ],
            "correct_answer": "A",
            "hints": ["Hint 1", "Hint 2", "Hint 3"],
            "detailed_solution": "Detailed solution text.",
            "common_misconception_warning": "Warning text.",
            "difficulty": "medium",
        }
        course_bank = {
            "schema_version": "1.0.0",
            "course_id": "math_app",
            "course_title": "Math Course",
            "title": "Math Course",
            "description": "Curso formativo con ejercicios interactivos.",
            "language": "es",
            "created_at": "2026-10-11T12:00:00Z",
            "competencies": [
                {
                    "id": "C-01",
                    "code": "C01",
                    "name": "Concept One",
                    "category": "Concept",
                    "description": "Description text here.",
                    "mastery_target": 100,
                }
            ],
            "questions": [copy.deepcopy(base_q) for _ in range(20)],
        }
        # Re-index uniquely
        for i, q in enumerate(course_bank["questions"]):
            q["id"] = f"Q-C01-{i+1:03d}"
            q["question_id"] = q["id"]

        publisher = CoursePublisher(courses_dir=courses_dir)
        pub_res1 = publisher.publish(course_bank, strict=False)
        assert pub_res1.success
        assert (courses_dir / "math_app.json").is_file()

        # Append additional questions
        new_bank = {
            "schema_version": "1.0.0",
            "course_id": "math_app",
            "course_title": "Math Course",
            "title": "Math Course",
            "description": "Curso formativo con ejercicios interactivos.",
            "language": "es",
            "created_at": "2026-10-11T12:00:00Z",
            "competencies": course_bank["competencies"],
            "questions": [
                {
                    "id": "Q-C01-001",  # Same ID, must be deduplicated / re-indexed
                    "competency_id": "C-01",
                    "interaction_type": "multiple_choice_7_options",
                    "stem": "New appended question stem with sufficient length?",
                    "options": copy.deepcopy(base_q["options"]),
                    "correct_answer": "A",
                    "hints": ["Hint 1", "Hint 2", "Hint 3"],
                    "detailed_solution": "Detailed solution text.",
                    "common_misconception_warning": "Warning text.",
                    "difficulty": "medium",
                }
            ],
        }

        pub_res2 = publisher.publish(new_bank, strict=False, append=True)
        assert pub_res2.success

        final_data = json.loads((courses_dir / "math_app.json").read_text(encoding="utf-8"))
        final_ids = [q["id"] for q in final_data["questions"]]
        assert len(final_ids) == 21
        assert len(set(final_ids)) == 21, "All question IDs must remain unique after append"
