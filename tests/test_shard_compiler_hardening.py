"""Comprehensive Test Suite for Shard Compiler Hardening (Content-to-Course v3.3).

Verifies:
1. Zero-Disk-Mutation on failed/passed compiles in compile_shard.py across all failure paths with CRLF.
2. Unified SHA-256 Intelligent Circuit Breaker (.check_attempts/compile_{norm_shard_id}.json),
   idempotent [NO-CHANGE] re-run caching, streak >= 3 halt on identical error hash,
   evolving error tolerance up to limit 10, distinct_compiles > 10 halt, volatile hash stability,
   and clean reset on PASS.
3. Modular Competency Splicing (shards/shard_fixes/<CID>.py):
   - 100% fix rescue when shard_data.py has Python SyntaxError or is missing,
   - Tuple replacement and sole fix compilation,
   - Case-insensitive & delimiter-agnostic filename normalization (Hab-03, hab_04),
   - sys.modules & linecache cache safety across repeated compiles in same process,
   - Accurate line mapping and fix file hashing.
4. Surgical Diagnostics:
   - AST warning on rf"..." / fr"..." with {{{.
   - Pure PrairieLearn @var@ template accepted without {...} braces.
   - Unrendered placeholders check (@var@, uninterpolated {key} in vars, bare {ident}).
   - Single-letter vars alongside LaTeX macros produce 0 false positives while leaks are caught.
   - TPL-VAR / TPL-COLLAPSE reporting failing seed, colliding options, constant vars, stem_variants reminder.
   - R-16 Option Length Parity reporting len(correct), avg(distractors), ratio, range [0.65x, 1.35x], distractor lengths.
   - [TPL-DRY] Traceback stripping internal engine frames and mapping to exact function/line in shard source / fix file.
"""

import hashlib
import json
import os
import re
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

from check_templates import (
    _format_dry_failure,
    check_ast_rf_triple_braces,
    check_single_template,
    check_templates_file_or_dir,
    check_unrendered_placeholders_in_instance,
    format_parity_error,
    normalize_error_string_for_hash,
)
from compile_shard import (
    ShardDataLineLocator,
    compile_shard,
    discover_fix_files,
    heal_shard_source_file,
    heal_shard_source_text,
)
from engine.invariants import check_unrendered_placeholders


def _setup_test_workspace(tmp_path: Path, shard_id: str = "shard_01", comp_ids=None):
    if comp_ids is None:
        comp_ids = ["C-01"]
    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    templates_dir = work_dir / "templates"
    shards_dir.mkdir(parents=True, exist_ok=True)
    templates_dir.mkdir(parents=True, exist_ok=True)

    manifest_payload = {
        "shards": [
            {
                "shard_id": shard_id,
                "competency_ids": comp_ids,
                "shard_data_path": str((shards_dir / f"{shard_id}_data.py").resolve().as_posix()),
                "templates_dir": str(templates_dir.resolve().as_posix()),
                "competencies": [{"id": cid, "name": f"Competency {cid}", "distractors": []} for cid in comp_ids],
            }
        ]
    }
    (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(manifest_payload), encoding="utf-8")
    return work_dir, shards_dir


class TestZeroDiskMutation:
    """Requirement 3: Zero-Disk-Mutation on compilation."""

    def test_broken_compile_does_not_modify_shard_source_on_disk(self, tmp_path: Path):
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_01", ["C-01"])
        shard_py = shards_dir / "shard_01_data.py"

        # Content with unescaped LaTeX prefixes in non-raw string and syntax errors
        original_content = (
            "# Unhealed comment\n"
            "TEMPLATES = [\n"
            "    ('C-01', 'fill_in_the_blank', 'Calcule \\rho = \\frac{a}{b}', None, None, 'Sol', 'KC', [], ('doc.pdf', 1, ''))\n"
            "]\n"
        )
        shard_py.write_text(original_content, encoding="utf-8")

        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert not success

        # Verify disk file is 100% byte-for-byte identical
        disk_content = shard_py.read_text(encoding="utf-8")
        assert disk_content == original_content

    def test_successful_compile_leaves_shard_source_untouched_on_disk(self, tmp_path: Path):
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_01", ["C-01"])
        shard_py = shards_dir / "shard_01_data.py"

        original_code = (
            "import random\n"
            "def gen_c01(rng):\n"
            "    v = rng.randint(10, 50)\n"
            "    return {'vars': {'v': v}, 'correct': str(v), 'distractors': []}\n"
            "def ver_c01(res):\n"
            "    return True\n"
            "TEMPLATES = [\n"
            "    ('C-01', 'fill_in_the_blank', 'Stem {v}', gen_c01, ver_c01, 'Sol {v}', 'KC', [], ('doc.pdf', 1, ''))\n"
            "]\n"
        )
        shard_py.write_text(original_code, encoding="utf-8")

        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert success, f"Expected clean pass, got: {errors}"

        # Original source on disk remains untouched
        disk_content = shard_py.read_text(encoding="utf-8")
        assert disk_content == original_code

    def test_zero_disk_mutation_across_all_five_failure_paths_with_crlf(self, tmp_path: Path):
        """Adversarial check: byte-for-byte SHA256 identity across 5 failure paths with CRLF on Windows."""
        cases = {
            "syntax_error": (
                "TEMPLATES = [\n"
                "    ('C-01', 'fill_in_the_blank', 'Broken syntax ((\n"
            ),
            "zero_division": (
                "def gen(rng):\n"
                "    return 10 / 0\n"
                "def ver(r): return True\n"
                "TEMPLATES = [\n"
                "    ('C-01', 'fill_in_the_blank', 'Stem {v}', gen, ver, 'Sol', 'KC', [], ('doc.pdf', 1, ''))\n"
                "]\n"
            ),
            "katex_failure": (
                "import random\n"
                "def gen(rng):\n"
                "    return {'vars': {'a': 1}, 'correct': '1', 'distractors': []}\n"
                "def ver(r): return True\n"
                "TEMPLATES = [\n"
                "    ('C-01', 'fill_in_the_blank', 'Formula $ \\frac{a} $ sin cerrar', gen, ver, 'Sol', 'KC', [], ('doc.pdf', 1, ''))\n"
                "]\n"
            ),
            "r16_parity_failure": (
                "import random\n"
                "def gen(rng):\n"
                "    v = rng.randint(10, 50)\n"
                "    return {'vars': {'v': v}, 'correct': 'X', 'distractors': ['Un distractor sumamente largo y detallado que supera por mucho la longitud de la correcta ' * 3 for _ in range(6)]}\n"
                "def ver(r): return True\n"
                "TEMPLATES = [\n"
                "    ('C-01', 'multiple_choice_7_options', 'Stem {v}', gen, ver, 'Sol', 'KC', ['D1','D2','D3','D4','D5','D6'], ('doc.pdf', 1, ''))\n"
                "]\n"
            ),
            "tpl_var_collapse": (
                "def gen(rng):\n"
                "    return {'vars': {'const': 1}, 'correct': '1', 'distractors': ['2','3','4','5','6','7']}\n"
                "def ver(r): return True\n"
                "TEMPLATES = [\n"
                "    ('C-01', 'multiple_choice_7_options', 'Static stem without variations', gen, ver, 'Sol', 'KC', ['D1','D2','D3','D4','D5','D6'], ('doc.pdf', 1, ''))\n"
                "]\n"
            ),
        }

        for case_name, code_lf in cases.items():
            sub_dir = tmp_path / f"zero_disk_{case_name}"
            work_dir, shards_dir = _setup_test_workspace(sub_dir, "shard_01", ["C-01"])
            shard_py = shards_dir / "shard_01_data.py"

            # Force Windows CRLF endings
            code_crlf = code_lf.replace("\n", "\r\n")
            shard_py.write_bytes(code_crlf.encode("utf-8"))

            sha_before = hashlib.sha256(shard_py.read_bytes()).hexdigest()

            success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
            assert not success, f"Expected failure for {case_name}, but compile succeeded!"

            raw_bytes_after = shard_py.read_bytes()
            sha_after = hashlib.sha256(raw_bytes_after).hexdigest()

            # Byte-for-byte SHA256 equality guaranteed
            assert sha_before == sha_after, f"Zero-Disk-Mutation violated for {case_name}!"
            assert b"\r\n" in raw_bytes_after, f"CRLF endings corrupted for {case_name}!"


class TestUnifiedCircuitBreaker:
    """Requirement 2: Unified SHA-256 Intelligent Circuit Breaker."""

    def test_state_file_tracks_all_fields_and_idempotency(self, tmp_path: Path):
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_01", ["C-01"])
        shard_py = shards_dir / "shard_01_data.py"
        shard_py.write_text("TEMPLATES = 'broken'\n", encoding="utf-8")

        # Compile 1
        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert not success

        att_file = work_dir / ".check_attempts" / "compile_shard_01.json"
        assert att_file.is_file()
        state = json.loads(att_file.read_text(encoding="utf-8"))
        assert state["distinct_compiles"] == 1
        assert state["same_error_streak"] == 1
        assert state["last_source_sha256"] != ""
        assert state["last_err_hash"] != ""
        assert len(state["last_errors"]) > 0

        # Compile 2: Identical source -> Idempotent [NO-CHANGE]
        success2, errors2 = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert not success2
        assert any("[NO-CHANGE" in e for e in errors2)

        # Counter and streak do NOT increment on NO-CHANGE
        state2 = json.loads(att_file.read_text(encoding="utf-8"))
        assert state2["distinct_compiles"] == 1
        assert state2["same_error_streak"] == 1

    def test_circuit_breaker_halts_on_3_consecutive_identical_error_hashes(self, tmp_path: Path):
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_01", ["C-01"])
        shard_py = shards_dir / "shard_01_data.py"

        for attempt in range(1, 4):
            # Modify comment to change source hash but keep exact same error
            shard_py.write_text(f"TEMPLATES = 'broken'  # distinct try {attempt}\n", encoding="utf-8")
            success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
            assert not success
            if attempt == 3:
                assert any("STOP, send_message the Director" in e for e in errors)
                att_file = work_dir / ".check_attempts" / "compile_shard_01.json"
                state = json.loads(att_file.read_text(encoding="utf-8"))
                assert state["same_error_streak"] >= 3

    def test_evolving_errors_do_not_halt_at_3_and_proceed_towards_10(self, tmp_path: Path):
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_01", ["C-01"])
        shard_py = shards_dir / "shard_01_data.py"

        # Run 4 distinct compiles with DIFFERENT errors
        error_sources = [
            "TEMPLATES = 'error_1'\n",
            "TEMPLATES = [1, 2, 3]\n",
            "TEMPLATES = [('C-01',)]\n",
            "TEMPLATES = [('C-01', 'fill_in_the_blank', 'Stem', None)]\n",
        ]

        for idx, src in enumerate(error_sources, start=1):
            shard_py.write_text(src, encoding="utf-8")
            success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
            assert not success
            # Should NOT trigger premature circuit breaker halt at attempt 3 or 4 because errors evolve!
            assert not any("STOP, send_message the Director" in e for e in errors)

        att_file = work_dir / ".check_attempts" / "compile_shard_01.json"
        state = json.loads(att_file.read_text(encoding="utf-8"))
        assert state["distinct_compiles"] == 4
        assert state["same_error_streak"] == 1  # Streak reset due to evolving errors!

    def test_halt_at_distinct_compiles_limit_10(self, tmp_path: Path):
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_01", ["C-01"])
        shard_py = shards_dir / "shard_01_data.py"
        att_dir = work_dir / ".check_attempts"
        att_dir.mkdir(parents=True, exist_ok=True)
        att_file = att_dir / "compile_shard_01.json"

        # Seed state at distinct_compiles = 10
        att_file.write_text(json.dumps({
            "distinct_compiles": 10,
            "same_error_streak": 1,
            "last_source_sha256": "old_hash",
            "last_err_hash": "old_err",
            "last_errors": ["Previous error"],
        }), encoding="utf-8")

        shard_py.write_text("TEMPLATES = 'brand_new_code'\n", encoding="utf-8")
        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert not success
        # 11th distinct compile must trigger terminal halt
        assert any("STOP, send_message the Director" in e for e in errors)
        assert any("Límite de 10 compilaciones distintas" in e for e in errors)

    def test_circuit_breaker_hash_stability_across_volatile_elements(self):
        """Adversarial check: circuit breaker err_hash is invariant to random module UUIDs, timestamps, temp paths, and CRLF."""
        err_run1 = (
            "[-] Error en c2c_shard_mod_shard_01_a1b2c3\r\n"
            "    File \"C:\\Users\\test\\AppData\\Local\\Temp\\tmp123\\shard_01_data.py\", line 15\n"
            "    Timestamp: 2026-10-24T10:15:30.123456Z at 0x7f8b9c0d1e2f\n"
            "    TypeError: unsupported operand type(s) for +: 'int' and 'str'\n"
        )

        err_run2 = (
            "[-] Error en c2c_shard_mod_shard_01_f9e8d7\n"
            "    File \"/home/user/.check_attempts/_staged/shard_01_data.py\", line 15\n"
            "    Timestamp: 2026-10-24 12:45:00 at 0x1a2b3c4d5e6f\n"
            "    TypeError: unsupported operand type(s) for +: 'int' and 'str'\n"
        )

        norm1 = normalize_error_string_for_hash(err_run1)
        norm2 = normalize_error_string_for_hash(err_run2)

        hash1 = hashlib.sha256(norm1.encode("utf-8")).hexdigest()
        hash2 = hashlib.sha256(norm2.encode("utf-8")).hexdigest()

        assert hash1 == hash2, f"Error hashes diverged across volatile elements!\nNorm1: {norm1}\nNorm2: {norm2}"


class TestModularCompetencySplicing:
    """Requirement 4: Modular Competency Splicing (<work_dir>/shards/shard_fixes/<CID>.py)."""

    def test_splicing_replaces_competency_tuples(self, tmp_path: Path):
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_01", ["C-01", "C-02"])
        shard_py = shards_dir / "shard_01_data.py"

        # Shard has valid C-01 but broken C-02
        shard_code = (
            "import random\n"
            "def gen_c01(rng):\n"
            "    v = rng.randint(10, 50)\n"
            "    return {'vars': {'v': v}, 'correct': str(v), 'distractors': []}\n"
            "def ver_c01(r): return True\n"
            "TEMPLATES = [\n"
            "    ('C-01', 'fill_in_the_blank', 'Stem 1 {v}', gen_c01, ver_c01, 'Sol 1 {v}', 'KC', [], ('doc.pdf', 1, '')),\n"
            "    ('C-02', 'fill_in_the_blank', 'Broken C02', None, None, 'Sol', 'KC', [], ('doc.pdf', 1, '')),\n"
            "]\n"
        )
        shard_py.write_text(shard_code, encoding="utf-8")

        # Author writes modular fix for C-02 in shards/shard_fixes/C-02.py
        fixes_dir = shards_dir / "shard_fixes"
        fixes_dir.mkdir(parents=True, exist_ok=True)
        fix_c02 = fixes_dir / "C-02.py"
        fix_code = (
            "import random\n"
            "def gen_c02(rng):\n"
            "    w = rng.randint(100, 200)\n"
            "    return {'vars': {'w': w}, 'correct': str(w), 'distractors': []}\n"
            "def ver_c02(r): return True\n"
            "TEMPLATES = [\n"
            "    ('C-02', 'fill_in_the_blank', 'Fixed Stem 2 {w}', gen_c02, ver_c02, 'Sol 2 {w}', 'KC', [], ('doc.pdf', 2, '')),\n"
            "]\n"
        )
        fix_c02.write_text(fix_code, encoding="utf-8")

        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert success, f"Expected successful splice, got errors: {errors}"

        # Verify compiled templates
        tpl_c02 = json.loads((work_dir / "templates" / "C-02.json").read_text(encoding="utf-8"))
        assert "Fixed Stem 2 {w}" in tpl_c02.get("stem", "")
        assert tpl_c02.get("source_file") == "C-02.py"

    def test_splice_error_lines_map_to_shard_fixes_file(self, tmp_path: Path):
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_01", ["C-01"])
        shard_py = shards_dir / "shard_01_data.py"
        shard_py.write_text("TEMPLATES = []\n", encoding="utf-8")

        fixes_dir = shards_dir / "shard_fixes"
        fixes_dir.mkdir(parents=True, exist_ok=True)
        fix_c01 = fixes_dir / "C-01.py"
        # Tuple with only 3 elements in fix file (requires 9)
        fix_c01.write_text("TEMPLATES = [('C-01', 'fill_in_the_blank', 'Stem')]\n", encoding="utf-8")

        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert not success
        err_str = "\n".join(errors)
        assert "C-01.py" in err_str
        assert "Líneas 1..1 en C-01.py" in err_str

    def test_circuit_breaker_hash_includes_fix_file(self, tmp_path: Path):
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_01", ["C-01"])
        shard_py = shards_dir / "shard_01_data.py"
        shard_py.write_text("TEMPLATES = []\n", encoding="utf-8")

        fixes_dir = shards_dir / "shard_fixes"
        fixes_dir.mkdir(parents=True, exist_ok=True)
        fix_c01 = fixes_dir / "C-01.py"
        fix_c01.write_text("TEMPLATES = [('C-01', 'broken 1')]\n", encoding="utf-8")

        # Compile 1
        compile_shard(work_dir, shard_id="shard_01", strict=False)
        att_file = work_dir / ".check_attempts" / "compile_shard_01.json"
        state1 = json.loads(att_file.read_text(encoding="utf-8"))

        # Modify fix file without touching shard_01_data.py
        fix_c01.write_text("TEMPLATES = [('C-01', 'broken 2')]\n", encoding="utf-8")
        compile_shard(work_dir, shard_id="shard_01", strict=False)
        state2 = json.loads(att_file.read_text(encoding="utf-8"))

        # source_sha256 must change because fix file was edited!
        assert state1["last_source_sha256"] != state2["last_source_sha256"]
        assert state2["distinct_compiles"] == 2

    def test_100_percent_fix_coverage_rescues_shard_with_broken_syntax_error(self, tmp_path: Path):
        """Adversarial check: 100% shard_fixes coverage rescues shard even if shard_XX_data.py has SyntaxError on L600."""
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_06", ["Hab-03", "Hab-04"])
        shard_py = shards_dir / "shard_06_data.py"

        # Simulate broken code with Python SyntaxError left by aborted author
        broken_code = "# Line 1\n" * 599 + "def broken_syntax_on_line_600(((\n"
        shard_py.write_text(broken_code, encoding="utf-8")

        # c2c_repair writes clean fix files for 100% of competencies in shard_fixes/
        fixes_dir = shards_dir / "shard_fixes"
        fixes_dir.mkdir(parents=True, exist_ok=True)

        fix_hab03 = (
            "import random\n"
            "def gen_h03(rng):\n"
            "    a = rng.randint(10, 50)\n"
            "    return {'vars': {'a': a}, 'correct': str(a), 'distractors': []}\n"
            "def ver_h03(r): return True\n"
            "TEMPLATES = [\n"
            "    ('Hab-03', 'fill_in_the_blank', 'Stem H03 {a}', gen_h03, ver_h03, 'Sol {a}', 'KC', [], ('doc.pdf', 1, ''))\n"
            "]\n"
        )
        (fixes_dir / "Hab-03.py").write_text(fix_hab03, encoding="utf-8")

        fix_hab04 = (
            "import random\n"
            "def gen_h04(rng):\n"
            "    b = rng.randint(100, 200)\n"
            "    return {'vars': {'b': b}, 'correct': str(b), 'distractors': []}\n"
            "def ver_h04(r): return True\n"
            "TEMPLATES = [\n"
            "    ('Hab-04', 'fill_in_the_blank', 'Stem H04 {b}', gen_h04, ver_h04, 'Sol {b}', 'KC', [], ('doc.pdf', 2, ''))\n"
            "]\n"
        )
        (fixes_dir / "Hab-04.py").write_text(fix_hab04, encoding="utf-8")

        success, errors = compile_shard(work_dir, shard_id="shard_06", strict=False)
        assert success, f"Expected successful rescue via shard_fixes, got errors: {errors}"

        # Both templates compiled cleanly
        assert (work_dir / "templates" / "Hab-03.json").is_file()
        assert (work_dir / "templates" / "Hab-04.json").is_file()

    def test_100_percent_fix_coverage_when_shard_file_is_completely_missing(self, tmp_path: Path):
        """Adversarial check: 100% shard_fixes coverage compiles cleanly even when shard_data.py does not exist."""
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_06", ["Hab-03", "Hab-04"])
        # Ensure shard_06_data.py does NOT exist
        shard_py = shards_dir / "shard_06_data.py"
        if shard_py.is_file():
            shard_py.unlink()

        fixes_dir = shards_dir / "shard_fixes"
        fixes_dir.mkdir(parents=True, exist_ok=True)

        fix_code_template = (
            "import random\n"
            "def gen(rng):\n"
            "    v = rng.randint(1, 100)\n"
            "    return {'vars': {'v': v}, 'correct': str(v), 'distractors': []}\n"
            "def ver(r): return True\n"
            "TEMPLATES = [\n"
            "    ('CID_TOKEN', 'fill_in_the_blank', 'Stem CID_TOKEN {v}', gen, ver, 'Solución {v}', 'KC', [], ('doc.pdf', 1, ''))\n"
            "]\n"
        )
        (fixes_dir / "Hab-03.py").write_text(fix_code_template.replace("CID_TOKEN", "Hab-03"), encoding="utf-8")
        (fixes_dir / "Hab-04.py").write_text(fix_code_template.replace("CID_TOKEN", "Hab-04"), encoding="utf-8")

        success, errors = compile_shard(work_dir, shard_id="shard_06", strict=False)
        assert success, f"Expected clean compile from fixes only, got errors: {errors}"
        assert (work_dir / "templates" / "Hab-03.json").is_file()
        assert (work_dir / "templates" / "Hab-04.json").is_file()

    def test_fix_filename_normalization_variants(self, tmp_path: Path):
        """Adversarial check: both hab-03.py (lowercase) and Hab_04.py (underscore) map to Hab-03 and Hab-04."""
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_06", ["Hab-03", "Hab-04"])
        fixes_dir = shards_dir / "shard_fixes"
        fixes_dir.mkdir(parents=True, exist_ok=True)

        fix_template = (
            "import random\n"
            "def gen(rng):\n"
            "    x = rng.randint(1, 99)\n"
            "    return {'vars': {'x': x}, 'correct': str(x), 'distractors': []}\n"
            "def ver(r): return True\n"
            "TEMPLATES = [\n"
            "    ('CID_TOKEN', 'fill_in_the_blank', 'Stem CID_TOKEN {x}', gen, ver, 'Solución {x}', 'KC', [], ('doc.pdf', 1, ''))\n"
            "]\n"
        )
        # hab-03.py (lowercase hyphen)
        (fixes_dir / "hab-03.py").write_text(fix_template.replace("CID_TOKEN", "Hab-03"), encoding="utf-8")
        # Hab_04.py (capital underscore)
        (fixes_dir / "Hab_04.py").write_text(fix_template.replace("CID_TOKEN", "Hab-04"), encoding="utf-8")

        success, errors = compile_shard(work_dir, shard_id="shard_06", strict=False)
        assert success, f"Expected clean normalization match, got: {errors}"
        assert (work_dir / "templates" / "Hab-03.json").is_file()
        assert (work_dir / "templates" / "Hab-04.json").is_file()

    def test_sys_modules_and_linecache_cache_safety_on_repeated_compiles(self, tmp_path: Path):
        """Adversarial check: repeated compile_shard() calls in the same process do not serve stale cached fix files."""
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_01", ["C-01"])
        fixes_dir = shards_dir / "shard_fixes"
        fixes_dir.mkdir(parents=True, exist_ok=True)
        fix_c01 = fixes_dir / "C-01.py"

        # Version 1 of fix file
        fix_v1 = (
            "import random\n"
            "def gen_c01(rng):\n"
            "    v = rng.randint(1, 10)\n"
            "    return {'vars': {'v': v}, 'correct': 'VERSION_ONE', 'distractors': []}\n"
            "def ver_c01(r): return True\n"
            "TEMPLATES = [\n"
            "    ('C-01', 'fill_in_the_blank', 'Stem V1 {v}', gen_c01, ver_c01, 'Sol V1 {v}', 'KC', [], ('doc.pdf', 1, ''))\n"
            "]\n"
        )
        fix_c01.write_text(fix_v1, encoding="utf-8")
        s1, e1 = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert s1
        t1 = json.loads((work_dir / "templates" / "C-01.json").read_text(encoding="utf-8"))
        assert "Stem V1" in t1["stem"]

        # Version 2 of fix file: modify code in place
        fix_v2 = (
            "import random\n"
            "def gen_c01(rng):\n"
            "    v = rng.randint(20, 30)\n"
            "    return {'vars': {'v': v}, 'correct': 'VERSION_TWO', 'distractors': []}\n"
            "def ver_c01(r): return True\n"
            "TEMPLATES = [\n"
            "    ('C-01', 'fill_in_the_blank', 'Stem V2 {v}', gen_c01, ver_c01, 'Sol V2 {v}', 'KC', [], ('doc.pdf', 1, ''))\n"
            "]\n"
        )
        fix_c01.write_text(fix_v2, encoding="utf-8")
        s2, e2 = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert s2
        t2 = json.loads((work_dir / "templates" / "C-01.json").read_text(encoding="utf-8"))
        assert "Stem V2" in t2["stem"], "Stale cached version served instead of fresh code!"


class TestSurgicalDiagnostics:
    """Requirement 5: Surgical Diagnostics."""

    def test_rf_triple_brace_warning(self):
        source = 'stem = rf"Formula \\frac{{{x}}}{{{y}}} con {{{val}}}"'
        warnings = check_ast_rf_triple_braces(source)
        assert len(warnings) > 0
        assert "Warning" in warnings[0]
        assert "@var@" in warnings[0]

    def test_unrendered_placeholders_detected_in_instance(self):
        instance = {
            "stem": "Resuelva @x:fmt@ dado {v}",
            "solution": "La solución para {uninterpolated_var} es directa.",
            "hints": ["Pista con {bare_token} en prosa"],
            "options": [{"content": "$x = 10$", "is_correct": True}],
        }
        vars_dict = {"v": 10, "uninterpolated_var": 5}
        errors = check_unrendered_placeholders_in_instance(instance, vars_dict)

        # Unresolved @x:fmt@
        assert any("@x:fmt@" in e for e in errors)
        # Uninterpolated variable in vars
        assert any("uninterpolated_var" in e for e in errors)
        # Bare token in prose
        assert any("bare_token" in e for e in errors)

    def test_unrendered_placeholders_does_not_flag_valid_latex(self):
        instance = {
            "stem": r"Calcule $\frac{a}{b}$ con $x_{i}$ y $\text{delta}$.",
            "solution": r"Dada la relación $\sqrt{k}$ y $\begin{matrix} 1 \end{matrix}$.",
            "hints": [r"Verifique $\mathbf{X}$ y $e^{\alpha}$."],
            "options": [{"content": r"$\frac{1}{2}$", "is_correct": True}],
        }
        errors = check_unrendered_placeholders_in_instance(instance, {})
        assert len(errors) == 0

    def test_r16_option_length_parity_diagnostic(self):
        err = type("ValidationError", (), {
            "rule_id": "R-16",
            "message": "Giveaway course length",
            "item_id": "Q-01",
        })()
        questions = {
            "Q-01": {
                "template_id": "T-C01",
                "options": [
                    {"content": "A short answer", "is_correct": True},  # 14 chars
                    {"content": "A very long detailed comprehensive distractor text 1", "is_correct": False},
                    {"content": "A very long detailed comprehensive distractor text 2", "is_correct": False},
                ]
            }
        }
        res = format_parity_error("C-01", err, questions, item_ids=["Q-01"])
        assert "len(correct)=14" in res
        assert "avg(distractors)=" in res
        assert "rango permitido=[0.65x, 1.35x]" in res

    def test_tpl_dry_traceback_strips_internal_frames_and_maps_fix_file(self, tmp_path: Path):
        work_dir = tmp_path / "work"
        shards_dir = work_dir / "shards"
        fixes_dir = shards_dir / "shard_fixes"
        fixes_dir.mkdir(parents=True, exist_ok=True)
        fix_c01 = fixes_dir / "C-01.py"
        fix_code = (
            "# L1\n"
            "# L2\n"
            "def gen_fail(rng):\n"
            "    return 10 / 0  # ZeroDivisionError on L4\n"
        )
        fix_c01.write_text(fix_code, encoding="utf-8")

        gen_code = (
            "def generate(rng):\n"
            "    return 10 / 0\n"
        )

        report = _format_dry_failure(
            competency_id="C-01",
            tpl_id="T-C-01",
            generate_py=gen_code,
            failing_seed=100,
            shard_py=shards_dir / "shard_01_data.py",
            print_output=False,
        )

        # Internal frames from check_templates/engine stripped, maps to shard_fixes/C-01.py
        assert "shard_fixes/C-01.py" in report
        assert "check_templates.py" not in report
        assert "engine/sandbox.py" not in report

    def test_pure_prairielearn_at_var_template_accepted_without_braces(self, tmp_path: Path):
        """Adversarial check: pure @var@ PrairieLearn template with zero {...} braces passes check_templates with 0 errors.

        Also verifies negative companion: truly static stem with NEITHER {var} NOR @var@ NOR stem_variants IS rejected.
        """
        # 1. Pure @var@ template with ZERO curly brace placeholders and NO stem_variants
        template = {
            "id": "T-C01",
            "competency_id": "C-01",
            "interaction_type": "fill_in_the_blank",
            "type": "fill_in_the_blank",
            "difficulty": "medium",
            "bloom": "Apply",
            "stem": r"Calcule el valor de $\frac{@a@}{@b@}$ aplicando el teorema fundamental.",
            "stem_variants": [],  # Empty stem_variants to strictly exercise stem placeholder detection!
            "solution": r"El valor calculado es @res@ con precisión formal.",
            "hints": [
                r"Recuerde dividir @a@ entre @b@ de manera exacta.",
                r"Verifique que el denominador no sea nulo antes de calcular.",
                r"Considere el valor numérico redondeado al orden correspondiente.",
            ],
            "generate_py": (
                "import random\n"
                "def generate(rng):\n"
                "    a = rng.randint(10, 50)\n"
                "    b = rng.randint(2, 9)\n"
                "    res = round(a / b, 2)\n"
                "    return {'vars': {'a': a, 'b': b, 'res': res}, 'correct': str(res), 'distractors': []}\n"
            ),
            "cross_check_py": (
                "def verify(res):\n"
                "    return True\n"
                "\n"
                "cross_check = verify\n"
            ),
            "distractor_ids": [],
        }

        errors = check_single_template(
            template,
            competency_id="C-01",
            declared_distractor_ids=set(),
            num_dry_run_seeds=20,
        )
        # Strict zero-error assertion: pure @var@ must pass 100% cleanly
        assert errors == [], f"Expected clean pass with 0 errors on pure @var@ template, got: {errors}"

        # 2. Negative companion check: Truly static stem with NEITHER {var} NOR @var@ NOR stem_variants
        static_template = dict(template)
        static_template["stem"] = r"Calcule el valor numérico constante aplicando el teorema fundamental."
        static_errors = check_single_template(
            static_template,
            competency_id="C-01",
            declared_distractor_ids=set(),
            num_dry_run_seeds=20,
        )
        tpl_var_failures = [e for e in static_errors if "TPL-VAR" in e and "stem must contain at least one placeholder" in e]
        assert len(tpl_var_failures) > 0, "Static stem without any placeholders or variants was not rejected by TPL-VAR!"

    def test_single_letter_vars_alongside_latex_macros_not_flagged(self):
        """Adversarial check: single-letter vars alongside LaTeX macros produce 0 false positives, while real leaks are caught."""
        vars_dict = {"n": 100, "d": 4, "a": 2, "b": 5}

        # Valid mathematical text with LaTeX macros and single-letter arguments
        valid_latex = r"Calcule $\frac{a}{b}$ cuando $X_n \xrightarrow{d} X$ con $x_{n}$ y ${k}^*$."
        errs = check_unrendered_placeholders(valid_latex, "stem", variables=vars_dict)
        assert len(errs) == 0, f"False positives on valid LaTeX: {errs}"

        # Real leaked placeholders: {delta}, @delta@, and bare {n} in prose
        leaked_text = r"El error es tol <= {delta} y @delta@ con resultado {n}."
        leaked_errs = check_unrendered_placeholders(leaked_text, "stem", variables=vars_dict)
        assert len(leaked_errs) == 3, f"Expected 3 errors for leaked tokens, got: {leaked_errs}"
        assert any("{delta}" in e for e in leaked_errs)
        assert any("@delta@" in e for e in leaked_errs)
        assert any("{n}" in e for e in leaked_errs)


class TestInfiniteLoopManifestAndAutoHealHardening:
    """Regression suite for infinite-loop guard, --manifest fallback, and AST-safe f-string vars auto-heal."""

    def test_infinite_while_loop_in_generator_aborts_rapidly_with_mapped_line(self, tmp_path: Path):
        import time

        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_12", ["C-02"])
        shard_py = shards_dir / "shard_12_data.py"
        code = (
            "def gen_c02_frontera(rng):\n"
            "    k = rng.randint(2, 3)\n"
            "    d1, d2, d6 = 1, k * 5, 2 * 5\n"
            "    while len({0, d1, d2, d6}) < 4:\n"
            "        d1 += 1\n"
            "    return {'vars': {'d1': d1}, 'correct': str(d1), 'distractors': []}\n"
            "def ver_c02(res):\n"
            "    return True\n"
            "TEMPLATES = [\n"
            "    ('C-02', 'fill_in_the_blank', 'Stem @d1@', gen_c02_frontera, ver_c02, 'Sol @d1@', 'KC', [], ('doc.pdf', 1, ''))\n"
            "]\n"
        )
        shard_py.write_text(code, encoding="utf-8")

        t0 = time.perf_counter()
        success, errors = compile_shard(work_dir, shard_id="shard_12", strict=False, seeds=20)
        elapsed = time.perf_counter() - t0

        assert not success
        assert elapsed < 3.0, f"Infinite loop took too long to abort: {elapsed:.2f}s"
        joined = "\n".join(errors)
        assert "TPL-DRY" in joined or "SandboxTimeoutError" in joined

    def test_compile_shard_resolves_pre_shard_manifest_when_passed_pre_cta_manifest(self, tmp_path: Path):
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_01", ["C-01"])
        pre_cta = work_dir / "pre_cta_manifest.json"
        pre_cta.write_text(json.dumps({"course_id": "test", "documents": [{"name": "doc.pdf"}]}), encoding="utf-8")

        shard_py = shards_dir / "shard_01_data.py"
        shard_py.write_text(
            "def gen_c01(rng):\n"
            "    v = rng.randint(10, 500)\n"
            "    return {'vars': {'v': v}, 'correct': str(v), 'distractors': []}\n"
            "def ver_c01(res): return True\n"
            "TEMPLATES = [\n"
            "    ('C-01', 'fill_in_the_blank', 'Calcule @v@', gen_c01, ver_c01, 'Sol @v@', 'KC', [], ('doc.pdf', 1, ''))\n"
            "]\n",
            encoding="utf-8",
        )

        success, errors = compile_shard(
            work_dir,
            shard_id="shard_01",
            strict=False,
            manifest_path=pre_cta,
        )
        assert success, f"Expected --manifest pre_cta_manifest.json to fall back to pre_shard_manifest.json, got: {errors}"

    def test_auto_heal_vars_export_preserves_fstring_format_specifiers_in_dict_var(self, tmp_path: Path):
        work_dir, shards_dir = _setup_test_workspace(tmp_path, "shard_08", ["Hab-08"])
        shard_py = shards_dir / "shard_08_data.py"
        shard_py.write_text(
            "def gen_hab08(rng):\n"
            "    n = rng.randint(20, 200) * 10\n"
            "    b = rng.randint(15, 95) / 10.0\n"
            "    g = rng.randint(20, 75) / 100.0\n"
            "    extra = rng.randint(1, 9)\n"
            "    ans = f'{(b / (1.0 - g)) / n:.4f}'\n"
            "    v = {\n"
            "        'n': n,\n"
            "        'b': f'{b:.1f}',\n"
            "        'g': f'{g:.2f}',\n"
            "        'ans': ans,\n"
            "    }\n"
            "    return {'vars': v, 'correct': ans, 'distractors': []}\n"
            "def ver_hab08(res): return True\n"
            "TEMPLATES = [\n"
            "    ('Hab-08', 'fill_in_the_blank', r'Con $n=@n@$, $\\hat{\\beta}=@b@$, $\\hat{\\gamma}=@g@$ y ajuste {extra}:', gen_hab08, ver_hab08, r'Sol @ans@ ({extra})', 'KC', [], ('doc.pdf', 1, ''))\n"
            "]\n",
            encoding="utf-8",
        )

        success, errors = compile_shard(work_dir, shard_id="shard_08", strict=False, seeds=30)
        assert success, f"f-string format specifier inside dict variable was corrupted by auto-heal: {errors}"

