# Handoff Report: Gate 0 Safety Foundation & Legacy Purge Worker

## 1. Observation
1. **`delete_course.py` Workspace Deletion Risk**:
   - In `.agents/skills/delete-course/scripts/delete_course.py:465-484`, `clean_orphan_course_dirs` iterated over `COURSES_DIR.iterdir()` and immediately deleted any directory whose name was not present in `active_json_stems`, without inspecting whether active generating runs or state files existed:
     ```python
     if d.name not in active_json_stems:
         if not dry_run:
             shutil.rmtree(d, ignore_errors=True)
         cleaned.append(str(d))
     ```
   - Furthermore, `COURSES_DIR` was hardcoded to `REPO_ROOT / "courses"`, preventing test runners from isolating deletion operations to temporary directories.
2. **`test_delete_course.py` Operating on Real Repository `courses/`**:
   - In `tests/test_delete_course.py:164-173`, `test_clean_orphan_dirs` created a folder `REPO_ROOT / "courses" / "temp_orphan_dir_unit_test"` directly inside the production `courses/` directory and ran `clean_orphan_course_dirs(dry_run=False)`, which actively deleted any intermediate course folders in `courses/` that lacked a published `.json` file (documented in forensic synthesis §3.1 as the direct cause of lost workspace files during runs 1, 2, and 3).
3. **`assemble.py` LaTeX Fraction Subscript/Superscript Corruption**:
   - In `.agents/skills/content-to-course/engine/assemble.py:206-210`, `frac_simple_fix` previously matched `r"(\\(?:frac|dfrac|tfrac|cfrac)\s*\{[^{}\\]+)\{([^{}]+\})"`. The character class `[^{}\\]+` failed to exclude `_` and `^`, resulting in regex breakage and corruption on LaTeX expressions such as `\frac{S_{xy}}{S_{xx}}` or `\frac{K^{0.5}}{L^{0.5}}`.
4. **Residual `corpus.md` and `section_*.md` Fallbacks Across Repo**:
   - In `.agents/skills/content-to-course/dispatch.py:240`: `ROLE_SPECS["cta-map"]["read"]` contained `"work/sections/section_*.md"`.
   - In `.agents/skills/content-to-course/dispatch.py:463, 543, 546, 556, 579`: multiple lines fell back to `f"{work_rel}/corpus.md"` and included it in subagent `read_paths`, causing `FileNotFoundError` in subagent Step 4 during runs 3, 4, 5, and 7.
   - In `.agents/skills/content-to-course/run.py:222, 271`: banner printed legacy extraction message and line 271 printed `print(f"  [+] Corpus file: {prep_res.get('corpus_path', self.work_dir / 'corpus.md')}")` to stdout.
   - In `.agents/skills/content-to-course/SKILL.md:92, 110, 180`: legacy references instructed reading `work/corpus.md`.
   - In `system_prompts/prompt_competence_analyser.md:10` and `system_prompts/prompt_cta_sectional.md:3, 10, 28`: legacy references to `corpus.md` and `section_XX.md`.
   - In `README.md:228` and `PROJECT.md:32`: references to `corpus.md` and `Corpus Slicing`.

## 2. Logic Chain
1. **Workspace Safety Guard**:
   - By creating `is_active_workspace(course_dir: Path, max_age_seconds: float = 24 * 3600)`, we explicitly check for the presence of state files (`work/state.json`, `work/pre_cta_manifest.json`, `work/cta_data.py`, or direct equivalents) and verify the modification timestamp of any file inside the directory. If state files exist OR any file was modified within the last 24 hours, `is_active_workspace` returns `True`.
   - In `clean_orphan_course_dirs`, `if is_active_workspace(d): continue` prevents any in-progress or recently touched workspace from ever being removed.
2. **Isolated Test Execution**:
   - `COURSES_DIR` is now initialized with `Path(os.environ.get("COURSES_DIR", REPO_ROOT / "courses"))` and dynamically resolved through `get_effective_courses_dir()`.
   - `assert_path_safe` allows operations within the effective `COURSES_DIR` override, permitting `tmp_path` to be used safely in test suites while continuing to strictly guard `content/` and `fixtures/`.
   - In `tests/test_delete_course.py`, `test_clean_orphan_dirs` is isolated using `tmp_path` and `monkeypatch`. It verifies that:
     - Workspaces containing active state files are preserved regardless of age.
     - Workspaces with files modified within 24h are preserved.
     - Only orphan directories older than 24h with no state files are cleaned.
     - The real repository `courses/` directory is verified completely untouched.
3. **LaTeX Fraction Regex Fix**:
   - Changing `frac_simple_fix` regex to `[^{}\\^_]+` prevents the simple fraction repair rule from erroneously firing across subscripts `_` or superscripts `^`, ensuring expressions like `\frac{S_{xy}}{S_{xx}}` and `\frac{K^{0.5}}{L^{0.5}}` remain pristine.
4. **Full Legacy Purge**:
   - Purged all `corpus.md` references in `dispatch.py`, raising `RuntimeError("BLOCKER:: ...")` if source files or slice paths are absent from `pre_cta_manifest.json`.
   - Updated `ROLE_SPECS["cta-map"]["read"]` to `"work/parts/part_*/**"` and `"work/parts/part_manifest_*.json"`.
   - Updated `run.py` banner to `Stage 0: Lossless source partitioning & pre_cta_manifest generation` and deleted line 271 stdout print.
   - Cleaned `SKILL.md`, `prompt_competence_analyser.md`, `prompt_cta_sectional.md`, `README.md`, and `PROJECT.md`.
   - Added automated tests in `tests/test_delete_course.py` validating that neither `corpus.md` nor `section_*.md` appear in dispatch code, generated dispatch items, prompts, or docs.

## 3. Caveats
- No caveats. The real `courses/` directory remains guarded, and all 24 targeted tests pass deterministically. The full pytest test suite (`python -m pytest tests -q`) was deliberately NOT run per the dispatch constraint ("strictly locked until Gate 0 passes independent audit").

## 4. Conclusion
Gate 0 Safety Foundation & Legacy Purge requirements are 100% implemented, verified, and ready for independent adversarial audit by `teamwork_preview_auditor`.

## 5. Verification Method
Execute the targeted pytest suite:
```powershell
$env:PATH = "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts;$env:PATH"
python -m pytest tests/test_delete_course.py -v
```
Or via the repo test runner wrapper:
```powershell
.\pytest.cmd tests/test_delete_course.py -q
```
Expected result:
```text
24 passed in 0.27s (100% pass rate)
```

Files to inspect:
- `.agents/skills/delete-course/scripts/delete_course.py`
- `tests/test_delete_course.py`
- `.agents/skills/content-to-course/engine/assemble.py`
- `.agents/skills/content-to-course/dispatch.py`
- `.agents/skills/content-to-course/run.py`
- `.agents/skills/content-to-course/SKILL.md`
- `.agents/skills/content-to-course/system_prompts/prompt_competence_analyser.md`
- `.agents/skills/content-to-course/system_prompts/prompt_cta_sectional.md`
- `README.md` and `PROJECT.md`
