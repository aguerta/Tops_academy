"""Comprehensive Unit Tests for Shard Compiler, Diagnostics & Circuit Breakers (Stream B).

Covers:
1. Graceful Missing-File Error Handling:
   - A .py path input that does not exist returns a clear error and never calls mkdir.
   - Auto-infers shard_id and work_dir from path.
2. Bounded Compilation [COMPILE n/6]:
   - Tracks compilation attempts per shard in work/.check_attempts/.
   - Prints [COMPILE n/6] on each invocation.
   - Emits terminal STOP at limit: "STOP, send_message the Director".
   - Clears attempt tracking on clean pass.
3. Dry-Run Diagnostics (_format_dry_failure):
   - Prints first failing seed, parameters, type(exc).__name__: str(exc),
     and last 3 traceback frames mapped to shard_XX_data.py source lines.
4. Stateful SHA-256 Circuit Breaker:
   - Tracks per-competency state {attempts, last_hash, halted}.
   - Same-hash repeat failures trigger terminal STOP: "STOP, send_message the Director".
   - Changed source hash re-evaluates and resets halt.
   - Clean pass clears the halt (unlinks attempt file).
5. Adaptive Shard Sizing in plan_shards.py:
   - comps_per_shard = clamp(ceil(N / 8), 2, 6) with up to 8 concurrent authors.
"""

import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

import pytest

# Ensure skills root is in sys.path
_skill_root = Path(__file__).resolve().parents[1] / ".agents" / "skills" / "content-to-course"
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

from check_templates import _format_dry_failure, check_templates_file_or_dir
from compile_shard import compile_shard, ShardDataLineLocator
from plan_shards import determine_shard_count


class TestMissingFileHandling:
    """Tests that missing .py file inputs fail gracefully without creating directories."""

    def test_missing_py_file_never_creates_directory(self, tmp_path: Path):
        """Calling compile_shard with a non-existent .py file must NOT create it as a directory."""
        work_dir = tmp_path / "work"
        shards_dir = work_dir / "shards"
        shards_dir.mkdir(parents=True, exist_ok=True)
        missing_file = shards_dir / "shard_03_data.py"

        assert not missing_file.exists()

        success, errors = compile_shard(missing_file)
        assert not success
        assert len(errors) > 0
        assert any("No existe el archivo de datos" in e for e in errors)

        # CRITICAL: Verify the missing file path was NOT created as a directory
        assert not missing_file.exists(), f"BUG DETECTED: {missing_file} was created as a directory!"

    def test_infer_shard_id_and_work_dir_from_missing_path(self, tmp_path: Path):
        """Verify shard_id and work_p are inferred properly even when the file is missing."""
        work_dir = tmp_path / "test_course" / "work"
        target_path = work_dir / "shards" / "shard_07_data.py"

        success, errors = compile_shard(target_path)
        assert not success
        assert "shard_07_data.py" in errors[0]
        assert not target_path.exists()


class TestBoundedCompilation:
    """Tests bounded compilation counter [COMPILE n/6] and terminal STOP."""

    def _setup_minimal_workspace(self, tmp_path: Path, shard_id: str = "shard_01"):
        work_dir = tmp_path / "work"
        shards_dir = work_dir / "shards"
        templates_dir = work_dir / "templates"
        shards_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)

        # Write pre_shard_manifest.json
        manifest_payload = {
            "total_competencies": 1,
            "total_shards": 1,
            "shards": [
                {
                    "shard_id": shard_id,
                    "shard_index": 0,
                    "competency_ids": ["C-01"],
                    "competencies": [{"id": "C-01", "name": "Concepto 1", "type": "concept", "distractors": []}],
                    "shard_data_path": str((shards_dir / f"{shard_id}_data.py").resolve().as_posix()),
                    "templates_dir": str(templates_dir.resolve().as_posix()),
                }
            ],
        }
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(manifest_payload), encoding="utf-8")
        return work_dir, shards_dir

    def test_compile_counter_increments_and_halts_at_limit(self, tmp_path: Path, capsys):
        """Verify unified circuit breaker increments distinct compiles, handles [NO-CHANGE], and halts on 3 repeat errors."""
        work_dir, shards_dir = self._setup_minimal_workspace(tmp_path, "shard_01")
        shard_py = shards_dir / "shard_01_data.py"

        # Create broken shard data that fails syntax/parity
        shard_py.write_text("TEMPLATES = 'broken'\n", encoding="utf-8")

        # Attempt 1: First distinct compile
        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert not success
        captured = capsys.readouterr()
        assert "[COMPILE 1/10]" in captured.out or "[COMPILE 1/10]" in captured.err

        # Attempt 2: Re-run with UNCHANGED code -> Idempotent [NO-CHANGE]
        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert not success
        assert any("[NO-CHANGE" in e for e in errors)
        captured = capsys.readouterr()
        # Does NOT increment to [COMPILE 2/10]
        assert "[COMPILE 2/10]" not in captured.out

        # Distinct Attempt 2: modify code slightly but produce same error
        shard_py.write_text("TEMPLATES = 'broken'  # distinct try 2\n", encoding="utf-8")
        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert not success
        captured = capsys.readouterr()
        assert "[COMPILE 2/10]" in captured.out or "[COMPILE 2/10]" in captured.err

        # Distinct Attempt 3: modify code slightly, 3rd consecutive identical error -> HALT!
        shard_py.write_text("TEMPLATES = 'broken'  # distinct try 3\n", encoding="utf-8")
        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert not success
        assert any("STOP, send_message the Director" in e for e in errors)

    def test_compile_counter_resets_on_success(self, tmp_path: Path):
        """Verify successful compilation removes the attempt tracker file."""
        work_dir, shards_dir = self._setup_minimal_workspace(tmp_path, "shard_01")
        att_dir = work_dir / ".check_attempts"
        att_dir.mkdir(parents=True, exist_ok=True)
        compile_att_file = att_dir / "compile_shard_01.json"
        compile_att_file.write_text(json.dumps({"count": 3}), encoding="utf-8")

        # Create a valid shard with 1 template
        shard_py = shards_dir / "shard_01_data.py"
        shard_code = (
            "import random\n"
            "def gen_c01(rng):\n"
            "    v = rng.randint(10, 50)\n"
            "    return {'vars': {'v': v}, 'correct': str(v), 'distractors': []}\n"
            "def ver_c01(res):\n"
            "    return True\n"
            "TEMPLATES = [\n"
            "    ('C-01', 'fill_in_the_blank', 'Stem {v}', gen_c01, ver_c01, 'Sol {v}', 'KC', [], ('doc.pdf', 1, 'Quote'))\n"
            "]\n"
        )
        shard_py.write_text(shard_code, encoding="utf-8")

        success, errors = compile_shard(work_dir, shard_id="shard_01", strict=False)
        assert success, f"Expected success but got errors: {errors}"
        # On success, compile_att_file should be cleared
        assert not compile_att_file.exists()


class TestDryRunDiagnostics:
    """Tests for _format_dry_failure reporting seeds, parameters, exceptions, and mapped lines."""

    def test_format_dry_failure_output(self, tmp_path: Path):
        """Verify _format_dry_failure outputs failing seed, parameters, exception, and traceback."""
        shard_py = tmp_path / "shard_02_data.py"
        shard_code = (
            "# Line 1\n"
            "# Line 2\n"
            "def gen_test(rng):\n"
            "    A = rng.randint(1, 10)\n"
            "    B = 0\n"
            "    result = A / B  # Division by zero\n"
            "    return {'vars': {'A': A}, 'correct': '1', 'distractors': []}\n"
            "\n"
            "def ver_test(res):\n"
            "    return True\n"
            "\n"
            "TEMPLATES = [\n"
            "    ('C-02', 'fill_in_the_blank', 'Stem', gen_test, ver_test, 'Sol', 'KC', [], ('doc', 1, ''))\n"
            "]\n"
        )
        shard_py.write_text(shard_code, encoding="utf-8")

        gen_code = (
            "def generate(rng):\n"
            "    A = rng.randint(1, 10)\n"
            "    B = 0\n"
            "    result = A / B\n"
            "    return {'vars': {'A': A}, 'correct': '1', 'distractors': []}\n"
        )

        report = _format_dry_failure(
            competency_id="C-02",
            tpl_id="T-C-02",
            generate_py=gen_code,
            failing_seed=42,
            shard_py=shard_py,
            print_output=False,
        )

        assert "[-] [TPL-DRY: FALLO EN EJECUCIÓN DRY-RUN]" in report
        assert "Primer seed fallido: 42" in report
        assert "Parámetros:" in report
        assert "ZeroDivisionError: division by zero" in report
        assert "shard_02_data.py" in report
        assert "Traceback" in report


class TestStatefulSHA256CircuitBreaker:
    """Tests for stateful SHA-256 circuit breaker {attempts, last_hash, halted}."""

    def test_stateful_circuit_breaker_cycle(self, tmp_path: Path):
        """Verify circuit breaker tracks hash, halts on repeat failures, and clears on change or pass."""
        templates_dir = tmp_path / "templates"
        attempts_dir = tmp_path / ".check_attempts"
        templates_dir.mkdir(parents=True, exist_ok=True)
        attempts_dir.mkdir(parents=True, exist_ok=True)

        tpl_file = templates_dir / "C-01.json"

        # Broken template 1 (fails AST/schema or dry-run)
        broken_tpl_1 = {
            "id": "T-C01-01",
            "competency_id": "C-01",
            "interaction_type": "fill_in_the_blank",
            "difficulty": "medium",
            "bloom": "Understand",
            "stem": "Stem",
            "generate_py": "def generate(rng):\n    x = 1 / 0\n    return {'vars': {}, 'correct': '1'}\n",
            "cross_check_py": "def verify(r):\n    return True\n",
            "solution": "Sol",
            "distractor_ids": [],
            "hints": ["H1", "H2", "H3"],
        }
        tpl_file.write_text(json.dumps(broken_tpl_1), encoding="utf-8")

        # 1st run: fails, attempts=1
        clean, errs = check_templates_file_or_dir(
            [tpl_file],
            attempts_dir=attempts_dir,
            shard_id="shard_01",
            strict=False,
            auto_fix=False,
        )
        assert not clean
        att_file = attempts_dir / "shard_01_C-01.json"
        assert att_file.is_file()
        att_data = json.loads(att_file.read_text(encoding="utf-8"))
        assert att_data["attempts"] == 1
        assert att_data["last_hash"] is not None
        assert not att_data["halted"]

        # 2nd run with SAME hash: attempts=2
        clean, errs = check_templates_file_or_dir(
            [tpl_file],
            attempts_dir=attempts_dir,
            shard_id="shard_01",
            strict=False,
            auto_fix=False,
        )
        assert not clean
        att_data = json.loads(att_file.read_text(encoding="utf-8"))
        assert att_data["attempts"] == 2
        assert not att_data["halted"]

        # 3rd run with SAME hash: attempts=3 -> HALTED with terminal STOP
        clean, errs = check_templates_file_or_dir(
            [tpl_file],
            attempts_dir=attempts_dir,
            shard_id="shard_01",
            strict=False,
            auto_fix=False,
        )
        assert not clean
        att_data = json.loads(att_file.read_text(encoding="utf-8"))
        assert att_data["attempts"] == 3
        assert att_data["halted"]
        assert any("STOP, send_message the Director" in e for e in errs)

        # 4th run: AUTHOR MODIFIES CODE (different hash): re-evaluates and resets halt!
        broken_tpl_2 = dict(broken_tpl_1)
        broken_tpl_2["stem"] = "Modified stem for C-01"
        tpl_file.write_text(json.dumps(broken_tpl_2), encoding="utf-8")

        clean, errs = check_templates_file_or_dir(
            [tpl_file],
            attempts_dir=attempts_dir,
            shard_id="shard_01",
            strict=False,
            auto_fix=False,
        )
        assert not clean
        att_data = json.loads(att_file.read_text(encoding="utf-8"))
        assert att_data["attempts"] == 1  # Reset to 1 on code change!
        assert not att_data["halted"]     # Halt cleared!

        # 5th run: AUTHOR FIXES THE CODE (clean pass): clears attempt file!
        fixed_tpl = {
            "id": "T-C01-01",
            "competency_id": "C-01",
            "interaction_type": "fill_in_the_blank",
            "difficulty": "medium",
            "bloom": "Understand",
            "stem": "Calcule el valor de {x} dado el enunciado formal.",
            "generate_py": (
                "def generate(rng):\n"
                "    x = rng.randint(10, 100)\n"
                "    return {'vars': {'x': x}, 'correct': str(x), 'distractors': []}\n"
            ),
            "cross_check_py": "def verify(r):\n    return True\n",
            "solution": "La solución detallada para el valor de {x} es directa.",
            "distractor_ids": [],
            "hints": ["H1 contextualizada", "H2 procedimiento", "H3 verificacion"],
        }
        tpl_file.write_text(json.dumps(fixed_tpl), encoding="utf-8")

        clean, errs = check_templates_file_or_dir(
            [tpl_file],
            attempts_dir=attempts_dir,
            shard_id="shard_01",
            strict=False,
            auto_fix=False,
        )
        assert clean, f"Expected clean pass, got: {errs}"
        assert not att_file.exists(), "Pass must clear the halt and remove attempt file!"



class TestAdaptiveShardSizing:
    """Tests for adaptive shard sizing in plan_shards.py: clamp(ceil(N / 8), 2, DEFAULT_COMPS_PER_SHARD)."""

    def test_determine_shard_count_adaptive(self):
        """Verify clamp(ceil(N / 8), 2, 2) in Case 2B across various course sizes."""
        # N = 1 -> 1 shard
        assert determine_shard_count(1) == 1

        # N = 8: ceil(8/8) = 1 -> clamped to 2 -> ceil(8/2) = 4 shards
        assert determine_shard_count(8) == 4

        # N = 16: ceil(16/8) = 2 -> 2/shard -> ceil(16/2) = 8 shards
        assert determine_shard_count(16) == 8

        # N = 24: under Case 2B (max 2/shard) -> ceil(24/2) = 12 shards
        assert determine_shard_count(24) == 12

        # N = 32: under Case 2B (max 2/shard) -> ceil(32/2) = 16 shards
        assert determine_shard_count(32) == 16

        # N = 43: under Case 2B (max 2/shard) -> ceil(43/2) = 22 shards
        assert determine_shard_count(43) == 22

        # N = 60: under Case 2B (max 2/shard) -> ceil(60/2) = 30 shards
        assert determine_shard_count(60) == 30

        # Parametric override: Case 2A (max_comps_per_shard=3)
        assert determine_shard_count(24, max_comps_per_shard=3) == 8

        # Parametric override: legacy v3.22 (max_comps_per_shard=6)
        assert determine_shard_count(43, max_comps_per_shard=6) == 8
        assert determine_shard_count(60, max_comps_per_shard=6) == 10

    def test_requested_k_overrides_adaptive(self):
        """Explicit requested_k takes precedence."""
        assert determine_shard_count(24, requested_k=4) == 4

    def test_max_comps_per_shard_overrides_adaptive(self):
        """Explicit max_comps_per_shard takes precedence."""
        assert determine_shard_count(24, max_comps_per_shard=2) == 12
