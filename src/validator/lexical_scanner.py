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

# Precompiled regex patterns for zero-copy in-place token matching
RE_ALPHA = re.compile(r"[a-zA-Z]+")
RE_ALNUM = re.compile(r"[a-zA-Z0-9]+")

# Comprehensive catalog of LaTeX commands starting with characters
# that form valid JSON control escapes (b, f, n, r, t) or non-standard escapes (v, 0)
LATEX_CONTROL_PREFIXES: dict[str, set[str]] = {
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
    },
    "f": {
        # Fractions & Operators
        "frac", "flat", "forall", "frown",
        # Boxes, Frames & Layout
        "fbox", "framebox", "fcolorbox", "flalign",
        # Fonts & Notes
        "footnotesize", "footnote", "footnotemark", "footnotetext", "frak",
        # Symbols
        "fallingdotseq"
    },
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
    },
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
    },
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


def consolidate_lexical_errors(errors: list[ValidationError]) -> list[ValidationError]:
    """Consolidates identical lexical errors (e.g. repeated \\frac or \\Delta) across lines."""
    if not errors:
        return []
    grouped: dict[tuple[str, str, str], list[ValidationError]] = {}
    for err in errors:
        canonical_msg = re.sub(r"\s+at line \d+(?:, col \d+)?", "", err.message)
        canonical_msg = re.sub(r"\s*:\s*$", "", canonical_msg.strip())
        key = (err.rule_id, err.code, canonical_msg)
        grouped.setdefault(key, []).append(err)

    consolidated: list[ValidationError] = []
    for (rule_id, code, canonical_msg), err_list in grouped.items():
        if len(err_list) == 1:
            consolidated.append(err_list[0])
        else:
            collected_lines: list[int] = []
            for e in err_list:
                if e.lines:
                    collected_lines.extend(e.lines)
                elif e.line is not None:
                    collected_lines.append(e.line)
            consolidated.append(ValidationError(
                rule_id=rule_id,
                code=code,
                message=canonical_msg,
                line=collected_lines[0] if collected_lines else None,
                lines=sorted(set(collected_lines)),
                item_id=err_list[0].item_id,
                details={"consolidated_count": len(err_list)},
            ))
    return consolidated


def scan_lexical(raw_text: str, consolidate: bool = False) -> list[ValidationError]:
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
            # Count the full run of consecutive backslashes starting at esc_pos
            bs_end = pos
            while bs_end < n and raw_text[bs_end] == "\\":
                bs_end += 1
            run_len = bs_end - pos

            if bs_end >= n:
                line, col = get_line_col(raw_text, esc_pos)
                errors.append(ValidationError(
                    rule_id="R-01",
                    code="ERR_INVALID_JSON",
                    message=f"File is not valid JSON at line {line}, col {col}: Trailing backslash in string literal",
                    line=line,
                    col=col
                ))
                break

            # Only inspect command word if run_len could be an over-escape (>= 4) or compact row break (>= 6)
            if (run_len >= 4 and run_len % 4 == 0) or (run_len >= 6 and run_len % 4 == 2):
                word_m = RE_ALPHA.match(raw_text, bs_end)
                if word_m and run_len % 4 == 0:
                    # Rule R-23: Over-escaped LaTeX command (e.g. \\\\cmd, \\\\\\\\cmd).
                    # In JSON, 4k backslashes decode to 2k backslashes in memory, rendering as
                    # KaTeX linebreak(s) + bare command name text without a backslash.
                    cmd_word = word_m.group(0)
                    line, col = get_line_col(raw_text, esc_pos)
                    errors.append(ValidationError(
                        rule_id="R-23",
                        code="ERR_LATEX_OVERESCAPE",
                        message=f"Over-escaped LaTeX command '\\\\\\\\{cmd_word}' at line {line}, col {col} evaluates to '\\\\{cmd_word}' (linebreak + literal text in KaTeX). Must be encoded as '\\\\{cmd_word}' in JSON",
                        line=line,
                        col=col,
                    ))
                    pos = word_m.end()
                    continue

                if word_m and run_len >= 6 and run_len % 4 == 2:
                    # Compact matrix/cases row break immediately followed by a command without space:
                    # e.g. \\\\\\frac (6 raw backslashes) decodes to \\\frac in memory (\\ linebreak + \frac command).
                    # All backslashes are valid JSON escaped pairs (\\). Consume them cleanly.
                    pos = bs_end
                    continue

            pos += 1
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
                word_match = RE_ALPHA.match(raw_text, pos)
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
                word_match = RE_ALNUM.match(raw_text, pos)
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
            word_match = RE_ALPHA.match(raw_text, pos)
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

    if consolidate and len(errors) > 1:
        return consolidate_lexical_errors(errors)
    return errors
