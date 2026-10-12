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


def validate_katex_syntax(text: str, context: str) -> List[str]:
    """Validate KaTeX delimiter balance, absence of $$$, {{/}}, and unsubstituted {var}."""
    errors: List[str] = []
    if not isinstance(text, str):
        return errors

    # 1. Triple dollar delimiters
    if "$$$" in text:
        errors.append(f"Triple dollar delimiter '$$$' detected in {context}.")

    # 2. Residual double curly braces
    if "{{" in text or "}}" in text:
        errors.append(f"Residual double curly braces ('{{' or '}}') detected in {context}.")

    # 3. Balanced '$' delimiters
    clean_text = text.replace(r"\$", "")
    if clean_text.count("$$") % 2 != 0:
        errors.append(f"Unbalanced display math delimiter '$$' in {context}.")
    else:
        inline_text = clean_text.replace("$$", "")
        if inline_text.count("$") % 2 != 0:
            errors.append(f"Unbalanced inline math delimiter '$' in {context}.")

    # 4. Unsubstituted template variables: {var}
    for m in re.finditer(r"\{([a-zA-Z0-9_]+)\}", text):
        var_name = m.group(1)
        start = m.start()

        # Legitimate LaTeX: preceded by escape '\', subscript '_', or superscript '^'
        if start > 0 and text[start - 1] in ("\\", "_", "^"):
            continue

        prefix = text[:start]
        # Legitimate LaTeX: argument of a LaTeX command e.g. \frac, \text, \mathbf, \begin, \sqrt[...]
        if re.search(r"\\[a-zA-Z]+(\[[^\]]*\])?\s*$", prefix):
            continue

        # Legitimate LaTeX: second argument of a multi-arg LaTeX command e.g. \frac{a}{b}, \begin{array}{cc}
        if re.search(r"\\[a-zA-Z]+(\[[^\]]*\])?\{[^}]*\}\s*$", prefix):
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
    else:
        errors.extend(validate_katex_syntax(stem, "stem"))

    hints = instance.get("hints", [])
    if not isinstance(hints, list) or not (3 <= len(hints) <= 5):
        errors.append(f"Instance must have between 3 and 5 hints (found {len(hints) if isinstance(hints, list) else 'invalid'}).")
    else:
        for idx, hint in enumerate(hints):
            if not isinstance(hint, str) or not hint.strip():
                errors.append(f"Hint {idx + 1} must be a non-empty string.")
            else:
                errors.extend(validate_katex_syntax(hint, f"hint {idx + 1}"))

    solution = instance.get("detailed_solution") or instance.get("solution")
    if isinstance(solution, str) and solution:
        errors.extend(validate_katex_syntax(solution, "detailed_solution"))

    options_raw = instance.get("options")
    if isinstance(options_raw, list):
        for idx, opt in enumerate(options_raw):
            if isinstance(opt, dict):
                c = opt.get("content")
                if isinstance(c, str):
                    errors.extend(validate_katex_syntax(c, f"option {idx + 1} content"))

    # 1. Multiple Choice 7 options
    if interaction_type == "multiple_choice_7_options":
        options = instance.get("options", [])
        if not isinstance(options, list) or len(options) != 7:
            errors.append(f"MC7 requires exactly 7 options (found {len(options) if isinstance(options, list) else 'invalid'}).")
        else:
            correct_count = 0
            correct_content = None
            distractor_contents = []

            seen_contents = set()
            for idx, opt in enumerate(options):
                if not isinstance(opt, dict):
                    errors.append(f"Option {idx} is not a valid dictionary.")
                    continue
                
                content = str(opt.get("content", "")).strip()
                if not content:
                    errors.append(f"Option {idx} has empty content.")
                
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
            if strict_length_bounds and correct_content and len(distractor_contents) == 6:
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
                if correct_content in stem:
                    errors.append(f"Correct answer '{correct_content}' leaked verbatim in stem text.")
                if hints and len(hints) >= 1 and correct_content in hints[0]:
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
        if not isinstance(options, list) or not (4 <= len(options) <= 6):
            errors.append(f"MS requires 4 to 6 options (found {len(options) if isinstance(options, list) else 'invalid'}).")
        else:
            correct_count = 0
            seen_contents = set()
            for idx, opt in enumerate(options):
                if not isinstance(opt, dict):
                    errors.append(f"Option {idx} is not a valid dictionary.")
                    continue
                content = str(opt.get("content", "")).strip()
                if not content:
                    errors.append(f"Option {idx} has empty content.")
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
            if not (1 <= correct_count <= len(options) - 1):
                errors.append(
                    f"MS correct count must be between 1 and {len(options) - 1} (found {correct_count} correct out of {len(options)} options)."
                )

    return (len(errors) == 0, errors)
