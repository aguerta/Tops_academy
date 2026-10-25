# PROGRESS: Stream 2B — Prompts & Skill Hardening v3.3 (`impr_2b`)

**Author:** Stream 2B Improver (`impr_2b`)  
**Status:** In Progress / Completed Verification  
**Date:** 2026-10-24  
**Teamwork Directory:** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_2b_impr`

---

## Task Progress Checklist

- [x] **Pre-Flight Scrutiny & Briefing:**
  - Audited Implementer's delivery and verified 100% genuine implementation.
  - Verified no architectural blockers.
  - Documented plan in `stream_2b_impr/BRIEFING.md`.

- [x] **Task 1: `compile_shard.py` Read Prohibition Parity:**
  - Updated `prompt_shard_author.md` (Full + Lean) to explicitly prohibit reading `.agents/skills/content-to-course/compile_shard.py` with `view_file` / `read_file` (matching `c2c_hook_guard.py`).
  - Clarified that `compile_shard.py` is ONLY executed via `run_command` using the worker's `compile_cmd`.
  - Maintained exact path string for `test_anti_cheat_and_introspection_policy`.

- [x] **Task 2: Blind Judge Turn-Count Clarity:**
  - Harmonized `prompt_blind_judge.md` (Full + Lean) with unequivocal turn contracts:
    - Inline Mode (`--no-pointer`, Zero-Warmup In-Prompt Payload): strictly 1 turn (`RESOLUCIÓN EN 1 SOLO TURNO`).
    - Harmonized Pointer Mode (`pointer=True`): 2 turns exact (Turn 1: `view_file` on `work/dispatch/items/judge_XX.json`; Turn 2: `write_file(Overwrite=True)` without `ArtifactMetadata` + `send_message` / text `DONE: <output_path>`).
  - Preserved all backward-compatibility keyword anchors.

- [x] **Task 3: Lean Prompt Byte Headroom:**
  - Tightened `lean/prompt_shard_author.md` to **4,622 bytes** (strictly `<= 4,750` bytes, providing 498 bytes of headroom under the 5,120-byte hard limit).
  - Maintained all mandatory tokens: complete runnable `@var@` Python example, `stem_variants`, `shard_fixes/`, `ArtifactMetadata` prohibition, and read bans.

- [x] **Task 4: Full End-to-End Dry-Run Validation (`check_single_template`):**
  - Expanded `tests/test_prompts_contract_alignment.py` to run `check_single_template` from `check_templates.py` on all 3 extracted template examples (Full H-01, Full H-02, Lean H-01) with 50 dry-run seeds.
  - Verified strict `assert errors == []` on 100% of instances.
  - Added explicit test for `compile_shard.py` read prohibition parity.
  - Added explicit test for blind judge 2-turn pointer contract.
  - Added explicit test for author lean prompt byte headroom (`<= 4,750` bytes).
  - All 12/12 tests in `test_prompts_contract_alignment.py` PASSED in 0.72s.
