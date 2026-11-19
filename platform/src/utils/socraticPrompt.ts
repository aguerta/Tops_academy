import { Question, StructuredUserAnswer } from '../types';

export interface SocraticPromptContext {
  courseTitle: string;
  question: Question;
  selectedOptionContent?: string;
  structuredAnswer?: StructuredUserAnswer | null;
  errorRationale?: string;
  hintsRevealed: number;
}

function summarizeStructuredAnswer(ans: StructuredUserAnswer | null | undefined): string {
  if (!ans) return '';
  switch (ans.kind) {
    case 'open_symbolic':
      return ans.expression ? `Expresión simbólica: ${ans.expression}` : '';
    case 'proof_dag':
      return ans.orderedStepIds.length > 0
        ? `Secuencia propuesta de pasos: ${ans.orderedStepIds.join(' -> ')}`
        : '';
    case 'adversarial_break':
      if (ans.selectedStepId) return `Paso falaz seleccionado: ${ans.selectedStepId}`;
      if (Object.keys(ans.witnessValues).length > 0) {
        return `Testigo propuesto: ${JSON.stringify(ans.witnessValues)}`;
      }
      return '';
    case 'unstructured_model':
      return `Modelado Stage 0: Fase 1=${JSON.stringify(ans.phase1Roles)}, Fase 2=${ans.phase2SelectedIds.join(', ')}, Fase 3=${ans.phase3SelectedId || ans.phase3Expression}`;
    case 'invariant_canvas':
      return `Estado Canvas: sliders=${JSON.stringify(ans.sliderValues)}, puntos=${JSON.stringify(ans.pointPositions)}, aristas=${ans.selectedEdgeIds.join(',')}`;
    case 'concept_matching':
      return `Emparejamientos propuestos: ${JSON.stringify(ans.pairs)}`;
  }
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

  const rawSelected = ctx.selectedOptionContent || summarizeStructuredAnswer(ctx.structuredAnswer);
  const selectedOptText = rawSelected
    ? `\nMI RESPUESTA INCORRECTA SELECCIONADA:\n"${rawSelected}"\n`
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
