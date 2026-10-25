"""Stage 0 Ingest: Zero-Waste Multiformat Ingestion Engine for content-to-course v3.2.

Features:
- Extracts page images for visual LLM processing into work/pages/<doc_slug>/page_XXX.png
- High-resolution image handling: tiles only when width > 3072 or height > 3072
- Native .tex expansion and frame extraction
- Generates a single authoritative central manifest: work/pre_cta_manifest.json
"""

import argparse
import hashlib
import json
import math
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, Union

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf
from PIL import Image

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff"}
PDF_EXTENSIONS = {".pdf"}
TEX_EXTENSIONS = {".tex"}


def compute_sha256(filepath_or_bytes: Union[str, Path, bytes]) -> str:
    """Calculate hex SHA-256 digest of file path or byte buffer."""
    h = hashlib.sha256()
    if isinstance(filepath_or_bytes, (str, Path)):
        with open(filepath_or_bytes, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
    else:
        h.update(filepath_or_bytes)
    return h.hexdigest()


def natural_sort_key(s: Union[str, Path]) -> List[Union[int, str]]:
    """Key for natural alphanumeric sorting (e.g. page1, page2, page10, lecture_01)."""
    text = Path(s).as_posix() if isinstance(s, Path) else str(s)
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r"(\d+)", text)]


def normalize_corrupt_diacritics(text: str) -> str:
    """Normalize broken accent marks common in Beamer LaTeX exports."""
    if not text:
        return ""
    replacements = [
        (r"´a", "á"), (r"´e", "é"), (r"´i", "í"), (r"´o", "ó"), (r"´u", "ú"),
        (r"´A", "Á"), (r"´E", "É"), (r"´I", "Í"), (r"´O", "Ó"), (r"´U", "Ú"),
        (r"¨u", "ü"), (r"¨U", "Ü"),
        (r"~n", "ñ"), (r"~N", "Ñ"),
        (r"´\s+([aeiouAEIOU])", r"´\1"),
    ]
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)
    return unicodedata.normalize("NFC", text)


def slugify_doc_name(name: str) -> str:
    """Convert filename or stem to clean alphanumeric slug."""
    stem = Path(name).stem
    clean = re.sub(r"[^a-zA-Z0-9_\-]", "_", stem)
    clean = re.sub(r"_+", "_", clean).strip("_")
    return clean or "document"


def tile_large_image(
    image_path: Path,
    out_dir: Path,
    doc_name: str,
    grid_cols: int = 3,
    grid_rows: int = 2,
    overlap_pct: float = 10.0,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Tile high-resolution image into a grid with overlap plus an overview thumbnail."""
    out_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(image_path) as im:
        im_rgba = im.convert("RGBA")
        width, height = im_rgba.size

        # 1. Overview thumbnail (max dimension 1500 px)
        overview_im = im_rgba.copy()
        overview_im.thumbnail((1500, 1500), Image.Resampling.LANCZOS)
        overview_path = out_dir / "overview.png"
        overview_im.save(overview_path, format="PNG")
        overview_hash = compute_sha256(overview_path)

        overview_meta = {
            "doc": doc_name,
            "page": 0,
            "kind": "image_overview",
            "sha256": overview_hash,
            "image_path": str(overview_path.as_posix()),
        }

        overlap_frac = overlap_pct / 100.0
        tile_w = int(math.ceil(width / (1.0 + (grid_cols - 1) * (1.0 - overlap_frac))))
        step_x = int(round(tile_w * (1.0 - overlap_frac)))
        tile_h = int(math.ceil(height / (1.0 + (grid_rows - 1) * (1.0 - overlap_frac))))
        step_y = int(round(tile_h * (1.0 - overlap_frac)))

        tile_metas = []
        tile_index = 1
        for r in range(grid_rows):
            y0 = r * step_y
            y1 = min(height, y0 + tile_h)
            if r == grid_rows - 1:
                y0 = max(0, height - tile_h)
                y1 = height
            for c in range(grid_cols):
                x0 = c * step_x
                x1 = min(width, x0 + tile_w)
                if c == grid_cols - 1:
                    x0 = max(0, width - tile_w)
                    x1 = width
                tile_crop = im_rgba.crop((x0, y0, x1, y1))
                tile_filename = f"tile_r{r}_c{c}.png"
                tile_filepath = out_dir / tile_filename
                tile_crop.save(tile_filepath, format="PNG")
                tile_hash = compute_sha256(tile_filepath)
                tile_metas.append({
                    "doc": doc_name,
                    "page": tile_index,
                    "kind": "image_tile",
                    "sha256": tile_hash,
                    "image_path": str(tile_filepath.as_posix()),
                })
                tile_index += 1

    return overview_meta, tile_metas


def ingest_image_file(
    image_path: Path,
    out_doc_dir: Path,
) -> int:
    """Ingests an image file. Strictly tiles ONLY if width > 3072 or height > 3072."""
    out_doc_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(image_path) as im:
        w, h = im.size

    if w > 3072 or h > 3072:
        overview, tiles = tile_large_image(image_path, out_doc_dir, image_path.name, grid_cols=3, grid_rows=2)
        return len(tiles)
    else:
        dest_path = out_doc_dir / "page_001.png"
        with Image.open(image_path) as im:
            im.save(dest_path, format="PNG")
        return 1


def expand_tex_inputs(tex_path: Path, visited: Optional[Set[str]] = None) -> str:
    """Expands \\input and \\include statements recursively in LaTeX sources."""
    if visited is None:
        visited = set()
    real_p = tex_path.resolve()
    if str(real_p) in visited or not real_p.exists():
        return ""
    visited.add(str(real_p))
    base_dir = tex_path.parent
    content = real_p.read_text(encoding="utf-8", errors="replace")

    def repl_input(match):
        sub_name = match.group(1).strip()
        if not sub_name.endswith(".tex"):
            sub_name += ".tex"
        sub_path = base_dir / sub_name
        return expand_tex_inputs(sub_path, visited)

    return re.sub(r"\\(?:input|include)\{([^}]+)\}", repl_input, content)


def ingest_tex_file(
    tex_path: Path,
    out_doc_dir: Path,
) -> int:
    """Ingests a LaTeX (.tex) source file, saving expanded frames or source."""
    out_doc_dir.mkdir(parents=True, exist_ok=True)
    full_tex = expand_tex_inputs(tex_path)

    frame_matches = list(re.finditer(r"\\begin\{frame\}(?:\[.*?\])?(?:\{.*?\})?(.*?)\\end\{frame\}", full_tex, re.DOTALL))
    if frame_matches:
        for idx, m in enumerate(frame_matches, 1):
            frame_body = m.group(1).strip()
            txt_filepath = out_doc_dir / f"frame_{idx:03d}.tex"
            txt_filepath.write_text(frame_body, encoding="utf-8")
        return len(frame_matches)
    else:
        txt_filepath = out_doc_dir / f"{tex_path.stem}.tex"
        txt_filepath.write_text(full_tex, encoding="utf-8")
        return 1


def ingest_course(
    input_path: Union[str, Path],
    output_dir: Union[str, Path],
    course_id: Optional[str] = None,
    cta_mode: str = "direct",
    dpi: int = 150,
    order_override: Optional[Union[str, List[str], Sequence[str]]] = None,
    render_pages: bool = True,
    input_files: Optional[Sequence[Union[str, Path]]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """Stage 0 Ingestion: Zero-Waste PDF page rendering and central pre_cta_manifest.json generation.

    Eliminates all legacy intermediate artifacts (corpus.md, corpus_raw.md, density.json,
    budget.json, vision_pages.json, order.json, pages/manifest.json, sections/*).
    """
    in_path = Path(input_path).resolve()
    work_dir = Path(output_dir).resolve()
    pages_dir = work_dir / "pages"
    cta_parts_dir = work_dir / "cta_parts"

    pages_dir.mkdir(parents=True, exist_ok=True)
    cta_parts_dir.mkdir(parents=True, exist_ok=True)

    # Resolve course_id
    if not course_id or course_id in ("work", "Tops_academy"):
        if in_path.is_file():
            course_id = in_path.stem
        elif in_path.is_dir() and in_path.name not in ("in", "content", "course", "work"):
            course_id = in_path.name
        else:
            parent_cand = work_dir.parent.name if work_dir.name == "work" else work_dir.name
            course_id = parent_cand if parent_cand not in ("work", "Tops_academy", ".") else "course"
    if not course_id:
        course_id = "course"

    # Normalize cta_mode: "direct" by default, or "mapreduce"
    clean_mode = str(cta_mode or "direct").strip().lower()
    if clean_mode in ("mapreduce", "map_reduce", "map-reduce", "multiple"):
        mode = "mapreduce"
    else:
        mode = "direct"

    # NOTE: If cta_mode == "mapreduce", deterministic rules or LLM arbitration to subdivide
    # files into multiple subparts are pending for a future iteration (currently 1 file = 1 subpart).

    # Discover target files
    target_files: List[Path] = []
    if input_files is not None:
        for p in input_files:
            cand = Path(p).resolve()
            if cand.is_file():
                target_files.append(cand)
            elif cand.is_dir():
                for root, _, files in os.walk(cand):
                    for f in files:
                        ext = Path(f).suffix.lower()
                        if ext in PDF_EXTENSIONS or ext in IMAGE_EXTENSIONS or ext in TEX_EXTENSIONS:
                            target_files.append(Path(root) / f)
            else:
                raise FileNotFoundError(f"Input file does not exist: {cand}")
    elif in_path.is_dir():
        for root, _, files in os.walk(in_path):
            for f in files:
                ext = Path(f).suffix.lower()
                if ext in PDF_EXTENSIONS or ext in IMAGE_EXTENSIONS or ext in TEX_EXTENSIONS:
                    target_files.append(Path(root) / f)
    elif in_path.is_file():
        target_files.append(in_path)
    else:
        raise FileNotFoundError(f"Input path does not exist: {in_path}")

    if order_override:
        norm_order_list = [unicodedata.normalize("NFC", Path(x).name.lower()) for x in order_override] if isinstance(order_override, (list, tuple)) else [unicodedata.normalize("NFC", str(order_override).lower())]

        def sort_key(f: Path):
            fname = unicodedata.normalize("NFC", f.name.lower())
            fstem = unicodedata.normalize("NFC", f.stem.lower())
            try:
                return (0, norm_order_list.index(fname))
            except ValueError:
                try:
                    return (0, norm_order_list.index(fstem))
                except ValueError:
                    return (1, natural_sort_key(f))

        target_files = sorted(target_files, key=sort_key)
    else:
        target_files = sorted(target_files, key=natural_sort_key)

    files_manifest: List[Dict[str, Any]] = []
    subparts_manifest: List[Dict[str, Any]] = []
    total_pages_sum = 0
    seen_slugs: Dict[str, int] = {}

    for file_idx, fpath in enumerate(target_files):
        ext = fpath.suffix.lower()
        doc_name = fpath.name
        base_slug = slugify_doc_name(doc_name)
        if base_slug in seen_slugs:
            seen_slugs[base_slug] += 1
            doc_slug = f"{base_slug}_{seen_slugs[base_slug]}"
        else:
            seen_slugs[base_slug] = 1
            doc_slug = base_slug

        out_doc_dir = pages_dir / doc_slug

        size_bytes = fpath.stat().st_size
        file_type = "pdf" if ext in PDF_EXTENSIONS else ("tex" if ext in TEX_EXTENSIONS else "image")
        num_pages = 1

        if file_type == "pdf":
            doc = pymupdf.open(fpath)
            num_pages = len(doc)
            if render_pages:
                out_doc_dir.mkdir(parents=True, exist_ok=True)
                zoom = dpi / 72.0
                matrix = pymupdf.Matrix(zoom, zoom)
                for p_idx in range(num_pages):
                    page_num = p_idx + 1
                    page = doc[p_idx]
                    pix = page.get_pixmap(matrix=matrix)
                    img_path = out_doc_dir / f"page_{page_num:03d}.png"
                    pix.save(str(img_path))
            doc.close()
        elif file_type == "image":
            out_doc_dir.mkdir(parents=True, exist_ok=True)
            num_pages = ingest_image_file(fpath, out_doc_dir)
        elif file_type == "tex":
            out_doc_dir.mkdir(parents=True, exist_ok=True)
            num_pages = ingest_tex_file(fpath, out_doc_dir)

        total_pages_sum += num_pages
        valid_range = [1, num_pages]

        file_entry = {
            "file_index": file_idx,
            "doc": doc_name,
            "doc_slug": doc_slug,
            "type": file_type,
            "path": fpath.as_posix(),
            "size_bytes": size_bytes,
            "total_pages": num_pages,
            "valid_page_range": valid_range,
        }
        files_manifest.append(file_entry)

        subpart_id = f"part_{file_idx + 1:02d}"
        subpart_entry = {
            "subpart_id": subpart_id,
            "subpart_index": file_idx,
            "doc": doc_name,
            "doc_slug": doc_slug,
            "file_index": file_idx,
            "path": fpath.as_posix(),
            "type": file_type,
            "page_range": valid_range,
            "total_pages": num_pages,
            "cta_data_path": (cta_parts_dir / f"{subpart_id}_data.py").as_posix(),
            "cta_out_path": (cta_parts_dir / f"{subpart_id}.json").as_posix(),
        }
        subparts_manifest.append(subpart_entry)

    manifest_payload = {
        "course_id": course_id,
        "cta_mode": mode,
        "total_files": len(files_manifest),
        "total_pages": total_pages_sum,
        "files": files_manifest,
        "subparts": subparts_manifest,
    }

    manifest_file = work_dir / "pre_cta_manifest.json"
    manifest_file.write_text(
        json.dumps(manifest_payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return manifest_payload


def main():
    parser = argparse.ArgumentParser(description="Stage 0 Zero-Waste Multiformat Ingestion Engine")
    parser.add_argument("--input", required=True, help="Input directory or file path")
    parser.add_argument("--output-dir", "--work", dest="output_dir", required=True, help="Output work directory")
    parser.add_argument("--course-id", default=None, help="Optional course ID")
    parser.add_argument("--cta-mode", choices=["direct", "mapreduce"], default="direct", help="CTA execution mode")
    parser.add_argument("--dpi", type=int, default=150, help="DPI for PDF page rendering (default 150)")
    parser.add_argument("--render-pages", dest="render_pages", action="store_true", default=False, help="Render PDF pages to PNG (default False)")
    parser.add_argument("--no-render-pages", dest="render_pages", action="store_false", help="Do not render PDF pages to PNG")
    args = parser.parse_args()

    manifest = ingest_course(
        input_path=args.input,
        output_dir=args.output_dir,
        course_id=args.course_id,
        cta_mode=args.cta_mode,
        dpi=args.dpi,
        render_pages=args.render_pages,
    )
    print(f"[+] Ingestion complete: {manifest['total_files']} files, {manifest['total_pages']} pages processed.")
    print(f"[+] Manifest written to: {Path(args.output_dir) / 'pre_cta_manifest.json'} (cta_mode={manifest['cta_mode']})")


if __name__ == "__main__":
    main()
