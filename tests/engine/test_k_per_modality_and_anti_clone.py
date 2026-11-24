"""Test suite for mandatory recommended_modalities (2 <= M <= 4), K per modality (K=2/K=3),
4 deterministic anti-clone gates in compile_shard.py, and dynamic Stage 4 quotas.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
C2C_DIR = REPO_ROOT / ".agents" / "skills" / "content-to-course"

for p in (C2C_DIR, REPO_ROOT):
    p_str = str(p)
    if p_str not in sys.path:
        sys.path.insert(0, p_str)

import check_cta
import compile_cta
import cta_merge
import dispatch
import plan_shards
from compile_shard import compile_shard
from engine import stage_contract
from engine.instantiate import get_competency_quota, instantiate_competency


def _write_manifest(work_dir: Path, doc: str = "manual.pdf") -> dict:
    work_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "course_id": "test_k_course",
        "title": "Curso K Modalities",
        "files": [{"doc": doc, "file_index": 0, "total_pages": 30, "valid_page_range": [1, 30]}],
    }
    (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return manifest


def _sample_distractors(prefix: str, n: int = 6):
    return [
        (
            f"Trampa {i}",
            f"Creencia errónea {i} sobre parámetro {prefix}",
            f"Principio correcto {i}",
            f"$x_{i} = {i + 10}$",
            f"Revise minuciosamente el procedimiento formal del paso número {i} antes de enviar.",
            f"Omitió verificación del paso {i}." if i <= 2 else None,
        )
        for i in range(1, n + 1)
    ]


def _make_cta_dict_comp(cid: str = "Hab-01", ctype: str = "skill", rec_mods=None) -> dict:
    nd = 6 if ctype == "skill" else 3
    cid_clean = cid.replace("-", "")
    comp = {
        "id": cid,
        "type": ctype,
        "name": f"Competencia {cid}",
        "description_latex": r"Análisis formal de expresiones paramétricas $f(x) = ax + b$ en dominios reales.",
        "bloom": "Apply" if ctype == "skill" else "Understand",
        "prerequisites": [],
        "evidence": [{"doc": "manual.pdf", "page": 1}],
        "assumptions": [
            {
                "id": f"A-{cid_clean}-01",
                "statement_latex": r"Dominio real no degenerado $x > 0$ bajo parámetros finitos.",
                "violation_consequence": "Fuera del dominio positivo la regla pierde validez analítica.",
            }
        ],
        "distractors": [
            {
                "id": f"D-{cid_clean}-{i:02d}",
                "name": f"Error {i}",
                "trigger": f"Condición errónea #{i} en parámetro del modelo",
                "wrong_belief": f"Confunde término #{i} del modelo",
                "correct_belief": r"$f(x) = ax + b$",
                "manifestation": f"$x_{i}$",
                "error_type": "conceptual_swap",
                "severity": "high",
                "origin": "source",
                "evidence": {"doc": "manual.pdf", "page": 1},
                "remediation_hint": f"Revise detenidamente la propiedad matemática #{i} y cada parámetro del modelo.",
                "omitted_step": f"Paso omitido #{i}" if (ctype == "skill" and i <= 2) else None,
            }
            for i in range(1, nd + 1)
        ],
    }
    if rec_mods is not None:
        comp["recommended_modalities"] = rec_mods
    return comp


def _setup_shard_workspace(tmp_path: Path, cid: str, ctype: str, rec_mods: list[str], shard_code: str) -> Path:
    work = tmp_path / "work"
    shards = work / "shards"
    templates = work / "templates"
    shards.mkdir(parents=True, exist_ok=True)
    templates.mkdir(parents=True, exist_ok=True)
    _write_manifest(work)
    comp = _make_cta_dict_comp(cid=cid, ctype=ctype, rec_mods=rec_mods)
    cta = {
        "contract_version": 2,
        "course_id": "test_k_course",
        "title": "Curso K Modalities",
        "macro_competency": "Dominio integral",
        "competencies": [comp],
    }
    (work / "cta.json").write_text(json.dumps(cta, indent=2, ensure_ascii=False), encoding="utf-8")
    (shards / "pre_shard_manifest.json").write_text(
        json.dumps(
            {
                "min_archetypes": 4,
                "stage4_contract": stage_contract.global_contract(),
                "shards": [
                    {
                        "shard_id": "shard_01",
                        "min_archetypes": 4,
                        "competency_ids": [cid],
                        "competencies": [comp],
                    }
                ],
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    (shards / "shard_01_data.py").write_text(shard_code, encoding="utf-8")
    return work


class TestStageContractScaling:
    def test_required_templates_and_quotas_k2_and_k3(self):
        assert stage_contract.MIN_MODALITIES_PER_COMPETENCY == 2
        assert stage_contract.MAX_MODALITIES_PER_COMPETENCY == 4
        assert stage_contract.DEFAULT_TEMPLATES_PER_MODALITY >= 2

        assert [stage_contract.required_templates_for_competency(m, 2) for m in (2, 3, 4)] == [4, 6, 8]
        assert [stage_contract.required_templates_for_competency(m, 3) for m in (2, 3, 4)] == [6, 9, 12]
        assert stage_contract.required_templates_for_competency(0, 2) == 4

        assert [stage_contract.quota_for_competency("skill", n) for n in (4, 6, 8)] == [30, 30, 32]
        assert [stage_contract.quota_for_competency("concept", n) for n in (4, 6, 8)] == [20, 20, 24]
        assert [stage_contract.quota_for_competency("skill", n) for n in (6, 9, 12)] == [30, 36, 48]
        assert [stage_contract.quota_for_competency("fact", n) for n in (6, 9, 12)] == [20, 27, 36]

    def test_contract_tokens_and_drift_support_k_overrides(self):
        rendered = stage_contract.render_contract_tokens(
            "K=<<S4_TPL_PER_MOD>>, M in [<<S4_MIN_MODS>>..<<S4_MAX_MODS>>]"
        )
        assert rendered == f"K={stage_contract.DEFAULT_TEMPLATES_PER_MODALITY}, M in [2..4]"

        gc_k3 = stage_contract.global_contract(templates_per_modality=3)
        assert gc_k3["templates_per_modality"] == 3
        assert stage_contract.contract_drift(gc_k3) == ""

        legacy_gc = {
            "version": stage_contract.CONTRACT_VERSION,
            "quota_skill": stage_contract.QUOTA_SKILL,
            "quota_other": stage_contract.QUOTA_OTHER,
            "min_diversity_ratio": stage_contract.MIN_DIVERSITY_RATIO,
            "min_archetypes": stage_contract.MIN_ARCHETYPES,
        }
        assert stage_contract.contract_drift(legacy_gc) == ""
        assert "must be an int >= 1" in stage_contract.contract_drift({**gc_k3, "templates_per_modality": 0})


class TestCtaModalityEnforcementAndMerge:
    def test_compile_cta_module_rejects_missing_and_out_of_range_and_allows_v1_override(self):
        base_tuple = (
            "skill",
            "Hab-01",
            "Cálculo Afín",
            r"Evalúa expresiones afines $f(x) = ax + b$ con parámetros reales positivos.",
            "Apply",
            "manual.pdf",
            1,
            [],
            _sample_distractors("Hab01", 6),
            [("A-Hab01-01", r"Dominio real positivo $x > 0$.", "Fuera de dominio falla la evaluación.")],
        )

        with pytest.raises(ValueError, match=r"\[CTA-MODALITY-MISSING\]"):
            compile_cta.compile_cta_module([base_tuple], require_assumptions=True, contract_version=2)

        with pytest.raises(ValueError, match=r"\[CTA-MODALITY-MISSING\]"):
            compile_cta.compile_cta_module([(*base_tuple, [])], require_assumptions=True, contract_version=2)

        with pytest.raises(ValueError, match=r"\[CTA-MODALITY-RANGE\]"):
            compile_cta.compile_cta_module([(*base_tuple, ["FIB"])], require_assumptions=True, contract_version=2)

        with pytest.raises(ValueError, match=r"\[CTA-MODALITY-RANGE\]"):
            compile_cta.compile_cta_module(
                [(*base_tuple, ["FIB", "MS", "open_symbolic", "proof_dag", "adversarial_break"])],
                require_assumptions=True,
                contract_version=2,
            )

        with pytest.raises(ValueError, match=r"\[M20-MC7-CAP\]"):
            compile_cta.compile_cta_module([(*base_tuple, ["MC7", "FIB"])], require_assumptions=True, contract_version=2)

        for mods in (["FIB", "open_symbolic"], ["FIB", "MS", "open_symbolic"], ["FIB", "MS", "open_symbolic", "proof_dag"]):
            out = compile_cta.compile_cta_module([(*base_tuple, mods)], require_assumptions=True, contract_version=2)
            assert len(out["competencies"][0]["recommended_modalities"]) == len(mods)

        legacy_out = compile_cta.compile_cta_module(
            [base_tuple], require_assumptions=True, contract_version=2, require_modalities=False
        )
        assert "recommended_modalities" not in legacy_out["competencies"][0]

    def test_check_cta_rules_and_part_enforce_missing_range_and_duplicates(self, tmp_path: Path):
        manifest = _write_manifest(tmp_path)

        cta_missing = {
            "contract_version": 2,
            "course_id": "c_test",
            "title": "Test",
            "competencies": [_make_cta_dict_comp("Hab-01", "skill", rec_mods=None)],
        }
        res_m = check_cta.validate_cta_rules(cta_missing, manifest_data=manifest, require_assumptions=True)
        assert not res_m.valid and any("[CTA-MODALITY-MISSING]" in e for e in res_m.errors)

        cta_empty = {**cta_missing, "competencies": [_make_cta_dict_comp("Hab-01", "skill", rec_mods=[])]}
        res_e = check_cta.check_cta_part(cta_empty, manifest_data=manifest, require_assumptions=True)
        assert not res_e.valid and any("[CTA-MODALITY-MISSING]" in e for e in res_e.errors)

        cta_one = {
            **cta_missing,
            "competencies": [_make_cta_dict_comp("Hab-01", "skill", rec_mods=["fill_in_the_blank"])],
        }
        res_1 = check_cta.validate_cta_rules(cta_one, manifest_data=manifest, require_assumptions=True)
        assert not res_1.valid and any("[CTA-MODALITY-RANGE]" in e for e in res_1.errors)

        cta_five = {
            **cta_missing,
            "competencies": [
                _make_cta_dict_comp(
                    "Hab-01",
                    "skill",
                    rec_mods=[
                        "fill_in_the_blank",
                        "open_symbolic",
                        "multiple_select",
                        "proof_dag",
                        "adversarial_break",
                    ],
                )
            ],
        }
        res_5 = check_cta.validate_cta_rules(cta_five, manifest_data=manifest, require_assumptions=True)
        assert not res_5.valid and any("[CTA-MODALITY-RANGE]" in e for e in res_5.errors)

        cta_dup = {
            **cta_missing,
            "competencies": [_make_cta_dict_comp("Hab-01", "skill", rec_mods=["fill_in_the_blank", "fill_in_the_blank"])],
        }
        res_dup = check_cta.validate_cta_rules(cta_dup, manifest_data=manifest, require_assumptions=True)
        assert not res_dup.valid and any("[CTA-MODALITY-RANGE]" in e for e in res_dup.errors)

        res_legacy = check_cta.validate_cta_rules(
            cta_missing, manifest_data=manifest, require_assumptions=True, require_modalities=False
        )
        assert res_legacy.valid, res_legacy.errors

    def test_cta_merge_case_b_truncates_union_to_max_4_preserving_survivor_order(self, tmp_path: Path):
        work = tmp_path / "work_merge"
        _write_manifest(work)

        c1 = _make_cta_dict_comp("C-01", "concept", rec_mods=["open_symbolic", "proof_dag", "unstructured_model"])
        c2 = _make_cta_dict_comp(
            "C-02",
            "concept",
            rec_mods=["concept_matching", "adversarial_break", "fill_in_the_blank", "open_symbolic"],
        )
        c2["prerequisites"] = []
        draft = {
            "contract_version": 2,
            "course_id": "test_k_course",
            "title": "Curso Merge",
            "macro_competency": "Macro",
            "competencies": [c1, c2],
        }
        harmonize = {
            "duplicate_decisions": [
                {
                    "pair": ["C-01", "C-02"],
                    "decision": "merge",
                    "keep_id": "C-01",
                    "drop_id": "C-02",
                    "reason": "Equivalentes",
                }
            ],
            "add_prerequisites": [],
            "rename": [],
            "drop_duplicate_distractors": [],
        }
        (work / "cta_draft.json").write_text(json.dumps(draft, indent=2), encoding="utf-8")
        (work / "cta_order.json").write_text(json.dumps({"order": ["C-01", "C-02"]}, indent=2), encoding="utf-8")
        (work / "duplicate_candidates.json").write_text(
            json.dumps({"candidates": [{"pair": ["C-01", "C-02"], "reason": "Equivalentes"}]}, indent=2),
            encoding="utf-8",
        )
        (work / "cta_harmonize.json").write_text(json.dumps(harmonize, indent=2), encoding="utf-8")

        cta_out = cta_merge.apply_harmonize(work)
        merged = cta_out["competencies"][0]
        assert merged["recommended_modalities"] == [
            "open_symbolic",
            "proof_dag",
            "unstructured_model",
            "concept_matching",
        ]


class TestPlanShardsAndDispatchScaling:
    def test_plan_shards_and_dispatch_propagate_k2_k3_and_auto_shrink_at_k3(self, tmp_path: Path):
        work = tmp_path / "work_plan"
        _write_manifest(work)
        comps = [
            _make_cta_dict_comp("Hab-01", "skill", rec_mods=["open_symbolic", "fill_in_the_blank", "multiple_select"]),
            _make_cta_dict_comp("Hab-02", "skill", rec_mods=["fill_in_the_blank", "open_symbolic", "proof_dag", "adversarial_break"]),
            _make_cta_dict_comp("C-01", "concept", rec_mods=["concept_matching", "unstructured_model"]),
            _make_cta_dict_comp("C-02", "concept", rec_mods=["open_symbolic", "proof_dag", "adversarial_break"]),
            _make_cta_dict_comp("C-03", "concept", rec_mods=["fill_in_the_blank", "multiple_select"]),
        ]
        comps[1]["prerequisites"] = ["Hab-01"]
        comps[2]["prerequisites"] = ["C-01"] if False else ["Hab-01"]
        comps[3]["prerequisites"] = ["C-01"]
        comps[4]["prerequisites"] = ["C-02"]
        cta = {
            "contract_version": 2,
            "course_id": "test_k_course",
            "title": "Curso Plan",
            "macro_competency": "Macro",
            "competencies": comps,
        }
        cta_path = work / "cta.json"
        cta_path.write_text(json.dumps(cta, indent=2, ensure_ascii=False), encoding="utf-8")

        # K = 2 default (Complexity-Weighted Sharding: DEFAULT_COMPS_PER_SHARD=2, MAX_SKILLS_PER_SHARD=1)
        res_k2 = plan_shards.plan_shards(cta_path, work / "shards_k2", templates_per_modality=2)
        assert res_k2["templates_per_modality"] == 2
        assert res_k2["max_skills_per_shard"] == 1
        assert res_k2["comps_per_shard"] == 2
        s4_k2 = {cid: c for s in res_k2["shards"] for cid, c in s["stage4_contract"].items()}
        assert s4_k2["Hab-01"]["min_templates_required"] == 6
        assert s4_k2["Hab-01"]["quota"] == 30
        assert s4_k2["Hab-02"]["min_templates_required"] == 8
        assert s4_k2["Hab-02"]["quota"] == 32
        assert s4_k2["C-01"]["min_templates_required"] == 4
        assert s4_k2["C-01"]["quota"] == 20

        # K = 3 auto-adjusts shard capacities and scales quotas
        res_k3 = plan_shards.plan_shards(cta_path, work / "shards", templates_per_modality=3)
        assert res_k3["templates_per_modality"] == 3
        assert res_k3["max_skills_per_shard"] == 1
        assert res_k3["comps_per_shard"] == 2
        s4_k3 = {cid: c for s in res_k3["shards"] for cid, c in s["stage4_contract"].items()}
        assert s4_k3["Hab-01"]["min_templates_required"] == 9
        assert s4_k3["Hab-01"]["quota"] == 36
        assert s4_k3["Hab-02"]["min_templates_required"] == 12
        assert s4_k3["Hab-02"]["quota"] == 48
        assert s4_k3["C-02"]["min_templates_required"] == 9
        assert s4_k3["C-02"]["quota"] == 27

        # Dispatch authors propagates M, K, min_tpls and --templates-per-modality 3
        disp = dispatch.dispatch_authors(work_dir=work, pointer=True)
        assert len(disp["Subagents"]) >= 4
        author_01_md = (work / "dispatch" / "items" / "author_01_data.md").read_text(encoding="utf-8")
        assert "--templates-per-modality 3" in author_01_md
        assert "obligatorio >= 3 plantillas distintas por modalidad" in author_01_md

    def test_dispatch_authors_and_build_cli_accept_templates_per_modality_override(self, tmp_path: Path):
        import subprocess

        work = tmp_path / "work_cli_override"
        _write_manifest(work)
        comps = [
            _make_cta_dict_comp("C-01", "concept", rec_mods=["mc7", "open_text"]),
            _make_cta_dict_comp("Hab-01", "skill", rec_mods=["open_symbolic", "fill_in_the_blank"]),
        ]
        cta = {
            "contract_version": 2,
            "course_id": "test_k_course",
            "title": "Curso CLI Override",
            "macro_competency": "Macro",
            "competencies": comps,
        }
        cta_path = work / "cta.json"
        cta_path.write_text(json.dumps(cta, indent=2, ensure_ascii=False), encoding="utf-8")

        # Initial plan has K=2
        res_k2 = plan_shards.plan_shards(cta_path, work / "shards", templates_per_modality=2)
        assert res_k2["templates_per_modality"] == 2

        # 1. dispatch-authors CLI with --templates-per-modality 3 overrides K=2 manifest
        proc_da = subprocess.run(
            [
                sys.executable,
                str(C2C_DIR / "dispatch.py"),
                "dispatch-authors",
                "--work-dir",
                str(work),
                "--templates-per-modality",
                "3",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert proc_da.returncode == 0, f"dispatch-authors failed: {proc_da.stderr}"
        author_01_md = (work / "dispatch" / "items" / "author_01_data.md").read_text(encoding="utf-8")
        assert "--templates-per-modality 3" in author_01_md
        assert "templates_per_modality:** `3`" in author_01_md
        assert ">= 3 plantillas distintas" in author_01_md

        # 2. build --role author CLI with --templates-per-modality 3 also succeeds and overrides K=2
        (work / "dispatch" / "items" / "author_01_data.md").unlink()
        proc_build = subprocess.run(
            [
                sys.executable,
                str(C2C_DIR / "dispatch.py"),
                "build",
                "--role",
                "author",
                "--work-dir",
                str(work),
                "--templates-per-modality",
                "3",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert proc_build.returncode == 0, f"dispatch.py build failed: {proc_build.stderr}"
        author_01_md_build = (work / "dispatch" / "items" / "author_01_data.md").read_text(encoding="utf-8")
        assert "--templates-per-modality 3" in author_01_md_build
        assert "templates_per_modality:** `3`" in author_01_md_build
        assert ">= 3 plantillas distintas" in author_01_md_build


_RATS_HEADER = r'''
RATS = {
    "D-Hab01-01": r"Resta el intercepto $@b@$ al operar con pendiente $@a@$ en vez de sumarlo.",
    "D-Hab01-02": r"Omite el intercepto $@b@$ devolviendo solo el producto parcial en $@a@$.",
    "D-Hab01-03": r"Agrupa $@b@$ dentro del factor $@a@$ alterando la suma independiente de $@b@$.",
    "D-Hab01-04": r"Omite la pendiente $@a@$ y opera directamente la entrada frente a $@b@$.",
    "D-Hab01-05": r"Suma linealmente $@a@$ y $@b@$ en vez de evaluar el producto completo con $@a@$.",
    "D-Hab01-06": r"Intercambia pendiente $@a@$ con intercepto $@b@$ al plantear la regla lineal.",
}
def _pv(c):
    for t in reversed("".join(x if x in "0123456789.eE+-" else " " for x in str(c)).split()):
        try: return float(t.rstrip("."))
        except ValueError: pass
    return float("nan")
def _o(v, d, e):
    return {"value": v, "is_correct": d is None} | ({"distractor_id": d, "error_rationale": e} if d else {})
'''


class TestCompileShardModalityFloorAndAntiClone:
    def test_rejects_3_mc7_plus_1_open_symbolic_for_m2_k2(self, tmp_path: Path):
        code = _RATS_HEADER + r'''
def gen_1(r):
    a, x, b = r.randint(3, 25), r.randint(10, 50), r.randint(5, 30)
    ans = a * x + b
    ds = [(f"D-Hab01-{i:02d}", str(ans + i * 3), RATS[f"D-Hab01-{i:02d}"]) for i in range(1, 7)]
    return {"vars": {"a": a, "x": x, "b": b, "ans": ans}, "correct": str(ans), "ds": ds}
def gen_2(r):
    a, x, b = r.randint(3, 25), r.randint(12, 52), r.randint(6, 32)
    ans = x * x + a - b
    ds = [(f"D-Hab01-{i:02d}", str(ans + i * 4), RATS[f"D-Hab01-{i:02d}"]) for i in range(1, 7)]
    return {"vars": {"a": a, "x": x, "b": b, "ans": ans}, "correct": str(ans), "ds": ds}
def gen_3(r):
    a, b, d = r.randint(3, 25), r.randint(5, 30), r.randint(2, 18)
    ans = (a + d) * b + a
    ds = [(f"D-Hab01-{i:02d}", str(ans + i * 5), RATS[f"D-Hab01-{i:02d}"]) for i in range(1, 7)]
    return {"vars": {"a": a, "b": b, "d": d, "ans": ans}, "correct": str(ans), "ds": ds}
def gen_4(r):
    a, b = r.randint(2, 25), r.randint(3, 35)
    return {"vars": {"a": a, "b": b, "ans": f"{a}*x+{b}"}, "correct": f"{a}*x+{b}", "variables": ["x"], "symbolic_config": {"variables": ["x"]}}
def ver_1(c, v): return abs(_pv(c) - (v["a"] * v["x"] + v["b"])) < 1e-4
def ver_2(c, v): return abs(_pv(c) - (v["x"] * v["x"] + v["a"] - v["b"])) < 1e-4
def ver_3(c, v): return abs(_pv(c) - ((v["a"] + v["d"]) * v["b"] + v["a"])) < 1e-4
def ver_4(c, v): return str(c).replace(" ", "") == f"{v['a']}*x+{v['b']}"
S1 = [r"Evalúa $f(@x@)=@a@(@x@)+@b@$:", r"Calcula regla afín $@a@(@x@)+@b@$:", r"Obtén $y$ para $x=@x@$ con $@a@,@b@$:", r"Determina valor directo en $@x@$ con $@a@,@b@$:"]
S2 = [r"Invierte expresión cuadrática $@x@^2+@a@-@b@$:", r"Calcula diferencia $@x@^2+@a@-@b@$:", r"Halla magnitud inversa usando $@x@,@a@,@b@$:", r"Resuelve $@x@^2+@a@-@b@$ exactamente:"]
S3 = [r"Con choque $@d@$ calcula $(@a@+@d@)@b@+@a@$:", r"Perturba $@a@$ por $@d@$ y multiplica por $@b@$:", r"Evalúa variante desplazada con $@a@,@b@,@d@$:", r"Determina producto perturbado de $@a@+@d@$ y $@b@$:"]
S4 = [r"Escribe fórmula simbólica en variable $x$ con pendiente $@a@$ e intercepto $@b@$:", r"Expresa $f(x)$ con pendiente $@a@$ y término $@b@$:", r"Modela en variable $x$ la recta de parámetros $@a@,@b@$:", r"Define analíticamente en $x$ la recta lineal usando $@a@,@b@$:"]
H1 = [r"Identifica pendiente $@a@$ en la regla.", r"Aplica término independiente $@b@$.", r"Verifica signos al multiplicar."]
H2 = [r"Eleva $@x@$ al cuadrado antes de sumar $@a@$.", r"Resta el parámetro $@b@$ al final.", r"Revisa la prioridad aritmética."]
H3 = [r"Suma primero el desplazamiento $@d@$ a $@a@$.", r"Multiplica la suma por $@b@$.", r"Agrega $@a@$ tras el producto."]
H4 = [r"Escribe coeficiente $@a@$ multiplicando a x.", r"Añade intercepto $@b@$ como suma.", r"Usa sintaxis simbólica estándar en x."]
SOL = r"Paso 1: Sustituimos parámetros reales en la expresión dada. Paso 2: Evaluamos el resultado exacto @ans@."
TEMPLATES = [
    {"id": "T-Hab-01-01", "cid": "Hab-01", "qtype": "FIB", "archetype": "direct", "band": ("easy", "Apply"), "gen": gen_1, "ver": ver_1, "stem_variants": S1, "hints": H1, "sol": SOL, "rats": RATS},
    {"id": "T-Hab-01-02", "cid": "Hab-01", "qtype": "FIB", "archetype": "inverse", "band": ("medium", "Apply"), "gen": gen_2, "ver": ver_2, "stem_variants": S2, "hints": H2, "sol": SOL, "rats": RATS},
    {"id": "T-Hab-01-03", "cid": "Hab-01", "qtype": "FIB", "archetype": "perturbation", "band": ("hard", "Analyze"), "gen": gen_3, "ver": ver_3, "stem_variants": S3, "hints": H3, "sol": SOL, "rats": RATS},
    {"id": "T-Hab-01-04", "cid": "Hab-01", "qtype": "open_symbolic", "archetype": "boundary_or_edge_case", "assumption_id": "A-Hab01-01", "band": ("hard", "Evaluate"), "gen": gen_4, "ver": ver_4, "stem_variants": S4, "hints": H4, "sol": SOL},
]
'''
        work = _setup_shard_workspace(tmp_path / "k2", "Hab-01", "skill", ["fill_in_the_blank", "open_symbolic"], code)
        ok, errs = compile_shard(work, shard_id="shard_01", strict=True, seeds=30, min_archetypes=4, templates_per_modality=2)
        joined = "\n".join(errs)
        assert not ok and "[CTA-MODALITY-PLAN]" in joined and "'open_symbolic' solo tiene 1/2" in joined

        # Explicit legacy K=1 override permits 3 FIB + 1 open_symbolic across 2 modalities
        work_k1 = _setup_shard_workspace(tmp_path / "k1", "Hab-01", "skill", ["fill_in_the_blank", "open_symbolic"], code)
        ok_k1, errs_k1 = compile_shard(work_k1, shard_id="shard_01", strict=True, seeds=30, min_archetypes=4, templates_per_modality=1)
        assert ok_k1 and errs_k1 == [], errs_k1

    def test_rejects_4_templates_for_m3_k2_and_passes_6_valid_templates(self, tmp_path: Path):
        # Extract the verified 6-template Hab-01 code from prompt_shard_author.md
        import re
        sa_txt = (C2C_DIR / "system_prompts" / "prompt_shard_author.md").read_text(encoding="utf-8")
        hab_code = [b for b in re.findall(r"```python\s+(.*?)```", sa_txt, re.DOTALL) if "TEMPLATES" in b][0]

        work_ok = _setup_shard_workspace(
            tmp_path / "m3_ok",
            "Hab-01",
            "skill",
            ["fill_in_the_blank", "open_symbolic", "multiple_select"],
            hab_code,
        )
        ok, errs = compile_shard(work_ok, shard_id="shard_01", strict=True, seeds=30, min_archetypes=4, templates_per_modality=2)
        assert ok and errs == [], errs

        # Trim to 4 templates (violates 3 * 2 = 6 minimum and MS count 0 < 2)
        short_code = hab_code.replace(
            "{'id':'T-Hab-01-05'", "# trimmed\n# {'id':'T-Hab-01-05'"
        ).replace(
            "{'id':'T-Hab-01-06'", "# {'id':'T-Hab-01-06'"
        )
        work_bad = _setup_shard_workspace(
            tmp_path / "m3_short",
            "Hab-01",
            "skill",
            ["fill_in_the_blank", "open_symbolic", "multiple_select"],
            short_code,
        )
        ok_b, errs_b = compile_shard(work_bad, shard_id="shard_01", strict=True, seeds=15, min_archetypes=4, templates_per_modality=2)
        assert not ok_b and "[CTA-MODALITY-PLAN]" in "\n".join(errs_b)

        # Even at K=1, omitting 'multiple_select' still fails [CTA-MODALITY-PLAN]
        ok_legacy, _ = compile_shard(
            work_bad, shard_id="shard_01", strict=True, seeds=15, min_archetypes=4, templates_per_modality=1
        )
        assert not ok_legacy

    def test_k3_m2_passes_with_6_distinct_templates_and_k1_legacy_passes(self, tmp_path: Path):
        code_k3 = _RATS_HEADER + r'''
def gen_1(r):
    a, x = r.randint(3, 35), r.randint(4, 40)
    ans = a * x + 7
    rat = r"Resta constante 7 tras multiplicar $@a@$ y $@x@$ en vez de sumarla."
    return {"vars": {"a": a, "x": x, "ans": ans}, "correct": str(ans), "ds": [("D-Hab01-01", str(a * x - 7), rat)]}
def gen_2(r):
    a, b, x = r.randint(3, 25), r.randint(5, 35), r.randint(4, 30)
    y = a * x + b
    rat = r"Despeja restando $@b@$ de $@y@$ sin dividir por pendiente $@a@$."
    return {"vars": {"a": a, "b": b, "y": y, "ans": x}, "correct": str(x), "ds": [("D-Hab01-04", str(y - b), rat)]}
def gen_3(r):
    a, x, d = r.randint(3, 25), r.randint(4, 30), r.randint(2, 20)
    ans = a * (x * x + d)
    rat = r"Omite elevar $@x@$ al cuadrado al combinar con constante $@d@$ y factor $@a@$."
    return {"vars": {"a": a, "x": x, "d": d, "ans": ans}, "correct": str(ans), "ds": [("D-Hab01-02", str(a * (x + d)), rat)]}
def gen_4(r):
    a, x, b = r.randint(4, 25), r.randint(5, 30), r.randint(26, 50)
    r1 = r"Resta el término $@b@$ al producto $@a@\cdot@x@$ en lugar de sumarlo."
    r2 = r"Multiplica pendiente $@a@$ por suma $(@x@+@b@)$ distribuyendo erróneamente."
    r3 = r"Omite el producto $@a@\cdot@x@$ y conserva solo el intercepto $@b@$."
    return {"vars": {"a": a, "x": x, "b": b}, "options": [
        _o(f"$y = {a*x+b}$", None, None), _o(f"$y > {b}$", None, None), _o(f"$y > {a}$", None, None),
        _o(f"$y = {a*x-b}$", "D-Hab01-01", r1), _o(f"$y = {a*(x+b)}$", "D-Hab01-05", r2),
        _o(f"$y = {b}$", "D-Hab01-02", r3), _o(f"$y = {a*x+2*b}$", "D-Hab01-01", r1),
    ]}
def gen_5(r):
    a, d = r.randint(4, 22), r.randint(3, 18)
    b = a * d + r.randint(11, 45)
    r1 = r"Suma linealmente $@a@$ y $@d@$ confundiendo adición con tasa por paso."
    r2 = r"Toma parámetro auxiliar $@b@$ como incremento en lugar de $@a@\cdot@d@$."
    r3 = r"Invierte el signo del incremento por paso respecto a $@a@$ y $@d@$."
    return {"vars": {"a": a, "d": d, "b": b}, "options": [
        _o(f"$\\Delta y = {a*d}$", None, None), _o(f"$\\Delta y > 0$ ($a={a}$)", None, None),
        _o(f"$\\Delta y = {a+d}$", "D-Hab01-03", r1), _o(f"$\\Delta y = {b}$", "D-Hab01-06", r2),
        _o(f"$\\Delta y = {-a*d}$", "D-Hab01-01", r3), _o(f"$\\Delta y = {a*d+b}$", "D-Hab01-06", r2),
        _o(f"$\\Delta y = {2*a*d}$", "D-Hab01-03", r1),
    ]}
def gen_6(r):
    a, x, b = -r.randint(4, 22), r.randint(5, 25), r.randint(6, 32)
    r1 = r"Resta $@b@$ al término negativo $@a@\cdot@x@$ en lugar de sumarlo."
    r2 = r"Distribuye pendiente negativa $@a@$ sobre el intercepto $@b@$ en $x=@x@$."
    r3 = r"Omite el término lineal $@a@\cdot@x@$ dejando solo el intercepto $@b@$."
    return {"vars": {"a": a, "x": x, "b": b}, "options": [
        _o(f"$f({x}) = {a*x+b}$", None, None), _o(f"$f({x}) < {b}$", None, None),
        _o(f"$f({x}) = {a*x-b}$", "D-Hab01-01", r1), _o(f"$f({x}) = {a*(x+b)}$", "D-Hab01-03", r2),
        _o(f"$f({x}) = {b}$", "D-Hab01-02", r3), _o(f"$f({x}) = {a*x+2*b}$", "D-Hab01-01", r1),
        _o(f"$f({x}) = {2*a*x+b}$", "D-Hab01-03", r2),
    ]}
def ver_1(c, v): return abs(_pv(c) - (v["a"] * v["x"] + 7)) < 1e-4
def ver_2(c, v): return abs(_pv(c) - (v["y"] - v["b"]) / v["a"]) < 1e-4
def ver_3(c, v): return abs(_pv(c) - (v["a"] * (v["x"] ** 2 + v["d"]))) < 1e-4
def _ms_chk(r, cond):
    o = r.get("options", []) if isinstance(r, dict) else []
    t = [u for u in o if u.get("is_correct") is True]
    f = [u for u in o if u.get("is_correct") is False]
    return len(o) >= 5 and len(t) >= 2 and len(f) >= 2 and cond(t, f) and all(u.get("distractor_id") in RATS and len(u.get("error_rationale", "")) >= 20 for u in f)
def ver_4(r):
    v = r.get("vars", {}); val = v.get("a", 0) * v.get("x", 0) + v.get("b", 0)
    return _ms_chk(r, lambda t, f: any(_pv(u["value"]) == val for u in t) and any(">" in u["value"] for u in t) and all(_pv(u["value"]) != val for u in f))
def ver_5(r):
    v = r.get("vars", {}); dv = v.get("a", 0) * v.get("d", 0)
    return _ms_chk(r, lambda t, f: any(_pv(u["value"]) == dv for u in t) and any(">" in u["value"] for u in t) and all(_pv(u["value"]) != dv for u in f))
def ver_6(r):
    v = r.get("vars", {}); fv = v.get("a", 0) * v.get("x", 0) + v.get("b", 0)
    return v.get("a", 0) < 0 and _ms_chk(r, lambda t, f: any(_pv(u["value"]) == fv for u in t) and any("<" in u["value"] for u in t) and all(_pv(u["value"]) != fv for u in f))
S1 = [r"Calcule evaluación afín $@a@(@x@)+7$:", r"Halle $@a@x+7$ en $x=@x@$:", r"Evalúe expresión directa con $@a@,@x@$:", r"Determine suma afín $@a@ \cdot @x@ + 7$:"]
S2 = [r"Despeje raíz $x$ de $@a@x+@b@=@y@$:", r"Aísle variable $x$ cuando $@a@x+@b@=@y@$:", r"Encuentre incógnita en $@a@x+@b@=@y@$:", r"Calcule abscisa solución de $@a@x+@b@=@y@$:"]
S3 = [r"Evalúe función cuadrática $@a@(@x@^2+@d@)$:", r"Calcule producto perturbado $@a@(@x@^2+@d@)$:", r"Obtenga salida cuadrática con $@a@,@x@,@d@$:", r"Determine magnitud $@a@(@x@^2+@d@)$:"]
S4 = [r"Dada pendiente $@a@>0$, $x=@x@$ e intercepto $@b@$, marque ciertas:", r"Con $@a@>0, b=@b@$ en $x=@x@$, elija válidas:", r"Seleccione propiedades verdaderas para $y=@a@x+@b@$:", r"Identifique valores reales de $y=@a@x+@b@$ en $@x@$:" ]
S5 = [r"Pendiente $@a@>0$ y paso $@d@>0$ ($b=@b@$): marque incremento:", r"Calcule cambio $\Delta y$ al aumentar $@d@$ con pendiente $@a@$:", r"Propiedades válidas de $\Delta y = @a@ \cdot @d@$ ($b=@b@$):", r"Escoja afirmaciones exactas sobre variación $\Delta y$:"]
S6 = [r"Con pendiente negativa $@a@<0$ en $x=@x@$, marque válidas:", r"Para $@a@<0$, $b=@b@$ y $x=@x@$, seleccione ciertas:", r"Evalúe propiedades de frontera negativa $@a@<0$:", r"Decida cuáles relaciones valen bajo $@a@<0, b=@b@$:" ]
H1 = [r"Multiplique factor $@a@$ por $@x@$.", r"Sume el desplazamiento positivo 7.", r"Verifique aritmética entera final."]
H2 = [r"Reste $@b@$ en ambos miembros de $@y@$.", r"Divida la diferencia entre $@a@$.", r"Compruebe sustituyendo en $@a@x+@b@$."]
H3 = [r"Eleve $@x@$ al cuadrado antes de sumar $@d@$.", r"Multiplique el paréntesis por $@a@$.", r"Revise jerarquía de potencias."]
H4 = [r"Evalúe $@a@ \cdot @x@ + @b@$ con signo positivo.", r"Compare producto frente al intercepto $@b@$.", r"Marque ambas afirmaciones verdaderas."]
H5 = [r"Recuerde que $\Delta y$ depende de $@a@$ y $@d@$.", r"El intercepto $@b@$ se cancela en diferencias.", r"Selección múltiple de dos opciones."]
H6 = [r"Pendiente negativa $@a@<0$ decrece con $@x@>0$.", r"Compare valor resultante contra cota $@b@$.", r"Verifique signos negativos al sumar."]
SOL = r"Paso 1: Identificamos los parámetros reales de la instancia. Paso 2: Evaluamos cada expresión respetando signos y orden."
TEMPLATES = [
    {"id": "T-Hab-01-01", "cid": "Hab-01", "qtype": "FIB", "archetype": "direct", "band": ("easy", "Apply"), "gen": gen_1, "ver": ver_1, "stem_variants": S1, "hints": H1, "sol": SOL, "rats": RATS},
    {"id": "T-Hab-01-02", "cid": "Hab-01", "qtype": "FIB", "archetype": "inverse", "band": ("medium", "Apply"), "gen": gen_2, "ver": ver_2, "stem_variants": S2, "hints": H2, "sol": SOL, "rats": RATS},
    {"id": "T-Hab-01-03", "cid": "Hab-01", "qtype": "FIB", "archetype": "perturbation", "band": ("hard", "Analyze"), "gen": gen_3, "ver": ver_3, "stem_variants": S3, "hints": H3, "sol": SOL, "rats": RATS},
    {"id": "T-Hab-01-04", "cid": "Hab-01", "qtype": "MS", "archetype": "direct", "band": ("easy", "Analyze"), "gen": gen_4, "ver": ver_4, "stem_variants": S4, "hints": H4, "sol": SOL, "rats": RATS},
    {"id": "T-Hab-01-05", "cid": "Hab-01", "qtype": "MS", "archetype": "perturbation", "band": ("medium", "Evaluate"), "gen": gen_5, "ver": ver_5, "stem_variants": S5, "hints": H5, "sol": SOL, "rats": RATS},
    {"id": "T-Hab-01-06", "cid": "Hab-01", "qtype": "MS", "archetype": "boundary_or_edge_case", "assumption_id": "A-Hab01-01", "band": ("hard", "Evaluate"), "gen": gen_6, "ver": ver_6, "stem_variants": S6, "hints": H6, "sol": SOL, "rats": RATS},
]
'''
        work = _setup_shard_workspace(tmp_path / "k3", "Hab-01", "skill", ["fill_in_the_blank", "multiple_select"], code_k3)
        ok, errs = compile_shard(work, shard_id="shard_01", strict=True, seeds=30, min_archetypes=4, templates_per_modality=3)
        assert ok and errs == [], errs

        # Same 6-template shard also satisfies legacy K=1
        work_k1 = _setup_shard_workspace(tmp_path / "k1_from_6", "Hab-01", "skill", ["fill_in_the_blank", "multiple_select"], code_k3)
        ok_k1, errs_k1 = compile_shard(work_k1, shard_id="shard_01", strict=True, seeds=30, min_archetypes=4, templates_per_modality=1)
        assert ok_k1 and errs_k1 == [], errs_k1

    def test_anti_clone_ast_band_stem_and_sympy_gates(self, tmp_path: Path):
        # 1. [TPL-CLONE-AST]: renamed locals + changed numeric literals + swapped D-id/rationale in gen
        code_ast = _RATS_HEADER + r'''
def gen_1(r):
    a, b = r.randint(4, 40), r.randint(5, 45)
    val = a * b + 5
    return {"vars": {"a": a, "b": b, "ans": val}, "correct": str(val), "ds": [("D-Hab01-01", str(a * b - 5), r"Resta el constante 5 tras multiplicar $@a@$ y $@b@$ en lugar de sumarlo.")]}
def gen_2(r):
    p, q = r.randint(7, 50), r.randint(9, 55)
    res = p * q + 11
    return {"vars": {"p": p, "q": q, "ans": res}, "correct": str(res), "ds": [("D-Hab01-02", str(p * q - 11), r"Resta el desplazamiento 11 al producto de $@p@$ por $@q@$ en vez de sumarlo.")]}
def gen_3(r):
    m, k = r.randint(4, 30), r.randint(3, 25)
    rm1 = r"Resta $@k@$ de $@m@$ ignorando adición positiva de ambos términos."
    rm2 = r"Multiplica $@m@$ y $@k@$ confundiendo suma con área rectangular."
    return {"vars": {"m": m, "k": k}, "options": [_o(f"${m+k}$", None, None), _o(f"${m+k}>0$", None, None), _o(f"${m+k}>1$", None, None), _o(f"${m-k}$", "D-Hab01-03", rm1), _o(f"${m*k}$", "D-Hab01-04", rm2), _o(f"${m+2*k}$", "D-Hab01-05", rm1), _o(f"${m-2*k}$", "D-Hab01-06", rm2)]}
def gen_4(r):
    a, b = -r.randint(4, 30), r.randint(6, 40)
    return {"vars": {"a": a, "b": b}, "options": [_o(f"$z={a+b}$", None, None), _o(f"$z<{b}$", None, None), _o(f"$z={a-b}$", "D-Hab01-05", RATS["D-Hab01-05"]), _o(f"$z={b-a}$", "D-Hab01-06", RATS["D-Hab01-06"]), _o(f"$z={a}$", "D-Hab01-05", RATS["D-Hab01-05"]), _o(f"$z={a+2*b}$", "D-Hab01-03", RATS["D-Hab01-03"]), _o(f"$z={b+2*a}$", "D-Hab01-04", RATS["D-Hab01-04"])]}
def ver_1(c, v): return abs(_pv(c) - (v["a"] * v["b"] + 5)) < 1e-4
def ver_2(c, v): return abs(_pv(c) - (v["p"] * v["q"] + 11)) < 1e-4
def _ms_chk(r, cond):
    o = r.get("options", []) if isinstance(r, dict) else []
    t = [u for u in o if u.get("is_correct") is True]
    f = [u for u in o if u.get("is_correct") is False]
    return len(o) == 7 and len(t) in (2, 3, 4, 5) and len(f) >= 2 and cond(t, f) and all(u.get("distractor_id") in RATS and len(u.get("error_rationale", "")) >= 20 for u in f)
def ver_3(r):
    v = r.get("vars", {}); sm = v.get("m", 0) + v.get("k", 0)
    return v.get("m", 0) > 0 and v.get("k", 0) > 0 and _ms_chk(
        r,
        lambda t, f: any(">" not in u["value"] and _pv(u["value"]) == sm for u in t)
        and any(">" in u["value"] and str(sm) in u["value"] for u in t)
        and all(">" not in u["value"] and _pv(u["value"]) != sm for u in f),
    )
def ver_4(r):
    v = r.get("vars", {}); sm = v.get("a", 0) + v.get("b", 0)
    return v.get("a", 0) < 0 and _ms_chk(
        r,
        lambda t, f: any("<" not in u["value"] and _pv(u["value"]) == sm for u in t)
        and any("<" in u["value"] and str(v.get("b", "")) in u["value"] for u in t)
        and all("<" not in u["value"] and _pv(u["value"]) != sm for u in f),
    )
S1 = [r"Calcule producto desplazado $@a@ \cdot @b@ + 5$:", r"Evalúe $@a@(@b@)+5$ directamente:", r"Obtén suma multiplicativa con $@a@,@b@$:", r"Determina entero $@a@ \cdot @b@ + 5$:"]
S2 = [r"Resuelva ecuación auxiliar $@p@ \cdot @q@ + 11$:", r"Halle incógnita con factores $@p@$ y $@q@$:", r"Invierta regla afín para $@p@$ y $@q@$:", r"Despeje magnitud entera con $@p@,@q@$:"]
S3 = [r"Con $@m@,@k@>0$, marque suma positiva:", r"Elija propiedades ciertas para $@m@+@k@$:", r"Seleccione expresiones válidas en $@m@,@k@$:", r"Identifique cotas exactas de $@m@+@k@$:"]
S4 = [r"Bajo frontera negativa $@a@<0$ y $@b@$, marque:", r"Para $@a@<0$, seleccione desigualdades válidas:", r"Evalúe signo límite en $@a@<0$ y $@b@$:", r"Decida opciones ciertas cuando $@a@<0$:"]
H1 = [r"Multiplique $@a@$ por $@b@$ primero.", r"Sume exactamente 5 al producto.", r"Verifique aritmética de enteros."]
H2 = [r"Calcule el producto de $@p@$ y $@q@$.", r"Añada desplazamiento 11 al final.", r"Revise signo positivo final."]
H3 = [r"Sume directamente parámetros $@m@$ y $@k@$.", r"Todo término positivo suma positivo.", r"Descarte resta y producto."]
H4 = [r"Considere signo negativo de $@a@$.", r"Sume valor positivo $@b@$ al negativo.", r"Compare contra la cota $@b@$."]
SOL = r"Paso 1: Identificamos parámetros enteros de la instancia. Paso 2: Operamos exactamente."
TEMPLATES = [
    {"id": "T-Hab-01-01", "cid": "Hab-01", "qtype": "FIB", "archetype": "direct", "band": ("easy", "Apply"), "gen": gen_1, "ver": ver_1, "stem_variants": S1, "hints": H1, "sol": SOL, "rats": RATS},
    {"id": "T-Hab-01-02", "cid": "Hab-01", "qtype": "FIB", "archetype": "inverse", "band": ("medium", "Apply"), "gen": gen_2, "ver": ver_2, "stem_variants": S2, "hints": H2, "sol": SOL, "rats": RATS},
    {"id": "T-Hab-01-03", "cid": "Hab-01", "qtype": "MS", "archetype": "perturbation", "band": ("hard", "Analyze"), "gen": gen_3, "ver": ver_3, "stem_variants": S3, "hints": H3, "sol": SOL, "rats": RATS},
    {"id": "T-Hab-01-04", "cid": "Hab-01", "qtype": "MS", "archetype": "boundary_or_edge_case", "assumption_id": "A-Hab01-01", "band": ("hard", "Evaluate"), "gen": gen_4, "ver": ver_4, "stem_variants": S4, "hints": H4, "sol": SOL, "rats": RATS},
]
'''
        w_ast = _setup_shard_workspace(tmp_path / "ast", "Hab-01", "skill", ["fill_in_the_blank", "multiple_select"], code_ast)
        ok_ast, errs_ast = compile_shard(w_ast, shard_id="shard_01", strict=True, seeds=30, min_archetypes=4, templates_per_modality=2)
        joined_ast = "\n".join(errs_ast)
        assert not ok_ast and "[TPL-CLONE-AST]" in joined_ast and "[TPL-DYNAMIC-RATIONALE]" not in joined_ast, errs_ast

        # 2. [TPL-CLONE-BAND]: same (archetype, difficulty, bloom) inside same modality (different AST)
        code_band = code_ast.replace(
            "res = p * q + 11", "res = p + q * q + 11"
        ).replace(
            'v["p"] * v["q"] + 11', 'v["p"] + v["q"] ** 2 + 11'
        ).replace(
            '{"id": "T-Hab-01-02", "cid": "Hab-01", "qtype": "FIB", "archetype": "inverse", "band": ("medium", "Apply")',
            '{"id": "T-Hab-01-02", "cid": "Hab-01", "qtype": "FIB", "archetype": "direct", "band": ("easy", "Apply")',
        )
        w_band = _setup_shard_workspace(tmp_path / "band", "Hab-01", "skill", ["fill_in_the_blank", "multiple_select"], code_band)
        ok_band, errs_band = compile_shard(w_band, shard_id="shard_01", strict=True, seeds=30, min_archetypes=3, templates_per_modality=2)
        assert not ok_band and "[TPL-CLONE-BAND]" in "\n".join(errs_band), errs_band

        # 3. [TPL-CLONE-STEM]: stem_variants Jaccard >= 0.70 (different AST & band)
        code_stem = code_ast.replace(
            "res = p * q + 11", "res = p + q * q + 11"
        ).replace(
            'v["p"] * v["q"] + 11', 'v["p"] + v["q"] ** 2 + 11'
        ).replace(
            'S2 = [r"Resuelva ecuación auxiliar $@p@ \\cdot @q@ + 11$:", r"Halle incógnita con factores $@p@$ y $@q@$:", r"Invierta regla afín para $@p@$ y $@q@$:", r"Despeje magnitud entera con $@p@,@q@$:"]',
            'S2 = [r"Calcule producto desplazado $@p@ \\cdot @q@ + 11$:", r"Evalúe $@p@(@q@)+11$ directamente:", r"Obtén suma multiplicativa con $@p@,@q@$:", r"Determina entero $@p@ \\cdot @q@ + 11$:"]',
        )
        w_stem = _setup_shard_workspace(tmp_path / "stem", "Hab-01", "skill", ["fill_in_the_blank", "multiple_select"], code_stem)
        ok_stem, errs_stem = compile_shard(w_stem, shard_id="shard_01", strict=True, seeds=30, min_archetypes=4, templates_per_modality=2)
        assert not ok_stem and "[TPL-CLONE-STEM]" in "\n".join(errs_stem), errs_stem

        # 4. [TPL-CLONE-SYMPY]: equivalent open_symbolic expressions in same archetype vs non-equivalent
        sympy_bad = r'''
RATS = {
    "D-C01-01": r"Confunde distribución del factor constante $@a@$ frente al término lineal.",
    "D-C01-02": r"Omite el coeficiente $@b@$ al desarrollar la expresión polinómica.",
    "D-C01-03": r"Invierte el signo del término independiente $@a@$ en la frontera.",
}
def _o(v, d, e):
    return {"value": v, "is_correct": d is None} | ({"distractor_id": d, "error_rationale": e} if d else {})
def gen_1(r):
    a = r.randint(3, 40)
    expr = f"{a}*(x + 1)"
    return {"vars": {"a": a, "ans": expr}, "correct": expr, "variables": ["x"], "symbolic_config": {"variables": ["x"]}, "ds": [("D-C01-01", f"{a}*x + 1", RATS["D-C01-01"])]}
def gen_2(r):
    b = r.randint(3, 40)
    expr = f"{b}*x + {b}"
    return {"vars": {"b": b, "ans": expr}, "correct": expr, "variables": ["x"], "symbolic_config": {"variables": ["x"]}, "ds": [("D-C01-02", f"{b}*x - {b}", RATS["D-C01-02"])]}
def gen_3(r):
    a, k = r.randint(4, 30), r.randint(3, 25)
    ra = r"Resta el término $@k@$ del parámetro $@a@$ ignorando que la operación correcta exige sumar ambos términos positivos."
    rb = r"Multiplica factores $@a@$ y $@k@$ confundiendo el producto con el incremento directo de la expresión lineal."
    return {"vars": {"a": a, "k": k}, "options": [_o(f"${a+k}$", None, None), _o(f"${a+k}>0$", None, None), _o(f"${a+k}>1$", None, None), _o(f"${a-k}$", "D-C01-02", ra), _o(f"${a*k+1}$", "D-C01-03", rb), _o(f"${a+2*k}$", "D-C01-01", ra), _o(f"${a*k+2}$", "D-C01-02", rb)]}
def gen_4(r):
    a, m = r.randint(4, 28), r.randint(3, 22)
    ra = r"Suma linealmente los factores $@a@$ y $@m@$ en vez de aplicar correctamente la regla multiplicativa completa."
    return {"vars": {"a": a, "m": m}, "options": [_o(f"$p={a*m}$", None, None), _o(f"$p>{a}$", None, None), _o(f"$p={a+m}$", "D-C01-01", ra), _o(f"$p=-{m}$", "D-C01-03", RATS["D-C01-03"]), _o(f"$p={a}$", "D-C01-01", ra), _o(f"$p={a+2*m}$", "D-C01-02", ra), _o(f"$p=-{a+m}$", "D-C01-03", RATS["D-C01-03"])]}
def ver_1(c, v):
    import sympy; x = sympy.Symbol("x")
    try: return sympy.simplify(sympy.sympify(str(c)) - v["a"] * (x + 1)) == 0
    except Exception: return False
def ver_2(c, v):
    import sympy; x = sympy.Symbol("x")
    try: return sympy.simplify(sympy.sympify(str(c)) - (v["b"] * x + v["b"])) == 0
    except Exception: return False
def _pv(c):
    for t in reversed("".join(x if x in "0123456789.eE+-" else " " for x in str(c)).split()):
        try: return float(t.rstrip("."))
        except ValueError: pass
    return float("nan")
def _ms_chk(r, cond):
    o = r.get("options", []) if isinstance(r, dict) else []
    t = [u for u in o if u.get("is_correct") is True]
    f = [u for u in o if u.get("is_correct") is False]
    return len(o) == 7 and len(t) in (2, 3, 4, 5) and len(f) >= 2 and cond(t, f) and all(u.get("distractor_id") in RATS and len(u.get("error_rationale", "")) >= 20 for u in f)
def ver_3(r):
    v = r.get("vars", {}); sm = v.get("a", 0) + v.get("k", 0)
    return v.get("a", 0) > 0 and v.get("k", 0) > 0 and _ms_chk(
        r,
        lambda t, f: any(">" not in u["value"] and _pv(u["value"]) == sm for u in t)
        and any(">" in u["value"] and str(sm) in u["value"] for u in t)
        and all(">" not in u["value"] and _pv(u["value"]) != sm for u in f),
    )
def ver_4(r):
    v = r.get("vars", {}); pr = v.get("a", 0) * v.get("m", 0)
    return v.get("a", 0) > 0 and v.get("m", 0) > 1 and _ms_chk(
        r,
        lambda t, f: any(">" not in u["value"] and _pv(u["value"]) == pr for u in t)
        and any(">" in u["value"] and str(v.get("a", "")) in u["value"] for u in t)
        and all(">" not in u["value"] and _pv(u["value"]) != pr for u in f),
    )
S1 = [r"Escriba la forma factorizada multiplicando $@a@$ por $(x+1)$:", r"Exprese linealmente $@a@(x+1)$ en variable $x$:", r"Represente producto $@a@$ sobre binomio $(x+1)$:"]
S2 = [r"Desarrolle polinomio expandido en $x$ de pendiente $@b@$ e intercepto $@b@$:", r"Formule suma algebraica $@b@x + @b@$ en $x$:", r"Indique término completo en variable $x$ con coeficiente $@b@$ y constante $@b@$:"]
S3 = [r"Con $@a@,@k@>0$, seleccione identidades de suma:", r"Marque proposiciones válidas sobre $@a@+@k@$:", r"Identifique propiedades ciertas en $@a@,@k@$:"]
S4 = [r"Para frontera $@a@,@m@>0$, escoja cotas válidas:", r"Determine relaciones ciertas del producto $@a@ \cdot @m@$:", r"Elija afirmaciones correctas en frontera $@a@,@m@$:"]
H1 = [r"Conserve el factor $@a@$ fuera del paréntesis.", r"Incluya la unidad dentro del binomio.", r"Escriba multiplicación explícita."]
H2 = [r"Desarrolle coeficiente $@b@$ multiplicando a x.", r"Añada el término independiente $@b@$.", r"Verifique suma final de términos."]
H3 = [r"Evalúe la adición positiva de $@a@$ y $@k@$.", r"Verifique positividad estricto sobre cero.", r"Descarte resta y multiplicación."]
H4 = [r"Multiplique enteros positivos $@a@$ y $@m@$.", r"Observe cota estricta sobre $@a@$.", r"Descarte valores negativos."]
SOL = r"Paso 1: Identificamos coeficientes y estructura polinómica. Paso 2: Verificamos equivalencia formal."
TEMPLATES = [
    {"id": "T-C01-01", "cid": "C-01", "qtype": "open_symbolic", "archetype": "direct", "band": ("easy", "Understand"), "gen": gen_1, "ver": ver_1, "stem_variants": S1, "hints": H1, "sol": SOL, "rats": RATS},
    {"id": "T-C01-02", "cid": "C-01", "qtype": "open_symbolic", "archetype": "direct", "band": ("medium", "Apply"), "gen": gen_2, "ver": ver_2, "stem_variants": S2, "hints": H2, "sol": SOL, "rats": RATS},
    {"id": "T-C01-03", "cid": "C-01", "qtype": "MS", "archetype": "inverse", "band": ("medium", "Analyze"), "gen": gen_3, "ver": ver_3, "stem_variants": S3, "hints": H3, "sol": SOL, "rats": RATS},
    {"id": "T-C01-04", "cid": "C-01", "qtype": "MS", "archetype": "boundary_or_edge_case", "assumption_id": "A-C01-01", "band": ("hard", "Evaluate"), "gen": gen_4, "ver": ver_4, "stem_variants": S4, "hints": H4, "sol": SOL, "rats": RATS},
]
'''
        w_sym_bad = _setup_shard_workspace(tmp_path / "sym_bad", "C-01", "concept", ["open_symbolic", "multiple_select"], sympy_bad)
        ok_sb, errs_sb = compile_shard(w_sym_bad, shard_id="shard_01", strict=True, seeds=20, min_archetypes=3, templates_per_modality=2)
        assert not ok_sb and "[TPL-CLONE-SYMPY]" in "\n".join(errs_sb), errs_sb

        # Non-equivalent open_symbolic expression (x**2 + b) passes all 4 anti-clone gates
        sympy_ok = sympy_bad.replace(
            'expr = f"{b}*x + {b}"',
            'expr = f"x**2 + {b}"',
        ).replace(
            '(v["b"] * x + v["b"])',
            '(x**2 + v["b"])',
        ).replace(
            '{"id": "T-C01-03", "cid": "C-01", "qtype": "MS", "archetype": "inverse"',
            '{"id": "T-C01-03", "cid": "C-01", "qtype": "MS", "archetype": "perturbation"',
        )
        w_sym_ok = _setup_shard_workspace(tmp_path / "sym_ok", "C-01", "concept", ["open_symbolic", "multiple_select"], sympy_ok)
        ok_so, errs_so = compile_shard(w_sym_ok, shard_id="shard_01", strict=True, seeds=20, min_archetypes=3, templates_per_modality=2)
        assert ok_so and errs_so == [], errs_so


class TestInstantiateDynamicQuotas:
    def test_instantiate_competency_scales_quotas_for_n_4_6_8_12(self):
        assert get_competency_quota("skill", num_templates=4) == 30
        assert get_competency_quota("skill", num_templates=6) == 30
        assert get_competency_quota("skill", num_templates=8) == 32
        assert get_competency_quota("skill", num_templates=12) == 48
        assert get_competency_quota("concept", num_templates=4) == 20
        assert get_competency_quota("concept", num_templates=6) == 20
        assert get_competency_quota("concept", num_templates=8) == 24
        assert get_competency_quota("fact", num_templates=12) == 36

        def _make_tpl(idx: int) -> dict:
            gen_py = (
                "def generate(r):\n"
                f"    a = r.randint({10 + idx * 5}, {5000 + idx * 5})\n"
                f"    ans = a + {idx + 1}\n"
                "    return {'vars': {'a': a, 'ans': ans}, 'correct': str(ans)}\n"
            )
            ver_py = (
                "def cross_check(inst):\n"
                "    v = inst.get('vars', {})\n"
                f"    return str(inst.get('correct')) == str(v['a'] + {idx + 1})\n"
            )
            return {
                "id": f"T-Hab-01-{idx + 1:02d}",
                "interaction_type": "fill_in_the_blank",
                "stem": f"Con parámetro @a@ en variante {idx + 1}, halle resultado:",
                "stem_variants": [
                    f"Variante {idx + 1}A con parámetro $@a@$:",
                    f"Variante {idx + 1}B dado $@a@$:",
                    f"Variante {idx + 1}C para $@a@$:",
                ],
                "hints": ["Hint 1", "Hint 2", "Hint 3"],
                "solution": "Paso 1: suma directa. Paso 2: resultado @ans@.",
                "generate_py": gen_py,
                "cross_check_py": ver_py,
            }

        for n_tpls, ctype, expected_quota in [(4, "skill", 30), (6, "skill", 30), (8, "skill", 32), (12, "skill", 48), (8, "concept", 24), (12, "concept", 36)]:
            tpls = [_make_tpl(i) for i in range(n_tpls)]
            res = instantiate_competency(
                competency_id="Hab-01" if ctype == "skill" else "C-01",
                category=ctype,
                templates=tpls,
                base_seed=1000,
            )
            assert res["quota_target"] == expected_quota
            assert res["total_generated"] == expected_quota
            per_tpl_min = 4 if ctype == "skill" else 3
            assert expected_quota // n_tpls >= per_tpl_min
