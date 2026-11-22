import { Question } from '../types';
import { isOptionCorrect } from './questionUtils';

/**
 * Extracts all unique real diagnostic distractor IDs (D-XX-YY) carried by a question
 * across all 9 modalities, used for Misconception Ledger immunity tracking and
 * Misconception Drill session selection.
 */
export function extractCarriedDistractorIds(q: Question): string[] {
  const ids = new Set<string>();
  const addId = (raw?: string | null) => {
    if (typeof raw === 'string') {
      const trimmed = raw.trim();
      if (trimmed) ids.add(trimmed);
    }
  };

  for (const opt of q.options || []) {
    if (!opt.is_correct) {
      addId(opt.distractor_id);
    }
  }

  for (const dd of q.diagnostic_distractors || []) {
    addId(dd.distractor_id);
  }

  if (q.proof_dag) {
    for (const step of q.proof_dag.steps || []) {
      if (step.is_fallacy) addId(step.distractor_id);
    }
  }

  if (q.adversarial_break) {
    for (const step of q.adversarial_break.steps || []) {
      addId(step.distractor_id);
    }
    for (const ro of q.adversarial_break.reason_options || []) {
      if (!ro.is_correct) addId(ro.distractor_id);
    }
    for (const p of q.adversarial_break.predicates || []) {
      addId(p.distractor_id);
    }
    for (const tp of q.adversarial_break.trap_predicates || []) {
      addId(tp.distractor_id);
    }
  }

  if (q.unstructured_model) {
    for (const item of q.unstructured_model.phase1_variables?.items || []) {
      addId(item.distractor_id);
    }
    for (const opt of q.unstructured_model.phase2_assumptions?.options || []) {
      addId(opt.distractor_id);
    }
    for (const opt of q.unstructured_model.phase3_formulation?.options || []) {
      if (!opt.is_correct) addId(opt.distractor_id);
    }
    for (const dd of q.unstructured_model.phase3_formulation?.diagnostic_distractors || []) {
      addId(dd.distractor_id);
    }
  }

  if (q.invariant_canvas) {
    for (const inv of q.invariant_canvas.invariants || []) {
      addId(inv.distractor_id);
    }
    if (q.invariant_canvas.tree_invariants) {
      addId(q.invariant_canvas.tree_invariants.distractor_id);
    }
  }

  if (q.concept_matching) {
    for (const p of q.concept_matching.premises || []) {
      addId(p.distractor_id);
    }
    for (const t of q.concept_matching.targets || []) {
      addId(t.distractor_id);
    }
  }

  return Array.from(ids);
}

/**
 * Extracts real distractor IDs and diagnostic rationales from incorrect selections
 * in multiple_choice_7_options and multiple_select items.
 */
export function extractOptionDistractors(
  q: Question,
  selectedOptionIds: string[]
): { ids: string[]; rationales: Record<string, string> } {
  const ids: string[] = [];
  const rationales: Record<string, string> = {};
  const seen = new Set<string>();

  for (const chosenId of selectedOptionIds) {
    const opt = (q.options || []).find((o) => o.id === chosenId);
    if (!opt || isOptionCorrect(q, opt.id)) continue;
    const did = typeof opt.distractor_id === 'string' ? opt.distractor_id.trim() : '';
    if (!did) continue;
    if (!seen.has(did)) {
      seen.add(did);
      ids.push(did);
    }
    if (opt.error_rationale && opt.error_rationale.trim()) {
      rationales[did] = opt.error_rationale.trim();
    }
  }

  return { ids, rationales };
}
