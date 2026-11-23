# Especificación Técnica Detallada — Milestone 8
## Motor de Retención Espaciada FSRS-5/6 (`ts-fsrs`), *Mastery Challenge* (6 preg. + Cooldown 12h por Competencia), *Misconception Ledger* y Bitácora de Fluidez

> **Documento de Especificación Técnica, Psicométrica y de Evaluación**  
> **Hito Vinculado:** Milestone 8 en [`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/future_milestones/FUTURE_MILESTONES.md)  
> **Estado:** ✅ **COMPLETADO / VERIFICADO (2026-11-21) — Implementado y Certificado en `milestone_20` / `main`.**  
> **Regla de Sincronización:** Cualquier cambio en el scheduler FSRS, tabla de mapeo automático, umbrales de decaimiento, cooldown por competencia o contratos de `masteryStorage.ts` / `cloudSync.ts` / `types.ts` debe registrarse simultáneamente en este archivo y en [`docs/FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/future_milestones/FUTURE_MILESTONES.md).

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
- **Integración limpia sobre el puente `Question`:** el 100% de las preguntas en las 8–9 modalidades activas de [`Question`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/types.ts#L480) ya transportan `competency_id`, `type`, `difficulty` y `distractor_id` (`D-XX-YY`), mientras `PracticeSession` e `IronExamSession` emiten `QuestionTelemetry` hacia [`masteryStorage.ts`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/utils/masteryStorage.ts).

---

## 2. Granularidad de Actualización, Atribución Cross-Skill y Tabla de Mapeo Automático

### 2.1. Granularidad FSRS y Atribución Cross-Skill
- **1 revisión FSRS agregada por `(competency_id, session)`:** Si una sesión contiene múltiples preguntas de la misma competencia (por ejemplo, 4 preguntas de `C-01` en una Práctica), se agregan en **una única revisión FSRS** al cerrar la sesión. Esto evita distorsionar `S` y `reps` con ráfagas en el mismo minuto ($\Delta t \approx 0$).
- **Atribución Cross-Skill real en sesiones intercaladas (`Quiz`, `Unit Test`, `Mastery Challenge`, `Course Challenge` / `Iron Exam`, `"Practicar mis Trampas"`):** Cada pregunta se agrupa y calibra contra su propio `question.competency_id` (actualizando tanto su `MasteryTier` como su tarjeta FSRS y `Misconception Ledger`). En `Unit Test`, el puntaje agregado (`unit_test.percentage` y `isUnitCompleted`) sigue registrándose sobre la unidad objetivo para preservar la fórmula 80/20.

### 2.2. Mediana Personal por Modalidad (`speedRatio`) — Solo Premio de Fluidez, Nunca Castigo
Dado que una misma competencia mezcla modalidades rápidas (`MC7`, `concept_matching`) con modalidades analíticas largas (`proof_dag`, `unstructured_model`, `invariant_canvas`), y que un estudiante meticuloso resolviendo en papel no debe ser penalizado por tomarse 2 minutos, **la latencia nunca castiga a `Hard (2)`**. En su lugar, la latencia cumple dos funciones estrictamente positivas/analíticas:
1. Alimenta la **Curva de Fluidez** en `ProgressLogView.tsx`.
2. Cuando existen **$n \ge 3$ observaciones previas personales** para la tupla `(competency_id, modality)`, permite premiar con **`Easy (4)`** si el estudiante resuelve limpio a la primera y más rápido que `< 0.7x` su propia mediana personal:
   $$\text{speedRatio}_i = \frac{\min(\text{seconds\_spent}_i,\, 300)}{\text{personalMedian}(c, m)}$$
   *(si alguna pregunta de la competencia aún tiene $n < 3$ muestras personales en esa modalidad, `hasPersonalBaseline = false` y la sesión se evalúa como máximo en `Good (3)`).*

### 2.3. Tabla de Mapeo Automático sin Autocalificación del Estudiante
Tops Academy **no interrumpe al alumno** preguntándole *"¿Qué tan fácil fue?"*. Para cada competencia evaluada en una sesión (con `ratio = correct / total`, `hintsUsed = sum(hints_used)`, `totalWrongAttempts = sum(wrong_attempts)` capturado desde `wrongAttemptsCount` en `PracticeSession`, `hasLuckyGuess` verdadero si algún acierto en Modo Hierro tuvo `quadrant === 'lucky_guess'`, y `priorReviews = fsrs?.reps ?? 0`), el rating FSRS se deriva determinísticamente por orden de prioridad:

| Regla (Evaluación Secuencial Top-Down) | Rating FSRS | Efecto en $(D, S)$ | Justificación Cognitiva |
| :--- | :---: | :--- | :--- |
| **`ratio < 0.75`** *(incluye fallo en ítem único `0/1`)* | **`Again (1)`** | Sube $D$; contrae drásticamente $S$ (lapsus). | Fallo de recuperación o fragilidad severa; re-cola en remediación. |
| **`ratio ∈ [0.75, 1.0)`** **o** **`hintsUsed >= 2`** **o** **`totalWrongAttempts >= 1`** **o** **`hasLuckyGuess`** | **`Hard (2)`** | Sube levemente $D$; crecimiento moderado de $S$. | Señal cognitiva inequívoca de esfuerzo/fragilidad: acierto parcial, muletas, corrección tras error previo o acierto por azar en Modo Hierro. *(Nunca por reloj).* |
| **`ratio === 1.0`** **y** **`hintsUsed === 0`** **y** **`totalWrongAttempts === 0`** **y** **`hasPersonalBaseline`** **y** **`speedRatio < 0.7`** **y** **`priorReviews >= 3`** *(sin `low` confidence)* | **`Easy (4)`** | Reduce $D$; acelera fuertemente $S$. | Fluidez consolidada de Sistema 1: acierto limpio a la primera y `< 0.7x` su propia mediana personal. |
| **`ratio === 1.0`** *(resto: acierto a la primera con `hintsUsed <= 1`, sin importar si tardó 2+ min derivando en papel)* | **`Good (3)`** | Estabiliza $D$; crecimiento estándar de $S$ según $R(t)$. | Evocación sólida y autónoma en ZPD esperada. Cero falsos castigos por trabajo ordenado en papel. |

---

## 3. Interacción con Tiers de Maestría M14, Cooldown de 12h por Competencia y *Mastery Challenge*

El motor FSRS **complementa** las transiciones deterministas de [Milestone 14](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m14_khan_mastery_engine.md) preservando intacta la **fórmula híbrida 80/20** (`calculateCourseProgress`):

### 3.1. Regla de Ascenso `Proficient → Mastered` (Estilo Khan Estricto + 80/20 Intacto)
- **`Practice`, `Quiz`, `Unit Test` y `"Practicar mis Trampas"` (`misconception_drill`):** llegan como máximo a **`Proficient`** (80 pts).
  - Un **`Unit Test` al 100%** sigue marcando la unidad como **`Completed` (Verde)** y sigue aportando el **80%** de `calculateCourseProgress` sin ningún cambio; la única diferencia es que el *Mastery Tier* de la competencia queda en `Proficient` hasta validarse tras el intervalo de espaciado.
- **Vías de ascenso `Proficient → Mastered`:** únicamente **`Mastery Challenge` (6 preg.)** o **`Course Challenge` / `Iron Exam` (24–30 preg.)** pueden promover una competencia de `Proficient` $\to$ `Mastered` cuando:
  1. La competencia obtiene acierto limpio (`ratio === 1.0`, sin Hint-Cap `hintsUsed < 2`), **y**
  2. Han transcurrido **$\ge 12$ horas (`43,200,000 ms`)** desde `last_tier_promotion_at` (momento en que esa competencia alcanzó `Proficient`, o su `last_practiced` legacy si el campo no existía).
- **Cooldown estrictamente por competencia (no bloquea sesiones):** El temporizador de 12 horas **nunca bloquea abrir ni rendir** un *Mastery Challenge* ni un *Course Challenge*. Si el alumno rinde una sesión antes de las 12h, las competencias que ya cumplieron $\ge 12\text{h}$ sí ascienden a `Mastered`, mientras que las que aún tienen $< 12\text{h}$ se mantienen en `Proficient` (mostrando explícitamente el tiempo restante en `CompletionScreen.tsx`, ej. *"En enfriamiento 12h — faltan 6h 20m para Mastered"*).

### 3.2. Decaimiento en Memoria $R(t)$, `review_reason` y *Up Next for You*
Al evaluar el estado del curso (`loadCourseMastery(course, now)`), se calcula $R(t)$ en tiempo real para cada competencia con tarjeta FSRS:
1. **Separación de causa (`review_reason: 'error' | 'decay'`):**
   - Errores reales en cualquier sesión encienden `needs_review = true, review_reason = 'error'`.
   - **`Mastered` con $R(t) < 0.85$** o **`Proficient` con $R(t) < 0.70$:** enciende `needs_review = true` con `review_reason = 'decay'` (sin sobrescribir `'error'` si ya había error activo). Así la UI **nunca** muestra *"Se detectaron errores"* cuando la causa es únicamente decaimiento temporal.
2. **Abandono Extremo ($R(t) < 0.50$):**
   - Degrada preventivamente el tier (`Mastered` $\to$ `Proficient`, o `Proficient` $\to$ `Familiar`, actualizando `points`), **sin borrar ni modificar `unit_test.percentage`** (la barra 80/20 no retrocede silenciosamente).
   - La evaluación en lectura no dispara sincronización en la nube innecesaria salvo cuando ocurre una degradación persistible.
3. **Jerarquía de 6 Niveles en *Up Next for You* (`CourseOverview.tsx`):**
   - **Prioridad 1 — Error reciente (`review_reason === 'error'`, rojo):** `"Repasar ahora ➔"` sobre la primera unidad con laguna detectada.
   - **Prioridad 2 — Repaso Espaciado FSRS (`review_reason === 'decay'`, ámbar/índigo):** recomienda lanzar el **Mastery Challenge (6 preg.)** ordenando por menor $R(t)$ (indicando cuántas competencias requieren refresco).
   - **Prioridad 3 — Siguiente unidad no iniciada (`Not started`, azul).**
   - **Prioridad 4 — Unit Test pendiente (`< 100%`, ámbar).**
   - **Prioridad 5 — Course Challenge / Examen Modo Hierro (morado).**
   - **Prioridad 6 — Maestría Total 100% (esmeralda).**

### 3.3. *Mastery Challenge* (6 Preguntas) Separado del *Course Challenge*
- **Naturaleza distinta al *Course Challenge*:** El *Course Challenge* (24–30 preg. en Modo Hierro) sigue siendo el simulacro final del 20% del curso. El ***Mastery Challenge*** es una sesión rápida de **6 preguntas** que corre en [`PracticeSession.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/PracticeSession.tsx) (`sessionType = 'mastery_challenge'`), con feedback inmediato por ítem y Hint-Cap activo (sin cronómetro de Modo Hierro).
- **Selección (`buildMasteryChallengeQuestions(course, mastery, now, count = 6)`):**
  - **Nunca incluye competencias `Not started`** (disponible en cuanto exista $\ge 1$ competencia iniciada). Si hay $< 6$ competencias iniciadas, completa hasta 6 con preguntas distintas de esas mismas competencias.
  - Orden de prioridad de selección:
    1. Competencias con $R(t)$ vencido (`review_reason === 'decay'`), ordenadas de menor a mayor $R(t)$.
    2. Competencias en `Proficient` que **ya cumplieron el cooldown de $\ge 12\text{h}$** (elegibles para subir a `Mastered`).
    3. Competencias en `Familiar` o `Attempted` (o con error activo).
    4. Competencias en `Proficient` aún dentro de $< 12\text{h}$ o `Mastered` con menor $R(t)$ como relleno si faltan ítems hasta 6.
- **Calibración independiente por skill:** cada competencia evaluada dentro de las 6 preguntas se calibra de forma atómica e independiente (acierto limpio + $\ge 12\text{h}$ $\to$ `Mastered`; fallo $\to$ degrada 1 nivel), sin candado global del 80%.

---

## 4. Contratos TypeScript Retrocompatibles (`types.ts`, `masteryStorage.ts` y `cloudSync.ts`)

Todos los campos nuevos son **opcionales** para garantizar retrocompatibilidad 100% con registros existentes en `localStorage` (`tops_academic_progress_v1`) y sincronización vía [`cloudSync.ts`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/utils/cloudSync.ts):

```typescript
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
  due: string;             // ISO timestamp de próximo repaso óptimo
  stability: number;       // S en días
  difficulty: number;      // D en [1, 10]
  elapsed_days: number;
  scheduled_days: number;
  learning_steps?: number; // Requerido por ts-fsrs v5+
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
  resolved_streak: number; // Resuelta cuando >= 2 aciertos autónomos en preguntas portadoras
}

export interface SrsReviewTelemetry {
  date: string;            // ISO timestamp (para deduplicación en cloudSync)
  competency_id: string;
  delta_t_days: number;
  predicted_r: number;     // R(t) predicho ANTES de contestar
  actual_correct: boolean; // Resultado observado (para Brier Score / Log-Loss)
  rating: FsrsRating;
}
```

Extensiones retrocompatibles:
- En `QuestionTelemetry`:
  - `question_type?: QuestionType;`
  - `wrong_attempts?: number;` (número de intentos fallidos previos en esa pregunta antes de acertar/avanzar, desde `wrongAttemptsCount` en `PracticeSession`, `0` en Modo Hierro)
  - `matched_distractor_ids?: string[];` (IDs `D-XX-YY` efectivamente activados al fallar)
  - `matched_distractor_rationales?: Record<string, string>;`
  - `carried_distractor_ids?: string[];` (todos los `D-XX-YY` que porta la pregunta, para evaluar inmunidad en `resolved_streak`)
  - `metacognitive_quadrant?: MetacognitiveItemAudit['quadrant'];` (para detectar `lucky_guess` en Modo Hierro)
- En `CompetencyMastery`:
  - `fsrs?: FsrsCardState;`
  - `last_tier_promotion_at?: string;` (timestamp ISO del último ascenso a `Proficient` o superior)
  - `review_reason?: ReviewReason;`
  - `modality_latencies?: Partial<Record<QuestionType, number[]>>;` (últimas 15 latencias válidas por modalidad para calcular mediana por tupla `(comp, modality)`)
- En `CourseMasteryRecord`:
  - `last_mastery_challenge_at?: string;`
  - `misconception_ledger?: Record<string, MisconceptionEntry>;`
  - `srs_telemetry?: SrsReviewTelemetry[];` (ventana circular acotada a los **últimos 500 eventos por curso**)
- En `ChallengeSkillResult`:
  - `cooldown_remaining_ms?: number;` (presente cuando una skill en `Proficient` acertó pero sigue dentro de las 12h)
- En `cloudSync.ts`:
  - `mergeCompetencyMastery` preserva y fusiona `fsrs` (por `last_review` más reciente / mayor `reps`), `last_tier_promotion_at` (más reciente), `review_reason` y `modality_latencies`.
  - `mergeAllMasteryData` preserva y fusiona `last_mastery_challenge_at` (más reciente), `misconception_ledger` (por `distractor_id`, tomando `last_seen` más reciente y `max(count)` sin inflar duplicados) y `srs_telemetry` (deduplicado por `date|competency_id`, ordenado cronológicamente y acotado a 500 registros).

---

## 5. *Misconception Ledger* y Bitácora de Fluidez (`ProgressLogView.tsx`)

### 5.1. Cuaderno Personal de Trampas (*Misconception Ledger*)
1. **Captura en las 9 modalidades (incluyendo Modo Hierro):**
   - Solo se registran en `misconception_ledger` los fallos que activan un `distractor_id` real (`D-XX-YY`) en `MC7`, `MS`, `FIB` (`diagnostic_distractors`), `open_symbolic`, `proof_dag`, `adversarial_break`, `unstructured_model`, `invariant_canvas` o `concept_matching`.
   - Errores sin distractor coincidente (ej. errata libre o respuesta en blanco en Modo Hierro) siguen alimentando `needs_review` (`review_reason = 'error'`), `recent_misconceptions` y FSRS `Again(1)` sin contaminar el Ledger con IDs sintéticos.
   - Al activarse `distractor_id`, se incrementa `count += 1`, se actualiza `last_seen` y `rationale`, y se resetea `resolved_streak = 0`.
2. **Resolución estricta por trampa portadora (`resolved_streak >= 2`):**
   - Cuando el estudiante responde **correctamente y sin pistas (`hintsUsed === 0`)** una pregunta que contiene explícitamente `distractor_id` dentro de sus distractores (`carried_distractor_ids`), se incrementa `resolved_streak += 1` para cada entrada activa coincidente. Al alcanzar `resolved_streak >= 2`, la trampa pasa a estado **Superada**.
3. **Sesión *"Practicar mis Trampas"* (`buildMisconceptionSession`):**
   - Selector en [`sessionShuffler.ts`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/utils/sessionShuffler.ts): `buildMisconceptionSession(course, activeDistractorIds, count = 6)` filtra las preguntas del curso portadoras de esas trampas activas (balanceando entre trampas más frecuentes y distintas semillas) y las ejecuta en `PracticeSession.tsx` (`sessionType = 'misconception_drill'`).
   - Sus resultados actualizan `misconception_ledger`, FSRS y `MasteryTier` (con tope en `Proficient`, sin saltar el cooldown de 12h).

### 5.2. Bitácora de Fluidez y Retención (`ProgressLogView.tsx`)
- **Ubicación y Navegación:** Nueva vista dedicada (`AppViewMode = 'progress_log'`), integrada en [`navigationHistory.ts`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/utils/navigationHistory.ts) (retroceder vuelve limpio a `'overview'`), accesible desde un botón dedicado en [`Sidebar.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/Sidebar.tsx) y en [`CourseOverview.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/CourseOverview.tsx).
- **Visualización ligera (0 librerías externas de gráficas — SVG puro + Tailwind)** en 4 bloques:
  1. **Mapa de Retención $R(t)$ por Unidad:** barras de retrievability actual ($0\text{–}100\%$), próxima fecha óptima `due`, indicador de estado (`Óptimo`, `Por repasar`, `Crítico <50%`) y CTA directo a *Mastery Challenge*.
  2. **Curva de Fluidez (Compresión de Latencia Sistema 2 $\to$ Sistema 1):** gráfica SVG de evolución de segundos promedio por pregunta a lo largo de las sesiones del curso (`history`), destacando récord personal y reducción porcentual.
  3. **Cuaderno de Trampas (*Misconception Ledger*):** pestañas **Activas** vs. **Superadas (`resolved_streak >= 2`)**, mostrando `distractor_id`, competencia, rationale KaTeX, frecuencia, barra de progreso `resolved_streak / 2` y botón **"Practicar mis Trampas"** (cuando hay $\ge 1$ activa).
  4. **Calibración Empírica FSRS (Brier Score y Log-Loss):** panel calculado sobre `srs_telemetry` (hasta 500 eventos), mostrando Brier Score (meta `< 0.20`), Log-Loss, sesgo medio ($\overline{R} - \overline{y}$) y aviso de muestra mínima mientras existan `< 20` repasos con $\Delta t > 0$.

---

## 6. Plan de Evaluación y Pruebas en 2 Capas

### Capa 1 — Pruebas Deterministas en CI (*Clock-Injection Time-Travel*)
Toda función de cálculo FSRS, decaimiento y cooldown en `fsrsEngine.ts` y `masteryStorage.ts` acepta un parámetro inyectable `now: Date = new Date()`. La suite automatizada (`tests/platform/test_m8_fsrs_srs_and_ledger.py`) bundleará los módulos TypeScript reales con `esbuild` + `node` y verificará:
1. **Curva de Decaimiento Monótona:** avanzando el reloj virtual `+1d`, `+7d`, `+14d`, `+45d`, $R(t)$ decrece estrictamente, activa `review_reason = 'decay'` al cruzar `0.85` (`Mastered`) y `0.70` (`Proficient`), y degrada el tier (sin tocar `unit_test.percentage`) al cruzar `< 0.50`.
2. **Efecto de Espaciado y Contracción ante Lapsus:** un `Good` tras `t = 5d` produce mayor crecimiento de $S$ que un `Good` inmediato a `t = 0.01d`; un `Again` contrae $S$ e incrementa `difficulty` y `lapses`.
3. **Compuerta de Cooldown 12h por Competencia (Sin Bloquear Otras Skills):** en un mismo *Mastery Challenge* con 2 skills en `Proficient`, la skill A con `11h 59m` permanece en `Proficient` (reportando `cooldown_remaining_ms > 0`) mientras la skill B con `12h 01m` asciende simultáneamente a `Mastered`. Además, `Unit Test` 100% topa en `Proficient` preservando `isUnitCompleted === true` y el `80%` de `calculateCourseProgress`.
4. **Mapeo Automático sin Castigo por Reloj + Reintentos + Modo Hierro:** validación de `Again | Hard | Good | Easy` incluyendo fallo parcial (`3/4` $\to$ `Hard`, `2/4` $\to$ `Again`), reintento (`wrongAttemptsCount >= 1` $\to$ `Hard`), estudiante meticuloso en papel (`180s`, `0` pistas, `0` errores $\to$ `Good` limpio), `lucky_guess` $\to$ `Hard`, y premio `Easy` solo cuando `< 0.7x` su propia mediana personal ($n \ge 3$).
5. **Atribución Cross-Skill + *Misconception Ledger* + `cloudSync` Merge:** en un `Unit Test` intercalado, los ítems previos actualizan sus propias competencias; `resolved_streak` solo sube con `hintsUsed === 0` en preguntas portadoras del `distractor_id`; `mergeAllMasteryData` preserva `fsrs`, `misconception_ledger` y `srs_telemetry` (acotado a 500).

### Capa 2 — Calibración Empírica Longitudinal (*Brier Score / Log-Loss*)
Cada evento en `srs_telemetry` almacena `(date, competency_id, delta_t_days, predicted_r, actual_correct, rating)`. Tras 2–4 semanas de uso real ($\ge 20$ repasos espaciados):
- **Brier Score:** $\text{BS} = \frac{1}{N}\sum_{i=1}^{N} (R_i - y_i)^2$ (meta: $\text{BS} < 0.20$).
- **Log-Loss:** $-\frac{1}{N}\sum_{i=1}^{N} [y_i \ln(\hat{R}_i) + (1-y_i)\ln(1-\hat{R}_i)]$ (con recorte numérico $\hat{R}_i \in [10^{-6}, 1-10^{-6}]$).
- Si $R(t)$ sobreestima sistemáticamente los aciertos reales ($\text{mean}(R_i) > \text{mean}(y_i) + 0.08$), se ajustan `request_retention` (por defecto `0.90` $\to$ `0.92`) o los umbrales de `speedRatio` sin migrar datos previos.
