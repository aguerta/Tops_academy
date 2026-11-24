# 05. Auditoría *First Principles*: Adaptive Expertise, Límites Deterministas ($0 API) y Análisis de Milestones

> **Fecha:** 2026-11-24  
> **Tipo:** Auditoría cognitiva, verificación empírica del repositorio y análisis arquitectónico de hoja de ruta  
> **Documentos auditados:**
> 1. *Auditoría Cognitiva y Arquitectónica: Tops Academy frente a la Generación de Expertos* (PDF, 6 págs., v4.0 / M20)
> 2. *Tops Academy frente a la filosofía de Khan Academy — Análisis Comparativo y Arquitectura Cognitiva* (HTML)
> 3. [`docs/future_milestones/FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/future_milestones/FUTURE_MILESTONES.md)  
> **Restricciones duras fijadas por el mantenedor:**
> - **Objetivo final:** *Adaptive Expertise* (construida **secuencialmente**: primero Fluidez, luego Flexibilidad/Transferencia hacia exámenes cuantitativos y problemas inéditos).
> - **Restricción de calificación:** `$0 API` / calificación determinista local (**innegociable / hard**).
> - **Telemetría actual:** `0` datos empíricos de aprendizaje.
> - **Población inicial de prueba:** `N = 1` (uso personal del mantenedor en cursos reales).

---

## 1. Supuestos Ocultos Expuestos (*First Principles*)

Ambos documentos auditados saltan a roadmaps de funcionalidades (5 palancas en el PDF; 8 funciones de Khan + 6 ajustes cognitivos en el HTML) sin demostrar primero el cuello de botella real ni respetar las restricciones físicas del sistema.

| Supuesto Oculto en los Análisis | Qué es Convención / Analogía (Rechazable) | Qué es Verdad Fundamental (Física / Cognición / Datos) |
| :--- | :--- | :--- |
| **1. Benchmark prestado** | Comparar un arnés individual universitario contra Khan Academy (infraestructura escolar K–14) o contra *The Expert Myth* (ajedrez, medicina, escritores) como listas de chequeo normativas. | Un sistema solo puede evaluarse contra su propia función objetivo y restricciones. Importar funciones de Khan (SEL, barras de fecha de examen, *Ctrl+K*, suite de 4 prompts) sin cuello de botella probado es copia por analogía. |
| **2. "Lo que falta en la teoría = causa de fallo"** | Etiquetar brechas teóricas como "Críticas" o "P0" sin evidencia de aprendizaje. | La memoria de trabajo, la recuperación y el espaciado son leyes reales, pero **con `0` telemetría** no existe prueba de si el fallo actual ocurre en adquisición inicial, incorporación tras fallo, sobreajuste a plantillas o retención. |
| **3. Compatibilidad entre calificación abierta y `$0 API`** | Proponer *Shop Time* (demostraciones escritas de 30–90 min, defensa de modelos abiertos) e IRT/Elo + FSRS por `competencia × arquetipo × D-XX-YY`. | La calificación determinista exige un invariante verificable por máquina; las pruebas en prosa abierta y la defensa empírica de supuestos no lo tienen. Además, con `N = 1`, IRT/Elo y FSRS por tupla fina sufren escasez severa de datos (*sparsity*). |
| **4. Estado real de los datos en producción** | El reporte HTML asume que `ContentCoreDrawer` tiene contenido teórico poblado y que `archetype` existe en runtime. | Verificación directa en `courses/*.json`: **`content_modules = 0`** en 5/5 cursos M20 publicados y **`archetype = None`** en 5,320/5,320 ítems publicados. |

---

## 2. Verificación Empírica del Código y Bancos M20

Auditoría directa sobre `courses/*.json` y `platform/src/`:

1. **Cursos publicados M20 (`courses/*.json`):**
   - `estadistica_3_pre_pc2_m20.json`: 58 comp., 1,396 ítems — `content_modules = 0`, `archetype = None` (1,396/1,396).
   - `mateco_4_optimizacion_v20_k_3.json`: 27 comp., 963 ítems — `content_modules = 0`, `archetype = None` (963/963).
   - `mateco_4_optimizacion_k3_v2_m20.json`: 27 comp., 903 ítems — `content_modules = 0`, `archetype = None` (903/903).
   - `mateco_4_optimizacion_k4_m20.json`: 31 comp., 1,452 ítems — `content_modules = 0`, `archetype = None` (1,452/1,452).
   - `solow_v17_m20.json`: 19 comp., 606 ítems — `content_modules = 0`, `archetype = None` (606/606).
2. **[`PracticeSession.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/PracticeSession.tsx#L608-L636):**
   - `0` referencias a `masteryTier` y `0` referencias a `content_core`.
   - Aplica exactamente la misma cortina *Blank-First*, acceso a pistas y feedback inmediato a `Not started` y a `Proficient`/`Mastered`.
   - Tras 4 intentos fallidos (`isExhausted`), registra `isCorrect: false` y avanza al siguiente ítem sin verificar incorporación.
3. **[`sessionShuffler.ts`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/utils/sessionShuffler.ts#L39-L97):**
   - `calibrateByMasteryDifficulty` agrupa en 3 bandas estáticas (`easy`/`medium`/`hard`) y baraja con Fisher-Yates, sin adaptación intra-sesión.
4. **[`ContentCoreDrawer.tsx`](file:///d:/Augusto/personal_portfolio/Tops_academy/platform/src/components/ContentCoreDrawer.tsx#L43-L55):**
   - Soporta un único `worked_example` y actualmente recibe `0` módulos en todos los cursos M20.

### Veredicto Cruzado: Qué se sostiene vs. Qué falla
- **Se sostiene (mecanismos reales + bugs verificados):**
  - Pérdida de contrato pipeline $\to$ runtime (`archetype = None`, `content_modules = 0`).
  - Ciclo de incorporación roto tras *4-strikes* (leer la solución crea ilusión de corrección sin re-verificación).
  - Ilusión de generación abierta en modalidades M20 (>54% es andamiaje cerrado: ordenar pasos en `ProofDAG`, seleccionar roles/opciones en `Stage0Modeler`).
  - Andamiaje plano sin distinguir `Not started` de `Proficient+`.
- **Falla (analogía prestada, error factual o violación de restricciones):**
  - El reporte HTML recomienda 3 funciones sobre `ContentCoreDrawer` (hoy vacío) y 1 reporte por `archetype` (hoy `None`), e inventa puntajes en su gráfico *dumbbell* (da `5.0/5.0` en evocación libre pese a que >54% es andamiaje cerrado).
  - El reporte PDF propone *Shop Time* abierto (30–90 min) y calificación de hitos libres (viola `$0 API` determinista) e IRT/Elo + FSRS ultra-granular (inviable con `N = 1`).

---

## 3. Frontera Exacta de *Adaptive Expertise* bajo Restricción `$0 API` Determinista

### 3.1. Por qué ni Lean 4 ni un LLM "Sistema 1" (Gemini Nano / Flash sin razonamiento) resuelven la calificación abierta

1. **Lean 4 para pruebas de estudiantes:**
   - **Carga cognitiva extrínseca:** La memoria de trabajo sostiene ~4 bloques (*chunks*). Un estudiante de Optimización o Estadística Asintótica no puede gastar su memoria de trabajo en aprender el dominio *y simultáneamente* luchar contra tipos dependientes, tácticas y nombres de lemas de Mathlib. Sin 20–40 horas previas de fluidez en Lean 4, el sistema evalúa sintaxis del compilador, no pensamiento matemático. (Y envolver Lean 4 en menús desplegables de tácticas solo recrea `ProofDAG`).
   - **Frontera formal vs. empírica:** Lean 4 verifica validez deductiva interna a partir de axiomas fijos; **no puede** verificar si los supuestos de un modelo económico/estadístico son adecuados para un problema real ruidoso.
2. **Gemini "Sistema 1" API (modelo rápido no deliberativo o modelo local pequeño como Chrome Built-in AI / Gemini Nano):**
   - **Si es API en la nube:** Rompe la restricción dura de `$0 API` / PWA offline.
   - **Si es modelo pequeño/local o rápido (Sistema 1):** Calificar una demostración inédita o una defensa de modelo es una tarea de **Sistema 2** (detectar saltos lógicos sutiles, cuantificadores mal invertidos, condiciones de regularidad omitidas). Los modelos Sistema 1 tienen altas tasas de falsos positivos ante prosa matemática verosímil y alucinan contraejemplos—peor que no tener calificador, porque inyectan falsa confianza.

### 3.2. Secuencia Cognitiva y Descomposición en 4 Mecanismos

Confirmado contra los apuntes base (*Learning Fundamentals* y *Notes of The Practice of Learning*, N°28–29): **primero Fluidez** (automatizar esquemas básicos para liberar memoria de trabajo), **luego Flexibilidad** (estirar y romper esa automatización mediante variedad para impedir el sobreajuste).

| Mecanismo de *Adaptive Expertise* | ¿Verificable Determinísticamente a `$0 API`? | Señal Determinista Exacta |
| :--- | :---: | :--- |
| **1. Disociación Estructura Profunda vs. Superficie** (reconocer el principio bajo historias/notación inéditas y detectar supuestos rotos) | **Sí** | Selección de modelo sin etiqueta de unidad (*Fuzzy Boundary*), detección de condición violada o contraejemplo verificado por SymPy/mathjs/Z3. |
| **2. Compuerta de Árbol de Decisión Experto** (análisis cualitativo/estructural *antes* de calcular) | **Sí (parcial)** | Checkpoints previos obligatorios (signo, convexidad, régimen asintótico, identificabilidad, comportamiento en frontera) verificados determinísticamente antes del álgebra. |
| **3. Variedad Controlada (Anti-Overfitting)** (variedad de tarea y de atención sobre esquemas fluidos) | **Sí** | Interleaving entre unidades + rotación del invariante exigido sobre el mismo problema (`direct` $\to$ `inverse` $\to$ `perturbation` $\to$ `boundary`) con salidas deterministas. |
| **4. Síntesis Abierta y Defensa de Modelos** (pruebas largas desde cero, defensa de supuestos empíricos, explicación causal en prosa) | **No** | **Fuera de la frontera determinista.** No intentar fingirlo en la app; delegarlo explícitamente fuera del motor de calificación (revisión humana o puente manual `$0 API` hacia un modelo Sistema 2 externo). |

---

## 4. Hipótesis Falsables Mínimas para `N = 1` (Antes de Cambiar Pedagogía)

Con `N = 1` (uso personal) **no** son posibles pruebas A/B entre grupos ni calibración IRT/Elo. La falsación válida es **longitudinal intra-sujeto** (registro de eventos + sonda fría de transferencia):

1. **H1 — Sobrecarga en Novato (`content_modules = 0` + fricción plana):**
   - *Predicción falsable:* En competencias `Not started`, la tasa de fallo en 1.er intento + uso inmediato de pistas / abandono es marcadamente mayor que en `Familiar`, explicada por falta de exposición previa más que por dificultad del ítem.
2. **H2 — Fuga de Incorporación tras *4-Strikes*:**
   - *Predicción falsable:* Tras agotar 4 intentos en una trampa `D-XX-YY` y leer la solución, el mismo usuario vuelve a caer en la **exacta misma `D-XX-YY`** en el siguiente encuentro a una tasa similar a su línea base (demostrando que leer la solución no consolidó corrección).
3. **H3 — Ilusión de Andamiaje Cerrado / Overfitting Rutinario (Sonda de Transferencia):**
   - *Predicción falsable:* Alcanzar $\ge 85\%$ en sesiones etiquetadas/andamiadas (`ProofDAG`, `Stage0Modeler`, práctica aislada) pero caer $\ge 30$ puntos porcentuales en una **sonda fría, sin etiqueta de unidad y de respuesta libre** (`open_symbolic` / testigo numérico) con la misma estructura profunda y diferente envoltura superficial.
4. **H4 — *Expertise Reversal* Intra-Sujeto:**
   - *Predicción falsable:* En competencias ya `Proficient`/`Mastered`, las sesiones donde aún se consumen pistas o múltiples reintentos predicen peor desempeño diferido en `IronExamSession` que aquellas resueltas en frío.

---

## 5. Análisis de Hoja de Ruta (`FUTURE_MILESTONES.md`): ¿Adaptar Existentes o Crear Nuevo Milestone?

Revisión de los hitos activos en [`docs/future_milestones/FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/future_milestones/FUTURE_MILESTONES.md):

| Hito en `FUTURE_MILESTONES.md` | Decisión | Justificación *First Principles* |
| :--- | :--- | :--- |
| **Milestone 8 (FSRS), 14 (Mastery), 20 (Bloom/Iron)** | **No reabrir** | Ya cerrados en `MILESTONES_COMPLETED.md`; reabrirlos viola la gobernanza del roadmap. |
| **Milestone 19 (`k=4` / FTP) — P0** | **Mantener enfocado (+ 1 fix de contrato)** | Es ingeniería pura de compilación/cuota. Único ajuste menor: asegurar que `publish` deje de perder `archetype` (`None` $\to$ arquetipo real en `courses/*.json`). |
| **Milestone 15 F2 (Lean 4) y 16 F2 (Z3)** | **Sin cambios** | Lean 4 sigue en P3 Investigación para el kernel del pipeline; **no** extenderlo a calificación de pruebas de estudiantes. |
| **Milestone 9 (Fusionado con M21) — P1** | **Adaptar (alcance quirúrgico)** | M9 ya es dueño de emitir `ContentCore` (`content_modules`, hoy `0`). Adaptar el esquema de `worked_example` para admitir **pares de *Contrasting Cases*** (`worked_examples: WorkedExample[]`, 1–2) cuando se implemente Paso 4 / Fase B. Rechazar las adiciones cosméticas de Khan (SEL, barras de fecha, *Ctrl+K*). |
| **Nuevo Milestone 22 (Propuesto)** | **Crear (estructurado en 2 Fases con compuerta empírica)** | Ningún hito abierto es dueño de la mecánica intra-sesión de `PracticeSession.tsx`, ni de la telemetría falsable `N=1`, ni de la sonda de transferencia sin etiquetas (Mecanismos 1–3). |

### Estructura Propuesta para el Nuevo Milestone 22 (Gated / Sin Solucionismo Prematuro)

> **Milestone 22: Telemetría Falsable (`N=1`), Sonda de Transferencia y Transición Determinista Fluidez $\to$ *Adaptive Expertise***

- **Fase 0 — Contrato de Datos y Compuerta de Falsación (P1, sin cambios pedagógicos aún):**
  1. Preservar `archetype` en la publicación de `courses/*.json` (corregir la pérdida del 100%).
  2. Registrar en almacenamiento local (exportable a JSON) el log mínimo intra-sujeto necesario para evaluar **H1, H2, H3 y H4** (primer intento limpio, `D-XX-YY` tras *4-strikes*, uso de pistas por `masteryTier`, y contraste práctica etiquetada vs. sonda fría).
  3. Añadir una **Sonda de Transferencia Fría** (ítems sin etiqueta de unidad/competencia, sin pistas, en `open_symbolic` / testigo numérico) para medir H3 directamente.
- **Fase 1 — Intervenciones Pedagógicas Condicionadas a Evidencia de Fase 0 (P2, *gated*):**
  - *Solo si H2 se confirma:* Cerrar el ciclo de incorporación en `PracticeSession.tsx` (re-verificación con variante isomórfica/perturbada tras *4-strikes*).
  - *Solo si H1 o H4 se confirman:* Conectar `masteryTier` en `PracticeSession.tsx` (andamiaje gradual: *Contrasting Cases* de M9 en `Not started`; retardo de pistas y auto-verificación previa en `Familiar+`).
  - *Solo si H3 se confirma:* Sesiones *Fuzzy Boundary* (sin etiqueta de unidad) y compuertas cualitativas previas al cálculo (Mecanismos 1–3 dentro de la frontera determinista).
- **Exclusiones Explícitas (Descartadas por *First Principles*):**
  - Sin IRT/Elo ni FSRS por `competencia × arquetipo × D-XX-YY` (escasez de datos con `N=1`).
  - Sin *Shop Time* abierto en prosa, ni calificador Lean 4 para estudiantes, ni LLM Sistema 1 como calificador.
  - Sin copia de funciones K–12 de Khan Academy (puntos cosméticos, micro-copy SEL, metas con fecha de examen, *Ctrl+K*, suite de 4 prompts).
