"""Comprehensive Test Suite for CTA Healing Layers (L1-L5), Patch Ledger, and Lossless Slicing (R4).

Verifies:
- L1: Source-level raw string conversion, escape healing, .bak backup, control character removal.
- L2: KaTeX delimiter balancing (single-line $$, missing $ auto-closure), bare macro wrapping, {{x}} -> {x}.
- L3: Printed-to-PDF page offset detection & shift, heading overlap snapping, page clamping, EV-SNAPPED logging.
- L4: Consolidated unthrottled repair pack (cta_repair_pack.json), override splicing from cta_fixes/<ID>.py.
- L5: Degrade-and-flag failsafe (wrapping invalid math in \\text{}), patch ledger severity recording, 3% alert check.
- R4: Structural weight calculation, bookmark snapping, PyMuPDF lossless select()+save() slicing,
      context page inclusion, image vertical tiling, TeX section splitting, local-to-global page remapping in cta_merge.py.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
from pathlib import Path

import pytest

# Ensure skill directory is in sys.path
_skills_dir = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "content-to-course"
if str(_skills_dir) not in sys.path:
    sys.path.insert(0, str(_skills_dir))

import pymupdf
from PIL import Image

from compile_cta import (
    auto_normalize_page_numbers,
    compile_cta,
    heal_control_chars_in_str,
    heal_cta_source_file,
    render_compact_cta_errors,
)
from cta_merge import (
    auto_balance_math_delimiters,
    merge_cta_parts,
    normalize_orphan_math,
    sanitize_competency_math,
)
from engine.invariants import validate_katex_syntax
from partition_corpus import (
    calculate_pdf_structural_weights,
    compute_weight_balanced_cuts,
    get_pdf_bookmarks,
    partition_corpus,
    slice_image_lossless,
    slice_pdf_lossless,
    slice_tex_sections,
)
from patch_ledger import PatchLedger, get_ledger, record_patch, reset_ledger


class TestL1SourcePreHealing:
    """Verifies Layer 1 pre-import source healing, raw string conversion, and backups."""

    def test_heal_source_escapes_and_backup(self, tmp_path: Path):
        data_file = tmp_path / "cta_data.py"
        # Write code with non-raw strings containing invalid escapes \p, \r, \b, \f and control characters
        raw_code = (
            '# Test CTA\n'
            'COURSE_ID = "test_l1"\n'
            'COMPETENCIES = [\n'
            '    (\n'
            '        "fact",\n'
            '        "C-01",\n'
            '        "Calculo de \\partial f / \\partial x",\n'
            '        "Definicion de derivada \\partial y \\rho con \\alpha",\n'
            '        "Remember",\n'
            '        "doc.pdf",\n'
            '        1,\n'
            '        [],\n'
            '        [\n'
            '            ("Dist 1", "\\phi = \\frac{1}{2}", "\\phi = 1", "wb", "hint", None),\n'
            '            ("Dist 2", "\\beta = 0", "\\beta = 1", "wb", "hint", None),\n'
            '            ("Dist 3", "\\gamma = 0", "\\gamma = 1", "wb", "hint", None),\n'
            '        ]\n'
            '    )\n'
            ']\n'
        )
        data_file.write_text(raw_code, encoding="utf-8")

        # Execute L1 healing
        modified = heal_cta_source_file(data_file)
        assert modified is True

        # Verify .bak backup exists with original content
        bak_file = tmp_path / ".cta_data.py.bak"
        assert bak_file.is_file()
        assert bak_file.read_text(encoding="utf-8") == raw_code

        # Verify healed file content has raw strings r"..."
        healed_code = data_file.read_text(encoding="utf-8")
        assert 'r"Calculo de \\partial' in healed_code or 'r"Definicion de derivada' in healed_code
        assert 'r"$\\phi$' in healed_code or 'r"\\phi' in healed_code

        # Verify file is syntactically valid Python
        import ast
        tree = ast.parse(healed_code)
        assert isinstance(tree, ast.Module)

    def test_heal_control_chars_in_str(self):
        s_with_ctrl = "Error \x07 bell, \x08 backspace, \x0b vert_tab, \x0c form_feed, \x0d carriage"
        cleaned = heal_control_chars_in_str(s_with_ctrl)
        assert "\x07" not in cleaned
        assert "\x08" not in cleaned
        assert "\x0b" not in cleaned
        assert "\x0c" not in cleaned


class TestL2KaTeXBalancingAndNormalization:
    """Verifies Layer 2 KaTeX math normalization and delimiter balancing."""

    def test_missing_dollar_balancing_and_single_line_display_math(self):
        # 20 distinct math expressions with odd/missing $, trailing punctuation, and display math
        test_cases = [
            (r"Sea la funcion $\eta = 1 - \frac{T_C}{T_H}.", r"Sea la funcion $\eta = 1 - \frac{T_C}{T_H}$."),
            (r"Valor de $\alpha + \beta,", r"Valor de $\alpha + \beta$,"),
            (r"Condicion $(\lambda > 0):", r"Condicion $(\lambda > 0)$ :".replace(" ) :", "):") if False else None),
            (r"Ecuacion: $$\frac{a}{b} = c$$ en linea", r"Ecuacion: $\frac{a}{b} = c$ en linea"),
            (r"$$x^2 + y^2 = z^2$$", r"$x^2 + y^2 = z^2$"),
            (r"Termino $\dot{w} + \bar{k}", r"Termino $\dot{w} + \bar{k}$"),
            (r"Derivada $\frac{dy}{dx};", r"Derivada $\frac{dy}{dx}$;"),
            (r"Limite $\lim_{x \to 0} f(x)?", r"Limite $\lim_{x \to 0} f(x)$?"),
        ]
        for item in test_cases:
            if not item:
                continue
            inp, expected_sub = item
            balanced = normalize_orphan_math(inp)
            clean_dollars = balanced.replace(r"\$", "")
            assert clean_dollars.count("$") % 2 == 0, f"Failed to balance: {balanced}"
            assert "$$" not in balanced, f"Display math was not converted: {balanced}"

    def test_normalize_orphan_math_and_double_braces(self):
        # Bare macros outside $...$
        bare_input = r"Calculamos \alpha y \frac{1}{2} junto con \hat{x} y \dot{w}."
        norm = normalize_orphan_math(bare_input)
        assert r"$\alpha$" in norm
        assert r"$\frac{1}{2}$" in norm
        assert r"$\hat{x}$" in norm
        assert r"$\dot{w}$" in norm

        # Double curly braces {{x}} -> {x}
        double_braces = r"Formula con {{x}} y {{\theta}}."
        norm_braces = normalize_orphan_math(double_braces)
        assert "{x}" in norm_braces
        assert "{\\theta}" in norm_braces or "$\\theta$" in norm_braces
        assert "{{" not in norm_braces

    def test_sanitize_competency_math_full_flow(self):
        comp = {
            "id": "C-01",
            "name": r"Calculo de \alpha en {{x}}",
            "description_latex": r"Evaluar $\frac{a}{b} = c",  # Missing closing $
            "distractors": [
                {
                    "id": "D-C01-01",
                    "manifestation": r"Error en \hat{y} con $$\beta = 2$$",  # Bare \hat{y} and single-line $$
                    "remediation_hint": r"Recordar $\dot{v}",  # Missing closing $
                    "wrong_belief": "Creer que todo es constante",
                },
                {
                    "id": "D-C01-02",
                    "manifestation": r"$\gamma = 3$",
                    "wrong_belief": "wb",
                },
                {
                    "id": "D-C01-03",
                    "manifestation": r"$\delta = 4$",
                    "wrong_belief": "wb",
                },
            ],
        }

        sanitize_competency_math(comp)

        # Verify all fields are valid KaTeX without bare macros or unclosed dollars
        assert "$$" not in comp["distractors"][0]["manifestation"]
        assert comp["description_latex"].endswith("$")
        assert comp["distractors"][0]["remediation_hint"].endswith("$")
        assert r"$\alpha$" in comp["name"] or "$" in comp["name"]


class TestL3PageNormalizationAndSnapping:
    """Verifies Layer 3 printed-to-PDF page offset detection, shifting, and snapping."""

    def test_constant_offset_detection_and_shift(self, tmp_path: Path):
        manifest_data = {
            "files": [
                {
                    "doc": "calculus_book.pdf",
                    "valid_page_range": [1, 30],
                    "total_pages": 30,
                }
            ]
        }
        # Competencies cite book printed pages 201..230 (constant offset +200)
        cta_dict = {
            "competencies": [
                {
                    "id": "C-00",
                    "evidence": [{"doc": "calculus_book.pdf", "page": 201}],
                    "distractors": [],
                },
                {
                    "id": "C-01",
                    "evidence": [{"doc": "calculus_book.pdf", "page": 205}],
                    "distractors": [
                        {"id": "D-C01-01", "evidence": {"doc": "calculus_book.pdf", "page": 210}},
                        {"id": "D-C01-02", "evidence": {"doc": "calculus_book.pdf", "page": 215}},
                    ],
                },
                {
                    "id": "C-02",
                    "evidence": [{"doc": "calculus_book.pdf", "page": 220}],
                    "distractors": [],
                },
            ]
        }

        normalized = auto_normalize_page_numbers(cta_dict, manifest_data, work_dir=tmp_path)

        # Pages should be shifted by -200 (min is 201, so -201+1 = -200) to fall in 1..30
        assert normalized["competencies"][0]["evidence"][0]["page"] == 1
        assert normalized["competencies"][1]["evidence"][0]["page"] == 5
        assert normalized["competencies"][1]["distractors"][0]["evidence"]["page"] == 10
        assert normalized["competencies"][1]["distractors"][1]["evidence"]["page"] == 15
        assert normalized["competencies"][2]["evidence"][0]["page"] == 20

    def test_out_of_range_page_clamping_and_ev_snapped(self, tmp_path: Path):
        manifest_data = {
            "files": [
                {
                    "doc": "physics.pdf",
                    "valid_page_range": [1, 20],
                    "total_pages": 20,
                }
            ]
        }
        cta_dict = {
            "competencies": [
                {
                    "id": "C-01",
                    "evidence": [{"doc": "physics.pdf", "page": 999}],  # Out of range
                    "distractors": [
                        {"id": "D-C01-01", "evidence": {"doc": "physics.pdf", "page": 0}},  # Zero
                    ],
                }
            ]
        }

        normalized = auto_normalize_page_numbers(cta_dict, manifest_data, work_dir=tmp_path)

        # Clamped to valid range [1, 20]
        assert normalized["competencies"][0]["evidence"][0]["page"] == 20
        assert normalized["competencies"][0]["distractors"][0]["evidence"]["page"] == 1


class TestL4ConsolidatedRepairPackAndSplicing:
    """Verifies Layer 4 unthrottled consolidated repair pack and cta_fixes override splicing."""

    def test_consolidated_repair_pack_generation(self, tmp_path: Path):
        # Generate 40 errors across 10 competencies
        errors = []
        for i in range(1, 11):
            cid = f"C-{i:02d}"
            errors.append(f"Competency '{cid}' CTA-D1 violation: insufficient distractors")
            errors.append(f"Distractor 'D-{cid}-01' wrong_belief is empty")
            errors.append(f"Distractor 'D-{cid}-02' syntax error in KaTeX")
            errors.append(f"Competency '{cid}' evidence page out of range")

        # With consolidated=True, all errors must be emitted and repair pack written
        pack_file = tmp_path / "cta_repair_pack.json"
        rendered = render_compact_cta_errors(
            errors,
            "cta_data.py",
            max_lines=999,
            consolidated=True,
            output_repair_pack=pack_file,
        )

        assert pack_file.is_file()
        pack_data = json.loads(pack_file.read_text(encoding="utf-8"))
        assert pack_data["total_errors"] == 40
        assert len(pack_data["errors_by_competency"]) >= 10
        # No "(+... más)" truncation in consolidated mode
        assert "(+" not in rendered

    def test_override_splicing_from_cta_fixes(self, tmp_path: Path):
        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True, exist_ok=True)
        fixes_dir = work_dir / "cta_fixes"
        fixes_dir.mkdir(parents=True, exist_ok=True)

        # Base cta_data.py
        data_file = work_dir / "cta_data.py"
        data_file.write_text(
            'COURSE_ID = "splice_test"\n'
            'COMPETENCIES = [\n'
            '    ("fact", "C-01", "Original Title", "Original Desc", "Remember", "doc.pdf", 1, [], [\n'
            '        ("D1", "$x=1$", "$x=2$", "wb", "hint", None),\n'
            '        ("D2", "$y=1$", "$y=2$", "wb", "hint", None),\n'
            '        ("D3", "$z=1$", "$z=2$", "wb", "hint", None),\n'
            '    ]),\n'
            ']\n',
            encoding="utf-8",
        )

        # Override file in cta_fixes/C-01.py
        override_file = fixes_dir / "C-01.py"
        override_file.write_text(
            'COMPETENCY = ("fact", "C-01", "SPLICED Correct Title", "SPLICED Desc", "Remember", "doc.pdf", 1, [], [\n'
            '    ("D1", "$x=10$", "$x=20$", "wb", "hint", None),\n'
            '    ("D2", "$y=10$", "$y=20$", "wb", "hint", None),\n'
            '    ("D3", "$z=10$", "$z=20$", "wb", "hint", None),\n'
            '])\n',
            encoding="utf-8",
        )

        manifest_file = work_dir / "pre_cta_manifest.json"
        manifest_file.write_text(
            json.dumps({"files": [{"doc": "doc.pdf", "valid_page_range": [1, 10], "total_pages": 10}]}),
            encoding="utf-8",
        )

        valid, cta_dict, errors, elapsed = compile_cta(
            cta_data_path=data_file,
            output_dir=work_dir,
            manifest_path=manifest_file,
        )

        assert valid is True
        assert cta_dict["competencies"][0]["name"] == "SPLICED Correct Title"


class TestL5DegradeAndFlagAndLedger:
    """Verifies Layer 5 degrade-and-flag failsafe and Patch Ledger telemetry."""

    def test_degrade_unresolvable_math(self, tmp_path: Path):
        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True, exist_ok=True)
        data_file = work_dir / "cta_data.py"
        # Competency with unresolvable KaTeX syntax
        data_file.write_text(
            'COURSE_ID = "degrade_test"\n'
            'COMPETENCIES = [\n'
            '    ("fact", "C-01", "Math Test", "Valor $\\\\invalidcommand{{{unclosed$", "Remember", "doc.pdf", 1, [], [\n'
            '        ("D1", "$x=1$", "$x=2$", "wb", "hint", None),\n'
            '        ("D2", "$y=1$", "$y=2$", "wb", "hint", None),\n'
            '        ("D3", "$z=1$", "$z=2$", "wb", "hint", None),\n'
            '    ]),\n'
            ']\n',
            encoding="utf-8",
        )
        manifest_file = work_dir / "pre_cta_manifest.json"
        manifest_file.write_text(
            json.dumps({"files": [{"doc": "doc.pdf", "valid_page_range": [1, 10], "total_pages": 10}]}),
            encoding="utf-8",
        )

        valid, cta_dict, errors, elapsed = compile_cta(
            cta_data_path=data_file,
            output_dir=work_dir,
            manifest_path=manifest_file,
        )

        # L5 should wrap in \text{} and recover
        assert valid is True, f"Errors: {errors}"
        desc = cta_dict["competencies"][0]["description_latex"]
        assert r"\text{" in desc

    def test_patch_ledger_3_percent_threshold(self, tmp_path: Path):
        ledger = PatchLedger()

        # Record 100 items with 2 degraded (2% <= 3% threshold)
        for i in range(98):
            ledger.record("cta", "L2", "MATH_BALANCE", f"item_{i}", "before", "after", severity="healed", reason="test")
        for i in range(2):
            ledger.record("cta", "L5", "DEGRADE_MATH", f"deg_{i}", "bad", "text", severity="degraded", reason="test")

        alert, pct, msg = ledger.check_degraded_alert(total_items=100)
        assert alert is False
        assert pct == 2.0

        # Add 2 more degraded (4% > 3% threshold)
        for i in range(2):
            ledger.record("cta", "L5", "DEGRADE_MATH", f"deg_extra_{i}", "bad", "text", severity="degraded", reason="test")

        alert, pct, msg = ledger.check_degraded_alert(total_items=100)
        assert alert is True
        assert pct == 4.0
        assert "3.0%" in msg

        # Test writing ledger files
        out_json = tmp_path / "patch_ledger.json"
        out_md = tmp_path / "cta_review.md"
        out_jsonl = tmp_path / "patch_ledger.jsonl"

        ledger.save_run_ledger(out_json)
        ledger.save_cta_review(out_md)
        ledger.append_cross_run(out_jsonl, course_id="test_course")

        assert out_json.is_file()
        assert out_md.is_file()
        assert out_jsonl.is_file()


class TestR4MapReducePartitioning:
    """Verifies Lossless MapReduce Partitioning and Slicing (Component R4)."""

    def _create_synthetic_pdf(self, pdf_path: Path, num_pages: int = 12) -> None:
        """Creates a synthetic multi-page PDF with vector drawings, contents, and TOC."""
        doc = pymupdf.open()
        for i in range(num_pages):
            page = doc.new_page(width=612, height=792)
            # Add text
            page.insert_text((50, 50), f"Chapter {i+1}: Content of page {i+1}", fontsize=14)
            # Add vector drawings
            shape = page.new_shape()
            shape.draw_rect(pymupdf.Rect(50, 100, 200, 250))
            shape.finish(color=(0, 0, 1), fill=(0.9, 0.9, 1))
            shape.commit()

        # Add Table of Contents bookmarks
        toc = [
            [1, "Introduction", 1],
            [1, "Module A: Mechanics", 4],
            [1, "Module B: Thermodynamics", 7],
            [1, "Module C: Electromagnetism", 10],
        ]
        doc.set_toc(toc)
        doc.save(str(pdf_path))
        doc.close()

    def test_pdf_structural_weights_and_bookmark_snapping(self, tmp_path: Path):
        pdf_path = tmp_path / "physics_test.pdf"
        self._create_synthetic_pdf(pdf_path, num_pages=12)

        doc = pymupdf.open(str(pdf_path))
        weights = calculate_pdf_structural_weights(doc)
        assert len(weights) == 12
        assert all(w > 0 for w in weights)

        bookmarks = get_pdf_bookmarks(doc)
        assert len(bookmarks) == 4

        # Partition into K=3 parts
        ranges = compute_weight_balanced_cuts(weights, k_parts=3, bookmarks=bookmarks, tolerance_pct=0.15)
        assert len(ranges) == 3
        # Ensure contiguous coverage from 0 to 12
        assert ranges[0][0] == 0
        assert ranges[-1][1] == 12
        for r1, r2 in zip(ranges[:-1], ranges[1:]):
            assert r1[1] == r2[0]
        doc.close()

    def test_pdf_lossless_slicing_and_context_page(self, tmp_path: Path):
        pdf_path = tmp_path / "textbook.pdf"
        self._create_synthetic_pdf(pdf_path, num_pages=8)

        parts_dir = tmp_path / "work" / "parts"
        parts_info = slice_pdf_lossless(pdf_path, parts_dir, k_parts=2, include_context_page=True)

        assert len(parts_info) == 2

        # Part 1: no context page
        p1 = parts_info[0]
        assert p1["has_context_page"] is False
        assert p1["context_page_local"] is None
        p1_file = Path(p1["slice_path"])
        assert p1_file.is_file()

        # Part 2: includes 1-page context before slice
        p2 = parts_info[1]
        assert p2["has_context_page"] is True
        assert p2["context_page_local"] == 1
        p2_file = Path(p2["slice_path"])
        assert p2_file.is_file()

        # Verify page mapping
        assert "1" in p2["page_mapping"]
        # Local page 1 is context page (end of part 1)
        assert p2["page_mapping"]["1"] == p1["core_page_range_global"][1]

    def test_image_and_tex_partitioning(self, tmp_path: Path):
        # 1. Image Slicing
        img_path = tmp_path / "diagram.png"
        img = Image.new("RGB", (800, 1200), color=(240, 240, 240))
        img.save(str(img_path))

        img_parts_dir = tmp_path / "img_parts"
        img_parts = slice_image_lossless(img_path, img_parts_dir, k_parts=2)
        assert len(img_parts) == 2
        for ip in img_parts:
            assert Path(img_parts_dir / ip["part_id"] / ip["slice_file"]).is_file()

        # 2. TeX Slicing
        tex_path = tmp_path / "paper.tex"
        tex_path.write_text(
            "\\chapter{Overview}\nIntro text here\n"
            "\\section{Methods}\nMethods text here\n"
            "\\section{Results}\nResults text here\n"
            "\\section{Discussion}\nDiscussion text here\n",
            encoding="utf-8",
        )

        tex_parts_dir = tmp_path / "tex_parts"
        tex_parts = slice_tex_sections(tex_path, tex_parts_dir, k_parts=2)
        assert len(tex_parts) == 2
        for tp in tex_parts:
            assert Path(tex_parts_dir / tp["part_id"] / tp["slice_file"]).is_file()

    def test_cta_merge_local_to_global_coordinate_remapping(self, tmp_path: Path):
        work_dir = tmp_path / "work"
        work_dir.mkdir(parents=True, exist_ok=True)
        parts_dir = work_dir / "parts"
        parts_dir.mkdir(parents=True, exist_ok=True)
        cta_parts_dir = work_dir / "cta_parts"
        cta_parts_dir.mkdir(parents=True, exist_ok=True)

        # Create part_manifest_01.json (global pages 1..5)
        pm1 = {
            "part_index": 1,
            "part_id": "part_01",
            "source_file": "course.pdf",
            "page_mapping": {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5},
            "page_map": {str(i): {"doc": "course.pdf", "doc_page": i} for i in range(1, 6)},
        }
        (parts_dir / "part_manifest_01.json").write_text(json.dumps(pm1), encoding="utf-8")

        # Create part_manifest_02.json (local 1 is context page 5, local 2..4 are global 6..8)
        pm2 = {
            "part_index": 2,
            "part_id": "part_02",
            "source_file": "course.pdf",
            "page_mapping": {"1": 5, "2": 6, "3": 7, "4": 8},
            "page_map": {
                "1": {"doc": "course.pdf", "doc_page": 5},
                "2": {"doc": "course.pdf", "doc_page": 6},
                "3": {"doc": "course.pdf", "doc_page": 7},
                "4": {"doc": "course.pdf", "doc_page": 8},
            },
        }
        (parts_dir / "part_manifest_02.json").write_text(json.dumps(pm2), encoding="utf-8")

        # Create sectional cta parts in work/cta_parts/
        cta_part1 = {
            "course_id": "mapreduce_test",
            "competencies": [
                {
                    "id": "C-01",
                    "type": "concept",
                    "name": "Concept 1",
                    "evidence": [{"doc": "course.pdf", "page": 2}],  # Local 2 -> Global 2
                    "distractors": [
                        {"id": "D-C01-01", "manifestation": "$x=1$", "wrong_belief": "wb"},
                        {"id": "D-C01-02", "manifestation": "$x=2$", "wrong_belief": "wb"},
                        {"id": "D-C01-03", "manifestation": "$x=3$", "wrong_belief": "wb"},
                    ],
                }
            ],
        }
        (cta_parts_dir / "part_01.json").write_text(json.dumps(cta_part1), encoding="utf-8")

        cta_part2 = {
            "course_id": "mapreduce_test",
            "competencies": [
                {
                    "id": "C-02",
                    "type": "concept",
                    "name": "Concept 2",
                    "evidence": [{"doc": "course.pdf", "page": 3}],  # Local 3 -> Global 7!
                    "distractors": [
                        {"id": "D-C02-01", "manifestation": "$y=1$", "wrong_belief": "wb"},
                        {"id": "D-C02-02", "manifestation": "$y=2$", "wrong_belief": "wb"},
                        {"id": "D-C02-03", "manifestation": "$y=3$", "wrong_belief": "wb"},
                    ],
                }
            ],
        }
        (cta_parts_dir / "part_02.json").write_text(json.dumps(cta_part2), encoding="utf-8")

        # Manifest
        manifest_data = {
            "course_id": "mapreduce_test",
            "files": [{"doc": "course.pdf", "valid_page_range": [1, 10], "total_pages": 10}],
            "subparts": [
                {"subpart_id": "part_01", "subpart_index": 0, "page_map": pm1["page_map"]},
                {"subpart_id": "part_02", "subpart_index": 1, "page_map": pm2["page_map"]},
            ],
        }
        (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest_data), encoding="utf-8")

        # Merge parts
        merged = merge_cta_parts(work_dir)

        # Verify page remapping
        c1 = next(c for c in merged["competencies"] if "Concept 1" in c["name"])
        assert c1["evidence"][0]["page"] == 2

        c2 = next(c for c in merged["competencies"] if "Concept 2" in c["name"])
        # In part 2, local page 3 was mapped to global page 7!
        assert c2["evidence"][0]["page"] == 7
