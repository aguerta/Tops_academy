"""Regression & Hardening Tests for C2C Stream 1B (Dispatch Absolute POSIX Paths, Deterministic line_range & Repair Slices)."""

from __future__ import annotations

import json
import re
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from dispatch import (  # noqa: E402
    _locate_competency_line_range,
    dispatch_authors,
    dispatch_cta,
    dispatch_repair,
)


def _is_abs_posix(path_str: str) -> bool:
    return "\\" not in path_str and (path_str.startswith("/") or bool(re.match(r"^[A-Za-z]:/", path_str)))


class TestC2CHardeningDispatch(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="c2c_h1b_")
        self.work_dir = Path(self.test_dir) / "work"
        self.work_dir.mkdir(parents=True, exist_ok=True)
        (self.work_dir / "pre_cta_manifest.json").write_text(
            json.dumps({
                "course_id": "hardening_test",
                "cta_mode": "direct",
                "documents": [
                    {
                        "name": "book.pdf",
                        "path": "content/book.pdf",
                        "total_pages": 20,
                        "valid_page_range": [1, 20],
                    }
                ],
            }),
            encoding="utf-8",
        )
        (self.work_dir / "cta.json").write_text(
            json.dumps({
                "course_id": "hardening_test",
                "competencies": [
                    {
                        "id": "C-01",
                        "type": "knowledge",
                        "name": "Competencia Uno",
                        "description_latex": r"Definición $x = 1$",
                        "evidence": [{"doc": "book.pdf", "page": 1}],
                        "distractors": [
                            {"id": f"D-01-{i:02d}", "name": f"D{i}", "wrong_belief": f"WB {i}"}
                            for i in range(1, 7)
                        ],
                    },
                    {
                        "id": "Hab-05",
                        "type": "skill",
                        "name": "Habilidad Cinco",
                        "description_latex": r"Calcular $y = 2x$",
                        "evidence": [{"doc": "book.pdf", "page": 5}],
                        "distractors": [
                            {"id": f"D-05-{i:02d}", "name": f"D{i}", "wrong_belief": f"WB {i}"}
                            for i in range(1, 7)
                        ],
                    },
                ],
            }),
            encoding="utf-8",
        )
        shards_dir = self.work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        (shards_dir / "pre_shard_manifest.json").write_text(
            json.dumps({
                "shards": [
                    {"shard_id": "shard_01", "competency_ids": ["C-01", "Hab-05"]},
                ]
            }),
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_pointer_prompts_emit_absolute_posix_paths_and_fit_650_bytes(self) -> None:
        """CTA (direct/mapreduce), Authors, and Repairs emit absolute POSIX paths in READ/WRITE within 650 B."""
        # 1. CTA direct
        cta_dir = dispatch_cta(self.work_dir, mode="direct", pointer=True)
        p_cta_dir = cta_dir["Subagents"][0]["Prompt"]
        self.assertLessEqual(len(p_cta_dir.encode("utf-8")), 650)
        self.assertIn("compile_cta.py", p_cta_dir)
        expected_cta_py = (self.work_dir / "cta_data.py").resolve().as_posix()
        self.assertIn(f"WRITE: `{expected_cta_py}`", p_cta_dir)
        self.assertTrue(_is_abs_posix(expected_cta_py))

        # 2. CTA mapreduce with pdf slice
        slice_pdf = self.work_dir / "slices" / "part_01" / "book_p1_10.pdf"
        slice_pdf.parent.mkdir(parents=True, exist_ok=True)
        slice_pdf.write_bytes(b"%PDF-1.4")
        (self.work_dir / "pre_cta_manifest.json").write_text(
            json.dumps({
                "course_id": "hardening_test",
                "cta_mode": "mapreduce",
                "subparts": [
                    {
                        "subpart_id": "part_01",
                        "doc": "book.pdf",
                        "path": "work/slices/part_01/book_p1_10.pdf",
                        "slice_path": "work/slices/part_01/book_p1_10.pdf",
                        "page_range": [1, 10],
                        "total_pages": 10,
                    }
                ],
            }),
            encoding="utf-8",
        )
        cta_mr = dispatch_cta(self.work_dir, mode="mapreduce", pointer=True)
        p_cta_mr = cta_mr["Subagents"][0]["Prompt"]
        self.assertLessEqual(len(p_cta_mr.encode("utf-8")), 650)
        self.assertIn(f"READ: `{slice_pdf.resolve().as_posix()}`", p_cta_mr)
        expected_part_py = (self.work_dir / "cta_parts" / "part_01_data.py").resolve().as_posix()
        self.assertIn(f"WRITE: `{expected_part_py}`", p_cta_mr)
        self.assertIn(".agents/skills/content-to-course/compile_cta.py", p_cta_mr)

        # 3. Authors
        auth = dispatch_authors(self.work_dir, pointer=True)
        p_auth = auth["Subagents"][0]["Prompt"]
        self.assertLessEqual(len(p_auth.encode("utf-8")), 650)
        expected_data_md = (self.work_dir / "dispatch" / "items" / "author_01_data.md").resolve().as_posix()
        expected_shard_py = (self.work_dir / "shards" / "shard_01_data.py").resolve().as_posix()
        self.assertIn(f"READ: `{expected_data_md}`", p_auth)
        self.assertIn(f"WRITE: `{expected_shard_py}`", p_auth)
        self.assertIn(".agents/skills/content-to-course/compile_shard.py", p_auth)

        # 4. Repair (single competency)
        (self.work_dir / "judge_report.json").write_text(
            json.dumps({
                "disagreements": [
                    {"cid": "Hab-05", "item_id": "Q-05-01", "reason": "Ambiguous stem"},
                ]
            }),
            encoding="utf-8",
        )
        rep_single = dispatch_repair(self.work_dir, ids=["Hab-05"], pointer=True)
        p_rep_s = rep_single["Subagents"][0]["Prompt"]
        self.assertLessEqual(len(p_rep_s.encode("utf-8")), 650)
        expected_rep_md = (self.work_dir / "prompts" / "repair" / "repair_hab05_data.md").resolve().as_posix()
        self.assertIn(expected_rep_md, p_rep_s)
        self.assertIn(expected_shard_py, p_rep_s)
        self.assertIn(".agents/skills/content-to-course/compile_shard.py", p_rep_s)

        # 5. Repair (consolidated multi-competency)
        (self.work_dir / "judge_report.json").write_text(
            json.dumps({
                "disagreements": [
                    {"cid": "C-01", "item_id": "Q-01-01", "reason": "Bad option"},
                    {"cid": "Hab-05", "item_id": "Q-05-01", "reason": "Ambiguous stem"},
                ]
            }),
            encoding="utf-8",
        )
        rep_multi = dispatch_repair(self.work_dir, pointer=True)
        p_rep_m = rep_multi["Subagents"][0]["Prompt"]
        self.assertLessEqual(len(p_rep_m.encode("utf-8")), 650)
        expected_cons_md = (self.work_dir / "prompts" / "repair" / "repair_shard_01_data.md").resolve().as_posix()
        self.assertIn(f"READ: `{expected_cons_md}`", p_rep_m)
        self.assertIn(expected_shard_py, p_rep_m)
        self.assertIn(".agents/skills/content-to-course/compile_shard.py", p_rep_m)

    def test_locate_competency_line_range_ast_and_syntax_fallback(self) -> None:
        """_locate_competency_line_range resolves exact line_range for cid without prefix collisions (< 10 ms)."""
        shard_py = self.work_dir / "shards" / "shard_01_data.py"
        shard_py.write_text(
            "\n".join([
                "def gen_c01_01(rng):",          # L1
                "    return {'vars': {'x': 1}}",  # L2
                "",                               # L3
                "def ver_c01_01(ans, vars):",     # L4
                "    return True",                # L5
                "",                               # L6
                "def gen_c010_01(rng):",         # L7
                "    return {'vars': {'x': 10}}", # L8
                "",                               # L9
                "def gen_hab05_01(rng):",        # L10
                "    return {'vars': {'y': 2}}",  # L11
                "",                               # L12
                "TEMPLATES = [",                  # L13
                "    ('T-C-01-01', 'C-01', 'easy', gen_c01_01, ver_c01_01),",  # L14
                "    ('T-C-010-01', 'C-010', 'easy', gen_c010_01),",           # L15
                "    {'id': 'T-Hab-05-01', 'cid': 'Hab-05', 'gen': gen_hab05_01},",  # L16
                "]",                              # L17
            ]),
            encoding="utf-8",
        )

        # Warm up regex/AST cache, then verify < 5 ms under parallel xdist load
        _locate_competency_line_range(shard_py, "C-01")
        t0 = time.perf_counter()
        s_c01, e_c01 = _locate_competency_line_range(shard_py, "C-01")
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        self.assertEqual((s_c01, e_c01), (1, 14))
        self.assertLess(elapsed_ms, 5.0)

        s_hab05, e_hab05 = _locate_competency_line_range(shard_py, "Hab-05")
        self.assertEqual((s_hab05, e_hab05), (10, 16))

        # Verify SyntaxError fallback
        broken_py = self.work_dir / "shards" / "shard_02_data.py"
        broken_py.write_text(
            "\n".join([
                "def gen_hab05_01(rng):",
                "    x = ((",
                "TEMPLATES = [",
                "    {'cid': 'Hab-05'},",
                "]",
            ]),
            encoding="utf-8",
        )
        s_brk, e_brk = _locate_competency_line_range(broken_py, "Hab-05")
        self.assertEqual((s_brk, e_brk), (1, 4))

    def test_repair_slices_normalized_alias_and_populated_line_range(self) -> None:
        """dispatch_repair writes {shard_id}_{cid_norm}.json alias, populates line_range on judge disagreements, and cites exact existing path."""
        shard_py = self.work_dir / "shards" / "shard_01_data.py"
        shard_py.write_text(
            "\n".join([
                "def gen_hab05_01(rng):",
                "    return {'vars': {'y': 2}}",
                "TEMPLATES = [",
                "    {'id': 'T-Hab-05-01', 'cid': 'Hab-05', 'gen': gen_hab05_01},",
                "]",
            ]),
            encoding="utf-8",
        )
        (self.work_dir / "judge_report.json").write_text(
            json.dumps({
                "disagreements": [
                    {"cid": "Hab-05", "item_id": "Q-05-01", "reason": "Judge discrepancy"},
                ]
            }),
            encoding="utf-8",
        )

        res = dispatch_repair(self.work_dir, ids=["Hab-05"], pointer=True)
        slices_dir = self.work_dir / "dispatch" / "repair_slices"
        orig_slice = slices_dir / "shard_01_Hab-05.json"
        norm_slice = slices_dir / "shard_01_hab05.json"
        self.assertTrue(orig_slice.is_file())
        self.assertTrue(norm_slice.is_file())

        slice_data = json.loads(norm_slice.read_text(encoding="utf-8"))
        self.assertEqual(slice_data["line_range"]["start"], 1)
        self.assertEqual(slice_data["line_range"]["end"], 4)
        self.assertEqual(slice_data["line_range"]["locations_count"], 0)

        expected_slice_abs = orig_slice.resolve().as_posix()
        rep_md = (self.work_dir / "prompts" / "repair" / "repair_hab05_data.md").read_text(encoding="utf-8")
        self.assertIn(expected_slice_abs, rep_md)
        self.assertTrue(Path(expected_slice_abs).is_file())
        self.assertIn(expected_slice_abs, res["Subagents"][0]["Prompt"])


if __name__ == "__main__":
    unittest.main()
