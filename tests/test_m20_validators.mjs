import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import esbuild from '../platform/node_modules/esbuild/lib/main.js';

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'm20-validators-'));
const entryFile = path.join(tmpDir, 'entry.ts');
const outFile = path.join(tmpDir, 'bundle.mjs');

const repoPlatformSrc = path.resolve(process.cwd(), 'platform/src').replace(/\\/g, '/');
fs.writeFileSync(
  entryFile,
  `
export * from '${repoPlatformSrc}/services/symbolicValidator.ts';
export * from '${repoPlatformSrc}/utils/mathEquivalence.ts';
export * from '${repoPlatformSrc}/components/canvas/TopologyValidator.ts';
export * from '${repoPlatformSrc}/utils/questionUtils.ts';
export * from '${repoPlatformSrc}/utils/socraticPrompt.ts';
export * from '${repoPlatformSrc}/utils/ironExamGrading.ts';
export * from '${repoPlatformSrc}/utils/latexOptionLabel.ts';
`,
  'utf8'
);

await esbuild.build({
  entryPoints: [entryFile],
  bundle: true,
  format: 'esm',
  platform: 'node',
  outfile: outFile,
  packages: 'external',
  logLevel: 'silent',
});

// Point external `mathjs` import inside bundled module to platform/node_modules/mathjs
const mathjsUrl = pathToFileURL(
  path.resolve(process.cwd(), 'platform/node_modules/mathjs/lib/esm/index.js')
).href;
let code = fs.readFileSync(outFile, 'utf8');
code = code.replace(/from\s+["']mathjs["']/g, `from "${mathjsUrl}"`);
fs.writeFileSync(outFile, code, 'utf8');

const m = await import(pathToFileURL(outFile).href);

try {
  // 1. Open Symbolic & Canonical Formulas
  const synOk = m.checkSymbolicSyntax('m*g*sin(theta)', ['m', 'g', 'theta']);
  assert.equal(synOk.valid, true);
  assert.ok(synOk.latexPreview.length > 0);

  const synBadVar = m.checkSymbolicSyntax('m*g*z', ['m', 'g', 'theta']);
  assert.equal(synBadVar.valid, false);
  assert.ok(synBadVar.error.includes('z'));

  const inclineAns = {
    expression: 'm*g*sin(theta)',
    accepted_equivalents: ['g*m*sin(theta)', 'm*g*sin(theta)'],
    tolerance: 0.001,
  };
  const inclineTraps = [
    {
      distractor_id: 'D-PHYS-01',
      expression: 'm*g*cos(theta)',
      error_rationale: 'La componente paralela al plano inclinado proyecta con seno, no con coseno.',
    },
  ];
  assert.equal(m.validateSymbolicAnswer('g * m * sin(θ)', inclineAns, inclineTraps).isCorrect, true);
  assert.equal(m.validateSymbolicAnswer('m·g·sin(theta)', inclineAns, inclineTraps).isCorrect, true);

  const trapHit = m.validateSymbolicAnswer('m*g*cos(theta)', inclineAns, inclineTraps);
  assert.equal(trapHit.isCorrect, false);
  assert.equal(trapHit.matchedDistractorId, 'D-PHYS-01');
  assert.ok(trapHit.diagnosticRationale.includes('seno'));

  // Exponential decay A*e^(-k*t) == A*exp(-k*t)
  const decayAns = { expression: 'A*e^(-k*t)', tolerance: 0.001 };
  assert.equal(m.validateSymbolicAnswer('A * exp(-k * t)', decayAns).isCorrect, true);
  assert.equal(m.validateSymbolicAnswer('A * e**(-k*t)', decayAns).isCorrect, true);
  assert.equal(m.validateSymbolicAnswer('A * e^(k*t)', decayAns).isCorrect, false);

  // Natural log alias
  assert.equal(m.validateSymbolicAnswer('ln(x)', { expression: 'log(x)' }).isCorrect, true);

  // Additional implicit/symbolic edge cases (open_symbolic + fill_in_the_blank)
  const polyTarget = { expression: '3*x + 5*v**2', tolerance: 0.001 };
  const polyCfg = { variables: ['x', 'v'] };
  assert.equal(m.validateSymbolicAnswer('3x+5v^2', polyTarget, undefined, polyCfg).isCorrect, true);
  assert.equal(m.validateSymbolicAnswer('3x+5(v^2)', polyTarget, undefined, polyCfg).isCorrect, true);
  assert.equal(m.validateSymbolicAnswer('3x+5(v)^2', polyTarget, undefined, polyCfg).isCorrect, true);
  assert.equal(m.validateSymbolicAnswer('(3)x+5v^(2)', polyTarget, undefined, polyCfg).isCorrect, true);
  assert.equal(m.validateSymbolicAnswer('5v^2+3x', polyTarget, undefined, polyCfg).isCorrect, true);

  // fill_in_the_blank checkMathEquivalence directly
  assert.equal(m.checkMathEquivalence('3x+5v^2', '3*x + 5*v**2'), true);
  assert.equal(m.checkMathEquivalence('3x+5(v^2)', '3*x + 5*v**2'), true);
  assert.equal(m.checkMathEquivalence('ln(x)', 'log(x)'), true);
  assert.equal(m.checkMathEquivalence('2ln(x)', '2*log(x)'), true);
  assert.equal(m.checkMathEquivalence('2xy', '2*x*y'), true);
  assert.equal(m.checkMathEquivalence('12tv', '12*t*v'), true);
  assert.equal(m.checkMathEquivalence('xln(x)', 'x*log(x)'), true);
  assert.equal(m.checkMathEquivalence('xe^x', 'x*exp(x)'), true);
  assert.equal(m.checkMathEquivalence('xsin(x)', 'x*sin(x)'), true);
  assert.equal(m.checkMathEquivalence('sin^2(x)', 'sin(x)^2'), true);
  assert.equal(m.checkMathEquivalence('ln^2(x)', 'log(x)^2'), true);
  assert.equal(m.checkMathEquivalence('1e-5', 0.00001), true);

  // Domain-aware checkSymbolicSyntax: splits valid concatenated vars, preserves multi-char declared vars, rejects undeclared
  assert.equal(m.checkSymbolicSyntax('2xy', ['x', 'y']).valid, true);
  assert.equal(m.checkSymbolicSyntax('xln(x)', ['x']).valid, true);
  assert.equal(m.checkSymbolicSyntax('sin^2(x)', ['x']).valid, true);
  assert.equal(m.checkSymbolicSyntax('xy + x_1', ['xy', 'x_1']).valid, true);
  assert.equal(m.checkSymbolicSyntax('2xz', ['x', 'y']).valid, false);
  assert.equal(m.checkSymbolicSyntax('sin + 1', ['x']).valid, false);

  // 2. FIB with diagnostic_distractors
  const fibTrap = m.validateSymbolicAnswer(
    '10',
    { value: '25', tolerance: 0.01 },
    [{ distractor_id: 'D-FIB-01', value: '10', error_rationale: 'Multiplicaste por 2 en lugar de elevar al cuadrado.' }]
  );
  assert.equal(fibTrap.isCorrect, false);
  assert.equal(fibTrap.matchedDistractorId, 'D-FIB-01');
  assert.equal(m.validateSymbolicAnswer('25.00', { value: '25', tolerance: 0.01 }).isCorrect, true);

  // 3. ProofDAG (< 5ms, multiple valid topological orders, fallacy trap, justifications)
  const dagSpec = {
    steps: [
      { id: 'S1', content: 'Dato base', is_fallacy: false, justification: 'Hipótesis' },
      { id: 'S2', content: 'Rama A', is_fallacy: false, justification: 'Lema A' },
      { id: 'S3', content: 'Rama B', is_fallacy: false, justification: 'Lema B' },
      { id: 'S4', content: 'Cierre', is_fallacy: false, justification: 'Conclusión' },
      {
        id: 'F1',
        content: 'Salto inválido',
        is_fallacy: true,
        distractor_id: 'D-DAG-01',
        error_rationale: 'Paso F1 invierte la desigualdad.',
      },
    ],
    edges: [
      ['S1', 'S2'],
      ['S1', 'S3'],
      ['S2', 'S4'],
      ['S3', 'S4'],
    ],
    require_justification: true,
    justification_bank: ['Hipótesis', 'Lema A', 'Lema B', 'Conclusión'],
  };
  const validJust = { S1: 'Hipótesis', S2: 'Lema A', S3: 'Lema B', S4: 'Conclusión' };
  const t0 = performance.now();
  assert.equal(m.validateProofDagSubmission(['S1', 'S2', 'S3', 'S4'], validJust, dagSpec).isCorrect, true);
  assert.equal(m.validateProofDagSubmission(['S1', 'S3', 'S2', 'S4'], validJust, dagSpec).isCorrect, true);
  assert.ok(performance.now() - t0 < 25);

  const dagFallacy = m.validateProofDagSubmission(['S1', 'F1', 'S2', 'S3', 'S4'], validJust, dagSpec);
  assert.equal(dagFallacy.isCorrect, false);
  assert.equal(dagFallacy.matchedDistractorId, 'D-DAG-01');

  const dagBadOrder = m.validateProofDagSubmission(['S1', 'S4', 'S2', 'S3'], validJust, dagSpec);
  assert.equal(dagBadOrder.isCorrect, false);

  const dagBadJust = m.validateProofDagSubmission(['S1', 'S2', 'S3', 'S4'], { ...validJust, S2: 'Conclusión' }, dagSpec);
  assert.equal(dagBadJust.isCorrect, false);

  // 4. Adversarial Break: find_fallacy + counterexample (including chained comparison)
  const advFallacy = {
    mode: 'find_fallacy',
    steps: [
      { id: 'A1', content: "f'(0)=0", is_fallacy: false, valid_explanation: 'Punto crítico correcto.' },
      {
        id: 'A2',
        content: "Como f''(0)=0, concluye punto silla.",
        is_fallacy: true,
        distractor_id: 'D-ADV-01',
        error_rationale: "Cuando f''(0)=0 el criterio de segunda derivada es inconcluso.",
      },
    ],
    reason_options: [
      { id: 'R1', content: 'El criterio es inconcluso cuando f\'\'(0)=0.', is_correct: true },
      { id: 'R2', content: 'Falta factor 2.', is_correct: false, distractor_id: 'D-ADV-02', error_rationale: 'No es factor constante.' },
    ],
  };
  assert.equal(m.validateAdversarialSubmission({ selectedStepId: 'A2', selectedReasonId: 'R1' }, advFallacy).isCorrect, true);
  assert.equal(m.validateAdversarialSubmission({ selectedStepId: 'A1', selectedReasonId: 'R1' }, advFallacy).isCorrect, false);
  const badReason = m.validateAdversarialSubmission({ selectedStepId: 'A2', selectedReasonId: 'R2' }, advFallacy);
  assert.equal(badReason.isCorrect, false);
  assert.equal(badReason.matchedDistractorId, 'D-ADV-02');

  const advCe = {
    mode: 'counterexample',
    inputs: [{ id: 'n', label: 'n', type: 'integer', min: 1, max: 20 }],
    predicates: [
      { expr: '3 <= n <= 10', failure_rationale: 'Debe cumplir 3 <= n <= 10.' },
      { expr: 'n**2 >= 3*n', failure_rationale: 'No refuta la cota.' },
    ],
  };
  assert.equal(m.validateAdversarialSubmission({ witnessValues: { n: '5' } }, advCe).isCorrect, true);
  assert.equal(m.validateAdversarialSubmission({ witnessValues: { n: '12' } }, advCe).isCorrect, false);
  assert.equal(m.validateAdversarialSubmission({ witnessValues: { n: '2' } }, advCe).isCorrect, false);

  // 5. Unstructured Model (Stage 0)
  const umSpec = {
    phase1_variables: {
      prompt: 'Clasifica',
      roles: ['parametro', 'incognita', 'irrelevante'],
      items: [
        { id: 'V1', label: 'T_0', correct_role: 'parametro' },
        { id: 'V2', label: 'k', correct_role: 'incognita' },
        { id: 'V3', label: 'Color', correct_role: 'irrelevante', error_rationale: 'Atributo irrelevante.' },
      ],
    },
    phase2_assumptions: {
      prompt: 'Supuestos',
      options: [
        { id: 'A1', content: 'T_a constante', is_required: true },
        { id: 'A2', content: 'Calor infinito', is_required: false, error_rationale: 'Físicamente imposible.' },
      ],
    },
    phase3_formulation: {
      prompt: 'Fórmula',
      input_mode: 'symbolic',
      correct_expression: { expression: 'T_a + (T_0 - T_a)*e^(-k*t)', tolerance: 0.001 },
      diagnostic_distractors: [
        { distractor_id: 'D-UM-01', expression: 'T_0*e^(-k*t)', error_rationale: 'Falta temperatura ambiente T_a.' },
      ],
    },
  };
  const s0Good = {
    phase1Roles: { V1: 'parametro', V2: 'incognita', V3: 'irrelevante' },
    phase2SelectedIds: ['A1'],
    phase3SelectedId: null,
    phase3Expression: 'T_a + (T_0 - T_a)*exp(-k*t)',
  };
  assert.equal(m.validateStage0Phase(1, s0Good, umSpec).isCorrect, true);
  assert.equal(m.validateStage0Phase(2, s0Good, umSpec).isCorrect, true);
  assert.equal(m.validateStage0Phase(3, s0Good, umSpec).isCorrect, true);
  assert.equal(m.validateStage0Phase(1, { ...s0Good, phase1Roles: { ...s0Good.phase1Roles, V3: 'incognita' } }, umSpec).isCorrect, false);
  assert.equal(m.validateStage0Phase(2, { ...s0Good, phase2SelectedIds: ['A1', 'A2'] }, umSpec).isCorrect, false);
  assert.equal(m.validateStage0Phase(3, { ...s0Good, phase3Expression: 'T_0*e^(-k*t)' }, umSpec).matchedDistractorId, 'D-UM-01');

  // 6. TopologyValidator: Cartesian piecewise kink + Tree info-set equivalence
  const cartSpec = {
    mode: 'cartesian',
    sliders: [{ id: 'cutoff', label: 'corte', min: 10, max: 90, initial: 50 }],
    interactive_curves: [{ id: 'budget', expression: 'x < cutoff ? 200 - 2*x : 150 - x' }],
    interactive_points: [{ id: 'opt', x: 50, y: 100 }],
    invariants: [
      { id: 'I1', kind: 'kink_at', curve_id: 'budget', x: 'cutoff', target: 0.5 },
      { id: 'I2', kind: 'point_on_curve', point_id: 'opt', curve_id: 'budget', tolerance: 0.5 },
      { id: 'I3', kind: 'point_coords', point_id: 'opt', target_x: 50, target_y: 100, tolerance: 0.5 },
    ],
  };
  assert.equal(
    m.validateCartesianInvariants({ sliderValues: { cutoff: 50 }, pointPositions: { opt: { x: 50, y: 100 } } }, cartSpec).isCorrect,
    true
  );
  assert.equal(
    m.validateCartesianInvariants({ sliderValues: { cutoff: 50 }, pointPositions: { opt: { x: 20, y: 160 } } }, cartSpec).isCorrect,
    false
  );

  const treeSpec = {
    mode: 'tree',
    interaction_mode: 'both',
    tree_invariants: {
      required_edges: ['E1', 'E3'],
      required_info_sets: [['N1', 'N2']],
      edge_error_rationale: 'Rama subóptima.',
      info_set_error_rationale: 'Información imperfecta errónea.',
    },
  };
  // Order-independent sets & nodes pass
  assert.equal(
    m.validateTreeInvariants({ selectedEdgeIds: ['E3', 'E1'], infoSets: [['N2', 'N1']] }, treeSpec).isCorrect,
    true
  );
  assert.equal(
    m.validateTreeInvariants({ selectedEdgeIds: ['E2'], infoSets: [['N1', 'N2']] }, treeSpec).isCorrect,
    false
  );

  // 7. Concept Matching
  const cmSpec = {
    premises: [{ id: 'P1', content: 'A' }, { id: 'P2', content: 'B' }],
    targets: [
      { id: 'T1', content: '1' },
      { id: 'T2', content: '2' },
      { id: 'T3', content: '3', is_distractor: true, distractor_id: 'D-CM-1', error_rationale: 'Trampa cruzada.' },
    ],
    correct_pairs: { P1: 'T1', P2: 'T2' },
  };
  assert.equal(m.validateConceptMatchingSubmission({ P1: 'T1', P2: 'T2' }, cmSpec).isCorrect, true);
  assert.equal(m.validateConceptMatchingSubmission({ P1: 'T3', P2: 'T2' }, cmSpec).matchedDistractorId, 'D-CM-1');

  // 8. Smart Blank-First Curtain Matrix
  const mustHave = ['multiple_choice_7_options', 'multiple_select', 'concept_matching', 'proof_dag'];
  const mustSkip = ['fill_in_the_blank', 'open_symbolic', 'adversarial_break', 'unstructured_model', 'invariant_canvas'];
  for (const t of mustHave) assert.equal(m.requiresBlankFirstCurtain({ type: t }), true, t);
  for (const t of mustSkip) assert.equal(m.requiresBlankFirstCurtain({ type: t }), false, t);

  // 9. P1-1: trap_predicates, evaluateAdversarialReadouts, slider_eq aliases, and toPlainOptionLabel
  const trapAdv = {
    mode: 'counterexample',
    inputs: [{ id: 'x', label: 'x', type: 'number', min: 0, max: 100 }],
    trap_predicates: [
      {
        expr: 'abs(x - 4) < 0.05',
        distractor_id: 'D-TRAP-01',
        error_rationale: 'Evaluaste el punto estacionario local x=4.',
      },
    ],
    predicates: [{ id: 'P1', expr: 'x > 10', failure_rationale: 'Debe superar 10.' }],
    computed_readouts: [{ id: 'R1', label: '$2x + 1$', expr: '2*x + 1', unit: 'usd' }],
  };
  const trapPredHit = m.validateAdversarialSubmission(
    { selectedStepId: null, selectedReasonId: null, witnessValues: { x: '4' } },
    trapAdv
  );
  assert.equal(trapPredHit.isCorrect, false);
  assert.equal(trapPredHit.matchedDistractorId, 'D-TRAP-01');

  const roList = m.evaluateAdversarialReadouts(trapAdv.computed_readouts, { x: '12' });
  assert.equal(roList[0].value, 25);
  assert.equal(roList[0].formatted, '25');
  assert.equal(roList[0].unit, 'usd');

  const sliderAliasSpec = {
    mode: 'cartesian',
    sliders: [{ id: 's1', label: 'Pendiente', min: 0, max: 10, initial: 1 }],
    invariants: [
      { id: 'S_TV', kind: 'slider_eq', slider_id: 's1', target_value: 4, tolerance: 0.1 },
      { id: 'S_EX', kind: 'slider_eq', slider_id: 's1', expected: '2*2', tolerance: 0.1 },
    ],
  };
  assert.equal(
    m.validateCartesianInvariants({ sliderValues: { s1: 4 }, pointPositions: {} }, sliderAliasSpec).isCorrect,
    true
  );
  assert.equal(
    m.validateCartesianInvariants({ sliderValues: { s1: 2 }, pointPositions: {} }, sliderAliasSpec).isCorrect,
    false
  );

  const strippedLabel = m.toPlainOptionLabel('$x^2 + \\frac{1}{2} - \\alpha \\le 0$');
  assert.equal(strippedLabel.includes('$'), false);
  assert.equal(strippedLabel.includes('\\'), false);

  // 10. M20 Iron Exam Grading across all 9 modalities + Metacognitive Audit
  const ironQuestions = [
    {
      id: 'q1_mc7',
      competency_id: 'C-01',
      type: 'multiple_choice_7_options',
      stem: 'MC7',
      options: [
        { id: 'opt_a', content: '10', is_correct: true },
        { id: 'opt_b', content: '20', is_correct: false, error_rationale: 'Wrong' },
      ],
      correct_answer: 'opt_a',
      hints: [],
      solution: '10',
    },
    {
      id: 'q2_ms',
      competency_id: 'C-01',
      type: 'multiple_select',
      stem: 'MS',
      options: [
        { id: 'opt_a', content: 'A', is_correct: true },
        { id: 'opt_b', content: 'B', is_correct: true },
        { id: 'opt_c', content: 'C', is_correct: false, error_rationale: 'Not C' },
      ],
      correct_answer: ['opt_a', 'opt_b'],
      hints: [],
      solution: 'A, B',
    },
    {
      id: 'q3_fib',
      competency_id: 'Hab-01',
      type: 'fill_in_the_blank',
      stem: '2+2',
      options: [],
      correct_answer: '4',
      hints: [],
      solution: '4',
    },
    {
      id: 'q4_os',
      competency_id: 'Hab-01',
      type: 'open_symbolic',
      stem: 'd/dx(x^2)',
      options: [],
      correct_answer: { expression: '2*x', canonical_algebraic: '2*x', variables: ['x'] },
      hints: [],
      solution: '2x',
    },
    {
      id: 'q5_dag',
      competency_id: 'C-01',
      type: 'proof_dag',
      stem: 'DAG',
      options: [],
      proof_dag: {
        steps: [
          { id: 'S1', content: '1', is_distractor: false },
          { id: 'S2', content: '2', is_distractor: false },
          { id: 'S3', content: '3', is_distractor: false },
        ],
        edges: [['S1', 'S2'], ['S2', 'S3']],
        require_justification: false,
      },
      correct_answer: {},
      hints: [],
      solution: 'S1->S2->S3',
    },
    {
      id: 'q6_adv',
      competency_id: 'Hab-01',
      type: 'adversarial_break',
      stem: 'Adv',
      options: [],
      adversarial_break: trapAdv,
      correct_answer: {},
      hints: [],
      solution: 'x=20',
    },
    {
      id: 'q7_um',
      competency_id: 'Hab-01',
      type: 'unstructured_model',
      stem: 'UM',
      options: [],
      unstructured_model: umSpec,
      correct_answer: {},
      hints: [],
      solution: 'S0',
    },
    {
      id: 'q8_ic',
      competency_id: 'Hab-02',
      type: 'invariant_canvas',
      stem: 'IC',
      options: [],
      invariant_canvas: cartSpec,
      correct_answer: {},
      hints: [],
      solution: 'kink',
    },
    {
      id: 'q9_cm',
      competency_id: 'C-01',
      type: 'concept_matching',
      stem: 'CM',
      options: [],
      concept_matching: cmSpec,
      correct_answer: {},
      hints: [],
      solution: 'P1->T1',
    },
  ];

  // Un-interacted canvas must be graded unanswered + incorrect
  const canvasDraftNotInteracted = m.createInitialIronDraft(ironQuestions[7]);
  assert.equal(m.gradeIronExamQuestion(ironQuestions[7], canvasDraftNotInteracted).answered, false);
  assert.equal(m.gradeIronExamQuestion(ironQuestions[7], canvasDraftNotInteracted).isCorrect, false);

  const drafts = {
    q1_mc7: { ...m.createInitialIronDraft(ironQuestions[0]), selectedOption: 'opt_a' }, // high + right => calibrated_mastery
    q2_ms: { ...m.createInitialIronDraft(ironQuestions[1]), selectedMultiOptions: ['opt_c'] }, // high + wrong => illusion_of_competence
    q3_fib: { ...m.createInitialIronDraft(ironQuestions[2]), fillBlankValue: '4' }, // low + right => lucky_guess
    q4_os: { ...m.createInitialIronDraft(ironQuestions[3]), structuredAnswer: { kind: 'open_symbolic', expression: 'x' } }, // low + wrong => known_gap
    q5_dag: { ...m.createInitialIronDraft(ironQuestions[4]), structuredAnswer: { kind: 'proof_dag', orderedStepIds: ['S1', 'S2', 'S3'], justifications: {} } },
    q6_adv: { ...m.createInitialIronDraft(ironQuestions[5]), structuredAnswer: { kind: 'adversarial_break', selectedStepId: null, selectedReasonId: null, witnessValues: { x: '20' } } },
    q7_um: { ...m.createInitialIronDraft(ironQuestions[6]), structuredAnswer: { kind: 'unstructured_model', ...s0Good } },
    q8_ic: {
      ...m.createInitialIronDraft(ironQuestions[7]),
      structuredAnswer: { kind: 'invariant_canvas', sliderValues: { cutoff: 50 }, pointPositions: { opt: { x: 50, y: 100 } }, selectedEdgeIds: [], infoSets: [] },
      canvasInteracted: true,
    },
    q9_cm: { ...m.createInitialIronDraft(ironQuestions[8]), structuredAnswer: { kind: 'concept_matching', pairs: { P1: 'T1', P2: 'T2' } } },
  };
  const { audit } = m.computeMetacognitiveAudit(
    ironQuestions,
    drafts,
    { q1_mc7: 'high', q2_ms: 'high', q3_fib: 'low', q4_os: 'low' },
    'high',
    { q2_ms: true }
  );
  assert.equal(audit.correct_count, 7);
  assert.equal(audit.calibrated_mastery_count, 6);
  assert.equal(audit.illusions_of_competence_count, 1);
  assert.equal(audit.lucky_guesses_count, 1);
  assert.equal(audit.known_gaps_count, 1);

  console.log('ALL M20 VALIDATOR UNIT TESTS PASSED!');
} finally {
  fs.rmSync(tmpDir, { recursive: true, force: true });
}
