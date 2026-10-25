# DISPATCH: Stream 3A — Final Integration Improver (`impr_3a`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory (Governance Docs):** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_3a_impr`
- **Implementer Handoff to Review:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_3a_impl/handoff.md`
- **Exclusive Production/Test/Report Write Boundaries:**
  1. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/subagent_types.json`
  2. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_forensic_replay_ab30cf91.py`
  3. `d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/CERTIFICACION_HARDENING_C2C_V33.md`
  4. `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/check_templates.py` *(lines 2066–2086 only, if needed)*
  5. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_c2c_solow2_architectural_improvements.py`
  6. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_c2c_v321_multi_instance_and_append.py`
  7. `d:/Augusto/personal_portfolio/Tops_academy/tests/test_engine_invariants_adversarial.py`

> **CRITICAL RULES:**
> - **DO NOT** create `.agents/hooks.json` yet!
> - **DO NOT** leave any `.c2c_subagent_lock.json` file inside `REPO_ROOT` (`courses/*` or `work*/`).
> - **NEVER** pass `ArtifactMetadata` when calling `write_file` or `edit_file`.

## High-Value Adversarial Polish Checklist

1. **Verify Real Greene PDFs Execution in `V1` (`test_forensic_replay_ab30cf91.py`):**
   - Check the actual paths of the Greene PDFs inside `d:/Augusto/personal_portfolio/Tops_academy/content/` (and/or `courses/asyntotic_estatistics_v2.json` source docs) to confirm `test_v1_bootstrap_zero_raster_multi_pdf_and_stdout_cap` finds the **real** Greene PDFs on disk and executes `bootstrap` against them (zero `pytest.skip` triggered in `test_forensic_replay_ab30cf91.py`!). Also test `format_compact_json_stdout` under extreme multi-part workloads (e.g. 25 subparts) to confirm `len(out.encode("utf-8")) <= 1500` AND `json.loads(out)` succeeds.
2. **Verify Actual `[CIRCUIT BREAKER]` Trip in `V6` & Single-Letter Econometrics Vars (`z`, `w`, `u`, `d`, `k`, `n`) in `V5`:**
   - In `V6`: Confirm `test_v6` asserts the compiler explicitly halts with `[CIRCUIT BREAKER]` on the 3rd distinct edit producing the same normalized `err_hash`, AND resets cleanly once fixed via `shard_fixes/C-08.py`.
   - In `V5`: Include `z`, `w`, `u`, `d`, `k`, `n` alongside `\mu`, `\sigma^2`, `\xrightarrow{d}`, `Q_{zx}^{-1}`, `\mathbb{R}^{k}` in the valid template (0 false positives) AND confirm both `{delta}` AND `@delta@` unrendered leaks are hard-blocked before Stage 5.
3. **Verify `subagent_types.json` Exact Sync (`dispatch.py`):**
   - Assert programmatically inside `test_forensic_replay_ab30cf91.py` (or a dedicated assertion in V1/V7) that `.agents/skills/content-to-course/subagent_types.json` on disk is 100% synchronized with `system_prompts/*.md` (contains `@var@`, `shard_fixes`, `ArtifactMetadata` prohibition, coherent Blind Judge pointer mode, and `compile_shard.py` read prohibition).
4. **Accuracy Polish in `reports/c2c_audits/CERTIFICACION_HARDENING_C2C_V33.md`:**
   - Fix Row `#12` (around line 101): clarify that `granularity: standard` is **relative page density (`3–5` competencias por cada `5–10` páginas densas)** rather than a fixed `60–70` cap, combined with Milestone 7.4 `1 Hab/shard` weighted isolation.
   - Fix Cat `06` (around line 115): clarify `R-16` engine invariant range `[0.65x, 1.35x]` (with author target `[0.80x, 1.20x]`) and zero artificial filler in `calibrate_option_lengths`.
   - Update exact final `pytest` counts and runtime in `CERTIFICACION_HARDENING_C2C_V33.md` if you add assertions/tests.

Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_forensic_replay_ab30cf91.py -v` (`< 10s`) AND `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests -q` (`0 failed`), verify 0 `.c2c_subagent_lock.json` files in `REPO_ROOT`, write `BRIEFING.md`, `progress.md`, and `handoff.md` in `stream_3a_impr/`, and `send_message` `DONE:: stream_3a_impr | ...` to `d0ce22db-904e-4856-b353-59975bfb5874`.
