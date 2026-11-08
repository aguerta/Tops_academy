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

import json
import re
import sys
from pathlib import Path
import pytest

# Ensure skill directories and repo root are in sys.path
repo_root = Path(__file__).resolve().parents[1]
c2c_dir = repo_root / ".agents" / "skills" / "content-to-course"
qa_dir = repo_root / ".agents" / "skills" / "course-qa-evaluator" / "scripts"

for p in (c2c_dir, qa_dir, repo_root):
    p_str = str(p)
    if p_str not in sys.path:
        sys.path.insert(0, p_str)

from compile_shard import compile_shard
from compile_cta import compile_cta
from engine.instantiate import instantiate_competency
from validator.core import validate_course_content
from standardized_audit_engine import run_full_audit


def test_lean_prompt_sizes_and_subagent_types_hygiene():
    """Validates byte caps on prompt_shard_author.md and CRLF cleanliness in subagent_types.json."""
    shard_author_prompt = c2c_dir / "system_prompts" / "lean" / "prompt_shard_author.md"
    assert shard_author_prompt.is_file(), f"Missing file: {shard_author_prompt}"
    raw_prompt_bytes = shard_author_prompt.read_bytes()
    assert len(raw_prompt_bytes) <= 5000, (
        f"prompt_shard_author.md exceeds 5000 bytes: {len(raw_prompt_bytes)} bytes"
    )

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
        '            ("Inversión de focos", r"$\\eta = 1 - \\frac{T_H}{T_C}$", r"$\\eta = 1 - \\frac{T_C}{T_H}$", r"$\\eta > 1$", "Revisar focos térmicos $T_C$ y $T_H$.", "Omitir cociente."),'
        '\n'
        '            ("Calor residual espurio", r"$\\eta = 1 - \\frac{T_C}{T_H}$", r"$\\eta = 1 - \\frac{T_C}{T_H}$", r"$\\eta \\le 0$", "Revisar segundo principio.", "Omitir resta."),'
        '\n'
        '            ("Desplazamiento arbitrario", r"$\\eta = 1 - \\frac{T_C-40}{T_H-40}$", r"$\\eta = 1 - \\frac{T_C}{T_H}$", r"$\\eta \\ne \\eta_0$", "Revisar escala absoluta.", "Omitir Kelvin."),'
        '\n'
        '            ("Factor espurio en foco caliente", r"$\\eta = 1 - \\frac{T_C}{1.5 T_H}$", r"$\\eta = 1 - \\frac{T_C}{T_H}$", r"$\\eta$ distorsionado", "Revisar balance energético.", "Omitir conservación."),'
        '\n'
        '            ("Normalización suma", r"$\\eta = \\frac{T_H - T_C}{T_H + T_C}$", r"$\\eta = 1 - \\frac{T_C}{T_H}$", r"Denominador suma", "Revisar rendimiento térmico.", "Omitir división."),'
        '\n'
        '            ("Semidiferencia", r"$\\eta = \\frac{T_H - T_C}{2 T_H}$", r"$\\eta = 1 - \\frac{T_C}{T_H}$", r"Factor dos espurio", "Revisar trabajo neto obtenido.", "Omitir integración."),'
        '\n'
        '        ],\n'
        '        [\n'
        '            ("A-Hab01-01", r"Reversibilidad estricta $\\sigma_{\\text{irr}} = 0$", r"Bajo irreversibilidad $\\sigma_{\\text{irr}} > 0$, el rendimiento real es menor."),'
        '\n'
        '        ],\n'
        '    )\n'
        ']\n'
    )
    (work_dir / "cta_data.py").write_text(cta_data_code, encoding="utf-8")
    cta_ok, cta_dict, cta_errs, _ = compile_cta(work_dir / "cta_data.py", work_dir, require_assumptions=True)
    assert cta_ok, f"compile_cta failed: {cta_errs}"
    cta_json_file = work_dir / "cta.json"
    assert cta_json_file.is_file(), "cta.json was not created"

    # Ensure distractor IDs align with D-H01-01..06 as expected by Hab-01
    cta_obj = json.loads(cta_json_file.read_text(encoding="utf-8"))
    comp_hab = cta_obj["competencies"][0]
    for idx, d in enumerate(comp_hab["distractors"], start=1):
        d["id"] = f"D-H01-0{idx}"
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

    # 4. Compile shard with --strict --min-archetypes 4 --seeds 50
    success, errors = compile_shard(
        work_dir_or_path=work_dir,
        shard_id="shard_01",
        strict=True,
        seeds=50,
        min_archetypes=4,
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
    assert len(tpl_list) == 4, f"Expected 4 archetypes, found {len(tpl_list)}"

    tpl_types = [t.get("interaction_type") for t in tpl_list]
    assert tpl_types.count("multiple_choice_7_options") >= 1 or tpl_types.count("multiple_choice") >= 1
    assert tpl_types.count("fill_in_the_blank") >= 2
    assert tpl_types.count("multiple_select") >= 1

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
