# Cognitive Task Analysis (CTA): Estadistica 3 S9 Vmapreduce Vlean43 V5

- **Course ID:** `estadistica_3_s9_vmapreduce_vlean43_v5`
- **Macro-Competency:** Dominio y aplicación analítica integral de Estadistica 3 S9 Vmapreduce Vlean43 V5
- **Structure:** 20 total competencies (0 Facts, 11 Concepts, 9 Skills) with 264 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Límites de Normalidad y Umbral Asintótico | Concept | Understand | Unidad 4: Límites de Normalidad y Umbral Asintótico | - | 6 |
| `C-02` | Muestra Aleatoria i.i.d., Estimador, Sesgo, Eficiencia y ECM | Concept | Understand | Unidad 5: Sesgo, Eficiencia Relativa y ECM | C-01 | 12 |
| `Hab-01` | Descomposición del ECM y Trade-off Sesgo-Varianza | Skill | Apply | Unidad 6: Descomposición Escalar y Matricial del ECM | C-02 | 12 |
| `Hab-02` | Momentos de Media y Cuasivarianza Muestral | Skill | Apply | Unidad 8: Momentos de Media y Cuasivarianza Muestral | C-02 | 12 |
| `C-03` | Sucesiones Aleatorias, Convergencia en Probabilidad y Consistencia | Concept | Understand | Unidad 10: Convergencia en Probabilidad y Consistencia Débil | C-01, C-02 | 18 |
| `Hab-03` | Convergencia en Media Cuadrática y Superconsistencia | Skill | Analyze | Unidad 12: Convergencia en Media Cuadrática y Superconsistencia | Hab-01, C-03 | 12 |
| `Hab-04` | Desigualdades de Markov y Chebyshev y Cotas Probabilísticas | Skill | Apply | Unidad 14: Demostración y Cota de la Desigualdad de Markov | C-03 | 30 |
| `C-04` | Desigualdad de Jensen y No Conmutatividad | Concept | Understand | Unidad 17: Desigualdad de Jensen y No Conmutatividad | - | 12 |
| `C-05` | Desigualdad de Cauchy-Schwarz y Correlación | Concept | Understand | Unidad 19: Desigualdad de Cauchy-Schwarz y Correlación | C-04 | 6 |
| `C-06` | Modos de Convergencia (a.s., d, Lr) y su Jerarquía | Concept | Understand | Unidad 20: Jerarquía de Convergencias Lr y Probabilidad | C-04, C-05, C-03, Hab-04 | 24 |
| `Hab-06` | Implicaciones Lr, No Reciprocidad y Diagnóstico Asintótico | Skill | Apply | Unidad 21: Demostración de Implicaciones Lr y Momentos | C-04, C-06 | 18 |
| `C-07` | Insesgadez vs. Consistencia de Estimadores | Concept | Analyze | Unidad 27: Insesgadez vs. Consistencia de Estimadores | C-06 | 12 |
| `Hab-08` | Cálculo de Esperanza, Varianza, Sesgo, ECM y Consistencia | Skill | Apply | Unidad 25: Cálculo de Varianza Exacta y ECM en Estimadores | C-07, C-02, Hab-04 | 30 |
| `H-01` | Espacio Muestral, Axiomas de Kolmogorov y Variable Aleatoria | Concept | Remember | Unidad 13: Espacio Muestral y Axiomas de Kolmogorov | - | 12 |
| `C-20` | Ley de los Grandes Números (LGN) | Concept | Understand | Unidad 40: Ley de los Grandes Números (LGN) | C-03, H-01 | 6 |
| `C-21` | Teorema Central del Límite (TCL) | Concept | Understand | Unidad 42: Teorema Central del Límite (TCL) | C-20, C-01, C-06 | 6 |
| `Hab-17` | Probabilidades Asintóticas e Inferencia de Proporciones con TCL | Skill | Apply | Unidad 43: Cálculo de Probabilidades Asintóticas con TCL | C-21 | 12 |
| `C-22` | Teoremas de la Aplicación Continua (CMT) y de Slutsky | Concept | Understand | Unidad 46: Teorema de la Aplicación Continua (CMT) | C-20 | 12 |
| `Hab-19` | Contraste Asintótico con Varianza Desconocida | Skill | Apply | Unidad 49: Contraste Asintótico con Varianza Desconocida | C-21, C-22 | 6 |
| `Hab-20` | Método Delta para Funciones No Lineales | Skill | Apply | Unidad 50: Método Delta para Funciones No Lineales | C-21, C-22 | 6 |

---

## Detailed Competency Specifications

### [C-01] Límites de Normalidad y Umbral Asintótico (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 4: Límites de Normalidad y Umbral Asintótico
- **Prerequisites:** None
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 4)

#### Description & Cognitive Model
Fragilidad del supuesto gaussiano en muestras finitas y dependencia de la velocidad de convergencia del TCL respecto a asimetría, curtosis leptocúrtica y precisión en colas extremas frente a la regla empírica $n \ge 30$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Regla universal n>=30 | conceptual_swap | high | $n \ge 30$ garantiza normalidad en cualquier muestra | Evalúe asimetría y curtosis poblacional: $n=30$ solo aproxima visualmente la $t$ pero falla con datos sesgados o colas pesadas. |
| `D-C01-02` | Convergencia uniforme | conceptual_swap | high | El centro $Z\approx 0$ y las colas convergen igual | Distinga centro y colas: el TCL aproxima rápido cerca de $\mu$, pero los términos de orden superior distorsionan las colas al $5\%$. |
| `D-C01-03` | Normalidad garantizada | conceptual_swap | high | Los errores reales siguen exactamente $\mathcal{N}(0,\sigma^2)$ | Reconozca la fragilidad del supuesto normal en PGD reales como ENAHO o BCRP y justifique la inferencia mediante teoría asintótica. |
| `D-C01-04` | Ignora outliers | conceptual_swap | high | Los valores atípicos no afectan el promedio si $n=30$ | Considere que en distribuciones leptocúrticas unos pocos valores extremos dominan la suma muestral y desaceleran la convergencia. |
| `D-C01-05` | Solo tamaño muestral | conceptual_swap | high | La tasa del TCL es independiente de los momentos | Incluya tercer y cuarto momento estandarizados junto al nivel $\alpha$ exigido para determinar cuándo la discrepancia en colas es tolerable. |
| `D-C01-06` | Confunde consistencia | conceptual_swap | high | Consistencia implica normalidad exacta en muestras finitas | Separe consistencia (concentración alrededor de $\theta$) de normalidad asintótica y distribución exacta en muestras finitas. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Existencia de momentos superiores finitos (asimetría y curtosis) | Sin ellos la velocidad de aproximación al TCL no queda acotada. | - |
| `A-C01-02` | - | Tolerancia explícita de error de tamaño en cola bajo $H_0$ | Sin umbral de tolerancia no hay criterio operativo para suficiencia de $n$. | - |

---

### [C-02] Muestra Aleatoria i.i.d., Estimador, Sesgo, Eficiencia y ECM (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 5: Sesgo, Eficiencia Relativa y ECM
- **Prerequisites:** C-01
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 5), `EST3_LEC07_26.2_V2.pdf` (page 3)

#### Description & Cognitive Model
Muestra aleatoria $Y_1,\dots,Y_n$ i.i.d. con distribución $F_Y$, distinción entre estimador $\hat{\theta}_n=T(Y_1,\dots,Y_n)$ y estimación puntual, y propiedades exactas en muestras finitas sin normalidad: $\mathrm{Sesgo}(\hat{\theta}_n)=\mathbb{E}[\hat{\theta}_n]-\theta$, insesgadez exacta, eficiencia relativa escalar y matricial ($\Delta\succeq \mathbf{0}$) y $\mathrm{ECM}(\hat{\theta}_n)=\mathbb{E}[(\hat{\theta}_n-\theta)^2]$.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Signo del sesgo | conceptual_swap | high | $\mathrm{Sesgo}(\hat{\theta}_n)=\theta-\mathbb{E}[\hat{\theta}_n]$ | Reste el parámetro verdadero a la esperanza del estimador: un valor positivo indica sobreestimación sistemática respecto a $\theta$. |
| `D-C02-02` | Confunde estimación | conceptual_swap | high | El sesgo se mide con el valor puntual $\hat{\theta}_n(y)-\theta$ | Diferencie estimador (variable aleatoria con distribución muestral) de estimación puntual y tome esperanza sobre todas las muestras. |
| `D-C02-03` | Insesgadez puntual | conceptual_swap | high | Basta que $\mathbb{E}[\hat{\theta}_n]=\theta$ para un $\theta_0$ específico | Exija que la igualdad $\mathbb{E}[\hat{\theta}_n]=\theta$ se cumpla idénticamente para todo $\theta$ en el espacio paramétrico $\Theta$. |
| `D-C02-04` | Eficiencia sin insesgadez | conceptual_swap | high | Menor varianza implica mejor estimador aunque sea sesgado | Restrinja la comparación de eficiencia relativa por varianza a estimadores insesgados; si hay sesgo compare mediante el ECM total. |
| `D-C02-05` | Matriz definida negativa | conceptual_swap | high | $\hat{\theta}_{1,n}$ es más eficiente si $\mathrm{Var}(\hat{\theta}_{1,n})-\mathrm{Var}(\hat{\theta}_{2,n})\succeq \mathbf{0}$ | Invierta la diferencia a $\mathrm{Var}(\hat{\theta}_{2,n})-\mathrm{Var}(\hat{\theta}_{1,n})\succeq \mathbf{0}$ para que $\mathbf{c}^\top\Delta\mathbf{c}\ge 0$ refleje menor varianza. |
| `D-C02-06` | ECM sin segundo momento | conceptual_swap | high | El ECM siempre existe sin exigir $\mathbb{E}[\hat{\theta}_n^2]<\infty$ | Verifique primero que el segundo momento $\mathbb{E}[\hat{\theta}_n^2]<\infty$ sea finito para garantizar existencia de varianza y ECM. |
| `D-C02-07` | Confunde estimador con estimación | conceptual_swap | high | $\hat{\theta}_n$ es un número fijo | Distinga el estimador (fórmula que es variable aleatoria) de la estimación (número concreto $1800$ obtenido en una muestra). |
| `D-C02-08` | Confunde estimador con parámetro | conceptual_swap | high | $\bar{Y}=\mu$ siempre | Recuerde que $\mu$ es el parámetro poblacional desconocido y $\bar{Y}$ es solo un estimador aleatorio que lo aproxima. |
| `D-C02-09` | Omite identidad distributiva | conceptual_swap | high | i.i.d. significa solo independientes | Incluya ambas condiciones de i.i.d.: las observaciones son independientes y comparten la misma distribución poblacional $F_Y$. |
| `D-C02-10` | Omite independencia muestral | conceptual_swap | high | i.i.d. significa solo igual distribución | Verifique independencia: en una muestra aleatoria i.i.d., conocer una observación $Y_i$ no aporta información sobre $Y_j$. |
| `D-C02-11` | Ignora dependencia del tamaño n | conceptual_swap | high | La distribución de $\hat{\theta}_n$ no cambia con $n$ | Observe el subíndice $n$ en $\hat{\theta}_n$: la fórmula y su distribución muestral cambian al variar el tamaño muestral. |
| `D-C02-12` | Confunde muestra con población | conceptual_swap | high | $n$ es el tamaño de la población | Diferencie los $n$ datos muestrales observados de la población completa descrita por $F_Y$ y el parámetro $\theta$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | Segundo momento finito del estimador $\mathbb{E}[\hat{\theta}_n^2]<\infty$ | Si diverge, ni la varianza ni el ECM están definidos. | - |
| `A-C02-02` | - | Muestreo aleatorio simple i.i.d. desde una distribución común $F_Y$ | Si hay dependencia o cambios de distribución entre individuos, se altera la distribución muestral de $\hat{\theta}_n$. | - |

---

### [Hab-01] Descomposición del ECM y Trade-off Sesgo-Varianza (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 6: Descomposición Escalar y Matricial del ECM
- **Prerequisites:** C-02
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 6), `EST3_LEC07_26.2_V2.pdf` (page 9)

#### Description & Cognitive Model
Derivación y cálculo de $\mathrm{ECM}(\hat{\theta}_n)=\mathrm{Var}(\hat{\theta}_n)+[\mathrm{Sesgo}(\hat{\theta}_n)]^2$ y su extensión matricial $\mathrm{Var}(\hat{\theta}_n)+\mathrm{Sesgo}(\hat{\theta}_n)\mathrm{Sesgo}(\hat{\theta}_n)^\top$ sumando y restando $\mathbb{E}[\hat{\theta}_n]$, junto con el análisis del trade-off sesgo-varianza para comparar estimadores.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Suma lineal sesgo | skipped_step | high | $\mathrm{ECM}(\hat{\theta}_n)=\mathrm{Var}(\hat{\theta}_n)+\mathrm{Sesgo}(\hat{\theta}_n)$ | Eleve al cuadrado el sesgo al expandir el binomio alrededor de $\mathbb{E}[\hat{\theta}_n]$: el ECM mide distancia cuadrática, siempre no negativa. |
| `D-Hab01-02` | Conserva término cruzado | skipped_step | high | $\mathrm{ECM}=\mathrm{Var}+2\,\mathrm{Sesgo}+\mathrm{Sesgo}^2$ | Aplique linealidad al desvío centrado: $\mathbb{E}[\hat{\theta}_n-\mathbb{E}[\hat{\theta}_n]]=0$, lo que anula idénticamente el término cruzado central. |
| `D-Hab01-03` | Desviación estándar | conceptual_swap | high | $\mathrm{ECM}(\hat{\theta}_n)=\sqrt{\mathrm{Var}(\hat{\theta}_n)}+\mathrm{Sesgo}(\hat{\theta}_n)^2$ | Identifique el primer sumando $\mathbb{E}[(\hat{\theta}_n-\mathbb{E}[\hat{\theta}_n])^2]$ como la varianza exacta, no como su raíz cuadrada. |
| `D-Hab01-04` | Producto interno escalar | skipped_step | high | $\mathrm{ECM}=\mathrm{Var}(\hat{\theta}_n)+\mathrm{Sesgo}^\top\mathrm{Sesgo}$ | Respete las dimensiones matriciales $k\times k$ usando el producto exterior $\mathrm{Sesgo}(\hat{\theta}_n)\mathrm{Sesgo}(\hat{\theta}_n)^\top$ en el caso multivariado. |
| `D-Hab01-05` | Resta sesgo cuadrado | conceptual_swap | high | $\mathrm{ECM}(\hat{\theta}_n)=\mathrm{Var}(\hat{\theta}_n)-[\mathrm{Sesgo}(\hat{\theta}_n)]^2$ | Sume ambos componentes no negativos: el sesgo siempre penaliza e incrementa el ECM por encima de la varianza del estimador. |
| `D-Hab01-06` | Trata theta aleatoria | conceptual_swap | high | $\mathbb{E}[\hat{\theta}_n-\theta]$ depende de una $\theta$ aleatoria | Trate tanto a $\theta$ como a $\mathbb{E}[\hat{\theta}_n]$ como constantes determinísticas para extraer $\mathbb{E}[\hat{\theta}_n]-\theta$ fuera de la esperanza. |
| `D-Hab01-07` | No eleva el sesgo al cuadrado | skipped_step | high | $\text{ECM}(\hat{\theta})=\text{Var}(\hat{\theta})+\text{Sesgo}(\hat{\theta})$ | Eleve el sesgo al cuadrado en $\text{ECM}=\text{Var}+[\text{Sesgo}]^2$; un sesgo negativo nunca puede reducir el ECM. |
| `D-Hab01-08` | Usa error estándar en vez de varianza | conceptual_swap | high | $\text{ECM}=ee(\hat{\theta})+[\text{Sesgo}]^2$ | Sume la varianza $\text{Var}(\hat{\theta})$, no su raíz cuadrada $ee(\hat{\theta})$, para mantener consistencia cuadrática. |
| `D-Hab01-09` | Rechaza todo estimador sesgado | conceptual_swap | high | Insesgado siempre tiene menor ECM | Compare el $\text{ECM}$ total: un estimador con ligero sesgo puede lograr menor distancia cuadrática promedio si reduce mucho la varianza. |
| `D-Hab01-10` | Suma término cruzado no nulo | skipped_step | high | $\text{ECM}=\text{Var}+[\text{Sesgo}]^2+2\text{Var}\cdot\text{Sesgo}$ | Observe que $2(E[\hat{\theta}]-\theta)E[\hat{\theta}-E[\hat{\theta}]]=0$ porque $E[\hat{\theta}-E[\hat{\theta}]]=0$. |
| `D-Hab01-11` | Resta el sesgo al cuadrado | conceptual_swap | high | $\text{ECM}=\text{Var}-[\text{Sesgo}]^2$ | Sume ambos componentes positivos: tanto la varianza como $[\text{Sesgo}]^2$ penalizan el error cuadrático medio. |
| `D-Hab01-12` | Elige mayor ECM como mejor | conceptual_swap | high | Mayor ECM indica mejor estimador | Recuerde que el ECM mide error cuadrático promedio al parámetro verdadero; por tanto, menor ECM significa mejor estimador. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Linealidad del operador esperanza matemática | Sin linealidad no se separan varianza, término cruzado y sesgo. | - |
| `A-Hab01-02` | - | Existencia de segundo momento finito $E[\hat{\theta}^2]<\infty$ | Si el segundo momento del estimador diverge, el ECM es infinito y no admite descomposición finita. | - |

---

### [Hab-02] Momentos de Media y Cuasivarianza Muestral (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 8: Momentos de Media y Cuasivarianza Muestral
- **Prerequisites:** C-02
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 8), `EST3_LEC07_26.2_V2.pdf` (page 11)

#### Description & Cognitive Model
Cálculo exacto sin normalidad en muestras i.i.d. de $\mathbb{E}[\bar{Y}_n]=\mu$, $\mathrm{Var}(\bar{Y}_n)=\sigma^2/n$, cuasivarianza insesgada $\mathbb{E}[S_n^2]=\sigma^2$ con $n-1$ grados de libertad y varianza muestral $\mathbb{E}[m_2]=\frac{n-1}{n}\sigma^2$ (sesgada en muestras finitas pero asintóticamente insesgada).

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Constante lineal varianza | skipped_step | high | $\mathrm{Var}(\bar{Y}_n)=\frac{1}{n}\mathrm{Var}(\sum Y_i)=\sigma^2$ | Aplique la propiedad cuadrática $\mathrm{Var}(cX)=c^2\mathrm{Var}(X)$ para obtener $1/n^2$ multiplicando a $n\sigma^2$, resultando $\sigma^2/n$. |
| `D-Hab02-02` | Suma signos cruzados | skipped_step | high | $\sum (Y_i-\bar{Y}_n)^2=\sum (Y_i-\mu)^2+n(\bar{Y}_n-\mu)^2$ | Simplifique $-2n(\bar{Y}_n-\mu)^2+n(\bar{Y}_n-\mu)^2=-n(\bar{Y}_n-\mu)^2$: centrar en $\bar{Y}_n$ siempre reduce la suma de cuadrados. |
| `D-Hab02-03` | Omite grados de libertad | skipped_step | high | $\mathbb{E}[\sum (Y_i-\bar{Y}_n)^2]=n\sigma^2$ por lo que $m_2$ es insesgado | Reste el grado de libertad consumido $-n(\sigma^2/n)=-\sigma^2$ al estimar $\mu$ con $\bar{Y}_n$, obteniendo $(n-1)\sigma^2$. |
| `D-Hab02-04` | Requiere normalidad | conceptual_swap | high | $\mathbb{E}[S_n^2]=\sigma^2$ solo vale bajo $Y_i\sim\mathcal{N}(\mu,\sigma^2)$ | Note que la demostración solo usa i.i.d. con media y varianza finitas; la normalidad no interviene en ninguno de los cuatro momentos. |
| `D-Hab02-05` | Covarianzas no nulas | conceptual_swap | high | $\mathrm{Var}(\sum Y_i)=\sum \mathrm{Var}(Y_i)+\sum_{i\neq j}\sigma^2$ | Anule $\mathrm{Cov}(Y_i,Y_j)=0$ para todo $i\neq j$ usando el supuesto de independencia mutua de la muestra aleatoria simple. |
| `D-Hab02-06` | Sesgo persistente m2 | conceptual_swap | high | El sesgo de $m_2$ no desaparece cuando $n\to\infty$ | Tome el límite de $\mathbb{E}[m_2]=\sigma^2-\sigma^2/n$: cuando $n\to\infty$ el sesgo $-\sigma^2/n\to 0$ y $m_2$ es asintóticamente insesgado. |
| `D-Hab02-07` | Divide entre n para insesgadez | skipped_step | high | $E[m_2]=\sigma^2$ | Divida la suma de cuadrados entre $n-1$ para obtener $s^2=20/3=6.67$, corrigiendo el grado de libertad gastado en $\bar{Y}$. |
| `D-Hab02-08` | Confunde dirección del sesgo de m2 | conceptual_swap | high | $E[m_2]=\frac{n+1}{n}\sigma^2$ | Recuerde que los desvíos respecto a $\bar{Y}$ son menores que respecto a $\mu$; por ello $m_2$ subestima $\sigma^2$ con $E[m_2]=\frac{n-1}{n}\sigma^2$. |
| `D-Hab02-09` | No resta la media en desvíos | skipped_step | high | $s^2=\frac{1}{n-1}\sum Y_i^2$ | Reste primero la media muestral $\bar{Y}$ a cada observación antes de elevar al cuadrado los desvíos $(Y_i-\bar{Y})^2$. |
| `D-Hab02-10` | Olvida elevar al cuadrado desvíos | conceptual_swap | high | $s^2=\frac{1}{n-1}\sum(Y_i-\bar{Y})$ | Eleve al cuadrado cada desvío $(Y_i-\bar{Y})^2$; la suma lineal de desvíos respecto a la media siempre es cero. |
| `D-Hab02-11` | Confunde sesgo finito con asintótico | conceptual_swap | high | $m_2$ mantiene sesgo $-0.25\sigma^2$ para todo $n$ | Evalúe el sesgo $-\sigma^2/n$: aunque para $n=4$ es $-25\%$, tiende a $0$ cuando $n\to\infty$ (asintóticamente insesgado). |
| `D-Hab02-12` | Divide suma por n-2 | conceptual_swap | high | $s^2=\frac{1}{n-2}\sum(Y_i-\bar{Y})^2$ | Reste solo $1$ grado de libertad al estimar únicamente $\mu$ mediante $\bar{Y}$, dividiendo entre $n-1$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Muestra aleatoria simple i.i.d. con $n\ge 2$ y $\sigma^2<\infty$ | Sin independencia mutua aparecen covarianzas cruzadas no nulas. | - |
| `A-Hab02-02` | - | Tamaño muestral $n\ge 2$ con observaciones i.i.d. y $\sigma^2<\infty$ | Si $n=1$, el denominador $n-1$ se anula y la cuasivarianza $s^2$ queda indeterminada. | - |

---

### [C-03] Sucesiones Aleatorias, Convergencia en Probabilidad y Consistencia (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 10: Convergencia en Probabilidad y Consistencia Débil
- **Prerequisites:** C-01, C-02
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 10), `EST3_LEC07_26.2_V2.pdf` (page 19), `EST3_LEC07_26.2_V2.pdf` (page 27)

#### Description & Cognitive Model
Sucesión de variables aleatorias $\{X_n\}_{n=1}^\infty$ indexada por $n$, definición de convergencia en probabilidad $X_n \xrightarrow{p} c$ ($\lim_{n\to\infty} P(|X_n - c| > \varepsilon) = 0$ para todo $\varepsilon > 0$) y $X_n \xrightarrow{p} X$, junto con el criterio de consistencia débil $\mathrm{plim}_{n\to\infty}\hat{\theta}_n=\theta$.

#### Fused Distractor Models (18)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Límite determinístico | conceptual_swap | high | $X_n \xrightarrow{p} c$ equivale a $|X_n(\omega)-c|<\varepsilon$ para todo $\omega$ | Recuerde que $X_n$ es una sucesión de distribuciones: se exige que la probabilidad fuera de la banda $2\varepsilon$ tienda a cero, no imposibilidad. |
| `D-C03-02` | Colapso hacia X | conceptual_swap | high | Si $X_n \xrightarrow{p} X$, la distribución de $X_n$ colapsa en un punto | Distinga límite constante (masa puntual en $c$) de variable aleatoria $X$ (realizaciones $X_n(\omega)$ y $X(\omega)$ cercanas en el mismo espacio). |
| `D-C03-03` | Igualdad exacta | conceptual_swap | high | Consistencia exige $\lim_{n\to\infty}\mathbb{P}(\hat{\theta}_n=\theta)=1$ | Use la banda cerrada $|X_n-c|\le\varepsilon$ para todo $\varepsilon>0$, ya que en variables continuas $\mathbb{P}(X_n=c)=0$ para todo $n$. |
| `D-C03-04` | Solo un epsilon | conceptual_swap | high | Basta comprobar $\lim_{n\to\infty}\mathbb{P}(|X_n-c|>0.05)=0$ | Verifique la condición para todo $\varepsilon>0$ arbitrariamente pequeño, de modo que la masa se concentre en cualquier vecindad de $c$. |
| `D-C03-05` | Consistencia vs insesgadez | conceptual_swap | high | Todo estimador insesgado es consistente y viceversa | Diferencie insesgadez en muestras finitas (propiedad de la media) de consistencia (concentración de toda la distribución cuando $n\to\infty$). |
| `D-C03-06` | Para un solo theta | conceptual_swap | high | $\hat{\theta}_n$ es consistente si converge en probabilidad solo en $\theta=0$ | Exija convergencia en probabilidad $\lim_{n\to\infty}\mathbb{P}(\|\hat{\theta}_n-\theta\|>\varepsilon)=0$ para todo $\theta$ del espacio paramétrico $\Theta$. |
| `D-C03-07` | Confunde sucesión aleatoria con numérica | conceptual_swap | high | Cada $X_n$ es un número determinista | Recuerde que cada término $X_n$ es una variable aleatoria; por ello existen distintos sentidos de convergencia al crecer $n$. |
| `D-C03-08` | Confunde término $X_n$ con sucesión | conceptual_swap | high | $X_n$ y $\{X_n\}_{n=1}^\infty$ son lo mismo | Distinga un término específico $X_n$ (para tamaño $n$ fijo) de la sucesión completa $\{X_n\}_{n=1}^\infty$ al variar $n$. |
| `D-C03-09` | Asume peso constante de cada dato | conceptual_swap | high | Cada nuevo dato pesa igual al crecer $n$ | Note que cada dato nuevo pesa $1/n$ en el promedio $\bar{Y}_n$, por lo que las fluctuaciones se atenúan al crecer $n$. |
| `D-C03-10` | Confunde índice n con valor de Y | conceptual_swap | high | $n$ es el valor observado de la variable | Diferencie la observación individual $Y_i$ del término $X_n=\bar{Y}_n$ calculado sobre las primeras $n$ observaciones. |
| `D-C03-11` | Ignora necesidad de modos de convergencia | conceptual_swap | high | Solo hay una definición posible de límite para $\{X_n\}$ | Reconozca que como cada $X_n$ es aleatorio, definir hacia dónde se estabiliza $\{X_n\}$ requiere modos probabilísticos de convergencia. |
| `D-C03-12` | Asume estabilización sin nuevos datos | conceptual_swap | high | $\bar{Y}_n$ converge con $n$ fijo | La estabilización asintótica ocurre al incorporar más observaciones ($n\to\infty$), reduciendo el peso $1/n$ de cada nueva realización. |
| `D-C03-13` | Convergencia determinista | conceptual_swap | high | $X_n \xrightarrow{p} c$ significa que $|X_n - c| \to 0$ para todo resultado | Recuerde que $X_n$ es aleatoria: lo que converge a cero no es cada realización individual sino la probabilidad de desviarse más de $\epsilon$. |
| `D-C03-14` | Epsilon fijo único | conceptual_swap | high | Basta que $P(|X_n - c| > 1) \to 0$ para tener convergencia en probabilidad | Exija que la probabilidad de error tienda a cero para todo margen $\epsilon > 0$ arbitrariamente pequeño, no solo para un valor particular. |
| `D-C03-15` | Invierte sentido de desigualdad | conceptual_swap | high | $\lim_{n\to\infty} P(|X_n - c| \le \epsilon) = 0$ | Verifique que la masa de probabilidad debe concentrarse dentro de $(c-\epsilon, c+\epsilon)$, es decir $P(|X_n-c|\le \epsilon) \to 1$ y $P(|X_n-c|>\epsilon) \to 0$. |
| `D-C03-16` | Confunde estimador con parámetro | conceptual_swap | high | Un estimador consistente converge a la media muestral fija | Note que un estimador es consistente respecto al parámetro poblacional verdadero $\theta$ cuando $n$ crece, no respecto a una muestra finita particular. |
| `D-C03-17` | Confunde con insesgadez | conceptual_swap | high | Consistencia equivale a que $E[\hat{\theta}_n] = \theta$ | Distinga acertar en promedio con $n$ fijo (insesgadez) de concentrar toda la distribución alrededor de $\theta$ al crecer $n$ (consistencia). |
| `D-C03-18` | Confunde cota no nula con falla | conceptual_swap | high | Si la cota de Chebyshev en $n=25$ es $1$, el estimador es inconsistente | Evalúe el límite de la cota cuando $n \to \infty$, no en un tamaño muestral pequeño: $\lim_{n\to\infty} \sigma^2/(n\epsilon^2) = 0$ basta para consistencia. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Variables definidas sobre un mismo espacio $(\Omega,\mathcal{F},\mathbb{P})$ | Sin espacio común no está definida la diferencia $X_n-X$. | - |
| `A-C03-02` | - | Definición consistente de los estimadores $\{X_n\}_{n=1}^\infty$ bajo el mismo esquema poblacional | Si cambia el experimento subyacente en cada $n$, la sucesión no describe el comportamiento asintótico de un mismo estimador. | - |
| `A-C03-03` | - | Sucesión de variables aleatorias $\{X_n\}_{n\ge 1}$ indexada por tamaño muestral $n$ | Sin definir cómo cambia el estimador al crecer $n$, no tiene sentido el límite $\text{plim}$. | - |

---

### [Hab-03] Convergencia en Media Cuadrática y Superconsistencia (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 12: Convergencia en Media Cuadrática y Superconsistencia
- **Prerequisites:** Hab-01, C-03
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 12), `EST3_LEC07_26.2_V2.pdf` (page 29)

#### Description & Cognitive Model
Aplicación del criterio de convergencia en media cuadrática $L^2$ ($X_n \xrightarrow{\mathrm{m.s.}} c \Leftrightarrow \mathbb{E}[(X_n-c)^2]\to 0 \Leftrightarrow \mathbb{E}[X_n]\to c$ y $\mathrm{Var}(X_n)\to 0$), su implicación a convergencia en probabilidad vía Markov y análisis de velocidad superconsistente $\mathcal{O}(1/n^2)$ en estadísticos de orden extremos como $X_{(1)}\sim\mathrm{Exp}(n\theta)$.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Solo insesgadez asintótica | skipped_step | high | Basta $\lim_{n\to\infty}\mathbb{E}[X_n]=c$ para que $X_n \xrightarrow{\mathrm{m.s.}} c$ | Verifique ambas condiciones simultáneas del Teorema 3.4: la varianza también debe colapsar a cero para que el ECM tienda a cero. |
| `D-Hab03-02` | Mínimo sigue Exp(theta) | skipped_step | high | $X_{(1)}=\min\{X_i\}$ mantiene distribución $\mathrm{Exp}(\theta)$ | Calcule la supervivencia conjunta $\mathbb{P}(X_{(1)}>t)=\prod e^{-\theta t}=e^{-n\theta t}$ para identificar el parámetro escalado $\lambda_n=n\theta$. |
| `D-Hab03-03` | Tasa estándar 1/n | skipped_step | high | La varianza de $X_{(1)}$ decae a tasa $\mathcal{O}(1/n)$ igual que $\bar{X}_n$ | Eleve al cuadrado el parámetro escalado $n\theta$ en la varianza exponencial $1/\lambda_n^2$, obteniendo $\mathrm{Var}(X_{(1)})=1/(n^2\theta^2)$. |
| `D-Hab03-04` | Complemento invertido | conceptual_swap | high | $\mathbb{P}(X_{(1)}>t)=1-\prod \mathbb{P}(X_i\le t)$ se usa como producto directo | Use intersección y no unión: el mínimo supera $t$ si y solo si todas las observaciones de la muestra superan simultáneamente $t$. |
| `D-Hab03-05` | Momento Lr infinito | conceptual_swap | high | $X_n \xrightarrow{L^r} X$ se define aunque $\mathbb{E}[|X_n|^r]=\infty$ | Compruebe la finitud de los momentos absolutos $\mathbb{E}[|X_n|^r]<\infty$ y $\mathbb{E}[|X|^r]<\infty$ antes de evaluar la norma $L^r$. |
| `D-Hab03-06` | Criterio solo suficiente | conceptual_swap | high | $\mathbb{E}[X_n]\to c$ y $\mathrm{Var}(X_n)\to 0$ no son necesarios para $L^2$ | Acote cada sumando no negativo por $\mathrm{ECM}(X_n)$ y aplique el teorema del sándwich para demostrar la necesidad de ambas condiciones. |
| `D-Hab03-07` | Omite varianza en ECM | conceptual_swap | high | $E[X_n] \to c$ basta para que $X_n \xrightarrow{m.s.} c$ | Exija tanto que el sesgo tienda a cero ($E[X_n] \to c$) como que la varianza se anule ($\text{Var}(X_n) \to 0$), pues $\text{ECM}=\text{Var}+\text{Sesgo}^2$. |
| `D-Hab03-08` | Omite sesgo en ECM | conceptual_swap | high | $\text{Var}(X_n) \to 0$ basta para converger en media cuadrática a $c$ | Compruebe también que el sesgo desaparece ($E[X_n] \to c$): si la varianza cae a cero pero el sesgo persiste en $3$, converge a $\mu+3$ y no a $\mu$. |
| `D-Hab03-09` | Invierte implicación con plim | conceptual_swap | high | $X_n \xrightarrow{p} c \Rightarrow X_n \xrightarrow{m.s.} c$ | Recuerde que Markov sobre $(X_n-c)^2$ prueba $\xrightarrow{m.s.} \Rightarrow \xrightarrow{p}$, pero el recíproco falla si existen colas raras muy pesadas. |
| `D-Hab03-10` | Suma sesgo sin cuadrado | conceptual_swap | high | $E[(X_n - c)^2] = \text{Var}(X_n) + \text{Sesgo}(X_n)$ | Eleve el sesgo al cuadrado en la descomposición $\text{ECM} = \text{Var}(X_n) + (E[X_n]-c)^2$ para garantizar términos no negativos. |
| `D-Hab03-11` | Aplica Markov sin cuadrado | conceptual_swap | high | $P(|X_n-c|>\epsilon) \le E[X_n-c]/\epsilon$ | Aplique Markov a la variable no negativa $(X_n-c)^2$ con umbral $\epsilon^2$, obteniendo el cociente $\text{ECM}/\epsilon^2 \to 0$. |
| `D-Hab03-12` | Confunde esperanza con convergencia | conceptual_swap | high | $E[X_n] \to c$ equivale a $E[|X_n-c|] \to 0$ | No confunda el cuadrado del sesgo $(E[X_n]-c)^2$ con el error cuadrático medio $E[(X_n-c)^2]$ que además incluye $\text{Var}(X_n)$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | Varianza finita $\mathrm{Var}(X_n)<\infty$ y parámetro fijo $\theta>0$ | Sin varianza finita no aplica la descomposición del ECM. | - |
| `A-Hab03-02` | - | Existencia de segundos momentos $E[X_n^2] < \infty$ para todo $n$ | Si $X_n$ no tiene varianza finita, la convergencia en media cuadrática ni siquiera está definida. | - |

---

### [Hab-04] Desigualdades de Markov y Chebyshev y Cotas Probabilísticas (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 14: Demostración y Cota de la Desigualdad de Markov
- **Prerequisites:** C-03
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 14), `Clases_sintetizadas_semana_9.pdf` (page 16), `EST3_LEC07_26.2_V2.pdf` (page 21), `EST3_LEC07_26.2_V2.pdf` (page 23), `EST3_LEC07_26.2_V2.pdf` (page 24)

#### Description & Cognitive Model
Derivación y aplicación de cotas probabilísticas libres de distribución: desigualdad de Markov $\mathbb{P}(Y\ge\delta)\le \mathbb{E}[Y]/\delta$ ($Y\ge 0$, $\delta>0$) y desigualdad de Chebyshev generalizada $\mathbb{P}(|X-c|\ge\varepsilon)\le \mathbb{E}[|X-c|^r]/\varepsilon^r$ y clásica $\mathbb{P}(|X-\mu|\ge\varepsilon)\le \mathrm{Var}(X)/\varepsilon^2$ ($\mathbb{P}(|X-\mu|\ge k\sigma)\le 1/k^2$), contrastando dichas cotas frente a valores exactos bajo normalidad.

#### Fused Distractor Models (30)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Aplica a Y negativa | skipped_step | high | Markov vale para cualquier $Y\in\mathbb{R}$ sin restricción de signo | Exija $Y\ge 0$ casi seguramente: si $Y$ toma valores negativos, $\mathbb{E}[Y|Y<\delta]$ puede ser negativa y no puede descartarse. |
| `D-Hab04-02` | Invierte cota condicional | skipped_step | high | $\mathbb{E}[Y|Y\ge\delta]\le\delta$ en la partición superior | Aplique monotonía de la esperanza sobre $\{Y\ge\delta\}$: como todo valor del subuniverso es al menos $\delta$, su promedio cumple $\mathbb{E}[Y|Y\ge\delta]\ge\delta$. |
| `D-Hab04-03` | Invierte desigualdad final | conceptual_swap | high | $\mathbb{P}(Y\ge\delta)\ge \mathbb{E}[Y]/\delta$ | Conserve el sentido correcto $\mathbb{E}[Y]\ge \delta\mathbb{P}(Y\ge\delta)$ al descartar el sumando no negativo y divida entre $\delta>0$. |
| `D-Hab04-04` | Omite factor delta | skipped_step | high | $\int_{\delta}^{\infty} y f_Y(y)\,dy \ge \int_{\delta}^{\infty} f_Y(y)\,dy$ | Mantenga la constante $\delta>0$ al acotar $y f_Y(y)\ge \delta f_Y(y)$ sobre $[\delta,\infty)$ para obtener $\delta\,\mathbb{P}(Y\ge\delta)$. |
| `D-Hab04-05` | Cota con delta<=0 | conceptual_swap | high | La cota sigue siendo válida para $\delta=0$ o $\delta<0$ | Exija $\delta>0$ estricto para que la división por $\delta$ esté definida y preserve el sentido de la desigualdad. |
| `D-Hab04-06` | Cambia por igualdad | conceptual_swap | high | $\mathbb{P}(Y\ge\delta)=\mathbb{E}[Y]/\delta$ si $Y$ es continua | Recuerde que se descarta la integral $\int_0^\delta y f_Y(y)\,dy\ge 0$ y se reemplaza $y$ por $\delta$, produciendo una cota superior gruesa. |
| `D-Hab04-07` | Denominador sin potencia | skipped_step | high | $\mathbb{P}(|X-\mu|\ge\varepsilon)\le \mathrm{Var}(X)/\varepsilon$ | Transforme ambos lados del evento mediante $h(u)=u^r$, definiendo el umbral $\delta=\varepsilon^r$ (o $\varepsilon^2$ cuando $r=2$) en el denominador. |
| `D-Hab04-08` | Desviación estándar arriba | conceptual_swap | high | $\mathbb{P}(|X-\mu|\ge\varepsilon)\le \sigma/\varepsilon^2$ | Calcule $\mathbb{E}[|X-\mu|^2]=\mathrm{Var}(X)=\sigma^2$ en el numerador para mantener coherencia cuadrática con $\varepsilon^2$. |
| `D-Hab04-09` | Falla por r<=0 | skipped_step | high | La transformación $u\mapsto u^r$ preserva la desigualdad para todo $r\in\mathbb{R}$ | Verifique $h'(u)=ru^{r-1}>0$ para $r>0$: solo cuando $r>0$ la potencia es estrictamente creciente en $[0,\infty)$ y preserva eventos. |
| `D-Hab04-10` | Omite valor absoluto | conceptual_swap | high | $\mathbb{P}(X-\mu\ge\varepsilon)\le \mathrm{Var}(X)/\varepsilon^2$ requiere $X\ge 0$ | Note que $Y=|X-c|^r\ge 0$ siempre es no negativa aunque $X$ tome valores negativos, permitiendo aplicar Markov a $Y$. |
| `D-Hab04-11` | Varianza con c!=mu | conceptual_swap | high | $\mathbb{E}[(X-c)^2]=\mathrm{Var}(X)$ para cualquier constante $c\in\mathbb{R}$ | Use $\mathrm{Var}(X)$ únicamente cuando el centro es $c=\mu=\mathbb{E}[X]$; para otro centro $c$ conserve $\mathbb{E}[(X-c)^2]$ en el numerador. |
| `D-Hab04-12` | Cota estricta inválida | conceptual_swap | high | Chebyshev no acota la desigualdad estricta $\mathbb{P}(|X-c|>\varepsilon)$ | Aplique monotonía de probabilidad: $\{|X-c|>\varepsilon\}\subseteq\{|X-c|\ge\varepsilon\}$ implica $\mathbb{P}(|X-c|>\varepsilon)\le\mathbb{P}(|X-c|\ge\varepsilon)$. |
| `D-Hab04-13` | Aplica con negativos | conceptual_swap | high | $P(Y \ge \delta) \le E[Y]/\delta$ vale aunque $Y$ tome valores negativos | Verifique siempre no negatividad $Y \ge 0$ antes de aplicar Markov: los valores negativos invalidan $E[Y] \ge \delta P(Y \ge \delta)$. |
| `D-Hab04-14` | Invierte razón | conceptual_swap | high | $P(Y \ge \delta) \le \delta / E[Y]$ | Divida la esperanza $E[Y]$ entre el umbral $\delta$, no al revés: umbrales más altos reducen la probabilidad máxima posible. |
| `D-Hab04-15` | Cota inferior | conceptual_swap | high | $P(Y \ge \delta) \ge E[Y]/\delta$ | Recuerde que Markov acota desde arriba ($E[Y] \ge \delta P(Y \ge \delta)$), dando un techo máximo y nunca un piso mínimo. |
| `D-Hab04-16` | Confunde igualdad | conceptual_swap | high | $P(Y \ge \delta) = E[Y]/\delta$ | Interprete $E[Y]/\delta$ como cota conservadora válida para toda distribución no negativa, no como probabilidad exacta. |
| `D-Hab04-17` | Usa cola izquierda | conceptual_swap | high | $P(Y \le \delta) \le E[Y]/\delta$ | Aplique Markov únicamente al evento de cola derecha $\{Y \ge \delta\}$, donde $Y \ge \delta$ garantiza la acotación de la indicadora. |
| `D-Hab04-18` | Exige normalidad | conceptual_swap | high | Markov requiere que $Y$ sea simétrica o normal | Recuerde que la gran ventaja de Markov es no requerir forma distribucional alguna, bastando $Y \ge 0$ y $E[Y]$ finita. |
| `D-Hab04-19` | Olvida elevar épsilon | conceptual_swap | high | $P(|X-\mu| \ge \epsilon) \le \text{Var}(X)/\epsilon$ | Eleve al cuadrado la tolerancia $\epsilon$ en el denominador porque Chebyshev aplica Markov a $Y=(X-\mu)^2$ con umbral $\delta=\epsilon^2$. |
| `D-Hab04-20` | Usa desviación en vez de varianza | conceptual_swap | high | $P(|X-\mu| \ge \epsilon) \le \sigma / \epsilon^2$ | Coloque la varianza $\sigma^2 = E[(X-\mu)^2]$ en el numerador, no la desviación estándar $\sigma$, para mantener consistencia de unidades. |
| `D-Hab04-21` | Olvida cuadrado en k | conceptual_swap | high | $P(|X-\mu| \ge k\sigma) \le 1/k$ | Aplique $1/k^2$ al sustituir $\epsilon=k\sigma$ en $\sigma^2/\epsilon^2$, lo que da $25\%$ para $k=2$ y $11.1\%$ para $k=3$. |
| `D-Hab04-22` | Aplica Markov directo a X | conceptual_swap | high | Chebyshev requiere $X \ge 0$ igual que Markov | Note que Chebyshev aplica Markov a $Y=(X-\mu)^2 \ge 0$, por lo cual es válida aunque $X$ tome valores negativos. |
| `D-Hab04-23` | Cola unilateral sin dividir | conceptual_swap | high | $P(X-\mu \ge \epsilon) = 1 - \text{Var}(X)/\epsilon^2$ | Distinga la cota máxima bilateral $\le 1/k^2$ de la probabilidad exacta; para el evento complementario $|X-\mu|<\epsilon$ la cota es $\ge 1-\sigma^2/\epsilon^2$. |
| `D-Hab04-24` | Ignora varianza finita | conceptual_swap | high | Chebyshev vale aunque $\text{Var}(X)$ no exista | Exija existencia de media $\mu$ y varianza finita $\text{Var}(X) < \infty$ antes de acotar colas con Chebyshev. |
| `D-Hab04-25` | Confunde epsilon con k | skipped_step | high | Sustituye $\epsilon$ directamente en $1/k^2$ | Calcule primero $k = \epsilon / \sigma$ antes de usar $1/k^2$, o bien sustituya directamente $\sigma^2 / \epsilon^2 = 25/100 = 0.25$. |
| `D-Hab04-26` | Usa intervalo unilateral como k | skipped_step | high | Toma $k$ respecto al extremo sin centrar en $\mu$ | Mida la distancia $\epsilon = |x - \mu|$ desde la media poblacional $\mu$ antes de dividir por $\sigma$ para obtener $k$. |
| `D-Hab04-27` | Usa varianza como sigma | skipped_step | high | Toma $\sigma = \text{Var}(X)$ al calcular $k = \epsilon/\sigma$ | Extraiga la raíz cuadrada $\sigma = \sqrt{\text{Var}(X)}$ al convertir $\epsilon$ en unidades de desviación estándar $k=\epsilon/\sigma$. |
| `D-Hab04-28` | Usa Markov cuando solo dan varianza | conceptual_swap | high | Aplica $E[X]/\delta$ en lugar de $\text{Var}(X)/\epsilon^2$ para desviaciones | Seleccione Chebyshev cuando acote desviaciones alrededor de la media con $\sigma^2$ conocida, reservando Markov para $P(Y \ge \delta)$ con $Y \ge 0$. |
| `D-Hab04-29` | Confunde cota con exacta normal | conceptual_swap | high | Asume que la cota de Chebyshev coincide con el área normal | Distinga la cota universal de Chebyshev ($25\%$ para $k=2$) del valor exacto bajo normalidad ($4.6\%$): Chebyshev es siempre conservadora. |
| `D-Hab04-30` | Cota mayor que uno como probabilidad | conceptual_swap | high | Reporta $E[Y]/\delta > 1$ como probabilidad válida | Recuerde que cuando $E[Y]/\delta \ge 1$ o $k \le 1$, la cota es trivial ($P \le 1$) y no restringe la probabilidad real. |

#### Formal Mathematical Assumptions (6)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Variable aleatoria no negativa $\mathbb{P}(Y\ge 0)=1$ y $\mathbb{E}[Y]<\infty$ | Si $Y$ toma valores negativos falla la cota de Markov. | - |
| `A-Hab04-02` | - | Momento absoluto finito $\mathbb{E}[|X-c|^r]<\infty$ con $r>0$ | Sin momento finito la cota de Chebyshev queda indeterminada. | - |
| `A-Hab04-03` | - | No negatividad $Y \ge 0$ y umbral positivo $\delta > 0$ | Si $Y$ puede ser negativa o $\delta \le 0$, falla $E[Y] \ge E[Y 1\{Y \ge \delta\}] \ge \delta P(Y \ge \delta)$. | - |
| `A-Hab04-04` | - | Existencia de esperanza finita $E[Y] < \infty$ | Si $E[Y]$ diverge, la cota $E[Y]/\delta$ carece de poder informativo. | - |
| `A-Hab04-05` | - | Existencia de segundo momento finito $\text{Var}(X) = \sigma^2 < \infty$ | Sin varianza finita, el numerador de Chebyshev queda indeterminado. | - |
| `A-Hab04-06` | - | Disponibilidad de momentos poblacionales ($E[Y]$ o $\mu,\sigma^2$) | Sin conocer al menos un momento válido no puede evaluarse ninguna cota. | - |

---

### [C-04] Desigualdad de Jensen y No Conmutatividad (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 17: Desigualdad de Jensen y No Conmutatividad
- **Prerequisites:** None
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 17), `EST3_LEC07_26.2_V2.pdf` (page 25)

#### Description & Cognitive Model
Desigualdad de Jensen $\mathbb{E}[g(X)] \ge g(\mathbb{E}[X])$ para $g$ convexa y $\mathbb{E}[h(X)] \le h(\mathbb{E}[X])$ para $h$ cóncava, derivada vía recta tangente de soporte, que explica la no conmutatividad de $\mathbb{E}[\cdot]$ ante funciones no lineales.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Conmutatividad de esperanza | conceptual_swap | high | $\mathbb{E}[g(X)] = g(\mathbb{E}[X])$ para cualquier función $g$ | Recuerde que la esperanza solo conmuta con funciones afines $ax+b$; para funciones no lineales estrictas como $\sqrt{u}$ o $1/u$, aplique la desigualdad de Jensen. |
| `D-C04-02` | Invierte signo convexo | conceptual_swap | high | $\mathbb{E}[g(X)] \le g(\mathbb{E}[X])$ cuando $g$ es convexa | Verifique la curvatura: una función convexa ($g'' \ge 0$) queda sobre su recta tangente, por lo que $\mathbb{E}[g(X)] \ge g(\mathbb{E}[X])$, nunca menor. |
| `D-C04-03` | Invierte signo cóncavo | conceptual_swap | high | $\mathbb{E}[h(X)] \ge h(\mathbb{E}[X])$ cuando $h$ es cóncava | Multiplique por $-1$ la función cóncava $h$ para volverla convexa: al invertir la desigualdad resulta $\mathbb{E}[h(X)] \le h(\mathbb{E}[X])$, sesgando $S_n$ hacia abajo. |
| `D-C04-04` | Confunde plim con esperanza | conceptual_swap | high | $\mathbb{E}[1/\bar{Y}_n] = 1/\mu$ por ser análogo al límite en probabilidad | Distinga muestras finitas de asintótica: $g(x)=1/x$ ($x>0$) es convexa, luego $\mathbb{E}[1/\bar{Y}_n] > 1/\mu$; solo $\text{plim}$ atraviesa funciones continuas. |
| `D-C04-05` | Omite cota lineal tangente | conceptual_swap | high | La tangente en $\mu$ cruza la gráfica convexa en otros puntos | Incluya siempre el término $g'(\mu)(X-\mu)$ de la recta tangente de soporte; al tomar esperanza, $\mathbb{E}[X-\mu]=0$ anula dicho término exactamente. |
| `D-C04-06` | Descuida dominio abierto | conceptual_swap | high | Jensen vale sin restricción sobre el soporte ni integrabilidad | Verifique que el soporte de $X$ esté contenido en el intervalo abierto $I$ donde $g$ es convexa y que tanto $\mathbb{E}[|X|]$ como $\mathbb{E}[|g(X)|]$ sean finitos. |
| `D-C04-07` | Intercambia esperanza y función | conceptual_swap | high | $E[g(X)] = g(E[X])$ para cualquier función continua $g$ | Recuerde que la esperanza solo conmuta con funciones lineales $a+bX$; en funciones curvas aparece una brecha determinada por la curvatura. |
| `D-C04-08` | Invierte signo en convexa | conceptual_swap | high | $E[g(X)] \le g(E[X])$ cuando $g$ es convexa ($\cup$) | Verifique con $g(x)=x^2$: como $E[X^2]-(E[X])^2=\text{Var}(X) \ge 0$, toda función convexa satisface $E[g(X)] \ge g(E[X])$. |
| `D-C04-09` | Invierte signo en cóncava | conceptual_swap | high | $E[h(X)] \ge h(E[X])$ cuando $h$ es cóncava ($\cap$) | Note que $\sqrt{\cdot}$ es cóncava ($h''<0$), por lo cual Jensen invierte la desigualdad: $E[s] = E[\sqrt{s^2}] \le \sqrt{E[s^2]} = \sigma$. |
| `D-C04-10` | Confunde plim con esperanza | conceptual_swap | high | Si $E[g(\hat{\theta})] \ne g(\theta)$, tampoco $\text{plim } g(\hat{\theta}) = g(\theta)$ | Separe esperanza finita de límite en probabilidad: Jensen prohíbe pasar $E[\cdot]$ por funciones no lineales, pero $\text{plim}$ sí pasa por funciones continuas. |
| `D-C04-11` | Confunde curvatura en dominio | conceptual_swap | high | $g(x)=1/x$ es cóncava para $x>0$ | Calcule la segunda derivada $g''(x)=2/x^3 > 0$ para $x>0$: al ser convexa en el semieje positivo, se cumple $E[1/X] \ge 1/E[X]$. |
| `D-C04-12` | Olvida caso degenerado | conceptual_swap | high | La desigualdad siempre es estricta si $g$ es convexa | Tenga presente que si $X$ es constante ($\text{Var}(X)=0$) o $g$ es afín, se cumple la igualdad $E[g(X)] = g(E[X])$. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Soporte de $X$ contenido en intervalo abierto $I \subseteq \mathbb{R}$ con $\mathbb{E}[|X|] < \infty$ y $\mathbb{E}[|g(X)|] < \infty$ | Sin soporte convexo e integrabilidad absoluta, la esperanza de $g(X)$ puede no existir o no aplicarse la recta de soporte. | - |
| `A-C04-02` | - | Monotonía y linealidad del operador esperanza $\mathbb{E}[\cdot]$ | Permite pasar de la desigualdad puntual $g(X) \ge g(\mu) + g'(\mu)(X-\mu)$ a la desigualdad en esperanzas. | - |
| `A-C04-03` | - | Convexidad o concavidad de $g$ en el soporte de $X$ y existencia de $E[X], E[g(X)]$ | Si la curvatura cambia de signo dentro del soporte de $X$, Jensen no garantiza una dirección global. | - |

---

### [C-05] Desigualdad de Cauchy-Schwarz y Correlación (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 19: Desigualdad de Cauchy-Schwarz y Correlación
- **Prerequisites:** C-04
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 19)

#### Description & Cognitive Model
Desigualdad de Cauchy-Schwarz $(\mathbb{E}[XY])^2 \le \mathbb{E}[X^2]\mathbb{E}[Y^2]$ demostrada mediante el discriminante de $P(t)=\mathbb{E}[(tX+Y)^2] \ge 0$, fundamentando el producto interno en $L^2$ y la acotación $|\rho_{XY}| \le 1$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Olvida elevar al cuadrado | conceptual_swap | high | $(\mathbb{E}[XY])^2 \le \sqrt{\mathbb{E}[X^2]\mathbb{E}[Y^2]}$ | Mantenga la homogeneidad de grado 2: $(\mathbb{E}[XY])^2$ se acota por $\mathbb{E}[X^2]\mathbb{E}[Y^2]$, por lo que $|\mathbb{E}[XY]|$ se acota por la raíz de ese producto. |
| `D-C05-02` | Discriminante positivo | conceptual_swap | high | $P(t) \ge 0$ implica $\Delta = b^2 - 4ac \ge 0$ | Recuerde que una parábola $at^2+bt+c \ge 0$ con $a>0$ no tiene dos raíces reales distintas, lo cual exige que su discriminante cumpla $\Delta = b^2 - 4ac \le 0$. |
| `D-C05-03` | Confunde con varianza | conceptual_swap | high | $|\mathbb{E}[XY]| \le \sqrt{\text{Var}(X)\text{Var}(Y)}$ para variables no centradas | Distinga el segundo momento no centrado $\mathbb{E}[X^2]$ de $\text{Var}(X)$: la cota con varianzas aplica únicamente al aplicar Cauchy-Schwarz a $\tilde{X}=X-\mathbb{E}[X]$ e $\tilde{Y}=Y-\mathbb{E}[Y]$. |
| `D-C05-04` | Omite valor absoluto | conceptual_swap | high | $\mathbb{E}[XY] \le \sqrt{\mathbb{E}[X^2]\mathbb{E}[Y^2]}$ es la cota bilateral completa | Al extraer raíz cuadrada de $(\mathbb{E}[XY])^2$, obtenga $|\mathbb{E}[XY]|$, garantizando tanto la cota superior $+1$ como la cota inferior $-1$ para $\rho_{XY}$. |
| `D-C05-05` | Divide por cero trivial | conceptual_swap | high | El método del discriminante aplica directamente aun si $\mathbb{E}[X^2]=0$ | Separe explícitamente el escenario trivial ($\mathbb{E}[X^2]=0 \Rightarrow \mathbb{P}(X=0)=1 \Rightarrow 0 \le 0$) antes de usar la parábola no degenerada con $a>0$. |
| `D-C05-06` | Confunde producto con suma | conceptual_swap | high | $(\mathbb{E}[XY])^2 \le \mathbb{E}[X^2] + \mathbb{E}[Y^2]$ | Revise el producto $4ac$ en el discriminante: al despejar $4(\mathbb{E}[XY])^2 \le 4\mathbb{E}[X^2]\mathbb{E}[Y^2]$, los segundos momentos aparecen multiplicados, no sumados. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Existencia de segundos momentos finitos $\mathbb{E}[X^2] < \infty$ y $\mathbb{E}[Y^2] < \infty$ | Garantiza que los coeficientes $a,b,c$ del polinomio cuadrático $P(t)$ y la norma en $L^2$ estén bien definidos. | - |

---

### [C-06] Modos de Convergencia (a.s., d, Lr) y su Jerarquía (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 20: Jerarquía de Convergencias Lr y Probabilidad
- **Prerequisites:** C-04, C-05, C-03, Hab-04
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 20), `EST3_LEC07_26.2_V2.pdf` (page 33), `EST3_LEC07_26.2_V2.pdf` (page 35), `EST3_LEC07_26.2_V2.pdf` (page 37)

#### Description & Cognitive Model
Modos de convergencia asintótica —casi segura ($X_n \xrightarrow{a.s.} c \Leftrightarrow P(\lim_{n\to\infty} X_n = c)=1$), en distribución ($X_n \xrightarrow{d} X \Leftrightarrow \lim_{n\to\infty} F_{X_n}(x) = F_X(x)$ en puntos de continuidad de $F_X$) y en $L^r$— y su teorema de jerarquía: para $0<s<r$, $X_n \xrightarrow{L^r} X \Rightarrow X_n \xrightarrow{L^s} X \Rightarrow X_n \xrightarrow{p} X \Rightarrow X_n \xrightarrow{d} X$, $\xrightarrow{a.s.}\Rightarrow\xrightarrow{p}$, el caso límite constante $\xrightarrow{d} c \Rightarrow \xrightarrow{p} c$, y convergencia de momentos absolutos si $r\ge 1$.

#### Fused Distractor Models (24)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Invierte orden de potencias | conceptual_swap | high | Convergencia en $L^1$ implica convergencia en $L^2$ ($0<s<r$ invertido) | Verifique la dirección de dominio: normas de orden superior $r$ penalizan más las colas, por lo que $L^r \Rightarrow L^s$ solo cuando $r > s$, nunca en sentido inverso. |
| `D-C06-02` | Asume equivalencia bilateral | conceptual_swap | high | Convergencia en probabilidad equivale a convergencia en media cuadrática | Reemplace la equivalencia por implicación unidireccional: $L^2 \Rightarrow p$ siempre se cumple, pero el recíproco es falso cuando existen valores atípicos extremos. |
| `D-C06-03` | Confunde L2 con ECM=0 | conceptual_swap | high | $\text{Var}(\hat{\theta}_n) \to 0$ basta para $L^2$ sin verificar el sesgo | Recuerde que $L^2$ exige $\text{ECM}(\hat{\theta}_n) = \text{Var}(\hat{\theta}_n) + [\text{Sesgo}(\hat{\theta}_n)]^2 \to 0$; si el sesgo no tiende a cero, no converge al parámetro. |
| `D-C06-04` | Exige r>=1 para Lr a p | conceptual_swap | high | $X_n \xrightarrow{L^r} X \Rightarrow X_n \xrightarrow{p} X$ requiere $r \ge 2$ | Distinga ambos incisos: $X_n \xrightarrow{L^r} X \Rightarrow X_n \xrightarrow{p} X$ vale para todo $r>0$ (incluido $r=1$); la condición $r \ge 1$ solo se pide para Minkowski en momentos. |
| `D-C06-05` | Confunde momento absoluto con error | conceptual_swap | high | $\mathbb{E}[|X_n|^r] \to \mathbb{E}[|X|^r]$ equivale a $X_n \xrightarrow{L^r} X$ | Diferencie convergencia de momentos absolutos $\mathbb{E}[|X_n|^r] \to \mathbb{E}[|X|^r]$ de $\mathbb{E}[|X_n - X|^r] \to 0$; esta última implica la primera, no al revés. |
| `D-C06-06` | Omite finitud de momento límite | conceptual_swap | high | $\mathbb{E}[|X_n|^r] \to \mathbb{E}[|X|^r]$ sin exigir $\mathbb{E}[|X|^r] < \infty$ | Verifique la hipótesis $\mathbb{E}[|X|^r] < \infty$ (es decir, $X \in L^r$) antes de aplicar la desigualdad de Minkowski para demostrar la convergencia de momentos absolutos. |
| `D-C06-07` | Intercambia límite y probabilidad | conceptual_swap | high | $P(\lim_{n\to\infty} X_n = c) = 1$ es lo mismo que $\lim_{n\to\infty} P(|X_n - c| \le \epsilon) = 1$ | Distinga el orden de los operadores: $\xrightarrow{p}$ evalúa cada $n$ por separado antes del límite, mientras $\xrightarrow{a.s.}$ exige que toda la trayectoria quede en $c \pm \epsilon$. |
| `D-C06-08` | Invierte implicación a.s. y p | conceptual_swap | high | $X_n \xrightarrow{p} c \Rightarrow X_n \xrightarrow{a.s.} c$ | Recuerde que la convergencia casi segura es más exigente que en probabilidad: $\xrightarrow{a.s.} \Rightarrow \xrightarrow{p}$, pero una sucesión puede acercarse en probabilidad y seguir saltando ocasionalmente. |
| `D-C06-09` | Exige cero saltos iniciales | conceptual_swap | high | Si $X_n$ se aleja mucho de $c$ para $n=10$, no converge casi seguramente | Recuerde que la convergencia casi segura permite fluctuaciones grandes al inicio: exige que a partir de cierto $N(\omega)$ finito la trayectoria no vuelva a salir de $c\pm\epsilon$. |
| `D-C06-10` | Exige determinismo absoluto | conceptual_swap | high | Convergencia casi segura significa que ninguna trayectoria puede diverger | Note que eventos excepcionales como infinitas caras seguidas pueden existir en el espacio muestral, pero su probabilidad conjunta es exactamente $0$. |
| `D-C06-11` | Confunde con media cuadrática | conceptual_swap | high | $X_n \xrightarrow{a.s.} c$ implica $E[(X_n - c)^2] \to 0$ | Separe ambas nociones fuertes: ni $\xrightarrow{a.s.}$ implica $\xrightarrow{m.s.}$ (pueden fallar los momentos) ni $\xrightarrow{m.s.}$ implica $\xrightarrow{a.s.}$ en general. |
| `D-C06-12` | Confunde LFGN con LDGN | conceptual_swap | high | La Ley Fuerte de los Grandes Números solo da convergencia en probabilidad | Asocie la Ley Fuerte de los Grandes Números con $\bar{Y}_n \xrightarrow{a.s.} \mu$ (trayectoria completa con probabilidad $1$), que a su vez implica $\xrightarrow{p}$. |
| `D-C06-13` | Compara valores en vez de FDA | conceptual_swap | high | $X_n \xrightarrow{d} X$ significa que $X_n$ toma valores cercanos a $X$ | Recuerde que la convergencia en distribución solo compara las funciones de distribución acumulada $F_{X_n}$ y $F_X$, no la cercanía realización a realización. |
| `D-C06-14` | Exige convergencia en discontinuidades | conceptual_swap | high | $F_{X_n}(x) \to F_X(x)$ debe cumplirse incluso en puntos de salto de $F_X$ | Verifique la condición únicamente en los puntos de continuidad de $F_X$; excluir discontinuidades evita descartar sucesiones deterministas como $1/n \to 0$. |
| `D-C06-15` | Confunde densidades con FDA | conceptual_swap | high | $X_n \xrightarrow{d} X$ equivale siempre a convergencia puntual de densidades | Defina la convergencia en distribución mediante las probabilidades acumuladas $F_{X_n}(x) = P(X_n \le x)$, lo que permite pasar de distribuciones discretas a continuas. |
| `D-C06-16` | Exige normalidad exacta de datos | conceptual_swap | high | Solo si $Y_i$ son normales puede $Z_n = \sqrt{n}(\bar{Y}_n-\mu)/\sigma$ converger a $N(0,1)$ | Note que aunque $Y_i$ sea muy asimétrica, $\sqrt{n}(\bar{Y}_n-\mu)/\sigma \xrightarrow{d} N(0,1)$ justifica aproximar probabilidades con la tabla normal cuando $n$ es grande. |
| `D-C06-17` | Confunde constante con variable aleatoria | conceptual_swap | high | $X_n \xrightarrow{d} X$ requiere que $X_n$ y $X$ estén en el mismo espacio muestral | Observe que $F_{X_n}(x)$ y $F_X(x)$ dependen solo de las distribuciones marginales, de modo que $X_n$ y $X$ ni siquiera necesitan estar acopladas en el mismo espacio. |
| `D-C06-18` | Confunde distribución límite con igualdad finita | conceptual_swap | high | Si $Z_n \xrightarrow{d} N(0,1)$, entonces $P(Z_n \le 1.645) = 0.950$ para $n=30$ | Distinga aproximación asintótica de distribución exacta en muestra finita: con $n$ moderado y datos asimétricos persiste un error de aproximación. |
| `D-C06-19` | Invierte jerarquía d hacia p | conceptual_swap | high | $X_n \xrightarrow{d} X \Rightarrow X_n \xrightarrow{p} X$ en general | Recuerde que $\xrightarrow{d}$ es el modo más débil y solo garantiza igual forma límite; si el límite $X$ no es constante, $X_n$ y $X$ pueden estar lejos siempre. |
| `D-C06-20` | Niega caso constante d hacia p | conceptual_swap | high | Incluso si $X_n \xrightarrow{d} c$ constante, no implica $X_n \xrightarrow{p} c$ | Aplique la excepción fundamental: cuando el límite en distribución es una constante $c$, toda la probabilidad se concentra en un punto y $\xrightarrow{d} c \Leftrightarrow \xrightarrow{p} c$. |
| `D-C06-21` | Encadena m.s. con a.s. | conceptual_swap | high | $X_n \xrightarrow{m.s.} X \Rightarrow X_n \xrightarrow{a.s.} X$ | Trace las dos ramas separadas que confluyen en $\xrightarrow{p}$: tanto $\xrightarrow{m.s.}$ como $\xrightarrow{a.s.}$ implican $\xrightarrow{p}$, pero ninguna implica a la otra directamente. |
| `D-C06-22` | Omite puente hacia distribución | conceptual_swap | high | La convergencia en probabilidad no implica convergencia en distribución | Use la jerarquía completa: si $X_n \xrightarrow{p} X$, necesariamente $X_n \xrightarrow{d} X$, porque concentrar la diferencia fuerza la aproximación de las FDA. |
| `D-C06-23` | Supone equivalencia total | conceptual_swap | high | Los cuatro modos de convergencia son equivalentes si existen momentos | Respete estrictamente el sentido unidireccional de las flechas de la jerarquía salvo equivalencias explícitas como $\xrightarrow{d} c \Leftrightarrow \xrightarrow{p} c$. |
| `D-C06-24` | Confunde p con m.s. | conceptual_swap | high | $X_n \xrightarrow{p} c$ siempre implica sesgo y varianza tendiendo a cero | Note que $\xrightarrow{m.s.} \Rightarrow \xrightarrow{p}$, pero no a la inversa: existen estimadores consistentes cuyo segundo momento diverge o no tiende a cero. |

#### Formal Mathematical Assumptions (4)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Para convergencia de momentos absolutos se requiere $r \ge 1$ y $\mathbb{E}[|X|^r] < \infty$ | Solo cuando $r \ge 1$ la funcional $\|U\|_r=(\mathbb{E}[|U|^r])^{1/r}$ define una norma que satisface la desigualdad de Minkowski. | - |
| `A-C06-02` | - | Espacio de probabilidad común donde está definida toda la trayectoria $\{X_n(\omega)\}_{n\ge 1}$ | Sin un espacio común para la sucesión completa no puede definirse el evento $\{\omega : \lim_{n\to\infty} X_n(\omega) = c\}$. | - |
| `A-C06-03` | - | Existencia de una función de distribución acumulada límite $F_X(x)$ bien definida | Sin una FDA límite propia (sin fuga de masa al infinito), la sucesión no converge en distribución. | - |
| `A-C06-04` | - | Límite degenerado $c \in \mathbb{R}$ para activar la implicación inversa $\xrightarrow{d} c \Rightarrow \xrightarrow{p} c$ | Cuando el límite es una variable aleatoria no degenerada, $X_n \xrightarrow{d} X$ no implica cercanía en probabilidad. | - |

---

### [Hab-06] Implicaciones Lr, No Reciprocidad y Diagnóstico Asintótico (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 21: Demostración de Implicaciones Lr y Momentos
- **Prerequisites:** C-04, C-06
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 21), `Clases_sintetizadas_semana_9.pdf` (page 23), `EST3_LEC07_26.2_V2.pdf` (page 38)

#### Description & Cognitive Model
Demostración de implicaciones $L^r \Rightarrow L^s$, $L^r \Rightarrow p$ y convergencia de momentos absolutos (vía Jensen, Chebyshev generalizada y Minkowski), y diagnóstico asintótico de sucesiones y estimadores incluyendo contraejemplos de no reciprocidad ($X_n \in \{0, n^2\}$ o $\{0, n\}$ con probabilidad $1/n$ donde $X_n \xrightarrow{p} 0$ mientras los momentos divergen).

#### Fused Distractor Models (18)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Exponente cóncavo s/r | skipped_step | high | Aplica Jensen directamente a $g(z)=z^{s/r}$ asumiendo que es convexa | Como $0<s/r<1$, $z^{s/r}$ es cóncava; debe definir $Z_n=|X_n-X|^s$ y aplicar Jensen a $g(z)=z^{r/s}$ (con $r/s>1$, convexa) antes de elevar a la potencia $s/r$. |
| `D-Hab06-02` | Omite potencia r en Chebyshev | skipped_step | high | $\mathbb{P}(|X_n-X| > \varepsilon) \le \mathbb{E}[|X_n-X|^r]/\varepsilon$ sin exponente en $\varepsilon$ | Aplique Chebyshev de orden $r$: al transformar $|X_n-X| \ge \varepsilon$ en $|X_n-X|^r \ge \varepsilon^r$, el umbral del denominador debe elevarse a $\varepsilon^r$. |
| `D-Hab06-03` | Invierte sentido de Minkowski | skipped_step | high | $\|X_n\|_r \ge \|X_n-X\|_r + \|X\|_r$ al acotar momentos absolutos | Aplique primero la desigualdad triangular sobre la norma $\|\cdot\|_r = (\mathbb{E}[|\cdot|^r])^{1/r}$ con $X_n=(X_n-X)+X$ y $X=(X-X_n)+X_n$ antes de elevar a la potencia $r$. |
| `D-Hab06-04` | Olvida continuidad en cero | conceptual_swap | high | No justifica el paso al límite de $(\mathbb{E}[|X_n-X|^r])^{s/r} \to 0$ | Complete el cierre asintótico: por no negatividad $0 \le \mathbb{E}[|X_n-X|^s] \le (\mathbb{E}[|X_n-X|^r])^{s/r}$ y continuidad de $u^{s/r}$ en $u=0$, concluya por el Teorema del Sándwich. |
| `D-Hab06-05` | Confunde cota estricta | conceptual_swap | high | Chebyshev acota solo $\ge \varepsilon$ y no puede acotar $> \varepsilon$ | Use la inclusión de eventos $\{|X_n-X| > \varepsilon\} \subseteq \{|X_n-X| \ge \varepsilon\}$, lo cual garantiza $\mathbb{P}(|X_n-X| > \varepsilon) \le \mathbb{P}(|X_n-X| \ge \varepsilon) \le \mathbb{E}[|X_n-X|^r]/\varepsilon^r$. |
| `D-Hab06-06` | Omite simetría en valor absoluto | conceptual_swap | high | Usa solo $\|X_n\|_r - \|X\|_r \le \|X_n-X\|_r$ para concluir $|\|X_n\|_r-\|X\|_r| \to 0$ | Desarrolle ambas descomposiciones ($X_n=(X_n-X)+X$ y $X=(X-X_n)+X_n$) para obtener la desigualdad triangular inversa $0 \le |\|X_n\|_r - \|X\|_r| \le \|X_n-X\|_r$. |
| `D-Hab06-07` | Aplica Markov inversa | skipped_step | high | Si $X_n \xrightarrow{p} 0$, entonces necesariamente $\mathbb{E}[X_n] \to 0$ | Calcule directamente $\mathbb{E}[X_n] = n^2(1/n) = n \to +\infty$; el operador $\text{plim}$ ignora la magnitud del valor atípico $n^2$, mientras la esperanza pondera valor por probabilidad. |
| `D-Hab06-08` | Omite condición $n^2$ > epsilon | skipped_step | high | El evento $\{|X_n| > \varepsilon\}$ equivale a $\{X_n = n^2\}$ para todo $n \ge 1$ sin condición | Especifique que para cualquier $\varepsilon > 0$ dado, a partir de todo $n$ tal que $n^2 > \varepsilon$, el único punto del soporte fuera de $[-\varepsilon, \varepsilon]$ es $X_n = n^2$. |
| `D-Hab06-09` | Error en segundo momento | conceptual_swap | high | Calcula $\mathbb{E}[X_n^2] = n^2 \cdot (1/n) = n$ olvidando elevar $n^2$ al cuadrado | Eleve al cuadrado el valor del soporte antes de multiplicar por la probabilidad: $(n^2)^2 \cdot (1/n) = n^4/n = n^3$, y verifique $\text{Var}(X_n) = n^3 - n^2 = n^2(n-1)$. |
| `D-Hab06-10` | Confunde variante acotada | conceptual_swap | high | En la variante $X_n \in \{0, n\}$ con probabilidad $1/n$, $\mathbb{E}[X_n] \to 0$ | Evalúe la variante: $\mathbb{E}[X_n] = 0(1-1/n) + n(1/n) = 1$ para todo $n$, demostrando que $\lim_{n\to\infty}\mathbb{E}[X_n] = 1$ difiere de $\text{plim}_{n\to\infty} X_n = 0$. |
| `D-Hab06-11` | Confunde varianza con ECM | conceptual_swap | high | Calcula $\text{Var}(X_n) = n^3$ omitiendo restar $(\mathbb{E}[X_n])^2$ | Distinga el ECM respecto a cero ($\mathbb{E}[(X_n-0)^2] = \mathbb{E}[X_n^2] = n^3$) de la varianza centrada en la media: $\text{Var}(X_n) = \mathbb{E}[X_n^2] - (\mathbb{E}[X_n])^2 = n^3 - n^2$. |
| `D-Hab06-12` | Confunde soporte con probabilidad | conceptual_swap | high | Evalúa $\mathbb{P}(X_n = n^2) = 1 - 1/n$ invirtiendo las masas discretas | Verifique la asignación de la función de masa: el punto extremo $n^2$ ocurre con probabilidad evanescente $1/n \to 0$, concentrando la masa $1-1/n \to 1$ en cero. |
| `D-Hab06-13` | Confunde igualdad marginal con plim | skipped_step | high | Para $X_n=-Z$ con $Z \sim N(0,1)$, toma $P(|X_n-Z|>1)=0$ porque tienen igual ley | Calcule la diferencia aleatoria explícita $|X_n - Z| = |-Z - Z| = 2|Z|$ antes de evaluar $P(2|Z| > 1) = P(|Z| > 0.5) = 0.617 \not\to 0$. |
| `D-Hab06-14` | Omite factor 2 en diferencia | skipped_step | high | Con $X_n=-Z$, escribe $|X_n-Z|=|Z|$ en vez de $2|Z|$ | Sustituya $X_n = -Z$ cuidadosamente en $X_n - Z = -Z - Z = -2Z$, de modo que $|X_n - Z| > 1$ equivale a $|Z| > 0.5$. |
| `D-Hab06-15` | Clasifica Y1 como consistente | skipped_step | high | Al clasificar $Y_1$, concluye consistencia porque $E[Y_1]=\mu$ | Evalúe la varianza de $Y_1$ conforme crece $n$: $\text{Var}(Y_1)=\sigma^2=100$ no disminuye al agregar datos, por lo que $Y_1$ es insesgado pero inconsistente. |
| `D-Hab06-16` | Clasifica sesgado decreciente como inconsistente | conceptual_swap | high | Para $\bar{Y}_n + 5/n$, marca no insesgado y por tanto no consistente | Compruebe el comportamiento asintótico de ambos componentes: $5/n \to 0$ y $\sigma^2/n \to 0$, por lo cual $\bar{Y}_n + 5/n$ es sesgado pero consistente. |
| `D-Hab06-17` | Niega convergencia en distribución por simetría | conceptual_swap | high | Si $X_n = -Z$, entonces $X_n$ no converge en distribución a $Z$ | Verifique la FDA de $-Z$: por simetría de $N(0,1)$, $-Z \sim N(0,1)$, luego $F_{X_n}(x) = F_Z(x)$ para todo $x$ y sí hay convergencia en distribución. |
| `D-Hab06-18` | Confunde consistencia con a.s. sin LFGN | conceptual_swap | high | Cualquier sucesión con $F_{X_n} \to F_X$ converge casi seguramente | Recuerde que $\xrightarrow{a.s.} \Rightarrow \xrightarrow{p} \Rightarrow \xrightarrow{d}$: al fallar $\xrightarrow{p}$ en $X_n = -Z$, queda automáticamente descartada la convergencia casi segura. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Continuidad y monotonía creciente de $u \mapsto u^{s/r}$ en $[0, \infty)$ para $0 < s < r$ | Permite extraer la potencia $s/r$ en la desigualdad de Jensen y evaluar el límite en $u=0$. | - |
| `A-Hab06-02` | - | Definición de límite en probabilidad $\lim_{n\to\infty}\mathbb{P}(|X_n - c| > \varepsilon) = 0$ para todo $\varepsilon > 0$ | Establece el criterio exacto bajo el cual $X_n \xrightarrow{p} 0$ depende solo de la probabilidad de cola y no de la magnitud de $n^2$. | - |
| `A-Hab06-03` | - | Especificación conjunta de $(X_n, X)$ o fórmula explícita de $\hat{\theta}_n$ en función de la muestra | Sin conocer la dependencia conjunta entre $X_n$ y $X$ no puede evaluarse $P(|X_n - X| > \epsilon)$. | - |

---

### [C-07] Insesgadez vs. Consistencia de Estimadores (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 27: Insesgadez vs. Consistencia de Estimadores
- **Prerequisites:** C-06
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 27), `EST3_LEC07_26.2_V2.pdf` (page 31)

#### Description & Cognitive Model
Independencia lógica entre insesgadez (propiedad de muestras finitas $\mathbb{E}[\hat{\theta}_n]=\theta$) y consistencia (propiedad asintótica $\hat{\theta}_n \xrightarrow{p} \theta$), ilustrada por $M_A=Y_1$ y $M_B$ (insesgados inconsistentes) frente a $M_C=\bar{Y}_n+1/n$ (sesgado consistente).

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Insesgado implica consistente | conceptual_swap | high | Todo estimador insesgado para todo $n$ converge en probabilidad al parámetro | Recuerde que la insesgadez solo fija la esperanza en cada $n$; si la varianza no colapsa a cero (como en $M_A=Y_1$ o $M_B$), las colas no se concentran y el estimador es inconsistente. |
| `D-C07-02` | Consistente implica insesgado | conceptual_swap | high | Todo estimador consistente debe ser insesgado en muestras finitas | Distinga muestras finitas de asintótica: $M_C$ es sesgado para todo $n$ finito, pero tanto su sesgo ($1/n \to 0$) como su varianza ($\sigma_Y^2/n \to 0$) se disipan garantizando consistencia. |
| `D-C07-03` | Usa n datos basta | conceptual_swap | high | Cualquier promedio insesgado que use las $n$ observaciones es consistente | Observe cómo caen los pesos: en $M_B$, los pesos geométricos $a^{i-1}$ ($0<a<1$) decaen exponencialmente e ignoran las nuevas observaciones, dejando el estimador dominado por las primeras. |
| `D-C07-04` | Confunde sesgo finito con asintótico | conceptual_swap | high | Si $\text{Sesgo}(\hat{\theta}_n) \to 0$, entonces $\hat{\theta}_n$ es consistente aunque su varianza no tienda a 0 | La insesgadez asintótica ($\text{Sesgo} \to 0$) no basta para consistencia; también se requiere que la dispersión alrededor de la media se disipe ($\text{Var} \to 0$ o colas $\to 0$). |
| `D-C07-05` | Descarta estimadores sesgados | conceptual_swap | high | En econometría aplicada se prefiere un estimador insesgado aunque sea inconsistente | Aplique la primacía de la consistencia: en econometría (2SLS, GMM, MV, MCO con rezagos), los estimadores relevantes suelen ser sesgados en muestras finitas pero consistentes cuando $n \to \infty$. |
| `D-C07-06` | Confunde suma de pesos con LGN | conceptual_swap | high | Si la suma de pesos normalizados es $1$, se cumple automáticamente la Ley de Grandes Números | Diferencie normalización de concentración: aunque los pesos de $M_B$ sumen $1$, su suma de cuadrados $\sum w_i^2$ converge a $(1-a)/(1+a) > 0$, impidiendo que la varianza colapse a cero. |
| `D-C07-07` | Insesgadez implica consistencia | conceptual_swap | high | Todo estimador insesgado es automáticamente consistente | Recuerde el contraejemplo $\hat{\mu}_n = Y_1$: es insesgado en todo $n$, pero su varianza permanece fija en $\sigma^2$ y nunca se concentra en $\mu$. |
| `D-C07-08` | Consistencia implica insesgadez | conceptual_swap | high | Todo estimador consistente debe ser insesgado | Distinga propiedad de muestra finita (insesgadez) de propiedad asintótica (consistencia): un sesgo tipo $c/n$ desaparece cuando $n \to \infty$. |
| `D-C07-09` | Confunde sesgo de Jensen con inconsistencia | conceptual_swap | high | Si $E[g(\hat{\theta}_n)] \ne g(\theta)$ por Jensen, entonces $g(\hat{\theta}_n)$ es inconsistente | Separe expectativa finita de límite en probabilidad: aunque Jensen produce sesgo finito en $s$ o $1/\bar{Y}_n$, ambos siguen siendo consistentes si $g$ es continua. |
| `D-C07-10` | Prioriza insesgadez siempre | conceptual_swap | high | En econometría de muestras grandes la insesgadez es más importante que la consistencia | Note que en muestras grandes la econometría prioriza la consistencia porque MCO con regresores estocásticos, VI y MV suelen ser sesgados en muestra finita. |
| `D-C07-11` | Confunde varianza nula con sesgo nulo | conceptual_swap | high | Un estimador con varianza decreciente es necesariamente insesgado | Evalúe la esperanza $E[\hat{\theta}_n]$ por separado de $\text{Var}(\hat{\theta}_n)$: agregar $5/n$ desplaza el centro sin cambiar la dispersión. |
| `D-C07-12` | Asimila insesgadez asintótica a finita | conceptual_swap | high | Si $\lim_{n\to\infty} E[\hat{\theta}_n] = \theta$, entonces el estimador es insesgado | Exija $E[\hat{\theta}_n] = \theta$ exactamente para todo $n$ finito para llamar insesgado a un estimador; si solo vale en el límite es asintóticamente insesgado. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Muestra aleatoria simple $\{Y_i\}_{i=1}^n$ i.i.d. con $\mathbb{E}[Y_i]=\mu_Y$ y $0 < \text{Var}(Y_i)=\sigma_Y^2 < \infty$ | Permite comparar en igualdad de condiciones el comportamiento exacto en muestras finitas y el límite asintótico de $M_A, M_B, M_C$. | - |
| `A-C07-02` | - | Parametrización fija $\theta$ independiente de $n$ y familia de estimadores $\{\hat{\theta}_n\}$ | Si el objeto estimado cambia con $n$, no es posible comparar sesgo fijo con límite asintótico. | - |

---

### [Hab-08] Cálculo de Esperanza, Varianza, Sesgo, ECM y Consistencia (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 25: Cálculo de Varianza Exacta y ECM en Estimadores
- **Prerequisites:** C-07, C-02, Hab-04
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 25), `EST3_LEC07_26.2_V2.pdf` (page 17), `EST3_LEC07_26.2_V2.pdf` (page 5), `EST3_LEC07_26.2_V2.pdf` (page 7), `EST3_LEC07_26.2_V2.pdf` (page 30)

#### Description & Cognitive Model
Cálculo algebraico de esperanza $E[X]$, varianza $\mathrm{Var}(X)$, error estándar $ee(\hat{\theta})$, sesgo $\mathrm{Sesgo}(\hat{\theta})=E[\hat{\theta}]-\theta$, eficiencia relativa, descomposición del ECM y prueba de consistencia vía series geométricas finitas (ej. $M_B$, $M_C$) y desigualdad de Chebyshev.

#### Fused Distractor Models (30)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | No eleva pesos al cuadrado | skipped_step | high | $\text{Var}\left(\sum_{i=1}^n c_i Y_i\right) = \sum_{i=1}^n c_i \text{Var}(Y_i)$ | Aplique la propiedad cuadrática de la varianza en combinaciones independientes: cada coeficiente $c_i = \frac{1-a}{1-a^n}a^{i-1}$ debe elevarse al cuadrado, generando razón $r=a^2$ en la serie. |
| `D-Hab08-02` | Suma constante altera varianza | skipped_step | high | $\text{Var}(\bar{Y}_n + 1/n) = \text{Var}(\bar{Y}_n) + 1/n^2$ | Recuerde que sumar una constante determinística $1/n$ desplaza la media pero no altera la varianza ($\text{Var}(M_C)=\sigma_Y^2/n$); el término $1/n^2$ entra al ECM vía $[\text{Sesgo}(M_C)]^2$. |
| `D-Hab08-03` | Olvida cancelar factores | skipped_step | high | $\frac{1-a^{2n}}{1-a^2}$ se simplifica dejando $(1-a)^2$ en el numerador | Factorice ambas diferencias de cuadrados: $1-a^2=(1-a)(1+a)$ y $1-a^{2n}=(1-a^n)(1+a^n)$, cancele $(1-a)(1-a^n)$ y tome el límite $a^n \to 0$ para obtener $\sigma_Y^2\frac{1-a}{1+a}$. |
| `D-Hab08-04` | Olvida elevar sesgo al cuadrado | conceptual_swap | high | $\text{ECM}(M_C) = \text{Var}(M_C) + \text{Sesgo}(M_C)$ | Use la descomposición exacta $\text{ECM}(M_C) = \text{Var}(M_C) + [\text{Sesgo}(M_C)]^2 = \frac{\sigma_Y^2}{n} + \frac{1}{n^2}$, manteniendo homogeneidad cuadrática antes de aplicar Chebyshev. |
| `D-Hab08-05` | Invierte razón en serie finita | conceptual_swap | high | $\sum_{i=1}^n a^{2(i-1)} = \frac{1-a^n}{1-a^2}$ usando exponente $n$ en vez de $2n$ | Aplique la fórmula de serie geométrica $\sum_{i=1}^n r^{i-1}=\frac{1-r^n}{1-r}$ con razón $r=a^2$, por lo que el numerador es $1-(a^2)^n = 1-a^{2n}$. |
| `D-Hab08-06` | Omite distribución normal en colas | conceptual_swap | high | Para $M_B$, la varianza positiva impide escribir la probabilidad exacta de cola | Aproveche que $Y_i \sim \mathcal{N}(\mu_Y, \sigma_Y^2)$ independientes implica que $M_B$ es normal exacta, obteniendo $\lim_{n\to\infty}\mathbb{P}(|M_B-\mu_Y|\ge\delta)=2[1-\Phi(\delta/(\sigma_Y\sqrt{\frac{1-a}{1+a}}))]>0$. |
| `D-Hab08-07` | No eleva al cuadrado en E[$X^2$] | skipped_step | high | $\text{Var}(X)=E[X]-(E[X])^2$ | Eleve cada valor $x$ al cuadrado antes de ponderar por su probabilidad para obtener $E[X^2]$ en la fórmula abreviada. |
| `D-Hab08-08` | Olvida restar (E[X])^2 | skipped_step | high | $\text{Var}(X)=E[X^2]$ | Reste siempre $(E[X])^2$ a $E[X^2]$; de lo contrario mide el segundo momento no centrado en lugar de la dispersión. |
| `D-Hab08-09` | Promedio simple sin ponderar | conceptual_swap | high | $E[X]=\frac{1}{k}\sum_{j=1}^k x_j$ | Pondere cada valor posible $x$ por su probabilidad $P(X=x)$; el promedio aritmético simple solo vale si son equiprobables. |
| `D-Hab08-10` | Confunde varianza con sigma | skipped_step | high | $\sigma=\text{Var}(X)$ | Extraiga la raíz cuadrada $\sigma=\sqrt{\text{Var}(X)}$ para expresar la dispersión en las mismas unidades que $X$. |
| `D-Hab08-11` | Desvíos sin elevar al cuadrado | conceptual_swap | high | $\text{Var}(X)=E[X-E[X]]$ | Eleve al cuadrado cada desvío $(x-E[X])^2$ antes de promediar; de lo contrario los signos positivos y negativos se cancelan. |
| `D-Hab08-12` | Error en orden de cuadrado | conceptual_swap | high | $E[X^2]=(E[X])^2$ | Recuerde que la función cuadrada no conmuta con la esperanza: en general $E[X^2]\ge(E[X])^2$ con igualdad solo si $X$ es constante. |
| `D-Hab08-13` | Invierte signo del sesgo | skipped_step | high | $\text{Sesgo}(\hat{\theta})=\theta-E[\hat{\theta}]$ | Calcule $E[\hat{\theta}]-\theta$: un estimador que subestima en promedio tiene sesgo negativo ($1800-2000=-200$). |
| `D-Hab08-14` | Evalúa sesgo en una realización | conceptual_swap | high | $\text{Sesgo}=\hat{\theta}_{\text{obs}}-\theta$ | Evalúe el sesgo sobre la esperanza $E[\hat{\theta}]$, no sobre una muestra aislada; la insesgadez es propiedad de la fórmula. |
| `D-Hab08-15` | Saca c fuera sin multiplicar mu | skipped_step | high | $E[c\bar{Y}]=c+\mu$ | Aplique la propiedad multiplicativa de la esperanza lineal: $E[c\bar{Y}]=cE[\bar{Y}]=c\mu$, luego $\text{Sesgo}=(c-1)\mu$. |
| `D-Hab08-16` | Omite dividir por n en la media | conceptual_swap | high | $E[\bar{Y}]=\sum_{i=1}^n E[Y_i]=n\mu$ | Incluya el factor $1/n$ por linealidad: $E[\bar{Y}]=\frac{1}{n}\sum_{i=1}^n E[Y_i]=\frac{1}{n}(n\mu)=\mu$. |
| `D-Hab08-17` | Confunde sesgo nulo con varianza nula | conceptual_swap | high | $E[\hat{\theta}]=\theta\Rightarrow \hat{\theta}=\theta$ | Recuerde que $E[\hat{\theta}]=\theta$ solo garantiza acierto en promedio tras repetir el muestreo, no ausencia de error muestral. |
| `D-Hab08-18` | Sesgo independiente de mu en cY | conceptual_swap | high | $\text{Sesgo}(c\bar{Y})=c-1$ | Multiplique $(c-1)$ por el parámetro $\mu$: el sesgo absoluto es $c\mu-\mu=(c-1)\mu$ y depende de la escala de $\mu$. |
| `D-Hab08-19` | No eleva 1/n al cuadrado | skipped_step | high | $\text{Var}(\bar{Y})=\frac{1}{n}\sum\text{Var}(Y_i)=\sigma^2$ | Saque las constantes al cuadrado al calcular varianzas: $\text{Var}(\frac{1}{n}\sum Y_i)=\frac{1}{n^2}\sum\text{Var}(Y_i)=\frac{\sigma^2}{n}$. |
| `D-Hab08-20` | Error estándar igual a varianza sobre n | skipped_step | high | $ee(\bar{Y})=\sigma^2/n$ | Tome la raíz cuadrada de la varianza del estimador: $ee(\bar{Y})=\sqrt{\sigma^2/n}=\sigma/\sqrt{n}$. |
| `D-Hab08-21` | Divide sigma por n en vez de raíz de n | conceptual_swap | high | $ee(\bar{Y})=\sigma/n$ | Divida $\sigma$ entre $\sqrt{n}$, no entre $n$: duplicar precisión exige cuadruplicar el tamaño muestral $n$. |
| `D-Hab08-22` | Elige mayor varianza como eficiente | conceptual_swap | high | $\text{Var}(\hat{\theta}_1)>\text{Var}(\hat{\theta}_2)\Rightarrow\hat{\theta}_1$ más eficiente | Recuerde que menor varianza significa estimaciones más concentradas alrededor de $\theta$ y, por tanto, mayor eficiencia. |
| `D-Hab08-23` | Compara eficiencia ignorando sesgo | conceptual_swap | high | Menor varianza siempre implica mejor estimador | Verifique primero que ambos estimadores sean insesgados antes de aplicar el criterio de eficiencia por mínima varianza. |
| `D-Hab08-24` | No eleva c al cuadrado en Var(cY) | conceptual_swap | high | $\text{Var}(c\bar{Y})=c\text{Var}(\bar{Y})$ | Aplique $\text{Var}(c\bar{Y})=c^2\text{Var}(\bar{Y})$: un factor escalar $0.9$ reduce la varianza por $0.9^2=0.81$. |
| `D-Hab08-25` | Olvida cuadrado al calcular ECM | skipped_step | high | Suma $\text{Var}(\hat{\mu}_n) + \text{Sesgo}(\hat{\mu}_n)$ linealmente | Eleve al cuadrado el sesgo $(5/n)^2 = 25/n^2$ antes de sumarlo a la varianza $100/n$ para calcular correctamente el ECM. |
| `D-Hab08-26` | Confunde varianza de media con sigma2 | skipped_step | high | Usa $\text{Var}(\bar{Y}_n + a/n) = \sigma^2$ independiente de $n$ | Calcule $\text{Var}(\bar{Y}_n) = \sigma^2/n$ bajo muestreo aleatorio simple, y note que la constante determinista $+5/n$ no altera la varianza. |
| `D-Hab08-27` | Agrega constante a varianza | skipped_step | high | $\text{Var}(\bar{Y}_n + 5/n) = \text{Var}(\bar{Y}_n) + 25/n^2$ | Aplique $\text{Var}(X + a_n) = \text{Var}(X)$ para cualquier término determinista $a_n = 5/n$, que afecta únicamente al sesgo. |
| `D-Hab08-28` | Confunde tasas de caída | conceptual_swap | high | Afirma que el sesgo al cuadrado ($1/n^2$) cae más lento que la varianza ($1/n$) | Compare los exponentes en el denominador: $1/n^2$ decae mucho más rápido que $1/n$ al crecer $n$, por lo que la varianza domina el ECM grande. |
| `D-Hab08-29` | Exige insesgadez exacta | conceptual_swap | high | Concluye que $\hat{\mu}_n = \bar{Y}_n + 5/n$ no es consistente porque $\text{Sesgo}=5/n \ne 0$ | Tome el límite cuando $n \to \infty$: aunque haya sesgo en muestra finita, $5/n \to 0$ y $100/n \to 0$ garantizan $\text{ECM} \to 0$ y consistencia. |
| `D-Hab08-30` | Olvida factor n en Chebyshev | conceptual_swap | high | En $P(|\bar{Y}_n - \mu| > \epsilon) \le \sigma^2/\epsilon^2$ omite dividir por $n$ | Sustituya la varianza del estimador $\text{Var}(\bar{Y}_n) = \sigma^2/n$ en el numerador de Chebyshev, obteniendo $100/(4n) \to 0$. |

#### Formal Mathematical Assumptions (5)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Independencia mutua ($\text{Cov}(Y_i, Y_j) = 0$ para $i \ne j$) y normalidad $Y_i \sim \mathcal{N}(\mu_Y, \sigma_Y^2)$ con $0 < a < 1$ | Sin independencia aparecen covarianzas cruzadas en $\text{Var}(M_B)$, y sin $0<a<1$ no se cumple $a^n \to 0$. | - |
| `A-Hab08-02` | - | Existencia de momentos finitos $E[|X|]<\infty$ y $E[X^2]<\infty$ | Si $E[X^2]$ diverge, la varianza no está definida y la fórmula $E[X^2]-(E[X])^2$ falla. | - |
| `A-Hab08-03` | - | Existencia de esperanza finita $E[|Y_i|]<\infty$ para linealidad | Si la esperanza poblacional no existe, no puede definirse $E[\hat{\theta}]$ ni verificarse insesgadez. | - |
| `A-Hab08-04` | - | Independencia entre $Y_1,\dots,Y_n$ y varianza poblacional finita $\sigma^2<\infty$ | Si las observaciones están correlacionadas, $\text{Var}(\bar{Y})$ incluye covarianzas cruzadas y difiere de $\sigma^2/n$. | - |
| `A-Hab08-05` | - | Observaciones i.i.d. o incorrelacionadas con varianza común $\sigma^2 < \infty$ | Si las observaciones tienen fuerte dependencia persistente, $\text{Var}(\bar{Y}_n)$ puede no caer como $\sigma^2/n$. | - |

---

### [H-01] Espacio Muestral, Axiomas de Kolmogorov y Variable Aleatoria (Concept)

- **Bloom Level:** Remember
- **Session:** Unidad 13: Espacio Muestral y Axiomas de Kolmogorov
- **Prerequisites:** None
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 13), `EST3_LEC07_26.2_V2.pdf` (page 15)

#### Description & Cognitive Model
Definición del espacio muestral $\Omega$, eventos $A\subseteq\Omega$, axiomas de probabilidad de Kolmogorov ($0\le P(A)\le 1$, $P(\Omega)=1$, aditividad disjunta) y variable aleatoria como regla determinista $X:\Omega\to\mathbb{R}$ con distribución inducida $P(X=x)=P(\{\omega:X(\omega)=x\})$.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Suma eventos solapados | conceptual_swap | high | $P(A\cup B)=P(A)+P(B)$ siempre | Reste $P(A\cap B)$ cuando $A$ y $B$ comparten resultados; la suma directa solo vale si $A\cap B=\emptyset$. |
| `D-H01-02` | Confunde omega con muestra | conceptual_swap | high | $\Omega=\{y_1,\dots,y_n\}$ observados | Distinga el espacio muestral $\Omega$ (todos los resultados posibles) de la muestra observada en los datos. |
| `D-H01-03` | Probabilidad fuera de rango | conceptual_swap | high | $P(A)>1$ o $P(A)<0$ | Verifique siempre el primer axioma de Kolmogorov: toda probabilidad debe cumplir $0\le P(A)\le 1$. |
| `D-H01-04` | Espacio muestral incompleto | conceptual_swap | high | $P(\Omega)<1$ | Asegure que $\Omega$ contenga todos los resultados posibles del experimento para satisfacer $P(\Omega)=1$. |
| `D-H01-05` | Multiplica en vez de sumar | conceptual_swap | high | $P(A\cup B)=P(A)P(B)$ | Sume probabilidades (y reste la intersección) para la unión de eventos; el producto aplica a intersecciones independientes. |
| `D-H01-06` | Evento como elemento único | conceptual_swap | high | $A\in\Omega$ en vez de $A\subseteq\Omega$ | Recuerde que $\omega\in\Omega$ es un resultado elemental, mientras que un evento $A\subseteq\Omega$ es un subconjunto. |
| `D-H01-07` | Confunde regla con resultado | conceptual_swap | high | La función $X(\cdot)$ cambia al azar | Aclare que la regla $X(\cdot)$ es fija; lo aleatorio es qué resultado $\omega\in\Omega$ ocurre al realizar el experimento. |
| `D-H01-08` | Igualdad variable y realización | conceptual_swap | high | $X$ es idéntico a $x$ | Separe notación: mayúscula $X$ denota la variable antes de observar y minúscula $x$ el valor realizado después. |
| `D-H01-09` | Ignora multiplicidad en omega | conceptual_swap | high | $P(X=1)=1/4$ con dos monedas | Sume las probabilidades de todos los resultados $\omega\in\Omega$ que producen el mismo número $X(\omega)=x$. |
| `D-H01-10` | Dominio erróneo de X | conceptual_swap | high | $X:\mathbb{R}\to\Omega$ | Recuerde que una variable aleatoria mapea del espacio muestral hacia los reales: $X:\Omega\to\mathbb{R}$. |
| `D-H01-11` | Confunde soporte con omega | conceptual_swap | high | Soporte de $X$ igual a $\Omega$ | Distinga los resultados $\omega\in\Omega$ (cualitativos o simbólicos) de los valores numéricos $x\in\mathbb{R}$ que toma $X$. |
| `D-H01-12` | No normaliza distribución inducida | conceptual_swap | high | $\sum_x P(X=x)\neq 1$ | Verifique que la distribución trasladada desde $\Omega$ sume exactamente $1$ sobre todo el soporte de $X$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-H01-01` | - | Medibilidad de $X$ respecto a la $\sigma$-álgebra $\mathcal{F}$ | Sin medibilidad no puede asignarse probabilidad $P(X=x)$ a los conjuntos preimagen. | - |

---

### [C-20] Ley de los Grandes Números (LGN) (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 40: Ley de los Grandes Números (LGN)
- **Prerequisites:** C-03, H-01
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 40)

#### Description & Cognitive Model
Convergencia en probabilidad $\bar{Y}_n \xrightarrow{p} \mu$ (ley débil) y casi segura $\bar{Y}_n \xrightarrow{a.s.} \mu$ (ley fuerte) del promedio muestral $\bar{Y}_n = \frac{1}{n}\sum_{i=1}^n Y_i$ para observaciones i.i.d. con esperanza finita $\mu$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C20-01` | Exige normalidad original | conceptual_swap | high | $Y_i \sim N(\mu,\sigma^2)$ necesario para LGN | La LGN no requiere normalidad de los datos individuales $Y_i$; solo exige observaciones i.i.d. con esperanza poblacional finita $E[Y_i] = \mu$. |
| `D-C20-02` | Exige varianza finita | conceptual_swap | high | $\sigma^2 < \infty$ indispensable para LGN | Las leyes débil de Khinchine y fuerte de Kolmogorov solo exigen media finita $E[|Y_i|] < \infty$; tener $\sigma^2 < \infty$ solo facilita probarlo vía $\mathrm{Var}(\bar{Y}_n)=\sigma^2/n \to 0$. |
| `D-C20-03` | Confunde LGN con TCL | conceptual_swap | high | $\bar{Y}_n$ se vuelve normal por la LGN | Distinga límite de forma: la LGN establece que $\bar{Y}_n$ converge a la constante $\mu$ (consistencia), mientras que la normalidad asintótica proviene del TCL. |
| `D-C20-04` | Límite en valor individual | conceptual_swap | high | $Y_n \xrightarrow{p} \mu$ | La convergencia se cumple para el promedio acumulado $\bar{Y}_n$, donde los errores se compensan al promediar, no para un dato individual $Y_n$ aislado. |
| `D-C20-05` | Varianza constante | conceptual_swap | high | $\mathrm{Var}(\bar{Y}_n) = \sigma^2$ | Divida la varianza poblacional entre $n$: $\mathrm{Var}(\bar{Y}_n) = \sigma^2/n \to 0$ cuando $n \to \infty$, lo cual garantiza convergencia en media cuadrática y en probabilidad. |
| `D-C20-06` | Muestra finita exacta | conceptual_swap | high | $\bar{Y}_n = \mu$ con $n$ finito | La LGN es un resultado asintótico cuando $n \to \infty$: con $n$ finito el error $|\bar{Y}_n - \mu|$ disminuye en probabilidad, pero no se anula exactamente. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C20-01` | - | Observaciones $Y_1, \dots, Y_n$ i.i.d. con esperanza finita $E[Y_i] = \mu$ | Si la media no es finita (como en Cauchy), el promedio muestral no converge a una constante. | - |

---

### [C-21] Teorema Central del Límite (TCL) (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 42: Teorema Central del Límite (TCL)
- **Prerequisites:** C-20, C-01, C-06
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 42)

#### Description & Cognitive Model
Convergencia en distribución $Z_n = \frac{\bar{Y}_n - \mu}{\sigma/\sqrt{n}} = \frac{\sqrt{n}(\bar{Y}_n - \mu)}{\sigma} \xrightarrow{d} N(0,1)$, equivalente a $\bar{Y}_n \stackrel{a}{\sim} N(\mu, \sigma^2/n)$, sin importar la distribución original de $Y_i$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C21-01` | Omite factor raíz de n | conceptual_swap | high | $\frac{\bar{Y}_n - \mu}{\sigma} \xrightarrow{d} N(0,1)$ | Multiplique el error $\bar{Y}_n - \mu$ por $\sqrt{n}$ porque la desviación estándar de $\bar{Y}_n$ decrece a ritmo $\sigma/\sqrt{n}$; sin $\sqrt{n}$ el límite colapsa a $0$. |
| `D-C21-02` | Varianza sin dividir por n | conceptual_swap | high | $\bar{Y}_n \stackrel{a}{\sim} N(\mu, \sigma^2)$ | Use la varianza de la media muestral $\sigma^2/n$ en $\bar{Y}_n \stackrel{a}{\sim} N(\mu, \sigma^2/n)$, ya que promediar $n$ observaciones reduce la dispersión por un factor $n$. |
| `D-C21-03` | Divide por n sin raíz | conceptual_swap | high | $Z_n = \frac{n(\bar{Y}_n - \mu)}{\sigma}$ | Aplique $\sqrt{n}$ y no $n$ en el numerador de $Z_n$, pues el error estándar de $\bar{Y}_n$ es $\sigma/\sqrt{n}$ y escalar por $n$ haría diverger la varianza. |
| `D-C21-04` | Normalidad de los datos | conceptual_swap | high | $Y_i \stackrel{a}{\sim} N(\mu, \sigma^2)$ | El TCL describe la distribución del promedio $\bar{Y}_n$, no la de cada dato individual $Y_i$, que conserva su distribución poblacional original aunque $n$ crezca. |
| `D-C21-05` | Convergencia en probabilidad | conceptual_swap | high | $Z_n \xrightarrow{p} N(0,1)$ | El TCL establece convergencia en distribución ($\xrightarrow{d}$) hacia $N(0,1)$, porque $Z_n$ converge en forma distribucional y no hacia una constante fija. |
| `D-C21-06` | Aplica con varianza infinita | conceptual_swap | high | $\sigma^2 = \infty$ admite TCL clásico | Verifique la condición $0 < \sigma^2 < \infty$ antes de aplicar el TCL clásico; si la varianza es infinita o nula, la estandarización estándar falla. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C21-01` | - | Observaciones $Y_i$ i.i.d. con media $\mu$ y varianza finita positiva $0 < \sigma^2 < \infty$ | Si $\sigma^2$ es infinita o cero, $Z_n$ no converge a $N(0,1)$. | - |

---

### [Hab-17] Probabilidades Asintóticas e Inferencia de Proporciones con TCL (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 43: Cálculo de Probabilidades Asintóticas con TCL
- **Prerequisites:** C-21
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 43), `EST3_LEC07_26.2_V2.pdf` (page 44)

#### Description & Cognitive Model
Aproximación de probabilidades sobre la media muestral $P(\bar{Y}_n > c) \approx P\left(Z > \frac{c - \mu}{\sigma/\sqrt{n}}\right)$ mediante $\bar{Y}_n \stackrel{a}{\sim} N(\mu, \sigma^2/n)$ e inferencia asintótica para proporciones ($Y_i\sim\mathrm{Bernoulli}(p)$, $\hat{p}\stackrel{a}{\sim}N(p,\frac{p(1-p)}{n})$, $ee(\hat{p})$, $IC_{95\%}$ y efecto $\sqrt{n}$ en tamaño muestral).

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab17-01` | Usa desviación poblacional | skipped_step | high | $Z = \frac{c - \mu}{\sigma}$ | Calcule primero el error estándar de la media $\sigma/\sqrt{n}$ antes de estandarizar; usar $\sigma$ directamente evalúa un individuo y no el promedio de $n$ datos. |
| `D-Hab17-02` | Divide entre n | skipped_step | high | $Z = \frac{c - \mu}{\sigma/n}$ | Recuerde que la varianza de $\bar{Y}_n$ es $\sigma^2/n$, por lo que su desviación estándar es $\sqrt{\sigma^2/n} = \sigma/\sqrt{n}$, no $\sigma/n$. |
| `D-Hab17-03` | Invierte signo de Z | conceptual_swap | high | $P(\bar{Y}_n > c) \approx P(Z < z_c)$ | Conserve el sentido de la desigualdad al estandarizar: si pide $P(\bar{Y}_n > c)$, calcule la cola derecha $1 - \Phi(z_c) = P(Z > z_c)$. |
| `D-Hab17-04` | Confunde aproximado con exacto | conceptual_swap | high | $P_{\text{TCL}}(\bar{Y}_n > c) = P_{\text{exacta}}$ | Reconozca que el TCL da una aproximación asintótica para $n$ grande; en muestras finitas con datos muy asimétricos persiste una leve diferencia frente al valor exacto. |
| `D-Hab17-05` | Invierte resta en Z | conceptual_swap | high | $Z = \frac{\mu - c}{\sigma/\sqrt{n}}$ | Reste siempre la media poblacional $\mu$ al punto de corte $c$ en la estandarización $(c - \mu)/(\sigma/\sqrt{n})$ para no invertir el signo del estadístico $Z$. |
| `D-Hab17-06` | Usa varianza en denominador | conceptual_swap | high | $Z = \frac{c - \mu}{\sigma^2/n}$ | Estandarice dividiendo por la desviación estándar $\sigma/\sqrt{n}$ y no por la varianza $\sigma^2/n$, ya que $Z$ debe quedar adimensional en unidades de error estándar. |
| `D-Hab17-07` | Duplica n para mitad de error | skipped_step | high | $n' = 2n$ reduce margen a la mitad | Cuadruplique el tamaño muestral ($n' = 4n$) para reducir el margen de error a la mitad, ya que el error estándar decrece proporcionalmente a $1/\sqrt{n}$. |
| `D-Hab17-08` | Olvida raíz en ee | skipped_step | high | $ee(\hat{p}) = \frac{\hat{p}(1-\hat{p})}{n}$ | Extraiga la raíz cuadrada de $\hat{p}(1-\hat{p})/n$ para obtener el error estándar antes de multiplicar por el valor crítico $1.96$ del intervalo. |
| `D-Hab17-09` | Omite factor 1-p | conceptual_swap | high | $ee(\hat{p}) = \sqrt{\frac{\hat{p}}{n}}$ | Incluya la varianza Bernoulli completa $\hat{p}(1-\hat{p})$ en el numerador del error estándar, pues $\mathrm{Var}(Y_i) = p(1-p)$ para variables binarias. |
| `D-Hab17-10` | Usa valor crítico erróneo | conceptual_swap | high | $IC_{95\%}: \hat{p} \pm 1.64\,ee(\hat{p})$ | Use $z_{0.975} = 1.96$ para un intervalo bilateral al $95\%$ de confianza, dejando $2.5\%$ en cada cola de la distribución normal estándar. |
| `D-Hab17-11` | Multiplica por 100 parcial | conceptual_swap | high | $ee(\hat{p}) = \sqrt{\frac{55 \times 45}{400}}$ | Exprese tanto $\hat{p}$ como $1-\hat{p}$ en proporciones entre $0$ y $1$ (o ambos en porcentaje coherentemente) antes de calcular el error estándar e intervalo. |
| `D-Hab17-12` | Exige normalidad Bernoulli | conceptual_swap | high | $Y_i \in \{0,1\}$ impide usar TCL | Como $\hat{p} = \bar{Y}_n$ es un promedio de variables Bernoulli con varianza finita $p(1-p)$, el TCL garantiza su normalidad aproximada cuando $n$ es grande. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab17-01` | - | Tamaño muestral $n$ suficientemente grande para mitigar la asimetría de $Y_i$ | Con $n$ pequeño y fuerte asimetría, la aproximación normal presenta errores notables en las colas. | - |
| `A-Hab17-02` | - | Muestra aleatoria i.i.d. de tamaño $n$ grande y $\hat{p}$ reemplaza a $p$ válidamente por Slutsky | Con $n$ pequeño o $p$ muy cercano a $0$ o $1$, la aproximación normal y el reemplazo de $p$ pierden precisión. | - |

---

### [C-22] Teoremas de la Aplicación Continua (CMT) y de Slutsky (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 46: Teorema de la Aplicación Continua (CMT)
- **Prerequisites:** C-20
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 46), `EST3_LEC07_26.2_V2.pdf` (page 48)

#### Description & Cognitive Model
Preservación de la convergencia bajo transformaciones continuas (CMT: si $X_n \xrightarrow{p} c$ y $g$ continua en $c$, $g(X_n) \xrightarrow{p} g(c)$, y análogamente para $\xrightarrow{d}$) y combinación algebraica de límites asintóticos (Teorema de Slutsky: si $B_n \xrightarrow{d} B$ y $A_n \xrightarrow{p} a$, entonces $A_n+B_n\xrightarrow{d}a+B$, $A_n B_n\xrightarrow{d}aB$ y $B_n/A_n\xrightarrow{d}B/a$ para $a\neq 0$).

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C22-01` | Aplica regla a esperanza | conceptual_swap | high | $E[g(X_n)] = g(E[X_n])$ | Separe $\mathrm{plim}$ de esperanza: por la desigualdad de Jensen, $E[g(X)] \neq g(E[X])$ en funciones no lineales, aunque $g(X_n)$ sea consistente vía $\mathrm{plim}$. |
| `D-C22-02` | Omite continuidad en c | conceptual_swap | high | $\mathrm{plim}\,g(X_n) = g(c)$ sin continuidad | Verifique que $g$ sea continua en el límite $c$ (por ejemplo, $\mu \neq 0$ para $g(x)=1/x$); si $g$ salta o explota en $c$, el límite en probabilidad falla. |
| `D-C22-03` | Exige linealidad de g | conceptual_swap | high | CMT solo vale si $g$ es lineal | El CMT vale para cualquier función continua aunque sea no lineal (como raíz cuadrada, cuadrado o recíproco fuera de cero), no requiere linealidad. |
| `D-C22-04` | Confunde consistencia con sesgo | conceptual_swap | high | $g(X_n)$ consistente $\Rightarrow$ insesgado | Recuerde que la consistencia asintótica no implica insesgamiento en muestras finitas: $s = \sqrt{s^2}$ es sesgado para $\sigma$ con $n$ pequeño pero consistente. |
| `D-C22-05` | Restringe a probabilidad | conceptual_swap | high | CMT no aplica a $\xrightarrow{d}$ | El CMT aplica tanto a convergencia en probabilidad ($\xrightarrow{p}$) como a convergencia en distribución ($\xrightarrow{d}$) bajo funciones continuas. |
| `D-C22-06` | Evalúa g en el estimador | conceptual_swap | high | $g(X_n) \xrightarrow{p} g(X)$ aleatorio | Sustituya la constante límite $c = \mathrm{plim}\,X_n$ dentro de $g(\cdot)$ para obtener el límite determinístico $g(c)$ del estimador transformado. |
| `D-C22-07` | Dos en distribución | conceptual_swap | high | $A_n \xrightarrow{d} A, B_n \xrightarrow{d} B \Rightarrow A_n B_n \xrightarrow{d} AB$ | Exija que $A_n$ converja en probabilidad a una constante $a$, no solo en distribución a una variable aleatoria, pues de otro modo la conjunta no está garantizada. |
| `D-C22-08` | División entre cero | conceptual_swap | high | $B_n / A_n \xrightarrow{d} B/0$ si $A_n \xrightarrow{p} 0$ | Verifique siempre que $a \neq 0$ antes de dividir por $A_n$ bajo Slutsky; si $A_n \xrightarrow{p} 0$, el cociente $B_n/A_n$ diverge o queda indeterminado. |
| `D-C22-09` | Eleva grado a probabilidad | conceptual_swap | high | $A_n B_n \xrightarrow{p} aB$ | El producto hereda el modo más débil: como $B_n$ solo converge en distribución hacia una variable aleatoria $B$, el producto $A_n B_n$ converge en distribución ($\xrightarrow{d}$). |
| `D-C22-10` | Omite efecto de a | conceptual_swap | high | $A_n B_n \xrightarrow{d} B$ aunque $a \neq 1$ | Incorpore el valor exacto de la constante límite $a$ en la distribución final ($a+B$, $aB$ o $B/a$); solo desaparece cuando $a=0$ en suma o $a=1$ en producto. |
| `D-C22-11` | Reemplaza por no consistente | conceptual_swap | high | $\hat{\sigma}$ sesgado e inconsistente vale en Slutsky | Asegure que el estimador sustituto $A_n$ sea consistente ($A_n \xrightarrow{p} a$); sin consistencia no se conserva la distribución límite del estadístico. |
| `D-C22-12` | Confunde con independencia | conceptual_swap | high | Slutsky requiere $A_n$ y $B_n$ independientes | Slutsky no requiere independencia entre $A_n$ y $B_n$, justamente porque $A_n$ converge a una constante determinística $a$ y permite usar $s$ junto a $\bar{Y}_n$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C22-01` | - | La función $g(\cdot)$ es continua en el valor límite $c$ (o casi seguramente en el soporte del límite) | Si $g$ presenta discontinuidades en $c$ (como $1/\mu$ en $\mu=0$), $g(X_n)$ no converge a $g(c)$. | - |
| `A-C22-02` | - | La sucesión $A_n$ converge en probabilidad a una constante finita $a$ (y $a \neq 0$ en cocientes) | Si $A_n$ solo converge en distribución o $a=0$ en el denominador, el límite combinado no está garantizado. | - |

---

### [Hab-19] Contraste Asintótico con Varianza Desconocida (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 49: Contraste Asintótico con Varianza Desconocida
- **Prerequisites:** C-21, C-22
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 49)

#### Description & Cognitive Model
Justificación y cálculo del estadístico $t = \frac{\bar{Y}_n - \mu_0}{s/\sqrt{n}} = \frac{\sigma}{s} \cdot \frac{\bar{Y}_n - \mu_0}{\sigma/\sqrt{n}} \xrightarrow{d} N(0,1)$ mediante CMT ($\sigma/s \xrightarrow{p} 1$), TCL bajo $H_0$ y Slutsky para contrastar $H_0: \mu = \mu_0$ al $5\%$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab19-01` | Olvida raíz de n en t | skipped_step | high | $t = \frac{\bar{y} - \mu_0}{s}$ | Divida la desviación estándar muestral $s$ entre $\sqrt{n}$ para formar el error estándar $s/\sqrt{n}$ antes de calcular el estadístico de contraste $t$. |
| `D-Hab19-02` | Exige normalidad para tabla Z | skipped_step | high | Sin $Y_i \sim N$ no vale crítico $1.96$ | Con $n$ grande, el TCL aporta normalidad asintótica de la media sin requerir datos normales, y Slutsky junto con CMT permiten sustituir $\sigma$ por $s$ manteniendo límite $N(0,1)$. |
| `D-Hab19-03` | Regla de rechazo invertida | conceptual_swap | high | Rechaza $H_0$ si $|t| < 1.96$ | Rechace $H_0$ al $5\%$ bilateral únicamente cuando el estadístico cae en las colas extremas ($|t| \ge 1.96$); valores cercanos a cero como $|1.5| < 1.96$ no rechazan $H_0$. |
| `D-Hab19-04` | Usa s cuadrado en lugar de s | conceptual_swap | high | $t = \frac{\bar{y} - \mu_0}{s^2/\sqrt{n}}$ | Use la desviación estándar muestral $s$ (no la varianza $s^2$) en $s/\sqrt{n}$ para que el factor $\sigma/s$ converja en probabilidad a $1$. |
| `D-Hab19-05` | Divide entre n sin raíz | conceptual_swap | high | $t = \frac{\bar{y} - \mu_0}{s/n}$ | Divida $s$ entre $\sqrt{n} = 20$ y no entre $n = 400$, pues el error estándar escala como $1/\sqrt{n}$ en el TCL. |
| `D-Hab19-06` | Ignora prueba bajo H0 | conceptual_swap | high | Evalúa $t$ sin fijar $\mu = \mu_0$ | Centre la diferencia en el valor hipotético $\mu_0$ de $H_0: \mu = \mu_0$, ya que el TCL bajo la hipótesis nula garantiza que $(\bar{Y}_n - \mu_0)/(\sigma/\sqrt{n}) \xrightarrow{d} N(0,1)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab19-01` | - | Muestra grande con varianza finita positiva y consistencia $s^2 \xrightarrow{p} \sigma^2 > 0$ | Si $n$ es pequeño y los datos no son normales, ni el TCL ni la sustitución de $\sigma$ por $s$ garantizan la distribución límite normal. | - |

---

### [Hab-20] Método Delta para Funciones No Lineales (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 50: Método Delta para Funciones No Lineales
- **Prerequisites:** C-21, C-22
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 50)

#### Description & Cognitive Model
Aproximación lineal por Taylor de primer orden: si $\sqrt{n}(\hat{\theta}-\theta)\xrightarrow{d}N(0,V)$ y $g'(\theta)\neq 0$, entonces $\sqrt{n}(g(\hat{\theta})-g(\theta))\xrightarrow{d}N(0,[g'(\theta)]^2 V)$, $ee(g(\hat{\theta}))\approx |g'(\hat{\theta})|\cdot ee(\hat{\theta})$ e $IC_{95\%}$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab20-01` | Transforma el error estándar | skipped_step | high | $ee(g(\hat{\theta})) = g(ee(\hat{\theta}))$ | Multiplique el error estándar original $ee(\hat{\theta})$ por $|g'(\hat{\theta})|$ en vez de aplicar $g(\cdot)$ al error estándar; la incertidumbre escala por la pendiente local. |
| `D-Hab20-02` | Olvida valor absoluto en derivada | skipped_step | high | $ee(g(\hat{\theta})) = g'(\hat{\theta}) \cdot ee(\hat{\theta})$ | Aplique valor absoluto $|g'(\hat{\theta})|$ al calcular el error estándar porque toda desviación estándar o error estándar es no negativo. |
| `D-Hab20-03` | No eleva derivada en varianza | conceptual_swap | high | $\mathrm{Var}_{a}(g(\hat{\theta})) = g'(\theta) V$ | Eleve al cuadrado la derivada en la varianza asintótica $[g'(\theta)]^2 V$, ya que $\mathrm{Var}(aX) = a^2\mathrm{Var}(X)$ en la expansión lineal de Taylor. |
| `D-Hab20-04` | Transforma extremos sin derivada | conceptual_swap | high | $IC(1/\mu) = [1/U, 1/L]$ solo | Para construir el intervalo asintótico simétrico por Método Delta, primero reescale el error estándar mediante $|g'(\hat{\theta})|\cdot ee(\hat{\theta})$ y luego calcule $g(\hat{\theta}) \pm 1.96\,ee(g(\hat{\theta}))$. |
| `D-Hab20-05` | Aplica con derivada nula | conceptual_swap | high | $g'(\theta) = 0$ da aproximación normal | Verifique la condición $g'(\theta) \neq 0$; si la primera derivada se anula, el término lineal de Taylor desaparece y el método delta de primer orden no aplica. |
| `D-Hab20-06` | Omite derivar correctamente | conceptual_swap | high | $g(m) = 1/m \Rightarrow g'(m) = 1/m^2$ | Calcule cuidadosamente la primera derivada $g'(m) = -1/m^2$ antes de evaluarla en $\hat{\theta} = \bar{y}$ para evitar errores de escala en el error estándar. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab20-01` | - | Función $g$ diferenciable en $\theta$ con primera derivada no nula $g'(\theta) \neq 0$ | Si $g'(\theta) = 0$ o $g$ no es derivable en $\theta$, la aproximación lineal de primer orden colapsa. | - |

---
