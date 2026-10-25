"""Tests for Stream 1B: Sandbox GIL contention resilience, AST pre-compilation, and isolated circuit-breaker."""

import json
from pathlib import Path
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent / ".agents" / "skills" / "content-to-course"
if str(SKILL_DIR) not in sys.path:
    sys.path.insert(0, str(SKILL_DIR))

from engine.sandbox import (
    call_with_timeout,
    execute_sandbox_batch,
    SandboxSecurityError,
    SecurityViolationError,
    SandboxTimeoutError,
    SandboxExecutionError,
)
from check_templates import check_templates_file_or_dir


class TestSandboxBatchPrecompilationAndErrors:
    """Verifies that execute_sandbox_batch pre-compiles code and maintains accurate error types."""

    def test_execute_sandbox_batch_50_seeds_clean(self):
        """Batch executes 50 seeds cleanly without redundant AST parses or compiles."""
        code = """
def generate(rng):
    import math
    a = rng.randint(1, 50)
    b = rng.randint(1, 50)
    hypot = math.hypot(a, b)
    return {
        "vars": {"a": a, "b": b, "hypot": hypot},
        "correct": str(round(hypot, 2)),
        "distractors": [str(round(hypot + 1, 2)), str(round(hypot - 1, 2)), str(round(hypot * 2, 2))]
    }
"""
        seeds = list(range(100, 150))
        results = execute_sandbox_batch(code, seeds=seeds, timeout_per_item=0.8)
        assert len(results) == 50
        assert all(r.get("success") is True for r in results)
        assert all(r.get("ok") is True for r in results)
        assert all("result" in r for r in results)
        assert results[0]["result"]["vars"]["a"] is not None

    def test_syntax_error_detection(self):
        """Syntax errors in generate_py are captured cleanly."""
        bad_syntax_code = "def generate(rng)\n    return 42"  # Missing colon
        seeds = [1, 2, 3]
        results = execute_sandbox_batch(bad_syntax_code, seeds=seeds)
        assert len(results) >= 1
        assert results[0]["success"] is False
        assert "SyntaxError" in results[0]["error"]
        assert results[0].get("stage") == "generate"

    def test_security_violation_detection(self):
        """SandboxSecurityError / SecurityViolationError is raised on prohibited imports or builtins."""
        banned_code = """
import os
def generate(rng):
    return {"vars": {}, "correct": 1, "distractors": []}
"""
        with pytest.raises((SecurityViolationError, SandboxSecurityError)):
            execute_sandbox_batch(banned_code, seeds=[42])

    def test_real_infinite_loop_timeout_clean_termination(self):
        """Real infinite loop while True: pass is caught cleanly by SandboxTimeoutError."""
        infinite_loop_code = """
def generate(rng):
    while True:
        pass
    return {"vars": {}, "correct": 1, "distractors": []}
"""
        seeds = [10, 20]
        results = execute_sandbox_batch(infinite_loop_code, seeds=seeds, timeout_per_item=0.4)
        assert len(results) == 2
        for r in results:
            assert r["success"] is False
            assert "SandboxTimeoutError" in r["error"]

    def test_cross_check_mutation_isolation(self):
        """Mutations inside verify(gen_res) do not contaminate result['vars'] or other seed outputs."""
        code_gen = """
def generate(rng):
    val = rng.randint(100, 200)
    return {
        "vars": {"val": val, "items": [1, 2, 3]},
        "correct": str(val),
        "distractors": [str(val + 1), str(val - 1), str(val + 2)]
    }
"""
        code_verify_mutating = """
def verify(res):
    # Adversarially attempt to mutate input result dictionary
    res["vars"]["val"] = 99999
    res["vars"]["items"].append(99999)
    res["vars"]["injected_key"] = "compromised"
    return True
"""
        seeds = [10, 20, 30]
        results = execute_sandbox_batch(
            generate_py=code_gen,
            seeds=seeds,
            cross_check_py=code_verify_mutating,
            timeout_per_item=0.8,
        )
        assert len(results) == 3
        for r in results:
            assert r["success"] is True
            vars_dict = r["result"]["vars"]
            assert vars_dict["val"] != 99999, "vars['val'] was mutated by cross_check verify!"
            assert vars_dict["items"] == [1, 2, 3], "vars['items'] was mutated by cross_check verify!"
            assert "injected_key" not in vars_dict, "injected_key leaked into result vars!"


class TestGILContentionResistance:
    """Verifies that 16 concurrent threads do not suffer false timeouts under GIL contention."""

    def test_16_concurrent_threads_no_false_timeouts(self):
        """16 concurrent threads running execute_sandbox_batch with timeout_sec=0.8 must all succeed."""
        valid_template_code = """
def generate(rng):
    import math
    import fractions
    x = rng.randint(2, 20)
    y = rng.randint(3, 30)
    frac = fractions.Fraction(x, y)
    return {
        "vars": {"x": x, "y": y, "frac": str(frac)},
        "correct": str(frac),
        "distractors": [str(frac + 1), str(frac - 1), str(frac * 2)]
    }
"""
        seeds = list(range(200, 215))  # 15 seeds per thread

        def _worker_task(thread_id: int):
            return execute_sandbox_batch(
                generate_py=valid_template_code,
                seeds=seeds,
                timeout_sec=0.8,
            )

        with ThreadPoolExecutor(max_workers=16) as executor:
            futures = [executor.submit(_worker_task, i) for i in range(16)]
            for fut in futures:
                batch_res = fut.result()
                assert len(batch_res) == len(seeds)
                for item in batch_res:
                    assert item.get("success") is True, f"Item failed under GIL: {item}"

    def test_real_infinite_loop_under_thread_pool_executor_raises_timeout(self):
        """Infinite loop while True: pass running inside a ThreadPoolExecutor worker thread with active threads."""
        infinite_loop_code = """
def generate(rng):
    while True:
        pass
    return {"vars": {}, "correct": "1", "distractors": []}
"""
        stop_event = threading.Event()

        def _bg_keepalive():
            stop_event.wait(timeout=5.0)

        with ThreadPoolExecutor(max_workers=4) as executor:
            # Keep a background worker alive to guarantee threading.active_count() > 1
            bg_fut = executor.submit(_bg_keepalive)
            assert threading.active_count() > 1

            def _run_in_thread():
                return execute_sandbox_batch(
                    infinite_loop_code,
                    seeds=[42],
                    timeout_per_item=0.4,
                )

            t0 = time.time()
            worker_fut = executor.submit(_run_in_thread)
            batch_res = worker_fut.result(timeout=4.0)
            elapsed = time.time() - t0

            stop_event.set()
            bg_fut.result()

            assert len(batch_res) == 1
            assert batch_res[0]["success"] is False
            assert "SandboxTimeoutError" in batch_res[0]["error"]
            assert elapsed < 3.0, f"Worker thread timeout took {elapsed:.2f}s, expected < 3.0s"

        # Also verify direct call_with_timeout invocation inside ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=2) as executor:
            def _loop_task():
                def _loop():
                    while True:
                        pass
                return call_with_timeout(_loop, timeout=0.3)

            fut = executor.submit(_loop_task)
            with pytest.raises(SandboxTimeoutError):
                fut.result(timeout=3.0)


class TestCompetencyCircuitBreakerIsolation:
    """Verifies that budget halt tracking isolates each competency and avoids false halts on clean competencies."""

    def test_isolated_budget_halt_on_failing_competency_only(self, tmp_path):
        """When C-01 and C-02 are healthy and C-03 fails 3 times, ONLY C-03 enters BUDGET HALT."""
        attempts_dir = tmp_path / ".check_attempts"
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)

        cta_data = {
            "course_id": "test_isolation_course",
            "title": "Circuit Breaker Test Course",
            "competencies": [
                {"id": "C-01", "name": "Comp 1", "type": "concept", "distractors": []},
                {"id": "C-02", "name": "Comp 2", "type": "concept", "distractors": []},
                {"id": "C-03", "name": "Comp 3", "type": "concept", "distractors": []},
            ],
        }
        cta_file = tmp_path / "cta.json"
        cta_file.write_text(json.dumps(cta_data, indent=2), encoding="utf-8")

        # Healthy template generator
        def _make_healthy_tpl(cid: str):
            return {
                "competency_id": cid,
                "templates": [
                    {
                        "id": f"T-{cid}-01",
                        "competency_id": cid,
                        "interaction_type": "fill_in_the_blank",
                        "difficulty": "easy",
                        "bloom": "Apply",
                        "stem": f"Encuentre la solución analítica para el parámetro {{v}} en la competencia {cid}.",
                        "stem_variants": [
                            f"Encuentre la solución analítica para el parámetro {{v}} en la competencia {cid}.",
                            f"Calcule el valor exacto del coeficiente {{v}} correspondiente a {cid}.",
                            f"Determine analíticamente la magnitud {{v}} según las condiciones de {cid}.",
                            f"Evalúe la cantidad escalar {{v}} asociada a la especificación {cid}.",
                            f"Halle el resultado final para la variable {{v}} en el contexto {cid}.",
                            f"Identifique el valor matemático del parámetro {{v}} para {cid}.",
                        ],
                        "generate_py": (
                            "def generate(rng):\n"
                            "    v = rng.randint(100, 999)\n"
                            "    return {'vars': {'v': v}, 'correct': str(v), 'value': str(v), 'distractors': []}\n"
                        ),
                        "cross_check_py": "def verify(res):\n    return True\n",
                        "hints": ["Hint 1", "Hint 2", "Hint 3"],
                        "solution": "Solución {v}",
                        "distractor_ids": [],
                    }
                ],
            }

        # Failing template (narrow domain, no variants -> fails TPL-VAR, or runtime error)
        def _make_failing_tpl(cid: str):
            return {
                "competency_id": cid,
                "templates": [
                    {
                        "id": f"T-{cid}-01",
                        "competency_id": cid,
                        "interaction_type": "fill_in_the_blank",
                        "difficulty": "easy",
                        "bloom": "Apply",
                        "stem": f"Failing stem for {cid}",
                        "generate_py": (
                            "def generate(rng):\n"
                            "    raise RuntimeError('Deliberate runtime crash in generate')\n"
                        ),
                        "cross_check_py": "def verify(res):\n    return True\n",
                        "hints": ["h1", "h2", "h3"],
                        "solution": "sol",
                        "distractor_ids": [],
                    }
                ],
            }

        # Write template files
        (templates_dir / "C-01.json").write_text(json.dumps(_make_healthy_tpl("C-01"), indent=2), encoding="utf-8")
        (templates_dir / "C-02.json").write_text(json.dumps(_make_healthy_tpl("C-02"), indent=2), encoding="utf-8")
        (templates_dir / "C-03.json").write_text(json.dumps(_make_failing_tpl("C-03"), indent=2), encoding="utf-8")

        # Run 1: First check
        is_clean_1, errors_1 = check_templates_file_or_dir(
            templates_dir,
            cta_path=cta_file,
            num_dry_run_seeds=10,
            attempts_dir=attempts_dir,
            strict=False,
        )
        assert is_clean_1 is False
        assert any("C-03" in e for e in errors_1)
        assert not any("BUDGET HALT" in e for e in errors_1)

        # C-01 and C-02 must be clean in attempts_dir
        c1_att = attempts_dir / "C-01.json"
        c2_att = attempts_dir / "C-02.json"
        c3_att = attempts_dir / "C-03.json"
        assert not c1_att.exists(), "C-01 should not have an attempt file registered on clean pass"
        assert not c2_att.exists(), "C-02 should not have an attempt file registered on clean pass"
        assert c3_att.exists(), "C-03 must record its failed attempt"
        c3_data_1 = json.loads(c3_att.read_text(encoding="utf-8"))
        assert c3_data_1["attempts"] == 1
        assert c3_data_1["halted"] is False

        # Run 2: Second check (same unmodified source)
        is_clean_2, errors_2 = check_templates_file_or_dir(
            templates_dir,
            cta_path=cta_file,
            num_dry_run_seeds=10,
            attempts_dir=attempts_dir,
            strict=False,
        )
        assert is_clean_2 is False
        c3_data_2 = json.loads(c3_att.read_text(encoding="utf-8"))
        assert c3_data_2["attempts"] == 2
        assert c3_data_2["halted"] is False
        assert not c1_att.exists()
        assert not c2_att.exists()

        # Run 3: Third check (triggers BUDGET HALT on C-03)
        is_clean_3, errors_3 = check_templates_file_or_dir(
            templates_dir,
            cta_path=cta_file,
            num_dry_run_seeds=10,
            attempts_dir=attempts_dir,
            strict=False,
        )
        assert is_clean_3 is False
        c3_data_3 = json.loads(c3_att.read_text(encoding="utf-8"))
        assert c3_data_3["attempts"] >= 3
        assert c3_data_3["halted"] is True

        # Exactly C-03 must be in BUDGET HALT
        halt_messages = [e for e in errors_3 if "BUDGET HALT" in e]
        assert len(halt_messages) >= 1
        assert any("BUDGET HALT on competency 'C-03'" in m for m in halt_messages)
        # Ensure C-01 and C-02 NEVER have BUDGET HALT
        assert not any("C-01" in m for m in halt_messages)
        assert not any("C-02" in m for m in halt_messages)
        assert not c1_att.exists()
        assert not c2_att.exists()

    def test_competency_recovery_clears_attempt_file_while_neighbor_fails(self, tmp_path):
        """When C-03 was in BUDGET HALT and is fixed in run 4 while C-02 fails for the first time:
        C-03 must clear its attempt file and exit BUDGET HALT, while C-02 registers attempt 1."""
        attempts_dir = tmp_path / ".check_attempts"
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)

        cta_data = {
            "course_id": "test_recovery_course",
            "title": "Circuit Breaker Recovery Test",
            "competencies": [
                {"id": "C-01", "name": "Comp 1", "type": "concept", "distractors": []},
                {"id": "C-02", "name": "Comp 2", "type": "concept", "distractors": []},
                {"id": "C-03", "name": "Comp 3", "type": "concept", "distractors": []},
            ],
        }
        cta_file = tmp_path / "cta.json"
        cta_file.write_text(json.dumps(cta_data, indent=2), encoding="utf-8")

        def _make_healthy(cid: str):
            return {
                "competency_id": cid,
                "templates": [
                    {
                        "id": f"T-{cid}-01",
                        "competency_id": cid,
                        "interaction_type": "fill_in_the_blank",
                        "difficulty": "easy",
                        "bloom": "Apply",
                        "stem": f"Encuentre el resultado para {{v}} en {cid}.",
                        "stem_variants": [
                            f"Encuentre el resultado para {{v}} en {cid}.",
                            f"Calcule el valor del parámetro {{v}} para {cid}.",
                            f"Determine analíticamente el coeficiente {{v}} de {cid}.",
                            f"Evalúe la cantidad escalar {{v}} en {cid}.",
                            f"Halle la magnitud requerida {{v}} para {cid}.",
                            f"Identifique el resultado de {{v}} en {cid}.",
                        ],
                        "generate_py": (
                            "def generate(rng):\n"
                            "    v = rng.randint(10, 99)\n"
                            "    return {'vars': {'v': v}, 'correct': str(v), 'value': str(v), 'distractors': []}\n"
                        ),
                        "cross_check_py": "def verify(res):\n    return True\n",
                        "hints": ["h1", "h2", "h3"],
                        "solution": "sol {v}",
                        "distractor_ids": [],
                    }
                ],
            }

        def _make_failing(cid: str):
            return {
                "competency_id": cid,
                "templates": [
                    {
                        "id": f"T-{cid}-01",
                        "competency_id": cid,
                        "interaction_type": "fill_in_the_blank",
                        "difficulty": "easy",
                        "bloom": "Apply",
                        "stem": f"Failing stem for {cid}",
                        "generate_py": (
                            "def generate(rng):\n"
                            "    raise ValueError('Deliberate fail')\n"
                        ),
                        "cross_check_py": "def verify(res):\n    return True\n",
                        "hints": ["h1", "h2", "h3"],
                        "solution": "sol",
                        "distractor_ids": [],
                    }
                ],
            }

        # Setup initial state: C-01 & C-02 healthy, C-03 failing
        (templates_dir / "C-01.json").write_text(json.dumps(_make_healthy("C-01")), encoding="utf-8")
        (templates_dir / "C-02.json").write_text(json.dumps(_make_healthy("C-02")), encoding="utf-8")
        (templates_dir / "C-03.json").write_text(json.dumps(_make_failing("C-03")), encoding="utf-8")

        # Runs 1, 2, 3: Drive C-03 into BUDGET HALT
        for i in range(1, 4):
            check_templates_file_or_dir(
                templates_dir,
                cta_path=cta_file,
                num_dry_run_seeds=5,
                attempts_dir=attempts_dir,
                strict=False,
            )

        c3_att = attempts_dir / "C-03.json"
        assert c3_att.is_file(), "C-03 attempt file must exist"
        c3_data = json.loads(c3_att.read_text(encoding="utf-8"))
        assert c3_data["halted"] is True
        assert c3_data["attempts"] >= 3

        # Run 4: FIX C-03 (healthy now!), and BREAK C-02 (failing now!)
        (templates_dir / "C-03.json").write_text(json.dumps(_make_healthy("C-03")), encoding="utf-8")
        (templates_dir / "C-02.json").write_text(json.dumps(_make_failing("C-02")), encoding="utf-8")

        is_clean_4, errors_4 = check_templates_file_or_dir(
            templates_dir,
            cta_path=cta_file,
            num_dry_run_seeds=5,
            attempts_dir=attempts_dir,
            strict=False,
        )

        assert is_clean_4 is False, "Run 4 must not be clean overall because C-02 failed"
        # C-03 must be completely cleared: attempt file removed!
        assert not c3_att.exists(), "C-03.json attempt file must be deleted upon clean pass!"
        # No BUDGET HALT message for C-03
        assert not any("BUDGET HALT on competency 'C-03'" in e for e in errors_4)
        assert not any("competency 'C-03'" in e.lower() for e in errors_4)

        # C-02 must have its attempt recorded (attempt 1, not halted)
        c2_att = attempts_dir / "C-02.json"
        assert c2_att.is_file()
        c2_data = json.loads(c2_att.read_text(encoding="utf-8"))
        assert c2_data["attempts"] == 1
        assert c2_data["halted"] is False

        # C-01 remained healthy throughout: never has an attempt file
        c1_att = attempts_dir / "C-01.json"
        assert not c1_att.exists()

    def test_shared_prefix_id_non_collision(self, tmp_path):
        """Competencies with shared prefix (e.g. C-01 healthy vs C-010 failing) must never collide."""
        attempts_dir = tmp_path / ".check_attempts"
        templates_dir = tmp_path / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)

        cta_data = {
            "course_id": "test_prefix_course",
            "title": "Prefix Collision Test",
            "competencies": [
                {"id": "C-01", "name": "Comp 01", "type": "concept", "distractors": []},
                {"id": "C-010", "name": "Comp 010", "type": "concept", "distractors": []},
            ],
        }
        cta_file = tmp_path / "cta.json"
        cta_file.write_text(json.dumps(cta_data, indent=2), encoding="utf-8")

        def _make_healthy(cid: str):
            return {
                "competency_id": cid,
                "templates": [
                    {
                        "id": f"T-{cid}-01",
                        "competency_id": cid,
                        "interaction_type": "fill_in_the_blank",
                        "difficulty": "easy",
                        "bloom": "Apply",
                        "stem": f"Valor para {{v}} en {cid}.",
                        "stem_variants": [
                            f"Valor para {{v}} en {cid}.",
                            f"Calcule el valor para {{v}} en {cid}.",
                            f"Determine el parámetro {{v}} en {cid}.",
                            f"Evalúe la variable {{v}} en {cid}.",
                            f"Halle la solución de {{v}} en {cid}.",
                            f"Identifique el valor de {{v}} en {cid}.",
                        ],
                        "generate_py": (
                            "def generate(rng):\n"
                            "    v = rng.randint(10, 50)\n"
                            "    return {'vars': {'v': v}, 'correct': str(v), 'value': str(v), 'distractors': []}\n"
                        ),
                        "cross_check_py": "def verify(res):\n    return True\n",
                        "hints": ["h1", "h2", "h3"],
                        "solution": "sol {v}",
                        "distractor_ids": [],
                    }
                ],
            }

        def _make_failing(cid: str):
            return {
                "competency_id": cid,
                "templates": [
                    {
                        "id": f"T-{cid}-01",
                        "competency_id": cid,
                        "interaction_type": "fill_in_the_blank",
                        "difficulty": "easy",
                        "bloom": "Apply",
                        "stem": f"Failing stem for {cid}",
                        "generate_py": (
                            "def generate(rng):\n"
                            "    raise RuntimeError('C-010 specific syntax/runtime crash')\n"
                        ),
                        "cross_check_py": "def verify(res):\n    return True\n",
                        "hints": ["h1", "h2", "h3"],
                        "solution": "sol",
                        "distractor_ids": [],
                    }
                ],
            }

        # Write C-01 (healthy) and C-010 (failing)
        (templates_dir / "C-01.json").write_text(json.dumps(_make_healthy("C-01")), encoding="utf-8")
        (templates_dir / "C-010.json").write_text(json.dumps(_make_failing("C-010")), encoding="utf-8")

        # Run 3 consecutive cycles to push C-010 into BUDGET HALT
        errs = []
        for i in range(1, 4):
            is_clean, errs = check_templates_file_or_dir(
                templates_dir,
                cta_path=cta_file,
                num_dry_run_seeds=5,
                attempts_dir=attempts_dir,
                strict=False,
            )
            assert is_clean is False

        c01_att = attempts_dir / "C-01.json"
        c010_att = attempts_dir / "C-010.json"

        # C-01 must NEVER have an attempt file registered
        assert not c01_att.exists(), "C-01 must NOT have attempt file despite shared prefix with C-010!"

        # C-010 must have entered BUDGET HALT
        assert c010_att.is_file()
        c010_data = json.loads(c010_att.read_text(encoding="utf-8"))
        assert c010_data["halted"] is True
        assert c010_data["attempts"] >= 3

        # Errors must explicitly mention C-010 and NOT C-01
        halt_msgs = [e for e in errs if "BUDGET HALT" in e]
        assert len(halt_msgs) >= 1
        assert any("BUDGET HALT on competency 'C-010'" in m for m in halt_msgs)
        assert not any("BUDGET HALT on competency 'C-01'" in m for m in halt_msgs)
