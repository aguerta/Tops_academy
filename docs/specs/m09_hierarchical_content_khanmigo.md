# Especificación Técnica Detallada — Milestone 9
## Arquitectura Jerárquica de Contenido (PPT $\to$ Glosario, ContentCore Khanmigo en 5 Bloques, Supuestos Explícitos y Unidad 0 PRE-XX)

> **Documento de Especificación Técnica y Contratos de Datos**  
> **Hito Vinculado:** Milestone 9 en [`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/FUTURE_MILESTONES.md)  
> **Estado:** 🏛️ **P1 — Quick Wins Completados y Certificados (2026-11-14)** *(Anclaje PPT, Unidad 0 `PRE-XX`, `ContentCoreDrawer` vía rápida, Backfill 8 cursos / 237 competencias y fix ETag en `courseLoader.ts`)*. **Remanente:** Paso 4 (Quizzes de Subtema 3–5 reactivos, Challenges integradores 8–12 reactivos y emisión nativa LLM de `ContentCore` en `compile_cta.py`).  
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

---

## 4. Análisis Forense de Implementación, Blast Radius y Estimación con Gemini 4 Hydrogen

> **Actualización de Ingeniería (2026-11-14):** Evaluación técnica del estado real del código fuente y re-estimación del esfuerzo bajo el workflow **Flash Duet** con **Gemini 4 Hydrogen (Medium / High)**.

### 4.1. Hallazgo Clave en el Código Actual (`cta.schema.json` vs. `run.py`)
Al auditar [`.agents/skills/content-to-course/schemas/cta.schema.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/schemas/cta.schema.json#L17-L47) frente a [`.agents/skills/content-to-course/run.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/run.py#L1269-L1277), se verificó que **gran parte de la materia prima de Milestone 9 ya se genera en Stage 1**, pero se descarta antes de llegar a la plataforma web:
- **`cta.json` ya contiene:** `evidence` (`doc`/`pdf`/`page`), `assumptions` (`id`, `name`, `statement_latex`, `role_in_proof`, `violation_consequence` — equivalente directo de `ExplicitAssumption`), `session`, `unit_index` y `source_examples`.
- **Dónde se recorta:** En `run.py` (`_instantiate_single_comp`, L1269–L1277), `course_comp_dict` solo exporta 7 campos básicos (`id`, `code`, `name`, `category`, `description`, `mastery_target`, `prerequisites`) hacia `courses/<course_id>.json`.

### 4.2. Impacto del Salto Generacional: Gemini 3.8 Flash vs. Gemini 4 Hydrogen (Medium / High)

| Métrica | Gemini 3.8 Flash | Gemini 4 Hydrogen (Medium) | Gemini 4 Hydrogen (High) | Impacto en Workflow *Flash Duet* |
| :--- | :---: | :---: | :---: | :--- |
| **Linaje** | Familia 3.8 | Destilado de **Gemini 4 Carbon** | Destilado de **Gemini 4 Carbon** (default) | Coherencia entre contratos Python (`cta.schema.json`) y TypeScript (`types.ts`). |
| **Velocidad de Salida** | ~111 tok/s | **~198+ tok/s** | **~180–198 tok/s** | **2.0x a 2.8x más rápido** en lecturas por lotes y edición multi-archivo. |
| **Intelligence Index** | ~31 | ~46–48 | **~51** (~1.65x vs 3.8 Flash) | Comprensión de esquemas cruzados al primer intento. |
| **Terminal-Bench 4.1 (Coding)** | **18.2%** | ~48–52% | **57.0% (>3x vs 3.8 Flash)** | Menos ciclos fallidos de `tsc`/`pytest` y menor tasa de retrabajo. |
| **Tasa de Alucinación** | Línea base (1x) | ~4x menor | **>5x menor** | Preservación estricta de invariantes M1/M6 sin inventar props. |

- **Asignación recomendada en Flash Duet:** **Hydrogen Medium** para Implementadores de frontera cerrada y Auditores Forenses; **Hydrogen High** (o Argon High) para Orquestador / lógica cruzada densa (`CourseOverview.tsx` + `masteryStorage.ts` + `compile_cta.py`).

### 4.3. Desglose Incremental (*Quick Win* vs. *End-to-End*)
1. ✅ **Paso 1 — Anclaje a Diapositivas (`evidence` + `session`):** Exportar `evidence`, `session` y `unit_index` en `run.py` $\to$ tipar en `types.ts` $\to$ agrupar visualmente por `doc`/`pdf` y rango de páginas en `CourseOverview.tsx` + `hierarchyAdapter.ts` *(Completado 2026-11-14)*.
2. ✅ **Paso 2 — Calentamiento sin Fricción (Unidad 0 `PRE-XX`):** Prefijo `PRE-` y `is_prerequisite` habilitados en `cta.schema.json`, `schema_validator.py`, `compile_cta.py`, `cta_merge.py`, `prompt_cta_architect.md`, `MasteryGrid.tsx` y `Sidebar.tsx` *(Completado 2026-11-14)*.
3. ✅ **Paso 3 (Vía Rápida) — `ContentCore` en 5 Bloques + Glosario + Backfill:** Propagación de `assumptions` y `source_examples` en `run.py`, síntesis retrocompatible en `hierarchyAdapter.ts`, visor `ContentCoreDrawer.tsx` compatible con Split 50% (M1), hidratación determinista de 8 cursos (237 competencias) vía `scripts/backfill_m9_hierarchy.py` y corrección de invalidación `ETag` sin cabecera previa en `courseLoader.ts` *(Completado 2026-11-14)*.
4. ⏳ **Paso 4 (Remanente End-to-End) — Jerarquía de 3 Niveles, Emisión Nativa LLM y Evaluación Escalonada:** Emisión explícita de `modules[]` / `ContentCore` en `compile_cta.py` + `prompt_cta_harmonizer.md`, Quizzes formativos por `SubtopicUnit` (3–5 reactivos) y Challenges integradores por PPT (8–12 reactivos) en `App.tsx` + `masteryStorage.ts`.

### 4.4. Blast Radius Exacto End-to-End (16 Archivos en 3 Streams Disjuntos)

| Stream (Flash Duet) | Archivo | Acción | Qué cambia |
| :--- | :--- | :---: | :--- |
| **9A: Schemas & C2C** | [`.agents/skills/content-to-course/schemas/cta.schema.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/schemas/cta.schema.json) | MODIFY | Regex `PRE-XX` + definición opcional de `modules`, `glossary` y `content_core`. |
| **9A** | [`schemas/course.schema.json`](file:///d:/Augusto/personal_portfolio/Tops_academy/schemas/course.schema.json) (`src/validator/models.py`, `rules.py`) | MODIFY | Admitir `modules?: ContentModule[]`, `evidence`, `assumptions` con retrocompatibilidad v1/v2. |
| **9A** | [`.agents/skills/content-to-course/compile_cta.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/compile_cta.py) | MODIFY | Compilar `PRE-XX`, `MODULES`/`GLOSSARY`/`CONTENT_CORE` o auto-agrupar desde `evidence`. |
| **9A** | [`.agents/skills/content-to-course/cta_merge.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/cta_merge.py) & [`check_cta.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/check_cta.py) | MODIFY | Preservar `PRE-XX` al inicio del DAG topológico y validar bloques de `ContentCore`. |
| **9A** | [`.agents/skills/content-to-course/run.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/run.py#L1269-L1277) & [`course_publisher.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/course_publisher.py) | MODIFY | Propagar `evidence`, `assumptions`, `session` y construir `modules[]` en `course.json`. |
| **9A** | `system_prompts/lean/prompt_cta_architect.md` & `prompt_cta_harmonizer.md` | MODIFY | Instrucción compacta para emitir `PRE-XX` y `ContentCore` por PPT. |
| **9B: Plataforma React** | [`platform/src/types.ts`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/types.ts) | MODIFY | Interfaces `ExplicitAssumption`, `ContentGlossaryTerm`, `ContentCore`, `SubtopicUnit`, `ContentModule`. |
| **9B** | `platform/src/utils/hierarchyAdapter.ts` | NEW | Adaptador puro que sintetiza módulos desde cursos planos existentes sin romper compatibilidad. |
| **9B** | `platform/src/components/ContentCoreDrawer.tsx` | NEW | Visor ergonómico (Split 50% M1) de los 5 bloques Khanmigo + Supuestos Explícitos + Glosario LaTeX. |
| **9B** | [`platform/src/components/CourseOverview.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/CourseOverview.tsx) & [`Sidebar.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/Sidebar.tsx) | MODIFY | Unidad 0 (`PRE-XX`), acordeones por PPT, acceso a `ContentCore`/Glosario, Subtemas (Quiz 3–5) y Challenge PPT (8–12). |
| **9B** | [`platform/src/App.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/App.tsx) & [`masteryStorage.ts`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/utils/masteryStorage.ts) | MODIFY | Lanzamiento de `subtopic_quiz` y `module_challenge` reutilizando calibración bidireccional M14. |
| **9C: Backfill & Tests** | `scripts/backfill_m9_hierarchy.py` + `tests/platform/test_m9_hierarchy.py` + `tests/pipeline/test_m9_cta_modules.py` | NEW | Inyección determinista de `evidence`/`assumptions`/`modules` en cursos existentes (`< 2 s`) + suite de contratos. |

### 4.5. Estimación de Tiempo Actualizada

| Modalidad | Gemini 3.8 Flash (Legado) | Gemini 4 Hydrogen (Secuencial) | **Flash Duet Paralelo (Hydrogen Medium/High)** |
| :--- | :---: | :---: | :---: |
| **Quick Win Incremental** *(Anclaje PPT + Supuestos + `PRE-XX` + Backfill)* | ~1.5 – 2 h | ~18 – 25 min | **~10 – 14 min** |
| **Milestone 9 Completo End-to-End** *(Gate 1: 9A + 9B $\to$ Gate 2: 9C)* | 5 – 7 h | ~50 – 70 min | **~25 – 35 min** |
