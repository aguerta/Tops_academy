"""Unit tests for the hardened Milestone 3 Semantic Archetypes Gate [M3-ARCHETYPES].

Verifies:
1. Rejection when a competency passes cloned / identical stems across its tuples
   (e.g., passing the same `stems` list to all tuples in TEMPLATES).
2. Rejection when a generator helper declares the `arch` parameter (e.g. `def _gen_*(rng, arch=1):`)
   but never utilizes `arch` in its body, leading to silent duplicate instances.
3. Clean PASS (100%) when distinct stem lists, Form-B 9-tuples, Tri-Band coverage,
   and active practice (FIB/MS) are used.
4. Form-B contract strict rejections:
   - Form-A tuple rejection
   - Difficulty without bloom rejection
   - 2-tuple distractor rejection in strict mode
   - [TPL-DYNAMIC-RATIONALE] rejection when distractor rationale lacks @var@
   - [TPL-VERIFIER] rejection for trivial ver_fn
   - [TPL-FIB-KATEX] rejection for external dollar delimiters in FIB
   - Extraction of distractor_ids in MS dry-run
   - Tri-band coverage and active practice validation
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


def _setup_workspace_shard(tmp_path: Path, shard_id: str = "shard_01", cid: str = "H-01", ctype: str = "skill"):
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
                "type": ctype,
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
        """Verifies that passing the same stems list to the tuples in TEMPLATES
        is rejected with [M3-ARCHETYPES] reporting repeated stem_es.
        """
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        code = r'''
import random

def _gen_h01(rng, arch=1):
    tc = rng.randint(200, 300)
    delta = rng.randint(100, 200) * arch
    th = tc + delta
    ans = round(1.0 - (tc / th), 3)
    dists = [round(1.0 - (tc / (th + 50 * i + 10)), 3) for i in range(1, 7)]
    v = {"tc": tc, "th": th, "ans": ans, **{f"d{i}": d for i, d in enumerate(dists, 1)}}
    return {
        "vars": v,
        "correct": r"$\eta = @ans@$",
        "distractors": [
            (f"D-H-01-{i:02d}", rf"$\eta = @d{i}@$", f"Error al computar con foco @tc@ en el paso {i}.")
            for i in range(1, 7)
        ],
    }

def gen_h01_1(rng): return _gen_h01(rng, 1)
def gen_h01_2(rng): return _gen_h01(rng, 2)
def gen_h01_3(rng): return _gen_h01(rng, 3)
def gen_h01_4(rng): return _gen_h01(rng, 4)

def ver_h01(res): return bool(res and isinstance(res.get("vars"), dict) and res.get("correct") == r"$\eta = @ans@$")

stems_reused = [
    r"Una máquina térmica opera entre focos a $T_H = @th@$ y $T_C = @tc@$. Calcule el rendimiento:",
    r"Determine la eficiencia para focos $T_H = @th@$ y $T_C = @tc@$:",
    r"Halle la razón de trabajo neto con $T_H = @th@$ y $T_C = @tc@$:",
]

hints = [
    "Identifique primero las temperaturas de foco caliente y foco frío en grados Kelvin.",
    "Aplique la expresión del límite termodinámico del ciclo reversible entre ambos focos.",
    "Realice la división entre el foco frío y caliente antes de restar de la unidad.",
]

TEMPLATES = [
    ("T-H01-01", "H-01", "multiple_choice_7_options", gen_h01_1, ver_h01, ("easy", "Remember"), stems_reused, hints, "Solución detallada paso a paso."),
    ("T-H01-02", "H-01", "multiple_choice_7_options", gen_h01_2, ver_h01, ("medium", "Apply"), stems_reused, hints, "Solución detallada paso a paso."),
    ("T-H01-03", "H-01", "multiple_choice_7_options", gen_h01_3, ver_h01, ("medium", "Analyze"), stems_reused, hints, "Solución detallada paso a paso."),
    ("T-H01-04", "H-01", "multiple_choice_7_options", gen_h01_4, ver_h01, ("hard", "Evaluate"), stems_reused, hints, "Solución detallada paso a paso."),
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

        code = r'''
import random

def _gen_h01(rng, arch=1):
    tc = rng.randint(250, 350)
    th = tc + rng.randint(150, 450)
    ans = round(1.0 - (tc / th), 3)
    dists = [round(ans + 0.05 * i, 3) for i in range(1, 7)]
    v = {"tc": tc, "th": th, "ans": ans, **{f"d{i}": d for i, d in enumerate(dists, 1)}}
    return {
        "vars": v,
        "correct": r"$\eta = @ans@$",
        "distractors": [
            (f"D-H-01-{i:02d}", rf"$\eta = @d{i}@$", f"Error al computar con foco @tc@ en el paso {i}.")
            for i in range(1, 7)
        ],
    }

def gen_h01_1(rng): return _gen_h01(rng, 1)
def gen_h01_2(rng): return _gen_h01(rng, 2)
def gen_h01_3(rng): return _gen_h01(rng, 3)
def gen_h01_4(rng): return _gen_h01(rng, 4)

def ver_h01(res): return bool(res and isinstance(res.get("vars"), dict) and res.get("correct") == r"$\eta = @ans@$")

stems_1 = [
    "Calcule la eficiencia directa con $T_H=@th@$ y $T_C=@tc@$:",
    "Determine el rendimiento directo del ciclo con $T_H=@th@$ y $T_C=@tc@$:",
    "Establezca el balance de energía frontal con $T_H=@th@$ y $T_C=@tc@$:",
]
stems_2 = [
    "Deduzca la temperatura inversa con $T_H=@th@$ y $T_C=@tc@$:",
    "Halle el rendimiento del ciclo invertido con $T_H=@th@$ y $T_C=@tc@$:",
    "Obtenga la relación inversa entre focos con $T_H=@th@$ y $T_C=@tc@$:",
]
stems_3 = [
    "Evalúe la perturbación térmica con $T_H=@th@$ y $T_C=@tc@$:",
    "Calcule la tasa perturbada con $T_H=@th@$ y $T_C=@tc@$:",
    "Determine la respuesta ante perturbación con $T_H=@th@$ y $T_C=@tc@$:",
]
stems_4 = [
    "Establezca la cota límite en la frontera con $T_H=@th@$ y $T_C=@tc@$:",
    "Determine el valor asintótico en la frontera con $T_H=@th@$ y $T_C=@tc@$:",
    "Halle la eficiencia límite extrema con $T_H=@th@$ y $T_C=@tc@$:",
]

hints = [
    "Identifique primero las temperaturas de foco caliente y foco frío en grados Kelvin.",
    "Aplique la expresión del límite termodinámico del ciclo reversible entre ambos focos.",
    "Realice la división entre el foco frío y caliente antes de restar de la unidad.",
]

TEMPLATES = [
    ("T-H01-U01", "H-01", "multiple_choice_7_options", gen_h01_1, ver_h01, ("easy", "Remember"), stems_1, hints, "Solución detallada paso a paso."),
    ("T-H01-U02", "H-01", "multiple_choice_7_options", gen_h01_2, ver_h01, ("medium", "Apply"), stems_2, hints, "Solución detallada paso a paso."),
    ("T-H01-U03", "H-01", "multiple_choice_7_options", gen_h01_3, ver_h01, ("medium", "Analyze"), stems_3, hints, "Solución detallada paso a paso."),
    ("T-H01-U04", "H-01", "multiple_choice_7_options", gen_h01_4, ver_h01, ("hard", "Evaluate"), stems_4, hints, "Solución detallada paso a paso."),
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
        """Verifies that when 4 distinct stem lists are supplied, Tri-Band coverage is met,
        and _gen_h01 actively branches on `arch`, compilation succeeds (PASS 100%).
        """
        work_dir, shards_dir, templates_dir, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        code = r'''
import random

def _gen_h01(rng, arch=1):
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
    dists = [round(1.0 - (tc / (th + 50 * i + 10)), 3) for i in range(1, 7)]
    v = {"tc": tc, "th": th, "ans": ans, **{f"d{i}": d for i, d in enumerate(dists, 1)}}
    if arch in (3, 4):
        # FIB format: correct is plain number string without surrounding dollar delimiters
        return {
            "vars": v,
            "correct": str(ans),
            "distractors": [],
        }
    return {
        "vars": v,
        "correct": r"$\eta = @ans@$",
        "distractors": [
            (f"D-H-01-{i:02d}", rf"$\eta = @d{i}@$", f"Error al computar con foco @tc@ en el paso {i}.")
            for i in range(1, 7)
        ],
    }

def gen_h01_1(rng): return _gen_h01(rng, 1)
def gen_h01_2(rng): return _gen_h01(rng, 2)
def gen_h01_3(rng): return _gen_h01(rng, 3)
def gen_h01_4(rng): return _gen_h01(rng, 4)

def ver_h01(res): return bool(res and isinstance(res.get("vars"), dict) and (res.get("correct") == r"$\eta = @ans@$" or str(res.get("vars", {}).get("ans")) == str(res.get("correct"))))

stems_1 = [
    r"Calcule la eficiencia directa de Carnot con focos $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
    r"Determine el rendimiento térmico frontal entre temperaturas $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
    r"Halle la razón de eficiencia del ciclo con focos $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
]
stems_2 = [
    r"En un análisis inverso con foco frío a $T_C = @tc@\text{ K}$ y caliente a $T_H = @th@\text{ K}$, halle $\eta$:",
    r"Deduzca el rendimiento inverso asociado a las cotas térmicas $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
    r"Calcule la eficiencia invertida para los reservorios $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
]
stems_3 = [
    r"Si se aplica una perturbación térmica con reservorios a $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$, evalúe $\eta$:",
    r"Calcule la variación en la eficiencia bajo el régimen perturbado $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
    r"Estime el nuevo valor de rendimiento ante perturbación con $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
]
stems_4 = [
    r"Bajo el régimen asintótico de frontera extrema con $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$, determine el límite:",
    r"En la cota extrema del ciclo con $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$, establezca la eficiencia límite $\eta$:",
    r"Calcule el valor asintótico de la eficiencia para $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
]

hints = [
    "Identifique primero las temperaturas de foco caliente y foco frío en grados Kelvin.",
    "Aplique la expresión del límite termodinámico del ciclo reversible entre ambos focos.",
    "Realice la división entre el foco frío y caliente antes de restar de la unidad.",
]

TEMPLATES = [
    ("T-H01-PASS-01", "H-01", "multiple_choice_7_options", gen_h01_1, ver_h01, ("easy", "Remember"), stems_1, hints, "Solución detallada paso a paso."),
    ("T-H01-PASS-02", "H-01", "multiple_choice_7_options", gen_h01_2, ver_h01, ("medium", "Apply"), stems_2, hints, "Solución detallada paso a paso."),
    ("T-H01-PASS-03", "H-01", "fill_in_the_blank", gen_h01_3, ver_h01, ("medium", "Analyze"), stems_3, hints, "Solución detallada paso a paso."),
    ("T-H01-PASS-04", "H-01", "fill_in_the_blank", gen_h01_4, ver_h01, ("hard", "Evaluate"), stems_4, hints, "Solución detallada paso a paso."),
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
        mathematically identical (correct, vars) across all tuples is rejected by [M3-ARCHETYPES].
        """
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        code = r'''
import random

def _gen_h01(rng, arch=1):
    _ = arch  # Trivial AST evasion attempt!
    tc = rng.randint(250, 350)
    delta = rng.randint(150, 450)
    th = tc + delta
    ans = round(1.0 - (tc / th), 3)
    dists = [round(1.0 - (tc / (th + 50 * i + 10)), 3) for i in range(1, 7)]
    v = {"tc": tc, "th": th, "ans": ans, **{f"d{i}": d for i, d in enumerate(dists, 1)}}
    return {
        "vars": v,
        "correct": r"$\eta = @ans@$",
        "distractors": [
            (f"D-H-01-{i:02d}", rf"$\eta = @d{i}@$", f"Error al computar con foco @tc@ en el paso {i}.")
            for i in range(1, 7)
        ],
    }

def gen_h01_1(rng): return _gen_h01(rng, 1)
def gen_h01_2(rng): return _gen_h01(rng, 2)
def gen_h01_3(rng): return _gen_h01(rng, 3)
def gen_h01_4(rng): return _gen_h01(rng, 4)

def ver_h01(res): return bool(res and isinstance(res.get("vars"), dict) and res.get("correct") == r"$\eta = @ans@$")

stems_1 = [
    r"Calcule la eficiencia directa con focos $T_H = @th@$ y $T_C = @tc@$:",
    r"Determine el rendimiento frontal con $T_H = @th@$ y $T_C = @tc@$:",
    r"Halle el valor de rendimiento con $T_H = @th@$ y $T_C = @tc@$:",
]
stems_2 = [
    r"Deduzca el rendimiento inverso para focos $T_H = @th@$ y $T_C = @tc@$:",
    r"Calcule la eficiencia en régimen inverso con $T_H = @th@$ y $T_C = @tc@$:",
    r"Halle la razón inversa con focos $T_H = @th@$ y $T_C = @tc@$:",
]
stems_3 = [
    r"Evalúe la perturbación térmica con focos $T_H = @th@$ y $T_C = @tc@$:",
    r"Estime el impacto perturbativo con $T_H = @th@$ y $T_C = @tc@$:",
    r"Halle la variación de eficiencia con $T_H = @th@$ y $T_C = @tc@$:",
]
stems_4 = [
    r"Establezca el comportamiento de frontera con $T_H = @th@$ y $T_C = @tc@$:",
    r"Determine la cota en el régimen asintótico con $T_H = @th@$ y $T_C = @tc@$:",
    r"Halle la eficiencia límite con $T_H = @th@$ y $T_C = @tc@$:",
]

hints = [
    "Identifique primero las temperaturas de foco caliente y foco frío en grados Kelvin.",
    "Aplique la expresión del límite termodinámico del ciclo reversible entre ambos focos.",
    "Realice la división entre el foco frío y caliente antes de restar de la unidad.",
]

TEMPLATES = [
    ("T-H01-U01", "H-01", "multiple_choice_7_options", gen_h01_1, ver_h01, ("easy", "Remember"), stems_1, hints, "Solución detallada paso a paso."),
    ("T-H01-U02", "H-01", "multiple_choice_7_options", gen_h01_2, ver_h01, ("medium", "Apply"), stems_2, hints, "Solución detallada paso a paso."),
    ("T-H01-U03", "H-01", "multiple_choice_7_options", gen_h01_3, ver_h01, ("medium", "Analyze"), stems_3, hints, "Solución detallada paso a paso."),
    ("T-H01-U04", "H-01", "multiple_choice_7_options", gen_h01_4, ver_h01, ("hard", "Evaluate"), stems_4, hints, "Solución detallada paso a paso."),
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
        in shards/shard_fixes/H-01.py with 4 genuine archetypes, compilation succeeds cleanly (PASS 100%).
        """
        work_dir, shards_dir, templates_dir, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        broken_base_code = r'''
import random

def _gen_h01(rng, arch=1):
    return {"vars": {}, "correct": "0", "distractors": []}

def gen_broken(rng): return _gen_h01(rng, 1)
def ver_broken(res): return True

TEMPLATES = [
    ("T-H01-01", "H-01", "fill_in_the_blank", gen_broken, ver_broken, ("easy", "Remember"), ["Stem 1", "Stem 2", "Stem 3"], ["Pista corta"], "Solución"),
]
'''
        shard_py.write_text(broken_base_code, encoding="utf-8")

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
    dists = [round(1.0 - (tc / (th + 50 * i + 10)), 3) for i in range(1, 7)]
    v = {"tc": tc, "th": th, "ans": ans, **{f"d{i}": d for i, d in enumerate(dists, 1)}}
    if arch in (3, 4):
        return {
            "vars": v,
            "correct": str(ans),
            "distractors": [],
        }
    return {
        "vars": v,
        "correct": r"$\eta = @ans@$",
        "distractors": [
            (f"D-H-01-{i:02d}", rf"$\eta = @d{i}@$", f"Error al computar con foco @tc@ en el paso {i}.")
            for i in range(1, 7)
        ],
    }

def gen_h01_1(rng): return _gen_h01_modular(rng, 1)
def gen_h01_2(rng): return _gen_h01_modular(rng, 2)
def gen_h01_3(rng): return _gen_h01_modular(rng, 3)
def gen_h01_4(rng): return _gen_h01_modular(rng, 4)

def ver_h01(res): return bool(res and isinstance(res.get("vars"), dict) and (res.get("correct") == r"$\eta = @ans@$" or str(res.get("vars", {}).get("ans")) == str(res.get("correct"))))

stems_1 = [
    r"Calcule la eficiencia directa con focos $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
    r"Halle la razón de eficiencia con focos $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
    r"Determine el rendimiento frontal con $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
]
stems_2 = [
    r"En un análisis inverso con foco frío a $T_C = @tc@\text{ K}$ y caliente a $T_H = @th@\text{ K}$, halle $\eta$:",
    r"Deduzca el rendimiento inverso para focos $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
    r"Calcule la eficiencia invertida con $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
]
stems_3 = [
    r"Si se aplica una perturbación térmica con reservorios a $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$, evalúe $\eta$:",
    r"Estime el impacto perturbativo con $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
    r"Calcule la variación en la eficiencia bajo el régimen $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
]
stems_4 = [
    r"Bajo el régimen asintótico de frontera extrema con $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$, determine el límite:",
    r"En la cota extrema del ciclo con $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$, establezca la eficiencia $\eta$:",
    r"Calcule el valor asintótico de la eficiencia para $T_H = @th@\text{ K}$ y $T_C = @tc@\text{ K}$:",
]

hints = [
    "Identifique primero las temperaturas de foco caliente y foco frío en grados Kelvin.",
    "Aplique la expresión del límite termodinámico del ciclo reversible entre ambos focos.",
    "Realice la división entre el foco frío y caliente antes de restar de la unidad.",
]

TEMPLATES = [
    ("T-H01-FIX-01", "H-01", "multiple_choice_7_options", gen_h01_1, ver_h01, ("easy", "Remember"), stems_1, hints, "Solución detallada paso a paso."),
    ("T-H01-FIX-02", "H-01", "multiple_choice_7_options", gen_h01_2, ver_h01, ("medium", "Apply"), stems_2, hints, "Solución detallada paso a paso."),
    ("T-H01-FIX-03", "H-01", "fill_in_the_blank", gen_h01_3, ver_h01, ("medium", "Analyze"), stems_3, hints, "Solución detallada paso a paso."),
    ("T-H01-FIX-04", "H-01", "fill_in_the_blank", gen_h01_4, ver_h01, ("hard", "Evaluate"), stems_4, hints, "Solución detallada paso a paso."),
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

    def test_rejection_of_form_a(self, tmp_path: Path):
        """Verifies that passing a legacy Form-A tuple is rejected with Form-A detection guidance."""
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        code = r'''
import random
def gen(rng): return {"vars": {"v": 1}, "correct": "1", "distractors": []}
def ver(res): return bool(res and "vars" in res)
stems = ["Stem uno con variable @v@", "Stem dos con variable @v@", "Stem tres con variable @v@"]
hints = ["Pista uno con suficiente longitud", "Pista dos con suficiente longitud", "Pista tres con suficiente longitud"]

# Legacy Form-A 9-tuple: (cid, qtype, stems, gen, ver, sol, kc, hints, ref)
TEMPLATES = [
    ("H-01", "fill_in_the_blank", stems, gen, ver, "Solución", "KC", hints, ("doc.pdf", 1, "")),
]
'''
        shard_py.write_text(code, encoding="utf-8")
        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert not success
        err_str = "\n".join(errors)
        assert "Contrato legacy Form-A detectado" in err_str or "Form-B" in err_str

    def test_rejection_of_difficulty_without_bloom(self, tmp_path: Path):
        """Verifies that element [5] must be a 2-tuple (difficulty, bloom) and not a plain string."""
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        code = r'''
import random
def gen(rng): return {"vars": {"v": 1}, "correct": "1", "distractors": []}
def ver(res): return bool(res and "vars" in res)
stems = ["Stem uno con variable @v@", "Stem dos con variable @v@", "Stem tres con variable @v@"]
hints = ["Pista uno con suficiente longitud", "Pista dos con suficiente longitud", "Pista tres con suficiente longitud"]

TEMPLATES = [
    ("T-H01-01", "H-01", "fill_in_the_blank", gen, ver, "medium", stems, hints, "Solución"),
]
'''
        shard_py.write_text(code, encoding="utf-8")
        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert not success
        err_str = "\n".join(errors)
        assert "2-tupla (difficulty, bloom)" in err_str

    def test_rejection_of_2tuple_distractor_in_strict_mode(self, tmp_path: Path):
        """Verifies that in strict=True, MC7 distractors must be 3-tuples (did, val, rationale)."""
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        code = r'''
import random
def gen(rng):
    v = rng.randint(10, 50)
    return {
        "vars": {"v": v},
        "correct": rf"$\eta = {v}$",
        # 2-tuple distractor: forbidden in strict=True!
        "distractors": [(f"D-H-01-{i:02d}", rf"$\eta = {v + i}$") for i in range(1, 7)],
    }
def ver(res): return bool(res and "vars" in res)
stems = ["Stem uno con variable @v@", "Stem dos con variable @v@", "Stem tres con variable @v@"]
hints = ["Pista uno con suficiente longitud", "Pista dos con suficiente longitud", "Pista tres con suficiente longitud"]

TEMPLATES = [
    ("T-H01-01", "H-01", "multiple_choice_7_options", gen, ver, ("medium", "Apply"), stems, hints, "Solución"),
]
'''
        shard_py.write_text(code, encoding="utf-8")
        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=True)
        assert not success
        err_str = "\n".join(errors)
        assert "[TPL-MC7-STRICT]" in err_str or "3-tupla" in err_str

    def test_rejection_of_static_rationale_tpl_dynamic_rationale(self, tmp_path: Path):
        """Verifies that a parametric distractor with static rationale lacking @var@ triggers [TPL-DYNAMIC-RATIONALE]."""
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        code = r'''
import random
def gen(rng):
    v = rng.randint(10, 50)
    dists = [v + i for i in range(1, 7)]
    return {
        "vars": {"v": v, **{f"d{i}": d for i, d in enumerate(dists, 1)}},
        "correct": r"$\eta = @v@$",
        # Rationale is static string with no @var@ token!
        "distractors": [
            (f"D-H-01-{i:02d}", rf"$\eta = @d{i}@$", "Esta es una explicación estática sin variables.")
            for i in range(1, 7)
        ],
    }
def ver(res): return bool(res and "vars" in res)
stems = ["Stem uno con variable @v@", "Stem dos con variable @v@", "Stem tres con variable @v@"]
hints = ["Pista uno con suficiente longitud", "Pista dos con suficiente longitud", "Pista tres con suficiente longitud"]

TEMPLATES = [
    ("T-H01-01", "H-01", "multiple_choice_7_options", gen, ver, ("medium", "Apply"), stems, hints, "Solución"),
]
'''
        shard_py.write_text(code, encoding="utf-8")
        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=True)
        assert not success
        err_str = "\n".join(errors)
        assert "[TPL-DYNAMIC-RATIONALE]" in err_str

    def test_rejection_of_trivial_ver_fn(self, tmp_path: Path):
        """Verifies that a trivial ver_fn like `return True` is rejected by [TPL-VERIFIER]."""
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        code = r'''
import random
def gen(rng): return {"vars": {"v": 1}, "correct": "1", "distractors": []}
def ver(res): return True  # Trivial!
stems = ["Stem uno con variable @v@", "Stem dos con variable @v@", "Stem tres con variable @v@"]
hints = ["Pista uno con suficiente longitud", "Pista dos con suficiente longitud", "Pista tres con suficiente longitud"]

TEMPLATES = [
    ("T-H01-01", "H-01", "fill_in_the_blank", gen, ver, ("medium", "Apply"), stems, hints, "Solución"),
]
'''
        shard_py.write_text(code, encoding="utf-8")
        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert not success
        err_str = "\n".join(errors)
        assert "[TPL-VERIFIER]" in err_str

    def test_rejection_of_external_dollar_in_fib(self, tmp_path: Path):
        """Verifies that external dollar delimiters in correct/value of FIB trigger [TPL-FIB-KATEX]."""
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        code = r'''
import random
def gen(rng):
    v = rng.randint(10, 50)
    # Deliberate external $ delimiters in FIB correct field
    return {"vars": {"v": v}, "correct": rf"${v}$", "distractors": []}
def ver(res): return bool(res and "vars" in res)
stems = ["Stem uno con variable @v@", "Stem dos con variable @v@", "Stem tres con variable @v@"]
hints = ["Pista uno con suficiente longitud", "Pista dos con suficiente longitud", "Pista tres con suficiente longitud"]

TEMPLATES = [
    ("T-H01-01", "H-01", "fill_in_the_blank", gen, ver, ("medium", "Apply"), stems, hints, "Solución"),
]
'''
        shard_py.write_text(code, encoding="utf-8")
        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert not success
        err_str = "\n".join(errors)
        assert "[TPL-FIB-KATEX]" in err_str

    def test_extraction_of_distractor_ids_in_ms(self, tmp_path: Path):
        """Verifies that dry-run extracts distractor_id of false options in MS templates."""
        work_dir, shards_dir, templates_dir, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01", ctype="concept")
        shard_py = shards_dir / "shard_01_data.py"

        code = r'''
import random
def gen_ms(rng):
    v = rng.randint(10, 500)
    w = rng.randint(10, 500)
    return {
        "vars": {"v": v, "w": w},
        "options": [
            {"value": "Afirmación correcta uno @v@", "is_correct": True},
            {"value": "Afirmación correcta dos @w@", "is_correct": True},
            {
                "value": "Afirmación errónea con @v@",
                "is_correct": False,
                "distractor_id": "D-H-01-01",
                "error_rationale": "Justificación errónea dependiente de @v@.",
            },
            {
                "value": "Afirmación errónea con @w@",
                "is_correct": False,
                "distractor_id": "D-H-01-02",
                "error_rationale": "Justificación errónea dependiente de @w@.",
            },
        ],
    }
def ver_ms(res): return bool(res and "options" in res)
stems = ["Stem opción uno @v@", "Stem opción dos @v@", "Stem opción tres @v@"]
hints = ["Pista larga para el primer paso", "Pista larga para el segundo paso", "Pista larga para el tercer paso"]

TEMPLATES = [
    ("T-H01-01", "H-01", "multiple_select", gen_ms, ver_ms, ("medium", "Analyze"), stems, hints, "Solución explicada."),
]
'''
        shard_py.write_text(code, encoding="utf-8")
        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False, seeds=5)
        assert success, f"Expected MS compile to succeed, got: {errors}"
        out_json = templates_dir / "H-01.json"
        data = json.loads(out_json.read_text(encoding="utf-8"))
        assert "D-H-01-01" in data.get("distractor_ids", [])

    def test_tri_band_coverage_and_active_practice_validation(self, tmp_path: Path):
        """Verifies rejection when difficulty bands are missing or active practice requirements are unmet."""
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01", ctype="skill")
        shard_py = shards_dir / "shard_01_data.py"

        # Case 1: Missing "hard" band (only easy and medium)
        code_missing_band = r'''
import random
def _gen(rng, arch=1):
    v = rng.randint(10, 50) * arch
    return {
        "vars": {"v": v},
        "correct": str(v),
        "distractors": [],
    }
def g1(rng): return _gen(rng, 1)
def g2(rng): return _gen(rng, 2)
def g3(rng): return _gen(rng, 3)
def ver(res): return bool(res and (res.get("correct") == r"$\eta = @v@$" or res.get("correct") == str(res.get("vars", {}).get("v"))))
s1 = ["Stem uno A @v@", "Stem uno B @v@", "Stem uno C @v@"]
s2 = ["Stem dos A @v@", "Stem dos B @v@", "Stem dos C @v@"]
s3 = ["Stem tres A @v@", "Stem tres B @v@", "Stem tres C @v@"]
hints = ["Pista larga para el primer paso", "Pista larga para el segundo paso", "Pista larga para el tercer paso"]

TEMPLATES = [
    ("T-H01-01", "H-01", "fill_in_the_blank", g1, ver, ("easy", "Remember"), s1, hints, "Solución 1"),
    ("T-H01-02", "H-01", "fill_in_the_blank", g2, ver, ("medium", "Apply"), s2, hints, "Solución 2"),
    ("T-H01-03", "H-01", "fill_in_the_blank", g3, ver, ("medium", "Analyze"), s3, hints, "Solución 3"),
]
'''
        shard_py.write_text(code_missing_band, encoding="utf-8")
        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=True, min_archetypes=3)
        assert not success
        err_str = "\n".join(errors)
        assert "Cobertura incompleta de bandas de dificultad" in err_str
        assert "hard" in err_str

        # Case 2: Skill competency lacking active practice (requires >= 2 FIB/MS, providing only 1 FIB and 2 MC7)
        code_lacking_active = r'''
import random
def _gen(rng, arch=1):
    v = rng.randint(10, 50) * arch
    dists = [v + i for i in range(1, 7)]
    if arch == 3:
        return {"vars": {"v": v}, "correct": str(v), "distractors": []}
    return {
        "vars": {"v": v, **{f"d{i}": d for i, d in enumerate(dists, 1)}},
        "correct": r"$\eta = @v@$",
        "distractors": [(f"D-H-01-{i:02d}", rf"$\eta = @d{i}@$", f"Error al usar @v@ en el paso {i}.") for i in range(1, 7)],
    }
def g1(rng): return _gen(rng, 1)
def g2(rng): return _gen(rng, 2)
def g3(rng): return _gen(rng, 3)
def ver(res): return bool(res and (res.get("correct") == r"$\eta = @v@$" or res.get("correct") == str(res.get("vars", {}).get("v"))))
s1 = ["Stem uno A @v@", "Stem uno B @v@", "Stem uno C @v@"]
s2 = ["Stem dos A @v@", "Stem dos B @v@", "Stem dos C @v@"]
s3 = ["Stem tres A @v@", "Stem tres B @v@", "Stem tres C @v@"]
hints = ["Pista larga para el primer paso", "Pista larga para el segundo paso", "Pista larga para el tercer paso"]

TEMPLATES = [
    ("T-H01-01", "H-01", "multiple_choice_7_options", g1, ver, ("easy", "Remember"), s1, hints, "Solución 1"),
    ("T-H01-02", "H-01", "multiple_choice_7_options", g2, ver, ("medium", "Apply"), s2, hints, "Solución 2"),
    ("T-H01-03", "H-01", "fill_in_the_blank", g3, ver, ("hard", "Analyze"), s3, hints, "Solución 3"),
]
'''
        shard_py.write_text(code_lacking_active, encoding="utf-8")
        success2, errors2 = compile_shard(work_dir, shard_id="shard_01", strict=True, min_archetypes=3)
        assert not success2
        err_str2 = "\n".join(errors2)
        assert "Práctica activa insuficiente" in err_str2

    def test_default_min_archetypes_contract(self, tmp_path: Path):
        """Verifies default min_archetypes=3 when not passed, respecting manifest or explicit arg."""
        work_dir, shards_dir, _, cta_file, manifest_file = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        # 1. Update manifest to remove min_archetypes
        m_data = json.loads(manifest_file.read_text(encoding="utf-8"))
        m_data.pop("min_archetypes", None)
        manifest_file.write_text(json.dumps(m_data), encoding="utf-8")

        shard_py = shards_dir / "shard_01_data.py"
        code_2_tpls = r'''
import random
def _gen(rng, arch=1):
    v = rng.randint(10, 50) * arch
    return {"vars": {"v": v}, "correct": str(v), "distractors": []}
def g1(rng): return _gen(rng, 1)
def g2(rng): return _gen(rng, 2)
def ver(res): return bool(res and "vars" in res)
s1 = ["Consigna A uno @v@", "Consigna A dos @v@", "Consigna A tres @v@"]
s2 = ["Consigna B uno @v@", "Consigna B dos @v@", "Consigna B tres @v@"]
hints = ["Pista uno con suficiente longitud", "Pista dos con suficiente longitud", "Pista tres con suficiente longitud"]

TEMPLATES = [
    ("T-H01-01", "H-01", "fill_in_the_blank", g1, ver, ("easy", "Remember"), s1, hints, "Sol 1"),
    ("T-H01-02", "H-01", "fill_in_the_blank", g2, ver, ("medium", "Apply"), s2, hints, "Sol 2"),
]
'''
        shard_py.write_text(code_2_tpls, encoding="utf-8")

        # When min_archetypes is None, under strict=True default effective is 3 -> fails because 2 < 3
        success1, errors1 = compile_shard(work_dir, shard_id="shard_01", strict=True, min_archetypes=None)
        assert not success1
        err_str1 = "\n".join(errors1)
        assert "[M3-ARCHETYPES]" in err_str1
        assert "define solo 2 plantilla(s)" in err_str1

        # Explicit min_archetypes=1 override is respected (bypassing M3 archetypes gate)
        code_1_tpl = r'''
import random
def g1(rng):
    v = rng.randint(10, 500)
    return {"vars": {"v": v}, "correct": str(v), "distractors": []}
def ver(res): return bool(res and res.get("correct") == str(res.get("vars", {}).get("v")))
s1 = [
    "Consigna A uno @v@ con formulación distintiva",
    "Consigna A dos @v@ con variación estructural",
    "Consigna A tres @v@ con consigna analítica",
    "Consigna A cuatro @v@ con planteamiento formal",
    "Consigna A cinco @v@ con derivación directa",
    "Consigna A seis @v@ con cálculo sistemático",
]
hints = ["Pista uno con suficiente longitud", "Pista dos con suficiente longitud", "Pista tres con suficiente longitud"]
TEMPLATES = [
    ("T-H01-01", "H-01", "fill_in_the_blank", g1, ver, ("easy", "Remember"), s1, hints, "Sol 1"),
]
'''
        shard_py.write_text(code_1_tpl, encoding="utf-8")
        success2, errors2 = compile_shard(work_dir, shard_id="shard_01", strict=True, min_archetypes=1, seeds=10)
        assert success2, f"Explicit min_archetypes=1 must be respected: {errors2}"

        # Manifest min_archetypes=4 is respected
        m_data["min_archetypes"] = 4
        manifest_file.write_text(json.dumps(m_data), encoding="utf-8")
        code_3_tpls = r'''
import random
def _gen(rng, arch=1):
    v = rng.randint(10, 50) * arch
    return {"vars": {"v": v}, "correct": str(v), "distractors": []}
def g1(rng): return _gen(rng, 1)
def g2(rng): return _gen(rng, 2)
def g3(rng): return _gen(rng, 3)
def ver(res): return bool(res and res.get("correct") == str(res.get("vars", {}).get("v")))
s1 = ["Consigna A uno @v@", "Consigna A dos @v@", "Consigna A tres @v@"]
s2 = ["Consigna B uno @v@", "Consigna B dos @v@", "Consigna B tres @v@"]
s3 = ["Consigna C uno @v@", "Consigna C dos @v@", "Consigna C tres @v@"]
hints = ["Pista uno con suficiente longitud", "Pista dos con suficiente longitud", "Pista tres con suficiente longitud"]

TEMPLATES = [
    ("T-H01-01", "H-01", "fill_in_the_blank", g1, ver, ("easy", "Remember"), s1, hints, "Sol 1"),
    ("T-H01-02", "H-01", "fill_in_the_blank", g2, ver, ("medium", "Apply"), s2, hints, "Sol 2"),
    ("T-H01-03", "H-01", "fill_in_the_blank", g3, ver, ("hard", "Analyze"), s3, hints, "Sol 3"),
]
'''
        shard_py.write_text(code_3_tpls, encoding="utf-8")
        success3, errors3 = compile_shard(work_dir, shard_id="shard_01", strict=True, min_archetypes=None)
        assert not success3
        err_str3 = "\n".join(errors3)
        assert "[M3-ARCHETYPES]" in err_str3
        assert "define solo 3 plantilla(s)" in err_str3

    def test_ms_and_mc7_strict_rejection_with_exact_line_diagnostics(self, tmp_path: Path):
        """Verifies deterministic line diagnostics for MC7 2-tuples and MS options in strict mode."""
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01", ctype="concept")
        shard_py = shards_dir / "shard_01_data.py"

        # Case 1: MS option missing distractor_id
        code_ms_no_id = r'''
import random
def gen_ms(rng):
    return {
        "vars": {"v": 10},
        "options": [
            {"value": "Afirmación correcta", "is_correct": True},
            {"value": "Afirmación falsa sin id", "is_correct": False, "error_rationale": "Justificación suficientemente larga para la opción."},
        ],
    }
def ver_ms(res): return bool(res and "options" in res)
stems = ["Enunciado opción uno @v@", "Enunciado opción dos @v@", "Enunciado opción tres @v@"]
hints = ["Pista uno con suficiente longitud", "Pista dos con suficiente longitud", "Pista tres con suficiente longitud"]

TEMPLATES = [
    ("T-H01-01", "H-01", "multiple_select", gen_ms, ver_ms, ("medium", "Analyze"), stems, hints, "Solución explicada."),
]
'''
        shard_py.write_text(code_ms_no_id, encoding="utf-8")
        success1, errors1 = compile_shard(work_dir, shard_id="shard_01", strict=True, min_archetypes=1)
        assert not success1
        err_str1 = "\n".join(errors1)
        assert "[TPL-MS-DISTRACTOR-ID]" in err_str1
        assert "Línea" in err_str1
        assert "shard_01_data.py" in err_str1

        # Case 2: MS option with rationale < 20 chars
        code_ms_short_rat = r'''
import random
def gen_ms2(rng):
    return {
        "vars": {"v": 10},
        "options": [
            {"value": "Afirmación correcta", "is_correct": True},
            {"value": "Afirmación falsa", "is_correct": False, "distractor_id": "D-H-01-01", "error_rationale": "Corta."},
        ],
    }
def ver_ms2(res): return bool(res and "options" in res)
stems = ["Enunciado opción uno @v@", "Enunciado opción dos @v@", "Enunciado opción tres @v@"]
hints = ["Pista uno con suficiente longitud", "Pista dos con suficiente longitud", "Pista tres con suficiente longitud"]

TEMPLATES = [
    ("T-H01-01", "H-01", "multiple_select", gen_ms2, ver_ms2, ("medium", "Analyze"), stems, hints, "Solución explicada."),
]
'''
        shard_py.write_text(code_ms_short_rat, encoding="utf-8")
        success2, errors2 = compile_shard(work_dir, shard_id="shard_01", strict=True, min_archetypes=1)
        assert not success2
        err_str2 = "\n".join(errors2)
        assert "[TPL-MS-RATIONALE]" in err_str2
        assert "Línea" in err_str2

        # Case 3: MC7 2-tuple distractor in strict mode
        code_mc7_2tuple = r'''
import random
def gen_mc7(rng):
    v = rng.randint(10, 50)
    return {
        "vars": {"v": v},
        "correct": rf"$\alpha = {v}$",
        "distractors": [(f"D-H-01-{i:02d}", rf"$\alpha = {v + i}$") for i in range(1, 7)],
    }
def ver_mc7(res): return bool(res and "vars" in res)
stems = ["Enunciado MC7 uno @v@", "Enunciado MC7 dos @v@", "Enunciado MC7 tres @v@"]
hints = ["Pista uno con suficiente longitud", "Pista dos con suficiente longitud", "Pista tres con suficiente longitud"]

TEMPLATES = [
    ("T-H01-01", "H-01", "multiple_choice_7_options", gen_mc7, ver_mc7, ("medium", "Apply"), stems, hints, "Solución."),
]
'''
        shard_py.write_text(code_mc7_2tuple, encoding="utf-8")
        success3, errors3 = compile_shard(work_dir, shard_id="shard_01", strict=True, min_archetypes=1)
        assert not success3
        err_str3 = "\n".join(errors3)
        assert "[TPL-MC7-STRICT]" in err_str3
        assert "Línea" in err_str3

    def test_competency_hab_two_fib_one_ms_passes_strict_and_tpl_d3(self, tmp_path: Path):
        """Confirms a Hab-* competency with 2 FIB + 1 MS (cero MC7) compiles cleanly in strict=True,
        populates distractor_ids in MS, and satisfies check_templates TPL-D3.
        """
        work_dir, shards_dir, templates_dir, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "Hab-01", ctype="skill")
        shard_py = shards_dir / "shard_01_data.py"

        code = r'''
import random

# Archetype 1: FIB Easy Remember
def gen_fib1(rng):
    a = rng.randint(10, 30)
    b = rng.randint(2, 5)
    ans = a + b
    return {
        "vars": {"a": a, "b": b, "ans": ans},
        "correct": str(ans),
        "distractors": [],
    }
def ver_fib1(res): return bool(res and isinstance(res.get("vars"), dict) and "ans" in res["vars"])

# Archetype 2: FIB Hard Evaluate
def gen_fib2(rng):
    w = rng.randint(50, 90)
    ans = w * 2
    return {
        "vars": {"w": w, "ans": ans},
        "correct": str(ans),
        "distractors": [],
    }
def ver_fib2(res): return bool(res and isinstance(res.get("vars"), dict) and "ans" in res["vars"])

# Archetype 3: MS Medium Apply
def gen_ms(rng):
    k = rng.randint(2, 8)
    d1 = k + 1
    d2 = k + 2
    return {
        "vars": {"k": k, "d1": d1, "d2": d2},
        "options": [
            {"value": "Afirmación verdadera fundamental sobre factor @k@.", "is_correct": True},
            {"value": "Segunda afirmación verdadera complementaria con @k@.", "is_correct": True},
            {
                "value": "Afirmación errónea basada en valor espurio @d1@.",
                "is_correct": False,
                "distractor_id": "D-Hab-01-01",
                "error_rationale": "Inversión formal del factor térmico usando @k@ erróneo.",
            },
            {
                "value": "Afirmación errónea con valor desplazado @d2@.",
                "is_correct": False,
                "distractor_id": "D-Hab-01-02",
                "error_rationale": "Confusión entre calor cedido y trabajo neto con base @k@.",
            },
        ],
    }
def ver_ms(res): return bool(res and isinstance(res.get("vars"), dict) and "k" in res["vars"])

s1 = [
    r"Calcule la suma básica nominal sabiendo que los sumandos son $a = @a@$ y $b = @b@$:",
    r"Determine la adición del proceso para los parámetros $a = @a@$ y $b = @b@$:",
    r"Halle la cantidad combinada correspondiente a $a = @a@$ y $b = @b@$:",
    r"Establezca el total acumulado considerando las magnitudes $a = @a@$ y $b = @b@$:",
    r"Deduzca el resultado de la agregación de las magnitudes $a = @a@$ y $b = @b@$:",
]
s2 = [
    r"En el régimen asintótico superior con escala $w = @w@$, halle el doble del valor:",
    r"Evalúe el doble del sistema térmico cuando el valor base es $w = @w@$:",
    r"Determine el factor doble del límite asintótico con escala térmica $w = @w@$:",
    r"Calcule el valor duplicado resultante bajo el parámetro de escala $w = @w@$:",
    r"Halle el resultado del doble de la magnitud escalada con $w = @w@$:",
]
s3 = [
    r"Seleccione todas las afirmaciones válidas respecto al parámetro de escala $k = @k@$:",
    r"Identifique las proposiciones analíticas verdaderas para el régimen con $k = @k@$:",
    r"Determine cuáles de las siguientes propiedades se verifican para $k = @k@$:",
    r"Indique el conjunto de enunciados correctos asociados al valor $k = @k@$:",
    r"Elija las aseveraciones matemáticamente rigurosas para la escala $k = @k@$:",
]

hints = [
    "Identifique con precisión las variables del enunciado y sus unidades.",
    "Aplique las relaciones algebraicas formales correspondientes a cada régimen.",
    "Verifique la consistencia numérica y las cotas dimensionales del resultado.",
]

TEMPLATES = [
    ("T-Hab01-01", "Hab-01", "fill_in_the_blank", gen_fib1, ver_fib1, ("easy", "Remember"), s1, hints, "Solución detallada paso a paso 1."),
    ("T-Hab01-02", "Hab-01", "fill_in_the_blank", gen_fib2, ver_fib2, ("hard", "Evaluate"), s2, hints, "Solución detallada paso a paso 2."),
    ("T-Hab01-03", "Hab-01", "multiple_select", gen_ms, ver_ms, ("medium", "Apply"), s3, hints, "Solución detallada paso a paso 3."),
]
'''
        # Update CTA with Hab-01 distractors
        cta_payload = {
            "competencies": [
                {
                    "id": "Hab-01",
                    "name": "Competencia Hab-01 Termodinámica",
                    "type": "skill",
                    "distractors": [
                        {"id": "D-Hab-01-01", "remediation_hint": "Inversión del cociente térmico en la formulación."},
                        {"id": "D-Hab-01-02", "remediation_hint": "Confusión entre calor cedido y trabajo neto."},
                        {"id": "D-Hab-01-03", "remediation_hint": "Desplazamiento erróneo en la diferencia de reservorios."},
                        {"id": "D-Hab-01-04", "remediation_hint": "Factor espurio en el reservorio caliente."},
                    ],
                }
            ]
        }
        cta_file.write_text(json.dumps(cta_payload, indent=2, ensure_ascii=False), encoding="utf-8")

        shard_py.write_text(code, encoding="utf-8")
        success, errors = compile_shard(
            work_dir_or_path=work_dir,
            shard_id="shard_01",
            strict=True,
            min_archetypes=3,
            cta_path=cta_file,
            seeds=20,
        )

        assert success, f"Expected clean compilation of 2 FIB + 1 MS, got: {errors}"
        assert len(errors) == 0

        # Verify output templates JSON has distractor_ids populated in MS
        out_json = templates_dir / "Hab-01.json"
        assert out_json.is_file()
        data = json.loads(out_json.read_text(encoding="utf-8"))
        assert "templates" in data
        assert len(data["templates"]) == 3

        ms_tpl = next(t for t in data["templates"] if t["interaction_type"] == "multiple_select")
        assert "D-Hab-01-01" in ms_tpl.get("distractor_ids", [])
        assert "D-Hab-01-02" in ms_tpl.get("distractor_ids", [])

    def test_fib_external_dollars_rejected_immediately(self, tmp_path: Path):
        """Verifies FIB answers with external $ delimiters ('$42$', '$x + 1$') fail immediately with [TPL-FIB-KATEX]."""
        work_dir, shards_dir, _, cta_file, _ = _setup_workspace_shard(tmp_path, "shard_01", "H-01")
        shard_py = shards_dir / "shard_01_data.py"

        # Test case: "$42$"
        code_dollar_num = r'''
import random
def gen(rng): return {"vars": {"v": 42}, "correct": "$42$", "distractors": []}
def ver(res): return bool(res and "vars" in res)
stems = ["Enunciado uno @v@", "Enunciado dos @v@", "Enunciado tres @v@"]
hints = ["Pista uno con suficiente longitud", "Pista dos con suficiente longitud", "Pista tres con suficiente longitud"]

TEMPLATES = [
    ("T-H01-01", "H-01", "fill_in_the_blank", gen, ver, ("medium", "Apply"), stems, hints, "Solución."),
]
'''
        shard_py.write_text(code_dollar_num, encoding="utf-8")
        success1, errors1 = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert not success1
        err_str1 = "\n".join(errors1)
        assert "[TPL-FIB-KATEX]" in err_str1
        assert "$42$" in err_str1
        assert "Línea" in err_str1

        # Test case: "$x + 1$"
        code_dollar_expr = r'''
import random
def gen(rng): return {"vars": {"v": 1}, "correct": "$x + 1$", "distractors": []}
def ver(res): return bool(res and "vars" in res)
stems = ["Enunciado uno @v@", "Enunciado dos @v@", "Enunciado tres @v@"]
hints = ["Pista uno con suficiente longitud", "Pista dos con suficiente longitud", "Pista tres con suficiente longitud"]

TEMPLATES = [
    ("T-H01-01", "H-01", "fill_in_the_blank", gen, ver, ("medium", "Apply"), stems, hints, "Solución."),
]
'''
        shard_py.write_text(code_dollar_expr, encoding="utf-8")
        success2, errors2 = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert not success2
        err_str2 = "\n".join(errors2)
        assert "[TPL-FIB-KATEX]" in err_str2
        assert "$x + 1$" in err_str2
        assert "Línea" in err_str2

