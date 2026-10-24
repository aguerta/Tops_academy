# BRIEFING: Stream 1E Improver Pre-Flight Scrutiny & Blocker Analysis

**Date:** 2026-10-24  
**Role:** Phase 2 Improver (`stream_1e_impr`)  
**Target:** Stream 1E (Zero-Raster PDF Ingest, Multi-PDF Sources Fix, PATCH_LEDGER_ALERT Calibration & End-to-End `--append` CTA)  
**Status:** BLOCKER IDENTIFIED (Requires Orchestrator Authorization for `check_cta.py`)

---

## 1. Pre-Flight Verification of Implementer's Deliverables

We audited all changes introduced by `stream_1e_impl`:
1. `ingest.py`:
   - `render_pages` flag added with default `True` for backward-compatible unit tests, configurable in CLI (`--render-pages`/`--no-render-pages`).
   - `input_files` parameter added to bypass directory walking and isolate exact target files.
   - PDF rasterization skipped when `render_pages=False`.
2. `prepare.py`:
   - Bug where `input_target = sources[0].parent` when multiple sources were passed is eliminated; `input_files=sources` passed directly.
   - `existing_competencies_outline` injected into `manifest["delta"]` for downstream LLM prompts.
3. `cta_merge.py`:
   - Regex 5b upgraded to match repeated sub/superscripts (`Q_{zx}^{-1}`).
   - Lossless normalizations recorded with `severity="healed"` under rule `NORMALIZE_ORPHAN_MATH`.
   - `merge_cta_parts` respects `delta_info` offsets (`next_H`, `next_C`, `next_Hab`).
   - `apply_harmonize` checks DAG with base competencies included and filters out base prereq false positives.
4. `compile_cta.py`:
   - Evaluated fields counted across all fields (`count_evaluated_fields`), properly calibrating denominator for `PATCH_LEDGER_ALERT`.
   - Base prerequisites filtered out of validation errors.
5. `tests/test_fast_ingest_and_cta_append.py`:
   - 8 comprehensive tests passing in 0.48s.

---

## 2. Architectural Blocker: `check_cta.py` Downstream `--append` Validation

### 2.1 Location
- File: `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/check_cta.py` (lines 170-184, 689-692)
- Caller: `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/run.py` (line 446)

### 2.2 Conflict & Root Cause
In `run.py` (`run_stage_cta`, line 446):
```python
is_valid, errors = check_cta_file(cta_data, manifest_data=manifest_data, file_path=cta_file) if check_cta_file else validate_cta_rules(cta_data, manifest_data=manifest_data, file_path=cta_file)
if not is_valid:
    raise ValueError(f"cta.json contains {len(errors)} validation errors.")
```
In `check_cta.py`, `validate_cta_rules` delegates DAG acyclicity check to `check_prerequisites_dag`:
```python
dag_errors = check_prerequisites_dag(competencies)
errors.extend(dag_errors)
```
Inside `check_prerequisites_dag`:
```python
comp_ids = {c["id"] for c in competencies}
for comp in competencies:
    cid = comp["id"]
    for prereq in comp.get("prerequisites", []):
        if prereq not in comp_ids:
            errors.append(f"Competency '{cid}' references non-existent prerequisite '{prereq}'.")
```
Notice:
1. `check_cta.py` does NOT check `manifest_data.get("delta")` or `manifest_data.get("existing_course")` for `existing_competency_ids`.
2. When `--append` produces a delta competency (e.g., `C-05`) whose pedagogical prerequisite is an existing base competency (e.g., `C-01`), `check_cta.py` rejects it with:
   `Competency 'C-05' references non-existent prerequisite 'C-01'.`
3. As a consequence, while `compile_cta.py` and `cta_merge.py` implemented local regex workarounds to pass their internal validations, when `run.py` runs Stage 01 (`run_stage_cta`), it executes `check_cta_file` directly and aborts with `ValueError: cta.json contains 1 validation errors.`!
4. Furthermore, running `python check_cta.py cta.json --manifest pre_cta_manifest.json` from the CLI on an appended course will fail.

### 2.3 Proposed Clean Fix (4 lines in `check_cta.py`)
```python
# 1. In check_prerequisites_dag:
def check_prerequisites_dag(competencies: List[Dict[str, Any]], allowed_prereq_ids: Optional[Set[str]] = None) -> List[str]:
    errors = []
    comp_ids = {c["id"] for c in competencies}
    valid_ids = comp_ids | (allowed_prereq_ids or set())

    adj: Dict[str, List[str]] = {cid: [] for cid in comp_ids}
    for comp in competencies:
        cid = comp["id"]
        for prereq in comp.get("prerequisites", []):
            if prereq not in valid_ids:
                errors.append(f"Competency '{cid}' references non-existent prerequisite '{prereq}'.")
            elif prereq in comp_ids:
                adj[cid].append(prereq)
...

# 2. In validate_cta_rules:
    delta_info = (manifest_data or {}).get("delta") or (manifest_data or {}).get("existing_course")
    existing_comp_ids = set(delta_info.get("existing_competency_ids", [])) if isinstance(delta_info, dict) else set()
    dag_errors = check_prerequisites_dag(competencies, allowed_prereq_ids=existing_comp_ids)

# 3. Export check_cta_file alias:
check_cta_file = validate_cta_rules
```

### 2.4 Escalation Request
`check_cta.py` is currently outside the Write Boundaries of Stream 1E. There is zero overlap with any other stream (Streams 1A, 1B, 1C, 1D do not modify `check_cta.py`).
We request the Orchestrator authorize adding `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/check_cta.py` to Stream 1E Write Boundaries.

---

## 3. Hardening & Adversarial Improvement Plan

While awaiting authorization, we have analyzed the remaining hardening items:
1. **Zero Empty Directory Clutter:**
   - In `ingest.py`, currently `out_doc_dir.mkdir(parents=True, exist_ok=True)` is called unconditionally on line 300.
   - When `render_pages=False` and all inputs are PDFs, this creates empty directories `work/pages/<doc_slug>/`.
   - Improvement: defer creating `out_doc_dir` until pages are actually being written (`if render_pages:`) or for non-PDF types (`image`, `tex`).
2. **Slug Collision Safety & Windows Unicode Stems:**
   - In `ingest.py`, track `seen_slugs` to append numerical suffix if two distinct documents resolve to the same slug (e.g. `ch1/notes.pdf` and `ch2/notes.pdf`, or `Anna’s Archive-93.pdf`).
3. **Compound Greene Math Expressions:**
   - In `cta_merge.py`, expand `normalize_orphan_math` to cleanly wrap parenthesized matrix transpose expressions (`(Z'X)^{-1}`, `X'Z(Z'Z)^{-1}Z'X`) and `\operatorname{plim}_{n \to \infty}` without corrupting inner tokens or generating unbalanced delimiters.
4. **Adversarial Test Suite Expansion:**
   - Test Greene matrix and limit expressions from `ab30cf91`.
   - Test Unicode filenames (`Anna’s Archive-93.pdf`).
   - Test duplicate basename disambiguation in `ingest_course`.
   - Test zero empty directories in `work/pages/` when `render_pages=False`.
