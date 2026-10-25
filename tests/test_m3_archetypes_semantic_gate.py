"""Unit tests for the hardened Milestone 3 Semantic Archetypes Gate [M3-ARCHETYPES].

Verifies:
1. Rejection when a competency passes cloned / identical stems across its tuples
   (e.g., passing the same `stems` list to all 4 tuples in TEMPLATES).
2. Rejection when a generator helper declares the `arch` parameter (e.g. `def _gen_*(rng, arch=1):`)
   but never utilizes `arch` in its body, leading to silent duplicate instances.
3. Clean PASS (100%) when 4 distinct stem lists and an active `arch`-branching generator are used.
"""

import json
import sys
from pathlib import Path
import pytest

# Ensure skill root and project src are in sys.path
_skill_root = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

_src_root = Path(__file__).resolve().parents[1] / "src"
if str(_src_root) not in sys.path:
    sys.path.insert(0, str(_src_root))

from compile_shard import compile_shard


def _setup_workspace_shard(tmp_path: Path, shard_id: str = "shard_01", cid: str = "H-01"):
    """Sets up an isolated workspace with cta.json and pre_shard_manifest.json."""
    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    templates_dir = work_dir / "templates"
    shards_dir.mkdir(parents=True, exist_ok=True)
    templates_dir.mkdir(parents=True, exist_ok=True)

    cta_payload = {
        "competencies": [
            {
                "id": cid,
                "name": f"Competencia {cid} Termodinámica",
                "type": "skill",
                "distractors": [
                    {"id": f"D-{cid}-01", "remediation_hint": "Inversión del cociente térmico en la formulación."},
                    {"id": f"D-{cid}-02", "remediation_hint": "Confusión entre calor cedido y trabajo neto."},
                    {"id": f"D-{cid}-03", "remediation_hint": "Desplazamiento erróneo en la diferencia de reservorios."},
                    {"id": f"D-{cid}-04", "remediation_hint": "Factor espurio en el reservorio caliente."},
                    {"id": f"D-{cid}-05", "remediation_hint": "Normalización espuria por suma total de temperaturas."},
                    {"id": f"D-{cid}-06", "remediation_hint": "Factor de semidiferencia en el cálculo de eficiencia."},
                ],
            }
        ]
    }
    cta_file = work_dir / "cta.json"
    cta_file.write_text(json.dumps(cta_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    manifest_payload = {
        "min_archetypes": 4,
        "shards": [
            {
                "shard_id": shard_id,
                "competency_ids": [cid],
                "shard_data_path": str((shards_dir / f"{shard_id}_data.py").resolve().as_posix()),
                "templates_dir": str(templates_dir.resolve().as_posix()),
                "competencies": cta_payload["competencies"],
            }
        ]
    }
    manifest_file = shards_dir / "pre_shard_manifest.json"
    manifest_file.write_text(json.dumps(manifest_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    return work_dir, shards_dir, templates_dir, cta_file, manifest_file


class TestM3ArchetypesSemanticGate:
    """Tests the semantic gate [M3-ARCHETYPES] in compile_shard."""

    def test_m3_archetypes_gate_rejects_reused_stems_across_tuples(self, tmp_path: Path):
        """Verifies that passing the same stems list to the 4 tuples in TEMPLATES
        is rejected with [M3-ARCHETYPES] reporting repeated stem_es.
        """
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        # Generator properly branches on arch, BUT the author passed the exact same stems list
        code = r'''
import random

def _gen_h01(rng, arch=1):
    tc = rng.randint(200, 300)
    delta = rng.randint(100, 200) * arch
    th = tc + delta
    ans = round(1.0 - (tc / th), 3)
    dists = [round(ans + 0.05 * i, 3) for i in range(1, 7)]
    v = {"tc": tc, "th": th, "ans": ans, **{f"d{i}": d for i, d in enumerate(dists, 1)}}
    return {
        "vars": v,
        "correct": r"$\eta = @ans@$",
        "distractors": [(f"D-H01-{i:02d}", rf"$\eta = @d{i}@$") for i in range(1, 7)],
    }

def gen_h01_1(rng): return _gen_h01(rng, 1)
def gen_h01_2(rng): return _gen_h01(rng, 2)
def gen_h01_3(rng): return _gen_h01(rng, 3)
def gen_h01_4(rng): return _gen_h01(rng, 4)

def ver_h01(res): return True

# Reusing the SAME stems list across all 4 tuples (Violation!)
stems_reused = [
    r"Una máquina térmica opera entre focos a $T_H = @th@$ y $T_C = @tc@$. Calcule el rendimiento:",
    r"Determine la eficiencia para focos $T_H = @th@$ y $T_C = @tc@$:",
]

TEMPLATES = [
    ("H-01", "multiple_choice_7_options", stems_reused, gen_h01_1, ver_h01, "Solución 1", "KC", [], "Ref 1"),
    ("H-01", "multiple_choice_7_options", stems_reused, gen_h01_2, ver_h01, "Solución 2", "KC", [], "Ref 2"),
    ("H-01", "multiple_choice_7_options", stems_reused, gen_h01_3, ver_h01, "Solución 3", "KC", [], "Ref 3"),
    ("H-01", "multiple_choice_7_options", stems_reused, gen_h01_4, ver_h01, "Solución 4", "KC", [], "Ref 4"),
]
'''
        shard_py.write_text(code, encoding="utf-8")

        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            min_archetypes=4,
            cta_path=cta_file,
            seeds=10,
        )

        assert not success, "Expected compilation to FAIL due to cloned stems"
        assert len(errors) > 0
        error_msg = "\n".join(errors)
        assert "[M3-ARCHETYPES]" in error_msg
        assert "repite el mismo enunciado (stem_es)" in error_msg

    def test_m3_archetypes_gate_rejects_unused_arch_parameter(self, tmp_path: Path):
        """Verifies that defining `def _gen_h01(rng, arch=1):` without ever reading
        `arch` in its body is rejected with [M3-ARCHETYPES] pointing out the unused parameter.
        """
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        # Stems are distinct, but arch is declared and ignored in _gen_h01
        code = r'''
import random

def _gen_h01(rng, arch=1):
    # arch is declared in signature but NEVER read in the body!
    tc = rng.randint(250, 350)
    th = tc + rng.randint(150, 450)
    ans = round(1.0 - (tc / th), 3)
    dists = [round(ans + 0.05 * i, 3) for i in range(1, 7)]
    v = {"tc": tc, "th": th, "ans": ans, **{f"d{i}": d for i, d in enumerate(dists, 1)}}
    return {
        "vars": v,
        "correct": r"$\eta = @ans@$",
        "distractors": [(f"D-H01-{i:02d}", rf"$\eta = @d{i}@$") for i in range(1, 7)],
    }

def gen_h01_1(rng): return _gen_h01(rng, 1)
def gen_h01_2(rng): return _gen_h01(rng, 2)
def gen_h01_3(rng): return _gen_h01(rng, 3)
def gen_h01_4(rng): return _gen_h01(rng, 4)

def ver_h01(res): return True

stems_1 = ["Calcule la eficiencia directa con $T_H=@th@$ y $T_C=@tc@$:"]
stems_2 = ["Deduzca la temperatura inversa con $T_H=@th@$ y $T_C=@tc@$:"]
stems_3 = ["Evalúe la perturbación térmica con $T_H=@th@$ y $T_C=@tc@$:"]
stems_4 = ["Establezca la cota límite en la frontera con $T_H=@th@$ y $T_C=@tc@$:"]

TEMPLATES = [
    ("H-01", "multiple_choice_7_options", stems_1, gen_h01_1, ver_h01, "Solución 1", "KC", [], "Ref 1"),
    ("H-01", "multiple_choice_7_options", stems_2, gen_h01_2, ver_h01, "Solución 2", "KC", [], "Ref 2"),
    ("H-01", "multiple_choice_7_options", stems_3, gen_h01_3, ver_h01, "Solución 3", "KC", [], "Ref 3"),
    ("H-01", "multiple_choice_7_options", stems_4, gen_h01_4, ver_h01, "Solución 4", "KC", [], "Ref 4"),
]
'''
        shard_py.write_text(code, encoding="utf-8")

        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            min_archetypes=4,
            cta_path=cta_file,
            seeds=10,
        )

        assert not success, "Expected compilation to FAIL due to ignored 'arch' argument"
        assert len(errors) > 0
        error_msg = "\n".join(errors)
        assert "[M3-ARCHETYPES]" in error_msg
        assert "recibe el parámetro 'arch' pero nunca" in error_msg

    def test_m3_archetypes_gate_passes_with_distinct_stems_and_active_arch(self, tmp_path: Path):
        """Verifies that when 4 distinct stem lists are supplied and _gen_h01 actively branches
        on `arch`, compilation succeeds (PASS 100%) and produces the 4-archetype template JSON.
        """
        work_dir, shards_dir, templates_dir, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        code = r'''
import random

def _gen_h01(rng, arch=1):
    if arch == 1:
        # Directo: régimen estándar
        tc = rng.randint(250, 350)
        delta = rng.randint(150, 450)
    elif arch == 2:
        # Inverso: criogénico
        tc = rng.randint(70, 180)
        delta = rng.randint(100, 300)
    elif arch == 3:
        # Perturbación: salto térmico elevado
        tc = rng.randint(300, 400)
        delta = rng.randint(500, 900)
    else:
        # Frontera: cota extrema
        tc = rng.randint(200, 280)
        delta = rng.randint(800, 1500)

    th = tc + delta
    ans = round(1.0 - (tc / th), 3)
    dists = [round(ans + 0.05 * i, 3) for i in range(1, 7)]
    v = {"tc": tc, "th": th, "ans": ans, **{f"d{i}": d for i, d in enumerate(dists, 1)}}
    return {
        "vars": v,
        "correct": r"$\eta = @ans@$",
        "distractors": [(f"D-H01-{i:02d}", rf"$\eta = @d{i}@$") for i in range(1, 7)],
    }

def gen_h01_1(rng): return _gen_h01(rng, 1)
def gen_h01_2(rng): return _gen_h01(rng, 2)
def gen_h01_3(rng): return _gen_h01(rng, 3)
def gen_h01_4(rng): return _gen_h01(rng, 4)

def ver_h01(res): return True

stems_1 = [
    r"Calcule la eficiencia directa de Carnot con focos $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
    r"Determine el rendimiento térmico frontal entre temperaturas $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
]
stems_2 = [
    r"En un análisis inverso con foco frío a $T_C = @tc@\text{ K}$ y caliente a $T_H = @th@\text{ K}$, halle $\eta$:",
    r"Deduzca el rendimiento inverso asociado a las cotas térmicas $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
]
stems_3 = [
    r"Si se aplica una perturbación térmica con reservorios a $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$, evalúe $\eta$:",
    r"Calcule la variación en la eficiencia bajo el régimen perturbado $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
]
stems_4 = [
    r"Bajo el régimen asintótico de frontera extrema con $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$, determine el límite:",
    r"En la cota extrema del ciclo con $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$, establezca la eficiencia límite $\eta$:",
]

TEMPLATES = [
    ("H-01", "multiple_choice_7_options", stems_1, gen_h01_1, ver_h01, "Solución 1", "KC", [], "Ref 1"),
    ("H-01", "multiple_choice_7_options", stems_2, gen_h01_2, ver_h01, "Solución 2", "KC", [], "Ref 2"),
    ("H-01", "multiple_choice_7_options", stems_3, gen_h01_3, ver_h01, "Solución 3", "KC", [], "Ref 3"),
    ("H-01", "multiple_choice_7_options", stems_4, gen_h01_4, ver_h01, "Solución 4", "KC", [], "Ref 4"),
]
'''
        shard_py.write_text(code, encoding="utf-8")

        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            min_archetypes=4,
            cta_path=cta_file,
            seeds=20,
        )

        assert success, f"Expected successful compilation, but failed with: {errors}"
        assert len(errors) == 0

        # Verify compiled templates JSON
        out_json = templates_dir / "H-01.json"
        assert out_json.is_file(), f"Output JSON not found at {out_json}"
        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload.get("competency_id") == "H-01"
        assert "templates" in payload
        assert len(payload["templates"]) == 4

        # Verify pass marker
        pass_marker = work_dir / ".check_attempts" / "pass_shard_01.json"
        assert pass_marker.is_file()
        p_data = json.loads(pass_marker.read_text(encoding="utf-8"))
        assert p_data.get("status") == "PASS"
        assert p_data.get("shard_id") == "shard_01"

    def test_m3_archetypes_gate_rejects_trivial_arch_evasion_and_mathematical_clones(self, tmp_path: Path):
        """Verifies that an author attempting trivial AST evasion with `_ = arch` but producing
        mathematically identical (correct, vars) across all 4 tuples is rejected by [M3-ARCHETYPES].
        """
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        # Stems are distinct and author includes `_ = arch` dummy load,
        # but outputs are mathematical clones because arch is never used to branch calculation
        code = r'''
import random

def _gen_h01(rng, arch=1):
    _ = arch  # Trivial AST evasion attempt!
    tc = rng.randint(250, 350)
    delta = rng.randint(150, 450)
    th = tc + delta
    ans = round(1.0 - (tc / th), 3)
    dists = [round(ans + 0.05 * i, 3) for i in range(1, 7)]
    v = {"tc": tc, "th": th, "ans": ans, **{f"d{i}": d for i, d in enumerate(dists, 1)}}
    return {
        "vars": v,
        "correct": r"$\eta = @ans@$",
        "distractors": [(f"D-H01-{i:02d}", rf"$\eta = @d{i}@$") for i in range(1, 7)],
    }

def gen_h01_1(rng): return _gen_h01(rng, 1)
def gen_h01_2(rng): return _gen_h01(rng, 2)
def gen_h01_3(rng): return _gen_h01(rng, 3)
def gen_h01_4(rng): return _gen_h01(rng, 4)

def ver_h01(res): return True

stems_1 = [r"Calcule la eficiencia directa con focos $T_H = @th@$ y $T_C = @tc@$:"]
stems_2 = [r"Deduzca el rendimiento inverso para focos $T_H = @th@$ y $T_C = @tc@$:"]
stems_3 = [r"Evalúe la perturbación térmica con focos $T_H = @th@$ y $T_C = @tc@$:"]
stems_4 = [r"Establezca el comportamiento de frontera con $T_H = @th@$ y $T_C = @tc@$:"]

TEMPLATES = [
    ("H-01", "multiple_choice_7_options", stems_1, gen_h01_1, ver_h01, "Solución 1", "KC", [], "Ref 1"),
    ("H-01", "multiple_choice_7_options", stems_2, gen_h01_2, ver_h01, "Solución 2", "KC", [], "Ref 2"),
    ("H-01", "multiple_choice_7_options", stems_3, gen_h01_3, ver_h01, "Solución 3", "KC", [], "Ref 3"),
    ("H-01", "multiple_choice_7_options", stems_4, gen_h01_4, ver_h01, "Solución 4", "KC", [], "Ref 4"),
]
'''
        shard_py.write_text(code, encoding="utf-8")

        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            min_archetypes=4,
            cta_path=cta_file,
            seeds=10,
        )

        assert not success, "Expected compilation to FAIL due to mathematical clones / dummy arch evasion"
        assert len(errors) > 0
        error_msg = "\n".join(errors)
        assert "[M3-ARCHETYPES]" in error_msg
        assert "salidas matemáticas idénticas" in error_msg or "recibe el parámetro 'arch' pero nunca" in error_msg

    def test_m3_archetypes_gate_accepts_modular_fix_overriding_broken_shard(self, tmp_path: Path):
        """Verifies that when a broken shard base is repaired via a modular fix file
        in shards/shard_fixes/H-01.py with 4 genuine archetypes, compilation succeeds cleanly (PASS 100%)
        without producing false positives from legacy code in shard_01_data.py.
        """
        work_dir, shards_dir, templates_dir, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        # Broken shard base with legacy broken generator
        broken_base_code = r'''
import random

def _gen_h01(rng, arch=1):
    # Broken legacy generator that ignores arch
    return {"vars": {}, "correct": "0", "distractors": []}

def gen_broken(rng): return _gen_h01(rng, 1)
def ver_broken(res): return True

TEMPLATES = [
    ("H-01", "multiple_choice_7_options", ["Legacy cloned stem"], gen_broken, ver_broken, "sol", "KC", [], "ref"),
]
'''
        shard_py.write_text(broken_base_code, encoding="utf-8")

        # Now write modular fix in shards/shard_fixes/H-01.py
        fixes_dir = shards_dir / "shard_fixes"
        fixes_dir.mkdir(parents=True, exist_ok=True)
        fix_py = fixes_dir / "H-01.py"

        modular_fix_code = r'''
import random

def _gen_h01_modular(rng, arch=1):
    if arch == 1:
        tc = rng.randint(250, 350)
        delta = rng.randint(150, 450)
    elif arch == 2:
        tc = rng.randint(70, 180)
        delta = rng.randint(100, 300)
    elif arch == 3:
        tc = rng.randint(300, 400)
        delta = rng.randint(500, 900)
    else:
        tc = rng.randint(200, 280)
        delta = rng.randint(800, 1500)

    th = tc + delta
    ans = round(1.0 - (tc / th), 3)
    dists = [round(ans + 0.05 * i, 3) for i in range(1, 7)]
    v = {"tc": tc, "th": th, "ans": ans, **{f"d{i}": d for i, d in enumerate(dists, 1)}}
    return {
        "vars": v,
        "correct": r"$\eta = @ans@$",
        "distractors": [(f"D-H01-{i:02d}", rf"$\eta = @d{i}@$") for i in range(1, 7)],
    }

def gen_h01_1(rng): return _gen_h01_modular(rng, 1)
def gen_h01_2(rng): return _gen_h01_modular(rng, 2)
def gen_h01_3(rng): return _gen_h01_modular(rng, 3)
def gen_h01_4(rng): return _gen_h01_modular(rng, 4)

def ver_h01(res): return True

stems_1 = [r"Calcule la eficiencia directa con focos $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:"]
stems_2 = [r"En un análisis inverso con foco frío a $T_C = @tc@\text{ K}$ y caliente a $T_H = @th@\text{ K}$, halle $\eta$:"]
stems_3 = [r"Si se aplica una perturbación térmica con reservorios a $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$, evalúe $\eta$:"]
stems_4 = [r"Bajo el régimen asintótico de frontera extrema con $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$, determine el límite:"]

TEMPLATES = [
    ("H-01", "multiple_choice_7_options", stems_1, gen_h01_1, ver_h01, "Solución 1", "KC", [], "Ref 1"),
    ("H-01", "multiple_choice_7_options", stems_2, gen_h01_2, ver_h01, "Solución 2", "KC", [], "Ref 2"),
    ("H-01", "multiple_choice_7_options", stems_3, gen_h01_3, ver_h01, "Solución 3", "KC", [], "Ref 3"),
    ("H-01", "multiple_choice_7_options", stems_4, gen_h01_4, ver_h01, "Solución 4", "KC", [], "Ref 4"),
]
'''
        fix_py.write_text(modular_fix_code, encoding="utf-8")

        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            min_archetypes=4,
            cta_path=cta_file,
            seeds=20,
        )

        assert success, f"Expected modular fix to pass cleanly, but failed with: {errors}"
        assert len(errors) == 0

        # Verify output templates JSON
        out_json = templates_dir / "H-01.json"
        assert out_json.is_file()
        payload = json.loads(out_json.read_text(encoding="utf-8"))
        assert payload.get("competency_id") == "H-01"
        assert len(payload["templates"]) == 4

        # Verify pass marker
        pass_marker = work_dir / ".check_attempts" / "pass_shard_01.json"
        assert pass_marker.is_file()
        p_data = json.loads(pass_marker.read_text(encoding="utf-8"))
        assert p_data.get("status") == "PASS"
