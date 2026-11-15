# Cognitive Task Analysis (CTA): Estadistica 3 S9 Vmapreduce Vlean43 V3

- **Course ID:** `estadistica_3_s9_vmapreduce_vlean43_v3`
- **Macro-Competency:** Dominio y aplicación analítica integral de Estadistica 3 S9 Vmapreduce Vlean43 V3
- **Structure:** 20 total competencies (0 Facts, 11 Concepts, 9 Skills) with 270 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `PRE-01` | Monotonía de la Esperanza y Desigualdad de Chebyshev | Skill | Understand | Unidad 17: Monotonía de la Esperanza y Cota de Chebyshev | - | 18 |
| `C-01` | Muestra i.i.d. y Propiedades de Estimadores en Muestras Finitas | Concept | Understand | Unidad 4: Criterio de Muestra Grande y Colas Extremas | - | 30 |
| `Hab-01` | Descomposición del ECM y Dilema Sesgo-Varianza | Skill | Apply | Unidad 6: Descomposición del ECM y Dilema Sesgo-Varianza | C-01 | 12 |
| `Hab-02` | Momentos de Media y Varianza Muestral sin Normalidad | Skill | Apply | Unidad 9: Momentos de Media y Varianza Muestral sin Normalidad | C-01 | 12 |
| `C-03` | Sucesiones Aleatorias, Convergencia en Probabilidad y Consistencia | Concept | Understand | Unidad 10: Convergencia en Probabilidad y Consistencia Débil | C-01 | 18 |
| `C-04` | Convergencia en Media r-ésima, Media Cuadrática y Tasa Asintótica | Concept | Understand | Unidad 11: Convergencia en Media r-ésima y Media Cuadrática | Hab-01, C-03 | 18 |
| `Hab-04` | Demostración y Aplicación de la Desigualdad de Markov | Skill | Apply | Unidad 14: Demostración y Aplicación de la Desigualdad de Markov | C-03 | 12 |
| `C-05` | Desigualdad de Jensen y Sesgo No Lineal | Concept | Understand | Unidad 17: Desigualdad de Jensen y Sesgo No Lineal | PRE-01 | 12 |
| `C-06` | Desigualdad de Cauchy-Schwarz y Correlación | Concept | Understand | Unidad 18: Desigualdad de Cauchy-Schwarz y Correlación | PRE-01 | 6 |
| `C-07` | Convergencia Casi Segura y Jerarquía de Modos de Convergencia | Concept | Analyze | Unidad 20: Jerarquía de Modos de Convergencia | PRE-01, C-05 | 18 |
| `Hab-06` | Análisis de Contraejemplos entre Modos de Convergencia | Skill | Analyze | Unidad 22: Contraejemplo de Convergencia en Probabilidad sin L^r | C-07 | 12 |
| `Hab-07` | Insesgadez, Consistencia y Evaluación mediante ECM | Skill | Apply | Unidad 24: Evaluación de Insesgadez y Consistencia en M_A, M_B, M_C | PRE-01, C-07 | 18 |
| `C-08` | Espacio de Probabilidad, Variables Aleatorias y Momentos | Concept | Understand | Unidad 13: Espacio de Probabilidad y Axiomas de Kolmogorov | - | 24 |
| `C-20` | Convergencia en Distribución | Concept | Understand | Unidad 35: Convergencia en Distribución | C-03, C-08 | 6 |
| `C-22` | Ley de los Grandes Números (LGN) | Concept | Understand | Unidad 40: Ley de los Grandes Números (LGN) | C-03, C-07, C-08 | 6 |
| `C-23` | Teorema Central del Límite (TCL) | Concept | Understand | Unidad 42: Teorema Central del Límite (TCL) | C-22 | 6 |
| `Hab-15` | Inferencia Asintótica para Medias y Proporciones vía TCL | Skill | Apply | Unidad 43: Cálculo de Probabilidades Asintóticas para Medias | C-23 | 12 |
| `C-24` | Teorema de la Aplicación Continua (CMT) y Teorema de Slutsky | Concept | Understand | Unidad 46: Teorema de la Aplicación Continua (CMT) | C-22 | 12 |
| `Hab-17` | Contraste de Hipótesis Asintótico con Varianza Desconocida | Skill | Apply | Unidad 49: Contraste de Hipótesis Asintótico con Varianza Desconocida | C-24 | 6 |
| `C-26` | Método Delta: Estimación de Error Estándar e Intervalos | Skill | Understand | Unidad 50: El Método Delta | C-23 | 12 |

---

## Detailed Competency Specifications

### [PRE-01] Monotonía de la Esperanza y Desigualdad de Chebyshev (Skill)

- **Bloom Level:** Understand
- **Session:** Unidad 17: Monotonía de la Esperanza y Cota de Chebyshev
- **Prerequisites:** None
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 17), `Clases_sintetizadas_semana_9.pdf` (page 16), `EST3_LEC07_26.2_V2.pdf` (page 23)

#### Description & Cognitive Model
Monotonía de la esperanza ($U\ge V$ c.s. $\Rightarrow\mathbb{E}[U]\ge\mathbb{E}[V]$), deducción de Chebyshev generalizada $\mathbb{P}(|X-c|\ge\varepsilon)\le\mathbb{E}[|X-c|^r]/\varepsilon^r$ vía Markov, forma clásica $\mathbb{P}(|X-\mu|\ge k\sigma)\le 1/k^2$ y cota en términos de $\mathrm{ECM}$.

#### Fused Distractor Models (18)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-PRE01-01` | Invierte desigualdad | conceptual_swap | high | $\mathbb{P}(|\hat{\beta}_n-\beta|>\varepsilon)\ge\frac{\mathrm{ECM}(\hat{\beta}_n)}{\varepsilon^2}$ | Invierta el sentido: la desigualdad de Chebyshev acota superiormente la probabilidad de cola, por lo que $\mathbb{P}$ siempre es menor o igual que $\mathrm{ECM}/\varepsilon^2$. |
| `D-PRE01-02` | Omite cuadrado en eps | conceptual_swap | high | $\mathbb{P}(|\hat{\beta}_n-\beta|>\varepsilon)\le\frac{\mathrm{ECM}(\hat{\beta}_n)}{\varepsilon}$ | Eleve el umbral al cuadrado: al definir la variable auxiliar cuadrática $(\hat{\beta}_n-\beta)^2$, la transformación del umbral exige dividir entre $\varepsilon^2$. |
| `D-PRE01-03` | Solo usa varianza | conceptual_swap | high | $\mathbb{P}(|\hat{\beta}_n-\beta|>\varepsilon)\le\frac{\mathrm{Var}(\hat{\beta}_n)}{\varepsilon^2}$ | Incluya el sesgo al cuadrado cuando $\mathbb{E}[\hat{\beta}_n]\neq\beta$: centrar en el parámetro $\beta$ exige $\mathbb{E}[(\hat{\beta}_n-\beta)^2]=\mathrm{ECM}(\hat{\beta}_n)$. |
| `D-PRE01-04` | Invierte monotonía | conceptual_swap | high | $U\ge V\Rightarrow\mathbb{E}[U]\le\mathbb{E}[V]$ | Conserve el sentido de la desigualdad al tomar esperanza: como $\mathbb{E}[U-V]\ge 0$ para variables no negativas, la monotonía preserva $\mathbb{E}[U]\ge\mathbb{E}[V]$. |
| `D-PRE01-05` | Confunde cota con igualdad | conceptual_swap | high | $\mathbb{P}(|\hat{\beta}_n-\beta|>\varepsilon)=\frac{\mathrm{ECM}(\hat{\beta}_n)}{\varepsilon^2}$ | Trate la expresión como cota superior y no como igualdad exacta: Chebyshev provee un límite válido para cualquier distribución con segundo momento finito. |
| `D-PRE01-06` | ECM cero no basta | conceptual_swap | high | $\mathrm{ECM}(\hat{\beta}_n)\to 0\text{ no implica }\hat{\beta}_n\xrightarrow{p}\beta$ | Aplique el teorema del sándwich sobre la cota de Chebyshev: si $\mathrm{ECM}(\hat{\beta}_n)\to 0$, la probabilidad en las colas queda atrapada hacia cero. |
| `D-PRE01-07` | Omitir potencia r en el denominador | skipped_step | high | $\mathbb{P}(|X-c|\ge\varepsilon)\le\frac{\mathbb{E}[|X-c|^r]}{\varepsilon}$ | Transforme ambos lados de $|X-c|\ge\varepsilon$ mediante $h(u)=u^r$ para fijar $\delta=\varepsilon^r$ en el denominador de Markov. |
| `D-PRE01-08` | Confundir desviación estándar con varianza | conceptual_swap | high | $\mathbb{P}(|X-\mu|\ge\varepsilon)\le\frac{\operatorname{Var}(X)}{\varepsilon}$ | Fije $r=2$ y $c=\mu$ para obtener $\mathbb{E}[(X-\mu)^2]=\operatorname{Var}(X)$ en el numerador y $\varepsilon^2$ en el denominador. |
| `D-PRE01-09` | Transformación para r<=0 | skipped_step | high | $h(u)=u^r$ es estrictamente creciente para cualquier $r\in\mathbb{R}$ | Verifique $r>0$ de modo que $h'(u)=ru^{r-1}>0$ en $(0,\infty)$ y se preserve el sentido de la desigualdad de eventos. |
| `D-PRE01-10` | Aplicar Chebyshev directo a X sin valor absoluto | skipped_step | high | Define $Y=(X-c)^r$ para $r$ impar sin valor absoluto | Defina $Y=|X-c|^r\ge 0$ para garantizar no negatividad y poder aplicar válidamente la desigualdad de Markov. |
| `D-PRE01-11` | Fallo en desigualdad estricta | conceptual_swap | high | Chebyshev no aplica a $\mathbb{P}(|X-c|>\varepsilon)$ porque Markov usa $\ge$ | Use la inclusión de eventos $\{|X-c|>\varepsilon\}\subseteq\{|X-c|\ge\varepsilon\}$ para mantener válida la misma cota superior. |
| `D-PRE01-12` | Centrar en c != mu llamando varianza al numerador | conceptual_swap | high | $\mathbb{P}(|X-c|\ge\varepsilon)\le\frac{\operatorname{Var}(X)}{\varepsilon^2}$ para cualquier $c\in\mathbb{R}$ | Recuerde que $\mathbb{E}[(X-c)^2]=\operatorname{Var}(X)+(\mu-c)^2$; solo cuando $c=\mu$ el numerador se reduce exactamente a $\operatorname{Var}(X)$. |
| `D-PRE01-13` | Omite elevar umbral al cuadrado | skipped_step | high | $P(|X - \mu| \ge \epsilon) \le \frac{\operatorname{Var}(X)}{\epsilon}$ | Eleve al cuadrado la distancia $\epsilon$ en el denominador porque Chebyshev aplica Markov a $Y = (X - \mu)^2$ con umbral $\delta = \epsilon^2$. |
| `D-PRE01-14` | Usa desviación en vez de varianza | skipped_step | high | $P(|X - \mu| \ge \epsilon) \le \frac{\sigma}{\epsilon^2}$ | Use la varianza $\sigma^2 = \operatorname{Var}(X)$ en el numerador, no la desviación estándar $\sigma$, para mantener unidades cuadráticas homogéneas. |
| `D-PRE01-15` | Confunde k con desviación absoluta | skipped_step | high | $P(|X - \mu| \ge \epsilon) \le \frac{1}{\epsilon^2}$ | Divida primero $\epsilon$ entre $\sigma$ para hallar $k = \epsilon/\sigma = 2$ antes de aplicar la forma estandarizada $1/k^2$. |
| `D-PRE01-16` | Toma complemento como cota superior | conceptual_swap | high | $P(|X - \mu| \ge k\sigma) \le 1 - \frac{1}{k^2}$ | Recuerde que $1/k^2$ acota la cola $|X-\mu| \ge k\sigma$, mientras que $1 - 1/k^2$ es cota inferior para el intervalo central. |
| `D-PRE01-17` | Aplica regla normal en lugar de cota | conceptual_swap | high | $P(|X - \mu| \ge 2\sigma) \le 0.046$ para toda distribución | Aplique $1/k^2 = 0.25$ cuando desconozca la distribución; las probabilidades normales como $4.6\%$ solo valen bajo normalidad. |
| `D-PRE01-18` | Descuenta una sola cola | conceptual_swap | high | $P(|X - \mu| \ge k\sigma) \le \frac{1}{2k^2}$ | Conserve $1/k^2$ completo: Chebyshev ya acota ambas colas simultáneamente mediante $(X-\mu)^2 \ge k^2\sigma^2$ sin asumir simetría. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-PRE01-01` | - | Existencia de segundo momento $\mathbb{E}[X^2]<\infty$ | Sin segundo momento finito el $\mathrm{ECM}$ diverge y la cota cuadrática pierde utilidad. | - |
| `A-PRE01-02` | - | Momento absoluto de orden $r>0$ finito ($\mathbb{E}[|X-c|^r]<\infty$) y $\varepsilon>0$ | Sin momento de orden $r$ finito (como en la distribución de Cauchy), la cota de Chebyshev diverge. | - |
| `A-PRE01-03` | - | La variable $X$ posee media $\mu$ y varianza finita $\sigma^2 = \operatorname{Var}(X) < \infty$ | Sin segundo momento finito no existe cota de Chebyshev. | - |

---

### [C-01] Muestra i.i.d. y Propiedades de Estimadores en Muestras Finitas (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 4: Criterio de Muestra Grande y Colas Extremas
- **Prerequisites:** None
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 4), `Clases_sintetizadas_semana_9.pdf` (page 5), `EST3_LEC07_26.2_V2.pdf` (page 3), `EST3_LEC07_26.2_V2.pdf` (page 5), `EST3_LEC07_26.2_V2.pdf` (page 7)

#### Description & Cognitive Model
Muestra aleatoria i.i.d. $Y_1,\dots,Y_n\sim F_Y$, estimador $\hat{\theta}_n$ como variable aleatoria, sesgo $\operatorname{Sesgo}(\hat{\theta}_n)=\mathbb{E}[\hat{\theta}_n]-\theta$, insesgadez, varianza, error estándar, eficiencia relativa escalar/matricial, ECM y evaluación crítica del criterio $n\ge 30$ frente a asimetría y colas extremas.

#### Fused Distractor Models (30)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Regla universal n>=30 | conceptual_swap | high | $n \ge 30$ garantiza normalidad del estadístico sin importar la distribución | Verifique asimetría y curtosis poblacional: colas pesadas ralentizan la aproximación normal en las colas críticas. |
| `D-C01-02` | Confundir centro con colas | conceptual_swap | high | La convergencia en $Z \approx 0$ implica precisión en $|Z| \approx 1.96$ | Distinga aproximación central de convergencia en colas extremas, donde se evalúan los contrastes al $\alpha=5\%$ o $1\%$. |
| `D-C01-03` | Ignorar efecto de outliers | conceptual_swap | high | Los valores atípicos no distorsionan la suma muestral cuando $n=30$ | Considere que en distribuciones leptocúrticas pocos valores extremos dominan la suma muestral y distorsionan los momentos. |
| `D-C01-04` | Normalidad exacta finita | conceptual_swap | high | Los errores poblacionales empíricos siempre siguen $\mathcal{N}(0,\sigma^2)$ | Reconozca la fragilidad distributiva del MRLC: sin normalidad exacta del PGD, los estadísticos exactos pierden validez. |
| `D-C01-05` | Independencia de alpha | conceptual_swap | high | El tamaño muestral necesario es independiente del nivel de significancia $\alpha$ | Recuerde que un nivel $\alpha$ más exigente evalúa colas más extremas y demanda mayor $n$ para controlar el error Tipo I. |
| `D-C01-06` | Confundir cuantiles t con PGD | conceptual_swap | high | Si $t_{29}$ se parece a $\mathcal{N}(0,1)$, cualquier dato con $n=30$ es normal | Separe la similitud visual entre $t_{n-1}$ y $\mathcal{N}(0,1)$ bajo errores gaussianos de la velocidad real de convergencia del TCL. |
| `D-C01-07` | Confundir estimador y estimación | conceptual_swap | high | Un estimador $\hat{\theta}_n$ es un número real fijo y determinístico | Diferencie el estimador $\hat{\theta}_n$ (variable aleatoria con distribución muestral) de la estimación puntual numérica observada. |
| `D-C01-08` | Signo invertido del sesgo | conceptual_swap | high | $\operatorname{Sesgo}(\hat{\theta}_n)=\theta-\mathbb{E}[\hat{\theta}_n]$ | Aplique la definición $\operatorname{Sesgo}(\hat{\theta}_n)=\mathbb{E}[\hat{\theta}_n]-\theta$: una subestimación esperada produce sesgo negativo. |
| `D-C01-09` | Eficiencia sin insesgadez | conceptual_swap | high | Cualquier estimador con menor $\operatorname{Var}(\hat{\theta}_n)$ es relativamente más eficiente | Exija insesgadez previa ($\mathbb{E}[\hat{\theta}_{1,n}]=\mathbb{E}[\hat{\theta}_{2,n}]=\theta$) antes de comparar varianzas para eficiencia relativa. |
| `D-C01-10` | Orden matricial por traza | conceptual_swap | high | $\Delta \succeq 0$ equivale a comparar solo los elementos diagonales de $\operatorname{Var}$ | Verifique que la matriz diferencia $\Delta=\operatorname{Var}(\hat{\theta}_{2,n})-\operatorname{Var}(\hat{\theta}_{1,n})$ sea semidefinida positiva ($c^\top\Delta c\ge 0$). |
| `D-C01-11` | Estadístico con parámetros | conceptual_swap | high | Un estadístico $T(Y_1,\dots,Y_n)$ puede depender de parámetros poblacionales $\theta$ | Recuerde que un estadístico debe ser función Borel-medible exclusivamente de la muestra observable sin parámetros desconocidos. |
| `D-C01-12` | Confundir ECM con varianza | conceptual_swap | high | $\operatorname{ECM}(\hat{\theta}_n)=\mathbb{E}[(\hat{\theta}_n-\mathbb{E}[\hat{\theta}_n])^2]$ | Centre la distancia cuadrática esperada alrededor del parámetro verdadero $\theta$: $\operatorname{ECM}(\hat{\theta}_n)=\mathbb{E}[(\hat{\theta}_n-\theta)^2]$. |
| `D-C01-13` | Confunde estimador y estimación | conceptual_swap | high | $\hat{\theta}_n=1800$ | Distinga el estimador (regla aleatoria $\hat{\theta}_n=T(Y_1,\dots,Y_n)$) de la estimación (número observado $\bar{y}$). |
| `D-C01-14` | Cree al parámetro aleatorio | conceptual_swap | high | $\theta\sim\text{distribución muestral}$ | Recuerde que el parámetro poblacional $\theta$ es una constante fija desconocida; quien varía es $\hat{\theta}_n$. |
| `D-C01-15` | Olvida independencia en i.i.d. | conceptual_swap | high | $Y_i\sim F_Y$ dependientes | Exija ambas condiciones en i.i.d.: independencia mutua entre observaciones e idéntica distribución $F_Y$. |
| `D-C01-16` | Ignora dependencia respecto a n | conceptual_swap | high | $\hat{\theta}_n=\hat{\theta}$ fijo con $n$ | Observe que el subíndice $n$ indica cómo cambia la distribución muestral de $\hat{\theta}_n$ con el tamaño de muestra. |
| `D-C01-17` | Confunde i.d. con valores iguales | conceptual_swap | high | $Y_1=Y_2=\dots=Y_n$ | Aclare que idénticamente distribuidas significa compartir la ley $F_Y$, no arrojar el mismo valor observado. |
| `D-C01-18` | Niega distribución del estimador | conceptual_swap | high | $\mathrm{Var}(\hat{\theta}_n)=0$ | Reconozca que al depender de datos aleatorios $Y_1,\dots,Y_n$, $\hat{\theta}_n$ es variable aleatoria con su distribución. |
| `D-C01-19` | Sesgo sobre una sola muestra | conceptual_swap | high | $\mathrm{Sesgo}(\hat{\theta})=\hat{\theta}_{\text{obs}}-\theta$ | Evalúe el sesgo como propiedad de la fórmula $E[\hat{\theta}]-\theta$, no como error en una muestra particular. |
| `D-C01-20` | Signo invertido del sesgo | conceptual_swap | high | $\mathrm{Sesgo}(\hat{\theta})=\theta-E[\hat{\theta}]$ | Reste $\theta$ a $E[\hat{\theta}]$: un estimador que subestima en promedio tiene sesgo negativo. |
| `D-C01-21` | Ignora constante multiplicativa | conceptual_swap | high | $E[c\bar{Y}]=\mu$ | Aplique la linealidad de la esperanza $E[c\bar{Y}]=cE[\bar{Y}]=c\mu$, lo que produce $\mathrm{Sesgo}(c\bar{Y})=(c-1)\mu$. |
| `D-C01-22` | Confunde insesgado con exacto | conceptual_swap | high | $E[\hat{\theta}]=\theta\Rightarrow \hat{\theta}=\theta$ | Recuerde que insesgadez garantiza acierto en promedio tras infinitas repeticiones, no en una muestra aislada. |
| `D-C01-23` | Sesgo igual a varianza | conceptual_swap | high | $\mathrm{Sesgo}(\hat{\theta})=E[(\hat{\theta}-\theta)^2]$ | Distinga el sesgo lineal $E[\hat{\theta}]-\theta$ del error cuadrático medio $E[(\hat{\theta}-\theta)^2]$. |
| `D-C01-24` | Linealidad aditiva errónea | conceptual_swap | high | $E[\bar{Y}]=\sum_{i=1}^n E[Y_i]$ | Conserve el factor $1/n$ al aplicar linealidad de la esperanza: $E[\bar{Y}]=\frac{1}{n}\sum_{i=1}^n\mu=\mu$. |
| `D-C01-25` | Olvida elevar factor 1/n | conceptual_swap | high | $\mathrm{Var}(\bar{Y})=\frac{\sigma^2}{n}$ omitido como $\frac{\sigma^2}{n^2}$ o $\sigma^2$ | Saque las constantes al cuadrado en la varianza: $\mathrm{Var}(\frac{1}{n}\sum Y_i)=\frac{1}{n^2}(n\sigma^2)=\frac{\sigma^2}{n}$. |
| `D-C01-26` | Confunde varianza y error estándar | conceptual_swap | high | $\mathrm{ee}(\hat{\theta})=\mathrm{Var}(\hat{\theta})$ | Tome la raíz cuadrada de la varianza para obtener $\mathrm{ee}(\hat{\theta})$ en las mismas unidades que $\theta$. |
| `D-C01-27` | Eficiencia sin insesgadez | conceptual_swap | high | $\mathrm{Var}(\hat{\theta}_1)<\mathrm{Var}(\hat{\theta}_2)\Rightarrow \hat{\theta}_1\text{ mejor}$ | Verifique primero que ambos estimadores sean insesgados antes de usar la menor varianza como criterio de eficiencia. |
| `D-C01-28` | Precisión lineal en n | conceptual_swap | high | $\mathrm{ee}(\bar{Y})=\sigma/n$ | Recuerde que el error estándar decrece con $\sqrt{n}$, por lo que $n=9$ reduce la dispersión por un factor $\sqrt{9}=3$. |
| `D-C01-29` | Mayor varianza más eficiente | conceptual_swap | high | $\mathrm{Var}(\hat{\theta}_1)>\mathrm{Var}(\hat{\theta}_2)\Rightarrow \hat{\theta}_1\text{ más eficiente}$ | Asocie mayor eficiencia a menor varianza, pues concentra más las estimaciones alrededor del valor verdadero. |
| `D-C01-30` | Suma varianzas ignorando covarianza | conceptual_swap | high | $\mathrm{Var}(\sum Y_i)=\sum\mathrm{Var}(Y_i)$ siempre | Verifique independencia o incorrelación entre $Y_i$; si hay covarianza no nula, aparecen términos cruzados. |

#### Formal Mathematical Assumptions (5)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Existencia de momentos de orden superior (asimetría y curtosis) en el PGD | Si faltan momentos o las colas son muy pesadas, la convergencia en colas falla para $n$ moderado. | - |
| `A-C01-02` | - | Muestra aleatoria simple i.i.d. con segundo momento finito $\mathbb{E}[\hat{\theta}_n^2]<\infty$ | Sin segundo momento finito no existen $\operatorname{Var}(\hat{\theta}_n)$ ni $\operatorname{ECM}(\hat{\theta}_n)$. | - |
| `A-C01-03` | - | Muestreo aleatorio simple $Y_1,\dots,Y_n\ \mathrm{i.i.d.}\sim F_Y$ | Sin i.i.d. cambian las propiedades muestrales de $T$. | - |
| `A-C01-04` | - | Linealidad de la esperanza y existencia de $E[\hat{\theta}]$ | Sin $E[\hat{\theta}]$ finito no se define el sesgo. | - |
| `A-C01-05` | - | Independencia muestral y varianza poblacional finita $\sigma^2<\infty$ | Con $\sigma^2=\infty$ o correlación falla $\sigma^2/n$. | - |

---

### [Hab-01] Descomposición del ECM y Dilema Sesgo-Varianza (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 6: Descomposición del ECM y Dilema Sesgo-Varianza
- **Prerequisites:** C-01
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 6), `EST3_LEC07_26.2_V2.pdf` (page 9)

#### Description & Cognitive Model
Derivación algebraica y cálculo de $\operatorname{ECM}(\hat{\theta}_n)=\mathbb{E}[(\hat{\theta}_n-\theta)^2]=\operatorname{Var}(\hat{\theta}_n)+[\operatorname{Sesgo}(\hat{\theta}_n)]^2$ en casos escalar y multivariado, y comparación cuantitativa del intercambio sesgo-varianza entre estimadores.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Omitir cuadrado del sesgo | skipped_step | high | $\operatorname{ECM}(\hat{\theta}_n)=\operatorname{Var}(\hat{\theta}_n)+\operatorname{Sesgo}(\hat{\theta}_n)$ | Eleve siempre el sesgo al cuadrado $[\operatorname{Sesgo}(\hat{\theta}_n)]^2$ al expandir el binomio para garantizar no negatividad. |
| `D-Hab01-02` | Término cruzado no nulo | skipped_step | high | $2(\mathbb{E}[\hat{\theta}_n]-\theta)\mathbb{E}[\hat{\theta}_n-\mathbb{E}[\hat{\theta}_n]] \neq 0$ | Aplique linealidad de la esperanza al desvío centrado: $\mathbb{E}[\hat{\theta}_n-\mathbb{E}[\hat{\theta}_n]]=0$, anulando el término cruzado. |
| `D-Hab01-03` | Transpuesta invertida matricial | conceptual_swap | high | $\operatorname{ECM}(\hat{\theta}_n)=\operatorname{Var}(\hat{\theta}_n)+\operatorname{Sesgo}(\hat{\theta}_n)^\top\operatorname{Sesgo}(\hat{\theta}_n)$ | Use el producto externo $\operatorname{Sesgo}(\hat{\theta}_n)\operatorname{Sesgo}(\hat{\theta}_n)^\top$ para obtener una matriz $k\times k$ compatible. |
| `D-Hab01-04` | Insesgado siempre óptimo | conceptual_swap | high | Un estimador insesgado siempre tiene menor ECM que cualquier estimador sesgado | Compare la suma $\operatorname{Var}+[\operatorname{Sesgo}]^2$: un sesgo pequeño con menor varianza puede reducir el ECM total. |
| `D-Hab01-05` | Suma y resta incorrecta | skipped_step | high | Introduce $\pm \theta$ fuera del cuadrado antes de aplicar la esperanza | Sume y reste $\mathbb{E}[\hat{\theta}_n]$ dentro del paréntesis cuadrático $(\hat{\theta}_n-\mathbb{E}[\hat{\theta}_n]+\mathbb{E}[\hat{\theta}_n]-\theta)^2$. |
| `D-Hab01-06` | Un componente basta para ECM->0 | conceptual_swap | high | $\operatorname{ECM}(\hat{\theta}_n)\to 0$ si solo $\operatorname{Var}(\hat{\theta}_n)\to 0$ | Recuerde que ambos términos son no negativos: $\operatorname{ECM}\to 0$ requiere que tanto $\operatorname{Var}(\hat{\theta}_n)\to 0$ como $\operatorname{Sesgo}(\hat{\theta}_n)\to 0$. |
| `D-Hab01-07` | Olvida elevar sesgo al cuadrado | skipped_step | high | $\mathrm{ECM}(\hat{\theta})=\mathrm{Var}(\hat{\theta})+\mathrm{Sesgo}(\hat{\theta})$ | Eleve el sesgo al cuadrado $[\mathrm{Sesgo}(\hat{\theta})]^2$ antes de sumarlo a la varianza para mantener unidades cuadráticas. |
| `D-Hab01-08` | No eleva c al cuadrado en Var | skipped_step | high | $\mathrm{Var}(c\bar{Y})=c\,\mathrm{Var}(\bar{Y})$ | Aplique la propiedad $\mathrm{Var}(c\bar{Y})=c^2\mathrm{Var}(\bar{Y})$ multiplicando por $0.9^2=0.81$. |
| `D-Hab01-09` | Rechaza todo estimador sesgado | conceptual_swap | high | $\mathrm{Sesgo}\neq 0\Rightarrow \mathrm{ECM}\text{ peor}$ | Compare el ECM total $\mathrm{Var}+[\mathrm{Sesgo}]^2$: un estimador ligeramente sesgado puede reducir mucho la varianza. |
| `D-Hab01-10` | Agrega término cruzado no nulo | conceptual_swap | high | $\mathrm{ECM}=\mathrm{Var}+\mathrm{Sesgo}^2+2\,\mathrm{Var}\cdot\mathrm{Sesgo}$ | Note que al sumar y restar $E[\hat{\theta}]$, el término cruzado contiene $E[\hat{\theta}-E[\hat{\theta}]]=0$ y se anula. |
| `D-Hab01-11` | Usa error estándar en vez de Var | conceptual_swap | high | $\mathrm{ECM}=\mathrm{ee}(\hat{\theta})+[\mathrm{Sesgo}(\hat{\theta})]^2$ | Sume la varianza $\mathrm{Var}(\hat{\theta})$ (no la raíz cuadrada $\mathrm{ee}$) al cuadrado del sesgo. |
| `D-Hab01-12` | Elige mayor ECM | conceptual_swap | high | $\mathrm{ECM}_1>\mathrm{ECM}_2\Rightarrow \hat{\theta}_1\text{ mejor}$ | Recuerde que el ECM mide distancia cuadrática promedio al parámetro verdadero: menor ECM indica mejor estimador. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Segundo momento finito $\mathbb{E}[\hat{\theta}_n^2]<\infty$ y linealidad del operador esperanza | Sin segundo momento finito la expansión algebraica dentro de la esperanza no está bien definida. | - |
| `A-Hab01-02` | - | Segundo momento finito $E[\hat{\theta}^2]<\infty$ para descomponer el ECM | Sin segundo momento finito el ECM diverge. | - |

---

### [Hab-02] Momentos de Media y Varianza Muestral sin Normalidad (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 9: Momentos de Media y Varianza Muestral sin Normalidad
- **Prerequisites:** C-01
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 9), `EST3_LEC07_26.2_V2.pdf` (page 11)

#### Description & Cognitive Model
Demostración y cálculo de $\mathbb{E}[\bar{Y}_n]=\mu$, $\operatorname{Var}(\bar{Y}_n)=\sigma^2/n$, cuasivarianza insesgada $\mathbb{E}[S_n^2]=\sigma^2$ y sesgo $-\sigma^2/n$ de la varianza sin corregir $m_2=\frac{1}{n}\sum(Y_i-\bar{Y})^2$ bajo muestra i.i.d. sin normalidad.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Constante lineal en varianza | skipped_step | high | $\operatorname{Var}\!\left(\frac{1}{n}\sum_{i=1}^n Y_i\right)=\frac{1}{n}\operatorname{Var}\!\left(\sum_{i=1}^n Y_i\right)$ | Aplique la propiedad cuadrática $\operatorname{Var}(cX)=c^2\operatorname{Var}(X)$ para factorizar $\frac{1}{n^2}$ y obtener $\frac{\sigma^2}{n}$. |
| `D-Hab02-02` | Confundir suma respecto a mu y $Y_bar$ | skipped_step | high | $\mathbb{E}\!\left[\sum_{i=1}^n(Y_i-\bar{Y}_n)^2\right]=n\sigma^2$ | Use la identidad $\sum(Y_i-\bar{Y}_n)^2=\sum(Y_i-\mu)^2-n(\bar{Y}_n-\mu)^2$ antes de tomar esperanza para descontar $\sigma^2$. |
| `D-Hab02-03` | Insesgadez falsa de m2 | conceptual_swap | high | $\mathbb{E}[m_2]=\sigma^2$ y $\mathbb{E}[S_n^2]=\frac{n}{n-1}\sigma^2$ | Divida $(n-1)\sigma^2$ entre $n-1$ para $S_n^2$ (insesgado) y entre $n$ para $m_2$ (sesgo negativo $-\sigma^2/n$). |
| `D-Hab02-04` | Requiere normalidad para E[S2] | conceptual_swap | high | $\mathbb{E}[S_n^2]=\sigma^2$ solo se cumple si $Y_i \sim \mathcal{N}(\mu,\sigma^2)$ | Note que la prueba usa únicamente i.i.d., $\mathbb{E}[Y_i]=\mu$ y $\operatorname{Var}(Y_i)=\sigma^2<\infty$, sin supuesto gaussiano. |
| `D-Hab02-05` | Covarianzas cruzadas no nulas | skipped_step | high | Incluye $\operatorname{Cov}(Y_i,Y_j)\neq 0$ para $i\neq j$ bajo muestra i.i.d. | Use la independencia mutua de la muestra aleatoria simple para anular $\operatorname{Cov}(Y_i,Y_j)=0$ cuando $i\neq j$. |
| `D-Hab02-06` | Sesgo persistente asintótico | conceptual_swap | high | El sesgo de $m_2$ no desaparece cuando $n\to\infty$ | Evalúe el límite $\lim_{n\to\infty}\frac{n-1}{n}\sigma^2=\sigma^2$: el sesgo $-\sigma^2/n$ tiende a cero y $m_2$ es asintóticamente insesgado. |
| `D-Hab02-07` | Divide cuasivarianza entre n | skipped_step | high | $s^2=\frac{1}{n}\sum(Y_i-\bar{Y})^2$ | Divida la suma de cuadrados entre $n-1$ grados de libertad en $s^2$ para corregir la subestimación al usar $\bar{Y}$. |
| `D-Hab02-08` | Cree insesgada a m2 | conceptual_swap | high | $E[m_2]=\sigma^2$ | Calcule $E[m_2]=\frac{n-1}{n}\sigma^2$: como $\bar{Y}$ minimiza la suma de cuadrados, $m_2$ subestima $\sigma^2$ en $\sigma^2/n$. |
| `D-Hab02-09` | Sesgo positivo de m2 | conceptual_swap | high | $E[m_2]=\frac{n+1}{n}\sigma^2$ | Recuerde que $\sum(Y_i-\bar{Y})^2=\sum(Y_i-\mu)^2-n(\bar{Y}-\mu)^2\le\sum(Y_i-\mu)^2$, por lo que $m_2$ subestima. |
| `D-Hab02-10` | Olvida restar media muestral | skipped_step | high | $s^2=\frac{1}{n-1}\sum Y_i^2$ | Reste primero la media muestral $\bar{y}$ a cada dato $Y_i$ antes de elevar los desvíos al cuadrado. |
| `D-Hab02-11` | Sesgo asintótico persistente | conceptual_swap | high | $\lim_{n\to\infty} E[m_2]\neq \sigma^2$ | Note que el sesgo $-\sigma^2/n$ tiende a cero cuando $n\to\infty$, haciendo a $m_2$ asintóticamente insesgado. |
| `D-Hab02-12` | Omite cuadrado en desvíos | conceptual_swap | high | $s^2=\frac{1}{n-1}\sum(Y_i-\bar{Y})$ | Eleve al cuadrado cada desvío $(Y_i-\bar{Y})^2$, pues la suma lineal de desvíos respecto a $\bar{Y}$ siempre es cero. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Observaciones i.i.d. con media $\mu<\infty$, varianza $\sigma^2<\infty$ y $n \ge 2$ | Con $n=1$, $S_n^2$ no está definido por división entre cero y sin independencia fallaría $\operatorname{Var}(\bar{Y}_n)=\sigma^2/n$. | - |
| `A-Hab02-02` | - | Tamaño muestral $n\ge 2$ y varianza poblacional $\sigma^2<\infty$ | Con $n=1$ la cuasivarianza divide entre cero. | - |

---

### [C-03] Sucesiones Aleatorias, Convergencia en Probabilidad y Consistencia (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 10: Convergencia en Probabilidad y Consistencia Débil
- **Prerequisites:** C-01
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 10), `EST3_LEC07_26.2_V2.pdf` (page 19), `EST3_LEC07_26.2_V2.pdf` (page 27)

#### Description & Cognitive Model
Sucesiones de variables aleatorias $\{X_n\}_{n=1}^\infty$, definición formal de convergencia en probabilidad $X_n\xrightarrow{p} c$ ($\lim_{n\to\infty}\mathbb{P}(|X_n-c|>\varepsilon)=0\ \forall\varepsilon>0$), banda geométrica $2\varepsilon$, convergencia a $X$ y consistencia débil $\operatorname{plim}_{n\to\infty}\hat{\theta}_n=\theta$.

#### Fused Distractor Models (18)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Confundir límite de probabilidad con certeza | conceptual_swap | high | $X_n \xrightarrow{p} c$ significa que $|X_n-c|\le\varepsilon$ para todo $\omega\in\Omega$ desde cierto $N$ | Distinga sucesiones reales de aleatorias: $X_n\xrightarrow{p}c$ exige que la probabilidad fuera de $[c-\varepsilon,c+\varepsilon]$ tienda a cero. |
| `D-C03-02` | Colapso degenerado hacia X | conceptual_swap | high | Si $X_n \xrightarrow{p} X$, la distribución de $X_n$ colapsa en un solo punto | Recuerde el enfoque de Greene: cuando $X_n\xrightarrow{p}X$, la diferencia $|X_n-X|$ converge a cero en probabilidad, no $X$ a una constante. |
| `D-C03-03` | Banda de ancho épsilon | conceptual_swap | high | La banda centrada en $c$ es $[c-\varepsilon/2, c+\varepsilon/2]$ de ancho $\varepsilon$ | Verifique el intervalo $[c-\varepsilon,c+\varepsilon]$ asociado a $|X_n-c|\le\varepsilon$, cuyo ancho total alrededor de $c$ es $2\varepsilon$. |
| `D-C03-04` | Consistencia solo en un punto | conceptual_swap | high | Basta que $\operatorname{plim}\hat{\theta}_n=\theta_0$ para un solo $\theta_0$ particular | Exija que $\lim_{n\to\infty}\mathbb{P}(\|\hat{\theta}_n-\theta\|>\varepsilon)=0$ se cumpla para todo $\varepsilon>0$ y todo $\theta\in\Theta$. |
| `D-C03-05` | Inversión de límite de probabilidad | conceptual_swap | high | $\lim_{n\to\infty}\mathbb{P}(|X_n-c|>\varepsilon)=1$ | Distinga el evento cola $\{|X_n-c|>\varepsilon\}$ (límite $0$) del evento interior $\{|X_n-c|\le\varepsilon\}$ (límite $1$). |
| `D-C03-06` | Confundir consistencia con insesgadez | conceptual_swap | high | Todo estimador insesgado es automáticamente consistente | Recuerde que la insesgadez es una propiedad de esperanza en muestra finita y no garantiza concentración de masa alrededor de $\theta$ si $n\to\infty$. |
| `D-C03-07` | Confunde término con sucesión | conceptual_swap | high | $X_n=\{X_1,X_2,\dots\}$ | Distinga un término concreto $X_n$ (para tamaño fijo $n$) de la sucesión completa $\{X_n\}_{n=1}^\infty$. |
| `D-C03-08` | Trata sucesión como determinista | conceptual_swap | high | $X_n\in\mathbb{R}$ fijo como $a_n$ | Recuerde que cada término $X_n$ es una variable aleatoria, por lo que converger admite distintos modos probabilísticos. |
| `D-C03-09` | Peso constante de cada nuevo dato | conceptual_swap | high | $\bar{Y}_{n+1}-\bar{Y}_n\text{ no decrece}$ | Observe que cada nueva observación pondera $1/n$ en el promedio, estabilizando $\bar{Y}_n$ al crecer $n$. |
| `D-C03-10` | Confunde índice muestral con dato | conceptual_swap | high | $X_n=Y_n$ | Diferencie la observación individual $Y_n$ del estimador acumulado $X_n=\bar{Y}_n=\frac{1}{n}\sum_{i=1}^n Y_i$. |
| `D-C03-11` | Supone convergencia exacta finita | conceptual_swap | high | $\bar{Y}_n=\mu$ para $n$ grande finito | Reconozca que en muestras finitas $\bar{Y}_n$ sigue variando aleatoriamente; la estabilización es un fenómeno asintótico. |
| `D-C03-12` | Invierte tamaño muestral en suma | conceptual_swap | high | $X_n=\sum_{i=1}^n Y_i$ | Divida la suma acumulada entre $n$ para formar $\bar{Y}_n$, de lo contrario la magnitud crece con $n$ sin estabilizarse. |
| `D-C03-13` | Confunde con límite determinista | conceptual_swap | high | $X_n \xrightarrow{p} c$ significa que $|X_n - c| = 0$ para $n$ grande | Interprete la convergencia en probabilidad como concentración probabilística: para cada $\epsilon > 0$, la probabilidad de exceder $\epsilon$ tiende a cero. |
| `D-C03-14` | Invierte desigualdad del margen | conceptual_swap | high | $\lim_{n \to \infty} P(|X_n - c| \le \epsilon) = 0$ | Verifique el evento de error $|X_n - c| > \epsilon$: es la probabilidad de alejarse más de $\epsilon$ la que tiende a $0$, mientras $P(|X_n - c| \le \epsilon) \to 1$. |
| `D-C03-15` | Exige un solo epsilon fijo | conceptual_swap | high | Basta que $P(|X_n - c| > 1) \to 0$ para garantizar $X_n \xrightarrow{p} c$ | Exija la condición para todo $\epsilon > 0$ arbitrariamente pequeño; un margen grande fijo no detecta dispersión residual menor a $1$. |
| `D-C03-16` | Confunde consistencia con normalidad | conceptual_swap | high | Un estimador es consistente solo si sus datos siguen una distribución normal | Use Chebyshev para notar que la consistencia de $\bar{Y}_n$ vía $\operatorname{Var}(\bar{Y}_n) = \sigma^2/n \to 0$ no requiere normalidad sino varianza finita. |
| `D-C03-17` | Confunde con esperanza constante | conceptual_swap | high | $\operatorname{plim} X_n = c$ equivale a $E[X_n] = c$ para todo $n$ | Recuerde que tener esperanza igual a $c$ no concentra la distribución si la varianza no decrece cuando $n \to \infty$. |
| `D-C03-18` | Omite el límite en n | conceptual_swap | high | $P(|X_n - c| > \epsilon) = 0$ para todo $n \ge 1$ | Aplique el límite $n \to \infty$: en muestras finitas la probabilidad de error es positiva (p. ej. $32\%$ con $n=25$) y solo desaparece asintóticamente. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | Sucesión $\{X_n\}_{n=1}^\infty$ y límite $X$ definidos en el mismo espacio $(\Omega,\mathcal{F},\mathbb{P})$ | Si no comparten espacio de probabilidad, la diferencia aleatoria $X_n-X$ no está definida. | - |
| `A-C03-02` | - | Todos los términos $X_n$ definidos sobre un mismo espacio $(\Omega,\mathcal{F},P)$ | Sin espacio común no se define convergencia. | - |
| `A-C03-03` | - | La sucesión de variables aleatorias $\{X_n\}_{n \ge 1}$ está definida sobre espacios de probabilidad bien especificados y $\epsilon > 0$ es arbitrario | Si el margen $\epsilon$ no puede hacerse arbitrariamente pequeño, no hay concentración en $c$. | - |

---

### [C-04] Convergencia en Media r-ésima, Media Cuadrática y Tasa Asintótica (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 11: Convergencia en Media r-ésima y Media Cuadrática
- **Prerequisites:** Hab-01, C-03
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 11), `Clases_sintetizadas_semana_9.pdf` (page 13), `EST3_LEC07_26.2_V2.pdf` (page 29)

#### Description & Cognitive Model
Convergencia en norma $L^r$ ($\mathbb{E}[|X_n-X|^r]\to 0$), criterio necesario y suficiente en media cuadrática $X_n\xrightarrow{m.s.}c \Leftrightarrow \mathbb{E}[X_n]\to c$ y $\operatorname{Var}(X_n)\to 0$, implicación hacia $\xrightarrow{p}$ y análisis del mínimo exponencial $X_{(1)}\sim\operatorname{Exp}(n\theta)$ con tasa $\mathcal{O}(1/n^2)$.

#### Fused Distractor Models (18)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Solo suficiencia en Teorema 3.4 | conceptual_swap | high | $X_n\xrightarrow{m.s.}c$ implica $\operatorname{Var}(X_n)\to 0$ pero no requiere $\mathbb{E}[X_n]\to c$ | Aplique el Teorema 3.4 completo: como $\operatorname{Var}\ge 0$ y $(\mathbb{E}[X_n]-c)^2\ge 0$, el sándwich exige que ambos tiendan a cero. |
| `D-C04-02` | Confundir E[(Xn-c)^2] con Var(Xn) | conceptual_swap | high | $\lim_{n\to\infty}\mathbb{E}[(X_n-c)^2]=0 \iff \lim_{n\to\infty}\operatorname{Var}(X_n)=0$ siempre | Distinga el desvío respecto a $\mathbb{E}[X_n]$ (varianza) del desvío respecto a $c$ (ECM); si $\mathbb{E}[X_n]\to b\neq c$, el ECM no tiende a cero. |
| `D-C04-03` | Ignorar existencia de momentos $L^r$ | conceptual_swap | high | La convergencia en $L^r$ se define aunque $\mathbb{E}[|X_n|^r]=\infty$ | Verifique previamente que los momentos absolutos $\mathbb{E}[|X_n|^r]<\infty$ y $\mathbb{E}[|X|^r]<\infty$ existan antes de evaluar $L^r$. |
| `D-C04-04` | Confundir r=1 y r=2 | conceptual_swap | high | La convergencia en media cuadrática corresponde a $r=1$ ($\mathbb{E}[|X_n-X|]\to 0$) | Asocie la media cuadrática exclusivamente con $r=2$, evaluando el límite de $\mathbb{E}[(X_n-X)^2]$. |
| `D-C04-05` | Límite de la esperanza sin cuadrado | conceptual_swap | high | $\lim_{n\to\infty}\mathbb{E}[(X_n-c)^2]=\lim_{n\to\infty}\operatorname{Var}(X_n)+(\lim_{n\to\infty}\mathbb{E}[X_n]-c)$ | Mantenga el cuadrado del sesgo $(\mathbb{E}[X_n]-c)^2$ al aplicar la descomposición del ECM en el Teorema 3.4. |
| `D-C04-06` | Límite aleatorio en Teorema 3.4 | conceptual_swap | high | El criterio $\mathbb{E}[X_n]\to X$ y $\operatorname{Var}(X_n)\to 0$ aplica cuando $X$ es aleatoria no degenerada | Restrinja la descomposición $\mathbb{E}[(X_n-c)^2]=\operatorname{Var}(X_n)+(\mathbb{E}[X_n]-c)^2$ al caso en que $c\in\mathbb{R}$ es una constante determinística. |
| `D-C04-07` | Inversión de parámetro lambda=theta/n | skipped_step | high | El mínimo muestral sigue $\operatorname{Exp}(\theta/n)$ con $\mathbb{E}[X_{(1)}]=n/\theta$ | Calcule $\mathbb{P}(X_{(1)}>t)=\prod_{i=1}^n e^{-\theta t}=e^{-(n\theta)t}$ para identificar el parámetro escalado $\lambda_n=n\theta$ y media $1/(n\theta)$. |
| `D-C04-08` | Confundir FDA con supervivencia | skipped_step | high | $\mathbb{P}(X_{(1)}>t)=\prod_{i=1}^n (1-e^{-\theta t})$ | Note que $\{X_{(1)}>t\}=\bigcap_{i=1}^n\{X_i>t\}$: todas las observaciones deben superar $t$, usando $e^{-\theta t}$ antes de restar de $1$. |
| `D-C04-09` | Tasa estándar O(1/n) en varianza | conceptual_swap | high | $\operatorname{Var}(X_{(1)})=\frac{1}{n\theta^2}$ con tasa estándar $\mathcal{O}(1/n)$ | Aplique la fórmula de varianza exponencial $1/\lambda_n^2$ con $\lambda_n=n\theta$ para obtener $\operatorname{Var}(X_{(1)})=\frac{1}{n^2\theta^2}$ (tasa $\mathcal{O}(1/n^2)$). |
| `D-C04-10` | ECM igual a solo varianza | skipped_step | high | $\operatorname{ECM}(X_{(1)})=\frac{1}{n^2\theta^2}$ | Sume varianza y sesgo al cuadrado respecto a $c=0$: $\frac{1}{n^2\theta^2}+\left(\frac{1}{n\theta}\right)^2=\frac{2}{n^2\theta^2}$. |
| `D-C04-11` | Olvidar signo en integral de supervivencia | conceptual_swap | high | $\int_t^\infty \theta e^{-\theta x}\,dx = -e^{-\theta t}$ | Evalúe correctamente $[{-e^{-\theta x}}]_t^\infty = 0 - (-e^{-\theta t}) = e^{-\theta t} > 0$. |
| `D-C04-12` | Límite convergente a media poblacional | conceptual_swap | high | $X_{(1)}\xrightarrow{m.s.}\frac{1}{\theta}$ | Tome $\lim_{n\to\infty}\frac{1}{n\theta}=0$: el mínimo muestral se pega a la frontera inferior del soporte $c=0$. |
| `D-C04-13` | Omite convergencia del sesgo | conceptual_swap | high | $X_n \xrightarrow{m.s.} c$ equivale únicamente a $\operatorname{Var}(X_n) \to 0$ | Verifique tanto $\operatorname{Var}(X_n) \to 0$ como $E[X_n] \to c$: un estimador con varianza nula puede concentrarse en un valor sesgado distinto de $c$. |
| `D-C04-14` | Omite convergencia de varianza | conceptual_swap | high | Si $E[X_n] \to c$, entonces $X_n \xrightarrow{m.s.} c$ | Controle además que $\operatorname{Var}(X_n) \to 0$: por la descomposición del ECM, ambos términos no negativos deben anularse en el límite. |
| `D-C04-15` | Olvida elevar el error al cuadrado | conceptual_swap | high | $X_n \xrightarrow{m.s.} c \Leftrightarrow E[X_n - c] \to 0$ | Eleve al cuadrado la desviación $(X_n - c)^2$ dentro de la esperanza para evitar cancelación entre errores positivos y negativos. |
| `D-C04-16` | Invierte implicación hacia probabilidad | conceptual_swap | high | $X_n \xrightarrow{p} c \Rightarrow X_n \xrightarrow{m.s.} c$ siempre | Recuerde que la implicación va de media cuadrática a probabilidad (aplicando Markov a $(X_n - c)^2$); la recíproca puede fallar si hay colas pesadas. |
| `D-C04-17` | Exige sesgo nulo finito | conceptual_swap | high | Solo si $E[X_n] = c$ para todo $n$ hay convergencia en media cuadrática | Exija únicamente que el sesgo tienda a cero asintóticamente ($E[X_n] \to c$), no que sea cero en cada tamaño muestral finito. |
| `D-C04-18` | Aplica Markov sin cuadrar distancia | conceptual_swap | high | $P(|X_n - c| > \epsilon) \le \frac{E[(X_n - c)^2]}{\epsilon}$ | Divida $E[(X_n - c)^2]$ entre $\epsilon^2$, pues el evento $|X_n - c| > \epsilon$ equivale a $(X_n - c)^2 > \epsilon^2$ al aplicar Markov. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Momentos finitos de orden $r>0$ ($\mathbb{E}[|X_n|^r]<\infty$ y $\mathbb{E}[|X|^r]<\infty$) | Si el momento de orden $r$ es infinito, no puede evaluarse convergencia en espacio $L^r$. | - |
| `A-C04-02` | - | Muestra aleatoria simple $X_1,\dots,X_n \stackrel{iid}{\sim}\operatorname{Exp}(\theta)$ con $\theta>0$ fijo | Sin independencia la probabilidad conjunta $\mathbb{P}(\bigcap \{X_i>t\})$ no se factoriza como productoria. | - |
| `A-C04-03` | - | La sucesión $X_n$ tiene segundo momento finito $E[X_n^2] < \infty$ para todo $n$ | Si no existe varianza finita, no puede evaluarse el ECM ni la convergencia en media cuadrática. | - |

---

### [Hab-04] Demostración y Aplicación de la Desigualdad de Markov (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 14: Demostración y Aplicación de la Desigualdad de Markov
- **Prerequisites:** C-03
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 14), `EST3_LEC07_26.2_V2.pdf` (page 21)

#### Description & Cognitive Model
Demostración y aplicación de la desigualdad de Markov $\mathbb{P}(Y\ge\delta)\le\mathbb{E}[Y]/\delta$ para $Y\ge 0$ casi seguramente y $\delta>0$ mediante partición del espacio muestral y esperanza iterada, sin conocer la distribución completa.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Invertir el sentido de la cota | conceptual_swap | high | $\mathbb{P}(Y\ge\delta)\ge\frac{\mathbb{E}[Y]}{\delta}$ | Verifique que $\mathbb{E}[Y]\ge \delta\mathbb{P}(Y\ge\delta)$ implica al dividir entre $\delta>0$ que $\mathbb{P}(Y\ge\delta)\le\frac{\mathbb{E}[Y]}{\delta}$. |
| `D-Hab04-02` | Aplicar Markov sin no negatividad | skipped_step | high | La desigualdad de Markov vale para cualquier $Y\in\mathbb{R}$ aunque tome valores negativos | Exija $Y\ge 0$ casi seguramente para garantizar $\mathbb{E}[Y\mid Y<\delta]\ge 0$ y poder descartar $\mathbb{P}(Y<\delta)\mathbb{E}[Y\mid Y<\delta]$. |
| `D-Hab04-03` | Descartar sumando sin justificar signo | skipped_step | high | Suprime $\mathbb{P}(Y<\delta)\mathbb{E}[Y\mid Y<\delta]$ suponiendo que vale cero | Justifique la desigualdad $\mathbb{E}[Y]\ge\mathbb{P}(Y\ge\delta)\mathbb{E}[Y\mid Y\ge\delta]$ usando que $\mathbb{P}(Y<\delta)\mathbb{E}[Y\mid Y<\delta]\ge 0$. |
| `D-Hab04-04` | Cota errónea para esperanza condicional | skipped_step | high | $\mathbb{E}[Y\mid Y\ge\delta]\le\delta$ | Aplique monotonía de la esperanza sobre $\{Y\ge\delta\}$: si todo valor es al menos $\delta$, su promedio cumple $\mathbb{E}[Y\mid Y\ge\delta]\ge\delta$. |
| `D-Hab04-05` | Umbral delta <= 0 | conceptual_swap | high | Permite $\delta=0$ o $\delta<0$ al dividir $\mathbb{E}[Y]\ge\delta\mathbb{P}(Y\ge\delta)$ | Exija $\delta>0$ estricto para evitar división por cero o inversión del signo de la desigualdad. |
| `D-Hab04-06` | Confundir integral truncada con P(Y>=delta) | conceptual_swap | high | $\int_\delta^\infty y\,f_Y(y)\,dy = \mathbb{P}(Y\ge\delta)$ | Acote $y f_Y(y)\ge \delta f_Y(y)$ en $[\delta,\infty)$ y extraiga $\delta$ antes de identificar $\int_\delta^\infty f_Y(y)\,dy=\mathbb{P}(Y\ge\delta)$. |
| `D-Hab04-07` | Aplica sin no negatividad | conceptual_swap | high | Markov vale para cualquier $Y \in \mathbb{R}$ sin restricción de signo | Verifique siempre que $Y \ge 0$ casi seguramente; si $Y$ puede ser negativa, $E[Y]$ puede compensarse y anular la cota. |
| `D-Hab04-08` | Invierte razón esperanza-umbral | conceptual_swap | high | $P(Y \ge \delta) \le \frac{\delta}{E[Y]}$ | Divida la esperanza $E[Y]$ entre el umbral $\delta$, nunca al revés: al subir el umbral $\delta$, la cota de cola debe disminuir. |
| `D-Hab04-09` | Confunde cota con igualdad | conceptual_swap | high | $P(Y \ge \delta) = \frac{E[Y]}{\delta}$ exactamente | Interprete $\frac{E[Y]}{\delta}$ solo como un límite superior válido para toda distribución, no como el valor exacto de la probabilidad. |
| `D-Hab04-10` | Invierte sentido desigualdad | conceptual_swap | high | $P(Y \le \delta) \le \frac{E[Y]}{\delta}$ | Aplique Markov sobre la cola superior $Y \ge \delta$, pues solo los valores grandes consumen promedio en $E[Y] \ge \delta P(Y \ge \delta)$. |
| `D-Hab04-11` | Usa varianza en Markov | conceptual_swap | high | $P(Y \ge \delta) \le \frac{\operatorname{Var}(Y)}{\delta^2}$ | Distinga Markov (usa $E[Y]/\delta$ para $Y \ge 0$) de Chebyshev (usa $\operatorname{Var}(X)/\epsilon^2$ sobre desviaciones $|X-\mu|$). |
| `D-Hab04-12` | Omite positividad del umbral | conceptual_swap | high | La cota vale para todo $\delta \ge 0$ | Exija $\delta > 0$ estricto para dividir por el umbral al derivar $E[Y] \ge \delta P(Y \ge \delta)$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Variable aleatoria no negativa casi seguramente ($\mathbb{P}(Y\ge 0)=1$) con $\mathbb{E}[Y]<\infty$ y $\delta>0$ | Si $Y$ toma valores negativos con probabilidad positiva, el primer sumando puede ser negativo y rompe la cota. | - |
| `A-Hab04-02` | - | La variable aleatoria satisface $Y \ge 0$ con esperanza finita $E[Y] < \infty$ | Si $Y$ toma valores negativos o $E[Y]$ diverge, la cota pierde validez. | - |

---

### [C-05] Desigualdad de Jensen y Sesgo No Lineal (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 17: Desigualdad de Jensen y Sesgo No Lineal
- **Prerequisites:** PRE-01
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 17), `EST3_LEC07_26.2_V2.pdf` (page 25)

#### Description & Cognitive Model
Desigualdad de Jensen para funciones convexas ($\mathbb{E}[g(X)]\ge g(\mathbb{E}[X])$) y cóncavas ($\mathbb{E}[h(X)]\le h(\mathbb{E}[X])$) demostrada por recta tangente de soporte, explicando la no conmutatividad de $\mathbb{E}[\cdot]$ y el sesgo en $S_n=\sqrt{S_n^2}$ y $1/\bar{Y}_n$.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Conmuta esperanza | conceptual_swap | high | $\mathbb{E}[g(X)]=g(\mathbb{E}[X])$ | Restrinja la conmutatividad exclusivamente a transformaciones afines $g(x)=ax+b$: en funciones curvas la esperanza de la imagen difiere de la imagen de la media. |
| `D-C05-02` | Invierte caso convexo | conceptual_swap | high | $\mathbb{E}[g(X)]\le g(\mathbb{E}[X])$ | Verifique el signo de la curvatura: en funciones convexas ($g''\ge 0$) la curva queda sobre su tangente en $\mu$, por lo que $\mathbb{E}[g(X)]\ge g(\mathbb{E}[X])$. |
| `D-C05-03` | Sesgo positivo en Sn | conceptual_swap | high | $\mathbb{E}[\sqrt{S_n^2}]>\sigma$ | Identifique que $h(u)=\sqrt{u}$ es estrictamente cóncava ($h''(u)<0$), lo que invierte la desigualdad de Jensen y vuelve a $S_n$ sesgado hacia abajo. |
| `D-C05-04` | Sesgo negativo recíproco | conceptual_swap | high | $\mathbb{E}[1/\bar{Y}_n]<1/\mu$ | Calcule la segunda derivada de $g(x)=1/x$ para $x>0$: al ser $g''(x)=2/x^3>0$ convexa, Jensen implica $\mathbb{E}[1/\bar{Y}_n]>1/\mathbb{E}[\bar{Y}_n]=1/\mu$. |
| `D-C05-05` | Confunde plim con E | conceptual_swap | high | $\mathrm{plim}\,g(\hat{\theta}_n)\neq g(\mathrm{plim}\,\hat{\theta}_n)$ | Distinga muestras finitas de asintótica: $\mathbb{E}[\cdot]$ no conmuta con $g$ no lineal, pero $\mathrm{plim}$ sí atraviesa funciones continuas por Slutsky. |
| `D-C05-06` | Olvida soporte en I | conceptual_swap | high | $\mathbb{E}[h(X)]\le h(\mathbb{E}[X])\text{ sin }X\in I$ | Compruebe que el soporte de $X$ esté contenido en el intervalo $I$ donde $g$ es convexa o cóncava y que ambos momentos involucrados sean finitos. |
| `D-C05-07` | Conmuta esperanza con función no lineal | conceptual_swap | high | $E[g(X)] = g(E[X])$ para toda función continua $g$ | Reserve la igualdad $E[g(X)] = g(E[X])$ solo para funciones afines $g(x) = a + bx$; la curvatura introduce un sesgo dado por la dispersión. |
| `D-C05-08` | Invierte sentido en función convexa | conceptual_swap | high | Para $g$ convexa se cumple $E[g(X)] \le g(E[X])$ | Recuerde que una función convexa (en forma $\cup$) satisface $E[g(X)] \ge g(E[X])$, coherente con $\operatorname{Var}(X) = E[X^2] - (E[X])^2 \ge 0$. |
| `D-C05-09` | Asume insesgadez tras raíz cuadrada | conceptual_swap | high | Si $s^2$ es insesgado para $\sigma^2$, entonces $s = \sqrt{s^2}$ es insesgado para $\sigma$ | Aplique Jensen usando que $\sqrt{\cdot}$ es cóncava: $E[s] = E[\sqrt{s^2}] \le \sqrt{E[s^2]} = \sigma$, por lo que $s$ tiene sesgo negativo en general. |
| `D-C05-10` | Invierte sentido en función cóncava | conceptual_swap | high | Para $h$ cóncava se cumple $E[h(X)] \ge h(E[X])$ | Verifique la concavidad ($\cap$) de $h$: en funciones cóncavas la secante queda por debajo de la curva, produciendo $E[h(X)] \le h(E[X])$. |
| `D-C05-11` | Confunde Jensen con límite en probabilidad | conceptual_swap | high | Como $E[g(X)] \ge g(E[X])$, tampoco $\operatorname{plim} g(X_n)$ iguala a $g(\operatorname{plim} X_n)$ | Distinga el operador esperanza $E[\cdot]$ (afectado por la varianza en muestras finitas) del límite en probabilidad, que sí pasa por funciones continuas. |
| `D-C05-12` | Calcula diferencia sin varianza | conceptual_swap | high | Para $g(x)=x^2$ la brecha $E[g(X)] - g(E[X])$ vale $E[X]$ | Identifique que para $g(x)=x^2$ la diferencia exacta $E[X^2] - (E[X])^2$ es $\operatorname{Var}(X)$, reflejando cómo la dispersión amplifica la convexidad. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Integrabilidad $\mathbb{E}[|X|]<\infty$ y $\mathbb{E}[|g(X)|]<\infty$ sobre intervalo $I$ | Sin esperanza finita y soporte en $I$, la recta de soporte no garantiza la cota. | - |
| `A-C05-02` | - | Existen las esperanzas $E[X]$ y $E[g(X)]$, y la función $g$ es convexa o cóncava en el soporte de $X$ | Si $g$ cambia de curvatura o faltan momentos, la desigualdad global no se sostiene. | - |

---

### [C-06] Desigualdad de Cauchy-Schwarz y Correlación (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 18: Desigualdad de Cauchy-Schwarz y Correlación
- **Prerequisites:** PRE-01
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 18)

#### Description & Cognitive Model
Desigualdad de Cauchy-Schwarz $(\mathbb{E}[XY])^2\le\mathbb{E}[X^2]\mathbb{E}[Y^2]$ demostrada mediante el caso degenerado ($\mathbb{E}[X^2]=0$) y el discriminante no positivo $\Delta=b^2-4ac\le 0$ del polinomio $P(t)=\mathbb{E}[(tX+Y)^2]\ge 0$, acotando $|\mathrm{Cov}(X,Y)|\le\sigma_X\sigma_Y$ y $-1\le\rho_{XY}\le 1$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Olvida el cuadrado en EXY | conceptual_swap | high | $\mathbb{E}[XY]\le\mathbb{E}[X^2]\mathbb{E}[Y^2]$ | Respete las unidades cuadráticas: el producto de esperanzas cuadráticas acota a $(\mathbb{E}[XY])^2$, por lo que para $|\mathbb{E}[XY]|$ debe extraer raíz cuadrada. |
| `D-C06-02` | Discriminante positivo | conceptual_swap | high | $\Delta=b^2-4ac\ge 0$ | Recuerde la geometría de parábolas con $a>0$: para que $P(t)\ge 0$ en todo $\mathbb{R}$, no puede tener dos raíces reales distintas, lo cual exige $\Delta\le 0$. |
| `D-C06-03` | Omite valor absoluto | conceptual_swap | high | $\mathbb{E}[XY]\le\sqrt{\mathbb{E}[X^2]\mathbb{E}[Y^2]}\text{ sin valor absoluto}$ | Conserve el valor absoluto $|\mathbb{E}[XY]|=\sqrt{(\mathbb{E}[XY])^2}$ al tomar raíz cuadrada; así se obtiene también $-1\le\rho_{XY}\le 1$ para correlaciones negativas. |
| `D-C06-04` | Omite centrar en Cov | conceptual_swap | high | $|\mathrm{Cov}(X,Y)|\le\sqrt{\mathbb{E}[X^2]\mathbb{E}[Y^2]}$ | Centre las variables como $\tilde{X}=X-\mathbb{E}[X]$ e $\tilde{Y}=Y-\mathbb{E}[Y]$ antes de aplicar Cauchy-Schwarz para obtener las varianzas en la cota. |
| `D-C06-05` | Signo erróneo en igualdad | conceptual_swap | high | $Y=t^*X\text{ con }t^*>0\text{ cuando }(tX+Y)^2=0$ | Despeje correctamente la raíz de $t^*X+Y=0$: si $\mathbb{E}[(t^*X+Y)^2]=0$, entonces $t^*X+Y=0$ c.s., es decir, dependencia lineal perfecta $Y=-t^*X$. |
| `D-C06-06` | Confunde con independencia | conceptual_swap | high | $(\mathbb{E}[XY])^2=\mathbb{E}[X]^2\mathbb{E}[Y]^2$ | No confunda Cauchy-Schwarz con factorización bajo independencia: la cota siempre utiliza los segundos momentos no centrados $\mathbb{E}[X^2]$ y $\mathbb{E}[Y^2]$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Segundos momentos finitos $\mathbb{E}[X^2]<\infty$ y $\mathbb{E}[Y^2]<\infty$ en el mismo espacio | Sin segundos momentos finitos el producto interno en $L^2$ y el polinomio $P(t)$ no están definidos. | - |

---

### [C-07] Convergencia Casi Segura y Jerarquía de Modos de Convergencia (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 20: Jerarquía de Modos de Convergencia
- **Prerequisites:** PRE-01, C-05
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 20), `EST3_LEC07_26.2_V2.pdf` (page 33), `EST3_LEC07_26.2_V2.pdf` (page 37)

#### Description & Cognitive Model
Convergencia casi segura $X_n\xrightarrow{a.s.}c$ sobre trayectorias completas y jerarquía asintótica completa: $X_n\xrightarrow{r}X\Rightarrow X_n\xrightarrow{s}X$ ($0<s<r$), $X_n\xrightarrow{m.s.}X\Rightarrow X_n\xrightarrow{p}X\Rightarrow X_n\xrightarrow{d}X$, $X_n\xrightarrow{a.s.}X\Rightarrow X_n\xrightarrow{p}X$ y caso límite constante $X_n\xrightarrow{d}c\Rightarrow X_n\xrightarrow{p}c$.

#### Fused Distractor Models (18)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Invierte dirección s y r | conceptual_swap | high | $X_n\xrightarrow{s}X\Rightarrow X_n\xrightarrow{r}X\quad(0<s<r)$ | Recuerde que las normas de orden superior son más exigentes porque penalizan más las colas: la implicación va siempre de orden mayor $r$ a menor $s$. |
| `D-C07-02` | Usa exponente s/r en Jensen | conceptual_swap | high | $g(z)=z^{s/r}\text{ es convexa para }0<s<r$ | Revise el exponente en la prueba del inciso 1: como $0<s<r$, $r/s>1$ hace convexa a $g(z)=z^{r/s}$, mientras que $z^{s/r}$ es cóncava. |
| `D-C07-03` | Invierte p hacia L2 | conceptual_swap | high | $X_n\xrightarrow{p}X\Rightarrow X_n\xrightarrow{m.s.}X$ | Evite invertir la implicación del Teorema 5.1: la convergencia en media $r$-ésima garantiza convergencia en probabilidad, pero el recíproco es falso sin acotación uniforme. |
| `D-C07-04` | Omite r>=1 en Minkowski | conceptual_swap | high | $\|U\|_r=(\mathbb{E}[|U|^r])^{1/r}\text{ es norma para }0<r<1$ | Exija $r\ge 1$ al invocar la desigualdad de Minkowski en el inciso 3, pues para $0<r<1$ la funcional $\|\cdot\|_r$ no satisface la desigualdad triangular. |
| `D-C07-05` | Confunde momento sin módulo | conceptual_swap | high | $X_n\xrightarrow{r}X\text{ con }r=2\text{ solo da }\mathbb{E}[X_n]\to\mathbb{E}[X]$ | Utilice la desigualdad triangular inversa $||\!X_n\!|_r-|\!X\!|_r|\le|\!X_n-X\!|_r$ para concluir la convergencia del momento absoluto completo de orden $r$. |
| `D-C07-06` | Olvida E[|X|^r]<infinito | conceptual_swap | high | $\mathbb{E}[|X_n|^r]\to\mathbb{E}[|X|^r]\text{ aunque }X\notin L^r$ | Verifique la hipótesis $\mathbb{E}[|X|^r]<\infty$ antes de aplicar la desigualdad de Minkowski, ya que si $X\notin L^r$ la norma $\|X\|_r$ no está definida. |
| `D-C07-07` | Intercambia límite y probabilidad | conceptual_swap | high | $P(\lim_{n \to \infty} X_n = c) = 1$ es idéntico a $\lim_{n \to \infty} P(|X_n - c| > \epsilon) = 0$ | Distinga el alcance de cada modo: en probabilidad evalúa cada $n$ por separado; casi segura exige que toda la trayectoria quede en $c \pm \epsilon$ desde algún $n$. |
| `D-C07-08` | Exige convergencia determinista sin excepción | conceptual_swap | high | $X_n \xrightarrow{a.s.} c$ exige que $\lim_{n \to \infty} X_n(\omega) = c$ para todo resultado $\omega$ sin excepción | Permita eventos excepcionales de probabilidad cero: basta que el conjunto de trayectorias convergentes tenga probabilidad $1$. |
| `D-C07-09` | Invierte jerarquía con probabilidad | conceptual_swap | high | $X_n \xrightarrow{p} c \Rightarrow X_n \xrightarrow{a.s.} c$ siempre | Aplique la dirección correcta: la convergencia casi segura implica convergencia en probabilidad, pero la recíproca falla en sucesiones con picos raros recurrentes. |
| `D-C07-10` | Confunde N fijo con trayectoria | conceptual_swap | high | En convergencia casi segura existe un $N$ común que funciona para todas las realizaciones | Recuerde que el índice a partir del cual la trayectoria permanece en $c \pm \epsilon$ depende de la trayectoria aleatoria específica $\omega$. |
| `D-C07-11` | Asocia LFGN con convergencia débil | conceptual_swap | high | La Ley Fuerte de los Grandes Números garantiza únicamente convergencia en probabilidad | Asocie la LFGN con convergencia casi segura (trayectorias completas con probabilidad $1$), y la Ley Débil con convergencia en probabilidad. |
| `D-C07-12` | Exige probabilidad cero del límite | conceptual_swap | high | $X_n \xrightarrow{a.s.} c \Leftrightarrow P(\lim_{n \to \infty} X_n = c) = 0$ | Asigne probabilidad $1$ al evento $\lim_{n \to \infty} X_n = c$; lo que vale $0$ es la probabilidad del complemento donde la trayectoria no converge a $c$. |
| `D-C07-13` | Invierte flecha distribución a probabilidad | conceptual_swap | high | $X_n \xrightarrow{d} X \Rightarrow X_n \xrightarrow{p} X$ para cualquier límite $X$ | Recuerde que la convergencia en distribución es la más débil y no implica convergencia en probabilidad, salvo cuando el límite es una constante $c$. |
| `D-C07-14` | Ignora excepción de límite constante | conceptual_swap | high | Ni siquiera $X_n \xrightarrow{d} c$ (constante) implica $X_n \xrightarrow{p} c$ | Aplique el caso especial: si el límite es una constante $c$, toda la masa se concentra en un punto y sí se cumple $X_n \xrightarrow{p} c$. |
| `D-C07-15` | Ordena casi segura bajo media cuadrática | conceptual_swap | high | $X_n \xrightarrow{m.s.} X \Rightarrow X_n \xrightarrow{a.s.} X$ siempre | Separe ambas ramas fuertes: tanto $m.s.$ como $a.s.$ implican convergencia en probabilidad, pero ninguna de las dos implica en general a la otra. |
| `D-C07-16` | Coloca probabilidad sobre casi segura | conceptual_swap | high | $X_n \xrightarrow{p} X \Rightarrow X_n \xrightarrow{a.s.} X$ | Coloque la convergencia casi segura por encima de la convergencia en probabilidad en exigencia: $X_n \xrightarrow{a.s.} X \Rightarrow X_n \xrightarrow{p} X$. |
| `D-C07-17` | Desconecta media cuadrática de distribución | conceptual_swap | high | $X_n \xrightarrow{m.s.} X$ no implica $X_n \xrightarrow{d} X$ | Encadene las implicaciones transitivamente: $X_n \xrightarrow{m.s.} X \Rightarrow X_n \xrightarrow{p} X \Rightarrow X_n \xrightarrow{d} X$. |
| `D-C07-18` | Confunde condiciones de la tabla resumen | conceptual_swap | high | $F_{X_n}(x) \to F_X(x)$ corresponde a convergencia en probabilidad | Asocie $F_{X_n}(x) \to F_X(x)$ con convergencia en distribución; consistencia corresponde a $P(|X_n - c| > \epsilon) \to 0$. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Hipótesis de integrabilidad $\mathbb{E}[|X|^r]<\infty$ y $r\ge 1$ en el inciso 3 | Sin $X\in L^r$ y $r\ge 1$, la desigualdad de Minkowski no es válida para acotar momentos. | - |
| `A-C07-02` | - | Toda la sucesión $\{X_n\}_{n \ge 1}$ está definida sobre un mismo espacio de probabilidad $(\Omega, \mathcal{F}, P)$ | Sin un espacio conjunto para todas las $X_n$, no tiene sentido hablar de trayectorias. | - |
| `A-C07-03` | - | Para comparar $m.s.$, $a.s.$ y $p$ hacia $X$, las variables $X_n$ y $X$ comparten espacio de probabilidad | Sin espacio conjunto no puede definirse $X_n - X$ para evaluar distancia en probabilidad o $L^2$. | - |

---

### [Hab-06] Análisis de Contraejemplos entre Modos de Convergencia (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 22: Contraejemplo de Convergencia en Probabilidad sin L^r
- **Prerequisites:** C-07
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 22), `EST3_LEC07_26.2_V2.pdf` (page 38)

#### Description & Cognitive Model
Construcción y verificación analítica de contraejemplos entre modos de convergencia: sucesiones con valores atípicos explosivos $X_n\in\{0,n^2\}$ donde $X_n\xrightarrow{p}0$ sin convergencia $L^r$, y casos donde $X_n\xrightarrow{d}X$ pero $X_n\not\xrightarrow{p}X$ (e.g. $X_n=-Z$).

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Confunde soporte con prob | skipped_step | high | $\mathbb{P}(|X_n|>\varepsilon)=n^2\cdot\frac{1}{n}=n\to+\infty$ | Separe el cálculo de probabilidades del cálculo de esperanzas: $\mathrm{plim}$ solo mide la masa de probabilidad fuera de la banda $\varepsilon$, sin multiplicar por $n^2$. |
| `D-Hab06-02` | Calcula mal E[$Xn^2$] | skipped_step | high | $\mathbb{E}[X_n^2]=n^2\cdot\frac{1}{n}=n$ | Eleve al cuadrado cada elemento del soporte antes de ponderar por su probabilidad: $(n^2)^2\cdot(1/n)=n^4/n=n^3$. |
| `D-Hab06-03` | Confunde Var con E[$X^2$] | conceptual_swap | high | $\mathrm{Var}(X_n)=\mathbb{E}[X_n^2]=n^3$ | Aplique la identidad completa $\mathrm{Var}(X_n)=\mathbb{E}[X_n^2]-(\mathbb{E}[X_n])^2$: como $\mathbb{E}[X_n]=n$ no es cero, debe restar $n^2$. |
| `D-Hab06-04` | Asume evento para todo n | conceptual_swap | high | $\{|X_n|>\varepsilon\}=\{X_n=n^2\}\text{ incluso si }n^2\le\varepsilon$ | Fije $\varepsilon>0$ y elija $n$ suficientemente grande tal que $n^2>\varepsilon$: solo a partir de ese umbral el punto $n^2$ cae fuera de $(-\varepsilon,\varepsilon)$. |
| `D-Hab06-05` | Cree que plim implica E=0 | conceptual_swap | high | $X_n\xrightarrow{p}0\Rightarrow\lim_{n\to\infty}\mathbb{E}[X_n]=0$ | Calcule explícitamente $\mathbb{E}[X_n]=n\cdot(1/n)=1$ en la variante $X_n\in\{0,n\}$: un valor atípico cuya magnitud crece al ritmo $n$ impide que la esperanza converja a cero. |
| `D-Hab06-06` | Ignora masa en cero | conceptual_swap | high | $\mathbb{E}[X_n]=0\cdot\frac{1}{n}+n^2\left(1-\frac{1}{n}\right)$ | Asocie cada valor del soporte con su probabilidad exacta: el valor atípico $n^2$ ocurre con probabilidad rara $1/n$, mientras $0$ concentra masa $1-1/n$. |
| `D-Hab06-07` | Asigna distancia nula por igual ley | skipped_step | high | Como $X_n \sim N(0,1)$ y $Z \sim N(0,1)$, entonces $|X_n - Z| = 0$ | Evalúe la diferencia variable a variable: si $X_n = -Z$, entonces $|X_n - Z| = |-Z - Z| = 2|Z|$, que no es cero salvo cuando $Z = 0$. |
| `D-Hab06-08` | Omite factor dos al despejar | skipped_step | high | $P(|X_n - Z| > 1) = P(|Z| > 1) = 0.317$ | Factorice el coeficiente antes de despejar: $|X_n - Z| = 2|Z| > 1$ equivale a $|Z| > 0.5$, cuya probabilidad bajo $N(0,1)$ es $0.617$. |
| `D-Hab06-09` | Toma una sola cola normal | skipped_step | high | $P(|Z| > 0.5) = P(Z > 0.5) = 0.3085$ | Sume ambas colas simétricas para el valor absoluto: $P(|Z| > 0.5) = 2 \cdot P(Z > 0.5) \approx 0.617$. |
| `D-Hab06-10` | Niega convergencia en distribución de -Z | conceptual_swap | high | Como $X_n = -Z$ tiene signo opuesto, $X_n$ no converge en distribución a $Z$ | Use la simetría de $N(0,1)$: $-Z$ también sigue $N(0,1)$, por lo que $F_{X_n}(x) = F_Z(x)$ para todo $n$ y sí hay convergencia en distribución. |
| `D-Hab06-11` | Supone que el límite n anula 0.617 | conceptual_swap | high | Al crecer $n$, la constante $0.617$ tenderá a cero | Observe que $X_n = -Z$ no depende de $n$, por lo que $P(|X_n - Z| > 1) = 0.617$ permanece constante para todo $n$ y no converge a $0$. |
| `D-Hab06-12` | Suma signos opuestos como cero | conceptual_swap | high | $X_n - Z = -Z + Z = 0$ | Respete el signo de la resta en $|X_n - Z|$: al sustituir $X_n = -Z$ queda $|-Z - Z| = |-2Z| = 2|Z|$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Distribución de masa discreta con soporte $\{0,n^2\}$ y probabilidad $1/n$ en el extremo | Si el valor extremo no creciera al menos como $n$, los momentos podrían no diverger. | - |
| `A-Hab06-02` | - | La variable $Z \sim N(0,1)$ es simétrica respecto al origen de modo que $-Z \sim N(0,1)$ | Si la distribución de $Z$ fuera asimétrica, $-Z$ no tendría la misma distribución que $Z$. | - |

---

### [Hab-07] Insesgadez, Consistencia y Evaluación mediante ECM (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 24: Evaluación de Insesgadez y Consistencia en M_A, M_B, M_C
- **Prerequisites:** PRE-01, C-07
- **Evidence Citations:** `Clases_sintetizadas_semana_9.pdf` (page 24), `EST3_LEC07_26.2_V2.pdf` (page 30), `EST3_LEC07_26.2_V2.pdf` (page 31)

#### Description & Cognitive Model
Distinción entre insesgadez finita y consistencia asintótica (ninguna implica a la otra), análisis comparativo de $M_A, M_B, M_C$ y evaluación de consistencia mediante $\mathrm{ECM}=\mathrm{Var}+\mathrm{Sesgo}^2$ y tasas de caída ($1/n$ vs. $1/n^2$).

#### Fused Distractor Models (18)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Insesgado implica consistente | skipped_step | high | $M_A\text{ y }M_B\text{ son consistentes por ser insesgados}$ | Evalúe la varianza límite además del sesgo: $M_B$ concentra peso en las primeras observaciones mediante $a^{i-1}$, impidiendo que $\mathrm{Var}(M_B)$ colapse a cero. |
| `D-Hab07-02` | Olvida elevar coefs en Var | skipped_step | high | $\mathrm{Var}(M_B)=\left(\frac{1-a}{1-a^n}\right)\sigma_Y^2\sum_{i=1}^n a^{i-1}$ | Eleve al cuadrado cada coeficiente de la combinación lineal al calcular la varianza bajo independencia: $\mathrm{Var}(c_i Y_i)=c_i^2\sigma_Y^2$, generando razón $a^2$. |
| `D-Hab07-03` | Error serie geométrica r=$a^2$ | conceptual_swap | high | $\sum_{i=1}^n a^{2(i-1)}=\frac{1-a^{2n}}{1-a}$ | Identifique que la razón de la nueva serie geométrica es $r=a^2$; por tanto el denominador debe ser $1-r=1-a^2=(1-a)(1+a)$. |
| `D-Hab07-04` | Suma 1/n a la varianza | conceptual_swap | high | $\mathrm{Var}(M_C)=\frac{\sigma_Y^2}{n}+\frac{1}{n^2}$ | Recuerde que una constante determinística $1/n$ tiene varianza nula y no altera $\mathrm{Var}(\bar{Y}_n)$; el término $1/n^2$ entra en el $\mathrm{ECM}$ como $[\mathrm{Sesgo}(M_C)]^2$. |
| `D-Hab07-05` | Límite erróneo de $a^n$ | conceptual_swap | high | $\lim_{n\to\infty}a^n=1\quad\text{para }0<a<1$ | Aplique la propiedad exponencial para razones estrictamente menores que uno ($0<a<1$): conforme $n\to\infty$, $a^n\to 0$ y el factor $\frac{1+a^n}{1-a^n}$ tiende a $1$. |
| `D-Hab07-06` | Confunde sesgo con inconst. | conceptual_swap | high | $\mathrm{Sesgo}(M_C)=\frac{1}{n}\neq 0\Rightarrow M_C\text{ es inconsistente}$ | Distinga sesgo finito de consistencia asintótica: aunque $M_C$ es sesgado para $n$ finito, tanto $\mathrm{Sesgo}(M_C)=1/n$ como $\mathrm{Var}(M_C)=\sigma_Y^2/n$ tienden a cero. |
| `D-Hab07-07` | Suma sesgo sin elevar al cuadrado | skipped_step | high | $\operatorname{ECM} = \operatorname{Var} + \operatorname{Sesgo}$ | Eleve al cuadrado el sesgo antes de sumarlo a la varianza: $\operatorname{Sesgo} = 5/n$ aporta $(5/n)^2 = 25/n^2$ al error cuadrático medio. |
| `D-Hab07-08` | Confunde tasas de caída asintótica | skipped_step | high | El sesgo cuadrado cae más lento que la varianza ($1/n$ frente a $1/n^2$) | Compare los exponentes en $n$: cuando el sesgo es $O(1/n)$, su cuadrado cae a ritmo $1/n^2$, mucho más rápido que la varianza $1/n$. |
| `D-Hab07-09` | Descarta consistencia por sesgo finito | conceptual_swap | high | Si $\operatorname{Sesgo}(\hat{\mu}_n) = 5/n$ es distinto de cero, el estimador es inconsistente | Evalúe el límite cuando $n \to \infty$: tanto $\operatorname{Var} = 100/n \to 0$ como $\operatorname{Sesgo}^2 = 25/n^2 \to 0$, luego $\operatorname{ECM} \to 0$ y es consistente. |
| `D-Hab07-10` | Omite dividir varianza entre n | skipped_step | high | $\operatorname{Var}(\bar{Y}_n + 5/n) = \sigma^2 = 100$ para todo $n$ | Recuerde que sumar la constante $5/n$ no altera la varianza de $\bar{Y}_n$, la cual vale $\sigma^2/n = 100/n$ bajo muestreo i.i.d. |
| `D-Hab07-11` | Altera varianza al sumar constante | conceptual_swap | high | $\operatorname{Var}(\bar{Y}_n + 5/n) = \frac{100}{n} + \frac{25}{n^2}$ | Mantenga invariante la varianza al trasladar por una constante determinista $5/n$: esa constante solo entra en el término de sesgo. |
| `D-Hab07-12` | Multiplica varianza y sesgo cuadrado | conceptual_swap | high | $\operatorname{ECM} = \operatorname{Var} \cdot \operatorname{Sesgo}^2$ | Sume los componentes ortogonales $\operatorname{Var} + \operatorname{Sesgo}^2$; multiplicarlos subestimaría el ECM y anularía la varianza si el sesgo es cero. |
| `D-Hab07-13` | Asume que insesgadez implica consistencia | conceptual_swap | high | Todo estimador insesgado es automáticamente consistente | Verifique si la varianza decrece con $n$: $Y_1$ es insesgado para todo $n$, pero su varianza queda fija en $\sigma^2 = 100$ al ignorar los demás datos. |
| `D-Hab07-14` | Asume que consistencia implica insesgadez | conceptual_swap | high | Todo estimador consistente es insesgado en muestras finitas | Separe las propiedades: estimadores como $\bar{Y}_n + 5/n$, VI o MV son sesgados en muestra finita pero convergen al parámetro cuando $n \to \infty$. |
| `D-Hab07-15` | Reduce varianza de Y1 con n | conceptual_swap | high | Al crecer $n$, $\operatorname{Var}(Y_1) = \sigma^2/n \to 0$ | Note que $Y_1$ utiliza una sola observación independientemente de cuántas se recolecten, por lo que su varianza permanece constante en $\sigma^2$. |
| `D-Hab07-16` | Prioriza insesgadez en muestras grandes | conceptual_swap | high | En econometría asintótica siempre se descarta cualquier estimador sesgado aunque sea consistente | Priorice la consistencia en muestras grandes cuando no haya estimadores insesgados disponibles, pues el sesgo asintótico desaparece al crecer $n$. |
| `D-Hab07-17` | Confunde insesgadez con eficiencia | conceptual_swap | high | $\bar{Y}_n$ es consistente únicamente porque es insesgado | Atribuya la consistencia de $\bar{Y}_n$ a que cumple conjuntamente $E[\bar{Y}_n] = \mu$ y $\operatorname{Var}(\bar{Y}_n) = \sigma^2/n \to 0$. |
| `D-Hab07-18` | Niega existencia de ambos atributos | conceptual_swap | high | Un estimador no puede ser insesgado y consistente al mismo tiempo | Reconozca que insesgadez y consistencia son propiedades independientes: $\bar{Y}_n$ satisface ambas cuando la varianza poblacional es finita. |

#### Formal Mathematical Assumptions (3)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Muestra aleatoria i.i.d. $Y_i\sim\mathcal{N}(\mu_Y,\sigma_Y^2)$ con $0<\sigma_Y^2<\infty$ y $a\in(0,1)$ | La independencia anula covarianzas cruzadas en $\mathrm{Var}(M_B)$ y $a\in(0,1)$ asegura $a^n\to 0$. | - |
| `A-Hab07-02` | - | Las observaciones de la muestra son i.i.d. con varianza finita $\sigma^2 < \infty$ de modo que $\operatorname{Var}(\bar{Y}_n) = \sigma^2/n$ | Si hay correlación fuerte entre observaciones, la varianza puede no caer a tasa $1/n$. | - |
| `A-Hab07-03` | - | El parámetro $\theta$ es identificable y la familia de estimadores $\{\hat{\theta}_n\}_{n \ge 1}$ admite esperanza o límite en probabilidad | Sin una sucesión definida para todo $n$ no puede evaluarse consistencia frente a insesgadez. | - |

---

### [C-08] Espacio de Probabilidad, Variables Aleatorias y Momentos (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 13: Espacio de Probabilidad y Axiomas de Kolmogorov
- **Prerequisites:** None
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 13), `EST3_LEC07_26.2_V2.pdf` (page 14), `EST3_LEC07_26.2_V2.pdf` (page 15), `EST3_LEC07_26.2_V2.pdf` (page 17)

#### Description & Cognitive Model
Espacio de probabilidad $(\Omega,\mathcal{F},P)$, axiomas de Kolmogorov, regla de adición $P(A\cup B)=P(A)+P(B)-P(A\cap B)$, variable aleatoria $X:\Omega\to\mathbb{R}$, esperanza $E[X]$ y varianza $\mathrm{Var}(X)=E[X^2]-(E[X])^2$.

#### Fused Distractor Models (24)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Confunde espacio con muestra | conceptual_swap | high | $\Omega=\{y_1,\dots,y_n\}$ | Distinga el espacio muestral $\Omega$ de resultados posibles frente a la muestra observada. |
| `D-C08-02` | Probabilidad mayor a uno | conceptual_swap | high | $P(A)>1$ | Aplique el primer axioma de Kolmogorov: toda probabilidad cumple siempre $0\le P(A)\le 1$. |
| `D-C08-03` | Suma sin disyunción | conceptual_swap | high | $P(A\cup B)=P(A)+P(B)$ | Verifique si $A\cap B=\emptyset$; si hay intersección, reste $P(A\cap B)$ para no contar doble. |
| `D-C08-04` | Evento seguro menor a uno | conceptual_swap | high | $P(\Omega)<1$ | Recuerde el segundo axioma de Kolmogorov: la probabilidad del espacio muestral total es $P(\Omega)=1$. |
| `D-C08-05` | Probabilidad negativa | conceptual_swap | high | $P(A)<0$ | Verifique sus cálculos: por el axioma de no negatividad ninguna probabilidad puede ser negativa. |
| `D-C08-06` | Ignora la sigma-álgebra | conceptual_swap | high | $\mathcal{F}=\Omega$ | Diferencie $\Omega$ (resultados elementales) de $\mathcal{F}$ (colección de eventos medibles). |
| `D-C08-07` | Doble conteo en intersección | skipped_step | high | $P(A\cup B)=P(A)+P(B)$ | Identifique los elementos comunes en $A\cap B$ y reste $P(A\cap B)$ para evitar contarlos dos veces. |
| `D-C08-08` | Suma en vez de restar | conceptual_swap | high | $P(A\cup B)=P(A)+P(B)+P(A\cap B)$ | Reste $P(A\cap B)$ en lugar de sumarla, pues la intersección ya fue incluida en $P(A)$ y en $P(B)$. |
| `D-C08-09` | Multiplica probabilidades | conceptual_swap | high | $P(A\cup B)=P(A)P(B)$ | No confunda unión con producto de eventos independientes: use la regla aditiva con $P(A)+P(B)-P(A\cap B)$. |
| `D-C08-10` | Confunde unión e intersección | skipped_step | high | $P(A\cup B)=P(A\cap B)$ | Distinga $A\cup B$ (ocurre al menos uno) de $A\cap B$ (ocurren ambos eventos simultáneamente). |
| `D-C08-11` | Denominador muestral erróneo | conceptual_swap | high | $P(A)=\frac{|A|}{n_{\text{obs}}}$ | Divida siempre el número de resultados favorables entre la cardinalidad total $|\Omega|$ del espacio muestral. |
| `D-C08-12` | Complemento mal aplicado | conceptual_swap | high | $P(A\cup B)=1-P(A\cap B)$ | Use $1-P(A^c\cap B^c)$ si recurre al complemento, o bien la regla directa $P(A)+P(B)-P(A\cap B)$. |
| `D-C08-13` | Confunde variable y realización | conceptual_swap | high | $X=x$ | Distinga $X$ (regla aleatoria antes de observar) de su realización $x$ (número fijo tras observar). |
| `D-C08-14` | Asigna igual peso a valores | conceptual_swap | high | $P(X=x)=\frac{1}{|\mathrm{Ran}(X)|}$ | Traslade las probabilidades desde $\Omega$: sume los pesos de todos los $\omega$ tales que $X(\omega)=x$. |
| `D-C08-15` | Cree aleatoria la regla | conceptual_swap | high | $X(\omega)$ cambia sin cambiar $\omega$ | Recuerde que la regla $X(\omega)$ es fija; lo aleatorio es qué resultado elemental $\omega\in\Omega$ ocurre. |
| `D-C08-16` | Invierte dominio y rango | conceptual_swap | high | $X:\mathbb{R}\to\Omega$ | Verifique el sentido de la función: una variable aleatoria mapea cada resultado $\omega\in\Omega$ a $\mathbb{R}$. |
| `D-C08-17` | Omite preimagen múltiple | conceptual_swap | high | $P(X=x)=P(\omega_1)$ | Incluya todos los resultados de $\Omega$ que producen el mismo valor $x$ al sumar probabilidades. |
| `D-C08-18` | Confunde evento con valor | conceptual_swap | high | $X=\{CS,SC\}$ | Separe el evento $\{\omega:X(\omega)=x\}\subseteq\Omega$ del número real $x$ que toma la variable $X$. |
| `D-C08-19` | Promedio simple sin pesos | skipped_step | high | $E[X]=\frac{1}{k}\sum x_j$ | Pondere cada valor posible $x$ por su probabilidad $P(X=x)$ en vez de promediar valores sin pesos. |
| `D-C08-20` | Confunde E[$X^2$] con (E[X])^2 | skipped_step | high | $\mathrm{Var}(X)=0$ | Calcule $E[X^2]=\sum x^2 P(X=x)$ elevando cada $x$ antes de promediar; en general $E[X^2]\neq(E[X])^2$. |
| `D-C08-21` | Olvida elevar al cuadrado E[X] | conceptual_swap | high | $\mathrm{Var}(X)=E[X^2]-E[X]$ | Reste el cuadrado de la esperanza $(E[X])^2$ en la fórmula $\mathrm{Var}(X)=E[X^2]-(E[X])^2$. |
| `D-C08-22` | Suma probabilidades en vez de x | conceptual_swap | high | $E[X]=\sum P(X=x)$ | Multiplique cada valor numérico $x$ por su probabilidad $P(X=x)$ antes de sumar. |
| `D-C08-23` | Confunde varianza y desviación | conceptual_swap | high | $\sigma=\mathrm{Var}(X)$ | Extraiga la raíz cuadrada de $\mathrm{Var}(X)$ para obtener la desviación estándar $\sigma$ en unidades de $X$. |
| `D-C08-24` | Invierte signo en resta | conceptual_swap | high | $\mathrm{Var}(X)=(E[X])^2-E[X^2]$ | Reste $(E[X])^2$ a $E[X^2]$; por desigualdad de Jensen siempre se cumple $E[X^2]\ge (E[X])^2$. |

#### Formal Mathematical Assumptions (4)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Colección $\mathcal{F}$ cerrada bajo complementos y uniones numerables | Sin $\sigma$-álgebra no hay probabilidad bien definida. | - |
| `A-C08-02` | - | Resultados equiprobables en $\Omega$ finito | Si no son equiprobables no vale $|A|/|\Omega|$. | - |
| `A-C08-03` | - | Medibilidad $\{\omega:X(\omega)\le x\}\in\mathcal{F}$ para todo $x\in\mathbb{R}$ | Sin medibilidad no existe distribución de $X$. | - |
| `A-C08-04` | - | Existencia de momentos finitos $E[|X|]<\infty$ y $E[X^2]<\infty$ | Si $E[X^2]=\infty$, la varianza no está definida. | - |

---

### [C-20] Convergencia en Distribución (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 35: Convergencia en Distribución
- **Prerequisites:** C-03, C-08
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 35)

#### Description & Cognitive Model
Definición $X_n \xrightarrow{d} X \Leftrightarrow \lim_{n \to \infty} F_{X_n}(x) = F_X(x)$ en puntos de continuidad de $F_X$ y uso en aproximaciones normales de muestras grandes

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C20-01` | Exige igualdad de realizaciones | conceptual_swap | high | Si $X_n \xrightarrow{d} X$, entonces $X_n$ toma valores cercanos a $X$ para $n$ grande | Recuerde que la convergencia en distribución compara funciones de distribución acumulada (FDA), no los valores realizados de $X_n$ y $X$. |
| `D-C20-02` | Exige convergencia en discontinuidades | conceptual_swap | high | Debe cumplirse $F_{X_n}(x) \to F_X(x)$ en todo $x \in \mathbb{R}$ sin excluir discontinuidades | Excluya los puntos de discontinuidad de $F_X$: para una constante $0$, $F_0$ salta en $x=0$, y en todo $x \ne 0$ las FDA sí convergen. |
| `D-C20-03` | Confunde FDA con densidad puntual | conceptual_swap | high | $X_n \xrightarrow{d} X$ significa que $P(X_n = x) \to P(X = x)$ para todo $x$ | Compare las probabilidades acumuladas $P(X_n \le x) \to P(X \le x)$ en puntos de continuidad de $F_X$, no masas puntuales. |
| `D-C20-04` | Limita aproximación normal a datos normales | conceptual_swap | high | No puede usarse $N(0,1)$ como límite si los datos $Y_i$ son asimétricos como Exponencial(1) | Note que aunque $Y_i \sim \operatorname{Exp}(1)$ sea muy asimétrica, la media estandarizada $Z_n$ converge en distribución a $N(0,1)$ cuando $n$ crece. |
| `D-C20-05` | Asume igualdad exacta en n finito | conceptual_swap | high | Si $Z_n \xrightarrow{d} N(0,1)$, entonces $P(Z_n \le 1.645) = 0.950$ desde $n = 5$ | Use $0.950$ como aproximación asintótica para $n$ grande; en $n$ pequeño (p. ej. $n=5$, donde da $0.933$) existe error de aproximación. |
| `D-C20-06` | Descarta espacio conjunto innecesario | conceptual_swap | high | $X_n \xrightarrow{d} X$ requiere que $X_n$ y $X$ estén definidas sobre el mismo espacio muestral | Reconozca que al depender solo de las FDA marginales $F_{X_n}$ y $F_X$, la convergencia en distribución no exige espacio común. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C20-01` | - | La convergencia $\lim_{n \to \infty} F_{X_n}(x) = F_X(x)$ se evalúa en todo punto $x$ donde $F_X$ es continua | Exigirla en saltos de $F_X$ excluiría sucesiones deterministas convergentes como $1/n \to 0$. | - |

---

### [C-22] Ley de los Grandes Números (LGN) (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 40: Ley de los Grandes Números (LGN)
- **Prerequisites:** C-03, C-07, C-08
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 40)

#### Description & Cognitive Model
Establece que el promedio muestral $\bar{Y}_n$ de variables i.i.d. con media finita $\mu$ converge en probabilidad ($\bar{Y}_n \xrightarrow{p} \mu$, ley débil) y casi seguramente ($\bar{Y}_n \xrightarrow{a.s.} \mu$, ley fuerte) a la media poblacional, fundamentando la consistencia.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C22-01` | Exige normalidad | conceptual_swap | high | La LGN solo aplica si $Y_i \sim N(\mu,\sigma^2)$ | Recuerde que la LGN no requiere normalidad poblacional, solo variables i.i.d. con esperanza $E[Y_i]=\mu$ finita. |
| `D-C22-02` | Exige varianza finita | conceptual_swap | high | Sin $\sigma^2<\infty$ no se cumple la LGN | Distinga las hipótesis mínimas: Khinchine y Kolmogorov solo exigen media finita; $\sigma^2<\infty$ solo facilita probar convergencia en media cuadrática. |
| `D-C22-03` | Confunde LGN con TCL | conceptual_swap | high | $\bar{Y}_n \xrightarrow{p} N(\mu,\sigma^2/n)$ por LGN | Separe ambos teoremas: la LGN indica que $\bar{Y}_n$ converge a la constante $\mu$, mientras el TCL describe la distribución normal de los errores. |
| `D-C22-04` | Igualdad en muestra finita | conceptual_swap | high | Con $n$ grande se cumple $\bar{Y}_n = \mu$ exacto | Comprenda que la LGN garantiza convergencia asintótica cuando $n \to \infty$, por lo que en muestras finitas persiste un error $|\bar{y}_n-\mu|>0$. |
| `D-C22-05` | Fija ritmo del error | conceptual_swap | high | La LGN fija la tasa exacta y distribución del error | Recuerde que la LGN únicamente asegura que el error tiende a cero; la velocidad $1/\sqrt{n}$ y la forma normal corresponden al TCL. |
| `D-C22-06` | Aplica a observación única | conceptual_swap | high | $Y_i \xrightarrow{p} \mu$ para cada dato individual | Note que la compensación de errores individuales ocurre al promediar $n$ observaciones en $\bar{Y}_n$, no en una realización aislada $Y_i$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C22-01` | - | Observaciones $Y_1,\dots,Y_n$ i.i.d. con esperanza $E[Y_i]=\mu$ finita | Sin independencia o con media infinita, los errores no se compensan y $\bar{Y}_n$ puede no converger a $\mu$. | - |

---

### [C-23] Teorema Central del Límite (TCL) (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 42: Teorema Central del Límite (TCL)
- **Prerequisites:** C-22
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 42)

#### Description & Cognitive Model
Establece que para $Y_i$ i.i.d. con media $\mu$ y varianza $0<\sigma^2<\infty$, la media estandarizada $Z_n=\frac{\sqrt{n}(\bar{Y}_n-\mu)}{\sigma}$ converge en distribución a $N(0,1)$, implicando $\bar{Y}_n \overset{a}{\sim} N(\mu, \sigma^2/n)$ sin importar la distribución original.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C23-01` | Escala por n en vez de raíz | conceptual_swap | high | $Z_n = \frac{n(\bar{Y}_n-\mu)}{\sigma} \xrightarrow{d} N(0,1)$ | Verifique que el error $\bar{Y}_n-\mu$ se encoge a ritmo $1/\sqrt{n}$, por lo que debe multiplicar por $\sqrt{n}$ para obtener varianza límite unitaria. |
| `D-C23-02` | Varianza sin dividir por n | conceptual_swap | high | $\bar{Y}_n \overset{a}{\sim} N(\mu, \sigma^2)$ | Distinga la varianza de una observación $\sigma^2$ de la varianza del promedio muestral $\sigma^2/n$, la cual disminuye al crecer la muestra. |
| `D-C23-03` | Exige población normal | conceptual_swap | high | El TCL requiere que $Y_i$ sea aproximadamente normal | Recuerde que la potencia del TCL radica en que el promedio muestral tiende a la normalidad sin importar la asimetría o forma original de $Y_i$. |
| `D-C23-04` | Confunde convergencia d con p | conceptual_swap | high | $Z_n \xrightarrow{p} N(0,1)$ o a constante | Diferencie convergencia en distribución (forma de la función de distribución límite $N(0,1)$) de convergencia en probabilidad a una constante. |
| `D-C23-05` | Omite factor raíz de n | conceptual_swap | high | $(\bar{Y}_n-\mu)/\sigma \xrightarrow{d} N(0,1)$ | Note que sin el factor $\sqrt{n}$, la diferencia $\bar{Y}_n-\mu$ colapsa a la constante cero por la LGN en lugar de estabilizarse en $N(0,1)$. |
| `D-C23-06` | Permite varianza infinita | conceptual_swap | high | El TCL Lindeberg-Lévy vale con $\sigma^2=\infty$ | Verifique siempre las condiciones del TCL clásico: requiere variables i.i.d. con varianza finita y estrictamente positiva $0<\sigma^2<\infty$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C23-01` | - | Muestra i.i.d. con media $\mu$ y varianza finita no nula $0<\sigma^2<\infty$ | Si $\sigma^2$ es infinita o cero, la estandarización por $\sigma/\sqrt{n}$ no converge a $N(0,1)$. | - |

---

### [Hab-15] Inferencia Asintótica para Medias y Proporciones vía TCL (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 43: Cálculo de Probabilidades Asintóticas para Medias
- **Prerequisites:** C-23
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 43), `EST3_LEC07_26.2_V2.pdf` (page 44)

#### Description & Cognitive Model
Aplicación de la aproximación normal $\bar{Y}_n\overset{a}{\sim}N(\mu,\sigma^2/n)$ para probabilidades de cola, construcción del error estándar $ee(\hat{p})=\sqrt{\hat{p}(1-\hat{p})/n}$ e intervalo $IC_{95\%}=\hat{p}\pm 1.96\,ee(\hat{p})$ en proporciones, y cálculo de tamaño muestral ($4n$ para reducir margen a la mitad).

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab15-01` | Divide entre n sin raíz | skipped_step | high | $ee(\bar{Y}) = \sigma/n$ | Recuerde que la desviación estándar de $\bar{Y}$ es $\sigma/\sqrt{n}$, no $\sigma/n$; para $n=100$ y $\sigma=10$, el denominador es $10/10=1$. |
| `D-Hab15-02` | Usa sigma poblacional sin n | skipped_step | high | $Z = (\bar{Y}-\mu)/\sigma$ | No confunda la dispersión individual $\sigma$ con el error estándar de la media $\sigma/\sqrt{n}$: debe dividir $\sigma$ entre $\sqrt{n}$ al evaluar $\bar{Y}$. |
| `D-Hab15-03` | Coloca varianza en denominador | skipped_step | high | $Z = (\bar{Y}-\mu)/(\sigma^2/n)$ | Asegúrese de estandarizar dividiendo entre la desviación estándar $\sqrt{\sigma^2/n}=\sigma/\sqrt{n}$, nunca entre la varianza de la media. |
| `D-Hab15-04` | Invierte sentido de la cola | conceptual_swap | high | $P(\bar{Y}>12) \approx P(Z<2)$ | Verifique el signo de la desigualdad solicitada: para cola superior $P(Z>2)$ reste $1-\Phi(2)=0.023$ en vez de tomar $\Phi(2)$. |
| `D-Hab15-05` | Asume igualdad exacta | conceptual_swap | high | El TCL da probabilidad exacta finita | Considere que el TCL ofrece una aproximación asintótica; con $n=100$ en datos exponenciales persiste una leve diferencia frente al valor exacto $0.028$. |
| `D-Hab15-06` | Invierte resta en numerador | conceptual_swap | high | $Z = (\mu - a)/(\sigma/\sqrt{n})$ | Mantenga el signo correcto al estandarizar: reste la media poblacional $\mu$ al umbral $a$ ($a-\mu$) para preservar el sentido de la cola. |
| `D-Hab15-07` | Duplica n para mitad de margen | skipped_step | high | Para reducir el margen a la mitad basta $2n$ | Recuerde que el margen de error es proporcional a $1/\sqrt{n}$: para dividirlo entre $2$, debe multiplicar el tamaño muestral por $2^2=4$ ($n=1600$). |
| `D-Hab15-08` | Omite factor complemento 1-p | skipped_step | high | $ee(\hat{p}) = \sqrt{\hat{p}/n}$ | Use la varianza completa de una variable Bernoulli $\operatorname{Var}(Y_i)=p(1-p)$ al calcular el error estándar de la proporción muestral. |
| `D-Hab15-09` | Olvida raíz en error estándar | skipped_step | high | $ee(\hat{p}) = \hat{p}(1-\hat{p})/n$ | Note que $\hat{p}(1-\hat{p})/n$ es la varianza asintótica de $\hat{p}$; debe tomar su raíz cuadrada para obtener el error estándar del intervalo. |
| `D-Hab15-10` | Usa cuantil erróneo al 95% | conceptual_swap | high | $IC_{95\%}: \hat{p} \pm 1.645\,ee(\hat{p})$ | Verifique el cuantil normal bilateral para $95\%$ de confianza ($2.5\%$ en cada cola), el cual corresponde a $z_{0.975}=1.96$, no a $1.645$. |
| `D-Hab15-11` | Descarta mayoría con IC>0.5 | conceptual_swap | high | Si $0.50 \notin IC_{95\%}$ no hay mayoría | Interprete los límites del intervalo: como todo el $IC_{95\%}$ se ubica estrictamente por encima de $0.50$, los datos respaldan mayoría. |
| `D-Hab15-12` | Divide fuera de la raíz | conceptual_swap | high | $ee(\hat{p}) = \sqrt{\hat{p}(1-\hat{p})}/n$ | Incluya el tamaño muestral $n$ dentro de la raíz cuadrada (o divida entre $\sqrt{n}$), ya que la varianza de la media cae con $1/n$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab15-01` | - | Tamaño muestral $n$ suficientemente grande para mitigar la asimetría poblacional | Con $n$ pequeño en distribuciones muy asimétricas, la aproximación normal difiere de la distribución exacta. | - |
| `A-Hab15-02` | - | Observaciones $Y_i \sim \text{Bernoulli}(p)$ i.i.d. y $n$ grande para sustituir $p$ por $\hat{p}$ | Con muestras pequeñas o dependientes, la aproximación normal y el error estándar plug-in pierden validez. | - |

---

### [C-24] Teorema de la Aplicación Continua (CMT) y Teorema de Slutsky (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 46: Teorema de la Aplicación Continua (CMT)
- **Prerequisites:** C-22
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 46), `EST3_LEC07_26.2_V2.pdf` (page 48)

#### Description & Cognitive Model
Teorema de la Aplicación Continua (CMT: $X_n\xrightarrow{p}c\Rightarrow g(X_n)\xrightarrow{p}g(c)$ y análogo en $\xrightarrow{d}$) y Teorema de Slutsky para combinar $B_n\xrightarrow{d}B$ con $A_n\xrightarrow{p}a$ mediante suma, producto o cociente ($a\ne 0$), justificando sustituir parámetros por estimadores consistentes.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C24-01` | Igualdad en esperanza (Jensen) | conceptual_swap | high | $E[g(X_n)] = g(E[X_n])$ por CMT | Distinga $\operatorname{plim}$ de esperanza: por la desigualdad de Jensen $E[g(X)] \ne g(E[X])$ en general, pero el $\operatorname{plim}$ sí traspasa funciones continuas. |
| `D-C24-02` | Confunde sesgo finito con inconsistencia | conceptual_swap | high | Todo estimador sesgado es inconsistente | Recuerde que un estimador puede ser sesgado en muestras finitas (como $s$ o $1/\bar{Y}$) y aun así ser consistente por aplicación continua. |
| `D-C24-03` | Ignora continuidad en el límite | conceptual_swap | high | $\operatorname{plim}(1/\bar{Y}) = 1/\mu$ incluso si $\mu=0$ | Verifique siempre que $g$ sea continua en el punto límite $c$: si $\mu=0$, la función $1/x$ es discontinua en $0$ y el teorema no aplica. |
| `D-C24-04` | Limita a funciones lineales | conceptual_swap | high | El plim solo pasa por transformaciones lineales | Note que la continuidad basta para el CMT; al ser $g(x)=x^2$ continua, $t(n) \xrightarrow{d} N(0,1)$ implica $t(n)^2 \xrightarrow{d} \chi^2_1$. |
| `D-C24-05` | Excluye convergencia en distribución | conceptual_swap | high | El CMT solo vale para $\xrightarrow{p}$ | Recuerde que el teorema de la aplicación continua rige tanto para convergencia en probabilidad como para convergencia en distribución. |
| `D-C24-06` | Olvida transformar el límite | conceptual_swap | high | $g(X_n) \xrightarrow{p} c$ en vez de $g(c)$ | Aplique la función continua $g$ también sobre el límite del parámetro: si $s^2 \xrightarrow{p} \sigma^2$, entonces $\sqrt{s^2} \xrightarrow{p} \sqrt{\sigma^2}=\sigma$. |
| `D-C24-07` | Combina dos límites en distribución | conceptual_swap | high | Si $A_n \xrightarrow{d} A$ y $B_n \xrightarrow{d} B \Rightarrow A_n+B_n \xrightarrow{d} A+B$ | Verifique la condición clave de Slutsky: $A_n$ debe converger en probabilidad a una constante $a$; con dos límites solo en distribución no está garantizado. |
| `D-C24-08` | Permite divisor constante cero | conceptual_swap | high | $B_n/A_n \xrightarrow{d} B/a$ válido para $a=0$ | Exija siempre $a \ne 0$ antes de aplicar el cociente $B_n/A_n \xrightarrow{d} B/a$, pues dividir por un término que converge a cero produce indeterminación. |
| `D-C24-09` | Exige que Bn vaya a constante | conceptual_swap | high | Requiere $B_n \xrightarrow{p} b$ y $A_n \xrightarrow{p} a$ | Recuerde que Slutsky está diseñado precisamente para combinar una variable que converge en distribución ($B_n$) con un estimador consistente ($A_n \xrightarrow{p} a$). |
| `D-C24-10` | Omite escalamiento por a | conceptual_swap | high | $A_n B_n \xrightarrow{d} B$ independientemente de $a$ | Conserve la constante límite $a$ en la expresión asintótica: $A_n B_n$ converge en distribución a $aB$, modificando escala si $a \ne 1$. |
| `D-C24-11` | Afirma exactitud en muestra chica | conceptual_swap | high | Slutsky da distribución exacta con $\hat{\sigma}$ | Tenga presente que Slutsky es un resultado asintótico ($n \to \infty$); en muestras pequeñas reemplazar $\sigma$ por $s$ introduce dispersión adicional. |
| `D-C24-12` | Restringe solo a sumas | conceptual_swap | high | Slutsky no aplica a productos ni cocientes | Recuerde que Slutsky cubre sumas, productos y cocientes ($a \ne 0$), permitiendo sustituir parámetros desconocidos en errores estándar de denominadores. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C24-01` | - | La función $g$ es continua en el límite $c$ (o en el soporte de la variable límite $X$) | Si $g$ presenta discontinuidades donde se concentra el límite, $g(X_n)$ puede no converger a $g(c)$. | - |
| `A-C24-02` | - | La sucesión $A_n$ converge en probabilidad a una constante $a$ (con $a \ne 0$ en cocientes) | Si $A_n$ converge solo en distribución a una variable aleatoria, la distribución del producto o suma puede cambiar. | - |

---

### [Hab-17] Contraste de Hipótesis Asintótico con Varianza Desconocida (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 49: Contraste de Hipótesis Asintótico con Varianza Desconocida
- **Prerequisites:** C-24
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 49)

#### Description & Cognitive Model
Descompone el estadístico $t=\frac{\bar{Y}-\mu_0}{s/\sqrt{n}}=\frac{\sigma}{s}\cdot\frac{\bar{Y}-\mu_0}{\sigma/\sqrt{n}}$ aplicando CMT ($\sigma/s \xrightarrow{p} 1$), TCL bajo $H_0$ y Slutsky para contrastar hipótesis con cuantiles normales aun sin normalidad ni $\sigma$ conocido.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab17-01` | Divide s entre n sin raíz | skipped_step | high | $t = (\bar{y}-\mu_0)/(s/n)$ | Calcule el error estándar como $s/\sqrt{n}$: para $n=400$ y $s=4$, el denominador es $4/\sqrt{400}=4/20=0.2$, dando $t=1.5$. |
| `D-Hab17-02` | Exige normalidad para usar 1.96 | skipped_step | high | Sin datos normales no vale el cuantil $1.96$ | Combine TCL (normalidad asintótica de $\bar{Y}$) con CMT y Slutsky ($\sigma/s \xrightarrow{p} 1$) para justificar el uso de cuantiles $N(0,1)$ en muestras grandes. |
| `D-Hab17-03` | Omite desviación s | skipped_step | high | $t = (\bar{y}-\mu_0)\sqrt{n}$ | Estandarice siempre por el error estándar completo $s/\sqrt{n}$ para que el estadístico sea adimensional y converja a $N(0,1)$ bajo $H_0$. |
| `D-Hab17-04` | Invierte regla de rechazo | conceptual_swap | high | Se rechaza $H_0$ al $5\%$ si $|t|<1.96$ | Recuerde la regla bilateral al $5\%$: solo se rechaza $H_0$ cuando el estadístico cae en las colas extremas ($|t| \ge 1.96$), no cuando $|1.5|<1.96$. |
| `D-Hab17-05` | Compara t contra alfa | conceptual_swap | high | Se rechaza si $|t| > 0.05$ | No confunda el nivel de significancia $\alpha=0.05$ (una probabilidad) con el valor crítico de la distribución normal ($z_{0.975}=1.96$). |
| `D-Hab17-06` | Anula límite de sigma/s | conceptual_swap | high | $\sigma/s \xrightarrow{p} 0$ por consistencia | Aplique la aplicación continua correctamente: como $s \xrightarrow{p} \sigma > 0$, la razón $\sigma/s$ converge en probabilidad a $\sigma/\sigma=1$, no a $0$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab17-01` | - | Hipótesis nula $H_0: \mu=\mu_0$ cierta, estimador consistente $s \xrightarrow{p} \sigma > 0$ y $n$ grande | Si $H_0$ es falsa o $n$ es muy pequeño, el estadístico $t$ no se distribuye como $N(0,1)$. | - |

---

### [C-26] Método Delta: Estimación de Error Estándar e Intervalos (Skill)

- **Bloom Level:** Understand
- **Session:** Unidad 50: El Método Delta
- **Prerequisites:** C-23
- **Evidence Citations:** `EST3_LEC07_26.2_V2.pdf` (page 50), `EST3_LEC07_26.2_V2.pdf` (page 51)

#### Description & Cognitive Model
Método Delta mediante expansión de Taylor de primer orden: $\sqrt{n}(g(\hat{\theta})-g(\theta))\xrightarrow{d}N(0,[g'(\theta)]^2 V)$ cuando $g'(\theta)\ne 0$, y cálculo de error estándar aproximado $|g'(\hat{\theta})|\cdot ee(\hat{\theta})$ e $IC_{95\%}$ para transformaciones no lineales.

#### Fused Distractor Models (12)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C26-01` | Omite cuadrado en varianza | conceptual_swap | high | Varianza límite igual a $g'(\theta)V$ | Recuerde la propiedad de la varianza $\operatorname{Var}(cX)=c^2\operatorname{Var}(X)$: al multiplicar por $g'(\theta)$, la varianza asintótica escala por $[g'(\theta)]^2$. |
| `D-C26-02` | Aplica g al error estándar | conceptual_swap | high | $ee(g(\hat{\theta})) \approx g(ee(\hat{\theta}))$ | Aplique la expansión de Taylor de primer orden: la incertidumbre se multiplica por la pendiente local $|g'(\hat{\theta})|$, no se evalúa dentro de $g$. |
| `D-C26-03` | Omite valor absoluto en ee | conceptual_swap | high | $ee(g(\hat{\theta})) \approx g'(\hat{\theta})\cdot ee(\hat{\theta})$ | Incluya siempre el valor absoluto $|g'(\hat{\theta})|$ en el error estándar, pues la raíz cuadrada de $[g'(\hat{\theta})]^2 V$ es no negativa. |
| `D-C26-04` | Ignora condición g'(theta) no nulo | conceptual_swap | high | El método delta de orden 1 vale con $g'(\theta)=0$ | Verifique que $g'(\theta) \ne 0$: si la primera derivada se anula, el término lineal desaparece y se requiere una expansión de segundo orden. |
| `D-C26-05` | Atribuye eliminación de sesgo | conceptual_swap | high | El método delta vuelve insesgado a $g(\hat{\theta})$ | Distinga precisión asintótica de insesgadez: el método delta aproxima el error estándar y la normalidad asintótica, sin corregir sesgos finitos. |
| `D-C26-06` | Divide entre la derivada | conceptual_swap | high | $ee(g(\hat{\theta})) \approx ee(\hat{\theta})/|g'(\hat{\theta})|$ | Observe la aproximación $g(\hat{\theta})-g(\theta) \approx g'(\theta)(\hat{\theta}-\theta)$: la desviación se multiplica por $|g'(\hat{\theta})|$, nunca se divide. |
| `D-C26-07` | Aplica g directa al ee | skipped_step | high | $ee(1/\bar{Y}) = 1/ee(\bar{Y})$ | No transforme el error estándar con $g$: derive $g(m)=-1/m^2$, evalúe en $\bar{y}=2$ ($-0.25$) y multiplique $|-0.25|\times 0.1=0.025$. |
| `D-C26-08` | Error estándar negativo por signo | skipped_step | high | $ee(1/\bar{Y}) = -0.25 \times 0.1 = -0.025$ | Tome el valor absoluto de la derivada evaluada ($|-0.25|=0.25$) antes de multiplicar por $ee(\bar{Y})$, garantizando un error estándar positivo. |
| `D-C26-09` | Deriva mal la potencia inversa | skipped_step | high | La derivada de $1/m$ es $-1/m$ | Aplique la regla de la potencia a $m^{-1}$: su derivada es $-1\cdot m^{-2}=-1/m^2$, que evaluada en $\bar{y}=2$ da $-1/4=-0.25$. |
| `D-C26-10` | Omite cuantil 1.96 en el IC | conceptual_swap | high | $IC_{95\%}: g(\bar{y}) \pm ee(g(\bar{Y}))$ | Multiplique el error estándar del método delta por el cuantil normal $1.96$ ($0.5 \pm 1.96\times 0.025$) para lograr cobertura asintótica del $95\%$. |
| `D-C26-11` | Usa pendiente al cuadrado en ee | conceptual_swap | high | $ee(1/\bar{Y}) \approx [g'(\bar{y})]^2 \cdot ee(\bar{Y})$ | Note que $[g'(\bar{y})]^2$ multiplica a la varianza; para el error estándar (raíz cuadrada de la varianza) use $|g'(\bar{y})|$ sin elevar al cuadrado. |
| `D-C26-12` | Multiplica por g en vez de g' | conceptual_swap | high | $ee(1/\bar{Y}) \approx g(\bar{y}) \cdot ee(\bar{Y})$ | Use la derivada $g'(\bar{y})=-0.25$ en lugar de la función $g(\bar{y})=0.5$, ya que el método delta pondera el error por la tasa de cambio local. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C26-01` | - | Estimador $\hat{\theta}$ asintóticamente normal y función $g$ derivable con $g'(\theta) \ne 0$ | Si $g'(\theta)=0$ o $g$ no es diferenciable en $\theta$, la aproximación de Taylor de primer orden colapsa. | - |
| `A-C26-02` | - | Estimación $\bar{y} \ne 0$ y muestra grande para la linealización local de $g(\mu)=1/\mu$ | Cerca de $\bar{y}=0$, la fuerte curvatura de $1/\mu$ invalida la aproximación lineal del intervalo. | - |

---
