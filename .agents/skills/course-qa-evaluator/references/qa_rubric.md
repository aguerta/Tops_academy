# Rúbrica Normativa de Auditoría de Calidad Pedagógica, Psicométrica y Path-to-Mastery v2.0

Esta rúbrica establece los estándares formales e implacables de evaluación para cursos en la plataforma **Top's Academy**, fusionando **Quality Matters (QM)**, **OSCQR**, **Bloom's 2-Sigma Mastery Learning**, **Zona de Desarrollo Próximo (ZPD — Vygotsky)**, **Práctica de Evocación Activa (Roediger & Karpicke)** y la arquitectura real del motor interactivo de Top's Academy (`sessionShuffler.ts`, `masteryStorage.ts`, `PracticeSession.tsx` 3-strikes, `FeedbackToast.tsx`).

---

## 1. Escala de Calificación y Dimensiones (Total: 20.0 Puntos)

### Dimensión 1: Arquitectura Curricular, Topología DAG y Calibración ZPD (0 a 4.0 puntos)
- **4.0 pts (Excelente)**: Micro-competencias atómicas balanceadas entre Hechos `[H]`, Conceptos `[C]` y Habilidades `[Hab]`; grafo DAG acíclico, conexo, en orden topológico válido (`idx(prereq) < idx(comp)` para soportar navegación *Up Next* e interleaving 60/40 en Quiz y 55/45 en Unit Test); **calibración ZPD real con 3 bandas de dificultad (`easy`, `medium`, `hard`) por competencia** para activar `calibrateByMasteryDifficulty` en todas las transiciones (`Not started` $\to$ `Mastered`).
- **2.2 - 3.2 pts (Aceptable con Brecha ZPD)**: DAG limpio y granularidad sólida, pero **colapso de calibración ZPD** (`100%` de reactivos codificados en una sola banda como `'medium'`, desactivando `calibrateByMasteryDifficulty` en el 100% de competencias: **deducción obligatoria de -1.2 a -1.5 pts**, techo máximo `2.5 - 2.8 / 4.0`) o nodos isla desconectados (`-0.2 a -0.4 pts`).
- **0.0 - 2.0 pts (Crítico / Deficiente)**: Contenido monolítico, ciclos en el DAG, prerrequisitos invertidos masivos o ausencia de progresión estructural.

### Dimensión 2: Calidad Psicométrica, Modalidad de Evocación y Anti-Gaming (0 a 5.0 puntos)
- **5.0 pts (Excelente)**: Diversidad genuina de modalidades cognitivas (combinando `multiple_choice_7_options`, `multiple_select` de discriminación condicional y `fill_in_the_blank` de evocación activa evaluado por `mathEquivalence.ts`); $\ge 4$ arquetipos matemáticos verdaderamente distintos por competencia (1=Directo, 2=Inverso, 3=Perturbación, 4=Frontera); distractores derivados de errores algebraicos/conceptuales reales; cero fugas, cero relleno artificial y alta entropía de claves correctas.
- **2.5 - 3.8 pts (Aceptable / Mecanización Parcial)**:
  - **Monocultivo 100% reconocimiento pasivo (`MC7 = 100%`, `FIB = 0%`, `MS = 0%`)**: Permite sustitución inversa desde las opciones sin generación activa, especialmente grave en Habilidades `[Hab]` (**deducción obligatoria: -1.0 a -1.3 pts**).
  - **Distractores numéricos sintéticos por multiplicador mágico (`1.333x`, `0.667x`, `1.667x`, `0.333x`)**: Generados mecánicamente sin origen cognitivo (**deducción: -0.6 a -1.2 pts**).
  - **Relleno burocrático de longitud para evadir `[R-15]`** (ej. `", para los parámetros bajo análisis"` añadido asimétricamente): Actúa como pista test-wise inversa (**deducción: -0.3 a -0.6 pts**).
- **0.0 - 2.4 pts (Crítico)**: Metainformación delatora visible, *Phantom Keying* / prefijos sintéticos (`"Opción alterna X:"`), **Vulnerabilidad de Memorización Visual** ($\le 4$ claves correctas únicas en $\ge 15$ ítems permitiendo alcanzar *Mastered* sin leer el enunciado), o **Corrupción Matemática de Claves / Cuantificadores Vacuos** (ej. sustituir $\varepsilon$ por constante fija manteniendo *"para todo $\varepsilon > 0$"* o desacuerdos no reparados de Stage-5 Blind Judges).

### Dimensión 3: Andamiaje Socrático Progresivo y Remediación Diagnóstica (0 a 5.0 puntos)
En `PracticeSession.tsx`, el estudiante dispone de **3 intentos (3-Strikes Safeguard)** antes del bloqueo con 0 puntos. Las pistas progresivas y el `error_rationale` de `FeedbackToast.tsx` son su único puente hacia el dominio:
- **5.0 pts (Excelente)**: 3 a 5 pistas socráticas genuinas, específicas a los datos/ecuaciones del reactivo (Pista 1: Conceptual $\to$ Pista 2: Estrategia procedimental $\to$ Pista 3: Articulación operativa sin regalar la clave); `error_rationale` 100% alineado con el error exacto que produce ese distractor específico; solución paso a paso clara y advertencia de error común no genérica.
- **2.5 - 3.9 pts (Aceptable)**: Pistas reales pero verbosas, escasas o parcialmente genéricas; reciclaje moderado de `error_rationale`.
- **0.5 - 2.0 pts (Crítico — Fallo de Andamiaje en Camino a Mastery)**:
  - **Pistas Mad-Libs sintéticas de compilador** (`"Identifique la estructura conceptual de {comp}: analice las relaciones formales..."` en $>50\%$ del banco): Aportan información nula al estudiante bloqueado (**techo estricto en D3: $\le 2.0 / 5.0$**).
  - **Envenenamiento Anti-Socrático de Pistas** (`"asegurando considerar adecuadamente: [distractor / omitir... / creencia falsa]"`): Sabotea activamente al estudiante induciéndolo a marcar un distractor y perder sus 3 intentos (**techo estricto en D3: $0.8 - 1.5 / 5.0$**, además de activar la penalización dura `socratic_hint_poisoning`).
  - **Desconexión Diagnóstica en `FeedbackToast`** (reciclaje $>90\%$ de `error_rationale` estáticos de `cta.json`, ej. explicar matrices $k\times k$ cuando el alumno cometió un error escalar aritmético): **-0.5 a -1.0 pt adicional**.

### Dimensión 4: Alineación Instruccional, Taxonomía de Bloom y Pureza de Dominio (0 a 4.0 puntos)
- **4.0 pts (Excelente)**: Congruencia absoluta entre objetivos, rigor matemático del dominio y evaluación; competencias de Habilidad `[Hab]` evaluadas y etiquetadas genuinamente en niveles superiores de Bloom (`Apply`, `Analyze`, `Evaluate`); enunciados redactados en registro disciplinar auténtico.
- **2.2 - 3.4 pts (Aceptable con Desalineación)**:
  - **Colapso declarativo de Bloom** (`100%` de reactivos —incluyendo Habilidades `[Hab]`— etiquetados como `Understand`): **-0.5 a -0.8 pts**.
  - **Contaminación léxica inter-dominio por prefijos robóticos** (ej. `"Teniendo en consideración los fundamentos del equilibrio"`, `"condiciones de frontera"`, `"ecuaciones fundamentales del régimen"` inyectados desde plantillas de Solow/EDP en un curso de Estadística): **-0.5 a -0.8 pts**.
  - Desacuerdos latentes de jueces ciegos (`stage5_judge_audit`) o ambigüedad matemática entre distractores y clave: **-0.5 a -1.2 pts**.
- **0.0 - 2.0 pts (Crítico)**: Preguntas huérfanas, teoremas falsos enseñados como verdaderos o desconexión severa con el sílabo fuente.

### Dimensión 5: Accesibilidad, Ergonomía Cognitiva en UI y Sintaxis KaTeX (0 a 2.0 puntos)
- **2.0 pts (Excelente)**: Sintaxis KaTeX 100% limpia (`$...$` balanceados, llaves cerradas, cero `$$$`, cero `{{...}}`), fórmulas renderizables sin desbordamiento móvil y notación simbólica canónica ($\hat{\theta}, \bar{Y}_n, \operatorname{plim}$).
- **0.8 - 1.5 pts (Aceptable con Fricción Ergonómica)**:
  - **Abuso de `$\text{...}$` para oraciones completas en prosa** ($\ge 45$ caracteres): Fuerza `white-space: nowrap` en KaTeX rompiendo el ajuste de línea en tarjetas de opciones (**-0.4 a -0.7 pts**).
  - **Pseudo-matemática con identificadores crudos de Python** (ej. `$theta_hat$`, `E[$theta_hat$]` en vez de `$\hat{\theta}$`): **-0.3 a -0.6 pts**.
- **0.0 - 0.7 pts (Crítico)**: Delimitadores `$` impares, llaves rotas masivas, residuos f-string sin interpolar o colapso visual severo.

---

## 2. Penalizaciones Duras Automáticas (Hard Deductions)

Se aplican deducciones directas acumulativas sobre la suma de las 5 dimensiones:
- **`bank_lt_3_exercises` (-2.0 pts)**: Si alguna competencia tiene $< 3$ problemas prácticos.
- **`hints_zero` (-1.0 pt c/u)**: Por cada ejercicio que carezca de pistas (`hints = 0`).
- **`orphan_questions` (-2.0 pts)**: Si existen preguntas huérfanas sin `competency_id` válido.
- **`socratic_hint_poisoning` (-1.5 pts)**: Si $\ge 5\%$ del banco instruye al alumno en pistas a *"considerar adecuadamente"* un distractor o error conceptual (sabotaje directo del límite de 3 intentos).
- **`vacuous_quantifier_key_corruption` (-1.0 pt)**: Si existen reactivos que sustituyen variables ligadas por constantes dejando cuantificadores universales vacuos (`para todo \varepsilon > 0`), corrompiendo la clave matemática.
- **`answer_memorization_exploit` (-0.5 pt por competencia, máx -2.0 pts)**: Por competencias ($\ge 15$ ítems) con $\le 4$ respuestas correctas únicas que permiten alcanzar *Mastered* por memorización visual.

> [!IMPORTANT]
> `final_score = max(0.0, min(20.0, round(sum_dimensions - sum_hard_penalties, 2)))`. El evaluador **DEBE** respetar las deducciones duras precalculadas y aplicar rigor absoluto sin inflación complaciente de notas.

---

## 3. Índice de Preparación para el Dominio — Mastery Path Readiness Index (`MPRI`: 0 a 100)

Complementariamente a la nota QM-OSCQR (`/20.0`), toda auditoría reporta el **`MPRI` (`/100.0`)** calculado sobre 6 pilares cognitivos y de plataforma:
1. **`zpd_adaptive_progression` (20 pts)**: Multibanda `easy`/`medium`/`hard` + alineación Bloom `Apply+` en Habilidades.
2. **`retrieval_modality_and_anti_gaming` (20 pts)**: Presencia de generación activa (`FIB`) / selección múltiple (`MS`), entropía de respuestas y ausencia de relleno `[R-15]` o cuantificadores vacuos.
3. **`socratic_scaffolding_lifeline` (25 pts)**: Pistas socráticas genuinas libres de boilerplate Mad-Libs y libres de envenenamiento anti-socrático.
4. **`diagnostic_remediation_alignment` (15 pts)**: Cobertura, unicidad y fidelidad diagnóstica de `error_rationale` sin distractores `1.333x` arbitrarios.
5. **`dag_and_interleaving_topology` (10 pts)**: Grafo DAG acíclico, conexo, en orden topológico y con anclaje de prerrequisitos para Quiz/Unit Test.
6. **`cognitive_ergonomics_and_framing` (10 pts)**: Pureza KaTeX, ausencia de `\text{prosa}` desbordante, ausencia de `$theta_hat$` crudo y ausencia de prefijos de dominios ajenos.

**Tiers de Certificación QM-OSCQR (`/20.0`)**:
- **EXCELENTE (17.0 - 20.0 pts)**: Producción inmediata certificada para dominio real.
- **ACEPTABLE (14.0 - 16.9 pts)**: Base matemática sólida pero con brechas de calibración adaptativa o ergonomía que requieren pulido.
- **DEFICIENTE (11.0 - 13.9 pts)**: Ilusión de maestría o fallos sistemáticos de andamiaje/modalidad; requiere refactorización de compilador/plantillas antes de certificar.
- **CRÍTICO (0.0 - 10.9 pts)**: Sabotaje cognitivo, claves corruptas o colapso severo; rechazado para estudio autónomo.

---

## 4. Esquema JSON de Salida Estructurada (`<course_id>_qa_report.json`)

```json
{
  "course_metadata": {
    "course_id": "string",
    "unit_title": "string",
    "detected_objective": "string",
    "total_competencies": 0,
    "total_questions": 0
  },
  "dimension_scores": {
    "architecture_granularity": { "score": 0.0, "max": 4.0, "feedback": "string" },
    "assessment_quality": { "score": 0.0, "max": 5.0, "feedback": "string" },
    "scaffolding_hints": { "score": 0.0, "max": 5.0, "feedback": "string" },
    "instructional_alignment": { "score": 0.0, "max": 4.0, "feedback": "string" },
    "technical_ergonomics": { "score": 0.0, "max": 2.0, "feedback": "string" }
  },
  "penalties_applied": [
    { "rule": "string", "reason": "string", "deduction": 0.0 }
  ],
  "raw_subtotal": 0.0,
  "final_score": 0.0,
  "quality_tier": "CRÍTICO (0-10.9) | DEFICIENTE (11-13.9) | ACEPTABLE (14-16.9) | EXCELENTE (17-20)",
  "mastery_path_readiness": {
    "mpri_score": 0.0,
    "mpri_max": 100.0,
    "mpri_tier": "string",
    "pillars": {
      "zpd_adaptive_progression": { "score": 0.0, "max": 20.0 },
      "retrieval_modality_and_anti_gaming": { "score": 0.0, "max": 20.0 },
      "socratic_scaffolding_lifeline": { "score": 0.0, "max": 25.0 },
      "diagnostic_remediation_alignment": { "score": 0.0, "max": 15.0 },
      "dag_and_interleaving_topology": { "score": 0.0, "max": 10.0 },
      "cognitive_ergonomics_and_framing": { "score": 0.0, "max": 10.0 }
    },
    "student_journey_verdict": "string"
  },
  "discovered_lint_rules": [
    {
      "rule_id": "string",
      "severity": "critical | warning | info",
      "regex_pattern": "string",
      "description": "string",
      "evidence_items": ["Q-001"]
    }
  ],
  "remediation_actions": [
    "string"
  ]
}
```
