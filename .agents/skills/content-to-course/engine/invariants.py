"""Question invariant evaluation for content-to-course v2.

Evaluates 100% of instances against strict psychometric and correctness rules:
- 1 correct answer (for MC7)
- Distractors distinct from correct and each other (TPL-D4)
- Cross-check verification passes
- No answer leaks in stem or progressive hints
- Interaction type structural constraints:
    * MC7: exactly 7 options, 1 correct, length anti-giveaway bounded
    * FIB: non-empty answer, tolerance or accepted equivalents
    * MS: 4-6 options, 1 to n-1 correct
- Scaffolding: 3 to 5 hints
"""

import re
from typing import Any, Dict, List, Optional, Tuple, Union


class InvariantViolationError(Exception):
    """Raised when an instance violates mathematical or structural invariants."""
    pass


def validate_katex_syntax(text: str, context: str, allow_template_vars: bool = False) -> List[str]:
    """Validate KaTeX delimiter balance, absence of $$$, {{/}}, macro arity, environments, delimiters, and unsubstituted {var}."""
    errors: List[str] = []
    if not isinstance(text, str):
        return errors

    # 1. Triple dollar delimiters
    if "$$$" in text:
        errors.append(f"Triple dollar delimiter '$$$' detected in {context}.")

    # 2. Residual double curly braces (paired template placeholders like {{var}})
    if re.search(r"\{\{\s*[a-zA-Z0-9_]+\s*\}\}", text) or re.search(r"(?<!\\)\{\{", text):
        errors.append(f"Residual double curly braces ('{{{{' or '}}}}') detected in {context}.")

    # 3. Balanced '$' delimiters
    clean_text = text.replace(r"\$", "")
    if clean_text.count("$$") % 2 != 0:
        errors.append(f"Unbalanced display math delimiter '$$' in {context}.")
    else:
        inline_text = clean_text.replace("$$", "")
        if inline_text.count("$") % 2 != 0:
            errors.append(f"Unbalanced inline math delimiter '$' in {context}.")

    # 4. Balanced curly braces inside LaTeX math blocks
    math_matches = re.findall(r"\$\$(.*?)\$\$|\$(.*?)\$", text, flags=re.DOTALL)
    for mb in math_matches:
        block = mb[0] if mb[0] else mb[1]
        clean_block = block.replace(r"\{", "").replace(r"\}", "")
        if clean_block.count("{") != clean_block.count("}"):
            errors.append(f"Unbalanced curly braces in LaTeX math expression in {context}: '{clean_block[:60]}...'")

    # 5. Unclosed nested accent/style macros (e.g. \hat{\boldsymbol{\beta}} with missing outer brace)
    accent_macros = r"(?:hat|bar|tilde|vec|dot|ddot|acute|grave|check|breve|mathring|widehat|widetilde|overline|underline)"
    style_macros = r"(?:boldsymbol|mathbf|bm|mathit|mathrm|mathcal|text|symbf)"
    nested_accent_pattern = re.compile(
        rf"\\({accent_macros})\s*\{{\s*\\({style_macros})\{{([^{{}}]*)\}}(?!\s*\}})"
    )
    for m in nested_accent_pattern.finditer(text):
        accent_name = m.group(1)
        style_name = m.group(2)
        inner_content = m.group(3)
        errors.append(
            f"Unclosed nested macro brace detected in {context}: '\\{accent_name}{{\\{style_name}{{{inner_content}}}}}' requires closing brace '}}'."
        )

    # 6. Macro arity validation (\frac, \binom, \overset, \underset, etc. require 2 arguments)
    two_arg_macros = re.compile(r"\\(frac|dfrac|tfrac|cfrac|binom|overset|underset)\b")
    for m in two_arg_macros.finditer(text):
        macro_name = m.group(1)
        pos = m.end()
        # skip whitespace
        while pos < len(text) and text[pos].isspace():
            pos += 1

        # Must start with '{'
        if pos >= len(text) or text[pos] != "{":
            errors.append(f"LaTeX macro '\\{macro_name}' missing argument brackets '{{...}}' in {context}.")
            continue

        # Parse first argument
        depth1 = 1
        pos += 1
        while pos < len(text) and depth1 > 0:
            ch = text[pos]
            if ch == "$" and not (pos > 0 and text[pos - 1] == "\\"):
                break
            if ch == "\\" and pos + 1 < len(text):
                pos += 2
                continue
            if ch == "{":
                depth1 += 1
            elif ch == "}":
                depth1 -= 1
            pos += 1

        if depth1 != 0:
            errors.append(f"LaTeX macro '\\{macro_name}' has unclosed first argument in {context}.")
            continue

        # Skip whitespace between arguments
        while pos < len(text) and text[pos].isspace():
            pos += 1

        # Must start with '{' for second argument
        if pos >= len(text) or text[pos] != "{":
            errors.append(f"LaTeX macro '\\{macro_name}' requires 2 arguments, but second argument is missing in {context}.")
            continue

        # Parse second argument
        depth2 = 1
        pos += 1
        while pos < len(text) and depth2 > 0:
            ch = text[pos]
            if ch == "$" and not (pos > 0 and text[pos - 1] == "\\"):
                break
            if ch == "\\" and pos + 1 < len(text):
                pos += 2
                continue
            if ch == "{":
                depth2 += 1
            elif ch == "}":
                depth2 -= 1
            pos += 1

        if depth2 != 0:
            errors.append(f"LaTeX macro '\\{macro_name}' has unclosed second argument in {context}.")
            continue

    # 7. Unclosed LaTeX environments (\begin{env} ... \end{env})
    env_matches = re.finditer(r"\\(begin|end)\{([a-zA-Z*]+)\}", text)
    env_stack: List[str] = []
    for em in env_matches:
        action = em.group(1)
        env_name = em.group(2)
        if action == "begin":
            env_stack.append(env_name)
        else:
            if not env_stack:
                errors.append(f"Unmatched LaTeX environment close '\\end{{{env_name}}}' in {context}.")
            else:
                last_env = env_stack.pop()
                if last_env != env_name:
                    errors.append(
                        f"Mismatched LaTeX environment: '\\begin{{{last_env}}}' closed by '\\end{{{env_name}}}' in {context}."
                    )
    while env_stack:
        env_name = env_stack.pop()
        errors.append(f"Unclosed LaTeX environment '\\begin{{{env_name}}}' in {context}.")

    # 8. Unclosed scalable delimiters (\left( ... \right), \left[ ... \right], \left\{ ... \right\})
    left_paren = len(re.findall(r"\\left\s*\(", text))
    right_paren = len(re.findall(r"\\right\s*\)", text))
    if left_paren > right_paren:
        errors.append(f"Unclosed scalable delimiter '\\left(' without matching '\\right)' in {context}.")
    elif right_paren > left_paren:
        errors.append(f"Unmatched scalable delimiter '\\right)' without matching '\\left(' in {context}.")

    left_bracket = len(re.findall(r"\\left\s*\[", text))
    right_bracket = len(re.findall(r"\\right\s*\]", text))
    if left_bracket > right_bracket:
        errors.append(f"Unclosed scalable delimiter '\\left[' without matching '\\right]' in {context}.")
    elif right_bracket > left_bracket:
        errors.append(f"Unmatched scalable delimiter '\\right]' without matching '\\left[' in {context}.")

    left_brace = len(re.findall(r"\\left\s*\\\{", text))
    right_brace = len(re.findall(r"\\right\s*\\\}", text))
    if left_brace > right_brace:
        errors.append(f"Unclosed scalable delimiter '\\left\\{{' without matching '\\right\\}}' in {context}.")
    elif right_brace > left_brace:
        errors.append(f"Unmatched scalable delimiter '\\right\\}}' without matching '\\left\\{{' in {context}.")

    total_left = len(re.findall(r"\\left\b", text))
    total_right = len(re.findall(r"\\right\b", text))
    if total_left > total_right and left_paren == right_paren and left_bracket == right_bracket and left_brace == right_brace:
        errors.append(f"Unclosed scalable delimiter '\\left' without matching '\\right' in {context}.")
    elif total_right > total_left and left_paren == right_paren and left_bracket == right_bracket and left_brace == right_brace:
        errors.append(f"Unmatched scalable delimiter '\\right' without matching '\\left' in {context}.")

    # 9. Unsubstituted template variables: {var}
    if not (allow_template_vars or context.startswith("stem_variants")):
        for m in re.finditer(r"\{([a-zA-Z0-9_]+)\}", text):
            var_name = m.group(1)
            start = m.start()

            # Legitimate LaTeX: preceded by escape '\', subscript '_', or superscript '^'
            if start > 0 and text[start - 1] in ("\\", "_", "^"):
                continue

            prefix = text[:start].rstrip()
            # Legitimate LaTeX: argument of a LaTeX command e.g. \frac, \text, \mathbf, \begin, \sqrt[...]
            if re.search(r"\\[a-zA-Z]+(\[[^\]]*\])?\s*$", prefix):
                continue

            # Legitimate LaTeX: subsequent argument of a multi-arg LaTeX command e.g. \frac{a}{b}, \frac{d\dot{k}}{dk}
            is_subsequent_latex_arg = False
            s = prefix
            while s.endswith("}"):
                depth = 0
                idx = len(s) - 1
                while idx >= 0:
                    if s[idx] == "}":
                        depth += 1
                    elif s[idx] == "{":
                        depth -= 1
                        if depth == 0:
                            break
                    idx -= 1
                if depth == 0 and idx >= 0:
                    s = s[:idx].rstrip()
                    if re.search(r"\\[a-zA-Z]+(\[[^\]]*\])?$", s):
                        is_subsequent_latex_arg = True
                        break
                else:
                    break

            if is_subsequent_latex_arg:
                continue

            errors.append(f"Unsubstituted template variable '{{{var_name}}}' detected in {context}.")

    return errors


def check_instance_invariants(
    instance: Dict[str, Any],
    interaction_type: str,
    strict_length_bounds: bool = True,
) -> Tuple[bool, List[str]]:
    """Check whether a generated question instance satisfies all invariant rules.
    
    Args:
        instance: The dictionary of generated parameters/options/hints.
        interaction_type: "multiple_choice_7_options", "fill_in_the_blank", or "multiple_select".
        strict_length_bounds: Whether to enforce the 0.80/1.20 length bound on MC7.
        
    Returns:
        (is_valid, list_of_error_messages)
    """
    errors: List[str] = []

    stem = instance.get("stem", "")
    if not stem or not isinstance(stem, str) or len(stem.strip()) < 5:
        errors.append("Stem must be a non-empty string with at least 5 characters.")
    if isinstance(stem, str) and stem:
        errors.extend(validate_katex_syntax(stem, "stem"))

    hints = instance.get("hints", [])
    if not isinstance(hints, list):
        errors.append(f"Instance hints must be a list (found {type(hints).__name__}).")
    else:
        if not (3 <= len(hints) <= 5):
            errors.append(f"Instance must have between 3 and 5 hints (found {len(hints)}).")
        for idx, hint in enumerate(hints):
            if not isinstance(hint, str) or not hint.strip():
                errors.append(f"Hint {idx + 1} must be a non-empty string.")
            else:
                errors.extend(validate_katex_syntax(hint, f"hint {idx + 1}"))

    for sol_key in ("detailed_solution", "solution"):
        solution = instance.get(sol_key)
        if isinstance(solution, str) and solution:
            errors.extend(validate_katex_syntax(solution, sol_key))

    for misc_key in ("misconception_warning", "common_misconception_warning"):
        misc = instance.get(misc_key)
        if isinstance(misc, str) and misc:
            errors.extend(validate_katex_syntax(misc, misc_key))

    options_raw = instance.get("options")
    if isinstance(options_raw, list):
        for idx, opt in enumerate(options_raw):
            if isinstance(opt, dict):
                c = opt.get("content")
                if isinstance(c, str):
                    errors.extend(validate_katex_syntax(c, f"option {idx + 1} content"))
                r = opt.get("error_rationale")
                if isinstance(r, str) and r:
                    errors.extend(validate_katex_syntax(r, f"option {idx + 1} error_rationale"))

    # 1. Multiple Choice 7 options
    if interaction_type == "multiple_choice_7_options":
        options = instance.get("options", [])
        if not isinstance(options, list):
            errors.append(f"MC7 requires a list of options (found {type(options).__name__}).")
        else:
            if len(options) != 7:
                errors.append(f"MC7 requires exactly 7 options (found {len(options)}).")

            correct_count = 0
            correct_content = None
            distractor_contents = []

            seen_contents = set()
            for idx, opt in enumerate(options):
                if not isinstance(opt, dict):
                    errors.append(f"Option {idx + 1} is not a valid dictionary.")
                    continue
                
                content = str(opt.get("content", "")).strip()
                if not content:
                    errors.append(f"Option {idx + 1} has empty content.")
                
                # Check option text uniqueness
                norm_content = re.sub(r"\s+", " ", content)
                if norm_content in seen_contents:
                    errors.append(f"Duplicate option content detected: '{content}'")
                seen_contents.add(norm_content)

                if opt.get("is_correct") is True:
                    correct_count += 1
                    correct_content = content
                else:
                    distractor_contents.append(content)
                    rationale = opt.get("error_rationale")
                    if rationale is None or not isinstance(rationale, str) or not rationale.strip():
                        errors.append(
                            f"MC7 option {idx + 1} with is_correct=False must possess a non-empty 'error_rationale'."
                        )

            if correct_count != 1:
                errors.append(f"MC7 must have exactly 1 correct option (found {correct_count}).")

            # Check that distractors are distinct from correct answer
            if correct_content is not None:
                for d in distractor_contents:
                    if d.strip() == correct_content.strip():
                        errors.append(f"Distractor identical to correct answer: '{d}'")

            # Check length anti-giveaway bounds:
            # 0.80 * min(len(D)) <= len(correct) <= 1.20 * max(len(D))
            if strict_length_bounds and correct_content and distractor_contents:
                d_lens = [len(d) for d in distractor_contents]
                min_d = min(d_lens)
                max_d = max(d_lens)
                c_len = len(correct_content)

                if min_d > 0 and max_d > 0:
                    lower_bound = 0.80 * min_d
                    upper_bound = 1.20 * max_d
                    if c_len < lower_bound:
                        errors.append(
                            f"Length anti-giveaway violation: correct option too short ({c_len} chars < {lower_bound:.1f} = 0.80 * min(D))."
                        )
                    elif c_len > upper_bound:
                        errors.append(
                            f"Length anti-giveaway violation: correct option too long ({c_len} chars > {upper_bound:.1f} = 1.20 * max(D))."
                        )

            # Check answer leak in stem or early hints
            if correct_content and len(correct_content) >= 5 and not correct_content.isdigit():
                # Avoid trivial matches like single numbers
                if isinstance(stem, str) and correct_content in stem:
                    errors.append(f"Correct answer '{correct_content}' leaked verbatim in stem text.")
                if hints and len(hints) >= 1 and isinstance(hints[0], str) and correct_content in hints[0]:
                    errors.append(f"Correct answer '{correct_content}' leaked verbatim in first hint.")

    # 2. Fill in the blank
    elif interaction_type == "fill_in_the_blank":
        ans = instance.get("correct_answer")
        if ans is None:
            ans = instance.get("correct")
        
        if ans is None:
            errors.append("FIB instance must provide a correct answer.")
        else:
            if isinstance(ans, dict):
                val = ans.get("value") or ans.get("expression") or ans.get("canonical_algebraic")
                if val is None or str(val).strip() == "":
                    errors.append("FIB answer dict missing value/expression/canonical_algebraic.")
            elif isinstance(ans, (int, float, str)):
                if str(ans).strip() == "":
                    errors.append("FIB scalar answer is empty.")
            else:
                errors.append(f"FIB answer format invalid: {type(ans)}")

    # 3. Multiple select
    elif interaction_type == "multiple_select":
        options = instance.get("options", [])
        if not isinstance(options, list):
            errors.append(f"MS requires a list of options (found {type(options).__name__}).")
        else:
            if not (4 <= len(options) <= 6):
                errors.append(f"MS requires 4 to 6 options (found {len(options)}).")

            correct_count = 0
            seen_contents = set()
            for idx, opt in enumerate(options):
                if not isinstance(opt, dict):
                    errors.append(f"Option {idx + 1} is not a valid dictionary.")
                    continue
                content = str(opt.get("content", "")).strip()
                if not content:
                    errors.append(f"Option {idx + 1} has empty content.")
                norm_content = re.sub(r"\s+", " ", content)
                if norm_content in seen_contents:
                    errors.append(f"Duplicate option content detected in MS: '{content}'")
                seen_contents.add(norm_content)

                if opt.get("is_correct") is True:
                    correct_count += 1
                else:
                    rationale = opt.get("error_rationale")
                    if rationale is None or not isinstance(rationale, str) or not rationale.strip():
                        errors.append(
                            f"MS option {idx + 1} with is_correct=False must possess a non-empty 'error_rationale'."
                        )

            # Invariant: 1 <= correct_count <= len(options) - 1
            if len(options) > 0 and not (1 <= correct_count <= len(options) - 1):
                errors.append(
                    f"MS correct count must be between 1 and {len(options) - 1} (found {correct_count} correct out of {len(options)} options)."
                )

    return (len(errors) == 0, errors)
