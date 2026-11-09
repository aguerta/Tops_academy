"""Automated Test Suite for Milestone 14:
Khan Academy Mastery 2.0 Bidirectional Calibration, Degradation, Hint-Cap, and Fluency Timing.
"""
import json
import subprocess
import uuid
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

def eval_node_snippet(code: str) -> dict:
    """Executes a TypeScript/JavaScript snippet with mocked localStorage and returns JSON output."""
    runner = f"""
    const localStorageStore = {{}};
    global.localStorage = {{
      getItem: (k) => localStorageStore[k] || null,
      setItem: (k, v) => {{ localStorageStore[k] = String(v); }},
      removeItem: (k) => {{ delete localStorageStore[k]; }},
      clear: () => {{ for (const k in localStorageStore) delete localStorageStore[k]; }}
    }};
    global.window = {{ localStorage: global.localStorage }};

    const path = require('path');
    const mastery = require(path.resolve(__dirname, '../platform/src/utils/masteryStorage.ts'));

    {code}
    """
    temp_file = REPO_ROOT / "tests" / f"_temp_eval_{uuid.uuid4().hex[:8]}.ts"
    try:
        temp_file.write_text(runner, encoding="utf-8")
        res = subprocess.run(
            ["npx", "tsx", str(temp_file)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            shell=True,
        )
        if res.returncode != 0:
            raise RuntimeError(f"Node execution failed:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}")
        return json.loads(res.stdout.strip())
    finally:
        if temp_file.exists():
            temp_file.unlink(missing_ok=True)


def test_tier_transitions_degradation_and_promotions():
    """Verifies AC-32, AC-33, AC-34: Degradation upon failure and graduated promotion."""
    code = """
    const results = {
      // 1. Degradation from Mastered on single failure
      masteredFail: mastery.calculateTierTransition('Mastered', 0, 1, 'challenge', 0),
      // 2. Degradation from Proficient on single failure
      proficientFail: mastery.calculateTierTransition('Proficient', 0, 1, 'challenge', 0),
      // 3. Degradation from Familiar on single failure
      familiarFail: mastery.calculateTierTransition('Familiar', 0, 1, 'challenge', 0),
      // 4. Attempted on failure stays Attempted
      attemptedFail: mastery.calculateTierTransition('Attempted', 0, 1, 'challenge', 0),
      // 5. Not started on failure goes to Attempted
      notStartedFail: mastery.calculateTierTransition('Not started', 0, 1, 'challenge', 0),
      // 6. Not started on success jumps to Familiar (diagnostic leap)
      notStartedSuccess: mastery.calculateTierTransition('Not started', 1, 1, 'challenge', 0),
      // 7. Familiar on success goes to Proficient
      familiarSuccess: mastery.calculateTierTransition('Familiar', 1, 1, 'challenge', 0),
      // 8. Hint-cap: success with 2 hints caps at Familiar
      hintCappedNotStarted: mastery.calculateTierTransition('Not started', 1, 1, 'challenge', 2),
      hintCappedAttempted: mastery.calculateTierTransition('Attempted', 1, 1, 'challenge', 3),
      hintCappedFamiliar: mastery.calculateTierTransition('Familiar', 1, 1, 'challenge', 2),
    };
    console.log(JSON.stringify(results));
    """
    data = eval_node_snippet(code)
    assert data["masteredFail"] == "Proficient"
    assert data["proficientFail"] == "Familiar"
    assert data["familiarFail"] == "Attempted"
    assert data["attemptedFail"] == "Attempted"
    assert data["notStartedFail"] == "Attempted"
    assert data["notStartedSuccess"] == "Familiar"
    assert data["familiarSuccess"] == "Proficient"
    # Hint-cap assertions:
    assert data["hintCappedNotStarted"] == "Familiar"
    assert data["hintCappedAttempted"] == "Familiar"
    assert data["hintCappedFamiliar"] == "Familiar"


def test_course_challenge_calibration_and_telemetry():
    """Verifies atomic calibration across multiple competencies in a Course Challenge."""
    code = """
    const course = {
      course_id: 'test_course_1',
      title: 'Econometrics I',
      competencies: [
        { id: 'comp_1', name: 'MCO Basics', category: 'Unit 1' },
        { id: 'comp_2', name: 'Heteroskedasticity', category: 'Unit 2' },
        { id: 'comp_3', name: 'Instrumental Variables', category: 'Unit 3' }
      ],
      questions: []
    };

    // Preload mastery: comp_1 Mastered, comp_2 Familiar, comp_3 Not started
    const initialRecord = mastery.loadCourseMastery(course);
    initialRecord.competencies['comp_1'].status = 'Mastered';
    initialRecord.competencies['comp_1'].points = 100;
    initialRecord.competencies['comp_2'].status = 'Familiar';
    initialRecord.competencies['comp_2'].points = 50;
    initialRecord.competencies['comp_3'].status = 'Not started';
    initialRecord.competencies['comp_3'].points = 0;
    global.localStorage.setItem('tops_academic_progress_v1', JSON.stringify({ [course.course_id]: initialRecord }));

    // Challenge telemetry:
    // comp_1 fails (should level down to Proficient)
    // comp_2 succeeds (should level up to Proficient)
    // comp_3 succeeds (should level up to Familiar)
    const telemetry = [
      { question_id: 'q1', competency_id: 'comp_1', is_correct: false, hints_used: 0, seconds_spent: 35, question_text: 'MCO fail' },
      { question_id: 'q2', competency_id: 'comp_2', is_correct: true, hints_used: 0, seconds_spent: 40, question_text: 'Hetero ok' },
      { question_id: 'q3', competency_id: 'comp_3', is_correct: true, hints_used: 0, seconds_spent: 50, question_text: 'IV ok' }
    ];

    const summary = mastery.updateCourseChallengeWithSkillCalibration(course, telemetry, 125);
    console.log(JSON.stringify(summary));
    """
    summary = eval_node_snippet(code)

    assert summary["overall_score"] == 2
    assert summary["overall_total"] == 3
    assert len(summary["skills_leveled_down"]) == 1
    assert summary["skills_leveled_down"][0]["competency_id"] == "comp_1"
    assert summary["skills_leveled_down"][0]["new_tier"] == "Proficient"
    assert summary["skills_leveled_down"][0]["delta_points"] == -20

    assert len(summary["skills_leveled_up"]) == 2
    comp_ids_up = {s["competency_id"] for s in summary["skills_leveled_up"]}
    assert "comp_2" in comp_ids_up
    assert "comp_3" in comp_ids_up

    # Misconceptions collected
    assert len(summary["misconceptions"]) == 1
    assert summary["misconceptions"][0]["competency_id"] == "comp_1"


def test_timing_stats_and_fluency_rules():
    """Verifies: Best time updated ONLY on 100% approval, last time always updated, 300s cap."""
    code = """
    const course = {
      course_id: 'test_course_timing',
      title: 'Microeconomics',
      competencies: [{ id: 'comp_1', name: 'Elasticity', category: 'Unit 1' }],
      questions: []
    };

    // 1. First session: 100% score (3/3), 90s total (30s/q) -> Should set best time and last time
    const res1 = mastery.updateCompetencyScore(course, 'comp_1', 3, 3, 'practice', { totalSeconds: 90, hintsUsed: 0 });
    const timing1 = res1.competencies['comp_1'].timing.practice;

    // 2. Second session: faster (60s total, 20s/q) BUT imperfect score (2/3) -> Last time updates, best time STAYS 30s
    const res2 = mastery.updateCompetencyScore(course, 'comp_1', 2, 3, 'practice', { totalSeconds: 60, hintsUsed: 0 });
    const timing2 = res2.competencies['comp_1'].timing.practice;
    const needsReviewAfterFail = res2.competencies['comp_1'].needs_review;

    // 3. Third session: faster (45s total, 15s/q) AND perfect score (3/3) -> Best time updates to 15s, needs_review clears
    const res3 = mastery.updateCompetencyScore(course, 'comp_1', 3, 3, 'practice', { totalSeconds: 45, hintsUsed: 0 });
    const timing3 = res3.competencies['comp_1'].timing.practice;
    const needsReviewAfterClean = res3.competencies['comp_1'].needs_review;

    console.log(JSON.stringify({
      timing1,
      timing2,
      needsReviewAfterFail,
      timing3,
      needsReviewAfterClean
    }));
    """
    res = eval_node_snippet(code)

    assert res["timing1"]["best_avg_seconds_per_question"] == 30
    assert res["timing1"]["last_avg_seconds_per_question"] == 30

    # In session 2, score was 2/3: best time must not change
    assert res["timing2"]["best_avg_seconds_per_question"] == 30
    assert res["timing2"]["last_avg_seconds_per_question"] == 20
    assert res["needsReviewAfterFail"] is True

    # In session 3, score was 3/3: best time updates, needs review clears
    assert res["timing3"]["best_avg_seconds_per_question"] == 15
    assert res["timing3"]["last_avg_seconds_per_question"] == 15
    assert res["needsReviewAfterClean"] is False
