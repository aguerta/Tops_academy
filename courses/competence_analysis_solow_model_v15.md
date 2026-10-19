# Cognitive Task Analysis (CTA): Solow Model V15

- **Course ID:** `solow_model_v15`
- **Macro-Competency:** Dominio y aplicación analítica integral de Solow Model V15
- **Structure:** 15 total competencies (3 Facts, 6 Concepts, 6 Skills) with 90 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Hipótesis de Sustitución de Factores y Rendimientos Constantes a Escala | Concept | Understand | Unidad 2: Hipótesis de Sustitución de Factores y Rendimientos Constantes a Escala | - | 6 |
| `H-01` | Definición de la Función de Producción en Forma Intensiva | Fact | Remember | Unidad 2: Definición de la Función de Producción en Forma Intensiva | C-01 | 6 |
| `Hab-01` | Derivación de la Tasa de Variación Temporal del Capital por Trabajador | Skill | Apply | Unidad 2: Derivación de la Tasa de Variación Temporal del Capital por Trabajador | C-01, H-01 | 6 |
| `H-02` | Ecuación Diferencial Fundamental del Modelo de Solow | Fact | Remember | Unidad 3: Ecuación Diferencial Fundamental del Modelo de Solow | Hab-01 | 6 |
| `C-02` | Estabilidad Dinámica Global en el Diagrama de Línea de Fase | Concept | Analyze | Unidad 3: Estabilidad Dinámica Global en el Diagrama de Línea de Fase | H-02 | 6 |
| `C-03` | Propiedades del Estado Uniforme de Crecimiento Equilibrado | Concept | Understand | Unidad 4: Propiedades del Estado Uniforme de Crecimiento Equilibrado | C-02 | 6 |
| `Hab-02` | Linealización y Resolución de la Ecuación de Bernoulli Cobb-Douglas | Skill | Apply | Unidad 4: Linealización y Resolución de la Ecuación de Bernoulli Cobb-Douglas | H-02, C-03 | 6 |
| `Hab-03` | Cálculo del Capital de Estado Uniforme y Estática Comparativa | Skill | Apply | Unidad 5: Cálculo del Capital de Estado Uniforme y Estática Comparativa | Hab-02 | 6 |
| `C-04` | Colapso del Filo de la Navaja de Harrod-Domar bajo Proporciones Fijas | Concept | Analyze | Unidad 10: Colapso del Filo de la Navaja de Harrod-Domar bajo Proporciones Fijas | C-01, H-02 | 6 |
| `Hab-04` | Determinación de la Condición de Existencia de Equilibrio en Tecnologías CES | Skill | Apply | Unidad 14: Determinación de la Condición de Existencia de Equilibrio en Tecnologías CES | H-02, C-02 | 6 |
| `H-03` | Ecuación de Arbitraje de Activos de Bienes de Capital y Tasa Propia | Fact | Remember | Unidad 17: Ecuación de Arbitraje de Activos de Bienes de Capital y Tasa Propia | - | 6 |
| `C-05` | Comportamiento de Precios de Factores y Distribución Funcional Neoclásica | Concept | Understand | Unidad 20: Comportamiento de Precios de Factores y Distribución Funcional Neoclásica | H-03, C-01 | 6 |
| `Hab-05` | Modelación del Progreso Técnico Neutral y Dinámica Asintótica de Crecimiento | Skill | Apply | Unidad 22: Modelación del Progreso Técnico Neutral y Dinámica Asintótica de Crecimiento | Hab-02, C-03 | 6 |
| `Hab-06` | Evaluación del Impacto de la Política Fiscal en la Acumulación de Capital | Skill | Apply | Unidad 26: Evaluación del Impacto de la Política Fiscal en la Acumulación de Capital | H-02, Hab-03 | 6 |
| `C-06` | Equilibrios Múltiples y la Trampa de Pobreza Demográfica | Concept | Analyze | Unidad 27: Equilibrios Múltiples y la Trampa de Pobreza Demográfica | C-02, H-02 | 6 |

---

## Detailed Competency Specifications

### [C-01] Hipótesis de Sustitución de Factores y Rendimientos Constantes a Escala (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 2: Hipótesis de Sustitución de Factores y Rendimientos Constantes a Escala
- **Prerequisites:** None
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
En el modelo neoclásico, la producción agregada $Q = F(K, L)$ admite sustitución continua entre factores con rendimientos constantes a escala: $F(\mu K, \mu L) = \mu F(K, L)$ para todo $\mu > 0$, con productos marginales positivos $F_K > 0, F_L > 0$ y rendimientos marginales decrecientes $F_{KK} < 0, F_{LL} < 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Confundir rendimientos constantes a escala con productos marginales constantes | conceptual_swap | high | $\frac{\partial^2 F}{\partial K^2} = 0 \text{ debido a la homogeneidad de grado 1}$ | Los rendimientos a escala evalúan la variación simultánea y proporcional de todos los insumos, mientras que el producto marginal varía un solo insumo manteniendo los demás constantes. |
| `D-C01-02` | Asunción de rigidez tecnológica de coeficientes fijos tipo Leontief | conceptual_swap | high | $Q = \min\left(\frac{K}{a}, \frac{L}{b}\right)$ | Solow abandona la hipótesis de proporciones fijas de Harrod-Domar para permitir la sustituibilidad factorial suave a lo largo de isocuantas convexas. |
| `D-C01-03` | Violación del teorema de Euler para funciones linealmente homogéneas | conceptual_swap | high | $F(K, L) \ne K \cdot F_K + L \cdot F_L$ | Por el Teorema de Euler, una función homogénea de grado 1 distribuye exactamente el producto total cuando cada factor recibe su producto marginal. |
| `D-C01-04` | Atribución errónea de rendimientos crecientes a escala al modelo básico | conceptual_swap | high | $F(\mu K, \mu L) > \mu F(K, L) \text{ por economías de aglomeración}$ | El modelo base de Solow asume estrictamente rendimientos constantes a escala sin indivisibilidades ni externalidades. |
| `D-C01-05` | Confundir producto medio con producto marginal | conceptual_swap | high | $\text{PMP}_K = \frac{Q}{K}$ | El producto medio $Q/K$ es el producto por unidad de capital, mientras que el producto marginal es la derivada parcial respecto a $K$. |
| `D-C01-06` | Ignorar el supuesto de recursos no reproducibles | conceptual_swap | high | $\text{Inclusión de tierra o recursos no aumentables en } F(K, L)$ | Solow señala explícitamente que la ausencia de recursos fijos no reproducibles (como la tierra ricardiana) permite postular rendimientos constantes a escala en $K$ y $L$. |

---

### [H-01] Definición de la Función de Producción en Forma Intensiva (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 2: Definición de la Función de Producción en Forma Intensiva
- **Prerequisites:** C-01
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Gracias a la homogeneidad de grado 1, el producto por trabajador $q \equiv \frac{Q}{L}$ se expresa como una función de la relación capital-trabajo $k \equiv \frac{K}{L}$: $q = \phi(k) \equiv F(k, 1)$, con $\phi'(k) > 0$ y $\phi''(k) < 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Inversión de la relación capital-trabajo en la definición intensiva | conceptual_swap | high | $k = \frac{L}{K}$ | La relación capital-trabajo $k$ define las unidades de capital físico por cada unidad de mano de obra, $k = K/L$. |
| `D-H01-02` | Confundir la derivada de la forma intensiva con el producto medio | conceptual_swap | high | $\phi'(k) = \frac{\phi(k)}{k}$ | La primera derivada $\phi'(k)$ coincide exactamente con el producto marginal del capital $\partial Q/\partial K$, no con el producto medio $\phi(k)/k$. |
| `D-H01-03` | Signo positivo en la segunda derivada de la forma intensiva | conceptual_swap | high | $\phi''(k) > 0$ | La concavidad de la función de producción impone que $\phi''(k) < 0$, reflejando rendimientos marginales decrecientes del capital acumulado. |
| `D-H01-04` | Omitir la dependencia unitaria de la mano de obra en la normalización | conceptual_swap | high | $\phi(k) = F(K, 1)$ | Al dividir $F(K, L)$ entre $L$, el argumento del capital se transforma en $K/L = k$ y el argumento de trabajo se normaliza a 1. |
| `D-H01-05` | Asumir producto nulo con capital positivo y trabajo cero | conceptual_swap | high | $\lim_{k \to \infty} \phi(k) = 0$ | Para valores positivos de $k$, el producto por trabajador es estrictamente positivo y creciente con respecto a la dotación de capital por operario. |
| `D-H01-06` | Confusión entre producto por trabajador y producto agregado | conceptual_swap | high | $\phi(k) = Q$ | La función $\phi(k)$ mide el producto medio por trabajador; el producto total se recupera multiplicando por la masa laboral: $Q = L \phi(k)$. |

---

### [Hab-01] Derivación de la Tasa de Variación Temporal del Capital por Trabajador (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 2: Derivación de la Tasa de Variación Temporal del Capital por Trabajador
- **Prerequisites:** C-01, H-01
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
A partir de la identidad $K = k L$, derivar la tasa de cambio temporal $\dot{k} \equiv \frac{dk}{dt}$ aplicando la regla de la cadena y del producto: $\dot{K} = \dot{k}L + k\dot{L} = \dot{k}L + \lambda k L$, para despejar $\dot{k} = \frac{\dot{K}}{L} - \lambda k$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Omisión del crecimiento poblacional en la diferenciación del capital per cápita | skipped_step | high | $\dot{k} = \frac{\dot{K}}{L}$ | Al crecer la fuerza laboral a tasa $\lambda$, parte de la inversión debe destinarse a equipar a los nuevos entrantes sin incrementar la dotación per cápita. |
| `D-Hab01-02` | Suma en vez de resta del efecto de dilución demográfica | conceptual_swap | high | $\dot{k} = \frac{\dot{K}}{L} + \lambda k$ | El crecimiento de la mano de obra diluye la relación capital-trabajo existente, restando dotación efectiva por trabajador. |
| `D-Hab01-03` | Omitir sustituir la tasa de crecimiento exponencial en la derivada de mano de obra | skipped_step | high | $\dot{K} = \dot{k}L + k$ | La tasa de variación del trabajo es $\dot{L} = \lambda L$, no una constante unitaria. |
| `D-Hab01-04` | Confundir tasa absoluta de cambio con tasa de crecimiento porcentual | conceptual_swap | high | $\frac{\dot{k}}{k} = \dot{K} - \dot{L}$ | La tasa de crecimiento porcentual de un cociente es la diferencia de las tasas de crecimiento porcentuales de numerador y denominador. |
| `D-Hab01-05` | Inversión del orden en la regla del cociente | conceptual_swap | high | $\dot{k} = \frac{K\dot{L} - \dot{K}L}{L^2}$ | La regla del cociente establece que la derivada de $u/v$ es $(u'v - uv')/v^2$, donde $u = K$ y $v = L$. |
| `D-Hab01-06` | Asumir que el stock de mano de obra es constante en el tiempo | conceptual_swap | high | $\dot{L} = 0 \implies \dot{K} = L\dot{k}$ | El modelo de Solow postula explícitamente un crecimiento exógeno continuo de la mano de obra a tasa constante $\lambda > 0$. |

---

### [H-02] Ecuación Diferencial Fundamental del Modelo de Solow (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 3: Ecuación Diferencial Fundamental del Modelo de Solow
- **Prerequisites:** Hab-01
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
La ecuación diferencial ordinaria no lineal de primer orden que gobierna la trayectoria temporal de la relación capital-trabajo es: $\dot{k} = s\phi(k) - \lambda k$, donde $s\phi(k)$ es la inversión bruta por trabajador y $\lambda k$ es la inversión de reposición o ensanchamiento de capital.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H02-01` | Inversión de los términos de ahorro y ensanchamiento de capital | conceptual_swap | high | $\dot{k} = \lambda k - s\phi(k)$ | El ahorro invertido $s\phi(k)$ expande la dotación per cápita, mientras que el crecimiento poblacional $\lambda k$ la desgasta o diluye. |
| `D-H02-02` | Omisión de la propensión marginal al ahorro en la función de inversión | conceptual_swap | high | $\dot{k} = \phi(k) - \lambda k$ | Solo una fracción constante $s \in (0, 1)$ del producto se ahorra e invierte; la fracción $1-s$ se destina al consumo presente. |
| `D-H02-03` | Confundir producto por trabajador con capital por trabajador en el término de ahorro | conceptual_swap | high | $\dot{k} = s k - \lambda \phi(k)$ | El ahorro procede del producto generado $\phi(k)$, mientras que la dilución demográfica actúa sobre el stock de capital acumulado $k$. |
| `D-H02-04` | Adición de la tasa de depreciación física con signo positivo | conceptual_swap | high | $\dot{k} = s\phi(k) + (\lambda + \delta)k$ | Tanto la depreciación física $\delta$ como el crecimiento de la fuerza laboral $\lambda$ reducen la dotación de capital por operario. |
| `D-H02-05` | Uso del producto agregado en lugar de la forma intensiva en la ecuación per cápita | conceptual_swap | high | $\dot{k} = s Q - \lambda k$ | La ecuación diferencial para $\dot{k}$ relaciona variables intensivas: $s\phi(k)$ es ahorro por trabajador, no ahorro agregado $sQ$. |
| `D-H02-06` | Tratamiento de la propensión al ahorro como variable temporal dependiente de k | conceptual_swap | high | $s = s(k) \text{ obligatoriamente en el modelo canónico}$ | En el modelo básico de Solow, la propensión al ahorro $s$ es un parámetro exógeno e invariable en el tiempo. |

---

### [C-02] Estabilidad Dinámica Global en el Diagrama de Línea de Fase (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 3: Estabilidad Dinámica Global en el Diagrama de Línea de Fase
- **Prerequisites:** H-02
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
El estado estacionario $\bar{k} > 0$ satisface $s\phi(\bar{k}) = \lambda \bar{k}$. El equilibrio es dinámicamente estable si la pendiente de la línea de fase es negativa en $\bar{k}$: $\left.\frac{d\dot{k}}{dk}\right|_{k = \bar{k}} = s\phi'(\bar{k}) - \lambda < 0$, de modo que si $k < \bar{k}$, $\dot{k} > 0$, y si $k > \bar{k}$, $\dot{k} < 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Confundir pendiente positiva de la línea de fase con estabilidad dinámica | conceptual_swap | high | $\left.\frac{d\dot{k}}{dk}\right|_{\bar{k}} > 0 \implies \text{Estabilidad}$ | Una pendiente negativa de $\dot{k}$ respecto a $k$ garantiza fuerzas de restauración hacia el equilibrio ante cualquier perturbación. |
| `D-C02-02` | Asumir que toda intersección entre s phi(k) y lambda k es un atractor estable | conceptual_swap | high | $\forall k^* \text{ con } \dot{k} = 0 \implies k^* \text{ es estable}$ | Si la curva de ahorro corta a la línea de ensanchamiento desde abajo, la pendiente de $\dot{k}$ es positiva y el punto es inestable. |
| `D-C02-03` | Interpretar el origen k=0 como equilibrio estable universal | conceptual_swap | high | $\bar{k} = 0 \text{ es siempre asintóticamente estable}$ | Cuando la productividad marginal en el origen es infinita, cualquier dotación infinitesimal de capital impulsa la economía hacia el equilibrio positivo. |
| `D-C02-04` | Confundir la curva de ahorro con la línea de fase completa | conceptual_swap | high | $\dot{k} = s\phi(k)$ | La línea de fase grafica la diferencia neta entre la curva de ahorro $s\phi(k)$ y la recta $\lambda k$, no la curva de ahorro sola. |
| `D-C02-05` | Asunción de oscilaciones periódicas en el ajuste de primer orden | conceptual_swap | high | $k(t) \text{ experimenta ciclos oscilatorios amortiguados alrededor de } \bar{k}$ | Una ecuación diferencial autónoma de primer orden en la recta real no admite oscilaciones; las trayectorias convergen monótonamente. |
| `D-C02-06` | Creer que una mayor tasa de ahorro altera la estabilidad intrínseca del sistema | conceptual_swap | high | $\text{Un incremento de } s \text{ desestabiliza el equilibrio}$ | Para cualquier $s \in (0, 1)$, con funciones de producción estrictamente cóncavas, el equilibrio intertemporal resultante sigue siendo globalmente estable. |

---

### [C-03] Propiedades del Estado Uniforme de Crecimiento Equilibrado (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 4: Propiedades del Estado Uniforme de Crecimiento Equilibrado
- **Prerequisites:** C-02
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
En el estado uniforme (o balanced growth path) donde $\dot{k} = 0$, la relación capital-trabajo $k = \bar{k}$ y el producto por trabajador $q = \phi(\bar{k})$ permanecen constantes en el tiempo, lo que implica que el capital agregado $K$, el producto agregado $Q$ y la inversión neta crecen exactamente a la tasa de crecimiento poblacional $\lambda$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Creer que el crecimiento del producto per cápita es positivo y constante en estado uniforme sin tecnología | conceptual_swap | high | $\frac{\dot{q}}{q} = \lambda \text{ en ausencia de progreso técnico}$ | Sin progreso tecnológico, el producto por trabajador permanece constante en el estado uniforme; solo las variables agregadas crecen a tasa $\lambda$. |
| `D-C03-02` | Afirmar que un aumento en la tasa de ahorro incrementa permanentemente la tasa de crecimiento de largo plazo | conceptual_swap | high | $\lim_{t \to \infty} \frac{\dot{Q}}{Q} = f(s) > \lambda$ | En el modelo neoclásico, un mayor ahorro genera un efecto nivel transitorio, pero no altera la tasa de crecimiento de estado uniforme, fijada por $\lambda$. |
| `D-C03-03` | Confundir estado uniforme con estado estacionario clásico de crecimiento cero agregado | conceptual_swap | high | $\dot{K} = 0 \text{ y } \dot{Q} = 0 \text{ en estado uniforme}$ | El estado uniforme es una generalización del estado estacionario: las variables per cápita son estacionarias, pero las agregadas se expanden al compás de la mano de obra. |
| `D-C03-04` | Asumir que la inversión neta crece a una tasa diferente a la del capital en estado uniforme | conceptual_swap | high | $\frac{\dot{I}}{I} = s\lambda \ne \lambda$ | Dado que $I = sQ$ y $Q$ crece a tasa $\lambda$, la inversión neta $I$ crece rigurosamente a la tasa $\lambda$. |
| `D-C03-05` | Negar que la relación capital-producto sea constante a lo largo de la senda equilibrada | conceptual_swap | high | $\frac{K}{Q} \text{ crece a tasa } \lambda \text{ en el estado uniforme}$ | En estado uniforme, tanto $K$ como $Q$ crecen a la misma tasa $\lambda$, de modo que el coeficiente de capital $K/Q$ permanece rigurosamente invariante. |
| `D-C03-06` | Creer que el progreso tecnológico neutral desplaza la tasa de crecimiento del capital per cápita a cero en todo momento | conceptual_swap | high | $\dot{k}/k = 0 \text{ incluso con progreso técnico exógeno multiplicativo}$ | Al incorporarse tecnología creciente $T(t)$, la curva de ahorro se desplaza secularmente hacia arriba, aumentando continuamente el capital por trabajador. |

---

### [Hab-02] Linealización y Resolución de la Ecuación de Bernoulli Cobb-Douglas (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 4: Linealización y Resolución de la Ecuación de Bernoulli Cobb-Douglas
- **Prerequisites:** H-02, C-03
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Para una función de producción Cobb-Douglas $Q = K^\alpha L^{1-\alpha}$, la ecuación fundamental $\dot{k} + \lambda k = s k^\alpha$ es de Bernoulli. Al definir el cambio de variable $z \equiv k^{1-\alpha}$, linealizarla en la forma canónica $\frac{dz}{dt} + (1-\alpha)\lambda z = (1-\alpha)s$ y obtener su solución general por factor integrante.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Error de signo en la potencia de la sustitución de Bernoulli | skipped_step | high | $z = k^{\alpha - 1}$ | Para la ecuación $\dot{k} + P(t)k = Q(t)k^m$, la sustitución linealizadora estándar es $z = k^{1-m}$, lo que para $m=\alpha$ da $z = k^{1-\alpha}$. |
| `D-Hab02-02` | Omisión del factor (1-alpha) al aplicar la regla de la cadena a la derivada | skipped_step | high | $\frac{dz}{dt} = k^{-\alpha}\dot{k} \implies \frac{dz}{dt} + \lambda z = s$ | Al derivar $z = k^{1-\alpha}$ respecto al tiempo, la regla de la cadena exige multiplicar por la derivada de la potencia: $\frac{dz}{dt} = (1-\alpha)k^{-\alpha}\dot{k}$. |
| `D-Hab02-03` | Omitir el término homogéneo exponencial transitorio en la trayectoria temporal | conceptual_swap | high | $z(t) = \frac{s}{\lambda}$ | La solución de una ecuación diferencial lineal de primer orden contiene la solución complementaria transitoria que decae exponencialmente. |
| `D-Hab02-04` | Uso incorrecto del signo en el exponente de decaimiento temporal | conceptual_swap | high | $z(t) = \left[z(0) - \frac{s}{\lambda}\right]e^{(1-\alpha)\lambda t} + \frac{s}{\lambda}$ | El factor integrante $e^{\int (1-\alpha)\lambda dt}$ introduce un signo negativo en la función exponencial de la solución homogénea. |
| `D-Hab02-05` | Inversión del exponente al recuperar k(t) a partir de z(t) | conceptual_swap | high | $k(t) = [z(t)]^{1-\alpha}$ | Si $z = k^{1-\alpha}$, la función inversa exige elevar $z$ al exponente recíproco $\frac{1}{1-\alpha}$. |
| `D-Hab02-06` | Confundir el parámetro alfa con el factor de elasticidad laboral | conceptual_swap | high | $z = k^\alpha$ | El exponente de la variable de estado $k$ en la función intensiva es $\alpha$; por tanto, el término de acoplamiento es $1-\alpha$. |

---

### [Hab-03] Cálculo del Capital de Estado Uniforme y Estática Comparativa (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 5: Cálculo del Capital de Estado Uniforme y Estática Comparativa
- **Prerequisites:** Hab-02
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 5)

#### Description & Cognitive Model
Determinar el nivel analítico de capital por trabajador en el estado uniforme igualando $\dot{k} = 0 \implies s \bar{k}^\alpha = \lambda \bar{k}$, obteniendo $\bar{k} = \left(\frac{s}{\lambda}\right)^{\frac{1}{1-\alpha}}$, y calcular sus derivadas parciales respecto a $s$ y $\lambda$ para evaluar impactos de política.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Inversión del cociente paramétrico en el valor de equilibrio | skipped_step | high | $\bar{k} = \left(\frac{\lambda}{s}\right)^{\frac{1}{1-\alpha}}$ | El capital de equilibrio es directamente proporcional al ahorro e inversamente proporcional al crecimiento demográfico: $\bar{k} = (s/\lambda)^{1/(1-\alpha)}$. |
| `D-Hab03-02` | Omisión del exponente de rendimientos decrecientes en el capital estacionario | skipped_step | high | $\bar{k} = \frac{s}{\lambda}$ | La relación $s/\lambda$ corresponde a $\bar{k}^{1-\alpha}$; para obtener $\bar{k}$ se debe elevar a la potencia fraccionaria $\frac{1}{1-\alpha}$. |
| `D-Hab03-03` | Signo incorrecto en la estática comparativa frente al crecimiento poblacional | conceptual_swap | high | $\frac{\partial \bar{k}}{\partial \lambda} > 0$ | Un aumento en el crecimiento poblacional exige más inversión simplemente para equipar a los nuevos obreros, reduciendo la dotación media en equilibrio. |
| `D-Hab03-04` | Cálculo erróneo del producto por trabajador de estado uniforme | conceptual_swap | high | $\bar{q} = \left(\frac{s}{\lambda}\right)^{\frac{1}{1-\alpha}}$ | El producto per cápita en estado uniforme es $\phi(\bar{k}) = \bar{k}^\alpha = (s/\lambda)^{\frac{\alpha}{1-\alpha}}$, no $\bar{k}$. |
| `D-Hab03-05` | Asumir elasticidad unitaria del capital estacionario respecto al ahorro | conceptual_swap | high | $\frac{\partial \ln \bar{k}}{\partial \ln s} = 1$ | Debido a la curvatura de la producción, la elasticidad del capital respecto al ahorro es $\frac{1}{1-\alpha}$, la cual es estrictamente mayor que 1. |
| `D-Hab03-06` | Confusión entre la tasa de crecimiento de k y el valor absoluto de bar k ante aumentos de s | conceptual_swap | high | $\text{Un aumento en } s \text{ eleva permanentemente } \left.\frac{\dot{k}}{k}\right|_{t \to \infty}$ | Un cambio paramétrico en $s$ tiene efecto nivel permanente sobre $\bar{k}$ y $\bar{q}$, pero solo efectos transitorios sobre la tasa de crecimiento de $k$. |

---

### [C-04] Colapso del Filo de la Navaja de Harrod-Domar bajo Proporciones Fijas (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 10: Colapso del Filo de la Navaja de Harrod-Domar bajo Proporciones Fijas
- **Prerequisites:** C-01, H-02
- **Evidence Citations:** `solow1956.pdf` (page 10)

#### Description & Cognitive Model
En la tecnología con proporciones fijas $Y = \min\left(\frac{K}{a}, \frac{L}{b}\right)$, la ley de movimiento $\dot{r} = s\min\left(\frac{r}{a}, \frac{1}{b}\right) - nr$ genera desequilibrios estructurales insolubles por mercado: si $n > \frac{s}{a}$, el capital es el cuello de botella y surge desempleo secular creciente; si $n < \frac{s}{a}$, el trabajo es el cuello de botella y surge capacidad ociosa redundante.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Creer que la flexibilidad salarial elimina el desempleo con proporciones fijas | conceptual_swap | high | $\text{Un descenso en } w \text{ restablece el pleno empleo cuando } n > \frac{s}{a}$ | Con proporciones fijas, la imposibilidad de sustitución física impide que los precios absorban el exceso de factor; si no hay máquinas, no puede contratarse mano de obra. |
| `D-C04-02` | Inversión de los roles de cuello de botella según las tasas natural y garantizada | conceptual_swap | high | $n > \frac{s}{a} \implies \text{El trabajo es el factor redundante con exceso de capital}$ | Cuando la tasa natural de población supera la tasa garantizada de ahorro $s/a$, la acumulación de capital no alcanza a equipar a toda la masa laboral. |
| `D-C04-03` | Asumir que el filo de la navaja persiste bajo isocuantas convexas diferenciables | conceptual_swap | high | $\text{El modelo de Solow conserva la inestabilidad de filo de la navaja de Harrod-Domar}$ | Solow demuestra que la aparente inestabilidad de Harrod-Domar es un artefacto del supuesto rígido de coeficientes fijos, y desaparece con factores sustituibles. |
| `D-C04-04` | Confusión en el valor del coeficiente de aceleración a | conceptual_swap | high | $a = \frac{Y}{K}$ | El coeficiente $a$ representa las unidades de capital necesarias para producir una unidad de producto, es decir, la inversa de la productividad del capital. |
| `D-C04-05` | Creer que n = s/a se alcanza endógenamente mediante mecanismos de mercado en coeficientes fijos | conceptual_swap | high | $\frac{s}{a} \to n \text{ automáticamente sin intervención con tecnología Leontief}$ | En Harrod-Domar, los tres parámetros $s, a, n$ son exógenos e independientes, por lo que su igualdad es un 'accidente fortuito' sin mecanismo estabilizador. |
| `D-C04-06` | Afirmar que la productividad marginal del capital es positiva cuando r > a/b | conceptual_swap | high | $\text{PMg}_K > 0 \text{ cuando } r > \frac{a}{b}$ | Cuando $r > a/b$, la mano de obra limita el producto y cualquier unidad adicional de capital permanece ociosa, con productividad marginal nula. |

---

### [Hab-04] Determinación de la Condición de Existencia de Equilibrio en Tecnologías CES (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 14: Determinación de la Condición de Existencia de Equilibrio en Tecnologías CES
- **Prerequisites:** H-02, C-02
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Para una función de producción CES con $\rho = 1/2$, $Y = (a\sqrt{K} + \sqrt{L})^2$, formular la ecuación diferencial intensiva $\dot{r} = s(a\sqrt{r} + 1)^2 - nr$ y determinar algebraicamente la condición de existencia de estado estacionario estable $sa^2 < n$, despejando el valor $r^* = \left(\frac{1}{\sqrt{n/s} - a}\right)^2$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Inversión de la condición de umbral para existencia de estado estacionario | skipped_step | high | $sa^2 > n \implies \text{Existe estado estacionario estable}$ | Si $sa^2 > n$, la curva de ahorro crece asintóticamente más rápido que el rayo demográfico $nr$, haciendo imposible la existencia de un estado estacionario. |
| `D-Hab04-02` | Error de despeje algebraico en la raíz cuadrada de la ecuación característica | skipped_step | high | $r^* = \left(\frac{1}{\sqrt{n/s} + a}\right)^2$ | Al resolver $s(a\sqrt{r}+1)^2 = nr$, se extrae raíz cuadrada obteniendo $\sqrt{s}(a\sqrt{r}+1) = \sqrt{n}\sqrt{r}$, de donde $\sqrt{r}(\sqrt{n} - a\sqrt{s}) = \sqrt{s}$. |
| `D-Hab04-03` | Omitir la constante de interacción cruzada al expandir la función intensiva | conceptual_swap | high | $F(r, 1) = a^2 r + 1$ | El binomio al cuadrado contiene el doble producto de los términos: $(a\sqrt{r} + 1)^2 = a^2 r + 2a\sqrt{r} + 1$. |
| `D-Hab04-04` | Asumir que la tecnología CES con sustitución alta siempre garantiza estado estacionario | conceptual_swap | high | $\forall a, s, n \implies \exists r^* > 0$ | Cuando la productividad marginal del capital no converge a cero para $r \to \infty$, una tasa de ahorro suficientemente alta genera crecimiento perpetuo. |
| `D-Hab04-05` | Cálculo erróneo del producto por trabajador estacionario en la CES | conceptual_swap | high | $y^* = \frac{1}{1 - a\sqrt{s/n}}$ | Al evaluar $y^* = (a\sqrt{r^*} + 1)^2$, se obtiene $y^* = \frac{1}{(1 - a\sqrt{s/n})^2}$, lo que exige elevar el denominador al cuadrado. |
| `D-Hab04-06` | Confusión entre el parámetro rho de sustitución y el parámetro de escala a | conceptual_swap | high | $\rho = a$ | En la especificación CES $Y = (a K^\rho + L^\rho)^{1/\rho}$, el exponente $\rho = 1/2$ determina la sustituibilidad, mientras que $a$ es un coeficiente de ponderación. |

---

### [H-03] Ecuación de Arbitraje de Activos de Bienes de Capital y Tasa Propia (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 17: Ecuación de Arbitraje de Activos de Bienes de Capital y Tasa Propia
- **Prerequisites:** None
- **Evidence Citations:** `solow1956.pdf` (page 17)

#### Description & Cognitive Model
En equilibrio competitivo continuo sin incertidumbre, el arbitraje entre activos financieros y bienes de capital impone que la tasa de interés monetaria $i(t)$ iguale la tasa de rendimiento propio del capital más la ganancia de capital: $i(t) = \frac{q(t)}{p(t)} + \frac{\dot{p}(t)}{p(t)}$, donde $q(t)$ es el alquiler del capital y $p(t)$ su precio de transferencia.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H03-01` | Omisión de las ganancias o pérdidas de capital en la condición de no arbitraje | conceptual_swap | high | $i(t) = \frac{q(t)}{p(t)}$ | Un tenedor de capital percibe tanto el flujo de servicios reales de alquiler $q/p$ como la variación en el valor patrimonial del bien $\dot{p}/p$. |
| `D-H03-02` | Inversión de signo en el término de ganancia de capital | conceptual_swap | high | $i(t) = \frac{q(t)}{p(t)} - \frac{\dot{p}(t)}{p(t)}$ | Si el precio del capital sube ($\dot{p} > 0$), la posesión de bienes de capital genera una ganancia de capital positiva que se suma al canon de alquiler. |
| `D-H03-03` | Confundir precio del producto con tasa de interés en la fórmula de valor presente | conceptual_swap | high | $p(t) = \int_t^\infty q(u) du$ | El precio de compra de una unidad de capital $p(t)$ debe ser el valor actual descontado de la corriente futura infinita de ingresos por alquiler. |
| `D-H03-04` | Asumir que el canon real de alquiler q/p es independiente del ratio capital-trabajo | conceptual_swap | high | $\frac{q}{p} = \text{constante}$ | En una economía competitiva con rendimientos constantes, la rentabilidad real de los servicios del capital $q/p$ equivale estrictamente a su producto marginal $\phi'(k)$. |
| `D-H03-05` | Intercambio de roles entre la tasa monetaria de interés y la tasa propia del bien | conceptual_swap | high | $\text{Tasa propia} = i(t) + \frac{\dot{p}}{p}$ | La tasa propia en unidades de capital es $q/p$, la cual equivale a la tasa monetaria deducida la inflación del bien de capital. |
| `D-H03-06` | Creer que con precios constantes p(t) persiste divergencia entre i y q/p | conceptual_swap | high | $\dot{p} = 0 \implies i(t) \ne \frac{q(t)}{p(t)}$ | Cuando el nivel general de precios es constante ($\dot{p} = 0$), el arbitraje perfecto colapsa la tasa de interés nominal exactamente a la renta real del capital. |

---

### [C-05] Comportamiento de Precios de Factores y Distribución Funcional Neoclásica (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 20: Comportamiento de Precios de Factores y Distribución Funcional Neoclásica
- **Prerequisites:** H-03, C-01
- **Evidence Citations:** `solow1956.pdf` (page 20)

#### Description & Cognitive Model
En equilibrio competitivo, los factores reciben sus productos marginales reales: $\frac{w}{p} = \frac{\partial F}{\partial L} = \phi(k) - k\phi'(k)$ y $\frac{q}{p} = \frac{\partial F}{\partial K} = \phi'(k)$. Al aumentar la dotación $k$, la tasa de alquiler real $q/p$ cae monótonamente mientras que el salario real $w/p$ y la relación de precios relativos $w/q$ aumentan estrictamente.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Creer que la tasa de interés debe caer indefinidamente para sostener el crecimiento de largo plazo | conceptual_swap | high | $\lim_{t \to \infty} \frac{q}{p} = 0 \text{ obligatoriamente para evitar el desempleo}$ | Solow demuestra, contra Harrod, que la tasa de interés no requiere caer perpetuamente hacia cero, sino que converge a un valor constante determinado por $\bar{k}$. |
| `D-C05-02` | Inversión de la respuesta del salario real ante la acumulación de capital | conceptual_swap | high | $\frac{d(w/p)}{dk} < 0$ | Dado que $\phi''(k) < 0$, un mayor capital por trabajador incrementa la productividad marginal del trabajo y, por ende, el salario real de equilibrio. |
| `D-C05-03` | Asumir que las participaciones factoriales varían en la función Cobb-Douglas | conceptual_swap | high | $\frac{wL}{pY} = f(k, s, n)$ | La tecnología Cobb-Douglas presenta elasticidad unitaria de sustitución, fijando la participación del trabajo en $1-\alpha$ independientemente de los precios factoriales. |
| `D-C05-04` | Confundir la pendiente de la isocuanta con el ratio de cantidades en vez de precios | conceptual_swap | high | $-\frac{dK}{dL} = \frac{K}{L}$ | La pendiente de la isocuanta mide la tasa marginal de sustitución técnica, la cual en equilibrio competitivo se iguala al cociente de precios de factores $w/q$. |
| `D-C05-05` | Atribuir indeterminación de precios de factores a cualquier nivel de k | conceptual_swap | high | $\text{Los precios factoriales son indeterminados para todo } k$ | Bajo rendimientos constantes y funciones estrictamente diferenciables, los productos marginales determinan unívocamente $w/p$ y $q/p$ para cada valor de $k$. |
| `D-C05-06` | Ignorar el agotamiento del producto en la distribución del ingreso | conceptual_swap | high | $\frac{w}{p}L + \frac{q}{p}K \ne Y$ | Por el Teorema de Euler en grado 1, la remuneración de los factores según su productividad marginal agota exactamente el producto total $Y$. |

---

### [Hab-05] Modelación del Progreso Técnico Neutral y Dinámica Asintótica de Crecimiento (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 22: Modelación del Progreso Técnico Neutral y Dinámica Asintótica de Crecimiento
- **Prerequisites:** Hab-02, C-03
- **Evidence Citations:** `solow1956.pdf` (page 22)

#### Description & Cognitive Model
Bajo progreso tecnológico Hicks-neutral $Y = e^{gt} K^\alpha L^{1-\alpha}$, derivar la ecuación diferencial de acumulación $\dot{K} = s e^{gt} K^\alpha (L_0 e^{nt})^{1-\alpha}$ y resolverla mostrando que la tasa asintótica de crecimiento del capital es $n + \frac{g}{1-\alpha}$ y la del producto per cápita es $\frac{g}{1-\alpha}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Omitir el efecto multiplicador del ahorro en la tasa de crecimiento del capital con tecnología | skipped_step | high | $\frac{\dot{K}}{K} = n + g$ | El progreso tecnológico genera mayor producto, lo que induce mayor inversión y amplifica el ritmo de acumulación por encima de la suma directa $n+g$. |
| `D-Hab05-02` | Asignación errónea de la tasa de crecimiento del capital al producto por trabajador | skipped_step | high | $\frac{\dot{y}}{y} = n + \frac{g}{1-\alpha}$ | El producto por trabajador $y = Y/L$ descuenta el crecimiento demográfico $n$, expandiéndose a la tasa neta $\frac{g}{1-\alpha}$. |
| `D-Hab05-03` | Suponer convergencia a una relación capital-trabajo finita constante | conceptual_swap | high | $\lim_{t \to \infty} \frac{\dot{k}}{k} = 0 \text{ con progreso técnico neutral continuo}$ | Con progreso técnico continuo, la relación capital-trabajo $k$ nunca se estanca en un valor constante, sino que crece sostenidamente a tasa $\frac{g}{1-\alpha}$. |
| `D-Hab05-04` | Inversión de los ponderadores elásticos en el factor tecnológico | conceptual_swap | high | $\frac{\dot{K}}{K} = n + \frac{g}{\alpha}$ | La tasa compuesta de amplificación tecnológica depende de la participación del trabajo $1-\alpha$, ya que la tecnología neutral impulsa la eficiencia laboral. |
| `D-Hab05-05` | Asumir que la participación del trabajo en el producto colapsa a cero con progreso técnico | conceptual_swap | high | $\lim_{t \to \infty} \frac{wL}{Y} = 0$ | Bajo especificación Cobb-Douglas, aun cuando los salarios reales aumentan continuamente al ritmo $\frac{g}{1-\alpha}$, la participación distributiva permanece exactamente en $1-\alpha$. |
| `D-Hab05-06` | Ignorar el crecimiento secular de la relación capital-producto | conceptual_swap | high | $\frac{K}{Y} = \text{constante en presencia de tecnología Hicks-neutral pura}$ | Solow demuestra que con progreso multiplicativo neutral $e^{gt}$, el cociente capital-producto crece a la tasa $g = (n + g/(1-\alpha)) - (n + \alpha g/(1-\alpha))$. |

---

### [Hab-06] Evaluación del Impacto de la Política Fiscal en la Acumulación de Capital (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 26: Evaluación del Impacto de la Política Fiscal en la Acumulación de Capital
- **Prerequisites:** H-02, Hab-03
- **Evidence Citations:** `solow1956.pdf` (page 26)

#### Description & Cognitive Model
Modelar la intervención estatal mediante un impuesto proporcional a la renta $t \in (0, 1)$ donde una fracción $v \in [0, 1]$ del recaudo se destina a inversión pública y el resto a consumo, obteniendo la tasa de ahorro efectiva modificada $s^* = s + (v - s)t$, y determinar la dirección del desplazamiento del stock de capital de estado uniforme.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Asumir que la tributación siempre reduce la tasa de ahorro y el capital de equilibrio | skipped_step | high | $s^* < s \quad \forall v \in [0, 1]$ | Si el Estado invierte una proporción de los impuestos mayor que la propensión privada al ahorro ($v > s$), el impuesto eleva la tasa de ahorro agregada. |
| `D-Hab06-02` | Error algebraico en el cálculo de la tasa de ahorro agregada con impuestos | skipped_step | high | $s^* = s(1 - t) + vt = s + (v - 1)t$ | Al expandir $s(1-t) + vt = s - st + vt = s + (v-s)t$, el coeficiente neto sobre la tasa impositiva es $v-s$. |
| `D-Hab06-03` | Creer que el impuesto sobre la renta altera la tasa de crecimiento asintótica de la economía | conceptual_swap | high | $\lim_{t \to \infty} \frac{\dot{Q}}{Q} = n + f(t)$ | La política tributaria modifica el nivel de capital y producto per cápita en estado uniforme, pero la tasa de crecimiento asintótica sigue regida por $n$. |
| `D-Hab06-04` | Negar que la tasa impositiva afecte los precios relativos de equilibrio de los factores | conceptual_swap | high | $\frac{w}{q} \text{ es estrictamente independiente de } t$ | Al alterar la tasa de ahorro efectiva $s^*$, la relación capital-trabajo $r^*$ se desplaza, induciendo un nuevo vector de equilibrio para salarios y alquileres. |
| `D-Hab06-05` | Confusión en el destino del gasto cuando todo el recaudo se consume públicamente | conceptual_swap | high | $v = 0 \implies s^* = s$ | Si los impuestos se destinan íntegramente al consumo gubernamental ($v=0$), la tasa efectiva de ahorro cae a $s(1-t)$, reduciendo el stock de capital. |
| `D-Hab06-06` | Aplicar el impuesto sobre el capital en vez de sobre el flujo total de producto | conceptual_swap | high | $\dot{K} = sY - tK$ | El análisis de E. Cary Brown en Solow contempla un gravamen proporcional sobre el producto o ingreso real $Y$, no un gravamen sobre el stock de capital físico. |

---

### [C-06] Equilibrios Múltiples y la Trampa de Pobreza Demográfica (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 27: Equilibrios Múltiples y la Trampa de Pobreza Demográfica
- **Prerequisites:** C-02, H-02
- **Evidence Citations:** `solow1956.pdf` (page 27)

#### Description & Cognitive Model
Cuando la tasa de crecimiento poblacional es endógena al nivel de vida $n = n(r)$, la curva de ensanchamiento demográfico $n(r)r$ puede intersectar a la curva de ahorro $sF(r, 1)$ en múltiples puntos, generando un equilibrio estable de bajo nivel de ingresos (trampa de pobreza) en $r_1$ y un umbral inestable de despegue en $r_2$, requiriendo un 'gran empujón' de inversión para alcanzar el crecimiento sostenido.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Clasificar el umbral intermedio r2 como un atractor estable | conceptual_swap | high | $r_2 \text{ es un atractor local al que convergen economías con dotación cercana}$ | En $r_2$, la curva $n(r)r$ corta desde abajo a $sF(r, 1)$, haciendo que cualquier perturbación positiva impulse a la economía hacia arriba y cualquier caída la regrese a $r_1$. |
| `D-C06-02` | Asumir que las trampas de pobreza requieren obligatoriamente rendimientos crecientes a escala | conceptual_swap | high | $\text{Los equilibrios múltiples solo pueden existir con indivisibilidades tecnológicas o economías de escala}$ | Solow demuestra explícitamente que no se requieren rendimientos crecientes; la no-linealidad en la respuesta poblacional $n(r)$ es suficiente para generar trampas de pobreza. |
| `D-C06-03` | Creer que pequeños incrementos graduales de capital pueden superar la trampa en r1 | conceptual_swap | high | $\text{Pequeños incrementos marginales de capital acumulan suficiente impulso para cruzar } r_2$ | Para dotaciones iniciales menores que $r_2$, las fuerzas endógenas devuelven al sistema hacia la trampa $r_1$, exigiendo un esfuerzo masivo discontinuo ('big push'). |
| `D-C06-04` | Inversión de las cuencas de atracción de los equilibrios | conceptual_swap | high | $r_0 > r_2 \implies r \to r_1$ | Una vez que la dotación de capital supera el umbral crítico $r_2$, la economía se desmarca de la trampa y converge hacia estados de alto ingreso. |
| `D-C06-05` | Asumir que la tasa de crecimiento demográfico es monótona creciente para todo nivel de renta | conceptual_swap | high | $n(r) \text{ crece indefinidamente con el ingreso per cápita}$ | La curva de crecimiento poblacional de Solow refleja la transición demográfica: aumenta en etapas de subsistencia y disminuye en etapas avanzadas de desarrollo. |
| `D-C06-06` | Afirmar que en r1 el ingreso per cápita crece indefinidamente | conceptual_swap | high | $\frac{\dot{y}}{y} > 0 \text{ en el equilibrio de trampa } r_1$ | En $r_1$, la economía se encuentra en un estado uniforme estable pero de bajísima productividad, donde el ahorro apenas cubre el vertiginoso ritmo demográfico. |

---
