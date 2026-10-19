# Master Execution Plan: C2C Hardening

## Overview
This plan implements the complete hardening of the Top's Academy Content-to-Course (C2C) multi-agent pipeline targeting reliable, unattended course generation in ≤ 20 minutes per run, eliminating micro-edit loops, straggler token burn, Director emission latency, and enforcing strict data safety.

## Safety & Concurrency Architecture

### Gate 0 (Sequential Foundation — Safety Lock)
*Strictly sequential prerequisite. NO other streams or full pytest test runs may execute until Gate 0 achieves an independent Auditor PASS.*
- **Scope**: Requirement 1 (P0 Data Safety, Legacy Artifact Purge, assemble.py fix)
- **Target Files Owned**:
  - `delete_course.py` (inside delete-course skill)
  - `tests/test_delete_course.py`
  - `assemble.py` (2-line `frac_simple_fix`)
  - Purge of `corpus.md` / `section_*.md` in:
    - `.agents/skills/content-to-course/dispatch.py`
    - `.agents/skills/content-to-course/run.py`
    - `.agents/skills/content-to-course/SKILL.md`
    - `.agents/skills/content-to-course/system_prompts/prompt_competence_analyser.md`
    - `.agents/skills/content-to-course/system_prompts/prompt_cta_sectional.md`
    - `README.md`
    - `PROJECT.md`
- **Verification Commands**:
  - `python -m pytest tests/test_delete_course.py -q`
  - Automated check asserting zero stdout occurrences of `corpus.md` / `section_*.md` during prepare or inside `work/dispatch/**`.
- **Gate 0 Exit Criteria**: Independent Forensic Auditor sign-off (PASS) certifying data safety isolation and complete legacy artifact purge.

---

### Gate 1 (Concurrent Parallel Implementation Streams)
*Unlocked only after Gate 0 PASS is certified.*

#### Stream A: CTA Architecture & Ingest
- **Requirements**:
  - R3 (P2 CTA Zero-Micro-Edit, L0-L5 Layered Healing, `patch_ledger.py`, `cta_review.md`, alert >3% degraded)
  - R4 (P3 Lossless MapReduce Partitioning & Slicing, `partition_corpus.py`, `cta_merge.py`, `pymupdf` `select()`+`save()`, local slice coordinates)
- **Target Files Owned**:
  - `.agents/skills/content-to-course/compile_cta.py`
  - `.agents/skills/content-to-course/check_cta.py`
  - `.agents/skills/content-to-course/cta_merge.py`
  - `.agents/skills/content-to-course/partition_corpus.py` (NEW)
  - `.agents/skills/content-to-course/patch_ledger.py` (NEW)
  - `.agents/skills/content-to-course/system_prompts/prompt_cta_architect.md`
  - `tests/test_cta_healing.py` (NEW)
- **Independent Audit & Review**: Adversarial review, edge-case stress (corrupted math, dense ink, bookmarks), verification of single atomic write.

#### Stream B: Template Engine & Author Pipeline
- **Requirements**:
  - R2 (P1 Stage 3 Diagnostics, Tool Isolation, SHA-256 Circuit Breakers, `_format_dry_failure`, missing file handling, canonical author prompt)
  - R6.1 (P5 Author Adaptive Sizing `clamp(ceil(N / 8), 2, 6)`, syntax normalization `{{token}}` -> `{token}`, parameter space >= 500)
- **Target Files Owned**:
  - `.agents/skills/content-to-course/check_templates.py`
  - `.agents/skills/content-to-course/compile_shard.py`
  - `.agents/skills/content-to-course/plan_shards.py`
  - `.agents/skills/content-to-course/engine/assemble.py` (syntax normalization)
  - `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
  - `tests/test_latex_engine.py` (NEW)
  - `tests/test_compile_shard.py`
- **Independent Audit & Review**: Adversarial review of circuit breaker state transitions, diagnostic formatting, and template scaling bounds.

#### Stream C: Orchestration, Watchdog & Evaluation
- **Requirements**:
  - R5 (P4 Director Pointer Prompts <=300B, static system prompts <=5KB, Swift-Dispatch SLA <=20s, pre-Stage 5 cleanup `kill_all`, watchdog `budget_guard.py`, stateful resume in `work/state.json`)
  - R6.2 (P6 Judge Native Batching <=12 items per batch `judge_batch_NN.json`, incomplete detection, blind re-dispatch)
- **Target Files Owned**:
  - `.agents/skills/content-to-course/dispatch.py` (pointer prompts, judge splitting, SLAs)
  - `.agents/skills/content-to-course/judge.py`
  - `.agents/skills/content-to-course/budget_guard.py` (NEW)
  - `.agents/skills/content-to-course/system_prompts/` (lean prompt refactor)
- **Independent Audit & Review**: Verification of judge blindness (no ground truth in item files), watchdog thresholds (40 turns, 5M tokens), and stateful recovery.

#### Stream D: Environment, Append & Documentation
- **Requirements**:
  - R7 (P7 Append Workflow delta generation with continuous ID sequences, Unicode resilience for PowerShell titles, path quoting sanitation)
  - P8 (Documentation v3.22 update in SKILL.md, architectural diagrams, failure taxonomies, watchdog procedures)
- **Target Files Owned**:
  - `.agents/skills/content-to-course/prepare.py` / `run.py` (append delta & title parsing)
  - `.agents/skills/content-to-course/course_publisher.py`
  - `.agents/skills/content-to-course/SKILL.md` (v3.22 update)
- **Independent Audit & Review**: Unicode stress testing, Windows path escaping checks, ID sequence collision testing.

---

### Gate 2 (Integration & End-to-End Benchmark)
*Unlocked when all Gate 1 streams achieve individual auditor PASS.*
- **Step 1**: Merging and stream reconciliation.
- **Step 2**: Full repository regression test suite execution: `python -m pytest tests -q`.
- **Step 3**: Dedicated MapReduce P3.0 spike against `solow_model` corpus.
- **Step 4**: Full acceptance criteria verification (AC table in ORIGINAL_REQUEST.md).

---

### Requirement 8: Independent Adversarial Audit & Iterative Repair Loop
- Completely separate forensic auditor dispatched for each stream / requirement.
- Zero-tolerance anti-cheating verification: NO mocks, NO hardcoded bypasses, NO weakened assertions.
- In case of failure / critique, an iterative review-fix loop immediately executes until a formal PASS certification is stamped.
- Final victory claim sent to caller only when ALL requirements R1-R7 and Gate 2 pass 100%.
