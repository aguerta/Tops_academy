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
    risk_clusters: Dict[str, List[str]] = field(default_factory=dict)
    all_issues: List[Dict[str, Any]] = field(default_factory=list)
    issues_by_item: Dict[str, List[str]] = field(default_factory=dict)


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
        re.compile(r"\\frac\{[^{}\n]+\{[^{}\n]+\}"),
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

            # Collect all textual fields in the question
            texts_to_check = [("stem", q.get("stem", ""))]
            for idx, opt in enumerate(q.get("options", [])):
                if isinstance(opt, dict):
                    texts_to_check.append((f"opt_{idx}_text", opt.get("text", "")))
                    texts_to_check.append((f"opt_{idx}_rationale", opt.get("error_rationale", "")))
                elif isinstance(opt, str):
                    texts_to_check.append((f"opt_{idx}_str", opt))

            for h_idx, hint in enumerate(q.get("hints", [])):
                h_text = hint.get("text", "") if isinstance(hint, dict) else str(hint)
                texts_to_check.append((f"hint_{h_idx}", h_text))

            sol = q.get("detailed_solution")
            if isinstance(sol, dict):
                texts_to_check.append(("solution_steps", " ".join(sol.get("steps", []))))
                texts_to_check.append(("solution_misconception", sol.get("misconception_warning", "")))
            elif isinstance(sol, str):
                texts_to_check.append(("solution_text", sol))

            # Execute pattern evaluations
            q_has_katex_issue = False
            for field_name, text in texts_to_check:
                if not text:
                    continue

                # 1. Unclosed nested braces
                for pat in self.UNCLOSED_BRACE_PATTERNS:
                    m = pat.search(text)
                    if m:
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
                text = opt.get("text", "")
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
            sol = q.get("detailed_solution")

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

                # Check for generic boilerplate misconception warnings
                misc_warning = sol.get("misconception_warning", "") if isinstance(sol, dict) else ""
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
            
            texts_to_check = [("stem", q.get("stem", ""))]
            for idx, opt in enumerate(q.get("options", [])):
                if isinstance(opt, dict):
                    texts_to_check.append((f"opt_{idx}_text", opt.get("text", "")))
                    texts_to_check.append((f"opt_{idx}_rationale", opt.get("error_rationale", "")))
                elif isinstance(opt, str):
                    texts_to_check.append((f"opt_{idx}_str", opt))
            for h_idx, hint in enumerate(q.get("hints", [])):
                h_text = hint.get("text", "") if isinstance(hint, dict) else str(hint)
                texts_to_check.append((f"hint_{h_idx}", h_text))
            sol = q.get("detailed_solution")
            if isinstance(sol, dict):
                texts_to_check.append(("solution_steps", " ".join(sol.get("steps", []))))
                texts_to_check.append(("solution_misconception", sol.get("misconception_warning", "")))
            elif isinstance(sol, str):
                texts_to_check.append(("solution_text", sol))

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
            
            texts_to_check = [("stem", q.get("stem", ""))]
            for idx, opt in enumerate(q.get("options", [])):
                if isinstance(opt, dict):
                    texts_to_check.append((f"opt_{idx}_text", opt.get("text", "")))
            
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

        # 3. Compute hard deductions automatically
        hard_penalties = []
        zero_hints = summaries.get("scaffolding_hints_linter", {}).get("zero_hints_count", 0)
        underpopulated = summaries.get("architecture_dag_linter", {}).get("underpopulated_competencies_count", 0)
        orphans = summaries.get("architecture_dag_linter", {}).get("orphan_questions_count", 0)

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

        # 4. Formulate risk clusters and item-level issues map
        risk_clusters: dict[str, list[str]] = {
            "katex_issues": [],
            "telltale_distractors": [],
            "fstring_residues": [],
            "scaffolding_flaws": [],
            "template_residues": [],
            "blind_replacements": [],
        }

        issues_by_item: dict[str, list[str]] = {}

        for iss in issues:
            qid = iss.item_id
            if qid not in issues_by_item:
                issues_by_item[qid] = []
            issues_by_item[qid].append(f"[{iss.severity.upper()}] {iss.message}")

            if iss.dimension == "D5_katex" and qid not in risk_clusters["katex_issues"]:
                risk_clusters["katex_issues"].append(qid)
            elif "delatora" in iss.message.lower() and qid not in risk_clusters["telltale_distractors"]:
                risk_clusters["telltale_distractors"].append(qid)
            elif "f-string" in iss.message.lower() and qid not in risk_clusters["fstring_residues"]:
                risk_clusters["fstring_residues"].append(qid)
            elif iss.dimension == "D3_scaffolding" and qid not in risk_clusters["scaffolding_flaws"]:
                risk_clusters["scaffolding_flaws"].append(qid)
            elif iss.linter == "template_variable_residue_linter" and qid not in risk_clusters["template_residues"]:
                risk_clusters["template_residues"].append(qid)
            elif iss.linter == "blind_string_replacement_linter" and qid not in risk_clusters["blind_replacements"]:
                risk_clusters["blind_replacements"].append(qid)

        # 5. Calculate global Risk Score (0 to 100)
        total_q = max(len(questions), 1)
        critical_count = sum(1 for iss in issues if iss.severity == "critical")
        warning_count = sum(1 for iss in issues if iss.severity == "warning")
        risk_score = round(min(100.0, ((critical_count * 3.0 + warning_count * 1.0) / total_q) * 50.0), 2)

        return TelemetryReport(
            course_id=course_id,
            title=title,
            total_competencies=len(comps),
            total_questions=len(questions),
            dimension_summaries=summaries,
            hard_penalties=hard_penalties,
            risk_score=risk_score,
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
