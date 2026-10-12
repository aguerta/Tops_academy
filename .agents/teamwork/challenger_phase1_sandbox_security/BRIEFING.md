# BRIEFING — 2026-10-11T21:45:00Z

## Mission
Adversarial empirical stress testing and security audit of `sandbox.py` (AST whitelist, dunder protection, timeout/resource limits, determinism, math libraries, and sandbox escapes) issuing an empirical gate verdict.

## 🔒 My Identity
- Archetype: challenger
- Roles: critic, specialist
- Working directory: g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_phase1_sandbox_security
- Original parent: 8c6e51b9-04fd-4a8c-a9ab-21b3a1985725
- Milestone: phase1_sandbox_security
- Instance: 1 of 1

## 🔒 Key Constraints
- Review-only — do NOT modify implementation code (`sandbox.py` or skill engine)
- Empirical verification: find bugs by writing and executing tests — if not reproduced empirically, it does not count
- Layout compliance: `.agents/teamwork/` must contain only metadata (no code/tests)
- Gate verdict: issue an explicit verdict (APPROVE or REQUEST_CHANGES) with concrete evidence

## Current Parent
- Conversation ID: 8c6e51b9-04fd-4a8c-a9ab-21b3a1985725
- Updated: 2026-10-11T21:45:00Z

## Review Scope
- **Files to review**: `.agents/skills/content-to-course/engine/sandbox.py`, `.agents/teamwork/ORIGINAL_REQUEST.md` (R3: Sandbox Whitelist & Security)
- **Interface contracts**: AST whitelist validation (`validate_code_ast`), sandbox isolation (`execute_sandbox_instance`, `execute_sandbox_batch`), timeout enforcement (2.0s), determinism via RNG, math libraries (`math`, `fractions`, `statistics`, `sympy`, `numpy`, `scipy.stats`, `random`)
- **Review criteria**: Empirical security against arbitrary code execution, escapes, resource exhaustion, and library validity

## Key Decisions Made
- Confirmed standard restrictions pass (39 tests).
- Confirmed legitimate math libraries and RNG determinism pass (2 tests).
- Discovered and empirically proved 5 critical/high security bypasses + 1 RNG non-determinism issue + 1 cold-start timeout issue (6 empirical attack tests).
- Gate Verdict: REQUEST_CHANGES. Changes required in `sandbox.py` to patch attribute traversal, submodule leaks, engine re-exports, and import overhead.

## Artifact Index
- `g:\Mi unidad\Competence_analyser\tests\test_sandbox_adversarial.py` — 47 automated empirical adversarial tests (100% passing reproduction)
- `g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_phase1_sandbox_security\handoff.md` — formal 5-component handoff report

## Attack Surface
- **Hypotheses tested**:
  1. Direct banned module/builtin import: BLOCKED by AST (PASS).
  2. Submodule attribute traversal via allowed modules (`fractions.sys`, `statistics.sys`): VULNERABLE (arbitrary code execution confirmed).
  3. Re-export traversal via allowed engine module (`import engine.sandbox as es`): VULNERABLE (`es.subprocess.run` arbitrary host command execution confirmed).
  4. Dynamic dunder traversal via `fractions.operator.attrgetter`: VULNERABLE (retrieved `os.system` via `__subclasses__` and `__globals__`).
  5. Native memory / ctypes access via `numpy.ctypeslib.ctypes`: VULNERABLE.
  6. Unseeded global random module: VULNERABLE (template using `random.randint` is non-deterministic across identical seeds).
  7. Cold-start import overhead of `sympy` + `scipy` causing false timeouts on 2.0s limit: CONFIRMED (~1.92s import time).
- **Vulnerabilities found**: 5 critical/high security bypasses, 1 non-determinism defect, 1 cold-start timeout flaw.
- **Untested angles**: All major vectors empirically tested and proven in `test_sandbox_adversarial.py`.

## Loaded Skills
- **Source**: g:\Mi unidad\Competence_analyser\.agents\skills\content-to-course\SKILL.md
- **Local copy**: g:\Mi unidad\Competence_analyser\.agents\teamwork\challenger_phase1_sandbox_security\SKILL_content-to-course.md
- **Core methodology**: Conversion of academic course materials into interactive Top's Academy courses using strict JSON contracts and sandboxed Python execution
