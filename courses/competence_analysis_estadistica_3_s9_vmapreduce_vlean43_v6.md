# Cognitive Task Analysis (CTA): Estadistica 3 S9 Vmapreduce Vlean43 V6

- **Course ID:** `estadistica_3_s9_vmapreduce_vlean43_v6`
- **Macro-Competency:** Dominio y aplicación analítica integral de Estadistica 3 S9 Vmapreduce Vlean43 V6
- **Structure:** 29 total competencies (1 Facts, 18 Concepts, 10 Skills) with 276 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Sesgo, Eficiencia y ECM | Concept | Understand | Unidad 5: Sesgo, Eficiencia y ECM | - | 18 |
| `Hab-01` | Descomposición del ECM | Skill | Apply | Unidad 6: Descomposición del ECM | C-01 | 24 |
| `Hab-02` | Momentos de Media y Cuasivarianza | Skill | Apply | Unidad 8: Momentos de Media y Cuasivarianza | C-01 | 12 |
| `C-02` | Convergencia en Probabilidad y Consistencia | Concept | Understand | Unidad 10: Convergencia en Probabilidad y Consistencia | C-01 | 18 |
| `C-03` | Convergencia en Media r-ésima y Cuadrática | Concept | Understand | Unidad 11: Convergencia en Media r-ésima y Cuadrática | Hab-01, C-02 | 12 |
| `Hab-03` | Convergencia del Mínimo Exponencial | Skill | Apply | Unidad 12: Convergencia del Mínimo Exponencial | C-03 | 6 |
| `C-04` | Desigualdad de Markov | Concept | Understand | Unidad 14: Desigualdad de Markov | C-02 | 12 |
| `Hab-04` | Desigualdad de Chebyshev | Concept | Apply | Unidad 16: Desigualdad de Chebyshev | C-04 | 18 |
| `C-06` | Desigualdad de Jensen | Concept | Understand | Unidad 18: Desigualdad de Jensen | Hab-04 | 12 |
| `C-07` | Desigualdad de Cauchy-Schwarz | Concept | Understand | Unidad 19: Desigualdad de Cauchy-Schwarz | Hab-04 | 6 |
| `C-08` | Jerarquía de Convergencias Estocásticas | Concept | Analyze | Unidad 21: Jerarquía de Convergencias Estocásticas | Hab-04, C-06 | 12 |
| `Hab-05` | Análisis de Convergencia en Probabilidad vs. Momentos | Skill | Apply | Unidad 23: Análisis de Convergencia en Probabilidad vs. Momentos | C-08 | 6 |
| `Hab-06` | Evaluación de Insesgadez y Consistencia de Estimadores | Skill | Evaluate | Unidad 26: Evaluación de Insesgadez y Consistencia de Estimadores | Hab-04, C-08 | 18 |
| `H-01` | Axiomas de Probabilidad de Kolmogorov | Fact | Remember | Unidad 13: Axiomas de Probabilidad de Kolmogorov | C-01 | 6 |
| `C-09` | Variable Aleatoria y Distribución Inducida | Concept | Understand | Unidad 15: Variable Aleatoria y Distribución Inducida | H-01 | 6 |
| `C-10` | Muestra Aleatoria i.i.d. y Estimador | Concept | Understand | Unidad 3: Muestra Aleatoria i.i.d. y Estimador | C-09 | 6 |
| `C-11` | Esperanza y Varianza de Variable Aleatoria | Concept | Understand | Unidad 17: Esperanza y Varianza de Variable Aleatoria | C-09 | 12 |
| `Hab-11` | Acotación de Probabilidades sin Distribución | Skill | Apply | Unidad 24: Acotación de Probabilidades sin Distribución | C-04, Hab-04 | 6 |
| `Hab-12` | Cuantificación de Sesgo en Transformaciones No Lineales | Skill | Apply | Unidad 26: Cuantificación de Sesgo en Transformaciones No Lineales | C-06 | 6 |
| `C-22` | Convergencia Casi Segura | Concept | Understand | Unidad 33: Convergencia Casi Segura | C-02 | 6 |
| `C-23` | Convergencia en Distribución | Concept | Understand | Unidad 35: Convergencia en Distribución | C-02 | 6 |
| `C-25` | Ley de los Grandes Números (LGN) | Concept | Understand | Unidad 40: Ley de los Grandes Números (LGN) | C-02, C-10 | 6 |
| `C-26` | Teorema Central del Límite (TCL) | Concept | Understand | Unidad 42: Teorema Central del Límite (TCL) | C-25 | 6 |
| `Hab-14` | Aproximación Normal de Probabilidades Muestrales | Skill | Apply | Unidad 43: Aproximación Normal de Probabilidades Muestrales | C-26 | 6 |
| `Hab-15` | Intervalos de Confianza Asintóticos para Proporciones | Skill | Apply | Unidad 44: Intervalos de Confianza Asintóticos para Proporciones | C-26 | 6 |
| `C-27` | Teorema de la Aplicación Continua | Concept | Understand | Unidad 46: Teorema de la Aplicación Continua | C-25 | 6 |
| `C-28` | Teorema de Slutsky | Concept | Understand | Unidad 48: Teorema de Slutsky | C-26, C-27 | 6 |
| `C-29` | El Método Delta | Concept | Understand | Unidad 50: El Método Delta | C-26 | 6 |
| `Hab-16` | Cálculo de Error Estándar e IC por Método Delta | Skill | Apply | Unidad 51: Cálculo de Error Estándar e IC por Método Delta | C-29 | 6 |

---

## Detailed Competency Specifications

### [C-01] Sesgo, Eficiencia y ECM (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 5: Sesgo, Eficiencia y ECM
- **Prerequisites:** None
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 5), `EST3_LEC07_26.2_V2.pdf` (page 5), `EST3_LEC07_26.2_V2.pdf` (page 7)

#### Description & Cognitive Model
Definición en muestras finitas de sesgo $\text{Sesgo}(\hat{\theta}_n)=\mathbb{E}[\hat{\theta}_n]-\theta$, insesgadez ($\mathbb{E}[\hat{\theta}_n]=\theta$), varianza, error estándar $ee(\hat{\theta})=\sqrt{\text{Var}(\hat{\theta})}$, eficiencia relativa y Error Cuadrático Medio $\text{ECM}(\hat{\theta}_n)=\mathbb{E}[(\hat{\theta}_n-\theta)^2]$.

#### Fused Distractor Models (18)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Signo del sesgo | conceptual_swap | high | $\text{Sesgo}(\hat{\theta}_n)=\theta-\mathbb{E}[\hat{\theta}_n]$ | Reste siempre el parámetro verdadero a la esperanza del estimador: un sesgo positivo indica sobreestimación sistemática. |
| `D-C01-02` | Confunde estimador | conceptual_swap | high | $\hat{\theta}_n$ es un número fijo | Distinga el estimador como variable aleatoria con distribución muestral de la estimación puntual numérica obtenida en una muestra. |
| `D-C01-03` | Insesgadez puntual | conceptual_swap | high | $\hat{\theta}_n=\theta$ en cada muestra | Aplique el operador esperanza $\mathbb{E}[\hat{\theta}_n]=\theta$: la insesgadez es una propiedad promedio sobre muestras repetidas, no puntual. |
| `D-C01-04` | Eficiencia por sesgo | conceptual_swap | high | Más eficiente si menor sesgo | Compare las varianzas $\text{Var}(\hat{\theta}_{1,n})<\text{Var}(\hat{\theta}_{2,n})$ entre estimadores insesgados, o verifique que la diferencia matricial sea semidefinida positiva. |
| `D-C01-05` | ECM lineal | conceptual_swap | high | $\text{ECM}(\hat{\theta}_n)=\mathbb{E}[|\hat{\theta}_n-\theta|]$ | Eleve al cuadrado la desviación $(\hat{\theta}_n-\theta)^2$ dentro de la esperanza para definir correctamente el Error Cuadrático Medio. |
| `D-C01-06` | Matriz negativa | conceptual_swap | high | $\text{Var}(\hat{\theta}_2)-\text{Var}(\hat{\theta}_1)\preceq 0$ | Verifique que $\mathbf{c}^\top[\text{Var}(\hat{\theta}_{2,n})-\text{Var}(\hat{\theta}_{1,n})]\mathbf{c}\ge 0$ para todo $\mathbf{c}\ne 0$, garantizando menor varianza en toda combinación lineal. |
| `D-C01-07` | Insesgadez por muestra | conceptual_swap | high | Insesgado significa $\hat{\theta}=\theta$ siempre | Comprenda que la insesgadez refiere al promedio $E[\hat{\theta}]=\theta$ sobre infinitas muestras. |
| `D-C01-08` | Signo invertido en sesgo | conceptual_swap | high | $\text{Sesgo}(\hat{\theta})=\theta-E[\hat{\theta}]$ | Calcule siempre $E[\hat{\theta}]-\theta$ para que un sesgo negativo indique subestimación sistemática. |
| `D-C01-09` | Confunde sesgo con error | conceptual_swap | high | $\text{Sesgo}(\hat{\theta})=\hat{\theta}-\theta$ | Tome la esperanza $E[\hat{\theta}]$ antes de restar $\theta$, pues el sesgo es determinista. |
| `D-C01-10` | Insesgado implica precisión | conceptual_swap | high | Todo estimador insesgado tiene $\text{Var}=0$ | Separe centrado ($E[\hat{\theta}]=\theta$) de dispersión ($\text{Var}(\hat{\theta})$): un insesgado puede variar mucho. |
| `D-C01-11` | Sesgo relativo | conceptual_swap | high | $\text{Sesgo}(\hat{\theta})=E[\hat{\theta}]/\theta$ | Defina el sesgo como diferencia aditiva $E[\hat{\theta}]-\theta$, nula exactamente cuando $E[\hat{\theta}]=\theta$. |
| `D-C01-12` | Propiedad del parámetro | conceptual_swap | high | El sesgo depende solo de $\theta$ | Atribuya el sesgo a la regla de estimación $\hat{\theta}$, pues distintos estimadores tienen distinto sesgo. |
| `D-C01-13` | Eficiencia sin insesgadez | conceptual_swap | high | Menor varianza implica más eficiente siempre | Compare varianzas por eficiencia solo entre estimadores que cumplan ambos ser insesgados. |
| `D-C01-14` | Confunde varianza y ee | conceptual_swap | high | $ee(\hat{\theta})=\text{Var}(\hat{\theta})$ | Tome raíz cuadrada $ee(\hat{\theta})=\sqrt{\text{Var}(\hat{\theta})}$ para expresar precisión en unidades de $\theta$. |
| `D-C01-15` | Varianza lineal en 1/n | conceptual_swap | high | $\text{Var}(\bar{Y})=\sigma^2/n^2$ o $\sigma^2$ | Aplique $\text{Var}(\frac{1}{n}\sum Y_i)=\frac{1}{n^2}(n\sigma^2)=\frac{\sigma^2}{n}$ usando independencia muestral. |
| `D-C01-16` | Mayor varianza es mejor | conceptual_swap | high | Más varianza significa más eficiencia | Asociar menor varianza con estimaciones más concentradas alrededor de $\theta$, luego mayor eficiencia. |
| `D-C01-17` | Error estándar lineal en n | conceptual_swap | high | $ee(\bar{Y})=\sigma/n$ | Divida $\sigma$ entre $\sqrt{n}$ porque la raíz cuadrada actúa sobre $\text{Var}(\bar{Y})=\sigma^2/n$. |
| `D-C01-18` | Descarta información igual | conceptual_swap | high | $Y_1$ y $\bar{Y}$ tienen igual precisión | Use toda la muestra mediante $\bar{Y}$ para reducir la varianza en un factor $n$ frente a $Y_1$. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Segundo momento finito $\mathbb{E}[\hat{\theta}_n^2]<\infty$ | Sin segundo momento finito no existen la varianza ni el ECM del estimador. | - |
| `A-C01-02` | - | Existencia de la esperanza $E[\hat{\theta}]<\infty$ | Si no existe esperanza, no puede definirse el sesgo. | - |
| `A-C01-03` | - | Independencia de $Y_i$ y varianza finita $\sigma^2<\infty$ | Si hay correlación o $\sigma^2=\infty$, falla $\text{Var}(\bar{Y})=\sigma^2/n$. | - |

---

### [Hab-01] Descomposición del ECM (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 6: Descomposición del ECM
- **Prerequisites:** C-01
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 6), `EST3_LEC07_26.2_V2.pdf` (page 6), `EST3_LEC07_26.2_V2.pdf` (page 9), `EST3_LEC07_26.2_V2.pdf` (page 10)

#### Description & Cognitive Model
Demostración algebraica y aplicación de la identidad $\text{ECM}(\hat{\theta}_n)=\text{Var}(\hat{\theta}_n)+[\text{Sesgo}(\hat{\theta}_n)]^2$ en casos escalar y multivariado, incluyendo evaluación de sesgo por linealidad y comparación de estimadores de contracción $c\bar{Y}$.

#### Fused Distractor Models (24)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Omite cuadrado sesgo | skipped_step | high | $\text{ECM}=\text{Var}(\hat{\theta}_n)+\text{Sesgo}(\hat{\theta}_n)$ | Eleve al cuadrado el sesgo al expandir el binomio $(\hat{\theta}_n-\mathbb{E}[\hat{\theta}_n]+\mathbb{E}[\hat{\theta}_n]-\theta)^2$ para preservar unidades cuadráticas. |
| `D-Hab01-02` | Término cruzado vivo | skipped_step | high | $\text{ECM}=\text{Var}+2\text{Cov}+\text{Sesgo}^2$ | Aplique linealidad de la esperanza en el término cruzado: $\mathbb{E}[\hat{\theta}_n-\mathbb{E}[\hat{\theta}_n]]=0$ anula exactamente el doble producto. |
| `D-Hab01-03` | Resta sesgo cuadrado | conceptual_swap | high | $\text{ECM}=\text{Var}(\hat{\theta}_n)-[\text{Sesgo}(\hat{\theta}_n)]^2$ | Sume ambos componentes no negativos: tanto la varianza como el sesgo al cuadrado penalizan e incrementan el Error Cuadrático Medio. |
| `D-Hab01-04` | Transpuesta invertida | conceptual_swap | high | $\text{Sesgo}^\top\text{Sesgo}$ en matriz ECM | Use el producto externo $\text{Sesgo}(\hat{\theta}_n)\text{Sesgo}(\hat{\theta}_n)^\top$ para obtener una matriz de dimensión $k\times k$ compatible con $\text{Var}(\hat{\theta}_n)$. |
| `D-Hab01-05` | Insesgado óptimo | conceptual_swap | high | Todo insesgado minimiza el ECM | Evalúe la suma $\text{Var}+[\text{Sesgo}]^2$: un estimador con sesgo pequeño y varianza mucho menor puede lograr menor ECM total. |
| `D-Hab01-06` | Centro en parámetro | conceptual_swap | high | $\text{Var}(\hat{\theta}_n)=\mathbb{E}[(\hat{\theta}_n-\theta)^2]$ | Centre la varianza en $\mathbb{E}[\hat{\theta}_n]$ y no en $\theta$; solo coinciden con el ECM cuando el estimador es exactamente insesgado. |
| `D-Hab01-07` | Saca constante sin multiplicar | skipped_step | high | $E[c\bar{Y}]=E[\bar{Y}]=\mu$ | Aplique linealidad $E[c\bar{Y}]=cE[\bar{Y}]=c\mu$ antes de restar $\mu$ en el sesgo. |
| `D-Hab01-08` | Olvida restar mu | skipped_step | high | $\text{Sesgo}(c\bar{Y})=c\mu$ | Reste el parámetro verdadero $\mu$ a $E[c\bar{Y}]=c\mu$ para obtener $(c-1)\mu$. |
| `D-Hab01-09` | Divide por n dos veces | conceptual_swap | high | $E[\bar{Y}]=\frac{1}{n^2}\sum E[Y_i]=\mu/n$ | Conserve el factor $1/n$ lineal al sumar $n$ esperanzas iguales a $\mu$: $\frac{1}{n}(n\mu)=\mu$. |
| `D-Hab01-10` | Invierte c-1 | conceptual_swap | high | $\text{Sesgo}(c\bar{Y})=(1-c)\mu$ | Calcule $c\mu-\mu=(c-1)\mu$ respetando el orden $E[\hat{\mu}]-\mu$ para conservar el signo. |
| `D-Hab01-11` | Aplica potencia al escalar | conceptual_swap | high | $E[c\bar{Y}]=c^2\mu$ | Distinga esperanza ($E[cX]=cE[X]$) de varianza ($\text{Var}(cX)=c^2\text{Var}(X)$). |
| `D-Hab01-12` | Exige c=0 para sesgo nulo | conceptual_swap | high | $\text{Sesgo}(c\bar{Y})=0$ si $c=0$ | Resuelva $(c-1)\mu=0$ para verificar que el estimador $c\bar{Y}$ solo es insesgado si $c=1$. |
| `D-Hab01-13` | Olvida elevar sesgo | conceptual_swap | high | $\text{ECM}(\hat{\theta})=\text{Var}(\hat{\theta})+\text{Sesgo}(\hat{\theta})$ | Eleve el sesgo al cuadrado $[\text{Sesgo}(\hat{\theta})]^2$ para igualar unidades cuadráticas y evitar cancelaciones. |
| `D-Hab01-14` | Término cruzado no nulo | conceptual_swap | high | $\text{ECM}=\text{Var}+\text{Sesgo}^2+2\,\text{cruzado}$ | Factorice $2(E[\hat{\theta}]-\theta)E[\hat{\theta}-E[\hat{\theta}]]$ y note que $E[\hat{\theta}-E[\hat{\theta}]]=0$. |
| `D-Hab01-15` | Insesgado siempre gana | conceptual_swap | high | Un estimador sesgado nunca supera a uno insesgado | Compare el ECM total: un estimador con poco sesgo puede ganar si reduce mucho la varianza. |
| `D-Hab01-16` | Resta el sesgo cuadrado | conceptual_swap | high | $\text{ECM}=\text{Var}(\hat{\theta})-[\text{Sesgo}(\hat{\theta})]^2$ | Sume ambos componentes no negativos, pues tanto el sesgo como la varianza alejan de $\theta$. |
| `D-Hab01-17` | Confunde ECM con ee | conceptual_swap | high | $\text{ECM}(\hat{\theta})=ee(\hat{\theta})$ si es insesgado | Recuerde que si $\text{Sesgo}(\hat{\theta})=0$, entonces $\text{ECM}(\hat{\theta})=\text{Var}(\hat{\theta})$ y no su raíz. |
| `D-Hab01-18` | Confunde ECM con sesgo | conceptual_swap | high | $\text{ECM}(\hat{\theta})=E[\hat{\theta}-\theta]$ | Incluya el cuadrado $(\hat{\theta}-\theta)^2$ para medir distancia cuadrática promedio al parámetro. |
| `D-Hab01-19` | Escala lineal en varianza | skipped_step | high | $\text{Var}(c\bar{Y})=c\,\text{Var}(\bar{Y})$ | Eleve al cuadrado la constante $c$ al sacarla de la varianza: $\text{Var}(c\bar{Y})=c^2\text{Var}(\bar{Y})$. |
| `D-Hab01-20` | Omite cuadrado en sesgo | skipped_step | high | $\text{ECM}=c^2\text{Var}(\bar{Y})+(c-1)\mu$ | Eleve el sesgo $-0.2$ al cuadrado antes de sumarlo a la varianza: $(-0.2)^2=0.040$. |
| `D-Hab01-21` | Usa $sigma^2$ sin dividir por n | conceptual_swap | high | $\text{Var}(\bar{Y})=\sigma^2$ | Divida la varianza poblacional $\sigma^2$ entre el tamaño de muestra $n$ para obtener $\text{Var}(\bar{Y})$. |
| `D-Hab01-22` | Elige mayor ECM | conceptual_swap | high | Mejor estimador es el de mayor ECM | Seleccione el estimador con menor ECM, ya que minimiza la distancia cuadrática promedio a $\theta$. |
| `D-Hab01-23` | Olvida sesgo de $cY_bar$ | conceptual_swap | high | $\text{ECM}(c\bar{Y})=\text{Var}(c\bar{Y})$ | Incluya el término $[\text{Sesgo}(c\bar{Y})]^2=(c-1)^2\mu^2$ porque $c\neq 1$ introduce sesgo. |
| `D-Hab01-24` | Error en $Sesgo^2$ negativo | conceptual_swap | high | $(-0.2)^2=-0.040$ | Verifique que el cuadrado de un sesgo negativo siempre es positivo: $(-0.2)^2=+0.040$. |

#### Formal Mathematical Assumptions (4)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Linealidad del operador esperanza $\mathbb{E}[aX+b]=a\mathbb{E}[X]+b$ | Sin linealidad no se factoriza el término determinístico ni se anula el término cruzado. | - |
| `A-Hab01-02` | - | Media poblacional común $E[Y_i]=\mu$ para todo $i$ | Sin media común, $E[\bar{Y}]$ no equivale a $\mu$. | - |
| `A-Hab01-03` | - | Segundo momento finito $E[\hat{\theta}^2]<\infty$ | Si no existe segundo momento, el ECM es infinito. | - |
| `A-Hab01-04` | - | Parámetros conocidos o especificados $\mu,\sigma^2$ para la comparación puntual | Sin valores de $\mu,\sigma^2$, no se ordenan numéricamente los ECM. | - |

---

### [Hab-02] Momentos de Media y Cuasivarianza (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 8: Momentos de Media y Cuasivarianza
- **Prerequisites:** C-01
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 8), `EST3_LEC07_26.2_V2.pdf` (page 11)

#### Description & Cognitive Model
Deducción sin normalidad de $\mathbb{E}[\bar{Y}_n]=\mu$, $\text{Var}(\bar{Y}_n)=\sigma^2/n$, $\mathbb{E}[S_n^2]=\sigma^2$ y el sesgo $-\sigma^2/n$ del estimador $m_2$

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Varianza sin cuadrado | skipped_step | high | $\text{Var}(\bar{Y}_n)=\frac{\sigma^2}{n^2}$ o $\frac{\sigma^2}{\sqrt{n}}$ | Extraiga el factor $1/n$ al cuadrado de la varianza: $(1/n)^2\cdot n\sigma^2=\sigma^2/n$ gracias a la independencia de las observaciones. |
| `D-Hab02-02` | Suma respecto a mu | skipped_step | high | $\mathbb{E}[\sum(Y_i-\bar{Y}_n)^2]=n\sigma^2$ | Reste el término $-n\mathbb{E}[(\bar{Y}_n-\mu)^2]=-\sigma^2$ tras centrar en $\mu$, obteniendo $(n-1)\sigma^2$ por el grado de libertad consumido. |
| `D-Hab02-03` | Sesgo positivo en m2 | conceptual_swap | high | $\mathbb{E}[m_2]=\frac{n+1}{n}\sigma^2>\sigma^2$ | Recuerde que $\bar{Y}_n$ minimiza la suma de desviaciones cuadráticas en la muestra, por lo que $m_2$ subestima $\sigma^2$ con sesgo $-\sigma^2/n$. |
| `D-Hab02-04` | Exige normalidad | conceptual_swap | high | $S_n^2$ solo es insesgado si $Y_i\sim\mathcal{N}$ | Aplique únicamente finitud de $\mu$ y $\sigma^2$ junto con independencia: la demostración por momentos no requiere distribución gaussiana. |
| `D-Hab02-05` | Olvida covarianzas nulas | conceptual_swap | high | $\text{Var}(\sum Y_i)=n\sigma^2+n(n-1)\sigma^2$ | Use el supuesto de muestra aleatoria simple (i.i.d.) para anular todas las covarianzas cruzadas $\text{Cov}(Y_i,Y_j)=0$ con $i\ne j$. |
| `D-Hab02-06` | Insesgadez de $S_n$ | conceptual_swap | high | $\mathbb{E}[S_n]=\sigma$ | Note que la raíz cuadrada es cóncava; por la desigualdad de Jensen, $\mathbb{E}[S_n]<\sqrt{\mathbb{E}[S_n^2]}=\sigma$, luego $S_n$ es sesgado. |
| `D-Hab02-07` | Divide $s^2$ entre n | skipped_step | high | $s^2=\frac{1}{n}\sum (Y_i-\bar{Y})^2$ | Divida la suma de cuadrados entre $n-1$ en $s^2$ para corregir el grado de libertad gastado por $\bar{Y}$. |
| `D-Hab02-08` | Omite cuadrado en desvíos | skipped_step | high | $\sum (Y_i-\bar{Y})$ en vez de $\sum (Y_i-\bar{Y})^2$ | Eleve cada desvío $Y_i-\bar{Y}$ al cuadrado antes de sumarlos, pues los desvíos simples suman cero. |
| `D-Hab02-09` | No centra en la media | conceptual_swap | high | $s^2=\frac{1}{n-1}\sum Y_i^2$ | Reste primero la media muestral $\bar{Y}$ a cada observación antes de elevar al cuadrado. |
| `D-Hab02-10` | Invierte sesgo de m2 | conceptual_swap | high | $E[m_2]=\frac{n}{n-1}\sigma^2$ | Recuerde que $E[m_2]=\frac{n-1}{n}\sigma^2<\sigma^2$, por lo que $m_2$ subestima $\sigma^2$ en $-\sigma^2/n$. |
| `D-Hab02-11` | Sesgo de $s^2$ no nulo | conceptual_swap | high | $E[s^2]=\frac{n-1}{n}\sigma^2$ | Verifique que dividir entre $n-1$ cancela el factor $\frac{n-1}{n}$ y vuelve insesgada a $s^2$. |
| `D-Hab02-12` | Error al calcular media | conceptual_swap | high | $\bar{y}$ es la mediana o suma sin dividir | Calcule primero $\bar{y}=\frac{1}{n}\sum_{i=1}^n y_i$ antes de construir los desvíos $y_i-\bar{y}$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Muestra aleatoria simple i.i.d. con $\mathbb{E}[Y_i]=\mu$ y $\text{Var}(Y_i)=\sigma^2<\infty$ | Sin independencia se agregan covarianzas cruzadas y sin varianza finita no existen los momentos. | - |
| `A-Hab02-02` | - | Tamaño muestral $n\ge 2$ para evitar división por cero | Si $n=1$, $s^2$ queda indeterminada por $n-1=0$. | - |

---

### [C-02] Convergencia en Probabilidad y Consistencia (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 10: Convergencia en Probabilidad y Consistencia
- **Prerequisites:** C-01
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 10), `EST3_LEC07_26.2_V2.pdf` (page 19), `EST3_LEC07_26.2_V2.pdf` (page 27)

#### Description & Cognitive Model
Sucesiones de variables aleatorias $\{X_n\}_{n=1}^\infty$, definición formal de convergencia en probabilidad $\text{plim}_{n\to\infty}X_n=c$ mediante $\lim_{n\to\infty}\mathbb{P}(|X_n-c|>\varepsilon)=0$ y consistencia débil $\hat{\theta}_n\xrightarrow{p}\theta$.

#### Fused Distractor Models (18)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Límite de esperanzas | conceptual_swap | high | $\text{plim } X_n=c\iff\lim\mathbb{E}[X_n]=c$ | Separe ambos conceptos: la convergencia en probabilidad exige que la masa fuera de $[c-\varepsilon,c+\varepsilon]$ tienda a cero para todo $\varepsilon>0$. |
| `D-C02-02` | Epsilon fijo grande | conceptual_swap | high | Basta probar $\mathbb{P}(|X_n-c|>\varepsilon)\to 0$ para $\varepsilon=1$ | Exija el cuantificador universal $\forall\varepsilon>0$: la probabilidad de las colas debe colapsar incluso para bandas arbitrariamente estrechas. |
| `D-C02-03` | Sentido de desigualdad | conceptual_swap | high | $\lim_{n\to\infty}\mathbb{P}(|X_n-c|>\varepsilon)=1$ | Invierta el límite según el evento: la probabilidad fuera de la banda tiende a $0$, mientras que dentro de $|X_n-c|\le\varepsilon$ tiende a $1$. |
| `D-C02-04` | Colapso a punto en VA | conceptual_swap | high | $X_n\xrightarrow{p} X$ implica $X_n$ degenera en punto | Diferencie el límite constante del aleatorio: hacia $X$, la diferencia $|X_n-X|$ colapsa en cero manteniendo la distribución de $X$. |
| `D-C02-05` | Consistencia vs insesgadez | conceptual_swap | high | Insesgado en finitas equivale a consistente | Verifique si la varianza decrece con $n$: un estimador insesgado cuya varianza no colapsa a cero no converge en probabilidad a $\theta$. |
| `D-C02-06` | Solo un parámetro | conceptual_swap | high | Consistencia vale para un único $\theta_0$ | Exija consistencia para todo $\theta\in\Theta$ en el espacio paramétrico, garantizando validez sin conocer el valor verdadero. |
| `D-C02-07` | Confunde término y sucesión | conceptual_swap | high | $X_n$ y $\{X_n\}_{n=1}^\infty$ son lo mismo | Distinga $X_n$ (un término para tamaño $n$) de $\{X_n\}_{n=1}^\infty$ (toda la sucesión indexada). |
| `D-C02-08` | Sucesión determinista | conceptual_swap | high | $\{X_n\}$ converge como números reales | Reconozca que cada término $X_n$ es aleatorio, por lo que converger admite distintos sentidos. |
| `D-C02-09` | Peso constante por dato | conceptual_swap | high | Cada dato nuevo pesa igual al crecer $n$ | Note que en $\bar{Y}_n$ cada observación nueva aporta solo $1/n$, estabilizando el promedio. |
| `D-C02-10` | Confunde índice con valor | conceptual_swap | high | $n$ es el valor de la variable | Interprete $n$ como el tamaño de muestra o posición en la lista, no como el valor observado. |
| `D-C02-11` | Muestra fija | conceptual_swap | high | Cambiar $n$ no genera nueva variable | Considere que cada nuevo $n$ define una nueva variable aleatoria sobre la muestra acumulada. |
| `D-C02-12` | Estabilización instantánea | conceptual_swap | high | Con $n=5$ ya alcanza el límite | Distinga fluctuaciones iniciales finitas del comportamiento asintótico cuando $n\to\infty$. |
| `D-C02-13` | Convergencia determinista | conceptual_swap | high | $X_n \xrightarrow{p} c$ significa que $|X_n - c| = 0$ para $n$ grande | Recuerde que la convergencia en probabilidad permite desviaciones, haciendo su probabilidad nula al crecer $n$. |
| `D-C02-14` | Valor único de epsilon | conceptual_swap | high | Basta que $P(|X_n - c| > \epsilon) \to 0$ para $\epsilon = 1$ | Exija que el límite sea cero para todo $\epsilon > 0$ arbitrariamente pequeño. |
| `D-C02-15` | Confunde con esperanza | conceptual_swap | high | $\operatorname{plim} X_n = c$ equivale a $E[X_n] = c$ para todo $n$ | Distinga que $\operatorname{plim}$ describe la concentración probabilística asintótica cuando $n \to \infty$, no la media finita. |
| `D-C02-16` | Sentido desigualdad | conceptual_swap | high | $X_n \xrightarrow{p} c \iff \lim_{n\to\infty} P(|X_n - c| \le \epsilon) = 0$ | Verifique que la probabilidad de alejarse ($> \epsilon$) tiende a $0$, mientras la de acercarse ($\le \epsilon$) tiende a $1$. |
| `D-C02-17` | Fija n finito | conceptual_swap | high | Un estimador consistente tiene error cero con $n = 1000$ | Interprete la consistencia como un límite asintótico ($n \to \infty$); con $n$ finito siempre hay probabilidad residual. |
| `D-C02-18` | Niega continuidad plim | conceptual_swap | high | Si $\hat{\theta}_n \xrightarrow{p} \theta$, entonces $g(\hat{\theta}_n) \not\xrightarrow{p} g(\theta)$ | Recuerde que, a diferencia de la esperanza, el $\operatorname{plim}$ sí pasa a través de funciones continuas. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | Sucesión de variables aleatorias $\{X_n\}_{n=1}^\infty$ en un espacio $(\Omega,\mathcal{F},\mathbb{P})$ común | Sin espacio común no está definida la variable diferencia $X_n-X$ ni su probabilidad. | - |
| `A-C02-02` | - | Proceso generador bien definido para todo tamaño $n\in\mathbb{N}$ | Sin extensión a todo $n$, no existe límite asintótico. | - |
| `A-C02-03` | - | La sucesión $\{X_n\}$ está definida sobre un espacio de probabilidad común para todo $n \ge 1$ | Sin espacio de probabilidad bien definido no existe $P(|X_n - c| > \epsilon)$. | - |

---

### [C-03] Convergencia en Media r-ésima y Cuadrática (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 11: Convergencia en Media r-ésima y Cuadrática
- **Prerequisites:** Hab-01, C-02
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 11), `EST3_LEC07_26.2_V2.pdf` (page 29)

#### Description & Cognitive Model
Definición de convergencia en norma $L^r$ y media cuadrática $X_n \xrightarrow{m.s.} c \iff \lim_{n\to\infty}\mathbb{E}[(X_n-c)^2]=0$, equivalente a insesgadez asintótica y colapso de varianza, implicando $X_n \xrightarrow{p} c$.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Solo varianza cero | conceptual_swap | high | $\text{Var}(X_n)\to 0\Rightarrow X_n\xrightarrow{\text{m.s.}} c$ | Compruebe ambas condiciones del Teorema 3.4: si la varianza colapsa pero $\mathbb{E}[X_n]\to b\ne c$, el ECM converge a $(b-c)^2>0$. |
| `D-C03-02` | Solo insesgadez asintótica | conceptual_swap | high | $\mathbb{E}[X_n]\to c\Rightarrow X_n\xrightarrow{\text{m.s.}} c$ | Verifique también $\lim_{n\to\infty}\text{Var}(X_n)=0$; sin colapso de varianza, la dispersión alrededor de $c$ persiste en el límite. |
| `D-C03-03` | Inversa con probabilidad | conceptual_swap | high | $X_n\xrightarrow{p} c\Rightarrow X_n\xrightarrow{\text{m.s.}} c$ | Recuerde que la implicación va solo de $L^2$ hacia probabilidad: colas con probabilidad decreciente pero valores grandes hacen divergir el ECM. |
| `D-C03-04` | Sin momentos finitos | conceptual_swap | high | $L^r$ aplica aunque $\mathbb{E}[|X_n|^r]=\infty$ | Verifique primero que $\mathbb{E}[|X_n|^r]<\infty$ y $\mathbb{E}[|X|^r]<\infty$; de lo contrario la distancia en norma $L^r$ no está definida. |
| `D-C03-05` | Exponente r en norma | conceptual_swap | high | $\mathbb{E}[|X_n-X|]^r\to 0$ fuera del operador | Evalúe la esperanza del error elevado a la potencia $r$, $\mathbb{E}[|X_n-X|^r]\to 0$, donde las desviaciones grandes pesan más si $r>1$. |
| `D-C03-06` | Valor absoluto en L2 | conceptual_swap | high | $X_n\xrightarrow{\text{m.s.}} c \iff \mathbb{E}[|X_n-c|]\to 0$ | Distinga $r=1$ (media absoluta) de $r=2$ (media cuadrática); $L^2$ corresponde a $\mathbb{E}[(X_n-c)^2]\to 0$ y es más exigente. |
| `D-C03-07` | Solo sesgo a cero | conceptual_swap | high | $E[X_n] \to c$ basta para que $X_n \xrightarrow{m.s.} c$ | Verifique ambas condiciones simultáneamente: tanto el sesgo como la varianza $\operatorname{Var}(X_n)$ deben tender a cero. |
| `D-C03-08` | Solo varianza a cero | conceptual_swap | high | $\operatorname{Var}(X_n) \to 0$ basta para que $X_n \xrightarrow{m.s.} c$ | Recuerde que $\operatorname{Var}(X_n) \to 0$ sin sesgo nulo solo concentra al estimador alrededor de un valor incorrecto. |
| `D-C03-09` | Implicación inversa | conceptual_swap | high | $X_n \xrightarrow{p} c \Rightarrow X_n \xrightarrow{m.s.} c$ siempre | Recuerde que la implicación va de $m.s.$ hacia $p$ (vía Markov); pueden existir variables sin momentos que convergen en probabilidad. |
| `D-C03-10` | Usa desviación sin cuadrado | conceptual_swap | high | $E[|X_n - c|] \to 0$ define la convergencia en media cuadrática | Incluya el cuadrado en $E[(X_n - c)^2]$ para poder descomponerlo en $\operatorname{Var}(X_n) + \operatorname{Sesgo}^2$. |
| `D-C03-11` | Suma sesgo lineal | conceptual_swap | high | $\operatorname{ECM} = \operatorname{Var}(X_n) + \operatorname{Sesgo}(X_n)$ | Eleve el sesgo al cuadrado en $\operatorname{ECM} = \operatorname{Var}(X_n) + (E[X_n]-c)^2$. |
| `D-C03-12` | Sesgo finito impide m.s. | conceptual_swap | high | Si $E[X_n] \ne c$ para todo $n$ finito, entonces $X_n \not\xrightarrow{m.s.} c$ | Permita sesgo en muestras finitas siempre que $\operatorname{Sesgo}(X_n) \to 0$ cuando $n \to \infty$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Existencia de momentos absolutos de orden $r$: $\mathbb{E}[|X_n|^r]<\infty$ y $\mathbb{E}[|X|^r]<\infty$ | Si el momento de orden $r$ es infinito, no puede evaluarse la convergencia en $L^r$. | - |
| `A-C03-02` | - | Existen los segundos momentos $E[X_n^2] < \infty$ para todo $n$ | Sin segundo momento finito no está definido el error cuadrático medio. | - |

---

### [Hab-03] Convergencia del Mínimo Exponencial (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 12: Convergencia del Mínimo Exponencial
- **Prerequisites:** C-03
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 12)

#### Description & Cognitive Model
Deducción de la distribución exacta $X_{(1)}\sim\text{Exp}(n\theta)$ para $X_i\stackrel{\text{i.i.d.}}{\sim}\text{Exp}(\theta)$ y prueba de $X_{(1)}\xrightarrow{\text{m.s.}} 0$ con varianza $O(1/n^2)$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Evento unión mínimo | skipped_step | high | $\{X_{(1)}>t\}=\bigcup_{i=1}^n\{X_i>t\}$ | Exprese $\{X_{(1)}>t\}$ como intersección $\bigcap_{i=1}^n\{X_i>t\}$: el mínimo supera $t$ solo si todas las observaciones superan $t$. |
| `D-Hab03-02` | Parámetro dividido n | skipped_step | high | $X_{(1)}\sim\text{Exp}(\theta/n)$ | Sume los exponentes al multiplicar $n$ veces $e^{-\theta t}$: $(e^{-\theta t})^n=e^{-(n\theta)t}$, escalando la tasa a $\lambda_n=n\theta$. |
| `D-Hab03-03` | Varianza tasa 1/n | conceptual_swap | high | $\text{Var}(X_{(1)})=\frac{1}{n\theta^2}$ | Eleve al cuadrado el parámetro escalado $\lambda_n=n\theta$ en la varianza exponencial $1/\lambda_n^2$, obteniendo $1/(n^2\theta^2)$ (superconsistencia). |
| `D-Hab03-04` | Confunde FDA con supervivencia | conceptual_swap | high | $F_{X_{(1)}}(t)=e^{-n\theta t}$ | Reste de la unidad la función de supervivencia: $F_{X_{(1)}}(t)=1-\mathbb{P}(X_{(1)}>t)=1-e^{-n\theta t}$ para $t\ge 0$. |
| `D-Hab03-05` | Media como parámetro | conceptual_swap | high | $\mathbb{E}[X_{(1)}]=n\theta$ | Invierta el parámetro de tasa en la distribución exponencial: $\mathbb{E}[X_{(1)}]=1/(n\theta)$, el cual tiende a $0$ cuando $n\to\infty$. |
| `D-Hab03-06` | ECM solo varianza | conceptual_swap | high | $\text{ECM}(X_{(1)})=\frac{1}{n^2\theta^2}$ | Sume varianza y sesgo al cuadrado respecto a $c=0$: $\frac{1}{n^2\theta^2}+\left(\frac{1}{n\theta}\right)^2=\frac{2}{n^2\theta^2}\to 0$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | Independencia mutua de $\{X_1,\dots,X_n\}$ con $X_i\sim\text{Exp}(\theta)$ y $\theta>0$ | Sin independencia la probabilidad de la intersección no factoriza como producto de marginales. | - |

---

### [C-04] Desigualdad de Markov (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 14: Desigualdad de Markov
- **Prerequisites:** C-02
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 14), `EST3_LEC07_26.2_V2.pdf` (page 21)

#### Description & Cognitive Model
Cota probabilística libre de distribución $\mathbb{P}(Y\ge\delta)\le\mathbb{E}[Y]/\delta$ para $Y\ge 0$ casi seguramente y $\delta>0$, demostrada vía esperanza iterada e integral

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Aplica con negativos | conceptual_swap | high | Vale para cualquier $Y\in\mathbb{R}$ sin restricción | Verifique la hipótesis $\mathbb{P}(Y\ge 0)=1$: si $Y$ toma valores negativos, descartar la región $Y<\delta$ no garantiza conservar una cota inferior. |
| `D-C04-02` | Sentido invertido | conceptual_swap | high | $\mathbb{P}(Y\ge\delta)\ge\frac{\mathbb{E}[Y]}{\delta}$ | Recuerde que $\mathbb{E}[Y]\ge\delta\,\mathbb{P}(Y\ge\delta)$ al truncar valores menores que $\delta$, por lo que $\mathbb{E}[Y]/\delta$ es cota superior. |
| `D-C04-03` | Umbral delta cero | conceptual_swap | high | Permite $\delta=0$ o $\delta<0$ en el cociente | Exija $\delta>0$ estricto para dividir sin indeterminación ni invertir el sentido de la desigualdad en el despeje. |
| `D-C04-04` | Cota inferior condicional | conceptual_swap | high | $\mathbb{E}[Y\mid Y\ge\delta]\le\delta$ | Aplique monotonía de la esperanza sobre el evento $\{Y\ge\delta\}$: si todo valor del subuniverso es $\ge\delta$, su promedio es $\ge\delta$. |
| `D-C04-05` | Descarta región negativa | conceptual_swap | high | $\int_0^\delta y f_Y(y)dy<0$ | Note que en $[0,\delta]$ tanto $y\ge 0$ como $f_Y(y)\ge 0$, por lo que la integral sobre $[0,\delta]$ es no negativa y suprimirla acota por abajo. |
| `D-C04-06` | Exige densidad continua | conceptual_swap | high | Markov solo vale si $Y$ tiene densidad $f_Y$ | Aplique la demostración por esperanza iterada sobre la partición $\{Y<\delta\}\cup\{Y\ge\delta\}$, válida para variables discretas, continuas o mixtas. |
| `D-C04-07` | Omite no negatividad | conceptual_swap | high | $P(Y \ge \delta) \le \frac{E[Y]}{\delta}$ vale para cualquier $Y$ | Verifique siempre que $Y \ge 0$ antes de aplicar Markov; valores negativos invalidan la cota. |
| `D-C04-08` | Invierte razón | conceptual_swap | high | $P(Y \ge \delta) \le \frac{\delta}{E[Y]}$ | Coloque la esperanza en el numerador y el umbral $\delta$ en el denominador para que la cota baje al crecer $\delta$. |
| `D-C04-09` | Sentido desigualdad | conceptual_swap | high | $P(Y \ge \delta) \ge \frac{E[Y]}{\delta}$ | Recuerde que Markov da un techo máximo de probabilidad, no un mínimo garantizado. |
| `D-C04-10` | Usa varianza | conceptual_swap | high | $P(Y \ge \delta) \le \frac{\operatorname{Var}(Y)}{\delta}$ | Use el primer momento $E[Y]$ en Markov lineal; la varianza aparece recién en Chebyshev con $\delta^2$. |
| `D-C04-11` | Umbral nulo | conceptual_swap | high | La cota es válida incluso para $\delta = 0$ | Exija $\delta > 0$ estrictamente para evitar división por cero en el denominador. |
| `D-C04-12` | Cota exacta | conceptual_swap | high | $P(Y \ge \delta) = \frac{E[Y]}{\delta}$ | Interprete la expresión como una cota superior gruesa válida para cualquier distribución no negativa. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | No negatividad casi segura $\mathbb{P}(Y\ge 0)=1$ y esperanza finita $\mathbb{E}[Y]<\infty$ | Si $Y$ toma valores negativos o $\mathbb{E}[Y]=\infty$, la cota de Markov pierde validez o es trivial. | - |
| `A-C04-02` | - | La variable aleatoria satisface $Y \ge 0$ casi seguramente y $E[Y] < \infty$ | Si $Y$ toma valores negativos, $E[Y]$ no acota $\delta P(Y \ge \delta)$. | - |

---

### [Hab-04] Desigualdad de Chebyshev (Concept)

- **Bloom Level:** Apply
- **Session:** Unidad 16: Desigualdad de Chebyshev
- **Prerequisites:** C-04
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 16), `Clases_sintetizadas_semana_9.pdf` (page 17), `EST3_LEC07_26.2_V2.pdf` (page 23)

#### Description & Cognitive Model
Deducción mediante Markov sobre $Y=|X-c|^r$ y acotación bilateral de colas $\mathbb{P}(|X-c|\ge\varepsilon)\le\mathbb{E}[|X-c|^r]/\varepsilon^r$ y caso estándar $\mathbb{P}(|X-\mu|\ge\varepsilon)\le\text{Var}(X)/\varepsilon^2$.

#### Fused Distractor Models (18)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Omite potencia en epsilon | skipped_step | high | $\mathbb{P}(|X-\mu|\ge\varepsilon)\le\frac{\text{Var}(X)}{\varepsilon}$ | Transforme ambos lados del evento con la función creciente $u\mapsto u^r$ para obtener $\delta=\varepsilon^r$ en el denominador (con $r=2$, $\varepsilon^2$). |
| `D-Hab04-02` | Usa desviación estándar | skipped_step | high | $\mathbb{P}(|X-\mu|\ge\varepsilon)\le\frac{\sigma}{\varepsilon^2}$ | Use el segundo momento centrado $\mathbb{E}[(X-\mu)^2]=\text{Var}(X)=\sigma^2$ en el numerador, manteniendo consistencia dimensional con $\varepsilon^2$. |
| `D-Hab04-03` | Sin valor absoluto | conceptual_swap | high | $\mathbb{P}(X-\mu\ge\varepsilon)\le\frac{\text{Var}(X)}{\varepsilon^2}$ como igualdad | Identifique que Chebyshev acota ambas colas $|X-\mu|\ge\varepsilon$; una cola unilateral queda acotada por el mismo techo pero de forma más gruesa. |
| `D-Hab04-04` | Fija c distinto sin cambio | conceptual_swap | high | $\mathbb{P}(|X-c|\ge\varepsilon)\le\frac{\text{Var}(X)}{\varepsilon^2}$ para $c\ne\mu$ | Sustituya $\text{Var}(X)$ por $\mathbb{E}[(X-c)^2]=\text{Var}(X)+(\mu-c)^2$ cuando el centro $c$ difiera de la esperanza poblacional $\mu$. |
| `D-Hab04-05` | Potencia negativa r | conceptual_swap | high | Aplica $u\mapsto u^r$ con $r\le 0$ | Exija $r>0$ para que $h'(u)=ru^{r-1}>0$ y la función sea estrictamente creciente, preservando la equivalencia $\{|X-c|\ge\varepsilon\}=\{|X-c|^r\ge\varepsilon^r\}$. |
| `D-Hab04-06` | Varianza infinita | conceptual_swap | high | Chebyshev aplica con momentos infinitos | Verifique previamente que $\mathbb{E}[|X-c|^r]<\infty$ (o $\text{Var}(X)<\infty$); sin momento finito la desigualdad de Markov no es aplicable. |
| `D-Hab04-07` | Exponente lineal | conceptual_swap | high | $\mathbb{P}(|X-\mu|\ge \varepsilon)\le \frac{\text{Var}(X)}{\varepsilon}$ | Eleve el umbral a la potencia $r=2$: al definir $Y=(X-\mu)^2$, el umbral transformado en Markov es $\delta=\varepsilon^2$. |
| `D-Hab04-08` | Invierte razón | conceptual_swap | high | $\mathbb{P}(|X-c|\ge \varepsilon)\le \frac{\varepsilon^r}{\mathbb{E}[|X-c|^r]}$ | Mantenga el momento en el numerador y $\varepsilon^r$ en el denominador: mayor dispersión eleva la cota, mayor umbral la reduce. |
| `D-Hab04-09` | Desviación sin valor absoluto | conceptual_swap | high | $\mathbb{P}(X-\mu\ge \varepsilon)\le \frac{\text{Var}(X)}{\varepsilon^2}$ como igualdad | Recuerde que Chebyshev acota la probabilidad bilateral $|X-\mu|\ge \varepsilon$ usando el momento absoluto de orden $r$. |
| `D-Hab04-10` | Usa desviación estándar | conceptual_swap | high | $\mathbb{P}(|X-\mu|\ge \varepsilon)\le \frac{\sigma}{\varepsilon^2}$ | Use la varianza $\sigma^2=\mathbb{E}[(X-\mu)^2]$ en el numerador cuando $r=2$, para conservar homogeneidad de unidades con $\varepsilon^2$. |
| `D-Hab04-11` | Cota estricta inválida | conceptual_swap | high | La cota falla si $\mathbb{P}(|X-c|>\varepsilon)$ es estricta | Note que $\{|X-c|>\varepsilon\}\subseteq\{|X-c|\ge \varepsilon\}$, por lo que $\mathbb{P}(|X-c|>\varepsilon)$ hereda exactamente la misma cota. |
| `D-Hab04-12` | Exige normalidad | conceptual_swap | high | Chebyshev solo aplica si $X\sim\mathcal{N}(\mu,\sigma^2)$ | Aplique Chebyshev a cualquier variable aleatoria con momento finito de orden $r>0$, sin requerir supuesto paramétrico. |
| `D-Hab04-13` | Exponente lineal | conceptual_swap | high | $P(|X - \mu| \ge \epsilon) \le \frac{\operatorname{Var}(X)}{\epsilon}$ | Eleve el margen $\epsilon$ al cuadrado porque Chebyshev aplica Markov a $(X - \mu)^2 \ge \epsilon^2$. |
| `D-Hab04-14` | Desviación en numerador | conceptual_swap | high | $P(|X - \mu| \ge \epsilon) \le \frac{\sigma}{\epsilon^2}$ | Coloque la varianza $\sigma^2$ en el numerador para mantener coherencia dimensional con $\epsilon^2$. |
| `D-Hab04-15` | Cota de una cola | conceptual_swap | high | $P(X - \mu \ge k\sigma) \le \frac{1}{k^2}$ es exacta para una cola | Recuerde que $1/k^2$ acota ambas colas simultáneamente mediante el valor absoluto $|X-\mu|$. |
| `D-Hab04-16` | Requiere normalidad | conceptual_swap | high | Chebyshev solo es válida si $X \sim N(\mu, \sigma^2)$ | Aplique Chebyshev a cualquier distribución con varianza finita; la normalidad solo da cotas más estrechas. |
| `D-Hab04-17` | Invierte k | conceptual_swap | high | $P(|X - \mu| \ge k\sigma) \le k^2$ | Divida $1$ entre $k^2$ para que la probabilidad máxima disminuya al alejarse más desviaciones estándar. |
| `D-Hab04-18` | Usa 1-1/$k^2$ | conceptual_swap | high | $P(|X - \mu| \ge k\sigma) \le 1 - \frac{1}{k^2}$ | Distinga que $1/k^2$ acota estar fuera de $\mu \pm k\sigma$, mientras $1 - 1/k^2$ acota por debajo estar dentro. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Momento absoluto finito $\mathbb{E}[|X-c|^r]<\infty$ para algún $r>0$ y umbral $\varepsilon>0$ | Sin momento de orden $r$ finito no se puede acotar la cola mediante Markov. | - |
| `A-Hab04-02` | - | Existencia de momento $\mathbb{E}[|X-c|^r]<\infty$ con $r>0$ y $\varepsilon>0$ | Sin momento finito de orden $r$, la cota de Chebyshev diverge y no acota la cola. | - |
| `A-Hab04-03` | - | La variable $X$ posee media $\mu$ y varianza finita $\sigma^2 = \operatorname{Var}(X) < \infty$ | Si la varianza es infinita, la cota $1/k^2$ carece de sustento. | - |

---

### [C-06] Desigualdad de Jensen (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 18: Desigualdad de Jensen
- **Prerequisites:** Hab-04
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 18), `EST3_LEC07_26.2_V2.pdf` (page 25)

#### Description & Cognitive Model
No conmutatividad de la esperanza bajo funciones no lineales: $\mathbb{E}[g(X)]\ge g(\mathbb{E}[X])$ en convexas y $\le$ en cóncavas

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Conmuta esperanza | conceptual_swap | high | $\mathbb{E}[g(X)]=g(\mathbb{E}[X])$ para toda $g$ continua | Recuerde que $\mathbb{E}[\cdot]$ solo conmuta con funciones afines $ax+b$; para funciones no lineales rige la desigualdad de Jensen. |
| `D-C06-02` | Invierte sentido convexo | conceptual_swap | high | Si $g$ es convexa, $\mathbb{E}[g(X)]\le g(\mathbb{E}[X])$ | Verifique la recta tangente soporte $g(x)\ge g(\mu)+g'(\mu)(x-\mu)$: al tomar esperanza se obtiene $\mathbb{E}[g(X)]\ge g(\mathbb{E}[X])$. |
| `D-C06-03` | Confunde sesgo de $S_n$ | conceptual_swap | high | $S_n=\sqrt{S_n^2}$ es insesgado o sesgado hacia arriba | Como $h(u)=\sqrt{u}$ es estrictamente cóncava ($h''(u)<0$), Jensen implica $\mathbb{E}[\sqrt{S_n^2}]<\sqrt{\mathbb{E}[S_n^2]}=\sigma$. |
| `D-C06-04` | Confunde con plim | conceptual_swap | high | $\mathbb{E}[g(\hat{\theta}_n)]\to g(\theta)$ sin condiciones adicionales | Distinga $\mathbb{E}[\cdot]$ de $\text{plim}$: solo $\text{plim}$ atraviesa funciones continuas no lineales; la esperanza exige linealidad. |
| `D-C06-05` | Exige diferenciabilidad | conceptual_swap | high | Jensen falla si $g$ tiene un vértice en $\mu=\mathbb{E}[X]$ | Use un subgradiente $g'(\mu)$ en la recta de soporte cuando $g$ no sea diferenciable en $\mu$; la convexidad basta. |
| `D-C06-06` | Omite dominio abierto | conceptual_swap | high | Aplica $g(x)=1/x$ sin restringir $X>0$ | Verifique que el soporte de $X$ esté contenido en un intervalo abierto $I$ donde $g$ mantenga su convexidad o concavidad. |
| `D-C06-07` | Linealidad universal | conceptual_swap | high | $E[g(X)] = g(E[X])$ para toda función $g$ | Aplique linealidad de la esperanza solo a funciones afines $ax+b$; las no lineales introducen curvatura. |
| `D-C06-08` | Invierte convexidad | conceptual_swap | high | $E[g(X)] \le g(E[X])$ cuando $g$ es convexa | Verifique que en una función convexa (forma $\cup$) los valores extremos elevan el promedio por encima de $g(E[X])$. |
| `D-C06-09` | Insesgadez preservada | conceptual_swap | high | Si $s^2$ es insesgado para $\sigma^2$, entonces $s = \sqrt{s^2}$ es insesgado para $\sigma$ | Aplique Jensen con la función cóncava $\sqrt{\cdot}$ para mostrar que $E[s] \le \sqrt{E[s^2]} = \sigma$. |
| `D-C06-10` | Invierte concavidad | conceptual_swap | high | $E[\sqrt{s^2}] \ge \sqrt{E[s^2]}$ | Recuerde que la raíz cuadrada es cóncava (forma $\cap$), por lo que $E[s]$ subestima o iguala a $\sigma$. |
| `D-C06-11` | Confunde con plim | conceptual_swap | high | Ni la esperanza ni el $\operatorname{plim}$ pasan por funciones no lineales | Distinga que la esperanza no conmuta con funciones no lineales, pero el límite en probabilidad sí por continuidad. |
| `D-C06-12` | Igualdad sin recta | conceptual_swap | high | La igualdad $E[g(X)] = g(E[X])$ ocurre aunque $X$ sea aleatoria y $g$ cuadrática | Recuerde que para funciones estrictamente convexas la igualdad exige que $X$ sea constante ($\operatorname{Var}(X)=0$). |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Soporte de $X$ en intervalo abierto $I\subseteq\mathbb{R}$ con $\mathbb{E}[|X|]<\infty$ y $\mathbb{E}[|g(X)|]<\infty$ | Sin integrabilidad y convexidad en $I$, la recta tangente o la esperanza pueden no existir. | - |
| `A-C06-02` | - | La función $g$ es convexa (o $h$ cóncava) en el soporte de $X$ y existen $E[X]$ y $E[g(X)]$ | Sin convexidad definida o esperanza finita la desigualdad falla. | - |

---

### [C-07] Desigualdad de Cauchy-Schwarz (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 19: Desigualdad de Cauchy-Schwarz
- **Prerequisites:** Hab-04
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 19)

#### Description & Cognitive Model
Acotación del segundo momento cruzado $(\mathbb{E}[XY])^2\le \mathbb{E}[X^2]\mathbb{E}[Y^2]$ por discriminante no positivo y cota $|\rho_{XY}|\le 1$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Omite raíz cuadrada | conceptual_swap | high | $|\mathbb{E}[XY]|\le \mathbb{E}[X^2]\mathbb{E}[Y^2]$ | Tome raíz cuadrada en ambos miembros de $(\mathbb{E}[XY])^2\le \mathbb{E}[X^2]\mathbb{E}[Y^2]$ para obtener $\sqrt{\mathbb{E}[X^2]}\sqrt{\mathbb{E}[Y^2]}$. |
| `D-C07-02` | Discriminante positivo | conceptual_swap | high | $P(t)=\mathbb{E}[(tX+Y)^2]\ge 0 \Rightarrow \Delta = b^2-4ac \ge 0$ | Observe que una parábola $at^2+bt+c\ge 0$ con $a>0$ no tiene dos raíces reales distintas, por lo que $\Delta=b^2-4ac\le 0$. |
| `D-C07-03` | Confunde producto con covarianza | conceptual_swap | high | $(\mathbb{E}[XY])^2\le \text{Var}(X)\text{Var}(Y)$ sin centrar | Aplique la cota a las variables centradas $\tilde{X}=X-\mathbb{E}[X]$ e $\tilde{Y}=Y-\mathbb{E}[Y]$ para acotar $|\text{Cov}(X,Y)|$. |
| `D-C07-04` | Igualdad por independencia | conceptual_swap | high | $|\mathbb{E}[XY]|=\sqrt{\mathbb{E}[X^2]\mathbb{E}[Y^2]}$ si $X,Y$ son independientes | Recuerde que la igualdad ocurre solo bajo dependencia lineal perfecta $Y=-t^*X$ casi seguramente, no por independencia. |
| `D-C07-05` | Omite valor absoluto | conceptual_swap | high | $\mathbb{E}[XY]\ge -\sqrt{\mathbb{E}[X^2]\mathbb{E}[Y^2]}$ ignorado | Use $|\mathbb{E}[XY]|$ al tomar $\sqrt{(\mathbb{E}[XY])^2}$ para preservar tanto la cota superior como la inferior ($-1\le\rho_{XY}\le 1$). |
| `D-C07-06` | Primeros momentos en cota | conceptual_swap | high | $(\mathbb{E}[XY])^2\le (\mathbb{E}[X])^2(\mathbb{E}[Y])^2$ | Use los segundos momentos $\mathbb{E}[X^2]$ y $\mathbb{E}[Y^2]$; por Jensen $(\mathbb{E}[X])^2\le \mathbb{E}[X^2]$ y no acota el producto. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Segundos momentos finitos $\mathbb{E}[X^2]<\infty$ y $\mathbb{E}[Y^2]<\infty$ en el mismo espacio | Si los segundos momentos divergen, el polinomio cuadrático $P(t)$ no está bien definido. | - |

---

### [C-08] Jerarquía de Convergencias Estocásticas (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 21: Jerarquía de Convergencias Estocásticas
- **Prerequisites:** Hab-04, C-06
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 21), `EST3_LEC07_26.2_V2.pdf` (page 37)

#### Description & Cognitive Model
Implicaciones entre modos de convergencia: $X_n\xrightarrow{r}X \Rightarrow X_n\xrightarrow{s}X$ ($0<s<r$, vía Jensen), $m.s. \Rightarrow p \Rightarrow d$, $a.s. \Rightarrow p$, caso de límite constante $X_n \xrightarrow{d} c \Rightarrow X_n \xrightarrow{p} c$, y no equivalencia $d \not\Rightarrow p$.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Invierte orden de normas | conceptual_swap | high | Si $0<s<r$, entonces $X_n\xrightarrow{s}X \Rightarrow X_n\xrightarrow{r}X$ | Recuerde que $g(z)=z^{r/s}$ es convexa solo cuando $r/s>1$, por lo que la norma mayor $L^r$ domina a la menor $L^s$. |
| `D-C08-02` | Invierte implicación a p | conceptual_swap | high | $X_n\xrightarrow{p}X \Rightarrow X_n\xrightarrow{m.s.}X$ | Note que Chebyshev va de $L^r$ hacia $\xrightarrow{p}$ en un solo sentido; la recíproca falla cuando hay colas atípicas explosivas. |
| `D-C08-03` | Minkowski sin r>=1 | conceptual_swap | high | Usa norma $L^r$ y desigualdad triangular para $0<r<1$ | Verifique que $r\ge 1$ antes de aplicar la desigualdad de Minkowski, pues para $0<r<1$ no se cumple la desigualdad triangular. |
| `D-C08-04` | Omite momento límite | conceptual_swap | high | Concluye $\mathbb{E}[|X_n|^r]\to \mathbb{E}[|X|^r]$ sin verificar $\mathbb{E}[|X|^r]<\infty$ | Exija $\mathbb{E}[|X|^r]<\infty$ para que $\|X\|_r$ pertenezca al espacio normado $L^r$ y sea válida la forma inversa de Minkowski. |
| `D-C08-05` | Confunde potencia s/r | conceptual_swap | high | Aplica Jensen a $g(z)=z^{s/r}$ con $0<s<r$ como convexa | Defina $Z_n=|X_n-X|^s$ y $g(z)=z^{r/s}$ con $r/s>1$ para garantizar $g''(z)\ge 0$ y aplicar correctamente Jensen. |
| `D-C08-06` | Convergencia de signos | conceptual_swap | high | $X_n\xrightarrow{r}X \Rightarrow \mathbb{E}[X_n^r]\to \mathbb{E}[X^r]$ para todo $r\ge 1$ sin valor absoluto | Aplique Minkowski sobre las normas $\|X_n\|_r=(\mathbb{E}[|X_n|^r])^{1/r}$ con valor absoluto para garantizar existencia y no negatividad. |
| `D-C08-07` | Invierte p y d | conceptual_swap | high | $X_n \xrightarrow{d} X \Rightarrow X_n \xrightarrow{p} X$ para cualquier límite $X$ | Recuerde que la convergencia en distribución es la más débil y no implica convergencia en probabilidad salvo cuando el límite es constante. |
| `D-C08-08` | Asume d más fuerte | conceptual_swap | high | La convergencia en distribución es más fuerte que la convergencia en probabilidad | Ubique la convergencia en distribución como la condición más débil de la jerarquía ($m.s. \Rightarrow p \Rightarrow d$). |
| `D-C08-09` | Olvida excepción constante | conceptual_swap | high | $X_n \xrightarrow{d} c$ nunca implica $X_n \xrightarrow{p} c$ | Aplique el caso especial: si el límite es una constante $c$, toda la masa se concentra en un punto y $d \Rightarrow p$. |
| `D-C08-10` | Implicación a.s. y m.s. | conceptual_swap | high | $X_n \xrightarrow{a.s.} X \Rightarrow X_n \xrightarrow{m.s.} X$ siempre | Recuerde que $a.s.$ y $m.s.$ no se implican mutuamente en general; ambas implican convergencia en probabilidad. |
| `D-C08-11` | Contraejemplo -Z | conceptual_swap | high | Si $Z \sim N(0,1)$ y $X_n = -Z$, entonces $P(|X_n - Z| > 1) \to 0$ | Evalúe la diferencia $|X_n - Z| = |-Z - Z| = 2|Z|$, cuya probabilidad de superar $1$ es $0.617$ para todo $n$. |
| `D-C08-12` | Descarta d desde p | conceptual_swap | high | $X_n \xrightarrow{p} X$ no garantiza $X_n \xrightarrow{d} X$ | Asegure la cadena $m.s. \Rightarrow p \Rightarrow d$: todo estimador consistente converge también en distribución al mismo límite. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Exponentes reales $0<s<r$ para monotonía $L^r\Rightarrow L^s$, y $r\ge 1$ con $\mathbb{E}[|X|^r]<\infty$ para Minkowski | Fuera de estos rangos se pierde la convexidad de $z^{r/s}$ o la desigualdad triangular. | - |
| `A-C08-02` | - | La implicación inversa $X_n \xrightarrow{d} c \Rightarrow X_n \xrightarrow{p} c$ requiere que el límite $c$ sea una constante determinista | Si el límite es una variable aleatoria no degenerada, $d$ no implica $p$. | - |

---

### [Hab-05] Análisis de Convergencia en Probabilidad vs. Momentos (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 23: Análisis de Convergencia en Probabilidad vs. Momentos
- **Prerequisites:** C-08
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 23)

#### Description & Cognitive Model
Evaluación de sucesiones discretas con valores atípicos explosivos (ej. $X_n=n^2$ con prob. $1/n$) para probar $X_n\xrightarrow{p}0$ sin convergencia en $L^1$ ni $L^2$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Confunde soporte con probabilidad | skipped_step | high | Como $X_n=n^2\to\infty$, concluye que $X_n$ no converge en probabilidad | Evalúe la probabilidad fuera de la banda $\mathbb{P}(|X_n-0|>\varepsilon)=1/n\to 0$; el operador $\text{plim}$ ignora la magnitud del outlier. |
| `D-Hab05-02` | Intercambia plim y esperanza | skipped_step | high | Como $\text{plim } X_n=0$, deduce $\lim_{n\to\infty}\mathbb{E}[X_n]=0$ | Calcule explícitamente $\mathbb{E}[X_n]=n^2(1/n)=n\to +\infty$ para comprobar que el valor extremo domina la esperanza. |
| `D-Hab05-03` | Omite cuadrado en L2 | conceptual_swap | high | Calcula $\mathbb{E}[X_n^2]=n^2(1/n)=n$ en lugar de $(n^2)^2(1/n)=n^3$ | Eleve al cuadrado cada valor del soporte al calcular el segundo momento: $\mathbb{E}[X_n^2]=(n^2)^2(1/n)=n^3\to +\infty$. |
| `D-Hab05-04` | Confunde L1 con L2 | conceptual_swap | high | En variante $X_n\in\{0,n\}$ con prob. $1/n$, afirma $\mathbb{E}[X_n]\to 0$ | Sume los productos valor por probabilidad: $\mathbb{E}[X_n]=0(1-1/n)+n(1/n)=1\neq 0$, mostrando que tampoco converge en $L^1$. |
| `D-Hab05-05` | Varianza sin restar media | conceptual_swap | high | Toma $\text{Var}(X_n)=\mathbb{E}[X_n^2]=n^3$ sin restar $(\mathbb{E}[X_n])^2$ | Aplique $\text{Var}(X_n)=\mathbb{E}[X_n^2]-(\mathbb{E}[X_n])^2=n^3-n^2=n^2(n-1)$ antes de tomar el límite cuando $n\to\infty$. |
| `D-Hab05-06` | Asume banda fija sin n grande | conceptual_swap | high | Elige $\varepsilon=5$ y evalúa $n=1$ para concluir $|X_1-0|=1\le \varepsilon$ | Considere $n$ suficientemente grande tal que $n^2>\varepsilon$ para cualquier $\varepsilon>0$ fijo, de modo que $\{|X_n|>\varepsilon\}=\{X_n=n^2\}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Fijar $\varepsilon>0$ arbitrario y evaluar $\lim_{n\to\infty}$ sobre $n$ tal que $n^2>\varepsilon$ | Para $n$ pequeños el evento de cola es vacío y no refleja el comportamiento asintótico. | - |

---

### [Hab-06] Evaluación de Insesgadez y Consistencia de Estimadores (Skill)

- **Bloom Level:** Evaluate
- **Session:** Unidad 26: Evaluación de Insesgadez y Consistencia de Estimadores
- **Prerequisites:** Hab-04, C-08
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 26), `EST3_LEC07_26.2_V2.pdf` (page 30), `EST3_LEC07_26.2_V2.pdf` (page 31)

#### Description & Cognitive Model
Distinción conceptual y cálculo asintótico mediante sesgo, varianza exacta y $\text{ECM} = \text{Var} + \text{Sesgo}^2$ para distinguir estimadores insesgados inconsistentes de sesgados consistentes.

#### Fused Distractor Models (18)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Insesgadez implica consistencia | skipped_step | high | Como $\mathbb{E}[M_B]=\mu_Y$ para todo $n$, entonces $M_B\xrightarrow{p}\mu_Y$ | Verifique además $\lim_{n\to\infty}\text{Var}(M_B)=\sigma_Y^2\frac{1-a}{1+a}>0$: al no colapsar la varianza, la probabilidad en colas no tiende a cero. |
| `D-Hab06-02` | Sesgo finito implica inconsistencia | skipped_step | high | Como $\mathbb{E}[M_C]=\mu_Y+1/n\neq\mu_Y$, $M_C$ es inconsistente | Calcule $\text{ECM}(M_C)=\frac{\sigma_Y^2}{n}+\frac{1}{n^2}\to 0$ y aplique Chebyshev para probar que $M_C$ es asintóticamente insesgado y consistente. |
| `D-Hab06-03` | Error en suma geométrica | conceptual_swap | high | Usa $\sum_{i=1}^n a^{2(i-1)}=\frac{1-a^n}{1-a^2}$ en la varianza de $M_B$ | Eleve la razón $r=a^2$ a la potencia $n$ en la serie geométrica: $\sum_{i=1}^n (a^2)^{i-1}=\frac{1-a^{2n}}{1-a^2}$, y factorice $(1-a^n)(1+a^n)$. |
| `D-Hab06-04` | No eleva pesos al cuadrado | conceptual_swap | high | $\text{Var}(M_B)=\left(\frac{1-a}{1-a^n}\right)\sum_{i=1}^n a^{i-1}\text{Var}(Y_i)$ | Recuerde que $\text{Var}(\sum c_i Y_i)=\sum c_i^2\text{Var}(Y_i)$ bajo independencia, por lo que tanto el factor $\frac{1-a}{1-a^n}$ como $a^{i-1}$ van al cuadrado. |
| `D-Hab06-05` | Altera varianza con constante | conceptual_swap | high | $\text{Var}(\bar{Y}_n+1/n)=\frac{\sigma_Y^2}{n}+\frac{1}{n^2}$ | Note que sumar una constante determinística $1/n$ no altera la varianza ($\text{Var}(M_C)=\sigma_Y^2/n$); el término $1/n^2$ entra al $\text{ECM}$ vía el sesgo al cuadrado. |
| `D-Hab06-06` | Confunde uso de n datos con consistencia | conceptual_swap | high | Como $M_B$ usa las $n$ observaciones, su varianza tiende a $0$ | Observe que los pesos geométricos $a^{i-1}$ ($0<a<1$) concentran el peso en las primeras observaciones, impidiendo que la Ley de Grandes Números actúe. |
| `D-Hab06-07` | No eleva sesgo al cuadrado | skipped_step | high | Calcula $\operatorname{ECM} = \frac{100}{n} + \frac{5}{n} = \frac{105}{n}$ | Eleve al cuadrado el término de sesgo $5/n$ antes de sumarlo a la varianza $100/n$. |
| `D-Hab06-08` | Descarta por sesgo | skipped_step | high | Concluye que $\hat{\mu}_n = \bar{Y}_n + 5/n$ es inconsistente por ser sesgado | Evalúe el límite del sesgo cuando $n \to \infty$: como $5/n \to 0$ y $100/n \to 0$, el estimador es consistente. |
| `D-Hab06-09` | Varianza cambia con constante | conceptual_swap | high | Calcula $\operatorname{Var}(\bar{Y}_n + 5/n) = \frac{100}{n} + \frac{25}{n^2}$ | Recuerde que sumar una constante determinista $5/n$ desplaza la media pero deja intacta la varianza $\sigma^2/n$. |
| `D-Hab06-10` | Ritmo invertido | conceptual_swap | high | Afirma que el $\operatorname{Sesgo}^2$ cae más lento que la varianza | Compare las potencias para $n$ grande: $1/n^2$ decrece más rápido hacia cero que $1/n$. |
| `D-Hab06-11` | Olvida n en varianza de media | conceptual_swap | high | Usa $\operatorname{Var}(\bar{Y}_n) = \sigma^2 = 100$ sin dividir entre $n$ | Divida la varianza poblacional $\sigma^2$ entre $n$ para obtener la varianza de la media muestral $\bar{Y}_n$. |
| `D-Hab06-12` | Confunde ECM con sesgo | conceptual_swap | high | Identifica el valor del $\operatorname{ECM}$ con el sesgo del estimador | Separe ambos componentes: el sesgo mide desviación sistemática en media y el ECM suma varianza más sesgo al cuadrado. |
| `D-Hab06-13` | Insesgadez implica consistencia | conceptual_swap | high | Todo estimador insesgado es automáticamente consistente | Observe el contraejemplo $Y_1$: su esperanza es $\mu$, pero su varianza $\sigma^2$ nunca disminuye al crecer $n$. |
| `D-Hab06-14` | Consistencia implica insesgadez | conceptual_swap | high | Todo estimador consistente debe ser insesgado | Recuerde el contraejemplo $\bar{Y}_n + 5/n$, que es sesgado para todo $n$ finito pero converge en probabilidad a $\mu$. |
| `D-Hab06-15` | Prioriza insesgadez asintótica | conceptual_swap | high | En muestras grandes, la econometría prefiere un estimador insesgado inconsistente | Priorice la consistencia en muestras grandes, pues muchos estimadores econométricos (VI, MV) tienen sesgo finito que desaparece. |
| `D-Hab06-16` | Varianza de Y1 cae | conceptual_swap | high | La varianza de $Y_1$ tiende a cero al aumentar $n$ | Note que $Y_1$ ignora las $n-1$ observaciones nuevas, por lo que su varianza permanece constante en $\sigma^2$. |
| `D-Hab06-17` | Misma propiedad | conceptual_swap | high | Insesgadez y consistencia significan lo mismo con distinta notación | Separe claramente muestra finita ($n$ fijo, esperanza igual a $\theta$) de propiedad asintótica ($n \to \infty$, concentración en $\theta$). |
| `D-Hab06-18` | Sesgo 5/n no desaparece | conceptual_swap | high | Un estimador con sesgo $5/n$ mantiene sesgo asintótico | Evalúe $\lim_{n\to\infty} 5/n = 0$: el sesgo desaparece asintóticamente permitiendo consistencia. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Muestra aleatoria i.i.d. $Y_i\sim\mathcal{N}(\mu_Y,\sigma_Y^2)$ con $0<\sigma_Y^2<\infty$ y $a\in(0,1)$ | La independencia permite sumar varianzas y $a\in(0,1)$ asegura que $a^n\to 0$. | - |
| `A-Hab06-02` | - | Las observaciones tienen varianza finita $\sigma^2 < \infty$ e independencia para $\operatorname{Var}(\bar{Y}_n) = \sigma^2/n$ | Sin independencia o varianza finita la fórmula $\sigma^2/n$ falla. | - |
| `A-Hab06-03` | - | El estimador $\hat{\theta}_n$ está definido para cada tamaño muestral $n$ y tiene esperanza finita | Sin esperanza finita no puede evaluarse la insesgadez. | - |

---

### [H-01] Axiomas de Probabilidad de Kolmogorov (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 13: Axiomas de Probabilidad de Kolmogorov
- **Prerequisites:** C-01
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 13)

#### Description & Cognitive Model
Terna $(\Omega,\mathcal{F},P)$ donde $0\le P(A)\le 1$, $P(\Omega)=1$ y $P(A\cup B)=P(A)+P(B)$ si $A\cap B=\emptyset$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Suma sin disjunción | conceptual_swap | high | $P(A\cup B)=P(A)+P(B)$ siempre | Reste la intersección $P(A\cap B)$ cuando los eventos $A$ y $B$ compartan resultados. |
| `D-H01-02` | Probabilidad mayor a uno | conceptual_swap | high | $P(A)>1$ es posible | Verifique que toda probabilidad pertenezca al intervalo $[0,1]$ por el primer axioma. |
| `D-H01-03` | Probabilidad negativa | conceptual_swap | high | $P(A)<0$ en eventos raros | Asegure no negatividad $P(A)\ge 0$ para todo evento medible $A\subseteq\Omega$ del espacio. |
| `D-H01-04` | Omega menor que uno | conceptual_swap | high | $P(\Omega)<1$ | Recuerde que el evento seguro $\Omega$ agota todos los resultados posibles, luego $P(\Omega)=1$. |
| `D-H01-05` | Confunde unión e intersección | conceptual_swap | high | $P(A\cup B)=P(A)P(B)$ | Distinga unión de eventos disjuntos (suma) de intersección independiente (producto). |
| `D-H01-06` | Confunde muestra con Omega | conceptual_swap | high | $\Omega$ es la muestra observada | Separe el espacio muestral $\Omega$ (todo resultado posible) de la muestra observada. |

---

### [C-09] Variable Aleatoria y Distribución Inducida (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 15: Variable Aleatoria y Distribución Inducida
- **Prerequisites:** H-01
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 15)

#### Description & Cognitive Model
Regla $X:\Omega\to\mathbb{R}$ que asigna $\omega\mapsto X(\omega)=x$ y traslada probabilidades vía $P(X=x)=P(\{\omega:X(\omega)=x\})$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Regla aleatoria | conceptual_swap | high | La función $X$ cambia al azar | Identifique que lo aleatorio es el resultado $\omega\in\Omega$ y no la regla determinista $X$. |
| `D-C09-02` | Confunde X con x | conceptual_swap | high | $X$ y $x$ son el mismo objeto | Use mayúscula $X$ para la variable aleatoria y minúscula $x$ para su realización numérica. |
| `D-C09-03` | Ignora multiplicidad | conceptual_swap | high | $P(X=x)=1/|\Omega|$ siempre | Agrupe todos los resultados $\omega$ con $X(\omega)=x$ antes de sumar sus probabilidades. |
| `D-C09-04` | Codominio no real | conceptual_swap | high | $X(\omega)$ puede ser cualitativo | Convierta cada resultado $\omega$ del experimento en un número real $x\in\mathbb{R}$. |
| `D-C09-05` | Suma fuera de Omega | conceptual_swap | high | $\sum_x P(X=x)\neq 1$ | Verifique que la distribución inducida conserve probabilidad total igual a $1$ sobre el soporte. |
| `D-C09-06` | Confunde soporte y Omega | conceptual_swap | high | El soporte de $X$ es $\Omega$ | Distinga el dominio $\Omega$ (resultados) de la imagen numérica $X(\Omega)\subseteq\mathbb{R}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Medibilidad de $X$ respecto a $\mathcal{F}$ | Sin ella no existe $P(X=x)$ bien definida. | - |

---

### [C-10] Muestra Aleatoria i.i.d. y Estimador (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 3: Muestra Aleatoria i.i.d. y Estimador
- **Prerequisites:** C-09
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 3)

#### Description & Cognitive Model
Muestra $Y_1,\dots,Y_n\text{ i.i.d.}\sim F_Y$ y estimador $\hat{\theta}_n=T(Y_1,\dots,Y_n)$ como variable aleatoria cuya realización es la estimación.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Confunde estimador y estimación | conceptual_swap | high | El estimador es un número fijo | Distinga el estimador $\hat{\theta}_n$ (regla aleatoria) de la estimación (número observado en una muestra). |
| `D-C10-02` | Ignora independencia | conceptual_swap | high | i.i.d. solo exige misma $F_Y$ | Verifique ambas condiciones de i.i.d.: independencia mutua e idéntica distribución $F_Y$. |
| `D-C10-03` | Confunde parámetro y estimador | conceptual_swap | high | $\theta$ cambia con la muestra | Recuerde que $\theta$ es una constante poblacional desconocida y $\hat{\theta}_n$ es la variable aleatoria. |
| `D-C10-04` | Omite dependencia en n | conceptual_swap | high | $\hat{\theta}_n$ no depende de $n$ | Observe el subíndice $n$: al cambiar el tamaño muestral cambia la distribución del estimador. |
| `D-C10-05` | Estimador usa parámetro | conceptual_swap | high | $\hat{\theta}_n$ puede depender de $\theta$ | Construya el estimador exclusivamente con los datos observables $Y_1,\dots,Y_n$ sin parámetros desconocidos. |
| `D-C10-06` | Muestreo sin azar | conceptual_swap | high | Cualquier grupo de $n$ datos es i.i.d. | Garantice selección aleatoria para que ninguna observación informe o sesgue a las demás. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | Muestreo aleatorio simple con reemplazo o población infinita | Sin él falla el supuesto de independencia e identidad. | - |

---

### [C-11] Esperanza y Varianza de Variable Aleatoria (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 17: Esperanza y Varianza de Variable Aleatoria
- **Prerequisites:** C-09
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 17), `EST3_LEC07_26.2_V2.pdf` (page 18)

#### Description & Cognitive Model
Promedio ponderado $E[X]=\sum_x x P(X=x)$ (o integral continua) y dispersión $\text{Var}(X)=E[(X-E[X])^2]=E[X^2]-(E[X])^2$.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C11-01` | Promedio simple | conceptual_swap | high | $E[X]=\frac{1}{k}\sum x_i$ sin pesos | Pondere cada valor posible $x$ por su probabilidad $P(X=x)$ y no por equiprobabilidad. |
| `D-C11-02` | Invierte orden en varianza | conceptual_swap | high | $\text{Var}(X)=(E[X])^2-E[X^2]$ | Reste el cuadrado de la esperanza al segundo momento $E[X^2]$ para mantener $\text{Var}(X)\ge 0$. |
| `D-C11-03` | Olvida elevar esperanza | conceptual_swap | high | $\text{Var}(X)=E[X^2]-E[X]$ | Eleve al cuadrado la esperanza $(E[X])^2$ al aplicar la identidad de expansión cuadrática. |
| `D-C11-04` | Linealiza el cuadrado | conceptual_swap | high | $E[X^2]=(E[X])^2$ siempre | Recuerde que la esperanza es lineal, pero no conmuta con funciones no lineales como $x^2$. |
| `D-C11-05` | Desvío sin cuadrado | conceptual_swap | high | $\text{Var}(X)=E[X-E[X]]$ | Eleve al cuadrado los desvíos $(X-E[X])^2$ antes de tomar esperanza para medir dispersión. |
| `D-C11-06` | Confunde desvío típico | conceptual_swap | high | $\sigma=\text{Var}(X)$ | Tome raíz cuadrada $\sigma=\sqrt{\text{Var}(X)}$ cuando requiera expresar dispersión en unidades originales. |
| `D-C11-07` | Omite cuadrado en E[$X^2$] | skipped_step | high | $E[X^2]=\sum_x x P(X=x)$ | Eleve cada valor $x$ al cuadrado antes de multiplicarlo por $P(X=x)$ para obtener $E[X^2]$. |
| `D-C11-08` | Olvida restar (E[X])^2 | skipped_step | high | $\text{Var}(X)=E[X^2]$ | Reste $(E[X])^2$ al segundo momento $E[X^2]$ luego de calcular ambos términos por separado. |
| `D-C11-09` | Eleva probabilidad al cuadrado | conceptual_swap | high | $E[X^2]=\sum_x x^2 P(X=x)^2$ | Mantenga las probabilidades $P(X=x)$ lineales al calcular momentos $E[X^k]=\sum x^k P(X=x)$. |
| `D-C11-10` | No pondera desvíos | conceptual_swap | high | $\text{Var}(X)=\sum_x (x-E[X])^2$ | Multiplique cada desvío cuadrático $(x-E[X])^2$ por su probabilidad $P(X=x)$ antes de sumar. |
| `D-C11-11` | Confunde sigma con varianza | conceptual_swap | high | $\sigma=\text{Var}(X)=0.5$ | Extraiga la raíz cuadrada de la varianza para reportar la desviación estándar $\sigma$. |
| `D-C11-12` | Error de signo en desvío | conceptual_swap | high | $(0-1)^2=-1$ | Verifique que todo desvío cuadrático $(x-E[X])^2$ sea no negativo antes de ponderar. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C11-01` | - | Existencia de momentos $E[|X|]<\infty$ y $E[X^2]<\infty$ | Sin momentos finitos divergen esperanza o varianza. | - |
| `A-C11-02` | - | Distribución discreta válida con $\sum_x P(X=x)=1$ | Si no suma 1, los momentos quedan mal escalados. | - |

---

### [Hab-11] Acotación de Probabilidades sin Distribución (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 24: Acotación de Probabilidades sin Distribución
- **Prerequisites:** C-04, Hab-04
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 24)

#### Description & Cognitive Model
Cálculo numérico de cotas de probabilidad mediante Markov $P(Y \ge \delta) \le \frac{E[Y]}{\delta}$ y Chebyshev $P(|X-\mu|\ge k\sigma) \le \frac{1}{k^2}$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab11-01` | Confunde k y epsilon | skipped_step | high | Usa $\epsilon = 10$ directamente en $1/k^2$ obteniendo $1/100$ | Divida primero la distancia $\epsilon$ entre $\sigma$ para hallar $k = \epsilon/\sigma$ antes de usar $1/k^2$. |
| `D-Hab11-02` | Usa varianza en k | skipped_step | high | Calcula $k = \epsilon / \sigma^2$ | Use la desviación estándar $\sigma$, no la varianza $\sigma^2$, al expresar $\epsilon$ como $k\sigma$. |
| `D-Hab11-03` | Suma k=1 | conceptual_swap | high | Reporta cota superior mayor a 1 como probabilidad válida | Recuerde que si la cota algebraica supera $1$, la cota efectiva es trivialmente $1$ por axioma de probabilidad. |
| `D-Hab11-04` | Confunde Markov y Cheb. | conceptual_swap | high | Aplica $\operatorname{Var}(Y)/\delta$ sin conocer la varianza | Seleccione Markov si solo conoce $E[Y]$ y $Y\ge 0$; reserve Chebyshev para desviaciones bilaterales con $\sigma^2$. |
| `D-Hab11-05` | Aplica regla normal | conceptual_swap | high | Usa $4.6\%$ en lugar de $25\%$ para $k=2$ sin supuesto normal | Use la cota conservadora $1/k^2 = 0.25$ cuando la distribución sea desconocida; la normal requiere supuesto paramétrico. |
| `D-Hab11-06` | Cota interior | conceptual_swap | high | Calcula $P(|X - \mu| < k\sigma) \le 1/k^2$ | Asigne $1/k^2$ a las colas extremas $|X-\mu|\ge k\sigma$; el intervalo central tiene probabilidad al menos $1 - 1/k^2$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab11-01` | - | Se verifica $Y \ge 0$ para Markov y existencia de $\mu, \sigma^2 < \infty$ para Chebyshev | Sin estos supuestos la cota calculada es inválida. | - |

---

### [Hab-12] Cuantificación de Sesgo en Transformaciones No Lineales (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 26: Cuantificación de Sesgo en Transformaciones No Lineales
- **Prerequisites:** C-06
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 26)

#### Description & Cognitive Model
Evaluación numérica y analítica de la brecha $E[g(X)] - g(E[X])$ mediante la desigualdad de Jensen y la identidad $E[X^2] - (E[X])^2 = \operatorname{Var}(X)$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab12-01` | Confunde E[$X^2$] y E[X]^2 | skipped_step | high | Calcula $E[X^2] = (E[X])^2 = 4$ | Eleve cada realización al cuadrado antes de promediar para hallar $E[X^2] = (1^2+3^2)/2 = 5$. |
| `D-Hab12-02` | Brecha igual a media | skipped_step | high | Asume que $E[g(X)] - g(E[X]) = E[X]$ | Calcule la diferencia exacta para $g(x)=x^2$ como $E[X^2] - (E[X])^2 = \operatorname{Var}(X)$. |
| `D-Hab12-03` | Olvida pesos | conceptual_swap | high | Promedia $1^2$ y $3^2$ sin dividir entre el total de probabilidades | Pondere cada valor $g(x_i)$ por su probabilidad $p_i$ (aquí $0.5$) al calcular $E[g(X)]$. |
| `D-Hab12-04` | Resta inversa | conceptual_swap | high | Calcula $g(E[X]) - E[g(X)] = 4 - 5 = -1$ como exceso de Jensen | Reste $E[g(X)] - g(E[X]) \ge 0$ cuando $g$ es convexa, pues el promedio de la función supera a la función del promedio. |
| `D-Hab12-05` | Confunde desv. y var. | conceptual_swap | high | Iguala la brecha $E[X^2] - (E[X])^2$ a la desviación estándar $\sigma$ | Mantenga la varianza $\operatorname{Var}(X)$ sin raíz cuadrada al expresar $E[X^2] - (E[X])^2$. |
| `D-Hab12-06` | Extrapolación lineal | conceptual_swap | high | Usa $\operatorname{Var}(X)$ como brecha para cualquier función $g(x)$ | Limite la identidad exacta $E[g(X)] - g(E[X]) = \operatorname{Var}(X)$ al caso cuadrático $g(x)=x^2$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab12-01` | - | La variable $X$ tiene segundo momento finito $E[X^2] < \infty$ | Si $E[X^2]$ diverge, la varianza y la brecha no están definidas. | - |

---

### [C-22] Convergencia Casi Segura (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 33: Convergencia Casi Segura
- **Prerequisites:** C-02
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 33)

#### Description & Cognitive Model
Convergencia de la trayectoria completa $X_n \xrightarrow{a.s.} c \iff P(\lim_{n\to\infty} X_n = c) = 1$, más exigente que la convergencia en probabilidad

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C22-01` | Equivalente a prob. | conceptual_swap | high | Convergencia casi segura y en probabilidad son equivalentes | Recuerde que la convergencia casi segura exige estabilidad de toda la trayectoria, mientras la en probabilidad evalúa cada $n$ por separado. |
| `D-C22-02` | Permite salidas infinitas | conceptual_swap | high | Bajo $X_n \xrightarrow{a.s.} c$, la trayectoria puede salir de $c \pm \epsilon$ infinitas veces | Note que $P(\lim X_n = c) = 1$ garantiza que, desde cierto $n$, la trayectoria queda para siempre dentro de $c \pm \epsilon$. |
| `D-C22-03` | N fijo para toda trayectoria | conceptual_swap | high | El índice $n$ a partir del cual queda en $c \pm \epsilon$ es igual para todas las trayectorias | Aclare que el índice umbral depende de cada trayectoria aleatoria particular, aunque exista con probabilidad $1$. |
| `D-C22-04` | Ley débil en monedas | conceptual_swap | high | La ley fuerte de los grandes números solo garantiza convergencia en probabilidad | Asocie la LFGN con convergencia casi segura: la proporción muestral converge a la probabilidad teórica con probabilidad $1$. |
| `D-C22-05` | Probabilidad mayor a 0 | conceptual_swap | high | $P(\lim_{n\to\infty} X_n = c) > 0$ basta para convergencia casi segura | Exija que la probabilidad del evento límite sea exactamente $1$ (casi seguramente). |
| `D-C22-06` | Confunde lim y P | conceptual_swap | high | $\lim_{n\to\infty} P(X_n = c) = 1$ es la definición de convergencia casi segura | Mantenga el límite dentro de la probabilidad $P(\lim_{n\to\infty} X_n = c) = 1$, pues evalúa el comportamiento de la sucesión completa. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C22-01` | - | Todas las variables $X_n$ viven en un mismo espacio de probabilidad $(\Omega, \mathcal{F}, P)$ | La convergencia casi segura evalúa trayectorias $\omega \in \Omega$ y carece de sentido sin espacio conjunto. | - |

---

### [C-23] Convergencia en Distribución (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 35: Convergencia en Distribución
- **Prerequisites:** C-02
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 35)

#### Description & Cognitive Model
Convergencia de funciones de distribución acumulada $X_n \xrightarrow{d} X \iff \lim_{n\to\infty} P(X_n \le x) = P(X \le x)$ en todo punto de continuidad de $F_X$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C23-01` | Compara valores | conceptual_swap | high | $X_n \xrightarrow{d} X$ implica que $X_n$ y $X$ toman valores cercanos | Recuerde que la convergencia en distribución solo compara las FDA (forma de la distribución), no la cercanía entre realizaciones. |
| `D-C23-02` | Exige todo punto x | conceptual_swap | high | Debe cumplirse $F_{X_n}(x) \to F_X(x)$ incluso en discontinuidades de $F_X$ | Excluya los puntos de discontinuidad de $F_X$ en la definición para no descartar límites degenerados naturales. |
| `D-C23-03` | Compara densidades | conceptual_swap | high | Se define igualando funciones de densidad $f_{X_n}(x) \to f_X(x)$ solamente | Use siempre la función de distribución acumulada $F_X(x) = P(X \le x)$, pues existe incluso sin densidad. |
| `D-C23-04` | No sirve para IC | conceptual_swap | high | La convergencia en distribución no permite usar valores críticos normales en muestras grandes | Aplique la convergencia en distribución justamente para justificar el uso de valores críticos límite ($1.645, 1.96$) en inferencia. |
| `D-C23-05` | Confunde con $X_n$ = X | conceptual_swap | high | Solo hay convergencia en distribución si $X_n$ tiene exactamente la distribución límite para todo $n$ | Permita que las distribuciones finitas difieran de $F_X$, siempre que se aproximen a ella cuando $n \to \infty$. |
| `D-C23-06` | Requiere mismo espacio | conceptual_swap | high | $X_n \xrightarrow{d} X$ requiere que $X_n$ y $X$ estén definidas juntas | Note que solo depende de las distribuciones marginales $F_{X_n}$ y $F_X$, sin requerir espacio conjunto. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C23-01` | - | La convergencia de $F_{X_n}(x)$ se evalúa únicamente en los puntos $x$ donde $F_X$ es continua | En discontinuidades de $F_X$ el límite puede no coincidir sin invalidar la convergencia. | - |

---

### [C-25] Ley de los Grandes Números (LGN) (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 40: Ley de los Grandes Números (LGN)
- **Prerequisites:** C-02, C-10
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 40)

#### Description & Cognitive Model
Convergencia del promedio muestral $\bar{Y}_n = \frac{1}{n}\sum_{i=1}^n Y_i$ hacia la media poblacional $\mu$ en probabilidad (ley débil) o casi segura (ley fuerte) cuando $n \to \infty$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C25-01` | Confunde con normalidad | conceptual_swap | high | $\bar{Y}_n \xrightarrow{d} N(0,1)$ | Distinga convergencia al parámetro $\mu$ (LGN) de la forma normal de los errores alrededor de $\mu$ (TCL). |
| `D-C25-02` | Converge a varianza | conceptual_swap | high | $\bar{Y}_n \xrightarrow{p} \sigma^2$ | Recuerde que el promedio muestral estima la esperanza poblacional $\mu$, no la varianza $\sigma^2$. |
| `D-C25-03` | Exige normalidad | conceptual_swap | high | $Y_i \sim N(\mu,\sigma^2)$ necesario | Verifique las hipótesis de Khinchine y Kolmogorov: basta independencia, idéntica distribución y media finita. |
| `D-C25-04` | Varianza constante | conceptual_swap | high | $\mathrm{Var}(\bar{Y}_n) = \sigma^2$ | Divida la varianza entre $n$: $\mathrm{Var}(\bar{Y}_n)=\sigma^2/n \to 0$ cuando la muestra crece. |
| `D-C25-05` | Confunde muestra con dato | conceptual_swap | high | $Y_n \xrightarrow{p} \mu$ | Aplique el límite al promedio $\bar{Y}_n$, no a una observación individual $Y_n$ cuya dispersión no se reduce. |
| `D-C25-06` | Da tasa de error | conceptual_swap | high | $|\bar{Y}_n - \mu| = O(1/n)$ | Separe ambos teoremas: la LGN asegura que el error tiende a cero, pero la tasa $1/\sqrt{n}$ proviene del TCL. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C25-01` | - | Variables $Y_1, \dots, Y_n$ i.i.d. con esperanza finita $E[Y_i]=\mu$ | Sin media finita o independencia la compensación de errores falla y $\bar{Y}_n$ no converge. | - |

---

### [C-26] Teorema Central del Límite (TCL) (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 42: Teorema Central del Límite (TCL)
- **Prerequisites:** C-25
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 42)

#### Description & Cognitive Model
Convergencia en distribución del promedio estandarizado $Z_n = \frac{\sqrt{n}(\bar{Y}_n - \mu)}{\sigma} \xrightarrow{d} N(0,1)$, implicando $\bar{Y}_n \stackrel{a}{\sim} N(\mu, \sigma^2/n)$ para muestras grandes

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C26-01` | Omite factor raíz de n | conceptual_swap | high | $\frac{\bar{Y}_n - \mu}{\sigma} \xrightarrow{d} N(0,1)$ | Multiplique por $\sqrt{n}$ en el numerador o divida $\sigma$ entre $\sqrt{n}$; sin ese factor el límite colapsa a $0$. |
| `D-C26-02` | Factor n sin raíz | conceptual_swap | high | $\frac{n(\bar{Y}_n - \mu)}{\sigma} \xrightarrow{d} N(0,1)$ | Use la desviación estándar $\sigma/\sqrt{n}$ del promedio: los errores se encogen a ritmo $1/\sqrt{n}$, no $1/n$. |
| `D-C26-03` | Varianza sin dividir por n | conceptual_swap | high | $\bar{Y}_n \stackrel{a}{\sim} N(\mu, \sigma^2)$ | Recuerde que la varianza de la media muestral es $\sigma^2/n$, por lo que disminuye al aumentar $n$. |
| `D-C26-04` | Aplica a dato individual | conceptual_swap | high | $Y_i \stackrel{a}{\sim} N(\mu, \sigma^2)$ | Aplique el TCL al promedio $\bar{Y}_n$: la distribución de cada dato individual $Y_i$ conserva su forma original. |
| `D-C26-05` | Exige simetría previa | conceptual_swap | high | Solo vale si $Y_i$ es simétrica | Aplique el TCL aunque $Y_i$ sea muy asimétrica; basta que $n$ sea grande y $0 < \sigma^2 < \infty$. |
| `D-C26-06` | Confunde con exactitud | conceptual_swap | high | $\bar{Y}_n \sim N(\mu, \sigma^2/n)$ exacto | Interprete $\stackrel{a}{\sim}$ como aproximación asintótica: con $n$ finito puede persistir ligera asimetría. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C26-01` | - | Variables $Y_i$ i.i.d. con media $\mu$ y varianza finita $0 < \sigma^2 < \infty$ | Si la varianza es infinita o nula, la estandarización por $\sigma/\sqrt{n}$ no converge a $N(0,1)$. | - |

---

### [Hab-14] Aproximación Normal de Probabilidades Muestrales (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 43: Aproximación Normal de Probabilidades Muestrales
- **Prerequisites:** C-26
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 43)

#### Description & Cognitive Model
Cálculo aproximado de probabilidades sobre la media muestral $P(\bar{Y}_n > c) \approx P\left(Z > \frac{c - \mu}{\sigma/\sqrt{n}}\right)$ mediante el TCL usando la desviación estándar $\sigma/\sqrt{n}$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab14-01` | Estandariza con sigma | skipped_step | high | $Z = \frac{c - \mu}{\sigma}$ | Divida $\sigma$ entre $\sqrt{n}$ antes de estandarizar: el error estándar de $\bar{Y}_n$ es $\sigma/\sqrt{n}$, no $\sigma$. |
| `D-Hab14-02` | Divide por n en lugar de raíz | conceptual_swap | high | $Z = \frac{c - \mu}{\sigma/n}$ | Aplique $\sqrt{n}$ en el error estándar $\sigma/\sqrt{n}$; dividir entre $n$ corresponde a la varianza cuando $\sigma=1$. |
| `D-Hab14-03` | Usa varianza en denominador | skipped_step | high | $Z = \frac{c - \mu}{\sigma^2/n}$ | Extraiga la raíz cuadrada de la varianza $\sigma^2/n$ para obtener el error estándar $\sigma/\sqrt{n}$ antes de estandarizar. |
| `D-Hab14-04` | Invierte signo de diferencia | conceptual_swap | high | $P(Z > \frac{\mu - c}{\sigma/\sqrt{n}})$ | Respete el orden $c - \mu$ al estandarizar ambos lados de $\bar{Y}_n > c$ para preservar el sentido de la desigualdad. |
| `D-Hab14-05` | Confunde cola superior | conceptual_swap | high | $P(\bar{Y}_n > c) \approx \Phi(z)$ | Calcule el complemento $1 - \Phi(z)$ cuando la desigualdad pide cola derecha $P(Z > z)$. |
| `D-Hab14-06` | Ignora diferencia asintótica | conceptual_swap | high | $P(\bar{Y}_n > c) = P_{\text{exacta}}$ | Recuerde que la normal es una aproximación asintótica y puede diferir levemente de la distribución exacta con $n$ finito. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab14-01` | - | Tamaño muestral $n$ suficientemente grande para que la asimetría residual sea pequeña | Con $n$ muy pequeño y datos muy asimétricos la aproximación normal pierde precisión. | - |

---

### [Hab-15] Intervalos de Confianza Asintóticos para Proporciones (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 44: Intervalos de Confianza Asintóticos para Proporciones
- **Prerequisites:** C-26
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 44)

#### Description & Cognitive Model
Cálculo del error estándar $ee(\hat{p}) = \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$, el intervalo $IC_{95\%}: \hat{p} \pm 1.96\,ee(\hat{p})$ y el escalado del margen de error con $1/\sqrt{n}$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab15-01` | Olvida raíz en error estándar | skipped_step | high | $ee(\hat{p}) = \frac{\hat{p}(1-\hat{p})}{n}$ | Aplique la raíz cuadrada a la varianza $\hat{p}(1-\hat{p})/n$ para obtener el error estándar en unidades de proporción. |
| `D-Hab15-02` | Duplica n para mitad de error | skipped_step | high | Duplicar $n$ reduce error a mitad | Recuerde que el margen baja con $1/\sqrt{n}$: para reducirlo a la mitad debe cuadruplicar el tamaño de muestra. |
| `D-Hab15-03` | Omite factor 1 menos p | conceptual_swap | high | $ee(\hat{p}) = \sqrt{\frac{\hat{p}}{n}}$ | Incluya ambos factores de la varianza Bernoulli $\hat{p}(1-\hat{p})$ en el numerador antes de dividir entre $n$. |
| `D-Hab15-04` | Usa valor crítico erróneo | conceptual_swap | high | $IC_{95\%}: \hat{p} \pm 1.64\,ee(\hat{p})$ | Emplee el cuantil bilateral $z_{0.975}=1.96$ para confianza del $95\%$, no $1.64$ que corresponde al $90\%$. |
| `D-Hab15-05` | Divide entre n fuera de raíz | conceptual_swap | high | $ee(\hat{p}) = \frac{\sqrt{\hat{p}(1-\hat{p})}}{n}$ | Mantenga $n$ dentro del radical $\sqrt{\hat{p}(1-\hat{p})/n}$ porque la desviación estándar escala como $1/\sqrt{n}$. |
| `D-Hab15-06` | Confunde proporción con media | conceptual_swap | high | $ee(\hat{p}) = \frac{s}{\sqrt{n}}$ arbitrario | Aproveche que en variables Bernoulli $0/1$ la varianza queda determinada por $\hat{p}(1-\hat{p})$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab15-01` | - | Observaciones $Y_i \sim \mathrm{Bernoulli}(p)$ i.i.d. con $n$ grande para usar $\hat{p}$ en $ee(\hat{p})$ | En muestras pequeñas la aproximación normal y el reemplazo de $p$ por $\hat{p}$ pierden validez. | - |

---

### [C-27] Teorema de la Aplicación Continua (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 46: Teorema de la Aplicación Continua
- **Prerequisites:** C-25
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 46)

#### Description & Cognitive Model
Preservación de la convergencia bajo funciones continuas $g$: si $X_n \xrightarrow{p} c$ y $g$ es continua en $c$, entonces $g(X_n) \xrightarrow{p} g(c)$ (y análogamente $X_n \xrightarrow{d} X \Rightarrow g(X_n) \xrightarrow{d} g(X)$)

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C27-01` | Aplica Jensen al plim | conceptual_swap | high | $\mathrm{plim}\, g(X_n) \ne g(\mathrm{plim}\, X_n)$ | Distinga esperanza y límite en probabilidad: aunque $E[g(X)] \ne g(E[X])$, el $\mathrm{plim}$ sí atraviesa funciones continuas. |
| `D-C27-02` | Confunde consistencia con insesgamiento | conceptual_swap | high | $g(X_n)$ es insesgado para $g(c)$ | Recuerde que transformaciones no lineales como $\sqrt{s^2}$ o $1/\bar{Y}$ son sesgadas en muestras finitas aunque sean consistentes. |
| `D-C27-03` | Ignora continuidad en el límite | conceptual_swap | high | Vale para cualquier $g$ discontinua | Verifique que $g$ sea continua en el punto límite $c$; si hay discontinuidad en $c$, el límite puede no preservarse. |
| `D-C27-04` | Restringe a funciones lineales | conceptual_swap | high | Solo vale si $g(x)=ax+b$ | Aplique el teorema a funciones no lineales continuas como raíces, cuadrados o cocientes fuera de cero. |
| `D-C27-05` | Divide por cero en el límite | conceptual_swap | high | $1/\bar{Y}_n \xrightarrow{p} 1/\mu$ si $\mu=0$ | Compruebe $\mu \ne 0$ antes de aplicar $g(x)=1/x$, pues $g$ no es continua en $0$. |
| `D-C27-06` | Solo sirve para plim | conceptual_swap | high | No aplica a convergencia en distribución | Recuerde que el teorema también preserva la convergencia en distribución bajo transformaciones continuas. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C27-01` | - | Continuidad de la función $g$ en el punto límite $c$ (o en el soporte de $X$) | En puntos de discontinuidad pequeños errores en $X_n$ pueden generar saltos en $g(X_n)$. | - |

---

### [C-28] Teorema de Slutsky (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 48: Teorema de Slutsky
- **Prerequisites:** C-26, C-27
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 48)

#### Description & Cognitive Model
Combinación asintótica cuando $B_n \xrightarrow{d} B$ y $A_n \xrightarrow{p} a$ (constante): $A_n+B_n \xrightarrow{d} a+B$, $A_n B_n \xrightarrow{d} aB$ y $B_n/A_n \xrightarrow{d} B/a$ ($a \ne 0$), permitiendo sustituir $\sigma$ por $s$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C28-01` | Aplica con dos distribuciones | conceptual_swap | high | $A_n \xrightarrow{d} A, B_n \xrightarrow{d} B \Rightarrow A_n B_n \xrightarrow{d} AB$ | Exija que una de las sucesiones converja en probabilidad a una constante $a$; con dos límites en distribución no está garantizado. |
| `D-C28-02` | Permite constante cero en cociente | conceptual_swap | high | $B_n/A_n \xrightarrow{d} B/a$ si $a=0$ | Verifique que el límite constante del denominador sea $a \ne 0$ antes de aplicar el cociente de Slutsky. |
| `D-C28-03` | Cambia distribución límite por s | conceptual_swap | high | $\frac{\bar{Y}-\mu_0}{s/\sqrt{n}}$ requiere datos normales | Aplique Slutsky con $\sigma/s \xrightarrow{p} 1$ y el TCL: en muestras grandes el estadístico $t$ converge a $N(0,1)$ sin normalidad. |
| `D-C28-04` | Multiplica varianza por a sin cuadrado | conceptual_swap | high | $aB \sim N(0, a\sigma^2)$ | Eleve al cuadrado la constante $a$ al calcular la varianza de $aB$, aunque la media escale por $a$. |
| `D-C28-05` | Exige independencia entre An y Bn | conceptual_swap | high | Requiere $A_n \perp B_n$ | Recuerde que Slutsky no exige independencia entre $A_n$ y $B_n$ porque $A_n$ colapsa a una constante determinista. |
| `D-C28-06` | Confunde con esperanza de producto | conceptual_swap | high | $E[A_n B_n] = a E[B]$ finito | Limite la conclusión de Slutsky a la distribución asintótica, no a igualdades exactas de esperanzas en muestras finitas. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C28-01` | - | Convergencia en probabilidad de $A_n$ a una constante $a$ (con $a \ne 0$ en cocientes) | Si $A_n$ converge solo en distribución a una variable aleatoria, la distribución conjunta con $B_n$ es necesaria. | - |

---

### [C-29] El Método Delta (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 50: El Método Delta
- **Prerequisites:** C-26
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 50)

#### Description & Cognitive Model
Aproximación normal asintótica de una transformación suave $g(\hat{\theta})$: si $\sqrt{n}(\hat{\theta}-\theta) \xrightarrow{d} N(0,V)$ y $g'(\theta)\ne 0$, entonces $\sqrt{n}(g(\hat{\theta})-g(\theta)) \xrightarrow{d} N(0, [g'(\theta)]^2 V)$

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C29-01` | Olvida elevar derivada al cuadrado | conceptual_swap | high | $\mathrm{Var}_{a}(g(\hat{\theta})) = g'(\theta) V$ | Eleve al cuadrado la pendiente $g'(\theta)$ en la varianza asintótica $[g'(\theta)]^2 V$, ya que $\mathrm{Var}(cX)=c^2\mathrm{Var}(X)$. |
| `D-C29-02` | Evalúa g en vez de derivada | conceptual_swap | high | $\mathrm{Var}_{a}(g(\hat{\theta})) = [g(\theta)]^2 V$ | Derive primero la función $g$ mediante Taylor de primer orden: la incertidumbre escala con la pendiente $g'(\theta)$, no con $g(\theta)$. |
| `D-C29-03` | Aplica g a la varianza | conceptual_swap | high | $\mathrm{Var}_{a}(g(\hat{\theta})) = g(V)$ | Multiplique la varianza $V$ por $[g'(\theta)]^2$; la función $g$ transforma el estimador, no directamente su varianza. |
| `D-C29-04` | Ignora condición de derivada no nula | conceptual_swap | high | Válido aunque $g'(\theta)=0$ | Verifique $g'(\theta) \ne 0$: si la primera derivada se anula, el término lineal desaparece y la aproximación normal falla. |
| `D-C29-05` | Exige función lineal | conceptual_swap | high | Solo vale si $g$ es lineal | Aplique el método delta precisamente a funciones no lineales suaves, aproximándolas localmente por su recta tangente. |
| `D-C29-06` | Omite valor absoluto en ee | conceptual_swap | high | $ee(g(\hat{\theta})) = g'(\hat{\theta})\,ee(\hat{\theta})$ | Tome valor absoluto $|g'(\hat{\theta})|$ al calcular el error estándar para garantizar una magnitud no negativa. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C29-01` | - | Diferenciabilidad continua de $g$ en $\theta$ con derivada no nula $g'(\theta) \ne 0$ | Si $g'(\theta)=0$ o $g$ no es derivable en $\theta$, la expansión de Taylor de primer orden colapsa. | - |

---

### [Hab-16] Cálculo de Error Estándar e IC por Método Delta (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 51: Cálculo de Error Estándar e IC por Método Delta
- **Prerequisites:** C-29
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 51)

#### Description & Cognitive Model
Derivación de $g'(\hat{\theta})$, cálculo del error estándar $ee(g(\hat{\theta})) \approx |g'(\hat{\theta})|\cdot ee(\hat{\theta})$ y construcción del intervalo $IC_{95\%}: g(\hat{\theta}) \pm 1.96\,ee(g(\hat{\theta}))$ para funciones no lineales

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab16-01` | Omite valor absoluto en derivada | skipped_step | high | $ee(1/\bar{Y}) = -0.25 \times 0.1 = -0.025$ | Aplique valor absoluto a $g'(\hat{\theta})$ antes de multiplicar por $ee(\hat{\theta})$ porque todo error estándar es positivo. |
| `D-Hab16-02` | Transforma extremos con g | skipped_step | high | $ee(1/\bar{Y}) = 1/ee(\bar{Y})$ | No aplique $g$ directamente al error estándar; multiplique $ee(\bar{Y})$ por la magnitud de la derivada $|g'(\bar{y})|$. |
| `D-Hab16-03` | Deriva incorrectamente 1 sobre m | conceptual_swap | high | $g'(m) = 1/m^2$ | Derive $m^{-1}$ correctamente como $-m^{-2}$; aunque el valor absoluto coincida, el signo es clave en Taylor. |
| `D-Hab16-04` | Multiplica por derivada al cuadrado | conceptual_swap | high | $ee(g(\hat{\theta})) = [g'(\hat{\theta})]^2 ee(\hat{\theta})$ | Recuerde que el cuadrado $[g'(\hat{\theta})]^2$ multiplica a la varianza, mientras que al error estándar se multiplica por $|g'(\hat{\theta})|$. |
| `D-Hab16-05` | Centra IC en estimador original | conceptual_swap | high | $IC_{95\%}: \bar{y} \pm 1.96\,ee(1/\bar{Y})$ | Centre el intervalo de confianza en el estimador transformado $g(\bar{y})$, no en el parámetro original $\bar{y}$. |
| `D-Hab16-06` | Usa ee original en IC transformado | conceptual_swap | high | $IC_{95\%}: g(\bar{y}) \pm 1.96\,ee(\bar{Y})$ | Sustituya $ee(\bar{Y})$ por $ee(g(\bar{Y}))$ escalado por $|g'(\bar{y})|$ al construir el intervalo del parámetro transformado. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab16-01` | - | Estimador $\hat{\theta}$ con $g'(\hat{\theta}) \ne 0$ y distribución asintóticamente normal | Cerca de puntos donde $g'$ se anula o cambia bruscamente, el intervalo simétrico pierde cobertura. | - |

---
