# Antigravity Skill Pipeline & Competence Analysis Specification

**Project**: Top's Academy  
**Component**: Content-to-Course Antigravity Skill (`.agents/skills/course_generator`) & Competence Analysis Pipeline  
**Author**: Specification Miner (Skill & Competence Analysis)  
**Date**: 2026-10-11  
**Status**: Complete Specification  

---

## 1. Executive Summary & Architecture Overview

The purpose of the **Content-to-Course Antigravity Skill** is to provide a fully automated, psychometrically rigorous pipeline that ingests any academic course material (specifically starting with `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf`), decomposes it through formal **Cognitive Task Analysis (CTA)** into a structured taxonomy of competencies, generates a high-volume, Top's Academy-style exercise bank (meeting strict quotas: $\ge 30$ questions per Skill competency, $\ge 20$ per Fact/Concept competency), verifies answer keys independently, validates against the R2 course validator with an iterative repair loop, and publishes the resulting course directly to the practice platform's `courses/` directory.

### 1.1 Architecture & Pipeline Flow

```
+-------------------------------------------------------------------------------+
|                             INPUT: Academic PDF                               |
|            (e.g., sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf)|
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| PHASE 1: Content Extraction & Formula Normalization                           |
| - PyMuPDF / pdfplumber text extraction                                         |
| - Multi-line equation reconstruction & LaTeX token sanitization               |
| - Section & outline chunking (Beamer slides / sections)                       |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| PHASE 2: Cognitive Task Analysis (CTA) Engine                                 |
| - Prompt based on system_prompts/prompt_competence_analyser.md                |
| - Knowledge Triad: Facts [H], Concepts [C], Skills [Hab]                      |
| - Expert Blindness analysis & common exam traps                               |
| - Top's Academy-style Automation Seeds (parameterized micro-drills)            |
| - Output: courses/competence_analysis_<course_id>.md                          |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| PHASE 3: Batch Question Generation Engine                                     |
| - Prompting system based on system_prompts/prompt_creator_exercises.md        |
| - Chunked batching (5-8 items per LLM call) to prevent token truncation       |
| - Exact volume targets: >=30 per Skill [Hab], >=20 per Fact/Concept [H/C]     |
| - 3 Interaction Types: multiple_choice_7_options, fill_in_the_blank,          |
|   multiple_select (4-6 options, 1 to n-1 correct)                             |
| - Anti-Giveaway Engine: per-item length bounds [0.8*min, 1.2*max] &           |
|   course distribution (<=25% longest, <=25% shortest)                         |
| - LaTeX escape protection: strict double-backslash '\\' JSON encoding         |
| - Integrated graph definitions (curves, points, labels)                       |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| PHASE 4: Independent Verification Tier                                        |
| - Tier 1: SymPy Programmatic Solver (symbolic math, roots, traces, diffs)     |
| - Tier 2: Blind Solver LLM Agent (solves stem without answer key)             |
| - Arbitration & reconciliation of discordant answers                         |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| PHASE 5: Automated R2 Validator & Iterative Repair Loop                       |
| - Executes CLI course validator                                               |
| - Syntax, schema, escaped LaTeX, option counts, hint counts, volume quotas,   |
|   anti-giveaway length ratios                                                 |
| - Targeted auto-repair: regex escape sanitizer, length rebalancing prompt,    |
|   shortfall generator. Max 3 iterations.                                      |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| PHASE 6: Course Publication & User Notification                               |
| - Writes final JSON to courses/<course_id>.json                               |
| - Platform auto-discovers and registers course                                |
| - Skill reports course summary, unit counts, question totals, launch command  |
+-------------------------------------------------------------------------------+
                                      |
                                      v
+-------------------------------------------------------------------------------+
| PHASE 7: Verification & Quality Audits                                        |
| - Question Audit: >=40 items sampled, >=95% accuracy threshold                |
| - Blind-Guess Distractor Test: >=40 MC items (no stem), <=30% guess rate      |
+-------------------------------------------------------------------------------+
```

---

## 2. In-Depth Analysis of Input Material (`sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf`)

### 2.1 Document Metadata & Structural Overview
- **File Path**: `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf`
- **Total Pages**: 25 slides
- **Format**: PDF 1.5, compiled with `pdfTeX-1.40.29` using LaTeX `beamer` class
- **Author**: Mgtr. Saúl Elguera (`selguera@iep.org.pe`), Universidad Nacional Mayor de San Marcos (UNMSM), Facultad de Ciencias Económicas
- **Target Course**: Matemática para Economía IV (2026 - II)
- **Primary Language**: Spanish (Castilian academic Spanish)
- **Pedagogical Goal**: Equipping economics students with analytical techniques to model dynamic systems, production functions, and partial differential equations (PDEs / EDPs) of first and second order.

### 2.2 Content & Mathematical Breakdown by Slide Section

| Slide Range | Section Title | Key Theoretical Topics & Mathematical Depth |
|-------------|---------------|---------------------------------------------|
| **1 - 2** | Carátula y Contenido | Portada del curso y agenda temática estructurada en 6 bloques. |
| **3 - 4** | Introducción: Homogeneidad y Euler | Función homogénea de grado $n$: $f(t\mathbf{x}) = t^n f(\mathbf{x})$. Función Cobb-Douglas $F(K, L) = A K^\alpha L^\beta$ de grado $\alpha+\beta$. Teorema de Euler: $\sum_{i=1}^n x_i \frac{\partial f}{\partial x_i} = n f(\mathbf{x})$. Aplicación económica: Agotamiento del producto bajo competencia perfecta ($K F_K + L F_L = (\alpha+\beta)F$). |
| **5 - 7** | Definición, Orden, Grado y Solución | Definición formal de derivadas parciales multi-índice $D^k f$. Definición general de EDP: $F(\mathbf{x}, y, y_1, \dots, y_n, \dots) = 0$. Orden (mayor derivada), grado (potencia de mayor derivada), linealidad vs cuasilinealidad ($a(x,y)u_x + b(x,y)u_y + c(x,y)u = d(x,y)$ vs $u_y + u u_x = 0$). Concepto de solución general y verificación por sustitución directa (ej. $U(x,y) = e^{x-y}$ para $U_x + U_y = 0$). |
| **8 - 9** | Método de Separación de Variables | Supuesto multiplicativo $U(x,y) = f(x)g(y)$. Cálculo de derivadas parciales $U_x = f'g, U_y = fg', U_{xx} = f''g$. Reducción a sistema de EDOs desacopladas acopladas mediante constante de separación $\lambda$. Ejemplo resuelto completo: Ecuación del calor 1D $U_y - 4 U_{xx} = 0$, con bifurcación de regímenes según $\lambda = 0, \lambda > 0, \lambda < 0$. |
| **10** | Método de Características | EDP cuasilineal de primer orden $a(x,y)U_x + b(x,y)U_y = c(x,y)$. Parametrización de curva sobre la superficie integral $x(s), y(s)$. Regla de la cadena: $\frac{dU}{ds} = U_x \frac{dx}{ds} + U_y \frac{dy}{ds}$. Sistema característico: $\frac{dx}{ds} = a(x,y), \frac{dy}{ds} = b(x,y), \frac{dU}{ds} = c(x,y)$. |
| **11 - 18** | Método de Lagrange (EDPs de 1er Orden) | Sistema auxiliar simétrico de Lagrange: $\frac{dx}{a(x,y)} = \frac{dy}{b(x,y)} = \frac{dU}{c(x,y)}$. Deducción de dos integrales primeras independientes $m(x,y,U) = c_1$ y $n(x,y,U) = c_2$. Solución general implícita: $\phi(m, n) = 0$. Verificación por derivación implícita e independencia funcional ($|\nabla \phi| = 0$). 5 Ejemplos canónicos resueltos paso a paso: <br>1. Coeficientes constantes: $3U_x + 2U_y = 5 \implies \phi(2x-3y, 5y-2U) = 0$. <br>2. Variables separables directas: $x U_x + y U_y = U \implies \phi(x/y, y/U) = 0$. <br>3. Multiplicadores de Lagrange: $(x-y)U_x + (U-x)U_y = y-U \implies m=x+y+U, n=xU + y^2/2$. <br>4. Sustitución de primera integral: $x U_x + y U_y = x e^{-U} \implies m=x/y, n=e^U - x$. <br>5. Sumas diferenciales: $x^2 U_x + y^2 U_y = x^2 + y^2 \implies m=\frac{x-y}{xy}, n=x - U + y$. |
| **19 - 20** | EDPs con Condiciones Iniciales (Cauchy) | Problema de Cauchy para EDP cuasilineal: $-y u_x + x u_y = u^2 + 1$ con curva inicial $u(x,0) = x^2$. Parametrización en $t=0, s=m$: $x(0)=m, y(0)=0, u(0)=m^2$. Solución de EDOs: $u(t) = \tan(t+c_1)$, $y(t) = m\sin t$, $x(t) = m\cos t$. Inversión de parámetros $t = \arctan(y/x), m^2 = x^2+y^2$. Solución explícita final: $u(x,y) = \tan\left(\arctan(y/x) + \arctan(x^2+y^2)\right)$. |
| **21 - 24** | EDPs de 2do Orden con Coeficientes Constantes | Forma canónica: $a U_{xx} + b U_{xy} + c U_{yy} = d(x,y)$. Partición en solución complementaria $U_h$ y particular $U_p$. Ensayo homogéneo $U = \phi(y + nx)$ que conduce a la ecuación característica $a n^2 + b n + c = 0$, con discriminante $\Delta = b^2 - 4ac$. <br>- $\Delta > 0$: 2 raíces reales distintas $\implies U_h = f_1(y+n_1 x) + f_2(y+n_2 x)$. <br>- $\Delta = 0$: raíz doble real $\implies U_h = f_1(y+nx) + x f_2(y+nx)$. <br>- $\Delta < 0$: raíces complejas conjugadas $\implies$ soluciones oscilatorias complejas. <br>Solución particular vía descomposición de operadores diferenciales: $(D_x - m_1 D_y)(D_x - m_2 D_y) U = d(x,y)$. Reducción en cascada a dos EDPs de primer orden resolubles por Lagrange. Ejemplo resuelto: $U_{xx} + U_{xy} - 6U_{yy} = x + y$. |
| **25** | Bibliografía | Frank Ayres, *Teoría y Problemas de Ecuaciones Diferenciales*, Serie Schaum, 1979. |

### 2.3 Extraction Feasibility & Mathematical Challenges
1. **PyMuPDF Text Cleanliness**: Text extraction using `fitz.open()` extracts all slide text cleanly with UTF-8 support.
2. **Multi-line Math Splits**: In LaTeX Beamer slides, fractions and operators often span 2 to 3 lines in raw text (e.g. numerator line, line break, denominator line, or operator symbols like $\sum$). The pipeline must use a formula normalization pass to stitch multi-line mathematical terms into standard inline `$formula$` or block `$$formula$$` LaTeX expressions.
3. **Language Consistency**: The input document is 100% in Spanish. Original Request R3 mandates: *"exercise text in the source content's language"*. Therefore, all stems, options, hints, and explanations must be generated in grammatically flawless Spanish.

---

## 3. Cognitive Task Analysis (CTA) Specification

The Cognitive Task Analysis transforms the declarative textbook material into an operational, granular taxonomy of assessable competencies. It adheres to the framework defined in `system_prompts/prompt_competence_analyser.md` and demonstrated in `system_prompts/output_example_competences.md`.

### 3.1 Terminal Macro-Competency
> **Macro-Competencia Terminal Inferida**:  
> Formular, clasificar analíticamente, reducir operacionalmente y resolver con precisión cuantitativa ecuaciones en derivadas parciales de primer y segundo orden (lineales y cuasilineales) aplicadas a modelos económicos y dinámicos, aplicando el Teorema de Euler a funciones homogéneas de producción, ejecutando la separación de variables, resolviendo sistemas característicos de Charpit-Lagrange con multiplicadores algebraicos, deduciendo superficies integrales explícitas ante condiciones iniciales de Cauchy mediante inversión paramétrica, y descomponiendo operadores diferenciales de segundo orden en cascada para aislar componentes homogéneos y particulares.

### 3.2 Granular Competency Taxonomy

#### A. Hechos Requeridos [H] (Facts - Declarative / Identities)
* **[H-01]** `Definición de Homogeneidad e Identidad de Euler`: Una función es homogénea de grado $n$ si $f(t\mathbf{x}) = t^n f(\mathbf{x})$; la identidad de Euler establece $\sum_{i=1}^k x_i \frac{\partial f}{\partial x_i} = n f(\mathbf{x})$.
* **[H-02]** `Taxonomía de Orden, Grado y Cuasilinealidad`: El orden de una EDP es la derivada parcial de mayor orden presente; el grado es el exponente algebraico de dicha derivada una vez eliminados radicales; una EDP es cuasilineal si es lineal en las derivadas de mayor orden con coeficientes que pueden depender de las variables independientes y de la función incógnita.
* **[H-03]** `Identidad de Verificación de Solución`: Una función $U = f(x,y)$ es solución si y solo si al sustituir formalmente sus derivadas parciales en la EDP se reduce a una identidad algebraica en todo su dominio.
* **[H-04]** `Sistema Simétrico Auxiliar de Lagrange`: Para la EDP $a(x,y,u)u_x + b(x,y,u)u_y = c(x,y,u)$, el sistema característico asociado es $\frac{dx}{a} = \frac{dy}{b} = \frac{du}{c}$.
* **[H-05]** `Polinomio Característico y Discriminante de 2do Orden`: Para $a U_{xx} + b U_{xy} + c U_{yy} = d(x,y)$, la ecuación característica es $a n^2 + b n + c = 0$, con discriminante $\Delta = b^2 - 4ac$.
* **[H-06]** `Formas Canónicas Homogéneas según el Signo de Discriminante`:
  - Si $\Delta > 0$ (Hiperbólica): $U_h = f_1(y + n_1 x) + f_2(y + n_2 x)$.
  - Si $\Delta = 0$ (Parabólica): $U_h = f_1(y + n x) + x f_2(y + n x)$.
  - Si $\Delta < 0$ (Elíptica): $U_h = \phi_1(y + (w+vi)x) + \phi_2(y + (w-vi)x)$.
* **[H-07]** `Representación por Operadores Diferenciales`: Notación $D_x \equiv \frac{\partial}{\partial x}$, $D_y \equiv \frac{\partial}{\partial y}$; el operador cuadrático $a D_x^2 + b D_x D_y + c D_y^2$ se factoriza como $(D_x - m_1 D_y)(D_x - m_2 D_y)$.

#### B. Conceptos Estructurales [C] (Concepts - Relational Models & Boundary Conditions)
* **[C-01]** `Interpretación Económica del Teorema de Euler y Agotamiento del Producto`: En mercados competitivos donde los factores reciben su producto marginal ($P_K = F_K, P_L = F_L$), el grado de homogeneidad determina si el pago total a factores agota el producto ($\alpha+\beta=1$, rendimientos constantes a escala), genera déficit ($\alpha+\beta>1$) o deja excedente económico ($\alpha+\beta<1$).
  - *Distinción fina / Trampa común*: Confundir rendimientos constantes a escala con rendimientos marginales decrecientes (los rendimientos a escala dependen de $\alpha+\beta$, mientras que los marginales dependen de cada exponente individual).
* **[C-02]** `Geometría de Curvas Características y Superficies Integrales`: La solución de una EDP cuasilineal es una superficie $U=U(x,y)$ en $\mathbb{R}^3$ formada por una familia uniparamétrica de curvas características tangentes en cada punto al campo vectorial $(a, b, c)$.
  - *Distinción fina / Trampa común*: Creer que las curvas características se cruzan arbitrariamente; en puntos de regularidad forman una foliación de la superficie.
* **[C-03]** `Principio de Separabilidad y el Rol de la Constante de Separación $\lambda$`: El ansatz $U(x,y)=f(x)g(y)$ solo es válido si la EDP permite aislar términos que dependen estrictamente de una sola variable independiente a cada lado de la igualdad, forzando a que ambos lados igualen una constante fija $\lambda$.
  - *Distinción fina / Trampa común*: Asumir que toda EDP es separable; términos cruzados no homogéneos o coeficientes acoplados impiden la separación.
* **[C-04]** `Independencia Funcional de Integrales Primeras`: Para que $\phi(m, n) = 0$ constituya la solución general de Lagrange, los gradientes $\nabla m$ y $\nabla n$ deben ser linealmente independientes (rango jacobiano 2), asegurando que representen superficies no colineales.
  - *Distinción fina / Trampa común*: Seleccionar dos integrales primeras donde una es función trivial de la otra (ej. $n = m^2$).
* **[C-05]** `Condición de No Tangencia en el Problema de Cauchy`: El problema con condición inicial $u(x_0(s), y_0(s)) = u_0(s)$ posee solución única si y solo si la curva inicial no es tangente a las curvas características (determinante de transversales no nulo).
  - *Distinción fina / Trampa común*: Intentar imponer condiciones iniciales a lo largo de una característica, lo que provoca que no haya solución o existan infinitas.
* **[C-06]** `Partición Superposicional y Reducción en Cascada`: La solución completa de una EDP de 2do orden se descompone aditivamente en $U = U_h + U_p$; la solución particular $U_p$ puede obtenerse resolviendo dos EDPs de 1er orden consecutivas desacopladas mediante el operador intermedio $V(x,y)$.

#### C. Habilidades Procedimentales y de Decisión [Hab] (Skills - Observable Actions)
* **[Hab-01]** `Cálculo de Grados de Homogeneidad y Aplicación de Euler`: Evaluar formalmente $f(t\mathbf{x})$, simplificar potencias para deducir el grado $n$, y computar la suma ponderada de derivadas parciales multiplicadas por sus coordenadas.
* **[Hab-02]** `Verificación Operativa de Soluciones Candidatas`: Calcular derivadas parciales sucesivas mediante regla de la cadena y producto, sustituir en el operador diferencial de la EDP y simplificar algebraicamente hasta demostrar la anulación exacta.
* **[Hab-03]** `Desacoplamiento por Separación de Variables en EDPs Físico-Económicas`: Proponer $U=fg$, calcular derivadas, agrupar cocientes $\frac{f''}{f}$ y $\frac{g'}{g}$, igualar a la constante $\lambda$ y resolver los regímenes ordinarios resultantes según el signo de $\lambda$.
* **[Hab-04]** `Integración Directa del Sistema Auxiliar de Lagrange`: Formular el sistema simétrico $\frac{dx}{a}=\frac{dy}{b}=\frac{du}{c}$, seleccionar pares de fracciones con variables separables, e integrar analíticamente para obtener integrales primeras $m(x,y,u)=c_1$ y $n(x,y,u)=c_2$.
* **[Hab-05]** `Construcción de Integrales Primeras mediante Multiplicadores de Lagrange`: Determinar multiplicadores algebraicos $(\alpha_1, \alpha_2, \alpha_3)$ tales que $\alpha_1 a + \alpha_2 b + \alpha_3 c = 0$, integrando la forma diferencial exacta resultante $\alpha_1 dx + \alpha_2 dy + \alpha_3 du = 0$.
* **[Hab-06]** `Resolución del Problema de Cauchy e Inversión Paramétrica`: Parametrizar la curva inicial en función de un parámetro $m$ en $t=0$, resolver las EDOs para $x(t), y(t), u(t)$, despejar analíticamente los parámetros libres $t$ y $m$ en términos de $(x,y)$, y sustituirlos en $u$ para aislar la solución explícita $u(x,y)$.
* **[Hab-07]** `Cálculo Espectral y Ensamblado de la Solución Homogénea de 2do Orden`: Sustituir el ansatz $U=\phi(y+nx)$, resolver la ecuación cuadrática característica $an^2+bn+c=0$, evaluar el discriminante $\Delta$ y escribir la combinación lineal canónica correspondiente.
* **[Hab-08]** `Determinación de la Solución Particular vía Factorización de Operadores`: Factorizar el polinomio en operadores diferenciales $(D_x - r_1 D_y)(D_x - r_2 D_y)U = d(x,y)$, definir la variable intermedia $V(x,y)$, resolver la primera EDP de 1er orden para $V$ por Lagrange, y luego resolver la segunda EDP para $U$.

### 3.3 Expert Blindness (Ceguera del Experto)

| Paso Implícito / Trampa | Por qué el texto teórico lo omite | Impacto si el alumno no lo domina |
|-------------------------|-----------------------------------|-----------------------------------|
| **Pérdida de la constante de integración como función arbitraria**: en EDOs se añaden escalares $c_1$; en EDPs las constantes de integración son funciones arbitrarias de la otra variable (ej. $\int u_x dx = U + \phi(y)$). | El profesor considera obvio el concepto de cálculo multivariable. | El alumno confunde la solución general con una familia uniparamétrica de curvas en vez de una familia infinita de superficies, invalidando el resultado. |
| **Omisión de división por coeficientes al reordenar la ecuación característica de 2do orden**: al asumir $U = \phi(y + nx)$, la derivada con respecto a $x$ aporta el factor $n$, conduciendo a $an^2 + bn + c = 0$; si se asume $\phi(x + my)$, la ecuación es $a + bm + cm^2 = 0$. | Se sobreentiende la simetría de la sustitución sin explicitar qué variable se pondera. | El estudiante invierte las raíces $n$ con $1/n$ y coloca coeficientes erróneos en los argumentos de las funciones arbitrarias. |
| **Elección incorrecta de multiplicadores en Lagrange**: suponer que cualquier combinación sirve sin verificar que el denominador sume rigurosamente cero. | Los textos exhiben los multiplicadores ya encontrados como un truco ingenioso. | El alumno intenta integrar expresiones diferenciales que no son cerradas ni exactas, bloqueándose en integrales no elementales. |
| **Singularidades al despejar parámetros en el problema de Cauchy**: despejar $t = \arctan(y/x)$ asumiendo implícitamente $x \neq 0$ y cuadrantes específicos. | Se prioriza la obtención de la fórmula cerrada sin discutir ramas algebraicas o dominios restringidos. | Respuestas discontinuas en exámenes o pérdida de ramas válidas de la solución. |
| **Confusión entre la solución particular $U_p$ y la general $U = U_h + U_p$**: olvidar que la factorización de operadores resuelve únicamente $U_p$ y que la solución completa requiere agregar las funciones arbitrarias de la parte homogénea. | El autor se concentra en el cálculo pesado del operador y asume que el alumno sumará $U_h$ al final. | Pérdida de la mitad del puntaje en evaluaciones formales por entregar únicamente una solución particular. |
| **Olvidar sustituir la primera integral en la segunda ecuación del sistema de Lagrange**: cuando el tercer término contiene variables no separables directamente con el primero. | Se considera un paso obvio de sustitución algebraica elemental. | El alumno declara que la ecuación "no tiene solución separable" al ver variables cruzadas. |

### 3.4 Semillas de Automatización y Fluidez (Estilo Top's Academy)

| ID Habilidad | Micro-Competencia a Automatizar | Tipo de Ejercicio Mecánico Sugerido | Parámetros que deben variar aleatoriamente |
|--------------|--------------------------------|-------------------------------------|--------------------------------------------|
| **Hab-01** | Grado de funciones Cobb-Douglas y derivadas de Euler | Entrada Numérica directa del grado $n$ o valor monetario de $K F_K + L F_L$ | Parámetros $\alpha, \beta \in (0, 2)$, $A \in [1, 10]$, valores de capital y trabajo |
| **Hab-02** | Verificación rápida de soluciones en $U_x \pm k U_y = 0$ | Opción Múltiple (7 opciones): ¿Cuál de las siguientes 7 funciones es solución? | Formas funcionales: $e^{ax+by}$, $\sin(ax+by)$, $\ln(ax+by)$, coeficientes $a, b \in [-5, 5]$ |
| **Hab-03** | Cálculo de la constante de separación $\lambda$ en ecuaciones de calor | Respuesta Numérica / Selección Múltiple de las EDOs desacopladas | Coeficiente de difusión $\kappa \in \{1, 2, 4, 9, 16\}$, signo de $\lambda$ |
| **Hab-04** | Integración del primer par del sistema de Lagrange $\frac{dx}{a} = \frac{dy}{b}$ | Expresión algebraica en LaTeX de la primera integral $m(x,y) = c_1$ | Coeficientes enteros $a, b \in [-8, 8]$, lineales $x, y$ |
| **Hab-05** | Identificación de multiplicadores nulos en Lagrange | Selección Múltiple (Checkboxes): Seleccionar la terna $(\alpha_1, \alpha_2, \alpha_3)$ que anula $\sum \alpha_i P_i$ | EDPs canónicas con variables rotacionales $(x-y, y-u, u-x)$ |
| **Hab-06** | Parametrización en $t=0$ para condiciones de Cauchy | Entrada directa de las condiciones $x(0), y(0), u(0)$ en términos de $m$ | Curvas iniciales: rectas $y=0$, parábolas $u(x,0)=k x^2$, exponenciales |
| **Hab-07** | Raíces características y clasificación de EDPs de 2do orden | Clasificación rápida: ¿Hiperbólica, Parabólica o Elíptica? | Coeficientes $a, b, c \in [-10, 10]$ con $\Delta$ positivo, cero o negativo |
| **Hab-08** | Factorización de operadores diferenciales $D_x^2 + b D_x D_y + c D_y^2$ | Entrada algebraica de las raíces $m_1, m_2$ en $(D_x - m_1 D_y)(D_x - m_2 D_y)$ | Coeficientes factorizables con enteros sencillos (ej. $-6, +5, -4$) |

---

## 4. Exercise Generation Pipeline & Volume Strategy

### 4.1 Strict Quotas & Capacity Planning
Original Request R2 & R3 mandates:
- **Skill [Hab] competencies**: $\ge 30$ questions each.
- **Fact [H] / Concept [C] competencies**: $\ge 20$ questions each.

For our 8 Skills, 7 Facts, and 6 Concepts:
- 8 Skills $\times 30$ = 240 questions
- 7 Facts $\times 20$ = 140 questions
- 6 Concepts $\times 20$ = 120 questions
- **Total Course Bank = 500 questions**!

For a focused high-density initial deployment (or when selecting a core subset for demonstration):
- If the course is scoped to 3 Skills + 2 Concepts + 2 Facts (7 units):
  $3 \times 30 + 4 \times 20 = 170$ questions.
- Regardless of scope, the skill generator must handle any arbitrary number of competencies without hitting context window or rate limits.

### 4.2 The Batching Architecture (Solving LLM Context & Truncation Bottlenecks)
A single LLM invocation cannot generate 150 to 500 rich mathematical items without truncating or corrupting JSON syntax. The skill pipeline implements a **Deterministic Batching Engine**:

```
[Master CTA Taxonomy]
         │
         ▼
[Competency Work Queue]  --> (Iterates one competency at a time)
         │
         ├── Competency C-01 (Target: 20 items)
         │       ├── Batch 1 (Items 1-7):   3 MC7, 2 FIB, 2 MS (Easy/Med)
         │       ├── Batch 2 (Items 8-14):  2 MC7, 3 FIB, 2 MS (Med)
         │       └── Batch 3 (Items 15-20): 2 MC7, 2 FIB, 2 MS (Hard)
         │
         ├── Competency Hab-04 (Target: 30 items)
         │       ├── Batch 1 (Items 1-8):   3 MC7, 3 FIB, 2 MS
         │       ├── Batch 2 (Items 9-16):  3 MC7, 3 FIB, 2 MS
         │       ├── Batch 3 (Items 17-24): 3 MC7, 2 FIB, 3 MS
         │       └── Batch 4 (Items 25-30): 2 MC7, 2 FIB, 2 MS
         │
         └── (Repeat for all competencies)
                 │
                 ▼
     [Batch JSON Validator & Sanitizer]
                 │
                 ▼
     [Course Bank Aggregator & ID Unifier]
```

#### Batch Engine Specification:
1. **Batch Size**: 6 to 8 questions per LLM generation call.
2. **Batch Prompt Input**:
   - Relevant excerpts of theoretical slides.
   - Specific Competency CTA definition + Expert Blindness notes.
   - Generation parameters: target difficulty distribution, interaction type counts, and unique ID prefix (e.g. `Q-HAB04-B1-001`).
3. **Batch Output Validation**:
   - Each batch is parsed and validated independently immediately upon return.
   - If a batch fails JSON parsing or LaTeX escape checks, only that 6-8 item batch is re-prompted (not the whole course).
4. **Course Assembly**:
   - The aggregator concatenates valid batches, checks global uniqueness of IDs, and validates overall course quotas.

### 4.3 Anti-Giveaway Rules & Psychometric Engineering

Standard LLM exercise generators produce obvious giveaways: the correct option is often the longest, includes elaborate rationales while distractors are blunt, or uses hedged wording. The skill implements strict psychometric safeguards:

#### Rule 1: Per-Item Length Bounding (Hard Validator Enforced)
For every `multiple_choice_7_options` question:
Let $L_{\text{correct}}$ be the character length of the correct option's content.
Let $D = \{L(d_1), L(d_2), \dots, L(d_6)\}$ be the character lengths of the 6 distractors.
$$\min(D) \times 0.80 \le L_{\text{correct}} \le \max(D) \times 1.20$$
*Violation behavior*: Rejected immediately if $L_{\text{correct}} > 1.20 \times \max(D)$ or $L_{\text{correct}} < 0.80 \times \min(D)$.

#### Rule 2: Course-Level Length Distribution (Hard Validator Enforced)
Across all multiple-choice items in the course:
- The correct option must **NOT** be the strictly longest (or tied for longest) in more than **25%** of items:
  $$\frac{\sum [L_{\text{correct}} \ge \max(D)]}{N_{\text{MC}}} \le 0.25$$
- The correct option must **NOT** be the strictly shortest (or tied for shortest) in more than **25%** of items:
  $$\frac{\sum [L_{\text{correct}} \le \min(D)]}{N_{\text{MC}}} \le 0.25$$

#### Rule 3: Syntactic & Justification Symmetry (Prompt Enforced)
- **Zero Asymmetric Rationales**: If the correct answer includes an explanation (e.g., "... porque $\text{tr}(A) < 0$"), **ALL 6 distractors must include a plausible, grammatically matched rationale** (e.g., "... debido a que el determinante es nulo"). Conversely, if distractors are concise, the correct answer must be equally concise.
- **Grammatical Parallelism**: All 7 options must start with identical grammatical forms (all nouns, all full sentences, or all mathematical clauses).
- **Prohibition of Qualifier Cues**: Distractors must never be loaded with absolutist words ("siempre", "nunca", "en cualquier caso") while the correct option uses hedged words ("frecuentemente", "bajo ciertas condiciones").

#### Rule 4: Misconception-Grounded Distractor Construction
Distractors must not be random noise. They must be constructed by applying genuine mathematical misconceptions from the CTA:
- Applying Euler's theorem without verifying homogeneity.
- Reversing signs in the characteristic polynomial ($n = \frac{b \pm \sqrt{\Delta}}{2a}$ instead of $-b$).
- Forgetting the Jacobian determinant factor in transformation of variables.
- Treating Cauchy parameters as linear instead of solving trigonometric relations ($x^2+y^2=m^2$).

### 4.4 Interaction Types Distribution & Formatting

1. **`multiple_choice_7_options`**:
   - Exactly 7 options (`A`, `B`, `C`, `D`, `E`, `F`, `G`).
   - Exactly 1 option with `is_correct: true`.
   - Correct position randomized uniformly across `A` through `G`.
2. **`fill_in_the_blank`**:
   - `options: []` (empty array).
   - `correct_answer.value`: Canonical LaTeX or numeric string.
   - `correct_answer.accepted_equivalents`: Array of mathematically equivalent forms (e.g. `["1 - (alpha + n)*sigma", "1 - \\alpha\\sigma - n\\sigma", "1 - (\\alpha + n)\\sigma"]`).
   - Clear input instructions and placeholder.
3. **`multiple_select`**:
   - 4 to 6 options.
   - Cardinality constraint: between 1 and $n-1$ options must be correct (never 0, never all $n$).
   - `correct_answer.value`: Array of correct option IDs, e.g. `["A", "C", "D"]`.
   - Binary all-or-nothing grading policy.

### 4.5 Embedded Graph Specification
The practice platform renders graphs specified in question JSON. The generator incorporates graph objects for relevant geometric concepts (characteristics, Cauchy trajectories):

```json
"graph": {
  "type": "function_plot",
  "x_axis": { "label": "x", "domain": [-5, 5] },
  "y_axis": { "label": "y", "domain": [-5, 5] },
  "curves": [
    { "fn": "sqrt(4 - x^2)", "domain": [-2, 2], "style": "solid", "color": "#1a73e8" },
    { "fn": "-sqrt(4 - x^2)", "domain": [-2, 2], "style": "solid", "color": "#1a73e8" }
  ],
  "points": [
    { "x": 0, "y": 0, "label": "Origen", "type": "closed" }
  ]
}
```

---

## 5. Independent Verification Step for Answer Keys

To guarantee $\ge 95\%$ accuracy on all generated questions without circular LLM self-bias, the pipeline incorporates an **Independent Verification Step** decoupled from the generator:

### 5.1 Verification Architecture

```
Generated Question Candidate
            │
            ├─────────────────────────────────────────┐
            ▼                                         ▼
   [Tier 1: SymPy Solver]                  [Tier 2: Blind LLM Solver]
  - Solves algebraic relations            - Receives ONLY stem & options
  - Verifies characteristic roots         - NO access to correct_answer,
  - Verifies homogeneity degrees            hints, or solution
  - Checks differential operators         - Returns independent answer
            │                                         │
            └────────────────────┬────────────────────┘
                                 │
                                 ▼
                    [Arbitration Controller]
                                 │
      ┌──────────────────────────┴──────────────────────────┐
   [MATCH]                                              [DISCORDANCE]
   Question approved                                    Item flagged ->
   for Course Bank                                      Auto-repair / Regenerate
```

### 5.2 Verification Protocols
1. **Tier 1 (SymPy Programmatic Verifier)**:
   - For `fill_in_the_blank` with algebraic or numeric expressions: SymPy parses the student/correct answer and tests mathematical equivalence using `sympy.simplify(expr1 - expr2) == 0`.
   - For 2nd-order characteristic roots: SymPy computes roots of $a n^2 + b n + c = 0$ and verifies they match `correct_answer.value`.
   - For homogeneity: SymPy verifies $f(t x_1, t x_2) == t^n f(x_1, x_2)$.
2. **Tier 2 (Blind LLM Solver Agent)**:
   - Prompt provides: `stem`, `context_application`, and options (for MC/MS).
   - Explicitly withholds: `correct_answer`, `hints`, `detailed_solution`, and `error_rationale`.
   - Solves the problem from first principles and outputs its independent solution.
   - If the blind solver's answer agrees with the generator's `correct_answer`, confidence is verified.
   - If they disagree: A specialized *Mathematical Arbitrator* inspects both derivations and picks the correct answer or triggers question regeneration.

---

## 6. Automated R2 Validator Integration & Iterative Repair Loop

### 6.1 R2 Validator Rules Checklist
The skill calls the platform's validator CLI (e.g. `npm run validate -- courses/<course_id>.json` or `python -m validator courses/<course_id>.json`). The validator checks 11 immutable criteria:

1. **Valid JSON**: Strict parse without syntax errors.
2. **LaTeX Escape Integrity**: All backslashes in mathematical formulas escaped as `\\`. No silent control characters (`\t`, `\n`, `\f`, `\r`, `\b`, `\u`) corrupting LaTeX macros.
3. **Schema Compliance**: Course metadata, competency definitions, valid question structures.
4. **Multiple-Choice 7 Options**: Exactly 7 options, exactly 1 with `is_correct: true`.
5. **Multiple-Select Cardinality**: 4 to 6 options, correct count between 1 and $n-1$.
6. **Fill-in-the-Blank Options**: Empty options array `[]`, non-empty canonical answer, valid `accepted_equivalents`.
7. **Scaffolding Hints**: Between 3 and 5 progressive hints per question ($3 \le \text{count} \le 5$).
8. **Unique Identifiers**: All `id` fields unique across the course.
9. **Valid Competency References**: Every `competency_ref.id` matches an existing unit in the course metadata.
10. **Volume Quotas**: $\ge 30$ questions per Skill [Hab] competency; $\ge 20$ questions per Fact [H] / Concept [C] competency.
11. **Anti-Giveaway Length Rules**:
    - Item-level: $0.80 \times \min(D) \le L_{\text{correct}} \le 1.20 \times \max(D)$.
    - Course-level: Correct option $\le 25\%$ longest and $\le 25\%$ shortest across all MC items.

### 6.2 Iterative Repair State Machine

```
      +------------------------+
      | Course JSON Generated  |
      +------------------------+
                  │
                  ▼
      +------------------------+
      |  Run R2 Validator CLI  |
      +------------------------+
                  │
         ┌────────┴────────┐
         │ Exits 0?        │
         ├─────────────────┤
         │ YES             │ NO (Error JSON output)
         ▼                 ▼
   +-----------+    +-------------------------------------+
   | Published |    | Classify Errors & Route to Fixers:  |
   +-----------+    | 1. LaTeX Escapes: Regex sanitizer   |
                    | 2. Length Bounds: Targeted rewrite  |
                    | 3. Quota Shortfall: Batch generator |
                    | 4. Hint Count: Prompt padder/pruner |
                    +-------------------------------------+
                                   │
                                   ▼
                    +-------------------------------------+
                    | Apply Fix & Increment Iteration (<=3)|
                    +-------------------------------------+
```

#### Specialized Repair Modules:
- **Module A: Regex LaTeX Sanitizer**:
  Scans all string values in the JSON. If a single backslash is followed by standard LaTeX command letters (`alpha`, `beta`, `frac`, `text`, `det`, `partial`), it replaces it with `\\`. If a control character (such as `\t` from `\text` or `\f` from `\frac`) is detected, it restores the intended LaTeX command string `\\text` or `\\frac`.
- **Module B: Option Length Rebalancer**:
  If question $Q$ violates the 20% length bound, a targeted prompt receives the stem and the 7 options, calculates the target character length interval $[L_{\min}, L_{\max}]$, and instructs the LLM to rewrite the options to fall strictly within that interval without altering the mathematical meaning.
- **Module C: Targeted Shortfall Generator**:
  If competency `Hab-03` has only 28 questions, the pipeline launches an atomic mini-batch to generate the exact missing 2 questions and appends them to the bank.

---

## 7. Course Publication Protocol

1. **Target Destination**: The validated course file is saved to the practice platform's designated course directory:
   `g:\Mi unidad\Competence_analyser\courses\<course_id>.json`
   (e.g., `courses/ecuaciones_derivadas_parciales.json`).
2. **Auto-Discovery**: The web practice platform dynamically monitors or scans `courses/*.json` upon server start or client reload. No web app code changes or recompilations are needed.
3. **Execution Summary & Handoff**: Upon publication, the skill prints a clear summary:
   - Course Title and Course ID.
   - Total Competencies/Units breakdown by type (Skills, Concepts, Facts).
   - Total Question count by interaction type (MC7, FIB, MS).
   - Confirmation of 100% R2 validator pass.
   - Exact command and browser URL to start practicing immediately:
     `npm start` -> `http://localhost:3000/#/course/ecuaciones_derivadas_parciales`.

---

## 8. Quality Audit Methodology

Per ORIGINAL_REQUEST.md Acceptance Criteria, the skill must be verified through two rigorous, independent psychometric audits:

### 8.1 Question Audit Protocol ($\ge 40$ questions, $\ge 95\%$ accuracy)
- **Sampling Strategy**:
  - Sample $\ge 40$ questions randomly across all competencies in the published course.
  - Stratified sample: At least 15 MC7, 15 FIB, 10 MS items, spanning Easy, Medium, and Hard difficulties.
- **Independent Auditor Agent**:
  - An independent auditor agent (separate from the generator) reviews each sampled item against the source PDF and CTA taxonomy.
- **Audit Rubric**:
  1. *Mathematical & Factual Correctness*: Is the designated correct answer 100% mathematically correct?
  2. *Distractor & Hint Coherence*: Are all distractors genuinely incorrect for the explained reasons? Do hints guide progressively without logical leaps?
  3. *Competency Mapping*: Does the item directly evaluate the tagged competency?
  4. *Formatting & LaTeX*: Is LaTeX rendering cleanly without raw broken tokens?
- **Pass Threshold**: $\ge 95\%$ (at least 38 of 40 items) must receive a flawless score. Every flawed question detected during audit must be corrected in the course JSON.

### 8.2 Blind-Guess Distractor Test Protocol ($\ge 40$ MC items, $\le 30\%$ guess rate)
- **Purpose**: Prove that multiple-choice options cannot be guessed by superficial test-wiseness cues (length, grammatical hints, outlier formatting).
- **Sampling Strategy**:
  - Sample $\ge 40$ `multiple_choice_7_options` questions at random from the course bank.
- **Blindfold Protocol**:
  - The test harness strips the question stem, the competency reference, hints, solutions, and misconception warnings.
  - The 7 options are stripped of their existing letter labels (`A` through `G`) and randomly shuffled.
  - Only the 7 bare option strings are presented to an independent LLM agent.
- **Solver Prompt**:
  > *"Analyze the following 7 response options. You are not given the question. Based solely on formatting, option length, grammatical clues, specificity, or test construction patterns, guess which option is the intended correct answer."*
- **Mathematical Analysis of Chance**:
  - With 7 options, pure chance guess rate is $\frac{1}{7} \approx 14.28\%$.
- **Acceptance Threshold**:
  - Correct guess rate must be **$\le 30\%$** (at most 12 out of 40 guessed correctly).
- **Remediation Loop**:
  - For every item correctly guessed by the blind solver, the harness investigates the cue (e.g. was it the most specific? did it have qualifying clauses?).
  - The item options are rewritten to eliminate the cue, and the blind test is repeated until the $\le 30\%$ threshold is met.

---

## 9. Converting `output_example_exercises.json` into a Valid Demo Course

The file `system_prompts/output_example_exercises.json` currently has critical issues identified during inspection:

### 9.1 Defect Inventory of `output_example_exercises.json`
1. **JSON Syntax Failure (Unescaped LaTeX Backslashes)**:
   - Line 19 contains `\Delta = [\text{tr}(A)]^2 - 4\det(A) < 0`. In standard JSON, `\D` is an illegal escape, causing `JSONDecodeError`.
   - Macros like `\text`, `\frac`, `\nu` silently convert into control characters (tab `\t`, formfeed `\f`, newline `\n`).
2. **Answer-Length Giveaways**:
   - In Question 1 (`Q-HAB03-ISLM-001`): Correct option `C` is 157 characters (the longest by 13.8%), and is the *only* option providing a full justification (`porque tr(A) < 0, det(A) > 0 y Delta < 0`).
   - In Question 4 (`Q-HAB06-SOLOW-004`): Correct option `E` is 181 characters (longest by 10.4%).
   - In Question 7 (`Q-HAB04-EIG-007`): Correct option `B` is tied for shortest.
   - Result: Correct answer is longest in $2/3 = 66.7\%$ of MC items (violating the $\le 25\%$ course rule).
3. **Volume Shortfall**:
   - Total questions in file = 7. R2 validator mandates $\ge 30$ per Skill and $\ge 20$ per Fact/Concept.

### 9.2 Step-by-Step Conversion Strategy
1. **Sanitize Syntax**: Run Python/Node script to escape all backslashes (`\` $\to$ `\\`) and convert control characters back to LaTeX tokens.
2. **Rebalance Options**: Strip justifications from correct options or add parallel justifications to all distractors so lengths match within $\pm 10\%$.
3. **Expand Question Bank**: Using the batch generator with `system_prompts/output_example_competences.md`, generate additional questions for each unit until reaching $\ge 30$ for Skills (`Hab-02`, `Hab-03`, `Hab-04`, `Hab-05`, `Hab-06`, `Hab-07`) and $\ge 20$ for Concepts/Facts.
4. **Validate & Publish**: Run the R2 validator to verify exit code 0, and save as `courses/demo_sistemas_edos.json`.

---

## 10. Antigravity Skill Definition (`SKILL.md`)

Below is the complete specification for the skill file to be created in `.agents/skills/course_generator/SKILL.md`:

```markdown
---
name: course_generator
description: End-to-end skill to analyze course PDF documents, extract competencies via Cognitive Task Analysis, generate Top's Academy-style practice banks (>=30 per Skill, >=20 per Fact/Concept) with anti-giveaway rules and LaTeX validation, verify answer keys independently, validate via R2 validator, and publish to the local practice platform.
triggers:
  - "create course from pdf"
  - "generate Top's Academy course"
  - "analyze competencies"
  - "publish course"
---

# Content-to-Course Generator Skill

When invoked with a PDF document:
1. Run extraction script to extract plain text and structural formulas.
2. Execute Cognitive Task Analysis (CTA) following the prompt in system_prompts/prompt_competence_analyser.md and save the analysis markdown to courses/competence_analysis_<course_id>.md.
3. Run the batch generator engine to generate >=30 questions per Skill [Hab] competency and >=20 per Fact/Concept competency across all 3 interaction types.
4. Run independent verification (SymPy + Blind Solver) to confirm answer keys.
5. Execute the R2 validator CLI. If errors are reported, run the iterative repair loop until exit code is 0.
6. Publish the course JSON to courses/<course_id>.json.
7. Print the course summary and launch instructions for the user.
```

---

## Features Discovered

| # | Category | Feature | Description | Inputs | Outputs | Error Behavior | Discovered Via |
|---|----------|---------|-------------|--------|---------|----------------|----------------|
| 1 | Content Extraction | PyMuPDF Text & Math Extractor | Extracts full text and outline from Beamer slides; handles UTF-8 characters and multi-line equations. | Course PDF file path | Clean text dump and slide outline | Throws FileNotFoundError if PDF missing | `sample_content/I__Ecuaciones_en_derivadas_parciales_2026.pdf` probing |
| 2 | CTA Engine | Knowledge Triad Decomposition | Categorizes domain into Facts [H], Concepts [C], and Skills [Hab]. | Extracted PDF text | Structured Markdown taxonomy | Re-prompts if taxonomy missing categories | `system_prompts/prompt_competence_analyser.md` |
| 3 | CTA Engine | Expert Blindness Catalog | Uncovers omitted operations, hidden algebraic assumptions, and typical exam pitfalls. | Extracted PDF theory | Expert Blindness markdown table | Defaults to standard algebraic traps if none found | `system_prompts/output_example_competences.md` |
| 4 | CTA Engine | Khan-Style Automation Seeds | Identifies high-frequency procedural sub-tasks for fluency drills. | CTA Skills breakdown | Automation Seeds matrix with parametric variations | Flags missing parameter ranges | `prompt_competence_analyser.md` |
| 5 | Exercise Generation | Chunked Batch Orchestrator | Splits question generation into 5-8 question batches to prevent LLM output token truncation. | Competency taxonomy, target counts | Discrete batch JSON objects | Retries individual batch on syntax error | R3 volume requirements analysis |
| 6 | Exercise Generation | 7-Option Multiple Choice Engine | Generates MC items with exactly 7 options and 1 correct answer, randomly placed across A-G. | Competency spec, context, stem | MC7 JSON item with 6 distractors | Re-generates if option count != 7 | `prompt_creator_exercises.md` & R2 spec |
| 7 | Exercise Generation | Fill-in-the-Blank with Algebraic Equivalents | Generates open input questions with canonical answer and accepted equivalent LaTeX variants. | Problem stem, target variable | FIB JSON item with empty options `[]` | Fails R2 if options array not empty | `prompt_creator_exercises.md` & R2 spec |
| 8 | Exercise Generation | Multiple-Select with Cardinality Bounds | Generates 4-6 statements where between 1 and $n-1$ are correct; binary grading. | Multi-property statement stem | MS JSON item with correct array `['A', 'C']` | Re-generates if 0 or all $n$ are correct | R2 validator rules |
| 9 | Psychometric QA | Per-Item Anti-Giveaway Length Bounding | Enforces correct option character length within $[0.8\min(D), 1.2\max(D)]$. | Item options list | Pass/Fail boolean flag | Triggers option length rebalancer | ORIGINAL_REQUEST.md R2 rule |
| 10 | Psychometric QA | Course-Level Length Distribution Check | Enforces correct option is longest in $\le 25\%$ and shortest in $\le 25\%$ across all MC items. | Entire course question bank | Course distribution statistics | Fails R2 validation; prompts option rebalancing | ORIGINAL_REQUEST.md R2 rule |
| 11 | Psychometric QA | Homogeneous Distractor Justification | Ensures all 7 options carry matching rationales or none carry rationales; eliminates give-away justifications. | Option content generator | Parallel option strings | Strips asymmetric justifications | Inspection of `output_example_exercises.json` |
| 12 | LaTeX Integrity | JSON Backslash Escaping & Control Character Sanitizer | Ensures all LaTeX backslashes are double-escaped `\\` and recovers corrupted control characters (`\t`, `\n`, `\f`). | Raw JSON string | Strictly valid JSON string | Emits parse error if unrecoverable | Inspection of `output_example_exercises.json` |
| 13 | Verification | SymPy Programmatic Solver Tier | Verifies mathematical expressions, characteristic roots, and Euler homogeneity using symbolic math. | Math equations / answers | Boolean equivalence confirmation | Flags item for LLM arbitration if solver errors | SymPy 1.13.1 environment check |
| 14 | Verification | Blind LLM Solver Tier | Independent LLM solves stem without access to answer key, hints, or solution. | Stem, context, interaction type | Blind solver answer value | Flags item if mismatch with generator key | Skill Acceptance Criteria (R3/R4) |
| 15 | Validation | Automated R2 Validator Loop | Runs CLI course validator and loops with targeted repair modules (max 3 tries). | Course JSON file | Validator exit code (0 or error report) | Halts after 3 iterations with diagnostic log | ORIGINAL_REQUEST.md R2 & Acceptance Criteria |
| 16 | Publication | Dynamic Course Publishing | Saves validated course to `courses/<course_id>.json` for immediate discovery by web app. | Validated course JSON | File on disk, console launch message | Writes error to stderr if directory unwritable | ORIGINAL_REQUEST.md R1 & R3 |
| 17 | Quality Audit | 40-Question Stratified Audit | Randomly samples $\ge 40$ questions and audits correctness against PDF and CTA ($\ge 95\%$ pass). | Course JSON, source PDF | Audit report with accuracy % | Auto-fixes any identified defective items | Skill Acceptance Criteria |
| 18 | Quality Audit | Blind-Guess Distractor Audit | Samples $\ge 40$ MC items without stem/hints and tests if blind guess rate $\le 30\%$. | Bare option sets (shuffled) | Guess accuracy percentage | Rewrites options of guessed items | Skill Acceptance Criteria |

---

## Edge Cases

| # | Feature | Input | Observed Behavior | Remediation / Design Handling |
|---|---------|-------|-------------------|-------------------------------|
| 1 | LaTeX Escaping | LaTeX macro `\text{tr}(A)` or `\frac{a}{b}` in raw JSON string | Python/Node JSON parser sees `\t` as tab and `\f` as formfeed; invalid escape like `\Delta` throws `JSONDecodeError`. | Pre-pass regex string sanitizer replaces `\command` with `\\command` and decodes escaped control characters before JSON parsing. |
| 2 | Anti-Giveaway Rule | Mathematical formulas naturally differing in length (e.g. `\lambda=0` vs `\lambda=\frac{-b\pm\sqrt{b^2-4ac}}{2a}`) | Correct option could easily exceed 120% of the shortest distractor length if distractors are trivial numbers. | Generator must make distractors structurally symmetric: if correct answer is a quadratic formula, all distractors must be full quadratic expressions with alternate signs or constants. |
| 3 | Multiple-Select Grading | Student selects 2 of 3 correct options in a 5-option question | All-or-nothing grading rule means question is marked incorrect (score 0). | Stems must clearly state "Selecciona todas las opciones correctas"; feedback explicitly highlights which options were missed. |
| 4 | Fill-in-the-Blank Equivalence | Algebraic answers with varied notation: `1 - (alpha+n)*sigma` vs `1 - \alpha\sigma - n\sigma` vs `1 - \sigma(\alpha + n)` | Simple string comparison would falsely mark valid mathematical answers wrong. | Platform grader and validation engine use SymPy / math.js algebraic simplification to test `simplify(user_ans - correct_ans) == 0`. |
| 5 | Token Window Exhaustion | Attempting to generate 30 questions for `Hab-01` in a single LLM prompt | Response gets cut off at token limit (e.g. 4096 tokens), leaving dangling JSON brackets and invalid syntax. | Strict batching: generate in chunks of 6-8 questions per prompt and merge incrementally. |
| 6 | Cauchy Initial Conditions | Boundary curve tangent to characteristics ($x_0'(s) b - y_0'(s) a = 0$) | Cauchy problem has zero or infinite solutions (non-transverse boundary). | In CTA Concept [C-05], explicitly flag non-transversality as an expert trap and design MS items testing this boundary condition. |
| 7 | Repeated Roots ($\Delta = 0$) | 2nd-order characteristic equation $an^2 + bn + c = 0$ with single root $n$ | Standard linear combination $f_1(y+nx) + f_2(y+nx)$ collapses to a single function without independent second basis. | Enforce in Fact [H-06] that second term must contain the multiplier $x$: $U_h = f_1(y+nx) + x f_2(y+nx)$; generate distractors that omit $x$. |
| 8 | Complex Conjugate Roots ($\Delta < 0$) | 2nd-order characteristic roots $w \pm vi$ | Direct substitution yields complex arguments in arbitrary functions. | Include in Fact [H-06] and Skill [Hab-07] canonical real-variable formulations and test recognition of hyperbolic vs elliptic behaviors. |
| 9 | Large Course Scaling | 15+ competencies requiring 450+ questions total | Long generation runtime, potential network drops or rate limits. | Persistent batch checkpointing: save each completed batch to a staging folder (`.cache/course_gen/`), allowing resumable runs. |
