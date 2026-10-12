"""Multiformat Ingestion & Pre-processing Engine for content-to-course v3.

Features:
- Cascading multiformat ingestion (PDF, Beamer LaTeX, Vector Ink, Images, .tex sources)
- Intelligent Beamer cleanup: BBox header/footer noise removal
- Mathematical density & corruption scoring: detects CMEX fonts, broken diacritics, and complex vector plots
- Hybrid Vision Dispatch: selectively renders PNGs only for pages needing visual interpretation
- Single-pass Corpus Assembly: synthesizes clean `corpus.md`, `density.json`, and `budget.json`
- Native `.tex` ingestion with frame/section decomposition and TikZ detection
- 100% backward compatibility for `manifest.json` schema and legacy transcription mode
"""

import argparse
import datetime
import hashlib
import json
import math
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont


HANDOUT_MAX_SIDE_2X2 = 2400
HANDOUT_MAX_SIDE_1X2 = 3200

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


def normalize_corrupt_diacritics(text: str) -> str:
    """Normalize broken accent marks common in Beamer LaTeX exports.
    
    Examples: Secci´on -> Sección, Te´orico -> Teórico, ˆx -> x̂
    """
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

    # Normalize unicode combinations
    text = unicodedata.normalize("NFC", text)
    return text


def clean_beamer_text(page: fitz.Page) -> str:
    """Extract and clean text from Beamer slide, stripping repetitive navigation/footers."""
    page_rect = page.rect
    height = page_rect.height if page_rect.height > 0 else 1.0

    try:
        page_dict = page.get_text("dict")
        blocks = page_dict.get("blocks", [])
    except Exception:
        return normalize_corrupt_diacritics(page.get_text())

    clean_lines: List[str] = []
    for b in blocks:
        if b.get("type") != 0:  # not text
            continue
        bbox = b.get("bbox", (0, 0, 0, 0))
        y0, y1 = bbox[1], bbox[3]

        # Strip standard Beamer bottom footer (e.g. "Author (Uni) Slide 13 / 29")
        if y0 > height * 0.91:
            raw_footer = " ".join("".join(s.get("text", "") for s in l.get("spans", [])) for l in b.get("lines", []))
            if re.search(r"\d+\s*/\s*\d+|UNMSM|Universidad|\bSlide\b|\b202\d\b", raw_footer, re.I):
                continue

        for line in b.get("lines", []):
            line_str = "".join(span.get("text", "") for span in line.get("spans", []))
            if line_str.strip():
                clean_lines.append(line_str)

    text = "\n".join(clean_lines)
    return normalize_corrupt_diacritics(text)


def analyze_page_density(
    page: fitz.Page,
    page_num: int,
    doc_name: str,
) -> Dict[str, Any]:
    """Calculate content density, drawing counts, math fonts, and needs_vision flag."""
    raw_text = clean_beamer_text(page)
    char_count = len(raw_text.strip())

    try:
        images_count = len(page.get_images())
    except Exception:
        images_count = 0

    try:
        drawings_count = len(page.get_drawings())
    except Exception:
        drawings_count = 0

    try:
        fonts = page.get_fonts()
        font_names = [f[3] for f in fonts if len(f) > 3]
    except Exception:
        font_names = []

    has_cmex = any("CMEX" in fn or "CMSY" in fn for fn in font_names)
    broken_math = bool(re.search(r"[´¨ˆ˜]|⏞|⏟|\[︁|\]︁|\[︂|\bIk\b|\bIn\b", raw_text))
    is_ink = (char_count < 50 and drawings_count > 150)

    # Heuristic for needs_vision
    needs_vision = False
    reasons = []

    if is_ink:
        needs_vision = True
        reasons.append("vector_ink_or_handwriting")
    if images_count > 0:
        needs_vision = True
        reasons.append("embedded_images")
    if drawings_count > 450:
        needs_vision = True
        reasons.append("complex_vector_drawings_or_diagrams")
    if has_cmex and broken_math:
        needs_vision = True
        reasons.append("deconstructed_latex_math_formulas")
    if char_count < 150 and (drawings_count > 30 or broken_math):
        needs_vision = True
        reasons.append("sparse_fragmented_formula_content")

    return {
        "doc": doc_name,
        "page": page_num,
        "chars": char_count,
        "n_images": images_count,
        "n_drawings": drawings_count,
        "is_ink": is_ink,
        "has_cmex_fonts": has_cmex,
        "broken_math_patterns": broken_math,
        "needs_vision": needs_vision,
        "reasons": reasons,
        "extracted_text": raw_text,
    }


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

        # 1. Generate overview thumbnail (max dimension 1500 px)
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
            "render_dpi": None,
            "tile": None,
            "has_text_layer": False,
            "image_path": str(overview_path.as_posix()),
            "text_layer_path": None,
            "transcription_path": str((out_dir / "overview.md").as_posix()),
            "needs_vision": True,
        }

        # 2. Compute tile boundaries with overlap
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

                tile_meta = {
                    "doc": doc_name,
                    "page": tile_index,
                    "kind": "image_tile",
                    "sha256": tile_hash,
                    "render_dpi": None,
                    "tile": {
                        "row": r,
                        "col": c,
                        "rows": grid_rows,
                        "cols": grid_cols,
                        "overlap_pct": overlap_pct,
                        "box": [x0, y0, x1, y1],
                    },
                    "has_text_layer": False,
                    "image_path": str(tile_filepath.as_posix()),
                    "text_layer_path": None,
                    "transcription_path": str((out_dir / f"tile_r{r}_c{c}.md").as_posix()),
                    "needs_vision": True,
                }
                tile_metas.append(tile_meta)
                tile_index += 1

    return overview_meta, tile_metas


def process_image_file(
    image_path: Path,
    pages_base_dir: Path,
) -> List[Dict[str, Any]]:
    """Ingest a single image file, determining if tiling is required."""
    doc_stem = image_path.stem
    doc_name = image_path.name
    out_dir = pages_base_dir / doc_stem

    with Image.open(image_path) as im:
        w, h = im.size

    if max(w, h) > 2500:
        overview, tiles = tile_large_image(image_path, out_dir, doc_name, grid_cols=3, grid_rows=2, overlap_pct=10.0)
        return [overview] + tiles
    else:
        out_dir.mkdir(parents=True, exist_ok=True)
        dest_path = out_dir / f"{doc_stem}.png"
        with Image.open(image_path) as im:
            im.save(dest_path, format="PNG")
        im_hash = compute_sha256(dest_path)

        meta = {
            "doc": doc_name,
            "page": 1,
            "kind": "image_single",
            "sha256": im_hash,
            "render_dpi": None,
            "tile": None,
            "has_text_layer": False,
            "image_path": str(dest_path.as_posix()),
            "text_layer_path": None,
            "transcription_path": str((out_dir / f"{doc_stem}.md").as_posix()),
            "needs_vision": True,
        }
        return [meta]


def ingest_tex_file(
    tex_path: Path,
    pages_base_dir: Path,
) -> List[Dict[str, Any]]:
    """Ingests a LaTeX (.tex) source file, resolving inputs and chunking into frames/sections."""
    doc_stem = tex_path.stem
    doc_name = tex_path.name
    out_dir = pages_base_dir / doc_stem
    out_dir.mkdir(parents=True, exist_ok=True)

    base_dir = tex_path.parent

    def resolve_tex(p: Path, visited: Set[str]) -> str:
        real_p = p.resolve()
        if str(real_p) in visited or not real_p.exists():
            return ""
        visited.add(str(real_p))

        content = real_p.read_text(encoding="utf-8", errors="replace")

        def repl_input(match):
            sub_name = match.group(1).strip()
            if not sub_name.endswith(".tex"):
                sub_name += ".tex"
            sub_path = base_dir / sub_name
            return resolve_tex(sub_path, visited)

        content = re.sub(r"\\(?:input|include)\{([^}]+)\}", repl_input, content)
        return content

    full_tex = resolve_tex(tex_path, set())

    # Detect frames
    frame_matches = list(re.finditer(r"\\begin\{frame\}(?:\[.*?\])?(?:\{.*?\})?(.*?)\\end\{frame\}", full_tex, re.DOTALL))
    metas: List[Dict[str, Any]] = []

    if frame_matches:
        for idx, m in enumerate(frame_matches, 1):
            frame_body = m.group(1).strip()
            frame_title_m = re.search(r"\\frametitle\{([^}]+)\}", frame_body)
            frame_title = frame_title_m.group(1) if frame_title_m else f"Frame {idx}"

            txt_filename = f"frame_{idx:03d}.tex"
            txt_filepath = out_dir / txt_filename
            txt_filepath.write_text(frame_body, encoding="utf-8")

            has_tikz = bool(re.search(r"\\begin\{tikzpicture\}|\\includegraphics|\\begin\{axis\}", frame_body))

            metas.append({
                "doc": doc_name,
                "page": f"frame-{idx}",
                "kind": "tex_frame",
                "sha256": compute_sha256(txt_filepath),
                "render_dpi": None,
                "tile": None,
                "has_text_layer": True,
                "image_path": None,
                "text_layer_path": str(txt_filepath.as_posix()),
                "transcription_path": str((out_dir / f"frame_{idx:03d}.md").as_posix()),
                "title": frame_title,
                "has_tikz": has_tikz,
                "content": frame_body,
            })
    else:
        # Fallback to single tex document
        txt_filepath = out_dir / f"{doc_stem}.tex"
        txt_filepath.write_text(full_tex, encoding="utf-8")
        metas.append({
            "doc": doc_name,
            "page": 1,
            "kind": "tex_source",
            "sha256": compute_sha256(txt_filepath),
            "render_dpi": None,
            "tile": None,
            "has_text_layer": True,
            "image_path": None,
            "text_layer_path": str(txt_filepath.as_posix()),
            "transcription_path": str((out_dir / f"{doc_stem}.md").as_posix()),
            "content": full_tex,
        })

    return metas


def partition_vision_batches(
    items: List[Dict[str, Any]],
    batch_size: int = 10,
) -> List[Dict[str, Any]]:
    """Partition manifest items into balanced vision batches (~10 items per batch)."""
    batches = []
    num_batches = math.ceil(len(items) / batch_size) if items else 0

    for b_idx in range(num_batches):
        start_idx = b_idx * batch_size
        end_idx = min(len(items), start_idx + batch_size)
        batch_items = items[start_idx:end_idx]
        batch_id = f"vision_batch_{b_idx + 1:02d}"

        batches.append({
            "batch_id": batch_id,
            "batch_index": b_idx + 1,
            "total_batches": num_batches,
            "item_count": len(batch_items),
            "items": batch_items,
        })

    return batches


def natural_sort_key(s: Union[str, Path]) -> List[Union[int, str]]:
    """Key for natural alphanumeric sorting (e.g. page1, page2, page10, EST3_LEC01)."""
    text = Path(s).as_posix() if isinstance(s, Path) else str(s)
    return [int(c) if c.isdigit() else c.lower() for c in re.split(r"(\d+)", text)]


class ConsolidatedPatchPath(str):
    """String path representing a consolidated patch file, compatible with path and content lookups."""
    def __new__(cls, path: Union[str, Path], content: str = ""):
        path_str = str(Path(path).as_posix())
        obj = super().__new__(cls, path_str)
        obj._content = content
        return obj

    @property
    def content(self) -> str:
        if not self._content:
            try:
                self._content = Path(self).read_text(encoding="utf-8")
            except Exception:
                pass
        return self._content

    def read_text(self, encoding: str = "utf-8") -> str:
        return Path(self).read_text(encoding=encoding)

    def __contains__(self, item: Any) -> bool:
        if super().__contains__(item):
            return True
        return item in self.content


def consolidate_document_patches(work_dir: Union[str, Path]) -> Dict[str, str]:
    """Consolidates visual patches in work/patches/ into unified markdown files per original document.
    
    Groups all page/tile patches belonging to the same document (e.g. solow1956_page001.md,
    solow1956_page002.md) into work/patches/<doc_stem>.md with level 2 headings for each page
    (## Page 1, ## Page 2), maintaining strict sequential and chronological order of pages and images.
    Distinct documents (e.g. EST3_LEC01.pdf vs stats 3 3-10.png) are consolidated into their respective
    separate files (EST3_LEC01.md and stats_3_3-10.md).
    
    Returns:
        Dict mapping clean doc_stem to consolidated patch path (ConsolidatedPatchPath).
    """
    work_dir = Path(work_dir).resolve()
    patches_dir = work_dir / "patches"
    if not patches_dir.exists() or not patches_dir.is_dir():
        return {}

    # 1. Discover known document stems from manifest or pages directory
    known_stems: Dict[str, str] = {}
    manifest_doc_order: List[str] = []

    for manifest_candidate in [work_dir / "pages" / "manifest.json", work_dir / "manifest.json"]:
        if manifest_candidate.is_file():
            try:
                mdata = json.loads(manifest_candidate.read_text(encoding="utf-8"))
                for item in mdata.get("items", []):
                    raw_doc = item.get("doc", "")
                    if raw_doc:
                        stem = Path(raw_doc).stem
                        clean = re.sub(r"\s+", "_", stem)
                        known_stems[stem.lower()] = clean
                        known_stems[clean.lower()] = clean
                        if clean not in manifest_doc_order:
                            manifest_doc_order.append(clean)
            except Exception:
                pass

    pages_dir = work_dir / "pages"
    if pages_dir.is_dir():
        for pdir in pages_dir.iterdir():
            if pdir.is_dir():
                clean = re.sub(r"\s+", "_", pdir.name)
                known_stems[pdir.name.lower()] = clean
                known_stems[clean.lower()] = clean
                if clean not in manifest_doc_order:
                    manifest_doc_order.append(clean)

    # 2. Match patch files
    page_pattern = re.compile(r"^(?P<doc>.+?)[_ -]+(?:page|p|frame|img|image)?[_ -]*(?P<page>\d+)\.md$", re.IGNORECASE)
    tile_pattern = re.compile(r"^(?P<doc>.+?)[_ -]+tile[_ -]*(?P<tile>.+)\.md$", re.IGNORECASE)

    doc_groups: Dict[str, List[Tuple[Any, Path]]] = {}
    unmatched_files: List[Path] = []

    for pfile in sorted(patches_dir.glob("*.md"), key=natural_sort_key):
        if not pfile.is_file():
            continue
        fname = pfile.name
        m_page = page_pattern.match(fname)
        m_tile = tile_pattern.match(fname)

        if m_page:
            raw_doc = m_page.group("doc").strip()
            page_val = int(m_page.group("page"))
            clean_doc = known_stems.get(raw_doc.lower(), re.sub(r"\s+", "_", raw_doc))
            doc_groups.setdefault(clean_doc, []).append((page_val, pfile))
        elif m_tile:
            raw_doc = m_tile.group("doc").strip()
            tile_val = m_tile.group("tile").strip()
            clean_doc = known_stems.get(raw_doc.lower(), re.sub(r"\s+", "_", raw_doc))
            doc_groups.setdefault(clean_doc, []).append((tile_val, pfile))
        else:
            unmatched_files.append(pfile)

    # Handle files that don't follow _page<num>.md (e.g. already named <doc_stem>.md or single-image patches)
    for pfile in unmatched_files:
        stem = pfile.stem
        clean_doc = known_stems.get(stem.lower(), re.sub(r"\s+", "_", stem))
        if clean_doc in doc_groups:
            # Already has decomposed page patches, skip previous consolidated output to avoid recursion
            continue
        # Single document patch without page suffix: treat as page 1
        doc_groups.setdefault(clean_doc, []).append((1, pfile))

    if not doc_groups:
        return {}

    # 3. Determine document ordering (preserving manifest/chronological order)
    ordered_docs: List[str] = []
    for d in manifest_doc_order:
        if d in doc_groups and d not in ordered_docs:
            ordered_docs.append(d)
    for d in sorted(doc_groups.keys(), key=natural_sort_key):
        if d not in ordered_docs:
            ordered_docs.append(d)

    consolidated_results: Dict[str, str] = {}

    # 4. Consolidate each document maintaining strict sequential order of pages and images
    for doc_name in ordered_docs:
        raw_items = doc_groups[doc_name]

        # Strict sequential sorting by page number / tile order / natural sort
        def get_item_order(entry: Tuple[Any, Path]):
            page_val, path = entry
            if isinstance(page_val, int):
                return (0, page_val, natural_sort_key(path))
            m = re.search(r"\d+", str(page_val))
            if m:
                return (0, int(m.group(0)), natural_sort_key(path))
            return (1, 0, natural_sort_key(path))

        sorted_items = sorted(raw_items, key=get_item_order)

        sections: List[str] = []
        for page_val, ppath in sorted_items:
            try:
                body = ppath.read_text(encoding="utf-8").strip()
            except Exception:
                body = ""

            # Strip duplicate leading # Page X or ## Page X headings
            clean_body = re.sub(
                r"^#+\s*(?:Page|Página|Pagina)\s*[\w\.-]+[^\n]*\n*",
                "",
                body,
                flags=re.IGNORECASE,
            ).strip()

            heading = f"## Page {page_val}"

            if clean_body:
                sections.append(f"{heading}\n\n{clean_body}\n")
            else:
                sections.append(f"{heading}\n")

        consolidated_content = "\n".join(sections).strip() + "\n"
        out_file = patches_dir / f"{doc_name}.md"
        out_file.write_text(consolidated_content, encoding="utf-8")

        consolidated_results[doc_name] = ConsolidatedPatchPath(out_file, consolidated_content)

    return consolidated_results


def resolve_document_order(
    input_path: Union[str, Path],
    order_override: Optional[Union[str, Path, List[Union[str, Path]]]] = None,
    work_dir: Optional[Union[str, Path]] = None,
) -> List[Path]:
    """Resolves and validates document order.
    
    Defaults to natural alphanumeric sort. If order_override is provided (as a list,
    or path to work/order.json), validates that it contains exactly the existing
    documents with no missing or extra items. Writes the resolved order to work/order.json.
    """
    input_p = Path(input_path).resolve()
    target_files: List[Path] = []
    if input_p.is_dir():
        for root, _, files in os.walk(input_p):
            for f in files:
                ext = Path(f).suffix.lower()
                if ext in PDF_EXTENSIONS or ext in IMAGE_EXTENSIONS or ext in TEX_EXTENSIONS:
                    target_files.append(Path(root) / f)
    elif input_p.is_file():
        target_files.append(input_p)
    else:
        raise FileNotFoundError(f"Input path does not exist: {input_p}")

    default_ordered = sorted(target_files, key=natural_sort_key)

    # Check if override was provided or if work_dir/order.json exists
    override_list = None
    if order_override is None and work_dir is not None:
        cand_order = Path(work_dir) / "order.json"
        if cand_order.is_file():
            order_override = cand_order

    if order_override is not None:
        if isinstance(order_override, (str, Path)):
            override_path = Path(order_override)
            if override_path.is_file():
                try:
                    raw_data = json.loads(override_path.read_text(encoding="utf-8"))
                    if isinstance(raw_data, list):
                        override_list = raw_data
                    elif isinstance(raw_data, dict):
                        override_list = raw_data.get("order") or raw_data.get("documents") or raw_data.get("items") or []
                    else:
                        override_list = [str(raw_data)]
                except Exception as e:
                    raise ValueError(f"Failed to parse order override JSON file {override_path}: {e}")
            else:
                if "," in str(order_override):
                    override_list = [s.strip() for s in str(order_override).split(",") if s.strip()]
                else:
                    override_list = [str(order_override)]
        elif isinstance(order_override, list):
            override_list = order_override

    if override_list is not None:
        name_map = {f.name: f for f in target_files}
        stem_map = {f.stem: f for f in target_files}
        resolved: List[Path] = []
        seen = set()
        extra = []

        for item in override_list:
            item_str = Path(item).name if isinstance(item, (str, Path)) else str(item)
            match = name_map.get(item_str) or stem_map.get(item_str)
            if not match:
                bname = Path(item_str).name
                match = name_map.get(bname) or stem_map.get(bname)
            if match:
                if match not in seen:
                    resolved.append(match)
                    seen.add(match)
            else:
                extra.append(str(item))

        missing = [f.name for f in target_files if f not in seen]
        if extra or missing:
            raise ValueError(
                f"Document order override validation failed. "
                f"Missing documents: {missing}; Extra documents: {extra}"
            )
        final_order = resolved
    else:
        final_order = default_ordered

    # Write work/order.json if work_dir or candidate path exists
    out_order_path = None
    if work_dir is not None:
        out_order_path = Path(work_dir) / "order.json"
    elif isinstance(order_override, (str, Path)) and Path(order_override).name == "order.json" and Path(order_override).parent.exists():
        out_order_path = Path(order_override)
    else:
        w_cand = Path("work")
        if w_cand.exists() and w_cand.is_dir():
            out_order_path = w_cand / "order.json"

    if out_order_path:
        try:
            out_order_path.parent.mkdir(parents=True, exist_ok=True)
            out_order_path.write_text(
                json.dumps([p.name for p in final_order], indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
        except Exception:
            pass

    return final_order


def partition_handouts(
    handouts: Union[List[Any], int],
    max_agents: int = 6,
    per_agent: int = 6,
) -> List[Dict[str, Any]]:
    """Partitions handouts into balanced consecutive shards for parallel vision patchers.
    
    Rules:
    - If N <= 2 -> 1 agent.
    - If N > 2 -> K = min(max_agents, math.ceil(N / per_agent)).
    - Chunks are consecutive and balanced.
    """
    if isinstance(handouts, int):
        handout_items = [{"handout_id": f"handout_{i+1:03d}"} for i in range(handouts)]
    else:
        handout_items = list(handouts)

    n = len(handout_items)
    if n == 0:
        return []

    if n <= 2:
        k = 1
    else:
        k = min(max_agents, math.ceil(n / per_agent))

    base_size = n // k
    rem = n % k
    shards: List[Dict[str, Any]] = []
    start = 0

    for i in range(k):
        count = base_size + (1 if i < rem else 0)
        end = start + count
        chunk = handout_items[start:end]
        start = end

        handout_ids = []
        docs = []
        for h in chunk:
            if isinstance(h, dict):
                hid = h.get("handout_id", "")
                handout_ids.append(hid)
                for p in h.get("pages", []):
                    d = p.get("doc")
                    if d and d not in docs:
                        docs.append(d)
            else:
                handout_ids.append(str(h))

        shards.append({
            "shard_id": i + 1,
            "handout_ids": handout_ids,
            "docs": docs,
        })

    return shards


def create_handouts(
    work_dir: Union[str, Path],
    manifest: Union[Dict[str, Any], str, Path],
    dpi: int = 150,
) -> Dict[str, Any]:
    """Generates 2x2 and 1x2 handouts for pages requiring visual interpretation.
    
    - Filters manifest items with needs_vision == True.
    - For kind == 'beamer_text': groups 4 consecutive pages within same doc, 2x2 layout.
    - For kind == 'ink_pdf' or image: groups 2 consecutive pages, 1x2 layout.
    - Renders with PyMuPDF (fitz) and scales with PIL preserving aspect ratio so long side <= HANDOUT_MAX_SIDE.
    - Draws indelible banner on each quadrant: '[DOC: {doc} | PAGE: {n}]'.
    - Saves work/handouts/handout_{idx:03d}.png and work/handouts/handout_{idx:03d}_text.md.
    - Writes work/handouts/handouts_manifest.json.
    """
    work_p = Path(work_dir).resolve()
    handouts_dir = work_p / "handouts"
    handouts_dir.mkdir(parents=True, exist_ok=True)

    if isinstance(manifest, (str, Path)):
        manifest_data = json.loads(Path(manifest).read_text(encoding="utf-8"))
    else:
        manifest_data = manifest

    items = manifest_data.get("items", [])
    source_path_val = manifest_data.get("source_path", "")

    # Filter items with needs_vision == True or image sources
    vision_items = [
        it for it in items
        if it.get("needs_vision") is True or str(it.get("kind", "")).startswith("image")
    ]

    if not vision_items:
        empty_manifest = {
            "total_handouts": 0,
            "agents_recommended": 1,
            "handouts": [],
            "shards": [],
        }
        (handouts_dir / "handouts_manifest.json").write_text(
            json.dumps(empty_manifest, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        return empty_manifest

    # Group by document preserving original document order in manifest
    doc_groups: Dict[str, List[Dict[str, Any]]] = {}
    for it in vision_items:
        doc_name = it.get("doc", "")
        doc_groups.setdefault(doc_name, []).append(it)

    # Sort pages within each document
    def _extract_page_int(it):
        p = it.get("page", 0)
        if isinstance(p, int):
            return p
        m = re.search(r"\d+", str(p))
        return int(m.group(0)) if m else 0

    for doc_name in doc_groups:
        doc_groups[doc_name].sort(key=_extract_page_int)

    handouts_list: List[Dict[str, Any]] = []
    handout_idx = 1

    for doc_name, doc_items in doc_groups.items():
        first_kind = doc_items[0].get("kind", "")
        if first_kind == "beamer_text":
            chunk_size = 4
            layout = "2x2"
            max_side = HANDOUT_MAX_SIDE_2X2
        else:
            chunk_size = 2
            layout = "1x2"
            max_side = HANDOUT_MAX_SIDE_1X2

        for i in range(0, len(doc_items), chunk_size):
            chunk = doc_items[i : i + chunk_size]
            quadrant_images: List[Image.Image] = []
            quadrant_texts: List[str] = []

            for p_item in chunk:
                p_doc = p_item.get("doc", "")
                p_num = _extract_page_int(p_item)
                
                # Retrieve or render page image and PyMuPDF text
                page_img = None
                page_txt = ""

                # 1. Search candidate PDF
                cand_pdf = None
                for candidate in [
                    Path(p_item.get("pdf_path", "")),
                    Path(source_path_val) / p_doc if source_path_val else None,
                    Path(source_path_val) if source_path_val and Path(source_path_val).is_file() and Path(source_path_val).name == p_doc else None,
                    work_p / p_doc,
                    work_p.parent / p_doc,
                    work_p / "pages" / Path(p_doc).stem / p_doc,
                    Path(p_doc),
                ]:
                    if candidate and candidate.is_file() and candidate.suffix.lower() == ".pdf":
                        cand_pdf = candidate
                        break

                if cand_pdf is None or not cand_pdf.is_file():
                    for root_dir in [work_p, work_p.parent, Path(source_path_val).parent if source_path_val else None, Path(".")]:
                        if root_dir and Path(root_dir).is_dir():
                            found = list(Path(root_dir).rglob(p_doc))
                            if found:
                                cand_pdf = found[0]
                                break

                if cand_pdf and cand_pdf.is_file():
                    try:
                        fdoc = fitz.open(cand_pdf)
                        fpage = fdoc[p_num - 1] if 0 <= p_num - 1 < len(fdoc) else fdoc[0]
                        zoom = dpi / 72.0
                        pix = fpage.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
                        page_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        page_txt = clean_beamer_text(fpage)
                        fdoc.close()
                    except Exception:
                        pass

                if page_img is None:
                    # 2. Try pre-rendered image_path
                    img_cand = p_item.get("image_path")
                    if img_cand and Path(img_cand).is_file():
                        try:
                            page_img = Image.open(img_cand).convert("RGB")
                        except Exception:
                            pass

                if page_img is None:
                    # 3. Fallback placeholder
                    page_img = Image.new("RGB", (800, 600), (245, 245, 245))

                # Check text layer path if text is empty
                txt_cand = p_item.get("text_layer_path")
                if not page_txt and txt_cand and Path(txt_cand).is_file():
                    try:
                        page_txt = Path(txt_cand).read_text(encoding="utf-8")
                    except Exception:
                        pass

                # Draw indelible banner on each quadrant: [DOC: {doc} | PAGE: {n}]
                qw, qh = page_img.size
                banner_h = max(32, int(qh * 0.05))
                draw = ImageDraw.Draw(page_img)
                draw.rectangle([(0, 0), (qw, banner_h)], fill=(20, 24, 36))
                banner_text = f"[DOC: {p_doc} | PAGE: {p_num}]"
                try:
                    font = ImageFont.load_default(size=max(14, int(banner_h * 0.55)))
                except TypeError:
                    font = ImageFont.load_default()
                draw.text((12, max(2, (banner_h - 18) // 2)), banner_text, fill=(255, 255, 255), font=font)

                quadrant_images.append(page_img)
                quadrant_texts.append(page_txt)

            # Compose Grid
            if layout == "2x2":
                w_max = max(im.width for im in quadrant_images)
                h_max = max(im.height for im in quadrant_images)
                grid_w = 2 * w_max
                grid_h = 2 * h_max
                grid_img = Image.new("RGB", (grid_w, grid_h), (255, 255, 255))
                coords = [(0, 0), (w_max, 0), (0, h_max), (w_max, h_max)]
                for q_i, q_im in enumerate(quadrant_images):
                    grid_img.paste(q_im, coords[q_i])

                if max(grid_w, grid_h) > max_side:
                    scale = float(max_side) / float(max(grid_w, grid_h))
                    new_w = int(round(grid_w * scale))
                    new_h = int(round(grid_h * scale))
                    grid_img = grid_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            else:  # 1x2
                first_im = quadrant_images[0]
                is_landscape = first_im.width > first_im.height
                if is_landscape:
                    # Apilado vertical (1 col, 2 rows)
                    w_max = max(im.width for im in quadrant_images)
                    h_max = max(im.height for im in quadrant_images)
                    grid_w = w_max
                    grid_h = len(quadrant_images) * h_max
                    grid_img = Image.new("RGB", (grid_w, grid_h), (255, 255, 255))
                    for q_i, q_im in enumerate(quadrant_images):
                        grid_img.paste(q_im, (0, q_i * h_max))
                else:
                    # Lado a lado horizontal (2 cols, 1 row)
                    w_max = max(im.width for im in quadrant_images)
                    h_max = max(im.height for im in quadrant_images)
                    grid_w = len(quadrant_images) * w_max
                    grid_h = h_max
                    grid_img = Image.new("RGB", (grid_w, grid_h), (255, 255, 255))
                    for q_i, q_im in enumerate(quadrant_images):
                        grid_img.paste(q_im, (q_i * w_max, 0))

                if max(grid_img.width, grid_img.height) > max_side:
                    scale = float(max_side) / float(max(grid_img.width, grid_img.height))
                    new_w = int(round(grid_img.width * scale))
                    new_h = int(round(grid_h * scale))
                    grid_img = grid_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

            handout_id = f"handout_{handout_idx:03d}"
            handout_png_path = handouts_dir / f"{handout_id}.png"
            grid_img.save(handout_png_path, format="PNG")

            # Build text support markdown
            text_sections = [
                f"# Text Support for {handout_id}",
                f"Layout: `{layout}` | Document: `{doc_name}`\n",
            ]
            for p_item, q_txt in zip(chunk, quadrant_texts):
                p_d = p_item.get("doc", "")
                p_n = _extract_page_int(p_item)
                clean_t = q_txt.strip() if q_txt.strip() else "(No PyMuPDF text layer detected)"
                text_sections.append(f"## [DOC: {p_d} | PAGE: {p_n}]\n\n{clean_t}\n")

            handout_txt_path = handouts_dir / f"{handout_id}_text.md"
            handout_txt_path.write_text("\n".join(text_sections), encoding="utf-8")

            handout_entry = {
                "handout_id": handout_id,
                "layout": layout,
                "image_path": str(handout_png_path.as_posix()),
                "text_support_path": str(handout_txt_path.as_posix()),
                "pages": [{"doc": it["doc"], "page": _extract_page_int(it)} for it in chunk],
            }
            handouts_list.append(handout_entry)
            handout_idx += 1

    shards = partition_handouts(handouts_list)
    handouts_manifest_res = {
        "total_handouts": len(handouts_list),
        "agents_recommended": len(shards),
        "handouts": handouts_list,
        "shards": shards,
    }
    (handouts_dir / "handouts_manifest.json").write_text(
        json.dumps(handouts_manifest_res, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    return handouts_manifest_res


def stitch_patches_to_corpus(
    work_dir: Union[str, Path],
    partial: bool = False,
) -> Dict[str, Any]:
    """Stitches vision patches into corpus.md, rebuilding from corpus_raw.md.
    
    - Reads patches from work/handout_patches/patch_handout_*.md.
    - Parses headers '## <<DOC: {doc} | PAGE: {n}>>'.
    - Validates against expected in handouts_manifest.json. If partial=False and missing, raises error.
    - If work/corpus_raw.md does not exist, copies work/corpus.md to work/corpus_raw.md.
    - Reconstructs work/corpus.md replacing PyMuPDF blocks with patch content.
    - Writes consolidated patches per document in work/patches/{doc_stem}.md for compatibility.
    """
    work_p = Path(work_dir).resolve()
    handout_patches_dir = work_p / "handout_patches"
    handouts_manifest_path = work_p / "handouts" / "handouts_manifest.json"
    corpus_file = work_p / "corpus.md"
    corpus_raw_file = work_p / "corpus_raw.md"
    patches_dir = work_p / "patches"
    patches_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load expected pages from handouts_manifest.json
    handouts = []
    if handouts_manifest_path.is_file():
        hdata = json.loads(handouts_manifest_path.read_text(encoding="utf-8"))
        handouts = hdata.get("handouts", [])

    handout_pages_map: Dict[str, List[Tuple[str, int]]] = {}
    for h in handouts:
        hid = h["handout_id"]
        plist = [(p["doc"], int(p["page"])) for p in h.get("pages", [])]
        handout_pages_map[hid] = plist

    # 2. Parse patch files
    header_pattern = re.compile(
        r"^##\s*<<\s*DOC:\s*(?P<doc>[^|>]+?)\s*\|\s*PAGE:\s*(?P<page>\d+)[^>]*>>[ \t]*\n?",
        re.MULTILINE,
    )

    parsed_patches: Dict[Tuple[str, int], str] = {}
    present_handouts: Set[str] = set()

    if handout_patches_dir.is_dir():
        for pfile in sorted(handout_patches_dir.glob("patch_handout_*.md"), key=natural_sort_key):
            if not pfile.is_file():
                continue
            hid = pfile.stem.replace("patch_", "")
            present_handouts.add(hid)
            content = pfile.read_text(encoding="utf-8")
            matches = list(header_pattern.finditer(content))
            for i, match in enumerate(matches):
                doc_name = match.group("doc").strip()
                page_num = int(match.group("page"))
                start_body = match.end()
                end_body = matches[i + 1].start() if i + 1 < len(matches) else len(content)
                body = content[start_body:end_body].strip()
                parsed_patches[(doc_name, page_num)] = body

    # 3. Validation
    if not partial:
        missing_handouts = []
        missing_pages = []
        for hid, expected_list in handout_pages_map.items():
            if hid not in present_handouts:
                missing_handouts.append(hid)
                missing_pages.extend(expected_list)
            else:
                for (d, p) in expected_list:
                    if (d, p) not in parsed_patches or not parsed_patches[(d, p)]:
                        missing_handouts.append(hid)
                        missing_pages.append((d, p))
        if missing_handouts:
            raise ValueError(
                f"Missing required handout patches (partial=False). "
                f"Missing handouts: {sorted(set(missing_handouts))}; Missing pages: {missing_pages}"
            )
    else:
        # Partial validation: for present handouts, verify their pages are present
        for hid in present_handouts:
            if hid in handout_pages_map:
                for (d, p) in handout_pages_map[hid]:
                    if (d, p) not in parsed_patches:
                        raise ValueError(f"Incomplete patch for {hid}: missing page {p} of {d}")

    # 4. Backup corpus.md to corpus_raw.md
    if not corpus_raw_file.is_file():
        if corpus_file.is_file():
            corpus_raw_file.write_text(corpus_file.read_text(encoding="utf-8"), encoding="utf-8")
        else:
            raise FileNotFoundError(f"Neither corpus_raw.md nor corpus.md exists in {work_p}")

    corpus_raw_text = corpus_raw_file.read_text(encoding="utf-8")

    # 5. Reconstruct corpus.md
    page_block_pattern = re.compile(
        r"(^##\s*<<\s*DOC:\s*(?P<doc>[^|>]+?)\s*\|\s*PAGE:\s*(?P<page>\d+)(?P<extra>[^>]*)>>[ \t]*\n?)",
        re.MULTILINE,
    )
    matches = list(page_block_pattern.finditer(corpus_raw_text))
    reconstructed_parts = []
    last_idx = 0

    if not matches:
        reconstructed_parts.append(corpus_raw_text)
    else:
        for i, match in enumerate(matches):
            reconstructed_parts.append(corpus_raw_text[last_idx : match.start()])
            doc_name = match.group("doc").strip()
            page_num = int(match.group("page"))

            next_start = matches[i + 1].start() if i + 1 < len(matches) else len(corpus_raw_text)

            patch_key = (doc_name, page_num)
            if patch_key not in parsed_patches:
                for (p_doc, p_n), p_content in parsed_patches.items():
                    if (p_doc == doc_name or Path(p_doc).name == Path(doc_name).name or Path(p_doc).stem == Path(doc_name).stem) and p_n == page_num:
                        patch_key = (p_doc, p_n)
                        break

            if patch_key in parsed_patches:
                patch_content = parsed_patches[patch_key]
                reconstructed_parts.append(
                    f"## <<DOC: {doc_name} | PAGE: {page_num} | PATCHED: YES>>\n\n{patch_content}\n\n"
                )
            else:
                reconstructed_parts.append(corpus_raw_text[match.start() : next_start])

            last_idx = next_start

    corpus_file.write_text("".join(reconstructed_parts), encoding="utf-8")

    # 6. Write consolidated patches per document in work/patches/{doc_stem}.md for compatibility
    docs_in_patches: Set[str] = {d for (d, _) in parsed_patches.keys()}
    for doc in docs_in_patches:
        doc_stem = Path(doc).stem
        clean_stem = re.sub(r"\s+", "_", doc_stem)
        doc_pages = [(p, txt) for (d, p), txt in parsed_patches.items() if d == doc or Path(d).stem == doc_stem]
        doc_pages.sort(key=lambda x: x[0])
        
        doc_sections = []
        for p, txt in doc_pages:
            clean_t = re.sub(r"^#+\s*(?:Page|Página|Pagina)\s*[\w\.-]+[^\n]*\n*", "", txt, flags=re.IGNORECASE).strip()
            doc_sections.append(f"## Page {p}\n\n{clean_t}\n")
        
        out_patch_file = patches_dir / f"{clean_stem}.md"
        out_patch_file.write_text("\n".join(doc_sections).strip() + "\n", encoding="utf-8")

    return {
        "stitched_pages": len(parsed_patches),
        "corpus_path": str(corpus_file.as_posix()),
        "patches_count": len(present_handouts),
    }


def generate_section_slices(
    work_dir: Union[str, Path],
    max_sections: int = 4,
) -> Dict[str, Any]:
    """Generates balanced section slices (M <= 4) for sectional CTA analysis.
    
    - Orders documents according to resolve_document_order.
    - If a document dominates (> 40% of total tokens and > 20 pages), splits it into consecutive blocks at handout boundaries.
    - Groups consecutive units into M <= 4 balanced sections.
    - Generates work/sections/section_{idx:02d}.md and work/sections/sections_manifest.json.
    """
    work_p = Path(work_dir).resolve()
    sections_dir = work_p / "sections"
    sections_dir.mkdir(parents=True, exist_ok=True)

    # 1. Determine document order
    order_file = work_p / "order.json"
    manifest_file = work_p / "pages" / "manifest.json"
    if not manifest_file.exists():
        manifest_file = work_p / "manifest.json"

    if order_file.is_file():
        doc_order = json.loads(order_file.read_text(encoding="utf-8"))
    elif manifest_file.is_file():
        mdata = json.loads(manifest_file.read_text(encoding="utf-8"))
        seen = []
        for it in mdata.get("items", []):
            d = it.get("doc")
            if d and d not in seen:
                seen.append(d)
        doc_order = seen
    else:
        doc_order = []

    # 2. Collect token and page stats per document
    density_file = work_p / "density.json"
    doc_tokens: Dict[str, int] = {}
    doc_pages_map: Dict[str, List[int]] = {}

    if density_file.is_file():
        ddata = json.loads(density_file.read_text(encoding="utf-8"))
        for entry in ddata:
            d = entry.get("doc", "")
            p = entry.get("page", 1)
            p_int = int(re.search(r"\d+", str(p)).group(0)) if re.search(r"\d+", str(p)) else 1
            chars = entry.get("chars", 0)
            nv = entry.get("needs_vision", False)
            toks = math.ceil(chars / 3.2) + (1500 if nv else 0)
            doc_tokens[d] = doc_tokens.get(d, 0) + toks
            doc_pages_map.setdefault(d, []).append(p_int)

    total_tokens = sum(doc_tokens.values())
    if total_tokens <= 0:
        total_tokens = 1

    # 3. Read handouts
    handouts_file = work_p / "handouts" / "handouts_manifest.json"
    all_handouts = []
    if handouts_file.is_file():
        all_handouts = json.loads(handouts_file.read_text(encoding="utf-8")).get("handouts", [])

    # 4. Create atomic units (splitting dominant documents at handout boundaries)
    atomic_units = []

    for doc in doc_order:
        tokens = doc_tokens.get(doc, 0)
        pages_list = sorted(doc_pages_map.get(doc, [1]))
        pages_count = len(pages_list)
        is_dominant = (tokens > 0.40 * total_tokens) and (pages_count > 20)

        # Handouts for this doc
        doc_handouts = [
            h for h in all_handouts
            if any(p.get("doc") == doc or Path(p.get("doc", "")).name == Path(doc).name for p in h.get("pages", []))
        ]

        if not is_dominant:
            atomic_units.append({
                "doc": doc,
                "page_start": pages_list[0] if pages_list else 1,
                "page_end": pages_list[-1] if pages_list else 1,
                "tokens": tokens,
                "handouts": [h["handout_id"] for h in doc_handouts],
            })
        else:
            # Dominant document! Split into consecutive blocks at handout boundaries
            other_docs_count = len(doc_order) - 1
            max_chunks = max(2, min(max_sections, max_sections - other_docs_count))

            if len(doc_handouts) >= 2:
                h_k = min(max_chunks, len(doc_handouts))
                base_h = len(doc_handouts) // h_k
                rem_h = len(doc_handouts) % h_k
                start_h = 0
                for c_idx in range(h_k):
                    count_h = base_h + (1 if c_idx < rem_h else 0)
                    end_h = start_h + count_h
                    chunk_handouts = doc_handouts[start_h:end_h]
                    start_h = end_h

                    chunk_p_start = chunk_handouts[0]["pages"][0]["page"]
                    chunk_p_end = chunk_handouts[-1]["pages"][-1]["page"]

                    if c_idx == 0 and pages_list:
                        chunk_p_start = min(chunk_p_start, pages_list[0])
                    if c_idx == h_k - 1 and pages_list:
                        chunk_p_end = max(chunk_p_end, pages_list[-1])

                    chunk_toks = int(tokens * (count_h / len(doc_handouts)))
                    atomic_units.append({
                        "doc": doc,
                        "page_start": chunk_p_start,
                        "page_end": chunk_p_end,
                        "tokens": chunk_toks,
                        "handouts": [h["handout_id"] for h in chunk_handouts],
                    })
            else:
                h_k = max_chunks
                p_per_chunk = math.ceil(pages_count / h_k)
                for c_idx in range(h_k):
                    p_s_idx = c_idx * p_per_chunk
                    p_e_idx = min(pages_count - 1, (c_idx + 1) * p_per_chunk - 1)
                    if p_s_idx >= pages_count:
                        break
                    atomic_units.append({
                        "doc": doc,
                        "page_start": pages_list[p_s_idx],
                        "page_end": pages_list[p_e_idx],
                        "tokens": int(tokens / h_k),
                        "handouts": [h["handout_id"] for h in doc_handouts],
                    })

    if not atomic_units:
        return {"total_sections": 0, "sections": []}

    if len(atomic_units) <= max_sections:
        section_groups = [[u] for u in atomic_units]
    else:
        m = max_sections
        n = len(atomic_units)
        base_u = n // m
        rem_u = n % m
        section_groups = []
        u_start = 0
        for i in range(m):
            cnt = base_u + (1 if i < rem_u else 0)
            section_groups.append(atomic_units[u_start : u_start + cnt])
            u_start += cnt

    corpus_text = ""
    for candidate_corpus in [work_p / "corpus.md", work_p / "corpus_raw.md"]:
        if candidate_corpus.is_file():
            corpus_text = candidate_corpus.read_text(encoding="utf-8")
            break

    page_block_pattern = re.compile(
        r"(^##\s*<<\s*DOC:\s*(?P<doc>[^|>]+?)\s*\|\s*PAGE:\s*(?P<page>\d+)[^>]*>>[ \t]*\n?)",
        re.MULTILINE,
    )
    corpus_blocks = {}
    c_matches = list(page_block_pattern.finditer(corpus_text))
    for i, cm in enumerate(c_matches):
        c_doc = cm.group("doc").strip()
        c_page = int(cm.group("page"))
        c_end = c_matches[i + 1].start() if i + 1 < len(c_matches) else len(corpus_text)
        corpus_blocks[(c_doc, c_page)] = corpus_text[cm.start() : c_end]

    sections_res_list = []
    for s_idx, group in enumerate(section_groups, 1):
        s_id = f"section_{s_idx:02d}"
        s_docs = []
        s_page_ranges = {}
        s_handouts = []
        s_tokens = 0

        for u in group:
            d = u["doc"]
            if d not in s_docs:
                s_docs.append(d)
            s_page_ranges[d] = [u["page_start"], u["page_end"]]
            for hid in u["handouts"]:
                if hid not in s_handouts:
                    s_handouts.append(hid)
            s_tokens += u["tokens"]

        is_ready = True
        for hid in s_handouts:
            p_file = work_p / "handout_patches" / f"patch_{hid}.md"
            if not p_file.is_file() or p_file.stat().st_size == 0:
                is_ready = False
                break

        extracted_sections = []
        for (c_d, c_p), block in corpus_blocks.items():
            matching_doc = None
            for d in s_docs:
                if c_d == d or Path(c_d).name == Path(d).name or Path(c_d).stem == Path(d).stem:
                    matching_doc = d
                    break
            if matching_doc:
                prange = s_page_ranges.get(matching_doc, [1, 999999])
                if prange[0] <= c_p <= prange[1]:
                    extracted_sections.append(block)

        sec_file = sections_dir / f"{s_id}.md"
        range_str = ", ".join(f"{d} (pages {r[0]}-{r[1]})" for d, r in s_page_ranges.items())
        header = (
            f"# Section {s_idx:02d}\n"
            f"Section Index: {s_idx}\n"
            f"Documents: {', '.join(s_docs)}\n"
            f"Page Ranges: {range_str}\n\n"
        )
        sec_file.write_text(header + "".join(extracted_sections), encoding="utf-8")

        sections_res_list.append({
            "section_id": s_id,
            "section_index": s_idx,
            "docs": s_docs,
            "page_ranges": s_page_ranges,
            "requires_handouts": s_handouts,
            "ready": is_ready,
            "dispatched": False,
            "file_path": str(sec_file.as_posix()),
            "estimated_tokens": s_tokens,
        })

    sections_manifest_data = {
        "total_sections": len(sections_res_list),
        "sections": sections_res_list,
    }
    (sections_dir / "sections_manifest.json").write_text(
        json.dumps(sections_manifest_data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return sections_manifest_data


def normalize_cta_mode(mode_raw: Optional[str]) -> str:
    """Normalizes CTA mode string to 'direct' or 'mapreduce'."""
    if not mode_raw:
        return "direct"
    s = str(mode_raw).strip().lower()
    if s in ("direct", "single", "direct_cta", "direct-cta"):
        return "direct"
    if s in ("mapreduce", "map_reduce", "map-reduce", "multiple", "multi", "sectional", "multiple_cta", "multiple-cta"):
        return "mapreduce"
    return "direct"


def choose_cta_mode(
    budget: Union[Dict[str, Any], str, Path],
    work_dir: Optional[Union[str, Path]] = None,
    cta_mode: str = "auto",
    granularity: str = "standard",
) -> str:
    """Records user-specified or explicit CTA mode ('direct' or 'mapreduce').
    
    The CTA mode is an explicit directive specified by the user ('direct' vs 'mapreduce' / 'multiple').
    It is completely orthogonal to vision preprocessing: whether direct or mapreduce,
    any pages requiring visual interpretation are transcribed via vision subagents before CTA synthesis.
    """
    if isinstance(budget, (str, Path)):
        bpath = Path(budget)
        bdata = json.loads(bpath.read_text(encoding="utf-8"))
    else:
        bdata = budget
        bpath = Path(work_dir) / "budget.json" if work_dir else None

    total_h = bdata.get("total_handouts", 0)
    clean_mode = str(cta_mode or "auto").strip().lower()

    if clean_mode in ("direct", "single", "direct_cta", "direct-cta"):
        mode = "direct"
        source = "user_explicit"
    elif clean_mode in ("mapreduce", "map_reduce", "map-reduce", "multiple", "multi", "sectional", "multiple_cta", "multiple-cta"):
        mode = "mapreduce"
        source = "user_explicit"
    else:
        # Fallback if 'auto' or unspecified: default based on corpus volume
        total_items = bdata.get("total_items", 0)
        total_tokens = bdata.get("total_estimated_tokens", 0)
        total_files = bdata.get("total_source_files", 1)
        if total_items > 30 or total_tokens > 40000 or total_files >= 4:
            mode = "mapreduce"
        else:
            mode = "direct"
        source = "heuristic"

    bdata["cta_mode"] = mode
    bdata["cta_mode_source"] = source
    bdata["granularity"] = granularity

    if bpath and bpath.is_file():
        try:
            bpath.write_text(json.dumps(bdata, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass
    elif work_dir:
        cand_b = Path(work_dir) / "budget.json"
        if cand_b.is_file():
            try:
                disk_data = json.loads(cand_b.read_text(encoding="utf-8"))
                disk_data["cta_mode"] = mode
                disk_data["cta_mode_source"] = source
                disk_data["granularity"] = granularity
                disk_data["total_handouts"] = total_h
                cand_b.write_text(json.dumps(disk_data, indent=2, ensure_ascii=False), encoding="utf-8")
            except Exception:
                pass

    return mode


def prepare_corpus(
    input_path: Union[str, Path],
    output_dir: Union[str, Path],
    vision: str = "auto",
    legacy_transcribe: bool = False,
    order_override: Optional[Union[str, Path, List[Union[str, Path]]]] = None,
    cta_mode: str = "auto",
    granularity: str = "standard",
) -> Dict[str, Any]:
    """Single-pass ingestion & pre-processing engine.
    
    Extracts text, scores page density, selectively renders images, and generates:
    - work/corpus.md (assembled text layer)
    - work/density.json (page-by-page density & needs_vision report)
    - work/budget.json (token budgeting & recommended agent dispatch)
    - work/vision_pages.json (list of image paths requiring visual interpretation)
    - work/pages/manifest.json (standard manifest)
    """
    input_path = Path(input_path).resolve()
    work_dir = Path(output_dir).resolve()
    pages_dir = work_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)

    manifest_file = pages_dir / "manifest.json"
    corpus_file = work_dir / "corpus.md"
    density_file = work_dir / "density.json"
    budget_file = work_dir / "budget.json"
    vision_pages_file = work_dir / "vision_pages.json"

    # 1. Discover and order target files
    target_files = resolve_document_order(input_path, order_override=order_override, work_dir=work_dir)

    all_manifest_items: List[Dict[str, Any]] = []
    density_profiles: List[Dict[str, Any]] = []
    corpus_sections: List[str] = [f"# Course Ingestion Corpus\nSource: `{input_path.as_posix()}`\n\n"]
    vision_pages_list: List[Dict[str, Any]] = []

    total_tokens_est = 0

    for fpath in target_files:
        ext = fpath.suffix.lower()
        doc_stem = fpath.stem
        doc_name = fpath.name
        out_doc_dir = pages_dir / doc_stem
        out_doc_dir.mkdir(parents=True, exist_ok=True)

        if ext in PDF_EXTENSIONS:
            doc = fitz.open(fpath)
            total_pages = len(doc)

            for p_idx in range(total_pages):
                page_num = p_idx + 1
                page = doc[p_idx]
                density_info = analyze_page_density(page, page_num, doc_name)

                # Determine if image should be rendered
                if vision == "all":
                    render_img = True
                elif vision == "none":
                    render_img = False
                else:  # auto
                    render_img = density_info["needs_vision"]

                img_path_str = None
                img_hash = None
                target_dpi = 150 if density_info["is_ink"] else 130

                if render_img:
                    zoom = target_dpi / 72.0
                    matrix = fitz.Matrix(zoom, zoom)
                    pix = page.get_pixmap(matrix=matrix)
                    img_filename = f"page_{page_num:03d}.png"
                    img_filepath = out_doc_dir / img_filename
                    pix.save(str(img_filepath))
                    img_path_str = str(img_filepath.as_posix())
                    img_hash = compute_sha256(img_filepath)

                    vision_pages_list.append({
                        "doc": doc_name,
                        "page": page_num,
                        "image_path": img_path_str,
                        "reasons": density_info["reasons"],
                    })

                # Save text layer
                clean_text = density_info["extracted_text"]
                txt_filename = f"page_{page_num:03d}_text.txt"
                txt_filepath = out_doc_dir / txt_filename
                txt_filepath.write_text(clean_text, encoding="utf-8")

                kind = "ink_pdf" if density_info["is_ink"] else "beamer_text"
                item_meta = {
                    "doc": doc_name,
                    "page": page_num,
                    "kind": kind,
                    "sha256": img_hash or compute_sha256(txt_filepath),
                    "render_dpi": target_dpi if render_img else None,
                    "tile": None,
                    "has_text_layer": density_info["chars"] > 10,
                    "image_path": img_path_str,
                    "text_layer_path": str(txt_filepath.as_posix()),
                    "transcription_path": str((out_doc_dir / f"page_{page_num:03d}.md").as_posix()),
                    "needs_vision": density_info["needs_vision"],
                }
                all_manifest_items.append(item_meta)

                # Density profile
                density_profiles.append({
                    "doc": doc_name,
                    "page": page_num,
                    "chars": density_info["chars"],
                    "images": density_info["n_images"],
                    "drawings": density_info["n_drawings"],
                    "needs_vision": density_info["needs_vision"],
                    "reasons": density_info["reasons"],
                    "rendered_image": img_path_str,
                })

                # Append to corpus.md
                vision_flag = "YES" if render_img else "NO"
                corpus_sections.append(
                    f"--- \n"
                    f"## <<DOC: {doc_name} | PAGE: {page_num} | NEEDS_VISION: {vision_flag}>>\n\n"
                    f"{clean_text}\n\n"
                )

                # Estimate tokens
                text_toks = math.ceil(density_info["chars"] / 3.2)
                img_toks = 1500 if render_img else 0
                total_tokens_est += text_toks + img_toks

            doc.close()

        elif ext in TEX_EXTENSIONS:
            tex_items = ingest_tex_file(fpath, pages_dir)
            for item in tex_items:
                all_manifest_items.append(item)
                content = item.get("content", "")
                p_label = item.get("page", 1)
                corpus_sections.append(
                    f"--- \n"
                    f"## <<DOC: {doc_name} | PAGE: {p_label} | TYPE: LATEX_TEX>>\n\n"
                    f"```latex\n{content}\n```\n\n"
                )
                total_tokens_est += math.ceil(len(content) / 3.2)

        elif ext in IMAGE_EXTENSIONS:
            img_items = process_image_file(fpath, pages_dir)
            for item in img_items:
                all_manifest_items.append(item)
                img_p = item.get("image_path")
                vision_pages_list.append({
                    "doc": doc_name,
                    "page": item.get("page", 1),
                    "image_path": img_p,
                    "reasons": ["image_source"],
                })
                corpus_sections.append(
                    f"--- \n"
                    f"## <<DOC: {doc_name} | PAGE: {item.get('page')} | TYPE: IMAGE>>\n"
                    f"Image file: `{img_p}`\n\n"
                )
                total_tokens_est += 1500

    # Write files
    corpus_file.write_text("".join(corpus_sections), encoding="utf-8")
    corpus_raw_file = work_dir / "corpus_raw.md"
    if not corpus_raw_file.is_file():
        corpus_raw_file.write_text("".join(corpus_sections), encoding="utf-8")
    density_file.write_text(json.dumps(density_profiles, indent=2, ensure_ascii=False), encoding="utf-8")
    vision_pages_file.write_text(json.dumps(vision_pages_list, indent=2, ensure_ascii=False), encoding="utf-8")

    needs_vision_count = len(vision_pages_list)

    # Generate standard manifest
    by_kind = {}
    for it in all_manifest_items:
        k = it.get("kind", "other")
        by_kind[k] = by_kind.get(k, 0) + 1

    manifest_data = {
        "manifest_version": "3.0",
        "source_path": str(input_path.as_posix()),
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_items": len(all_manifest_items),
        "by_kind": by_kind,
        "items": all_manifest_items,
    }
    manifest_file.write_text(json.dumps(manifest_data, indent=2, ensure_ascii=False), encoding="utf-8")

    # Generate handouts (Component 1)
    handouts_res = create_handouts(work_dir, manifest_data)
    total_handouts = handouts_res.get("total_handouts", 0)

    if total_handouts > 0:
        strategy = "handouts_vision"
        rec_agents = handouts_res.get("agents_recommended", 1)
        rec_msg = (
            f"{needs_vision_count} páginas con contenido visual ({total_handouts} handouts). "
            f"Despachar {rec_agents} subagente(s) de visión en paralelo y coser parches (stitch) obligatoriamente antes de CTA."
        )
    elif needs_vision_count > 0:
        strategy = "pages_vision"
        rec_msg = f"{needs_vision_count} páginas requieren visión. Despachar visión antes de proceder al análisis de CTA."
    else:
        strategy = "none"
        rec_msg = "Sin contenido visual que requiera visión."

    budget_data = {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "total_source_files": len(target_files),
        "total_items": len(all_manifest_items),
        "total_estimated_tokens": total_tokens_est,
        "pages_requiring_vision": needs_vision_count,
        "total_handouts": total_handouts,
        "vision_strategy": strategy,
        "recommendation": rec_msg,
    }

    # Choose and record cta_mode in budget
    selected_cta_mode = choose_cta_mode(
        budget_data,
        work_dir=work_dir,
        cta_mode=cta_mode,
        granularity=granularity,
    )
    budget_data["cta_mode"] = selected_cta_mode
    budget_data["granularity"] = granularity
    budget_file.write_text(json.dumps(budget_data, indent=2, ensure_ascii=False), encoding="utf-8")

    # Generate section slices (Component 1)
    sections_res = generate_section_slices(work_dir)

    if legacy_transcribe:
        batches = partition_vision_batches(all_manifest_items, batch_size=10)
        (work_dir / "vision_batches.json").write_text(json.dumps(batches, indent=2, ensure_ascii=False), encoding="utf-8")

    patches_dir = work_dir / "patches"
    consolidated_patches = {}
    if patches_dir.exists() and patches_dir.is_dir():
        consolidated_patches = consolidate_document_patches(work_dir)

    return {
        "manifest": manifest_data,
        "budget": budget_data,
        "corpus_path": str(corpus_file.as_posix()),
        "corpus_raw_path": str(corpus_raw_file.as_posix()),
        "density_path": str(density_file.as_posix()),
        "vision_pages_path": str(vision_pages_file.as_posix()),
        "handouts": handouts_res,
        "sections": sections_res,
        "cta_mode": selected_cta_mode,
        "granularity": granularity,
        "consolidated_patches": consolidated_patches,
        "needs_vision_count": needs_vision_count,
        "strategy": strategy,
    }


def run_ingest(
    input_path: Union[str, Path],
    output_dir: Union[str, Path],
    cache_manifest: bool = True,
) -> Dict[str, Any]:
    """Backward compatibility wrapper invoking prepare_corpus."""
    prep = prepare_corpus(input_path, output_dir, vision="auto", legacy_transcribe=True)
    return prep["manifest"]


def main():
    parser = argparse.ArgumentParser(description="Multiformat Ingestion & Pre-processing Engine v3")
    parser.add_argument("--input", required=False, help="Input directory or file path")
    parser.add_argument("--output-dir", required=True, help="Output work directory")
    parser.add_argument("--vision", choices=["auto", "all", "none"], default="auto", help="Vision rendering mode")
    parser.add_argument("--order", required=False, help="Document order override (JSON path or comma-separated list)")
    parser.add_argument("--cta-mode", choices=["auto", "direct", "mapreduce", "multiple"], default="auto", help="CTA execution mode (direct, mapreduce, multiple, auto)")
    parser.add_argument("--granularity", choices=["fine", "standard", "coarse"], default="standard", help="Pedagogical competency granularity")
    parser.add_argument("--legacy-transcribe", action="store_true", help="Generate legacy vision batches")
    parser.add_argument("--consolidate-patches", action="store_true", help="Consolidate patch files in work/patches by document")
    parser.add_argument("--stitch", action="store_true", help="Stitch handout patches into corpus.md")
    parser.add_argument("--partial", action="store_true", help="Allow partial stitching of available patches")
    parser.add_argument("--sections", action="store_true", help="Generate section slices")
    parser.add_argument("--handouts", action="store_true", help="Create handouts from manifest")
    args = parser.parse_args()

    work_p = Path(args.output_dir)

    if args.stitch:
        res = stitch_patches_to_corpus(work_p, partial=args.partial)
        print(f"[+] Stitched {res.get('stitched_pages', 0)} pages from {res.get('patches_count', 0)} handouts into {res.get('corpus_path')}")
        return

    if args.sections:
        res = generate_section_slices(work_p)
        print(f"[+] Generated {res.get('total_sections', 0)} sections in {args.output_dir}/sections")
        return

    if args.handouts:
        m_cand = work_p / "pages" / "manifest.json"
        if not m_cand.exists():
            m_cand = work_p / "manifest.json"
        res = create_handouts(work_p, m_cand)
        print(f"[+] Created {res.get('total_handouts', 0)} handouts in {args.output_dir}/handouts")
        return

    if args.consolidate_patches and not args.input:
        res = consolidate_document_patches(work_p)
        print(f"[+] Consolidated {len(res)} document patches in {args.output_dir}")
        return

    if not args.input:
        parser.error("--input is required when not running standalone --consolidate-patches/stitch/sections/handouts")

    res = prepare_corpus(
        args.input,
        args.output_dir,
        vision=args.vision,
        legacy_transcribe=args.legacy_transcribe,
        order_override=args.order,
        cta_mode=args.cta_mode,
        granularity=args.granularity,
    )
    if args.consolidate_patches and not res.get("consolidated_patches"):
        consolidate_document_patches(work_p)

    b = res["budget"]
    print(f"[+] Ingestion complete: {res['manifest']['total_items']} items processed into {args.output_dir}")
    print(f"[+] Estimated tokens: {b['total_estimated_tokens']} | Needs vision: {b['pages_requiring_vision']} ({b['vision_strategy']}) | CTA mode: {b.get('cta_mode')}")


if __name__ == "__main__":
    main()
