#!/usr/bin/env python3
"""standardized_audit_engine.py

Centralized, deterministic static audit engine for the course-qa-evaluator skill.
Implements the Google Antigravity SDK Hybrid Multi-Agent pattern:
1. Fast Deterministic Pass (< 300 ms): Exhaustive AST/regex/linter checks on 100% of items.
2. Risk Clustering: Identifies outliers and risk vectors for adaptive semantic sampling.
3. Extensible Registry: Pluggable linters allowing easy domain adaptation and rule learning.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


# ============================================================================
# Core Telemetry Data Structures
# ============================================================================

@dataclass
class LintIssue:
    linter: str
    dimension: str  # D1_architecture, D2_assessment, D3_scaffolding, D4_alignment, D5_katex
    severity: str   # critical, warning, info
    item_id: str
    competency_id: str
    message: str
    snippet: Optional[str] = None


@dataclass
class TelemetryReport:
    course_id: str
    title: str
    total_competencies: int
    total_questions: int
    dimension_summaries: Dict[str, Any] = field(default_factory=dict)
    hard_penalties: List[Dict[str, Any]] = field(default_factory=list)
    risk_score: float = 0.0  # 0.0 (clean) to 100.0 (high anomaly density)
    mastery_path_readiness: Dict[str, Any] = field(default_factory=dict)
    risk_clusters: Dict[str, List[str]] = field(default_factory=dict)
    all_issues: List[Dict[str, Any]] = field(default_factory=list)
    issues_by_item: Dict[str, List[str]] = field(default_factory=dict)


def _get_opt_text(opt: Any) -> str:
    """Extract visible option text across v1/v2 ('text') and v3 ('content' / 'value') schemas."""
    if isinstance(opt, dict):
        return str(opt.get("text") or opt.get("content") or opt.get("value") or "")
    if isinstance(opt, str):
        return opt
    return ""


def _collect_question_text_fields(q: dict, include_rationales: bool = True, include_hints_sol: bool = True) -> List[tuple[str, str]]:
    """Collect all relevant textual fields in a question across v1/v2/v3 schemas."""
    fields: List[tuple[str, str]] = [("stem", str(q.get("stem") or ""))]
    for idx, opt in enumerate(q.get("options", []) or []):
        if isinstance(opt, dict):
            fields.append((f"opt_{idx}_text", _get_opt_text(opt)))
            if include_rationales:
                fields.append((f"opt_{idx}_rationale", str(opt.get("error_rationale") or "")))
        elif isinstance(opt, str):
            fields.append((f"opt_{idx}_str", opt))

    if include_hints_sol:
        for h_idx, hint in enumerate(q.get("hints", []) or []):
            h_text = hint.get("text", "") if isinstance(hint, dict) else str(hint)
            fields.append((f"hint_{h_idx}", h_text))

        sol = q.get("detailed_solution") or q.get("solution")
        if isinstance(sol, dict):
            fields.append(("solution_steps", " ".join(str(s) for s in sol.get("steps", []))))
            fields.append(("solution_misconception", str(sol.get("misconception_warning") or "")))
        elif isinstance(sol, str):
            fields.append(("solution_text", sol))

        top_misc = q.get("misconception_warning") or q.get("common_misconception_warning")
        if isinstance(top_misc, str) and top_misc:
            fields.append(("misconception_warning", top_misc))

    return fields


# ============================================================================
# Universal Linters
# ============================================================================

class BaseLinter:
    name: str = "base_linter"
    dimension: str = "D1_architecture"

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        raise NotImplementedError


class KaTeXSyntaxLinter(BaseLinter):
    name = "katex_syntax_linter"
    dimension = "D5_katex"

    # Known nested LaTeX commands that often fail brace balancing in generative pipelines
    UNCLOSED_BRACE_PATTERNS = [
        re.compile(r"\\hat\{\\boldsymbol\{[a-zA-Z0-9_\\]+(?!\})"),
        re.compile(r"\\hat\{\\mathbf\{[a-zA-Z0-9_\\]+(?!\})"),
        re.compile(r"\\hat\{\\(?:boldsymbol|mathbf)\{[a-zA-Z]+(?=[)=+\s\',])"),
        re.compile(r"\\frac\{\\text\{[a-zA-Z0-9_\s]+\}\{\\text\{[a-zA-Z0-9_\s]+(?!\})"),
        re.compile(r"\\sqrt\{c_\{[a-zA-Z0-9]+\}(?!\})"),
        re.compile(r"\^\{[^}]*\\frac\{[^}]*\}\{[^}]*\}\s*\\text"),
    ]

    UNESCAPED_LATEX_CMD = re.compile(r"(?<!\$)(?<!\\)\\(dot|bar|vec|hat|tilde|ddot)\{[a-zA-Z0-9]+\}(?!\$)")
    TRIPLE_DOLLAR = re.compile(r"\${3,}")
    DOUBLE_BRACE = re.compile(r"\{\{[a-zA-Z0-9_]+\}\}")

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        unclosed_braces = []
        triple_dollars = []
        double_braces = []
        unbalanced_dollars = []
        orphan_latex = []

        questions = course_data.get("questions", [])

        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")

            # Collect all textual fields in the question (v1/v2 'text' + v3 'content')
            texts_to_check = _collect_question_text_fields(q, include_rationales=True, include_hints_sol=True)

            # Execute pattern evaluations
            q_has_katex_issue = False
            for field_name, text in texts_to_check:
                if not text:
                    continue

                # 1. Unclosed nested braces
                for pat in self.UNCLOSED_BRACE_PATTERNS:
                    m = pat.search(text)
                    if m and text.count('{') != text.count('}'):
                        unclosed_braces.append(qid)
                        q_has_katex_issue = True
                        issues.append(LintIssue(
                            linter=self.name,
                            dimension=self.dimension,
                            severity="critical",
                            item_id=qid,
                            competency_id=cid,
                            message=f"Comando KaTeX anidado con llaves sin cerrar en '{field_name}'",
                            snippet=m.group(0)[:50],
                        ))
                        break

                # 2. Triple dollars
                if self.TRIPLE_DOLLAR.search(text):
                    triple_dollars.append(qid)
                    q_has_katex_issue = True
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="warning",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Delimitador KaTeX triple '$$$' en '{field_name}'",
                    ))

                # 3. Double braces from Python f-strings
                m_db = self.DOUBLE_BRACE.search(text)
                if m_db:
                    double_braces.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="warning",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Doble llave espuria de f-string '{m_db.group(0)}' en '{field_name}'",
                        snippet=m_db.group(0),
                    ))

                # 4. Dollar delimiter parity balance
                dollar_count = text.count("$")
                if dollar_count % 2 != 0:
                    unbalanced_dollars.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="critical",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Delimitadores '$' desbalanceados (conteo impar: {dollar_count}) en '{field_name}'",
                    ))

                # 5. Orphan LaTeX commands in plain text (without $)
                m_orph = self.UNESCAPED_LATEX_CMD.search(text)
                if m_orph and "$" not in text:
                    orphan_latex.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="info",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Comando LaTeX expuesto en texto plano '{m_orph.group(0)}' en '{field_name}'",
                        snippet=m_orph.group(0),
                    ))

        return {
            "unclosed_braces_count": len(set(unclosed_braces)),
            "unclosed_braces_items": list(set(unclosed_braces))[:15],
            "triple_dollars_count": len(set(triple_dollars)),
            "double_braces_count": len(set(double_braces)),
            "unbalanced_dollars_count": len(set(unbalanced_dollars)),
            "orphan_latex_plain_text_count": len(set(orphan_latex)),
        }


class DistractorIntegrityLinter(BaseLinter):
    name = "distractor_integrity_linter"
    dimension = "D2_assessment"

    # Canonical telltale cues dictionary (distractor confessions)
    TELLTALE_PATTERNS = [
        re.compile(r"\b(err[oó]neamente|incorrectamente|falsamente)\b", re.IGNORECASE),
        re.compile(r"\b(derivada\s+err[oó]nea|f[oó]rmula\s+err[oó]nea|c[aá]lculo\s+err[oó]neo)\b", re.IGNORECASE),
        re.compile(r"\b(omitiendo\s+(elevar|multiplicar|dividir|sumar|restar))\b", re.IGNORECASE),
        re.compile(r"\b(confundiendo\s+con|al\s+rev[eé]s)\b", re.IGNORECASE),
        re.compile(r"\b(factorizando\s+err[oó]neamente|con\s+signos\s+positivos\s+incorrectos)\b", re.IGNORECASE),
    ]

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        telltale_items = []
        missing_rationales = []
        malformed_options_count = 0
        total_distractors = 0
        distractors_with_rationale = 0

        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")
            options = q.get("options", [])
            qtype = q.get("interaction_type") or q.get("type")

            if not isinstance(options, list):
                continue

            for opt_idx, opt in enumerate(options):
                if not isinstance(opt, dict):
                    continue

                is_correct = opt.get("is_correct", False)
                text = _get_opt_text(opt)
                rationale = opt.get("error_rationale", "")

                if not is_correct:
                    total_distractors += 1
                    if rationale and len(rationale.strip()) > 5:
                        distractors_with_rationale += 1
                    else:
                        missing_rationales.append(f"{qid}_opt{opt_idx}")
                        issues.append(LintIssue(
                            linter=self.name,
                            dimension=self.dimension,
                            severity="warning",
                            item_id=qid,
                            competency_id=cid,
                            message=f"Distractor en índice {opt_idx} carece de error_rationale diagnóstico",
                        ))

                    # Check for telltale distractor confessions in visible option text
                    for pat in self.TELLTALE_PATTERNS:
                        m = pat.search(text)
                        if m:
                            telltale_items.append(qid)
                            issues.append(LintIssue(
                                linter=self.name,
                                dimension=self.dimension,
                                severity="critical",
                                item_id=qid,
                                competency_id=cid,
                                message=f"Metainformación delatora en distractor visible: '{m.group(0)}'",
                                snippet=text[:60],
                            ))
                            break

        return {
            "total_distractors_evaluated": total_distractors,
            "distractors_with_rationale_count": distractors_with_rationale,
            "rationale_coverage_pct": round((distractors_with_rationale / total_distractors * 100) if total_distractors else 100.0, 2),
            "telltale_distractor_items_count": len(set(telltale_items)),
            "telltale_distractor_sample_items": list(set(telltale_items))[:15],
            "missing_rationales_count": len(missing_rationales),
        }


class ScaffoldingHintsLinter(BaseLinter):
    name = "scaffolding_hints_linter"
    dimension = "D3_scaffolding"

    # Regex for un-evaluated Python f-string placeholders
    FSTRING_PLACEHOLDER = re.compile(r"\{[a-zA-Z0-9_]+:[^}]+\}")

    # Common generic boilerplate in misconception warnings
    GENERIC_WARNING_PHRASES = [
        "verifique cuidadosamente los supuestos y c[aá]lculos antes de seleccionar",
        "recuerde aplicar la definici[oó]n formal",
        "preste atenci[oó]n a los signos",
    ]

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        zero_hints_items = []
        insufficient_hints = []
        fstring_placeholders_items = []
        generic_misconception_items = []
        missing_solutions = []

        generic_pats = [re.compile(p, re.IGNORECASE) for p in self.GENERIC_WARNING_PHRASES]

        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")
            hints = q.get("hints", [])
            sol = q.get("detailed_solution") or q.get("solution")

            # 1. Hint depth check
            if len(hints) == 0:
                zero_hints_items.append(qid)
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="critical",
                    item_id=qid,
                    competency_id=cid,
                    message="Reactivo carece por completo de pistas (hints = 0). Aplica penalización dura de -1.0 pt.",
                ))
            elif len(hints) < 3:
                insufficient_hints.append(qid)
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="warning",
                    item_id=qid,
                    competency_id=cid,
                    message=f"Andamiaje insuficiente: reactivo cuenta solo con {len(hints)} pistas (norma: 3-5).",
                ))

            # 1b. Check for prerequisite IDs or keyword stubs as hints (Learned Linter)
            stub_hints_found = []
            for h in hints:
                if isinstance(h, str):
                    h_clean = h.strip()
                    if re.match(r'^(?:C|H|Hab|Fact|Concept|Skill)-\d+$', h_clean, re.I):
                        stub_hints_found.append(f"ID de competencia '{h_clean}'")
                    elif len(h_clean.split()) <= 1 and len(h_clean) < 25 and not any(punct in h_clean for punct in '.!?:$'):
                        stub_hints_found.append(f"Palabra clave stub '{h_clean}'")
                    elif len(h_clean.split()) <= 2 and '_' in h_clean and len(h_clean) < 25:
                        stub_hints_found.append(f"Tag snake_case '{h_clean}'")
            if stub_hints_found:
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="warning",
                    item_id=qid,
                    competency_id=cid,
                    message=f"Pistas deficientes detectadas (no socráticas): {', '.join(stub_hints_found[:2])}",
                ))

            # 2. Detailed solution check
            if not sol:
                missing_solutions.append(qid)
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="critical",
                    item_id=qid,
                    competency_id=cid,
                    message="Reactivo carece de detailed_solution",
                ))
            else:
                sol_str = json.dumps(sol, ensure_ascii=False) if isinstance(sol, dict) else str(sol)

                # Check for un-evaluated f-strings
                m_fstr = self.FSTRING_PLACEHOLDER.search(sol_str)
                if m_fstr:
                    fstring_placeholders_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="warning",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Placeholder f-string sin interpolar '{m_fstr.group(0)}' en solución detallada",
                        snippet=m_fstr.group(0),
                    ))

                # Check for generic boilerplate misconception warnings (nested or top-level)
                misc_warning = (
                    sol.get("misconception_warning", "")
                    if isinstance(sol, dict)
                    else str(q.get("misconception_warning") or q.get("common_misconception_warning") or "")
                )
                if misc_warning:
                    for g_pat in generic_pats:
                        if g_pat.search(misc_warning):
                            generic_misconception_items.append(qid)
                            break

        return {
            "zero_hints_count": len(zero_hints_items),
            "zero_hints_items": zero_hints_items,
            "insufficient_hints_count": len(insufficient_hints),
            "fstring_placeholders_count": len(set(fstring_placeholders_items)),
            "fstring_placeholders_sample_items": list(set(fstring_placeholders_items))[:15],
            "generic_misconception_count": len(set(generic_misconception_items)),
            "missing_solutions_count": len(missing_solutions),
        }


class ArchitectureDAGLinter(BaseLinter):
    name = "architecture_dag_linter"
    dimension = "D1_architecture"

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        competencies = course_data.get("competencies", [])
        questions = course_data.get("questions", [])

        comp_ids = {c.get("id"): c for c in competencies}
        comp_counts: dict[str, int] = {cid: 0 for cid in comp_ids}
        orphan_questions = []

        categories = {"Fact": 0, "Concept": 0, "Skill": 0, "Other": 0}
        comps_missing_prereqs = []

        for c in competencies:
            cid = c.get("id", "unknown")
            cat = c.get("category", "Other")
            if cat in categories:
                categories[cat] += 1
            else:
                categories["Other"] += 1

            prereqs = c.get("prerequisites", [])
            if not prereqs or len(prereqs) == 0:
                comps_missing_prereqs.append(cid)

        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id")
            if not cid or cid not in comp_ids:
                orphan_questions.append(qid)
                issues.append(LintIssue(
                    linter=self.name,
                    dimension="D4_alignment",
                    severity="critical",
                    item_id=qid,
                    competency_id=cid or "none",
                    message=f"Pregunta huérfana: competency_id '{cid}' no existe en el catálogo curricular.",
                ))
            else:
                comp_counts[cid] += 1

        underpopulated_comps = [cid for cid, cnt in comp_counts.items() if cnt < 3]
        for cid in underpopulated_comps:
            issues.append(LintIssue(
                linter=self.name,
                dimension=self.dimension,
                severity="critical",
                item_id=f"comp_{cid}",
                competency_id=cid,
                message=f"Banco < 3 ejercicios prácticos en competencia '{cid}' ({comp_counts[cid]} reactivos). Aplica penalización dura de -2.0 pts.",
            ))

        return {
            "total_competencies": len(competencies),
            "category_distribution": categories,
            "competencies_missing_prerequisites_count": len(comps_missing_prereqs),
            "underpopulated_competencies_count": len(underpopulated_comps),
            "underpopulated_competencies": underpopulated_comps,
            "orphan_questions_count": len(orphan_questions),
            "orphan_questions_items": orphan_questions,
            "min_questions_per_comp": min(comp_counts.values()) if comp_counts else 0,
            "max_questions_per_comp": max(comp_counts.values()) if comp_counts else 0,
        }


class TemplateVariableResidueLinter(BaseLinter):
    name = "template_variable_residue_linter"
    dimension = "D2_assessment"

    VAR_RESIDUE_PATTERN = re.compile(r"\b[a-zA-Z0-9_]+_(?:val|param|var|arg)\b")

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        residue_items = []
        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")
            
            texts_to_check = _collect_question_text_fields(q, include_rationales=True, include_hints_sol=True)

            for field_name, text in texts_to_check:
                if not text:
                    continue
                m = self.VAR_RESIDUE_PATTERN.search(text)
                if m:
                    residue_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="warning",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Variable de código o plantilla sin interpolar '{m.group(0)}' en '{field_name}'",
                        snippet=m.group(0),
                    ))
                    break

        return {
            "template_variable_residue_count": len(set(residue_items)),
            "template_variable_residue_items": list(set(residue_items))[:15],
        }


class BlindStringReplacementLinter(BaseLinter):
    name = "blind_string_replacement_linter"
    dimension = "D2_assessment"

    BLIND_REPLACE_PATTERN = re.compile(r"\\(?:dot|ddot)\{?\d+\}?")

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        leaked_items = []
        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")
            
            texts_to_check = _collect_question_text_fields(q, include_rationales=False, include_hints_sol=False)
            
            for field_name, text in texts_to_check:
                if not text:
                    continue
                m = self.BLIND_REPLACE_PATTERN.search(text)
                if m:
                    leaked_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="critical",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Sustitución ciega de variable bajo operador diferencial '{m.group(0)}' en '{field_name}'",
                        snippet=m.group(0),
                    ))
                    break

        return {
            "blind_string_replacement_count": len(set(leaked_items)),
            "blind_string_replacement_items": list(set(leaked_items))[:15],
        }


class ClonedDistractorValueLinter(BaseLinter):
    name = "cloned_distractor_value_linter"
    dimension = "D2_assessment"

    SYNTHETIC_PREFIX_PAT = re.compile(r"^\s*(?:Opci[oó]n|Alternativa|Variante)\s+(?:alterna\s+)?\d+\s*:?", re.IGNORECASE)

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        cloned_items = []

        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")
            options = q.get("options", [])
            if not isinstance(options, list):
                continue

            correct_texts = []
            for opt in options:
                if isinstance(opt, dict) and opt.get("is_correct", False):
                    correct_texts.append(_get_opt_text(opt).strip())

            for opt_idx, opt in enumerate(options):
                if not isinstance(opt, dict) or opt.get("is_correct", False):
                    continue
                text = _get_opt_text(opt).strip()

                # 1. Check for synthetic clone prefix (e.g. 'Opción alterna 4:')
                if self.SYNTHETIC_PREFIX_PAT.search(text):
                    cloned_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="critical",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Distractor con prefijo sintético de clonación ('{text[:35]}...') en opción {opt_idx}",
                        snippet=text[:50],
                    ))
                    continue

                # 2. Check if distractor text matches any correct answer exactly
                for c_text in correct_texts:
                    if c_text and text == c_text:
                        cloned_items.append(qid)
                        issues.append(LintIssue(
                            linter=self.name,
                            dimension=self.dimension,
                            severity="critical",
                            item_id=qid,
                            competency_id=cid,
                            message=f"Distractor clonado con valor idéntico a la clave correcta en opción {opt_idx}",
                            snippet=text[:50],
                        ))
                        break

        return {
            "cloned_distractor_items_count": len(set(cloned_items)),
            "cloned_distractor_sample_items": list(set(cloned_items))[:15],
        }


class ParentheticalTelltaleLinter(BaseLinter):
    name = "parenthetical_telltale_linter"
    dimension = "D2_assessment"

    PARENTHETICAL_TELLTALE_PAT = re.compile(
        r"\(\s*(?:confusi[oó]n|error|omisi[oó]n|sesgo|falsamente|definici[oó]n\s+err[oó]nea|desplazamiento\s+err[oó]neo|c[aá]lculo\s+err[oó]neo)[^)]*\)",
        re.IGNORECASE,
    )

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        telltale_items = []

        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")
            options = q.get("options", [])
            if not isinstance(options, list):
                continue

            for opt_idx, opt in enumerate(options):
                if not isinstance(opt, dict):
                    continue
                text = _get_opt_text(opt)
                m = self.PARENTHETICAL_TELLTALE_PAT.search(text)
                if m:
                    telltale_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="critical",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Metainformación delatora parentética en opción visible {opt_idx}: '{m.group(0)}'",
                        snippet=m.group(0),
                    ))

        return {
            "parenthetical_telltale_count": len(set(telltale_items)),
            "parenthetical_telltale_items": list(set(telltale_items))[:15],
        }


class ArchetypeEntropyLinter(BaseLinter):
    name = "archetype_entropy_linter"
    dimension = "D2_assessment"
    MIN_ARCHETYPES = 3

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        meta = course_data.get("metadata", {}) if isinstance(course_data.get("metadata"), dict) else {}
        contract_ver = course_data.get("contract_version", meta.get("contract_version"))
        explicit_min_arch = course_data.get("min_archetypes", meta.get("min_archetypes"))

        if explicit_min_arch is not None:
            try:
                req_arch = int(explicit_min_arch)
            except (ValueError, TypeError):
                req_arch = 4 if (contract_ver is not None and int(contract_ver) >= 2) else 3
        elif contract_ver is not None:
            try:
                req_arch = 4 if int(contract_ver) >= 2 else 3
            except (ValueError, TypeError):
                req_arch = 3
        else:
            req_arch = 3

        questions = course_data.get("questions", [])
        q_by_comp: dict[str, list[dict]] = {}
        for q in questions:
            cid = q.get("competency_id", "unassigned")
            q_by_comp.setdefault(cid, []).append(q)

        monotonous_comps = []
        low_archetype_variety_comps = []
        archetype_counts_by_comp: dict[str, int] = {}

        for cid, qlist in q_by_comp.items():
            if len(qlist) < 15:
                continue

            skeletons = []
            for q in qlist:
                stem = q.get("stem", "")
                clean_stem = re.sub(r"\$[^$]+\$", "$MATH$", stem)
                clean_stem = re.sub(r"\d+", "NUM", clean_stem)
                clean_stem = re.sub(r"\s+", " ", clean_stem).strip().lower()
                skeletons.append(clean_stem)

            if not skeletons:
                continue

            counts: dict[str, int] = {}
            for sk in skeletons:
                counts[sk] = counts.get(sk, 0) + 1
            distinct_skeletons = len(counts)
            archetype_counts_by_comp[cid] = distinct_skeletons
            max_freq = max(counts.values())
            ratio = max_freq / len(skeletons)
            tpl_ids = {str(q.get("template_id")).strip() for q in qlist if q.get("template_id")}

            if ratio > 0.85:
                monotonous_comps.append(cid)
                if distinct_skeletons < req_arch:
                    low_archetype_variety_comps.append(cid)
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="warning",
                    item_id=qlist[0].get("id", cid),
                    competency_id=cid,
                    message=(
                        f"Monocultivo de arquetipo en competencia '{cid}': {round(ratio * 100, 1)}% de las preguntas "
                        f"comparten la misma plantilla estructural ({distinct_skeletons} esqueleto(s) distinto(s))"
                    ),
                ))
            elif distinct_skeletons < req_arch:
                monotonous_comps.append(cid)
                low_archetype_variety_comps.append(cid)
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="warning",
                    item_id=qlist[0].get("id", cid),
                    competency_id=cid,
                    message=(
                        f"Variedad insuficiente de arquetipos en competencia '{cid}': solo {distinct_skeletons} "
                        f"esqueleto(s) estructural(es) distinto(s) en {len(qlist)} preguntas "
                        f"(mínimo requerido: {req_arch} bajo contrato Tri-Banda)"
                    ),
                ))
            elif tpl_ids and len(tpl_ids) < req_arch:
                monotonous_comps.append(cid)
                low_archetype_variety_comps.append(cid)
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="warning",
                    item_id=qlist[0].get("id", cid),
                    competency_id=cid,
                    message=(
                        f"Variedad insuficiente de plantillas en competencia '{cid}': solo {len(tpl_ids)} "
                        f"template_id distinto(s) en {len(qlist)} preguntas "
                        f"(mínimo requerido: {req_arch} bajo contrato Tri-Banda)"
                    ),
                ))

        return {
            "min_required_archetypes": req_arch,
            "monotonous_competencies_count": len(monotonous_comps),
            "monotonous_competencies": monotonous_comps,
            "low_archetype_variety_competencies_count": len(low_archetype_variety_comps),
            "low_archetype_variety_competencies": low_archetype_variety_comps,
            "min_distinct_skeletons_observed": min(archetype_counts_by_comp.values()) if archetype_counts_by_comp else 0,
        }


class UninterpolatedMathVariableLinter(BaseLinter):
    name = "uninterpolated_math_variable_linter"
    dimension = "D5_katex"

    UNINTERPOLATED_MATH_PAT = re.compile(r"(?:\$|\b)\{([a-zA-Z_][a-zA-Z0-9_]*)\}(?:\$|\b)")
    CONSECUTIVE_SIGNS_PAT = re.compile(r"(?:\+\s*-\d+|-\s*-\d+)")
    KNOWN_LATEX_SINGLE_LETTER_OR_MACRO = {"n", "i", "j", "k", "t", "x", "y", "z", "R", "C", "N", "alpha", "beta", "gamma", "theta", "sigma", "lambda", "mu"}

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        infracting_items = []

        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")

            texts_to_check = [("stem", q.get("stem", ""))]
            for idx, opt in enumerate(q.get("options", [])):
                if isinstance(opt, dict):
                    texts_to_check.append((f"opt_{idx}", _get_opt_text(opt)))
            sol = q.get("detailed_solution") or q.get("solution")
            if isinstance(sol, dict):
                texts_to_check.append(("solution_steps", " ".join(sol.get("steps", []))))
            elif isinstance(sol, str):
                texts_to_check.append(("solution", sol))

            for field_name, text in texts_to_check:
                if not text:
                    continue

                m_sign = self.CONSECUTIVE_SIGNS_PAT.search(text)
                if m_sign:
                    infracting_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="warning",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Colisión de signos algebraicos sin simplificar ('{m_sign.group(0)}') en '{field_name}'",
                        snippet=m_sign.group(0),
                    ))
                    break

                for m in self.UNINTERPOLATED_MATH_PAT.finditer(text):
                    var_name = m.group(1)
                    if var_name not in self.KNOWN_LATEX_SINGLE_LETTER_OR_MACRO:
                        infracting_items.append(qid)
                        issues.append(LintIssue(
                            linter=self.name,
                            dimension=self.dimension,
                            severity="warning",
                            item_id=qid,
                            competency_id=cid,
                            message=f"Variable de plantilla posiblemente sin interpolar '{{{var_name}}}' en '{field_name}'",
                            snippet=m.group(0),
                        ))
                        break

        return {
            "uninterpolated_math_items_count": len(set(infracting_items)),
            "uninterpolated_math_sample_items": list(set(infracting_items))[:15],
        }


# ============================================================================
# Path-to-Mastery v2.0 Linters (Ruthless Cognitive & Platform-Aware Suite)
# ============================================================================

class ZPDProgressionCalibrationLinter(BaseLinter):
    """Audits Zone of Proximal Development (ZPD) adaptive calibration readiness.

    Directly mirrors platform/src/utils/sessionShuffler.ts (`calibrateByMasteryDifficulty`):
    - If a competency has <= 1 distinct difficulty band, ZPD adaptive band prioritization
      short-circuits (`nonEmptyBands <= 1`), serving identical distributions to 'Not started'
      and 'Mastered' learners.
    - Also verifies cognitive alignment of 'Skill' [Hab] items with higher-order Bloom levels
      (Apply / Analyze / Evaluate / Create) rather than hardcoded 'Understand'.
    """
    name = "zpd_progression_linter"
    dimension = "D1_architecture"

    HIGHER_BLOOM = {"apply", "analyze", "evaluate", "create", "aplicar", "analizar", "evaluar", "crear"}

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        competencies = course_data.get("competencies", [])
        questions = course_data.get("questions", [])

        comp_cat = {c.get("id"): (c.get("category") or c.get("type") or "Other") for c in competencies}
        q_by_comp: dict[str, list[dict]] = {c.get("id"): [] for c in competencies if c.get("id")}
        diff_counts = {"easy": 0, "medium": 0, "hard": 0}
        bloom_counts: dict[str, int] = {}

        skill_total = 0
        skill_higher_bloom = 0

        for q in questions:
            cid = q.get("competency_id", "unassigned")
            q_by_comp.setdefault(cid, []).append(q)
            diff = str(q.get("difficulty") or "medium").lower().strip()
            if diff in diff_counts:
                diff_counts[diff] += 1
            else:
                diff_counts["medium"] += 1

            bloom = str(q.get("bloom_taxonomy_level") or q.get("bloom") or "unspecified").strip()
            bloom_counts[bloom] = bloom_counts.get(bloom, 0) + 1

            is_skill = comp_cat.get(cid) == "Skill" or str(cid).lower().startswith("hab")
            if is_skill:
                skill_total += 1
                if bloom.lower() in self.HIGHER_BLOOM:
                    skill_higher_bloom += 1

        eligible_comps = 0
        zpd_dead_comps = []
        two_band_comps = []
        three_band_comps = []
        missing_hard_comps = []
        missing_easy_comps = []

        for cid, qlist in q_by_comp.items():
            if len(qlist) < 5:
                continue
            eligible_comps += 1
            bands = {str(q.get("difficulty") or "medium").lower().strip() for q in qlist}
            if len(bands) <= 1:
                zpd_dead_comps.append(cid)
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="warning",
                    item_id=qlist[0].get("id", f"comp_{cid}"),
                    competency_id=cid,
                    message=(
                        f"Colapso de calibración ZPD en '{cid}': 100% de sus {len(qlist)} reactivos tienen "
                        f"dificultad '{next(iter(bands))}', desactivando calibrateByMasteryDifficulty en la plataforma."
                    ),
                ))
            elif len(bands) == 2:
                two_band_comps.append(cid)
            else:
                three_band_comps.append(cid)

            if "hard" not in bands:
                missing_hard_comps.append(cid)
            if "easy" not in bands:
                missing_easy_comps.append(cid)

        if skill_total >= 10 and skill_higher_bloom == 0:
            sample_skill_q = next(
                (q for q in questions if comp_cat.get(q.get("competency_id")) == "Skill" or str(q.get("competency_id", "")).lower().startswith("hab")),
                questions[0] if questions else {},
            )
            issues.append(LintIssue(
                linter=self.name,
                dimension="D4_alignment",
                severity="warning",
                item_id=sample_skill_q.get("id", "course_bloom"),
                competency_id=sample_skill_q.get("competency_id", "global"),
                message=(
                    f"Desalineación cognitiva de Bloom: 0/{skill_total} reactivos de Habilidad [Hab] están etiquetados "
                    f"en niveles aplicativos/analíticos (Apply/Analyze); todos colapsan en niveles declarativos."
                ),
            ))

        return {
            "difficulty_distribution": diff_counts,
            "bloom_distribution": bloom_counts,
            "eligible_competencies_evaluated": eligible_comps,
            "zpd_dead_competencies_count": len(zpd_dead_comps),
            "zpd_dead_competencies": zpd_dead_comps[:20],
            "two_band_competencies_count": len(two_band_comps),
            "three_band_competencies_count": len(three_band_comps),
            "missing_hard_tier_competencies_count": len(missing_hard_comps),
            "missing_easy_tier_competencies_count": len(missing_easy_comps),
            "skill_questions_total": skill_total,
            "skill_higher_bloom_count": skill_higher_bloom,
            "skill_higher_bloom_pct": round((skill_higher_bloom / skill_total * 100.0) if skill_total else 100.0, 2),
        }


class RetrievalModalityDiversityLinter(BaseLinter):
    """Audits active recall (generation) vs. passive recognition balance on the Path to Mastery.

    Cognitive science (Roediger & Karpicke; Bjork desirable difficulties) shows that 100% MC7
    recognition permits backward substitution from options and inflates mastery scores compared
    to constructed-response (`fill_in_the_blank` via mathEquivalence.ts) and multi-condition
    discrimination (`multiple_select`).
    """
    name = "retrieval_modality_linter"
    dimension = "D2_assessment"

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        competencies = course_data.get("competencies", [])
        questions = course_data.get("questions", [])
        comp_cat = {c.get("id"): (c.get("category") or c.get("type") or "Other") for c in competencies}

        mc_count = 0
        fib_count = 0
        ms_count = 0
        other_count = 0
        q_by_comp: dict[str, list[dict]] = {}

        for q in questions:
            cid = q.get("competency_id", "unassigned")
            q_by_comp.setdefault(cid, []).append(q)
            qtype = str(q.get("interaction_type") or q.get("type") or "").lower().strip()
            if "multiple_choice" in qtype:
                mc_count += 1
            elif "fill_in_the_blank" in qtype or "open_ended" in qtype:
                fib_count += 1
            elif "multiple_select" in qtype:
                ms_count += 1
            else:
                other_count += 1

        total_q = len(questions)
        recognition_only_skills = []
        for cid, qlist in q_by_comp.items():
            is_skill = comp_cat.get(cid) == "Skill" or str(cid).lower().startswith("hab")
            if is_skill and len(qlist) >= 10:
                has_fib = any(
                    "fill_in_the_blank" in str(q.get("interaction_type") or q.get("type") or "").lower()
                    for q in qlist
                )
                if not has_fib:
                    recognition_only_skills.append(cid)

        if total_q >= 20 and fib_count == 0 and ms_count == 0:
            issues.append(LintIssue(
                linter=self.name,
                dimension=self.dimension,
                severity="warning",
                item_id=questions[0].get("id", "course_modality"),
                competency_id=questions[0].get("competency_id", "global"),
                message=(
                    f"Monocultivo absoluto de reconocimiento pasivo: {mc_count}/{total_q} (100%) son "
                    f"opción múltiple (MC7), con 0% fill_in_the_blank (evocación activa) y 0% multiple_select."
                ),
            ))

        return {
            "mc7_count": mc_count,
            "fib_count": fib_count,
            "ms_count": ms_count,
            "mc7_share_pct": round((mc_count / total_q * 100.0) if total_q else 0.0, 2),
            "fib_share_pct": round((fib_count / total_q * 100.0) if total_q else 0.0, 2),
            "ms_share_pct": round((ms_count / total_q * 100.0) if total_q else 0.0, 2),
            "active_generation_or_discrimination_pct": round(((fib_count + ms_count) / total_q * 100.0) if total_q else 100.0, 2),
            "recognition_only_skill_competencies_count": len(recognition_only_skills),
            "recognition_only_skill_competencies": recognition_only_skills[:20],
        }


class SocraticScaffoldingIntegrityLinter(BaseLinter):
    """Audits the pedagogical integrity of progressive hints protecting the 3-strikes loop.

    Detects three severe Path-to-Mastery failures:
    1. Anti-Socratic Hint Poisoning (`critical`): Compiler fallback wraps a misconception,
       `wrong_belief`, `omitted_step` starting with 'omitir/confundir/ignorar', or a verbatim
       distractor expression inside 'asegurando considerar adecuadamente: ...', actively
       steering struggling students into selecting a distractor and burning a strike!
    2. Mad-Libs Boilerplate Hints (`warning`): Generic templates ('Identifique la estructura
       conceptual de X: analice las relaciones formales...') providing zero problem-specific guidance.
    3. Premature Answer Leak (`critical`): Hint 1 or Hint 2 reveals the exact correct answer text.
    """
    name = "socratic_scaffolding_integrity_linter"
    dimension = "D3_scaffolding"

    BOILERPLATE_HINT_PATS = [
        re.compile(r"Identifique\s+la\s+estructura\s+conceptual\s+de\s+.+?:\s*analice\s+las\s+relaciones\s+formales", re.IGNORECASE),
        re.compile(r"Revise\s+el\s+procedimiento\s+anal[ií]tico\s+paso\s+a\s+paso\s+para\s+.+?,\s*asegurando\s+considerar\s+adecuadamente:", re.IGNORECASE),
        re.compile(r"Antes\s+de\s+concluir,\s+compruebe\s+la\s+consistencia\s+dimensional\s+del\s+resultado\s+de\s+", re.IGNORECASE),
    ]

    POISONED_CONSIDER_PAT = re.compile(
        r"asegurando\s+considerar\s+adecuadamente:\s*(omitir|confundir|ignorar|olvidar|suponer\s+err[oó]neamente|asumir\s+que|reemplazar\s+err[oó]neamente|dividir\s+err[oó]neamente|no\s+elevar)",
        re.IGNORECASE,
    )
    SYMBOLIC_POISON_PAT = re.compile(
        r"(?:asegurando\s+considerar\s+adecuadamente|eval[uú]e\s+posibles\s+desv[ií]os\s+al\s+considerar):\s*\$",
        re.IGNORECASE,
    )
    CONSIDER_EXTRACT_PAT = re.compile(
        r"(?:asegurando\s+considerar\s+adecuadamente|eval[uú]e\s+posibles\s+desv[ií]os\s+al\s+considerar):\s*(.+)$",
        re.IGNORECASE,
    )

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        boilerplate_items = []
        poisoned_items = []
        answer_leak_items = []

        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")
            hints_raw = q.get("hints", []) or []
            hints = [h.get("text", "") if isinstance(h, dict) else str(h) for h in hints_raw]

            options = q.get("options", []) or []
            correct_texts = [
                _get_opt_text(o).strip()
                for o in options
                if isinstance(o, dict) and o.get("is_correct") and len(_get_opt_text(o).strip()) >= 12
            ]
            distractor_cores = []
            for o in options:
                if isinstance(o, dict) and not o.get("is_correct"):
                    dt = _get_opt_text(o).strip().strip("$").strip()
                    if len(dt) >= 12:
                        distractor_cores.append(dt.rstrip("."))

            has_bp = False
            has_poison = False
            poison_snippet = ""

            for h_idx, h_txt in enumerate(hints):
                if not h_txt:
                    continue

                if any(p.search(h_txt) for p in self.BOILERPLATE_HINT_PATS):
                    has_bp = True

                # Check explicit misconception verb or symbolic LaTeX misconception after 'considerar adecuadamente:'
                m_pois = self.POISONED_CONSIDER_PAT.search(h_txt) or self.SYMBOLIC_POISON_PAT.search(h_txt)
                if m_pois:
                    has_poison = True
                    poison_snippet = h_txt[m_pois.start():][:85]

                # Check if a distractor's exact formula/claim is injected after 'considerar adecuadamente:'
                if not has_poison and "asegurando considerar adecuadamente:" in h_txt.lower():
                    m_ext = self.CONSIDER_EXTRACT_PAT.search(h_txt)
                    if m_ext:
                        injected = m_ext.group(1).strip().rstrip(".").strip("$").strip()
                        for dc in distractor_cores:
                            if dc and (dc in injected or (len(injected) >= 14 and injected in dc)):
                                has_poison = True
                                poison_snippet = h_txt[m_ext.start():][:90]
                                break

                # Check premature answer leak in Hint 1 or Hint 2 (leaving Hint 3+ for operational check)
                if h_idx < max(1, len(hints) - 1):
                    for ct in correct_texts:
                        ct_clean = ct.strip("$").strip()
                        if len(ct_clean) >= 15 and ct_clean in h_txt:
                            answer_leak_items.append(qid)
                            issues.append(LintIssue(
                                linter=self.name,
                                dimension=self.dimension,
                                severity="critical",
                                item_id=qid,
                                competency_id=cid,
                                message=f"Fuga prematura de clave correcta en Pista {h_idx + 1} antes del andamiaje final.",
                                snippet=ct_clean[:60],
                            ))
                            break

            if has_poison:
                poisoned_items.append(qid)
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="critical",
                    item_id=qid,
                    competency_id=cid,
                    message="Envenenamiento anti-socrático de pista: instruye 'considerar adecuadamente' un distractor o error conceptual.",
                    snippet=poison_snippet[:80],
                ))
            elif has_bp:
                boilerplate_items.append(qid)
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="warning",
                    item_id=qid,
                    competency_id=cid,
                    message="Andamiaje Mad-Libs sintético de compilador sin guía socrática específica al problema.",
                    snippet=hints[0][:75] if hints else "",
                ))

        total_q = max(len(questions), 1)
        bp_total = len(set(boilerplate_items) | set(poisoned_items))
        return {
            "boilerplate_hints_items_count": bp_total,
            "boilerplate_hints_pct": round(bp_total / total_q * 100.0, 2),
            "boilerplate_sample_items": list(set(boilerplate_items))[:15],
            "poisoned_hints_items_count": len(set(poisoned_items)),
            "poisoned_hints_pct": round(len(set(poisoned_items)) / total_q * 100.0, 2),
            "poisoned_hints_sample_items": list(set(poisoned_items))[:15],
            "hint_answer_leak_items_count": len(set(answer_leak_items)),
            "genuine_socratic_hints_pct": round(max(0.0, (len(questions) - bp_total) / total_q * 100.0), 2),
        }


class DiagnosticRationaleAlignmentLinter(BaseLinter):
    """Audits formative remediation quality in FeedbackToast.tsx.

    Detects:
    1. Synthetic Magic-Multiplier Distractors (`critical`): Numerical distractors fabricated by
       multiplying the correct answer by compile_shard.py's hardcoded constants
       `[1.333, 0.667, 1.667, 0.333, 1.25, 0.75, 1.5, 0.5, 2.1, 0.45, 1.85, 0.15]`, which carry
       disconnected pool-cycled rationales that misdiagnose the student's actual arithmetic error.
    2. Global Rationale Recycling Collapse (`warning`): High repetition of static CTA rationale
       strings across parametric items (< 15% unique rationales across >= 60 distractors).
    """
    name = "diagnostic_rationale_alignment_linter"
    dimension = "D2_assessment"

    MAGIC_MULTIPLIERS = (1.333, 0.667, 1.667, 0.333, 1.25, 0.75, 1.5, 0.5, 2.1, 0.45, 1.85, 0.15)
    NUM_RE = re.compile(r"-?\d+\.\d+|-?\d+")

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        all_rationales: list[str] = []
        magic_mult_items: list[str] = []
        magic_mult_candidates: list[tuple[str, str, list[float], str]] = []

        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")
            options = q.get("options", []) or []
            if not isinstance(options, list):
                continue

            correct_texts = []
            distractor_texts = []
            for o in options:
                if not isinstance(o, dict):
                    continue
                txt = _get_opt_text(o).strip()
                if o.get("is_correct"):
                    correct_texts.append(txt)
                else:
                    distractor_texts.append(txt)
                    rat = str(o.get("error_rationale") or "").strip()
                    if rat:
                        all_rationales.append(rat)

            # Check for compile_shard.py magic-multiplier numerical distractors
            if len(correct_texts) == 1 and len(distractor_texts) >= 4:
                c_nums = self.NUM_RE.findall(correct_texts[0])
                # Only test when correct option ends with or centers on a non-integer/non-trivial number
                if c_nums:
                    try:
                        c_val = float(c_nums[-1])
                        if abs(c_val) > 1e-6 and abs(c_val) not in (1.0, 2.0, 4.0):
                            matched_mults = []
                            for dt in distractor_texts:
                                d_nums = self.NUM_RE.findall(dt)
                                if not d_nums:
                                    continue
                                d_val = float(d_nums[-1])
                                # Ignore conceptual distractors where d_val is identical to c_val (e.g. sign or event domain misconceptions)
                                if abs(d_val - c_val) <= 1e-4:
                                    continue
                                actual_ratio = d_val / c_val if abs(c_val) > 1e-9 else 0.0
                                for m in self.MAGIC_MULTIPLIERS:
                                    # Strictly focus on non-half/non-double distinctive multipliers or >=3 total hits
                                    if abs(actual_ratio - m) <= 0.05 and abs(d_val - round(c_val * m, 3)) <= 0.0015:
                                        matched_mults.append(m)
                                        break
                            distinctive_hits = [m for m in matched_mults if m in (1.333, 0.667, 1.667, 0.333, 2.1, 0.45, 1.85, 0.15)]
                            if len(distinctive_hits) >= 2 or len(matched_mults) >= 4:
                                magic_mult_items.append(qid)
                                magic_mult_candidates.append((qid, cid, distinctive_hits[:3] or matched_mults[:3], correct_texts[0][:50]))
                    except ValueError:
                        pass

        # Only flag as systematic magic-multiplier violation when > 7% of evaluated MC7 items in the competency/course hit
        mc7_total = max(1, sum(1 for q in questions if isinstance(q.get("options"), list) and len(q.get("options", [])) >= 5))
        if len(set(magic_mult_items)) / mc7_total > 0.07:
            for qid, cid, m_hits, snip in magic_mult_candidates:
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="critical",
                    item_id=qid,
                    competency_id=cid,
                    message=(
                        f"Distractores numéricos sintéticos por multiplicador arbitrario ({m_hits}) "
                        f"con error_rationale desconectado del cálculo real."
                    ),
                    snippet=snip,
                ))
        else:
            magic_mult_items = []

        total_rats = len(all_rationales)
        unique_rats = len(set(all_rationales))
        uniqueness_pct = round((unique_rats / total_rats * 100.0) if total_rats else 100.0, 2)

        if total_rats >= 60 and uniqueness_pct < 15.0 and questions:
            issues.append(LintIssue(
                linter=self.name,
                dimension="D3_scaffolding",
                severity="warning",
                item_id=questions[0].get("id", "course_rationales"),
                competency_id=questions[0].get("competency_id", "global"),
                message=(
                    f"Reciclaje masivo de error_rationale: solo {unique_rats}/{total_rats} ({uniqueness_pct}%) "
                    f"justificaciones diagnósticas son únicas en todo el curso."
                ),
            ))

        return {
            "total_rationales": total_rats,
            "unique_rationales": unique_rats,
            "rationale_uniqueness_pct": uniqueness_pct,
            "magic_multiplier_distractor_items_count": len(set(magic_mult_items)),
            "magic_multiplier_sample_items": list(set(magic_mult_items))[:15],
        }


class AntiGamingPsychometricLinter(BaseLinter):
    """Detects superficial test-wiseness exploits and mathematical quantifier corruptions.

    1. Answer Memorization Exploit (`critical`): Competency (>= 15 items) has <= 4 unique correct
       answer strings, allowing students to reach 'Mastered' by visual string recognition without
       reading stems.
    2. Artificial [R-15] Length-Padding Suffixes (`warning`): Options padded with bureaucratic
       filler clauses (', para los parámetros bajo análisis', ', bajo las condiciones del modelo').
    3. Cross-Domain Robotic Stem Prefixes (`warning`): Solow/PDE lead-in phrases ('fundamentos del
       equilibrio', 'condiciones de frontera', 'ecuaciones fundamentales del régimen') injected
       into non-PDE / non-macroeconomic courses.
    4. Vacuous Universal Quantifier Instantiation (`critical`): Substituting a numeric literal
       in place of epsilon inside a limit/probability while retaining 'para todo \\varepsilon > 0',
       making the universal quantifier vacuous and mathematically corrupt.
    """
    name = "anti_gaming_psychometric_linter"
    dimension = "D2_assessment"

    PADDING_SUFFIX_PAT = re.compile(
        r",\s*(?:para\s+los\s+par[aá]metros\s+bajo\s+an[aá]lisis|bajo\s+las\s+condiciones\s+del\s+modelo|seg[uú]n\s+el\s+marco\s+te[oó]rico\s+establecido|en\s+el\s+contexto\s+del\s+sistema\s+analizado|seg[uú]n\s+los\s+supuestos\s+cl[aá]sicos\s+del\s+modelo|bajo\s+las\s+hip[oó]tesis\s+del\s+modelo|para\s+la\s+muestra\s+de\s+datos\s+observada|de\s+acuerdo\s+con\s+la\s+teor[ií]a\s+econom[eé]trica|en\s+la\s+formulaci[oó]n\s+matricial\s+considerada|en\s+el\s+contexto\s+del\s+contraste\s+analizado|en\s+el\s+marco\s+de\s+la\s+especificaci[oó]n)(?:,\s*[^.]{10,60})?\s*\.?\s*$",
        re.IGNORECASE,
    )
    CROSS_DOMAIN_PREFIX_PAT = re.compile(
        r"^(?:Teniendo\s+en\s+consideraci[oó]n\s+los\s+fundamentos\s+del\s+equilibrio|Considerando\s+las\s+ecuaciones\s+fundamentales\s+del\s+r[eé]gimen|Al\s+examinar\s+detenidamente\s+las\s+condiciones\s+de\s+frontera)",
        re.IGNORECASE,
    )
    FORALL_EPS_PAT = re.compile(r"(?:para\s+todo(?:\s+margen)?\s+\$?\\(?:var)?epsilon\s*>\s*0|\\forall\s+\\(?:var)?epsilon\s*>\s*0)", re.IGNORECASE)
    BOUND_CONSTANT_FORALL_PAT = re.compile(r"(?:para\s+todo(?:\s+\w+)?|\\forall)\s+\$?\\(?:var)?epsilon\s*=\s*-?\d+(?:\.\d+)?", re.IGNORECASE)
    HARDCODED_INEQ_PAT = re.compile(r"(?:\\le|\\ge|<|>)\s*0\.\d+")
    EQUILIBRIUM_PDE_COURSE_KEYWORDS = ("equilibrio", "solow", "derivadas parciales", "pde", "edo", "frontera", "control óptimo", "control optimo", "macroeconom")

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        title_desc = (
            str(course_data.get("title") or "") + " " +
            str(course_data.get("course_title") or "") + " " +
            str(course_data.get("description") or "")
        ).lower()
        is_pde_or_macro = any(kw in title_desc for kw in self.EQUILIBRIUM_PDE_COURSE_KEYWORDS)

        q_by_comp: dict[str, list[dict]] = {}
        padded_items: list[str] = []
        cross_domain_items: list[str] = []
        vacuous_quantifier_items: list[str] = []

        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")
            q_by_comp.setdefault(cid, []).append(q)
            stem = str(q.get("stem") or "").strip()

            if not is_pde_or_macro:
                m_cd = self.CROSS_DOMAIN_PREFIX_PAT.search(stem)
                if m_cd:
                    cross_domain_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension="D4_alignment",
                        severity="warning",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Prefijo robótico contaminado de otro dominio (Solow/EDP) en enunciado: '{m_cd.group(0)}'",
                        snippet=m_cd.group(0),
                    ))

            for o_idx, opt in enumerate(q.get("options", []) or []):
                if not isinstance(opt, dict):
                    continue
                txt = _get_opt_text(opt).strip()
                m_pad = self.PADDING_SUFFIX_PAT.search(txt)
                if m_pad:
                    padded_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="warning",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Relleno artificial de longitud en opción {o_idx} para evadir [R-15]: '{m_pad.group(0).strip()}'",
                        snippet=txt[-65:],
                    ))

                # Check vacuous quantifier instantiation (e.g. P(|X_n - c| <= 0.13) = 1 valido para todo \varepsilon > 0 or 'para todo \epsilon = 0.02 > 0')
                has_bound_const = bool(self.BOUND_CONSTANT_FORALL_PAT.search(txt))
                has_vacuous_forall = False
                if self.FORALL_EPS_PAT.search(txt):
                    prefix_part = self.FORALL_EPS_PAT.split(txt)[0]
                    if "\\varepsilon" not in prefix_part and "\\epsilon" not in prefix_part and self.HARDCODED_INEQ_PAT.search(prefix_part):
                        has_vacuous_forall = True
                if has_bound_const or has_vacuous_forall:
                    vacuous_quantifier_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                            severity="critical",
                            item_id=qid,
                            competency_id=cid,
                            message=(
                                f"Corrupción matemática de cuantificador universal en opción {o_idx}: "
                                f"sustituye '\\varepsilon' por constante numérica dejando 'para todo \\varepsilon > 0' vacuo."
                            ),
                            snippet=txt[:85],
                        ))

        memorizable_comps = []
        for cid, qlist in q_by_comp.items():
            if len(qlist) < 15:
                continue
            ans_set = set()
            for q in qlist:
                opts = q.get("options", [])
                if isinstance(opts, list) and opts:
                    corr = tuple(sorted(_get_opt_text(o).strip() for o in opts if isinstance(o, dict) and o.get("is_correct")))
                    ans_set.add(corr)
                else:
                    ans_set.add(json.dumps(q.get("correct_answer"), sort_keys=True))
            if len(ans_set) <= 4:
                memorizable_comps.append({"competency_id": cid, "unique_answers": len(ans_set), "total_items": len(qlist)})
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="critical",
                    item_id=qlist[0].get("id", f"comp_{cid}"),
                    competency_id=cid,
                    message=(
                        f"Vulnerabilidad de memorización mecánica en '{cid}': solo {len(ans_set)} clave(s) correcta(s) "
                        f"única(s) en {len(qlist)} reactivos (el alumno memoriza la cadena sin leer el problema)."
                    ),
                ))

        return {
            "memorizable_competencies_count": len(memorizable_comps),
            "memorizable_competencies": memorizable_comps,
            "length_padded_items_count": len(set(padded_items)),
            "length_padded_sample_items": list(set(padded_items))[:15],
            "cross_domain_prefix_items_count": len(set(cross_domain_items)),
            "cross_domain_prefix_sample_items": list(set(cross_domain_items))[:15],
            "vacuous_quantifier_items_count": len(set(vacuous_quantifier_items)),
            "vacuous_quantifier_sample_items": list(set(vacuous_quantifier_items))[:15],
        }


class DAGMasteryTopologyLinter(BaseLinter):
    """Audits prerequisite DAG topology for linear 'Up Next' navigation and Quiz/Unit Test interleaving.

    Mirrors platform/src/utils/sessionShuffler.ts (`buildInterleavedSessionQuestions`) and App.tsx:
    - Detects directed cycles in prerequisites.
    - Detects inverted prerequisite edges (`idx(prereq) > idx(comp)`), where a learner following
      the unit list practices a dependent competency BEFORE its prerequisite.
    - Detects isolated island competencies (`in_degree == 0` and `out_degree == 0` in multi-unit courses).
    - Computes maximum prerequisite chain depth (`max_dag_depth`) and checks whether `Skill` nodes
      are anchored to `Fact` / `Concept` prerequisites.
    """
    name = "dag_mastery_topology_linter"
    dimension = "D1_architecture"

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        competencies = course_data.get("competencies", [])
        idx_map = {c.get("id"): idx for idx, c in enumerate(competencies) if c.get("id")}
        adj: dict[str, list[str]] = {cid: [] for cid in idx_map}
        in_deg: dict[str, int] = {cid: 0 for cid in idx_map}
        out_deg: dict[str, int] = {cid: 0 for cid in idx_map}

        inverted_edges = []
        dangling_prereqs = []
        skills_without_prereqs = []

        any_prereqs_defined = any(bool(c.get("prerequisites")) for c in competencies)

        for idx, c in enumerate(competencies):
            cid = c.get("id", f"idx_{idx}")
            cat = c.get("category") or c.get("type") or "Other"
            prereqs = c.get("prerequisites", []) or []

            if (cat == "Skill" or str(cid).lower().startswith("hab")) and not prereqs and any_prereqs_defined:
                skills_without_prereqs.append(cid)

            for p in prereqs:
                if p not in idx_map:
                    dangling_prereqs.append({"competency_id": cid, "missing_prerequisite": p})
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="critical",
                        item_id=f"comp_{cid}",
                        competency_id=cid,
                        message=f"Prerrequisito inexistente '{p}' referenciado por '{cid}'.",
                    ))
                    continue

                adj[p].append(cid)
                out_deg[p] += 1
                in_deg[cid] += 1

                if idx_map[p] > idx:
                    inverted_edges.append({"competency_id": cid, "comp_idx": idx, "prereq_id": p, "prereq_idx": idx_map[p]})
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="warning",
                        item_id=f"comp_{cid}",
                        competency_id=cid,
                        message=(
                            f"Inversión topológica en secuencia de estudio: '{cid}' (pos {idx}) requiere "
                            f"'{p}' que aparece después (pos {idx_map[p]})."
                        ),
                    ))

        # Kahn's algorithm for cycle detection & longest path depth
        in_copy = dict(in_deg)
        queue = [cid for cid, d in in_copy.items() if d == 0]
        depth = {cid: 0 for cid in idx_map}
        visited = 0

        while queue:
            u = queue.pop(0)
            visited += 1
            for v in adj.get(u, []):
                depth[v] = max(depth[v], depth[u] + 1)
                in_copy[v] -= 1
                if in_copy[v] == 0:
                    queue.append(v)

        has_cycle = visited < len(idx_map)
        if has_cycle:
            issues.append(LintIssue(
                linter=self.name,
                dimension=self.dimension,
                severity="critical",
                item_id="course_dag",
                competency_id="global",
                message="El grafo curricular contiene ciclos dirigidos (viola invariante DAG).",
            ))

        isolated = []
        if len(competencies) >= 3:
            for cid in idx_map:
                if in_deg[cid] == 0 and out_deg[cid] == 0:
                    isolated.append(cid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="warning",
                        item_id=f"comp_{cid}",
                        competency_id=cid,
                        message=f"Nodo isla desconectado del grafo de dominio: '{cid}' (in_degree=0, out_degree=0).",
                    ))

        # Undirected connected components check (detects MapReduce / multi-chapter disconnected subgraphs)
        undirected: dict[str, set[str]] = {cid: set() for cid in idx_map}
        for u, nbrs in adj.items():
            for v in nbrs:
                undirected[u].add(v)
                undirected[v].add(u)
        seen_cc: set[str] = set()
        cc_sizes: list[int] = []
        for cid in idx_map:
            if cid in seen_cc:
                continue
            comp_nodes = []
            bfs_q = [cid]
            seen_cc.add(cid)
            while bfs_q:
                curr = bfs_q.pop(0)
                comp_nodes.append(curr)
                for nb in undirected[curr]:
                    if nb not in seen_cc:
                        seen_cc.add(nb)
                        bfs_q.append(nb)
            cc_sizes.append(len(comp_nodes))
        multi_node_subgraphs = sum(1 for sz in cc_sizes if sz >= 2)
        if multi_node_subgraphs >= 2:
            issues.append(LintIssue(
                linter=self.name,
                dimension=self.dimension,
                severity="critical",
                item_id="course_dag_subgraphs",
                competency_id="global",
                message=(
                    f"Fractura topológica del grafo: el curso está partido en {multi_node_subgraphs} sub-grafos "
                    f"conexos disjuntos de tamaños {[sz for sz in cc_sizes if sz >= 2]} sin aristas puente."
                ),
            ))

        return {
            "has_cycle": has_cycle,
            "max_dag_depth": max(depth.values()) if depth else 0,
            "connected_components_count": len(cc_sizes),
            "multi_node_subgraphs_count": multi_node_subgraphs,
            "inverted_prerequisite_edges_count": len(inverted_edges),
            "inverted_prerequisite_edges": inverted_edges[:15],
            "dangling_prerequisites_count": len(dangling_prereqs),
            "isolated_competencies_count": len(isolated),
            "isolated_competencies": isolated,
            "skills_without_prerequisites_count": len(skills_without_prereqs),
            "skills_without_prerequisites": skills_without_prereqs,
        }


class KaTeXFrontendErgonomicsLinter(BaseLinter):
    """Audits frontend KaTeX ergonomics on QuestionCard.tsx and FeedbackToast.tsx.

    Detects:
    1. Full-sentence `\\text{...}` abuse (`warning`): Wrapping >= 45-character Spanish prose
       inside `$\\text{...}$` forces KaTeX `white-space: nowrap`, breaking mobile/card wrapping.
    2. Raw Python identifier pseudo-math (`warning`): Rendering snake_case identifiers like
       `$theta_hat$`, `$beta_hat$`, `$y_bar$` inside math delimiters instead of `\\hat{\\theta}`.
    """
    name = "katex_frontend_ergonomics_linter"
    dimension = "D5_katex"

    PROSE_IN_TEXT_PAT = re.compile(r"^\s*\$\\text\{(.{45,})\}\$\s*$")
    RAW_IDENT_MATH_PAT = re.compile(r"\$[a-zA-Z]+_(?:hat|bar|tilde|vec|star|dot|sq|ols|mle|var|est)\b")

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        prose_in_text_items = []
        raw_ident_items = []

        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")

            for field_name, txt in _collect_question_text_fields(q, include_rationales=True, include_hints_sol=True):
                if not txt:
                    continue

                if field_name.startswith("opt_") and self.PROSE_IN_TEXT_PAT.match(txt):
                    prose_in_text_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="warning",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Oración completa en prosa envuelta en '$\\text{{...}}$' (rompe ajuste de línea en UI) en '{field_name}'",
                        snippet=txt[:65],
                    ))

                m_raw = self.RAW_IDENT_MATH_PAT.search(txt)
                if m_raw:
                    raw_ident_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="warning",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Identificador crudo de código en modo matemático '{m_raw.group(0)}' (debe usar macro LaTeX formal) en '{field_name}'",
                        snippet=m_raw.group(0),
                    ))

        return {
            "prose_in_katex_text_items_count": len(set(prose_in_text_items)),
            "prose_in_katex_text_sample_items": list(set(prose_in_text_items))[:15],
            "raw_identifier_math_items_count": len(set(raw_ident_items)),
            "raw_identifier_math_sample_items": list(set(raw_ident_items))[:15],
        }


def compute_mastery_path_readiness(summaries: dict[str, Any], total_comps: int, total_questions: int) -> dict[str, Any]:
    """Compute the deterministic Mastery Path Readiness Index (MPRI: 0.0 to 100.0) across 6 pillars."""
    total_q = max(total_questions, 1)
    total_c = max(total_comps, 1)

    zpd = summaries.get("zpd_progression_linter", {})
    mod = summaries.get("retrieval_modality_linter", {})
    soc = summaries.get("socratic_scaffolding_integrity_linter", {})
    scaf = summaries.get("scaffolding_hints_linter", {})
    diag = summaries.get("diagnostic_rationale_alignment_linter", {})
    dist = summaries.get("distractor_integrity_linter", {})
    cloned = summaries.get("cloned_distractor_value_linter", {})
    ag = summaries.get("anti_gaming_psychometric_linter", {})
    arch_ent = summaries.get("archetype_entropy_linter", {})
    dag_t = summaries.get("dag_mastery_topology_linter", {})
    katex = summaries.get("katex_syntax_linter", {})
    erg = summaries.get("katex_frontend_ergonomics_linter", {})

    # Pillar 1: ZPD Adaptive Progression & Bloom Calibration (20 pts)
    elig_c = zpd.get("eligible_competencies_evaluated", 0)
    if elig_c > 0:
        three_b = zpd.get("three_band_competencies_count", 0)
        two_b = zpd.get("two_band_competencies_count", 0)
        band_score = 12.0 * ((three_b * 1.0 + two_b * 0.6) / elig_c)
    else:
        band_score = 12.0
    bloom_score = 8.0 * (zpd.get("skill_higher_bloom_pct", 100.0) / 100.0)
    p1_zpd = round(max(0.0, min(20.0, band_score + bloom_score)), 2)

    # Pillar 2: Retrieval Modality & Anti-Memorization (20 pts)
    if total_questions >= 20:
        active_pct = mod.get("active_generation_or_discrimination_pct", 0.0)
        modality_score = 10.0 * min(1.0, active_pct / 25.0)
    else:
        modality_score = 10.0
    mem_comps = ag.get("memorizable_competencies_count", 0)
    arch_mono_comps = arch_ent.get("monotonous_competencies_count", 0)
    vac_items = ag.get("vacuous_quantifier_items_count", 0)
    pad_ratio = ag.get("length_padded_items_count", 0) / total_q
    anti_gaming_score = max(
        0.0,
        10.0 - mem_comps * 3.0 - min(4.0, arch_mono_comps * 1.5) - min(5.0, vac_items * 0.5) - pad_ratio * 8.0,
    )
    p2_retrieval = round(max(0.0, min(20.0, modality_score + anti_gaming_score)), 2)

    # Pillar 3: Socratic Scaffolding Lifeline (25 pts) — protects 3-strikes progression
    valid_hints_ratio = max(0.0, (total_questions - scaf.get("zero_hints_count", 0) - scaf.get("insufficient_hints_count", 0)) / total_q)
    bp_ratio = soc.get("boilerplate_hints_pct", 0.0) / 100.0
    poison_ratio = soc.get("poisoned_hints_pct", 0.0) / 100.0
    leak_cnt = soc.get("hint_answer_leak_items_count", 0)
    p3_socratic = round(
        max(0.0, 25.0 * valid_hints_ratio - 12.0 * bp_ratio - 15.0 * poison_ratio - min(5.0, leak_cnt * 1.0)),
        2,
    )

    # Pillar 4: Diagnostic Remediation Alignment (15 pts) — powers FeedbackToast.tsx
    cov_score = 5.0 * (dist.get("rationale_coverage_pct", 100.0) / 100.0)
    if diag.get("total_rationales", 0) >= 60:
        uniq_score = 5.0 * min(1.0, diag.get("rationale_uniqueness_pct", 100.0) / 35.0)
    else:
        uniq_score = 5.0
    magic_ratio = diag.get("magic_multiplier_distractor_items_count", 0) / total_q
    cloned_cnt = cloned.get("cloned_distractor_items_count", 0)
    dist_auth_score = max(0.0, 5.0 - min(5.0, magic_ratio * 25.0) - min(5.0, cloned_cnt * 1.0))
    p4_diagnostic = round(max(0.0, min(15.0, cov_score + uniq_score + dist_auth_score)), 2)

    # Pillar 5: Knowledge Graph & Interleaving Topology (10 pts) — powers Quiz/Test interleaving
    p5_raw = 10.0
    if dag_t.get("has_cycle"):
        p5_raw -= 6.0
    p5_raw -= dag_t.get("dangling_prerequisites_count", 0) * 2.5
    p5_raw -= dag_t.get("inverted_prerequisite_edges_count", 0) * 2.0
    p5_raw -= dag_t.get("isolated_competencies_count", 0) * 1.5
    p5_raw -= min(3.0, dag_t.get("skills_without_prerequisites_count", 0) * 1.0)
    p5_topology = round(max(0.0, min(10.0, p5_raw)), 2)

    # Pillar 6: Cognitive Load & KaTeX Frontend Ergonomics (10 pts)
    katex_crit = katex.get("unclosed_braces_count", 0) + katex.get("unbalanced_dollars_count", 0)
    prose_ratio = erg.get("prose_in_katex_text_items_count", 0) / total_q
    raw_id_ratio = erg.get("raw_identifier_math_items_count", 0) / total_q
    cd_ratio = ag.get("cross_domain_prefix_items_count", 0) / total_q
    p6_ergonomics = round(
        max(0.0, 10.0 - min(5.0, katex_crit * 0.5) - min(4.0, prose_ratio * 12.0) - min(3.0, raw_id_ratio * 15.0) - min(3.0, cd_ratio * 15.0)),
        2,
    )

    mpri_score = round(p1_zpd + p2_retrieval + p3_socratic + p4_diagnostic + p5_topology + p6_ergonomics, 2)
    if mpri_score >= 85.0:
        mpri_tier = "GOLD MASTERY PATH (85-100): Certificado para Dominio Adaptativo"
    elif mpri_score >= 65.0:
        mpri_tier = "PARTIAL MASTERY PATH (65-84): Funcional con Brechas ZPD/Modalidad"
    elif mpri_score >= 40.0:
        mpri_tier = "ILLUSION OF MASTERY (40-64): Riesgo de Memorización / Mecanización Superficial"
    else:
        mpri_tier = "MASTERY-HOSTILE (0-39): Sabotaje Cognitivo / Colapso de Andamiaje Adaptativo"

    return {
        "mpri_score": mpri_score,
        "mpri_max": 100.0,
        "mpri_tier": mpri_tier,
        "pillars": {
            "zpd_adaptive_progression": {"score": p1_zpd, "max": 20.0},
            "retrieval_modality_and_anti_gaming": {"score": p2_retrieval, "max": 20.0},
            "socratic_scaffolding_lifeline": {"score": p3_socratic, "max": 25.0},
            "diagnostic_remediation_alignment": {"score": p4_diagnostic, "max": 15.0},
            "dag_and_interleaving_topology": {"score": p5_topology, "max": 10.0},
            "cognitive_ergonomics_and_framing": {"score": p6_ergonomics, "max": 10.0},
        },
    }


# ============================================================================
# Linter Registry & Engine Orchestrator
# ============================================================================

class AuditLinterRegistry:
    """Registry pattern facilitating dynamic extension and learning of new linters."""

    def __init__(self):
        self.universal_linters: list[BaseLinter] = [
            ArchitectureDAGLinter(),
            DistractorIntegrityLinter(),
            ScaffoldingHintsLinter(),
            KaTeXSyntaxLinter(),
            TemplateVariableResidueLinter(),
            BlindStringReplacementLinter(),
            ClonedDistractorValueLinter(),
            ParentheticalTelltaleLinter(),
            ArchetypeEntropyLinter(),
            UninterpolatedMathVariableLinter(),
            # Path-to-Mastery v2.0 Suite
            ZPDProgressionCalibrationLinter(),
            RetrievalModalityDiversityLinter(),
            SocraticScaffoldingIntegrityLinter(),
            DiagnosticRationaleAlignmentLinter(),
            AntiGamingPsychometricLinter(),
            DAGMasteryTopologyLinter(),
            KaTeXFrontendErgonomicsLinter(),
        ]
        self.domain_linters: dict[str, list[BaseLinter]] = {}

    def register_domain_linter(self, domain_key: str, linter: BaseLinter):
        if domain_key not in self.domain_linters:
            self.domain_linters[domain_key] = []
        self.domain_linters[domain_key].append(linter)

    def execute_all(self, course_data: dict) -> TelemetryReport:
        course_id = course_data.get("course_id", "unknown_course")
        title = course_data.get("title") or course_data.get("course_title", course_id)
        comps = course_data.get("competencies", [])
        questions = course_data.get("questions", [])

        issues: list[LintIssue] = []
        summaries: dict[str, Any] = {}

        # 1. Run universal linters
        for linter in self.universal_linters:
            summary = linter.run(course_data, issues)
            summaries[linter.name] = summary

        # 2. Run domain-specific linters if applicable
        category = course_data.get("category", "").lower()
        for dom_key, l_list in self.domain_linters.items():
            if dom_key in category:
                for dl in l_list:
                    s = dl.run(course_data, issues)
                    summaries[dl.name] = s

        # 3. Compute hard deductions automatically (QM-OSCQR + Path-to-Mastery v2.0)
        hard_penalties = []
        zero_hints = summaries.get("scaffolding_hints_linter", {}).get("zero_hints_count", 0)
        underpopulated = summaries.get("architecture_dag_linter", {}).get("underpopulated_competencies_count", 0)
        orphans = summaries.get("architecture_dag_linter", {}).get("orphan_questions_count", 0)
        poisoned_pct = summaries.get("socratic_scaffolding_integrity_linter", {}).get("poisoned_hints_pct", 0.0)
        poisoned_cnt = summaries.get("socratic_scaffolding_integrity_linter", {}).get("poisoned_hints_items_count", 0)
        vacuous_cnt = summaries.get("anti_gaming_psychometric_linter", {}).get("vacuous_quantifier_items_count", 0)
        mem_comps_cnt = summaries.get("anti_gaming_psychometric_linter", {}).get("memorizable_competencies_count", 0)

        if underpopulated > 0:
            hard_penalties.append({
                "rule": "bank_lt_3_exercises",
                "deduction": 2.0,
                "reason": f"{underpopulated} competencia(s) tienen menos de 3 ejercicios prácticos.",
            })

        if zero_hints > 0:
            hard_penalties.append({
                "rule": "hints_zero",
                "deduction": float(zero_hints * 1.0),
                "reason": f"{zero_hints} reactivo(s) carecen por completo de pistas progresivas (hints = 0).",
            })

        if orphans > 0:
            hard_penalties.append({
                "rule": "orphan_questions",
                "deduction": 2.0,
                "reason": f"{orphans} reactivo(s) huérfanos sin asignación curricular válida.",
            })

        if len(questions) >= 20 and poisoned_pct >= 5.0:
            hard_penalties.append({
                "rule": "socratic_hint_poisoning",
                "deduction": 1.5,
                "reason": (
                    f"{poisoned_cnt} reactivos ({poisoned_pct}%) sufren envenenamiento anti-socrático: "
                    f"la Pista 2/3 instruye 'considerar adecuadamente' un distractor o error conceptual."
                ),
            })

        if vacuous_cnt > 0:
            hard_penalties.append({
                "rule": "vacuous_quantifier_key_corruption",
                "deduction": 1.0,
                "reason": (
                    f"{vacuous_cnt} reactivo(s) corrompen cuantificadores universales ('para todo \\varepsilon > 0' "
                    f"con constante numérica fija), invalidando la veracidad matemática de la clave."
                ),
            })

        if mem_comps_cnt > 0:
            hard_penalties.append({
                "rule": "answer_memorization_exploit",
                "deduction": round(min(2.0, mem_comps_cnt * 0.5), 2),
                "reason": (
                    f"{mem_comps_cnt} competencia(s) permiten alcanzar 'Mastered' por memorización visual "
                    f"(<= 4 respuestas correctas únicas en >= 15 reactivos)."
                ),
            })

        # 4. Formulate risk clusters and item-level issues map
        risk_clusters: dict[str, list[str]] = {
            "katex_issues": [],
            "telltale_distractors": [],
            "fstring_residues": [],
            "scaffolding_flaws": [],
            "template_residues": [],
            "blind_replacements": [],
            "cloned_distractors": [],
            "archetype_monotony": [],
            # Path-to-Mastery v2.0 clusters
            "poisoned_hints": [],
            "boilerplate_hints": [],
            "magic_multiplier_distractors": [],
            "memorizable_answers": [],
            "length_padded_options": [],
            "cross_domain_prefixes": [],
            "vacuous_quantifiers": [],
            "katex_ergonomics": [],
        }

        issues_by_item: dict[str, list[str]] = {}

        for iss in issues:
            qid = iss.item_id
            if qid not in issues_by_item:
                issues_by_item[qid] = []
            issues_by_item[qid].append(f"[{iss.severity.upper()}] {iss.message}")

            if iss.linter == "katex_frontend_ergonomics_linter":
                if qid not in risk_clusters["katex_ergonomics"]:
                    risk_clusters["katex_ergonomics"].append(qid)
                if qid not in risk_clusters["katex_issues"]:
                    risk_clusters["katex_issues"].append(qid)
            elif iss.dimension == "D5_katex" and qid not in risk_clusters["katex_issues"]:
                risk_clusters["katex_issues"].append(qid)
            elif "delatora" in iss.message.lower() and qid not in risk_clusters["telltale_distractors"]:
                risk_clusters["telltale_distractors"].append(qid)
            elif "f-string" in iss.message.lower() and qid not in risk_clusters["fstring_residues"]:
                risk_clusters["fstring_residues"].append(qid)
            elif iss.linter == "socratic_scaffolding_integrity_linter":
                if "envenenamiento" in iss.message.lower() or "fuga" in iss.message.lower():
                    if qid not in risk_clusters["poisoned_hints"]:
                        risk_clusters["poisoned_hints"].append(qid)
                else:
                    if qid not in risk_clusters["boilerplate_hints"]:
                        risk_clusters["boilerplate_hints"].append(qid)
                if qid not in risk_clusters["scaffolding_flaws"]:
                    risk_clusters["scaffolding_flaws"].append(qid)
            elif iss.dimension == "D3_scaffolding" and qid not in risk_clusters["scaffolding_flaws"]:
                risk_clusters["scaffolding_flaws"].append(qid)
            elif iss.linter == "diagnostic_rationale_alignment_linter":
                if qid not in risk_clusters["magic_multiplier_distractors"]:
                    risk_clusters["magic_multiplier_distractors"].append(qid)
            elif iss.linter == "anti_gaming_psychometric_linter":
                msg_low = iss.message.lower()
                if "memorización" in msg_low and qid not in risk_clusters["memorizable_answers"]:
                    risk_clusters["memorizable_answers"].append(qid)
                elif "relleno artificial" in msg_low and qid not in risk_clusters["length_padded_options"]:
                    risk_clusters["length_padded_options"].append(qid)
                elif "prefijo robótico" in msg_low and qid not in risk_clusters["cross_domain_prefixes"]:
                    risk_clusters["cross_domain_prefixes"].append(qid)
                elif "cuantificador universal" in msg_low and qid not in risk_clusters["vacuous_quantifiers"]:
                    risk_clusters["vacuous_quantifiers"].append(qid)
            elif iss.linter == "template_variable_residue_linter" and qid not in risk_clusters["template_residues"]:
                risk_clusters["template_residues"].append(qid)
            elif iss.linter == "blind_string_replacement_linter" and qid not in risk_clusters["blind_replacements"]:
                risk_clusters["blind_replacements"].append(qid)
            elif iss.linter == "cloned_distractor_value_linter" and qid not in risk_clusters["cloned_distractors"]:
                risk_clusters["cloned_distractors"].append(qid)
            elif iss.linter == "archetype_entropy_linter" and qid not in risk_clusters["archetype_monotony"]:
                risk_clusters["archetype_monotony"].append(qid)

        # 5. Calculate global Risk Score (0 to 100) & Mastery Path Readiness Index (0 to 100)
        total_q = max(len(questions), 1)
        critical_count = sum(1 for iss in issues if iss.severity == "critical")
        warning_count = sum(1 for iss in issues if iss.severity == "warning")
        risk_score = round(min(100.0, ((critical_count * 3.0 + warning_count * 1.0) / total_q) * 50.0), 2)
        mastery_readiness = compute_mastery_path_readiness(summaries, len(comps), len(questions))

        return TelemetryReport(
            course_id=course_id,
            title=title,
            total_competencies=len(comps),
            total_questions=len(questions),
            dimension_summaries=summaries,
            hard_penalties=hard_penalties,
            risk_score=risk_score,
            mastery_path_readiness=mastery_readiness,
            risk_clusters=risk_clusters,
            all_issues=[asdict(iss) for iss in issues],
            issues_by_item=issues_by_item,
        )


def run_full_audit(course_data: dict) -> dict:
    """Entry point for python imports."""
    registry = AuditLinterRegistry()
    telemetry = registry.execute_all(course_data)
    return asdict(telemetry)


def main():
    parser = argparse.ArgumentParser(description="Deterministic Course Audit Engine")
    parser.add_argument("--course-file", type=str, required=True, help="Path to course JSON file")
    parser.add_argument("--out", type=str, help="Optional output JSON path for telemetry")
    args = parser.parse_args()

    fpath = Path(args.course_file)
    if not fpath.exists():
        print(f"Error: File {fpath} does not exist.", file=sys.stderr)
        sys.exit(1)

    course_data = json.loads(fpath.read_text(encoding="utf-8"))
    report = run_full_audit(course_data)

    out_json = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(out_json, encoding="utf-8")
        print(f"Wrote telemetry to {args.out}")
    else:
        print(out_json)


if __name__ == "__main__":
    main()
