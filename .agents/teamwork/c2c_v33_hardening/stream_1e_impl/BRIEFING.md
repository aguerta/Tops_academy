# BRIEFING: Stream 1E Pre-Flight Verification & Implementation Plan

**Date:** 2026-10-24  
**Author:** Phase 1 Implementer (`impl_1e`)  
**Target:** Stream 1E (Zero-Raster PDF Ingest, Multi-PDF Sources Fix, PATCH_LEDGER_ALERT Calibration & End-to-End `--append` CTA)

---

## 1. Pre-Flight File & Signature Verification

All target files in Write Boundaries were inspected in Step 0:
1. `ingest.py`:
   - Current signature: `ingest_course(input_path, output_dir, course_id=None, cta_mode="direct", dpi=150, order_override=None, **kwargs)`
   - Backward compatibility check: `tests/test_handouts.py::test_stage0_ingest_multiformat_pdf_tex_image` calls `ingest_course(in_dir, work_dir, ...)` without `render_pages` and asserts `len(list((work_dir / "pages" / "lecture_01").glob("page_*.png"))) == 3`.
   - **Resolution:** In `ingest_course`, set `render_pages: bool = True` by default so direct legacy unit test calls continue to render page PNGs without regressions. In `prepare_course` (`prepare.py`), pass `render_pages=render_pages` where `prepare_course` defaults to `render_pages: bool = False`. Additionally, in CLI `ingest.py`, add `--render-pages` / `--no-render-pages` defaulting to `render_pages=False`.
   - `input_files` parameter: Add `input_files: Optional[Sequence[Union[str, Path]]] = None` to `ingest_course`. When provided, process ONLY those exact resolved files without walking `in_path`.

2. `prepare.py`:
   - Line 191 currently contains `input_target = sources[0] if len(sources) == 1 else sources[0].parent`. If 2 PDFs from a 20-PDF folder are passed, it scans the entire parent folder!
   - **Resolution:** Pass `input_files=sources` directly to `ingest_course(input_path=sources[0], output_dir=clean_work_dir, ..., render_pages=render_pages, input_files=sources)`.
   - In `--append` mode: Enrich `delta_info` and `manifest["delta"]` with `"existing_competencies_outline": [{"id": c.get("id") or c.get("competency_id"), "type": c.get("type") or c.get("category", "concept").lower(), "name": c.get("name") or c.get("title")} for c in existing_comps]`.

3. `compile_cta.py` & `patch_ledger.py`:
   - Root cause of `ab30cf91` failure: `normalize_orphan_math` in `cta_merge.py` had regex 5b matching single sub/superscript only (`([a-zA-Z0-9\\]+[_^](?:\{...\}|\*))`), truncating `Q_{zx}^{-1}` into `$Q_{zx}$^{-1}`. The remaining `^{-1}` triggered KaTeX raw LaTeX errors in `check_cta.py`, which caused `compile_cta.py` to trigger L5 degrade fallback, which replaced with `\text{...}`, recorded 10 patches as `"degraded"`, and divided by `len(competencies) == 16` (`10/16 = 62.5% > 3.0%`), aborting with `PATCH_LEDGER_ALERT`.
   - **Resolution:**
     1. In `cta_merge.py`, upgrade regex 5b in `normalize_orphan_math` to match repeated/compound sub/superscripts `(?:[_^](?:\{[a-zA-Z0-9_+\-*./]+\}|[a-zA-Z0-9*+]+))+`.
     2. In `cta_merge.py`, when `sanitize_competency_math` wraps orphan math or heals KaTeX, record with `severity="healed"`, layer="L2", rule_id="NORMALIZE_ORPHAN_MATH".
     3. In `compile_cta.py`, calculate `total_eval_fields` by counting every evaluated string field across all competencies and distractors (not just `len(competencies)`).
     4. Set `get_ledger().set_total_fields(total_eval_fields)` and pass `total_items=total_eval_fields` to ledger methods.

4. `cta_merge.py` & `compile_cta.py` Continuous IDs in `--append`:
   - Lines 509-511 in `cta_merge.py` (`merge_cta_parts`) hardcoded `fact_count = 0`, `concept_count = 0`, `skill_count = 0`.
   - **Resolution:**
     1. Read `next_ids_by_prefix` from `manifest_data.get("delta")` or `delta_manifest.json` using a helper that handles both int (`{'H': 5}`) and string (`{'H-': 'H-05'}`).
     2. Initialize `fact_count = next_H - 1`, `concept_count = next_C - 1`, `skill_count = next_Hab - 1`.
     3. In `compile_cta.py`, support `next_ids_by_prefix` during ID assignment.
     4. In both `compile_cta.py` and `cta_merge.py`, permit prerequisites in new delta competencies to reference `existing_competency_ids` from `delta_manifest.json`.

5. Active Workspace Protection:
   - Verify `delete_course.py` protection for `courses/<slug>/work/` and `courses/<slug>/work_append/` containing fresh state files (`pre_cta_manifest.json` or `state.json`).

---

## 2. Execution Sequence
1. Write `progress.md`.
2. Edit `ingest.py`: Add `render_pages` and `input_files` to `ingest_course`; update CLI args.
3. Edit `prepare.py`: Fix `input_files=sources` call, pass `render_pages=render_pages`, enrich `existing_competencies_outline` in delta manifest.
4. Edit `cta_merge.py`: Fix compound sub/superscript regex, record orphan math wraps as `healed`, implement `next_ids_by_prefix` initialization and existing prerequisite allowance.
5. Edit `compile_cta.py`: Count total evaluated fields as denominator, record lossless fixes as `healed`, support continuous IDs and existing prerequisite allowance in append mode.
6. Create `tests/test_fast_ingest_and_cta_append.py` with full test matrix.
7. Run test suite: New tests + existing suites (`test_handouts.py`, `test_pipeline_optimizations.py`, `test_skill.py`, `test_cta_healing.py`, `test_cta_mapreduce.py`, `test_delete_course.py`).
8. Write `handoff.md` and notify Orchestrator via `send_message`.
