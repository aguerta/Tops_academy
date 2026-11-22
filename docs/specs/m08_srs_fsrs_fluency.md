# Especificación Técnica Detallada — Milestone 8
## Motor de Retención Espaciada FSRS-5/6 (`ts-fsrs`), *Mastery Challenge* (12h), *Misconception Ledger* y Fluidez

> **Documento de Especificación Técnica, Psicométrica y de Evaluación**  
> **Hito Vinculado:** Milestone 8 en [`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/FUTURE_MILESTONES.md)  
> **Estado:** 🔁 **P2 — Especificación Técnica Completa (Listo para Implementación).**  
> **Regla de Sincronización:** Cualquier cambio en el scheduler FSRS, tabla de mapeo automático, umbrales de decaimiento o contratos de `masteryStorage.ts` / `types.ts` debe registrarse simultáneamente en este archivo y en [`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/FUTURE_MILESTONES.md).

---

## 1. Fundamento Algorítmico: FSRS-5/6 (`ts-fsrs`) frente a SM-2 y Ebbinghaus Fijo

El enfoque clásico de umbrales estáticos (14 días / 45 días sin práctica) asume que todas las competencias y todos los estudiantes olvidan a la misma velocidad. **FSRS (*Free Spaced Repetition Scheduler*, v5/v6)** —el algoritmo moderno oficial de Anki— modela la dinámica de memoria específica por competencia mediante el **modelo DSR de tres componentes**:

1. **Difficulty ($D \in [1.0, 10.0]$):** qué tan intrínsecamente difícil resulta la competencia para este estudiante según su historial de aciertos, pistas y lapsus.
2. **Stability ($S > 0$, en días):** intervalo de tiempo esperado tras el cual la probabilidad de recordar la competencia cae al `90%`.
3. **Retrievability ($R(t) \in [0, 1]$):** probabilidad estimada de evocación exitosa tras $t$ días transcurridos desde la última práctica autónoma, modelada por la curva de olvido potencial de FSRS:
   $$R(t) = \left(1 + \text{FACTOR} \cdot \frac{t}{S}\right)^{\text{DECAY}}$$

### Ventajas Arquitectónicas en Tops Academy
- **Librería oficial `ts-fsrs` (~5 KB gzip, licencia MIT, 0 dependencias de backend):** corre 100% client-side en el navegador y PWA offline (GitHub Pages \$0).
- **Superioridad empírica frente a SM-2:** ajusta dinámicamente los intervalos de repaso según *retrievability* real al momento de la práctica (premiando repasos tardíos exitosos con mayor crecimiento de $S$ y evitando sobre-repasar competencias fáciles).
- **Integración limpia sobre el puente `Question`:** [`Question`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/types.ts#L480) ya transporta `competency_id`, `difficulty` y `diagnostic_distractors` (`D-XX-YY`), mientras `PracticeSession` e `IronExamSession` ya emiten `QuestionTelemetry` (acierto, `hints_used`, `seconds_spent`) hacia [`masteryStorage.ts`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/utils/masteryStorage.ts).

---

## 2. Tabla de Mapeo Automático sin Autocalificación del Estudiante

A diferencia de Anki, Tops Academy **no interrumpe al alumno** preguntándole *"¿Qué tan fácil fue?"* tras cada ejercicio. En su lugar, la telemetría objetiva capturada en `QuestionTelemetry` y `TimingStats` se traduce determinísticamente a los 4 grados de FSRS:

| Condición Objetiva del Intento / Sesión | Rating FSRS | Efecto en $(D, S)$ | Justificación Cognitiva |
| :--- | :---: | :--- | :--- |
| **Fallo (`is_correct = false` o `score = 0`)** | **`Again (1)`** | Sube $D$; contrae drásticamente $S$ (lapsus). | Evidencia fallo de recuperación o trampa activa; re-cola inmediata en remediación. |
| **Acierto asistido (`hintsUsed >= 2`) o latencia lenta (`seconds_spent > 2.0 * median_comp_seconds`)** | **`Hard (2)`** | Sube levemente $D$; crecimiento moderado de $S$. | Evocación con andamiaje o esfuerzo alto de Sistema 2. |
| **Acierto autónomo (`hintsUsed <= 1`) en tiempo normal (`0.7x..2.0x` de mediana)** | **`Good (3)`** | Estabiliza $D$; crecimiento estándar de $S$ según $R(t)$. | Evocación sólida y autónoma en ZPD esperada. |
| **Acierto autónomo fluido (`hintsUsed = 0` y `seconds_spent < 0.7 * median_comp_seconds`, con `n >= 3` previos)** | **`Easy (4)`** | Reduce $D$; acelera fuertemente $S$. | Fluidez consolidada de Sistema 1 (reconocimiento automático sin muletas). |

> [!NOTE]
> Cuando aún no existe historial suficiente para estimar `median_comp_seconds` ($n < 3$), el umbral de referencia usa el valor nominal por defecto según modalidad (`45 s` en `MC7`/`concept_matching`, `90 s` en `FIB`/`open_symbolic`, `120 s` en `proof_dag`/`adversarial_break`/`unstructured_model`/`invariant_canvas`).

---

## 3. Interacción con Tiers de Maestría M14 y Cooldown de 12 Horas

El motor FSRS **complementa** (no reemplaza) las transiciones deterministas de [Milestone 14](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m14_khan_mastery_engine.md):

1. **Decaimiento Suave (Indicador Visual `needs_review`) vs. Degradación de Tier:**
   - Al cargar un curso (`loadCourseMastery(courseId, now)`), se evalúa $R(t)$ en tiempo real sin mutar agresivamente los puntos ganados ante pequeñas demoras:
   - **`Mastered` con $R(t) < 0.85$** o **`Proficient` con $R(t) < 0.70$:** enciende `needs_review = true` y prioriza la competencia en la cola del *Mastery Challenge* y en el banner *Up Next for You*.
   - **Abandono Extremo ($R(t) < 0.50$):** degrada preventivamente `Mastered` $\to$ `Proficient` o `Proficient` $\to$ `Familiar` para evitar falsa sensación de dominio tras meses sin contacto.
2. ***Mastery Challenge* de 6 Preguntas y Cooldown de 12 Horas:**
   - Tarjeta transversal de 6 ítems que mezcla competencias con menor $R(t)$ (por debajo del umbral de retención objetivo) y competencias en `Proficient`.
   - **Regla de Oro de Ascenso:** únicamente un *Mastery Challenge* aprobado ($\ge 80\%$ global y acierto en la competencia) tras respetar un **cooldown mínimo de 12 horas** (`43,200,000 ms`) desde la última promoción a `Proficient` o intento previo de *Mastery Challenge* permite ascender de `Proficient` $\to$ `Mastered` (impidiendo *cramming* en una sola tarde).

---

## 4. Contratos TypeScript Retrocompatibles (`types.ts` y `masteryStorage.ts`)

Todos los campos nuevos son **opcionales** para mantener compatibilidad total con registros existentes en `localStorage` (`tops_academic_progress_v1`) y sincronización vía `cloudSync.ts`:

```typescript
export type FsrsRating = 1 | 2 | 3 | 4; // 1=Again, 2=Hard, 3=Good, 4=Easy

export interface FsrsCardState {
  due: string;             // ISO timestamp de próximo repaso óptimo
  stability: number;       // S en días
  difficulty: number;      // D en [1, 10]
  elapsed_days: number;
  scheduled_days: number;
  reps: number;
  lapses: number;
  state: 0 | 1 | 2 | 3;    // 0=New, 1=Learning, 2=Review, 3=Relearning
  last_review?: string;    // ISO timestamp del último repaso
}

export interface MisconceptionEntry {
  distractor_id: string;   // Ej. "D-Hab04-02"
  competency_id: string;
  rationale: string;
  count: number;
  last_seen: string;       // ISO timestamp
  resolved_streak: number; // Se limpia tras >= 2 aciertos autónomos consecutivos
}

export interface SrsReviewTelemetry {
  competency_id: string;
  delta_t_days: number;
  predicted_r: number;     // R(t) predicho antes de contestar
  actual_correct: boolean; // Resultado observado (para Brier Score)
  rating: FsrsRating;
}
```

Extensión sobre `CompetencyMastery` y `CourseMasteryRecord`:
- En `CompetencyMastery`: `fsrs?: FsrsCardState;` y `last_tier_promotion_at?: string;`
- En `CourseMasteryRecord`: `last_mastery_challenge_at?: string;` y `misconception_ledger?: Record<string, MisconceptionEntry>;`
- En `history`: campo opcional `srs_telemetry?: SrsReviewTelemetry[];` para auditoría longitudinal sin inflar almacenamiento.

---

## 5. *Misconception Ledger* y Bitácora de Fluidez (`ProgressLogView.tsx`)

1. **Cuaderno Personal de Trampas (*Misconception Ledger*):**
   - Cada vez que el estudiante falla eligiendo o activando un `distractor_id` (`D-XX-YY` en `MC7`, `MS`, `ds` de `FIB`/`open_symbolic`, pasos falaces de `proof_dag`/`adversarial_break`), incrementa `misconception_ledger[distractor_id]`.
   - Nuevo selector en [`sessionShuffler.ts`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/utils/sessionShuffler.ts): `buildMisconceptionSession(course, activeDistractorIds, count = 6)` que selecciona preguntas portadoras de esas trampas activas y las abre directamente en `PracticeSession.tsx` bajo el botón **"Practicar mis Trampas"**.
   - Cuando el estudiante acierta 2 veces seguidas una competencia sin activar la trampa (`resolved_streak >= 2`), la trampa pasa a estado resuelto.
2. **Bitácora de Fluidez (`ProgressLogView.tsx`):**
   - Vista dedicada con: (a) distribución actual de retención $R(t)$ por unidad, (b) curva de compresión de latencia media por pregunta (de Sistema 2 lento en los primeros intentos a Sistema 1 fluido), y (c) ranking de trampas frecuentes activas vs. superadas.

---

## 6. Plan de Evaluación y Pruebas en 2 Capas

Dado que un algoritmo SRS ocurre a lo largo de días/semanas, su validación se divide en dos capas estrictas:

### Capa 1 — Pruebas Deterministas en CI (*Clock-Injection Time-Travel*)
Toda función de cálculo FSRS y cooldown en `masteryStorage.ts` aceptará un parámetro inyectable `now: Date = new Date()`. La suite automatizada verificará mediante bundle real `esbuild` + `node`:
1. **Curva de Decaimiento Monótona:** avanzando el reloj virtual `+1d`, `+7d`, `+14d`, `+45d`, $R(t)$ decrece estrictamente y dispara `needs_review` al cruzar `0.85` (`Mastered`) y `0.70` (`Proficient`).
2. **Efecto de Espaciado y Contracción ante Lapsus:** un `Good` tras `t = 5d` produce mayor crecimiento de $S$ que un `Good` inmediato a `t = 0.01d`; un `Again` contrae $S$ e incrementa `difficulty` y `lapses`.
3. **Compuerta de Cooldown 12 Horas:** intentar ascender `Proficient -> Mastered` vía *Mastery Challenge* a las `11h 59m` mantiene el tier en `Proficient`, y a las `12h 01m` con acierto lo promueve a `Mastered`.
4. **Mapeo Automático y *Misconception Ledger*:** validación de los 4 ratings desde `(is_correct, hints_used, seconds_spent)` y limpieza de trampas tras `resolved_streak >= 2`.

### Capa 2 — Calibración Empírica Longitudinal (*Brier Score / Log-Loss*)
Cada evento en `history[].srs_telemetry` almacena `(predicted_r, actual_correct)`. Tras 2–4 semanas de uso real:
- **Brier Score:** $\text{BS} = \frac{1}{N}\sum_{i=1}^{N} (R_i - y_i)^2$ (meta: $\text{BS} < 0.20$).
- **Log-Loss:** $-\frac{1}{N}\sum_{i=1}^{N} [y_i \ln(R_i) + (1-y_i)\ln(1-R_i)]$.
- Si $R(t)$ sobreestima sistemáticamente los aciertos reales ($\text{mean}(R_i) > \text{mean}(y_i) + 0.08$), se ajustan los parámetros `request_retention` (por defecto `0.90` $\to$ `0.92`) o los pesos de mapeo de `Hard`/`Easy` sin migrar datos previos.
