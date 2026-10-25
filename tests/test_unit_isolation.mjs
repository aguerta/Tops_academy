import assert from 'node:assert';

console.log('--- STARTING UNIT ISOLATION, INTERLEAVING & ZPD CALIBRATION TESTS ---');

function shuffleArray(items) {
  const result = [...items];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

function calibrateByMasteryDifficulty(questions, masteryTier) {
  if (!masteryTier || questions.length <= 1) {
    return questions;
  }

  const easy = [];
  const medium = [];
  const hard = [];

  for (const q of questions) {
    const diff = (q.difficulty || 'medium').toLowerCase();
    if (diff === 'easy') {
      easy.push(q);
    } else if (diff === 'hard') {
      hard.push(q);
    } else {
      medium.push(q);
    }
  }

  const nonEmptyBands = [easy.length > 0, medium.length > 0, hard.length > 0].filter(Boolean).length;
  if (nonEmptyBands <= 1) {
    return questions;
  }

  if (masteryTier === 'Not started' || masteryTier === 'Attempted') {
    const primaryBand = shuffleArray([...easy, ...medium]);
    const secondaryBand = shuffleArray(hard);
    return [...primaryBand, ...secondaryBand];
  }

  if (masteryTier === 'Familiar') {
    const shuffledEasy = shuffleArray(easy);
    const shuffledMedium = shuffleArray(medium);
    const shuffledHard = shuffleArray(hard);
    const easyMid = Math.ceil(shuffledEasy.length / 2);
    const hardMid = Math.ceil(shuffledHard.length / 2);

    const primaryBand = shuffleArray([
      ...shuffledMedium,
      ...shuffledEasy.slice(0, easyMid),
      ...shuffledHard.slice(0, hardMid),
    ]);
    const secondaryBand = shuffleArray([
      ...shuffledEasy.slice(easyMid),
      ...shuffledHard.slice(hardMid),
    ]);
    return [...primaryBand, ...secondaryBand];
  }

  const primaryBand = shuffleArray([...hard, ...medium]);
  const secondaryBand = shuffleArray(easy);
  return [...primaryBand, ...secondaryBand];
}

function prepareSessionQuestions(questions, shuffleQuestions = false, expectedCompetencyId, masteryTier) {
  let validatedList = questions;

  if (typeof expectedCompetencyId === 'string' && expectedCompetencyId.trim() !== '') {
    const target = expectedCompetencyId.trim().toLowerCase();
    validatedList = questions.filter((q) => {
      const qComp = (q.competency_id || '').trim().toLowerCase();
      return qComp === target;
    });
  } else if (Array.isArray(expectedCompetencyId) && expectedCompetencyId.length > 0) {
    const allowedSet = new Set(
      expectedCompetencyId.map((id) => String(id).trim().toLowerCase()).filter(Boolean)
    );
    validatedList = questions.filter((q) => {
      const qComp = (q.competency_id || '').trim().toLowerCase();
      return allowedSet.has(qComp);
    });
  }

  let qList = shuffleQuestions ? shuffleArray(validatedList) : [...validatedList];
  if (shuffleQuestions && masteryTier) {
    qList = calibrateByMasteryDifficulty(qList, masteryTier);
  }

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

function buildInterleavedSessionQuestions(
  allQuestions,
  competencies,
  sessionType,
  targetComp,
  masteryTier
) {
  if (sessionType === 'challenge') {
    const shuffled = prepareSessionQuestions(allQuestions, true, undefined, masteryTier);
    return shuffled.slice(0, Math.min(30, shuffled.length));
  }

  if (!targetComp) {
    return [];
  }

  const targetId = targetComp.id.trim().toLowerCase();
  const targetCode = (targetComp.code || '').trim().toLowerCase();
  const matchesComp = (q, comp) => {
    if (!q.competency_id) return false;
    const qComp = q.competency_id.trim().toLowerCase();
    const cId = comp.id.trim().toLowerCase();
    const cCode = (comp.code || '').trim().toLowerCase();
    return qComp === cId || (cCode !== '' && qComp === cCode);
  };

  const targetPool = allQuestions.filter((q) => matchesComp(q, targetComp));
  if (targetPool.length === 0) {
    return [];
  }

  const totalCount =
    sessionType === 'test'
      ? 9
      : sessionType === 'quiz'
      ? 5
      : 4;

  if (sessionType === 'practice') {
    const preparedTarget = prepareSessionQuestions(
      targetPool,
      true,
      targetId || targetCode,
      masteryTier
    );
    return preparedTarget.slice(0, Math.min(totalCount, preparedTarget.length));
  }

  const unitIdx = competencies.findIndex(
    (c) => c.id.trim().toLowerCase() === targetId
  );
  const prereqSet = new Set(
    (targetComp.prerequisites || []).map((p) => p.trim().toLowerCase()).filter(Boolean)
  );

  let priorComps = [];
  if (sessionType === 'quiz') {
    const precedingSlice =
      unitIdx > 0 ? competencies.slice(Math.max(0, unitIdx - 2), unitIdx) : [];
    const explicitPrereqs = competencies.filter(
      (c) =>
        c.id.trim().toLowerCase() !== targetId &&
        (prereqSet.has(c.id.trim().toLowerCase()) ||
          (c.code && prereqSet.has(c.code.trim().toLowerCase())))
    );
    const mergedMap = new Map();
    for (const c of [...explicitPrereqs, ...precedingSlice]) {
      mergedMap.set(c.id.trim().toLowerCase(), c);
    }
    priorComps = Array.from(mergedMap.values()).slice(-2);
  } else if (sessionType === 'test') {
    const precedingAll = unitIdx > 0 ? competencies.slice(0, unitIdx) : [];
    const explicitPrereqs = competencies.filter(
      (c) =>
        c.id.trim().toLowerCase() !== targetId &&
        (prereqSet.has(c.id.trim().toLowerCase()) ||
          (c.code && prereqSet.has(c.code.trim().toLowerCase())))
    );
    const mergedMap = new Map();
    for (const c of [...precedingAll, ...explicitPrereqs]) {
      mergedMap.set(c.id.trim().toLowerCase(), c);
    }
    priorComps = Array.from(mergedMap.values());
  }

  const priorPool =
    priorComps.length > 0
      ? allQuestions.filter((q) => priorComps.some((c) => matchesComp(q, c)))
      : [];

  if (priorPool.length === 0) {
    const preparedTarget = prepareSessionQuestions(
      targetPool,
      true,
      targetId || targetCode,
      masteryTier
    );
    return preparedTarget.slice(0, Math.min(totalCount, preparedTarget.length));
  }

  const allowedPriorIds = Array.from(
    new Set(priorComps.flatMap((c) => [c.id, c.code || '']).filter(Boolean))
  );

  const preparedTarget = prepareSessionQuestions(
    targetPool,
    true,
    targetId || targetCode,
    masteryTier
  );
  const preparedPrior = prepareSessionQuestions(
    priorPool,
    true,
    allowedPriorIds,
    masteryTier
  );

  const desiredTargetCount = sessionType === 'quiz' ? 3 : 5;
  const desiredPriorCount = totalCount - desiredTargetCount;

  const chosenTarget = preparedTarget.slice(0, desiredTargetCount);
  const chosenPrior = preparedPrior.slice(0, desiredPriorCount);

  let combined = [...chosenTarget, ...chosenPrior];

  if (combined.length < totalCount) {
    const usedIds = new Set(combined.map((q) => q.id));
    const remainingTarget = preparedTarget.filter((q) => !usedIds.has(q.id));
    const remainingPrior = preparedPrior.filter((q) => !usedIds.has(q.id));
    for (const extra of [...remainingTarget, ...remainingPrior]) {
      if (combined.length >= totalCount) break;
      combined.push(extra);
    }
  }

  return shuffleArray(combined);
}

// Mock question generator
function createMockQuestion(id, competencyId, stem, difficulty = 'medium') {
  return {
    id,
    competency_id: competencyId,
    type: 'multiple_choice_7_options',
    difficulty,
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

// Create a mixed pool of questions across 4 different units / competencies
const mixedPool = [
  createMockQuestion('q1', 'H-01', 'Polinomio caracteristico 1', 'easy'),
  createMockQuestion('q2', 'H-01', 'Polinomio caracteristico 2', 'medium'),
  createMockQuestion('q3', 'H-02', 'Formula cuadratica 1', 'easy'),
  createMockQuestion('q4', 'H-02', 'Formula cuadratica 2', 'medium'),
  createMockQuestion('q5', 'H-03', 'Inversa matricial 1', 'easy'),
  createMockQuestion('q6', 'H-03', 'Inversa matricial 2', 'medium'),
  createMockQuestion('q7', 'H-03', 'Inversa matricial 3', 'hard'),
  createMockQuestion('q8', 'C-05', 'Modelo IS-LM dinamico 1', 'medium'),
  createMockQuestion('q9', 'C-05', 'Modelo IS-LM dinamico 2', 'hard'),
  createMockQuestion('q10', 'C-05', 'Modelo IS-LM dinamico 3', 'easy'),
  createMockQuestion('q11', 'C-05', 'Modelo IS-LM dinamico 4', 'medium'),
  createMockQuestion('q12', 'C-05', 'Modelo IS-LM dinamico 5', 'hard'),
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

// Test 3: Horizon 1 P3 — Blocked Practice vs Interleaved Quiz & Cumulative Unit Test
{
  const mockCompetencies = [
    { id: 'H-01', code: 'HEC-01', name: 'Polinomio', category: 'Fact', description: '', mastery_target: 100 },
    { id: 'H-02', code: 'HEC-02', name: 'Cuadratica', category: 'Fact', description: '', mastery_target: 100 },
    { id: 'H-03', code: 'HEC-03', name: 'Inversa Matricial 2x2', category: 'Fact', description: '', mastery_target: 100 },
    { id: 'C-05', code: 'CON-05', name: 'IS-LM Dinamico', category: 'Concept', description: '', mastery_target: 100 },
    { id: 'H-99', code: 'HEC-99', name: 'Empty Unit', category: 'Fact', description: '', mastery_target: 100 },
  ];

  // Case A: Practice session for H-03 remains 100% isolated to H-03
  const practiceH03 = buildInterleavedSessionQuestions(mixedPool, mockCompetencies, 'practice', mockCompetencies[2]);
  assert.strictEqual(practiceH03.length, 3, 'Practice pool must strictly contain 3 H-03 questions');
  assert.ok(practiceH03.every((q) => q.competency_id === 'H-03'), 'Practice must never leak other units');

  // Case B: Quiz for H-03 (index 2) interleaves H-03 (3 items) with preceding H-01/H-02 (2 items)
  const quizH03 = buildInterleavedSessionQuestions(mixedPool, mockCompetencies, 'quiz', mockCompetencies[2]);
  assert.strictEqual(quizH03.length, 5, 'Quiz for H-03 must have 5 interleaved questions');
  const quizTargetCount = quizH03.filter((q) => q.competency_id === 'H-03').length;
  const quizPriorCount = quizH03.filter((q) => q.competency_id === 'H-01' || q.competency_id === 'H-02').length;
  assert.strictEqual(quizTargetCount, 3, 'Quiz must include 3 questions from target unit H-03');
  assert.strictEqual(quizPriorCount, 2, 'Quiz must interleave 2 questions from preceding units H-01/H-02');
  assert.ok(quizH03.every((q) => q.competency_id !== 'C-05'), 'Quiz must never pull from future units (C-05)');

  // Case C: Unit Test for C-05 (index 3) interleaves C-05 (5 items) with preceding H-01..H-03 (4 items)
  const testC05 = buildInterleavedSessionQuestions(mixedPool, mockCompetencies, 'test', mockCompetencies[3]);
  assert.strictEqual(testC05.length, 9, 'Unit Test for C-05 must have 9 cumulative interleaved questions');
  const testTargetCount = testC05.filter((q) => q.competency_id === 'C-05').length;
  const testPriorCount = testC05.filter((q) => ['H-01', 'H-02', 'H-03'].includes(q.competency_id)).length;
  assert.strictEqual(testTargetCount, 5, 'Unit Test must include 5 questions from target unit C-05');
  assert.strictEqual(testPriorCount, 4, 'Unit Test must interleave 4 questions from prior units');

  // Case D: Empty competency must NEVER fallback to course questions
  const poolEmpty = buildInterleavedSessionQuestions(mixedPool, mockCompetencies, 'practice', mockCompetencies[4]);
  assert.strictEqual(poolEmpty.length, 0, 'Empty competency must yield 0 questions, NOT fallback to course');
}

// Test 4: Horizon 1 P4 — ZPD Difficulty Calibration by MasteryTier
{
  const compPool = [
    createMockQuestion('e1', 'HAB-1', 'Easy 1', 'easy'),
    createMockQuestion('e2', 'HAB-1', 'Easy 2', 'easy'),
    createMockQuestion('m1', 'HAB-1', 'Med 1', 'medium'),
    createMockQuestion('m2', 'HAB-1', 'Med 2', 'medium'),
    createMockQuestion('m3', 'HAB-1', 'Med 3', 'medium'),
    createMockQuestion('m4', 'HAB-1', 'Med 4', 'medium'),
    createMockQuestion('m5', 'HAB-1', 'Med 5', 'medium'),
    createMockQuestion('h1', 'HAB-1', 'Hard 1', 'hard'),
    createMockQuestion('h2', 'HAB-1', 'Hard 2', 'hard'),
    createMockQuestion('h3', 'HAB-1', 'Hard 3', 'hard'),
  ];

  // Novice ('Not started'): first 4 items must come exclusively from easy + medium band (0 hard items)
  for (let i = 0; i < 25; i++) {
    const noviceSession = prepareSessionQuestions(compPool, true, 'HAB-1', 'Not started').slice(0, 4);
    assert.ok(
      noviceSession.every((q) => q.difficulty === 'easy' || q.difficulty === 'medium'),
      'Not started session of 4 items must scaffold with easy/medium items before hard items'
    );
  }

  // Advanced ('Proficient'): first 4 items must come exclusively from hard + medium band (0 easy items)
  for (let i = 0; i < 25; i++) {
    const advancedSession = prepareSessionQuestions(compPool, true, 'HAB-1', 'Proficient').slice(0, 4);
    assert.ok(
      advancedSession.every((q) => q.difficulty === 'hard' || q.difficulty === 'medium'),
      'Proficient session of 4 items must prioritize hard/medium items over easy items'
    );
  }
}

console.log('ALL UNIT ISOLATION, INTERLEAVING & ZPD CALIBRATION TESTS PASSED (100% SUCCESS)!');
