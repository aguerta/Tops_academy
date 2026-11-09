import { Question } from '../types';

export interface SocraticPromptContext {
  courseTitle: string;
  question: Question;
  selectedOptionContent?: string;
  errorRationale?: string;
  hintsRevealed: number;
}

/**
 * Builds an academically rigorous, anti-giveaway socratic prompt to be pasted
 * into an external LLM (Gemini Pro, Claude, ChatGPT) at $0 API cost.
 */
export function buildSocraticPrompt(ctx: SocraticPromptContext): string {
  const hintsList =
    ctx.question.hints && ctx.hintsRevealed > 0
      ? ctx.question.hints
          .slice(0, ctx.hintsRevealed)
          .map((h, i) => `   ${i + 1}. ${h}`)
          .join('\n')
      : '   (Ninguna pista previa consultada)';

  const selectedOptText = ctx.selectedOptionContent
    ? `\nMI RESPUESTA INCORRECTA SELECCIONADA:\n"${ctx.selectedOptionContent}"\n`
    : '';

  const rationaleText = ctx.errorRationale
    ? `\nDIAGNÓSTICO DEL SISTEMA SOBRE EL ERROR:\n${ctx.errorRationale}\n`
    : '';

  return `Actúa como un profesor universitario socrático riguroso en el curso de "${ctx.courseTitle}".
Estoy resolviendo un ejercicio académico y me encuentro atascado tras agotar mis intentos de resolución autónoma.

ENUNCIADO DEL PROBLEMA:
${ctx.question.stem}
${selectedOptText}${rationaleText}
PISTAS PREVIAS DEL SISTEMA:
${hintsList}

REGLAS ESTRICTAS DE TUTORÍA SOCRÁTICA (ANTI-GIVEAWAY):
1. PROHIBIDO revelar la respuesta correcta o indicar qué opción o letra marcar.
2. PROHIBIDO resolver el ejercicio o desarrollar la demostración paso a paso.
3. Formula EXACTAMENTE UNA SOLA pregunta reflexiva sobre el primer principio, teorema central o condición de regularidad que me permita deducir de forma autónoma dónde estuvo el fallo en mi razonamiento.`;
}
