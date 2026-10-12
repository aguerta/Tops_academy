"""Psychometric Anti-Giveaway Checker.

Implements:
- R-15: Per-Item Option Length Symmetry (ERR_GIVEAWAY_ITEM)
  Correct option cannot be > 20% longer than max distractor or > 20% shorter than min distractor.
- R-16: Per-Course Longest/Shortest Option Distribution (ERR_GIVEAWAY_COURSE)
  Correct option cannot be longest in > 25% of MC items, or shortest in > 25% of MC items.
"""
from __future__ import annotations

from typing import Any
from .models import ValidationError


def check_psychometrics(data: dict[str, Any]) -> list[ValidationError]:
    """Evaluates per-item and per-course length distributions to prevent giveaway heuristics."""
    errors: list[ValidationError] = []

    course_id = data.get("course_id", "course")
    questions = data.get("questions")
    if not isinstance(questions, list):
        return errors

    mc_count = 0
    longest_count = 0
    shortest_count = 0

    for q in questions:
        if not isinstance(q, dict):
            continue
        if q.get("interaction_type") != "multiple_choice_7_options":
            continue

        q_id = q.get("id", "UNKNOWN")
        options = q.get("options")
        if not isinstance(options, list):
            continue

        correct_opts = [opt for opt in options if isinstance(opt, dict) and opt.get("is_correct") is True]
        distractors = [opt for opt in options if isinstance(opt, dict) and opt.get("is_correct") is False]

        if len(correct_opts) != 1 or len(distractors) == 0:
            # Covered by R-11/R-10
            continue

        mc_count += 1
        c_opt = correct_opts[0]
        len_c = len(str(c_opt.get("content", "")).strip())
        dist_lengths = [len(str(d.get("content", "")).strip()) for d in distractors]

        max_d = max(dist_lengths)
        min_d = min(dist_lengths)

        # Track course-level longest / shortest
        is_longest = (len_c >= max_d)
        is_shortest = (len_c <= min_d)

        if is_longest:
            longest_count += 1
        if is_shortest:
            shortest_count += 1

        # --- Rule R-15: Per-Item Length Symmetry ---
        # 1. Upper bound: len_c > 1.20 * max_d
        if len_c > 1.20 * max_d:
            pct = ((len_c - max_d) / max_d * 100.0) if max_d > 0 else 100.0
            errors.append(ValidationError(
                rule_id="R-15",
                code="ERR_GIVEAWAY_ITEM",
                message=(
                    f"Question '{q_id}': correct option length ({len_c}) is "
                    f"{pct:.1f}% longer than max distractor ({max_d}); "
                    f"maximum allowed difference is 20.0%"
                ),
                item_id=q_id,
                details={"len_c": len_c, "max_dist": max_d, "pct": pct}
            ))

        # 2. Lower bound: len_c < 0.80 * min_d
        elif len_c < 0.80 * min_d:
            pct = ((min_d - len_c) / min_d * 100.0) if min_d > 0 else 100.0
            errors.append(ValidationError(
                rule_id="R-15",
                code="ERR_GIVEAWAY_ITEM",
                message=(
                    f"Question '{q_id}': correct option length ({len_c}) is "
                    f"{pct:.1f}% shorter than min distractor ({min_d}); "
                    f"maximum allowed difference is 20.0%"
                ),
                item_id=q_id,
                details={"len_c": len_c, "min_dist": min_d, "pct": pct}
            ))

    # --- Rule R-16: Per-Course Longest/Shortest Cap ---
    if mc_count > 0:
        longest_ratio = longest_count / mc_count
        if longest_ratio > 0.25:
            pct = longest_ratio * 100.0
            errors.append(ValidationError(
                rule_id="R-16",
                code="ERR_GIVEAWAY_COURSE",
                message=(
                    f"Course '{course_id}': correct option is longest in "
                    f"{longest_count}/{mc_count} ({pct:.1f}%) multiple-choice items; "
                    f"maximum allowed is 25.0%"
                ),
                details={"longest_count": longest_count, "total_mc": mc_count, "pct": pct}
            ))

        shortest_ratio = shortest_count / mc_count
        if shortest_ratio > 0.25:
            pct = shortest_ratio * 100.0
            errors.append(ValidationError(
                rule_id="R-16",
                code="ERR_GIVEAWAY_COURSE",
                message=(
                    f"Course '{course_id}': correct option is shortest in "
                    f"{shortest_count}/{mc_count} ({pct:.1f}%) multiple-choice items; "
                    f"maximum allowed is 25.0%"
                ),
                details={"shortest_count": shortest_count, "total_mc": mc_count, "pct": pct}
            ))

    return errors
