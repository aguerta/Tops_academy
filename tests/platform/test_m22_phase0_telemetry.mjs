import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.resolve(__dirname, '..', '..');

const require = createRequire(import.meta.url);
const esbuild = require(path.join(ROOT_DIR, 'platform', 'node_modules', 'esbuild'));

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'tops-m22-test-'));

async function loadTsModule(relPath) {
  const entry = path.join(ROOT_DIR, relPath);
  const outFile = path.join(tmpDir, `${path.basename(relPath, '.ts')}.mjs`);
  await esbuild.build({
    entryPoints: [entry],
    outfile: outFile,
    bundle: true,
    platform: 'node',
    format: 'esm',
    target: 'node20',
    nodePaths: [path.join(ROOT_DIR, 'platform', 'node_modules')],
    logLevel: 'silent',
  });
  return import(pathToFileURL(outFile).href);
}

function createMemoryStorage() {
  const store = new Map();
  return {
    getItem(key) {
      return store.has(key) ? store.get(key) : null;
    },
    setItem(key, value) {
      store.set(key, String(value));
    },
    removeItem(key) {
      store.delete(key);
    },
    clear() {
      store.clear();
    },
  };
}

function makeEvent(overrides = {}) {
  return {
    id: `ev_${Math.random().toString(36).slice(2, 10)}`,
    timestamp: '2026-11-24T12:00:00.000Z',
    course_id: 'course_a',
    competency_id: 'C1',
    question_id: 'Q1',
    archetype: 'direct',
    modality: 'open_symbolic',
    difficulty: 'medium',
    mastery_tier_before: 'Not started',
    session_mode: 'practice',
    is_unlabeled_probe: false,
    first_attempt_correct: true,
    final_correct: true,
    wrong_attempts: 0,
    exhausted_4_strikes: false,
    hints_used: 0,
    triggered_distractor_ids: [],
    seconds_spent: 15,
    ...overrides,
  };
}

try {
  const telemetry = await loadTsModule('platform/src/utils/m22Telemetry.ts');
  const shuffler = await loadTsModule('platform/src/utils/sessionShuffler.ts');

  console.log('--- STARTING M22 PHASE 0 TELEMETRY & COLD PROBE TESTS ---');

  // 1. Resilient storage & malformed JSON handling
  const originalDescriptor = Object.getOwnPropertyDescriptor(globalThis, 'localStorage');
  Object.defineProperty(globalThis, 'localStorage', {
    configurable: true,
    get() {
      throw new Error('localStorage unavailable');
    },
  });
  assert.deepEqual(telemetry.loadM22Events(), []);
  assert.doesNotThrow(() => telemetry.appendM22Events([makeEvent({ id: 'unavail_1' })]));
  assert.doesNotThrow(() => telemetry.clearM22Events());

  const memStorage = createMemoryStorage();
  Object.defineProperty(globalThis, 'localStorage', {
    configurable: true,
    value: memStorage,
  });

  memStorage.setItem(telemetry.M22_TELEMETRY_STORAGE_KEY, '{malformed_json');
  assert.deepEqual(telemetry.loadM22Events(), []);

  // 2. Append, course filter, and clear
  telemetry.appendM22Events([
    makeEvent({ id: 'e1', course_id: 'course_a' }),
    makeEvent({ id: 'e2', course_id: 'course_b' }),
  ]);
  assert.equal(telemetry.loadM22Events().length, 2);
  assert.equal(telemetry.loadM22Events('course_a').length, 1);
  assert.equal(telemetry.loadM22Events('course_b').length, 1);

  telemetry.clearM22Events('course_a');
  assert.equal(telemetry.loadM22Events().length, 1);
  assert.equal(telemetry.loadM22Events()[0].id, 'e2');
  telemetry.clearM22Events();
  assert.equal(telemetry.loadM22Events().length, 0);

  // 3. FIFO cap at 5,000 events
  const bulk = Array.from({ length: 5005 }, (_, idx) =>
    makeEvent({ id: `bulk_${idx}`, timestamp: `2026-11-24T12:00:${String(idx % 60).padStart(2, '0')}Z` })
  );
  telemetry.appendM22Events(bulk);
  const loadedBulk = telemetry.loadM22Events();
  assert.equal(loadedBulk.length, 5000);
  assert.equal(loadedBulk[0].id, 'bulk_5');
  assert.equal(loadedBulk[4999].id, 'bulk_5004');
  telemetry.clearM22Events();

  // 4. H1-H4 Hypothesis Summary Computation
  const hypothesisEvents = [
    // H1: Not started (2 events: 0/2 first-attempt correct, 2/2 hinted)
    makeEvent({
      id: 'h1_ns_1',
      timestamp: '2026-11-24T10:00:00Z',
      competency_id: 'C1',
      mastery_tier_before: 'Not started',
      first_attempt_correct: false,
      final_correct: false,
      wrong_attempts: 4,
      exhausted_4_strikes: true,
      hints_used: 1,
      triggered_distractor_ids: ['D-01-02'],
    }),
    makeEvent({
      id: 'h1_ns_2',
      timestamp: '2026-11-24T10:01:00Z',
      competency_id: 'C1',
      mastery_tier_before: 'Not started',
      first_attempt_correct: false,
      final_correct: true,
      wrong_attempts: 1,
      hints_used: 2,
      // H2 recurrence of exact D-01-02 on next encounter for C1!
      triggered_distractor_ids: ['D-01-02'],
    }),
    // H2 non-recurrence case on C2
    makeEvent({
      id: 'h2_c2_1',
      timestamp: '2026-11-24T10:02:00Z',
      competency_id: 'C2',
      mastery_tier_before: 'Attempted',
      first_attempt_correct: false,
      final_correct: false,
      wrong_attempts: 4,
      exhausted_4_strikes: true,
      hints_used: 0,
      triggered_distractor_ids: ['D-02-01'],
    }),
    makeEvent({
      id: 'h2_c2_2',
      timestamp: '2026-11-24T10:03:00Z',
      competency_id: 'C2',
      mastery_tier_before: 'Attempted',
      first_attempt_correct: false,
      final_correct: true,
      wrong_attempts: 1,
      exhausted_4_strikes: false,
      hints_used: 0,
      // Different trap -> not a recurrence of D-02-01
      triggered_distractor_ids: ['D-02-99'],
    }),
    // H1 Familiar+ & H4 Proficient/Mastered cold vs hint-assisted
    makeEvent({
      id: 'h4_cold_1',
      timestamp: '2026-11-24T10:04:00Z',
      competency_id: 'C3',
      mastery_tier_before: 'Proficient',
      session_mode: 'cold_transfer_probe',
      is_unlabeled_probe: true,
      first_attempt_correct: false,
      final_correct: false,
      hints_used: 0,
    }),
    makeEvent({
      id: 'h4_hint_1',
      timestamp: '2026-11-24T10:05:00Z',
      competency_id: 'C3',
      mastery_tier_before: 'Mastered',
      session_mode: 'practice',
      is_unlabeled_probe: false,
      first_attempt_correct: true,
      final_correct: true,
      hints_used: 1,
    }),
    makeEvent({
      id: 'h1_fam_1',
      timestamp: '2026-11-24T10:06:00Z',
      competency_id: 'C4',
      mastery_tier_before: 'Familiar',
      session_mode: 'cold_transfer_probe',
      is_unlabeled_probe: true,
      first_attempt_correct: true,
      final_correct: true,
      hints_used: 0,
    }),
  ];

  const summary = telemetry.computeM22HypothesisSummary(hypothesisEvents);
  assert.equal(summary.total_events, 7);

  // H1 checks
  assert.equal(summary.h1_tier_calibration.not_started.n, 2);
  assert.equal(summary.h1_tier_calibration.not_started.first_attempt_accuracy, 0);
  assert.equal(summary.h1_tier_calibration.not_started.hint_rate, 1);
  assert.equal(summary.h1_tier_calibration.familiar_plus.n, 3);
  assert.ok(Math.abs(summary.h1_tier_calibration.familiar_plus.first_attempt_accuracy - 2 / 3) < 1e-9);
  assert.ok(Math.abs(summary.h1_tier_calibration.familiar_plus.hint_rate - 1 / 3) < 1e-9);

  // H2 checks (2 4-strike events with follow-ups: 1 exact recurrence, 1 non-recurrence -> 0.5)
  assert.equal(summary.h2_trap_recurrence.total_4_strike_events, 2);
  assert.equal(summary.h2_trap_recurrence.followed_exposures, 2);
  assert.equal(summary.h2_trap_recurrence.recurrences, 1);
  assert.equal(summary.h2_trap_recurrence.recurrence_rate, 0.5);

  // H3 checks (labeled: 5 events, 1 first-attempt correct = 0.2; unlabeled: 2 events, 1 correct = 0.5)
  assert.equal(summary.h3_unlabeled_transfer.labeled.n, 5);
  assert.equal(summary.h3_unlabeled_transfer.unlabeled_probe.n, 2);
  assert.ok(Math.abs(summary.h3_unlabeled_transfer.accuracy_delta - (0.2 - 0.5)) < 1e-9);

  // H4 checks (Proficient/Mastered: 1 cold 0/1, 1 hint-assisted 1/1)
  assert.equal(summary.h4_hint_dependence.proficient_mastered_cold.n, 1);
  assert.equal(summary.h4_hint_dependence.proficient_mastered_cold.first_attempt_accuracy, 0);
  assert.equal(summary.h4_hint_dependence.proficient_mastered_hint_assisted.n, 1);
  assert.equal(summary.h4_hint_dependence.proficient_mastered_hint_assisted.first_attempt_accuracy, 1);
  assert.equal(summary.h4_hint_dependence.accuracy_delta, 1);
  assert.equal(summary.h4_hint_dependence.hint_assisted_share, 0.5);

  // 5. JSON Export schema
  telemetry.appendM22Events(hypothesisEvents);
  const exported = JSON.parse(telemetry.exportM22EventsAsJson('course_a'));
  assert.equal(exported.schema_version, 'm22_phase0_v1');
  assert.equal(exported.course_id, 'course_a');
  assert.equal(exported.total_events, 7);
  assert.equal(exported.events.length, 7);
  assert.equal(exported.summary.h2_trap_recurrence.recurrence_rate, 0.5);

  // 6. Cold Transfer Probe Shuffler invariants
  const mixedQuestions = [
    { id: 'q_mc', competency_id: 'C1', type: 'multiple_choice_7_options', stem: 'MC', options: [], correct_answer: 'A', hints: [], solution: 's' },
    { id: 'q_ms', competency_id: 'C1', type: 'multiple_select', stem: 'MS', options: [], correct_answer: ['A'], hints: [], solution: 's' },
    { id: 'q_dag', competency_id: 'C2', type: 'proof_dag', stem: 'DAG', options: [], correct_answer: {}, hints: [], solution: 's' },
    { id: 'q_fallacy', competency_id: 'C2', type: 'adversarial_break', adversarial_break: { mode: 'find_fallacy' }, stem: 'AF', options: [], correct_answer: {}, hints: [], solution: 's' },
    { id: 'q_open_1', competency_id: 'C1', type: 'open_symbolic', stem: 'Open 1', options: [], correct_answer: 'x', hints: [], solution: '', detailed_solution: 'normalized sol' },
    { id: 'q_open_2', competency_id: 'C1', type: 'open_symbolic', stem: 'Open 2', options: [], correct_answer: '2x', hints: [], solution: 's' },
    { id: 'q_fitb_1', competency_id: 'C2', type: 'fill_in_the_blank', stem: 'FITB 1', options: [], correct_answer: '42', hints: [], solution: 's' },
    { id: 'q_ce_1', competency_id: 'C3', type: 'adversarial_break', adversarial_break: { mode: 'counterexample' }, stem: 'CE 1', options: [], correct_answer: {}, hints: [], solution: 's' },
    { id: 'q_open_3', competency_id: 'C4', type: 'open_symbolic', stem: 'Open 3', options: [], correct_answer: 'y', hints: [], solution: 's' },
  ];

  const probe4 = shuffler.buildColdTransferProbeQuestions(mixedQuestions, 4);
  assert.equal(probe4.length, 4);
  const allowedTypes = new Set(['open_symbolic', 'fill_in_the_blank', 'adversarial_break']);
  for (const q of probe4) {
    assert.ok(allowedTypes.has(q.type), `Unexpected type in probe: ${q.type}`);
    if (q.type === 'adversarial_break') {
      assert.equal(q.adversarial_break?.mode, 'counterexample');
    }
  }
  // Cross-competency spread: 4 distinct competencies for maxItems=4
  const probe4Comps = new Set(probe4.map((q) => q.competency_id));
  assert.equal(probe4Comps.size, 4, 'Expected 1 item per eligible competency when maxItems=4');

  // Normalization check (detailed_solution -> solution)
  const probeAll = shuffler.buildColdTransferProbeQuestions(mixedQuestions, 8);
  assert.equal(probeAll.length, 5);
  const open1 = probeAll.find((q) => q.id === 'q_open_1');
  assert.ok(open1);
  assert.equal(open1.solution, 'normalized sol');

  // 6b. mergeM22Events & replaceM22Events
  const localMerge = [
    makeEvent({ id: 'm_3', timestamp: '2026-11-24T12:03:00.000Z', question_id: 'Q3' }),
    makeEvent({ id: 'm_1', timestamp: '2026-11-24T12:01:00.000Z', question_id: 'Q1_local' }),
  ];
  const remoteMerge = [
    makeEvent({ id: 'm_1', timestamp: '2026-11-24T12:01:00.000Z', question_id: 'Q1_remote' }),
    makeEvent({ id: 'm_2', timestamp: '2026-11-24T12:02:00.000Z', question_id: 'Q2' }),
    makeEvent({ id: 'm_0', timestamp: 'not-a-date', question_id: 'Q0' }),
  ];
  const mergedEvents = telemetry.mergeM22Events(localMerge, remoteMerge);
  assert.deepEqual(
    mergedEvents.map((e) => e.id),
    ['m_0', 'm_1', 'm_2', 'm_3'],
    'mergeM22Events must deduplicate by id and sort chronologically (invalid timestamps -> 0)'
  );
  assert.equal(mergedEvents[1].question_id, 'Q1_local', 'dedup should prefer local event on id collision');

  // 5,000 FIFO cap in mergeM22Events
  const localBulk = Array.from({ length: 3000 }, (_, i) =>
    makeEvent({
      id: `cap_l_${i}`,
      timestamp: new Date(Date.UTC(2026, 10, 24, 0, 0, i)).toISOString(),
    })
  );
  const remoteBulk = Array.from({ length: 2500 }, (_, i) =>
    makeEvent({
      id: `cap_r_${i}`,
      timestamp: new Date(Date.UTC(2026, 10, 24, 1, 0, i)).toISOString(),
    })
  );
  const mergedCapped = telemetry.mergeM22Events(localBulk, remoteBulk);
  assert.equal(mergedCapped.length, 5000);
  assert.equal(mergedCapped[0].id, 'cap_l_500');
  assert.equal(mergedCapped[4999].id, 'cap_r_2499');

  // replaceM22Events writes capped array to storage
  telemetry.replaceM22Events(mergedEvents);
  assert.deepEqual(
    telemetry.loadM22Events().map((e) => e.id),
    ['m_0', 'm_1', 'm_2', 'm_3']
  );
  telemetry.clearM22Events();

  if (originalDescriptor) {
    Object.defineProperty(globalThis, 'localStorage', originalDescriptor);
  }
  console.log('ALL M22 PHASE 0 TELEMETRY & COLD PROBE TESTS PASSED!');
} finally {
  fs.rmSync(tmpDir, { recursive: true, force: true });
}
