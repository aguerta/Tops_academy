"""Automated Verification Suite for Milestone 14-B: Simulador Adaptativo en 2 Módulos (Modo Hierro)."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from tests.helpers.common import PLATFORM_DIR, PLATFORM_SRC


def _find_esbuild() -> Path:
    cand = PLATFORM_DIR / "node_modules" / ".bin" / ("esbuild.cmd" if shutil.which("cmd") else "esbuild")
    if cand.is_file():
        return cand
    raw = PLATFORM_DIR / "node_modules" / "esbuild" / "bin" / "esbuild"
    if raw.is_file():
        return raw
    raise FileNotFoundError("esbuild binary not found in platform/node_modules")


def test_m14b_adaptive_module_routing_and_projection_runtime(tmp_path: Path) -> None:
    """Bundles real sessionShuffler.ts via esbuild and validates M14-B routing, no-repeat, and grade projection."""
    shuffler_ts = PLATFORM_SRC / "utils" / "sessionShuffler.ts"
    bundle_mjs = tmp_path / "shuffler.mjs"
    esbuild = _find_esbuild()

    cmd_build = [
        str(esbuild),
        str(shuffler_ts),
        "--bundle",
        "--format=esm",
        "--platform=node",
        f"--outfile={bundle_mjs}",
    ]
    res_build = subprocess.run(cmd_build, capture_output=True, text=True, check=False)
    assert res_build.returncode == 0, f"esbuild failed: {res_build.stderr}"

    driver_mjs = tmp_path / "test_driver.mjs"
    driver_mjs.write_text(
        f"""
import assert from 'node:assert/strict';
import {{
  ADAPTIVE_MODULE_CUTOFF_PCT,
  buildAdaptiveModule1,
  buildAdaptiveModule2,
  computeAdaptiveExamSummary,
}} from {bundle_mjs.as_uri()!r};

assert.equal(ADAPTIVE_MODULE_CUTOFF_PCT, 70);

const competencies = ['C-01', 'C-02', 'C-03', 'C-04', 'C-05', 'C-06'].map((id) => ({{
  id,
  code: id,
  name: `Comp ${{id}}`,
  category: 'Concept',
  description: `Desc ${{id}}`,
  mastery_target: 100,
}}));

const questions = [];
let idx = 1;
for (const c of competencies) {{
  for (const diff of ['easy', 'easy', 'medium', 'medium', 'medium', 'hard', 'hard', 'hard']) {{
    questions.push({{
      id: `Q-${{idx++}}`,
      competency_id: c.id,
      type: 'fill_in_the_blank',
      difficulty: diff,
      stem: `Pregunta ${{idx}} ${{c.id}} ${{diff}}`,
      options: [],
      correct_answer: {{ value: '1', tolerance: 0.01 }},
      hints: ['h1', 'h2', 'h3'],
      solution: '1',
    }});
  }}
}}

const course = {{
  course_id: 'test_m14b',
  title: 'Test M14-B',
  description: 'Test',
  version: '1.0.0',
  competencies,
  questions,
}};

const mod1 = buildAdaptiveModule1(course, 12);
assert.equal(mod1.length, 12);
const mod1Ids = new Set(mod1.map((q) => q.id));
assert.equal(mod1Ids.size, 12, 'Module 1 must have 12 unique questions');

// High score >= 70% -> advanced track, zero repeats, hard priority
const advPlan = buildAdaptiveModule2(course, 75, mod1Ids, new Set(['C-02']), 12);
assert.equal(advPlan.tier, 'advanced');
assert.equal(advPlan.cutoffPercentage, 70);
assert.equal(advPlan.questions.length, 12);
for (const q of advPlan.questions) {{
  assert.ok(!mod1Ids.has(q.id), `Question ${{q.id}} repeated from Module 1`);
}}
const advHardCount = advPlan.questions.filter((q) => q.difficulty === 'hard').length;
assert.ok(advHardCount >= 8, `Expected hard-heavy advanced module, got ${{advHardCount}}`);

// Low score < 70% -> standard track, zero repeats, reinforces missed competencies
const stdPlan = buildAdaptiveModule2(course, 58, mod1Ids, new Set(['C-01']), 12);
assert.equal(stdPlan.tier, 'standard');
assert.equal(stdPlan.questions.length, 12);
for (const q of stdPlan.questions) {{
  assert.ok(!mod1Ids.has(q.id), `Question ${{q.id}} repeated from Module 1`);
}}
const stdNonHardCount = stdPlan.questions.filter((q) => q.difficulty !== 'hard').length;
assert.ok(stdNonHardCount >= 8, `Expected medium/easy-focused standard module, got ${{stdNonHardCount}}`);

// Projection & unit breakdown checks
const allAdvQ = [...mod1, ...advPlan.questions];
const perfectTel = allAdvQ.map((q) => ({{
  question_id: q.id,
  competency_id: q.competency_id,
  is_correct: true,
  hints_used: 0,
  seconds_spent: 15,
}}));
const summaryAdv = computeAdaptiveExamSummary(
  course,
  {{ moduleIndex: 1, tier: 'diagnostic', score: 12, total: 12, percentage: 100, elapsedSeconds: 180 }},
  {{ moduleIndex: 2, tier: 'advanced', score: 12, total: 12, percentage: 100, elapsedSeconds: 180 }},
  perfectTel,
  allAdvQ
);
assert.equal(summaryAdv.routedTier, 'advanced');
assert.equal(summaryAdv.projectedGrade20, 20.0);
assert.equal(summaryAdv.avgSecondsPerQuestion, 15.0);
assert.ok(summaryAdv.unitBreakdown.length === 6);

const summaryStd = computeAdaptiveExamSummary(
  course,
  {{ moduleIndex: 1, tier: 'diagnostic', score: 6, total: 12, percentage: 50, elapsedSeconds: 180 }},
  {{ moduleIndex: 2, tier: 'standard', score: 12, total: 12, percentage: 100, elapsedSeconds: 180 }},
  perfectTel,
  [...mod1, ...stdPlan.questions]
);
assert.equal(summaryStd.routedTier, 'standard');
assert.ok(summaryStd.projectedGrade20 <= 15.5, 'Standard track ceiling must remain <= 15.5');
console.log('M14B_RUNTIME_OK');
""",
        encoding="utf-8",
    )

    res_node = subprocess.run(["node", str(driver_mjs)], capture_output=True, text=True, check=False)
    assert res_node.returncode == 0, f"Node test failed:\nSTDOUT:{res_node.stdout}\nSTDERR:{res_node.stderr}"
    assert "M14B_RUNTIME_OK" in res_node.stdout


def test_m14b_ui_contracts_present() -> None:
    """Verifies M14-B props, 5m/1m timer warnings, routing gate, and post-exam summary in UI components."""
    iron_src = (PLATFORM_SRC / "components" / "session" / "IronExamSession.tsx").read_text(encoding="utf-8")
    assert "moduleIndex?: 1 | 2;" in iron_src
    assert "remainingSeconds <= 60" in iron_src
    assert "remainingSeconds <= 300" in iron_src
    assert "iron-module-badge" in iron_src

    challenge_src = (PLATFORM_SRC / "components" / "CourseChallenge.tsx").read_text(encoding="utf-8")
    assert "start-adaptive-challenge-btn" in challenge_src

    completion_src = (PLATFORM_SRC / "components" / "CompletionScreen.tsx").read_text(encoding="utf-8")
    assert "adaptive-exam-summary" in completion_src
    assert "adaptive-projected-grade" in completion_src

    app_src = (PLATFORM_SRC / "App.tsx").read_text(encoding="utf-8")
    assert "adaptive-routing-card" in app_src
    assert "start-adaptive-module2-btn" in app_src
    assert "buildAdaptiveModule1" in app_src
    assert "buildAdaptiveModule2" in app_src
    assert "computeAdaptiveExamSummary" in app_src
