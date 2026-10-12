# BRIEFING — 2026-10-11T00:58:00Z

## Mission
Build the "Top's Academy" platform, exercise-bank validator, content-to-course Antigravity skill, and end-to-end demo meeting all acceptance criteria.

## 🔒 My Identity
- Archetype: teamwork_preview_orchestrator
- Roles: orchestrator, user_liaison, human_reporter, successor
- Working directory: g:\Mi unidad\Competence_analyser\.agents\teamwork\orchestrator
- Original parent: Sentinel / Parent (7e638524-1a06-4e86-8bac-6392dd5a5ea4)
- Original parent conversation ID: 7e638524-1a06-4e86-8bac-6392dd5a5ea4

## 🔒 My Workflow
- **Pattern**: Project Pattern (with Dual Track: Implementation + E2E Testing)
- **Scope document**: g:\Mi unidad\Competence_analyser\PROJECT.md
1. **Decompose**:
   - Survey (Step 0): Spawn 3 Explorers / Spec Miners to map authoritative assets (reference screenshots, system prompts, sample PDF, and existing codebase).
   - Establish PROJECT.md with architecture, feature inventory, code layout, milestones, interface contracts.
   - Decompose into Milestones (R2 Validator & Format, R1 Practice Platform, R3 Antigravity Skill, R4 Demo & Audits) + E2E Testing Track.
2. **Dispatch & Execute**:
   - Dispatch sub-orchestrators / specialist subagents per milestone following the Explorer -> Worker -> Reviewer -> Challenger -> Auditor cycle.
3. **On failure**:
   - Retry -> Replace -> Skip (except auditor) -> Redistribute -> Redesign.
4. **Succession**:
   - When spawn count >= 16 and pending subagents complete, write handoff.md, cancel crons, spawn successor.
- **Work items**:
  0. Survey phase [in-progress]
  1. E2E Testing Track (harness, automated headless browser tests, validator tests) [pending]
  2. R2: Exercise Bank Format, Schema & Validator CLI + automated tests [pending]
  3. R1: Top's Academy-style Practice Platform web app [pending]
  4. R3: Content-to-Course Antigravity Skill (.agents/skills/) [pending]
  5. R4: End-to-End Demo (PDE PDF processing + Demo Course conversion + Question Audits + Visual Fidelity Review) [pending]
- **Current phase**: 0 (Survey)
- **Current focus**: Step 0 Survey across codebase, references, and specs

## 🔒 Key Constraints
- NEVER write, modify, or create source code files directly.
- NEVER run build/test commands yourself — require workers to do so.
- NEVER investigate or explore the problem at the code level — dispatch Explorers for technical investigation.
- File-editing tools ONLY for metadata/state files (.md) in .agents/teamwork/ and project scope documents.
- Audit Enforcement: BINARY VETO on integrity violations.
- Windows environment: use npm.cmd/npx.cmd (PowerShell blocks npm.ps1).
- Google Drive sync awareness.
- Never reuse a subagent after it has delivered its handoff — always spawn fresh.
- Pass 100% acceptance criteria before reporting completion.

## Current Parent
- Conversation ID: 7e638524-1a06-4e86-8bac-6392dd5a5ea4
- Updated: 2026-10-11T00:58:00Z

## Key Decisions Made
- Project pattern selected with survey phase (Step 0) to catalog reference screenshots, system prompts, sample PDF, and existing files.

## Team Roster
| Agent | Type | Work Item | Status | Conv ID |
|-------|------|-----------|--------|---------|
| explorer_ui_survey | teamwork_preview_explorer | Survey UI references & R1 spec | completed | fe6671ab-08a4-4743-961a-8c59911c084f |
| spec_miner_format | teamwork_preview_spec_miner | Survey format, schema, LaTeX & validator rules | completed | db4e3a2b-9b21-4f55-9d06-d719174e0f0a |
| spec_miner_skill | teamwork_preview_spec_miner | Survey competence analysis, PDF & skill pipeline | completed | b884c09d-995a-4558-87cf-d84993a5cec3 |
| worker_m1_validator | teamwork_preview_worker | Implement M1 Format Validator & fixtures | completed | fe5bd590-54be-4a41-84f3-2c593c771f36 |
| test_writer_e2e | teamwork_preview_test_writer | Implement E2E Test Suite & TEST_INFRA.md | completed | 26fb541c-d73c-4a32-a27e-5e68798b7678 |
| reviewer_m1_1 | teamwork_preview_reviewer | Review M1 Validator & Fixtures | completed | 9443abaf-8863-4c6f-bc96-42ce692caafb |
| reviewer_m1_2 | teamwork_preview_reviewer | Review M1 Code Quality & CLI | completed | 01562930-f595-4723-b95d-b39b1d2e2d99 |
| challenger_m1_1 | teamwork_preview_challenger | Adversarial testing M1 Validator | completed | e7bf97b3-5205-418c-a348-4d93bbb94cc6 |
| challenger_m1_2 | teamwork_preview_challenger | Empirical stress testing M1 Validator | completed | 39829f65-44a2-4c70-8b24-c2f022904b56 |
| auditor_m1_1 | teamwork_preview_auditor | Forensic Integrity Audit M1 | completed | e2964196-161f-4344-862c-e0e11d08684f |
| explorer_m1_fix_lexical | teamwork_preview_explorer | Lexical corruption remediation plan | completed | dec6b8c0-8143-4e39-a89c-9c22c58f3d3b |
| explorer_m1_fix_semantic | teamwork_preview_explorer | Semantic/schema remediation plan | completed | 86049328-1352-429f-ac01-a6048475b78f |
| explorer_m1_fix_packaging | teamwork_preview_explorer | Packaging & CLI remediation plan | completed | 3b200a65-7004-4a2e-a429-9e6af3ff4c25 |
| worker_m1_patch | teamwork_preview_worker | Implement M1 remediations across validator | completed | dce96c91-5d42-4e8d-b526-242f082bf409 |
| reviewer_m1_2_1 | teamwork_preview_reviewer | Review patched validator & R2 rules | in-progress | 1c8e1b50-8254-4e6b-a15b-b52f1278f4dc |
| reviewer_m1_2_2 | teamwork_preview_reviewer | Review packaging & CLI behavior | in-progress | 9c46475d-86f2-4786-be99-2e3fe21fbc85 |
| challenger_m1_2_1 | teamwork_preview_challenger | Adversarial stress test patched validator | in-progress | f27366e6-6797-4ab6-96b3-896bb2d9c5f9 |
| challenger_m1_2_2 | teamwork_preview_challenger | Empirical battery verification | in-progress | f4b05d7f-f74e-4ff8-b4bf-4e1da5924b70 |
| auditor_m1_2_1 | teamwork_preview_auditor | Forensic Integrity Audit M1 Iter 2 | in-progress | 0b836a09-4125-4737-aa65-834f5b322925 |

| worker_m2_platform | teamwork_preview_worker | Build Top's Academy Practice Platform web app | in-progress | 123fd3f9-7789-4941-b786-0b6f0581f9c8 |

## Succession Status
- Succession required: no (orchestrator is top-level singleton in this runtime)
- Active specialists spawned: 20
- Pending subagents: 123fd3f9-7789-4941-b786-0b6f0581f9c8

## Active Timers
- Heartbeat cron: 84948f37-b77a-4675-a1cb-6a3b8a288462/task-281
- Safety timer: none

## Artifact Index
- g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md — Authoritative specifications and AC
- g:\Mi unidad\Competence_analyser\.agents\teamwork\orchestrator\DISPATCH.md — Incoming dispatch record
- g:\Mi unidad\Competence_analyser\.agents\teamwork\orchestrator\BRIEFING.md — Persistent working memory
- g:\Mi unidad\Competence_analyser\.agents\teamwork\orchestrator\progress.md — Progress and liveness heartbeat
- g:\Mi unidad\Competence_analyser\.agents\teamwork\orchestrator\plan.md — Detailed execution plan
- g:\Mi unidad\Competence_analyser\.agents\teamwork\orchestrator\context.md — Context and requirements index
