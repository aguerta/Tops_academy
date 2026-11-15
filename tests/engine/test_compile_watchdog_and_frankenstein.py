"""Focused tests for compile_shard watchdog separation, [TPL-FRANKENSTEIN-SUM], edit_file reminder, and sandbox call_with_timeout."""

from __future__ import annotations

import json
import sys
import time
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

_skills_root = Path(__file__).resolve().parents[2] / ".agents" / "skills" / "content-to-course"
if str(_skills_root) not in sys.path:
    sys.path.insert(0, str(_skills_root))

from compile_shard import (
    EvaluationContext,
    _CompilationWatchdog,
    compile_shard,
    detect_frankenstein_sum,
)
from engine.sandbox import SandboxTimeoutError, call_with_timeout


class TestEvaluationContextAndWatchdog:
    """Verify per-seed vs global process timeout separation in _CompilationWatchdog."""

    def test_evaluation_context_set_always_updates_start_time(self):
        EvaluationContext.reset(shard_id="shard_01")
        t1 = EvaluationContext.get()["start_time"]
        time.sleep(0.03)
        EvaluationContext.set(template_id="T-01", gen_fn="_gen_01", archetype=1, seed=101)
        ctx2 = EvaluationContext.get()
        t2 = ctx2["start_time"]
        assert t2 > t1
        time.sleep(0.03)
        EvaluationContext.set(seed=102)
        t3 = EvaluationContext.get()["start_time"]
        assert t3 > t2

    def test_watchdog_global_timeout_does_not_blame_fast_seed_with_infinite_loop(self):
        """Accumulated time across fast seeds triggers global timeout, NOT [TIMEOUT_INFINITE_LOOP]."""
        wd = _CompilationWatchdog(timeout=0.55, shard_id="shard_fast_accum", seed_timeout=0.4)
        captured = StringIO()

        def _fake_exit(code):
            raise SystemExit(code)

        # Simulate fast seeds updating EvaluationContext while total_elapsed crosses 0.55s
        wd.start_time = time.time() - 0.65
        EvaluationContext.reset("shard_fast_accum")
        EvaluationContext.set(template_id="T-FAST-01", gen_fn="_gen_fast", archetype=1, seed=42)

        with patch("compile_shard.os._exit", side_effect=_fake_exit), patch.object(sys, "stderr", captured), patch.object(
            sys, "stdout", StringIO()
        ):
            with pytest.raises(SystemExit) as exc_info:
                wd._run()
        assert exc_info.value.code == 1
        out = captured.getvalue()
        assert "[TIMEOUT_GLOBAL_PROCESS]" in out
        assert "[TIMEOUT_INFINITE_LOOP]" not in out
        assert "_gen_fast" not in out

    def test_watchdog_short_budget_active_seed_emits_timeout_infinite_loop(self):
        """When global timeout < seed_timeout (e.g. --watchdog-timeout 1.5), an active seed emits [TIMEOUT_INFINITE_LOOP]."""
        wd = _CompilationWatchdog(timeout=1.5, shard_id="shard_short", seed_timeout=3.0)
        captured = StringIO()

        def _fake_exit(code):
            raise SystemExit(code)

        wd.start_time = time.time() - 1.6
        EvaluationContext.reset("shard_short")
        EvaluationContext.set(template_id="T-SHORT-01", gen_fn="_gen_short", archetype=1, seed=0)

        with patch("compile_shard.os._exit", side_effect=_fake_exit), patch.object(sys, "stderr", captured), patch.object(
            sys, "stdout", StringIO()
        ):
            with pytest.raises(SystemExit) as exc_info:
                wd._run()
        assert exc_info.value.code == 1
        out = captured.getvalue()
        assert "[TIMEOUT_INFINITE_LOOP]" in out
        assert "_gen_short" in out

    def test_watchdog_slow_seed_emits_timeout_infinite_loop_pinpoint(self):
        """A single seed exceeding seed_timeout emits [TIMEOUT_INFINITE_LOOP] blaming gen_fn and seed."""
        wd = _CompilationWatchdog(timeout=90.0, shard_id="shard_slow_seed", seed_timeout=0.4)
        captured = StringIO()

        def _fake_exit(code):
            raise SystemExit(code)

        wd.start_time = time.time() - 0.6
        EvaluationContext.reset("shard_slow_seed")
        EvaluationContext.set(template_id="T-SLOW-01", gen_fn="_gen_slow", archetype=2, seed=77)
        # Backdate seed start_time to simulate a hung seed
        with EvaluationContext._lock:
            EvaluationContext._current["start_time"] = time.time() - 0.55

        with patch("compile_shard.os._exit", side_effect=_fake_exit), patch.object(sys, "stderr", captured), patch.object(
            sys, "stdout", StringIO()
        ):
            with pytest.raises(SystemExit) as exc_info:
                wd._run()
        assert exc_info.value.code == 1
        out = captured.getvalue()
        assert "[TIMEOUT_INFINITE_LOOP]" in out
        assert "_gen_slow" in out
        assert "77" in out


class TestFrankensteinSumAndEditReminder:
    """Verify [TPL-FRANKENSTEIN-SUM] and edit_file reminder in compile_shard."""

    @pytest.mark.parametrize(
        "bad_stem",
        [
            "Calcule la suma de la probabilidad $P(X > 2)$ y la varianza $\\sigma^2$.",
            "Determine el índice compuesto sumando la cota de probabilidad y el tamaño muestral $n$.",
            "Halle la suma entre el error cuadrático medio (ECM) y el estadístico Z.",
            "Obtenga la suma de la desviación estándar y el p-valor observado.",
            "Calcule la suma del ancho del intervalo de confianza y la probabilidad de cobertura.",
        ],
    )
    def test_detect_frankenstein_sum_rejects_incompatible_units(self, bad_stem):
        result = detect_frankenstein_sum(bad_stem)
        assert result is not None, f"Expected Frankenstein sum detection for: {bad_stem}"
        assert len(result) == 2 and result[0] != result[1]

    @pytest.mark.parametrize(
        "valid_stem",
        [
            "Calcule la suma de las probabilidades $P(X=0)$ y $P(X=1)$.",
            "Determine la suma de las varianzas $\\sigma_1^2$ y $\\sigma_2^2$ de dos muestras independientes.",
            "Para un tamaño muestral $n=30$, calcule la suma de las probabilidades $P(A)$ y $P(B)$.",
            "Halle la varianza muestral $S^2$ y la desviación estándar $S$ de los datos.",
        ],
    )
    def test_detect_frankenstein_sum_allows_homogeneous_or_non_sum_stems(self, valid_stem):
        assert detect_frankenstein_sum(valid_stem) is None

    def test_compile_shard_rejects_frankenstein_sum_and_includes_edit_file_reminder(self, tmp_path: Path):
        work_dir = tmp_path / "work"
        shards_dir = work_dir / "shards"
        templates_dir = work_dir / "templates"
        shards_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)

        manifest = {
            "total_competencies": 1,
            "total_shards": 1,
            "shards": [
                {
                    "shard_id": "shard_01",
                    "shard_index": 0,
                    "competency_ids": ["C-01"],
                    "competencies": [{"id": "C-01", "name": "Concepto 01", "type": "concept", "distractors": []}],
                    "shard_data_path": str((shards_dir / "shard_01_data.py").resolve().as_posix()),
                    "templates_dir": str(templates_dir.resolve().as_posix()),
                }
            ],
        }
        (shards_dir / "pre_shard_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

        shard_code = '''
def _gen_c01(rng, arch=1):
    x = rng.randint(2, 9)
    return {"vars": {"x": x}, "correct": str(x)}

def _ver_c01(cand, v):
    return abs(float(cand) - float(v["x"])) < 1e-3

TEMPLATES = [
    (
        "T-C01-01",
        "C-01",
        "fill_in_the_blank",
        _gen_c01,
        _ver_c01,
        ("easy", "Apply"),
        [
            "Dado x=@x@, calcule la suma de la probabilidad de éxito y la varianza poblacional.",
            "Con x=@x@, halle la probabilidad de acierto del evento.",
            "Para x=@x@, determine la probabilidad solicitada.",
        ],
        [
            "Pista 1 suficientemente larga para pasar el mínimo de caracteres.",
            "Pista 2 suficientemente larga para pasar el mínimo de caracteres.",
            "Pista 3 suficientemente larga para pasar el mínimo de caracteres.",
        ],
        "Solución detallada con el valor @x@ correctamente explicado paso a paso.",
    ),
]
'''
        shard_file = shards_dir / "shard_01_data.py"
        shard_file.write_text(shard_code, encoding="utf-8")

        success, errors = compile_shard(
            work_dir_or_path=shard_file,
            shard_id="shard_01",
            strict=True,
            seeds=3,
            output_dir=templates_dir,
            min_archetypes=1,
        )
        assert not success
        joined = "\n".join(errors)
        assert "[TPL-FRANKENSTEIN-SUM]" in joined
        assert "⚠️ USA edit_file (NO uses write_file con Overwrite=True o el hook bloqueará tu turno)" in joined


class TestSandboxCallWithTimeout:
    """Verify optimized _timeout_tracer in call_with_timeout."""

    def test_call_with_timeout_returns_valid_result(self):
        def _compute(a, b):
            total = 0
            for i in range(200):
                total += (a * i + b)
            return total

        res = call_with_timeout(_compute, args=(3, 5), timeout=0.5)
        assert res == sum(3 * i + 5 for i in range(200))

    def test_call_with_timeout_aborts_infinite_loop(self):
        def _infinite():
            i = 0
            while True:
                i += 1

        with pytest.raises(SandboxTimeoutError):
            call_with_timeout(_infinite, timeout=0.15)

    def test_call_with_timeout_aborts_infinite_recursion(self):
        def _recurse(n):
            return _recurse(n + 1)

        with pytest.raises((SandboxTimeoutError, RecursionError)):
            call_with_timeout(_recurse, args=(0,), timeout=0.15)
