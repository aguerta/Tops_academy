"""Test suite for Stage 0 Ingestion Engine in Content-to-Course (C2C) v3.2.

Certifies:
1. Zero-Waste Multiformat Ingestion: PDF page rendering, native TeX expansion, and image discovery.
2. Central Pre-CTA Manifest: Generation of work/pre_cta_manifest.json with files, subparts, cta_mode,
   and strict absence of "next_milestones_notes".
3. Absolute elimination of legacy intermediate artifacts (corpus.md, density.json, budget.json,
   vision_pages.json, order.json, pages/manifest.json, sections/*).
4. Image Tiling Threshold (> 3072x3072): Tiling occurs strictly if width > 3072 or height > 3072.
5. Natural sorting and order override mechanism.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

import pytest
from PIL import Image

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

# Ensure skill directory is in sys.path
SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from ingest import (
    compute_sha256,
    expand_tex_inputs,
    ingest_course,
    ingest_image_file,
    natural_sort_key,
    normalize_corrupt_diacritics,
    tile_large_image,
)


def create_synthetic_pdf(filepath: Path, num_pages: int = 3, prefix: str = "Slide") -> Path:
    """Helper to create synthetic test PDFs with PyMuPDF."""
    doc = pymupdf.open()
    for i in range(num_pages):
        page = doc.new_page(width=800, height=600)
        page.insert_text(pymupdf.Point(50, 100), f"{prefix} - Page {i + 1}", fontsize=24)
    doc.save(str(filepath))
    doc.close()
    return filepath


def test_stage0_ingest_multiformat_pdf_tex_image(tmp_path: Path):
    """Test Stage 0 ingest with mixed PDF, TeX, and image inputs."""
    in_dir = tmp_path / "inputs"
    in_dir.mkdir(parents=True)
    work_dir = tmp_path / "work"

    # 1. Create a 3-page PDF
    pdf_path = create_synthetic_pdf(in_dir / "lecture_01.pdf", num_pages=3, prefix="Lecture 1")

    # 2. Create a TeX file with 2 frames
    tex_path = in_dir / "notes.tex"
    tex_content = (
        "\\documentclass{beamer}\n"
        "\\begin{document}\n"
        "\\begin{frame}{First Frame}\nContent 1\n\\end{frame}\n"
        "\\begin{frame}{Second Frame}\nContent 2\n\\end{frame}\n"
        "\\end{document}\n"
    )
    tex_path.write_text(tex_content, encoding="utf-8")

    # 3. Create a small image
    img_path = in_dir / "diagram.png"
    img = Image.new("RGB", (600, 400), color="blue")
    img.save(str(img_path))

    manifest = ingest_course(
        input_path=in_dir,
        output_dir=work_dir,
        course_id="math_foundations",
        cta_mode="direct",
    )

    # Verify central pre_cta_manifest.json
    manifest_file = work_dir / "pre_cta_manifest.json"
    assert manifest_file.is_file(), "pre_cta_manifest.json was not created"

    data = json.loads(manifest_file.read_text(encoding="utf-8"))
    assert data["course_id"] == "math_foundations"
    assert data["cta_mode"] == "direct"
    assert data["total_files"] == 3
    assert len(data["files"]) == 3
    assert len(data["subparts"]) == 3

    # Assert strict absence of deprecated keys
    assert "next_milestones_notes" not in data, "pre_cta_manifest.json must NOT contain 'next_milestones_notes'"

    # Verify page images exist
    pdf_pages = list((work_dir / "pages" / "lecture_01").glob("page_*.png"))
    assert len(pdf_pages) == 3


def test_stage0_absence_of_legacy_artifacts(tmp_path: Path):
    """Verify that Stage 0 ingest eliminates all legacy intermediate artifacts."""
    in_dir = tmp_path / "inputs"
    in_dir.mkdir(parents=True)
    work_dir = tmp_path / "work"

    create_synthetic_pdf(in_dir / "test.pdf", num_pages=2)

    ingest_course(input_path=in_dir, output_dir=work_dir, course_id="clean_course")

    # Verify absence of legacy artifacts
    legacy_artifacts = [
        work_dir / "corpus.md",
        work_dir / "corpus_raw.md",
        work_dir / "density.json",
        work_dir / "vision_pages.json",
        work_dir / "budget.json",
        work_dir / "order.json",
        work_dir / "pages" / "manifest.json",
        work_dir / "sections",
    ]
    for art in legacy_artifacts:
        assert not art.exists(), f"Legacy artifact must NOT exist in C2C v3.2: {art}"


def test_stage0_image_tiling_threshold_3072px(tmp_path: Path):
    """Verify image tiling strictly occurs ONLY when width > 3072 or height > 3072."""
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True)

    # Case A: 3000x2500 (<= 3072) -> Single untiled image (page_001.png)
    small_path = tmp_path / "under_limit.png"
    img_small = Image.new("RGB", (3000, 2500), color="green")
    img_small.save(str(small_path))

    out_small = work_dir / "pages" / "under_limit"
    count_small = ingest_image_file(small_path, out_small)
    assert count_small == 1
    assert (out_small / "page_001.png").is_file()
    assert not (out_small / "overview.png").exists()

    # Case B: 3500x3200 (> 3072) -> Tiled into 3x2 grid (6 tiles) + 1 overview.png
    large_path = tmp_path / "over_limit.png"
    img_large = Image.new("RGB", (3500, 3200), color="white")
    img_large.save(str(large_path))

    out_large = work_dir / "pages" / "over_limit"
    count_large = ingest_image_file(large_path, out_large)
    assert count_large == 6
    assert (out_large / "overview.png").is_file()
    assert len(list(out_large.glob("tile_r*_c*.png"))) == 6


def test_stage0_tex_input_expansion(tmp_path: Path):
    """Verify recursive LaTeX \\input and \\include expansion."""
    main_tex = tmp_path / "main.tex"
    sub_tex = tmp_path / "chapter1.tex"

    sub_tex.write_text("Sub content with math $\\alpha = 1$.", encoding="utf-8")
    main_tex.write_text("Main content.\n\\input{chapter1.tex}\nEnd main.", encoding="utf-8")

    expanded = expand_tex_inputs(main_tex)
    assert "Main content." in expanded
    assert "Sub content with math $\\alpha = 1$." in expanded
    assert "End main." in expanded


def test_stage0_diacritics_normalization():
    """Verify normalization of corrupt Beamer LaTeX accents."""
    raw = "Ecuaci´on de distribuci´on param´etrica y funci´on"
    normalized = normalize_corrupt_diacritics(raw)
    assert normalized == "Ecuación de distribución paramétrica y función"


def test_stage0_natural_sort_and_order_override(tmp_path: Path):
    """Verify natural sorting and order override mechanism."""
    in_dir = tmp_path / "sort_inputs"
    in_dir.mkdir(parents=True)
    work_dir = tmp_path / "work"

    create_synthetic_pdf(in_dir / "lecture_10.pdf", num_pages=1)
    create_synthetic_pdf(in_dir / "lecture_2.pdf", num_pages=1)
    create_synthetic_pdf(in_dir / "lecture_1.pdf", num_pages=1)

    # Default natural sort: lecture_1, lecture_2, lecture_10
    manifest_default = ingest_course(in_dir, work_dir / "run1")
    names_default = [f["doc"] for f in manifest_default["files"]]
    assert names_default == ["lecture_1.pdf", "lecture_2.pdf", "lecture_10.pdf"]

    # Order override: lecture_10 first
    override = ["lecture_10.pdf", "lecture_1.pdf", "lecture_2.pdf"]
    manifest_custom = ingest_course(in_dir, work_dir / "run2", order_override=override)
    names_custom = [f["doc"] for f in manifest_custom["files"]]
    assert names_custom == ["lecture_10.pdf", "lecture_1.pdf", "lecture_2.pdf"]
