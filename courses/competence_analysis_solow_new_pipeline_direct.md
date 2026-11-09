# Cognitive Task Analysis (CTA): Solow New Pipeline Direct

- **Course ID:** `solow_new_pipeline_direct`
- **Macro-Competency:** Dominio y aplicación analítica integral de Solow New Pipeline Direct
- **Structure:** 15 total competencies (4 Facts, 6 Concepts, 5 Skills) with 90 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `H-01` | Propiedades de la Función de Producción Neoclásica | Fact | Remember | Unidad 2: Propiedades de la Función de Producción Neoclásica | - | 6 |
| `C-01` | Forma Intensiva de la Función de Producción | Concept | Understand | Unidad 2: Forma Intensiva de la Función de Producción | H-01 | 6 |
| `H-02` | Ecuaciones de Comportamiento del Ahorro y la Fuerza Laboral | Fact | Remember | Unidad 2: Ecuaciones de Comportamiento del Ahorro y la Fuerza Laboral | H-01 | 6 |
| `Hab-01` | Derivación de la Ecuación Fundamental de Acumulación de Capital | Skill | Apply | Unidad 3: Derivación de la Ecuación Fundamental de Acumulación de Capital | C-01, H-02 | 6 |
| `C-02` | Existencia y Estabilidad Dinámica del Estado Estacionario | Concept | Analyze | Unidad 3: Existencia y Estabilidad Dinámica del Estado Estacionario | Hab-01 | 6 |
| `C-03` | Propiedades del Crecimiento en Estado Uniforme | Concept | Understand | Unidad 4: Propiedades del Crecimiento en Estado Uniforme | C-02 | 6 |
| `Hab-02` | Resolución de la Ecuación de Bernoulli para Cobb-Douglas | Skill | Apply | Unidad 4: Resolución de la Ecuación de Bernoulli para Cobb-Douglas | Hab-01, C-02 | 6 |
| `H-03` | Crítica Teórica a la Hipótesis del Filo de Navaja de Harrod-Domar | Fact | Remember | Unidad 2: Crítica Teórica a la Hipótesis del Filo de Navaja de Harrod-Domar | C-02 | 6 |
| `C-04` | Dinámica con Proporciones Fijas en la Formulación de Solow | Concept | Analyze | Unidad 10: Dinámica con Proporciones Fijas en la Formulación de Solow | H-03 | 6 |
| `Hab-03` | Análisis de Estabilidad con Múltiples Estados Estacionarios | Skill | Analyze | Unidad 8: Análisis de Estabilidad con Múltiples Estados Estacionarios | C-02, C-04 | 6 |
| `Hab-04` | Evaluación del Régimen de Crecimiento en Tecnología CES Cuadrática | Skill | Apply | Unidad 14: Evaluación del Régimen de Crecimiento en Tecnología CES Cuadrática | Hab-01, C-02 | 6 |
| `H-04` | Condición de No Arbitraje de Activos de Capital y Tasa de Interés | Fact | Remember | Unidad 17: Condición de No Arbitraje de Activos de Capital y Tasa de Interés | C-03 | 6 |
| `C-05` | Ajuste de Precios Factoriales y Pleno Empleo Continuo | Concept | Understand | Unidad 16: Ajuste de Precios Factoriales y Pleno Empleo Continuo | H-04, C-01 | 6 |
| `Hab-05` | Dinámica con Progreso Técnico Neutral en el Sentido de Hicks | Skill | Apply | Unidad 22: Dinámica con Progreso Técnico Neutral en el Sentido de Hicks | Hab-02, C-03 | 6 |
| `C-06` | Tasa de Ahorro Endógena y Efectos de la Política Tributaria | Concept | Understand | Unidad 25: Tasa de Ahorro Endógena y Efectos de la Política Tributaria | C-05, Hab-05 | 6 |

---

## Detailed Competency Specifications

### [H-01] Propiedades de la Función de Producción Neoclásica (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 2: Propiedades de la Función de Producción Neoclásica
- **Prerequisites:** None
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
La función de producción agregada $Q = F(K, L)$ satisface rendimientos constantes a escala $F(\mu K, \mu L) = \mu F(K, L)$, productos marginales positivos $F_K > 0, F_L > 0$ y rendimientos marginales decrecientes $F_{KK} < 0, F_{LL} < 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Confusión de rendimientos | conceptual_swap | high | Rendimientos crecientes a escala con $F(\mu K, \mu L) = \mu^2 F(K, L)$ | El modelo de Solow requiere homogeneidad de primer grado para permitir la agregación y la forma intensiva. |
| `D-H01-02` | Signo de la segunda derivada | conceptual_swap | high | $F_{KK} > 0$ indicando productividad marginal creciente | La ley de rendimientos decrecientes exige que la segunda derivada respecto a cada insumo sea estrictamente negativa. |
| `D-H01-03` | Inversión de condiciones marginales | conceptual_swap | high | $F_K < 0$ y $F_L < 0$ en el rango relevante | En la región económicamente eficiente los productos marginales de los factores deben ser estrictamente positivos. |
| `D-H01-04` | Rendimientos decrecientes a escala | conceptual_swap | high | $F(\mu K, \mu L) < \mu F(K, L)$ para todo $\mu > 1$ | Los rendimientos decrecientes aplican a factores individuales, mientras que la escala global es linealmente homogénea. |
| `D-H01-05` | Dependencia de escala no homogénea | conceptual_swap | high | $F(K, L) = K^\alpha + L^\beta$ con $\alpha + \beta = 1$ | Una forma puramente aditiva no exhibe complementariedad ni homogeneidad estricta de primer grado. |
| `D-H01-06` | Falta de producto cruzado | conceptual_swap | high | $F_{KL} < 0$ en todo el dominio | Con rendimientos constantes a escala y dos insumos, un aumento en el factor trabajo incrementa la productividad marginal del capital. |

---

### [C-01] Forma Intensiva de la Función de Producción (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 2: Forma Intensiva de la Función de Producción
- **Prerequisites:** H-01
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Al dividir la función homogénea de grado 1 por el factor trabajo $L$, el producto por trabajador $q = Q/L$ se expresa como una función de la relación capital-trabajo $k = K/L$, dada por $q = \phi(k) = F(k, 1)$, cumpliendo $\phi'(k) > 0$ y $\phi''(k) < 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Error en la variable intensiva | conceptual_swap | high | $q = \phi(K) = F(K, 1)$ sin normalizar por el trabajo | La relación capital-trabajo $k = K/L$ es imprescindible para colapsar las dos dimensiones a una sola variable intensiva. |
| `D-C01-02` | Confusión entre producto medio y marginal | conceptual_swap | high | $\phi'(k) = \frac{\phi(k)}{k}$ en cualquier punto | Debido a la concavidad estricta con $\phi''(k) < 0$, la productividad marginal del capital es estrictamente menor que su productividad media. |
| `D-C01-03` | Signo de la curvatura intensiva | conceptual_swap | high | $\phi''(k) > 0$ para $k > 0$ | La hipótesis de rendimientos decrecientes del capital asegura que la función intensiva $\phi(k)$ sea estrictamente cóncava. |
| `D-C01-04` | Inversión de ratios | conceptual_swap | high | $k = L/K$ y $q = L/Q$ | Las variables intensivas estándar en la literatura de crecimiento representan unidades por trabajador, no trabajadores por unidad de capital. |
| `D-C01-05` | Relación con el producto marginal del capital | conceptual_swap | high | $F_K = \phi(k) - k \phi'(k)$ | Por el teorema de Euler, la productividad marginal del capital es directamente la derivada de la forma intensiva $\phi'(k)$. |
| `D-C01-06` | Relación con el producto marginal del trabajo | conceptual_swap | high | $F_L = \phi'(k)$ | El producto marginal del trabajo corresponde al residuo intensivo $\phi(k) - k \phi'(k)$, no a $\phi'(k)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Homogeneidad de grado 1 en la función agregada $F(\mu K, \mu L) = \mu F(K, L)$ | Sin rendimientos constantes a escala la función no puede reducirse a una única variable intensiva de capital por trabajador. | - |

---

### [H-02] Ecuaciones de Comportamiento del Ahorro y la Fuerza Laboral (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 2: Ecuaciones de Comportamiento del Ahorro y la Fuerza Laboral
- **Prerequisites:** H-01
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
La inversión neta coincide con el ahorro agregado a través de una propensión marginal constante $\dot{K} = s Q$ con $0 < s < 1$, mientras que la fuerza laboral crece a una tasa exógena constante $\dot{L}/L = \lambda$, determinando la trayectoria $L(t) = L_0 e^{\lambda t}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H02-01` | Tasa de ahorro variable en el modelo base | conceptual_swap | high | $\dot{K} = s(t) Q(t)$ con $s(t)$ función creciente del tiempo | En la versión fundamental de Solow, la propensión al ahorro $s$ se postula como un parámetro exógeno y estrictamente constante. |
| `D-H02-02` | Crecimiento laboral lineal | conceptual_swap | high | $L(t) = L_0 + \lambda t$ | Una tasa porcentual constante $\dot{L}/L = \lambda$ produce una trayectoria exponencial, no un crecimiento lineal. |
| `D-H02-03` | Confusión entre stock y flujo | conceptual_swap | high | $K(t) = s Q(t)$ en lugar de acumulación continua | El ahorro genera la tasa de cambio instantánea del stock de capital (inversión neta $\dot{K}$), no el stock acumulado directamente. |
| `D-H02-04` | Tasa de depreciación en el ahorro | conceptual_swap | high | $\dot{K} = (1 - s) Q$ | El flujo de inversión neta proviene de la fracción ahorrada $s$, mientras que $(1 - s)$ representa el consumo de la economía. |
| `D-H02-05` | Tasa de crecimiento de mano de obra decreciente | conceptual_swap | high | $\dot{L}/L = \lambda / t$ | El modelo de Solow asume tasa demográfica constante $\lambda > 0$, prescindiendo de efectos malthusianos en su formulación base. |
| `D-H02-06` | Inversión desacoplada del ahorro | conceptual_swap | high | $\dot{K} = I_0 e^{\mu t}$ independiente del producto | En el modelo neoclásico no existe función de inversión autónoma desacoplada: el ahorro determina exactamente la inversión efectiva. |

---

### [Hab-01] Derivación de la Ecuación Fundamental de Acumulación de Capital (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 3: Derivación de la Ecuación Fundamental de Acumulación de Capital
- **Prerequisites:** C-01, H-02
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
A partir de la definición de capital por trabajador $k = K/L$, se aplica la derivada temporal $\dot{k} = \frac{\dot{K} L - K \dot{L}}{L^2} = \frac{\dot{K}}{L} - k \frac{\dot{L}}{L}$ y se sustituyen $\dot{K} = s L \phi(k)$ y $\dot{L}/L = \lambda$ para deducir $\dot{k} = s\phi(k) - \lambda k$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Signo en la dilución de capital | skipped_step | high | $\dot{k} = s\phi(k) + \lambda k$ | El crecimiento de la mano de obra reduce la dotación de capital por trabajador, por lo que el término $\lambda k$ entra con signo negativo. |
| `D-Hab01-02` | Omisión del factor de escala laboral | skipped_step | high | $\dot{k} = s\phi(k) - \lambda$ | Al derivar $k = K/L$, el segundo término contiene $(K/L)(\dot{L}/L) = \lambda k$, no una constante $\lambda$. |
| `D-Hab01-03` | Error algebraico en el producto agregado | conceptual_swap | high | $\dot{k} = s F(K, L) - \lambda k$ | Para obtener una ecuación autónoma en $k$, el producto agregado debe expresarse en términos per cápita como $Q/L = \phi(k)$. |
| `D-Hab01-04` | Inversión de los términos de ahorro y dilución | conceptual_swap | high | $\dot{k} = \lambda k - s\phi(k)$ | La acumulación de capital $\dot{K}/L = s\phi(k)$ incrementa $k$, mientras que la dilución $\lambda k$ lo amortigua. |
| `D-Hab01-05` | Olvido de la propensión al ahorro | conceptual_swap | high | $\dot{k} = \phi(k) - \lambda k$ | Solo la fracción $s$ del producto se transforma en capital nuevo; el resto se destina al consumo presente. |
| `D-Hab01-06` | Fórmula con derivadas parciales cruzadas | conceptual_swap | high | $\dot{k} = s\phi'(k) - \lambda k$ | La inversión bruta por trabajador depende del producto total por trabajador $\phi(k)$, no de la productividad marginal $\phi'(k)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Diferenciabilidad continua de las trayectorias temporales $K(t)$ y $L(t)$ | Si las trayectorias de capital o mano de obra presentan saltos discretos, no es aplicable el cálculo diferencial en tiempo continuo. | - |

---

### [C-02] Existencia y Estabilidad Dinámica del Estado Estacionario (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 3: Existencia y Estabilidad Dinámica del Estado Estacionario
- **Prerequisites:** Hab-01
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
El equilibrio intertemporal de estado uniforme $k^*$ se alcanza cuando $\dot{k} = 0$, lo que implica $s\phi(k^*) = \lambda k^*$. Su estabilidad dinámica asintótica queda garantizada porque la pendiente de la línea de fase en el entorno de $k^*$ es estrictamente negativa: $s\phi'(k^*) - \lambda < 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Condición de inestabilidad | conceptual_swap | high | $s\phi'(k^*) - \lambda > 0$ en el punto de corte | Para que un equilibrio dinámico continuo sea estable, la derivada de $\dot{k}$ respecto a $k$ debe ser estrictamente negativa en el equilibrio. |
| `D-C02-02` | Confusión entre valor de estado estacionario y variación nula | conceptual_swap | high | $k^* = 0$ como único punto de equilibrio estable del sistema | Bajo las condiciones de Inada existe una intersección estrictamente positiva $k^* > 0$ que atrae las trayectorias desde cualquier condición inicial. |
| `D-C02-03` | Indeterminación de la tasa de depreciación demográfica | conceptual_swap | high | $s\phi(k^*) = \lambda$ independientemente de $k^*$ | El requerimiento de inversión por trabajador para mantener $k$ constante crece proporcionalmente con el stock de capital per cápita. |
| `D-C02-04` | Trayectorias divergentes | conceptual_swap | high | Si $k(0) < k^*$, entonces $\dot{k} < 0$ provocando descapitalización total | Cuando la dotación de capital es inferior a $k^*$, el ahorro generado supera la dilución demográfica, impulsando $k$ hacia arriba. |
| `D-C02-05` | Equilibrio determinado únicamente por la tecnología | conceptual_swap | high | $k^*$ depende únicamente de $\phi(k)$ sin importar $s$ o $\lambda$ | El estado estacionario surge de la intersección entre la curva de ahorro efectivo $s\phi(k)$ y la recta de inversión de reemplazo $\lambda k$. |
| `D-C02-06` | Convergencia oscilatoria en una dimensión | conceptual_swap | high | La trayectoria $k(t)$ oscila periódicamente alrededor de $k^*$ | En una ecuación diferencial autónoma de primer orden en una sola variable, las soluciones son estrictamente monótonas en el tiempo. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | Condiciones de Inada estándar $\lim_{k \to 0} \phi'(k) = \infty$ y $\lim_{k \to \infty} \phi'(k) = 0$ | Garantizan que la curva de ahorro corte a la recta de dilución en un único punto interior estrictamente positivo y globalmente estable. | - |

---

### [C-03] Propiedades del Crecimiento en Estado Uniforme (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 4: Propiedades del Crecimiento en Estado Uniforme
- **Prerequisites:** C-02
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
En el estado uniforme de crecimiento balanceado, la relación capital-trabajo $k^*$ y el producto medio $q^* = \phi(k^*)$ son constantes en el tiempo, de modo que las variables agregadas $K(t)$, $L(t)$ y $Q(t)$ crecen a la tasa demográfica constante $\lambda$, resultando en una tasa de crecimiento del ingreso per cápita nula.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Crecimiento per cápita permanente sin tecnología | conceptual_swap | high | El producto por trabajador $Q/L$ crece indefinidamente a la tasa $\lambda$ | En ausencia de progreso tecnológico, los rendimientos decrecientes del capital frenan el crecimiento del ingreso per cápita en el estado estacionario. |
| `D-C03-02` | Disparidad de tasas de crecimiento agregadas | conceptual_swap | high | El capital agregado $K$ crece a tasa $s \lambda$ mientras el producto $Q$ crece a tasa $\lambda$ | La constancia de $K/L$ y $Q/L$ exige matemáticamente que tanto $K$ como $Q$ crezcan a la misma tasa exponencial que la mano de obra $L$. |
| `D-C03-03` | Inversión neta nula | conceptual_swap | high | La inversión neta $\dot{K}$ es igual a cero en el estado uniforme | Para mantener $k^*$ ante el incremento continuo de trabajadores, el stock de capital agregado debe expandirse continuamente a tasa $\lambda$. |
| `D-C03-04` | Efecto permanente de una mayor tasa de ahorro | conceptual_swap | high | Un incremento en $s$ eleva permanentemente la tasa de crecimiento de largo plazo de $Q$ | En el modelo de Solow básico, cambios en la tasa de ahorro tienen efectos de nivel sobre el producto, pero no alteran la tasa de crecimiento secular. |
| `D-C03-05` | Comportamiento de la relación capital-producto | conceptual_swap | high | La relación capital-producto $K/Q$ diverge hacia infinito | En el estado uniforme, la relación capital-producto es constante e idéntica a la razón entre la tasa de ahorro y la tasa demográfica $s/\lambda$. |
| `D-C03-06` | Crecimiento del consumo per cápita | conceptual_swap | high | El consumo per cápita crece a la tasa $1 - s$ | Como el producto por trabajador es invariante en el estado uniforme, el consumo per cápita $(1 - s)q^*$ también es constante en el tiempo. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Crecimiento exógeno e invariable de la fuerza laboral a tasa $\lambda > 0$ | Si la fuerza de trabajo no se expande a una tasa exponencial constante, el estado uniforme deja de presentar tasas idénticas de crecimiento. | - |

---

### [Hab-02] Resolución de la Ecuación de Bernoulli para Cobb-Douglas (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 4: Resolución de la Ecuación de Bernoulli para Cobb-Douglas
- **Prerequisites:** Hab-01, C-02
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Para la función Cobb-Douglas $Q = K^\alpha L^{1-\alpha}$ con $\phi(k) = k^\alpha$, la ecuación no lineal $\dot{k} + \lambda k = s k^\alpha$ se transforma mediante $z = k^{1-\alpha}$ en la ecuación diferencial lineal $\frac{dz}{dt} + (1-\alpha)\lambda z = (1-\alpha)s$, cuya solución analítica revela $k^*(t) = (s/\lambda)^{1/(1-\alpha)}$ cuando $t \to \infty$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Exponente invertido en el estado estacionario | skipped_step | high | $k^* = \left(\frac{s}{\lambda}\right)^{1-\alpha}$ | Como $z = k^{1-\alpha}$ y $z^* = s/\lambda$, la variable original requiere la raíz $(1-\alpha)$-ésima: $k^* = (s/\lambda)^{1/(1-\alpha)}$. |
| `D-Hab02-02` | Error en el factor multiplicador de la transformación | skipped_step | high | $\frac{dz}{dt} + \lambda z = s$ | Al derivar $z = k^{1-\alpha}$, se obtiene $\dot{z} = (1-\alpha)k^{-\alpha}\dot{k}$, por lo que todos los términos deben escalarse por $(1-\alpha)$. |
| `D-Hab02-03` | Signo incorrecto en la solución temporal | conceptual_swap | high | $z(t) = \left(z(0) - \frac{s}{\lambda}\right) e^{(1-\alpha)\lambda t} + \frac{s}{\lambda}$ | El factor integrante de una ecuación en forma $\dot{z} + a z = b$ contiene $e^{-at}$, garantizando convergencia amortiguada hacia el equilibrio. |
| `D-Hab02-04` | Confusión entre parámetros de escala y elasticidad | conceptual_swap | high | $k^* = \left(\frac{\lambda}{s}\right)^{\frac{1}{\alpha}}$ | Un aumento en la propensión al ahorro $s$ expande la dotación de capital, requiriendo que $s$ figure en el numerador. |
| `D-Hab02-05` | Producto por trabajador en equilibrio incorrecto | conceptual_swap | high | $q^* = \left(\frac{s}{\lambda}\right)^{\frac{1}{1-\alpha}}$ | Para la tecnología Cobb-Douglas, $q^* = (k^*)^\alpha$, por lo que la potencia acumulada es $\alpha/(1-\alpha)$. |
| `D-Hab02-06` | Tasa de convergencia distorsionada | conceptual_swap | high | La velocidad de convergencia al estado estacionario es $\lambda$ | La linealización formal muestra que el coeficiente de amortiguamiento exponencial es exactamente $(1-\alpha)\lambda$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Elasticidad del capital acotada en el intervalo abierto $0 < \alpha < 1$ | Si $\alpha = 1$, la ecuación diferencial no exhibe rendimientos decrecientes y no converge a un estado estacionario estable. | - |

---

### [H-03] Crítica Teórica a la Hipótesis del Filo de Navaja de Harrod-Domar (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 2: Crítica Teórica a la Hipótesis del Filo de Navaja de Harrod-Domar
- **Prerequisites:** C-02
- **Evidence Citations:** `solow1956.pdf` (page 2)

#### Description & Cognitive Model
El modelo de Harrod-Domar predice inestabilidad estructural o crecimiento de filo de navaja debido a que la tasa natural impuesta por la demografía $n$ y la tasa garantizada por el ahorro $s/v$ operan de forma desacoplada bajo coeficientes técnicos fijos $v = K/Y$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H03-01` | Atribución errónea de la inestabilidad de Harrod-Domar | conceptual_swap | high | La inestabilidad proviene exclusivamente de la variabilidad de la tasa de interés | Solow demuestra formalmente que la rigidez de proporciones tecnológicas es la que impide el ajuste continuo entre las tasas natural y garantizada. |
| `D-H03-02` | Definición de la tasa garantizada | conceptual_swap | high | La tasa garantizada se define como $s \cdot v$ | La tasa de crecimiento requerida por los empresarios para justificar su inversión es el cociente entre el ahorro y el coeficiente de capital $s/v$. |
| `D-H03-03` | Papel de la sustitución factorial en Harrod-Domar | conceptual_swap | high | Harrod y Domar asumieron sustituibilidad perfecta entre insumos | El modelo de Harrod-Domar descarta expresamente la sustitución factorial, empleando funciones de producción de proporciones rígidas. |
| `D-H03-04` | Consecuencia de discrepancias entre tasas | conceptual_swap | high | Si $s/v > n$ se produce pleno empleo automático mediante ajuste de precios | Cuando la tasa de acumulación garantizada sobrepasa el crecimiento laboral, la incapacidad de sustitución genera maquinaria inactiva. |
| `D-H03-05` | Identificación de la tasa natural de crecimiento | conceptual_swap | high | La tasa natural de Harrod es la tasa a la que se deprecia el capital físico | La tasa natural de crecimiento viene fijada por el incremento biológico de la población laboral y el avance técnico exógeno. |
| `D-H03-06` | Naturaleza del ajuste en el modelo neoclásico | conceptual_swap | high | Solow elimina el filo de navaja fijando la tasa de ahorro por decreto estatal | La variabilidad continua de la intensidad de capital permite que $v(k)$ se adapte hasta que la tasa garantizada coincida con la natural. |

---

### [C-04] Dinámica con Proporciones Fijas en la Formulación de Solow (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 10: Dinámica con Proporciones Fijas en la Formulación de Solow
- **Prerequisites:** H-03
- **Evidence Citations:** `solow1956.pdf` (page 10)

#### Description & Cognitive Model
Bajo una tecnología de Leontief $Y = \min(K/a, L/b)$, la ecuación diferencial fundamental adopta la forma $\dot{r} = s \min(r/a, 1/b) - n r$. Si la tasa natural supera a la garantizada ($n > s/a$), el ratio capital-trabajo decae provocando desempleo estructural creciente; si $n < s/a$, el capital se vuelve crónicamente redundante.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Inversión de los regímenes de cuello de botella | conceptual_swap | high | Cuando $r > a/b$, el capital es el factor escaso y limitante | Si la dotación de capital por trabajador supera la razón técnica $a/b$, existe más capital del que la mano de obra disponible puede operar. |
| `D-C04-02` | Fórmula de la tasa de acumulación en el tramo horizontal | conceptual_swap | high | Para $r \ge a/b$, la ecuación es $\dot{r} = \frac{s r}{a} - n r$ | En la zona donde el trabajo es el cuello de botella, el producto por trabajador está topado en $1/b$, haciendo que el ahorro sea la constante $s/b$. |
| `D-C04-03` | Equilibrio interior estable universal con Leontief | conceptual_swap | high | Siempre existe un equilibrio interior $r^*$ estable sin importar los parámetros $n$ y $s/a$ | Si la pendiente de la recta demográfica $n$ supera la tasa garantizada $s/a$, no existe punto de corte positivo y el capital per cápita decrece. |
| `D-C04-04` | Comportamiento de la remuneración factorial con factor redundante | conceptual_swap | high | Si $r > a/b$, la productividad marginal del capital y su alquiler real se mantienen positivos | En equilibrio competitivo con proporciones fijas, cualquier factor cuya oferta supere la requerida por el cuello de botella tiene producto marginal nulo. |
| `D-C04-05` | Forma de la curva de ahorro por trabajador | conceptual_swap | high | La función $s \min(r/a, 1/b)$ es una parábola estrictamente cóncava | Las funciones de tipo Leontief generan isocuantas en ángulo recto y una función intensiva lineal por tramos con un codo en la proporción técnica. |
| `D-C04-06` | Determinación de la desocupación de mano de obra | conceptual_swap | high | El desempleo ocurre únicamente si $r > a/b$ | Si el capital es insuficiente para equipar a toda la fuerza de trabajo disponible ($r < a/b$), una fracción de los trabajadores queda forzosamente desempleada. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Tecnología Leontief con elasticidad de sustitución factorial nula $\sigma = 0$ | La rigidez absoluta de los coeficientes de producción impide cualquier adaptación marginal de las técnicas productivas ante escasez factorial. | - |

---

### [Hab-03] Análisis de Estabilidad con Múltiples Estados Estacionarios (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 8: Análisis de Estabilidad con Múltiples Estados Estacionarios
- **Prerequisites:** C-02, C-04
- **Evidence Citations:** `solow1956.pdf` (page 8)

#### Description & Cognitive Model
Evaluar las intersecciones entre la curva de ahorro por trabajador $s F(r, 1)$ y el rayo demográfico $n r$ cuando la función de producción presenta convexidades locales, clasificando los estados estacionarios según el signo de la derivada direccional: las raíces $r_1, r_3$ con $s F'(r, 1) < n$ son dinámicamente estables, mientras que la raíz intermedia $r_2$ con $s F'(r_2, 1) > n$ es inestable y delimita una trampa de pobreza.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Clasificación invertida de estabilidad en raíces múltiples | skipped_step | high | La raíz intermedia $r_2$ es estable y las raíces extremas $r_1, r_3$ son inestables | Cuando la curva de ahorro cruza la recta de dilución desde abajo, $sF' > n$, cualquier perturbación positiva acelera la acumulación alejándose del punto. |
| `D-Hab03-02` | Identificación errónea del umbral de escape | skipped_step | high | Una economía con capital inicial $r_0 < r_2$ converge espontáneamente hacia $r_3$ | Para alcanzar el régimen de alto ingreso en $r_3$, se requiere un impulso de inversión inicial que supere el umbral crítico $r_2$. |
| `D-Hab03-03` | Condición de pendiente para estabilidad local | conceptual_swap | high | La estabilidad de un estado estacionario exige que $s F'(r^*, 1) > n$ | Para que un incremento en $r$ genere fuerzas correctivas negativas ($\dot{r} < 0$), la inversión de reemplazo debe crecer más rápido que el nuevo ahorro. |
| `D-Hab03-04` | Existencia de equilibrios sin supuestos de concavidad global | conceptual_swap | high | Es imposible que existan tres estados estacionarios en un modelo con rendimientos constantes | Si la productividad marginal del capital se eleva transitoriamente debido a indivisibilidades o externalidades, la curva intensiva adquiere forma sigmoide. |
| `D-Hab03-05` | Dinámica en el origen sin capital | conceptual_swap | high | El origen $r = 0$ siempre es un estado estacionario estable de crecimiento | Sin insumo de capital no se genera flujo de producto ni ahorro, impidiendo el arranque de la economía sin una inyección autónoma. |
| `D-Hab03-06` | Efecto de un choque transitorio sobre la trampa de desarrollo | conceptual_swap | high | Cualquier choque menor desplaza permanentemente la economía de $r_1$ a $r_3$ | Como $r_1$ es localmente asintóticamente estable, choques pequeños que mantengan el capital por debajo de $r_2$ regresan monótonamente a $r_1$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | No monotonía en la curvatura de la productividad marginal con zonas de convexidad local | La presencia de múltiples estados estacionarios requiere que la función intensiva no sea cóncava en todo su dominio de definición. | - |

---

### [Hab-04] Evaluación del Régimen de Crecimiento en Tecnología CES Cuadrática (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 14: Evaluación del Régimen de Crecimiento en Tecnología CES Cuadrática
- **Prerequisites:** Hab-01, C-02
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Para la función de producción con alta sustituibilidad $Y = (a\sqrt{K} + \sqrt{L})^2$, formular la ecuación intensiva $\dot{r} = s(a\sqrt{r} + 1)^2 - nr$. Analizar algebraicamente la existencia del estado estacionario finito $r^* = \left(\frac{1}{\sqrt{n/s} - a}\right)^2$ bajo la condición $s a^2 < n$, y demostrar que si $s a^2 > n$ la economía experimenta acumulación infinita sin cota superior.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Condición de divergencia autosostenida errónea | skipped_step | high | La acumulación infinita ocurre si $s a^2 < n$ | Cuando la asíntota de la productividad marginal del capital $s a^2$ supera la dilución $n$, la curva de ahorro jamás corta a la recta de dilución desde arriba. |
| `D-Hab04-02` | Fórmula del estado estacionario con raíz traspuesta | skipped_step | high | $r^* = \left(\sqrt{n/s} - a\right)^2$ | Al resolver $s(a\sqrt{r} + 1)^2 = n r$, se obtiene $\sqrt{s}(a\sqrt{r} + 1) = \sqrt{n}\sqrt{r}$, lo que conduce a $\sqrt{r}(\sqrt{n/s} - a) = 1$. |
| `D-Hab04-03` | Ingreso per cápita límite en el estado estacionario | conceptual_swap | high | $q^* = \frac{1}{\sqrt{n/s} - a}$ | Como la forma intensiva es $\phi(r) = (a\sqrt{r} + 1)^2$, al sustituir $\sqrt{r^*} = \frac{1}{\sqrt{n/s} - a}$ el producto resulta elevado al cuadrado. |
| `D-Hab04-04` | Participación distributiva del trabajo dependiente de parámetros | conceptual_swap | high | La participación del trabajo es estrictamente constante e independiente de $s$ y $n$ | En tecnologías con elasticidad de sustitución distinta de uno, las participaciones factoriales de equilibrio dependen de las tasas de ahorro y crecimiento. |
| `D-Hab04-05` | Comportamiento de la productividad marginal en el origen | conceptual_swap | high | La productividad marginal del capital tiende a infinito cuando $r \to 0$ | En esta variante tecnológica, la producción es viable únicamente con factor trabajo, reflejado en $\phi(0) = 1 > 0$. |
| `D-Hab04-06` | Sensibilidad del capital estacionario respecto a la propensión al ahorro | conceptual_swap | high | Un incremento en la propensión al ahorro $s$ reduce la intensidad de capital de equilibrio $r^*$ | Un mayor ahorro desplaza hacia arriba la curva de inversión, requiriendo un nivel superior de capital por trabajador para equilibrar la depreciación. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Elasticidad de sustitución entre capital y trabajo estrictamente mayor que la unidad con parámetro $p = 1/2$ | Permite que la productividad marginal del capital permanezca acotada inferiormente por una constante positiva cuando $r$ tiende a infinito. | - |

---

### [H-04] Condición de No Arbitraje de Activos de Capital y Tasa de Interés (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 17: Condición de No Arbitraje de Activos de Capital y Tasa de Interés
- **Prerequisites:** C-03
- **Evidence Citations:** `solow1956.pdf` (page 17)

#### Description & Cognitive Model
Bajo mercados financieros sin fricciones y previsión perfecta, el rendimiento total por poseer una unidad de capital físico, compuesto por el alquiler real más las ganancias o pérdidas de capital, debe igualar a la tasa de interés monetaria: $i(t) = \frac{q(t)}{p(t)} + \frac{\dot{p}(t)}{p(t)}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H04-01` | Omisión de la ganancia de capital | conceptual_swap | high | $i(t) = \frac{q(t)}{p(t)}$ independientemente de la evolución de precios | Si el precio del bien de capital cambia a lo largo del tiempo, los tenedores perciben una apreciación o depreciación que altera el rendimiento total. |
| `D-H04-02` | Signo de la apreciación del capital | conceptual_swap | high | $i(t) = \frac{q(t)}{p(t)} - \frac{\dot{p}(t)}{p(t)}$ | Una subida del precio del activo genera una ganancia de capital positiva para el propietario, sumándose al flujo de rentas por alquiler. |
| `D-H04-03` | Inversión de precios en el rendimiento propio | conceptual_swap | high | $i(t) = \frac{p(t)}{q(t)} + \frac{\dot{p}(t)}{p(t)}$ | La tasa de retorno propio se expresa como el cociente entre el alquiler percibido $q(t)$ y el costo de adquisición del capital $p(t)$. |
| `D-H04-04` | Coincidencia forzada entre tasa de interés y alquiler con precios variables | conceptual_swap | high | El alquiler real y la tasa de interés monetaria son siempre idénticos aún con inflación | La tasa de interés monetaria solo equivale exactamente a la tasa propia del bien si los precios agregados permanecen estrictamente estables. |
| `D-H04-05` | Determinación exógena de la tasa de interés sin arbitraje | conceptual_swap | high | La tasa de interés la fija el banco central sin relación con la productividad del capital | En el marco competitivo real, la tasa de rendimiento financiero debe ajustarse continuamente para igualar la productividad física del capital. |
| `D-H04-06` | Fórmula en valor presente | conceptual_swap | high | $p(t) = \int_t^\infty q(u) e^{i(u)} du$ con exponente positivo | El precio de transferencia del bien de capital debe descontar los flujos futuros de alquiler mediante la integral negativa de la tasa de interés. |

---

### [C-05] Ajuste de Precios Factoriales y Pleno Empleo Continuo (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 16: Ajuste de Precios Factoriales y Pleno Empleo Continuo
- **Prerequisites:** H-04, C-01
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
En una economía competitiva con retornos constantes a escala, el salario real y el alquiler del capital se determinan instantáneamente por sus productividades marginales: $\frac{w}{p} = F_L(r) = f(r) - r f'(r)$ y $\frac{q}{p} = F_K(r) = f'(r)$, dependiendo exclusivamente de la relación capital-trabajo $r$ y garantizando el vaciado continuo de los mercados de factores.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Dependencia del salario respecto a la escala absoluta | conceptual_swap | high | El salario real depende del tamaño absoluto de la fuerza laboral $L$ y del capital agregado $K$ | Por el teorema de Euler en funciones homogéneas de grado 1, las productividades marginales son funciones homogéneas de grado cero en las cantidades. |
| `D-C05-02` | Dirección del ajuste salarial ante escasez de capital | conceptual_swap | high | Una reducción en $r$ eleva el salario real y abarata el alquiler del capital | Si el capital se vuelve escaso respecto a la mano de obra, su productividad marginal aumenta mientras que la productividad marginal del trabajo decae. |
| `D-C05-03` | Inversión de las fórmulas de productividad marginal | conceptual_swap | high | $\frac{w}{p} = f'(r)$ y $\frac{q}{p} = f(r) - r f'(r)$ | La derivada de la función intensiva respecto a la relación capital-trabajo mide el producto marginal del capital, no del trabajo. |
| `D-C05-04` | Agotamiento del producto bajo rendimientos a escala | conceptual_swap | high | La suma de remuneraciones factoriales $w L + q K$ no iguala el valor total del producto $p Y$ | Bajo rendimientos constantes a escala y remuneración competitiva según productividades marginales, el producto total se reparte íntegramente. |
| `D-C05-05` | Comportamiento de la relación salario-renta de capital | conceptual_swap | high | El ratio de precios relativos $w/q$ disminuye cuando $r$ aumenta | A medida que una economía se equipa con más capital por trabajador, el trabajo se vuelve relativamente más escaso y su precio relativo $w/q$ se eleva. |
| `D-C05-06` | Distribución funcional en el caso Cobb-Douglas | conceptual_swap | high | En la Cobb-Douglas la participación del trabajo varía fuertemente con la acumulación de capital | La elasticidad de sustitución igual a uno en la tecnología Cobb-Douglas fija las participaciones relativas de los factores independientemente de $r$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Mercados de bienes y factores perfectamente competitivos con ajuste instantáneo de precios | Si existen rigideces salariales o poder de mercado monopólico, las productividades marginales dejan de igualar los precios reales de los factores. | - |

---

### [Hab-05] Dinámica con Progreso Técnico Neutral en el Sentido de Hicks (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 22: Dinámica con Progreso Técnico Neutral en el Sentido de Hicks
- **Prerequisites:** Hab-02, C-03
- **Evidence Citations:** `solow1956.pdf` (page 22)

#### Description & Cognitive Model
Incorporar el cambio técnico neutral $Y = e^{gt} K^\alpha L^{1-\alpha}$ en la ecuación de acumulación $\dot{K} = s Y$, deduciendo que el stock de capital per cápita $k = K/L$ se expande a la tasa secular constante $\frac{g}{1-\alpha}$ y el producto agregado a la tasa compuesta $n + \frac{g}{1-\alpha}$, superando permanentemente la tasa de crecimiento demográfico $n$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Tasa de crecimiento del capital per cápita sin efecto multiplicador | skipped_step | high | El capital per cápita crece a la tasa $g$ | El incremento de eficiencia genera mayor producto, lo que a su vez genera más ahorro y capital, acelerando la tasa en un factor $1/(1-\alpha)$. |
| `D-Hab05-02` | Tasa de expansión del producto agregado | skipped_step | high | El producto agregado crece a la tasa $n + g$ | Como la relación capital-trabajo crece a tasa $g/(1-\alpha)$, el producto por trabajador crece a esa misma tasa, sumándose al crecimiento laboral $n$. |
| `D-Hab05-03` | Comportamiento de la relación capital-trabajo de largo plazo | conceptual_swap | high | La relación capital-trabajo converge a un valor constante fijo a pesar del progreso técnico | Con desplazamiento secular continuo de la función de producción hacia arriba, el punto de corte con la dilución se desplaza sin límite hacia la derecha. |
| `D-Hab05-04` | Evolución del salario real en el largo plazo | conceptual_swap | high | El salario real permanece estancado debido a la competencia de la población creciente | Al expandirse continuamente la dotación de capital efectivo por trabajador, la productividad marginal del trabajo y el salario real aumentan sin límite. |
| `D-Hab05-05` | Tasa de crecimiento de la relación capital-producto | conceptual_swap | high | La relación capital-producto $K/Y$ crece a la tasa $\frac{g}{1-\alpha}$ | En el sendero de crecimiento balanceado tanto $K$ como $Y$ crecen a la tasa $n + g/(1-\alpha)$, preservando la constancia de su razón $K/Y$. |
| `D-Hab05-06` | Naturaleza del progreso técnico Hicks-neutral | conceptual_swap | high | El progreso neutral de Hicks altera la relación marginal de sustitución para una combinación dada de factores | Por definición, una innovación neutral de Hicks multiplica la función de producción por un escalar dependiente del tiempo sin distorsionar las pendientes de las isocuantas. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Progreso técnico neutral en el sentido de Hicks a tasa exponencial exógena constante $A(t) = e^{gt}$ | Si el avance técnico se desacelera o favorece asimétricamente a un factor, la tasa de crecimiento de largo plazo no permanece constante. | - |

---

### [C-06] Tasa de Ahorro Endógena y Efectos de la Política Tributaria (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 25: Tasa de Ahorro Endógena y Efectos de la Política Tributaria
- **Prerequisites:** C-05, Hab-05
- **Evidence Citations:** `solow1956.pdf` (page 25)

#### Description & Cognitive Model
Cuando la propensión al ahorro depende de la rentabilidad del capital $s = s(r)$, la ecuación de acumulación $\dot{r} = s(r)F(r, 1) - n r$ puede asegurar estabilidad dinámica si el ahorro se reduce ante excesos de capital; asimismo, un impuesto proporcional sobre la renta a tasa $t$ altera la tasa efectiva de ahorro a $s(1-t) + t v$, donde $v$ representa la fracción del ingreso fiscal canalizada a formación de capital.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Efecto estabilizador del ahorro sensible al retorno | conceptual_swap | high | Un ahorro que cae cuando el rendimiento disminuye tiende a desestabilizar el sistema | Al caer el ahorro cuando el stock de capital es elevado, se frena la acumulación excesiva, garantizando la convergencia hacia el estado estacionario. |
| `D-C06-02` | Tasa efectiva de ahorro cuando la recaudación fiscal se consume | conceptual_swap | high | Si el gobierno consume toda la recaudación ($v = 0$), el ahorro efectivo asciende a $s + t(1-s)$ | Al detraer impuestos del ingreso disponible y no destinarlos a inversión, el flujo disponible para acumulación se contrae en la proporción $(1-t)$. |
| `D-C06-03` | Tasa efectiva de ahorro cuando la recaudación se invierte íntegramente | conceptual_swap | high | Si el gobierno invierte toda la recaudación ($v = 1$), la tasa efectiva de ahorro es $s(1-t)$ | El ahorro privado residual $s(1-t)$ más la inversión pública total $t$ eleva la fracción de ingreso destinada a formar capital productivo. |
| `D-C06-04` | Impacto impositivo sobre la relación capital-trabajo estacionaria | conceptual_swap | high | Un impuesto cuyos ingresos se consumen totalmente eleva la relación capital-trabajo $r^*$ | La reducción de la tasa efectiva de ahorro desplaza la curva de acumulación hacia abajo, cortando al rayo $nr$ en un nivel de capital per cápita inferior. |
| `D-C06-05` | Neutralidad impositiva cuando el sector público ahorra la misma fracción que el privado | conceptual_swap | high | Si $v = s$, la política fiscal altera drásticamente la tasa de acumulación de capital | Cuando el Estado ahorra exactamente la misma fracción del ingreso que las familias, la reasignación de recursos entre consumo e inversión es nula. |
| `D-C06-06` | Posibilidad de estado estacionario malthusiano | conceptual_swap | high | El ahorro variable garantiza la aparición de un estado estacionario clásico sin crecimiento poblacional | Aunque la acumulación neta de capital pudiera cesar, el crecimiento exógeno de la mano de obra continuaría diluyendo la dotación de capital per cápita. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Comportamiento monótono no creciente de la propensión al ahorro respecto a la relación capital-trabajo $s'(r) \le 0$ | Asegura que aumentos en la dotación de capital no generen espirales desestabilizadoras de sobreacumulación incontrolada. | - |

---
