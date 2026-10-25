"""Comprehensive Test Suite for Stream 1E:
Zero-Raster PDF Ingest, Multi-PDF Sources Isolation,
Lossless LaTeX Healing & PATCH_LEDGER_ALERT Calibration,
Continuous IDs in --append Mode, and Active Workspace Protection.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import time
from pathlib import Path

import pytest

# Ensure skill directories are in sys.path
_repo_root = Path(__file__).resolve().parent.parent
_skills_dir = _repo_root / ".agents" / "skills" / "content-to-course"
_delete_skill_dir = _repo_root / ".agents" / "skills" / "delete-course" / "scripts"

for p in (_skills_dir, _delete_skill_dir, _repo_root):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

from check_cta import check_cta_file, check_prerequisites_dag, validate_cta_rules
from compile_cta import compile_cta, compile_cta_module, count_evaluated_fields
from engine.invariants import validate_katex_syntax
from cta_merge import (
    apply_harmonize,
    merge_cta_parts,
    normalize_orphan_math,
    parse_next_ids_by_prefix,
    sanitize_competency_math,
)
from delete_course import clean_orphan_course_dirs, is_active_workspace
from ingest import ingest_course
from patch_ledger import get_ledger, reset_ledger
from prepare import prepare_course


def _create_dummy_pdf(pdf_path: Path, num_pages: int = 5) -> Path:
    """Helper creating a fast synthetic multi-page PDF."""
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open()
    for i in range(num_pages):
        page = doc.new_page(width=612, height=792)
        page.insert_text((50, 50), f"Document {pdf_path.stem} - Page {i+1}", fontsize=14)
    doc.save(str(pdf_path))
    doc.close()
    return pdf_path


class TestZeroRasterIngestAndMultiPdf:
    """Verifies sub-second zero-raster ingest and strict multi-PDF source subsetting."""

    def test_zero_raster_pdf_ingest_speed_and_zero_png(self, tmp_path: Path):
        """Zero-Raster PDF Ingest runs in < 1.0s and renders 0 page PNGs."""
        pdf_path = tmp_path / "content" / "large_lecture.pdf"
        _create_dummy_pdf(pdf_path, num_pages=20)

        work_dir = tmp_path / "work"
        t0 = time.perf_counter()
        manifest = prepare_course(
            input_path=pdf_path,
            work_dir=work_dir,
            course_id="test_zero_raster",
            render_pages=False,
        )
        elapsed = time.perf_counter() - t0

        assert elapsed < 1.0, f"prepare_course took {elapsed:.3f}s (exceeds 1.0s threshold)"
        assert manifest["total_files"] == 1
        assert manifest["total_pages"] == 20

        # Check pages directory: zero PNGs rendered
        pages_dir = work_dir / "pages"
        assert pages_dir.exists()
        png_files = list(pages_dir.rglob("*.png"))
        assert len(png_files) == 0, f"Expected 0 rendered PNGs, found {len(png_files)}: {png_files}"

        # Manifest JSON was correctly generated
        manifest_file = work_dir / "pre_cta_manifest.json"
        assert manifest_file.is_file()
        data = json.loads(manifest_file.read_text(encoding="utf-8"))
        assert data["files"][0]["valid_page_range"] == [1, 20]

    def test_multi_pdf_subset_isolation(self, tmp_path: Path):
        """Passing 2 PDFs out of 4 in the same directory ingests ONLY the 2 requested PDFs."""
        folder = tmp_path / "content" / "mixed_docs"
        folder.mkdir(parents=True, exist_ok=True)

        doc_a = _create_dummy_pdf(folder / "doc_A.pdf", num_pages=3)
        doc_b = _create_dummy_pdf(folder / "doc_B.pdf", num_pages=5)
        doc_c = _create_dummy_pdf(folder / "doc_C.pdf", num_pages=4)
        doc_d = _create_dummy_pdf(folder / "doc_D.pdf", num_pages=2)

        work_dir = tmp_path / "work_subset"
        # Explicit subset: only doc_A and doc_C
        manifest = prepare_course(
            input_path=[doc_a, doc_c],
            work_dir=work_dir,
            course_id="test_subset",
            render_pages=False,
        )

        assert manifest["total_files"] == 2, f"Expected 2 files, got {manifest['total_files']}"
        assert manifest["total_pages"] == 7  # 3 + 4

        doc_names = [f["doc"] for f in manifest["files"]]
        assert "doc_A.pdf" in doc_names
        assert "doc_C.pdf" in doc_names
        assert "doc_B.pdf" not in doc_names
        assert "doc_D.pdf" not in doc_names

    def test_zero_raster_zero_empty_directory_clutter(self, tmp_path: Path):
        """When render_pages=False for PDFs, zero empty work/pages/<doc_slug>/ directories are created."""
        pdf_path = tmp_path / "content" / "sample.pdf"
        _create_dummy_pdf(pdf_path, num_pages=5)
        work_dir = tmp_path / "work_clutter"

        manifest = prepare_course(
            input_path=pdf_path,
            work_dir=work_dir,
            course_id="test_no_clutter",
            render_pages=False,
        )
        pages_dir = work_dir / "pages"
        subdirs = [d for d in pages_dir.iterdir() if d.is_dir()]
        assert len(subdirs) == 0, f"Expected 0 empty subdirectories in pages/, found {subdirs}"

    def test_multi_pdf_duplicate_slug_collision_and_unicode_safety(self, tmp_path: Path):
        """Duplicate basenames across directories and Unicode filenames (Anna’s Archive) are disambiguated cleanly."""
        folder1 = tmp_path / "vol1"
        folder2 = tmp_path / "vol2"
        pdf1 = _create_dummy_pdf(folder1 / "lecture_notes.pdf", num_pages=3)
        pdf2 = _create_dummy_pdf(folder2 / "lecture_notes.pdf", num_pages=4)
        pdf3 = _create_dummy_pdf(tmp_path / "content" / "Anna’s Archive-93.pdf", num_pages=6)

        work_dir = tmp_path / "work_collision"
        manifest = prepare_course(
            input_path=[pdf1, pdf2, pdf3],
            work_dir=work_dir,
            course_id="test_collision",
            render_pages=False,
        )

        assert manifest["total_files"] == 3
        slugs = [f["doc_slug"] for f in manifest["files"]]
        assert len(set(slugs)) == 3, f"Expected 3 unique slugs, got {slugs}"
        assert "lecture_notes" in slugs
        assert "lecture_notes_2" in slugs
        assert "Anna_s_Archive-93" in slugs


class TestPatchLedgerAndLatexHealing:
    """Verifies harmless deterministic LaTeX healing is recorded as healed (0% degraded)."""

    def test_compound_subscript_and_superscript_healing(self):
        """Compound subscripts like Q_{zx}^{-1} are cleanly wrapped without splitting."""
        raw = "La matriz de proyección Q_{zx}^{-1} y el factor \\alpha con x_{t-1}."
        healed = normalize_orphan_math(raw)
        assert "$Q_{zx}^{-1}$" in healed
        assert "^{-1}" not in healed.replace("$Q_{zx}^{-1}$", "")
        assert "$\\alpha$" in healed
        assert "$x_{t-1}$" in healed

    def test_compile_cta_orphan_latex_healing_not_degraded(self, tmp_path: Path):
        """10 orphan LaTeX fields compile with ok=True, 0 errors, degraded_pct == 0.0%, healed >= 10."""
        reset_ledger("test_healing_course")
        pdf_path = tmp_path / "math_source.pdf"
        _create_dummy_pdf(pdf_path, num_pages=10)

        work_dir = tmp_path / "work"
        prepare_course(
            input_path=pdf_path,
            work_dir=work_dir,
            course_id="test_healing_course",
            render_pages=False,
        )

        # Build cta_data.py with 10 orphan LaTeX fields
        cta_data_content = '''# -*- coding: utf-8 -*-
COURSE_ID = "test_healing_course"
COURSE_TITLE = "Econometría Matemática"

COMPETENCIES = [
    (
        "concept",
        "C-01",
        "Matriz de proyección Q_{zx}^{-1}",
        "Propiedades algebraicas de Q_{zx}^{-1} y su relación con \\alpha.",
        "Understand",
        "math_source.pdf",
        1,
        [],
        [
            ("Error en Q_{zx}^{-1}", "Cree que Q_{zx}^{-1} es escalar", "Q_{zx}^{-1} es matriz invertible.", "$0$", "Revisar álgebra lineal.", None),
            ("Error en \\alpha", "Confunde \\alpha con \\beta", "\\alpha representa el vector estructural.", "$0$", "Revisar estimador.", None),
            ("Error en x_{t-1}", "Asume x_{t-1} contemporáneo", "x_{t-1} es la variable retardada.", "$0$", "Revisar series de tiempo.", None),
            ("Error en k^*", "Ignora el punto estacionario k^*", "k^* denota la regla de oro.", "$0$", "Verificar estado estacionario.", None),
            ("Error en r^*", "Supone r^* variable", "r^* es la tasa fija de equilibrio.", "$0$", "Consultar tasa real.", None),
            ("Error en dot{w}", "Confunde dot{w} con velocidad fija", "dot{w} es derivada temporal continua.", "$0$", "Revisar cálculo diferencial.", None),
        ],
    ),
    (
        "skill",
        "Hab-01",
        "Cálculo del estimador con x_{t-1}",
        "Determinar analíticamente el estimador insesgado usando matriz Q_{zx}^{-1} y retardos x_{t-1}.",
        "Apply",
        "math_source.pdf",
        2,
        ["C-01"],
        [
            ("Error algebraico 1", "Omite transponer matriz", "Debe transponer antes de invertir.", "$0$", "Ver paso transposición.", "Omitir transponer la matriz"),
            ("Error algebraico 2", "Multiplica matrices en orden inverso", "El producto matricial no es conmutativo.", "$0$", "Ver orden matricial.", "Invertir el orden del producto matricial"),
            ("Distractor adicional 3", "Confunde término de error", "El error tiene media condicional nula.", "$0$", "Revisar supuestos.", None),
            ("Distractor adicional 4", "Aplica operador incorrecto", "Usar esperanza matemática conditional.", "$0$", "Revisar valor esperado.", None),
            ("Distractor adicional 5", "Confunde varianza con covarianza", "La matriz es de varianza-covarianza.", "$0$", "Revisar momentos estocásticos.", None),
            ("Distractor adicional 6", "Cancela términos dependientes", "No se pueden cancelar términos estocásticos.", "$0$", "Revisar simplificación.", None),
        ],
    ),
]
'''
        data_file = work_dir / "cta_data.py"
        data_file.write_text(cta_data_content, encoding="utf-8")

        valid, cta_dict, errors, elapsed = compile_cta(
            cta_data_path=data_file,
            output_dir=work_dir,
            manifest_path=work_dir / "pre_cta_manifest.json",
        )

        assert valid is True, f"compile_cta failed with errors: {errors}"
        assert len(errors) == 0

        ledger = get_ledger()
        sev_counts = ledger.count_by_severity()
        assert sev_counts.get("degraded", 0) == 0, f"Expected 0 degraded patches, got {sev_counts}"
        assert sev_counts.get("healed", 0) >= 10, f"Expected >= 10 healed patches, got {sev_counts}"

        # Degraded percentage must be 0.0%
        deg_pct = ledger.degraded_percentage()
        assert deg_pct == 0.0
        alert, _, _ = ledger.check_degraded_alert()
        assert alert is False

        # Verify compiled JSON preserved clean LaTeX delimiters
        cta_json = json.loads((work_dir / "cta.json").read_text(encoding="utf-8"))
        c1 = cta_json["competencies"][0]
        assert "$Q_{zx}^{-1}$" in c1["name"]
        assert "$Q_{zx}^{-1}$" in c1["description_latex"]
        assert "$\\alpha$" in c1["description_latex"]

    def test_greene_econometrics_compound_math_expressions(self):
        """Real Greene expressions from ab30cf91 (inverses, transposes, operator limits) heal with 0 KaTeX errors."""
        expressions = [
            ("Matriz Q_{zx}^{-1}", "$Q_{zx}^{-1}$"),
            ("Inversa (Z'X)^{-1}", "$(Z'X)^{-1}$"),
            ("Límite \\operatorname{plim}_{n \\to \\infty}", "$\\operatorname{plim}_{n \\to \\infty}$"),
            ("Varianza \\hat{\\sigma}^2", "$\\hat{\\sigma}^2$"),
            ("Proyección X'Z(Z'Z)^{-1}Z'X", "$X'Z(Z'Z)^{-1}Z'X$"),
            ("Estimador (X'X)^{-1}X'y", "$(X'X)^{-1}X'y$"),
            ("Estimador IV \\hat{\\beta}_{IV}", "$\\hat{\\beta}_{IV}$"),
            ("Estimador OLS \\hat{\\beta}_{OLS}", "$\\hat{\\beta}_{OLS}$"),
        ]
        for raw, expected in expressions:
            healed = normalize_orphan_math(raw)
            assert expected in healed, f"Expected '{expected}' in '{healed}' (raw: '{raw}')"
            assert healed.count("$") % 2 == 0, f"Unbalanced dollars in '{healed}'"
            assert "$$$" not in healed
            errs = validate_katex_syntax(healed, "greene_math", allow_template_vars=True)
            assert len(errs) == 0, f"KaTeX syntax errors in '{healed}': {errs}" 


class TestContinuousIdsAppendAndHarmonize:
    """Verifies end-to-end continuous ID sequences and cross-course prerequisite validation."""

    def test_parse_next_ids_by_prefix_formats(self):
        """parse_next_ids_by_prefix handles integer, string, and category maps correctly."""
        assert parse_next_ids_by_prefix(None) == {"H": 1, "C": 1, "Hab": 1}
        assert parse_next_ids_by_prefix({}) == {"H": 1, "C": 1, "Hab": 1}

        # Int map
        info_int = {"next_ids_by_prefix": {"H": 5, "C": 12, "Hab": 8}}
        assert parse_next_ids_by_prefix(info_int) == {"H": 5, "C": 12, "Hab": 8}

        # String map with hyphens
        info_str = {"next_ids_by_prefix": {"H-": "H-03", "C-": "C-05", "Hab-": "Hab-04"}}
        assert parse_next_ids_by_prefix(info_str) == {"H": 3, "C": 5, "Hab": 4}

        # next_numbers_by_prefix
        info_nums = {"next_numbers_by_prefix": {"H-": 3, "C-": 5, "Hab-": 4}}
        assert parse_next_ids_by_prefix(info_nums) == {"H": 3, "C": 5, "Hab": 4}

    def test_end_to_end_append_direct_and_mapreduce(self, tmp_path: Path):
        """Base course with H-01..02, C-01..04, Hab-01..03 produces delta starting at H-03, C-05, Hab-04."""
        courses_dir = tmp_path / "courses"
        courses_dir.mkdir(parents=True, exist_ok=True)

        # 1. Create existing base course JSON
        base_course = {
            "course_id": "macro_base",
            "course_title": "Macroeconomía Base",
            "competencies": [
                {"id": "H-01", "type": "fact", "name": "Hecho 1", "description_latex": "Desc", "distractors": []},
                {"id": "H-02", "type": "fact", "name": "Hecho 2", "description_latex": "Desc", "distractors": []},
                {"id": "C-01", "type": "concept", "name": "Concepto 1", "description_latex": "Desc", "distractors": []},
                {"id": "C-02", "type": "concept", "name": "Concepto 2", "description_latex": "Desc", "distractors": []},
                {"id": "C-03", "type": "concept", "name": "Concepto 3", "description_latex": "Desc", "distractors": []},
                {"id": "C-04", "type": "concept", "name": "Concepto 4", "description_latex": "Desc", "distractors": []},
                {"id": "Hab-01", "type": "skill", "name": "Habilidad 1", "description_latex": "Desc", "distractors": []},
                {"id": "Hab-02", "type": "skill", "name": "Habilidad 2", "description_latex": "Desc", "distractors": []},
                {"id": "Hab-03", "type": "skill", "name": "Habilidad 3", "description_latex": "Desc", "distractors": []},
            ],
            "questions": [{"id": "Q-01"}],
        }
        (courses_dir / "macro_base.json").write_text(json.dumps(base_course, indent=2), encoding="utf-8")

        # 2. Ingest new material with prepare_course in append mode
        append_pdf = tmp_path / "delta_lecture.pdf"
        _create_dummy_pdf(append_pdf, num_pages=6)

        work_append = tmp_path / "work_append"
        manifest = prepare_course(
            input_path=append_pdf,
            work_dir=work_append,
            course_id="macro_base",
            courses_dir=courses_dir,
            append=True,
            render_pages=False,
        )

        assert manifest.get("append_mode") is True
        delta = manifest.get("delta", {})
        assert delta.get("next_ids_by_prefix") == {"C-": "C-05", "Hab-": "Hab-04", "H-": "H-03"}
        assert "existing_competencies_outline" in delta
        assert len(delta["existing_competencies_outline"]) == 9

        # 3. Direct mode compile_cta with continuous IDs and referencing existing C-01
        reset_ledger("macro_base")
        cta_data_content = '''# -*- coding: utf-8 -*-
COURSE_ID = "macro_base"
COURSE_TITLE = "Macroeconomía Base (Delta)"

COMPETENCIES = [
    (
        "fact",
        "",  # Auto-assign next fact ID -> H-03
        "Regla de Taylor Delta",
        "Fórmula de la tasa de interés óptima $i_t = r^* + \\pi_t$.",
        "Remember",
        "delta_lecture.pdf",
        1,
        ["C-01"],  # Valid cross-reference to base course!
        [
            ("Error en Taylor", "Asume tasa fija", "La tasa es variable.", "$0$", "Revisar regla.", None),
            ("Error en inflación", "Omite meta de inflación", "La meta es explicita.", "$0$", "Revisar meta.", None),
            ("Error de signo", "Invierte signo de brecha", "La brecha positiva sube tasa.", "$0$", "Revisar signo.", None),
            ("Error en r", "Confunde r real con nominal", "r es tasa real neutra.", "$0$", "Revisar Fisher.", None),
            ("Error temporal", "Usa inflación rezagada", "Usa inflación esperada.", "$0$", "Revisar timing.", None),
            ("Error de coeficiente", "Asume coeficiente unitario", "El coeficiente usual es 1.5.", "$0$", "Revisar peso.", None),
        ],
    ),
    (
        "concept",
        "",  # Auto-assign next concept ID -> C-05
        "Canal de Crédito Bancario",
        "Mecanismo de transmisión de la política monetaria.",
        "Understand",
        "delta_lecture.pdf",
        2,
        ["C-01"],  # Valid cross-reference to base course!
        [
            ("Error en préstamos", "Cree que los préstamos no varían", "Los préstamos se contraen.", "$0$", "Revisar canal.", None),
            ("Error en colateral", "Ignora el efecto colateral", "El colateral amplifica el shock.", "$0$", "Revisar colateral.", None),
            ("Error de oferta", "Confunde oferta y demanda de crédito", "Es un shock de oferta bancaria.", "$0$", "Revisar oferta.", None),
            ("Error en spreads", "Asume spreads constantes", "Los spreads se amplían en crisis.", "$0$", "Revisar spreads.", None),
            ("Error en bancos", "Trata bancos como neutros", "Los bancos tienen fricciones financieras.", "$0$", "Revisar intermediación.", None),
            ("Error regulatorio", "Omite requerimiento de capital", "El capital bancario limita el crédito.", "$0$", "Revisar Basilea.", None),
        ],
    ),
    (
        "skill",
        "",  # Auto-assign next skill ID -> Hab-04
        "Cálculo del Impacto en Reservas",
        "Determinar el cambio en las reservas bancarias ante variación de tasa.",
        "Apply",
        "delta_lecture.pdf",
        3,
        ["C-01", "C-05"],
        [
            ("Error cálculo 1", "Omite el multiplicador monetario", "Debe incluir el multiplicador.", "$0$", "Revisar multiplicador.", "Omitir el multiplicador monetario"),
            ("Error cálculo 2", "Multiplica por tasa bruta", "Debe usar tasa neta porcentual.", "$0$", "Revisar tasa.", "Multiplicar por la tasa bruta en vez de neta"),
            ("Error 3", "Confunde M1 con base monetaria", "Las reservas afectan la base.", "$0$", "Revisar agregados.", None),
            ("Error 4", "Ignora encaje legal", "El encaje determina la fracción retenida.", "$0$", "Revisar encaje.", None),
            ("Error 5", "Aplica descuento simple", "Usar interés compuesto continuo.", "$0$", "Revisar descuento.", None),
            ("Error 6", "Suma variables no homogéneas", "Convertir a unidades reales.", "$0$", "Revisar unidades.", None),
        ],
    ),
]
'''
        (work_append / "cta_data.py").write_text(cta_data_content, encoding="utf-8")
        valid, cta_dict, errors, elapsed = compile_cta(
            cta_data_path=work_append / "cta_data.py",
            output_dir=work_append,
            manifest_path=work_append / "pre_cta_manifest.json",
        )

        assert valid is True, f"compile_cta append failed with errors: {errors}"
        comps = cta_dict["competencies"]
        assert len(comps) == 3

        # Continuous ID assertions
        assert comps[0]["id"] == "H-03", f"Expected H-03, got {comps[0]['id']}"
        assert comps[1]["id"] == "C-05", f"Expected C-05, got {comps[1]['id']}"
        assert comps[2]["id"] == "Hab-04", f"Expected Hab-04, got {comps[2]['id']}"

        # Distractor IDs continuous matching
        assert comps[0]["distractors"][0]["id"] == "D-H03-01"
        assert comps[1]["distractors"][0]["id"] == "D-C05-01"
        assert comps[2]["distractors"][0]["id"] == "D-Hab04-01"

        # Prerequisites preserved existing C-01 reference
        assert "C-01" in comps[0]["prerequisites"]
        assert "C-01" in comps[1]["prerequisites"]
        assert "C-01" in comps[2]["prerequisites"]

    def test_merge_cta_parts_append_continuous_ids(self, tmp_path: Path):
        """merge_cta_parts honors delta_manifest and starts sequences at next continuous IDs."""
        work_dir = tmp_path / "work_parts_append"
        work_dir.mkdir(parents=True, exist_ok=True)
        parts_dir = work_dir / "cta_parts"
        parts_dir.mkdir(parents=True, exist_ok=True)

        manifest_data = {
            "course_id": "macro_parts_append",
            "cta_mode": "mapreduce",
            "delta": {
                "next_ids_by_prefix": {"H-": "H-03", "C-": "C-05", "Hab-": "Hab-04"},
                "existing_competency_ids": ["H-01", "H-02", "C-01", "C-02", "C-03", "C-04", "Hab-01", "Hab-02", "Hab-03"],
            },
            "files": [{"doc": "doc.pdf", "file_index": 0}],
            "subparts": [
                {"subpart_id": "part_01", "subpart_index": 0, "doc": "doc.pdf", "file_index": 0},
                {"subpart_id": "part_02", "subpart_index": 1, "doc": "doc.pdf", "file_index": 0},
            ],
        }
        (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")

        # Part 1: 1 Fact, 1 Concept
        part_01 = {
            "competencies": [
                {
                    "id": "H-99",
                    "type": "fact",
                    "name": "Hecho Delta 1",
                    "description_latex": "Desc",
                    "unit_index": 1,
                    "evidence": [{"doc": "doc.pdf", "page": 1}],
                    "prerequisites": ["C-01"],
                    "distractors": [
                        {"id": "D-H99-01", "name": "D1", "wrong_belief": "W", "correct_belief": "C", "manifestation": "$0$", "evidence": {"doc": "doc.pdf", "page": 1}},
                        {"id": "D-H99-02", "name": "D2", "wrong_belief": "W", "correct_belief": "C", "manifestation": "$0$", "evidence": {"doc": "doc.pdf", "page": 1}},
                    ],
                },
                {
                    "id": "C-99",
                    "type": "concept",
                    "name": "Concepto Delta 1",
                    "description_latex": "Desc",
                    "unit_index": 2,
                    "evidence": [{"doc": "doc.pdf", "page": 2}],
                    "prerequisites": ["C-01"],
                    "distractors": [
                        {"id": "D-C99-01", "name": "D1", "wrong_belief": "W", "correct_belief": "C", "manifestation": "$0$", "evidence": {"doc": "doc.pdf", "page": 2}},
                        {"id": "D-C99-02", "name": "D2", "wrong_belief": "W", "correct_belief": "C", "manifestation": "$0$", "evidence": {"doc": "doc.pdf", "page": 2}},
                    ],
                },
            ]
        }
        (parts_dir / "part_01.json").write_text(json.dumps(part_01, indent=2), encoding="utf-8")

        # Part 2: 1 Skill, 1 Concept
        part_02 = {
            "competencies": [
                {
                    "id": "Hab-99",
                    "type": "skill",
                    "name": "Habilidad Delta 1",
                    "description_latex": "Desc",
                    "unit_index": 3,
                    "evidence": [{"doc": "doc.pdf", "page": 3}],
                    "prerequisites": ["C-01", "C-99"],
                    "distractors": [
                        {"id": "D-Hab99-01", "name": "D1", "omitted_step": "Omit 1", "correct_belief": "C", "manifestation": "$0$", "evidence": {"doc": "doc.pdf", "page": 3}},
                        {"id": "D-Hab99-02", "name": "D2", "omitted_step": "Omit 2", "correct_belief": "C", "manifestation": "$0$", "evidence": {"doc": "doc.pdf", "page": 3}},
                    ],
                },
                {
                    "id": "C-98",
                    "type": "concept",
                    "name": "Concepto Delta 2",
                    "description_latex": "Desc",
                    "unit_index": 4,
                    "evidence": [{"doc": "doc.pdf", "page": 4}],
                    "prerequisites": ["C-01"],
                    "distractors": [
                        {"id": "D-C98-01", "name": "D1", "wrong_belief": "W", "correct_belief": "C", "manifestation": "$0$", "evidence": {"doc": "doc.pdf", "page": 4}},
                        {"id": "D-C98-02", "name": "D2", "wrong_belief": "W", "correct_belief": "C", "manifestation": "$0$", "evidence": {"doc": "doc.pdf", "page": 4}},
                    ],
                },
            ]
        }
        (parts_dir / "part_02.json").write_text(json.dumps(part_02, indent=2), encoding="utf-8")

        merged = merge_cta_parts(work_dir)
        m_comps = merged["competencies"]
        ids = [c["id"] for c in m_comps]

        # Starting sequences: H starts at H-03, C starts at C-05 and C-06, Hab starts at Hab-04
        assert "H-03" in ids
        assert "C-05" in ids
        assert "C-06" in ids
        assert "Hab-04" in ids

        # Distractor IDs renumbered cleanly with new prefixes
        h03_comp = next(c for c in m_comps if c["id"] == "H-03")
        assert h03_comp["distractors"][0]["id"] == "D-H03-01"
        assert h03_comp["distractors"][1]["id"] == "D-H03-02"

        # Cross-prerequisite to base course C-01 preserved
        assert "C-01" in h03_comp["prerequisites"]

    def test_check_cta_rules_append_prerequisite_dag(self):
        """validate_cta_rules and check_cta_file accept base course prerequisites under --append."""
        def _dist(did: str, page: int = 2):
            return {
                "id": did,
                "name": f"Error {did}",
                "wrong_belief": "Creencia errónea.",
                "correct_belief": "Creencia correcta.",
                "trigger": "Al evaluar el modelo.",
                "manifestation": "$0$",
                "error_type": "conceptual_swap",
                "severity": "medium",
                "origin": "source",
                "remediation_hint": "Revisar conceptos base.",
                "evidence": {"doc": "doc.pdf", "page": page},
            }

        manifest_data = {
            "course_id": "macro_append",
            "files": [{"doc": "doc.pdf", "total_pages": 10, "valid_page_range": [1, 10]}],
            "delta": {
                "existing_course_id": "macro_base",
                "existing_competency_ids": ["C-01", "C-02", "H-01"],
                "next_ids_by_prefix": {"H": 3, "C": 5, "Hab": 4},
            },
        }
        cta_data = {
            "competencies": [
                {
                    "id": "C-05",
                    "name": "Equilibrio General Dinámico",
                    "type": "concept",
                    "description": "Modelo DSGE con retardo.",
                    "description_latex": "Modelo DSGE con retardo.",
                    "bloom": "Understand",
                    "unit_index": 1,
                    "evidence": [{"doc": "doc.pdf", "page": 2}],
                    "prerequisites": ["C-01"],
                    "distractors": [
                        _dist("D-C05-01"),
                        _dist("D-C05-02"),
                        _dist("D-C05-03"),
                    ],
                }
            ]
        }
        valid, errors = validate_cta_rules(cta_data, manifest_data=manifest_data)
        assert valid is True, f"validate_cta_rules failed with base prerequisite: {errors}"
        assert len(errors) == 0

        valid2, errors2 = check_cta_file(cta_data, manifest_data=manifest_data)
        assert valid2 is True
        assert len(errors2) == 0

        # Adversarial check: Unknown prerequisite not in delta causes failure
        bad_cta = {
            "competencies": [
                {
                    **cta_data["competencies"][0],
                    "prerequisites": ["C-99"],
                }
            ]
        }
        bad_valid, bad_errors = validate_cta_rules(bad_cta, manifest_data=manifest_data)
        assert bad_valid is False
        assert any("non-existent prerequisite 'C-99'" in e for e in bad_errors)

    def test_apply_harmonize_append_offsets_and_base_prereqs(self, tmp_path: Path):
        """apply_harmonize preserves append offsets and base course prerequisites without re-zeroing."""
        def _dist(did: str, page: int = 1):
            return {
                "id": did,
                "name": f"Error {did}",
                "wrong_belief": "W",
                "correct_belief": "C",
                "trigger": "T",
                "manifestation": "$0$",
                "error_type": "conceptual_swap",
                "severity": "medium",
                "origin": "source",
                "remediation_hint": "R",
                "evidence": {"doc": "doc.pdf", "page": page},
            }

        work_dir = tmp_path / "work_harmonize"
        work_dir.mkdir(parents=True, exist_ok=True)

        manifest_data = {
            "course_id": "test_harm_append",
            "files": [{"doc": "doc.pdf", "total_pages": 10, "valid_page_range": [1, 10]}],
            "delta": {
                "existing_course_id": "test_base",
                "existing_competency_ids": ["C-01", "H-01"],
                "next_ids_by_prefix": {"H": 3, "C": 5, "Hab": 4},
            },
        }
        (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")

        cta_draft = {
            "course_id": "test_harm_append",
            "competencies": [
                {
                    "id": "H-03",
                    "name": "Dato 3",
                    "type": "fact",
                    "description": "Desc H-03",
                    "description_latex": "Desc H-03",
                    "bloom": "Remember",
                    "unit_index": 1,
                    "evidence": [{"doc": "doc.pdf", "page": 1}],
                    "prerequisites": ["C-01"],
                    "distractors": [
                        _dist("D-H03-01", page=1),
                        _dist("D-H03-02", page=1),
                        _dist("D-H03-03", page=1),
                    ],
                },
                {
                    "id": "C-05",
                    "name": "Concepto 5",
                    "type": "concept",
                    "description": "Desc C-05",
                    "description_latex": "Desc C-05",
                    "bloom": "Understand",
                    "unit_index": 2,
                    "evidence": [{"doc": "doc.pdf", "page": 2}],
                    "prerequisites": ["H-03"],
                    "distractors": [
                        _dist("D-C05-01", page=2),
                        _dist("D-C05-02", page=2),
                        _dist("D-C05-03", page=2),
                    ],
                },
            ]
        }
        (work_dir / "cta_draft.json").write_text(json.dumps(cta_draft, indent=2), encoding="utf-8")
        (work_dir / "cta_order.json").write_text(json.dumps({"order": ["H-03", "C-05"]}, indent=2), encoding="utf-8")
        (work_dir / "duplicate_candidates.json").write_text(json.dumps({"candidates": []}, indent=2), encoding="utf-8")

        harmonize_data = {
            "merges": [],
            "add_prerequisites": [
                {"competency": "C-05", "requires": ["C-01"]}
            ]
        }
        (work_dir / "cta_harmonize.json").write_text(json.dumps(harmonize_data, indent=2), encoding="utf-8")

        res = apply_harmonize(work_dir=work_dir, no_merge=True)
        assert "competencies" in res
        res_comps = res["competencies"]
        res_ids = [c["id"] for c in res_comps]
        assert res_ids == ["H-03", "C-05"]

        c05 = next(c for c in res_comps if c["id"] == "C-05")
        assert "C-01" in c05["prerequisites"]
        assert "H-03" in c05["prerequisites"]


class TestWorkspaceProtection:
    """Verifies Bottleneck #10: Active workspace protection in delete_course."""

    def test_active_workspace_protection_work_and_work_append(self, tmp_path: Path):
        """Active workspaces with fresh state files in work/ or work_append/ are never marked orphan or deleted."""
        courses_dir = tmp_path / "courses"
        courses_dir.mkdir(parents=True, exist_ok=True)

        # 1. Active course with work/pre_cta_manifest.json
        c1 = courses_dir / "active_course_1"
        (c1 / "work").mkdir(parents=True, exist_ok=True)
        (c1 / "work" / "pre_cta_manifest.json").write_text('{"course_id": "c1"}', encoding="utf-8")

        # 2. Active course with work_append/pre_cta_manifest.json
        c2 = courses_dir / "active_course_2"
        (c2 / "work_append").mkdir(parents=True, exist_ok=True)
        (c2 / "work_append" / "pre_cta_manifest.json").write_text('{"course_id": "c2"}', encoding="utf-8")

        # 3. Active course with state.json
        c3 = courses_dir / "active_course_3"
        (c3 / "work").mkdir(parents=True, exist_ok=True)
        (c3 / "work" / "state.json").write_text('{"step": 1}', encoding="utf-8")

        assert is_active_workspace(c1) is True
        assert is_active_workspace(c2) is True
        assert is_active_workspace(c3) is True
        assert is_active_workspace(c1 / "work") is True
        assert is_active_workspace(c2 / "work_append") is True

        # Test clean_orphan_course_dirs with COURSES_DIR override
        old_env = os.environ.get("COURSES_DIR")
        try:
            os.environ["COURSES_DIR"] = str(courses_dir)
            cleaned = clean_orphan_course_dirs(dry_run=True)
            # Active courses must NOT be cleaned
            assert str(c1) not in cleaned
            assert str(c2) not in cleaned
            assert str(c3) not in cleaned
        finally:
            if old_env is not None:
                os.environ["COURSES_DIR"] = old_env
            else:
                os.environ.pop("COURSES_DIR", None)
