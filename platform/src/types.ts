export type QuestionType =
  | 'multiple_choice_7_options'
  | 'multiple_select'
  | 'fill_in_the_blank';

export type CompetencyCategory = 'Skill' | 'Concept' | 'Fact';

export interface Competency {
  id: string;
  code: string;
  name: string;
  category: CompetencyCategory;
  description: string;
  mastery_target: number;
  prerequisites?: string[];
}

export interface CurveSpec {
  id?: string;
  label?: string;
  label_pos?: [number, number];
  color?: string;
  expression?: string;
  fn?: string;
  domain?: [number, number];
}

export interface PointSpec {
  x: number;
  y: number;
  type: 'open' | 'closed';
  label?: string;
  color?: string;
}

export interface GraphSpec {
  type?: string;
  x_range: [number, number];
  y_range: [number, number];
  step?: number;
  width?: number;
  height?: number;
  curves?: CurveSpec[];
  points?: PointSpec[];
}

export interface QuestionOption {
  id: string;
  option_id?: string;
  content: string;
  is_correct?: boolean;
  distractor_id?: string;
  error_rationale?: string | null;
}

export interface FillBlankAnswer {
  expression?: string;
  canonical_algebraic?: string;
  value?: string | number;
  accepted_equivalents?: string[];
  tolerance?: number;
  min_decimals?: number;
}

export type CorrectAnswer = string | number | string[] | FillBlankAnswer;

export interface Question {
  id: string;
  competency_id: string;
  type: QuestionType;
  difficulty?: 'easy' | 'medium' | 'hard';
  stem: string;
  graph?: GraphSpec;
  options: QuestionOption[];
  correct_answer: CorrectAnswer;
  hints: string[];
  solution: string;
  detailed_solution?: string;
  misconception_warning?: string;
  common_misconception_warning?: string;
}

export interface Course {
  course_id: string;
  title: string;
  description: string;
  version: string;
  language?: string;
  competencies: Competency[];
  questions: Question[];
}

export interface CourseSummary {
  id: string;
  filename: string;
  title: string;
  description: string;
  status: 'valid' | 'error';
  error_message?: string;
  total_competencies?: number;
  total_questions?: number;
  data?: Course;
  bytes?: number;
  etag?: string;
}

export interface CourseManifest {
  generated_at: string;
  courses: CourseSummary[];
}

export type MasteryTier =
  | 'Not started'
  | 'Attempted'
  | 'Familiar'
  | 'Proficient'
  | 'Mastered';

export interface UnitTestRecord {
  last_score: number;
  total_questions: number;
  percentage: number;
  completed_at: string;
}

export interface TimingStats {
  best_avg_seconds_per_question?: number;
  best_total_seconds?: number;
  last_avg_seconds_per_question?: number;
  last_total_seconds?: number;
}

export interface QuestionTelemetry {
  question_id: string;
  competency_id: string;
  is_correct: boolean;
  hints_used: number;
  seconds_spent: number;
  question_text?: string;
}

export interface ChallengeSkillResult {
  competency_id: string;
  competency_name: string;
  total_questions: number;
  correct_questions: number;
  previous_tier: MasteryTier;
  new_tier: MasteryTier;
  direction: 'up' | 'down' | 'maintained';
  delta_points: number;
}

export interface ChallengeExecutionSummary {
  record: CourseMasteryRecord;
  overall_score: number;
  overall_total: number;
  overall_percentage: number;
  total_seconds: number;
  avg_seconds_per_question: number;
  is_new_record: boolean;
  skills_leveled_up: ChallengeSkillResult[];
  skills_leveled_down: ChallengeSkillResult[];
  skills_maintained: ChallengeSkillResult[];
  misconceptions: Array<{
    question_id: string;
    competency_id: string;
    competency_name: string;
    text: string;
  }>;
}

export interface CompetencyMastery {
  status: MasteryTier;
  points: number;
  last_practiced: string;
  unit_test?: UnitTestRecord;
  history: Array<{
    date: string;
    score: number;
    total: number;
    type: 'practice' | 'quiz' | 'test' | 'challenge';
    total_seconds?: number;
    avg_seconds_per_question?: number;
    previous_tier?: MasteryTier;
    new_tier?: MasteryTier;
  }>;
  timing?: {
    practice?: TimingStats;
    quiz?: TimingStats;
    test?: TimingStats;
  };
  needs_review?: boolean;
  recent_misconceptions?: Array<{
    date: string;
    question_id: string;
    concept_name: string;
  }>;
}

export interface CourseMasteryRecord {
  course_id: string;
  mastery_points: number;
  competencies: Record<string, CompetencyMastery>;
  course_challenge?: {
    completed: boolean;
    last_score: number;
    total_questions: number;
    percentage?: number;
    completed_at: string;
    timing?: TimingStats;
  };
}

export type CourseProgressStatus =
  | 'completed'             // 100%: All Unit Tests 100% + Course Challenge 100% (Verde Fuerte)
  | 'unit_tests_mastered'  // 80%: All Unit Tests 100%, Course Challenge < 100% (Verde Light)
  | 'in_progress'          // 1 - 79%: En progreso (Amarillo)
  | 'not_started';         // 0%: Sin iniciar (Neutro)

export interface CourseProgressDetails {
  percentage: number;
  status: CourseProgressStatus;
  completedUnits: number;
  inProgressUnits: number;
  notStartedUnits: number;
  totalUnits: number;
}
