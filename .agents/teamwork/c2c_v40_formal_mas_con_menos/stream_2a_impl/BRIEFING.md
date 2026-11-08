# BRIEFING — Stream 2A (Fase A: Implementador Ortogonal — Gate 2)

## 1. Executive Summary & Objective
Stream 2A implements Gate 2 of the Flash Dyad Orchestrator (C2C v4.0 Formal Mas con Menos):
- **Cryptographic Fast-Path (`< 5 ms`)** via `shard_XX.cert.json` receipts in `run.py` (`--stage templates` and `--stage certify`), avoiding sandbox re-execution when hashes match.
- **Critical Fix for `--stage gates` and `--stage repair-matrix`**:
  - `repair-matrix` reading `grouped_by_rule` or `groups` + `diagnostics_by_competency` + `failing_shards`/`affected_shards`.
  - `gates` executing full pipeline sequence `build` -> `verify` -> publication QA dry-run -> `repair-matrix`, reporting failure if any stage detects blocking issues.
  - Rejection specs normalized with `RejectionSpec` from `engine.interstage_schemas` writing `"status": "REJECTED"` and synchronizing dual keys (`failing_shards` / `affected_shards`, `grouped_by_rule` / `groups`).
- **Governance Fields in `.c2c_subagent_lock.json`**:
  - Adding `{ active, course_id, created_at, fsm_state, turn_count: 0, max_turns: 40, est_tokens: 0, max_tokens: 5000000, last_error_sha256: "", error_sha256_streak: 0, max_error_streak: 3 }` while preserving backward compatibility.
- **Documentation & Rule Invariants**:
  - Update `SKILL.md` to C2C v4.0 contract (`MIN_ARCHETYPES = 4`, DSL `Form-C`, explicit `assumptions`, `ver_*` triple contract, 2D editing matrix, `*.cert.json` `< 5 ms`, `--lean` default, Epistemic Judge 1-seed $\alpha_{\text{Kernel}} = 0$).
  - Create `.agents/rules/c2c-quality-invariants.md` per `FUTURE_MILESTONES.md` §8.1.
- **Align and Expand 7 Exclusive Test Suites**:
  - `test_prompts_contract_alignment.py`
  - `test_bootstrap_and_wave_streaming.py`
  - `test_run_templates_and_dispatch_repair.py`
  - `test_append_workflow.py`
  - `test_c2c_v321_multi_instance_and_append.py`
  - `test_skill.py`
  - `test_delete_course.py`

## 2. Line Ranges & Target Analysis in `run.py`

### 2.1. Fast-Path `< 5 ms` in `--stage templates` (~L755-L960)
- **Current logic:** Reads `pre_shard_manifest.json`, checks if files are up-to-date, conditionally runs `compile_shard`, then unconditionally invokes `check_templates_file_or_dir(templates_dir, cta_path=cta_file)` which runs 50 seeds across every single template in the sandbox.
- **Target implementation:**
  - Support `--force-recheck` (or `self.force_recheck`).
  - When `not getattr(self, "force_recheck", False)`:
    - Inspect `work/shards/<shard_id>.cert.json` (or all `*.cert.json` in `work/shards/`).
    - Validate each certificate:
      1. `cert.get("passed_50_seeds") is True`
      2. `cert.get("source_sha256") == hashlib.sha256((shards_dir / f"{shard_id}_data.py").read_bytes()).hexdigest()`
      3. `cert.get("cta_sha256") == hashlib.sha256(cta_file.read_bytes()).hexdigest()`
      4. For every `cid, tpl_sha` in `cert.get("template_shas", {}).items()`:
         - Resolve `cid_file`: check `templates_dir / cid` if ends with `.json` else `templates_dir / f"{cid}.json"`.
         - Confirm file exists and `hashlib.sha256(cid_file.read_bytes()).hexdigest() == tpl_sha`.
    - Collect all CIDs that are certified.
    - If ALL templates are certified, log fast-path validation `< 5 ms`, skip sandbox execution entirely, and emit `templates_report.json` with status `"PASS"`.
    - If only a subset are certified, only pass uncertified or changed template files to `check_templates_file_or_dir`.
- **Rejection Spec on Failure (~L1188-L1215):**
  - Use `RejectionSpec` from `engine.interstage_schemas` to write both `specific_error_report.json` and `template_failures.json`.
  - Ensures `"status": "REJECTED"`, with synchronized `failing_shards` and `affected_shards`, `grouped_by_rule` and `groups`.

### 2.2. Fast-Path in `--stage certify` (~L1896)
- In `run_stage_certify`, check certificates before running `run_stage_templates`: if templates are cryptographically certified and source files haven't changed, fast-path step completes in `< 5 ms`.

### 2.3. Fix for `--stage repair-matrix` (~L1670-L1754)
- **Problem:** Currently only reads `spec.get("groups")` from `specific_error_report.json`, ignoring `course_publisher.py` outputs or `publish_rejection_spec.json`, and missing `grouped_by_rule`, `diagnostics_by_competency`, and `affected_shards`.
- **Target:**
  - Check both `specific_error_report.json` and `publish_rejection_spec.json` (and `template_failures.json`).
  - Read `grouped_by_rule = spec.get("grouped_by_rule") or spec.get("groups") or {}`.
  - Read `diagnostics = spec.get("diagnostics_by_competency") or {}`.
  - Extract failing competencies and shards from both `failing_shards` and `affected_shards`.
  - Consolidate all findings seamlessly into `matrix`.

### 2.4. Fix for `--stage gates` (~L1755-L1771)
- **Problem:** Currently only runs `build` and `repair-matrix`, completely skipping `verify` and publication QA audit (`run_full_audit`). Courses with psychometric/lexical failures get a false `PASS`.
- **Target:**
  - Execute in deterministic sequence:
    1. `run_stage_build()`
    2. `run_stage_verify()` (`validate_course_content`)
    3. Dry-run QA gates: call `CoursePublisher.validate_candidate` or `standardized_audit_engine.run_full_audit(course_file)`. If blocking issues are found, write `publish_rejection_spec.json`.
    4. `run_stage_repair_matrix()` consolidating findings.
  - If any of steps 1-3 detects blocking failures, `run_stage_gates` MUST set `gate_ok = False`, report failure status, and return/exit with non-zero status if called via CLI.

### 2.5. Governance in `.c2c_subagent_lock.json` (~L1958-L1965)
- Initialize lockfile with:
  ```json
  {
    "active": true,
    "course_id": self.course_id,
    "created_at": now_utc,
    "fsm_state": "bootstrap",
    "turn_count": 0,
    "max_turns": 40,
    "est_tokens": 0,
    "max_tokens": 5000000,
    "last_error_sha256": "",
    "error_sha256_streak": 0,
    "max_error_streak": 3,
    "director_conversation_id": self.director_id or "",
    "work_dir": self.work_dir.resolve().as_posix(),
    "exempt_conversation_ids": []
  }
  ```

## 3. Strict Guardrails & Invariants
- **Zero-Domain Invariant (`test_skill.py`):**
  - In `run.py`, ALL docstrings and comments must be strictly in English.
  - Forbidden substrings: `edo`, `pde`, `derivadas`, `jacobiana`, `eigen`, `euler`, `cobb_douglas`, `lotka`, `lagrange`, `regresi`.
- **Exclusive Write Boundary:**
  - Only touch the 12 listed files.
- **Windows cp1252 Safety:**
  - Avoid raw `\u0332` or unhandled unicode in stdout.

## 4. Test Alignment Strategy
- **`test_prompts_contract_alignment.py`**:
  - Update tests to support Form-C Quad-Band contract (`TEMPLATES` list of dicts with `archetype` and `band`), while keeping backward compatibility with 9-tuples.
  - Allow `"FORBIDDEN"` in prompt security check assertions.
- **`test_bootstrap_and_wave_streaming.py`**:
  - Add hints to mock template in `create_mock_template_file` so `check_instance_invariants` passes in judge generation.
  - Allow `work_order` as dict or read from `Prompt`.
- **Add New Tests**:
  - Add unit test for `< 5 ms` cert fast-path and byte-level invalidation.
  - Add unit test for `gates` blocking on `verify` and QA failures.
  - Add unit test for `repair-matrix` reading `grouped_by_rule` and `diagnostics_by_competency`.
