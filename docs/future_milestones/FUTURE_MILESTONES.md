# Hoja de Ruta Maestra de Evolución y Milestones: Tops Academy
## Elevando la Vara: Certificación Formal Multi-Agente Neuro-Simbólica (Lean 4), Transición hacia Evocación Activa (Bloom Superior), Multiplicación Anti-Overfitting con Gemini 4 y "Antigravity Study Harness"

> **Documento Estratégico y Hoja de Ruta Ejecutiva de Ingeniería**  
> **Fecha de Actualización:** 2026-11-21 (Branch: `milestone_20` / `main` — Arquitectura de 4 Ejes, Reforma `TPL-D3` Anti-Descarte, Milestone 20 Core + 20-B Modo Hierro cerrados, **`k = 2` (`DEFAULT_TEMPLATES_PER_MODALITY = 2`) consolidado como estándar estable de producción**, piloto empírico `k = 3` certificado en `mateco_4_optimizacion_v20_k_3` [`19.92/20.0`, `MPRI 99.65`], y hoja de ruta en M19 hacia `k = 4` bajo arquitectura *First-Pass & Quota-Safe* para Google AI Pro)  
> **Ubicación Canónica:** [`FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/FUTURE_MILESTONES.md) *(espejo byte a byte en [`docs/future_milestones/FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/future_milestones/FUTURE_MILESTONES.md))*.  
> **Áreas del Ecosistema:** Pipeline Multi-Agente C2C (`.agents/skills/content-to-course/` + Kernel Formal `Lean 4`), Motor Determinista y Simbólico (`engine/` + `SymPy`/`Z3`/`Lean 4`), Evaluador de Calidad (`course-qa-evaluator`), Plataforma Web (`React 18 + Vite + TypeScript + PWA`) y Marco Neurocognitivo de Adquisición de Pericia (*The Expert Myth* + *Khan Academy Mastery*).

---

## ⚠️ Regla Fundamental de Gobernanza y Sincronización Bidireccional (Innegociable para Agentes)

> [!IMPORTANT]
> **CONVENCIÓN DE REFERENCIAS TÉCNICAS Y ACTUALIZACIÓN CRUZADA:**
> 1. **Propósito de este Archivo:** Este documento (`FUTURE_MILESTONES.md`) es la **hoja de ruta estratégica de alto nivel**. Define el *qué*, el *por qué* cognitivo, las *prioridades*, los *criterios de aceptación (AC)* y las fases de ejecución de los hitos pendientes.
> 2. **Dónde vive la especificación profunda:** Para mantener este roadmap ágil y legible, los detalles de implementación técnica pesados (contratos TypeScript, esquemas JSON, teoremas Lean 4, matrices psicométricas de 12 filas, wireframes de UI y plantillas de prompts) **residen en los archivos especializados de referencia** listados abajo.
> 3. **Protocolo para Subagentes y Desarrolladores:**
>    - **Lectura Profunda Obligatoria:** Cuando un agente vaya a diseñar, auditar o implementar un hito, **DEBE abrir y leer el archivo de especificación técnica correspondiente** citado en la ficha del hito.
>    - **Actualización Bidireccional:** Si durante el desarrollo o la toma de decisiones arquitectónicas cambia el alcance, los contratos o la lógica de un hito, el agente **DEBE actualizar simultáneamente este archivo, su espejo en `docs/future_milestones/FUTURE_MILESTONES.md` y el archivo de especificación detallada vinculado**, garantizando cero desincronización (*zero drift*).
>    - **Cierre y Migración:** Al completarse y certificarse un hito con pruebas pasando, su ficha detallada se retira de este archivo y se traslada a [`MILESTONES_COMPLETED.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/MILESTONES_COMPLETED.md).

### Mapa del Ecosistema Documental

| Archivo de Referencia | Qué Contiene y Cuándo Debe Consultarse / Actualizarse |
| :--- | :--- |
| 📘 [`CONOCIMIENTO_TRIBAL.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/CONOCIMIENTO_TRIBAL.md) | **Física de inferencia, causas raíz y arquitectura causal:** Velocidades de streaming de `flash`, Matriz 2D de Gobernanza, las 11 patologías del código, mediciones de hardware (ASUS TUF vs 14" 150%), lecciones KaTeX (no `white-space: normal`) y contratos de los 4 arquetipos. Consultar siempre que se modifiquen hooks, compiladores o reglas de la plataforma. |
| 📗 [`MILESTONES_COMPLETED.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/MILESTONES_COMPLETED.md) | **Registro histórico de lo ya certificado:** Bitácora forense de entrega de los Milestones 1, 1-T, 2, 2a, 3, 4, 6, 7, 9 (Quick Wins), 10, 11 (núcleo), 12, 13, 14, 15 (F1), 16 (F1) y **20 (Core + 20-B Modo Hierro)**, con commits y suites de verificación. Consultar para auditar lo existente y registrar nuevos cierres. |
| 📄 [`docs/specs/m06_study_harness.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m06_study_harness.md) | **Especificación del Milestone 6:** Wireframes ASCII de 1/2 pantalla, máquina de estados de la cortina *Blank-First*, diagrama de secuencia, contraste de la Hipótesis Huerta y suite de 4 prompts Khanmigo \$0 API. |
| 📄 [`docs/specs/m09_hierarchical_content_khanmigo.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m09_hierarchical_content_khanmigo.md) | **Especificación del Milestone 9:** Tipados completos de TypeScript (`ContentCore`, `ContentModule`, `ExplicitAssumption`, `SubtopicUnit`), jerarquía de 3 niveles y extractor de Unidad 0 `PRE-XX`. |
| 📄 [`docs/specs/m14_khan_mastery_engine.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m14_khan_mastery_engine.md) | **Especificación del Milestone 14 y 14-B:** Matriz canónica de transición psicométrica de 12 filas, interfaces de `masteryStorage.ts`, fórmula híbrida 80/20, *Hint-Cap* y simulador adaptativo de parcial. |
| 📄 [`docs/specs/m15_m18_formal_lean4.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m15_m18_formal_lean4.md) | **Especificación de los Milestones 15 a 18:** Los 6 teoremas constructivos de `TopsAcademyC2C.lean`, compilación Perceus C FFI (`< 0.5 ms`), SMT Z3, arbitraje bicameral con $\alpha_{\text{Kernel}} = 0$ y arnés `#print axioms` con nonce criptográfico. |
| 📄 [`docs/specs/sintesis_plantillas_arquetipos.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/sintesis_plantillas_arquetipos.md) | **Especificación de los Milestones 19 y 20 (Fusionado con M5):** Arquitectura de los 4 ejes (Arquetipo, Modalidad, Dificultad y Taxonomía de Bloom), reforma `TPL-D3` para entrada libre (`FIB`/`open_symbolic`), inversión de cuota anti-descarte y multiplicación $K=2..3$ plantillas disjuntas por arquetipo con 3 candados anti-clon. |
| 📚 [`docs/investigaciones/`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/investigaciones/) | **Estudios fundacionales:** Investigaciones de desacoplamiento KaTeX (01, 02), limitaciones cognitivas de la plataforma (03, 04) y análisis forenses externos. |

---

## 1. El Diagnóstico Estratégico y Neurocognitivo: De la Identificación por Descarte a la Producción Analítica y Anti-Overfitting

En auditorías automatizadas bajo estándares Quality Matters (QM), OSCQR y Mastery Learning, el pipeline C2C alcanzó puntajes de excelencia formal (**18.7 – 20.0 / 20.0 pts**) en cursos masivos de alta complejidad técnica (`solow_growth_model`, `gavilano_pre_parcial` con 127 competencias, `asymptotic_statistics_v7` con 32 competencias).

Sin embargo, el contraste estricto frente a los principios de adquisición de pericia (*The Expert Myth*) y la Taxonomía de Bloom revela una **paradoja de falsa suficiencia**:

```mermaid
flowchart TD
    subgraph CurrentParadigm ["Paradigma Inicial (Riesgo de Descarte y Overfitting)"]
        P1["Predominio de Reconocimiento (MC7)\nIncentivado por TPL-D3; permite sacar la respuesta por descarte"]
        P2["1 Plantilla por Arquetipo (4 por Competencia)\nAunque cambien las semillas numéricas, el alumno memoriza el molde"]
        P3["Techo Cognitivo en FIB Numérico\nDificulta evaluar pasos deductivos, contraejemplos y producción simbólica"]
        P4["Canal Verbal-Simbólico Exclusivo\nCero evaluación gráfica interactiva (diagramas de fase, isoclinas, árboles)"]
        P5["Maestría Estática sin Decaimiento\nEstado permanente sin considerar el olvido longitudinal"]
    end

    subgraph FutureParadigm ["Nuevo Paradigma (Gemini 4): Evocación Activa, Bloom Superior y K Plantillas/Arquetipo"]
        N1["Inversión de Cuota y TPL-D3 en Entrada Libre\nFIB y Open Symbolic diagnostican trampas D-XX-YY sin mostrar opciones"]
        N2["Multiplicación K=2..3 Plantillas Disjuntas por Arquetipo\n8 a 12 plantillas/competencia con 3 candados anti-clon (AST, Bloom, Léxico)"]
        N3["Modalidades de Bloom Superior (Analyze / Evaluate / Create)\nProofDAG paso a paso, Adversarial Break, Stage 0 y Lienzo SVG en GitHub Pages $0"]
        N4["Arquitectura Jerárquica de Contenido (PPT/Módulo)\nContenido PPT -> [Glosario + Núcleo] + Familia de Subtemas"]
        N5["Motor SRS y Re-calibración Dinámica Khan 2.0\nDegradación obligatoria por fallo y decaimiento espaciado"]
    end

    CurrentParadigm ==>|Transformación Estratégica| FutureParadigm
```

### 1.1. La Arquitectura de los 4 Ejes en la Creación de Problemas y su Reforma

Cada plantilla en `TEMPLATES` es una tupla de 9 elementos (`[tpl_id, cid, qtype, gen_fn, ver_fn, (difficulty, bloom), stems, hints, sol]`) que cruza **4 ejes ortogonales**:

| Eje | Qué Define | Estado Actual Verificado (`compile_shard.py` — **`k=2` Estable**) | Evolución Estratégica (Habilitada por Gemini 4 — **Hito Futuro `k=4`**) |
| :--- | :--- | :--- | :--- |
| **1. Arquetipo** | Qué razonamiento exige al estudiante. | `MIN_ARCHETYPES = 4`: `direct`, `inverse`, `perturbation`, `boundary_or_edge_case` con **`DEFAULT_TEMPLATES_PER_MODALITY = 2` ($k=2$ estable en producción: $6..8$ plantillas/comp, `~786` preg/curso)** y piloto empírico $k=3$ certificado (`mateco_4_optimizacion_v20_k_3`, `963` preg, `19.92/20`, `MPRI 99.65`). | Mantener **$k=2$ como estándar estable por defecto** para proteger la cuota de Google AI Pro, y evolucionar hacia **$k=4$ (`12..16` plantillas/comp, `1,284+` preg/curso)** en [Milestone 19](#milestone-19-escalamiento-sostenible-a-k4-1284-reactivos-arquitectura-first-pass-75-1ra-compilación-y-protección-de-cuota-google-ai-pro) una vez alcanzadas las 5 metas *First-Pass & Quota-Safe* (`<= 11.55M` tokens brutos). |
| **2. Modalidad / Tipo** | Cómo responde el estudiante (interfaz cognitiva). | **Reforma `TPL-D3` y M20 activas en producción:** `0% MC7` en `Skill` (`Hab-*`), $\le 1$ `MC7` en `Concept`/`Fact`, $\ge 80\%$ activo en 8 modalidades (`FIB`, `MS`, `open_symbolic`, `proof_dag`, `adversarial_break`, `unstructured_model`, `invariant_canvas`, `concept_matching`). | Escalar de $k=2$ plantillas/modalidad a $k=4$ plantillas estructuralmente disjuntas por modalidad recomendada (o esquema híbrido $k=3$ plantillas $\times s=4$ semillas con `0` tokens LLM extra en Stage 4). |
| **3. Banda de Dificultad** | Ubicación en la Zona de Desarrollo Próximo (ZPD). | Cobertura obligatoria de las 3 bandas: `direct` $\to$ `'easy'`, `inverse` $\to$ `'medium'`, `perturbation` $\to$ `'hard'`, `boundary` $\to$ `'hard'`. | Se preserva el anclaje Tri-Banda por arquetipo para alimentar el enrutamiento ZPD (`sessionShuffler.ts`) y el simulador adaptativo en 2 módulos. |
| **4. Taxonomía de Bloom** | Profundidad del procesamiento cognitivo. | Mínimo 2 niveles por competencia. Regla dura `[M3-SKILL-BLOOM]`: prohibido `Remember`/`Understand` en `Hab-*` (exige `Apply` o superior). | **Ascenso taxonómico dentro de cada arquetipo:** Las $k$ plantillas de un mismo arquetipo/modalidad varían su tupla `(modalidad, bloom)`, empujando sistemáticamente hacia `Analyze`, `Evaluate` y `Create` (`73.52%` en `Analyze+Evaluate`, Tier `ÉLITE` demostrado en `v20_k_3`). |

### 1.2. Los 8 Puntos Ciegos Cognitivos que Definen la Nueva Vara
Fundamentados en los estudios [`docs/investigaciones/03_Limitaciones_de_la_plataforma_de_estudio.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/investigaciones/03_Limitaciones_de_la_plataforma_de_estudio.md) y [`04_Limites_de_la_plataforma_y_estudio.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/investigaciones/04_Limites_de_la_plataforma_y_estudio.md):
1. **Evocación Libre (*Free Recall*) vs. Reconocimiento:** Superar el descarte asistido exigiendo formular respuestas sin opciones visibles.
2. **Traducción Visoespacial (*Dual Channels*):** Evaluar interacción gráfico-espacial (diagramas de fase, isoclinas, campos vectoriales).
3. **Encadenamiento de Demostraciones (*Step-by-Step Proofs*):** Evaluar secuencias de micro-decisiones analíticas encadenadas.
4. **Combate a la Ilusión Explicativa:** Forzar la formulación activa y el contraste de contraejemplos.
5. **Formulación No Estructurada:** Filtrar regularidades relevantes frente a datos distractores en el enunciado.
6. **Trabajo Computacional (*Shop Time*):** Experimentación paramétrica sin solución analítica cerrada.
7. **Andamiaje Diferido (*Delayed Scaffolding*):** Retardo inicial de pistas para entrenar la metacognición.
8. **Síntesis Estructural (*Part-Whole*):** Unificar el aprendizaje en torno a la fuente real (PPT) con Glosario, Núcleo Conceptual y Challenges integradores.

### 1.3. Matriz de Contraste: *The Expert Myth* vs. Estado del Arte de Tops Academy

| Pilar de Pericia | Mecanismo Cognitivo Requerido | Estado Actual en Producción | Brecha Remanente (Gap hacia la Pericia) |
| :--- | :--- | :--- | :--- |
| **1. Evocación Pura vs. Reconocimiento** | Producir la respuesta o derivación frente a la hoja en blanco (*free recall*), sin descartar opciones. | Cortina Smart *Blank-First*, Navegación Mouseless ([Milestone 6](file:///d:/Augusto/personal_portfolio/Tops_academy/MILESTONES_COMPLETED.md#milestone-6-antigravity-study-harness-20-modo-blank-first-y-transferencia-khanmigo-0-api)) y **Milestone 20 (Core + 20-B Modo Hierro)**. Reforma `TPL-D3` con `ds` en `FIB`/`open_symbolic`, candados `[M20-MC7-CAP]` (**`0 MC7` prohibido en `Skill` / `Hab-*` y $\le 1$ `MC7` en `Concept`/`Fact`**), `[M20-ACTIVE-QUOTA]` ($\ge 80\%$ activo), 6 modalidades de Bloom Superior (`proof_dag`, `adversarial_break`, `unstructured_model`, `invariant_canvas`, `concept_matching`, `open_symbolic`) y simulacro cronometrado a libro cerrado con calibración metacognitiva obligatoria (`IronExamSession.tsx` + `MetacognitiveModal.tsx`) en producción estática (\$0). | ✅ Pilar cubierto en Milestone 20 (Core + 20-B Modo Hierro) con **`k=2` estable en producción**; escalamiento sostenible hacia $k=4$ bajo arquitectura *First-Pass* en [Milestone 19](#milestone-19-escalamiento-sostenible-a-k4-1284-reactivos-arquitectura-first-pass-75-1ra-compilación-y-protección-de-cuota-google-ai-pro). |
| **2. Variedad Estructural sin Overfitting** | Miles de intentos sobre el principio evitando que el alumno memorice un único molde de despeje. | **`DEFAULT_TEMPLATES_PER_MODALITY = 2` ($k=2$) estable en producción** (`6..8` plantillas/comp, `786` reactivos en `mateco_4_optimizacion_v20`, `19.37/20`, `MPRI 97.42`) + piloto empírico $k=3$ certificado (`mateco_4_optimizacion_v20_k_3`, `321` plantillas $\times 3$ semillas = `963` reactivos, `19.92/20`, `MPRI 99.65`). | ⚠️ Escalamiento sostenible a **$k=4$ (`1,284+` reactivos)** sin agotar la cuota de Google AI Pro mediante las 5 metas *First-Pass* ($\ge 75\%$ 1ra compilación, $\le 11.55\text{M}$ tokens brutos) ([Milestone 19](#milestone-19-escalamiento-sostenible-a-k4-1284-reactivos-arquitectura-first-pass-75-1ra-compilación-y-protección-de-cuota-google-ai-pro)) + deducción SMT Z3 ([Milestone 16 F2](#milestone-16-fase-2-deducción-algebraica-automática-con-z3-y-lemas-lean-4)). |
| **3. Alta Validez Interna y Rigor Formal** | Garantía matemática de ausencia de colisiones, ciclos curriculares o enunciados incompletos. | Patrón PrairieLearn `@var@`, compilador AST `KaTeXAST` ([Milestone 4](file:///d:/Augusto/personal_portfolio/Tops_academy/MILESTONES_COMPLETED.md)) y Kernel Python isomórfico ([Milestone 15 F1](file:///d:/Augusto/personal_portfolio/Tops_academy/MILESTONES_COMPLETED.md)). | ⚠️ Binario nativo Perceus C Lean 4 `< 0.5 ms` ([Milestone 15 F2](#milestone-15-fase-2-kernel-nativo-perceus-c-lean-4-ffi-05-ms-y-drt-industrial)), clausura epistémica DAG ([Milestone 17](#milestone-17-certificación-formal-del-dag-curricular-clausura-epistémica-y-arbitraje-neuro-simbólico)) y arnés CI `#print axioms` ([Milestone 18](#milestone-18-arnés-de-certificación-continua-anti-drift-de-contratos-y-auditoría-print-axioms)). |
| **4. Feedback Inmediato** | Diagnóstico instantáneo de por qué falló el razonamiento. | Refutation Feedback en Toast (`FeedbackToast.tsx`) con `error_rationale`. | ⚠️ Falta bifurcación adaptativa de examen parcial en 2 módulos ([Milestone 14-B](#milestone-14-b-simulador-cronometrado-adaptativo-de-examen-parcial-en-2-módulos-sat-bluebook)); remediación y degradación core cerradas en [Milestone 14](file:///d:/Augusto/personal_portfolio/Tops_academy/MILESTONES_COMPLETED.md#milestone-14-motor-de-maestría-integral-20-estilo-khan-academy-calibración-bidireccional-híbrido-8020-fluidez-y-motor-up-next). |
| **5. Práctica Deliberada y Retención** | Operar en ZPD (70–85%), clasificar problemas ciegos y frenar olvido. | Interleaving pedagógico dinámico y ZPD implementados (`sessionShuffler.ts`). | ⚠️ Ausencia de decaimiento temporal SRS ([Milestone 8](#milestone-8-motor-de-decaimiento-en-memoria-srs-mastery-challenge-12h-misconception-ledger-y-fluidez)). Degradación y calibración completadas en [Milestone 14](file:///d:/Augusto/personal_portfolio/Tops_academy/MILESTONES_COMPLETED.md#milestone-14-motor-de-maestría-integral-20-estilo-khan-academy-calibración-bidireccional-híbrido-8020-fluidez-y-motor-up-next); resta simulador adaptativo en 2 módulos ([Milestone 14-B](#milestone-14-b-simulador-cronometrado-adaptativo-de-examen-parcial-en-2-módulos-sat-bluebook)). |

---

## 2. Consolidación de Hitos de Modalidades y Plantillas (M5 + M20, Estabilidad de $k=2$ y Reforma de M19 hacia $k=4$)

Para alinear la ingeniería en torno al objetivo de **mayor exigencia cognitiva (Bloom superior sin descarte) + cero overfitting + sostenibilidad de cuota en Google AI Pro**, se han estructurado los siguientes ejes sobre el banco de problemas:

1. 🔗 **Fusión de Milestone 5 + Milestone 20 $\longrightarrow$ Milestone 20 (Core + 20-B Modo Hierro) + Estándar Estable $k=2$ ✅ Completado:**
   - **Milestone 20 Core (✅ Certificado el 2026-11-18 en [`MILESTONES_COMPLETED.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/MILESTONES_COMPLETED.md)):** Completó íntegramente bajo arquitectura estática de **GitHub Pages (\$0)** la reforma `TPL-D3` (`ds` en `FIB` y `open_symbolic`), autonomía del CTA ($2 \le M \le 4$ modalidades canónicas, **`DEFAULT_TEMPLATES_PER_MODALITY = 2` ($k=2$) como estándar estable en producción** y 4 candados anti-clon), cuota anti-descarte (`[M20-MC7-CAP]`: **`0 MC7` prohibido en `Skill` y $\le 1$ `MC7` en `Concept`/`Fact`**; `[M20-ACTIVE-QUOTA]`: $\ge 80\%$ activo), compiladores Shift-Left (`proof_compiler.py`, `adversarial_generator.py`), Smart `Blank-First` y las 6 modalidades de Bloom Superior (`open_symbolic` con `mathjs`, `proof_dag`, `adversarial_break`, `unstructured_model` Stage 0, `invariant_canvas` SVG cartesiano/árbol y `concept_matching`).
   - **Milestone 20-B — Modo Hierro (✅ Implementado y endurecido el 2026-11-21 en [`MILESTONES_COMPLETED.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/MILESTONES_COMPLETED.md)):** Arnés cronometrado con cuenta regresiva a libro cerrado (`IronExamSession.tsx`), retención total de feedback hasta entrega final y auditoría metacognitiva obligatoria (`MetacognitiveModal.tsx` + `ironExamGrading.ts`).
   - **Consolidación de $k=2$ como Estándar Estable y Piloto $k=3$ (✅ Auditado el 2026-11-21):**
     - **`k=2` (Estable por defecto en `engine/stage_contract.py`):** Validado en `solow_m20_v1..v3` y `mateco_4_optimizacion_v20` (`786` reactivos, `19.37/20.0`, `MPRI 97.42/100`, `14.72 min` normalizado, `14.6M` tokens brutos, `USD 11.41`). Queda congelado como configuración predeterminada estable para no saturar la cuota de tokens de Google AI Pro.
     - **Piloto `k=3` (`mateco_4_optimizacion_v20_k_3`):** Alcanzó calidad récord (`19.92/20.0`, `MPRI 99.65/100`, `risk_score = 0.05`, Bloom `3.931` Tier `ÉLITE`, `321` plantillas $\times 3$ semillas = `963` reactivos), pero evidenció que con una tasa de 1ra compilación de `9.52%` (`2/21` shards) los reintentos multiplican el caché leído entre `2.9x` y `7.6x` (`20.62M` tokens brutos, `USD 16.22`).
2. 🔗 **Reforma de Milestone 19 $\longrightarrow$ [Milestone 19: Escalamiento Sostenible a $k=4$ (`1,284+` Reactivos), Arquitectura *First-Pass* ($\ge 75\%$ 1ra Compilación) y Protección de Cuota Google AI Pro](#milestone-19-escalamiento-sostenible-a-k4-1284-reactivos-arquitectura-first-pass-75-1ra-compilación-y-protección-de-cuota-google-ai-pro):**
   - Define las **5 metas técnicas de compilación *First-Pass* y ahorro de tokens** necesarias para que **$k=4$ (`--templates-per-modality 4`, `428` plantillas, `1,284` reactivos)** pueda adoptarse en el futuro como nuevo estándar reduciendo el consumo de **`34.57M` tokens brutos (`USD 25.31` realista hoy)** a **`<= 11.55M` tokens brutos (`~USD 11.06–12.85`, `< 10 min`)**, es decir, **consumiendo un 44% menos de cuota que el $k=3$ actual**.

*(Nota: Los hitos **Milestone 9**, **Milestone 14-B** y **Milestone 21** se mantienen **desacoplados e independientes** en sus fichas respectivas).*

---

## 3. Matriz Maestra de Priorización de Ingeniería (Hitos Activos)

> *Nota: Los hitos completados y certificados (1, 1-T, 2, 2a, 3, 4, 6, 7, 9 [Quick Wins], 10, 11 [núcleo], 12, 13, 14, 15 [F1], 16 [F1] y **20 [Core + 20-B Modo Hierro con `k=2` Estable]**) viven en [`MILESTONES_COMPLETED.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/MILESTONES_COMPLETED.md).*

| Hito / Milestone | Área | Impacto Cognitivo, Formal y de Eficiencia | Esfuerzo | Estado / Prioridad | Especificación Técnica |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Milestone 19: Escalamiento Sostenible a $k=4$ (`1,284+` Reactivos), Arquitectura *First-Pass* ($\ge 75\%$) y Protección de Cuota Google AI Pro** | Pipeline C2C / Compilador | **Habilitar $k=4$ (`428` plantillas, `1,284` preg.) con menos tokens que $k=3$ hoy.** Manteniendo **`k=2` como estándar estable actual**, implementar las 5 metas *First-Pass* (auto-poda `[TPL-ORPHAN-VARS]`, helper `c2c_verify_equiv`, sweep completo en Stage 3B, semáforo `max_concurrency=12` y opción híbrida $k=3, s=4$) para bajar $k=4$ de `34.6M` a `<= 11.55M` tokens brutos (`~USD 11.06–12.85`). | 1.5 a 2.5 d | 🧬 **P1 — Futuro Estándar $k=4$ (*Quota-Safe*)** | [Spec 4 Ejes y Bloom](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/sintesis_plantillas_arquetipos.md) |
| **Milestone 15 (Fase 2): Kernel Nativo Perceus C Lean 4** | Pipeline / Formal Kernel | **Sobrecarga `< 0.5 ms` y verificación matemática nativa.** Compilar `TopsAcademyC2C.lean` a binario nativo C vía FFI, *Proof-Carrying Artifacts* (`*.cert.json`) y DRT estilo AWS Cedar. | 1.5 a 2.5 d | 🛡️ **P0 — En Roadmap** | [Spec Formal Lean 4](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m15_m18_formal_lean4.md) |
| **Milestone 16 (Fase 2): Deducción Simbólica Z3 / Lean 4** | Motor / Verificación | **Más calidad matemática con 0 Late-Catches.** Integración de solver SMT Z3 y lemas Lean 4 (`omega`/`ring`/`grind`) para `TPL_D4_Universal` y prueba de no-equivalencia AST entre arquetipos y sub-plantillas. | 1.5 a 2 d | 📐 **P0 — En Roadmap** | [Spec Formal Lean 4](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m15_m18_formal_lean4.md) |
| **Milestone 17: Certificación DAG y Arbitraje Bayesiano** | Curricular / Arbitraje | **Cero ciclos/huérfanos y dominancia $\alpha_{\text{Kernel}} = 0$.** Conectividad/aciclicidad en `cta_merge.py`; juez 1-seed pre-verificado; clausura epistémica de símbolos libres. | 1 a 1.5 d | 🧠 **P0 — En Progreso** | [Spec Formal Lean 4](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m15_m18_formal_lean4.md) |
| **Milestone 18: Arnés de Certificación Continua** | CI / Anti-Regresión | **Inmunidad permanente ante drift inter-etapa.** Schemas Pydantic inter-etapa (`interstage_schemas.py`), auto-compilación CI de prompts y auditoría `#print axioms` con nonce. | 1 a 1.5 d | 🔒 **P0 — En Progreso** | [Spec Formal Lean 4](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m15_m18_formal_lean4.md) |
| **Milestone 14-B: Simulador Adaptativo de Examen Parcial (SAT Bluebook)** | Motor Maestría / Frontend | **Enrutamiento dinámico en 2 módulos y reloj de examen.** Módulo 1 diagnóstico $\to$ Módulo 2 Estándar vs. Avanzado y temporizador con cuenta regresiva universitaria. | 1 d | ⏳ **P2 — Post-M14** | [Spec Khan Mastery](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m14_khan_mastery_engine.md) |
| **Milestone 9: Jerarquía PPT y ContentCore Khanmigo** | Curricular / Schema | **Alineación con material real y Unidad 0 PRE-XX.** Quick Wins completados (2026-11-14: anclaje PPT, `PRE-XX`, `ContentCoreDrawer`, `hierarchyAdapter`, backfill 8 cursos); resta Paso 4 (Quizzes Subtema 3–5, Challenge PPT 8–12 y `ContentCore` LLM nativo). | ~15 min *(Paso 4 remanente en Flash Duet)* | 🏛️ **P1 — Quick Wins Cerrados (Paso 4 Pendiente)** | [Spec Jerarquía PPT](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m09_hierarchical_content_khanmigo.md) |
| **Milestone 8: Motor SRS, Retención y Fluidez** | Motor de Sesión | **Retención longitudinal y metacognición del error.** Decaimiento Ebbinghaus, tarjeta *Mastery Challenge* 12h, Cuaderno de Trampas y curva de compresión de latencia. | 2 a 3 d | 🔁 **P2 — Ciclo de Pericia** | [Ficha M8](#milestone-8-motor-de-decaimiento-en-memoria-srs-mastery-challenge-12h-misconception-ledger-y-fluidez) |
| **Milestone 21: Bloques por Documento Fuente ("Núcleo & Glosario") respetando el orden pedagógico** | Curricular / Frontend | **Agrupamiento por tramos contiguos respetando el orden del JSON.** Fase A implementada (`modulesPreserveOrder`); pendiente Fase B (emisión de `modules` explícitos ordenados tras deduplicar competencias apuntes/diapositivas). | 0.5 a 1 d | 📦 **Backlog (Fase A Lista / Fase B Pendiente)** | [Ficha M21](#milestone-21-backlog-bloques-por-documento-fuente-núcleo--glosario-respetando-el-orden-pedagógico) |
| *Opcionales A, B y C (11b): Daemon RAM, Capacitor y Carga Instantánea* | Infra / Frontend | *Optimizaciones secundarias: pool en memoria RAM, empaquetado móvil nativo y apertura asíncrona de cursos pesados.* | 3 a 8 h | ⏳ **Backlog / Opcional** | [Módulos Opcionales](#módulos-opcionales-y-de-backlog-secundario) |

---

## 4. Fichas Ejecutivas de los Milestones Pendientes

> *Nota: El Milestone 20 completo (**Milestone 20 Core**, **Milestone 20-B: Modo Hierro** y la consolidación de **`k=2` (`DEFAULT_TEMPLATES_PER_MODALITY = 2`) como estándar estable de producción**) fue cerrado y trasladado a [`MILESTONES_COMPLETED.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/MILESTONES_COMPLETED.md#milestone-20-core--20-b-modo-hierro-arquitectura-epistémica-de-excelencia-6-modalidades-de-bloom-superior-reforma-anti-descarte-tpl-d3-smart-blank-first-y-modo-hierro-en-github-pages-0).*

<a id="milestone-19-no-urgente--backlog-de-expansión-escalamiento-proporcional-2x3x-del-banco-de-preguntas-sin-degradar-calidad-form-c"></a>
<a id="milestone-19-multiplicación-estructural-de-plantillas-por-arquetipo-k23-con-gemini-4-y-escalamiento-2x3x-anti-overfitting"></a>
<a id="milestone-19-escalamiento-sostenible-a-k4-1284-reactivos-arquitectura-first-pass-75-1ra-compilación-y-protección-de-cuota-google-ai-pro"></a>
### Milestone 19: Escalamiento Sostenible a $k=4$ (`1,284+` Reactivos), Arquitectura *First-Pass* ($\ge 75\%$ 1ra Compilación) y Protección de Cuota Google AI Pro
* **Estado:** 🧬 **P1 — Futuro Estándar $k=4$ bajo Arquitectura *First-Pass & Quota-Safe* (~1.5 a 2.5 d).**
  - **Estándar Estable Actual en Producción (`k=2`):** `DEFAULT_TEMPLATES_PER_MODALITY = 2` en [`engine/stage_contract.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/content-to-course/engine/stage_contract.py#L23-L32) queda **fijo como valor por defecto estable** (`mateco_4_optimizacion_v20`: `786` reactivos, `19.37/20.0`, `MPRI 97.42/100`, `14.72 min` normalizado, `14.6M` tokens brutos, `USD 11.41`).
  - **Piloto Empírico Certificado (`k=3`):** `mateco_4_optimizacion_v20_k_3` (`d65b2d48`, `27` competencias, `321` plantillas $\times 3$ semillas = `963` reactivos) certificó **`19.92/20.0` (`PLATINUM MASTERY`), `MPRI 99.65/100`, `risk_score = 0.05` y Bloom `3.931` (`Tier ÉLITE`)** en `23.45 min` (`20.62M` tokens brutos, `USD 16.22`).
* **Objetivo:** Alcanzar las condiciones de ingeniería en el compilador (`compile_shard.py`), el despachador de olas (`c2c_wave_workflow.py`) y el reparador (`dispatch-repair`) para que **$k=4$ (`--templates-per-modality 4`, `428` plantillas únicas, `1,284` reactivos)** pueda convertirse en el futuro estándar de la plataforma **sin agotar la cuota de tokens del plan Google AI Pro**, reduciendo el consumo por curso de **`34.57M` tokens brutos (`USD 25.31` realista hoy)** a **`<= 11.55M` tokens brutos (`<= 4.15M` activos, `~USD 11.06–12.85`, `< 10 min`)**.

#### 1. Diagnóstico Forense: Por Qué Cada Fallo de Compilación Multiplica por `3x–7.6x` el Consumo de Cuota
La telemetría empírica extraída de `mateco_4_optimizacion_v20_k_3` (`shard_timing_profile.json` + `telemetry.json`) sobre los shards de **1 competencia** demuestra que el costo real de escalar $k$ no proviene de escribir más plantillas en el primer turno, sino de los **reintentos post-1ra-compilación**:

| Intentos de Compilación (`compile_runs`) | Shards ($n$) | Turnos Prom. | Tiempo Pared (`Pre` / `Post`) | Tokens Input | Tokens Output | Tokens Activos | Tokens Caché Leídos | Costo Promedio / Shard (H2) | Multiplicador vs. 1ra Compilación |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`1` compilación (Clean-Room)** | `2` (`shard_09`, `03`) | **`4.5`** | **`106.0s`** (`87.5s` / `18.5s`) | `51,770` | `21,842` | **`73,612`** | **`116,810`** | **`USD 0.2502`** | **Baseline (`1.00x`)** |
| **`2` compilaciones (1 fallo)** | `7` | `8.1` | `182.1s` (`87.7s` / `94.4s`) | `76,585` | `38,425` | `115,010` | `336,308` | `USD 0.4283` | **`+71.2%` costo / `2.88x` caché** |
| **`3` compilaciones (2 fallos)** | `5` | `11.0` | `211.2s` (`89.6s` / `121.6s`) | `82,907` | `34,802` | `117,709` | `513,090` | `USD 0.4239` | **`+69.4%` costo / `4.39x` caché** |
| **`4` compilaciones (3 fallos)** | `1` (`shard_05`) | `15.0` | `368.0s` (`105.0s` / `263.0s`) | `99,869` | `50,030` | `149,899` | `890,012` | `USD 0.5918` | **`+136.5%` costo / `7.62x` caché** |
| **Shards de 2 comp. (`2–4` comp.)** | `6` (`shard_15..20`) | `11.7` | `272.8s` (`119.3s` / `153.5s`) | `110,158` | `55,908` | `166,066` | `775,177` | `USD 0.6427` | **`+156.9%` por shard (`6.64x` caché)** |

#### 2. Matriz Económica y de Cuota: Mundo *First-Pass* Ideal vs. Mundo Realista Hoy ($k=2, 3, 4$)
Estandarizado sobre el DAG canónico de `27` competencias atómicas y tarifas Gemini 4 Hydrogen (`USD 1.50/1M` In, `USD 7.50/1M` Out+Thinking, `USD 0.075/1M` Cache Read):

| Escenario | Plantillas / Reactivos | 1ra Compilación Stage 3 | Olas Rejudge | Tiempo Pared | Tokens Activos (In+Out) | Tokens Caché Leídos | **Tokens Brutos Totales** | **Costo Total (USD)** | **Costo / Preg.** | **Cursos por ~100M Cuota Bruta** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1. $k=2$ Estable Actual (Real Norm.)** | `214–262` / **`786`** | `0.0%` (`13` shards) | `1` ola + LQAS | `14.7 min` | `3.50M` | `11.10M` | **`14.60M`** | **`USD 11.41`** | `USD 0.0145` | `~6.8 cursos` |
| **2. $k=3$ Piloto Certificado (Real)** | `321` / **`963`** | `9.5%` (`2/21` shards) | `3` olas | `23.5 min` | `5.22M` | `15.40M` | **`20.62M`** | **`USD 16.22`** | `USD 0.0168` | `~4.8 cursos` |
| **3. $k=4$ Realista Hoy (Sin mejoras)** | `428` / **`1,284`** | `~3.5%` (`~3.0` comp/sh) | `3–4` olas | `~29.2 min` | `7.70M` | `26.87M` | **`34.57M`** | **`USD 25.31`** | `USD 0.0197` | `~2.9 cursos` ❌ |
| **4. $k=2$ Mundo *First-Pass* Ideal** | `214` / **`642–786`** | `100%` (`1.0` comp/sh) | `0` olas | `~6.2 min` | `2.39M` | `3.81M` | **`6.20M`** | **`USD 7.47`** | `USD 0.0095` | `~16.1 cursos` |
| **5. $k=3$ Mundo *First-Pass* Ideal** | `321` / **`963`** | `100%` (`1.0` comp/sh) | `0` olas | `~6.4 min` | `2.88M` | `4.66M` | **`7.54M`** | **`USD 8.90`** | `USD 0.0092` | `~13.3 cursos` |
| **6. $k=4$ Mundo *First-Pass* Ideal** | `428` / **`1,284`** | `100%` (`1.0` comp/sh) | `0` olas | `~6.8 min` | `3.42M` | `5.30M` | **`8.72M`** | **`USD 11.06`** | **`USD 0.0086`** | `~11.5 cursos` |
| **7. Meta M19: $k=4$ *Quota-Safe* (Metas 1–4)** | `428` / **`1,284`** | **`>= 75%` (`<= 1.3` c/sh)** | **`<= 1` ola** | **`~9.5 min`** | **`4.15M`** | **`7.40M`** | **`11.55M` (`-66.6%`)** | **`USD 12.85`** | **`USD 0.0100`** | **`~8.6 cursos`** ✅ |
| **8. Atajo Híbrido: $k=3, s=4$ + Metas 1–4** | `321` / **`1,284`** | **`>= 80%` (`<= 1.25` c/sh)** | **`<= 1` ola** | **`~8.2 min`** | **`3.45M`** | **`6.10M`** | **`9.55M` (`-72.4%`)** | **`USD 10.60`** | **`USD 0.0083`** | **`~10.5 cursos`** ✅ |

#### 3. Las 5 Metas Técnicas ("First-Pass & Quota-Safe Gates") para Promover $k=4$ sin Agotar Google AI Pro
1. **Meta 1 — Subir 1ra Compilación de Stage 3 de `9.5%` a `>= 75%` mediante Auto-Sanitización en `compile_shard.py` (`-13.5M` tokens / `-USD 8.50`):**
   - **Auto-poda de `[TPL-ORPHAN-VARS]` (`15/21` shards en `v20_k_3`):** Podar automáticamente en `compile_shard.py` las claves de `vars` no referenciadas en `@...@` (emitiendo `INFO` sin fallar la compilación) cuando todos los placeholders del reactivo estén resueltos.
   - **Preludio canónico `c2c_verify_equiv` para `[TPL-VERIFIER-UNSOUND]` (`14/21` shards):** Proveer en el entorno de `ver_fn` un verificador híbrido (simplificación simbólica `SymPy` + fallback numérico multi-punto en `3` semillas irracionales) que evite fallos de cancelación con flotantes/exponenciales (como `exp(-0.5*(3-t))` en `shard_05`) y evalúe siempre sobre strings ya interpolados.
   - **Normalización de `[TPL-STEM-VARIANT-PARITY]` (`13/21` shards) y Linter Pre-Vuelo de Coeficientes F-String (`-\d+\{[a-zA-Z_]`):** Detectar en Stage 3 concatenaciones accidentales tipo `-2{b}` (`-23` en vez de `-{2*b}`) antes de llegar a Blind Judges.
2. **Meta 2 — Particionamiento Estricto `1 Competencia = 1 Shard` con Semáforo `max_concurrency = 10–12` en `c2c_wave_workflow.py`:**
   - Evitar shards de `2–3` competencias (que en `v20_k_3` tardaron `+45.6%` y consumieron `775k` tokens de caché) y escalonar el despacho de los `27` shards en sub-olas de `10–12` agentes concurrentes para **erradicar los errores `429 RESOURCE_EXHAUSTED`** (que golpearon a `10/21` shards en el segundo `0` de `v20_k_3`).
3. **Meta 3 — Contrato *"Whole-Competency Sweep"* en Stage 3B (`dispatch-repair`) para Converger en `<= 1` Ola de Rejudge (`-2.5M` tokens):**
   - En `v20_k_3`, la competencia `C-02` requirió **3 olas secuenciales de Repair + Rejudge** porque la Ola 1 corrigió `T-C02-09` sin inspeccionar `T-C02-07`, `T-C02-08` ni `T-C02-06`. `dispatch-repair` exigirá auditar las $M \times k$ plantillas hermanas de la competencia fallida en una sola intervención.
4. **Meta 4 — Diagnósticos Ultra-Compactos en `compile_shard.py` (`<= 12` líneas por fallo, `-1.5M` tokens de caché):**
   - Comprimir la salida stdout de errores de compilación a 1 línea accionable por plantilla fallida para no inflar el contexto acumulado en los turnos siguientes.
5. **Meta 5 — Desacople entre $k$ (`--templates-per-modality`, Stage 3 LLM) y $s$ (`MIN_SEEDS_PER_TEMPLATE`, Stage 4 Python Local `0` Tokens):**
   - Parametrizar `--seeds-per-template s` en `run.py` y `engine/stage_contract.py` para permitir generar bancos de **`1,284` reactivos con $(k=3, s=4)$ a costo `0` de LLM adicional**, y habilitar $(k=4, s=3..4)$ una vez certificadas las Metas 1 a 4.

#### 4. Los 3 Candados Deterministas Anti-Clon en `compile_shard.py`
Cuando se opera con $k \ge 2$ plantillas por modalidad/arquetipo, `compile_shard.py` aplica tres pruebas automáticas para garantizar variedad estructural genuina:
1. **Candado 1 — Disyunción de Árbol Sintáctico Algebraico (AST / SymPy / Z3 intra-competencia):** Rechaza plantillas que produzcan árboles AST equivalentes o salidas colisionantes en semillas de control (`seed=100, 101`).
2. **Candado 2 — Disyunción de Tupla `(Modalidad, Nivel de Bloom)` y Progresión Cognitiva:** Empuja la distribución hacia `Analyze` y `Evaluate` (`>= 70%` en `Analyze+Evaluate`).
3. **Candado 3 — Distancia Léxica y de Escenario en `stem_variants`:** Índice de similitud Jaccard de n-gramas acotado ($\le 0.45$) entre plantillas de una misma competencia.

#### 5. Criterios de Aceptación (AC):
1. **AC-1 (`k=2` Estable por Defecto):** `DEFAULT_TEMPLATES_PER_MODALITY = 2` se mantiene como valor por defecto en `engine/stage_contract.py` y `run.py` hasta que las Metas 1–4 estén certificadas en CI.
2. **AC-2 (Auto-Sanitización y Helper `c2c_verify_equiv` en `compile_shard.py`):** Implementación de la Meta 1 (auto-poda de `[TPL-ORPHAN-VARS]`, `c2c_verify_equiv` y linter `-\d+\{[a-zA-Z_]`), elevando la tasa de 1ra compilación en corridas reales de `9.5%` a **`>= 75%`**.
3. **AC-3 (Control de Ráfagas y *Whole-Competency Sweep*):** `c2c_wave_workflow.py` soporta `max_concurrency = 12` (`0` errores `429`) y `dispatch-repair` converge en `<= 1` ola de Rejudge.
4. **AC-4 (Corrida Certificada $k=4$ *Quota-Safe*):** Corrida completa con `--templates-per-modality 4` (`>= 1,284` reactivos) completada en **`<= 12.0M` tokens brutos (`<= 4.2M` activos, `<= USD 13.00`, `< 11 min`)** y calificación QA `>= 19.8/20.0` (`MPRI >= 99.0`).
> 📄 **Especificación Técnica Completa y Síntesis de los 4 Ejes:** Consultar [`docs/specs/sintesis_plantillas_arquetipos.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/sintesis_plantillas_arquetipos.md).

---

### Milestone 15 (Fase 2): Kernel Nativo Perceus C Lean 4, FFI (`< 0.5 ms`) y DRT Industrial
* **Estado:** 🛡️ **P0 — En Roadmap.** *(Fase 1 Isomórfica en Python cerrada el 2026-11-08; ver [`MILESTONES_COMPLETED.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/MILESTONES_COMPLETED.md)).*
* **Objetivo:** Compilar `formal/TopsAcademyC2C.lean` a binario nativo C vía *Perceus Reference Counting* (FBIP) e invocarlo síncronamente vía FFI en `c2c_hook_guard.py` con sobrecarga $< 0.5\text{ ms}$, blindando el 100% de las herramientas.
* **Criterios de Aceptación:**
  1. Binario nativo exporta `@[export c2c_verify_transition_c]` invocado sin latencia de VM en subagentes.
  2. Emisión de *Proof-Carrying Artifacts* (`*.cert.json`) encadenando SHA-256 de transiciones válidas.
  3. Suite de *Differential Random Testing* (DRT) sobre 10,000 trazas aleatorias (`Hypothesis`) verificando paridad matemática entre Python y Lean 4.
> 📄 **Especificación Técnica Completa:** Consultar [`docs/specs/m15_m18_formal_lean4.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m15_m18_formal_lean4.md) para el detalle de los 6 teoremas constructivos y la interfaz FFI.

---

### Milestone 16 (Fase 2): Deducción Algebraica Automática con Z3 y Lemas Lean 4
* **Estado:** 📐 **P0 — En Roadmap.** *(Fase 1 Motor y Contratos Python cerrada el 2026-11-08; ver [`MILESTONES_COMPLETED.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/MILESTONES_COMPLETED.md)).*
* **Objetivo:** Demostración analítica universal de invariantes matemáticos directamente en Stage 3, cerrando cualquier brecha de Late-Catches en Stage 6 y respaldando formalmente el **Candado 1 de Milestone 19** (no-equivalencia algebraica entre los 4 arquetipos y entre las $K$ plantillas de un mismo arquetipo).
* **Criterios de Aceptación:**
  1. Integración de solver SMT Z3 en `compile_shard.py` para verificar `TPL_D4_Universal` (la respuesta correcta no colisiona con los distractores en todo el espacio paramétrico, tanto en `MC7` como en el mapa `ds` de `FIB`/`open_symbolic`).
  2. Demostración formal con tácticas Lean 4 (`omega`, `ring`, `grind`) y SymPy/Z3 de que las $4 \times K$ funciones generadoras de una competencia producen fórmulas algebraicas objetivo genuinamente no equivalentes en AST.
> 📄 **Especificación Técnica Completa:** Consultar [`docs/specs/m15_m18_formal_lean4.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m15_m18_formal_lean4.md) para los contratos SMT y lemas formales.

---

### Milestone 17: Certificación Formal del DAG Curricular, Clausura Epistémica y Arbitraje Neuro-Simbólico
* **Estado:** 🧠 **P0 — En Progreso.**
* **Objetivo:** Garantizar que el árbol curricular sea un DAG acíclico, conexo, epistémicamente cerrado y monótono ($K_t \subseteq K_{t+1}$), con arbitraje bicameral donde el kernel formal domine estrictamente ($\alpha_{\text{Kernel}} = 0$).
* **Criterios de Aceptación:**
  1. Certificación constructiva en Stage 1 (`cta_merge.py` y `--append`): ordenamiento topológico certificado, cero huérfanos y preservación de definiciones previas.
  2. Auditor de Clausura Epistémica de Símbolos Libres: verifica $S_{\text{sol}} \subseteq S_{\text{stem}} \cup S_{\text{std}}$, bloqueando enunciados incompletos (como `Hab-19` sin función de utilidad o `C-01`).
  3. Arbitraje bicameral: Cámara Formal ($\alpha_{\text{Kernel}} = 0$, veto absoluto en matemáticas) + Cámara Epistémica LLM (1 semilla pre-verificada por plantilla para auditar claridad verbal y no-giveaway).
> 📄 **Especificación Técnica Completa:** Consultar [`docs/specs/m15_m18_formal_lean4.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m15_m18_formal_lean4.md) para el protocolo de dominancia bayesiana.

---

### Milestone 18: Arnés de Certificación Continua, Anti-Drift de Contratos y Auditoría `#print axioms`
* **Estado:** 🔒 **P0 — En Progreso.**
* **Objetivo:** Erradicar de raíz desincronizaciones silenciosas entre etapas mediante contratos unificados tipados, auditoría de axiomas en CI y benchmark SLA "Golden Runs".
* **Criterios de Aceptación:**
  1. Contrato Único Tipado Inter-Etapa (`engine/interstage_schemas.py`): schemas Pydantic compartidos para todos los JSONs intermedios.
  2. Auditoría `#print axioms` con Nonce Criptográfico: rechazo duro de cualquier prueba que contenga `sorry`, `unsafe` o axiomas no autorizados.
  3. Compuerta CI de Auto-Compilación de Prompts (`test_system_prompts_compile_clean.py`): compila los bloques Python de los prompts contra las reglas vigentes.
  4. Benchmark SLA C2C v4.0: wall-time `< 12.0 min` ($\sigma_t < 90\text{ s}$), `< 12M tokens`, PASS Turno 1 $\ge 85\%$ y 0 Late-Catches en Stage 6.
> 📄 **Especificación Técnica Completa:** Consultar [`docs/specs/m15_m18_formal_lean4.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m15_m18_formal_lean4.md) para el arnés anti-drift y nonce CI.

---

### Milestone 14-B: Simulador Cronometrado Adaptativo de Examen Parcial en 2 Módulos (SAT Bluebook)
* **Estado:** ⏳ **P2 — Post-M14 (Roadmap Activo).** *(El núcleo de Milestone 14 —calibración bidireccional en Challenge/Test/Quiz, degradación estricta por fallo, barra híbrida 80/20, telemetría de fluidez por reactivo y motor 'Up Next for You' de 5 niveles— fue completado y certificado en [`MILESTONES_COMPLETED.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/MILESTONES_COMPLETED.md#milestone-14-motor-de-maestría-integral-20-estilo-khan-academy-calibración-bidireccional-híbrido-8020-fluidez-y-motor-up-next)).*
* **Objetivo:** Implementar la experiencia de simulador de examen parcial cronometrado adaptativo en dos etapas secuenciales (*Multistage Adaptive Testing* estilo SAT Bluebook / GRE) para evaluar la preparación de examen universitario con enrutamiento dinámico según el desempeño en el primer módulo.
* **Criterios de Aceptación:**
  1. **Enrutamiento Adaptativo en 2 Módulos:**
     - **Módulo 1 (Diagnóstico, 10–12 preguntas):** Muestreo equilibrado de todas las unidades del curso con dificultad heterogénea (ZPD media).
     - **Compuerta de Puntuación:** Al finalizar el Módulo 1, si el puntaje es $\ge 70\%$, el alumno es enrutado al **Módulo 2 Avanzado** (ZPD alta/experto); si es $< 70\%$, es enrutado al **Módulo 2 Estándar** (ZPD media/refuerzo).
  2. **Reloj de Examen Universitario y Condiciones de Prueba:**
     - Temporizador con cuenta regresiva global por módulo y advertencias visuales a los 5 minutos y 1 minuto.
     - Modalidad a libro cerrado opcional con deshabilitación de pistas y feedback diferido hasta el envío final del examen.
  3. **Diagnóstico Post-Examen y Proyección de Nota:**
     - Panel de resultados con desglose por unidad, tiempo medio por pregunta y proyección de calificación universitaria basada en la dificultad del módulo completado.
> 📄 **Especificación Técnica Completa:** Consultar [`docs/specs/m14_khan_mastery_engine.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m14_khan_mastery_engine.md) para el modelo de enrutamiento adaptativo de 2 etapas y diseño del temporizador.

---

### Milestone 9: Arquitectura Jerárquica de Contenido (PPT $\to$ Glosario, ContentCore Khanmigo en 5 Bloques y Unidad 0 `PRE-XX`)
* **Estado:** 🏛️ **P1 — Fase Quick Wins Completada y Certificada (2026-11-14); Paso 4 End-to-End Pendiente.** *(Quick Wins implementados en `main` bajo Flash Duet Paralelo: ver [`MILESTONES_COMPLETED.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/MILESTONES_COMPLETED.md#milestone-9-fase-quick-wins-jerarquía-ppt-unidad-0-pre-xx-contentcoredrawer-y-backfill)).*
* **Objetivo:** Erradicar la fragmentación plana. Reorganizar la plataforma y el pipeline en 3 niveles anclados a las PPT reales, precedidos por la **Unidad 0 (*Get Ready*)**:
  $$\text{Unidad 0 (PRE-XX)} \longrightarrow \text{Contenido PPT (Módulo)} \longrightarrow \text{Familia de Subtemas} \longrightarrow \text{Competencias (4 Arquetipos)}$$
* **Completado en Quick Wins (2026-11-14):**
  1. ✅ **Anclaje PPT y Propagación (`run.py`, `cta.schema.json`, `schema_validator.py`):** Exportación de `evidence`, `session`, `unit_index`, `assumptions` y `source_examples` hacia `courses/<course_id>.json`.
  2. ✅ **Unidad 0 `PRE-XX` (`compile_cta.py`, `cta_merge.py`, `prompt_cta_architect.md`, `MasteryGrid.tsx`, `Sidebar.tsx`):** Soporte integral del prefijo `PRE-XX` / `is_prerequisite` al inicio del currículum con badges visuales.
  3. ✅ **`ContentCoreDrawer.tsx` + `hierarchyAdapter.ts` + Backfill:** Visor ergonómico Split 50% de 5 bloques Khanmigo, `ExplicitAssumption` y Glosario LaTeX, hidratación de 8 cursos (237 competencias) vía `scripts/backfill_m9_hierarchy.py` y fix de invalidación `ETag` en `courseLoader.ts`.
* **Criterios de Aceptación Remanentes (Paso 4 End-to-End):**
  1. Emisión nativa LLM de `modules[]` y `ContentCore` por PPT en `compile_cta.py` y `prompt_cta_harmonizer.md`.
  2. Quizzes formativos por subtema (`SubtopicUnit`, 3–5 preguntas) y Challenges integradores por PPT (8–12 preguntas) en `App.tsx` + `masteryStorage.ts`.
> 📄 **Especificación Técnica Completa:** Consultar [`docs/specs/m09_hierarchical_content_khanmigo.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/m09_hierarchical_content_khanmigo.md) para las interfaces TypeScript, esquemas JSON, comparativa Gemini 4 Hydrogen vs. 3.8 Flash, blast radius y desglose incremental.

---

### Milestone 8: Motor de Decaimiento en Memoria (SRS), *Mastery Challenge* (12h), *Misconception Ledger* y Fluidez
* **Estado:** 🔁 **P2 — Cierre de Ciclo de Pericia (~2 a 3 d).**
* **Objetivo:** Resolver la paradoja de retención entrenando el clasificador perceptual a largo plazo mediante repetición espaciada y metacognición del error.
* **Criterios de Aceptación:**
  1. Modelo de decaimiento temporal Ebbinghaus en `masteryStorage.ts` (degradación a los 14 y 45 días sin práctica).
  2. Tarjeta *Mastery Challenge* de 6 preguntas con cooldown de 12 horas (única vía para ascender de `Proficient` a `Mastered`).
  3. Cuaderno Personal de Trampas (*Misconception Ledger*): persistencia de errores frecuentes y sesión "Practicar mis Trampas".
  4. Bitácora de Fluidez (`ProgressLogView.tsx`): curva de compresión de latencia (paso de Sistema 2 lento a Sistema 1 fluido).

---

### Milestone 21 (Backlog): Bloques por Documento Fuente ("Núcleo & Glosario") respetando el orden pedagógico
* **Estado:** Fase A implementada: bloques = tramos contiguos del orden del JSON (nuevo bloque al cambiar `evidence[0].doc`) con guarda `modulesPreserveOrder` (si la concatenación no reproduce el JSON, se muestra lista plana). Pendiente Fase B.
* **Motivo:** El agrupamiento automático por `evidence[0].doc` movía todas las unidades de un PDF al primer bloque, rompiendo el orden pedagógico de `course.competencies` (ej. PDF 02 con 22 unidades antes que PDF 01) y haciendo que los Unit Tests mezclaran temas aún no vistos.
* **Regla inviolable:** el orden del JSON manda siempre; la numeración de unidades es la posición en `competencies` (no `unit_index`, que es página del PDF).
* **Propuesta:** agrupar solo por *tramos contiguos* del mismo documento (el JSON actual daría 5 bloques: 02→3, 01→14, 02→19, 03→10, 04→8), o que el CTA emita `modules` explícitos ya ordenados. Reactivar con test que verifique que la concatenación de los módulos reproduce exactamente el orden del JSON.
* **Fase B (destino):** que el CTA/`compile_cta.py` emita `modules` temáticos explícitos (título + ids en orden) validados en `publish` con la misma regla de orden. Requiere antes fusionar competencias duplicadas apuntes/diapositivas (ver QA report), pues hoy los temas se recorren dos veces (unidades 4–17 y 18–36).

---

### Módulos Opcionales y de Backlog Secundario
- **Opcional A: Pipeline Performance Daemon en RAM / SSD:** Pool persistente en memoria para eliminar I/O de disco.
- **Opcional B: Empaquetado Nativo con Capacitor:** Wrapper binario para publicación en Google Play / App Store (la PWA actual ya cubre el 95% de casos offline).
- **Opcional C (Milestone 11b): Apertura Instantánea de Cursos Pesados:** Elimina micro-bloqueos en laptops de gama media al abrir cursos de más de 14 MB (desacoplar `await saveToIndexedDB` en `courseLoader.ts` hacia ejecución en segundo plano *fire-and-forget*, pausar la cola de prefetch mientras el usuario interactúa con la práctica, instrumentar marcas con `performance.mark` y code-splitting con `React.lazy` para `PracticeSession`, `CompletionScreen` y `CourseChallenge`). Estado: ⏳ *P3 — Optimización UX / Backlog Opcional (~0.5 a 1 d)*.
- **Opcional D (Endurecimiento M20): Piso Mínimo `steps >= 3` en `proof_dag` y `adversarial_break` (`find_fallacy`):** Elevar el mínimo actual de `2` a **`>= 3` pasos** (ideal `3..5`) en `engine/proof_compiler.py` (`L180`: `valid_steps >= 3`), `engine/adversarial_generator.py` (`L226`: `len(raw_steps) >= 3`) y `engine/invariants.py` (`L1378`), evitando casos triviales de 2 permutaciones o 50/50 (1 correcto vs. 1 falacia) y actualizando los fixtures mínimos / ejemplo `gen_pd` de `prompt_shard_author.md`. Estado: ⏳ *Backlog / Mejora de Rigor (~2 h)*.

---

## 5. Gobernanza y Reglas de Workspace

1. **Regla Universal Sincronizada (`.agents/rules/c2c-quality-invariants.md`):**
   - 4 arquetipos obligatorios (`min_archetypes: 4`) con **`DEFAULT_TEMPLATES_PER_MODALITY = 2` ($k=2$) como estándar estable en producción**, escalable en Milestone 19 a $k = 4$ (`--templates-per-modality 4`, `1,284+` reactivos) tras cumplir las 5 metas *First-Pass & Quota-Safe* ($\ge 75\%$ 1ra compilación y $\le 11.55\text{M}$ tokens brutos).
   - Reforma `TPL-D3`: captura de distractores diagnósticos en modalidades de evocación libre (`FIB`, `open_symbolic`) para minimizar el uso de `MC7`.
   - Triple contrato de verificadores `ver_*`: `soundness` positiva, refutación estricta de distractores (`ver_fn(d_i) is False`) y veto a `try/except: return True`.
   - Cero bucles ad-hoc `_clean_ds`, cero metainformación visible en opciones y pistas socráticas en 3–5 niveles libres de respuestas anticipadas.
2. **Consolidación de System Prompts Lean v4.0 y Compuertas A/B 2.0 (`.agents/skills/content-to-course/system_prompts/lean/`):** ✅ *IMPLEMENTADA*
   - Ejemplos canónicos en `Form-C` validados y consolidados; `--lean` fijado por defecto en `dispatch.py` para todos los roles; flags `--fail-total` e inyección de `assumptions` operativas.

---

## 6. Plan de Acción de Ingeniería en 4 Fases (Cronograma Maestro)

| Fase | Horizonte | Entregables Clave ("Más Exigencia Cognitiva y Menos Overfitting con Menos Tokens") | Estado |
| :--- | :---: | :--- | :---: |
| **Fase 1: Corrección de Bugs Silenciosos, Endurecimiento Isomórfico y Recorte de Tokens/Tiempo** | **Día 1 – 2** | Fix `np.bool_`, refutación estricta `ver_*`, Matriz 2D `decidirEstrategiaEdicion`, deduplicación `-2M` tokens en `dispatch.py`, recibos SHA-256 (`< 5 ms`), precheck AST `< 50 ms` y suite global de 1,404 tests en 27.76s. *(Milestones 7, 15-P1, 16-P1, 18-P1)* | ✅ **CERRADA** |
| **Fase 2: Arquitectura *First-Pass* ($\ge 75\%$), Escalamiento Sostenible a $k=4$ (*Quota-Safe*) y Shift-Left Simbólico** | **Día 3 – 5** | ✅ **`k=2` consolidado como estándar estable** (`DEFAULT_TEMPLATES_PER_MODALITY = 2`) y piloto $k=3$ certificado (`19.92/20`, `MPRI 99.65`); **En Curso (M19):** las 5 metas *First-Pass* (auto-poda `[TPL-ORPHAN-VARS]`, `c2c_verify_equiv`, sweep completo en Stage 3B, semáforo `max_concurrency=12` y desacople $k$ vs. $s$) para habilitar $k=4$ (`1,284` preg.) en `<= 11.55M` tokens brutos, junto con solver SMT Z3 y Juez Epistémico 1-Seed ($\alpha_{\text{Kernel}} = 0$). *(Milestones 19, 16-P2, 17)* | 🛠️ **EN CURSO** *(M20 + `k=2` ✅)* |
| **Fase 3: Modalidades de Bloom Superior en GitHub Pages ($0) y Toolchain Formal Lean 4 (`< 0.5 ms`)** | **Día 6 – 9** | ✅ **M20 UI + Modo Hierro completados** (`open_symbolic`, `ProofDAG.tsx`, `AdversarialArena.tsx`, `Stage0Modeler.tsx`, `InvariantCanvas.tsx`, `ConceptMatching.tsx`, `IronExamSession.tsx`, `MetacognitiveModal.tsx`); **Pendiente:** binario nativo Perceus C de `TopsAcademyC2C.lean` (`< 0.5 ms`) y arnés `#print axioms`. *(Milestones 15-P2, 18)* | 🚀 **ROADMAP P0** *(M20 ✅)* |
| **Fase 4: Plataforma Khan Academy 2.0, ContentCore Khanmigo y Retención Longitudinal SRS** | **Semana 2** | Paso 4 de Jerarquía PPT + `ContentCore` (Milestone 9), Simulador Adaptativo de Examen Parcial en 2 Módulos SAT Bluebook (Milestone 14-B), motor de decaimiento Ebbinghaus SRS, *Mastery Challenge* 12h y *Misconception Ledger* (Milestone 8), y Fase B de bloques por documento fuente (Milestone 21). *(Milestones 9, 14-B, 8, 21)* | 🎯 **ROADMAP** |

---

## 7. Índice Canónico de Investigaciones y Archivos de Soporte

Los estudios técnicos, diagnósticos forenses y análisis comparativos que fundamentan esta hoja de ruta:
- 📄 [`docs/investigaciones/01_Solucion_al_conflicto_KaTeX_y_Python_en_LLMs.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/investigaciones/01_Solucion_al_conflicto_KaTeX_y_Python_en_LLMs.md): Desacoplamiento PrairieLearn.
- 📄 [`docs/investigaciones/02_Separacion_KaTeX_y_Python_LLM.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/investigaciones/02_Separacion_KaTeX_y_Python_LLM.md): Tokens ortogonales `@PARAM@` y QuickJS.
- 📄 [`docs/investigaciones/03_Limitaciones_de_la_plataforma_de_estudio.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/investigaciones/03_Limitaciones_de_la_plataforma_de_estudio.md): Análisis de los puntos ciegos cognitivos del paradigma cerrado.
- 📄 [`docs/investigaciones/04_Limites_de_la_plataforma_y_estudio.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/investigaciones/04_Limites_de_la_plataforma_y_estudio.md): Especificación psicométrica hacia *Deep Mastery*.
- 📄 [`reports/c2c_audits/historical_benchmark.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/historical_benchmark.md): Historial de 43 corridas del pipeline C2C.
- 📄 [`reports/c2c_audits/reporte_problemas_reparacion_c2c.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/c2c_audits/reporte_problemas_reparacion_c2c.md): Diagnóstico forense de subagentes reparadores y stragglers.
- 📄 [`docs/investigaciones/external_analysis/`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/investigaciones/external_analysis/): Serie de 4 diagnósticos forenses sobre cuellos de botella sintácticos.

### 7.1. Auditorías Pendientes de Análisis en Modo Agéntico
Se requiere ejecutar y analizar en modo agéntico la auditoría forense de rendimiento y calidad unificada (vía skills `c2c-run-auditor` y `c2c-unified-auditor`) para las siguientes sesiones de orquestación registradas:
- ⏳ [Content to Course MapReduce Generation](conversation://66915882-b7f8-441f-9fc7-d4a964050a42) (`saul_pc_sistemas_de_ecuaciones_vmapreduce5`).
- ⏳ [Solow Model Course Generation](conversation://3981c7eb-7122-4ba2-9615-2418a55bf657) (`solow_new_pipeline_direct`).
- ⏳ [Solow Model Course Creation](conversation://539b37fa-3efe-4464-a86d-0ec0a8f8130b) (`solow_new_pipeline_mapreduce`).

---
*Documento canónico y ejecutivo de hoja de ruta. Cualquier cambio en contratos o alcance técnico debe sincronizarse de forma bidireccional con su espejo en [`docs/future_milestones/FUTURE_MILESTONES.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/future_milestones/FUTURE_MILESTONES.md), los archivos en [`docs/specs/`](file:///d:/Augusto/personal_portfolio/Tops_academy/docs/specs/) y [`CONOCIMIENTO_TRIBAL.md`](file:///d:/Augusto/personal_portfolio/Tops_academy/CONOCIMIENTO_TRIBAL.md).*
