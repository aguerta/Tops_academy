# Handoff Report: Test Suites, Sandbox Security, Course Status, and Verification Architecture

**Agent**: `explorer_survey_tests`  
**Working Directory**: `g:\Mi unidad\Competence_analyser\.agents\teamwork\explorer_survey_tests`  
**Date**: 2026-10-11T20:50:00Z  
**Recipient**: Parent Orchestrator (`8c6e51b9-04fd-4a8c-a9ab-21b3a1985725`)  

---

## 1. Observation

1. **Current Test Suites**:
   - `python -m pytest tests/test_validator.py tests/test_platform.py -v`:
     - Result: `114 passed in 18.14s`.
     - `tests/test_validator.py` (521 lines, 64 tests) imports solely from `src/validator/` and tests 28 fixtures (`courses/fixtures/`).
     - `tests/test_platform.py` (281 lines, 50 tests) executes `tests/test_math_adversarial_suite.mjs` via Node and tests server endpoints in `run_platform.py`.
     - Ripgrep search across `tests/` confirmed that `from batch_generator`, `from cta_analyzer`, `from pdf_extractor`, `from verifier`, `from repair_loop`, and `from course_publisher` appear **only** in `tests/test_skill.py`.
   - `python -m pytest tests/test_skill.py -v`:
     - Result: `27 passed in 20.20s`.
     - Lines 36–42 import legacy modules from `.agents/skills/content-to-course/`.
     - Lines 280–425 test domain-specific PDE/EDO logic (`test_blind_solver_cobb_douglas_degree`, `test_blind_solver_lagrange_first_order_pde`, `test_characteristic_roots_hyperbolic_parabolic_elliptic`, `test_cta_analyzer_full_taxonomy_decomposition`).

2. **Existing Course Files & Validator Status**:
   - `python -m validator.cli courses/pde_course.json --strict`:
     - Result: `VALID: Course 'pde_course' passed all 16 validation rules (strict mode).`
     - Metrics: 21 competencies (7 Fact, 6 Concept, 8 Skill), 500 questions.
     - SHA-256: `3A8D4C0D23CA9FCFA8A2B7E05765725E1C3B71391DDB74011667850256694192`.
   - `python -m validator.cli courses/sistemas_edos.json --strict`:
     - Result: `VALID: Course 'sistemas_edos' passed all 16 validation rules (strict mode).`
     - Metrics: 20 competencies (8 Fact, 5 Concept, 7 Skill), 470 questions.
     - SHA-256: `6AFAFB088AEABF0729A4223DE8F28BEC80D958395C5157C56D592F4B9D3FCB06`.

3. **Input Content Profile (`content/estadistica3_Cano/`)**:
   - `EST3_LEC01_26_2.pdf`: 297,245 B, 13 pages, Beamer LaTeX, text layer contains 5,243 chars with corrupted diacritics (`Regresi´on`, `Te´orico`, `ˆβ`).
   - `EST3_LEC02_26_2.pdf`: 311,530 B, 26 pages, Beamer LaTeX, text layer contains 12,749 chars.
   - `EST3_LEC03_26_2.pdf`: 305,378 B, 29 pages, Beamer LaTeX, text layer contains 19,406 chars.
   - `Stats3 10-10.pdf`: 3,560,906 B, 9 pages, OneNote export vector ink with only 381 characters of metadata across all pages. Contains numerical exercise on page 1 ($X=\begin{bmatrix}1&1\\1&2\\1&3\end{bmatrix}$, $Y=(3,5,6)^T$, $P$, $\hat{Y}$, $e$).
   - `stats 3 3-10.png`: 697,520 B, RGBA raster image, dimensions **5941 × 3327 px** (exceeds 2500 px). Contains handwritten mathematical derivations and an EViews regression table ($R^2=0.9967$, $F=459.75$, $p=0.0000$).
   - Total vision workload: 68 Beamer slides + 9 handwritten pages + (6 tiles + 1 overview) = 84 vision transcription items.

4. **Sandbox & Platform Implementation Realities**:
   - Operating system is Windows (`win32`, Python 3.12.10). POSIX signals (`signal.SIGALRM`) are unavailable.
   - AST analysis of template code can statically intercept unwhitelisted imports (`os`, `sys`, `subprocess`, `socket`, `urllib`), prohibited builtins (`open`, `eval`, `exec`, `__import__`), and dunder attributes (`__class__`, `__dict__`, etc.).
   - Runtime timeout (2.0s per instance) and memory limits require isolated worker execution via `subprocess.run` or `ProcessPoolExecutor`.
   - `platform/src/utils/mathEquivalence.ts` currently defaults to `0.001` tolerance, does not convert comma decimals (`0,8333`), and expects target to have `expression` rather than `canonical_algebraic` or `value`.

---

## 2. Logic Chain

1. **Test Decoupling**:
   - Observation 1 demonstrates that only `tests/test_skill.py` imports from `.agents/skills/content-to-course/`.
   - Therefore, completely rewriting `tests/test_skill.py` to test the new generic engine will have zero impact on `tests/test_validator.py` and `tests/test_platform.py`.
   - Both `test_validator.py` and `test_platform.py` will continue to pass without modifying their code.

2. **Course Immutability**:
   - Observation 2 verifies that `pde_course.json` and `sistemas_edos.json` are currently valid under strict mode.
   - Their SHA-256 hashes establish a cryptographic invariant: any accidental drift or modification during Phase 1 refactoring will be immediately detected.

3. **Ingestion & Tiling Necessity**:
   - Observation 3 shows `Stats3 10-10.pdf` has essentially no text layer (381 chars), and `stats 3 3-10.png` has a resolution of 5941 × 3327 px with small handwritten symbols.
   - Therefore, standard text extraction cannot capture this content. Pure vision transcription and 3×2 image tiling with 10% overlap are mandatory to avoid information loss.

4. **Sandbox Architecture on Windows**:
   - Observation 4 shows that timeout handling cannot rely on UNIX signals.
   - Therefore, a dual-layer sandbox is required:
     1. Static AST layer: parses the code and rejects prohibited nodes (`Import`, `Name`, `Attribute`, `Call`) in < 1 ms before process execution.
     2. Runtime subprocess layer: runs `generate(rng)` with a fixed seed in an isolated worker process terminated after 2.0s via `subprocess` or `ProcessPoolExecutor`.

5. **Test Plan & Phase 1 Freeze**:
   - The requirements specify a strict sequential 2-phase protocol.
   - By organizing the verification into 6 formal gates (Platform, Validator, Legacy Courses, Generic Skill Suite, Anti-Overfitting Grep, and Freeze Baseline), the team can guarantee 100% verification before freezing code.

---

## 3. Caveats

- **External Node Tooling**: `tests/test_platform.py` relies on Node.js running `tests/test_math_adversarial_suite.mjs`. When Component 8 updates `mathEquivalence.ts` and `test_math_adversarial_suite.ts`, the bundle must be rebuilt to `.mjs` so the Python test picks up the changes.
- **Vision Execution in Phase 2**: The transcription of the 84 image units is an LLM vision subagent task scheduled for Phase 2. In Phase 1, `ingest.py` and `check_pages.py` are verified using mocked and real image tiling fixtures, but the full 84-image transcription takes place in Phase 2.

---

## 4. Conclusion

1. **Safe Rewrite**: `tests/test_skill.py` can be refactored safely into 6 modular test classes (32 test cases) covering AST sandbox security, deterministic seeding, 2.0s timeout, duplicate rejection, contract validation (`CTA-D1/D2`, `TPL-D1..D4`), image tiling, and few-shot EDP/EDO regression.
2. **Existing Integrity**: `tests/test_validator.py` and `tests/test_platform.py` remain untouched and 100% passing.
3. **Course Baseline**: `pde_course.json` and `sistemas_edos.json` are valid and locked with SHA-256 hashes.
4. **Phase 1 Freeze Protocol**: The 6-Gate verification procedure provides complete, deterministic coverage to freeze code prior to Phase 2 course generation.

---

## 5. Verification Method

To independently verify all findings in this report, execute the following commands:

1. **Verify Existing Tests**:
   ```powershell
   python -m pytest tests/test_validator.py tests/test_platform.py -v
   python -m pytest tests/test_skill.py -v
   ```
   *Expected*: All tests pass (114 in validator/platform, 27 in skill).

2. **Verify Legacy Courses Strict Mode**:
   ```powershell
   python -m validator.cli courses/pde_course.json --strict
   python -m validator.cli courses/sistemas_edos.json --strict
   ```
   *Expected*: Exit code 0 on both courses.

3. **Verify Course SHA-256 Hashes**:
   ```powershell
   powershell -Command "Get-FileHash courses/*.json | Format-List"
   ```
   *Expected*:
   - `pde_course.json`: `3A8D4C0D23CA9FCFA8A2B7E05765725E1C3B71391DDB74011667850256694192`
   - `sistemas_edos.json`: `6AFAFB088AEABF0729A4223DE8F28BEC80D958395C5157C56D592F4B9D3FCB06`

4. **Verify Input Assets & Dimensions**:
   ```powershell
   python -c "import fitz, PIL.Image; print('Stats3 pages:', len(fitz.open('content/estadistica3_Cano/Stats3 10-10.pdf'))); print('PNG size:', PIL.Image.open('content/estadistica3_Cano/stats 3 3-10.png').size)"
   ```
   *Expected*: 9 pages for `Stats3 10-10.pdf`, `(5941, 3327)` for `stats 3 3-10.png`.
