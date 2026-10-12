"""Generic Parametric Question Engine for content-to-course v2.

Exports:
- sandbox: AST whitelist validation and isolated execution
- render: KaTeX formatting helpers
- invariants: Question invariant validation
- diversity: Stem text diversity calculation
- instantiate: Deterministic seed sweeping and quota generation
- assemble: Assembling question JSON objects adhering to platform format
"""

from engine.sandbox import (
    validate_code_ast,
    execute_sandbox_instance,
    execute_sandbox_batch,
    run_code_in_env,
    build_sandbox_globals,
    SecurityViolationError,
    SandboxExecutionError,
    SandboxTimeoutError,
)
from engine.render import bmatrix, table_array, fmt, latex_frac
from engine.invariants import (
    check_instance_invariants,
    validate_katex_syntax,
    InvariantViolationError,
)
from engine.diversity import mask_stem_numbers, evaluate_competency_diversity
from engine.assemble import (
    assemble_question,
    format_template_string,
    sanitize_katex_syntax,
    check_course_giveaway_distribution,
)
from engine.instantiate import (
    instantiate_template,
    instantiate_competency,
    allocate_template_quotas,
    get_competency_quota,
)

__all__ = [
    "validate_code_ast",
    "execute_sandbox_instance",
    "execute_sandbox_batch",
    "run_code_in_env",
    "build_sandbox_globals",
    "SecurityViolationError",
    "SandboxExecutionError",
    "SandboxTimeoutError",
    "bmatrix",
    "table_array",
    "fmt",
    "latex_frac",
    "check_instance_invariants",
    "validate_katex_syntax",
    "InvariantViolationError",
    "mask_stem_numbers",
    "evaluate_competency_diversity",
    "assemble_question",
    "format_template_string",
    "sanitize_katex_syntax",
    "check_course_giveaway_distribution",
    "instantiate_template",
    "instantiate_competency",
    "allocate_template_quotas",
    "get_competency_quota",
]
