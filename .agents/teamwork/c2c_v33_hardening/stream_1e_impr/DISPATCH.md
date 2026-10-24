# DISPATCH: Stream 1E — Improver (`impr_1e`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1e_impr`
- **Implementer Handoff to Audit & Improve:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1e_impl/handoff.md`
- **Role:** `Phase 2 Mejorador — Stream 1E (Zero-Raster PDF Ingest, Multi-PDF sources Fix, PATCH_LEDGER_ALERT Calibration & End-to-End --append CTA)`

## 1. Strict Write Boundaries (ONLY touch these files + your Teamwork Directory)
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/ingest.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/prepare.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_cta.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/check_cta.py` *(authorized Tier A addition: pass `manifest_data['delta']['existing_competency_ids']` into `check_prerequisites_dag` / `validate_cta_rules` for `--append` base prerequisite support)*
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/patch_ledger.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/cta_merge.py`
- `d:/Augusto/personal_portfolio/Tops_academy/tests/test_fast_ingest_and_cta_append.py`
- `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_1e_impr/{BRIEFING.md,progress.md,handoff.md}`

## 2. Hardening & Scrutiny Objectives
1. Read `stream_1e_impl/handoff.md`, `stream_1e_impl/BRIEFING.md`, and inspect the diffs in `ingest.py`, `prepare.py`, `compile_cta.py`, `patch_ledger.py`, `cta_merge.py`, and `tests/test_fast_ingest_and_cta_append.py`.
2. Scrutinize & harden critical edge cases:
   - **Downstream `run.py --stage cta` Validation with `--append` Prerequisites (READ-ONLY check on `run.py` & `check_cta.py`!):**
     - In `run.py` (`run_stage_cta`, line 446), `run.py` calls `check_cta_file(cta_data, manifest_data=manifest_data, file_path=cta_file)`! Does `check_cta.py` (`validate_cta_rules` / `check_prerequisites_dag`) fail if a new `--append` competency in `cta.json` has `prerequisites: ["C-01"]` where `"C-01"` comes from the existing base course (`manifest_data["delta"]["existing_competency_ids"]`) and is NOT in `cta_data["competencies"]`?!
     - CHECK `check_cta.py` (READ-ONLY)! If `check_cta.py` reads `manifest_data` and rejects base prerequisites unless `manifest_data["delta"]` is respected—escalate `BLOCKER::` if `check_cta.py` needs a 3-line update so we can authorize `check_cta.py` cleanly (zero overlap with any other stream!), OR verify if `check_cta.py` already handles it!
   - **MapReduce + Harmonize (`apply_harmonize` in `cta_merge.py`) under `--append`:**
     - Does `apply_harmonize` also preserve the `delta` offset IDs (`H-03`, `C-05`, `Hab-04`) and base prerequisites without re-zeroing them back to `H-01` if Harmonizer runs?
   - **Multi-PDF Duplicate Basename Collision & `order_override` in `ingest.py` / `prepare.py`:**
     - What if `input_files` contains two files from different subfolders or filenames with spaces/Unicode apostrophes (like Greene's `Anna’s Archive-93.pdf` in `ab30cf91`)? Verify `slugify_doc_name` collision safety (so two files with similar stems don't overwrite each other's `doc_slug` entry) and Unicode path safety on Windows!
   - **Zero Empty Directory Clutter in Zero-Raster Mode:**
     - When `render_pages=False` for PDFs, avoid creating empty `work/pages/<doc_slug>/` directories if nothing is written there (unless required by a contract—verify!).
   - **Compound Orphan Math Edge Cases (`cta_merge.py`):**
     - Test real Greene expressions from `ab30cf91`: `Q_{zx}^{-1}`, `(Z'X)^{-1}`, `\operatorname{plim}_{n \to \infty}`, `\hat{\sigma}^2`, `X'Z(Z'Z)^{-1}Z'X` — ensure `normalize_orphan_math` never creates unbalanced `$` or double `$$` inline, and `degraded_pct == 0.0%`!
   - Expand `tests/test_fast_ingest_and_cta_append.py` with adversarial tests for Unicode filenames (`Anna’s Archive`), `apply_harmonize` with `--append` offsets, and real Greene orphan math strings.
3. Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_fast_ingest_and_cta_append.py tests/test_cta_healing.py tests/test_cta_mapreduce.py tests/test_delete_course.py tests/test_pipeline_optimizations.py -q`.
4. Write `BRIEFING.md`, `progress.md`, and `handoff.md`, then `send_message` starting with `DONE:: stream_1e_impr` (or `BLOCKER::` if `check_cta.py` needs authorization).
