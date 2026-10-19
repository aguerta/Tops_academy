# Dispatch: Gate 1 Stream A (CTA Architecture & Ingest Worker)

## Identity
- Role: Stream A Implementation Worker (CTA Architecture & Ingest)
- Type: teamwork_preview_worker
- Working Directory: d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_stream_a/
- Parent Conversation ID: e831bfe5-b034-48b8-9c7e-f1ebfdfd3200

## Scope & Requirements
1. **R3 (P2 CTA Zero-Micro-Edit Architecture & Patch Ledger)**:
   - Re-architect CTA generation:
     - Atomic creation via single `write_to_file` using raw strings (`r"..."`).
     - Limit architect edits to <= 1 repair turn, <= 3 total file edits, <= 2 compile cycles.
     - Update `prompt_cta_architect.md` and `dispatch.py` to instruct atomic single-call write and remove prohibition on overwrite.
     - Embed compact validator rules (<= 2.5 KB) in item dispatch and forbid reading `compile_cta.py` or `check_cta.py`.
   - Layered automated healing in `compile_cta.py`:
     - L1: Pre-import LaTeX tokenization and raw-string conversion (`heal_cta_source_file`), control-char healing, atomic write back with `.bak`.
     - L2: Deterministic KaTeX syntax repair (`sanitize_competency_math`): odd `$` closed at field end, `$$` inside single line -> `$`, bare macros (`\alpha`, `\hat{..}`, `\frac{..}{..}`, `\dot{..}`) wrapped in `$..$`, `{{x}}` -> `{x}`, write back to source file, log to `work/telemetry/cta_sanitizer_log.json`.
     - L3: Evidence page normalization and heading snapping (`auto_normalize_page_numbers`): detect printed-to-PDF offset, snap to valid page by token overlap, log warning `EV-SNAPPED`, deterministic `work/pages_index.md`.
     - L4: Consolidated repair pack: remove 2-snippet, 5-ID, 8-group throttles in `render_compact_cta_errors`. Emit all remaining errors at once grouped by competency with exact lines and suggested replacements. Write `work/cta_repair_pack.json`. Splicing override files (`cta_fixes/<ID>.py`).
     - L5: Degrade-and-flag: wrap unresolvable math in `\text{}` or snap evidence to nearest valid page after 1 repair cycle.
   - Patch Ledger (`patch_ledger.py`):
     - `record_patch(stage, layer, rule_id, scope, before, after, severity, reason)`.
     - Per run: `work/telemetry/patch_ledger.json` (`healed`, `snapped`, `degraded`).
     - Human view: `work/cta_review.md`.
     - Across runs: append to `reports/c2c_patches/patch_ledger.jsonl`.
     - Alert if degraded fields exceed 3%.
   - Add unit tests in `tests/test_cta_healing.py`.
2. **R4 (P3 Lossless MapReduce Partitioning & Slicing)**:
   - Create `partition_corpus.py`:
     - Weight-balanced sequential partitioning based strictly on PDF structural weights (content stream size, vector strokes, ink/image density) without text extraction.
     - Split whole corpus as one ordered sequence of page units into K contiguous ranges (K = clamp(round(total_weight / W), 2, 4)).
     - Physical slicing using `pymupdf` `select()` + `save()` into lossless sub-PDFs (`work/parts/part_NN/`). Fallback to `insert_pdf` only if needed.
     - Image sources: split into tiles by cropping original pixels without re-encoding to JPEG.
     - `.tex` sources: split at `\section` boundaries.
     - Localized slice page indexing (pages 1..n) in `part_manifest_NN.json` and remapped to global coordinates in `cta_merge.py`.
     - 1 page of read-only context before each slice.
     - Independent part compilation (`check_cta.py --part`).

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## 2026-10-19T04:22:02Z
You are the Stream A Implementation Worker (CTA Architecture & Ingest).
Your working directory is: d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_stream_a/

You MUST read and follow:
1. d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/ORIGINAL_REQUEST.md (under header ## 2026-10-19T03:49:57Z)
2. d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/worker_stream_a/DISPATCH.md
3. d:/Augusto/Downloads/c2c_hardening_plan.md (§5 P2 and P3)
4. d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/master_forensic_synthesis_7_runs.md (§3.2)

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Your write boundaries:
- .agents/skills/content-to-course/compile_cta.py
- .agents/skills/content-to-course/check_cta.py
- .agents/skills/content-to-course/cta_merge.py
- .agents/skills/content-to-course/partition_corpus.py (NEW)
- .agents/skills/content-to-course/patch_ledger.py (NEW)
- .agents/skills/content-to-course/system_prompts/prompt_cta_architect.md
- tests/test_cta_healing.py (NEW)

Key Objectives:
1. R3 (P2 CTA Zero-Micro-Edit Architecture & Patch Ledger):
   - Atomic creation via single write_to_file using raw strings (r"..."). Update prompt_cta_architect.md to enforce writing whole part in ONE write_to_file and forbid incremental construction.
   - Limit architect edits: <= 1 repair turn, <= 3 total file edits, <= 2 compile cycles.
   - Layered automated healing:
     * L1: Pre-import LaTeX tokenization & raw-string conversion (heal_cta_source_file), control char healing, atomic write back with .bak.
     * L2: Semantic healing (sanitize_competency_math): odd $ closed, $$ inside single line -> $, bare macros (\alpha, \hat{..}, \frac{..}{..}, \dot{..}) wrapped in $..$, {{x}} -> {x}, write back to source file, log to work/telemetry/cta_sanitizer_log.json.
     * L3: Evidence page normalization & heading snapping (auto_normalize_page_numbers): detect printed-to-PDF offset, snap to valid page by token overlap, log warning EV-SNAPPED, deterministic work/pages_index.md.
     * L4: Consolidated repair pack: remove 2-snippet, 5-ID, 8-group throttles in render_compact_cta_errors. Emit all remaining errors at once grouped by competency with exact line and suggested replacement. Write work/cta_repair_pack.json. Support splicing override files (cta_fixes/<ID>.py).
     * L5: Degrade-and-flag: wrap unresolvable math in \text{} or snap evidence to nearest valid page after 1 repair cycle.
   - Patch Ledger (patch_ledger.py):
     * record_patch(stage, layer, rule_id, scope, before, after, severity, reason).
     * Per run: work/telemetry/patch_ledger.json (healed, snapped, degraded).
     * Human view: work/cta_review.md.
     * Across runs: reports/c2c_patches/patch_ledger.jsonl (append-only).
     * Alert if degraded fields exceed 3%.
   - Add unit tests in tests/test_cta_healing.py reproducing real failures (\p escapes, 20 missing $, out-of-range pages, $$ in single line, degrade step produces valid KaTeX).
2. R4 (P3 Lossless MapReduce Partitioning & Slicing):
   - Implement partition_corpus.py:
     * Weight-balanced sequential partitioning based strictly on PDF structural weights (content stream size, vector strokes, ink/image density) without text extraction.
     * Sequential page units partitioned into K contiguous ranges (K = clamp(round(total_weight / W), 2, 4)). Snapped to PDF bookmarks (get_toc()) within ±10% when available.
     * Physical slicing using pymupdf select() + save() into lossless sub-PDFs (work/parts/part_NN/). Preserving vector ink and original typography.
     * Image sources: split into tiles by cropping original pixels without re-encoding to JPEG.
     * .tex sources: split at \section boundaries.
     * Local slice page indexing (pages 1..n) in part_manifest_NN.json, remapped to global coordinates in cta_merge.py.
     * 1 page read-only context before each slice.
     * Independent part compilation (check_cta.py --part).

Targeted test execution:
Run: python -m pytest tests/test_cta_healing.py -v
Ensure all tests pass. Write handoff.md and send_message to parent orchestrator.
