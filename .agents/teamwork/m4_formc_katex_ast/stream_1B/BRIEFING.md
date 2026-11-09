# BRIEFING — STREAM 1B (Milestone 4: `compile_shard.py` & `shard_precheck.py`)

## 1. Baseline Findings & Architecture Overview

### A. How `compile_shard.py` processes `TEMPLATES`
- **Loading & Fix-Splicing (lines ~1697–1780)**:
  `compile_shard.py` dynamically imports or executes the shard file (or uses fixes from `shards/shard_fixes/<CID>.py`). It retrieves `TEMPLATES = getattr(mod, "TEMPLATES", None)` and wraps entries in `tuple_records` with references to `file_path`, `locator`, and `orig_idx`.
  In fix files, it inspects each record in `tuple_records`, extracting `t_cid` to replace existing records when a match with `cid_fix` is found.
- **Competency Parity & Format Detection (lines ~1793–1856)**:
  `compile_shard.py` loops over `tuple_records`:
  * If `isinstance(t, dict)` (Form-C), it reads `t.get("cid")` or `t.get("competency_id")`.
  * If `isinstance(t, (list, tuple))` (Form-B), it enforces length == 9 and extracts `t[1]` as candidate CID.
  * If neither, it fails compilation.
- **Main Compilation Loop (lines ~1880–2000+)**:
  It extracts template fields:
  * Form-C dict: extracts `id`/`tpl_id`, `cid`/`competency_id`, `qtype`, `gen`/`generator_code`, `ver`/`verifier_code`, `band`/`difficulty_bloom`, `stems`/`stem_variants`, `hints`, `sol`/`solution`, `archetype`, `assumption_id`, `fmt`, `rats`.
  * Form-B 9-tuple: extracts indexed fields (0 to 8).
  It then builds canonical question objects, normalizes codes via `extract_function_code`, and handles MC7 option generation with `build_adapted_mc7_generator`.

### B. `extract_function_code`
- Takes `fn_or_str`, `target_name`, optional `locator`, `fn_name_hint`, `include_preamble`.
- Obtains source via `locator.function_segments`, `locator.functions`, or `inspect.getsource`.
- Transforms lambda assignments or expressions into standard `def <target_name>(...)` functions.
- Renames the root function to `target_name`.
- Injects aliases: `generate = generate_params` or `cross_check = verify`.
- Injects pruned preamble (dependencies/imports/helpers) if `include_preamble and locator`.

### C. `build_adapted_mc7_generator`
- Wraps an MC7 generator (`generate_params`) so that outputs are guaranteed to be `{ "vars": ..., "correct": ..., "distractors": ..., "options": [...] }`.
- Applies option string formatting `fmt` if specified (`fmt.replace("@X@", s)`).
- Normalizes distractors using `rats_map` or CTA declared distractors.
- Ensures strict 3-tuple format for distractors in strict mode: `(did, val, rationale)`.

### D. `pykatex_warnings`
- Inspects math spans (`$$...$$` or `$...$`, or whole string if `whole_is_math`).
- Normalizes variables: replaces `@var@` tokens with `1` before testing render.
- Calls `_pykatex.renderToString(probe, display)`.
- Catches errors and formats them as `[!] Warning: [PYKATEX-WARN] {context}: {msg} (span: {span[:60]!r})`.
- Currently does not extract the exact column number (`[col=N]`) from the error message.

### E. `shard_precheck.py`
- Fast AST-only single-pass static checker (< 50 ms).
- Inspects AST nodes for high-frequency mistakes:
  * `while` in `gen_*` (`[TPL-AD-HOC-PERTURBATION]`).
  * `raise` in `ver_*` (`[TPL-DEBUG-ARTIFACT]`).
  * Arity mismatch in `ver_*` (`[VER-SIGNATURE]`).
  * Alias assignment of verifiers (`[NO-GLOBAL-ALIAS]`).
  * Non-dynamic `RATS` (`[TPL-DYNAMIC-RATIONALE]`).
  * Non-raw strings with unescaped control chars (`[LATEX-RAW-STRING]`).
- All findings are warnings only and never change the compile verdict.

## 2. Plan of Modifications
1. Support `ShardCompetenceContract` (Pydantic M4.1) by converting any object with `to_form_c_dict()` or `model_dump()` to Form-C dict when reading `TEMPLATES` in `compile_shard.py`.
2. Implement AST auto-export of `vars` (`inject_ast_auto_vars`) in `compile_shard.py` and wrap/recompile in-memory `gen_raw` so both AST code string and runtime callable export `vars` automatically if omitted.
3. Enhance `pykatex_warnings` to report exact error column `[col=N]` from PyKaTeX exceptions.
4. Add `[SYMPY-LATEX-MATRIX]` and `[KATEX-AST-CHECK]` static AST checks in `shard_precheck.py`.
5. Run full test verification.
