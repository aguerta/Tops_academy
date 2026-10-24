# Stream 1E Implementation Handoff Report

**Date:** 2026-10-24  
**Implementer:** Phase 1 Implementer (`stream_1e_impl`)  
**Target:** Stream 1E — Zero-Raster PDF Ingest, Multi-PDF Sources Fix, PATCH_LEDGER_ALERT Calibration & End-to-End `--append` CTA  
**Status:** COMPLETE (All Tests Passing, 0 Regressions)

---

## 1. Summary of Files & Functions Changed

### 1. `ingest.py`
- **`ingest_course(...)`**:
  - Added parameter `render_pages: bool = True` (backward compatible default for direct legacy test calls; in CLI defaults to `False` via `--render-pages` / `--no-render-pages`).
  - Added parameter `input_files: Optional[Sequence[Union[str, Path]]] = None`: when passed, processes strictly the resolved input file paths instead of walking `input_path` directory.
  - When `render_pages=False` and `file_type == "pdf"`, opens `pymupdf.open(fpath)`, reads `len(doc)` for page counts, and closes immediately without calling `page.get_pixmap()` or saving `page_XXX.png`.
- **CLI parser**:
  - Added `--render-pages` (action="store_true", default=False) and `--no-render-pages` (action="store_false").

### 2. `prepare.py`
- **`prepare_course(...)`**:
  - Added parameter `render_pages: bool = False` (defaulting to zero-raster ingest).
  - Fixed catastrophic directory scan bug (previously `input_target = sources[0] if len(sources) == 1 else sources[0].parent`): now passes `input_files=sources` and `render_pages=render_pages` directly into `ingest_course()`.
  - In `--append` mode, enriched `delta_info` and central `pre_cta_manifest.json` / `delta_manifest.json` with `"existing_competencies_outline": [{"id": c.get("id") or c.get("competency_id"), "type": c.get("type") or c.get("category", "concept").lower(), "name": c.get("name") or c.get("title")} for c in existing_comps]`.

### 3. `cta_merge.py`
- **`normalize_orphan_math(text)`**:
  - Upgraded regex 5b from `\b([a-zA-Z0-9\\]+[_^](?:\{[a-zA-Z0-9_+\-*./]+\}|\*))` to `\b([a-zA-Z0-9\\]+(?:[_^](?:\{[a-zA-Z0-9_+\-*./]+\}|[a-zA-Z0-9*+]+))+)` to handle compound sub/superscripts (e.g. `Q_{zx}^{-1}` -> `$Q_{zx}^{-1}$` instead of corrupted `$Q_{zx}$^{-1}`).
- **`sanitize_competency_math(comp, record_patches=True)`**:
  - When mechanical wrapping or healing modifies fields in competencies or distractors, records patches via `record_patch(stage="cta", layer="L2", rule_id="NORMALIZE_ORPHAN_MATH", severity="healed", ...)` so deterministic normalizations are never counted as degraded.
- **`parse_next_ids_by_prefix(delta_info)`**:
  - New robust parser supporting `None`, int maps (`{"H": 5, "C": 12, "Hab": 8}`), string maps (`{"H-": "H-03", ...}`), and category maps.
- **`merge_cta_parts(work_dir)`**:
  - Reads `delta_info` and initializes `fact_count = next_H - 1`, `concept_count = next_C - 1`, `skill_count = next_Hab - 1` to guarantee continuous sequential IDs in `--append` mode.
  - Rewrites distractor prefixes (`D-H03-01..06`, etc.) and preserves existing base course prerequisites (e.g. `C-01`).
- **`apply_harmonize(...)`**:
  - Loaded `existing_competency_ids` from delta manifest. In `add_prerequisites`, permits prerequisites that reference existing base competencies. In DAG check, validates with existing base competency nodes present. In `validate_cta_rules`, filters out false-positive DAG errors for existing base IDs.

### 4. `compile_cta.py`
- **`count_evaluated_fields(cta_dict)`**:
  - Evaluates all string and structural fields across competencies and distractors (~60 fields per competency) to provide the true denominator for degraded percentage calculations.
- **`compile_cta_module(...)`**:
  - Added `initial_counts: Optional[Dict[str, int]] = None` and `existing_competency_ids: Optional[Set[str]] = None`.
  - Supports continuous IDs starting at `next_H`, `next_C`, `next_Hab`. Detects collisions with existing base IDs and reallocates cleanly.
- **`compile_cta(...)`**:
  - Reordered pipeline to load `manifest_data` and `delta_info` before invoking `compile_cta_module`.
  - Passed `initial_counts` and `existing_competency_ids`.
  - Filtered out non-existent prerequisite errors in `validate_cta_rules` (and after L5 degrade) when the prerequisite is in `existing_competency_ids`.
  - Set `get_ledger().set_total_fields(total_eval_fields)` and passed `total_items=total_eval_fields` to `save_run_ledger`, `save_cta_review`, `append_cross_run_record`, and `check_degraded_alert`.

### 5. `tests/test_fast_ingest_and_cta_append.py` (New Test Suite)
- Covers:
  1. Zero-Raster speed (< 1.0s) & 0 PNGs rendered on multi-page PDFs.
  2. Multi-PDF subset isolation (selecting 2 PDFs out of 4 in the same directory ingests only the 2 requested).
  3. Compound sub/superscript regex healing (`Q_{zx}^{-1}`, `\alpha`, `x_{t-1}`).
  4. 10 orphan LaTeX fields compile with `ok=True`, 0 errors, `degraded_pct == 0.0%`, `healed >= 10`.
  5. `parse_next_ids_by_prefix` format compatibility.
  6. End-to-end direct `--append`: produces continuous IDs `H-03`, `C-05`, `Hab-04`, `D-H03-01..06`, with `C-01` base prereqs accepted.
  7. End-to-end map-reduce `--append`: `merge_cta_parts` produces continuous IDs and distractor prefixes.
  8. Active workspace protection in `delete_course`: verifies `is_active_workspace` and `clean_orphan_course_dirs` never delete `courses/<slug>/work/` or `courses/<slug>/work_append/` containing fresh state files.

---

## 2. Test Verification & Results

Command executed:
```powershell
& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_fast_ingest_and_cta_append.py tests/test_cta_healing.py tests/test_cta_mapreduce.py tests/test_delete_course.py tests/test_handouts.py tests/test_pipeline_optimizations.py -q
```

Results:
- **`test_fast_ingest_and_cta_append.py`**: 8 passed (0.48s)
- **`test_cta_healing.py`**: 15 passed (0.40s)
- **`test_cta_mapreduce.py`**: 18 passed (4.23s)
- **`test_delete_course.py`**: 24 passed (1.89s)
- **`test_handouts.py`**: 6 passed (1.19s)
- **`test_pipeline_optimizations.py`**: 4 passed, 2 skipped (0.41s)
- **TOTAL**: **75 passed, 2 skipped, 0 failed in 7.96s** (100% green).

---

## 3. Edge Cases for Improver (`Phase 2 of 3: Improver`) to Scrutinize

1. **`ingest_course` Default Parameter vs Pipeline Ingest:**
   - `ingest_course` default in Python signature is `render_pages: bool = True` to preserve exact backward compatibility with legacy unit tests (e.g. `tests/test_handouts.py`).
   - `prepare_course` (and CLI `ingest.py`) explicitly defaults `render_pages=False`. The Improver should verify whether all production C2C entry points invoke through `prepare_course` or CLI.
2. **Compound Subscript Variations in Orphan Math:**
   - The upgraded regex `\b([a-zA-Z0-9\\]+(?:[_^](?:\{[a-zA-Z0-9_+\-*./]+\}|[a-zA-Z0-9*+]+))+)` handles `Q_{zx}^{-1}`, `x_1^2`, `k^*`, etc. Improver can test exotic combinations like triple sub/superscripts or nested subscripts if needed.
3. **Prerequisite DAG Cycles with Base Course:**
   - In `--append` mode, delta competencies may reference base course competencies. Because base competencies are effectively at index `< 0` and have no outgoing edges into the delta, cycles between base and delta cannot occur unless base competencies are somehow modified (which is forbidden in append mode).
