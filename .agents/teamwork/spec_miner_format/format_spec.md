# Specification: Course Format, JSON Schema & Psychometric Validator

**Project**: Top's Academy  
**Component**: Exercise-Bank Format & Validator (R2 Acceptance Criteria)  
**Author**: Format & Validator Spec Miner  
**Date**: 2026-10-11  
**Status**: APPROVED SPECIFICATION  

---

## 1. Executive Summary & Specification Scope

This document defines the formal, versioned JSON schema and the algorithmic validator specification for the **Top's Academy** course generation and practice platform. It establishes the authoritative standard for:
1. **Course Structure & Metadata**: Top-level course manifest, competencies (units), and question banks.
2. **Pedagogical Typologies**: Canonical 7-option multiple-choice items, multi-select items (1 to $n-1$ correct), and direct input fill-in-the-blank items with symbolic mathematical equivalence.
3. **Interactive Graph Models**: Declarative vector graph definitions (axes, curves, open/closed points, labels) renderable via Canvas/SVG/JSXGraph.
4. **Scaffolding & Solutions**: 3 to 5 progressive hints per item, step-by-step analytical solutions, and explicit misconception warnings.
5. **Psychometric Anti-Giveaway Engine**: Strict per-item and per-course length symmetry rules, and qualitative distractor parity constraints.
6. **LaTeX & JSON Escaping Guarantees**: Complete eradication of single-backslash escape corruptions (both syntax-invalid escapes and silently-valid escapes producing ASCII control characters).

---

## 2. Exhaustive Flaw Analysis of `output_example_exercises.json`

An automated and manual inspection of `system_prompts/output_example_exercises.json` was conducted across lexical, syntactic, structural, and psychometric dimensions. The file fails standard JSON parsing immediately and exhibits severe pedagogical giveaway cues.

### 2.1 Lexical & Syntactic Corruptions

The file is **NOT valid JSON** (RFC 8259 violation) and cannot be parsed by `json.loads()` or `JSON.parse()`.

```
$ python -c "import json; json.load(open('system_prompts/output_example_exercises.json'))"
JSON error: Invalid \escape: line 19 column 113 (char 785)
```

The underlying causes fall into four distinct categories:

#### A. Invalid JSON Escape Sequences (519 occurrences)
JSON strings only permit the following escapes: `\"`, `\\`, `\/`, `\b`, `\f`, `\n`, `\r`, `\t`, `\uXXXX`. In `output_example_exercises.json`, LaTeX math commands were written with single backslashes instead of double backslashes (`\\`). When followed by characters outside the permitted escape set, standard JSON parsers abort immediately with syntax errors.

| Escaped Token | Occurrences | Example in File | Standard JSON Parser Action |
|:---|:---:|:---|:---|
| `\e` | 98 | `\end{bmatrix}` | Fatal syntax error: `Invalid \escape` |
| `\d` | 96 | `\dot{Y}_t`, `\det(A)`, `\delta` | Fatal syntax error: `Invalid \escape` |
| `\l` | 94 | `\lambda` | Fatal syntax error: `Invalid \escape` |
| `\s` | 53 | `\sigma`, `\sqrt` | Fatal syntax error: `Invalid \escape` |
| `\a` | 52 | `\alpha` | Fatal syntax error: `Invalid \escape` |
| `\g` | 44 | `\gamma` | Fatal syntax error: `Invalid \escape` |
| `\p` | 21 | `\pm`, `\pi` | Fatal syntax error: `Invalid \escape` |
| `\D` | 19 | `\Delta` | Fatal syntax error: `Invalid \escape` |
| `\i` | 15 | `\implies` | Fatal syntax error: `Invalid \escape` |
| `\m` | 9 | `\mu` | Fatal syntax error: `Invalid \escape` |
| `\o` | 8 | `\omega` | Fatal syntax error: `Invalid \escape` |
| `\q` | 8 | `\quad` | Fatal syntax error: `Invalid \escape` |
| `\c` | 2 | `\cos` | Fatal syntax error: `Invalid \escape` |
| **Total** | **519** | — | — |

#### B. Silently-Valid Escape Sequences Corrupting LaTeX (366 occurrences)
The most insidious flaw occurs when the first letter of a LaTeX command happens to match a valid JSON escape character. In these cases, a permissive or standard parser **does not fail**, but silently mutates the LaTeX command into an invisible ASCII control character:

| Escaped Token | Occurrences | Intended LaTeX Command | Silent JSON Conversion Result | Impact on Rendering Engine |
|:---|:---:|:---|:---|:---|
| `\b` | 139 | `\begin{bmatrix}`, `\beta`, `\bar{G}` | ASCII 0x08 (Backspace `\x08`) + `egin{bmatrix}` | KaTeX syntax error: unknown command `\x08egin` |
| `\t` | 66 | `\tau`, `\theta`, `\text{tr}`, `\times` | ASCII 0x09 (Horizontal Tab `\t`) + `au`, `heta` | KaTeX syntax error: corrupt macro identifier |
| `\f` | 59 | `\frac{1}{2}`, `\frac{\text{tr}(A)}{2}` | ASCII 0x0C (Form Feed `\x0c`) + `rac{1}{2}` | KaTeX syntax error: unknown command `\x0crac` |
| `\n` | 68 | `\nu`, `\nabla`, mixed text newlines | ASCII 0x0A (Line Feed `\n`) + `u`, `abla` | Corrupts math block tokens; newline inside math |
| `\r` | 4 | `\right)` | ASCII 0x0D (Carriage Return `\r`) + `ight)` | KaTeX syntax error: unmatched left delimiter |
| **Total** | **366** | — | — | — |

#### C. Raw Unescaped Multiline Strings (11 blocks)
RFC 8259 Section 9 explicitly prohibits literal unescaped control characters (U+0000 through U+001F) in string literals. The example file contains raw unescaped newlines inside JSON strings:
- **Lines 110–116**: Stem string of `Q-HAB02-GOODWIN-002` spans 7 lines with raw line breaks around math delimiters.
- **Lines 158–172**: Detailed solution of `Q-HAB02-GOODWIN-002` contains raw line breaks mixed with `\\n`.
- **Lines 186–190**: Stem string of `Q-MS-GOODWIN-003` broken across 5 raw lines.
- **Lines 273–277**: Stem string of `Q-HAB06-SOLOW-004`.
- **Lines 354–358**: Detailed solution of `Q-HAB06-SOLOW-004`.
- **Lines 372–382**: Stem string of `Q-HAB05-INHOMOG-005`.
- **Lines 422–434**: Detailed solution of `Q-HAB05-INHOMOG-005`.
- **Lines 448–454**: Stem string of `Q-MS-PHILLIPS-006`.
- **Lines 523–527**: Detailed solution of `Q-MS-PHILLIPS-006`.
- **Lines 541–543**: Stem string of `Q-HAB04-EIG-007`.
- **Lines 620–626**: Detailed solution of `Q-HAB04-EIG-007`.

#### D. Unescaped Quotes in String Literals (4 occurrences)
- **Line 232**: `"accepted_equivalents": [ "["A", "B", "E"]", ... ]` — inner double quotes are unescaped (`""A", "B", "E"]"`), breaking JSON array string syntax.
- **Line 496**: `"accepted_equivalents": [ "["A", "B", "C"]", ... ]` — identical unescaped inner quotes syntax failure.

---

### 2.2 Psychometric & Giveaway Deficiencies

Psychometric validity requires that an examinee cannot deduce the correct answer through superficial textual heuristics without knowing the underlying domain knowledge.

#### A. Multiple-Choice Option Lengths & Course-Level Distributions
The file contains 3 multiple-choice questions (`Q-HAB03-ISLM-001`, `Q-HAB06-SOLOW-004`, `Q-HAB04-EIG-007`):

| Question ID | Correct Opt ID | Correct Len | Distractor Min | Distractor Max | Excess vs Max Distractor | Shortfall vs Min Distractor | Longest in Item? | Shortest in Item? |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `Q-HAB03-ISLM-001` | C | 157 | 115 | 138 | **+13.8%** | 0.0% | **YES (Longest)** | NO |
| `Q-HAB06-SOLOW-004` | E | 181 | 138 | 164 | **+10.4%** | 0.0% | **YES (Longest)** | NO |
| `Q-HAB04-EIG-007` | B | 130 | 130 | 153 | 0.0% | 0.0% | NO | **YES (Shortest, tied)** |

**Per-Course Giveaway Violations (R2 Acceptance Criteria)**:
1. **Longest Option Threshold**:
   - Count of MC items where correct option is longest: $2 / 3 = \mathbf{66.7\%}$.
   - **Allowed maximum**: $\le 25.0\%$.
   - **Status**: **SEVERE VIOLATION** ($66.7\% > 25\%$).
2. **Shortest Option Threshold**:
   - Count of MC items where correct option is shortest: $1 / 3 = \mathbf{33.3\%}$.
   - **Allowed maximum**: $\le 25.0\%$.
   - **Status**: **SEVERE VIOLATION** ($33.3\% > 25\%$).

#### B. Qualitative Justification Asymmetry
- **`Q-HAB03-ISLM-001`**:
  - Distractor options provide vague assertions:
    - *A*: `"...debido a que el término -\mu c_1 introduce una raíz con parte real estrictamente positiva."`
    - *B*: `"...dado que la velocidad de ajuste del mercado monetario c_2 desestabiliza la traza."`
  - Correct option C provides the entire multi-step proof and all three spectral invariants:
    - *C*: `"Foco asintóticamente estable (espiral convergente), con oscilaciones amortiguadas hacia (Y^E, r^E) porque \text{tr}(A) < 0, \det(A) > 0 y \Delta < 0."`
  - A student or blind LLM guessing agent recognizes option C immediately because it contains the complete mathematical theorem statement.
- **`Q-HAB06-SOLOW-004`**:
  - Correct option E bridges both eigenvalues and the stability theorem:
    - *E*: `"\lambda_1 = \delta(\alpha - 1) < 0 y \lambda_2 = -\gamma < 0; ambos autovalores son reales y estrictamente negativos, por lo que (K^*, P^*) es un nodo asintóticamente estable."`
  - Distractors omit the explicit sign reasoning or omit the bridge sentence.

---

### 2.3 Structural & Architectural Schema Flaws

1. **Missing Top-Level Course Metadata**:
   - The file only defines `"topic_id"`, `"topic_title"`, `"generated_at"`, `"total_questions"`, and `"questions"`.
   - It lacks `schema_version`, `course_id`, `course_title`, `description`, `language`, and the top-level `competencies` array.
2. **Missing Competency Manifest**:
   - Competencies are only referenced ad-hoc inside each question via `"competency_ref": {"id": "...", "name": "...", "category": "..."}`. There is no course-level registry of units/competencies.
3. **Severe Question Count Deficit**:
   - Total questions in file = 7.
   - Requirements from R2: Every Skill competency $\ge 30$ questions; every Fact/Concept competency $\ge 20$ questions.
   - Deficit inventory:
     - `Hab-03` (Skill): 2 questions (deficit: 28)
     - `Hab-02` (Skill): 1 question (deficit: 29)
     - `C-02` (Concept): 1 question (deficit: 19)
     - `Hab-06` (Skill): 1 question (deficit: 29)
     - `Hab-05` (Skill): 1 question (deficit: 29)
     - `Hab-04` (Skill): 1 question (deficit: 29)
   - Minimum questions required to validate this course: $5 \times 30 + 1 \times 20 = \mathbf{170\text{ questions}}$. Deficit: 163 questions!
4. **Missing Graph Definitions**:
   - No declarative representation of function graphs or phase diagrams.

---

## 3. Formal JSON Schema Specification

The course format is versioned as `1.0.0` and validated against JSON Schema Draft-07.

### 3.1 Course Schema (Draft-07)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://khan-on-demand.local/schemas/course-v1.json",
  "title": "OnDemandKhanAcademyCourse",
  "description": "Standardized, versioned JSON format for Top's Academy courses, competencies, and practice banks.",
  "type": "object",
  "required": [
    "schema_version",
    "course_id",
    "course_title",
    "description",
    "language",
    "created_at",
    "competencies",
    "questions"
  ],
  "additionalProperties": false,
  "properties": {
    "schema_version": {
      "type": "string",
      "pattern": "^1\\.[0-9]+\\.[0-9]+$"
    },
    "course_id": {
      "type": "string",
      "pattern": "^[a-z0-9_-]+$"
    },
    "course_title": {
      "type": "string",
      "minLength": 3
    },
    "description": {
      "type": "string",
      "minLength": 10
    },
    "language": {
      "type": "string",
      "pattern": "^[a-z]{2}(-[A-Z]{2})?$"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "competencies": {
      "type": "array",
      "minItems": 1,
      "items": {
        "$ref": "#/definitions/Competency"
      }
    },
    "questions": {
      "type": "array",
      "minItems": 1,
      "items": {
        "$ref": "#/definitions/Question"
      }
    }
  },
  "definitions": {
    "Competency": {
      "type": "object",
      "required": ["id", "name", "category", "description"],
      "additionalProperties": false,
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^(Hab|C|H|Aut)-[0-9]{2,}$"
        },
        "name": {
          "type": "string",
          "minLength": 3
        },
        "category": {
          "type": "string",
          "enum": ["Skill", "Concept", "Fact", "Automation_Seed"]
        },
        "description": {
          "type": "string",
          "minLength": 5
        }
      }
    },
    "Question": {
      "type": "object",
      "required": [
        "id",
        "competency_id",
        "bloom_taxonomy_level",
        "difficulty",
        "interaction_type",
        "context_application",
        "stem",
        "interface_config",
        "options",
        "correct_answer",
        "hints",
        "detailed_solution",
        "common_misconception_warning"
      ],
      "additionalProperties": false,
      "properties": {
        "id": {
          "type": "string",
          "pattern": "^Q-[A-Z0-9_-]+$"
        },
        "competency_id": {
          "type": "string",
          "pattern": "^(Hab|C|H|Aut)-[0-9]{2,}$"
        },
        "competency_ref": {
          "type": "object",
          "properties": {
            "id": { "type": "string" },
            "name": { "type": "string" },
            "category": { "type": "string" }
          }
        },
        "bloom_taxonomy_level": {
          "type": "string",
          "enum": ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
        },
        "difficulty": {
          "type": "string",
          "enum": ["easy", "medium", "hard"]
        },
        "interaction_type": {
          "type": "string",
          "enum": [
            "multiple_choice_7_options",
            "multiple_select",
            "fill_in_the_blank"
          ]
        },
        "context_application": {
          "type": "string",
          "minLength": 3
        },
        "stem": {
          "type": "string",
          "minLength": 10
        },
        "graph": {
          "$ref": "#/definitions/Graph"
        },
        "interface_config": {
          "type": "object",
          "required": [
            "allow_calculator",
            "input_placeholder",
            "expected_format",
            "grading_policy"
          ],
          "additionalProperties": false,
          "properties": {
            "allow_calculator": { "type": "boolean" },
            "input_placeholder": { "type": ["string", "null"] },
            "expected_format": {
              "type": "string",
              "enum": [
                "numeric",
                "fraction",
                "algebraic_expression",
                "single_selection",
                "multiple_selection"
              ]
            },
            "grading_policy": {
              "type": "string",
              "enum": [
                "single_choice",
                "binary_all_or_nothing"
              ]
            }
          }
        },
        "options": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/Option"
          }
        },
        "correct_answer": {
          "type": "object",
          "required": ["value", "accepted_equivalents"],
          "additionalProperties": false,
          "properties": {
            "value": {
              "oneOf": [
                { "type": "string" },
                {
                  "type": "array",
                  "items": { "type": "string" },
                  "minItems": 1
                }
              ]
            },
            "canonical_algebraic": {
              "type": "string",
              "description": "Standard SymPy/mathjs parseable form for algebraic items"
            },
            "accepted_equivalents": {
              "type": "array",
              "items": { "type": "string" }
            }
          }
        },
        "hints": {
          "type": "array",
          "minItems": 3,
          "maxItems": 5,
          "items": {
            "$ref": "#/definitions/Hint"
          }
        },
        "detailed_solution": {
          "type": "string",
          "minLength": 10
        },
        "common_misconception_warning": {
          "type": "string",
          "minLength": 5
        }
      }
    },
    "Option": {
      "type": "object",
      "required": ["option_id", "content", "is_correct", "error_rationale"],
      "additionalProperties": false,
      "properties": {
        "option_id": {
          "type": "string",
          "pattern": "^[A-G]$"
        },
        "content": {
          "type": "string",
          "minLength": 1
        },
        "is_correct": {
          "type": "boolean"
        },
        "error_rationale": {
          "type": ["string", "null"]
        }
      }
    },
    "Hint": {
      "type": "object",
      "required": ["step_number", "title", "content"],
      "additionalProperties": false,
      "properties": {
        "step_number": {
          "type": "integer",
          "minimum": 1
        },
        "title": {
          "type": "string",
          "minLength": 2
        },
        "content": {
          "type": "string",
          "minLength": 5
        }
      }
    },
    "Graph": {
      "type": "object",
      "required": ["x_axis", "y_axis"],
      "additionalProperties": false,
      "properties": {
        "title": { "type": "string" },
        "x_axis": {
          "type": "object",
          "required": ["label", "min", "max"],
          "additionalProperties": false,
          "properties": {
            "label": { "type": "string" },
            "min": { "type": "number" },
            "max": { "type": "number" },
            "step": { "type": "number" }
          }
        },
        "y_axis": {
          "type": "object",
          "required": ["label", "min", "max"],
          "additionalProperties": false,
          "properties": {
            "label": { "type": "string" },
            "min": { "type": "number" },
            "max": { "type": "number" },
            "step": { "type": "number" }
          }
        },
        "curves": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/Curve"
          }
        },
        "points": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/Point"
          }
        },
        "annotations": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["x", "y", "text"],
            "additionalProperties": false,
            "properties": {
              "x": { "type": "number" },
              "y": { "type": "number" },
              "text": { "type": "string" }
            }
          }
        }
      }
    },
    "Curve": {
      "type": "object",
      "required": ["id", "fn"],
      "additionalProperties": false,
      "properties": {
        "id": { "type": "string" },
        "fn": { "type": "string" },
        "label": { "type": "string" },
        "color": { "type": "string" },
        "style": {
          "type": "string",
          "enum": ["solid", "dashed", "dotted"]
        }
      }
    },
    "Point": {
      "type": "object",
      "required": ["x", "y", "style"],
      "additionalProperties": false,
      "properties": {
        "x": { "type": "number" },
        "y": { "type": "number" },
        "style": {
          "type": "string",
          "enum": ["closed", "open"]
        },
        "label": { "type": "string" },
        "color": { "type": "string" }
      }
    }
  }
}
```

---

## 4. Mathematical Equivalence Engine & Grading Policies

R1 and R2 mandate that fill-in-the-blank items are graded by **mathematical equivalence**, not naive string equality.

### 4.1 Evaluation Architecture
Grading of student input $I$ against canonical answer $A$ and accepted equivalents $E$:

1. **Exact String Match**:
   Normalize whitespace and case. If $\text{norm}(I) \in \{\text{norm}(A)\} \cup \{\text{norm}(e) \mid e \in E\}$, return `CORRECT`.
2. **Numeric Equivalence**:
   If $A$ represents a number (integer, decimal, fraction):
   - Evaluate fractions (e.g. `"-2/7"`, `"-10/35"`).
   - Evaluate floats with floating-point tolerance $\epsilon = 10^{-4}$ (e.g. `0.5` matches `1/2`; `-0.2857` matches `-2/7`).
3. **Symbolic Algebraic Equivalence**:
   - Parse canonical answer $A$ and student input $I$ using a symbolic engine (SymPy on server/CLI; SymPy/mathjs on client).
   - Parse LaTeX representations by stripping `\` macros and normalizing standard operations (e.g. `\alpha` $\to$ `alpha`, `\sigma` $\to$ `sigma`, implicit multiplication `\alpha\sigma` $\to$ `alpha*sigma`).
   - Simplify difference:
     $$\Delta = \text{simplify}(I - A)$$
     If $\Delta = 0$, return `CORRECT`.
   - Examples of guaranteed equivalences:
     - `1 - (alpha + n)*sigma` $\equiv$ `1 - alpha*sigma - n*sigma` $\equiv$ `1 - sigma*(alpha + n)` $\equiv$ `1 - \alpha\sigma - n\sigma`.
     - `\frac{1 - (\alpha + n)\sigma}{1}` $\equiv$ `1 - (\alpha + n)\sigma`.
     - `\lambda^2 - 2\lambda - 35` $\equiv$ `(\lambda - 7)(\lambda + 5)`.

### 4.2 Multiple-Select Grading Policy
- **Binary All-or-Nothing**:
  Let $S_{correct} = \{opt\_id \mid option.is\_correct = \text{true}\}$.
  Let $S_{selected} = \{opt\_id \text{ selected by student}\}$.
  $$\text{Grade} = \begin{cases} 1.0 & \text{if } S_{selected} = S_{correct} \\ 0.0 & \text{otherwise} \end{cases}$$
  Selecting any distractor or omitting any correct option yields a grade of zero.

---

## 5. Psychometric Anti-Giveaway Engine

To ensure that questions assess mastery rather than test-taking tricks, the validator enforces two quantitative length rules and qualitative distractor parity constraints.

### 5.1 Formal Definitions & Formulas

For each question $q$ where `interaction_type` is `"multiple_choice_7_options"`:
- Let $O = [o_1, o_2, \dots, o_7]$ be the options.
- Let $o^*$ be the unique option with $o^*.is\_correct = \text{true}$.
- Let $\mathcal{D} = \{o \in O \mid o.is\_correct = \text{false}\}$ be the set of 6 distractors.
- For any option $o$, length is defined as the trimmed character count:
  $$L(o) = \text{length}(o.content.strip())$$
- Let $L_{correct} = L(o^*)$.
- Let $L_{max\_dist} = \max_{d \in \mathcal{D}} L(d)$.
- Let $L_{min\_dist} = \min_{d \in \mathcal{D}} L(d)$.

#### Rule G-01: Per-Item Upper Length Threshold
The correct option cannot be more than $20\%$ longer than the longest distractor.
$$\text{If } L_{correct} > L_{max\_dist}: \quad \frac{L_{correct} - L_{max\_dist}}{L_{max\_dist}} \le 0.20$$
*Violation Trigger*: If $L_{correct} > 1.20 \times L_{max\_dist}$, reject question $q$.

#### Rule G-02: Per-Item Lower Length Threshold
The correct option cannot be more than $20\%$ shorter than the shortest distractor.
$$\text{If } L_{correct} < L_{min\_dist}: \quad \frac{L_{min\_dist} - L_{correct}}{L_{min\_dist}} \le 0.20$$
*Violation Trigger*: If $L_{correct} < 0.80 \times L_{min\_dist}$, reject question $q$.

#### Rule G-03: Per-Course Longest Option Cap
Across the entire course, let $\mathcal{Q}_{MC}$ be the set of all multiple-choice items, with cardinality $N_{MC} = |\mathcal{Q}_{MC}|$.
An item $q$ is defined as "correct is longest" (strictly or tied) if:
$$\text{IsLongest}(q) = [L_{correct} \ge L_{max\_dist}]$$
Let $K_{longest} = \sum_{q \in \mathcal{Q}_{MC}} \mathbb{I}(\text{IsLongest}(q))$.
The proportion of items where the correct option is the longest must not exceed $25\%$:
$$P_{longest} = \frac{K_{longest}}{N_{MC}} \le 0.25$$
*Violation Trigger*: If $P_{longest} > 0.25$, reject the course.

#### Rule G-04: Per-Course Shortest Option Cap
An item $q$ is defined as "correct is shortest" (strictly or tied) if:
$$\text{IsShortest}(q) = [L_{correct} \le L_{min\_dist}]$$
Let $K_{shortest} = \sum_{q \in \mathcal{Q}_{MC}} \mathbb{I}(\text{IsShortest}(q))$.
The proportion of items where the correct option is the shortest must not exceed $25\%$:
$$P_{shortest} = \frac{K_{shortest}}{N_{MC}} \le 0.25$$
*Violation Trigger*: If $P_{shortest} > 0.25$, reject the course.

### 5.2 Qualitative Distractor Parity Rules
1. **Justification Symmetry**:
   - If the correct option includes a causal clause (e.g. `porque...`, `debido a que...`, `dado que...`), all distractors must include a corresponding causal clause of comparable depth based on realistic misconceptions.
   - If distractors do not provide justifications, the correct option must not provide one.
2. **Grammatical Parallelism**:
   - All options must begin with the same grammatical structure (e.g., all nouns, all finite verbs, or all mathematical predicates).
3. **Plausibility & Misconception Grounding**:
   - Distractors must directly address known expert blind spots and canonical algebraic errors (e.g. sign flip in trace, inverted matrix transposition, omitting particular solution). Random or frivolous distractors are prohibited.

---

## 6. Complete Validator Architecture & Rule Inventory

The validator executes as a two-pass CLI tool:
- **Pass 1: Raw Text & Lexical Scanner**: Detects unescaped quotes, unescaped raw newlines, syntax-invalid backslashes, and silent control character corruptions before JSON AST construction.
- **Pass 2: Semantic & Psychometric Analyzer**: Validates schema compliance, relational integrity, question minimum counts, option counts, and anti-giveaway metrics.

### 6.1 Validation Rule Inventory

| Rule ID | Category | Description | Violation Condition | Exit Code | Diagnostic Message Format |
|:---|:---|:---|:---|:---:|:---|
| **R-01** | Lexical | Valid JSON Structure | Malformed syntax, unescaped quotes, unescaped newlines | 1 | `[ERR_INVALID_JSON] File is not valid JSON at line {line}, col {col}: {reason}` |
| **R-02** | Lexical | LaTeX Backslash Syntax | Single backslash followed by non-JSON-escape char | 1 | `[ERR_LATEX_SYNTAX] Invalid escape sequence '\{seq}' at line {line}, col {col}. Must be double-escaped as '\\{seq}'` |
| **R-03** | Lexical | LaTeX Control Char Corruption | Single backslash preceding LaTeX keyword (`\begin`, `\frac`, `\tau`, `\nu`, `\beta`, `\right`) | 1 | `[ERR_LATEX_CORRUPT] LaTeX corruption detected: '\{cmd}' at line {line} has single backslash producing control character (e.g. tab, formfeed, backspace). Must be double-escaped as '\\{cmd}'` |
| **R-04** | Schema | Top-Level Course Metadata | Missing `course_id`, `schema_version`, `competencies`, `questions` | 1 | `[ERR_SCHEMA] Missing required top-level field '{field}'` |
| **R-05** | Integrity | Duplicate Competency IDs | Two competencies share identical `id` | 1 | `[ERR_DUP_COMPETENCY] Duplicate competency ID found: '{id}'` |
| **R-06** | Integrity | Duplicate Question IDs | Two questions share identical `id` | 1 | `[ERR_DUP_QUESTION] Duplicate question ID found: '{id}'` |
| **R-07** | Integrity | Missing Competency Reference | Question references `competency_id` not in `competencies` | 1 | `[ERR_MISSING_COMPETENCY] Question '{q_id}' references unknown competency '{comp_id}'` |
| **R-08** | Count | Minimum Questions: Skill | Skill [Hab] competency has $< 30$ questions | 1 | `[ERR_COUNT_SKILL] Competency '{id}' (category 'Skill') has {count} questions; minimum required is 30` |
| **R-09** | Count | Minimum Questions: Fact/Concept | Fact [H] or Concept [C] competency has $< 20$ questions | 1 | `[ERR_COUNT_CONCEPT] Competency '{id}' (category '{cat}') has {count} questions; minimum required is 20` |
| **R-10** | MC Item | Multiple-Choice Option Count | MC item does not have exactly 7 options | 1 | `[ERR_MC_COUNT] Question '{q_id}' has {n} options; multiple-choice items must have exactly 7 options` |
| **R-11** | MC Item | Multiple-Choice Correct Count | MC item does not have exactly 1 correct option | 1 | `[ERR_MC_CORRECT] Question '{q_id}' has {k} correct options; multiple-choice items must have exactly 1 correct option` |
| **R-12** | MS Item | Multiple-Select Option Count | MS item has $< 4$ or $> 6$ options | 1 | `[ERR_MS_COUNT] Question '{q_id}' has {n} options; multiple-select items must have between 4 and 6 options` |
| **R-13** | MS Item | Multiple-Select Correct Count | MS item has $k < 1$ or $k = n$ correct options | 1 | `[ERR_MS_CORRECT] Question '{q_id}' has {k} correct options out of {n}; multiple-select items must have between 1 and n-1 correct options` |
| **R-14** | Hints | Hint Count Scaffolding | Question has $< 3$ or $> 5$ hints | 1 | `[ERR_HINT_COUNT] Question '{q_id}' has {h} hints; must have between 3 and 5 hints` |
| **R-15** | Giveaway | Per-Item Option Length Symmetry | Correct option $> 20\%$ longer than max distractor or $> 20\%$ shorter than min distractor | 1 | `[ERR_GIVEAWAY_ITEM] Question '{q_id}': correct option length ({len_c}) is {pct:.1f}% {longer/shorter} than {max/min} distractor ({len_d}); maximum allowed difference is 20.0%` |
| **R-16** | Giveaway | Per-Course Longest/Shortest Cap | Correct option is longest in $> 25\%$ of MC items, or shortest in $> 25\%$ | 1 | `[ERR_GIVEAWAY_COURSE] Course '{course_id}': correct option is {longest/shortest} in {k}/{n} ({pct:.1f}%) multiple-choice items; maximum allowed is 25.0%` |

---

## 7. Test Matrix & Acceptance Fixture Catalog

To satisfy the Validator Acceptance Criteria in `ORIGINAL_REQUEST.md`, a suite of automated unit and integration tests must run against 21 discrete test fixtures:

```
fixtures/
├── 01_original_example_unmodified.json      # Fails R-01, R-02, R-03, R-04, R-08, R-09, R-16
├── 02_syntax_malformed_json.json            # Fails R-01 (unclosed brace)
├── 03_syntax_unescaped_quotes.json          # Fails R-01 (inner quotes unescaped)
├── 04_syntax_raw_newlines.json              # Fails R-01 (literal newlines in strings)
├── 05_latex_invalid_escape.json             # Fails R-02 (single backslash \alpha)
├── 06_latex_silent_corruption_tab.json      # Fails R-03 (\tau turns into \t)
├── 07_latex_silent_corruption_formfeed.json # Fails R-03 (\frac turns into \f)
├── 08_latex_silent_corruption_backspace.json# Fails R-03 (\beta turns into \b)
├── 09_schema_missing_course_title.json      # Fails R-04 (missing course_title)
├── 10_duplicate_competency_ids.json         # Fails R-05 (duplicate Hab-01)
├── 11_duplicate_question_ids.json           # Fails R-06 (duplicate Q-001)
├── 12_missing_competency_reference.json     # Fails R-07 (Q-001 references Hab-99)
├── 13_skill_29_questions.json               # Fails R-08 (Skill has exactly 29 questions)
├── 14_concept_19_questions.json             # Fails R-09 (Concept has exactly 19 questions)
├── 15_fact_19_questions.json                # Fails R-09 (Fact has exactly 19 questions)
├── 16_mc_6_options.json                     # Fails R-10 (MC has 6 options instead of 7)
├── 17_mc_8_options.json                     # Fails R-10 (MC has 8 options instead of 7)
├── 18_mc_0_correct.json                     # Fails R-11 (MC has 0 correct options)
├── 19_mc_2_correct.json                     # Fails R-11 (MC has 2 correct options)
├── 20_ms_all_correct.json                   # Fails R-13 (MS has all options correct)
├── 21_ms_0_correct.json                     # Fails R-13 (MS has 0 correct options)
├── 22_hints_2_hints.json                    # Fails R-14 (Question has 2 hints)
├── 23_hints_6_hints.json                    # Fails R-14 (Question has 6 hints)
├── 24_giveaway_item_too_long.json           # Fails R-15 (Correct option 35% longer)
├── 25_giveaway_item_too_short.json          # Fails R-15 (Correct option 30% shorter)
├── 26_giveaway_course_longest_30pct.json    # Fails R-16 (Correct longest in 30% of MC)
├── 27_giveaway_course_shortest_30pct.json   # Fails R-16 (Correct shortest in 30% of MC)
└── 28_valid_complete_course.json            # PASSES ALL RULES (Exit code 0)
```

### 7.1 Detailed Test Matrix

| # | Fixture File | Target Rule | Expected Exit Code | Expected Diagnostic Substring |
|:---:|:---|:---:|:---:|:---|
| 1 | `01_original_example_unmodified.json` | R-01, R-02, R-03, R-08, R-16 | `1` | `[ERR_INVALID_JSON]` or `[ERR_LATEX_SYNTAX]` |
| 2 | `02_syntax_malformed_json.json` | R-01 | `1` | `[ERR_INVALID_JSON]` |
| 3 | `03_syntax_unescaped_quotes.json` | R-01 | `1` | `[ERR_INVALID_JSON]` |
| 4 | `04_syntax_raw_newlines.json` | R-01 | `1` | `[ERR_INVALID_JSON]` |
| 5 | `05_latex_invalid_escape.json` | R-02 | `1` | `[ERR_LATEX_SYNTAX] Invalid escape sequence '\alpha'` |
| 6 | `06_latex_silent_corruption_tab.json` | R-03 | `1` | `[ERR_LATEX_CORRUPT] LaTeX corruption detected: '\tau'` |
| 7 | `07_latex_silent_corruption_formfeed.json` | R-03 | `1` | `[ERR_LATEX_CORRUPT] LaTeX corruption detected: '\frac'` |
| 8 | `08_latex_silent_corruption_backspace.json` | R-03 | `1` | `[ERR_LATEX_CORRUPT] LaTeX corruption detected: '\beta'` |
| 9 | `09_schema_missing_course_title.json` | R-04 | `1` | `[ERR_SCHEMA] Missing required top-level field 'course_title'` |
| 10 | `10_duplicate_competency_ids.json` | R-05 | `1` | `[ERR_DUP_COMPETENCY] Duplicate competency ID found: 'Hab-01'` |
| 11 | `11_duplicate_question_ids.json` | R-06 | `1` | `[ERR_DUP_QUESTION] Duplicate question ID found: 'Q-001'` |
| 12 | `12_missing_competency_reference.json` | R-07 | `1` | `[ERR_MISSING_COMPETENCY] Question 'Q-001' references unknown competency 'Hab-99'` |
| 13 | `13_skill_29_questions.json` | R-08 | `1` | `[ERR_COUNT_SKILL] Competency 'Hab-01' (category 'Skill') has 29 questions; minimum required is 30` |
| 14 | `14_concept_19_questions.json` | R-09 | `1` | `[ERR_COUNT_CONCEPT] Competency 'C-01' (category 'Concept') has 19 questions; minimum required is 20` |
| 15 | `15_fact_19_questions.json` | R-09 | `1` | `[ERR_COUNT_CONCEPT] Competency 'H-01' (category 'Fact') has 19 questions; minimum required is 20` |
| 16 | `16_mc_6_options.json` | R-10 | `1` | `[ERR_MC_COUNT] Question 'Q-001' has 6 options; multiple-choice items must have exactly 7 options` |
| 17 | `17_mc_8_options.json` | R-10 | `1` | `[ERR_MC_COUNT] Question 'Q-001' has 8 options; multiple-choice items must have exactly 7 options` |
| 18 | `18_mc_0_correct.json` | R-11 | `1` | `[ERR_MC_CORRECT] Question 'Q-001' has 0 correct options` |
| 19 | `19_mc_2_correct.json` | R-11 | `1` | `[ERR_MC_CORRECT] Question 'Q-001' has 2 correct options` |
| 20 | `20_ms_all_correct.json` | R-13 | `1` | `[ERR_MS_CORRECT] Question 'Q-001' has 5 correct options out of 5; multiple-select items must have between 1 and n-1` |
| 21 | `21_ms_0_correct.json` | R-13 | `1` | `[ERR_MS_CORRECT] Question 'Q-001' has 0 correct options out of 5` |
| 22 | `22_hints_2_hints.json` | R-14 | `1` | `[ERR_HINT_COUNT] Question 'Q-001' has 2 hints; must have between 3 and 5 hints` |
| 23 | `23_hints_6_hints.json` | R-14 | `1` | `[ERR_HINT_COUNT] Question 'Q-001' has 6 hints; must have between 3 and 5 hints` |
| 24 | `24_giveaway_item_too_long.json` | R-15 | `1` | `[ERR_GIVEAWAY_ITEM] Question 'Q-001': correct option length` |
| 25 | `25_giveaway_item_too_short.json` | R-15 | `1` | `[ERR_GIVEAWAY_ITEM] Question 'Q-001': correct option length` |
| 26 | `26_giveaway_course_longest_30pct.json` | R-16 | `1` | `[ERR_GIVEAWAY_COURSE] Course 'demo': correct option is longest in 3/10 (30.0%)` |
| 27 | `27_giveaway_course_shortest_30pct.json` | R-16 | `1` | `[ERR_GIVEAWAY_COURSE] Course 'demo': correct option is shortest in 3/10 (30.0%)` |
| 28 | `28_valid_complete_course.json` | All | `0` | `VALID: Course 'demo' passed all 16 validation rules` |

---

## 8. CLI Specification for the Validator

The validator must be executable as a standalone command and callable programmatically:

```bash
# Validate single file
python -m validator path/to/course.json

# Validate entire directory of courses
python -m validator courses/

# JSON output for automated integration pipelines
python -m validator --json path/to/course.json
```

### Exit Codes:
- `0`: All files strictly valid.
- `1`: One or more validation rules violated.
- `2`: File not found or unreadable IO error.

### CLI Diagnostic Output Example:
```
[VALIDATION FAILURE] courses/incomplete_course.json
  Rule R-08 [ERR_COUNT_SKILL]: Competency 'Hab-01' (category 'Skill') has 29 questions; minimum required is 30.
  Rule R-15 [ERR_GIVEAWAY_ITEM]: Question 'Q-HAB01-014': correct option length (148) is 24.4% longer than max distractor (119); maximum allowed difference is 20.0%.
  Rule R-16 [ERR_GIVEAWAY_COURSE]: Course 'incomplete_course': correct option is longest in 9/30 (30.0%) multiple-choice items; maximum allowed is 25.0%.
FAILED: 3 errors detected.
```
