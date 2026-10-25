"""Tests for C2C v3.4 Stream 1D: Worker Write Isolation, Early Post-PASS Cut, & Anti-Monolithic Rewrite Guards.

Verifies:
1. Rule A: Worker Python write path isolation blocks ad-hoc debug scripts (test_debug.py, debug_shard.py, etc.)
   outside authorized C2C shard/fix/scratch paths.
2. Rule B: Early cut guard post-PASS blocks write_file and edit_file on shard_XX_data.py when pass_shard_XX.json is PASS.
3. Rule C: Anti-monolithic rewrite guard blocks write_file when shard_XX_data.py exists with >250 lines and
   prior compilation failure is recorded, while allowing edit_file and shard_fixes/<CID>.py.
4. Clean integration with Director diet and auditor exemptions.
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / ".agents" / "skills" / "content-to-course"))

from c2c_hook_guard import evaluate_hook_payload, process_hook  # noqa: E402


class TestHookPostPassAndWriteIsolation(unittest.TestCase):
    """Suite verifying Stream 1D Hook Guard Rules A, B, and C."""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="c2c_hook_1d_test_")
        self.lock_file = Path(self.test_dir) / ".c2c_subagent_lock.json"
        self.course_id = "demo_course"
        self.work_dir = Path(self.test_dir) / "courses" / self.course_id / "work"
        self.shards_dir = self.work_dir / "shards"
        self.shard_fixes_dir = self.shards_dir / "shard_fixes"
        self.check_attempts_dir = self.work_dir / ".check_attempts"

        self.shards_dir.mkdir(parents=True, exist_ok=True)
        self.shard_fixes_dir.mkdir(parents=True, exist_ok=True)
        self.check_attempts_dir.mkdir(parents=True, exist_ok=True)

        self.director_id = "director-conv-uuid"
        self.worker_id = "worker-subagent-uuid"
        self.auditor_id = "auditor-conv-uuid"

        # Active lock for the demo course
        self.lock_data = {
            "active": True,
            "director_conversation_id": self.director_id,
            "course_id": self.course_id,
            "work_dir": str(self.work_dir),
            "exempt_conversation_ids": [self.auditor_id],
        }
        self.lock_file.write_text(json.dumps(self.lock_data), encoding="utf-8")

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    # --------------------------------------------------------------------------
    # RULE A: Worker Python Write Path Isolation (Ad-Hoc Debug Script Blocking)
    # --------------------------------------------------------------------------

    def test_rule_a_blocks_root_debug_scripts(self) -> None:
        """Worker is blocked from creating ad-hoc debug scripts in project root."""
        ad_hoc_scripts = [
            "test_debug.py",
            "debug_shard.py",
            "scratch_debug.py",
            "quick_test.py",
            "courses/demo_course/work/adhoc_debug.py",
            "courses/demo_course/work/shards/random_script.py",
            "tests/test_something.py",
        ]

        for script_path in ad_hoc_scripts:
            payload = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {
                        "Path": script_path,
                        "Content": "print('debugging')",
                    },
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(
                res.get("decision"),
                "deny",
                f"Expected deny for worker creating ad-hoc script: {script_path}",
            )
            self.assertIn("BLOCKER:: Prohibido crear o editar scripts Python arbitrarios", res.get("reason", ""))
            self.assertIn("work/shards/<shard_id>_data.py", res.get("reason", ""))

    def test_rule_a_allows_authorized_c2c_worker_python_paths(self) -> None:
        """Worker is allowed to write to legitimate C2C Python paths."""
        authorized_writes = [
            ("courses/demo_course/work/shards/shard_01_data.py", "# shard data"),
            ("courses/demo_course/work/shards/shard_fixes/Hab-01.py", "# modular fix"),
            ("courses/demo_course/work/shards/build_shard_01.py", "# build script"),
            ("courses/demo_course/work/cta/part_01.py", "# cta part"),
            ("courses/demo_course/work/cta_data.py", "# cta data"),
            ("courses/demo_course/work_append/shards/shard_01_data.py", "# append data"),
            ("scratch/my_scratch_script.py", "# scratch test"),
            ("C:/Users/augus/.gemini/antigravity/brain/session/scratch/test.py", "# brain scratch"),
        ]

        for path_str, content_str in authorized_writes:
            payload = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {
                        "Path": path_str,
                        "Content": content_str,
                    },
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(
                res.get("decision"),
                "allow",
                f"Expected allow for legitimate worker Python path: {path_str}, got: {res}",
            )

    def test_rule_a_allows_non_python_worker_files(self) -> None:
        """Rule A does not interfere with non-Python files like JSON manifests or text files."""
        non_py_files = [
            "courses/demo_course/work/shards/shard_01_manifest.json",
            "courses/demo_course/work/notes.txt",
        ]
        for path_str in non_py_files:
            payload = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {
                        "Path": path_str,
                        "Content": "{}",
                    },
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(res.get("decision"), "allow", f"Failed for {path_str}: {res}")

    # --------------------------------------------------------------------------
    # RULE B: Early Cut Guard Post-PASS (.check_attempts/pass_<shard_id>.json)
    # --------------------------------------------------------------------------

    def test_rule_b_blocks_write_and_edit_when_shard_passed(self) -> None:
        """When pass_<shard_id>.json has status PASS, write_file and edit_file are blocked."""
        # Setup pass_shard_01.json
        pass_file = self.check_attempts_dir / "pass_shard_01.json"
        pass_file.write_text(json.dumps({"status": "PASS", "shard_id": "shard_01"}), encoding="utf-8")

        shard_py = self.shards_dir / "shard_01_data.py"

        # 1. write_file attempt
        payload_write = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(shard_py),
                    "Content": "# unnecessary rewrite after pass",
                },
            },
        }
        res_write = process_hook(payload_write, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_write.get("decision"), "deny")
        self.assertIn("BLOCKER:: El shard shard_01 ya aprobó todas las validaciones estrictas ([+] PASS)", res_write.get("reason", ""))
        self.assertIn("emite DONE inmediatamente", res_write.get("reason", ""))

        # 2. edit_file attempt
        payload_edit = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "edit_file",
                "args": {
                    "Path": str(shard_py),
                    "Target": "pass",
                    "Replacement": "pass",
                },
            },
        }
        res_edit = process_hook(payload_edit, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_edit.get("decision"), "deny")
        self.assertIn("BLOCKER:: El shard shard_01 ya aprobó todas las validaciones estrictas ([+] PASS)", res_edit.get("reason", ""))

        # 3. replace_file_content attempt
        payload_replace = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "replace_file_content",
                "args": {
                    "Path": str(shard_py),
                    "Target": "pass",
                    "Replacement": "pass",
                },
            },
        }
        res_replace = process_hook(payload_replace, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_replace.get("decision"), "deny")

    def test_rule_b_allows_writing_to_other_shards_without_pass_file(self) -> None:
        """A shard that has not passed yet is not blocked by Rule B."""
        # pass_shard_01 exists, but shard_02 has no pass file
        pass_file = self.check_attempts_dir / "pass_shard_01.json"
        pass_file.write_text(json.dumps({"status": "PASS"}), encoding="utf-8")

        shard_02_py = self.shards_dir / "shard_02_data.py"
        payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(shard_02_py),
                    "Content": "# shard 02 in progress",
                },
            },
        }
        res = process_hook(payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res.get("decision"), "allow")

    def test_rule_b_allows_when_pass_file_is_not_status_pass(self) -> None:
        """If pass file has status != PASS (e.g. FAIL or IN_PROGRESS), writes are allowed."""
        pass_file = self.check_attempts_dir / "pass_shard_01.json"
        pass_file.write_text(json.dumps({"status": "FAIL", "errors": ["E1"]}), encoding="utf-8")

        shard_py = self.shards_dir / "shard_01_data.py"
        payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "edit_file",
                "args": {
                    "Path": str(shard_py),
                    "Target": "# a",
                    "Replacement": "# b",
                },
            },
        }
        res = process_hook(payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res.get("decision"), "allow")

    # --------------------------------------------------------------------------
    # RULE C: Anti-Monolithic Rewrite Guard After Compile Failure (> 250 lines)
    # --------------------------------------------------------------------------

    def test_rule_c_blocks_monolithic_write_file_on_compiled_shard_over_250_lines(self) -> None:
        """When shard exists with > 250 lines and previous compile failure exists, write_file is blocked."""
        shard_py = self.shards_dir / "shard_01_data.py"
        # Create existing file with 260 lines
        lines = [f"# Line {i}\n" for i in range(260)]
        shard_py.write_text("".join(lines), encoding="utf-8")

        # Record a previous compile attempt in .check_attempts/compile_shard_01.json
        compile_file = self.check_attempts_dir / "compile_shard_01.json"
        compile_file.write_text(
            json.dumps({
                "distinct_compiles": 1,
                "same_error_streak": 1,
                "last_err_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "last_errors": ["[SHARD-01] SyntaxError line 15"],
            }),
            encoding="utf-8",
        )

        # 1. Full write_file attempt should be DENIED
        payload_write = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(shard_py),
                    "Content": "".join(lines),
                },
            },
        }
        res_write = process_hook(payload_write, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_write.get("decision"), "deny")
        self.assertIn("BLOCKER:: El archivo shard_01_data.py ya fue compilado y supera las 250 líneas", res_write.get("reason", ""))
        self.assertIn("usa edit_file quirúrgico", res_write.get("reason", ""))
        self.assertIn("work/shards/shard_fixes/<CID>.py", res_write.get("reason", ""))

        # 2. Surgical edit_file on the same file should be ALLOWED
        payload_edit = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "edit_file",
                "args": {
                    "Path": str(shard_py),
                    "Target": "# Line 15",
                    "Replacement": "# Line 15 repaired",
                },
            },
        }
        res_edit = process_hook(payload_edit, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_edit.get("decision"), "allow")

        # 3. Writing a modular fix in work/shards/shard_fixes/Hab-01.py should be ALLOWED
        fix_py = self.shard_fixes_dir / "Hab-01.py"
        payload_fix = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(fix_py),
                    "Content": "TEMPLATES_OVERRIDE = []",
                },
            },
        }
        res_fix = process_hook(payload_fix, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_fix.get("decision"), "allow")

    def test_rule_c_allows_turn1_creation_when_file_not_on_disk(self) -> None:
        """Turn 1 initial creation of shard_data.py (file not yet on disk) is allowed even with > 250 lines."""
        shard_py = self.shards_dir / "shard_03_data.py"
        self.assertFalse(shard_py.is_file())

        big_content = "".join([f"# Line {i}\n" for i in range(300)])
        payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(shard_py),
                    "Content": big_content,
                },
            },
        }
        res = process_hook(payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res.get("decision"), "allow")

    def test_rule_c_allows_write_file_when_under_250_lines(self) -> None:
        """When existing shard and new content have <= 250 lines, write_file is allowed."""
        shard_py = self.shards_dir / "shard_04_data.py"
        small_content = "".join([f"# Line {i}\n" for i in range(80)])
        shard_py.write_text(small_content, encoding="utf-8")

        # Prior compile attempt exists
        compile_file = self.check_attempts_dir / "compile_shard_04.json"
        compile_file.write_text(json.dumps({"distinct_compiles": 1, "last_err_hash": "hash1"}), encoding="utf-8")

        payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(shard_py),
                    "Content": small_content,
                },
            },
        }
        res = process_hook(payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res.get("decision"), "allow")

    def test_rule_c_allows_write_file_when_no_prior_compile_attempt(self) -> None:
        """If compile_<shard_id>.json does not exist yet (no prior compile), write_file is allowed."""
        shard_py = self.shards_dir / "shard_05_data.py"
        lines = "".join([f"# Line {i}\n" for i in range(300)])
        shard_py.write_text(lines, encoding="utf-8")

        # No compile_shard_05.json exists in .check_attempts
        payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(shard_py),
                    "Content": lines,
                },
            },
        }
        res = process_hook(payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res.get("decision"), "allow")

    # --------------------------------------------------------------------------
    # Roles & Exemptions: Director and Auditor Behavior
    # --------------------------------------------------------------------------

    def test_auditor_exemption_bypasses_all_worker_rules(self) -> None:
        """An exempt auditor can write/read freely without worker rule blockage."""
        # Setup pass_shard_01.json
        pass_file = self.check_attempts_dir / "pass_shard_01.json"
        pass_file.write_text(json.dumps({"status": "PASS"}), encoding="utf-8")

        shard_py = self.shards_dir / "shard_01_data.py"
        shard_py.write_text("".join([f"# Line {i}\n" for i in range(300)]), encoding="utf-8")

        # Auditor editing shard_01_data.py (would be blocked by Rule B for worker)
        payload = {
            "conversationId": self.auditor_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(shard_py),
                    "Content": "# auditor override",
                },
            },
        }
        res = process_hook(payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res.get("decision"), "allow")

    def test_director_diet_remains_active_for_director(self) -> None:
        """Director is evaluated under Director Diet (Case A), not under worker rules."""
        shard_py = self.shards_dir / "shard_01_data.py"
        payload = {
            "conversationId": self.director_id,
            "toolCall": {
                "name": "view_file",
                "args": {"Path": str(shard_py)},
            },
        }
        res = process_hook(payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res.get("decision"), "deny")
        self.assertIn("Director Diet", res.get("reason", ""))

    # --------------------------------------------------------------------------
    # Hardening: Windows Paths, Shard Fixes Resilience, & Fail-Open Safety
    # --------------------------------------------------------------------------

    def test_windows_path_formats_and_casing_variations(self) -> None:
        """Rule B and Rule C correctly resolve paths across Windows backslashes, casing, file URIs, and double slashes."""
        # Setup pass_shard_01.json
        pass_file = self.check_attempts_dir / "pass_shard_01.json"
        pass_file.write_text(json.dumps({"status": "PASS", "shard_id": "shard_01"}), encoding="utf-8")

        shard_py = self.shards_dir / "shard_01_data.py"
        shard_str = str(shard_py)

        windows_variants = [
            # Windows backslashes
            shard_str.replace("/", "\\"),
            # Double backslashes
            shard_str.replace("/", "\\\\"),
            # File URI
            f"file:///{shard_str.replace('\\', '/')}",
            # File URI localhost
            f"file://localhost/{shard_str.replace('\\', '/')}",
            # Lowercase drive letter
            f"{shard_str[0].lower()}{shard_str[1:]}",
            # Uppercase drive letter
            f"{shard_str[0].upper()}{shard_str[1:]}",
            # Mixed slashes and double slashes
            shard_str.replace("/", "//").replace("\\", "//"),
            # Leading ./
            f"./{shard_str}",
            # Uppercase filename
            f"{shard_py.parent.as_posix()}/SHARD_01_DATA.PY",
        ]

        for p in windows_variants:
            payload = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "edit_file",
                    "args": {
                        "Path": p,
                        "Target": "# foo",
                        "Replacement": "# bar",
                    },
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(
                res.get("decision"),
                "deny",
                f"Expected Rule B deny for Windows path variant: '{p}', got: {res}",
            )
            self.assertIn("ya aprobó todas las validaciones estrictas ([+] PASS)", res.get("reason", ""))
            self.assertIn("emite DONE inmediatamente", res.get("reason", ""))

    def test_shard_fixes_always_allowed_even_with_compile_failures_and_over_250_lines(self) -> None:
        """shard_fixes/<CID>.py must always be allowed, even when compile_<shard_id>.json has failures and > 250 lines."""
        # Setup compile_shard_01.json with multiple failures
        compile_file = self.check_attempts_dir / "compile_shard_01.json"
        compile_file.write_text(
            json.dumps({
                "distinct_compiles": 10,
                "attempts": 10,
                "last_err_hash": "deadbeef12345678",
                "last_errors": ["[SHARD-01] ValidationError: competency Q_01 invalid format"],
            }),
            encoding="utf-8",
        )

        # shard_01_data.py has 300 lines on disk
        shard_py = self.shards_dir / "shard_01_data.py"
        shard_py.write_text("".join([f"# Line {i}\n" for i in range(300)]), encoding="utf-8")

        # Large content (> 250 lines) for a modular fix
        big_fix_content = "".join([f"# Modular Fix Line {i}\n" for i in range(280)])

        fix_variants = [
            # Standard relative work path
            ("courses/demo_course/work/shards/shard_fixes/Hab-01.py", "write_file", {"Path": "courses/demo_course/work/shards/shard_fixes/Hab-01.py", "Content": big_fix_content}),
            # Relative to shards/ directory
            ("shard_fixes/Hab-02.py", "write_file", {"Path": "shard_fixes/Hab-02.py", "Content": big_fix_content}),
            # Windows backslashes
            ("courses\\demo_course\\work\\shards\\shard_fixes\\Hab-03.py", "write_file", {"Path": "courses\\demo_course\\work\\shards\\shard_fixes\\Hab-03.py", "Content": big_fix_content}),
            # Absolute path
            (str(self.shard_fixes_dir / "Hab-04.py"), "write_file", {"Path": str(self.shard_fixes_dir / "Hab-04.py"), "Content": big_fix_content}),
            # edit_file on existing fix
            ("courses/demo_course/work/shards/shard_fixes/Hab-01.py", "edit_file", {"Path": "courses/demo_course/work/shards/shard_fixes/Hab-01.py", "Target": "Line 1", "Replacement": "Line 1 repaired"}),
        ]

        for desc, tool, args in fix_variants:
            payload = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": tool,
                    "args": args,
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(
                res.get("decision"),
                "allow",
                f"Expected allow for shard_fixes variant '{desc}' with {tool}, got: {res}",
            )

        # In contrast, writing to shard_01_data.py with > 250 lines remains BLOCKED by Rule C
        payload_blocked = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(shard_py),
                    "Content": "".join([f"# Line {i}\n" for i in range(260)]),
                },
            },
        }
        res_blocked = process_hook(payload_blocked, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_blocked.get("decision"), "deny")
        self.assertIn("BLOCKER:: El archivo shard_01_data.py ya fue compilado y supera las 250 líneas", res_blocked.get("reason", ""))

    def test_pass_file_corrupt_or_fail_does_not_block_fail_open(self) -> None:
        """When pass_<shard_id>.json is corrupt, empty, binary, or has status != PASS, writes are safely allowed."""
        pass_file = self.check_attempts_dir / "pass_shard_01.json"
        shard_py = self.shards_dir / "shard_01_data.py"
        shard_py.write_text("# initial content\n", encoding="utf-8")

        corrupt_scenarios = [
            ("empty_file", ""),
            ("corrupt_json_prefix", '{"status": "PASS", "shard_id": '),
            ("truncated_json", '{"status"'),
            ("non_json_garbage", "FATAL CRASH SEGFAULT 0x000000"),
            ("explicit_fail_status", json.dumps({"status": "FAIL", "errors": ["Compiler error at line 40"]})),
            ("in_progress_status", json.dumps({"status": "IN_PROGRESS"})),
        ]

        for label, content in corrupt_scenarios:
            pass_file.write_text(content, encoding="utf-8")

            payload = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "edit_file",
                    "args": {
                        "Path": str(shard_py),
                        "Target": "# initial",
                        "Replacement": "# updated",
                    },
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(
                res.get("decision"),
                "allow",
                f"Fail-open expected for pass_file scenario '{label}', but got: {res}",
            )

    def test_hook_guard_latency_under_25ms(self) -> None:
        """Execution latency for process_hook under active lock and file checks is well under 25ms per call."""
        import time

        shard_py = self.shards_dir / "shard_01_data.py"
        shard_py.write_text("# Line 1\n# Line 2\n", encoding="utf-8")

        payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "edit_file",
                "args": {
                    "Path": str(shard_py),
                    "Target": "# Line 1",
                    "Replacement": "# Line 1 modified",
                },
            },
        }

        # Warm up
        process_hook(payload, custom_lock_file=str(self.lock_file))

        latencies = []
        for _ in range(100):
            t0 = time.perf_counter()
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            latencies.append(elapsed_ms)
            self.assertEqual(res.get("decision"), "allow")

        max_latency = max(latencies)
        avg_latency = sum(latencies) / len(latencies)

        self.assertLess(
            max_latency,
            25.0,
            f"Max latency {max_latency:.2f}ms exceeded SLA threshold of 25ms",
        )
        self.assertLess(
            avg_latency,
            5.0,
            f"Average latency {avg_latency:.2f}ms exceeded target of 5ms",
        )

    def test_hook_stdout_is_pure_ascii_json_under_cp1252_pipe(self) -> None:
        """Subprocess stdout must be 100% 7-bit ASCII JSON even with Spanish accents and PYTHONIOENCODING=cp1252."""
        import subprocess

        hook_script = REPO_ROOT / ".agents" / "skills" / "content-to-course" / "c2c_hook_guard.py"
        pass_file = self.check_attempts_dir / "pass_shard_01.json"
        pass_file.write_text(json.dumps({"status": "PASS", "shard_id": "shard_01"}), encoding="utf-8")

        payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(self.shards_dir / "shard_01_data.py"),
                    "Content": "# post-pass write",
                },
            },
        }
        env = dict(os.environ, PYTHONIOENCODING="cp1252")
        proc = subprocess.run(
            [sys.executable, str(hook_script)],
            cwd=self.test_dir,
            input=json.dumps(payload).encode("utf-8"),
            capture_output=True,
            env=env,
        )
        self.assertEqual(proc.returncode, 0, f"Hook must always exit 0, stderr={proc.stderr!r}")
        self.assertTrue(
            all(b < 128 for b in proc.stdout),
            f"Hook emitted non-ASCII bytes on CP1252 pipe (breaks protojson UTF-8): {proc.stdout!r}",
        )
        decoded = json.loads(proc.stdout.decode("utf-8"))
        self.assertEqual(decoded.get("decision"), "deny")
        self.assertIn("aprobó", decoded.get("reason", ""))
        self.assertIn("Detén", decoded.get("reason", ""))

    # --------------------------------------------------------------------------
    # STREAM 1C: Sweet Spot CTA & Shards, Error Thresholds, & Anti-Leak Guards
    # --------------------------------------------------------------------------

    def test_rule_c_error_count_under_6_blocks_write_file_on_shard_even_under_250_lines(self) -> None:
        """When error_count is in [1, 5], write_file is blocked even if shard is under 250 lines (e.g. 120 lines)."""
        shard_py = self.shards_dir / "shard_01_data.py"
        shard_content = "".join([f"# Line {i}\n" for i in range(120)])
        shard_py.write_text(shard_content, encoding="utf-8")

        for err_cnt in (1, 3, 5):
            compile_file = self.check_attempts_dir / "compile_shard_01.json"
            compile_file.write_text(
                json.dumps({
                    "distinct_compiles": 1,
                    "error_count": err_cnt,
                    "last_errors": [f"Error {i}" for i in range(err_cnt)],
                }),
                encoding="utf-8",
            )

            # write_file must be DENIED
            payload_write = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {
                        "Path": str(shard_py),
                        "Content": shard_content,
                    },
                },
            }
            res_write = process_hook(payload_write, custom_lock_file=str(self.lock_file))
            self.assertEqual(res_write.get("decision"), "deny")
            self.assertIn(f"registra {err_cnt} errores (< 6, umbral oficial)", res_write.get("reason", ""))
            self.assertIn("usa edit_file quirúrgico", res_write.get("reason", ""))
            self.assertIn("work/shards/shard_fixes/<CID>.py", res_write.get("reason", ""))

            # edit_file must be ALLOWED
            payload_edit = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "edit_file",
                    "args": {
                        "Path": str(shard_py),
                        "Target": "# Line 10",
                        "Replacement": "# Line 10 fixed",
                    },
                },
            }
            res_edit = process_hook(payload_edit, custom_lock_file=str(self.lock_file))
            self.assertEqual(res_edit.get("decision"), "allow")

            # writing to shard_fixes/Hab-01.py must be ALLOWED
            payload_fix = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {
                        "Path": str(self.shard_fixes_dir / "Hab-01.py"),
                        "Content": "# modular fix",
                    },
                },
            }
            res_fix = process_hook(payload_fix, custom_lock_file=str(self.lock_file))
            self.assertEqual(res_fix.get("decision"), "allow")

    def test_rule_c_error_count_6_or_more_allows_write_file_on_shard(self) -> None:
        """When error_count >= 6 (e.g. 6, 10), official sweet spot allows write_file rewrite."""
        shard_py = self.shards_dir / "shard_01_data.py"
        shard_content = "".join([f"# Line {i}\n" for i in range(120)])
        shard_py.write_text(shard_content, encoding="utf-8")

        for err_cnt in (6, 10):
            compile_file = self.check_attempts_dir / "compile_shard_01.json"
            compile_file.write_text(
                json.dumps({
                    "distinct_compiles": 1,
                    "error_count": err_cnt,
                    "last_errors": [f"Error {i}" for i in range(err_cnt)],
                }),
                encoding="utf-8",
            )

            payload_write = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {
                        "Path": str(shard_py),
                        "Content": shard_content,
                    },
                },
            }
            res_write = process_hook(payload_write, custom_lock_file=str(self.lock_file))
            self.assertEqual(res_write.get("decision"), "allow")

    def test_rule_c_has_syntax_error_allows_write_file_recovery(self) -> None:
        """When has_syntax_error is True, write_file is allowed even with error_count=1."""
        shard_py = self.shards_dir / "shard_01_data.py"
        shard_py.write_text("def broken_syntax(:\n", encoding="utf-8")

        compile_file = self.check_attempts_dir / "compile_shard_01.json"
        compile_file.write_text(
            json.dumps({
                "distinct_compiles": 1,
                "error_count": 1,
                "has_syntax_error": True,
                "last_errors": ["SyntaxError: invalid syntax at line 1"],
            }),
            encoding="utf-8",
        )

        payload_write = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(shard_py),
                    "Content": "def valid_syntax(): pass\n",
                },
            },
        }
        res_write = process_hook(payload_write, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_write.get("decision"), "allow")

    def test_rule_c_cta_error_count_thresholds_and_fixes(self) -> None:
        """Rule C applies < 6 errors threshold to cta_data.py and cta_parts/part_01_data.py."""
        cta_parts_dir = self.work_dir / "cta_parts"
        cta_fixes_dir = self.work_dir / "cta_fixes"
        cta_parts_dir.mkdir(parents=True, exist_ok=True)
        cta_fixes_dir.mkdir(parents=True, exist_ok=True)

        cta_targets = [
            (self.work_dir / "cta_data.py", "compile_cta.json", "cta_data.py"),
            (cta_parts_dir / "part_01_data.py", "compile_cta_part_01.json", "part_01_data.py"),
        ]

        for target_path, compile_name, filename in cta_targets:
            target_content = "".join([f"# Line {i}\n" for i in range(100)])
            target_path.write_text(target_content, encoding="utf-8")

            # 1. error_count in (2, 5) -> write_file DENIED, edit_file ALLOWED, cta_fixes ALLOWED
            for err_cnt in (2, 5):
                compile_file = self.check_attempts_dir / compile_name
                compile_file.write_text(
                    json.dumps({
                        "distinct_compiles": 1,
                        "error_count": err_cnt,
                        "last_errors": [f"CTA error {i}" for i in range(err_cnt)],
                    }),
                    encoding="utf-8",
                )

                payload_write = {
                    "conversationId": self.worker_id,
                    "toolCall": {
                        "name": "write_file",
                        "args": {
                            "Path": str(target_path),
                            "Content": target_content,
                        },
                    },
                }
                res_write = process_hook(payload_write, custom_lock_file=str(self.lock_file))
                self.assertEqual(res_write.get("decision"), "deny")
                self.assertIn(f"registra {err_cnt} errores (< 6, umbral oficial)", res_write.get("reason", ""))
                self.assertIn("work/cta_fixes/<CID>.py", res_write.get("reason", ""))

                payload_edit = {
                    "conversationId": self.worker_id,
                    "toolCall": {
                        "name": "edit_file",
                        "args": {
                            "Path": str(target_path),
                            "Target": "# Line 5",
                            "Replacement": "# Line 5 fixed",
                        },
                    },
                }
                res_edit = process_hook(payload_edit, custom_lock_file=str(self.lock_file))
                self.assertEqual(res_edit.get("decision"), "allow")

                # cta_fixes must always be allowed
                payload_fix = {
                    "conversationId": self.worker_id,
                    "toolCall": {
                        "name": "write_file",
                        "args": {
                            "Path": str(cta_fixes_dir / "C-01.py"),
                            "Content": "# modular cta fix",
                        },
                    },
                }
                res_fix = process_hook(payload_fix, custom_lock_file=str(self.lock_file))
                self.assertEqual(res_fix.get("decision"), "allow")

            # 2. error_count = 6 -> write_file ALLOWED
            compile_file = self.check_attempts_dir / compile_name
            compile_file.write_text(
                json.dumps({
                    "distinct_compiles": 1,
                    "error_count": 6,
                    "last_errors": [f"CTA error {i}" for i in range(6)],
                }),
                encoding="utf-8",
            )
            payload_write = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {
                        "Path": str(target_path),
                        "Content": target_content,
                    },
                },
            }
            res_write_6 = process_hook(payload_write, custom_lock_file=str(self.lock_file))
            self.assertEqual(res_write_6.get("decision"), "allow")

            # 3. has_syntax_error = True (with error_count = 2) -> write_file ALLOWED for recovery
            compile_file.write_text(
                json.dumps({
                    "distinct_compiles": 1,
                    "error_count": 2,
                    "has_syntax_error": True,
                    "last_errors": ["SyntaxError: invalid syntax line 1"],
                }),
                encoding="utf-8",
            )
            payload_syntax = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {
                        "Path": str(target_path),
                        "Content": target_content,
                    },
                },
            }
            res_syntax = process_hook(payload_syntax, custom_lock_file=str(self.lock_file))
            self.assertEqual(res_syntax.get("decision"), "allow")

    def test_rule_b_cta_post_pass_early_cut(self) -> None:
        """When pass_cta_{target_id}.json has PASS, writes and edits to CTA files are blocked."""
        cta_parts_dir = self.work_dir / "cta_parts"
        cta_parts_dir.mkdir(parents=True, exist_ok=True)
        part_py = cta_parts_dir / "part_01_data.py"
        part_py.write_text("# initial content\n", encoding="utf-8")

        # Create pass_cta_part_01.json
        pass_file = self.check_attempts_dir / "pass_cta_part_01.json"
        pass_file.write_text(json.dumps({"status": "PASS", "part_id": "part_01"}), encoding="utf-8")

        # write_file blocked
        payload_write = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {"Path": str(part_py), "Content": "# post-pass write"},
            },
        }
        res_write = process_hook(payload_write, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_write.get("decision"), "deny")
        self.assertIn("BLOCKER:: El módulo CTA part_01 ya aprobó todas las validaciones estrictas ([+] PASS)", res_write.get("reason", ""))
        self.assertIn("emite DONE inmediatamente", res_write.get("reason", ""))

        # edit_file blocked
        payload_edit = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "edit_file",
                "args": {"Path": str(part_py), "Target": "# initial", "Replacement": "# mod"},
            },
        }
        res_edit = process_hook(payload_edit, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_edit.get("decision"), "deny")
        self.assertIn("BLOCKER:: El módulo CTA part_01 ya aprobó todas las validaciones estrictas ([+] PASS)", res_edit.get("reason", ""))

    def test_rule_a_allows_cta_fixes_and_parts_whitelist(self) -> None:
        """Worker is allowed to write to cta_fixes and cta_parts while ad-hoc scripts are denied."""
        cta_paths = [
            "courses/demo_course/work/cta_fixes/C-01.py",
            "cta_fixes/C-02.py",
            "courses/demo_course/work/cta_parts/part_01_data.py",
            "courses/demo_course/work/cta_parts/part_02.py",
            "courses/demo_course/work/cta_parts/cta_fixes/C-03.py",
        ]

        for p in cta_paths:
            payload = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {"Path": p, "Content": "# legitimate cta file"},
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(res.get("decision"), "allow", f"Failed for {p}: {res}")

        # Ad-hoc script still blocked and references cta_fixes
        payload_bad = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {"Path": "courses/demo_course/work/adhoc_debug.py", "Content": "print(1)"},
            },
        }
        res_bad = process_hook(payload_bad, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_bad.get("decision"), "deny")
        self.assertIn("work/cta_fixes/<CID>.py", res_bad.get("reason", ""))

    def test_worker_denied_reading_tests_directory(self) -> None:
        """Worker is denied viewing tests/test_validator.py via view_file, grep_search, and shell commands."""
        # 1. view_file
        payload_view = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "view_file",
                "args": {"AbsolutePath": "tests/test_validator.py"},
            },
        }
        res_view = process_hook(payload_view, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_view.get("decision"), "deny")
        self.assertIn("Boundary", res_view.get("reason", ""))

        # 2. grep_search targeting tests
        payload_grep = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "grep_search",
                "args": {"query": "def test_", "path": "tests/test_validator.py"},
            },
        }
        res_grep = process_hook(payload_grep, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_grep.get("decision"), "deny")

        # 3. shell reading commands targeting tests/
        shell_cmds = [
            "Get-Content tests/test_validator.py",
            "type tests\\test_validator.py",
            "cat tests/test_validator.py",
            'python -c "open(\'tests/test_validator.py\').read()"',
        ]
        for cmd_str in shell_cmds:
            payload_cmd = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "run_command",
                    "args": {"CommandLine": cmd_str},
                },
            }
            res_cmd = process_hook(payload_cmd, custom_lock_file=str(self.lock_file))
            self.assertEqual(res_cmd.get("decision"), "deny", f"Failed to deny: {cmd_str}")

    def test_worker_denied_git_exploration_and_courses_listing(self) -> None:
        """Worker is denied running git exploration commands and listing general courses/."""
        # 1. Git exploration commands
        git_cmds = [
            "git log -n 5",
            "git status",
            "git diff HEAD~1",
            "git branch -a",
            "git show HEAD",
            "git grep search_term",
        ]
        for cmd_str in git_cmds:
            payload = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "run_command",
                    "args": {"CommandLine": cmd_str},
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(res.get("decision"), "deny", f"Failed for {cmd_str}")
            self.assertIn("Git exploration commands", res.get("reason", ""))

        # 2. Listing general courses/ or sibling courses
        denied_listings = [
            "Get-ChildItem -Path courses/ -Recurse",
            "Get-ChildItem courses",
            "dir courses\\",
            "ls courses/",
            "tree courses",
        ]
        for cmd_str in denied_listings:
            payload = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "run_command",
                    "args": {"CommandLine": cmd_str},
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(res.get("decision"), "deny", f"Failed for {cmd_str}")
            self.assertIn("Cross-Course Isolation", res.get("reason", ""))

        # 3. Listing within active course should be ALLOWED
        allowed_cmd = f"Get-ChildItem -Path courses/{self.course_id}/work"
        payload_allowed = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": allowed_cmd},
            },
        }
        res_allowed = process_hook(payload_allowed, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_allowed.get("decision"), "allow")

    # --------------------------------------------------------------------------
    # IMPROVER HARDENING: Windows Paths, error_count == 0, Corrupt JSON,
    # [M3-ARCHETYPES] Denial Messaging, and evaluate_hook_payload Benchmark
    # --------------------------------------------------------------------------

    def test_windows_backslashes_and_relative_paths_rules_a_b_c(self) -> None:
        r"""Windows backslashes (courses\c1\...) and relative paths normalize correctly across Rules A, B, and C."""
        cta_parts_dir = self.work_dir / "cta_parts"
        cta_fixes_dir = self.work_dir / "cta_fixes"
        cta_parts_dir.mkdir(parents=True, exist_ok=True)
        cta_fixes_dir.mkdir(parents=True, exist_ok=True)

        # 1. Rule A: writing to cta_fixes with Windows backslashes is ALLOWED
        win_cta_fix = rf"courses\{self.course_id}\work\cta_fixes\C-01.py"
        res_fix = evaluate_hook_payload(
            {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {"Path": win_cta_fix, "Content": "# win fix"},
                },
            },
            custom_lock_file=str(self.lock_file),
        )
        self.assertEqual(res_fix.get("decision"), "allow")

        # 2. Rule A: relative path with backslashes to cta_fixes is ALLOWED
        res_rel_fix = evaluate_hook_payload(
            {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {"Path": r"work\cta_fixes\C-01.py", "Content": "# rel fix"},
                },
            },
            custom_lock_file=str(self.lock_file),
        )
        self.assertEqual(res_rel_fix.get("decision"), "allow")

        # 3. Rule B: post-PASS with Windows backslashes is BLOCKED on shard and CTA
        shard_py = self.shards_dir / "shard_01_data.py"
        shard_py.write_text("# shard content\n", encoding="utf-8")
        pass_shard = self.check_attempts_dir / "pass_shard_01.json"
        pass_shard.write_text(json.dumps({"status": "PASS"}), encoding="utf-8")

        win_shard_path = rf"courses\{self.course_id}\work\shards\shard_01_data.py"
        res_win_pass_shard = evaluate_hook_payload(
            {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {"Path": win_shard_path, "Content": "# post pass"},
                },
            },
            custom_lock_file=str(self.lock_file),
        )
        self.assertEqual(res_win_pass_shard.get("decision"), "deny")
        self.assertIn("BLOCKER:: El shard shard_01 ya aprobó", res_win_pass_shard.get("reason", ""))

        # 4. Rule B: post-PASS with Windows backslashes on CTA part
        part_py = cta_parts_dir / "part_01_data.py"
        part_py.write_text("# cta part content\n", encoding="utf-8")
        pass_cta = self.check_attempts_dir / "pass_cta_part_01.json"
        pass_cta.write_text(json.dumps({"status": "PASS"}), encoding="utf-8")

        win_part_path = rf"courses\{self.course_id}\work\cta_parts\part_01_data.py"
        res_win_pass_cta = evaluate_hook_payload(
            {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {"Path": win_part_path, "Content": "# post pass"},
                },
            },
            custom_lock_file=str(self.lock_file),
        )
        self.assertEqual(res_win_pass_cta.get("decision"), "deny")
        self.assertIn("BLOCKER:: El módulo CTA part_01 ya aprobó", res_win_pass_cta.get("reason", ""))

        # 5. Rule C: error_count < 6 with Windows backslashes blocks write_file
        pass_shard.unlink()  # remove pass file so Rule C is evaluated
        compile_shard = self.check_attempts_dir / "compile_shard_01.json"
        compile_shard.write_text(
            json.dumps({"distinct_compiles": 1, "error_count": 3, "last_errors": ["err1", "err2", "err3"]}),
            encoding="utf-8",
        )
        shard_py.write_text("".join([f"# Line {i}\n" for i in range(100)]), encoding="utf-8")

        res_win_rule_c = evaluate_hook_payload(
            {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {"Path": win_shard_path, "Content": "# rewrite"},
                },
            },
            custom_lock_file=str(self.lock_file),
        )
        self.assertEqual(res_win_rule_c.get("decision"), "deny")
        self.assertIn("registra 3 errores (< 6, umbral oficial)", res_win_rule_c.get("reason", ""))

    def test_rule_c_error_count_zero_and_none_safe_legacy_fallback(self) -> None:
        """error_count == 0 or error_count is None safely falls back to legacy (>250 lines deny, <=250 lines allow)."""
        shard_py = self.shards_dir / "shard_01_data.py"
        compile_file = self.check_attempts_dir / "compile_shard_01.json"

        # Case A: error_count == 0 with small shard (100 lines <= 250) -> ALLOW write_file
        small_content = "".join([f"# Line {i}\n" for i in range(100)])
        shard_py.write_text(small_content, encoding="utf-8")
        compile_file.write_text(
            json.dumps({"distinct_compiles": 1, "error_count": 0, "last_errors": []}),
            encoding="utf-8",
        )
        res_small_0 = evaluate_hook_payload(
            {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {"Path": str(shard_py), "Content": small_content},
                },
            },
            custom_lock_file=str(self.lock_file),
        )
        self.assertEqual(res_small_0.get("decision"), "allow", f"Expected allow for error_count=0 on 100 lines: {res_small_0}")

        # Case B: error_count == 0 with large shard (300 lines > 250) -> DENY write_file (legacy fallback)
        large_content = "".join([f"# Line {i}\n" for i in range(300)])
        shard_py.write_text(large_content, encoding="utf-8")
        res_large_0 = evaluate_hook_payload(
            {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {"Path": str(shard_py), "Content": large_content},
                },
            },
            custom_lock_file=str(self.lock_file),
        )
        self.assertEqual(res_large_0.get("decision"), "deny")
        self.assertIn("supera las 250 líneas", res_large_0.get("reason", ""))

        # Case C: error_count is None with small shard (100 lines <= 250) -> ALLOW write_file
        shard_py.write_text(small_content, encoding="utf-8")
        compile_file.write_text(
            json.dumps({"distinct_compiles": 1, "last_err_hash": "hash_abc"}),  # error_count omitted
            encoding="utf-8",
        )
        res_small_none = evaluate_hook_payload(
            {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {"Path": str(shard_py), "Content": small_content},
                },
            },
            custom_lock_file=str(self.lock_file),
        )
        self.assertEqual(res_small_none.get("decision"), "allow")

        # Case D: error_count is None with large shard (300 lines > 250) -> DENY write_file (legacy fallback)
        shard_py.write_text(large_content, encoding="utf-8")
        res_large_none = evaluate_hook_payload(
            {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {"Path": str(shard_py), "Content": large_content},
                },
            },
            custom_lock_file=str(self.lock_file),
        )
        self.assertEqual(res_large_none.get("decision"), "deny")
        self.assertIn("supera las 250 líneas", res_large_none.get("reason", ""))

    def test_rule_c_corrupt_json_in_check_attempts_fail_safe_without_exception(self) -> None:
        """Corrupt JSON in .check_attempts/compile_shard_01.json or compile_cta.json falls back safely without unhandled exception."""
        shard_py = self.shards_dir / "shard_01_data.py"
        small_content = "".join([f"# Line {i}\n" for i in range(80)])
        shard_py.write_text(small_content, encoding="utf-8")

        # Corrupted compile file with truncated/invalid JSON
        compile_file = self.check_attempts_dir / "compile_shard_01.json"
        compile_file.write_text("{\"error_count\": 2, \"broken_json: ...", encoding="utf-8")

        # Must not raise an unhandled JSONDecodeError and must fall back safely (allow for small shard)
        payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {"Path": str(shard_py), "Content": small_content},
            },
        }
        res = evaluate_hook_payload(payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res.get("decision"), "allow")

        # Empty compile file
        compile_file.write_text("", encoding="utf-8")
        res_empty = evaluate_hook_payload(payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_empty.get("decision"), "allow")

        # CTA compile file corrupted
        cta_data_py = self.work_dir / "cta_data.py"
        cta_data_py.write_text("# cta data\n", encoding="utf-8")
        compile_cta = self.check_attempts_dir / "compile_cta.json"
        compile_cta.write_text("{bad cta json", encoding="utf-8")

        payload_cta = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {"Path": str(cta_data_py), "Content": "# new cta"},
            },
        }
        res_cta = evaluate_hook_payload(payload_cta, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_cta.get("decision"), "allow")

    def test_rule_c_m3_archetypes_denial_message_guidance(self) -> None:
        """Small shard (1-2 competencies, ~75-120 lines) with [M3-ARCHETYPES] (error_count 1-2) gets clear denial guidance."""
        shard_py = self.shards_dir / "shard_01_data.py"
        # 1-2 competencies emitting only 1 archetype per competence (~85 lines)
        short_shard_content = "".join([f"# Archetype template code line {i}\n" for i in range(85)])
        shard_py.write_text(short_shard_content, encoding="utf-8")

        # Compiler reports [M3-ARCHETYPES] missing archetype tuple (error_count = 1 or 2)
        for err_cnt in (1, 2):
            compile_file = self.check_attempts_dir / "compile_shard_01.json"
            compile_file.write_text(
                json.dumps({
                    "distinct_compiles": 1,
                    "error_count": err_cnt,
                    "last_errors": ["[M3-ARCHETYPES] Competence C1 has only 1 archetype; minimum is 2."],
                }),
                encoding="utf-8",
            )

            # write_file rewrite is BLOCKED
            payload_write = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {"Path": str(shard_py), "Content": short_shard_content},
                },
            }
            res_write = evaluate_hook_payload(payload_write, custom_lock_file=str(self.lock_file))
            self.assertEqual(res_write.get("decision"), "deny")
            # Verify ultra-clear guidance on TEMPLATES and [M3-ARCHETYPES]
            reason = res_write.get("reason", "")
            self.assertIn(f"registra {err_cnt} errores (< 6, umbral oficial)", reason)
            self.assertIn("edit_file", reason)
            self.assertIn("TEMPLATES", reason)
            self.assertIn("[M3-ARCHETYPES]", reason)
            self.assertIn("work/shards/shard_fixes/<CID>.py", reason)

            # edit_file surgical addition is ALLOWED
            payload_edit = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "edit_file",
                    "args": {
                        "Path": str(shard_py),
                        "Target": "# Archetype template code line 10\n",
                        "Replacement": "# Archetype template code line 10\n# Archetype 2 tuple added\n",
                    },
                },
            }
            res_edit = evaluate_hook_payload(payload_edit, custom_lock_file=str(self.lock_file))
            self.assertEqual(res_edit.get("decision"), "allow")

            # writing modular fix in shard_fixes/<CID>.py is ALLOWED
            payload_fix = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "write_file",
                    "args": {
                        "Path": str(self.shard_fixes_dir / "C1.py"),
                        "Content": "# modular archetype fix\nTEMPLATES = [('arch2', ...)]\n",
                    },
                },
            }
            res_fix = evaluate_hook_payload(payload_fix, custom_lock_file=str(self.lock_file))
            self.assertEqual(res_fix.get("decision"), "allow")

    def test_evaluate_hook_payload_benchmark_under_10ms_latency(self) -> None:
        """Benchmark: 50 consecutive invocations of evaluate_hook_payload achieve average latency < 10ms (SLA target < 5ms)."""
        import time

        payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {
                    "Path": str(self.shards_dir / "shard_99_data.py"),
                    "Content": "# new shard content\n",
                },
            },
        }

        # Warm up 5 calls
        for _ in range(5):
            evaluate_hook_payload(payload, custom_lock_file=str(self.lock_file))

        latencies_ms: List[float] = []
        for _ in range(50):
            t0 = time.perf_counter()
            res = evaluate_hook_payload(payload, custom_lock_file=str(self.lock_file))
            lat = (time.perf_counter() - t0) * 1000.0
            latencies_ms.append(lat)
            self.assertEqual(res.get("decision"), "allow")

        avg_latency = sum(latencies_ms) / len(latencies_ms)
        max_latency = max(latencies_ms)

        self.assertLess(
            avg_latency,
            10.0,
            f"Average latency {avg_latency:.2f}ms exceeded SLA threshold of 10.0ms",
        )
        self.assertLess(
            avg_latency,
            5.0,
            f"Average latency {avg_latency:.2f}ms exceeded high-performance target of 5.0ms",
        )
        self.assertLess(
            max_latency,
            25.0,
            f"Max latency {max_latency:.2f}ms exceeded SLA threshold of 25.0ms",
        )


if __name__ == "__main__":
    unittest.main()
