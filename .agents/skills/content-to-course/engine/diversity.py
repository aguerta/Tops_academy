"""Stem diversity evaluation for content-to-course v2.

Calculates unique(masked_stems) / total >= 0.5 per competency to prevent
repetitive stems that only differ by numerical substitution.
"""

import re
from typing import Any, Dict, List, Tuple


def mask_stem_numbers(stem: str) -> str:
    """Mask numeric quantities, fractions, and matrices to isolate structural syntax."""
    # 1. Normalize whitespace
    text = re.sub(r"\s+", " ", stem.strip())

    # 2. Mask bmatrix and table arrays
    text = re.sub(r"\\begin\{bmatrix\}.*?\\end\{bmatrix\}", "[BMATRIX]", text)
    text = re.sub(r"\\begin\{array\}\{.*?\}.*?\\end\{array\}", "[ARRAY]", text)

    # 3. Mask LaTeX fractions
    text = re.sub(r"\\frac\{[^{}]+\}\{[^{}]+\}", "[FRAC]", text)

    # 4. Mask numeric literals (integers, floats, scientific notation)
    text = re.sub(r"\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b", "[NUM]", text)

    # 5. Mask numbers adjacent to LaTeX math symbols
    text = re.sub(r"(?<=[=\+\-\*\/\^])\s*\d+", " [NUM]", text)

    return text


def evaluate_competency_diversity(
    stems: List[str],
    min_diversity_ratio: float = 0.5,
) -> Dict[str, Any]:
    """Calculate stem structural diversity ratio for a competency.
    
    Returns:
        {
            "total": int,
            "unique_masked": int,
            "diversity_ratio": float,
            "passes": bool,
            "sample_masked": list of strings
        }
    """
    if not stems:
        return {
            "total": 0,
            "unique_masked": 0,
            "diversity_ratio": 0.0,
            "passes": False,
            "sample_masked": [],
        }

    masked_stems = [mask_stem_numbers(s) for s in stems]
    unique_masked = len(set(masked_stems))
    total = len(stems)
    ratio = unique_masked / total if total > 0 else 0.0
    passes = ratio >= min_diversity_ratio

    return {
        "total": total,
        "unique_masked": unique_masked,
        "diversity_ratio": round(ratio, 4),
        "passes": bool(passes),
        "sample_masked": list(set(masked_stems))[:5],
    }
