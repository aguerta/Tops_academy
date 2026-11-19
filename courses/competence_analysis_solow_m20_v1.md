# Cognitive Task Analysis (CTA): Solow M20 V1

- **Course ID:** `solow_m20_v1`
- **Macro-Competency:** Dominio y aplicación analítica integral de Solow M20 V1
- **Structure:** 22 total competencies (1 Facts, 11 Concepts, 10 Skills) with 96 fused distractors.

## Curriculum Overview

| ID | Name | Type | Bloom | Session | Prerequisites | Distractors |
|:---|:---|:---:|:---:|:---|:---|:---:|
| `C-01` | Función Intensiva y Retornos | Concept | Understand | Unidad 2: Función Intensiva y Retornos | - | 3 |
| `Hab-01` | Ecuación Fundamental de Solow | Skill | Apply | Unidad 2: Ecuación Fundamental de Solow | C-01 | 6 |
| `C-02` | Línea de Fase y Estabilidad | Concept | Analyze | Unidad 3: Línea de Fase y Estabilidad | Hab-01 | 3 |
| `C-03` | Estado Uniforme y Tecnología | Concept | Evaluate | Unidad 4: Estado Uniforme y Tecnología | C-02 | 3 |
| `Hab-02` | Solución Cobb-Douglas Bernoulli | Skill | Apply | Unidad 5: Solución Cobb-Douglas Bernoulli | Hab-01, C-02 | 6 |
| `C-04` | Acumulación Neoclásica | Concept | Understand | Unidad 3: Acumulación Neoclásica | C-01 | 3 |
| `Hab-03` | Ecuación Relación Capital-Trabajo | Skill | Apply | Unidad 6: Ecuación Relación Capital-Trabajo | C-04 | 6 |
| `C-05` | Estabilidad del Equilibrio | Concept | Analyze | Unidad 7: Estabilidad del Equilibrio | Hab-03 | 3 |
| `H-01` | Tecnología de Proporciones Fijas | Fact | Remember | Unidad 10: Tecnología de Proporciones Fijas | C-04 | 3 |
| `Hab-04` | Dinámica Harrod-Domar | Skill | Apply | Unidad 11: Dinámica Harrod-Domar | Hab-03, H-01 | 6 |
| `Hab-05` | Solución Explícita Cobb-Douglas | Skill | Apply | Unidad 13: Solución Explícita Cobb-Douglas | Hab-03, C-05 | 6 |
| `Hab-06` | Familia CES y Crecimiento Perpetuo | Skill | Analyze | Unidad 14: Familia CES y Crecimiento Perpetuo | Hab-03, C-05 | 6 |
| `C-06` | Precios Competitivos y Productividad Marginal | Concept | Understand | Unidad 16: Precios Competitivos y Productividad Marginal | C-04 | 3 |
| `C-07` | Precios de Factores y Arbitraje | Concept | Understand | Unidad 17: Precios de Factores y Arbitraje | C-06 | 3 |
| `C-08` | Isocuantas y Razón de Precios | Concept | Understand | Unidad 19: Isocuantas y Razón de Precios | C-07 | 3 |
| `Hab-07` | Precios en Proporciones Fijas | Skill | Apply | Unidad 20: Precios en Proporciones Fijas | C-08 | 6 |
| `Hab-08` | Salarios y Participación Factorial | Skill | Apply | Unidad 21: Salarios y Participación Factorial | C-07, C-08 | 6 |
| `Hab-09` | Cambio Tecnológico Neutral | Skill | Apply | Unidad 22: Cambio Tecnológico Neutral | C-07 | 6 |
| `C-09` | Oferta de Trabajo Elástica | Concept | Analyze | Unidad 24: Oferta de Trabajo Elástica | C-07, C-08 | 3 |
| `C-10` | Ahorro Variable e Impuesto a la Renta | Concept | Analyze | Unidad 26: Ahorro Variable e Impuesto a la Renta | C-07 | 3 |
| `C-11` | Población Endógena y Trampa | Concept | Evaluate | Unidad 28: Población Endógena y Trampa | C-10 | 3 |
| `Hab-10` | Salario Rígido y Trampa de Liquidez | Skill | Analyze | Unidad 29: Salario Rígido y Trampa de Liquidez | C-08, C-09 | 6 |

---

## Detailed Competency Specifications

### [C-01] Función Intensiva y Retornos (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 2: Función Intensiva y Retornos
- **Prerequisites:** None
- **Recommended Modalities:** concept_matching, adversarial_break, multiple_choice_7_options
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Transformación de la función homogénea lineal $Q=f(K,L)$ a forma intensiva $Q=L\phi(k)$ con $k=K/L$, $\phi'(k)>0$ y $\phi''(k)<0$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C01-01` | Proporción fija Domar | conceptual_swap | high | $Q=\rho K$ sin sustitución | Distinga el modelo de Solow, donde $K$ y $L$ se combinan en proporciones variables, del modelo de Domar de proporción fija. |
| `D-C01-02` | Retornos crecientes en k | conceptual_swap | high | $\phi''(k)>0$ | Recuerde que $f_{KK}<0$ implica $\phi''(k)=L f_{KK}<0$, por lo que el producto por trabajador crece a tasa decreciente. |
| `D-C01-03` | Omite factor L | conceptual_swap | high | $Q=\phi(k)$ | Aplique la homogeneidad lineal $f(K,L)=Lf(K/L,1)$ para conservar el factor de escala $L$ multiplicando a $\phi(k)$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C01-01` | - | Homogeneidad lineal $f(\lambda K, \lambda L) = \lambda f(K, L)$ con $K, L > 0$ | Sin retornos constantes a escala no puede reducirse $Q/L$ a una función exclusiva de $k=K/L$. | - |
| `A-C01-02` | - | Productividad marginal positiva $f_K>0$ y decreciente $f_{KK}<0$ | Si $f_{KK}\ge 0$, entonces $\phi''(k)\ge 0$ y la curva $s\phi(k)$ no sería cóncava. | - |

---

### [Hab-01] Ecuación Fundamental de Solow (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 2: Ecuación Fundamental de Solow
- **Prerequisites:** C-01
- **Recommended Modalities:** open_symbolic, proof_dag, fill_in_the_blank
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 2)

#### Description & Cognitive Model
Condensación dinámica de $\dot{K}=sL\phi(k)$ y $\dot{L}/L=\lambda$ mediante diferenciación de $K=kL$ para obtener $\dot{k}=s\phi(k)-\lambda k$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab01-01` | Omite regla producto | skipped_step | high | $\dot{K}=L\dot{k}$ | Aplique la regla del producto al diferenciar $K=kL$ respecto al tiempo: $\dot{K}=L\dot{k}+k\dot{L}$ antes de sustituir $\dot{L}=\lambda L$. |
| `D-Hab01-02` | Suma dilución laboral | skipped_step | high | $\dot{k}=s\phi(k)+\lambda k$ | Al igualar $L\dot{k}+k\lambda L=sL\phi(k)$, reste $k\lambda L$ de ambos lados para reflejar que el crecimiento laboral diluye el capital. |
| `D-Hab01-03` | No elimina factor L | conceptual_swap | high | $\dot{k}=sL\phi(k)-\lambda kL$ | Divida toda la igualdad $L\dot{k}+k\lambda L=sL\phi(k)$ entre $L>0$ para obtener una ecuación diferencial solo en $k$. |
| `D-Hab01-04` | Confunde ahorro en K | conceptual_swap | high | $\dot{k}=sk-\lambda k$ | Recuerde que la inversión bruta es una proporción $s$ del producto $Q=L\phi(k)$, no del stock de capital $K$. |
| `D-Hab01-05` | Omite parámetro s | conceptual_swap | high | $\dot{k}=\phi(k)-\lambda k$ | Incluya la propensión marginal al ahorro $s$ en $\dot{K}=sQ$, pues solo una fracción constante del producto se invierte. |
| `D-Hab01-06` | Aplica lambda al ahorro | conceptual_swap | high | $\dot{k}=s\lambda\phi(k)-k$ | Asocie $\lambda$ exclusivamente a la tasa de crecimiento de la mano de obra $\dot{L}/L=\lambda$ en el término de dilución $-\lambda k$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab01-01` | - | Propensión constante al ahorro $s$ tal que $\dot{K} = sQ$ | Si $s$ variara endógenamente con $k$ o $t$, la ecuación $\dot{k}=s\phi(k)-\lambda k$ dejaría de ser autónoma. | - |
| `A-Hab01-02` | - | Crecimiento exponencial de la fuerza laboral $\dot{L}/L = \lambda > 0$ | Si $\lambda$ no fuera constante, el término de dilución en $\dot{k}$ dependería explícitamente del tiempo. | - |

---

### [C-02] Línea de Fase y Estabilidad (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 3: Línea de Fase y Estabilidad
- **Prerequisites:** Hab-01
- **Recommended Modalities:** invariant_canvas, adversarial_break, concept_matching
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 3)

#### Description & Cognitive Model
Análisis cualitativo de $\dot{k}=s\phi(k)-\lambda k$ mediante las curvas $s\phi(k)$ y $\lambda k$, intersección en $\bar{k}>0$ y convergencia estable.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C02-01` | Invierte signo de dk/dt | conceptual_swap | high | $\dot{k}<0$ cuando $s\phi(k)>\lambda k$ | Evalúe la distancia vertical $\dot{k}=s\phi(k)-\lambda k$: cuando la curva $s\phi(k)$ supera al rayo $\lambda k$, $\dot{k}$ es positivo y $k$ aumenta. |
| `D-C02-02` | Equilibrio inestable | conceptual_swap | high | Pendiente positiva en $\bar{k}$ | Verifique que la línea de fase cruza el eje horizontal en $\bar{k}$ con pendiente negativa, garantizando convergencia desde cualquier $k(0)>0$. |
| `D-C02-03` | Curva no parte del origen | conceptual_swap | high | $s\phi(0)>0$ | Considere que el capital $K$ es indispensable: si $K=0$ entonces $k=0$ y $Q=0$, por lo que $s\phi(k)$ parte del origen. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C02-01` | - | El capital es indispensable: si $k=0$, entonces $\phi(0)=0$ y $s\phi(0)=0$ | Si $s\phi(0)>0$, la economía produciría sin capital y cambiaría la geometría cerca del origen. | - |
| `A-C02-02` | - | Existe un intervalo de $k>0$ donde $s\phi(k) > \lambda k$ y luego $s\phi(k) < \lambda k$ | Sin cruce entre $s\phi(k)$ y $\lambda k$ para $k>0$, no existiría una relación capital-trabajo de equilibrio $\bar{k}>0$. | - |

---

### [C-03] Estado Uniforme y Tecnología (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 4: Estado Uniforme y Tecnología
- **Prerequisites:** C-02
- **Recommended Modalities:** multiple_select, adversarial_break, concept_matching
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 4)

#### Description & Cognitive Model
Caracterización del estado uniforme con crecimiento común a tasa $\lambda$ para $K, L, Q$ e inversión, y desplazamiento ascendente por progreso $T(t)$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C03-01` | Confunde uniforme y estacionario | conceptual_swap | high | $\dot{K}=\dot{Q}=0$ en $\bar{k}$ | Distinga estado uniforme de estado estacionario: en $\bar{k}$, $k$ es constante pero $K, L, Q$ y la inversión neta crecen a tasa $\lambda$. |
| `D-C03-02` | Desplazamiento hacia abajo | conceptual_swap | high | $T(t)$ reduce $\bar{k}$ | Note que $Q=T(t)f(K,L)$ con $dT/dt>0$ desplaza la curva $s\phi(k)$ hacia arriba, generando intersecciones sucesivas más altas con $\lambda k$. |
| `D-C03-03` | Requiere balance Domar | conceptual_swap | high | Convergencia solo si $k(0)=\bar{k}$ | Recuerde que en Solow la economía alcanza el estado uniforme automáticamente desde cualquier $k(0)>0$, sin el filo de la navaja de Domar. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C03-01` | - | La relación capital-mano de obra permanece invariante en el nivel de equilibrio $\bar{k}$ | Si $k$ no hubiera convergido a $\bar{k}$, $K$ y $L$ crecerían a tasas distintas y no habría estado uniforme. | - |
| `A-C03-02` | - | Progreso tecnológico multiplicativo $Q=T(t)f(K,L)$ con $dT/dt > 0$ | Si $T(t)$ fuera constante, la curva $s\phi(k)$ permanecería fija y $\bar{k}$ no aumentaría secularmente. | - |

---

### [Hab-02] Solución Cobb-Douglas Bernoulli (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 5: Solución Cobb-Douglas Bernoulli
- **Prerequisites:** Hab-01, C-02
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `05_15_07_El_modelo_de_crecimiento_de_Solow.pdf` (page 5)

#### Description & Cognitive Model
Linealización de $\dot{k}+\lambda k=sk^\alpha$ mediante $z=k^{1-\alpha}$ para hallar la trayectoria temporal $k^{1-\alpha}(t)$ y su límite $(s/\lambda)^{1/(1-\alpha)}$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab02-01` | Cambio de variable erróneo | skipped_step | high | $z=k^\alpha$ | En la ecuación de Bernoulli $\dot{k}+\lambda k=sk^\alpha$ con $m=\alpha$, use $z=k^{1-m}=k^{1-\alpha}$ para eliminar la no linealidad. |
| `D-Hab02-02` | Omite factor 1-alpha | skipped_step | high | $\frac{dz}{dt}+\lambda z=s$ | Al derivar $z=k^{1-\alpha}$, aplique la regla de la cadena $\dot{z}=(1-\alpha)k^{-\alpha}\dot{k}$ para conservar el factor $(1-\alpha)$ en ambos términos. |
| `D-Hab02-03` | Exponente directo en límite | conceptual_swap | high | $k^*=(s/\lambda)^{1-\alpha}$ | Despeje $k$ desde $k^{1-\alpha}\to s/\lambda$ elevando ambos lados al exponente recíproco $1/(1-\alpha)$. |
| `D-Hab02-04` | Invierte razón en límite | conceptual_swap | high | $k^*=(\lambda/s)^{1/(1-\alpha)}$ | Verifique que en $\frac{dz}{dt}+(1-\alpha)\lambda z=(1-\alpha)s$ el término particular constante es $b/a=s/\lambda$, no $\lambda/s$. |
| `D-Hab02-05` | Signo positivo exponente t | conceptual_swap | high | $e^{+(1-\alpha)\lambda t}$ | Dado que $(1-\alpha)>0$ y $\lambda>0$, el factor homogéneo $e^{-(1-\alpha)\lambda t}$ tiene exponente negativo y tiende a cero cuando $t\to\infty$. |
| `D-Hab02-06` | Omite condición inicial | conceptual_swap | high | $k^{1-\alpha}(t)=\frac{s}{\lambda}$ | Incluya la desviación inicial $[k(0)^{1-\alpha}-s/\lambda]e^{-(1-\alpha)\lambda t}$ para describir la trayectoria completa antes de $t\to\infty$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab02-01` | - | Función Cobb-Douglas $Q=K^\alpha L^{1-\alpha}$ con elasticidad $\alpha\in(0,1)$ | Si $\alpha=1$, $(1-\alpha)=0$ y la sustitución de Bernoulli $z=k^{1-\alpha}$ colapsa. | - |
| `A-Hab02-02` | - | Parámetros positivos $(1-\alpha)>0$ y $\lambda>0$ en la trayectoria exponencial | Si $(1-\alpha)\lambda\le 0$, el término $e^{-(1-\alpha)\lambda t}$ no decae a cero cuando $t\to\infty$. | - |

---

### [C-04] Acumulación Neoclásica (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 3: Acumulación Neoclásica
- **Prerequisites:** C-01
- **Recommended Modalities:** concept_matching, adversarial_break, multiple_choice_7_options
- **Evidence Citations:** `solow1956.pdf` (page 3)

#### Description & Cognitive Model
Ecuación fundamental de acumulación de capital $\dot{K}=sF(K,L)$ bajo ahorro constante $s\in(0,1)$ y función de producción con rendimientos constantes a escala.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C04-01` | Ahorro sobre capital | conceptual_swap | high | $\dot{K}=sK$ | Aplique la propensión al ahorro $s$ sobre el flujo de producto neto $Y=F(K,L)$, no sobre el stock de capital $K$. |
| `D-C04-02` | Olvida tasa de ahorro | conceptual_swap | high | $\dot{K}=F(K,L)$ | Recuerde que solo una fracción constante $s\in(0,1)$ del producto neto se ahorra e invierte; el resto se consume. |
| `D-C04-03` | Rendimientos decrecientes globales | conceptual_swap | high | $F(\lambda K,\lambda L)<\lambda Y$ | El modelo excluye factores fijos no acumulables como la tierra para mantener rendimientos constantes a escala en $K$ y $L$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C04-01` | - | Homogeneidad de grado uno $F(\lambda K,\lambda L)=\lambda Y$ sin recurso fijo. | Sin rendimientos constantes a escala no existe forma per cápita. | - |
| `A-C04-02` | - | Pleno empleo perpetuo de capital y trabajo con $L(t)=L_0 e^{nt}$. | Si hay desempleo persistente, $\dot{K}=sF(K,L)$ deja de determinar la trayectoria. | - |

---

### [Hab-03] Ecuación Relación Capital-Trabajo (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 6: Ecuación Relación Capital-Trabajo
- **Prerequisites:** C-04
- **Recommended Modalities:** proof_dag, open_symbolic, fill_in_the_blank
- **Evidence Citations:** `solow1956.pdf` (page 6)

#### Description & Cognitive Model
Derivación de la ecuación diferencial de la relación capital-trabajo $\dot{r}=sF(r,1)-nr$ usando $r=K/L$ y homogeneidad de grado uno.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab03-01` | Omite dilución laboral | skipped_step | high | $\dot{r}=sF(r,1)$ | Al diferenciar $r=K/L$ respecto al tiempo aparece el término de dilución $-nr$ debido al crecimiento poblacional. |
| `D-Hab03-02` | Suma en vez de restar | skipped_step | high | $\dot{r}=sF(r,1)+nr$ | Como $L$ está en el denominador de $r=K/L$, su crecimiento $n$ reduce $r$, por lo que el término debe restar. |
| `D-Hab03-03` | No divide por L | skipped_step | high | $\dot{r}=sF(K,L)-nr$ | Use homogeneidad de grado uno para factorizar $L$ y expresar la producción por trabajador como $F(r,1)$. |
| `D-Hab03-04` | Dilución constante | conceptual_swap | high | $\dot{r}=sF(r,1)-n$ | La tasa relativa $\dot{r}/r=\dot{K}/K-n$ implica que al multiplicar ambos lados por $r$ el segundo término es $nr$. |
| `D-Hab03-05` | Invierte s y n | conceptual_swap | high | $\dot{r}=nF(r,1)-sr$ | El ahorro $s$ multiplica la producción por trabajador $F(r,1)$ y la tasa laboral $n$ multiplica al capital por trabajador $r$. |
| `D-Hab03-06` | Aplica s solo a r | conceptual_swap | high | $\dot{r}=sr-nr$ | La función de producción por trabajador $F(r,1)$ es cóncava y distinta de la identidad lineal $r$ en el modelo neoclásico. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab03-01` | - | Fuerza laboral crece exógenamente a tasa constante $L(t)=L_0 e^{nt}$. | Si $n$ varía o es endógeno, el término de dilución $-nr$ cambia. | - |

---

### [C-05] Estabilidad del Equilibrio (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 7: Estabilidad del Equilibrio
- **Prerequisites:** Hab-03
- **Recommended Modalities:** invariant_canvas, adversarial_break, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 7)

#### Description & Cognitive Model
Análisis cualitativo de estabilidad en $\dot{r}=sF(r,1)-nr$: convergencia a $r^*$ cuando $sF(r,1)$ cruza $nr$ desde arriba y multiplicidad o inexistencia.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C05-01` | Confunde estabilidad | conceptual_swap | high | Cruce desde abajo es estable | Un equilibrio es estable solo si $\dot{r}>0$ a la izquierda y $\dot{r}<0$ a la derecha, es decir, $sF(r,1)$ cruza $nr$ desde arriba. |
| `D-C05-02` | Estabilidad universal | conceptual_swap | high | Siempre existe $r^*$ único | La Figura III muestra que si $sF(r,1)$ permanece siempre arriba o abajo de $nr$, no existe equilibrio de crecimiento balanceado. |
| `D-C05-03` | Crecimiento nulo en r* | conceptual_swap | high | En $r^*$ el capital no crece | Cuando $\dot{r}=0$, la razón $K/L$ es constante, lo que significa que $K$, $L$ y $Y$ crecen todos a la tasa natural $n$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C05-01` | - | Capital inicial positivo $K_0>0$ cuando $F(0,1)=0$. | Si $K=0$ y no se produce sin capital, el sistema queda atrapado en $r=0$. | - |

---

### [H-01] Tecnología de Proporciones Fijas (Fact)

- **Bloom Level:** Remember
- **Session:** Unidad 10: Tecnología de Proporciones Fijas
- **Prerequisites:** C-04
- **Recommended Modalities:** multiple_choice_7_options, fill_in_the_blank, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 10)

#### Description & Cognitive Model
Función de producción Leontief o Harrod-Domar $Y=\min(K/a,L/b)$ donde $a$ es el coeficiente de aceleración del capital y $b$ el requisito laboral.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-H01-01` | Suma de factores | conceptual_swap | high | $Y=K/a+L/b$ | En proporciones fijas no hay sustitución: el primer cuello de botella limita el producto mediante el operador mínimo. |
| `D-H01-02` | Confunde coeficientes | conceptual_swap | high | $Y=\min(aK,bL)$ | Si se requieren $a$ unidades de capital y $b$ de trabajo por unidad de producto, el máximo producto es $\min(K/a,L/b)$. |
| `D-H01-03` | Tasa garantizada errónea | conceptual_swap | high | La tasa garantizada es $s/b$ | En el modelo Harrod-Domar de proporciones fijas, la tasa garantizada de crecimiento es $s/a$, usando el coeficiente de capital $a$. |

---

### [Hab-04] Dinámica Harrod-Domar (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 11: Dinámica Harrod-Domar
- **Prerequisites:** Hab-03, H-01
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 11)

#### Description & Cognitive Model
Resolución por tramos de $\dot{r}=s\min(r/a,1/b)-nr$ en el caso Harrod-Domar y determinación de redundancia de trabajo o exceso de capacidad.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab04-01` | Tramo único | skipped_step | high | $\dot{r}=(s/a-n)r$ para todo $r$ | Cuando $r\ge a/b$ el trabajo es el cuello de botella y la ecuación diferencial cambia a $\dot{r}=s/b-nr$. |
| `D-Hab04-02` | Invierte umbral | skipped_step | high | Cambio ocurre en $r=b/a$ | La igualdad $r/a=1/b$ define el punto de quiebre exacto en $r=a/b$, no en su recíproco $b/a$. |
| `D-Hab04-03` | Equilibrio sin redundancia | conceptual_swap | high | Si $n_3<s/a$ hay pleno empleo de $K$ | Cuando $r=s/(n_3 b)>a/b$, el capital excede lo requerido y solo se emplea la proporción $an_3/s$ del stock. |
| `D-Hab04-04` | Redundancia invertida | conceptual_swap | high | Si $n_1>s/a$ sobra capital | Si $n_1>s/a$, la razón $r$ cae hacia cero y el trabajo se vuelve el factor redundante con desempleo creciente. |
| `D-Hab04-05` | Solución exponencial errónea | conceptual_swap | high | $r=(r_0-s/(nb))e^{nt}$ | La ecuación $\dot{r}=s/b-nr$ tiene solución convergente con término homogéneo $e^{-nt}$ hacia el límite $s/(nb)$. |
| `D-Hab04-06` | Empleo bajo cuello de capital | conceptual_swap | high | Empleo efectivo es $aK/b$ | Cuando el capital limita la producción en $Y=K/a$, el empleo efectivo de trabajo es exactamente $bY=bK/a$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab04-01` | - | Proporciones estrictamente fijas sin sustitución entre capital y trabajo. | Cualquier desigualdad entre $n$ y $s/a$ genera desempleo creciente o exceso de capacidad. | - |

---

### [Hab-05] Solución Explícita Cobb-Douglas (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 13: Solución Explícita Cobb-Douglas
- **Prerequisites:** Hab-03, C-05
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 13)

#### Description & Cognitive Model
Integración directa de $\dot{K}=sK^a(L_0 e^{nt})^{1-a}$ y cálculo del equilibrio $r^*=(s/n)^{1/(1-a)}$ y coeficiente de capital $C=s/n$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab05-01` | Exponente sin invertir | skipped_step | high | $r^*=(s/n)^{1-a}$ | Al despejar $sr^a=nr$, se obtiene $r^{1-a}=s/n$, por lo que debe elevarse ambos miembros al recíproco $1/(1-a)$. |
| `D-Hab05-02` | Invierte s y n | skipped_step | high | $r^*=(n/s)^{1/(1-a)}$ | Un mayor ahorro $s$ aumenta el capital de equilibrio $r^*=(s/n)^{1/(1-a)}$, mientras una mayor tasa $n$ lo reduce. |
| `D-Hab05-03` | Ingreso per cápita erróneo | conceptual_swap | high | $(Y/L)^*=(s/n)^{1/(1-a)}$ | Como $Y/L=r^a$ en Cobb-Douglas, el ingreso per cápita de largo plazo es $(r^*)^a=(s/n)^{a/(1-a)}$. |
| `D-Hab05-04` | Coeficiente de capital erróneo | conceptual_swap | high | $C=n/s$ | En estado estacionario $n=s/C$, de modo que el coeficiente capital-producto $K/Y$ se ajusta endógenamente a $C=s/n$. |
| `D-Hab05-05` | Olvida condición inicial en K(t) | conceptual_swap | high | $K(t)=[(s/n)L_0^b e^{nbt}]^{1/b}$ | La integración exacta de Bernoulli incluye la constante de integración $K_0^b-(s/n)L_0^b$ que desaparece solo asintóticamente. |
| `D-Hab05-06` | Exponente a en lugar de b | conceptual_swap | high | $r^*=(s/n)^{1/a}$ | El exponente que surge de simplificar $r/r^a=r^{1-a}$ al igualar $sr^a=nr$ es $b=1-a$, nunca $a$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab05-01` | - | Participación del capital estrictamente acotada $0<a<1$. | Si $a\ge 1$, $sF(r,1)$ no cruza $nr$ desde arriba y no hay equilibrio estable. | - |

---

### [Hab-06] Familia CES y Crecimiento Perpetuo (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 14: Familia CES y Crecimiento Perpetuo
- **Prerequisites:** Hab-03, C-05
- **Recommended Modalities:** open_symbolic, adversarial_break, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 14)

#### Description & Cognitive Model
Análisis de $\dot{r}=s(a\sqrt{r}+1)^2-nr$ para $Y=(a\sqrt{K}+\sqrt{L})^2$: condición de equilibrio $sa^2<n$, valor $r^*=(1/(\sqrt{n/s}-a))^2$ y divergencia si $sa^2>n$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab06-01` | Condición de equilibrio invertida | skipped_step | high | Existe equilibrio si $sa^2>n$ | Si $sa^2>n$, la curva $s(a\sqrt{r}+1)^2$ siempre supera a $nr$ y $r$ crece indefinidamente sin equilibrio. |
| `D-Hab06-02` | Olvida elevar al cuadrado r* | skipped_step | high | $r^*=1/(\sqrt{n/s}-a)$ | Al resolver $\sqrt{s}(a\sqrt{r}+1)=\sqrt{nr}$ se obtiene $\sqrt{r^*}$, que debe elevarse al cuadrado para hallar $r^*$. |
| `D-Hab06-03` | Orden de resta en denominador | conceptual_swap | high | $r^*=(1/(a-\sqrt{n/s}))^2$ | Cuando $sa^2<n$ se cumple $\sqrt{n/s}>a$, por lo que la raíz positiva requiere $\sqrt{n/s}-a$ en el denominador. |
| `D-Hab06-04` | Altura inicial nula | conceptual_swap | high | $sF(0,1)=0$ | En esta familia es posible producir con un solo factor, por lo que la curva parte de altura $sF(0,1)=s>0$ en $r=0$. |
| `D-Hab06-05` | Ingreso límite erróneo | conceptual_swap | high | $(Y/L)^*=1/(1-a\sqrt{n/s})^2$ | Sustituyendo $r^*$ en $(a\sqrt{r}+1)^2$ resulta el ingreso límite por trabajador igual a $1/(1-a\sqrt{s/n})^2$. |
| `D-Hab06-06` | Factorización errónea | conceptual_swap | high | $A=a+\sqrt{n/s}$ y $B=a+\sqrt{n/s}$ | La diferencia de cuadrados $(a\sqrt{r}+1)^2-(n/s)r$ se factoriza con $A=a-\sqrt{n/s}$ y $B=a+\sqrt{n/s}$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab06-01` | - | Parámetro de elasticidad $0<p<1$ (aquí $p=1/2$) para rendimientos marginales decrecientes. | Si $p\ge 1$, las isocuantas pierden la convexidad estándar. | - |

---

### [C-06] Precios Competitivos y Productividad Marginal (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 16: Precios Competitivos y Productividad Marginal
- **Prerequisites:** C-04
- **Recommended Modalities:** concept_matching, adversarial_break, multiple_choice_7_options
- **Evidence Citations:** `solow1956.pdf` (page 16)

#### Description & Cognitive Model
Determinación de salario real $w/p=\partial F/\partial L$ y renta real del capital $q/p=\partial F/\partial K$ en competencia perfecta, dependientes solo de $r$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C06-01` | Dependencia de escala | conceptual_swap | high | $\partial F/\partial K$ depende de $K$ y $L$ por separado | Por rendimientos constantes a escala, las productividades marginales dependen únicamente de la razón capital-trabajo $r=K/L$. |
| `D-C06-02` | Nivel absoluto de precios | conceptual_swap | high | El modelo real determina $p(t)$ | En el sistema real no hay ecuación monetaria para el nivel absoluto de precios, por lo que $p(t)$ se toma como dado. |
| `D-C06-03` | Confunde salario nominal y real | conceptual_swap | high | $\partial F/\partial L=w$ | La productividad marginal física iguala al salario real $w/p$ y a la renta real $q/p$, no a los valores nominales $w$ y $q$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C06-01` | - | Competencia pura y ajuste instantáneo de precios de factores sin rigideces. | Bajo competencia monopolística o rigidez salarial falla la igualdad con productividad marginal. | - |

---

### [C-07] Precios de Factores y Arbitraje (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 17: Precios de Factores y Arbitraje
- **Prerequisites:** C-06
- **Recommended Modalities:** proof_dag, adversarial_break, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 17)

#### Description & Cognitive Model
Ecuaciones de productividad marginal $\frac{\partial F}{\partial L}=\frac{w}{p}$ y $\frac{\partial F}{\partial K}=\frac{q}{p}$ junto con la condición de arbitraje perfecto $i(t)=\frac{q(t)}{p(t)}+\frac{\dot{p}(t)}{p(t)}$ que iguala el rendimiento de capital y fondos prestables.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C07-01` | Iguala tasa nominal y renta real | conceptual_swap | high | $i(t)=\frac{q(t)}{p(t)}$ | Sume la ganancia o pérdida de capital $\dot{p}(t)/p(t)$ a la renta propia $q(t)/p(t)$ para igualar el retorno de mantener capital físico frente a bonos. |
| `D-C07-02` | Signo invertido en variación de precios | conceptual_swap | high | $i(t)=\frac{q(t)}{p(t)}-\frac{\dot{p}(t)}{p(t)}$ | Verifique que si el precio del bien cae ($\dot{p}<0$), la renta propia $q/p$ debe superar a la tasa monetaria $i$ para compensar la pérdida de valor. |
| `D-C07-03` | Confunde salario con alquiler de capital | conceptual_swap | high | $\frac{\partial F}{\partial L}=\frac{q}{p}$ | Asocie la derivada respecto al trabajo $\partial F/\partial L$ con el salario real $w/p$ y la derivada respecto al capital $\partial F/\partial K$ con el alquiler real $q/p$. |

#### Formal Mathematical Assumptions (2)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C07-01` | - | Competencia perfecta, previsión perfecta y ausencia de riesgo en la asignación de activos | Sin arbitraje perfecto ni previsión perfecta no se cumple la igualdad exacta entre $i$ y el retorno del capital. | - |
| `A-C07-02` | - | Rendimientos constantes a escala en $F(K,L)$ | Si no hay rendimientos constantes, las productividades marginales no dependen solo de $r=K/L$. | - |

---

### [C-08] Isocuantas y Razón de Precios (Concept)

- **Bloom Level:** Understand
- **Session:** Unidad 19: Isocuantas y Razón de Precios
- **Prerequisites:** C-07
- **Recommended Modalities:** invariant_canvas, adversarial_break, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 19)

#### Description & Cognitive Model
Bajo rendimientos constantes a escala, la pendiente de las isocuantas de $F(K,L)$ es constante a lo largo de cualquier rayo $K=rL$ y refleja la razón de precios factoriales $w/q$, convergiendo a un equilibrio único si $r \to r^*$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C08-01` | Invierte razón de precios | conceptual_swap | high | Pendiente igual a $\frac{q}{w}$ | Recuerde que en el plano con $K$ vertical y $L$ horizontal, la relación marginal de sustitución técnica $-dK/dL$ iguala $F_L/F_K = w/q$ en equilibrio competitivo. |
| `D-C08-02` | Razón variable sobre un rayo | conceptual_swap | high | $w/q$ cambia con la escala sobre $r$ fijo | Aplique la homogeneidad de grado uno de $F(K,L)$: las derivadas parciales son homogéneas de grado cero, por lo que $w/q$ depende únicamente del cociente $r=K/L$. |
| `D-C08-03` | Confunde inestabilidad con caída perpetua | conceptual_swap | high | Siempre se requiere $i(t)$ cayendo sin límite | Distinga la posición de Harrod del modelo neoclásico: cuando existe un equilibrio estable $r^*$, la caída requerida en $w/p$ o $q/p$ es acotada y finita. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C08-01` | - | Isocuantas suaves con convexidad normal y rendimientos constantes a escala | Sin convexidad normal, un aumento de $r$ no garantiza un aumento monótono de $w/q$. | - |

---

### [Hab-07] Precios en Proporciones Fijas (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 20: Precios en Proporciones Fijas
- **Prerequisites:** C-08
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 20)

#### Description & Cognitive Model
Determinar los precios reales de los factores $w$ y $q$ en el caso límite de Harrod-Domar con isocuantas en ángulo recto según la posición de la razón observada $r=K/L$ respecto al cociente técnico $a/b$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab07-01` | Invierte factor redundante con r grande | skipped_step | high | $r > a/b \Rightarrow w=0, q=p/a$ | Compare el capital disponible por trabajador $r$ con el requerido $a/b$: si $r > a/b$ sobra capital, por lo que su productividad marginal es cero ($q=0$) y $w=p/b$. |
| `D-Hab07-02` | Invierte factor redundante con r pequeño | skipped_step | high | $r < a/b \Rightarrow q=0, w=p/b$ | Cuando $r < a/b$ hay escasez de capital y exceso de mano de obra: el trabajo es redundante ($w=0$) y todo el valor del producto se imputa al capital ($q=p/a$). |
| `D-Hab07-03` | Determinación única en el vértice | conceptual_swap | high | $r = a/b \Rightarrow w=p/b, q=p/a$ | En el vértice exacto $r=a/b$ ambos factores son escasos y no es posible imputar fracciones separadas: $w$ y $q$ son indeterminados sujetos solo a $aq+bw=p$. |
| `D-Hab07-04` | Suma directa sin coeficientes | conceptual_swap | high | $w + q = p$ en $r = a/b$ | Pondere cada precio factorial por su requerimiento unitario de insumo ($a$ unidades de capital y $b$ de trabajo) para obtener $aq+bw=p$. |
| `D-Hab07-05` | Multiplica en lugar de dividir | conceptual_swap | high | $r > a/b \Rightarrow w = bp$ | Como una unidad de producto requiere $b$ unidades de trabajo y $q=0$, el costo unitario $bw$ debe igualar $p$, de donde $w=p/b$. |
| `D-Hab07-06` | Confunde razón técnica con inversa | conceptual_swap | high | Compara $r$ contra $b/a$ | Verifique las unidades de $r=K/L$: si se requieren $a$ unidades de $K$ y $b$ de $L$ por unidad de producto, la proporción balanceada de capital a trabajo es $a/b$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab07-01` | - | Función de producción de coeficientes fijos $Y=\min(K/a, L/b)$ | Si existe sustituibilidad entre factores, las derivadas marginales no saltan discontinuamente en $a/b$. | - |

---

### [Hab-08] Salarios y Participación Factorial (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 21: Salarios y Participación Factorial
- **Prerequisites:** C-07, C-08
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 21)

#### Description & Cognitive Model
Calcular el salario real de equilibrio y la participación relativa del trabajo $(w/p)(L/Y)$ tanto en el caso Cobb-Douglas $Y=K^a L^{1-a}$ como en la función $Y=(a\sqrt{K}+\sqrt{L})^2$ en función de $s$ y $n$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab08-01` | Participación variable en Cobb-Douglas | skipped_step | high | $\frac{wL}{pY}$ depende de $s$ y $n$ en Cobb-Douglas | En Cobb-Douglas $w/p=(1-a)r^a$ y $Y/L=r^a$, por lo que $r$ se cancela en el cociente $(w/p)/(Y/L)=1-a$, manteniendo la participación constante. |
| `D-Hab08-02` | Error de signo en participación cuadrática | skipped_step | high | $\frac{wL}{pY} = 1 + a\sqrt{s/n}$ | Divida $w/p = \frac{1}{1-a\sqrt{s/n}}$ entre $Y/L = \frac{1}{(1-a\sqrt{s/n})^2}$ para obtener $1 - a\sqrt{s/n}$, que siempre es menor que la unidad. |
| `D-Hab08-03` | Invierte razón s/n en participación | conceptual_swap | high | $\frac{wL}{pY} = 1 - a\sqrt{n/s}$ | Recuerde que en $Y=(a\sqrt{K}+\sqrt{L})^2$ el equilibrio exige $\sqrt{r^*}=\frac{1}{\sqrt{n/s}-a}$, lo que al simplificar deja $\sqrt{s/n}$ en la participación. |
| `D-Hab08-04` | Exponente erróneo en salario Cobb-Douglas | conceptual_swap | high | $w/p = (1-a)(s/n)^{\frac{1}{1-a}}$ | Sustituya $r^*=(s/n)^{\frac{1}{1-a}}$ dentro de $w/p=(1-a)r^a$, obteniendo el exponente compuesto $a/(1-a)$ para el salario real. |
| `D-Hab08-05` | Dirección errónea ante mayor n | conceptual_swap | high | Mayor $n$ reduce la participación laboral en $Y=(a\sqrt{K}+\sqrt{L})^2$ | Observe que aunque mayor $n$ reduce el salario real $w/p$, el término $a\sqrt{s/n}$ disminuye y eleva la participación agregada $1-a\sqrt{s/n}$. |
| `D-Hab08-06` | Omite constante 1 en derivada | conceptual_swap | high | $\frac{\partial Y}{\partial L} = a\sqrt{r}$ en $Y=(a\sqrt{K}+\sqrt{L})^2$ | Aplique la regla de la cadena: $2(a\sqrt{K}+\sqrt{L})\frac{1}{2\sqrt{L}} = a\sqrt{K/L} + 1 = a\sqrt{r} + 1$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab08-01` | - | Existencia de equilibrio estacionario con $\sqrt{n/s} > a$ en $Y=(a\sqrt{K}+\sqrt{L})^2$ | Si $\sqrt{n/s} \le a$, no existe razón capital-trabajo estacionaria finita $r^*$. | - |

---

### [Hab-09] Cambio Tecnológico Neutral (Skill)

- **Bloom Level:** Apply
- **Session:** Unidad 22: Cambio Tecnológico Neutral
- **Prerequisites:** C-07
- **Recommended Modalities:** open_symbolic, fill_in_the_blank, unstructured_model
- **Evidence Citations:** `solow1956.pdf` (page 22)

#### Description & Cognitive Model
Resolver el crecimiento asintótico del capital, producto, razón capital-trabajo y coeficiente capital-producto cuando se introduce cambio tecnológico neutral multiplicativo $Y=e^{gt}K^a(L_0 e^{nt})^{1-a}$ con $b=1-a$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab09-01` | Tasa de crecimiento del capital sin factor 1/b | skipped_step | high | $\frac{\dot{K}}{K} \to n + g$ | Integre $\dot{K}=sK^a L_0^{1-a}e^{(nb+g)t}$ para ver que el exponente temporal $(nb+g)$ se divide por $b=1-a$, dando la tasa asintótica $n+g/b$. |
| `D-Hab09-02` | Tasa errónea del producto | skipped_step | high | $\frac{\dot{Y}}{Y} \to n + g/b$ | Evalúe $Y=e^{gt}K^a L^{1-a}$: la tasa de $Y$ suma $g + a(n+g/b) + (1-a)n$, lo que simplifica a $n + ag/b$ (menor que $n+g/b$). |
| `D-Hab09-03` | Estabilidad de K/L con progreso g>0 | conceptual_swap | high | $K/L$ converge a un valor constante $r^*$ | Con $A(t)=e^{gt}$ la función $sF(r,1)$ se expande continuamente, por lo que $K/L$ crece sin límite a la tasa asintótica $(n+g/b)-n = g/b$. |
| `D-Hab09-04` | Coeficiente capital-producto constante | conceptual_swap | high | $K/Y$ permanece constante en el largo plazo | Reste las tasas asintóticas de $K$ y de $Y$: $(n+g/b)-(n+ag/b) = (1-a)g/b = g > 0$, por lo que $K/Y$ crece a tasa $g$. |
| `D-Hab09-05` | Participación laboral creciente | conceptual_swap | high | La participación laboral sube con $K/L$ | Aunque el salario real $w/p$ sube continuamente al crecer $K/L$, en la función Cobb-Douglas la participación del trabajo permanece fija en $1-a$. |
| `D-Hab09-06` | Confunde b con a en denominador | conceptual_swap | high | $K/L$ crece a tasa $g/a$ | Recuerde que la ecuación diferencial se linealiza en $K^{1-a}=K^b$, por lo que la constante divisora del exponente temporal es siempre $b=1-a$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab09-01` | - | Cambio tecnológico neutral de Hicks $Y=e^{gt}F(K,L)$ con $F$ Cobb-Douglas y $a\in(0,1)$ | Con progreso puramente aumentador de trabajo o elasticidad distinta de 1, $K/Y$ puede estabilizarse. | - |

---

### [C-09] Oferta de Trabajo Elástica (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 24: Oferta de Trabajo Elástica
- **Prerequisites:** C-07, C-08
- **Recommended Modalities:** proof_dag, adversarial_break, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 24)

#### Description & Cognitive Model
Generalización de la oferta laboral a $L=L_0 e^{nt}(w/p)^h$ y al caso general $L=G(t,w/p)$, mostrando cuándo la elasticidad salarial $h$ deja inalterado el equilibrio $r^*$ o modifica la condición $\dot{r}=0$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C09-01` | Supone cambio de equilibrio con oferta h | conceptual_swap | high | $r^*$ depende de $h$ en $L=L_0 e^{nt}(w/p)^h$ | Observe en $\dot{r}=(sF(r,1)-nr)(1+ah/r)^{-1}$ que el factor $(1+ah/r)^{-1}$ es positivo, por lo que $\dot{r}=0$ ocurre exactamente en el mismo $r^*$ que con $h=0$. |
| `D-C09-02` | Omite efecto general de G | conceptual_swap | high | $r^*$ nunca cambia con oferta laboral elástica | En el caso general $\dot{r}=0$ exige $sF(r,1)=\frac{r}{G}\frac{\partial G}{\partial t}$; solo si $\frac{1}{G}\frac{\partial G}{\partial t}=n$ se preserva el $r^*$ original. |
| `D-C09-03` | Tasa de crecimiento distinta de n | conceptual_swap | high | $K$ e $Y$ crecen más rápido que $n$ en equilibrio | Cuando $r$ converge al equilibrio $r^*$, el salario real $w/p$ se estabiliza ($\dot{w}=0$), por lo que $L$, $K$ e $Y$ terminan creciendo a la misma tasa $n$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C09-01` | - | Nivel de precios constante $p$ y función de producción Cobb-Douglas para la forma explícita $(6a)$ | Si $p$ varía o $F$ no es Cobb-Douglas, la eliminación de $\dot{w}/w$ no toma la forma simple $(1+ah/r)^{-1}$. | - |

---

### [C-10] Ahorro Variable e Impuesto a la Renta (Concept)

- **Bloom Level:** Analyze
- **Session:** Unidad 26: Ahorro Variable e Impuesto a la Renta
- **Prerequisites:** C-07
- **Recommended Modalities:** invariant_canvas, multiple_select, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 26)

#### Description & Cognitive Model
Extensión del modelo con tasa de ahorro $s(r)$ decreciente en la razón capital-trabajo y con impuesto proporcional a la renta $t$ cuya fracción invertida $v$ transforma la tasa de ahorro efectiva en $s+(v-s)t$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C10-01` | Impuesto siempre reduce ahorro | conceptual_swap | high | Tasa efectiva igual a $s(1-t)$ siempre | Considere el uso fiscal de la recaudación: si el Estado invierte una fracción $v$ de los ingresos $tY$, el ahorro total es $s(1-t)Y+vtY = (s+(v-s)t)Y$. |
| `D-C10-02` | Estado estacionario clásico sin capital | conceptual_swap | high | $s(r)=0$ detiene el crecimiento de $L$ | Si $r$ sube tanto que anula el ahorro neto, la acumulación de $K$ se detiene, pero el crecimiento continuo de $L$ a tasa $n$ reduce $r$ y reactiva la inversión. |
| `D-C10-03` | Ahorro creciente con capital-trabajo | conceptual_swap | high | $s(r)$ es creciente en $r$ | Bajo rendimientos decrecientes, un mayor $r$ reduce el alquiler real $q/p$; si el ahorro responde positivamente al rendimiento del capital, $s(r)$ es decreciente en $r$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C10-01` | - | La tasa de ahorro depende positivamente de la renta del capital $q/p$ (inversamente de $r$) | Si el ahorro aumentara al caer $q/p$, la curva $s(r)F(r,1)$ perdería su efecto estabilizador. | - |

---

### [C-11] Población Endógena y Trampa (Concept)

- **Bloom Level:** Evaluate
- **Session:** Unidad 28: Población Endógena y Trampa
- **Prerequisites:** C-10
- **Recommended Modalities:** invariant_canvas, adversarial_break, concept_matching
- **Evidence Citations:** `solow1956.pdf` (page 28)

#### Description & Cognitive Model
Endogeneización de la tasa de crecimiento poblacional $n(r)$ según el ingreso per cápita $F(r,1)$, produciendo múltiples equilibrios en $\dot{r}=sF(r,1)-n(r)r$: un equilibrio estable bajo $r_1$ y un umbral crítico inestable $r_2$.

#### Fused Distractor Models (3)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-C11-01` | Invierte estabilidad de equilibrios | conceptual_swap | high | $r_1$ es inestable y $r_2$ es estable | Analice el signo de $\dot{r}=sF(r,1)-n(r)r$: debajo de $r_1$ es positivo y entre $r_1$ y $r_2$ es negativo, por lo que $r_1$ atrae trayectorias y $r_2$ las repele. |
| `D-C11-02` | Requiere rendimientos crecientes para trampa | conceptual_swap | high | La trampa exige indivisibilidades o rendimientos crecientes | Solow demuestra que aun con rendimientos constantes a escala y sin indivisibilidades, una función poblacional $n(r)$ no monótona genera trampa en $r_1$ y despegue sobre $r_2$. |
| `D-C11-03` | Retorno tras gran impulso | conceptual_swap | high | Si $r_0 > r_2$, el sistema vuelve a $r_1$ | Por encima del umbral crítico $r_2$, $sF(r,1) > n(r)r$ ($\dot{r}>0$), desencadenando una expansión autosostenida del capital y del ingreso per cápita. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-C11-01` | - | La tasa de crecimiento poblacional $n(r)$ es negativa para ingresos muy bajos, creciente en niveles medios y decreciente en ingresos altos | Con $n$ constante o estrictamente monótona en sentido contrario desaparece la multiplicidad de equilibrios. | - |

---

### [Hab-10] Salario Rígido y Trampa de Liquidez (Skill)

- **Bloom Level:** Analyze
- **Session:** Unidad 29: Salario Rígido y Trampa de Liquidez
- **Prerequisites:** C-08, C-09
- **Recommended Modalities:** open_symbolic, proof_dag, adversarial_break
- **Evidence Citations:** `solow1956.pdf` (page 29)

#### Description & Cognitive Model
Determinar la dinámica de desempleo o escasez laboral cuando el salario real se fija en $\bar{w}/p$ (fijando $r=\bar{r}$), así como la subutilización del capital bajo preferencia por la liquidez $\bar{M}=Q(F(K,L),F_K(K,L))$.

#### Fused Distractor Models (6)

| Distractor ID | Trap / Name | Error Type | Severity | Misconception / Omitted Step | Remediation Hint |
|:---|:---|:---:|:---:|:---|:---|
| `D-Hab10-01` | Invierte condición de desempleo | skipped_step | high | $\frac{s}{\bar{r}}F(\bar{r},1) > n \Rightarrow$ desempleo | Compare la tasa de crecimiento del empleo $\dot{L}/L=(s/\bar{r})F(\bar{r},1)$ con la de la fuerza laboral $n$: si $(s/\bar{r})F(\bar{r},1) < n$ falta empleo y surge desempleo. |
| `D-Hab10-02` | Confunde pendiente del rayo en diagrama | skipped_step | high | Rayo más empinado que $n$ implica $\dot{r} < 0$ | La pendiente del rayo desde el origen a $sF(r,1)$ en $\bar{r}$ es $(s/\bar{r})F(\bar{r},1)$: si es más plana que $n$ ($\dot{r}<0$ en el caso flexible), habrá desempleo. |
| `D-Hab10-03` | Trampa de liquidez con tasa baja | conceptual_swap | high | Interés rígido por debajo del equilibrio subutiliza capital | Si la tasa de interés se vuelve rígida por encima del nivel correspondiente al $r^*$ de equilibrio, la demanda de capital en uso cae bajo la oferta y surge subutilización. |
| `D-Hab10-04` | Modelo real suficiente para liquidez | conceptual_swap | high | El modelo real basta para analizar preferencia por liquidez | Solow advierte que ante la elección entre efectivo y capital físico en la trampa de liquidez, el nivel de precios $p$ importa y se vuelve indispensable una dinámica monetaria. |
| `D-Hab10-05` | Salario rígido permite variar r | conceptual_swap | high | $K/L$ sigue variando con $\bar{w}/p$ fijo | Como las productividades marginales dependen solo de $r$, fijar $\bar{w}/p$ fija necesariamente la razón capital-trabajo en $\bar{r}$ mientras haya ajuste competitivo de $K/L$. |
| `D-Hab10-06` | Omite factor 1/r en tasa de empleo | conceptual_swap | high | $\frac{\dot{L}}{L} = sF(\bar{r},1)$ | Sustituya $K=\bar{r}L$ en $\dot{K}=sF(K,L)$ para obtener $\bar{r}\dot{L}=sF(\bar{r}L,L)$, y divida por $\bar{r}L$ usando rendimientos constantes: $\dot{L}/L=(s/\bar{r})F(\bar{r},1)$. |

#### Formal Mathematical Assumptions (1)

| Assumption ID | Name / Label | Formal Statement (LaTeX) | Violation Consequence | Role in Proof |
|:---|:---|:---|:---|:---|
| `A-Hab10-01` | - | Salario real rígido $\bar{w}/p$ con empleo determinado por igualdad de productividad marginal, o tasa de interés rígida en trampa de liquidez | Con precios y salarios perfectamente flexibles se restablece el pleno empleo de ambos factores. | - |

---
