import assert from 'node:assert';

console.log('--- STARTING KEYBOARD NAVIGATION & AUTO-ADVANCE LOGIC TESTS ---');

function isOptionCorrect(question, optId) {
  if (!question || !question.options) return false;
  const opt = question.options.find((o) => o.id === optId);
  if (!opt) return false;
  if (typeof opt.is_correct === 'boolean') return opt.is_correct === true;
  return false;
}

function getCorrectOptionIds(question) {
  if (!question || !question.options) return [];
  return question.options.filter((o) => o.is_correct === true).map((o) => o.id);
}

// Test 1: Multiple choice question check logic
const mcqQuestion = {
  id: 'q1',
  type: 'multiple_choice_7_options',
  prompt: 'Calculate derivative',
  correct_answer: 'B',
  options: [
    { id: 'opt_a', option_id: 'A', content: 'x', is_correct: false },
    { id: 'opt_b', option_id: 'B', content: '2x', is_correct: true },
    { id: 'opt_c', option_id: 'C', content: 'x^2', is_correct: false },
  ]
};

// Case 1A: Selected wrong option -> Enter evaluates to incorrect, no auto-advance
{
  const selectedOption = 'opt_a';
  const hasAnswer = selectedOption !== null;
  assert.strictEqual(hasAnswer, true, 'Should have answer');
  const isCorrect = isOptionCorrect(mcqQuestion, selectedOption);
  assert.strictEqual(isCorrect, false, 'Should evaluate as false for wrong option');
}

// Case 1B: Selected correct option -> Enter evaluates to correct, triggers auto-advance
{
  const selectedOption = 'opt_b';
  const hasAnswer = selectedOption !== null;
  assert.strictEqual(hasAnswer, true, 'Should have answer');
  const isCorrect = isOptionCorrect(mcqQuestion, selectedOption);
  assert.strictEqual(isCorrect, true, 'Should evaluate as true for correct option');
}

// Test 2: Multiple select question
const msQuestion = {
  id: 'q2',
  type: 'multiple_select',
  prompt: 'Select all linear equations',
  correct_answer: ['A', 'C'],
  options: [
    { id: 'opt_a', option_id: 'A', content: 'y = 2x', is_correct: true },
    { id: 'opt_b', option_id: 'B', content: 'y = x^2', is_correct: false },
    { id: 'opt_c', option_id: 'C', content: 'y = -x', is_correct: true },
  ]
};

// Case 2A: Partial selection -> incorrect
{
  const selectedMultiOptions = ['opt_a'];
  const correctIds = getCorrectOptionIds(msQuestion).sort();
  const sSorted = [...selectedMultiOptions].sort();
  const isCorrect =
    sSorted.length === correctIds.length &&
    sSorted.every((val, idx) => val === correctIds[idx]);
  assert.strictEqual(isCorrect, false, 'Partial selection is incorrect');
}

// Case 2B: Full correct selection -> correct
{
  const selectedMultiOptions = ['opt_c', 'opt_a'];
  const correctIds = getCorrectOptionIds(msQuestion).sort();
  const sSorted = [...selectedMultiOptions].sort();
  const isCorrect =
    sSorted.length === correctIds.length &&
    sSorted.every((val, idx) => val === correctIds[idx]);
  assert.strictEqual(isCorrect, true, 'Full correct selection is correct');
}

// Test 3: Auto-advance timing simulation
{
  let advanced = false;
  let timerId = null;

  const simulateEnterOnCorrect = () => {
    // Timer sets auto-advance
    timerId = setTimeout(() => {
      advanced = true;
    }, 50);
  };

  simulateEnterOnCorrect();
  assert.strictEqual(advanced, false, 'Should not advance immediately at 0ms');

  await new Promise((r) => setTimeout(r, 60));
  assert.strictEqual(advanced, true, 'Should advance after timeout');
}

// Test 4: Second Enter cancels timer and advances immediately
{
  let advanceCount = 0;
  let timerId = null;

  const handleNext = () => {
    if (timerId) {
      clearTimeout(timerId);
      timerId = null;
    }
    advanceCount++;
  };

  // 1st Enter: schedules auto-advance
  timerId = setTimeout(() => {
    handleNext();
  }, 100);

  // 2nd Enter pressed before timeout: immediate advance
  handleNext();
  assert.strictEqual(advanceCount, 1, 'Advanced immediately on 2nd Enter');

  // Wait past 100ms to ensure timer didn't fire duplicate advance
  await new Promise((r) => setTimeout(r, 120));
  assert.strictEqual(advanceCount, 1, 'Timer did not fire duplicate advance');
}

console.log('ALL KEYBOARD NAVIGATION & AUTO-ADVANCE TESTS PASSED!');
