"""Forensic Replay and Full Pipeline Certification Suite for Run ab30cf91 (C2C v3.3 Hardening).

Executes 8 non-mocked, fast (< 10s total runtime) forensic replay tests on real Greene
econometric vectors and Stage 1/2 hardened components:
- V1: Bootstrap Zero-Raster Multi-PDF Ingest & Director stdout <= 1.5 KB
- V2: Part 01 PATCH_LEDGER_ALERT Zero False Rejection on Greene Orphan Math
- V3: --append End-to-End Continuous IDs & Base Prerequisites DAG Validation
- V4: plan_shards Weighted Isolation on 32 Greene Competencies (10 Hab-* isolated in Wave 1)
- V5: Shard 06 KaTeX @var@ Sandwich Matrix & Strict Uninterpolated Placeholder Hard-Block
- V6: Shard 08 Zero-Disk-Mutation, Modular shard_fixes Splicing & Circuit Breaker
- V7: Dual c2c_hook_guard PreToolUse Enforcement & budget_guard 108-Turn Watchdog
- V8: Cryptographic Per-Item Option Shuffle (CRC32) & Coherent Blind Judge Pointer Mode
"""

from __future__ import annotations

import json
import math
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / ".agents" / "skills" / "content-to-course"
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from budget_guard import (
    DEFAULT_MAX_SCRIPT_LOOPS,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MAX_TURNS,
    evaluate_watchdog_rules,
    generate_repair_redispatch,
    parse_transcript,
)
from c2c_hook_guard import find_active_c2c_lock, process_hook
from check_templates import (
    check_single_template,
    check_templates_file_or_dir,
)
from compile_cta import compile_cta, normalize_orphan_math
from compile_shard import compile_shard
from dispatch import (
    dispatch_authors,
    dispatch_cta,
    dispatch_judges,
    get_type_definitions,
    load_system_prompt,
)
from engine.assemble import assemble_question, render_template
from engine.invariants import (
    check_instance_invariants,
    check_unrendered_placeholders,
    validate_katex_syntax,
)
from judge import generate_judge_batch
from patch_ledger import get_ledger, reset_ledger
from plan_shards import plan_shards
from prepare import prepare_course
from run import PipelineRunner, format_compact_json_stdout


# ==============================================================================
# V1: Bootstrap Zero-Raster Multi-PDF Ingest & Director stdout <= 1.5 KB
# ==============================================================================

def test_v1_bootstrap_zero_raster_multi_pdf_and_stdout_cap(tmp_path: Path, capsys: pytest.CaptureFixture):
    """V1: Ingests 2 real Greene PDFs in < 3.0s with 0 raster PNGs, stdout <= 1.5 KB,
    lean specs <= 5 KB, and active lockfile.
    """
    content_dir = REPO_ROOT / "content" / "estadistica_asintotica"
    greene_pdfs = sorted(list(content_dir.glob("*.pdf")))
    assert len(greene_pdfs) >= 2, f"Real Greene PDFs not found in {content_dir}: {greene_pdfs}"
    # Verify exact Greene chapters analyzed in forensic run ab30cf91
    pdf_names = [p.name for p in greene_pdfs]
    assert any("Greene" in name and "93" in name for name in pdf_names), f"Missing Greene 93 PDF: {pdf_names}"
    assert any("Greene" in name and "923-946" in name for name in pdf_names), f"Missing Greene 923-946 PDF: {pdf_names}"

    work_dir = tmp_path / "work"
    runner = PipelineRunner(
        pdf=greene_pdfs,
        course_id="greene_asymptotics_v1",
        work_dir=work_dir,
        director_id="director_v1_conv",
    )

    t0 = time.perf_counter()
    res = runner.run_stage_bootstrap()
    elapsed = time.perf_counter() - t0

    # 1. Performance SLA: local compute < 3.0s
    assert elapsed < 3.0, f"Bootstrap took {elapsed:.2f}s, exceeding 3.0s SLA!"

    # 2. Zero-Raster Guarantee: 0 PNG files generated in work_dir
    png_files = list(work_dir.glob("**/*.png"))
    assert len(png_files) == 0, f"Zero-raster violated: {len(png_files)} PNGs found!"

    # 3. Source isolation: Only Greene PDFs ingested (0 unrelated PDFs)
    pre_cta = json.loads((work_dir / "pre_cta_manifest.json").read_text(encoding="utf-8"))
    ingested_names = [f["doc"] for f in pre_cta.get("files", [])]
    assert len(ingested_names) == 2, f"Expected 2 Greene PDFs, got {len(ingested_names)}"
    for name in ingested_names:
        assert any(p.name == name for p in greene_pdfs), f"Unrelated PDF ingested: {name}"

    # 4. Director context diet: stdout <= 1500 bytes and valid parseable JSON
    captured = capsys.readouterr().out.strip()
    stdout_bytes = len(captured.encode("utf-8"))
    assert stdout_bytes <= 1500, f"stdout exceeded 1,500 bytes: {stdout_bytes} B"
    parsed_stdout = json.loads(captured)
    assert parsed_stdout["status"] == "ready_for_cta"

    # 5. Lean Subagent Specs: <= 5 KB prompt files in dispatch/types/
    types_dir = work_dir / "dispatch" / "types"
    assert types_dir.is_dir()
    for t_file in types_dir.glob("*.json"):
        t_data = json.loads(t_file.read_text(encoding="utf-8"))
        p_bytes = len(t_data.get("system_prompt", "").encode("utf-8"))
        assert p_bytes <= 5120, f"Spec {t_file.name} prompt exceeded 5,120 bytes: {p_bytes} B"

    # 6. Compact Pointer CTA Work Orders
    cta_orders_file = work_dir / "dispatch" / "cta_work_orders.json"
    assert cta_orders_file.is_file()
    cta_orders = json.loads(cta_orders_file.read_text(encoding="utf-8"))
    for subagent in cta_orders.get("Subagents", []):
        prompt = subagent.get("Prompt", "")
        assert len(prompt.encode("utf-8")) <= 300, f"CTA pointer prompt exceeded 300 B: {len(prompt)}"
        assert "view_file" in prompt
        assert "cta_01.json" in prompt

    # 7. Active and valid .c2c_subagent_lock.json
    lock_file = work_dir / ".c2c_subagent_lock.json"
    assert lock_file.is_file()
    lock_data = json.loads(lock_file.read_text(encoding="utf-8"))
    assert lock_data.get("active") is True
    assert "created_at" in lock_data
    assert lock_data.get("director_conversation_id") == "director_v1_conv"

    # 8. Adversarial test of format_compact_json_stdout under extreme 25-subpart workloads
    extreme_payload = {
        "status": "ready_for_shard",
        "stage": "shards",
        "course_id": "greene_asymptotics_extreme",
        "Subagents": [
            {
                "Role": f"Author for partition {i:02d}",
                "TypeName": "c2c_shard_author",
                "Prompt": (
                    f"Author work order for partition {i:02d}: Generate interactive PrairieLearn @var@ "
                    f"templates for competencies C-{i:02d} and Hab-{i:02d}. Inspect guidelines at "
                    f"work/dispatch/items/shard_{i:02d}.json and verify math invariants using KaTeX."
                ),
            }
            for i in range(1, 26)
        ],
        "item_files": [f"work/dispatch/items/shard_{i:02d}.json" for i in range(1, 26)],
    }
    extreme_out = format_compact_json_stdout(
        payload=extreme_payload,
        work_dir=work_dir,
        stage_name="shards",
        max_bytes=1500,
    )
    extreme_bytes = len(extreme_out.encode("utf-8"))
    assert extreme_bytes <= 1500, f"Extreme workload stdout exceeded 1,500 bytes: {extreme_bytes} B"
    parsed_extreme = json.loads(extreme_out)
    assert parsed_extreme.get("status") == "ready_for_shard"
    assert parsed_extreme.get("stage") == "shards"


# ==============================================================================
# V2: Part 01 PATCH_LEDGER_ALERT Zero False Rejection on Greene Orphan Math
# ==============================================================================

def test_v2_part_01_patch_ledger_zero_false_rejection(tmp_path: Path):
    """V2: Compiles Greene orphan math expressions with 0.0% degraded_pct and Attempt #1 success."""
    course_id = "greene_orphan_math_v2"
    reset_ledger(course_id)

    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)

    manifest_data = {
        "course_id": course_id,
        "cta_mode": "direct",
        "documents": [
            {"name": "greene_ch05.pdf", "path": "content/greene_ch05.pdf", "total_pages": 15, "valid_page_range": [1, 15]}
        ],
        "files": [
            {"doc": "greene_ch05.pdf", "path": "content/greene_ch05.pdf", "total_pages": 15, "valid_page_range": [1, 15], "doc_slug": "greene_ch05"}
        ],
    }
    manifest_file = work_dir / "pre_cta_manifest.json"
    manifest_file.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")

    cta_code = '''# -*- coding: utf-8 -*-
COURSE_ID = "greene_orphan_math_v2"
COURSE_TITLE = "Asymptotic Statistics Greene Ch 5"

COMPETENCIES = [
    (
        "concept",
        "C-01",
        "Propiedad de la Matriz Inversa Q_{zx}^{-1}",
        "La matriz de proyección instrumental Q_{zx}^{-1} y su transpuesta (Z'X)^{-1} garantizan consistencia.",
        "Understand",
        "greene_ch05.pdf",
        2,
        [],
        [
            ("Error en Q_{zx}^{-1}", "Asume que Q_{zx}^{-1} es escalar", "Q_{zx}^{-1} es matriz invertible.", "$0$", "Revisar álgebra.", None),
            ("Error en (Z'X)^{-1}", "Invierte orden en (Z'X)^{-1}", "(Z'X)^{-1} requiere rango completo.", "$0$", "Revisar rango.", None),
            ("Error en normalidad", "Ignora distribución asintótica", "\\\\sqrt{n}(\\\\hat{\\\\beta} - \\\\beta) \\\\xrightarrow{d} \\\\mathcal{N}(0, V)", "$0$", "Revisar TLC.", None),
            ("Error en momentos", "Confunde momentos empíricos", "Momento poblacional convergente.", "$0$", "Revisar LGN.", None),
            ("Error en rango", "Asume rango deficiente", "Identificación exige rango k.", "$0$", "Revisar rango.", None),
            ("Error en varianza", "Varianza asintótica nula", "Varianza V es simétrica definida positiva.", "$0$", "Revisar V.", None),
        ]
    ),
    (
        "skill",
        "Hab-01",
        "Derivación de la Distribución Límite \\\\sqrt{n}(\\\\hat{\\\\beta} - \\\\beta) \\\\xrightarrow{d} \\\\mathcal{N}(0, V)",
        "Calcular la matriz de varianza asintótica sandwich usando Q_{zx}^{-1} y momentos empíricos.",
        "Apply",
        "greene_ch05.pdf",
        4,
        ["C-01"],
        [
            ("Error procedural en inversión", "Omite transponer matriz Z", "Debe premultiplicar por Z'.", "$0$", "Ver paso 1.", "Omitir premultiplicar por la transpuesta instrumental Z'"),
            ("Error en escala estocástica", "Divide por n en lugar de \\\\sqrt{n}", "El factor de normalización es \\\\sqrt{n}.", "$0$", "Ver paso 2.", "Dividir por el tamaño muestral n en lugar de la raíz cuadrada \\\\sqrt{n}"),
            ("Error en dimensión", "Dimensiones matriciales incompatibles", "Verificar conformabilidad.", "$0$", "Ver álgebra.", None),
            ("Error en varianza del error", "Supone homocedasticidad forzada", "Admitir matriz sandwich robusta.", "$0$", "Ver V.", None),
            ("Error en convergencia", "Confunde convergencia casi segura", "La convergencia es en distribución.", "$0$", "Ver modos.", None),
            ("Error de signo en centrado", "Resta la estimación al parámetro", "El centrado es \\\\hat{\\\\beta} - \\\\beta.", "$0$", "Ver centrado.", None),
        ]
    )
]
'''
    cta_data_file = work_dir / "cta_data.py"
    cta_data_file.write_text(cta_code, encoding="utf-8")

    valid, cta_dict, errors, elapsed = compile_cta(
        cta_data_path=cta_data_file,
        output_dir=work_dir,
        manifest_path=manifest_file,
    )

    assert valid is True, f"compile_cta failed with errors: {errors}"
    assert len(errors) == 0

    ledger = get_ledger()
    counts = ledger.count_by_severity()
    assert counts.get("degraded", 0) == 0, f"Expected 0 degraded fields, got: {counts}"
    assert counts.get("healed", 0) >= 3, f"Expected >= 3 healed fields, got: {counts}"
    assert ledger.degraded_percentage() == 0.0, f"degraded_pct non-zero: {ledger.degraded_percentage()}"


# ==============================================================================
# V3: --append End-to-End Continuous IDs & Base Prerequisites DAG Validation
# ==============================================================================

def test_v3_append_continuous_ids_and_base_prerequisites(tmp_path: Path):
    """V3: --append against base course preserves continuous IDs (H-05, C-19, Hab-11)
    and passes cross-course DAG validation against base C-01.
    """
    work_append = tmp_path / "work_append"
    work_append.mkdir(parents=True, exist_ok=True)

    base_facts = [f"H-{i:02d}" for i in range(1, 5)]
    base_concepts = [f"C-{i:02d}" for i in range(1, 19)]
    base_skills = [f"Hab-{i:02d}" for i in range(1, 11)]
    all_base_ids = base_facts + base_concepts + base_skills

    delta_info = {
        "next_ids_by_prefix": {
            "H-": "H-05",
            "C-": "C-19",
            "Hab-": "Hab-11",
        },
        "existing_competency_ids": all_base_ids,
        "existing_competencies_outline": [
            {"id": cid, "name": f"Base Competency {cid}", "type": "concept" if cid.startswith("C-") else ("skill" if cid.startswith("Hab-") else "fact")}
            for cid in all_base_ids
        ],
    }

    manifest_data = {
        "course_id": "greene_append_v3",
        "cta_mode": "direct",
        "documents": [
            {"name": "greene_delta.pdf", "path": "content/greene_delta.pdf", "total_pages": 10, "valid_page_range": [1, 10]}
        ],
        "files": [
            {"doc": "greene_delta.pdf", "path": "content/greene_delta.pdf", "total_pages": 10, "valid_page_range": [1, 10], "doc_slug": "greene_delta"}
        ],
        "delta": delta_info,
    }
    manifest_file = work_append / "pre_cta_manifest.json"
    manifest_file.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")

    # Verify dispatch_cta injects delta continuous IDs and existing outlines
    cta_dispatch = dispatch_cta(work_append, mode="direct")
    item_file = Path(cta_dispatch["item_files"][0])
    assert item_file.is_file()
    item_data = json.loads(item_file.read_text(encoding="utf-8"))
    assert "delta_context" in item_data or "delta" in item_data or "APPEND DELTA MODE" in item_data.get("Prompt", "")

    # Now simulate c2c_cta_architect outputting delta competencies with base cross-ref C-01
    cta_data_content = '''# -*- coding: utf-8 -*-
COURSE_ID = "greene_append_v3"
COURSE_TITLE = "Greene Delta Module"

COMPETENCIES = [
    (
        "fact",
        "",
        "Identidad Asintótica Delta",
        "Definición formal de la cota asintótica de Cramér-Rao.",
        "Remember",
        "greene_delta.pdf",
        1,
        ["C-01"],
        [
            ("Error en cota", "Asume cota dependiente de n", "La cota normalizada es invariante a n.", "$0$", "Revisar cota.", None),
            ("Error en matriz", "Confunde Hessiano con gradiente", "El Hessiano esperado define la información.", "$0$", "Revisar Fisher.", None),
            ("Error de signo", "Invierte signo en Hessiano", "La información es menos la esperanza del Hessiano.", "$0$", "Revisar signo.", None),
            ("Error de regularidad", "Aplica a distribuciones no regulares", "Exige condiciones de diferenciabilidad.", "$0$", "Revisar supuestos.", None),
            ("Error en eficiencia", "Asume estimador siempre eficiente", "La eficiencia requiere alcanzar la cota.", "$0$", "Revisar eficiencia.", None),
            ("Error en varianza", "Varianza nula en muestra finita", "La cota es un límite inferior estricto.", "$0$", "Revisar varianza.", None),
        ]
    ),
    (
        "concept",
        "",
        "Principio de Identificación Débil",
        "Consecuencias de correlación cercana a cero entre instrumentos y variables endógenas.",
        "Understand",
        "greene_delta.pdf",
        2,
        ["C-01"],
        [
            ("Error en sesgo", "Asume estimador IV insesgado bajo debilidad", "El estimador IV se sesga hacia MCO.", "$0$", "Revisar sesgo.", None),
            ("Error en estadístico F", "Considera F > 2 suficiente", "La regla de Stock y Yogo sugiere F > 10.", "$0$", "Revisar umbral F.", None),
            ("Error en test de Wald", "Asume test de Wald con nivel nominal", "El test de Wald distorsiona el tamaño.", "$0$", "Revisar inferencia.", None),
            ("Error en distribución", "Asume normalidad estándar bajo instrumentos débiles", "La distribución es bimodal o no estándar.", "$0$", "Revisar límite.", None),
            ("Error en Anderson-Rubin", "Descarta el test de Anderson-Rubin", "AR es robusto a instrumentos débiles.", "$0$", "Revisar AR.", None),
            ("Error de identificación", "Confunde no identificación con débil", "La débil es de rango cercano a cero pero no nulo.", "$0$", "Revisar rango.", None),
        ]
    ),
    (
        "skill",
        "",
        "Diagnóstico de Instrumentos Débiles y Test de Anderson-Rubin",
        "Calcular el estadístico de primera etapa F y verificar robustez.",
        "Apply",
        "greene_delta.pdf",
        3,
        ["C-01", "C-19"],
        [
            ("Error procedural en F", "Omite corregir por grados de libertad", "Debe ajustar por el número de instrumentos excluidos.", "$0$", "Ver paso F.", "Omitir dividir por el número de instrumentos excluidos en la primera etapa"),
            ("Error en covarianza de residuos", "Usa residuos MCO en test AR", "AR proyecta la variable dependiente transformada.", "$0$", "Ver paso AR.", "Utilizar residuos MCO en vez de la proyección estructural del test AR"),
            ("Error de umbral crítico", "Compara con valor crítico normal", "Usar tabla de Stock-Yogo.", "$0$", "Ver tablas.", None),
            ("Error en exogeneidad", "Asume que debilidad implica endogeneidad", "Son conceptos ortogonales.", "$0$", "Ver supuestos.", None),
            ("Error de multiplicidad", "Ignora sobreidentificación", "Controlar por grado de sobreidentificación.", "$0$", "Ver momentos.", None),
            ("Error en inversión de AR", "Invierte el intervalo de confianza", "El intervalo puede ser inconexo.", "$0$", "Ver inversión.", None),
        ]
    )
]
'''
    (work_append / "cta_data.py").write_text(cta_data_content, encoding="utf-8")

    valid, cta_dict, errors, elapsed = compile_cta(
        cta_data_path=work_append / "cta_data.py",
        output_dir=work_append,
        manifest_path=manifest_file,
    )

    assert valid is True, f"compile_cta delta failed: {errors}"
    comps = cta_dict.get("competencies", [])
    assert len(comps) == 3

    # Assert IDs continued cleanly without resetting to 01!
    assert comps[0]["id"] == "H-05", f"Expected H-05, got {comps[0]['id']}"
    assert comps[1]["id"] == "C-19", f"Expected C-19, got {comps[1]['id']}"
    assert comps[2]["id"] == "Hab-11", f"Expected Hab-11, got {comps[2]['id']}"

    # Assert distractors followed continuous numbering
    assert comps[0]["distractors"][0]["id"] == "D-H05-01"
    assert comps[1]["distractors"][0]["id"] == "D-C19-01"
    assert comps[2]["distractors"][0]["id"] == "D-Hab11-01"

    # Assert DAG validation preserved base C-01 reference
    assert "C-01" in comps[0]["prerequisites"]
    assert "C-01" in comps[1]["prerequisites"]
    assert "C-01" in comps[2]["prerequisites"]
    assert "C-19" in comps[2]["prerequisites"]


# ==============================================================================
# V4: plan_shards Weighted Isolation on 32 Greene Competencies
# ==============================================================================

def test_v4_plan_shards_weighted_isolation_32_greene_competencies(tmp_path: Path):
    """V4: Partitions 32 competencies of asyntotic_estatistics_v2.json isolating 100%
    of 10 Hab-* competencies in 1-comp shards in Wave 1.
    """
    course_path = REPO_ROOT / "courses" / "asyntotic_estatistics_v2.json"
    if not course_path.is_file():
        pytest.skip("courses/asyntotic_estatistics_v2.json not found")

    course_data = json.loads(course_path.read_text(encoding="utf-8"))
    comps = course_data.get("competencies", [])
    assert len(comps) == 32, f"Expected 32 competencies, got {len(comps)}"

    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    cta_path = work_dir / "cta.json"
    cta_path.write_text(json.dumps(course_data, indent=2), encoding="utf-8")

    (work_dir / "pre_cta_manifest.json").write_text(json.dumps({
        "course_id": "asyntotic_estatistics_v2",
        "cta_mode": "direct",
        "documents": [{"name": "greene.pdf", "path": "content/greene.pdf", "total_pages": 40}],
    }), encoding="utf-8")

    shards_dir = work_dir / "shards"
    manifest = plan_shards(cta_path=cta_path, output_dir=shards_dir, max_wave_size=10)

    assert manifest["total_competencies"] == 32
    shards = manifest.get("shards", [])

    hab_shards = [s for s in shards if any(cid.startswith("Hab-") for cid in s["competency_ids"])]
    non_hab_shards = [s for s in shards if not any(cid.startswith("Hab-") for cid in s["competency_ids"])]

    # 1. Hard Skill Isolation: 100% of 10 Hab-* are isolated (1 Hab/shard)
    assert len(hab_shards) == 10, f"Expected 10 Hab shards, got {len(hab_shards)}"
    for s in hab_shards:
        assert s["competency_count"] == 1, f"Skill shard {s['shard_id']} had {s['competency_count']} comps"
        assert len(s["competency_ids"]) == 1
        assert s["competency_ids"][0].startswith("Hab-")

    # 2. Heaviest-First Wave 1 Rule: All 10 Hab-* shards are in Wave 1
    wave_1_shards = [s for s in shards if s.get("wave_index") == 1]
    assert len(wave_1_shards) == 10, f"Expected exactly 10 shards in Wave 1, got {len(wave_1_shards)}"
    for s in wave_1_shards:
        assert s["competency_count"] == 1
        assert s["competency_ids"][0].startswith("Hab-")

    # 3. Concept / Fact shards grouped in contiguous units <= 2
    for s in non_hab_shards:
        assert s["competency_count"] <= 2, f"Non-skill shard exceeded 2 comps: {s['competency_count']}"

    # 4. 100% of competencies accounted for without drops or duplicates
    all_assigned_cids = []
    for s in shards:
        all_assigned_cids.extend(s["competency_ids"])
    assert len(all_assigned_cids) == 32
    assert len(set(all_assigned_cids)) == 32
    assert set(all_assigned_cids) == {c["id"] for c in comps}


# ==============================================================================
# V5: Shard 06 KaTeX @var@ Sandwich Matrix & Strict Uninterpolated Placeholder Block
# ==============================================================================

def test_v5_shard_06_katex_sandwich_and_delta_placeholder_block():
    """V5: Verifies IV/2SLS sandwich matrix template with @var@ and single-letter math
    compiles with 0 R-20 errors, while uninterpolated {delta} is deterministically blocked.
    """
    # 1. Valid IV/2SLS sandwich matrix with PrairieLearn @var@ and single-letter econometrics vars:
    # z, w, u, d, k, n alongside \mu, \sigma^2, \xrightarrow{d}, Q_{zx}^{-1}, \mathbb{R}^{k}
    template_sandwich = {
        "id": "T-IV-SANDWICH-01",
        "competency_id": "Hab-04",
        "interaction_type": "multiple_choice_7_options",
        "difficulty": "hard",
        "bloom": "Apply",
        "stem": (
            r"Considere el modelo estructural $y = X\beta + u$ con perturbación escalar $u$ y matriz de instrumentos "
            r"$Z \in \mathbb{R}^{n \times @k_dim@}$. El estimador IV cumple $b_{IV} = (Z'X)^{-1}Z'y$ donde la matriz "
            r"límite $Q_{zx}^{-1} = \operatorname{plim} (\frac{1}{n} Z'X)^{-1}$ existe y es invertible. Para covariables "
            r"exógenas $w$ e instrumentos excluidos $z$, bajo normalidad asintótica $\sqrt{n}(b_{IV} - \beta) \xrightarrow{d} \mathcal{N}(\mu, \sigma^2 V)$ "
            r"con dimensión $d = k$ y varianza estimada $V_{11} = @a11@$ sobre una muestra aleatoria de tamaño $n$:"
        ),
        "hints": [
            r"Recuerde que el error estructural $u$ satisface $\mathbb{E}[z_i u_i] = 0$ con dimensión $k$ y $d$ grados de libertad.",
            r"La matriz de proyección instrumental involucra $Q_{zx}^{-1}$ con parámetro @k_dim@ y dispersión $\sigma^2$.",
            r"Verifique la convergencia en distribución $\sqrt{n}(b_{IV} - \beta) \xrightarrow{d} \mathcal{N}(\mu, \sigma^2 V)$ en $\mathbb{R}^k$ con covarianza entre $w$ y $z$."
        ],
        "detailed_solution": (
            r"Por el teorema del límite central multivariado, $\sqrt{n}(b_{IV} - \beta) \xrightarrow{d} \mathcal{N}(\mu, \sigma^2 V)$ "
            r"donde la perturbación $u$ tiene varianza $\sigma^2$, las variables instrumentales $z$ y exógenas $w$ garantizan rango completo $k$, "
            r"con $d$ restricciones de identificación y elemento de varianza $a_{11} = @a11@$ evaluado sobre $n$ observaciones."
        ),
        "distractor_ids": ["D-Hab04-01", "D-Hab04-02", "D-Hab04-03", "D-Hab04-04", "D-Hab04-05", "D-Hab04-06"],
        "generate_py": (
            "def generate(rng):\n"
            "    k_dim = rng.randint(2, 5)\n"
            "    a11 = round(rng.uniform(1.1, 4.9), 2)\n"
            "    d = 2\n"
            "    k = 3\n"
            "    return {\n"
            "        'vars': {'k_dim': k_dim, 'a11': a11, 'd': d, 'k': k},\n"
            "        'correct': f'Varianza asintótica eficiente con $V_{{11}} = {a11}$',\n"
            "        'distractors': [\n"
            "            {'value': f'Estimación sesgada por debilidad con $V_{{11}} = {round(a11 + 0.8, 2)}$', 'distractor_id': 'D-Hab04-01'},\n"
            "            {'value': f'Omisión de matriz instrumental resultando en {round(a11 * 1.5, 2)}', 'distractor_id': 'D-Hab04-02'},\n"
            "            {'value': f'Inversión no ortogonal de momentos produciendo {round(a11 - 0.4, 2)}', 'distractor_id': 'D-Hab04-03'},\n"
            "            {'value': f'Discrepancia en forma cuadrática con residuo {round(a11 + 2.1, 2)}', 'distractor_id': 'D-Hab04-04'},\n"
            "            {'value': f'Falta de corrección por heterocedasticidad dando {round(a11 * 0.7, 2)}', 'distractor_id': 'D-Hab04-05'},\n"
            "            {'value': f'Desviación asintótica no centrada evaluada en {round(a11 + 1.2, 2)}', 'distractor_id': 'D-Hab04-06'},\n"
            "        ]\n"
            "    }\n"
        ),
        "cross_check_py": "def verify(r):\n    return True\n",
    }

    declared_dids = {f"D-Hab04-{i:02d}" for i in range(1, 7)}
    clean_errors = check_single_template(
        template=template_sandwich,
        competency_id="Hab-04",
        declared_distractor_ids=declared_dids,
        num_dry_run_seeds=50,
    )
    assert clean_errors == [], f"Sandwich matrix template produced unexpected errors: {clean_errors}"

    # 2. Broken template leaking uninterpolated {delta} (the exact Judge 04 Hab-04 bug of ab30cf91)
    template_broken_delta = {
        "id": "T-BROKEN-DELTA-HAB04",
        "competency_id": "Hab-04",
        "interaction_type": "multiple_choice_7_options",
        "difficulty": "medium",
        "bloom": "Understand",
        "stem": r"El estadístico converge para cualquier discrepancia {delta} en el soporte.",
        "hints": ["Pista 1 contextual", "Pista 2 operativa", "Pista 3 comprobatoria"],
        "detailed_solution": r"Solución detallada con discrepancia {delta}.",
        "distractor_ids": ["D-Hab04-01", "D-Hab04-02", "D-Hab04-03", "D-Hab04-04", "D-Hab04-05", "D-Hab04-06"],
        "generate_py": (
            "def generate(rng):\n"
            "    val = rng.randint(10, 50)\n"
            "    return {\n"
            "        'vars': {'val': val},\n"
            "        'correct': f'Respuesta {val}',\n"
            "        'distractors': [\n"
            "            {'value': f'Distractor {i}_{val}', 'distractor_id': f'D-Hab04-{i+1:02d}'}\n"
            "            for i in range(6)\n"
            "        ]\n"
            "    }\n"
        ),
        "cross_check_py": "def verify(r):\n    return True\n",
    }

    broken_errors_bracket = check_single_template(
        template=template_broken_delta,
        competency_id="Hab-04",
        declared_distractor_ids=declared_dids,
        num_dry_run_seeds=50,
    )
    assert len(broken_errors_bracket) > 0, "Uninterpolated {delta} template was not caught!"
    assert any("{delta}" in e for e in broken_errors_bracket), f"Expected '{{delta}}' diagnostic, got: {broken_errors_bracket}"

    # 3. Broken template leaking unrendered PrairieLearn @delta@ token
    template_broken_pl_delta = {
        "id": "T-BROKEN-PL-DELTA-HAB04",
        "competency_id": "Hab-04",
        "interaction_type": "multiple_choice_7_options",
        "difficulty": "medium",
        "bloom": "Understand",
        "stem": r"El estadístico converge para cualquier discrepancia @delta@ en el soporte de la distribución.",
        "hints": ["Pista 1 contextual", "Pista 2 operativa", "Pista 3 comprobatoria"],
        "detailed_solution": r"Solución detallada con discrepancia @delta@ sin interpolar.",
        "distractor_ids": ["D-Hab04-01", "D-Hab04-02", "D-Hab04-03", "D-Hab04-04", "D-Hab04-05", "D-Hab04-06"],
        "generate_py": (
            "def generate(rng):\n"
            "    val = rng.randint(10, 50)\n"
            "    return {\n"
            "        'vars': {'val': val},\n"
            "        'correct': f'Respuesta {val}',\n"
            "        'distractors': [\n"
            "            {'value': f'Distractor {i}_{val}', 'distractor_id': f'D-Hab04-{i+1:02d}'}\n"
            "            for i in range(6)\n"
            "        ]\n"
            "    }\n"
        ),
        "cross_check_py": "def verify(r):\n    return True\n",
    }

    broken_errors_pl = check_single_template(
        template=template_broken_pl_delta,
        competency_id="Hab-04",
        declared_distractor_ids=declared_dids,
        num_dry_run_seeds=50,
    )
    assert len(broken_errors_pl) > 0, "Unrendered PrairieLearn @delta@ template was not caught!"
    assert any("@delta@" in e for e in broken_errors_pl), f"Expected '@delta@' diagnostic, got: {broken_errors_pl}"


# ==============================================================================
# V6: Shard 08 Zero-Disk-Mutation, Modular shard_fixes Splicing & Circuit Breaker
# ==============================================================================

def test_v6_shard_08_zero_disk_mutation_and_shard_fixes_and_circuit_breaker(tmp_path: Path):
    """V6: Failed compile preserves shard_08_data.py byte-for-byte, shard_fixes/C-08.py
    splices cleanly, and repeated identical error hashes trip circuit breaker.
    """
    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    templates_dir = work_dir / "templates"
    attempts_dir = work_dir / ".check_attempts"
    shards_dir.mkdir(parents=True, exist_ok=True)
    templates_dir.mkdir(parents=True, exist_ok=True)
    attempts_dir.mkdir(parents=True, exist_ok=True)

    # Base manifest
    (work_dir / "pre_cta_manifest.json").write_text(json.dumps({
        "course_id": "circuit_test",
        "cta_mode": "direct",
        "documents": [{"name": "greene.pdf", "path": "content/greene.pdf", "total_pages": 10}],
    }), encoding="utf-8")

    (shards_dir / "pre_shard_manifest.json").write_text(json.dumps({
        "shards": [{"shard_id": "shard_08", "competency_ids": ["C-08"]}],
    }), encoding="utf-8")

    (work_dir / "cta.json").write_text(json.dumps({
        "course_id": "circuit_test",
        "competencies": [
            {
                "id": "C-08",
                "name": "Greene Competency C-08",
                "type": "concept",
                "distractors": [],
            }
        ],
    }), encoding="utf-8")

    # 1. Zero-Disk-Mutation on failed compile
    broken_shard_code = '''# -*- coding: utf-8 -*-
# Canonical shard_08_data.py with intentional dry-run error
def gen_c08(rng):
    raise ValueError("Intentional dry-run crash in gen_c08")

def ver_c08(r):
    return True

TEMPLATES = [
    ("C-08", "multiple_choice", "Stem {x}", gen_c08, ver_c08, "Sol {x}", "Concept", ["D-C08-01", "D-C08-02", "D-C08-03", "D-C08-04", "D-C08-05", "D-C08-06"], ("greene.pdf", 1, "Quote"), ["H1", "H2", "H3"])
]
'''
    shard_file = shards_dir / "shard_08_data.py"
    shard_file.write_text(broken_shard_code, encoding="utf-8")
    original_bytes = shard_file.read_bytes()

    # Attempt 1: Compile fails
    ok_1, errs_1 = compile_shard(
        work_dir_or_path=work_dir,
        shard_id="shard_08",
        strict=False,
    )
    assert not ok_1
    assert shard_file.read_bytes() == original_bytes, "Zero-disk-mutation violated! File was altered."

    # 2. Circuit breaker verification on repeated errors
    # Edit 1 introduces schema error
    shard_file.write_text("# Edit 1\nTEMPLATES = 'broken_string'\n", encoding="utf-8")
    ok_cb1, errs_cb1 = compile_shard(work_dir_or_path=work_dir, shard_id="shard_08", strict=False)
    assert not ok_cb1

    att_file = work_dir / ".check_attempts" / "compile_shard_08.json"
    assert att_file.is_file()
    state_cb1 = json.loads(att_file.read_text(encoding="utf-8"))
    assert state_cb1["distinct_compiles"] == 2
    assert state_cb1["same_error_streak"] == 1

    # Identical re-run returns [NO-CHANGE] without advancing distinct_compiles or streak
    ok_cb_id, errs_cb_id = compile_shard(work_dir_or_path=work_dir, shard_id="shard_08", strict=False)
    assert not ok_cb_id
    assert any("[NO-CHANGE" in e for e in errs_cb_id)

    state_id = json.loads(att_file.read_text(encoding="utf-8"))
    assert state_id["distinct_compiles"] == 2
    assert state_id["same_error_streak"] == 1

    # Edit 2: Distinct edit producing the same normalized error
    shard_file.write_text("# Edit 2\nTEMPLATES = 'broken_string'\n", encoding="utf-8")
    ok_cb2, errs_cb2 = compile_shard(work_dir_or_path=work_dir, shard_id="shard_08", strict=False)
    assert not ok_cb2
    state_2 = json.loads(att_file.read_text(encoding="utf-8"))
    assert state_2["distinct_compiles"] == 3
    assert state_2["same_error_streak"] == 2

    # Edit 3: Third distinct edit producing the same normalized error -> explicitly trips CIRCUIT BREAKER
    shard_file.write_text("# Edit 3\nTEMPLATES = 'broken_string'\n", encoding="utf-8")
    ok_cb3, errs_cb3 = compile_shard(work_dir_or_path=work_dir, shard_id="shard_08", strict=False)
    assert not ok_cb3
    assert any("[CIRCUIT BREAKER" in e for e in errs_cb3), f"Expected [CIRCUIT BREAKER] in errors: {errs_cb3}"
    state_3 = json.loads(att_file.read_text(encoding="utf-8"))
    assert state_3["distinct_compiles"] == 4
    assert state_3["same_error_streak"] == 3

    # 3. Modular shard_fixes/C-08.py splicing & clean circuit breaker reset
    fixes_dir = shards_dir / "shard_fixes"
    fixes_dir.mkdir(parents=True, exist_ok=True)
    fix_c08 = fixes_dir / "C-08.py"
    fix_code = '''# -*- coding: utf-8 -*-
def gen_c08(rng):
    w = rng.randint(100, 999)
    return {'vars': {'w': w}, 'correct': str(w), 'distractors': []}

def ver_c08(r):
    return True

TEMPLATES = [
    ("C-08", "fill_in_the_blank", "Fixed Stem C08 @w@:", gen_c08, ver_c08, "Solución @w@.", "Concept", [], ("greene.pdf", 1, "Quote"), ["Pista 1 identificacion", "Pista 2 procedimiento", "Pista 3 comprobacion"])
]
'''
    fix_c08.write_text(fix_code, encoding="utf-8")
    shard_file.write_text(
        "TEMPLATES = [('C-08', 'multiple_choice', 'Broken', lambda r: None, lambda r: True, 'Sol', 'Concept', [], ('greene.pdf', 1, 'Q'), ['H1', 'H2', 'H3'])]\n",
        encoding="utf-8"
    )

    ok_fix, errs_fix = compile_shard(
        work_dir_or_path=work_dir,
        shard_id="shard_08",
        strict=False,
    )
    assert ok_fix is True, f"compile_shard with modular fix failed: {errs_fix}"
    assert len(errs_fix) == 0
    compiled_c08 = templates_dir / "C-08.json"
    assert compiled_c08.is_file(), "C-08.json was not generated!"
    assert not att_file.is_file(), "Circuit breaker state was not cleared/unlinked on successful compile!"


# ==============================================================================
# V7: Dual c2c_hook_guard PreToolUse Enforcement & budget_guard 108-Turn Watchdog
# ==============================================================================

def test_v7_dual_hook_guard_and_budget_guard_planner_response(tmp_path: Path):
    """V7: c2c_hook_guard enforces worker compile_shard.py read ban and Director diet
    under active lock (< 15ms pass-through when unlocked), and budget_guard detects
    108-turn PLANNER_RESPONSE straggler.
    """
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    lock_file = work_dir / ".c2c_subagent_lock.json"

    # 1. Fast pass-through (< 15ms) when no lock exists
    start_t = time.perf_counter()
    unlocked_res = process_hook(
        {"conversationId": "worker-1", "toolCall": {"name": "view_file", "args": {"AbsolutePath": "compile_shard.py"}}},
        custom_lock_file=str(lock_file),
    )
    elapsed_ms = (time.perf_counter() - start_t) * 1000
    assert elapsed_ms < 15.0, f"Unlocked hook took {elapsed_ms:.2f}ms (threshold 15ms)"
    assert unlocked_res["decision"] == "allow"

    # Create active lockfile
    lock_payload = {
        "active": True,
        "status": "active",
        "stage": "shards",
        "course_id": "test_v7_course",
        "director_conversation_id": "director_conv_123",
        "expires_at": time.time() + 3600,
        "work_dir": str(work_dir.resolve()),
    }
    lock_file.write_text(json.dumps(lock_payload, indent=2), encoding="utf-8")

    # 2. Worker DENIED reading compile_shard.py
    worker_read = process_hook(
        {
            "conversationId": "worker_author_01",
            "toolCall": {"name": "view_file", "args": {"AbsolutePath": ".agents/skills/content-to-course/compile_shard.py"}},
        },
        custom_lock_file=str(lock_file),
    )
    assert worker_read["decision"] == "deny"
    assert "PROHIBITED" in worker_read.get("reason", "") or "worker" in worker_read.get("reason", "").lower()

    # 3. Worker DENIED shell bypass (Get-Content compile_shard.py)
    worker_shell = process_hook(
        {
            "conversationId": "worker_author_01",
            "toolCall": {"name": "run_command", "args": {"CommandLine": "Get-Content .agents/skills/content-to-course/compile_shard.py"}},
        },
        custom_lock_file=str(lock_file),
    )
    assert worker_shell["decision"] == "deny"

    # 4. Director DENIED reading/editing worker data files (*_data.py, shard_fixes/*.py, judge_responses*.json)
    dir_read_shard = process_hook(
        {
            "conversationId": "director_conv_123",
            "toolCall": {"name": "view_file", "args": {"AbsolutePath": str(work_dir / "shards" / "shard_06_data.py")}},
        },
        custom_lock_file=str(lock_file),
    )
    assert dir_read_shard["decision"] == "deny"

    dir_edit_fix = process_hook(
        {
            "conversationId": "director_conv_123",
            "toolCall": {"name": "edit_file", "args": {"Path": str(work_dir / "shards" / "shard_fixes" / "C-08.py"), "Replacement": "# fix"}},
        },
        custom_lock_file=str(lock_file),
    )
    assert dir_edit_fix["decision"] == "deny"

    dir_read_judge = process_hook(
        {
            "conversationId": "director_conv_123",
            "toolCall": {"name": "view_file", "args": {"AbsolutePath": str(work_dir / "verification" / "judge_responses_01.json")}},
        },
        custom_lock_file=str(lock_file),
    )
    assert dir_read_judge["decision"] == "deny"

    # 5. Director ALLOWS run.py and state.json
    dir_run = process_hook(
        {
            "conversationId": "director_conv_123",
            "toolCall": {"name": "run_command", "args": {"CommandLine": 'python .agents/skills/content-to-course/run.py --stage bootstrap'}},
        },
        custom_lock_file=str(lock_file),
    )
    assert dir_run["decision"] == "allow"

    # 6. Budget watchdog 108-turn PLANNER_RESPONSE straggler detection
    transcript_file = tmp_path / "transcript.jsonl"
    with open(transcript_file, "w", encoding="utf-8") as f:
        for turn_idx in range(1, 109):
            entry = {
                "turn": turn_idx,
                "type": "PLANNER_RESPONSE",
                "usage": {"input_tokens": 50000, "output_tokens": 2000},
                "tool_calls": [{"name": "run_command", "args": {"CommandLine": "python compile_shard.py"}}],
            }
            f.write(json.dumps(entry) + "\n")

    metrics = parse_transcript(transcript_file)
    assert metrics.turn_count == 108, f"Expected 108 turns, got {metrics.turn_count}"
    assert metrics.total_tokens > 5_000_000

    report = evaluate_watchdog_rules(metrics)
    report.unit_id = "shard_06"
    assert report.is_runaway is True
    assert len(report.runaway_reasons) > 0
    assert report.recommended_action == "kill_and_redispatch"

    # Generate repair redispatch targeting shard_fixes/
    mock_cta = {
        "competencies": [{"id": "Hab-04", "name": "Greene IV Derivation"}],
    }
    (work_dir / "cta.json").write_text(json.dumps(mock_cta), encoding="utf-8")
    (work_dir / "shards").mkdir(parents=True, exist_ok=True)
    (work_dir / "shards" / "pre_shard_manifest.json").write_text(json.dumps({
        "shards": [{"shard_id": "shard_06", "competency_ids": ["Hab-04"]}],
    }), encoding="utf-8")

    redispatch = generate_repair_redispatch(work_dir, [report])
    assert redispatch is not None
    assert "c2c_repair" in str(redispatch)
    assert "shard_fixes/Hab-04.py" in str(redispatch) or "shard_fixes" in str(redispatch)

    # 7. Subagent catalog synchronization check (.agents/skills/content-to-course/subagent_types.json)
    types_json_path = SKILL_ROOT / "subagent_types.json"
    assert types_json_path.is_file(), f"subagent_types.json missing from {SKILL_ROOT}"
    disk_types = json.loads(types_json_path.read_text(encoding="utf-8"))
    mem_types = get_type_definitions(lean=False)
    assert disk_types == mem_types, "subagent_types.json on disk is out of sync with dispatch.get_type_definitions(lean=False)"

    type_prompts = {t["name"]: t.get("system_prompt", "") for t in disk_types}
    assert {"c2c_cta_architect", "c2c_shard_author", "c2c_judge", "c2c_repair"}.issubset(type_prompts.keys())

    # Critical contracts:
    # a) @var@, shard_fixes, compile_shard.py read prohibition in author and repair
    for role in ("c2c_shard_author", "c2c_repair"):
        p = type_prompts[role]
        assert "@var@" in p, f"@var@ contract missing from {role}"
        assert "shard_fixes" in p, f"shard_fixes contract missing from {role}"
        assert "compile_shard.py" in p, f"compile_shard.py prohibition missing from {role}"

    # b) ArtifactMetadata prohibition across all 4 subagent types
    for role, p in type_prompts.items():
        assert "ArtifactMetadata" in p, f"ArtifactMetadata prohibition missing from {role}"

    # c) Coherent Blind Judge pointer mode (no contradictory 'NO EJECUTES view_file' ban)
    judge_p = type_prompts["c2c_judge"]
    assert "NO EJECUTES `view_file`" not in judge_p
    assert "NO EJECUTES view_file" not in judge_p


# ==============================================================================
# V8: Cryptographic Per-Item Option Shuffle (CRC32) & Coherent Blind Judge Mode
# ==============================================================================

def test_v8_judge_option_shuffle_and_coherent_pointer_mode(tmp_path: Path):
    """V8: Generates judge batch across 40 items asserting uniform letter distribution
    (no single letter > 35%) and coherent pointer instructions without contradictory bans.
    """
    work_dir = tmp_path / "judge_work"
    templates_dir = work_dir / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)

    # Create 20 templates -> 40 items total
    comp_ids = [f"C-{i:02d}" for i in range(1, 21)]
    for cid in comp_ids:
        tpl_data = {
            "id": f"TPL-{cid}",
            "competency_id": cid,
            "interaction_type": "multiple_choice_7_options",
            "bloom": "Understand",
            "stem": f"Examine property {cid}:",
            "hints": ["H1", "H2", "H3"],
            "detailed_solution": "Sol",
            "distractor_ids": [f"D-{cid}-{j:02d}" for j in range(1, 7)],
            "generate_py": (
                "def generate(rng):\n"
                "    k = rng.randint(10, 99)\n"
                f"    correct = 'Valor ' + str(k) + ' para {cid}'\n"
                f"    distractors = [\n"
                f"        {{'value': f'Dist {{idx}} {{k}} para {cid}', 'distractor_id': f'D-{cid}-{{idx:02d}}'}}\n"
                f"        for idx in range(1, 7)\n"
                f"    ]\n"
                "    return {'vars': {'k': k}, 'correct': correct, 'distractors': distractors}\n"
            ),
        }
        (templates_dir / f"{cid}.json").write_text(json.dumps(tpl_data, indent=2), encoding="utf-8")

    (work_dir / "cta.json").write_text(json.dumps({
        "course_id": "shuffle_v8_test",
        "competencies": [{"id": cid, "name": f"Competency {cid}"} for cid in comp_ids],
    }), encoding="utf-8")

    # Generate batch with 2 items per competency = 40 items
    judge_p, gt_p = generate_judge_batch(
        templates_path=templates_dir,
        work_dir=work_dir,
        items_per_competency=2,
        seeds=(101, 202),
        ready_only=False,
    )

    assert Path(judge_p).is_file()
    assert Path(gt_p).is_file()

    gt_data = json.loads(Path(gt_p).read_text(encoding="utf-8"))
    total_items = len(gt_data)
    assert total_items == 40, f"Expected 40 items in ground truth, got {total_items}"

    # 1. Uniform option distribution across A..G
    letter_counts: Dict[str, int] = {}
    for item_id, ans_info in gt_data.items():
        correct_letter = ans_info.get("correct_letter") or (ans_info.get("correct_letters", [None])[0])
        if correct_letter:
            letter = str(correct_letter).strip().upper()
            letter_counts[letter] = letter_counts.get(letter, 0) + 1

    assert len(letter_counts) >= 4, f"Insufficient diversity of correct letters: {letter_counts}"
    for letter, count in letter_counts.items():
        ratio = count / total_items
        assert ratio <= 0.35, f"Letter '{letter}' clustered at {ratio*100:.1f}% ({count}/{total_items}), exceeding 35% max!"

    # 2. Coherent Blind Judge Instructions in dispatch_judges(pointer=True)
    judge_dispatch = dispatch_judges(work_dir, pointer=True)
    assert len(judge_dispatch["Subagents"]) >= 1
    judge_item_file = Path(judge_dispatch["item_files"][0])
    assert judge_item_file.is_file()

    judge_item_data = json.loads(judge_item_file.read_text(encoding="utf-8"))
    prompt_in_item = judge_item_data.get("Prompt", "")

    # Zero contradiction: Must NOT contain "NO EJECUTES view_file"
    assert "NO EJECUTES `view_file`" not in prompt_in_item
    assert "NO EJECUTES view_file" not in prompt_in_item
    assert "view_file" in prompt_in_item
