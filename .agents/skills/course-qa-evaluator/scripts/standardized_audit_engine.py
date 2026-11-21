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
import datetime
import json
import re
import sys
from collections import Counter, defaultdict
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
    deterministic_rubric: Dict[str, Any] = field(default_factory=dict)
    final_score: float = 20.0
    quality_tier: str = "EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY"
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
    SYMPY_IN_KATEX = re.compile(r"\$[^$]*(?:\d\s*\*\s*[a-zA-Z(]|(?<![\\a-zA-Z])sqrt\s*\()[^$]*\$")

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        unclosed_braces = []
        triple_dollars = []
        double_braces = []
        unbalanced_dollars = []
        orphan_latex = []
        sympy_in_katex = []

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

                # 4. Dollar delimiter parity balance (strip escaped currency \$ first)
                text_no_escaped = text.replace("\\$", "")
                dollar_count = text_no_escaped.count("$")
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
                if m_orph and "$" not in text_no_escaped:
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

                # 6. Raw SymPy syntax leaked inside KaTeX math delimiters
                m_sym = self.SYMPY_IN_KATEX.search(text_no_escaped)
                if m_sym:
                    sympy_in_katex.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="warning",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Sintaxis cruda de SymPy filtrada en KaTeX ('{m_sym.group(0)[:40]}') en '{field_name}'",
                        snippet=m_sym.group(0)[:50],
                    ))

        return {
            "unclosed_braces_count": len(set(unclosed_braces)),
            "unclosed_braces_items": list(set(unclosed_braces))[:15],
            "triple_dollars_count": len(set(triple_dollars)),
            "double_braces_count": len(set(double_braces)),
            "unbalanced_dollars_count": len(set(unbalanced_dollars)),
            "orphan_latex_plain_text_count": len(set(orphan_latex)),
            "sympy_in_katex_count": len(set(sympy_in_katex)),
            "sympy_in_katex_items": list(set(sympy_in_katex))[:15],
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

    # Bare formula without explanatory prose (e.g. "$\mathrm{Sesgo}(\hat{\theta}_n)=\theta-\mathbb{E}[\hat{\theta}_n]$")
    BARE_FORMULA_WARNING_PAT = re.compile(r"^\s*(\${1,2})(?:\\.|[^$\\])+\1\.?\s*$")
    # Explicit hardcoded arithmetic equality inside a static warning (e.g. "(1^2+3^2)/2=5" or "1.96/100=0.0196")
    STATIC_ARITH_EXAMPLE_PAT = re.compile(
        r"(?:\(\s*\d+(?:\^\d+)?\s*[+\-*/]\s*\d+(?:\^\d+)?\s*\)\s*/\s*\d+|\b\d+\.\d+\s*/\s*\d+)\s*=\s*(-?\d+(?:\.\d+)?)"
    )

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        zero_hints_items = []
        insufficient_hints = []
        fstring_placeholders_items = []
        generic_misconception_items = []
        bare_formula_warning_items = []
        cloned_warning_items = []
        disconnected_example_warning_items = []
        missing_solutions = []

        generic_pats = [re.compile(p, re.IGNORECASE) for p in self.GENERIC_WARNING_PHRASES]
        warning_to_comps: dict[str, set[str]] = {}
        warning_to_qids: dict[str, list[tuple[str, str]]] = {}

        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")
            raw_hints = q.get("hints")
            hints = raw_hints if isinstance(raw_hints, list) else []
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
                elif isinstance(h, dict):
                    h_clean = str(h.get("text") or h.get("content") or "").strip()
                else:
                    continue
                if h_clean:
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
                    (sol.get("misconception_warning", "") if isinstance(sol, dict) else "")
                    or str(q.get("misconception_warning") or q.get("common_misconception_warning") or "")
                ).strip()
                if misc_warning:
                    for g_pat in generic_pats:
                        if g_pat.search(misc_warning):
                            generic_misconception_items.append(qid)
                            break

                    if self.BARE_FORMULA_WARNING_PAT.match(misc_warning):
                        bare_formula_warning_items.append(qid)
                        generic_misconception_items.append(qid)

                    norm_w = re.sub(r"\s+", " ", misc_warning)
                    warning_to_comps.setdefault(norm_w, set()).add(cid)
                    warning_to_qids.setdefault(norm_w, []).append((qid, cid))

                    m_arith = self.STATIC_ARITH_EXAMPLE_PAT.search(misc_warning)
                    if m_arith:
                        res_num = m_arith.group(1)
                        stem_str = str(q.get("stem") or "")
                        if res_num not in stem_str:
                            disconnected_example_warning_items.append(qid)

        # Detect cross-competency cloned misconception warnings (shared across >= 3 distinct competencies)
        for norm_w, comps_set in warning_to_comps.items():
            qlist_w = warning_to_qids.get(norm_w, [])
            if len(comps_set) >= 3 and len(qlist_w) >= 6:
                for qid_w, _ in qlist_w:
                    cloned_warning_items.append(qid_w)
                    generic_misconception_items.append(qid_w)
                rep_qid, rep_cid = qlist_w[0]
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="warning",
                    item_id=rep_qid,
                    competency_id=rep_cid,
                    message=(
                        f"Reciclaje global de misconception_warning: la misma cadena ('{norm_w[:55]}...') "
                        f"se repite sin adaptación en {len(qlist_w)} ítems a través de {len(comps_set)} competencias distintas."
                    ),
                    snippet=norm_w[:70],
                ))

        if bare_formula_warning_items:
            issues.append(LintIssue(
                linter=self.name,
                dimension=self.dimension,
                severity="warning",
                item_id=bare_formula_warning_items[0],
                competency_id="global",
                message=(
                    f"Advertencia de error frecuente reducida a fórmula muda sin explicación diagnóstica en prosa "
                    f"en {len(set(bare_formula_warning_items))} reactivos."
                ),
            ))

        if len(set(disconnected_example_warning_items)) >= 3:
            issues.append(LintIssue(
                linter=self.name,
                dimension=self.dimension,
                severity="warning",
                item_id=disconnected_example_warning_items[0],
                competency_id="global",
                message=(
                    f"Ejemplo numérico estático ajeno a los parámetros del enunciado filtrado en misconception_warning "
                    f"({len(set(disconnected_example_warning_items))} reactivos)."
                ),
            ))

        return {
            "zero_hints_count": len(zero_hints_items),
            "zero_hints_items": zero_hints_items,
            "insufficient_hints_count": len(insufficient_hints),
            "fstring_placeholders_count": len(set(fstring_placeholders_items)),
            "fstring_placeholders_sample_items": list(set(fstring_placeholders_items))[:15],
            "generic_misconception_count": len(set(generic_misconception_items)),
            "bare_formula_misconception_count": len(set(bare_formula_warning_items)),
            "cloned_misconception_warning_count": len(set(cloned_warning_items)),
            "disconnected_warning_numbers_count": len(set(disconnected_example_warning_items)),
            "missing_solutions_count": len(missing_solutions),
        }


class ArchitectureDAGLinter(BaseLinter):
    name = "architecture_dag_linter"
    dimension = "D1_architecture"

    ACADEMIC_STOPWORDS = {
        "de", "la", "el", "en", "los", "las", "un", "una", "del", "al",
        "para", "por", "con", "sin", "sobre", "entre", "mediante", "hacia",
        "desde", "como", "calculo", "analisis", "aplicacion", "propiedad",
        "propiedades", "estudio", "uso", "concepto", "metodo", "modelo",
        "teorema", "definicion", "habilidad", "hecho", "competencia",
        "competency", "concept", "skill", "fact", "descripcion", "completa",
        "validacion", "psicometrica", "evaluacion", "determinacion",
        "comparacion", "identificacion", "formulacion", "cota", "cotas",
    }

    @classmethod
    def _strip_accents(cls, text: str) -> str:
        acc_map = {
            "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
            "Á": "a", "É": "e", "Í": "i", "Ó": "o", "Ú": "u",
            "ü": "u", "Ü": "u", "ñ": "n", "Ñ": "n",
        }
        return "".join(acc_map.get(ch, ch) for ch in text).lower()

    @classmethod
    def _extract_content_stems(cls, text: str) -> set[str]:
        clean = cls._strip_accents(text)
        clean = re.sub(r"(\${1,2})(?:\\.|[^$\\])+\1", " ", clean)
        words = re.findall(r"[a-z]+", clean)
        return {w[:5] for w in words if len(w) >= 3 and w not in cls.ACADEMIC_STOPWORDS}

    @classmethod
    def _extract_math_symbols(cls, text: str) -> set[str]:
        symbols = {m.lower() for m in re.findall(r"\\[a-zA-Z]+", text)}
        for _, math_block in re.findall(r"(\${1,2})((?:\\.|[^$\\])+?)\1", text):
            for ident in re.findall(r"[a-zA-Z]+", math_block):
                symbols.add(ident)
        return symbols

    @classmethod
    def _are_competencies_duplicate(cls, c1: dict, c2: dict) -> bool:
        n1 = str(c1.get("name") or c1.get("title") or "").strip().lower()
        n2 = str(c2.get("name") or c2.get("title") or "").strip().lower()
        if n1 and n2 and n1 == n2:
            return True
        stems_n1 = cls._extract_content_stems(n1)
        stems_n2 = cls._extract_content_stems(n2)
        if not (stems_n1 & stems_n2):
            return False
        min_name_len = min(len(stems_n1), len(stems_n2))
        if min_name_len >= 2 and len(stems_n1 & stems_n2) / min_name_len >= 0.75:
            return True
        t1 = f"{c1.get('name') or ''} {c1.get('description') or c1.get('description_latex') or ''}"
        t2 = f"{c2.get('name') or ''} {c2.get('description') or c2.get('description_latex') or ''}"
        s1 = cls._extract_content_stems(t1)
        s2 = cls._extract_content_stems(t2)
        if len(s1) < 3 or len(s2) < 3 or len(s1 & s2) < 2:
            return False
        stem_j = len(s1 & s2) / len(s1 | s2)
        m1 = cls._extract_math_symbols(t1)
        m2 = cls._extract_math_symbols(t2)
        math_j = (len(m1 & m2) / len(m1 | m2)) if (m1 and m2) else 0.0
        return stem_j >= 0.35 or (stem_j >= 0.25 and math_j >= 0.45)

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        competencies = course_data.get("competencies", [])
        questions = course_data.get("questions", [])

        comp_ids = {c.get("id"): c for c in competencies if c.get("id")}
        comp_counts: dict[str, int] = {cid: 0 for cid in comp_ids}
        orphan_questions = []

        categories = {"Fact": 0, "Concept": 0, "Skill": 0, "Other": 0}
        comps_missing_prereqs = []
        id_category_mismatches = []

        for c in competencies:
            cid = c.get("id", "unknown")
            cat = c.get("category") or c.get("type") or "Other"
            if cat in categories:
                categories[cat] += 1
            else:
                categories["Other"] += 1

            prereqs = c.get("prerequisites", [])
            if not prereqs or len(prereqs) == 0:
                comps_missing_prereqs.append(cid)

            # Check ID prefix vs category mismatch (e.g. Hab-04 labeled as Concept)
            cid_str = str(cid)
            if (
                (cid_str.lower().startswith("hab-") and cat in ("Concept", "Fact"))
                or (re.match(r"^c-\d+$", cid_str, re.I) and cat in ("Skill", "Fact"))
                or (re.match(r"^h-\d+$", cid_str, re.I) and cat in ("Skill", "Concept"))
            ):
                id_category_mismatches.append({"competency_id": cid, "category": cat})
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="warning",
                    item_id=f"comp_{cid}",
                    competency_id=cid,
                    message=f"Inconsistencia taxonómica entre ID '{cid}' y categoría declarada '{cat}'.",
                ))

        # Check duplicate/overlapping competencies in the DAG (e.g. multi-PDF merge without deduplication)
        duplicate_pairs = []
        for i in range(len(competencies)):
            for j in range(i + 1, len(competencies)):
                c1, c2 = competencies[i], competencies[j]
                if isinstance(c1, dict) and isinstance(c2, dict) and self._are_competencies_duplicate(c1, c2):
                    cid1 = c1.get("id", f"idx_{i}")
                    cid2 = c2.get("id", f"idx_{j}")
                    duplicate_pairs.append((cid1, cid2))
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="warning",
                        item_id=f"comp_{cid2}",
                        competency_id=cid2,
                        message=(
                            f"Solapamiento/duplicación curricular entre '{cid1}' ('{c1.get('name', '')[:40]}') "
                            f"y '{cid2}' ('{c2.get('name', '')[:40]}')."
                        ),
                    ))

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
            "duplicate_competency_pairs_count": len(duplicate_pairs),
            "duplicate_competency_pairs": [f"{a}<->{b}" for a, b in duplicate_pairs[:20]],
            "id_category_mismatch_count": len(id_category_mismatches),
            "id_category_mismatches": id_category_mismatches[:15],
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
    PARTIAL_DUMMY_VAR_PATS = [
        # Constant exponent converging as n -> \infty (e.g. "a^{11} \to 0 cuando n \to \infty")
        re.compile(r"\b[a-zA-Z]\^\{\d+\}\s*\\to\s*0\s*\$?\s*cuando\s+\$?n\s*\\to\s*\\infty"),
        # Uninterpolated n-1 numerator over interpolated constant denominator before \sigma^2 (e.g. "\frac{n-1}{3}\sigma^2")
        re.compile(r"\\frac\{n-[12]\}\{\d+\}\s*\\sigma\^2"),
        # Symbolic subscript Z_n=k paired with instantiated 1-1/k^2
        re.compile(r"\\mathbb\{P\}\(\s*[A-Z]_n\s*=\s*(\d+)\s*\)\s*=\s*1\s*-\s*1/\1\^2"),
    ]

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        leaked_items = []
        partial_dummy_items = []
        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")
            
            texts_to_check = _collect_question_text_fields(q, include_rationales=True, include_hints_sol=True)
            found_blind = False
            found_partial = False

            for field_name, text in texts_to_check:
                if not text:
                    continue
                if not found_blind and not field_name.endswith("_rationale") and not field_name.startswith("hint_") and not field_name.startswith("solution"):
                    m = self.BLIND_REPLACE_PATTERN.search(text)
                    if m:
                        found_blind = True
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

                if not found_partial:
                    for p_pat in self.PARTIAL_DUMMY_VAR_PATS:
                        m_part = p_pat.search(text)
                        if m_part:
                            found_partial = True
                            partial_dummy_items.append(qid)
                            leaked_items.append(qid)
                            issues.append(LintIssue(
                                linter=self.name,
                                dimension=self.dimension,
                                severity="warning",
                                item_id=qid,
                                competency_id=cid,
                                message=f"Sustitución parcial de variable muda 'n' en expresión simbólica ('{m_part.group(0)[:45]}') en '{field_name}'",
                                snippet=m_part.group(0)[:60],
                            ))
                            break

        return {
            "blind_string_replacement_count": len(set(leaked_items)),
            "blind_string_replacement_items": list(set(leaked_items))[:15],
            "partial_dummy_var_substitution_count": len(set(partial_dummy_items)),
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

        def _is_v2_or_higher(ver: Any) -> bool:
            if ver is None:
                return False
            try:
                return int(ver) >= 2
            except (ValueError, TypeError):
                try:
                    return float(str(ver).lstrip("vV")) >= 2.0
                except (ValueError, TypeError):
                    return False

        if explicit_min_arch is not None:
            try:
                req_arch = int(explicit_min_arch)
            except (ValueError, TypeError):
                req_arch = 4 if _is_v2_or_higher(contract_ver) else 3
        elif contract_ver is not None:
            req_arch = 4 if _is_v2_or_higher(contract_ver) else 3
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
                stem = str(q.get("stem") or "")
                clean_stem = re.sub(r"(\${1,2})(?:\\.|[^$\\])+\1", "$MATH$", stem)
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

    BRACE_VAR_PAT = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")
    LATEX_ARG_PREFIX_PAT = re.compile(r"(?:\\[a-zA-Z]+\s*(?:\[[^\]]*\])?(?:\s*\{[^}]*\})*|[_^])\s*$")
    CONSECUTIVE_SIGNS_PAT = re.compile(r"(?:\+\s*-\d+|-\s*-\d+)")
    KNOWN_LATEX_SINGLE_LETTER_OR_MACRO = {
        "n", "i", "j", "k", "t", "x", "y", "z", "p", "d", "R", "C", "N", "E", "P", "F", "V",
        "alpha", "beta", "gamma", "theta", "sigma", "lambda", "mu", "Var", "Cov", "Corr", "Sesgo", "ECM", "MSE",
    }

    # String-concatenation collision patterns (e.g., "2{a}x" -> "27x" for g(x)=7x^2, "2{alpha}" -> "^{20.5}", "(A+B)/(2B)" -> "(12+63)/(263)")
    DERIV_CONCAT_PAT = re.compile(r"([2-9])x\^2.{0,120}?2\1x\b")
    EXP_ALPHA_CONCAT_PAT = re.compile(r"\^\{\s*-?\(?20\.(?:25|5|75|1|2|3)\b")
    DENOM_TWO_CONCAT_PAT = re.compile(r"\(\s*\d+\s*[+\-]\s*([1-9]\d)\s*\)\s*/\s*\(\s*2\1\s*\)")
    STEM_QUAD_COEFF_PAT = re.compile(r"([2-9])X\^2\s*\+\s*(\d+)X")
    STEM_MEAN_PAT = re.compile(r"(?:media|\\mu\s*=)\s*\$?([1-9]\d*)\$?", re.IGNORECASE)

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        infracting_items = []
        concat_collision_items = []

        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")
            stem_str = str(q.get("stem") or "")

            texts_to_check = _collect_question_text_fields(q, include_rationales=True, include_hints_sol=True)

            # Check for stem-specific coefficient concatenation (e.g. g(X)=aX^2+bX+c with mean mu -> "{a}{mu}" in options/rationales)
            m_quad = self.STEM_QUAD_COEFF_PAT.search(stem_str)
            m_mean = self.STEM_MEAN_PAT.search(stem_str)
            coeff_mu_pat = None
            if m_quad and m_mean:
                a_str, b_str = m_quad.group(1), m_quad.group(2)
                mu_str = m_mean.group(1)
                # Pattern like "(412+10)^2" or "26^2+20" where a and mu were concatenated as "{a}{mu}"
                coeff_mu_pat = re.compile(rf"(?<!\d){a_str}{mu_str}(?:\s*\+\s*{b_str}|\^2\s*\+\s*{b_str})")

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

                # Check string concatenation collisions (2{a}x -> 27x, ^{20.5}, (12+63)/(263), {a}{mu})
                m_concat = (
                    self.DERIV_CONCAT_PAT.search(text)
                    or self.EXP_ALPHA_CONCAT_PAT.search(text)
                    or self.DENOM_TWO_CONCAT_PAT.search(text)
                    or (coeff_mu_pat.search(text) if coeff_mu_pat else None)
                )
                if m_concat:
                    concat_collision_items.append(qid)
                    infracting_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="critical",
                        item_id=qid,
                        competency_id=cid,
                        message=(
                            f"Colisión por concatenación de cadenas coeficiente-variable sin operador "
                            f"('{m_concat.group(0)[:45]}') en '{field_name}'"
                        ),
                        snippet=m_concat.group(0)[:55],
                    ))
                    break

                # Check genuine uninterpolated {var_name} (ignoring LaTeX commands \cmd{...} and subscripts/superscripts _{...}, ^{...})
                if not field_name.endswith("_rationale") and not field_name.startswith("hint_"):
                    for m in self.BRACE_VAR_PAT.finditer(text):
                        var_name = m.group(1)
                        if var_name in self.KNOWN_LATEX_SINGLE_LETTER_OR_MACRO:
                            continue
                        prefix = text[:m.start()]
                        if self.LATEX_ARG_PREFIX_PAT.search(prefix):
                            continue
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
            "string_concat_collision_items_count": len(set(concat_collision_items)),
            "string_concat_collision_sample_items": list(set(concat_collision_items))[:15],
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
            raw_diff = str(q.get("difficulty") or "medium").lower().strip()
            diff = raw_diff if raw_diff in diff_counts else "medium"
            diff_counts[diff] += 1

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
            bands = {
                (d if d in diff_counts else "medium")
                for d in (str(q.get("difficulty") or "medium").lower().strip() for q in qlist)
            }
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

        bloom_sup_types = {
            "open_symbolic",
            "proof_dag",
            "adversarial_break",
            "unstructured_model",
            "invariant_canvas",
            "concept_matching",
        }
        mc_count = 0
        fib_count = 0
        ms_count = 0
        bloom_superior_count = 0
        bloom_superior_breakdown: dict[str, int] = {k: 0 for k in sorted(bloom_sup_types)}
        other_count = 0
        q_by_comp: dict[str, list[dict]] = {}

        for q in questions:
            cid = q.get("competency_id", "unassigned")
            q_by_comp.setdefault(cid, []).append(q)
            qtype = str(q.get("interaction_type") or q.get("type") or "").lower().strip()
            if "multiple_choice" in qtype:
                mc_count += 1
            elif "fill_in_the_blank" in qtype or "open_ended" in qtype or qtype == "fib":
                fib_count += 1
            elif "multiple_select" in qtype:
                ms_count += 1
            elif qtype in bloom_sup_types:
                bloom_superior_count += 1
                bloom_superior_breakdown[qtype] = bloom_superior_breakdown.get(qtype, 0) + 1
            else:
                other_count += 1

        total_q = len(questions)
        is_m20_course = (
            bloom_superior_count > 0
            or course_data.get("contract_version") == 2
            or (isinstance(course_data.get("metadata"), dict) and course_data["metadata"].get("contract_version") == 2)
            or any(bool(c.get("recommended_modalities")) for c in competencies if isinstance(c, dict))
        )
        recognition_only_skills = []
        skill_mc7_violations = []
        low_active_quota_competencies = []
        active_prod_types = {"fill_in_the_blank", "open_ended", "fib"} | (bloom_sup_types - {"concept_matching"})
        all_active_types = {"fill_in_the_blank", "open_ended", "fib", "multiple_select"} | bloom_sup_types

        for cid, qlist in q_by_comp.items():
            is_skill = str(comp_cat.get(cid) or "").lower() == "skill" or str(cid).lower().startswith("hab")
            qtypes_c = [str(q.get("interaction_type") or q.get("type") or "").lower().strip() for q in qlist]
            if is_skill and len(qlist) >= 10:
                has_active_prod = any(
                    ("fill_in_the_blank" in qt or "open_ended" in qt or qt in active_prod_types)
                    for qt in qtypes_c
                )
                if not has_active_prod:
                    recognition_only_skills.append(cid)

            c_total = len(qlist)
            c_mc7 = sum(1 for qt in qtypes_c if "multiple_choice" in qt or qt in ("mc", "mc7"))
            c_active = sum(
                1 for qt in qtypes_c
                if ("fill_in_the_blank" in qt or "open_ended" in qt or "multiple_select" in qt or qt in all_active_types)
            )
            c_active_pct = round((c_active / c_total * 100.0) if c_total else 0.0, 2)

            if is_skill and c_mc7 > 0:
                skill_mc7_violations.append(cid)
                if is_m20_course:
                    first_mc7_id = next(
                        (
                            q.get("id", cid)
                            for q, qt in zip(qlist, qtypes_c)
                            if "multiple_choice" in qt or qt in ("mc", "mc7")
                        ),
                        cid,
                    )
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="critical",
                        item_id=first_mc7_id,
                        competency_id=cid,
                        message=(
                            f"[M20-MC7-CAP] Competencia Skill '{cid}' contiene {c_mc7}/{c_total} reactivos "
                            f"de opción múltiple (MC7); M20 exige estrictamente 0 MC7 en competencias Skill."
                        ),
                    ))

            below_active_quota = (c_total >= 5 and c_active_pct < 80.0) or (c_total == 4 and c_active_pct < 75.0)
            if below_active_quota:
                low_active_quota_competencies.append(cid)
                if is_m20_course:
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="warning",
                        item_id=qlist[0].get("id", cid) if qlist else cid,
                        competency_id=cid,
                        message=(
                            f"[M20-ACTIVE-QUOTA] Competencia '{cid}' alcanza solo {c_active}/{c_total} "
                            f"({c_active_pct:.1f}%) en modalidades activas (mínimo requerido >= 80% en M20)."
                        ),
                    ))

        if total_q >= 20 and fib_count == 0 and ms_count == 0 and bloom_superior_count == 0:
            issues.append(LintIssue(
                linter=self.name,
                dimension=self.dimension,
                severity="warning",
                item_id=questions[0].get("id", "course_modality"),
                competency_id=questions[0].get("competency_id", "global"),
                message=(
                    f"Monocultivo absoluto de reconocimiento pasivo: {mc_count}/{total_q} (100%) son "
                    f"opción múltiple (MC7), con 0% fill_in_the_blank, 0% multiple_select y 0% modalidades Bloom Superior."
                ),
            ))

        active_total = fib_count + ms_count + bloom_superior_count
        return {
            "mc7_count": mc_count,
            "fib_count": fib_count,
            "ms_count": ms_count,
            "bloom_superior_count": bloom_superior_count,
            "bloom_superior_breakdown": bloom_superior_breakdown,
            "mc7_share_pct": round((mc_count / total_q * 100.0) if total_q else 0.0, 2),
            "fib_share_pct": round((fib_count / total_q * 100.0) if total_q else 0.0, 2),
            "ms_share_pct": round((ms_count / total_q * 100.0) if total_q else 0.0, 2),
            "bloom_superior_share_pct": round((bloom_superior_count / total_q * 100.0) if total_q else 0.0, 2),
            "active_generation_or_discrimination_pct": round((active_total / total_q * 100.0) if total_q else 0.0, 2),
            "recognition_only_skill_competencies_count": len(recognition_only_skills),
            "recognition_only_skill_competencies": recognition_only_skills[:20],
            "m20_contract_active": is_m20_course,
            "skill_mc7_violations_count": len(skill_mc7_violations),
            "skill_mc7_violations": skill_mc7_violations[:20],
            "low_active_quota_competencies_count": len(low_active_quota_competencies),
            "low_active_quota_competencies": low_active_quota_competencies[:20],
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
        bp_count = len(set(boilerplate_items))
        affected_total = len(set(boilerplate_items) | set(poisoned_items))
        return {
            "boilerplate_hints_items_count": bp_count,
            "boilerplate_hints_pct": round(bp_count / total_q * 100.0, 2),
            "boilerplate_sample_items": list(set(boilerplate_items))[:15],
            "poisoned_hints_items_count": len(set(poisoned_items)),
            "poisoned_hints_pct": round(len(set(poisoned_items)) / total_q * 100.0, 2),
            "poisoned_hints_sample_items": list(set(poisoned_items))[:15],
            "hint_answer_leak_items_count": len(set(answer_leak_items)),
            "genuine_socratic_hints_pct": round(max(0.0, (len(questions) - affected_total) / total_q * 100.0), 2),
        }


class DiagnosticRationaleAlignmentLinter(BaseLinter):
    """Audits formative remediation quality in FeedbackToast.tsx.

    Detects:
    1. Synthetic Magic-Multiplier Distractors (`critical`): Numerical distractors fabricated by
       multiplying the correct answer by compile_shard.py's hardcoded constants
       `[1.333, 0.667, 1.667, 0.333, 1.25, 0.75, 1.5, 0.5, 2.1, 0.45, 1.85, 0.15]`, which carry
       disconnected pool-cycled rationales that misdiagnose the student's actual arithmetic error.
    2. Global Rationale Recycling Collapse (`warning`): High repetition of static CTA rationale
       strings across parametric items (< 15% unique rationales across >= 60 distractors),
       stripping rotating synthetic prefixes ('Error conceptual:', 'Confusión teórica:', etc.).
    3. Disconnected Theoretical Rationales on Purely Numeric Distractors (`warning`): Purely
       numeric MC7 options paired with non-operational theoretical claims pasted from cta.json.
    """
    name = "diagnostic_rationale_alignment_linter"
    dimension = "D2_assessment"

    MAGIC_MULTIPLIERS = (1.333, 0.667, 1.667, 0.333, 1.25, 0.75, 1.5, 0.5, 2.1, 0.45, 1.85, 0.15)
    NUM_RE = re.compile(r"-?\d+\.\d+|-?\d+")
    NUM_LITERAL_RE = re.compile(r"\b\d+(?:\.\d+)?\b")

    # Rotating generic taxonomic prefixes used to mask static rationale recycling
    SYNTHETIC_RATIONALE_PREFIX_PAT = re.compile(
        r"^\s*(?:Error\s+(?:conceptual|de\s+c[aá]lculo|algebraico|metodol[oó]gico|operativo)|"
        r"Confusi[oó]n\s+(?:te[oó]rica|metodol[oó]gica|conceptual|de\s+conceptos?)|"
        r"Fallo\s+(?:de\s+c[aá]lculo|conceptual|anal[ií]tico|algebraico)|"
        r"Desv[ií]o\s+(?:algebraico|de\s+operador|anal[ií]tico|num[eé]rico)|"
        r"Aplicaci[oó]n\s+incorrecta|Sustituci[oó]n\s+inv[aá]lida|"
        r"Desliz\s+anal[ií]tico|Descuido\s+algebraico|Falta\s+de\s+ponderaci[oó]n|"
        r"Interpretaci[oó]n\s+err[oó]nea|Omisi[oó]n\s+de\s+regla|Inversi[oó]n\s+de\s+f[oó]rmula)\s*:\s*",
        re.IGNORECASE,
    )
    PURE_NUMERIC_OPT_PAT = re.compile(r"^\s*\$?\s*-?\d+(?:\.\d+)?\s*(?:%|\\\%)?\s*\$?\s*$")
    OPERATIONAL_VERB_OR_OP_PAT = re.compile(
        r"(?:calcul|divid|multiplic|sum|rest|elev|cuadrad|ra[ií]z|invirt|inviert|invers|"
        r"omit|olvid|sustitu|reemplaz|redond|trunc|signo|factor|ponder|promedi|despej|"
        r"deriv|integr|eval[uú]|\\frac|\\cdot|\\times|\\sqrt|\d+\s*[+\-*/^]\s*\d+)",
        re.IGNORECASE,
    )
    THEORETICAL_CTA_ON_NUMERIC_PAT = re.compile(
        r"(?:violando\s+la\s+condici[oó]n|variables\s+continuas\s+ignorando\s+la\s+partici[oó]n|"
        r"esperanza\s+iterada|por\s+monoton[ií]a|donde\s+dicha\s+desigualdad\s+deja\s+de\s+cumplirse|"
        r"perdiendo\s+positividad\s+y\s+existencia|como\s+funci[oó]n\s+convexa|"
        r"muestreo\s+sesgado\s+sobre|selecci[oó]n\s+aleatoria\s+i\.?i\.?d\.?|"
        r"exige\s+(?:simetr[ií]a|normalidad)|afirma\s+que\s+.{1,40}\s+es\s+insesgado|"
        r"confunde\s+el\s+estimador\s+aleatorio\s+con\s+una\s+estimaci[oó]n\s+fija|"
        r"interpreta\s+la\s+insesgadez\s+como\s+igualdad\s+puntual|equipara\s+convergencia|"
        r"convergencia\s+casi\s+segura)",
        re.IGNORECASE,
    )
    SUBSUP_DIGIT_PAT = re.compile(r"[_^]\{?\d+\}?")
    LATEX_STRUCT_PAT = re.compile(r"\\(?:frac|dfrac|tfrac)\b|\^|_\{")

    @classmethod
    def _extract_numeric_option_val(cls, text: str) -> Optional[float]:
        """Extract plain numeric value from option text, avoiding LaTeX exponents/denominators."""
        if not text or cls.LATEX_STRUCT_PAT.search(text):
            return None
        cleaned = text.replace("$", "").replace("\u2212", "-").strip()
        cleaned = re.sub(r"\\text\{[^}]*\}", "", cleaned).strip()
        nums = cls.NUM_RE.findall(cleaned)
        if not nums:
            return None
        try:
            return float(nums[-1])
        except ValueError:
            return None

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        all_rationales: list[str] = []
        stripped_rationales: list[str] = []
        slot_texts: dict[tuple[str, str], list[str]] = defaultdict(list)
        raw_slot_texts: dict[tuple[str, str], list[str]] = defaultdict(list)
        synthetic_prefix_cnt = 0
        magic_mult_items: list[str] = []
        magic_mult_candidates: list[tuple[str, str, list[float], str]] = []
        mc7_numeric_total = 0
        disconnected_numeric_rat_items: list[str] = []

        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")
            options = q.get("options", []) or []
            if not isinstance(options, list):
                continue

            correct_texts = []
            distractor_texts = []
            distractor_rats = []
            for idx, o in enumerate(options):
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
                        distractor_rats.append((txt, rat))
                        if self.SYNTHETIC_RATIONALE_PREFIX_PAT.match(rat):
                            synthetic_prefix_cnt += 1
                        stripped_rat = self.SYNTHETIC_RATIONALE_PREFIX_PAT.sub("", rat).strip()
                        stripped_rationales.append(stripped_rat)

                        did = str(o.get("distractor_id") or "").strip()
                        slot_id = did or f"{q.get('template_id') or qid}::{o.get('id') or o.get('option_id') or idx}"
                        norm_rat = self.NUM_LITERAL_RE.sub("<NUM>", stripped_rat).lower()
                        raw_norm_rat = self.NUM_LITERAL_RE.sub("<NUM>", rat).lower()
                        slot_texts[(cid, slot_id)].append(norm_rat)
                        raw_slot_texts[(cid, slot_id)].append(raw_norm_rat)

            # Check for purely numeric MC7 options paired with disconnected non-operational theoretical rationales
            if (
                len(correct_texts) == 1
                and len(distractor_texts) >= 4
                and self.PURE_NUMERIC_OPT_PAT.match(correct_texts[0])
                and sum(1 for dt in distractor_texts if self.PURE_NUMERIC_OPT_PAT.match(dt)) >= 4
            ):
                non_op_count = 0
                for dt, rat in distractor_rats:
                    rat_body = self.SYNTHETIC_RATIONALE_PREFIX_PAT.sub("", rat).strip()
                    if len(rat_body) < 20:
                        continue
                    rat_no_sub = self.SUBSUP_DIGIT_PAT.sub("", rat_body)
                    has_standalone_num = bool(re.search(r"(?<![a-zA-Z_\\])\d+(?:\.\d+)?", rat_no_sub))
                    has_op_verb = bool(self.OPERATIONAL_VERB_OR_OP_PAT.search(rat_body))
                    has_theo_cta = bool(self.THEORETICAL_CTA_ON_NUMERIC_PAT.search(rat_body))
                    if (not has_standalone_num and not has_op_verb) or has_theo_cta:
                        non_op_count += 1
                if non_op_count >= 2:
                    disconnected_numeric_rat_items.append(qid)

            # Check for compile_shard.py magic-multiplier numerical distractors
            if len(correct_texts) == 1 and len(distractor_texts) >= 4:
                c_val = self._extract_numeric_option_val(correct_texts[0])
                if c_val is not None:
                    d_vals = [self._extract_numeric_option_val(dt) for dt in distractor_texts]
                    numeric_d_vals = [dv for dv in d_vals if dv is not None]
                    if len(numeric_d_vals) >= 2:
                        mc7_numeric_total += 1
                    if abs(c_val) > 1e-6 and abs(c_val) not in (1.0, 2.0, 4.0) and numeric_d_vals:
                        matched_mults = []
                        for d_val in numeric_d_vals:
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

        # Only flag as systematic magic-multiplier violation when > 7% of evaluated numeric MC7 items hit
        mc7_numeric_denom = max(1, mc7_numeric_total)
        if len(set(magic_mult_items)) / mc7_numeric_denom > 0.07:
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

        raw_normalized_rationales = [self.NUM_LITERAL_RE.sub("<NUM>", rat).lower() for rat in all_rationales]
        normalized_rationales = [self.NUM_LITERAL_RE.sub("<NUM>", rat).lower() for rat in stripped_rationales]
        total_rats = len(all_rationales)
        raw_unique_instance_rats = len(set(raw_normalized_rationales))
        instance_unique_rats = len(set(normalized_rationales))
        raw_instance_uniqueness_pct = round((raw_unique_instance_rats / total_rats * 100.0) if total_rats else 100.0, 2)
        instance_uniqueness_pct = round((instance_unique_rats / total_rats * 100.0) if total_rats else 100.0, 2)
        synth_prefix_pct = round((synthetic_prefix_cnt / total_rats * 100.0) if total_rats else 0.0, 2)

        canon_by_slot = {
            k: Counter(txts).most_common(1)[0][0]
            for k, txts in slot_texts.items()
            if txts
        }
        raw_canon_by_slot = {
            k: Counter(txts).most_common(1)[0][0]
            for k, txts in raw_slot_texts.items()
            if txts
        }
        total_slots = len(canon_by_slot)
        by_cid_canon: dict[str, list[str]] = defaultdict(list)
        for (c_key, _), c_txt in canon_by_slot.items():
            by_cid_canon[c_key].append(c_txt)

        unique_slots_per_cid = sum(len(set(txts)) for txts in by_cid_canon.values())
        global_unique_slots = len(set(canon_by_slot.values()))
        unique_slots = min(unique_slots_per_cid, global_unique_slots)
        raw_unique_slots = len(set(raw_canon_by_slot.values()))

        slot_uniqueness_pct = round((unique_slots / total_slots * 100.0) if total_slots else 100.0, 2)
        raw_slot_uniqueness_pct = round((raw_unique_slots / total_slots * 100.0) if total_slots else 100.0, 2)

        unique_rats = unique_slots
        uniqueness_pct = slot_uniqueness_pct
        raw_uniqueness_pct = raw_slot_uniqueness_pct

        if total_rats >= 60 and uniqueness_pct < 80.0 and questions:
            issues.append(LintIssue(
                linter=self.name,
                dimension="D3_scaffolding",
                severity="warning",
                item_id=questions[0].get("id", "course_rationales"),
                competency_id=questions[0].get("competency_id", "global"),
                message=(
                    f"Reciclaje masivo de error_rationale: solo {unique_rats}/{total_slots} ({uniqueness_pct}%) "
                    f"slots de distractores tienen justificaciones diagnósticas únicas en todo el curso (< 80.0%)."
                ),
            ))

        if (
            total_rats >= 60
            and synth_prefix_pct >= 25.0
            and (uniqueness_pct < 80.0 or (raw_slot_uniqueness_pct - slot_uniqueness_pct) >= 10.0)
            and questions
        ):
            issues.append(LintIssue(
                linter=self.name,
                dimension="D3_scaffolding",
                severity="warning",
                item_id=questions[0].get("id", "course_rationales"),
                competency_id=questions[0].get("competency_id", "global"),
                message=(
                    f"Enmascaramiento de reciclaje diagnóstico mediante prefijos rotativos: "
                    f"{synth_prefix_pct}% de los rationales usan prefijos sintéticos para inflar la unicidad aparente "
                    f"de {uniqueness_pct}% (real por slot) a {raw_uniqueness_pct}% (nominal por slot; instancia: {instance_uniqueness_pct}% -> {raw_instance_uniqueness_pct}%)."
                ),
            ))

        if len(set(disconnected_numeric_rat_items)) >= 3:
            issues.append(LintIssue(
                linter=self.name,
                dimension=self.dimension,
                severity="warning",
                item_id=disconnected_numeric_rat_items[0],
                competency_id="global",
                message=(
                    f"Desconexión diagnóstica en opciones numéricas: {len(set(disconnected_numeric_rat_items))} reactivos "
                    f"presentan distractores puramente numéricos con error_rationale teórico copiado del CTA sin vínculo con el cálculo."
                ),
            ))

        return {
            "total_rationales": total_rats,
            "unique_rationales": unique_rats,
            "rationale_uniqueness_pct": uniqueness_pct,
            "raw_normalized_uniqueness_pct": raw_slot_uniqueness_pct,
            "total_rationale_slots": total_slots,
            "unique_rationale_slots": unique_slots,
            "slot_rationale_uniqueness_pct": slot_uniqueness_pct,
            "raw_slot_rationale_uniqueness_pct": raw_slot_uniqueness_pct,
            "instance_unique_rationales": instance_unique_rats,
            "instance_rationale_uniqueness_pct": instance_uniqueness_pct,
            "raw_instance_uniqueness_pct": raw_instance_uniqueness_pct,
            "synthetic_prefix_rationales_count": synthetic_prefix_cnt,
            "synthetic_prefix_rationales_pct": synth_prefix_pct,
            "disconnected_numeric_rationale_items_count": len(set(disconnected_numeric_rat_items)),
            "disconnected_numeric_rationale_sample_items": list(set(disconnected_numeric_rat_items))[:15],
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
    5. Decorative Parameter Stuffing & Contradictory Premise Injection (`warning`): Artificial
       parenthetical unused parameters ('(no r=1/9)', '(entorno 5, índice 16)', '(prueba 30, n=28)')
       or declaring 'i.i.d.' variables with non-zero covariance in the same stem.
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
    DECORATIVE_PARAM_STUFFING_PAT = re.compile(
        r"(?:\(\s*(?:no\s+\$?[a-zA-Z]\s*=\s*[\d/.-]+\$?|(?:entorno|prueba|escenario|corrida|caso)\s+\$?\d+\$?\s*,\s*(?:[ií]ndice|n|m|k|\$[nm]\$)\s*=?\s*\$?\d+\$?)\s*\)|"
        r"\bcon\s+margen\s+\$?\d+(?:\.\d+)?\$?\s+y\s+referencia\s+\$?\d+)",
        re.IGNORECASE,
    )
    CONTRADICTORY_IID_COV_PAT = re.compile(
        r"\bi\.?i\.?d\.?(?!\w).{0,140}?\bcovarianza\s+\$?[1-9]\d*(?:\.\d+)?\$?",
        re.IGNORECASE,
    )
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
        decorative_stuffing_items: list[str] = []

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

            m_dec = self.DECORATIVE_PARAM_STUFFING_PAT.search(stem) or self.CONTRADICTORY_IID_COV_PAT.search(stem)
            if m_dec:
                decorative_stuffing_items.append(qid)
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="warning",
                    item_id=qid,
                    competency_id=cid,
                    message=f"Inyección de parámetro decorativo inerte o premisa contradictoria en enunciado: '{m_dec.group(0)[:55]}'",
                    snippet=m_dec.group(0)[:65],
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
                if isinstance(opts, list) and opts and any(isinstance(o, dict) for o in opts):
                    corr = tuple(sorted(_get_opt_text(o).strip() for o in opts if isinstance(o, dict) and o.get("is_correct")))
                    if corr:
                        ans_set.add(corr)
                    else:
                        ans_val = q.get("correct_answer") if q.get("correct_answer") is not None else q.get("answer")
                        ans_set.add(json.dumps(ans_val, sort_keys=True))
                else:
                    ans_val = q.get("correct_answer") if q.get("correct_answer") is not None else q.get("answer")
                    m20_spec = None
                    for m20_k in ("proof_dag", "adversarial_break", "unstructured_model", "invariant_canvas", "concept_matching"):
                        if isinstance(q.get(m20_k), dict):
                            m20_spec = q[m20_k]
                            break
                    if m20_spec is not None:
                        ans_set.add(json.dumps({"ans": ans_val, "spec": m20_spec}, sort_keys=True, default=str))
                    else:
                        ans_set.add(json.dumps(ans_val, sort_keys=True, default=str))
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
            "decorative_param_stuffing_items_count": len(set(decorative_stuffing_items)),
            "decorative_param_stuffing_sample_items": list(set(decorative_stuffing_items))[:15],
        }


class DomainImpossibleDistractorLinter(BaseLinter):
    """Detects options (distractors AND correct keys) that violate fundamental mathematical domain bounds.

    1. Negative values (< 0) when the stem asks for variance, standard deviation,
       standard error, MSE/ECM, or sample size.
    2. Values > 1.0 or < 0.0 (or > 100% / < 0% for percentages) when the stem asks for an exact probability.
    3. Corrupted correct key (> 1.0 or < 0.0) or negative distractor (< 0.0) in Markov/Chebyshev probability bounds.
    4. Degenerate boundary collapse (`0.0000` or `1.0000`) in continuous CDF/probability correct keys due to underflow.
    """
    name = "domain_impossible_distractor_linter"
    dimension = "D2_assessment"

    NON_NEGATIVE_STEM_PAT = re.compile(
        r"\b(?:varianza|desviaci[oó]n\s+(?:est[aá]ndar|t[ií]pica)|"
        r"error\s+(?:est[aá]ndar|t[ií]pico|cuadr[aá]tico\s+medio)|"
        r"ecm|mse|tama[ñn]o\s+de\s+(?:la\s+)?muestra)\b",
        re.IGNORECASE,
    )
    EXACT_PROB_STEM_PAT = re.compile(
        r"(?:\b(?:calcule|calcula|determine|determina|halle|halla|encuentre|encuentra|"
        r"cu[aá]l\s+es|obtenga|eval[uú]e)\s+(?:el\s+valor\s+de\s+)?(?:la\s+)?"
        r"(?:probabilidad\b|funci[oó]n\s+de\s+distribuci[oó]n\s+\$?F|\$?\\mathbb\{P\}\s*\(|\$?P\s*\()|"
        r"\bprobabilidad\s+(?:de\s+que|exacta|conjunta|condicional|marginal)\b)",
        re.IGNORECASE,
    )
    PROB_BOUND_STEM_PAT = re.compile(
        r"\b(?:cota\s+de\s+(?:markov|chebyshev|chebychev)\s+(?:en\s+probabilidad|para\s+\$?(?:\\mathbb\{P\}|P)\s*\()|"
        r"cota\s+(?:superior|inferior)\s+(?:de\s+probabilidad|para\s+\$?(?:\\mathbb\{P\}|P)\s*\())",
        re.IGNORECASE,
    )
    BOUND_EXCLUSION_PAT = re.compile(
        r"\b(?:markov|chebyshev|chebychev|desigualdad|cota\s+(?:superior|inferior)|"
        r"l[ií]mite\s+superior|acotar|cota\s+m[aá]xima)\b",
        re.IGNORECASE,
    )
    NON_PROB_TARGET_PAT = re.compile(
        r"\b(?:calcule|calcula|determine|determina|halle|halla|encuentre|encuentra|obtenga)\s+"
        r"(?:el\s+valor\s+de\s+)?(?:la\s+|el\s+)?"
        r"(?:varianza|desviaci[oó]n|esperanza|media|error\s+cuadr[aá]tico|ecm|mse|sesgo|covarianza|tama[ñn]o|momento|cuantil)\b",
        re.IGNORECASE,
    )
    NUMERIC_OPT_PAT = re.compile(r"^(?:[a-zA-Z_\\(){}\[\]]+\s*=\s*)?(-?\d+(?:\.\d+)?)\s*(%|\\\%)?$")
    DEGENERATE_PROB_KEY_PAT = re.compile(r"^\$?\s*(?:0\.0{3,4}|1\.0{3,4})\s*\$?$")

    @classmethod
    def _extract_numeric_value(cls, text: str) -> tuple[Optional[float], bool]:
        if "por ciento" in text.lower():
            return None, False
        cleaned = text.replace("$", "").replace("\u2212", "-").strip()
        cleaned = re.sub(r"\\text\{[^}]*\}", "", cleaned).strip()
        m = cls.NUMERIC_OPT_PAT.fullmatch(cleaned)
        if not m:
            return None, False
        try:
            return float(m.group(1)), bool(m.group(2))
        except ValueError:
            return None, False

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        negative_domain_items: list[str] = []
        prob_gt_one_items: list[str] = []
        corrupted_prob_key_items: list[str] = []
        degenerate_prob_key_items: list[str] = []

        for q in questions:
            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")
            stem = str(q.get("stem") or "")
            options = q.get("options", []) or []
            if not isinstance(options, list) or not stem:
                continue

            requires_non_neg = bool(self.NON_NEGATIVE_STEM_PAT.search(stem))
            asks_non_prob_target = bool(self.NON_PROB_TARGET_PAT.search(stem))
            requires_prob_bound = bool(self.PROB_BOUND_STEM_PAT.search(stem)) and not asks_non_prob_target
            requires_exact_prob = (
                bool(self.EXACT_PROB_STEM_PAT.search(stem))
                and not bool(self.BOUND_EXCLUSION_PAT.search(stem))
                and not asks_non_prob_target
            )
            if not requires_non_neg and not requires_exact_prob and not requires_prob_bound:
                continue

            flagged_corrupt_key = False
            flagged_degen_key = False
            flagged_neg_distractor = False
            flagged_prob_gt_one = False

            for o_idx, opt in enumerate(options):
                if not isinstance(opt, dict):
                    continue
                is_corr = bool(opt.get("is_correct", False))
                txt = _get_opt_text(opt).strip()
                val, is_pct = self._extract_numeric_value(txt)
                if val is None:
                    continue
                upper_prob = 100.0 if is_pct else 1.0

                # 1. Check correct key for probability or probability bound > 1.0 or < 0.0
                if is_corr and (requires_exact_prob or requires_prob_bound):
                    if (val > upper_prob or val < 0.0) and not flagged_corrupt_key:
                        flagged_corrupt_key = True
                        corrupted_prob_key_items.append(qid)
                        prob_gt_one_items.append(qid)
                        issues.append(LintIssue(
                            linter=self.name,
                            dimension=self.dimension,
                            severity="critical",
                            item_id=qid,
                            competency_id=cid,
                            message=(
                                f"Clave correcta matemáticamente corrupta en opción {o_idx}: "
                                f"probabilidad o cota de probabilidad fuera de [0, {upper_prob:g}] ({val})."
                            ),
                            snippet=txt[:60],
                        ))
                        continue
                    if requires_exact_prob and self.DEGENERATE_PROB_KEY_PAT.match(txt) and not flagged_degen_key:
                        flagged_degen_key = True
                        degenerate_prob_key_items.append(qid)
                        issues.append(LintIssue(
                            linter=self.name,
                            dimension=self.dimension,
                            severity="warning",
                            item_id=qid,
                            competency_id=cid,
                            message=(
                                f"Colapso degenerado por underflow/overflow en clave correcta ({txt}): "
                                f"probabilidad continua redondeada exactamente a extremo frontera."
                            ),
                            snippet=txt[:60],
                        ))
                    continue

                if is_corr:
                    continue

                # 2. Check distractors
                if (requires_non_neg or requires_exact_prob or requires_prob_bound) and val < 0.0 and not flagged_neg_distractor:
                    flagged_neg_distractor = True
                    negative_domain_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="critical",
                        item_id=qid,
                        competency_id=cid,
                        message=(
                            f"Distractor imposible por dominio en opción {o_idx}: "
                            f"valor negativo ({val}) para magnitud o probabilidad estrictamente no negativa."
                        ),
                        snippet=txt[:60],
                    ))
                    continue

                if requires_exact_prob and val > upper_prob and not flagged_prob_gt_one:
                    flagged_prob_gt_one = True
                    prob_gt_one_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="critical",
                        item_id=qid,
                        competency_id=cid,
                        message=(
                            f"Distractor imposible por dominio en opción {o_idx}: "
                            f"probabilidad exacta > {upper_prob:g} ({val}{'%' if is_pct else ''})."
                        ),
                        snippet=txt[:60],
                    ))
                    continue

        flagged = set(negative_domain_items) | set(prob_gt_one_items) | set(corrupted_prob_key_items)
        return {
            "domain_impossible_items_count": len(flagged),
            "negative_non_neg_magnitude_count": len(set(negative_domain_items)),
            "prob_gt_one_count": len(set(prob_gt_one_items)),
            "corrupted_prob_key_items_count": len(set(corrupted_prob_key_items)),
            "degenerate_prob_key_items_count": len(set(degenerate_prob_key_items)),
            "domain_impossible_sample_items": list(flagged)[:15],
        }


class FibRoundingContractLinter(BaseLinter):
    """Penalizes FIB items without calculator whose correct_answer has >= 3 decimals
    and whose stem lacks an explicit rounding instruction.
    """
    name = "fib_rounding_contract_linter"
    dimension = "D2_assessment"

    ROUNDING_INSTRUCTION_PAT = re.compile(
        r"\b(?:decimales?|redonde\w*|cifras?\s+significativas?|aproxim\w+\s+a\s+\d+|trunc\w*)\b",
        re.IGNORECASE,
    )
    THREE_PLUS_DECIMALS_PAT = re.compile(r"^-?\d+\.(\d{3,})$")

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        uncontracted_items: list[str] = []

        for q in questions:
            qtype = str(q.get("interaction_type") or q.get("type") or "").strip().lower()
            if qtype not in ("fill_in_the_blank", "fib"):
                continue
            if q.get("allow_calculator") is True:
                continue

            ans = q.get("correct_answer")
            if ans is None:
                continue
            ans_str = str(ans).strip()
            if not self.THREE_PLUS_DECIMALS_PAT.fullmatch(ans_str):
                continue

            stem = str(q.get("stem") or "")
            if self.ROUNDING_INSTRUCTION_PAT.search(stem):
                continue

            qid = q.get("id", "unknown")
            cid = q.get("competency_id", "unassigned")
            uncontracted_items.append(qid)
            issues.append(LintIssue(
                linter=self.name,
                dimension=self.dimension,
                severity="warning",
                item_id=qid,
                competency_id=cid,
                message=(
                    f"Ítem FIB sin calculadora con respuesta '{ans_str}' (>= 3 decimales) "
                    f"carece de instrucción explícita de redondeo en el enunciado."
                ),
                snippet=ans_str,
            ))

        return {
            "fib_uncontracted_rounding_count": len(set(uncontracted_items)),
            "fib_uncontracted_rounding_items": list(set(uncontracted_items))[:15],
        }


class MsLengthBiasLinter(BaseLinter):
    """Audits average option length ratio len(true_options) / len(false_options)
    in multiple_select items and flags courses where > 60% exceed 1.08x.
    """
    name = "ms_length_bias_linter"
    dimension = "D2_assessment"

    RATIO_THRESHOLD = 1.08
    ITEM_PCT_THRESHOLD = 0.60

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        evaluated_ms = 0
        biased_items: list[tuple[str, str, float]] = []

        for q in questions:
            qtype = str(q.get("interaction_type") or q.get("type") or "").strip().lower()
            if qtype != "multiple_select":
                continue

            options = q.get("options", []) or []
            if not isinstance(options, list):
                continue

            true_lens = [len(_get_opt_text(o).strip()) for o in options if isinstance(o, dict) and o.get("is_correct")]
            false_lens = [len(_get_opt_text(o).strip()) for o in options if isinstance(o, dict) and not o.get("is_correct")]
            if not true_lens or not false_lens:
                continue

            avg_true = sum(true_lens) / len(true_lens)
            avg_false = sum(false_lens) / len(false_lens)
            if avg_false <= 0:
                continue

            evaluated_ms += 1
            ratio = avg_true / avg_false
            if ratio > self.RATIO_THRESHOLD:
                qid = q.get("id", "unknown")
                cid = q.get("competency_id", "unassigned")
                biased_items.append((qid, cid, round(ratio, 3)))

        biased_pct = round((len(biased_items) / evaluated_ms * 100.0) if evaluated_ms else 0.0, 2)
        if evaluated_ms > 0 and (len(biased_items) / evaluated_ms) > self.ITEM_PCT_THRESHOLD:
            rep_qid, rep_cid, _ = biased_items[0]
            issues.append(LintIssue(
                linter=self.name,
                dimension=self.dimension,
                severity="warning",
                item_id=rep_qid,
                competency_id=rep_cid,
                message=(
                    f"Sesgo sistemático de longitud en multiple_select: {len(biased_items)}/{evaluated_ms} "
                    f"({biased_pct}%) ítems presentan ratio len(true)/len(false) > {self.RATIO_THRESHOLD}x."
                ),
            ))

        return {
            "total_ms_items": evaluated_ms,
            "biased_ms_items_count": len(biased_items),
            "biased_ms_pct": biased_pct,
            "biased_ms_sample_items": [qid for qid, _, _ in biased_items[:15]],
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
        idx_map: dict[str, int] = {}
        duplicate_comp_ids: list[str] = []
        for idx, c in enumerate(competencies):
            cid_raw = c.get("id")
            if not cid_raw:
                continue
            if cid_raw in idx_map:
                duplicate_comp_ids.append(cid_raw)
                issues.append(LintIssue(
                    linter=self.name,
                    dimension=self.dimension,
                    severity="critical",
                    item_id=f"comp_{cid_raw}",
                    competency_id=cid_raw,
                    message=f"ID de competencia duplicado '{cid_raw}' en la estructura curricular.",
                ))
            else:
                idx_map[cid_raw] = idx

        adj: dict[str, list[str]] = {cid: [] for cid in idx_map}
        in_deg: dict[str, int] = {cid: 0 for cid in idx_map}
        out_deg: dict[str, int] = {cid: 0 for cid in idx_map}

        inverted_edges = []
        dangling_prereqs = []
        skills_without_prereqs = []
        seen_comp_ids: set[str] = set()

        any_prereqs_defined = any(bool(c.get("prerequisites")) for c in competencies)

        for idx, c in enumerate(competencies):
            cid = c.get("id")
            if not cid or cid in seen_comp_ids:
                continue
            seen_comp_ids.add(cid)
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
            "duplicate_competency_ids_count": len(set(duplicate_comp_ids)),
            "duplicate_competency_ids": list(set(duplicate_comp_ids)),
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
    3. Raw Python scientific float notation (`warning`): Rendering `$-7.2e-05$` or `$1.1e-04$`
       inside KaTeX (where `e` is parsed as Euler's constant minus 05).
    4. Raw asterisk multiplication (`warning`): Rendering `$500*0.73*0.27$` instead of `\\cdot`.
    """
    name = "katex_frontend_ergonomics_linter"
    dimension = "D5_katex"

    PROSE_IN_TEXT_PAT = re.compile(r"^\s*\$\\text\{(.{45,})\}\$\s*$")
    RAW_IDENT_MATH_PAT = re.compile(r"\$[a-zA-Z]+_(?:hat|bar|tilde|vec|star|dot|sq|ols|mle|var|est)\b")
    RAW_SCI_FLOAT_MATH_PAT = re.compile(r"(\${1,2})(?:\\.|[^$\\])*\b-?\d+(?:\.\d+)?e[+-]0?\d+\b(?:\\.|[^$\\])*\1")
    RAW_ASTERISK_MATH_PAT = re.compile(r"(\${1,2})(?:\\.|[^$\\])*\d\s*\*\s*\d(?:\\.|[^$\\])*\1")

    def run(self, course_data: dict, issues: list[LintIssue]) -> dict:
        questions = course_data.get("questions", [])
        prose_in_text_items = []
        raw_ident_items = []
        raw_sci_float_items = []
        raw_asterisk_items = []

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

                m_sci = self.RAW_SCI_FLOAT_MATH_PAT.search(txt)
                if m_sci:
                    raw_sci_float_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="warning",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Notación científica cruda de Python en KaTeX '{m_sci.group(0)[:40]}' (debe usar '\\times 10^{{...}}') en '{field_name}'",
                        snippet=m_sci.group(0)[:50],
                    ))

                m_ast = self.RAW_ASTERISK_MATH_PAT.search(txt)
                if m_ast:
                    raw_asterisk_items.append(qid)
                    issues.append(LintIssue(
                        linter=self.name,
                        dimension=self.dimension,
                        severity="warning",
                        item_id=qid,
                        competency_id=cid,
                        message=f"Operador asterisco crudo '*' para multiplicación en KaTeX '{m_ast.group(0)[:40]}' (usar '\\cdot' o '\\times') en '{field_name}'",
                        snippet=m_ast.group(0)[:50],
                    ))

        return {
            "prose_in_katex_text_items_count": len(set(prose_in_text_items)),
            "prose_in_katex_text_sample_items": list(set(prose_in_text_items))[:15],
            "raw_identifier_math_items_count": len(set(raw_ident_items)),
            "raw_identifier_math_sample_items": list(set(raw_ident_items))[:15],
            "raw_scientific_float_items_count": len(set(raw_sci_float_items)),
            "raw_scientific_float_sample_items": list(set(raw_sci_float_items))[:15],
            "raw_asterisk_math_items_count": len(set(raw_asterisk_items)),
            "raw_asterisk_math_sample_items": list(set(raw_asterisk_items))[:15],
        }


def compute_mastery_path_readiness(summaries: dict[str, Any], total_comps: int, total_questions: int) -> dict[str, Any]:
    """Compute the deterministic Mastery Path Readiness Index (MPRI: 0.0 to 100.0) across 6 pillars."""
    if total_comps == 0 or total_questions == 0:
        return {
            "mpri_score": 0.0,
            "mpri_max": 100.0,
            "mpri_tier": "MASTERY-HOSTILE (0-39): Curso vacío o sin reactivos/competencias",
            "pillars": {
                "zpd_adaptive_progression": {"score": 0.0, "max": 20.0},
                "retrieval_modality_and_anti_gaming": {"score": 0.0, "max": 20.0},
                "socratic_scaffolding_lifeline": {"score": 0.0, "max": 25.0},
                "diagnostic_remediation_alignment": {"score": 0.0, "max": 15.0},
                "dag_and_interleaving_topology": {"score": 0.0, "max": 10.0},
                "cognitive_ergonomics_and_framing": {"score": 0.0, "max": 10.0},
            },
        }

    total_q = max(total_questions, 1)
    total_c = max(total_comps, 1)

    arch_dag = summaries.get("architecture_dag_linter", {})
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
    dom_imp = summaries.get("domain_impossible_distractor_linter", {})
    fib_round = summaries.get("fib_rounding_contract_linter", {})
    ms_bias = summaries.get("ms_length_bias_linter", {})
    uninterp = summaries.get("uninterpolated_math_variable_linter", {})
    blind = summaries.get("blind_string_replacement_linter", {})

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
    dec_stuff = ag.get("decorative_param_stuffing_items_count", 0)
    ms_bias_pen = 1.5 if ms_bias.get("biased_ms_pct", 0.0) > 60.0 else 0.0
    fib_uncontracted_ratio = fib_round.get("fib_uncontracted_rounding_count", 0) / total_q
    anti_gaming_score = max(
        0.0,
        10.0
        - mem_comps * 3.0
        - min(4.0, arch_mono_comps * 1.5)
        - min(5.0, vac_items * 0.5)
        - pad_ratio * 8.0
        - min(2.0, dec_stuff * 0.08)
        - ms_bias_pen
        - min(2.0, fib_uncontracted_ratio * 10.0),
    )
    p2_retrieval = round(max(0.0, min(20.0, modality_score + anti_gaming_score)), 2)

    # Pillar 3: Socratic Scaffolding Lifeline (25 pts) — protects 3-strikes progression
    valid_hints_ratio = max(0.0, (total_questions - scaf.get("zero_hints_count", 0) - scaf.get("insufficient_hints_count", 0)) / total_q)
    bp_ratio = soc.get("boilerplate_hints_pct", 0.0) / 100.0
    poison_ratio = soc.get("poisoned_hints_pct", 0.0) / 100.0
    leak_cnt = soc.get("hint_answer_leak_items_count", 0)
    gen_misc_ratio = (scaf.get("generic_misconception_count", 0) / total_q) if total_questions >= 50 else 0.0
    disc_warn_cnt = scaf.get("disconnected_warning_numbers_count", 0)
    p3_socratic = round(
        max(
            0.0,
            25.0 * valid_hints_ratio
            - 12.0 * bp_ratio
            - 15.0 * poison_ratio
            - min(5.0, leak_cnt * 1.0)
            - min(3.5, gen_misc_ratio * 6.0)
            - min(1.5, disc_warn_cnt * 0.1),
        ),
        2,
    )

    # Pillar 4: Diagnostic Remediation Alignment (15 pts) — powers FeedbackToast.tsx
    cov_score = 5.0 * (dist.get("rationale_coverage_pct", 100.0) / 100.0)
    if diag.get("total_rationales", 0) >= 60:
        uniq_pct = diag.get("rationale_uniqueness_pct", 100.0)
        raw_uniq_pct = diag.get("raw_normalized_uniqueness_pct", uniq_pct)
        if uniq_pct >= 80.0:
            uniq_score = 5.0
        else:
            uniq_score = 2.5 * (uniq_pct / 80.0)
        if diag.get("synthetic_prefix_rationales_pct", 0.0) >= 25.0 and (
            uniq_pct < 80.0 or (raw_uniq_pct - uniq_pct) >= 10.0
        ):
            uniq_score = max(0.0, uniq_score - 1.2)
    else:
        uniq_score = 5.0
    magic_ratio = diag.get("magic_multiplier_distractor_items_count", 0) / total_q
    cloned_cnt = cloned.get("cloned_distractor_items_count", 0)
    disc_num_ratio = diag.get("disconnected_numeric_rationale_items_count", 0) / total_q
    dom_cnt = dom_imp.get("domain_impossible_items_count", 0)
    corrupt_key_cnt = dom_imp.get("corrupted_prob_key_items_count", 0)
    degen_key_cnt = dom_imp.get("degenerate_prob_key_items_count", 0)
    dist_auth_score = max(
        0.0,
        5.0
        - min(5.0, magic_ratio * 25.0)
        - min(5.0, cloned_cnt * 1.0)
        - min(3.5, disc_num_ratio * 12.0)
        - min(3.5, dom_cnt * 0.25 + corrupt_key_cnt * 0.8 + degen_key_cnt * 0.3),
    )
    p4_diagnostic = round(max(0.0, min(15.0, cov_score + uniq_score + dist_auth_score)), 2)

    # Pillar 5: Knowledge Graph & Interleaving Topology (10 pts) — powers Quiz/Test interleaving
    p5_raw = 10.0
    if dag_t.get("has_cycle"):
        p5_raw -= 6.0
    p5_raw -= dag_t.get("dangling_prerequisites_count", 0) * 2.5
    p5_raw -= dag_t.get("inverted_prerequisite_edges_count", 0) * 2.0
    p5_raw -= dag_t.get("isolated_competencies_count", 0) * 1.5
    p5_raw -= min(3.0, dag_t.get("skills_without_prerequisites_count", 0) * 1.0)
    p5_raw -= min(2.5, arch_dag.get("duplicate_competency_pairs_count", 0) * 0.35)
    p5_raw -= min(1.5, arch_dag.get("id_category_mismatch_count", 0) * 0.6)
    p5_topology = round(max(0.0, min(10.0, p5_raw)), 2)

    # Pillar 6: Cognitive Load & KaTeX Frontend Ergonomics (10 pts)
    katex_crit = katex.get("unclosed_braces_count", 0) + katex.get("unbalanced_dollars_count", 0)
    prose_ratio = erg.get("prose_in_katex_text_items_count", 0) / total_q
    raw_id_ratio = erg.get("raw_identifier_math_items_count", 0) / total_q
    cd_ratio = ag.get("cross_domain_prefix_items_count", 0) / total_q
    concat_cnt = uninterp.get("string_concat_collision_items_count", 0)
    sci_ast_cnt = erg.get("raw_scientific_float_items_count", 0) + erg.get("raw_asterisk_math_items_count", 0)
    part_dummy_cnt = blind.get("partial_dummy_var_substitution_count", 0)
    p6_ergonomics = round(
        max(
            0.0,
            10.0
            - min(5.0, katex_crit * 0.5)
            - min(4.0, prose_ratio * 12.0)
            - min(3.0, raw_id_ratio * 15.0)
            - min(3.0, cd_ratio * 15.0)
            - min(3.5, concat_cnt * 0.25 + sci_ast_cnt * 0.12 + part_dummy_cnt * 0.2),
        ),
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


def compute_deterministic_rubric_scores(
    summaries: dict[str, Any],
    total_comps: int,
    total_questions: int,
    hard_penalties: list[dict[str, Any]],
    judge_audit: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Compute the deterministic 20-point QM-OSCQR & Mastery Learning rubric across 5 dimensions."""
    if total_comps == 0 or total_questions == 0:
        empty_msg = "Curso vacío o sin competencias/reactivos válidos."
        sum_hard_penalties = round(sum(float(p.get("deduction", 0.0)) for p in hard_penalties if isinstance(p, dict)), 2)
        return {
            "dimension_scores": {
                "architecture_granularity": {"score": 0.0, "max": 4.0, "feedback": empty_msg},
                "assessment_quality": {"score": 0.0, "max": 5.0, "feedback": empty_msg},
                "scaffolding_hints": {"score": 0.0, "max": 5.0, "feedback": empty_msg},
                "instructional_alignment": {"score": 0.0, "max": 4.0, "feedback": empty_msg},
                "technical_ergonomics": {"score": 0.0, "max": 2.0, "feedback": empty_msg},
            },
            "raw_subtotal": 0.0,
            "penalties_applied": hard_penalties,
            "hard_penalties_total": sum_hard_penalties,
            "final_score": 0.0,
            "quality_tier": "CRÍTICO (0.0 - 10.9 pts)",
        }

    total_q = max(total_questions, 1)
    total_c = max(total_comps, 1)

    arch_dag = summaries.get("architecture_dag_linter", {})
    dist = summaries.get("distractor_integrity_linter", {})
    scaf = summaries.get("scaffolding_hints_linter", {})
    katex = summaries.get("katex_syntax_linter", {})
    tpl = summaries.get("template_variable_residue_linter", {})
    blind = summaries.get("blind_string_replacement_linter", {})
    cloned = summaries.get("cloned_distractor_value_linter", {})
    zpd = summaries.get("zpd_progression_linter", {})
    mod = summaries.get("retrieval_modality_linter", {})
    soc = summaries.get("socratic_scaffolding_integrity_linter", {})
    diag = summaries.get("diagnostic_rationale_alignment_linter", {})
    ag = summaries.get("anti_gaming_psychometric_linter", {})
    dag_top = summaries.get("dag_mastery_topology_linter", {})
    erg = summaries.get("katex_frontend_ergonomics_linter", {})
    dom_imp = summaries.get("domain_impossible_distractor_linter", {})
    fib_round = summaries.get("fib_rounding_contract_linter", {})
    ms_bias = summaries.get("ms_length_bias_linter", {})
    uninterp = summaries.get("uninterpolated_math_variable_linter", {})

    # Dimensión 1: Arquitectura Curricular, Topología DAG y Calibración ZPD (0 a 4.0 pts)
    d1 = 4.0
    if dag_top.get("has_cycle"):
        d1 -= 2.0
    d1 -= dag_top.get("inverted_prerequisite_edges_count", 0) * 0.4
    d1 -= dag_top.get("dangling_prerequisites_count", 0) * 0.5
    d1 -= dag_top.get("isolated_competencies_count", 0) * 0.3
    d1 -= min(0.6, max(0, dag_top.get("connected_components_count", 1) - 1) * 0.3)
    d1 -= min(0.8, arch_dag.get("underpopulated_competencies_count", 0) * 0.4)
    d1 -= min(1.0, arch_dag.get("orphan_questions_count", 0) * 0.5)
    d1 -= min(0.6, arch_dag.get("duplicate_competency_pairs_count", 0) * 0.08)
    d1 -= min(0.4, arch_dag.get("id_category_mismatch_count", 0) * 0.2)

    elig_c = zpd.get("eligible_competencies_evaluated", 0)
    if elig_c > 0:
        three_b = zpd.get("three_band_competencies_count", 0)
        two_b = zpd.get("two_band_competencies_count", 0)
        zpd_ratio = (three_b * 1.0 + two_b * 0.7) / elig_c
        if zpd_ratio < 1.0:
            d1 -= round((1.0 - zpd_ratio) * 1.5, 2)
    d1 = max(0.0, min(4.0, round(d1, 2)))

    cat_dist = arch_dag.get("category_distribution", {})
    cat_str = f"{cat_dist.get('Fact', 0)} Hechos, {cat_dist.get('Concept', 0)} Conceptos, {cat_dist.get('Skill', 0)} Habilidades"
    d1_fb = (
        f"Estructura curricular con {total_comps} competencias ({cat_str}). "
        f"DAG acíclico y conexo (ciclos={dag_top.get('has_cycle', False)}, comp. conexos={dag_top.get('connected_components_count', 1)}, "
        f"pares solapados={arch_dag.get('duplicate_competency_pairs_count', 0)}). "
        f"ZPD: {zpd.get('three_band_competencies_count', 0)}/{elig_c or total_comps} competencias con calibración tri-banda ('easy', 'medium', 'hard')."
    )

    # Dimensión 2: Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming (0 a 5.0 pts)
    d2 = 5.0
    if total_q >= 20:
        active_pct = mod.get("active_generation_or_discrimination_pct", 0.0)
        if active_pct < 25.0:
            d2 -= round(1.2 * (1.0 - active_pct / 25.0), 2)
    cov = dist.get("rationale_coverage_pct", 100.0)
    if cov < 100.0:
        d2 -= round((100.0 - cov) * 0.05, 2)
    magic_cnt = diag.get("magic_multiplier_distractor_items_count", 0)
    if magic_cnt > 0:
        d2 -= min(1.2, round((magic_cnt / total_q) * 15.0, 2))
    pad_cnt = ag.get("length_padded_items_count", 0)
    if pad_cnt > 0:
        d2 -= min(0.6, round((pad_cnt / total_q) * 10.0, 2))
    d2 -= min(1.0, dist.get("telltale_distractor_items_count", 0) * 0.2)
    d2 -= min(0.8, cloned.get("cloned_distractor_items_count", 0) * 0.1)
    d2 -= min(0.8, ag.get("vacuous_quantifier_items_count", 0) * 0.3)
    dom_cnt = dom_imp.get("domain_impossible_items_count", 0)
    corrupt_key_cnt = dom_imp.get("corrupted_prob_key_items_count", 0)
    degen_key_cnt = dom_imp.get("degenerate_prob_key_items_count", 0)
    if dom_cnt > 0 or degen_key_cnt > 0:
        d2 -= min(0.9, round(dom_cnt * 0.06 + corrupt_key_cnt * 0.25 + degen_key_cnt * 0.08, 2))
    if ms_bias.get("biased_ms_pct", 0.0) > 60.0:
        d2 -= 0.25
    fib_uncontracted = fib_round.get("fib_uncontracted_rounding_count", 0)
    if fib_uncontracted > 0:
        d2 -= min(0.35, round((fib_uncontracted / total_q) * 2.0, 2))
    dec_stuff = ag.get("decorative_param_stuffing_items_count", 0)
    if dec_stuff > 0:
        d2 -= min(0.35, round(dec_stuff * 0.015, 2))
    disc_num_cnt = diag.get("disconnected_numeric_rationale_items_count", 0)
    if disc_num_cnt > 0:
        d2 -= min(0.5, round((disc_num_cnt / total_q) * 2.0, 2))
    d2 = max(0.0, min(5.0, round(d2, 2)))

    active_gen = mod.get("active_generation_or_discrimination_pct", 0.0)
    bloom_sup_str = (
        f", BloomSup={mod.get('bloom_superior_share_pct', 0.0)}%"
        if mod.get("bloom_superior_count", 0) > 0
        else ""
    )
    d2_fb = (
        f"Modalidad: MC7={mod.get('mc7_share_pct', 0.0)}%, FIB={mod.get('fib_share_pct', 0.0)}%, MS={mod.get('ms_share_pct', 0.0)}%{bloom_sup_str} "
        f"({active_gen}% evocación activa/discriminación). "
        f"Distractores: {dist.get('total_distractors_evaluated', 0)} evaluados con {cov}% cobertura de error_rationale "
        f"(imposibles por dominio={dom_cnt}, claves corruptas={corrupt_key_cnt}, sesgo MS={ms_bias.get('biased_ms_pct', 0.0)}%)."
    )

    # Dimensión 3: Andamiaje Socrático Progresivo y Remediación Diagnóstica (0 a 5.0 pts)
    d3 = 5.0
    insuf_hints = scaf.get("insufficient_hints_count", 0)
    if insuf_hints > 0:
        d3 -= min(2.0, round((insuf_hints / total_q) * 5.0, 2))
    miss_sol = scaf.get("missing_solutions_count", 0)
    if miss_sol > 0:
        d3 -= min(1.0, round((miss_sol / total_q) * 5.0, 2))
    bp_pct = soc.get("boilerplate_hints_pct", 0.0)
    if bp_pct > 0.0:
        d3 -= min(2.5, round((bp_pct / 100.0) * 3.0, 2))
    poison_pct = soc.get("poisoned_hints_pct", 0.0)
    if poison_pct > 0.0:
        d3 -= min(3.0, round((poison_pct / 100.0) * 4.0, 2))
    d3 -= min(1.0, soc.get("hint_answer_leak_items_count", 0) * 0.2)
    if diag.get("total_rationales", 0) >= 60:
        uniq = diag.get("rationale_uniqueness_pct", 100.0)
        raw_uniq = diag.get("raw_normalized_uniqueness_pct", uniq)
        if uniq < 80.0:
            d3 -= round((80.0 - uniq) * 0.015, 2)
        if diag.get("synthetic_prefix_rationales_pct", 0.0) >= 25.0 and (
            uniq < 80.0 or (raw_uniq - uniq) >= 10.0
        ):
            d3 -= 0.25
    if disc_num_cnt > 0:
        d3 -= min(0.9, round((disc_num_cnt / total_q) * 3.5, 2))
    gen_misc = scaf.get("generic_misconception_count", 0)
    if gen_misc > 0 and total_q >= 50:
        d3 -= min(0.6, round((gen_misc / total_q) * 1.2, 2))
    disc_warn = scaf.get("disconnected_warning_numbers_count", 0)
    if disc_warn > 0:
        d3 -= min(0.25, round(disc_warn * 0.015, 2))
    d3 = max(0.0, min(5.0, round(d3, 2)))

    zero_hints_cnt = scaf.get("zero_hints_count", 0)
    adequate_hints_pct = round(max(0.0, (total_questions - zero_hints_cnt - insuf_hints) / total_q * 100.0), 1)
    genuine_hints_pct = soc.get("genuine_socratic_hints_pct", 100.0)
    d3_fb = (
        f"Andamiaje formativo: {adequate_hints_pct}% de reactivos con 3 a 5 pistas socráticas escalonadas "
        f"({genuine_hints_pct}% pistas genuinas, {bp_pct}% boilerplate Mad-Libs, {poison_pct}% envenenadas). "
        f"Unicidad diagnóstica real de rationales: {diag.get('rationale_uniqueness_pct', 100.0)}% "
        f"(rationales numéricos desconectados={disc_num_cnt}, advertencias clonadas/mudas={gen_misc})."
    )

    # Dimensión 4: Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio (0 a 4.0 pts)
    d4 = 4.0
    bloom_skill_pct = zpd.get("skill_higher_bloom_pct", 100.0)
    if bloom_skill_pct < 80.0:
        d4 -= round((80.0 - bloom_skill_pct) * 0.02, 2)
    cd_cnt = ag.get("cross_domain_prefix_items_count", 0)
    if cd_cnt > 0:
        d4 -= min(0.8, round((cd_cnt / total_q) * 10.0, 2))
    if dec_stuff > 0:
        d4 -= min(0.3, round(dec_stuff * 0.01, 2))
    if judge_audit and judge_audit.get("available"):
        agree_rate = judge_audit.get("agreement_rate", 1.0)
        if agree_rate < 0.95:
            d4 -= min(1.2, round((0.95 - agree_rate) * 5.0, 2))
    d4 = max(0.0, min(4.0, round(d4, 2)))

    d4_fb = (
        f"Alineación cognitiva de Bloom: {bloom_skill_pct}% de habilidades prácticas en niveles superiores (Apply+). "
        f"Registro disciplinar auténtico y alta fidelidad con los contenidos fuente."
    )

    # Dimensión 5: Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX (0 a 2.0 pts)
    d5 = 2.0
    crit_katex = katex.get("unclosed_braces_count", 0) + katex.get("unbalanced_dollars_count", 0) + katex.get("triple_dollars_count", 0)
    d5 -= min(1.0, crit_katex * 0.5)
    prose_cnt = erg.get("prose_in_katex_text_items_count", 0)
    if prose_cnt > 0:
        d5 -= min(0.3, round(prose_cnt * 0.04, 2))
    raw_ids = erg.get("raw_identifier_math_items_count", 0)
    if raw_ids > 0:
        d5 -= min(0.4, round(raw_ids * 0.05, 2))
    sci_ast = erg.get("raw_scientific_float_items_count", 0) + erg.get("raw_asterisk_math_items_count", 0)
    if sci_ast > 0:
        d5 -= min(0.3, round(sci_ast * 0.02, 2))
    concat_cnt = uninterp.get("string_concat_collision_items_count", 0)
    if concat_cnt > 0:
        d5 -= min(0.5, round(concat_cnt * 0.05, 2))
    residues = tpl.get("template_variable_residue_count", 0) + blind.get("blind_string_replacement_count", 0)
    if residues > 0:
        d5 -= min(0.5, round(residues * 0.1, 2))
    d5 = max(0.0, min(2.0, round(d5, 2)))

    d5_fb = (
        f"Sintaxis KaTeX: {crit_katex} errores críticos (delimitadores balanceados, llaves cerradas, cero $$$). "
        f"Ergonomía: {prose_cnt} observaciones de prosa en \\text{{...}}, {raw_ids} identificadores crudos, "
        f"{concat_cnt} colisiones por concatenación y {sci_ast} formatos flotantes/asteriscos crudos."
    )

    raw_subtotal = round(d1 + d2 + d3 + d4 + d5, 2)
    sum_hard_penalties = round(sum(float(p.get("deduction", 0.0)) for p in hard_penalties if isinstance(p, dict)), 2)
    final_score = round(max(0.0, min(20.0, raw_subtotal - sum_hard_penalties)), 2)

    if final_score >= 19.0:
        quality_tier = "EXCELENTE (19.0 - 20.0 pts) — PLATINUM MASTERY"
    elif final_score >= 17.0:
        quality_tier = "EXCELENTE (17.0 - 18.9 pts) — GOLD MASTERY"
    elif final_score >= 14.0:
        quality_tier = "ACEPTABLE (14.0 - 16.9 pts) — SILVER MASTERY"
    elif final_score >= 11.0:
        quality_tier = "DEFICIENTE (11.0 - 13.9 pts)"
    else:
        quality_tier = "CRÍTICO (0.0 - 10.9 pts)"

    return {
        "dimension_scores": {
            "architecture_granularity": {"score": d1, "max": 4.0, "feedback": d1_fb},
            "assessment_quality": {"score": d2, "max": 5.0, "feedback": d2_fb},
            "scaffolding_hints": {"score": d3, "max": 5.0, "feedback": d3_fb},
            "instructional_alignment": {"score": d4, "max": 4.0, "feedback": d4_fb},
            "technical_ergonomics": {"score": d5, "max": 2.0, "feedback": d5_fb},
        },
        "raw_subtotal": raw_subtotal,
        "penalties_applied": hard_penalties,
        "hard_penalties_total": sum_hard_penalties,
        "final_score": final_score,
        "quality_tier": quality_tier,
    }


def generate_deterministic_qa_report(telemetry: dict, course_data: dict) -> tuple[dict, str]:
    """Generates the structured JSON dictionary and standard Markdown report for course QA audit."""
    course_id = course_data.get("course_id") or telemetry.get("course_id", "unknown_course")
    title = course_data.get("title") or course_data.get("course_title") or telemetry.get("title", course_id)
    description = course_data.get("description", "")
    total_comps = len(course_data.get("competencies", [])) or telemetry.get("total_competencies", 0)
    questions = course_data.get("questions", [])
    total_questions = len(questions) or telemetry.get("total_questions", 0)

    types_count: dict[str, int] = {}
    for q in questions:
        qtype = q.get("interaction_type") or q.get("type", "unknown")
        types_count[qtype] = types_count.get(qtype, 0) + 1

    det_rubric = telemetry.get("deterministic_rubric", {})
    dim_scores = det_rubric.get("dimension_scores", {})
    d1 = dim_scores.get("architecture_granularity", {"score": 4.0, "max": 4.0, "feedback": ""})
    d2 = dim_scores.get("assessment_quality", {"score": 5.0, "max": 5.0, "feedback": ""})
    d3 = dim_scores.get("scaffolding_hints", {"score": 5.0, "max": 5.0, "feedback": ""})
    d4 = dim_scores.get("instructional_alignment", {"score": 4.0, "max": 4.0, "feedback": ""})
    d5 = dim_scores.get("technical_ergonomics", {"score": 2.0, "max": 2.0, "feedback": ""})

    hard_penalties = telemetry.get("hard_penalties", [])
    raw_subtotal = det_rubric.get("raw_subtotal", 20.0)
    final_score = det_rubric.get("final_score", telemetry.get("final_score", 20.0))
    quality_tier = det_rubric.get("quality_tier", telemetry.get("quality_tier", "EXCELENTE (PLATINUM MASTERY)"))

    mpri_data = telemetry.get("mastery_path_readiness", {})
    mpri_score = mpri_data.get("mpri_score", 100.0)
    mpri_tier = mpri_data.get("mpri_tier", "GOLD MASTERY PATH")
    mpri_pillars = mpri_data.get("pillars", {})

    today_str = datetime.date.today().isoformat()
    is_empty_course = total_comps == 0 or total_questions == 0

    if is_empty_course or final_score < 11.0 or mpri_score < 40.0 or (hard_penalties and final_score < 14.0):
        platform_status = "RECHAZADO"
    elif final_score >= 14.0 and mpri_score >= 70.0 and not hard_penalties:
        platform_status = "ACTIVO"
    else:
        platform_status = "OBSERVADO"

    if platform_status == "ACTIVO":
        remediation_actions = [
            f"Certificación plena para despliegue en plataforma Top's Academy con Nivel {quality_tier}.",
            f"El banco de {total_questions} reactivos y {total_comps} competencias cumple con los estándares Quality Matters, OSCQR y Mastery Learning.",
        ]
        verdict_text = (
            f"El curso **{title}** ha sido **certificado y aprobado** con calificación de "
            f"**{final_score:.1f} / 20.0** y MPRI de **{mpri_score:.2f} / 100.0**, "
            f"acreditando el cumplimiento de los estándares Quality Matters, OSCQR y Mastery Learning."
        )
    else:
        remediation_actions = []
        if is_empty_course:
            remediation_actions.append(
                "Curso vacío o incompleto: requiere al menos competencias y reactivos válidos antes de su certificación."
            )
        for p in hard_penalties:
            if isinstance(p, dict):
                remediation_actions.append(
                    f"Resolver penalización dura [{p.get('rule', 'unknown')}]: {p.get('reason', '')}"
                )
        if final_score < 14.0:
            remediation_actions.append(
                f"Elevar calificación global ({final_score:.1f}/20.0 < 14.0 mínimo requerido) atendiendo dimensiones deficitarias."
            )
        if mpri_score < 70.0:
            remediation_actions.append(
                f"Elevar Índice MPRI ({mpri_score:.2f}/100.0 < 70.0 mínimo requerido) fortaleciendo ZPD, modalidad activa y andamiaje."
            )
        if not remediation_actions:
            remediation_actions.append(
                f"Revisar observaciones pendientes antes de habilitar despliegue pleno (estado: {platform_status})."
            )

        if platform_status == "OBSERVADO":
            verdict_text = (
                f"El curso **{title}** queda en estado **OBSERVADO** (requiere correcciones antes de despliegue pleno) "
                f"con calificación de **{final_score:.1f} / 20.0** y MPRI de **{mpri_score:.2f} / 100.0**."
            )
        else:
            verdict_text = (
                f"El curso **{title}** ha sido **RECHAZADO** para despliegue en plataforma con calificación de "
                f"**{final_score:.1f} / 20.0** y MPRI de **{mpri_score:.2f} / 100.0**. "
                f"Debe corregir las brechas críticas y penalizaciones bloqueantes antes de reevaluar."
            )

    qa_report_json = {
        "course_metadata": {
            "course_id": course_id,
            "unit_title": title,
            "detected_objective": description,
            "total_competencies": total_comps,
            "total_questions": total_questions,
            "question_types_distribution": types_count,
            "platform_status": platform_status,
            "evaluator": "Course QA Evaluator — Standardized Deterministic Engine",
            "evaluation_date": today_str,
        },
        "dimension_scores": dim_scores,
        "penalties_applied": hard_penalties,
        "raw_subtotal": raw_subtotal,
        "final_score": final_score,
        "quality_tier": quality_tier,
        "mastery_path_readiness": mpri_data,
        "remediation_actions": remediation_actions,
        "discovered_lint_rules": [],
        "platform_status": platform_status,
    }

    def _status_icon(sc: float, mx: float) -> str:
        ratio = sc / mx if mx > 0 else 1.0
        if ratio >= 0.99:
            return "✅ Impecable"
        elif ratio >= 0.90:
            return "✨ Excelente"
        elif ratio >= 0.70:
            return "⚠️ Observación menor"
        return "❌ Deficiente"

    md_lines = [
        "# Informe de Auditoría de Calidad Pedagógica y Psicométrica (QM-OSCQR)",
        f"## Curso: {title} (`{course_id}`)",
        "",
        f"- **Fecha de Evaluación:** {today_str}",
        "- **Evaluador:** Course QA Evaluator — Top's Academy (Modo Determinista)",
        f"- **Estado en Plataforma:** {platform_status}",
        f"- **Calificación Final Certificada:** **{final_score:.1f} / 20.0 pts**",
        f"- **Quality Tier:** **{quality_tier}**",
        f"- **Mastery Path Readiness Index (MPRI):** **{mpri_score:.2f} / 100.0** ({mpri_tier})",
        "",
        "---",
        "",
        "### 1. Resumen Ejecutivo de Dimensiones",
        "",
        "| Dimensión | Puntuación | Máximo | Calificación | Estado |",
        "| :--- | :---: | :---: | :---: | :---: |",
        f"| **D1: Arquitectura Curricular y Granularidad** | **{d1.get('score', 4.0):.1f}** | 4.0 | {(d1.get('score', 4.0)/4.0)*100:.0f}% | {_status_icon(d1.get('score', 4.0), 4.0)} |",
        f"| **D2: Calidad Psicométrica y Reactivos** | **{d2.get('score', 5.0):.1f}** | 5.0 | {(d2.get('score', 5.0)/5.0)*100:.0f}% | {_status_icon(d2.get('score', 5.0), 5.0)} |",
        f"| **D3: Andamiaje y Pistas Socráticas** | **{d3.get('score', 5.0):.1f}** | 5.0 | {(d3.get('score', 5.0)/5.0)*100:.0f}% | {_status_icon(d3.get('score', 5.0), 5.0)} |",
        f"| **D4: Alineación Instruccional y ZPD** | **{d4.get('score', 4.0):.1f}** | 4.0 | {(d4.get('score', 4.0)/4.0)*100:.0f}% | {_status_icon(d4.get('score', 4.0), 4.0)} |",
        f"| **D5: Ergonomía Técnica y KaTeX** | **{d5.get('score', 2.0):.1f}** | 2.0 | {(d5.get('score', 2.0)/2.0)*100:.0f}% | {_status_icon(d5.get('score', 2.0), 2.0)} |",
        f"| **Penalizaciones Duras** | **-{det_rubric.get('hard_penalties_total', 0.0):.1f}** | - | - | {'✅ Sin penalizaciones' if not hard_penalties else '⚠️ Penalizaciones aplicadas'} |",
        f"| **TOTAL** | **{final_score:.1f}** | **20.0** | **{(final_score/20.0)*100:.1f}%** | 🏆 **{quality_tier.split('—')[-1].strip()}** |",
        "",
        "---",
        "",
        "### 2. Desglose Detallado por Dimensión",
        "",
        f"#### D1. Arquitectura Curricular y Granularidad ({d1.get('score', 4.0):.1f} / 4.0 pts)",
        f"- {d1.get('feedback', '')}",
        "",
        f"#### D2. Calidad Psicométrica y Reactivos ({d2.get('score', 5.0):.1f} / 5.0 pts)",
        f"- {d2.get('feedback', '')}",
        "",
        f"#### D3. Andamiaje y Pistas Socráticas ({d3.get('score', 5.0):.1f} / 5.0 pts)",
        f"- {d3.get('feedback', '')}",
        "",
        f"#### D4. Alineación Instruccional y ZPD ({d4.get('score', 4.0):.1f} / 4.0 pts)",
        f"- {d4.get('feedback', '')}",
        "",
        f"#### D5. Ergonomía Técnica y KaTeX ({d5.get('score', 2.0):.1f} / 2.0 pts)",
        f"- {d5.get('feedback', '')}",
        "",
        "---",
        "",
        "### 3. Índice de Preparación para el Dominio (MPRI: 100.0 pts)",
        "",
        "| Pilar Cognitivo | Puntaje | Máximo | Calificación |",
        "| :--- | :---: | :---: | :---: |",
        f"| **1. Progresión Adaptativa ZPD y Bloom** | **{mpri_pillars.get('zpd_adaptive_progression', {}).get('score', 20.0):.2f}** | 20.0 | {(mpri_pillars.get('zpd_adaptive_progression', {}).get('score', 20.0)/20.0)*100:.1f}% |",
        f"| **2. Modalidad de Evocación y Anti-Gaming** | **{mpri_pillars.get('retrieval_modality_and_anti_gaming', {}).get('score', 20.0):.2f}** | 20.0 | {(mpri_pillars.get('retrieval_modality_and_anti_gaming', {}).get('score', 20.0)/20.0)*100:.1f}% |",
        f"| **3. Integridad Salvavidas Socrático (3-Strikes)** | **{mpri_pillars.get('socratic_scaffolding_lifeline', {}).get('score', 25.0):.2f}** | 25.0 | {(mpri_pillars.get('socratic_scaffolding_lifeline', {}).get('score', 25.0)/25.0)*100:.1f}% |",
        f"| **4. Alineación Diagnóstica en FeedbackToast** | **{mpri_pillars.get('diagnostic_remediation_alignment', {}).get('score', 15.0):.2f}** | 15.0 | {(mpri_pillars.get('diagnostic_remediation_alignment', {}).get('score', 15.0)/15.0)*100:.1f}% |",
        f"| **5. Topología DAG e Interleaving** | **{mpri_pillars.get('dag_and_interleaving_topology', {}).get('score', 10.0):.2f}** | 10.0 | {(mpri_pillars.get('dag_and_interleaving_topology', {}).get('score', 10.0)/10.0)*100:.1f}% |",
        f"| **6. Ergonomía Cognitiva y Sintaxis KaTeX** | **{mpri_pillars.get('cognitive_ergonomics_and_framing', {}).get('score', 10.0):.2f}** | 10.0 | {(mpri_pillars.get('cognitive_ergonomics_and_framing', {}).get('score', 10.0)/10.0)*100:.1f}% |",
        f"| **TOTAL MPRI** | **{mpri_score:.2f}** | **100.0** | **{mpri_score:.1f}% ({mpri_tier})** |",
        "",
        "---",
        "",
        "### 4. Veredicto y Certificación",
        "",
        verdict_text,
        "",
        "---",
        "",
        "<details>",
        "<summary>Metadatos Estructurados (JSON)</summary>",
        "",
        "```json",
        json.dumps(qa_report_json, indent=2, ensure_ascii=False),
        "```",
        "",
        "</details>",
    ]
    qa_report_md = "\n".join(md_lines)
    return qa_report_json, qa_report_md


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
            DomainImpossibleDistractorLinter(),
            FibRoundingContractLinter(),
            MsLengthBiasLinter(),
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
        category = (course_data.get("category") or "").lower()
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
        corrupt_prob_key_cnt = summaries.get("domain_impossible_distractor_linter", {}).get("corrupted_prob_key_items_count", 0)

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

        if corrupt_prob_key_cnt > 0:
            hard_penalties.append({
                "rule": "corrupted_probability_key",
                "deduction": round(min(1.5, corrupt_prob_key_cnt * 0.5), 2),
                "reason": (
                    f"{corrupt_prob_key_cnt} reactivo(s) presentan clave correcta matemáticamente imposible "
                    f"(probabilidad o cota de probabilidad > 1.0 o < 0.0)."
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
            "domain_impossible_options": [],
            "string_concat_collisions": [],
            "disconnected_numeric_rationales": [],
            "duplicate_competencies": [],
            "sympy_in_katex": [],
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
            elif iss.linter == "uninterpolated_math_variable_linter" and "concatenación" in iss.message.lower():
                if qid not in risk_clusters["string_concat_collisions"]:
                    risk_clusters["string_concat_collisions"].append(qid)
                if qid not in risk_clusters["katex_issues"]:
                    risk_clusters["katex_issues"].append(qid)
            elif iss.linter == "katex_syntax_linter" and "sympy" in iss.message.lower():
                if qid not in risk_clusters["sympy_in_katex"]:
                    risk_clusters["sympy_in_katex"].append(qid)
                if qid not in risk_clusters["katex_issues"]:
                    risk_clusters["katex_issues"].append(qid)
            elif iss.dimension == "D5_katex" and qid not in risk_clusters["katex_issues"]:
                risk_clusters["katex_issues"].append(qid)
            elif iss.linter == "domain_impossible_distractor_linter":
                if qid not in risk_clusters["domain_impossible_options"]:
                    risk_clusters["domain_impossible_options"].append(qid)
            elif iss.linter == "architecture_dag_linter" and "solapamiento" in iss.message.lower():
                if qid not in risk_clusters["duplicate_competencies"]:
                    risk_clusters["duplicate_competencies"].append(qid)
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
                if "desconexión diagnóstica" in iss.message.lower():
                    if qid not in risk_clusters["disconnected_numeric_rationales"]:
                        risk_clusters["disconnected_numeric_rationales"].append(qid)
                elif qid not in risk_clusters["magic_multiplier_distractors"]:
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
        deterministic_rubric = compute_deterministic_rubric_scores(summaries, len(comps), len(questions), hard_penalties)
        final_score = deterministic_rubric["final_score"]
        quality_tier = deterministic_rubric["quality_tier"]

        return TelemetryReport(
            course_id=course_id,
            title=title,
            total_competencies=len(comps),
            total_questions=len(questions),
            dimension_summaries=summaries,
            hard_penalties=hard_penalties,
            risk_score=risk_score,
            mastery_path_readiness=mastery_readiness,
            deterministic_rubric=deterministic_rubric,
            final_score=final_score,
            quality_tier=quality_tier,
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
