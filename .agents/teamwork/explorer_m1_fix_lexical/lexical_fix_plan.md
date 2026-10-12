# Lexical Corruption Remediation Plan: Watertight Fix Strategy for Rules R-03 and R-02

**Document ID**: `M1-LEXICAL-FIX-PLAN`  
**Author**: Explorer 1 (`explorer_m1_fix_lexical`)  
**Target Milestone**: Milestone 1 (Exercise Bank Format & Validator, R2)  
**Date**: 2026-10-11T01:40:00Z  
**Status**: PROPOSAL / READY FOR IMPLEMENTATION  

---

## 1. Executive Summary & Problem Statement

During the Milestone 1 Gate review, Reviewer 2, Challenger 1, and Challenger 2 issued unanimous **REQUEST_CHANGES** verdicts due to critical blind spots in the Pass 1 pre-parse lexical scanner (`src/validator/lexical_scanner.py`).

### 1.1 The Vulnerability
Requirement R2 mandates:
> *"The validator must reject: invalid JSON; schema violations; LaTeX backslash corruption (including silently-valid escapes that produce control characters)"*

Under RFC 8259 Section 7, the characters `\b`, `\f`, `\n`, `\r`, and `\t` are valid JSON escape sequences that decode to ASCII control characters:
- `\b` -> Backspace (0x08)
- `\f` -> Form Feed (0x0C)
- `\n` -> Line Feed / Newline (0x0A)
- `\r` -> Carriage Return (0x0D)
- `\t` -> Character Tabulation / Tab (0x09)

When course creators or automated LLM generation pipelines produce exercise banks containing LaTeX math formulas (e.g. `$x \ne y$`, `\norm{v}`, `\boxed{ans}`, `\therefore`, `\bigcap A_i`), omitting double-backslashes causes the leading backslash and initial letter to form a valid JSON escape. 

Because `src/validator/lexical_scanner.py` relied on a narrow, hardcoded whitelist in `LATEX_CONTROL_PREFIXES`, any LaTeX command whose first letter is `b`, `f`, `n`, `r`, or `t` that was omitted from the whitelist was treated as a valid JSON escape. The scanner silently advanced past the escape, and downstream JSON parsers (`json.loads`) decoded the command into a corrupted control byte followed by truncated letters:
- `\ne 0` -> `<0x0A>e 0` (Newline + "e 0")
- `\not=` -> `<0x0A>ot=` (Newline + "ot=")
- `\norm{x}` -> `<0x0A>orm{x}` (Newline + "orm{x}")
- `\boxed{x}` -> `<0x08>oxed{x}` (Backspace + "oxed{x}")
- `\therefore` -> `<0x09>herefore` (Tab + "herefore")
- `\thickspace` -> `<0x09>hickspace` (Tab + "hickspace")
- `\textcolor{red}{x}` -> `<0x09>extcolor{red}{x}` (Tab + "extcolor{red}{x}")
- `\bigcap` -> `<0x08>igcap` (Backspace + "igcap")
- `\bigcup` -> `<0x08>igcup` (Backspace + "igcup")
- `\bigoplus` -> `<0x08>igoplus` (Backspace + "igoplus")
- `\bigotimes` -> `<0x08>igotimes` (Backspace + "igotimes")
- `\rank` -> `<0x0D>ank` (Carriage return + "ank")
- `\bm{v}` -> `<0x08>m{v}` (Backspace + "m{v}")
- `\tr(A)` -> `<0x09>r(A)` (Tab + "r(A)")
- `\ref{eq1}` -> `<0x0D>ef{eq1}` (Carriage return + "ef{eq1}")
- `\newline` -> `<0x0A>ewline` (Newline + "ewline")

When delivered to the practice platform (Milestone 2), KaTeX crashes on these corrupted strings, breaking the user interface.

### 1.2 Empirical Failure Baseline
- In `tests/test_adversarial_validator.py`: **11 failures** in `TestAdversarialLatex::test_unescaped_latex_command_starting_with_control_prefix`.
- In `tests/validator/test_empirical_stress.py`: **2 failures** in `test_fn_latex_newline_command_escape` and `test_fn_latex_not_command_escape`.
- Reviewer 2 review: Flagged `\bm`, `\tr`, `\ref`, `\ne`, `\not`.

---

## 2. Root Cause Analysis in `src/validator/lexical_scanner.py`

### 2.1 The Fallthrough Bug (Lines 210–213)
In `scan_lexical()`:
```python
if next_ch in LATEX_CONTROL_PREFIXES:
    word_match = re.match(r"^[a-zA-Z]+", raw_text[pos:])
    if word_match:
        word = word_match.group(0)
        known_commands = LATEX_CONTROL_PREFIXES[next_ch]
        if word.lower() in known_commands or word in known_commands:
            # Emit R-03 error...
            continue

    # FATAL FLAW: Fallthrough assumes any unknown word is a legitimate JSON escape!
    if next_ch in ("b", "f", "n", "r", "t"):
        pos += 1
        continue
```
When `word` was not in `known_commands`, line 211 treated the sequence as a valid JSON escape (`\b`, `\f`, `\n`, `\r`, `\t`) and advanced `pos += 1`. This allowed corrupted LaTeX commands to slip directly into the parsed AST.

### 2.2 Exact Token Matching Bug
In `LATEX_CONTROL_PREFIXES["b"]`, `"box"` was included, but `"boxed"` was not.
Because `word_match = re.match(r"^[a-zA-Z]+", raw_text[pos:])` captures `"boxed"`, `"boxed"` did not match `"box"`. The scanner failed to recognize `"boxed"` as a variation or separate command, falling through to silent corruption.

### 2.3 Dead Code Bug (Lines 95–131)
In lines 95–106:
```python
if ch in ("\n", "\r"):
    # Emits R-01 error and calls continue!
    pos += 1
    continue
```
In lines 108–141:
```python
byte_val = ord(ch)
if byte_val < 32:
    if byte_val in CONTROL_CHAR_TO_LATEX:
        ...
```
Because `\n` (0x0A) and `\r` (0x0D) are intercepted by lines 95–106 and immediately trigger `continue`, the `CONTROL_CHAR_TO_LATEX` logic for `0x0A` and `0x0D` can never execute under any circumstances. Furthermore, literal control characters < 32 inside raw JSON strings violate RFC 8259 (R-01); silent LaTeX corruption happens when backslashes are encoded in ASCII text as `\` followed by `[bfnrt]`, not as raw bytes < 32 in the source file.

### 2.4 Prefix `v` and `0` Tokenization Truncation (Lines 215–226)
In RFC 8259, `\v` and `\0` are NOT valid JSON escape sequences.
In lines 215–226:
```python
line, col = get_line_col(raw_text, esc_pos)
seq = "\\" + next_ch  # Sets seq to "\v" or "\0" rather than the full word "\varpi"!
errors.append(ValidationError(
    rule_id="R-02",
    code="ERR_LATEX_SYNTAX",
    message=f"Invalid escape sequence '{seq}' at line {line}, col {col}. Must be double-escaped as '\\{seq}'",
    line=line,
    col=col
))
pos += 1  # Leaves the rest of the word "arpi" in raw_text!
continue
```
If a command like `\varpi` or `\vert` is not in `LATEX_CONTROL_PREFIXES["v"]`, it produces an error message mentioning only `'\v'` rather than `'\varpi'`, and advances by only 1 character instead of the entire token.

---

## 3. Comprehensive LaTeX Command Taxonomy for Prefixes `b`, `f`, `n`, `r`, `t`, `v`, `0`

To guarantee zero false negatives, the command dictionary must cover all standard AMS-LaTeX, KaTeX, `mathtools`, and physics macros. Below is the complete catalog:

### 3.1 Prefix `b` (JSON `\b` -> Backspace 0x08)
```python
"b": {
    # Environments & Matrices
    "begin", "bmatrix", "Bmatrix", "bordermatrix", "bmod", "bgroup",
    # Fonts & Math Styles
    "beta", "bar", "bold", "boldsymbol", "mathbf", "mathbb", "mathbfit",
    "mathbffrak", "mathbfscr", "mathbfsf", "mathbaseline", "bm", "bf", "bfseries",
    # Sizing Delimiters & Large Operators
    "big", "Big", "bigg", "Bigg", "bigl", "Bigl", "biggl", "Biggl",
    "bigr", "Bigr", "biggr", "Biggr", "bigm", "Bigm", "biggm", "Biggm",
    "bigcap", "bigcup", "bigodot", "bigoplus", "bigotimes", "bigsqcup",
    "biguplus", "bigvee", "bigwedge",
    # Accents, Boxes & Spacing
    "breve", "bullet", "bot", "backslash", "bigskip", "break",
    "box", "boxed", "boxdot", "boxplus", "boxminus", "boxtimes", "boxempty",
    # Symbols & Relations
    "binom", "brace", "brack", "bowtie", "bra", "because", "between",
    "barwedge", "beth", "blacklozenge", "blacksquare", "blacktriangle",
    "blacktriangledown", "blacktriangleleft", "blacktriangleright",
    "bumpeq", "Bumpeq", "backprime", "backsim", "backsimeq", "bkarrow", "by"
}
```

### 3.2 Prefix `f` (JSON `\f` -> Form Feed 0x0C)
```python
"f": {
    # Fractions & Operators
    "frac", "flat", "forall", "frown",
    # Boxes, Frames & Layout
    "fbox", "framebox", "fcolorbox", "flalign",
    # Fonts & Notes
    "footnotesize", "footnote", "footnotemark", "footnotetext", "frak",
    # Symbols
    "fallingdotseq"
}
```

### 3.3 Prefix `n` (JSON `\n` -> Line Feed 0x0A)
```python
"n": {
    # Negations & Logical Relations
    "ne", "neq", "neg", "not", "notin", "ni", "nexists", "nparallel",
    "ncong", "nshortmid", "nshortparallel", "nmid", "nequiv", "nasymp",
    "napprox", "nbumpeq", "nsim",
    # Inequality & Ordering Negations
    "nleq", "ngeq", "nless", "ngtr", "nprec", "nsucc", "npreceq", "nsucceq",
    # Subset & Superset Negations
    "nsubseteq", "nsubseteqq", "nsupseteq", "nsupseteqq", "nsqsubseteq", "nsqsupseteq",
    # Triangle Negations
    "ntriangleleft", "ntriangleright", "ntrianglelefteq", "ntrianglerighteq",
    # Arrow Negations
    "nLeftarrow", "nRightarrow", "nLeftrightarrow",
    "nleftarrow", "nrightarrow", "nleftrightarrow",
    # Turnstile Negations
    "nvdash", "nvDash", "nVdash", "nVDash",
    # Greek & Calculus / Vectors
    "nu", "nabla", "natural", "nearrow", "nwarrow", "norm",
    # Layout & Text Commands
    "newline", "noindent", "nonumber", "normalsize", "nobreak", "nopagebreak", "null",
    # Macro Declarations
    "newcommand", "newenvironment", "newtheorem", "newcolumntype", "nocite"
}
```

### 3.4 Prefix `r` (JSON `\r` -> Carriage Return 0x0D)
```python
"r": {
    # Delimiters & Roots
    "right", "root", "rangle", "rceil", "rfloor", "rbrace", "rbrack",
    # Greek, Functions & Operators
    "rho", "Re", "rank", "real", "restriction", "ring",
    # Arrows
    "rightarrow", "Rightarrow", "rightleftharpoons", "rightharpoonup", "rightharpoondown",
    "rightleftarrows", "rightrightarrows", "rightsquigarrow", "rightarrowtail", "rightthreetimes",
    "risingdotseq",
    # Text, Fonts & Cross-referencing
    "ref", "relax", "rm", "rmfamily", "rule", "raisebox", "require",
    "renewcommand", "renewenvironment"
}
```

### 3.5 Prefix `t` (JSON `\t` -> Tab 0x09)
```python
"t": {
    # Greek, Trig & Functions
    "tau", "theta", "times", "tilde", "to", "top", "tan", "tanh",
    "tfrac", "tbinom", "triangle", "triangledown", "triangleleft", "triangleright", "triangleq",
    "tr",
    # Text & Fonts
    "text", "textbf", "textit", "texttt", "textsf", "textcolor",
    "textnormal", "textup", "textsl", "textsc", "textmd", "textstyle",
    # Symbols & Spacing
    "therefore", "thickspace", "thinspace", "thickapprox", "thicksim",
    "tag", "tiny", "tensor", "twoheadrightarrow", "twoheadleftarrow", "the"
}
```

### 3.6 Prefix `v` (Non-standard / Math Vector commands)
```python
"v": {
    "vec", "vert", "Vert", "vspace", "vline", "vcenter", "vphantom",
    "varDelta", "varGamma", "varTheta", "varLambda", "varXi", "varPi",
    "varSigma", "varUpsilon", "varPhi", "varPsi", "varOmega",
    "varepsilon", "varkappa", "varphi", "varpi", "varrho", "varsigma", "vartheta"
}
```

### 3.7 Prefix `0`
```python
"0": {
    "0"
}
```

---

## 4. Multi-Layer Watertight Defense Architecture

A static dictionary alone is powerful, but a truly watertight lexical scanner should combine multiple layers of defense to prevent zero-day omissions or custom macro leaks while strictly avoiding false positives on legitimate formatted JSON strings.

```
                              ┌─────────────────────────────┐
                              │ Character '\\' encountered  │
                              └──────────────┬──────────────┘
                                             │
                       ┌─────────────────────┴─────────────────────┐
                       ▼                                           ▼
             Next char is '\\'                           Next char is NOT '\\'
             (Escaped backslash: \\)                               │
             Advance pos += 2; PASS                                │
                                                                   ▼
                                                 ┌───────────────────────────────────┐
                                                 │ Is next_ch in ('"', '/')?         │
                                                 │ -> Standard JSON escape: PASS     │
                                                 │                                   │
                                                 │ Is next_ch == 'u'?                │
                                                 │ -> Check 4 hex digits (\uXXXX)    │
                                                 └─────────────────┬─────────────────┘
                                                                   │
                                   ┌───────────────────────────────┴───────────────────────────────┐
                                   ▼                                                               ▼
                     Next char in ('b','f','n','r','t')                             Next char NOT in ('b','f','n','r','t')
                                   │                                                               │
     ┌─────────────────────────────┴─────────────────────────────┐                                 ▼
     │                                                           │                   Syntax-Invalid Escape:
     ▼                                                           ▼                   Extract token [a-zA-Z]+
Layer 1: Command matches dictionary?                       Layer 2: Inside Math      Report R-02 (ERR_LATEX_SYNTAX)
(e.g. \norm, \ne, \not, \therefore, \boxed, \tr, ...)      Mode ($...$ or $$...$$)?
-> Report R-03 (ERR_LATEX_CORRUPT)                         and followed by letters?
                                                           -> Report R-03 (ERR_LATEX_CORRUPT)
     │                                                           │
     └─────────────────────────────┬─────────────────────────────┘
                                   │ (Neither Layer 1 nor 2)
                                   ▼
     ┌───────────────────────────────────────────────────────────┐
     │ Layer 3: Next char is 'b', 'f', or 'r' followed by letter?│
     │ -> Backspace/formfeed/lone CR before letter is corrupt!  │
     │    Report R-03 (ERR_LATEX_CORRUPT)                        │
     │                                                           │
     │ Layer 4: Next char followed by syntax '{', '[', '_', '^'? │
     │ (e.g. \custommacro{arg})                                  │
     │ -> Report R-03 (ERR_LATEX_CORRUPT)                        │
     │                                                           │
     │ Otherwise: Valid JSON escape (\n newline, \t tab)         │
     │ Advance pos += 1; PASS                                    │
     └───────────────────────────────────────────────────────────┘
```

### Layer 1: Comprehensive Dictionary Matching
Extract the word following the backslash using `re.match(r"^[a-zA-Z]+", raw_text[pos:])`.
If `word.lower()` or `word` matches `LATEX_CONTROL_PREFIXES[next_ch]`:
- Flag `R-03: ERR_LATEX_CORRUPT`
- Advance `pos += len(word)`

### Layer 2: Math Mode Context Tracking (`in_math`)
Track `in_math` state across single (`$`) and display (`$$`) delimiters within string literals.
Inside math mode:
- Legitimate JSON formatting escapes like `\n` or `\t` are never used before ASCII words.
- If `next_ch in ('b', 'f', 'n', 'r', 't')` and is immediately followed by ANY alphabetic characters `[a-zA-Z]+`:
  Flag `R-03: ERR_LATEX_CORRUPT` immediately, even if the command is an obscure or unlisted macro.
- Advances `pos += len(word)`.

### Layer 3: Inherent Control Byte Heuristic (`\b`, `\f`, `\r`)
Outside math mode:
- In educational course JSON, ASCII backspace (`\b`), form feed (`\f`), and carriage return (`\r`) are never followed immediately by letters.
- If `next_ch in ('b', 'f', 'r')` and `re.match(r"^[a-zA-Z]+", raw_text[pos:])` matches a token of length >= 2:
  Flag `R-03: ERR_LATEX_CORRUPT`.

### Layer 4: Structural Syntax Signatures
Outside math mode, if `next_ch in ('n', 't')`:
If the token is immediately followed by `{` (e.g. `\customcmd{x}`) or `[` or `_` or `^`:
- Flag `R-03: ERR_LATEX_CORRUPT`.

### Safe Fallthrough for Legitimate JSON Formatting
If `next_ch == 'n'` or `'t'` outside math mode, and the word does not match the dictionary and does not have LaTeX structural signatures (e.g. `"Linea uno\nLinea dos"`, `"\tDescription"`):
- Treated as a valid JSON escape.
- Advance `pos += 1`.
- Zero false positives!

---

## 5. Watertight Fix Strategy for Rule R-02 (Syntax-Invalid Escapes)

For characters that are NOT valid JSON escapes (letters other than `"`, `\`, `/`, `b`, `f`, `n`, `r`, `t`, `u`):
1. **Full Word Tokenization**:
   Extract the entire command token via `re.match(r"^[a-zA-Z]+", raw_text[pos:])`.
   - Example: For `\Delta`, token is `"Delta"`, `seq = "\\Delta"`.
   - Example: For `\varpi`, token is `"varpi"`, `seq = "\\varpi"`.
   - Example: For non-word symbols like `\{`, `seq = "\\{"`.
2. **Correct Position Advancement**:
   Advance `pos += len(token)` (or `pos += 1` if non-word). This prevents trailing letters (like `"elta"` from `\Delta`) from being erroneously processed as plain string characters.
3. **Prefix `v` and `0` Alignment**:
   In `LATEX_CONTROL_PREFIXES`, `v` commands can either be flagged as R-03 (as currently structured in `lexical_scanner.py`) or R-02. In either case, the entire token (e.g. `\vec`, `\vert`) is captured and reported with line and column numbers.

---

## 6. Dead Code Clean-Up

In `src/validator/lexical_scanner.py`:
1. Remove unreachable branches in `CONTROL_CHAR_TO_LATEX` for `0x0A` (`\n`) and `0x0D` (`\r`), or reorder checks such that unescaped raw newlines in string literals trigger `R-01: ERR_INVALID_JSON` consistently while any unescaped ASCII control character < 32 triggers `R-01`.
2. Ensure `ord(ch) < 32` checks don't shadow or mask pre-parse backslash scans.

---

## 7. Concrete Implementation Blueprint for `src/validator/lexical_scanner.py`

Below is the complete, drop-in replacement implementation blueprint for `src/validator/lexical_scanner.py`:

```python
"""Lexical Scanner (Pass 1).

Performs a pre-parse lexical scan on the raw file text to detect:
1. Syntax-invalid JSON escape sequences (R-02, e.g. \\Delta, \\sigma, \\alpha).
2. Silent control character escapes where LaTeX commands were accidentally unescaped
   (R-03, e.g. \\text, \\frac, \\nu, \\tau, \\rho, \\beta, \\theta, \\ne, \\not, \\norm, \\boxed, \\therefore).
3. Raw unescaped newlines and control characters inside string literals (R-01).
"""
from __future__ import annotations

import re
from typing import Optional
from .models import ValidationError

# Comprehensive catalog of LaTeX commands starting with characters
# that form valid JSON control escapes (b, f, n, r, t) or non-standard escapes (v, 0)
LATEX_CONTROL_PREFIXES: dict[str, set[str]] = {
    "b": {
        "begin", "beta", "bar", "bmatrix", "Bmatrix", "bmod", "boldsymbol", "binom",
        "breve", "bullet", "bot", "big", "Big", "bigg", "Bigg", "bold",
        "backslash", "bigskip", "bordermatrix", "box", "boxed", "bm", "bf", "bfseries",
        "mathbf", "mathbb", "mathbfit", "mathbffrak", "mathbfscr", "mathbfsf", "mathbaseline",
        "bigl", "Bigl", "biggl", "Biggl", "bigr", "Bigr", "biggr", "Biggr",
        "bigm", "Bigm", "biggm", "Biggm", "bigcap", "bigcup", "bigodot", "bigoplus",
        "bigotimes", "bigsqcup", "biguplus", "bigvee", "bigwedge", "bowtie", "bra",
        "brace", "brack", "because", "between", "barwedge", "beth", "bgroup", "break",
        "blacklozenge", "blacksquare", "blacktriangle", "blacktriangledown",
        "blacktriangleleft", "blacktriangleright", "bumpeq", "Bumpeq", "backprime",
        "backsim", "backsimeq", "bkarrow", "boxdot", "boxplus", "boxminus", "boxtimes", "boxempty"
    },
    "f": {
        "frac", "forall", "flat", "frown", "fbox", "footnotesize", "framebox",
        "footnote", "footnotemark", "footnotetext", "frak", "fallingdotseq",
        "fcolorbox", "flalign"
    },
    "n": {
        "nu", "nabla", "neq", "ne", "neg", "not", "notin", "ni", "nsubseteq", "nexists",
        "natural", "nearrow", "nwarrow", "normalsize", "nparallel", "noindent", "nonumber",
        "norm", "newline", "ncong", "nshortmid", "nshortparallel", "nmid", "nequiv",
        "nasymp", "napprox", "nbumpeq", "nsim", "nleq", "ngeq", "nless", "ngtr",
        "nprec", "nsucc", "npreceq", "nsucceq", "nsubseteqq", "nsupseteq", "nsupseteqq",
        "nsqsubseteq", "nsqsupseteq", "ntriangleleft", "ntriangleright", "ntrianglelefteq",
        "ntrianglerighteq", "nLeftarrow", "nRightarrow", "nLeftrightarrow",
        "nleftarrow", "nrightarrow", "nleftrightarrow", "nvdash", "nvDash", "nVdash", "nVDash",
        "nobreak", "nopagebreak", "null", "newcommand", "newenvironment", "newtheorem"
    },
    "r": {
        "right", "rho", "rangle", "rceil", "rfloor", "rightarrow", "Rightarrow", "Re", "root",
        "rank", "ref", "real", "rbrace", "rbrack", "restriction", "ring",
        "rightleftharpoons", "rightharpoonup", "rightharpoondown", "rightleftarrows",
        "rightrightarrows", "rightsquigarrow", "rightarrowtail", "rightthreetimes",
        "risingdotseq", "rm", "rmfamily", "rule", "raisebox", "require", "relax",
        "renewcommand", "renewenvironment"
    },
    "t": {
        "tau", "theta", "text", "times", "tilde", "to", "top", "tan", "tanh",
        "triangle", "tfrac", "textbf", "textit", "texttt", "textsf", "tag", "tiny",
        "thinspace", "thickspace", "therefore", "textcolor", "textnormal", "textup",
        "textsl", "textsc", "textmd", "textstyle", "tr", "tbinom", "tensor",
        "thickapprox", "thicksim", "twoheadrightarrow", "twoheadleftarrow",
        "triangledown", "triangleleft", "triangleright", "triangleq"
    },
    "v": {
        "vec", "vert", "Vert", "vspace", "vline", "vcenter", "vphantom",
        "varDelta", "varGamma", "varTheta", "varLambda", "varXi", "varPi",
        "varSigma", "varUpsilon", "varPhi", "varPsi", "varOmega",
        "varepsilon", "varkappa", "varphi", "varpi", "varrho", "varsigma", "vartheta"
    },
    "0": {
        "0"
    }
}


def get_line_col(text: str, pos: int) -> tuple[int, int]:
    """Calculates 1-based (line, col) for a given character index."""
    line = text.count("\n", 0, pos) + 1
    last_nl = text.rfind("\n", 0, pos)
    col = pos + 1 if last_nl == -1 else pos - last_nl
    return line, col


def scan_lexical(raw_text: str) -> list[ValidationError]:
    """Scans raw file text before JSON parsing and returns all detected lexical errors."""
    errors: list[ValidationError] = []
    n = len(raw_text)
    pos = 0
    in_string = False
    in_math = False
    string_start_pos = 0

    while pos < n:
        ch = raw_text[pos]

        if not in_string:
            if ch == '"':
                in_string = True
                in_math = False
                string_start_pos = pos
                pos += 1
            else:
                pos += 1
            continue

        # --- Inside string literal ---
        if ch == '"':
            # End of string literal
            in_string = False
            in_math = False
            pos += 1
            continue

        # Math mode toggle tracking within string literal
        if ch == '$':
            # Check for $$ or $
            if pos + 1 < n and raw_text[pos + 1] == '$':
                in_math = not in_math
                pos += 2
                continue
            else:
                in_math = not in_math
                pos += 1
                continue

        # Check for unescaped raw newlines inside string literal (RFC 8259 Section 9 violation)
        if ch in ("\n", "\r"):
            line, col = get_line_col(raw_text, pos)
            errors.append(ValidationError(
                rule_id="R-01",
                code="ERR_INVALID_JSON",
                message=f"File is not valid JSON at line {line}, col {col}: Unescaped raw newline inside string literal",
                line=line,
                col=col
            ))
            pos += 1
            continue

        # Check for literal ASCII control characters (< 32)
        byte_val = ord(ch)
        if byte_val < 32:
            line, col = get_line_col(raw_text, pos)
            errors.append(ValidationError(
                rule_id="R-01",
                code="ERR_INVALID_JSON",
                message=f"File is not valid JSON at line {line}, col {col}: Unescaped control character (ASCII {byte_val:#04x}) inside string literal",
                line=line,
                col=col
            ))
            pos += 1
            continue

        # Handle backslash escapes
        if ch == "\\":
            esc_pos = pos
            pos += 1
            if pos >= n:
                line, col = get_line_col(raw_text, esc_pos)
                errors.append(ValidationError(
                    rule_id="R-01",
                    code="ERR_INVALID_JSON",
                    message=f"File is not valid JSON at line {line}, col {col}: Trailing backslash in string literal",
                    line=line,
                    col=col
                ))
                break

            next_ch = raw_text[pos]

            if next_ch == "\\":
                # Escaped backslash: \\
                pos += 1
                continue

            if next_ch in ('"', "/"):
                # Escaped quote or solidus
                pos += 1
                continue

            if next_ch == "u":
                # Unicode escape: \uXXXX
                hex_part = raw_text[pos + 1:pos + 5]
                if len(hex_part) == 4 and all(c in "0123456789abcdefABCDEF" for c in hex_part):
                    pos += 5
                else:
                    line, col = get_line_col(raw_text, esc_pos)
                    errors.append(ValidationError(
                        rule_id="R-01",
                        code="ERR_INVALID_JSON",
                        message=f"File is not valid JSON at line {line}, col {col}: Invalid unicode escape sequence",
                        line=line,
                        col=col
                    ))
                    pos += 1
                continue

            # Check if next_ch is one of b, f, n, r, t, v, 0
            if next_ch in LATEX_CONTROL_PREFIXES:
                word_match = re.match(r"^[a-zA-Z]+", raw_text[pos:])
                if word_match:
                    word = word_match.group(0)
                    known_commands = LATEX_CONTROL_PREFIXES[next_ch]

                    # Multi-layer detection:
                    # Layer 1: Dictionary match
                    is_known = (word in known_commands or word.lower() in {c.lower() for c in known_commands})

                    # Layer 2: Inside math mode, any command is an unescaped LaTeX command
                    is_math_cmd = in_math and len(word) >= 2

                    # Layer 3: Non-text control characters (\b, \f, \r) followed by letters
                    is_inherent_control = next_ch in ("b", "f", "r") and len(word) >= 2

                    # Layer 4: Followed by LaTeX arguments or syntax ({, [, _, ^, =, <, >)
                    rest_idx = pos + len(word)
                    has_syntax_sig = (
                        rest_idx < n and raw_text[rest_idx] in ("{", "[", "_", "^", "=", "<", ">", "\\")
                    )

                    if is_known or is_math_cmd or is_inherent_control or has_syntax_sig:
                        line, col = get_line_col(raw_text, esc_pos)
                        cmd = "\\" + word
                        errors.append(ValidationError(
                            rule_id="R-03",
                            code="ERR_LATEX_CORRUPT",
                            message=(
                                f"LaTeX corruption detected: '{cmd}' at line {line} has single backslash "
                                f"producing control character (e.g. tab, formfeed, backspace). "
                                f"Must be double-escaped as '\\{cmd}'"
                            ),
                            line=line,
                            col=col
                        ))
                        pos += len(word)
                        continue

                # If not a recognized LaTeX command, next_ch in (b, f, n, r, t) is a valid JSON escape
                if next_ch in ("b", "f", "n", "r", "t"):
                    pos += 1
                    continue

                # If next_ch is 'v' or '0', it's not a standard JSON escape -> Rule R-02
                line, col = get_line_col(raw_text, esc_pos)
                word_match = re.match(r"^[a-zA-Z0-9]+", raw_text[pos:])
                token = word_match.group(0) if word_match else next_ch
                seq = "\\" + token
                errors.append(ValidationError(
                    rule_id="R-02",
                    code="ERR_LATEX_SYNTAX",
                    message=f"Invalid escape sequence '{seq}' at line {line}, col {col}. Must be double-escaped as '\\{seq}'",
                    line=line,
                    col=col
                ))
                pos += len(token)
                continue

            # next_ch is NOT in ('"', '\\', '/', 'b', 'f', 'n', 'r', 't', 'u', 'v', '0')
            # This is an invalid JSON escape: R-02!
            word_match = re.match(r"^[a-zA-Z]+", raw_text[pos:])
            if word_match:
                token = word_match.group(0)
                seq = "\\" + token
                pos += len(token)
            else:
                seq = "\\" + next_ch
                pos += 1

            line, col = get_line_col(raw_text, esc_pos)
            errors.append(ValidationError(
                rule_id="R-02",
                code="ERR_LATEX_SYNTAX",
                message=f"Invalid escape sequence '{seq}' at line {line}, col {col}. Must be double-escaped as '\\{seq}'",
                line=line,
                col=col
            ))
            continue

        pos += 1

    if in_string:
        line, col = get_line_col(raw_text, string_start_pos)
        errors.append(ValidationError(
            rule_id="R-01",
            code="ERR_INVALID_JSON",
            message=f"File is not valid JSON at line {line}, col {col}: Unterminated string literal",
            line=line,
            col=col
        ))

    return errors
```

---

## 8. Verification Strategy & Invalidation Conditions

The implementer can independently verify that all blind spots are eliminated using the following tests:

1. **Verify Adversarial LaTeX Test Suite**:
   ```powershell
   python -m pytest tests/test_adversarial_validator.py -k "TestAdversarialLatex" -v
   ```
   *Expected outcome*: 12/12 tests PASS (including `\norm`, `\ne`, `\boxed`, `\therefore`, `\thickspace`, `\textcolor`, `\bigcap`, `\bigcup`, `\bigoplus`, `\bigotimes`, `\rank`).

2. **Verify Challenger 2 False Negative Tests**:
   ```powershell
   python -m pytest tests/validator/test_empirical_stress.py -k "test_fn_latex" -v
   ```
   *Expected outcome*: Both `test_fn_latex_newline_command_escape` and `test_fn_latex_not_command_escape` PASS.

3. **Verify Baseline Test Suite Stability**:
   ```powershell
   python -m pytest tests/validator/test_validator.py -v
   ```
   *Expected outcome*: 67/67 tests PASS with zero regressions.

4. **Verify Reviewer 2 Commands**:
   ```bash
   python -c "from src.validator.lexical_scanner import scan_lexical; errs = scan_lexical('{\"stem\": \"x \\not= y and a \\ne b and \\bm{v} and \\tr(A) and \\ref{eq1}\"}'); print([e.rule_id for e in errs])"
   ```
   *Expected outcome*: Returns `['R-03', 'R-03', 'R-03', 'R-03', 'R-03']`.
