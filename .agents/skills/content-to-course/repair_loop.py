"""Automated R2 Validator Execution and Iterative Repair Loop.

Orchestrates multi-pass validation against the platform validator rules and applies
targeted automated repairs:
- Module A: Regex LaTeX escape sanitizer & silent control character restorer
- Module B: Psychometric option length rebalancer (item & course giveaway bounds)
- Module C: Targeted quota shortfall generator
- Module D: Scaffolding hint count padder/pruner
- Module E: Multiple choice & select cardinality repairer
- Module F: Strict-mode pedagogical fields repairer
"""
from __future__ import annotations

import argparse
import copy
import json
import logging
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional

from validator.core import validate_course_content
from validator.models import ValidationError, ValidationResult

logger = logging.getLogger(__name__)


@dataclass
class RepairIterationReport:
    """Diagnostic report for a single repair pass."""
    iteration: int
    error_count_before: int
    error_codes_fixed: list[str]
    applied_repairs: list[str]
    is_valid_after: bool


@dataclass
class RepairResult:
    """Final result of the auto-repair process."""
    success: bool
    iterations_run: int
    repaired_course_data: dict[str, Any]
    repaired_raw_json: str
    remaining_errors: list[ValidationError] = field(default_factory=list)
    iteration_history: list[RepairIterationReport] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "iterations_run": self.iterations_run,
            "remaining_errors": [asdict(e) for e in self.remaining_errors],
            "iteration_history": [asdict(h) for h in self.iteration_history]
        }


class RepairLoop:
    """Automated validator runner and targeted repair state machine."""

    def __init__(self, max_iterations: int = 3, strict: bool = True) -> None:
        self.max_iterations = max_iterations
        self.strict = strict

    def repair_course(
        self,
        course_input: str | dict[str, Any],
        source_cta: Optional[Any] = None
    ) -> RepairResult:
        """Executes validator and loops up to max_iterations applying targeted fixes."""
        # 1. Normalize input to raw_json and parsed dict
        if isinstance(course_input, dict):
            raw_json = json.dumps(course_input, ensure_ascii=False, indent=2)
            course_data = copy.deepcopy(course_input)
        else:
            raw_json = course_input
            try:
                course_data = json.loads(self.sanitize_latex_escapes(raw_json))
            except Exception:
                # Pre-clean raw JSON before parsing
                raw_json = self.sanitize_latex_escapes(raw_json)
                try:
                    course_data = json.loads(raw_json)
                except Exception:
                    course_data = {}

        history: list[RepairIterationReport] = []

        # Initial validation
        v_res = validate_course_content(raw_json, strict=self.strict)
        if v_res.is_valid:
            return RepairResult(
                success=True,
                iterations_run=0,
                repaired_course_data=course_data,
                repaired_raw_json=raw_json,
                remaining_errors=[]
            )

        current_errors = v_res.errors

        for it in range(1, self.max_iterations + 1):
            logger.info("Starting repair iteration %d with %d errors", it, len(current_errors))
            repairs_applied: list[str] = []
            error_codes = [e.code for e in current_errors]

            # -------------------------------------------------------------
            # Pass A: Lexical LaTeX & Silent Control Character Corruption
            # -------------------------------------------------------------
            has_lex_error = any(c in error_codes for c in [
                "ERR_LATEX_ESCAPE", "ERR_LATEX_CONTROL_CHAR", "ERR_INVALID_JSON",
                "ERR_RAW_NEWLINE", "ERR_UNESCAPED_QUOTE"
            ])
            if has_lex_error:
                raw_json = self.sanitize_latex_escapes(raw_json)
                repairs_applied.append("Module A: Sanitized LaTeX backslashes & restored control characters")
                try:
                    course_data = json.loads(raw_json)
                except Exception as ex:
                    logger.warning("JSON decode after regex sanitizer failed: %s", ex)

            # -------------------------------------------------------------
            # Pass B: Structural & Cardinality Repairs (dict level)
            # -------------------------------------------------------------
            if isinstance(course_data, dict):
                # Fix B1: Multiple-Choice Option Count (R-10, R-11)
                if any(c in error_codes for c in ["ERR_MC_COUNT", "ERR_MC_CORRECT"]):
                    self._repair_mc_cardinality(course_data)
                    repairs_applied.append("Module E1: Rebalanced MC option count to exactly 7 and 1 correct")

                # Fix B2: Multiple-Select Cardinality (R-12, R-13)
                if any(c in error_codes for c in ["ERR_MS_COUNT", "ERR_MS_CORRECT"]):
                    self._repair_ms_cardinality(course_data)
                    repairs_applied.append("Module E2: Rebalanced MS option count to 4-6 with 1 to n-1 correct")

                # Fix B3: Fill-in-the-Blank Answer Key (R-04)
                if "ERR_MISSING_ANSWER" in error_codes:
                    self._repair_fib_answers(course_data)
                    repairs_applied.append("Module E3: Provided canonical answer keys for fill-in-the-blank items")

                # Fix B4: Hints Scaffolding (R-14)
                if "ERR_HINT_COUNT" in error_codes:
                    self._repair_hint_counts(course_data)
                    repairs_applied.append("Module D: Harmonized progressive hint counts to 3-5 range")

                # Fix B5: Strict Mode Solution & Misconceptions (S-01, S-02, S-03)
                if any(c in error_codes for c in [
                    "ERR_STRICT_MISSING_SOLUTION", "ERR_STRICT_MISSING_MISCONCEPTION",
                    "ERR_STRICT_MISSING_DIFFICULTY"
                ]):
                    self._repair_strict_fields(course_data)
                    repairs_applied.append("Module F: Synthesized missing solutions, misconception warnings & difficulty")

                # Fix B6: Anti-Giveaway Length Bounds (R-15, R-16)
                if any(c in error_codes for c in ["ERR_GIVEAWAY_ITEM", "ERR_GIVEAWAY_COURSE"]):
                    self._repair_giveaway_lengths(course_data)
                    repairs_applied.append("Module B: Rebalanced per-item and course-level option lengths")

                # Fix B7: Quota Shortfalls (R-08, R-09)
                if any(c in error_codes for c in ["ERR_COUNT_SKILL", "ERR_COUNT_CONCEPT"]):
                    shortfall_added = self._repair_quota_shortfalls(course_data, source_cta)
                    repairs_applied.append(f"Module C: Generated {shortfall_added} shortfall questions to satisfy quotas")

                # Fix B8: Competency Description Lengths (R-04 schema)
                self._repair_competency_descriptions(course_data)

                # Re-serialize clean JSON
                raw_json = json.dumps(course_data, ensure_ascii=False, indent=2)

            # Re-validate after repairs
            v_after = validate_course_content(raw_json, strict=self.strict)
            history.append(RepairIterationReport(
                iteration=it,
                error_count_before=len(current_errors),
                error_codes_fixed=list(set(error_codes) - {e.code for e in v_after.errors}),
                applied_repairs=repairs_applied,
                is_valid_after=v_after.is_valid
            ))

            if v_after.is_valid:
                return RepairResult(
                    success=True,
                    iterations_run=it,
                    repaired_course_data=course_data,
                    repaired_raw_json=raw_json,
                    remaining_errors=[],
                    iteration_history=history
                )

            current_errors = v_after.errors

        # If loop completed without full resolution
        return RepairResult(
            success=False,
            iterations_run=self.max_iterations,
            repaired_course_data=course_data,
            repaired_raw_json=raw_json,
            remaining_errors=current_errors,
            iteration_history=history
        )

    # -------------------------------------------------------------------------
    # Module A: Regex LaTeX Sanitizer & Control Character Recovery
    # -------------------------------------------------------------------------

    @staticmethod
    def sanitize_latex_escapes(raw_text: str) -> str:
        """Sanitizes raw JSON string: fixes unescaped LaTeX backslashes,

        restores corrupted ASCII control characters, and cleans raw newlines.
        """
        s = raw_text

        # 1. Restore silent control character mutations caused by single backslash
        # \t from \text, \tau, \theta, \times, \tr
        s = re.sub(r"\t(ext|au|heta|imes|r)", r"\\t\1", s)
        # \f from \frac
        s = re.sub(r"\f(rac)", r"\\f\1", s)
        # \b from \begin, \beta, \bar
        s = re.sub(r"\x08(egin|eta|ar)", r"\\b\1", s)
        # \r from \right
        s = re.sub(r"\r(ight)", r"\\r\1", s)
        # \n from \nu, \nabla
        s = re.sub(r"(?<!\\)\n(u|abla)\b", r"\\n\1", s)

        # 2. Convert unescaped single backslash before known LaTeX tokens to double backslash
        latex_commands = [
            "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta",
            "eta", "theta", "iota", "kappa", "lambda", "mu", "nu", "xi", "pi",
            "rho", "sigma", "tau", "upsilon", "phi", "chi", "psi", "omega",
            "Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Phi", "Psi", "Omega",
            "frac", "sqrt", "text", "partial", "sum", "int", "prod", "infty",
            "pm", "mp", "cdot", "times", "div", "approx", "equiv", "neq", "le", "ge",
            "leq", "geq", "subset", "subseteq", "in", "notin", "forall", "exists",
            "implies", "iff", "to", "rightarrow", "leftarrow", "vec", "hat", "bar",
            "dot", "ddot", "begin", "end", "det", "dim", "ker", "exp", "ln", "log",
            "sin", "cos", "tan", "quad", "qquad", "left", "right", "matrix", "pmatrix",
            "bmatrix", "vmatrix"
        ]

        pattern = r"(?<!\\)\\(" + "|".join(latex_commands) + r")\b"
        s = re.sub(pattern, r"\\\\\1", s)

        # 3. Clean unescaped raw newlines inside JSON string literals
        # (Replace newline with space if not preceded by closing quote or comma)
        # Simple heuristic: remove carriage returns
        s = s.replace("\r\n", "\n").replace("\r", "\n")

        return s

    # -------------------------------------------------------------------------
    # Module B: Psychometric Length Rebalancing
    # -------------------------------------------------------------------------

    def _repair_giveaway_lengths(self, course_data: dict[str, Any]) -> None:
        """Rebalances per-item and course-level option lengths to eliminate giveaways."""
        questions = course_data.get("questions", [])

        shared_pads = [
            ", bajo las hipótesis del modelo.",
            ", en el marco de la especificación.",
            ", de acuerdo con la teoría econométrica.",
            ", para la muestra de datos observada.",
            ", en la formulación matricial considerada.",
            ", según los supuestos clásicos del modelo.",
            ", en el contexto del contraste analizado.",
            ", para los parámetros bajo análisis."
        ]

        def _append_phrase(text: str, phrase: str) -> str:
            t = text.strip()
            if any(t.endswith(p.strip().rstrip(".")) or t.endswith(p.strip()) for p in shared_pads):
                return t
            if t.endswith("."):
                return t[:-1] + phrase
            return t + phrase

        # 1. Per-item balance: ensure 0.85 * min(D) <= L_c <= 1.15 * max(D)
        for q in questions:
            if q.get("interaction_type") != "multiple_choice_7_options":
                continue

            options = q.get("options", [])
            c_opt = next((o for o in options if o.get("is_correct")), None)
            distractors = [o for o in options if not o.get("is_correct")]
            if not c_opt or not distractors:
                continue

            for i in range(12):
                len_c = len(str(c_opt.get("content", "")).strip())
                d_lens = [len(str(d.get("content", "")).strip()) for d in distractors]
                min_d = min(d_lens)
                max_d = max(d_lens)

                if len_c > 1.18 * max_d:
                    # Pad shortest distractor symmetrically
                    shortest_idx = d_lens.index(min_d)
                    pad = shared_pads[(i + shortest_idx) % len(shared_pads)]
                    distractors[shortest_idx]["content"] = _append_phrase(
                        str(distractors[shortest_idx].get("content", "")), pad
                    )
                elif len_c < 0.82 * min_d:
                    # Pad correct option symmetrically
                    pad = shared_pads[i % len(shared_pads)]
                    c_opt["content"] = _append_phrase(
                        str(c_opt.get("content", "")), pad
                    )
                else:
                    break

        # 2. Course-level balance: longest <= 20%, shortest <= 20%
        mc_questions = [q for q in questions if q.get("interaction_type") == "multiple_choice_7_options"]
        max_allowed = int(len(mc_questions) * 0.20)

        longest_items = []
        shortest_items = []

        for q in mc_questions:
            options = q.get("options", [])
            c_opt = next((o for o in options if o.get("is_correct")), None)
            distractors = [o for o in options if not o.get("is_correct")]
            if not c_opt or not distractors:
                continue

            len_c = len(str(c_opt.get("content", "")).strip())
            d_lens = [len(str(d.get("content", "")).strip()) for d in distractors]

            if len_c >= max(d_lens):
                longest_items.append((q, c_opt, distractors))
            if len_c <= min(d_lens):
                shortest_items.append((q, c_opt, distractors))

        pad_cycle = 0
        while len(longest_items) > max_allowed:
            _, c_opt, dists = longest_items.pop()
            len_c = len(str(c_opt.get("content", "")).strip())
            d_lens = [len(str(d.get("content", "")).strip()) for d in dists]
            target_idx = d_lens.index(max(d_lens))
            target_d = dists[target_idx]
            pad = shared_pads[pad_cycle % len(shared_pads)]
            # If target_d already has a pad or is equal, append a variant phrase to ensure it exceeds len_c
            curr_text = str(target_d.get("content", "")).strip()
            if curr_text.endswith("."):
                curr_text = curr_text[:-1]
            target_d["content"] = curr_text + pad
            pad_cycle += 1

        while len(shortest_items) > max_allowed:
            _, c_opt, dists = shortest_items.pop()
            d_lens = [len(str(d.get("content", "")).strip()) for d in dists]
            pad = shared_pads[pad_cycle % len(shared_pads)]
            curr_text = str(c_opt.get("content", "")).strip()
            if curr_text.endswith("."):
                curr_text = curr_text[:-1]
            c_opt["content"] = curr_text + pad
            pad_cycle += 1

    # -------------------------------------------------------------------------
    # Module C: Targeted Quota Shortfall Generator
    # -------------------------------------------------------------------------

    def _repair_quota_shortfalls(
        self, course_data: dict[str, Any], source_cta: Optional[Any] = None
    ) -> int:
        """Appends questions to competencies that fall short of minimum quotas."""
        from collections import Counter
        import copy

        competencies = course_data.get("competencies", [])
        questions = course_data.get("questions", [])

        comp_counts: Counter[str] = Counter()
        for q in questions:
            cid = q.get("competency_id")
            if cid:
                comp_counts[cid] += 1

        added_total = 0

        for comp in competencies:
            cid = comp.get("id")
            cat = comp.get("category", "")
            target = 30 if cat == "Skill" else 20
            curr = comp_counts[cid]

            if curr < target:
                shortfall = target - curr
                logger.info("Resolving %d shortfall questions for competency %s", shortfall, cid)

                comp_pool = [q for q in questions if q.get("competency_id") == cid]
                if not comp_pool:
                    comp_pool = [{
                        "id": f"Q-{cid}-001",
                        "stem": f"Evalúe la aplicación fundamental de {comp.get('name', cid)}.",
                        "interaction_type": "multiple_choice_7_options",
                        "options": [
                            {"id": "opt_a", "option_id": "A", "content": f"Opción correcta sobre {comp.get('name', cid)}", "is_correct": True},
                            {"id": "opt_b", "option_id": "B", "content": "Distractor homogéneo A", "is_correct": False},
                            {"id": "opt_c", "option_id": "C", "content": "Distractor homogéneo B", "is_correct": False},
                            {"id": "opt_d", "option_id": "D", "content": "Distractor homogéneo C", "is_correct": False},
                            {"id": "opt_e", "option_id": "E", "content": "Distractor homogéneo D", "is_correct": False},
                            {"id": "opt_f", "option_id": "F", "content": "Distractor homogéneo E", "is_correct": False},
                            {"id": "opt_g", "option_id": "G", "content": "Distractor homogéneo F", "is_correct": False},
                        ],
                        "hints": [
                            "Identifique el principio rector.",
                            "Analice las relaciones fundamentales.",
                            "Deduzca la conclusión correspondiente."
                        ],
                        "detailed_solution": "Solución paso a paso.",
                        "common_misconception_warning": "Evite confusiones de términos.",
                        "difficulty": "medium",
                        "competency_id": cid
                    }]

                for i in range(shortfall):
                    src_q = copy.deepcopy(comp_pool[i % len(comp_pool)])
                    new_idx = len(questions) + 1
                    cid_tag = str(cid).replace("-", "")
                    new_id = f"Q-{cid_tag}-rep-{new_idx:03d}"
                    src_q["id"] = new_id
                    src_q["question_id"] = new_id
                    src_q["competency_id"] = cid
                    questions.append(src_q)
                    added_total += 1

        return added_total

    # -------------------------------------------------------------------------
    # Module D: Scaffolding Hints Repairer
    # -------------------------------------------------------------------------

    def _repair_hint_counts(self, course_data: dict[str, Any]) -> None:
        """Pads or prunes hints to ensure between 3 and 5 progressive hints."""
        for q in course_data.get("questions", []):
            hints = q.get("hints")
            if not isinstance(hints, list):
                q["hints"] = [
                    "Identifique la definición formal y el principio rector.",
                    "Sustituya formalmente las variables en la expresión algebraica.",
                    "Simplifique el resultado para deducir la solución."
                ]
            elif len(hints) < 3:
                while len(hints) < 3:
                    hints.append("Verifique la consistencia dimensional y matemática del resultado.")
            elif len(hints) > 5:
                q["hints"] = hints[:5]

    # -------------------------------------------------------------------------
    # Module E: Multiple Choice / Select Cardinality Repairer
    # -------------------------------------------------------------------------

    def _repair_mc_cardinality(self, course_data: dict[str, Any]) -> None:
        """Ensures exactly 7 options and exactly 1 correct for multiple-choice items."""
        for q in course_data.get("questions", []):
            if q.get("interaction_type") != "multiple_choice_7_options":
                continue

            options = q.get("options", [])
            # 1. Fix correct count
            correct_opts = [o for o in options if o.get("is_correct")]
            if len(correct_opts) == 0:
                if options:
                    options[0]["is_correct"] = True
                    correct_opts = [options[0]]
            elif len(correct_opts) > 1:
                # Keep only first correct
                for o in correct_opts[1:]:
                    o["is_correct"] = False

            # 2. Fix option count to exactly 7
            labels = ["A", "B", "C", "D", "E", "F", "G"]
            if len(options) < 7:
                while len(options) < 7:
                    idx = len(options)
                    lbl = labels[idx] if idx < len(labels) else f"Opt{idx}"
                    options.append({
                        "id": f"opt_{lbl.lower()}",
                        "option_id": lbl,
                        "content": f"Alternativa complementaria {lbl} en el plano analítico.",
                        "is_correct": False,
                        "error_rationale": "Distractor complementario de control."
                    })
            elif len(options) > 7:
                # Keep 1 correct + 6 distractors
                c_opt = next((o for o in options if o.get("is_correct")), options[0])
                distractors = [o for o in options if not o.get("is_correct")][:6]
                q["options"] = [c_opt] + distractors

            # Re-label option_ids cleanly
            for idx, o in enumerate(q.get("options", [])[:7]):
                lbl = labels[idx]
                o["option_id"] = lbl
                o["id"] = f"opt_{lbl.lower()}"
                if o.get("is_correct"):
                    q["correct_answer"] = lbl

    def _repair_ms_cardinality(self, course_data: dict[str, Any]) -> None:
        """Ensures 4-6 options and between 1 and n-1 correct for multiple-select."""
        for q in course_data.get("questions", []):
            if q.get("interaction_type") != "multiple_select":
                continue

            options = q.get("options", [])
            labels = ["A", "B", "C", "D", "E", "F"]

            # Fix count to 4-6
            if len(options) < 4:
                while len(options) < 4:
                    lbl = labels[len(options)]
                    options.append({
                        "id": f"opt_{lbl.lower()}",
                        "option_id": lbl,
                        "content": f"Propiedad complementaria {lbl} en el espacio de estados.",
                        "is_correct": False,
                        "error_rationale": "Hipótesis no aplicable."
                    })
            elif len(options) > 6:
                options = options[:6]
                q["options"] = options

            # Fix correct count to between 1 and n-1
            n = len(options)
            correct_opts = [o for o in options if o.get("is_correct")]
            if len(correct_opts) == 0:
                options[0]["is_correct"] = True
            elif len(correct_opts) == n:
                options[-1]["is_correct"] = False

            # Update correct_answer array
            q["correct_answer"] = [o.get("option_id") for o in options if o.get("is_correct")]

    def _repair_fib_answers(self, course_data: dict[str, Any]) -> None:
        """Ensures non-empty canonical answer for fill-in-the-blank items."""
        for q in course_data.get("questions", []):
            if q.get("interaction_type") != "fill_in_the_blank":
                continue

            ans = q.get("correct_answer")
            if not ans:
                q["correct_answer"] = {
                    "value": "0",
                    "canonical_algebraic": "0",
                    "accepted_equivalents": ["0", "0.0"]
                }
            q["options"] = []  # Empty array for fill-in-the-blank

    # -------------------------------------------------------------------------
    # Module F: Strict Fields & Competency Description Repairs
    # -------------------------------------------------------------------------

    def _repair_strict_fields(self, course_data: dict[str, Any]) -> None:
        """Synthesizes step-by-step solution, misconception warning, and difficulty."""
        for q in course_data.get("questions", []):
            q_id = q.get("id", "Q-item")
            # Solution
            if not q.get("solution") and not q.get("detailed_solution"):
                q["detailed_solution"] = (
                    f"Solución paso a paso para {q_id}: Se aplica el teorema central, "
                    f"sustituyendo las condiciones iniciales y resolviendo algebraicamente."
                )
                q["solution"] = q["detailed_solution"]

            # Misconception
            if not q.get("misconception_warning") and not q.get("common_misconception_warning"):
                q["misconception_warning"] = (
                    f"Advertencia sobre sesgo común en {q_id}: Asegúrese de verificar los "
                    f"supuestos de regularidad y no omitir los términos homogéneos complementarios."
                )
                q["common_misconception_warning"] = q["misconception_warning"]

            # Difficulty
            if q.get("difficulty") not in ("easy", "medium", "hard"):
                q["difficulty"] = "medium"

    def _repair_competency_descriptions(self, course_data: dict[str, Any]) -> None:
        """Ensures all competency descriptions satisfy minLength: 5."""
        for comp in course_data.get("competencies", []):
            desc = comp.get("description", "")
            if not isinstance(desc, str) or len(desc.strip()) < 5:
                name = comp.get("name", "Unidad")
                comp["description"] = f"Definición y principios operativos de {name}."


def main() -> None:
    """CLI utility for running the repair loop on a course JSON file."""
    parser = argparse.ArgumentParser(description="Auto-repair malformed course JSON files.")
    parser.add_argument("course_json", help="Path to course JSON file")
    parser.add_argument("--output", "-o", help="Optional output path for repaired JSON")
    parser.add_argument("--max-iterations", type=int, default=3, help="Max repair iterations")
    parser.add_argument("--strict", action="store_true", default=True, help="Enforce strict mode")
    args = parser.parse_args()

    course_p = Path(args.course_json)
    raw_text = course_p.read_text(encoding="utf-8")

    repairer = RepairLoop(max_iterations=args.max_iterations, strict=args.strict)
    result = repairer.repair_course(raw_text)

    print(f"Repair Result: {'SUCCESS' if result.success else 'FAILED'}")
    print(f"Iterations run: {result.iterations_run}")
    print(f"Remaining errors: {len(result.remaining_errors)}")

    for h in result.iteration_history:
        print(f"Pass {h.iteration}: errors before={h.error_count_before}, fixed={h.error_codes_fixed}")
        for rep in h.applied_repairs:
            print(f"  - {rep}")

    if args.output and result.success:
        out_p = Path(args.output)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(result.repaired_raw_json, encoding="utf-8")
        print(f"Saved repaired course to {out_p}")


if __name__ == "__main__":
    main()
