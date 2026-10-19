# Cognitive Task Analysis (CTA): Practica Parcial Saul Standard Coarse

- **Course ID:** `practica_parcial_saul_standard_coarse`
- **Macro-Competency:** Dominio y aplicación analítica integral de Practica Parcial Saul Standard Coarse
- **Structure:** 13 total competencies (1 Facts, 6 Concepts, 6 Skills) with 78 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Método de Curvas Características para Ecuaciones en Derivadas Parciales de Primer Orden | Concept | Understand | Unidad 17: Método de Curvas Características para Ecuaciones en Derivadas Parciales de Primer Orden | - | 6 |
| `Hab-01` | Resolución de EDPs Cuasilineales mediante el Método de Lagrange y Multiplicadores | Skill | Apply | Unidad 23: Resolución de EDPs Cuasilineales mediante el Método de Lagrange y Multiplicadores | C-01 | 6 |
| `H-01` | Teorema de Euler sobre Funciones Homogéneas y Relación de Identidad Diferencial | Fact | Remember | Unidad 6: Teorema de Euler sobre Funciones Homogéneas y Relación de Identidad Diferencial | C-01 | 6 |
| `Hab-02` | Resolución de Problemas de Frontera y Aplicaciones Económicas de EDPs | Skill | Apply | Unidad 1: Resolución de Problemas de Frontera y Aplicaciones Económicas de EDPs | H-01, Hab-01 | 6 |
| `C-02` | Estructura Algebraica del Espacio de Soluciones de Sistemas Lineales Autónomos de EDOs | Concept | Understand | Unidad 6: Estructura Algebraica del Espacio de Soluciones de Sistemas Lineales Autónomos de EDOs | - | 6 |
| `Hab-03` | Cálculo de Soluciones Analíticas de Sistemas Lineales de EDOs Homogéneos y No Homogéneos | Skill | Apply | Unidad 9: Cálculo de Soluciones Analíticas de Sistemas Lineales de EDOs Homogéneos y No Homogéneos | C-02 | 6 |
| `C-03` | Clasificación Topológica de Puntos de Equilibrio mediante el Esquema Traza-Determinante | Concept | Understand | Unidad 8: Clasificación Topológica de Puntos de Equilibrio mediante el Esquema Traza-Determinante | C-02 | 6 |
| `Hab-04` | Construcción de Diagramas de Fase y Análisis de Isoclinas Nulas en Sistemas 2x2 | Skill | Apply | Unidad 6: Construcción de Diagramas de Fase y Análisis de Isoclinas Nulas en Sistemas 2x2 | C-03 | 6 |
| `C-04` | Linealización Local de Sistemas Dinámicos No Lineales y Teorema de Hartman-Grobman | Concept | Understand | Unidad 13: Linealización Local de Sistemas Dinámicos No Lineales y Teorema de Hartman-Grobman | C-02 | 6 |
| `C-05` | Dinámica Macroeconómica Continua y Ajuste en Modelos IS-LM e Inflación-Desempleo | Concept | Understand | Unidad 3: Dinámica Macroeconómica Continua y Ajuste en Modelos IS-LM e Inflación-Desempleo | C-03, Hab-03 | 6 |
| `Hab-05` | Resolución y Calibración de Sistemas Macroeconómicos Dinámicos Continuos | Skill | Apply | Unidad 5: Resolución y Calibración de Sistemas Macroeconómicos Dinámicos Continuos | C-05 | 6 |
| `C-06` | Dinámica No Lineal en Modelos Ecológicos y Ciclos Económicos de Goodwin | Concept | Understand | Unidad 15: Dinámica No Lineal en Modelos Ecológicos y Ciclos Económicos de Goodwin | C-04 | 6 |
| `Hab-06` | Análisis Cualitativo y Estabilidad de Sistemas No Lineales de Crecimiento, Polución y Especies | Skill | Apply | Unidad 4: Análisis Cualitativo y Estabilidad de Sistemas No Lineales de Crecimiento, Polución y Especies | C-04, C-06 | 6 |

---

## Detailed Competency Specifications

### [C-01] Método de Curvas Características para Ecuaciones en Derivadas Parciales de Primer Orden (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 17: Método de Curvas Características para Ecuaciones en Derivadas Parciales de Primer Orden
- **Prerequisites:** None
- **Evidence Citations:** `TEMA 1 (EDP SAÚL) 2.pdf` (page 17)

#### Description & Cognitive Model
Para una EDP cuasilineal $a(x, y) U_x + b(x, y) U_y = c(x, y)$, la derivada direccional a lo largo de una curva parametrizada $(x(s), y(s))$ satisface $\frac{dU}{ds} = U_x \frac{dx}{ds} + U_y \frac{dy}{ds}$, lo que reduce la EDP al sistema característico $\frac{dx}{ds} = a(x, y)$, $\frac{dy}{ds} = b(x, y)$ y $\frac{dU}{ds} = c(x, y)$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Confusión entre derivada total y derivada parcial en la curva característica | conceptual_swap | high | $\frac{dU}{ds} = U_x + U_y$ | Por la regla de la cadena multivariada, la variación total depende de la tasa de cambio de cada coordenada respecto al parámetro de trayectoria $s$. |
| `D-C01-02` | Inversión de coeficientes direccionales en el sistema característico | conceptual_swap | high | $\frac{dx}{ds} = b(x, y), \quad \frac{dy}{ds} = a(x, y)$ | El coeficiente que multiplica a $U_x$ rige la evolución de $x$, y el coeficiente de $U_y$ rige la de $y$. |
| `D-C01-03` | Asunción de trayectorias características independientes de la solución en EDPs cuasilineales | conceptual_swap | high | $\frac{dy}{dx} = \frac{b(x,y)}{a(x,y)} \text{ es siempre desacoplada de } U$ | Si los coeficientes dependen de la función incógnita $U$, las características espaciales y la solución evolucionan acopladas simultáneamente. |
| `D-C01-04` | Tratamiento de la superficie integral como un campo escalar estático | conceptual_swap | high | $\nabla U \cdot (a, b) = 0 \text{ para cualquier función } c(x, y)$ | El vector tangente a la superficie característica $(a, b, c)$ es ortogonal al vector normal gradiente extendido $(U_x, U_y, -1)$. |
| `D-C01-05` | Confusión entre curvas características y curvas de nivel | conceptual_swap | high | $U(x(s), y(s)) = \text{constante a lo largo de toda curva característica}$ | Las características son curvas de nivel de $U$ únicamente si la ecuación es estrictamente homogénea ($c = 0$). |
| `D-C01-06` | Falla al verificar la transversalidad con la curva de condiciones iniciales | conceptual_swap | high | $\text{Cualquier curva con datos iniciales permite reconstruir una superficie solución única}$ | El teorema de existencia geométrica exige transversalidad entre la curva portadora de condiciones iniciales y las características locales. |

---

### [Hab-01] Resolución de EDPs Cuasilineales mediante el Método de Lagrange y Multiplicadores (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 23: Resolución de EDPs Cuasilineales mediante el Método de Lagrange y Multiplicadores
- **Prerequisites:** C-01
- **Evidence Citations:** `TEMA 1 (EDP SAÚL) 2.pdf` (page 23)

#### Description & Cognitive Model
Formular el sistema de ecuaciones subsidiarias de Lagrange $\frac{dx}{a(x, y, U)} = \frac{dy}{b(x, y, U)} = \frac{dU}{c(x, y, U)}$, integrar dos combinaciones diferenciales independientes $m(x, y, U) = c_1$ y $n(x, y, U) = c_2$ mediante separación o combinaciones lineales de multiplicadores, y expresar la solución general implícita $\phi(m, n) = 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Omisión de la constante de integración al resolver la primera ecuación subsidiaria | skipped_step | high | $\ln x = \ln y \implies x - y = 0$ | Toda integral primera de un sistema subsidiario de Lagrange debe aislar una constante de movimiento arbitraria $c_1$. |
| `D-Hab01-02` | Uso de integrales primeras funcionalmente dependientes | conceptual_swap | high | $m = \frac{x}{y}, \quad n = \left(\frac{x}{y}\right)^2$ | Las funciones $m$ y $n$ deben ser funcionalmente independientes en el espacio $(x, y, U)$, verificando que sus gradientes no sean colineales. |
| `D-Hab01-03` | Elección errónea de multiplicadores en la combinación lineal de razones | skipped_step | high | $\lambda_1 a + \lambda_2 b + \lambda_3 c \neq 0 \text{ pero se asume diferencial exacto nulo}$ | Para formar una integral primera por multiplicadores, la combinación lineal en el denominador debe anularse idénticamente. |
| `D-Hab01-04` | Inversión de signos en la integración por multiplicadores diferenciales | conceptual_swap | high | $dx + dy + dU = 0 \implies x + y - U = c_1$ | La integración directa de términos aditivos preserva rigurosamente los signos algebraicos de los diferenciales. |
| `D-Hab01-05` | Confusión entre solución implícita y producto de integrales | conceptual_swap | high | $U(x, y) = m(x, y, U) \cdot n(x, y, U)$ | La solución general de Lagrange se formula mediante una función arbitraria diferenciable $\phi(m, n) = 0$ que relaciona ambas integrales primeras. |
| `D-Hab01-06` | Despeje algebraico incorrecto de U en presencia de términos trascendentes | conceptual_swap | high | $e^U - x = c_2 \implies U = \ln(x) + c_2$ | Al aplicar la función inversa logarítmica, el argumento completo de la suma debe quedar dentro del logaritmo: $\ln(x + \psi(m))$. |

---

### [H-01] Teorema de Euler sobre Funciones Homogéneas y Relación de Identidad Diferencial (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 6: Teorema de Euler sobre Funciones Homogéneas y Relación de Identidad Diferencial
- **Prerequisites:** C-01
- **Evidence Citations:** `TEMA 1 (EDP SAÚL) 2.pdf` (page 6)

#### Description & Cognitive Model
Una función diferenciable $f: \mathbb{R}^n \to \mathbb{R}$ es homogénea de grado $n$ si y solo si verifica la identidad de Euler: $\sum_{i=1}^n x_i \frac{\partial f}{\partial x_i} = n f(x_1, \dots, x_n)$, lo que en economía fundamenta el agotamiento del producto bajo rendimientos constantes de escala.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Confusión del grado de homogeneidad con la suma de exponentes en funciones no homogéneas | conceptual_swap | high | $f(x, y) = x^\alpha + y^\beta \implies n = \alpha + \beta$ | Una función sólo es homogénea si todos los términos escalan con la misma potencia exacta $t^n$ ante una multiplicación escalar. |
| `D-H01-02` | Omisión del factor de escala del grado n en el lado derecho de la identidad | conceptual_swap | high | $\sum_{i=1}^n x_i \frac{\partial f}{\partial x_i} = f(x_1, \dots, x_n)$ | El lado derecho de la identidad de Euler contiene explícitamente el grado de homogeneidad $n$ multiplicando al valor de la función. |
| `D-H01-03` | Inversión de variables multiplicadoras en las derivadas parciales | conceptual_swap | high | $\sum_{i=1}^n \frac{1}{x_i} \frac{\partial f}{\partial x_i} = n f(x)$ | Cada derivada parcial debe multiplicarse directamente por la variable respecto a la cual se diferencia ($x_i \frac{\partial f}{\partial x_i}$). |
| `D-H01-04` | Confusión entre el grado de homogeneidad de la función y el de sus derivadas parciales | conceptual_swap | high | $\frac{\partial f}{\partial x_i} \text{ es homogénea de grado } n$ | Diferenciar una función homogénea de grado $n$ reduce su grado de homogeneidad en una unidad, quedando en $n-1$. |
| `D-H01-05` | Violación de la hipótesis de diferenciabilidad continua | conceptual_swap | high | $\text{El teorema de Euler se cumple para cualquier función homogénea, incluso discontinua}$ | La demostración de Euler descansa fundamentalmente en la regla de la cadena sobre $f(tx)$, requiriendo diferenciabilidad continua. |
| `D-H01-06` | Confusión entre homogeneidad de grado cero y función constante | conceptual_swap | high | $n = 0 \implies f(x_1, \dots, x_n) = \text{constante}$ | Una función homogénea de grado 0 es constante sobre rayos que parten del origen, pero varía con la composición relativa de los argumentos. |

---

### [Hab-02] Resolución de Problemas de Frontera y Aplicaciones Económicas de EDPs (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 1: Resolución de Problemas de Frontera y Aplicaciones Económicas de EDPs
- **Prerequisites:** H-01, Hab-01
- **Evidence Citations:** `MATH_IV_Problem_Set_II_2026_II.pdf` (page 1)

#### Description & Cognitive Model
Integrar EDPs de primer orden que modelan funciones económicas (utilidad $U(\gamma, \theta)$, beneficios $\Pi(p, w)$ o precios espaciales $P(x, y)$), imponer condiciones de frontera como $\Pi(p, 1) = \frac{p^2}{4}$ o $U(\gamma, 0) = \gamma^2$ para determinar la forma funcional unívoca, y derivar funciones de demanda y oferta óptimas mediante los Lemas de Roy y Hotelling.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Omisión de la condición de frontera al determinar la función arbitraria de la EDP | skipped_step | high | $\Pi(p, w) = w \cdot \psi\left(\frac{p}{w}\right) \text{ con } \psi \text{ indeterminada}$ | La condición de frontera determina de forma unívoca la regla de correspondencia de la función arbitraria $\psi$. |
| `D-Hab02-02` | Signo incorrecto en la aplicación del lema de Hotelling para demandas factoriales | conceptual_swap | high | $L(p, w) = \frac{\partial \Pi}{\partial w}$ | Por el lema de Hotelling, el negativo de la derivada del beneficio respecto al precio del factor representa la demanda de insumos. |
| `D-Hab02-03` | Inversión del cociente en la identidad de Roy para la demanda del consumidor | skipped_step | high | $x(p, m) = -\frac{V_m}{V_p}$ | La identidad de Roy establece que la demanda marshalliana es el negativo del cociente entre la derivada respecto al precio y la derivada respecto al ingreso: $-V_p / V_m$. |
| `D-Hab02-04` | Error algebraico al evaluar la homogeneidad de grado 1 en la función de beneficios | conceptual_swap | high | $p \frac{\partial \Pi}{\partial p} + w \frac{\partial \Pi}{\partial w} = 0$ | La función de beneficios escala linealmente con los precios nominales (homogénea de grado 1), mientras que la utilidad indirecta es de grado 0. |
| `D-Hab02-05` | Diferenciación incorrecta de funciones racionales al calcular elasticidades | conceptual_swap | high | $\epsilon_{L, w} = \frac{\partial L}{\partial w} \cdot \frac{w}{L} = +1 \text{ para } L(p, w) = \frac{p^2}{4w^2}$ | La derivada de $w^{-2}$ introduce un factor $-2$, confirmando una curva de demanda de trabajo con pendiente negativa. |
| `D-Hab02-06` | Planteamiento erróneo del gradiente espacial en problemas de costos de transporte | conceptual_swap | high | $\frac{dP}{ds} = a P_y + b P_x = \tau$ | Por regla de la cadena sobre la trayectoria parametrizada, $\frac{dP}{ds} = \frac{\partial P}{\partial x} \frac{\partial x}{\partial s} + \frac{\partial P}{\partial y} \frac{\partial y}{\partial s} = a P_x + b P_y$. |

---

### [C-02] Estructura Algebraica del Espacio de Soluciones de Sistemas Lineales Autónomos de EDOs (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 6: Estructura Algebraica del Espacio de Soluciones de Sistemas Lineales Autónomos de EDOs
- **Prerequisites:** None
- **Evidence Citations:** `TEMA 2 (S'EDOS I ).pdf` (page 6)

#### Description & Cognitive Model
Para el sistema lineal $\dot{X} = AX$, la solución general se construye como combinación lineal de soluciones independientes $X(t) = \sum_{i=1}^n c_i X_i(t)$ a partir de los pares propios $(\lambda_i, v_i)$ que satisfacen $(A - \lambda_i I) v_i = 0$, gobernada por las raíces del polinomio característico $p(\lambda) = \det(A - \lambda I) = 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Confusión entre valores propios y vectores propios | conceptual_swap | high | $(A - \lambda I) = v$ | Un autovalor $\lambda$ es un escalar que satisface $\det(A - \lambda I) = 0$, mientras que el autovector $v$ es un elemento no nulo del núcleo de $A - \lambda I$. |
| `D-C02-02` | Violación del principio de superposición en sistemas no lineales | conceptual_swap | high | $\text{Cualquier combinación lineal } c_1 X_1 + c_2 X_2 \text{ es solución de } \dot{X} = f(X)$ | La propiedad de que la suma de soluciones sea solución requiere linealidad: $A(c_1 X_1 + c_2 X_2) = c_1 AX_1 + c_2 AX_2$. |
| `D-C02-03` | Asunción de que autovalores repetidos siempre generan base completa de autovectores estándar | conceptual_swap | high | $\lambda_1 = \lambda_2 \implies X(t) = c_1 e^{\lambda_1 t} v_1 + c_2 e^{\lambda_1 t} v_2 \text{ siempre con } v_1, v_2 \text{ independientes}$ | Cuando una matriz no es diagonalizable, la base de soluciones exige autovectores generalizados acoplados con potencias de $t$. |
| `D-C02-04` | Desacoplamiento incorrecto de la parte real e imaginaria en autovalores complejos | conceptual_swap | high | $\lambda = a \pm bi \implies X(t) = e^{at} (v_1 + v_2)$ | Por la fórmula de Euler, la parte imaginaria $bi$ engendra oscilaciones trigonométricas $\cos(bt)$ y $\sin(bt)$ moduladas por la envolvente $e^{at}$. |
| `D-C02-05` | Omisión de la matriz identidad en el polinomio característico | conceptual_swap | high | $p(\lambda) = \det(A) - \lambda$ | El escalar $\lambda$ debe restarse de cada elemento de la diagonal principal restando $\lambda I$ antes de calcular el determinante. |
| `D-C02-06` | Confusión entre solución homogénea y solución completa de sistemas no homogéneos | conceptual_swap | high | $\dot{X} = AX + B \implies X(t) = X_h(t) \cdot X_p(t)$ | Por la linealidad del operador diferencial, la solución general es la suma afín de la solución complementaria más una solución particular. |

---

### [Hab-03] Cálculo de Soluciones Analíticas de Sistemas Lineales de EDOs Homogéneos y No Homogéneos (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 9: Cálculo de Soluciones Analíticas de Sistemas Lineales de EDOs Homogéneos y No Homogéneos
- **Prerequisites:** C-02
- **Evidence Citations:** `TEMA 2 (S'EDOS I ).pdf` (page 9)

#### Description & Cognitive Model
Calcular los autovalores y autovectores de la matriz $A \in \mathbb{R}^{2 \times 2}$, formular la matriz fundamental de soluciones según la naturaleza espectral (reales distintos, complejos o repetidos), y determinar la solución particular del sistema no homogéneo $\dot{X} = AX + B$ mediante $X_p = -A^{-1} B$ para vectores constantes o coeficientes indeterminados.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Signo invertido en el cálculo del estado estacionario no homogéneo | skipped_step | high | $X_p = A^{-1} B$ | Al despejar $AX_p + B = 0$, restar $B$ de ambos miembros introduce un signo negativo: $X_p = -A^{-1} B$. |
| `D-Hab03-02` | Inversión errónea de una matriz 2x2 | conceptual_swap | high | $\left(\begin{array}{cc} a & b \\ c & d \end{array}\right)^{-1} = \frac{1}{\det(A)} \left(\begin{array}{cc} a & -b \\ -c & d \end{array}\right)$ | La inversa de una matriz $2 \times 2$ intercambia los elementos diagonales ($a \leftrightarrow d$) y cambia el signo de los no diagonales. |
| `D-Hab03-03` | Omisión de la resolución del sistema para autovectores generalizados | skipped_step | high | $(A - \lambda_1 I) v_2 = 0 \text{ cuando } \lambda_1 = \lambda_2$ | En el caso degenerado con un único autovector propio $v_1$, el autovector generalizado $v_2$ resuelve el sistema no homogéneo $(A - \lambda I)v_2 = v_1$. |
| `D-Hab03-04` | Error en la formulación de coeficientes indeterminados con términos lineales | conceptual_swap | high | $B(t) = \binom{2t}{t} \implies X_p(t) = \binom{A_1}{B_1} t$ | El método de coeficientes indeterminados para un forzamiento polinomial lineal exige incluir tanto el término lineal como el término constante. |
| `D-Hab03-05` | Desfase angular en la descomposición de autovectores complejos | conceptual_swap | high | $X(t) = c_1 e^{at} (r \cos bt + s \sin bt) + c_2 e^{at} (s \cos bt - r \sin bt)$ | La parte real de $e^{(a+bi)t}(r+si)$ es $e^{at}(r\cos bt - s\sin bt)$ y la imaginaria es $e^{at}(s\cos bt + r\sin bt)$. |
| `D-Hab03-06` | Normalización nula del autovector al fijar variables libres | conceptual_swap | high | $\left(\begin{array}{cc} -6 & 12 \\ 3 & -6 \end{array}\right) \binom{v_x}{v_y} = 0 \implies v_x = 0, v_y = 0$ | Un autovector es por definición no nulo; al resolver un sistema homogéneo indeterminado se debe asignar un parámetro no nulo a la variable libre. |

---

### [C-03] Clasificación Topológica de Puntos de Equilibrio mediante el Esquema Traza-Determinante (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 8: Clasificación Topológica de Puntos de Equilibrio mediante el Esquema Traza-Determinante
- **Prerequisites:** C-02
- **Evidence Citations:** `TEMA 2 (S'EDOS II).pdf` (page 8)

#### Description & Cognitive Model
Para la matriz jacobiana $A$ de un sistema de EDOs $2 \times 2$, el polinomio característico es $\lambda^2 - \operatorname{tr}(A) \lambda + \det(A) = 0$ con discriminante $\Delta = \operatorname{tr}(A)^2 - 4 \det(A)$, de modo que el equilibrio es punto silla si $\det(A) < 0$, nodo estable si $\det(A) > 0, \Delta \ge 0, \operatorname{tr}(A) < 0$, y foco o espiral estable si $\det(A) > 0, \Delta < 0, \operatorname{tr}(A) < 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Confundir la condición de punto silla con inestabilidad por traza | conceptual_swap | high | $\operatorname{tr}(A) > 0 \implies \text{punto silla}$ | Un punto silla se caracteriza estrictamente por un determinante negativo, lo que garantiza que el producto de autovalores sea negativo. |
| `D-C03-02` | Inversión de la condición de estabilidad por el signo de la traza | conceptual_swap | high | $\operatorname{tr}(A) > 0 \implies \text{equilibrio asintóticamente estable}$ | La estabilidad exige que la parte real de todos los autovalores sea negativa; puesto que $\lambda_1 + \lambda_2 = \operatorname{tr}(A)$, la traza debe ser negativa. |
| `D-C03-03` | Confusión entre nodo y foco cuando el discriminante cambia de signo | conceptual_swap | high | $\Delta > 0 \implies \text{trayectorias en espiral oscilatorias}$ | Las oscilaciones sólo emergen cuando $\Delta < 0$, introduciendo una componente imaginaria no nula en los autovalores. |
| `D-C03-04` | Identificación errónea de un centro o vórtice en sistemas disipativos | conceptual_swap | high | $\operatorname{tr}(A) < 0, \Delta < 0 \implies \text{vórtice (órbitas cerradas periódicas)}$ | Un vórtice perfecto con órbitas cerradas neutralmente estables exige estrictamente traza nula ($\operatorname{tr}(A) = 0$). |
| `D-C03-05` | Ignorar la naturaleza espectral en la parábola frontera Delta igual a cero | conceptual_swap | high | $\Delta = 0 \implies \text{comportamiento caótico}$ | La parábola $\operatorname{tr}(A)^2 = 4 \det(A)$ separa la región de nodos reales de la región de focos espirales en el plano de estabilidad. |
| `D-C03-06` | Confusión entre estabilidad local y global en análisis traza-determinante | conceptual_swap | high | $\operatorname{tr}(J) < 0, \det(J) > 0 \implies \text{el sistema no lineal es globalmente estable en todo } \mathbb{R}^2$ | La linealización local basada en el jacobiano describe rigurosamente la topología en una vecindad del equilibrio, no globalmente. |

---

### [Hab-04] Construcción de Diagramas de Fase y Análisis de Isoclinas Nulas en Sistemas 2x2 (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 6: Construcción de Diagramas de Fase y Análisis de Isoclinas Nulas en Sistemas 2x2
- **Prerequisites:** C-03
- **Evidence Citations:** `TEMA 2 (S'EDOS II).pdf` (page 6)

#### Description & Cognitive Model
Determinar las isoclinas nulas $\dot{x} = 0$ y $\dot{y} = 0$, calcular sus pendientes para particionar el plano de fase en cuadrantes dinámicos, deducir los signos vectoriales $(\operatorname{sgn}(\dot{x}), \operatorname{sgn}(\dot{y}))$ en cada región, y esbozar las trayectorias de fase identificando ramas estables e inestables.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Intercambio de orientación en la derivada del campo de direcciones | skipped_step | high | $\frac{dx}{dy} = \frac{\dot{x}}{\dot{y}} \implies \dot{x} = 0 \text{ horizontal}$ | La pendiente de las curvas en el plano cartesiano $(x, y)$ es $\frac{dy}{dx} = \frac{\dot{y}}{\dot{x}}$; donde $\dot{x}=0$ la tangente es vertical y donde $\dot{y}=0$ es horizontal. |
| `D-Hab04-02` | Error en la determinación del sentido de las flechas del diagrama de fase | conceptual_swap | high | $\dot{x} > 0 \implies \text{flujo hacia la izquierda en el eje horizontal}$ | Una derivada positiva $\dot{x} > 0$ significa crecimiento de la variable, por lo que el desplazamiento espacial es hacia la derecha. |
| `D-Hab04-03` | Omisión de la prueba de signos en regiones adyacentes a las isoclinas | skipped_step | high | $\text{Asumir que el cuadrante I siempre tiene } \dot{x} > 0 \text{ y } \dot{y} > 0$ | Para determinar el sentido de las flechas de fase se debe evaluar un punto de prueba numérico a cada lado de cada isoclina. |
| `D-Hab04-04` | Confusión entre isoclinas y variedades invariantes asintóticas | conceptual_swap | high | $\text{Las trayectorias de solución siguen exactamente las líneas de las isoclinas nulas}$ | Una trayectoria cruza una isoclina nula perpendicularmente (vertical u horizontalmente), sin estar atrapada en ella salvo que sea un invariante. |
| `D-Hab04-05` | Despeje incorrecto de la pendiente de la isoclina nula | conceptual_swap | high | $5x + 2y = 0 \implies y = -\frac{2}{5} x$ | Al despejar $y$ en $ax + by = 0$, el coeficiente de $x$ pasa al numerador y el de $y$ al denominador: $y = -\frac{a}{b} x$. |
| `D-Hab04-06` | Determinación errónea de la variedad estable en un punto silla | conceptual_swap | high | $\text{La variedad estable corresponde al autovalor positivo } \lambda_1 > 0$ | La rama o variedad estable es el conjunto de puntos que convergen hacia el equilibrio cuando $t \to \infty$, asociado al autovalor negativo. |

---

### [C-04] Linealización Local de Sistemas Dinámicos No Lineales y Teorema de Hartman-Grobman (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 13: Linealización Local de Sistemas Dinámicos No Lineales y Teorema de Hartman-Grobman
- **Prerequisites:** C-02
- **Evidence Citations:** `TEMA 2 (S'EDOS I ).pdf` (page 13)

#### Description & Cognitive Model
Para un sistema no lineal autónomo $\dot{X} = F(X)$, la dinámica cualitativa en la vecindad de un punto de equilibrio hiperbólico $X^*$ ($\operatorname{Re}(\lambda_i) \neq 0$) es topológicamente equivalente a la de su sistema linealizado $\dot{X} = J(X^*) (X - X^*)$, donde $J(X^*) = \left[ \frac{\partial F_i}{\partial x_j}(X^*) \right]$ es la matriz jacobiana evaluada en el equilibrio.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Aplicación de linealización en equilibrios no hiperbólicos | conceptual_swap | high | $\operatorname{Re}(\lambda) = 0 \implies \text{el Jacobiano determina fielmente la estabilidad del sistema no lineal}$ | El teorema de Hartman-Grobman requiere hiperbolicidad ($\operatorname{Re}(\lambda) \neq 0$); si la traza es cero, los términos de segundo orden pueden desestabilizar el centro. |
| `D-C04-02` | Evaluación del Jacobiano en variables dinámicas en lugar del punto de equilibrio | conceptual_swap | high | $\dot{X} = J(x, y) X \text{ como aproximación lineal local válida}$ | Para obtener un sistema lineal con coeficientes constantes, todas las derivadas parciales de la matriz jacobiana deben evaluarse en las coordenadas del equilibrio $X^*$. |
| `D-C04-03` | Omisión del vector de traslación respecto al estado estacionario | conceptual_swap | high | $\dot{X} = J(X^*) X$ | La expansión en serie de Taylor de primer orden alrededor de $X^*$ opera sobre las desviaciones relativas $X - X^*$. |
| `D-C04-04` | Intercambio de filas y columnas en la derivación de la matriz jacobiana | conceptual_swap | high | $J_{12} = \frac{\partial g}{\partial x}, \quad J_{21} = \frac{\partial f}{\partial y}$ | La primera fila contiene el gradiente de la primera ecuación $\dot{x} = f(x, y)$, y la segunda fila el de la segunda $\dot{y} = g(x, y)$. |
| `D-C04-05` | Confusión entre multiplicidad de equilibrios y unicidad global | conceptual_swap | high | $\text{Un único análisis jacobiano describe todo el espacio de fases de un sistema no lineal}$ | Los sistemas no lineales pueden albergar múltiples puntos de equilibrio simultáneos (ej. un foco y dos sillas), cada uno con su propio comportamiento local. |
| `D-C04-06` | Ignorar la naturaleza topológica continua en Hartman-Grobman | conceptual_swap | high | $\text{La linealización preserva ángulos, curvaturas y diferenciabilidad exacta de las trayectorias}$ | La equivalencia entre el sistema no lineal y su linealización es topológica (preserva el sentido de las flechas y la estabilidad), pero no necesariamente $C^1$. |

---

### [C-05] Dinámica Macroeconómica Continua y Ajuste en Modelos IS-LM e Inflación-Desempleo (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 3: Dinámica Macroeconómica Continua y Ajuste en Modelos IS-LM e Inflación-Desempleo
- **Prerequisites:** C-03, Hab-03
- **Evidence Citations:** `TEMA 2 (APLICACIONES ECONOMICAS).pdf` (page 3)

#### Description & Cognitive Model
En modelos macroeconómicos continuos con ajuste proporcional por exceso de demanda (mercado de bienes $\dot{Y} = c_1(D - O)$ y monetario $\dot{r} = c_2(L^d - L^o)$ o curva de Phillips adaptativa $\dot{\pi} = j(p - \pi)$), la velocidad de ajuste y los parámetros estructurales condicionan la traza y determinante del sistema, determinando si la convergencia al estado estacionario es monótona (nodo) u oscilatoria (foco amortiguado).

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Confusión entre velocidad de ajuste de precios y posición del estado estacionario | conceptual_swap | high | $\text{Un incremento en } c_1 \text{ o } j \text{ modifica el nivel de equilibrio de largo plazo } Y^* \text{ o } \pi^*$ | El estado estacionario satisface $\dot{Y}=0, \dot{r}=0$; al anularse las derivadas, los multiplicadores de velocidad $c_1, c_2$ se cancelan. |
| `D-C05-02` | Asunción de estabilidad incondicional sin verificar la propensión marginal a consumir | conceptual_swap | high | $\text{El modelo IS-LM dinámico es siempre estable independientemente de la propensión } c$ | Si la propensión marginal a consumir induce un multiplicador keynesiano inestable ($c(1-\tau) \ge 1$), el sistema se vuelve intrínsecamente inestable. |
| `D-C05-03` | Inversión del efecto de la sensibilidad al financiamiento sobre la oscilación | conceptual_swap | high | $\text{Una menor sensibilidad de la inversión a la tasa de interés } \mu \text{ siempre genera mayor oscilación}$ | Una menor sensibilidad financiera desacopla los mercados de bienes y dinero, reduciendo el término sub-radical negativo del discriminante $\Delta$. |
| `D-C05-04` | Confusión entre expectativas adaptativas y previsión perfecta en la curva de Phillips | conceptual_swap | high | $\dot{\pi} = j(p - \pi) \implies \pi_t = p_t \text{ instantáneamente en todo } t$ | Bajo expectativas adaptativas continuas, la inflación esperada sigue a la inflación observada con un retardo dinámico proporcional a $j$. |
| `D-C05-05` | Interpretación incorrecta de perturbaciones monetarias en el plano de fase IS-LM | conceptual_swap | high | $\text{Un incremento en la oferta monetaria } \bar{m} \text{ desplaza la isoclina de bienes } \dot{Y} = 0$ | La oferta monetaria real entra directamente en el exceso de demanda de dinero ($L^d - \bar{m}$), por lo que perturba la isoclina $\dot{r} = 0$. |
| `D-C05-06` | Confusión entre estabilidad asintótica y oscilaciones sostenidas en inflación-desempleo | conceptual_swap | high | $\Delta < 0 \implies \text{ciclo límite autosostenido constante}$ | En un sistema lineal con traza negativa, los ciclos son transitorios y convergen asintóticamente hacia el punto estacionario. |

---

### [Hab-05] Resolución y Calibración de Sistemas Macroeconómicos Dinámicos Continuos (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 5: Resolución y Calibración de Sistemas Macroeconómicos Dinámicos Continuos
- **Prerequisites:** C-05
- **Evidence Citations:** `TEMA 2 (APLICACIONES ECONOMICAS).pdf` (page 5)

#### Description & Cognitive Model
Escribir modelos macroeconómicos dinámicos en la forma matricial $\dot{X} = AX + B$, calcular los valores de estado estacionario $X^* = -A^{-1} B$, calibrar los parámetros numéricos para derivar los autovalores y trayectorias analíticas explícitas $X(t)$, y evaluar el impacto de perturbaciones paramétricas en la trayectoria temporal.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Signo incorrecto al plantear la matriz jacobiana del modelo IS-LM | skipped_step | high | $A = \left(\begin{array}{cc} c_1[c(1-\tau)-1] & \mu c_1 \\ c_2 \theta & \gamma c_2 \end{array}\right)$ | Tanto la inversión decrece con la tasa de interés ($-\mu c_1$) como la demanda de dinero decrece con el costo de oportunidad ($-\gamma c_2$). |
| `D-Hab05-02` | Error de cálculo al evaluar el estado estacionario particular con parámetros numéricos | conceptual_swap | high | $X^* = \binom{1}{1} \text{ para } c_1=1, c_2=1, c=0.5, \tau=0, \mu=1, \theta=1, \gamma=2, B=\binom{10}{-4}$ | El equilibrio estacionario se calcula invirtiendo formalmente la matriz calibrada: $X^* = -A^{-1} B = -\frac{1}{2}\left(\begin{array}{cc} -2 & 1 \\ -1 & -0.5 \end{array}\right)\binom{10}{-4}$. |
| `D-Hab05-03` | Omisión del ajuste de las condiciones iniciales al resolver la combinación lineal temporal | skipped_step | high | $X(t) = e^{\lambda_1 t} v_1 + e^{\lambda_2 t} v_2 + X^* \text{ sin resolver el sistema algebraico para } (c_1, c_2)$ | Las constantes $c_1, c_2$ deben despejarse del sistema generado por las condiciones iniciales evaluadas en $t = 0$ restando el equilibrio. |
| `D-Hab05-04` | Inversión del impacto cualitativo de una reducción en la sensibilidad financiera | conceptual_swap | high | $\Delta \mu < 0 \implies \text{el nivel de producción de equilibrio de largo plazo disminuye}$ | El impacto de $\mu$ sobre $Y^*$ depende de la relación entre el gasto autónomo y los saldos reales monetarios según la fórmula de estática comparativa. |
| `D-Hab05-05` | Cálculo erróneo de la traza y determinante tras la modificación del parámetro | conceptual_swap | high | $\mu = 0.5 \implies \det(A) = 1.0$ | Al cambiar $\mu$ de 1 a 0.5, el elemento $A_{12} = -\mu c_1$ pasa a ser $-0.5$, alterando el determinante a $(-0.5)(-2) - (-0.5)(1) = 1.5$. |
| `D-Hab05-06` | Confusión en la deducción de la tasa de inflación en la curva de Phillips adaptativa | conceptual_swap | high | $p^* = \alpha - T - \beta U^* + g \pi^* \implies p^* \neq \pi^*$ | En el estado estacionario, el proceso de aprendizaje adaptativo concluye plenamente: $\dot{\pi} = 0 \implies \pi^* = p^*$. |

---

### [C-06] Dinámica No Lineal en Modelos Ecológicos y Ciclos Económicos de Goodwin (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 15: Dinámica No Lineal en Modelos Ecológicos y Ciclos Económicos de Goodwin
- **Prerequisites:** C-04
- **Evidence Citations:** `TEMA 2 (APLICACIONES ECONOMICAS).pdf` (page 15)

#### Description & Cognitive Model
En sistemas biológicos de Lokta-Volterra y en el modelo macroeconómico de distribución y crecimiento de Goodwin ($\dot{v} = v(\gamma - u \delta)$, $\dot{u} = u(-a + b v)$), las no linealidades bilineales generan un equilibrio interior positivo $(u^*, v^*) = (\frac{\gamma}{\delta}, \frac{a}{b})$ con jacobiano de traza nula $\operatorname{tr}(J^*) = 0$ y determinante positivo $\det(J^*) = \delta b u^* v^* = \gamma a > 0$, caracterizando un centro lineal con oscilaciones cíclicas cerradas en el plano distributivo empleo-salario.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Confundir el modelo de Goodwin con un ciclo límite aislado | conceptual_swap | high | $\text{El sistema de Goodwin colapsa hacia una única órbita periódica aislada atrayente}$ | Al ser análogo a Lokta-Volterra con constante de movimiento (invariante de Lotka), el modelo genera una foliación de órbitas cerradas según la condición inicial. |
| `D-C06-02` | Interpretación errónea de autovalores puramente imaginarios como inestabilidad explosiva | conceptual_swap | high | $\lambda = \pm i \sqrt{\gamma a} \implies \text{trayectorias espirales divergentes inestables}$ | Una parte real nula ($\operatorname{Re}(\lambda)=0$) no expande ni contrae las órbitas en la aproximación lineal, produciendo un centro neutro. |
| `D-C06-03` | Intercambio de roles dinámicos entre participación salarial y tasa de empleo | conceptual_swap | high | $\text{Un mayor empleo reduce el crecimiento de los salarios por la curva de Phillips}$ | La curva de Phillips en Goodwin postula que a mayor empleo ($v$), los salarios reales crecen más rápido ($\frac{\dot{w}}{w} = -\eta + \rho v$). |
| `D-C06-04` | Inversión de las coordenadas del punto estacionario en el plano fase | conceptual_swap | high | $(u^*, v^*) = \left(\frac{a}{b}, \frac{\gamma}{\delta}\right)$ | De $\dot{v}=0$ se despeja $u^* = \gamma/\delta$, y de $\dot{u}=0$ se despeja $v^* = a/b$. |
| `D-C06-05` | Ignorar el impacto del crecimiento poblacional y tecnológico en la distribución de equilibrio | conceptual_swap | high | $\text{Aumentos en el crecimiento demográfico } n \text{ no afectan la participación salarial de equilibrio } u^*$ | Para sostener un mayor crecimiento de la fuerza laboral y equipararla con capital, se requiere mayor tasa de acumulación e inversión, reduciendo $u^*$. |
| `D-C06-06` | Confusión entre el modelo competitivo de especies y el modelo depredador-presa | conceptual_swap | high | $\text{El modelo de dos especies competidoras siempre genera ciclos cerrados continuos como Lokta-Volterra}$ | A diferencia de presa-depredador, en especies competidoras el acoplamiento negativo mutuo elimina la rotación cerrada y genera una separatriz de silla. |

---

### [Hab-06] Análisis Cualitativo y Estabilidad de Sistemas No Lineales de Crecimiento, Polución y Especies (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 4: Análisis Cualitativo y Estabilidad de Sistemas No Lineales de Crecimiento, Polución y Especies
- **Prerequisites:** C-04, C-06
- **Evidence Citations:** `MATH_IV_Problem_Set_III_2026_II.pdf` (page 4)

#### Description & Cognitive Model
Para sistemas no lineales en economía ambiental ($\dot{k} = s \frac{k^\alpha}{p} - \delta k$, $\dot{p} = k^\beta - \gamma p$) o crecimiento endógeno con I+D, determinar analíticamente los puntos de equilibrio interiores $(k^*, p^*)$, calcular las derivadas parciales de la matriz jacobiana $J(k^*, p^*)$, y evaluar la estabilidad asintótica local determinando si el equilibrio es un atractor nodal o un punto silla.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Omisión de la condición estacionaria acoplada para el capital y la polución | skipped_step | high | $k^* = \left(\frac{s}{\delta}\right)^{\frac{1}{1-\alpha}} \text{ ignorando el efecto de la polución } p$ | La polución $p$ reduce directamente la producción de capital $\frac{k^\alpha}{p}$, por lo que ambos estados estacionarios están mutuamente determinados. |
| `D-Hab06-02` | Derivación parcial errónea del término cociente en la matriz jacobiana | conceptual_swap | high | $\frac{\partial}{\partial p} \left(s \frac{k^\alpha}{p} - \delta k\right) = s \frac{k^\alpha}{p^2}$ | La derivada de $p^{-1}$ respecto a $p$ es $-p^{-2}$, introduciendo un signo negativo fundamental en la sensibilidad cruzada del jacobiano. |
| `D-Hab06-03` | Omisión del cálculo del determinante jacobiano para clasificar la estabilidad | skipped_step | high | $\operatorname{tr}(J^*) < 0 \implies \text{el equilibrio es automáticamente un atractor estable}$ | Una traza negativa no impide que uno de los autovalores sea positivo si el determinante es negativo ($\det(J) = \lambda_1 \lambda_2 < 0$). |
| `D-Hab06-04` | Error en la linealización logarítmica de modelos de crecimiento endógeno con I+D | conceptual_swap | high | $\frac{\dot{g}_A}{g_A} = \beta g_K + \gamma n + \theta g_A$ | Al tomar la tasa de crecimiento de $g_A = c_A K^\beta L^\gamma A^{\theta-1}$, el exponente de $A$ es $\theta - 1$, aportando $(\theta-1)g_A$. |
| `D-Hab06-05` | Inversión de las ramas de la separatriz en sistemas competitivos | conceptual_swap | high | $\text{Cualquier condición inicial por encima de la diagonal favorece a la especie } x$ | En modelos de competencia con punto silla, la separatriz divide el plano en dos regiones disyuntas de atracción hacia equilibrios frontera opuestos. |
| `D-Hab06-06` | Sustitución de potencias incorrecta al evaluar el determinante en el punto estacionario | conceptual_swap | high | $\det(J^*) = \delta \gamma (\alpha - 1)$ | El producto no diagonal $-J_{12} J_{21}$ resulta positivo debido al doble signo negativo (de $-s k^\alpha / p^2$ y de la fórmula $-J_{12}J_{21}$). |

---
