# BRIEFING — 2026-10-12T06:12:00Z

## Mission
Refactor and optimize the `content-to-course` educational generation pipeline and Top's Academy practice platform per R1-R6 in ORIGINAL_REQUEST.md.

## 🔒 My Identity
- Archetype: teamwork_preview_orchestrator
- Roles: orchestrator, user_liaison, human_reporter, successor
- Working directory: g:\Mi unidad\Competence_analyser\.agents\teamwork\teamwork_preview_orchestrator_1
- Original parent: Sentinel
- Original parent conversation ID: 8d2e77ed-9bd1-4a71-a0a4-87db403e5506

## 🔒 My Workflow
- **Pattern**: Project
- **Scope document**: g:\Mi unidad\Competence_analyser\PROJECT.md
1. **Decompose**: Survey codebase, decompose R1-R6 into discrete milestones, verify feature inventory.
2. **Dispatch & Execute**:
   - Delegate (sub-orchestrator) per milestone and dual-track E2E Testing Orchestrator. Direct iteration loop within sub-milestones (Explorer -> Worker -> Reviewer -> Challenger -> Auditor -> Gate).
3. **On failure**:
   - Retry -> Replace -> Skip -> Redistribute -> Redesign -> Escalate.
4. **Succession**: At 16 spawns, write handoff.md, spawn successor.
- **Work items**:
  1. Survey & codebase mapping [in-progress]
  2. E2E Testing Track [pending]
  3. Milestone M1: Pipeline Ingestion & CTA Sequencing (R1) [pending]
  4. Milestone M2: Shard Generation & Variability Validation (R2) [pending]
  5. Milestone M3: Stem Variants & Question Diversity (R3) [pending]
  6. Milestone M4: Stratified Blind Judge & Key Normalization (R4) [pending]
  7. Milestone M5: Practice UI 3-Strikes Safeguard (R5) [pending]
  8. Milestone M6: Automated Test Suite & Multi-Core Validation (R6) [pending]
  9. Final Milestone: 100% E2E tests pass & Adversarial Hardening [pending]
- **Current phase**: 0 (Survey)
- **Current focus**: Surveying codebase and specifications across R1-R6

## 🔒 Key Constraints
- NEVER write, modify, or create source code files directly.
- NEVER run build/test commands yourself — require workers to do so.
- NEVER investigate or explore the problem at the code level — dispatch Explorers for technical investigation. Your analysis is limited to reading agent reports, gate verdicts, and state files to make dispatch decisions.
- You MAY use file-editing tools ONLY for metadata/state files (.md) in your .agents/teamwork/ folder.
- Never reuse a subagent after it has delivered its handoff — always spawn fresh.
- Binary veto on Forensic Auditor integrity violations.

## Current Parent
- Conversation ID: 8d2e77ed-9bd1-4a71-a0a4-87db403e5506
- Updated: 2026-10-12T06:10:46Z

## Key Decisions Made
- Initialized Project Orchestrator for R1-R6 pipeline refactor and optimization.
- Initiating Survey phase with 3 parallel explorers/spec miners to map current codebase implementation vs R1-R6 requirements.

## Team Roster
| Agent | Type | Work Item | Status | Conv ID |
|-------|------|-----------|--------|---------|
| explorer_survey_1 | teamwork_preview_explorer | Survey R1 & R2 | in-progress | 404dbed2-99be-4b57-b954-9a794b4b133b |
| explorer_survey_2 | teamwork_preview_explorer | Survey R3 & R4 | in-progress | 66128057-5de7-464b-abb8-4e66f58393b3 |
| spec_miner_survey_3 | teamwork_preview_spec_miner | Survey R5 & R6 | in-progress | 662b13b7-89d1-4098-a9f8-f1bab69b92c0 |

## Succession Status
- Succession required: no
- Spawn count: 3 / 16
- Pending subagents: 404dbed2-99be-4b57-b954-9a794b4b133b, 66128057-5de7-464b-abb8-4e66f58393b3, 662b13b7-89d1-4098-a9f8-f1bab69b92c0
- Predecessor: none
- Successor: not yet spawned

## Active Timers
- Heartbeat cron: not started
- Safety timer: none
- On succession: kill all timers before spawning successor
- On context truncation: run `manage_task(Action="list")` — re-create if missing

## Artifact Index
- g:\Mi unidad\Competence_analyser\.agents\teamwork\ORIGINAL_REQUEST.md — Authoritative User Request
- g:\Mi unidad\Competence_analyser\PROJECT.md — Global architecture, feature inventory, milestones
- g:\Mi unidad\Competence_analyser\.agents\teamwork\teamwork_preview_orchestrator_1\progress.md — Liveness & status tracking
