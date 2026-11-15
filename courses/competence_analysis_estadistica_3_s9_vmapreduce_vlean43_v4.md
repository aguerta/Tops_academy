# Cognitive Task Analysis (CTA): Estadistica 3 S9 Vmapreduce Vlean43 V4

- **Course ID:** `estadistica_3_s9_vmapreduce_vlean43_v4`
- **Macro-Competency:** Dominio y aplicación analítica integral de Estadistica 3 S9 Vmapreduce Vlean43 V4
- **Structure:** 20 total competencies (0 Facts, 13 Concepts, 7 Skills) with 264 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `PRE-01` | Linealidad, Monotonía de la Esperanza y Desigualdad de Jensen | Concept | Understand | Unidad 17: Monotonía y Linealidad de la Esperanza | - | 18 |
| `C-01` | Umbral Muestral y Colas Asintóticas | Concept | Analyze | Unidad 3: Umbral Muestral y Colas Asintóticas | - | 6 |
| `C-02` | Estimadores en Muestras Finitas y Descomposición del ECM | Concept | Understand | Unidad 5: Propiedades de Estimadores en Muestras Finitas | C-01 | 18 |
| `Hab-01` | Momentos, Sesgo, Varianza y Eficiencia de Estimadores | Skill | Apply | Unidad 8: Momentos Exactos de Media y Cuasivarianza Muestral | C-02, PRE-01 | 30 |
| `C-04` | Sucesiones Aleatorias, Convergencia en Probabilidad y Consistencia | Concept | Understand | Unidad 10: Convergencia en Probabilidad y Consistencia Débil | C-01, C-02 | 18 |
| `C-05` | Convergencia en Media r-ésima y Media Cuadrática | Concept | Understand | Unidad 11: Convergencia en Media r-ésima y Media Cuadrática | C-02, C-04 | 12 |
| `Hab-02` | Evaluación de ECM, Tasas de Convergencia y Consistencia | Skill | Apply | Unidad 12: Convergencia Superconsistente del Mínimo Exponencial | C-05, Hab-01 | 24 |
| `C-06` | Desigualdad de Markov y Esperanza Truncada | Concept | Understand | Unidad 14: Desigualdad de Markov y Esperanza Truncada | C-04, PRE-01 | 12 |
| `Hab-03` | Desigualdad de Chebyshev y Demostración de Consistencia | Skill | Apply | Unidad 16: Deducción de Chebyshev Generalizada y Estándar | C-06 | 18 |
| `C-08` | Desigualdad de Cauchy-Schwarz y Correlación | Concept | Understand | Unidad 18: Desigualdad de Cauchy-Schwarz y Correlación | PRE-01 | 6 |
| `C-09` | Modos de Convergencia, Jerarquía y No Reciprocidad | Concept | Understand | Unidad 20: Jerarquía de Convergencias Lr y Probabilidad | PRE-01, C-05, Hab-03 | 30 |
| `Hab-04` | Análisis de Jerarquía, Contraejemplos y Divergencia de Momentos | Skill | Analyze | Unidad 23: Análisis de Plim frente a Divergencia de Momentos | C-09 | 12 |
| `C-11` | Espacio de Probabilidad, Axiomas y Variable Aleatoria | Concept | Understand | Unidad 13: Espacio Muestral, Axiomas de Kolmogorov y Regla de la Unión | - | 12 |
| `C-22` | Ley de los Grandes Números (LGN) | Concept | Understand | Unidad 40: Ley de los Grandes Números (LGN) | C-09, C-11 | 6 |
| `C-23` | Teorema Central del Límite (TCL) | Concept | Understand | Unidad 42: Teorema Central del Límite (TCL) | C-22, C-09 | 6 |
| `Hab-15` | Aproximación Normal, Error Estándar e Intervalos vía TCL | Skill | Apply | Unidad 43: Aproximación Normal de Probabilidades Muestrales | C-23 | 12 |
| `C-24` | Teorema de la Aplicación Continua (CMT) | Concept | Understand | Unidad 46: Teorema de la Aplicación Continua (CMT) | C-22 | 6 |
| `C-25` | Teorema de Slutsky | Concept | Understand | Unidad 48: Teorema de Slutsky | C-22, C-23 | 6 |
| `Hab-17` | Inferencia Asintótica con Varianza Desconocida | Skill | Apply | Unidad 49: Inferencia Asintótica con Varianza Desconocida | C-24, C-25 | 6 |
| `Hab-18` | Método Delta para Error Estándar e Intervalos | Skill | Apply | Unidad 50: Método Delta para Error Estándar e Intervalos | C-23, C-24 | 6 |

---

## Detailed Competency Specifications

### [PRE-01] Linealidad, Monotonía de la Esperanza y Desigualdad de Jensen (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 17: Monotonía y Linealidad de la Esperanza
- **Prerequisites:** None
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 17), `EST3_LEC07_26.2_V2.pdf` (page 25)

#### Description & Cognitive Model
Propiedades estructurales del operador $\mathbb{E}[\cdot]$ (monotonía y linealidad) y Desigualdad de Jensen: para $g$ convexa en $I$, $\mathbb{E}[g(X)] \ge g(\mathbb{E}[X])$, y para $h$ cóncava, $\mathbb{E}[h(X)] \le h(\mathbb{E}[X])$ (vía recta tangente y no conmutatividad con funciones no lineales).

#### Fused Distractor Models (18)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-PRE01-01` | Conmuta con no lineales | conceptual_swap | high | $\mathbb{E}[g(X)]=g(\mathbb{E}[X])$ | La linealidad de la esperanza solo aplica a combinaciones afines $aX+b$, nunca a transformaciones no lineales. |
| `D-PRE01-02` | Linealidad en productos | conceptual_swap | high | $\mathbb{E}[XY]=\mathbb{E}[X]\mathbb{E}[Y]$ | La esperanza del producto iguala al producto de esperanzas solo si $\operatorname{Cov}(X,Y)=0$; en general incluye la covarianza. |
| `D-PRE01-03` | Invierte monotonía | conceptual_swap | high | $U \ge V \Rightarrow \mathbb{E}[U] \le \mathbb{E}[V]$ | El operador esperanza preserva el orden de desigualdades casi seguras sin invertir el signo cuando las variables no se multiplican por negativos. |
| `D-PRE01-04` | Linealidad de varianza | conceptual_swap | high | $\operatorname{Var}(aX+b)=a\operatorname{Var}(X)+b$ | Solo el operador esperanza es lineal respecto a constantes aditivas; la varianza ignora traslaciones $b$ y escala por $a^2$. |
| `D-PRE01-05` | Esperanza aleatoria en recta | conceptual_swap | high | $\mathbb{E}[g'(\mu)X]=g'(X)\mathbb{E}[X]$ | Al evaluar $g'(\mu)$ en la constante determinística $\mu=\mathbb{E}[X]$, sale como factor constante fuera del operador esperanza. |
| `D-PRE01-06` | Monotonía sin acotar | conceptual_swap | high | $U \ge V \text{ solo en un punto}$ | Para concluir $\mathbb{E}[U]\ge\mathbb{E}[V]$ por monotonía, la desigualdad puntual $U\ge V$ debe cumplirse casi seguramente en todo el soporte. |
| `D-PRE01-07` | Invierte signo convexo | conceptual_swap | high | $\mathbb{E}[g(X)] \le g(\mathbb{E}[X])$ | Una función convexa tiene forma de U y queda sobre su tangente, por lo que promediar valores extremos empuja $\mathbb{E}[g(X)]$ por encima de $g(\mathbb{E}[X])$. |
| `D-PRE01-08` | Invierte signo cóncavo | conceptual_swap | high | $\mathbb{E}[h(X)] \ge h(\mathbb{E}[X])$ | Para funciones cóncavas como $h(u)=\sqrt{u}$ ($h''<0$), se cumple $\mathbb{E}[h(X)] \le h(\mathbb{E}[X])$, explicando que $S_n$ subestime a $\sigma$. |
| `D-PRE01-09` | Confunde plim con E | conceptual_swap | high | $\mathbb{E}[1/\bar{Y}_n] = 1/\mathbb{E}[\bar{Y}_n]$ | El operador $\operatorname{plim}$ atraviesa funciones continuas por Teorema de Aplicación Continua, pero $\mathbb{E}[\cdot]$ no conmuta con funciones no lineales en muestras finitas. |
| `D-PRE01-10` | Omite restricción soporte | conceptual_swap | high | $\mathbb{E}[1/X] \ge 1/\mathbb{E}[X]$ en $\mathbb{R}$ | La función $g(x)=1/x$ solo es convexa en el intervalo abierto $(0,\infty)$; verifique siempre que el soporte de $X$ esté contenido en $I$. |
| `D-PRE01-11` | Tangente invertida | conceptual_swap | high | $g(x) \le g(\mu)+g'(\mu)(x-\mu)$ | La caracterización geométrica de una función convexa sitúa la gráfica $g(x)$ siempre por encima o sobre su tangente de soporte en $(\mu,g(\mu))$. |
| `D-PRE01-12` | Igualdad sin linealidad | conceptual_swap | high | $\mathbb{E}[g(X)]=g(\mathbb{E}[X])$ siempre | La igualdad en Jensen para variables no degeneradas solo se garantiza cuando $g(x)=ax+b$ es afín; con curvatura estricta la desigualdad es estricta. |
| `D-PRE01-13` | Linealidad falsa | conceptual_swap | high | $E[g(X)] = g(E[X])$ para toda función $g$ | Recuerde que la esperanza solo conmuta con funciones lineales; en funciones no lineales aparece un sesgo dado por la curvatura. |
| `D-PRE01-14` | Invierte convexa | conceptual_swap | high | Si $g$ es convexa entonces $E[g(X)] \le g(E[X])$ | Verifique la dirección usando $g(x)=x^2$: como $\mathrm{Var}(X)=E[X^2]-(E[X])^2 \ge 0$, para funciones convexas siempre vale $E[g(X)] \ge g(E[X])$. |
| `D-PRE01-15` | Invierte cóncava | conceptual_swap | high | Si $h$ es cóncava entonces $E[h(X)] \ge h(E[X])$ | Recuerde que $\sqrt{\cdot}$ es cóncava, por lo que Jensen implica $E[s] = E[\sqrt{s^2}] \le \sqrt{E[s^2]} = \sigma$. |
| `D-PRE01-16` | Insesgadez transferida | conceptual_swap | high | Si $s^2$ es insesgado para $\sigma^2$, entonces $s$ es insesgado para $\sigma$ | Distinga estimadores de varianza y de desviación estándar: la raíz cuadrada cóncava rompe la insesgadez en muestras finitas. |
| `D-PRE01-17` | Confunde con plim | conceptual_swap | high | Ni la esperanza ni el $\mathrm{plim}$ pasan por funciones no lineales | Separe esperanza finita de límite en probabilidad: aunque $E[g(X)] \neq g(E[X])$, las funciones continuas sí preservan el $\mathrm{plim}$. |
| `D-PRE01-18` | Solo variables positivas | conceptual_swap | high | Jensen exige $X > 0$ incluso para $g(x) = x^2$ | Compruebe solo que $g$ sea convexa o cóncava en el dominio de $X$ y que $E[X]$ y $E[g(X)]$ existan. |

#### Formal Mathematical Assumptions (4)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-PRE01-01` | - | Existencia de esperanzas finitas $\mathbb{E}[|U|]<\infty$ y $\mathbb{E}[|V|]<\infty$ | Sin integrabilidad absoluta los operadores de esperanza pueden quedar indeterminados. | - |
| `A-PRE01-02` | - | Esperanzas finitas $\mathbb{E}[|X|]<\infty$ y $\mathbb{E}[|g(X)|]<\infty$ con soporte en $I$ | Sin soporte en $I$ y momentos finitos no existe la recta de soporte integrable. | - |
| `A-PRE01-03` | - | Convexidad de $g$ o concavidad de $h$ sobre el soporte de $X$ | Si la función cambia de curvatura dentro del soporte, el sentido de la desigualdad de Jensen es indeterminado. | - |
| `A-PRE01-04` | - | Existencia de las esperanzas $E[X]$ y $E[g(X)]$ | Sin integrabilidad de $X$ y $g(X)$, los términos de la desigualdad no están bien definidos. | - |

---

### [C-01] Umbral Muestral y Colas Asintóticas (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 3: Umbral Muestral y Colas Asintóticas
- **Prerequisites:** None
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 3)

#### Description & Cognitive Model
Evaluación del umbral muestral para aproximación normal según asimetría, curtosis leptocúrtica y precisión en las colas críticas al nivel de significancia $\alpha$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Regla fija n>=30 | conceptual_swap | high | $n \ge 30$ basta universalmente para el TCL | Recuerde que la velocidad de convergencia depende de asimetría y curtosis poblacionales, no de un umbral fijo. |
| `D-C01-02` | Centro igual colas | conceptual_swap | high | Convergencia en el centro garantiza colas precisas | Distinga centro y colas: el TCL aproxima rápido cerca de $\mu$, pero falla en colas extremas con datos asimétricos. |
| `D-C01-03` | Ignora leptocurtosis | conceptual_swap | high | Valores atípicos no afectan velocidad asintótica | Considere el cuarto momento estandarizado: la curtosis alta y outliers desaceleran la cancelación en la expansión. |
| `D-C01-04` | Confunde normalidad | conceptual_swap | high | Teoría asintótica exige errores $\varepsilon_i \sim \mathcal{N}(0,\sigma^2)$ | Separe muestras finitas de asintótica: la teoría asintótica prescinde de normalidad exacta del PGD cuando $n \to \infty$. |
| `D-C01-05` | Omite nivel alfa | conceptual_swap | high | El nivel $\alpha$ no modifica el $n^*$ requerido | Note que exigencias más estrictas en colas (menor $\alpha$) aumentan la discrepancia relativa y requieren mayor $n^*$. |
| `D-C01-06` | Error Tipo II | conceptual_swap | high | Mala aproximación en colas solo afecta potencia | Verifique que errores en la cola crítica alteran directamente la probabilidad de rechazo bajo $H_0$ (error Tipo I). |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Existencia de momentos poblacionales finitos (asimetría y curtosis) | Sin momentos de orden superior finitos, la tasa de aproximación normal puede colapsar. | - |

---

### [C-02] Estimadores en Muestras Finitas y Descomposición del ECM (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 5: Propiedades de Estimadores en Muestras Finitas
- **Prerequisites:** C-01
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 5), `EST3_LEC07_26.2_V2.pdf` (page 3)

#### Description & Cognitive Model
Muestra aleatoria i.i.d. $Y_1,\dots,Y_n \sim F_Y$, estadístico frente a estimador $\hat{\theta}_n$ y estimación puntual, sesgo e insesgadez exacta $\mathbb{E}[\hat{\theta}_n]=\theta$, eficiencia relativa escalar y matricial $\Delta \succeq 0$, y descomposición $\mathrm{ECM}(\hat{\theta}_n) = \mathrm{Var}(\hat{\theta}_n) + [\mathrm{Sesgo}(\hat{\theta}_n)]^2$ con dilema sesgo-varianza.

#### Fused Distractor Models (18)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Estimador vs punto | conceptual_swap | high | Un estimador $\hat{\theta}_n$ es un número real fijo | Diferencie estimador (variable aleatoria con distribución muestral) de estimación puntual (realización numérica). |
| `D-C02-02` | Estadístico paramétrico | conceptual_swap | high | Un estadístico puede depender de $\theta$ desconocido | Verifique que un estadístico $T(Y_1,\dots,Y_n)$ es función observable libre de parámetros poblacionales desconocidos. |
| `D-C02-03` | Eficiencia sin sesgo | conceptual_swap | high | Menor varianza implica eficiencia aunque haya sesgo | Recuerde que la eficiencia relativa pura compara únicamente estimadores insesgados; con sesgo se usa el ECM. |
| `D-C02-04` | Orden matriz inverso | conceptual_swap | high | $\hat{\theta}_1$ más eficiente si $\mathrm{Var}(\hat{\theta}_1)-\mathrm{Var}(\hat{\theta}_2)\succeq 0$ | Corrija el signo de la diferencia: $\hat{\theta}_1$ es más eficiente cuando $\mathrm{Var}(\hat{\theta}_2)-\mathrm{Var}(\hat{\theta}_1)\succeq 0$. |
| `D-C02-05` | Elemento a elemento | conceptual_swap | high | Matriz semidefinida positiva equivale a entradas $\ge 0$ | Exija que la forma cuadrática $\mathbf{c}^\top \Delta \mathbf{c} \ge 0$ se cumpla para todo vector no nulo $\mathbf{c} \in \mathbb{R}^k$. |
| `D-C02-06` | Independencia parcial | conceptual_swap | high | Muestra i.i.d. solo pide igual media y varianza | Recuerde que i.i.d. exige independencia conjunta e idéntica función de distribución acumulada marginal $F_Y(y)$. |
| `D-C02-07` | Sesgo sin cuadrado | conceptual_swap | high | $\mathrm{ECM}(\hat{\theta}_n) = \mathrm{Var}(\hat{\theta}_n) + \mathrm{Sesgo}(\hat{\theta}_n)$ | Eleve al cuadrado el sesgo: $\mathrm{ECM}$ promedia distancias cuadráticas y no permite cancelación de signos. |
| `D-C02-08` | Término cruzado vivo | conceptual_swap | high | Queda un término $2\,\mathrm{Sesgo}\,\mathbb{E}[\hat{\theta}_n - \mathbb{E}[\hat{\theta}_n]] \neq 0$ | Aplique linealidad de la esperanza: $\mathbb{E}[\hat{\theta}_n - \mathbb{E}[\hat{\theta}_n]] = 0$, anulando el término cruzado. |
| `D-C02-09` | Insesgado siempre óptimo | conceptual_swap | high | Ningún estimador sesgado tiene menor ECM que uno insesgado | Evalúe el dilema sesgo-varianza: un sesgo pequeño con gran reducción de varianza disminuye el ECM total. |
| `D-C02-10` | Transpuesta incorrecta | conceptual_swap | high | En $\mathbb{R}^k$, matriz ECM usa $\mathrm{Sesgo}^\top \mathrm{Sesgo}$ | Verifique dimensiones matriciales: el producto externo $\mathrm{Sesgo}(\hat{\theta}_n)\mathrm{Sesgo}(\hat{\theta}_n)^\top$ produce dimensión $k\times k$. |
| `D-C02-11` | Resta en lugar suma | conceptual_swap | high | $\mathrm{ECM}(\hat{\theta}_n) = \mathrm{Var}(\hat{\theta}_n) - [\mathrm{Sesgo}(\hat{\theta}_n)]^2$ | Recuerde que ambos sumandos son no negativos y penalizan aditivamente el error cuadrático esperado alrededor de $\theta$. |
| `D-C02-12` | Cero con sesgo fijo | conceptual_swap | high | $\mathrm{ECM} \to 0$ aunque el sesgo sea constante no nulo | Note que como ambos términos son $\ge 0$, $\mathrm{ECM}\to 0$ exige que varianza y sesgo tiendan a cero juntos. |
| `D-C02-13` | Confusión estimador y estimación | conceptual_swap | high | $\hat{\theta}_n$ es un número fijo | Distinga el estimador $\bar{Y}$ (fórmula aleatoria que cambia entre muestras) de la estimación $\bar{y}=1800$ (número observado). |
| `D-C02-14` | Confusión parámetro con estimador | conceptual_swap | high | $\mu=\bar{Y}$ | Separe el parámetro $\theta$ (constante desconocida de la población) del estimador $\hat{\theta}_n$ (variable aleatoria muestral). |
| `D-C02-15` | Interpretación parcial de i.i.d. | conceptual_swap | high | i.i.d. significa solo independencia | Verifique ambas condiciones de i.i.d.: independencia mutua entre observaciones e idéntica distribución común $F_Y$. |
| `D-C02-16` | Ignora dependencia del tamaño $n$ | conceptual_swap | high | $\hat{\theta}_n$ es invariante con $n$ | Considere el subíndice $n$: al aumentar el tamaño muestral cambia el estimador $\hat{\theta}_n$ y se concentra su distribución. |
| `D-C02-17` | Estimación igual al valor poblacional | conceptual_swap | high | $\bar{y}=\mu$ exactamente | Recuerde que una estimación concreta aproxima $\theta$ con error muestral; otra muestra produciría un valor distinto. |
| `D-C02-18` | Confusión muestra con población | conceptual_swap | high | $F_Y$ es la muestra observada | Diferencie la población gobernada por $F_Y$ de la muestra aleatoria $Y_1,\dots,Y_n$ extraída de dicha población. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | Segundo momento finito $\mathbb{E}[\hat{\theta}_n^2] < \infty$ (o matriz de covarianzas finita) | Sin segundo momento finito no existen varianza ni eficiencia relativa. | - |
| `A-C02-02` | - | Existencia de segundo momento $\mathbb{E}[\hat{\theta}_n^2] < \infty$ y linealidad de $\mathbb{E}[\cdot]$ | Garantiza la separación algebraica exacta entre varianza y sesgo cuadrado. | - |
| `A-C02-03` | - | Las observaciones $Y_1,\dots,Y_n$ son independientes e idénticamente distribuidas según $F_Y$ | Garantiza simetría muestral y evita correlaciones entre unidades. | - |

---

### [Hab-01] Momentos, Sesgo, Varianza y Eficiencia de Estimadores (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 8: Momentos Exactos de Media y Cuasivarianza Muestral
- **Prerequisites:** C-02, PRE-01
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 8), `EST3_LEC07_26.2_V2.pdf` (page 17), `EST3_LEC07_26.2_V2.pdf` (page 5), `EST3_LEC07_26.2_V2.pdf` (page 7), `EST3_LEC07_26.2_V2.pdf` (page 11)

#### Description & Cognitive Model
Cálculo de esperanza $\mathbb{E}[X]$ y varianza $\mathrm{Var}(X)$, derivación sin normalidad de $\mathbb{E}[\bar{Y}_n]=\mu$, $\mathrm{Var}(\bar{Y}_n)=\sigma^2/n$, $\mathbb{E}[S_n^2]=\sigma^2$ y sesgo $-\sigma^2/n$ de $m_2$, y evaluación analítica de sesgo, insesgadez, error estándar y eficiencia relativa entre estimadores.

#### Fused Distractor Models (30)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Varianza sin 1/n | skipped_step | high | $\mathrm{Var}(\bar{Y}_n) = \sigma^2$ o $\frac{\sigma^2}{n^2}$ | Sume las $n$ varianzas individuales después de extraer $(1/n)^2$: $n\sigma^2/n^2 = \sigma^2/n$. |
| `D-Hab01-02` | Covarianza no nula | conceptual_swap | high | Incluye covarianzas cruzadas en muestra i.i.d. | Use la independencia mutua de la muestra i.i.d.: todas las covarianzas cruzadas $\mathrm{Cov}(Y_i,Y_j)$ son cero. |
| `D-Hab01-03` | Signo positivo en (4) | skipped_step | high | $\sum (Y_i-\bar{Y}_n)^2 = \sum (Y_i-\mu)^2 + n(\bar{Y}_n-\mu)^2$ | Revise el término cruzado $-2(\bar{Y}_n-\mu)\cdot n(\bar{Y}_n-\mu)$: al sumarlo con $+n(\bar{Y}_n-\mu)^2$ queda signo negativo. |
| `D-Hab01-04` | Confunde mu con Ybar | conceptual_swap | high | $\mathbb{E}[(Y_i-\bar{Y}_n)^2] = \mathrm{Var}(Y_i) = \sigma^2$ | Distinga dispersión respecto a $\mu$ ($\sigma^2$) de dispersión respecto a $\bar{Y}_n$, que pierde un grado de libertad. |
| `D-Hab01-05` | Grado libertad extra | conceptual_swap | high | $m_2$ tiene sesgo positivo $+\sigma^2/n$ | Recuerde que $\bar{Y}_n$ minimiza $\sum(Y_i-c)^2$, haciendo la dispersión observada menor y generando sesgo $-\sigma^2/n$. |
| `D-Hab01-06` | Requiere normalidad | conceptual_swap | high | $\mathbb{E}[S_n^2] = \sigma^2$ requiere $Y_i \sim \mathcal{N}(\mu,\sigma^2)$ | Observe que la prueba usa solo independencia, igual distribución y $\sigma^2<\infty$, sin asumir normalidad. |
| `D-Hab01-07` | Promedio simple sin ponderar | skipped_step | high | $E[X]=\frac{1}{k}\sum x_j$ | Pondere cada valor posible $x$ por su probabilidad $P(X=x)$ en lugar de dividir simplemente entre la cantidad de valores. |
| `D-Hab01-08` | Confunde $E[X^2]$ con $(E[X])^2$ | skipped_step | high | $\mathrm{Var}(X)=E[X^2]-E[X]$ | Eleve al cuadrado la esperanza $E[X]$ antes de restarla de $E[X^2]$, pues $\mathrm{Var}(X)=E[X^2]-(E[X])^2$. |
| `D-Hab01-09` | Olvida elevar desvíos al cuadrado | conceptual_swap | high | $\mathrm{Var}(X)=E[X-E[X]]$ | Eleve al cuadrado cada desvío $(x-E[X])^2$ antes de ponderar por $P(X=x)$; sin cuadrado las desviaciones se cancelan. |
| `D-Hab01-10` | Confunde varianza con desviación estándar | conceptual_swap | high | $\sigma=\mathrm{Var}(X)$ | Extraiga la raíz cuadrada $\sigma=\sqrt{\mathrm{Var}(X)}$ para expresar la dispersión en las mismas unidades que $X$. |
| `D-Hab01-11` | Suma $E[X^2]+(E[X])^2$ | conceptual_swap | high | $\mathrm{Var}(X)=E[X^2]+(E[X])^2$ | Reste $(E[X])^2$ de $E[X^2]$ tras expandir $E[(X-E[X])^2]$; sumar viola la no negatividad centrada. |
| `D-Hab01-12` | Aplica $(E[X])^2$ en vez de $E[X^2]$ | conceptual_swap | high | $E[X^2]=(E[X])^2$ | Calcule $E[X^2]=\sum_x x^2 P(X=x)$ primero; elevar cada $x$ antes de promediar difiere de elevar el promedio. |
| `D-Hab01-13` | Signo invertido del sesgo | skipped_step | high | $\mathrm{Sesgo}(\hat{\theta})=\theta-E[\hat{\theta}]$ | Reste $\theta$ a $E[\hat{\theta}]$: un estimador que subestima en promedio tiene $\mathrm{Sesgo}(\hat{\theta})=E[\hat{\theta}]-\theta<0$. |
| `D-Hab01-14` | Confunde estimación puntual con sesgo | skipped_step | high | $\mathrm{Sesgo}(\hat{\theta})=\hat{\theta}-\theta$ | Evalúe la esperanza $E[\hat{\theta}]$ sobre muestras repetidas; una realización alejada de $\theta$ no implica sesgo. |
| `D-Hab01-15` | Omite factor $1/n$ en esperanza de suma | conceptual_swap | high | $E[\bar{Y}]=n\mu$ | Factorice $1/n$ por linealidad de la esperanza: $E[\bar{Y}]=\frac{1}{n}\sum_{i=1}^n E[Y_i]=\frac{1}{n}(n\mu)=\mu$. |
| `D-Hab01-16` | Asume insesgado cualquier múltiplo de $\bar{Y}$ | conceptual_swap | high | $E[c\bar{Y}]=\mu$ | Aplique homogeneidad $E[c\bar{Y}]=cE[\bar{Y}]=c\mu$, por lo que $\mathrm{Sesgo}(c\bar{Y})=(c-1)\mu$ solo es cero si $c=1$. |
| `D-Hab01-17` | Confunde insesgadez con varianza cero | conceptual_swap | high | $E[\hat{\theta}]=\theta \Rightarrow \hat{\theta}=\theta$ | Separe exactitud promedio ($E[\hat{\theta}]=\theta$) de precisión muestra a muestra, la cual depende de $\mathrm{Var}(\hat{\theta})$. |
| `D-Hab01-18` | Evalúa sesgo con razón en vez de resta | conceptual_swap | high | $\mathrm{Sesgo}(\hat{\theta})=E[\hat{\theta}]/\theta$ | Exprese el sesgo como diferencia aditiva $E[\hat{\theta}]-\theta$, de modo que insesgadez equivale a sesgo igual a cero. |
| `D-Hab01-19` | No eleva al cuadrado la constante $1/n$ | skipped_step | high | $\mathrm{Var}(\bar{Y})=\frac{1}{n}\sum \mathrm{Var}(Y_i)=\sigma^2$ | Use $\mathrm{Var}(aZ)=a^2\mathrm{Var}(Z)$: al sacar $1/n$ de la varianza queda $\frac{1}{n^2}(n\sigma^2)=\frac{\sigma^2}{n}$. |
| `D-Hab01-20` | Confunde varianza con error estándar | skipped_step | high | $\mathrm{ee}(\bar{Y})=\sigma^2/n$ | Tome la raíz cuadrada $\mathrm{ee}(\hat{\theta})=\sqrt{\mathrm{Var}(\hat{\theta})}$ para volver a las unidades originales de $\theta$. |
| `D-Hab01-21` | Divide error estándar entre $n$ | conceptual_swap | high | $\mathrm{ee}(\bar{Y})=\sigma/n$ | Divida $\sigma$ entre $\sqrt{n}$, no entre $n$, porque el error estándar es $\sqrt{\sigma^2/n}=\sigma/\sqrt{n}$. |
| `D-Hab01-22` | Compara eficiencia ignorando sesgo | conceptual_swap | high | Menor varianza implica mayor eficiencia siempre | Aplique el criterio de eficiencia relativa solo entre estimadores insesgados; con sesgo se compara mediante ECM. |
| `D-Hab01-23` | Confunde menor varianza con menor eficiencia | conceptual_swap | high | $\mathrm{Var}(\hat{\theta}_1)>\mathrm{Var}(\hat{\theta}_2)\Rightarrow \hat{\theta}_1$ más eficiente | Recuerde que menor varianza significa estimaciones más concentradas alrededor del parámetro y, por tanto, mayor eficiencia. |
| `D-Hab01-24` | Ignora covarianzas si hubiera dependencia | conceptual_swap | high | $\mathrm{Var}(\sum Y_i)=\sum \mathrm{Var}(Y_i)$ siempre | Verifique independencia muestral antes de omitir términos de covarianza en la varianza de una suma aleatoria. |
| `D-Hab01-25` | Divide cuasivarianza entre $n$ creyéndola insesgada | skipped_step | high | $E[m_2]=\sigma^2$ | Divida entre $n-1$ al estimar $\sigma^2$ porque estimar $\mu$ con $\bar{Y}$ consume un grado de libertad y achica los desvíos. |
| `D-Hab01-26` | Resta media poblacional desconocida | conceptual_swap | high | $s^2=\frac{1}{n-1}\sum (Y_i-\mu)^2$ | Note que $n-1$ corrige la subestimación causada al centrar en $\bar{Y}$; con $\mu$ conocida se dividiría entre $n$. |
| `D-Hab01-27` | Olvida elevar desvíos muestrales al cuadrado | skipped_step | high | $s^2=\frac{1}{n-1}\sum (Y_i-\bar{Y})$ | Eleve al cuadrado cada desvío $(Y_i-\bar{Y})^2$ antes de sumar; la suma lineal de desvíos respecto a $\bar{Y}$ siempre es cero. |
| `D-Hab01-28` | Confunde sesgo de $m_2$ con insesgadez exacta | conceptual_swap | high | $m_2$ tiene sesgo nulo para $n$ finito | Recuerde que $E[m_2]=\frac{n-1}{n}\sigma^2$ implica sesgo $-\sigma^2/n$; el sesgo desaparece solo asintóticamente cuando $n\to\infty$. |
| `D-Hab01-29` | Multiplica por $(n-1)/n$ sobre $s^2$ erróneamente | conceptual_swap | high | $E[s^2]=\frac{n-1}{n}\sigma^2$ | Verifique que $s^2$ ya incorpora la corrección $1/(n-1)$, de modo que $E[s^2]=\sigma^2$ exactamente para todo $n\ge 2$. |
| `D-Hab01-30` | Usa $n-1$ también en la media $\bar{Y}$ | conceptual_swap | high | $\bar{Y}=\frac{1}{n-1}\sum Y_i$ | Divida la media muestral $\bar{Y}$ entre $n$; la corrección $n-1$ aplica solo a la suma de cuadrados en $s^2$. |

#### Formal Mathematical Assumptions (5)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Muestra aleatoria simple i.i.d. con $n \ge 2$, $\mathbb{E}[Y_i]=\mu<\infty$ y $\mathrm{Var}(Y_i)=\sigma^2<\infty$ | Sin $n\ge 2$ y momentos finitos, $S_n^2$ no está definido o carece de esperanza finita. | - |
| `A-Hab01-02` | - | Existen el primer y segundo momento finito, es decir $E[X^2]<\infty$ | Sin segundo momento finito la varianza diverge y no está definida. | - |
| `A-Hab01-03` | - | Cada observación $Y_i$ posee esperanza finita $E[Y_i]=\mu$ y se aplica linealidad de la esperanza | Permite calcular $E[\bar{Y}]=\mu$ sin requerir independencia. | - |
| `A-Hab01-04` | - | Las observaciones $Y_1,\dots,Y_n$ son independientes con varianza finita común $\sigma^2$ | Anula las covarianzas cruzadas y produce $\mathrm{Var}(\bar{Y})=\sigma^2/n$. | - |
| `A-Hab01-05` | - | El tamaño muestral satisface $n\ge 2$ con observaciones i.i.d. de varianza $\sigma^2<\infty$ | Sin $n\ge 2$ el denominador $n-1$ de la cuasivarianza se anula. | - |

---

### [C-04] Sucesiones Aleatorias, Convergencia en Probabilidad y Consistencia (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 10: Convergencia en Probabilidad y Consistencia Débil
- **Prerequisites:** C-01, C-02
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 10), `EST3_LEC07_26.2_V2.pdf` (page 19), `EST3_LEC07_26.2_V2.pdf` (page 27)

#### Description & Cognitive Model
Sucesión ordenada $\{X_n\}_{n=1}^\infty$ de estimadores según tamaño muestral, estabilización asintótica y convergencia en probabilidad $X_n \xrightarrow{p} c \Leftrightarrow \lim_{n\to\infty} P(|X_n - c| > \varepsilon) = 0 \;\forall \varepsilon > 0$ ($\mathrm{plim}\,\hat{\theta}_n = \theta$) como definición de consistencia débil.

#### Fused Distractor Models (18)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Límite determinístico | conceptual_swap | high | $X_n \xrightarrow{p} c$ equivale a límite real $|X_n-c|<\varepsilon$ | Recuerde que cada $X_n$ es variable aleatoria con distribución $F_{X_n}$; debe evaluar $\mathbb{P}(|X_n-c|>\varepsilon)\to 0$. |
| `D-C04-02` | Probabilidad cero | conceptual_swap | high | $\lim_{n\to\infty}\mathbb{P}(|X_n-c|\le \varepsilon) = 0$ | Invierta el evento correctamente: la probabilidad dentro de la banda $[c-\varepsilon,c+\varepsilon]$ debe tender a $1$, no a $0$. |
| `D-C04-03` | Epsilon fijo | conceptual_swap | high | Basta verificar el límite para un único $\varepsilon_0 > 0$ | Exija el cuantificador universal $\forall \varepsilon > 0$: la cola fuera de cualquier banda arbitraria debe anularse. |
| `D-C04-04` | Colapso hacia X | conceptual_swap | high | Si $X_n \xrightarrow{p} X$, la distribución de $X_n$ colapsa a un punto | Distinga límite constante de variable aleatoria: hacia $X$, las realizaciones $X_n(\omega)$ y $X(\omega)$ se acercan entre sí. |
| `D-C04-05` | Consistencia puntual | conceptual_swap | high | Consistencia solo requiere $\hat{\theta}_n \xrightarrow{p} \theta_0$ en un punto | Verifique que el estimador debe converger en probabilidad a $\theta$ para todo valor posible en el espacio paramétrico $\Theta$. |
| `D-C04-06` | Insesgado es consistente | conceptual_swap | high | Todo estimador insesgado es automáticamente consistente | Note que insesgadez controla solo el centro esperado; sin colapso de dispersión la masa no se concentra en $\theta$. |
| `D-C04-07` | Confunde término con sucesión | conceptual_swap | high | $X_n=\{X_n\}_{n=1}^\infty$ | Distinga un término particular $X_n$ (para un $n$ fijo) de toda la lista ordenada $\{X_n\}_{n=1}^\infty$ indexada por $n$. |
| `D-C04-08` | Trata sucesión aleatoria como determinística | conceptual_swap | high | $\lim_{n\to\infty} X_n$ es igual que en reales | Recuerde que cada $X_n$ es una variable aleatoria, por lo que converger admite distintos sentidos probabilísticos. |
| `D-C04-09` | Peso constante de cada observación nueva | conceptual_swap | high | Cada dato nuevo pesa igual sin importar $n$ | Note que cada nueva observación pesa $1/n$ en el promedio $\bar{Y}_n$, por lo que las fluctuaciones se atenúan al crecer $n$. |
| `D-C04-10` | Confunde tamaño $n$ con valor observado | conceptual_swap | high | $n$ es el valor de $Y_i$ | Identifique $n$ como el tamaño muestral creciente $1,2,3,\dots$ que indexa la sucesión de estimadores. |
| `D-C04-11` | Cree que muestra pequeña basta para estabilizar | conceptual_swap | high | $\bar{Y}_5=\mu$ por estabilización | Interprete $n\to\infty$ como comportamiento asintótico al acumular indefinidamente datos, no como igualdad en $n$ pequeño. |
| `D-C04-12` | Asume suma acumulada en vez de promedio | conceptual_swap | high | $X_n=\sum_{i=1}^n Y_i$ | Divida la suma acumulada entre $n$ para formar $\bar{Y}_n=\frac{1}{n}\sum_{i=1}^n Y_i$ si busca estabilización en $\mu$. |
| `D-C04-13` | Límite determinista | conceptual_swap | high | $X_n \xrightarrow{p} c$ significa que $|X_n - c| = 0$ para $n$ finito | Comprenda que $X_n$ sigue siendo aleatorio; lo que tiende a cero al crecer $n$ es la probabilidad de superar cualquier margen $\epsilon > 0$. |
| `D-C04-14` | Solo un epsilon | conceptual_swap | high | Basta que $P(|X_n - c| > 1) \to 0$ para tener consistencia | Exija que el límite se cumpla para todo $\epsilon > 0$, por pequeño que sea, para garantizar concentración total en $c$. |
| `D-C04-15` | Invierte desigualdad | conceptual_swap | high | $X_n \xrightarrow{p} c \Leftrightarrow \lim_{n\to\infty} P(|X_n - c| \le \epsilon) = 0$ | Distinga evento de éxito y error: la probabilidad de quedar dentro de $c \pm \epsilon$ debe tender a $1$, y la de salir fuera a $0$. |
| `D-C04-16` | Confunde con esperanza | conceptual_swap | high | $X_n \xrightarrow{p} c \Leftrightarrow E[X_n] = c$ | Separe el centro promedio para $n$ fijo de la concentración asintótica de toda la distribución alrededor del parámetro $c$. |
| `D-C04-17` | Casi segura disfrazada | conceptual_swap | high | $X_n \xrightarrow{p} c$ significa que la trayectoria nunca vuelve a salir de $c \pm \epsilon$ | Note que $\xrightarrow{p}$ evalúa cada $n$ grande por separado; impedir desviaciones infinitas de la trayectoria corresponde a $\xrightarrow{a.s.}$. |
| `D-C04-18` | Consistencia de parámetro | conceptual_swap | high | Un estimador es consistente si su varianza es menor que $1$ | Verifique que el estimador converja en probabilidad al parámetro verdadero conforme $n \to \infty$. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Sucesión $\{X_n\}$ y límite $X$ definidos sobre el mismo espacio de probabilidad $(\Omega,\mathcal{F},\mathbb{P})$ | Sin espacio común no puede definirse la diferencia medible $X_n - X$. | - |
| `A-C04-02` | - | La sucesión $\{X_n\}_{n=1}^\infty$ se define sobre un espacio de probabilidad común cuando $n\to\infty$ | Permite analizar el comportamiento límite de los estimadores. | - |
| `A-C04-03` | - | Sucesión de variables aleatorias $\{X_n\}_{n \ge 1}$ definida sobre un espacio de probabilidad común | Sin una sucesión indexada por el tamaño muestral $n$, no tiene sentido tomar el límite $n \to \infty$. | - |

---

### [C-05] Convergencia en Media r-ésima y Media Cuadrática (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 11: Convergencia en Media r-ésima y Media Cuadrática
- **Prerequisites:** C-02, C-04
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 11), `EST3_LEC07_26.2_V2.pdf` (page 29)

#### Description & Cognitive Model
Convergencia en norma $L^r$ ($\lim_{n\to\infty}\mathbb{E}[|X_n-X|^r]=0$) y criterio necesario y suficiente para $X_n \xrightarrow{\mathrm{m.s.}} c \Leftrightarrow \mathbb{E}[(X_n-c)^2]\to 0$: insesgadez asintótica ($\mathrm{Sesgo}\to 0$) y colapso de varianza ($\mathrm{Var}(X_n)\to 0$), implicando $X_n \xrightarrow{p} c$.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Solo varianza cero | conceptual_swap | high | $\mathrm{Var}(X_n)\to 0$ basta para $X_n \xrightarrow{\mathrm{m.s.}} c$ | Use la descomposición del ECM: si $\mathrm{Var}(X_n)\to 0$ pero el sesgo no tiende a $0$, converge a otro punto, no a $c$. |
| `D-C05-02` | Solo sesgo asintótico | conceptual_swap | high | $\mathbb{E}[X_n]\to c$ basta para convergencia en media cuadrática | Exija simultáneamente $\lim_{n\to\infty}\mathrm{Var}(X_n)=0$; sin ello el segundo término $\mathrm{Var}(X_n)$ mantiene positivo el ECM. |
| `D-C05-03` | Insesgadez finita | conceptual_swap | high | $X_n \xrightarrow{\mathrm{m.s.}} c$ requiere $\mathbb{E}[X_n]=c$ para todo $n$ | Note que basta insesgadez asintótica ($\lim_{n\to\infty}\mathbb{E}[X_n]=c$), pues el cuadrado del sesgo límite es cero. |
| `D-C05-04` | Límite dentro valor abs | conceptual_swap | high | $L^r$ exige $\mathbb{E}[\lim_{n\to\infty}|X_n-X|^r]=0$ | Escriba el límite fuera de la esperanza: la definición de $L^r$ evalúa $\lim_{n\to\infty}\mathbb{E}[|X_n-X|^r]=0$. |
| `D-C05-05` | Sin momento orden r | conceptual_swap | high | $L^r$ aplica aunque $\mathbb{E}[|X_n|^r]=\infty$ | Verifique primero que los momentos absolutos de orden $r$ de $X_n$ y $X$ sean finitos para que la norma $L^r$ exista. |
| `D-C05-06` | Necesidad sin cota | conceptual_swap | high | $\mathrm{ECM}\to 0$ no implica que varianza y sesgo tiendan a $0$ | Recuerde que $\mathrm{Var}(X_n)\ge 0$ y $(\mathbb{E}[X_n]-c)^2\ge 0$; por Teorema del Sándwich ambos deben ir a cero. |
| `D-C05-07` | Solo varianza cero | conceptual_swap | high | $X_n \xrightarrow{m.s.} c \Leftrightarrow \mathrm{Var}(X_n) \to 0$ | Descomponga $E[(X_n - c)^2] = \mathrm{Var}(X_n) + (E[X_n] - c)^2$; si el sesgo no tiende a cero, el ECM converge al sesgo al cuadrado y no a $c$. |
| `D-C05-08` | Solo sesgo cero | conceptual_swap | high | $E[X_n] \to c$ basta para que $X_n \xrightarrow{m.s.} c$ | Exija también que $\mathrm{Var}(X_n) \to 0$, pues un estimador insesgado cuya varianza no disminuye (como $Y_1$) no converge a $c$. |
| `D-C05-09` | Implicación invertida | conceptual_swap | high | $X_n \xrightarrow{p} c \Rightarrow X_n \xrightarrow{m.s.} c$ | Recuerde que Markov aplicada a $(X_n - c)^2$ prueba $m.s. \Rightarrow p$, pero la recíproca falla si colas pequeñas hacen divergir el segundo momento. |
| `D-C05-10` | Potencia lineal en ECM | conceptual_swap | high | $\mathrm{ECM} = \mathrm{Var}(X_n) + \mathrm{Sesgo}$ | Eleve el sesgo al cuadrado en $E[(X_n - c)^2] = \mathrm{Var}(X_n) + \mathrm{Sesgo}^2$ para que ambos términos sean no negativos y coherentes en unidades. |
| `D-C05-11` | Diferencia absoluta | conceptual_swap | high | $X_n \xrightarrow{m.s.} c \Leftrightarrow E[X_n - c] \to 0$ | Use el error cuadrático $(X_n - c)^2$ para evitar que errores positivos y negativos se cancelen entre sí. |
| `D-C05-12` | Exige insesgadez exacta | conceptual_swap | high | Si $E[X_n] \neq c$ para todo $n$, entonces $X_n$ no converge en media cuadrática | Permita sesgo en muestras finitas siempre que dicho sesgo tienda a cero cuando $n \to \infty$ junto con la varianza. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Momentos absolutos finitos $\mathbb{E}[|X_n|^r] < \infty$ para todo $n$ y $\mathbb{E}[|X|^r] < \infty$ | Sin momentos finitos de orden $r$ no puede definirse la convergencia en $L^r$. | - |
| `A-C05-02` | - | Existencia del segundo momento finito $E[X_n^2] < \infty$ para todo $n$ | Si $X_n$ carece de segundo momento finito, el error cuadrático medio no está definido y $\xrightarrow{m.s.}$ no aplica. | - |

---

### [Hab-02] Evaluación de ECM, Tasas de Convergencia y Consistencia (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 12: Convergencia Superconsistente del Mínimo Exponencial
- **Prerequisites:** C-05, Hab-01
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 12), `Clases_sintetizadas_semana_9.pdf` (page 25), `EST3_LEC07_26.2_V2.pdf` (page 9), `EST3_LEC07_26.2_V2.pdf` (page 30)

#### Description & Cognitive Model
Cálculo analítico de $\mathbb{E}[\hat{\theta}_n]$, $\mathrm{Var}(\hat{\theta}_n)$ y $\mathrm{ECM}(\hat{\theta}_n) = \mathrm{Var}(\hat{\theta}_n) + [\mathrm{Sesgo}(\hat{\theta}_n)]^2$ para comparar estimadores bajo el trade-off sesgo-varianza, diagnosticar consistencia y evaluar tasas de caída $1/n$ frente a tasas superconsistentes $\mathcal{O}(1/n^2)$ como $X_{(1)} \sim \mathrm{Exponencial}(n\theta)$.

#### Fused Distractor Models (24)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | FDA en lugar supervivencia | skipped_step | high | $\mathbb{P}(X_{(1)}>t) = \prod \mathbb{P}(X_i \le t)$ | Use la función de supervivencia: el mínimo supera $t$ si y solo si todas las observaciones superan $t$, dando $e^{-n\theta t}$. |
| `D-Hab02-02` | Parámetro sin escalar | skipped_step | high | $X_{(1)} \sim \mathrm{Exponencial}(\theta/n)$ | Sume los exponentes al multiplicar $n$ veces $e^{-\theta t}$: el parámetro de tasa se multiplica por $n$ ($\lambda_n = n\theta$). |
| `D-Hab02-03` | Varianza con tasa 1/n | conceptual_swap | high | $\mathrm{Var}(X_{(1)}) = \frac{1}{n\theta^2}$ | Sustituya $\lambda_n = n\theta$ completo en la varianza exponencial $1/\lambda_n^2$: resulta $1/(n^2\theta^2)$, tasa $\mathcal{O}(1/n^2)$. |
| `D-Hab02-04` | Olvida sesgo en ECM | skipped_step | high | $\mathrm{ECM}(X_{(1)}) = \frac{1}{n^2\theta^2}$ | Sume varianza y cuadrado del sesgo hacia $c=0$: $\frac{1}{n^2\theta^2} + (\frac{1}{n\theta})^2 = \frac{2}{n^2\theta^2}$. |
| `D-Hab02-05` | Límite igual a 1/theta | conceptual_swap | high | $X_{(1)} \xrightarrow{\mathrm{m.s.}} \frac{1}{\theta}$ | Tome $n\to\infty$ sobre $\mathbb{E}[X_{(1)}]=1/(n\theta)$: el mínimo colapsa hacia la frontera inferior del soporte $c=0$. |
| `D-Hab02-06` | Densidad como FDA | conceptual_swap | high | $F_{X_{(1)}}(t) = e^{-n\theta t}$ | Calcule el complemento $F_{X_{(1)}}(t) = 1 - \mathbb{P}(X_{(1)} > t) = 1 - e^{-n\theta t}$ para $t \ge 0$. |
| `D-Hab02-07` | No cuadra pesos en varianza | skipped_step | high | $\operatorname{Var}(M_B)=\left(\frac{1-a}{1-a^n}\right)\sigma_Y^2\sum_{i=1}^n a^{i-1}$ | Por propiedades de la varianza de variables independientes, cada coeficiente $c_i=\frac{1-a}{1-a^n}a^{i-1}$ debe elevarse al cuadrado: $\sum c_i^2 \sigma_Y^2$ con razón $r=a^2$. |
| `D-Hab02-08` | Error en suma geométrica | skipped_step | high | $\sum_{i=1}^n a^{2(i-1)}=\frac{1-a^n}{1-a^2}$ | Al identificar $\sum_{i=1}^n a^{2(i-1)}=\sum_{i=1}^n (a^2)^{i-1}$, la fórmula $\frac{1-r^n}{1-r}$ con $r=a^2$ produce $\frac{1-(a^2)^n}{1-a^2}=\frac{1-a^{2n}}{1-a^2}$. |
| `D-Hab02-09` | Varianza alterada por +1/n | conceptual_swap | high | $\operatorname{Var}(\bar{Y}_n+1/n)=\frac{\sigma_Y^2}{n}+\frac{1}{n^2}$ | La constante determinística $1/n$ traslada la media ($\operatorname{Sesgo}=1/n$) pero no aporta variabilidad: $\operatorname{Var}(M_C)=\sigma_Y^2/n$, mientras el $1/n^2$ entra en el $\operatorname{ECM}$. |
| `D-Hab02-10` | Límite erróneo de $a^n$ | conceptual_swap | high | $\lim_{n\to\infty} a^n = 1 \text{ para } 0<a<1$ | Como $0<a<1$ estrictamente, la potencia exponencial decae a cero ($\lim_{n\to\infty}a^n=0$), dejando $\lim\operatorname{Var}(M_B)=\sigma_Y^2\frac{1-a}{1+a}>0$. |
| `D-Hab02-11` | Olvida factorizar 1-a2n | conceptual_swap | high | $\frac{(1-a)^2}{(1-a^n)^2}\cdot\frac{1-a^{2n}}{1-a^2}=\frac{1-a}{1-a^n}$ | Factorice $1-a^2=(1-a)(1+a)$ y $1-a^{2n}=(1-a^n)(1+a^n)$ antes de simplificar para obtener $\sigma_Y^2\left(\frac{1-a}{1+a}\right)\left(\frac{1+a^n}{1-a^n}\right)$. |
| `D-Hab02-12` | ECM suma sesgo lineal | conceptual_swap | high | $\operatorname{ECM}(M_C)=\operatorname{Var}(M_C)+\operatorname{Sesgo}(M_C)$ | Por la descomposición del Error Cuadrático Medio, el sesgo entra elevado al cuadrado: $\operatorname{ECM}(M_C)=\operatorname{Var}(M_C)+[\operatorname{Sesgo}(M_C)]^2=\frac{\sigma_Y^2}{n}+\frac{1}{n^2}$. |
| `D-Hab02-13` | Omite elevar el sesgo al cuadrado | skipped_step | high | $\mathrm{ECM}(\hat{\theta})=\mathrm{Var}(\hat{\theta})+\mathrm{Sesgo}(\hat{\theta})$ | Eleve el sesgo al cuadrado en $\mathrm{Var}(\hat{\theta})+[\mathrm{Sesgo}(\hat{\theta})]^2$ para mantener unidades cuadráticas positivas. |
| `D-Hab02-14` | Rechaza todo estimador sesgado automáticamente | skipped_step | high | Sesgado siempre tiene mayor ECM que insesgado | Compare el ECM total: un estimador con pequeño sesgo puede lograr menor ECM si reduce suficientemente la varianza. |
| `D-Hab02-15` | Conserva término cruzado distinto de cero | conceptual_swap | high | $\mathrm{ECM}=\mathrm{Var}+\mathrm{Sesgo}^2+2\cdot\mathrm{Sesgo}$ | Verifique que $2(E[\hat{\theta}]-\theta)E[\hat{\theta}-E[\hat{\theta}]]=0$ porque $E[\hat{\theta}-E[\hat{\theta}]]=0$. |
| `D-Hab02-16` | Eleva $0.9$ linealmente en la varianza | conceptual_swap | high | $\mathrm{Var}(0.9\bar{Y})=0.9\mathrm{Var}(\bar{Y})$ | Eleve el factor de contracción al cuadrado: $\mathrm{Var}(c\bar{Y})=c^2\mathrm{Var}(\bar{Y})=0.81\times 0.4=0.324$. |
| `D-Hab02-17` | Confunde ECM con varianza en sesgados | conceptual_swap | high | $\mathrm{ECM}(\hat{\theta})=\mathrm{Var}(\hat{\theta})$ siempre | Recuerde que $\mathrm{ECM}=\mathrm{Var}$ únicamente cuando el estimador es insesgado; con sesgo debe sumar $[\mathrm{Sesgo}(\hat{\theta})]^2$. |
| `D-Hab02-18` | Cree que mayor ECM es mejor | conceptual_swap | high | Mayor ECM indica mejor estimador | Minimice el ECM, pues mide la distancia cuadrática promedio entre el estimador $\hat{\theta}$ y el parámetro $\theta$. |
| `D-Hab02-19` | Tasa errónea del sesgo cuadrado | skipped_step | high | Para $\mathrm{Sesgo} = 5/n$, el término $\mathrm{Sesgo}^2$ es $5/n$ o $25/n$ | Eleve tanto el numerador como el denominador al cuadrado: $(5/n)^2 = 25/n^2$, el cual decae más rápido que $\mathrm{Var} = 100/n$. |
| `D-Hab02-20` | Descarta por sesgado | skipped_step | high | Como $\hat{\mu}_n = \bar{Y}_n + 5/n$ tiene sesgo $5/n \neq 0$, es inconsistente | Evalúe el límite cuando $n \to \infty$: aunque $5/n \neq 0$ para todo $n$ finito, tanto $5/n \to 0$ como $100/n \to 0$, luego $\mathrm{ECM} \to 0$ y $\hat{\mu}_n$ es consistente. |
| `D-Hab02-21` | Varianza afectada por constante | conceptual_swap | high | $\mathrm{Var}(\bar{Y}_n + 5/n) = \frac{100}{n} + \frac{25}{n^2}$ | Recuerde que sumar la constante determinista $5/n$ desplaza la media (genera sesgo) pero deja intacta la varianza $\mathrm{Var}(\bar{Y}_n) = 100/n$. |
| `D-Hab02-22` | Confunde tasas de caída | conceptual_swap | high | El $\mathrm{Sesgo}^2$ cae más lento ($1/n$) que la varianza ($1/n^2$) | Compare órdenes: $25/n^2$ decae cuadráticamente frente a $100/n$, de modo que para $n$ grande casi todo el ECM proviene de la varianza. |
| `D-Hab02-23` | Suma desvío estándar y sesgo | conceptual_swap | high | $\mathrm{ECM} = \frac{10}{\sqrt{n}} + \frac{5}{n}$ | Sume magnitudes cuadráticas homogéneas: varianza ($100/n$) más sesgo al cuadrado ($25/n^2$). |
| `D-Hab02-24` | Cero solo si sesgo cero | conceptual_swap | high | $\mathrm{ECM} \to 0$ únicamente cuando $\mathrm{Sesgo} = 0$ idénticamente | Verifique que basta la desaparición asintótica del sesgo ($\mathrm{Sesgo} \to 0$) para que $\mathrm{ECM} \to 0$. |

#### Formal Mathematical Assumptions (4)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Muestra aleatoria simple i.i.d. con $X_i \sim \mathrm{Exponencial}(\theta)$ y parámetro fijo $\theta > 0$ | Sin independencia ni soporte $[0,\infty)$, $X_{(1)}$ no sigue ley $\mathrm{Exponencial}(n\theta)$. | - |
| `A-Hab02-02` | - | Muestra i.i.d. $Y_i \sim \mathcal{N}(\mu_Y,\sigma_Y^2)$ con $0<\sigma_Y^2<\infty$ y $a\in(0,1)$ | Garantiza independencia en la varianza de $M_B$ y decaimiento $a^n\to 0$. | - |
| `A-Hab02-03` | - | El estimador $\hat{\theta}$ tiene varianza y sesgo finitos | Permite descomponer el ECM en suma finita de varianza y sesgo al cuadrado. | - |
| `A-Hab02-04` | - | Descomposición aditiva válida $E[(\hat{\theta}_n - \theta)^2] = \mathrm{Var}(\hat{\theta}_n) + (E[\hat{\theta}_n] - \theta)^2$ con segundo momento finito | Sin varianza finita o si el sesgo no se expresa como función de $n$, no pueden compararse tasas asintóticas del ECM. | - |

---

### [C-06] Desigualdad de Markov y Esperanza Truncada (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 14: Desigualdad de Markov y Esperanza Truncada
- **Prerequisites:** C-04, PRE-01
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 14), `EST3_LEC07_26.2_V2.pdf` (page 21)

#### Description & Cognitive Model
Teorema de Markov $\mathbb{P}(Y \ge \delta) \le \mathbb{E}[Y]/\delta$ para variables no negativas casi seguramente $Y \ge 0$ sin conocer su distribución, y su prueba por partición y monotonía $\mathbb{E}[Y \mid Y \ge \delta] \ge \delta$.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Sin no negatividad | conceptual_swap | high | Markov aplica a cualquier variable real $Y \in \mathbb{R}$ | Exija $\mathbb{P}(Y \ge 0) = 1$: si $Y$ toma valores negativos, descartar la parte $Y < \delta$ no preserva la desigualdad. |
| `D-C06-02` | Sentido invertido | conceptual_swap | high | $\mathbb{P}(Y \ge \delta) \ge \frac{\mathbb{E}[Y]}{\delta}$ | Verifique la lectura: como $\mathbb{E}[Y] \ge \delta\,\mathbb{P}(Y\ge\delta)$, dividir entre $\delta>0$ da un techo máximo, no mínimo. |
| `D-C06-03` | Condicional menor delta | conceptual_swap | high | $\mathbb{E}[Y \mid Y \ge \delta] \le \delta$ | Recuerde la monotonía: en el subuniverso $\{Y\ge\delta\}$ todos los valores son al menos $\delta$, luego su promedio es $\ge \delta$. |
| `D-C06-04` | Umbral no positivo | conceptual_swap | high | Permite evaluar la cota en $\delta \le 0$ | Restrinja $\delta > 0$ estrictamente para evitar división por cero y preservar el sentido de la desigualdad al dividir. |
| `D-C06-05` | Cota menor que uno | conceptual_swap | high | $\mathbb{E}[Y]/\delta$ siempre es menor o igual a $1$ | Note que si $\delta < \mathbb{E}[Y]$ la cota supera $1$ y sigue siendo válida matemáticamente, aunque trivialmente informativa. |
| `D-C06-06` | Sin factor probabilidad | conceptual_swap | high | $\mathbb{E}[Y] = \mathbb{E}[Y \mid Y < \delta] + \mathbb{E}[Y \mid Y \ge \delta]$ | Aplique la Ley de Esperanzas Iteradas ponderando cada esperanza condicional por la probabilidad de su evento en la partición. |
| `D-C06-07` | Sin no negatividad | conceptual_swap | high | $P(Y \ge \delta) \le \frac{E[Y]}{\delta}$ vale para cualquier $Y \in \mathbb{R}$ | Verifique que $Y \ge 0$ casi seguramente antes de usar Markov; si $Y$ toma negativos, la cota falla. |
| `D-C06-08` | Invierte razón | conceptual_swap | high | $P(Y \ge \delta) \le \frac{\delta}{E[Y]}$ | Divida la esperanza $E[Y]$ entre el umbral $\delta$, pues umbrales mayores reducen la probabilidad máxima. |
| `D-C06-09` | Igualdad exacta | conceptual_swap | high | $P(Y \ge \delta) = \frac{E[Y]}{\delta}$ | Interprete $E[Y]/\delta$ como una cota superior gruesa pero universal, nunca como la probabilidad exacta del evento. |
| `D-C06-10` | Cola inferior | conceptual_swap | high | $P(Y \le \delta) \le \frac{E[Y]}{\delta}$ | Recuerde que Markov acota la cola derecha $Y \ge \delta$, ya que solo allí se cumple $Y \cdot 1\{Y \ge \delta\} \ge \delta \cdot 1\{Y \ge \delta\}$. |
| `D-C06-11` | Cota por varianza | conceptual_swap | high | $P(Y \ge \delta) \le \frac{\mathrm{Var}(Y)}{\delta}$ | Use $E[Y]$ en el numerador de Markov; la varianza entra recién en Chebyshev al transformar a $(X - \mu)^2$. |
| `D-C06-12` | Exige normalidad | conceptual_swap | high | Markov solo aplica si $Y$ tiene distribución conocida | Aproveche precisamente que Markov no requiere conocer la forma distribucional de $Y$, solo su existencia de media y $Y \ge 0$. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | No negatividad casi segura $\mathbb{P}(Y \ge 0)=1$, $\mathbb{E}[Y]<\infty$ y umbral $\delta > 0$ | Sin no negatividad casi segura falla la supresión del término $\mathbb{P}(Y<\delta)\mathbb{E}[Y\mid Y<\delta]$. | - |
| `A-C06-02` | - | Variable aleatoria no negativa $Y \ge 0$ con esperanza finita $E[Y] < \infty$ | Si $Y$ toma valores negativos o $E[Y]$ no existe, la desigualdad $E[Y] \ge \delta P(Y \ge \delta)$ deja de cumplirse. | - |
| `A-C06-03` | - | Umbral estrictamente positivo $\delta > 0$ | Si $\delta \le 0$, el cociente $E[Y]/\delta$ se indefine o invierte el sentido de la cota. | - |

---

### [Hab-03] Desigualdad de Chebyshev y Demostración de Consistencia (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 16: Deducción de Chebyshev Generalizada y Estándar
- **Prerequisites:** C-06
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 16), `EST3_LEC07_26.2_V2.pdf` (page 23), `EST3_LEC07_26.2_V2.pdf` (page 28)

#### Description & Cognitive Model
Transformación auxiliar $Y=|X-c|^r$ y $\delta=\varepsilon^r$ en Markov para deducir la desigualdad de Chebyshev generalizada y estándar $\mathbb{P}(|X-\mu|\ge\varepsilon)\le \mathrm{Var}(X)/\varepsilon^2$, acotar desvíos y demostrar la consistencia de $\bar{Y}_n$ mediante $\mathbb{P}(|\bar{Y}_n-\mu|>\varepsilon)\le \frac{\sigma^2}{n\varepsilon^2}\to 0$.

#### Fused Distractor Models (18)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Omite potencia en eps | skipped_step | high | $\mathbb{P}(|X-c| \ge \varepsilon) \le \frac{\mathbb{E}[|X-c|^r]}{\varepsilon}$ | Transforme ambos lados del evento con $h(u)=u^r$: $\delta = \varepsilon^r$ debe aparecer elevado a $r$ en el denominador. |
| `D-Hab03-02` | Exponente negativo r | skipped_step | high | La equivalencia de eventos vale para todo $r \in \mathbb{R}$ | Justifique monotonía estricta con $h'(u)=ru^{r-1}>0$: requiere $r > 0$ para preservar el sentido de la desigualdad. |
| `D-Hab03-03` | Varianza con c distinto | skipped_step | high | $\mathbb{P}(|X-c| \ge \varepsilon) \le \frac{\mathrm{Var}(X)}{\varepsilon^2}$ para todo $c$ | Recuerde que para $c \neq \mu$ el numerador es $\mathbb{E}[(X-c)^2]$; solo coincide con $\mathrm{Var}(X)$ al elegir $c=\mu=\mathbb{E}[X]$. |
| `D-Hab03-04` | Sin valor absoluto | conceptual_swap | high | $\mathbb{P}(X-c \ge \varepsilon) = \mathbb{P}((X-c)^r \ge \varepsilon^r)$ | Conserve el valor absoluto $|X-c|\ge 0$ antes de elevar a $r$; sin módulo los valores negativos alteran la equivalencia. |
| `D-Hab03-05` | Desviación en lugar var | conceptual_swap | high | $\mathbb{P}(|X-\mu| \ge \varepsilon) \le \frac{\sigma}{\varepsilon^2}$ o $\frac{\sigma^2}{\varepsilon}$ | Mantenga consistencia de orden $r=2$: numerador en unidades cuadráticas $\mathrm{Var}(X)=\sigma^2$ y denominador $\varepsilon^2$. |
| `D-Hab03-06` | Falla en estricta | conceptual_swap | high | La cota no vale para desigualdad estricta $|X-c| > \varepsilon$ | Use inclusión de eventos: $\{|X-c|>\varepsilon\} \subseteq \{|X-c|\ge\varepsilon\}$, por lo que mantiene la misma cota superior. |
| `D-Hab03-07` | Olvida cuadrado en epsilon | skipped_step | high | $P(|X - \mu| \ge \epsilon) \le \frac{\mathrm{Var}(X)}{\epsilon}$ | Eleve el margen $\epsilon$ al cuadrado al pasar de $|X - \mu| \ge \epsilon$ a $(X - \mu)^2 \ge \epsilon^2$ antes de aplicar Markov. |
| `D-Hab03-08` | Usa sigma sin elevar | skipped_step | high | $P(|X - \mu| \ge \epsilon) \le \frac{\sigma}{\epsilon^2}$ | Use la varianza $\mathrm{Var}(X) = \sigma^2$ en el numerador, ya que $E[(X - \mu)^2] = \sigma^2$ y no $\sigma$. |
| `D-Hab03-09` | Confunde k con epsilon | conceptual_swap | high | $P(|X - \mu| \ge k\sigma) \le \frac{\sigma^2}{k^2}$ | Cancele $\sigma^2$ al sustituir $\epsilon = k\sigma$: $\sigma^2 / (k\sigma)^2 = 1/k^2$, independiente de $\sigma$. |
| `D-Hab03-10` | Cota de probabilidad exacta | conceptual_swap | high | $P(|X - 170| \ge 10) = 0.25$ exactamente | Recuerde que Chebyshev da un techo conservador válido para toda distribución; bajo normalidad el valor real es $4.6\%$. |
| `D-Hab03-11` | Cola dentro del intervalo | conceptual_swap | high | $P(|X - \mu| \le k\sigma) \le \frac{1}{k^2}$ | Aplique el complemento: al menos $1 - 1/k^2$ cae dentro de $\mu \pm k\sigma$, y a lo sumo $1/k^2$ queda fuera. |
| `D-Hab03-12` | No aplica sin normalidad | conceptual_swap | high | Sin normalidad no se puede acotar $P(|X - \mu| \ge k\sigma)$ | Use Chebyshev precisamente cuando desconozca la distribución, pues solo requiere media y varianza finitas. |
| `D-Hab03-13` | Olvida dividir por n | skipped_step | high | $\mathrm{Var}(\bar{Y}_n) = \sigma^2$, luego $P(|\bar{Y}_n - \mu| > \epsilon) \le \frac{\sigma^2}{\epsilon^2}$ | Divida la varianza poblacional $\sigma^2$ entre $n$ para obtener $\mathrm{Var}(\bar{Y}_n) = \sigma^2/n$; sin ese factor $1/n$ la cota no converge a cero. |
| `D-Hab03-14` | Usa n al cuadrado | conceptual_swap | high | $P(|\bar{Y}_n - \mu| > \epsilon) \le \frac{\sigma^2}{n^2 \epsilon^2}$ | Recuerde que $ee(\bar{Y}_n) = \sigma/\sqrt{n}$, por lo que al elevarlo al cuadrado resulta $\mathrm{Var}(\bar{Y}_n) = \sigma^2/n$ y no $\sigma^2/n^2$. |
| `D-Hab03-15` | Exige normalidad para cota | conceptual_swap | high | La cota $\frac{100}{4n}$ requiere $Y_i \sim N(50, 100)$ | Separe ambas columnas: la probabilidad exacta sí supone $Y_i \sim N(50,100)$, pero la cota de Chebyshev $\sigma^2/(n\epsilon^2)$ solo usa varianza finita. |
| `D-Hab03-16` | Cota mayor que uno | conceptual_swap | high | Para $n=25$ y $\epsilon=2$, la probabilidad exacta es $1.000$ | Recuerde que una cota superior igual a $1$ es no informativa (toda probabilidad es $\le 1$); el valor normal exacto en ese caso es $0.317$. |
| `D-Hab03-17` | Omite epsilon al cuadrado | skipped_step | high | $P(|\bar{Y}_n - 50| > 2) \le \frac{100}{2n}$ | Eleve $\epsilon = 2$ al cuadrado en el denominador de Chebyshev para obtener $100/(4n) = 25/n$. |
| `D-Hab03-18` | Descarta consistencia en n=25 | conceptual_swap | high | Si para $n=25$ la cota es $1.000$, entonces $\bar{Y}_n$ no es consistente | Evalúe el comportamiento asintótico cuando $n \to \infty$: la cota $\sigma^2/(n\epsilon^2) \to 0$ para todo $\epsilon > 0$, demostrando consistencia. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | Orden $r > 0$ con momento absoluto finito $\mathbb{E}[|X-c|^r] < \infty$ y $\varepsilon > 0$ | Sin $r>0$ y momento finito, falla la monotonía o diverge la cota de Markov. | - |
| `A-Hab03-02` | - | Varianza finita $\mathrm{Var}(X) = \sigma^2 < \infty$ y $\epsilon > 0$ | Si la varianza es infinita, la cota de Chebyshev resulta trivial o inaplicable. | - |
| `A-Hab03-03` | - | Observaciones muestrales con media común $\mu$, varianza finita $\sigma^2 < \infty$ e independencia (o incorrelación) tal que $\mathrm{Var}(\bar{Y}_n) = \sigma^2/n$ | Si la correlación entre observaciones no decae y $\mathrm{Var}(\bar{Y}_n)$ no tiende a cero, la cota no prueba consistencia. | - |

---

### [C-08] Desigualdad de Cauchy-Schwarz y Correlación (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 18: Desigualdad de Cauchy-Schwarz y Correlación
- **Prerequisites:** PRE-01
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 18)

#### Description & Cognitive Model
Teorema 4.4: $(\mathbb{E}[XY])^2 \le \mathbb{E}[X^2]\mathbb{E}[Y^2]$ demostrada por el método del discriminante sobre $P(t)=\mathbb{E}[(tX+Y)^2]\ge 0$, implicando $|\operatorname{Cov}(X,Y)|\le \sigma_X\sigma_Y$ y $|\rho_{XY}|\le 1$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Omite cuadrado en E[XY] | conceptual_swap | high | $\mathbb{E}[XY] \le \mathbb{E}[X^2]\mathbb{E}[Y^2]$ | Por homogeneidad dimensional, $(\mathbb{E}[XY])^2$ se compara con $\mathbb{E}[X^2]\mathbb{E}[Y^2]$, o bien $|\mathbb{E}[XY]|$ con $\sqrt{\mathbb{E}[X^2]}\sqrt{\mathbb{E}[Y^2]}$. |
| `D-C08-02` | Confunde con producto de medias | conceptual_swap | high | $(\mathbb{E}[XY])^2 \le (\mathbb{E}[X])^2(\mathbb{E}[Y])^2$ | Cauchy-Schwarz acota el producto cruzado usando segundos momentos $\mathbb{E}[X^2]$ y $\mathbb{E}[Y^2]$ (normas $L^2$), no las medias al cuadrado. |
| `D-C08-03` | Signo del discriminante | conceptual_swap | high | $\Delta = b^2-4ac \ge 0$ | Una parábola con $a=\mathbb{E}[X^2]>0$ que nunca cruza bajo el eje horizontal tiene a lo sumo una raíz real, lo que exige discriminante $\Delta \le 0$. |
| `D-C08-04` | Olvida centrar en Cov | conceptual_swap | high | $|\operatorname{Cov}(X,Y)| \le \sqrt{\mathbb{E}[X^2]}\sqrt{\mathbb{E}[Y^2]}$ | La cota $|\operatorname{Cov}(X,Y)|\le \sigma_X\sigma_Y$ y $-1\le\rho_{XY}\le 1$ resulta de aplicar Cauchy-Schwarz a variables centradas $\tilde{X}=X-\mathbb{E}[X]$ e $\tilde{Y}=Y-\mathbb{E}[Y]$. |
| `D-C08-05` | Omite factor 2 en b | conceptual_swap | high | $b=\mathbb{E}[XY]$ | Al expandir $\mathbb{E}[(tX+Y)^2]$ el coeficiente lineal es $b=2\mathbb{E}[XY]$, cuya cancelación del factor $4$ en $b^2-4ac\le 0$ produce la desigualdad exacta. |
| `D-C08-06` | Divide por E[X2]=0 | conceptual_swap | high | Caso trivial requiere $\Delta \le 0$ | Si $\mathbb{E}[X^2]=0$, la variable colapsa a $0$ c.s. y el polinomio degenera en constante; se resuelve aparte verificando $0\le 0$ directamente. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Segundos momentos finitos $\mathbb{E}[X^2]<\infty$ y $\mathbb{E}[Y^2]<\infty$ | Sin pertenencia a $L^2$ la forma cuadrática $\mathbb{E}[(tX+Y)^2]$ no está bien definida. | - |

---

### [C-09] Modos de Convergencia, Jerarquía y No Reciprocidad (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 20: Jerarquía de Convergencias Lr y Probabilidad
- **Prerequisites:** PRE-01, C-05, Hab-03
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 20), `Clases_sintetizadas_semana_9.pdf` (page 22), `EST3_LEC07_26.2_V2.pdf` (page 31), `EST3_LEC07_26.2_V2.pdf` (page 33), `EST3_LEC07_26.2_V2.pdf` (page 35)

#### Description & Cognitive Model
Modos de convergencia ($L^r$, casi segura $X_n \xrightarrow{a.s.} c$, en probabilidad $X_n \xrightarrow{p} c$ y en distribución $X_n \xrightarrow{d} X$), jerarquía de implicaciones ($X_n \xrightarrow{r} X \Rightarrow X_n \xrightarrow{s} X \Rightarrow X_n \xrightarrow{p} X \Rightarrow X_n \xrightarrow{d} X$ y $X_n \xrightarrow{a.s.} X \Rightarrow X_n \xrightarrow{p} X$) y refutación de falsas recíprocas: $X_n \xrightarrow{p} c$ no implica $L^1, L^2$ ni $\mathbb{E}[X_n]\to c$, e insesgadez finita es lógicamente independiente de la consistencia.

#### Fused Distractor Models (30)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Invierte orden de potencias | conceptual_swap | high | $X_n \xrightarrow{s} X \Rightarrow X_n \xrightarrow{r} X \ (0<s<r)$ | Las normas de orden superior penalizan más las colas; por ello $L^r$ domina a $L^s$ cuando $r>s$, nunca al revés ($L^2 \Rightarrow L^1$, no $L^1 \Rightarrow L^2$). |
| `D-C09-02` | Invierte m.s. y probabilidad | conceptual_swap | high | $X_n \xrightarrow{p} X \Rightarrow X_n \xrightarrow{m.s.} X$ | La implicación del Teorema 5.1 es unidireccional: convergencia en media cuadrática implica consistencia en probabilidad, pero la recíproca es falsa en general. |
| `D-C09-03` | Exponente convexo invertido | conceptual_swap | high | $g(z)=z^{s/r}$ es convexa ($0<s<r$) | Como $0<s<r$, el cociente $r/s>1$ hace que $g(z)=z^{r/s}$ sea convexa ($g''\ge 0$); elevar $\mathbb{E}[|X_n-X|^s]$ a $r/s$ permite acotarlo por $\mathbb{E}[|X_n-X|^r]$. |
| `D-C09-04` | Confunde momento con diferencia | conceptual_swap | high | $\mathbb{E}[|X_n|^r]\to\mathbb{E}[|X|^r] \Rightarrow X_n \xrightarrow{r} X$ | La convergencia de $\mathbb{E}[|X_n|^r]$ hacia $\mathbb{E}[|X|^r]$ es consecuencia de $X_n \xrightarrow{r} X$ vía Minkowski inversa, pero no implica que $X_n-X$ tienda a cero. |
| `D-C09-05` | Chebyshev con exponente erróneo | conceptual_swap | high | $\mathbb{P}(|X_n-X|>\varepsilon) \le \mathbb{E}[|X_n-X|^r]/\varepsilon$ | Al aplicar Chebyshev generalizada de orden $r$, el umbral $\varepsilon$ también debe elevarse a la potencia $r$: $\mathbb{E}[|X_n-X|^r]/\varepsilon^r \to 0$. |
| `D-C09-06` | Aplica Minkowski con r<1 | conceptual_swap | high | $\|U+V\|_r \le \|U\|_r+\|V\|_r$ para $0<r<1$ | La funcional $\|U\|_r=(\mathbb{E}[|U|^r])^{1/r}$ define una norma que satisface la desigualdad de Minkowski únicamente cuando $r \ge 1$. |
| `D-C09-07` | Asume p implica L2 | conceptual_swap | high | $X_n \xrightarrow{p} c \Rightarrow \lim \mathbb{E}[(X_n-c)^2]=0$ | El límite en probabilidad solo mide la masa fuera de $(-\varepsilon,\varepsilon)$, ignorando la magnitud de valores atípicos raros que pueden hacer diverger los momentos. |
| `D-C09-08` | Confunde plim con lim E | conceptual_swap | high | $\operatorname{plim} \hat{\theta}_n = \lim_{n\to\infty}\mathbb{E}[\hat{\theta}_n]$ | En variables instrumentales débiles o sucesiones como $X_n\in\{0,n\}$, $\operatorname{plim} X_n=0$ aunque $\lim \mathbb{E}[X_n]=1$ o $+\infty$; son operadores distintos. |
| `D-C09-09` | Insesgado implica consistente | conceptual_swap | high | $\mathbb{E}[\hat{\theta}_n]=\theta \Rightarrow \hat{\theta}_n \xrightarrow{p} \theta$ | La insesgadez es una propiedad de muestras finitas; si la varianza no colapsa a cero cuando $n\to\infty$ (como en $M_A$ o $M_B$), el estimador sigue siendo inconsistente. |
| `D-C09-10` | Consistente implica insesgado | conceptual_swap | high | $\hat{\theta}_n \xrightarrow{p} \theta \Rightarrow \mathbb{E}[\hat{\theta}_n]=\theta$ | Un estimador sesgado en muestras finitas es consistente siempre que tanto su sesgo como su varianza converjan a cero asintóticamente ($\operatorname{ECM}\to 0$). |
| `D-C09-11` | Usar toda la muestra basta | conceptual_swap | high | Incluir $n$ datos garantiza consistencia | Incluso usando las $n$ observaciones, ponderaciones que decaen geométricamente ($a^{i-1}$) concentran el peso en los primeros datos e impiden la cancelación por LDGN. |
| `D-C09-12` | Sesgo constante basta | conceptual_swap | high | $\operatorname{Var}(\hat{\theta}_n)\to 0$ basta para consistencia | Si la varianza tiende a cero pero el sesgo permanece distinto de cero en el límite, el estimador converge en probabilidad al valor sesgado $\theta+b$, no a $\theta$. |
| `D-C09-13` | Insesgadez implica consistencia | conceptual_swap | high | Todo estimador insesgado es automáticamente consistente | Use el contraejemplo $Y_1$: es insesgado en todo $n$, pero su varianza sigue siendo $\sigma^2 = 100$ sin importar cuán grande sea $n$, así que no es consistente. |
| `D-C09-14` | Consistencia implica insesgadez | conceptual_swap | high | Todo estimador consistente debe ser insesgado | Distinga propiedad de muestra finita y propiedad asintótica: $\bar{Y}_n + 5/n$ tiene sesgo $5/n$ en todo $n$ finito pero converge en probabilidad a $\mu$. |
| `D-C09-15` | Prioridad econométrica invertida | conceptual_swap | high | La econometría descarta estimadores sesgados en muestra finita aunque sean consistentes | Recuerde que en muestras grandes la econometría prioriza la consistencia, pues estimadores clave como MCO con regresores estocásticos, VI o MV son sesgados. |
| `D-C09-16` | Confunde media con dispersión | conceptual_swap | high | Insesgado significa que la varianza de $\hat{\theta}_n$ es cero | Separe primer momento y concentración: insesgadez solo fija el centro $E[\hat{\theta}_n] = \theta$ con $n$ fijo, no la varianza. |
| `D-C09-17` | Descarta sesgo de Jensen | conceptual_swap | high | Si $\hat{\sigma}^2$ es consistente e insesgado, entonces $\hat{\sigma} = \sqrt{\hat{\sigma}^2}$ es insesgado | Aplique Jensen para notar que $\sqrt{\hat{\sigma}^2}$ es sesgado en muestras finitas aunque siga siendo consistente por continuidad. |
| `D-C09-18` | Muestra fija vs límite | conceptual_swap | high | La consistencia se evalúa con $n$ fijo y la insesgadez con $n \to \infty$ | Asocie insesgadez a una propiedad exacta para $n$ fijo ($E[\hat{\theta}_n]=\theta$) y consistencia a una propiedad límite cuando $n \to \infty$. |
| `D-C09-19` | Equivalente a probabilidad | conceptual_swap | high | $X_n \xrightarrow{a.s.} c$ es equivalente a $X_n \xrightarrow{p} c$ | Note que $\xrightarrow{a.s.}$ exige que toda la trayectoria quede dentro de $c \pm \epsilon$ desde cierto $n$ en adelante, lo cual es estrictamente más fuerte que $\xrightarrow{p}$. |
| `D-C09-20` | Invierte cuantificador | conceptual_swap | high | $X_n \xrightarrow{p} c \Rightarrow X_n \xrightarrow{a.s.} c$ | Recuerde la dirección correcta: $\xrightarrow{a.s.} \Rightarrow \xrightarrow{p}$, ya que una sucesión puede converger en probabilidad con excursiones raras infinitamente frecuentes. |
| `D-C09-21` | Confunde límite y P | conceptual_swap | high | $X_n \xrightarrow{a.s.} c \Leftrightarrow \lim_{n\to\infty} P(X_n = c) = 1$ | Coloque el límite dentro de $P(\cdot)$: $P(\lim_{n\to\infty} X_n = c) = 1$ evalúa la probabilidad del conjunto de trayectorias convergentes. |
| `D-C09-22` | Cero saltos iniciales | conceptual_swap | high | En convergencia casi segura, $X_n$ nunca se aleja de $c$ desde $n=1$ | Permita desviaciones iniciales grandes (como en los primeros $10$ lanzamientos); lo exigido es que desde algún $N(\omega)$ finito ya no vuelva a salir de $c \pm \epsilon$. |
| `D-C09-23` | Ley débil en vez de fuerte | conceptual_swap | high | La ley débil garantiza $P(\lim_{n\to\infty} \bar{Y}_n = \mu) = 1$ | Distinga ambos teoremas: la ley débil prueba $\xrightarrow{p}$, mientras que la Ley Fuerte de los Grandes Números garantiza $\xrightarrow{a.s.}$ con probabilidad $1$. |
| `D-C09-24` | Certeza determinista | conceptual_swap | high | Probabilidad $1$ implica que no existe ningún resultado $\omega$ donde falle | Recuerde que casi seguro permite un conjunto excepcional de eventos con probabilidad cero donde la trayectoria no converge. |
| `D-C09-25` | Iguala realizaciones | conceptual_swap | high | $X_n \xrightarrow{d} X$ implica que $X_n$ y $X$ toman valores cercanos | Recuerde que $\xrightarrow{d}$ solo compara las formas de las funciones de distribución acumulada $F_{X_n}$ y $F_X$, no la cercanía entre variables. |
| `D-C09-26` | Exige todo punto x | conceptual_swap | high | Debe cumplirse $F_{X_n}(x) \to F_X(x)$ incluso en discontinuidades de $F_X$ | Excluya los puntos de discontinuidad de $F_X$ en la definición para no rechazar convergencias naturales a límites puntuales como $1/n \to 0$. |
| `D-C09-27` | Compara densidades siempre | conceptual_swap | high | $X_n \xrightarrow{d} X$ equivale a convergencia de las medias $E[X_n] \to E[X]$ | Evalúe la convergencia puntual de las funciones de distribución acumulada $P(X_n \le x) \to P(X \le x)$ en puntos continuos de $F_X$. |
| `D-C09-28` | Normalidad en n finito | conceptual_swap | high | Si $Z_n \xrightarrow{d} N(0,1)$, entonces $Z_n$ es exactamente normal para $n=30$ | Reconozca que en muestras finitas de datos asimétricos la aproximación normal presenta un error ($0.941$ vs $0.950$) que desaparece cuando $n \to \infty$. |
| `D-C09-29` | No sirve para inferencia | conceptual_swap | high | La convergencia en distribución no permite construir intervalos ni contrastes | Aplique $\xrightarrow{d}$ precisamente para justificar el uso de cuantiles límite (normal o $\chi^2$) en inferencia asintótica. |
| `D-C09-30` | Exige mismo espacio | conceptual_swap | high | $X_n$ y $X$ deben estar definidos con dependencia conjunta positiva | Note que $F_{X_n}$ y $F_X$ solo dependen de las distribuciones marginales de cada variable. |

#### Formal Mathematical Assumptions (5)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Para convergencia de momentos absolutos se requiere $r \ge 1$ y $\mathbb{E}[|X|^r]<\infty$ | Sin $r \ge 1$ falla Minkowski y sin momento finito la norma límite diverge. | - |
| `A-C09-02` | - | Comparación entre propiedades puntuales para $n$ finito y comportamiento límite cuando $n\to\infty$ | Sin distinguir régimen finito de asintótico se confunden sesgo y consistencia. | - |
| `A-C09-03` | - | Existencia de la esperanza $E[\hat{\theta}_n]$ cuando se evalúa insesgadez en muestras finitas | Un estimador consistente puede carecer de esperanza finita en muestras pequeñas, imposibilitando definir su sesgo. | - |
| `A-C09-04` | - | Espacio de probabilidad $(\Omega, \mathcal{F}, P)$ que soporte simultáneamente toda la trayectoria infinita $\{X_n\}_{n \ge 1}$ | Sin una medida conjunta sobre trayectorias completas, el evento $\{\lim_{n\to\infty} X_n = c\}$ no es medible. | - |
| `A-C09-05` | - | Evaluación del límite únicamente en puntos $x$ donde la FDA límite $F_X$ es continua | Incluir puntos de salto de $F_X$ invalidaría casos básicos como $X_n = 1/n \xrightarrow{d} 0$. | - |

---

### [Hab-04] Análisis de Jerarquía, Contraejemplos y Divergencia de Momentos (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 23: Análisis de Plim frente a Divergencia de Momentos
- **Prerequisites:** C-09
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 23), `EST3_LEC07_26.2_V2.pdf` (page 37)

#### Description & Cognitive Model
Aplicación de la jerarquía entre modos de convergencia ($m.s. \Rightarrow p \Rightarrow d$, $a.s. \Rightarrow p$ y el caso límite constante $X_n \xrightarrow{d} c \Rightarrow X_n \xrightarrow{p} c$) y evaluación formal de sucesiones con valores atípicos extremos y contraejemplos (como $X_n\in\{0,n^2\}$ o $X_n=-Z$) contrastando $\mathrm{plim}$ frente a momentos $L^1, L^2$.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Suma probabilidades erróneas | skipped_step | high | $\mathbb{P}(|X_n|>\varepsilon) = n^2/n = n$ | La probabilidad del evento $\{|X_n|>\varepsilon\}$ depende solo de la masa asignada a los valores fuera de la banda ($\mathbb{P}(X_n=n^2)=1/n$), no de su magnitud $n^2$. |
| `D-Hab04-02` | Olvida exponente en L2 | skipped_step | high | $\mathbb{E}[X_n^2] = n^2 \cdot (1/n) = n$ | Al evaluar el segundo momento de $X_n=n^2$, eleve primero el valor del soporte al cuadrado $(n^2)^2=n^4$ antes de multiplicar por su probabilidad $1/n$, obteniendo $n^3$. |
| `D-Hab04-03` | Confunde soporte con epsilon | conceptual_swap | high | $\mathbb{P}(X_n=0) = 1$ para $n$ finito | Fije primero $\varepsilon>0$ arbitrario y asegure que para todo $n$ suficientemente grande ($n^2>\varepsilon$) el único punto exterior a la banda es $X_n=n^2$. |
| `D-Hab04-04` | Varianza como segundo momento | conceptual_swap | high | $\operatorname{Var}(X_n)=\mathbb{E}[X_n^2]=n^3$ | El Error Cuadrático Medio respecto a $0$ es $\mathbb{E}[X_n^2]=n^3$, pero la varianza requiere restar la media al cuadrado: $\operatorname{Var}(X_n)=n^3-n^2=n^2(n-1)$. |
| `D-Hab04-05` | Supone E[Xn]=0 en {0,n} | conceptual_swap | high | Si $X_n\in\{0,n\}$, entonces $\mathbb{E}[X_n]\to 0$ | En la variante $X_n\in\{0,n\}$ con prob $1/n$, calcule el producto exacto $\mathbb{E}[X_n]=n\cdot(1/n)=1$ antes de tomar el límite cuando $n\to\infty$. |
| `D-Hab04-06` | Falla en igualdad L1 | conceptual_swap | high | $\mathbb{E}[|X_n|] \text{ diverge solo si } X_n<0$ | Dado que $X_n\in\{0,n^2\}$ es no negativa, $|X_n|=X_n$, por lo que $\mathbb{E}[|X_n|]=\mathbb{E}[X_n]=n\to +\infty$ y falla la convergencia en $L^1$. |
| `D-Hab04-07` | Generaliza d a p | skipped_step | high | $X_n \xrightarrow{d} X \Rightarrow X_n \xrightarrow{p} X$ para cualquier límite $X$ | Verifique si el límite es aleatorio: si $X$ no es constante, $\xrightarrow{d}$ no implica $\xrightarrow{p}$, pues $|-Z - Z| = 2|Z|$ no tiende a cero. |
| `D-Hab04-08` | Olvida excepción constante | conceptual_swap | high | $X_n \xrightarrow{d} c$ nunca implica $X_n \xrightarrow{p} c$ | Aplique el caso especial: cuando el límite es una constante $c$, toda la masa se concentra en un punto y $\xrightarrow{d}$ sí implica $\xrightarrow{p}$. |
| `D-Hab04-09` | Conecta m.s. con a.s. | skipped_step | high | $X_n \xrightarrow{m.s.} X \Rightarrow X_n \xrightarrow{a.s.} X$ directamente | Recuerde que ni $\xrightarrow{m.s.}$ implica $\xrightarrow{a.s.}$ ni $\xrightarrow{a.s.}$ implica $\xrightarrow{m.s.}$ en general; ambas implican $\xrightarrow{p}$ por vías distintas. |
| `D-Hab04-10` | Invierte p hacia m.s. | conceptual_swap | high | $X_n \xrightarrow{p} X \Rightarrow X_n \xrightarrow{m.s.} X$ | Recuerde que $\xrightarrow{m.s.}$ es más exigente porque controla colas mediante el segundo momento; $\xrightarrow{p}$ solo implica $\xrightarrow{d}$. |
| `D-Hab04-11` | Niega simetría normal | conceptual_swap | high | Si $Z \sim N(0,1)$, entonces $-Z$ no converge en distribución a $Z$ | Compare las distribuciones marginales: por simetría de la normal estándar, $-Z \sim N(0,1)$ igual que $Z$, de modo que $F_{X_n}(x) = F_Z(x)$ para todo $n$. |
| `D-Hab04-12` | Asume d más fuerte | conceptual_swap | high | La convergencia en distribución es la más exigente de todas | Ordene de mayor a menor exigencia: $\xrightarrow{m.s.}$ y $\xrightarrow{a.s.}$ implican $\xrightarrow{p}$, y $\xrightarrow{p}$ implica $\xrightarrow{d}$, siendo $\xrightarrow{d}$ la más débil. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Umbral arbitrario $\varepsilon>0$ fijo previo al paso al límite $n\to\infty$ | Permite identificar $\{|X_n|>\varepsilon\}=\{X_n=n^2\}$ para todo $n$ grande. | - |
| `A-Hab04-02` | - | Definición conjunta de $X_n$ y $X$ en el mismo espacio de probabilidad al evaluar $|X_n - X|$ para $\xrightarrow{p}$, $\xrightarrow{a.s.}$ o $\xrightarrow{m.s.}$ | Sin un espacio común no puede medirse la distancia $|X_n - X|$, mientras que $\xrightarrow{d}$ solo usa distribuciones marginales. | - |

---

### [C-11] Espacio de Probabilidad, Axiomas y Variable Aleatoria (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 13: Espacio Muestral, Axiomas de Kolmogorov y Regla de la Unión
- **Prerequisites:** None
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 13), `EST3_LEC07_26.2_V2.pdf` (page 15)

#### Description & Cognitive Model
Espacio de probabilidad $(\Omega,\mathcal{F},P)$ con axiomas de Kolmogorov y regla de la unión $P(A\cup B)=P(A)+P(B)-P(A\cap B)$, junto con la variable aleatoria $X:\Omega\to\mathbb{R}$, distinción entre $X$ y realización $x$, y distribución inducida $P(X=x)=P(\{\omega:X(\omega)=x\})$.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C11-01` | Suma sin restar intersección | conceptual_swap | high | $P(A\cup B)=P(A)+P(B)$ | Reste $P(A\cap B)$ porque los resultados comunes como el $6$ se cuentan dos veces al sumar $P(A)$ y $P(B)$. |
| `D-C11-02` | Confusión espacio muestral y muestra | conceptual_swap | high | $\Omega=\{y_1,\dots,y_n\}$ | Distinga el espacio muestral $\Omega$ (todos los resultados posibles) de la muestra (los datos concretos observados). |
| `D-C11-03` | Probabilidad mayor que uno | conceptual_swap | high | $P(A\cup B)>1$ | Verifique el primer axioma $0\le P(E)\le 1$: ninguna probabilidad válida puede superar $1$ ni ser negativa. |
| `D-C11-04` | Espacio total menor que uno | conceptual_swap | high | $P(\Omega)<1$ | Asegure el segundo axioma $P(\Omega)=1$, pues algún resultado dentro del espacio muestral debe ocurrir con certeza. |
| `D-C11-05` | Confusión unión e intersección | conceptual_swap | high | $P(A\cup B)=P(A\cap B)$ | Diferencie unión $A\cup B$ (ocurre al menos uno) de intersección $A\cap B$ (ocurren ambos simultáneamente). |
| `D-C11-06` | Producto en lugar de suma | conceptual_swap | high | $P(A\cup B)=P(A)P(B)$ | Sume probabilidades en la unión y reste la intersección; multiplicar corresponde a intersección bajo independencia. |
| `D-C11-07` | Confusión variable y realización | conceptual_swap | high | $X=x$ antes de observar | Separe $X$ (regla aleatoria antes de observar) de su realización $x$ (número concreto tras ejecutar el experimento). |
| `D-C11-08` | Asignación uniforme sin agrupar | conceptual_swap | high | $P(X=x)=\frac{1}{|\Omega|}$ | Agrupe todos los resultados $\omega$ que generan el mismo número $x$, por ejemplo $\{CS,SC\}$ suma $0.25+0.25=0.50$. |
| `D-C11-09` | Regla considerada aleatoria | conceptual_swap | high | La regla $X(\cdot)$ cambia en cada ensayo | Recuerde que la función $X$ es fija; lo aleatorio es qué resultado $\omega\in\Omega$ ocurre en cada realización. |
| `D-C11-10` | Dominio invertido en la función | conceptual_swap | high | $X:\mathbb{R}\to\Omega$ | Invierta la dirección: una variable aleatoria asigna a cada resultado $\omega\in\Omega$ un número real $x\in\mathbb{R}$. |
| `D-C11-11` | Suma de probabilidades distinta de uno | conceptual_swap | high | $\sum_x P(X=x)<1$ | Verifique que la suma de probabilidades inducidas sobre todos los valores posibles de $X$ sea exactamente $1$. |
| `D-C11-12` | Confusión valor $x$ con probabilidad | conceptual_swap | high | $P(X=x)=x$ | Distinga el soporte numérico $x$ de la probabilidad $P(X=x)\in[0,1]$ trasladada desde el espacio muestral $\Omega$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C11-01` | - | La colección de eventos $\mathcal{F}$ forma una $\sigma$-álgebra cerrada bajo uniones y complementos | Garantiza que $A\cup B$ y $A\cap B$ tengan probabilidad bien definida. | - |
| `A-C11-02` | - | Para todo $x\in\mathbb{R}$, el conjunto $\{\omega\in\Omega:X(\omega)\le x\}$ pertenece a $\mathcal{F}$ | Asegura que cada valor real tenga probabilidad medible bajo $P$. | - |

---

### [C-22] Ley de los Grandes Números (LGN) (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 40: Ley de los Grandes Números (LGN)
- **Prerequisites:** C-09, C-11
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 40)

#### Description & Cognitive Model
Consistencia del promedio muestral $\bar{Y}_n = \frac{1}{n}\sum_{i=1}^n Y_i \xrightarrow{p} \mu$ (ley débil) y $\bar{Y}_n \xrightarrow{a.s.} \mu$ (ley fuerte) para $Y_i$ i.i.d. con $E[Y_i]=\mu$ finita; con $\sigma^2<\infty$, $\operatorname{Var}(\bar{Y}_n)=\sigma^2/n \to 0$ implica convergencia en media cuadrática sin fijar ritmo ni distribución.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C22-01` | Confunde LGN con TCL | conceptual_swap | high | $\bar{Y}_n \xrightarrow{d} N(\mu, \sigma^2/n)$ es la LGN | Distinga LGN de TCL: la LGN solo garantiza convergencia del promedio hacia $\mu$, sin dar forma distribucional. |
| `D-C22-02` | Confunde con muestra finita | conceptual_swap | high | $\bar{y}_n = \mu$ para cualquier $n$ grande | Recuerde que el promedio muestral se aproxima al límite $\mu$ cuando $n \to \infty$, pero conserva error finito. |
| `D-C22-03` | Exige normalidad original | conceptual_swap | high | Solo vale si $Y_i \sim N(\mu, \sigma^2)$ | Verifique solo independencia, idéntica distribución y media finita $\mu$: la LGN no requiere normalidad de $Y_i$. |
| `D-C22-04` | Varianza constante | conceptual_swap | high | $\operatorname{Var}(\bar{Y}_n) = \sigma^2$ | Aplique la fórmula $\operatorname{Var}(\bar{Y}_n) = \sigma^2/n$: al crecer $n$, la dispersión del promedio colapsa a cero. |
| `D-C22-05` | Observación individual | conceptual_swap | high | $Y_i \xrightarrow{p} \mu$ | Diferencie cada dato individual $Y_i$ del promedio $\bar{Y}_n$: los errores se compensan solo al promediar. |
| `D-C22-06` | Invierte convergencia | conceptual_swap | high | $\mu \xrightarrow{p} \bar{Y}_n$ | Recuerde que $\mu$ es una constante fija y es el estimador aleatorio $\bar{Y}_n$ quien converge hacia $\mu$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C22-01` | - | Variables $Y_1,\dots,Y_n$ i.i.d. con media poblacional finita $E[Y_i]=\mu$ | Si la esperanza no es finita o hay dependencia fuerte, el promedio muestral puede no converger a $\mu$. | - |

---

### [C-23] Teorema Central del Límite (TCL) (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 42: Teorema Central del Límite (TCL)
- **Prerequisites:** C-22, C-09
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 42)

#### Description & Cognitive Model
Normalidad asintótica del promedio estandarizado $Z_n = \frac{\bar{Y}_n-\mu}{\sigma/\sqrt{n}} = \frac{\sqrt{n}(\bar{Y}_n-\mu)}{\sigma} \xrightarrow{d} N(0,1)$ y $\bar{Y}_n \stackrel{a}{\sim} N(\mu, \sigma^2/n)$ para $Y_i$ i.i.d. con $0<\sigma^2<\infty$, cualquiera sea la distribución original; el factor $\sqrt{n}$ compensa el encogimiento de $\bar{Y}_n-\mu$ a ritmo $1/\sqrt{n}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C23-01` | Omite factor raíz de n | conceptual_swap | high | $\frac{\bar{Y}_n-\mu}{\sigma} \xrightarrow{d} N(0,1)$ | Multiplique por $\sqrt{n}$ porque $\bar{Y}_n-\mu$ se encoge a ritmo $1/\sqrt{n}$; sin ese factor el límite colapsa a cero. |
| `D-C23-02` | Usa factor n lineal | conceptual_swap | high | $\frac{n(\bar{Y}_n-\mu)}{\sigma} \xrightarrow{d} N(0,1)$ | Use desviación estándar $\sigma/\sqrt{n}$ y no $\sigma/n$: la varianza de $\bar{Y}_n$ decrece con $n$, su desvío con $\sqrt{n}$. |
| `D-C23-03` | Normalidad de datos | conceptual_swap | high | $Y_i \stackrel{a}{\sim} N(\mu, \sigma^2)$ cuando $n$ crece | Distinga la distribución de cada observación $Y_i$ de la del promedio $\bar{Y}_n$: solo el promedio tiende a ser normal. |
| `D-C23-04` | Desviación en lugar de varianza | conceptual_swap | high | $\bar{Y}_n \stackrel{a}{\sim} N(\mu, \sigma/\sqrt{n})$ | Verifique la convención $N(\mu, \text{varianza})$: el segundo parámetro es $\sigma^2/n$ y no el error estándar. |
| `D-C23-05` | Confunde convergencia en prob. | conceptual_swap | high | $Z_n \xrightarrow{p} N(0,1)$ | Use convergencia en distribución ($\xrightarrow{d}$) en el TCL: $Z_n$ converge en forma hacia $N(0,1)$, no a un número. |
| `D-C23-06` | Ignora varianza finita | conceptual_swap | high | El TCL aplica siempre que $E[Y_i]=\mu$ exista | Exija siempre varianza positiva y finita ($0<\sigma^2<\infty$) además de la media para garantizar el límite normal. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C23-01` | - | Muestra i.i.d. con varianza poblacional finita y positiva $0<\sigma^2<\infty$ | Con varianza infinita o nula falla la estandarización hacia una distribución $N(0,1)$ no degenerada. | - |

---

### [Hab-15] Aproximación Normal, Error Estándar e Intervalos vía TCL (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 43: Aproximación Normal de Probabilidades Muestrales
- **Prerequisites:** C-23
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 43), `EST3_LEC07_26.2_V2.pdf` (page 44)

#### Description & Cognitive Model
Cálculo aproximado de probabilidades sobre promedios muestrales mediante $\bar{Y}_n \stackrel{a}{\sim} N(\mu, \sigma^2/n)$ evaluando asimetría residual, y aplicación del TCL a proporciones Bernoulli($p$) mediante $\hat{p} \stackrel{a}{\sim} N(p, p(1-p)/n)$, error estándar $ee(\hat{p})$, intervalo $IC_{95\%}: \hat{p}\pm 1.96\,ee(\hat{p})$ y dimensionamiento muestral.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab15-01` | Usa desviación poblacional | skipped_step | high | $Z = \frac{c-\mu}{\sigma}$ | Divida la desviación poblacional $\sigma$ por $\sqrt{n}$ antes de estandarizar $\bar{Y}_n$: el error estándar es $\sigma/\sqrt{n}$. |
| `D-Hab15-02` | Divide por n en vez de raíz | skipped_step | high | $Z = \frac{c-\mu}{\sigma/n}$ | Use $\sigma/\sqrt{n}$ en el denominador, no $\sigma/n$: la varianza de $\bar{Y}_n$ es $\sigma^2/n$ y su raíz es $\sigma/\sqrt{n}$. |
| `D-Hab15-03` | Cola izquierda en vez de derecha | conceptual_swap | high | $P(\bar{Y}_n > c) \approx \Phi(z)$ | Verifique el sentido de la desigualdad: para cola superior $P(Z > z)$ calcule $1 - \Phi(z)$, no $\Phi(z)$. |
| `D-Hab15-04` | Confunde varianza con desvío | conceptual_swap | high | $\sigma_{\bar{Y}} = \sigma^2/n$ | Extraiga la raíz cuadrada de la varianza $\sigma^2/n$ antes de dividir $(c-\mu)$ para estandarizar a $Z$. |
| `D-Hab15-05` | Ignora signo de diferencia | conceptual_swap | high | $Z = \frac{\mu - c}{\sigma/\sqrt{n}}$ | Reste siempre en orden $(\text{valor} - \text{media})$ para conservar el signo correcto del estadístico $Z$. |
| `D-Hab15-06` | Supone igualdad exacta | conceptual_swap | high | $P(\bar{Y}_n > c) = P(Z > z)$ exacto | Interprete el resultado del TCL como aproximación asintótica ($\approx$); con $n$ finito la asimetría deja un pequeño sesgo. |
| `D-Hab15-07` | Duplica n para mitad de error | skipped_step | high | $n' = 2n \Rightarrow ME' = ME/2$ | Como el margen decrece con $1/\sqrt{n}$, para reducirlo a la mitad debe cuadruplicar el tamaño de la muestra ($n'=4n$). |
| `D-Hab15-08` | Omite factor (1-p) | skipped_step | high | $ee(\hat{p}) = \sqrt{\hat{p}/n}$ | Use la varianza completa de una Bernoulli $\hat{p}(1-\hat{p})$ en el numerador antes de dividir por $n$ y sacar raíz. |
| `D-Hab15-09` | Olvida raíz cuadrada en ee | conceptual_swap | high | $ee(\hat{p}) = \frac{\hat{p}(1-\hat{p})}{n}$ | Aplique raíz cuadrada a la varianza muestral $\hat{p}(1-\hat{p})/n$ para obtener el error estándar antes de multiplicar por $1.96$. |
| `D-Hab15-10` | Omite 1.96 en el intervalo | conceptual_swap | high | $IC_{95\%} = \hat{p} \pm ee(\hat{p})$ | Multiplique el error estándar por el valor crítico $1.96$ (cuantil $0.975$ de $N(0,1)$) para obtener el $95\%$ de confianza. |
| `D-Hab15-11` | Error estándar en el numerador | conceptual_swap | high | $ee(\hat{p}) = \sqrt{n\,\hat{p}(1-\hat{p})}$ | Divida siempre por $n$ dentro de la raíz cuadrada: una muestra más grande reduce la varianza del estimador $\hat{p}$. |
| `D-Hab15-12` | Confunde proporción con suma | conceptual_swap | high | $\hat{p} \stackrel{a}{\sim} N(np, np(1-p))$ | Distinga el conteo de éxitos ($\sum Y_i$) de la proporción ($\hat{p} = \bar{Y}_n$): la media es $p$ y la varianza $p(1-p)/n$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab15-01` | - | Tamaño muestral $n$ suficientemente grande respecto a la asimetría de $Y_i$ | Si $n$ es pequeño y la distribución original es muy asimétrica, la aproximación normal difiere de la exacta. | - |
| `A-Hab15-02` | - | Observaciones Bernoulli i.i.d. con $n$ suficientemente grande y $p$ alejado de $0$ o $1$ | Si $np$ o $n(1-p)$ es muy pequeño, la aproximación normal de $\hat{p}$ pierde precisión. | - |

---

### [C-24] Teorema de la Aplicación Continua (CMT) (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 46: Teorema de la Aplicación Continua (CMT)
- **Prerequisites:** C-22
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 46)

#### Description & Cognitive Model
Invariancia de la convergencia ante transformaciones continuas: si $X_n \xrightarrow{p} c$ y $g$ es continua en $c$, entonces $g(X_n) \xrightarrow{p} g(c)$ ($\operatorname{plim} g(X_n) = g(\operatorname{plim} X_n)$), y análogamente $X_n \xrightarrow{d} X \Rightarrow g(X_n) \xrightarrow{d} g(X)$; a diferencia de la esperanza (Jensen), $\operatorname{plim}$ sí atraviesa funciones no lineales.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C24-01` | Aplica Jensen al plim | conceptual_swap | high | $\operatorname{plim} g(X_n) \neq g(\operatorname{plim} X_n)$ si $g$ es convexa | Distinga esperanza de límite en probabilidad: $E[g(X)] \neq g(E[X])$ por Jensen, pero $\operatorname{plim}$ sí pasa por $g$ continua. |
| `D-C24-02` | Confunde sesgo con inconsistencia | conceptual_swap | high | Todo estimador sesgado en $n$ finito es inconsistente | Recuerde que $s$ y $1/\bar{Y}$ son sesgados en muestras finitas, pero por el CMT siguen siendo consistentes para $\sigma$ y $1/\mu$. |
| `D-C24-03` | Ignora discontinuidad en el límite | conceptual_swap | high | $1/\bar{Y}_n \xrightarrow{p} 1/\mu$ incluso cuando $\mu = 0$ | Verifique que $g$ sea continua en el punto límite $c$: en $g(x)=1/x$ se requiere $\mu \neq 0$ para garantizar convergencia. |
| `D-C24-04` | Confunde esperanza con plim | conceptual_swap | high | $E[g(X_n)] = g(E[X_n])$ para $g$ continua | Restrinja la permutación con funciones no lineales al $\operatorname{plim}$ y a $\xrightarrow{d}$; la esperanza solo es lineal. |
| `D-C24-05` | Excluye convergencia en dist. | conceptual_swap | high | El CMT solo vale para $\xrightarrow{p}$, no para $\xrightarrow{d}$ | Aplique el CMT tanto a convergencia en probabilidad como en distribución: $X_n \xrightarrow{d} X$ implica $g(X_n) \xrightarrow{d} g(X)$. |
| `D-C24-06` | Exige linealidad de g | conceptual_swap | high | Solo vale para $g(x)=ax+b$ | Recuerde que el CMT solo exige continuidad de $g$ en el límite, por lo que abarca raíces, cocientes y potencias. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C24-01` | - | Continuidad de la función $g$ en el límite constante $c$ (o en el soporte de $X$) | Si $g$ presenta una discontinuidad en el límite (como $1/x$ en $0$), no se garantiza la convergencia. | - |

---

### [C-25] Teorema de Slutsky (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 48: Teorema de Slutsky
- **Prerequisites:** C-22, C-23
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 48)

#### Description & Cognitive Model
Combinación algebraica de convergencias asintóticas: si $B_n \xrightarrow{d} B$ y $A_n \xrightarrow{p} a$ donde $a$ es constante, entonces $A_n+B_n \xrightarrow{d} a+B$, $A_n B_n \xrightarrow{d} aB$ y $B_n/A_n \xrightarrow{d} B/a$ ($a \neq 0$); es indispensable que $A_n$ converja en probabilidad a una constante para sustituir parámetros desconocidos sin alterar la distribución límite.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C25-01` | Aplica con dos en distribución | conceptual_swap | high | $A_n \xrightarrow{d} A \land B_n \xrightarrow{d} B \Rightarrow A_n+B_n \xrightarrow{d} A+B$ | Exija que una de las dos sucesiones converja en probabilidad a una constante $a$: con dos en distribución falla la conjunta. |
| `D-C25-02` | Divide por constante nula | conceptual_swap | high | $B_n/A_n \xrightarrow{d} B/a$ para todo $a \in \mathbb{R}$ | Compruebe siempre que la constante límite del denominador cumpla $a \neq 0$ antes de aplicar el cociente de Slutsky. |
| `D-C25-03` | Asume convergencia en prob. | conceptual_swap | high | $A_n \xrightarrow{p} a \land B_n \xrightarrow{d} B \Rightarrow A_n B_n \xrightarrow{p} aB$ | Recuerde que al combinar $\xrightarrow{p}$ con $\xrightarrow{d}$ el modo resultante es convergencia en distribución ($\xrightarrow{d}$). |
| `D-C25-04` | Exige límite aleatorio en A | conceptual_swap | high | Si $A_n \xrightarrow{p} a$ constante, el producto se degenera | Entienda que la convergencia de $A_n$ a una constante $a$ es precisamente lo que permite tratarla como constante en el límite. |
| `D-C25-05` | Confunde con linealidad exacta | conceptual_swap | high | $B_n/A_n = B/a$ en muestras finitas | Distinga la igualdad exacta en muestra finita de la igualdad en distribución límite válida conforme $n \to \infty$. |
| `D-C25-06` | Exige independencia de An y Bn | conceptual_swap | high | Slutsky requiere $A_n$ independiente de $B_n$ | Recuerde que Slutsky no exige independencia entre $A_n$ y $B_n$ porque $A_n$ converge en probabilidad a una constante. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C25-01` | - | Convergencia en probabilidad de $A_n$ hacia una constante $a$ (con $a \neq 0$ en cocientes) | Si $A_n$ converge solo en distribución o hacia cero en un cociente, el límite combinado no está garantizado. | - |

---

### [Hab-17] Inferencia Asintótica con Varianza Desconocida (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 49: Inferencia Asintótica con Varianza Desconocida
- **Prerequisites:** C-24, C-25
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 49)

#### Description & Cognitive Model
Justificación y cálculo del contraste de hipótesis $H_0:\mu=\mu_0$ en muestras grandes no normales mediante la factorización $t = \frac{\bar{Y}-\mu_0}{s/\sqrt{n}} = \frac{\sigma}{s} \cdot \frac{\bar{Y}-\mu_0}{\sigma/\sqrt{n}} \xrightarrow{d} N(0,1)$, integrando el CMT ($\sigma/s \xrightarrow{p} 1$), el TCL bajo $H_0$, el Teorema de Slutsky y la decisión con valor crítico normal ($|t| > 1.96$ al $5\%$).

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab17-01` | Omite raíz de n en t | skipped_step | high | $t = \frac{\bar{y}-\mu_0}{s}$ | Divida $s$ entre $\sqrt{n}$ para obtener el error estándar $s/\sqrt{n}$ antes de calcular el estadístico de contraste $t$. |
| `D-Hab17-02` | Límite erróneo de sigma/s | skipped_step | high | $\frac{\sigma}{s} \xrightarrow{p} \sigma$ | Aplique el CMT a $s^2 \xrightarrow{p} \sigma^2$: como $s \xrightarrow{p} \sigma$, el cociente $\sigma/s$ converge en probabilidad a $1$. |
| `D-Hab17-03` | Rechaza por signo invertido | conceptual_swap | high | Rechaza $H_0$ si $|t| < 1.96$ | Compare correctamente contra la región crítica: se rechaza $H_0$ al $5\%$ bilateral solo cuando $|t| > 1.96$. |
| `D-Hab17-04` | Exige normalidad poblacional | conceptual_swap | high | No se puede usar tabla normal si $Y_i$ no es normal | Combine TCL y Slutsky: con $n$ grande, el estadístico $t$ es asintóticamente $N(0,1)$ aunque los datos no sean normales. |
| `D-Hab17-05` | Usa n en vez de s/raíz(n) | conceptual_swap | high | $t = \frac{\bar{y}-\mu_0}{s/n}$ | Use $\sqrt{n}=20$ en el denominador de $s/\sqrt{n}$, no $n=400$, acorde con el ritmo de convergencia del TCL. |
| `D-Hab17-06` | Olvida supuesto H0 | conceptual_swap | high | $Z_n \xrightarrow{d} N(0,1)$ sin asumir $H_0$ | Recuerde que $\frac{\bar{Y}-\mu_0}{\sigma/\sqrt{n}} \xrightarrow{d} N(0,1)$ solo se cumple bajo la hipótesis nula $\mu=\mu_0$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab17-01` | - | Estimador consistente $s^2 \xrightarrow{p} \sigma^2$ con $\sigma>0$ y tamaño muestral $n$ grande | Si $s$ no es consistente o $n$ es pequeño con datos asimétricos, el límite $N(0,1)$ de $t$ no es válido. | - |

---

### [Hab-18] Método Delta para Error Estándar e Intervalos (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 50: Método Delta para Error Estándar e Intervalos
- **Prerequisites:** C-23, C-24
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 50)

#### Description & Cognitive Model
Aplicación de la expansión de Taylor de primer orden $\sqrt{n}(g(\hat{\theta})-g(\theta)) \xrightarrow{d} N(0, [g'(\theta)]^2 V)$ para estimar funciones no lineales (como $g(m)=1/m$), calcular su error estándar $ee(g(\hat{\theta})) \approx |g'(\hat{\theta})| \cdot ee(\hat{\theta})$ y construir el intervalo $IC_{95\%} = g(\hat{\theta}) \pm 1.96\,ee(g(\hat{\theta}))$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab18-01` | Transforma directo el ee | skipped_step | high | $ee(g(\hat{\theta})) \approx g(ee(\hat{\theta}))$ | Multiplique $ee(\hat{\theta})$ por $|g'(\hat{\theta})|$, no evalúe $g$ sobre el error estándar: la derivada escala el desvío. |
| `D-Hab18-02` | Omite valor absoluto | skipped_step | high | $ee(g(\hat{\theta})) \approx g'(\hat{\theta}) \cdot ee(\hat{\theta})$ | Aplique valor absoluto a $g'(\hat{\theta})$ porque todo error estándar es no negativo y la varianza lleva $[g'(\theta)]^2$. |
| `D-Hab18-03` | Transforma extremos del IC | conceptual_swap | high | $IC_{95\%}(g(\theta)) = [g(L), g(U)]$ | Calcule el intervalo simétrico asintótico $g(\hat{\theta}) \pm 1.96\,|g'(\hat{\theta})|\,ee(\hat{\theta})$ usando el método delta. |
| `D-Hab18-04` | Eleva derivada sin variar | conceptual_swap | high | $ee(g(\hat{\theta})) \approx [g'(\hat{\theta})]^2 \cdot ee(\hat{\theta})$ | Distinga varianza de error estándar: $[g'(\hat{\theta})]^2$ multiplica a la varianza, mientras $|g'(\hat{\theta})|$ multiplica al $ee$. |
| `D-Hab18-05` | Deriva mal el cociente | conceptual_swap | high | Para $g(m)=1/m$, $g'(m) = 1/m$ | Calcule correctamente la derivada de $m^{-1}$: $g'(m) = -1/m^2$, por lo que en $m=2$ resulta $g'(2) = -0.25$. |
| `D-Hab18-06` | Aplica con derivada nula | conceptual_swap | high | El método delta funciona aunque $g'(\theta)=0$ | Verifique $g'(\theta) \neq 0$: si la primera derivada se anula, desaparece el término lineal y falla la aproximación. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab18-01` | - | Función $g$ derivable en $\theta$ con primera derivada no nula $g'(\theta) \neq 0$ | Si $g'(\theta)=0$, la expansión de primer orden colapsa a cero y se requieren términos de orden superior. | - |

---
