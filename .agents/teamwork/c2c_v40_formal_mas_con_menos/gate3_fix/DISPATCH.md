# DISPATCH — Gate 3 Micro-Remediation (`gate3_fix`)

## 1. Exclusive Write Boundary
1. `.agents/skills/content-to-course/compile_shard.py`
2. `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
3. `.agents/skills/content-to-course/subagent_types.json`
4. `.agents/teamwork/c2c_v40_formal_mas_con_menos/gate3_fix/handoff.md` `[NEW]`

*(Do NOT modify any test files or other production files. Also restore any modified/untracked `reports/qa_audits/*_payload.json` if dirty in `git status --short` via `git checkout -- reports/qa_audits/` or removing untracked `*_payload.json` created during audit).*

## 2. Exact Root Causes & Surgical Fixes (3/1,389 tests)

### Fix #1 — `tests/test_prompts_contract_alignment.py::test_compile_shard_read_prohibition_parity`
- **Root Cause**: Line 4 of `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md` currently says:
  `- Turn-0 Autosufficiency: author_XX.json. READ/WRITE: shards/<shard_id>_data.py, shards/shard_fixes/<CID>.py.`
  Because `READ` and `WRITE` were merged as `READ/WRITE:`, `re.search(r"READ:\s*(.*?)(?=\.\s*WRITE|\Z)", content, re.IGNORECASE)` fails to match!
- **Surgical Fix**:
  1. Change line 4 of `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md` to:
     `- Turn-0 Autosufficiency: author_XX.json. READ: shards/<shard_id>_data.py. WRITE: shards/<shard_id>_data.py, shards/shard_fixes/<CID>.py.`
     (And on line 9, replace the two UTF-8 en-dashes `–` in `80–110` and `180–220` with ASCII `-` so total file size stays `~4,740 bytes <= 4,750 bytes`).
  2. Ensure `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md` is written in **pure LF (`\n`, 0 `\r` bytes)** (`[System.IO.File]::WriteAllBytes(..., [System.Text.UTF8Encoding]::new($false).GetBytes($text))`).
  3. Run `tests/test_c2c_v321_comp4_prompts.py` to sync `.agents/skills/content-to-course/subagent_types.json`, then strip any `\r` from `.agents/skills/content-to-course/subagent_types.json` so `subagent_types.json` ALSO has `0` `\r` bytes (`<= 18,432` bytes).

### Fix #2 — `tests/test_c2c_straggler_and_postproduction_prevention.py` (`test_compile_shard_diagnoses_static_mono_key` & `test_compile_shard_diagnoses_magic_multipliers_without_ans_variable`)
- **Root Cause**: In `.agents/skills/content-to-course/compile_shard.py` around line `2442`, `[VERIFIER-TAUTOLOGY-DETECTED]` immediately calls `return _fail(...)` inside the per-tuple loop before reaching `check_templates_file_or_dir` (`[TPL-STATIC-OPT]`) and `m3_errors` (`[DIAG-MAGIC-MULT]` / `[TPL-STATIC-OPT]`). Both legacy tests intentionally use simplified verifiers while testing `[TPL-STATIC-OPT]` (`mono-clave`) and `[DIAG-MAGIC-MULT]`.
- **Surgical Fix (Zero Weakening — Consolidated Error Reporting)**:
  1. Around line `1806` (next to `gen_callables_by_cid: Dict[str, List[Any]] = {}`), initialize:
     `deferred_verifier_errors: List[str] = []`
  2. Around lines `2385-2446`, introduce `tautology_recorded = False` before `for test_seed in (42, 43, 44):`, guard `if isinstance(dists_test, list) and not tautology_recorded:`, and when `refute_res is True`, instead of `return _fail(...)`, append to `deferred_verifier_errors` and set `tautology_recorded = True; break`:
     ```python
     if refute_res is True:
         line_no = _find_diagnostic_line(curr_loc, ver_fn_name, orig_idx, d_val)
         deferred_verifier_errors.append(
             f"{cid}.json ({curr_p.name}): [VERIFIER-TAUTOLOGY-DETECTED] El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) "
             f"retornó True para el distractor falso '{d_val}'. El verificador no refuta respuestas incorrectas (tautología)."
         )
         tautology_recorded = True
         break
     ```
  3. Around line `3231` (where `if m3_errors:` sets `is_clean = False`), include `deferred_verifier_errors` so `compile_shard` ALWAYS fails if ANY tautology, `m3_errors`, or `check_templates` error occurred, consolidating all diagnostics into `raw_errors`:
     ```python
     if deferred_verifier_errors or m3_errors:
         is_clean = False
         raw_errors = deferred_verifier_errors + m3_errors + list(raw_errors)
     ```
  4. Keep all Python comments in English (`zero_domain` invariant).

## 3. Mandatory Verification
Run single-process pytest on all affected suites:
```powershell
& ".venv\Scripts\python.exe" -m pytest -o addopts="" tests/test_prompts_contract_alignment.py tests/test_c2c_straggler_and_postproduction_prevention.py tests/test_c2c_v321_comp4_prompts.py tests/test_dispatch_turn0_and_milestone3_prompts.py tests/test_compile_shard.py tests/test_shard_compiler_hardening.py tests/test_system_prompts_compile_clean.py tests/test_c2c_v40_formal_certification.py tests/test_skill.py -q
```
Verify byte counts and pure LF (`cr=0`) on both `lean/prompt_shard_author.md` (`<= 4,750 B`) and `subagent_types.json` (`<= 18,432 B`), write `.agents/teamwork/c2c_v40_formal_mas_con_menos/gate3_fix/handoff.md`, and send `DONE:: Gate 3 Fix`.
