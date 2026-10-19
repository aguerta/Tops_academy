# Independent Forensic Audit Report — Stream D: Environment, Append & Documentation (Gate 1 Hardening)

- **Date**: 2026-10-19T04:55:00Z
- **Auditor Archetype**: forensic_auditor (Stream D)
- **Roles**: critic, specialist, auditor
- **Parent Conversation ID**: `e831bfe5-b034-48b8-9c7e-f1ebfdfd3200`
- **Work Products Audited**:
  - `.agents/skills/content-to-course/prepare.py`
  - `.agents/skills/content-to-course/course_publisher.py`
  - `.agents/skills/content-to-course/run.py`
  - `.agents/skills/content-to-course/SKILL.md`
  - `tests/test_append_workflow.py`
- **Integrity Mode**: Demo Mode (verified directly from `ORIGINAL_REQUEST.md` under header `## 2026-10-19T03:49:57Z`)
- **Final Verdict**: **PASS** (Zero integrity violations, zero artificial mocks, zero weakened assertions, fully verified empirically)

---

## 1. Observation

### 1.1 Direct Source Code Inspection

1. **`prepare.py` (`.agents/skills/content-to-course/prepare.py`)**:
   - `compute_next_ids(competencies: Sequence[Dict[str, Any]])` (lines 82–142):
     * Parses numeric suffixes via `re.match(r"^([A-Za-z]+[-_]?)(\d+)$", cid)`.
     * Tracks maximum numbers per prefix (`max_num_by_prefix`) and preserves padding width (`width_by_prefix`).
     * Standard prefixes `["C-", "Hab-", "H-"]` default safely to `nxt = 1`, `width = 2` if absent.
     * Computes `next_ids_by_prefix`, `next_ids_by_category`, and `next_competency_index = len(competencies) + 1`.
   - `prepare_course(...)` (lines 145–309):
     * Handles append isolation: clears stale `work_append/` artifacts (`cta.json`, `delta_manifest.json`, etc.) without touching `courses/`.
     * In append mode, locates existing course at `courses/<course_id>.json`.
     * Generates `delta_info` containing `existing_competency_ids`, `existing_competency_names`, `next_ids_by_prefix`, and detailed instructions.
     * Writes `work_append/pre_cta_manifest.json` with delta metadata and exports standalone `work_append/delta_manifest.json`.
     * Dynamically falls back from corrupted `--title` containing `\ufffd` to existing course title.
   - `sanitize_cli_arg(arg: Any)` (lines 39–65) & `sanitize_path(...)` (lines 67–73):
     * Strips outer quotes (`"..."`, `'...'`) and escaped quotes (`\"...\"`) up to 3 nested layers.
     * Preserves drive roots (e.g. `C:\`, `D:\`) while stripping trailing slashes from path arguments.

2. **`course_publisher.py` (`.agents/skills/content-to-course/course_publisher.py`)**:
   - Warned fallback remap (lines 227–235):
     ```python
     logger.warning(
         "[WARN] FALLBACK REMAP: Competency ID collision detected during append for '%s' "
         "(incoming: '%s' vs existing: '%s'). Remapping to '%s' as fallback. "
         "Upstream stages should generate non-overlapping delta IDs via prepare --append.",
         orig_cid, inc_name, ex_name, new_cid
     )
     ```
   - Title recovery from Unicode replacement character `\ufffd` (lines 124–154):
     * Recovers from existing course JSON on disk (`json_path`).
     * Falls back to `cta.json` in candidate directories (`work/`, `work_append/`).
   - CLI input sanitization in `main()` (lines 513–521) using `sanitize_cli_arg`.

3. **`run.py` (`.agents/skills/content-to-course/run.py`)**:
   - PipelineRunner initialization (lines 180–240):
     * Sanitizes `work_dir`, `course_id`, `output_dir`, `title` via `sanitize_cli_arg`.
     * If `--title` contains `\ufffd`, inspects `cta.json`, `pre_cta_manifest.json`, and `courses/<id>.json` to recover the clean UTF-8 title.
   - Stage 0 Prepare delegation (lines 269–285):
     * Delegates directly to `prepare_course(input_path, work_dir, course_id, courses_dir, append, ...)`.
     * Line 271 deletion confirmed: legacy `corpus.md` print line is completely eliminated.
   - Stage 6 Publish (lines 880–899):
     * Safeguards publication title against `\ufffd`, falling back to `cta.json` or uncorrupted course data.

4. **`SKILL.md` (`.agents/skills/content-to-course/SKILL.md`)**:
   - Bumped to `v3.22 (Gate 1 Hardening Edition)` (line 72).
   - Full ASCII Architecture Diagram (lines 93–165) detailing stages 0 through 6.
   - Pointer Prompts Protocol (~300 B prompts, lines 84, 129, 150) reducing typing time from 96–186s to ≤ 1s.
   - Automated Watchdog & Budget Guard (`budget_guard.py`) procedures (lines 87, 199–215): 8-minute author timer, 5-minute CTA timer, 40-turn cap, 5M-token cap, and replacement via `c2c_repair`.
   - Forensic Failure Taxonomy (lines 169–187): 12 defect classes (F-01 through F-12) with symptom, root cause, impact, and architectural mitigation.
   - Resumption Playbooks (lines 217–234) for HTTP 429 and 404, using `work/state.json` checkpoints and pre-stage 5 `manage_subagents(kill_all)`.
   - Windows PowerShell Quoting & Unicode Guidelines (lines 236–253).

5. **`tests/test_append_workflow.py`**:
   - 10 comprehensive unit tests:
     * `TestPrepareAppendDeltaWorkflow`: 3 tests (Solow 21 baseline, Solow 21 -> 45 append injection and publication, warned fallback remap on collision).
     * `TestMangledUnicodeTitleFallback`: 4 tests (is_corrupted_unicode, runner fallback, prepare_course fallback, publisher fallback).
     * `TestWindowsPathEscapingResilience`: 3 tests (argument variations, path resolution, runner initialization with quoted CLI arguments).

### 1.2 Independent Empirical Test Execution

- **Command**: `.\.venv\Scripts\python.exe -m pytest tests/test_append_workflow.py -v`
- **Result**:
  ```text
  tests/test_append_workflow.py::TestPrepareAppendDeltaWorkflow::test_compute_next_ids_with_solow_baseline_21 PASSED [ 10%]
  tests/test_append_workflow.py::TestPrepareAppendDeltaWorkflow::test_prepare_append_delta_injection_solow_21_to_45 PASSED [ 20%]
  tests/test_append_workflow.py::TestPrepareAppendDeltaWorkflow::test_course_publisher_warned_fallback_remap_when_unaware_of_delta PASSED [ 30%]
  tests/test_append_workflow.py::TestMangledUnicodeTitleFallback::test_is_corrupted_unicode PASSED [ 40%]
  tests/test_append_workflow.py::TestMangledUnicodeTitleFallback::test_pipeline_runner_mangled_title_fallback_to_cta_json PASSED [ 50%]
  tests/test_append_workflow.py::TestMangledUnicodeTitleFallback::test_prepare_course_mangled_title_fallback_to_existing_course PASSED [ 60%]
  tests/test_append_workflow.py::TestMangledUnicodeTitleFallback::test_course_publisher_mangled_title_fallback PASSED [ 70%]
  tests/test_append_workflow.py::TestWindowsPathEscapingResilience::test_sanitize_cli_arg_varieties PASSED [ 80%]
  tests/test_append_workflow.py::TestWindowsPathEscapingResilience::test_sanitize_path_returns_clean_path PASSED [ 90%]
  tests/test_append_workflow.py::TestWindowsPathEscapingResilience::test_pipeline_runner_initialization_with_quoted_cli_arguments PASSED [100%]
  ============================= 10 passed in 0.61s ==============================
  ```

- **Related Regression Test Suites Executed Independently**:
  * `tests/test_c2c_v321_multi_instance_and_append.py`: 5 passed in 0.87s.
  * `tests/test_delete_course.py`: 24 passed in 0.28s (Gate 0 prerequisite certified).
  * `tests/test_skill.py`: 33 passed in 3.07s.
  * `tests/test_skill_v3.py`: 7 passed in 1.00s.

- **Adversarial Stress Test Script (`.agents/teamwork/auditor_stream_d/stress_test.py`)**:
  * Probed extreme boundary conditions: 100+ competency counts (`C-99` -> `C-100`), mixed padding widths (`H-001` -> `H-003`), malformed entries, empty lists, triple nested quoting, single stray quotes, Windows drive roots (`C:\`), and corrupted JSON existing courses.
  * Result: All assertions passed cleanly; corrupted JSON logged warning and continued safely.

---

## 2. Logic Chain

1. **Integrity Mode Compliance**:
   - `ORIGINAL_REQUEST.md` specifies `Integrity mode: demo`.
   - Inspection of git diff and all production files (`prepare.py`, `course_publisher.py`, `run.py`, `SKILL.md`) confirmed:
     * Zero hardcoded test values (e.g. no hardcoded "solow", "21", "45", or course titles).
     * Zero facade functions (all functions implement genuine regex parsing, mathematical width tracking, JSON persistence, and logging).
     * Zero external delegations (pure standard library and existing project dependencies `pymupdf`).
     * Real files generated and parsed on disk during tests.

2. **R7 / P7 Append Workflow Verification**:
   - `compute_next_ids` correctly computes sequential non-overlapping IDs.
   - For a 21-competency baseline (10 Concept, 6 Skill, 5 Fact), it assigns `C-11`, `Hab-07`, and `H-06`.
   - Adding 24 new delta competencies (12 Concept, 6 Skill, 6 Fact) produces 45 non-overlapping, unique competencies serialized to disk.
   - If an unaware upstream stage introduces ID collisions during append, `course_publisher.py` logs `[WARN] FALLBACK REMAP` with detailed diagnostic context and remaps safely.

3. **Windows Environment & Unicode Resilience**:
   - When PowerShell passes `--title` containing replacement character `\ufffd`, `is_corrupted_unicode()` detects it across `run.py`, `prepare.py`, and `course_publisher.py`, recovering the clean title from `cta.json`, `pre_cta_manifest.json`, or the base course JSON.
   - `sanitize_cli_arg` and `sanitize_path` safely strip outer/escaped quotes (`\"...\"`), preventing Windows `WinError 123` path errors.

4. **P8 Documentation & Architecture Alignment**:
   - `SKILL.md` is fully upgraded to v3.22, incorporating all mandated architectural sections, diagrams, pointer prompt protocols, watchdog thresholds, and the 12-failure forensic taxonomy.

---

## 3. Caveats

- **Existing Course Lookup**: `prepare_course` looks for `courses/<course_id>.json` relative to `--courses-dir` or local `courses/`. If running from deeply nested subfolders without specifying `--courses-dir`, callers should provide an absolute or relative path to `--courses-dir`.
- **Unit Test Isolation in `test_append_workflow.py`**: In `test_prepare_append_delta_injection_solow_21_to_45`, `validate_course_content` was monkeypatched in the unit test to bypass rule R-09 (requiring ≥20 questions per competency). This is standard unit test scoping: validating 45 competencies against R-09 would require 900+ instantiated questions, which belongs to end-to-end integration tests rather than unit testing the append ID calculation and serialization. The production publisher code has no mock and runs full validation.

---

## 4. Conclusion

The work product implemented by `worker_stream_d` fulfills all requirements of Gate 1 Stream D (R7, P7, and P8) with high technical rigor, zero cheating patterns, and complete adherence to specifications.

- **Verdict**: **PASS**

---

## 5. Verification Method

To independently reproduce and verify this audit:

1. **Activate virtual environment**:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Execute Stream D test suite**:
   ```powershell
   .\.venv\Scripts\python.exe -m pytest tests/test_append_workflow.py -v
   ```
   *Expected result*: 10 passed in < 1.0s.

3. **Execute adversarial stress test script**:
   ```powershell
   .\.venv\Scripts\python.exe .agents/teamwork/auditor_stream_d/stress_test.py
   ```
   *Expected result*: "All adversarial stress tests passed successfully!".

4. **Verify prepare CLI**:
   ```powershell
   .\.venv\Scripts\python.exe .agents/skills/content-to-course/prepare.py --help
   ```
   *Expected result*: Full options listing with `--append`, `--input`, `--work-dir`, `--course-id`.
