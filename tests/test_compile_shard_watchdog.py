"""Automated test suite verifying the compilation watchdog timer, pinpoint diagnostics, and Windows I/O resilience.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path
import pytest

repo_root = Path(__file__).resolve().parents[1]
c2c_dir = repo_root / ".agents" / "skills" / "content-to-course"
if str(c2c_dir) not in sys.path:
    sys.path.insert(0, str(c2c_dir))

from compile_shard import EvaluationContext, _CompilationWatchdog
from run import wait_for_file_resilient


def test_evaluation_context_thread_safety_and_tracking():
    """Verify EvaluationContext correctly tracks active execution context."""
    EvaluationContext.reset(shard_id="shard_42")
    ctx = EvaluationContext.get()
    assert ctx["shard_id"] == "shard_42"
    assert ctx["template_id"] == "unknown"

    EvaluationContext.set(template_id="T-C-23-04", gen_fn="_gen_c23", archetype=4, seed=14)
    ctx2 = EvaluationContext.get()
    assert ctx2["shard_id"] == "shard_42"
    assert ctx2["template_id"] == "T-C-23-04"
    assert ctx2["gen_fn"] == "_gen_c23"
    assert ctx2["archetype"] == 4
    assert ctx2["seed"] == 14


def test_wait_for_file_resilient_delayed_appearance(tmp_path: Path):
    """Verify wait_for_file_resilient waits for delayed NTFS buffer flush without failing."""
    test_file = tmp_path / "delayed_artifact.json"
    assert not test_file.exists()

    def _write_delayed():
        time.sleep(0.3)
        test_file.write_text(json.dumps({"status": "flushed"}), encoding="utf-8")

    writer_t = threading.Thread(target=_write_delayed)
    writer_t.start()

    resolved = wait_for_file_resilient(test_file, timeout=2.0, initial_delay=0.1)
    writer_t.join()

    assert resolved.is_file()
    assert json.loads(resolved.read_text(encoding="utf-8"))["status"] == "flushed"


def test_wait_for_file_resilient_missing_path_clean_timeout(tmp_path: Path):
    """Verify wait_for_file_resilient returns path after timeout when file never appears."""
    missing = tmp_path / "never_exists.json"
    t0 = time.time()
    resolved = wait_for_file_resilient(missing, timeout=0.3, initial_delay=0.05)
    elapsed = time.time() - t0
    assert not resolved.exists()
    assert elapsed >= 0.25


def test_watchdog_subprocess_pinpoint_on_infinite_loop(tmp_path: Path):
    """Verify compile_shard.py watchdog halts with exit code 1 and pinpoint diagnostic on hanging generator."""
    work_dir = tmp_path / "work"
    shards_dir = work_dir / "shards"
    templates_dir = work_dir / "templates"
    shards_dir.mkdir(parents=True, exist_ok=True)
    templates_dir.mkdir(parents=True, exist_ok=True)

    # Pre-shard manifest required by compile_shard
    manifest = {
        "total_competencies": 1,
        "total_shards": 1,
        "shards": [
            {
                "shard_id": "shard_99",
                "shard_index": 0,
                "competency_ids": ["C-99"],
                "competencies": [{"id": "C-99", "name": "Concepto 99", "type": "concept", "distractors": []}],
                "shard_data_path": str((shards_dir / "shard_99_data.py").resolve().as_posix()),
                "templates_dir": str(templates_dir.resolve().as_posix()),
            }
        ]
    }
    (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    # Shard code containing an infinite loop in the generator
    hanging_shard_code = '''
def _gen_hanging(rng, arch=1):
    for _ in iter(int, 1):
        pass
    return {"vars": {"ans": 1}, "correct": "1"}

def ver_hanging(c, v):
    return abs(float(c) - float(v.get("ans", 0))) < 1e-3

TEMPLATES = [
    ("T-C-99-01", "C-99", "multiple_choice_7_options", _gen_hanging, ver_hanging, ("easy", "Remember"), ["stem 1", "stem 2", "stem 3"], ["hint 1234567890123456789012345", "hint 2234567890123456789012345", "hint 3234567890123456789012345"], "sol"),
]
'''
    shard_file = shards_dir / "shard_99_data.py"
    shard_file.write_text(hanging_shard_code, encoding="utf-8")

    compile_script = c2c_dir / "compile_shard.py"
    cmd = [
        sys.executable,
        "-u",
        str(compile_script),
        "--input", str(shard_file),
        "--work", str(work_dir),
        "--shard", "shard_99",
        "--watchdog-timeout", "1.5",
    ]

    t0 = time.time()
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
    elapsed = time.time() - t0

    # Must exit with non-zero code (exit code 1)
    assert proc.returncode != 0, f"Expected non-zero exit code but got {proc.returncode}. Output: {proc.stdout}"

    # Must terminate in approximately the watchdog timeout budget (< 8s under heavy parallel load), not 10s timeout or hanging indefinitely
    assert elapsed < 8.0, f"Compilation took too long to abort: {elapsed:.2f}s"

    combined_output = proc.stdout + "\n" + proc.stderr
    # Must emit surgical pinpoint diagnostic
    assert "[-] CRITICAL ERROR: [TIMEOUT_INFINITE_LOOP]" in combined_output or "FAIL: [TIMEOUT_INFINITE_LOOP]" in combined_output
    assert "shard_99" in combined_output
