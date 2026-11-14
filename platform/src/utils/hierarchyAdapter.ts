import {
  Competency,
  ContentCore,
  ContentGlossaryTerm,
  ContentModule,
  Course,
  EvidenceRef,
  ExplicitAssumption,
  Question,
  SubtopicUnit,
} from '../types';

function isPrerequisiteCompetency(c: Competency): boolean {
  return c.is_prerequisite === true || c.id.startsWith('PRE-');
}

function normalizeDocName(raw: string): string {
  const parts = raw.split(/[\\/]/);
  return parts[parts.length - 1]?.trim() || raw.trim();
}

function resolveGroupKey(c: Competency): { key: string; title: string; sourceFile: string } {
  const firstEvidence = c.evidence?.[0];
  const rawDoc = firstEvidence?.doc || firstEvidence?.pdf;
  if (rawDoc && rawDoc.trim().length > 0) {
    const cleanDoc = normalizeDocName(rawDoc);
    return { key: `doc:${cleanDoc}`, title: cleanDoc, sourceFile: cleanDoc };
  }

  if (c.session && c.session.trim().length > 0) {
    const prefix = c.session.split(/[:\-–—]/)[0].trim() || c.session.trim();
    return { key: `session:${prefix}`, title: prefix, sourceFile: c.session.trim() };
  }

  return { key: 'general', title: 'Contenido del Curso', sourceFile: 'Curso' };
}

function extractNumericPages(evidenceList?: EvidenceRef[]): number[] {
  if (!evidenceList || evidenceList.length === 0) return [];
  const pages: number[] = [];
  for (const ev of evidenceList) {
    if (typeof ev.page === 'number' && Number.isFinite(ev.page)) pages.push(ev.page);
    if (typeof ev.slide === 'number' && Number.isFinite(ev.slide)) pages.push(ev.slide);
    if (Array.isArray(ev.pages)) {
      for (const p of ev.pages) {
        if (typeof p === 'number' && Number.isFinite(p)) pages.push(p);
      }
    }
  }
  return pages;
}

function computeSlideRange(competencies: Competency[]): [number, number] | undefined {
  const allPages = competencies.flatMap((c) => extractNumericPages(c.evidence));
  if (allPages.length === 0) return undefined;
  return [Math.min(...allPages), Math.max(...allPages)];
}

function synthesizeGlossary(competencies: Competency[]): ContentGlossaryTerm[] {
  return competencies
    .filter((c) => c.category === 'Fact' || c.category === 'Concept')
    .map((c) => ({
      term: c.name,
      definition: c.description,
      related_competencies: [c.id],
    }));
}

function collectAssumptions(competencies: Competency[]): ExplicitAssumption[] {
  const seen = new Set<string>();
  const result: ExplicitAssumption[] = [];
  let idx = 1;
  for (const c of competencies) {
    if (!c.assumptions) continue;
    for (const a of c.assumptions) {
      const key = a.statement_latex.trim();
      if (!key || seen.has(key)) continue;
      seen.add(key);
      result.push({
        id: a.id || `A-${c.id}-${idx++}`,
        name: a.name,
        statement_latex: a.statement_latex,
        role_in_proof: a.role_in_proof,
        violation_consequence: a.violation_consequence,
      });
    }
  }
  return result;
}

function collectPitfalls(questions: Question[]): string[] {
  const seen = new Set<string>();
  const pitfalls: string[] = [];

  const pushUnique = (raw?: string | null) => {
    if (!raw) return;
    const trimmed = raw.trim();
    if (!trimmed || seen.has(trimmed)) return;
    seen.add(trimmed);
    pitfalls.push(trimmed);
  };

  for (const q of questions) {
    if (pitfalls.length >= 5) break;
    pushUnique(q.misconception_warning);
    if (pitfalls.length >= 5) break;
    pushUnique(q.common_misconception_warning);
    if (pitfalls.length >= 5) break;
    for (const opt of q.options || []) {
      pushUnique(opt.error_rationale);
      if (pitfalls.length >= 5) break;
    }
  }

  return pitfalls.slice(0, 5);
}

function synthesizeContentCore(
  moduleTitle: string,
  competencies: Competency[],
  moduleQuestions: Question[],
  allCompetencies: Competency[],
  isPrerequisiteModule: boolean
): ContentCore {
  const compById = new Map(allCompetencies.map((c) => [c.id, c]));

  const prereqItems: string[] = [];
  if (isPrerequisiteModule) {
    for (const c of competencies) {
      prereqItems.push(c.name);
    }
  } else {
    const seenPrereq = new Set<string>();
    for (const c of competencies) {
      for (const preId of c.prerequisites || []) {
        const label = compById.get(preId)?.name || preId;
        if (!seenPrereq.has(label)) {
          seenPrereq.add(label);
          prereqItems.push(label);
        }
      }
    }
  }

  const prerequisiteRecall =
    prereqItems.length > 0
      ? prereqItems.join(' • ')
      : '';

  const intuitiveAnalogy = competencies
    .slice(0, 2)
    .map((c) => c.description)
    .filter(Boolean)
    .join(' ');

  const assumptions = collectAssumptions(competencies);
  const firstQ = moduleQuestions[0];
  const solutionText = firstQ ? (firstQ.detailed_solution || firstQ.solution || '').trim() : '';

  return {
    title: moduleTitle,
    prerequisite_recall: prerequisiteRecall,
    intuitive_analogy: intuitiveAnalogy,
    governing_theorems_and_assumptions: {
      theorems_latex: [],
      assumptions,
    },
    worked_example: {
      problem_latex: firstQ ? firstQ.stem : '',
      step_by_step_latex: solutionText ? [solutionText] : [],
    },
    common_exam_pitfalls: collectPitfalls(moduleQuestions),
  };
}

function buildModule(
  id: string,
  title: string,
  sourceFile: string,
  competencies: Competency[],
  courseQuestions: Question[],
  allCompetencies: Competency[],
  isPrerequisiteModule: boolean
): ContentModule {
  const compIds = new Set(competencies.map((c) => c.id));
  const moduleQuestions = courseQuestions.filter((q) => compIds.has(q.competency_id));
  const questionIds = moduleQuestions.map((q) => q.id);

  const subtopics: SubtopicUnit[] = [
    {
      id: `${id}_subtopic_01`,
      title,
      description: '',
      competency_ids: competencies.map((c) => c.id),
      quiz_question_pool: questionIds,
    },
  ];

  return {
    id,
    is_prerequisite_module: isPrerequisiteModule,
    title,
    source_file: sourceFile,
    slide_range: computeSlideRange(competencies),
    glossary: synthesizeGlossary(competencies),
    core: synthesizeContentCore(
      title,
      competencies,
      moduleQuestions,
      allCompetencies,
      isPrerequisiteModule
    ),
    subtopics,
    content_challenge_pool: questionIds,
  };
}

/**
 * Resolves hierarchical ContentModules for a course.
 * Returns `course.modules` if explicitly provided and non-empty; otherwise
 * groups competencies backwards-compatibly into Unit 0 (Get Ready) + document/session modules
 * with fast-path ContentCore and glossary synthesis.
 */
export function resolveCourseModules(course: Course): ContentModule[] {
  if (course.modules && course.modules.length > 0) {
    return course.modules;
  }

  const allCompetencies = course.competencies || [];
  if (allCompetencies.length === 0) return [];

  const questions = course.questions || [];
  const modules: ContentModule[] = [];

  const preUnits = allCompetencies.filter(isPrerequisiteCompetency);
  const regularUnits = allCompetencies.filter((c) => !isPrerequisiteCompetency(c));

  if (preUnits.length > 0) {
    const firstPreDoc = preUnits[0]?.evidence?.[0]?.doc || preUnits[0]?.evidence?.[0]?.pdf;
    modules.push(
      buildModule(
        'module_00_get_ready',
        'Unidad 0: Get Ready (Prerrequisitos)',
        firstPreDoc ? normalizeDocName(firstPreDoc) : 'Prerrequisitos',
        preUnits,
        questions,
        allCompetencies,
        true
      )
    );
  }

  const groups = new Map<
    string,
    { title: string; sourceFile: string; competencies: Competency[] }
  >();

  for (const c of regularUnits) {
    const { key, title, sourceFile } = resolveGroupKey(c);
    const existing = groups.get(key);
    if (existing) {
      existing.competencies.push(c);
    } else {
      groups.set(key, { title, sourceFile, competencies: [c] });
    }
  }

  let modIdx = 1;
  for (const [, group] of groups) {
    const id = `module_${String(modIdx).padStart(2, '0')}`;
    modules.push(
      buildModule(
        id,
        group.title,
        group.sourceFile,
        group.competencies,
        questions,
        allCompetencies,
        false
      )
    );
    modIdx++;
  }

  return modules;
}
