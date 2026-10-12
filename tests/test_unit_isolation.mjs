import assert from 'node:assert';

console.log('--- STARTING UNIT ISOLATION & SHUFFLE BOUNDARY TESTS ---');

function shuffleArray(items) {
  const result = [...items];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

function prepareSessionQuestions(questions, shuffleQuestions = false, expectedCompetencyId) {
  let validatedList = questions;

  if (expectedCompetencyId) {
    const target = expectedCompetencyId.trim().toLowerCase();
    validatedList = questions.filter((q) => {
      const qComp = (q.competency_id || '').trim().toLowerCase();
      return qComp === target;
    });
  }

  const qList = shuffleQuestions ? shuffleArray(validatedList) : [...validatedList];

  return qList.map((rawQ) => {
    if (rawQ.options && rawQ.options.length > 0) {
      return {
        ...rawQ,
        options: shuffleArray(rawQ.options),
      };
    }
    return rawQ;
  });
}

// Mock question generator
function createMockQuestion(id, competencyId, stem) {
  return {
    id,
    competency_id: competencyId,
    type: 'multiple_choice_7_options',
    stem,
    options: [
      { id: 'opt_a', option_id: 'A', content: 'Option A', is_correct: true },
      { id: 'opt_b', option_id: 'B', content: 'Option B', is_correct: false },
    ],
    correct_answer: 'A',
    hints: ['Hint 1'],
    solution: 'Solution'
  };
}

// Create a mixed pool of questions across 3 different units / competencies
const mixedPool = [
  createMockQuestion('q1', 'H-01', 'Polinomio caracteristico 1'),
  createMockQuestion('q2', 'H-01', 'Polinomio caracteristico 2'),
  createMockQuestion('q3', 'H-02', 'Formula cuadratica 1'),
  createMockQuestion('q4', 'H-02', 'Formula cuadratica 2'),
  createMockQuestion('q5', 'H-03', 'Inversa matricial 1'),
  createMockQuestion('q6', 'H-03', 'Inversa matricial 2'),
  createMockQuestion('q7', 'H-03', 'Inversa matricial 3'),
  createMockQuestion('q8', 'C-05', 'Modelo IS-LM dinamico 1'),
  createMockQuestion('q9', 'C-05', 'Modelo IS-LM dinamico 2'),
];

// Test 1: prepareSessionQuestions with expectedCompetencyId isolates strictly
{
  const h03Session = prepareSessionQuestions(mixedPool, true, 'H-03');
  assert.strictEqual(h03Session.length, 3, 'Should only contain the 3 H-03 questions');
  for (const q of h03Session) {
    assert.strictEqual(q.competency_id, 'H-03', `Question ${q.id} must belong to H-03`);
    assert.ok(!q.stem.includes('IS-LM'), `Question ${q.id} must not be an IS-LM question`);
  }
}

// Test 2: Stress test with 100 successive reshuffles
{
  for (let trial = 0; trial < 100; trial++) {
    const shuffled = prepareSessionQuestions(mixedPool, true, 'H-03');
    assert.strictEqual(shuffled.length, 3, `Trial ${trial}: length must be 3`);
    for (const q of shuffled) {
      assert.strictEqual(
        q.competency_id,
        'H-03',
        `Trial ${trial}: Leaked question ${q.id} with competency ${q.competency_id}`
      );
    }
  }
}

// Test 3: Simulation of launchSession pool filtering logic
{
  const mockCourse = {
    course_id: 'test_course',
    competencies: [
      { id: 'H-01', code: 'HEC-01', name: 'Polinomio', category: 'Fact', description: '', mastery_target: 100 },
      { id: 'H-03', code: 'HEC-03', name: 'Inversa Matricial 2x2', category: 'Fact', description: '', mastery_target: 100 },
      { id: 'H-99', code: 'HEC-99', name: 'Empty Unit', category: 'Fact', description: '', mastery_target: 100 },
    ],
    questions: mixedPool
  };

  function simulateLaunchPool(type, comp) {
    if (type === 'challenge') {
      return mockCourse.questions;
    }
    if (!comp) return [];
    const targetId = comp.id.trim().toLowerCase();
    const targetCode = (comp.code || '').trim().toLowerCase();
    return mockCourse.questions.filter((q) => {
      const qComp = (q.competency_id || '').trim().toLowerCase();
      return qComp === targetId || (targetCode !== '' && qComp === targetCode);
    });
  }

  // Case A: Practice session for H-03
  const poolH03 = simulateLaunchPool('practice', mockCourse.competencies[1]);
  assert.strictEqual(poolH03.length, 3, 'Practice pool must strictly contain 3 questions');
  assert.ok(poolH03.every((q) => q.competency_id === 'H-03'));

  // Case B: Unit test for H-01
  const poolH01 = simulateLaunchPool('test', mockCourse.competencies[0]);
  assert.strictEqual(poolH01.length, 2, 'Test pool must strictly contain 2 questions');
  assert.ok(poolH01.every((q) => q.competency_id === 'H-01'));

  // Case C: Empty competency must NEVER fallback to course questions
  const poolEmpty = simulateLaunchPool('practice', mockCourse.competencies[2]);
  assert.strictEqual(poolEmpty.length, 0, 'Empty competency must yield 0 questions, NOT fallback to course');

  // Case D: Course challenge uses all questions
  const poolChallenge = simulateLaunchPool('challenge', null);
  assert.strictEqual(poolChallenge.length, mixedPool.length, 'Challenge uses full pool');
}

console.log('ALL UNIT ISOLATION & SHUFFLE BOUNDARY TESTS PASSED (100% SUCCESS)!');
