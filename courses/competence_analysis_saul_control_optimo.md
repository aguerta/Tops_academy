# Cognitive Task Analysis (CTA): Saul Control Optimo

- **Course ID:** `saul_control_optimo`
- **Macro-Competency:** Dominio y aplicación analítica integral de Saul Control Optimo
- **Structure:** 15 total competencies (3 Facts, 7 Concepts, 5 Skills) with 90 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Funcional y Trayectorias Admisibles en Tiempo Continuo | Concept | Understand | Unidad 5: Funcional y Trayectorias Admisibles en Tiempo Continuo | - | 6 |
| `H-01` | Clasificación de Funcionales de Lagrange, Mayer y Bolza | Fact | Remember | Unidad 8: Clasificación de Funcionales de Lagrange, Mayer y Bolza | C-01 | 6 |
| `C-02` | Ecuación de Euler en el Problema Básico Variacional | Concept | Understand | Unidad 9: Ecuación de Euler en el Problema Básico Variacional | C-01 | 6 |
| `H-02` | Condición de Segundo Orden de Legendre | Fact | Remember | Unidad 10: Condición de Segundo Orden de Legendre | C-02 | 6 |
| `C-03` | Condiciones de Suficiencia Global y Hessiano de F | Concept | Analyze | Unidad 11: Condiciones de Suficiencia Global y Hessiano de F | C-02, H-02 | 6 |
| `Hab-01` | Resolución del Problema Básico Variacional con Extremos Fijos | Skill | Apply | Unidad 14: Resolución del Problema Básico Variacional con Extremos Fijos | C-02, H-02, C-03 | 6 |
| `C-04` | Casos Particulares de la Ecuación de Euler | Concept | Understand | Unidad 18: Casos Particulares de la Ecuación de Euler | C-02 | 6 |
| `H-03` | Identidad de Beltrami para Funcionales Autónomos | Fact | Remember | Unidad 19: Identidad de Beltrami para Funcionales Autónomos | C-04 | 6 |
| `Hab-02` | Integración de Extremos Usando Primeras Integrales de Euler | Skill | Apply | Unidad 20: Integración de Extremos Usando Primeras Integrales de Euler | C-04, H-03, Hab-01 | 6 |
| `C-05` | Condición de Transversalidad para Estado Final Libre | Concept | Understand | Unidad 21: Condición de Transversalidad para Estado Final Libre | C-02, Hab-01 | 6 |
| `Hab-03` | Optimización Variacional con Estado Final Libre | Skill | Apply | Unidad 22: Optimización Variacional con Estado Final Libre | C-05, Hab-01 | 6 |
| `C-06` | Condición de Transversalidad para Instante Final Libre | Concept | Understand | Unidad 24: Condición de Transversalidad para Instante Final Libre | C-02, H-03, Hab-01 | 6 |
| `Hab-04` | Optimización Dinámica con Tiempo Terminal Libre | Skill | Apply | Unidad 25: Optimización Dinámica con Tiempo Terminal Libre | C-06, Hab-01 | 6 |
| `C-07` | Modelado del Monopolio Dinámico de Evans | Concept | Analyze | Unidad 27: Modelado del Monopolio Dinámico de Evans | C-01, C-02 | 6 |
| `Hab-05` | Optimización del Tradeoff Inflación-Desempleo y Trayectoria Óptima | Skill | Apply | Unidad 28: Optimización del Tradeoff Inflación-Desempleo y Trayectoria Óptima | C-02, Hab-01 | 6 |

---

## Detailed Competency Specifications

### [C-01] Funcional y Trayectorias Admisibles en Tiempo Continuo (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 5: Funcional y Trayectorias Admisibles en Tiempo Continuo
- **Prerequisites:** None
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 5)

#### Description & Cognitive Model
Un funcional $V[y] = \int_{t_0}^T F(t, y(t), y'(t)) dt$ es una aplicación cuyo dominio es un conjunto de curvas o trayectorias admisibles $y(t) \in C^1[t_0, T]$ y cuyo codominio es la recta real $\mathbb{R}$, evaluando el valor acumulado de cada arco continuo entre puntos de frontera prefijados.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Confusión entre función y funcional | conceptual_swap | high | Pensar que un funcional asigna un valor escalar a cada instante de tiempo individual $t$ en lugar de evaluar una trayectoria completa $y(t)$ | Un funcional no evalúa puntualmente un instante temporal $t$, sino que cuantifica el desempeño de toda la curva admisible entre los extremos de tiempo. |
| `D-C01-02` | Restricción errónea de regularidad | conceptual_swap | high | Creer que las trayectorias admisibles pueden ser funciones discontinuas arbitrarias sin diferenciabilidad | Para poder calcular la integral del funcional que incluye la velocidad $\dot{y}(t)$, la curva debe admitir derivada en casi todo el intervalo. |
| `D-C01-03` | Confusión con optimización estática | conceptual_swap | high | Considerar que optimizar un funcional es idéntico a maximizar una función multivariada sobre variables estáticas independientes | En optimización dinámica, la decisión en un punto altera la posición futura mediante la velocidad $\dot{y}(t)$, impidiendo optimizar cada instante por separado. |
| `D-C01-04` | Inversión de dominio y codominio | conceptual_swap | high | Pensar que el funcional toma un número real y devuelve como salida una trayectoria continua | El funcional asigna un número escalar representativo del costo o beneficio acumulado a cada trayectoria candidata, no una función a un número. |
| `D-C01-05` | Ignorancia de las condiciones de frontera | conceptual_swap | high | Creer que el conjunto de trayectorias admisibles incluye curvas que no pasan por los puntos prescritos $(t_0, y_0)$ y $(T, y_T)$ | Si una trayectoria no interseca los puntos de frontera inicial y terminal fijados en el planteamiento, queda excluida del espacio admisible. |
| `D-C01-06` | Confusión entre valor de arco y valor de trayectoria | conceptual_swap | high | Asumir que el valor del funcional $V[y]$ coincide con el valor del integrando en el punto inicial $F(t_0, y(t_0), \dot{y}(t_0))$ | El funcional acumula los aportes diferenciales $F dt$ sobre toda la duración del proceso dinámico y no se restringe a la etapa de partida. |

---

### [H-01] Clasificación de Funcionales de Lagrange, Mayer y Bolza (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 8: Clasificación de Funcionales de Lagrange, Mayer y Bolza
- **Prerequisites:** C-01
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 8)

#### Description & Cognitive Model
Identificación canónica de los tres formatos estándar de problemas variacionales: Problema de Lagrange $V[y] = \int_0^T F[t, y(t), y'(t)]dt$, Problema de Mayer $V[y] = G(T, y(T))$ y Problema de Bolza $V[y] = \int_0^T F[t, y(t), y'(t)]dt + G(T, y(T))$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Confusión entre Lagrange y Mayer | conceptual_swap | high | Clasificar un funcional compuesto exclusivamente por una integral definida $\int_0^T F dt$ como un problema de Mayer | El problema de Lagrange acumula valores a lo largo del trayecto continuo, mientras que Mayer solo remunera la posición al cierre del horizonte. |
| `D-H01-02` | Identificación errónea del problema de Bolza | conceptual_swap | high | Creer que el problema de Bolza contiene únicamente una función de valor terminal sin término integral acumulativo | Bolza combina ambos componentes: la acumulación continua de flujo en el intervalo y el pago o penalidad terminal en el instante final. |
| `D-H01-03` | Asimilación indebida de Lagrange a Bolza sin término terminal | conceptual_swap | high | Catalogar un funcional como problema de Bolza irreducible aun cuando la función terminal $G(T, y(T))$ sea nula | Sin una función de pago terminal explícita, el problema de optimización pertenece por definición a la clase de Lagrange. |
| `D-H01-04` | Confusión en el argumento de la función terminal de Mayer | conceptual_swap | high | Pensar que la función de Mayer $G$ depende de la derivada terminal $\dot{y}(T)$ en vez del nivel de la variable de estado $y(T)$ | La función terminal de Mayer evalúa el estado alcanzado al final del proceso y no la tasa instantánea de cambio con la que se arriba. |
| `D-H01-05` | Inclusión impropia de integrales en problemas de Mayer | conceptual_swap | high | Afirmar que un problema de Mayer puede integrar funciones continuas intermedias sin perder su denominación | Cualquier adición de un operador integral en la función objetivo transforma la estructura en un problema de tipo Bolza. |
| `D-H01-06` | Confusión en la variable de integración temporal | conceptual_swap | high | Creer que en el problema de Lagrange la integral se formula respecto a la variable de estado $y$ en lugar del tiempo $t$ | El diferencial de integración en la formulación de Lagrange es el tiempo $dt$, sumando las contribuciones instantáneas en $[0, T]$. |

---

### [C-02] Ecuación de Euler en el Problema Básico Variacional (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 9: Ecuación de Euler en el Problema Básico Variacional
- **Prerequisites:** C-01
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 9)

#### Description & Cognitive Model
Condición necesaria de primer orden para que una trayectoria suave $x^*(t)$ proporcione un extremo local al funcional $J(x) = \int_{t_0}^{t_1} F(x, \dot{x}, t)dt$: $F_x - \frac{d}{dt}F_{\dot{x}} = 0$, que al desarrollarse adopta la forma diferencial de segundo orden $F_x - F_{x\dot{x}}\dot{x} - F_{\dot{x}\dot{x}}\ddot{x} - F_{\dot{x}t} = 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Error de signo en la derivada temporal del momento | conceptual_swap | high | Formular la ecuación de Euler sumando en lugar de restar la derivada temporal total de $F_{\dot{x}}$: $F_x + \frac{d}{dt}F_{\dot{x}} = 0$ | Al aplicar el lema fundamental del cálculo de variaciones, el término $\int F_{\dot{x}}\dot{\eta}dt$ se integra por partes produciendo $-\int \frac{d}{dt}(F_{\dot{x}})\eta dt$. |
| `D-C02-02` | Confusión entre derivada total y derivada parcial temporal | conceptual_swap | high | Reemplazar la derivada total $\frac{d}{dt}F_{\dot{x}}$ por la derivada parcial $\frac{\partial}{\partial t}F_{\dot{x}}$, omitiendo la regla de la cadena | Dado que $x(t)$ y $\dot{x}(t)$ varían en el tiempo a lo largo de la trayectoria, la derivada temporal total debe incluir todas las dependencias intermedias. |
| `D-C02-03` | Pretensión errónea de suficiencia | conceptual_swap | high | Creer que verificar la ecuación de Euler basta para garantizar que la trayectoria sea un óptimo global sin comprobar curvatura | Euler es el análogo a igualar la primera derivada a cero; se requieren condiciones de curvatura (segundo orden o concavidad/convexidad) para calificar el extremo. |
| `D-C02-04` | Error en el orden diferencial de la ecuación de Euler | conceptual_swap | high | Suponer que la ecuación de Euler es invariablemente una ecuación diferencial de primer orden para cualquier integrando $F$ | La aceleración $\ddot{x}$ ingresa a través de la diferenciación de la velocidad en la regla de la cadena, haciendo que la EDO sea de segundo orden. |
| `D-C02-05` | Omisión de la derivada respecto al estado | conceptual_swap | high | Limitar la condición de Euler a exigir que la derivada respecto a la velocidad sea constante, omitiendo el término $F_x$ | Despreciar el impacto del nivel del estado $F_x$ solo es lícito en casos particulares donde la función objetivo no contiene la posición $x$. |
| `D-C02-06` | Inversión de los roles de las derivadas de posición y velocidad | conceptual_swap | high | Escribir la ecuación de Euler aplicando la derivada temporal a $F_x$ en vez de a $F_{\dot{x}}$: $F_{\dot{x}} - \frac{d}{dt}F_x = 0$ | La integración por partes se efectúa sobre la función cuya variación está derivada en el tiempo ($\dot{\eta}$), transfiriendo el operador $\frac{d}{dt}$ a $F_{\dot{x}}$. |

---

### [H-02] Condición de Segundo Orden de Legendre (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 10: Condición de Segundo Orden de Legendre
- **Prerequisites:** C-02
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 10)

#### Description & Cognitive Model
Condición necesaria local de segundo orden para extremales del problema básico: para que $x^*(t)$ sea un máximo local se exige $F_{\dot{x}\dot{x}}[x^*(t), \dot{x}^*(t), t] \le 0$ para todo $t \in [t_0, t_1]$, y para que sea un mínimo local se exige $F_{\dot{x}\dot{x}}[x^*(t), \dot{x}^*(t), t] \ge 0$ para todo $t \in [t_0, t_1]$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H02-01` | Inversión de desigualdades entre máximo y mínimo | conceptual_swap | high | Postular que un máximo local exige $F_{\dot{x}\dot{x}} \ge 0$ y que un mínimo local requiere $F_{\dot{x}\dot{x}} \le 0$ | De modo análogo al cálculo diferencial elemental donde $f''(x) \le 0$ caracteriza un máximo, la segunda derivada respecto a la velocidad debe ser no positiva. |
| `D-H02-02` | Confusión de variable en el criterio de Legendre | conceptual_swap | high | Evaluar la condición de Legendre sobre la segunda derivada respecto al estado $F_{xx}$ en lugar de respecto a la velocidad $F_{\dot{x}\dot{x}}$ | Legendre aísla variaciones de alta frecuencia concentradas en la derivada $\dot{x}$, por lo que la derivada determinante es $F_{\dot{x}\dot{x}}$. |
| `D-H02-03` | Atribución de suficiencia global a la condición de Legendre | conceptual_swap | high | Asumir que la verificación estricta de $F_{\dot{x}\dot{x}} < 0$ garantiza por sí sola la existencia de un máximo global del problema | Legendre solo comprueba la curvatura en la dirección de la velocidad; si la interacción cruzada con la posición es desfavorable, el punto puede no ser extremo. |
| `D-H02-04` | Evaluación puntual aislada en lugar de intervalo completo | conceptual_swap | high | Creer que la condición de Legendre solo necesita comprobarse en los instantes inicial y final $t_0, t_1$ | Si en algún instante intermedio del intervalo la segunda derivada $F_{\dot{x}\dot{x}}$ cambia de signo, la trayectoria deja de calificar como extremal. |
| `D-H02-05` | Confusión con el determinante de la matriz Hessiana | conceptual_swap | high | Definir la condición de Legendre como la exigencia sobre el signo del determinante completo de la matriz Hessiana | Legendre analiza el coeficiente principal de la segunda variación de la integral, que corresponde al término cuadrático en $\dot{\eta}$, es decir $F_{\dot{x}\dot{x}}$. |
| `D-H02-06` | Uso de derivadas de orden superior a dos | conceptual_swap | high | Considerar que la condición de Legendre examina derivadas de tercer orden del integrando $F$ | La segunda variación del funcional solo contiene términos cuadráticos en $\eta$ y $\dot{\eta}$, dependiendo exclusivamente de derivadas segundas. |

---

### [C-03] Condiciones de Suficiencia Global y Hessiano de F (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 11: Condiciones de Suficiencia Global y Hessiano de F
- **Prerequisites:** C-02, H-02
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 11)

#### Description & Cognitive Model
Si la función integrando $F(x, \dot{x}, t)$ es cóncava (respectivamente convexa) en $(x, \dot{x})$ para cada $t \in [t_0, t_1]$, toda trayectoria $x^*(t)$ que satisfaga la ecuación de Euler y las condiciones de frontera es un máximo (o mínimo) global; dicha propiedad se comprueba mediante la matriz hessiana $H_F = \begin{bmatrix} F_{xx} & F_{x\dot{x}} \\ F_{\dot{x}x} & F_{\dot{x}\dot{x}} \end{bmatrix}$ semidefinida negativa o positiva.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Error en el criterio del determinante para matrices definidas negativas | conceptual_swap | high | Afirmar que para concavidad estricta tanto el menor $F_{xx}$ como el determinante $\det(H_F)$ deben ser estrictamente negativos | El determinante de una matriz $2 \times 2$ definida negativa es el producto de dos autovalores estrictamente negativos, por lo que resulta siempre positivo. |
| `D-C03-02` | Inversión de curvatura para mínimos globales | conceptual_swap | high | Exigir que el integrando $F(x, \dot{x}, t)$ sea una función cóncava para garantizar que la trayectoria extremal constituya un mínimo global | La concavidad garantiza cotas superiores y máximos globales; para acotar inferiormente y asegurar mínimos globales la función debe ser convexa. |
| `D-C03-03` | Inclusión indebida del tiempo en la matriz Hessiana | conceptual_swap | high | Construir la matriz Hessiana derivando respecto a las tres variables $(x, \dot{x}, t)$ en una matriz de tamaño $3 \times 3$ | El tiempo $t$ es el índice de acumulación temporal y no una variable de elección del estado; el Hessiano de suficiencia es estrictamente $2 \times 2$. |
| `D-C03-04` | Rechazo injustificado de suficiencia con determinante nulo | conceptual_swap | high | Declarar que el criterio de suficiencia no concluye si $\det(H_F) = 0$ aun cuando $F_{xx} \le 0$ y $F_{\dot{x}\dot{x}} \le 0$ | La convexidad o concavidad no estricta (semidefinida) es plenamente suficiente para demostrar que la solución de Euler es un extremo global. |
| `D-C03-05` | Sustitución ilegítima del Hessiano por la condición de Legendre | conceptual_swap | high | Concluir que $F$ es globalmente convexa basándose únicamente en que $F_{\dot{x}\dot{x}} > 0$ sin evaluar $F_{xx}$ ni los términos cruzados | La curvatura multivariada exige evaluar la interacción de todas las segundas derivadas; el signo de una sola derivada diagonal no garantiza convexidad conjunta. |
| `D-C03-06` | Inversión de signos en la definición de matriz definida positiva | conceptual_swap | high | Creer que una matriz es definida positiva si su diagonal es positiva y su determinante es estrictamente negativo | Un determinante negativo indica que los autovalores tienen signos opuestos, correspondiendo a un punto de ensilladura o matriz indefinida. |

---

### [Hab-01] Resolución del Problema Básico Variacional con Extremos Fijos (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 14: Resolución del Problema Básico Variacional con Extremos Fijos
- **Prerequisites:** C-02, H-02, C-03
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 14)

#### Description & Cognitive Model
Deducción y solución analítica de trayectorias óptimas en problemas básicos de cálculo variacional mediante la formulación de la ecuación de Euler, integración diferencial con constantes $c_1, c_2$, fijación por extremos prescritos $x(t_0)=x_0$ y $x(t_1)=x_1$, y validación con Legendre y suficiencia.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Error de raíces en el polinomio característico de Euler | skipped_step | high | Para la ecuación $\ddot{x} - x = 0$, suponer raíces repetidas y escribir erróneamente la solución general como $x(t) = c_1 e^t + c_2 t e^t$ | La ecuación diferencial lineal de segundo orden con raíces simples $\pm 1$ se resuelve como combinación lineal de exponenciales independientes. |
| `D-Hab01-02` | Omisión del ajuste por condiciones de frontera fijas | skipped_step | high | Dejar la trayectoria expresada en términos de constantes indeterminadas $c_1, c_2$ sin despejarlas con los valores extremos dados | Un problema con condiciones de contorno fijas requiere explicitar numéricamente las constantes de integración para individualizar la trayectoria. |
| `D-Hab01-03` | Asignación prematura de constantes sin resolver el sistema simultáneo | conceptual_swap | high | Al evaluar $x(0) = c_1 + c_2 = 1$, asumir arbitrariamente $c_1 = 1$ y $c_2 = 0$ ignorando la ecuación del extremo terminal $x(1) = e$ | No se pueden inferir las constantes por separado; debe plantearse el sistema $2 \times 2$ para despejar unívocamente $c_1 = 0$ y $c_2 = 1$. |
| `D-Hab01-04` | Omisión de verificación de las condiciones de segundo orden | skipped_step | high | Dar por resuelto el problema de optimización al hallar la trayectoria de Euler sin verificar Legendre ni el Hessiano de suficiencia | Hallar un punto estacionario mediante Euler no garantiza optimalidad; se debe contrastar el signo de las derivadas segundas. |
| `D-Hab01-05` | Error en la derivada parcial de potencia de la velocidad | conceptual_swap | high | Calcular la derivada parcial de un término cuadrático $\dot{x}^2$ como $\dot{x}$ en lugar de $2\dot{x}$ al armar la ecuación de Euler | Un error en el coeficiente diferencial altera los autovalores y raíces de la ecuación diferencial, invalidando la trayectoria resultante. |
| `D-Hab01-06` | Falta de división por dos en la doble integración temporal | conceptual_swap | high | Integrar la aceleración constante $\ddot{x} = \frac{b}{2a}$ como $x(t) = \frac{b}{2a}t^2 + c_1 t + c_2$ olvidando el factor de integración de $t$ | La integral de $t dt$ introduce un factor $\frac{1}{2}$, transformando el denominador de $2a$ en $4a$ en el término cuadrático de la trayectoria. |

---

### [C-04] Casos Particulares de la Ecuación de Euler (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 18: Casos Particulares de la Ecuación de Euler
- **Prerequisites:** C-02
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 18)

#### Description & Cognitive Model
Reducciones analíticas de la ecuación de Euler según la ausencia explícita de variables en el integrando: si $F$ no depende de $x$, se obtiene la primera integral $F_{\dot{x}} = c$; si $F$ no depende de $\dot{x}$, se obtiene la relación finita $F_x = 0$; y si $F$ es autónomo (no depende explícitamente de $t$), rige la conservación de Beltrami $F - \dot{x}F_{\dot{x}} = C$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Confusión del caso sin variable de estado | conceptual_swap | high | Creer que si el integrando no depende de $x$, la trayectoria óptima debe ser necesariamente una constante fija $x(t) = k$ | La derivada constante implica que la velocidad $\dot{x}$ es fija o predecible, no que el estado no se desplace en el tiempo. |
| `D-C04-02` | Confusión del caso sin velocidad en el integrando | conceptual_swap | high | Pensar que si el integrando no contiene $\dot{x}$, el problema genera una ecuación diferencial ordinaria de segundo orden estándar | Sin la derivada temporal, el problema pierde su naturaleza diferencial y se resuelve puntualmente en cada instante como un óptimo estático. |
| `D-C04-03` | Sobredeterminación de contornos en ausencia de derivadas | conceptual_swap | high | Asumir que cuando la solución óptima es una curva rígida $F_x(x, t) = 0$, siempre se pueden imponer extremos arbitrarios $x(t_0)=a$ y $x(t_1)=b$ | Una relación algebraica fija no posee grados de libertad para forzar la curva a través de puntos predeterminados independientes. |
| `D-C04-04` | Aplicación indebida de Beltrami a funcionales no autónomos | conceptual_swap | high | Aplicar la conservación $F - \dot{x}F_{\dot{x}} = C$ a problemas donde el integrando $F$ incluye explícitamente el tiempo $t$ | Si el tiempo aparece de forma explícita en el integrando, la derivada total de la cantidad es $\frac{d}{dt}(F - \dot{x}F_{\dot{x}}) = \frac{\partial F}{\partial t} \ne 0$. |
| `D-C04-05` | Error en la derivada temporal de la expresión de Beltrami | conceptual_swap | high | Afirmar que al derivar $F - \dot{x}F_{\dot{x}}$ respecto al tiempo no se cancelan los términos en aceleración | La identidad de Beltrami se fundamenta en la anulación mutua entre $\dot{x}\frac{d}{dt}F_{\dot{x}}$ y $\dot{x}F_x$ gracias a la dinámica de Euler. |
| `D-C04-06` | Tratamiento estático de la velocidad en la primera integral | conceptual_swap | high | Asumir que en la primera integral $F_{\dot{x}} = c$, la velocidad $\dot{x}$ puede tratarse como un parámetro numérico desacoplado de $x(t)$ | La primera integral reduce el orden de dos a uno, pero continúa siendo una relación diferencial entre la posición y el tiempo. |

---

### [H-03] Identidad de Beltrami para Funcionales Autónomos (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 19: Identidad de Beltrami para Funcionales Autónomos
- **Prerequisites:** C-04
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 19)

#### Description & Cognitive Model
Primera integral fundamental del cálculo de variaciones: para funcionales donde el integrando no depende explícitamente del tiempo ($\frac{\partial F}{\partial t} = 0$), se conserva a lo largo de toda trayectoria extremal la cantidad $F(x, \dot{x}) - \dot{x}\frac{\partial F}{\partial \dot{x}} = C$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H03-01` | Error de signo en la combinación hamiltoniana de Beltrami | conceptual_swap | high | Escribir la identidad de Beltrami sumando el producto de la velocidad por el momento conjugado: $F + \dot{x}F_{\dot{x}} = C$ | La transformación de Legendre que define la energía o Hamiltoniano conservado $-H = F - \dot{x}F_{\dot{x}}$ contiene obligatoriamente un signo negativo. |
| `D-H03-02` | Multiplicación de la velocidad por la derivada incorrecta | conceptual_swap | high | Formular la identidad de Beltrami multiplicando la velocidad por la derivada respecto al estado: $F - \dot{x}F_x = C$ | El momento canónico generalizado es $p = F_{\dot{x}}$; por ende la cantidad conservada vincula $\dot{x}F_{\dot{x}}$ y no la derivada respecto a la posición. |
| `D-H03-03` | Presuposición de constante nula universal | conceptual_swap | high | Creer que la constante de Beltrami $C$ debe ser idénticamente cero en cualquier problema variacional autónomo | Solo en problemas con tiempo terminal libre la condición de transversalidad fija $C = 0$; en extremos fijos $C$ adopta cualquier magnitud real. |
| `D-H03-04` | Confusión sobre la condición de autonomía del funcional | conceptual_swap | high | Afirmar que la identidad de Beltrami requiere que el integrando no dependa de la variable de estado $x$ | Autonomía significa invarianza temporal ante traslaciones en $t$, permitiendo dependencias funcionales arbitrarias en la posición $x$ y velocidad $\dot{x}$. |
| `D-H03-05` | Sustitución de velocidad por aceleración en la formulación | conceptual_swap | high | Escribir la identidad de Beltrami incorporando la aceleración de segundo orden: $F - \ddot{x}F_{\dot{x}} = C$ | La magnitud $F - \dot{x}F_{\dot{x}}$ es dimensionalmente homogénea y reduce el orden diferencial del problema al involucrar solo $\dot{x}$. |
| `D-H03-06` | Confusión entre conservación del integrando y de Beltrami | conceptual_swap | high | Suponer que para un integrando autónomo el propio valor de $F(x(t), \dot{x}(t))$ permanece constante a lo largo del tiempo | Salvo casos triviales, $F$ cambia continuamente de valor a lo largo de la curva; la integral primera es la estructura combinada hamiltoniana. |

---

### [Hab-02] Integración de Extremos Usando Primeras Integrales de Euler (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 20: Integración de Extremos Usando Primeras Integrales de Euler
- **Prerequisites:** C-04, H-03, Hab-01
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 20)

#### Description & Cognitive Model
Resolución expedita de problemas variacionales mediante la identificación y aplicación directa de primeras integrales ($F_{\dot{x}} = c$ y $F - \dot{x}F_{\dot{x}} = C$), reduciendo la EDO de segundo orden a primer orden para obtener trayectorias analíticas mediante cuadraturas.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Error de integración en casos lineales sin variable de estado | skipped_step | high | Para el funcional con integrando $F = t^2 - \dot{x}^2$, obtener $F_{\dot{x}} = -2\dot{x} = c$ e integrar cuadráticamente como $x(t) = c t^2 + c_2$ | La integral de una constante respecto al tiempo produce una función lineal en $t$, no un término cuadrático. |
| `D-Hab02-02` | Omisión de comprobación de consistencia en problemas rígidos | skipped_step | high | Al resolver $\min \int_0^1 (t+x)^2 dt$, afirmar que existe solución continua para cualquier par arbitrario de extremos $x(0)=a$ y $x(1)=b$ | Cuando la optimización produce una curva rígida sin constantes de integración, las condiciones de frontera deben coincidir estrictamente con los puntos de la curva. |
| `D-Hab02-03` | Error algebraico en el signo del momento en funcionales cuadráticos | conceptual_swap | high | Para $F = 2 - 3x\dot{x}^2$, calcular erróneamente $F - \dot{x}F_{\dot{x}} = (2 - 3x\dot{x}^2) - 6x\dot{x}^2 = 2 - 9x\dot{x}^2$ | Al restar un término negativo $(-6x\dot{x}^2)$ la operación se convierte en adición, cambiando el signo a $+3x\dot{x}^2$. |
| `D-Hab02-04` | Olvido de la constante de integración en separación de variables | skipped_step | high | Al separar variables en $\sqrt{x}dx = k dt$, omitir la constante aditiva de integración secundaria al calcular $x(t)$ | Una ecuación de segundo orden reducida a primer orden requiere dos constantes totales para ajustarse a las dos condiciones de contorno. |
| `D-Hab02-05` | Confusión entre signo de la constante y carácter del extremo | conceptual_swap | high | Afirmar que una constante de integración negativa invalida que la trayectoria constituya un mínimo del funcional | El carácter de óptimo depende de la curvatura del funcional y no de si la trayectoria tiene pendiente o posición negativa. |
| `D-Hab02-06` | Uso de derivadas implícitas espurias en el cálculo de Euler | conceptual_swap | high | Diferenciar $t^2 - \dot{x}^2$ respecto a $x$ como si contuviera una derivada implícita respecto a la posición | En el cálculo variacional, las derivadas parciales de $F$ se computan tratando a cada argumento de forma desacoplada. |

---

### [C-05] Condición de Transversalidad para Estado Final Libre (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 21: Condición de Transversalidad para Estado Final Libre
- **Prerequisites:** C-02, Hab-01
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 21)

#### Description & Cognitive Model
En problemas variacionales con horizonte temporal fijo $t_1$ pero estado terminal no restringido ($x(t_1) = \text{libre}$), la condición de frontera natural o transversalidad exige anular la derivada parcial respecto a la velocidad en el instante terminal: $\left. \frac{\partial F}{\partial \dot{x}} \right|_{t=t_1} = 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Confusión de orden de frontera en estado libre | conceptual_swap | high | Exigir que la variable de estado se anule al final $x(t_1) = 0$ cuando el enunciado establece que el estado final es libre | Libre implica que el sistema optimiza la altura terminal a conveniencia, lo que se traduce matemáticamente en la anulación del momento $F_{\dot{x}}$ en $t_1$. |
| `D-C05-02` | Evaluación de transversalidad en el instante inicial | conceptual_swap | high | Evaluar la condición de transversalidad en el instante de partida $t=t_0$ en lugar de en la frontera libre $t=t_1$ | La transversalidad suple la ausencia de fijación de contorno exactamente en el borde donde la variación $\eta(t_1)$ es arbitraria. |
| `D-C05-03` | Confusión con transversalidad de tiempo final libre | conceptual_swap | high | Aplicar la condición hamiltoniana $\left. [F - \dot{x}F_{\dot{x}}] \right|_{t=t_1} = 0$ cuando el tiempo $t_1$ está prefijado y el estado es libre | Mover la frontera verticalmente genera el término de momento $F_{\dot{x}}$, mientras que moverla horizontalmente en el tiempo genera el término hamiltoniano. |
| `D-C05-04` | Creencia errónea de invalidación de la ecuación de Euler | conceptual_swap | high | Suponer que tener un estado final libre libera a la trayectoria de satisfacer la ecuación de Euler en el interior del intervalo | La condición de transversalidad solo aporta una ecuación de contorno en el extremo; la trayectoria interna sigue gobernada por Euler. |
| `D-C05-05` | Anulación de la derivada respecto a la posición en la frontera | conceptual_swap | high | Proponer como condición de transversalidad que la derivada de posición se anule en el extremo final: $\left. F_x \right|_{t=t_1} = 0$ | El factor que acompaña a la variación libre en los límites de integración por partes es el momento conjugado $F_{\dot{x}}$, no $F_x$. |
| `D-C05-06` | Asimetría de signos según el tipo de extremo | conceptual_swap | high | Afirmar que en problemas de minimización la condición de transversalidad de estado libre exige $F_{\dot{x}}|_{t_1} > 0$ | Sin restricciones de desigualdad en la cota final, la condición de estacionariedad obliga a que la pendiente de la primera variación sea cero. |

---

### [Hab-03] Optimización Variacional con Estado Final Libre (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 22: Optimización Variacional con Estado Final Libre
- **Prerequisites:** C-05, Hab-01
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 22)

#### Description & Cognitive Model
Procedimiento integral para determinar la trayectoria extremal y el nivel óptimo terminal $x^*(t_1)$ resolviendo la ecuación de Euler acoplada a la condición inicial fija $x(t_0)=x_0$ y la condición de transversalidad terminal $F_{\dot{x}}|_{t=t_1} = 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Evaluación temporal incorrecta de la transversalidad en la velocidad | skipped_step | high | Para $\min \int_0^2 [t\dot{x} + \dot{x}^2]dt$, evaluar la condición $t + 2\dot{x} = 0$ en $t=0$ en lugar de en el instante final libre $t=2$ | La transversalidad sustituye la condición de contorno ausente en el extremo terminal y debe evaluarse obligatoriamente en $t=2$. |
| `D-Hab03-02` | Error fraccionario al integrar la velocidad lineal | skipped_step | high | Al integrar la ecuación $\dot{x} = -\frac{t}{2} + \frac{c}{2}$, escribir $x(t) = -t^2 + ct + c_1$ omitiendo los denominadores | Al integrar una variable lineal con coeficiente fraccionario se debe multiplicar el denominador por el nuevo exponente 2. |
| `D-Hab03-03` | Fusión errónea de constantes de integración independientes | conceptual_swap | high | Asumir que la constante de momento $c$ y la constante de posición $c_1$ deben ser numéricamente idénticas antes de aplicar condiciones | Cada constante atiende a una exigencia distinta: una ancla el origen espacial y la otra calibra la inclinación óptima de llegada. |
| `D-Hab03-04` | Omisión del cálculo del valor terminal óptimo alcanzado | skipped_step | high | Concluir el ejercicio reportando la fórmula $x(t) = -\frac{t^2}{4}$ sin calcular explícitamente el nivel final alcanzado $x(2)$ | La solución óptima queda incompleta si no se especifica el estado terminal que el sistema dinámico eligió libremente alcanzar. |
| `D-Hab03-05` | Cálculo defectuoso de la condición de Legendre con términos mixtos | conceptual_swap | high | Calcular $\frac{\partial^2 F}{\partial \dot{x}^2}$ como función dependiente del tiempo $t$ a partir del término cruzado $t\dot{x}$ | El término $t\dot{x}$ tiene grado uno en $\dot{x}$, por lo que al derivarlo dos veces respecto a la velocidad se anula por completo. |
| `D-Hab03-06` | Restricción infundada de optimalidad a carácter puramente local | conceptual_swap | high | Afirmar que un estado libre impide que la solución de Euler sea un mínimo global | La suficiencia global se deriva de la curvatura del integrando en todo el espacio y abarca tanto problemas con extremos fijos como libres. |

---

### [C-06] Condición de Transversalidad para Instante Final Libre (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 24: Condición de Transversalidad para Instante Final Libre
- **Prerequisites:** C-02, H-03, Hab-01
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 24)

#### Description & Cognitive Model
En problemas de optimización variacional donde el estado terminal está prefijado $x(t_1) = x_1$ pero el instante final es libre ($t_1 = \text{libre}$), la condición de transversalidad exige la anulación del valor hamiltoniano en la frontera móvil: $\left. [F - \dot{x} F_{\dot{x}}] \right|_{t=t_1} = 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Confusión con la transversalidad de estado libre | conceptual_swap | high | Postular que para instante final libre la condición de transversalidad es la anulación de la derivada de velocidad $\left. F_{\dot{x}} \right|_{t=t_1} = 0$ | Variar el extremo horizontal temporal introduce la variación del límite integral mediante la regla de Leibniz, originando $F - \dot{x}F_{\dot{x}}$. |
| `D-C06-02` | Error de signo en la expresión de la energía terminal | conceptual_swap | high | Escribir la transversalidad temporal sumando el momento: $\left. [F + \dot{x}F_{\dot{x}}] \right|_{t=t_1} = 0$ | La formulación correcta de la energía terminal requiere el signo negativo para equilibrar la tasa de variación temporal del límite superior. |
| `D-C06-03` | Admisión de horizontes temporales negativos no causales | conceptual_swap | high | Aceptar como duración temporal válida un valor negativo $t_1 < 0$ que anule algebraicamente la ecuación cuadrática de frontera | Una integral temporal con límite final menor al inicial invierte el sentido físico del proceso dinámico y carece de validez. |
| `D-C06-04` | Extensión indebida de la transversalidad terminal a todo el intervalo | conceptual_swap | high | Pensar que $[F - \dot{x}F_{\dot{x}}] = 0$ rige en todo $t \in [t_0, t_1]$ aun cuando el integrando dependa explícitamente del tiempo | La transversalidad es una condición de contorno de frontera y no una identidad diferencial en todo el intervalo si hay dependencia temporal explícita. |
| `D-C06-05` | Descarte de la condición de posición terminal fija | conceptual_swap | high | Creer que al ser el instante final $t_1$ libre, ya no es necesario satisfacer la cota de estado $x(t_1) = x_1$ | Tener tiempo libre significa elegir el momento óptimo para llegar a un destino previamente fijado, manteniendo la exigencia sobre el estado final. |
| `D-C06-06` | Sustitución de la velocidad por la aceleración en la transversalidad | conceptual_swap | high | Plantear la transversalidad de tiempo libre como $\left. [F - \ddot{x}F_{\dot{x}}] \right|_{t=t_1} = 0$ | El diferencial de posición inducido por el desplazamiento temporal $dt_1$ se relaciona mediante la pendiente $\dot{x} = \frac{dx}{dt}$. |

---

### [Hab-04] Optimización Dinámica con Tiempo Terminal Libre (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 25: Optimización Dinámica con Tiempo Terminal Libre
- **Prerequisites:** C-06, Hab-01
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 25)

#### Description & Cognitive Model
Cálculo acoplado de la trayectoria óptima $x^*(t)$ y del horizonte temporal óptimo $t_1^*$ mediante la resolución simultánea de la ecuación de Euler, la condición de contorno terminal $x(t_1)=x_1$ y la condición de transversalidad $[F - \dot{x}F_{\dot{x}}]|_{t=t_1} = 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Error algebraico al formular la expresión hamiltoniana | skipped_step | high | Para el problema $\min \int_0^{t_1} [3\dot{x}^2 + x]dt$, evaluar $F - \dot{x}F_{\dot{x}}$ como $3\dot{x}^2 + x - 3\dot{x}^2 = x$ | La derivada parcial de $3\dot{x}^2$ respecto a la velocidad es $6\dot{x}$, por lo que el producto resta $6\dot{x}^2$, dejando un término neto en $-3\dot{x}^2$. |
| `D-Hab04-02` | Desacoplamiento erróneo del sistema no lineal de frontera | skipped_step | high | Intentar resolver el tiempo final $t_1$ de forma aislada sin sustituir la constante $c_1$ deducida de la transversalidad | El horizonte temporal y las constantes de integración forman un sistema no lineal simultáneo que debe resolverse en estrecho acoplamiento. |
| `D-Hab04-03` | Error en el coeficiente al integrar aceleración constante | conceptual_swap | high | A partir de $1 - 6\ddot{x} = 0 \implies \ddot{x} = \frac{1}{6}$, integrar como $x(t) = \frac{t^2}{6} + c_1 t + c_2$ | Al integrar el término lineal $\frac{t}{6}$ se multiplica el denominador por dos, obteniendo $\frac{t^2}{12}$. |
| `D-Hab04-04` | Omisión del descarte causal de la raíz temporal negativa | skipped_step | high | Elegir la raíz negativa $t_1 = -\sqrt{60}$ argumentando que minimiza algebraicamente la variable temporal | Las soluciones con tiempo negativo violan la direccionalidad del proceso dinámico en tiempo continuo y deben ser descartadas. |
| `D-Hab04-05` | Omisión de la evaluación completa del estado en la transversalidad | conceptual_swap | high | Olvidar sustituir la función $x(t_1) = \frac{t_1^2}{12} + c_1 t_1$ en el término de posición $x$ al evaluar la transversalidad | La transversalidad es una condición sobre toda la función de estado y sus derivadas evaluadas en el límite superior. |
| `D-Hab04-06` | Falta de verificación de suficiencia de mínimo global | conceptual_swap | high | Omitir comprobar que $F_{\dot{x}\dot{x}} = 6 > 0$ y que el integrando es convexo en $(x, \dot{x})$ para validar el mínimo | Verificar la convexidad global asegura que no se haya obtenido un punto de ensilladura o un costo maximal en la frontera móvil. |

---

### [C-07] Modelado del Monopolio Dinámico de Evans (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 27: Modelado del Monopolio Dinámico de Evans
- **Prerequisites:** C-01, C-02
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 27)

#### Description & Cognitive Model
Estructuración económica de un monopolista donde la demanda de mercado depende tanto del precio actual $p(t)$ como de la tendencia o expectativa de variación del precio $\dot{p}(t)$: $q = a - bp(t) + h\dot{p}(t)$ ($a,b>0, h \ne 0$), con costos cuadráticos $C(q) = \alpha q^2 + \beta q + \gamma$, para formular el funcional de beneficios a maximizar $\int_{t_0}^{t_1} [pq(p, \dot{p}) - C(q)]dt$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Omisión de la dinámica de expectativas en la demanda | conceptual_swap | high | Modelar la demanda del monopolio dinámico como $q = a - bp(t)$ omitiendo el término dependiente de la tasa de cambio del precio $\dot{p}(t)$ | Si la demanda no dependiera de $\dot{p}$, el problema se desacoplaría en una sucesión de optimizaciones estáticas independientes en cada instante. |
| `D-C07-02` | Confusión conceptual sobre el parámetro de tendencia | conceptual_swap | high | Afirmar que el parámetro $h$ representa el costo marginal o de almacenamiento de la empresa | La estructura de costos está gobernada por $\alpha, \beta, \gamma$; el parámetro $h$ modela exclusivamente la reacción especulativa de la demanda. |
| `D-C07-03` | Error en la definición del beneficio instantáneo | conceptual_swap | high | Definir el beneficio instantáneo del monopolista restando los ingresos a los costos: $\pi(t) = C(q) - p q$ | Para maximizar utilidades, los ingresos deben entrar con signo positivo y los costos de producción deben deducirse en el integrando. |
| `D-C07-04` | Confusión de la variable de estado principal | conceptual_swap | high | Asumir que la cantidad producida $q(t)$ es la variable de estado dinámico cuya derivada se optimiza | El monopolista selecciona la senda de precios $p(t)$ en el mercado, quedando la cantidad determinada por la función de demanda resultante. |
| `D-C07-05` | Linealización errónea de los costos de producción | conceptual_swap | high | Asumir que los costos de producción son lineales $C(q) = c q$, ignorando la deseconomía de escala del modelo canónico | La convexidad cuadrática en los costos es esencial para acotar la velocidad óptima de ajuste del precio y evitar soluciones degeneradas. |
| `D-C07-06` | Inclusión impropia de tasa de descuento intertemporal | conceptual_swap | high | Afirmar que el modelo formulado en la sesión incluye un factor de descuento exponencial $e^{-rt}$ con $r > 0$ | Para facilitar la resolución analítica de la EDO de Euler se asume una tasa de descuento nula, ponderando por igual todos los períodos. |

---

### [Hab-05] Optimización del Tradeoff Inflación-Desempleo y Trayectoria Óptima (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 28: Optimización del Tradeoff Inflación-Desempleo y Trayectoria Óptima
- **Prerequisites:** C-02, Hab-01
- **Evidence Citations:** `optimizacion_dinamica.pdf` (page 28)

#### Description & Cognitive Model
Formulación variacional y resolución del problema de política monetaria óptima de desinflación (Taylor 1989): sustitución de Phillips y expectativas en el costo social $\lambda(\pi, \dot{\pi}) = (\frac{\dot{\pi}}{\beta j})^2 + \alpha(\frac{\dot{\pi}}{j}+\pi)^2$, deducción de la EDO de Euler para $\pi(t)$, obtención de las raíces $r = \pm \frac{\beta j \sqrt{\alpha}}{\sqrt{1+\beta^2\alpha}}$ y cálculo de la senda óptima con contornos $\pi(0)=\pi_0, \pi(T)=0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Error en el despeje algebraico de las expectativas adaptativas | skipped_step | high | Al despejar la tasa de inflación $p$ de $\dot{\pi} = j(p - \pi)$, obtener $p = \frac{\pi}{j} + \dot{\pi}$ en lugar de $p = \frac{\dot{\pi}}{j} + \pi$ | El factor $j$ divide a la tasa de variación $\dot{\pi}$ y no a la inflación esperada $\pi$. |
| `D-Hab05-02` | Error de radicación en las raíces características de Euler | skipped_step | high | Para la ecuación $(1 + \beta^2\alpha)\ddot{\pi} - \beta^2 j^2\alpha \pi = 0$, calcular las raíces como $r = \pm \frac{\beta j \alpha}{1 + \beta^2\alpha}$ omitiendo las raíces cuadradas | Al despejar $r = \sqrt{r^2}$ se debe aplicar el operador radical tanto al numerador ($\sqrt{\alpha}$) como al denominador $(\sqrt{1+\beta^2\alpha})$. |
| `D-Hab05-03` | Colapso trivial del sistema de contorno terminal | conceptual_swap | high | Al imponer la condición terminal $\pi(T) = c_1 e^{r_1 T} + c_2 e^{-r_1 T} = 0$, forzar erróneamente $c_1 = c_2 = 0$ | Si ambas constantes fueran nulas, la inflación inicial sería cero, violando la premisa del problema de desinflar desde una tasa inicial $\pi_0 \ne 0$. |
| `D-Hab05-04` | Omisión de comprobación de la condición de Legendre para el costo social | skipped_step | high | Dar por óptima la política monetaria sin verificar que la segunda derivada respecto a $\dot{\pi}$ sea estrictamente positiva | Dado que $\alpha, \beta, j > 0$, la segunda derivada es estrictamente positiva, garantizando que la política hallada minimiza las pérdidas sociales. |
| `D-Hab05-05` | Anulación prematura del término exponencial creciente en horizonte finito | conceptual_swap | high | Eliminar la constante $c_1$ asumiendo horizonte infinito $T \to \infty$ en un problema planteado con horizonte finito $T$ | Solo en un horizonte infinito se descartan las raíces inestables por acotamiento; con tiempo finito la convergencia terminal fija ambas constantes. |
| `D-Hab05-06` | Inversión del signo en la ecuación diferencial de Euler | conceptual_swap | high | Escribir la ecuación de Euler como $(1 + \beta^2\alpha)\ddot{\pi} + \beta^2 j^2\alpha \pi = 0$ con signo positivo | Un signo positivo produciría oscilaciones trigonométricas de inflación en vez de una trayectoria suave monótona hacia la estabilidad. |

---
