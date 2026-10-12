"""KaTeX rendering helper functions for exercise templates.

These helpers are available inside parametric templates to format matrices,
tables, fractions, and numeric values cleanly in KaTeX notation.
"""

from fractions import Fraction
from typing import Any, List, Optional, Union


def fmt(x: Any, nd: int = 4) -> str:
    """Format a numeric value or symbol for KaTeX output.
    
    Integers or values within epsilon of an integer are returned without decimal points.
    Floats are formatted with up to `nd` decimal places.
    Fractions are rendered as LaTeX \\frac{n}{d}.
    """
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        if x.numerator < 0:
            return f"-\\frac{{{abs(x.numerator)}}}{{{x.denominator}}}"
        return f"\\frac{{{x.numerator}}}{{{x.denominator}}}"
    
    if hasattr(x, "is_integer") and callable(getattr(x, "is_integer")):
        if x.is_integer():
            return str(int(x))
    
    if isinstance(x, (int, bool)):
        return str(int(x))
    
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-9:
            return str(int(round(x)))
        formatted = f"{x:.{nd}f}"
        # Strip redundant trailing zeros after decimal point if they exceed 2 digits
        # but preserve up to nd digits for high precision
        return formatted
    
    return str(x)


def latex_frac(num: Any, den: Any) -> str:
    """Render a fraction in LaTeX \\frac{num}{den} handling signs cleanly."""
    if isinstance(num, (int, float)) and isinstance(den, (int, float)):
        if den == 0:
            raise ZeroDivisionError("Fraction denominator cannot be zero")
        if den == 1:
            return fmt(num)
        if den == -1:
            return fmt(-num)
        if (num < 0 and den < 0):
            return latex_frac(-num, -den)
        if den < 0:
            return f"-\\frac{{{fmt(num)}}}{{{fmt(-den)}}}"
        if num < 0:
            return f"-\\frac{{{fmt(-num)}}}{{{fmt(den)}}}"
    
    return f"\\frac{{{fmt(num)}}}{{{fmt(den)}}}"


def bmatrix(matrix: Any, nd: int = 4) -> str:
    """Format a 2D matrix or list of lists as KaTeX \\begin{bmatrix} ... \\end{bmatrix}.
    
    Works with nested lists, tuples, or 2D numpy arrays.
    """
    # Convert numpy array or iterable to nested list
    if hasattr(matrix, "tolist"):
        rows = matrix.tolist()
    else:
        rows = list(matrix)
    
    if not rows:
        return "\\begin{bmatrix}\\end{bmatrix}"
    
    # Handle 1D vector as row vector
    if not isinstance(rows[0], (list, tuple)):
        row_str = " & ".join(fmt(val, nd) for val in rows)
        return f"\\begin{{bmatrix}} {row_str} \\end{{bmatrix}}"
    
    row_strings = []
    for row in rows:
        row_str = " & ".join(fmt(val, nd) for val in row)
        row_strings.append(row_str)
    
    inner = " \\\\ ".join(row_strings)
    return f"\\begin{{bmatrix}} {inner} \\end{{bmatrix}}"


def table_array(rows: List[List[Any]], headers: Optional[List[str]] = None, align: Optional[str] = None, nd: int = 4) -> str:
    """Format a table as KaTeX \\begin{array}{...} ... \\end{array}.
    
    Useful for regression outputs, summary statistics, or ANOVA tables.
    """
    if not rows and not headers:
        return "\\begin{array}{c}\\end{array}"
    
    num_cols = len(headers) if headers else (len(rows[0]) if rows else 1)
    
    if align is None:
        # Default: left-aligned first column, centered remaining columns
        if num_cols == 1:
            align = "c"
        else:
            align = "l" + "c" * (num_cols - 1)
    
    lines = []
    if headers:
        lines.append(" & ".join(str(h) for h in headers) + " \\\\ \\hline")
    
    for row in rows:
        row_str = " & ".join(fmt(val, nd) for val in row)
        lines.append(row_str)
    
    inner = " \\\\ ".join(lines)
    return f"\\begin{{array}}{{{align}}} {inner} \\end{{array}}"
