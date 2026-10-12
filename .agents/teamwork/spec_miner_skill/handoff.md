# Handoff Report: Competence Analysis & Skill Pipeline Spec Miner

**Agent Folder**: `.agents/teamwork/spec_miner_skill`  
**Deliverable**: `skill_spec.md`  
**Parent Agent**: `orchestrator` (`84948f37-b77a-4675-a1cb-6a3b8a288462`)  
**Date**: 2026-10-11  
**Status**: Hard Handoff (Task Complete)  

---

## 1. Observation

1. **System Requirements & Acceptance Criteria**:
   - `ORIGINAL_REQUEST.md`: Lines 30–32 define Requirement **R3. Content-to-course Antigravity skill**:
     > "A workspace skill (discoverable by Antigravity under `.agents/skills/`) that, when the user provides a PDF, automatically: extracts the content (including math), produces and saves the competence analysis, generates the exercise bank grounded in both the analysis and the original content (≥30 questions per Skill competency, ≥20 per Fact/Concept competency; mix of all three types and difficulties; graphs where relevant; exercise text in the source content's language), checks the correctness of answers through a step independent of generation, validates with the R2 validator and repairs until it passes, publishes the course to the platform's courses folder, and tells the user how to open it. Correct answers must never be identifiable without knowing the subject: distractors must be plausible and homogeneous with the correct option in length, form, grammar, specificity and level of detail... It must cope with large courses (e.g. 15+ competencies × 30 questions) without truncated or malformed output."
   - Lines 58–62 define Skill Acceptance Criteria:
     - `SKILL.md` under `.agents/skills/` documenting full pipeline.
     - Sample PDF execution producing saved competence analysis and valid course passing validator with $\ge 30$ questions per Skill and $\ge 20$ per Fact/Concept.
     - Independent reviewer audit of $\ge 40$ questions: $\ge 95\%$ accuracy.
     - Blind-guess test: $\ge 40$ MC items without stem guessed in $\le 30\%$ (chance $\approx 14\%$).
     - Demo course derived from `output_example_exercises.json` passing validator and playable.

2. **Reference Input PDF**:
   - Path: `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf`.
   - Tool execution (`fitz.open()`): 25 pages/slides, Beamer presentation in Spanish, author Mgtr. Saúl Elguera (UNMSM, Facultad de Ciencias Económicas, Matemática para Economía IV 2026 - II).
   - Core topics: Euler's homogeneous function theorem ($f(t\mathbf{x}) = t^n f(\mathbf{x})$, Cobb-Douglas $A K^\alpha L^\beta$, factor exhaustion); PDE definitions, order, degree, linearity vs quasilinearity; Solution verification ($U = e^{x-y}$ in $U_x+U_y=0$); Method of separation of variables (1D heat equation $U_y - 4 U_{xx} = 0$, separation constant $\lambda$); Method of characteristics for 1st-order PDEs ($\frac{dx}{ds}=a, \frac{dy}{ds}=b, \frac{dU}{ds}=c$); Charpit-Lagrange auxiliary symmetric systems ($\frac{dx}{a}=\frac{dy}{b}=\frac{dU}{c}$, solutions $\phi(m,n)=0$, 5 worked examples including constant coefficients, separable, Lagrange multipliers, substitutions); Cauchy problems with initial curves ($-y u_x + x u_y = u^2+1, u(x,0)=x^2$, parametric inversion $t=\arctan(y/x), m^2=x^2+y^2$); 2nd-order constant coefficient PDEs ($a U_{xx} + b U_{xy} + c U_{yy} = d$, characteristic equation $an^2+bn+c=0$, discriminant $\Delta$, hyperbolic $\Delta>0$, parabolic $\Delta=0$, elliptic $\Delta<0$); Differential operator factorization and cascade reduction ($(D_x - r_1 D_y)(D_x - r_2 D_y) U = d(x,y)$, worked example $U_{xx}+U_{xy}-6U_{yy}=x+y$).

3. **CTA Guide & Output Example**:
   - `system_prompts/prompt_competence_analyser.md`: Instructs Cognitive Task Analysis based on Knowledge Triad (Facts [H], Concepts [C], Skills [Hab]), Expert Blindness (omitted steps, algebraic traps, domain boundaries), Cognitive Load/Fluency overlearning (Top's Academy automation seeds), and Transfer Bridges.
   - `system_prompts/output_example_competences.md`: 228-line reference demonstration of CTA on 2D ODE dynamic macroeconomic models.

4. **Flaws in `system_prompts/output_example_exercises.json`**:
   - Python `json.load()` failed verbatim with `JSONDecodeError: Invalid \escape: line 19 column 113 (char 767)`.
   - Inspection revealed raw unescaped LaTeX backslashes (`\Delta` is illegal JSON escape; `\text`, `\frac`, `\nu` become silent control characters `\t`, `\f`, `\n`).
   - Length analysis via `analyze_options.py`: In Question 1 (`Q-HAB03-ISLM-001`), correct option `C` is 157 chars (longest by 13.8%) and uniquely carries justification (`porque tr(A) < 0...`); in Question 4 (`Q-HAB06-SOLOW-004`), correct option `E` is 181 chars (longest by 10.4%); in Question 7 (`Q-HAB04-EIG-007`), correct option `B` is tied for shortest. The correct answer was longest in $2/3$ (66.7%) of MC items, severely violating R2's $\le 25\%$ course rule.
   - Only 7 questions total, violating R2's volume requirement ($\ge 30$ per Skill, $\ge 20$ per Fact/Concept).

5. **Tooling & Environment Checks**:
   - Node: `v24.14.0`, npm: `11.9.0` (use `npm.cmd` / `npx.cmd`).
   - Python: `3.12.2800.0`. Installed packages: `fitz` (PyMuPDF 1.25.1), `pdfplumber`, `pypdf`, `sympy` (1.13.1).

---

## 2. Logic Chain

1. **Extraction Feasibility**:
   - Because `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf` contains clear digital text and well-defined slide titles, PyMuPDF can extract text and slide structures without OCR.
   - However, because Beamer compiles fractions and matrices across multiple lines, raw text extraction produces fragmented math lines.
   - *Inference*: A formula normalization pre-pass or structured prompt reconstruction is mandatory to reconstitute valid LaTeX expressions ($...$ and $$...$$).

2. **CTA Competence Model**:
   - The PDF explicitly covers 6 core mathematical modules. Mapping this to the CTA framework yields:
     - 7 Facts [H-01 to H-07] (Euler identity, PDE definitions/order/degree, solution identity, Lagrange symmetric system, 2nd-order characteristic polynomial, canonical forms by $\Delta$, differential operators).
     - 6 Concepts [C-01 to C-06] (Product exhaustion under perfect competition, characteristic curves as surface tangents, separation constant $\lambda$, functional independence of first integrals, Cauchy non-transversality condition, superposional cascade reduction).
     - 8 Skills [Hab-01 to Hab-08] (Verifying homogeneity degree, verifying candidate solutions, separating variables in heat equations, integrating symmetric Lagrange systems, finding Lagrange multipliers, solving Cauchy problems with parametric elimination, 2nd-order spectral classification, operator cascade factoring).
   - *Inference*: This provides 21 concrete units. Scoping all 21 units at $\ge 30$ / $\ge 20$ questions yields 500 questions; a focused curriculum of 7 units (3 Skills + 4 Concepts/Facts) yields 170 questions.

3. **Batch Generation Necessity**:
   - Generating 170 to 500 questions with 7 options, 3-5 hints, solutions, and misconception warnings requires $\approx 100,000$ to $300,000$ tokens of output.
   - A single LLM response is bounded by $4,096$ or $8,192$ output tokens (capable of generating at most 6–8 rich questions).
   - *Inference*: The generator must be architected as a chunked batch orchestrator (generating 6–8 questions per prompt) with an accumulator that validates each batch independently and merges them into the master course JSON.

4. **Anti-Giveaway & Psychometric Rigor**:
   - The analysis of `output_example_exercises.json` proved that LLMs systematically give away correct answers by appending explanations only to the correct option and making it the longest.
   - *Inference*: The pipeline must enforce strict bounds:
     $0.80 \times \min(D) \le L_{\text{correct}} \le 1.20 \times \max(D)$ per question, and $\le 25\%$ longest / $\le 25\%$ shortest across the course.
     Stems and prompt constraints must mandate symmetric rationales: either all 7 options carry matching rationales or none do.

5. **Independent Verification & Quality Audits**:
   - Acceptance criteria require $\ge 95\%$ accuracy on a 40-question sample and $\le 30\%$ guess rate on a 40-question blind-guess test.
   - To achieve this without manual intervention, the skill must incorporate:
     - Tier 1: SymPy programmatic checking for algebraic and polynomial equivalence.
     - Tier 2: Blind LLM solver that receives stems and bare options without keys or hints.
     - An automated repair loop with regex sanitizers, option length rebalancers, and batch shortfall fillers.

---

## 3. Caveats

- **No Caveats on Feasibility**: All required Python libraries (`fitz`, `sympy`, `pdfplumber`) and Node/npm are verified installed and functional.
- **Language Constraint**: Exercise text must be in Spanish because the source PDF is in Spanish. The practice platform UI itself remains in English per R1.
- **SymPy Parsing Limits**: While SymPy handles standard polynomials, derivatives, and algebraic fractions easily, highly non-linear implicit relations ($\phi(m, n) = 0$) require the Tier 2 Blind LLM solver for verification rather than pure algebraic equality.

---

## 4. Conclusion

The specification for the Competence Analysis & Skill Pipeline is complete, fully documented, and ready for implementation in Milestone 3 & Milestone 4.
The complete architecture, prompt templates, batching engine design, anti-giveaway rules, verification tiers, R2 repair state machine, audit methodologies, and edge cases are documented in `skill_spec.md`.

---

## 5. Verification Method

To independently verify the findings in this report:

1. **Verify PDF Extraction & Structure**:
   ```bash
   python -c "import fitz; doc=fitz.open('sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf'); print('Pages:', len(doc)); print(doc[10].get_text('text')[:300])"
   ```
2. **Verify JSON Syntax Error in Sample Exercises**:
   ```bash
   python -c "import json; json.load(open('system_prompts/output_example_exercises.json', encoding='utf-8'))"
   # Asserts JSONDecodeError at line 19 column 113
   ```
3. **Verify Option Giveaway in Sample Exercises**:
   ```bash
   python .agents/teamwork/spec_miner_format/analyze_options.py
   # Confirms Correct option is longest in 66.7% of MC items
   ```
4. **Verify SymPy & Environment Tools**:
   ```bash
   python -c "import sympy; print('SymPy:', sympy.__version__)"
   node -v
   npm.cmd -v
   ```
5. **Inspect Deliverables**:
   Inspect `g:\Mi unidad\Competence_analyser\.agents\teamwork\spec_miner_skill\skill_spec.md` for complete specification tables, CTA taxonomy, batching protocol, and audit rubrics.
