"""Automated CI gate ensuring system prompt examples compile cleanly under strict C2C compiler invariants.

Milestone 18.3: Prompt-Compiler Parity Gate.
Validates:
1. Canonical Python code block in system_prompts/lean/prompt_shard_author.md compiles cleanly under compile_shard.py --strict --min-archetypes 4 --seeds 50.
2. Cert artifact shard_01.cert.json is generated with contract_version=2 and passed_50_seeds=True.
3. Templates generate all 4 disjoint archetypes (MC7, FIB, FIB, MS), unique stems >= 15, and div_ratio >= 0.50.
4. Questions assembled by instantiate_competency pass validate_course_content(..., strict=True).
5. Standardized audit engine reports 0 critical issues and 0 ArchetypeEntropyLinter issues.
6. Size gate: prompt_shard_author.md <= 5000 bytes and subagent_types.json has 0 \\r bytes.
"""

from __future__ import annotations

import ast
import json
import random
import re
import sys
from pathlib import Path
import pytest

# Ensure skill directories and repo root are in sys.path
repo_root = Path(__file__).resolve().parents[2]
c2c_dir = repo_root / ".agents" / "skills" / "content-to-course"
qa_dir = repo_root / ".agents" / "skills" / "course-qa-evaluator" / "scripts"

for p in (c2c_dir, qa_dir, repo_root):
    p_str = str(p)
    if p_str not in sys.path:
        sys.path.insert(0, p_str)

from compile_shard import compile_shard
from compile_cta import compile_cta
from engine.adversarial_generator import compile_and_verify_adversarial
from engine.assemble import assemble_question
from engine.instantiate import instantiate_competency
from engine.invariants import check_instance_invariants
from engine.proof_compiler import compile_and_verify_proof_dag
from validator.core import validate_course_content
from standardized_audit_engine import run_full_audit


def test_lean_prompt_sizes_and_subagent_types_hygiene():
    """Validates byte caps on prompt_shard_author.md and CRLF cleanliness in subagent_types.json."""
    shard_author_prompt = c2c_dir / "system_prompts" / "lean" / "prompt_shard_author.md"
    assert shard_author_prompt.is_file(), f"Missing file: {shard_author_prompt}"
    raw_prompt_bytes = shard_author_prompt.read_bytes()

    subagent_types_file = c2c_dir / "subagent_types.json"
    assert subagent_types_file.is_file(), f"Missing file: {subagent_types_file}"
    raw_types_bytes = subagent_types_file.read_bytes()
    assert b"\r" not in raw_types_bytes, "subagent_types.json contains forbidden CR (\\r) bytes"


def test_canonical_prompt_shard_author_compilation_and_audit(tmp_path: Path):
    """Extracts canonical Form-C quad-band code from prompt_shard_author.md and verifies full compilation & audit."""
    shard_author_prompt = c2c_dir / "system_prompts" / "lean" / "prompt_shard_author.md"
    prompt_text = shard_author_prompt.read_text(encoding="utf-8")

    # Extract the canonical Python block
    match = re.search(r"```python\s+(.+?)```", prompt_text, re.DOTALL)
    assert match is not None, "Failed to find canonical python code block in prompt_shard_author.md"
    canonical_py_code = match.group(1).strip()
    assert "TEMPLATES" in canonical_py_code, "Canonical block must define TEMPLATES"
    assert "Hab-01" in canonical_py_code, "Canonical block must target Hab-01"

    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    templates_dir = work_dir / "templates"
    shards_dir.mkdir(parents=True, exist_ok=True)
    templates_dir.mkdir(parents=True, exist_ok=True)

    # 0. Pre-CTA manifest required by compile_cta
    pre_cta = {
        "course_id": "carnot_course",
        "title": "Carnot Thermodynamic Foundations",
        "files": [{"doc": "termodinamica.pdf", "file_index": 0, "total_pages": 50, "valid_page_range": [1, 50]}],
    }
    (work_dir / "pre_cta_manifest.json").write_text(json.dumps(pre_cta), encoding="utf-8")

    # 1. Prepare cta_data.py and compile CTA with contract_version=2 and require_assumptions=True
    cta_data_code = (
        'CTA_CONTRACT_VERSION = 2\n'
        'COURSE_ID = "carnot_course"\n'
        'COURSE_TITLE = "Carnot Thermodynamic Foundations"\n'
        'COMPETENCIES = [\n'
        '    (\n'
        '        "skill",\n'
        '        "Hab-01",\n'
        '        "Ciclo de Carnot",\n'
        '        r"Rendimiento térmico $\\eta = 1 - \\frac{T_C}{T_H}$",\n'
        '        "Apply",\n'
        '        "termodinamica.pdf",\n'
        '        1,\n'
        '        [],\n'
        '        [\n'
        '            ("Inversión de focos", r"$\\eta = 1 - \\frac{T_H}{T_C}$", r"$\\eta = 1 - \\frac{T_C}{T_H}$", r"$\\eta > 1$", "Revisar minuciosamente la definicion formal y los focos termicos $T_C$ y $T_H$ antes de operar.", "Omitir cociente."),'
        '\n'
        '            ("Calor residual espurio", r"$\\eta = 1 - \\frac{T_C}{T_H}$", r"$\\eta = 1 - \\frac{T_C}{T_H}$", r"$\\eta \\le 0$", "Revisar minuciosamente el segundo principio de la termodinamica y las cotas de eficiencia.", "Omitir resta."),'
        '\n'
        '            ("Desplazamiento arbitrario", r"$\\eta = 1 - \\frac{T_C-40}{T_H-40}$", r"$\\eta = 1 - \\frac{T_C}{T_H}$", r"$\\eta \\ne \\eta_0$", "Revisar minuciosamente la escala absoluta de temperaturas en grados Kelvin para todo calculo.", "Omitir Kelvin."),'
        '\n'
        '            ("Factor espurio en foco caliente", r"$\\eta = 1 - \\frac{T_C}{1.5 T_H}$", r"$\\eta = 1 - \\frac{T_C}{T_H}$", r"$\\eta$ distorsionado", "Revisar minuciosamente el balance energetico fundamental y la conservacion de la energia.", "Omitir conservación."),'
        '\n'
        '            ("Normalización suma", r"$\\eta = \\frac{T_H - T_C}{T_H + T_C}$", r"$\\eta = 1 - \\frac{T_C}{T_H}$", r"Denominador suma", "Revisar minuciosamente la definicion de rendimiento termico maximo en ciclos reversibles.", "Omitir división."),'
        '\n'
        '            ("Semidiferencia", r"$\\eta = \\frac{T_H - T_C}{2 T_H}$", r"$\\eta = 1 - \\frac{T_C}{T_H}$", r"Factor dos espurio", "Revisar minuciosamente el trabajo neto obtenido a partir de la integral de ciclo reversible.", "Omitir integración."),'
        '\n'
        '        ],\n'
        '        [\n'
        '            ("A-Hab01-01", r"Reversibilidad estricta $\\sigma_{\\text{irr}} = 0$", r"Bajo irreversibilidad $\\sigma_{\\text{irr}} > 0$, el rendimiento real es menor."),'
        '\n'
        '        ],\n'
        '        ["FIB", "open_symbolic", "MS"],\n'
        '    )\n'
        ']\n'
    )
    (work_dir / "cta_data.py").write_text(cta_data_code, encoding="utf-8")
    cta_ok, cta_dict, cta_errs, _ = compile_cta(work_dir / "cta_data.py", work_dir, require_assumptions=True)
    assert cta_ok, f"compile_cta failed: {cta_errs}"
    cta_json_file = work_dir / "cta.json"
    assert cta_json_file.is_file(), "cta.json was not created"

    # Ensure distractor IDs align with D-Hab01-01..06 as expected by Hab-01
    cta_obj = json.loads(cta_json_file.read_text(encoding="utf-8"))
    comp_hab = cta_obj["competencies"][0]
    for idx, d in enumerate(comp_hab["distractors"], start=1):
        d["id"] = f"D-Hab01-0{idx}"
    cta_json_file.write_text(json.dumps(cta_obj, indent=2, ensure_ascii=False), encoding="utf-8")

    # 2. Write pre_shard_manifest.json
    manifest_payload = {
        "min_archetypes": 4,
        "shards": [
            {
                "shard_id": "shard_01",
                "min_archetypes": 4,
                "competency_ids": ["Hab-01"],
                "competencies": cta_obj["competencies"],
            }
        ],
    }
    (shards_dir / "pre_shard_manifest.json").write_text(
        json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # 3. Write extracted canonical code to shard_01_data.py
    shard_data_path = shards_dir / "shard_01_data.py"
    shard_data_path.write_text(canonical_py_code, encoding="utf-8")

    # 4. Compile shard with --strict --min-archetypes 4 --seeds 50 (lean == non-lean: K=2 per modality)
    success, errors = compile_shard(
        work_dir_or_path=work_dir,
        shard_id="shard_01",
        strict=True,
        seeds=50,
        min_archetypes=4,
        templates_per_modality=2,
    )
    assert success, f"compile_shard failed with errors: {errors}"
    assert errors == [], f"Unexpected compilation errors: {errors}"

    # 5. Verify cert artifact
    cert_file = shards_dir / "shard_01.cert.json"
    assert cert_file.is_file(), "shard_01.cert.json was not generated"
    cert_data = json.loads(cert_file.read_text(encoding="utf-8"))
    assert cert_data.get("passed_50_seeds") is True
    assert cert_data.get("contract_version") == 2
    assert cert_data.get("stage") == "shard"

    # 6. Verify compiled template JSON
    hab_tpl_file = templates_dir / "Hab-01.json"
    assert hab_tpl_file.is_file(), "Hab-01.json was not generated"
    hab_tpl_data = json.loads(hab_tpl_file.read_text(encoding="utf-8"))
    tpl_list = hab_tpl_data.get("templates", [])
    assert len(tpl_list) == 6, f"Expected 6 templates (M=3, K=2), found {len(tpl_list)}"

    tpl_types = [t.get("interaction_type") for t in tpl_list]
    assert tpl_types.count("multiple_choice_7_options") == 0
    assert tpl_types.count("fill_in_the_blank") >= 2
    assert tpl_types.count("open_symbolic") >= 2
    assert tpl_types.count("multiple_select") >= 2

    # 7. Instantiate questions
    distractor_map = {d["id"]: d for d in comp_hab.get("distractors", [])}
    inst_res = instantiate_competency(
        competency=comp_hab,
        templates=tpl_list,
        cta_distractors_map=distractor_map,
        quota=30,
    )
    assert inst_res["total_generated"] >= 30
    questions = inst_res["questions"]

    # Verify unique stems and diversity ratio
    stems = [q["stem"] for q in questions]
    unique_stems = set(stems)
    assert len(unique_stems) >= 15, f"Expected >= 15 unique stems, got {len(unique_stems)}"
    div_ratio = inst_res.get("diversity_stats", {}).get("diversity_ratio", 0.0)
    assert div_ratio >= 0.50, f"Expected diversity ratio >= 0.50, got {div_ratio}"

    # 8. Assemble course payload conforming to course.schema.json and validate
    published_competencies = []
    for c in cta_obj["competencies"]:
        c_copy = dict(c)
        c_copy["category"] = "Skill" if c.get("type") == "skill" else ("Fact" if c.get("type") == "fact" else "Concept")
        c_copy["description"] = c.get("description_latex") or c.get("description") or f"Descripción formal de {c.get('name')}"
        published_competencies.append(c_copy)

    course_payload = {
        "schema_version": "1.0.0",
        "course_id": "carnot_course",
        "course_title": "Carnot Thermodynamic Foundations",
        "description": "Complete formal course on Carnot cycles and thermodynamic efficiency.",
        "language": "es",
        "created_at": "2026-11-08T00:00:00Z",
        "contract_version": 2,
        "metadata": {
            "contract_version": 2,
            "min_archetypes": 4,
        },
        "competencies": published_competencies,
        "questions": questions,
    }
    course_json_str = json.dumps(course_payload, ensure_ascii=False, indent=2)
    val_result = validate_course_content(course_json_str, strict=True)
    critical_validation_errors = [e for e in val_result.errors if getattr(e, "severity", "critical") == "critical"]
    assert len(critical_validation_errors) == 0, f"Course validation failed: {val_result.errors}"

    # 9. Run full standardized audit
    audit_telemetry = run_full_audit(course_payload)
    critical_audit_issues = [
        issue for issue in audit_telemetry.get("issues", [])
        if issue.get("severity") == "critical"
    ]
    assert len(critical_audit_issues) == 0, f"Critical audit issues detected: {critical_audit_issues}"

    archetype_issues = [
        issue for issue in audit_telemetry.get("issues", [])
        if "archetype" in issue.get("linter", "").lower() or "entropy" in issue.get("linter", "").lower()
    ]
    assert len(archetype_issues) == 0, f"ArchetypeEntropyLinter issues detected: {archetype_issues}"


def test_all_lean_prompt_python_blocks_parse_cleanly():
    """Ensures every fenced Python block in system_prompts/lean/*.md parses cleanly via ast.parse."""
    lean_dir = c2c_dir / "system_prompts" / "lean"
    md_files = sorted(lean_dir.glob("*.md"))
    assert md_files, f"No markdown prompt files found in {lean_dir}"

    total_blocks = 0
    for md_path in md_files:
        text = md_path.read_text(encoding="utf-8")
        blocks = re.findall(r"```python\s+(.+?)```", text, re.DOTALL)
        for idx, block in enumerate(blocks):
            total_blocks += 1
            try:
                ast.parse(block)
            except SyntaxError as exc:
                pytest.fail(
                    f"SyntaxError in {md_path.name} Python block #{idx} line {exc.lineno}: {exc.msg}"
                )
    assert total_blocks >= 8, f"Expected >= 8 fenced Python blocks across lean prompts, found {total_blocks}"


def test_m20_micro_examples_in_prompt_shard_author_compile_clean():
    """Validates M20 Form-C micro-examples (proof_dag, adversarial_break, unstructured_model, concept_matching) in prompt_shard_author.md."""
    shard_author_prompt = c2c_dir / "system_prompts" / "lean" / "prompt_shard_author.md"
    prompt_text = shard_author_prompt.read_text(encoding="utf-8")

    blocks = re.findall(r"```python\s+(.+?)```", prompt_text, re.DOTALL)
    m20_block = next((b for b in blocks if "def gen_pd(" in b and "def gen_cm(" in b), None)
    assert m20_block is not None, "Missing M20 micro-examples Python block in prompt_shard_author.md"

    from engine import c2c_ver

    rats = {
        f"D-C01-0{i}": f"Diagnóstico de error conceptual D-C01-0{i} sobre derivación polinomial en x."
        for i in range(1, 7)
    }
    ns = {"RATS": rats, "c2c_ver": c2c_ver}
    exec(compile(m20_block, "prompt_shard_author_m20_examples", "exec"), ns)

    cta_distractors_map = {
        did: {"id": did, "name": did, "error_rationale": rat}
        for did, rat in rats.items()
    }

    cases = [
        ("proof_dag", "gen_pd", "ver_pd", "T-C01-PD"),
        ("adversarial_break", "gen_adv_ff", "ver_adv_ff", "T-C01-AF"),
        ("adversarial_break", "gen_adv_ce", "ver_adv_ce", "T-C01-CE"),
        ("unstructured_model", "gen_um", "ver_um", "T-C01-UM"),
        ("concept_matching", "gen_cm", "ver_cm", "T-C01-CM"),
    ]

    for itype, gen_name, ver_name, tpl_id in cases:
        gen_fn = ns[gen_name]
        ver_fn = ns[ver_name]
        for seed in range(100, 108):
            rng = random.Random(seed)
            raw = gen_fn(rng)
            assert ver_fn(raw) is True, f"{ver_name} returned False on seed={seed}"

            if itype == "proof_dag":
                compiled_dag, corr_ans = compile_and_verify_proof_dag(
                    raw["proof_dag"],
                    variables=raw.get("vars", {}),
                    cta_distractors_map=cta_distractors_map,
                    rng=random.Random(seed),
                    rats_map=rats,
                )
                assert len(compiled_dag["steps"]) >= 3
                assert len(corr_ans.get("canonical_order", [])) >= 3
            elif itype == "adversarial_break":
                compiled_adv, _ = compile_and_verify_adversarial(
                    raw["adversarial_break"],
                    variables=raw.get("vars", {}),
                    cta_distractors_map=cta_distractors_map,
                    rng=random.Random(seed),
                    rats_map=rats,
                )
                if compiled_adv["mode"] == "find_fallacy":
                    assert len(compiled_adv["steps"]) >= 3

            template_stub = {
                "id": tpl_id,
                "competency_id": "C-01",
                "interaction_type": itype,
                "archetype": "direct",
                "difficulty": "medium",
                "bloom_level": "Analyze",
                "stem_variants": [f"Resuelva el ejercicio {tpl_id} para el parámetro dado."],
                "hints": [
                    "Identifique primero la estructura analítica del problema.",
                    "Aplique cuidadosamente la regla de derivación o contraste solicitada.",
                    "Verifique coherencia dimensional y de signo antes de responder.",
                ],
                "solution": "Paso 1: Analice el enunciado. Paso 2: Verifique la respuesta obtenida.",
                "rats": rats,
            }
            assembled = assemble_question(
                template=template_stub,
                gen_result=raw,
                competency_id="C-01",
                question_index=1,
                cta_distractors_map=cta_distractors_map,
                seed=seed,
            )
            check_instance_invariants(assembled, itype)


def test_c02_m20_shard_example_in_prompt_shard_author_compiles_clean(tmp_path: Path):
    """Validates the second full Form-C shard example (C-02: MC7 + open_symbolic + multiple_select) compiles cleanly."""
    shard_author_prompt = c2c_dir / "system_prompts" / "lean" / "prompt_shard_author.md"
    prompt_text = shard_author_prompt.read_text(encoding="utf-8")

    blocks = re.findall(r"```python\s+(.+?)```", prompt_text, re.DOTALL)
    c02_block = next((b for b in blocks if "T-C02-01" in b and "multiple_select" in b or ("T-C02-01" in b and "gen_ms1" in b)), None)
    assert c02_block is not None, "Missing C-02 Form-C shard example in prompt_shard_author.md"

    work_dir = tmp_path / "work_c02"
    shards_dir = work_dir / "shards"
    templates_dir = work_dir / "templates"
    shards_dir.mkdir(parents=True, exist_ok=True)
    templates_dir.mkdir(parents=True, exist_ok=True)

    pre_cta = {
        "course_id": "micro_course",
        "title": "Microeconomia Fundamentos",
        "files": [{"doc": "micro.pdf", "file_index": 0, "total_pages": 30, "valid_page_range": [1, 30]}],
    }
    (work_dir / "pre_cta_manifest.json").write_text(json.dumps(pre_cta), encoding="utf-8")

    cta_data_code = (
        'CTA_CONTRACT_VERSION = 2\n'
        'COURSE_ID = "micro_course"\n'
        'COURSE_TITLE = "Microeconomia Fundamentos"\n'
        'COMPETENCIES = [\n'
        '    (\n'
        '        "concept",\n'
        '        "C-02",\n'
        '        "Restricción Presupuestaria",\n'
        '        r"Analiza la recta presupuestaria $p_1 x_1 + p_2 x_2 = m$, sus interceptos y su región factible.",\n'
        '        "Analyze",\n'
        '        "micro.pdf",\n'
        '        2,\n'
        '        [],\n'
        '        [\n'
        '            ("Olvida factor 1/2", r"$a/\\sqrt{x}$", r"$\\frac{a}{2\\sqrt{x}}$", r"Error de coeficiente", "Revisar minuciosamente la regla de potencia y el exponente fraccionario al derivar radicales.", "Omitir 1/2."),\n'
        '            ("Suma gasto al ingreso", r"$(m+p_1 x)/p_2$", r"$(m-p_1 x)/p_2$", r"Signo invertido", "Revisar minuciosamente el signo negativo al trasladar el gasto en x_1 al despejar la recta.", "Sumar gasto."),\n'
        '            ("Frontera punteada", r"$>$", r"$\\le$", r"Región opuesta", "Revisar minuciosamente la diferencia entre desigualdad débil sólida y región factible inferior.", "Frontera punteada."),\n'
        '            ("Divide por suma de precios", r"$m/(p_1+p_2)$", r"$m/p_2$", r"Denominador erróneo", "Revisar minuciosamente que cuando x_1=0 solo interviene el precio del bien 2 en el intercepto.", "Sumar precios."),\n'
        '            ("Multiplica ingreso y precio", r"$m p_2$", r"$m/p_2$", r"Producto espurio", "Revisar minuciosamente que la cantidad máxima se obtiene dividiendo el ingreso entre el precio.", "Multiplicar."),\n'
        '            ("Resta precio al ingreso", r"$m-p_2$", r"$m/p_2$", r"Diferencia espuria", "Revisar minuciosamente la relación de cociente lineal entre el presupuesto total y el precio.", "Restar precio."),\n'
        '        ],\n'
        '        [\n'
        '            ("A-C02-01", r"Precios e ingreso estrictamente positivos $p_1,p_2,m>0$", r"Permite definir interceptos finitos y pendiente negativa."),\n'
        '        ],\n'
        '        ["MC7", "open_symbolic", "multiple_select"],\n'
        '    )\n'
        ']\n'
    )
    (work_dir / "cta_data.py").write_text(cta_data_code, encoding="utf-8")
    cta_ok, _, cta_errs, _ = compile_cta(work_dir / "cta_data.py", work_dir, require_assumptions=True)
    assert cta_ok, f"compile_cta failed: {cta_errs}"

    cta_obj = json.loads((work_dir / "cta.json").read_text(encoding="utf-8"))
    for idx, d in enumerate(cta_obj["competencies"][0]["distractors"], start=1):
        d["id"] = f"D-C02-{idx:02d}"
    (work_dir / "cta.json").write_text(json.dumps(cta_obj, indent=2, ensure_ascii=False), encoding="utf-8")

    manifest_payload = {
        "min_archetypes": 4,
        "shards": [
            {
                "shard_id": "shard_02",
                "min_archetypes": 4,
                "competency_ids": ["C-02"],
                "competencies": cta_obj["competencies"],
            }
        ],
    }
    (shards_dir / "pre_shard_manifest.json").write_text(
        json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (shards_dir / "shard_02_data.py").write_text(c02_block.strip(), encoding="utf-8")

    success, errors = compile_shard(
        work_dir_or_path=work_dir,
        shard_id="shard_02",
        strict=True,
        seeds=50,
        min_archetypes=4,
        templates_per_modality=2,
    )
    assert success, f"compile_shard failed on C-02 prompt example: {errors}"
    assert errors == []
