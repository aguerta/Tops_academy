# BRIEFING — 2026-10-11T12:09:00Z

## Mission
Adversarial empirical testing of anti-giveaway guarantees on >=40 multiple-choice questions from `courses/pde_course.json` using a blind-guess protocol (target <= 30.0% guess accuracy).

## 🔒 My Identity
- Archetype: EMPIRICAL CHALLENGER
- Roles: critic, specialist
- Working directory: g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_m4_blind_guess
- Original parent: 7609f41d-901b-455e-a8d4-9ddd5b18b728
- Milestone: M4
- Instance: 1 of 1

## 🔒 Key Constraints
- Review-only — do NOT modify implementation code or course json directly
- Empirical verification required: write and execute test scripts directly, no unverified claims
- Strip stems, context, hints, solutions, and misconception warnings completely
- Shuffle 7 options per item
- Adversarial inspection for psychometric cues (length, formatting, asymmetric detail, qualifier words, mathematical cues)
- Target: <=30.0% blind-guess accuracy across >=40 sampled items

## Current Parent
- Conversation ID: 7609f41d-901b-455e-a8d4-9ddd5b18b728
- Updated: 2026-10-11T12:00:00Z

## Review Scope
- **Files to review**: `courses/pde_course.json`, `.agents/skills/content-to-course/batch_generator.py`
- **Interface contracts**: `PROJECT.md`, `.agents/teamwork/ORIGINAL_REQUEST.md`
- **Review criteria**: Anti-giveaway guarantees, blind-guess rate <= 30%, distractor plausibility and symmetry

## Attack Surface
- **Hypotheses tested**:
  * Can an adversarial test-taker guess correct answers without question stems at a rate >30%? Confirmed (78% on N=50 sample, 66% on N=250 course population).
  * Do options have asymmetric qualifier cues? Confirmed: unilateral append of `", en todo el dominio."` to correct answer in `batch_generator.py` line 404 leaks the answer in 42.8% of items.
  * Are distractor lengths uniformly distributed around correct answer? Fails: correct option is 2nd longest in 43.2% of items and shortest in 0% of items.
- **Vulnerabilities found**:
  * Critical psychometric giveaway: `", en todo el dominio."` appended exclusively to `c_clean` in `batch_generator.py`.
  * Semantic computation giveaway: verification items include `= 0` for correct answer and `\neq 0` for distractors.
- **Untested angles**: Full re-test pending code repair by worker.

## Loaded Skills
- **Source**: g:\Mi unidad\Competence_analyser\.agents\skills\content-to-course\SKILL.md
- **Local copy**: g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_m4_blind_guess\SKILL_content_to_course.md
- **Core methodology**: Ingests PDFs, extracts competencies via CTA, generates exercises with psychometric anti-giveaway guarantees (length/format/complexity symmetry, no negative distractors, 7 plausible options), verifies keys via SymPy/blind solver tiers.

## Key Decisions Made
- Deterministically sampled 50 items (seed=42) and tested both sample and full population (250 items).
- Empirically documented failure of the <=30% blind-guess test.
- Issuing `Verdict: REQUEST_CHANGES` in `handoff.md`.

## Artifact Index
- `DISPATCH.md` — Inbound instructions
- `BRIEFING.md` — Situational awareness and identity
- `progress.md` — Liveness heartbeat and step tracking
- `handoff.md` — Final 5-component handoff report with verdict
- `tests/test_blind_guess_empirical.py` — Reproducible empirical test harness
- `tests/blind_guess_empirical_results.json` — Complete JSON test data
- `tests/table_output.md` — Formatted 50-item audit log
