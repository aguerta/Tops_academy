#!/usr/bin/env python3
"""Lossless MapReduce Partitioning and Slicing Engine for Top's Academy C2C Pipeline.

Implements Component R4 of Gate 1:
- Structural Weight Analysis: content stream size, vector strokes, ink/image density
  strictly without text extraction.
- Weight-Balanced Sequential Partitioning into K in [2, 4] contiguous ranges.
- Bookmark Snapping: snaps cuts to PDF bookmarks (doc.get_toc()) within +/- 10%.
- Lossless Physical Slicing via PyMuPDF select() + save() into work/parts/part_NN/.
- 1-page read-only context before each slice (for part > 1).
- Image source tiling via lossless pixel cropping (PIL).
- TeX source splitting at \\section / \\chapter boundaries.
- Local-to-global page coordinate mapping recorded in part_manifest_NN.json.
- Generates work/pages_index.md and updates work/pre_cta_manifest.json.
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

try:
    import pymupdf  # type: ignore
except ImportError:
    try:
        import fitz as pymupdf  # type: ignore
    except ImportError:
        pymupdf = None

try:
    from PIL import Image  # type: ignore
except ImportError:
    Image = None

logger = logging.getLogger("partition_corpus")
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def calculate_pdf_structural_weights(doc: Any) -> List[float]:
    """Calculates structural weight for each page of a PDF document without extracting text.

    Weight components:
    - Content stream size: len(page.read_contents())
    - Vector strokes: len(page.get_drawings()) * 500
    - Ink / Image density: len(page.get_images()) * 2000
    """
    weights: List[float] = []
    num_pages = len(doc)
    for p_idx in range(num_pages):
        page = doc[p_idx]
        stream_bytes = 0
        try:
            contents = page.read_contents()
            if contents:
                stream_bytes = len(contents)
        except Exception:
            stream_bytes = 0

        drawings_count = 0
        try:
            drawings = page.get_drawings()
            drawings_count = len(drawings)
        except Exception:
            drawings_count = 0

        images_count = 0
        try:
            images = page.get_images()
            images_count = len(images)
        except Exception:
            images_count = 0

        # Structural weight strictly from document structural primitives
        weight = float(stream_bytes) + (500.0 * drawings_count) + (2000.0 * images_count)
        weights.append(max(1.0, weight))
    return weights


def get_pdf_bookmarks(doc: Any) -> List[Dict[str, Any]]:
    """Extracts table of contents bookmarks from PDF with 0-indexed page targets."""
    bookmarks: List[Dict[str, Any]] = []
    try:
        toc = doc.get_toc()  # [[lvl, title, page_1_indexed, ...], ...]
        for item in toc:
            if len(item) >= 3:
                lvl, title, p_1 = item[0], item[1], item[2]
                if isinstance(p_1, int) and 1 <= p_1 <= len(doc):
                    bookmarks.append({
                        "level": lvl,
                        "title": str(title).strip(),
                        "page_1_indexed": p_1,
                        "page_0_indexed": p_1 - 1,
                    })
    except Exception as e:
        logger.debug("Failed to read TOC: %s", e)
    return bookmarks


def compute_weight_balanced_cuts(
    page_weights: List[float],
    k_parts: int,
    bookmarks: Optional[List[Dict[str, Any]]] = None,
    tolerance_pct: float = 0.10,
) -> List[Tuple[int, int]]:
    """Computes K contiguous page ranges [start_idx, end_idx) balanced by structural weight.

    Snaps partition cuts to the nearest PDF bookmark within +/- tolerance_pct of page range.
    """
    total_pages = len(page_weights)
    if total_pages == 0:
        return []
    if k_parts <= 1 or total_pages < k_parts:
        return [(0, total_pages)]

    total_weight = sum(page_weights)
    target_weight_per_part = total_weight / float(k_parts)

    # 1. Compute raw cuts based on cumulative weight
    raw_cuts: List[int] = []
    accum = 0.0
    current_target = target_weight_per_part
    for idx, w in enumerate(page_weights):
        accum += w
        if len(raw_cuts) < k_parts - 1 and accum >= current_target:
            raw_cuts.append(idx + 1)  # boundary after idx
            current_target += target_weight_per_part

    # Ensure we have k_parts - 1 cuts
    while len(raw_cuts) < k_parts - 1:
        prev = raw_cuts[-1] if raw_cuts else 0
        next_cut = prev + max(1, (total_pages - prev) // (k_parts - len(raw_cuts)))
        raw_cuts.append(min(total_pages - 1, next_cut))

    # 2. Snap cuts to bookmarks within +/- 10% tolerance
    bookmark_pages = [bm["page_0_indexed"] for bm in (bookmarks or [])]
    tol_pages = max(1, int(round(total_pages * tolerance_pct)))

    snapped_cuts: List[int] = []
    prev_cut = 0
    for cut in raw_cuts:
        best_cut = cut
        min_dist = tol_pages + 1
        for bm_p in bookmark_pages:
            dist = abs(bm_p - cut)
            if dist <= tol_pages and bm_p > prev_cut and bm_p < total_pages:
                if dist < min_dist:
                    min_dist = dist
                    best_cut = bm_p

        # Ensure strictly increasing
        if best_cut <= prev_cut:
            best_cut = prev_cut + 1
        if best_cut >= total_pages:
            best_cut = total_pages - 1

        snapped_cuts.append(best_cut)
        prev_cut = best_cut

    # 3. Form [start, end) intervals
    ranges: List[Tuple[int, int]] = []
    start = 0
    for cut in snapped_cuts:
        if cut > start:
            ranges.append((start, cut))
            start = cut
    if start < total_pages:
        ranges.append((start, total_pages))

    return ranges


def slice_pdf_lossless(
    source_pdf: Union[str, Path],
    output_dir: Union[str, Path],
    k_parts: Optional[int] = None,
    include_context_page: bool = True,
) -> List[Dict[str, Any]]:
    """Losslessly partitions a PDF file into K contiguous slices using PyMuPDF select() + save()."""
    if pymupdf is None:
        raise RuntimeError("pymupdf (or fitz) is required for lossless PDF slicing.")

    source_path = Path(source_pdf).resolve()
    out_path = Path(output_dir).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(str(source_path))
    total_pages = len(doc)

    if k_parts is None:
        # Determine K dynamically in [2, 4]
        if total_pages <= 4:
            k_parts = 2
        elif total_pages <= 12:
            k_parts = 3
        else:
            k_parts = 4
    k_parts = max(2, min(4, k_parts))
    if total_pages < k_parts:
        k_parts = max(1, total_pages)

    page_weights = calculate_pdf_structural_weights(doc)
    bookmarks = get_pdf_bookmarks(doc)
    ranges = compute_weight_balanced_cuts(page_weights, k_parts, bookmarks=bookmarks)

    parts_info: List[Dict[str, Any]] = []

    for k, (start_idx, end_idx) in enumerate(ranges, 1):
        part_id = f"part_{k:02d}"
        part_dir = out_path / part_id
        part_dir.mkdir(parents=True, exist_ok=True)

        # Context page: 1 page before start_idx if start_idx > 0
        has_context = include_context_page and (start_idx > 0)
        pages_to_extract = ([start_idx - 1] + list(range(start_idx, end_idx))) if has_context else list(range(start_idx, end_idx))

        slice_filename = f"{source_path.stem}_{part_id}.pdf"
        slice_filepath = part_dir / slice_filename

        # Lossless slice via clean insert_pdf (immune to MuPDF in-place select() mutation crash on Windows)
        slice_doc = pymupdf.open()
        for p in pages_to_extract:
            slice_doc.insert_pdf(doc, from_page=p, to_page=p)
        # Preserve original streams and objects without lossy recompression
        slice_doc.save(str(slice_filepath), garbage=3, deflate=True)
        slice_doc.close()

        # Build local (1-indexed) to global (1-indexed) page mapping
        page_mapping: Dict[str, int] = {}
        page_map_detailed: Dict[str, Dict[str, Any]] = {}
        for local_idx, orig_p_0 in enumerate(pages_to_extract, 1):
            global_p_1 = orig_p_0 + 1
            page_mapping[str(local_idx)] = global_p_1
            page_map_detailed[str(local_idx)] = {
                "doc": source_path.name,
                "doc_page": global_p_1,
                "is_context": bool(has_context and local_idx == 1),
            }

        core_start_local = 2 if has_context else 1
        core_end_local = len(pages_to_extract)

        manifest = {
            "part_index": k,
            "part_id": part_id,
            "source_file": source_path.name,
            "source_path": str(source_path),
            "slice_pdf": slice_filename,
            "slice_path": str(slice_filepath),
            "has_context_page": has_context,
            "context_page_local": 1 if has_context else None,
            "context_page_global": start_idx if has_context else None,
            "core_page_range_local": [core_start_local, core_end_local],
            "core_page_range_global": [start_idx + 1, end_idx],
            "page_count": len(pages_to_extract),
            "total_pages": len(pages_to_extract),
            "page_mapping": page_mapping,
            "page_map": page_map_detailed,
            "valid_page_range": [1, len(pages_to_extract)],
            "weight": sum(page_weights[start_idx:end_idx]),
        }

        # Write part_manifest_NN.json
        manifest_file = part_dir / f"part_manifest_{k:02d}.json"
        manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

        parts_info.append(manifest)

    doc.close()
    return parts_info


def slice_image_lossless(
    source_img_path: Union[str, Path],
    output_dir: Union[str, Path],
    k_parts: int = 2,
    context_overlap_px: int = 50,
) -> List[Dict[str, Any]]:
    """Losslessly slices an image into K vertical tiles without JPEG re-encoding."""
    if Image is None:
        raise RuntimeError("Pillow (PIL) is required for image slicing.")

    img_path = Path(source_img_path).resolve()
    out_path = Path(output_dir).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    with Image.open(str(img_path)) as img:
        width, height = img.size
        format_name = img.format or "PNG"

        k_parts = max(2, min(4, k_parts))
        step_h = height // k_parts
        parts_info: List[Dict[str, Any]] = []

        for k in range(1, k_parts + 1):
            part_id = f"part_{k:02d}"
            part_dir = out_path / part_id
            part_dir.mkdir(parents=True, exist_ok=True)

            y_top = max(0, (k - 1) * step_h - (context_overlap_px if k > 1 else 0))
            y_bottom = height if k == k_parts else k * step_h

            crop_box = (0, y_top, width, y_bottom)
            tile = img.crop(crop_box)

            # Preserve lossless PNG or matching format
            out_ext = ".png" if format_name.upper() in ("PNG", "WEBP") else ".png"
            tile_filename = f"{img_path.stem}_{part_id}{out_ext}"
            tile_filepath = part_dir / tile_filename
            tile.save(str(tile_filepath), format="PNG")

            manifest = {
                "part_index": k,
                "part_id": part_id,
                "source_file": img_path.name,
                "slice_file": tile_filename,
                "crop_box": list(crop_box),
                "original_size": [width, height],
                "page_count": 1,
                "total_pages": 1,
                "valid_page_range": [1, 1],
                "page_mapping": {"1": k},
                "page_map": {"1": {"doc": img_path.name, "doc_page": k}},
            }
            manifest_file = part_dir / f"part_manifest_{k:02d}.json"
            manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
            parts_info.append(manifest)

    return parts_info


def slice_tex_sections(
    source_tex_path: Union[str, Path],
    output_dir: Union[str, Path],
    k_parts: int = 2,
) -> List[Dict[str, Any]]:
    """Splits a LaTeX .tex file at \\section or \\chapter boundaries into K parts."""
    tex_path = Path(source_tex_path).resolve()
    out_path = Path(output_dir).resolve()
    out_path.mkdir(parents=True, exist_ok=True)

    text = tex_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Locate sectioning boundaries
    sec_pattern = re.compile(r"^\s*\\(?:chapter|section)\*?\{([^}]+)\}")
    split_lines: List[int] = [0]
    sec_titles: List[str] = ["Preamble / Start"]

    for idx, line in enumerate(lines):
        m = sec_pattern.match(line)
        if m and idx > 0:
            split_lines.append(idx)
            sec_titles.append(m.group(1).strip())

    split_lines.append(len(lines))

    num_sections = len(split_lines) - 1
    k_parts = max(2, min(4, k_parts))
    if num_sections < k_parts:
        k_parts = max(1, num_sections)

    # Divide sections into K chunks
    secs_per_chunk = math.ceil(num_sections / k_parts)
    parts_info: List[Dict[str, Any]] = []

    for k in range(1, k_parts + 1):
        part_id = f"part_{k:02d}"
        part_dir = out_path / part_id
        part_dir.mkdir(parents=True, exist_ok=True)

        sec_start = (k - 1) * secs_per_chunk
        sec_end = min(num_sections, k * secs_per_chunk)
        if sec_start >= num_sections:
            break

        line_start = split_lines[sec_start]
        line_end = split_lines[sec_end]
        part_content = "".join(lines[line_start:line_end])

        part_filename = f"{tex_path.stem}_{part_id}.tex"
        part_filepath = part_dir / part_filename
        part_filepath.write_text(part_content, encoding="utf-8")

        manifest = {
            "part_index": k,
            "part_id": part_id,
            "source_file": tex_path.name,
            "slice_file": part_filename,
            "section_range": [sec_start + 1, sec_end],
            "sections": sec_titles[sec_start:sec_end],
            "line_range": [line_start + 1, line_end],
            "page_count": sec_end - sec_start,
            "total_pages": sec_end - sec_start,
            "valid_page_range": [1, sec_end - sec_start],
            "page_mapping": {str(i + 1): sec_start + i + 1 for i in range(sec_end - sec_start)},
            "page_map": {
                str(i + 1): {"doc": tex_path.name, "doc_page": sec_start + i + 1}
                for i in range(sec_end - sec_start)
            },
        }
        manifest_file = part_dir / f"part_manifest_{k:02d}.json"
        manifest_file.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
        parts_info.append(manifest)

    return parts_info


def generate_pages_index_md(
    parts_info: List[Dict[str, Any]],
    work_dir: Union[str, Path],
    source_name: str,
) -> Path:
    """Generates work/pages_index.md documenting local to global page coordinates."""
    work_p = Path(work_dir).resolve()
    out_file = work_p / "pages_index.md"

    lines = [
        f"# Index of Partitions and Pages for {source_name}",
        "",
        f"- **Total Slices**: {len(parts_info)}",
        "- **Strategy**: Structural Weight-Balanced Partitioning (PyMuPDF lossless)",
        "",
        "| Part ID | Slice File | Core Global Pages | Local Pages | Context Page | Weight / Size |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for p in parts_info:
        pid = p.get("part_id", "")
        sfile = p.get("slice_pdf") or p.get("slice_file", "")
        core_g = p.get("core_page_range_global", ["-", "-"] )
        core_str = f"Pages {core_g[0]}–{core_g[1]}" if isinstance(core_g, list) and len(core_g) == 2 else "-"
        loc_cnt = p.get("page_count", 1)
        ctx = f"Global Page {p.get('context_page_global')}" if p.get("has_context_page") else "None (Part 1)"
        w = round(p.get("weight", 0), 1)
        w_str = f"{w:,.0f}" if w > 0 else "-"
        lines.append(f"| `{pid}` | `{sfile}` | {core_str} | 1..{loc_cnt} | {ctx} | {w_str} |")

    lines.append("")
    lines.append("## Coordinate Remapping Reference")
    lines.append("During `cta_merge.py`, competencies and distractors citing slice-local page numbers are automatically remapped to global PDF coordinates.")
    lines.append("")

    out_file.write_text("\n".join(lines), encoding="utf-8")
    return out_file


def update_pre_cta_manifest(
    work_dir: Union[str, Path],
    parts_info: List[Dict[str, Any]],
    source_name: str,
    course_id: Optional[str] = None,
) -> Path:
    """Creates or updates work/pre_cta_manifest.json with partition metadata."""
    work_p = Path(work_dir).resolve()
    manifest_p = work_p / "pre_cta_manifest.json"

    manifest_data: Dict[str, Any] = {}
    if manifest_p.is_file():
        try:
            manifest_data = json.loads(manifest_p.read_text(encoding="utf-8"))
        except Exception:
            manifest_data = {}

    course_id = course_id or manifest_data.get("course_id") or Path(source_name).stem.lower()
    manifest_data["course_id"] = course_id
    manifest_data["partitioned"] = True
    manifest_data["parts_count"] = len(parts_info)

    subparts = []
    for p in parts_info:
        subparts.append({
            "subpart_id": p.get("part_id"),
            "subpart_index": p.get("part_index", 1) - 1,
            "slice_file": p.get("slice_pdf") or p.get("slice_file"),
            "source_doc": p.get("source_file"),
            "core_page_range": p.get("core_page_range_global"),
            "page_map": p.get("page_map"),
            "page_mapping": p.get("page_mapping"),
            "total_pages": p.get("page_count"),
        })

    manifest_data["subparts"] = subparts

    # Ensure files list includes the source file
    files = manifest_data.get("files", [])
    if not any(f.get("doc") == source_name for f in files):
        total_p = sum(p.get("page_count", 1) for p in parts_info)
        files.append({
            "doc": source_name,
            "doc_slug": Path(source_name).stem.lower(),
            "file_index": 0,
            "total_pages": total_p,
            "valid_page_range": [1, total_p],
        })
    manifest_data["files"] = files

    manifest_p.write_text(json.dumps(manifest_data, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest_p


def partition_corpus(
    corpus_path: Union[str, Path],
    work_dir: Union[str, Path],
    k_parts: Optional[int] = None,
    course_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Primary entry point: partitions corpus into weight-balanced slices into work/parts/."""
    c_path = Path(corpus_path).resolve()
    w_dir = Path(work_dir).resolve()
    w_dir.mkdir(parents=True, exist_ok=True)
    parts_dir = w_dir / "parts"
    parts_dir.mkdir(parents=True, exist_ok=True)

    if not c_path.exists():
        raise FileNotFoundError(f"Corpus path not found: {c_path}")

    # If c_path is a directory, pick first eligible PDF or image
    if c_path.is_dir():
        pdfs = list(c_path.glob("*.pdf"))
        if pdfs:
            target_file = pdfs[0]
        else:
            images = list(c_path.glob("*.png")) + list(c_path.glob("*.jpg"))
            if images:
                target_file = images[0]
            else:
                texs = list(c_path.glob("*.tex"))
                if texs:
                    target_file = texs[0]
                else:
                    raise FileNotFoundError(f"No PDF, image, or TeX files found in directory: {c_path}")
    else:
        target_file = c_path

    ext = target_file.suffix.lower()
    if ext == ".pdf":
        parts_info = slice_pdf_lossless(target_file, parts_dir, k_parts=k_parts)
    elif ext in (".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"):
        parts_info = slice_image_lossless(target_file, parts_dir, k_parts=k_parts or 2)
    elif ext in (".tex", ".latex"):
        parts_info = slice_tex_sections(target_file, parts_dir, k_parts=k_parts or 2)
    else:
        raise ValueError(f"Unsupported file format for partitioning: {ext}")

    generate_pages_index_md(parts_info, w_dir, target_file.name)
    update_pre_cta_manifest(w_dir, parts_info, target_file.name, course_id=course_id)
    return parts_info


def main():
    parser = argparse.ArgumentParser(description="Lossless MapReduce Corpus Partitioning Engine")
    parser.add_argument("corpus", help="Path to source PDF, image, or TeX file, or corpus folder")
    parser.add_argument("--work", "--work-dir", dest="work", required=True, help="Work directory")
    parser.add_argument("--parts", "-k", type=int, default=None, help="Number of parts (2..4)")
    parser.add_argument("--course-id", default=None, help="Course identifier")
    args = parser.parse_args()

    parts = partition_corpus(args.corpus, args.work, k_parts=args.parts, course_id=args.course_id)
    print(f"SUCCESS: Partitioned {args.corpus} into {len(parts)} parts in {Path(args.work) / 'parts'}")
    for p in parts:
        print(f"  - {p['part_id']}: pages {p.get('core_page_range_global', p.get('page_count'))} ({p.get('slice_pdf', p.get('slice_file'))})")


if __name__ == "__main__":
    main()
