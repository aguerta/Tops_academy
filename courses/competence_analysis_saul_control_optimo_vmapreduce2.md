# Cognitive Task Analysis (CTA): Saul Control Optimo Vmapreduce2

- **Course ID:** `saul_control_optimo_vmapreduce2`
- **Macro-Competency:** Dominio y aplicación analítica integral de Saul Control Optimo Vmapreduce2
- **Structure:** 18 total competencies (5 Facts, 7 Concepts, 6 Skills) with 108 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Concepto de funcional y trayectoria admisible en optimización dinámica | Concept | Understand | Unidad 5: Concepto de funcional y trayectoria admisible en optimización dinámica | - | 6 |
| `H-01` | Estructura canónica de los problemas de Lagrange, Mayer y Bolza | Fact | Remember | Unidad 8: Estructura canónica de los problemas de Lagrange, Mayer y Bolza | C-01 | 6 |
| `C-02` | Ecuación de Euler como condición necesaria de primer orden | Concept | Understand | Unidad 9: Ecuación de Euler como condición necesaria de primer orden | C-01 | 6 |
| `H-02` | Forma desarrollada de la ecuación diferencial de Euler | Fact | Understand | Unidad 9: Forma desarrollada de la ecuación diferencial de Euler | C-02 | 6 |
| `C-03` | Condición necesaria de segundo orden de Legendre | Concept | Understand | Unidad 10: Condición necesaria de segundo orden de Legendre | C-02 | 6 |
| `C-04` | Condiciones de suficiencia global mediante concavidad y convexidad | Concept | Understand | Unidad 11: Condiciones de suficiencia global mediante concavidad y convexidad | C-02 | 6 |
| `H-03` | Criterio del hessiano para concavidad y convexidad en cálculo variacional | Fact | Understand | Unidad 12: Criterio del hessiano para concavidad y convexidad en cálculo variacional | C-04 | 6 |
| `Hab-01` | Resolución de la ecuación de Euler con condiciones de contorno fijas | Skill | Apply | Unidad 14: Resolución de la ecuación de Euler con condiciones de contorno fijas | H-02, C-02 | 6 |
| `Hab-02` | Verificación de condiciones de segundo orden y suficiencia en problemas variacionales | Skill | Evaluate | Unidad 15: Verificación de condiciones de segundo orden y suficiencia en problemas variacionales | C-03, H-03, Hab-01 | 6 |
| `Hab-03` | Resolución analítica y clasificación de funcionales con parámetros y dinámica lineal-cuadrática | Skill | Apply | Unidad 16: Resolución analítica y clasificación de funcionales con parámetros y dinámica lineal-cuadrática | Hab-01, Hab-02 | 6 |
| `H-04` | Primera Integral e Identidad de Beltrami | Fact | Remember | Unidad 19: Primera Integral e Identidad de Beltrami | C-02 | 6 |
| `C-05` | Casos Particulares de Reducción de la Ecuación de Euler | Concept | Understand | Unidad 18: Casos Particulares de Reducción de la Ecuación de Euler | H-04 | 6 |
| `C-06` | Condición de Transversalidad con Estado Final Libre | Concept | Understand | Unidad 21: Condición de Transversalidad con Estado Final Libre | C-05 | 6 |
| `Hab-04` | Resolución de Problemas Variacionales con Extremo Terminal Libre | Skill | Apply | Unidad 22: Resolución de Problemas Variacionales con Extremo Terminal Libre | C-06 | 6 |
| `C-07` | Condición de Transversalidad con Instante Final Libre | Concept | Understand | Unidad 24: Condición de Transversalidad con Instante Final Libre | H-04, C-06 | 6 |
| `Hab-05` | Determinación del Horizonte y Trayectoria con Instante Final Libre | Skill | Apply | Unidad 25: Determinación del Horizonte y Trayectoria con Instante Final Libre | C-07 | 6 |
| `H-05` | Estructura del Modelo de Monopolio Dinámico de Evans | Fact | Remember | Unidad 27: Estructura del Modelo de Monopolio Dinámico de Evans | C-05 | 6 |
| `Hab-06` | Optimización Dinámica del Modelo Trade-off Inflación-Desempleo | Skill | Apply | Unidad 28: Optimización Dinámica del Modelo Trade-off Inflación-Desempleo | C-05 | 6 |

---

## Detailed Competency Specifications

### [C-01] Concepto de funcional y trayectoria admisible en optimización dinámica (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 5: Concepto de funcional y trayectoria admisible en optimización dinámica
- **Prerequisites:** None
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 5)

#### Description & Cognitive Model
Definición de un funcional $V[y] = \int_0^T F(t, y(t), y'(t)) dt$ como una correspondencia que asigna un número real a cada trayectoria continua admisible $y(t)$ en el espacio de funciones.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Confusión entre función y funcional | conceptual_swap | high | Un funcional asigna una variable $y$ a un conjunto de puntos $t$, evaluándose puntualmente como $V(t) = F(t, y)$. | Un funcional opera sobre espacios de funciones (curvas completas) y no evalúa puntos individuales independientes en el dominio real. |
| `D-C01-02` | Restricción errónea de dominio funcional | conceptual_swap | high | El funcional solo está definido para trayectorias lineales $y(t) = at + b$. | Las trayectorias admisibles no están limitadas a polinomios de primer grado, sino a curvas de clase $C^1$ que satisfagan las condiciones de contorno. |
| `D-C01-03` | Confusión entre argumento de estado y funcional | conceptual_swap | high | El funcional $V[y]$ es equivalente al integrando puntual $F(t, y, y')$. | La función de arco $F$ evalúa el estado y su tasa de cambio instantánea, mientras que el funcional integra estos valores sobre todo el horizonte temporal. |
| `D-C01-04` | Ambigüedad en la noción de trayectoria admisible | conceptual_swap | high | Cualquier función discontinua en $[0, T]$ es admisible siempre que $V[y]$ converja. | En el cálculo variacional clásico las curvas admisibles requieren continuidad y diferenciabilidad para calcular el arco y su velocidad instantánea. |
| `D-C01-05` | Error de dimensionalidad de la imagen del funcional | conceptual_swap | high | La imagen del funcional $V[y]$ es una nueva función temporal $v(t)$. | Un funcional proyecta un espacio de dimensión infinita (el espacio de funciones admisibles) en la recta real unidimensional $\mathbb{R}$. |
| `D-C01-06` | Inversión de variables en el arco | conceptual_swap | high | El arco se define únicamente por el tiempo final $T$ y la pendiente $y'(T)$, ignorando el estado intermedio $y(t)$. | La evaluación del funcional a lo largo del tiempo requiere el conocimiento simultáneo de la etapa $t$, el estado $y(t)$ y la velocidad $y'(t)$. |

---

### [H-01] Estructura canónica de los problemas de Lagrange, Mayer y Bolza (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 8: Estructura canónica de los problemas de Lagrange, Mayer y Bolza
- **Prerequisites:** C-01
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 8)

#### Description & Cognitive Model
Identificación analítica de las tres formas estándar de funcionales: problema de Lagrange $V[y] = \int_0^T F(t, y, y') dt$, problema de Mayer $V[y] = G(T, y(T))$ y problema de Bolza $V[y] = \int_0^T F(t, y, y') dt + G(T, y(T))$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Confusión entre problema de Lagrange y Mayer | conceptual_swap | high | El problema de Lagrange evalúa exclusivamente el valor final $V[y] = G(T, y(T))$. | El problema que optimiza únicamente una función del estado final $G(T, y(T))$ es el de Mayer, no el de Lagrange. |
| `D-H01-02` | Identificación errónea del problema de Bolza | conceptual_swap | high | El problema de Bolza se define como el producto de la integral y el término terminal $V[y] = G(T, y(T)) \cdot \int_0^T F dt$. | La formulación canónica de Bolza combina linealmente el rendimiento acumulativo de flujo continuo con el pago o penalización terminal mediante adición. |
| `D-H01-03` | Omisión del término integral en el problema de Bolza | conceptual_swap | high | El problema de Bolza solo contiene una función de ponderación intermedia $F(t, y)$ sin integrar respecto al tiempo. | Un problema de Bolza sin integral en el intervalo temporal pierde el costo de trayectoria propio del cálculo variacional. |
| `D-H01-04` | Confusión sobre la función de pago terminal en Mayer | conceptual_swap | high | El problema de Mayer depende explícitamente de la derivada segunda $\ddot{y}(T)$ en el instante final. | La función terminal $G(T, y(T))$ evalúa el estado alcanzado al final del horizonte temporal, sin involucrar derivadas de orden superior. |
| `D-H01-05` | Error de denominación en la forma integral pura | conceptual_swap | high | Un funcional con solo integrando $\int_0^T F(t, y, y') dt$ se denomina problema de Mayer. | Mayer corresponde únicamente al término terminal, mientras que la integral de trayectoria define al problema de Lagrange. |
| `D-H01-06` | Falsa equivalencia de problemas dinámicos | conceptual_swap | high | Cualquier problema de Bolza es idéntico al de Lagrange si la función terminal $G(T, y(T))$ es no nula. | Si $G(T, y(T)) \ne 0$, el término terminal altera las condiciones de transversalidad y la función objetivo global. |

---

### [C-02] Ecuación de Euler como condición necesaria de primer orden (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 9: Ecuación de Euler como condición necesaria de primer orden
- **Prerequisites:** C-01
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 9)

#### Description & Cognitive Model
Principio variacional que establece que toda trayectoria óptima local $x^*(t)$ que maximiza o minimiza el funcional $J(x) = \int_{t_0}^{t_1} F(x, \dot{x}, t) dt$ satisface $F_x - \frac{d}{dt} F_{\dot{x}} = 0$ para todo $t \in [t_0, t_1]$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Error de signo en la condición de Euler | conceptual_swap | high | $F_x + \frac{d}{dt} F_{\dot{x}} = 0$ | La primera variación nula $\delta J = 0$ tras integración por partes produce un signo negativo ante el término temporal de la derivada respecto a la velocidad. |
| `D-C02-02` | Inversión de variables en las derivadas parciales | conceptual_swap | high | $F_{\dot{x}} - \frac{d}{dt} F_x = 0$ | La derivada respecto a la variable de estado $F_x$ es el término algebraico directo, y la derivada respecto a la velocidad $F_{\dot{x}}$ es la que se deriva respecto al tiempo. |
| `D-C02-03` | Confusión entre condición necesaria y suficiente | conceptual_swap | high | Cualquier trayectoria que satisfaga la ecuación de Euler es garantizadamente un máximo global. | La anulación de la primera variación solo caracteriza puntos estacionarios locales (máximos, mínimos o puntos de inflexión funcional). |
| `D-C02-04` | Omisión de la diferenciación total respecto al tiempo | conceptual_swap | high | $F_x - F_{\dot{x}} = 0$ | El término $\frac{d}{dt} F_{\dot{x}}$ representa una derivada temporal total a lo largo de la trayectoria, no una simple resta estática de derivadas parciales. |
| `D-C02-05` | Confusión con optimización estática multivariada | conceptual_swap | high | $F_x = 0$ y $F_{\dot{x}} = 0$ simultáneamente para cada $t$. | En optimización dinámica el estado y la velocidad están interconectados por la trayectoria; sus derivadas parciales no se anulan de forma independiente. |
| `D-C02-06` | Falso requisito de orden superior en primer orden | conceptual_swap | high | La condición necesaria de primer orden exige adicionalmente que $F_{xx} \le 0$ en todo punto. | Las derivadas segundas corresponden a las condiciones de segundo orden (Legendre) o suficiencia, no a la condición de Euler de primer orden. |

---

### [H-02] Forma desarrollada de la ecuación diferencial de Euler (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 9: Forma desarrollada de la ecuación diferencial de Euler
- **Prerequisites:** C-02
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 9)

#### Description & Cognitive Model
Expresión desarrollada de la ecuación de Euler mediante la regla de la cadena para la derivada total: $F_x - F_{x\dot{x}}\dot{x} - F_{\dot{x}\dot{x}}\ddot{x} - F_{\dot{x}t} = 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H02-01` | Error de signos en la regla de la cadena temporal | conceptual_swap | high | $F_x + F_{x\dot{x}}\dot{x} + F_{\dot{x}\dot{x}}\ddot{x} + F_{\dot{x}t} = 0$ | El signo negativo que precede a $\frac{d}{dt} F_{\dot{x}}$ distribuye sobre todos los términos de la derivada total respecto al tiempo. |
| `D-H02-02` | Confusión en la derivada cruzada respecto al tiempo | conceptual_swap | high | $F_x - F_{xx}\dot{x} - F_{\dot{x}\dot{x}}\ddot{x} - F_{xt} = 0$ | La derivada total $\frac{d}{dt} F_{\dot{x}}$ involucra derivadas de $F_{\dot{x}}$ respecto a $x$, $\dot{x}$ y $t$, dando $F_{\dot{x}x}\dot{x}$, $F_{\dot{x}\dot{x}}\ddot{x}$ y $F_{\dot{x}t}$. |
| `D-H02-03` | Omisión de la aceleración del estado | conceptual_swap | high | $F_x - F_{x\dot{x}}\dot{x} - F_{\dot{x}t} = 0$ | La ecuación de Euler es una ecuación diferencial ordinaria generalmente de segundo orden en $x(t)$, requiriendo el término $F_{\dot{x}\dot{x}}\ddot{x}$. |
| `D-H02-04` | Multiplicador erróneo de la velocidad | conceptual_swap | high | $F_x - F_{x\dot{x}} x - F_{\dot{x}\dot{x}}\ddot{x} - F_{\dot{x}t} = 0$ | Al aplicar $\frac{d}{dt}$ a $F_{\dot{x}}(x, \dot{x}, t)$, por la regla de la cadena $\frac{\partial F_{\dot{x}}}{\partial x} \frac{dx}{dt} = F_{x\dot{x}}\dot{x}$, multiplicando por la velocidad $\dot{x}$ y no por el estado $x$. |
| `D-H02-05` | Confusión con derivada segunda de posición pura | conceptual_swap | high | $F_x - F_{xx}\ddot{x} - F_{\dot{x}\dot{x}}\dot{x} - F_{\dot{x}t} = 0$ | El coeficiente de la aceleración $\ddot{x}$ es necesariamente la segunda derivada respecto a la velocidad $F_{\dot{x}\dot{x}}$, no respecto a la posición $F_{xx}$. |
| `D-H02-06` | Error de cancelación en sistemas autónomos | conceptual_swap | high | Si $F$ no depende explícitamente de $t$, entonces $F_{x\dot{x}} = 0$ necesariamente. | La independencia temporal directa elimina la derivada parcial explícita $F_{\dot{x}t}$, sin implicar la nulidad de las derivadas espaciales cruzadas. |

---

### [C-03] Condición necesaria de segundo orden de Legendre (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 10: Condición necesaria de segundo orden de Legendre
- **Prerequisites:** C-02
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 10)

#### Description & Cognitive Model
Criterio de curvatura local que establece que a lo largo de la trayectoria extremal $x^*(t)$, es condición necesaria que $F_{\dot{x}\dot{x}} \le 0$ para un máximo local y $F_{\dot{x}\dot{x}} \ge 0$ para un mínimo local en todo $t \in [t_0, t_1]$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Inversión de los signos de la condición de Legendre | conceptual_swap | high | $F_{\dot{x}\dot{x}} \ge 0$ para un máximo local y $F_{\dot{x}\dot{x}} \le 0$ para un mínimo local. | Al igual que en cálculo elemental, la concavidad requerida para maximizar exige una segunda derivada no positiva respecto a la tasa de variación. |
| `D-C03-02` | Evaluación sobre la variable incorrecta | conceptual_swap | high | $F_{xx} \le 0$ para máximo local y $F_{xx} \ge 0$ para mínimo local como condición de Legendre. | La condición de Legendre evalúa las variaciones rápidas de la velocidad $\dot{x}$, requiriendo analizar la derivada segunda $F_{\dot{x}\dot{x}}$. |
| `D-C03-03` | Confusión entre condición necesaria y condición de suficiencia global | conceptual_swap | high | Si $F_{\dot{x}\dot{x}} \le 0$ en $x^*(t)$, la trayectoria es necesariamente un máximo global. | La verificación de Legendre descarta que la extremal sea un mínimo o punto de ensilladura respecto a variaciones de velocidad, pero no prueba la maximalidad global. |
| `D-C03-04` | Falso requisito de estricta desigualdad en la condición necesaria | conceptual_swap | high | Para un máximo local se exige obligatoriamente la condición estricta $F_{\dot{x}\dot{x}} < 0$, excluyendo la igualdad a cero. | El teorema 1.2 establece la desigualdad no estricta $F_{\dot{x}\dot{x}} \le 0$ como requisito necesario para todo $t \in [t_0, t_1]$. |
| `D-C03-05` | Confusión con el determinante hessiano completo | conceptual_swap | high | La condición de Legendre exige que $\det(H_F) \le 0$ para un máximo local. | El determinante del hessiano se utiliza en condiciones de suficiencia de concavidad bivariada, mientras que Legendre solo examina la curvatura respecto a $\dot{x}$. |
| `D-C03-06` | Incompatibilidad temporal | conceptual_swap | high | Basta con que $F_{\dot{x}\dot{x}} \le 0$ se cumpla únicamente en el instante final $t_1$. | Si la condición se viola en algún subintervalo de $[t_0, t_1]$, la trayectoria extremal no puede ser un maximizador local del funcional. |

---

### [C-04] Condiciones de suficiencia global mediante concavidad y convexidad (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 11: Condiciones de suficiencia global mediante concavidad y convexidad
- **Prerequisites:** C-02
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 11)

#### Description & Cognitive Model
Teoremas de suficiencia que garantizan que si $F(x, \dot{x}, t)$ es conjuntamente cóncava en $(x, \dot{x})$ para todo $t \in [t_0, t_1]$, la solución de Euler con condiciones de contorno es un máximo global; si es convexa, es un mínimo global.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Inversión de propiedades de concavidad y convexidad | conceptual_swap | high | La concavidad de $F$ en $(x, \dot{x})$ garantiza un mínimo global y la convexidad un máximo global. | Una función objetivo cóncava acota superiormente los valores del funcional garantizando maximalidad global frente a cualquier trayectoria admisible. |
| `D-C04-02` | Reducción errónea a concavidad unidimensional | conceptual_swap | high | Es suficiente que $F(x, \dot{x}, t)$ sea cóncava únicamente respecto a $x$, independientemente de $\dot{x}$. | La variación de la trayectoria perturba tanto el estado como su derivada simultáneamente, requiriendo concavidad conjunta en el espacio $(x, \dot{x})$. |
| `D-C04-03` | Omisión de las condiciones de contorno y transversalidad | conceptual_swap | high | La concavidad de $F$ garantiza el máximo global aun si la trayectoria no verifica las condiciones de contorno o transversalidad. | La concavidad solo asegura que no existan otras trayectorias admisibles con mayor valor si la trayectoria base satisface las ecuaciones de contorno. |
| `D-C04-04` | Confusión sobre la dependencia temporal en la suficiencia | conceptual_swap | high | La función $F(x, \dot{x}, t)$ debe ser cóncava respecto a la terna completa $(x, \dot{x}, t)$, incluyendo el tiempo. | El tiempo $t$ es un parámetro exógeno de integración; la optimización se realiza sobre las funciones $x(t)$ y sus derivadas, no sobre la escala temporal. |
| `D-C04-05` | Falsa necesidad de estricta concavidad para suficiencia | conceptual_swap | high | Si $F$ es únicamente semidefinida negativa (cóncava pero no estrictamente), no puede garantizarse un máximo global. | La concavidad semidefinida asegura que ningún valor admisible supere al óptimo, aunque el maximizador global pudiera no ser estrictamente único. |
| `D-C04-06` | Confusión entre condición local de Legendre y suficiencia global | conceptual_swap | high | Verificar la condición de Legendre $F_{\dot{x}\dot{x}} \le 0$ es suficiente para afirmar que la trayectoria es un máximo global. | La condición de Legendre no analiza las derivadas cruzadas ni la curvatura respecto al estado $x$, por lo que no puede garantizar optimalidad global. |

---

### [H-03] Criterio del hessiano para concavidad y convexidad en cálculo variacional (Fact)

- **Bloom Level:** Understand
- **Session:** Unidad 12: Criterio del hessiano para concavidad y convexidad en cálculo variacional
- **Prerequisites:** C-04
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 12)

#### Description & Cognitive Model
Caracterización de la concavidad y convexidad de $F(x, \dot{x}, t)$ mediante los menores principales del hessiano $H_F = \begin{bmatrix} F_{xx} & F_{x\dot{x}} \\ F_{\dot{x}x} & F_{\dot{x}\dot{x}} \end{bmatrix}$, donde definida negativa requiere $F_{xx} < 0$ y $\det(H_F) > 0$, y definida positiva requiere $F_{xx} > 0$ y $\det(H_F) > 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H03-01` | Signo incorrecto del determinante para concavidad | conceptual_swap | high | Para que $H_F$ sea definida negativa se requiere $F_{xx} < 0$ y $\det(H_F) < 0$. | En una matriz de $2 \times 2$, los signos de los menores principales para definida negativa deben alternar: primero negativo ($F_{xx} < 0$) y segundo positivo ($\det(H_F) > 0$). |
| `D-H03-02` | Confusión de signos en la definición positiva | conceptual_swap | high | Para que $H_F$ sea definida positiva se requiere $F_{xx} < 0$ y $\det(H_F) > 0$. | Una matriz definida positiva exige que todos sus menores principales dominantes sean estrictamente positivos. |
| `D-H03-03` | Estructura errónea de la matriz hessiana $H_F$ | conceptual_swap | high | $H_F = \begin{bmatrix} F_{xx} & F_{xt} \\ F_{tx} & F_{tt} \end{bmatrix}$ | El hessiano relevante para la suficiencia se calcula con respecto a las variables del espacio de fase $(x, \dot{x})$, no respecto al tiempo $t$. |
| `D-H03-04` | Error de clasificación con determinante nulo | conceptual_swap | high | Si $F_{xx} \le 0$ y $\det(H_F) = 0$, la matriz es indefinida y no se puede concluir concavidad. | Un determinante nulo con primer menor no positivo cumple los requisitos de semidefinición negativa, garantizando concavidad débil. |
| `D-H03-05` | Confusión entre el primer y segundo menor | conceptual_swap | high | Basta con que $\det(H_F) > 0$ para clasificar la función como cóncava, sin importar el signo de $F_{xx}$. | Un determinante positivo puede provenir de dos autovalores positivos (definida positiva) o dos autovalores negativos (definida negativa); el signo de $F_{xx}$ es indispensable. |
| `D-H03-06` | Incompatibilidad de simetría en el hessiano | conceptual_swap | high | El elemento $F_{x\dot{x}}$ no coincide con $F_{\dot{x}x}$ debido a la dirección temporal del arco. | Para funciones de clase $C^2$, el orden de diferenciación parcial no altera el resultado, por lo que el hessiano es simétrico. |

---

### [Hab-01] Resolución de la ecuación de Euler con condiciones de contorno fijas (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 14: Resolución de la ecuación de Euler con condiciones de contorno fijas
- **Prerequisites:** H-02, C-02
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 14)

#### Description & Cognitive Model
Aplicar la ecuación de Euler $F_x - \frac{d}{dt}F_{\dot{x}} = 0$ a funcionales cuadráticos, derivar la ecuación diferencial ordinaria resultante y resolver la trayectoria extremal sujeta a condiciones iniciales y terminales $x(t_0) = x_0$ y $x(t_1) = x_1$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Error en la derivación de la ecuación diferencial | conceptual_swap | high | Para $F = x^2 + \dot{x}^2$, la ecuación resultante es $\ddot{x} + x = 0$, generando $x(t) = c_1 \cos(t) + c_2 \sin(t)$. | El término $-\frac{d}{dt}(2\dot{x}) = -2\ddot{x}$ al despejarse con $2x$ produce $2x - 2\ddot{x} = 0 \Rightarrow \ddot{x} - x = 0$, no una suma. |
| `D-Hab01-02` | Omitir la evaluación de condiciones de frontera | skipped_step | high | $x(t) = c_1 e^{-t} + c_2 e^t$, dejando las constantes arbitrarias sin determinar para el intervalo $[0, 1]$. | Un problema con extremos fijos requiere calcular explícitamente las constantes de integración a partir de los valores dados en $t_0$ y $t_1$. |
| `D-Hab01-03` | Confusión en las raíces del polinomio característico | conceptual_swap | high | Para $\ddot{x} - x = 0$, el polinomio característico es $m^2 + 1 = 0$, con raíces complejas $m = \pm i$. | El coeficiente negativo de $x$ implica $m^2 - 1 = 0$, cuyas raíces son números reales $\pm 1$, dando soluciones exponenciales reales. |
| `D-Hab01-04` | Omitir la diferenciación temporal del momento conjugado | skipped_step | high | Establecer $2x - 2\dot{x} = 0 \Rightarrow \dot{x} - x = 0$, obteniendo $x(t) = e^t$ sin derivar $\dot{x}$ respecto al tiempo. | La derivada temporal total actúa sobre $\dot{x}$ produciendo la aceleración $\ddot{x}$; omitirla reduce espuriamente el orden de la ecuación diferencial. |
| `D-Hab01-05` | Error de evaluación en el sistema de constantes | conceptual_swap | high | Al evaluar $x(0) = c_1 + c_2 = 1$ y $x(1) = c_1 e^{-1} + c_2 e = e$, asignar erróneamente $c_1 = 1$ y $c_2 = 0$, dando $x(t) = e^{-t}$. | Sustituyendo $c_1 = 1, c_2 = 0$ en $t=1$ daría $x(1) = e^{-1} \ne e$, violando la condición terminal especificada. |
| `D-Hab01-06` | Diferenciación parcial incorrecta del integrando | conceptual_swap | high | Calcular $F_x = 2$ y $F_{\dot{x}} = 2$ a partir de $F = x^2 + \dot{x}^2$, obteniendo una ecuación algebraica en vez de diferencial. | La variable de estado $x$ y la velocidad $\dot{x}$ son variables independientes en la función de arco $F(x, \dot{x}, t)$, por lo que sus derivadas retienen las variables lineales. |

---

### [Hab-02] Verificación de condiciones de segundo orden y suficiencia en problemas variacionales (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 15: Verificación de condiciones de segundo orden y suficiencia en problemas variacionales
- **Prerequisites:** C-03, H-03, Hab-01
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 15)

#### Description & Cognitive Model
Evaluar analíticamente la condición de Legendre $F_{\dot{x}\dot{x}}$ y construir la matriz hessiana $H_F$ para clasificar el extremo local y certificar la optimalidad global mediante convexidad o concavidad en ejemplos con extremos fijos.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Confusión entre extremo local y conclusión global | conceptual_swap | high | Al constatar que $F_{\dot{x}\dot{x}} = 2 > 0$, concluir directamente que $x(t) = e^t$ es un mínimo global sin analizar el hessiano. | Legendre descarta trayectorias perturbadas en velocidad localmente, pero la maximalidad o minimalidad global exige verificar concavidad o convexidad de $F$ en todo el dominio. |
| `D-Hab02-02` | Omitir el cálculo del determinante hessiano en la suficiencia | skipped_step | high | Concluir que $F$ es estrictamente convexa observando únicamente que $F_{xx} = 2 > 0$, sin calcular el determinante de $H_F$. | Una matriz con un elemento diagonal positivo no es necesariamente definida positiva si las derivadas cruzadas introducen indeterminación en el determinante. |
| `D-Hab02-03` | Error de signo en la clasificación del extremo por Legendre | conceptual_swap | high | Dado $F_{\dot{x}\dot{x}} = 2 > 0$, clasificar la trayectoria como un máximo local. | La segunda derivada positiva indica que cualquier desviación en la pendiente incrementa el valor del funcional, configurando un mínimo. |
| `D-Hab02-04` | Omitir la verificación de las derivadas cruzadas en el hessiano | skipped_step | high | Construir $H_F$ asumiendo que los términos fuera de la diagonal siempre se anulan sin calcular $\frac{\partial^2 F}{\partial x \partial \dot{x}}$. | Omitir el cómputo de los términos cruzados puede llevar a clasificaciones erróneas en integrando que contengan términos interactivos como $x\dot{x}$. |
| `D-Hab02-05` | Inversión de criterio de convexidad global | conceptual_swap | high | Al obtener $H_F = \begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix}$ definida positiva, declarar que la trayectoria es un máximo global. | Un funcional convexo evaluado en una extremal que satisface Euler produce un mínimo absoluto sobre el conjunto de trayectorias admisibles. |
| `D-Hab02-06` | Falsa no diferenciabilidad de las condiciones de suficiencia | conceptual_swap | high | Afirmar que no es posible aplicar el teorema de suficiencia porque la función depende implícitamente del tiempo. | La ausencia de dependencia explícita del tiempo o su presencia suave preserva la aplicabilidad de los teoremas de suficiencia variacional clásicos. |

---

### [Hab-03] Resolución analítica y clasificación de funcionales con parámetros y dinámica lineal-cuadrática (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 16: Resolución analítica y clasificación de funcionales con parámetros y dinámica lineal-cuadrática
- **Prerequisites:** Hab-01, Hab-02
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 16)

#### Description & Cognitive Model
Resolver la ecuación de Euler para integrando de la forma $F = bx + a\dot{x}^2 + ct$ con $a < 0$, integrar la trayectoria cuadrática sujeta a $x(0) = x_0$ y $x(t_1) = x_1$, y demostrar que constituye un máximo global mediante Legendre y semidefinición del hessiano.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Error de integración en la aceleración constante | conceptual_swap | high | De $\ddot{x} = \frac{b}{2a}$, integrar incorrectamente como $x(t) = \frac{b}{2a} t^2 + c_1 t + c_2$. | La integral de $\int t dt$ es $\frac{t^2}{2}$, por lo que $\frac{b}{2a} \cdot \frac{t^2}{2} = \frac{b}{4a}t^2$. |
| `D-Hab03-02` | Omitir el signo del parámetro en la condición de Legendre | skipped_step | high | Concluir que como $F_{\dot{x}\dot{x}} = 2a$, la solución es siempre un mínimo local independientemente del signo de $a$. | El signo negativo del parámetro $a$ es determinante para fijar la concavidad del integrando respecto a la velocidad. |
| `D-Hab03-03` | Error en el despeje del coeficiente lineal con condiciones de contorno | conceptual_swap | high | Con $x(0) = 2$ y $x(4) = 4$, obtener $c_1 = \frac{b}{a} + \frac{1}{2}$ en lugar de $c_1 = -(\frac{b}{a} - \frac{1}{2})$. | El despeje cuidadoso del coeficiente de primer orden es indispensable para que la parábola pase exactamente por el punto $(4, 4)$. |
| `D-Hab03-04` | Omitir la derivación respecto al tiempo del término de velocidad en Euler | skipped_step | high | Escribir la ecuación de Euler como $b - 2a\dot{x} = 0$, obteniendo una trayectoria lineal $\dot{x} = \frac{b}{2a}$. | El operador $\frac{d}{dt}$ debe actuar sobre la velocidad $\dot{x}$ para producir la aceleración $\ddot{x}$. |
| `D-Hab03-05` | Confusión en la clasificación del hessiano singular | conceptual_swap | high | Al obtener $H_F = \begin{bmatrix} 0 & 0 \\ 0 & 2a \end{bmatrix}$ con $\det(H_F) = 0$, afirmar que el problema no tiene solución óptima. | Un determinante nulo en el hessiano con curvatura no positiva confirma concavidad débil, lo que valida la condición de suficiencia global. |
| `D-Hab03-06` | Inclusión errónea del término temporal en la ecuación diferencial | conceptual_swap | high | Incluir el término $ct$ en la ecuación diferencial como $b + c - 2a\ddot{x} = 0$. | La dependencia explícita en $t$ se encuentra en un término aditivo puro $ct$, por lo que $\frac{\partial (ct)}{\partial x} = 0$ y $\frac{\partial (ct)}{\partial \dot{x}} = 0$. |

---

### [H-04] Primera Integral e Identidad de Beltrami (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 19: Primera Integral e Identidad de Beltrami
- **Prerequisites:** C-02
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 19)

#### Description & Cognitive Model
En problemas de cálculo de variaciones donde el integrando no depende explícitamente del tiempo ($F_t = 0$), la ecuación de Euler admite la primera integral conocida como identidad de Beltrami: $F - \dot{x} \frac{\partial F}{\partial \dot{x}} = C$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H04-01` | Error de signo en la primera integral | conceptual_swap | high | $F + \dot{x} F_{\dot{x}} = C$ | Confundir el signo negativo del término diferencial al integrar la derivada total respecto al tiempo. |
| `D-H04-02` | Confusión con la ecuación de Euler general | conceptual_swap | high | $\frac{\partial F}{\partial x} - \frac{d}{dt}\frac{\partial F}{\partial \dot{x}} = C$ | Asumir que la primera integral iguala la ecuación diferencial de Euler a una constante en lugar de integrarla. |
| `D-H04-03` | Omisión del factor de velocidad | conceptual_swap | high | $F - \frac{\partial F}{\partial \dot{x}} = C$ | Omitir la multiplicación por $\dot{x}$ en el término de momento conjugado al aplicar la regla del producto. |
| `D-H04-04` | Inversión de variables de estado y derivada | conceptual_swap | high | $\dot{x} - F \frac{\partial F}{\partial x} = C$ | Intercambiar la función integrando con la velocidad e incluir derivadas respecto a la posición $x$. |
| `D-H04-05` | Confusión con el caso sin dependencia de x | conceptual_swap | high | $\frac{\partial F}{\partial \dot{x}} = C$ | Aplicar la condición simplificada para $F_x = 0$ cuando la hipótesis correcta es la ausencia de tiempo explícito $F_t = 0$. |
| `D-H04-06` | Derivada temporal incorrecta | conceptual_swap | high | $F - \dot{x} \frac{\partial F}{\partial \dot{x}} = F_t$ | Igualar la cantidad conservada a la derivada parcial temporal en vez de reconocer que es idénticamente nula e igual a una constante. |

---

### [C-05] Casos Particulares de Reducción de la Ecuación de Euler (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 18: Casos Particulares de Reducción de la Ecuación de Euler
- **Prerequisites:** H-04
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 18)

#### Description & Cognitive Model
Propiedades de reducción del orden o simplificación algebraica de la ecuación de Euler cuando el integrando no contiene la variable de estado $x$ ($\frac{\partial F}{\partial \dot{x}} = c$) o no contiene la derivada $\dot{x}$ ($\frac{\partial F}{\partial x} = 0$).

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Confusión de variables ausentes | conceptual_swap | high | $\frac{\partial F}{\partial x} = c$ | Creer erróneamente que la ausencia de $x$ implica que la derivada respecto a $x$ es constante en lugar de cero. |
| `D-C05-02` | Ecuación diferencial de orden superior innecesaria | conceptual_swap | high | $\frac{d^2 x}{dt^2} = c$ | Integrar dos veces directamente sin aprovechar la primera integral de primer orden inmediata. |
| `D-C05-03` | Planteamiento estático indebido cuando falta la derivada | conceptual_swap | high | $\dot{x} = 0$ | Asumir que si la derivada temporal no figura en el integrando, el estado debe ser constante en el tiempo. |
| `D-C05-04` | Asignación errónea de constante arbitraria | conceptual_swap | high | $\frac{\partial F}{\partial x} = c$ | Igualar $F_x$ a una constante no nula cuando $\dot{x}$ no aparece en el integrando, violando $\frac{\partial F}{\partial \dot{x}} = 0$. |
| `D-C05-05` | Confusión entre ausencia de tiempo y ausencia de estado | conceptual_swap | high | $F - \dot{x} \frac{\partial F}{\partial \dot{x}} = c$ | Usar la identidad de Beltrami para casos donde $F$ no depende de $x$, complejizando el problema. |
| `D-C05-06` | Anulación incorrecta de la función integrando | conceptual_swap | high | $F(x, \dot{x}, t) = 0$ | Confundir la condición de primer orden de Euler con la anulación global del integrando objetivo. |

---

### [C-06] Condición de Transversalidad con Estado Final Libre (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 21: Condición de Transversalidad con Estado Final Libre
- **Prerequisites:** C-05
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 21)

#### Description & Cognitive Model
Fundamento variacional de la condición de contorno natural cuando el estado terminal $x(t_1)$ no está predeterminado en un tiempo $t_1$ fijo, exigiendo la anulación del momento generalizado: $\left.\frac{\partial F}{\partial \dot{x}}\right|_{t=t_1} = 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Confusión con estado terminal nulo | conceptual_swap | high | $x(t_1) = 0$ | Interpretar que estado final no restringido significa que el estado debe ser forzado a cero en el instante final. |
| `D-C06-02` | Confusión con instante final libre | conceptual_swap | high | $\left.\left(F - \dot{x} \frac{\partial F}{\partial \dot{x}}\right)\right|_{t=t_1} = 0$ | Aplicar la condición de transversalidad correspondiente a tiempo terminal libre en un problema donde el tiempo está fijado. |
| `D-C06-03` | Anulación del integrando terminal | conceptual_swap | high | $F(x(t_1), \dot{x}(t_1), t_1) = 0$ | Exigir que la función objetivo se anule en el punto final en lugar de su derivada variacional respecto a la velocidad. |
| `D-C06-04` | Evaluación en el instante inicial | conceptual_swap | high | $\left.\frac{\partial F}{\partial \dot{x}}\right|_{t=t_0} = 0$ | Evaluar la condición de transversalidad en el instante inicial $t_0$ a pesar de que $x(t_0)$ ya tiene una condición fija impuesta. |
| `D-C06-05` | Derivación respecto a la variable de estado | conceptual_swap | high | $\left.\frac{\partial F}{\partial x}\right|_{t=t_1} = 0$ | Confundir el momento conjugado $F_{\dot{x}}$ con la derivada parcial directa respecto al estado $F_x$. |
| `D-C06-06` | Confusión con condición de velocidad terminal nula | conceptual_swap | high | $\dot{x}(t_1) = 0$ | Suponer que el estado final libre implica que la velocidad terminal debe detenerse en $t_1$. |

---

### [Hab-04] Resolución de Problemas Variacionales con Extremo Terminal Libre (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 22: Resolución de Problemas Variacionales con Extremo Terminal Libre
- **Prerequisites:** C-06
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 22)

#### Description & Cognitive Model
Cálculo de la trayectoria óptima $x(t)$ integrando la ecuación de Euler, aplicando la condición de frontera inicial $x(t_0) = x_0$ y determinando la constante libre mediante la condición de transversalidad $\left.\frac{\partial F}{\partial \dot{x}}\right|_{t=t_1} = 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Omisión de la condición de transversalidad | skipped_step | high | $x(t) = -\frac{t^2}{4} + \frac{c}{2}t$ | Dejar la trayectoria dependiendo de una constante arbitraria $c$ sin determinar el valor que anula el momento terminal. |
| `D-Hab04-02` | Aplicación de frontera nula en lugar de transversalidad | skipped_step | high | $x(2) = 0 \Rightarrow x(t) = -\frac{t^2}{4} + \frac{t}{2}$ | Imponer arbitrariamente $x(t_1) = 0$ ante la indicación de que el estado terminal es libre. |
| `D-Hab04-03` | Error de integración en la constante inicial | conceptual_swap | high | $x(0) = c_1 \ne 0$ | Calcular erróneamente la constante $c_1$ a partir de la condición inicial $x(0) = 0$. |
| `D-Hab04-04` | Error algebraico al evaluar el momento conjugado | conceptual_swap | high | $t + 2\dot{x}|_{t=2} = 2 + 2c = 0 \Rightarrow c = -1$ | Sustituir incorrectamente la expresión de $\dot{x}(t)$ al evaluar la derivada variacional en $t=2$. |
| `D-Hab04-05` | Inversión de signo en la solución general | conceptual_swap | high | $x(t) = \frac{t^2}{4}$ | Omitir el signo negativo al despejar la aceleración en la ecuación diferencial de Euler. |
| `D-Hab04-06` | Omisión del cálculo de las constantes de integración | skipped_step | high | $x(t) = -\frac{t^2}{4} + c_1 t + c_2$ | Expresar la familia general de soluciones sin resolver el sistema de ecuaciones para las constantes. |

---

### [C-07] Condición de Transversalidad con Instante Final Libre (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 24: Condición de Transversalidad con Instante Final Libre
- **Prerequisites:** H-04, C-06
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 24)

#### Description & Cognitive Model
Condición de frontera variacional cuando el horizonte temporal final $t_1$ no está predeterminado pero el estado final $x(t_1) = x_1$ es fijo, requiriendo la anulación del Hamiltoniano en el instante terminal: $\left.\left(F - \dot{x}\frac{\partial F}{\partial \dot{x}}\right)\right|_{t=t_1} = 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Confusión con estado final libre | conceptual_swap | high | $\left.\frac{\partial F}{\partial \dot{x}}\right|_{t=t_1} = 0$ | Aplicar la condición para estado libre en vez de la condición hamiltoniana requerida cuando el tiempo es la variable libre. |
| `D-C07-02` | Omisión del producto velocidad-momento | conceptual_swap | high | $F|_{t=t_1} = 0$ | Exigir únicamente que el integrando se anule al final del horizonte, despreciando la contribución de la derivada $\dot{x}$. |
| `D-C07-03` | Signo positivo en la condición terminal | conceptual_swap | high | $\left.\left(F + \dot{x}\frac{\partial F}{\partial \dot{x}}\right)\right|_{t=t_1} = 0$ | Invertir el signo de la transformación de Legendre en la expresión de transversalidad temporal. |
| `D-C07-04` | Evaluación en tiempo inicial | conceptual_swap | high | $\left.\left(F - \dot{x}\frac{\partial F}{\partial \dot{x}}\right)\right|_{t=t_0} = 0$ | Evaluar la condición en el instante $t_0$, donde el tiempo inicial se encuentra estrictamente fijado. |
| `D-C07-05` | Confusión con anulación de la velocidad final | conceptual_swap | high | $\dot{x}(t_1) = 0$ | Suponer erróneamente que un tiempo final no especificado exige que el sistema deba detener su movimiento al llegar a $x_1$. |
| `D-C07-06` | Confusión con derivadas de segundo orden | conceptual_swap | high | $\left.\frac{\partial^2 F}{\partial \dot{x}^2}\right|_{t=t_1} = 0$ | Confundir la condición de transversalidad con la condición de Legendre de segundo orden. |

---

### [Hab-05] Determinación del Horizonte y Trayectoria con Instante Final Libre (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 25: Determinación del Horizonte y Trayectoria con Instante Final Libre
- **Prerequisites:** C-07
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 25)

#### Description & Cognitive Model
Procedimiento conjunto para resolver problemas con $t_1$ libre: integrar la ecuación de Euler, acoplar la condición terminal fija $x(t_1) = x_1$ con la transversalidad $\left.\left(F - \dot{x}F_{\dot{x}}\right)\right|_{t=t_1} = 0$ y despejar el valor del horizonte óptimo $t_1$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Omisión del despeje del horizonte óptimo | skipped_step | high | $t_1^2 - 60 = 0$ | Detener el cálculo en la ecuación cuadrática terminal sin resolver explícitamente para el valor numérico de $t_1$. |
| `D-Hab05-02` | Fijación arbitraria del tiempo terminal | skipped_step | high | $t_1 = 1 \Rightarrow x(t) = \frac{t^2}{12} + 4.9t$ | Asumir un valor arbitrario unitario para el tiempo en lugar de utilizar la condición de transversalidad para hallarlo. |
| `D-Hab05-03` | Error de signo al sustituir la trayectoria en la transversalidad | conceptual_swap | high | $-3c_1^2 + 10 = 0 \Rightarrow c_1 \ne 0$ | Cometer un error algebraico en el desarrollo del binomio de la velocidad terminal $\dot{x}(t_1)$. |
| `D-Hab05-04` | Elección de raíz negativa para el horizonte | conceptual_swap | high | $t_1 = -\sqrt{60}$ | No descartar la solución negativa de la raíz cuadrada en una variable que representa tiempo físico transcurrido. |
| `D-Hab05-05` | Error de integración de la ecuación diferencial | conceptual_swap | high | $x(t) = \frac{t^2}{6} + c_1 t + c_2$ | Omitir el factor $1/2$ al integrar la aceleración $\ddot{x} = 1/6$ dos veces respecto al tiempo. |
| `D-Hab05-06` | Omisión del cálculo de constantes a partir de la condición inicial | skipped_step | high | $x(t) = \frac{t^2}{12} + c_2$ | Asignar erróneamente el valor final $x(t_1)=5$ a la constante inicial $c_2$ en lugar de usar $x(0)=0$. |

---

### [H-05] Estructura del Modelo de Monopolio Dinámico de Evans (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 27: Estructura del Modelo de Monopolio Dinámico de Evans
- **Prerequisites:** C-05
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 27)

#### Description & Cognitive Model
En el modelo de monopolio dinámico de Evans (1924), la demanda depende tanto del precio como de su tendencia temporal, $q = a - bp(t) + h\dot{p}(t)$, planteando la maximización de la ganancia total acumulada $\int_{t_0}^{t_1} [pq - C(q)]dt$ sujeta a condiciones inicial y final de precio.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H05-01` | Omisión de la expectativa del cambio de precio | conceptual_swap | high | $q = a - bp(t)$ | Reducir el modelo dinámico a una función de demanda estática estándar sin término de inercia o expectativa de precios. |
| `D-H05-02` | Confusión de signo en la sensibilidad al cambio de precio | conceptual_swap | high | $q = a - bp(t) - h\dot{p}(t)$ | Invertir el signo del coeficiente de tendencia especulativa en la función de demanda del mercado. |
| `D-H05-03` | Costos de producción lineales | conceptual_swap | high | $C(q) = \beta q + \gamma$ | Omitir el término cuadrático de costos $\alpha q^2$ indispensable para la no linealidad del problema. |
| `D-H05-04` | Inclusión de tasa de descuento intertemporal positiva | conceptual_swap | high | $\int_{t_0}^{t_1} e^{-rt}[pq - C(q)]dt$ | Introducir factor de descuento exponencial cuando el supuesto fundacional del modelo de Evans fija la tasa de descuento en cero. |
| `D-H05-05` | Variable de control errónea en el funcional | conceptual_swap | high | $\max \int_{t_0}^{t_1} [q - C(p)]dt$ | Plantear el funcional de beneficios desconectando el ingreso total de la interacción precio-cantidad. |
| `D-H05-06` | Confusión con problema de horizonte infinito | conceptual_swap | high | $\int_{0}^{\infty} [pq - C(q)]dt$ | Asumir un horizonte infinito no acotado cuando el modelo clásico de Evans fija instantes finitos $t_0$ y $t_1$. |

---

### [Hab-06] Optimización Dinámica del Modelo Trade-off Inflación-Desempleo (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 28: Optimización Dinámica del Modelo Trade-off Inflación-Desempleo
- **Prerequisites:** C-05
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 28)

#### Description & Cognitive Model
Procedimiento para minimizar la pérdida social $\int_0^T \left[\left(\frac{\dot{\pi}}{\beta j}\right)^2 + \alpha\left(\frac{\dot{\pi}}{j} + \pi\right)^2\right]dt$: formular la ecuación de Euler $(1+\beta^2\alpha)\ddot{\pi} - \beta^2 j^2 \alpha \pi = 0$, hallar las raíces características $r = \pm \frac{\beta j \sqrt{\alpha}}{\sqrt{1+\beta^2\alpha}}$ y determinar la trayectoria $\pi(t)$ sujeta a $\pi(0)=\pi_0, \pi(T)=0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Error en la ecuación característica de Euler | skipped_step | high | $r^2 (1+\beta^2\alpha) + \beta^2 j^2 \alpha = 0$ | Invertir el signo entre la segunda derivada y el término de estado al deducir la ecuación diferencial lineal. |
| `D-Hab06-02` | Omisión del cálculo de las raíces características | skipped_step | high | $\pi(t) = c_1 e^{r t} + c_2 e^{-r t}$ | Expresar la solución genérica sin derivar la fórmula analítica explícita de las raíces $r$ en términos de los parámetros estructurales. |
| `D-Hab06-03` | Error al aplicar la condición terminal de inflación nula | conceptual_swap | high | $\pi(T) = c_1 + c_2 = 0 \Rightarrow c_1 = -c_2$ | Evaluar la condición terminal $\pi(T) = 0$ ignorando la dependencia exponencial del tiempo $T$. |
| `D-Hab06-04` | Solución oscilatoria imaginaria incorrecta | conceptual_swap | high | $\pi(t) = c_1 \cos(rt) + c_2 \sin(rt)$ | Asumir soluciones sinusoidales por considerar erróneamente raíces complejas en la ecuación característica. |
| `D-Hab06-05` | Omisión de la ponderación relativa en la función de costo | conceptual_swap | high | $\lambda(\pi, \dot{\pi}) = \dot{\pi}^2 + \pi^2$ | Simplificar arbitrariamente el costo social omitiendo los parámetros de la curva de Phillips $\beta$ y expectativas $j$. |
| `D-Hab06-06` | Omisión del despeje de las constantes de frontera | skipped_step | high | $c_1 + c_2 = \pi_0$ | Plantear solo la suma de constantes inicial sin resolver el sistema lineal acoplado con la condición en $T$. |

---
