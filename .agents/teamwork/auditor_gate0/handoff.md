# Forensic Audit Report: Gate 0 Safety Foundation & Legacy Purge

**Audited Work Product**: Gate 0 Implementation by `worker_gate0`
**Integrity Mode**: Demo (per `ORIGINAL_REQUEST.md` under `## 2026-10-19T03:49:57Z`)
**Auditor Identity**: Gate 0 Independent Forensic Auditor (`teamwork_preview_auditor`)
**Verdict**: **PASS (CLEAN)**

---

## 1. Observation

Direct empirical observations made across the audited codebase and runtime environments:

1. **`delete_course.py` Active Workspace Guard & Path Safety**:
   - In `.agents/skills/delete-course/scripts/delete_course.py:46-87`, `ACTIVE_WORKSPACE_STATE_FILES` defines:
     ```python
     ACTIVE_WORKSPACE_STATE_FILES: Tuple[str, ...] = (
         "work/state.json",
         "work/pre_cta_manifest.json",
         "work/cta_data.py",
         "state.json",
         "pre_cta_manifest.json",
         "cta_data.py",
     )
     ```
   - In `is_active_workspace(course_dir: Path, max_age_seconds: float = 24 * 3600) -> bool`:
     * Checks `(course_dir / rel_path).is_file()` for all items in `ACTIVE_WORKSPACE_STATE_FILES`. If present, returns `True` immediately.
     * Recursively traverses `course_dir.rglob("*")` for any file with `(time.time() - mtime) < max_age_seconds`. If any recent file is found, returns `True`.
     * Gracefully captures `(OSError, ValueError)` on stat calls, preventing crashes from broken links or permissions.
   - In `get_effective_courses_dir()`: checks `os.environ["COURSES_DIR"]` and falls back to module attribute `COURSES_DIR`.
   - In `clean_orphan_course_dirs()`:
     ```python
     if is_active_workspace(d):
         continue
     ```
     Guarantees that directories with active state files or recent files (<24h) are never deleted.
   - In `assert_path_safe(target_path: Path)`:
     * Enforces checks 1 (`content/`, `contents/`), 2 (`courses/fixtures`), and 3 (`PROTECTED_RELATIVE_DIRS`) **prior** to path resolution.
     * Permits operation in `effective_courses` (e.g. `tmp_path` during test execution) while maintaining an ironclad block on `content/` and `fixtures/`.

2. **`test_delete_course.py` Test Suite Isolation & Multi-Faceted Verification**:
   - In `tests/test_delete_course.py:172-261` (`test_clean_orphan_dirs`):
     * Strictly isolates the execution directory using `tmp_path` via `monkeypatch.setattr(delete_course_mod, "COURSES_DIR", tmp_path)` and `monkeypatch.setenv("COURSES_DIR", str(tmp_path))`.
     * Tests 7 distinct scenario folders: fixtures directory, active course with `.json`, active in-progress workspace with `work/pre_cta_manifest.json` (artificially aged to 48h), active workspace with `work/state.json` (aged 48h), active workspace with `work/cta_data.py` (aged 48h), active workspace with recent file (<24h, no state files), and old stale orphan directory (>48h, no state files).
     * Snapshots the real `courses/` directory before and after deletion:
       ```python
       real_courses_dir = REPO_ROOT / "courses"
       real_before = set(real_courses_dir.iterdir()) if real_courses_dir.exists() else set()
       ...
       real_after = set(real_courses_dir.iterdir()) if real_courses_dir.exists() else set()
       assert real_before == real_after
       ```
     * Verifies that the stale orphan is deleted while all active workspaces, recent files, and fixtures survive untouched.
   - Added unit test class `TestActiveWorkspaceSafeguards` (lines 280-322) testing individual isolation scenarios for state files, recent files, stale files, and empty directories.
   - Added unit test class `TestLatexRegexFracFix` (lines 323-366) testing `\frac{S_{xy}}{S_{xx}}`, `\frac{K^{0.5}}{L^{0.5}}`, `\frac{\sigma_{xy}^2}{\sigma_{xx}^2}`, and broken brace repair `\frac{a{b}`.
   - Added unit test class `TestPurgeLegacyCorpusAndSections` (lines 367-472) asserting absence of legacy references across dispatch, run banner, system prompts, skill instructions, generated dispatch items, and docs.

3. **`assemble.py` LaTeX Fraction Regex (`frac_simple_fix`)**:
   - In `.agents/skills/content-to-course/engine/assemble.py:207-210`:
     ```python
     frac_simple_fix = re.compile(
         r"(\\(?:frac|dfrac|tfrac|cfrac)\s*\{[^{}\\^_]+)\{([^{}]+\})"
     )
     text = frac_simple_fix.sub(r"\1}{\2", text)
     ```
   - Character class `[^{}\\^_]+` excludes subscripts `_` and superscripts `^`, preventing corruption of mathematical formulas like `\frac{S_{xy}}{S_{xx}}` and `\frac{K^{0.5}}{L^{0.5}}` (Defect #6 in forensic synthesis §3.1).

4. **Legacy Purge of `corpus.md` and `section_*.md`**:
   - `dispatch.py:240`: `ROLE_SPECS["cta-map"]["read"]` replaced `"work/sections/section_*.md"` with `"work/parts/part_*/**"` and `"work/parts/part_manifest_*.json"`.
   - `dispatch.py:463, 546, 559`: Replaced `corpus.md` fallbacks with direct source path / slice path or hard `BLOCKER::` failure.
   - `dispatch.py:584`: Scope header for role `cta` reads `[manifest_rel, "content/**"]` with zero mentions of `corpus.md`.
   - `run.py:222`: Stage 0 banner updated to `"Stage 0: Lossless source partitioning & pre_cta_manifest generation"`.
   - `run.py:271`: Misleading stdout print statement for `Corpus file:` deleted.
   - `SKILL.md`: Lines 92, 110, 180 updated to document direct PDF and `pymupdf` slice access.
   - `system_prompts/prompt_competence_analyser.md` and `prompt_cta_sectional.md`: All mentions of `corpus.md` and `section_XX.md` purged.
   - `README.md` and `PROJECT.md`: References to `corpus.md` and `Corpus Slicing` purged.
   - Repo-wide search confirms 0 operational residual references to `corpus.md` or `section_*.md`.

5. **Independent Execution Results**:
   - Pytest execution:
     ```powershell
     .\pytest.cmd tests/test_delete_course.py -v
     ```
     Result: **24 passed in 0.84s (100% pass rate)**.
   - Standalone adversarial Python execution:
     All 6 forensic verification checks (aged manifest protection, recent file protection, stale file cleanup, COURSES_DIR override, assert_path_safe immutability, and LaTeX fraction sanitization) passed cleanly.

---

## 2. Logic Chain

1. **Safety Foundation**:
   - Observation 1 proves that `is_active_workspace` explicitly checks both state files (`work/state.json`, `work/pre_cta_manifest.json`, `work/cta_data.py`) and file modification times (<24h).
   - In `clean_orphan_course_dirs`, calling `if is_active_workspace(d): continue` guarantees that active in-progress workspaces (such as those lost during runs 1, 2, and 3) cannot be deleted even if they lack a published `.json` file.
   - In `assert_path_safe`, checking immutable roots and fixtures before effective directory resolution guarantees that even under a malicious or misconfigured `COURSES_DIR` override, source content and fixtures remain inviolable.

2. **Test Isolation**:
   - Observation 2 demonstrates that `test_clean_orphan_dirs` is strictly bound to `tmp_path` using both `monkeypatch.setattr` and `monkeypatch.setenv`.
   - Asserting `real_before == real_after` provides empirical proof that running the test suite will never touch, delete, or alter any directory in the real production `courses/`.

3. **LaTeX Engine Integrity**:
   - Observation 3 confirms the regex adjustment `[^{}\\^_]+`. By excluding `_` and `^` from the numerator match, expressions with subscripts or exponents in the fraction numerator are not mismatched as unclosed braces, while broken braces such as `\frac{a{b}` are still properly healed to `\frac{a}{b}`.

4. **Legacy Artifact Purge**:
   - Observation 4 confirms that all residual references, fallback paths, and stdout print statements for `corpus.md` and `section_*.md` were eliminated across scripts, prompts, and documentation.
   - Automated tests in `test_delete_course.py` enforce this invariant continuously against regression.

5. **Anti-Cheating & Integrity Compliance**:
   - Source code analysis revealed zero artificial mocks, zero dummy return constants, zero hardcoded test bypasses, and zero weakened assertions.
   - Tests execute real filesystem I/O, timestamp manipulation via `os.utime`, and real regex transformations.
   - In accordance with Demo Mode rules in `ORIGINAL_REQUEST.md`, all logic was implemented from scratch using the Python standard library.

---

## 3. Caveats

- **Full Test Suite Scope**: The full repository test suite (`python -m pytest tests -q`) was deliberately NOT executed at Gate 0, in strict compliance with the execution lock defined in `ORIGINAL_REQUEST.md` ("executed strictly after Gate 0 / P0 isolation is certified") and because `playwright` is not installed in the root environment.
- **Empty Orphan Workspaces**: An orphan directory containing zero files and no state files is identified as inactive by `is_active_workspace` and will be removed by `clean_orphan_course_dirs`. This is by design, as truly empty orphan directories represent abandoned artifacts.

---

## 4. Conclusion

The implementation provided by `worker_gate0` fulfills 100% of the Gate 0 requirements specified in `ORIGINAL_REQUEST.md` (R1), `c2c_hardening_plan.md` (§5 P0), and `master_forensic_synthesis_7_runs.md` (§3.1).

- Active workspace data safety: **VERIFIED**.
- Real `courses/` directory isolation: **VERIFIED**.
- LaTeX fraction regex fix: **VERIFIED**.
- Legacy `corpus.md` and `section_*.md` purge: **VERIFIED**.
- Anti-cheating & integrity checks: **CLEAN (ZERO VIOLATIONS)**.

**Final Verdict**: **PASS**

---

## 5. Verification Method

To independently reproduce this verification:

```powershell
# 1. Run the targeted Gate 0 test suite
.\pytest.cmd tests/test_delete_course.py -v

# 2. Verify zero operational mentions of corpus.md across skills
git grep -i "corpus.md" .agents/skills/content-to-course/

# 3. Verify real courses directory remains untouched
ls courses/
```

Invalidation conditions:
- Any failure in `tests/test_delete_course.py`.
- Any modification of files in the real `courses/` or `content/` during test runs.
- Any re-introduction of `work/corpus.md` or `section_*.md` in `dispatch.py` or `run.py`.
