# Cognitive Task Analysis (CTA): Practica Parcial Saul Standard Coarse V2

- **Course ID:** `practica_parcial_saul_standard_coarse_v2`
- **Macro-Competency:** Dominio y aplicación analítica integral de Practica Parcial Saul Standard Coarse V2
- **Structure:** 14 total competencies (0 Facts, 5 Concepts, 9 Skills) with 84 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `Hab-01` | Resolución de EDPs Cuasilineales de Primer Orden mediante el Método de Lagrange y Curvas Características | Skill | Apply | Unidad 1: Resolución de EDPs Cuasilineales de Primer Orden mediante el Método de Lagrange y Curvas Características | - | 6 |
| `Hab-02` | Modelización y Optimización Económica mediante EDPs de Primer Orden y Teorema de Euler | Skill | Apply | Unidad 2: Modelización y Optimización Económica mediante EDPs de Primer Orden y Teorema de Euler | Hab-09 | 6 |
| `C-01` | Dualidad Microeconómica y EDPs de Homogeneidad de Euler | Concept | Understand | Unidad 1: Dualidad Microeconómica y EDPs de Homogeneidad de Euler | - | 6 |
| `Hab-03` | Modelado y Resolución de EDPs de Precios Espaciales con Costos de Transporte | Skill | Apply | Unidad 3: Modelado y Resolución de EDPs de Precios Espaciales con Costos de Transporte | C-05 | 6 |
| `Hab-04` | Resolución Analítica, Linealización y Evaluación de Perturbaciones en Sistemas Dinámicos 2D | Skill | Apply | Unidad 2: Resolución Analítica, Linealización y Evaluación de Perturbaciones en Sistemas Dinámicos 2D | C-05 | 6 |
| `C-02` | Clasificación Cualitativa de Estados Estacionarios y Diagramas de Fase en Sistemas Continuos | Concept | Analyze | Unidad 4: Clasificación Cualitativa de Estados Estacionarios y Diagramas de Fase en Sistemas Continuos | - | 6 |
| `C-03` | Fundamentos, Clasificación y Estructura de Solución de Ecuaciones en Derivadas Parciales | Concept | Understand | Unidad 10: Fundamentos, Clasificación y Estructura de Solución de Ecuaciones en Derivadas Parciales | - | 6 |
| `Hab-05` | Resolución de EDPs Cuasilineales de Primer Orden mediante Curvas Características y el Sistema Auxiliar de Lagrange | Skill | Apply | Unidad 23: Resolución de EDPs Cuasilineales de Primer Orden mediante Curvas Características y el Sistema Auxiliar de Lagrange | C-05 | 6 |
| `C-04` | Estructura Matricial y Estabilidad Dinámica de Sistemas Macroeconómicos Lineales | Concept | Understand | Unidad 5: Estructura Matricial y Estabilidad Dinámica de Sistemas Macroeconómicos Lineales | - | 6 |
| `Hab-06` | Linealización y Análisis Cualitativo de Sistemas Dinámicos no Lineales en Economía | Skill | Apply | Unidad 15: Linealización y Análisis Cualitativo de Sistemas Dinámicos no Lineales en Economía | C-05 | 6 |
| `Hab-07` | Resolución de Sistemas Lineales de EDO mediante Autovalores y Autovectores | Skill | Apply | Unidad 6: Resolución de Sistemas Lineales de EDO mediante Autovalores y Autovectores | - | 6 |
| `Hab-08` | Linealización de Sistemas Dinámicos No Lineales en Puntos de Equilibrio | Skill | Apply | Unidad 13: Linealización de Sistemas Dinámicos No Lineales en Puntos de Equilibrio | Hab-09 | 6 |
| `Hab-09` | Análisis Cualitativo de Sistemas de EDOs mediante Isoclinas y Diagramas de Fase | Skill | Apply | Unidad 6: Análisis Cualitativo de Sistemas de EDOs mediante Isoclinas y Diagramas de Fase | C-05 | 6 |
| `C-05` | Clasificación de Estabilidad de Sistemas de EDOs 2x2 mediante Traza y Determinante | Concept | Understand | Unidad 8: Clasificación de Estabilidad de Sistemas de EDOs 2x2 mediante Traza y Determinante | - | 6 |

---

## Detailed Competency Specifications

### [Hab-01] Resolución de EDPs Cuasilineales de Primer Orden mediante el Método de Lagrange y Curvas Características (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 1: Resolución de EDPs Cuasilineales de Primer Orden mediante el Método de Lagrange y Curvas Características
- **Prerequisites:** None
- **Evidence Citations:** `MATH_IV_Problem_Set_I.pdf` (page 1)

#### Description & Cognitive Model
Resolver ecuaciones en derivadas parciales cuasilineales de primer orden de la forma $P(x, y, U) U_x + Q(x, y, U) U_y = R(x, y, U)$ mediante el método de Lagrange y curvas características, determinando dos integrales primeras independientes $u(x, y, U) = c_1$ y $v(x, y, U) = c_2$ a partir del sistema auxiliar $\frac{dx}{P} = \frac{dy}{Q} = \frac{dU}{R}$, y aplicando condiciones de contorno para hallar soluciones particulares o implícitas de la forma $\phi(u, v) = 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Inversión incorrecta de coeficientes en el sistema auxiliar de Lagrange | skipped_step | high | $\frac{dx}{Q} = \frac{dy}{P} = \frac{dU}{R}$ | Los denominadores en el sistema característico corresponden a los coeficientes de las derivadas parciales respectivas: dx con P(x, y, U) y dy con Q(x, y, U). |
| `D-Hab01-02` | Dependencia funcional entre integrales primeras | skipped_step | high | $v(x, y, U) = g(u(x, y, U)) \implies \phi(u, v) = 0 \text{ define la solución general}$ | Para que la solución general $\phi$(u, v) = 0 sea válida, las integrales primeras u y v deben ser funcionalmente independientes (sus gradientes no colineales). |
| `D-Hab01-03` | Tratamiento erróneo del término no homogéneo en cuasilinealidad | conceptual_swap | high | $\frac{dx}{P} = \frac{dy}{Q} \text{ resuelve completamente la EDP ignorando el término } \frac{dU}{R}$ | El término de la función incógnita U evoluciona a lo largo de las características según dU/R; no puede resolverse solo en el plano (x, y). |
| `D-Hab01-04` | Evaluación incorrecta de la condición inicial de frontera de Cauchy | skipped_step | high | $U(x, x) = x^2 \implies \phi(x, x) = x^2$ | Para hallar la solución particular sujeta a una curva inicial, evalúe las integrales primeras u y v a lo largo de la parametrización de la curva de datos. |
| `D-Hab01-05` | Uso inadecuado de multiplicadores de Lagrange para el sistema auxiliar | conceptual_swap | high | $\frac{\alpha dx + \beta dy + \gamma dU}{\alpha P + \beta Q + \gamma R} = \text{constante sin anular el denominador}$ | Al aplicar el método de multiplicadores, la combinación lineal en el denominador debe anularse ($\alpha$ P + $\beta$ Q + $\gamma$ R = 0) para que el numerador sea una diferencial exacta. |
| `D-Hab01-06` | Confusión entre coordenadas características y solución explícita final | skipped_step | high | $U(s, t) \text{ es la solución final sin invertir } (s, t) \to (x, y)$ | Una vez integrada la EDP a lo largo de las características en términos de (s, t), es indispensable despejar los parámetros (s, t) en función de las variables originales (x, y). |

---

### [Hab-02] Modelización y Optimización Económica mediante EDPs de Primer Orden y Teorema de Euler (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 2: Modelización y Optimización Económica mediante EDPs de Primer Orden y Teorema de Euler
- **Prerequisites:** Hab-09
- **Evidence Citations:** `MATH_IV_Problem_Set_I.pdf` (page 2)

#### Description & Cognitive Model
Formular y resolver ecuaciones en derivadas parciales de primer orden aplicadas a la teoría del consumidor y de la producción, incluyendo la determinación de funciones de utilidad y cálculo de la relación marginal de sustitución $\text{RMS} = -\frac{U_\gamma}{U_\theta}$, la resolución de la EDP de Euler $K F_K + L F_L = n F$ sujeta a condiciones de contorno para funciones de producción homogéneas de grado $n$, y la posterior derivación de funciones de costo mínimo, demandas condicionadas y no condicionadas de factores, oferta y beneficios.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Inversión errónea del cociente en la Relación Marginal de Sustitución | skipped_step | high | $\text{RMS} = \frac{U_\theta}{U_\gamma}$ | La RMS de ocio ($\gamma$) por ingreso ($\theta$) representa la tasa a la que se sustituyen ambos bienes manteniendo la utilidad constante: U_$\gamma$ / U_$\theta$. |
| `D-Hab02-02` | Confusión en la formulación de la EDP del Teorema de Euler para homogeneidad | conceptual_swap | high | $K \frac{\partial F}{\partial L} + L \frac{\partial F}{\partial K} = n F(K, L)$ | El teorema de Euler establece que cada variable se multiplica por su propia derivada parcial respecto a dicha variable: K F_K + L F_L = n F. |
| `D-Hab02-03` | Omisión del grado de homogeneidad en la ecuación de Lagrange | skipped_step | high | $\frac{dK}{K} = \frac{dL}{L} = \frac{dF}{F} \text{ para cualquier función homogénea}$ | En la ecuación de Euler K F_K + L F_L = nF, el denominador correspondiente a dF en las ecuaciones auxiliares debe ser nF, reflejando el grado de homogeneidad n. |
| `D-Hab02-04` | Confusión entre demandas condicionadas y no condicionadas de factores | conceptual_swap | high | $\text{Las demandas condicionadas } L^c(w, r, q) \text{ provienen de maximizar el beneficio } \pi(p, w, r)$ | Las demandas condicionadas provienen del problema de minimización de costos y dependen de (w, r, q); las demandas no condicionadas provienen de maximización de beneficios y dependen de (w, r, p). |
| `D-Hab02-05` | Aplicación incorrecta de la condición de frontera en la función de producción | skipped_step | high | $F(1, L) = L \implies F(K, L) = L \cdot K^n$ | Para determinar la función arbitraria f proveniente de las características (por ejemplo L/K), sustituya la condición dada F(1, L) = L en la solución general F = K^n f(L/K). |
| `D-Hab02-06` | Incompatibilidad en rendimientos crecientes y maximización de beneficios competitivos | skipped_step | high | $\text{Con } n = 2 \text{ existen demandas no condicionadas finitas y beneficios definidos en competencia perfecta}$ | Cuando la función de producción tiene rendimientos crecientes a escala (n=2), el beneficio no está acotado superiormente en competencia perfecta bajo precios dados de factores y producto. |

---

### [C-01] Dualidad Microeconómica y EDPs de Homogeneidad de Euler (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 1: Dualidad Microeconómica y EDPs de Homogeneidad de Euler
- **Prerequisites:** None
- **Evidence Citations:** `MATH_IV_Problem_Set_II_2026_II.pdf` (page 1)

#### Description & Cognitive Model
Fundamentación de funciones de valor óptimo mediante homogeneidad y ecuaciones diferenciales en derivadas parciales de primer orden: modelado del beneficio $\Pi(p, w)$ como homogéneo de grado 1 ($p \frac{\partial \Pi}{\partial p} + w \frac{\partial \Pi}{\partial w} = \Pi$) y la utilidad indirecta $V(p, m)$ como homogénea de grado 0 ($p \frac{\partial V}{\partial p} + m \frac{\partial V}{\partial m} = 0$), integrando condiciones de frontera para la identificación funcional y aplicando el Lema de Hotelling ($y = \frac{\partial \Pi}{\partial p}$, $L = -\frac{\partial \Pi}{\partial w}$) y la Identidad de Roy ($x = -\frac{V_p}{V_m}$).

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Confusión del grado de homogeneidad en la EDP de Euler para beneficios | conceptual_swap | high | Considerar que la función de beneficios $\Pi(p, w)$ es homogénea de grado 0 ante variaciones proporcionales de precios y salarios, planteando $p \frac{\partial \Pi}{\partial p} + w \frac{\partial \Pi}{\partial w} = 0$. | El beneficio es la diferencia entre ingresos nominales y costos nominales; al reescalar todos los precios nominales por un factor $t$, el beneficio queda multiplicado por $t$ (grado 1). |
| `D-C01-02` | Inversión de signo en el Lema de Hotelling para demandas de factores | conceptual_swap | high | Asumir que la demanda óptima de trabajo se obtiene derivando directamente el beneficio respecto al salario con signo positivo: $L(p, w) = \frac{\partial \Pi}{\partial w}$. | Un aumento salarial reduce las ganancias de la empresa competitiva; la demanda de factores no puede ser negativa en equilibrio normal. |
| `D-C01-03` | Falla de homogeneidad de grado 0 en utilidad indirecta por ilusión monetaria | conceptual_swap | high | Creer que un incremento proporcional equiparable de precio e ingreso ($tp, tm$) incrementa la utilidad indirecta del consumidor al disponer de mayor valor nominal $m$. | El bienestar del consumidor depende de su capacidad adquisitiva real de bienes y no del valor nominal del dinero; no existe ilusión monetaria. |
| `D-C01-04` | Omisión del signo negativo en la Identidad de Roy | conceptual_swap | high | Calcular la demanda marshalliana como el cociente directo de derivadas parciales sin signo negativo: $x(p, m) = \frac{V_p}{V_m}$. | La demanda marshalliana de un bien debe ser positiva; verifique que la derivada de la utilidad respecto al precio es estrictamente negativa. |
| `D-C01-05` | Interpretación errónea de homogeneidad como neutralidad tecnológica | conceptual_swap | high | Atribuir la homogeneidad de grado 1 de la función de beneficios a rendimientos constantes a escala de la función de producción de la empresa. | La homogeneidad de la función de beneficio es una propiedad nominal monetaria garantizada por la optimización con precios dados, independiente de los rendimientos a escala de la tecnología. |
| `D-C01-06` | Identificación incorrecta de la constante de integración con condición de frontera | conceptual_swap | high | Aplicar la condición observada $\Pi(p, 1) = \frac{1}{4}p^2$ asumiendo que $\Pi(p, w) = \frac{1}{4}p^2 w$, violando el grado 1 de homogeneidad. | Verifique que la solución obtenida satisfaga la ecuación diferencial de Euler multiplicando por el factor de escala homogéneo de grado 1. |

---

### [Hab-03] Modelado y Resolución de EDPs de Precios Espaciales con Costos de Transporte (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 3: Modelado y Resolución de EDPs de Precios Espaciales con Costos de Transporte
- **Prerequisites:** C-05
- **Evidence Citations:** `MATH_IV_Problem_Set_II_2026_II.pdf` (page 3)

#### Description & Cognitive Model
Formulación y resolución rigurosa de ecuaciones en derivadas parciales cuasilineales de precios geográficos $a \frac{\partial P}{\partial x} + b \frac{\partial P}{\partial y} = \tau$ a partir de la tasa de transporte a lo largo de trayectorias comerciales $\frac{dP}{ds} = \tau$, aplicando la regla de la cadena multivariada, resolviendo el sistema característico asociado bajo condiciones de frontera espaciales de Cauchy $P(x, 0) = P_0 + \alpha x$ para obtener la función explícita $P(x, y)$, y evaluando la estática comparativa y los límites de no arbitraje espacial.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Error de proyección direccional en la regla de la cadena espacial | skipped_step | high | Formular la variación del precio a lo largo de la ruta ignorando las velocidades direccionales, escribiendo $\frac{dP}{ds} = \frac{\partial P}{\partial x} + \frac{\partial P}{\partial y} = \tau$ sin ponderar por $a$ y $b$. | Recuerde que cada unidad de avance a lo largo del parámetro de la ruta $s$ desplaza las coordenadas en las tasas constantes $\frac{dx}{ds} = a$ y $\frac{dy}{ds} = b$. |
| `D-Hab03-02` | Inversión del parámetro característico en la condición inicial | skipped_step | high | Despejar erróneamente el parámetro de la curva característica como $s = \frac{b}{y}$ o $s = \frac{x}{b}$, distorsionando la retroproyección del dato inicial al eje $y = 0$. | Integre $\frac{dy}{ds} = b$ desde $s = 0$ hasta $s$ con $y(0) = 0$ para obtener la relación exacta $s = \frac{y}{b}$. |
| `D-Hab03-03` | Omisión de la acumulación de costos de transporte en la trayectoria característica | skipped_step | high | Asumir que el precio a lo largo de la característica es constante, ignorando el término fuente $\tau$ e igualando directamente $P(x, y) = P(x_0, 0)$. | El precio aumenta a razón de $\tau$ unidades monetarias por cada unidad de distancia recorrida; integre $\frac{dP}{ds} = \tau$ a lo largo de la característica. |
| `D-Hab03-04` | Confusión entre brecha de precios espaciales y oportunidad de arbitraje | conceptual_swap | high | Afirmar que toda disparidad de precios entre localidades $P(x_2, y_2) \neq P(x_1, y_1)$ para un producto homogéneo implica una falla de mercado o arbitraje no explotado. | El comercio territorial sólo permite arbitraje si la diferencia de precios excede los costos de transporte de desplazar el bien entre mercados. |
| `D-Hab03-05` | Falla de estática comparativa ante incremento del costo marginal de transporte | conceptual_swap | high | Sostener que un incremento en $\tau$ disminuye el precio final $P(x, y)$ o afecta únicamente a las localidades sobre el eje inicial $y = 0$. | Diferencie la solución explícita $P(x, y)$ respecto al costo marginal de transporte $\tau$ y evalúe su signo para localidades con coordenada $y > 0$. |
| `D-Hab03-06` | Omisión de la condición de Cauchy no homogénea en la frontera | skipped_step | high | Fijar una condición de frontera constante $P(x, 0) = P_0$, omitiendo el término de gradiente $\alpha x$ observado en las localidades sobre el eje $y = 0$. | Incorpore la totalidad de la información de frontera que indica que cada unidad adicional de $x$ incrementa el precio inicial en $\alpha$ unidades. |

---

### [Hab-04] Resolución Analítica, Linealización y Evaluación de Perturbaciones en Sistemas Dinámicos 2D (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 2: Resolución Analítica, Linealización y Evaluación de Perturbaciones en Sistemas Dinámicos 2D
- **Prerequisites:** C-05
- **Evidence Citations:** `MATH_IV_Problem_Set_III_2026_II.pdf` (page 2)

#### Description & Cognitive Model
Formulación matricial de sistemas dinámicos continuos de la forma $\dot{X} = AX + B$ o no lineales $\dot{X} = F(X)$, determinación algebraica de estados estacionarios $X^*$, cálculo analítico de la matriz jacobiana $J(X^*)$ y sus autovalores/autovectores, obtención de trayectorias temporales acopladas mediante diagonalización o método de coeficientes indeterminados, y evaluación del impacto de shocks de política o cambios paramétricos sobre el equilibrio y la velocidad de convergencia.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Omisión del término constante homogéneo al calcular la solución particular del sistema | skipped_step | high | $\text{La solución general de un sistema no homogéneo } \dot{X} = AX + B \text{ es simplemente la combinación lineal de los modos homogéneos } X_h(t) = c_1 v_1 e^{\lambda_1 t} + c_2 v_2 e^{\lambda_2 t}$ | En sistemas dinámicos con términos independientes constantes, el estado estacionario $X^* = -A^{-1}B$ actúa como la solución particular que desplaza el centro del sistema. |
| `D-Hab04-02` | Omisión de la evaluación del jacobiano en el estado estacionario durante la linealización | skipped_step | high | $\text{Para linealizar un sistema no lineal } \dot{X} = F(X)\text{, basta tomar la matriz de derivadas parciales con variables genéricas } (x, y) \text{ y calcular su determinante}$ | Las propiedades locales de estabilidad se obtienen evaluando todas las derivadas parciales del jacobiano en el punto fijo $(x^*, y^*)$; los autovalores resultantes deben ser números reales o complejos fijos. |
| `D-Hab04-03` | Error de signo en la inversión de la matriz del sistema para el estado estacionario | conceptual_swap | high | $\text{El estado estacionario de } \dot{X} = AX + B = 0 \text{ se despeja como } X^* = A^{-1}B$ | Al trasponer el vector de términos constantes $B$ al otro lado de la igualdad, recuerda cambiar su signo: $AX^* = -B$, por lo que $X^* = -A^{-1}B$. |
| `D-Hab04-04` | Ajuste incorrecto de las constantes de integración con condiciones iniciales | skipped_step | high | $\text{Las constantes de integración } c_1, c_2 \text{ son simplemente iguales a las condiciones iniciales } X(0) = (Y(0), r(0))'$ | En $t=0$, la ecuación es $X(0) = X_h(0) + X^* = v_1 c_1 + v_2 c_2 + X^*$; debes resolver el sistema lineal $V c = X(0) - X^*$ para encontrar $c_1$ y $c_2$. |
| `D-Hab04-05` | Confusión en la regla de derivación temporal de tasas de crecimiento agregadas | conceptual_swap | high | $\text{La derivada temporal de una tasa de crecimiento } g_z = \dot{z}/z \text{ se calcula como } \dot{g}_z = \ddot{z}/\dot{z}$ | Para variables combinadas $g_K = c_K (AL/K)^{1-\alpha}$, toma logaritmos naturales $\ln g_K = \ln c_K + (1-\alpha)[\ln A + \ln L - \ln K]$ y deriva respecto al tiempo para obtener $\frac{\dot{g}_K}{g_K} = (1-\alpha)[g_A + n - g_K]$. |
| `D-Hab04-06` | Mala atribución del cambio paramétrico en el análisis estático-comparativo | conceptual_swap | high | $\text{Un cambio en un parámetro de sensibilidad de inversión } \mu \text{ o de productividad } B \text{ solo altera la velocidad de transición sin modificar el estado estacionario}$ | Calcula la derivada estático-comparativa del estado estacionario respecto al parámetro alterado; verás que la posición del equilibrio cambia a la par que la matriz jacobiana y sus autovalores. |

---

### [C-02] Clasificación Cualitativa de Estados Estacionarios y Diagramas de Fase en Sistemas Continuos (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 4: Clasificación Cualitativa de Estados Estacionarios y Diagramas de Fase en Sistemas Continuos
- **Prerequisites:** None
- **Evidence Citations:** `MATH_IV_Problem_Set_III_2026_II.pdf` (page 4)

#### Description & Cognitive Model
Caracterización topológica y de estabilidad local de equilibrios en sistemas de ecuaciones diferenciales bidimensionales $\dot{x} = f(x, y)$, $\dot{y} = g(x, y)$ a partir de la traza $\operatorname{Tr}(J)$ y el determinante $\det(J)$ de la matriz jacobiana evaluada en el estado estacionario, identificando puntos silla ($\det(J) < 0$), nodos o focos estables ($\det(J) > 0, \operatorname{Tr}(J) < 0$) e inestables ($\det(J) > 0, \operatorname{Tr}(J) > 0$), y la geometría de las isoclinas nulas $\dot{x} = 0$ y $\dot{y} = 0$ en el plano de fase.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Confusión de condición de punto silla con inestabilidad general por determinante | conceptual_swap | high | $\text{Un equilibrio con } \det(J) < 0 \text{ es un nodo repulsor inestable donde todas las trayectorias divergen}$ | Un determinante negativo implica autovalores reales de signos opuestos; existe exactamente una trayectoria unidimensional (variedad estable) que converge al equilibrio. |
| `D-C02-02` | Inversión de pendientes de isoclinas nulas en el plano de fase | conceptual_swap | high | $\text{La isoclina } \dot{p} = 0 \text{ indica la tasa de cambio vertical mientras que } \dot{k} = 0 \text{ determina el eje horizontal sin despeje explícito}$ | Cada isoclina nula divide el plano cartesiano en regiones donde la derivada de la variable respectiva es estrictamente positiva o negativa; verifica el signo evaluando a ambos lados de la curva. |
| `D-C02-03` | Identificación errónea de estabilidad asintótica por signo de la traza | conceptual_swap | high | $\text{Si la traza del jacobiano es negativa } (\operatorname{Tr}(J) < 0)\text{, el sistema dinámico es garantizadamente estable}$ | Revisa las condiciones de Routh-Hurwitz para sistemas 2D: la traza negativa es condición necesaria pero no suficiente; si el determinante es negativo, un autovalor es positivo y el sistema es un punto silla. |
| `D-C02-04` | Confusión entre focos espirales y centros conservativos | conceptual_swap | high | $\text{Cualquier sistema con autovalores complejos conjugados genera órbitas periódicas cerradas formando ciclos indefinidos}$ | El discriminante negativo genera componente oscilatoria, pero la estabilidad y la existencia de ciclos cerrados dependen estrictamente de que la parte real (la traza) sea nula. |
| `D-C02-05` | Confusión entre linealización local y validez global del diagrama de fase | conceptual_swap | high | $\text{La matriz jacobiana clasifica la estabilidad del sistema dinámico en todo el espacio de estados no lineal}$ | El análisis local mediante autovalores del jacobiano solo describe la trayectoria cerca del punto de equilibrio; fenómenos globales como cuencas de atracción requieren análisis no lineal global. |
| `D-C02-06` | Mala interpretación de la variedad estable e inestable como ejes coordenados | conceptual_swap | high | $\text{Las trayectorias de ajuste hacia un punto silla coinciden siempre con los ejes coordenados de las variables}$ | Para hallar la rama estable en un sistema lineal o linealizado, encuentra el autovector correspondiente al autovalor negativo; la variedad estable es tangente a la recta generada por dicho autovector. |

---

### [C-03] Fundamentos, Clasificación y Estructura de Solución de Ecuaciones en Derivadas Parciales (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 10: Fundamentos, Clasificación y Estructura de Solución de Ecuaciones en Derivadas Parciales
- **Prerequisites:** None
- **Evidence Citations:** `TEMA 1 (EDP SAÚL) 2.pdf` (page 10)

#### Description & Cognitive Model
Una ecuación en derivadas parciales (EDP) es una relación matemática $F(x_1, \dots, x_n, U, U_{x_1}, \dots, U_{x_n}, \dots) = 0$ que vincula una función incógnita multivariada $U$ con sus derivadas parciales. Se clasifica de acuerdo con su orden (la derivada de mayor orden presente), su grado (el exponente entero de dicha derivada de mayor orden) y su grado de linealidad, distinguiendo ecuaciones lineales de la forma $a(x,y)U_x + b(x,y)U_y + c(x,y)U = d(x,y)$ frente a ecuaciones cuasilineales como $U_y + U U_x = 0$ donde los coeficientes dependen de la función incógnita. A diferencia de las ecuaciones diferenciales ordinarias cuya solución general incorpora constantes escalares arbitrarias, la solución general de una EDP abarca familias infinitas de soluciones parametrizadas mediante funciones arbitrarias continuas $\phi$, como se manifiesta también en la caracterización de funciones homogéneas mediante el Teorema de Euler $\sum_{i=1}^n x_i \frac{\partial f}{\partial x_i} = n f$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Confusión entre el orden y el grado de una ecuación diferencial parcial | conceptual_swap | high | $\text{El orden de una EDP está determinado por la potencia o exponente más alto de sus términos, y el grado es el orden de derivación}$ | Identifica primero la derivada de mayor jerarquía presente (por ejemplo, una segunda derivada $U_{xy}$ tiene orden 2); el exponente de dicha derivada específica define el grado de la ecuación. |
| `D-C03-02` | Confusión entre linealidad y cuasilinealidad por presencia de términos de primer grado | conceptual_swap | high | $\text{Una ecuación de la forma } U_y + U U_x = 0 \text{ es estrictamente lineal porque las derivadas parciales aparecen elevadas a la potencia 1}$ | Para que una EDP sea lineal, los coeficientes de las derivadas parciales y del término en U deben depender exclusivamente de las variables independientes (x, y), sin interactuar multiplicativamente con U. |
| `D-C03-03` | Asimilación errónea de la solución general de una EDP como una familia finita de constantes escalares | conceptual_swap | high | $\text{La solución general de una EDP de primer orden contiene únicamente constantes arbitrarias escalares } c_1, c_2 \in \mathbb{R} \text{ al igual que una EDO}$ | Una EDP modela fenómenos en múltiples dimensiones; por ello, la solución general no se parametriza con simples escalares constantes, sino a través de funciones arbitrarias continuas de las invariantes características. |
| `D-C03-04` | Verificación incompleta o puntual de una solución candidata de EDP | conceptual_swap | high | $\text{Una función } U(x,y) \text{ es solución de la EDP si satisface la ecuación únicamente en puntos particulares del dominio}$ | Para verificar una solución, calcula formalmente sus derivadas parciales y sustitúyelas en la EDP: la igualdad debe cumplirse de manera idéntica en todos los puntos donde la solución esté definida. |
| `D-C03-05` | Confusión sobre el alcance y aplicabilidad del Teorema de Euler | conceptual_swap | high | $\text{La identidad diferencial } \sum_{i=1}^n x_i \frac{\partial f}{\partial x_i} = n f(x) \text{ es aplicable a cualquier función diferenciable general}$ | El teorema de Euler es una caracterización bidireccional exclusiva de funciones homogéneas; corrobora siempre la condición de escala f(tx) = t^n f(x) antes de aplicar la identidad de Euler. |
| `D-C03-06` | Confusión entre grado de homogeneidad y tipos de rendimientos a escala | conceptual_swap | high | $\text{Una función de producción Cobb-Douglas } F(K,L) = A K^\alpha L^\beta \text{ siempre presenta rendimientos constantes a escala sin importar } \alpha \text{ y } \beta$ | El grado de homogeneidad n = alpha + beta gobierna la escala de producción: compara n con la unidad para distinguir rendimientos crecientes, constantes o decrecientes. |

---

### [Hab-05] Resolución de EDPs Cuasilineales de Primer Orden mediante Curvas Características y el Sistema Auxiliar de Lagrange (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 23: Resolución de EDPs Cuasilineales de Primer Orden mediante Curvas Características y el Sistema Auxiliar de Lagrange
- **Prerequisites:** C-05
- **Evidence Citations:** `TEMA 1 (EDP SAÚL) 2.pdf` (page 23)

#### Description & Cognitive Model
Resolver analíticamente ecuaciones en derivadas parciales cuasilineales de primer orden de la forma general $a(x, y) U_x + b(x, y) U_y = c(x, y, U)$ aplicando el método de las curvas características y el sistema auxiliar de Lagrange $\frac{dx}{a(x, y)} = \frac{dy}{b(x, y)} = \frac{dU}{c(x, y, U)}$. El procedimiento analítico comprende: (1) parametrizar la superficie solución mediante curvas características $x(s), y(s), U(s)$ utilizando la regla de la cadena $\frac{dU}{ds} = U_x \frac{dx}{ds} + U_y \frac{dy}{ds}$; (2) formular el sistema simétrico de Lagrange y seleccionar pares de ecuaciones diferenciales ordinarias desacoplables; (3) integrar analíticamente dos EDOs independientes (empleando separación de variables o combinaciones algebraicas de multiplicadores) para aislar dos constantes de integración como integrales primeras independientes $m(x, y, U) = c_1$ y $n(x, y, U) = c_2$; y (4) sintetizar la solución general en su representación implícita $\phi(m, n) = 0$ o explícita despejando la función incógnita $U(x, y)$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Inversión o intercambio erróneo de coeficientes en el sistema auxiliar de Lagrange | conceptual_swap | high | $\text{En la EDP } a U_x + b U_y = c\text{, las razones características asocian derivadas cruzadas: } \frac{dx}{b} = \frac{dy}{a} = \frac{dU}{c}$ | Por la regla de la cadena dU/ds = Ux (dx/ds) + Uy (dy/ds). Al igualar con a Ux + b Uy = c, se deduce directamente dx/ds = a, dy/ds = b y dU/ds = c. |
| `D-Hab05-02` | Dependencia funcional entre las integrales primeras seleccionadas | conceptual_swap | high | $\text{Cualesquiera dos integrales halladas del sistema auxiliar } m(x,y,U)=c_1 \text{ y } n(x,y,U)=c_2 \text{ bastan para la solución general}$ | Verifica que el rango del gradiente o jacobiano de (m, n) respecto a las variables sea igual a 2 para garantizar que una integral primera no sea función redundante de la otra. |
| `D-Hab05-03` | Omisión del término no homogéneo al formular la integral de la función incógnita | skipped_step | high | $\text{La función } U \text{ se deduce integrando exclusivamente las variables espaciales sin acoplar el término fuente } c(x,y,U)$ | El sistema de Lagrange vincula tres razones; para capturar la variación de U debes seleccionar obligatoriamente un par que contenga a dU/c(x,y,U). |
| `D-Hab05-04` | Omisión de la constante de integración al resolver las EDOs características | skipped_step | high | $\text{Al integrar las igualdades de Lagrange se omiten las constantes de integración y se igualan directamente las primitivas evaluadas}$ | Las constantes de integración son las que definen las curvas características invariantes; aísla siempre c1 y c2 para obtener m(x,y,U) y n(x,y,U). |
| `D-Hab05-05` | Uso inválido de multiplicadores de Lagrange con denominador resultante no nulo | conceptual_swap | high | $\text{Al combinar razones } \frac{\alpha dx + \beta dy + \gamma dU}{\alpha a + \beta b + \gamma c}\text{, el numerador se iguala a cero independientemente del denominador}$ | La suma ponderada de diferenciales solo es idénticamente cero si la combinación lineal de los denominadores se anula de forma exacta: alpha*a + beta*b + gamma*c = 0. |
| `D-Hab05-06` | Restricción de la solución general a una constante escalar en vez de una función arbitraria | conceptual_swap | high | $\text{La solución final de la EDP se obtiene igualando una constante a un múltiplo numérico fijo de la otra: } c_2 = k \cdot c_1 \text{ con } k \in \mathbb{R}$ | A diferencia de las EDOs donde las constantes son fijadas por valores numéricos, en EDPs las constantes se relacionan a través de una función arbitraria continua phi(m, n) = 0. |

---

### [C-04] Estructura Matricial y Estabilidad Dinámica de Sistemas Macroeconómicos Lineales (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 5: Estructura Matricial y Estabilidad Dinámica de Sistemas Macroeconómicos Lineales
- **Prerequisites:** None
- **Evidence Citations:** `TEMA 2 (APLICACIONES ECONOMICAS).pdf` (page 5)

#### Description & Cognitive Model
Fundamentación de sistemas diferenciales lineales de primer orden de la forma $\dot{\mathbf{x}}(t) = A\mathbf{x}(t) + \mathbf{b}$ aplicados a modelos macroeconómicos (Inflación-Desempleo e IS-LM dinámica). Caracterización del equilibrio estacionario intertemporal $\mathbf{x}^* = -A^{-1}\mathbf{b}$ y análisis de estabilidad dinámica asintótica mediante el polinomio característico $\det(A - rI) = r^2 - \operatorname{tr}(A)r + \det(A) = 0$, donde la convergencia exige $\operatorname{tr}(A) < 0$ y $\det(A) > 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Confusión entre matriz dinámica de coeficientes y condición de equilibrio estático | conceptual_swap | high | $\text{El equilibrio estacionario requiere que todos los coeficientes de la matriz } A \text{ sean nulos en vez de } \dot{\mathbf{x}} = \mathbf{0}$ | El estado estacionario ocurre cuando las tasas temporales de cambio se anulan, resolviendo el sistema lineal algebraico no homogéneo. |
| `D-C04-02` | Criterio erróneo de signos en la traza para estabilidad asintótica | conceptual_swap | high | $\text{La estabilidad asintótica exige traza positiva } \operatorname{tr}(A) > 0 \text{ para garantizar crecimiento armónico}$ | Las soluciones contienen términos exponenciales $e^{r t}$; si la parte real de las raíces es positiva, las trayectorias divergen explosivamente. |
| `D-C04-03` | Inversión errónea de los multiplicadores de velocidad de ajuste | conceptual_swap | high | $\text{Las constantes de velocidad de ajuste } c_1, c_2 \text{ no alteran la estabilidad del sistema IS-LM dinámico}$ | En el modelo IS-LM dinámica, la matriz del sistema está factorizada por $c_1$ y $c_2$, influyendo en el discriminante $\Delta$ y la naturaleza real o compleja de las raíces. |
| `D-C04-04` | Confusión sobre la naturaleza oscilatoria según el discriminante característico | conceptual_swap | high | $\text{Un discriminante negativo } \Delta < 0 \text{ implica inestabilidad y divergencia del sistema dinámico}$ | El signo del discriminante determina la presencia de componentes trigonométricas periódicas (fluctuaciones), mientras que la parte real determina la convergencia o divergencia. |
| `D-C04-05` | Omisión del término autónomo en el cálculo del equilibrio particular | conceptual_swap | high | $\text{El vector de estado estacionario se calcula como } \mathbf{x}^* = A^{-1}\mathbf{b} \text{ olvidando el signo negativo de la transposición de términos}$ | Al igualar la derivada a cero, el término independiente b pasa al miembro derecho con signo opuesto antes de multiplicar por la inversa. |
| `D-C04-06` | Incompatibilidad dimensional entre expectativas adaptativas y tasa de inflación | conceptual_swap | high | $\text{En el modelo inflación-desempleo, la expectativa } \pi \text{ y la inflación efectiva } p \text{ evolucionan estáticamente sin rezago temporal}$ | Las expectativas adaptativas son un mecanismo dinámico continuo gobernado por un parámetro de velocidad de aprendizaje $0 < j \le 1$. |

---

### [Hab-06] Linealización y Análisis Cualitativo de Sistemas Dinámicos no Lineales en Economía (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 15: Linealización y Análisis Cualitativo de Sistemas Dinámicos no Lineales en Economía
- **Prerequisites:** C-05
- **Evidence Citations:** `TEMA 2 (APLICACIONES ECONOMICAS).pdf` (page 15)

#### Description & Cognitive Model
Procedimiento analítico para linealizar sistemas de ecuaciones diferenciales no lineales autónomos $\dot{x} = f(x, y)$, $\dot{y} = g(x, y)$ (modelos de contaminación acumulada, Lotka-Volterra y ciclos de Goodwin) en torno a sus equilibrios estacionarios $(x^*, y^*)$. Comprende el cálculo analítico de la matriz jacobiana $J(x, y)$, su evaluación en el punto fijo no trivial $J^* = J(x^*, y^*)$, la formulación de la ecuación característica $\det(J^* - \lambda I) = 0$ y la clasificación de la estabilidad local (nodos asintóticamente estables si $\operatorname{Re}(\lambda_i) < 0$ frente a centros conservativos con ciclos cerrados si $\lambda_{1,2} = \pm i\omega$).

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Evaluación del jacobiano fuera del punto de equilibrio estacionario | skipped_step | high | $\text{Se clasifica la estabilidad local evaluando el jacobiano en un punto arbitrario } (x_0, y_0) \text{ sin resolver previamente } \dot{x} = 0 \text{ y } \dot{y} = 0$ | Para aproximar válidamente por serie de Taylor de primer orden, la expansión debe centrarse en un punto crítico donde las derivadas se anulen. |
| `D-Hab06-02` | Omisión del acoplamiento cruzado en las derivadas parciales del jacobiano | skipped_step | high | $\text{Al calcular } J = \begin{bmatrix} \partial \dot{x}/\partial x & \partial \dot{x}/\partial y \\ \partial \dot{y}/\partial x & \partial \dot{y}/\partial y \end{bmatrix}\text{, se ignoran las derivadas cruzadas asumiendo ecuaciones desacopladas}$ | La dinámica del empleo depende de los salarios mediante $-u\delta v$ y la de los salarios del empleo mediante $b u v$, produciendo derivadas cruzadas no nulas. |
| `D-Hab06-03` | Interpretación errónea de autovalores imaginarios puros como punto de silla | skipped_step | high | $\text{Raíces características complejas puras } \lambda = \pm i\omega \text{ representan inestabilidad asimétrica de punto de silla}$ | Un punto de silla se genera por dos autovalores reales de signos opuestos; las raíces puramente imaginarias implican oscilaciones conservativas periódicas. |
| `D-Hab06-04` | Confusión entre estabilidad asintótica y estabilidad marginal u orbital | conceptual_swap | high | $\text{El ciclo de Goodwin y el modelo de Lotka-Volterra convergen asintóticamente al punto estacionario } (x^*, y^*)$ | La convergencia asintótica exige que la parte real sea estrictamente negativa. Con parte real nula, las fluctuaciones de empleo y salario forman ciclos neutros. |
| `D-Hab06-05` | Inversión de los signos en la ecuación característica cuadrática | conceptual_swap | high | $\text{La ecuación característica para una matriz } 2 \times 2 \text{ se formula como } \lambda^2 + \operatorname{tr}(J^*)\lambda - \det(J^*) = 0$ | Al calcular $\det(J^* - \lambda I) = (-\lambda)(-\lambda) - (-\delta v^*)(bu^*)$, el término constante es $+\delta b u^* v^* > 0$, lo que conduce a raíces imaginarias. |
| `D-Hab06-06` | Identificación errónea de puntos de equilibrio trivial y no trivial | conceptual_swap | high | $\text{El único punto de reposo en el modelo de polución acumulada o Goodwin es el origen } (0, 0)$ | En economía, los equilibrios interiores positivos reflejan estados estacionarios viables; el análisis relevante de estabilidad se efectúa en dicho equilibrio no trivial. |

---

### [Hab-07] Resolución de Sistemas Lineales de EDO mediante Autovalores y Autovectores (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 6: Resolución de Sistemas Lineales de EDO mediante Autovalores y Autovectores
- **Prerequisites:** None
- **Evidence Citations:** `TEMA 2 (S'EDOS I ).pdf` (page 6)

#### Description & Cognitive Model
Determinación de la trayectoria temporal de un sistema de EDO lineales homogéneo $\dot{X} = AX$ y no homogéneo $\dot{X} = AX + B$ mediante el cálculo de valores propios $\det(A - \lambda I) = \lambda^2 - \text{tr}(A)\lambda + \det(A) = 0$, vectores propios asociados y la superposición con la solución particular $X_p$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Confusión en la construcción de la solución con autovalores complejos | skipped_step | high | $\text{Creer que con autovalores complejos } \lambda = a \pm bi \text{ la solución omite la parte exponencial } e^{at} \text{ o mezcla incorrectamente senos y cosenos}$ | La parte real del autovalor genera la tasa de crecimiento o amortiguamiento exponencial, mientras que la parte imaginaria produce la oscilación armónica. |
| `D-Hab07-02` | Error en la obtención del autovector generalizado para raíces repetidas | skipped_step | high | $\text{Asumir que para autovalores repetidos } \lambda_1 = \lambda_2 \text{ basta multiplicar la misma solución por } t \text{ sin calcular el vector generalizado } v_2$ | En sistemas lineales acoplados con raíces repetidas, la solución incluye el autovector generalizado $(v_2 + v_1 t)$. |
| `D-Hab07-03` | Inversión errónea del signo en la solución particular de estado estacionario | conceptual_swap | high | $\text{Calcular la solución particular constante como } X_p = A^{-1}B \text{ olvidando el signo negativo al despejar } AX + B = 0$ | Al sustituir una solución constante en $\dot{X} = AX + B$, la derivada se anula, resultando en $AX_p = -B$ y por tanto $X_p = -A^{-1}B$. |
| `D-Hab07-04` | Confusión entre polinomio característico y matriz característica | conceptual_swap | high | $\text{Plantear } p(\lambda) = \det(A - \lambda) = 0 \text{ restando } \lambda \text{ a todas las entradas de la matriz } A$ | El escalar $\lambda$ se multiplica por la matriz identidad $I$, afectando únicamente los elementos de la diagonal principal. |
| `D-Hab07-05` | Omisión del acoplamiento vectorial en la combinación lineal | skipped_step | high | $\text{Asignar constantes independientes a cada variable escalar desacoplando los autovectores en el sistema}$ | Las constantes arbitrarias $c_1$ y $c_2$ multiplican a los vectores propios completos, vinculando de forma unívoca a las variables del sistema. |
| `D-Hab07-06` | Sustitución indebida de condiciones iniciales en la solución complementaria | conceptual_swap | high | $\text{Ajustar las constantes } c_1, c_2 \text{ usando las condiciones iniciales } X(0) \text{ únicamente sobre la parte complementaria } X_h$ | La solución general completa incluye la trayectoria homogénea más la particular; evaluar $t=0$ requiere considerar el valor inicial de ambas. |

---

### [Hab-08] Linealización de Sistemas Dinámicos No Lineales en Puntos de Equilibrio (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 13: Linealización de Sistemas Dinámicos No Lineales en Puntos de Equilibrio
- **Prerequisites:** Hab-09
- **Evidence Citations:** `TEMA 2 (S'EDOS I ).pdf` (page 13)

#### Description & Cognitive Model
Aproximación lineal local de un sistema autónomo no lineal $\dot{x} = f(x, y)$, $\dot{y} = g(x, y)$ alrededor de sus estados estacionarios $(x^*, y^*)$ mediante la evaluación de la matriz jacobiana $J(x^*, y^*)$ y la expansión en serie de Taylor.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Evaluación del Jacobiano fuera del punto de equilibrio | skipped_step | high | $\text{Construir la matriz linealizada utilizando variables dependientes } (x, y) \text{ sin evaluar en el punto de equilibrio } (x^*, y^*)$ | La aproximación lineal describe desviaciones locales y debe tener coeficientes constantes calculados en el punto estacionario. |
| `D-Hab08-02` | Omisión de la condición de equilibrio simultáneo | skipped_step | high | $\text{Identificar equilibrios anulando una sola ecuación o resolviendo } f(x, y) = 0 \text{ e ignorando } g(x, y) = 0$ | En el punto de equilibrio, todas las variables de estado se mantienen constantes simultáneamente ($\dot{x} = 0$ y $\dot{y} = 0$). |
| `D-Hab08-03` | Confusión en la transposición de derivadas cruzadas en el Jacobiano | conceptual_swap | high | $\text{Invertir la posición de las derivadas cruzadas en el Jacobiano, colocando } \frac{\partial g}{\partial x} \text{ en la primera fila}$ | La primera fila contiene el gradiente de la primera ecuación $\dot{x} = f(x,y)$, y la segunda fila el gradiente de $\dot{y} = g(x,y)$. |
| `D-Hab08-04` | Omisión del vector de corrección por origen no centrado | skipped_step | high | $\text{Expresar la versión linealizada en variables absolutas como } \dot{X} = JX \text{ omitiendo el término vectorial } B = -JX^*$ | La expansión de Taylor es en términos de $(x - x^*)$ y $(y - y^*)$; al expandir en variables absolutas aparece el vector constante $B = -JX^*$. |
| `D-Hab08-05` | Tratamiento de sistemas no lineales como desacoplados | conceptual_swap | high | $\text{Tratar el sistema acoplado como ecuaciones autónomas independientes e integrar respecto al tiempo por separado}$ | Las funciones de velocidad $f$ y $g$ acoplan las variables entre sí, impidiendo la integración escalar separada sin considerar la trayectoria del sistema. |
| `D-Hab08-06` | Inclusión errónea del valor residual en el punto de equilibrio | conceptual_swap | high | $\text{Asumir que el término constante de orden cero } f(x^*, y^*) \text{ permanece distinto de cero en el equilibrio}$ | En un punto de equilibrio, el término de orden cero de la serie de Taylor es nulo por definición de estado estacionario. |

---

### [Hab-09] Análisis Cualitativo de Sistemas de EDOs mediante Isoclinas y Diagramas de Fase (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 6: Análisis Cualitativo de Sistemas de EDOs mediante Isoclinas y Diagramas de Fase
- **Prerequisites:** C-05
- **Evidence Citations:** `TEMA 2 (S'EDOS II).pdf` (page 6)

#### Description & Cognitive Model
Construcción del plano de fases y determinación del comportamiento dinámico de un sistema autónomo 2x2 ($\dot{x} = f(x, y)$, $\dot{y} = g(x, y)$) mediante el cálculo analítico de las isoclinas nulas ($f(x, y) = 0$, $g(x, y) = 0$), la localización de los estados estacionarios en sus intersecciones, la determinación de la dirección de los vectores de flujo $(\dot{x}, \dot{y})$ en los cuadrantes delimitados, y la proyección de las trayectorias de solución.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab09-01` | Inversión geométrica de las pendientes asociadas a las isoclinas nulas | conceptual_swap | high | $\dot{x} = 0 \implies \text{trayectorias con pendiente horizontal; } \dot{y} = 0 \implies \text{trayectorias con pendiente vertical}$ | La pendiente de las trayectorias en el espacio de fases es $\frac{dy}{dx} = \frac{\dot{y}}{\dot{x}}$. Cuando $\dot{x} = 0$, la pendiente es vertical, y cuando $\dot{y} = 0$, la pendiente es horizontal. |
| `D-Hab09-02` | Omisión del cálculo conjunto de intersección para puntos de equilibrio | skipped_step | high | $\text{Cualquier punto sobre una sola isoclina } \dot{x} = 0 \text{ o } \dot{y} = 0 \text{ constituye un punto de equilibrio del sistema}$ | Un punto de equilibrio requiere velocidad nula en ambas variables de estado de manera simultánea, lo cual ocurre únicamente en la intersección de ambas isoclinas nulas. |
| `D-Hab09-03` | Inversión del sentido de las flechas de dirección de flujo en los cuadrantes | conceptual_swap | high | $\dot{x} > 0 \implies x(t) \text{ decrece (flecha hacia la izquierda); } \dot{y} > 0 \implies y(t) \text{ decrece (flecha hacia abajo)}$ | Una derivada temporal positiva indica crecimiento de la variable respectiva, por lo que la componente vectorial apunta en la dirección positiva del eje correspondiente. |
| `D-Hab09-04` | Omisión de la evaluación de signos del campo vectorial por regiones | skipped_step | high | $\text{Asumir una orientación uniforme del flujo dinámico en todo el plano de fase sin comprobar los signos en cada cuadrante}$ | Las isoclinas dividen el plano en regiones donde los signos de $\dot{x}$ e $\dot{y}$ se mantienen constantes; se debe evaluar un punto testigo en cada región. |
| `D-Hab09-05` | Confusión entre isoclinas lineales y la linealización jacobiana en sistemas no lineales | conceptual_swap | high | $\text{Sustituir las curvas isoclinas no lineales por rectas tangentes globales para deducir el comportamiento asintótico lejano}$ | La linealización de Taylor solo es válida en una vecindad infinitesimal del estado estacionario; la dinámica global requiere analizar las isoclinas no lineales en todo el plano. |
| `D-Hab09-06` | Omisión de la condición de frontera en la clasificación de trayectorias en torno al punto silla | skipped_step | high | $\text{Cualquier condición inicial converge asintóticamente al punto de silla a lo largo del tiempo}$ | En un punto de silla coexisten direcciones estables e inestables; la convergencia al equilibrio ocurre exclusivamente si la condición inicial se sitúa exactamente sobre la separatriz estable. |

---

### [C-05] Clasificación de Estabilidad de Sistemas de EDOs 2x2 mediante Traza y Determinante (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 8: Clasificación de Estabilidad de Sistemas de EDOs 2x2 mediante Traza y Determinante
- **Prerequisites:** None
- **Evidence Citations:** `TEMA 2 (S'EDOS II).pdf` (page 8)

#### Description & Cognitive Model
En un sistema lineal o linealizado $\dot{X} = AX$, la clasificación topológica y estabilidad local del punto de equilibrio se determinan mediante los invariantes matriciales $\operatorname{tr}(A)$, $\det(A)$ y el discriminante $\Delta = \operatorname{tr}(A)^2 - 4\det(A)$: un punto de silla ocurre si $\det(A) < 0$ ($\lambda_1 > 0 > \lambda_2$); un nodo o foco es asintóticamente estable si $\det(A) > 0$ y $\operatorname{tr}(A) < 0$; es inestable si $\det(A) > 0$ y $\operatorname{tr}(A) > 0$; y es un centro o vórtice neutro si $\det(A) > 0$ y $\operatorname{tr}(A) = 0$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Confusión entre punto de silla e inestabilidad nodal repulsora | conceptual_swap | high | $\det(A) < 0 \implies \text{el punto de equilibrio es un nodo repulsor inestable}$ | Un determinante negativo implica el producto de dos autovalores reales de signos opuestos, lo que define una variedad estable y una variedad inestable típicas del punto de silla. |
| `D-C05-02` | Asumir que traza negativa garantiza estabilidad asintótica sin verificar el determinante | conceptual_swap | high | $\operatorname{tr}(A) < 0 \implies \text{el equilibrio es asintóticamente estable de forma incondicional}$ | Para que ambas partes reales de los autovalores sean estrictamente negativas se requiere tanto traza negativa como determinante estrictamente positivo. |
| `D-C05-03` | Confusión de naturaleza de órbitas por el signo del discriminante | conceptual_swap | high | $\Delta = \operatorname{tr}(A)^2 - 4\det(A) < 0 \implies \text{el sistema posee autovalores reales y trayectorias nodales}$ | Un discriminante negativo bajo el radical de la fórmula cuadrática genera componentes imaginarias, lo que se traduce geométricamente en rotaciones o espirales en el plano de fase. |
| `D-C05-04` | Interpretación errónea de traza nula con determinante positivo como atractor | conceptual_swap | high | $\operatorname{tr}(A) = 0 \land \det(A) > 0 \implies \text{el punto de equilibrio es asintóticamente estable}$ | Una traza nula indica que la parte real del autovalor es cero, generando oscilaciones periódicas concéntricas cerradas sin atracción ni repulsión asintótica. |
| `D-C05-05` | Inversión del criterio de estabilidad según el signo de la traza | conceptual_swap | high | $\operatorname{tr}(A) > 0 \land \det(A) > 0 \implies \text{el equilibrio es un nodo o espiral estable}$ | La traza representa la suma de los autovalores; si el determinante es positivo y la traza es positiva, la parte real de los autovalores es estrictamente positiva, induciendo divergencia. |
| `D-C05-06` | Confusión entre nodo propio e impropio en la frontera crítica del discriminante | conceptual_swap | high | $\Delta = \operatorname{tr}(A)^2 - 4\det(A) = 0 \implies \text{el sistema siempre es un vórtice circular neutro}$ | La anulación del discriminante ocurre en la parábola frontera entre nodos y espirales, lo que representa raíces algebraicas repetidas, mientras que el centro requiere estrictamente traza nula y determinante positivo. |

---
