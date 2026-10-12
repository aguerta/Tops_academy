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
  misconception_warning?: string;
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
}

export type MasteryTier =
  | 'Not started'
  | 'Attempted'
  | 'Familiar'
  | 'Proficient'
  | 'Mastered';

export interface CompetencyMastery {
  status: MasteryTier;
  points: number;
  last_practiced: string;
  history: Array<{
    date: string;
    score: number;
    total: number;
    type: 'practice' | 'quiz' | 'test' | 'challenge';
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
    completed_at: string;
  };
}
