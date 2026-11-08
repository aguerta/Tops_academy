# BRIEFING — Gate 3 Micro-Remediation (`gate3_fix`)

## 1. Mission & Boundary Context
- **Role**: `c2c40_implementer` (senior systems & formal verification engineer).
- **Execution Stream**: Gate 3 Micro-Remediation (`gate3_fix`), Flash Dyad Orchestrator.
- **Exclusive Write Boundary**:
  1. `.agents/skills/content-to-course/compile_shard.py`
  2. `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
  3. `.agents/skills/content-to-course/subagent_types.json`
  4. `.agents/teamwork/c2c_v40_formal_mas_con_menos/gate3_fix/BRIEFING.md`
  5. `.agents/teamwork/c2c_v40_formal_mas_con_menos/gate3_fix/handoff.md`

## 2. Invariants & Guardrails
- **Zero-Domain Guardrail**:
  No occurrences of `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi` in any `.py` file inside `.agents/skills/content-to-course/`.
  All new comments and docstrings in `.py` files must strictly be written in English.
- **Hook Guardrail**:
  Do not run forbidden commands matching hook patterns (`python ... run.py --help`, `dispatch.py --help`, or `python -c` inspecting skill files).
- **Console Encoding**:
  Safe UTF-8 / ASCII encoding on Windows `cp1252`.
- **Pure LF Formatting**:
  Both `lean/prompt_shard_author.md` and `subagent_types.json` must be strictly formatted with pure LF (`\n`, 0 `\r` bytes).
- **Size Constraints**:
  - `prompt_shard_author.md` (lean) <= 4,750 bytes.
  - `subagent_types.json` <= 18,432 bytes.

## 3. Surgical Fix Analysis

### Fix 1: Prompt Contract Alignment & Read Prohibition Parity
- **Target File**: `.agents/skills/content-to-course/system_prompts/lean/prompt_shard_author.md`
- **Line 4**:
  - *Current*: `- Turn-0 Autosufficiency: author_XX.json. READ/WRITE: shards/<shard_id>_data.py, shards/shard_fixes/<CID>.py.`
  - *Replacement*: `- Turn-0 Autosufficiency: author_XX.json. READ: shards/<shard_id>_data.py. WRITE: shards/<shard_id>_data.py, shards/shard_fixes/<CID>.py.`
  - *Reason*: `test_compile_shard_read_prohibition_parity` uses regex `r"READ:\s*(.*?)(?=\.\s*WRITE|\Z)"`. Having `READ/WRITE:` broke this match.
- **Line 9**:
  - Replace UTF-8 en-dashes `–` (`80–110`, `180–220`) with ASCII hyphens `-` (`80-110`, `180-220`) to keep byte length under 4,750 bytes.
- **Subagent Types Sync**:
  - Run `tests/test_c2c_v321_comp4_prompts.py` to auto-synchronize `subagent_types.json` with pure LF and assert `size <= 18,432 bytes`.

### Fix 2: Verifier Tautology Error Consolidation (Zero Weakening)
- **Target File**: `.agents/skills/content-to-course/compile_shard.py`
- **Line Ranges**:
  - ~Line 1806: Initialize `deferred_verifier_errors: List[str] = []` alongside `gen_callables_by_cid`.
  - ~Lines 2385–2446:
    Introduce `tautology_recorded = False` before `for test_seed in (42, 43, 44):`.
    In the distractor refutation dry run:
    Guard with `if isinstance(dists_test, list) and not tautology_recorded:`.
    When `refute_res is True`, instead of immediate `return _fail(...)`, append to `deferred_verifier_errors`:
    `deferred_verifier_errors.append(f"{cid}.json ({curr_p.name}): [VERIFIER-TAUTOLOGY-DETECTED] El verificador ver_fn '{ver_fn_name}' en '{tpl_id}' (Línea {line_no} en {curr_p.name}) retornó True para el distractor falso '{d_val}'. El verificador no refuta respuestas incorrectas (tautología).")`
    Set `tautology_recorded = True` and `break`.
  - ~Line 3231:
    Update error consolidation:
    ```python
    if deferred_verifier_errors or m3_errors:
        is_clean = False
        raw_errors = deferred_verifier_errors + m3_errors + list(raw_errors)
    ```
- **Rationale**:
  Preserves 100% formal verification rigor. Verifier tautologies remain fatal (setting `is_clean = False`), but deferral allows the compiler to run downstream linters (`check_templates` mono-key check `[TPL-STATIC-OPT]` and M3 magic multiplier check `[DIAG-MAGIC-MULT]`), unblocking `test_compile_shard_diagnoses_static_mono_key` and `test_compile_shard_diagnoses_magic_multipliers_without_ans_variable`.

## 4. Test Verification Plan
Run single-process pytest across all impacted test suites:
- `tests/test_prompts_contract_alignment.py`
- `tests/test_c2c_straggler_and_postproduction_prevention.py`
- `tests/test_c2c_v321_comp4_prompts.py`
- `tests/test_dispatch_turn0_and_milestone3_prompts.py`
- `tests/test_compile_shard.py`
- `tests/test_shard_compiler_hardening.py`
- `tests/test_system_prompts_compile_clean.py`
- `tests/test_c2c_v40_formal_certification.py`
- `tests/test_skill.py`
