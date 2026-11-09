# Especificación Técnica Detallada — Milestone 14
## Motor de Maestría Integral 2.0 Estilo Khan Academy (Calibración Bidireccional en Challenge/Test/Quiz, Híbrido 80/20, Hint-Cap y Simulador Adaptativo)

> **Documento de Especificación Técnica y Psicométrica**  
> **Hito Vinculado:** Milestone 14 en [`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/FUTURE_MILESTONES.md)  
> **Estado:** 🎯 P1 — Prioridad Psicométrica y Pedagógica (~1.5 a 2 d).  
> **Regla de Sincronización:** Cualquier ajuste en la lógica de transiciones de maestría, penalización por fallo, cálculo global o componentes de `platform/src/utils/masteryStorage.ts` debe registrarse en este archivo y en [`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/FUTURE_MILESTONES.md).

---

## 1. Fundamentos Psicométricos y Pedagógicos (Estándar Khan Academy)

```mermaid
flowchart TD
    subgraph ChallengeSession ["Sesión de Course Challenge (~30 Reactivos Seleccionados)"]
        CC1["Reactivo de Competencia A\n(Acierto ✅)"]
        CC2["Reactivo de Competencia B\n(Fallo ❌ - 'Tener una mala')"]
        CC3["Reactivo de Competencia C\n(Acierto ✅)"]
    end

    subgraph StateBefore ["Nivel de Maestría Previo"]
        SA["Comp A: Familiar (50 pts)"]
        SB["Comp B: Mastered (100 pts)\n(Creencia de maestría total)"]
        SC["Comp C: Not started (0 pts)"]
    end

    subgraph StateAfter ["Re-calibración Dinámica Bidireccional (Post-Challenge)"]
        RA["Comp A: Proficient (80 pts) ⬆️\n(Promoción por acierto demostrable)"]
        RB["Comp B: Proficient (80 pts) ⬇️\n(DEGRADACIÓN OBLIGATORIA POR FALLO)\nFragilidad detectada: pierde estatus Mastered"]
        RC["Comp C: Familiar (50 pts) ⬆️\n(Aceleración diagnóstica sin pasar por 100%)"]
    end

    subgraph UIReport ["CompletionScreen.tsx & Overview"]
        UI1["Desglose Granular: Leveled Up vs Leveled Down"]
        UI2["Botón Directo: 'Practicar Comp B para recuperar Mastered'"]
        UI3["Recálculo Global de Maestría del Curso (% de Skills Proficient/Mastered)"]
    end

    CC1 -->|Acierto| SA --> RA
    CC2 -->|Fallo| SB --> RB
    CC3 -->|Acierto| SC --> RC
    RA --> UI1
    RB --> UI1
    RC --> UI1
    UI1 --> UI2
    UI1 --> UI3
```

1. **Evaluación Transversal, No Maestría Automática (*Assessment, Not Full Mastery*):**
   - El Course Challenge consta de ~30 preguntas estratificadas a lo largo de todo el árbol curricular.
   - Rendir o aprobar el Course Challenge ajusta los niveles de cada destreza individualmente, pero **no infla ciegamente todas las competencias al 100%**.
2. **Impacto en Niveles de Habilidad (Ajuste Bidireccional):**
   - Concluir una evaluación recalibra los niveles individuales (`Not started` $\leftrightarrow$ `Attempted` $\leftrightarrow$ `Familiar` $\leftrightarrow$ `Proficient` $\leftrightarrow$ `Mastered`) según el desempeño específico en cada competencia.
3. **Penalización y Degradación Estricta por Fallo Individual (*"En Caso de Tener una Mala"*):**
   - Si un alumno ostentaba una competencia en nivel `Mastered` (100 pts) o `Proficient` (80 pts) y durante el Course Challenge falla la pregunta de esa competencia, **la plataforma degrada inmediatamente su nivel** (`Mastered` $\to$ `Proficient`, o `Proficient` $\to$ `Familiar`).
   - Erradica la "maestría como trofeo estático inmutable": un error en un examen acumulativo demuestra fragilidad en la recuperación (*retrieval failure*) o interferencia proactiva/retroactiva que requiere remediación deliberada.

---

## 2. Matriz Canónica de Transición de Niveles en Evaluaciones Intercaladas

Cada pregunta contestada en `Course Challenge`, `Unit Test` o `Quiz` se mapea a su `competency_id`:

| Nivel Previo de la Skill | Desempeño en Pregunta(s) | Nuevo Nivel de la Skill | $\Delta$ Puntos | Efecto Pedagógico / Psicométrico |
| :--- | :---: | :---: | :---: | :--- |
| **`Mastered` (100 pts)** | ❌ **Incorrecta (Fallo)** | **`Proficient`** | **$-20$ pts** | **Degradación:** Pierde la maestría total ante evidencia de fallo. Obliga a re-evaluar la destreza. |
| **`Mastered` (100 pts)** | ✅ **Correcta (Acierto)** | **`Mastered`** | **$0$ pts** | **Ratificación:** Confirma retención a largo plazo y estabilidad en memoria activa. |
| **`Proficient` (80 pts)** | ❌ **Incorrecta (Fallo)** | **`Familiar`** | **$-30$ pts** | **Degradación:** Pierde la categoría intermedia por error conceptual; se sugiere práctica deliberada. |
| **`Proficient` (80 pts)** | ✅ **Correcta (Acierto)** | **`Proficient`** *(o `Mastered` si acumula Unit Test previo $\ge 80\%$ y 0 fallos históricos)* | **$0$ a $+20$ pts** | **Consolidación:** Mantiene solidez; puede alcanzar `Mastered` si cumple condición de prueba acumulada. |
| **`Familiar` (50 pts)** | ❌ **Incorrecta (Fallo)** | **`Attempted`** | **$-25$ pts** | **Degradación:** Retrocede a nivel elemental de intento. |
| **`Familiar` (50 pts)** | ✅ **Correcta (Acierto)** | **`Proficient`** | **$+30$ pts** | **Promoción:** Valida suficiencia operativa y eleva a nivel intermedio. |
| **`Attempted` (25 pts)** | ❌ **Incorrecta (Fallo)** | **`Attempted`** | **$0$ pts** | **Contención:** Registra el intento fallido sin cambios de nivel negativo. |
| **`Attempted` (25 pts)** | ✅ **Correcta (Acierto)** | **`Familiar`** | **$+25$ pts** | **Promoción:** Supera el umbral introductorio demostrando resolución correcta. |
| **`Not started` (0 pts)** | ❌ **Incorrecta (Fallo)** | **`Attempted`** | **$+25$ pts** | **Iniciación:** Marca la competencia como abordada por primera vez. |
| **`Not started` (0 pts)** | ✅ **Correcta (Acierto)** | **`Familiar`** | **$+50$ pts** | **Aceleración Diagnóstica:** Valida conocimiento previo significativo saltando al nivel *Familiar*. |

### Regla de Multi-Reactivo por Competencia
Si una evaluación incluye más de una pregunta de la misma competencia:
- **Acierto $\ge 80\%$:** Promoción o ratificación de nivel.
- **Acierto entre $50\%$ y $79\%$:** Retiene nivel actual (excepto si estaba en `Mastered`, en cuyo caso cualquier error degrada a `Proficient`).
- **Acierto $< 50\%$:** **Degradación estricta de 1 nivel hacia abajo**.

---

## 3. Extensión de Tipos y Métodos en `masteryStorage.ts`

```typescript
export interface ChallengeSkillResult {
  competency_id: string;
  competency_name: string;
  total_questions: number;
  correct_questions: number;
  previous_tier: MasteryTier;
  new_tier: MasteryTier;
  direction: 'up' | 'down' | 'maintained';
}

export interface ChallengeExecutionSummary {
  record: CourseMasteryRecord;
  overall_score: number;
  overall_total: number;
  overall_percentage: number;
  skills_leveled_up: ChallengeSkillResult[];
  skills_leveled_down: ChallengeSkillResult[];
  skills_maintained: ChallengeSkillResult[];
}

export function updateCourseChallengeWithSkillCalibration(
  course: Course,
  questionResults: Array<{ question: Question; isCorrect: boolean }>
): ChallengeExecutionSummary;
```

---

## 4. Las 6 Extensiones Estructurales del Motor Khan Academy 2.0

1. **Calibración Cross-Skill en `Quiz` y `Unit Test` Intercalados:**
   - Dado que `sessionShuffler.ts` inyecta ~40–45% de preguntas de prerrequisitos y unidades previas en `Quiz` y `Unit Test`, `handleCompleteSession` aplica actualización por `question.competency_id` en toda sesión intercalada.
2. **Fórmula Híbrida 80/20 en `calculateCourseProgress`:**
   - Barra de progreso global combinando **80% suma continua de `comp.points / (N * 100)`** + **20% proporción de competencias en `Proficient`/`Mastered`**, evitando que alumnos con múltiples habilidades en `Familiar` (50 pts) vean la barra congelada en 0%.
3. **Maestría Autónoma vs. Asistida por Pistas (*Hint-Assisted Cap*):**
   - Consultar la Pista 1 (recordatorio suave) no penaliza; abrir las Pistas 2 a 5 marca el reactivo como `assisted = true`, topando el ascenso máximo en `Familiar` (50 pts) hasta demostrar evocación autónoma.
4. **Degradación en Práctica/Quiz + Indicador *Red Dot* (`needs_review`):**
   - Obtener $< 50\%$ en una práctica o quiz degrada 1 escalón la competencia y enciende un indicador ámbar/rojo (*"Needs Review"*) en `MasteryGrid.tsx`.
5. **Recomendador Inteligente *"Up Next for You"* Basado en el DAG:**
   - Selecciona automáticamente la siguiente micro-destreza óptima priorizando: (a) prerrequisitos degradados, (b) competencias con *Red Dot*, y (c) frontera ZPD desbloqueada en el DAG.
6. **Simulador Cronometrado Adaptativo de Examen Parcial en 2 Módulos (Estilo SAT Bluebook / Khan Academy):**
   - Módulo 1 diagnóstico balanceado (12–15 reactivos con reloj visible/ocultable) cuyo desempeño enruta dinámicamente a un Módulo 2 Estándar (`easy`/`medium`) o Módulo 2 Avanzado (`hard` + Arquetipo 4), entrenando gestión de tiempo real bajo presión universitaria.

---

## 5. Criterios de Aceptación (AC-32 a AC-36)
- **AC-32 (Calibración Granular por Skill):** Actualización atómica de `record.competencies[comp_id]` tras Course Challenge.
- **AC-33 (Degradación Obligatoria ante Fallo):** Todo error en `Mastered` degrada a `Proficient` ($100 \to 80$ pts); en `Proficient` degrada a `Familiar` ($80 \to 50$ pts).
- **AC-34 (Promoción Progresiva ante Acierto):** Ningún Challenge individual promueve de `Not started` a `Mastered` directamente (*Assessment, Not Full Mastery*).
- **AC-35 (Desglose Visual en UI):** `CompletionScreen.tsx` despliega bloques diferenciados `Leveled Up` y `Leveled Down` con acceso directo a práctica correctiva.
- **AC-36 (Trazabilidad y Pruebas Unitarias):** Registro en `history` del evento `{ date, score, total, type: 'challenge', previous_tier, new_tier }`.
