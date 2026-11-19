import {
  IronDeferredReviewItem,
  IronExamQuestionDraft,
  MetacognitiveAudit,
  MetacognitiveConfidence,
  MetacognitiveItemAudit,
  Question,
  QuestionType,
} from '../types';
import {
  validateAdversarialSubmission,
  validateConceptMatchingSubmission,
  validateProofDagSubmission,
  validateStage0Phase,
  validateSymbolicAnswer,
} from '../services/symbolicValidator';
import {
  validateCartesianInvariants,
  validateTreeInvariants,
} from '../components/canvas/TopologyValidator';
import { checkMathEquivalence } from './mathEquivalence';
import {
  createInitialStructuredAnswer,
  getCorrectOptionIds,
  isOptionCorrect,
} from './questionUtils';

export interface IronQuestionGradeResult {
  isCorrect: boolean;
  answered: boolean;
  userSummary: string;
  diagnosticRationale?: string;
}

/**
 * Builds an empty answer draft initialized for the given question's modality.
 */
export function createInitialIronDraft(q: Question): IronExamQuestionDraft {
  return {
    selectedOption: null,
    selectedMultiOptions: [],
    fillBlankValue: '',
    structuredAnswer: createInitialStructuredAnswer(q),
    canvasInteracted: false,
  };
}

/**
 * Returns whether the student has provided a complete answer in Iron Exam mode.
 */
export function isDraftAnswered(q: Question, draft: IronExamQuestionDraft): boolean {
  const qType = (q.type || q.interaction_type || 'multiple_choice_7_options') as QuestionType;
  switch (qType) {
    case 'multiple_choice_7_options':
      return draft.selectedOption !== null;
    case 'multiple_select':
      return draft.selectedMultiOptions.length > 0;
    case 'fill_in_the_blank':
      return draft.fillBlankValue.trim().length > 0;
    case 'open_symbolic':
      return (
        draft.structuredAnswer?.kind === 'open_symbolic' &&
        draft.structuredAnswer.expression.trim().length > 0
      );
    case 'proof_dag': {
      if (draft.structuredAnswer?.kind !== 'proof_dag') return false;
      const spec = q.proof_dag;
      if (!spec || draft.structuredAnswer.orderedStepIds.length === 0) return false;
      if (!spec.require_justification) return true;
      return draft.structuredAnswer.orderedStepIds.every((id) =>
        Boolean(draft.structuredAnswer?.kind === 'proof_dag' && draft.structuredAnswer.justifications[id])
      );
    }
    case 'adversarial_break': {
      if (draft.structuredAnswer?.kind !== 'adversarial_break') return false;
      const spec = q.adversarial_break;
      if (!spec) return false;
      if (spec.mode === 'find_fallacy') {
        const hasReason =
          !spec.reason_options ||
          spec.reason_options.length === 0 ||
          Boolean(draft.structuredAnswer.selectedReasonId);
        return Boolean(draft.structuredAnswer.selectedStepId) && hasReason;
      }
      const inputs = spec.inputs || [];
      return (
        inputs.length > 0 &&
        inputs.every((inp) => {
          const iid = inp.id || inp.name || '';
          const val =
            draft.structuredAnswer?.kind === 'adversarial_break'
              ? draft.structuredAnswer.witnessValues[iid]
              : '';
          return Boolean(val && val.trim().length > 0);
        })
      );
    }
    case 'unstructured_model': {
      if (draft.structuredAnswer?.kind !== 'unstructured_model') return false;
      const spec = q.unstructured_model;
      if (!spec) return false;
      const p1Done = spec.phase1_variables.items.every((it) =>
        Boolean(draft.structuredAnswer?.kind === 'unstructured_model' && draft.structuredAnswer.phase1Roles[it.id])
      );
      const p2Done = draft.structuredAnswer.phase2SelectedIds.length > 0;
      const p3Done =
        spec.phase3_formulation.input_mode === 'select'
          ? draft.structuredAnswer.phase3SelectedId !== null
          : draft.structuredAnswer.phase3Expression.trim().length > 0;
      return p1Done && p2Done && p3Done;
    }
    case 'invariant_canvas':
      return draft.structuredAnswer?.kind === 'invariant_canvas' && draft.canvasInteracted;
    case 'concept_matching': {
      if (draft.structuredAnswer?.kind !== 'concept_matching') return false;
      const premises = q.concept_matching?.premises || [];
      return (
        premises.length > 0 &&
        premises.every((pr) =>
          Boolean(draft.structuredAnswer?.kind === 'concept_matching' && draft.structuredAnswer.pairs[pr.id])
        )
      );
    }
    default:
      return false;
  }
}

/**
 * Deterministically grades an Iron Exam draft across all 9 modalities using M20 validators.
 */
export function gradeIronExamQuestion(
  q: Question,
  draft: IronExamQuestionDraft
): IronQuestionGradeResult {
  const answered = isDraftAnswered(q, draft);
  if (!answered) {
    return {
      isCorrect: false,
      answered: false,
      userSummary: 'Sin responder',
      diagnosticRationale: 'Pregunta dejada en blanco o incompleta durante el Modo Hierro.',
    };
  }

  const qType = (q.type || q.interaction_type || 'multiple_choice_7_options') as QuestionType;
  switch (qType) {
    case 'multiple_choice_7_options': {
      const opt = q.options.find((o) => o.id === draft.selectedOption);
      const ok = draft.selectedOption !== null && isOptionCorrect(q, draft.selectedOption);
      return {
        isCorrect: ok,
        answered: true,
        userSummary: opt ? opt.content : String(draft.selectedOption || ''),
        diagnosticRationale: !ok ? opt?.error_rationale ?? undefined : undefined,
      };
    }

    case 'multiple_select': {
      const correctIds = getCorrectOptionIds(q).sort();
      const chosenIds = [...draft.selectedMultiOptions].sort();
      const ok =
        chosenIds.length === correctIds.length &&
        chosenIds.every((val, idx) => val === correctIds[idx]);
      const chosenContents = q.options
        .filter((o) => draft.selectedMultiOptions.includes(o.id))
        .map((o) => o.content);
      const rationales = q.options
        .filter((o) => draft.selectedMultiOptions.includes(o.id) && !isOptionCorrect(q, o.id))
        .map((o) => o.error_rationale)
        .filter(Boolean);
      return {
        isCorrect: ok,
        answered: true,
        userSummary: chosenContents.join(' | ') || 'Selección múltiple',
        diagnosticRationale: !ok ? rationales[0] ?? undefined : undefined,
      };
    }

    case 'fill_in_the_blank': {
      const ok = checkMathEquivalence(draft.fillBlankValue, q.correct_answer as any);
      let diagRationale: string | undefined;
      if (!ok && q.diagnostic_distractors?.length) {
        const res = validateSymbolicAnswer(
          draft.fillBlankValue,
          q.correct_answer,
          q.diagnostic_distractors,
          q.symbolic_config
        );
        diagRationale = res.diagnosticRationale || res.syntaxError;
      }
      return {
        isCorrect: ok,
        answered: true,
        userSummary: draft.fillBlankValue,
        diagnosticRationale: diagRationale,
      };
    }

    case 'open_symbolic': {
      const expr =
        draft.structuredAnswer?.kind === 'open_symbolic'
          ? draft.structuredAnswer.expression
          : '';
      const res = validateSymbolicAnswer(
        expr,
        q.correct_answer,
        q.diagnostic_distractors,
        q.symbolic_config
      );
      return {
        isCorrect: res.isCorrect,
        answered: true,
        userSummary: expr,
        diagnosticRationale: !res.isCorrect ? res.diagnosticRationale || res.syntaxError : undefined,
      };
    }

    case 'proof_dag': {
      const sVal =
        draft.structuredAnswer?.kind === 'proof_dag'
          ? draft.structuredAnswer
          : { orderedStepIds: [], justifications: {} };
      if (!q.proof_dag) {
        return { isCorrect: false, answered: true, userSummary: 'Sin especificación DAG' };
      }
      const res = validateProofDagSubmission(
        sVal.orderedStepIds,
        sVal.justifications,
        q.proof_dag
      );
      return {
        isCorrect: res.isCorrect,
        answered: true,
        userSummary: `Secuencia: ${sVal.orderedStepIds.join(' → ')}`,
        diagnosticRationale: !res.isCorrect ? res.diagnosticRationale : undefined,
      };
    }

    case 'adversarial_break': {
      const aVal =
        draft.structuredAnswer?.kind === 'adversarial_break'
          ? draft.structuredAnswer
          : { selectedStepId: null, selectedReasonId: null, witnessValues: {} };
      if (!q.adversarial_break) {
        return { isCorrect: false, answered: true, userSummary: 'Sin especificación adversarial' };
      }
      const res = validateAdversarialSubmission(aVal, q.adversarial_break);
      const summary =
        q.adversarial_break.mode === 'find_fallacy'
          ? `Paso ${aVal.selectedStepId || '—'}${aVal.selectedReasonId ? ` (${aVal.selectedReasonId})` : ''}`
          : JSON.stringify(aVal.witnessValues);
      return {
        isCorrect: res.isCorrect,
        answered: true,
        userSummary: summary,
        diagnosticRationale: !res.isCorrect ? res.diagnosticRationale : undefined,
      };
    }

    case 'unstructured_model': {
      const uVal =
        draft.structuredAnswer?.kind === 'unstructured_model'
          ? draft.structuredAnswer
          : {
              phase1Roles: {},
              phase2SelectedIds: [],
              phase3SelectedId: null,
              phase3Expression: '',
            };
      if (!q.unstructured_model) {
        return { isCorrect: false, answered: true, userSummary: 'Sin especificación Stage 0' };
      }
      const p1 = validateStage0Phase(1, uVal, q.unstructured_model);
      const p2 = validateStage0Phase(2, uVal, q.unstructured_model);
      const p3 = validateStage0Phase(3, uVal, q.unstructured_model);
      const ok = p1.isCorrect && p2.isCorrect && p3.isCorrect;
      const firstError =
        (!p1.isCorrect && p1.diagnosticRationale) ||
        (!p2.isCorrect && p2.diagnosticRationale) ||
        (!p3.isCorrect && p3.diagnosticRationale) ||
        undefined;
      const p3Summary =
        q.unstructured_model.phase3_formulation.input_mode === 'select'
          ? q.unstructured_model.phase3_formulation.options?.find(
              (o) => o.id === uVal.phase3SelectedId
            )?.content ||
            uVal.phase3SelectedId ||
            '—'
          : uVal.phase3Expression || '—';
      return {
        isCorrect: ok,
        answered: true,
        userSummary: `F1: ${Object.keys(uVal.phase1Roles).length} vars • F2: ${uVal.phase2SelectedIds.length} sup. • F3: ${p3Summary}`,
        diagnosticRationale: firstError,
      };
    }

    case 'invariant_canvas': {
      const cVal =
        draft.structuredAnswer?.kind === 'invariant_canvas'
          ? draft.structuredAnswer
          : {
              sliderValues: {},
              pointPositions: {},
              selectedEdgeIds: [],
              infoSets: [],
              inequalityStyle: q.invariant_canvas?.inequality?.initial_style ?? 'solid',
              inequalityShade: q.invariant_canvas?.inequality?.initial_shade ?? 'above',
            };
      if (!q.invariant_canvas) {
        return { isCorrect: false, answered: true, userSummary: 'Sin especificación canvas' };
      }
      const res =
        q.invariant_canvas.mode === 'tree'
          ? validateTreeInvariants(
              { selectedEdgeIds: cVal.selectedEdgeIds, infoSets: cVal.infoSets },
              q.invariant_canvas
            )
          : validateCartesianInvariants(
              {
                sliderValues: cVal.sliderValues,
                pointPositions: cVal.pointPositions,
                inequalityStyle: cVal.inequalityStyle,
                inequalityShade: cVal.inequalityShade,
              },
              q.invariant_canvas
            );
      const summary =
        q.invariant_canvas.mode === 'tree'
          ? `Ramas: [${cVal.selectedEdgeIds.join(', ')}], InfoSets: ${cVal.infoSets.length}`
          : `Sliders: ${JSON.stringify(cVal.sliderValues)}, Puntos: ${JSON.stringify(cVal.pointPositions)}`;
      return {
        isCorrect: res.isCorrect,
        answered: true,
        userSummary: summary,
        diagnosticRationale: !res.isCorrect ? res.diagnosticRationale : undefined,
      };
    }

    case 'concept_matching': {
      const pVal =
        draft.structuredAnswer?.kind === 'concept_matching' ? draft.structuredAnswer.pairs : {};
      if (!q.concept_matching) {
        return { isCorrect: false, answered: true, userSummary: 'Sin especificación matching' };
      }
      const res = validateConceptMatchingSubmission(pVal, q.concept_matching);
      return {
        isCorrect: res.isCorrect,
        answered: true,
        userSummary: `${Object.keys(pVal).length} emparejamientos`,
        diagnosticRationale: !res.isCorrect ? res.diagnosticRationale : undefined,
      };
    }

    default:
      return { isCorrect: false, answered: true, userSummary: 'Modalidad desconocida' };
  }
}

/**
 * Classifies an item's confidence vs correctness into the 4 metacognitive quadrants.
 */
function classifyQuadrant(
  confidence: MetacognitiveConfidence,
  isCorrect: boolean
): MetacognitiveItemAudit['quadrant'] {
  if (confidence === 'high') {
    return isCorrect ? 'calibrated_mastery' : 'illusion_of_competence';
  }
  if (confidence === 'medium') {
    return isCorrect ? 'calibrated_mastery' : 'known_gap';
  }
  return isCorrect ? 'lucky_guess' : 'known_gap';
}

/**
 * Computes the complete deferred Metacognitive Audit and per-item review records.
 */
export function computeMetacognitiveAudit(
  questions: Question[],
  drafts: Record<string, IronExamQuestionDraft>,
  itemConfidences: Record<string, MetacognitiveConfidence>,
  globalConfidence: MetacognitiveConfidence,
  flaggedIds: Record<string, boolean> = {}
): {
  audit: MetacognitiveAudit;
  deferredReview: IronDeferredReviewItem[];
  gradedResults: Record<string, IronQuestionGradeResult>;
} {
  let answeredCount = 0;
  let correctCount = 0;
  let calibratedMasteryCount = 0;
  let illusionsCount = 0;
  let luckyGuessesCount = 0;
  let knownGapsCount = 0;

  const items: MetacognitiveItemAudit[] = [];
  const deferredReview: IronDeferredReviewItem[] = [];
  const gradedResults: Record<string, IronQuestionGradeResult> = {};

  for (const q of questions) {
    const draft = drafts[q.id] || createInitialIronDraft(q);
    const graded = gradeIronExamQuestion(q, draft);
    gradedResults[q.id] = graded;

    const conf = itemConfidences[q.id] || globalConfidence;
    const quadrant = classifyQuadrant(conf, graded.isCorrect);

    if (graded.answered) answeredCount += 1;
    if (graded.isCorrect) correctCount += 1;

    if (quadrant === 'calibrated_mastery') calibratedMasteryCount += 1;
    else if (quadrant === 'illusion_of_competence') illusionsCount += 1;
    else if (quadrant === 'lucky_guess') luckyGuessesCount += 1;
    else knownGapsCount += 1;

    items.push({
      question_id: q.id,
      competency_id: q.competency_id,
      type: (q.type || q.interaction_type || 'multiple_choice_7_options') as QuestionType,
      confidence: conf,
      is_correct: graded.isCorrect,
      answered: graded.answered,
      quadrant,
      diagnostic_rationale: graded.diagnosticRationale,
    });

    deferredReview.push({
      question: q,
      is_correct: graded.isCorrect,
      answered: graded.answered,
      confidence: conf,
      flagged: Boolean(flaggedIds[q.id]),
      user_summary: graded.userSummary,
      diagnostic_rationale: graded.diagnosticRationale,
    });
  }

  const total = questions.length;
  const calibrationScore =
    total === 0
      ? 100
      : Math.round(
          ((calibratedMasteryCount * 1 + knownGapsCount * 0.8 + luckyGuessesCount * 0.5) / total) *
            100
        );

  return {
    audit: {
      global_confidence: globalConfidence,
      total_questions: total,
      answered_count: answeredCount,
      correct_count: correctCount,
      calibrated_mastery_count: calibratedMasteryCount,
      illusions_of_competence_count: illusionsCount,
      lucky_guesses_count: luckyGuessesCount,
      known_gaps_count: knownGapsCount,
      calibration_score: calibrationScore,
      items,
    },
    deferredReview,
    gradedResults,
  };
}
