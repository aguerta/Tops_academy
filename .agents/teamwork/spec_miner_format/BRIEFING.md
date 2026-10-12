# BRIEFING — 2026-10-11T01:05:00Z

## Mission
Discover and document the exact JSON schema, validation rules, LaTeX/JSON escaping pitfalls, giveaway detection criteria, and test matrix for the Top's Academy course generator.

## 🔒 My Identity
- Archetype: Specification Miner
- Roles: Format & Validator Spec Miner
- Working directory: g:\Mi unidad\Competence_analyser\.agents\teamwork\spec_miner_format
- Original parent: 84948f37-b77a-4675-a1cb-6a3b8a288462
- Milestone: Phase 1 Spec Mining Complete

## 🔒 Key Constraints
- Read-only probe; do NOT implement the production validator or generate courses.
- Only write metadata, reports, and specifications to my working directory `.agents/teamwork/spec_miner_format/`.
- Must inspect ORIGINAL_REQUEST.md, prompt_creator_exercises.md, and output_example_exercises.json.
- Identify all flaws in output_example_exercises.json (LaTeX backslash escaping, silently-valid escapes \t, \f, \n, \b, \v, \0, giveaway patterns, unescaped quotes).
- Formulate complete JSON schema & validator spec including anti-giveaway rules and test matrix.

## Current Parent
- Conversation ID: 84948f37-b77a-4675-a1cb-6a3b8a288462
- Updated: 2026-10-11T01:05:00Z

## Task Summary
- **What to analyze**: Format and validation criteria for courses, competencies, questions, graphs, hints, solutions, and anti-giveaway mechanisms.
- **Success criteria**: Comprehensive `format_spec.md` with JSON schema, validation rules, edge cases, flaw analysis of example file, and test matrix; complete `handoff.md`.
- **Interface contracts**: `ORIGINAL_REQUEST.md` (R2 and Validator Acceptance Criteria).

## Key Decisions Made
- Completed exhaustive flaw inventory of `output_example_exercises.json`: 519 syntax-invalid escapes, 366 silent control character escapes, 11 raw multiline string blocks, 4 unescaped quote occurrences.
- Quantitative verification of giveaway pattern: 66.7% MC items have correct option as longest (limit 25%), 33.3% as shortest (limit 25%).
- Designed complete Draft-07 JSON Schema covering Course root, Competencies/Units, Questions, Options, Hints, and declarative vector Graph models.
- Formulated two-pass validation architecture and complete 16-rule inventory (R-01 to R-16) with exit codes and error codes.
- Formulated SymPy / mathjs algebraic equivalence grading criteria.
- Designed 28-fixture test matrix covering all R2 acceptance criteria.
- Produced `format_spec.md` and structured 5-component `handoff.md`.

## Artifact Index
- `DISPATCH.md` — Original task dispatch
- `BRIEFING.md` — Situational memory
- `progress.md` — Liveness & progress tracker
- `format_spec.md` — Authoritative specification document
- `handoff.md` — 5-component handoff report
- `inspect_example.py` — Backslash and escape inspection script
- `flaw_inventory.py` — Detailed flaw categorization script
- `analyze_options.py` — Option length and giveaway analysis script
- `prototype_detector.py` — Two-pass LaTeX corruption detector prototype
- `probe_sympy.py` — SymPy mathematical equivalence verification script
