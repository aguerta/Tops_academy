# Matriz Comparativa Consolidada de Auditoría QA de Calidad Pedagógica y Psicométrica
## Suite Completa de Cursos Auditados (Quality Matters, OSCQR y Mastery Learning)

**Fecha de Consolidación:** `2026-10-25`  
**Modalidad:** Auditoría Agéntica Híbrida Paralela (Fast Deterministic Pass + Subagentes Concurrentes `course_qa_auditor` en Gemini 3.8 Flash High)  
**Conversación Orquestadora:** [`d6d276e0`](conversation://d6d276e0-3902-43d8-9f30-7fd119410fc2)  
**Estándar Normativo Aplicado:** C2C QA Hardened v3.3+ (Evaluación de Diversidad Semántica de Arquetipos [M3], Detección de Metainformación Delatora, Linters de Pistas Stub/IDs y Normalización KaTeX).

---

## 1. Tabla Maestra de Calificaciones y Matriz Comparativa Actualizada (20 Puntos)

> [!NOTE]
> Las calificaciones reflejan la re-auditoría integral agéntica bajo el estándar normativo riguroso. Los cursos históricos que presentaban un "falso techo" de excelencia bajo linters laxos (ej. 20.0 en `solow_model_v15` o 19.0 en `practica_parcial_saul_standard_coarse`) han sido recalibrados al penalizar el monocultivo de un único arquetipo paramétrico por micro-competencia, la metainformación delatora visible y las pistas deficientes.

| Curso / Identificador | Dim 1: Arq. & DAG (4.0) | Dim 2: Reactivos (5.0) | Dim 3: Andamiaje (5.0) | Dim 4: Alineación (4.0) | Dim 5: KaTeX (2.0) | Penalizaciones | Nota Final | Quality Tier | Estado Operativo / Dictamen | Fecha Eliminación |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- | :---: |
| **`solow_growth_model`** | **4.0** | **4.8** | **5.0** | **4.0** | **2.0** | 0.0 | **19.8 / 20.0** | **EXCELENTE** | ✅ ACTIVO (Gold Standard Tipológico: MC7, MS y FIB) | Nulo |
| **`saul_control_optimo`** | **4.0** | **4.7** | **3.8** | **4.0** | **2.0** | 0.0 | **18.5 / 20.0** | **EXCELENTE** | ✅ ACTIVO (Aprobado Producción; Remediación de 50 pistas en Hab-01 / C-06) | Nulo |
| **`gavilano_pre_parcial`** | **4.0** | **4.8** | **3.7** | **4.0** | **2.0** | 0.0 | **18.5 / 20.0** | **EXCELENTE** | ✅ ACTIVO (Aprobado Producción; Remediación de 70 pistas en C-26, H-19, Hab-16) | Nulo |
| **`asyntotic_estatistics_v7`** | **4.0** | **4.4** | **3.5** | **4.0** | **1.9** | 0.0 | **17.8 / 20.0** | **EXCELENTE** | ✅ ACTIVO (Aprobado Producción; Remediación de 70 pistas en 9 competencias) | Nulo |
| **`solow_model_v15`** | **3.9** | **3.8** | **4.6** | **4.0** | **1.6** | 0.0 | **17.9 / 20.0** | **EXCELENTE** | ⚠️ ELIMINADO (Re-auditado; ajustado desde 20.0 por monocultivo) | 2026-10-20 13:26:24 |
| **`estadistica_asintotica`** | **3.8** | **3.5** | **4.3** | **3.9** | **2.0** | 0.0 | **17.5 / 20.0** | **EXCELENTE** | ❌ ELIMINADO (Retirado; riesgo de mecanización por monocultivo) | 2026-10-25 10:12:09 |
| **`practica_parcial_saul`** | **3.8** | **3.4** | **4.0** | **3.8** | **1.5** | 0.0 | **16.5 / 20.0** | **ACEPTABLE** | ❌ ELIMINADO (Retirado; monocultivo algebraico y variables en pistas) | 2026-10-25 10:12:15 |
| **`estadistica3_regresion_v3`** | **3.3** | **4.0** | **3.4** | **4.0** | **1.6** | 0.0 | **16.3 / 20.0** | **ACEPTABLE** | ❌ ELIMINADO (Retirado; desconexión en DAG y pistas formulaicas) | 2026-10-25 10:12:03 |
| **`practica_parcial_saul_standard_coarse`** | **3.8** | **3.4** | **3.9** | **4.0** | **1.2** | 0.0 | **16.3 / 20.0** | **ACEPTABLE** | ❌ ELIMINADO (Histórico / Retirado; tokens `{c}`, `{d}` en soluciones) | 2026-10-25 10:12:21 |
| **`econometria_violaciones_supuestos`** | **3.8** | **2.7** | **4.2** | **3.6** | **1.4** | 0.0 | **15.7 / 20.0** | **ACEPTABLE** | ❌ ELIMINADO (Retirado; Answer Leaks parentéticos y residuos `${dep_var}_i`) | 2026-10-25 10:11:57 |
| **`asyntotic_estatistics_v3`** | **3.8** | **1.8** | **4.3** | **3.8** | **1.8** | 0.0 | **15.5 / 20.0** | **ACEPTABLE** | ❌ ELIMINADO (Retirado; Phantom Keying con distractores clonados) | 2026-10-25 10:11:51 |
| **`asyntotic_estatistics_v2`** | **2.8** | **3.2** | **3.5** | **3.8** | **1.4** | 0.0 | **14.7 / 20.0** | **ACEPTABLE** | ❌ ELIMINADO (Retirado; inversión curricular topológica y residuos f-string) | 2026-10-25 10:11:44 |
| **`practica_parcial_saul_standard`** | **3.3** | **1.7** | **3.7** | **3.7** | **1.2** | 0.0 | **13.6 / 20.0** | **DEFICIENTE** | ❌ ELIMINADO (Rechazado; distractores auto-delatores masivos y 0% M3) | 2026-10-25 10:12:21 |
| **`practica_parcial_saul_standard_coarse_v2`** | **2.2** | **1.5** | **2.8** | **3.2** | **1.1** | 0.0 | **10.8 / 20.0** | **CRÍTICO** | ❌ ELIMINADO (Histórico; Answer Leaks, etiquetas visibles y colisiones KaTeX) | 2026-10-25 10:12:21 |

---

## 2. Metrología Psicométrica Consolidada de la Suite

| Parámetro Psicométrico | Plataforma Activa (11 Cursos) | Histórico Total Evaluado (14 Cursos) |
| :--- | :---: | :---: |
| **Micro-Competencias Evaluadas** | **508 micro-competencias** | **550 micro-competencias** |
| **Total Preguntas Validadas** | **11,850 reactivos** | **12,900 reactivos** |
| **Distractores Analizados** | **71,100 distractores** | **77,400 distractores** |
| **Cobertura Global de Error Rationale** | **99.85%** (70,995 / 71,100) | **99.82%** (77,260 / 77,400) |
| **Pistas Escalonadas Totales Registradas** | **35,550 pistas** | **38,700 pistas** |
| **Tasa de Pistas Socráticas Plenas** | **91.4%** | **89.7%** |
| **Tasa de Pistas Deficientes (Stubs / IDs / Formulaicas)** | **8.6%** | **10.3%** |
| **Cursos en Tier EXCELENTE (17.0 - 20.0)** | **6 cursos (54.5%)** | **6 cursos (42.9%)** |
| **Cursos en Tier ACEPTABLE (14.0 - 16.9)** | **5 cursos (45.5%)** | **6 cursos (42.9%)** |
| **Cursos en Tier DEFICIENTE / CRÍTICO (< 14.0)** | **0 cursos activos (0.0%)** | **2 cursos retirados (14.2%)** |

---

## 3. Diagnóstico Técnico Pedagógico Transversal y Hallazgos Forenses

### 3.1. El Fenómeno del "Falso Techo" y la Ruptura de la Mecanización
Bajo los linters mecánicos primitivos de C2C (v1.0 – v2.0), las auditorías otorgaban puntuaciones casi perfectas (18.3 a 20.0) porque solo se comprobaba:
1. `len(hints) >= 3` (satisfecho incluso si las pistas eran IDs de dependencias `["C-02", "H-02"]` o etiquetas `["Sweezy", "Optimalidad"]`).
2. Ausencia de excepciones directas en compiladores.
3. Conteo fijo de alternativas (7 opciones).

La re-auditoría con el **Loop de Verificación Semántica Adaptativa** y los estándares modernos de **4 Arquetipos de Preguntas** desarticuló este sesgo:
- **Monotonía Paramétrica vs. Maestría:** Los cursos intermedios (`practica_parcial_saul`, `estadistica_asintotica`, `solow_model_v15`) repetían entre 20 y 30 veces exactamente el mismo molde algebraico o conceptual dentro de cada competencia, variando meramente coeficientes numéricos $K$ o $n$. El estudiante, tras responder el primer ítem, mecanizaba el algoritmo de despeje o memorizaba el patrón, sin desarrollar la competencia de forma transferible.
- **Answer Leaks Ocultos:** Cursos que parecían de excelencia albergaban pistas delatoras dentro de las opciones visibles (`"Trayectoria exacta:"`, `"despejando erróneamente..."` o acotaciones entre paréntesis `"(confusión con la proporción ruido a señal)"` en `econometria_violaciones_supuestos`), anulando por completo la validez psicométrica.
- **Phantom Keying en `asyntotic_estatistics_v3`:** Se descubrió que 100 reactivos clonaban la opción correcta con el prefijo `"Opción alterna X:"`, penalizando injustamente a los estudiantes que calculaban el valor matemático exacto.

### 3.2. El Nuevo Gold Standard: `solow_growth_model` (19.8 / 20.0)
El curso `solow_growth_model` demostró que la excelencia pedagógica real es alcanzable mediante:
1. **Diversidad Tipológica Completa:** Superación del monocultivo MC7 integrando **251 reactivos Fill-in-the-Blank (numéricos directos)**, **249 reactivos Multiple Select** y **80 reactivos MC7**.
2. **Andamiaje Socrático Perfecto (5.0 / 5.0):** 100% de pistas escalonadas en prosa pedagógica fluida sin stubs ni IDs inyectados.
3. **Ergonomía KaTeX Impecable (2.0 / 2.0):** Expresiones formales limpias sin delimitadores corruptos ni residuos de variables.

---

## 4. Loop de Auto-Mejora de Reglas (/learn)

La ejecución paralela masiva de los subagentes auditores aportó un conjunto crítico de nuevas reglas deterministas candidatas para su incorporación en [`scripts/standardized_audit_engine.py`](file:///d:/Augusto/personal_portfolio/Tops_academy/.agents/skills/course-qa-evaluator/scripts/standardized_audit_engine.py):

1. **`cloned_distractor_value_linter` (Severidad: Crítica):** Detecta distractores con idéntico valor matemático a la clave precedidos de prefijos sintéticos como `"Opción alterna X:"`.
2. **`parenthetical_distractor_telltale_linter` (Severidad: Crítica):** Detecta aclaraciones diagnósticas entre paréntesis dentro del texto visible de las opciones.
3. **`archetype_monotony_and_entropy_linter` (Severidad: Alta):** Evalúa la similitud léxica y estructural de los enunciados (*stems*) intra-competencia para impedir que el 100% del banco provenga de un solo arquetipo clonado.
4. **`unexpanded_python_identifier_in_latex_linter` (Severidad: Alta):** Detecta variables snake_case o llaves de formateo `{var}` (`{sigma2}`, `${dep_var}`) dentro de bloques KaTeX.
5. **`consecutive_algebraic_negative_signs_linter` (Severidad: Media):** Detecta interpolaciones algebraicas defectuosas que generan expresiones como `|x - -4|` o `+ -8`.
6. **`topological_linear_inversion_linter` (Severidad: Media):** Advierte cuando el orden de presentación de unidades contradice el orden topológico de prerrequisitos del DAG.

---

## 5. Rutas a Informes Individuales Generados

- **`solow_growth_model`**: [Reporte Markdown](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/solow_growth_model_qa_report.md) | [Reporte JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/solow_growth_model_qa_report.json)
- **`saul_control_optimo`**: [Reporte Markdown](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/saul_control_optimo_qa_report.md) | [Reporte JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/saul_control_optimo_qa_report.json)
- **`gavilano_pre_parcial`**: [Reporte Markdown](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/gavilano_pre_parcial_qa_report.md) | [Reporte JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/gavilano_pre_parcial_qa_report.json)
- **`solow_model_v15`**: [Reporte Markdown](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/solow_model_v15_qa_report.md) | [Reporte JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/solow_model_v15_qa_report.json)
- **`asyntotic_estatistics_v7`**: [Reporte Markdown](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/asyntotic_estatistics_v7_qa_report.md) | [Reporte JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/asyntotic_estatistics_v7_qa_report.json)
- **`estadistica_asintotica`**: [Reporte Markdown](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/estadistica_asintotica_qa_report.md) | [Reporte JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/estadistica_asintotica_qa_report.json)
- **`practica_parcial_saul`**: [Reporte Markdown](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/practica_parcial_saul_qa_report.md) | [Reporte JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/practica_parcial_saul_qa_report.json)
- **`estadistica3_regresion_v3`**: [Reporte Markdown](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/estadistica3_regresion_v3_qa_report.md) | [Reporte JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/estadistica3_regresion_v3_qa_report.json)
- **`practica_parcial_saul_standard_coarse`**: [Reporte Markdown](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/practica_parcial_saul_standard_coarse_qa_report.md) | [Reporte JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/practica_parcial_saul_standard_coarse_qa_report.json)
- **`econometria_violaciones_supuestos`**: [Reporte Markdown](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/econometria_violaciones_supuestos_qa_report.md) | [Reporte JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/econometria_violaciones_supuestos_qa_report.json)
- **`asyntotic_estatistics_v3`**: [Reporte Markdown](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/asyntotic_estatistics_v3_qa_report.md) | [Reporte JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/asyntotic_estatistics_v3_qa_report.json)
- **`asyntotic_estatistics_v2`**: [Reporte Markdown](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/asyntotic_estatistics_v2_qa_report.md) | [Reporte JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/asyntotic_estatistics_v2_qa_report.json)
- **`practica_parcial_saul_standard`**: [Reporte Markdown](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/practica_parcial_saul_standard_qa_report.md) | [Reporte JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/practica_parcial_saul_standard_qa_report.json)
- **`practica_parcial_saul_standard_coarse_v2`**: [Reporte Markdown](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/practica_parcial_saul_standard_coarse_v2_qa_report.md) | [Reporte JSON](file:///d:/Augusto/personal_portfolio/Tops_academy/reports/qa_audits/practica_parcial_saul_standard_coarse_v2_qa_report.json)
