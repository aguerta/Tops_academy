# DISPATCH: Stream 1E — Implementer (`impl_1e`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1e_impl`
- **Role:** `Phase 1 Implementador — Stream 1E (Zero-Raster PDF Ingest, Multi-PDF sources Fix, PATCH_LEDGER_ALERT Calibration & End-to-End --append CTA)`

## 1. Strict Write Boundaries (ONLY touch these files + your Teamwork Directory)
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/ingest.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/prepare.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_cta.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/patch_ledger.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/cta_merge.py`
- `d:/Augusto/personal_portfolio/Tops_academy/tests/test_fast_ingest_and_cta_append.py` *(new)*
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1e_impl/{BRIEFING.md,progress.md,handoff.md}`

*(Forbidden: Do NOT edit `run.py`, `dispatch.py`, `delete_course.py` [unless a real bug is found, in which case escalate `BLOCKER::`], `compile_shard.py`, or any other file outside the list above!)*

## 2. Technical Specifications
1. **Step 0 Pre-Flight Sanity Check:**
   - Read `ingest.py`, `prepare.py`, `compile_cta.py` (especially around `record_patch` / `PATCH_LEDGER_ALERT` and `--manifest` / ID assignment), `patch_ledger.py`, `cta_merge.py` (around `merge_cta_parts` lines 500–600), and existing tests (`tests/test_*ingest*`, `tests/test_*prepare*`, `tests/test_*cta*`, `tests/test_*delete*`).
   - **Pay special attention to backward compatibility with existing `ingest.py` unit tests!** Check whether existing tests call `ingest_course(in_path, work_dir)` and assert `work/pages/<slug>/page_001.png` exists! If legacy unit tests expect `ingest_course()` direct calls to render PNGs by default OR if `prepare_course()` can pass `render_pages=False` (or `ingest_course(..., render_pages: bool = False)` if no legacy test breaks—CHECK EXISTING TESTS FIRST!), design the default/flag cleanly so `prepare_course` / C2C pipeline runs **Zero-Raster PDF Ingest (`< 0.5s`, 0 PNGs rendered for PDFs)** while keeping 100% of existing tests green! Document this carefully in `BRIEFING.md`.
2. **Zero-Raster PDF Ingest & Explicit Multi-File `input_files` (`ingest.py` + `prepare.py`):**
   - In `ingest.py` (`ingest_course`):
     - Support `render_pages: bool = False` (verify against existing tests in Step 0!) and CLI flag `--render-pages` / `--no-render-pages`: when `render_pages` is `False`, for `file_type == "pdf"`, open with `pymupdf.open(fpath)`, read `num_pages = len(doc)`, close `doc` immediately (**do NOT call `page.get_pixmap()` or save `page_XXX.png`**!). Keep `ingest_image_file` (tiling raster images `> 3072px`) and `ingest_tex_file` active as before.
     - Add `input_files: Optional[Sequence[Union[str, Path]]] = None` parameter to `ingest_course`: when provided, process ONLY those exact resolved files instead of walking `in_path` directory!
   - In `prepare.py` (`prepare_course` around line 191):
     - Fix the catastrophic multi-PDF bug `input_target = sources[0] if len(sources) == 1 else sources[0].parent`! Pass `input_files=sources` (and `render_pages=False` by default, with optional `render_pages: bool = False` param on `prepare_course`) directly to `ingest_course()`, so passing 2 PDFs inside a folder of 20 PDFs NEVER scans or ingests the other 18 unrelated PDFs!
     - In `--append` mode (`prepare.py`), enrich `delta_manifest.json` (and `manifest["delta"]` in `pre_cta_manifest.json`) with `"existing_competencies_outline": [{"id": c["id"], "type": c.get("type"), "name": c.get("name")} for c in existing_comps]` alongside `"next_ids_by_prefix"`.
3. **Separate Harmless Deterministic LaTeX Healing from `degraded` in `PATCH_LEDGER_ALERT` (`compile_cta.py` + `patch_ledger.py`):**
   - In `ab30cf91` (`part_01`, Step 10), `compile_cta.py` failed with exit code 1: `PATCH_LEDGER_ALERT: ALERT: Degraded fields (10, 62.5%) exceed the strict threshold of 3.0%` simply because deterministic LaTeX math wrapping (`Q_{zx}^{-1}` -> `$Q_{zx}^{-1}$`) was recorded as `"degraded"` and divided by `16` competencies (`10/16 = 62.5%`)!
   - Inspect all `record_patch(...)` calls in `compile_cta.py` and `patch_ledger.py`:
     - Classify lossless/mechanical LaTeX normalizations (`$...$` orphan math wrapping, `{{x}} -> {x}`, `$$ -> $`, `r"..."` conversion, control-char healing) strictly as `severity="healed"` (or `"snapped"` for page-range snapping). Reserve `severity="degraded"` ONLY for genuine content degradation (e.g., unparseable broken LaTeX stripped/escaped to `\text{...}` fallback or truncated/empty fallback text).
     - Set `ledger.set_total_fields(total_evaluated_fields)` in `compile_cta.py` using the actual count of evaluated string fields across competencies and distractors (not just `len(competencies)`), so `degraded_percentage()` reflects the true field degradation rate!
4. **End-to-End Continuous IDs in `--append` Mode (`compile_cta.py` + `cta_merge.py`):**
   - Today `cta_merge.py` (`merge_cta_parts`, lines 509–511) hardcodes `fact_count = 0; concept_count = 0; skill_count = 0`, wiping out `delta_manifest.json` (`next_ids_by_prefix`)!
   - In `cta_merge.py` (`merge_cta_parts` and `apply_harmonize` if it renumbers) AND in `compile_cta.py` (when compiling direct-mode `cta_data.py` -> `cta.json` with a manifest containing `delta.next_ids_by_prefix` or `work/delta_manifest.json`):
     - Read `next_ids_by_prefix` (e.g., `{"H": 5, "C": 12, "Hab": 8}` or integer/string `"H-05"`—handle both int and `"H-05"` formats safely!) and initialize `fact_count = next_H - 1`, `concept_count = next_C - 1`, `skill_count = next_Hab - 1`!
     - Also allow prerequisites in new `--append` competencies to validly reference `existing_competency_ids` from `delta_manifest.json` without failing `check_cta` / `cta_merge` prerequisite validation! (Check if `compile_cta.py` / `cta_merge.py` strips unknown prereqs when `--append` references an existing base competency ID like `C-01`, and preserve valid existing base IDs!).
5. **Bottleneck #10 Active Workspace Protection Regression Test:**
   - Include a test in `tests/test_fast_ingest_and_cta_append.py` importing `delete_course` (`is_active_workspace` / `clean_orphan_course_dirs`) and verifying that both `courses/<slug>/work/` and `courses/<slug>/work_append/` containing a fresh `pre_cta_manifest.json` or `state.json` are NEVER deleted.

## 3. Required Tests & Verification
- Create `tests/test_fast_ingest_and_cta_append.py` covering:
  - Zero-Raster speed & zero PNG creation on multi-page PDF via `prepare_course` (`< 1.0s`).
  - Multi-PDF subset isolation: directory with 4 PDFs where `prepare_course` is given only 2 PDFs -> `pre_cta_manifest.json` has `total_files == 2` (NOT 4!).
  - `compile_cta.py` with 10 orphan LaTeX fields (`Q_{zx}^{-1}`, `\alpha`, `x_{t-1}`) -> compiles with `ok=True`, `0` errors, `degraded_pct == 0.0%`, `healed >= 10`.
  - End-to-end `--append`: base course with `H-01..H-02`, `C-01..C-04`, `Hab-01..Hab-03` -> `prepare_course(..., append=True)` -> `compile_cta` + `merge_cta_parts` produces new IDs starting at `H-03`, `C-05`, `Hab-04` and `D-H03-01..06`!
  - `delete_course.py` active `work_append/` protection.
- Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_fast_ingest_and_cta_append.py -q` plus all existing tests for `ingest`, `prepare`, `compile_cta`, `cta_merge`, and `delete_course`!
