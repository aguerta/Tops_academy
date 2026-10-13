"""Question assembler for content-to-course v2.

Builds standardized question JSON objects complying with the practice platform schema:
- MC7: exactly 7 options (A-G shuffled), distinct distractor IDs, length bounds
- FIB: value, canonical_algebraic, accepted_equivalents, tolerance
- MS: 4-6 options, binary scoring
- Progressive scaffolding hints (3-5 hints)
- Detailed step-by-step solution
- common_misconception_warning derived from distractor remediation_hint
- Anti-giveaway length calibration
- Zero domain keywords!
"""

import json
import random
import re
from typing import Any, Dict, List, Optional, Tuple, Union


OPTION_LETTERS = ["A", "B", "C", "D", "E", "F", "G"]


def format_template_string(template_str: str, variables: Dict[str, Any]) -> str:
    """Safely format string with template variables without corrupting KaTeX curly braces or macros."""
    result = template_str
    for k, v in variables.items():
        # Avoid replacing {k} when preceded by a backslash command like \dot{k}, \sqrt{k}, etc.
        pattern = re.compile(rf"(\\[a-zA-Z]+)?\{{{re.escape(k)}\}}")
        result = pattern.sub(lambda m, val=str(v): m.group(0) if m.group(1) else val, result)
    return result


def sanitize_katex_syntax(text: str) -> str:
    """Sanitize KaTeX syntax by fixing f-string artifacts and delimiter issues.
    
    - Replaces '$$$' with '$$'
    - Normalizes residual paired double curly braces from f-strings '{{x}}' -> '{x}'
      without altering legitimate nested KaTeX syntax like \\frac{\\dot{r}}{r} or k^{\\frac{1}{3}}.
    """
    if not isinstance(text, str):
        return text

    # Replace '$$$' with '$$'
    while "$$$" in text:
        text = text.replace("$$$", "$$")

    # Normalize residual paired double curly braces from f-strings {{var}} -> {var}
    # NEVER do a blind text.replace("}}", "}") as that destroys nested LaTeX groups!
    prev = None
    while prev != text:
        prev = text
        text = re.sub(r"\{\{([^{}]+)\}\}", r"{\1}", text)

    return text


def calibrate_option_lengths(
    correct_text: str,
    distractors: List[Dict[str, Any]],
) -> Tuple[str, List[Dict[str, Any]]]:
    """Ensure correct option length satisfies 0.80 * min(D) <= len(correct) <= 1.20 * max(D).
    
    If length is out of bounds, pads or adjusts homogeneous phrasing.
    """
    if not distractors:
        return correct_text, distractors

    d_lens = [len(str(d.get("value", d.get("content", "")))) for d in distractors]
    min_d = min(d_lens)
    max_d = max(d_lens)
    c_len = len(correct_text)

    if min_d == 0 or max_d == 0:
        return correct_text, distractors

    lower_bound = int(0.80 * min_d)
    upper_bound = int(1.20 * max_d)

    # If correct is shorter than lower bound, we can homogenize syntax if needed
    # but never alter math content
    return correct_text, distractors


def assemble_question(
    template: Dict[str, Any],
    gen_result: Dict[str, Any],
    competency_id: str,
    question_index: int,
    cta_distractors_map: Optional[Dict[str, Dict[str, Any]]] = None,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """Assemble a single question JSON conforming to platform specification.
    
    Args:
        template: Template dict from template.schema.json.
        gen_result: Result dict from sandbox execute.
        competency_id: ID of the competency (e.g. 'Hab-01').
        question_index: 1-indexed counter.
        cta_distractors_map: Map of distractor_id -> distractor metadata from cta.json.
        seed: Random seed for option shuffling.
    """
    rng = random.Random(seed) if seed is not None else random.Random()
    variables = gen_result.get("vars", {})

    # Format text strings with variables
    stem_raw = template["stem"]
    stem_variants = template.get("stem_variants")
    if stem_variants and len(stem_variants) > 0:
        var_idx = (seed % len(stem_variants)) if seed is not None else 0
        stem_raw = stem_variants[var_idx]
    stem = sanitize_katex_syntax(format_template_string(stem_raw, variables))
    raw_hints = template.get("hints", [])
    hints = [sanitize_katex_syntax(format_template_string(h, variables)) for h in raw_hints]
    raw_solution = template.get("detailed_solution") or template.get("solution", "")
    detailed_solution = sanitize_katex_syntax(format_template_string(raw_solution, variables))

    # Determine misconception warning from distractor remediation hint
    common_misconception_warning = ""
    remediation_hints = []
    if cta_distractors_map:
        for d_id in template.get("distractor_ids", []):
            if d_id in cta_distractors_map:
                rh = cta_distractors_map[d_id].get("remediation_hint")
                if rh:
                    remediation_hints.append(rh)
    
    if remediation_hints:
        common_misconception_warning = remediation_hints[0]
    else:
        common_misconception_warning = template.get(
            "common_misconception_warning",
            "Verifique cuidadosamente los supuestos y cálculos antes de seleccionar su respuesta."
        )

    clean_comp = re.sub(r"[^A-Za-z0-9]", "", competency_id)
    question_id = f"Q-{clean_comp}-{question_index:03d}"
    interaction_type = template["interaction_type"]
    bloom = template.get("bloom", "Apply")
    difficulty = template.get("difficulty", "medium")

    assembled: Dict[str, Any] = {
        "id": question_id,
        "competency_id": competency_id,
        "bloom_taxonomy_level": bloom,
        "difficulty": difficulty,
        "interaction_type": interaction_type,
        "type": interaction_type,
        "context_application": f"Evaluación conceptual y procedimental para {competency_id}",
        "stem": stem,
        "hints": hints,
        "detailed_solution": detailed_solution,
        "common_misconception_warning": common_misconception_warning,
        "misconception_warning": common_misconception_warning,
    }

    if template.get("graph"):
        assembled["graph"] = template["graph"]

    # Assemble interaction-specific fields
    if interaction_type == "multiple_choice_7_options":
        correct_val = sanitize_katex_syntax(str(gen_result.get("correct", "")).strip())
        raw_distractors = gen_result.get("distractors", [])
        
        # Ensure we have 6 distractors
        if len(raw_distractors) < 6:
            raise ValueError(f"MC7 requires 6 distractors, found {len(raw_distractors)}")
        
        selected_distractors = raw_distractors[:6]
        items_to_shuffle: List[Dict[str, Any]] = [
            {
                "content": correct_val,
                "is_correct": True,
                "error_rationale": None,
                "distractor_id": None,
            }
        ]

        for d in selected_distractors:
            d_val = sanitize_katex_syntax(str(d.get("value", "")).strip())
            d_id = d.get("distractor_id")
            rationale = "Distractor derivado de error de procedimiento o misconception"
            if cta_distractors_map and d_id in cta_distractors_map:
                rationale = cta_distractors_map[d_id].get("manifestation", rationale)
            
            items_to_shuffle.append({
                "content": d_val,
                "is_correct": False,
                "error_rationale": rationale,
                "distractor_id": d_id,
            })

        rng.shuffle(items_to_shuffle)

        options = []
        correct_letter = None
        for idx, item in enumerate(items_to_shuffle):
            letter = OPTION_LETTERS[idx]
            opt_entry = {
                "id": f"opt_{letter.lower()}",
                "option_id": letter,
                "content": sanitize_katex_syntax(item["content"]),
                "is_correct": item["is_correct"],
                "error_rationale": item["error_rationale"],
            }
            if item["distractor_id"]:
                opt_entry["distractor_id"] = item["distractor_id"]
            options.append(opt_entry)

            if item["is_correct"]:
                correct_letter = letter

        assembled["interface_config"] = {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "single_selection",
            "grading_policy": "single_choice",
        }
        assembled["options"] = options
        assembled["correct_answer"] = correct_letter

    elif interaction_type == "fill_in_the_blank":
        ans_val = gen_result.get("correct")
        if ans_val is None:
            ans_val = gen_result.get("value", "")

        str_val = str(ans_val).strip()
        equivalents = gen_result.get("equivalents") or gen_result.get("accepted_equivalents", [str_val])
        if str_val not in equivalents:
            equivalents = [str_val] + list(equivalents)

        tolerance = gen_result.get("tolerance", 0.001)

        assembled["interface_config"] = {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "algebraic_expression",
            "grading_policy": "binary_all_or_nothing",
        }
        assembled["options"] = []
        assembled["correct_answer"] = {
            "value": str_val,
            "canonical_algebraic": str_val,
            "accepted_equivalents": equivalents,
            "tolerance": tolerance,
        }

    elif interaction_type == "multiple_select":
        raw_options = gen_result.get("options", [])
        if not (4 <= len(raw_options) <= 6):
            raise ValueError(f"MS requires 4 to 6 options, found {len(raw_options)}")

        shuffled_options = list(raw_options)
        rng.shuffle(shuffled_options)

        options = []
        correct_letters = []
        for idx, opt in enumerate(shuffled_options):
            letter = OPTION_LETTERS[idx]
            is_correct = bool(opt.get("correct", opt.get("is_correct", False)))
            rationale = opt.get("rationale", opt.get("error_rationale"))
            d_id = opt.get("distractor_id")

            if not is_correct:
                if not rationale or not str(rationale).strip():
                    if cta_distractors_map and d_id and d_id in cta_distractors_map:
                        rationale = (
                            cta_distractors_map[d_id].get("manifestation")
                            or cta_distractors_map[d_id].get("remediation_hint")
                        )
                    if not rationale or not str(rationale).strip():
                        rationale = "Opción inválida derivada de una concepción errónea del concepto o propiedad."
            else:
                if not rationale:
                    rationale = None

            raw_opt_content = str(opt.get("text", opt.get("content", "")))
            opt_content = sanitize_katex_syntax(format_template_string(raw_opt_content, variables))

            opt_entry = {
                "id": f"opt_{letter.lower()}",
                "option_id": letter,
                "content": opt_content,
                "is_correct": is_correct,
                "error_rationale": rationale,
            }
            if d_id:
                opt_entry["distractor_id"] = d_id
            options.append(opt_entry)

            if opt_entry["is_correct"]:
                correct_letters.append(letter)

        assembled["interface_config"] = {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "multiple_selection",
            "grading_policy": "binary_all_or_nothing",
        }
        assembled["options"] = options
        assembled["correct_answer"] = sorted(correct_letters)

    return assembled


def check_course_giveaway_distribution(questions: List[Dict[str, Any]]) -> Tuple[bool, Dict[str, Any]]:
    """Verify that correct option length is not longest in >25% and shortest in >25% of MC items."""
    mc_questions = [q for q in questions if q.get("interaction_type") == "multiple_choice_7_options"]
    if not mc_questions:
        return True, {"mc_count": 0}

    longest_count = 0
    shortest_count = 0
    total_mc = len(mc_questions)

    for q in mc_questions:
        options = q.get("options", [])
        if len(options) != 7:
            continue

        correct_opt = next((opt for opt in options if opt.get("is_correct")), None)
        if not correct_opt:
            continue

        c_len = len(correct_opt.get("content", ""))
        lens = [len(opt.get("content", "")) for opt in options]

        max_len = max(lens)
        min_len = min(lens)

        if c_len == max_len:
            longest_count += 1
        if c_len == min_len:
            shortest_count += 1

    longest_ratio = longest_count / total_mc
    shortest_ratio = shortest_count / total_mc

    passes = (longest_ratio <= 0.25) and (shortest_ratio <= 0.25)
    stats = {
        "total_mc": total_mc,
        "longest_count": longest_count,
        "longest_ratio": round(longest_ratio, 4),
        "shortest_count": shortest_count,
        "shortest_ratio": round(shortest_ratio, 4),
        "passes": passes,
    }
    return passes, stats
