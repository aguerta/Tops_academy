"""Tests for Component 1: Handouts engine (2x2/1x2), Stitching, and Section Generation."""

import json
import math
import sys
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image
import pytest

# Ensure skill directory is in sys.path
SKILL_DIR = Path(__file__).parent.parent / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from ingest import (
    HANDOUT_MAX_SIDE_1X2,
    HANDOUT_MAX_SIDE_2X2,
    choose_cta_mode,
    create_handouts,
    generate_section_slices,
    partition_handouts,
    resolve_document_order,
    stitch_patches_to_corpus,
)


def create_synthetic_pdf(
    filepath: Path,
    num_pages: int = 4,
    width: float = 1600,
    height: float = 900,
    prefix: str = "Slide",
) -> Path:
    """Helper to create synthetic test PDFs with PyMuPDF."""
    doc = fitz.open()
    for i in range(num_pages):
        page = doc.new_page(width=width, height=height)
        page.insert_text(fitz.Point(80, 120), f"{prefix} - Page {i + 1}", fontsize=28)
    doc.save(str(filepath))
    doc.close()
    return filepath


def test_handout_grid_2x2_and_1x2(tmp_path):
    """Test 2x2 and 1x2 handout grids: dimensions respect max limits, banners are present."""
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)

    # 1. Beamer PDF (4 landscape pages: 1600x900) -> 2x2 grid
    beamer_pdf = create_synthetic_pdf(tmp_path / "beamer.pdf", num_pages=4, width=1600, height=900, prefix="Beamer")

    # 2. Ink PDF (2 portrait pages: 600x800) -> 1x2 grid
    ink_pdf = create_synthetic_pdf(tmp_path / "ink.pdf", num_pages=2, width=600, height=800, prefix="Ink")

    manifest = {
        "manifest_version": "3.0",
        "source_path": str(tmp_path.as_posix()),
        "items": [
            {"doc": "beamer.pdf", "page": 1, "kind": "beamer_text", "needs_vision": True, "pdf_path": str(beamer_pdf)},
            {"doc": "beamer.pdf", "page": 2, "kind": "beamer_text", "needs_vision": True, "pdf_path": str(beamer_pdf)},
            {"doc": "beamer.pdf", "page": 3, "kind": "beamer_text", "needs_vision": True, "pdf_path": str(beamer_pdf)},
            {"doc": "beamer.pdf", "page": 4, "kind": "beamer_text", "needs_vision": True, "pdf_path": str(beamer_pdf)},
            {"doc": "ink.pdf", "page": 1, "kind": "ink_pdf", "needs_vision": True, "pdf_path": str(ink_pdf)},
            {"doc": "ink.pdf", "page": 2, "kind": "ink_pdf", "needs_vision": True, "pdf_path": str(ink_pdf)},
        ],
    }

    res = create_handouts(work_dir, manifest, dpi=150)
    assert res["total_handouts"] == 2
    assert len(res["handouts"]) == 2

    # Verify Handout 1 (2x2)
    h1 = res["handouts"][0]
    assert h1["layout"] == "2x2"
    h1_img_path = Path(h1["image_path"])
    assert h1_img_path.is_file()
    with Image.open(h1_img_path) as im:
        assert max(im.width, im.height) <= HANDOUT_MAX_SIDE_2X2
        # Banner check: top strip has banner rectangle color (20, 24, 36)
        px = im.getpixel((20, 10))
        assert abs(px[0] - 20) <= 5 and abs(px[1] - 24) <= 5 and abs(px[2] - 36) <= 5

    h1_txt_path = Path(h1["text_support_path"])
    assert h1_txt_path.is_file()
    h1_txt = h1_txt_path.read_text(encoding="utf-8")
    assert "[DOC: beamer.pdf | PAGE: 1]" in h1_txt
    assert "[DOC: beamer.pdf | PAGE: 4]" in h1_txt

    # Verify Handout 2 (1x2)
    h2 = res["handouts"][1]
    assert h2["layout"] == "1x2"
    h2_img_path = Path(h2["image_path"])
    assert h2_img_path.is_file()
    with Image.open(h2_img_path) as im:
        assert max(im.width, im.height) <= HANDOUT_MAX_SIDE_1X2
        px = im.getpixel((20, 10))
        assert abs(px[0] - 20) <= 5 and abs(px[1] - 24) <= 5 and abs(px[2] - 36) <= 5

    h2_txt_path = Path(h2["text_support_path"])
    assert h2_txt_path.is_file()
    h2_txt = h2_txt_path.read_text(encoding="utf-8")
    assert "[DOC: ink.pdf | PAGE: 1]" in h2_txt
    assert "[DOC: ink.pdf | PAGE: 2]" in h2_txt


def test_no_cross_document_handouts(tmp_path):
    """Test that a handout never mixes pages from different documents."""
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)

    doc_a = create_synthetic_pdf(tmp_path / "doc_a.pdf", num_pages=3, width=1600, height=900, prefix="DocA")
    doc_b = create_synthetic_pdf(tmp_path / "doc_b.pdf", num_pages=3, width=1600, height=900, prefix="DocB")

    manifest = {
        "manifest_version": "3.0",
        "source_path": str(tmp_path.as_posix()),
        "items": [
            {"doc": "doc_a.pdf", "page": 1, "kind": "beamer_text", "needs_vision": True, "pdf_path": str(doc_a)},
            {"doc": "doc_a.pdf", "page": 2, "kind": "beamer_text", "needs_vision": True, "pdf_path": str(doc_a)},
            {"doc": "doc_a.pdf", "page": 3, "kind": "beamer_text", "needs_vision": True, "pdf_path": str(doc_a)},
            {"doc": "doc_b.pdf", "page": 1, "kind": "beamer_text", "needs_vision": True, "pdf_path": str(doc_b)},
            {"doc": "doc_b.pdf", "page": 2, "kind": "beamer_text", "needs_vision": True, "pdf_path": str(doc_b)},
            {"doc": "doc_b.pdf", "page": 3, "kind": "beamer_text", "needs_vision": True, "pdf_path": str(doc_b)},
        ],
    }

    res = create_handouts(work_dir, manifest)
    # doc_a has 3 pages -> 1 handout (pages 1..3 of doc_a)
    # doc_b has 3 pages -> 1 handout (pages 1..3 of doc_b)
    assert res["total_handouts"] == 2

    for h in res["handouts"]:
        docs_in_handout = {p["doc"] for p in h["pages"]}
        assert len(docs_in_handout) == 1, f"Handout {h['handout_id']} mixed documents: {docs_in_handout}"


def test_partition_handouts():
    """Test handout partitioning: K <= 6, consecutive balanced blocks."""
    # N <= 2 -> 1 agent
    s1 = partition_handouts(1)
    assert len(s1) == 1
    assert len(s1[0]["handout_ids"]) == 1

    s2 = partition_handouts(2)
    assert len(s2) == 1
    assert len(s2[0]["handout_ids"]) == 2

    # N = 7 -> K = min(6, ceil(7/6)) = 2 agents
    s7 = partition_handouts(7)
    assert len(s7) == 2
    assert len(s7[0]["handout_ids"]) == 4
    assert len(s7[1]["handout_ids"]) == 3
    # Check consecutive
    all_ids_7 = s7[0]["handout_ids"] + s7[1]["handout_ids"]
    assert all_ids_7 == [f"handout_{i+1:03d}" for i in range(7)]

    # N = 18 -> K = min(6, ceil(18/6)) = 3 agents
    s18 = partition_handouts(18)
    assert len(s18) == 3
    for shard in s18:
        assert len(shard["handout_ids"]) == 6

    # N = 40 -> K = 6 (capped at max_agents=6)
    s40 = partition_handouts(40)
    assert len(s40) == 6
    total_covered = sum(len(sh["handout_ids"]) for sh in s40)
    assert total_covered == 40
    # Balanced sizes: 40 // 6 = 6, remainder 4 -> sizes: [7, 7, 7, 7, 6, 6]
    sizes = [len(sh["handout_ids"]) for sh in s40]
    assert sizes == [7, 7, 7, 7, 6, 6]


def test_stitch_patches_to_corpus(tmp_path):
    """Test stitching patches into corpus.md: marker validation, replacement, and idempotence."""
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    handouts_dir = work_dir / "handouts"
    handouts_dir.mkdir(parents=True, exist_ok=True)
    patches_in_dir = work_dir / "handout_patches"
    patches_in_dir.mkdir(parents=True, exist_ok=True)

    corpus_initial = (
        "# Course Ingestion Corpus\n\n"
        "---\n"
        "## <<DOC: doc1.pdf | PAGE: 1 | NEEDS_VISION: YES>>\n\n"
        "Original raw PyMuPDF text on page 1\n\n"
        "---\n"
        "## <<DOC: doc1.pdf | PAGE: 2 | NEEDS_VISION: NO>>\n\n"
        "Original clean text on page 2\n\n"
    )
    (work_dir / "corpus.md").write_text(corpus_initial, encoding="utf-8")

    handouts_manifest = {
        "total_handouts": 1,
        "agents_recommended": 1,
        "handouts": [
            {
                "handout_id": "handout_001",
                "layout": "1x2",
                "pages": [{"doc": "doc1.pdf", "page": 1}],
            }
        ],
        "shards": [],
    }
    (handouts_dir / "handouts_manifest.json").write_text(json.dumps(handouts_manifest), encoding="utf-8")

    # 1. Validation failure when partial=False and patch is missing
    with pytest.raises(ValueError) as excinfo:
        stitch_patches_to_corpus(work_dir, partial=False)
    assert "handout_001" in str(excinfo.value)

    # 2. Partial=True succeeds even if patch is pending
    res_partial = stitch_patches_to_corpus(work_dir, partial=True)
    assert res_partial["stitched_pages"] == 0

    # 3. Add patch file with marker
    patch_content = (
        "## <<DOC: doc1.pdf | PAGE: 1>>\n\n"
        "Transcription with KaTeX: $\\alpha + \\beta = \\gamma$.\n"
        "Graph description: Scatter plot of regression residuals.\n"
    )
    (patches_in_dir / "patch_handout_001.md").write_text(patch_content, encoding="utf-8")

    # 4. Stitch patches
    res_stitched = stitch_patches_to_corpus(work_dir, partial=False)
    assert res_stitched["stitched_pages"] == 1
    assert (work_dir / "corpus_raw.md").is_file()

    corpus_after = (work_dir / "corpus.md").read_text(encoding="utf-8")
    assert "Original raw PyMuPDF text on page 1" not in corpus_after
    assert "$\\alpha + \\beta = \\gamma$" in corpus_after
    assert "Original clean text on page 2" in corpus_after

    # Consolidated compatibility patch
    compat_patch = work_dir / "patches" / "doc1.md"
    assert compat_patch.is_file()
    assert "## Page 1" in compat_patch.read_text(encoding="utf-8")

    # 5. Idempotence: running stitch again produces exact same output
    res_second = stitch_patches_to_corpus(work_dir, partial=False)
    corpus_second = (work_dir / "corpus.md").read_text(encoding="utf-8")
    assert corpus_after == corpus_second


def test_generate_section_slices(tmp_path):
    """Test section slicing: dominant document splitting, M <= 4 sections, and readiness."""
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    handouts_dir = work_dir / "handouts"
    handouts_dir.mkdir(parents=True, exist_ok=True)

    # Dominant doc: 24 pages, high token count
    # Minor doc: 4 pages, low token count
    doc_order = ["dominant.pdf", "minor.pdf"]
    (work_dir / "order.json").write_text(json.dumps(doc_order), encoding="utf-8")

    density_data = []
    # Dominant has 24 pages, 600 chars each -> ~1500 toks/page with vision
    for p in range(1, 25):
        density_data.append({"doc": "dominant.pdf", "page": p, "chars": 600, "needs_vision": True})
    for p in range(1, 5):
        density_data.append({"doc": "minor.pdf", "page": p, "chars": 200, "needs_vision": False})
    (work_dir / "density.json").write_text(json.dumps(density_data), encoding="utf-8")

    # Handouts for dominant doc (6 handouts of 4 pages each)
    handouts = []
    for h_i in range(1, 7):
        p_start = (h_i - 1) * 4 + 1
        p_end = h_i * 4
        handouts.append({
            "handout_id": f"handout_{h_i:03d}",
            "layout": "2x2",
            "pages": [{"doc": "dominant.pdf", "page": p} for p in range(p_start, p_end + 1)],
        })
    (handouts_dir / "handouts_manifest.json").write_text(json.dumps({"handouts": handouts}), encoding="utf-8")

    # Corpus
    corpus_parts = ["# Corpus\n\n"]
    for p in range(1, 25):
        corpus_parts.append(f"## <<DOC: dominant.pdf | PAGE: {p}>>\nContent of dominant page {p}\n\n")
    for p in range(1, 5):
        corpus_parts.append(f"## <<DOC: minor.pdf | PAGE: {p}>>\nContent of minor page {p}\n\n")
    (work_dir / "corpus.md").write_text("".join(corpus_parts), encoding="utf-8")

    # Generate sections
    res = generate_section_slices(work_dir, max_sections=4)
    total_sections = res["total_sections"]
    assert total_sections <= 4

    # Verify dominant document is split across multiple sections
    dominant_sections = [s for s in res["sections"] if "dominant.pdf" in s["docs"]]
    assert len(dominant_sections) >= 2, "Dominant document was not split"

    # Verify minor doc is NOT split across multiple sections
    minor_sections = [s for s in res["sections"] if "minor.pdf" in s["docs"]]
    assert len(minor_sections) == 1, "Non-dominant document was split"

    # Check readiness when patches are missing
    assert any(s["ready"] is False for s in res["sections"])

    # Create all required patches
    patches_dir = work_dir / "handout_patches"
    patches_dir.mkdir(parents=True, exist_ok=True)
    for h in handouts:
        (patches_dir / f"patch_{h['handout_id']}.md").write_text("Patch content", encoding="utf-8")

    # Re-run section generation: now all sections should be ready
    res_ready = generate_section_slices(work_dir, max_sections=4)
    assert all(s["ready"] is True for s in res_ready["sections"])


def test_resolve_document_order(tmp_path):
    """Test natural sort and override validation in resolve_document_order."""
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)

    # Create dummy files
    f10 = tmp_path / "lecture_10.pdf"
    f2 = tmp_path / "lecture_2.pdf"
    f1 = tmp_path / "lecture_1.pdf"
    f_img = tmp_path / "scan_3.png"

    f10.write_bytes(b"%PDF-1.4")
    f2.write_bytes(b"%PDF-1.4")
    f1.write_bytes(b"%PDF-1.4")
    f_img.write_bytes(b"\x89PNG\r\n\x1a\n")

    # 1. Default natural sort
    resolved = resolve_document_order(tmp_path, work_dir=work_dir)
    names = [p.name for p in resolved]
    assert names == ["lecture_1.pdf", "lecture_2.pdf", "lecture_10.pdf", "scan_3.png"]
    assert (work_dir / "order.json").is_file()

    # 2. Valid override list
    custom_order = ["scan_3.png", "lecture_10.pdf", "lecture_1.pdf", "lecture_2.pdf"]
    resolved_override = resolve_document_order(tmp_path, order_override=custom_order, work_dir=work_dir)
    assert [p.name for p in resolved_override] == custom_order
    order_data = json.loads((work_dir / "order.json").read_text(encoding="utf-8"))
    assert order_data == custom_order

    # 3. Invalid override: missing file
    with pytest.raises(ValueError) as exc_missing:
        resolve_document_order(tmp_path, order_override=["lecture_1.pdf", "lecture_2.pdf"], work_dir=work_dir)
    assert "Missing documents" in str(exc_missing.value)

    # 4. Invalid override: extra file
    with pytest.raises(ValueError) as exc_extra:
        resolve_document_order(
            tmp_path,
            order_override=["scan_3.png", "lecture_10.pdf", "lecture_1.pdf", "lecture_2.pdf", "ghost.pdf"],
            work_dir=work_dir,
        )
    assert "Extra documents" in str(exc_extra.value)


def test_choose_cta_mode(tmp_path):
    """Test choose_cta_mode logic: explicit user selection and size-based heuristic."""
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    b_file = work_dir / "budget.json"

    # Case 1: Explicit user says "direct" even with many handouts -> direct
    b1 = {"total_items": 10, "total_estimated_tokens": 8000, "pages_requiring_vision": 8, "total_handouts": 6}
    b_file.write_text(json.dumps(b1), encoding="utf-8")
    mode1 = choose_cta_mode(b_file, cta_mode="direct")
    assert mode1 == "direct"
    assert json.loads(b_file.read_text(encoding="utf-8"))["cta_mode"] == "direct"
    assert json.loads(b_file.read_text(encoding="utf-8"))["cta_mode_source"] == "user_explicit"

    # Case 2: Explicit user says "multiple" -> mapreduce
    mode2 = choose_cta_mode(b_file, cta_mode="multiple")
    assert mode2 == "mapreduce"
    assert json.loads(b_file.read_text(encoding="utf-8"))["cta_mode"] == "mapreduce"
    assert json.loads(b_file.read_text(encoding="utf-8"))["cta_mode_source"] == "user_explicit"

    # Case 3: Explicit user says "mapreduce" -> mapreduce
    mode3 = choose_cta_mode(b_file, cta_mode="mapreduce")
    assert mode3 == "mapreduce"
    assert json.loads(b_file.read_text(encoding="utf-8"))["cta_mode"] == "mapreduce"

    # Case 4: Heuristic auto with small corpus -> direct
    b4 = {"total_items": 12, "total_estimated_tokens": 12000, "pages_requiring_vision": 6, "total_handouts": 4}
    b_file.write_text(json.dumps(b4), encoding="utf-8")
    mode4 = choose_cta_mode(b_file, cta_mode="auto")
    assert mode4 == "direct"
    assert json.loads(b_file.read_text(encoding="utf-8"))["cta_mode_source"] == "heuristic"

    # Case 5: Heuristic auto with massive corpus -> mapreduce
    b5 = {"total_items": 55, "total_estimated_tokens": 65000, "pages_requiring_vision": 0, "total_handouts": 0}
    b_file.write_text(json.dumps(b5), encoding="utf-8")
    mode5 = choose_cta_mode(b_file, cta_mode="auto")
    assert mode5 == "mapreduce"
    assert json.loads(b_file.read_text(encoding="utf-8"))["cta_mode_source"] == "heuristic"


def test_direct_cta_with_vision_handouts(tmp_path):
    """Verifies that direct CTA mode does not cancel or eliminate vision requirements."""
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    b_file = work_dir / "budget.json"

    # Small document with 4 pages, but all 4 have heavy mathematical images requiring vision
    b_data = {
        "total_items": 4,
        "total_estimated_tokens": 6000,
        "pages_requiring_vision": 4,
        "total_handouts": 2,
    }
    b_file.write_text(json.dumps(b_data), encoding="utf-8")

    mode = choose_cta_mode(b_file, cta_mode="direct")
    assert mode == "direct"

    saved = json.loads(b_file.read_text(encoding="utf-8"))
    assert saved["cta_mode"] == "direct"
    assert saved["total_handouts"] == 2
    assert saved["pages_requiring_vision"] == 4

