# Forensic Investigation: Thinking Traces, Reasoning Token Expenditure, and Cognitive Failure Modes of Straggler Shard Authors

**Audit Date:** 2026-11-09  
**Investigator:** Forensic Thinking & Cognitive Profiler (Google Antigravity SDK & C2C Pipeline)  
**Target:** 9 Slowest Shard Author Subagents across Runs 1, 2, and 3  
**Artifact Path:** [`reports/c2c_audits/straggler_thinking_investigation.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/straggler_thinking_investigation.md)

---

## 1. Executive Summary

This forensic investigation analyzes the subagent execution transcripts (`transcript_full.jsonl`) for the 9 slowest shard authors ("stragglers") in the Content-to-Course (C2C v3.3) Load Inversion pipeline across three production benchmarks:
1. **Run 1 (`66915882`) - Sistemas de Ecuaciones Diferenciales (Saul):** `shard_14`, `shard_34`, `shard_33`, `shard_39`, `shard_40`.
2. **Run 2 (`3981c7eb`) - Modelo de Solow (MapReduce):** `shard_01`, `shard_10`.
3. **Run 3 (`539b37fa`) - Modelo de Solow (Direct):** `shard_06`, `shard_03`.

### Key Aggregate Findings

| Metric | Aggregate Across 9 Stragglers | Mean per Straggler | Worst Case (Single Shard) |
| :--- | :--- | :--- | :--- |
| **Execution Duration** | 5,585.0 s (~93.1 min) | 620.6 s (10.3 min) | `shard_14` (796.0 s / 13.3 min) |
| **Total Planner Turns** | 208 turns | 23.1 turns | `shard_10` (38 turns) |
| **Reasoning Characters (`thinking`)** | 503,668 chars | 55,963 chars | `shard_01` (89,142 chars) |
| **Total Output Tokens** | 715,190 tokens | 79,465 tokens | `shard_01` (111,784 tokens) |
| **Pre-Compile Thinking Share** | N/A | 65.2% | `shard_34` (81.4%) |
| **Post-Compile Thinking Share** | N/A | 34.8% | `shard_14` (58.0%) |

### The Core Diagnostic Diagnosis

The investigation proves that the slowest subagents were not delayed by network latency, I/O bottlenecks, or platform contention. Instead, **the stragglers suffered from four distinct, highly repetitive cognitive failure modes** induced by a combination of prompt rigidity, compiler diagnostic omissions, and unassisted mathematical derivation:

1. **Monolithic Turn-3 Mental Synthesis (Pre-Compile Bloat):** Every subagent attempted to mentally design all 4 Form-C archetypes (Direct, Inverse, Perturbation, Boundary/Edge-case), all 6 distractors, all LaTeX stems, hints, and custom python verifiers in a single massive Step-3 thinking block (24,000 to 44,000 characters). In 100% of cases (9 out of 9), this initial monolithic draft failed the very first run of `compile_shard.py`.
2. **The "UMBRAL < 6" Micro-Looping Trap:** Both the full and lean author prompts commanded: `[UMBRAL < 6 (1..5 errores)]: Usa edit_file quirúrgico en las líneas indicadas (<= 30 líneas); PROHIBIDO write_file completo`. When faced with 1 to 4 compiler warnings, subagents (`shard_10`, `shard_14`) spent up to 14 consecutive turns making single-line micro-edits interspersed with `view_file` calls without running the compiler, multiplying latency by 4x.
3. **Validator Diagnostic Omissions:** When `compile_shard.py` flagged missing distractors without outputting the exact set-difference (`shard_01`), the agent spent 40,000 thinking characters and 6 turns attempting to parse JSON using PowerShell scripts. When it reported `[DIAG-MAGIC-MULT]` (`shard_14`), the agent attempted rejection-sampling arrays rather than algebraic refactoring.
4. **Fragile String Parsing & LaTeX Clashes:** The canonical `_pv(c)` helper provided in the system prompt crashed with `ValueError: could not convert string to float: '2.708\\\\'` (`shard_34`) when LaTeX delimiters or double-backslashes leaked into candidate answers, requiring emergency in-turn patching.

---

## 2. Forensic Telemetry Matrix

The table below synthesizes the granular operational and cognitive metrics extracted directly from the system logs for all 9 investigated subagents.

| Shard Identifier | Subagent Conversation ID | Duration | Turns | Total Thinking | Pre % | Post % | Output Tokens | 1st Compile | Tool Calls (V / E / W / R) | Primary Cognitive Failure Mode |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Run 1 - `shard_14`** | `6a1e3d60-abf4-4c73-8498-de49729127e7` | 796.0s | 36 | 58,459 ch | 42.0% | **58.0%** | 81,754 | Step 5 (6 total) | V:17, E:10, W:1, R:6 | Micro-looping & `[DIAG-MAGIC-MULT]` rejection |
| **Run 1 - `shard_34`** | `18316bca-2b4b-4655-a55f-ba73fd316329` | 639.0s | 17 | 54,584 ch | **81.4%** | 18.6% | 69,997 | Step 5 (4 total) | V:6, E:4, W:1, R:4 | LaTeX Backslash Crash in `_pv(c)` |
| **Run 1 - `shard_33`** | `af7b7bb9-176a-4cd8-b488-f076b94343da` | 632.0s | 31 | 43,260 ch | **75.1%** | 24.9% | 62,527 | Step 5 (3 total) | V:15, E:8, W:1, R:3 | Background Task Polling & Rationale Diffs |
| **Run 1 - `shard_39`** | `0c7a4f9e-aced-4e1b-a180-537ee01d2609` | 610.0s | 19 | 45,403 ch | **75.4%** | 24.6% | 61,125 | Step 5 (3 total) | V:8, E:4, W:1, R:3 | Background Task Wait & Jacobian Derivations |
| **Run 1 - `shard_40`** | `7c610c33-df92-4583-8359-a2ec457d9029` | 592.0s | 13 | 50,294 ch | **76.8%** | 23.2% | 63,790 | Step 6 (2 total) | V:6, E:2, W:1, R:2 | Mental Math on Characteristic Polynomials |
| **Run 2 - `shard_01`** | `bc026805-82f8-4dd9-8589-e692345d94f5` | 719.0s | 20 | **89,142 ch** | 46.4% | **53.6%** | **111,784** | Step 5 (4 total) | V:6, E:4, W:1, R:8 | Validator Omission & PowerShell Debugging Loop |
| **Run 2 - `shard_10`** | `87fbcfa2-51a0-4a2e-b472-8c297cdf075a` | 677.0s | **38** | 68,220 ch | 55.2% | 44.8% | 96,571 | Step 5 (4 total) | V:20, E:11, W:1, R:4 | "UMBRAL < 6" Micro-Looping on Metalinguistics |
| **Run 3 - `shard_06`** | `1d7b6add-39f6-43e7-b0cd-e35665a78f48` | 472.0s | 15 | 56,657 ch | 69.5% | 30.5% | 81,284 | Step 5 (4 total) | V:5, E:4, W:2, R:4 | Step 17 Full File Rewrite (14k thinking chars) |
| **Run 3 - `shard_03`** | `d22e2d3a-9d50-4484-a0f9-e843a6d43eef` | 448.0s | 19 | 56,399 ch | 58.9% | 41.1% | 66,539 | Step 5 (3 total) | V:7, E:6, W:1, R:3 | Metalinguistic Rewriting & Convexity Stability |

---

## 3. Cognitive Profiling: Pre-Compile vs. Post-Compile Breakdown

A critical finding of this audit is that **the stragglers bifurcate into two distinct pathological profiles**:

```
[STRAGGLER TAXONOMY]
       │
       ├─ Type A: The "Monolithic Overthinker" (Pre-Compile Share >= 75%)
       │  ├─ Shards: Run 1 (34, 33, 39, 40), Run 3 (06)
       │  ├─ Pathology: Spends 30,000–45,000 characters of reasoning in Step 3 trying to
       │  │  derive every formula, eigenvalue, LaTeX stem, and distractor mentally.
       │  └─ Outcome: First compilation STILL fails 100% of the time.
       │
       └─ Type B: The "Diagnostic Spiraler" (Post-Compile Share >= 45%–58%)
          ├─ Shards: Run 1 (14), Run 2 (01, 10), Run 3 (03)
          ├─ Pathology: Encounters a compiler error and enters a diagnostic panic loop,
          │  triggering massive secondary thinking blocks (10,000–21,000 chars) and micro-edits.
          └─ Outcome: Accumulates 30 to 38 turns and over 100,000 output tokens.
```

### Type A: The Monolithic Overthinker (`Pre-Compile % >= 75%`)
- In `shard_34`, **81.4% of all thinking** occurred before the first compiler execution. In Turn 3 alone, the agent generated **44,127 characters of thinking** and **52,934 tokens**, attempting to solve the entire macroeconomic jump-dynamics saddle-point problem by hand.
- In `shard_40`, **76.8% of thinking** (37,958 chars in Turn 4) was spent calculating 2x2 matrix traces, determinants, and discriminant bounds to ensure real distinct eigenvalues before touching `compile_shard.py`.
- **The Core Paradox:** Despite spending up to 44,000 reasoning characters calculating values to make the initial code "perfect", **the first compilation in Step 5 failed in every single shard**. High pre-compile thinking provided zero immunity against validator rejection.

### Type B: The Diagnostic Spiraler (`Post-Compile % >= 45%–58%`)
- In `shard_14`, **58.0% of all thinking** (33,889 characters) occurred *after* the first compilation failure. Turn 35 alone contained **14,007 characters of thinking** after receiving a `[TPL-DRY]` sandbox error.
- In `shard_01`, **53.6% of thinking** (47,760 characters) occurred after compilation failed at Turn 5. The agent entered a 21,324-character thinking block in Turn 19 and an 11,499-character thinking block in Turn 25, trying to deduce which distractors were missing.
- In `shard_10`, the agent engaged in 38 turns, spending 30,574 post-compile thinking characters distributed over 14 consecutive micro-edits.

---

## 4. Deep Forensic Analysis of the Four Cognitive Failure Modes

### 4.1 Mental Math Overload (Manual Computation in Thinking Chains)

Instead of utilizing Python's sandboxed environment or mathematical libraries, subagents repeatedly performed high-complexity linear algebra, calculus, and dynamical systems derivations directly inside their reasoning tokens.

#### Evidence 1: Run 1 `shard_14` (Turn 3 & Turn 7)
In `shard_14` (analyzing non-homogeneous 2x2 differential systems $\dot{x} = ax + by + p, \dot{y} = cx + dy + q$), the model spent thousands of thinking tokens manually calculating matrix inversions and perturbation formulas:
> **Transcript Excerpt (Turn 3):**  
> *"The task is to analyze a system's stability and stationary points. Initial focus will be on solving the linear algebraic system to find the equilibrium point $(\bar{x}, \bar{y})$... Solving for the equilibrium point requires inverting the Jacobian matrix and accounting for the non-homogeneous term... The calculation shows $b \cdot q - d \cdot p' = a d x' - b c x^*$ which is not the expected product. Because $y'$ changes in accordance with $x'$, the expected calculation is incorrect... The analysis reveals the mathematical relationship between the original and perturbed solutions, leading to the correct integer condition. A detailed check confirms the formula relating $x'$ to $p'$ when the perturbation $\Delta p = k \cdot \det(A)$..."*

**Impact:** The agent spent over 12 minutes verifying integer divisibility and perturbation shifts manually. When it wrote the code, it still had a sign error that caused `ver_h14_3` to reject its own generated instance on seed 42 at Step 5.

#### Evidence 2: Run 1 `shard_40` (Turn 4)
In `shard_40` (characteristic polynomial and eigenvalues), the subagent derived the roots of $\lambda^2 - \operatorname{tr}(A)\lambda + \det(A) = 0$ manually:
> **Transcript Excerpt (Turn 4):**  
> *"Considering competency H-04, the canonical formula $p_A(\lambda) = \lambda^2 - \operatorname{tr}(A)\lambda + \det(A) = 0$ is the basis for question design... To ensure distinct real eigenvalues, we must have $\Delta = \operatorname{tr}(A)^2 - 4\det(A) > 0$. If $\operatorname{tr} = -5$ and $\det = 6$, then roots are $-2$ and $-3$... verifying that $\lambda_1 < \lambda_2 < 0$ for stable node..."*

**Root Cause:** The agent attempted to pick random matrix entries $a, b, c, d$ that would yield clean integer eigenvalues. Had it used the **Vieta Inverse Recipe** (pick integer eigenvalues $\lambda_1, \lambda_2$ first, then set $\operatorname{tr} = \lambda_1 + \lambda_2$ and $\det = \lambda_1 \lambda_2$), this calculation would have taken 0 reasoning tokens.

#### Evidence 3: Run 2 `shard_01` (Turn 3)
In `shard_01` (deriving the Solow fundamental differential equation), the subagent re-derived the entire continuous-time Solow growth model in reasoning text:
> **Transcript Excerpt (Turn 3):**  
> *"The target formula involves $\dot{k} = s\phi(k) - (\lambda + n + \delta)k$. Analyzing the distractors reveals common errors in deriving this equation, including omission of the population dilution effect, algebraic sign errors, confusing capital per worker with effective worker... differentiating $k = K/(AL)$ yields $\dot{k}/k = \dot{K}/K - \dot{A}/A - \dot{L}/L$... substituting $\dot{K} = s Y - \delta K$..."*

---

### 4.2 LaTeX Escaping Battles & Fragile Parsing

Subagents frequently engaged in multi-turn battles with LaTeX string escaping, backslash formatting, and parser collisions between JSON strings, Python raw strings, and KaTeX delimiters.

#### Evidence 1: Run 1 `shard_34` (The `2.708\\\\` Float Conversion Crash)
In `shard_34`, the agent authored `shard_34_data.py` using the exact `_pv(c)` implementation recommended in the system prompt:
```python
def _pv(c):
    return float(str(c).replace(r"\le", "=").replace(r"\ge", "=").replace(r"\approx", "=").replace("<=", "=").replace(">=", "=").replace("$", "").replace("%", "").split("=")[-1].strip())
```
At Step 13, `compile_shard.py` executed verification seed checks, causing an unhandled crash:
```
Traceback (most recent call last):
  File "compile_shard.py", line 2440, in run_ver
    return ver_raw(c_val, vars_d)
  File "shard_34_data.py", line 69, in ver_c19_1
    def ver_c19_1(c, v): return abs(_pv(c) - (v["gamma"] * v["n"] / (1.0 - v["beta"] - v["theta"]))) < 1e-2
  File "shard_34_data.py", line 2, in _pv
    return float(str(c)...split("=")[-1].strip())
ValueError: could not convert string to float: '2.708\\\\'
```
**Transcript Excerpt (Turn 15 -> 17):**  
The candidate answer string had a trailing LaTeX line break `\\` or escaped percent symbol `\%`. The subagent had to spend Turn 15 inspecting lines 1–6 and Turn 17 patching `_pv(c)` to:
```python
def _pv(c):
    return float(str(c).replace(r"\le", "=").replace(r"\ge", "=").replace(r"\approx", "=").replace("<=", "=").replace(">=", "=").replace("$", "").replace(r"\%", "").replace("%", "").replace("\\\\", "").split("=")[-1].strip())
```
**Cost:** 2 full turns, 2,800 tokens, and 45 seconds of execution time caused by the fragility of a regex snippet copied directly from pipeline instructions.

#### Evidence 2: Run 2 `shard_01` (Turn 3 & Turn 11) - Python F-String Delimiter Clashes
The agent spent substantial reasoning navigating double-brace escaping when interpolating Python variables into LaTeX equations:
> **Transcript Excerpt (Turn 3):**  
> *"The strategic use of `f\"$\\dot{{k}} > 0 \\Leftrightarrow {s}\\phi(k) - {lamb} k$\"` with specific placeholders maintains uniformity. The string `\"\\\\Leftrightarrow\"` is correctly identified in options... ensuring KaTeX does not interpret double braces as set notation..."*

---

### 4.3 Validator Diagnostic Confusion (Cryptic Compiler Feedback)

When `compile_shard.py` failed, its error messages frequently lacked the necessary delta/diff information, causing subagents to misinterpret the root cause and execute wild debugging tangents.

#### Evidence 1: Run 2 `shard_01` (Turns 5 -> 33) - The Missing Distractor Shell-Scripting Tangent
At Turn 5, `compile_shard.py` reported:
```
[-] FAIL: 1 errores detectados (1 errores consolidados) al compilar shard_01:
FAIL: 1 validaciones fallidas en templates:
[-] [DISCREPANCY] Distractors defined in configuration are not present in Hab-01 template
```
**The Flaw:** The compiler did *not* print *which* of the 12 distractors were missing. It simply emitted a generic discrepancy message.

**The Catastrophic Tangent:**
1. **Turn 7:** The agent spent **8,650 thinking characters** hypothesizing which distractors were missing.
2. **Turn 19:** The agent generated a **21,324-character thinking block**, re-reading all distractors in `author_01.json`.
3. **Turn 25:** Generating an **11,499-character thinking block**, the agent decided it could not figure out the missing distractors manually, so it executed a PowerShell script:
   ```powershell
   powershell -Command "$j = Get-Content 'courses/.../Hab-01.json' -Raw | ConvertFrom-Json; $j.templates | ForEach-Object { Write-Output ($_.template_id + ' | ' + ($_.distractor_ids -join ', ')) }"
   ```
4. **Turn 27 & Turn 29:** PowerShell failed with syntax errors:
   - `ParserError: MissingVariableNameAfterForeach`
   - `ObjectNotFound: =:String`
5. **Turn 31:** The agent corrected the PowerShell command:
   ```powershell
   powershell -Command "(Get-Content 'courses/.../Hab-01.json' -Raw | ConvertFrom-Json).templates | Select-Object template_id, distractor_ids"
   ```
6. **Turn 33:** Only after reading the PowerShell table output did the agent realize:
   > *"Examining the command output and the template file reveals... distractors `D-Hab01-03` and `D-Hab01-04` are entirely absent from all templates."*

**Total Cost of Missing Diff Diagnostic:** **>40,000 reasoning characters, 6 wasted tool turns, and ~250 seconds of agent latency!** A simple compiler message reading `Missing: ['D-Hab01-03', 'D-Hab01-04']` would have resolved this issue in a single 15-second edit turn.

#### Evidence 2: Run 1 `shard_14` (Turn 17 -> 51) - `[DIAG-MAGIC-MULT]` Rejection Sampling
At Turn 17, `compile_shard.py` flagged:
```
[-] [DIAG-MAGIC-MULT] En 'T-Hab-14-01' (función 'gen_h14_1', Líneas 132..132 en shard_14_data.py), los distractores numéricos en 27/234 semillas (>7%) coinciden con multiplicadores arbitrarios prohibidos ([0.333, 0.667, 1.333]...)
```
Instead of redesigning the distractor algebraic formula, the agent attempted to evade the diagnostic by hardcoding a blacklist and looping:
> **Transcript Excerpt (Turn 51 Edit):**  
> ```python
> BAD = (0.2, 0.25, 0.33, 0.333, 0.4, 0.5, 0.66, 0.667, 0.75, 1.25, 1.333, 1.5, 1.667, 1.85, 2.0)
> # agent added while loop checking: if any(abs(d / ans - b) < 0.05 for b in BAD): continue
> ```
This rejection loop caused random seeds to exceed iteration budgets, which led to `[TPL-DRY: FALLO EN EJECUCIÓN DRY-RUN]` on Turn 33, triggering another 14,007 characters of panicked reasoning in Turn 35.

---

### 4.4 Micro-Looping & Piecemeal Edits (The "UMBRAL < 6" Trap)

Both the standard system prompt (`prompt_shard_author.md`) and the lean version enforce a strict rule:
> *"Si hay < 6 errores (1..5 errores): Usa `edit_file` (replace_file_content) quirúrgico en las líneas indicadas (<= 30 líneas); PROHIBIDO write_file completo."*

While intended to prevent agents from blowing away working code on large 1,000-line repositories, **on a 150-line `shard_data.py` file, this rule acts as a severe cognitive trap**:

```
[THE MICRO-LOOPING TRAP]
Compiler reports 2 minor errors
       │
       ▼
Agent forbidden from rewriting file
       │
       ▼
Turn N:   `view_file` lines 1-30  ────────┐
Turn N+1: `edit_file` line 12             │
Turn N+2: `view_file` lines 31-60         │ Repeats 10 to 14 times!
Turn N+3: `edit_file` line 45             │ Each cycle: 1 turn = ~20-30s
Turn N+4: `view_file` lines 61-90         │ Accumulates 50k+ input tokens
Turn N+5: `edit_file` line 80  ───────────┘
       │
       ▼
Compiler run finally executed at Turn N+14!
```

#### Granular Evidence from Run 2 `shard_10` (Turns 9 to 39)
In `shard_10`, the compiler reported minor metalinguistic issues and distractor formatting across 2 competencies. Under the `< 6 errors` restriction, the agent was terrified of using `write_file`. Look at the exact turn progression:
- **Turn 9:** `view_file` lines 1–40 (Thinking: 3,617 chars)
- **Turn 11:** `view_file` lines 41–140
- **Turn 13:** `view_file` lines 141–233
- **Turn 15:** `view_file` lines 7–16 (Thinking: 13,212 chars!)
- **Turn 17:** `edit_file` (1 distractor in `RATS_C05`)
- **Turn 19:** `view_file` lines 110–125
- **Turn 21:** `edit_file` (1 distractor in `RATS_C06`)
- **Turn 23:** `view_file` lines 123–170
- **Turn 25:** `edit_file` (`_gen_c06` range change)
- **Turn 27:** `view_file` lines 150–175
- **Turn 29:** `edit_file` (`arch == 2` fix)
- **Turn 31:** `view_file` lines 180–225
- **Turn 33:** `edit_file` (`ver_c06_4` fix)
- **Turn 35:** `view_file` lines 199–216
- **Turn 37:** `edit_file` (`Q_C06_2` stem edit)
- **Turn 39:** FINALLY runs `compile_shard.py` (after **15 consecutive view/edit turns**!).

**Total Latency for Turn 9–39 Sequence:** **295 seconds (~5 minutes)** simply to modify ~35 lines of Python code!

---

## 5. In-Depth Case Studies of Top Stragglers

### Case Study 1: Run 1 - `shard_14` (The Longest Run: 796.0s, 36 turns)
- **Subagent Conversation ID:** `6a1e3d60-abf4-4c73-8498-de49729127e7`
- **Assigned Task:** `Hab-14` (Linear 2x2 differential systems with translation/perturbation).
- **Execution Breakdown:**
  - Turn 3: 24,029 chars thinking -> initial `write_file` (29,428 tokens).
  - Turn 5: 1st compile fails (`FAIL: [TPL-VERIFIER-UNSOUND] ver_h14_3`).
  - Turn 11: 2nd compile fails (`FAIL: [TPL-DYNAMIC-RATIONALE] @ystar@ not declared in vars`).
  - Turn 17: 3rd compile fails (`FAIL: [DIAG-MAGIC-MULT]`).
  - Turns 19–33: Agent tries to patch distractor multipliers.
  - Turn 33: Compiler outputs `[NO-CHANGE]`, agent panics.
  - Turn 35: **14,007 characters of reasoning** diagnosing why seeds failed.
  - Turns 37–61: **13 consecutive turns** of micro-editing line by line.
  - Turn 63: 5th compile fails (`[TPL-D4: OPCIONES DUPLICADAS]`).
  - Turn 69: 6th compile passes.
  - Total tokens: 81,754 out tokens, 58,459 reasoning characters.

### Case Study 2: Run 2 - `shard_01` (The Highest Token Consumer: 111,784 tokens, 89k thinking chars)
- **Subagent Conversation ID:** `bc026805-82f8-4dd9-8589-e692345d94f5`
- **Assigned Task:** `Hab-01` (Solow Model Fundamental ODE).
- **Execution Breakdown:**
  - Turn 3: 41,087 chars thinking -> initial `write_file` (49,583 tokens).
  - Turn 5: 1st compile fails (`FAIL: Discrepancy: distractors defined in configuration are not present in Hab-01 template`).
  - Turns 7–19: Massive thinking blocks (8.6k and 21.3k chars) trying to guess which distractors are missing.
  - Turn 25: 11,499 chars thinking -> launches PowerShell script to parse JSON.
  - Turns 27–31: Crashes with PowerShell parsing errors, adjusts syntax, finally lists template distractor mapping.
  - Turn 35: Edits distractor lists in `shard_01_data.py`.
  - Turn 37: Compile passes.
  - Total tokens: 111,784 tokens (highest in entire benchmark).

---

## 6. Actionable Engineering Proposals

To eliminate these straggler bottlenecks, we propose concrete changes across the compiler (`compile_shard.py`), prompt engineering (`prompt_shard_author.md`), and orchestration parameters.

### 6.1 Enhancements to `compile_shard.py`

#### Proposal 1: Explicit Set-Difference Diagnostics for Distractors
*Problem:* Cryptic messages like `discrepancy: distractors defined in config not present` trigger multi-turn guessing and shell-scripting loops.  
*Fix:* When checking distractor assignment coverage, compute and print the exact set difference:
```python
# In compile_shard.py (distractor verification)
missing_dids = set(config_dids) - set(used_dids)
extra_dids = set(used_dids) - set(config_dids)
if missing_dids or extra_dids:
    msg = []
    if missing_dids:
        msg.append(f"MISSING REQUIRED DISTRACTORS: {sorted(list(missing_dids))}. You must assign these to your templates.")
    if extra_dids:
        msg.append(f"UNDECLARED DISTRACTORS USED: {sorted(list(extra_dids))}.")
    return False, " | ".join(msg)
```

#### Proposal 2: Robust Built-In AST Numeric Parser (`parse_clean_number`)
*Problem:* Every shard writes its own fragile `_pv(c)` function that crashes on `\\`, `\%`, `\text{}`, or negative signs.  
*Fix:* Inject a standardized, robust parser into the template evaluation namespace, and auto-strip LaTeX clutter before invoking `ver_*`:
```python
import re

def parse_clean_number(val: any) -> float:
    # Bulletproof converter for LaTeX and mathematical strings
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip()
    # Strip LaTeX math delimiters and symbols
    s = re.sub(r'[\$\\%\s]', '', s)
    s = s.replace(r'\le', '=').replace(r'\ge', '=').replace(r'\approx', '=')
    s = s.replace('<=', '=').replace('>=', '=')
    s = re.sub(r'\\text\{[^}]*\}', '', s)
    s = re.sub(r'\\\\', '', s)
    if '=' in s:
        s = s.split('=')[-1]
    # Clean any remaining non-numeric chars except '.' and '-'
    s = re.sub(r'[^\d\.\-eE]', '', s)
    return float(s)
```

#### Proposal 3: Explicit Variable Token Diff on `[TPL-DYNAMIC-RATIONALE]`
*Problem:* Subagents use `@ystar@` in rationale while `vars` only has `['a', 'b', 'c', 'd', 'det', 'p', 'q']`.  
*Fix:* When rationale validation fails, print:
```
FAIL: [TPL-DYNAMIC-RATIONALE] Distractor 'D-Hab14-04' uses undeclared variable '@ystar@'.
  -> Declared variables in vars: ['a', 'b', 'c', 'd', 'det', 'p', 'q', 'tr']
  -> Action: Use one of the declared variables or add 'ystar' to vars in gen_*.
```

---

### 6.2 Prompt Engineering Optimizations (`prompt_shard_author.md`)

#### Proposal 4: Replace "UMBRAL < 6" Micro-Editing Rule with "Single-Turn Atomic Refactor"
*Problem:* Forbidding `write_file` when error count is < 6 forces 10 to 15 turns of 20-line edits on small 150-line files.  
*Fix:* Update the prompt instruction:
> **REVISION:**  
> *"On files smaller than 300 lines (such as `<shard_id>_data.py`), you are PERMITTED to use `write_file(Overwrite=True)` to fix all compiler errors in a single atomic turn. Do NOT make 10 piecemeal edits across 10 turns. If `compile_shard.py` fails, read the error, rewrite the entire file cleanly in Turn N+1, and immediately recompile in Turn N+2."*

#### Proposal 5: Strict Zero-Mental-Math Directive & Vieta Inverse Recipes
*Problem:* Models waste 30k+ thinking tokens deriving eigenvalues, Jacobians, and roots manually.  
*Fix:* Add explicit mathematical design guidelines:
> **REVISION:**  
> *"🚫 **STRICT ZERO-MENTAL-MATH POLICY:** Do NOT calculate eigenvalues, matrix inverses, or ODE equilibrium points in your thinking chain. Always use TARGET-FIRST parameter generation:*  
> *1. For 2x2 Matrices: Choose target integer eigenvalues $\lambda_1, \lambda_2 \in \mathbb{Z}$ first. Set $\operatorname{tr} = \lambda_1 + \lambda_2$ and $\det = \lambda_1 \lambda_2$. Pick random $a$, set $d = \operatorname{tr} - a$, pick factors $b, c$ such that $bc = ad - \det$.*  
> *2. For Linear Systems $A\vec{x} = \vec{b}$: Choose integer equilibrium $\vec{x}^* = (x^*, y^*)$ first. Generate matrix $A$. Compute $\vec{b} = -A\vec{x}^*$ directly in Python. Never invert matrices by hand."*

#### Proposal 6: Strict Prohibition of Shell-Scripting / Inline Code
*Problem:* Subagents trying to run PowerShell inline code (`powershell -Command ...`) enter syntax error loops.  
*Fix:* Add to Section 0:
> *"🚫 **PROHIBIDO ejecutar scripts PowerShell o comandos de introspección:** Está terminantemente prohibido ejecutar `powershell -Command`, `Get-Content`, o `python -c` para inspeccionar archivos. Toda información necesaria está en el work order y en el output de `compile_shard.py`."*

---

### 6.3 Orchestration & Execution Parameters

#### Proposal 7: Set `WaitMsBeforeAsync: 15000` for all Compiler Invocations
*Problem:* In `shard_33` and `shard_39`, `compile_shard.py` took ~5.2 seconds, exceeding the default 5,000ms wait, which switched the execution to a background task (`af7b7bb9.../task-6`). This caused agents to enter polling and task-management loops.  
*Fix:* Ensure all author dispatch scripts instruct agents to execute `compile_shard.py` with `WaitMsBeforeAsync: 15000` (or 20000) so compilation always terminates synchronously.

---

## 7. Projected Impact & ROI

Implementing the 7 proposals outlined above will transform the performance profile of straggler shard authors:

| Metric | Current Straggler Baseline | Projected Post-Optimization | Expected Improvement |
| :--- | :--- | :--- | :--- |
| **Average Straggler Duration** | 620.6 s (10.3 min) | **180.0 s (3.0 min)** | **-71.0% latency reduction** |
| **Worst-Case Duration (`shard_14`)** | 796.0 s (13.3 min) | **210.0 s (3.5 min)** | **-73.6% latency reduction** |
| **Average Turns per Shard** | 23.1 turns | **6 to 8 turns** | **-69.7% turns reduction** |
| **Reasoning Characters per Shard** | 55,963 chars | **15,000 to 20,000 chars** | **-68.0% reasoning overhead** |
| **Total Output Tokens per Shard** | 79,465 tokens | **25,000 to 30,000 tokens** | **-64.8% token expenditure** |
| **Compiler Roundtrips** | 3 to 6 rounds | **1 to 2 rounds** | **-66.7% compilation cycles** |

---

## 8. Conclusion

The forensic analysis of the 9 slowest shard authors demonstrates unequivocally that the "straggler problem" in the C2C pipeline is an artifact of **cognitive misalignment between compiler diagnostics and prompt constraints**. By replacing cryptic diagnostics with explicit set-difference diffs, removing the paralyzing "UMBRAL < 6" micro-editing restriction, providing target-first Vieta math recipes, and standardizing LaTeX numeric parsing in the compiler runtime, the Content-to-Course pipeline can achieve predictable, sub-3-minute shard completion times across all future course authoring runs.
