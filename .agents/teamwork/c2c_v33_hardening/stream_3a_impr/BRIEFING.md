# BRIEFING: Stream 3A Pre-Flight & Architectural Scrutiny (Phase 2: Mejorador)

**Role:** Stream 3A Improver (`impr_3a`)  
**Date:** 2026-10-24  
**Workspace:** `d:/Augusto/personal_portfolio/Tops_academy`  
**Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_3a_impr`  

---

## 1. Implementer Review & Fulfillment Audit

We reviewed `stream_3a_impl/handoff.md`, `stream_3a_impl/BRIEFING.md`, and all changes in the write boundary:
- **Baseline Test Suite**: 724 passed, 2 skipped, 0 failed in 83.54s.
- **Forensic Suite**: `tests/test_forensic_replay_ab30cf91.py` contains 8 non-mocked vector tests (`V1..V8`) passing in 2.60s (< 10s SLA).
- **Subagent Types**: `.agents/skills/content-to-course/subagent_types.json` was regenerated with `dispatch.get_type_definitions(lean=False)` (90,479 bytes), matching in-memory specifications.
- **Security & Hygiene**: Zero `.c2c_subagent_lock.json` files exist in `REPO_ROOT`; `.agents/hooks.json` has NOT been created (preserving orchestrator post-audit activation).

## 2. Hardening Plan & Adversarial Scrutiny

In accordance with `DISPATCH.md`, we identify 4 high-value areas to harden:

1. **V1 Real Greene PDFs & Extreme Stdout Capping Polish:**
   - In `test_v1_bootstrap_zero_raster_multi_pdf_and_stdout_cap`: replace `if len(greene_pdfs) < 2: pytest.skip(...)` with a hard assertion `assert len(greene_pdfs) >= 2` to guarantee zero `pytest.skip` is ever triggered during replay.
   - Verify that the ingested files match the real Greene chapters (`5th ed ... -93.pdf` and `Econometric Analysis ... -923-946.pdf`) referenced in forensic run `ab30cf91`.
   - Add an adversarial check testing `format_compact_json_stdout` under extreme multi-part workloads (e.g. 25-50 subparts) to assert `len(out.encode("utf-8")) <= 1500` and `json.loads(out)` succeeds deterministically.

2. **V5 Econometric Single-Letter Math Variables & Dual Unrendered Token Leaks:**
   - Expand the valid template in `test_v5` to include single-letter econometrics variables `$z$`, `$w$`, `$u$`, `$d$`, `$k$`, `$n$` alongside `\mu`, `\sigma^2`, `\xrightarrow{d}`, `Q_{zx}^{-1}`, `\mathbb{R}^{k}`, ensuring zero false positives across 50 dry-run seeds.
   - Expand unrendered leak tests to explicitly verify that BOTH `{delta}` and `@delta@` unrendered leaks are hard-blocked with clear diagnostics before Stage 5.

3. **V6 Explicit Circuit Breaker Halt & Clean Reset via `shard_fixes`:**
   - Harden `test_v6` to explicitly test that on the 3rd distinct edit producing the same normalized `err_hash`, `compile_shard` returns `[CIRCUIT BREAKER]` and records `same_error_streak == 3`.
   - Test that subsequently creating `shard_fixes/C-08.py` compiles cleanly (`ok is True`, `errs == []`) and unlinks the state file `.check_attempts/compile_shard_08.json` (clean reset).

4. **Programmatic Catalog Synchronization Verification:**
   - Add an explicit programmatic test asserting `subagent_types.json` on disk matches `dispatch.get_type_definitions(lean=False)` and contains all required contracts: `@var@`, `shard_fixes`, `ArtifactMetadata` prohibition, coherent Blind Judge pointer mode, and `compile_shard.py` worker read prohibition.

5. **Certification Report Precision:**
   - Fix Row `#12` in `reports/c2c_audits/CERTIFICACION_HARDENING_C2C_V33.md` regarding relative page density (`3–5` competencias por cada `5–10` páginas densas).
   - Fix Cat `06` regarding `R-16` invariant range `[0.65x, 1.35x]` (author target `[0.80x, 1.20x]`) and zero artificial filler.
   - Update final pytest counts and runtimes.
