"""Automated Verification Suite for Milestone 8:
FSRS-5/6 Spaced Retention (ts-fsrs), Per-Skill 12h Cooldown, Idea 1 No-Latency-Penalty
Rating Mapping, Cross-Skill Attribution, Misconception Ledger, and CloudSync Merge.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from tests.helpers.common import PLATFORM_DIR, PLATFORM_SRC


def _find_esbuild() -> Path:
    cand = PLATFORM_DIR / "node_modules" / ".bin" / ("esbuild.cmd" if shutil.which("cmd") else "esbuild")
    if cand.is_file():
        return cand
    raw = PLATFORM_DIR / "node_modules" / "esbuild" / "bin" / "esbuild"
    if raw.is_file():
        return raw
    raise FileNotFoundError("esbuild binary not found in platform/node_modules")


def _bundle_ts_module(src: Path, out: Path) -> None:
    esbuild = _find_esbuild()
    cmd = [
        str(esbuild),
        str(src),
        "--bundle",
        "--format=esm",
        "--platform=node",
        f"--outfile={out}",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    assert res.returncode == 0, f"esbuild failed on {src}:\n{res.stderr}"


def _run_node_driver(tmp_path: Path, driver_js: str) -> None:
    driver_path = tmp_path / "m8_driver.mjs"
    driver_path.write_text(driver_js, encoding="utf-8")
    res = subprocess.run(["node", str(driver_path)], capture_output=True, text=True, check=False)
    assert res.returncode == 0, f"Node test driver failed:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"


def test_m8_fsrs_decay_spacing_and_80_20_invariance(tmp_path: Path) -> None:
    """Layer 1 Time-Travel: monotone R(t) decay, spacing effect, lapse contraction, and 80/20 invariance."""
    fsrs_mjs = tmp_path / "fsrsEngine.mjs"
    mastery_mjs = tmp_path / "masteryStorage.mjs"
    _bundle_ts_module(PLATFORM_SRC / "utils" / "fsrsEngine.ts", fsrs_mjs)
    _bundle_ts_module(PLATFORM_SRC / "utils" / "masteryStorage.ts", mastery_mjs)

    driver = f"""
import assert from 'node:assert/strict';

const store = {{}};
globalThis.localStorage = {{
  getItem: (k) => store[k] || null,
  setItem: (k, v) => {{ store[k] = String(v); }},
  removeItem: (k) => {{ delete store[k]; }},
  clear: () => {{ for (const k in store) delete store[k]; }},
}};
globalThis.window = {{ localStorage: globalThis.localStorage }};

const fsrsMod = await import({fsrs_mjs.as_uri()!r});
const masteryMod = await import({mastery_mjs.as_uri()!r});

// 1. Spacing effect & lapse contraction
const t0 = new Date('2026-11-01T12:00:00.000Z');
const c0 = fsrsMod.createInitialFsrsCard(t0);
const r1 = fsrsMod.scheduleFsrsReview(c0, 3, t0).nextCard; // Good at t0

const tImmediate = new Date(t0.getTime() + 0.01 * 86400_000);
const tSpaced = new Date(t0.getTime() + 5 * 86400_000);
const sImmediate = fsrsMod.scheduleFsrsReview(r1, 3, tImmediate).nextCard.stability;
const sSpacedCard = fsrsMod.scheduleFsrsReview(r1, 3, tSpaced).nextCard;
assert.ok(
  sSpacedCard.stability > sImmediate,
  `Expected spaced Good stability (${{sSpacedCard.stability}}) > immediate (${{sImmediate}})`
);

const tLapse = new Date(tSpaced.getTime() + 2 * 86400_000);
const lapseCard = fsrsMod.scheduleFsrsReview(sSpacedCard, 1, tLapse).nextCard; // Again
assert.ok(lapseCard.stability < sSpacedCard.stability, 'Again must contract stability');
assert.ok(lapseCard.difficulty > sSpacedCard.difficulty, 'Again must raise difficulty');
assert.equal(lapseCard.lapses, 1);

// 2. Monotone R(t) decay over +1d, +7d, +14d, +45d and extreme abandonment (<0.50)
const fragileCard = fsrsMod.scheduleFsrsReview(c0, 1, t0).nextCard; // Initial Again (low stability)
const rVals = [1, 7, 14, 45].map((d) =>
  fsrsMod.computeRetrievability(fragileCard, new Date(t0.getTime() + d * 86400_000))
);
for (let i = 1; i < rVals.length; i++) {{
  assert.ok(rVals[i] < rVals[i - 1], `Expected strict R(t) decrease: ${{rVals.join(', ')}}`);
}}
assert.ok(rVals[3] < 0.50, `Expected extreme abandonment R(+45d) < 0.50 on fragile card, got ${{rVals[3]}}`);

// 3. Soft decay warning & extreme downgrade without touching 80/20 unit_test
const course = {{
  course_id: 'm8_decay_course',
  title: 'Decay Test',
  description: '',
  version: '1.0',
  competencies: [
    {{ id: 'C-01', code: 'C-01', name: 'Comp 1', category: 'Concept', description: '', mastery_target: 100 }},
    {{ id: 'C-02', code: 'C-02', name: 'Comp 2', category: 'Concept', description: '', mastery_target: 100 }},
  ],
  questions: [],
}};

// C-01 has Unit Test 100% and Mastered card that decays; C-02 has Unit Test 100%
const rAtT0 = masteryMod.loadCourseMastery(course, t0);
rAtT0.competencies['C-01'] = {{
  status: 'Mastered',
  points: 100,
  last_practiced: t0.toISOString(),
  last_tier_promotion_at: t0.toISOString(),
  unit_test: {{ last_score: 7, total_questions: 7, percentage: 100, completed_at: t0.toISOString() }},
  fsrs: r1,
  history: [{{ date: t0.toISOString(), score: 7, total: 7, type: 'test' }}],
}};
rAtT0.competencies['C-02'] = {{
  status: 'Proficient',
  points: 80,
  last_practiced: t0.toISOString(),
  last_tier_promotion_at: t0.toISOString(),
  unit_test: {{ last_score: 7, total_questions: 7, percentage: 100, completed_at: t0.toISOString() }},
  fsrs: r1,
  history: [{{ date: t0.toISOString(), score: 7, total: 7, type: 'test' }}],
}};
store['tops_academic_progress_v1'] = JSON.stringify({{ [course.course_id]: rAtT0 }});

// At +7d, r1 R is < 0.85 -> triggers soft review_reason = 'decay', stays Mastered
const t7d = new Date(t0.getTime() + 7 * 86400_000);
const loaded7d = masteryMod.loadCourseMastery(course, t7d);
assert.equal(loaded7d.competencies['C-01'].needs_review, true);
assert.equal(loaded7d.competencies['C-01'].review_reason, 'decay');
assert.equal(loaded7d.competencies['C-01'].status, 'Mastered');

// Replace C-01 fsrs with fragileCard and advance +45d -> R < 0.50 downgrades Mastered -> Proficient WITHOUT losing 80/20
loaded7d.competencies['C-01'].fsrs = fragileCard;
store['tops_academic_progress_v1'] = JSON.stringify({{ [course.course_id]: loaded7d }});
const t45d = new Date(t0.getTime() + 45 * 86400_000);
const loaded45d = masteryMod.loadCourseMastery(course, t45d);
assert.equal(loaded45d.competencies['C-01'].status, 'Proficient');
assert.equal(loaded45d.competencies['C-01'].points, 80);
assert.equal(loaded45d.competencies['C-01'].review_reason, 'decay');
assert.equal(loaded45d.competencies['C-01'].unit_test.percentage, 100);
const prog = masteryMod.calculateCourseProgress(loaded45d, 2);
assert.equal(prog.percentage, 80, '80/20 course progress must remain intact after FSRS downgrade');
assert.equal(prog.status, 'unit_tests_mastered');
"""
    _run_node_driver(tmp_path, driver)


def test_m8_per_skill_12h_cooldown_and_unit_test_cap(tmp_path: Path) -> None:
    """Verifies Unit Test 100% caps at Proficient while keeping 80% green, and 12h cooldown acts per-skill."""
    mastery_mjs = tmp_path / "masteryStorage.mjs"
    _bundle_ts_module(PLATFORM_SRC / "utils" / "masteryStorage.ts", mastery_mjs)

    driver = f"""
import assert from 'node:assert/strict';

const store = {{}};
globalThis.localStorage = {{
  getItem: (k) => store[k] || null,
  setItem: (k, v) => {{ store[k] = String(v); }},
  removeItem: (k) => {{ delete store[k]; }},
  clear: () => {{ for (const k in store) delete store[k]; }},
}};
globalThis.window = {{ localStorage: globalThis.localStorage }};

const masteryMod = await import({mastery_mjs.as_uri()!r});

const course = {{
  course_id: 'm8_cooldown_course',
  title: 'Cooldown Test',
  description: '',
  version: '1.0',
  competencies: [
    {{ id: 'C-A', code: 'C-A', name: 'Skill A', category: 'Skill', description: '', mastery_target: 100 }},
    {{ id: 'C-B', code: 'C-B', name: 'Skill B', category: 'Skill', description: '', mastery_target: 100 }},
  ],
  questions: [],
}};

const tBase = new Date('2026-11-10T10:00:00.000Z');
// Skill A passes multi-question Unit Test at t = 0 -> caps at Proficient, Completed (Verde) for 80/20
const telA = [
  {{ question_id: 'qA1', competency_id: 'C-A', is_correct: true, hints_used: 0, seconds_spent: 40, question_type: 'open_symbolic', wrong_attempts: 0 }},
  {{ question_id: 'qA1b', competency_id: 'C-A', is_correct: true, hints_used: 0, seconds_spent: 42, question_type: 'open_symbolic', wrong_attempts: 0 }},
];
masteryMod.updateCompetencyScore(course, 'C-A', 2, 2, 'test', {{ totalSeconds: 82, hintsUsed: 0 }}, telA, tBase);

// Skill B passed multi-question Unit Test 2 hours earlier (so at t + 11h59m from tBase, Skill B is at 13h59m >= 12h)
const tEarlier = new Date(tBase.getTime() - 2 * 3600_000);
const telB = [
  {{ question_id: 'qB1', competency_id: 'C-B', is_correct: true, hints_used: 0, seconds_spent: 40, question_type: 'open_symbolic', wrong_attempts: 0 }},
  {{ question_id: 'qB1b', competency_id: 'C-B', is_correct: true, hints_used: 0, seconds_spent: 38, question_type: 'open_symbolic', wrong_attempts: 0 }},
];
masteryMod.updateCompetencyScore(course, 'C-B', 2, 2, 'test', {{ totalSeconds: 78, hintsUsed: 0 }}, telB, tEarlier);

const recAfterTests = masteryMod.loadCourseMastery(course, tBase);
assert.equal(recAfterTests.competencies['C-A'].status, 'Proficient', 'Unit Test 100% must cap at Proficient');
assert.equal(recAfterTests.competencies['C-B'].status, 'Proficient');
assert.equal(masteryMod.isUnitCompleted(recAfterTests.competencies['C-A']), true);
assert.equal(masteryMod.calculateCourseProgress(recAfterTests, 2).percentage, 80);

// At tBase + 11h 59m: run Mastery Challenge covering BOTH Skill A (11h59m) and Skill B (13h59m)
const tCheck = new Date(tBase.getTime() + (11 * 3600 + 59 * 60) * 1000);
const summary1 = masteryMod.updateSessionWithCrossSkillCalibration(
  course,
  [
    {{ question_id: 'qA2', competency_id: 'C-A', is_correct: true, hints_used: 0, seconds_spent: 35, question_type: 'open_symbolic', wrong_attempts: 0 }},
    {{ question_id: 'qB2', competency_id: 'C-B', is_correct: true, hints_used: 0, seconds_spent: 35, question_type: 'open_symbolic', wrong_attempts: 0 }},
  ],
  70,
  'mastery_challenge',
  {{ now: tCheck }}
);

// Skill A blocked by per-skill cooldown (~1 min left), Skill B promoted to Mastered in same session!
assert.equal(summary1.record.competencies['C-A'].status, 'Proficient');
assert.equal(summary1.record.competencies['C-B'].status, 'Mastered');
const maintainedA = summary1.skills_maintained.find((s) => s.competency_id === 'C-A');
assert.ok(maintainedA && maintainedA.cooldown_remaining_ms > 0, 'Must expose cooldown_remaining_ms');

// At tBase + 12h 01m: Skill A now clears its 12h window and promotes to Mastered
const tEligible = new Date(tBase.getTime() + (12 * 3600 + 60) * 1000);
const summary2 = masteryMod.updateSessionWithCrossSkillCalibration(
  course,
  [
    {{ question_id: 'qA3', competency_id: 'C-A', is_correct: true, hints_used: 0, seconds_spent: 30, question_type: 'open_symbolic', wrong_attempts: 0 }},
  ],
  30,
  'mastery_challenge',
  {{ now: tEligible }}
);
assert.equal(summary2.record.competencies['C-A'].status, 'Mastered');
"""
    _run_node_driver(tmp_path, driver)


def test_m8_idea1_rating_mapping_and_no_latency_penalty(tmp_path: Path) -> None:
    """Verifies Idea 1: latency never penalizes to Hard; wrong_attempts/hints/partial/lucky_guess trigger Hard."""
    fsrs_mjs = tmp_path / "fsrsEngine.mjs"
    _bundle_ts_module(PLATFORM_SRC / "utils" / "fsrsEngine.ts", fsrs_mjs)

    driver = f"""
import assert from 'node:assert/strict';

const fsrsMod = await import({fsrs_mjs.as_uri()!r});

// 1. ratio < 0.75 -> Again (1)
assert.equal(
  fsrsMod.computeAutomaticFsrsRating({{
    ratio: 0.5,
    hintsUsed: 0,
    totalWrongAttempts: 0,
    priorReviews: 5,
    speedRatio: 0.5,
    hasPersonalBaseline: true,
  }}).rating,
  1
);

// 2. Partial accuracy [0.75, 1.0) -> Hard (2)
assert.equal(
  fsrsMod.computeAutomaticFsrsRating({{
    ratio: 0.75,
    hintsUsed: 0,
    totalWrongAttempts: 0,
    priorReviews: 5,
    speedRatio: 0.6,
    hasPersonalBaseline: true,
  }}).rating,
  2
);

// 3. Reintento previo (wrongAttemptsCount >= 1 before getting it right) -> Hard (2)
assert.equal(
  fsrsMod.computeAutomaticFsrsRating({{
    ratio: 1.0,
    hintsUsed: 0,
    totalWrongAttempts: 1,
    priorReviews: 5,
    speedRatio: 0.8,
    hasPersonalBaseline: true,
  }}).rating,
  2
);

// 4. Hints >= 2 -> Hard (2)
assert.equal(
  fsrsMod.computeAutomaticFsrsRating({{
    ratio: 1.0,
    hintsUsed: 2,
    totalWrongAttempts: 0,
    priorReviews: 5,
    speedRatio: 0.8,
    hasPersonalBaseline: true,
  }}).rating,
  2
);

// 5. Iron Exam lucky_guess -> Hard (2)
assert.equal(
  fsrsMod.computeAutomaticFsrsRating({{
    ratio: 1.0,
    hintsUsed: 0,
    totalWrongAttempts: 0,
    hasLuckyGuess: true,
    priorReviews: 5,
    speedRatio: 0.6,
    hasPersonalBaseline: true,
  }}).rating,
  2
);

// 6. Meticulous paper student (very slow speedRatio = 4.0, zero hints, zero wrong attempts) -> Good (3) NEVER Hard!
assert.equal(
  fsrsMod.computeAutomaticFsrsRating({{
    ratio: 1.0,
    hintsUsed: 0,
    totalWrongAttempts: 0,
    priorReviews: 5,
    speedRatio: 4.0,
    hasPersonalBaseline: true,
  }}).rating,
  3
);

// 7. Fast clean with personal baseline (speedRatio < 0.7, reps >= 3) -> Easy (4)
assert.equal(
  fsrsMod.computeAutomaticFsrsRating({{
    ratio: 1.0,
    hintsUsed: 0,
    totalWrongAttempts: 0,
    priorReviews: 3,
    speedRatio: 0.65,
    hasPersonalBaseline: true,
  }}).rating,
  4
);

// 8. Without >= 3 personal samples, fast answer caps at Good (3)
assert.equal(
  fsrsMod.computeAutomaticFsrsRating({{
    ratio: 1.0,
    hintsUsed: 0,
    totalWrongAttempts: 0,
    priorReviews: 3,
    speedRatio: 0.5,
    hasPersonalBaseline: false,
  }}).rating,
  3
);

// 9. Brier Score & Log-Loss calibration calculation
const cal = fsrsMod.computeCalibrationMetrics([
  {{ date: '2026-11-01T00:00:00Z', competency_id: 'C-1', delta_t_days: 0, predicted_r: 1, actual_correct: true, rating: 3 }}, // ignored (delta_t = 0)
  {{ date: '2026-11-05T00:00:00Z', competency_id: 'C-1', delta_t_days: 4, predicted_r: 0.9, actual_correct: true, rating: 3 }},
  {{ date: '2026-11-10T00:00:00Z', competency_id: 'C-1', delta_t_days: 5, predicted_r: 0.8, actual_correct: false, rating: 1 }},
]);
assert.equal(cal.n, 2);
assert.ok(Math.abs(cal.brierScore - ((0.01 + 0.64) / 2)) < 1e-6);
assert.ok(cal.logLoss > 0);
assert.equal(cal.isReliable, false);
"""
    _run_node_driver(tmp_path, driver)


def test_m8_cross_skill_ledger_selectors_and_cloudsync(tmp_path: Path) -> None:
    """Verifies cross-skill Unit Test attribution, carrier-strict Misconception Ledger, session selectors, Iron grading distractor IDs, and CloudSync merge."""
    mastery_mjs = tmp_path / "masteryStorage.mjs"
    shuffler_mjs = tmp_path / "sessionShuffler.mjs"
    cloud_mjs = tmp_path / "cloudSync.mjs"
    iron_mjs = tmp_path / "ironExamGrading.mjs"
    _bundle_ts_module(PLATFORM_SRC / "utils" / "masteryStorage.ts", mastery_mjs)
    _bundle_ts_module(PLATFORM_SRC / "utils" / "sessionShuffler.ts", shuffler_mjs)
    _bundle_ts_module(PLATFORM_SRC / "utils" / "cloudSync.ts", cloud_mjs)
    _bundle_ts_module(PLATFORM_SRC / "utils" / "ironExamGrading.ts", iron_mjs)

    driver = f"""
import assert from 'node:assert/strict';

const store = {{}};
globalThis.localStorage = {{
  getItem: (k) => store[k] || null,
  setItem: (k, v) => {{ store[k] = String(v); }},
  removeItem: (k) => {{ delete store[k]; }},
  clear: () => {{ for (const k in store) delete store[k]; }},
}};
globalThis.window = {{
  localStorage: globalThis.localStorage,
  dispatchEvent: () => {{}},
}};

const masteryMod = await import({mastery_mjs.as_uri()!r});
const shufflerMod = await import({shuffler_mjs.as_uri()!r});
const cloudMod = await import({cloud_mjs.as_uri()!r});
const ironMod = await import({iron_mjs.as_uri()!r});

const q1 = {{
  id: 'q1',
  competency_id: 'C-01',
  type: 'open_symbolic',
  difficulty: 'medium',
  stem: 'Deriva x^2',
  options: [],
  correct_answer: {{ expression: '2*x' }},
  diagnostic_distractors: [
    {{ distractor_id: 'D-C01-01', expression: 'x', error_rationale: 'Olvidó bajar el exponente' }},
  ],
  hints: [],
  solution: '2x',
}};
const q1NonCarrier = {{
  id: 'q1_other',
  competency_id: 'C-01',
  type: 'fill_in_the_blank',
  difficulty: 'easy',
  stem: 'Deriva 5',
  options: [],
  correct_answer: {{ value: 0 }},
  diagnostic_distractors: [
    {{ distractor_id: 'D-C01-99', expression: '5', error_rationale: 'Constante no es x' }},
  ],
  hints: [],
  solution: '0',
}};
const q2 = {{
  id: 'q2',
  competency_id: 'C-02',
  type: 'fill_in_the_blank',
  difficulty: 'medium',
  stem: 'Integral 2x',
  options: [],
  correct_answer: {{ expression: 'x^2' }},
  diagnostic_distractors: [],
  hints: [],
  solution: 'x^2',
}};
const q3Unstarted = {{
  id: 'q3',
  competency_id: 'C-03',
  type: 'fill_in_the_blank',
  difficulty: 'hard',
  stem: 'Unstarted q',
  options: [],
  correct_answer: {{ value: 1 }},
  hints: [],
  solution: '1',
}};

const course = {{
  course_id: 'm8_full',
  title: 'Calc',
  description: '',
  version: '1.0',
  competencies: [
    {{ id: 'C-01', code: 'C-01', name: 'Derivadas', category: 'Skill', description: '', mastery_target: 100 }},
    {{ id: 'C-02', code: 'C-02', name: 'Integrales', category: 'Skill', description: '', mastery_target: 100 }},
    {{ id: 'C-03', code: 'C-03', name: 'Series', category: 'Skill', description: '', mastery_target: 100 }},
  ],
  questions: [q1, q1NonCarrier, q2, q3Unstarted],
}};

// 1. Iron Exam grading extracts real distractor ID
const ironRes = ironMod.gradeIronExamQuestion(q1, {{
  selectedOption: null,
  selectedMultiOptions: [],
  fillBlankValue: '',
  structuredAnswer: {{ kind: 'open_symbolic', expression: 'x' }},
  canvasInteracted: false,
}});
assert.equal(ironRes.isCorrect, false);
assert.deepEqual(ironRes.matchedDistractorIds, ['D-C01-01']);

// 2. Interleaved Unit Test on C-02 where prior C-01 item fails with D-C01-01
const t1 = new Date('2026-11-12T10:00:00.000Z');
const utSummary = masteryMod.updateSessionWithCrossSkillCalibration(
  course,
  [
    {{
      question_id: 'q1',
      competency_id: 'C-01',
      is_correct: false,
      hints_used: 0,
      seconds_spent: 50,
      question_type: 'open_symbolic',
      wrong_attempts: 1,
      matched_distractor_ids: ['D-C01-01'],
      matched_distractor_rationales: {{ 'D-C01-01': 'Olvidó bajar el exponente' }},
      carried_distractor_ids: ['D-C01-01'],
    }},
    {{
      question_id: 'q2',
      competency_id: 'C-02',
      is_correct: true,
      hints_used: 0,
      seconds_spent: 45,
      question_type: 'fill_in_the_blank',
      wrong_attempts: 0,
    }},
  ],
  95,
  'test',
  {{ targetCompetencyId: 'C-02', now: t1 }}
);

// C-01 gets updated cross-skill + Ledger recorded, while unit_test lives on C-02
assert.equal(utSummary.record.competencies['C-01'].needs_review, true);
assert.equal(utSummary.record.competencies['C-01'].review_reason, 'error');
assert.equal(utSummary.record.competencies['C-02'].unit_test.percentage, 50);
assert.equal(utSummary.record.misconception_ledger['D-C01-01'].count, 1);
assert.equal(utSummary.record.misconception_ledger['D-C01-01'].resolved_streak, 0);

// 3. Mastery Challenge excludes C-03 (Not started) and Misconception Drill targets D-C01-01
const mcQuestions = shufflerMod.buildMasteryChallengeQuestions(course, utSummary.record, t1, 6);
assert.ok(mcQuestions.length > 0);
assert.ok(mcQuestions.every((q) => q.competency_id !== 'C-03'), 'Mastery Challenge must exclude Not started');

const trapQuestions = shufflerMod.buildMisconceptionSession(course, ['D-C01-01'], 6);
assert.equal(trapQuestions.length, 1);
assert.equal(trapQuestions[0].id, 'q1');

// 4. Non-carrier question on C-01 does NOT increment resolved_streak for D-C01-01
const t2 = new Date('2026-11-12T12:00:00.000Z');
masteryMod.updateSessionWithCrossSkillCalibration(
  course,
  [{{
    question_id: 'q1_other',
    competency_id: 'C-01',
    is_correct: true,
    hints_used: 0,
    seconds_spent: 20,
    question_type: 'fill_in_the_blank',
    wrong_attempts: 0,
    carried_distractor_ids: ['D-C01-99'],
  }}],
  20,
  'misconception_drill',
  {{ now: t2 }}
);
let rec2 = masteryMod.loadCourseMastery(course, t2);
assert.equal(rec2.misconception_ledger['D-C01-01'].resolved_streak, 0, 'Non-carrier question must not resolve D-C01-01');

// 5. Two clean autonomous passes on carrier q1 resolve D-C01-01 (resolved_streak === 2)
const t3 = new Date('2026-11-12T14:00:00.000Z');
masteryMod.updateSessionWithCrossSkillCalibration(
  course,
  [{{
    question_id: 'q1',
    competency_id: 'C-01',
    is_correct: true,
    hints_used: 0,
    seconds_spent: 25,
    question_type: 'open_symbolic',
    wrong_attempts: 0,
    carried_distractor_ids: ['D-C01-01'],
  }}],
  25,
  'misconception_drill',
  {{ now: t3 }}
);
const t4 = new Date('2026-11-12T16:00:00.000Z');
const res4 = masteryMod.updateSessionWithCrossSkillCalibration(
  course,
  [{{
    question_id: 'q1',
    competency_id: 'C-01',
    is_correct: true,
    hints_used: 0,
    seconds_spent: 22,
    question_type: 'open_symbolic',
    wrong_attempts: 0,
    carried_distractor_ids: ['D-C01-01'],
  }}],
  22,
  'misconception_drill',
  {{ now: t4 }}
);
assert.equal(res4.record.misconception_ledger['D-C01-01'].resolved_streak, 2);
assert.equal(masteryMod.getActiveMisconceptions(res4.record).length, 0);
assert.equal(masteryMod.getResolvedMisconceptions(res4.record).length, 1);

// 6. CloudSync merge preserves FSRS, Ledger & deduplicates/caps srs_telemetry to 500
const remoteCopy = JSON.parse(JSON.stringify({{ [course.course_id]: res4.record }}));
const localCopy = JSON.parse(JSON.stringify({{ [course.course_id]: res4.record }}));
localCopy[course.course_id].srs_telemetry = Array.from({{ length: 400 }}, (_, i) => ({{
  date: new Date(t4.getTime() + i * 1000).toISOString(),
  competency_id: 'C-01',
  delta_t_days: 1,
  predicted_r: 0.9,
  actual_correct: true,
  rating: 3,
}}));
remoteCopy[course.course_id].srs_telemetry = Array.from({{ length: 200 }}, (_, i) => ({{
  date: new Date(t4.getTime() + (i + 350) * 1000).toISOString(),
  competency_id: 'C-01',
  delta_t_days: 1,
  predicted_r: 0.9,
  actual_correct: true,
  rating: 3,
}}));
const merged = cloudMod.mergeAllMasteryData(localCopy, remoteCopy);
assert.ok(merged[course.course_id].competencies['C-01'].fsrs, 'CloudSync must preserve FSRS card');
assert.ok(merged[course.course_id].misconception_ledger['D-C01-01'], 'CloudSync must preserve Misconception Ledger');
assert.equal(merged[course.course_id].srs_telemetry.length, 500, 'CloudSync must cap srs_telemetry at 500');
"""
    _run_node_driver(tmp_path, driver)
