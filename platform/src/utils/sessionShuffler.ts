import { Question, QuestionOption } from '../types';
import { normalizeQuestion } from './questionUtils';

/**
 * Standard Fisher-Yates array shuffling algorithm.
 */
export function shuffleArray<T>(items: T[]): T[] {
  const result = [...items];
  for (let i = result.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [result[i], result[j]] = [result[j], result[i]];
  }
  return result;
}

/**
 * Prepares a practice session from a list of questions:
 * 1. Normalizes option IDs, correctness indicators, and answer keys.
 * 2. Shuffles options for all multiple-choice and multiple-select items.
 * 3. Optionally shuffles question order (for quizzes, tests, challenges).
 */
export function prepareSessionQuestions(
  questions: Question[],
  shuffleQuestions: boolean = false,
  expectedCompetencyId?: string
): Question[] {
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
    const q = normalizeQuestion(rawQ);
    if (q.options && q.options.length > 0) {
      return {
        ...q,
        options: shuffleArray<QuestionOption>(q.options),
      };
    }
    return q;
  });
}
