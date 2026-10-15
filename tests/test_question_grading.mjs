import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..');

// Import or re-implement the exact exported logic to verify against Node runtime
function isOptionCorrect(question, optId) {
  if (!question || !question.options || question.options.length === 0) {
    return false;
  }
  const opt = question.options.find((o) => o.id === optId);
  if (!opt) {
    return false;
  }
  if (typeof opt.is_correct === 'boolean') {
    return opt.is_correct === true;
  }
  const rawAnswer = question.correct_answer;
  if (rawAnswer === undefined || rawAnswer === null) {
    return false;
  }
  const optIdStr = (opt.id || '').trim();
  const optIdLower = optIdStr.toLowerCase();
  const optLetter = (opt.option_id || optIdStr.replace(/^opt_/, '')).trim().toLowerCase();

  if (typeof rawAnswer === 'string') {
    const target = rawAnswer.trim().toLowerCase();
    if (optIdLower === target) return true;
    if (optLetter === target) return true;
    if (optIdLower === `opt_${target}`) return true;
    if (`opt_${optLetter}` === target) return true;
    return false;
  }

  if (Array.isArray(rawAnswer)) {
    const targetList = rawAnswer.map((t) => String(t).trim().toLowerCase());
    return targetList.some(
      (t) =>
        t === optIdLower ||
        t === optLetter ||
        `opt_${t}` === optIdLower ||
        t === `opt_${optLetter}`
    );
  }

  if (typeof rawAnswer === 'number') {
    return String(rawAnswer) === opt.id || String(rawAnswer) === opt.option_id;
  }

  return false;
}

function getCorrectOptionIds(question) {
  if (!question || !question.options) {
    return [];
  }
  return question.options
    .filter((opt) => isOptionCorrect(question, opt.id))
    .map((opt) => opt.id);
}

function normalizeQuestion(question) {
  if (!question) return question;

  const normalizedSolution =
    (typeof question.solution === 'string' && question.solution.trim() !== ''
      ? question.solution
      : question.detailed_solution) || '';

  const normalizedMisconception =
    (typeof question.misconception_warning === 'string' &&
    question.misconception_warning.trim() !== ''
      ? question.misconception_warning
      : question.common_misconception_warning) || question.misconception_warning;

  const OPTION_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'];
  if (!question.options || question.options.length === 0) {
    return {
      ...question,
      solution: normalizedSolution,
      detailed_solution: question.detailed_solution || normalizedSolution,
      ...(normalizedMisconception
        ? {
            misconception_warning: normalizedMisconception,
            common_misconception_warning:
              question.common_misconception_warning || normalizedMisconception,
          }
        : {}),
    };
  }

  const normalizedOptions = question.options.map((opt, idx) => {
    const fallbackLetter = OPTION_LETTERS[idx] || `${idx + 1}`;
    const id = opt.id || (opt.option_id ? `opt_${opt.option_id.toLowerCase()}` : `opt_${fallbackLetter.toLowerCase()}`);
    const option_id = opt.option_id || id.replace(/^opt_/, '').toUpperCase();
    const isCorrect = typeof opt.is_correct === 'boolean'
      ? opt.is_correct
      : isOptionCorrect(question, opt.id || id);

    return {
      ...opt,
      id,
      option_id,
      is_correct: isCorrect,
    };
  });

  const q = {
    ...question,
    solution: normalizedSolution,
    detailed_solution: question.detailed_solution || normalizedSolution,
    ...(normalizedMisconception
      ? {
          misconception_warning: normalizedMisconception,
          common_misconception_warning:
            question.common_misconception_warning || normalizedMisconception,
        }
      : {}),
    options: normalizedOptions,
  };

  if (q.type === 'multiple_choice_7_options') {
    const correctOpt = normalizedOptions.find((o) => o.is_correct === true);
    if (correctOpt) {
      q.correct_answer = correctOpt.id;
    }
  } else if (q.type === 'multiple_select') {
    const correctIds = normalizedOptions
      .filter((o) => o.is_correct === true)
      .map((o) => o.id);
    if (correctIds.length > 0) {
      q.correct_answer = correctIds;
    }
  }

  return q;
}

function shuffleArray(items) {
  const result = [...items];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

function prepareSessionQuestions(questions, shuffleQuestions = false) {
  const qList = shuffleQuestions ? shuffleArray(questions) : [...questions];
  return qList.map((rawQ) => {
    const q = normalizeQuestion(rawQ);
    if (q.options && q.options.length > 0) {
      return {
        ...q,
        options: shuffleArray(q.options),
      };
    }
    return q;
  });
}

// ============================================================================
// TESTS SUITE
// ============================================================================
console.log('--- STARTING QUESTION EVALUATION & NORMALIZATION TEST SUITE ---');
let passCount = 0;
let failCount = 0;

function assert(condition, message) {
  if (condition) {
    passCount++;
  } else {
    failCount++;
    console.error(`FAIL: ${message}`);
  }
}

// Test 1: Screenshot Questions from sistemas_edos.json
let sistemasEdosPath = path.join(ROOT_DIR, 'courses', 'sistemas_edos.json');
if (!fs.existsSync(sistemasEdosPath)) {
  sistemasEdosPath = path.join(ROOT_DIR, 'archive_rejected_courses', 'sistemas_edos.json');
}
assert(fs.existsSync(sistemasEdosPath), 'sistemas_edos.json must exist');

const sistemasEdos = JSON.parse(fs.readFileSync(sistemasEdosPath, 'utf-8'));
const questionsMap = new Map(sistemasEdos.questions.map((q) => [q.id, q]));

// Screenshot 1: Q-H01-017 (matrix [[2, 4], [-1, -4]])
const q1 = questionsMap.get('Q-H01-017');
assert(q1 !== undefined, 'Q-H01-017 must exist');
if (q1) {
  // Original question has correct_answer = 'F', correct opt has id = 'opt_f'
  assert(isOptionCorrect(q1, 'opt_f') === true, 'Q-H01-017: opt_f must be correct');
  assert(isOptionCorrect(q1, 'opt_a') === false, 'Q-H01-017: opt_a must be distractor');
  assert(isOptionCorrect(q1, 'opt_c') === false, 'Q-H01-017: opt_c must be distractor');

  const norm1 = normalizeQuestion(q1);
  assert(norm1.correct_answer === 'opt_f', 'Normalized Q-H01-017 must have correct_answer "opt_f"');

  // Verify across 10 random shuffles
  for (let s = 0; s < 10; s++) {
    const session = prepareSessionQuestions([q1], false);
    const sq = session[0];
    const correctOpt = sq.options.find((o) => o.content.includes('+ 2\\lambda - 4 = 0'));
    assert(correctOpt !== undefined, 'Shuffled option with correct math must exist');
    assert(correctOpt.is_correct === true, 'Correct math option must have is_correct true');
    assert(isOptionCorrect(sq, correctOpt.id) === true, `Shuffled #${s}: correct math option must evaluate to true`);
  }
}

// Screenshot 2: Q-H01-020 (matrix [[1, 4], [-1, -3]])
const q2 = questionsMap.get('Q-H01-020');
assert(q2 !== undefined, 'Q-H01-020 must exist');
if (q2) {
  assert(isOptionCorrect(q2, 'opt_c') === true, 'Q-H01-020: opt_c must be correct');
  assert(isOptionCorrect(q2, 'opt_b') === false, 'Q-H01-020: opt_b must be distractor');
}

// Screenshot 5: Q-H02-024 (discriminant tr=-2, det=2)
const q5 = questionsMap.get('Q-H02-024');
assert(q5 !== undefined, 'Q-H02-024 must exist');
if (q5) {
  assert(isOptionCorrect(q5, 'opt_f') === true, 'Q-H02-024: opt_f must be correct');
  assert(isOptionCorrect(q5, 'opt_a') === false, 'Q-H02-024: opt_a must be distractor');
}

// Multiple Select in sistemas_edos: Q-H01-001
const qms = questionsMap.get('Q-H01-001');
assert(qms !== undefined, 'Q-H01-001 must exist');
if (qms) {
  const correctIds = getCorrectOptionIds(qms);
  assert(correctIds.includes('opt_a') && correctIds.includes('opt_b') && correctIds.includes('opt_c'), 'MS: opt_a, b, c correct');
  assert(!correctIds.includes('opt_d') && !correctIds.includes('opt_e'), 'MS: opt_d, e are false');

  // Multi-select exact match check
  const studentSelection = ['opt_a', 'opt_b', 'opt_c'];
  const sSorted = [...studentSelection].sort();
  const cSorted = [...correctIds].sort();
  const isMatch = sSorted.length === cSorted.length && sSorted.every((val, idx) => val === cSorted[idx]);
  assert(isMatch === true, 'MS full correct selection matches');

  // Incomplete selection must fail
  const incomplete = ['opt_a', 'opt_b'];
  const incompMatch = incomplete.length === cSorted.length && incomplete.every((val, idx) => val === cSorted[idx]);
  assert(incompMatch === false, 'MS incomplete selection fails');
}

// Test 2: Fixture valid_course_calculus.json (Legacy ID-based format)
const calculusPath = path.join(ROOT_DIR, 'courses', 'test_fixtures', 'valid_course_calculus.json');
if (fs.existsSync(calculusPath)) {
  const calcData = JSON.parse(fs.readFileSync(calculusPath, 'utf-8'));
  const calcQ1 = calcData.questions[0]; // correct_answer: "opt_b"
  assert(isOptionCorrect(calcQ1, 'opt_b') === true, 'Calculus Q1: opt_b must be correct');
  assert(isOptionCorrect(calcQ1, 'opt_a') === false, 'Calculus Q1: opt_a must be false');

  const calcQ4 = calcData.questions.find((q) => q.type === 'multiple_select');
  if (calcQ4) {
    const cIds = getCorrectOptionIds(calcQ4);
    assert(cIds.includes('opt_a') && cIds.includes('opt_c'), 'Calculus Q4: opt_a and opt_c correct');
    assert(!cIds.includes('opt_b') && !cIds.includes('opt_d'), 'Calculus Q4: opt_b and opt_d false');
  }
}

// Test 3: Sweep across ALL MC & MS questions in available courses
for (const cFile of ['estadistica3_regresion_v3.json', 'sistemas_edos.json', 'pde_course.json']) {
  let cPath = path.join(ROOT_DIR, 'courses', cFile);
  if (!fs.existsSync(cPath)) {
    cPath = path.join(ROOT_DIR, 'archive_rejected_courses', cFile);
  }
  if (!fs.existsSync(cPath)) continue;
  const cData = JSON.parse(fs.readFileSync(cPath, 'utf-8'));
  let mcTested = 0;
  let msTested = 0;

  for (const q of cData.questions) {
    if (q.type === 'multiple_choice_7_options' || q.interaction_type === 'multiple_choice_7_options') {
      const correctIds = getCorrectOptionIds(q);
      assert(correctIds.length === 1, `${cFile} ${q.id} must have exactly 1 correct option (got ${correctIds.length})`);
      mcTested++;
    } else if (q.type === 'multiple_select' || q.interaction_type === 'multiple_select') {
      const correctIds = getCorrectOptionIds(q);
      assert(correctIds.length >= 1 && correctIds.length < q.options.length, `${cFile} ${q.id} MS correct count must be between 1 and n-1 (got ${correctIds.length}/${q.options.length})`);
      msTested++;
    }
  }
  console.log(`Verified ${cFile}: ${mcTested} MC items, ${msTested} MS items`);
}

// Test 4 (Horizon 1 P1 & P2): Verify detailed_solution -> solution normalization and distractor error_rationale presence
const regPath = path.join(ROOT_DIR, 'courses', 'estadistica3_regresion_v3.json');
if (fs.existsSync(regPath)) {
  const regData = JSON.parse(fs.readFileSync(regPath, 'utf-8'));
  for (const q of regData.questions) {
    // Even if `solution` is removed to simulate raw v2 engine output, normalizeQuestion must populate it from `detailed_solution`
    const stripped = { ...q };
    delete stripped.solution;
    const normQ = normalizeQuestion(stripped);
    assert(
      typeof normQ.solution === 'string' && normQ.solution.trim().length > 10,
      `Horizon 1 P1: ${q.id} (${q.type}) normalized solution must be non-empty`
    );
    assert(
      typeof normQ.misconception_warning === 'string' && normQ.misconception_warning.trim().length > 5,
      `Horizon 1 P1: ${q.id} normalized misconception_warning must be non-empty`
    );

    if (q.type === 'multiple_choice_7_options' || q.type === 'multiple_select') {
      const distractors = normQ.options.filter((o) => !o.is_correct);
      for (const d of distractors) {
        assert(
          typeof d.error_rationale === 'string' && d.error_rationale.trim().length > 5,
          `Horizon 1 P2: ${q.id} distractor ${d.id} must have a diagnostic error_rationale`
        );
      }
    }
  }
  console.log(`Verified Horizon 1 P1 & P2 across all ${regData.questions.length} questions in estadistica3_regresion_v3.json`);
}

console.log('---------------------------------------------------------------');
console.log(`TEST RESULTS: ${passCount} PASSED, ${failCount} FAILED`);
if (failCount > 0) {
  process.exit(1);
} else {
  console.log('ALL TESTS PASSED WITH 100% SUCCESS!');
}
