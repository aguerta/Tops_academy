# DISPATCH: Stream 3A — Victory Gate Forensic Auditor (`audit_3a`)

- **Orchestrator Conversation ID (`Recipient` for `send_message`):** `d0ce22db-904e-4856-b353-59975bfb5874`
- **Teamwork Directory (ONLY allowed write target):** `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_3a_audit`
- **Artifacts to Audit:**
  - Master Plan: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/plan.md`
  - Original Request & Baseline Git Status: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/ORIGINAL_REQUEST.md`
  - Gate Status Board: `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/GATE_STATUS.md`
  - Stream 3A Specs & Handoffs:
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_3a_impl/{DISPATCH.md,handoff.md}`
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/teamwork/c2c_v33_hardening/stream_3a_impr/{DISPATCH.md,handoff.md}`
  - Audited Deliverables (READ-ONLY):
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/subagent_types.json`
    - `d:/Augusto/personal_portfolio/Tops_academy/tests/test_forensic_replay_ab30cf91.py`
    - `d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/CERTIFICACION_HARDENING_C2C_V33.md`
    - `d:/Augusto/personal_portfolio/Tops_academy/.agents/hooks.template.json`

## Victory Gate Audit Checklist
1. **Repository & Boundary Hygiene:**
   - Run `git status --short` and verify:
     - Zero stray scratch `.py` scripts in repository root or `.agents/skills/content-to-course/`.
     - Zero active `.c2c_subagent_lock.json` files anywhere inside `REPO_ROOT`.
     - `.agents/hooks.template.json` exists and is valid JSON (`"command": "python skills/content-to-course/c2c_hook_guard.py"`), while `.agents/hooks.json` is not yet created (reserved for post-audit activation).
2. **8-Vector Forensic Replay `ab30cf91` Audit (`tests/test_forensic_replay_ab30cf91.py`):**
   - Inspect all 8 vectors (`V1..V8`) line by line: confirm zero fake mocks, zero conditional skips on `V1..V8`, strict assertions on real Greene PDFs (`V1`), `0.0%` degraded math healing (`V2`), `--append` continuous IDs & base DAG (`V3`), 32 Greene competencies `10 Hab` isolated `1/shard` in Wave 1 (`V4`), `@var@` sandwich matrix + `{delta}` / `@delta@` hard block (`V5`), Zero-Disk-Mutation + `shard_fixes/C-08.py` + `[CIRCUIT BREAKER]` trip & reset (`V6`), `c2c_hook_guard.py` + `budget_guard.py` 108-turn `PLANNER_RESPONSE` + `subagent_types.json` sync (`V7`), and `crc32` uniform `A..G` shuffle + coherent Judge Pointer (`V8`).
   - Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests/test_forensic_replay_ab30cf91.py -v` and confirm `8 passed` in `< 10s`.
3. **Certification Document Audit (`reports/c2c_audits/CERTIFICACION_HARDENING_C2C_V33.md`):**
   - Verify 100% coverage of Bottlenecks `#1..#13` and `ab30cf91` Error Categories `01..12`, accurate `granularity: standard` relative density (`3–5` comps per `5–10` pages), accurate `R-16` bounds `[0.65x, 1.35x]`, and accurate `pytest` counts.
4. **Independent Full-Repository `pytest` Execution:**
   - Run `& "d:\Augusto\personal_portfolio\Tops_academy\.venv\Scripts\python.exe" -m pytest tests -q` and confirm **0 failed, 0 errors** across the entire repository!
5. Write `BRIEFING.md`, `progress.md`, and `handoff.md` inside `stream_3a_audit/`, then `send_message` starting with `PASS:: stream_3a_audit | ...` or `REJECT:: stream_3a_audit | ...`.
