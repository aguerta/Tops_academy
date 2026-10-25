"""Tests for C2C v3.3 Budget Watchdog & Lifecycle Hooks Guard (Stream 1D).

Covers:
1. Fast pass-through (< 50ms) when outside active C2C runs or lock is stale (> 2h).
2. Worker subagent denied reading compiler/validator source, .check_attempts, ground truth,
   and denied nested-quote python -c, while allowed reading content/dispatch and writing shard data.
3. Director denied reading/editing worker data files (*_data.py, shard_fixes/*.py, judge_responses*.json),
   while allowed reading state.json, judge_report.json, and running commands.
4. Invoking command from .agents/hooks.template.json via subprocess with cwd = .agents/ succeeds with exit 0.
5. Budget watchdog parsing Antigravity real brain transcript (108 PLANNER_RESPONSE turns, >5M tokens,
   tool script loop), flagging runaway, and generating modular shard_fixes repair order with next_schedule_seconds: 300.
6. Cumulative token estimator flagging >100-turn compact transcripts for >5M tokens.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / ".agents" / "skills" / "content-to-course"))

from budget_guard import (  # noqa: E402
    DEFAULT_MAX_SCRIPT_LOOPS,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MAX_TURNS,
    SubagentMetrics,
    SubagentWatchdogReport,
    evaluate_watchdog_rules,
    generate_repair_redispatch,
    identify_unfinished_competencies,
    parse_transcript,
    resolve_brain_transcript,
    scan_work_transcripts,
)
from c2c_hook_guard import (  # noqa: E402
    find_active_c2c_lock,
    process_hook,
)


class TestLifecycleHookGuard(unittest.TestCase):
    """Verifies PreToolUse hook enforcement in c2c_hook_guard.py."""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="c2c_hook_test_")
        self.lock_file = Path(self.test_dir) / ".c2c_subagent_lock.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_fast_passthrough_when_no_active_lock(self) -> None:
        """When no active lock exists, hook evaluates in < 50ms and allows tool calls."""
        payload = {
            "conversationId": "subagent-1",
            "toolCall": {
                "name": "view_file",
                "args": {"AbsolutePath": "compile_shard.py"},
            },
        }
        start = time.perf_counter()
        # Non-existent lockfile
        res = process_hook(payload, custom_lock_file=str(self.lock_file))
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        self.assertEqual(res.get("decision"), "allow")
        self.assertLess(elapsed_ms, 50.0)

    def test_passthrough_when_lock_is_stale_or_inactive(self) -> None:
        """Stale locks (> 2h) or inactive locks allow tool calls."""
        # Inactive lock
        self.lock_file.write_text(
            json.dumps({"active": False, "director_conversation_id": "dir-1"}),
            encoding="utf-8",
        )
        res = process_hook({"conversationId": "sub-1"}, custom_lock_file=str(self.lock_file))
        self.assertEqual(res.get("decision"), "allow")

        # Stale lock (> 7200 seconds old)
        self.lock_file.write_text(
            json.dumps({"active": True, "director_conversation_id": "dir-1"}),
            encoding="utf-8",
        )
        stale_time = time.time() - 8000
        os.utime(str(self.lock_file), (stale_time, stale_time))
        res_stale = process_hook({"conversationId": "sub-1"}, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_stale.get("decision"), "allow")

    def test_worker_denied_reading_compiler_engine_and_truth(self) -> None:
        """Worker is denied viewing/reading compiler source, engine, ground truth, and check_attempts."""
        self.lock_file.write_text(
            json.dumps({
                "active": True,
                "director_conversation_id": "director-conv-id",
                "work_dir": "courses/mycourse/work",
            }),
            encoding="utf-8",
        )

        forbidden_reads = [
            ".agents/skills/content-to-course/compile_shard.py",
            "check_templates.py",
            "compile_cta.py",
            "check_cta.py",
            "engine/assemble.py",
            "/engine/templates.py",
            "validator/schema.py",
            "src/validator/rule_checker.py",
            ".check_attempts/shard_01.json",
            "courses/mycourse/work/verification/judge_ground_truth.json",
            "SKILL.md",
        ]

        for target in forbidden_reads:
            payload = {
                "conversationId": "worker-subagent-01",
                "toolCall": {
                    "name": "view_file",
                    "args": {"AbsolutePath": target},
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(
                res.get("decision"),
                "deny",
                f"Expected deny for worker reading {target}, got: {res}",
            )
            self.assertIn("Boundary", res.get("reason", ""))

    def test_worker_denied_modifying_skills_and_check_attempts(self) -> None:
        """Worker is denied modifying .check_attempts or .agents/skills/."""
        self.lock_file.write_text(
            json.dumps({
                "active": True,
                "director_conversation_id": "director-conv-id",
            }),
            encoding="utf-8",
        )

        forbidden_writes = [
            ".check_attempts/shard_01.json",
            ".agents/skills/content-to-course/c2c_hook_guard.py",
            "skills/content-to-course/budget_guard.py",
        ]

        for target in forbidden_writes:
            payload = {
                "conversationId": "worker-subagent-01",
                "toolCall": {
                    "name": "write_file",
                    "args": {"Path": target, "Content": "tampered"},
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(
                res.get("decision"),
                "deny",
                f"Expected deny for worker writing {target}, got: {res}",
            )

    def test_worker_denied_deleting_check_attempts_and_nested_quote_python_c(self) -> None:
        """Worker is denied deleting .check_attempts and running complex nested-quote python -c."""
        self.lock_file.write_text(
            json.dumps({
                "active": True,
                "director_conversation_id": "director-conv-id",
            }),
            encoding="utf-8",
        )

        # 1. rm .check_attempts
        cmd_del = {
            "conversationId": "worker-subagent-01",
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": "rm -rf .check_attempts/shard_01.json"},
            },
        }
        res_del = process_hook(cmd_del, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_del.get("decision"), "deny")

        # 2. python -c with escaped quotes
        cmd_nested = {
            "conversationId": "worker-subagent-01",
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": r'python -c "import os; print(\"escaped\")"'},
            },
        }
        res_nested = process_hook(cmd_nested, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_nested.get("decision"), "deny")
        self.assertIn("Complex nested-quote", res_nested.get("reason", ""))

        # 3. python -c length > 120 chars
        long_code = "a" * 130
        cmd_long = {
            "conversationId": "worker-subagent-01",
            "toolCall": {
                "name": "run_command",
                "args": {"CommandLine": f'python -c "{long_code}"'},
            },
        }
        res_long = process_hook(cmd_long, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_long.get("decision"), "deny")

    def test_worker_allowed_safe_operations(self) -> None:
        """Worker is allowed reading content PDFs, dispatch items, and writing shard data/fixes."""
        self.lock_file.write_text(
            json.dumps({
                "active": True,
                "director_conversation_id": "director-conv-id",
            }),
            encoding="utf-8",
        )

        allowed_cases = [
            ("view_file", {"AbsolutePath": "content/econometrics.pdf"}),
            ("view_file", {"AbsolutePath": "work/dispatch/items/author_01.json"}),
            ("write_file", {"Path": "work/shards/shard_01_data.py", "Content": "# data"}),
            ("edit_file", {"Path": "work/shards/shard_fixes/Hab-03.py", "Replacement": "# fix"}),
            ("run_command", {"CommandLine": "python compile_shard.py --shard shard_01"}),
        ]

        for tool_name, args in allowed_cases:
            payload = {
                "conversationId": "worker-subagent-01",
                "toolCall": {
                    "name": tool_name,
                    "args": args,
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(
                res.get("decision"),
                "allow",
                f"Expected allow for worker operation {tool_name} {args}, got: {res}",
            )

    def test_director_context_diet_enforcement(self) -> None:
        """Director is denied viewing/editing worker *_data.py, shard_fixes/*.py, judge_responses*.json."""
        director_id = "director-conv-id-999"
        self.lock_file.write_text(
            json.dumps({
                "active": True,
                "director_conversation_id": director_id,
            }),
            encoding="utf-8",
        )

        # Denied targets for Director
        denied_targets = [
            "courses/econ/work/shards/shard_06_data.py",
            "work/cta_data.py",
            "work/shards/shard_fixes/Hab-03.py",
            "work/verification/judge_responses_01.json",
            ".agents/skills/content-to-course/run.py",
            ".agents/skills/content-to-course/dispatch.py",
        ]

        for target in denied_targets:
            for tool in ("view_file", "edit_file", "write_file"):
                payload = {
                    "conversationId": director_id,
                    "toolCall": {
                        "name": tool,
                        "args": {"Path": target},
                    },
                }
                res = process_hook(payload, custom_lock_file=str(self.lock_file))
                self.assertEqual(
                    res.get("decision"),
                    "deny",
                    f"Director should be denied {tool} on {target}",
                )
                self.assertIn("Director Diet", res.get("reason", ""))

        # Allowed targets for Director (compact manifests, reports, SKILL.md, commands)
        allowed_cases = [
            ("view_file", {"Path": ".agents/skills/content-to-course/SKILL.md"}),
            ("view_file", {"Path": "work/state.json"}),
            ("view_file", {"Path": "work/judge_report.json"}),
            ("view_file", {"Path": "work/dispatch/types/author.json"}),
            ("view_file", {"Path": "work/dispatch/items/author_01.json"}),
            ("run_command", {"CommandLine": "python .agents/skills/content-to-course/dispatch.py --role author"}),
        ]

        for tool, args in allowed_cases:
            payload = {
                "conversationId": director_id,
                "toolCall": {
                    "name": tool,
                    "args": args,
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(
                res.get("decision"),
                "allow",
                f"Director should be allowed {tool} on {args}",
            )

    def test_pre_bootstrap_fast_start_guard(self) -> None:
        """Even before .c2c_subagent_lock.json exists, Fast-Start Guard blocks C2C script exploration and manual PDF page counting."""
        denied_cmds = [
            '& ".venv\\Scripts\\python.exe" .agents/skills/content-to-course/run.py --help',
            '& ".venv\\Scripts\\python.exe" -c "with open(\'.agents/skills/content-to-course/run.py\') as f: print(f.read())"',
            '& ".venv\\Scripts\\python.exe" -c "import pypdf; r = pypdf.PdfReader(\'content/estadistica_asintotica/S1.pdf\')"',
            '& ".venv\\Scripts\\python.exe" -c "import fitz; doc = fitz.open(\'content/estadistica_asintotica/S1.pdf\')"',
        ]
        for cmd_str in denied_cmds:
            payload = {
                "conversationId": "new-director-conv",
                "toolCall": {
                    "name": "run_command",
                    "args": {"CommandLine": cmd_str},
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(
                res.get("decision"),
                "deny",
                f"Expected Fast-Start Guard deny for pre-bootstrap command: {cmd_str}",
            )
            self.assertIn("Fast-Start Guard", res.get("reason", ""))

    def test_hooks_template_json_structure_and_cwd_execution(self) -> None:
        """Verifies .agents/hooks.template.json schema and subprocess run with cwd = .agents/."""
        template_path = REPO_ROOT / ".agents" / "hooks.template.json"
        self.assertTrue(template_path.is_file(), f"Missing template: {template_path}")

        template_data = json.loads(template_path.read_text(encoding="utf-8"))
        live_hooks = REPO_ROOT / ".agents" / "hooks.json"
        if live_hooks.is_file():
            self.assertEqual(
                json.loads(live_hooks.read_text(encoding="utf-8")),
                template_data,
                ".agents/hooks.json must match .agents/hooks.template.json",
            )
        guard_key = next(iter(template_data.keys()))
        pre_tool_use = template_data[guard_key]["PreToolUse"][0]

        self.assertIn("read_file", pre_tool_use["matcher"])
        self.assertIn("run_command", pre_tool_use["matcher"])

        hook_spec = pre_tool_use["hooks"][0]
        cmd_str = hook_spec["command"]
        self.assertEqual(cmd_str, "python skills/content-to-course/c2c_hook_guard.py")

        # Explicit subprocess test with cwd = repo_root / ".agents"
        # We test running python script via sys.executable
        agents_dir = REPO_ROOT / ".agents"
        script_rel = "skills/content-to-course/c2c_hook_guard.py"
        self.assertTrue((agents_dir / script_rel).is_file())

        test_payload = {
            "conversationId": "subagent-cwd-test",
            "toolCall": {
                "name": "view_file",
                "args": {"AbsolutePath": "content/sample.pdf"},
            },
        }

        proc = subprocess.run(
            [sys.executable, script_rel],
            cwd=str(agents_dir),
            input=json.dumps(test_payload),
            capture_output=True,
            text=True,
            timeout=10,
        )

        self.assertEqual(proc.returncode, 0, f"Hook exited with non-zero code: {proc.stderr}")
        stdout_data = json.loads(proc.stdout.strip())
        self.assertEqual(stdout_data.get("decision"), "allow")

    def test_worker_denied_powershell_and_shell_read_commands(self) -> None:
        """Worker is denied attempting to read protected compiler/truth files via shell commands."""
        self.lock_file.write_text(
            json.dumps({
                "active": True,
                "director_conversation_id": "director-conv-id",
            }),
            encoding="utf-8",
        )

        forbidden_cmds = [
            "Get-Content compile_shard.py",
            "Get-Content .\\.agents\\skills\\content-to-course\\compile_shard.py",
            "gc check_templates.py",
            "type courses/econ/work/verification/judge_ground_truth.json",
            "type judge_ground_truth.json",
            "cat .check_attempts/shard_01.json",
            'Select-String "def" check_templates.py',
            'grep "def" compile_shard.py',
            "more compile_shard.py",
            "head -n 20 compile_shard.py",
            'python -c "print(open(\'compile_shard.py\').read())"',
            'powershell -Command "Get-Content compile_shard.py"',
            "[System.IO.File]::ReadAllText('compile_shard.py')",
            "Copy-Item compile_shard.py scratch.py",
            "cp compile_shard.py scratch.py",
        ]

        for cmd in forbidden_cmds:
            payload = {
                "conversationId": "worker-subagent-01",
                "toolCall": {
                    "name": "run_command",
                    "args": {"CommandLine": cmd},
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(
                res.get("decision"),
                "deny",
                f"Expected deny for command: '{cmd}', but got: {res}",
            )
            self.assertIn("Boundary", res.get("reason", ""))

    def test_worker_allowed_compiler_execution_commands(self) -> None:
        """Worker is allowed executing official compiler and checking commands."""
        self.lock_file.write_text(
            json.dumps({
                "active": True,
                "director_conversation_id": "director-conv-id",
            }),
            encoding="utf-8",
        )

        allowed_cmds = [
            "python compile_shard.py --shard shard_01",
            "python .agents/skills/content-to-course/compile_shard.py --work work --shard shard_01 --type standard",
            '& "d:\\Augusto\\.venv\\Scripts\\python.exe" compile_shard.py --shard shard_01',
            "python check_templates.py --work work",
            "python compile_cta.py --input work/cta_data.py --output work/cta.json",
        ]

        for cmd in allowed_cmds:
            payload = {
                "conversationId": "worker-subagent-01",
                "toolCall": {
                    "name": "run_command",
                    "args": {"CommandLine": cmd},
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(
                res.get("decision"),
                "allow",
                f"Expected allow for compiler execution command: '{cmd}', but got: {res}",
            )

    def test_windows_path_normalization_and_traversal_safety(self) -> None:
        """Verifies mixed backslashes, leading ./, traversal ../, casing, and URL encoding."""
        self.lock_file.write_text(
            json.dumps({
                "active": True,
                "director_conversation_id": "director-conv-id",
            }),
            encoding="utf-8",
        )

        evasion_paths = [
            "D:\\Augusto\\Personal_Portfolio\\Tops_Academy\\.agents\\skills\\content-to-course\\compile_shard.py",
            ".\\.agents\\skills\\content-to-course\\compile_shard.py",
            "..\\.check_attempts\\shard_01.json",
            "compile%5Fshard.py",
            "COMPILE_SHARD.PY",
            "file:///d:/Augusto/personal_portfolio/Tops_academy/compile_shard.py",
            "courses/econ/work/verification/judge%5Fground%5Ftruth.json",
        ]

        for p in evasion_paths:
            payload = {
                "conversationId": "worker-subagent-01",
                "toolCall": {
                    "name": "view_file",
                    "args": {"AbsolutePath": p},
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(
                res.get("decision"),
                "deny",
                f"Expected deny for evasion path: '{p}', but got: {res}",
            )

    def test_worker_denied_modifying_compiler_and_engine(self) -> None:
        """Worker is denied write_file or edit_file on compiler, validator, and engine files."""
        self.lock_file.write_text(
            json.dumps({
                "active": True,
                "director_conversation_id": "director-conv-id",
            }),
            encoding="utf-8",
        )

        forbidden_modifications = [
            ("write_file", {"Path": "compile_shard.py", "Content": "# hacked"}),
            ("edit_file", {"Path": "check_templates.py", "Replacement": "# hacked", "Target": "pass"}),
            ("write_file", {"Path": "skills/content-to-course/engine/assemble.py", "Content": "# hacked"}),
            ("edit_file", {"Path": "validator/schema.py", "Replacement": "# hacked", "Target": "def"}),
        ]

        for tool, args in forbidden_modifications:
            payload = {
                "conversationId": "worker-subagent-01",
                "toolCall": {
                    "name": tool,
                    "args": args,
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(
                res.get("decision"),
                "deny",
                f"Expected deny for worker modifying compiler/engine: {tool} on {args}",
            )

    def test_auditor_exemption_in_lockfile(self) -> None:
        """Auditor conversation IDs listed in exempt_conversation_ids bypass all restrictions."""
        auditor_id = "auditor-agent-uuid-777"
        self.lock_file.write_text(
            json.dumps({
                "active": True,
                "director_conversation_id": "director-conv-id",
                "exempt_conversation_ids": [auditor_id, "qa-reviewer-01"],
            }),
            encoding="utf-8",
        )

        # Auditor allowed reading worker data files (normally denied to Director)
        payload_auditor_data = {
            "conversationId": auditor_id,
            "toolCall": {
                "name": "view_file",
                "args": {"AbsolutePath": "work/shards/shard_01_data.py"},
            },
        }
        res_data = process_hook(payload_auditor_data, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_data.get("decision"), "allow")

        # Auditor allowed inspecting compiler files (normally denied to Worker)
        payload_auditor_comp = {
            "conversationId": auditor_id,
            "toolCall": {
                "name": "view_file",
                "args": {"AbsolutePath": "compile_shard.py"},
            },
        }
        res_comp = process_hook(payload_auditor_comp, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_comp.get("decision"), "allow")

        # Non-exempt caller remains denied
        payload_non_exempt = {
            "conversationId": "ordinary-worker-01",
            "toolCall": {
                "name": "view_file",
                "args": {"AbsolutePath": "compile_shard.py"},
            },
        }
        res_non_exempt = process_hook(payload_non_exempt, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_non_exempt.get("decision"), "deny")

    def test_docs_hooks_contract_schema_and_variations(self) -> None:
        """Verifies PreToolUse stdin/stdout schema adherence against docs/hooks.md."""
        self.lock_file.write_text(
            json.dumps({
                "active": True,
                "director_conversation_id": "dir-123",
            }),
            encoding="utf-8",
        )

        # Exact camelCase format from docs/hooks.md
        docs_payload = {
            "conversationId": "dir-123",
            "stepIdx": 5,
            "workspacePaths": ["/workspace"],
            "toolCall": {
                "name": "view_file",
                "args": {
                    "AbsolutePath": "work/dispatch/items/author_01.json",
                },
            },
        }
        res = process_hook(docs_payload, custom_lock_file=str(self.lock_file))
        self.assertIn("decision", res)
        self.assertIn(res["decision"], ("allow", "deny", "ask", "force_ask"))
        self.assertEqual(res["decision"], "allow")

        # Variations in field names (snake_case)
        snake_payload = {
            "conversation_id": "worker-sub-1",
            "step_index": 7,
            "tool_call": {
                "tool_name": "view_file",
                "tool_input": {
                    "file_path": "compile_shard.py",
                },
            },
        }
        res_snake = process_hook(snake_payload, custom_lock_file=str(self.lock_file))
        self.assertEqual(res_snake.get("decision"), "deny")

    def test_hook_guard_performance_benchmark(self) -> None:
        """Benchmark: 1,000 process_hook evaluations complete in < 250ms (< 0.25ms per call)."""
        self.lock_file.write_text(
            json.dumps({
                "active": True,
                "director_conversation_id": "director-bench",
            }),
            encoding="utf-8",
        )
        payload = {
            "conversationId": "worker-bench",
            "toolCall": {
                "name": "view_file",
                "args": {"AbsolutePath": "content/econometrics.pdf"},
            },
        }

        start = time.perf_counter()
        for _ in range(1000):
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            if res.get("decision") != "allow":
                break
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        self.assertLess(elapsed_ms, 250.0, f"1000 evaluations took {elapsed_ms:.1f}ms (expected < 250ms)")

    def test_cli_subprocess_stdin_stdout_robustness(self) -> None:
        """Invoking c2c_hook_guard.py via CLI with malformed, empty, allow, or deny input always exits code 0."""
        agents_dir = REPO_ROOT / ".agents"
        script_rel = "skills/content-to-course/c2c_hook_guard.py"

        # 1. Empty stdin -> allow
        proc_empty = subprocess.run(
            [sys.executable, script_rel],
            cwd=str(agents_dir),
            input="",
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(proc_empty.returncode, 0)
        self.assertEqual(json.loads(proc_empty.stdout.strip()).get("decision"), "allow")

        # 2. Malformed non-JSON stdin -> fail-open allow
        proc_bad = subprocess.run(
            [sys.executable, script_rel],
            cwd=str(agents_dir),
            input="NOT_A_VALID_JSON{{{",
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(proc_bad.returncode, 0)
        self.assertEqual(json.loads(proc_bad.stdout.strip()).get("decision"), "allow")

    def test_director_allowed_logs_and_dispatch_types(self) -> None:
        """Director is explicitly allowed reading logs, dispatch types, and dispatch items."""
        director_id = "director-conv-id-log-test"
        self.lock_file.write_text(
            json.dumps({
                "active": True,
                "director_conversation_id": director_id,
            }),
            encoding="utf-8",
        )

        allowed_director_reads = [
            "work/logs/director.log",
            "work/logs/run.log",
            "work/dispatch/types/author.json",
            "work/dispatch/items/watchdog_repair_01.json",
            "courses/econ/work/dispatch/subagent_types.json",
        ]

        for p in allowed_director_reads:
            payload = {
                "conversationId": director_id,
                "toolCall": {
                    "name": "view_file",
                    "args": {"AbsolutePath": p},
                },
            }
            res = process_hook(payload, custom_lock_file=str(self.lock_file))
            self.assertEqual(
                res.get("decision"),
                "allow",
                f"Director should be allowed to view {p}, got: {res}",
            )


class TestBudgetWatchdogBrainAndRedispatch(unittest.TestCase):
    """Verifies R5 Budget Watchdog transcript resolution, parsing, and redispatch."""

    def setUp(self) -> None:
        self.test_dir = tempfile.mkdtemp(prefix="c2c_watchdog_brain_test_")
        self.work_dir = Path(self.test_dir) / "work"
        self.work_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_resolve_brain_transcript_with_app_data_dir(self) -> None:
        """Resolves subagent transcript located in <appDataDir>/brain/<id>/.system_generated/logs/."""
        subagent_id = "test-subagent-uuid-1234"
        brain_log_dir = Path(self.test_dir) / "brain" / subagent_id / ".system_generated" / "logs"
        brain_log_dir.mkdir(parents=True, exist_ok=True)
        t_file = brain_log_dir / "transcript.jsonl"
        t_file.write_text('{"source":"MODEL","type":"PLANNER_RESPONSE","input_tokens":100}\n', encoding="utf-8")

        resolved = resolve_brain_transcript(subagent_id, app_data_dir=self.test_dir)
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved.resolve(), t_file.resolve())

    def test_parse_real_antigravity_brain_transcript_108_turns(self) -> None:
        """Parses real Antigravity transcript (or synthetic equivalent) with 108 PLANNER_RESPONSE turns."""
        real_transcript_path = Path("C:/Users/augus/.gemini/antigravity/brain/b9bc17ec-092d-4d5d-80b6-428307c2143b/.system_generated/logs/transcript.jsonl")

        if real_transcript_path.is_file():
            target_path = real_transcript_path
        else:
            # Build synthetic 108-turn transcript modeling shard_06
            synth_file = self.work_dir / "synthetic_transcript.jsonl"
            lines = [
                json.dumps({
                    "step_index": 0,
                    "source": "SYSTEM",
                    "type": "SYSTEM_MESSAGE",
                    "content": "You are Shard Author shard_06. Your work order is work/dispatch/items/author_01.json.",
                })
            ]
            for i in range(1, 109):
                lines.append(json.dumps({
                    "step_index": i * 2 - 1,
                    "source": "MODEL",
                    "type": "PLANNER_RESPONSE",
                    "input_tokens": 10000,
                    "cache_read_tokens": 50000,
                    "output_tokens": 500,
                    "tool_calls": [{"name": "run_command", "args": {"CommandLine": "python compile_shard.py"}}],
                }))
                lines.append(json.dumps({
                    "step_index": i * 2,
                    "source": "MODEL",
                    "type": "GENERIC",
                    "content": "Compilation error line 5",
                    "exit_code": 1,
                }))
            synth_file.write_text("\n".join(lines), encoding="utf-8")
            target_path = synth_file

        metrics = parse_transcript(target_path)
        self.assertEqual(metrics.turn_count, 108)
        self.assertGreater(metrics.total_tokens, 5_000_000)
        self.assertEqual(metrics.unit_id, "shard_06")

        report = evaluate_watchdog_rules(metrics)
        self.assertTrue(report.is_runaway)
        self.assertEqual(report.recommended_action, "kill_and_redispatch")
        self.assertTrue(any("Turn limit exceeded" in r for r in report.runaway_reasons))
        self.assertTrue(any("Token burn limit exceeded" in r for r in report.runaway_reasons))
        self.assertTrue(any("Script loop detected" in r for r in report.runaway_reasons))

    def test_cumulative_context_token_estimator_on_compact_transcript(self) -> None:
        """When transcript omits explicit tokens, cumulative estimator flags >100 turns for >5M tokens."""
        t_file = self.work_dir / "compact_100_turns.jsonl"
        lines = []
        for i in range(100):
            lines.append(json.dumps({
                "type": "PLANNER_RESPONSE",
                "content": f"Turn {i} without explicit token fields",
            }))
        t_file.write_text("\n".join(lines), encoding="utf-8")

        metrics = parse_transcript(t_file)
        self.assertEqual(metrics.turn_count, 100)
        # > 5M tokens estimated
        self.assertGreater(metrics.total_tokens, 5_000_000)
        self.assertGreater(metrics.cached_tokens, 5_000_000)

        report = evaluate_watchdog_rules(metrics)
        self.assertTrue(report.is_runaway)
        self.assertTrue(any("Token burn limit exceeded" in r for r in report.runaway_reasons))

    def test_generate_repair_redispatch_with_modular_shard_fixes_and_schedule(self) -> None:
        """generate_repair_redispatch instructs modular shard_fixes/<CID>.py and returns next_schedule_seconds: 300."""
        # Setup mock CTA and incomplete shard
        cta_data = {
            "competencies": [
                {"id": "Hab-03", "title": "IV Estimation"},
                {"id": "Hab-04", "title": "2SLS Estimation"},
            ]
        }
        (self.work_dir / "cta.json").write_text(json.dumps(cta_data, indent=2), encoding="utf-8")

        # Certified template only for Hab-03 (Hab-04 is missing)
        templates_dir = self.work_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)
        (templates_dir / "Hab-03.json").write_text(json.dumps({"competency_id": "Hab-03"}), encoding="utf-8")

        runaway_metrics = SubagentMetrics(
            subagent_id="subagent_shard_06",
            role="c2c_shard_author",
            transcript_path="dummy",
            turn_count=108,
            total_tokens=16_000_000,
            unit_id="shard_06",
            assigned_competency_ids=["Hab-03", "Hab-04"],
            is_completed=False,
        )

        report = SubagentWatchdogReport(
            subagent_id="subagent_shard_06",
            role="c2c_shard_author",
            unit_id="shard_06",
            is_runaway=True,
            runaway_reasons=["Turn limit exceeded: 108 > 40"],
            metrics=runaway_metrics,
            recommended_action="kill_and_redispatch",
        )

        res = generate_repair_redispatch(self.work_dir, [report])

        self.assertEqual(res["unfinished_count"], 1)
        self.assertEqual(res["next_schedule_seconds"], 300)
        self.assertEqual(len(res["Subagents"]), 1)

        subagent_spec = res["Subagents"][0]
        self.assertEqual(subagent_spec["TypeName"], "c2c_repair")
        self.assertIn("Hab-04", subagent_spec["Role"])
        self.assertIn("watchdog_repair_", subagent_spec["Prompt"])

        # Check work order item file written to disk
        item_file = Path(res["item_files"][0])
        self.assertTrue(item_file.is_file())
        item_data = json.loads(item_file.read_text(encoding="utf-8"))

        self.assertEqual(item_data["modular_fix_file"], "work/shards/shard_fixes/Hab-04.py")
        self.assertEqual(item_data["output_python"], "work/shards/shard_06_data.py")
        self.assertIn("--work", item_data["compile_command"])
        self.assertIn("--shard shard_06", item_data["compile_command"])
        self.assertIn("shard_fixes/Hab-04.py", item_data["instructions"])

    def test_parse_transcript_with_truncated_live_line(self) -> None:
        """Live transcripts mid-write with a truncated trailing JSON line parse cleanly."""
        t_file = self.work_dir / "truncated_live_transcript.jsonl"
        valid_line_1 = json.dumps({
            "source": "MODEL",
            "type": "PLANNER_RESPONSE",
            "input_tokens": 5000,
            "output_tokens": 200,
            "content": "Step 1 complete",
        })
        valid_line_2 = json.dumps({
            "source": "MODEL",
            "type": "PLANNER_RESPONSE",
            "input_tokens": 6000,
            "output_tokens": 250,
            "content": "Step 2 working",
        })
        # Partial truncated line as written by active subagent
        truncated_line = '{"step_index": 3, "source": "MODEL", "type": "PLANNER_RESP'

        t_file.write_text(f"{valid_line_1}\n{valid_line_2}\n{truncated_line}", encoding="utf-8")

        metrics = parse_transcript(t_file)
        self.assertEqual(metrics.turn_count, 2)
        self.assertEqual(metrics.input_tokens, 11000)
        self.assertEqual(metrics.output_tokens, 450)

    def test_resolve_brain_transcript_with_transcript_full_fallback(self) -> None:
        """When transcript.jsonl is missing but transcript_full.jsonl exists, resolves cleanly."""
        subagent_id = "test-subagent-uuid-full-5678"
        brain_log_dir = Path(self.test_dir) / "brain" / subagent_id / ".system_generated" / "logs"
        brain_log_dir.mkdir(parents=True, exist_ok=True)
        full_file = brain_log_dir / "transcript_full.jsonl"
        full_file.write_text('{"source":"MODEL","type":"PLANNER_RESPONSE","input_tokens":500}\n', encoding="utf-8")

        resolved = resolve_brain_transcript(subagent_id, app_data_dir=self.test_dir)
        self.assertIsNotNone(resolved)
        self.assertEqual(resolved.resolve(), full_file.resolve())

    def test_parse_transcript_empty_file(self) -> None:
        """Empty transcript file returns zeroed metrics without exception."""
        empty_file = self.work_dir / "empty_transcript.jsonl"
        empty_file.write_text("", encoding="utf-8")

        metrics = parse_transcript(empty_file)
        self.assertEqual(metrics.turn_count, 0)
        self.assertEqual(metrics.total_tokens, 0)


if __name__ == "__main__":
    unittest.main()
