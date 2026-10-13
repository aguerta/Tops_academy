"""Structural, pedagogical, and referential integrity rules (Pass 2).

Implements:
- R-05: Duplicate Competency IDs (ERR_DUP_COMPETENCY)
- R-06: Duplicate Question IDs (ERR_DUP_QUESTION)
- R-07: Missing Competency Reference (ERR_MISSING_COMPETENCY)
- R-08: Question count minimums: Skill >= 30 (ERR_COUNT_SKILL)
- R-09: Question count minimums: Fact/Concept >= 20 (ERR_COUNT_CONCEPT)
- R-10: Multiple choice option count == 7 (ERR_MC_COUNT)
- R-11: Multiple choice correct count == 1 (ERR_MC_CORRECT)
- R-12: Multiple select option count between 4 and 6 (ERR_MS_COUNT)
- R-13: Multiple select correct count between 1 and n-1 (ERR_MS_CORRECT)
- R-14: Hint count scaffolding between 3 and 5 (ERR_HINT_COUNT)
- R-04: Answer key presence for fill_in_the_blank (ERR_MISSING_ANSWER)
Extended Quality Rules:
- R-17: Formative Rationale without Placeholders (ERR_PLACEHOLDER_RATIONALE)
- R-18: Confinement of Psychometric Meta-Information (ERR_META_GIVEAWAY)
- R-19: Answer Leak Prevention in Fill-in-the-Blank (ERR_ANSWER_LEAK)
- R-20: LaTeX Syntax, Delimiters, Double Braces, and Unreplaced Template Vars (ERR_LATEX_SYNTAX)
- R-22: Mandatory Diagnostic Error Rationale in Multiple Select (ERR_MS_MISSING_RATIONALE)
Strict Mode Rules:
- S-01: Step-by-step solution required (ERR_STRICT_MISSING_SOLUTION)
- S-02: Misconception warning required (ERR_STRICT_MISSING_MISCONCEPTION)
- S-03: Explicit difficulty required (ERR_STRICT_MISSING_DIFFICULTY)
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Any
from .models import ValidationError



def check_semantic_rules(data: dict[str, Any]) -> list[ValidationError]:
    """Validates structural and pedagogical rules on parsed course data."""
    errors: list[ValidationError] = []

    competencies = data.get("competencies")
    questions = data.get("questions")

    if not isinstance(competencies, list) or not isinstance(questions, list):
        # Schema validator handles non-list structure
        return errors

    # --- Rule R-05: Duplicate Competency IDs ---
    seen_comp_ids: set[str] = set()
    for comp in competencies:
        if isinstance(comp, dict) and "id" in comp:
            comp_id = comp["id"]
            if comp_id in seen_comp_ids:
                errors.append(ValidationError(
                    rule_id="R-05",
                    code="ERR_DUP_COMPETENCY",
                    message=f"Duplicate competency ID found: '{comp_id}'",
                    item_id=comp_id
                ))
            else:
                seen_comp_ids.add(comp_id)

    # --- Rule R-06: Duplicate Question IDs ---
    seen_q_ids: set[str] = set()
    for q in questions:
        if isinstance(q, dict) and "id" in q:
            q_id = q["id"]
            if q_id in seen_q_ids:
                errors.append(ValidationError(
                    rule_id="R-06",
                    code="ERR_DUP_QUESTION",
                    message=f"Duplicate question ID found: '{q_id}'",
                    item_id=q_id
                ))
            else:
                seen_q_ids.add(q_id)

    # --- Rule R-07: Referential Integrity (Competency Reference) ---
    declared_comp_ids = {c["id"] for c in competencies if isinstance(c, dict) and "id" in c}
    q_counts_by_comp: Counter[str] = Counter()

    for q in questions:
        if not isinstance(q, dict):
            continue
        q_id = q.get("id", "UNKNOWN")
        comp_id = q.get("competency_id")
        if not comp_id and isinstance(q.get("competency_ref"), dict):
            comp_id = q["competency_ref"].get("id")

        if comp_id:
            if comp_id not in declared_comp_ids:
                errors.append(ValidationError(
                    rule_id="R-07",
                    code="ERR_MISSING_COMPETENCY",
                    message=f"Question '{q_id}' references unknown competency '{comp_id}'",
                    item_id=q_id
                ))
            else:
                q_counts_by_comp[comp_id] += 1
        else:
            errors.append(ValidationError(
                rule_id="R-07",
                code="ERR_MISSING_COMPETENCY",
                message=f"Question '{q_id}' has no competency_id specified",
                item_id=q_id
            ))

    # --- Rules R-08 & R-09: Minimum Questions per Competency ---
    for comp in competencies:
        if not isinstance(comp, dict) or "id" not in comp:
            continue
        c_id = comp["id"]
        category = comp.get("category", "")
        count = q_counts_by_comp[c_id]

        if category == "Skill":
            if count < 30:
                errors.append(ValidationError(
                    rule_id="R-08",
                    code="ERR_COUNT_SKILL",
                    message=f"Competency '{c_id}' (category 'Skill') has {count} questions; minimum required is 30",
                    item_id=c_id
                ))
        elif category in ("Fact", "Concept"):
            if count < 20:
                errors.append(ValidationError(
                    rule_id="R-09",
                    code="ERR_COUNT_CONCEPT",
                    message=f"Competency '{c_id}' (category '{category}') has {count} questions; minimum required is 20",
                    item_id=c_id
                ))

    # --- Rules R-10 through R-14 & R-04: Per-Question Structural Constraints ---
    for q in questions:
        if not isinstance(q, dict):
            continue
        q_id = q.get("id", "UNKNOWN")
        itype = q.get("interaction_type")
        options = q.get("options")
        hints = q.get("hints")

        # R-14: Hint Count Scaffolding
        if isinstance(hints, list):
            h_count = len(hints)
            if h_count < 3 or h_count > 5:
                errors.append(ValidationError(
                    rule_id="R-14",
                    code="ERR_HINT_COUNT",
                    message=f"Question '{q_id}' has {h_count} hints; must have between 3 and 5 hints",
                    item_id=q_id
                ))

        # R-10 & R-11: Multiple Choice (exactly 7 options, exactly 1 correct)
        if itype == "multiple_choice_7_options":
            if isinstance(options, list):
                n_opts = len(options)
                if n_opts != 7:
                    errors.append(ValidationError(
                        rule_id="R-10",
                        code="ERR_MC_COUNT",
                        message=f"Question '{q_id}' has {n_opts} options; multiple-choice items must have exactly 7 options",
                        item_id=q_id
                    ))
                k_correct = sum(1 for opt in options if isinstance(opt, dict) and opt.get("is_correct") is True)
                if k_correct != 1:
                    errors.append(ValidationError(
                        rule_id="R-11",
                        code="ERR_MC_CORRECT",
                        message=f"Question '{q_id}' has {k_correct} correct options; multiple-choice items must have exactly 1 correct option",
                        item_id=q_id
                    ))
            else:
                errors.append(ValidationError(
                    rule_id="R-10",
                    code="ERR_MC_COUNT",
                    message=f"Question '{q_id}' has 0 options; multiple-choice items must have exactly 7 options",
                    item_id=q_id
                ))

        # R-12 & R-13: Multiple Select (4 to 6 options, 1 to n-1 correct)
        elif itype == "multiple_select":
            if isinstance(options, list):
                n_opts = len(options)
                if n_opts < 4 or n_opts > 6:
                    errors.append(ValidationError(
                        rule_id="R-12",
                        code="ERR_MS_COUNT",
                        message=f"Question '{q_id}' has {n_opts} options; multiple-select items must have between 4 and 6 options",
                        item_id=q_id
                    ))
                if n_opts > 0:
                    k_correct = sum(1 for opt in options if isinstance(opt, dict) and opt.get("is_correct") is True)
                    if k_correct < 1 or k_correct >= n_opts:
                        errors.append(ValidationError(
                            rule_id="R-13",
                            code="ERR_MS_CORRECT",
                            message=f"Question '{q_id}' has {k_correct} correct options out of {n_opts}; multiple-select items must have between 1 and n-1 correct options",
                            item_id=q_id
                        ))
            else:
                errors.append(ValidationError(
                    rule_id="R-12",
                    code="ERR_MS_COUNT",
                    message=f"Question '{q_id}' has 0 options; multiple-select items must have between 4 and 6 options",
                    item_id=q_id
                ))

        # R-04: Fill-in-the-Blank Answer Key Validation
        elif itype == "fill_in_the_blank":
            ans = q.get("correct_answer")
            is_valid_ans = False

            if isinstance(ans, str) and bool(ans.strip()):
                is_valid_ans = True
            elif isinstance(ans, (int, float)) and not isinstance(ans, bool):
                is_valid_ans = True
            elif isinstance(ans, list) and len(ans) > 0 and any(isinstance(x, str) and bool(x.strip()) for x in ans):
                is_valid_ans = True
            elif isinstance(ans, dict) and len(ans) > 0:
                val = ans.get("value")
                expr = ans.get("expression")
                has_valid_val = (
                    (isinstance(val, str) and bool(val.strip()))
                    or (isinstance(val, (int, float)) and not isinstance(val, bool))
                    or (isinstance(val, list) and len(val) > 0 and any(isinstance(x, str) and bool(x.strip()) for x in val))
                )
                has_valid_expr = isinstance(expr, str) and bool(expr.strip())
                if has_valid_val or has_valid_expr:
                    is_valid_ans = True

            if not is_valid_ans:
                errors.append(ValidationError(
                    rule_id="R-04",
                    code="ERR_MISSING_ANSWER",
                    message=f"Question '{q_id}' of type 'fill_in_the_blank' must specify a valid non-empty 'correct_answer' with expression or value",
                    item_id=q_id
                ))

    return errors


def check_strict_rules(data: dict[str, Any]) -> list[ValidationError]:
    """Evaluates strict-mode criteria: verifies mandatory solutions,
    misconception warnings, and valid difficulty levels for every question.
    """
    errors: list[ValidationError] = []
    questions = data.get("questions", [])
    if not isinstance(questions, list):
        return errors

    for q in questions:
        if not isinstance(q, dict):
            continue
        q_id = q.get("id", "UNKNOWN")

        # S-01: Step-by-step solution required
        sol = q.get("solution") or q.get("detailed_solution")
        if not sol or not isinstance(sol, str) or not sol.strip():
            errors.append(ValidationError(
                rule_id="S-01",
                code="ERR_STRICT_MISSING_SOLUTION",
                message=f"Question '{q_id}' must provide a non-empty step-by-step 'solution' or 'detailed_solution' in strict mode",
                item_id=q_id
            ))

        # S-02: Misconception warning required
        misc = q.get("misconception_warning") or q.get("common_misconception_warning")
        if not misc or not isinstance(misc, str) or not misc.strip():
            errors.append(ValidationError(
                rule_id="S-02",
                code="ERR_STRICT_MISSING_MISCONCEPTION",
                message=f"Question '{q_id}' must provide a non-empty 'misconception_warning' in strict mode",
                item_id=q_id
            ))

        # S-03: Explicit difficulty required
        diff = q.get("difficulty")
        if diff not in ("easy", "medium", "hard"):
            errors.append(ValidationError(
                rule_id="S-03",
                code="ERR_STRICT_MISSING_DIFFICULTY",
                message=f"Question '{q_id}' must specify a valid difficulty level ('easy', 'medium', 'hard') in strict mode",
                item_id=q_id
            ))

    return errors


def check_extended_quality_rules(data: dict[str, Any]) -> list[ValidationError]:
    """Validates extended pedagogical and structural quality rules:
    - R-17: Placeholder/Generic Error Rationale (ERR_PLACEHOLDER_RATIONALE)
    - R-18: Meta-information / Psychometric Giveaway in option content (ERR_META_GIVEAWAY)
    - R-19: Answer Leak in fill_in_the_blank question stem (ERR_ANSWER_LEAK)
    - R-20: LaTeX Syntax, Delimiters, Residual Double Braces, and Template Variables (ERR_LATEX_SYNTAX)
    - R-22: Mandatory Diagnostic Error Rationale in multiple_select (ERR_MS_MISSING_RATIONALE)
    """
    errors: list[ValidationError] = []

    generic_placeholders = {
        "placeholder", "distractor", "error", "n/a", "na", "none", "null",
        "ninguno", "ninguna", "comodin", "comodín", "generic", "generico",
        "genérico", "todo", "tbd", "opcion incorrecta", "opción incorrecta",
        "incorrect", "incorrecto", "incorrecta", "test", "dummy", "default",
    }

    def is_placeholder_rationale(rationale: Any) -> bool:
        if not isinstance(rationale, str):
            return True
        cleaned = rationale.strip().strip(".!?,;:\"'-_ ").lower()
        if not cleaned:
            return True
        if cleaned in generic_placeholders:
            return True
        if re.match(r"^(?:placeholder|distractor|error)(?:\s+[a-z0-9]+)?$", cleaned):
            return True
        if re.match(r"^error\s+(?:gen[eé]rico|rationale|de\s+prueba)$", cleaned):
            return True
        if "placeholder" in cleaned:
            return True
        if re.match(r"^n/?a$", cleaned):
            return True
        if re.match(r"^none$", cleaned):
            return True
        return False

    meta_giveaway_regex = re.compile(
        r"^\s*confundiendo\b|\b(?:sumando|restando|calculado|calculando|asumiendo|multiplicando|dividiendo)\s+err[oó]neamente\b",
        re.IGNORECASE
    )

    def check_latex_and_templates(text: str, q_id: str, field_desc: str) -> list[ValidationError]:
        text_errors: list[ValidationError] = []

        # 1. Prohibición de delimitadores triples '$$$'
        if "$$$" in text:
            text_errors.append(ValidationError(
                rule_id="R-20",
                code="ERR_LATEX_SYNTAX",
                message=f"Question '{q_id}' in {field_desc}: Forbidden triple math delimiter '$$$' detected",
                item_id=q_id
            ))

        # 2. Número par y balanceado de delimitadores '$' y '$$'
        clean_text = text.replace(r"\$", "")
        if clean_text.count("$$") % 2 != 0:
            text_errors.append(ValidationError(
                rule_id="R-20",
                code="ERR_LATEX_SYNTAX",
                message=f"Question '{q_id}' in {field_desc}: Unbalanced display math delimiters '$$'",
                item_id=q_id
            ))
        clean_inline = clean_text.replace("$$", "")
        if clean_inline.count("$") % 2 != 0:
            text_errors.append(ValidationError(
                rule_id="R-20",
                code="ERR_LATEX_SYNTAX",
                message=f"Question '{q_id}' in {field_desc}: Unbalanced inline math delimiters '$'",
                item_id=q_id
            ))

        # 3. Prohibición de llaves dobles residuales '{{' o '}}' dentro de expresiones matemáticas
        math_matches = re.findall(r"\$\$(.*?)\$\$|\$(.*?)\$", text, flags=re.DOTALL)
        has_double_brace_in_math = False
        has_unbalanced_braces_in_math = False
        unbalanced_sample = ""
        for mb in math_matches:
            block = mb[0] if mb[0] else mb[1]
            if "{{" in block and not re.search(r"\\[a-zA-Z]+\s*\{\{", block):
                has_double_brace_in_math = True
            if re.search(r"\{\{\s*[a-zA-Z0-9_]+\s*\}\}", block):
                has_double_brace_in_math = True
            clean_block = block.replace(r"\{", "").replace(r"\}", "")
            if clean_block.count("{") != clean_block.count("}"):
                has_unbalanced_braces_in_math = True
                unbalanced_sample = clean_block[:60]
                break

        if has_unbalanced_braces_in_math:
            text_errors.append(ValidationError(
                rule_id="R-20",
                code="ERR_LATEX_SYNTAX",
                message=f"Question '{q_id}' in {field_desc}: Unbalanced curly braces in LaTeX math block: '{unbalanced_sample}'",
                item_id=q_id
            ))

        if has_double_brace_in_math:
            text_errors.append(ValidationError(
                rule_id="R-20",
                code="ERR_LATEX_SYNTAX",
                message=f"Question '{q_id}' in {field_desc}: Residual double braces '{{{{' or '}}}}' found in mathematical expression",
                item_id=q_id
            ))

        # 4. Prohibición de variables de plantilla no sustituidas (patrón '{variable_name}' no reemplazado)
        # Permite explícitamente notación matemática de conjuntos/tuplas mayúsculas (ej. {K}, {Y}, {K, L})
        unreplaced: list[str] = []
        for m in re.finditer(r"\{([a-zA-Z0-9_,\s]+)\}", text):
            inner = m.group(1).strip()
            # Si contiene letras y todas son mayúsculas (ej. {K}, {Y}, {K, L}, {A, B}), es notación matemática/económica
            letters = re.findall(r"[a-zA-Z]", inner)
            if letters and all(c.isupper() for c in letters):
                continue
            # Solo evaluar como variable de plantilla si coincide con identificador típico (ej. {k_val}, {slope})
            if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", inner):
                continue
            start = m.start()
            prefix = text[:start]
            # Valid LaTeX macro preceding: e.g. \text{, \frac{a}{b}, \begin{cases}
            if re.search(r"\\[a-zA-Z]+(?:\s*\{[^{}]*\})*\s*$", prefix):
                continue
            # Subscripts and superscripts: _{...}, ^{...}
            if re.search(r"[_^]\s*$", prefix):
                continue
            # Escaped brace \{
            if re.search(r"\\\{\s*$", prefix):
                continue
            unreplaced.append(m.group(0))

        if unreplaced:
            preview = ", ".join(unreplaced[:3])
            text_errors.append(ValidationError(
                rule_id="R-20",
                code="ERR_LATEX_SYNTAX",
                message=f"Question '{q_id}' in {field_desc}: Unreplaced template variable(s) found: {preview}",
                item_id=q_id
            ))

        # 5. Linter de residuos de variables de código en texto estudiantil (_val, _num, _str)
        var_residues = re.findall(r"\b([a-zA-Z0-9]+_(?:val|num|str|res))\b", text)
        if var_residues:
            res_preview = ", ".join(sorted(set(var_residues))[:3])
            text_errors.append(ValidationError(
                rule_id="R-20",
                code="ERR_VARIABLE_RESIDUE",
                message=f"Question '{q_id}' in {field_desc}: Leaked raw code variable identifier(s) found: {res_preview}",
                item_id=q_id
            ))

        # 6. Linter de sustitución ciega que corrompe operadores diferenciales (\dot36 en lugar de \dot{r})
        if re.search(r"\\dot\d+", text) or re.search(r"\\dot\{\d+\}", text):
            text_errors.append(ValidationError(
                rule_id="R-19",
                code="ERR_ANSWER_LEAK_SYNTAX",
                message=f"Question '{q_id}' in {field_desc}: Corrupted differential operator or answer leak detected (e.g. \\dot<number>)",
                item_id=q_id
            ))

        # 7. Unclosed nested accent/style macros (\hat{\boldsymbol{, \hat{\mathbf{, \bar{\mathbf{, \tilde{\boldsymbol{)
        nested_macro_pattern = re.compile(
            r"\\(hat|bar|tilde|vec|dot|ddot|check|acute|grave|mathring|widecheck|widehat|widetilde)"
            r"\s*\{\s*"
            r"\\(boldsymbol|mathbf|bm|mathit|mathrm|mathbb|mathcal|text|textbf)"
            r"\s*\{"
        )
        for m in nested_macro_pattern.finditer(text):
            start_pos = m.end()
            depth = 2
            idx = start_pos
            is_unclosed = False
            while idx < len(text):
                ch = text[idx]
                if ch == "\\":
                    idx += 2
                    continue
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 1:
                        rest = text[idx + 1:].lstrip()
                        if not rest or not rest.startswith("}"):
                            is_unclosed = True
                            break
                    elif depth == 0:
                        break
                elif ch == "$" and depth > 0:
                    is_unclosed = True
                    break
                idx += 1
            else:
                if depth > 0:
                    is_unclosed = True

            if is_unclosed:
                snippet = text[m.start():min(len(text), m.start() + 40)]
                text_errors.append(ValidationError(
                    rule_id="R-20",
                    code="ERR_LATEX_SYNTAX",
                    message=f"Question '{q_id}' in {field_desc}: Unclosed nested accent/style macro detected: '{snippet}'",
                    item_id=q_id
                ))

        # 8. Macro arity validation (\frac, \binom, \overset, \underset, etc.)
        for m in re.finditer(r"\\(frac|dfrac|cfrac|binom|dbinom|tbinom|overset|underset)\b", text):
            macro_name = m.group(1)
            # Find and parse argument 1
            curr = m.end()
            while curr < len(text) and text[curr].isspace():
                curr += 1
            arg1_valid = False
            if curr < len(text) and text[curr] == "{":
                depth = 1
                curr += 1
                while curr < len(text):
                    if text[curr] == "\\":
                        curr += 2
                        continue
                    if text[curr] == "{":
                        depth += 1
                    elif text[curr] == "}":
                        depth -= 1
                        if depth == 0:
                            arg1_valid = True
                            curr += 1
                            break
                    elif text[curr] == "$":
                        break
                    curr += 1

            arg2_valid = False
            if arg1_valid:
                while curr < len(text) and text[curr].isspace():
                    curr += 1
                if curr < len(text) and text[curr] == "{":
                    depth = 1
                    curr += 1
                    while curr < len(text):
                        if text[curr] == "\\":
                            curr += 2
                            continue
                        if text[curr] == "{":
                            depth += 1
                        elif text[curr] == "}":
                            depth -= 1
                            if depth == 0:
                                arg2_valid = True
                                break
                        elif text[curr] == "$":
                            break
                        curr += 1

            if not arg1_valid or not arg2_valid:
                snippet = text[m.start():min(len(text), m.start() + 40)]
                text_errors.append(ValidationError(
                    rule_id="R-20",
                    code="ERR_LATEX_SYNTAX",
                    message=f"Question '{q_id}' in {field_desc}: Macro '\\{macro_name}' requires 2 braced arguments, but was incomplete or malformed: '{snippet}'",
                    item_id=q_id
                ))

        # 9. Unclosed LaTeX environments (\begin{env} ... \end{env})
        env_stack: list[str] = []
        for m in re.finditer(r"\\(begin|end)\s*\{([a-zA-Z*]+)\}", text):
            action, env = m.group(1), m.group(2)
            if action == "begin":
                env_stack.append(env)
            else:
                if not env_stack:
                    text_errors.append(ValidationError(
                        rule_id="R-20",
                        code="ERR_LATEX_SYNTAX",
                        message=f"Question '{q_id}' in {field_desc}: Unexpected LaTeX environment closure '\\end{{{env}}}' with no matching '\\begin'",
                        item_id=q_id
                    ))
                elif env_stack[-1] != env:
                    expected = env_stack.pop()
                    text_errors.append(ValidationError(
                        rule_id="R-20",
                        code="ERR_LATEX_SYNTAX",
                        message=f"Question '{q_id}' in {field_desc}: Mismatched LaTeX environment closure '\\end{{{env}}}', expected '\\end{{{expected}}}'",
                        item_id=q_id
                    ))
                else:
                    env_stack.pop()

        for unclosed_env in env_stack:
            text_errors.append(ValidationError(
                rule_id="R-20",
                code="ERR_LATEX_SYNTAX",
                message=f"Question '{q_id}' in {field_desc}: Unclosed LaTeX environment '\\begin{{{unclosed_env}}}' detected (missing '\\end{{{unclosed_env}}}')",
                item_id=q_id
            ))

        # 10. Unclosed scalable delimiters (\left( \right), \left[ \right], \left\{ \right\})
        matching_delims = {
            "(": ")",
            "[": "]",
            r"\{": r"\}",
        }
        delim_stack: list[str] = []

        def report_unclosed_delims(stack: list[str]) -> None:
            for unclosed_delim in stack:
                exp_r = matching_delims.get(unclosed_delim, "")
                right_desc = f"'\\right{exp_r}'" if exp_r else "'\\right'"
                text_errors.append(ValidationError(
                    rule_id="R-20",
                    code="ERR_LATEX_SYNTAX",
                    message=f"Question '{q_id}' in {field_desc}: Unclosed scalable delimiter '\\left{unclosed_delim}' detected (missing matching {right_desc})",
                    item_id=q_id
                ))

        token_pattern = re.compile(
            r"\$\$|(?<!\\)\$|\\(left|right)\s*(\(|\)|\[|\]|\\\{|\\\}|\||\.)"
        )
        for tm in token_pattern.finditer(text):
            tok = tm.group(0)
            if tok in ("$$", "$"):
                if delim_stack:
                    report_unclosed_delims(delim_stack)
                    delim_stack.clear()
            else:
                direction, delim = tm.group(1), tm.group(2)
                if direction == "left":
                    delim_stack.append(delim)
                else:
                    if not delim_stack:
                        text_errors.append(ValidationError(
                            rule_id="R-20",
                            code="ERR_LATEX_SYNTAX",
                            message=f"Question '{q_id}' in {field_desc}: Unexpected scalable delimiter closure '\\right{delim}' with no matching '\\left'",
                            item_id=q_id
                        ))
                    else:
                        open_delim = delim_stack.pop()
                        expected_close = matching_delims.get(open_delim)
                        if expected_close and delim != expected_close and delim != ".":
                            text_errors.append(ValidationError(
                                rule_id="R-20",
                                code="ERR_LATEX_SYNTAX",
                                message=f"Question '{q_id}' in {field_desc}: Mismatched scalable delimiter '\\right{delim}', expected '\\right{expected_close}' for '\\left{open_delim}'",
                                item_id=q_id
                            ))

        if delim_stack:
            report_unclosed_delims(delim_stack)
            delim_stack.clear()

        return text_errors

    # --- Rule R-20: Root Course Metadata ---
    course_id = str(data.get("course_id", "course"))
    course_title = data.get("course_title")
    if isinstance(course_title, str):
        errors.extend(check_latex_and_templates(course_title, course_id, "course_title"))

    course_desc = data.get("description")
    if isinstance(course_desc, str):
        errors.extend(check_latex_and_templates(course_desc, course_id, "description"))

    # --- Rule R-20: Course Competencies ---
    competencies = data.get("competencies")
    if isinstance(competencies, list):
        for comp in competencies:
            if not isinstance(comp, dict):
                continue
            comp_id = str(comp.get("id", "competency"))
            comp_name = comp.get("name")
            if isinstance(comp_name, str):
                errors.extend(check_latex_and_templates(comp_name, comp_id, "competency.name"))
            comp_desc = comp.get("description")
            if isinstance(comp_desc, str):
                errors.extend(check_latex_and_templates(comp_desc, comp_id, "competency.description"))

    questions = data.get("questions")
    if not isinstance(questions, list):
        return errors

    for q in questions:
        if not isinstance(q, dict):
            continue
        q_id = q.get("id", "UNKNOWN")
        itype = q.get("interaction_type")
        options = q.get("options")

        # --- Rule R-20: LaTeX Syntax in question text fields ---
        if isinstance(q.get("stem"), str):
            errors.extend(check_latex_and_templates(q["stem"], q_id, "stem"))

        hints = q.get("hints")
        if isinstance(hints, list):
            for i, h in enumerate(hints):
                if isinstance(h, str):
                    errors.extend(check_latex_and_templates(h, q_id, f"hints[{i}]"))
                elif isinstance(h, dict):
                    for sub_k in ("text", "content", "hint"):
                        sub_val = h.get(sub_k)
                        if isinstance(sub_val, str):
                            errors.extend(check_latex_and_templates(sub_val, q_id, f"hints[{i}].{sub_k}"))

        sol = q.get("solution")
        if isinstance(sol, str):
            errors.extend(check_latex_and_templates(sol, q_id, "solution"))
        det_sol = q.get("detailed_solution")
        if isinstance(det_sol, str) and det_sol != sol:
            errors.extend(check_latex_and_templates(det_sol, q_id, "detailed_solution"))

        misc = q.get("misconception_warning")
        if isinstance(misc, str):
            errors.extend(check_latex_and_templates(misc, q_id, "misconception_warning"))
        comm_misc = q.get("common_misconception_warning")
        if isinstance(comm_misc, str) and comm_misc != misc:
            errors.extend(check_latex_and_templates(comm_misc, q_id, "common_misconception_warning"))

        # --- Rules R-17, R-18, R-20, R-22 on Options ---
        if isinstance(options, list):
            for i, opt in enumerate(options):
                if not isinstance(opt, dict):
                    continue
                opt_id = opt.get("id") or opt.get("option_id") or f"opt_{i}"
                opt_content = opt.get("content")
                is_correct = opt.get("is_correct")

                # R-20 on option content
                if isinstance(opt_content, str):
                    errors.extend(check_latex_and_templates(opt_content, q_id, f"options[{opt_id}].content"))

                # R-20 on option error_rationale
                err_rationale = opt.get("error_rationale")
                if isinstance(err_rationale, str):
                    errors.extend(check_latex_and_templates(err_rationale, q_id, f"options[{opt_id}].error_rationale"))

                # R-18: Meta-information giveaway in visible option content
                if isinstance(opt_content, str) and meta_giveaway_regex.search(opt_content):
                    errors.append(ValidationError(
                        rule_id="R-18",
                        code="ERR_META_GIVEAWAY",
                        message=f"Question '{q_id}': Option '{opt_id}' contains psychometric meta-information error giveaway in visible content: '{opt_content[:60]}...'",
                        item_id=q_id
                    ))

                # R-17 & R-22: Error rationales on distractors (is_correct is False)
                if is_correct is False:
                    rationale = opt.get("error_rationale")
                    if itype == "multiple_choice_7_options":
                        if rationale is None or (isinstance(rationale, str) and not rationale.strip()):
                            errors.append(ValidationError(
                                rule_id="R-17",
                                code="ERR_PLACEHOLDER_RATIONALE",
                                message=f"Question '{q_id}': Option '{opt_id}' with is_correct=False must have a non-empty, descriptive 'error_rationale'",
                                item_id=q_id
                            ))
                        elif is_placeholder_rationale(rationale):
                            errors.append(ValidationError(
                                rule_id="R-17",
                                code="ERR_PLACEHOLDER_RATIONALE",
                                message=f"Question '{q_id}': Option '{opt_id}' contains a generic placeholder 'error_rationale': '{rationale}'",
                                item_id=q_id
                            ))
                    elif itype == "multiple_select":
                        if rationale is None or (isinstance(rationale, str) and not rationale.strip()):
                            errors.append(ValidationError(
                                rule_id="R-22",
                                code="ERR_MS_MISSING_RATIONALE",
                                message=f"Question '{q_id}': Option '{opt_id}' in multiple_select with is_correct=False must include diagnostic 'error_rationale'",
                                item_id=q_id
                            ))
                        elif is_placeholder_rationale(rationale):
                            errors.append(ValidationError(
                                rule_id="R-17",
                                code="ERR_PLACEHOLDER_RATIONALE",
                                message=f"Question '{q_id}': Option '{opt_id}' in multiple_select contains a generic placeholder 'error_rationale': '{rationale}'",
                                item_id=q_id
                            ))

        # --- Rule R-19: Answer Leak in fill_in_the_blank ---
        if itype == "fill_in_the_blank":
            stem = q.get("stem")
            ans = q.get("correct_answer")
            if isinstance(stem, str) and ans is not None:
                candidate_answers: list[str] = []
                if isinstance(ans, (int, float)) and not isinstance(ans, bool):
                    candidate_answers.append(str(ans))
                elif isinstance(ans, str):
                    candidate_answers.append(ans)
                elif isinstance(ans, list):
                    for item in ans:
                        if isinstance(item, (int, float)) and not isinstance(item, bool):
                            candidate_answers.append(str(item))
                        elif isinstance(item, str):
                            candidate_answers.append(item)
                elif isinstance(ans, dict):
                    val = ans.get("value")
                    expr = ans.get("expression")
                    if isinstance(val, (int, float)) and not isinstance(val, bool):
                        candidate_answers.append(str(val))
                    elif isinstance(val, str):
                        candidate_answers.append(val)
                    elif isinstance(val, list):
                        for item in val:
                            if isinstance(item, (int, float)) and not isinstance(item, bool):
                                candidate_answers.append(str(item))
                            elif isinstance(item, str):
                                candidate_answers.append(item)
                    if isinstance(expr, str):
                        candidate_answers.append(expr)

                for cand in candidate_answers:
                    clean_cand = cand.strip().strip("$").strip()
                    if not clean_cand:
                        continue
                    escaped_cand = re.escape(clean_cand)
                    leak_pattern = re.compile(
                        rf"(?:=\s*|\bes\s+(?:igual\s+a\s+)?)\$?{escaped_cand}\$?(?=[^0-9a-zA-Z]|$)",
                        re.IGNORECASE
                    )
                    if leak_pattern.search(stem):
                        errors.append(ValidationError(
                            rule_id="R-19",
                            code="ERR_ANSWER_LEAK",
                            message=f"Question '{q_id}': Stem explicitly leaks the correct answer '{clean_cand}' as '= {clean_cand}' or 'es {clean_cand}'",
                            item_id=q_id
                        ))
                        break

    return errors
