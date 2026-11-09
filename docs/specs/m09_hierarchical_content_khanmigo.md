# Especificación Técnica Detallada — Milestone 9
## Arquitectura Jerárquica de Contenido (PPT $\to$ Glosario, ContentCore Khanmigo en 5 Bloques, Supuestos Explícitos y Unidad 0 PRE-XX)

> **Documento de Especificación Técnica y Contratos de Datos**  
> **Hito Vinculado:** Milestone 9 en [`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/FUTURE_MILESTONES.md)  
> **Estado:** 🏛️ P1 — Arquitectura Curricular y Schemas.  
> **Regla de Sincronización:** Cualquier cambio en la estructura de los módulos, bloques de `ContentCore`, tipados de `platform/src/types.ts` o esquemas JSON (`cta.schema.json`, `course.schema.json`) debe registrarse en este archivo y sincronizarse con [`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/FUTURE_MILESTONES.md).

---

## 1. Fundamento Pedagógico: Superación de la Atomización Plana

El paradigma inicial del pipeline C2C trataba cada micro-competencia como una unidad curricular aislada y plana:
$$\text{Curso} \longrightarrow \text{Unidades Planas (Unit = Competencia)} \longrightarrow \text{Quiz / Challenge redundantes}$$

Esto fragmentaba la visión holística del estudiante y generaba repetición excesiva de unit tests para destrezas mínimas. El Milestone 9 reorganiza el curso en una estructura de 3 niveles anclada a las diapositivas o apuntes reales, precedida por una **Unidad 0 (*Get Ready*)** de nivelación diagnóstica:

$$\text{Unidad 0 (PRE-XX)} \longrightarrow \text{Contenido / PPT (Módulo)} \longrightarrow \text{Familia de Subtemas} \longrightarrow \text{Competencias (4 Arquetipos)}$$

---

## 2. Contratos Canónicos de Datos (TypeScript & JSON Schemas)

Estos tipos se incorporan en [`platform/src/types.ts`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/types.ts) y en los esquemas de validación `schemas/cta.schema.json` y `schemas/course.schema.json`:

```typescript
/**
 * Declaración formal de un supuesto explícito del modelo o teorema.
 * Permite entrenar al estudiante contra la ilusión de validez universal.
 */
export interface ExplicitAssumption {
  id: string; // ej. "A-MCO-01"
  name: string; // ej. "Exogeneidad Estricta"
  statement_latex: string; // ej. "\\mathbb{E}[u \\mid X] = 0"
  role_in_proof: string; // Qué paso exacto de la derivación analítica habilita este supuesto
  violation_consequence: string; // Qué propiedad colapsa si falla (sesgo, inconsistencia, etc.)
}

/**
 * Término de glosario contextualizado al módulo / PPT.
 */
export interface ContentGlossaryTerm {
  term: string;
  definition: string;
  formula_latex?: string;
  related_competencies?: string[];
}

/**
 * Estructura pedagógica obligatoria en 5 bloques (Transferencia Khanmigo / Sal Khan).
 * Erradica los resúmenes genéricos y modela la intuición experta.
 */
export interface ContentCore {
  title: string;
  prerequisite_recall: string; // 1. Qué herramienta previa necesita recordar el alumno hoy
  intuitive_analogy: string; // 2. Intuición física o económica antes del formalismo matemático
  governing_theorems_and_assumptions: {
    theorems_latex: string[];
    assumptions: ExplicitAssumption[]; // 3. Supuestos explícitos y qué pasa al violarlos
  };
  worked_example: {
    problem_latex: string;
    step_by_step_latex: string[]; // 4. Ejemplo resuelto citando el supuesto usado en cada paso
  };
  common_exam_pitfalls: string[]; // 5. Trampas clásicas de parciales y errores frecuentes
}

/**
 * Subtema que agrupa un subconjunto de 2 a 4 competencias con afinidad temática.
 */
export interface SubtopicUnit {
  id: string; // ej. "subtopic_01_steady_state"
  title: string;
  description: string;
  competency_ids: string[];
  quiz_question_pool?: string[];
}

/**
 * Módulo jerárquico correspondiente a una presentación real (PPT) o a la Unidad 0.
 */
export interface ContentModule {
  id: string; // ej. "module_00_get_ready" o "module_ppt_01_solow_growth"
  is_prerequisite_module?: boolean; // true para Unidad 0 "Get Ready" (PRE-XX)
  title: string;
  source_file: string;
  slide_range?: [number, number];
  glossary: ContentGlossaryTerm[];
  core: ContentCore;
  subtopics: SubtopicUnit[];
  content_challenge_pool: string[];
}
```

---

## 3. La Unidad 0 (*Get Ready* / Prerrequisitos Fundacionales `PRE-XX`)

### 3.1. Detección y Extracción Automática en Stage 1 (`compile_cta.py`)
Durante la fase de análisis de tareas cognitivas (CTA), el orquestador analiza las diapositivas de entrada e identifica las competencias instrumentales asumidas como conocidas:
- Álgebra matricial (inversión de matrices, rango, formas cuadráticas).
- Cálculo multivariable (derivadas parciales, multiplicadores de Lagrange, gradientes).
- Probabilidad y distribuciones fundamentales ($\chi^2$, Normal multivariada, propiedades de esperanza condicional).

Las competencias detectadas se etiquetan con el prefijo `PRE-XX` (ej. `PRE-01: Inversión de matrices 2x2`).

### 3.2. Evaluación Escalonada por Granularidad
1. **Quizzes Formativos de Subtema (3–5 reactivos):** Evaluaciones rápidas intercaladas dentro de la sesión de práctica.
2. **Challenge Integrador de la PPT (8–12 reactivos):** Evaluación transversal del módulo completo que mide la integración conceptual entre subtemas.
3. **Course Challenge Global (~30 reactivos):** Calibración muestral holística del curso completo.
