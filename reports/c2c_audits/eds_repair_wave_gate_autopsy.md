# Forensic Autopsy: The 13 Stage 3B Repair Wave & Gate Verification Breakdown

**Target Run:** `saul_pc_sistemas_de_ecuaciones_vmapreduce5`  
**Director Conversation ID:** `66915882-b7f8-441f-9fc7-d4a964050a42`  
**Target Course:** `courses/saul_pc_sistemas_de_ecuaciones_vmapreduce5`  
**Pipeline Standard:** Content-to-Course (C2C v3.2 / v3.3)  
**Date of Incident:** November 8–9, 2026  
**Investigator:** Forensic Pipeline Architecture & Gate Verification Subagent  
**Report Artifact:** `reports/c2c_audits/eds_repair_wave_gate_autopsy.md`

---

## 1. Executive Summary & Forensic Verdict

A forensic investigation into run `saul_pc_sistemas_de_ecuaciones_vmapreduce5` was conducted to determine why **13 Stage 3B Repair Engineers** were dispatched across **7 shards** (`shard_14`, `shard_33`, `shard_34`, `shard_37`, `shard_39`, `shard_40`, `shard_42`), why these errors bypassed Shard Author execution, why Stage 3 (`templates`) passed in `< 5 ms` with a cryptographic certificate, and why the run subsequently crashed during `run.py --stage gates` (`task-311`).

### The Core Finding: A Phantom Repair Wave Induced by Zombie Artifact Poisoning

The wave of 13 Repair Engineers was **NOT** caused by undetected code flaws surviving into the final course build. 
Instead, it was a **false-positive cascade** triggered by a triad of structural defects:

```
+---------------------------------------------------------------------------------------------------+
| 1. RACE CONDITION: Orchestrator prematurely ran 'run.py --stage templates' (task-228)             |
|    at 20:11:23 while 8 shard authors were actively editing/compiling.                              |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
| 2. GHOST ARTIFACT PERSISTENCE: task-228 failed on WIP files, writing 'template_failures.json'.    |
|    Authors then fixed all errors and certified. Stage 3 (task-268) took the <5ms fast-path,        |
|    BUT DID NOT PURGE 'template_failures.json'.                                                    |
+---------------------------------------------------------------------------------------------------+
                                                  │
                                                  ▼
+---------------------------------------------------------------------------------------------------+
| 3. MULTI-COMPETENCY CONTAGION & ZOMBIE INGESTION: task-311 ('run.py --stage gates')               |
|    passed Build, Verify, and QA (19.6/20.0 Platinum). But 'run_stage_repair_matrix' read the      |
|    stale 20:11:23 rejection file, expanded 7 shards into 13 competencies, and halted the gate.   |
+---------------------------------------------------------------------------------------------------+
```

1. **Premature Orchestrator Trigger (Step 226 / `task-228`):** The orchestrator executed `run.py --stage templates` at `20:11:23` while shards 14, 33, 34, 37, 39, 40, 42, and 44 were actively running. This abortive execution inspected intermediate, work-in-progress files in `work/templates/`, crashed with 18 validation errors, and wrote `work/template_failures.json`.
2. **Author Self-Correction & Cryptographic Certification (Steps 236–264):** Shard authors continued working in their subagent loops. Their local compiler (`compile_shard.py`) caught all syntax, `[R-18]`, `[TPL-DRY]`, and `[TPL-VAR]` flaws, blocked certification until resolved, and finally emitted exit code `0` and valid cryptographic certificates (`shard_XX.cert.json`) between `20:12:09` and `20:17:35`.
3. **Stage 3 Fast-Path Blind Spot (Step 266 / `task-268`):** When all 44 shards certified, `run.py --stage templates` ran again. It verified that all 61 template files matched their `shard_XX.cert.json` SHA-256 hashes, took the `< 5 ms` Fast-Path, and passed. **Critical Flaw:** The fast-path never purged the stale `work/template_failures.json` left behind by `task-228`.
4. **Gate Poisoning & Contagion Fan-Out (Step 309 / `task-311`):** `run.py --stage gates` executed Stage 4 (Build instantiated 1,490 items), Stage 5 (Verify passed 16/16 strict rules), and deterministic QA audit (scored `19.6/20.0` Platinum Mastery, MPRI `99.90/100.0`). However, in `run_stage_repair_matrix()`, the runner unconditionally loaded `template_failures.json` without verifying whether its contents were stale relative to the newer `.cert.json` files.
5. **Shard Packing Contagion:** In `pre_shard_manifest.json`, shards 28–44 packed **2 competencies per shard**. Because `run.py` expanded each failing shard name into all of its constituent competencies, 7 failing shards expanded into **13 competencies**—even though 6 of those competencies had zero errors in the initial failure log!
6. **Concurrent Repair Clashing:** 13 Repair Engineers were launched simultaneously to fix files that were already certified. In multi-competency shards, pairs of subagents (e.g., C-16 and C-17 on `shard_33`, C-19 and C-20 on `shard_34`) concurrently edited the identical `shard_XX_data.py` file, risking write-write race collisions until the run finally stabilized.
7. **Emergency Fix Commit (`14aa55c`):** At `21:07:13` (post-incident), commit `14aa55c` was deployed to add `template_failures.json` to the unlinked file list in `run_stage_gates()` and implement `_is_failure_stale()`.

---

## 2. Chronological Timeline of Events (Hard Log Evidence)

All timestamps reflect local time (`UTC-5`, corresponding to UTC timestamps in logs):

| Timestamp (Local) | Step / Task ID | Component / Actor | Action / Result | Log Evidence & Status |
| :--- | :--- | :--- | :--- | :--- |
| **20:03:18** | Step 65 | Orchestrator | `run.py --stage shard` | CTA partitioned into 44 shards for 61 competencies (`pre_shard_manifest.json`). Shards 01–27 have 1 skill; shards 28–44 have 2 concepts/facts. |
| **20:03:42** | Steps 71–75 | Orchestrator | Subagent Dispatch | 44 Shard Authors spawned concurrently. |
| **20:11:01** | Subagent `0abe54e5` | Shard Author `shard_37` | `compile_shard.py` attempt 3 | **FAILED (Exit 1):** Detected `[R-18]` and `[TPL-VAR]` on `H-01` and `C-01`. Author begins fixing. |
| **20:11:15** | Step 224 | Subagent `96da028f` | Shard Author `shard_28` | Emits `DONE: shard_28.json`. |
| **20:11:23** | Step 226 / `task-228` | Orchestrator | `run.py --stage templates` | **PREMATURE EXECUTION.** Launched while 8 shards are still running (`shard_14, 33, 34, 37, 39, 40, 42, 44`). |
| **20:11:38** | Step 229 / `task-228` | Stage 3 Runner | Validation on WIP files | Inspects unfinalized templates in `work/templates/`. Encounters `T-Hab-14-01/02/03` seed 123 failure. |
| **20:12:01** | Step 234 / `task-228` | Stage 3 Runner | **TASK TERMINATION (FATAL)** | `task-228` exits with code 1: *"Templates contain 18 errors"*. Writes `work/template_failures.json` containing 7 failing shards. |
| **20:12:09** | Subagent `bdafda52` | Shard Author `shard_42` | `compile_shard.py` | **PASS:** `shard_42.cert.json` written. Author emits `DONE` (Step 236). |
| **20:13:48** | Subagent `0abe54e5` | Shard Author `shard_37` | `compile_shard.py` attempt 4 | **PASS:** `shard_37.cert.json` written (clean 50 seeds). Author emits `DONE` (Step 255). |
| **20:14:00** | Subagent `7c610c33` | Shard Author `shard_40` | `compile_shard.py` | **PASS:** `shard_40.cert.json` written. Author emits `DONE` (Step 256). |
| **20:14:18** | Subagent `0c7a4f9e` | Shard Author `shard_39` | `compile_shard.py` | **PASS:** `shard_39.cert.json` written. Author emits `DONE` (Step 258). |
| **20:14:38** | Subagent `af7b7bb9` | Shard Author `shard_33` | `compile_shard.py` | **PASS:** `shard_33.cert.json` written. Author emits `DONE` (Step 260). |
| **20:14:47** | Subagent `18316bca` | Shard Author `shard_34` | `compile_shard.py` | **PASS:** `shard_34.cert.json` written. Author emits `DONE` (Step 262). |
| **20:17:35** | Subagent `6a1e3d60` | Shard Author `shard_14` | `compile_shard.py` attempt 6 | **PASS:** `shard_14.cert.json` written. Author emits `DONE` (Step 264). |
| **20:17:48** | Step 266 / `task-268` | Orchestrator | `run.py --stage templates` | **PASS (Fast-Path < 5 ms):** All 61 templates certified via `shard_XX.cert.json`. **LEAK:** `template_failures.json` is NOT deleted! |
| **20:18:08** | Step 270 / `task-272` | Orchestrator | `run.py --stage build` | **PASS:** Built 1,490 items with stem diversity >= 0.533. Wrote `course.json`. |
| **20:18:45** | Step 286 / `task-288` | Orchestrator | Blind Judge Arbitration | 10 blind judges evaluate 120 items. Result: 100% agreement (120/120 agreed, 0 discordances). |
| **20:21:46** | Step 309 / `task-311` | Orchestrator | `run.py --stage gates` | **GATES EXECUTION.** Build ok, Verify ok (16/16 strict rules passed), QA dry-run ok (19.6/20.0 Platinum). |
| **20:22:04** | Step 311 / `task-311` | `run_stage_repair_matrix` | **CRASH (FATAL)** | Reads stale `template_failures.json` (from 20:11:23). Expands 7 shards to 13 competencies. Exits code 1. |
| **20:22:27** | Step 317 | Orchestrator | `view_file repair_matrix.json` | Shows `"status": "REPAIR_NEEDED"` with 13 competencies across 7 shards. |
| **20:22:34** | Steps 319–325 | Orchestrator | Subagent Dispatch | Spawns 13 Stage 3B Repair Engineers concurrently. |
| **20:25–20:31**| Steps 338–370 | Repair Engineers | Repair Wave Execution | Subagents edit and recompile shards in 2–3 minutes (repairing non-existent bugs or colliding on files). |
| **21:02:00** | Post-repair | Orchestrator | `run.py --stage gates` | **PASS:** Matrix reported 0 competencies, 0 shards. Course verified and certified. |
| **21:07:13** | Commit `14aa55c` | Architecture Patch | `run.py` Hotfix | Adds `template_failures.json` unlinking in `run_stage_gates` and `_is_failure_stale` guard. |

---

## 3. The 13 Flagged Competencies: Failure Codes & Shard Packing Analysis

The 13 competencies flagged in `courses/saul_pc_sistemas_de_ecuaciones_vmapreduce5/work/repair_matrix.json` (captured in `transcript.jsonl` Line 317) originated from exactly **7 shards**. 

### The Shard Packing Architecture

In `pre_shard_manifest.json`, the 61 course competencies were divided as follows:
- **Shards 01–27 (27 shards):** 1 Skill competency per shard (`Hab-01` to `Hab-27`, 30 questions each).
- **Shards 28–44 (17 shards):** **2 Concept/Fact competencies per shard** (20 questions each, 40 total per shard).

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ SHARD PACKING & CONTAGION MATRIX                                                           │
├───────────┬──────────────────────┬─────────────┬────────────────────────────────────────────┤
│ Shard ID  │ Packed Competencies  │ Shard Type  │ True Offender in task-228 Log vs Collateral│
├───────────┼──────────────────────┼─────────────┼────────────────────────────────────────────┤
│ shard_14  │ Hab-14               │ Single (1)  │ Hab-14: [TPL-DRY] seed 123 AssertionError   │
│ shard_33  │ C-16, C-17           │ Dual (2)    │ C-16: [TPL-DYNAMIC-RATIONALE] | C-17: CLEAN│
│ shard_34  │ C-19, C-20           │ Dual (2)    │ C-20: [TPL-D4], [TPL-STATIC-OPT] | C-19:CLN│
│ shard_37  │ H-01, C-01           │ Dual (2)    │ C-01 & H-01: [R-18], [TPL-VAR]             │
│ shard_39  │ C-05, H-03           │ Dual (2)    │ WIP at 20:11:23 (unfinalized) | BOTH CLEAN │
│ shard_40  │ C-10, H-04           │ Dual (2)    │ H-04: [TPL-STATIC-OPT] | C-10: CLEAN       │
│ shard_42  │ H-06, C-18           │ Dual (2)    │ WIP at 20:11:23 (unfinalized) | BOTH CLEAN │
└───────────┴──────────────────────┴─────────────┴────────────────────────────────────────────┘
Total: 7 Shards = 1 Single-pack + 6 Dual-packs = 13 Competencies
```

### Exact Failure Codes Flagged in `task-228.log`

The following exact rule violations were recorded in `task-228.log` when Stage 3 ran prematurely:

#### 1. `[R-18: DISTRACTORES BOILERPLATE SINTÉTICOS]`
- **Target Competency:** `C-01` (`T-C-01-01`), `H-01` (`T-H-01-01`)
- **Offending Fragment:**
  ```text
  repetitive trivial template across 6 options ('$\text{coeficientes } [A \mid B] = 90$...')
  repetitive trivial template across 6 options ('$\text{orden del sistema} = 0$...')
  ```
- **Cause:** In attempt 3 of Shard Author 37, distractors were generated using a loop that varied only a numeric index inside a fixed LaTeX string. The rule in `engine/invariants.py` (`check_synthetic_boilerplate_distractors`, lines 224–240) detected $\ge 4$ options sharing an identical prose skeleton $> 20$ characters.

#### 2. `[TPL-DYNAMIC-RATIONALE: RATIONALE ESTÁTICO EN DISTRACTOR DINÁMICO]`
- **Target Competency:** `C-16` (`T-C-16-04`)
- **Offending Fragment:**
  ```text
  Distractor 'D-C16-02' varía en contenido (6 variantes) pero tiene error_rationale estático:
  'La isoclina afín se desplaza hacia abajo'
  ```
- **Cause:** Distractor content was dynamically computed from random parameters across seeds, but its pedagogical explanation was a fixed string missing `@var@` parameter placeholders.

#### 3. `[TPL-D4: OPCIONES DUPLICADAS]`
- **Target Competency:** `C-20` (`T-C-20-01`)
- **Offending Fragment:**
  ```text
  seed=124: Dos o más opciones tienen contenido idéntico ('$e(0) = 62$')
  ```
- **Cause:** In seed 124, random parameter generation caused perturbation values for two distinct distractor IDs to evaluate to the identical numerical scalar.

#### 4. `[TPL-STATIC-OPT: CONJUNTO DE OPCIONES ESTÁTICO / BAJA VARIABILIDAD]`
- **Target Competency:** `C-20` (`T-C-20-04`), `H-04` (`T-H-04-02`), `Hab-14` (`T-Hab-14-01`)
- **Offending Fragment:**
  ```text
  T-C-20-04: Únicamente 4/5 conjuntos de opciones generados en 50 semillas (multiple_select).
  T-H-04-02: Únicamente 7/10 claves correctas únicas en 50 semillas (requerido >= 10).
  T-Hab-14-01: Únicamente 7/10 claves correctas únicas en 49 semillas.
  ```
- **Cause:** Narrow parameter spaces in generator loops (`range(1, 4)`) caused correct answers or option sets to collapse onto a small set of values across 50 dry-run seeds.

#### 5. `[TPL-DRY: FALLO EN EJECUCIÓN DRY-RUN]`
- **Target Competency:** `Hab-14` (`T-Hab-14-01`, `T-Hab-14-02`, `T-Hab-14-03`)
- **Offending Fragment:**
  ```text
  Primer seed fallido: 123
  Parámetros: {'a': 3, 'b': 2, 'c': 2, 'd': -4, 'det': -16, 'tr': -1, 'xstar': -1, 'ystar': 2, 'p': 16, 'q': 16, 'ans': -1}
  Excepción: AssertionError: cross_check verification returned False
  ```
- **Cause:** In attempt 4 of Shard Author 14, the analytical cross-check verifier had a sign inversion in calculating equilibrium translation coordinates $(A^{-1}B)$ under seed 123.

#### 6. `[TPL-VAR: DIVERSIDAD DE REACTIVOS]`
- **Target Competency:** `C-01`, `H-01`
- **Offending Fragment:**
  ```text
  Fallo al instanciar cuota de diversidad (20 ítems):
  Template T-C-01-01 could only generate 0/5 unique invariant instances after 300 attempts.
  ```
- **Cause:** In attempt 3 of Shard Author 37, collision rejection loops in `instantiate_competency` timed out because the random variable space was too constrained to produce 5 unique instances.

#### 7. `[SHARD] <shard_id> marked as failing/affected` (Contagion Tag)
- **Target Competencies:** `C-17`, `C-19`, `H-03`, `C-10`, `H-06`, `C-05`, `C-18`
- **Cause:** These competencies had **ZERO** intrinsic errors in the log. They were marked solely because of `run.py` lines 2159–2165:
  ```python
  for s_id in (spec.get("failing_shards") or spec.get("affected_shards") or []):
      cids_for_s = shard_to_cids.get(s_id, [])
      if cids_for_s:
          for c_id in cids_for_s:
              _add(c_id, "linter", f"[SHARD] {s_id} marked as failing/affected")
  ```

---

## 4. Why Errors Were Not Caught During Shard Author Execution

A central question of this forensic audit is: **Did `compile_shard.py` allow flawed code to compile and emit `.cert.json` during the Shard Authors' execution?**

### The Empirical Evidence: `compile_shard.py` BLOCKED Every Flaw

Inspection of subagent transcripts proves conclusively that `compile_shard.py` **DID NOT** allow these errors to pass. Shard Authors were actively blocked by `compile_shard.py` and had to perform multiple iterations to resolve them.

#### Case Study 1: Shard Author 37 (`0abe54e5-5f85-45ee-aa26-ae65f222ab21`)
- **Step 30 (`20:11:01`):** Shard Author 37 ran `compile_shard.py`.  
  Output: **FAILED with exit code 1**.  
  Compiler explicitly reported:
  ```text
  [-] FAIL: 4 errores detectados al compilar shard_37:
  [-] [R-18: DISTRACTORES BOILERPLATE SINTÉTICOS] in H-01.json and C-01.json
  [-] [TPL-VAR: DIVERSIDAD DE REACTIVOS] in C-01.json and H-01.json
  ```
  `shard_37.cert.json` was **NOT** generated.
- **Step 31–51:** Shard Author 37 read the line-mapped error, modified `shard_37_data.py` with `edit_file`, diversified distractor formulas, and widened parameter ranges.
- **Step 52 (`20:13:41`):** Shard Author 37 ran `compile_shard.py` attempt 4.  
  Output: **PASSED with exit code 0**:
  ```text
  [+] PASS: Shard 'shard_37' compilado exitosamente (2 competencias, 8 plantillas/arquetipos, 50 semillas dry-run validadas).
  ```
  `shard_37.cert.json` was generated at timestamp `1794187428` (`20:13:48`).

#### Case Study 2: Shard Author 14 (`6a1e3d60-abf4-4c73-8498-de49729127e7`)
- **Attempt 4 (`20:11:20`):** Shard Author 14 ran `compile_shard.py`.  
  Output: **FAILED with exit code 1**.  
  Compiler reported `[TPL-DRY]` on seed 123 (`cross_check verification returned False`). `shard_14.cert.json` was **NOT** generated.
- **Attempt 5–6:** Shard Author 14 corrected the verifier formula.
- **Step 69 (`20:17:31`):** Shard Author 14 ran `compile_shard.py` attempt 6.  
  Output: **PASSED with exit code 0**:
  ```text
  [+] PASS: Shard 'shard_14' compilado exitosamente (1 competencias, 4 plantillas/arquetipos, 50 semillas dry-run validadas).
  ```
  `shard_14.cert.json` was generated at timestamp `1794187627` (`20:17:35`).

### Why Did the Errors Leak to the Gate?

The errors did not leak because `compile_shard.py` was too permissive. They leaked because:

```
20:11:01                  20:11:23                   20:13:41                20:17:48
Author 37 Fails           Orchestrator Fires         Author 37 Fixes         Fast-Path Stage 3
(WIP template on disk)    Premature Task-228         & Certifies Clean       Passes in <5ms
                          (Captures WIP failures     (shard_37.cert.json)    (Leaves stale
                          in template_failures.json)                         failure file on disk)
```

1. When `compile_shard.py` runs, it writes template files into `work/templates/<cid>.json` **before** running validation (lines 3065–3088 of `compile_shard.py`).
2. When validation fails, the intermediate JSON file remains in `work/templates/` while the author prepares an edit.
3. The orchestrator launched `run.py --stage templates` (`task-228`) **while these intermediate files were sitting uncertified on disk**.
4. `task-228` validated the intermediate files, crashed, and dumped `work/template_failures.json`.
5. When the author subsequently succeeded, the intermediate file was overwritten with clean code and certified, but `template_failures.json` was never notified or deleted.

---

## 5. Anatomy of the Fast-Path & Gate Verifier Discrepancy

### Why Stage 3 Passed in `< 5 ms` (Task-268)

When the orchestrator launched Stage 3 for the second time at `20:17:48` (`task-268`), lines 1050–1076 of `run.py` executed:

```python
# run.py lines 1074-1077
if not getattr(self, "force_recheck", False) and len(certified_template_files) == len(all_template_files) and len(all_template_files) > 0:
    print(f"  [+] Fast-path < 5 ms: All {len(all_template_files)} template(s) cryptographically certified via shard_XX.cert.json.")
    is_valid = True
    errors = []
```

Because all 44 shards had completed their final compilation loops and emitted `shard_XX.cert.json`, all 61 templates matched their expected SHA-256 hashes. The runner skipped `check_templates_file_or_dir()` entirely and returned `is_valid = True`.

### The Critical Omission in Stage 3

In `run.py`, when Stage 3 succeeds:
- It records timing (`timings.json`).
- It writes `work/reports/templates_report.json` with status `"PASS"`.
- **IT DOES NOT UNLINK OR PURGE `work/template_failures.json`!**

Lines 1147–1167 only write `template_failures.json` when `not is_valid`. There was no corresponding cleanup block:
```python
# MISSING IN RUN.PY:
if is_valid:
    (self.work_dir / "template_failures.json").unlink(missing_ok=True)
```

### Why the Pipeline Crashed in `run.py --stage gates` (Task-311)

At `20:21:46`, the orchestrator ran `task-311` (`run.py --stage gates`). 
Here is what `run_stage_gates()` actually executed (lines 2242–2328 of `run.py`):

1. **Build Gate (`run_stage_build`):** Passed! Instantiated 1,490 items across all 61 competencies. Anti-giveaway bounds passed (`longest=64.0%, shortest=60.1%`).
2. **Verify Gate (`run_stage_verify`):** Passed! Strict validation passed `100% (16/16 rules)`. Verified course written to `course_verified.json`.
3. **QA Deterministic Audit Gate:** Passed! QM-OSCQR score was `19.6/20.0` (Platinum Mastery) and MPRI was `99.90/100.0`. 0 hard penalties.
4. **Repair Matrix Gate (`run_stage_repair_matrix`):**
   ```python
   # run.py line 2075-2081 (at commit e357df5, during incident):
   report_candidates = [
       self.work_dir / "specific_error_report.json",
       self.work_dir / "publish_rejection_spec.json",
       self.work_dir / "template_failures.json",  # <-- LOADED HERE!
   ]
   for rep_p in report_candidates:
       if not rep_p.is_file():
           continue
       spec = json.loads(rep_p.read_text(encoding="utf-8"))
       # INGESTED ALL 7 FAILING SHARDS FROM 20:11:23!
   ```

Because `work/template_failures.json` was still on disk from `task-228` (10 minutes earlier), `run_stage_repair_matrix()` ingested all 7 failing shards, expanded them to 13 competencies, wrote `repair_matrix.json` with status `"REPAIR_NEEDED"`, and raised:

```json
[FATAL ERROR] Pipeline terminated:
{
  "status": "failed",
  "stage": "gates",
  "timestamp": "2026-11-09T01:22:04.690529+00:00",
  "error": "Quality gates failed. Blocking issues found in build, verify, or QA audit; repair matrix populated."
}
```

---

## 6. Multi-Competency Shard Packing: Compounding the Catastrophe

Packing 2 competencies per shard in shards 28–44 introduced two fatal architectural vulnerabilities:

### 1. Bounded Failure Isolation Collapse (Contagion)
When a shard contains multiple competencies, `compile_shard.py` compiles the entire file `shard_XX_data.py` into multiple template files (`templates/C-16.json` and `templates/C-17.json`). If `C-16` contains an error, `compile_shard.py` returns `False`, and `shard_33` as a whole is recorded as uncertified.

When `run_stage_repair_matrix()` processed `failing_shards`:
- `shard_33` was in `failing_shards` due to `C-16`.
- `shard_to_cids["shard_33"]` returned `["C-16", "C-17"]`.
- `_add("C-17", "linter", "[SHARD] shard_33 marked as failing/affected")` executed.
- `C-17`, which was completely clean and valid, was marked as failing!

This mechanism artificially doubled the repair burden across 6 dual-pack shards:
- `shard_33`: `C-16` (flawed in WIP) + `C-17` (clean) $\rightarrow$ 2 repair engineers
- `shard_34`: `C-20` (flawed in WIP) + `C-19` (clean) $\rightarrow$ 2 repair engineers
- `shard_37`: `C-01` (flawed in WIP) + `H-01` (flawed in WIP) $\rightarrow$ 2 repair engineers
- `shard_39`: `C-05` (clean) + `H-03` (clean) $\rightarrow$ 2 repair engineers
- `shard_40`: `H-04` (flawed in WIP) + `C-10` (clean) $\rightarrow$ 2 repair engineers
- `shard_42`: `C-18` (clean) + `H-06` (clean) $\rightarrow$ 2 repair engineers
- `shard_14`: `Hab-14` (flawed in WIP) $\rightarrow$ 1 repair engineer  
**Total:** $1 + 2 \times 6 = 13$ repair engineers dispatched.

### 2. Disjoint File Boundary Violation (Write-Write Race Collision)
Under the C2C architecture, each subagent has strict Scope-Lock boundaries. However, dispatching two repair engineers for the same shard meant:
- `Repair Engineer C-16` was given write access to `shard_33_data.py`.
- `Repair Engineer C-17` was given write access to `shard_33_data.py`.

Both subagents executed concurrently in background tasks. When `C-17` completed and called `edit_file` followed by `compile_shard.py` at `20:26:08`, it overwrote `shard_33_data.py`. When `C-16` called `edit_file` at `20:27:03`, it was editing a file that had already been altered by `C-17`. While both managed to converge without syntax errors, this violated the principle of disjoint write boundaries.

---

## 7. Forensic Verification of the Emergency Fix (`14aa55c`)

At `21:07:13` on November 8, 2026, commit `14aa55c2029` was committed to the repository:

```diff
commit 14aa55c2029f851f266d54f5ba027f81f9c824fc
Author: augus <augus@users.noreply.github.com>
Date:   Sun Nov 8 21:07:13 2026 -0500

    feat(c2c): optimize runtime locks, heartbeat logging and register pending agentic audits
    - run.py: add _LogCaptureStream streaming heartbeats and filter stale template failures

diff --git a/.agents/skills/content-to-course/run.py b/.agents/skills/content-to-course/run.py
--- a/.agents/skills/content-to-course/run.py
+++ b/.agents/skills/content-to-course/run.py
@@ -2051,6 +2074,26 @@ class PipelineRunner:
+        def _is_failure_stale(c: Any, rep_mtime: float) -> bool:
+            if not c:
+                return False
+            c_str = str(c)
+            s_id = cid_to_shard.get(c_str)
+            cand_certs = []
+            if s_id:
+                cand_certs.extend([
+                    self.work_dir / "shards" / f"{s_id}.cert.json",
+                    self.work_dir / f"{s_id}.cert.json",
+                ])
+            cand_certs.extend([
+                self.work_dir / "templates" / f"{c_str}.cert.json",
+                self.work_dir / "templates.cert.json",
+            ])
+            for cp in cand_certs:
+                if cp.is_file() and cp.stat().st_mtime > rep_mtime:
+                    return True
+            return False
...
@@ -2165,6 +2235,7 @@ class PipelineRunner:
             "publish_rejection_spec.json",
             "publish_rejection_spec.md",
             "audit_gate_report.json",
+            "template_failures.json",
         ):
             (self.work_dir / stale).unlink(missing_ok=True)
```

### Assessment of Commit `14aa55c`
The patch correctly recognized that:
1. `template_failures.json` was persisting across gate runs and needed to be unlinked in `run_stage_gates()`.
2. Rejection reports must be ignored if a valid `.cert.json` was generated *after* the rejection report timestamp (`cp.stat().st_mtime > rep_mtime`).

However, as demonstrated in Section 8, **loopholes remain** in the current implementation.

---

## 8. Remaining Architectural Gaps & Conclusive Remedies

To guarantee zero false positives, zero ghost rejection leakage, and zero multi-agent repair collisions, the following permanent architectural updates must be made:

### Gap 1: State Sanitization Deficit in `run_stage_templates()`
**Flaw:** If `run.py --stage templates` succeeds (via fast-path or full re-check), it does **not** unlink `template_failures.json`. If `run_stage_repair_matrix()` is subsequently invoked directly, or if `run_stage_gates()` is called in an environment where file modification times drift (e.g., git checkouts, cross-volume rsync, Windows FAT/NTFS timestamp rounding), stale rejection reports can still be ingested.

**Remedy:** Implement immediate state purging on success in `run_stage_templates()`:
```python
# .agents/skills/content-to-course/run.py
if is_valid:
    for stale_rep in ("template_failures.json", "template_failures.md"):
        (self.work_dir / stale_rep).unlink(missing_ok=True)
```

### Gap 2: Premature Stage Execution (Missing Active Subagent Barrier)
**Flaw:** The orchestrator was allowed to launch `task-228` (`run.py --stage templates`) while 8 shard authors were running. There is currently no pre-flight lock preventing pipeline stages from running if active subagents exist.

**Remedy:** Add an Orchestration Concurrency Sentinel to `run.py`:
```python
def check_no_active_shard_authors(work_dir: Path) -> None:
    """Blocks stage execution if shard authors are currently running."""
    lock_files = list((work_dir / "shards" / ".check_attempts").glob("*.lock"))
    if lock_files:
        raise RuntimeError(
            f"Cannot execute stage templates: {len(lock_files)} shard author(s) are actively compiling. "
            f"Wait for all authors to emit DONE."
        )
```

### Gap 3: Multi-Competency Shard Packing Contagion
**Flaw:** Bundling 2 competencies into 1 shard (`pre_shard_manifest.json`) destroys failure isolation. When repair is dispatched, 2 subagents concurrently modify the same file.

**Remedy:** Enforce a strict **1 Shard = 1 Competency** invariant in `plan_shards`:
- In `pre_shard_manifest.json`, `total_shards` must equal `total_competencies` (61 shards for 61 competencies).
- This guarantees completely disjoint file writing boundaries (`courses/.../shards/shard_XX_data.py`), eliminates shard-to-competency fan-out in repair matrices, and prevents write-write race collisions during repair waves.

### Gap 4: Coarse Shard-Level Contagion Mapping in `run_stage_repair_matrix`
**Flaw:** Lines 2159–2165 map every shard in `failing_shards` to *all* of its constituent competencies, dragging innocent competencies into repair.

**Remedy:** Only flag competencies that have explicit diagnostic error entries:
```python
# .agents/skills/content-to-course/run.py
# REPLACE lines 2159-2165:
# Do NOT fan-out failing_shards to all competencies blindly.
# Only flag competencies that have explicit entries in diagnostics_by_competency or locations.
```

### Gap 5: Intermediate Template Isolation in `compile_shard.py`
**Flaw:** `compile_shard.py` writes output JSON files directly to `work/templates/<cid>.json` before validating them. If validation fails, the uncertified template sits in the shared directory where other stages can see it.

**Remedy:** Use atomic staging:
`compile_shard.py` must write candidate templates to a staging directory (`work/shards/.staging/<shard_id>/<cid>.json`) and only move them to `work/templates/<cid>.json` upon achieving a clean validation exit code and emitting `.cert.json`.

---

## 9. Comprehensive Audit Summary Table

| Evaluation Criterion | Forensic Finding | Evidence Reference |
| :--- | :--- | :--- |
| **Number of Flagged Competencies** | 13 competencies | `transcript.jsonl` Line 317, `task-311.log` Line 88 |
| **Number of Affected Shards** | 7 shards (`shard_14, 33, 34, 37, 39, 40, 42`) | `repair_slices/`, `repair_matrix.json` |
| **True Source of Failures** | Intermediate WIP errors captured by premature task-228 | `task-228.log` Lines 72–194 |
| **Final Author Compilation Status** | 100% Passed and certified prior to Stage 4 Build | `shard_XX.cert.json` timestamps (20:12:09–20:17:35) |
| **Stage 3 Fast-Path Result** | Passed in `< 5 ms` with 61/61 certified templates | `task-268.log` Lines 50–53 |
| **Stage 4 Build Result** | Passed; 1,490 items built; stem diversity >= 0.533 | `task-272.log` Lines 5–73 |
| **Stage 5 Verify & QA Result** | Passed; 16/16 strict rules; QA Score 19.6/20.0 Platinum | `task-311.log` Lines 79–82 |
| **Mechanism of Stage Gates Failure** | Ingestion of unpurged `template_failures.json` from task-228 | `run.py` commit `e357df5` vs `14aa55c` |
| **Mechanism of Shard Expansion (7 $\rightarrow$ 13)** | Dual-pack shard fan-out in `run_stage_repair_matrix` | `run.py` lines 2159–2165 (`pre_shard_manifest.json`) |
| **Actual Course Quality** | Flawless (Platinum Mastery, 0 true defects in build) | `course_verified.json`, `gates.log` |
| **Repair Wave Classification** | **100% Phantom / False Positive Cascade** | All repair slices had empty diagnostic records |

---
*Report completed and certified for pipeline governance archive.*
