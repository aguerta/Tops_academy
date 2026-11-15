import json
import sys
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

import dispatch  # noqa: E402


@pytest.mark.parametrize("granularity", ["standard", "fine", "coarse"])
def test_granularity_substitution_and_5kb_limit(tmp_path: Path, granularity: str) -> None:
    """Verify 1-to-1 granularity substitution in c2c_cta_architect.json with <= 5120 bytes."""
    work_dir = tmp_path / "work"
    work_dir.mkdir(parents=True, exist_ok=True)
    (work_dir / "pre_cta_manifest.json").write_text(
        json.dumps({"course_id": "test_course", "granularity": granularity}),
        encoding="utf-8",
    )

    dispatch.generate_define_subagent_specs(work_dir, lean=True)
    arch_file = work_dir / "dispatch" / "types" / "c2c_cta_architect.json"
    assert arch_file.is_file()

    arch_spec = json.loads(arch_file.read_text(encoding="utf-8"))
    sys_prompt = arch_spec["system_prompt"]
    expected_label = dispatch.GRANULARITY_SPECS[granularity][0]

    assert f'granularity="{expected_label}"' in sys_prompt


def test_granularity_zero_byte_inflation_vs_standard(tmp_path: Path) -> None:
    """Verify fine/coarse modes never exceed standard system_prompt byte size."""
    sizes = {}
    for idx, gran in enumerate(["standard", "fine", "coarse"]):
        work_dir = tmp_path / f"work_{idx}"
        work_dir.mkdir(parents=True, exist_ok=True)
        manifest_name = "ingestion_manifest.json" if gran == "coarse" else "pre_cta_manifest.json"
        (work_dir / manifest_name).write_text(
            json.dumps({"course_id": "test_course", "granularity": gran}),
            encoding="utf-8",
        )
        dispatch.generate_define_subagent_specs(work_dir, lean=True)
        arch_spec = json.loads((work_dir / "dispatch" / "types" / "c2c_cta_architect.json").read_text(encoding="utf-8"))
        sizes[gran] = len(arch_spec["system_prompt"].encode("utf-8"))

    assert sizes["fine"] <= sizes["standard"]
    assert sizes["coarse"] <= sizes["standard"]


def test_dispatch_cta_mapreduce_syllabus_map_and_budget(tmp_path: Path) -> None:
    """Verify syllabus_map and integer competency budget in cta_XX.json for mapreduce mode."""
    work_dir = tmp_path / "work_mr"
    work_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "course_id": "test_mr",
        "cta_mode": "mapreduce",
        "granularity": "standard",
        "total_pages": 24,
        "subparts": [
            {
                "subpart_id": "part_01",
                "doc": "guia_1.pdf",
                "path": "content/guia_1.pdf",
                "page_range": [1, 10],
                "total_pages": 10,
            },
            {
                "subpart_id": "part_02",
                "doc": "guia_2.pdf",
                "path": "content/guia_2.pdf",
                "page_range": [1, 14],
                "total_pages": 14,
            },
        ],
    }
    (work_dir / "pre_cta_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    res = dispatch.dispatch_cta(work_dir, mode="mapreduce", pointer=True)
    item_files = res["item_files"]
    assert len(item_files) == 2

    expected_syllabus = [
        {"subpart_id": "part_02", "doc": "guia_2.pdf", "page_range": [1, 14], "total_pages": 14},
        {"subpart_id": "part_01", "doc": "guia_1.pdf", "page_range": [1, 10], "total_pages": 10},
    ]

    for item_path_str in item_files:
        item_data = json.loads(Path(item_path_str).read_text(encoding="utf-8"))
        prompt = item_data["Prompt"]
        work_order = item_data["work_order"]

        assert "## 2.1 MAPA GLOBAL DE SUBPARTES (SYLLABUS MAP — EVITAR EXTRACCIÓN REDUNDANTE)" in prompt
        assert "`part_01`" in prompt
        assert "`part_02`" in prompt
        assert work_order["syllabus_map"] == expected_syllabus

        subpart_id = item_data["subpart_id"]
        total_p = 14 if subpart_id == "part_02" else 10
        min_c = max(2, round(0.35 * total_p))
        max_c = max(min_c + 1, round(0.65 * total_p))
        assert work_order["target_competency_range"] == [min_c, max_c]
        assert f"presupuesto slice: **{min_c}–{max_c} competencias** para {total_p} págs" in prompt
