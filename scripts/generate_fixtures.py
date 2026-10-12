"""Fixture generator for the 28 acceptance test fixtures."""
from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path

FIXTURES_DIR = Path("courses/fixtures")
TEST_FIXTURES_DIR = Path("tests/validator/fixtures")


def make_mc_question(q_id: str, comp_id: str = "Hab-01", correct_len: int = 105) -> dict:
    """Generates a standard valid 7-option MC item with distractors of lengths 80..130."""
    # Distractor lengths: 80, 90, 100, 110, 120, 130
    distractor_lengths = [80, 90, 100, 110, 120, 130]

    def pad(text: str, target_len: int) -> str:
        if len(text) >= target_len:
            return text[:target_len]
        return text + " " + ("x" * (target_len - len(text) - 1))

    options = [
        {
            "id": "opt_a",
            "option_id": "A",
            "content": pad(f"Distractor A para {q_id}", distractor_lengths[0]),
            "is_correct": False,
            "error_rationale": "Razonamiento del error A para analisis cualitativo."
        },
        {
            "id": "opt_b",
            "option_id": "B",
            "content": pad(f"Distractor B para {q_id}", distractor_lengths[1]),
            "is_correct": False,
            "error_rationale": "Razonamiento del error B para analisis cualitativo."
        },
        {
            "id": "opt_c",
            "option_id": "C",
            "content": pad(f"Respuesta correcta C para {q_id}", correct_len),
            "is_correct": True,
            "error_rationale": None
        },
        {
            "id": "opt_d",
            "option_id": "D",
            "content": pad(f"Distractor D para {q_id}", distractor_lengths[2]),
            "is_correct": False,
            "error_rationale": "Razonamiento del error D para analisis cualitativo."
        },
        {
            "id": "opt_e",
            "option_id": "E",
            "content": pad(f"Distractor E para {q_id}", distractor_lengths[3]),
            "is_correct": False,
            "error_rationale": "Razonamiento del error E para analisis cualitativo."
        },
        {
            "id": "opt_f",
            "option_id": "F",
            "content": pad(f"Distractor F para {q_id}", distractor_lengths[4]),
            "is_correct": False,
            "error_rationale": "Razonamiento del error F para analisis cualitativo."
        },
        {
            "id": "opt_g",
            "option_id": "G",
            "content": pad(f"Distractor G para {q_id}", distractor_lengths[5]),
            "is_correct": False,
            "error_rationale": "Razonamiento del error G para analisis cualitativo."
        }
    ]

    return {
        "id": q_id,
        "competency_id": comp_id,
        "bloom_taxonomy_level": "Analyze",
        "difficulty": "medium",
        "interaction_type": "multiple_choice_7_options",
        "context_application": f"Analisis cualitativo del sistema lineal en item {q_id}",
        "stem": f"Considere el sistema dinamico $\\dot{{x}} = Ax$ para el item {q_id}. Si $\\text{{tr}}(A) < 0$, $\\det(A) > 0$ y $\\Delta < 0$, ¿cual es la estabilidad?",
        "interface_config": {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "single_selection",
            "grading_policy": "single_choice"
        },
        "options": options,
        "correct_answer": "C",
        "hints": [
            f"Primer paso de andamiaje analitico para resolver {q_id}.",
            f"Segundo paso: evaluar los signos de la traza y el determinante para {q_id}.",
            f"Tercer paso: verificar el discriminante espectral para {q_id}."
        ],
        "detailed_solution": f"Solucion paso a paso analitica del ejercicio {q_id}. Se calculan autovalores complejos conjugados con parte real negativa.",
        "common_misconception_warning": f"Advertencia sobre misconception comun en {q_id}: no confundir foco estable con centro conservativo."
    }


def make_ms_question(q_id: str, comp_id: str = "Hab-01") -> dict:
    """Generates a valid multiple-select question (5 options, 2 correct)."""
    options = [
        {"id": "opt_a", "option_id": "A", "content": f"Propiedad espectral A verificada en {q_id}", "is_correct": True, "error_rationale": None},
        {"id": "opt_b", "option_id": "B", "content": f"Propiedad espectral B verificada en {q_id}", "is_correct": True, "error_rationale": None},
        {"id": "opt_c", "option_id": "C", "content": f"Afirmacion incorrecta C para {q_id}", "is_correct": False, "error_rationale": "Falla la condicion de signo."},
        {"id": "opt_d", "option_id": "D", "content": f"Afirmacion incorrecta D para {q_id}", "is_correct": False, "error_rationale": "Confunde parte real con imaginaria."},
        {"id": "opt_e", "option_id": "E", "content": f"Afirmacion incorrecta E para {q_id}", "is_correct": False, "error_rationale": "Determinante nulo."}
    ]
    return {
        "id": q_id,
        "competency_id": comp_id,
        "bloom_taxonomy_level": "Understand",
        "difficulty": "medium",
        "interaction_type": "multiple_select",
        "context_application": f"Seleccion multiple de invariantes en {q_id}",
        "stem": f"Seleccione todas las afirmaciones verdaderas respecto a la matriz del sistema en {q_id}:",
        "interface_config": {
            "allow_calculator": False,
            "input_placeholder": None,
            "expected_format": "multiple_selection",
            "grading_policy": "binary_all_or_nothing"
        },
        "options": options,
        "correct_answer": ["A", "B"],
        "hints": [
            f"Analice cada afirmacion de manera independiente para {q_id}.",
            f"Verifique las relaciones entre traza y determinante para {q_id}.",
            f"Compruebe que exactamente dos opciones satisfacen los teoremas para {q_id}."
        ],
        "detailed_solution": f"Solucion paso a paso para seleccion multiple en {q_id}.",
        "common_misconception_warning": f"Misconception en seleccion multiple {q_id}."
    }


def make_fitb_question(q_id: str, comp_id: str = "Hab-01") -> dict:
    """Generates a valid fill-in-the-blank question."""
    return {
        "id": q_id,
        "competency_id": comp_id,
        "bloom_taxonomy_level": "Apply",
        "difficulty": "hard",
        "interaction_type": "fill_in_the_blank",
        "context_application": f"Calculo simbolico en {q_id}",
        "stem": f"Ingrese la expresion simplificada del multiplicador de ajuste para el ejercicio {q_id}:",
        "graph": {
            "title": "Diagrama de Fase en el Plano",
            "x_axis": {"label": "$Y$", "min": -10, "max": 10, "step": 2},
            "y_axis": {"label": "$r$", "min": -10, "max": 10, "step": 2},
            "curves": [
                {"id": "is_curve", "fn": "-0.5*x + 4", "label": "Curva IS", "color": "#1f77b4", "style": "solid"}
            ],
            "points": [
                {"x": 2, "y": 3, "style": "closed", "label": "Equilibrio $E^*$", "color": "#2ca02c"}
            ]
        },
        "interface_config": {
            "allow_calculator": True,
            "input_placeholder": "1 - (alpha + n)*sigma",
            "expected_format": "algebraic_expression",
            "grading_policy": "single_choice"
        },
        "options": [],
        "correct_answer": {
            "value": "1 - (alpha + n)*sigma",
            "canonical_algebraic": "1 - (alpha + n)*sigma",
            "accepted_equivalents": [
                "1 - alpha*sigma - n*sigma",
                "1 - sigma*(alpha + n)"
            ]
        },
        "hints": [
            f"Pista 1: Agrupe los terminos proporcionales a $\\sigma$ en {q_id}.",
            f"Pista 2: Aplique la propiedad distributiva en el denominador para {q_id}.",
            f"Pista 3: La forma canonica factorizada es $1 - (\\alpha + n)\\sigma$ para {q_id}."
        ],
        "detailed_solution": f"Solucion analitica detallada de {q_id}.",
        "common_misconception_warning": f"Misconception tipica en {q_id}."
    }


def generate_base_course(q_count: int = 30, comp_id: str = "Hab-01", category: str = "Skill") -> dict:
    """Builds a complete, valid base course with q_count questions."""
    questions = []
    # Mix of questions: mostly MC, with some MS and FITB
    for i in range(1, q_count + 1):
        q_id = f"Q-{i:03d}"
        if i == 25 or i == 26:
            questions.append(make_ms_question(q_id, comp_id=comp_id))
        elif i == 27 or i == 28:
            questions.append(make_fitb_question(q_id, comp_id=comp_id))
        else:
            questions.append(make_mc_question(q_id, comp_id=comp_id, correct_len=105))

    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "schema_version": "1.0.0",
        "course_id": "demo",
        "course_title": "Curso de Demostracion y Validacion Psicometrica",
        "description": "Banco de ejercicios canonico y completo para validacion del sistema Top's Academy.",
        "language": "es",
        "created_at": "2026-10-11T00:00:00Z",
        "competencies": [
            {
                "id": comp_id,
                "code": "HAB-01",
                "name": "Analisis Cualitativo de Sistemas Dinamicos Planos",
                "category": category,
                "description": "Determinacion de estabilidad asintotica y retratos de fase en sistemas bidimensionales.",
                "mastery_target": 100
            }
        ],
        "questions": questions
    }


def generate_all_fixtures() -> None:
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    TEST_FIXTURES_DIR.mkdir(parents=True, exist_ok=True)

    base = generate_base_course(q_count=30)

    # 01_original_example_unmodified.json
    shutil.copyfile("system_prompts/output_example_exercises.json", FIXTURES_DIR / "01_original_example_unmodified.json")

    # 02_syntax_malformed_json.json
    raw_valid = json.dumps(base, indent=2, ensure_ascii=False)
    # Remove closing braces to create malformed JSON
    (FIXTURES_DIR / "02_syntax_malformed_json.json").write_text(raw_valid[:-10], encoding="utf-8")

    # 03_syntax_unescaped_quotes.json
    c03 = copy.deepcopy(base)
    c03_str = json.dumps(c03, indent=2, ensure_ascii=False)
    # Inject unescaped quote inside string
    c03_bad = c03_str.replace('"stem": "Considere el sistema', '"stem": "Considere "el" sistema')
    (FIXTURES_DIR / "03_syntax_unescaped_quotes.json").write_text(c03_bad, encoding="utf-8")

    # 04_syntax_raw_newlines.json
    c04 = copy.deepcopy(base)
    c04_str = json.dumps(c04, indent=2, ensure_ascii=False)
    # Inject raw unescaped newline character inside string literal
    c04_bad = c04_str.replace('"stem": "Considere el sistema', '"stem": "Considere el\nsistema')
    (FIXTURES_DIR / "04_syntax_raw_newlines.json").write_text(c04_bad, encoding="utf-8")

    # 05_latex_invalid_escape.json (\alpha)
    c05 = copy.deepcopy(base)
    c05["questions"][0]["stem"] = r"Considere el parametro $\alpha$ de ajuste espectral."
    c05_str = json.dumps(c05, indent=2, ensure_ascii=False)
    c05_bad = c05_str.replace(r"\\alpha", r"\alpha")
    (FIXTURES_DIR / "05_latex_invalid_escape.json").write_text(c05_bad, encoding="utf-8")

    # 06_latex_silent_corruption_tab.json (\tau)
    c06 = copy.deepcopy(base)
    c06["questions"][0]["stem"] = r"Considere la tasa impositiva $\tau$ del modelo."
    c06_str = json.dumps(c06, indent=2, ensure_ascii=False)
    c06_bad = c06_str.replace(r"\\tau", r"\tau")
    (FIXTURES_DIR / "06_latex_silent_corruption_tab.json").write_text(c06_bad, encoding="utf-8")

    # 07_latex_silent_corruption_formfeed.json (\frac)
    c07 = copy.deepcopy(base)
    c07["questions"][0]["stem"] = r"Considere la fraccion $\frac{1}{2}$ del determinante."
    c07_str = json.dumps(c07, indent=2, ensure_ascii=False)
    c07_bad = c07_str.replace(r"\\frac", r"\frac")
    (FIXTURES_DIR / "07_latex_silent_corruption_formfeed.json").write_text(c07_bad, encoding="utf-8")

    # 08_latex_silent_corruption_backspace.json (\beta)
    c08 = copy.deepcopy(base)
    c08["questions"][0]["stem"] = r"Considere la elasticidad $\beta$ del producto."
    c08_str = json.dumps(c08, indent=2, ensure_ascii=False)
    c08_bad = c08_str.replace(r"\\beta", r"\beta")
    (FIXTURES_DIR / "08_latex_silent_corruption_backspace.json").write_text(c08_bad, encoding="utf-8")

    # 09_schema_missing_course_title.json
    c09 = copy.deepcopy(base)
    del c09["course_title"]
    (FIXTURES_DIR / "09_schema_missing_course_title.json").write_text(json.dumps(c09, indent=2, ensure_ascii=False), encoding="utf-8")

    # 10_duplicate_competency_ids.json
    c10 = copy.deepcopy(base)
    c10["competencies"].append({
        "id": "Hab-01",
        "code": "HAB-01-DUP",
        "name": "Competencia duplicada",
        "category": "Skill",
        "description": "Descripcion de prueba para duplicado."
    })
    (FIXTURES_DIR / "10_duplicate_competency_ids.json").write_text(json.dumps(c10, indent=2, ensure_ascii=False), encoding="utf-8")

    # 11_duplicate_question_ids.json
    c11 = copy.deepcopy(base)
    c11["questions"][1]["id"] = "Q-001"
    (FIXTURES_DIR / "11_duplicate_question_ids.json").write_text(json.dumps(c11, indent=2, ensure_ascii=False), encoding="utf-8")

    # 12_missing_competency_reference.json
    c12 = copy.deepcopy(base)
    c12["questions"][0]["competency_id"] = "Hab-99"
    (FIXTURES_DIR / "12_missing_competency_reference.json").write_text(json.dumps(c12, indent=2, ensure_ascii=False), encoding="utf-8")

    # 13_skill_29_questions.json
    c13 = generate_base_course(q_count=29, comp_id="Hab-01", category="Skill")
    (FIXTURES_DIR / "13_skill_29_questions.json").write_text(json.dumps(c13, indent=2, ensure_ascii=False), encoding="utf-8")

    # 14_concept_19_questions.json
    c14 = generate_base_course(q_count=19, comp_id="C-01", category="Concept")
    (FIXTURES_DIR / "14_concept_19_questions.json").write_text(json.dumps(c14, indent=2, ensure_ascii=False), encoding="utf-8")

    # 15_fact_19_questions.json
    c15 = generate_base_course(q_count=19, comp_id="H-01", category="Fact")
    (FIXTURES_DIR / "15_fact_19_questions.json").write_text(json.dumps(c15, indent=2, ensure_ascii=False), encoding="utf-8")

    # 16_mc_6_options.json
    c16 = copy.deepcopy(base)
    c16["questions"][0]["options"] = c16["questions"][0]["options"][:6]
    (FIXTURES_DIR / "16_mc_6_options.json").write_text(json.dumps(c16, indent=2, ensure_ascii=False), encoding="utf-8")

    # 17_mc_8_options.json
    c17 = copy.deepcopy(base)
    extra_opt = copy.deepcopy(c17["questions"][0]["options"][0])
    extra_opt["option_id"] = "H"
    extra_opt["id"] = "opt_h"
    extra_opt["content"] = "Opcion adicional H para ocho opciones."
    c17["questions"][0]["options"].append(extra_opt)
    (FIXTURES_DIR / "17_mc_8_options.json").write_text(json.dumps(c17, indent=2, ensure_ascii=False), encoding="utf-8")

    # 18_mc_0_correct.json
    c18 = copy.deepcopy(base)
    for opt in c18["questions"][0]["options"]:
        opt["is_correct"] = False
    (FIXTURES_DIR / "18_mc_0_correct.json").write_text(json.dumps(c18, indent=2, ensure_ascii=False), encoding="utf-8")

    # 19_mc_2_correct.json
    c19 = copy.deepcopy(base)
    c19["questions"][0]["options"][0]["is_correct"] = True
    c19["questions"][0]["options"][1]["is_correct"] = True
    for opt in c19["questions"][0]["options"][2:]:
        opt["is_correct"] = False
    (FIXTURES_DIR / "19_mc_2_correct.json").write_text(json.dumps(c19, indent=2, ensure_ascii=False), encoding="utf-8")

    # 20_ms_all_correct.json
    c20 = copy.deepcopy(base)
    ms_q = next(q for q in c20["questions"] if q["interaction_type"] == "multiple_select")
    ms_q["id"] = "Q-001"
    for opt in ms_q["options"]:
        opt["is_correct"] = True
    c20["questions"] = [ms_q] + [q for q in c20["questions"] if q["id"] != ms_q["id"] and q["id"] != "Q-001"]
    (FIXTURES_DIR / "20_ms_all_correct.json").write_text(json.dumps(c20, indent=2, ensure_ascii=False), encoding="utf-8")

    # 21_ms_0_correct.json
    c21 = copy.deepcopy(base)
    ms_q = next(q for q in c21["questions"] if q["interaction_type"] == "multiple_select")
    ms_q["id"] = "Q-001"
    for opt in ms_q["options"]:
        opt["is_correct"] = False
    c21["questions"] = [ms_q] + [q for q in c21["questions"] if q["id"] != ms_q["id"] and q["id"] != "Q-001"]
    (FIXTURES_DIR / "21_ms_0_correct.json").write_text(json.dumps(c21, indent=2, ensure_ascii=False), encoding="utf-8")

    # 22_hints_2_hints.json
    c22 = copy.deepcopy(base)
    c22["questions"][0]["hints"] = c22["questions"][0]["hints"][:2]
    (FIXTURES_DIR / "22_hints_2_hints.json").write_text(json.dumps(c22, indent=2, ensure_ascii=False), encoding="utf-8")

    # 23_hints_6_hints.json
    c23 = copy.deepcopy(base)
    c23["questions"][0]["hints"] = c23["questions"][0]["hints"] + [
        "Pista 4 adicional para el item.",
        "Pista 5 adicional para el item.",
        "Pista 6 adicional que excede el limite maximo."
    ]
    (FIXTURES_DIR / "23_hints_6_hints.json").write_text(json.dumps(c23, indent=2, ensure_ascii=False), encoding="utf-8")

    # 24_giveaway_item_too_long.json (correct option 35% longer than max distractor 100 -> 135)
    c24 = copy.deepcopy(base)
    # Distractors: max distractor is 100
    for i, opt in enumerate(c24["questions"][0]["options"]):
        if not opt["is_correct"]:
            opt["content"] = "Distractor con longitud exacta de cien caracteres para prueba de giveaway psicometrico en item."[:100]
        else:
            # 135 chars is 35% longer than 100
            opt["content"] = ("Respuesta correcta deliberadamente extendida para violar la regla de simetria de longitud "
                              "en mas del veinte por ciento alcanzando 135 chars!")[:135]
    (FIXTURES_DIR / "24_giveaway_item_too_long.json").write_text(json.dumps(c24, indent=2, ensure_ascii=False), encoding="utf-8")

    # 25_giveaway_item_too_short.json (correct option 30% shorter than min distractor 100 -> 70)
    c25 = copy.deepcopy(base)
    for i, opt in enumerate(c25["questions"][0]["options"]):
        if not opt["is_correct"]:
            opt["content"] = "Distractor con longitud exacta de cien caracteres para prueba de giveaway psicometrico en item."[:100]
        else:
            # 70 chars is 30% shorter than 100
            opt["content"] = "Respuesta correcta muy corta setenta carac!"[:70]
    (FIXTURES_DIR / "25_giveaway_item_too_short.json").write_text(json.dumps(c25, indent=2, ensure_ascii=False), encoding="utf-8")

    # 26_giveaway_course_longest_30pct.json (correct longest in 3/10 items = 30%)
    # Let's make a course with 30 questions (to satisfy min question count R-08), where 10 are MC and 20 are FITB.
    # In the 10 MC questions, exactly 3 have correct as longest (e.g. correct 125 vs max distractor 120 -> +4.2% <= 20% so item rule passes).
    # In the other 7 MC questions, correct is 105 (strictly between min distractor 80 and max distractor 130).
    c26 = generate_base_course(q_count=30)
    # Replace questions 0..9 with 10 MC items
    for idx in range(10):
        q_id = f"Q-{idx+1:03d}"
        if idx < 3:
            # Longest: distractor max is 120, correct is 125
            c26["questions"][idx] = make_mc_question(q_id, correct_len=125)
            # Ensure max distractor is 120
            for opt in c26["questions"][idx]["options"]:
                if not opt["is_correct"] and len(opt["content"]) > 120:
                    opt["content"] = opt["content"][:120]
        else:
            # Neither longest nor shortest: correct is 105, min dist 80, max dist 130
            c26["questions"][idx] = make_mc_question(q_id, correct_len=105)
    # Replace remaining questions 10..29 with FITB items so they don't count towards MC stats
    for idx in range(10, 30):
        c26["questions"][idx] = make_fitb_question(f"Q-{idx+1:03d}")
    (FIXTURES_DIR / "26_giveaway_course_longest_30pct.json").write_text(json.dumps(c26, indent=2, ensure_ascii=False), encoding="utf-8")

    # 27_giveaway_course_shortest_30pct.json (correct shortest in 3/10 items = 30%)
    c27 = generate_base_course(q_count=30)
    for idx in range(10):
        q_id = f"Q-{idx+1:03d}"
        if idx < 3:
            # Shortest: min distractor is 90, correct is 85 (-5.6% <= 20%, so item rule passes)
            c27["questions"][idx] = make_mc_question(q_id, correct_len=85)
            for opt in c27["questions"][idx]["options"]:
                if not opt["is_correct"] and len(opt["content"]) < 90:
                    opt["content"] = opt["content"].ljust(90, "y")
        else:
            c27["questions"][idx] = make_mc_question(q_id, correct_len=105)
    for idx in range(10, 30):
        c27["questions"][idx] = make_fitb_question(f"Q-{idx+1:03d}")
    (FIXTURES_DIR / "27_giveaway_course_shortest_30pct.json").write_text(json.dumps(c27, indent=2, ensure_ascii=False), encoding="utf-8")

    # 28_valid_complete_course.json (Passes 100%)
    c28 = copy.deepcopy(base)
    (FIXTURES_DIR / "28_valid_complete_course.json").write_text(json.dumps(c28, indent=2, ensure_ascii=False), encoding="utf-8")

    # Copy all fixtures into tests/validator/fixtures as well
    for f in FIXTURES_DIR.glob("*.json"):
        shutil.copyfile(f, TEST_FIXTURES_DIR / f.name)

    print(f"Successfully generated 28 fixtures in {FIXTURES_DIR} and {TEST_FIXTURES_DIR}")


if __name__ == "__main__":
    generate_all_fixtures()
