export type QuestionType =
  | 'multiple_choice_7_options'
  | 'multiple_select'
  | 'fill_in_the_blank'
  | 'open_symbolic'
  | 'proof_dag'
  | 'adversarial_break'
  | 'unstructured_model'
  | 'invariant_canvas'
  | 'concept_matching';

export type CompetencyCategory = 'Skill' | 'Concept' | 'Fact';

export interface EvidenceRef {
  doc?: string;
  pdf?: string;
  page?: number;
  pages?: number[];
  slide?: number;
  title?: string;
  snippet?: string;
}

export interface ExplicitAssumption {
  id: string;
  name?: string;
  statement_latex: string;
  role_in_proof?: string;
  violation_consequence: string;
}

export interface ContentGlossaryTerm {
  term: string;
  definition: string;
  formula_latex?: string;
  related_competencies?: string[];
}

export interface ContentCore {
  title: string;
  prerequisite_recall: string;
  intuitive_analogy: string;
  governing_theorems_and_assumptions: {
    theorems_latex: string[];
    assumptions: ExplicitAssumption[];
  };
  worked_example: {
    problem_latex: string;
    step_by_step_latex: string[];
  };
  common_exam_pitfalls: string[];
}

export interface SubtopicUnit {
  id: string;
  title: string;
  description: string;
  competency_ids: string[];
  quiz_question_pool?: string[];
}

export interface ContentModule {
  id: string;
  is_prerequisite_module?: boolean;
  title: string;
  source_file: string;
  slide_range?: [number, number];
  glossary: ContentGlossaryTerm[];
  core: ContentCore;
  subtopics: SubtopicUnit[];
  content_challenge_pool: string[];
}

export interface Competency {
  id: string;
  code: string;
  name: string;
  category: CompetencyCategory;
  description: string;
  mastery_target: number;
  prerequisites?: string[];
  is_prerequisite?: boolean;
  session?: string;
  unit_index?: number;
  evidence?: EvidenceRef[];
  assumptions?: ExplicitAssumption[];
  source_examples?: unknown[];
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

export interface DiagnosticDistractor {
  distractor_id?: string;
  expression?: string;
  value?: string | number;
  accepted_equivalents?: string[];
  tolerance?: number;
  match_type?: 'symbolic' | 'numeric' | 'exact' | 'regex';
  error_rationale: string;
}

export interface SymbolicConfig {
  variables?: string[];
  palette?: string[];
  placeholder?: string;
}

export interface ProofStep {
  id: string;
  content: string;
  is_fallacy: boolean;
  justification?: string;
  distractor_id?: string;
  error_rationale?: string;
}

export interface ProofDagSpec {
  goal?: string;
  steps: ProofStep[];
  edges: [string, string][];
  require_justification: boolean;
  justification_bank?: string[];
}

export interface AdversarialStep {
  id: string;
  label?: string;
  content: string;
  is_fallacy: boolean;
  distractor_id?: string;
  error_rationale?: string;
  valid_explanation?: string;
}

export interface AdversarialReasonOption {
  id: string;
  content: string;
  is_correct: boolean;
  distractor_id?: string;
  error_rationale?: string;
}

export interface AdversarialInputField {
  id: string;
  name?: string;
  label: string;
  placeholder?: string;
  type?: 'integer' | 'number';
  min?: number;
  max?: number;
  step?: number;
}

export interface AdversarialPredicate {
  id?: string;
  expr: string;
  failure_rationale?: string;
  error_rationale?: string;
  distractor_id?: string;
}

export interface AdversarialReadoutSpec {
  id?: string;
  label: string;
  expr: string;
  unit?: string;
}

export interface AdversarialBreakSpec {
  mode: 'find_fallacy' | 'counterexample';
  prompt?: string;
  steps?: AdversarialStep[];
  reason_options?: AdversarialReasonOption[];
  inputs?: AdversarialInputField[];
  predicates?: AdversarialPredicate[];
  trap_predicates?: AdversarialPredicate[];
  computed_readouts?: AdversarialReadoutSpec[];
  sample_witness?: Record<string, number>;
}

export interface Stage0VariableItem {
  id: string;
  label: string;
  correct_role: string;
  error_rationale?: string;
  distractor_id?: string;
}

export interface Stage0AssumptionOption {
  id: string;
  content: string;
  is_required: boolean;
  error_rationale?: string;
  distractor_id?: string;
}

export interface Stage0FormulationOption {
  id: string;
  content: string;
  is_correct: boolean;
  error_rationale?: string;
  distractor_id?: string;
}

export interface UnstructuredModelSpec {
  phase1_variables: {
    prompt: string;
    roles: string[];
    items: Stage0VariableItem[];
  };
  phase2_assumptions: {
    prompt: string;
    options: Stage0AssumptionOption[];
  };
  phase3_formulation: {
    prompt: string;
    input_mode: 'select' | 'symbolic';
    options?: Stage0FormulationOption[];
    correct_expression?: FillBlankAnswer;
    diagnostic_distractors?: DiagnosticDistractor[];
  };
}

export interface CanvasSlider {
  id: string;
  label?: string;
  min: number;
  max: number;
  step?: number;
  initial?: number;
  unit?: string;
}

export interface CanvasCurve {
  id?: string;
  label?: string;
  color?: string;
  expression?: string;
  fn?: string;
  domain?: [number, number];
  style?: 'solid' | 'dashed';
}

export interface CanvasPoint {
  id: string;
  label?: string;
  x: number;
  y: number;
  color?: string;
  snap?: number;
  lock_x?: boolean;
  lock_y?: boolean;
  min_x?: number;
  max_x?: number;
  min_y?: number;
  max_y?: number;
}

export interface CanvasFixedPoint {
  id?: string;
  x: number | string;
  y: number | string;
  label?: string;
  color?: string;
  style?: 'closed' | 'open';
}

export interface CanvasSegment {
  id?: string;
  from: [number | string, number | string];
  to: [number | string, number | string];
  color?: string;
  style?: 'solid' | 'dashed';
  label?: string;
}

export interface CanvasPolygon {
  id?: string;
  vertices: Array<[number | string, number | string]>;
  fill?: string;
  stroke?: string;
  label?: string;
}

export interface CanvasShadedRegion {
  id?: string;
  curve_top?: string;
  curve_bottom?: string;
  y_top?: number | string;
  y_bottom?: number | string;
  domain?: [number | string, number | string];
  fill?: string;
  label?: string;
}

export interface CanvasInequalityConfig {
  curve_id: string;
  initial_style?: 'solid' | 'dashed';
  initial_shade?: 'above' | 'below' | 'none';
  color?: string;
}

export interface CanvasInvariant {
  id?: string;
  kind:
    | 'point_on_curve'
    | 'point_coords'
    | 'slider_eq'
    | 'slider_range'
    | 'expr_true'
    | 'curves_intersect_at'
    | 'slope_at'
    | 'kink_at'
    | 'point_in_region'
    | 'inequality_state';
  point_id?: string;
  curve_id?: string;
  slider_id?: string;
  curve_a?: string;
  curve_b?: string;
  expr?: string;
  x?: number | string;
  target_x?: number | string;
  target_y?: number | string;
  target?: number;
  target_value?: number | string;
  expected?: number | string;
  min?: number;
  max?: number;
  tolerance?: number;
  expected_style?: 'solid' | 'dashed';
  expected_shade?: 'above' | 'below';
  distractor_id?: string;
  error_rationale?: string;
}

export interface TreeNodeSpec {
  id: string;
  label?: string;
  x: number;
  y: number;
  player?: string;
  payoff?: string;
  terminal?: boolean;
}

export interface TreeEdgeSpec {
  id: string;
  from: string;
  to: string;
  label?: string;
  action?: string;
}

export interface TreeInvariantsSpec {
  required_edges?: string[];
  required_info_sets?: string[][];
  distractor_id?: string;
  edge_error_rationale?: string;
  info_set_error_rationale?: string;
}

export interface InvariantCanvasSpec {
  mode: 'cartesian' | 'tree';
  x_range?: [number, number];
  y_range?: [number, number];
  step?: number;
  snap?: number;
  x_label?: string;
  y_label?: string;
  width?: number;
  height?: number;
  sliders?: CanvasSlider[];
  fixed_curves?: CanvasCurve[];
  interactive_curves?: CanvasCurve[];
  interactive_points?: CanvasPoint[];
  fixed_points?: CanvasFixedPoint[];
  segments?: CanvasSegment[];
  polygons?: CanvasPolygon[];
  shaded_regions?: CanvasShadedRegion[];
  inequality?: CanvasInequalityConfig;
  invariants?: CanvasInvariant[];
  interaction_mode?: 'edges' | 'info_sets' | 'both';
  nodes?: TreeNodeSpec[];
  edges?: TreeEdgeSpec[];
  tree_invariants?: TreeInvariantsSpec;
}

export interface MatchingItem {
  id: string;
  content: string;
  is_distractor?: boolean;
  distractor_id?: string;
  error_rationale?: string;
}

export interface ConceptMatchingSpec {
  left_title?: string;
  right_title?: string;
  premises: MatchingItem[];
  targets: MatchingItem[];
  correct_pairs: Record<string, string>;
  pair_rationales?: Record<string, string>;
}

export type StructuredUserAnswer =
  | { kind: 'open_symbolic'; expression: string }
  | { kind: 'proof_dag'; orderedStepIds: string[]; justifications: Record<string, string> }
  | {
      kind: 'adversarial_break';
      selectedStepId: string | null;
      selectedReasonId: string | null;
      witnessValues: Record<string, string>;
    }
  | {
      kind: 'unstructured_model';
      phase1Roles: Record<string, string>;
      phase2SelectedIds: string[];
      phase3SelectedId: string | null;
      phase3Expression: string;
    }
  | {
      kind: 'invariant_canvas';
      sliderValues: Record<string, number>;
      pointPositions: Record<string, { x: number; y: number }>;
      selectedEdgeIds: string[];
      infoSets: string[][];
      inequalityStyle?: 'solid' | 'dashed';
      inequalityShade?: 'above' | 'below' | 'none';
    }
  | { kind: 'concept_matching'; pairs: Record<string, string> };

export type CorrectAnswer = string | number | string[] | FillBlankAnswer | Record<string, unknown>;

export interface Question {
  id: string;
  competency_id: string;
  type: QuestionType;
  interaction_type?: QuestionType;
  difficulty?: 'easy' | 'medium' | 'hard';
  stem: string;
  graph?: GraphSpec;
  options: QuestionOption[];
  correct_answer: CorrectAnswer;
  diagnostic_distractors?: DiagnosticDistractor[];
  symbolic_config?: SymbolicConfig;
  proof_dag?: ProofDagSpec;
  adversarial_break?: AdversarialBreakSpec;
  unstructured_model?: UnstructuredModelSpec;
  invariant_canvas?: InvariantCanvasSpec;
  concept_matching?: ConceptMatchingSpec;
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
  modules?: ContentModule[];
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

export type SessionType =
  | 'practice'
  | 'quiz'
  | 'test'
  | 'challenge'
  | 'mastery_challenge'
  | 'misconception_drill';

export type FsrsRating = 1 | 2 | 3 | 4; // 1=Again, 2=Hard, 3=Good, 4=Easy

export type ReviewReason = 'error' | 'decay';

export interface FsrsCardState {
  due: string;
  stability: number;
  difficulty: number;
  elapsed_days?: number;
  scheduled_days: number;
  learning_steps?: number;
  reps: number;
  lapses: number;
  state: 0 | 1 | 2 | 3; // 0=New, 1=Learning, 2=Review, 3=Relearning
  last_review?: string;
}

export interface MisconceptionEntry {
  distractor_id: string;
  competency_id: string;
  rationale: string;
  count: number;
  last_seen: string;
  resolved_streak: number;
}

export interface SrsReviewTelemetry {
  date: string;
  competency_id: string;
  delta_t_days: number;
  predicted_r: number;
  actual_correct: boolean;
  rating: FsrsRating;
}

export interface CalibrationMetrics {
  n: number;
  brierScore: number | null;
  logLoss: number | null;
  meanPredictedR: number | null;
  meanActual: number | null;
  bias: number | null;
  isReliable: boolean;
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
  question_type?: QuestionType;
  wrong_attempts?: number;
  matched_distractor_ids?: string[];
  matched_distractor_rationales?: Record<string, string>;
  carried_distractor_ids?: string[];
  metacognitive_quadrant?: MetacognitiveItemAudit['quadrant'];
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
  cooldown_remaining_ms?: number;
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
    type: SessionType;
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
  review_reason?: ReviewReason;
  last_tier_promotion_at?: string;
  fsrs?: FsrsCardState;
  modality_latencies?: Partial<Record<QuestionType, number[]>>;
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
  last_mastery_challenge_at?: string;
  misconception_ledger?: Record<string, MisconceptionEntry>;
  srs_telemetry?: SrsReviewTelemetry[];
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

export type MetacognitiveConfidence = 'high' | 'medium' | 'low';

export interface IronExamQuestionDraft {
  selectedOption: string | null;
  selectedMultiOptions: string[];
  fillBlankValue: string;
  structuredAnswer: StructuredUserAnswer | null;
  canvasInteracted: boolean;
}

export interface MetacognitiveItemAudit {
  question_id: string;
  competency_id: string;
  type: QuestionType;
  confidence: MetacognitiveConfidence;
  is_correct: boolean;
  answered: boolean;
  quadrant:
    | 'calibrated_mastery'
    | 'illusion_of_competence'
    | 'lucky_guess'
    | 'known_gap';
  diagnostic_rationale?: string;
}

export interface MetacognitiveAudit {
  global_confidence: MetacognitiveConfidence;
  total_questions: number;
  answered_count: number;
  correct_count: number;
  calibrated_mastery_count: number;
  illusions_of_competence_count: number;
  lucky_guesses_count: number;
  known_gaps_count: number;
  calibration_score: number;
  items: MetacognitiveItemAudit[];
}

export interface IronDeferredReviewItem {
  question: Question;
  is_correct: boolean;
  answered: boolean;
  confidence: MetacognitiveConfidence;
  flagged: boolean;
  user_summary: string;
  diagnostic_rationale?: string;
}

export type AdaptiveModuleTier = 'diagnostic' | 'standard' | 'advanced';

export interface AdaptiveModuleResult {
  moduleIndex: 1 | 2;
  tier: AdaptiveModuleTier;
  score: number;
  total: number;
  percentage: number;
  elapsedSeconds: number;
}

export interface AdaptiveUnitBreakdownItem {
  competencyId: string;
  competencyName: string;
  correct: number;
  total: number;
  percentage: number;
  avgSeconds: number;
}

export interface AdaptiveExamSummary {
  module1: AdaptiveModuleResult;
  module2: AdaptiveModuleResult;
  routedTier: 'standard' | 'advanced';
  cutoffPercentage: number;
  projectedGrade20: number;
  avgSecondsPerQuestion: number;
  unitBreakdown: AdaptiveUnitBreakdownItem[];
}
