"""M15 Phase 2 (Python DRT): Hypothesis property-based & stateful tests for c2c_hook_guard.py."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Dict

from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.stateful import RuleBasedStateMachine, initialize, invariant, precondition, rule

REPO_ROOT = Path(__file__).resolve().parents[2]
GUARD_PATH = REPO_ROOT / ".agents" / "skills" / "content-to-course" / "c2c_hook_guard.py"


def _load_guard():
    spec = importlib.util.spec_from_file_location("c2c_hook_guard", GUARD_PATH)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules["c2c_hook_guard"] = mod
    spec.loader.exec_module(mod)
    return mod


guard = _load_guard()


@given(
    error_count=st.one_of(st.none(), st.integers(min_value=-5, max_value=30)),
    affected_lines=st.one_of(st.none(), st.integers(min_value=0, max_value=30)),
    has_syntax=st.booleans(),
    existing_lines=st.integers(min_value=0, max_value=600),
    target_type=st.sampled_from(["shard", "cta"]),
    affected_comps=st.integers(min_value=0, max_value=10),
    distinct_compiles=st.integers(min_value=0, max_value=5),
)
@settings(max_examples=250, deadline=None)
def test_decidir_estrategia_edicion_2d_invariants(
    error_count,
    affected_lines,
    has_syntax,
    existing_lines,
    target_type,
    affected_comps,
    distinct_compiles,
):
    """Certify 2D strategy matrix boundaries across all combinations of inputs."""
    res = guard.decidir_estrategia_edicion(
        error_count=error_count,
        affected_line_count=affected_lines,
        has_syntax_error=has_syntax,
        existing_lines=existing_lines,
        target_type=target_type,
        affected_competencies_count=affected_comps,
        distinct_compiles=distinct_compiles,
    )
    assert res in ("write_file", "edit_file", "modular_splicing", "legacy_over_250")

    if has_syntax or existing_lines < 40:
        assert res == "write_file"
    elif target_type == "cta" and error_count is not None and error_count >= 3 and affected_comps >= 3:
        assert res == "write_file"
    elif error_count is not None:
        if error_count <= 0:
            assert res == "write_file"
        else:
            eff = affected_lines if affected_lines is not None else error_count
            if error_count >= 6 or eff > 5:
                assert res == "modular_splicing"
            else:
                assert res == "edit_file"
    else:
        limit = 450 if (target_type == "shard" and distinct_compiles == 1) else 250
        assert res == ("legacy_over_250" if existing_lines > limit else "write_file")


@given(
    slug=st.text(
        alphabet=st.characters(whitelist_categories=("Lu", "Ll", "Nd"), min_codepoint=48, max_codepoint=250),
        min_size=1,
        max_size=18,
    ),
    use_backslash=st.booleans(),
)
@settings(max_examples=120, deadline=None)
def test_path_normalization_and_forbidden_targets(slug, use_backslash):
    """Protected directories content/ and internal skill/engine dirs remain denied across slash variants."""
    sep = "\\" if use_backslash else "/"
    engine_path = f"d:{sep}repo{sep}.agents{sep}skills{sep}content-to-course{sep}engine{sep}{slug}.py"
    content_path = f"d:{sep}repo{sep}content{sep}{slug}.pdf"
    assert guard._matches_forbidden_target(engine_path.lower(), ".agents/skills/")
    assert guard._matches_forbidden_target(engine_path.lower(), "/engine/")
    assert not guard._is_authorized_worker_python_write(engine_path)
    assert guard._matches_forbidden_target(content_path.lower(), "content/")
    assert not guard._is_authorized_worker_python_write(content_path)


class HookGuardFSM(RuleBasedStateMachine):
    """Stateful DRT over process_hook() validating isolation, SLA budgets, and kill barrier."""

    @initialize()
    def init_workspace(self):
        self.tmp_dir = Path(tempfile.mkdtemp(prefix="drt_hook_guard_"))
        self.work_dir = self.tmp_dir / "work"
        (self.work_dir / "shards" / "shard_fixes").mkdir(parents=True)
        (self.work_dir / "dispatch").mkdir(parents=True)
        self.lock_file = self.work_dir / ".c2c_subagent_lock.json"
        self.director_id = "dir-conv-drt"
        self.worker_id = "wrk-conv-drt"

        self.orig_user_home = guard.USER_HOME
        fake_home = self.tmp_dir / "home"
        t_dir = fake_home / ".gemini" / "antigravity" / "brain" / self.director_id / ".system_generated" / "logs"
        t_dir.mkdir(parents=True)
        (t_dir / "transcript.jsonl").write_text(
            "\n".join(
                [
                    json.dumps(
                        {
                            "type": "PLANNER_RESPONSE",
                            "tool_calls": [
                                {"name": "invoke_subagent", "args": {"Role": "Shard 01 Author"}}
                            ],
                        }
                    ),
                    json.dumps(
                        {
                            "source": "MODEL",
                            "content": f'Created the following subagent: {{"conversationId": "{self.worker_id}"}}',
                        }
                    ),
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        guard.USER_HOME = fake_home

        self.turn_count = 0
        self.est_tokens = 0
        self.error_streak = 0
        self.pending_subagent = True
        self._sync_lock()

    def _sync_lock(self):
        guard._LOCK_CACHE.clear()
        guard._DIRECTOR_TRANSCRIPT_CACHE.clear()
        lock_data = {
            "active": True,
            "role": "shard_author",
            "course_id": "test_course_drt",
            "director_conversation_id": self.director_id,
            "assigned_shard": "shard_01",
            "work_dir": str(self.work_dir),
            "max_turns": 40,
            "max_tokens": 5_000_000,
            "max_error_streak": 3,
            "turn_count": self.turn_count,
            "est_tokens": self.est_tokens,
            "error_sha256_streak": self.error_streak,
            "dispatched_workers": {self.worker_id: "shard_01"} if self.pending_subagent else {},
        }
        if self.pending_subagent:
            (self.work_dir / "dispatch" / "wave_state.json").write_text(
                json.dumps(
                    {
                        "active_workers": {
                            self.worker_id: {"target_id": "shard_01", "role": "shard_author"}
                        }
                    }
                ),
                encoding="utf-8",
            )
        self.lock_file.write_text(json.dumps(lock_data), encoding="utf-8")

    @rule(turns=st.integers(min_value=0, max_value=20), tokens=st.integers(min_value=0, max_value=2_000_000))
    def advance_budget(self, turns, tokens):
        self.turn_count = min(60, self.turn_count + turns)
        self.est_tokens = min(7_000_000, self.est_tokens + tokens)
        self._sync_lock()

    @rule(streak=st.integers(min_value=0, max_value=4))
    def set_error_streak(self, streak):
        self.error_streak = streak
        self._sync_lock()

    @rule(target_path=st.sampled_from([
        "content/notas.pdf",
        "d:/repo/content/apuntes.md",
        ".agents/skills/content-to-course/run.py",
        "courses/other_course/work/cta.json",
        "hack/debug_helper.py",
        ".check_attempts",
        "scratch/debug_helper.py",
    ]))
    def worker_attempt_forbidden_write(self, target_path):
        payload = {
            "conversationId": self.worker_id,
            "toolCall": {
                "name": "write_file",
                "args": {"Path": target_path, "Content": "x = 1"},
            },
        }
        decision = guard.process_hook(payload, custom_lock_file=str(self.lock_file))
        assert decision["decision"] in ("allow", "deny")
        if target_path != "scratch/debug_helper.py":
            assert decision["decision"] == "deny"

    @rule()
    @precondition(lambda self: self.pending_subagent)
    def director_attempt_premature_kill_all(self):
        payload = {
            "conversationId": self.director_id,
            "toolCall": {
                "name": "manage_subagents",
                "args": {"Action": "kill_all"},
            },
        }
        decision = guard.process_hook(payload, custom_lock_file=str(self.lock_file))
        assert decision["decision"] == "deny"

    @invariant()
    def budget_overflow_always_blocks_worker(self):
        over_budget = (
            self.turn_count > 40
            or self.est_tokens > 5_000_000
            or self.error_streak >= 3
        )
        if over_budget:
            payload = {
                "conversationId": self.worker_id,
                "toolCall": {
                    "name": "read_file",
                    "args": {"Path": str(self.work_dir / "shards" / "shard_01_data.py")},
                },
            }
            decision = guard.process_hook(payload, custom_lock_file=str(self.lock_file))
            assert decision["decision"] == "deny"
            assert "HARD_ABORT" in decision.get("reason", "")

    def teardown(self):
        guard.USER_HOME = self.orig_user_home
        guard._LOCK_CACHE.clear()
        guard._DIRECTOR_TRANSCRIPT_CACHE.clear()
        shutil.rmtree(self.tmp_dir, ignore_errors=True)


TestHookGuardStatefulDRT = HookGuardFSM.TestCase
TestHookGuardStatefulDRT.settings = settings(
    max_examples=60,
    stateful_step_count=15,
    deadline=None,
)
