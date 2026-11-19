# HANDOFF — C2C Prompt Convergence (Milestone 20 + CTA Autonomy) & Pipeline Alignment

> **Project Root:** `d:\Augusto\personal_portfolio\Tops_academy`
> **Python Venv:** `.\.venv\Scripts\python.exe` (Windows PowerShell)
> **Previous Session Artifact / Scratch Dir:** `C:\Users\augus\.gemini\antigravity\brain\803cd022-8081-4953-9985-2371d0930e6e\`
> **NEXT SESSION START HERE FOR PARALLEL 5-PAIR PROMPT ITERATION:** [HANDOFF_PROMPT_PAIRS.md](file:///d:/Augusto/personal_portfolio/Tops_academy/HANDOFF_PROMPT_PAIRS.md) — The 5 staged `.proposed.md` prompts were promoted cleanly to the non-lean full prompts in `.agents/skills/content-to-course/system_prompts/prompt_*.md` (`M20 v4.3`, `CR=0`, `audit_prompt.py --pipeline-check` `0/0/0` + `4/4`, `test_prompt_shard_author_file` + `test_system_prompts_shard_author_contract_and_budgets` `2 passed`), AND Phase 2 `.py` Milestone 20 alignments + `tests/engine/test_m20_pipeline_alignment.py` (19 tests) are now ALREADY APPLIED on disk. Use `HANDOFF_PROMPT_PAIRS.md` for the parallel Improver + Blind-Auditor pairs session.

---

## 1. Goal

1. **Converge all 5 staged C2C lean system prompt proposals** in `C:\Users\augus\.gemini\antigravity\brain\803cd022-8081-4953-9985-2371d0930e6e\scratch\prompt_*.proposed.md` to **`0 Alta / 0 Media / 0 Baja`** simultaneously on BOTH:
   - `.agents/skills/prompt-architect/scripts/audit_prompt.py --pipeline-check` (`4/4 ✅`), AND
   - an independent execution-capable blind auditor (`Model="inherit"`, running all few-shot examples inside each prompt inside `tempfile.TemporaryDirectory()`).
2. **Align the C2C pipeline `.py` files and tests** (`.agents/skills/content-to-course/*.py`, `engine/*.py`, `src/validator/rules.py`, plus new unit tests in `tests/engine/test_m20_pipeline_alignment.py`) with the **Milestone 20 + CTA-Autonomy paradigm**:
   - CTA Architects decide `recommended_modalities` per competency autonomously (no rigid MC/FIB/MS quotas).
   - Full validation, interpolation, diversity, KaTeX, and leak parity across all 9 modalities (`MC7`, `MS`, `FIB`, and the 6 M20 modalities: `open_symbolic`, `proof_dag`, `adversarial_break`, `unstructured_model`, `invariant_canvas`, `concept_matching`).
3. **Run full verification (`pytest`, `_validate_proposals.py`, `audit_prompt.py`)**, update `prompt_architect_audit_report.md` and `walkthrough.md`, and present the completed walkthrough (still **holding promotion** of staged prompts into `system_prompts/lean/*.md` & `subagent_types.json` until explicit user approval).

---

## 2. Inviolable Constraints & User Decisions

- **No 13 KB JSON budget:** Explicitly lifted by user (`"there is no json budget, forget about that"` / `"if you need, change the test"`). Spec ceiling raised to `< 46,080` bytes (single `read_file` cap) in `tests/pipeline/test_bootstrap_and_wave_streaming.py:146` and `scratch/_validate_proposals.py:47`.
- **Keep prompt edits staged in `scratch/prompt_*.proposed.md`:** NEVER overwrite `.agents/skills/content-to-course/system_prompts/lean/*.md`, `.agents/skills/content-to-course/subagent_types.json`, or anything inside `courses/` until explicit user approval.
- **Line endings:** Keep pure LF (`0` `\r` bytes) on all 5 staged `prompt_*.proposed.md` files.
- **Strict Blind Audit Isolation:** NEVER pass `audit_prompt.py` scores, prior-round audit findings, or `scratch/_validate_proposals.py` to any blind auditor subagent. The blind auditor subagent MUST be defined with `EnableWriteTools=True` and a strict read-only workspace rule so it can execute every prompt's few-shot examples in `tempfile.TemporaryDirectory()`.
- **Pre-existing background items in previous session:** Preview server `task-1713` (`PORT=5174`) and browser subagent `f80d6777-d5d3-4d73-a107-5f7ca4e05627` (not needed for this task).

---

## 3. Current Progress

### A. Status of the 5 Staged Prompt Proposals
All 5 files live in `C:\Users\augus\.gemini\antigravity\brain\803cd022-8081-4953-9985-2371d0930e6e\scratch\`.
Latest local verification (after final edits):
- **Pure LF:** `0` `\r` bytes across all 5 files.
- **`audit_prompt.py --pipeline-check --format markdown`:** **0 Alta / 0 Media / 0 Baja** and **`4/4 ✅`** on all 5 files.
- **`_validate_proposals.py`:** Exited `0` with **zero errors and zero warnings** across all prompt examples:
  - `SHARD_AUTHOR_EX1_COMPILED_50_SEEDS_OK`
  - `SHARD_AUTHOR_EX2_COMPILED_50_SEEDS_OK` (including `[TPL-ORPHAN-VARS]` warning eliminated)
  - `CTA_ARCHITECT_EXAMPLES_1_2_3_OK`
  - `REPAIR_AST_AND_EX2_COMPILED_50_SEEDS_OK`
  - `HARMONIZER_AND_JUDGE_JSON_OK`
  - `ALL_6_M20_JUDGE_MODALITIES_VERIFIED`

| Staged File | Raw / JSON Size | Round 6 Exec Blind Audit | Edits Applied After Round 6 |
|:---|---:|:---:|:---|
| `prompt_cta_architect.proposed.md` | 14,047 B / 14,696 B | **0 Alta / 0 Media / 0 Baja** (3/3 `compile_cta.py` + `check_cta.py` `EXIT 0`, 0 warnings) | None (ready) |
| `prompt_cta_harmonizer.proposed.md` | 10,255 B / 10,753 B | **0 Alta / 0 Media / 0 Baja** (3/3 `cta_merge.py apply` `EXIT 0`) | None (ready) |
| `prompt_blind_judge.proposed.md` | 13,953 B / 15,242 B | **0 Alta / 0 Media / 0 Baja** (4/4 JSON, 13/13 Python/SymPy verified, 7/7 `_sanitize_m20_judge_item`, 11/11 `rate=1.0`, 2/2 `BLOCKED`) | None (ready) |
| `prompt_shard_author.proposed.md` | 27,791 B / 28,671 B | 0 Alta / 0 Media / 1 Baja (`[TPL-ORPHAN-VARS]` warning on `'ha'` in `T-C02-02`; QA `20.0/20`, 50/50 valid) | Fixed L140-142 (`ver_cm` checks `v.get("ha")==v.get("a",0)//2`) & L164 (`SOL_CM` uses `=@ha@/\sqrt{x}$`); verified 0 warnings |
| `prompt_repair.proposed.md` | 18,282 B / 19,072 B | 0 Alta / 0 Media / 1 Baja (`RATS["D-C02-03"]` omitted `@c@` vs `s + c + 1` in `gen_c02_2`, plus double backticks on L12) | Fixed L93 (`$@s@ + @c@ + 1$`) & L12 backticks; verified 0 warnings |

- **Round 7 Execution-Backed Blind Audit (`Prompt Architect Blind Auditor R7 Exec`, `cfc02011-a2d3-4397-8d03-a9df6cc6a9ef`):** Completed before promotion with `0 Alta / 0 Media` across all 5 staged prompts + 100% live sandbox pass, reporting the following exact **`Baja`** counts: `prompt_cta_architect.proposed.md` **0/0/1** (`Lean` label vs size / `dispatch.py:103,133`), `prompt_cta_harmonizer.proposed.md` **0/0/1** (`Lean` label vs size), `prompt_shard_author.proposed.md` **0/0/2** (27.8 KB > `~12 KB` / missing header scope + L50 hardcoded `15`/`10`/`0.50` vs `<<S4_*>>`), `prompt_repair.proposed.md` **0/0/2** (`Lean` label vs size + L42–43 hardcoded `15`/`10` vs `<<S4_*>>`), `prompt_blind_judge.proposed.md` **0/0/1** (`Lean` label vs size). Its transcript is at `C:\Users\augus\.gemini\antigravity\brain\cfc02011-a2d3-4397-8d03-a9df6cc6a9ef\.system_generated\logs\transcript.jsonl`. All 5 staged files were then promoted into non-lean `.agents/skills/content-to-course/system_prompts/prompt_*.md` (`M20 v4.3`) for parallel 5-pair blind re-auditing & improvement via [HANDOFF_PROMPT_PAIRS.md](file:///d:/Augusto/personal_portfolio/Tops_academy/HANDOFF_PROMPT_PAIRS.md).

### B. Repository State (`git status --short`)
Modified in workspace prior to handoff:
- `.agents/skills/content-to-course/dispatch.py` — added `Doc: {doc_name}.` for `is_pdf_slice`, updated KaTeX hint to `[KATEX-TEXT-PROSE]/[KATEX-PROSE-OVERFLOW]`, and synced M20 judge & `recommended_modalities` fields
- `.agents/skills/content-to-course/judge.py` — changed `view_file` -> `read_file` in `emit_judge_redispatch`; M20 sanitization & matching
- `tests/pipeline/test_bootstrap_and_wave_streaming.py` — raised prompt JSON ceiling from `< 13000` to `< 46080`
- Prior-session modifications already present in working tree (do NOT touch `system_prompts/lean/*.md` for our 5 staged prompts until user approves):
  - `.agents/skills/content-to-course/system_prompts/lean/prompt_blind_judge.md`
  - `.agents/skills/content-to-course/system_prompts/prompt_blind_judge.md`
  - `.agents/skills/content-to-course/system_prompts/prompt_repair.md`
  - `.agents/skills/content-to-course/system_prompts/prompt_shard_author.md`
  - `reports/c2c_patches/patch_ledger.jsonl`

- **Phase 2 `.py` pipeline alignments have NOT been applied yet.**

---

## 4. What Worked

- **Execution-capable blind auditor in `tempfile.TemporaryDirectory()`:** Giving the blind auditor `EnableWriteTools=True` with a strict read-only workspace constraint so it actually executes every prompt's few-shot examples through `compile_cta.py`, `check_cta.py`, `cta_merge.py`, `compile_shard.py`, `shard_precheck.py`, `judge.py`, `validate_course_content`, and `standardized_audit_engine.run_full_audit` surfaced real defects missed by static reading alone (e.g. `[R-19]` leak in Repair `S4`/`gen_c02_4`, `[TPL-ORPHAN-VARS]` on `'ha'` in Shard Author `T-C02-02`, algebraic mismatch `$@s@ + 1$` vs `s + c + 1`).
- **Reporting BOTH KaTeX `\text{}` rules explicitly:** Documenting `<= 2 words / <= 20 chars` (`[KATEX-TEXT-PROSE]` in `check_templates.py:1307-1308`) AND `<= 45 chars` global (`[KATEX-PROSE-OVERFLOW]` in `engine/invariants.py:891` / `src/validator/rules.py:1088` / `shard_precheck.py:158`) resolved apparent contradictions.
- **Preserving test tokens accurately:** Using `` `StartLine`/`EndLine` (rango de líneas / `line_range`) `` in `prompt_repair.proposed.md:12` satisfied both tool-schema accuracy and `tests/pipeline/test_c2c_hardening_prompts.py:49` (`assert "line_range" in content`).
- **Compiler tag & hook-guard precision:** Using `[TPL-FIB-KATEX]` (`compile_shard.py:3302`) instead of legacy `[FIB-NAKED]` in `prompt_repair`, and matching `c2c_hook_guard.py:246-265` (`< 40` / `>= 40`, fallback `450`/`250`, `< 6` errors in `<= 5` lines).

---

## 5. What Didn't Work (Avoid Repeating)

- **Read-only blind auditor (`EnableWriteTools=False`):** The default `prompt_architect_blind_auditor` could not run commands to execute prompt examples; replace with an execution-capable definition constrained to `tempfile.TemporaryDirectory()`.
- **Putting `$k > @s@$` in Repair `S4` stem with `$k > {s}$` as a true option:** Triggered `[R-19]` answer leak and `0/5` diversity in `compile_shard.py`. Fixed by keeping `$k > @s@$` as premise in `S4` and using deduced `$3k > {3*s}$` and `$2k > {2*s}$` as true options (with `$k < -{s}$` and `$k = {s-1}$` as false distractors).
- **Non-canonical `param_space >= 500` in Shard Author:** Contradicted `check_templates.py` (no such rule exists) and `gen_ic` (`342` combinations); already removed.
- **`rg` on Windows PowerShell:** Not installed (`ObjectNotFound`); use `.\.venv\Scripts\python.exe -c ...` or `Select-String` instead.
- **Fixture gotcha awaiting Phase 2 (`engine/assemble.py`):** In `C:\Users\augus\.gemini\antigravity\brain\803cd022-8081-4953-9985-2371d0930e6e\scratch\_validate_proposals.py:255`, the synthetic `q_ic` test declares `"inequality": {"curve_id": "b", ...}` **without** `"fixed_curves"`. Once `engine/assemble.py` validates `inequality.curve_id` against declared `fixed_curves`/`interactive_curves`, update that fixture (and check `tests/engine/test_m20_anti_descarte_and_modalities.py` for any `inequality` fixture missing `fixed_curves`).

---

## 6. Next Steps (Execute in Order)

### Step 1: Verify Round 7 Blind Audit Reached `0/0/0` Across All 5 Prompts
1. Check `C:\Users\augus\.gemini\antigravity\brain\cfc02011-a2d3-4397-8d03-a9df6cc6a9ef\.system_generated\logs\transcript.jsonl` to read Round 7's final audit report across all 5 staged prompts (note: user is also aware full prompts in `system_prompts/` have legacy text outside `system_prompts/lean/`, which R6 flagged purely as an informational note `[I2]` — keep our staged `.proposed.md` targets focused).
2. If Round 7 did not finish or reported any new finding, apply the fix in `scratch/prompt_*.proposed.md`, re-run `_validate_proposals.py` + `CR: 0` + `audit_prompt.py --pipeline-check`, and run a fresh execution-capable blind auditor (`Model="inherit"`, zero score/prior-round leakage) until all 5 reach **`0 Alta / 0 Media / 0 Baja`**.

### Step 2: Phase 2 — `.py` Pipeline Alignment with Milestone 20 + CTA-Autonomy *(ALREADY APPLIED ON DISK — verify tests only)*
Apply these 6 code updates (all target locations verified in codebase):
1. **Canonical `recommended_modalities` validation (`compile_cta.py` & `check_cta.py`):**
   - `.agents/skills/content-to-course/compile_cta.py` (L1144–1190, L1530): define `_CANONICAL_MODALITIES = frozenset(_MODALITY_ALIASES.values())`; update `_normalize_recommended_modalities(raw_mods: Any, cid: str = "") -> List[str]` so any normalized modality not in `_CANONICAL_MODALITIES` raises `ValueError(f"[CTA-MODALITY-INVALID] Competency '{cid}': unrecognized modality '{raw}'. Allowed: {sorted(_CANONICAL_MODALITIES)}")`; pass `cid=raw_id` at L1530.
   - `.agents/skills/content-to-course/check_cta.py` (L742–798 in `_validate_competencies_rules`): define `_VALID_RECOMMENDED_MODALITIES` (the 9 canonical modalities) and validate `comp.get("recommended_modalities")` when non-`None` (must be a list of valid canonical modality strings), emitting `[CTA-MODALITY-INVALID]` errors with `cid` and optional line tag.
2. **Full M20 `invariant_canvas` validation & interpolation (`.agents/skills/content-to-course/engine/assemble.py:988-1127`):**
   - Define `VALID_CANVAS_INVARIANT_KINDS = frozenset({"point_on_curve", "point_coords", "kink_at", "slope_at", "slider_eq", "slider_range", "curves_intersect_at", "point_in_region", "inequality_state", "expr_true"})`.
   - Helper `_coerce_num_if_numeric(val: Any) -> Any`: convert pure numeric strings (`-?\d+(?:\.\d+)?`) to `int`/`float`.
   - Require every invariant's `kind` in `VALID_CANVAS_INVARIANT_KINDS` (`ValueError("[CANVAS-INVARIANT-KIND] ...")`).
   - Format `@var@` on `"expr"` as string and format + `_coerce_num_if_numeric` on `("target_x", "target_y", "x", "expected", "target_slope", "min", "max")`.
   - For `kind == "inequality_state"`, require `expected_style in ("solid", "dashed")` and `expected_shade in ("above", "below")` (`ValueError("[CANVAS-INEQUALITY] ...")`).
   - For `raw_ic.get("inequality")`, validate `curve_id` exists in declared `fixed_curves` or `interactive_curves` IDs (`ValueError("[CANVAS-INEQUALITY] ...")`), and validate optional `initial_style in ("solid", "dashed")` and `initial_shade in ("above", "below")`.
   - Recursively format `@var@` strings inside `raw_ic.get("target_state")` (coercing numeric leaves) and store in both `compiled_ic["target_state"]` and `correct_answer["target_state"]`.
3. **M20 instance invariants & KaTeX/leak guards (`.agents/skills/content-to-course/engine/invariants.py:1379-1440`):**
   - `unstructured_model`: run `validate_katex_syntax` on `phase1_variables.items[*].label`, `phase2_assumptions.options[*].{content, error_rationale}`, `phase3_formulation.options[*].{content, error_rationale}`, and `phase3_formulation.distractors[*].error_rationale`.
   - `invariant_canvas` (`cartesian`): validate invariant `kind` in `VALID_CANVAS_INVARIANT_KINDS`; validate `inequality` (`curve_id` in declared curves, valid `initial_style`/`initial_shade`) and `inequality_state` (`expected_style`/`expected_shade`); expand stem coordinate leak check (L1423) to `kind in ("point_coords", "kink_at")`; run `validate_katex_syntax` on `x_label`, `y_label`, `fixed_curves[*].label`, `interactive_curves[*].label`, `interactive_points[*].label`, `fixed_points[*].label`, `sliders[*].label`, `invariants[*].error_rationale`.
   - `invariant_canvas` (`tree`): run `validate_katex_syntax` on `nodes[*].label`, `edges[*].label`, `tree_invariants.{edge_error_rationale, info_set_error_rationale}`.
4. **`invariant_canvas` canonical diversity signature (`.agents/skills/content-to-course/check_templates.py:2793-2796`):**
   - Extend `sig_obj` for `invariant_canvas` with `inequality`, `geometry` (`fixed_points`, `interactive_points`, `segments`, `polygons`, `shaded_regions`, `sliders`), and `target_state`.
5. **Published course validator M20 parity (`src/validator/rules.py:1351-1454`):**
   - Rule `R-20`: add KaTeX checks for `unstructured_model` and `invariant_canvas` (`cartesian` + `tree`).
   - Rule `R-19`: add stem coordinate `(target_x, target_y)` leak check on `invariant_canvas` (`point_coords` and `kink_at`, excluding `fixed_points`).
6. **Update stale wording across pipeline utilities:**
   - `.agents/skills/content-to-course/shard_precheck.py:125`: `usa ver(c, v) (MC/FIB/open_symbolic) o ver(res) (MS/M20 estructurado), sin parametros opcionales.`
   - `.agents/skills/content-to-course/course_publisher.py:341-343`: replace `al menos 3 tuplas ... y la cuota de fill_in_the_blank / multiple_select` with `al menos 4 tuplas ortogonales en TEMPLATES para {cid} cubriendo ('easy', ...), ('medium', ...), ('hard', ...) con >= 2 niveles de Bloom, enunciados estructuralmente distintos y las modalidades recomendadas por el CTA (M20 / FIB / MS / MC7).`
   - `.agents/skills/content-to-course/run.py:1681`: add `M20={mod_l.get('bloom_superior_share_pct', 0.0)}%` alongside `MC7`, `FIB`, `MS`.
   - `.agents/skills/content-to-course/c2c_hook_guard.py:1812-1813`: replace `FIB/MS obligatorio` -> `modalidades alineadas al plan del CTA (M20 / FIB / MS / MC7)`.
   - `.agents/skills/content-to-course/plan_shards.py:143`: update `[FIB-NAKED]` -> `[TPL-FIB-KATEX]`.

### Step 3: Add Unit Tests & Update Synthetic `q_ic` Fixture
- Update `C:\Users\augus\.gemini\antigravity\brain\803cd022-8081-4953-9985-2371d0930e6e\scratch\_validate_proposals.py:255` (`q_ic`) to declare `"fixed_curves": [{"id": "b", "expression": "10 - 2*x", "domain": [0, 5]}]` (and check `tests/engine/test_m20_anti_descarte_and_modalities.py` for any `inequality` fixture missing `fixed_curves`).
- Create `tests/engine/test_m20_pipeline_alignment.py` testing:
  - `compile_cta` + `check_cta` 9 canonical modalities + `[CTA-MODALITY-INVALID]`
  - `assemble._assemble_invariant_canvas` (`kind`, `@var@` numeric coercion, `inequality.curve_id`/`initial_style`/`initial_shade`, `inequality_state`, `target_state` interpolation)
  - `invariants.check_instance_invariants` (`unstructured_model` KaTeX, `invariant_canvas` invalid `kind`/bad `inequality`/KaTeX/`point_coords` & `kink_at` stem leak excluding `fixed_points`)
  - `check_templates._canonical_answer_signature` diversity across `inequality`/`segments`/`polygons`/`shaded_regions`/`sliders`/`interactive_points`
  - `src/validator/rules.py` `R-20` (`unstructured_model`, `invariant_canvas`) & `R-19` (`invariant_canvas` stem leak)
  - `judge.py` M20 sanitization & answer matching across all 6 M20 modalities

### Step 4: Full Verification, Artifacts & Final Walkthrough Response
1. Run full test suite:
   ```powershell
   .\.venv\Scripts\python.exe -m pytest tests/engine/test_m20_pipeline_alignment.py tests/engine/test_m20_anti_descarte_and_modalities.py tests/pipeline/test_system_prompts_compile_clean.py tests/pipeline/test_c2c_hardening_prompts.py tests/pipeline/test_c2c_author_speedups.py tests/pipeline/test_c2c_v321_comp4_prompts.py tests/pipeline/test_c2c_v321_comp3_dispatch.py tests/pipeline/test_dispatch_scope.py tests/pipeline/test_bootstrap_and_wave_streaming.py tests/validator -q
   ```
2. Re-run `_validate_proposals.py` and `audit_prompt.py --pipeline-check --format markdown` on all 5 staged prompts (`0/0/0` + `4/4 ✅`, `CR: 0`).
3. Verify protected paths untouched:
   ```powershell
   git status --short courses/ .agents/skills/content-to-course/system_prompts/lean/ .agents/skills/content-to-course/subagent_types.json
   ```
   *(Note: `system_prompts/lean/prompt_blind_judge.md` already had a prior-session modification in `git status`; confirm none of the 5 `.proposed.md` drafts were promoted without approval and `courses/`/`subagent_types.json` are clean.)*
4. Update and read in full:
   - `C:\Users\augus\.gemini\antigravity\brain\803cd022-8081-4953-9985-2371d0930e6e\prompt_architect_audit_report.md`
   - `C:\Users\augus\.gemini\antigravity\brain\803cd022-8081-4953-9985-2371d0930e6e\walkthrough.md`
5. Deliver concise Spanish summary with clickable `file:///` links, exact verified counts, and ask user approval before promoting the 5 staged prompts to `system_prompts/lean/*.md` & `subagent_types.json`.
