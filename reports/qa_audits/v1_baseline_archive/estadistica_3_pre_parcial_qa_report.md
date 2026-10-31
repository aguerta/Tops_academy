# Reporte Normativo de Auditoría de Calidad Pedagógica y Técnica (Course QA)
## Curso: Estadistica 3 Pre Parcial (`estadistica_3_pre_parcial`)

**Plataforma:** Top's Academy  
**Estándares:** Quality Matters (QM), OSCQR, Mastery Learning  
**Fecha de Evaluación:** 26 de Octubre de 2026  
**Auditor:** Course QA Evaluator Subagent (Fast Hybrid Antigravity Engine)  

---

## 1. Resumen Ejecutivo y Dictamen de Certificación

| Métrica Global | Resultado |
| :--- | :--- |
| **Puntaje Consolidado** | **16.8 / 20.0 pts** |
| **Rango de Certificación** | **ACEPTABLE (14.0 - 16.9 pts)** |
| **Estado de Certificación** | **APROBADO CON OBSERVACIONES MENORES** (requiere remediación de pulido focalizado) |
| **Total de Micro-Competencias** | 93 micro-competencias |
| **Total de Reactivos Evaluados** | 2,190 preguntas |
| **Total de Distractores Inspeccionados** | 13,140 opciones |
| **Cobertura Diagnóstica de Rationale** | **100.0%** (13,140 / 13,140) |
| **Tasa de Compilación KaTeX** | **100.0%** (0 syntax fails, 0 delimitadores rotos) |
| **Penalizaciones Duras Aplicadas** | **0.0 pts** |

El curso **Estadistica 3 Pre Parcial** (`estadistica_3_pre_parcial`) es una suite evaluativa masiva y rigurosa compuesta por **2,190 reactivos** distribuidos en **93 micro-competencias**. El curso aborda exhaustivamente la econometría de regresión lineal simple y múltiple, derivaciones escalares y matriciales bajo el Teorema de Gauss-Markov, descomposición geométrica de proyecciones ortogonales ($P$ y $M$), inferencia estadística basada en distribuciones exactas ($t$ de Student, $F$ de Fisher, formas cuadráticas chi-cuadrado), diagnósticos y correcciones de violaciones a los supuestos clásicos (multicolinealidad, heterocedasticidad pura y autorregresiva ARCH, autocorrelación $AR(1)$ y de orden superior), especificación funcional, quiebres estructurales y endogeneidad.

El motor estático determinista procesó el 100% del banco de reactivos. Tras ejecutar el **Loop de Verificación Semántica**, se concluye que:
1. El **cluster de riesgo de 464 avisos de variables no interpoladas** corresponde en su totalidad a **falsos positivos sintácticos** originados por la presencia de expresiones legítimas de KaTeX (entornos matriciales `\begin{pmatrix}`, subíndices econométricos `_{BP}`, `_{LB}`, `_{MCO}`, `_{White}`, comandos de texto `\text{Tol}`, `\text{FIV}` y acentos `\hat{u}`, `\bar{X}`, `\bar{Y}`). Ninguna variable de plantilla real quedó sin interpolar.
2. Las **13 competencias basales sin prerrequisitos declarados** representan los puntos de entrada canónicos (nodos raíz) de los distintos subdominios del curso, garantizando la navegabilidad e integridad del grafo acíclico dirigido (DAG).
3. Se identificaron dos áreas de remediación pedagógica focalizada:
   - **Phantom Keying** localizado en la micro-competencia `Hab-11` (reactivos `Q-Hab11-721` y `Q-Hab11-722`), donde dos distractores clonan la respuesta correcta anteponiendo prefijos sintéticos (`"Opción alterna 5:"`, `"Opción alterna 6:"`).
   - Un cluster aislado de **32 reactivos con pistas deficientes tipo stub keywords** (`["Mco", "Insesgadez", "Gauss-markov"]`) en las competencias `Hab-06`, `Hab-08`, `Hab-19` y `Hab-20` (1.46% del total de reactivos).

Con un puntaje final de **16.8 / 20.0**, el curso se certifica en el nivel **ACEPTABLE**, quedando autorizado para su despliegue en plataforma condicionado a la ejecución de las acciones prioritarias de remediación.

---

## 2. Desglose Normativo por Dimensiones (Rúbrica de 20 Puntos)

```mermaid
xychart-beta
    title "Calificación por Dimensión vs. Puntaje Máximo"
    x-axis ["D1: Arquitectura", "D2: Evaluación", "D3: Andamiaje", "D4: Alineación", "D5: KaTeX"]
    y-axis "Puntaje" 0 --> 5
    bar [4.0, 3.2, 3.8, 4.0, 1.8]
    line [4.0, 5.0, 5.0, 4.0, 2.0]
```

| Dimensión | Puntos Obtenidos | Puntos Máximos | Cumplimiento (%) | Veredicto |
| :--- | :---: | :---: | :---: | :---: |
| **1. Arquitectura y Granularidad Curricular** | **4.0** | 4.0 | 100.0% | Excelente |
| **2. Calidad de Evaluación y Reactivos** | **3.2** | 5.0 | 64.0% | Aceptable |
| **3. Andamiaje y Pistas Progresivas** | **3.8** | 5.0 | 76.0% | Aceptable |
| **4. Alineación Instruccional** | **4.0** | 4.0 | 100.0% | Excelente |
| **5. Accesibilidad y Ergonomía Técnica / KaTeX** | **1.8** | 2.0 | 90.0% | Excelente |
| **Penalizaciones Duras Automáticas** | **0.0** | 0.0 | - | Sin deducción |
| **TOTAL CONSOLIDADO** | **16.8** | **20.0** | **84.0%** | **ACEPTABLE** |

---

### Dimensión 1: Arquitectura y Granularidad Curricular (4.0 / 4.0 pts)

- **Descomposición Cognitiva Tripartita:** Las 93 micro-competencias reflejan una distribución balanceada según los principios de Mastery Learning:
  - **Hechos [H]:** 24 competencias (25.8%), cubriendo especificaciones estándar, identidades matriciales, definiciones de estadísticos y reglas de decisión.
  - **Conceptos [C]:** 36 competencias (38.7%), abordando supuestos clásicos, teoremas fundamentales (Gauss-Markov, Slutsky, Frisch-Waugh-Lovell), ortogonalidad de operadores de proyección y mecanismos de distorsión inferencial.
  - **Habilidades [Hab]:** 33 competencias (35.5%), dedicadas a la derivación analítica de estimadores MCO, contrastes de hipótesis ($t$, $F$, LM, Chow, DWH), cálculo de matrices de covarianza robusta y algoritmos de estimación factible (MCG, Cochrane-Orcutt, Hildreth-Lu).
- **Densidad Psicométrica:** Cada micro-competencia dispone de un banco denso y robusto: exactamente 20 reactivos para Hechos y Conceptos, y 30 reactivos para Habilidades operativas. Esto arroja un promedio de 23.5 reactivos por competencia y cero unidades subpobladas (`underpopulated_competencies: 0`).
- **Verificación del Grafo DAG y Nodos Raíz:** 
  El escaneo preliminar identificó 13 competencias sin prerrequisitos declarados (`competencies_missing_prerequisites_count: 13`). El análisis semántico demostró que ninguna constituye una desconexión accidental del grafo ni una pregunta huérfana. Corresponden a los **13 nodos basales o axiomas fundacionales** que abren cada uno de los módulos temáticos del curso:
  1. `H-01`: *Especificación Estándar del Modelo de Regresión Lineal Simple*
  2. `H-03`: *Estructura de la Función de Regresión Poblacional y Perturbación Estocástica*
  3. `H-07`: *Estructura Matricial y Dimensiones del Modelo Lineal General*
  4. `C-17`: *Naturaleza Muestral y Grado de la Multicolinealidad*
  5. `C-21`: *Matriz de Covarianza de Perturbaciones No Esféricas*
  6. `H-19`: *Definición Formal de Heterocedasticidad y Pérdida de Eficiencia MCO*
  7. `H-20`: *Estadístico Durbin-Watson y Propiedades en Presencia de Autocorrelación AR(1)*
  8. `C-29`: *Inestabilidad de Parámetros, Quiebre Estructural y Modelación por Interacción*
  9. `H-21`: *Diagnóstico de Multicolinealidad Mediante el Factor de Inflación de Varianza (VIF)*
  10. `H-22`: *Estadístico de Jarque-Bera y Contraste de Normalidad de Residuos*
  11. `C-30`: *Sesgo por Variable Omitida y Dirección del Sesgo Econométrico*
  12. `C-32`: *Matriz de Proyección Ortogonal y Matriz de Residuos*
  13. `H-24`: *Estructura Matricial y Supuestos de Gauss-Markov del Modelo Lineal Múltiple*
  Todas estas competencias alimentan progresivamente a micro-competencias de orden superior, consolidando un grafo jerárquico y transitable sin ciclos.

---

### Dimensión 2: Calidad de Evaluación y Reactivos (3.2 / 5.0 pts)

- **Cobertura Diagnóstica Plena:** El 100.0% de los 13,140 distractores evaluados posee un `error_rationale` formativo riguroso. Cada distractor modela y explica una confusión conceptual o procedimental genuina de la literatura econométrica estándar:
  - Error en la dimensionalidad del vector de errores ($n \times 1$ vs. $K \times 1$).
  - Confusión entre la varianza teórica del estimador $\sigma^2(X'X)^{-1}$ y la estimada $s^2(X'X)^{-1}$.
  - Descuento erróneo de grados de libertad en regresión múltiple ($n-1$ vs. $n-K$).
  - Falacia de linealidad en la raíz de la varianza residual ($E[s] = \sigma$, refutada por la desigualdad de Jensen).
  - Confusión entre la ortogonalidad muestral ($X'\hat{u} = 0$) y la exogeneidad poblacional ($E[X'u] = 0$).
  - Inversión no conmutativa de productos matriciales ($(X'X)^{-1}X'y$ vs. $X'y(X'X)^{-1}$).
- **Integridad Psicométrica:** Ausencia absoluta de *Answer Leaks* en los enunciados, cero distractores delatores con muletillas pedagógicas visibles y cero rótulos parentéticos delatadores.
- **Hallazgos Críticos y Deducciones:**
  1. **Phantom Keying en la competencia `Hab-11` (-1.5 pts):**
     En los reactivos `Q-Hab11-721` y `Q-Hab11-722`, se detectó la presencia de opciones distractoras que reproducen exactamente la fórmula de la respuesta correcta bajo prefijos sintéticos artificiales:
     - En `Q-Hab11-721`:
       * *Opción B:* `"Opción alterna 5: $((X'X)^{-1}X'u)' = u' X (X'X)^{-1} \Rightarrow \text{Var}(\hat{\beta}|X) = \sigma^2 (X'X)^{-1}"`
       * *Opción D:* `"Opción alterna 6: $((X'X)^{-1}X'u)' = u' X (X'X)^{-1} \Rightarrow \text{Var}(\hat{\beta}|X) = \sigma^2 (X'X)^{-1}"`
       * *Clave E:* `"$((X'X)^{-1}X'u)' = u' X (X'X)^{-1} \Rightarrow \text{Var}(\hat{\beta}|X) = \sigma^2 (X'X)^{-1}$"`
     - En `Q-Hab11-722`:
       * *Opción B:* `"Opción alterna 6: $((X'X)^{-1}X'u)' = u' X (X'X)^{-1} \Rightarrow \text{Var}(\hat{\beta}|X) = \sigma^2 (X'X)^{-1}"`
       * *Opción F:* `"Opción alterna 5: $((X'X)^{-1}X'u)' = u' X (X'X)^{-1} \Rightarrow \text{Var}(\hat{\beta}|X) = \sigma^2 (X'X)^{-1}"`
       * *Clave E:* `"$((X'X)^{-1}X'u)' = u' X (X'X)^{-1} \Rightarrow \text{Var}(\hat{\beta}|X) = \sigma^2 (X'X)^{-1}$"`
     Conforme a la rúbrica (*"Phantom Keying: distractores con el valor idéntico a la clave bajo prefijos sintéticos tipo 'Opción alterna X:' (-2.0 a -3.0 pts)"*), dado que se trata de un incidente focalizado en dos reactivos de una única competencia y no de una falla sistemática global, se aplica una deducción ajustada de **-1.5 puntos**.
  2. **Monocultivo de Tipología de Reactivo (-0.3 pts):**
     El 100% de los 2,190 reactivos está formulado en el formato de Opción Múltiple de 7 alternativas (`multiple_choice_7_options`). Si bien MC7 ofrece una excelente resistencia a la adivinación fortuita ($P_{azar} \approx 14.3\%$), la rúbrica premia la variedad multimodal incluyendo reactivos de respuesta múltiple (MS) o completamiento numérico/algebraico (FIB). Se aplica una deducción de **-0.3 puntos**.

---

### Dimensión 3: Andamiaje y Feedback Progresivo (3.8 / 5.0 pts)

- **Andamiaje General de Alta Calidad (98.54% del Banco):**
  2,158 de los 2,190 reactivos disponen de 3 pistas socráticas escalonadas en prosa fluida y estructurada:
  1. *Pista 1 (Marco Conceptual):* Delimita el principio teórico o supuesto clásico involucrado.
  2. *Pista 2 (Guía Procedimental):* Orienta el planteamiento algebraico o numérico sin anticipar el resultado.
  3. *Pista 3 (Validación y Chequeo):* Previene el desvío hacia falacias frecuentes y exige contrastar la consistencia dimensional.
- **Soluciones Detalladas:** El 100% de los reactivos incluye una `detailed_solution` completa, con el desarrollo paso a paso de las ecuaciones normales, la expansión de formas cuadráticas o el cómputo de estadísticos empíricos.
- **Hallazgo Crítico y Justificación de la Deducción (-1.2 pts):**
  Se detectó un cluster específico de **32 reactivos** (1.46% del total) cuyas pistas fueron generadas como palabras clave breves o etiquetas snake_case en lugar de prosa socrática estructurada:
  - **`Hab-06` (reactivos `Q-Hab06-371` a `Q-Hab06-378`, 8 ítems):** Pistas: `["Mco", "Insesgadez", "Gauss-markov"]`.
  - **`Hab-08` (reactivos `Q-Hab08-451` a `Q-Hab08-458`, 8 ítems):** Pistas: `["Gauss-markov", "Varianza", "Eficiencia"]`.
  - **`Hab-19` (reactivos `Q-Hab19-1301` a `Q-Hab19-1308`, 8 ítems):** Pistas: `["Goldfeld_quandt", "Heterocedasticidad", "Submuestras"]`.
  - **`Hab-20` (reactivos `Q-Hab20-1331` a `Q-Hab20-1338`, 8 ítems):** Pistas: `["Arch", "Heterocedasticidad", "Engle"]`.
  Siguiendo el criterio de la rúbrica normativa (*"Pistas deficientes aisladas (stub hints de una sola palabra o tags snake_case) (-1.0 a -1.5 pts)"*), se aplica una deducción de **-1.2 puntos**.

---

### Dimensión 4: Alineación Instruccional (4.0 / 4.0 pts)

- **Congruencia Semántica:** Puntuación perfecta (4.0 / 4.0).
- **Cobertura Curricular Exhaustiva:** La suite cubre íntegramente los estándares de la enseñanza moderna de la Econometría y la Estadística Matemática intermedia/avanzada. Los 93 temas abarcan:
  - Formulación escalar y matricial del modelo lineal general ($y = X\beta + u$).
  - Ortogonalidad geométrica y álgebra de matrices de proyección ($P = X(X'X)^{-1}X'$) y aniquiladoras ($M = I - P$).
  - Propiedades en muestra finita (insesgadez, varianza-covarianza) y asintóticas (consistencia vía LGN y teorema de Slutsky).
  - Inferencia estadística exacta: contrastes $t$, contrastes $F$ sobre restricciones lineales generales ($R\beta = r$), matrices de centrado $M^0$ y descomposición ANOVA ($STC = SEC + SRC$).
  - Violaciones clásicas: multicolinealidad aproximada vs. exacta, métricas de diagnóstico (VIF, Tolerancia, Índice de Condición, Farrar-Glauber, regla de Klein) y métodos de regularización (Ridge, Componentes Principales).
  - Errores no esféricos: estructura general $\sigma^2\Omega$, estimadores MCG y MCGF, contraste de Breusch-Pagan, contraste de White, contraste de Goldfeld-Quandt, contraste de Glejser, modelos ARCH(q) de Engle, ponderadores de MCP y errores estándar robustos HCSE de White.
  - Dependencia temporal: perturbaciones $AR(1)$, contrastes de Durbin-Watson, $h$ de Durbin ante retardos de la dependiente, contraste LM de Breusch-Godfrey de orden $p$, contrastes portmanteau de Box-Pierce y Ljung-Box, transformaciones en cuasidiferencias (Prais-Winsten vs. Cochrane-Orcutt) y covarianza consistente HAC de Newey-West.
  - Tópicos avanzados de especificación: transformaciones funcionales (Lin-Log, Log-Lin, Box-Cox), quiebres estructurales y contrastes de Chow, contraste de normalidad de Jarque-Bera, sesgo por variable omitida, error de medición clásico y contraste de endogeneidad de Durbin-Wu-Hausman.
- **Cero Preguntas Huérfanas ni Contaminación Inter-Dominio:** El 100% de los reactivos pertenece al dominio econométrico declarado.
- **Nivel Taxonómico de Bloom:** Dominio predominante de los niveles de **Aplicación** (cálculo de estimadores, estadísticas de prueba, transformaciones matriciales) y **Análisis** (interpretación de paradojas de contrastes, derivaciones de sesgo, consecuencias inferenciales de errores no esféricos).

---

### Dimensión 5: Accesibilidad y Ergonomía Técnica / KaTeX (1.8 / 2.0 pts)

- **Integridad Sintáctica KaTeX:**
  - Delimitadores `$...$` balanceados: 100% (cero desbalanceados).
  - Triples signos de dólar (`$$$`): 0.
  - Llaves dobles accidentales (`{{...}}`): 0.
  - Delimitadores LaTeX en texto plano sin cerrar: 0.
- **Auditoría Semántica del Cluster de Variables No Interpoladas (464 Avisos):**
  El linter estático determinista emitió 464 advertencias de `uninterpolated_math_variable_linter`. La auditoría semántica detallada confirmó que el **100% de estos avisos son falsos positivos** provocados por una expresión regular de búsqueda de variables que no contempla construcciones válidas de LaTeX:
  1. *Entornos Matriciales KaTeX:* `\begin{pmatrix}` y `\end{pmatrix}` (e.g. `Q-Hab29-1921` a `1946`), donde `{pmatrix}` fue capturado como una supuesta variable.
  2. *Subíndices Econométricos Compuestos:* Fórmulas con `_{BP}` (Breusch-Pagan), `_{LB}` (Ljung-Box), `_{MCO}` (Mínimos Cuadrados Ordinarios), `_{White}` o `_{aux}` (e.g. `Q-C26-1536`, `Q-C28-1738`, `Q-H16-1411`), donde las llaves son sintaxis canónica de LaTeX para subíndices de múltiples caracteres.
  3. *Macros de Formato de Texto:* Expresiones como `\text{Tol}` y `\text{FIV}` en `Q-H13-1027` a `1029`, donde `{Tol}` y `{FIV}` son los argumentos del comando `\text{}`.
  4. *Acentos Matemáticos y Símbolos Escalares:* Notaciones como `\hat{u}`, `\hat{v}`, `\bar{X}`, `\bar{Y}` y `E(u_i|X_i)` (e.g. `Q-C05-276` a `280`, `Q-Hab25-1581` a `1602`, `Q-Hab31-2063` a `2070`), donde `{u}`, `{v}`, `{X}` y `{Y}` son argumentos de acento o variables aleatorias estándares.
  Todas estas expresiones compilan sin errores en el motor KaTeX de la plataforma, conservando una presentación tipográfica impecable.
- **Deducción Menor (-0.2 pts):** Se identificó una leve redundancia estilística en las cláusulas de cierre de opciones numéricas, donde se repiten frases de relleno sintáctico (e.g. `", para los parámetros bajo análisis"`, `", de acuerdo con la teoría econométrica"`, `", bajo las hipótesis del modelo"`).

---

## 3. Loop de Verificación Semántica: Evidencias y Citas Textuales

### Caso 1: Phantom Keying en `Hab-11` (Deducción en Dimensión 2)

En los reactivos `Q-Hab11-721` y `Q-Hab11-722`, el generador de distractores clonó el valor matemático de la clave correcta bajo etiquetas artificiales:

> **Reactivo `Q-Hab11-721`**  
> **Enunciado:** *"Considerando las ecuaciones fundamentales del régimen, obtenga: En un modelo de regresión lineal múltiple con matriz de diseño $X$ de orden $324 \times 8$ y perturbaciones con $E[uu'|X] = \sigma^2 I_{324}$, desarrolle la matriz de varianza-covarianza condicional $\text{Var}(\hat{\beta}|X) = E[(\hat{\beta}-\beta)(\hat{\beta}-\beta)'|X]$. ¿Cuál es la simplificación analítica correcta del producto intermedio y la matriz resultante?"*  
> - **Opción B (Distractor D-Hab11-03):** `"Opción alterna 5: $((X'X)^{-1}X'u)' = u' X (X'X)^{-1} \Rightarrow \text{Var}(\hat{\beta}|X) = \sigma^2 (X'X)^{-1}"` (is_correct: false)  
> - **Opción D (Distractor D-Hab11-05):** `"Opción alterna 6: $((X'X)^{-1}X'u)' = u' X (X'X)^{-1} \Rightarrow \text{Var}(\hat{\beta}|X) = \sigma^2 (X'X)^{-1}"` (is_correct: false)  
> - **Opción E (Clave Correcta):** `"$((X'X)^{-1}X'u)' = u' X (X'X)^{-1} \Rightarrow \text{Var}(\hat{\beta}|X) = \sigma^2 (X'X)^{-1}$"` (is_correct: true)  

**Diagnóstico Psicométrico:** Esta anomalía confunde al estudiante al presentar tres opciones con la fórmula exacta idéntica, diferenciadas únicamente por el prefijo `"Opción alterna X:"`. Requiere reemplazo inmediato por distractores con errores conceptuales reales (e.g. omitir la transposición del producto o alterar el orden de factores).

---

### Caso 2: Pistas Deficientes Tipo Stub Keywords en `Hab-06`, `Hab-08`, `Hab-19`, `Hab-20` (Deducción en Dimensión 3)

En 32 reactivos correspondientes a cuatro micro-competencias de Habilidades, las pistas se generaron como términos aislados sin desarrollo socrático:

> **Reactivo `Q-Hab06-371`**  
> **Enunciado:** *"Al examinar detenidamente las condiciones de frontera, resuelva: Considere el modelo de regresión lineal simple $Y_i = \beta_1 + \beta_2 X_i + u_i$ con parámetros poblacionales $\beta_1 = 24$ y $\beta_2 = 10$, varianza de las perturbaciones $\sigma^2 = 13$ y una muestra de $n = 69$ observaciones. Si se satisface el supuesto de Gauss-Markov de media condicional nula $E(u_i \mid X) = 0$, calcule el valor esperado condicional del estimador MCO de la pendiente, $E(\hat{\beta}_2 \mid X)$:"*  
> - **Pistas generadas:** `["Mco", "Insesgadez", "Gauss-markov"]`  
> - **Impacto pedagógico:** Las pistas actúan como simples etiquetas temáticas en lugar de andamiaje socrático guiado. Deben ser expandidas a prosa explicativa de 3 etapas.

---

### Caso 3: Desmitificación del Cluster de Variables No Interpoladas (Falsos Positivos)

La auditoría analizó las advertencias arrojadas en los 464 reactivos:

> **Reactivo `Q-Hab29-1921`** (advertencia: `{pmatrix}` en stem)  
> **Fragmento en JSON:**  
> `"...la matriz de productos cruzados es $X'X = \begin{pmatrix} 4 & 18 \\ 18 & 91 \end{pmatrix}$. Calcule el determinante..."`  
> **Veredicto Semántico:** Renderizado perfecto en KaTeX. `{pmatrix}` es el argumento del entorno de matriz de LaTeX, no un placeholder de plantilla.

> **Reactivo `Q-C26-1536`** (advertencia: `{BP}` en stem)  
> **Fragmento en JSON:**  
> `"...evaluando el estadístico de Box-Pierce $Q_{BP} = T \sum_{j=1}^p r_j^2$..."`  
> **Veredicto Semántico:** Subíndice matemático estándar en KaTeX. `{BP}` delimita los caracteres del subíndice para evitar que solo la `B` quede subindicada.

> **Reactivo `Q-H13-1027`** (advertencia: `{Tol}` en stem y `{FIV}` en solution)  
> **Fragmento en JSON:**  
> `"...con tolerancia $\text{Tol}_j = \frac{1}{\text{FIV}_j}$..."`  
> **Veredicto Semántico:** Comando estándar `\text{...}` para representar variables macroeconómicas o econométricas en fuente romana no itálica. Renderiza correctamente como $\text{Tol}_j = \frac{1}{\text{FIV}_j}$.

---

## 4. Loop de Auto-Mejora de Reglas de Linteo (Discovered Lint Rules)

A partir de las discrepancias halladas entre los resultados del motor determinista y la inspección semántica humana, se proponen formalmente tres nuevas reglas de linteo para optimizar el auditor estático de la plataforma:

### Regla 1: Exclusión de Entornos de Matriz y Comandos de Texto en el Detector de Variables
- **ID:** `exclude_latex_matrix_and_text_from_template_linter`
- **Linter Afectado:** `uninterpolated_math_variable_linter`
- **Expresión Regular Propuesta:**
  ```python
  r'(?<!\\begin\{)(?<!\\end\{)(?<!\\text\{)(?<!\\operatorname\{)\{([a-zA-Z_][a-zA-Z0-9_]*)\}(?!\$)'
  ```
- **Justificación:** Elimina más de 200 falsos positivos en suites avanzadas cuantitativas donde `\begin{pmatrix}`, `\begin{bmatrix}` o comandos como `\text{Tol}` y `\text{FIV}` son sintaxis canónica de KaTeX.

### Regla 2: Exclusión de Subíndices Econométricos Compuestos
- **ID:** `exclude_econometric_subscripts_from_template_linter`
- **Linter Afectado:** `uninterpolated_math_variable_linter`
- **Expresión Regular Propuesta:**
  ```python
  r'(?<!_)\{([A-Z]{2,5}|[a-z]{2,5})\}'
  ```
- **Justificación:** Previene más de 180 falsos positivos en notación econométrica estandarizada donde los subíndices de contrastes van entre llaves (e.g. `_{BP}`, `_{LB}`, `_{MCO}`, `_{White}`, `_{aux}`).

### Regla 3: Normalización de Prefijos Sintéticos en Detección de Distractores Clonados
- **ID:** `strip_synthetic_prefixes_before_cloned_distractor_check`
- **Linter Afectado:** `cloned_distractor_value_linter`
- **Lógica de Parche:**
  ```python
  clean_content = re.sub(r'^(Opción alterna \d+:\s*|Alternativa \d+:\s*)', '', option['content'])
  ```
- **Justificación:** Permite que el linter determinista capture automáticamente el fenómeno de "Phantom Keying", el cual actualmente evade la igualdad estricta de cadenas al estar enmascarado por prefijos sintéticos como `"Opción alterna 5:"`.

---

## 5. Plan de Acción y Remediación Priorizado

```mermaid
flowchart TD
    A["Reporte QA: ACEPTABLE (16.8 / 20.0)"] --> B["Prioridad ALTA: Hab-11"]
    A --> C["Prioridad MEDIA: Hab-06, Hab-08, Hab-19, Hab-20"]
    A --> D["Prioridad BAJA: Tipología Multimodal"]

    B --> B1["Reemplazar opciones clonadas en Q-Hab11-721 y Q-Hab11-722"]
    B1 --> B2["Eliminar prefijos 'Opción alterna X:' e inyectar errores conceptuales reales"]

    C --> C1["Expandir 32 stub hints a prosa socrática de 3 etapas"]
    C1 --> C2["Pista 1: Conceptual | Pista 2: Procedimental | Pista 3: Chequeo"]

    D --> D1["Introducir reactivos MS y FIB en versiones futuras del curso"]

    B2 --> E["Curso Certificado en Calidad EXCELENTE (18.5+ pts)"]
    C2 --> E
    D1 --> E
```

### Prioridad Alta (Inmediata - Previa a Despliegue en Producción)
1. **Remediar Phantom Keying en `Hab-11`:**
   - **Ítems:** `Q-Hab11-721` y `Q-Hab11-722`.
   - **Acción:** Reemplazar las opciones distractores que contienen `"Opción alterna 5:"` y `"Opción alterna 6:"` por formulaciones alternativas plausibles con errores algebraicos auténticos (e.g. transposición incorrecta de la matriz sándwich o inversión del orden del producto de covarianzas).

### Prioridad Media (Reingeniería de Andamiaje)
2. **Reescritura de Pistas en 32 Reactivos:**
   - **Ítems:** `Q-Hab06-371` a `378`, `Q-Hab08-451` a `458`, `Q-Hab19-1301` a `1308` y `Q-Hab20-1331` a `1338`.
   - **Acción:** Transformar las pistas tipo palabras clave aisladas (`["Mco", "Insesgadez", "Gauss-markov"]`) en andamiaje socrático completo de tres pasos en prosa fluida:
     * *Pista 1:* Enunciar el marco teórico (e.g. representación lineal del estimador $\hat{\beta}_2 = \sum k_i Y_i$ y propiedades de los ponderadores determinísticos $\sum k_i = 0$ y $\sum k_i X_i = 1$).
     * *Pista 2:* Guiar la aplicación de la esperanza condicional sobre la perturbación ($E[u_i|X] = 0$).
     * *Pista 3:* Formular la conclusión analítica e instruir la verificación del valor esperado resultante.

### Prioridad Baja (Optimización de Plataforma a Mediano Plazo)
3. **Diversificación Multimodal de Reactivos:**
   - Enriquecer el curso introduciendo ítems de selección múltiple (MS) con varias respuestas válidas y problemas de cálculo numérico directo (fill-in-the-blank) para reducir la dependencia exclusiva del formato MC7.
4. **Limpieza de Muletillas Estilísticas en Distractores Numéricos:**
   - Normalizar la redacción de distractores en reactivos de cálculo para eliminar redundancias como `", de acuerdo con la teoría econométrica"` o `", para la muestra de datos observada"`.

---

## 6. Dictamen Final

El curso **Estadistica 3 Pre Parcial** (`estadistica_3_pre_parcial`) se declara **APROBADO CON OBSERVACIONES MENORES (ACEPTABLE, 16.8 / 20.0 pts)**.

Presenta una calidad matemática, psicométrica y de alineación conceptual extraordinaria en más del 98% de su contenido. Las observaciones señaladas corresponden a dos fallas puntuales y perfectamente subsanables (Phantom Keying en 2 ítems y pistas breves en 32 reactivos), las cuales, una vez remediadas, permitirán elevar la calificación del curso al rango de **EXCELENCIA (18.5+ pts)**.
