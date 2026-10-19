# Dispatch: Gate 2 Integration & End-to-End Benchmark Worker

## Identity
- Role: Gate 2 Integration & Benchmark Worker
- Type: teamwork_preview_worker
- Working Directory: d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_gate2/
- Parent Conversation ID: e831bfe5-b034-48b8-9c7e-f1ebfdfd3200

## Mission & Scope
1. **Reconciliation & Regression Harmonization**:
   - Reconcile any legacy tests in `tests/` that assumed older static sharding or deprecated interfaces (e.g. `test_shard_default_amortized_v32` in `tests/test_template_variability.py` which expected static 6 comps/shard instead of v3.22 adaptive formula `clamp(ceil(N/8), 2, 6)`).
   - Ensure all suites pass cleanly:
     * `python -m pytest tests/test_delete_course.py tests/test_cta_healing.py tests/test_latex_engine.py tests/test_compile_shard.py tests/test_orchestration_resilience.py tests/test_append_workflow.py -q`
     * Full repository test suite: `python -m pytest tests -q` (executed now that Gate 0 data safety isolation is certified PASS). If Playwright tests are skipped due to browser env, document skipped status cleanly.
2. **Execute MapReduce P3.0 Spike against `solow_model`**:
   - Run the MapReduce partitioning and verification spike against the `solow_model` source corpus (`content/Solow_model/` or `content/I__Ecuaciones_en_derivadas_parciales_2026.pdf` if Solow source is located there; check `content/` and `courses/solow_model.json`).
   - Use `partition_corpus.py` to partition the corpus with structural weight analysis, verify bookmark snapping, physical slicing into `work/parts/part_NN/`, and verify `cta_merge.py` coordinate remapping and DAG validity (no cycles, backward prerequisites).
   - Verify: zero text extraction, pixel-identical slicing, cross-partition prerequisite remapping.
3. **Acceptance Criteria Verification**:
   - Verify all Programmatic Regression & Unit Testing items in `ORIGINAL_REQUEST.md`:
     * Target suites pass 100% clean.
     * Full repository suite passes without regressions.
     * `clean_orphan_course_dirs` verified not to delete active workspaces or <24h files.
     * Zero stdout occurrences of `corpus.md` or `section_*.md`.
   - Verify Performance & Quality Benchmark Gates metrics (record synthesis in `BENCHMARK_REPORT.md` in your folder or `reports/`).

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
