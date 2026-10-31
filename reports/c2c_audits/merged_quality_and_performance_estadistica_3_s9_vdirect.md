# Reporte Unificado de Auditoría Determinista: Calidad Estática y Telemetría Multi-Agente
## Curso: Estadistica 3 S9 Vdirect (`estadistica_3_s9_vdirect`)
### Plataforma Top's Academy — Pipeline Content-to-Course (C2C) v3.2

---

**Fecha de Consolidación:** 31 de Octubre de 2026  
**Identificador del Curso:** `estadistica_3_s9_vdirect`  
**Conversación Orquestadora Auditada:** [`592de77b-afd9-4fae-8744-4ef0be7212f4`](conversation://592de77b-afd9-4fae-8744-4ef0be7212f4)  
**Calificación QM-OSCQR / Risk Score:** **6.0 / 20.0 (CRÍTICO (0.0 - 10.9 pts) — RECHAZADO PARA ESTUDIO AUTÓNOMO)**  
**Mastery Path Readiness Index (`MPRI`):** **`35.94 / 100.0` (MASTERY-HOSTILE (0-39): Sabotaje Cognitivo / Colapso de Andamiaje Adaptativo)**  
**Tiempo de Pared Global:** **28.72 minutos** | **Cómputo Total de Agentes:** **131.42 minutos** | **Speedup:** **4.58x**  

---

## Tabla de Contenidos

- [PARTE I: TELEMETRÍA ESTÁTICA Y LINTERS DE CALIDAD (`StandardizedAuditEngine`)](#parte-i-telemetría-estática-y-linters-de-calidad-standardizedauditengine)
  - [1. Resumen Consolidado de Linters Deterministas](#1-resumen-consolidado-de-linters-deterministas)
  - [2. Resultados por Linter y Dimensión](#2-resultados-por-linter-y-dimensión)
  - [3. Clusters de Riesgo e Incidencias Detectadas](#3-clusters-de-riesgo-e-incidencias-detectadas)
  - [4. Muestra de Control Estratificada](#4-muestra-de-control-estratificada)
  - [5. Reglas de Linting Registradas (`discovered_lint_rules`)](#5-reglas-de-linting-registradas-discovered_lint_rules)
- [PARTE II: AUDITORÍA FORENSE DE RENDIMIENTO Y TELEMETRÍA (RUN AUDITOR)](#parte-ii-auditoría-forense-de-rendimiento-y-telemetría-run-auditor)
  - [6. Consolidación de Métricas de Rendimiento y Ratios Unitarios](#6-consolidación-de-métricas-de-rendimiento-y-ratios-unitarios)
  - [7. Distribución Empírica del Tiempo: Inferencia LLM vs. Ejecución de Herramientas](#7-distribución-empírica-del-tiempo-inferencia-llm-vs-ejecución-de-herramientas)
  - [8. Métricas Deterministas de Latencia por Etapa](#8-métricas-deterministas-de-latencia-por-etapa)
  - [9. Taxonomía Consolidada de Errores y Retrabajo](#9-taxonomía-consolidada-de-errores-y-retrabajo)
  - [10. Paquete Forense Agéntico Completo (Argon QA + Clúster Flash)](#10-paquete-forense-agéntico-completo-argon-qa--clúster-flash)

---

# PARTE I: TELEMETRÍA ESTÁTICA Y LINTERS DE CALIDAD (`StandardizedAuditEngine`)

## 1. Resumen Consolidado de Linters Deterministas

| Métrica Determinista | Valor Medido | Detalle Técnico |
| :--- | :--- | :--- |
| **Total de Competencias** | **27** | Distribución: Fact: 10, Concept: 9, Skill: 8 |
| **Banco Total de Reactivos** | **620 preguntas** | Rango por comp.: 20..30 |
| **Competencias Subpobladas (< 3 preg.)** | **0** | Nodos raíz sin prerrequisitos: 1 |
| **Preguntas Huérfanas** | **0** | Reactivos sin `competency_id` válido |
| **Cobertura de Rationales de Error** | **100.0%** | 3720 / 3720 distractores con `error_rationale` |
| **Distractores Delatores (Telltale)** | **0 items** | Confesiones de error en texto visible |
| **Andamiaje Socrático (Hints)** | **0 sin pistas** | 0 reactivos con `< 3` pistas; 0 sin solución |
| **Incidencias de Sintaxis KaTeX** | **0 incidencias** | Llaves sin cerrar: 0, `$` impares: 0, `$$$`: 0 |
| **Residuos de Código / F-strings** | **0 incidencias** | F-strings: 0, Vars plantilla: 0, `{{}}`: 0 |
| **Sustituciones Ciegas bajo Operador** | **0 incidencias** | Patrón `\dot{num}` / `\ddot{num}` |
| **Penalizaciones Duras Precalculadas** | **-2.5 puntos** | 2 reglas de deducción activadas |
| **Risk Score Global (0.0 - 100.0)** | **100.0** | 1417 issues totales detectados por linters |
| **Mastery Path Readiness (`MPRI`)** | **`35.94 / 100.0`** | MASTERY-HOSTILE (0-39): Sabotaje Cognitivo / Colapso de Andamiaje Adaptativo |

---

## 1B. Auditoría de Camino al Dominio (`Path-to-Mastery v2.0` — 6 Pilares Cognitivos)

| Pilar de Dominio del Estudiante | Puntaje MPRI | Máximo | Diagnóstico Empírico Determinista |
| :--- | :---: | :---: | :--- |
| **1. Progresión Adaptativa ZPD y Bloom** | **0.0** | 20.0 | Competencias con ZPD colapsado (1 sola banda): `27/27`; Habilidades en Bloom `Apply+`: `0.0%` |
| **2. Modalidad de Evocación y Anti-Gaming** | **3.55** | 20.0 | `MC7=100.0%`, `FIB=0.0%`, `MS=0.0%`; Comps memorizables: `2`; Cuantif. vacuos: `0`; Relleno `[R-15]`: `35` |
| **3. Integridad del Salvavidas Socrático (3-Strikes)** | **6.23** | 25.0 | Pistas genuinas: `0.0%`; Boilerplate Mad-Libs: `100.0%`; Pistas envenenadas: `280` (`45.16%`) |
| **4. Alineación Diagnóstica en `FeedbackToast`** | **10.61** | 15.0 | Unicidad global de `error_rationale`: `5.65%` (`210/3720`); Distractores `1.333x` arbitrarios: `5` |
| **5. Topología DAG e Interleaving (Quiz/Test)** | **10.0** | 10.0 | Ciclos: `False`, Profundidad DAG: `4`, Aristas invertidas: `0`, Islas: `0` |
| **6. Ergonomía Cognitiva y Pureza de Encuadre** | **5.55** | 10.0 | Prosa en `\text{...}`: `80`, Vars crudas `$theta_hat$`: `60`, Prefijos Solow/EDP ajenos: `60` |

---

## 2. Resultados por Linter y Dimensión

| Dimensión de la Rúbrica | Puntaje Obtenido | Máximo Posible | Observación Registrada |
| :--- | :---: | :---: | :--- |
| **Dimensión 1: Arquitectura y Granularidad** | **2.5** | 4.0 | Topologia DAG estructuralmente limpia (0 ciclos, profundidad 4, 0 islas, 27 competencias con 20-30 items), pero colapso total del ZPD adaptativo (620/620 reactivos hardcodeados en difficulty='medium', 27/27 competencias muertas en calibrateByMasteryDifficulty) y omision curricular de nodos propios para LGN Debil/Fuerte, Convergencia Casi Segura y Teorema de Slutsky. |
| **Dimensión 2: Calidad de Evaluación y Reactivos** | **1.9** | 5.0 | Tope Critico activado: monocultivo pasivo 100% MC7 (0% FIB y 0% MS en los 240 reactivos de Habilidad [Hab]), exploit de memorizacion visual de 1 unica respuesta invariante en 20 items de H-03 y H-04, distractores generados con multiplicadores porcentuales arbitrarios (1.5x, 0.75x, 1.15x, 0.93x en Q-C03-246, Q-H10-181, Q-H10-183) y coletillas burocraticas [R-15] asimetricas o tartamudeadas en Q-Hab01-381, Q-Hab02-412 y Q-Hab05-501. |
| **Dimensión 3: Andamiaje y Feedback Progresivo** | **1.0** | 5.0 | Tope Critico severo (0.8-1.5): sabotaje sistematico del salvavidas de 3 strikes en PracticeSession.tsx. El 100% (620/620) usa plantillas Mad-Libs vacias en Pista 1 e inyecta el error conceptual D-01 en Pista 2 bajo 'asegurando considerar adecuadamente: [misconception]' (280/620 capturados por regex literal y 620/620 confirmados semanticamente). En FeedbackToast.tsx, 94.35% de error_rationale son reciclados (210/3720 unicos), con desconexiones escalares vs matrices k x k (Q-Hab01-381) y eco literal de formulas falsas sin refutacion (Q-H04-061, Q-C01-201). |
| **Dimensión 4: Alineación Instruccional** | **2.2** | 4.0 | Aunque las derivaciones matematicas en detailed_solution son exactas (54/54 acuerdos en el Juez Ciego Etapa 5, muestreo 8.71%), compile_shard.py aplano el 100% (620/620) a bloom_taxonomy_level='Understand' (0.0% Apply/Analyze/Evaluate en 240 items Hab), inyecto 60 prefijos roboticos de crecimiento de Solow y EDP ('condiciones de frontera', 'ecuaciones fundamentales del regimen') y salto de Unidad 27 a Unidad 42 omitiendo LGN y Slutsky. |
| **Dimensión 5: Accesibilidad y Ergonomía Técnica / KaTeX** | **0.9** | 2.0 | Cero llaves rotas o signos $ desbalanceados, pero 80 reactivos (12.9%) envuelven oraciones completas en prosa dentro de $\text{...}$ provocando desborde horizontal movil (Q-C06-301, Q-C09-361), 60 reactivos (9.7%) filtran variables crudas de codigo en pistas ($theta_hat$, $Y_bar$, $sigma^2$, g'(theta), op(1) en Q-Hab01-395, Q-Hab03-441, Q-Hab08-606) y el titulo permanece como slug crudo ('Estadistica 3 S9 Vdirect'). |
| **Total Consolidado** | **6.0** | **20.0** | **CRÍTICO (0.0 - 10.9 pts) — RECHAZADO PARA ESTUDIO AUTÓNOMO** |

---

## 3. Clusters de Riesgo e Incidencias Detectadas

| Cluster de Riesgo | Ítems Afectados | Muestra de IDs |
| :--- | :---: | :--- |
| **`katex_issues`** | **230** | `Q-H01-006`, `Q-H01-007`, `Q-H01-008`, `Q-H01-009`, `Q-H01-010`, `Q-H01-016`, `Q-H01-017`, `Q-H01-018` |
| **`telltale_distractors`** | **0** | — |
| **`fstring_residues`** | **0** | — |
| **`scaffolding_flaws`** | **620** | `Q-H01-001`, `Q-H01-002`, `Q-H01-003`, `Q-H01-004`, `Q-H01-005`, `Q-H01-006`, `Q-H01-007`, `Q-H01-008` |
| **`template_residues`** | **0** | — |
| **`blind_replacements`** | **0** | — |
| **`cloned_distractors`** | **0** | — |
| **`archetype_monotony`** | **0** | — |
| **`poisoned_hints`** | **280** | `Q-H03-041`, `Q-H03-042`, `Q-H03-043`, `Q-H03-044`, `Q-H03-045`, `Q-H03-046`, `Q-H03-047`, `Q-H03-048` |
| **`boilerplate_hints`** | **340** | `Q-H01-001`, `Q-H01-002`, `Q-H01-003`, `Q-H01-004`, `Q-H01-005`, `Q-H01-006`, `Q-H01-007`, `Q-H01-008` |
| **`magic_multiplier_distractors`** | **6** | `Q-C01-202`, `Q-C03-246`, `Q-C07-322`, `Q-C07-330`, `Q-Hab01-395`, `Q-H01-001` |
| **`memorizable_answers`** | **2** | `Q-H03-041`, `Q-H04-061` |
| **`length_padded_options`** | **35** | `Q-C04-267`, `Q-C04-279`, `Q-C06-307`, `Q-C06-315`, `Q-C07-332`, `Q-C07-337`, `Q-C07-340`, `Q-C09-373` |
| **`cross_domain_prefixes`** | **60** | `Q-H01-011`, `Q-H01-013`, `Q-H02-021`, `Q-H02-038`, `Q-H02-040`, `Q-H03-042`, `Q-H03-045`, `Q-H04-062` |
| **`vacuous_quantifiers`** | **0** | — |
| **`katex_ergonomics`** | **140** | `Q-C01-201`, `Q-C01-202`, `Q-C01-203`, `Q-C01-204`, `Q-C01-205`, `Q-C01-206`, `Q-C01-207`, `Q-C01-208` |

---

## 4. Muestra de Control Estratificada

Ítems extraídos determinísticamente por competencia (`prepare_course_payload.py`):

1. **`Q-H01-001` (Muestra Aleatoria Simple e Independencia Idénticamente Distribuida | `multiple_choice_7_options` | `hints=3`):** `Analice la formulación operativa y deduzca: Sea una muestra aleatoria simple de tamaño $n = 43$ observaciones $\{Y_1, \d...`
2. **`Q-H01-002` (Muestra Aleatoria Simple e Independencia Idénticamente Distribuida | `multiple_choice_7_options` | `hints=3`):** `Verifique la consistencia del modelo y obtenga: Sea una muestra aleatoria simple de tamaño $n = 21$ observaciones $\{Y_1...`
3. **`Q-H02-021` (Definición Formal de Sesgo e Insesgadez Exacta | `multiple_choice_7_options` | `hints=3`):** `Al examinar detenidamente las condiciones de frontera, resuelva: Sea $\hat{\theta}_{26}$ un estimador puntual del paráme...`
4. **`Q-H02-022` (Definición Formal de Sesgo e Insesgadez Exacta | `multiple_choice_7_options` | `hints=3`):** `Con arreglo a las definiciones operativas del sistema, verifique: Sea $\hat{\theta}_{37}$ un estimador puntual del parám...`
5. **`Q-H03-041` (Definición Formal del Error Cuadrático Medio Escalar y Matricial | `multiple_choice_7_options` | `hints=3`):** `Realizando las deducciones matemáticas pertinentes, calcule: Considere un estimador puntual $\hat{\theta}_n$ basado en u...`
6. **`Q-H03-042` (Definición Formal del Error Cuadrático Medio Escalar y Matricial | `multiple_choice_7_options` | `hints=3`):** `Teniendo en consideración los fundamentos del equilibrio, determine: Considere un estimador puntual $\hat{\theta}_n$ bas...`
7. **`Q-H04-061` (Definición Formal de Convergencia en Probabilidad y Consistencia Débil | `multiple_choice_7_options` | `hints=3`):** `A partir del marco de análisis cuantitativo, encuentre: Sea $\{X_n\}$ una sucesión de variables aleatorias y $c$ una con...`
8. **`Q-H04-062` (Definición Formal de Convergencia en Probabilidad y Consistencia Débil | `multiple_choice_7_options` | `hints=3`):** `Considerando las ecuaciones fundamentales del régimen, obtenga: Sea $\{X_n\}$ una sucesión de variables aleatorias y $c$...`
9. **`Q-H05-081` (Definición de Convergencia en Media r-ésima y Media Cuadrática | `multiple_choice_7_options` | `hints=3`):** `Bajo los parámetros establecidos, calcule el valor exacto: Para una sucesión de variables $\{X_n\}$ con $\mathbb{E}[|X_n...`
10. **`Q-H05-082` (Definición de Convergencia en Media r-ésima y Media Cuadrática | `multiple_choice_7_options` | `hints=3`):** `Examine con detenimiento la situación y resuelva: Para una sucesión de variables $\{X_n\}$ con $\mathbb{E}[|X_n - X|^{3}...`

---

## 5. Reglas de Linting Registradas (`discovered_lint_rules`)

* **ID de Regla:** `symbolic_latex_anti_socratic_hint_poisoning`
* **Severidad:** critical
* **Patrón Regex:** `(?:asegurando considerar adecuadamente|evalúe posibles desvíos al considerar):\s*\$`
* **Descripción:** Detecta pistas anti-socráticas donde compile_shard.py inyecta directamente una fórmula simbólica falsa (D-01.misconception o D-02.misconception en LaTeX) precedida por una instrucción afirmativa, cubriendo los 340 reactivos adicionales que escapan al matcher literal cuando las opciones instancian valores numéricos.
* **Ítems Evidencia:** Q-H01-001, Q-H08-156, Q-H10-181, Q-C06-301, Q-C07-321

* **ID de Regla:** `echoed_misconception_error_rationale`
* **Severidad:** critical
* **Patrón Regex:** `^\$(?:\\text\{[^$]{15,}\}|\|X_n\(\\omega\)\s*-\s*c\|\s*<\s*\\varepsilon.*)\$$`
* **Descripción:** Detecta distractores cuyo error_rationale fue poblado erróneamente con la misma fórmula falsa de option.content o con el enunciado crudo del mito sin refutación pedagógica.
* **Ítems Evidencia:** Q-H04-061, Q-C01-201, Q-C01-202, Q-C08-341

* **ID de Regla:** `extended_and_stuttered_r15_length_padding`
* **Severidad:** warning
* **Patrón Regex:** `,\s*(?:según los supuestos clásicos del modelo|bajo las hipótesis del modelo|para la muestra de datos observada|de acuerdo con la teoría econométrica|en la formulación matricial considerada|en el contexto del contraste analizado|en el marco de la especificación)(?:,\s*(?:según los supuestos clásicos del modelo|bajo las hipótesis del modelo|para la muestra de datos observada|de acuerdo con la teoría econométrica|en la formulación matricial considerada|en el contexto del contraste analizado|en el marco de la especificación))*\.$`
* **Descripción:** Amplía el detector [R-15] para capturar las 7 variantes burocráticas hermanas y las colisiones de doble sufijo tartamudeado ('bajo las hipótesis del modelo, bajo las hipótesis del modelo.') inyectadas asimétricamente sobre claves o distractores.
* **Ítems Evidencia:** Q-Hab01-381, Q-Hab02-412, Q-Hab04-472, Q-Hab05-501, Q-Hab08-608

* **ID de Regla:** `fine_grained_percentage_multiplier_distractors`
* **Severidad:** warning
* **Patrón Regex:** `^\$[A-Za-z_\\{}^]+\s*=\s*-?\d+(?:\.\d+)?\$$`
* **Descripción:** Detecta bancos numéricos donde los 6 distractores se generan aplicando perturbaciones porcentuales fijas de malla fina (0.84x, 0.88x, 0.93x, 1.07x, 1.15x, 1.18x) sobre la respuesta correcta mientras el error_rationale declara un error algebraico estructural incompatible (como multiplicar por n en lugar de sqrt(n)).
* **Ítems Evidencia:** Q-H10-181, Q-H10-183, Q-H09-180

---

# PARTE II: AUDITORÍA FORENSE DE RENDIMIENTO Y TELEMETRÍA (RUN AUDITOR)

## 6. Consolidación de Métricas de Rendimiento y Ratios Unitarios

| Dimensión / Métrica | Valor Registrado | Observaciones de Ingeniería |
| :--- | :--- | :--- |
| **Material de Entrada (`pre_cta_manifest.json`)** | `2 archivos` (80 págs / 0.93 MB) | Ingesta directa PDF Zero-Waste (v3.2) |
| **Competencias Extraídas (`cta.json`)** | **`27 competencias`** | Compiladas desde tuplas posicionales (`compile_cta.py`) |
| **Shards Particionados (`pre_shard_manifest.json`)** | **`18 shards`** | Compilados vía `compile_shard.py` |
| **Subagentes Desplegados ($M$ CTA, $N$ Shards, $K$ Judges)** | **`24 subagentes`** | Fan-out dinámico coordinado por orquestador |
| **Reactivos Finales Validados** | **`620 preguntas`** | Evaluadas en sandbox in-process |
| **Tokens Entrada (Subagentes)** | **`2,110,060 tokens`** | Contexto acumulativo enviado a subagentes |
| **Tokens Salida (Subagentes)** | **`858,729 tokens`** | Código de tuplas Python y JSON generado |
| **Tokens Caché (Leídos)** | **`8,734,737 tokens`** | Caché de contexto reutilizado por la API |
| **Trazas de Pensamiento (`thinking_traces`)** | **`137 turnos` (615,081 chars)** | Razonamiento interno extraído de `transcript.jsonl` / `transcript_full.jsonl` |
| **Gran Total Tokens Activos** | **`2,968,789 tokens`** | Entrada + Salida neto (sin contar caché) |
| **Gran Total Tokens (con Caché)** | **`11,703,526 tokens`** | Consumo total de cuota facturable |
| **Tiempo de Pared Total** | **`1723.0 s` (28.72 min)** | Tiempo transcurrido de principio a fin |
| **Tiempo Cómputo Acumulado** | **`7885.0 s` (131.42 min)** | Suma escalar de tiempos de todos los agentes |
| **Factor de Aceleración Paralela** | **`4.58x`** | Relación tiempo cómputo vs tiempo de pared |
| **Tokens Totales por Pregunta** | **`18,876.7 tokens/preg`** | Esfuerzo de API por cada reactivo jugable |
| **Tokens Activos por Pregunta** | **`4,788.4 tokens/preg`** | Tokens netos de razonamiento y código por reactivo |
| **Tokens por Competencia (Global)** | **`433,463.9 tokens/comp`** | Densidad de diseño instruccional del curso |
| **Tokens de Autor por Competencia** | **`82,238.1 tokens/comp`** | Costo puro de la etapa de autoría |
| **Segundos de Pared por Pregunta** | **`2.78 s/preg`** | Ritmo de entrega percibido |
| **Rendimiento de Generación (QPM)** | **`21.59 preg/min`** | Velocidad de producción del pipeline |

---

## 7. Distribución Empírica del Tiempo: Inferencia LLM vs. Ejecución de Herramientas

- **Porcentaje Promedio en Inferencia LLM:** `95.8%`
- **Porcentaje Promedio en Ejecución Local de Herramientas:** `4.2%`

```
========================================================================================
DISTRIBUCIÓN DEL TIEMPO DE PARED POR SUBAGENTE (INFERENCIA LLM vs TOOLS)
========================================================================================
Direct CTA Architect   : [███████████████████████████████████████░] 1064s (99.6%) LLM | 4s Tools
Author Shard 01        : [███████████████████████████████████████░] 210s (98.1%) LLM | 4s Tools
Author Shard 02        : [███████████████████████████████████████░] 210s (99.1%) LLM | 2s Tools
Author Shard 03        : [███████████████████████████████████████░] 253s (98.8%) LLM | 3s Tools
Author Shard 04        : [███████████████████████████████████████░] 207s (98.6%) LLM | 3s Tools
Author Shard 05        : [███████████████████████████████████████░] 271s (99.3%) LLM | 2s Tools
Author Shard 06        : [███████████████████████████████████████░] 232s (98.7%) LLM | 3s Tools
Author Shard 07        : [███████████████████████████████████████░] 207s (98.6%) LLM | 3s Tools
Author Shard 08        : [███████████████████████████████████████░] 284s (98.3%) LLM | 5s Tools
Author Shard 09        : [███████████████████████████████████████░] 226s (97.8%) LLM | 5s Tools
Author Shard 10        : [███████████████████████████████████████░] 322s (99.1%) LLM | 3s Tools
Author Shard 11        : [██████████████████████████████████████░░] 342s (96.3%) LLM | 13s Tools
Author Shard 12        : [███████████████████████████████████████░] 234s (98.3%) LLM | 4s Tools
Author Shard 13        : [███████████████████████████████████████░] 326s (99.1%) LLM | 3s Tools
Author Shard 14        : [███████████████████████████████████████░] 281s (98.9%) LLM | 3s Tools
Author Shard 15        : [███████████████████████████████████████░] 287s (99.0%) LLM | 3s Tools
Author Shard 16        : [██████████████████████████████████████░░] 293s (96.4%) LLM | 11s Tools
Author Shard 17        : [███████████████████████████████████████░] 306s (98.1%) LLM | 6s Tools
Author Shard 18        : [███████████████████████████████████████░] 214s (98.6%) LLM | 3s Tools
Judge 01               : [████████████████████████████████████████] 52s (100.0%) LLM | 0s Tools
Judge 02               : [████████████████████████████████████████] 65s (100.0%) LLM | 0s Tools
Judge 03               : [███████████████████████████████████████░] 90s (97.8%) LLM | 2s Tools
Judge 04               : [████████████████████████████████████████] 54s (100.0%) LLM | 0s Tools
Judge 05               : [██████████████████████████████████████░░] 45s (95.7%) LLM | 2s Tools
========================================================================================
```

---

## 8. Métricas Deterministas de Latencia por Etapa

| Etapa del Pipeline | Agentes / Shards | Tiempo de Pared (s) | Detalle Determinista |
| :--- | :---: | :---: | :--- |
| **Stage 1B: CTA Architects** | `1` | `1068.0s` | Mappers max: `0.0s`, Harmonizer: `1068.0s` |
| **Stage 3: Shard Authors** | `18` | `355.0s` | Min: `210.0s`, Mediana: `273.0s`, Straggler: `Shard Author shard_11` (`+82.0s`) |
| **Stage 5: Blind Judges** | `5` | `92.0s` | Lote: `54` ítems, 1er intento: `True`, Auto-repair: `2` |
| **Orquestador Principal** | `1` | `1723.0s` | CLI: `64.0s`, Barrera: `39.0s`, Intervenciones: `0` (`0.0s`) |

---

## 9. Taxonomía Consolidada de Errores y Retrabajo

| Categoría de Error | Ocurrencias | Agentes Afectados | Causa Raíz Técnica y Ejemplo |
| :--- | :---: | :--- | :--- |
| **Missing File / Relative Path / Directory Error (FileNotFoundError)** | **43** | Author Shard 01, Author Shard 02, Author Shard 03 | Encountered error in step execution: declaring permissions: cortex tool view_file: convert |
| **Anti-Giveaway & Psychometric Parity Violations (R-14..R-19)** | **3** | Author Shard 11, Author Shard 14, Author Shard 16 | Encountered error in step execution: tool call denied by pre-tool hook: C2C Cross-Course I |
| **Token Limit Cutoff (Model Truncation)** | **1** | CTA Architect (part_01) | Error: Your previous response was cut off because it exceeded the output token limit Pleas |
| **LaTeX Control Character / Raw-String Corruption (R-03 / SyntaxWarning)** | **1** | CTA Architect (part_01) | The tool's output was truncated due to being too long. You can find the full output in a f |
| **Parameter Diversity & Option Collapse (TPL-VAR / TPL-COLLAPSE)** | **1** | Author Shard 11 | Command exited with code 1. / Command output: / [-] FAIL: 2 errores detectados (2 errores  |

---

## 10. Paquete Forense Agéntico Completo (Argon QA + Clúster Flash)

Todos los artefactos originales individuales generados por los auditores especializados se preservan íntegros en [`reports/audits_archive/estadistica_3_s9_vdirect/`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vdirect/):

- **Auditoría Cualitativa Profunda de Calidad (Gemini 4 Argon):** [`qa_report.md`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vdirect/qa_report.md) | [`qa_report.json`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vdirect/qa_report.json)
- **Informe Maestro Agéntico del Pipeline (Gemini Flash Lead + 3 Subagentes):** [`agentic_pipeline_audit.md`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vdirect/agentic_pipeline_audit.md)
- **Sub-Auditorías del Clúster Agéntico (`agentic_batches/`):** [`agentic_batches/`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vdirect/agentic_batches/)
- **Dashboard Visual Interactivo:** [`dashboard.html`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vdirect/dashboard.html)
- **Índice Completo del Archivo Persistente:** [`README.md`](file:///D:/Augusto/personal_portfolio/Tops_academy/reports/audits_archive/estadistica_3_s9_vdirect/README.md)
